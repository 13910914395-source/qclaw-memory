#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海南勘察招标日报 - 招标信息抓取脚本 (V4)
点击菜单获取招标公告
"""

import sys
import os
import json
import re
from datetime import datetime, timedelta
from urllib.parse import urljoin, quote

sys.path.insert(0, os.path.expanduser('~/Library/Application Support/QClaw/openclaw/config/skills/browser-cdp/scripts'))

try:
    from browser_launcher import BrowserLauncher, BrowserNeedsCDPError
    from cdp_client import CDPClient
    from page_snapshot import PageSnapshot
    from browser_actions import BrowserActions
except ImportError as e:
    print(f"导入 browser-cdp 模块失败: {e}")
    sys.exit(1)

KEYWORDS = ['勘察', '检测', '测绘', '岩土', '地质灾害']

class TenderScraper:
    def __init__(self):
        self.launcher = None
        self.client = None
        self.all_tenders = []
        
    def init_browser(self):
        self.launcher = BrowserLauncher()
        cdp_url = self.launcher.launch(browser='chrome', reuse_profile=True)
        self.client = CDPClient(cdp_url)
        self.client.connect()
        return cdp_url
        
    def navigate_to(self, url):
        tabs = self.client.list_tabs()
        for tab in tabs:
            if url in tab.get('url', ''):
                self.client.attach(tab['id'])
                return
        tab = self.client.create_tab(url)
        self.client.attach(tab['id'])
    
    def wait_and_get_content(self, actions, snapshot, wait_time=3):
        import time
        actions.wait_for_load()
        time.sleep(wait_time)
        html = actions.evaluate('document.documentElement.outerHTML')
        tree = snapshot.accessibility_tree()
        return html, tree
    
    def find_and_click_by_text(self, actions, snapshot, text_keywords, max_depth=3):
        """根据文本关键词查找并点击元素"""
        for attempt in range(max_depth):
            tree = snapshot.accessibility_tree()
            for line in tree.split('\n'):
                for keyword in text_keywords:
                    if keyword in line:
                        ref_match = re.search(r'\[(e\d+)\]', line)
                        if ref_match:
                            try:
                                actions.click_by_ref(ref_match.group(1))
                                return True, line
                            except Exception as e:
                                print(f"  点击失败: {e}")
                                continue
        return False, None
    
    def extract_links_from_tree(self, tree, source):
        """从Accessibility Tree中提取所有链接"""
        tenders = []
        lines = tree.split('\n')
        
        for line in lines:
            # 查找link元素
            if 'link' in line.lower():
                # 提取标题
                title_match = re.search(r'link\s+"([^"]+)"', line)
                if title_match:
                    title = title_match.group(1)
                    # 检查是否包含关键词
                    for keyword in KEYWORDS:
                        if keyword in title:
                            ref_match = re.search(r'\[(e\d+)\]', line)
                            tenders.append({
                                'title': title,
                                'ref': ref_match.group(1) if ref_match else None,
                                'keyword': keyword,
                                'source': source
                            })
                            break
        
        return tenders
    
    def scrape_ccgp_hainan(self):
        """抓取海南省政府采购网"""
        print("\n" + "=" * 60)
        print("正在抓取: 海南省政府采购网")
        print("=" * 60)
        
        tenders = []
        snapshot = PageSnapshot(self.client)
        actions = BrowserActions(self.client, snapshot)
        
        try:
            # 访问首页
            self.navigate_to('https://www.ccgp-hainan.gov.cn/')
            html, tree = self.wait_and_get_content(actions, snapshot)
            
            print("\n1. 点击'公告信息'菜单...")
            clicked, line = self.find_and_click_by_text(actions, snapshot, ['公告信息'])
            if clicked:
                print(f"   已点击: {line[:100]}")
                html, tree = self.wait_and_get_content(actions, snapshot, 5)
            
            print("\n2. 点击'采购公告'子菜单...")
            clicked, line = self.find_and_click_by_text(actions, snapshot, ['采购公告'])
            if clicked:
                print(f"   已点击: {line[:100]}")
                html, tree = self.wait_and_get_content(actions, snapshot, 5)
            
            print("\n3. 完整页面结构 (前5000字符):")
            print(tree[:5000])
            
            # 提取招标信息
            print("\n4. 提取招标信息...")
            results = self.extract_links_from_tree(tree, '海南省政府采购网')
            tenders.extend(results)
            print(f"   找到 {len(results)} 条")
            
            # 尝试翻页获取更多
            print("\n5. 尝试翻页获取更多数据...")
            for page in range(2, 6):  # 尝试获取前5页
                print(f"   尝试翻页到第 {page} 页...")
                # 查找下一页按钮
                tree = snapshot.accessibility_tree()
                next_clicked = False
                for line in tree.split('\n'):
                    if ('下一页' in line or 'next' in line.lower() or 
                        str(page) in line or '>' in line):
                        ref_match = re.search(r'\[(e\d+)\]', line)
                        if ref_match:
                            try:
                                actions.click_by_ref(ref_match.group(1))
                                html, tree = self.wait_and_get_content(actions, snapshot, 3)
                                results = self.extract_links_from_tree(tree, '海南省政府采购网')
                                tenders.extend(results)
                                print(f"   第 {page} 页找到 {len(results)} 条")
                                next_clicked = True
                                break
                            except:
                                continue
                if not next_clicked:
                    print("   未找到翻页按钮，停止翻页")
                    break
            
        except Exception as e:
            print(f"❌ 抓取失败: {e}")
            import traceback
            traceback.print_exc()
        
        return tenders
    
    def scrape_cebpubservice(self):
        """抓取中国招标投标公共服务平台"""
        print("\n" + "=" * 60)
        print("正在抓取: 中国招标投标公共服务平台")
        print("=" * 60)
        
        tenders = []
        snapshot = PageSnapshot(self.client)
        actions = BrowserActions(self.client, snapshot)
        
        try:
            # 尝试直接访问搜索页面
            urls_to_try = [
                'https://www.cebpubservice.com/',
                'https://www.cebpubservice.com/search.htm',
                'https://www.cebpubservice.com/tendersearch.htm',
            ]
            
            for url in urls_to_try:
                print(f"\n尝试访问: {url}")
                try:
                    self.navigate_to(url)
                    html, tree = self.wait_and_get_content(actions, snapshot, 5)
                    
                    if '502' in tree or 'Bad Gateway' in tree:
                        print("   返回502错误，尝试下一个URL...")
                        continue
                    
                    print(f"页面结构 (前3000字符):")
                    print(tree[:3000])
                    
                    # 提取招标信息
                    results = self.extract_links_from_tree(tree, '中国招标投标公共服务平台')
                    tenders.extend(results)
                    print(f"找到 {len(results)} 条")
                    
                    if tenders:
                        break
                        
                except Exception as e:
                    print(f"   访问失败: {e}")
                    continue
        
        except Exception as e:
            print(f"❌ 抓取失败: {e}")
        
        return tenders
    
    def run(self):
        print("=" * 60)
        print("海南勘察招标日报 - 招标信息抓取")
        print(f"抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"关键词: {', '.join(KEYWORDS)}")
        print("=" * 60)
        
        try:
            print("\n[初始化] 启动浏览器...")
            self.init_browser()
            print("✓ 浏览器已连接")
            
            # 抓取海南省政府采购网
            tenders1 = self.scrape_ccgp_hainan()
            self.all_tenders.extend(tenders1)
            
            # 抓取中国招标投标公共服务平台
            tenders2 = self.scrape_cebpubservice()
            self.all_tenders.extend(tenders2)
            
        except BrowserNeedsCDPError as e:
            print(f"⚠️ 浏览器需要手动授权: {e}")
        except Exception as e:
            print(f"❌ 错误: {e}")
            import traceback
            traceback.print_exc()
        
        # 去重
        seen = set()
        unique_tenders = []
        for t in self.all_tenders:
            key = t.get('title', '')
            if key and key not in seen:
                seen.add(key)
                unique_tenders.append(t)
        
        print("\n" + "=" * 60)
        print("抓取结果汇总")
        print("=" * 60)
        print(f"总计: {len(unique_tenders)} 条不重复招标信息")
        
        result = {
            'fetch_time': datetime.now().isoformat(),
            'keywords': KEYWORDS,
            'total_count': len(unique_tenders),
            'tenders': unique_tenders
        }
        
        output_file = '/Users/fasimac/.qclaw/workspace/tender_results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n结果已保存到: {output_file}")
        
        if unique_tenders:
            print("\n招标信息列表:")
            for i, t in enumerate(unique_tenders[:50], 1):
                print(f"{i}. [{t.get('source', '未知')}] {t.get('title', '无标题')[:80]}")
        else:
            print("\n⚠️ 未找到符合条件的招标信息")
        
        return unique_tenders

if __name__ == '__main__':
    scraper = TenderScraper()
    scraper.run()
