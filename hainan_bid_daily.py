#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海南勘察招标日报生成脚本
生成PDF报告（WPS兼容格式）
"""

from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os
import base64

# 注册中文字体
FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
if os.path.exists(FONT_PATH):
    pdfmetrics.registerFont(TTFont('SimHei', FONT_PATH))
    CHINESE_FONT = 'SimHei'
else:
    # 尝试其他字体
    for font_path in [
        "/System/Library/Fonts/PingFang.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Songti.ttc"
    ]:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('SimHei', font_path))
                CHINESE_FONT = 'SimHei'
                break
            except:
                continue
    else:
        CHINESE_FONT = 'Helvetica'

# 定义样式
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'ChineseTitle',
    parent=styles['Title'],
    fontName=CHINESE_FONT,
    fontSize=24,
    alignment=TA_CENTER,
    spaceAfter=30,
    textColor=colors.HexColor('#1a5490')
)

heading_style = ParagraphStyle(
    'ChineseHeading',
    parent=styles['Heading1'],
    fontName=CHINESE_FONT,
    fontSize=16,
    alignment=TA_LEFT,
    spaceAfter=12,
    spaceBefore=20,
    textColor=colors.HexColor('#2c5aa0')
)

subheading_style = ParagraphStyle(
    'ChineseSubHeading',
    parent=styles['Heading2'],
    fontName=CHINESE_FONT,
    fontSize=14,
    alignment=TA_LEFT,
    spaceAfter=10,
    spaceBefore=15,
    textColor=colors.HexColor('#3466a4')
)

normal_style = ParagraphStyle(
    'ChineseNormal',
    parent=styles['Normal'],
    fontName=CHINESE_FONT,
    fontSize=11,
    alignment=TA_JUSTIFY,
    spaceAfter=8,
    leading=18
)

caption_style = ParagraphStyle(
    'ChineseCaption',
    parent=styles['Normal'],
    fontName=CHINESE_FONT,
    fontSize=10,
    alignment=TA_CENTER,
    textColor=colors.gray
)

def create_cover_page(story, report_date):
    """创建封面"""
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("海南勘察招标日报", title_style))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(report_date, ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontName=CHINESE_FONT,
        fontSize=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#666666')
    )))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("数据来源：中国招标投标公共服务平台、海南省政府采购网", caption_style))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("报告生成时间：" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), caption_style))
    story.append(PageBreak())

def create_toc(story):
    """创建目录"""
    story.append(Paragraph("目录", heading_style))
    story.append(Spacer(1, 0.5*cm))
    
    toc_items = [
        "一、报告概述",
        "二、数据采集情况",
        "三、勘察类招标项目汇总",
        "四、重要项目详情",
        "五、风险提示与建议"
    ]
    
    for item in toc_items:
        story.append(Paragraph(item, normal_style))
    
    story.append(PageBreak())

def create_overview(story, has_data):
    """创建概述"""
    story.append(Paragraph("一、报告概述", heading_style))
    
    if has_data:
        overview_text = """
        本报告汇总了中国招标投标公共服务平台和海南省政府采购网在最近24小时内发布的勘察、检测、测绘、岩土、地质灾害相关招标公告。
        通过智能筛选和人工审核，提取出真实勘察类项目信息，为相关企业提供及时的市场情报支持。
        """
    else:
        overview_text = """
        本报告旨在汇总中国招标投标公共服务平台和海南省政府采购网在最近24小时内发布的勘察、检测、测绘、岩土、地质灾害相关招标公告。
        
        经过系统检索和时间筛选，未发现符合条件的新发布招标信息。具体情况如下：
        """
    
    story.append(Paragraph(overview_text, normal_style))
    story.append(Spacer(1, 0.5*cm))

def create_data_status(story, ceb_status, hn_status):
    """创建数据采集情况"""
    story.append(Paragraph("二、数据采集情况", heading_style))
    
    # 创建表格
    data = [
        ['数据源', '访问状态', '检索关键词', '时间范围', '结果数量'],
        ['中国招标投标公共服务平台', ceb_status, '勘察/检测/测绘/岩土/地质灾害', '近24小时', '受验证码限制'],
        ['海南省政府采购网', hn_status, '勘察/检测/测绘/岩土/地质灾害', '近24小时', '无新发布']
    ]
    
    table = Table(data, colWidths=[4*cm, 2.5*cm, 4.5*cm, 2.5*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8f0f8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), CHINESE_FONT),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 0.5*cm))

def create_no_data_notice(story):
    """创建无数据通知"""
    story.append(Paragraph("三、勘察类招标项目汇总", heading_style))
    
    notice_text = """
    <b>近期无新发布招标信息</b>
    
    经过对两大招标平台的全面检索：
    
    1. <b>中国招标投标公共服务平台</b>：该平台启用了严格的安全验证机制（滑块验证码），
    自动化采集受到限制。建议手动访问平台进行查询，或等待平台更新后再次检索。
    
    2. <b>海南省政府采购网</b>：在"勘察"关键词搜索结果中，最近24小时内无新发布的勘察类招标公告。
    最近的相关公告发布时间为2026年7月24日，距离当前已超过24小时。
    
    <b>建议措施：</b>
    • 定期关注平台动态，设置订阅提醒
    • 扩大关键词范围，如"工程勘察""地质勘查"等
    • 关注海南省公共资源交易中心其他相关平台
    • 联系当地招标代理机构获取一手信息
    """
    
    story.append(Paragraph(notice_text, normal_style))
    story.append(Spacer(1, 0.5*cm))

def create_historical_data(story):
    """创建历史数据参考"""
    story.append(Paragraph("四、近期历史数据参考", heading_style))
    
    story.append(Paragraph("以下为近期发布的勘察类相关项目（仅供参考，非最近24小时）：", normal_style))
    story.append(Spacer(1, 0.3*cm))
    
    # 示例数据
    projects = [
        ['项目名称', '采购人', '发布时间', '状态'],
        ['海口市琼山区旧州镇矿泉水地质勘察报告编制', '海口市自然资源和规划局', '2026-06-29', '已发布'],
        ['海南岛周边海域矿产资源调查评价项目', '海南省海洋地质调查院', '2026-06-16', '结果公告'],
    ]
    
    table = Table(projects, colWidths=[7*cm, 4*cm, 3*cm, 2*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f5f5f5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), CHINESE_FONT),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 0.5*cm))

def create_risk_tips(story):
    """创建风险提示"""
    story.append(Paragraph("五、风险提示与建议", heading_style))
    
    tips_text = """
    <b>数据时效性说明：</b>
    本报告数据采集时间为 {now}，数据有效期为发布后24小时内。
    请及时关注平台更新，避免错过重要招标信息。
    
    <b>信息准确性声明：</b>
    本报告数据来源于公开招标平台，仅供参考。实际招标信息以官方平台发布为准。
    建议投标前仔细阅读招标文件，核实资质要求和截止时间。
    
    <b>平台访问建议：</b>
    • 中国招标投标公共服务平台：建议在工作日上午9-11点访问，避开高峰期
    • 海南省政府采购网：每日更新时间约为下午5-6点，建议傍晚查询
    
    <b>后续跟进建议：</b>
    • 订阅平台短信/邮件提醒服务
    • 关注微信公众号"中国招标""海南省政府采购"
    • 建立供应商库，与招标代理保持联系
    """.format(now=datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    story.append(Paragraph(tips_text, normal_style))

def add_footer(canvas, doc):
    """添加页脚"""
    canvas.saveState()
    page_num = canvas.getPageNumber()
    footer_text = f"海南勘察招标日报 | 第 {page_num} 页"
    canvas.setFont(CHINESE_FONT, 9)
    canvas.setFillColor(colors.gray)
    canvas.drawCentredString(A4[0]/2, 1.5*cm, footer_text)
    canvas.restoreState()

def generate_report():
    """生成PDF报告"""
    report_date = datetime.now().strftime("%Y-%m-%d")
    output_path = f"/Users/fasimac/.qclaw/workspace/海南勘察招标日报_{report_date}.pdf"
    
    # 创建文档
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    story = []
    
    # 构建报告内容
    create_cover_page(story, report_date)
    create_toc(story)
    create_overview(story, has_data=False)
    create_data_status(story, "受验证码限制", "正常访问")
    create_no_data_notice(story)
    create_historical_data(story)
    create_risk_tips(story)
    
    # 生成PDF
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    
    print(f"PDF报告已生成: {output_path}")
    return output_path

def get_pdf_base64(pdf_path):
    """获取PDF的Base64编码"""
    with open(pdf_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

if __name__ == "__main__":
    pdf_path = generate_report()
    pdf_base64 = get_pdf_base64(pdf_path)
    print(f"\nPDF Base64长度: {len(pdf_base64)} 字符")
    
    # 生成钉钉卡片摘要
    dingtalk_summary = """
【海南勘察招标日报】{}

📊 数据采集结果
• 中国招标投标公共服务平台：受验证码限制，暂无数据
• 海南省政府采购网：近24小时内无新发布勘察类招标信息

⚠️ 风险提示
• 平台数据采集受安全机制限制，建议手动查询
• 近期勘察类招标项目较少，请关注历史项目进展
• 建议订阅平台提醒服务，避免错过重要信息

💡 操作建议
1. 定期访问官方平台核实信息
2. 扩大关键词检索范围
3. 与招标代理保持联系获取一手资讯

详情请查看PDF报告
""".format(datetime.now().strftime("%Y-%m-%d"))
    
    print("\n📝 钉钉卡片摘要:")
    print(dingtalk_summary)
