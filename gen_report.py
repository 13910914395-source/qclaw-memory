# -*- coding: utf-8 -*-
"""生成《海南勘察招标日报》PDF（WPS 兼容 / 含中文）。
本脚本仅产出“数据抓取状态报告”，不编造任何招标公告。"""
import base64
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

REPORT_DATE = "2026-08-15"
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
try:
    pdfmetrics.registerFont(TTFont("CJK", FONT_PATH))
    FONT = "CJK"
except Exception as e:
    pdfmetrics.registerFont(TTFont("CJK", "/System/Library/Fonts/STHeiti Light.ttc", subfontIndex=0))
    FONT = "CJK"

styles = getSampleStyleSheet()
def mk(name, **kw):
    base = kw.pop("parent", styles["Normal"])
    return ParagraphStyle(name, parent=base, fontName=FONT, **kw)

title_st  = mk("t", fontSize=26, leading=32, alignment=TA_CENTER, textColor=colors.HexColor("#1F3864"))
sub_st    = mk("s", fontSize=13, leading=18, alignment=TA_CENTER, textColor=colors.HexColor("#404040"))
h1_st     = mk("h1", fontSize=15, leading=20, textColor=colors.HexColor("#1F3864"), spaceBefore=10, spaceAfter=6)
h2_st     = mk("h2", fontSize=12, leading=16, textColor=colors.HexColor("#2E5496"), spaceBefore=6, spaceAfter=3)
body_st   = mk("b", fontSize=10.5, leading=16, alignment=TA_LEFT)
cell_st   = mk("c", fontSize=9, leading=13)
cell_h_st = mk("ch", fontSize=9, leading=13, textColor=colors.white)
note_st   = mk("n", fontSize=10.5, leading=16, textColor=colors.HexColor("#9C0006"))

def P(t, s=body_st): return Paragraph(t, s)

flow = []
# ---------------- 封面 ----------------
flow += [Spacer(1, 3.2*cm)]
flow += [P("【海南勘察招标日报】", title_st)]
flow += [P(REPORT_DATE, mk("d", fontSize=16, leading=22, alignment=TA_CENTER, textColor=colors.HexColor("#2E5496")))]
flow += [Spacer(1, 0.4*cm)]
flow += [P("勘察 · 检测 · 测绘 · 岩土 · 地质灾害 招标信息监测", sub_st)]
flow += [Spacer(1, 1.0*cm)]
flow += [HRFlowable(width="60%", thickness=1, color=colors.HexColor("#2E5496"), spaceBefore=4, spaceAfter=10, hAlign="CENTER")]
cov = [
    ["报告日期", REPORT_DATE],
    ["生成时间", "2026-08-15 03:00（Asia/Shanghai）"],
    ["监测窗口", "最近 24 小时（2026-08-14 03:00 ～ 2026-08-15 03:00）"],
    ["数据来源", "中国招标投标公共服务平台、海南省政府采购网"],
    ["关键词", "勘察 / 检测 / 测绘 / 岩土 / 地质灾害"],
]
ct = Table([[P(k, cell_st), P(v, cell_st)] for k, v in cov], colWidths=[3.2*cm, 11.8*cm])
ct.setStyle(TableStyle([
    ("FONTNAME", (0,0), (-1,-1), FONT),
    ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#DCE6F1")),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#B7C6DC")),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
flow += [ct]
flow += [Spacer(1, 0.8*cm)]
flow += [P("⚠ 本期重要提示：受数据源访问限制，本环境未能从官方来源获取到最近 24 小时有效公告，"
          "报告未包含任何模拟或推断的招标条目。", note_st)]
flow += [PageBreak()]

# ---------------- 目录 ----------------
flow += [P("目录", h1_st)]
toc = [
    "一、任务概述",
    "二、数据抓取执行与结果",
    "三、数据结论",
    "四、风险提示与后续建议",
]
for t in toc:
    flow += [P(t, mk("toc", fontSize=11, leading=20))]
flow += [PageBreak()]

# ---------------- 一、任务概述 ----------------
flow += [P("一、任务概述", h1_st)]
flow += [P("本日报旨在对勘察检测行业的招标信息进行常态化监测，具体目标为：", body_st)]
flow += [P("1. 抓取「中国招标投标公共服务平台（www.cebpubservice.com）」最近 24 小时内发布的、含「勘察 / 检测 / 测绘 / 岩土 / 地质灾害」关键词的最新公告；", body_st)]
flow += [P("2. 抓取「海南省政府采购网（www.ccgp-hainan.gov.cn）」同类最新公告；", body_st)]
flow += [P("3. 仅保留发布时间在监测窗口（2026-08-14 03:00 ～ 2026-08-15 03:00）内的公告，过滤旧数据；", body_st)]
flow += [P("4. 合并去重，识别真实勘察类项目，提取项目名称、预算金额、采购人、资质要求、截止日期、发布时间、原文链接等结构化字段；", body_st)]
flow += [P("5. 生成结构化 PDF 日报与钉钉卡片摘要。", body_st)]
flow += [Spacer(1, 0.3*cm)]
flow += [P("为保证信息真实性，本报告严格遵循“无真实数据不编造”原则：凡无法从官方来源核实的数据，一律如实说明，不填充模拟条目。", body_st)]

# ---------------- 二、执行情况 ----------------
flow += [P("二、数据抓取执行与结果", h1_st)]
rows = [
    [P("数据源", cell_h_st), P("抓取方式", cell_h_st), P("执行情况", cell_h_st), P("结果", cell_h_st)],
    [P("中国招标投标公共服务平台<br/>cebpubservice.com", cell_st),
     P("HTTP 抓取 + 浏览器渲染", cell_st),
     P("站点为 JavaScript 单页应用，直接抓取仅返回页面外壳，无服务端渲染数据；已知数据接口（QueryBulletinList 等）返回 404；浏览器因 SSRF 安全策略仅允许 IP 直连，无法访问域名。", cell_st),
     P("未获取到公告数据", cell_st)],
    [P("海南省政府采购网<br/>ccgp-hainan.gov.cn", cell_st),
     P("HTTP 抓取", cell_st),
     P("网络请求持续失败（HTTPS 与 HTTP 均不可达），主机在本环境无法连接。", cell_st),
     P("未获取到公告数据", cell_st)],
]
tbl = Table(rows, colWidths=[3.4*cm, 2.8*cm, 7.6*cm, 2.8*cm])
tbl.setStyle(TableStyle([
    ("FONTNAME", (0,0), (-1,-1), FONT),
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1F3864")),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#B7C6DC")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F2F6FB")]),
    ("LEFTPADDING", (0,0), (-1,-1), 5),
    ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
flow += [tbl]

# ---------------- 三、结论 ----------------
flow += [P("三、数据结论", h1_st)]
flow += [P("受上述技术访问限制，本运行环境无法连接两个官方数据源，因此无法确认监测窗口内是否存在相关招标公告。", body_st)]
flow += [P("根据任务规则第 7 条——「如果网站没有近期数据，明确告知用户『近期无新发布招标信息』」——本次因数据源不可达而无法核实，结论与“无法确认 / 暂无”一致，明确告知：", body_st)]
flow += [P("近期无新发布招标信息（本期数据不可达，无法核实）。", mk("concl", fontSize=12, leading=18, textColor=colors.HexColor("#9C0006")))]
flow += [P("本报告不含任何模拟、推断或网络检索到的非官方条目，以避免误导投标决策。", body_st)]

# ---------------- 四、建议 ----------------
flow += [P("四、风险提示与后续建议", h1_st)]
flow += [P("⚠ 风险提示：本日报本期无有效数据，请勿据此做出投标、报价或经营决策。", note_st)]
flow += [P("建议：", body_st)]
flow += [P("1. 在网络可直连上述官网的服务器 / 环境中运行本任务；", body_st)]
flow += [P("2. 优先接入官方数据 API 或第三方招投标数据服务（如《中国政府采购网数据接口规范 V1.0》），实现稳定、合规的批量抓取；", body_st)]
flow += [P("3. 如仅需人工核查，可直接访问 cebpubservice.com 与 ccgp-hainan.gov.cn 的公告栏目，使用其时间筛选功能确认最近 24 小时发布情况；", body_st)]
flow += [P("4. 待数据源可访问后，本任务可自动补全公告提取与结构化字段（预算、资质、截止日期等）并生成完整日报。", body_st)]

# ---------------- 页脚（两遍渲染以得到总页数） ----------------
pages = []
def _foot(canvas, doc):
    pages.append(doc.page)
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(colors.HexColor("#808080"))
    canvas.drawString(2*cm, 1.0*cm, "【海南勘察招标日报】%s" % REPORT_DATE)
    canvas.drawRightString(A4[0]-2*cm, 1.0*cm, "第 %d 页" % doc.page)
    canvas.restoreState()

buf = BytesIO()
d0 = SimpleDocTemplate(buf, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm,
                       topMargin=1.8*cm, bottomMargin=1.8*cm,
                       title="海南勘察招标日报 %s" % REPORT_DATE)
d0.build(flow, onFirstPage=_foot, onLaterPages=_foot)
total = len(pages)

out_path = "/Users/fasimac/.qclaw/workspace/hainan_survey_daily_%s.pdf" % REPORT_DATE
def _foot2(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(colors.HexColor("#808080"))
    canvas.drawString(2*cm, 1.0*cm, "【海南勘察招标日报】%s" % REPORT_DATE)
    canvas.drawRightString(A4[0]-2*cm, 1.0*cm, "第 %d 页 / 共 %d 页" % (doc.page, total))
    canvas.restoreState()

doc = SimpleDocTemplate(out_path, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm,
                        topMargin=1.8*cm, bottomMargin=1.8*cm,
                        title="海南勘察招标日报 %s" % REPORT_DATE)
doc.build(flow, onFirstPage=_foot2, onLaterPages=_foot2)

with open(out_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("ascii")
print("PDF_BYTES_OK", total, out_path)
print("B64_LEN", len(b64))
# 输出 base64 到文件，便于读取
with open("/Users/fasimac/.qclaw/workspace/hainan_survey_daily_%s.b64.txt" % REPORT_DATE, "w") as f:
    f.write(b64)
