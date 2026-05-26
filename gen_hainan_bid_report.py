#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""海南勘察招标日报生成器 2026-04-16"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os, datetime

# 中文字体路径（macOS系统字体）
FONT_PATHS = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
]

def get_font():
    for fp in FONT_PATHS:
        if os.path.exists(fp):
            try:
                pdfmetrics.registerFont(TTFont('ChineseFont', fp))
                return 'ChineseFont'
            except:
                pass
    return 'Helvetica'

FONT_NAME = get_font()

PAGE_W, PAGE_H = A4
MARGIN = 1.8*cm

# 颜色
COLOR_DARK_BLUE = colors.HexColor('#1a3a5c')
COLOR_MID_BLUE  = colors.HexColor('#2e6da4')
COLOR_LIGHT_BLUE = colors.HexColor('#d0e4f5')
COLOR_ACCENT    = colors.HexColor('#e85c2a')
COLOR_GRAY      = colors.HexColor('#6b7280')
COLOR_LIGHT_GRAY= colors.HexColor('#f3f4f6')
COLOR_WHITE     = colors.white
COLOR_BLACK     = colors.black
COLOR_RED       = colors.HexColor('#dc2626')
COLOR_GREEN     = colors.HexColor('#16a34a')

def make_styles():
    base = getSampleStyleSheet()
    s = {}
    s['title'] = ParagraphStyle('CustomTitle',
        fontName=FONT_NAME, fontSize=20, leading=26,
        textColor=COLOR_WHITE, alignment=TA_CENTER, spaceAfter=6)
    s['subtitle'] = ParagraphStyle('Subtitle',
        fontName=FONT_NAME, fontSize=12, leading=16,
        textColor=COLOR_LIGHT_BLUE, alignment=TA_CENTER, spaceAfter=4)
    s['h1'] = ParagraphStyle('H1',
        fontName=FONT_NAME, fontSize=14, leading=20,
        textColor=COLOR_DARK_BLUE, spaceBefore=12, spaceAfter=6,
        borderPad=4)
    s['h2'] = ParagraphStyle('H2',
        fontName=FONT_NAME, fontSize=11, leading=16,
        textColor=COLOR_MID_BLUE, spaceBefore=8, spaceAfter=4)
    s['body'] = ParagraphStyle('Body',
        fontName=FONT_NAME, fontSize=9, leading=14,
        textColor=COLOR_BLACK, spaceAfter=4)
    s['small'] = ParagraphStyle('Small',
        fontName=FONT_NAME, fontSize=7.5, leading=11,
        textColor=COLOR_GRAY)
    s['cell'] = ParagraphStyle('Cell',
        fontName=FONT_NAME, fontSize=8.5, leading=12,
        textColor=COLOR_BLACK)
    s['cell_bold'] = ParagraphStyle('CellBold',
        fontName='Helvetica-Bold', fontSize=8.5, leading=12,
        textColor=COLOR_BLACK)
    s['cell_small'] = ParagraphStyle('CellSmall',
        fontName=FONT_NAME, fontSize=7.5, leading=10,
        textColor=COLOR_GRAY)
    s['warn'] = ParagraphStyle('Warn',
        fontName=FONT_NAME, fontSize=9, leading=13,
        textColor=COLOR_RED)
    return s

def header_footer(canvas, doc):
    canvas.saveState()
    # 页眉
    canvas.setFillColor(COLOR_DARK_BLUE)
    canvas.rect(MARGIN, PAGE_H - 1.4*cm, PAGE_W - 2*MARGIN, 0.5*cm, fill=1, stroke=0)
    canvas.setFillColor(COLOR_WHITE)
    canvas.setFont(FONT_NAME, 8)
    canvas.drawCentredString(PAGE_W/2, PAGE_H - 1.1*cm,
        f"海南勘察招标日报 | {doc.report_date} | 仅供参考，以原文为准")
    # 页脚
    canvas.setFillColor(COLOR_GRAY)
    canvas.setFont(FONT_NAME, 7.5)
    canvas.drawCentredString(PAGE_W/2, 0.8*cm,
        f"第 {doc.page} 页  |  数据来源：中国招标投标公共服务平台 / 海南省政府采购网  |  生成时间：{doc.gen_time}")
    canvas.restoreState()

def build_cover(styles):
    elems = []
    # 蓝色顶部横幅
    cover_data = [[Paragraph('海南勘察招标日报', styles['title'])],
                  [Paragraph('Hainan Survey & Testing Tendering Daily Report', styles['subtitle'])]]
    cover_table = Table(cover_data, colWidths=[PAGE_W - 2*MARGIN])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_DARK_BLUE),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('ROUNDEDCORNERS', [8,8,8,8]),
    ]))
    elems.append(cover_table)
    elems.append(Spacer(1, 0.6*cm))

    # 日期信息框
    date_str = "2026年4月16日（星期四）"
    period_str = "统计周期：2026-04-15 09:13 至 2026-04-16 09:13（最近24小时）"
    info_data = [
        [Paragraph(f'<b>报告日期</b>', styles['cell']), Paragraph(date_str, styles['cell'])],
        [Paragraph(f'<b>统计周期</b>', styles['cell']), Paragraph(period_str, styles['cell'])],
        [Paragraph(f'<b>关键词</b>', styles['cell']),
         Paragraph('勘察 / 检测 / 测绘 / 岩土 / 地质灾害', styles['cell'])],
        [Paragraph(f'<b>数据来源</b>', styles['cell']),
         Paragraph('中国招标投标公共服务平台 / 海南省政府采购网 / 行业招标平台', styles['cell'])],
        [Paragraph(f'<b>搜索结果</b>', styles['cell']),
         Paragraph('🔴 最近24小时内，两大官方平台均无直接匹配海南勘察类新发布公告', styles['warn'])],
    ]
    info_table = Table(info_data, colWidths=[3.5*cm, PAGE_W-2*MARGIN-3.5*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_LIGHT_GRAY),
        ('BACKGROUND', (0,0), (0,-1), COLOR_LIGHT_BLUE),
        ('FONTNAME', (0,0), (0,-1), FONT_NAME),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [COLOR_LIGHT_BLUE, COLOR_LIGHT_GRAY]),
    ]))
    elems.append(info_table)
    elems.append(Spacer(1, 0.5*cm))

    # 摘要框
    summary_text = (
        '本报告统计周期内（最近24小时），通过中国招标投标公共服务平台（www.cebpubservice.com）和'
        '海南省政府采购网（www.ccgp-hainan.gov.cn）及主流行业招标平台进行多轮关键词检索，'
        '<b>结果如下：</b><br/><br/>'
        '① <b>中国招标投标公共服务平台</b>：以「勘察/检测/测绘/岩土/地质灾害+海南」为关键词检索，'
        '最近24小时内无直接匹配的新发布勘察类招标公告。<br/>'
        '② <b>海南省政府采购网</b>：以同类关键词检索，官方平台上无近24小时内的勘察检测类采购公告。<br/>'
        '③ <b>行业招标平台</b>：中国招标与采购网海南站、采招网海南页、招标采购导航网三亚站等存在少量招标动态，'
        '但经智能筛选，排除仅含"勘察"字样的无关项目（如工程监理、可行性研究等），'
        '<b>近24小时内无符合严格定义的勘察/检测/测绘类真实项目新增发布。</b><br/><br/>'
        '⚠️ <b><font color="red">风险提示：</font></b>若存在未被平台收录或延迟发布的信息，请以官方平台实时数据为准。'
    )
    summary_para = Paragraph(summary_text, styles['body'])
    summary_table = Table([[summary_para]], colWidths=[PAGE_W-2*MARGIN])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fff7ed')),
        ('BOX', (0,0), (-1,-1), 1.5, COLOR_ACCENT),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    elems.append(summary_table)
    elems.append(Spacer(1, 0.4*cm))

    # 目录
    elems.append(Paragraph('目录 | Table of Contents', styles['h1']))
    toc_items = [
        ('一', '数据来源与说明'),
        ('二', '近期行业动态摘要'),
        ('三', '附：近7日行业相关公告（非本周期）'),
        ('四', '投标建议与风险提示'),
    ]
    for num, title in toc_items:
        row_data = [[Paragraph(f'<b>{num}</b>', styles['cell_bold']),
                     Paragraph(title, styles['cell'])]]
        t = Table(row_data, colWidths=[1*cm, PAGE_W-2*MARGIN-1*cm])
        t.setStyle(TableStyle([
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LINEBELOW', (0,0), (-1,-1), 0.3, colors.HexColor('#e5e7eb')),
        ]))
        elems.append(t)
    elems.append(PageBreak())
    return elems

def build_section1(styles):
    elems = []
    elems.append(Paragraph('一、数据来源与说明', styles['h1']))
    elems.append(HRFlowable(width='100%', thickness=1.5, color=COLOR_MID_BLUE, spaceAfter=6))

    desc = (
        "本报告依据以下规则进行数据采集与筛选：<br/>"
        "• <b>数据源：</b>中国招标投标公共服务平台（www.cebpubservice.com）、"
        "海南省政府采购网（www.ccgp-hainan.gov.cn）及中国招标与采购网、"
        "采招网、中国电力招标网、招标采购导航网等主流行业平台<br/>"
        "• <b>关键词：</b>勘察 / 检测 / 测绘 / 岩土 / 地质灾害（多关键词OR组合）<br/>"
        "• <b>地域限定：</b>海南省 + 全国平台泛检<br/>"
        "• <b>时间范围：</b>最近24小时（2026-04-15 09:13 至 2026-04-16 09:13）<br/>"
        "• <b>筛选逻辑：</b>智能过滤仅含&ldquo;勘察/检测&rdquo;字样的非相关项目（如勘察设计、可行性研究含勘察字样、监理含检测字样等），"
        "保留真实勘察类、检测类、测绘类、岩土工程类、地质灾害类项目<br/>"
        "• <b>智能识别标准：</b>项目名称中包含工程勘察、物探、钻探、岩土测试、变形监测、"
        "CMA检测、测绘地形图、不动产测绘、地质灾害危险性评估等实质性内容"
    )
    elems.append(Paragraph(desc, styles['body']))
    elems.append(Spacer(1, 0.4*cm))
    return elems

def build_section2(styles):
    elems = []
    elems.append(Paragraph('二、近期行业动态摘要', styles['h1']))
    elems.append(HRFlowable(width='100%', thickness=1.5, color=COLOR_MID_BLUE, spaceAfter=6))
    elems.append(Paragraph(
        '<font color="#dc2626"><b>⚠ 重要提示：近24小时内（2026-04-15 09:13 ~ 2026-04-16 09:13），'
        '在指定数据源中未检索到符合条件的海南勘察/检测/测绘/岩土/地质灾害类新发布招标公告。</b></font>',
        styles['body']))
    elems.append(Spacer(1, 0.3*cm))
    elems.append(Paragraph(
        '以下为近24小时内，两大官方平台及行业平台检索到的相关动态，供您参考：',
        styles['body']))
    elems.append(Spacer(1, 0.2*cm))

    # 近24小时相关公告（非严格勘察类）
    headers = ['序号','项目名称','类型','平台来源','发布时间','风险提示']
    rows = [
        ['1','海南公司2026-2028年地质勘察集中采购-地质勘察服务（变更资审公告）',
         '招标公告\n（变更）','中国招标与采购网\n海南站', '2026-04-14','⚠ 公告变更，非新发布；建议核实资质变更内容'],
        ['2','三亚健康城项目HT09-15...',
         '招标公告','招标采购导航网\n三亚站', '2026-04-15','⚠ 名称含工程编号，建议核实是否属勘察类项目'],
        ['3','南山岭项目（机器管招投标）',
         '招标公告','招标采购导航网\n三亚站', '2026-04-15','⚠ 具体类别待核实，疑似工程项目'],
        ['4','东岸农贸市场提质升级工程...',
         '招标公告','招标采购导航网\n三亚站', '2026-04-15','⚠ 市政工程，非勘察检测专项'],
        ['5','S212隆永线路面修复养护工程',
         '招标公告','采招网海南', '2026-04-07','⛔ 发布时间已超过24小时'],
    ]

    col_widths = [0.7*cm, 6.8*cm, 2.0*cm, 2.8*cm, 2.0*cm, 3.5*cm]
    table_data = [[Paragraph(h, styles['cell_bold']) for h in headers]]
    for row in rows:
        table_data.append([Paragraph(str(c), styles['cell_small']) for c in row])

    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_DARK_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), COLOR_WHITE),
        ('FONTNAME', (0,0), (-1,0), FONT_NAME),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('FONTNAME', (0,1), (-1,-1), FONT_NAME),
        ('FONTSIZE', (0,1), (-1,-1), 7.5),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('ALIGN', (0,1), (0,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#94a3b8')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [COLOR_WHITE, COLOR_LIGHT_GRAY]),
        ('TEXTCOLOR', (5,1), (5,-1), COLOR_RED),
    ]))
    elems.append(t)
    elems.append(Spacer(1, 0.4*cm))
    return elems

def build_section3(styles):
    elems = []
    elems.append(Paragraph('三、附：近7日行业相关公告（非本周期）', styles['h1']))
    elems.append(HRFlowable(width='100%', thickness=1.5, color=COLOR_MID_BLUE, spaceAfter=6))
    elems.append(Paragraph(
        '以下为近7日内海南区域与勘察/检测/测绘相关的公告（供参考，非本次日报统计范围）：',
        styles['body']))
    elems.append(Spacer(1, 0.2*cm))

    headers3 = ['序号','项目名称','类型','平台来源','发布时间','预算金额（参考）']
    rows3 = [
        ['1','富岛公司监控盲区增补项目','招标预告','采招网海南','2026/4/13','未公开'],
        ['2','2026年上半年检验科理化项目检测试剂耗材采购','中标结果','采招网海南','2026/4/9','未公开'],
        ['3','2026年度海洋调查观测监测业务辅助服务项目','中标结果','采招网海南','2026/4/7','未公开'],
        ['4','S212隆永线路面修复养护工程','招标公告','采招网海南','2026/4/7','未公开'],
        ['5','海南省建设项目用地报批技术审查及备案入库服务','中标结果','采招网海南','2026/4/9','未公开'],
        ['6','国投洋浦港有限公司加油站2026年防雷装置检测项目','中标结果','采招网海南','2026/4/9','未公开'],
        ['7','海南公司2026-2028年地质勘察集中采购-地质勘察服务','招标公告\n（变更）','中国招标与采购网','2026/4/14','未公开'],
        ['8','中石油海南销售有限公司2026-2028年建设项目监理服务','招标公告','国际石油网','2026/4/14','150万元\n（含税）'],
    ]
    col_widths3 = [0.7*cm, 6.5*cm, 1.8*cm, 2.5*cm, 1.8*cm, 2.5*cm]
    table_data3 = [[Paragraph(h, styles['cell_bold']) for h in headers3]]
    for row in rows3:
        table_data3.append([Paragraph(str(c), styles['cell_small']) for c in row])
    t3 = Table(table_data3, colWidths=col_widths3, repeatRows=1)
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_MID_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), COLOR_WHITE),
        ('FONTNAME', (0,0), (-1,0), FONT_NAME),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('FONTNAME', (0,1), (-1,-1), FONT_NAME),
        ('FONTSIZE', (0,1), (-1,-1), 7.5),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('ALIGN', (0,1), (0,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#94a3b8')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [COLOR_WHITE, COLOR_LIGHT_GRAY]),
    ]))
    elems.append(t3)
    elems.append(Spacer(1, 0.3*cm))
    return elems

def build_section4(styles):
    elems = []
    elems.append(Paragraph('四、投标建议与风险提示', styles['h1']))
    elems.append(HRFlowable(width='100%', thickness=1.5, color=COLOR_MID_BLUE, spaceAfter=6))

    tips = [
        ('🔴 无近期数据应对策略',
         '• 近24小时无新增公告属正常情况，建议每日上午9:00-10:00定期刷新官方平台\n'
         '• 可关注各平台"最近三天"筛选功能扩大扫描范围\n'
         '• 中国招标投标公共服务平台支持按地区、关键词、时间联合筛选，建议收藏搜索URL'),
        ('🟡 关注延期/变更公告',
         '• 已发布的勘察集中采购公告可能出现变更（如海南公司2026-2028年地质勘察集中采购）\n'
         '• 建议跟踪已报名项目的澄清/变更通知，避免错过关键信息\n'
         '• 关注"资审公告变更"类文件，确认资质要求是否调整'),
        ('🟢 资质储备建议',
         '• 工程勘察综合资质甲级 / 岩土工程专项资质\n'
         '• CMA计量认证（检验检测机构资质认定）\n'
         '• 测绘乙级及以上资质（工程测量、界限与不动产测绘）\n'
         '• 地质灾害危险性评估资质\n'
         '• 建议提前准备上述资质证书电子版，确保投标时即传即用'),
        ('🔵 海南市场专项建议',
         '• 海南自贸港建设推动基础设施投资加速，关注省级重点项目中涉及地质勘察的分包机会\n'
         '• 海南自然灾害（台风、强降雨）频发，地质灾害排查与治理类项目具有持续性需求\n'
         '• 关注三亚、海口、儋州（含洋浦）三大重点区域的政府投资项目'),
    ]
    for title, content in tips:
        tip_data = [
            [Paragraph(f'<b>{title}</b>', styles['cell_bold'])],
            [Paragraph(content, styles['cell'])],
        ]
        tt = Table(tip_data, colWidths=[PAGE_W-2*MARGIN])
        tt.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_LIGHT_BLUE),
            ('BACKGROUND', (0,1), (-1,1), COLOR_WHITE),
            ('BOX', (0,0), (-1,-1), 0.8, COLOR_MID_BLUE),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        elems.append(tt)
        elems.append(Spacer(1, 0.25*cm))
    return elems

def build_report():
    report_date = "2026-04-16"
    gen_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    output_path = "/Users/fasimac/.qclaw/workspace/海南勘察招标日报_2026-04-16.pdf"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=1.8*cm,
        bottomMargin=1.5*cm,
        title=f"海南勘察招标日报 {report_date}",
        author="QClaw AI Agent",
        subject="勘察检测行业招标分析",
    )
    doc.report_date = report_date
    doc.gen_time = gen_time

    styles = make_styles()
    story = []
    story.extend(build_cover(styles))
    story.extend(build_section1(styles))
    story.extend(build_section2(styles))
    story.extend(build_section3(styles))
    story.extend(build_section4(styles))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF已生成: {output_path}")
    return output_path

if __name__ == '__main__':
    build_report()
