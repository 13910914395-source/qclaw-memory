#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海南勘察招标日报 - PDF报告生成
"""

import sys
import os
import json
from datetime import datetime

# 添加PDF skill脚本路径
sys.path.insert(0, os.path.expanduser('~/Library/Application Support/QClaw/openclaw/config/skills/pdf/scripts'))

from setup_chinese_pdf import setup_chinese_pdf

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import cm

def create_report():
    # 读取数据
    with open('/Users/fasimac/.qclaw/workspace/hainan_tender_report_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tenders = data['tenders']
    stats = data['stats']
    report_date = data['report_date']
    
    # 设置中文字体
    cn_font, styles = setup_chinese_pdf()
    
    # 创建PDF文档
    output_path = '/Users/fasimac/.qclaw/workspace/海南勘察招标日报_{}.pdf'.format(report_date)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # 自定义样式
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    heading1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10
    )
    
    heading2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY
    )
    
    # 构建文档内容
    story = []
    
    # 封面
    story.append(Spacer(1, 100))
    story.append(Paragraph("海南勘察招标日报", title_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"报告日期：{report_date}", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("关键词：勘察、检测、测绘、岩土、地质灾害", subtitle_style))
    story.append(PageBreak())
    
    # 目录
    story.append(Paragraph("目录", heading1_style))
    story.append(Spacer(1, 10))
    toc_items = [
        "一、数据概览",
        "二、招标信息汇总表",
        "三、详细招标信息",
        "四、风险提示与建议"
    ]
    for item in toc_items:
        story.append(Paragraph(item, body_style))
        story.append(Spacer(1, 5))
    story.append(PageBreak())
    
    # 一、数据概览
    story.append(Paragraph("一、数据概览", heading1_style))
    story.append(Spacer(1, 10))
    
    # 统计表格
    stats_data = [
        [Paragraph('类别', styles['Normal']), Paragraph('数量', styles['Normal'])],
        [Paragraph('勘察类', styles['Normal']), Paragraph(str(stats['勘察类']), styles['Normal'])],
        [Paragraph('检测类', styles['Normal']), Paragraph(str(stats['检测类']), styles['Normal'])],
        [Paragraph('测绘类', styles['Normal']), Paragraph(str(stats['测绘类']), styles['Normal'])],
        [Paragraph('岩土类', styles['Normal']), Paragraph(str(stats['岩土类']), styles['Normal'])],
        [Paragraph('地质灾害类', styles['Normal']), Paragraph(str(stats['地质灾害类']), styles['Normal'])],
        [Paragraph('总计', styles['Normal']), Paragraph(str(stats['总计']), styles['Normal'])]
    ]
    
    stats_table = Table(stats_data, colWidths=[200, 100])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E4057')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, -1), cn_font),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8E8E8')),
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("数据来源：", heading2_style))
    story.append(Paragraph("• 中国招标投标公共服务平台", body_style))
    story.append(Paragraph("• 海南省政府采购网", body_style))
    story.append(Paragraph("• 中国政府采购网", body_style))
    story.append(Paragraph("• 中国电力招标采购网", body_style))
    story.append(Paragraph("• 建设招标网", body_style))
    story.append(PageBreak())
    
    # 二、招标信息汇总表
    story.append(Paragraph("二、招标信息汇总表", heading1_style))
    story.append(Spacer(1, 10))
    
    # 汇总表格
    summary_data = [[
        Paragraph('序号', styles['Normal']),
        Paragraph('项目名称', styles['Normal']),
        Paragraph('类型', styles['Normal']),
        Paragraph('预算金额', styles['Normal']),
        Paragraph('发布日期', styles['Normal'])
    ]]
    
    for i, t in enumerate(tenders, 1):
        summary_data.append([
            Paragraph(str(i), styles['Normal']),
            Paragraph(t['项目名称'][:30] + '...' if len(t['项目名称']) > 30 else t['项目名称'], styles['Normal']),
            Paragraph(t['类型'], styles['Normal']),
            Paragraph(t['预算金额'][:15] + '...' if len(t['预算金额']) > 15 else t['预算金额'], styles['Normal']),
            Paragraph(t['发布时间'], styles['Normal'])
        ])
    
    summary_table = Table(summary_data, colWidths=[30, 180, 50, 100, 60], repeatRows=1)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E4057')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, -1), cn_font),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(summary_table)
    story.append(PageBreak())
    
    # 三、详细招标信息
    story.append(Paragraph("三、详细招标信息", heading1_style))
    story.append(Spacer(1, 10))
    
    # 按类型分组
    types = ['勘察', '检测', '测绘', '岩土', '地质灾害']
    for t_type in types:
        type_tenders = [t for t in tenders if t['类型'] == t_type]
        if type_tenders:
            story.append(Paragraph(f"{t_type}类项目", heading2_style))
            story.append(Spacer(1, 5))
            
            for t in type_tenders:
                story.append(Paragraph(f"项目名称：{t['项目名称']}", body_style))
                story.append(Paragraph(f"预算金额：{t['预算金额']}", body_style))
                story.append(Paragraph(f"采购人：{t['采购人']}", body_style))
                story.append(Paragraph(f"关键资质要求：{t['关键资质要求']}", body_style))
                story.append(Paragraph(f"截止日期：{t['截止日期']}", body_style))
                story.append(Paragraph(f"发布时间：{t['发布时间']}", body_style))
                story.append(Paragraph(f"原文链接：{t['原文链接']}", body_style))
                story.append(Paragraph(f"来源：{t['来源']}", body_style))
                story.append(Spacer(1, 10))
            
            story.append(Spacer(1, 10))
    
    story.append(PageBreak())
    
    # 四、风险提示与建议
    story.append(Paragraph("四、风险提示与建议", heading1_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("1. 资质要求提示", heading2_style))
    story.append(Paragraph("• 勘察类项目多要求工程勘察综合资质或专业资质，部分项目要求注册土木工程师（岩土）执业资格。", body_style))
    story.append(Paragraph("• 检测类项目普遍要求CMA资质认定证书。", body_style))
    story.append(Paragraph("• 测绘类项目要求测绘资质，部分项目要求乙级或以上资质。", body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("2. 投标时间提醒", heading2_style))
    story.append(Paragraph("• 请密切关注各项目的投标截止日期，避免错过投标时机。", body_style))
    story.append(Paragraph("• 部分项目已过期或已成交，仅供参考。", body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("3. 信息核实建议", heading2_style))
    story.append(Paragraph("• 建议投标前仔细阅读招标文件，核实项目具体要求。", body_style))
    story.append(Paragraph("• 可通过原文链接访问发布网站获取最新信息。", body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("4. 风险提示", heading2_style))
    story.append(Paragraph("• 本报告信息来源于公开渠道，仅供参考，不构成投标建议。", body_style))
    story.append(Paragraph("• 投标决策请基于完整的招标文件和专业判断。", body_style))
    
    # 页脚
    story.append(Spacer(1, 50))
    story.append(Paragraph("— 报告结束 —", ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10)))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER, fontSize=8)))
    
    # 生成PDF
    doc.build(story)
    print(f"PDF报告已生成：{output_path}")
    return output_path

if __name__ == '__main__':
    create_report()
