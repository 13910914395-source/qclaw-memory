# -*- coding: utf-8 -*-
"""Generate an honest, WPS-compatible PDF '海南勘察招标日报'.
This report does NOT fabricate tender data. It transparently states the
verified access limitation encountered while attempting to scrape the two
required official sources within the strict last-24h window.
"""
import base64
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Embed a real Chinese font for WPS/Acrobat compatibility
FONT_PATH = "/System/Library/Fonts/Songti.ttc"
try:
    pdfmetrics.registerFont(TTFont("CJK", FONT_PATH, subfontIndex=0))
    BASE = "CJK"
except Exception:
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    BASE = "STSong-Light"

NOW = datetime.datetime(2026, 8, 19, 3, 0, 0)  # Asia/Shanghai (task clock)
GEN_TS = NOW.strftime("%Y-%m-%d %H:%M:%S")

styles = getSampleStyleSheet()
def S(name, **kw):
    kw.setdefault("fontName", BASE)
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

title_style = S("TitleC", fontSize=26, leading=32, alignment=TA_CENTER,
                textColor=HexColor("#1F3864"), spaceAfter=6)
sub_style   = S("SubC", fontSize=13, leading=18, alignment=TA_CENTER,
                textColor=HexColor("#555555"))
h1          = S("H1", fontSize=15, leading=20, textColor=HexColor("#1F3864"),
                spaceBefore=10, spaceAfter=6)
body        = S("Body", fontSize=10.5, leading=16, alignment=TA_LEFT,
                spaceAfter=4)
bullet      = S("Bullet", fontSize=10.5, leading=16, leftIndent=14,
                bulletIndent=4, spaceAfter=2)
note        = S("Note", fontSize=9.5, leading=14, textColor=HexColor("#8B0000"))
small       = S("Small", fontSize=9, leading=12, textColor=HexColor("#777777"))

story = []

# ---------- COVER ----------
story.append(Spacer(1, 60))
story.append(Paragraph("海南勘察招标日报", title_style))
story.append(Paragraph("【海南勘察招标日报】2026-08-19", sub_style))
story.append(Spacer(1, 10))
story.append(HRFlowable(width="60%", thickness=1.2, color=HexColor("#1F3864"),
                        spaceBefore=4, spaceAfter=14, hAlign="CENTER"))
story.append(Paragraph("勘察 · 检测 · 测绘 · 岩土 · 地质灾害 招标信息日报", sub_style))
story.append(Spacer(1, 40))
cover_tbl = Table([
    ["统计窗口", "2026-08-18 03:00 ~ 2026-08-19 03:00（北京时间）"],
    ["数据来源", "中国招标投标公共服务平台 / 海南省政府采购网"],
    ["报告生成时间", GEN_TS],
    ["本期有效公告", "0 条（未能实时抓取核验）"],
], colWidths=[40*mm, 110*mm])
cover_tbl.setStyle(TableStyle([
    ("FONTNAME", (0,0), (-1,-1), BASE),
    ("FONTSIZE", (0,0), (-1,-1), 10.5),
    ("TEXTCOLOR", (0,0), (0,-1), HexColor("#1F3864")),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("LINEBELOW", (0,0), (-1,-2), 0.4, HexColor("#DDDDDD")),
]))
story.append(cover_tbl)
story.append(Spacer(1, 30))
story.append(Paragraph("本报告不含有任何虚构招标数据。详见正文第二节《数据抓取与核验说明》。",
                       note))
story.append(PageBreak())

# ---------- TOC ----------
story.append(Paragraph("目录", h1))
toc = [
    "一、本期数据概览",
    "二、数据抓取与核验说明（访问限制）",
    "三、结论与风险提示",
    "四、可行的后续方案",
]
for t in toc:
    story.append(Paragraph(t, body))
story.append(PageBreak())

# ---------- BODY ----------
story.append(Paragraph("一、本期数据概览", h1))
story.append(Paragraph(
    "按任务要求，需在统计窗口 <b>2026-08-18 03:00 至 2026-08-19 03:00</b>（北京时间，"
    "最近 24 小时）内，分别抓取中国招标投标公共服务平台（www.cebpubservice.com）与"
    "海南省政府采购网（www.ccgp-hainan.gov.cn）含「勘察 / 检测 / 测绘 / 岩土 / 地质灾害」"
    "关键词的最新公告各 50 条，经去重与真实性筛选后汇总。", body))
story.append(Paragraph(
    "<b>结论：本期未能从任一指定官方信源实时抓取并核验到任何公告，故无有效数据可汇总，"
    "报告不含任何招标条目。</b>", body))

story.append(Paragraph("二、数据抓取情况与访问限制（已逐项验证）", h1))
limits = [
    ("浏览器自动化（CDP/Chrome）",
     "被本运行环境的严格 SSRF / DNS 重绑定防护策略拦截：仅允许以 IP 字面量地址导航，"
     "禁止一切基于主机名的外部站点访问，因此无法打开上述两个网站。"),
    ("海南省政府采购网 ccgp-hainan.gov.cn",
     "抓取出口对该主机完全不可达：http / https、带 www 与不带 www 多种组合均返回"
     " “fetch failed”，无法获取列表或详情页。"),
    ("中国招标投标公共服务平台 cebpubservice.com",
     "为纯前端 JavaScript 单页应用；其公告数据经 XHR 接口加载，直接访问的数据端点"
     "（含搜索/列表路径）均返回 404，匿名环境无可用 GET 接口。"),
    ("公开搜索索引（web_search）",
     "仅能返回通用索引内容，未能提供上述两站在本统计窗口内、且字段完整"
     "（预算/资质/截止日/原文链接）的可核验公告。"),
]
for k, v in limits:
    story.append(Paragraph("• <b>%s</b>：%s" % (k, v), bullet))

story.append(Paragraph("三、结论与风险提示", h1))
story.append(Paragraph(
    "1. 本报告<b>不生成任何虚构的招标项目名称、预算金额、采购人、资质要求或截止日期</b>。"
    "以伪造数据填充日报，可能误导真实的投标与经营决策，存在合规与商业风险。", body))
story.append(Paragraph(
    "2. 因此本期无法得出“近期无新发布招标信息”的断言——准确表述应为："
    "<b>在受限运行环境下无法访问指定信源，故无法确认或排除近期公告</b>。", body))
story.append(Paragraph(
    "3. 如需据此进行投标研判，请在具备对应网络访问权限的环境中重新执行抓取，"
    "或参见第四节提供的可落地方案。", body))

story.append(Paragraph("四、可行的后续方案", h1))
for t in [
    "授予本运行环境对上述两个域名的出站网络访问（白名单 / 关闭 SSRF 主机名拦截），即可重跑真实抓取。",
    "提供两站的官方数据接口 / API Key（如 cebpubservice 信息 API、海南政府采购智慧云平台接口），可对接后生成完整日报。",
    "在可直连公网的机器上运行本任务的抓取脚本，再将结果回传，由本环境负责排版与 PDF 生成。",
]:
    story.append(Paragraph("• " + t, bullet))

story.append(Spacer(1, 14))
story.append(HRFlowable(width="100%", thickness=0.6, color=HexColor("#CCCCCC")))
story.append(Paragraph(
    "说明：本日报为自动化分析产物；当数据缺失时以透明说明替代虚构内容，"
    "以确保信息可溯源、可追责。", small))

# ---------- FOOTER ----------
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(BASE, 8)
    canvas.setFillColor(HexColor("#999999"))
    canvas.drawString(18*mm, 12*mm, "海南勘察招标日报 · 2026-08-19 · 自动生成")
    canvas.drawRightString(A4[0]-18*mm, 12*mm, "第 %d 页" % doc.page)
    canvas.restoreState()

OUT = "/Users/fasimac/.qclaw/workspace/海南勘察招标日报_2026-08-19.pdf"
doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=20*mm, rightMargin=20*mm,
                        topMargin=18*mm, bottomMargin=20*mm,
                        title="海南勘察招标日报 2026-08-19",
                        author="OpenClaw 招标分析助手")
doc.build(story, onFirstPage=footer, onLaterPages=footer)

with open(OUT, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("ascii")
print("PDF_BYTES_OK")
print("BASE64_LEN=%d" % len(b64))
# emit base64 in chunks to avoid one gigantic line issues
import sys
sys.stdout.write("BASE64_START\n")
# write to a side file for the caller to read
with open("/Users/fasimac/.qclaw/workspace/海南勘察招标日报_2026-08-19.b64.txt", "w") as f:
    f.write(b64)
print("WROTE_B64_FILE")
