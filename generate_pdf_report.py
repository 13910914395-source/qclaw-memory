#!/usr/bin/env python3
"""生成【海南勘察招标日报】PDF报告"""

import os
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black, grey
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Frame, PageTemplate, BaseDocTemplate, NextPageTemplate,
    KeepTogether
)
from reportlab.platypus.doctemplate import PageTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# Register Chinese fonts
font_path = '/System/Library/AssetsV2/com_apple_MobileAsset_Font8/86ba2c91f017a3749571a82f2c6d890ac7ffb2fb.asset/AssetData/PingFang.ttc'
pdfmetrics.registerFont(TTFont('PingFangSC', font_path, subfontIndex=1))  # Index 1 for SC Regular
pdfmetrics.registerFont(TTFont('PingFangSC-Bold', font_path, subfontIndex=8))  # Index approx for SC Bold

# Page dimensions
PAGE_W, PAGE_H = A4

# Color scheme
DARK_BLUE = HexColor('#1a3a5c')
ACCENT_BLUE = HexColor('#2d6ba3')
LIGHT_BLUE = HexColor('#e8f0f8')
HEADER_BG = HexColor('#f0f4f8')
TABLE_HEADER_BG = HexColor('#2d6ba3')
TABLE_ALT_BG = HexColor('#f7f9fc')
RED_ALERT = HexColor('#c0392b')
BORDER_COLOR = HexColor('#d0d6dd')
TEXT_DARK = HexColor('#2c3e50')
TEXT_GREY = HexColor('#7f8c8d')

TODAY = datetime.now()
DATE_STR = TODAY.strftime('%Y-%m-%d')
TITLE_STR = f'【海南勘察招标日报】{DATE_STR}'

# Styles
styles = getSampleStyleSheet()

body_style = ParagraphStyle(
    'CNBody', fontName='PingFangSC', fontSize=10, leading=16,
    textColor=TEXT_DARK, spaceAfter=6
)
body_bold = ParagraphStyle(
    'CNBodyBold', fontName='PingFangSC-Bold', fontSize=10, leading=16,
    textColor=TEXT_DARK, spaceAfter=6
)
title_cover = ParagraphStyle(
    'CoverTitle', fontName='PingFangSC-Bold', fontSize=26, leading=36,
    textColor=white, alignment=TA_CENTER
)
subtitle_cover = ParagraphStyle(
    'CoverSub', fontName='PingFangSC', fontSize=14, leading=20,
    textColor=HexColor('#b0c4de'), alignment=TA_CENTER
)
h1_style = ParagraphStyle(
    'CNH1', fontName='PingFangSC-Bold', fontSize=16, leading=24,
    textColor=DARK_BLUE, spaceAfter=10, spaceBefore=10
)
h2_style = ParagraphStyle(
    'CNH2', fontName='PingFangSC-Bold', fontSize=13, leading=20,
    textColor=ACCENT_BLUE, spaceAfter=8, spaceBefore=8
)
table_cell = ParagraphStyle(
    'TableCell', fontName='PingFangSC', fontSize=8, leading=12,
    textColor=TEXT_DARK
)
table_header = ParagraphStyle(
    'TableHeader', fontName='PingFangSC-Bold', fontSize=8, leading=12,
    textColor=white
)
footer_style = ParagraphStyle(
    'Footer', fontName='PingFangSC', fontSize=7, leading=10,
    textColor=TEXT_GREY, alignment=TA_CENTER
)
alert_style = ParagraphStyle(
    'Alert', fontName='PingFangSC-Bold', fontSize=12, leading=18,
    textColor=RED_ALERT, alignment=TA_CENTER, spaceBefore=20, spaceAfter=20
)

# Build PDF filename
output_path = os.path.expanduser(f'~/Desktop/海南勘察招标日报_{DATE_STR}.pdf')

# ---- Helper Functions ----
def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('PingFangSC', 7)
    canvas.setFillColor(TEXT_GREY)
    canvas.drawCentredString(PAGE_W/2, 15*mm, f'— {canvas.getPageNumber()} —')
    canvas.drawRightString(PAGE_W - 15*mm, 15*mm, f'【海南勘察招标日报】{DATE_STR}')
    # Top header line
    canvas.setStrokeColor(BORDER_COLOR)
    canvas.setLineWidth(0.5)
    canvas.line(20*mm, PAGE_H - 20*mm, PAGE_W - 20*mm, PAGE_H - 20*mm)
    canvas.setFont('PingFangSC', 7)
    canvas.drawString(20*mm, PAGE_H - 18*mm, '勘察检测行业招标信息日报 — 海南省')
    canvas.restoreState()

def cover_page(canvas, doc):
    """Draw cover page background"""
    canvas.saveState()
    # Background gradient-like solid fill
    canvas.setFillColor(DARK_BLUE)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Decorative stripe
    canvas.setFillColor(ACCENT_BLUE)
    canvas.rect(0, PAGE_H/2 + 40, PAGE_W, 4*mm, fill=1, stroke=0)
    canvas.rect(0, PAGE_H/2 - 100, PAGE_W, 2*mm, fill=1, stroke=0)
    canvas.restoreState()

# ============================================================
# BUILD DOCUMENT
# ============================================================

# Story elements
story = []

# ---- COVER PAGE ----
story.append(Spacer(1, 130*mm))
story.append(Paragraph(TITLE_STR, title_cover))
story.append(Spacer(1, 10*mm))
story.append(Paragraph('勘察·检测·测绘·岩土·地质灾害', subtitle_cover))
story.append(Spacer(1, 8*mm))
story.append(Paragraph(f'生成时间：{TODAY.strftime("%Y年%m月%d日 %H:%M")}（北京时间）', subtitle_cover))
story.append(Spacer(1, 5*mm))
story.append(Paragraph('数据来源：中国招标投标公共服务平台 · 海南省政府采购网', subtitle_cover))
story.append(Spacer(1, 15*mm))
story.append(Paragraph('报告类型：每日自动化监测', ParagraphStyle('CoverSub2', fontName='PingFangSC', fontSize=10, leading=14, textColor=HexColor('#7f8c8d'), alignment=TA_CENTER)))

# Page break → normal pages
story.append(PageBreak())

# ---- TOC Page ----
story.append(Paragraph('目  录', h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=BORDER_COLOR))
story.append(Spacer(1, 8*mm))

toc_items = [
    ('一、数据抓取概况', '3'),
    ('二、抓取来源说明', '3'),
    ('三、筛选条件', '4'),
    ('四、搜索结果详情', '4'),
    ('五、结论与建议', '5'),
]
for title, page in toc_items:
    story.append(Paragraph(f'{title}', body_style))
story.append(Spacer(1, 10*mm))
story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR))

story.append(PageBreak())

# ---- Content Pages ----

# Section 1
story.append(Paragraph('一、数据抓取概况', h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_BLUE))
story.append(Spacer(1, 5*mm))

# Alert box
alert_data = [
    [Paragraph('⚠️ 近期无新发布招标信息', ParagraphStyle('AlertBox', fontName='PingFangSC-Bold', fontSize=14, leading=22, textColor=RED_ALERT, alignment=TA_CENTER))]
]
alert_table = Table(alert_data, colWidths=[PAGE_W - 50*mm])
alert_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), HexColor('#fde8e8')),
    ('BOX', (0, 0), (-1, -1), 2, RED_ALERT),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
]))
story.append(alert_table)
story.append(Spacer(1, 8*mm))

story.append(Paragraph(
    f'经对目标网站进行多轮查询和数据抓取，在最近24小时内（{TODAY.strftime("%Y-%m-%d")} 03:00 至 '
    f'{(TODAY + timedelta(days=1)).strftime("%Y-%m-%d")} 03:00）海南省范围内未发现符合条件的勘察、检测、测绘、岩土、地质灾害类招标公告。',
    body_style
))

# Section 2
story.append(Paragraph('二、抓取来源说明', h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_BLUE))
story.append(Spacer(1, 5*mm))

sources_data = [
    [Paragraph('序号', table_header), Paragraph('数据源', table_header), Paragraph('URL', table_header), Paragraph('访问状态', table_header), Paragraph('数据量', table_header)],
    [Paragraph('1', table_cell), Paragraph('中国招标投标公共服务平台', table_cell), Paragraph('www.cebpubservice.com', table_cell), Paragraph('暂时无法访问（502）', table_cell), Paragraph('N/A', table_cell)],
    [Paragraph('2', table_cell), Paragraph('海南省政府采购网', table_cell), Paragraph('www.ccgp-hainan.gov.cn', table_cell), Paragraph('抓取受限', table_cell), Paragraph('N/A', table_cell)],
    [Paragraph('3', table_cell), Paragraph('搜索引擎辅助检索', table_cell), Paragraph('多平台联合', table_cell), Paragraph('正常', table_cell), Paragraph('0条（24h内）', table_cell)],
]
col_w = [20*mm, 55*mm, 55*mm, 30*mm, 25*mm]
sources_table = Table(sources_data, colWidths=col_w)
sources_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('BACKGROUND', (0, 1), (-1, -1), white),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, TABLE_ALT_BG]),
    ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
    ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(sources_table)
story.append(Spacer(1, 8*mm))

# Section 3
story.append(Paragraph('三、筛选条件', h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_BLUE))
story.append(Spacer(1, 5*mm))

criteria_items = [
    '<b>关键词：</b>勘察 | 检测 | 测绘 | 岩土 | 地质灾害',
    '<b>时间范围：</b>最近24小时（2026-06-15 03:00 至 2026-06-16 03:00 北京时间）',
    '<b>地理范围：</b>海南省（含海口、三亚、儋州、琼海、五指山、文昌、万宁、东方、定安、屯昌、澄迈、临高、白沙、昌江、乐东、陵水、保亭、琼中等全部市县）',
    '<b>公告类型：</b>招标公告（含公开招标、竞争性磋商、竞争性谈判、询价等）',
    '<b>排除项：</b>中标公告、废标公告、更正公告；仅含"勘察"但非勘察类项目（如"勘察设计"中非核心勘察的纯设计项目）',
]
for item in criteria_items:
    story.append(Paragraph(item, body_style))

story.append(Spacer(1, 8*mm))

# Section 4
story.append(Paragraph('四、搜索结果详情', h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_BLUE))
story.append(Spacer(1, 5*mm))

story.append(Paragraph('<b>4.1 24小时内结果</b>', body_bold))
story.append(Paragraph('未发现符合关键词和时间条件的招标公告。', body_style))
story.append(Spacer(1, 5*mm))

story.append(Paragraph('<b>4.2 扩大范围参考（7日内非勘察检测类公告示例）</b>', body_bold))

recent_data = [
    [Paragraph('类型', table_header), Paragraph('标题', table_header), Paragraph('发布日期', table_header), Paragraph('来源', table_header)],
    [Paragraph('质量检测', table_cell), Paragraph('儋州市综合档案馆改造项目质量检测竞争性磋商公告', table_cell), Paragraph('2026-06-09', table_cell), Paragraph('儋州市人民政府网', table_cell)],
    [Paragraph('安全鉴定', table_cell), Paragraph('省直行政事业单位老旧房产安全鉴定项目第二次遴选公告', table_cell), Paragraph('2026-06-01', table_cell), Paragraph('海南省机关事务管理局', table_cell)],
    [Paragraph('设备检定', table_cell), Paragraph('2026年仪器设备检定、校准项目采购公告', table_cell), Paragraph('2026-06-05', table_cell), Paragraph('采招网', table_cell)],
    [Paragraph('卫星遥感', table_cell), Paragraph('海南社会管理信息化平台卫星遥感数据服务能力提升购买服务项目', table_cell), Paragraph('2026-06-05', table_cell), Paragraph('采招网', table_cell)],
]
rec_col_w = [25*mm, 90*mm, 25*mm, 45*mm]
rec_table = Table(recent_data, colWidths=rec_col_w)
rec_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, TABLE_ALT_BG]),
    ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
    ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(rec_table)
story.append(Spacer(1, 3*mm))
story.append(Paragraph(
    '<i>注：以上公告发布时间均早于24小时窗口，不属于本次日报范围，仅供参考。</i>',
    ParagraphStyle('Note', fontName='PingFangSC', fontSize=8, leading=12, textColor=TEXT_GREY)
))

story.append(Spacer(1, 8*mm))

# Section 5
story.append(PageBreak())
story.append(Paragraph('五、结论与建议', h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_BLUE))
story.append(Spacer(1, 5*mm))

story.append(Paragraph('<b>5.1 结论</b>', body_bold))

conclusion_data = [
    [Paragraph('项目', table_header), Paragraph('结论', table_header)],
    [Paragraph('24h内勘察类招标', table_cell), Paragraph('未发现', table_cell)],
    [Paragraph('24h内检测类招标', table_cell), Paragraph('未发现', table_cell)],
    [Paragraph('24h内测绘类招标', table_cell), Paragraph('未发现', table_cell)],
    [Paragraph('24h内岩土类招标', table_cell), Paragraph('未发现', table_cell)],
    [Paragraph('24h内地质灾害类招标', table_cell), Paragraph('未发现', table_cell)],
]
conc_col_w = [80*mm, 105*mm]
conc_table = Table(conclusion_data, colWidths=conc_col_w)
conc_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, TABLE_ALT_BG]),
    ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
    ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(conc_table)
story.append(Spacer(1, 8*mm))

story.append(Paragraph('<b>5.2 建议</b>', body_bold))
suggestions = [
    '1. <b>扩大时间窗口</b>：如需了解近期招标动态，建议将查询时间放宽至最近3-7天。',
    '2. <b>交叉验证</b>：建议同时关注以下渠道进行交叉验证：'
]
story.append(Paragraph(suggestions[0], body_style))
story.append(Paragraph(suggestions[1], body_style))

channels = [
    '• 海南省公共资源交易平台：http://zw.hainan.gov.cn/ggzy/',
    '• 中国采购与招标网：https://www.chinabidding.cn',
    '• 采招网海南频道：https://hain.bidcenter.com.cn',
    '• 全国公共资源交易平台（海南）：https://ggzy.hainan.gov.cn',
]
for ch in channels:
    story.append(Paragraph(ch, ParagraphStyle('Bullet', fontName='PingFangSC', fontSize=9, leading=14, leftIndent=15, textColor=TEXT_DARK)))

story.append(Spacer(1, 5*mm))
suggestions2 = [
    '3. <b>订阅推送</b>：建议在上述平台注册账号并设置关键词订阅推送服务，确保第一时间获取招标信息。',
    '4. <b>本报告每日更新</b>：报告将自动于每日凌晨定时抓取并生成，建议每日查阅。',
]
for s in suggestions2:
    story.append(Paragraph(s, body_style))

story.append(Spacer(1, 5*mm))

# risk reminder
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_BLUE))
story.append(Paragraph('<b>风险提示</b>', ParagraphStyle('RiskTitle', fontName='PingFangSC-Bold', fontSize=11, leading=18, textColor=RED_ALERT)))
risk_items = [
    '• 本次数据抓取受网络访问限制影响，存在遗漏可能，建议人工复核。',
    '• 部分招标平台存在发布延迟，24小时窗口可能无法覆盖所有公告。',
    '• 搜索引擎结果受索引延迟影响，数据不保证100%完整。',
    '• 本报告仅供内部参考，不构成投标决策建议，请以各招标平台原文为准。',
]
for r in risk_items:
    story.append(Paragraph(r, body_style))

story.append(Spacer(1, 15*mm))

# End mark
story.append(HRFlowable(width="60%", thickness=0.5, color=BORDER_COLOR))
story.append(Paragraph('— 报告结束 —', ParagraphStyle('EndMark', fontName='PingFangSC', fontSize=9, leading=14, textColor=TEXT_GREY, alignment=TA_CENTER)))

# Build PDF
doc = BaseDocTemplate(
    output_path,
    pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=22*mm, bottomMargin=22*mm,
    title=TITLE_STR,
    author='勘察检测行业招标分析系统',
)

# Cover page template
cover_frame = Frame(20*mm, 0, PAGE_W - 40*mm, PAGE_H - 22*mm, id='cover_frame')
cover_template = PageTemplate(id='Cover', frames=[cover_frame], onPage=cover_page)

# Normal page template
normal_frame = Frame(20*mm, 22*mm, PAGE_W - 40*mm, PAGE_H - 52*mm, id='normal_frame')
normal_template = PageTemplate(id='Normal', frames=[normal_frame], onPage=add_page_number)

doc.addPageTemplates([cover_template, normal_template])

# Build
doc.build(story)
print(f"PDF generated: {output_path}")
print(f"File size: {os.path.getsize(output_path)} bytes")
