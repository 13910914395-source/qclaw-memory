#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海南勘察招标日报 - 招标信息抓取脚本 (V3)
直接访问公告列表页面
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
    
    def wait_and_get_content(self, actions, snapshot):
        import time
        actions.wait_for_load()
        time.sleep(3)
        html = actions.evaluate('document.documentElement.outerHTML')
        tree = snapshot.accessibility_tree()
        return html, tree
    
    def parse_tenders_from_tree(self, tree, source, base_url):
        """从Accessibility Tree解析招标信息"""
        tenders = []
        lines = tree.split('\n')
        
        for i, line in enumerate(lines):
            # 查找包含关键词的链接
            for keyword in KEYWORDS:
                if keyword in line and ('link' in line.lower() or '公告' in line):
                    # 提取标题
                    title_match = re.search(r'link\s+"([^"]+)"', line)
                    if title_match:
                        title = title_match.group(1)
                        # 提取ref
                        ref_match = re.search(r'\[(e\d+)\]', line)
                        ref = ref_match.group(1) if ref_match else None
                        
                        tenders.append({
                            'title': title,
                            'ref': ref,
                            'keyword': keyword,
                            'source': source,
                            'line': line[:200]
                        })
                        break
        
        return tenders
    
    def scrape_ccgp_hainan_notices(self):
        """抓取海南省政府采购网公告信息"""
        print("\n" + "=" * 60)
        print("正在抓取: 海南省政府采购网 - 公告信息")
        print("=" * 60)
        
        tenders = []
        snapshot = PageSnapshot(self.client)
        actions = BrowserActions(self.client, snapshot)
        
        try:
            # 访问公告信息页面
            notice_urls = [
                'https://www.ccgp-hainan.gov.cn/notices.html',
                'https://www.ccgp-hainan.gov.cn/notices/list',
            ]
            
            for url in notice_urls:
                print(f"\n尝试访问: {url}")
                try:
                    self.navigate_to(url)
                    html, tree = self.wait_and_get_content(actions, snapshot)
                    
                    print(f"页面内容长度: {len(html)}")
                    print(f"页面结构预览 (前2000字符):")
                    print(tree[:2000])
                    
                    # 解析招标信息
                    results = self.parse_tenders_from_tree(tree, '海南省政府采购网', url)
                    tenders.extend(results)
                    print(f"\n找到 {len(results)} 条潜在招标信息")
                    
                except Exception as e:
                    print(f"访问失败: {e}")
                    continue
            
            # 尝试点击"公告信息"菜单
            print("\n尝试通过菜单导航到公告页面...")
            self.navigate_to('https://www.ccgp-hainan.gov.cn/')
            html, tree = self.wait_and_get_content(actions, snapshot)
            
            # 查找公告信息链接
            for line in tree.split('\n'):
                if '公告信息' in line or '公告' in line:
                    print(f"找到菜单: {line[:150]}")
                    ref_match = re.search(r'\[(e\d+)\]', line)
                    if ref_match:
                        try:
                            actions.click_by_ref(ref_match.group(1))
                            html, tree = self.wait_and_get_content(actions, snapshot)
                            print(f"\n公告页面结构 (前2000字符):")
                            print(tree[:2000])
                            
                            results = self.parse_tenders_from_tree(tree, '海南省政府采购网', '')
                            tenders.extend(results)
                            break
                        except Exception as e:
                            print(f"点击失败: {e}")
            
        except Exception as e:
            print(f"❌ 抓取失败: {e}")
            import traceback
            traceback.print_exc()
        
        return tenders
    
    def scrape_cebpubservice_search(self):
        """抓取中国招标投标公共服务平台"""
        print("\n" + "=" * 60)
        print("正在抓取: 中国招标投标公共服务平台")
        print("=" * 60)
        
        tenders = []
        snapshot = PageSnapshot(self.client)
        actions = BrowserActions(self.client, snapshot)
        
        try:
            # 尝试不同的搜索URL格式
            search_urls = [
                'https://www.cebpubservice.com/search/search.htm',
                'https://www.cebpubservice.com/',
            ]
            
            for url in search_urls:
                print(f"\n尝试访问: {url}")
                try:
                    self.navigate_to(url)
                    html, tree = self.wait_and_get_content(actions, snapshot)
                    
                    print(f"页面结构预览 (前2000字符):")
                    print(tree[:2000])
                    
                    # 查找搜索框
                    for line in tree.split('\n'):
                        if 'search' in line.lower() or '搜索' in line or 'textbox' in line.lower():
                            print(f"找到输入元素: {line[:150]}")
                    
                except Exception as e:
                    print(f"访问失败: {e}")
        
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
            tenders1 = self.scrape_ccgp_hainan_notices()
            self.all_tenders.extend(tenders1)
            
            # 抓取中国招标投标公共服务平台
            tenders2 = self.scrape_cebpubservice_search()
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
            for i, t in enumerate(unique_tenders[:30], 1):
                print(f"{i}. [{t.get('source', '未知')}] {t.get('title', '无标题')[:70]}")
        else:
            print("\n⚠️ 未找到符合条件的招标信息")
        
        return unique_tenders

if __name__ == '__main__':
    scraper = TenderScraper()
    scraper.run()
