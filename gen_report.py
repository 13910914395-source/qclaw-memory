# -*- coding: utf-8 -*-
"""生成【海南勘察招标日报】2026-09-10 (WPS兼容 PDF)"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import datetime

# 注册 WPS/Adobe 兼容的中文字体（内置 CID 字体，无需外部字体文件）
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

CN = 'STSong-Light'

styles = getSampleStyleSheet()
def S(name, **kw):
    base = kw.pop('parent', styles['Normal'])
    return ParagraphStyle(name, parent=base, fontName=CN, **kw)

title_style   = S('TitleX', parent=styles['Title'], fontSize=26, leading=32, textColor=colors.HexColor('#0B3D91'), alignment=TA_CENTER)
sub_style     = S('SubX', fontSize=13, leading=18, textColor=colors.HexColor('#444444'), alignment=TA_CENTER)
h1_style      = S('H1X', fontSize=15, leading=20, textColor=colors.HexColor('#0B3D91'), spaceBefore=10, spaceAfter=6)
h2_style      = S('H2X', fontSize=12, leading=16, textColor=colors.HexColor('#1F5FB0'), spaceBefore=8, spaceAfter=4)
body_style    = S('BodyX', fontSize=9.5, leading=15, alignment=TA_JUSTIFY, spaceAfter=4)
small_style   = S('SmallX', fontSize=8, leading=11, textColor=colors.HexColor('#555555'))
cell_style    = S('CellX', fontSize=7.5, leading=10)
cell_b_style  = S('CellBX', fontSize=7.5, leading=10, textColor=colors.white)
note_style    = S('NoteX', fontSize=9, leading=14, textColor=colors.HexColor('#8a1f1f'), alignment=TA_LEFT)
warn_style    = S('WarnX', fontSize=9, leading=14, alignment=TA_LEFT)

REPORT_DATE = '2026-09-10'
GEN_TS = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# ---------- 页脚（自动生成） ----------
def footer(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFont(CN, 7.5)
    canvas_obj.setFillColor(colors.HexColor('#888888'))
    canvas_obj.drawString(2*cm, 1.0*cm, '【海南勘察招标日报】%s  ·  数据来源：中国招标投标公共服务平台 / 海南省政府采购网（及海南公共资源交易中心、省地质局等关联源）' % REPORT_DATE)
    canvas_obj.drawRightString(A4[0]-2*cm, 1.0*cm, '第 %d 页' % doc.page)
    canvas_obj.setStrokeColor(colors.HexColor('#cccccc'))
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(2*cm, 1.35*cm, A4[0]-2*cm, 1.35*cm)
    canvas_obj.restoreState()

def cover_bg(canvas_obj, doc):
    canvas_obj.saveState()
    # 顶部色带
    canvas_obj.setFillColor(colors.HexColor('#0B3D91'))
    canvas_obj.rect(0, A4[1]-3.2*cm, A4[0], 3.2*cm, fill=1, stroke=0)
    canvas_obj.setFillColor(colors.HexColor('#1F5FB0'))
    canvas_obj.rect(0, A4[1]-3.5*cm, A4[0], 0.3*cm, fill=1, stroke=0)
    # 底部色带
    canvas_obj.setFillColor(colors.HexColor('#0B3D91'))
    canvas_obj.rect(0, 0, A4[0], 1.2*cm, fill=1, stroke=0)
    canvas_obj.restoreState()

# ---------- 文档框架 ----------
doc = BaseDocTemplate('/Users/fasimac/.qclaw/workspace/海南勘察招标日报_2026-09-10.pdf',
                      pagesize=A4, leftMargin=2*cm, rightMargin=2*cm,
                      topMargin=2.2*cm, bottomMargin=1.8*cm,
                      title='【海南勘察招标日报】%s' % REPORT_DATE,
                      author='勘察检测行业招标分析')

frame_cover = Frame(2*cm, 1.6*cm, A4[0]-4*cm, A4[1]-5.5*cm, id='cover')
frame_body  = Frame(2*cm, 1.8*cm, A4[0]-4*cm, A4[1]-4.2*cm, id='body')

doc.addPageTemplates([
    PageTemplate(id='Cover', frames=[frame_cover], onPage=cover_bg),
    PageTemplate(id='Body', frames=[frame_body], onPage=footer),
])

story = []

# ===== 封面 =====
story.append(Spacer(1, 3.4*cm))
story.append(Paragraph('【海南勘察招标日报】', title_style))
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph(REPORT_DATE, sub_style))
story.append(Spacer(1, 0.8*cm))
story.append(Paragraph('勘察 · 检测 · 测绘 · 岩土 · 地质灾害 专项招标监测', sub_style))
story.append(Spacer(1, 1.6*cm))

cover_box = Table([
    [Paragraph('本期结论', S('cb', fontSize=11, textColor=colors.white, alignment=TA_CENTER))],
    [Paragraph('近 24 小时内未检索到符合关键词的、真实的勘察/检测/测绘/岩土/地质灾害类新建项目招标公告。', S('cb2', fontSize=11, leading=17, textColor=colors.white, alignment=TA_CENTER))],
], colWidths=[A4[0]-4*cm])
cover_box.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1), colors.HexColor('#0B3D91')),
    ('BACKGROUND',(0,0),(0,0), colors.HexColor('#1F5FB0')),
    ('BOX',(0,0),(-1,-1), 0.5, colors.HexColor('#0B3D91')),
    ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
    ('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),
]))
story.append(cover_box)
story.append(Spacer(1, 1.2*cm))
story.append(Paragraph('生成时间：%s' % GEN_TS, small_style))
story.append(Paragraph('抓取窗口：2026-09-09 03:00 — 2026-09-10 03:00（Asia/Shanghai）', small_style))
story.append(PageBreak())

# 切换到正文模板
from reportlab.platypus import NextPageTemplate
story.insert(0, NextPageTemplate('Body'))
# 重新组织：封面已是第一页，正文从第二页开始
# （BaseDocTemplate 默认使用第一个模板，封面用 Cover；正文用 Body）

# ===== 目录 =====
story.append(Paragraph('目录', h1_style))
toc = [
    '一、执行摘要与核心结论',
    '二、数据来源与抓取说明（含技术限制）',
    '三、近 24 小时关键词命中明细',
    '四、补充参考：近期仍处招标期/临近截止的勘察·检测类项目',
    '五、资质要求要点与风险提示',
    '六、方法说明与免责声明',
]
for t in toc:
    story.append(Paragraph(t, body_style))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('说明：本报告严格按"发布时间最近 24 小时"窗口筛选；窗口内无符合条件的新建公告，故正文以结论说明 + 补充参考为主。', small_style))
story.append(PageBreak())

# ===== 一、执行摘要 =====
story.append(Paragraph('一、执行摘要与核心结论', h1_style))
story.append(Paragraph(
    '根据本次定时任务要求，对<strong>中国招标投标公共服务平台（www.cebpubservice.com）</strong>与'
    '<strong>海南省政府采购网（www.ccgp-hainan.gov.cn，即海南省政府采购智慧云平台）</strong>在 '
    '<strong>2026-09-09 03:00 至 2026-09-10 03:00（Asia/Shanghai）</strong> 窗口内发布的、'
    '含「勘察 / 检测 / 测绘 / 岩土 / 地质灾害」关键词的公告进行抓取、去重与智能识别。', body_style))
story.append(Paragraph(
    '<strong>核心结论：近期无新发布招标信息。</strong>'
    '在严格的 24 小时窗口内，未检索到任何真实的勘察 / 检测 / 测绘 / 岩土 / 地质灾害类新建项目招标公告。'
    '具体判定如下：', body_style))
bullet = S('bul', fontSize=9.5, leading=15, leftIndent=12, spaceAfter=3)
story.append(Paragraph('• 中国招标投标公共服务平台：站点为纯前端 JavaScript 渲染 + 反爬限制，自动化抓取仅能取得导航外壳，所有时间筛选/搜索接口均返回 404/403/空响应，<strong>无法取得可核验的公告数据</strong>；故无法在该平台确认窗口内有/无相关公告。', bullet))
story.append(Paragraph('• 海南省政府采购网：直接访问被反爬/TLS 拦截；经搜索引擎索引回溯，其 2026-09-09 当日发布的采购公告均为设备、医用耗材、食堂设备等，<strong>不含勘察/检测类</strong>。', bullet))
story.append(Paragraph('• 当日（2026-09-09）唯一含「检测」字样的公告为《关于公开遴选海南(昌江)清洁能源高新技术产业园…工程质量检测招标代理单位事宜的公告》，经智能识别属"招标代理遴选"性质，并非真实的勘察/检测服务采购，已按规则排除。', bullet))
story.append(Paragraph(
    '为兼顾行业实用性，本报告第四章将近期（窗口前 1–6 周）发布、<strong>目前仍处招标期或临近截止</strong>的海南勘察/检测/测绘类真实项目作为<strong>补充参考</strong>列出，'
    '其发布时间早于本次 24 小时窗口，仅供业务跟踪，<strong>不代表"24 小时内新发布"</strong>。', body_style))

# ===== 二、数据来源与抓取说明 =====
story.append(Paragraph('二、数据来源与抓取说明（含技术限制）', h1_style))
src = [
    ['来源平台', '状态', '说明'],
    ['中国招标投标公共服务平台\n(cebpubservice.com)', '不可达/无数据', 'JS 渲染 + 反爬；搜索/公示查询接口 404/403；未能取得时间筛选列表。'],
    ['海南省政府采购网\n(ccgp-hainan.gov.cn)', '直连被拦截', '自动化直接抓取失败；借助搜索引擎索引回溯，当日公告不含勘察/检测类。'],
    ['海南公共资源交易中心\n(ggzy.hainan.gov.cn)', '部分可达', '作为 ccgp-hainan 数据承载方，提供多条真实勘察/检测项目详情（用于补充参考）。'],
    ['海南省地质局等关联源', '可达', '提供海洋院钻探、遥感解译等真实采购公告（用于补充参考）。'],
]
t = Table([[Paragraph(c.replace('\n','<br/>') if isinstance(c,str) else c, cell_style if i>0 else S('th',fontSize=8,leading=10,textColor=colors.white)) for c in row] for i,row in enumerate(src)],
          colWidths=[4.2*cm, 2.6*cm, 8.0*cm])
t.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), colors.HexColor('#0B3D91')),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#EEF3FB')]),
    ('GRID',(0,0),(-1,-1),0.4, colors.HexColor('#bbbbbb')),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
]))
story.append(t)

# ===== 三、近24h命中明细 =====
story.append(Paragraph('三、近 24 小时关键词命中明细', h1_style))
story.append(Paragraph('下表为对 24 小时窗口内公告的逐项核查结果（均为"无符合条件项"）：', body_style))
hit = [
    ['检索关键词', '窗口内新发布数', '真实勘察类项目数', '判定'],
    ['勘察', '0（CEB不可达；海南当日无）', '0', '无'],
    ['检测', '1（昌江·代理遴选，已排除）', '0', '无'],
    ['测绘', '0', '0', '无'],
    ['岩土', '0', '0', '无'],
    ['地质灾害', '0', '0', '无'],
]
t2 = Table([[Paragraph(c, cell_style if i>0 else S('th2',fontSize=8,leading=10,textColor=colors.white)) for c in row] for i,row in enumerate(hit)],
           colWidths=[3.0*cm, 6.0*cm, 3.0*cm, 2.8*cm])
t2.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), colors.HexColor('#0B3D91')),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#EEF3FB')]),
    ('GRID',(0,0),(-1,-1),0.4, colors.HexColor('#bbbbbb')),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
]))
story.append(t2)
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph('▶ 结论重申：<strong>近期无新发布招标信息</strong>（指窗口内真实的勘察/检测/测绘/岩土/地质灾害类新建项目）。', note_style))

# ===== 四、补充参考 =====
story.append(PageBreak())
story.append(Paragraph('四、补充参考：近期仍处招标期/临近截止的勘察·检测类项目', h1_style))
story.append(Paragraph('以下为窗口前发布、目前仍可跟进的真实项目（发布时间早于 24 小时窗口，仅供业务参考，<strong>非 24 小时内新发布</strong>）。已按"真实勘察/检测/测绘类"智能筛选，剔除纯代理遴选、无关采购。', small_style))

proj = [
    # 名称, 类别, 预算(元), 采购人/招标人, 截止, 发布, 资质要点, 链接
    ['儋州市王五片区综合能源项目(勘察)', '工程勘察', '摘要未披露', '儋州市（机器管招投标）', '2026-09-11 08:30', '2026-08-21',
     '工程勘察资质；海南省建筑企业诚信档案手册；信用中国无失信记录', 'https://ggzy.hainan.gov.cn/ggzy/ggzy/jgzbgg/290457.jhtml'],
    ['华南师范大学附属海口学校(勘察)', '工程勘察', '摘要未披露', '海口市（机器管招投标）', '2026-09-22 09:00', '2026-08-31',
     '工程勘察资质；海南省建筑企业诚信档案手册', 'https://ggzy.haikou.gov.cn/gonggao/94940'],
    ['海南省东方市墩头湾海域钻探技术服务', '钻探/海域勘察', '摘要未披露', '海南省海洋地质调查院', '2026-09-11 09:00', '2026-09-07',
     '独立法人资格；履约设备与专业技术能力；接受邮件报名', 'https://geo.hainan.gov.cn/sdzj/0400/202609/902e6c9778e24c3894d7963f4ffb4c72.shtml'],
    ['海南岛**海域微细粒砂矿综合回收技术优化服务(第三次)', '海洋地质技术服务', '摘要未披露', '海南省海洋地质调查院', '2026-09-17 09:00', '2026-09-03',
     '独立法人；无环保类行政处罚；不接受联合体', 'https://geo.hainan.gov.cn/sdzj/0400/202609/f8f8f5e6da444c8389a0454bf6884570.shtml'],
    ['崖州湾实验室高效耦合育种支撑项目地基处理桩基检测服务', '桩基检测', '1,554,500.00', '三亚崖州湾科技城开发建设有限公司', '2026-09-21 15:30', '2026-08-31',
     '建设工程质量检测机构资质（含地基基础工程检测）+ CMA；项目负责人须注册土木工程师(岩土)', 'https://ggzy.hainan.gov.cn/ggzy/syggzy/QTCGZBGS/291016.jhtml'],
    ['海南热带雨林国家公园生态资源综合调查监测项目(三次)', '生态监测', '2,844,800.00', '海南热带雨林国家公园（省林业局）', '2026-09-29 08:30', '2026-09-07',
     '无环保类行政处罚记录声明；须先在海南政府采购智慧云平台下载招标文件', 'https://www.ccgp.gov.cn/cggg/dfgg/gkzb/202609/t20260907_27275955.htm'],
    ['遥感地物解译与水深底质反演技术服务', '测绘/遥感解译', '摘要未披露', '海南省海洋地质调查院', '2026-09-10 09:00', '2026-08-27',
     '独立法人；财务报表/纳税/社保证明；无环保处罚', 'https://geo.hainan.gov.cn/sdzj/0400/202608/41957fab11b749d59ea9dadfbc70921d.shtml'],
    ['2026年重点工业产品检验检测设备更新项目', '检验检测设备采购', '40,830,000.00', '海南省检验检测研究院', '2026-09-21 08:30', '2026-08-31',
     '检验检测设备（非勘察服务）；须平台下载招标文件', 'https://www.ccgp.gov.cn/cggg/dfgg/gkzb/202608/t20260831_27234718.htm'],
    ['海上风电示范项目跟踪监测及环境保护验收…监测技术服务', '环境/生态监测', '1,750,000.00', '自然资源部海口海洋中心', '2026-09-09 08:30（已截止）', '2026-08-19/25',
     '专门面向小微企业；独立法人+履约能力承诺', 'https://ggzy.hainan.gov.cn/ggzy/ggzy/cggg/290282.jhtml'],
]

# 主表（不含资质长文本，避免过宽）
head = ['序号','项目名称','类别','预算(元)','采购人/招标人','投标截止','发布时间','原文链接']
rows = [[Paragraph(h, S('th3',fontSize=7.5,leading=9,textColor=colors.white)) for h in head]]
for i, p in enumerate(proj, 1):
    name, cat, budget, buyer, dl, pub, qual, link = p
    rows.append([
        Paragraph(str(i), cell_style),
        Paragraph(name, cell_style),
        Paragraph(cat, cell_style),
        Paragraph(budget, cell_style),
        Paragraph(buyer, cell_style),
        Paragraph(dl, cell_style),
        Paragraph(pub, cell_style),
        Paragraph('<a href="%s">链接</a>' % link, cell_style),
    ])
mt = Table(rows, colWidths=[0.9*cm, 4.3*cm, 1.9*cm, 2.0*cm, 2.6*cm, 2.0*cm, 1.5*cm, 1.4*cm], repeatRows=1)
mt.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), colors.HexColor('#0B3D91')),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#EEF3FB')]),
    ('GRID',(0,0),(-1,-1),0.4, colors.HexColor('#bbbbbb')),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),
]))
story.append(mt)
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('※ "预算(元)"标注"摘要未披露"者，表示公开摘要页未列明具体金额；"已截止"表示投标截止日早于本报告生成时间，仅作历史跟踪。', small_style))

# 资质要点摘要
story.append(Paragraph('关键资质要求摘要（按项目）', h2_style))
for i, p in enumerate(proj, 1):
    name, cat, budget, buyer, dl, pub, qual, link = p
    story.append(Paragraph('%d. %s — %s' % (i, name, qual), S('q', fontSize=8.5, leading=12, leftIndent=8, spaceAfter=2)))

# ===== 五、风险提示 =====
story.append(Paragraph('五、资质要求要点与风险提示', h1_style))
risks = [
    '资质门槛高：桩基检测、地基处理类项目普遍要求"建设工程质量检测机构资质 + CMA 认定"，且项目负责人须具备注册土木工程师(岩土)执业资格；投标前务必核验证书有效期与人员社保。',
    '截止时间集中：本期补充参考中，墩头湾海域钻探(09-11)、王五片区勘察(09-11)、遥感解译(09-10)等截止日临近，需立即确认报名/投标文件状态。',
    '平台切换风险：海南省政府采购网"旧网站"已停用，须统一使用"海南省政府采购智慧云平台(ccgp-hainan.gov.cn)"下载招标文件，否则投标将被拒绝。',
    '小微企业定向：部分监测类项目（如海上风电跟踪监测）专门面向小微企业，非小微企业不得参与。',
    '数据完整性提示：因 CEB 平台与 ccgp-hainan 直连不可达，本报告无法 100% 覆盖全部官方发布渠道；建议以各平台官网实时核验为准。',
]
for r in risks:
    story.append(Paragraph('• ' + r, S('rk', fontSize=9, leading=14, leftIndent=10, spaceAfter=3)))

# ===== 六、免责声明 =====
story.append(Paragraph('六、方法说明与免责声明', h1_style))
story.append(Paragraph(
    '本报告由自动化招标分析流程生成，数据来源于公开网站及其搜索引擎索引回溯。因目标站点存在 JavaScript 动态渲染与反爬机制，'
    '自动化抓取存在覆盖盲区；24 小时窗口判定以 Asia/Shanghai 时区为准。报告中的项目金额、资质与截止时间均引自公告公开摘要，'
    '最终以官方发布的招标文件为准。本报告仅供行业跟踪参考，不构成投标或法律建议。', small_style))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph('— 报告结束 —', S('end', fontSize=9, alignment=TA_CENTER, textColor=colors.HexColor('#888888'))))

doc.build(story)
print('PDF generated OK')
