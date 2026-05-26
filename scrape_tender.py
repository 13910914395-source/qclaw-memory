#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海南勘察招标日报 - 招标信息抓取脚本
抓取中国招标投标公共服务平台和海南省政府采购网的勘察类招标公告
"""

import sys
import os
import json
import re
import base64
from datetime import datetime, timedelta
from urllib.parse import urljoin, quote

# 添加 browser-cdp skill 脚本路径
skill_dir = os.path.expanduser("~/Library/Application Support/QClaw/openclaw/config/skills/browser-cdp")
sys.path.insert(0, os.path.join(skill_dir, "scripts"))

from browser_launcher import BrowserLauncher, BrowserNeedsCDPError
from cdp_client import CDPClient
from page_snapshot import PageSnapshot
from browser_actions import BrowserActions

# 关键词
KEYWORDS = ["勘察", "检测", "测绘", "岩土", "地质灾害"]

# 目标网站
CEB_URL = "https://www.cebpubservice.com"  # 中国招标投标公共服务平台
CCGP_HAINAN_URL = "http://www.ccgp-hainan.gov.cn"  # 海南省政府采购网

def setup_browser():
    """启动浏览器并返回CDP客户端"""
    launcher = BrowserLauncher()
    try:
        # 使用隔离profile启动新实例，避免需要用户授权
        cdp_url = launcher.launch(browser='chrome', reuse_profile=False, wait_for_user=False)
    except BrowserNeedsCDPError as e:
        print(f"⚠️ 浏览器CDP连接失败: {e}")
        print("请确保Chrome浏览器已开启远程调试端口")
        sys.exit(1)
    
    client = CDPClient(cdp_url)
    client.connect()
    return client, launcher

def get_yesterday_date():
    """获取昨天的日期字符串"""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")

def scrape_cebpubservice(client):
    """
    抓取中国招标投标公共服务平台
    返回招标公告列表
    """
    print("\n=== 正在抓取中国招标投标公共服务平台 ===")
    
    snapshot = PageSnapshot(client)
    actions = BrowserActions(client, snapshot)
    
    # 搜索关键词组合
    all_results = []
    
    for keyword in KEYWORDS:
        print(f"\n搜索关键词: {keyword}")
        try:
            # 构建搜索URL - 使用平台的搜索功能
            search_url = f"{CEB_URL}/search/search.htm?keyword={quote(keyword)}"
            
            # 检查已有标签页
            tabs = client.list_tabs()
            tab = None
            for t in tabs:
                if 'cebpubservice' in t.get('url', ''):
                    tab = t
                    break
            
            if tab:
                client.attach(tab['id'])
                actions.navigate(search_url)
            else:
                tab = client.create_tab(search_url)
                client.attach(tab['id'])
            
            actions.wait_for_load()
            import time
            time.sleep(3)  # 等待搜索结果加载
            
            # 获取页面内容
            tree = snapshot.accessibility_tree()
            
            # 尝试通过JavaScript获取更详细的列表数据
            js_result = actions.evaluate("""
                (function() {
                    var results = [];
                    // 尝试多种可能的选择器
                    var rows = document.querySelectorAll('.search-result-item, .list-item, tr, .item');
                    
                    rows.forEach(function(row) {
                        var titleEl = row.querySelector('a, .title, .name');
                        var dateEl = row.querySelector('.date, .time, td:nth-child(3), td:nth-child(4)');
                        var linkEl = row.querySelector('a');
                        
                        if (titleEl && titleEl.textContent.trim()) {
                            var title = titleEl.textContent.trim();
                            var date = dateEl ? dateEl.textContent.trim() : '';
                            var link = linkEl ? linkEl.href : '';
                            
                            // 检查是否包含关键词
                            var hasKeyword = ['勘察', '检测', '测绘', '岩土', '地质灾害'].some(function(kw) {
                                return title.includes(kw);
                            });
                            
                            if (hasKeyword) {
                                results.push({
                                    title: title,
                                    date: date,
                                    link: link,
                                    source: '中国招标投标公共服务平台'
                                });
                            }
                        }
                    });
                    
                    return {
                        results: results.slice(0, 50),
                        pageTitle: document.title,
                        pageUrl: window.location.href
                    };
                })()
            """)
            
            if js_result and 'results' in js_result:
                results = js_result['results']
                print(f"找到 {len(results)} 条相关公告")
                all_results.extend(results)
            
        except Exception as e:
            print(f"搜索关键词 '{keyword}' 时出错: {e}")
            continue
    
    # 去重
    seen_titles = set()
    unique_results = []
    for item in all_results:
        if item['title'] not in seen_titles:
            seen_titles.add(item['title'])
            unique_results.append(item)
    
    print(f"\n中国招标投标公共服务平台共找到 {len(unique_results)} 条去重后的公告")
    return unique_results[:50]

def scrape_ccgp_hainan(client):
    """
    抓取海南省政府采购网
    返回招标公告列表
    """
    print("\n=== 正在抓取海南省政府采购网 ===")
    
    snapshot = PageSnapshot(client)
    actions = BrowserActions(client, snapshot)
    
    all_results = []
    
    for keyword in KEYWORDS:
        print(f"\n搜索关键词: {keyword}")
        try:
            # 海南省政府采购网搜索URL
            search_url = f"{CCGP_HAINAN_URL}/cgxgg/gzgg/"
            
            # 检查已有标签页
            tabs = client.list_tabs()
            tab = None
            for t in tabs:
                if 'ccgp-hainan' in t.get('url', ''):
                    tab = t
                    break
            
            if tab:
                client.attach(tab['id'])
                actions.navigate(search_url)
            else:
                tab = client.create_tab(search_url)
                client.attach(tab['id'])
            
            actions.wait_for_load()
            import time
            time.sleep(3)
            
            # 获取页面内容
            js_result = actions.evaluate("""
                (function() {
                    var results = [];
                    var rows = document.querySelectorAll('tr, .list-item, .item, li');
                    
                    rows.forEach(function(row) {
                        var titleEl = row.querySelector('a, .title, .name, td:nth-child(2)');
                        var dateEl = row.querySelector('.date, .time, td:last-child');
                        var linkEl = row.querySelector('a');
                        
                        if (titleEl && titleEl.textContent.trim()) {
                            var title = titleEl.textContent.trim();
                            var date = dateEl ? dateEl.textContent.trim() : '';
                            var link = linkEl ? linkEl.href : '';
                            
                            var hasKeyword = ['勘察', '检测', '测绘', '岩土', '地质灾害'].some(function(kw) {
                                return title.includes(kw);
                            });
                            
                            if (hasKeyword) {
                                results.push({
                                    title: title,
                                    date: date,
                                    link: link,
                                    source: '海南省政府采购网'
                                });
                            }
                        }
                    });
                    
                    return {
                        results: results.slice(0, 50),
                        pageTitle: document.title
                    };
                })()
            """)
            
            if js_result and 'results' in js_result:
                results = js_result['results']
                print(f"找到 {len(results)} 条相关公告")
                all_results.extend(results)
                
        except Exception as e:
            print(f"搜索关键词 '{keyword}' 时出错: {e}")
            continue
    
    # 去重
    seen_titles = set()
    unique_results = []
    for item in all_results:
        if item['title'] not in seen_titles:
            seen_titles.add(item['title'])
            unique_results.append(item)
    
    print(f"\n海南省政府采购网共找到 {len(unique_results)} 条去重后的公告")
    return unique_results[:50]

def filter_recent_items(items, hours=24):
    """
    过滤最近24小时内发布的公告
    """
    recent_items = []
    now = datetime.now()
    cutoff = now - timedelta(hours=hours)
    
    for item in items:
        date_str = item.get('date', '')
        if not date_str:
            continue
            
        # 尝试解析各种日期格式
        try:
            # 格式: 2025-04-12 或 2025/04/12 或 2025年04月12日
            date_str_clean = re.sub(r'[年月/]', '-', date_str)
            date_str_clean = date_str_clean.replace('日', '').strip()
            
            # 尝试解析
            for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S']:
                try:
                    item_date = datetime.strptime(date_str_clean[:len(fmt.replace('%', ''))-3], '%Y-%m-%d')
                    if item_date >= cutoff:
                        recent_items.append(item)
                    break
                except:
                    continue
        except:
            # 如果无法解析日期，保留该项（保守策略）
            recent_items.append(item)
    
    return recent_items

def is_relevant_project(title):
    """
    智能识别真实勘察类项目
    排除仅含'勘察'字样的无关项目
    """
    # 必须包含的核心勘察相关词汇
    core_keywords = ['勘察', '勘查', '检测', '测绘', '岩土', '地质', '勘探', '测量', '测试']
    
    # 排除词（这些词出现时，可能不是真正的勘察项目）
    exclude_keywords = ['勘察设计一体化', '勘察设计总承包', '仅勘察设计', '勘察设计咨询']
    
    # 检查是否包含核心关键词
    has_core = any(kw in title for kw in core_keywords)
    
    # 检查是否被排除
    is_excluded = any(kw in title for kw in exclude_keywords)
    
    # 如果是纯设计类项目（含勘察设计但主要是设计），降低相关性
    if '设计' in title and not any(kw in title for kw in ['勘察', '勘查', '岩土', '地质']):
        return False
    
    return has_core and not is_excluded

def extract_project_info(item):
    """
    从公告标题中提取项目信息
    返回结构化数据
    """
    title = item.get('title', '')
    
    # 尝试提取预算金额
    budget_patterns = [
        r'(\d+(?:\.\d+)?)\s*万',
        r'(\d+(?:\.\d+)?)\s*万元',
        r'预算.*?([\d,]+(?:\.\d+)?)',
        r'金额.*?([\d,]+(?:\.\d+)?)',
    ]
    
    budget = "未公示"
    for pattern in budget_patterns:
        match = re.search(pattern, title)
        if match:
            budget = match.group(1).replace(',', '') + "万元"
            break
    
    # 尝试提取采购人
    buyer_patterns = [
        r'([\u4e00-\u9fa5]{2,}(?:局|院|中心|公司|集团|单位|学校|医院))',
    ]
    
    buyer = "未公示"
    for pattern in buyer_patterns:
        match = re.search(pattern, title)
        if match:
            buyer = match.group(1)
            break
    
    # 资质要求关键词
    cert_keywords = ['CMA', 'CNAS', '甲级', '乙级', '丙级', '一级', '二级', '注册', '工程师', '资质']
    cert_requirements = []
    for kw in cert_keywords:
        if kw in title:
            cert_requirements.append(kw)
    
    # 截止日期（通常需要从详情页获取，这里先标记）
    deadline = "详见公告"
    
    return {
        'project_name': title,
        'budget': budget,
        'buyer': buyer,
        'cert_requirements': '、'.join(cert_requirements) if cert_requirements else '详见公告',
        'deadline': deadline,
        'publish_date': item.get('date', ''),
        'source': item.get('source', ''),
        'link': item.get('link', '')
    }

def generate_pdf_report(projects, output_path):
    """
    生成PDF报告
    """
    # 添加PDF skill路径
    pdf_skill_dir = os.path.expanduser("~/Library/Application Support/QClaw/openclaw/config/skills/pdf")
    sys.path.insert(0, os.path.join(pdf_skill_dir, "scripts"))
    
    from setup_chinese_pdf import setup_chinese_pdf
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    
    cn_font, styles = setup_chinese_pdf()
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    story = []
    today_str = datetime.now().strftime("%Y年%m月%d日")
    
    # 封面
    story.append(Spacer(1, 100))
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Title'],
        fontSize=28,
        alignment=TA_CENTER,
        spaceAfter=30
    )
    story.append(Paragraph("海南勘察招标日报", title_style))
    story.append(Spacer(1, 20))
    
    date_style = ParagraphStyle(
        'CoverDate',
        parent=styles['Normal'],
        fontSize=16,
        alignment=TA_CENTER
    )
    story.append(Paragraph(today_str, date_style))
    story.append(Spacer(1, 50))
    
    # 统计信息
    stats_style = ParagraphStyle(
        'Stats',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER
    )
    story.append(Paragraph(f"本日共收录 {len(projects)} 条勘察检测类招标公告", stats_style))
    story.append(PageBreak())
    
    # 目录
    story.append(Paragraph("目  录", styles['Heading1']))
    story.append(Spacer(1, 20))
    toc_items = [
        "一、数据概览",
        "二、招标公告明细",
        "三、风险提示与建议"
    ]
    for item in toc_items:
        story.append(Paragraph(item, styles['Normal']))
        story.append(Spacer(1, 10))
    story.append(PageBreak())
    
    # 一、数据概览
    story.append(Paragraph("一、数据概览", styles['Heading1']))
    story.append(Spacer(1, 12))
    
    # 统计表格
    source_stats = {}
    for p in projects:
        source = p.get('source', '其他')
        source_stats[source] = source_stats.get(source, 0) + 1
    
    stats_data = [[Paragraph('数据来源', styles['Normal']), Paragraph('公告数量', styles['Normal'])]]
    for source, count in source_stats.items():
        stats_data.append([Paragraph(source, styles['Normal']), Paragraph(str(count), styles['Normal'])])
    
    stats_table = Table(stats_data, colWidths=[300, 100])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E4057')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, -1), cn_font),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(stats_table)
    story.append(PageBreak())
    
    # 二、招标公告明细
    story.append(Paragraph("二、招标公告明细", styles['Heading1']))
    story.append(Spacer(1, 12))
    
    # 项目表格
    for i, project in enumerate(projects, 1):
        story.append(Paragraph(f"{i}. {project['project_name']}", styles['Heading2']))
        
        detail_data = [
            [Paragraph('预算金额', styles['Normal']), Paragraph(project['budget'], styles['Normal'])],
            [Paragraph('采购人', styles['Normal']), Paragraph(project['buyer'], styles['Normal'])],
            [Paragraph('资质要求', styles['Normal']), Paragraph(project['cert_requirements'], styles['Normal'])],
            [Paragraph('截止时间', styles['Normal']), Paragraph(project['deadline'], styles['Normal'])],
            [Paragraph('发布时间', styles['Normal']), Paragraph(project['publish_date'], styles['Normal'])],
            [Paragraph('信息来源', styles['Normal']), Paragraph(project['source'], styles['Normal'])],
        ]
        
        if project['link']:
            detail_data.append([Paragraph('原文链接', styles['Normal']), Paragraph(project['link'], styles['Normal'])])
        
        detail_table = Table(detail_data, colWidths=[100, 380])
        detail_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8E8E8')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, -1), cn_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(detail_table)
        story.append(Spacer(1, 15))
        
        # 每5个项目分页
        if i % 5 == 0 and i < len(projects):
            story.append(PageBreak())
    
    story.append(PageBreak())
    
    # 三、风险提示与建议
    story.append(Paragraph("三、风险提示与建议", styles['Heading1']))
    story.append(Spacer(1, 12))
    
    tips = [
        "1. 请仔细核对公告中的资质要求，确保企业资质符合投标条件；",
        "2. 注意投标截止时间和开标时间，合理安排投标准备工作；",
        "3. 建议通过原文链接访问官方网站获取最新、最完整的信息；",
        "4. 本报告仅供参考，具体投标事宜请以官方公告为准。"
    ]
    for tip in tips:
        story.append(Paragraph(tip, styles['Normal']))
        story.append(Spacer(1, 8))
    
    # 页脚
    story.append(Spacer(1, 50))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    story.append(Paragraph(f"本报告由系统自动生成 | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}", footer_style))
    
    doc.build(story)
    print(f"\nPDF报告已生成: {output_path}")
    return output_path

def generate_dingtalk_summary(projects):
    """
    生成钉钉卡片摘要
    """
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    summary = f"""📋 【海南勘察招标日报】{today_str}

📊 数据概览
━━━━━━━━━━━━━━━━━━
本日共收录 {len(projects)} 条勘察检测类招标公告

"""
    
    # 按来源统计
    source_stats = {}
    for p in projects:
        source = p.get('source', '其他')
        source_stats[source] = source_stats.get(source, 0) + 1
    
    for source, count in source_stats.items():
        summary += f"• {source}: {count}条\n"
    
    summary += "\n📌 重点项目推荐\n━━━━━━━━━━━━━━━━━━\n"
    
    # 选取前5个项目
    for i, project in enumerate(projects[:5], 1):
        summary += f"""
{i}. {project['project_name'][:40]}{'...' if len(project['project_name']) > 40 else ''}
   💰 预算: {project['budget']}
   🏢 采购人: {project['buyer']}
   📅 发布时间: {project['publish_date']}
"""
    
    summary += """
⚠️ 风险提示
━━━━━━━━━━━━━━━━━━
• 投标前请仔细核对资质要求
• 注意投标截止时间，合理安排准备
• 建议访问官网获取完整信息

💡 提示：详细报告请查看附件PDF
"""
    
    return summary

def main():
    print("=" * 60)
    print("海南勘察招标日报 - 数据采集")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 启动浏览器
    print("\n正在启动浏览器...")
    client, launcher = setup_browser()
    
    try:
        # 抓取中国招标投标公共服务平台
        ceb_results = scrape_cebpubservice(client)
        
        # 抓取海南省政府采购网
        ccgp_results = scrape_ccgp_hainan(client)
        
        # 合并结果
        all_results = ceb_results + ccgp_results
        print(f"\n总共抓取到 {len(all_results)} 条原始公告")
        
        if not all_results:
            print("\n⚠️ 近期无新发布招标信息")
            return
        
        # 过滤最近24小时的公告
        recent_results = filter_recent_items(all_results, hours=24)
        print(f"最近24小时内发布的公告: {len(recent_results)} 条")
        
        # 智能筛选真实勘察类项目
        relevant_results = [r for r in recent_results if is_relevant_project(r.get('title', ''))]
        print(f"符合勘察检测类标准的项目: {len(relevant_results)} 条")
        
        if not relevant_results:
            print("\n⚠️ 近期无新发布勘察检测类招标信息")
            return
        
        # 提取项目信息
        projects = [extract_project_info(r) for r in relevant_results]
        
        # 生成PDF报告
        output_dir = os.path.expanduser("~/.qclaw/workspace")
        os.makedirs(output_dir, exist_ok=True)
        pdf_path = os.path.join(output_dir, f"海南勘察招标日报_{datetime.now().strftime('%Y%m%d')}.pdf")
        generate_pdf_report(projects, pdf_path)
        
        # 生成钉钉摘要
        dingtalk_summary = generate_dingtalk_summary(projects)
        
        # 输出结果
        print("\n" + "=" * 60)
        print("任务执行完成")
        print("=" * 60)
        
        # 读取PDF并输出base64
        with open(pdf_path, 'rb') as f:
            pdf_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        # 保存结果到JSON文件
        result = {
            'pdf_base64': pdf_base64,
            'dingtalk_summary': dingtalk_summary,
            'project_count': len(projects),
            'pdf_path': pdf_path
        }
        
        result_path = os.path.join(output_dir, 'tender_result.json')
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n结果已保存到: {result_path}")
        print(f"\n钉钉摘要:\n{dingtalk_summary}")
        
    except Exception as e:
        print(f"\n执行过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 不要关闭浏览器连接，保持复用
        pass

if __name__ == '__main__':
    main()
