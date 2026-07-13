# -*- coding: utf-8 -*-
"""Generate an HONEST 【海南勘察招标日报】 PDF (WPS-compatible) using reportlab + STSong-Light CJK font."""
import base64, io, datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, HRFlowable)

pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
CJK = 'STSong-Light'

GEN_TIME = "2026-07-10 12:26 (Asia/Shanghai)"
WINDOW = "2026-07-09 12:26 至 2026-07-10 12:26 (Asia/Shanghai)"

styles = getSampleStyleSheet()
def S(name, **kw):
    kw.setdefault('fontName', CJK)
    return ParagraphStyle(name, parent=styles['Normal'], **kw)

cover_title = S('cover_title', fontName=CJK, fontSize=26, leading=32,
               alignment=TA_CENTER, textColor=colors.HexColor('#1F3864'))
cover_sub = S('cover_sub', fontSize=13, leading=20, alignment=TA_CENTER,
              textColor=colors.HexColor('#444444'))
h1 = S('h1', fontSize=15, leading=22, textColor=colors.HexColor('#1F3864'),
       spaceBefore=10, spaceAfter=6)
h2 = S('h2', fontSize=12, leading=18, textColor=colors.HexColor('#2E5496'),
       spaceBefore=8, spaceAfter=4)
body = S('body', fontSize=10.5, leading=17, alignment=TA_LEFT, spaceAfter=5)
small = S('small', fontSize=9, leading=14, textColor=colors.HexColor('#555555'))
cell = S('cell', fontSize=8.5, leading=12)
cellb = S('cellb', fontSize=8.5, leading=12, textColor=colors.HexColor('#B00000'))
note = S('note', fontSize=10, leading=16, textColor=colors.HexColor('#B00000'),
         spaceBefore=4, spaceAfter=6)

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(CJK, 8)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawCentredString(A4[0]/2, 12*mm,
        "海南勘察招标日报 · 生成时间 %s · 第 %d 页" % (GEN_TIME, doc.page))
    canvas.drawCentredString(A4[0]/2, 7*mm,
        "本报告由公开网络检索生成，仅供线索参考，不构成投标或决策依据；数据以官方发布为准。")
    canvas.restoreState()

buf = io.BytesIO()
doc = SimpleDocTemplate(buf, pagesize=A4,
                        leftMargin=20*mm, rightMargin=20*mm,
                        topMargin=18*mm, bottomMargin=20*mm,
                        title="【海南勘察招标日报】2026-07-10",
                        author="勘察检测行业招标分析")
E = []

# ---------- COVER ----------
E.append(Spacer(1, 45*mm))
E.append(Paragraph("【海南勘察招标日报】", cover_title))
E.append(Spacer(1, 6*mm))
E.append(Paragraph("2026-07-10", cover_title))
E.append(Spacer(1, 10*mm))
E.append(Paragraph("勘察 · 检测 · 测绘 · 岩土 · 地质灾害 类招标信息日报", cover_sub))
E.append(Spacer(1, 4*mm))
E.append(Paragraph("数据窗口：%s" % WINDOW, cover_sub))
E.append(Spacer(1, 30*mm))
E.append(HRFlowable(width="60%", color=colors.HexColor('#1F3864')))
E.append(Spacer(1, 4*mm))
E.append(Paragraph("生成时间：%s" % GEN_TIME, cover_sub))
E.append(Paragraph("数据源：中国招标投标公共服务平台 / 海南省政府采购网 / 公开网络聚合检索", cover_sub))
E.append(PageBreak())

# ---------- 目录 ----------
E.append(Paragraph("目录", h1))
toc = [
    "一、报告摘要",
    "二、数据获取说明与局限性",
    "三、时间窗口与筛选方法",
    "四、检索结论",
    "五、参考线索（非24小时窗口，真实检索所得）",
    "六、风险提示与建议",
]
for t in toc:
    E.append(Paragraph(t, body))
E.append(PageBreak())

# ---------- 一、摘要 ----------
E.append(Paragraph("一、报告摘要", h1))
E.append(Paragraph(
    "本日报按既定要求，尝试抓取最近24小时（%s）内发布的、含"
    "「勘察」「检测」「测绘」「岩土」「地质灾害」关键词的招标公告，"
    "目标数据源为中国招标投标公共服务平台（cebpubservice.com）与海南省政府采购网"
    "（ccgp-hainan.gov.cn），并期望各取最新50条。" % WINDOW, body))
E.append(Paragraph(
    "<b>核心结论：在所及检索能力范围内，本次未能从指定官方渠道验证到任何"
    "近24小时内发布的海南地区勘察/检测/测绘/岩土/地质灾害类招标公告。"
    "即：近期无新发布招标信息（在所及检索能力范围内）。</b>", note))
E.append(Paragraph(
    "需要特别说明的是：本报告未生成任何虚构的招标条目。公开网络检索在24小时窗口内"
    "返回的海南相关结果为新闻、天气预警或无关采购（如物品采购、设计服务），"
    "均不属于本报告目标类别；检索到的真实勘察/检测类项目均发布于2026年6月及更早，"
    "已作为“参考线索”列于第五节，并明确标注其不在时间窗内。", body))

# ---------- 二、数据获取说明与局限性 ----------
E.append(Paragraph("二、数据获取说明与局限性", h1))
src_rows = [
    [Paragraph("<b>数据源</b>", cell), Paragraph("<b>访问状态</b>", cell),
     Paragraph("<b>平台今日招标公告量</b>", cell), Paragraph("<b>24h关键词结果</b>", cell)],
    [Paragraph("中国招标投标公共服务平台<br/>(www.cebpubservice.com)", cell),
     Paragraph("主域返回502；其数据子域(custominfo)与搜索引擎(ctbpsp.com)可加载，"
               "但检索为JavaScript驱动，无法在本工具内执行“关键词+时间”精确筛选与翻页。", cell),
     Paragraph("今日全平台 1766 条招标公告（平台首页显示）", cell),
     Paragraph("无法在工具内执行有效筛选，不能确认24h子集", cellb)],
    [Paragraph("海南省政府采购网<br/>(www.ccgp-hainan.gov.cn)", cell),
     Paragraph("连接失败（fetch failed），页面不可达，无法使用其时间筛选功能。", cell),
     Paragraph("未知（不可达）", cell),
     Paragraph("无", cellb)],
    [Paragraph("公开网络聚合检索<br/>(第三方招标聚合站)", cell),
     Paragraph("可访问，但仅返回标题与摘要片段，不含完整预算、资质、截止日期等字段，"
               "且无法按官方时间精确过滤。", cell),
     Paragraph("—", cell),
     Paragraph("24h窗口内未发现海南勘察/检测/测绘/岩土/地质灾害类公告", cellb)],
]
t = Table(src_rows, colWidths=[42*mm, 62*mm, 38*mm, 28*mm])
t.setStyle(TableStyle([
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#999999')),
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1F3864')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F2F4F8')]),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
E.append(t)
E.append(Spacer(1, 4*mm))
E.append(Paragraph(
    "说明：中国招标投标公共服务平台首页显示“今日发布 招标公告 1766 条”，"
    "证明平台当日确有大量公告；但受反爬与前端渲染限制，本工具无法在限定时间内"
    "完成“关键词∩最近24小时”的精确提取与字段级采集。", small))

# ---------- 三、时间窗口与筛选方法 ----------
E.append(Paragraph("三、时间窗口与筛选方法", h1))
E.append(Paragraph("· 时间窗口：%s（共24小时）。" % WINDOW, body))
E.append(Paragraph("· 关键词：勘察、检测、测绘、岩土、地质灾害。", body))
E.append(Paragraph("· 地域限定：以“海南/海口/三亚/儋州/陵水/琼海/文昌/万宁/澄迈/保亭/昌江/乐东/临高”等海南行政区为准。", body))
E.append(Paragraph("· 去重与真实项目识别：需排除仅含“勘察”字样但主体无关的采购（如普通物品采购、软件开发），"
                   "并合并跨源重复条目。本次因无有效24h原始数据进入该流程。", body))

# ---------- 四、检索结论 ----------
E.append(Paragraph("四、检索结论", h1))
E.append(Paragraph(
    "【结论】近24小时（%s）内，未能从指定官方渠道检索到可验证的"
    "海南地区勘察/检测/测绘/岩土/地质灾害类招标公告。" % WINDOW, note))
E.append(Paragraph("即：<b>近期无新发布招标信息</b>（在所及检索能力范围内）。", note))
E.append(Paragraph(
    "如后续需确认，建议在官方站点开放访问后，直接使用其“发布时间”筛选控件，"
    "分别查询上述关键词并人工核验预算、资质与截止日期字段。", body))

# ---------- 五、参考线索 ----------
E.append(PageBreak())
E.append(Paragraph("五、参考线索（非24小时窗口，真实检索所得，仅供参考）", h1))
E.append(Paragraph(
    "以下为本次检索到的、真实存在的海南地区勘察/检测/测绘/岩土类项目，"
    "但发布日期均在2026年6月及更早，<b>不在本报告24小时窗口内</b>，"
    "请勿当作今日新公告使用。仅作为业务线索参考。", small))
ref_rows = [
    [Paragraph("<b>项目名称</b>", cell), Paragraph("<b>地区</b>", cell),
     Paragraph("<b>发布日期</b>", cell), Paragraph("<b>类别</b>", cell),
     Paragraph("<b>来源</b>", cell)],
    [Paragraph("儋州市2026年度农村乱占耕地建房专项整治及其他耕地“非农化”、专项督查问题测绘工作竞争性磋商公告", cell),
     Paragraph("儋州", cell), Paragraph("2026-06-01", cell), Paragraph("测绘", cell),
     Paragraph("采招网", cell)],
    [Paragraph("三亚市天涯区2026年立新、扎南、抱龙田洋高标准农田建设项目测绘单位", cell),
     Paragraph("三亚", cell), Paragraph("2026-06-16", cell), Paragraph("测绘", cell),
     Paragraph("千里马", cell)],
    [Paragraph("陵水县高中学校提升改造项目（第三方工程质量检测）三次比选公告", cell),
     Paragraph("陵水", cell), Paragraph("2026-06-16", cell), Paragraph("检测", cell),
     Paragraph("千里马", cell)],
    [Paragraph("检测公司2026年第一期部分测绘项目劳务协作与技术服务招标公告", cell),
     Paragraph("海口", cell), Paragraph("2026-06-02", cell), Paragraph("测绘/检测", cell),
     Paragraph("千里马", cell)],
    [Paragraph("中国电建 三亚市藤桥河流域生态修复工程（勘察、设计、施工）EPC工程总承包劳务分包", cell),
     Paragraph("三亚", cell), Paragraph("2026-06-02", cell), Paragraph("勘察", cell),
     Paragraph("千里马", cell)],
]
rt = Table(ref_rows, colWidths=[78*mm, 14*mm, 20*mm, 18*mm, 18*mm])
rt.setStyle(TableStyle([
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#999999')),
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E5496')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F2F4F8')]),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
E.append(rt)

# ---------- 六、风险提示 ----------
E.append(Paragraph("六、风险提示与建议", h1))
E.append(Paragraph("1. 数据遗漏风险：因官方站点反爬/JS渲染限制，本工具未能执行精确时间筛选，"
                   "24小时窗口内可能存在未被检索到的公告，结论以“所及检索能力范围”为限。", body))
E.append(Paragraph("2. 字段缺失风险：公开聚合检索仅提供摘要，无法保证预算金额、CMA等级、人员证书、"
                   "设备清单、截止日期等字段的完整性，切勿据此直接投标。", body))
E.append(Paragraph("3. 时效风险：本报告生成于 %s，招标信息时效性强，请以官方平台实时发布为准。" % GEN_TIME, body))
E.append(Paragraph("4. 建议：如需准确、完整的24小时数据，请分别在 cebpubservice.com 与 "
                   "ccgp-hainan.gov.cn 使用官方“发布时间”筛选功能人工复核，并以官方公告正文为准。", body))
E.append(Spacer(1, 6*mm))
E.append(HRFlowable(width="100%", color=colors.HexColor('#CCCCCC')))
E.append(Paragraph("（本报告未包含任何虚构招标数据。如官方站点恢复可访问，可重新运行本日报任务获取完整结果。）", small))

doc.build(E, onFirstPage=footer, onLaterPages=footer)
pdf_bytes = buf.getvalue()
b64 = base64.b64encode(pdf_bytes).decode('ascii')
with open("/Users/fasimac/.qclaw/workspace/hainan_kancha_daily_2026-07-10.pdf", "wb") as f:
    f.write(pdf_bytes)
print("PDF_BYTES=%d" % len(pdf_bytes))
print("B64_LEN=%d" % len(b64))
print("B64_HEAD=" + b64[:80])
# emit full b64 to a side file for safe retrieval
with open("/Users/fasimac/.qclaw/workspace/hainan_kancha_daily_2026-07-10.b64.txt", "w") as f:
    f.write(b64)
print("WROTE_B64_FILE")
