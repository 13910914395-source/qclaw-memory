# -*- coding: utf-8 -*-
"""生成【海南勘察招标日报】PDF（WPS 兼容 / 中文嵌入字体 / 封面+目录+正文+页脚页码）"""
import os, json, datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, PageBreak, KeepTogether)
from reportlab.platypus.tableofcontents import TableOfContents

OUT = os.path.expanduser("~/.qclaw/workspace/海南勘察招标日报_2026-08-06.pdf")
DATA = os.path.expanduser("~/.qclaw/workspace/data/hn_survey_daily_2026-08-06.json")

# ---------- 字体 ----------
FONT_CANDIDATES = [
    ("/System/Library/Fonts/STHeiti Medium.ttc", 0, "CNBold"),
    ("/System/Library/Fonts/STHeiti Light.ttc", 0, "CNRegular"),
]
reg = bold = None
for path, idx, name in FONT_CANDIDATES:
    if os.path.exists(path):
        try:
            pdfmetrics.registerFont(TTFont(name, path, subfontIndex=idx))
            if name == "CNBold":
                bold = name
            else:
                reg = name
        except Exception as e:
            print("font fail", path, e)
if reg is None:
    pdfmetrics.registerFont(TTFont("CNRegular", "/System/Library/Fonts/Supplemental/Songti.ttc", subfontIndex=0))
    reg = "CNRegular"
if bold is None:
    bold = reg

# ---------- 样式 ----------
S = {}
S['cover_t'] = ParagraphStyle('ct', fontName=bold, fontSize=28, leading=40, alignment=TA_CENTER, textColor=colors.HexColor('#0B3D67'))
S['cover_s'] = ParagraphStyle('cs', fontName=reg, fontSize=14, leading=24, alignment=TA_CENTER, textColor=colors.HexColor('#40566B'))
S['cover_m'] = ParagraphStyle('cm', fontName=reg, fontSize=10.5, leading=18, alignment=TA_LEFT, textColor=colors.HexColor('#333333'))
S['h1'] = ParagraphStyle('h1', fontName=bold, fontSize=16, leading=26, spaceBefore=10, spaceAfter=8, textColor=colors.HexColor('#0B3D67'))
S['h2'] = ParagraphStyle('h2', fontName=bold, fontSize=12.5, leading=20, spaceBefore=8, spaceAfter=5, textColor=colors.HexColor('#12608F'))
S['body'] = ParagraphStyle('bd', fontName=reg, fontSize=10, leading=16.5, spaceAfter=4)
S['small'] = ParagraphStyle('sm', fontName=reg, fontSize=8.2, leading=11.5)
S['smallb'] = ParagraphStyle('smb', fontName=bold, fontSize=8.5, leading=12, textColor=colors.white)
S['note'] = ParagraphStyle('nt', fontName=reg, fontSize=9, leading=14.5, textColor=colors.HexColor('#8A4B00'))
S['toc1'] = ParagraphStyle('toc1', fontName=bold, fontSize=11.5, leading=22, leftIndent=6)
S['toc2'] = ParagraphStyle('toc2', fontName=reg, fontSize=10, leading=18, leftIndent=22)


def P(t, st='body'):
    return Paragraph(t, S[st])


# ---------- 文档模板（书签 + 页脚） ----------
class Doc(BaseDocTemplate):
    def __init__(self, fn, **kw):
        BaseDocTemplate.__init__(self, fn, **kw)
        fw, fh = A4[0] - 36 * mm, A4[1] - 42 * mm
        frame = Frame(18 * mm, 22 * mm, fw, fh, id='n')
        self.addPageTemplates([
            PageTemplate(id='main', frames=[frame], onPage=self._deco),
        ])

    def _deco(self, canv, doc):
        if doc.page <= 1:
            return
        canv.saveState()
        canv.setStrokeColor(colors.HexColor('#0B3D67'))
        canv.setLineWidth(0.8)
        canv.line(18 * mm, A4[1] - 17 * mm, A4[0] - 18 * mm, A4[1] - 17 * mm)
        canv.setFont(reg, 8)
        canv.setFillColor(colors.HexColor('#0B3D67'))
        canv.drawString(18 * mm, A4[1] - 15.2 * mm, "【海南勘察招标日报】2026-08-06")
        canv.drawRightString(A4[0] - 18 * mm, A4[1] - 15.2 * mm, "勘察 / 检测 / 测绘 / 岩土 / 地质灾害")
        canv.setStrokeColor(colors.HexColor('#C8D4DE'))
        canv.setLineWidth(0.5)
        canv.line(18 * mm, 17 * mm, A4[0] - 18 * mm, 17 * mm)
        canv.setFont(reg, 8)
        canv.setFillColor(colors.HexColor('#666666'))
        canv.drawString(18 * mm, 12.5 * mm, "数据源：中国招标投标公共服务平台 / 海南省政府采购网（自动抓取，仅供参考）")
        canv.drawRightString(A4[0] - 18 * mm, 12.5 * mm, "第 %d 页 / 共 %s 页" % (doc.page, getattr(doc, '_total', '?')))
        canv.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            st = flowable.style.name
            txt = flowable.getPlainText()
            if st == 'h1':
                self.notify('TOCEntry', (0, txt, self.page))
                self.canv.bookmarkPage('h1-%s' % self.page)
                self.canv.addOutlineEntry(txt, 'h1-%s' % self.page, 0, 0)
            elif st == 'h2':
                self.notify('TOCEntry', (1, txt, self.page))


class TwoPass(Doc):
    pass


def money(v):
    if v in (None, '', 'None'):
        return '—'
    try:
        f = float(v)
    except Exception:
        return str(v)
    if f >= 10000:
        return "%.2f 万元" % (f / 10000.0)
    return "%.2f 元" % f


# ---------- 载入数据 ----------
d = json.load(open(DATA, encoding='utf-8'))
HN = d['hainan']
CEB_HN = d['ceb_hainan']
CEB_ALL = d['ceb_all']
STAT = d['stat']

story = []

# ===== 封面 =====
story += [Spacer(1, 38 * mm)]
story += [P("【海南勘察招标日报】", 'cover_t')]
story += [P("2026-08-06", 'cover_t')]
story += [Spacer(1, 6 * mm)]
story += [P("勘察 · 检测 · 测绘 · 岩土 · 地质灾害　招标情报", 'cover_s')]
story += [Spacer(1, 4 * mm)]
story += [P("Hainan Geotechnical Survey &amp; Testing Tender Daily", 'cover_s')]
story += [Spacer(1, 16 * mm)]

cov = [
    ["报告名称", "【海南勘察招标日报】2026-08-06"],
    ["统计窗口", "2026-08-05 03:00 — 2026-08-06 03:00（最近 24 小时）"],
    ["数据来源", "① 中国招标投标公共服务平台 www.cebpubservice.com\n② 海南省政府采购网 www.ccgp-hainan.gov.cn"],
    ["检索关键词", "勘察、检测、测绘、岩土、地质灾害（含地质/监测/检验/初勘等扩展词）"],
    ["抓取口径", "使用两站官方时间筛选接口，仅保留窗口期内新发布公告"],
    ["原始命中", "国家平台 %d 条 / 海南省采购网 %d 条（窗口期内全量 %d 条）" % (STAT['ceb_raw'], STAT['hn_hit'], STAT['hn_total'])],
    ["去重后入库", "%d 条（其中海南属地 %d 条）" % (STAT['merged'], STAT['hn_related'])],
    ["生成时间", "2026-08-06 03:00（Asia/Shanghai，自动生成）"],
    ["编制", "勘察检测行业招标分析 Agent（QClaw）"],
]
t = Table([[P(a, 'cover_m'), P(b.replace("\n", "<br/>"), 'cover_m')] for a, b in cov],
          colWidths=[30 * mm, 128 * mm])
t.setStyle(TableStyle([
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#C8D4DE')),
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#EAF1F6')),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]))
story += [t]
story += [Spacer(1, 10 * mm)]
story += [P("※ 本报告由程序自动抓取生成，金额、截止时间等以公告原文为准；投标决策前请务必核对原文。", 'note')]
story += [PageBreak()]

# ===== 目录 =====
story += [P("目　录", 'h1')]
toc = TableOfContents()
toc.levelStyles = [S['toc1'], S['toc2']]
story += [toc, PageBreak()]

# ===== 一、数据概览 =====
story += [P("一、数据概览与核心结论", 'h1')]
story += [P("本期为 <b>2026-08-05 03:00 至 2026-08-06 03:00</b> 共 24 小时窗口的勘察检测类招标情报。"
            "两个数据源均使用站内官方时间筛选接口取数，已过滤全部历史存量数据。", 'body')]

ov = [["指标", "国家平台<br/>(cebpubservice)", "海南省政府采购网<br/>(ccgp-hainan)", "合计"],
      ["窗口期公告总量（全类目）", "—", str(STAT['hn_total']), str(STAT['hn_total'])],
      ["关键词命中（去重前）", str(STAT['ceb_raw']), str(STAT['hn_hit']), str(STAT['ceb_raw'] + STAT['hn_hit'])],
      ["去重 + 相关性研判后入库", str(STAT['ceb_keep']), str(STAT['hn_keep']), str(STAT['merged'])],
      ["其中<b>海南属地</b>项目", str(len(CEB_HN)), str(STAT['hn_keep']), str(STAT['hn_related'])],
      ["其中<b>真实工程勘察/岩土</b>项目", "1（初勘）", "0", "1"],
      ["其中<b>工程 / 环境检测</b>项目", "多数", "2", "—"],
      ["其中<b>测绘 / 不动产测量</b>项目", "4（无海南）", "1（土地评估）", "5"]]
tb = Table([[P(c, 'smallb' if i == 0 else 'small') for c in row] for i, row in enumerate(ov)],
           colWidths=[52 * mm, 36 * mm, 44 * mm, 26 * mm], repeatRows=1)
tb.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0B3D67')),
    ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#B9C7D3')),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F3F7FA')]),
    ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story += [tb, Spacer(1, 5 * mm)]

story += [P("核心结论", 'h2')]
for i, c in enumerate(d['conclusions'], 1):
    story += [P("<b>%d.</b> %s" % (i, c), 'body')]
story += [PageBreak()]

# ===== 二、海南属地重点项目 =====
story += [P("二、海南属地重点项目明细", 'h1')]
story += [P("按发布时间倒序。金额单位已统一换算；“—”表示公告原文未披露。", 'body')]

hdr = ["#", "项目名称", "预算金额", "采购人", "关键资质要求", "截止/开标", "发布时间"]
rows = [[P(h, 'smallb') for h in hdr]]
for i, it in enumerate(HN, 1):
    rows.append([P(str(i), 'small'), P(it['name'], 'small'), P(it['budget'], 'small'),
                 P(it['buyer'], 'small'), P(it['qual'], 'small'), P(it['deadline'], 'small'),
                 P(it['pubtime'], 'small')])
tb = Table(rows, colWidths=[7 * mm, 44 * mm, 21 * mm, 27 * mm, 34 * mm, 22 * mm, 19 * mm], repeatRows=1)
tb.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0B3D67')),
    ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#B9C7D3')),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F3F7FA')]),
    ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ('LEFTPADDING', (0, 0), (-1, -1), 3), ('RIGHTPADDING', (0, 0), (-1, -1), 3),
]))
story += [tb, Spacer(1, 6 * mm)]

story += [P("重点项目摘要", 'h2')]
for i, it in enumerate(HN, 1):
    blk = [P("<b>%d. %s</b>" % (i, it['name']), 'body'),
           P("采购人：%s　|　代理机构：%s　|　区划：%s" % (it['buyer'], it['agency'], it['region']), 'small'),
           P("预算：%s　|　项目编号：%s　|　截止/开标：%s　|　发布：%s" % (it['budget'], it['code'], it['deadline'], it['pubtime']), 'small'),
           P("资质与要求：%s" % it['qual'], 'small'),
           P("摘要：%s" % it['summary'], 'small'),
           P("原文：%s" % it['url'], 'small'),
           Spacer(1, 3.5 * mm)]
    story.append(KeepTogether(blk))
story += [PageBreak()]

# ===== 三、国家平台海南项目 =====
story += [P("三、国家平台（cebpubservice）海南相关项目", 'h1')]
hdr = ["#", "项目名称", "交易平台", "行业", "区域", "公告截止", "发布"]
rows = [[P(h, 'smallb') for h in hdr]]
for i, it in enumerate(CEB_HN, 1):
    rows.append([P(str(i), 'small'), P(it['name'], 'small'), P(it['plat'], 'small'), P(it['ind'], 'small'),
                 P(it['region'], 'small'), P(it['end'], 'small'), P(it['pub'], 'small')])
tb = Table(rows, colWidths=[7 * mm, 60 * mm, 30 * mm, 20 * mm, 22 * mm, 19 * mm, 16 * mm], repeatRows=1)
tb.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0B3D67')),
    ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#B9C7D3')),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F3F7FA')]),
    ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
story += [tb, Spacer(1, 5 * mm)]
for it in CEB_HN:
    story += [P("<b>%s</b>" % it['name'], 'body'),
              P("项目编号：%s　|　平台编号：%s　|　行业：%s　|　公告有效期至：%s" % (it['code'], it['platcode'], it['ind'], it['end']), 'small'),
              P("研判：%s" % it['note'], 'small'),
              P("检索入口：http://www.cebpubservice.com/ctpsp_iiss/searchbusinesstypebeforedooraction/getSearch.do（按项目编号检索）", 'small'),
              Spacer(1, 3 * mm)]
story += [PageBreak()]

# ===== 四、全国同类速览 =====
story += [P("四、全国同类项目速览（发布日 2026-08-05，Top 50）", 'h1')]
story += [P("用于横向掌握行业景气度与竞对动向，海南企业可关注可异地承接的检测/试验类框架项目。", 'body')]
hdr = ["#", "词", "项目名称", "区域", "行业", "截止"]
rows = [[P(h, 'smallb') for h in hdr]]
for i, it in enumerate(CEB_ALL, 1):
    rows.append([P(str(i), 'small'), P(it['kw'], 'small'), P(it['name'], 'small'),
                 P(it['region'], 'small'), P(it['ind'], 'small'), P(it['end'], 'small')])
tb = Table(rows, colWidths=[7 * mm, 11 * mm, 74 * mm, 25 * mm, 21 * mm, 16 * mm], repeatRows=1)
tb.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0B3D67')),
    ('GRID', (0, 0), (-1, -1), 0.35, colors.HexColor('#B9C7D3')),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F3F7FA')]),
    ('TOPPADDING', (0, 0), (-1, -1), 2.4), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.4),
]))
story += [tb, PageBreak()]

# ===== 五、资质与风险 =====
story += [P("五、资质门槛与风险提示", 'h1')]
story += [P("资质要点", 'h2')]
for c in d['qual_notes']:
    story += [P("● " + c, 'body')]
story += [Spacer(1, 3 * mm), P("风险提示", 'h2')]
for c in d['risks']:
    story += [P("▲ " + c, 'note')]
story += [Spacer(1, 4 * mm), P("行动建议", 'h2')]
for c in d['actions']:
    story += [P("→ " + c, 'body')]
story += [Spacer(1, 6 * mm)]
story += [P("附：数据口径说明", 'h2')]
story += [P(d['method'], 'small')]

# ---------- 构建（两遍：目录 + 总页数） ----------
doc = Doc(OUT, pagesize=A4, title="【海南勘察招标日报】2026-08-06",
          author="QClaw 勘察检测招标分析", subject="勘察/检测/测绘/岩土/地质灾害招标日报",
          creator="QClaw", topMargin=20 * mm, bottomMargin=22 * mm,
          leftMargin=18 * mm, rightMargin=18 * mm)


def _fp(canv, docu):
    pass


class Counter:
    n = 0


# 第一遍统计页数
import copy
tmp = "/tmp/_hn_probe.pdf"
doc1 = Doc(tmp, pagesize=A4, topMargin=20 * mm, bottomMargin=22 * mm, leftMargin=18 * mm, rightMargin=18 * mm)
doc1._total = '?'
doc1.multiBuild(copy.deepcopy(story))
total = doc1.page
doc._total = total
doc.multiBuild(story)
print("PAGES", total, "->", OUT, os.path.getsize(OUT))
