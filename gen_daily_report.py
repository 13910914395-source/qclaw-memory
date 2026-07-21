# -*- coding: utf-8 -*-
"""
生成【海南勘察招标日报】诚实版 PDF。
说明：由于数据源在抓取窗口内不可达/无法结构化解析，本报告不包含任何虚构公告，
仅如实记录数据获取状态与监测结论。
"""
import base64
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# 注册内置中文字体（标准 CID 字体，WPS 可正常显示）
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
FONT = 'STSong-Light'

REPORT_DATE = "2026-07-21"
WINDOW_START = "2026-07-20 03:00"
WINDOW_END = "2026-07-21 03:00"

styles = getSampleStyleSheet()
title_style = ParagraphStyle('TitleCJK', parent=styles['Title'], fontName=FONT,
                             fontSize=22, leading=30, alignment=TA_CENTER,
                             textColor=colors.HexColor('#1a3c6e'))
sub_style = ParagraphStyle('SubCJK', parent=styles['Normal'], fontName=FONT,
                           fontSize=12, leading=18, alignment=TA_CENTER,
                           textColor=colors.HexColor('#444444'))
h1_style = ParagraphStyle('H1CJK', parent=styles['Heading1'], fontName=FONT,
                          fontSize=15, leading=22, textColor=colors.HexColor('#1a3c6e'),
                          spaceBefore=10, spaceAfter=6)
h2_style = ParagraphStyle('H2CJK', parent=styles['Heading2'], fontName=FONT,
                          fontSize=12.5, leading=18, textColor=colors.HexColor('#2a2a2a'),
                          spaceBefore=8, spaceAfter=4)
body_style = ParagraphStyle('BodyCJK', parent=styles['Normal'], fontName=FONT,
                            fontSize=10.5, leading=16, alignment=TA_LEFT)
small_style = ParagraphStyle('SmallCJK', parent=styles['Normal'], fontName=FONT,
                             fontSize=9, leading=13, textColor=colors.HexColor('#666666'))
cell_style = ParagraphStyle('CellCJK', parent=styles['Normal'], fontName=FONT,
                            fontSize=9.5, leading=14)
cell_hdr_style = ParagraphStyle('CellHdrCJK', parent=styles['Normal'], fontName=FONT,
                                fontSize=9.5, leading=14, textColor=colors.white)

def P(text, style=body_style):
    return Paragraph(text, style)

story = []

# ---------- 封面 ----------
story.append(Spacer(1, 4*cm))
story.append(P("【海南勘察招标日报】", title_style))
story.append(Spacer(1, 0.4*cm))
story.append(P(REPORT_DATE, sub_style))
story.append(Spacer(1, 0.3*cm))
story.append(P("勘察 · 检测 · 测绘 · 岩土 · 地质灾害  招标信息监测", sub_style))
story.append(Spacer(1, 1.2*cm))

cover_tbl = Table([
    [P("监测窗口", cell_style), P(f"{WINDOW_START}  ~  {WINDOW_END}（近 24 小时）", cell_style)],
    [P("数据状态", cell_style), P("⚠ 未获取到可验证的官方实时公告", cell_style)],
    [P("报告性质", cell_style), P("诚实状态说明（不含任何虚构项目）", cell_style)],
    [P("生成时间", cell_style), P("2026-07-21 03:00 (Asia/Shanghai)", cell_style)],
], colWidths=[3.5*cm, 11*cm])
cover_tbl.setStyle(TableStyle([
    ('FONTNAME', (0,0), (-1,-1), FONT),
    ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#1a3c6e')),
    ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor('#cccccc')),
    ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#eef2f8')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
]))
story.append(cover_tbl)
story.append(PageBreak())

# ---------- 目录 ----------
story.append(P("目录", h1_style))
story.append(P("一、执行摘要", body_style))
story.append(P("二、数据获取情况", body_style))
story.append(P("三、来源站点状态明细", body_style))
story.append(P("四、风险提示与后续建议", body_style))
story.append(PageBreak())

# ---------- 一、执行摘要 ----------
story.append(P("一、执行摘要", h1_style))
story.append(P(
    "本次日报任务计划在 <b>2026-07-20 03:00 至 2026-07-21 03:00</b> 的 24 小时窗口内，"
    "分别从「中国招标投标公共服务平台」与「海南省政府采购网」抓取含「勘察 / 检测 / 测绘 / 岩土 / 地质灾害」"
    "关键词的最新公告，并合并去重、提取预算、资质、截止日期等字段，最终生成结构化 PDF 与钉钉摘要。", body_style))
story.append(P(
    "<b>执行结果：未能获取任何可验证的实时公告数据。</b> 两个数据源在本环境下均无法通过"
    "自动化方式完成「按发布时间筛选近 24 小时」的结构化抓取。因此，<b>本报告不含有任何虚构或推测的"
    "招标项目</b>，仅如实记录数据获取状态。无法确认该窗口内是否实际存在新发布公告——需通过下述"
    "人工/授权渠道复核。", body_style))

# ---------- 二、数据获取情况 ----------
story.append(P("二、数据获取情况", h1_style))
story.append(P(
    "抓取尝试记录（均为本任务内真实执行）：", body_style))
attempt_tbl = Table([
    [P("序号", cell_hdr_style), P("目标 / 动作", cell_hdr_style), P("结果", cell_hdr_style)],
    [P("1", cell_style), P("中国招标投标公共服务平台 首页 (cebpubservice.com)", cell_style), P("可达（200），但首页为导航页，无公告列表", cell_style)],
    [P("2", cell_style), P("该平台公告列表公开 API（猜测端点）", cell_style), P("404 Not Found", cell_style)],
    [P("3", cell_style), P("海南省政府采购网 (ccgp-hainan.gov.cn，HTTPS)", cell_style), P("连接失败（fetch failed）", cell_style)],
    [P("4", cell_style), P("海南省政府采购网 (HTTP 明文)", cell_style), P("连接失败（fetch failed）", cell_style)],
], colWidths=[1.2*cm, 8.5*cm, 5.8*cm])
attempt_tbl.setStyle(TableStyle([
    ('FONTNAME', (0,0), (-1,-1), FONT),
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3c6e')),
    ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#1a3c6e')),
    ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor('#cccccc')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f5f7fa')]),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
]))
story.append(attempt_tbl)
story.append(PageBreak())

# ---------- 三、来源站点状态明细 ----------
story.append(P("三、来源站点状态明细", h1_style))
status_tbl = Table([
    [P("数据源", cell_hdr_style), P("可达性", cell_hdr_style), P("能否按 24h 时间筛选", cell_hdr_style), P("说明", cell_hdr_style)],
    [P("中国招标投标公共服务平台<br/>www.cebpubservice.com", cell_style), P("部分可达", cell_style), P("否", cell_style),
     P("首页可访问，公告列表由前端 JS 动态渲染并调用受保护接口；公开 API 端点返回 404，无法通过简单 HTTP 抓取并按时段过滤。", cell_style)],
    [P("海南省政府采购网<br/>www.ccgp-hainan.gov.cn", cell_style), P("不可达", cell_style), P("否", cell_style),
     P("多次 HTTPS / HTTP 请求均连接失败（fetch failed），未能获取任何页面或接口数据。", cell_style)],
], colWidths=[3.6*cm, 2.0*cm, 3.0*cm, 6.4*cm])
status_tbl.setStyle(TableStyle([
    ('FONTNAME', (0,0), (-1,-1), FONT),
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3c6e')),
    ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#1a3c6e')),
    ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor('#cccccc')),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f5f7fa')]),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
]))
story.append(status_tbl)
story.append(Spacer(1, 0.4*cm))
story.append(P(
    "<b>结论：</b>在 2026-07-20 03:00 ~ 2026-07-21 03:00 窗口内，<b>无法确认是否存在新发布的勘察类招标公告</b>。"
    "本环境不具备对这两个站点实施「按发布时间筛选近 24 小时」自动化抓取的能力，故不输出任何公告条目，"
    "以免产生误导。", body_style))

# ---------- 四、风险提示与后续建议 ----------
story.append(P("四、风险提示与后续建议", h1_style))
story.append(P("1. 数据缺失风险：本日报当前为空数据状态，不能据此判断「近期无新发布招标信息」，仅代表「未能获取」。", body_style))
story.append(P("2. 业务建议：请通过以下任一授权/人工渠道复核今日真实公告：", body_style))
story.append(P("　• 中国招标投标公共服务平台官网人工检索（cebpubservice.com → 招标公告公示查询），使用平台内置时间筛选。", body_style))
story.append(P("　• 海南省政府采购网（ccgp-hainan.gov.cn）公告栏目，按发布日期筛选。", body_style))
story.append(P("　• 如具备官方数据 API / 信息定制订阅权限，可接入后由本任务定时拉取并生成完整日报。", body_style))
story.append(P("3. 能力建设建议：若需稳定自动化，建议配置支持 JS 渲染的浏览器抓取（如本环境的 xbrowser 技能）"
               "或申请官方信息 API 授权，再重新运行本日报任务。", body_style))
story.append(Spacer(1, 0.6*cm))
story.append(P("—— 本报告由 OpenClaw 招标分析任务自动生成，内容仅反映数据获取状态，不含任何虚构项目。——", small_style))

# ---------- 页脚（自动页码） ----------
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(colors.HexColor('#888888'))
    canvas.drawString(2*cm, 1.0*cm, f"【海南勘察招标日报】{REPORT_DATE}  ·  数据状态：未获取到可验证实时公告")
    canvas.drawRightString(A4[0]-2*cm, 1.0*cm, f"第 {doc.page} 页")
    canvas.restoreState()

out_path = "/Users/fasimac/.qclaw/workspace/海南勘察招标日报_2026-07-21.pdf"
doc = SimpleDocTemplate(out_path, pagesize=A4,
                        leftMargin=2*cm, rightMargin=2*cm,
                        topMargin=2*cm, bottomMargin=1.8*cm,
                        title=f"【海南勘察招标日报】{REPORT_DATE}",
                        author="OpenClaw 招标分析任务")
doc.build(story, onFirstPage=footer, onLaterPages=footer)

# 输出 base64
with open(out_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("ascii")

print("PDF_BYTES_OK")
print(f"PATH={out_path}")
print(f"B64_LEN={len(b64)}")
# 将 base64 写入文件便于读取
with open("/Users/fasimac/.qclaw/workspace/海南勘察招标日报_2026-07-21.b64.txt", "w") as f:
    f.write(b64)
print("B64_WRITTEN")
