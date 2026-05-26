#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海南勘察招标日报 - 招标信息抓取脚本 (V5)
使用搜索功能查找招标信息
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
    
    def search_and_extract(self, actions, snapshot, keyword, source):
        """搜索关键词并提取结果"""
        tenders = []
        
        # 获取当前页面结构
        tree = snapshot.accessibility_tree()
        
        # 查找搜索框
        search_ref = None
        for line in tree.split('\n'):
            if 'textbox' in line.lower() and ('输入' in line or '搜索' in line or 'query' in line.lower()):
                match = re.search(r'\[(e\d+)\]', line)
                if match:
                    search_ref = match.group(1)
                    print(f"   找到搜索框: {line[:80]}")
                    break
        
        if not search_ref:
            print("   未找到搜索框")
            return tenders
        
        try:
            # 清空搜索框并输入关键词
            actions.click_by_ref(search_ref)
            # 使用Ctrl+A全选然后输入新内容
            actions.evaluate('document.activeElement.select()')
            import time
            time.sleep(0.5)
            actions.type_text(keyword)
            time.sleep(0.5)
            
            # 查找搜索按钮
            tree = snapshot.accessibility_tree()
            search_btn = None
            for line in tree.split('\n'):
                if ('button' in line.lower() or 'link' in line.lower()) and ('搜索' in line or 'search' in line.lower()):
                    match = re.search(r'\[(e\d+)\]', line)
                    if match:
                        search_btn = match.group(1)
                        print(f"   找到搜索按钮: {line[:80]}")
                        break
            
            if search_btn:
                actions.click_by_ref(search_btn)
                print(f"   已点击搜索按钮")
            else:
                # 尝试按回车键
                actions.press_key('Return')
                print(f"   已按回车键搜索")
            
            # 等待搜索结果加载
            time.sleep(5)
            html, tree = self.wait_and_get_content(actions, snapshot, 3)
            
            print(f"   搜索结果页面结构 (前2000字符):")
            print(f"   {tree[:2000]}")
            
            # 提取招标信息
            lines = tree.split('\n')
            for line in lines:
                if 'link' in line.lower():
                    title_match = re.search(r'link\s+"([^"]+)"', line)
                    if title_match:
                        title = title_match.group(1)
                        # 检查是否包含关键词
                        if keyword in title:
                            ref_match = re.search(r'\[(e\d+)\]', line)
                            tenders.append({
                                'title': title,
                                'ref': ref_match.group(1) if ref_match else None,
                                'keyword': keyword,
                                'source': source
                            })
            
        except Exception as e:
            print(f"   搜索失败: {e}")
        
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
            html, tree = self.wait_and_get_content(actions, snapshot, 3)
            
            print("\n首页结构 (前1500字符):")
            print(tree[:1500])
            
            # 对每个关键词进行搜索
            for keyword in KEYWORDS:
                print(f"\n搜索关键词: {keyword}")
                results = self.search_and_extract(actions, snapshot, keyword, '海南省政府采购网')
                tenders.extend(results)
                print(f"   找到 {len(results)} 条")
                
                # 刷新页面以准备下一次搜索
                self.navigate_to('https://www.ccgp-hainan.gov.cn/')
                html, tree = self.wait_and_get_content(actions, snapshot, 3)
            
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
            # 尝试访问
            self.navigate_to('https://www.cebpubservice.com/')
            html, tree = self.wait_and_get_content(actions, snapshot, 5)
            
            if '502' in tree or 'Bad Gateway' in tree:
                print("   网站返回502错误，无法访问")
                return tenders
            
            print(f"页面结构 (前2000字符):")
            print(tree[:2000])
            
            # 对每个关键词进行搜索
            for keyword in KEYWORDS:
                print(f"\n搜索关键词: {keyword}")
                results = self.search_and_extract(actions, snapshot, keyword, '中国招标投标公共服务平台')
                tenders.extend(results)
                print(f"   找到 {len(results)} 条")
        
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
