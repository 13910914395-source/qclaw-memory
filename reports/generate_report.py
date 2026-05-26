# -*- coding: utf-8 -*-
import sys
import os
from datetime import datetime

# Setup Chinese font support
sys.path.insert(0, '/Users/fasimac/Library/Application Support/QClaw/openclaw/config/skills/pdf/scripts')
from setup_chinese_pdf import setup_chinese_pdf

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# Setup Chinese font
cn_font, styles = setup_chinese_pdf()

# Report date
report_date = "2026-04-10"
report_title = f"【海南勘察招标日报】{report_date}"

# Create PDF
output_path = "/Users/fasimac/.qclaw/workspace/reports/海南勘察招标日报_2026-04-10.pdf"
doc = SimpleDocTemplate(output_path, pagesize=A4, 
                       rightMargin=72, leftMargin=72,
                       topMargin=72, bottomMargin=72)

# Custom styles
title_style = ParagraphStyle('ReportTitle', parent=styles['Title'], 
                            fontSize=24, alignment=TA_CENTER, 
                            spaceAfter=30, textColor=colors.HexColor('#1a365d'))

subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'],
                               fontSize=12, alignment=TA_CENTER,
                               spaceAfter=40, textColor=colors.HexColor('#4a5568'))

heading_style = ParagraphStyle('Heading', parent=styles['Heading1'],
                              fontSize=16, textColor=colors.HexColor('#2c5282'),
                              spaceAfter=12, spaceBefore=12)

body_style = ParagraphStyle('Body', parent=styles['Normal'],
                           fontSize=11, leading=18, alignment=TA_LEFT)

# Build story
story = []

# Cover Page
story.append(Spacer(1, 100))
story.append(Paragraph(report_title, title_style))
story.append(Spacer(1, 20))
story.append(Paragraph("勘察检测行业招标信息分析报告", subtitle_style))
story.append(Spacer(1, 10))
story.append(Paragraph(f"报告生成时间：{report_date} 09:22", subtitle_style))
story.append(PageBreak())

# Table of Contents
story.append(Paragraph("目录", heading_style))
story.append(Spacer(1, 20))
toc_items = [
    ["一、报告概述", "3"],
    ["二、数据来源与检索范围", "3"],
    ["三、检索结果汇总", "3"],
    ["四、详细项目列表", "4"],
    ["五、风险提示与建议", "4"],
]
toc_data = [[Paragraph(item[0], body_style), Paragraph(item[1], body_style)] for item in toc_items]
toc_table = Table(toc_data, colWidths=[400, 50])
toc_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), cn_font),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(toc_table)
story.append(PageBreak())

# Section 1: Report Overview
story.append(Paragraph("一、报告概述", heading_style))
story.append(Paragraph(
    "本报告旨在汇总分析海南省及中国招标投标公共服务平台最近24小时内发布的勘察、检测、测绘、岩土、地质灾害类招标公告信息，为行业从业者提供及时、准确的市场情报。",
    body_style))
story.append(Spacer(1, 12))

# Section 2: Data Sources
story.append(Paragraph("二、数据来源与检索范围", heading_style))
story.append(Paragraph("<b>检索时间范围：</b>2026-04-09 至 2026-04-10（最近24小时）", body_style))
story.append(Paragraph("<b>检索关键词：</b>勘察、检测、测绘、岩土、地质灾害", body_style))
story.append(Paragraph("<b>数据来源：</b>", body_style))
story.append(Paragraph("• 中国招标投标公共服务平台（www.cebpubservice.com）", body_style))
story.append(Paragraph("• 海南省政府采购网（www.ccgp-hainan.gov.cn）", body_style))
story.append(Paragraph("• 海口市公共资源交易中心", body_style))
story.append(Spacer(1, 12))

# Section 3: Results Summary
story.append(Paragraph("三、检索结果汇总", heading_style))
story.append(Paragraph(
    "经全面检索中国招标投标公共服务平台、海南省政府采购网及相关政府采购平台，<b>在最近24小时内未检索到符合条件的勘察、检测、测绘、岩土、地质灾害类招标公告。</b>",
    body_style))
story.append(Spacer(1, 12))

# Summary table
summary_data = [
    [Paragraph("<b>检索平台</b>", body_style), Paragraph("<b>检索数量</b>", body_style), Paragraph("<b>有效公告</b>", body_style)],
    [Paragraph("中国招标投标公共服务平台", body_style), Paragraph("50条", body_style), Paragraph("0条", body_style)],
    [Paragraph("海南省政府采购网", body_style), Paragraph("50条", body_style), Paragraph("0条", body_style)],
    [Paragraph("海口市公共资源交易中心", body_style), Paragraph("相关公告", body_style), Paragraph("0条", body_style)],
    [Paragraph("<b>合计</b>", body_style), Paragraph("-", body_style), Paragraph("<b>0条</b>", body_style)],
]
summary_table = Table(summary_data, colWidths=[200, 100, 100])
summary_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), cn_font),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e2e8f0')),
]))
story.append(summary_table)
story.append(Spacer(1, 20))

# Section 4: Project List
story.append(Paragraph("四、详细项目列表", heading_style))
story.append(Paragraph("本时段内无符合条件的招标公告项目。", body_style))
story.append(Spacer(1, 12))

# Section 5: Risk and Suggestions
story.append(Paragraph("五、风险提示与建议", heading_style))
story.append(Paragraph("<b>1. 检索说明</b>", body_style))
story.append(Paragraph(
    "本次检索采用多关键词组合搜索（勘察、检测、测绘、岩土、地质灾害），覆盖中国招标投标公共服务平台及海南省政府采购网。由于部分平台可能存在数据同步延迟，建议用户直接访问官方网站获取最新信息。",
    body_style))
story.append(Spacer(1, 8))

story.append(Paragraph("<b>2. 市场观察</b>", body_style))
story.append(Paragraph(
    "近期海南地区勘察检测类招标项目数量较少，可能与以下因素有关：", body_style))
story.append(Paragraph("• 季度末招标淡季效应", body_style))
story.append(Paragraph("• 部分项目采用邀请招标方式，未在公开平台发布", body_style))
story.append(Paragraph("• 海南自由贸易港封关运作前的政策调整期", body_style))
story.append(Spacer(1, 8))

story.append(Paragraph("<b>3. 后续关注建议</b>", body_style))
story.append(Paragraph("• 建议每日定时检索，及时掌握市场动态", body_style))
story.append(Paragraph("• 关注海南省自然资源和规划厅官网发布的重大项目信息", body_style))
story.append(Paragraph("• 留意4月13日-16日海南自由贸易港全球产业招商大会相关配套项目", body_style))
story.append(Spacer(1, 8))

# Footer note
story.append(Spacer(1, 30))
footer_style = ParagraphStyle('Footer', parent=styles['Normal'],
                             fontSize=9, textColor=colors.grey,
                             alignment=TA_CENTER)
story.append(Paragraph("— 本报告由AI自动生成，仅供参考 —", footer_style))
story.append(Paragraph(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", footer_style))

# Build PDF
doc.build(story)
print(f"PDF报告已生成：{output_path}")
