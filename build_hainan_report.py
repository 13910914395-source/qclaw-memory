# -*- coding: utf-8 -*-
"""生成【海南勘察招标日报】PDF（WPS兼容，CJK）。"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# 中文CID字体（WPS/Adobe均支持）
try:
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    FONT = 'STSong-Light'
except Exception:
    FONT = 'Helvetica'

DATE = '2026-09-04'
WINDOW = '2026-09-03 03:00 ~ 2026-09-04 03:00（北京时间/Asia/Shanghai）'

styles = getSampleStyleSheet()
def S(name, **kw):
    base = kw.pop('parent', styles['Normal'])
    return ParagraphStyle(name, parent=base, fontName=FONT, **kw)

title_st   = S('t', fontSize=22, leading=28, alignment=TA_CENTER, spaceAfter=6)
sub_st     = S('sub', fontSize=12, leading=16, alignment=TA_CENTER, textColor=colors.HexColor('#555555'))
cover_meta = S('cm', fontSize=10.5, leading=18, alignment=TA_CENTER, textColor=colors.HexColor('#333333'))
h1_st      = S('h1', fontSize=14.5, leading=20, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor('#1a3c6e'))
h2_st      = S('h2', fontSize=12, leading=16, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor('#1a3c6e'))
body_st    = S('b', fontSize=10, leading=15, alignment=TA_LEFT, spaceAfter=4)
bullet_st  = S('bl', fontSize=10, leading=15, leftIndent=12, bulletIndent=2, spaceAfter=2)
cell_st    = S('c', fontSize=8.2, leading=11)
cell_h_st  = S('ch', fontSize=8.4, leading=11, textColor=colors.white)
note_st    = S('n', fontSize=9, leading=13, textColor=colors.HexColor('#8a1f1f'))

story = []

# ---------- 封面 ----------
story += [Spacer(1, 40*mm)]
story.append(Paragraph('【海南勘察招标日报】', title_st))
story.append(Paragraph(DATE, sub_st))
story.append(Spacer(1, 6*mm))
story.append(HRFlowable(width='60%', thickness=1.2, color=colors.HexColor('#1a3c6e')))
story.append(Spacer(1, 6*mm))
story.append(Paragraph('勘察 · 检测 · 测绘 · 岩土 · 地质灾害 招标信息日报', sub_st))
story.append(Spacer(1, 18*mm))
story.append(Paragraph('数据窗口：' + WINDOW, cover_meta))
story.append(Paragraph('生成时间：2026-09-04 03:00（定时任务自动生成）', cover_meta))
story.append(Paragraph('数据来源：中国招标投标公共服务平台、海南省政府采购网（及海南公共资源交易/各厅局站点聚合）', cover_meta))
story.append(Spacer(1, 14*mm))
story.append(Paragraph('⚠ 核心结论：近期无新发布招标信息（24小时窗口内未发现符合行业域的真实招标公告）', note_st))
story.append(PageBreak())

# ---------- 目录 ----------
story.append(Paragraph('目录', h1_st))
toc = [
    '一、数据来源与筛选方法',
    '二、24小时窗口核心结论',
    '三、窗口外近期参考（近30日，非本次窗口）',
    '四、风险提示与投标建议',
]
for i, t in enumerate(toc, 1):
    story.append(Paragraph(f'{i}. {t}', body_st))
story.append(PageBreak())

# ---------- 一、方法 ----------
story.append(Paragraph('一、数据来源与筛选方法', h1_st))
story.append(Paragraph('1. 抓取目标平台：', h2_st))
story.append(Paragraph('• 中国招标投标公共服务平台（www.cebpubservice.com）', bullet_st))
story.append(Paragraph('• 海南省政府采购网（www.ccgp-hainan.gov.cn，含海南省政府采购智慧云平台）', bullet_st))
story.append(Paragraph('• 辅助核验：海南省公共资源交易服务中心、海南省自然资源和规划厅、海南省住建厅、海南省地质局、海南省交通运输厅等海南本地发布源', bullet_st))
story.append(Paragraph('2. 时间筛选口径：', h2_st))
story.append(Paragraph('严格按"发布时间"落在窗口 ' + WINDOW + ' 内裁剪；仅保留窗口内公告，过滤全部旧数据。', body_st))
story.append(Paragraph('3. 关键词与智能识别：', h2_st))
story.append(Paragraph('命中关键词【勘察 / 检测 / 测绘 / 岩土 / 地质灾害】；并对仅含"勘察"字样但实质无关的项目（如技术优化服务、试剂采购等非工程域）进行排除。', body_st))
story.append(Paragraph('4. 工具局限说明（透明披露）：', h2_st))
story.append(Paragraph('上述两主站均为 JavaScript 动态渲染站点，本自动化环境无法直接套用其站内时间筛选并批量导出 50 条列表。本报告以公开检索结果的"发布时间"字段做时间裁剪与去重，结论基于可验证的发布时间，但极新的未索引条目可能存在遗漏。', body_st))

# ---------- 二、核心结论 ----------
story.append(Paragraph('二、24小时窗口核心结论', h1_st))
story.append(Paragraph('<b>结论：近期无新发布招标信息。</b>', body_st))
story.append(Paragraph('在严格 24 小时窗口（' + WINDOW + '）内，未发现符合"勘察/检测/测绘/岩土/地质灾害"行业域的真实招标公告。', body_st))
story.append(Paragraph('窗口内检索到的邻近条目（均判定为领域外，不计入本期）：', h2_st))
near = [
    ['项目名称', '发布时间', '判定'],
    [Paragraph('海口海关动植物检疫中心 进境食蟹猴检测试剂盒采购项目（比选）', cell_st),
     Paragraph('2026-09-03 21:24', cell_st),
     Paragraph('含"检测"关键词，但属动物检疫试剂采购，<b>非工程勘察/岩土/测绘/地质灾害域</b>', cell_st)],
    [Paragraph('海南省海洋地质调查院 海南岛**海域微细粒砂矿综合回收技术优化服务(第三次)', cell_st),
     Paragraph('2026-09-03 17:58', cell_st),
     Paragraph('不含上述任一关键词，属技术优化服务，<b>已排除</b>', cell_st)],
]
t = Table(near, colWidths=[62*mm, 26*mm, 72*mm])
t.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#1a3c6e')),
    ('TEXTCOLOR',(0,0),(-1,0),colors.white),
    ('FONTNAME',(0,0),(-1,-1),FONT),
    ('FONTSIZE',(0,0),(-1,-1),8.2),
    ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#999999')),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#f2f5fa')]),
]))
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(Paragraph('说明：按要求"若网站没有近期数据，明确告知用户——近期无新发布招标信息"，本期据此如实标注。', note_st))

# ---------- 三、窗口外参考 ----------
story.append(PageBreak())
story.append(Paragraph('三、窗口外近期参考（近30日，非本次窗口）', h1_st))
story.append(Paragraph('以下为海南省近期（2026-08 及以前）发布的真实勘察/检测/测绘/岩土/地质灾害类公告，<b>均不属于本次24小时窗口</b>，列出仅供持续跟踪与商机研判。', body_st))

rows = [
    ['项目名称', '采购人/发布方', '预算', '域', '发布', '截止', '关键资质'],
    ['崖州湾实验室高效耦合育种支撑项目地基处理桩基检测服务', '三亚崖州湾科技城开发建设有限公司(代理:海南政兴源)', '155.45万', '检测', '08-31', '09-21 15:30', 'CMA(地基基础)+注册土木工程师(岩土)'],
    ['万泉河防洪治理(堤防护岸)工程勘察设计', '海南省公共资源交易(机器管招投标)', '未披露(保证金10万)', '勘察', '08-17', '09-07 08:30', '工程勘察/设计资质'],
    ['三亚市角头湾渔港建设项目施工期海域、陆域环境监测技术服务', '三亚现代农业投资有限公司', '76.8万', '检测', '08-18', '09-04 08:30', 'CMA检验检测机构资质认定+检测能力附表'],
    ['儋州市2026年老旧小区改造及配套基础设施建设项目(物探)', '儋州市', '30万', '测绘', '08-22', '09-02 09:30', '物探能力'],
    ['G98环岛高速路面修复养护及边坡滑坡灾害治理工程', '海南省交通运输厅', '未披露', '地质灾害', '08-20', '09-11 09:30', '路基路面养护甲级等'],
    ['2026年房屋建筑、市政工程勘察设计和施工图审查质量检查技术辅助服务(二次)', '海南省住房和城乡建设厅', '22.12万', '勘察', '08-31', '09-04 17:00', '熟悉勘察设计政策'],
    ['2026年计量检定校准设备更新项目', '海南省检验检测研究院', '1184万', '检测', '08-19', '09-09 08:30', '—'],
    ['2026年重点工业产品检验检测设备更新项目', '海南省检验检测研究院', '4083万', '检测', '08-31', '09-21 08:30', '—'],
    ['海洋地质二十六号调查船船载声学设备安装服务', '中国地质调查局海口海洋地质调查中心', '75万', '地质勘测', '08-31', '09-11 09:30', '—'],
    ['海南岛周边海域矿产资源调查评价 无人智能勘查技术应用服务(二次)', '海南省海洋地质调查院', '39.48万', '测绘', '08-11', '—', '多波束/浅剖/ROV设备'],
    ['保亭县BT-2025-32号地块土壤污染状况调查', '保亭县自然资源和规划局', '未披露', '检测', '08-31', '报名09/01-09/03', '省级CMA(土壤、水、废水)'],
    ['2026年房屋市政工程进场材料防火性能抽测服务', '海南省建设工程质量安全监督管理局', '9万', '检测', '08-27', '—', '建设工程质量检测资质+CMA'],
    ['五指山市畅好乡-水满乡1:1万地质灾害精细化调查岩矿测试', '海南省自然资源和规划厅', '13.16万', '地质灾害', '05-29', '—', 'CMA计量认证'],
    ['海口基地港池海底勘察机构遴选', '海南省海洋和渔业监察总队', '未披露', '勘察', '03-17', '—', '测绘资质'],
]
data = [[Paragraph(c, cell_h_st) if i==0 else Paragraph(c, cell_st) for c in r] for i, r in enumerate(rows)]
t = Table(data, colWidths=[40*mm, 33*mm, 16*mm, 13*mm, 12*mm, 20*mm, 34*mm], repeatRows=1)
t.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#1a3c6e')),
    ('FONTNAME',(0,0),(-1,-1),FONT),
    ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#999999')),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#f2f5fa')]),
    ('LEFTPADDING',(0,0),(-1,-1),3),
    ('RIGHTPADDING',(0,0),(-1,-1),3),
    ('TOPPADDING',(0,0),(-1,-1),2),
    ('BOTTOMPADDING',(0,0),(-1,-1),2),
]))
story.append(t)
story.append(Spacer(1, 3*mm))
story.append(Paragraph('注：链接不在此罗列，以各原发布站公告页为准（海南省公共资源交易服务中心 ggzy.hainan.gov.cn、中国政府采购网 ccgp.gov.cn 海南分网、各厅局门户）。', note_st))

# ---------- 四、风险 ----------
story.append(PageBreak())
story.append(Paragraph('四、风险提示与投标建议', h1_st))
story.append(Paragraph('1. 时间窗口效应：', h2_st))
story.append(Paragraph('本期触发时间为凌晨 03:00，属发布低频时段；海南省招标公告多集中于工作日（周一至周五）白天发布。建议于 2026-09-04 上午及 2026-09-07（周一）复查，避免遗漏当日新发公告。', body_st))
story.append(Paragraph('2. 资质合规风险：', h2_st))
story.append(Paragraph('桩基检测、土壤/防火检测类普遍要求 CMA 计量认证 + 建设工程质量检测机构资质，且资质附表参数须覆盖本次采购项目；岩土类要求注册土木工程师(岩土)执业资格。投标前务必核验资质附表与人员在有效期内的注册状态。', body_st))
story.append(Paragraph('3. 政策风险：', h2_st))
story.append(Paragraph('《海南省房屋建筑和市政基础设施工程勘察成果文件、施工图设计文件审查要点(2026年版)》（琼建科〔2026〕164号）自 2026-09-01 起施行，全程线上审查，资质签章有效期、成果完整性由系统层面拦截；将影响后续勘察成果送审与招投标节奏。', body_st))
story.append(Paragraph('4. 数据源风险：', h2_st))
story.append(Paragraph('中国招标投标公共服务平台与海南省政府采购网均为 JS 动态站点，本日报基于公开检索的发布时间字段做时间裁剪，极新条目（发布后数小时内）可能尚未被检索索引。关键项目以原发布站公告正文为准，本报告不构成投标决策唯一依据。', body_st))
story.append(Spacer(1, 4*mm))
story.append(HRFlowable(width='100%', thickness=0.6, color=colors.HexColor('#999999')))
story.append(Paragraph('— 本报告由定时任务自动生成，数据经发布时间筛选与智能去重；如窗口内出现新公告，将于下一周期补报。 —', S('end', fontSize=8.5, leading=12, textColor=colors.HexColor('#777777'), alignment=TA_CENTER)))

# ---------- 页脚（自动页码） ----------
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(colors.HexColor('#888888'))
    canvas.drawString(18*mm, 10*mm, '【海南勘察招标日报】' + DATE)
    canvas.drawRightString(A4[0]-18*mm, 10*mm, '第 %d 页' % doc.page)
    canvas.drawCentredString(A4[0]/2, 10*mm, '数据窗口: 2026-09-03 03:00~09-04 03:00')
    canvas.restoreState()

doc = SimpleDocTemplate('/Users/fasimac/.qclaw/workspace/海南勘察招标日报_2026-09-04.pdf',
                        pagesize=A4, topMargin=18*mm, bottomMargin=16*mm,
                        leftMargin=18*mm, rightMargin=18*mm,
                        title='【海南勘察招标日报】2026-09-04', author='勘察检测行业招标分析')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print('PDF generated.')
