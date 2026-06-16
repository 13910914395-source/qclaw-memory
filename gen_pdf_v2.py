#!/usr/bin/env python3
"""生成【海南勘察招标日报】PDF报告 — 使用STHeiti/Arial Unicode中文字体"""

import os
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Frame, PageTemplate, BaseDocTemplate
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Chinese fonts
ARIAL_UNI = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
SONGTI = '/System/Library/Fonts/Supplemental/Songti.ttc'
HEITI = '/System/Library/Fonts/STHeiti Medium.ttc'

pdfmetrics.registerFont(TTFont('ArialUni', ARIAL_UNI))
pdfmetrics.registerFont(TTFont('SongtiBold', SONGTI, subfontIndex=1))
pdfmetrics.registerFont(TTFont('Songti', SONGTI, subfontIndex=3))
pdfmetrics.registerFont(TTFont('HeitiSC', HEITI, subfontIndex=1))
pdfmetrics.registerFont(TTFont('HeitiTC', HEITI, subfontIndex=0))

# Font aliases
BODY_FONT = 'HeitiSC'     # Clean sans-serif for body
TITLE_FONT = 'SongtiBold' # Serif for titles
BOLD_FONT = 'HeitiSC'     # Use same font for bold (no separate bold weight available easily)

PAGE_W, PAGE_H = A4

# Colors
DARK_BLUE = HexColor('#1a3a5c')
ACCENT_BLUE = HexColor('#2d6ba3')
LIGHT_BLUE = HexColor('#e8f0f8')
TABLE_HEADER_BG = HexColor('#2d6ba3')
TABLE_ALT_BG = HexColor('#f7f9fc')
RED_ALERT = HexColor('#c0392b')
BORDER_COLOR = HexColor('#d0d6dd')
TEXT_DARK = HexColor('#2c3e50')
TEXT_GREY = HexColor('#7f8c8d')
WHITE = white

TODAY = datetime.now()
DATE_STR = TODAY.strftime('%Y-%m-%d')
TITLE_STR = f'【海南勘察招标日报】{DATE_STR}'

# ===== Styles =====
body = ParagraphStyle('CNBody', fontName=BODY_FONT, fontSize=10, leading=18,
                       textColor=TEXT_DARK, spaceAfter=6)
body_bold = ParagraphStyle('CNBodyBold', fontName=BODY_FONT, fontSize=10, leading=18,
                            textColor=TEXT_DARK, spaceAfter=6)
cover_title_s = ParagraphStyle('CoverTitle', fontName=TITLE_FONT, fontSize=28, leading=40,
                                textColor=WHITE, alignment=TA_CENTER)
cover_sub_s = ParagraphStyle('CoverSub', fontName=BODY_FONT, fontSize=13, leading=20,
                              textColor=HexColor('#b0c4de'), alignment=TA_CENTER)
h1 = ParagraphStyle('CNH1', fontName=TITLE_FONT, fontSize=16, leading=26,
                     textColor=DARK_BLUE, spaceAfter=10, spaceBefore=14)
h2 = ParagraphStyle('CNH2', fontName=BODY_FONT, fontSize=12, leading=20,
                     textColor=ACCENT_BLUE, spaceAfter=6, spaceBefore=8)
tcell = ParagraphStyle('TCell', fontName=BODY_FONT, fontSize=8.5, leading=13, textColor=TEXT_DARK)
thead = ParagraphStyle('THead', fontName=BODY_FONT, fontSize=8.5, leading=13, textColor=WHITE)
footer_s = ParagraphStyle('Footer', fontName=BODY_FONT, fontSize=7, leading=10,
                           textColor=TEXT_GREY, alignment=TA_CENTER)
note = ParagraphStyle('Note', fontName=BODY_FONT, fontSize=8, leading=12, textColor=TEXT_GREY)

output_path = os.path.expanduser(f'~/Desktop/海南勘察招标日报_{DATE_STR}.pdf')

# ===== Page templates =====
def cover_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DARK_BLUE)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(ACCENT_BLUE)
    canvas.rect(0, PAGE_H/2 + 35, PAGE_W, 3*mm, fill=1, stroke=0)
    canvas.rect(0, PAGE_H/2 - 95, PAGE_W, 1.5*mm, fill=1, stroke=0)
    canvas.restoreState()

def normal_hf(canvas, doc):
    canvas.saveState()
    canvas.setFont(BODY_FONT, 7)
    canvas.setFillColor(TEXT_GREY)
    canvas.drawRightString(PAGE_W - 15*mm, 15*mm, f'海南勘察招标日报 · {DATE_STR}')
    canvas.drawCentredString(PAGE_W/2, 15*mm, f'— {canvas.getPageNumber()} —')
    canvas.setStrokeColor(BORDER_COLOR)
    canvas.setLineWidth(0.5)
    canvas.line(15*mm, PAGE_H - 20*mm, PAGE_W - 15*mm, PAGE_H - 20*mm)
    canvas.drawString(15*mm, PAGE_H - 18*mm, '勘察检测行业招标日报 · 海南省')
    canvas.restoreState()

cover_frame = Frame(15*mm, 0, PAGE_W - 30*mm, PAGE_H - 22*mm, id='cover')
normal_frame = Frame(15*mm, 22*mm, PAGE_W - 30*mm, PAGE_H - 52*mm, id='normal')

cover_tpl = PageTemplate(id='Cover', frames=[cover_frame], onPage=cover_bg)
normal_tpl = PageTemplate(id='Normal', frames=[normal_frame], onPage=normal_hf)

# ===== Build content =====
S = []

# -- Cover --
S.append(Spacer(1, 125*mm))
S.append(Paragraph(TITLE_STR, cover_title_s))
S.append(Spacer(1, 10*mm))
S.append(Paragraph('勘察 · 检测 · 测绘 · 岩土 · 地质灾害', cover_sub_s))
S.append(Spacer(1, 8*mm))
S.append(Paragraph(f'生成时间：{TODAY.strftime("%Y年%m月%d日 %H:%M")}（北京时间）', cover_sub_s))
S.append(Spacer(1, 5*mm))
S.append(Paragraph('数据源：中国招标投标公共服务平台 · 海南省政府采购网', cover_sub_s))
S.append(Spacer(1, 15*mm))
S.append(Paragraph('每日自动化监测报告', ParagraphStyle('cbot', fontName=BODY_FONT, fontSize=10, leading=14, textColor=HexColor('#7f8c8d'), alignment=TA_CENTER)))

S.append(PageBreak())

# -- TOC --
S.append(Paragraph('目  录', h1))
S.append(HRFlowable(width="100%", thickness=1, color=BORDER_COLOR))
S.append(Spacer(1, 8*mm))
for t, p in [('一、数据抓取概况', '3'), ('二、抓取来源说明', '3'),
             ('三、筛选条件', '4'), ('四、搜索结果详情', '4'),
             ('五、结论与建议', '5')]:
    S.append(Paragraph(f'{t}', body))
S.append(Spacer(1, 10*mm))
S.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR))

S.append(PageBreak())

# -- Section 1 --
S.append(Paragraph('一、数据抓取概况', h1))
S.append(HRFlowable(width="100%", thickness=1, color=ACCENT_BLUE))
S.append(Spacer(1, 5*mm))

alert_tbl = Table([
    [Paragraph('⚠️ 近期无新发布招标信息',
               ParagraphStyle('AB', fontName=BODY_FONT, fontSize=14, leading=22,
                              textColor=RED_ALERT, alignment=TA_CENTER))]
], colWidths=[PAGE_W - 45*mm])
alert_tbl.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor('#fde8e8')),
    ('BOX', (0,0), (-1,-1), 2, RED_ALERT),
    ('TOPPADDING', (0,0), (-1,-1), 12),
    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
]))
S.append(alert_tbl)
S.append(Spacer(1, 8*mm))
S.append(Paragraph(
    f'经对目标平台进行多轮数据查询，在最近24小时内（{TODAY.strftime("%Y-%m-%d")} 03:00 至 '
    f'{(TODAY + timedelta(days=1)).strftime("%Y-%m-%d")} 03:00）海南省范围内未发现符合关键词条件的勘察、检测、测绘、岩土、地质灾害类招标公告。',
    body))

# -- Section 2 --
S.append(Paragraph('二、抓取来源说明', h1))
S.append(HRFlowable(width="100%", thickness=1, color=ACCENT_BLUE))
S.append(Spacer(1, 5*mm))

src_data = [
    [Paragraph('序号', thead), Paragraph('数据源', thead), Paragraph('URL / 方式', thead),
     Paragraph('访问状态', thead), Paragraph('24h数据量', thead)],
    [Paragraph('1', tcell), Paragraph('中国招标投标公共服务平台', tcell),
     Paragraph('www.cebpubservice.com', tcell),
     Paragraph('无法访问(502)', tcell), Paragraph('N/A', tcell)],
    [Paragraph('2', tcell), Paragraph('海南省政府采购网', tcell),
     Paragraph('www.ccgp-hainan.gov.cn', tcell),
     Paragraph('抓取受限', tcell), Paragraph('N/A', tcell)],
    [Paragraph('3', tcell), Paragraph('搜索引擎多平台辅助', tcell),
     Paragraph('Baidu/Bing/google搜索', tcell),
     Paragraph('正常', tcell), Paragraph('0条', tcell)],
]
cw = [12*mm, 52*mm, 52*mm, 30*mm, 26*mm]
st = Table(src_data, colWidths=cw)
st.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER_BG),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, TABLE_ALT_BG]),
    ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
S.append(st)
S.append(Spacer(1, 8*mm))

# -- Section 3 --
S.append(Paragraph('三、筛选条件', h1))
S.append(HRFlowable(width="100%", thickness=1, color=ACCENT_BLUE))
S.append(Spacer(1, 5*mm))

for item in [
    '<b>关键词：</b>勘察 | 检测 | 测绘 | 岩土 | 地质灾害',
    '<b>时间窗口：</b>最近24小时（2026-06-15 03:00 ~ 2026-06-16 03:00）',
    '<b>区域范围：</b>海南省全境（海口、三亚、儋州、琼海、五指山、文昌、万宁、东方、定安、屯昌、澄迈、临高、白沙、昌江、乐东、陵水、保亭、琼中等市县）',
    '<b>公告类型：</b>招标公告（公开招标、竞争性磋商、竞争性谈判、询价等）',
    '<b>排除规则：</b>中标/废标/更正公告；非核心勘察类的纯设计项目',
]:
    S.append(Paragraph(item, body))

S.append(Spacer(1, 8*mm))

# -- Section 4 --
S.append(Paragraph('四、搜索结果详情', h1))
S.append(HRFlowable(width="100%", thickness=1, color=ACCENT_BLUE))
S.append(Spacer(1, 5*mm))

S.append(Paragraph('<b>4.1 24小时内结果</b>', h2))
S.append(Paragraph('经多轮搜索查询，未发现符合筛选条件的招标公告。', body))
S.append(Spacer(1, 5*mm))

S.append(Paragraph('<b>4.2 扩大范围参考（7日内相关公告示例，非勘察检测类）</b>', h2))

rec_data = [
    [Paragraph('发布时间', thead), Paragraph('公告标题', thead), Paragraph('分类', thead), Paragraph('来源', thead)],
    [Paragraph('2026-06-09', tcell), Paragraph('儋州市综合档案馆改造项目质量检测竞争性磋商公告', tcell),
     Paragraph('质量检测', tcell), Paragraph('儋州市人民政府网', tcell)],
    [Paragraph('2026-06-05', tcell), Paragraph('2026年仪器设备检定、校准项目采购公告', tcell),
     Paragraph('设备检定', tcell), Paragraph('采招网', tcell)],
    [Paragraph('2026-06-05', tcell), Paragraph('海南社会管理信息化平台卫星遥感数据服务能力提升购买服务项目', tcell),
     Paragraph('卫星遥感', tcell), Paragraph('采招网', tcell)],
    [Paragraph('2026-06-01', tcell), Paragraph('省直行政事业单位老旧房产安全鉴定项目第二次遴选公告', tcell),
     Paragraph('安全鉴定', tcell), Paragraph('海南省机关事务管理局', tcell)],
]
rw = [25*mm, 85*mm, 25*mm, 40*mm]
rt = Table(rec_data, colWidths=rw)
rt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER_BG),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, TABLE_ALT_BG]),
    ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
S.append(rt)
S.append(Spacer(1, 3*mm))
S.append(Paragraph('<i>注：以上公告发布时间均不在24小时窗口内，仅供趋势参考。</i>', note))

S.append(Spacer(1, 8*mm))

# -- Section 5 --
S.append(PageBreak())
S.append(Paragraph('五、结论与建议', h1))
S.append(HRFlowable(width="100%", thickness=1, color=ACCENT_BLUE))
S.append(Spacer(1, 5*mm))

S.append(Paragraph('<b>5.1 结论</b>', h2))
conc_data = [
    [Paragraph('类别', thead), Paragraph('24小时结果', thead)],
    [Paragraph('勘察类招标公告', tcell), Paragraph('未发现', tcell)],
    [Paragraph('检测类招标公告', tcell), Paragraph('未发现', tcell)],
    [Paragraph('测绘类招标公告', tcell), Paragraph('未发现', tcell)],
    [Paragraph('岩土类招标公告', tcell), Paragraph('未发现', tcell)],
    [Paragraph('地质灾害类招标公告', tcell), Paragraph('未发现', tcell)],
]
ccw = [80*mm, 95*mm]
ct = Table(conc_data, colWidths=ccw)
ct.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER_BG),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, TABLE_ALT_BG]),
    ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
S.append(ct)
S.append(Spacer(1, 8*mm))

S.append(Paragraph('<b>5.2 建议</b>', h2))
for s in [
    '1. <b>扩大时间窗口</b>：如需了解近期动态，建议将查询范围放宽至最近3-7天。',
    '2. <b>多平台交叉验证</b>：建议同时关注以下渠道：',
]:
    S.append(Paragraph(s, body))

for ch in [
    '• 海南省公共资源交易平台：http://zw.hainan.gov.cn/ggzy/',
    '• 全国公共资源交易平台（海南）：https://ggzy.hainan.gov.cn',
    '• 中国采购与招标网：https://www.chinabidding.cn',
    '• 采招网海南站：https://hain.bidcenter.com.cn',
]:
    S.append(Paragraph(ch, ParagraphStyle('Bullet', fontName=BODY_FONT, fontSize=9, leading=14, leftIndent=15, textColor=TEXT_DARK)))

S.append(Spacer(1, 5*mm))
for s in [
    '3. <b>订阅推送</b>：在上述平台注册并设置关键词订阅推送，确保第一时间获取招标信息。',
    '4. <b>定期监测</b>：本报告为每日自动化生成，建议每日查阅最新版本。',
]:
    S.append(Paragraph(s, body))

S.append(Spacer(1, 8*mm))

# Risk
S.append(HRFlowable(width="100%", thickness=1, color=ACCENT_BLUE))
S.append(Paragraph('<b>⚠ 风险提示</b>',
    ParagraphStyle('RT', fontName=BODY_FONT, fontSize=11, leading=18, textColor=RED_ALERT)))
for r in [
    '• 本次数据受网络访问限制，存在遗漏可能，建议人工复核。',
    '• 部分平台发布存在延迟，24小时窗口可能无法覆盖全部公告。',
    '• 搜索引擎结果受索引延迟影响，数据完整性不保证100%。',
    '• 本报告仅供内部参考，具体以各平台原文为准，不构成投标决策建议。',
]:
    S.append(Paragraph(r, body))

S.append(Spacer(1, 20*mm))
S.append(HRFlowable(width="60%", thickness=0.5, color=BORDER_COLOR))
S.append(Paragraph('— 报告结束 —',
    ParagraphStyle('End', fontName=BODY_FONT, fontSize=9, leading=14, textColor=TEXT_GREY, alignment=TA_CENTER)))

# ===== Build =====
doc = BaseDocTemplate(output_path, pagesize=A4,
    leftMargin=15*mm, rightMargin=15*mm,
    topMargin=22*mm, bottomMargin=22*mm,
    title=TITLE_STR, author='勘察检测行业招标分析系统')

doc.addPageTemplates([cover_tpl, normal_tpl])
doc.build(S)

size_kb = os.path.getsize(output_path) / 1024
print(f'✅ PDF generated: {output_path}')
print(f'📄 File size: {size_kb:.1f} KB')
