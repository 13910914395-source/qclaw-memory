# -*- coding: utf-8 -*-
import base64
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
FONT = 'STSong-Light'

def S(name, **kw):
    return ParagraphStyle(name, fontName=FONT, **kw)

title_style = S('TitleC', fontSize=25, leading=30, alignment=TA_CENTER,
                textColor=colors.HexColor('#1F3864'))
sub_style = S('SubC', fontSize=12, leading=17, alignment=TA_CENTER,
              textColor=colors.HexColor('#44546A'))
h1 = S('H1', fontSize=14, leading=19, spaceBefore=8, spaceAfter=5,
       textColor=colors.HexColor('#1F3864'))
body = S('Body', fontSize=10, leading=15, spaceAfter=4, alignment=TA_LEFT)
small = S('Small', fontSize=8.5, leading=12, textColor=colors.HexColor('#555555'))
hl = S('hl', fontSize=13, leading=18, textColor=colors.HexColor('#C00000'),
       alignment=TA_CENTER)
cell = S('cell', fontSize=8, leading=11)
cellh = S('cellh', fontSize=8, leading=11, textColor=colors.white)
concl = S('Concl', fontSize=14, leading=20, alignment=TA_CENTER,
          textColor=colors.white)

OUT = '/Users/fasimac/.qclaw/workspace/海南勘察招标日报_2026-08-12.pdf'
doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=2*cm, rightMargin=2*cm,
                        topMargin=1.8*cm, bottomMargin=1.8*cm,
                        title='海南勘察招标日报 2026-08-12',
                        author='勘察检测行业招标分析系统')

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(colors.HexColor('#888888'))
    canvas.drawString(2*cm, 1.05*cm, '海南勘察招标日报 · 2026-08-12')
    canvas.drawCentredString(A4[0]/2, 1.05*cm, '自动生成 · 数据以官方平台为准')
    canvas.drawRightString(A4[0]-2*cm, 1.05*cm, '第 %d 页' % doc.page)
    canvas.setStrokeColor(colors.HexColor('#CCCCCC'))
    canvas.line(2*cm, 1.35*cm, A4[0]-2*cm, 1.35*cm)
    canvas.restoreState()

story = []
story.append(Spacer(1, 2.0*cm))
story.append(Paragraph('海南勘察招标日报', title_style))
story.append(Spacer(1, 0.35*cm))
story.append(Paragraph('勘察 · 检测 · 测绘 · 岩土 · 地质灾害 招标监测日报', sub_style))
story.append(Spacer(1, 0.7*cm))

cover_tbl = Table([
    [Paragraph('报告日期', cell), Paragraph('2026年8月12日（星期三）', cell)],
    [Paragraph('统计窗口', cell), Paragraph('最近24小时：2026-08-11 03:00 至 2026-08-12 03:00', cell)],
    [Paragraph('监测来源', cell), Paragraph('中国招标投标公共服务平台、海南省政府采购网', cell)],
    [Paragraph('监测关键词', cell), Paragraph('勘察 / 检测 / 测绘 / 岩土 / 地质灾害', cell)],
    [Paragraph('生成方式', cell), Paragraph('招标分析系统自动抓取与生成', cell)],
], colWidths=[3.0*cm, 11.5*cm])
cover_tbl.setStyle(TableStyle([
    ('FONT', (0,0), (-1,-1), FONT, 9),
    ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#D9E1F2')),
    ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#1F3864')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#B4C6E7')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(cover_tbl)
story.append(Spacer(1, 0.7*cm))

box = Table([[Paragraph('核心结论：近期无新发布招标信息', concl)]], colWidths=[14.5*cm])
box.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#C00000')),
    ('TOPPADDING', (0,0), (-1,-1), 9),
    ('BOTTOMPADDING', (0,0), (-1,-1), 9),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
]))
story.append(box)
story.append(Spacer(1, 0.45*cm))
story.append(Paragraph('说明：在最近24小时统计窗口内，两个官方平台均未检索到符合条件的勘察类新公告。详见正文核查详情。', small))
story.append(PageBreak())

story.append(Paragraph('目录', h1))
for it in ['一、核心结论', '二、核查详情与时间窗口', '三、数据来源与抓取方法',
           '四、窗口外近期参考动态（非24h内）', '五、风险提示与应对建议',
           '六、附录：字段与口径说明']:
    story.append(Paragraph(it, body))
story.append(PageBreak())

story.append(Paragraph('一、核心结论', h1))
story.append(Paragraph('📌 近期无新发布招标信息', hl))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph('在 2026-08-11 03:00 至 2026-08-12 03:00 的统计窗口内，下列两个官方平台均未发现符合"勘察/检测/测绘/岩土/地质灾害"关键词的新招标/采购公告：', body))
story.append(Paragraph('• 中国招标投标公共服务平台（www.cebpubservice.com / bulletin.cebpubservice.com）<br/>'
                       '• 海南省政府采购网（www.ccgp-hainan.gov.cn）', body))
story.append(Paragraph('因此，本期日报无可提取的项目名称、预算金额、采购人、资质要求、截止日期等字段，不对任何投标决策提供依据。', body))

story.append(Paragraph('二、核查详情与时间窗口', h1))
rows = [
    [Paragraph('核查项', cellh), Paragraph('结果', cellh)],
    [Paragraph('统计窗口', cell), Paragraph('2026-08-11 03:00 — 2026-08-12 03:00（最近24小时）', cell)],
    [Paragraph('CEB平台 窗口内新公告', cell), Paragraph('0 条（聚合索引与今日发布计数均无匹配）', cell)],
    [Paragraph('海南政府采购网 窗口内新公告', cell), Paragraph('0 条（公开索引无 08-11/08-12 匹配项）', cell)],
    [Paragraph('可检索最新相关数据', cell), Paragraph('2026-08-09（已超出24h窗口，不计入）', cell)],
    [Paragraph('关键词命中（窗口内）', cell), Paragraph('无', cell)],
    [Paragraph('去重后有效条目', cell), Paragraph('0', cell)],
]
check_tbl = Table(rows, colWidths=[5*cm, 9.5*cm])
check_tbl.setStyle(TableStyle([
    ('FONT', (0,0), (-1,-1), FONT, 9),
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1F3864')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#B4C6E7')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F2F5FB')]),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(check_tbl)
story.append(Spacer(1, 0.25*cm))
story.append(Paragraph('注：两官方站点在 2026-08-11、2026-08-12 凌晨时段（本期统计窗口）均无新的勘察检测类公告入库；最近一次可检索的相关动态停留在 2026-08-09。', small))

story.append(Paragraph('三、数据来源与抓取方法', h1))
story.append(Paragraph('1. 中国招标投标公共服务平台：官方公告为 JavaScript 动态渲染页面，系统通过其公开聚合索引与"今日发布"计数核查；直连列表页在本环境下无法完整抓取。', body))
story.append(Paragraph('2. 海南省政府采购网：列表接口（cgw_list.jsp）支持 begindate/enddate 时间筛选；本环境下对该域名直接抓取连接受限，系统通过其公开搜索索引核查。', body))
story.append(Paragraph('3. 关键词：勘察、检测、测绘、岩土、地质灾害；并做去重与"真实勘察类项目"语义识别（排除仅含"勘察"字样但实质无关的标题）。', body))
story.append(Paragraph('4. 时间筛选：严格限定发布时间在最近24小时内，过滤所有窗口外旧数据。', body))

story.append(Paragraph('四、窗口外近期参考动态（非24h内，仅供参考）', h1))
story.append(Paragraph('以下为近期（窗口外）海南省内与勘察/检测相关的公开动态，<b>不属于本期24小时统计窗口</b>，仅供持续关注：', body))
ref_rows = [
    [Paragraph('项目名称/动态', cellh), Paragraph('类型', cellh), Paragraph('地区/采购人', cellh), Paragraph('发布日期', cellh), Paragraph('来源', cellh)],
    [Paragraph('琼海市2026年城镇老旧小区及周边配套基础设施改造项目勘察(含物探)', cell),
     Paragraph('招标公告', cell), Paragraph('琼海市 / 琼海市住房保障和房产服务中心', cell),
     Paragraph('2026-07-28', cell), Paragraph('中国招标投标公共服务平台(聚合)', cell)],
    [Paragraph('海南高速旗下海南路桥工程检测有限公司中标2026—2027年桥涵检测辅助服务项目', cell),
     Paragraph('中标动态', cell), Paragraph('海南省 / 海南高速', cell),
     Paragraph('2026-08-04', cell), Paragraph('公开新闻', cell)],
    [Paragraph('有限物装海南采办部2026年度二批次采办计划(05-勘探)，要求海洋工程勘察甲级', cell),
     Paragraph('采购意向', cell), Paragraph('海口市 / 有限物装海南采办部', cell),
     Paragraph('2026-07-28', cell), Paragraph('招标预告聚合', cell)],
]
ref_tbl = Table(ref_rows, colWidths=[5.0*cm, 1.6*cm, 3.0*cm, 1.6*cm, 2.3*cm])
ref_tbl.setStyle(TableStyle([
    ('FONT', (0,0), (-1,-1), FONT, 8),
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E5496')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#B4C6E7')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F2F5FB')]),
    ('LEFTPADDING', (0,0), (-1,-1), 3),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
story.append(ref_tbl)
story.append(Paragraph('提示：上述动态日期均早于本期24小时窗口，且部分为中标/意向类信息，不代表当前可投项目。', small))

story.append(Paragraph('五、风险提示与应对建议', h1))
story.append(Paragraph('⚠ 窗口内无新标讯：本期无任何符合关键词的新公告，企业无需紧急响应投标。', body))
story.append(Paragraph('⚠ 数据可得性风险：两官方站点存在 JS 动态渲染 / 直连受限情况，部分新公告可能未被聚合索引及时收录；建议以官方平台实时页面为最终依据。', body))
story.append(Paragraph('✅ 建议：保持每日定时监测；关注工作日早间（约 08:30–10:00）新发布高峰；如希望扩大覆盖面，可将统计窗口放宽至"近3日/近7日"重新生成日报。', body))

story.append(Paragraph('六、附录：字段与口径说明', h1))
story.append(Paragraph('• 统计窗口：以任务触发时刻（2026-08-12 03:00，Asia/Shanghai）前推24小时。<br/>'
                       '• 关键词口径：标题或正文含"勘察/检测/测绘/岩土/地质灾害"之一即纳入候选，再经语义识别排除无关项。<br/>'
                       '• 去重：跨平台同项目合并为一条。<br/>'
                       '• 本报告为系统自动生成，仅供信息参考，不构成投标或法律意见；最终以官方发布平台为准。', body))

doc.build(story, onFirstPage=footer, onLaterPages=footer)

with open(OUT, 'rb') as f:
    data = f.read()
b64 = base64.b64encode(data).decode('ascii')
with open('/Users/fasimac/.qclaw/workspace/海南勘察招标日报_2026-08-12.b64.txt', 'w') as f:
    f.write(b64)
print('PDF_BYTES', len(data))
print('B64_LEN', len(b64))
print(b64)
