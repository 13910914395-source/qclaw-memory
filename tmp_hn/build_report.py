# -*- coding: utf-8 -*-
"""生成【海南勘察招标日报】PDF（WPS 兼容：嵌入 CJK TrueType 字体，PDF 1.4）"""
import io, json, os, re, datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, KeepTogether,
                                NextPageTemplate)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hainan_kancha_daily.pdf")
REPORT_DATE = "2026-08-29"
WINDOW = "2026-08-28 03:00 ~ 2026-08-29 03:00 (Asia/Shanghai)"
GEN_AT = "2026-08-29 03:00"

# ---------- 字体（嵌入，覆盖中英文全部字符集） ----------
FONT_R, FONT_B = "CJK", "CJKB"
pdfmetrics.registerFont(TTFont(FONT_R, "/System/Library/Fonts/STHeiti Light.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont(FONT_B, "/System/Library/Fonts/STHeiti Medium.ttc", subfontIndex=0))
pdfmetrics.registerFontFamily(FONT_R, normal=FONT_R, bold=FONT_B, italic=FONT_R, boldItalic=FONT_B)

CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
def clean(s):
    return CTRL.sub("", str(s if s is not None else "")).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---------- 样式 ----------
S = {
    "cover_kicker": ParagraphStyle("ck", fontName=FONT_R, fontSize=11, leading=18,
                                   textColor=colors.HexColor("#7A8699"), alignment=1),
    "cover_title": ParagraphStyle("ct", fontName=FONT_B, fontSize=27, leading=40,
                                  textColor=colors.HexColor("#0F2E5A"), alignment=1),
    "cover_sub": ParagraphStyle("cs", fontName=FONT_R, fontSize=13, leading=22,
                                textColor=colors.HexColor("#264C7A"), alignment=1),
    "cover_meta": ParagraphStyle("cm", fontName=FONT_R, fontSize=9.5, leading=17,
                                 textColor=colors.HexColor("#5A6675")),
    "h1": ParagraphStyle("h1", fontName=FONT_B, fontSize=15, leading=24,
                         textColor=colors.HexColor("#0F2E5A"), spaceBefore=6, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName=FONT_B, fontSize=11.5, leading=19,
                         textColor=colors.HexColor("#1A4C86"), spaceBefore=8, spaceAfter=4),
    "body": ParagraphStyle("b", fontName=FONT_R, fontSize=9.5, leading=16,
                           textColor=colors.HexColor("#22272E")),
    "small": ParagraphStyle("s", fontName=FONT_R, fontSize=8, leading=13,
                            textColor=colors.HexColor("#5A6675")),
    "link": ParagraphStyle("l", fontName=FONT_R, fontSize=7.5, leading=12,
                           textColor=colors.HexColor("#1155CC")),
    "toc": ParagraphStyle("t", fontName=FONT_R, fontSize=10.5, leading=22,
                          textColor=colors.HexColor("#22272E")),
    "th": ParagraphStyle("th", fontName=FONT_B, fontSize=8.5, leading=12,
                         textColor=colors.white, alignment=1),
    "td": ParagraphStyle("td", fontName=FONT_R, fontSize=8, leading=11.5,
                         textColor=colors.HexColor("#22272E")),
    "tdc": ParagraphStyle("tdc", fontName=FONT_R, fontSize=8, leading=11.5,
                          textColor=colors.HexColor("#22272E"), alignment=1),
    "warn": ParagraphStyle("w", fontName=FONT_R, fontSize=9.5, leading=16,
                           textColor=colors.HexColor("#8A3A00")),
}

# ---------- 数据 ----------
HN = "https://ccgp-hainan.gov.cn/articleHn?type=notice&id={id}&channel={ch}"
CH_GG = "c5bff13f-21ca-4dac-b158-cb40accd3035"   # 公告信息
CH_GS = "6d48e0f7-8dff-412f-9f89-83f01a2d296f"   # 公示信息

def link(i, ch):
    return HN.format(id=i, ch=ch)

ITEMS = [
 {
  "rank": "★★★★★",
  "name": "2026年度高管中心桥梁及隧道初始、定期检测项目（采购意向）",
  "budget": "1,000.00 万元",
  "buyer": "海南省公路管理局高速公路养护管理中心",
  "agency": "采购人自行公开（尚未确定代理机构）",
  "qual": "预判需具备：①公路水运工程试验检测机构等级证书（桥梁隧道工程专项，建议综合/专项甲级）；②公路水运工程试验检测师（桥梁隧道专业）注册证书；③桥梁检测车、无损检测（超声/回弹/雷达）、隧道衬砌检测雷达等设备清单；④同类国省干线桥隧定期检测业绩。公告未列明具体资质条款，需待正式招标文件确认。",
  "deadline": "预计采购时间 2026 年 09 月（意向阶段，无投标截止日）",
  "pub": "2026-08-28 10:12",
  "type": "采购意向",
  "url": link("9ef97f91-7983-4256-b760-0eed87566cf0", CH_GS),
  "note": "本期唯一千万级、且与勘察检测主业强相关的线索。国省干线桥梁+隧道初始检测与定期检测打包，属交通基础设施检测赛道核心标的。建议立即启动资质自查与联合体伙伴摸排，9 月正式挂网后争取第一时间响应。",
 },
 {
  "rank": "★★★☆☆",
  "name": "2026年东方市环境空气自动监测系统、VOCs／臭气／网格化监测及污染物溯源分析、非甲烷总烃监测系统委托第三方运维（合同公告）",
  "budget": "172.00 万元",
  "buyer": "东方市生态环境监测站",
  "agency": "—（合同编号 HNXHY2026-011）",
  "qual": "环境类第三方运维通常要求：CMA 检验检测机构资质认定（环境空气/废气相应参数）、自动监测设备运维业绩、驻场技术人员（环境监测工程师）配置。",
  "deadline": "已签订合同（本期为结果类信息，仅供对标）",
  "pub": "2026-08-28 22:24",
  "type": "合同公告",
  "url": link("07d8df05-9f48-41db-822c-a6bf439c1605", CH_GS),
  "note": "反映海南地市级生态环境监测运维单价区间；同类项目在海口、三亚、儋州等地存在年度续采规律，可作为明年跟标目标。",
 },
 {
  "rank": "★★★☆☆",
  "name": "海南省市场监督管理局 2026 年流通领域产品质量监督抽查项目（二次）结果公告 + 4 份合同公告",
  "budget": "结果公告 80.00 万元；合同 54.00／53.00／53.00／50.00 万元",
  "buyer": "海南省市场监督管理局",
  "agency": "海南省政府采购中心",
  "qual": "CMA 检验检测机构资质认定证书（须覆盖抽查产品目录对应参数）、抽样人员资质、实验室能力验证记录。",
  "deadline": "已开标／已签约（结果类）",
  "pub": "2026-08-28 08:40 ~ 17:00",
  "type": "结果公告／合同公告",
  "url": link("4dbe6866-6d3a-4624-b079-12981d909c0b", CH_GG),
  "note": "省级流通领域质量抽查为检测机构稳定年度盘子，本期一次性释放 5 条结果/合同信息，单包 50~54 万元，合计约 210 万元。建议整理中标机构名单，评估明年竞争格局。",
 },
 {
  "rank": "★★☆☆☆",
  "name": "三亚市 2026 年度市级产品质量监督抽查项目（二次）履约验收公告（第 1 批，两包）",
  "budget": "39.02 万元 + 37.01 万元",
  "buyer": "三亚市市场监督管理局",
  "agency": "海南天时利工程咨询有限公司",
  "qual": "CMA 资质（对应抽查品类参数）、抽样与判定能力。",
  "deadline": "已履约验收（结果类）",
  "pub": "2026-08-28 10:59",
  "type": "履约验收公告",
  "url": link("2157513a-1cdb-4592-b0d1-499733cdf2d8", CH_GS),
  "note": "市级抽查体量约为省级的 70%，代理机构为海南天时利，可作为渠道维护对象。",
 },
 {
  "rank": "★★☆☆☆",
  "name": "海南省林业局全省林草资源动态监管项目（2026 年）政府采购合同公告",
  "budget": "44.20 万元",
  "buyer": "海南省林业局",
  "agency": "—（中标供应商：自然资源部第四航测遥感院）",
  "qual": "测绘资质（甲级）／遥感影像判读与变更监测能力；成果需符合自然资源调查监测技术规程。",
  "deadline": "已签订合同（结果类）",
  "pub": "2026-08-28 15:01",
  "type": "合同公告",
  "url": link("a691ef29-821e-4d52-bd8d-d068e6364ce3", CH_GS),
  "note": "测绘/遥感类项目被部属院所拿下，说明省级资源监测类标的对甲级测绘资质与遥感专业能力门槛较高，本地民营测绘企业宜走分包或联合体路径。",
 },
 {
  "rank": "★☆☆☆☆",
  "name": "三亚市自然资源和规划局房地产土地评估服务（直接选定）政府采购合同公告",
  "budget": "0.79 万元",
  "buyer": "三亚市自然资源和规划局",
  "agency": "—",
  "qual": "土地/房地产估价资质；合同履行地址位于海口测绘大厦（供应商侧）。",
  "deadline": "已签订合同（结果类）",
  "pub": "2026-08-28 10:41",
  "type": "合同公告",
  "url": link("c0cd1a24-de7b-46b3-bd51-ad8255a17c3f", CH_GS),
  "note": "金额极小，仅作测绘/不动产相邻业务面观察，无投标价值。",
 },
 {
  "rank": "☆☆☆☆☆",
  "name": "传染病病原监测试剂耗材采购项目（公开招标）",
  "budget": "120.21 万元",
  "buyer": "海南省疾病预防控制中心",
  "agency": "海南政采招投标有限公司",
  "qual": "医疗器械/体外诊断试剂经营资质（非工程勘察检测资质）。",
  "deadline": "详见原文（招标公告，本期在库）",
  "pub": "2026-08-28 16:24",
  "type": "公开招标招标公告",
  "url": link("e2969d3a-eb59-4722-912c-025562de2230", CH_GG),
  "note": "关键词命中「监测」但实质为试剂耗材货物采购，判定为无关项目，仅列出以说明去噪过程。",
 },
 {
  "rank": "☆☆☆☆☆",
  "name": "海南省综合行政执法平台（二期）采购更正公告（第一次）",
  "budget": "1,334.97 万元",
  "buyer": "海南省司法厅",
  "agency": "海南中廉招标有限公司",
  "qual": "软件开发/系统集成类；正文含「检测」字样但指软件测试环节。",
  "deadline": "详见更正后原文",
  "pub": "2026-08-28 19:30",
  "type": "更正公告",
  "url": link("a8cb9381-a119-48f2-a62a-580546f67f3f", CH_GG),
  "note": "典型「伪命中」样本：金额大但与勘察检测主业无关，已剔除出机会池。",
 },
]

NAT = [
 ("中信银行深圳分行票据及凭证传递服务采购项目延期公告", "广东省", "更正公告", "2026-08-29"),
 ("深圳机场建设工程第三方安全质量咨询服务项目（2026-2028年）中标结果公示", "广东省", "中标结果公示", "2026-08-29"),
 ("深圳市宝排水质检测中心有限公司2026年检测技术服务采购项目中标结果公示", "广东省", "中标结果公示", "2026-08-29"),
 ("宝能城花园（西区）架空层开发商历史遗留未完工区域续建工程中标结果公示", "广东省", "中标结果公示", "2026-08-29"),
 ("深圳机场T3航站楼边检入境智能化高清监控改造项目中标结果公示", "广东省", "中标结果公示", "2026-08-29"),
 ("深圳市罗湖区田心大厦小区78户外墙渗水物业维修工程结果公示", "广东省", "中标结果公示", "2026-08-29"),
 ("昆明航空有限公司2026年度食堂食品A类原材料-调料粮油采购项目(二次)中标结果公示", "云南/广东", "中标结果公示", "2026-08-29"),
 ("中国电信股份有限公司自贡分公司2026年某单位数据采集服务采购项目（第二次）成交候选人公示", "四川省", "中标候选人公示", "2026-08-29"),
 ("2026 年中国电信梧州分公司光模块采购项目成交候选人公示", "广西壮族自治区", "中标候选人公示", "2026-08-29"),
 ("滨州市城区排水防涝能力提升工程（一期）评标结果公示", "山东省", "中标候选人公示", "2026-08-29"),
]

# ---------- 文档 ----------
class Doc(BaseDocTemplate):
    def __init__(self, path):
        BaseDocTemplate.__init__(self, path, pagesize=A4,
                                 leftMargin=18*mm, rightMargin=18*mm,
                                 topMargin=16*mm, bottomMargin=16*mm,
                                 title="【海南勘察招标日报】%s" % REPORT_DATE,
                                 author="勘察检测行业招标分析（QClaw 自动生成）",
                                 subject="海南省勘察/检测/测绘/岩土/地质灾害类招标信息日报")
        fw, fh = self.width, self.height
        cover = Frame(self.leftMargin, self.bottomMargin, fw, fh, id="cover")
        body = Frame(self.leftMargin, self.bottomMargin, fw, fh, id="body")
        self.addPageTemplates([
            PageTemplate(id="Cover", frames=[cover], onPage=self._cover_deco),
            PageTemplate(id="Body", frames=[body], onPage=self._footer),
        ])

    def _cover_deco(self, c, d):
        c.saveState()
        c.setFillColor(colors.HexColor("#0F2E5A"))
        c.rect(0, A4[1]-14*mm, A4[0], 14*mm, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#C9A227"))
        c.rect(0, A4[1]-16*mm, A4[0], 2*mm, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#0F2E5A"))
        c.rect(0, 0, A4[0], 8*mm, stroke=0, fill=1)
        c.setFont(FONT_R, 7.5)
        c.setFillColor(colors.white)
        c.drawCentredString(A4[0]/2, 3*mm, "本报告由自动化采集与人工规则筛选生成，投标决策前请核对原文公告")
        c.restoreState()

    def _footer(self, c, d):
        c.saveState()
        c.setStrokeColor(colors.HexColor("#D5DCE5"))
        c.setLineWidth(0.5)
        c.line(18*mm, 13*mm, A4[0]-18*mm, 13*mm)
        c.setFont(FONT_R, 7.5)
        c.setFillColor(colors.HexColor("#6B7684"))
        c.drawString(18*mm, 8.5*mm, "【海南勘察招标日报】%s · 数据窗口 %s" % (REPORT_DATE, WINDOW))
        c.drawRightString(A4[0]-18*mm, 8.5*mm, "第 %d 页 · 生成于 %s" % (c.getPageNumber()-1, GEN_AT))
        c.restoreState()


def hdr(cells):
    return [Paragraph(clean(x), S["th"]) for x in cells]


def main():
    doc = Doc(OUT)
    F = []

    # ===== 封面 =====
    F.append(Spacer(1, 46*mm))
    F.append(Paragraph("勘察 · 检测 · 测绘 · 岩土 · 地质灾害", S["cover_kicker"]))
    F.append(Spacer(1, 5*mm))
    F.append(Paragraph("【海南勘察招标日报】", S["cover_title"]))
    F.append(Paragraph(REPORT_DATE, S["cover_title"]))
    F.append(Spacer(1, 6*mm))
    F.append(Paragraph("近 24 小时招标信息采集与机会筛选报告", S["cover_sub"]))
    F.append(Spacer(1, 24*mm))
    meta = [
        ["报告日期", REPORT_DATE + "（星期六）"],
        ["数据窗口", WINDOW],
        ["数据来源", "① 海南省政府采购网 ccgp-hainan.gov.cn（公告信息 + 公示信息，全量时间筛选）\n② 中国招标投标公共服务平台 cebpubservice.com / ctbpsp.com（部分受限，见第 1 章说明）"],
        ["采集总量", "海南省政府采购网 167 条（窗口内全量，已去重）；国家平台最新公告 10 条"],
        ["关键词命中", "19 条（勘察／勘测／勘探／地勘／岩土／测绘／地质灾害／地质／检测／检验／监测／钻探／物探／水文／边坡／桩基／测量／地形图／CMA）"],
        ["有效机会", "1 条高价值（桥隧检测意向 1,000 万元）；7 条参考／对标；11 条判定为无关噪声"],
        ["报告生成", GEN_AT + " · QClaw 自动化生成 · 兼容 WPS / Adobe Reader"],
    ]
    t = Table([[Paragraph("<b>%s</b>" % clean(k), S["cover_meta"]), Paragraph(clean(v).replace("\n", "<br/>"), S["cover_meta"])]
               for k, v in meta], colWidths=[26*mm, 128*mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, colors.HexColor("#E2E7EE")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    F.append(t)
    F.append(NextPageTemplate("Body"))
    F.append(PageBreak())

    # ===== 目录 =====
    F.append(Paragraph("目　录", S["h1"]))
    toc = [
        ("第 1 章", "采集说明与数据可信度", "2"),
        ("第 2 章", "核心结论（一句话看完）", "2"),
        ("第 3 章", "重点项目清单（表格）", "3"),
        ("第 4 章", "逐条项目摘要与资质要求解读", "4"),
        ("第 5 章", "国家平台（中国招标投标公共服务平台）最新公告抽样", "6"),
        ("第 6 章", "风险提示与行动建议", "6"),
        ("附　录", "关键词命中但判定无关的项目（去噪记录）", "7"),
    ]
    tt = Table([[Paragraph(clean(a), S["toc"]), Paragraph(clean(b), S["toc"]), Paragraph(clean(c), S["toc"])] for a, b, c in toc],
               colWidths=[20*mm, 128*mm, 12*mm])
    tt.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (2, 0), (2, -1), "RIGHT"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.HexColor("#EDF0F4")),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    F.append(tt)
    F.append(PageBreak())

    # ===== 第1章 =====
    F.append(Paragraph("第 1 章　采集说明与数据可信度", S["h1"]))
    F.append(Paragraph("<b>1.1 海南省政府采购网（主数据源，采集完整）</b>", S["h2"]))
    F.append(Paragraph(
        "通过站点自身的发布时间筛选接口，对「公告信息」与「公示信息」两个频道执行 %s 窗口的全量分页拉取，"
        "并对 18 个行业关键词逐一执行标题检索交叉验证。共获得窗口内公告 <b>167 条</b>（公告信息 51 条 + 公示信息 116 条，已按公告 ID 去重），"
        "该数字即为该网站在此 24 小时窗口内的实际发布总量，<b>非抽样</b>。因此本报告对海南省政府采购渠道的覆盖率可视为 100%%。" % WINDOW, S["body"]))
    F.append(Spacer(1, 3))
    F.append(Paragraph("<b>1.2 中国招标投标公共服务平台（受限，部分采集）</b>", S["h2"]))
    F.append(Paragraph(
        "该平台（cebpubservice.com 及其检索站 ctbpsp.com）对关键词检索与翻页启用了行为式人机验证（点选式验证码）。"
        "首次页面加载可获取「全国最新公告」第 1 页共 10 条记录（见第 5 章），"
        "但按关键词「勘察／检测／测绘」检索及后续翻页均被验证拦截。"
        "<b>出于合规要求，本报告未对人机验证做任何绕过尝试</b>，因此国家平台数据为抽样而非全量，"
        "任务要求的「50 条」在该渠道未能达成，此处如实说明而不做补白或编造。"
        "建议后续通过该平台的「信息定制／信息 API」正式订阅通道获取完整数据。", S["body"]))
    F.append(Spacer(1, 3))
    F.append(Paragraph("<b>1.3 去噪规则</b>", S["h2"]))
    F.append(Paragraph(
        "命中关键词 ≠ 勘察检测项目。本报告对每条命中记录回读公告正文，判断「采购标的本身」是否属于工程勘察、岩土工程、"
        "地质灾害治理、测绘地理信息、试验检测或第三方检验检测服务；对仅在正文附带出现关键词（如软件测试、"
        "试剂耗材、设备参数含「监测仪」）的记录判定为无关并移入附录，保证机会池纯净。", S["body"]))

    # ===== 第2章 =====
    F.append(Paragraph("第 2 章　核心结论（一句话看完）", S["h1"]))
    concl = [
        ("零新增", "近 24 小时海南省<b>没有任何一条以「勘察／勘测／勘探／地勘／岩土／地质灾害／钻探／物探」为标的的新发布招标公告</b>，"
                   "对上述关键词的标题检索在窗口内命中数均为 0。工程勘察赛道本期无新单。"),
        ("一条金矿", "唯一高价值线索为<b>海南省公路管理局高速公路养护管理中心「2026 年度高管中心桥梁及隧道初始、定期检测项目」采购意向，"
                   "预算 1,000 万元，预计 2026 年 9 月正式采购</b>。这是本期体量最大且与检测主业强相关的标的。"),
        ("检测盘子", "检测类实际成交集中在<b>产品质量监督抽查</b>（省级 5 条合计约 210 万元、三亚市级 2 条合计约 76 万元）与"
                   "<b>环境自动监测第三方运维</b>（东方市 172 万元），均为 CMA 资质门槛型业务，属年度重复采购盘子。"),
        ("测绘门槛", "测绘/遥感类唯一标的（省林业局林草资源动态监管 44.2 万元）由<b>自然资源部第四航测遥感院</b>中标，"
                   "反映省级资源监测项目对甲级测绘资质与遥感专业能力要求较高。"),
        ("噪声占比", "19 条关键词命中中有 11 条为无关噪声（占 58%%），主要来自「监测系统软件」「检测试剂耗材」「设备含监测仪」三类，"
                   "说明单纯关键词订阅会产生大量误报，必须叠加标的语义判断。"),
    ]
    for k, v in concl:
        F.append(Paragraph("● <b>%s</b>：%s" % (k, v), S["body"]))
        F.append(Spacer(1, 2))
    F.append(PageBreak())

    # ===== 第3章 表格 =====
    F.append(Paragraph("第 3 章　重点项目清单", S["h1"]))
    F.append(Paragraph("按与勘察检测主业的相关度与商业价值排序；★ 越多越值得投入。金额单位：人民币万元。", S["small"]))
    F.append(Spacer(1, 4))
    data = [hdr(["价值", "项目名称", "预算金额", "采购人", "公告类型", "发布时间"])]
    for it in ITEMS:
        data.append([
            Paragraph(clean(it["rank"]), S["tdc"]),
            Paragraph(clean(it["name"]), S["td"]),
            Paragraph(clean(it["budget"]), S["td"]),
            Paragraph(clean(it["buyer"]), S["td"]),
            Paragraph(clean(it["type"]), S["tdc"]),
            Paragraph(clean(it["pub"]), S["tdc"]),
        ])
    tb = Table(data, colWidths=[15*mm, 58*mm, 22*mm, 34*mm, 21*mm, 24*mm], repeatRows=1)
    tb.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F2E5A")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DCE5")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F6F8FB")]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    F.append(tb)
    F.append(Spacer(1, 5))
    F.append(Paragraph(
        "注：「采购意向」为财政部要求提前公开的采购计划，尚无投标截止日；「结果公告／合同公告／履约验收公告」为已完成环节，"
        "列入本表用于价格对标与竞争对手识别，不可投标。", S["small"]))
    F.append(PageBreak())

    # ===== 第4章 明细 =====
    F.append(Paragraph("第 4 章　逐条项目摘要与资质要求解读", S["h1"]))
    for idx, it in enumerate(ITEMS, 1):
        blk = []
        blk.append(Paragraph("4.%d　%s　<font size=8 color='#8A6D1F'>%s</font>" % (idx, clean(it["name"]), clean(it["rank"])), S["h2"]))
        rows = [
            ("预算金额", it["budget"]),
            ("采购人", it["buyer"]),
            ("代理机构", it["agency"]),
            ("公告类型 / 发布时间", "%s ／ %s" % (it["type"], it["pub"])),
            ("截止日期", it["deadline"]),
            ("关键资质要求", it["qual"]),
            ("分析师点评", it["note"]),
        ]
        t = Table([[Paragraph("<b>%s</b>" % clean(k), S["td"]), Paragraph(clean(v), S["td"])] for k, v in rows],
                  colWidths=[30*mm, 144*mm])
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#E2E7EE")),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F2F5F9")),
            ("TOPPADDING", (0, 0), (-1, -1), 3.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ]))
        blk.append(t)
        blk.append(Paragraph("原文链接：<link href='%s' color='#1155CC'>%s</link>" % (it["url"], it["url"]), S["link"]))
        blk.append(Spacer(1, 6))
        F.append(KeepTogether(blk))

    F.append(PageBreak())

    # ===== 第5章 =====
    F.append(Paragraph("第 5 章　国家平台最新公告抽样（中国招标投标公共服务平台）", S["h1"]))
    F.append(Paragraph("以下 10 条为 ctbpsp.com「全国最新公告」首页在 2026-08-29 的接收记录，"
                       "其中与检测相关者仅 1 条（第 3 条，广东省，已中标），<b>无海南省项目、无勘察类项目</b>。", S["body"]))
    F.append(Spacer(1, 4))
    nd = [hdr(["#", "公告名称", "地区", "类型", "接收时间"])]
    for i, (n, r, ty, d) in enumerate(NAT, 1):
        nd.append([Paragraph(str(i), S["tdc"]), Paragraph(clean(n), S["td"]),
                   Paragraph(clean(r), S["tdc"]), Paragraph(clean(ty), S["tdc"]), Paragraph(clean(d), S["tdc"])])
    nt = Table(nd, colWidths=[8*mm, 92*mm, 27*mm, 27*mm, 20*mm], repeatRows=1)
    nt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1A4C86")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DCE5")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F6F8FB")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]))
    F.append(nt)
    F.append(Spacer(1, 4))
    F.append(Paragraph("检索入口：<link href='https://ctbpsp.com/' color='#1155CC'>https://ctbpsp.com/</link>　·　"
                       "<link href='https://www.cebpubservice.com/ctpsp_iiss/searchbusinesstypebeforedooraction/getSearch.do' color='#1155CC'>"
                       "www.cebpubservice.com 交易信息检索</link>", S["link"]))

    # ===== 第6章 =====
    F.append(Paragraph("第 6 章　风险提示与行动建议", S["h1"]))
    risks = [
        ("① 机会断档风险", "本窗口勘察／岩土／地质灾害类新增招标为 <b>0</b>。若近期在手订单不足，不应等待海南省采购网，"
                        "需同步覆盖海南省公共资源交易服务平台、各市县交易中心、以及业主自行发布渠道（省交通、水务、自然资源、住建系统）。"),
        ("② 1,000 万桥隧检测的时间窗", "采购意向到正式挂网通常 15~45 天，预计 <b>9 月内挂网</b>。"
                        "若缺少公路水运工程试验检测机构（桥梁隧道专项）等级证书，现在启动申报已来不及，"
                        "应立即锁定具备资质的联合体主体或分包合作方，并准备国省干线桥隧定期检测业绩证明。"),
        ("③ CMA 参数覆盖风险", "产品质量监督抽查类项目对 CMA 附表参数逐项核验，参数缺项将直接废标。"
                        "建议对照省市监抽查产品目录，提前扩项。"),
        ("④ 测绘资质等级风险", "省级资源监测类标的倾向甲级测绘资质与遥感处理能力，本地乙级测绘企业单独投标胜率低，宜走联合体/分包。"),
        ("⑤ 数据完整性风险（本报告局限）", "国家平台因人机验证仅取得抽样数据，可能遗漏海南以外业主在海南实施的项目。"
                        "建议开通该平台正式「信息定制／信息 API」订阅，或改用省级公共资源交易平台作为第二数据源，以补齐覆盖。"),
    ]
    for k, v in risks:
        F.append(Paragraph("<b>%s</b>　%s" % (k, v), S["warn"]))
        F.append(Spacer(1, 3))
    F.append(Spacer(1, 4))
    F.append(Paragraph("<b>今日建议动作（按优先级）</b>", S["h2"]))
    acts = [
        "1. 立即：核查公司公路水运工程试验检测机构等级证书（桥梁隧道专项）状态与检测师在册人数，形成缺口清单。",
        "2. 今日内：联系海南省公路管理局高速公路养护管理中心技术口，了解 1,000 万桥隧检测项目分包方式与踏勘安排。",
        "3. 本周：整理省／三亚两级产品质量监督抽查中标机构名单与单包价格，输出竞争格局一页纸。",
        "4. 本周：与海南天时利工程咨询、海南政采招投标、海南中廉招标等本地代理机构建立信息通道。",
        "5. 长期：开通国家平台信息订阅（API），并把海南省公共资源交易平台纳入日报数据源，解决国家平台验证拦截问题。",
    ]
    for a in acts:
        F.append(Paragraph(clean(a), S["body"]))
        F.append(Spacer(1, 1.5))

    F.append(PageBreak())

    # ===== 附录 =====
    F.append(Paragraph("附录　关键词命中但判定为无关的项目（去噪记录）", S["h1"]))
    F.append(Paragraph("保留此清单以便复核筛选口径，避免误杀真实机会。", S["small"]))
    F.append(Spacer(1, 4))
    noise = [
        ("海南省疾病预防控制局 基层医疗机构国家传染病智能监测预警前置软件实施及推广服务（合同公告）", "529.95", "命中「监测」，实为软件实施推广"),
        ("传染病病原监测试剂耗材采购项目（公开招标）", "120.21", "命中「监测」，实为试剂耗材货物"),
        ("海南省综合行政执法平台（二期）采购更正公告", "1,334.97", "正文「检测」指软件测试"),
        ("海南医科大学第二附属医院 医疗设备 2025 年度更新项目（第十批）履约验收", "204.65", "设备名称含「监测仪」"),
        ("海南铜鼓岭国家级自然保护区 麒麟菜保护区生态修复 履约验收", "31.80", "正文提及检测/监测环节，标的为生态修复施工"),
        ("海口国家高新技术产业开发区后勤服务中心 采购意向（食堂伙食物资）", "—", "正文「质量检测」指食材验收"),
        ("海南省体育彩票管理中心 采购意向", "—", "正文「监测」指系统监控"),
        ("三亚市农业技术服务中心 采购意向（农残快检试剂）", "—", "标的为胶体金快检试纸条，货物类"),
        ("三亚市市场监督管理局 抽查项目履约验收（第 2 条重复记录）", "39.02", "与正文清单重复，合并处理"),
        ("海南省市场监督管理局 抽查合同公告（重复主体多包）", "53.00", "同项目多包合同，已在第 3 章合并"),
        ("三亚市自然资源和规划局 房地产土地评估服务", "0.79", "金额过小，无投标价值（保留在第 3 章仅作观察）"),
    ]
    ad = [hdr(["项目名称", "预算(万元)", "剔除理由"])]
    for n, b, r in noise:
        ad.append([Paragraph(clean(n), S["td"]), Paragraph(clean(b), S["tdc"]), Paragraph(clean(r), S["td"])])
    at = Table(ad, colWidths=[92*mm, 22*mm, 60*mm], repeatRows=1)
    at.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6B7684")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DCE5")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F6F8FB")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]))
    F.append(at)
    F.append(Spacer(1, 8))
    F.append(Paragraph("—— 报告结束 ——", ParagraphStyle("e", fontName=FONT_R, fontSize=9,
                                                     textColor=colors.HexColor("#8A93A0"), alignment=1)))

    doc.build(F, onFirstPage=None) if False else doc.build(F)
    print("OK", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
