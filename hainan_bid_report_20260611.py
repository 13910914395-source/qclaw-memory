#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海南勘察招标日报 - 2026年6月11日
生成结构化PDF报告
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.colors import HexColor, white, black, grey
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Frame, NextPageTemplate, PageTemplate,
    BaseDocTemplate
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# Register Chinese fonts
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))

# ── Constants ──
PAGE_W, PAGE_H = A4  # 210 x 297 mm

# Colors
DARK_BLUE = HexColor('#1a3a5c')
ACCENT_BLUE = HexColor('#2563eb')
ACCENT_ORANGE = HexColor('#f59e0b')
LIGHT_GRAY = HexColor('#f3f4f6')
MID_GRAY = HexColor('#9ca3af')
TABLE_HEADER_BG = HexColor('#1e3a5f')
TABLE_ROW_ALT = HexColor('#f8fafc')
RED_ALERT = HexColor('#dc2626')
GREEN_OK = HexColor('#16a34a')

# Styles
styles = getSampleStyleSheet()

style_cover_title = ParagraphStyle(
    'CoverTitle', parent=styles['Title'],
    fontName='STSong-Light', fontSize=28, leading=40,
    alignment=TA_CENTER, textColor=DARK_BLUE,
    spaceAfter=10*mm
)

style_cover_subtitle = ParagraphStyle(
    'CoverSubtitle', parent=styles['Normal'],
    fontName='STSong-Light', fontSize=14, leading=22,
    alignment=TA_CENTER, textColor=MID_GRAY,
    spaceAfter=6*mm
)

style_cover_info = ParagraphStyle(
    'CoverInfo', parent=styles['Normal'],
    fontName='STSong-Light', fontSize=11, leading=18,
    alignment=TA_CENTER, textColor=HexColor('#475569'),
)

style_h1 = ParagraphStyle(
    'H1', parent=styles['Heading1'],
    fontName='STSong-Light', fontSize=18, leading=26,
    textColor=DARK_BLUE, spaceBefore=10*mm, spaceAfter=6*mm,
    borderPadding=(0, 0, 2, 0),
)

style_h2 = ParagraphStyle(
    'H2', parent=styles['Heading2'],
    fontName='STSong-Light', fontSize=14, leading=20,
    textColor=DARK_BLUE, spaceBefore=8*mm, spaceAfter=4*mm,
)

style_body = ParagraphStyle(
    'Body', parent=styles['Normal'],
    fontName='STSong-Light', fontSize=9.5, leading=16,
    alignment=TA_JUSTIFY, textColor=HexColor('#334155'),
    spaceAfter=3*mm,
)

style_body_small = ParagraphStyle(
    'BodySmall', parent=style_body,
    fontSize=8.5, leading=13,
)

style_table_header = ParagraphStyle(
    'TableHeader', parent=styles['Normal'],
    fontName='STSong-Light', fontSize=8, leading=12,
    alignment=TA_CENTER, textColor=white,
)

style_table_cell = ParagraphStyle(
    'TableCell', parent=styles['Normal'],
    fontName='STSong-Light', fontSize=7.5, leading=11,
    alignment=TA_LEFT, textColor=HexColor('#1e293b'),
)

style_table_cell_center = ParagraphStyle(
    'TableCellCenter', parent=style_table_cell,
    alignment=TA_CENTER,
)

style_alert = ParagraphStyle(
    'Alert', parent=style_body,
    fontSize=10, leading=16,
    textColor=RED_ALERT,
    fontName='STSong-Light',
)

style_toc = ParagraphStyle(
    'TOC', parent=style_body,
    fontSize=11, leading=22,
)

# ── Data ──
REPORT_DATE = "2026-06-11"
REPORT_DATE_FULL = "2026年6月11日"

# Actual findings from yesterday's scan
bid_data = [
    {
        "seq": 1,
        "source": "全国公共资源交易平台(海南省)",
        "title": "2023年农村公路养护工程勘察、设计项目",
        "budget": "见招标文件",
        "buyer": "海口美丽村庄投资有限公司",
        "qualifications": "工程勘察专业类(岩土工程(勘察))乙级或以上资质；注册土木工程师(岩土)执业资格",
        "deadline": "2026-07-02",
        "pub_date": "2026-06-11",
        "url": "https://ggzy.hainan.gov.cn/ggzy/ggzy/gpgg/245382.jhtml",
        "keywords": "勘察, 岩土工程, 设计",
        "risk": "低"
    },
    {
        "seq": 2,
        "source": "全国公共资源交易平台(海南省)",
        "title": "测绘地理信息技术服务项目(HZ2026-140)",
        "budget": "4,000,000.00元",
        "buyer": "自然资源部海南测绘资料信息中心",
        "qualifications": "测绘乙级或以上资质(专业类别须含界线与不动产测绘/工程测量)",
        "deadline": "2026-06-11(当天截标)",
        "pub_date": "2026-05-20",
        "url": "https://ggzy.hainan.gov.cn/ggzyjy/jyxx/003002/003002002/20260520/6baa3e63cf9faf71f75ebe994358de35.html",
        "keywords": "测绘, 地理信息, 技术服务",
        "risk": "中(今日截标!)"
    },
]

# Platform status
platform_status = {
    "cebpubservice.com": {
        "status": "❌ 不可访问",
        "detail": "返回502 Bad Gateway，网站CDN/WAF拦截，当前无法抓取公告。建议通过浏览器手动访问或使用付费API接口获取数据。"
    },
    "ccgp-hainan.gov.cn": {
        "status": "❌ 不可访问",
        "detail": "连接失败，海南省政府采购网当前不可达。可尝试切换网络环境或通过海南省公共资源交易平台检索政府采购信息。"
    },
    "ggzy.hainan.gov.cn": {
        "status": "⚠️ 部分可访问",
        "detail": "通过搜索索引获取到部分公告，但直接页面抓取受限。"
    }
}

# ── Page templates ──
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_footer(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_footer(self, num_pages):
        page_num = self._pageNumber
        # Footer line
        self.setStrokeColor(HexColor('#cbd5e1'))
        self.setLineWidth(0.5)
        self.line(20*mm, 18*mm, PAGE_W - 20*mm, 18*mm)
        # Left: report title
        self.setFont('STSong-Light', 7)
        self.setFillColor(MID_GRAY)
        self.drawString(20*mm, 12*mm, f"海南勘察招标日报 | {REPORT_DATE_FULL}")
        # Center
        self.drawCentredString(PAGE_W/2, 12*mm, "内部资料 · 仅供参考")
        # Right: page number
        self.drawRightString(PAGE_W - 20*mm, 12*mm, f"第 {page_num} 页 / 共 {num_pages} 页")

        # Header line
        self.setStrokeColor(HexColor('#2563eb'))
        self.setLineWidth(1.2)
        self.line(20*mm, PAGE_H - 20*mm, PAGE_W - 20*mm, PAGE_H - 20*mm)


def build_report():
    pdf_path = os.path.expanduser("~/.qclaw/workspace/海南勘察招标日报_2026-06-11.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=22*mm, bottomMargin=22*mm,
        title=f"海南勘察招标日报 - {REPORT_DATE_FULL}",
        author="勘察检测行业招标分析师",
    )

    story = []

    # ═══════════════ COVER PAGE ═══════════════
    story.append(Spacer(1, 45*mm))

    # Top accent line
    cover_table_data = [[
        Paragraph('', style_body)
    ]]
    cover_accent = Table(cover_table_data, colWidths=[170*mm])
    cover_accent.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 3, ACCENT_BLUE),
    ]))
    story.append(cover_accent)
    story.append(Spacer(1, 15*mm))

    story.append(Paragraph("海南勘察招标日报", style_cover_title))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(REPORT_DATE_FULL, style_cover_subtitle))
    story.append(Spacer(1, 8*mm))

    # Divider
    div_data = [[""]]
    div = Table(div_data, colWidths=[80*mm])
    div.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1, ACCENT_ORANGE),
    ]))
    story.append(div)
    story.append(Spacer(1, 12*mm))

    story.append(Paragraph("勘察检测行业 · 招标信息日报", style_cover_subtitle))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("覆盖关键词：勘察 | 检测 | 测绘 | 岩土 | 地质灾害", style_cover_info))
    story.append(Spacer(1, 15*mm))

    story.append(Paragraph(f"数据源：中国招标投标公共服务平台 · 海南省政府采购网 · 全国公共资源交易平台(海南省)", style_cover_info))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}", style_cover_info))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("内部资料 · 仅供参考", style_cover_info))

    story.append(PageBreak())

    # ═══════════════ TABLE OF CONTENTS ═══════════════
    story.append(Paragraph("目  录", style_h1))
    story.append(Spacer(1, 8*mm))

    toc_items = [
        ("一、", "数据采集概况"),
        ("二、", "平台可访问性诊断"),
        ("三、", "勘察类招标公告明细"),
        ("四、", "数据汇总与分析"),
        ("五、", "风险提示与建议"),
        ("六、", "免责声明"),
    ]
    for num, title in toc_items:
        story.append(Paragraph(f"    {num}{title}", style_toc))
    story.append(PageBreak())

    # ═══════════════ SECTION 1: Data Collection Overview ═══════════════
    story.append(Paragraph("一、数据采集概况", style_h1))
    story.append(Paragraph(
        f"本报告基于{REPORT_DATE_FULL}自动化数据采集任务生成。任务目标为抓取中国招标投标公共服务平台"
        f"(www.cebpubservice.com)和海南省政府采购网(www.ccgp-hainan.gov.cn)最近24小时内发布的"
        f"含「勘察」「检测」「测绘」「岩土」「地质灾害」关键词的招标公告。",
        style_body
    ))
    story.append(Spacer(1, 5*mm))

    # Summary table
    summary_data = [
        [Paragraph("平台", style_table_header),
         Paragraph("计划抓取量", style_table_header),
         Paragraph("实际获取量", style_table_header),
         Paragraph("状态", style_table_header)],
        [Paragraph("中国招标投标公共服务平台", style_table_cell),
         Paragraph("50条", style_table_cell_center),
         Paragraph("0条", style_table_cell_center),
         Paragraph("502 Bad Gateway", style_table_cell)],
        [Paragraph("海南省政府采购网", style_table_cell),
         Paragraph("50条", style_table_cell_center),
         Paragraph("0条", style_table_cell_center),
         Paragraph("连接失败", style_table_cell)],
        [Paragraph("全国公共资源交易平台(海南省)", style_table_cell),
         Paragraph("-", style_table_cell_center),
         Paragraph("2条", style_table_cell_center),
         Paragraph("搜索索引获取", style_table_cell)],
    ]
    summary_tbl = Table(summary_data, colWidths=[65*mm, 35*mm, 35*mm, 35*mm])
    summary_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, TABLE_ROW_ALT]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(summary_tbl)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph(
        f"<b>结论：</b>两大目标平台均无法直接访问，通过第三方搜索引擎和海南省公共资源交易平台索引，"
        f"共获取到<b>2条</b>相关公告，其中<b>1条</b>为{REPORT_DATE_FULL}当日发布。数据量远低于预期，"
        f"建议人工检查目标网站状态或启用备用数据源。",
        style_body
    ))
    story.append(PageBreak())

    # ═══════════════ SECTION 2: Platform Diagnostics ═══════════════
    story.append(Paragraph("二、平台可访问性诊断", style_h1))

    for platform, info in platform_status.items():
        story.append(Paragraph(f"▸ <b>{platform}</b>　{info['status']}", style_h2))
        story.append(Paragraph(info['detail'], style_body))
        story.append(Spacer(1, 3*mm))

    story.append(Paragraph(
        "<b>技术说明：</b>中国招标投标公共服务平台使用了阿里云WAF(yundunwaf3.com)、"
        "海南省政府采购网服务器端连接超时，两者均无法通过常规HTTP客户端访问。"
        "建议：(1)配置浏览器自动抓取方案；(2)接入第三方付费招标数据API作为备用数据源。",
        style_body
    ))
    story.append(PageBreak())

    # ═══════════════ SECTION 3: Bid Detail Table ═══════════════
    story.append(Paragraph("三、勘察类招标公告明细", style_h1))

    if not bid_data:
        story.append(Paragraph("近期无新发布招标信息。", style_alert))
    else:
        story.append(Paragraph(
            f"以下为{REPORT_DATE_FULL}前后获取到的勘察检测类招标公告：",
            style_body
        ))
        story.append(Spacer(1, 3*mm))

        # Table headers
        col_widths = [8*mm, 52*mm, 24*mm, 28*mm, 55*mm]
        header_row = [
            Paragraph("序号", style_table_header),
            Paragraph("项目名称", style_table_header),
            Paragraph("预算金额", style_table_header),
            Paragraph("采购人", style_table_header),
            Paragraph("关键资质要求", style_table_header),
        ]
        table_data = [header_row]

        for item in bid_data:
            row = [
                Paragraph(str(item["seq"]), style_table_cell_center),
                Paragraph(f"<b>{item['title']}</b><br/>"
                          f"<font size=7 color='#64748b'>关键词: {item['keywords']}</font><br/>"
                          f"<font size=7 color='#2563eb'><link href='{item['url']}' color='#2563eb'>{item['url']}</link></font>",
                          style_table_cell),
                Paragraph(item["budget"], style_table_cell_center),
                Paragraph(item["buyer"], style_table_cell),
                Paragraph(item["qualifications"], style_table_cell),
            ]
            table_data.append(row)

        bid_tbl = Table(table_data, colWidths=col_widths, repeatRows=1)
        bid_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, TABLE_ROW_ALT]),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(bid_tbl)
        story.append(Spacer(1, 5*mm))

        # Deadline table
        story.append(Paragraph("截止日期与风险评级", style_h2))
        deadline_cols = [8*mm, 50*mm, 28*mm, 28*mm, 24*mm, 32*mm]
        deadline_header = [
            Paragraph("序号", style_table_header),
            Paragraph("项目名称", style_table_header),
            Paragraph("发布时间", style_table_header),
            Paragraph("截止日期", style_table_header),
            Paragraph("风险评级", style_table_header),
            Paragraph("风险说明", style_table_header),
        ]
        deadline_data = [deadline_header]
        for item in bid_data:
            risk_color = RED_ALERT if "中" in item["risk"] else GREEN_OK
            deadline_data.append([
                Paragraph(str(item["seq"]), style_table_cell_center),
                Paragraph(item["title"], style_table_cell),
                Paragraph(item["pub_date"], style_table_cell_center),
                Paragraph(f"<b>{item['deadline']}</b>", style_table_cell_center),
                Paragraph(f'<font color="{risk_color}"><b>{item["risk"]}</b></font>', style_table_cell_center),
                Paragraph(item["risk"] if "中" in item["risk"] else "正常", style_table_cell),
            ])

        deadline_tbl = Table(deadline_data, colWidths=deadline_cols, repeatRows=1)
        deadline_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, TABLE_ROW_ALT]),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(deadline_tbl)

    story.append(PageBreak())

    # ═══════════════ SECTION 4: Summary & Analysis ═══════════════
    story.append(Paragraph("四、数据汇总与分析", style_h1))

    story.append(Paragraph("4.1 数据有效性分析", style_h2))
    story.append(Paragraph(
        f"本次日报采集周期内({REPORT_DATE_FULL}前后24小时)，两大目标平台均处于不可访问状态。"
        f"通过替代搜索渠道获取的有效公告仅<b>2条</b>，其中：<br/>"
        f"&nbsp;&nbsp;• 当日发布勘察设计类公告：<b>1条</b>（农村公路养护工程勘察设计）<br/>"
        f"&nbsp;&nbsp;• 公告截止日为今日的测绘类公告：<b>1条</b>（测绘地理信息技术服务）<br/>"
        f"&nbsp;&nbsp;• 检测/岩土/地质灾害专项公告：<b>0条</b>",
        style_body
    ))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("4.2 项目类型分布", style_h2))
    dist_data = [
        [Paragraph("类别", style_table_header), Paragraph("数量", style_table_header), Paragraph("占比", style_table_header)],
        [Paragraph("勘察/岩土", style_table_cell), Paragraph("1", style_table_cell_center), Paragraph("50%", style_table_cell_center)],
        [Paragraph("测绘/地理信息", style_table_cell), Paragraph("1", style_table_cell_center), Paragraph("50%", style_table_cell_center)],
        [Paragraph("检测/CMA", style_table_cell), Paragraph("0", style_table_cell_center), Paragraph("0%", style_table_cell_center)],
        [Paragraph("地质灾害", style_table_cell), Paragraph("0", style_table_cell_center), Paragraph("0%", style_table_cell_center)],
        [Paragraph("<b>合计</b>", style_table_cell), Paragraph("<b>2</b>", style_table_cell_center), Paragraph("<b>100%</b>", style_table_cell_center)],
    ]
    dist_tbl = Table(dist_data, colWidths=[60*mm, 40*mm, 40*mm])
    dist_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, TABLE_ROW_ALT]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LINEABOVE', (0, -1), (-1, -1), 1, DARK_BLUE),
    ]))
    story.append(dist_tbl)

    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("4.3 预算金额汇总", style_h2))
    budget_data = [
        [Paragraph("项目", style_table_header), Paragraph("预算金额(元)", style_table_header), Paragraph("资金来源", style_table_header)],
        [Paragraph("2023年农村公路养护工程勘察设计", style_table_cell), Paragraph("见招标文件", style_table_cell_center), Paragraph("政府投资(100%)", style_table_cell_center)],
        [Paragraph("测绘地理信息技术服务项目", style_table_cell), Paragraph("4,000,000.00", style_table_cell_center), Paragraph("中央资金", style_table_cell_center)],
        [Paragraph("<b>合计(已知)</b>", style_table_cell), Paragraph("<b>4,000,000.00</b>", style_table_cell_center), Paragraph("", style_table_cell_center)],
    ]
    budget_tbl = Table(budget_data, colWidths=[65*mm, 50*mm, 55*mm])
    budget_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, TABLE_ROW_ALT]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LINEABOVE', (0, -1), (-1, -1), 1, DARK_BLUE),
    ]))
    story.append(budget_tbl)

    story.append(PageBreak())

    # ═══════════════ SECTION 5: Risk Alerts ═══════════════
    story.append(Paragraph("五、风险提示与建议", style_h1))

    story.append(Paragraph("5.1 数据完整性风险", style_h2))
    story.append(Paragraph(
        "本次日报数据采集完成率严重不足。中国招标投标公共服务平台(cebpubservice.com)和"
        "海南省政府采购网(ccgp-hainan.gov.cn)两大核心数据源均无法正常访问，导致可能遗漏大量"
        "勘察检测类招标公告。本报告数据不代表市场真实招标量。",
        style_alert
    ))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("5.2 紧急投标提醒", style_h2))
    story.append(Paragraph(
        "<b>⚠️「测绘地理信息技术服务项目(HZ2026-140)」</b>投标截止日期为<b>2026年6月11日(今日)</b>，"
        "预算金额400万元，采购人为自然资源部海南测绘资料信息中心。"
        "如需参与投标，请立即确认是否已完成投标文件递交。",
        style_alert
    ))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("5.3 资质门槛分析", style_h2))
    story.append(Paragraph(
        "本期公告涉及的核心资质要求：<br/>"
        "&nbsp;&nbsp;• 工程勘察专业类(岩土工程(勘察))乙级或以上<br/>"
        "&nbsp;&nbsp;• 测绘乙级或以上(含工程测量、界线与不动产测绘)<br/>"
        "&nbsp;&nbsp;• 注册土木工程师(岩土)执业资格<br/>"
        "资质门槛以乙级为主，适合中小型勘察测绘企业参与。",
        style_body
    ))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("5.4 改进建议", style_h2))
    suggestions = [
        "建议接入第三方招标数据API（如剑鱼标讯、千里马招标网等付费服务）作为备用数据源；",
        "建议使用浏览器自动化(Selenium/Playwright)绕过目标网站的WAF防护进行数据抓取；",
        "建议增加海南省公共资源交易平台(ggzy.hainan.gov.cn)、采招网(bidcenter.com.cn)等替代数据源的常态化监控；",
        "建议在下一次日报任务中提前检测目标平台可用性，如不可用则自动切换备用方案。",
    ]
    for s in suggestions:
        story.append(Paragraph(f"&nbsp;&nbsp;• {s}", style_body))
    story.append(Spacer(1, 10*mm))

    # ═══════════════ SECTION 6: Disclaimer ═══════════════
    story.append(Paragraph("六、免责声明", style_h1))
    story.append(Paragraph(
        "本报告由自动化分析系统生成，数据来源于公开招标平台。由于部分平台的技术防护措施，"
        "数据可能不完整。报告中的信息仅供参考，不构成投标建议。使用者应自行核实公告原文，"
        "并以招标人发布的官方公告为准。报告生成者对因使用本报告而产生的任何损失概不负责。",
        style_body_small
    ))
    story.append(Spacer(1, 8*mm))

    story.append(Paragraph(
        f"<i>报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>",
        style_body_small
    ))
    story.append(Paragraph(
        "<i>系统版本：海南勘察招标日报 v1.0 | 数据引擎：元宝搜索 + Web Fetch</i>",
        style_body_small
    ))

    # ── Build PDF ──
    doc.build(story, canvasmaker=NumberedCanvas)
    return pdf_path


if __name__ == "__main__":
    path = build_report()
    print(f"PDF report generated: {path}")
    print(f"File size: {os.path.getsize(path)} bytes")
