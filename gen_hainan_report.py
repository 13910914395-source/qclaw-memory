# -*- coding: utf-8 -*-
"""Generate 【海南勘察招标日报】2026-08-24 PDF (WPS-compatible, reportlab)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, NextPageTemplate)
from reportlab.platypus.tableofcontents import TableOfContents

pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
CN = 'STSong-Light'

# ---------- styles ----------
def S(name, **kw):
    kw.setdefault('fontName', CN)
    return ParagraphStyle(name, **kw)

title_style   = S('CoverTitle', fontSize=26, leading=32, alignment=TA_CENTER, textColor=colors.HexColor('#1F4E79'))
sub_style     = S('CoverSub', fontSize=13, leading=18, alignment=TA_CENTER, textColor=colors.HexColor('#444444'))
h1_style      = S('H1', fontSize=15, leading=20, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor('#1F4E79'))
h2_style      = S('H2', fontSize=12, leading=16, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor('#2E5C8A'))
body_style    = S('Body', fontSize=9.5, leading=14, spaceAfter=4)
small_style   = S('Small', fontSize=8, leading=11, textColor=colors.HexColor('#666666'))
cell_style    = S('Cell', fontSize=7.6, leading=10)
cellb_style   = S('CellB', fontSize=7.6, leading=10, textColor=colors.white)
note_style    = S('Note', fontSize=9, leading=13, textColor=colors.HexColor('#8a1f1f'))

def esc(t):
    return (str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))

# ---------- data ----------
WINDOW = "2026-08-23 03:00 ~ 2026-08-24 03:00（北京时间，近24小时）"

national_24h = [
    (1, "银川市生活垃圾综合处理站建设项目勘察设计中标结果公告", "宁夏", "房屋建筑", "宁夏公共资源交易平台", "2026-08-23", "勘察"),
    (2, "于洪区光辉街道中部片区农村基础设施建设项目勘察及设计（成交公告）", "辽宁", "商业服务", "发布工具", "2026-08-23", "勘察"),
    (3, "于洪区马三家街道三十家村等农村基础设施建设项目勘察及设计（成交公告）", "辽宁", "商业服务", "发布工具", "2026-08-23", "勘察"),
    (4, "明港路（华东路-港建路）改建工程勘察（含测量）服务项目竞争性磋商公告", "上海", "市政", "发布工具", "2026-08-23", "勘察/测绘"),
    (5, "华能河南分公司清能公司龙安区风电项目勘察设计服务预招标", "河南", "能源电力", "中国华能电子招投标系统", "2026-08-23", "勘察"),
    (6, "东营高铁片区综合开发基础设施配套项目（一期）部分单项工程勘察中标候选人公示", "山东", "房屋建筑", "阳光采购服务平台", "2026-08-24", "勘察"),
    (7, "鄂州市南浦虹桥竣工质量检测项目竞争性磋商公告", "湖北", "市政", "发布工具", "2026-08-23", "检测"),
    (8, "双柏县省级茯苓种业基地建设项目检测服务成交候选人公示", "云南", "房屋建筑", "楚雄州国企招采管理平台", "2026-08-23", "检测"),
    (9, "中国电信山东分公司2026年IDCISP系统网安模块检测技术服务项目询比终止公告", "山东", "其他", "中国电信阳光采购网", "2026-08-23", "检测"),
    (10, "中国铁路北京局集团有限公司石家庄站电气线路检测项目招标公告", "河北", "铁路", "发布工具", "2026-08-23", "检测"),
    (11, "中国铁路北京局集团有限公司石家庄站高铁中间站电气线路检测项目招标公告", "河北", "铁路", "发布工具", "2026-08-23", "检测"),
    (12, "中国电信股份有限公司无锡分公司2026年城域算网新技术应用及运载能力检测服务项目", "江苏", "其他", "中国电信阳光采购网", "2026-08-23", "检测"),
    (13, "中央储备粮济宁直属库有限公司梁山粮食仓储项目沉降观测及竣工测绘项目询比公告", "山东", "房屋建筑", "诚E招电子采购交易平台", "2026-08-23", "测绘"),
    (14, "中央储备粮济宁直属库有限公司梁山粮食仓储项目沉降观测及竣工测绘失败公告", "山东", "房屋建筑", "诚E招电子采购交易平台", "2026-08-23", "测绘"),
]

# 海南省近期相关项目回顾（非本24h窗口，供跟踪）；status: 今日截止/进行中/已截止
hainan_recent = [
    ("海洋院 海南岛周边海域矿产资源调查评价(2026年度)项目无人智能勘查技术应用服务（二次）", "2026-08-11", "详见原文", "2026-08-24 09:00", "今日截止", "勘查/勘察", "https://geo.hainan.gov.cn/sdzj/0400/202608/510937a933f246c39ff2397b50fbd59d.shtml"),
    ("海口市2026年度渔业船舶检验社会化服务项目（二次）", "2026-08-12", "10.00万元", "2026-08-24 09:00", "今日截止", "检验", "https://ggzy.haikou.gov.cn/gonggao/94588"),
    ("乐东港深海开发服务保障和防波堤配套工程（勘察设计服务）", "2026-08-18", "详见原文", "2026-09-08 08:30", "进行中", "勘察", "https://ggzy.hainan.gov.cn/ggzy/ldggzy/GGjxzbgs1/290171.jhtml"),
    ("海南省疾病预防控制中心异地新建附属配套（二期）项目方案设计及可研编制", "2026-08-13", "133.00万元", "2026-09-03 08:30", "进行中", "设计(勘察类)", "https://www.ccgp.gov.cn/cggg/dfgg/gkzb/202608/t20260813_27127312.htm"),
    ("金城·金秀城市更新项目(东区)5栋住宅楼加装电梯基础部位地质详细勘察", "2026-08-11", "5.38万元(控制价)", "2026-08-14", "已截止", "岩土/勘察", "https://www.hncq.cn/index.php?a=show&catid=107&id=5706"),
    ("海南空管分局停车棚重建工程及博鳌雷达站土建维修工程设计服务", "2026-08-11", "6.60万元", "2026-08-19", "已截止", "设计", "https://www.gmgitc.com/Bid/BidInfoDetail.aspx?SNID=92415"),
    ("澄迈县和美乡村建设项目工程勘察单位公开遴选", "2026-08-03", "72.00万元(限价)", "2026-08-06", "已截止", "勘察", "https://chengmai.hainan.gov.cn/cmnyj/gsgg/202608/97e725ab242f403a9c59f28edc947878.shtml"),
]

risks = [
    "【今日截止】海洋院“无人智能勘查技术应用服务（二次）”与“海口市渔业船舶检验社会化服务（二次）”均于 2026-08-24 09:00 截标，请立即确认投标/响应状态，避免错失。",
    "【数据源限制】海南省政府采购网（ccgp-hainan.gov.cn）在本次运行环境无法直接访问（SSRF/抓取限制），海南新发布数据可能漏抓；建议人工复核该站及海南省公共资源交易服务中心（ggzy.hainan.gov.cn）。",
    "【资质要点】检测类普遍要求 CMA（检验检测机构资质认定）且在有效期内；测绘类要求 乙级及以上测绘资质（工程测量）；勘察设计类要求相应工程勘察/设计资质；地质灾害类要求 地质灾害评估和治理工程勘查设计资质（甲级/乙级）。",
    "【区域机会】近24h全国勘察检测类新发共 14 条，集中在 市政 / 能源电力 / 铁路 / 房建；海南本地本窗口无新发，可重点跟踪在进行项目（乐东港勘察设计、省疾控方案设计）。",
    "【搜索口径说明】国家级平台为全文/模糊检索，已按“标题含完整关键词”严格去噪；岩土、地质灾害两词在近24h国家级平台无标题命中，故未列入主表。",
]

# ---------- doc with TOC ----------
class MyDoc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            sn = flowable.style.name
            if sn in ('H1', 'H2'):
                lvl = 0 if sn == 'H1' else 1
                self.notify('TOCEntry', (lvl, flowable.getPlainText(), self.page))

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(CN, 8)
    canvas.setFillColor(colors.HexColor('#888888'))
    canvas.drawString(20*mm, 12*mm, "【海南勘察招标日报】2026-08-24")
    canvas.drawRightString(190*mm, 12*mm, "第 %d 页" % doc.page)
    canvas.setStrokeColor(colors.HexColor('#cccccc'))
    canvas.line(20*mm, 15*mm, 190*mm, 15*mm)
    canvas.restoreState()

doc = MyDoc("/Users/fasimac/.qclaw/workspace/海南勘察招标日报_2026-08-24.pdf", pagesize=A4,
            leftMargin=20*mm, rightMargin=20*mm, topMargin=18*mm, bottomMargin=20*mm,
            title="海南勘察招标日报 2026-08-24", author="勘察检测招标分析师")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='main')
doc.addPageTemplates([PageTemplate(id='all', frames=[frame], onPage=footer)])

story = []

# ----- COVER -----
story.append(Spacer(1, 40*mm))
story.append(Paragraph("海南勘察招标日报", title_style))
story.append(Spacer(1, 6*mm))
story.append(Paragraph("2026-08-24", sub_style))
story.append(Spacer(1, 3*mm))
story.append(Paragraph("勘察 · 检测 · 测绘 · 岩土 · 地质灾害 行业招标动态", sub_style))
story.append(Spacer(1, 18*mm))

cover_stats = [
    ["数据窗口", WINDOW],
    ["全国近24h新发（真实勘察类）", "14 条"],
    ["海南省本级近24h新发", "0 条（站点不可直连 + 检索核对无新发）"],
    ["今日（08-24）截止项目", "2 项（风险提示）"],
    ["数据来源", "中国招标投标公共服务平台；海南省政府采购网（不可直连，已注明）"],
]
t = Table(cover_stats, colWidths=[55*mm, 105*mm])
t.setStyle(TableStyle([
    ('FONTNAME', (0,0), (-1,-1), CN),
    ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#1F4E79')),
    ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#EAF1F8')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BBD0E5')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(t)
story.append(Spacer(1, 14*mm))
story.append(Paragraph("说明：本报告由勘察检测行业招标分析师自动生成。海南省政府采购网在本次运行环境无法直接访问，海南相关数据经国家级聚合平台与公开检索交叉核对；凡未直接抓取处均已标注。", small_style))
story.append(PageBreak())

# ----- TOC -----
story.append(Paragraph("目录", h1_style))
toc = TableOfContents()
toc.levelStyles = [S('TOC1', fontSize=11, leading=18), S('TOC2', fontSize=9.5, leading=15, leftIndent=12)]
story.append(toc)
story.append(PageBreak())

# ----- 1. 数据概览 -----
story.append(Paragraph("一、数据概览与采集说明", h1_style))
story.append(Paragraph(
    "本次日报采集窗口为 <b>%s</b>。抓取目标为两大来源：① 中国招标投标公共服务平台"
    "（www.cebpubservice.com，国家级公告聚合，含海南公告）；② 海南省政府采购网"
    "（www.ccgp-hainan.gov.cn）。关键词集合：勘察 / 检测 / 测绘 / 岩土 / 地质灾害。" % esc(WINDOW), body_style))
story.append(Paragraph(
    "<b>采集结果：</b>来源①可正常访问，已使用网站“发布时间”筛选（startcheckDate/endcheckDate）"
    "限定近24小时，并对模糊全文检索结果按“标题含完整关键词”做严格去噪与去重。"
    "来源②在本次运行环境受 SSRF / 抓取限制<b>无法直接访问</b>，故未能直接抓取该站近24h列表；"
    "其海南相关数据通过国家级聚合平台（按【海南】地区标签核对）与公开检索交叉验证。", body_style))
story.append(Paragraph(
    "<b>核心结论：</b>近24小时内，全国勘察检测类真实招标/公示公告共 <b>14 条</b>；"
    "其中<b>海南省（省本级及市县）新发布公告 0 条</b>。详见下文。", body_style))

# ----- 2. 全国近24h主表 -----
story.append(Paragraph("二、近24小时全国勘察检测类招标公告（真实项目，已去重/过滤）", h1_style))
story.append(Paragraph("说明：仅保留标题含完整关键词的真实勘察/检测/测绘类项目；“岩土”“地质灾害”两词近24h在国家级平台无标题命中，未列入。", small_style))
story.append(Spacer(1, 3))
header = ["#", "项目名称", "地区", "行业", "来源渠道", "发布时间", "关键词"]
rows = [[Paragraph(esc(h), cellb_style) for h in header]]
for r in national_24h:
    rows.append([Paragraph(str(r[0]), cell_style), Paragraph(esc(r[1]), cell_style),
                 Paragraph(esc(r[2]), cell_style), Paragraph(esc(r[3]), cell_style),
                 Paragraph(esc(r[4]), cell_style), Paragraph(esc(r[5]), cell_style),
                 Paragraph(esc(r[6]), cell_style)])
tbl = Table(rows, colWidths=[7*mm, 58*mm, 12*mm, 16*mm, 38*mm, 19*mm, 16*mm], repeatRows=1)
tbl.setStyle(TableStyle([
    ('FONTNAME', (0,0), (-1,-1), CN),
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1F4E79')),
    ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#AAAAAA')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F2F6FB')]),
    ('LEFTPADDING', (0,0), (-1,-1), 3),
    ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
story.append(tbl)
story.append(Spacer(1, 3))
story.append(Paragraph("原文入口（按关键词检索）：http://bulletin.cebpubservice.com/xxfbcmses/search/bulletin.html?word=KEYWORD&startcheckDate=2026-08-23&endcheckDate=2026-08-24&dates=1", small_style))

# ----- 3. 海南专区 -----
story.append(Paragraph("三、海南省专区", h1_style))
story.append(Paragraph(
    "<b>近24小时新发布：0 条。</b>经国家级聚合平台（【海南】地区标签）与公开检索交叉核对，"
    "2026-08-23 至 2026-08-24 03:00 海南省无勘察/检测/测绘/岩土/地质灾害类招标公告新发布。"
    "以下为<b>近期（2026年8月）海南省相关项目回顾</b>，供持续跟踪；其中 2 项于今日（08-24）截止，已列入风险提示。", body_style))
story.append(Spacer(1, 3))
hheader = ["项目名称", "发布时间", "预算/控制价", "截止时间", "状态", "关键词"]
hrows = [[Paragraph(esc(h), cellb_style) for h in hheader]]
for r in hainan_recent:
    hrows.append([Paragraph(esc(r[0]), cell_style), Paragraph(esc(r[1]), cell_style),
                  Paragraph(esc(r[2]), cell_style), Paragraph(esc(r[3]), cell_style),
                  Paragraph(esc(r[4]), cell_style), Paragraph(esc(r[5]), cell_style)])
htbl = Table(hrows, colWidths=[62*mm, 20*mm, 24*mm, 26*mm, 16*mm, 20*mm], repeatRows=1)
htbl.setStyle(TableStyle([
    ('FONTNAME', (0,0), (-1,-1), CN),
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E5C8A')),
    ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#AAAAAA')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F2F6FB')]),
    ('LEFTPADDING', (0,0), (-1,-1), 3),
    ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
story.append(htbl)
story.append(Spacer(1, 2))
story.append(Paragraph("典型原文链接：海洋院勘查 http://geo.hainan.gov.cn/sdzj/0400/202608/510937a933f246c39ff2397b50fbd59d.shtml ；乐东港勘察设计 https://ggzy.hainan.gov.cn/ggzy/ldggzy/GGjxzbgs1/290171.jhtml", small_style))

# ----- 4. 风险提示 -----
story.append(Paragraph("四、风险提示与投标建议", h1_style))
for i, rk in enumerate(risks, 1):
    story.append(Paragraph("%d. %s" % (i, esc(rk)), body_style))

story.append(Spacer(1, 6))
story.append(Paragraph(
    "免责声明：本报告基于公开渠道自动采集，可能存在延迟、漏抓或解析误差；海南省政府采购网未直接抓取，"
    "相关结论以公开检索交叉核对为准。投标决策请以官方原文及采购文件为准。", small_style))

doc.multiBuild(story)
print("PDF generated OK")
