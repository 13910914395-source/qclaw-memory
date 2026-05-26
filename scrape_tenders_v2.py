#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海南勘察招标日报 - 招标信息抓取脚本 (改进版)
直接访问搜索页面和公告列表
"""

import sys
import os
import json
import re
from datetime import datetime, timedelta
from urllib.parse import urljoin, quote

# 添加 browser-cdp skill 脚本路径
sys.path.insert(0, os.path.expanduser('~/Library/Application Support/QClaw/openclaw/config/skills/browser-cdp/scripts'))

try:
    from browser_launcher import BrowserLauncher, BrowserNeedsCDPError
    from cdp_client import CDPClient
    from page_snapshot import PageSnapshot
    from browser_actions import BrowserActions
except ImportError as e:
    print(f"导入 browser-cdp 模块失败: {e}")
    sys.exit(1)

# 关键词列表
KEYWORDS = ['勘察', '检测', '测绘', '岩土', '地质灾害']

class TenderScraper:
    def __init__(self):
        self.launcher = None
        self.client = None
        self.all_tenders = []
        
    def init_browser(self):
        """初始化浏览器"""
        self.launcher = BrowserLauncher()
        cdp_url = self.launcher.launch(browser='chrome', reuse_profile=True)
        self.client = CDPClient(cdp_url)
        self.client.connect()
        return cdp_url
        
    def navigate_to(self, url):
        """导航到指定URL"""
        # 检查已有标签页
        tabs = self.client.list_tabs()
        for tab in tabs:
            if url in tab.get('url', ''):
                self.client.attach(tab['id'])
                return
        
        # 创建新标签页
        tab = self.client.create_tab(url)
        self.client.attach(tab['id'])
    
    def wait_and_get_html(self, actions, snapshot):
        """等待加载并获取HTML"""
        actions.wait_for_load()
        # 额外等待动态内容加载
        import time
        time.sleep(2)
        return actions.evaluate('document.documentElement.outerHTML')
    
    def extract_tenders_from_html(self, html, source):
        """从HTML中提取招标信息"""
        tenders = []
        
        # 尝试多种模式匹配招标信息
        # 模式1: 表格行中的招标信息
        table_patterns = [
            r'<tr[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>.*?</tr>',
            r'<tr[^>]*>.*?<td[^>]*>([^<]+)</td>.*?<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>.*?</tr>',
        ]
        
        # 模式2: 列表中的招标信息
        list_patterns = [
            r'<li[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>.*?</li>',
            r'<div[^>]*class="[^"]*(?:item|list|row)[^"]*"[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>.*?</div>',
        ]
        
        all_patterns = table_patterns + list_patterns
        
        for pattern in all_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if len(match) >= 2:
                    url = match[0] if 'http' in match[0] else match[1] if len(match) > 1 and 'http' in match[1] else match[0]
                    title = match[1] if len(match) > 1 and 'http' not in match[1] else match[0]
                    
                    # 检查是否包含关键词
                    for keyword in KEYWORDS:
                        if keyword in title:
                            tenders.append({
                                'title': re.sub(r'<[^>]+>', '', title).strip(),
                                'url': url if url.startswith('http') else '',
                                'keyword': keyword,
                                'source': source
                            })
                            break
        
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
            # 尝试直接访问搜索结果页面
            for keyword in KEYWORDS:
                print(f"\n搜索: {keyword}")
                
                # 构造搜索URL
                search_url = f"https://www.cebpubservice.com/search/search.htm?search={quote(keyword)}"
                self.navigate_to(search_url)
                html = self.wait_and_get_html(actions, snapshot)
                
                # 提取招标信息
                results = self.extract_tenders_from_html(html, '中国招标投标公共服务平台')
                tenders.extend(results)
                print(f"  找到 {len(results)} 条")
                
                # 获取快照查看页面结构
                tree = snapshot.accessibility_tree()
                print(f"  页面结构预览 (前500字符):")
                print(f"  {tree[:500]}...")
                
        except Exception as e:
            print(f"❌ 抓取失败: {e}")
            import traceback
            traceback.print_exc()
        
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
            # 先访问首页了解结构
            self.navigate_to('https://www.ccgp-hainan.gov.cn/')
            html = self.wait_and_get_html(actions, snapshot)
            
            # 获取快照
            tree = snapshot.accessibility_tree()
            print("页面结构:")
            print(tree[:1000])
            
            # 尝试搜索
            for keyword in KEYWORDS:
                print(f"\n搜索: {keyword}")
                
                # 尝试找到搜索框
                search_input = None
                for line in tree.split('\n'):
                    if 'textbox' in line.lower() or 'input' in line.lower() or '搜索' in line:
                        match = re.search(r'\[(e\d+)\]', line)
                        if match:
                            search_input = match.group(1)
                            print(f"  找到搜索框: {line[:100]}")
                            break
                
                if search_input:
                    try:
                        actions.click_by_ref(search_input)
                        actions.type_text(keyword)
                        
                        # 查找搜索按钮
                        tree = snapshot.accessibility_tree()
                        search_btn = None
                        for line in tree.split('\n'):
                            if 'button' in line.lower() or '搜索' in line or '查询' in line:
                                match = re.search(r'\[(e\d+)\]', line)
                                if match:
                                    search_btn = match.group(1)
                                    break
                        
                        if search_btn:
                            actions.click_by_ref(search_btn)
                            html = self.wait_and_get_html(actions, snapshot)
                            results = self.extract_tenders_from_html(html, '海南省政府采购网')
                            tenders.extend(results)
                            print(f"  找到 {len(results)} 条")
                        
                    except Exception as e:
                        print(f"  搜索操作失败: {e}")
                else:
                    print("  未找到搜索框")
                    
        except Exception as e:
            print(f"❌ 抓取失败: {e}")
            import traceback
            traceback.print_exc()
        
        return tenders
    
    def run(self):
        """运行抓取任务"""
        print("=" * 60)
        print("海南勘察招标日报 - 招标信息抓取")
        print(f"抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"关键词: {', '.join(KEYWORDS)}")
        print("=" * 60)
        
        try:
            # 初始化浏览器
            print("\n[初始化] 启动浏览器...")
            self.init_browser()
            print("✓ 浏览器已连接")
            
            # 抓取两个网站
            tenders1 = self.scrape_cebpubservice()
            self.all_tenders.extend(tenders1)
            
            tenders2 = self.scrape_ccgp_hainan()
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
            key = (t.get('title', ''), t.get('url', ''))
            if key not in seen and t.get('title'):
                seen.add(key)
                unique_tenders.append(t)
        
        # 输出结果
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
            for i, t in enumerate(unique_tenders[:20], 1):
                print(f"{i}. [{t.get('source', '未知')}] {t.get('title', '无标题')[:60]}")
        else:
            print("\n⚠️ 未找到符合条件的招标信息")
        
        return unique_tenders

if __name__ == '__main__':
    scraper = TenderScraper()
    scraper.run()
