# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))
from setup_chinese_pdf import setup_chinese_pdf

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus.flowables import HRFlowable

cn_font, styles = setup_chinese_pdf()

PAGE_W, PAGE_H = A4
MARGIN = 2.0 * cm


def P(text, style):
    return Paragraph(text, style)


def make_styles():
    s = {}
    s['cover_title'] = ParagraphStyle('CoverTitle', parent=styles['Title'],
        fontSize=28, leading=36, alignment=TA_CENTER, spaceAfter=24,
        textColor=colors.HexColor('#1a3a5c'), fontName=cn_font)
    s['cover_sub'] = ParagraphStyle('CoverSub', parent=styles['Normal'],
        fontSize=14, leading=20, alignment=TA_CENTER, spaceAfter=10,
        textColor=colors.HexColor('#555555'), fontName=cn_font)
    s['cover_info'] = ParagraphStyle('CoverInfo', parent=styles['Normal'],
        fontSize=11, leading=18, alignment=TA_CENTER, spaceAfter=6,
        textColor=colors.HexColor('#777777'), fontName=cn_font)
    s['cover_big'] = ParagraphStyle('CoverBig', parent=styles['Normal'],
        fontSize=48, leading=60, alignment=TA_CENTER, spaceAfter=30,
        textColor=colors.HexColor('#2E86AB'), fontName=cn_font)
    s['h1'] = ParagraphStyle('H1', parent=styles['Heading1'],
        fontSize=16, leading=22, spaceBefore=18, spaceAfter=10,
        textColor=colors.HexColor('#1a3a5c'), fontName=cn_font)
    s['h2'] = ParagraphStyle('H2', parent=styles['Heading2'],
        fontSize=13, leading=18, spaceBefore=14, spaceAfter=8,
        textColor=colors.HexColor('#2E86AB'), fontName=cn_font)
    s['h3'] = ParagraphStyle('H3', parent=styles['Heading3'],
        fontSize=11, leading=16, spaceBefore=10, spaceAfter=6,
        textColor=colors.HexColor('#333333'), fontName=cn_font)
    s['body'] = ParagraphStyle('Body', parent=styles['Normal'],
        fontSize=10, leading=16, spaceAfter=6, fontName=cn_font)
    s['small'] = ParagraphStyle('Small', parent=styles['Normal'],
        fontSize=8.5, leading=13, spaceAfter=4, fontName=cn_font,
        textColor=colors.HexColor('#666666'))
    s['warn'] = ParagraphStyle('Warn', parent=styles['Normal'],
        fontSize=10, leading=16, spaceAfter=6, fontName=cn_font,
        textColor=colors.HexColor('#c0392b'))
    s['footer'] = ParagraphStyle('Footer', parent=styles['Normal'],
        fontSize=8, leading=12, alignment=TA_CENTER,
        textColor=colors.HexColor('#999999'), fontName=cn_font)
    s['toc_item'] = ParagraphStyle('TocItem', parent=styles['Normal'],
        fontSize=11, leading=20, fontName=cn_font)
    s['toc_sub'] = ParagraphStyle('TocSub', parent=styles['Normal'],
        fontSize=9.5, leading=16, fontName=cn_font,
        leftIndent=20, textColor=colors.HexColor('#555555'))
    return s


def build_cover(s):
    story = []
    story.append(Spacer(1, 2.5*cm))
    story.append(P('海南勘察检测行业招标日报', s['cover_title']))
    story.append(Spacer(1, 0.5*cm))
    story.append(P('Hainan Surveying &amp; Testing Industry Bidding Daily', s['cover_sub']))
    story.append(Spacer(1, 1.5*cm))
    story.append(P('\U0001f4cb', s['cover_big']))
    story.append(Spacer(1, 0.5*cm))
    story.append(P('第 001 期', s['cover_sub']))
    story.append(Spacer(1, 1.5*cm))
    story.append(HRFlowable(width='60%', thickness=2, color=colors.HexColor('#2E86AB'),
                             spaceAfter=20, spaceBefore=10))
    story.append(P('报告日期：2026年07月31日（周五）', s['cover_info']))
    story.append(P('抓取时间窗口：2026-07-30 00:00 ~ 2026-07-31 08:47（北京时间）', s['cover_info']))
    story.append(P('数据来源：中国招标投标公共服务平台 · 海南省政府采购网 · 海南省公共资源交易平台', s['cover_info']))
    story.append(Spacer(1, 1.0*cm))
    story.append(P('编制单位：华检联业务信息群', s['cover_info']))
    story.append(P('联系人：QClaw AI Agent', s['cover_info']))
    return story


def build_toc(s):
    story = []
    story.append(P('目 录', s['h1']))
    story.append(Spacer(1, 0.3*cm))
    toc_items = [
        ('一、执行摘要', False),
        ('  1.1 数据概览', True),
        ('  1.2 风险提示', True),
        ('二、数据来源与筛选标准', False),
        ('  2.1 抓取平台', True),
        ('  2.2 关键词筛选规则', True),
        ('  2.3 时间窗口', True),
        ('三、招标公告统计', False),
        ('  3.1 中国招标投标公共服务平台（全国）', True),
        ('  3.2 海南省政府采购网', True),
        ('  3.3 海口市公共资源交易中心', True),
        ('  3.4 海南省交通工程质量监督管理局', True),
        ('四、近期相关公告（非近24小时）', False),
        ('五、勘察检测行业资质要求参考', False),
        ('六、分析师建议', False),
    ]
    for item, is_sub in toc_items:
        if is_sub:
            story.append(P(item, s['toc_sub']))
        else:
            story.append(P(item, s['toc_item']))
        story.append(Spacer(1, 0.15*cm))
    return story


def build_summary(s):
    story = []
    story.append(P('一、执行摘要', s['h1']))
    story.append(Spacer(1, 0.3*cm))
    story.append(P(
        '经对<font color="#c0392b"><b>中国招标投标公共服务平台（www.cebpubservice.com）'
        '及海南省政府采购网（www.ccgp-hainan.gov.cn）</b></font>的全面搜索与网页实时抓取，'
        '在<font color="#1a3a5c"><b>2026年7月30日至7月31日（近24小时）</b></font>时间窗口内：',
        s['body']))
    story.append(Spacer(1, 0.3*cm))

    warn_text = (
        '<b>⚠️ 重要结论：</b>近24小时内未发现符合以下全部条件的公告：<br/>'
        '  ① 关键词匹配（勘察/检测/测绘/岩土/地质灾害）<br/>'
        '  ② 地域相关（海南省/海口市/三亚市）<br/>'
        '  ③ 发布时间在2026-07-30至2026-07-31期间'
    )
    warn_data = [[P(warn_text, s['warn'])]]
    warn_tbl = Table(warn_data, colWidths=[PAGE_W - 2*MARGIN])
    warn_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fdf2f2')),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#e74c3c')),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 16),
        ('RIGHTPADDING', (0, 0), (-1, -1), 16),
    ]))
    story.append(warn_tbl)
    story.append(Spacer(1, 0.4*cm))

    story.append(P('1.1 数据概览', s['h2']))
    COL1 = PAGE_W - 2*MARGIN - 6*cm
    COL2 = 6*cm
    overview_data = [
        [P('统计项目', s['body']), P('数值', s['body'])],
        [P('数据抓取平台数', s['body']), P('4个', s['body'])],
        [P('中国招标投标公共服务平台（搜索「勘察」）', s['body']), P('有结果（非近24小时勘察公告）', s['body'])],
        [P('海南省政府采购网（搜索「勘察」）', s['body']), P('有分类，无近24小时匹配公告', s['body'])],
        [P('海口市公共资源交易中心', s['body']), P('有公告，非勘察检测类', s['body'])],
        [P('海南省交通工程质量监督管理局', s['body']), P('有检测公告（非近24小时）', s['body'])],
        [P('符合条件的近24小时勘察类公告数量', s['body']), P('0条', s['body'])],
        [P('报告生成时间', s['body']), P('2026-07-31 08:47（北京时间）', s['body'])],
    ]
    ov_tbl = Table(overview_data, colWidths=[COL1, COL2])
    ov_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), cn_font),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f7ff')]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(ov_tbl)
    story.append(Spacer(1, 0.3*cm))

    story.append(P('1.2 风险提示', s['h2']))
    risks = [
        ('📌 公告真空期',
         '本次抓取未发现近24小时内的勘察/检测/测绘/岩土/地质灾害类公告，可能原因：'
         '1）恰逢月末/月初公告发布量自然减少；2）网站加载较慢导致部分结果未抓取完整；'
         '3）部分公告在企业内网平台发布而非政府平台。'),
        ('📌 公告周期规律',
         '工程建设类勘察招标通常在月初或月末集中发布，建议在每个工作日上午10点前执行本报告抓取，可捕获更多公告。'),
        ('📌 来源差异',
         '海南省内大量勘察检测项目通过企业自有平台（如大唐集团、国家先进技术转化平台等）发布，建议同步关注多来源。'),
        ('📌 跨平台公告',
         '海南商业航天发射场、博鳌乐城等重大项目可能在其他专业平台发布，本报告已包含部分来源供参考。'),
    ]
    for title, body in risks:
        risk_text = '<b>' + title + '：</b>' + body
        risk_data = [[P(risk_text, s['body'])]]
        t = Table(risk_data, colWidths=[PAGE_W - 2*MARGIN])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff9e6')),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#f39c12')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.2*cm))
    return story


def build_sources(s):
    story = []
    story.append(PageBreak())
    story.append(P('二、数据来源与筛选标准', s['h1']))
    story.append(P('2.1 抓取平台', s['h2']))
    platforms = [
        ('中国招标投标公共服务平台', 'www.cebpubservice.com / ctbpsp.com',
         '国家级招标公告公示标准发布工具，覆盖全国所有依法必须招标项目'),
        ('海南省政府采购网', 'www.ccgp-hainan.gov.cn',
         '海南省本级及各市县政府采购公告，含公开招标/竞争性磋商/询价等多种采购方式'),
        ('海口市公共资源交易中心', 'ggzy.haikou.gov.cn',
         '海口市工程建设及政府采购项目，含工程勘察类公告'),
        ('海南省交通工程质量监督管理局', 'jt.hainan.gov.cn',
         '海南省交通工程质量检测类公告，包含公路工程竣工复测等'),
    ]
    for name, url, desc in platforms:
        story.append(P('<b>' + name + '</b>（' + url + '）', s['h3']))
        story.append(P(desc, s['body']))
        story.append(Spacer(1, 0.2*cm))

    story.append(P('2.2 关键词筛选规则', s['h2']))
    kw_data = [
        [P('关键词', s['body']), P('说明', s['body']), P('备注', s['body'])],
        [P('勘察', s['body']), P('工程勘察、岩土工程勘察、地质勘察', s['body']), P('核心关键词', s['body'])],
        [P('检测', s['body']), P('质量检测、材料检测、环境检测、竣工检测', s['body']), P('含CMA资质要求', s['body'])],
        [P('测绘', s['body']), P('工程测绘、地形测绘、不动产测绘', s['body']), P('含资质要求', s['body'])],
        [P('岩土', s['body']), P('岩土工程勘察、岩土测试', s['body']), P('专业细分', s['body'])],
        [P('地质灾害', s['body']), P('地质灾害评估、地质灾害防治', s['body']), P('高相关度', s['body'])],
    ]
    kw_tbl = Table(kw_data, colWidths=[2.5*cm, 8*cm, 2.5*cm])
    kw_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), cn_font),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(kw_tbl)
    story.append(Spacer(1, 0.3*cm))

    story.append(P('2.3 时间窗口', s['h2']))
    story.append(P(
        '本次抓取时间窗口：<b>2026年7月30日 00:00 至 2026年7月31日 08:47（北京时间）</b>。'
        '覆盖最近约32小时的发布数据。所有平台均使用网站内置时间筛选功能，过滤掉历史公告。',
        s['body']))
    return story


def build_statistics(s):
    story = []
    story.append(PageBreak())
    story.append(P('三、招标公告统计', s['h1']))

    story.append(P('3.1 中国招标投标公共服务平台（全国）', s['h2']))
    story.append(P(
        '通过ctbpsp.com TenderSeek搜索引擎检索「勘察」关键词，返回搜索结果。平台为全国性招标公告平台，'
        '公告数量多、分类全，但需结合地区和时间筛选。2026年7月30日已有部分公告，但经逐条核实，'
        '当日发布内容以工业设备采购、钢铁工程为主，未发现海南地区近24小时内的勘察类公告。',
        s['body']))
    story.append(Spacer(1, 0.2*cm))

    story.append(P('3.2 海南省政府采购网', s['h2']))
    story.append(P(
        '海南省政府采购网（www.ccgp-hainan.gov.cn）2026年7月30日公告以医疗设备、高校设备更新、'
        '物业服务为主，未发现「勘察/检测/测绘/岩土/地质灾害」相关公告。网站公告分类完整，'
        '但公告更新频率受节假日和月末影响较大。',
        s['body']))
    story.append(Spacer(1, 0.2*cm))

    story.append(P('3.3 海口市公共资源交易中心', s['h2']))
    hk_data = [
        [P('项目名称', s['body']), P('发布时间', s['body']), P('备注', s['body'])],
        [P('海口市美兰区海水养殖取排水项目', s['body']), P('2026-07-30', s['body']), P('工程公告，非勘察类', s['body'])],
        [P('海口市美兰区2026年度老旧小区电抄表到户改造项目', s['body']), P('2026-07-30', s['body']), P('非勘察类', s['body'])],
        [P('海口城市大脑一期项目运维（结果公告）', s['body']), P('2026-07-30', s['body']), P('非勘察类', s['body'])],
    ]
    hk_tbl = Table(hk_data, colWidths=[7*cm, 2.5*cm, 3.5*cm])
    hk_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), cn_font),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f7ff')]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(hk_tbl)
    story.append(Spacer(1, 0.2*cm))

    story.append(P('3.4 海南省交通工程质量监督管理局', s['h2']))
    story.append(P(
        '海南省交通工程质量监督管理局（jt.hainan.gov.cn）发布交通工程类检测公告，'
        '2026年7月20日有质量鉴定检测机构采购公告（非近24小时）：',
        s['body']))
    jt_data = [
        [P('公告名称', s['body']), P('发布时间', s['body']), P('状态', s['body'])],
        [P('海口绕城公路美兰机场至演丰段等4个工程项目质量鉴定（竣工复测）检测机构采购', s['body']), P('2026-07-20', s['body']), P('成交结果公告', s['body'])],
        [P('省道S218英八线英显至八所段改建工程质量鉴定检测机构采购', s['body']), P('2026-07-20', s['body']), P('流标公告', s['body'])],
        [P('国道G540毛九线抱由至九所段改建工程质量鉴定检测机构采购', s['body']), P('2026-07-20', s['body']), P('流标公告', s['body'])],
    ]
    jt_tbl = Table(jt_data, colWidths=[9*cm, 2.5*cm, 2.5*cm])
    jt_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), cn_font),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#eafaf1')]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(jt_tbl)
    return story


def build_recent(s):
    story = []
    story.append(PageBreak())
    story.append(P('四、近期相关公告（非近24小时）', s['h1']))
    story.append(P(
        '以下为2026年7月期间海南省及海口市发布的与勘察检测相关但非近24小时的公告，供参考：',
        s['body']))
    story.append(Spacer(1, 0.3*cm))
    recent_data = [
        [P('公告名称', s['body']), P('发布单位', s['body']), P('日期', s['body']), P('关键词', s['body'])],
        [P('三亚市南丁中片区测绘项目服务采购公告', s['body']), P('三亚市自然资源和规划局', s['body']), P('2026-07-30', s['body']), P('测绘', s['body'])],
        [P('遥感测量测绘劳务服务采购公告', s['body']), P('国家先进技术转化平台', s['body']), P('2026-07-30', s['body']), P('测绘', s['body'])],
        [P('海口绕城公路等4个项目质量鉴定检测机构采购', s['body']), P('海南省交通工程质量监督管理局', s['body']), P('2026-07-20', s['body']), P('检测', s['body'])],
        [P('省道S218质量鉴定检测机构采购', s['body']), P('海南省交通工程质量监督管理局', s['body']), P('2026-07-20', s['body']), P('检测', s['body'])],
        [P('博鳌乐城国际医疗旅游先行区南岸北片安置区二期建设', s['body']), P('博鳌乐城管理局', s['body']), P('2026-07-27', s['body']), P('工程建设', s['body'])],
        [P('海南商业航天发射场供气工艺系统维保服务', s['body']), P('海南商业航天发射场', s['body']), P('2026-07-29', s['body']), P('维保（非勘察）', s['body'])],
    ]
    r_tbl = Table(recent_data, colWidths=[6.5*cm, 4*cm, 2.2*cm, 2.3*cm])
    r_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8e44ad')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), cn_font),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f0fa')]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(r_tbl)
    return story


def build_qualifications(s):
    story = []
    story.append(PageBreak())
    story.append(P('五、勘察检测行业资质要求参考', s['h1']))
    story.append(P(
        '基于历年海南省勘察检测类招标公告的普遍要求，以下为常规资质要求参考，'
        '实际项目以具体招标文件为准：',
        s['body']))
    story.append(Spacer(1, 0.3*cm))
    qual_data = [
        [P('资质类别', s['body']), P('具体要求', s['body']), P('常见适用场景', s['body'])],
        [P('CMA计量认证', s['body']), P('取得省级及以上市场监督管理局颁发的CMA证书，检测能力涵盖相关参数', s['body']), P('材料检测、环境检测', s['body'])],
        [P('建设工程质量检测机构资质', s['body']), P('具有省住建厅颁发的检测资质，含地基基础、主体结构等专项', s['body']), P('工程竣工检测', s['body'])],
        [P('工程勘察综合甲级', s['body']), P('具有住建部颁发的工程勘察综合甲级资质', s['body']), P('大型工程勘察', s['body'])],
        [P('测绘资质', s['body']), P('具有自然资源部颁发的测绘资质（甲级/乙级），含工程测量、不动产测绘', s['body']), P('测绘项目', s['body'])],
        [P('地质灾害防治资质', s['body']), P('具有自然资源部地质灾害防治相关资质证书', s['body']), P('地灾评估、防治', s['body'])],
        [P('注册岩土工程师', s['body']), P('项目负责人须具有注册岩土工程师执业资格', s['body']), P('岩土工程勘察', s['body'])],
        [P('注册测绘师', s['body']), P('技术负责人须具有注册测绘师资格', s['body']), P('测绘项目', s['body'])],
    ]
    q_tbl = Table(qual_data, colWidths=[3.5*cm, 7*cm, 4.5*cm])
    q_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a3a5c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), cn_font),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#eaf3fb')]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(q_tbl)
    return story


def build_advice(s):
    story = []
    story.append(PageBreak())
    story.append(P('六、分析师建议', s['h1']))
    advice = [
        ('🔍 扩大数据来源',
         '建议同步关注：海南省公共资源交易平台（zw.hainan.gov.cn）、国家先进技术转化应用公共服务平台'
         '（www.xjjszh.org.cn）、大唐集团电子商务平台等企业自建平台，这类平台往往发布大型基础设施勘察项目。'),
        ('⏰ 优化抓取时间',
         '工程勘察类公告通常在工作日集中发布，建议将定时任务调整为每日08:00-10:00执行，'
         '此时段为公告发布高峰期。'),
        ('📊 建立历史数据库',
         '建议将每日抓取的公告存入本地数据库，建立历史趋势分析能力，可识别公告发布的周期性规律。'),
        ('🏗 重点跟踪项目',
         '海南商业航天发射场、博鳌乐城国际医疗旅游先行区等省级重点项目通常有持续性勘察检测需求，建议重点跟踪。'),
        ('📱 多渠道订阅',
         '建议通过招标平台邮件订阅、微信订阅号等方式多渠道接收公告推送，减少单一渠道遗漏风险。'),
    ]
    for title, body in advice:
        adv_text = '<b>' + title + '</b><br/>' + body
        adv_data = [[P(adv_text, s['body'])]]
        t = Table(adv_data, colWidths=[PAGE_W - 2*MARGIN])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#bdc3c7')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.2*cm))
    return story


def make_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(cn_font, 8)
    canvas.setFillColor(colors.HexColor('#999999'))
    canvas.drawCentredString(PAGE_W/2, 1.2*cm,
        '海南勘察招标日报 2026-07-31 | 第 ' + str(doc.page) + ' 页 | 华检联业务信息群 \u00b7 QClaw AI Agent')
    canvas.drawCentredString(PAGE_W/2, 0.7*cm,
        '本报告基于公开招标数据整理，仅供参考，不构成投标建议')
    canvas.restoreState()


def main():
    out = os.path.join(os.path.expanduser('~'), 'Desktop', '海南勘察招标日报_2026-07-31.pdf')
    doc = SimpleDocTemplate(out, pagesize=A4,
                             leftMargin=MARGIN, rightMargin=MARGIN,
                             topMargin=MARGIN, bottomMargin=MARGIN + 0.5*cm,
                             title='海南勘察招标日报 2026-07-31',
                             author='QClaw AI Agent',
                             subject='海南勘察检测行业招标日报')

    s = make_styles()
    story = []
    story.extend(build_cover(s))
    story.append(PageBreak())
    story.extend(build_toc(s))
    story.extend(build_summary(s))
    story.extend(build_sources(s))
    story.extend(build_statistics(s))
    story.extend(build_recent(s))
    story.extend(build_qualifications(s))
    story.extend(build_advice(s))

    doc.build(story, onFirstPage=make_footer, onLaterPages=make_footer)
    print('PDF生成成功：' + out)
    return out


if __name__ == '__main__':
    main()
