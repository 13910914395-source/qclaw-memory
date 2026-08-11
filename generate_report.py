#!/usr/bin/env python3
"""Generate 海南勘察招标日报 PDF Report - 2026-08-11"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime, os

# Register Chinese fonts
font_paths = {
    'hei': '/System/Library/Fonts/STHeiti Medium.ttc',
    'song': '/System/Library/Fonts/Supplemental/Songti.ttc',
}
pdfmetrics.registerFont(TTFont('Hei', font_paths['hei']))
pdfmetrics.registerFont(TTFont('Song', font_paths['song']))
pdfmetrics.registerFont(TTFont('Hei-Bold', font_paths['hei']))

PAGE_W, PAGE_H = A4

def build_styles():
    styles = getSampleStyleSheet()
    base = {
        'fontName': 'Hei',
        'fontSize': 10,
        'leading': 14,
        'textColor': colors.black,
    }
    s = {}
    s['title'] = ParagraphStyle('title', fontName='Hei-Bold', fontSize=20, leading=28,
                                 alignment=TA_CENTER, spaceAfter=6, textColor=colors.HexColor('#1a3a6c'))
    s['subtitle'] = ParagraphStyle('subtitle', fontName='Hei', fontSize=12, leading=16,
                                    alignment=TA_CENTER, spaceAfter=4, textColor=colors.HexColor('#2c5aa0'))
    s['meta'] = ParagraphStyle('meta', fontName='Song', fontSize=9, leading=12,
                                alignment=TA_CENTER, textColor=colors.gray)
    s['h1'] = ParagraphStyle('h1', fontName='Hei-Bold', fontSize=14, leading=20,
                               spaceBefore=12, spaceAfter=6, textColor=colors.HexColor('#1a3a6c'))
    s['h2'] = ParagraphStyle('h2', fontName='Hei-Bold', fontSize=11, leading=16,
                               spaceBefore=8, spaceAfter=4, textColor=colors.HexColor('#2c5aa0'))
    s['h3'] = ParagraphStyle('h3', fontName='Hei-Bold', fontSize=10, leading=14,
                               spaceBefore=6, spaceAfter=3, textColor=colors.HexColor('#333333'))
    s['body'] = ParagraphStyle('body', fontName='Song', fontSize=9, leading=13,
                                spaceBefore=2, spaceAfter=2, alignment=TA_JUSTIFY)
    s['body_bold'] = ParagraphStyle('body_bold', fontName='Hei-Bold', fontSize=9, leading=13,
                                     spaceBefore=2, spaceAfter=2)
    s['table_header'] = ParagraphStyle('th', fontName='Hei-Bold', fontSize=8, leading=10,
                                        alignment=TA_CENTER, textColor=colors.white)
    s['table_cell'] = ParagraphStyle('td', fontName='Song', fontSize=7.5, leading=10,
                                      alignment=TA_LEFT)
    s['table_cell_c'] = ParagraphStyle('tdc', fontName='Song', fontSize=7.5, leading=10,
                                        alignment=TA_CENTER)
    s['warn'] = ParagraphStyle('warn', fontName='Hei', fontSize=9, leading=13,
                                spaceBefore=4, spaceAfter=4, textColor=colors.HexColor('#c0392b'))
    s['footer'] = ParagraphStyle('footer', fontName='Song', fontSize=7.5, leading=10,
                                  alignment=TA_CENTER, textColor=colors.gray)
    s['toc_item'] = ParagraphStyle('toc', fontName='Song', fontSize=9, leading=14)
    return s

def header_footer(canvas, doc):
    canvas.saveState()
    # Header line
    canvas.setStrokeColor(colors.HexColor('#1a3a6c'))
    canvas.setLineWidth(1.5)
    canvas.line(2*cm, PAGE_H - 1.5*cm, PAGE_W - 2*cm, PAGE_H - 1.5*cm)
    # Header text
    canvas.setFont('Hei', 7.5)
    canvas.setFillColor(colors.HexColor('#1a3a6c'))
    canvas.drawString(2*cm, PAGE_H - 1.2*cm, '海南勘察招标日报')
    canvas.drawRightString(PAGE_W - 2*cm, PAGE_H - 1.2*cm, '中国招标投标公共服务平台 · 海南省政府采购网')
    # Footer line
    canvas.setLineWidth(0.5)
    canvas.setStrokeColor(colors.gray)
    canvas.line(2*cm, 1.5*cm, PAGE_W - 2*cm, 1.5*cm)
    # Footer text
    canvas.setFont('Song', 7.5)
    canvas.setFillColor(colors.gray)
    canvas.drawString(2*cm, 1.1*cm, f'第 {doc.page} 页  ·  生成时间：2026-08-11 03:00')
    canvas.drawRightString(PAGE_W - 2*cm, 1.1*cm, '内部参考 · 仅供参考')
    canvas.restoreState()

def build_cover(s):
    elems = []
    elems.append(Spacer(1, 3*cm))
    # Blue decorative bar
    elems.append(HRFlowable(width='100%', thickness=4, color=colors.HexColor('#1a3a6c'),
                              spaceAfter=0.5*cm))
    elems.append(Spacer(1, 1*cm))
    elems.append(Paragraph('海南勘察招标日报', s['title']))
    elems.append(Paragraph('Hainan Survey & Inspection Tendering Daily Report', s['subtitle']))
    elems.append(Spacer(1, 0.3*cm))
    elems.append(Paragraph('2026-08-11', ParagraphStyle('date_cover', fontName='Hei-Bold',
                fontSize=28, leading=34, alignment=TA_CENTER,
                textColor=colors.HexColor('#1a3a6c'))))
    elems.append(Spacer(1, 0.5*cm))
    elems.append(HRFlowable(width='60%', thickness=1.5, color=colors.HexColor('#2c5aa0'),
                              hAlign='CENTER', spaceAfter=0.5*cm))
    elems.append(Spacer(1, 1*cm))

    meta_data = [
        ['数据统计周期', '2026-08-10 03:00 ~ 2026-08-11 03:00（最近24小时）'],
        ['数据来源', '中国招标投标公共服务平台 · 海南省政府采购网'],
        ['关键词', '勘察 / 检测 / 测绘 / 岩土 / 地质灾害'],
        ['报告生成时间', '2026-08-11 03:00'],
        ['编制单位', '招标情报分析中心'],
    ]
    meta_table = Table(meta_data, colWidths=[4*cm, 11*cm])
    meta_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Song'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('FONTNAME', (0,0), (0,-1), 'Hei-Bold'),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#1a3a6c')),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f4fb')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor('#e8edf7'), colors.HexColor('#f0f4fb')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#c0cfe0')),
    ]))
    elems.append(meta_table)
    elems.append(Spacer(1, 2*cm))

    # Alert box
    alert_data = [[Paragraph(
        '⚠ 重要提示：经全面扫描，中国招标投标公共服务平台今日访问受限（触发表单验证），'
        '海南省政府采购网近24小时内（统计周期内）无新增勘察/检测/测绘/岩土/地质灾害相关招标公告。'
        '最近一条相关公告发布于 2026-08-08（三天前）。',
        ParagraphStyle('alert_p', fontName='Song', fontSize=9, leading=13,
                       textColor=colors.HexColor('#7d0000'))
    )]]
    alert_table = Table(alert_data, colWidths=[15*cm])
    alert_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fff3cd')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#e67e22')),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    elems.append(alert_table)
    elems.append(PageBreak())
    return elems

def build_toc(s):
    elems = []
    elems.append(Paragraph('目 录', s['title']))
    elems.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#1a3a6c'),
                              spaceAfter=0.5*cm))
    toc_items = [
        ('一、执行摘要', '3'),
        ('二、数据来源与抓取情况', '3'),
        ('三、海南省勘察类公告统计', '4'),
        ('四、公告清单（按关键词分类）', '4'),
        ('  4.1 勘察类公告', '4'),
        ('  4.2 检测类公告', '4'),
        ('  4.3 其他相关公告', '5'),
        ('五、资质要求提取', '5'),
        ('六、风险提示与建议', '6'),
        ('七、附录：近期历史公告摘要', '6'),
    ]
    for item, page in toc_items:
        row = Table([[Paragraph(item, s['toc_item']),
                      Paragraph(page, s['toc_item'])]],
                     colWidths=[13*cm, 2*cm])
        row.setStyle(TableStyle([
            ('ALIGN', (1,0), (1,0), 'RIGHT'),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        elems.append(row)
    elems.append(PageBreak())
    return elems

def build_summary(s):
    elems = []
    elems.append(Paragraph('一、执行摘要', s['h1']))
    elems.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#2c5aa0'),
                              spaceAfter=0.3*cm))
    summary = (
        '本报告汇总统计了2026年8月10日至8月11日（最近24小时）内，'
        '中国招标投标公共服务平台与海南省政府采购网发布的涉及勘察、检测、测绘、'
        '岩土及地质灾害等关键词的政府采购与招标公告。'
        '经全面扫描，数据情况如下：'
    )
    elems.append(Paragraph(summary, s['body']))
    elems.append(Spacer(1, 0.3*cm))

    # Summary stats table
    stats = [
        ['数据来源', '状态', '扫描结果', '最近发布'],
        ['中国招标投标公共服务平台', '❌ 访问受限', '触发人机验证，无法抓取', '无法获取'],
        ['海南省政府采购网', '✅ 正常访问', '共扫描149条"勘察"关键词公告', '2026-08-08'],
        ['海南省政府采购网 - 检测', '✅ 正常访问', '共扫描相关公告', '2026-08-03'],
        ['海南省政府采购网 - 测绘', '✅ 正常访问', '无相关公告', '—'],
        ['海南省政府采购网 - 岩土', '✅ 正常访问', '无相关公告', '—'],
        ['海南省政府采购网 - 地质灾害', '✅ 正常访问', '无相关公告', '—'],
    ]
    st = Table(stats, colWidths=[5.5*cm, 2.8*cm, 5.5*cm, 2.2*cm])
    st.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3a6c')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Hei-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('FONTNAME', (0,1), (-1,-1), 'Song'),
        ('FONTSIZE', (0,1), (-1,-1), 7.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f0f4fb')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#c0cfe0')),
    ]))
    elems.append(st)
    elems.append(Spacer(1, 0.5*cm))

    elems.append(Paragraph('二、数据来源与抓取情况', s['h1']))
    elems.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#2c5aa0'),
                              spaceAfter=0.3*cm))

    src_data = [
        ['平台', '网址', '访问状态', '备注'],
        ['中国招标投标公共服务平台', 'www.cebpubservice.com', '❌ 受限',
         '触发网易易盾人机验证(CAPTCHA)，无法自动化抓取；直接API调用返回404（接口已迁移）'],
        ['海南省政府采购网', 'www.ccgp-hainan.gov.cn', '✅ 正常',
         '成功抓取全部公告，通过关键词"勘察/检测/测绘/岩土/地质灾害"筛选，最近24小时内无新增'],
    ]
    st2 = Table(src_data, colWidths=[4.5*cm, 5*cm, 1.8*cm, 4.7*cm])
    st2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3a6c')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Hei-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('FONTNAME', (0,1), (-1,-1), 'Song'),
        ('FONTSIZE', (0,1), (-1,-1), 7),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#fff8f0'), colors.HexColor('#f0f8ff')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#c0cfe0')),
    ]))
    elems.append(st2)
    elems.append(PageBreak())
    return elems

def build_notice_table(s, notices, title, subtitle):
    """Build a table of notices"""
    elems = []
    elems.append(Paragraph(title, s['h1']))
    elems.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#2c5aa0'),
                              spaceAfter=0.2*cm))
    elems.append(Paragraph(subtitle, s['body']))
    elems.append(Spacer(1, 0.3*cm))

    if not notices:
        elems.append(Paragraph(
            '⚠ 统计周期内（2026-08-10 03:00 ~ 2026-08-11 03:00）无新增公告。'
            '最近一条相关公告发布于2026-08-08。',
            s['warn']))
        return elems

    headers = ['序号', '项目名称', '采购人/代理机构', '发布时间', '关键词']
    col_widths = [1*cm, 7*cm, 3.5*cm, 2*cm, 1.5*cm]

    header_row = [Paragraph(h, s['table_header']) for h in headers]
    data = [header_row]

    for i, n in enumerate(notices):
        row = [
            str(i+1),
            Paragraph(n.get('name','')[:80], s['table_cell']),
            Paragraph(n.get('org','')[:40], s['table_cell']),
            n.get('date',''),
            n.get('keyword',''),
        ]
        data.append(row)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3a6c')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Hei-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('FONTNAME', (0,1), (-1,-1), 'Song'),
        ('FONTSIZE', (0,1), (-1,-1), 7.5),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (3,0), (3,-1), 'CENTER'),
        ('ALIGN', (4,0), (4,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f0f4fb')]),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#c0cfe0')),
    ]))
    elems.append(t)
    elems.append(Spacer(1, 0.5*cm))
    return elems

def build_risk_section(s):
    elems = []
    elems.append(Paragraph('六、风险提示与建议', s['h1']))
    elems.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#2c5aa0'),
                              spaceAfter=0.3*cm))

    risks = [
        ('⚠️ 数据缺失风险',
         '中国招标投标公共服务平台今日触发表单验证，无法自动化抓取全国数据，建议人工复核。'),
        ('⚠️ 发布空档期',
         '海南省近24小时内（2026-08-10~08-11）无勘察/检测/测绘/岩土/地质灾害相关公告，'
         '可能存在发布延迟或假期效应。'),
        ('📌 关注历史公告',
         '最近一条相关公告（质量监督检测机构采购）发布于2026-08-03，建议持续跟踪该类项目后续招标。'),
        ('📌 关注地质勘查需求',
         '海口市琼山区旧州镇矿泉水地质勘查项目（2026-06-29）已公示，'
         '近期可能有配套勘察服务采购需求。'),
        ('💡 建议',
         '1) 建议关注海南省公共资源交易网（ggzy.hainan.gov.cn）扩大数据源；'
         '2) 建议明日重新扫描，关注周末发布的小批量公告；'
         '3) 岩土/地质灾害类公告建议同时关注海南省自然资源和规划厅网站。'),
    ]

    for title, content in risks:
        row_data = [[
            Paragraph(f'<b>{title}</b>', ParagraphStyle('rh', fontName='Hei-Bold',
                      fontSize=9, leading=13, textColor=colors.HexColor('#1a3a6c'))),
            Paragraph(content, s['body'])
        ]]
        rt = Table(row_data, colWidths=[3.5*cm, 12.5*cm])
        rt.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('LINEABOVE', (0,0), (-1,-1), 0.5, colors.HexColor('#e0e8f0')),
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fafbfe')),
        ]))
        elems.append(rt)
        elems.append(Spacer(1, 0.2*cm))

    return elems

def build_appendix(s, history_notices):
    elems = []
    elems.append(Paragraph('七、附录：近期历史公告摘要（参考）', s['h1']))
    elems.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#2c5aa0'),
                              spaceAfter=0.3*cm))
    elems.append(Paragraph(
        '以下为海南省政府采购网上近期（统计周期外）发布的相关公告，供业务参考：',
        s['body']))
    elems.append(Spacer(1, 0.3*cm))

    if history_notices:
        headers = ['序号', '项目名称', '采购人', '发布时间', '类型']
        col_widths = [1*cm, 7.5*cm, 3*cm, 2*cm, 2.5*cm]
        header_row = [Paragraph(h, s['table_header']) for h in headers]
        data = [header_row]
        for i, n in enumerate(history_notices):
            row = [
                str(i+1),
                Paragraph(n.get('name','')[:80], s['table_cell']),
                Paragraph(n.get('org','')[:35], s['table_cell']),
                n.get('date',''),
                n.get('type',''),
            ]
            data.append(row)
        t = Table(data, colWidths=col_widths, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Hei-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 8),
            ('FONTNAME', (0,1), (-1,-1), 'Song'),
            ('FONTSIZE', (0,1), (-1,-1), 7.5),
            ('ALIGN', (0,0), (0,-1), 'CENTER'),
            ('ALIGN', (3,0), (3,-1), 'CENTER'),
            ('ALIGN', (4,0), (4,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 3),
            ('RIGHTPADDING', (0,0), (-1,-1), 3),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f0f8ff')]),
            ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#c0cfe0')),
        ]))
        elems.append(t)
    return elems

def generate_pdf(output_path):
    s = build_styles()

    # Actual notice data from Hainan CCGP
    notices_24h = []  # No notices in last 24 hours

    history_notices = [
        {
            'name': '澄迈县2026年"十三五"时期耕地流失整改复耕全过程技术服务项目结果公告',
            'org': '澄迈县农业农村局',
            'date': '2026-08-08',
            'type': '中标结果公告',
            'keyword': '勘察'
        },
        {
            'name': '金牌西作业区规划修订(二次)结果公告',
            'org': '临高县交通运输局',
            'date': '2026-08-04',
            'type': '中标结果公告',
            'keyword': '勘察'
        },
        {
            'name': 'G98环岛高速公路大三亚段扩容工程质量监督检测机构采购更正公告',
            'org': '海南省交通工程质量监督管理局',
            'date': '2026-08-03',
            'type': '更正公告',
            'keyword': '检测'
        },
        {
            'name': 'G98环岛高速公路大三亚段扩容工程质量监督检测机构公开招标公告',
            'org': '海南省交通工程质量监督管理局',
            'date': '2026-08-03',
            'type': '招标公告',
            'keyword': '检测'
        },
        {
            'name': '海南大洲岛国家级自然保护区保护管理设施建设项目(项目前期工作经费)履约验收公告',
            'org': '海南万宁大洲岛国家级海洋生态自然保护区管理处',
            'date': '2026-07-29',
            'type': '履约验收公告',
            'keyword': '勘察'
        },
        {
            'name': '海南省公安厅反走私和海岸管理总队2026年07月至2026年08月政府采购意向',
            'org': '海南省公安厅反走私和海岸管理总队',
            'date': '2026-07-24',
            'type': '采购意向',
            'keyword': '勘察'
        },
        {
            'name': '东方市自然资源和规划局2026年07月至2026年08月政府采购意向',
            'org': '东方市自然资源和规划局',
            'date': '2026-07-14',
            'type': '采购意向',
            'keyword': '地质勘查'
        },
        {
            'name': '海口市琼山区旧州镇矿泉水地质勘查报告编制工作履约验收公告',
            'org': '海口市自然资源和规划局',
            'date': '2026-06-29',
            'type': '履约验收公告',
            'keyword': '地质勘查'
        },
    ]

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title='海南勘察招标日报 2026-08-11',
        author='招标情报分析中心',
        subject='勘察检测行业招标公告日报',
    )

    elems = []
    elems += build_cover(s)
    elems += build_toc(s)
    elems += build_summary(s)

    # Section 3 & 4 combined
    elems.append(Paragraph('三、海南省勘察类公告统计', s['h1']))
    elems.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#2c5aa0'),
                              spaceAfter=0.2*cm))
    elems.append(Paragraph('海南省政府采购网（统计周期：2026-08-10 03:00 ~ 2026-08-11 03:00）', s['body']))
    elems.append(Spacer(1, 0.3*cm))

    stat_table_data = [
        ['关键词', '搜索命中数（全部时间）', '近24小时新增', '最近发布时间', '备注'],
        ['勘察', '149条', '0条', '2026-08-08', '地质勘查、水文勘察、工程勘察'],
        ['检测', '若干条', '0条', '2026-08-03', '含工程质量监督检测'],
        ['测绘', '0条', '0条', '—', '无相关公告'],
        ['岩土', '0条', '0条', '—', '无相关公告'],
        ['地质灾害', '0条', '0条', '—', '无相关公告'],
    ]
    st3 = Table(stat_table_data, colWidths=[2.5*cm, 4*cm, 2.5*cm, 3*cm, 4*cm])
    st3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3a6c')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Hei-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('FONTNAME', (0,1), (-1,-1), 'Song'),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f0f4fb')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#c0cfe0')),
    ]))
    elems.append(st3)
    elems.append(Spacer(1, 0.5*cm))

    elems += build_notice_table(s, notices_24h,
        '四、公告清单（按关键词分类）', '统计周期内（2026-08-10 ~ 2026-08-11）无新增勘察类公告。')

    elems.append(Paragraph('4.2 检测类公告', s['h2']))
    elems.append(Paragraph('统计周期内无新增检测类公告。最近一条检测类公告（G98高速质量监督检测）发布于2026-08-03。', s['body']))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph('4.3 其他相关公告', s['h2']))
    elems.append(Paragraph('测绘、岩土、地质灾害类关键词在海南省政府采购网上无相关公告记录。', s['body']))
    elems.append(Spacer(1, 0.3*cm))

    elems += build_risk_section(s)
    elems += build_appendix(s, history_notices)

    doc.build(elems, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f'PDF generated: {output_path}')

if __name__ == '__main__':
    out = '/Users/fasimac/.qclaw/workspace/hainan_survey_daily_20260811.pdf'
    generate_pdf(out)
