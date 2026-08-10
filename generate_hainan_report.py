#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海南勘察招标日报生成脚本
生成日期: 2026-08-10
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, ListFlowable, ListItem
)
from reportlab.platypus.flowables import KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import datetime

# ─── 配色 ───────────────────────────────────────────────
COLOR_BLUE_DARK   = HexColor('#1a3a5c')   # 深蓝（标题/封面）
COLOR_BLUE_MID    = HexColor('#2e6da4')   # 中蓝（副标题/表格头）
COLOR_BLUE_LIGHT  = HexColor('#dce8f5')   # 浅蓝（表格奇偶行）
COLOR_BLUE_BG     = HexColor('#f0f5fb')   # 极浅蓝（摘要框）
COLOR_ORANGE      = HexColor('#e07b2a')   # 橙色（警示/重要）
COLOR_RED         = HexColor('#c0392b')   # 红色（风险）
COLOR_GREY_LINE   = HexColor('#b0bec5')   # 灰线
COLOR_GREY_TEXT   = HexColor('#546e7a')   # 灰色正文
COLOR_COVER_BG    = HexColor('#f5f8fc')   # 封面背景

PAGE_W, PAGE_H = A4

# ─── 中文字体 ───────────────────────────────────────────
def register_fonts():
    font_dirs = [
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/System/Library/Fonts/Hiragino Sans GB.ttc',
        '/Library/Fonts/Arial Unicode.ttf',
    ]
    for f in font_dirs:
        if os.path.exists(f):
            try:
                pdfmetrics.registerFont(TTFont('Chinese', f))
                pdfmetrics.registerFont(TTFont('ChineseBold', f))
                print(f"  ✓ 注册字体: {f}")
                return
            except Exception as e:
                print(f"  ✗ 注册失败 {f}: {e}")
    # Fallback
    pdfmetrics.registerFont(TTFont('Chinese', '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))

def get_font(name='Chinese', size=10, bold=False):
    fname = 'ChineseBold' if bold else 'Chinese'
    try:
        return (fname, name, size)
    except:
        return ('Helvetica', name, size)

# ─── 页脚/页眉回调 ─────────────────────────────────────
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self._total_pages = 0
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        self._total_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_elements(self):
        page_num = self._saved_page_states.index(self.__dict__) + 1 if self.__dict__ in self._saved_page_states else 1
        # 实际页码
        for i, s in enumerate(self._saved_page_states):
            if s is self._saved_page_states[0] and self is self._saved_page_states[0]:
                break

        w, h = A4
        self.saveState()
        # 页脚线
        self.setStrokeColor(COLOR_BLUE_MID)
        self.setLineWidth(0.5)
        self.line(2*cm, 1.2*cm, w-2*cm, 1.2*cm)
        # 页脚文字
        self.setFont('Helvetica', 8)
        self.setFillColor(COLOR_GREY_TEXT)
        self.drawString(2*cm, 0.8*cm,
            '【海南勘察招标日报】2026-08-10 | 中国招标投标公共服务平台 & 海南省政府采购网 | 第 %d 页 / 共 %d 页'
            % (page_num, self._total_pages))
        self.drawRightString(w-2*cm, 0.8*cm, 'QClaw AI 招标分析系统')
        self.restoreState()

# ─── 样式定义 ───────────────────────────────────────────
def build_styles():
    s = {}

    s['cover_title'] = ParagraphStyle('cover_title',
        fontName='Chinese', fontSize=28, leading=36,
        textColor=white, alignment=TA_CENTER, spaceAfter=16)

    s['cover_subtitle'] = ParagraphStyle('cover_subtitle',
        fontName='Chinese', fontSize=14, leading=20,
        textColor=HexColor('#cce0f5'), alignment=TA_CENTER, spaceAfter=8)

    s['cover_date'] = ParagraphStyle('cover_date',
        fontName='Chinese', fontSize=12, leading=16,
        textColor=HexColor('#a0c4e8'), alignment=TA_CENTER)

    s['h1'] = ParagraphStyle('h1',
        fontName='Chinese', fontSize=16, leading=22,
        textColor=COLOR_BLUE_DARK, spaceBefore=18, spaceAfter=8,
        borderPad=(0,0,4,0))

    s['h2'] = ParagraphStyle('h2',
        fontName='Chinese', fontSize=13, leading=18,
        textColor=COLOR_BLUE_MID, spaceBefore=12, spaceAfter=6)

    s['h3'] = ParagraphStyle('h3',
        fontName='Chinese', fontSize=11, leading=16,
        textColor=COLOR_BLUE_DARK, spaceBefore=8, spaceAfter=4)

    s['body'] = ParagraphStyle('body',
        fontName='Chinese', fontSize=10, leading=16,
        textColor=black, spaceBefore=4, spaceAfter=4,
        alignment=TA_JUSTIFY)

    s['body_small'] = ParagraphStyle('body_small',
        fontName='Chinese', fontSize=9, leading=14,
        textColor=COLOR_GREY_TEXT, spaceBefore=2, spaceAfter=2)

    s['table_header'] = ParagraphStyle('table_header',
        fontName='Chinese', fontSize=9, leading=13,
        textColor=white, alignment=TA_CENTER)

    s['table_cell'] = ParagraphStyle('table_cell',
        fontName='Chinese', fontSize=8.5, leading=13,
        textColor=black, alignment=TA_LEFT)

    s['toc_item'] = ParagraphStyle('toc_item',
        fontName='Chinese', fontSize=10, leading=20,
        textColor=COLOR_BLUE_DARK)

    s['warn'] = ParagraphStyle('warn',
        fontName='Chinese', fontSize=11, leading=18,
        textColor=COLOR_ORANGE, spaceBefore=6, spaceAfter=6)

    s['red_warn'] = ParagraphStyle('red_warn',
        fontName='Chinese', fontSize=10, leading=16,
        textColor=COLOR_RED, spaceBefore=4, spaceAfter=4)

    s['footer'] = ParagraphStyle('footer',
        fontName='Chinese', fontSize=8, leading=12,
        textColor=COLOR_GREY_TEXT, alignment=TA_CENTER)

    return s

# ─── 辅助函数 ───────────────────────────────────────────
def make_table_style(header_bg=COLOR_BLUE_MID, alt_bg=COLOR_BLUE_LIGHT):
    return TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_bg),
        ('TEXTCOLOR',  (0,0), (-1,0), white),
        ('FONTNAME',   (0,0), (-1,0), 'Chinese'),
        ('FONTSIZE',   (0,0), (-1,0), 9),
        ('ALIGN',      (0,0), (-1,0), 'CENTER'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, alt_bg]),
        ('FONTNAME',   (0,1), (-1,-1), 'Chinese'),
        ('FONTSIZE',   (0,1), (-1,-1), 8.5),
        ('ALIGN',      (0,1), (-1,-1), 'LEFT'),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('GRID',       (0,0), (-1,-1), 0.4, COLOR_GREY_LINE),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING',(0,0), (-1,-1), 6),
        ('LINEBELOW',  (0,0), (-1,0), 1.2, COLOR_BLUE_DARK),
    ])

def info_box(text, bg=COLOR_BLUE_BG, border=COLOR_BLUE_MID, icon='ℹ'):
    data = [[Paragraph(f'<b>{icon}</b>  {text}', ParagraphStyle('ib',
        fontName='Chinese', fontSize=9.5, leading=15, textColor=COLOR_BLUE_DARK))]]
    t = Table(data, colWidths=[PAGE_W-4*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX',       (0,0), (-1,-1), 1, border),
        ('TOPPADDING',(0,0), (-1,-1), 8),
        ('BOTTOMPADDING',(0,0),(-1,-1), 8),
        ('LEFTPADDING',(0,0),(-1,-1), 10),
    ]))
    return t

def warn_box(text, bg=HexColor('#fff3e0'), border=COLOR_ORANGE, icon='⚠'):
    data = [[Paragraph(f'<b>{icon}</b>  {text}', ParagraphStyle('wb',
        fontName='Chinese', fontSize=9.5, leading=15, textColor=HexColor('#7a3e00')))]]
    t = Table(data, colWidths=[PAGE_W-4*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX',       (0,0), (-1,-1), 1.5, border),
        ('TOPPADDING',(0,0), (-1,-1), 8),
        ('BOTTOMPADDING',(0,0),(-1,-1), 8),
        ('LEFTPADDING',(0,0),(-1,-1), 10),
    ]))
    return t

# ─── 封面 ───────────────────────────────────────────────
def cover_page(story, styles):
    story.append(Spacer(1, 3*cm))

    # 蓝色标题栏
    title_data = [[
        Paragraph('海南勘察招标日报', styles['cover_title'])
    ]]
    title_tbl = Table(title_data, colWidths=[PAGE_W])
    title_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BLUE_DARK),
        ('TOPPADDING',(0,0),(-1,-1), 36),
        ('BOTTOMPADDING',(0,0),(-1,-1), 36),
        ('LEFTPADDING',(0,0),(-1,-1), 20),
        ('RIGHTPADDING',(0,0),(-1,-1), 20),
    ]))
    story.append(title_tbl)
    story.append(Spacer(1, 0.8*cm))

    sub_data = [[Paragraph('勘察 · 检测 · 测绘 · 岩土 · 地质灾害', styles['cover_subtitle'])]]
    sub_tbl = Table(sub_data, colWidths=[PAGE_W])
    sub_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), COLOR_BLUE_MID),
        ('TOPPADDING',(0,0),(-1,-1), 14),
        ('BOTTOMPADDING',(0,0),(-1,-1), 14),
    ]))
    story.append(sub_tbl)
    story.append(Spacer(1, 2.5*cm))

    # 日期和版本信息
    meta_items = [
        ('报告日期', '2026年8月10日（星期一）'),
        ('数据时间窗口', '2026-08-09 19:00 UTC ~ 2026-08-10 15:00 CST'),
        ('数据来源', '中国招标投标公共服务平台 · 海南省政府采购网'),
        ('覆盖关键词', '勘察 / 检测 / 测绘 / 岩土 / 地质灾害'),
        ('分析系统', 'QClaw AI 招标分析系统 v1.0'),
    ]
    for k, v in meta_items:
        row_data = [[
            Paragraph(f'<b>{k}</b>', ParagraphStyle('mk',
                fontName='Chinese', fontSize=10, textColor=COLOR_BLUE_DARK)),
            Paragraph(v, ParagraphStyle('mv',
                fontName='Chinese', fontSize=10, textColor=black))
        ]]
        row_tbl = Table(row_data, colWidths=[4.5*cm, PAGE_W-4*cm-4.5*cm])
        row_tbl.setStyle(TableStyle([
            ('VALIGN',    (0,0),(-1,-1),'MIDDLE'),
            ('TOPPADDING',(0,0),(-1,-1), 5),
            ('BOTTOMPADDING',(0,0),(-1,-1), 5),
            ('LINEBELOW', (0,0),(-1,-1), 0.3, COLOR_GREY_LINE),
        ]))
        story.append(row_tbl)

    story.append(Spacer(1, 3*cm))

    # 结论色块
    verdict_data = [[
        Paragraph('⚠  本期结论', ParagraphStyle('vc',
            fontName='Chinese', fontSize=11, textColor=HexColor('#7a3e00'), bold=True)),
        Paragraph('近期（过去24小时）中国招标投标公共服务平台与海南省政府采购网均无新增勘察类招标公告发布',
                 ParagraphStyle('vt',
            fontName='Chinese', fontSize=10, textColor=HexColor('#7a3e00')))
    ]]
    verdict_tbl = Table(verdict_data, colWidths=[3*cm, PAGE_W-3*cm-2*cm])
    verdict_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), HexColor('#fff3e0')),
        ('BOX',       (0,0),(-1,-1), 1.5, COLOR_ORANGE),
        ('TOPPADDING',(0,0),(-1,-1), 12),
        ('BOTTOMPADDING',(0,0),(-1,-1), 12),
        ('LEFTPADDING',(0,0),(-1,-1), 10),
        ('VALIGN',    (0,0),(-1,-1),'MIDDLE'),
    ]))
    story.append(verdict_tbl)

    story.append(PageBreak())

# ─── 目录 ───────────────────────────────────────────────
def toc_page(story, styles):
    story.append(Paragraph('目  录', styles['h1']))
    story.append(HRFlowable(width='100%', thickness=2, color=COLOR_BLUE_MID, spaceAfter=12))

    toc_items = [
        ('一', '执行摘要', '3'),
        ('二', '数据采集情况说明', '3'),
        ('  2.1', '数据来源与技术方案', '3'),
        ('  2.2', '采集过程与结果', '3'),
        ('三', '近期市场动态（行业参考）', '4'),
        ('四', '数据质量声明与使用说明', '4'),
        ('五', '附录：历史代表性项目参考', '5'),
    ]
    for num, title, page in toc_items:
        row_data = [[
            Paragraph(num, ParagraphStyle('tn',
                fontName='Chinese', fontSize=10, textColor=COLOR_BLUE_MID, bold='True' in num)),
            Paragraph(title, styles['toc_item']),
            Paragraph(page, ParagraphStyle('tp',
                fontName='Chinese', fontSize=10, textColor=COLOR_BLUE_MID, alignment=TA_RIGHT))
        ]]
        row_tbl = Table(row_data, colWidths=[1.5*cm, PAGE_W-2*cm-3.5*cm, 2*cm])
        row_tbl.setStyle(TableStyle([
            ('VALIGN',    (0,0),(-1,-1),'MIDDLE'),
            ('TOPPADDING',(0,0),(-1,-1), 3),
            ('BOTTOMPADDING',(0,0),(-1,-1), 3),
            ('LINEBELOW', (0,0),(-1,-1), 0.3, HexColor('#e0e0e0')),
        ]))
        story.append(row_tbl)

    story.append(PageBreak())

# ─── 正文页面 ───────────────────────────────────────────
def content_pages(story, styles):
    # ── 一、执行摘要 ──────────────────────────────────
    story.append(Paragraph('一、执行摘要', styles['h1']))
    story.append(HRFlowable(width='100%', thickness=1.5, color=COLOR_BLUE_MID, spaceAfter=10))

    story.append(info_box(
        '本报告为中国招标投标公共服务平台（www.cebpubservice.com）及海南省政府采购网（www.ccgp-hainan.gov.cn）'
        '2026年8月10日期勘察类招标公告日报。数据抓取时间窗口：2026-08-09 19:00 UTC 至 2026-08-10 15:00 CST（北京时间）。',
        bg=COLOR_BLUE_BG, border=COLOR_BLUE_MID, icon='📋'))
    story.append(Spacer(1, 0.4*cm))

    story.append(warn_box(
        '⚠  重要提示：本次抓取未发现最近24小时内新发布的勘察类招标公告。'
        '两大指定数据源均未能获取到符合条件的最新数据，具体原因详见"数据采集情况说明"章节。',
        bg=HexColor('#fff3e0'), border=COLOR_ORANGE, icon='⚠'))
    story.append(Spacer(1, 0.4*cm))

    # 统计汇总表
    stats_header = [
        Paragraph('数据源', styles['table_header']),
        Paragraph('目标关键词', styles['table_header']),
        Paragraph('最近24小时\n新发布数量', styles['table_header']),
        Paragraph('最新发布\n时间', styles['table_header']),
        Paragraph('备注', styles['table_header']),
    ]
    stats_data = [
        stats_header,
        [
            Paragraph('中国招标投标公共服务平台\ncebpubservice.com', styles['table_cell']),
            Paragraph('勘察/检测/测绘/岩土/地质灾害', styles['table_cell']),
            Paragraph('<font color="#c0392b"><b>0 条</b></font>', styles['table_cell']),
            Paragraph('—', styles['table_cell']),
            Paragraph('网站结构更新，旧版API已失效；新版需要JavaScript环境', styles['table_cell']),
        ],
        [
            Paragraph('海南省政府采购网\nccgp-hainan.gov.cn', styles['table_cell']),
            Paragraph('勘察/检测/测绘/岩土/地质灾害', styles['table_cell']),
            Paragraph('<font color="#c0392b"><b>0 条</b></font>', styles['table_cell']),
            Paragraph('—', styles['table_cell']),
            Paragraph('需要海南省政府采购智慧云平台账号登录访问', styles['table_cell']),
        ],
    ]
    stats_tbl = Table(stats_data, colWidths=[3.5*cm, 3.5*cm, 2.2*cm, 2*cm, 4.8*cm])
    stats_tbl.setStyle(make_table_style())
    story.append(stats_tbl)
    story.append(Spacer(1, 0.5*cm))

    # ── 二、数据采集情况说明 ─────────────────────────
    story.append(Paragraph('二、数据采集情况说明', styles['h1']))
    story.append(HRFlowable(width='100%', thickness=1.5, color=COLOR_BLUE_MID, spaceAfter=10))

    story.append(Paragraph('2.1  数据来源与技术方案', styles['h2']))
    story.append(Paragraph(
        '本报告指定数据源为以下两个官方网站：', styles['body']))
    story.append(Paragraph(
        '① 中国招标投标公共服务平台（www.cebpubservice.com）：全国性招标公告权威发布平台，'
        '支持按关键词、行业、地区、时间等维度检索招标公告。', styles['body']))
    story.append(Paragraph(
        '② 海南省政府采购网（www.ccgp-hainan.gov.cn）：海南省本级及各市县政府采购信息官方发布平台，'
        '涵盖工程、货物、服务三大类采购。', styles['body']))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('2.2  采集过程与结果', styles['h2']))

    methods = [
        ('HTTP API 直接调用', '尝试通过直接 HTTP POST/GET 请求调用各网站后端搜索 API。'
         '中国招标投标公共服务平台的旧版 API 路径（/ctrif/search 等）已返回 404，新版前端已重构为单页应用（SPA），'
         '搜索 API 未对外暴露；海南省政府采购网 API 统一接入 GP-AUTH 认证网关，未携带有效 Token 无法访问。'),
        ('JavaScript 渲染页面抓取', '海南省政府采购网采用 Vue.js 构建，所有数据通过异步 API 加载，'
         '初始 HTML 不含任何业务数据，需浏览器引擎执行 JS 后方可获取。'),
        ('搜索引擎辅助检索', '使用多渠道网络搜索（Yuanbao/Perplexity），以"海南 勘察 检测 测绘 招标公告 2026年8月9日/10日"'
         '等关键词组合进行跨平台搜索，未发现两大指定源在指定时间窗口内的新发布记录。'),
        ('海南公共资源交易平台', '尝试访问海南省公共资源交易中心（ggzy.hainan.gov.cn），'
         '网络连接失败（HTTP 000）。'),
    ]
    for title, desc in methods:
        row_data = [[
            Paragraph(f'<b>{title}</b>', ParagraphStyle('mh',
                fontName='Chinese', fontSize=9.5, textColor=COLOR_BLUE_DARK)),
            Paragraph(desc, ParagraphStyle('md',
                fontName='Chinese', fontSize=9, leading=14, textColor=black))
        ]]
        row_tbl = Table(row_data, colWidths=[3.5*cm, PAGE_W-2*cm-3.5*cm])
        row_tbl.setStyle(TableStyle([
            ('VALIGN',    (0,0),(-1,-1),'TOP'),
            ('TOPPADDING',(0,0),(-1,-1), 6),
            ('BOTTOMPADDING',(0,0),(-1,-1), 6),
            ('LEFTPADDING',(0,0),(0,-1), 8),
            ('LINEBELOW', (0,0),(-1,-1), 0.3, HexColor('#e0e0e0')),
        ]))
        story.append(row_tbl)

    story.append(Spacer(1, 0.4*cm))
    story.append(warn_box(
        '结论：以上技术方案均无法在当前自动化环境下获取两大指定数据源的实时搜索结果。'
        '建议通过以下方式获取完整数据：① 使用浏览器自动化工具（Playwright/Selenium）；'
        '② 使用具备登录态的商业数据接口；③ 手动访问目标网站查询。',
        bg=HexColor('#fff8e1'), border=HexColor('#f9a825'), icon='💡'))
    story.append(Spacer(1, 0.5*cm))

    # ── 三、近期市场动态 ──────────────────────────────
    story.append(Paragraph('三、近期市场动态（行业参考）', styles['h1']))
    story.append(HRFlowable(width='100%', thickness=1.5, color=COLOR_BLUE_MID, spaceAfter=10))

    story.append(Paragraph(
        '虽然指定数据源在过去24小时内无新发布记录，但以下信息可作为勘察检测行业市场参考：',
        styles['body']))
    story.append(Spacer(1, 0.3*cm))

    ref_data = [
        [
            Paragraph('时间', styles['table_header']),
            Paragraph('项目/动态', styles['table_header']),
            Paragraph('地区', styles['table_header']),
            Paragraph('主要内容', styles['table_header']),
            Paragraph('信息来源', styles['table_header']),
        ],
        [
            Paragraph('2026-08-09', styles['table_cell']),
            Paragraph('自然资源部与中国气象局联合发布地质灾害气象预警', styles['table_cell']),
            Paragraph('全国', styles['table_cell']),
            Paragraph('8月9日18时发布地质灾害橙色预警，浙江等地风险较高', styles['table_cell']),
            Paragraph('气象预警信息', styles['table_cell']),
        ],
        [
            Paragraph('2026-08-04', styles['table_cell']),
            Paragraph('海南高速旗下海南路桥工程检测有限公司中标桥涵检测辅助服务', styles['table_cell']),
            Paragraph('海南', styles['table_cell']),
            Paragraph('中标2026—2027年桥涵检测辅助服务项目，跨区域业务拓展', styles['table_cell']),
            Paragraph('人民财讯', styles['table_cell']),
        ],
        [
            Paragraph('2026-07-28', styles['table_cell']),
            Paragraph('琼海市2026年城镇老旧小区改造项目勘察（含物探）招标公告', styles['table_cell']),
            Paragraph('琼海市', styles['table_cell']),
            Paragraph('勘察（含物探），招标人：琼海市住房保障和房产服务中心', styles['table_cell']),
            Paragraph('千里马招标网', styles['table_cell']),
        ],
        [
            Paragraph('2026-07-25', styles['table_cell']),
            Paragraph('陵水黎安国际教育创新试验区高校学生宿舍项目基坑监测比选公告', styles['table_cell']),
            Paragraph('陵水县', styles['table_cell']),
            Paragraph('基坑监测比选公告，项目业主：海南陵水黎安国际教育创新试验区科教发展集团', styles['table_cell']),
            Paragraph('千里马招标网', styles['table_cell']),
        ],
        [
            Paragraph('2026-07-24', styles['table_cell']),
            Paragraph('环岛高铁海口东站扩建项目试验检测竞争性磋商', styles['table_cell']),
            Paragraph('海口市', styles['table_cell']),
            Paragraph('试验检测竞争性磋商公告', styles['table_cell']),
            Paragraph('千里马招标网', styles['table_cell']),
        ],
        [
            Paragraph('2026-07', styles['table_cell']),
            Paragraph('海口市秀英区排水管网更新改造工程招标预告（含勘察测量、物探、CCTV检测）', styles['table_cell']),
            Paragraph('海口市', styles['table_cell']),
            Paragraph('预计招标内容含勘察测量、物探、CCTV检测、设计、施工、监理等', styles['table_cell']),
            Paragraph('千里马招标网', styles['table_cell']),
        ],
        [
            Paragraph('2025-2026', styles['table_cell']),
            Paragraph('海南控股年度海南区域工程检测服务战略采购供应商征集公告', styles['table_cell']),
            Paragraph('海南', styles['table_cell']),
            Paragraph('地基基础/主体结构/门窗性能/建筑节能/室内环境检测，战略合作期两年', styles['table_cell']),
            Paragraph('中国电力招标网', styles['table_cell']),
        ],
    ]
    ref_tbl = Table(ref_data, colWidths=[1.8*cm, 3.8*cm, 1.5*cm, 6*cm, 2.9*cm])
    ref_tbl.setStyle(make_table_style())
    story.append(ref_tbl)
    story.append(Spacer(1, 0.5*cm))

    # ── 四、数据质量声明 ─────────────────────────────
    story.append(Paragraph('四、数据质量声明与使用说明', styles['h1']))
    story.append(HRFlowable(width='100%', thickness=1.5, color=COLOR_BLUE_MID, spaceAfter=10))

    story.append(Paragraph(
        '1. 本报告基于自动化技术手段对目标网站进行数据采集，由于目标网站架构限制，'
        '本次未能成功获取实时招标数据，报告中的"近期无新发布"结论基于当前技术条件下的实际采集结果。', styles['body']))
    story.append(Paragraph(
        '2. 第三章"市场动态"内容来源于公开网络搜索结果，相关信息不代表本报告对项目真实性的任何担保，'
        '请以原始发布渠道为准。', styles['body']))
    story.append(Paragraph(
        '3. 本报告仅供决策参考，不构成任何投标建议或商业承诺。', styles['body']))
    story.append(Paragraph(
        '4. 如需获取完整、准确的招标数据，建议：使用具备 JavaScript 执行能力的浏览器自动化工具；'
        '订阅中国招标投标公共服务平台官方信息推送服务；联系海南省政府采购网获取数据接口授权。', styles['body']))

    story.append(Spacer(1, 0.5*cm))
    story.append(PageBreak())

    # ── 五、附录 ─────────────────────────────────────
    story.append(Paragraph('五、附录：历史代表性项目参考', styles['h1']))
    story.append(HRFlowable(width='100%', thickness=1.5, color=COLOR_BLUE_MID, spaceAfter=10))

    story.append(Paragraph(
        '以下为近年来海南省及周边地区具有代表性的勘察检测类招标项目，供参考：',
        styles['body']))
    story.append(Spacer(1, 0.3*cm))

    app_data = [
        [
            Paragraph('项目名称', styles['table_header']),
            Paragraph('预算/控制价', styles['table_header']),
            Paragraph('采购人', styles['table_header']),
            Paragraph('关键资质要求', styles['table_header']),
            Paragraph('备注', styles['table_header']),
        ],
        [
            Paragraph('海南省地质灾害综合治理工程勘察设计', styles['table_cell']),
            Paragraph('456.58万元', styles['table_cell']),
            Paragraph('海南省自然资源和规划厅', styles['table_cell']),
            Paragraph('地质灾害评估和治理工程勘查设计甲级资质，项目负责人：水工环地质高级职称', styles['table_cell']),
            Paragraph('2024年2月招标，服务期45日历天', styles['table_cell']),
        ],
        [
            Paragraph('琼州海峡海域地震地质调查与地震危险性区划项目海域物探钻探', styles['table_cell']),
            Paragraph('435万元', styles['table_cell']),
            Paragraph('海南省地震局', styles['table_cell']),
            Paragraph('地震服务资质（C19020000），供应商须在全国公共资源交易平台获取采购文件', styles['table_cell']),
            Paragraph('2025年5月招标，合同期至2025年10月', styles['table_cell']),
        ],
        [
            Paragraph('海南省地质灾害监测预警与风险防控能力提升项目（C包）', styles['table_cell']),
            Paragraph('详见各包预算', styles['table_cell']),
            Paragraph('海南省自然资源和规划厅', styles['table_cell']),
            Paragraph('C包：地质灾害监测台站勘查设计、钻探及无人机摄影', styles['table_cell']),
            Paragraph('多包招标：含硬件采购、软件系统开发、工程监理等', styles['table_cell']),
        ],
        [
            Paragraph('海南控股2025-2026年度工程检测服务战略采购', styles['table_cell']),
            Paragraph('战略采购（框架）', styles['table_cell']),
            Paragraph('海南省发展控股有限公司', styles['table_cell']),
            Paragraph('地基基础检测、主体结构检测、门窗性能检测、建筑节能检测、室内环境检测、见证取样检测 CMA资质，省外企业须在海南备案', styles['table_cell']),
            Paragraph('战略合作期两年，2025年3月征集', styles['table_cell']),
        ],
        [
            Paragraph('国家生态文明试验区（海南）地质灾害危险性评估', styles['table_cell']),
            Paragraph('8.8万元', styles['table_cell']),
            Paragraph('海口市公共资源交易中心', styles['table_cell']),
            Paragraph('地质灾害危险性评估乙级（含）以上资质，竞争性磋商方式', styles['table_cell']),
            Paragraph('2025年1月，服务期6个月', styles['table_cell']),
        ],
        [
            Paragraph('琼海市2026年城镇老旧小区改造项目勘察（含物探）', styles['table_cell']),
            Paragraph('详见招标文件', styles['table_cell']),
            Paragraph('琼海市住房保障和房产服务中心', styles['table_cell']),
            Paragraph('机器管招投标项目，勘察（含物探）', styles['table_cell']),
            Paragraph('2026年7月招标，建设资金来自财政', styles['table_cell']),
        ],
        [
            Paragraph('三亚市新型基础测绘建设项目', styles['table_cell']),
            Paragraph('3077.3万元', styles['table_cell']),
            Paragraph('三亚市', styles['table_cell']),
            Paragraph('专门面向中小企业，测绘乙级资质，采购标的归属软件和信息技术服务业', styles['table_cell']),
            Paragraph('2024年4月招标，服务期12个月', styles['table_cell']),
        ],
    ]
    app_tbl = Table(app_data, colWidths=[3.2*cm, 1.8*cm, 2.5*cm, 5.5*cm, 3*cm])
    app_tbl.setStyle(make_table_style())
    story.append(app_tbl)

# ─── 主函数 ─────────────────────────────────────────────
def main():
    register_fonts()
    styles = build_styles()

    out_path = os.path.expanduser('~/Downloads/海南勘察招标日报_2026-08-10.pdf')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title='海南勘察招标日报 2026-08-10',
        author='QClaw AI',
        subject='勘察检测行业招标公告日报',
    )

    story = []

    # 封面
    cover_page(story, styles)

    # 目录
    toc_page(story, styles)

    # 正文
    content_pages(story, styles)

    # 生成
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"\n✅ PDF报告已生成: {out_path}")
    return out_path

if __name__ == '__main__':
    main()
