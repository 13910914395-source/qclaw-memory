# -*- coding: utf-8 -*-
"""生成《海南勘察招标日报》PDF（WPS兼容，CJK子集嵌入）。"""
import base64
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
pdfmetrics.registerFont(TTFont("CJK", FONT))

# ---- 颜色 ----
NAVY = colors.HexColor("#1F3864")
BLUE = colors.HexColor("#2E75B6")
LIGHT = colors.HexColor("#D9E2F3")
GREY = colors.HexColor("#595959")
WARN = colors.HexColor("#C00000")

# ---- 样式 ----
ss = getSampleStyleSheet()
def mk(name, **kw):
    kw.setdefault("fontName", "CJK")
    return ParagraphStyle(name, parent=ss["Normal"], **kw)

style_title = mk("t", fontSize=22, leading=28, textColor=colors.white,
                alignment=TA_CENTER, spaceAfter=4)
style_sub = mk("s", fontSize=12, leading=16, textColor=colors.white,
               alignment=TA_CENTER)
style_h1 = mk("h1", fontSize=15, leading=20, textColor=NAVY, spaceBefore=10, spaceAfter=6)
style_h2 = mk("h2", fontSize=12, leading=16, textColor=BLUE, spaceBefore=8, spaceAfter=4)
style_body = mk("b", fontSize=10, leading=15, spaceAfter=4)
style_small = mk("sm", fontSize=8.5, leading=12, textColor=GREY)
style_cell = mk("c", fontSize=8.5, leading=11)
style_cellh = mk("ch", fontSize=8.5, leading=11, textColor=colors.white, alignment=TA_CENTER)
style_warn = mk("w", fontSize=12, leading=17, textColor=WARN, alignment=TA_CENTER, spaceAfter=4)
style_note = mk("n", fontSize=9.5, leading=14, spaceAfter=3)

DATE = "2026-08-27"
WIN_START = "2026-08-26 03:00"
WIN_END = "2026-08-27 03:00"
GEN = "2026-08-27 03:00（北京时间）"

story = []

# ===== 封面 =====
banner = Table([[Paragraph("海南勘察招标日报", style_title)],
                [Paragraph("勘察 · 检测 · 测绘 · 岩土 · 地质灾害  招标信息日报", style_sub)]],
               colWidths=[520])
banner.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), NAVY),
    ("TOPPADDING", (0,0), (-1,-1), 14),
    ("BOTTOMPADDING", (0,0), (-1,-1), 14),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
]))
story.append(banner)
story.append(Spacer(1, 18))
story.append(Paragraph(f"报告日期：{DATE}（星期四）", style_body))
story.append(Paragraph(f"数据窗口：{WIN_START} ~ {WIN_END}（北京时间，最近24小时）", style_body))
story.append(Paragraph("抓取平台：中国招标投标公共服务平台 (www.cebpubservice.com)　|　海南省政府采购网 (www.ccgp-hainan.gov.cn)", style_body))
story.append(Paragraph("关键词：勘察 / 检测 / 测绘 / 岩土 / 地质灾害", style_body))
story.append(Paragraph(f"生成时间：{GEN}", style_small))
story.append(Spacer(1, 16))

# 重要提示框
notice = Table([[Paragraph("⚠ 重要提示：近期无新发布招标信息", style_warn)],
                [Paragraph(
    "在本书规定的数据窗口（2026-08-26 03:00 至 2026-08-27 03:00，北京时间）内，"
    "通过当前可用的数据访问方式，未能从指定两个平台核实到任何满足关键词"
    "（勘察/检测/测绘/岩土/地质灾害）且发布时间在最近24小时内的招标公告。"
    "因此，本周期正式抓取结果为 <b>0 条</b>。", style_note)],
                [Paragraph(
    "说明：本次抓取受运行环境网络策略限制（目标站点需浏览器/登录态或反爬校验，"
    "实时接口不可直连），数据以公开检索缓存快照为参考。如需每日精准推送，"
    "建议在可直连内网/已登录浏览器环境部署定时抓取任务。", style_small)]],
               colWidths=[520])
notice.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#FCE4E4")),
    ("BOX", (0,0), (-1,-1), 1, WARN),
    ("LEFTPADDING", (0,0), (-1,-1), 10),
    ("RIGHTPADDING", (0,0), (-1,-1), 10),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("ALIGN", (0,0), (-1,0), "CENTER"),
]))
story.append(notice)
story.append(PageBreak())

# ===== 目录 =====
story.append(Paragraph("目录", style_h1))
toc = [
    "一、数据抓取范围与方法",
    "二、最近24小时公告清单（本周期抓取结果）",
    "三、近期相关参考公告（超出24h窗口，供持续关注）",
    "四、风险提示",
    "五、方法论与数据来源说明",
    "附录：数据来源链接",
]
for t in toc:
    story.append(Paragraph(t, style_body))
story.append(PageBreak())

# ===== 一、抓取范围与方法 =====
story.append(Paragraph("一、数据抓取范围与方法", style_h1))
story.append(Paragraph("• 平台一：中国招标投标公共服务平台（www.cebpubservice.com）—— 全国招标公告聚合平台。", style_body))
story.append(Paragraph("• 平台二：海南省政府采购网（www.ccgp-hainan.gov.cn）—— 海南省本级及市县政府采购公告。", style_body))
story.append(Paragraph("• 关键词集合：勘察、检测、测绘、岩土、地质灾害。", style_body))
story.append(Paragraph(f"• 时间筛选：仅保留发布时间 ∈ [{WIN_START}, {WIN_END}] 的公告，过滤全部旧数据。", style_body))
story.append(Paragraph("• 目标条数：各平台取满足时间条件的最新公告（任务目标各50条，满足即收录）。", style_body))
story.append(Paragraph("• 去重与智能识别：合并两平台重复项；剔除仅含关键词字样但实质无关的“伪勘察”项目（如纯办公维修、非技术类服务）。", style_body))

# ===== 二、24h清单 =====
story.append(Paragraph("二、最近24小时公告清单（本周期抓取结果）", style_h1))
hdr = ["序号","项目名称","采购人/单位","发布时间","预算/限价","截止日期","资质要求"]
rows = hdr
data = [rows,
        [Paragraph("本数据窗口内（%s ~ %s）未核实到符合条件的公告，本周期抓取结果 <b>0 条</b>。" % (WIN_START, WIN_END),
                   mk("empty", fontSize=10, leading=14, textColor=WARN, alignment=TA_CENTER))]]
tbl = Table(data, colWidths=[28,122,80,54,56,56,124])
tbl.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), NAVY),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,-1), "CJK"),
    ("FONTSIZE", (0,0), (-1,-1), 8.5),
    ("SPAN", (0,1), (-1,1)),
    ("BOX", (0,0), (-1,-1), 0.8, NAVY),
    ("INNERGRID", (0,0), (-1,0), 0.5, colors.white),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ("LEFTPADDING", (0,0), (-1,-1), 5),
    ("RIGHTPADDING", (0,0), (-1,-1), 5),
]))
story.append(tbl)
story.append(Spacer(1, 6))
story.append(Paragraph("注：上文“三、近期相关参考公告”所列项目均超出24小时窗口，不计入本周期抓取结果，仅供持续关注。", style_small))

# ===== 三、参考公告 =====
story.append(Paragraph("三、近期相关参考公告（超出24h窗口，供持续关注，不计入本日报）", style_h1))
story.append(Paragraph("以下为检索到的海南省近期（非本24h窗口）勘察/检测/测绘/岩土/地质灾害类项目，"
                       "仅供业务跟踪参考，截止日期与预算以原公告为准。", style_small))

ref_hdr = ["#","项目名称","采购人/单位","发布","预算/限价","截止","资质要求(摘要)"]
ref = [
    ["1","海南岛**海域微细粒砂矿综合回收技术优化服务(二次)采购公告","海南省海洋地质调查院","08-24","未披露","2026-09-07 09:00","海洋地质勘查/砂矿回收技术；邮箱报名"],
    ["2","海南省特种设备检验检测设备更新项目（公开招标）","海南省本级","08-19","未披露","详见公告","特种设备检验检测机构资质"],
    ["3","海南省2026年生产建设项目水土保持方案评审和质量管理及水土流失治理成效核查(二次)","海南省本级","08-19","未披露","详见公告","水土保持/监测相关"],
    ["4","海南省2026年水土保持遥感信息化监管及水土流失动态监测","海南省本级","07-23","未披露","详见公告","遥感监测/测绘"],
    ["5","三亚市地质灾害隐患再排查项目技术服务","三亚市自然资源和规划局","08-06","380,349.67元","报名期内","地质灾害评估和治理工程勘查设计甲级"],
    ["6","三亚市吉阳区太阳湾路沿线地质灾害及道路安全隐患排查项目","三亚市自然资源和规划局","08-06","未披露","2026-08-12","地灾评估甲级 + 建设工程质量检测(道路)资质"],
    ["7","万宁市南桥镇南林居项目地块地质灾害危险性评估单位遴选","万宁市南桥镇政府","07-30","控制价6万元","2026-08-07","地灾评估/治理工程勘查设计乙级及以上"],
    ["8","海南昌江等8市县地质灾害三查与监测预警示范(2026年度)专题研究","海南省地质调查院","05-25","12.93万元","询价期","地质灾害监测仪器设备/相关业绩"],
    ["9","五指山市畅好乡-水满乡1:1万地质灾害精细化调查岩矿测试","海南省自然资源和规划厅","05-29","13.16万元","服务期至2026-10-30","计量认证(CMA)资质"],
    ["10","琼海市2026年城镇老旧小区改造项目勘察(含物探)招标公告","琼海市(招标代理)","07-28","未披露","2026-08-19 08:30","工程勘察资质(含物探)"],
]
ref_rows = [[Paragraph(c, style_cellh) for c in ref_hdr]]
for r in ref:
    ref_rows.append([Paragraph(r[0], style_cell), Paragraph(r[1], style_cell),
                     Paragraph(r[2], style_cell), Paragraph(r[3], style_cell),
                     Paragraph(r[4], style_cell), Paragraph(r[5], style_cell),
                     Paragraph(r[6], style_cell)])
rtbl = Table(ref_rows, colWidths=[22,140,82,42,56,62,116], repeatRows=1)
rtbl.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), NAVY),
    ("FONTNAME", (0,0), (-1,-1), "CJK"),
    ("FONTSIZE", (0,0), (-1,-1), 8.5),
    ("BOX", (0,0), (-1,-1), 0.8, NAVY),
    ("INNERGRID", (0,0), (-1,-1), 0.4, colors.HexColor("#BFBFBF")),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F2F6FC")]),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("LEFTPADDING", (0,0), (-1,-1), 4),
    ("RIGHTPADDING", (0,0), (-1,-1), 4),
]))
story.append(rtbl)

# ===== 四、风险提示 =====
story.append(Paragraph("四、风险提示", style_h1))
risks = [
    "数据窗口内无新公告，建议次日同一时点复查，避免遗漏凌晨后补发项目。",
    "省地质局门户(geo.hainan.gov.cn)发布的海洋地质勘查类项目“海南岛**海域微细粒砂矿综合回收技术优化服务(二次)”于 2026-08-24 发布、2026-09-07 09:00 截止，时间较紧，相关供应商应优先关注。",
    "地质灾害类项目普遍要求“地质灾害评估和治理工程勘查设计甲级/乙级”资质，且岩矿/水土检测常需 CMA 计量认证；投标前务必核验资质等级、有效期与人员证书（如 CAAC 飞手执照、注册岩土工程师等）。",
    "三亚、万宁等市县项目预算较小（数万至数十万元）但资质门槛高，适合具备专项资质的中小企业精准切入。",
    "本参考列表非实时核实，所有截止日期、预算、资质以原公告正文为准；链接见附录。",
]
for r in risks:
    story.append(Paragraph("• " + r, style_body))

# ===== 五、方法论与来源 =====
story.append(Paragraph("五、方法论与数据来源说明", style_h1))
story.append(Paragraph("• 访问限制：运行环境对目标站点实施 SSRF/反爬策略——浏览器主机名与 IP 导航均被阻断，"
                       "web_fetch 无法解析 ccgp-hainan.gov.cn 域名，cebpubservice.com 实时数据接口返回 404。"
                       "本次数据基于公开检索缓存快照，无法 100% 排除两平台在 24h 窗口内确有发布但未被缓存索引的公告。", style_body))
story.append(Paragraph("• 改进建议：在具备直连/已登录浏览器环境部署定时抓取；或接入两平台官方“信息API / 订阅推送”能力，"
                       "以实现精确的最近24小时日报。", style_body))
story.append(Paragraph("• 智能识别：已对关键词命中项做实质判断，排除纯办公维修、非技术类服务等“伪勘察”项目；"
                       "本周期无满足24h条件的真实勘察类项目。", style_body))

# 附录链接
story.append(Paragraph("附录：数据来源链接", style_h2))
links = [
    "1. 海南岛**海域微细粒砂矿综合回收技术优化服务(二次)：https://geo.hainan.gov.cn/sdzj/0400/202608/48d1f7b8695b4164aa09cbccd5c947c5.shtml",
    "2. 海南省特种设备检验检测设备更新项目（2026-08-19 列表）：https://www.ccgp-hainan.gov.cn/cgw/cgw_show.jsp?id=14889",
    "3. 三亚市地质灾害隐患再排查项目：https://zgj.sanya.gov.cn/zgjsite/ttxw/202608/61fd0c78ba5749c88380a470adba90b2.shtml",
    "4. 三亚市吉阳区太阳湾路沿线地灾及道路安全隐患排查：https://zgj.sanya.gov.cn/zgjsite/tzgg/202608/cbd8a36487e84f039409fbc0b0fd597c.shtml",
    "5. 万宁市南桥镇地块地质灾害危险性评估：https://wanning.hainan.gov.cn/zfxxgk/sgxzgk/xzz/gkml/202607/t20260730_4119687.html",
    "6. 海南昌江等8市县地质灾害三查与监测预警示范：https://geo.hainan.gov.cn/sdzj/0400/202605/cb974f3c238f4a17a0c5e9e057357ae6.shtml",
    "7. 五指山市1:1万地灾精细化调查岩矿测试：https://lr.hainan.gov.cn/xxgk_317/0200/0202/202605/t20260529_4083794.html",
    "8. 琼海市老旧小区改造项目勘察(含物探)：https://ggzy.hainan.gov.cn/ggzy/qhggzy/GGjxzbgs1/288509.jhtml",
]
for l in links:
    story.append(Paragraph(l, style_small))

# ===== 页脚/页码 =====
def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("CJK", 7.5)
    canvas.setFillColor(GREY)
    canvas.drawString(36, 16, "海南勘察招标日报 · 自动生成 · 数据窗口 %s~%s" % (WIN_START, WIN_END))
    canvas.drawRightString(A4[0]-36, 16, "第 %d 页" % doc.page)
    canvas.setStrokeColor(colors.HexColor("#BFBFBF"))
    canvas.line(36, 22, A4[0]-36, 22)
    canvas.restoreState()

doc = SimpleDocTemplate(
    "/Users/fasimac/.qclaw/workspace/海南勘察招标日报_2026-08-27.pdf",
    pagesize=A4, leftMargin=36, rightMargin=36, topMargin=30, bottomMargin=28,
    title="海南勘察招标日报 2026-08-27", author="OpenClaw 招标分析")
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)

# base64
with open("/Users/fasimac/.qclaw/workspace/海南勘察招标日报_2026-08-27.pdf", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("ascii")
with open("/Users/fasimac/.qclaw/workspace/海南勘察招标日报_2026-08-27.b64.txt", "w", encoding="utf-8") as f:
    f.write(b64)
print("PDF bytes:", len(base64.b64decode(b64)))
print("B64 chars:", len(b64))
print("OK")
