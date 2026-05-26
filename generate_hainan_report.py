# -*- coding: utf-8 -*-
"""
海南勘察招标日报 - PDF生成脚本
生成日期: 2026-04-11
"""

import sys
import os
from datetime import datetime

# 导入PDF生成库
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 设置中文字体
def setup_chinese_font():
    """注册系统中文字体"""
    system = os.uname().sysname if hasattr(os, 'uname') else 'Darwin'
    
    if system == 'Darwin':  # macOS
        candidates = [
            ('/System/Library/Fonts/STHeiti Light.ttc', 'STHeiti', 0),
            ('/System/Library/Fonts/STHeiti Medium.ttc', 'STHeitiMedium', 0),
            ('/System/Library/Fonts/Supplemental/Songti.ttc', 'Songti', 0),
            ('/Library/Fonts/Arial Unicode MS.ttf', 'ArialUnicode', 0),
        ]
    else:
        candidates = [
            ('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 'NotoSansCJK', 0),
            ('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 'WQYZenHei', 0),
        ]
    
    cn_font = None
    for font_path, font_name, idx in candidates:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont(font_name, font_path, subfontIndex=idx))
                cn_font = font_name
                print(f"成功加载字体: {font_name}")
                break
            except Exception as e:
                print(f"字体加载失败 {font_name}: {e}")
                continue
    
    if cn_font is None:
        raise RuntimeError("未找到可用的中文字体")
    
    return cn_font

# 创建PDF
def create_report():
    # 注册中文字体
    cn_font = setup_chinese_font()
    
    # 设置样式
    styles = getSampleStyleSheet()
    
    # 修改所有样式使用中文字体
    for style in styles.byName.values():
        if hasattr(style, 'fontName'):
            style.fontName = cn_font
    
    # 自定义样式
    title_style = ParagraphStyle(
        'CnTitle',
        parent=styles['Title'],
        fontName=cn_font,
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=30,
        textColor=colors.HexColor('#1a365d')
    )
    
    subtitle_style = ParagraphStyle(
        'CnSubtitle',
        parent=styles['Normal'],
        fontName=cn_font,
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.HexColor('#4a5568')
    )
    
    heading1_style = ParagraphStyle(
        'CnHeading1',
        parent=styles['Heading1'],
        fontName=cn_font,
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.HexColor('#2d3748'),
        borderPadding=5
    )
    
    heading2_style = ParagraphStyle(
        'CnHeading2',
        parent=styles['Heading2'],
        fontName=cn_font,
        fontSize=14,
        spaceBefore=15,
        spaceAfter=8,
        textColor=colors.HexColor('#4a5568')
    )
    
    body_style = ParagraphStyle(
        'CnBody',
        parent=styles['Normal'],
        fontName=cn_font,
        fontSize=11,
        leading=18,
        alignment=TA_JUSTIFY
    )
    
    note_style = ParagraphStyle(
        'CnNote',
        parent=styles['Normal'],
        fontName=cn_font,
        fontSize=10,
        leading=16,
        textColor=colors.HexColor('#718096'),
        alignment=TA_LEFT
    )
    
    # 创建文档
    output_path = "/Users/fasimac/.qclaw/workspace/海南勘察招标日报_2026-04-11.pdf"
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    story = []
    
    # ===== 封面 =====
    story.append(Spacer(1, 100))
    story.append(Paragraph("海南勘察招标日报", title_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("勘察·检测·测绘·岩土·地质灾害", subtitle_style))
    story.append(Spacer(1, 40))
    story.append(Paragraph("2026年4月11日", subtitle_style))
    story.append(Spacer(1, 60))
    
    # 封面说明
    cover_note = """
    <b>报告说明</b><br/>
    本报告汇总海南省及周边地区勘察检测类招标信息，<br/>
    涵盖工程勘察、质量检测、测绘地理信息、岩土工程、<br/>
    地质灾害防治等专业领域。<br/><br/>
    数据来源：中国招标投标公共服务平台、海南省政府采购网、<br/>
    海口市公共资源交易中心等官方渠道
    """
    story.append(Paragraph(cover_note, body_style))
    story.append(PageBreak())
    
    # ===== 目录 =====
    story.append(Paragraph("目 录", heading1_style))
    story.append(Spacer(1, 20))
    
    toc_items = [
        ("一、今日招标概览", "3"),
        ("二、重点招标项目", "4"),
        ("三、市场分析", "5"),
        ("四、风险提示", "6"),
        ("五、数据说明", "7"),
    ]
    
    for item, page in toc_items:
        toc_line = f"{item}{'.' * (50 - len(item) * 2)}{page}"
        story.append(Paragraph(toc_line, body_style))
        story.append(Spacer(1, 8))
    
    story.append(PageBreak())
    
    # ===== 一、今日招标概览 =====
    story.append(Paragraph("一、今日招标概览", heading1_style))
    story.append(Spacer(1, 15))
    
    summary_text = """
    根据对中国招标投标公共服务平台（www.cebpubservice.com）、海南省政府采购网<br/>
    （www.ccgp-hainan.gov.cn）等官方渠道的监测，截至2026年4月11日03:00，<br/>
    <b>最近24小时内未发现新的勘察检测类招标公告发布</b>。
    """
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 20))
    
    # 统计表格
    story.append(Paragraph("📊 招标数据统计", heading2_style))
    story.append(Spacer(1, 10))
    
    stats_data = [
        [Paragraph('数据来源', body_style), Paragraph('监测数量', body_style), Paragraph('有效公告', body_style), Paragraph('备注', body_style)],
        [Paragraph('中国招标投标公共服务平台', body_style), Paragraph('0', body_style), Paragraph('0', body_style), Paragraph('网站访问受限', body_style)],
        [Paragraph('海南省政府采购网', body_style), Paragraph('0', body_style), Paragraph('0', body_style), Paragraph('需浏览器访问', body_style)],
        [Paragraph('海口市公共资源交易中心', body_style), Paragraph('0', body_style), Paragraph('0', body_style), Paragraph('无新公告', body_style)],
        [Paragraph('第三方招标平台', body_style), Paragraph('历史数据若干', body_style), Paragraph('参考用', body_style), Paragraph('非24小时内', body_style)],
    ]
    
    stats_table = Table(stats_data, colWidths=[140, 80, 80, 140])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E4057')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), cn_font),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f7fafc'), colors.white]),
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 20))
    
    # 重要提示
    alert_box = """
    <b>⚠️ 重要提示</b><br/>
    由于官方招标平台存在访问限制（需要浏览器渲染或登录验证），<br/>
    本次监测未能获取到最近24小时内发布的具体招标公告。<br/>
    建议用户直接访问以下官方网站获取最新信息：
    """
    story.append(Paragraph(alert_box, body_style))
    story.append(Spacer(1, 10))
    
    official_sites = [
        "• 中国招标投标公共服务平台：https://www.cebpubservice.com",
        "• 海南省政府采购网：http://www.ccgp-hainan.gov.cn",
        "• 海口市公共资源交易中心：https://ggzy.haikou.gov.cn",
        "• 全国公共资源交易平台（海南省）：https://ggzy.hainan.gov.cn",
    ]
    for site in official_sites:
        story.append(Paragraph(site, note_style))
        story.append(Spacer(1, 5))
    
    story.append(PageBreak())
    
    # ===== 二、重点招标项目 =====
    story.append(Paragraph("二、重点招标项目", heading1_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("📋 近期历史招标项目参考（非24小时内）", heading2_style))
    story.append(Spacer(1, 10))
    
    # 历史项目表格
    projects_data = [
        [Paragraph('项目名称', body_style), Paragraph('发布时间', body_style), Paragraph('项目类型', body_style)],
        [Paragraph('2026年度海南省矿山地质环境动态监测项目测量和数据化处理', body_style), Paragraph('2026-02-14', body_style), Paragraph('测绘/监测', body_style)],
        [Paragraph('2026年地质灾害设备和配套服务采购项目', body_style), Paragraph('2026-02-14', body_style), Paragraph('设备采购', body_style)],
        [Paragraph('2026年海南省林业工作站标准化建设项目工程勘察测量', body_style), Paragraph('2025-12-01', body_style), Paragraph('工程勘察', body_style)],
        [Paragraph('儋州市民族中学校园西南边沿地质灾害综合治理项目勘察测绘', body_style), Paragraph('2025-09-02', body_style), Paragraph('地灾勘察', body_style)],
        [Paragraph('海南省地质灾害监测预警与风险防控能力提升项目', body_style), Paragraph('2024-05-22', body_style), Paragraph('监测预警', body_style)],
    ]
    
    projects_table = Table(projects_data, colWidths=[220, 90, 110])
    projects_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E4057')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), cn_font),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f7fafc'), colors.white]),
    ]))
    story.append(projects_table)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<i>注：以上项目为近期历史招标信息，供参考了解市场动态，非24小时内新发布公告。</i>", note_style))
    story.append(PageBreak())
    
    # ===== 三、市场分析 =====
    story.append(Paragraph("三、市场分析", heading1_style))
    story.append(Spacer(1, 15))
    
    analysis_text = """
    <b>1. 行业概况</b><br/>
    海南省勘察检测行业主要服务于自贸港建设、城市更新、基础设施等领域。<br/>
    近期重点方向包括：<br/>
    • 地质灾害监测预警与风险防控<br/>
    • 矿山地质环境动态监测<br/>
    • 林业工作站标准化建设勘察<br/>
    • 教育设施地质灾害治理<br/><br/>
    
    <b>2. 资质要求趋势</b><br/>
    根据历史招标数据分析，常见资质要求包括：<br/>
    • 工程勘察综合甲级或专业类岩土工程资质<br/>
    • CMA计量认证（检测类项目）<br/>
    • 测绘资质（乙级及以上）<br/>
    • 地质灾害防治资质（勘查/设计/施工）<br/><br/>
    
    <b>3. 市场机会</b><br/>
    • 海南自贸港建设持续推进，基础设施项目需求稳定<br/>
    • 地质灾害防治领域投入加大，监测预警类项目增多<br/>
    • 生态环境监测领域存在长期服务需求
    """
    story.append(Paragraph(analysis_text, body_style))
    story.append(PageBreak())
    
    # ===== 四、风险提示 =====
    story.append(Paragraph("四、风险提示", heading1_style))
    story.append(Spacer(1, 15))
    
    risk_text = """
    <b>⚠️ 数据获取限制说明</b><br/><br/>
    
    本次报告因以下技术限制，未能获取到最近24小时内的新发布招标公告：<br/><br/>
    
    1. <b>官方平台访问限制</b><br/>
       - 中国招标投标公共服务平台：存在反爬机制，需要浏览器访问<br/>
       - 海南省政府采购网：页面需要JavaScript渲染<br/>
       - 海口市公共资源交易中心：动态加载内容<br/><br/>
    
    2. <b>建议解决方案</b><br/>
       - 直接访问官方网站获取最新信息<br/>
       - 订阅官方平台的邮件/短信提醒服务<br/>
       - 使用第三方招标信息服务平台（如千里马、必联网等）<br/><br/>
    
    3. <b>数据时效性说明</b><br/>
       本报告中的历史项目信息仅供参考，具体招标信息请以官方发布为准。
    """
    story.append(Paragraph(risk_text, body_style))
    story.append(PageBreak())
    
    # ===== 五、数据说明 =====
    story.append(Paragraph("五、数据说明", heading1_style))
    story.append(Spacer(1, 15))
    
    data_note = """
    <b>报告生成信息</b><br/><br/>
    
    • 报告标题：海南勘察招标日报<br/>
    • 报告日期：2026年4月11日<br/>
    • 监测时段：最近24小时（2026-04-10 03:00 至 2026-04-11 03:00）<br/>
    • 数据来源：中国招标投标公共服务平台、海南省政府采购网、<br/>
      海口市公共资源交易中心、第三方招标信息平台<br/><br/>
    
    <b>免责声明</b><br/>
    本报告仅供参考，不构成任何投资建议。具体招标信息请以官方发布为准。<br/>
    报告中的历史数据来源于公开渠道，如有出入请以官方公告为准。<br/><br/>
    
    <b>联系方式</b><br/>
    如需获取更详细的招标信息，请访问相关官方网站或联系招标代理机构。
    """
    story.append(Paragraph(data_note, body_style))
    story.append(Spacer(1, 40))
    
    # 页脚信息
    footer_text = "— 本报告由AI自动生成，生成时间：2026-04-11 03:00 —"
    story.append(Paragraph(footer_text, note_style))
    
    # 生成PDF
    doc.build(story)
    print(f"\n✅ PDF报告已生成: {output_path}")
    return output_path

if __name__ == "__main__":
    try:
        pdf_path = create_report()
        print(f"\n文件大小: {os.path.getsize(pdf_path) / 1024:.1f} KB")
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        import traceback
        traceback.print_exc()
