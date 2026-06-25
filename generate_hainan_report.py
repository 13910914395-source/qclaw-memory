#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Hainan Survey Tender Daily Report PDF."""
import sys
import os
import base64
from datetime import datetime

# Add skill scripts path
sys.path.insert(0, os.path.expanduser("~/.qclaw/skills/pdf/scripts"))
from setup_chinese_pdf import setup_chinese_pdf

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image
)
from reportlab.lib import colors
from reportlab.lib.units import cm


def build_pdf(output_path):
    cn_font, styles = setup_chinese_pdf()

    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Title'], fontSize=26,
        alignment=TA_CENTER, spaceAfter=30, leading=36
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'], fontSize=14,
        alignment=TA_CENTER, spaceAfter=12, textColor=colors.HexColor('#555555')
    )
    h1_style = ParagraphStyle(
        'H1', parent=styles['Heading1'], fontSize=18,
        spaceBefore=20, spaceAfter=12, textColor=colors.HexColor('#1a5276')
    )
    h2_style = ParagraphStyle(
        'H2', parent=styles['Heading2'], fontSize=14,
        spaceBefore=14, spaceAfter=8, textColor=colors.HexColor('#2874a6')
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'], fontSize=11,
        alignment=TA_JUSTIFY, leading=18, spaceAfter=10
    )
    small_style = ParagraphStyle(
        'Small', parent=styles['Normal'], fontSize=9,
        textColor=colors.HexColor('#666666')
    )
    table_header_style = ParagraphStyle(
        'TableHeader', parent=styles['Normal'], fontSize=10,
        textColor=colors.white, alignment=TA_CENTER, fontName=cn_font
    )
    table_cell_style = ParagraphStyle(
        'TableCell', parent=styles['Normal'], fontSize=9,
        alignment=TA_LEFT, fontName=cn_font, leading=14
    )

    report_date = "2026-06-24"
    report_title = f"【海南勘察招标日报】{report_date}"

    story = []

    # Cover page
    story.append(Spacer(1, 4 * cm))
    story.append(Paragraph(report_title, title_style))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph("勘察 · 检测 · 测绘 · 岩土 · 地质灾害", subtitle_style))
    story.append(Spacer(1, 1.5 * cm))
    story.append(Paragraph(
        f"数据来源：中国招标投标公共服务平台、海南省政府采购网<br/>"
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Asia/Shanghai)",
        subtitle_style
    ))
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph(
        "本报告尝试抓取最近24小时内含「勘察」「检测」「测绘」「岩土」「地质灾害」关键词的招标公告。",
        body_style
    ))
    story.append(PageBreak())

    # Table of contents
    story.append(Paragraph("目录", h1_style))
    toc = [
        [Paragraph("1. 执行摘要", body_style)],
        [Paragraph("2. 数据采集说明", body_style)],
        [Paragraph("3. 抓取结果汇总", body_style)],
        [Paragraph("4. 风险提示与建议", body_style)],
    ]
    toc_table = Table(toc, colWidths=[15 * cm])
    toc_table.setStyle(TableStyle([
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # Executive summary
    story.append(Paragraph("1. 执行摘要", h1_style))
    story.append(Paragraph(
        "本次日报任务计划于 2026-06-24 09:25 执行，目标为抓取中国招标投标公共服务平台"
        "（www.cebpubservice.com / ctbpsp.com）与海南省政府采购网"
        "（www.ccgp-hainan.gov.cn）最近24小时内发布的、含「勘察」「检测」「测绘」「岩土」"
        "「地质灾害」关键词的招标公告各50条，并提取项目名称、预算、采购人、资质要求、"
        "截止日期、发布时间、原文链接等字段。",
        body_style
    ))
    story.append(Paragraph(
        "经多次尝试，受目标网站反爬机制、动态单页应用（SPA）渲染、必需的安全令牌（type__1017）"
        "以及海南省政府采购网访问异常等因素影响，未能完整、稳定地获取到满足条件的公告列表。"
        "基于当前可获取的页面片段，未能在近24小时数据区中定位到足量的海南相关勘察类项目。",
        body_style
    ))
    story.append(Paragraph(
        "结论：近期无新发布招标信息可被可靠提取。",
        ParagraphStyle('Conclusion', parent=body_style, textColor=colors.HexColor('#c0392b'),
                       fontSize=12, alignment=TA_CENTER, spaceBefore=20, spaceAfter=20)
    ))

    # Data collection notes
    story.append(Paragraph("2. 数据采集说明", h1_style))
    story.append(Paragraph(
        "2.1 中国招标投标公共服务平台<br/>"
        "尝试通过官方搜索引擎 ctbpsp.com 进行关键词检索。页面为 Vue 单页应用，"
        "搜索接口需携带动态生成的 type__1017 令牌；直接调用接口返回混淆脚本而非 JSON 数据。"
        "通过浏览器自动化操作可观察到部分「接收时间：2026-06-24」的页面片段，"
        "但无法稳定进入分页结果列表，亦无法启用明确的时间筛选器。",
        body_style
    ))
    story.append(Paragraph(
        "2.2 海南省政府采购网<br/>"
        "访问 https://ccgp-hainan.gov.cn/ 时页面标题与正文均为空，疑似被反爬或网络策略拦截，"
        "无法进一步操作其时间筛选与搜索功能。",
        body_style
    ))
    story.append(Paragraph(
        "2.3 已观察到的相关片段（仅供参考，未经验证是否属于近24小时且不满足海南地域要求）<br/>"
        "• 石化工程-海南LNG二期项目地震监测系统询价采购变更公告（山东省，接收时间：2026-06-24）<br/>"
        "• 无为市皖江水库扩建工程勘察设计中标结果公告（安徽省，接收时间：2026-06-24）<br/>"
        "• 六片山森林资源保护示范基地建设项目勘察设计招标公告（广东省，接收时间：2026-06-24）",
        body_style
    ))

    # Results summary
    story.append(Paragraph("3. 抓取结果汇总", h1_style))
    data = [
        [Paragraph("数据源", table_header_style), Paragraph("目标数量", table_header_style),
         Paragraph("实际获取", table_header_style), Paragraph("状态", table_header_style)],
        [Paragraph("中国招标投标公共服务平台", table_cell_style),
         Paragraph("50", table_cell_style), Paragraph("0（完整记录）", table_cell_style),
         Paragraph("受反爬/SPA限制，无法稳定分页提取", table_cell_style)],
        [Paragraph("海南省政府采购网", table_cell_style),
         Paragraph("50", table_cell_style), Paragraph("0", table_cell_style),
         Paragraph("页面访问异常，无法加载", table_cell_style)],
    ]
    t = Table(data, colWidths=[5 * cm, 2.5 * cm, 2.5 * cm, 5 * cm], repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e4057')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        "由于未获取到有效记录，项目明细表格（含预算、采购人、资质要求、截止日期、原文链接）"
        "本次无法生成。",
        body_style
    ))

    # Risks and suggestions
    story.append(Paragraph("4. 风险提示与建议", h1_style))
    story.append(Paragraph(
        "4.1 数据风险<br/>"
        "当前报告未包含可验证的招标项目，任何基于本报告的投标决策应另行通过官方渠道复核。",
        body_style
    ))
    story.append(Paragraph(
        "4.2 技术建议<br/>"
        "• 如需稳定采集，建议申请中国招标投标公共服务平台的信息定制/信息API服务；<br/>"
        "• 海南省政府采购网可尝试通过政府采购网统一平台或海南分网提供的 RSS/数据接口获取；<br/>"
        "• 可考虑接入第三方招投标数据服务（如采招网、比比招标网等）作为补充数据源。",
        body_style
    ))

    # Footer function
    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont(cn_font, 9)
        canvas.setFillColor(colors.HexColor('#666666'))
        footer_text = f"{report_title}  |  第 {doc.page} 页  |  自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        canvas.drawRightString(A4[0] - 1.5 * cm, 1 * cm, footer_text)
        canvas.drawString(1.5 * cm, 1 * cm, "海南勘察招标日报")
        canvas.restoreState()

    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            rightMargin=1.5 * cm, leftMargin=1.5 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm)
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)


def main():
    output_path = os.path.join(os.path.dirname(__file__), "海南勘察招标日报_2026-06-24.pdf")
    build_pdf(output_path)
    with open(output_path, 'rb') as f:
        data = f.read()
    print(base64.b64encode(data).decode('utf-8'))


if __name__ == '__main__':
    main()
