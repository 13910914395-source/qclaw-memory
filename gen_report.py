# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# Use built-in Adobe CJK font (no embedding needed, WPS-compatible)
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
FONT = 'STSong-Light'

styles = getSampleStyleSheet()
def S(name, **kw):
    base = dict(fontName=FONT, wordWrap='CJK')
    base.update(kw)
    return ParagraphStyle(name, **base)

title_style   = S('Title', fontSize=22, leading=30, alignment=TA_CENTER, spaceAfter=10)
sub_style     = S('Sub',   fontSize=12, leading=18, alignment=TA_CENTER, textColor=colors.HexColor('#444444'))
h1_style      = S('H1', fontSize=15, leading=22, spaceBefore=14, spaceAfter=6, textColor=colors.HexColor('#1a3c7a'))
h2_style      = S('H2', fontSize=12, leading=18, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor('#1a3c7a'))
body_style    = S('Body', fontSize=10, leading=16, alignment=TA_LEFT, spaceAfter=4)
small_style   = S('Small', fontSize=8.5, leading=13)
cell_style    = S('Cell', fontSize=8.5, leading=12)
cell_h_style  = S('CellH', fontSize=8.5, leading=12, textColor=colors.white)
cell_b_style  = S('CellB', fontSize=8.5, leading=12, textColor=colors.HexColor('#b00000'))
warn_style    = S('Warn', fontSize=10, leading=16, textColor=colors.HexColor('#b00000'), spaceAfter=4)

story = []

# ---------- Cover ----------
story.append(Spacer(1, 3.5*cm))
story.append(Paragraph('【海南勘察招标日报】', title_style))
story.append(Paragraph('2026-09-02', title_style))
story.append(Spacer(1, 0.8*cm))
story.append(Paragraph('勘察 / 检测 / 测绘 / 岩土 / 地质灾害 类招标信息日报', sub_style))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('数据窗口：2026-09-01 03:00 ~ 2026-09-02 03:00（最近24小时）', sub_style))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('来源：中国招标投标公共服务平台、海南省政府采购网', sub_style))
story.append(Spacer(1, 1.2*cm))
story.append(HRFlowable(width='60%', color=colors.HexColor('#1a3c7a')))
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('⚠ 近期无新发布招标信息（近24小时内未发现符合条件的新公告）', warn_style))
story.append(PageBreak())

# ---------- 目录 ----------
story.append(Paragraph('目录', h1_style))
story.append(HRFlowable(width='100%', color=colors.HexColor('#cccccc')))
toc = [
    '一、核心结论',
    '二、数据检索方法与限制',
    '三、检索范围与关键词',
    '四、参考附录（真实数据，超出24小时窗口，仅供参考）',
    '    4.1 海南省近期相关公告',
    '    4.2 全国其他省份近期相关公告（非海南，仅供参考）',
    '五、风险提示与建议',
]
for t in toc:
    story.append(Paragraph(t, body_style))
story.append(PageBreak())

# ---------- 一、核心结论 ----------
story.append(Paragraph('一、核心结论', h1_style))
story.append(HRFlowable(width='100%', color=colors.HexColor('#cccccc')))
story.append(Paragraph(
    '根据对 <b>中国招标投标公共服务平台（www.cebpubservice.com / bulletin.cebpubservice.com）</b> '
    '与 <b>海南省政府采购网（www.ccgp-hainan.gov.cn）</b> 在 '
    '<b>2026-09-01 03:00 至 2026-09-02 03:00（最近24小时）</b> 的自动化检索：', body_style))
story.append(Paragraph('⚠ <b>近期无新发布招标信息</b> —— 近24小时内未发现含「勘察 / 检测 / 测绘 / 岩土 / 地质灾害」'
    '关键词的招标（采购）公告。', warn_style))
story.append(Paragraph('本结论基于本报告第三节所列检索方法得出；受目标网站技术限制（详见第二节），'
    '该结论表示"在限定自动化环境下无法确认存在新公告"，建议人工复核官网后再做投标决策。', body_style))

# ---------- 二、检索方法与限制 ----------
story.append(Paragraph('二、数据检索方法与限制', h1_style))
story.append(HRFlowable(width='100%', color=colors.HexColor('#cccccc')))
limits = [
    '1. 两大目标平台的公告列表均为 JavaScript 动态渲染页面；本环境下浏览器自动化受 SSRF 安全策略限制'
    '（仅允许 IP 字面量导航），无法直接渲染页面并应用网站自带的"公告发布时间=今天/2天内"时间筛选功能。',
    '2. 海南省政府采购网主域在自动抓取时返回连接失败（fetch failed），无法直达获取最近24小时公告列表；'
    '其公告详情页同样不可达。',
    '3. 中国招标投标公共服务平台（bulletin.cebpubservice.com）的公告表格由 XHR 异步加载，'
    '服务端渲染内容仅含导航/来源渠道下拉，未暴露可在限定环境获取的服务端 24 小时筛选视图。',
    '4. 作为补充核查，调用搜索引擎索引并按 date_after=2026-08-30 检索：全国范围内最近的相关公告发布于 '
    '2026-08-26 / 2026-08-27（山西临汾、湖北宜昌、甘肃临夏、河北涉县、江苏南京等），均非海南省且超出24小时窗口；'
    '海南省政府采购网索引中最新的同类公告发布于 2026-07-27（南海北部油气资源调查评价），更早项目多集中在 '
    '2026-02 至 2026-05，均不在最近24小时内。',
]
for t in limits:
    story.append(Paragraph(t, body_style))

# ---------- 三、检索范围与关键词 ----------
story.append(Paragraph('三、检索范围与关键词', h1_style))
story.append(HRFlowable(width='100%', color=colors.HexColor('#cccccc')))
story.append(Paragraph('• 平台：中国招标投标公共服务平台、海南省政府采购网', body_style))
story.append(Paragraph('• 关键词：勘察、检测、测绘、岩土、地质灾害', body_style))
story.append(Paragraph('• 时间窗：最近24小时（2026-09-01 03:00 ~ 2026-09-02 03:00， Asia/Shanghai）', body_style))
story.append(Paragraph('• 目标条数：各平台各50条（因无数据，实际命中0条）', body_style))
story.append(Paragraph('• 字段要求：项目名称、预算金额、采购人、关键资质要求、截止日期、发布时间、原文链接', body_style))

# ---------- 四、参考附录 ----------
story.append(PageBreak())
story.append(Paragraph('四、参考附录（真实数据，超出24小时窗口，仅供参考）', h1_style))
story.append(HRFlowable(width='100%', color=colors.HexColor('#cccccc')))
story.append(Paragraph('以下项目为检索过程中发现的真实公告，<b>发布时间均不在最近24小时窗口内</b>，'
    '仅用于研判行业趋势，<b>不得作为24小时内新标讯使用</b>。', warn_style))

story.append(Paragraph('4.1 海南省近期相关公告', h2_style))
hn_data = [
    ['项目名称', '发布时间', '采购人/委托方', '预算', '来源'],
    ['南海北部油气资源调查评价', '2026-07-27', '海南省地震局', '121.00万元', 'ccgp-hainan'],
    ['海南省红树林资源监测与成效评估', '2026-04-16', '海南省野生动植物保护管理局', '368.96万元', 'ccgp-hainan'],
    ['2026年海南省水务工程质量监督检测项目', '2026-04-16', '海南省水务建设质量监督定额局', '详见原文', 'ccgp-hainan'],
    ['三亚市循环经济产业园环境监测(三年)', '2026-04-17', '三亚市住房和城乡建设局', '110.00万元', 'ccgp-hainan'],
    ['海南岛东南部地热带深部勘查(2026年度)', '2026-04-17', '海南省生态环境地质调查院', '159.84万元', 'ccgp-hainan'],
    ['海口市全域耕地土壤重金属污染成因排查', '2026-03-09', '海口市生态环境局', '详见原文', 'ccgp-hainan'],
    ['铺前-清澜断裂南段活动断层精细探测与地震危险性评价', '2026-03-25', '海南省地震局', '700.40万元', 'ccgp-hainan'],
    ['海南省采矿损毁土地状况调查', '2026-03-20', '海南省自然资源和规划厅', '100.00万元', 'ccgp-hainan'],
    ['海南1:5万万宁县等3幅区域地质调查', '2026-05-07', '海南省地质调查院', '147.88万元', 'ccgp-hainan'],
    ['东方市东河镇…地形图测绘与地质工程勘察', '2026-03-27', '东方市自然资源和规划局', '询价', '东方市政府网'],
    ['五指山市畅好乡-水满乡1:1万地灾精细化调查岩矿测试', '2026-05-29', '海南省自然资源和规划厅', '13.16万元', 'lr.hainan.gov.cn'],
    ['琼中等中部山区地灾常态化调查-无人机数字航空摄影', '2026-02-16', '海南省自然资源和规划厅', '41.54万元', 'lr.hainan.gov.cn'],
]
rows = [[Paragraph(c, cell_h_style if i==0 else cell_style) for c in r] for i, r in enumerate(hn_data)]
t1 = Table(rows, colWidths=[5.0*cm, 2.0*cm, 4.2*cm, 2.3*cm, 2.5*cm], repeatRows=1)
t1.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3c7a')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#999999')),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#eef2f9')]),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
story.append(t1)

story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('4.2 全国其他省份近期相关公告（非海南，仅供参考）', h2_style))
nat_data = [
    ['项目名称', '发布时间', '采购人', '预算', '地区'],
    ['临汾经济开发区辖区内地质灾害岩土工程勘察及稳定性分析', '2026-08-26', '临汾经济开发区管委会', '38.85万元', '山西'],
    ['宜昌市重点区域地质灾害专项调查', '2026-08-24', '宜昌市地质环境监测站', '398.00万元', '湖北'],
    ['临夏州2026年度地质灾害防治专业监测预警点建设', '2026-08-27', '临夏州自然资源局', '155.20万元', '甘肃'],
    ['南京市栖霞区汇通路地块山体地灾治理及场地平整勘查设计', '2026-08-26', '栖霞区相关部门', '详见原文(甲级资质)', '江苏'],
    ['重庆市武隆区和顺镇岩边危岩带勘查设计', '2026-08-21', '武隆区', '143.00万元', '重庆'],
]
rows2 = [[Paragraph(c, cell_h_style if i==0 else cell_style) for c in r] for i, r in enumerate(nat_data)]
t2 = Table(rows2, colWidths=[5.6*cm, 2.0*cm, 4.4*cm, 2.6*cm, 1.5*cm], repeatRows=1)
t2.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3c7a')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#999999')),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#eef2f9')]),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
story.append(t2)

# ---------- 五、风险提示 ----------
story.append(PageBreak())
story.append(Paragraph('五、风险提示与建议', h1_style))
story.append(HRFlowable(width='100%', color=colors.HexColor('#cccccc')))
risk = [
    '1. 本报告"无新发布"结论受自动化检索技术限制影响，<b>不代表官网绝对无新公告</b>；'
    '在投标决策前请人工登录两平台，使用网站自带"公告发布时间 = 今天 / 2天内"筛选器复核。',
    '2. 第四节"参考附录"中的所有项目发布时间均<b>超出24小时窗口</b>，严禁当作24小时内新标讯用于投标测算或报备。',
    '3. 目标网站（尤其海南省政府采购网）存在反爬/连接限制，定时自动化抓取稳定性差；'
    '如需稳定获取，建议申请两平台官方数据 API，或配置可渲染 JS 的抓取环境。',
    '4. 资质识别提示：真实勘察/岩土类项目通常要求「工程勘察综合甲级 / 岩土工程（勘察）甲级」、'
    '「注册土木工程师（岩土）」、「地质灾害防治单位甲级/乙级资质」、「测绘乙级及以上」及 CMA 计量认证，'
    '筛选时注意排除仅名称含"勘察"字样的无关项目。',
]
for t in risk:
    story.append(Paragraph(t, body_style))

story.append(Spacer(1, 0.6*cm))
story.append(Paragraph('— 报告结束 · 本日报由自动检索任务生成，数据以官方发布为准 —', small_style))

# ---------- footer ----------
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawString(2*cm, 1.0*cm, '【海南勘察招标日报】2026-09-02')
    canvas.drawRightString(A4[0]-2*cm, 1.0*cm, '第 %d 页' % doc.page)
    canvas.setStrokeColor(colors.HexColor('#cccccc'))
    canvas.line(2*cm, 1.3*cm, A4[0]-2*cm, 1.3*cm)
    canvas.restoreState()

doc = SimpleDocTemplate(
    '/Users/fasimac/.qclaw/workspace/海南勘察招标日报_2026-09-02.pdf',
    pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=1.8*cm,
    title='【海南勘察招标日报】2026-09-02', author='OpenClaw 招标分析')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print('PDF generated.')
