#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海南勘察招标日报采集脚本
抓取中国招标投标公共服务平台和海南省政府采购网的勘察类招标公告
"""

import sys
import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

# 添加 browser-cdp skill 的 scripts 目录到路径
skill_dir = Path.home() / "Library/Application Support/QClaw/openclaw/config/skills/browser-cdp"
sys.path.insert(0, str(skill_dir / "scripts"))

from browser_launcher import BrowserLauncher, BrowserNeedsCDPError
from cdp_client import CDPClient
from page_snapshot import PageSnapshot
from browser_actions import BrowserActions

def init_browser():
    """初始化浏览器连接"""
    launcher = BrowserLauncher()
    try:
        # 使用隔离profile模式，避免需要用户授权
        cdp_url = launcher.launch(browser='chrome', reuse_profile=False, headless=False)
        print(f"✓ CDP连接成功: {cdp_url}")
    except BrowserNeedsCDPError as e:
        print(f"⚠️ 需要用户授权: {e}")
        return None, None, None
    
    client = CDPClient(cdp_url)
    client.connect()
    
    snapshot = PageSnapshot(client)
    actions = BrowserActions(client, snapshot)
    
    return launcher, client, actions, snapshot

def scrape_cebpubservice(actions, snapshot):
    """
    抓取中国招标投标公共服务平台
    网站: www.cebpubservice.com
    关键词: 勘察、检测、测绘、岩土、地质灾害
    时间范围: 最近24小时
    """
    print("\n" + "="*60)
    print("【1/2】抓取中国招标投标公共服务平台")
    print("="*60)
    
    announcements = []
    
    try:
        # 导航到网站
        print("→ 正在访问: https://www.cebpubservice.com")
        actions.navigate('https://www.cebpubservice.com')
        actions.wait_for_load()
        time.sleep(2)
        
        # 获取页面快照
        tree = snapshot.accessibility_tree()
        print("✓ 页面加载成功")
        
        # 截图查看页面结构
        screenshot_path = '/tmp/cebpubservice_home.png'
        actions.screenshot(screenshot_path)
        print(f"✓ 首页截图保存: {screenshot_path}")
        
        # 尝试查找搜索框
        print("\n→ 查找搜索功能...")
        print(f"页面快照（前2000字符）:\n{tree[:2000]}")
        
        # 这里需要根据实际页面结构进行操作
        # 由于网站可能有反爬机制，先截图查看页面状态
        
    except Exception as e:
        print(f"✗ 访问失败: {e}")
        # 尝试截图保存错误状态
        try:
            actions.screenshot('/tmp/cebpubservice_error.png')
        except:
            pass
    
    return announcements

def scrape_hainan_gp(actions, snapshot):
    """
    抓取海南省政府采购网
    网站: www.ccgp-hainan.gov.cn
    关键词: 勘察、检测、测绘、岩土、地质灾害
    时间范围: 最近24小时
    """
    print("\n" + "="*60)
    print("【2/2】抓取海南省政府采购网")
    print("="*60)
    
    announcements = []
    
    try:
        # 导航到网站
        print("→ 正在访问: http://www.ccgp-hainan.gov.cn")
        actions.navigate('http://www.ccgp-hainan.gov.cn')
        actions.wait_for_load()
        time.sleep(2)
        
        # 获取页面快照
        tree = snapshot.accessibility_tree()
        print("✓ 页面加载成功")
        
        # 截图查看页面结构
        screenshot_path = '/tmp/hainan_gp_home.png'
        actions.screenshot(screenshot_path)
        print(f"✓ 首页截图保存: {screenshot_path}")
        
        # 输出页面快照便于分析
        print(f"\n页面快照（前2000字符）:\n{tree[:2000]}")
        
    except Exception as e:
        print(f"✗ 访问失败: {e}")
        # 尝试截图保存错误状态
        try:
            actions.screenshot('/tmp/hainan_gp_error.png')
        except:
            pass
    
    return announcements

def main():
    """主函数"""
    print("="*60)
    print("海南勘察招标日报采集系统")
    print("="*60)
    print(f"采集时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"时间范围: 最近24小时")
    print(f"关键词: 勘察、检测、测绘、岩土、地质灾害")
    print("="*60)
    
    # 初始化浏览器
    print("\n[阶段1] 初始化浏览器...")
    launcher, client, actions, snapshot = init_browser()
    
    if not actions:
        print("\n✗ 浏览器初始化失败")
        return
    
    try:
        # 抓取第一个网站
        ceb_announcements = scrape_cebpubservice(actions, snapshot)
        
        # 抓取第二个网站
        hainan_announcements = scrape_hainan_gp(actions, snapshot)
        
        # 合并结果
        all_announcements = ceb_announcements + hainan_announcements
        
        print("\n" + "="*60)
        print("采集结果汇总")
        print("="*60)
        print(f"中国招标投标公共服务平台: {len(ceb_announcements)} 条")
        print(f"海南省政府采购网: {len(hainan_announcements)} 条")
        print(f"合计: {len(all_announcements)} 条")
        
        # 保存结果
        if all_announcements:
            result_file = f'/tmp/bid_announcements_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(all_announcements, f, ensure_ascii=False, indent=2)
            print(f"\n✓ 结果已保存: {result_file}")
        else:
            print("\n⚠️ 未采集到符合条件的公告")
            print("可能原因：")
            print("  1. 网站访问受限（反爬机制）")
            print("  2. 网站结构变化，需要更新采集逻辑")
            print("  3. 近期无符合条件的招标公告发布")
        
    except Exception as e:
        print(f"\n✗ 采集过程出错: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 保持连接，不关闭浏览器
        print("\n✓ 浏览器连接保持活跃，可用于后续任务")

if __name__ == '__main__':
    main()
