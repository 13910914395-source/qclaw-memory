#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海南勘察招标日报 - 招标信息抓取脚本
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
    print("请确保已安装 websockets: pip install websockets")
    sys.exit(1)

# 关键词列表
KEYWORDS = ['勘察', '检测', '测绘', '岩土', '地质灾害']

# 时间范围：最近24小时
TIME_THRESHOLD = datetime.now() - timedelta(hours=24)

def extract_tender_info(html_content, source_name):
    """从HTML内容中提取招标信息"""
    tenders = []
    
    # 这里使用正则表达式提取招标信息
    # 实际网站结构可能不同，需要根据实际页面调整
    
    # 示例模式：查找包含关键词的招标条目
    for keyword in KEYWORDS:
        # 查找包含关键词的招标项目
        pattern = rf'<a[^>]*href="([^"]+)"[^>]*>.*?({keyword}[^<]+)</a>'
        matches = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            url, title = match
            tenders.append({
                'title': title.strip(),
                'url': url,
                'keyword': keyword,
                'source': source_name
            })
    
    return tenders

def scrape_cebpubservice():
    """抓取中国招标投标公共服务平台"""
    print("=" * 60)
    print("正在抓取: 中国招标投标公共服务平台")
    print("=" * 60)
    
    launcher = BrowserLauncher()
    tenders = []
    
    try:
        # 启动浏览器
        print("[1/4] 启动浏览器...")
        cdp_url = launcher.launch(browser='chrome', reuse_profile=True)
        print(f"✓ CDP URL: {cdp_url}")
        
        client = CDPClient(cdp_url)
        client.connect()
        
        # 检查已有标签页
        print("[2/4] 检查已有标签页...")
        tabs = client.list_tabs()
        target_tab = None
        for tab in tabs:
            if 'cebpubservice' in tab.get('url', ''):
                target_tab = tab
                break
        
        if target_tab:
            client.attach(target_tab['id'])
            print("✓ 复用已有标签页")
        else:
            # 创建新标签页
            print("[3/4] 创建新标签页...")
            tab = client.create_tab('https://www.cebpubservice.com')
            client.attach(tab['id'])
        
        snapshot = PageSnapshot(client)
        actions = BrowserActions(client, snapshot)
        
        # 等待页面加载
        print("[4/4] 等待页面加载...")
        actions.wait_for_load()
        
        # 获取页面内容
        tree = snapshot.accessibility_tree()
        print(f"✓ 页面已加载")
        
        # 搜索关键词
        for keyword in KEYWORDS:
            print(f"\n搜索关键词: {keyword}")
            # 尝试在搜索框中输入关键词
            try:
                # 获取快照查找搜索框
                tree = snapshot.accessibility_tree()
                
                # 查找搜索输入框
                search_box = None
                for line in tree.split('\n'):
                    if 'search' in line.lower() or '搜索' in line:
                        # 提取 ref
                        match = re.search(r'\[(e\d+)\]', line)
                        if match:
                            search_box = match.group(1)
                            break
                
                if search_box:
                    actions.click_by_ref(search_box)
                    actions.type_text(keyword)
                    # 查找搜索按钮
                    tree = snapshot.accessibility_tree()
                    for line in tree.split('\n'):
                        if 'button' in line.lower() and ('search' in line.lower() or '搜索' in line or '查询' in line):
                            match = re.search(r'\[(e\d+)\]', line)
                            if match:
                                actions.click_by_ref(match.group(1))
                                break
                    
                    # 等待结果加载
                    actions.wait_for_load()
                    
                    # 获取结果页面内容
                    html_content = actions.evaluate('document.documentElement.outerHTML')
                    
                    # 提取招标信息
                    results = extract_tender_info(html_content, '中国招标投标公共服务平台')
                    tenders.extend(results)
                    print(f"  找到 {len(results)} 条相关招标信息")
                    
            except Exception as e:
                print(f"  搜索失败: {e}")
                continue
        
        print(f"\n✓ 中国招标投标公共服务平台抓取完成，共 {len(tenders)} 条")
        
    except BrowserNeedsCDPError as e:
        print(f"⚠️ 浏览器需要手动授权: {e}")
    except Exception as e:
        print(f"❌ 抓取失败: {e}")
        import traceback
        traceback.print_exc()
    
    return tenders

def scrape_ccgp_hainan():
    """抓取海南省政府采购网"""
    print("\n" + "=" * 60)
    print("正在抓取: 海南省政府采购网")
    print("=" * 60)
    
    launcher = BrowserLauncher()
    tenders = []
    
    try:
        # 启动浏览器
        print("[1/4] 启动浏览器...")
        cdp_url = launcher.launch(browser='chrome', reuse_profile=True)
        print(f"✓ CDP URL: {cdp_url}")
        
        client = CDPClient(cdp_url)
        client.connect()
        
        # 检查已有标签页
        print("[2/4] 检查已有标签页...")
        tabs = client.list_tabs()
        target_tab = None
        for tab in tabs:
            if 'ccgp-hainan' in tab.get('url', ''):
                target_tab = tab
                break
        
        if target_tab:
            client.attach(target_tab['id'])
            print("✓ 复用已有标签页")
        else:
            # 创建新标签页
            print("[3/4] 创建新标签页...")
            tab = client.create_tab('https://www.ccgp-hainan.gov.cn')
            client.attach(tab['id'])
        
        snapshot = PageSnapshot(client)
        actions = BrowserActions(client, snapshot)
        
        # 等待页面加载
        print("[4/4] 等待页面加载...")
        actions.wait_for_load()
        
        # 获取页面内容
        tree = snapshot.accessibility_tree()
        print(f"✓ 页面已加载")
        
        # 搜索关键词
        for keyword in KEYWORDS:
            print(f"\n搜索关键词: {keyword}")
            try:
                # 获取快照查找搜索框
                tree = snapshot.accessibility_tree()
                
                # 查找搜索输入框
                search_box = None
                for line in tree.split('\n'):
                    if 'search' in line.lower() or '搜索' in line or 'textbox' in line.lower():
                        match = re.search(r'\[(e\d+)\]', line)
                        if match:
                            search_box = match.group(1)
                            break
                
                if search_box:
                    actions.click_by_ref(search_box)
                    actions.type_text(keyword)
                    
                    # 查找搜索按钮
                    tree = snapshot.accessibility_tree()
                    for line in tree.split('\n'):
                        if 'button' in line.lower() or '搜索' in line or '查询' in line:
                            match = re.search(r'\[(e\d+)\]', line)
                            if match:
                                actions.click_by_ref(match.group(1))
                                break
                    
                    # 等待结果加载
                    actions.wait_for_load()
                    
                    # 获取结果页面内容
                    html_content = actions.evaluate('document.documentElement.outerHTML')
                    
                    # 提取招标信息
                    results = extract_tender_info(html_content, '海南省政府采购网')
                    tenders.extend(results)
                    print(f"  找到 {len(results)} 条相关招标信息")
                    
            except Exception as e:
                print(f"  搜索失败: {e}")
                continue
        
        print(f"\n✓ 海南省政府采购网抓取完成，共 {len(tenders)} 条")
        
    except BrowserNeedsCDPError as e:
        print(f"⚠️ 浏览器需要手动授权: {e}")
    except Exception as e:
        print(f"❌ 抓取失败: {e}")
        import traceback
        traceback.print_exc()
    
    return tenders

def main():
    print("=" * 60)
    print("海南勘察招标日报 - 招标信息抓取")
    print(f"抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"关键词: {', '.join(KEYWORDS)}")
    print(f"时间范围: 最近24小时 ({TIME_THRESHOLD.strftime('%Y-%m-%d %H:%M:%S')} 至今)")
    print("=" * 60)
    
    all_tenders = []
    
    # 抓取中国招标投标公共服务平台
    tenders1 = scrape_cebpubservice()
    all_tenders.extend(tenders1)
    
    # 抓取海南省政府采购网
    tenders2 = scrape_ccgp_hainan()
    all_tenders.extend(tenders2)
    
    # 去重
    seen = set()
    unique_tenders = []
    for t in all_tenders:
        key = (t.get('title', ''), t.get('url', ''))
        if key not in seen:
            seen.add(key)
            unique_tenders.append(t)
    
    print("\n" + "=" * 60)
    print("抓取结果汇总")
    print("=" * 60)
    print(f"总计: {len(unique_tenders)} 条不重复招标信息")
    
    # 输出JSON结果
    result = {
        'fetch_time': datetime.now().isoformat(),
        'time_range': {
            'from': TIME_THRESHOLD.isoformat(),
            'to': datetime.now().isoformat()
        },
        'keywords': KEYWORDS,
        'total_count': len(unique_tenders),
        'tenders': unique_tenders
    }
    
    output_file = '/Users/fasimac/.qclaw/workspace/tender_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果已保存到: {output_file}")
    
    # 打印摘要
    print("\n招标信息摘要:")
    for i, t in enumerate(unique_tenders[:10], 1):
        print(f"{i}. [{t.get('source', '未知')}] {t.get('title', '无标题')[:50]}...")
    
    if len(unique_tenders) > 10:
        print(f"... 还有 {len(unique_tenders) - 10} 条")

if __name__ == '__main__':
    main()
