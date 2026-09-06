# -*- coding: utf-8 -*-
"""Generate 【海南勘察招标日报】 PDF report (WPS-compatible).
Reports the honest finding: no qualifying Hainan survey-type tenders
confirmed within the requested last-24h window.
"""
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# --- CJK font ---
try:
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    FONT = 'STSong-Light'
except Exception:
    FONT = 'Helvetica'

NOW = datetime.datetime.now()
GEN_TS = NOW.strftime('%Y-%m-%d %H:%M:%S')
REPORT_DATE = '2026-09-06'
WIN_START = '2026-09-05 03:00'
WIN_END = '2026-09-06 03:00'

# --- styles ---
ss = getSampleStyleSheet()
title_style = ParagraphStyle('T', parent=ss['Title'], fontName=FONT,
                              fontSize=26, leading=32, textColor=colors.HexColor('#1F3864'))
sub_style = ParagraphStyle('Sub', parent=ss['Normal'], fontName=FONT,
                           fontSize=12, leading=18, textColor=colors.HexColor('#444444'),
                           alignment=TA_CENTER)
h1 = ParagraphStyle('H1', parent=ss['Heading1'], fontName=FONT, fontSize=16,
                    leading=22, textColor=colors.HexColor('#1F3864'), spaceBefore=10, spaceAfter=6)
h2 = ParagraphStyle('H2', parent=ss['Heading2'], fontName=FONT, fontSize=13,
                    leading=18, textColor=colors.HexColor('#2E5496'), spaceBefore=8, spaceAfter=4)
body = ParagraphStyle('Body', parent=ss['Normal'], fontName=FONT, fontSize=10.5,
                      leading=16, alignment=TA_JUSTIFY, spaceAfter=6)
small = ParagraphStyle('Small', parent=ss['Normal'], fontName=FONT, fontSize=8.5,
                       leading=12, textColor=colors.HexColor('#333333'))
cell = ParagraphStyle('Cell', parent=ss['Normal'], fontName=FONT, fontSize=8,
                      leading=11)
cellb = ParagraphStyle('CellB', parent=ss['Normal'], fontName=FONT, fontSize=8,
                       leading=11, textColor=colors.HexColor('#B00000'))
note = ParagraphStyle('Note', parent=ss['Normal'], fontName=FONT, fontSize=11,
                      leading=18, textColor=colors.HexColor('#B00000'),
                      alignment=TA_CENTER, spaceBefore=6, spaceAfter=6)

story = []

# ===== Cover =====
story.append(Spacer(1, 3.2*cm))
story.append(Paragraph('【海南勘察招标日报】', title_style))
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph(REPORT_DATE, sub_style))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('勘察 / 检测 / 测绘 / 岩土 / 地质灾害 类招标信息监测', sub_style))
story.append(Spacer(1, 1.0*cm))
cover_tbl = Table([
    ['监测窗口', f'{WIN_START} ~ {WIN_END}（Asia/Shanghai，最近24小时）'],
    ['生成时间', GEN_TS],
    ['数据来源', '中国招标投标公共服务平台（www.cebpubservice.com）\n海南省政府采购网（www.ccgp-hainan.gov.cn）'],
    ['关键词', '勘察、检测、测绘、岩土、地质灾害'],
    ['分析口径', '仅纳入发布时间在监测窗口内、且为真实勘察/检测/测绘类项目'],
], colWidths=[3.2*cm, 11.3*cm])
cover_tbl.setStyle(TableStyle([
    ('FONTNAME', (0,0), (-1,-1), FONT),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#E8EEF7')),
    ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#1F3864')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#B8C4D8')),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
# wrap cells as paragraphs for multi-line
cover_data = [
    [Paragraph('监测窗口', cell), Paragraph(f'{WIN_START} ~ {WIN_END}（Asia/Shanghai，最近24小时）', cell)],
    [Paragraph('生成时间', cell), Paragraph(GEN_TS, cell)],
    [Paragraph('数据来源', cell), Paragraph('中国招标投标公共服务平台（www.cebpubservice.com）<br/>海南省政府采购网（www.ccgp-hainan.gov.cn）', cell)],
    [Paragraph('关键词', cell), Paragraph('勘察、检测、测绘、岩土、地质灾害', cell)],
    [Paragraph('分析口径', cell), Paragraph('仅纳入发布时间在监测窗口内、且为真实勘察/检测/测绘类项目', cell)],
]
cover_tbl = Table(cover_data, colWidths=[3.2*cm, 11.3*cm])
cover_tbl.setStyle(TableStyle([
    ('FONTNAME', (0,0), (-1,-1), FONT),
    ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#E8EEF7')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#B8C4D8')),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(cover_tbl)
story.append(Spacer(1, 1.2*cm))
story.append(Paragraph('【重要结论】本期监测窗口内（最近24小时），未确认到符合条件的海南地区勘察/检测/测绘/岩土/地质灾害类新发布公告。', note))
story.append(PageBreak())

# ===== TOC =====
story.append(Paragraph('目录', h1))
toc = [
    '一、执行摘要',
    '二、数据获取与筛选说明',
    '三、最近24小时监测结果',
    '四、临近窗口参考（非24小时内，仅供参考）',
    '五、风险提示与行动建议',
]
for t in toc:
    story.append(Paragraph(t, body))
story.append(PageBreak())

# ===== 1. Executive summary =====
story.append(Paragraph('一、执行摘要', h1))
story.append(Paragraph(
    '本次日报按既定要求，对<strong>中国招标投标公共服务平台</strong>与<strong>海南省政府采购网</strong>在'
    f'<strong>{WIN_START} 至 {WIN_END}</strong>（Asia/Shanghai，最近24小时）发布的、含「勘察 / 检测 / 测绘 / 岩土 / 地质灾害」'
    '关键词的公告进行抓取与智能筛选。', body))
story.append(Paragraph(
    '<strong>结论：在指定监测窗口内，未确认到任何符合条件的海南地区勘察/检测/测绘/岩土/地质灾害类新发布公告。</strong>'
    '即：本期<strong>近期无新发布招标信息</strong>。', body))
story.append(Paragraph(
    '说明：本报告严格遵循「仅纳入监测窗口内真实勘察类项目」的口径，未对任何公告进行虚构或估算。'
    '因海南省政府采购网在本次任务执行期间无法直连访问、中国招标投标公共服务平台为前端动态渲染（无法提取列表），'
    '结合可检索公开索引，无法证实该窗口内存在符合条件的海南项目。详见第二节与第五节。', body))

# ===== 2. Methodology =====
story.append(Paragraph('二、数据获取与筛选说明', h1))
story.append(Paragraph('1. 目标站点与状态', h2))
status_tbl = Table([
    [Paragraph('数据源', cell), Paragraph('可达性', cell), Paragraph('说明', cell)],
    [Paragraph('海南省政府采购网<br/>ccgp-hainan.gov.cn', cell),
     Paragraph('不可达', cellb),
     Paragraph('执行期间多次直连均返回 fetch failed，无法读取其公告列表及时间筛选结果。', cell)],
    [Paragraph('中国招标投标公共服务平台<br/>cebpubservice.com', cell),
     Paragraph('前端动态渲染', cellb),
     Paragraph('首页仅返回导航结构，公告列表依赖 JavaScript 渲染，现有抓取工具无法提取列表与发布时间字段。', cell)],
    [Paragraph('中国政府采购网（全国镜像）<br/>ccgp.gov.cn', cell),
     Paragraph('可达（参照）', cell),
     Paragraph('作为可访问镜像核对，其 24h feed 仅含新疆/山西/上海/浙江/山东等地公告，未出现海南勘察类项目。', cell)],
], colWidths=[4.2*cm, 2.6*cm, 7.7*cm])
status_tbl.setStyle(TableStyle([
    ('FONTNAME', (0,0), (-1,-1), FONT),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#B8C4D8')),
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1F3864')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(status_tbl)
story.append(Paragraph('2. 筛选规则', h2))
story.append(Paragraph(
    '• 时间筛选：仅保留发布时间在监测窗口（2026-09-05 03:00 ~ 2026-09-06 03:00）内的公告；<br/>'
    '• 关键词命中：标题或正文含「勘察 / 检测 / 测绘 / 岩土 / 地质灾害」；<br/>'
    '• 真实性识别：排除仅含「勘察」字样但实质为货物采购、设备更新、船舶/消防/物业等非勘察类项目；<br/>'
    '• 去重合并：跨源同一项目仅保留一条。', body))

# ===== 3. 24h result =====
story.append(Paragraph('三、最近24小时监测结果', h1))
story.append(Paragraph('近期无新发布招标信息', note))
story.append(Paragraph(
    '在 2026-09-05 03:00 至 2026-09-06 03:00 的监测窗口内，未能从指定数据源确认任何符合'
    '「海南地区 + 勘察/检测/测绘/岩土/地质灾害」条件的招标/采购公告。'
    '可检索公开索引中，最近的相关海南项目均发布于该窗口之前（详见第四节，均为非24小时内数据）。', body))

# ===== 4. Near-window reference =====
story.append(Paragraph('四、临近窗口参考（非24小时内，仅供参考）', h1))
story.append(Paragraph(
    '以下为可检索到的最近海南地区相关公告，<strong>发布时间均早于本次监测窗口</strong>，'
    '列出供业务参考，不构成 24h 新增数据。其中部分为设备采购/船舶检验，已标注类别以供甄别。', body))

ref_data = [
    [Paragraph('项目名称', cell), Paragraph('采购人', cell), Paragraph('预算', cell),
     Paragraph('发布时间', cell), Paragraph('截止时间', cell), Paragraph('类别', cell), Paragraph('原文链接', cell)],
    [Paragraph('万宁市北大镇东兴农场机关小区边坡崩塌等9个地质灾害隐患治理实施方案', cell),
     Paragraph('万宁市自然资源和规划局', cell), Paragraph('94.6万元', cell),
     Paragraph('2026-08-25', cell), Paragraph('2026-09-07 10:00', cell), Paragraph('地质灾害', cell),
     Paragraph('wanning.hainan.gov.cn/.../t20260825_4134097.html', small)],
    [Paragraph('海南省深海技术创新中心检测中心实验室能力提升设备采购(二次)', cell),
     Paragraph('海南省深海技术创新中心', cell), Paragraph('311万元', cell),
     Paragraph('2026-08-31', cell), Paragraph('2026-09-15 09:30', cell), Paragraph('检测(设备)', cell),
     Paragraph('ccgp.gov.cn/cggg/dfgg/jzxcs/202608/t20260831_27233743.htm', small)],
    [Paragraph('2026年重点工业产品检验检测设备更新项目', cell),
     Paragraph('海南省检验检测研究院', cell), Paragraph('4083万元', cell),
     Paragraph('2026-08-31', cell), Paragraph('2026-09-21 08:30', cell), Paragraph('检验检测(设备)', cell),
     Paragraph('ccgp.gov.cn/cggg/dfgg/gkzb/202608/t20260831_27234718.htm', small)],
    [Paragraph('文昌市2026年渔业船舶检验社会化服务项目(二次)', cell),
     Paragraph('文昌市', cell), Paragraph('134.8万元', cell),
     Paragraph('2026-09-02', cell), Paragraph('2026-09-14 09:30', cell), Paragraph('检验(船舶)', cell),
     Paragraph('ccgp.gov.cn/cggg/dfgg/jzxcs/202609/t20260902_27251565.htm', small)],
    [Paragraph('海南岛**海域微细粒砂矿综合回收技术优化服务(第三次)', cell),
     Paragraph('海南省海洋地质调查院', cell), Paragraph('详见文件', cell),
     Paragraph('2026-09-03', cell), Paragraph('2026-09-17 09:00', cell), Paragraph('地质(砂矿)', cell),
     Paragraph('geo.hainan.gov.cn/sdzj/0400/202609/f8f8f5e6....shtml', small)],
]
ref_tbl = Table(ref_data, colWidths=[4.4*cm, 2.6*cm, 1.5*cm, 1.7*cm, 1.9*cm, 1.7*cm, 3.1*cm], repeatRows=1)
ref_tbl.setStyle(TableStyle([
    ('FONTNAME', (0,0), (-1,-1), FONT),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#B8C4D8')),
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E5496')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F2F6FB')]),
]))
story.append(ref_tbl)
story.append(Paragraph(
    '注：上述链接为可检索来源页短址，完整 URL 以各平台原文为准；预算/截止时间取自公告概要，最终以招标文件为准。', small))

# ===== 5. Risks =====
story.append(Paragraph('五、风险提示与行动建议', h1))
story.append(Paragraph(
    '• 站点不可达风险：海南省政府采购网在本次执行期不可直连，可能遗漏其窗口内真实公告，建议在工作时段（09:00–18:00）复核；<br/>'
    '• 索引滞后风险：公开检索索引存在抓取延迟，窗口临界点（临近 03:00）的公告可能暂未收录；<br/>'
    '• 动态渲染限制：cebpubservice.com 需浏览器交互方可读取列表，当前工具无法替代其站内时间筛选；<br/>'
    '• 业务建议：若需确保不漏标，建议改为每日 09:30 与 18:00 两个时点各运行一次，并接入平台官方订阅/API（如平台信息定制、信息API服务）。', body))
story.append(Spacer(1, 0.4*cm))
story.append(HRFlowable(width='100%', color=colors.HexColor('#B8C4D8')))
story.append(Paragraph(
    f'本报告由勘察检测行业招标分析助手自动生成 · 生成时间 {GEN_TS} · 监测窗口 {WIN_START}~{WIN_END}', small))

# ===== footer =====
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(colors.HexColor('#888888'))
    canvas.drawString(2*cm, 1.1*cm, f'【海南勘察招标日报】{REPORT_DATE}  ·  生成 {GEN_TS}')
    canvas.drawRightString(A4[0]-2*cm, 1.1*cm, f'第 {doc.page} 页')
    canvas.setStrokeColor(colors.HexColor('#B8C4D8'))
    canvas.line(2*cm, 1.4*cm, A4[0]-2*cm, 1.4*cm)
    canvas.restoreState()

doc = SimpleDocTemplate(
    '/Users/fasimac/.qclaw/workspace/海南勘察招标日报_2026-09-06.pdf',
    pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=1.8*cm,
    title=f'【海南勘察招标日报】{REPORT_DATE}', author='勘察检测行业招标分析助手')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print('PDF generated.')
