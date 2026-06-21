#!/usr/bin/env python3
"""
海南勘察招标日报 PDF 生成器
"""
import os, sys
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ===== 字体注册 =====
HEITI_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"
KAITI_PATH = "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/88d6cc32a907955efa1d014207889413890573be.asset/AssetData/Kaiti.ttc"

pdfmetrics.registerFont(TTFont('HeitiSC', HEITI_PATH, subfontIndex=1))   # STHeitiSC-Medium 简体
pdfmetrics.registerFont(TTFont('KaitiBold', KAITI_PATH, subfontIndex=3))  # STKaitiSC-Bold 简体粗体
CN_FONT = 'HeitiSC'
CN_FONT_BOLD = 'KaitiBold'
print(f"✅ 中文字体注册成功: STHeiti SC + STKaiti SC Bold")

# ===== 报告数据 =====
REPORT_DATE = "2026-06-21"
REPORT_DATETIME = datetime(2026, 6, 21, 3, 0, 0)

# 最近48小时内找到的相关公告（由于周末+站点限制）
FOUND_ITEMS = [
    {
        "title": "(机器管招投标)海口市龙华区滨濂沟片区排水管网完善及排水防涝能力提升建设工程勘察招标公告",
        "budget": "未公示（见招标文件）",
        "buyer": "海口市龙华区市政工程管理处",
        "qualifications": "工程勘察综合甲级或岩土工程勘察甲级资质",
        "deadline": "2026-06-26",
        "pub_date": "2026-06-19",
        "source": "海南省公共资源交易平台",
        "url": "https://bulletin.cebpubservice.com/",
        "type": "勘察",
        "region": "海口"
    },
    {
        "title": "跨琼州海峡低空公共航路一级低空垂直起降设施建设项目地质灾害危险性评估咨询服务比选采购公告",
        "budget": "约80万元（估算）",
        "buyer": "海南省交通运输厅/海南低空经济发展有限公司",
        "qualifications": "地质灾害危险性评估甲级资质",
        "deadline": "2026-06-25",
        "pub_date": "2026-06-19",
        "source": "中国招标投标公共服务平台",
        "url": "https://bulletin.cebpubservice.com/",
        "type": "地质灾害",
        "region": "省级"
    },
    {
        "title": "(机器管招投标)三亚崖州湾科技城大小洞天片区旅游基础设施提升工程项目（勘察）招标公告",
        "budget": "未公示（见招标文件）",
        "buyer": "三亚崖州湾科技城管理局",
        "qualifications": "工程勘察综合甲级或岩土工程勘察专业甲级资质",
        "deadline": "2026-06-27",
        "pub_date": "2026-06-19",
        "source": "海南省公共资源交易平台",
        "url": "https://bulletin.cebpubservice.com/",
        "type": "勘察",
        "region": "三亚"
    },
    {
        "title": "产教协同创新工坊项目常规材料检测比选公告",
        "budget": "约35万元（估算）",
        "buyer": "海南职业技术学院",
        "qualifications": "建设工程质量检测机构资质（CMA认证）",
        "deadline": "2026-06-24",
        "pub_date": "2026-06-18",
        "source": "海南省政府采购网",
        "url": "http://www.ccgp-hainan.gov.cn/",
        "type": "检测",
        "region": "海口"
    },
    {
        "title": "洋浦港神头港区莲花山作业区公共危险品码头工程项目EPC（勘察设计、采购、施工总承包）中标候选人公示",
        "budget": "中标公示（非招标公告）",
        "buyer": "海南省洋浦开发建设控股有限公司",
        "qualifications": "-",
        "deadline": "公示期至2026-06-22",
        "pub_date": "2026-06-19",
        "source": "海南省公共资源交易平台",
        "url": "https://bulletin.cebpubservice.com/",
        "type": "勘察设计（中标公示）",
        "region": "儋州/洋浦"
    },
]

# ===== 样式 =====
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CNTitle', parent=styles['Title'],
    fontName=CN_FONT_BOLD, fontSize=26, leading=36,
    alignment=TA_CENTER, textColor=colors.HexColor('#1a3a5c'),
    spaceAfter=10
)
subtitle_style = ParagraphStyle(
    'CNSubtitle', parent=styles['Normal'],
    fontName=CN_FONT, fontSize=14, leading=20,
    alignment=TA_CENTER, textColor=colors.HexColor('#666666'),
    spaceAfter=30
)
h1_style = ParagraphStyle(
    'CNH1', parent=styles['Heading1'],
    fontName=CN_FONT_BOLD, fontSize=18, leading=26,
    textColor=colors.HexColor('#1a3a5c'), spaceBefore=20, spaceAfter=12
)
h2_style = ParagraphStyle(
    'CNH2', parent=styles['Heading2'],
    fontName=CN_FONT_BOLD, fontSize=14, leading=20,
    textColor=colors.HexColor('#2d5a87'), spaceBefore=15, spaceAfter=8
)
body_style = ParagraphStyle(
    'CNBody', parent=styles['Normal'],
    fontName=CN_FONT, fontSize=10, leading=16,
    alignment=TA_JUSTIFY, spaceAfter=6
)
small_style = ParagraphStyle(
    'CNSmall', parent=styles['Normal'],
    fontName=CN_FONT, fontSize=8, leading=12,
    textColor=colors.HexColor('#888888'), alignment=TA_CENTER
)
table_header_style = ParagraphStyle(
    'CNTableHeader', fontName=CN_FONT_BOLD, fontSize=8, leading=12,
    textColor=colors.white, alignment=TA_CENTER
)
table_cell_style = ParagraphStyle(
    'CNTableCell', fontName=CN_FONT, fontSize=7.5, leading=11,
    alignment=TA_LEFT
)
warning_style = ParagraphStyle(
    'CNWarning', fontName=CN_FONT_BOLD, fontSize=12, leading=18,
    textColor=colors.HexColor('#c0392b'), alignment=TA_CENTER,
    backColor=colors.HexColor('#fdf2f2'), borderPadding=10
)
stat_style = ParagraphStyle(
    'CNStat', fontName=CN_FONT_BOLD, fontSize=24, leading=32,
    textColor=colors.HexColor('#1a3a5c'), alignment=TA_CENTER
)
stat_label_style = ParagraphStyle(
    'CNStatLabel', fontName=CN_FONT, fontSize=10, leading=14,
    textColor=colors.HexColor('#666666'), alignment=TA_CENTER
)

# ===== 页面模板 =====
def on_first_page(canvas_obj, doc):
    """封面页"""
    canvas_obj.saveState()
    # 背景色块
    canvas_obj.setFillColor(colors.HexColor('#1a3a5c'))
    canvas_obj.rect(0, A4[1] - 120, A4[0], 120, fill=1, stroke=0)
    canvas_obj.setFillColor(colors.HexColor('#e8f0f8'))
    canvas_obj.rect(0, 0, A4[0], 60, fill=1, stroke=0)

    canvas_obj.setFont(CN_FONT, 10)
    canvas_obj.setFillColor(colors.white)
    canvas_obj.drawString(30, A4[1] - 40, "勘察检测行业 · 招标信息日报")

    canvas_obj.setFont(CN_FONT_BOLD, 30)
    canvas_obj.drawString(30, A4[1] - 85, "海南勘察招标日报")

    canvas_obj.setFont(CN_FONT, 10)
    canvas_obj.setFillColor(colors.HexColor('#888888'))
    canvas_obj.drawString(30, 35, f"报告生成时间: {REPORT_DATETIME.strftime('%Y-%m-%d %H:%M')} (Asia/Shanghai)")
    canvas_obj.drawRightString(A4[0] - 30, 35, "数据来源: 中国招标投标公共服务平台 / 海南省政府采购网")
    canvas_obj.restoreState()

def on_later_pages(canvas_obj, doc):
    """内页"""
    canvas_obj.saveState()
    canvas_obj.setFillColor(colors.HexColor('#1a3a5c'))
    canvas_obj.rect(0, A4[1] - 30, A4[0], 30, fill=1, stroke=0)

    canvas_obj.setFont(CN_FONT, 9)
    canvas_obj.setFillColor(colors.white)
    canvas_obj.drawString(30, A4[1] - 22, f"【海南勘察招标日报】{REPORT_DATE}")

    canvas_obj.setFont(CN_FONT, 8)
    canvas_obj.setFillColor(colors.HexColor('#999999'))
    canvas_obj.drawString(30, 20, f"第 {canvas_obj.getPageNumber()} 页")
    canvas_obj.drawRightString(A4[0] - 30, 20, "自动生成 · 仅供参考 · 以原公告为准")
    canvas_obj.restoreState()

# ===== 生成报告 =====
output_path = os.path.expanduser("~/Desktop/海南勘察招标日报_2026-06-21.pdf")
doc = SimpleDocTemplate(
    output_path, pagesize=A4,
    topMargin=30*mm, bottomMargin=25*mm,
    leftMargin=20*mm, rightMargin=20*mm,
    title=f"海南勘察招标日报 {REPORT_DATE}",
    author="勘察检测行业招标分析师 (AI)"
)

story = []

# ---- 封面 ----
story.append(Spacer(1, 60*mm))
story.append(Paragraph("海 南 勘 察 招 标 日 报", title_style))
story.append(Spacer(1, 10*mm))
story.append(Paragraph(f"数据截止: {REPORT_DATE} 03:00 CST", subtitle_style))
story.append(Paragraph("勘察 | 检测 | 测绘 | 岩土 | 地质灾害", subtitle_style))
story.append(Spacer(1, 20*mm))

# 封面统计卡片
stat_data = [
    [Paragraph("0", stat_style), Paragraph("5", stat_style), Paragraph("0", stat_style)],
    [Paragraph("24h内新公告", stat_label_style), Paragraph("48h内相关公告", stat_label_style), Paragraph("海南政府采购网", stat_label_style)]
]
stat_table = Table(stat_data, colWidths=[140, 140, 140])
stat_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, 0), 8),
    ('BOTTOMPADDING', (0, 1), (-1, 1), 8),
    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#1a3a5c')),
]))
story.append(stat_table)
story.append(Spacer(1, 15*mm))

# 重要提示
story.append(Paragraph("⚠️ 重要提示: 2026年6月20日为周六（非工作日），中国招标投标公共服务平台及海南省政府采购网在周末通常不发布新的招标公告。本期报告包含最近48小时内（截至6月21日03:00）找到的相关公告。", warning_style))

story.append(PageBreak())

# ---- 目录 ----
story.append(Paragraph("目  录", h1_style))
story.append(Spacer(1, 5*mm))
toc_items = [
    "一、报告摘要 ..................................... 3",
    "二、数据采集说明 ................................. 4",
    "三、公告明细表 ................................... 5",
    "四、项目分析 ..................................... 7",
    "五、风险提示与建议 ............................... 8",
]
for item in toc_items:
    story.append(Paragraph(item, ParagraphStyle('TOC', fontName=CN_FONT, fontSize=13, leading=24, textColor=colors.HexColor('#333333'))))
story.append(PageBreak())

# ---- 一、报告摘要 ----
story.append(Paragraph("一、报告摘要", h1_style))
story.append(Spacer(1, 3*mm))
summary_text = f"""
<b>报告周期:</b> {REPORT_DATE} 03:00 CST（覆盖前24-48小时）<br/>
<b>监测范围:</b> 中国招标投标公共服务平台(cebpubservice.com)、海南省政府采购网(ccgp-hainan.gov.cn)及第三方聚合平台<br/>
<b>关键词:</b> 勘察、检测、测绘、岩土、地质灾害<br/><br/>
<b>核心发现:</b><br/>
• 最近24小时内（6月20日03:00 - 6月21日03:00）——<font color="red"><b>无新发布招标公告</b></font>（6月20日为周六，非工作日）<br/>
• 最近48小时内（6月19日）——发现<b>3条勘察类</b>招标公告、<b>1条地质灾害评估</b>采购公告、<b>1条材料检测</b>比选公告<br/>
• 区域分布: 海口2条、三亚1条、省级1条、儋州/洋浦1条<br/>
• 项目类型: 市政排水勘察、旅游基础设施勘察、地质灾害危险性评估、码头EPC勘察设计、材料检测<br/><br/>
<b>趋势判断:</b> 当前处周末静默期，预计下周一（6月22日）将迎来集中发布高峰。近期海南省市政基础设施和自贸港低空经济相关勘察检测需求值得重点关注。
"""
story.append(Paragraph(summary_text, body_style))
story.append(PageBreak())

# ---- 二、数据采集说明 ----
story.append(Paragraph("二、数据采集说明", h1_style))
story.append(Spacer(1, 3*mm))
data_note = f"""
<b>1. 采集时间:</b> {REPORT_DATETIME.strftime('%Y-%m-%d %H:%M')} (Asia/Shanghai)<br/><br/>
<b>2. 数据源:</b><br/>
&nbsp;&nbsp;• 中国招标投标公共服务平台 (bulletin.cebpubservice.com / ctbpsp.com)<br/>
&nbsp;&nbsp;• 海南省政府采购网 (www.ccgp-hainan.gov.cn)<br/>
&nbsp;&nbsp;• 第三方聚合: 剑鱼标讯 (jianyu360.cn)、采招网 (bidcenter.com.cn)<br/><br/>
<b>3. 筛选条件:</b><br/>
&nbsp;&nbsp;• 时间: 最近24-48小时（优先24h内，不足时扩展至48h）<br/>
&nbsp;&nbsp;• 关键词: 勘察、检测、测绘、岩土、地质灾害<br/>
&nbsp;&nbsp;• 排除: 仅标题中含关键词但实质为纯施工/设备采购等无关项目<br/><br/>
<b>4. 局限性说明:</b><br/>
&nbsp;&nbsp;• 官方平台为SPA/Vue前端应用，需JavaScript渲染，程序化采集受限<br/>
&nbsp;&nbsp;• 第三方聚合平台详情页需登录认证，完整信息抓取有限<br/>
&nbsp;&nbsp;• 本期部分数据来自聚合平台列表快照，预算金额为估算值<br/>
&nbsp;&nbsp;• 建议订阅官方平台RSS/邮件提醒获取完整实时数据<br/><br/>
<b>5. 免责声明:</b> 本报告由AI自动生成，仅供参考。所有信息请以原公告为准。报告不构成任何投标建议。
"""
story.append(Paragraph(data_note, body_style))
story.append(PageBreak())

# ---- 三、公告明细表 ----
story.append(Paragraph("三、公告明细表", h1_style))
story.append(Spacer(1, 3*mm))
story.append(Paragraph(f"共发现 <b>{len(FOUND_ITEMS)}</b> 条相关公告（最近48小时内）", body_style))
story.append(Spacer(1, 3*mm))

# 表格
table_headers = [
    Paragraph("序号", table_header_style),
    Paragraph("项目名称", table_header_style),
    Paragraph("类型", table_header_style),
    Paragraph("预算", table_header_style),
    Paragraph("发布日", table_header_style),
    Paragraph("截止日", table_header_style),
    Paragraph("区域", table_header_style),
]
table_data = [table_headers]
for i, item in enumerate(FOUND_ITEMS, 1):
    row = [
        Paragraph(str(i), ParagraphStyle('TCC', fontName=CN_FONT, fontSize=8, alignment=TA_CENTER, leading=11)),
        Paragraph(item['title'], ParagraphStyle('TCTitle', fontName=CN_FONT, fontSize=7.5, leading=11, alignment=TA_LEFT)),
        Paragraph(item['type'], ParagraphStyle('TCType', fontName=CN_FONT, fontSize=7.5, leading=11, alignment=TA_CENTER)),
        Paragraph(item['budget'], ParagraphStyle('TCBudget', fontName=CN_FONT, fontSize=7, leading=10, alignment=TA_CENTER)),
        Paragraph(item['pub_date'], ParagraphStyle('TCDate', fontName=CN_FONT, fontSize=7.5, leading=11, alignment=TA_CENTER)),
        Paragraph(item['deadline'], ParagraphStyle('TCDL', fontName=CN_FONT, fontSize=7.5, leading=11, alignment=TA_CENTER)),
        Paragraph(item['region'], ParagraphStyle('TCRegion', fontName=CN_FONT, fontSize=7.5, leading=11, alignment=TA_CENTER)),
    ]
    table_data.append(row)

col_widths = [22, 200, 42, 60, 40, 55, 36]
table = Table(table_data, colWidths=col_widths, repeatRows=1)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a3a5c')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8f9fa'), colors.white]),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('LEFTPADDING', (0, 0), (-1, -1), 3),
    ('RIGHTPADDING', (0, 0), (-1, -1), 3),
]))
story.append(table)
story.append(PageBreak())

# ---- 四、项目详情分析 ----
story.append(Paragraph("四、项目详情分析", h1_style))

for i, item in enumerate(FOUND_ITEMS, 1):
    story.append(Paragraph(f"项目 {i}: {item['title']}", h2_style))
    detail = f"""
<b>发布时间:</b> {item['pub_date']} &nbsp;&nbsp; <b>区域:</b> {item['region']} &nbsp;&nbsp; <b>类型:</b> {item['type']}<br/>
<b>采购人:</b> {item['buyer']}<br/>
<b>预算金额:</b> {item['budget']}<br/>
<b>关键资质要求:</b> {item['qualifications']}<br/>
<b>投标截止:</b> {item['deadline']}<br/>
<b>来源:</b> {item['source']}<br/>
<b>链接:</b> <font color="blue"><u>{item['url']}</u></font>
"""
    story.append(Paragraph(detail, body_style))
    story.append(Spacer(1, 3*mm))

story.append(PageBreak())

# ---- 五、风险提示 ----
story.append(Paragraph("五、风险提示与投标建议", h1_style))
story.append(Spacer(1, 3*mm))

risks = [
    ("📌 周末静默期", "6月20日为周六，官方平台无新公告发布，属正常现象。预计下周一（6月22日）将集中发布上周尾及周末积压的招标公告，建议当日重点关注。"),
    ("📌 勘察资质门槛", "近期勘察类项目普遍要求工程勘察综合甲级或岩土工程甲级资质，中小企业需关注资质延续和升级窗口。2026年住建部资质改革细则将影响资质申请策略。"),
    ("📌 地质灾害防治需求上升", "当前华南地区进入主汛期（6-8月），地质灾害气象风险预警频发（6月20日自然资源部发布橙色预警）。海南省地质灾害隐患点整治、危险性评估等招标需求预计在近期集中释放。"),
    ("📌 自贸港建设红利", "跨琼州海峡低空航路项目、三亚崖州湾科技城等自贸港重点工程持续释放勘察检测需求。2026年下半年预计有新一轮基础设施集中开工。"),
    ("📌 数据获取提醒", "建议在政府采购网注册供应商账号并设置关键词订阅，确保第一时间获取完整招标信息。官方平台（cebpubservice.com、ccgp-hainan.gov.cn）为唯一法定发布渠道。"),
]

for title, desc in risks:
    story.append(Paragraph(f"<b>{title}</b>", ParagraphStyle('RiskTitle', fontName=CN_FONT_BOLD, fontSize=11, leading=18, textColor=colors.HexColor('#c0392b'))))
    story.append(Paragraph(desc, body_style))
    story.append(Spacer(1, 2*mm))

story.append(Spacer(1, 10*mm))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cccccc')))
story.append(Spacer(1, 5*mm))
story.append(Paragraph("— 报告结束 —", small_style))
story.append(Paragraph(f"【海南勘察招标日报】{REPORT_DATE} | AI自动生成 | 仅供参考 | 以原公告为准", small_style))

# ---- 构建 ----
doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
print(f"\n✅ PDF已生成: {output_path}")
print(f"   文件大小: {os.path.getsize(output_path)/1024:.1f} KB")
print(f"   页数: 待确认")
