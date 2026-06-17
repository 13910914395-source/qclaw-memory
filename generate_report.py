#!/usr/bin/env python3
"""Generate 【海南勘察招标日报】PDF report"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate, Frame
from reportlab.platypus.frames import Frame
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.tableofcontents import TableOfContents

# Register Chinese fonts
FONT_HEITI = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_HEITI_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"

# Try to register fonts
FONTS_OK = True
try:
    pdfmetrics.registerFont(TTFont('Heiti', FONT_HEITI, subfontIndex=0))
    pdfmetrics.registerFont(TTFont('Heiti-Light', FONT_HEITI_LIGHT, subfontIndex=0))
    # Register PingFang if possible, but use Heiti as fallback
    pingfang_path = "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/86ba2c91f017a3749571a82f2c6d890ac7ffb2fb.asset/AssetData/PingFang.ttc"
    try:
        pdfmetrics.registerFont(TTFont('PingFang', pingfang_path, subfontIndex=1))
        BODY_FONT = 'PingFang'
        print("Using PingFang for body")
    except:
        BODY_FONT = 'Heiti'
        print("Falling back to Heiti for body")
    TITLE_FONT = 'Heiti'
    BOLD_FONT = 'Heiti'
    LIGHT_FONT = 'Heiti-Light'
except Exception as e:
    print(f"Font registration error: {e}")
    FONTS_OK = False
    BODY_FONT = 'Helvetica'
    TITLE_FONT = 'Helvetica-Bold'
    BOLD_FONT = 'Helvetica-Bold'
    LIGHT_FONT = 'Helvetica'

# Colors
DARK_BLUE = HexColor('#1a365d')
MEDIUM_BLUE = HexColor('#2c5282')
LIGHT_BLUE = HexColor('#ebf4ff')
ACCENT_RED = HexColor('#c53030')
ACCENT_ORANGE = HexColor('#dd6b20')
DARK_GREY = HexColor('#2d3748')
MED_GREY = HexColor('#718096')
LIGHT_GREY = HexColor('#e2e8f0')
TABLE_HEADER_BG = HexColor('#2c5282')
TABLE_ALT_ROW = HexColor('#f7fafc')

PAGE_W, PAGE_H = A4

# Styles
styles = getSampleStyleSheet()

cover_title_style = ParagraphStyle(
    'CoverTitle', fontName=TITLE_FONT, fontSize=28, leading=38,
    alignment=TA_CENTER, textColor=DARK_BLUE, spaceAfter=12
)
cover_subtitle_style = ParagraphStyle(
    'CoverSubtitle', fontName=BODY_FONT, fontSize=14, leading=20,
    alignment=TA_CENTER, textColor=MED_GREY, spaceAfter=6
)
cover_date_style = ParagraphStyle(
    'CoverDate', fontName=BOLD_FONT, fontSize=18, leading=24,
    alignment=TA_CENTER, textColor=MEDIUM_BLUE, spaceAfter=6
)

h1_style = ParagraphStyle(
    'H1', fontName=TITLE_FONT, fontSize=20, leading=28,
    textColor=DARK_BLUE, spaceBefore=20, spaceAfter=12
)
h2_style = ParagraphStyle(
    'H2', fontName=BOLD_FONT, fontSize=15, leading=22,
    textColor=MEDIUM_BLUE, spaceBefore=16, spaceAfter=8
)
h3_style = ParagraphStyle(
    'H3', fontName=BOLD_FONT, fontSize=12, leading=18,
    textColor=DARK_GREY, spaceBefore=12, spaceAfter=6
)

body_style = ParagraphStyle(
    'BodyCN', fontName=BODY_FONT, fontSize=10, leading=16,
    textColor=DARK_GREY, alignment=TA_JUSTIFY, spaceBefore=4, spaceAfter=4,
    firstLineIndent=0
)
body_bold_style = ParagraphStyle(
    'BodyCN-Bold', parent=body_style, fontName=BOLD_FONT
)
small_style = ParagraphStyle(
    'SmallCN', fontName=BODY_FONT, fontSize=8, leading=12,
    textColor=MED_GREY
)
table_header_style = ParagraphStyle(
    'TableHeader', fontName=BOLD_FONT, fontSize=9, leading=13,
    textColor=white, alignment=TA_CENTER
)
table_cell_style = ParagraphStyle(
    'TableCell', fontName=BODY_FONT, fontSize=8, leading=12,
    textColor=DARK_GREY, alignment=TA_LEFT
)
table_cell_center = ParagraphStyle(
    'TableCellCenter', parent=table_cell_style, alignment=TA_CENTER
)

TODAY = datetime.now().strftime('%Y-%m-%d')
REPORT_DATE = "2026-06-17"

# ─── Page template with footer ───
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(BODY_FONT, 8)
    canvas.setFillColor(MED_GREY)
    canvas.drawString(20*mm, 12*mm, f"【海南勘察招标日报】{REPORT_DATE}")
    canvas.drawRightString(PAGE_W - 20*mm, 12*mm, f"第 {canvas.getPageNumber()} 页")
    # Line above footer
    canvas.setStrokeColor(LIGHT_GREY)
    canvas.line(20*mm, 16*mm, PAGE_W - 20*mm, 16*mm)
    canvas.restoreState()

# ─── Build document ───
output_path = f"/Users/fasimac/.qclaw/workspace/海南勘察招标日报_{REPORT_DATE}.pdf"

doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=20*mm, bottomMargin=22*mm,
    title=f"海南勘察招标日报 {REPORT_DATE}",
    author="QClaw 招标分析系统"
)

story = []

# ═══════════════════ COVER PAGE ═══════════════════
story.append(Spacer(1, 80*mm))
story.append(Paragraph("海 南 勘 察 招 标 日 报", cover_title_style))
story.append(Spacer(1, 10*mm))
story.append(Paragraph(f"每日勘察检测行业招标信息监测报告", cover_subtitle_style))
story.append(Spacer(1, 8*mm))
story.append(Paragraph(f"报告日期：{REPORT_DATE}", cover_date_style))
story.append(Spacer(1, 5*mm))
story.append(Paragraph("监测周期：最近24小时（2026-06-16 03:00 ~ 2026-06-17 03:00）", cover_subtitle_style))
story.append(Spacer(1, 15*mm))

# Decorative line
story.append(HRFlowable(width="60%", thickness=1, color=MEDIUM_BLUE, spaceBefore=0, spaceAfter=8))
story.append(Paragraph("数据来源：中国招标投标公共服务平台 | 海南省政府采购网", cover_subtitle_style))
story.append(Paragraph("关键词：勘察 · 检测 · 测绘 · 岩土 · 地质灾害", cover_subtitle_style))
story.append(Paragraph("分析引擎：QClaw 勘察检测行业招标分析师", small_style))
story.append(PageBreak())

# ═══════════════════ TABLE OF CONTENTS ═══════════════════
story.append(Paragraph("目  录", h1_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=DARK_BLUE))
story.append(Spacer(1, 8*mm))

toc_items = [
    ("一、", "执行摘要", "3"),
    ("二、", "数据采集状态", "4"),
    ("  2.1", "中国招标投标公共服务平台（cebpubservice.com）", "4"),
    ("  2.2", "海南省政府采购网（ccgp-hainan.gov.cn）", "5"),
    ("  2.3", "全网补充检索", "6"),
    ("三、", "今日招标信息汇总", "7"),
    ("四、", "行业动态与政策观察", "8"),
    ("五、", "风险提示与建议", "9"),
    ("六、", "附录：数据采集技术说明", "10"),
]

for num, title, page in toc_items:
    indent = "　　" if num.startswith("  ") else ""
    story.append(Paragraph(
        f"{indent}{num.strip()}　{title}",
        ParagraphStyle('TOCItem', fontName=BODY_FONT, fontSize=11, leading=22,
                       textColor=DARK_GREY, leftIndent=10*mm if indent else 0)
    ))

story.append(PageBreak())

# ═══════════════════ SECTION 1: 执行摘要 ═══════════════════
story.append(Paragraph("一、执行摘要", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=MEDIUM_BLUE))
story.append(Spacer(1, 5*mm))

summary_data = [
    ["监测指标", "数据"],
    ["报告日期", REPORT_DATE],
    ["监测时段", "2026-06-16 03:00 ~ 2026-06-17 03:00"],
    ["目标平台(1)", "中国招标投标公共服务平台 (cebpubservice.com)"],
    ["目标平台(2)", "海南省政府采购网 (ccgp-hainan.gov.cn)"],
    ["监测关键词", "勘察、检测、测绘、岩土、地质灾害"],
    ["本期新增招标公告", "0 条"],
    ["累计监测招标公告", "0 条"],
]

t = Table(summary_data, colWidths=[120, 380])
t.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), BOLD_FONT),
    ('FONTNAME', (0, 0), (-1, 0), BOLD_FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('BACKGROUND', (0, 1), (0, -1), LIGHT_BLUE),
    ('ALIGN', (0, 0), (0, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GREY),
    ('ROWBACKGROUNDS', (1, 1), (-1, -1), [white, TABLE_ALT_ROW]),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
story.append(t)
story.append(Spacer(1, 8*mm))

story.append(Paragraph(
    f"<b>核心结论：</b>截至{REPORT_DATE} 03:00，在最近24小时监测周期内，"
    f"两个目标平台均未检索到符合关键词条件的新增勘察检测类招标公告。"
    f"中国招标投标公共服务平台（cebpubservice.com）在访问时持续返回502网关错误，"
    f"服务可能处于不可用状态；海南省政府采购网为JavaScript单页应用，不支持直接数据抓取。"
    f"同时通过多个搜索引擎进行的全网补充检索也未发现海南地区勘察检测类新增招标信息。"
    f"建议持续关注平台状态，并在服务恢复后补充抓取。",
    body_style
))
story.append(PageBreak())

# ═══════════════════ SECTION 2: 数据采集状态 ═══════════════════
story.append(Paragraph("二、数据采集状态", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=MEDIUM_BLUE))
story.append(Spacer(1, 5*mm))

# 2.1 cebpubservice
story.append(Paragraph("2.1 中国招标投标公共服务平台（cebpubservice.com）", h2_style))

ceb_data = [
    ["检测项目", "结果"],
    ["HTTP 状态", "502 Bad Gateway（持续）"],
    ["网站可访问性", "❌ 不可访问"],
    ["DNS 解析", "✅ 正常（39.96.127.96）"],
    ["搜索引擎索引", "❌ 未返回该平台近期记录"],
    ["数据抓取结果", "0 条公告"],
]
t = Table(ceb_data, colWidths=[120, 380])
t.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), BOLD_FONT),
    ('FONTNAME', (0, 0), (-1, 0), BOLD_FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('BACKGROUND', (0, 1), (0, -1), LIGHT_BLUE),
    ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GREY),
    ('ROWBACKGROUNDS', (1, 1), (-1, -1), [white, TABLE_ALT_ROW]),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(Paragraph(
    "该平台为中国招标投标公共服务平台国家级门户，服务部署于阿里云（Tengine/nginx），"
    "访问时持续返回502 Bad Gateway。可能原因为后端服务故障、维护中或触发了反爬策略。"
    "搜索引擎（百度、Bing、Google）也未返回该平台近期的相关索引结果。",
    body_style
))
story.append(PageBreak())

# 2.2 ccgp-hainan
story.append(Paragraph("2.2 海南省政府采购网（ccgp-hainan.gov.cn）", h2_style))

ccgp_data = [
    ["检测项目", "结果"],
    ["HTTP 状态", "200 OK（门户首页正常）"],
    ["网站类型", "Vue.js SPA 单页应用"],
    ["API 可访问性", "❌ 搜索API端点返回404"],
    ["数据抓取方式", "不适用（需浏览器渲染+身份认证）"],
    ["搜索引擎索引", "❌ 未返回该平台相关招标记录"],
    ["数据抓取结果", "0 条公告"],
]
t = Table(ccgp_data, colWidths=[120, 380])
t.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), BOLD_FONT),
    ('FONTNAME', (0, 0), (-1, 0), BOLD_FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('BACKGROUND', (0, 1), (0, -1), LIGHT_BLUE),
    ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GREY),
    ('ROWBACKGROUNDS', (1, 1), (-1, -1), [white, TABLE_ALT_ROW]),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(Paragraph(
    "海南省政府采购网采用Vue.js框架构建SPA应用，数据通过内部API异步加载，"
    "需完整的浏览器渲染环境和可能的身份认证令牌才能获取搜索数据。"
    "目前的自动化工具（web_fetch、curl）无法解析JavaScript渲染内容，"
    "API接口路径（/gateway/gpc-gpcms/rest/v2/）未公开文档，尝试多种端点均返回404。",
    body_style
))
story.append(PageBreak())

# 2.3 全网补充检索
story.append(Paragraph("2.3 全网补充检索", h2_style))

search_data = [
    ["搜索引擎", "检索策略", "返回结果"],
    ["百度/Google/Bing", "site:cebpubservice.com + 关键词", "0条相关招标公告"],
    ["百度/Google/Bing", "site:ccgp-hainan.gov.cn + 关键词", "0条相关招标公告"],
    ["元宝搜索(综合)", "海南 + 勘察/检测/测绘 + 招标", "0条相关招标公告"],
    ["元宝搜索(综合)", "勘察设计/地质勘察/第三方检测 + 海南", "0条相关招标公告"],
    ["多引擎(17引擎)", "泛关键词全网检索", "0条海南勘察类招标"],
]
t = Table(search_data, colWidths=[100, 180, 220])
t.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, 0), BOLD_FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GREY),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, TABLE_ALT_ROW]),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(PageBreak())

# ═══════════════════ SECTION 3: 招标信息汇总 ═══════════════════
story.append(Paragraph("三、今日招标信息汇总", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=MEDIUM_BLUE))
story.append(Spacer(1, 5*mm))

story.append(Paragraph(
    f"在{REPORT_DATE}的24小时监测周期内，<b>未发现符合筛选条件的勘察检测类新增招标公告</b>。",
    body_style
))
story.append(Spacer(1, 3*mm))

# Empty table with headers
empty_headers = ["序号", "项目名称", "预算金额", "采购人", "资质要求", "截止日期", "发布时间", "来源"]
empty_data = [empty_headers]
empty_data.append(["—", "近期无新发布招标信息", "—", "—", "—", "—", "—", "—"])

t = Table(empty_data, colWidths=[25, 110, 55, 70, 75, 55, 55, 55])
t.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, 0), BOLD_FONT),
    ('FONTNAME', (0, 1), (-1, 1), BODY_FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('BACKGROUND', (0, 1), (-1, 1), HexColor('#fff5f5')),
    ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GREY),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('ALIGN', (0, 0), (0, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(t)
story.append(Spacer(1, 6*mm))

story.append(Paragraph("📊 统计摘要", h3_style))
stats_data = [
    ["类别", "数量"],
    ["勘察类招标", "0"],
    ["检测类招标", "0"],
    ["测绘类招标", "0"],
    ["岩土工程类招标", "0"],
    ["地质灾害类招标", "0"],
    ["合计", "0"],
]
t = Table(stats_data, colWidths=[200, 300])
t.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, 0), BOLD_FONT),
    ('FONTNAME', (0, -1), (0, -1), BOLD_FONT),
    ('FONTNAME', (0, -1), (-1, -1), BOLD_FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('BACKGROUND', (0, -1), (-1, -1), LIGHT_BLUE),
    ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GREY),
    ('ALIGN', (0, 0), (0, -1), 'CENTER'),
    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -2), [white, TABLE_ALT_ROW]),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(PageBreak())

# ═══════════════════ SECTION 4: 行业动态 ═══════════════════
story.append(Paragraph("四、行业动态与政策观察", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=MEDIUM_BLUE))
story.append(Spacer(1, 5*mm))

story.append(Paragraph("4.1 海南自然资源要素精准供给政策", h3_style))
story.append(Paragraph(
    "2026年6月16日，海南省自然资源和规划厅发布消息，海南多部门联合印发《进一步强化自然资源要素精准供给若干政策措施》，"
    "围绕空间规划、耕地保护、土地征收、用地审批等8个方面出台21条具体政策举措。"
    "该政策将直接推动海南省勘察测绘、地质灾害评估等自然资源领域服务需求的增长。",
    body_style
))

story.append(Paragraph("4.2 全国勘察行业关注动态", h3_style))
story.append(Paragraph(
    "青海省中色股份控股子公司青海中色近日取得青海省都兰县哈日扎地区多金属矿勘探探矿权证，"
    "勘查面积12.63平方公里（2026年6月8日至2030年11月25日），"
    "反映矿产资源勘查领域持续活跃。辽宁矿投集团同期举行2026年度地质灾害应急演练，"
    "强化地质灾害防治能力建设。",
    body_style
))

story.append(Paragraph("4.3 平台数据可用性说明", h3_style))
story.append(Paragraph(
    "本次监测发现，国家级招标信息平台（cebpubservice.com）存在服务不稳定的情况。"
    "建议：①关注中国政府采购网（ccgp.gov.cn）海南分站作为备选数据源；"
    "②添加海南省公共资源交易平台（zw.hainan.gov.cn）作为补充监测渠道；"
    "③考虑引入商业招标数据API（如剑鱼标讯、招标雷达等）作为数据互补方案。",
    body_style
))
story.append(PageBreak())

# ═══════════════════ SECTION 5: 风险提示 ═══════════════════
story.append(Paragraph("五、风险提示与建议", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_RED))
story.append(Spacer(1, 5*mm))

risk_items = [
    ("⚠️ 数据源不可用风险", 
     "中国招标投标公共服务平台持续返回502错误，可能导致公告遗漏。"
     "该平台日均发布招标信息数千条，服务中断可能影响监测完整性。"),
    ("⚠️ 技术爬取限制",
     "海南省政府采购网采用SPA架构，传统HTTP抓取工具无法获取动态渲染数据。"
     "需要配置Headless浏览器（Puppeteer/Playwright）或接入商业API。"),
    ("⚠️ 零结果不代表无招标",
     "本期未检索到招标公告，可能因平台服务中断或搜索引擎索引延迟导致。"
     "不代表海南地区实际无勘察检测类招标活动。"),
    ("💡 改进建议",
     "1. 添加备选数据源：中国政府采购网(ccgp.gov.cn)、海南省公共资源交易平台"
     "2. 配置浏览器自动化：通过xbrowser或Playwright实现SPA动态渲染抓取"
     "3. 引入商业API：剑鱼标讯、招标雷达等商业平台提供结构化招标数据"
     "4. 延长监测窗口：将监测时段扩展至72小时以覆盖周末/节假日数据积压"),
]

for title, desc in risk_items:
    story.append(Paragraph(f"<b>{title}</b>", body_bold_style))
    story.append(Paragraph(desc, body_style))
    story.append(Spacer(1, 3*mm))

story.append(PageBreak())

# ═══════════════════ SECTION 6: 附录 ═══════════════════
story.append(Paragraph("六、附录：数据采集技术说明", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=MEDIUM_BLUE))
story.append(Spacer(1, 5*mm))

story.append(Paragraph("6.1 采集方法", h3_style))
tech_data = [
    ["方法", "工具", "目标平台", "结果"],
    ["HTTP直接请求", "curl / web_fetch", "cebpubservice.com", "502错误"],
    ["HTTP直接请求", "curl / web_fetch", "ccgp-hainan.gov.cn", "返回SPA壳页面"],
    ["API端点探测", "curl (多路径穷举)", "ccgp-hainan.gov.cn API", "全部404"],
    ["浏览器自动化", "CDP Browser", "两个平台", "SSRF策略阻止"],
    ["搜索引擎索引", "17引擎全网检索", "两个平台", "未返回招标公告"],
    ["元宝综合搜索", "web_search(多轮次)", "全网", "未发现海南勘察类招标"],
]
t = Table(tech_data, colWidths=[80, 110, 130, 180])
t.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, 0), BOLD_FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GREY),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, TABLE_ALT_ROW]),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(Spacer(1, 5*mm))

story.append(Paragraph("6.2 关键词配置", h3_style))
story.append(Paragraph(
    "核心关键词：勘察 | 检测 | 测绘 | 岩土 | 地质灾害<br/>"
    "扩展关键词：工程勘察 | 地质勘察 | 勘察设计 | 工程质量检测 | 第三方检测 | "
    "测绘服务 | 岩土工程 | 地质灾害评估 | 地质灾害治理<br/>"
    "排除词：勘察设计资质（人才招聘类）| 勘察设计注册工程师（考试类）",
    body_style
))

story.append(Paragraph("6.3 下一次监测", h3_style))
story.append(Paragraph(
    f"下一次自动监测将在 2026-06-18 约 03:00 执行。"
    f"建议在数据源恢复后，手动补充抓取可能遗漏的公告。",
    body_style
))

story.append(Spacer(1, 15*mm))
story.append(HRFlowable(width="100%", thickness=1, color=LIGHT_GREY))
story.append(Paragraph(f"报告自动生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CST", small_style))
story.append(Paragraph("生成引擎：QClaw 勘察检测行业招标分析师 v2.0 | ReportLab PDF Engine", small_style))
story.append(Paragraph("免责声明：本报告基于公开信息自动生成，仅供参考，不构成投标决策建议。", small_style))

# ─── Build PDF ───
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"PDF generated: {output_path}")
print(f"File size: {os.path.getsize(output_path)} bytes")
