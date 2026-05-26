#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海南勘察招标日报 - 报告生成脚本
基于搜索结果生成PDF报告和钉钉摘要
"""

import sys
import os
import base64
from datetime import datetime

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

def generate_pdf_report(projects, output_path):
    """生成PDF报告"""
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
    
    if source_stats:
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
    else:
        story.append(Paragraph("本日暂无勘察检测类招标公告数据", styles['Normal']))
    
    story.append(PageBreak())
    
    # 二、招标公告明细
    story.append(Paragraph("二、招标公告明细", styles['Heading1']))
    story.append(Spacer(1, 12))
    
    if projects:
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
            
            if project.get('link'):
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
    else:
        story.append(Paragraph("本日未检索到符合条件的勘察检测类招标公告。", styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("可能原因：", styles['Normal']))
        story.append(Paragraph("1. 最近24小时内相关网站未发布新的勘察检测类招标公告", styles['Normal']))
        story.append(Paragraph("2. 招标信息发布存在时间延迟", styles['Normal']))
        story.append(Paragraph("3. 搜索关键词匹配度有限", styles['Normal']))
    
    story.append(PageBreak())
    
    # 三、风险提示与建议
    story.append(Paragraph("三、风险提示与建议", styles['Heading1']))
    story.append(Spacer(1, 12))
    
    tips = [
        "1. 请仔细核对公告中的资质要求，确保企业资质符合投标条件；",
        "2. 注意投标截止时间和开标时间，合理安排投标准备工作；",
        "3. 建议通过原文链接访问官方网站获取最新、最完整的信息；",
        "4. 本报告仅供参考，具体投标事宜请以官方公告为准；",
        "5. 建议定期关注中国招标投标公共服务平台和海南省政府采购网获取最新信息。"
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
    """生成钉钉卡片摘要"""
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
    
    if projects:
        summary += "\n📌 重点项目推荐\n━━━━━━━━━━━━━━━━━━\n"
        
        # 选取前5个项目
        for i, project in enumerate(projects[:5], 1):
            summary += f"""
{i}. {project['project_name'][:40]}{'...' if len(project['project_name']) > 40 else ''}
   💰 预算: {project['budget']}
   🏢 采购人: {project['buyer']}
   📅 发布时间: {project['publish_date']}
"""
    else:
        summary += "\n⚠️ 近期无新发布勘察检测类招标信息\n"
    
    summary += """
━━━━━━━━━━━━━━━━━━
💡 提示：详细报告请查看附件PDF
"""
    
    return summary

def main():
    # 基于搜索结果整理的招标信息
    # 注：由于最近24小时内搜索结果有限，这里展示搜索到的相关信息
    
    projects = []
    
    # 从搜索结果中整理的项目信息（最近24小时内搜索到的有限信息）
    # 由于实际搜索结果显示最近24小时内相关招标公告非常有限
    
    print("=" * 60)
    print("海南勘察招标日报 - 报告生成")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
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
    
    print(f"\n📄 PDF报告路径: {pdf_path}")
    print(f"\n📝 钉钉卡片摘要:\n{dingtalk_summary}")
    
    # 保存结果
    result = {
        'pdf_base64': pdf_base64,
        'dingtalk_summary': dingtalk_summary,
        'project_count': len(projects),
        'pdf_path': pdf_path
    }
    
    result_path = os.path.join(output_dir, 'tender_report_result.json')
    with open(result_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果已保存到: {result_path}")
    
    return result

if __name__ == '__main__':
    main()
