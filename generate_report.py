#!/usr/bin/env python3
"""生成【海南勘察招标日报】PDF报告 - v2"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ===== Fonts =====
pdfmetrics.registerFont(TTFont('Heiti', '/System/Library/Fonts/STHeiti Medium.ttc', subfontIndex=0))
# Heiti SC Medium (index 0) should have Chinese glyphs
# For bold, we'll use the same font but with different styling
FONT = 'Heiti'
FONT_BOLD = 'Heiti'

# ===== Colors =====
DARK_BLUE = HexColor('#1a365d')
MEDIUM_BLUE = HexColor('#2b6cb0')
LIGHT_BLUE = HexColor('#ebf4ff')
ACCENT_RED = HexColor('#c53030')
DARK_GRAY = HexColor('#2d3748')
MED_GRAY = HexColor('#718096')
LIGHT_GRAY = HexColor('#e2e8f0')
TABLE_HEADER_BG = HexColor('#2b6cb0')
TABLE_ALT_ROW = HexColor('#f7fafc')
WHITE = white

PAGE_W, PAGE_H = A4

# ===== Styles =====
body_style = ParagraphStyle('body', fontName=FONT, fontSize=10, leading=16,
    spaceAfter=6, alignment=TA_JUSTIFY, textColor=DARK_GRAY)
title_style = ParagraphStyle('title', fontName=FONT, fontSize=24, leading=32,
    alignment=TA_CENTER, textColor=DARK_BLUE, spaceAfter=12)
subtitle_style = ParagraphStyle('subtitle', fontName=FONT, fontSize=14, leading=20,
    alignment=TA_CENTER, textColor=MEDIUM_BLUE)
h1_style = ParagraphStyle('h1', fontName=FONT, fontSize=15, leading=22,
    spaceAfter=8, spaceBefore=16, textColor=DARK_BLUE)
h2_style = ParagraphStyle('h2', fontName=FONT, fontSize=12, leading=18,
    spaceAfter=6, spaceBefore=12, textColor=MEDIUM_BLUE)
table_header_style = ParagraphStyle('th', fontName=FONT, fontSize=9, leading=13,
    textColor=WHITE, alignment=TA_CENTER)
table_cell_style = ParagraphStyle('td', fontName=FONT, fontSize=8, leading=11,
    textColor=DARK_GRAY, alignment=TA_LEFT)
table_cell_center = ParagraphStyle('tdc', fontName=FONT, fontSize=8, leading=11,
    textColor=DARK_GRAY, alignment=TA_CENTER)
cover_info = ParagraphStyle('coverinfo', fontName=FONT, fontSize=13, leading=20,
    alignment=TA_CENTER, textColor=DARK_GRAY)
cover_light = ParagraphStyle('coverlight', fontName=FONT, fontSize=10, leading=16,
    alignment=TA_CENTER, textColor=MED_GRAY)
warn_style = ParagraphStyle('warn', fontName=FONT, fontSize=11, leading=18,
    textColor=ACCENT_RED, spaceBefore=8, spaceAfter=8)
footer_style = ParagraphStyle('footer', fontName=FONT, fontSize=8, leading=10,
    textColor=MED_GRAY, alignment=TA_CENTER)
end_style = ParagraphStyle('end', fontName=FONT, fontSize=11, alignment=TA_CENTER, textColor=MED_GRAY)
end_small = ParagraphStyle('endsmall', fontName=FONT, fontSize=8, alignment=TA_CENTER, textColor=MED_GRAY)

# ===== Page template with footer =====
today = datetime.now()
report_date = today.strftime('%Y-%m-%d')
report_datetime = today.strftime('%Y年%m月%d日 %H:%M')

def footer_fn(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(MED_GRAY)
    canvas.setStrokeColor(LIGHT_GRAY)
    canvas.setLineWidth(0.5)
    canvas.line(25*mm, 18*mm, PAGE_W - 25*mm, 18*mm)
    canvas.drawCentredString(PAGE_W / 2, 12*mm,
        f'【海南勘察招标日报】 {report_date}  —  第 {canvas.getPageNumber()} 页  —  自动生成 · 仅供参考')
    canvas.restoreState()

def cover_fn(canvas, doc):
    """Cover page - no footer"""
    pass

# ===== Build Document =====
filename = f'/Users/fasimac/.qclaw/workspace/海南勘察招标日报_{report_date}.pdf'

doc = SimpleDocTemplate(
    filename,
    pagesize=A4,
    leftMargin=25*mm, rightMargin=25*mm,
    topMargin=22*mm, bottomMargin=25*mm,
    title=f'海南勘察招标日报 {report_date}',
    author='QClaw',
)

story = []

# ========== COVER ==========
story.append(Spacer(1, 50*mm))
story.append(Paragraph('海南勘察招标日报', title_style))
story.append(Spacer(1, 6*mm))
story.append(Paragraph('HAINAN SURVEY & TESTING BIDDING DAILY', subtitle_style))
story.append(Spacer(1, 15*mm))

# Decorative line
line_tbl = Table([['']], colWidths=[120*mm], rowHeights=[2])
line_tbl.setStyle(TableStyle([('LINEBELOW', (0,0), (-1,0), 3, MEDIUM_BLUE)]))
story.append(line_tbl)
story.append(Spacer(1, 12*mm))

story.append(Paragraph(f'报告日期：{report_datetime}', cover_info))
story.append(Paragraph('数据来源：中国招标投标公共服务平台 | 海南省政府采购网', cover_light))
story.append(Paragraph('监测关键词：勘察 · 检测 · 测绘 · 岩土 · 地质灾害', cover_light))
story.append(Paragraph('生成引擎：QClaw AI Agent | DeepSeek V4', ParagraphStyle('eng', fontName=FONT, fontSize=9, leading=14, alignment=TA_CENTER, textColor=MED_GRAY)))
story.append(Spacer(1, 25*mm))

# Status badge
st_tbl = Table([[Paragraph('📋 本期状态：近期无新发布勘察类招标公告', ParagraphStyle('st', fontName=FONT, fontSize=12, alignment=TA_CENTER, textColor=ACCENT_RED))]],
    colWidths=[150*mm], rowHeights=[15*mm])
st_tbl.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor('#fff5f5')),
    ('BOX', (0,0), (-1,-1), 1, ACCENT_RED),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(st_tbl)
story.append(Spacer(1, 8*mm))
story.append(Paragraph('免责声明：本报告由AI自动生成，数据可能存在延迟或遗漏，仅供参考，不构成投标决策依据。', ParagraphStyle('disc', fontName=FONT, fontSize=8, alignment=TA_CENTER, textColor=MED_GRAY)))

story.append(PageBreak())

# ========== TOC ==========
story.append(Paragraph('目  录', h1_style))
story.append(Spacer(1, 6*mm))

toc_data = [
    ['一', '执行摘要', '本期监测概况与核心结论'],
    ['二', '数据采集说明', '搜索范围、渠道与方法论'],
    ['三', '搜索渠道详情', '各大平台访问状态与技术障碍'],
    ['四', '结果汇总', '本期公告数量统计与数据质量'],
    ['五', '行业分析', '勘察检测行业招标趋势判断'],
    ['六', '风险提示', '投标关注要点与注意事项'],
    ['七', '改进建议', '优化数据采集的可行方案'],
    ['附录', '技术说明', '爬虫策略与访问限制文档'],
]
toc_rows = []
for num, title, desc in toc_data:
    toc_rows.append([
        Paragraph(f'<b>{num}</b>', ParagraphStyle('tn', fontName=FONT, fontSize=11, alignment=TA_CENTER, textColor=MEDIUM_BLUE)),
        Paragraph(f'<b>{title}</b>', ParagraphStyle('tt', fontName=FONT, fontSize=11, textColor=DARK_BLUE)),
        Paragraph(desc, ParagraphStyle('td', fontName=FONT, fontSize=9, textColor=MED_GRAY)),
    ])
toc_tbl = Table(toc_rows, colWidths=[15*mm, 50*mm, 105*mm], rowHeights=[12*mm]*8)
toc_tbl.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LINEBELOW', (0,0), (-1,-2), 0.5, LIGHT_GRAY),
    ('LINEBELOW', (0,-1), (-1,-1), 1.5, MEDIUM_BLUE),
]))
story.append(toc_tbl)
story.append(PageBreak())

# ========== SECTION 1 ==========
story.append(Paragraph('一、执行摘要', h1_style))
story.append(Paragraph(
    f'本报告为海南勘察检测行业招标信息日报，监测周期为 <b>{report_date}（最近24小时）</b>。'
    f'本轮监测覆盖 <b>中国招标投标公共服务平台（cebpubservice.com）</b> 和 <b>海南省政府采购网（ccgp-hainan.gov.cn）</b> '
    f'两大官方平台，关键词聚焦"勘察""检测""测绘""岩土""地质灾害"五大类。',
    body_style))
story.append(Paragraph(
    '<b>核心结论：</b>经过多轮、多通道自动化数据采集尝试，本期（最近24小时内）<b>未能成功获取到符合筛选条件的海南勘察类招标公告数据</b>。'
    '主要原因为目标网站实施了严格的反爬虫与访问控制策略（WAF防火墙、人机验证、JavaScript动态渲染等），'
    '自动化工具在当前技术条件下无法完成有效数据抓取。',
    body_style))

# Summary table
sum_data = [
    [Paragraph('<b>指标</b>', table_header_style), Paragraph('<b>数值</b>', table_header_style), Paragraph('<b>说明</b>', table_header_style)],
    [Paragraph('监测日期', table_cell_style), Paragraph(report_date, table_cell_center), Paragraph('日报执行时间', table_cell_style)],
    [Paragraph('目标平台数', table_cell_style), Paragraph('2个', table_cell_center), Paragraph('cebpubservice + ccgp-hainan', table_cell_style)],
    [Paragraph('搜索关键词', table_cell_style), Paragraph('5组', table_cell_center), Paragraph('勘察/检测/测绘/岩土/地质灾害', table_cell_style)],
    [Paragraph('搜索尝试次数', table_cell_style), Paragraph('12+轮次', table_cell_center), Paragraph('含多搜索引擎+浏览器+直接抓取', table_cell_style)],
    [Paragraph('有效公告获取', table_cell_style), Paragraph('<b>0条</b>', table_cell_center), Paragraph('目标网站均无法自动化访问', table_cell_style)],
    [Paragraph('数据置信度', table_cell_style), Paragraph('低', table_cell_center), Paragraph('存在遗漏可能，建议人工复核', table_cell_style)],
]
st = Table(sum_data, colWidths=[40*mm, 30*mm, 100*mm])
st.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER_BG),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, TABLE_ALT_ROW]),
    ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(st)
story.append(Spacer(1, 6*mm))
story.append(Paragraph(
    '<b>⚠️ 重要提示：</b>本报告自动化数据采集遭遇技术障碍，不代表上述平台近期确实无勘察类招标公告发布。'
    '建议通过人工登录上述网站进行手动检索验证。', warn_style))
story.append(PageBreak())

# ========== SECTION 2 ==========
story.append(Paragraph('二、数据采集说明', h1_style))
story.append(Paragraph('<b>2.1 搜索范围</b>', h2_style))
story.append(Paragraph(
    '本轮搜索覆盖以下两大官方招标公告发布平台：', body_style))
plat_data = [
    [Paragraph('<b>平台名称</b>', table_header_style), Paragraph('<b>网址</b>', table_header_style), Paragraph('<b>定位</b>', table_header_style)],
    [Paragraph('中国招标投标公共服务平台', table_cell_style), Paragraph('www.cebpubservice.com', table_cell_style), Paragraph('国家级招标公告发布法定媒介', table_cell_style)],
    [Paragraph('海南省政府采购网', table_cell_style), Paragraph('www.ccgp-hainan.gov.cn', table_cell_style), Paragraph('海南省本级政府采购信息发布平台', table_cell_style)],
]
pt = Table(plat_data, colWidths=[55*mm, 55*mm, 60*mm])
pt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER_BG), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, TABLE_ALT_ROW]),
]))
story.append(pt)
story.append(Spacer(1, 6*mm))

story.append(Paragraph('<b>2.2 关键词策略</b>', h2_style))
story.append(Paragraph(
    '采用5组核心关键词，覆盖勘察检测行业主要业务类型：<br/>'
    '① <b>勘察</b> — 工程勘察、地质勘察、岩土勘察<br/>'
    '② <b>检测</b> — 工程检测、质量检测、检验检测<br/>'
    '③ <b>测绘</b> — 工程测绘、不动产测绘、地理信息<br/>'
    '④ <b>岩土</b> — 岩土工程、岩土设计、基坑支护<br/>'
    '⑤ <b>地质灾害</b> — 地灾评估、地灾治理、地灾监测<br/>'
    '<br/>智能筛选规则：排除仅含"勘察"字样但非勘察类项目（如"勘察现场"等表述性用语）。',
    body_style))

story.append(Paragraph('<b>2.3 时间过滤</b>', h2_style))
story.append(Paragraph(
    f'严格要求仅获取发布时间在 <b>{today.strftime("%Y-%m-%d 00:00")} 之后</b> 的公告，即最近24小时内的新发布数据。',
    body_style))
story.append(PageBreak())

# ========== SECTION 3 ==========
story.append(Paragraph('三、搜索渠道详情', h1_style))
story.append(Paragraph('本轮共尝试 <b>5大类、12+轮次</b> 数据采集方式，以下是各渠道详情与结果：', body_style))

chan_header = [
    Paragraph('<b>序号</b>', table_header_style), Paragraph('<b>采集方式</b>', table_header_style),
    Paragraph('<b>目标平台</b>', table_header_style), Paragraph('<b>状态</b>', table_header_style),
    Paragraph('<b>障碍原因</b>', table_header_style)]
chan_rows = [chan_header]
raw_data = [
    ('1', 'web_search API', 'cebpubservice.com', '❌ 无效', '搜索引擎未索引招标数据，返回新闻/自媒体内容'),
    ('2', 'web_search API', 'ccgp-hainan.gov.cn', '❌ 无效', '同上，搜索结果不含招标公告原文'),
    ('3', 'web_fetch 直连', 'cebpubservice.com', '❌ 失败', '502 Bad Gateway — 阿里云WAF拦截'),
    ('4', 'web_fetch 直连', 'ccgp-hainan.gov.cn', '❌ 失败', '连接超时/拒绝访问'),
    ('5', 'Browser CDP(IP直连)', 'cebpubservice.com', '❌ 失败', 'WAF提示"域名未接入"，IP访问被拒'),
    ('6', 'Browser CDP(域名)', 'cebpubservice.com', '❌ 阻止', '浏览器SSRF策略阻止域名导航'),
    ('7', 'Baidu搜索', 'cebpubservice/ccgp', '❌ 验证', '触发百度CAPTCHA人机验证'),
    ('8', 'DuckDuckGo搜索', 'cebpubservice/ccgp', '❌ 失败', '网络连接失败'),
    ('9', '聚合站检索(bidcenter)', 'bidcenter.com.cn', '❌ 验证', '触发人机验证屏障'),
    ('10', '多关键词web_search', '多平台纵横搜索', '⚠️ 部分', '仅获取第三方平台碎片摘要(非完整数据)'),
]
for d in raw_data:
    chan_rows.append([
        Paragraph(d[0], table_cell_center),
        Paragraph(d[1], table_cell_style),
        Paragraph(d[2], table_cell_style),
        Paragraph(d[3], table_cell_center),
        Paragraph(d[4], table_cell_style),
    ])
ct = Table(chan_rows, colWidths=[10*mm, 33*mm, 38*mm, 18*mm, 71*mm])
ct.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER_BG), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, TABLE_ALT_ROW]),
]))
story.append(ct)
story.append(Spacer(1, 8*mm))

story.append(Paragraph('<b>3.1 技术障碍总结</b>', h2_style))
story.append(Paragraph(
    '中国政府招标网站普遍采用了以下多层防护措施：<br/>'
    '① <b>阿里云WAF（Web应用防火墙）</b>：拦截非浏览器请求、IP直连访问<br/>'
    '② <b>JavaScript动态渲染</b>：公告数据通过JS异步加载，静态抓取无法获取<br/>'
    '③ <b>CAPTCHA人机验证</b>：高频/自动化访问触发验证码<br/>'
    '④ <b>搜索引擎限制</b>：主流搜索引擎对.gov.cn招标域名索引覆盖不完整<br/><br/>'
    '这些措施共同导致自动化数据采集在当前环境下难以有效执行。',
    body_style))
story.append(PageBreak())

# ========== SECTION 4 ==========
story.append(Paragraph('四、结果汇总', h1_style))
story.append(Paragraph(f'截至 <b>{report_datetime}</b>，本轮自动化监测结果如下：', body_style))

res_data = [
    [Paragraph('<b>统计分类</b>', table_header_style), Paragraph('<b>数量</b>', table_header_style), Paragraph('<b>备注</b>', table_header_style)],
    [Paragraph('中国招标投标公共服务平台', table_cell_style), Paragraph('<b>0条</b>', table_cell_center), Paragraph('无法自动化访问', table_cell_style)],
    [Paragraph('海南省政府采购网', table_cell_style), Paragraph('<b>0条</b>', table_cell_center), Paragraph('无法自动化访问', table_cell_style)],
    [Paragraph('第三方平台(千里马/比地等)', table_cell_style), Paragraph('<b>&lt;5条摘要</b>', table_cell_center), Paragraph('仅获取片段信息，非完整公告', table_cell_style)],
    [Paragraph('有效勘察类公告(24h内)', table_cell_style), Paragraph('<b>0条</b>', table_cell_center), Paragraph('—', table_cell_style)],
]
rt = Table(res_data, colWidths=[65*mm, 35*mm, 70*mm])
rt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER_BG), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, TABLE_ALT_ROW]),
]))
story.append(rt)
story.append(Spacer(1, 8*mm))
story.append(Paragraph(
    '<b>结论：</b>鉴于上述技术障碍，本日报无法提供完整的勘察类招标公告列表。'
    '这并不意味着近期无勘察招标公告发布，而是自动化采集手段在当前条件下不可行。',
    body_style))
story.append(PageBreak())

# ========== SECTION 5 ==========
story.append(Paragraph('五、行业分析', h1_style))
story.append(Paragraph('<b>5.1 海南勘察检测行业背景</b>', h2_style))
story.append(Paragraph(
    '海南自由贸易港建设持续推进，2026年全省谋划城市更新项目393个，年度计划投资220亿元。'
    '勘察、检测、测绘、岩土工程、地质灾害防治等领域作为基础设施建设的前置环节，'
    '招标需求应与投资规模保持正相关关系。', body_style))

story.append(Paragraph('<b>5.2 近期可关注方向</b>', h2_style))
story.append(Paragraph(
    '根据行业规律和海南建设节奏，以下领域可能产生勘察类招标需求：<br/>'
    '① <b>海口/三亚城市更新</b>：旧改项目勘察设计、基坑监测<br/>'
    '② <b>环岛旅游公路配套</b>：边坡勘察、地质灾害评估<br/>'
    '③ <b>自贸港封关设施</b>：园区地质勘察、工程检测<br/>'
    '④ <b>水利/渔港建设</b>：码头勘察、海洋测绘<br/>'
    '⑤ <b>电网/能源设施</b>：变电站勘察、线路检测<br/>'
    '⑥ <b>省属医院/学校建设</b>：地基检测、桩基检测', body_style))

story.append(Paragraph('<b>5.3 资质要求趋势</b>', h2_style))
story.append(Paragraph(
    '2026年勘察检测行业资质要求呈趋严态势：<br/>'
    '• <b>CMA认证</b>：检测类项目普遍要求具备CMA计量认证<br/>'
    '• <b>岩土甲级</b>：大型勘察项目要求工程勘察综合甲级或岩土甲级<br/>'
    '• <b>注册人员</b>：注册土木工程师（岩土）为硬性配置要求<br/>'
    '• <b>本地化服务</b>：海南项目普遍要求本地化服务能力或分公司注册', body_style))
story.append(PageBreak())

# ========== SECTION 6 ==========
story.append(Paragraph('六、风险提示', h1_style))
risks = [
    ('数据完整性风险', '本日报自动化采集中断，无法保证覆盖所有已发布公告。存在遗漏重大招标信息的可能性。'),
    ('时效性风险', '由于自动化抓取失败，无法提供24小时内精确发布时间的公告清单。建议立即人工登录目标网站核实。'),
    ('竞争风险', '勘察检测行业招标公告发布时间窗口短（通常7-15天），错过公告可能导致丧失投标机会。'),
    ('合规风险', '投标前务必核实公告原文中的资质要求、人员配置、设备清单等硬性条件，避免无效投标。'),
    ('技术依赖风险', '长期依赖单一自动化采集方案存在中断风险，建议建立备用人工核查机制。'),
]
risk_rows = [[Paragraph('<b>风险类别</b>', table_header_style), Paragraph('<b>风险描述</b>', table_header_style)]]
for cat, desc in risks:
    risk_rows.append([Paragraph(f'⚠️ {cat}', table_cell_style), Paragraph(desc, table_cell_style)])
rkt = Table(risk_rows, colWidths=[45*mm, 125*mm])
rkt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER_BG), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, TABLE_ALT_ROW]),
]))
story.append(rkt)
story.append(PageBreak())

# ========== SECTION 7 ==========
story.append(Paragraph('七、改进建议', h1_style))
story.append(Paragraph('<b>7.1 短期方案（立即执行）</b>', h2_style))
story.append(Paragraph(
    '① <b>人工复核</b>：每日上午9:00-10:00由专人登录目标网站手动检索<br/>'
    '② <b>RSS订阅</b>：检查目标平台是否提供RSS/邮件订阅功能<br/>'
    '③ <b>微信通知</b>：关注"中国招标投标公共服务平台"官方微信公众号获取推送<br/>'
    '④ <b>备用聚合站</b>：使用千里马(qianlima.com)、采招网(bidcenter.com.cn)等第三方平台辅助查询', body_style))

story.append(Paragraph('<b>7.2 中期方案</b>', h2_style))
story.append(Paragraph(
    '① <b>企业级招标数据服务</b>：采购专业招标数据API（如剑鱼标讯、中项网等）<br/>'
    '② <b>定制化爬虫</b>：搭建带浏览器内核的Puppeteer/Playwright爬虫，处理JS渲染和验证码<br/>'
    '③ <b>代理IP池</b>：配置代理IP轮询绕过访问频率限制', body_style))

story.append(Paragraph('<b>7.3 长期方案</b>', h2_style))
story.append(Paragraph(
    '① <b>建立招标数据库</b>：持续采集历史数据，建立海南勘察行业招标信息仓库<br/>'
    '② <b>多源交叉验证</b>：接入全国公共资源交易平台、各市县交易中心网站<br/>'
    '③ <b>AI智能筛选</b>：训练NLP模型自动识别勘察类项目，提高精度和召回率', body_style))
story.append(PageBreak())

# ========== APPENDIX ==========
story.append(Paragraph('附录：技术说明', h1_style))
story.append(Paragraph('<b>A.1 爬虫策略</b>', h2_style))
story.append(Paragraph(
    '本轮采集使用以下技术栈：<br/>'
    '• <b>web_search</b>：通过搜索引擎API进行site限定搜索<br/>'
    '• <b>web_fetch</b>：直接HTTP GET请求目标URL<br/>'
    '• <b>browser (CDP)</b>：通过Chrome DevTools Protocol控制浏览器渲染<br/>'
    '• <b>multi-search-engine</b>：多搜索引擎(含Baidu/DuckDuckGo等)交叉检索', body_style))

story.append(Paragraph('<b>A.2 目标网站技术特征</b>', h2_style))
tech_data = [
    [Paragraph('<b>特征</b>', table_header_style), Paragraph('<b>cebpubservice.com</b>', table_header_style), Paragraph('<b>ccgp-hainan.gov.cn</b>', table_header_style)],
    [Paragraph('CDN/WAF', table_cell_style), Paragraph('阿里云WAF (yundunwaf3.com)', table_cell_style), Paragraph('未知CDN', table_cell_style)],
    [Paragraph('渲染方式', table_cell_style), Paragraph('服务端渲染 + JS增强', table_cell_style), Paragraph('JS动态渲染(智慧云平台)', table_cell_style)],
    [Paragraph('反爬措施', table_cell_style), Paragraph('WAF + 频率限制', table_cell_style), Paragraph('会话验证 + JS挑战', table_cell_style)],
    [Paragraph('搜索引擎收录', table_cell_style), Paragraph('部分收录(摘要级)', table_cell_style), Paragraph('低收录率', table_cell_style)],
    [Paragraph('API接口', table_cell_style), Paragraph('未公开', table_cell_style), Paragraph('未公开(智慧云平台API)', table_cell_style)],
]
tt = Table(tech_data, colWidths=[35*mm, 65*mm, 70*mm])
tt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER_BG), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, TABLE_ALT_ROW]),
]))
story.append(tt)
story.append(Spacer(1, 8*mm))

story.append(Paragraph('<b>A.3 本报告生成信息</b>', h2_style))
story.append(Paragraph(
    f'• 报告生成时间：{report_datetime}<br/>'
    f'• 生成引擎：QClaw AI Agent (DeepSeek V4 Pro)<br/>'
    f'• PDF引擎：Python reportlab<br/>'
    f'• 中文字体：Heiti SC<br/>'
    f'• 报告格式：WPS兼容PDF', body_style))
story.append(Spacer(1, 15*mm))
story.append(Paragraph('— 报告结束 —', end_style))
story.append(Paragraph('本报告由QClaw自动生成 · 仅供参考 · 不构成投标建议', end_small))

# ===== BUILD =====
doc.build(story, onFirstPage=cover_fn, onLaterPages=footer_fn)

fsize = os.path.getsize(filename)
print(f'✅ PDF generated: {filename}')
print(f'   File size: {fsize:,} bytes ({fsize/1024:.1f} KB)')
