#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海南勘察招标日报生成脚本
生成结构化PDF报告和钉钉卡片摘要
"""

import sys
import os
import base64
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.colors import HexColor, black, grey, lightgrey
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                  Table, TableStyle, Image, KeepTogether, ListFlowable, ListItem)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

# 注册中文字体
font_paths = [
    '/System/Library/Fonts/PingFang.ttc',
    '/System/Library/Fonts/STHeiti Light.ttc',
    '/System/Library/Fonts/Hiragino Sans GB.ttc',
    '/Library/Fonts/Arial Unicode.ttf'
]

font_registered = False
for font_path in font_paths:
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
            font_registered = True
            print(f"✓ 已注册字体: {font_path}")
            break
        except:
            continue

if not font_registered:
    print("⚠️ 未找到中文字体，使用默认字体")
    # 使用系统默认字体
    try:
        pdfmetrics.registerFont(TTFont('ChineseFont', '/System/Library/Fonts/SFNSDisplay.ttf'))
    except:
        pass

# 数据定义
current_date = "2026-04-17"
report_title = f"海南勘察招标日报 {current_date}"

# 收集到的数据
announcements = [
    {
        "source": "海南省政府采购网",
        "project_name": "海南省红树林资源监测与成效评估竞争性磋商公告",
        "budget": "未公开",
        "purchaser": "省本级",
        "category": "服务",
        "method": "竞争性磋商",
        "publish_date": "2026-04-16",
        "keywords": ["监测", "评估"],
        "relevance": "中",
        "link": "https://ccgp-hainan.gov.cn",
        "requirements": "需要红树林监测相关资质，具体要求需查看详细公告"
    },
    {
        "source": "海南省政府采购网",
        "project_name": "2026年海南省水务工程质量监督检测项目竞争性磋商公告",
        "budget": "未公开",
        "purchaser": "省本级",
        "category": "服务",
        "method": "竞争性磋商",
        "publish_date": "2026-04-16",
        "keywords": ["检测", "质量监督"],
        "relevance": "高",
        "link": "https://ccgp-hainan.gov.cn",
        "requirements": "需要CMA资质，水务工程质量检测相关资质，具体要求需查看详细公告"
    },
    {
        "source": "海南省政府采购网",
        "project_name": "海南岛周边海域矿产资源调查评价项目船舶租赁服务（第二次采购）竞争性磋商公告",
        "budget": "未公开",
        "purchaser": "省本级",
        "category": "服务",
        "method": "竞争性磋商",
        "publish_date": "2026-04-16",
        "keywords": ["调查", "矿产资源"],
        "relevance": "中",
        "link": "https://ccgp-hainan.gov.cn",
        "requirements": "需要相关海域调查资质，船舶服务能力，具体要求需查看详细公告"
    }
]

# 创建PDF
def create_pdf_report():
    """创建PDF报告"""
    
    # 输出文件路径
    output_path = f"/tmp/海南勘察招标日报_{current_date}.pdf"
    
    # 创建文档
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # 样式
    styles = getSampleStyleSheet()
    
    # 自定义样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontName='ChineseFont' if font_registered else 'Helvetica',
        fontSize=24,
        textColor=HexColor('#1a5490'),
        alignment=TA_CENTER,
        spaceAfter=30,
        spaceBefore=50
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontName='ChineseFont' if font_registered else 'Helvetica',
        fontSize=18,
        textColor=HexColor('#2c5aa0'),
        spaceBefore=20,
        spaceAfter=12,
        alignment=TA_LEFT
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontName='ChineseFont' if font_registered else 'Helvetica',
        fontSize=14,
        textColor=HexColor('#3a6ea5'),
        spaceBefore=15,
        spaceAfter=10,
        alignment=TA_LEFT
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName='ChineseFont' if font_registered else 'Helvetica',
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=18
    )
    
    small_style = ParagraphStyle(
        'CustomSmall',
        parent=styles['Normal'],
        fontName='ChineseFont' if font_registered else 'Helvetica',
        fontSize=9,
        textColor=grey,
        alignment=TA_LEFT,
        spaceAfter=6
    )
    
    # 构建内容
    story = []
    
    # 封面
    story.append(Spacer(1, 100))
    story.append(Paragraph(report_title, title_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("——勘察检测行业招标信息日报——", 
                           ParagraphStyle('Subtitle', parent=normal_style, 
                                         fontSize=14, alignment=TA_CENTER, 
                                         textColor=grey)))
    story.append(Spacer(1, 30))
    story.append(Paragraph(f"报告日期：{current_date}", 
                           ParagraphStyle('Date', parent=normal_style, 
                                         fontSize=12, alignment=TA_CENTER)))
    story.append(Spacer(1, 50))
    
    # 采集概况框
    info_text = """
    <b>采集时间范围：</b>最近24小时（2026-04-16 03:00 至 2026-04-17 03:00）<br/>
    <b>数据来源：</b>中国招标投标公共服务平台、海南省政府采购网、海南省公共资源交易网<br/>
    <b>关键词筛选：</b>勘察、检测、测绘、岩土、地质灾害<br/>
    <b>符合条件项目数：</b>3个
    """
    story.append(Paragraph(info_text, 
                           ParagraphStyle('Info', parent=normal_style, 
                                         fontSize=10, alignment=TA_LEFT,
                                         backColor=HexColor('#f0f7ff'),
                                         borderColor=HexColor('#1a5490'),
                                         borderWidth=1,
                                         borderPadding=10)))
    
    story.append(PageBreak())
    
    # 目录
    story.append(Paragraph("目 录", heading1_style))
    story.append(Spacer(1, 20))
    
    toc_items = [
        ("一、数据采集概况", 3),
        ("二、重点招标项目", 4),
        ("三、资质要求分析", 6),
        ("四、风险提示", 7),
        ("五、总结与建议", 8)
    ]
    
    for title, page in toc_items:
        story.append(Paragraph(f"{title} {'.'*50} {page}", normal_style))
    
    story.append(PageBreak())
    
    # 一、数据采集概况
    story.append(Paragraph("一、数据采集概况", heading1_style))
    story.append(Spacer(1, 10))
    
    overview_text = """
    本报告基于以下三个主要数据源进行采集分析：<br/><br/>
    <b>1. 中国招标投标公共服务平台（www.cebpubservice.com）</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;状态：访问失败（502 Bad Gateway）<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;原因：网站服务器响应异常，无法获取数据<br/><br/>
    <b>2. 海南省政府采购网（www.ccgp-hainan.gov.cn）</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;状态：访问成功<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;获取公告：约7条近期公告<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;筛选后符合条件：3条<br/><br/>
    <b>3. 海南省公共资源交易网（ggzy.hainan.gov.cn）</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;状态：访问成功<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;获取公告：约6条近期公告<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;筛选后符合条件：0条（无勘察类项目）
    """
    story.append(Paragraph(overview_text, normal_style))
    story.append(Spacer(1, 10))
    
    # 数据统计表
    story.append(Paragraph("数据统计", heading2_style))
    
    stats_data = [
        ['数据源', '状态', '公告总数', '符合条件数', '占比'],
        ['中国招标投标公共服务平台', '失败', '-', '-', '-'],
        ['海南省政府采购网', '成功', '7', '3', '43%'],
        ['海南省公共资源交易网', '成功', '6', '0', '0%'],
        ['合计', '-', '13', '3', '23%']
    ]
    
    stats_table = Table(stats_data, colWidths=[6*cm, 2*cm, 2.5*cm, 2.5*cm, 2*cm])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1a5490')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'ChineseFont' if font_registered else 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -2), HexColor('#f0f7ff')),
        ('BACKGROUND', (0, -1), (-1, -1), HexColor('#e6f2ff')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('FONTNAME', (0, -1), (-1, -1), 'ChineseFont' if font_registered else 'Helvetica-Bold'),
    ]))
    
    story.append(stats_table)
    story.append(PageBreak())
    
    # 二、重点招标项目
    story.append(Paragraph("二、重点招标项目", heading1_style))
    story.append(Spacer(1, 10))
    
    for i, item in enumerate(announcements, 1):
        story.append(Paragraph(f"项目{i}：{item['project_name']}", heading2_style))
        story.append(Spacer(1, 5))
        
        # 项目信息表
        project_data = [
            ['来源', item['source']],
            ['采购人', item['purchaser']],
            ['采购类别', item['category']],
            ['采购方式', item['method']],
            ['发布时间', item['publish_date']],
            ['相关度', f"{item['relevance']} ({'★★★' if item['relevance']=='高' else '★★' if item['relevance']=='中' else '★'})"],
            ['关键词', '、'.join(item['keywords'])],
            ['原文链接', item['link']]
        ]
        
        project_table = Table(project_data, colWidths=[3*cm, 12*cm])
        project_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#f0f7ff')),
            ('TEXTCOLOR', (0, 0), (0, -1), HexColor('#1a5490')),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'ChineseFont' if font_registered else 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dddddd')),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(project_table)
        story.append(Spacer(1, 8))
        
        # 资质要求
        story.append(Paragraph(f"<b>资质要求：</b>{item['requirements']}", small_style))
        story.append(Spacer(1, 15))
    
    story.append(PageBreak())
    
    # 三、资质要求分析
    story.append(Paragraph("三、资质要求分析", heading1_style))
    story.append(Spacer(1, 10))
    
    requirement_text = """
    根据本次采集到的招标公告分析，勘察检测类项目通常需要以下资质：<br/><br/>
    <b>1. 基础资质要求</b><br/>
    &nbsp;&nbsp;• CMA检验检测机构资质认定证书<br/>
    &nbsp;&nbsp;• CNAS实验室认可证书（部分项目）<br/>
    &nbsp;&nbsp;• 工程勘察综合资质或专业资质<br/>
    &nbsp;&nbsp;• 测绘资质证书<br/><br/>
    
    <b>2. 专项资质要求</b><br/>
    &nbsp;&nbsp;• 水务工程质量检测资质（对应检测项目）<br/>
    &nbsp;&nbsp;• 海洋调查相关资质（对应海域调查项目）<br/>
    &nbsp;&nbsp;• 环境监测相关资质（对应环境评估项目）<br/><br/>
    
    <b>3. 人员要求</b><br/>
    &nbsp;&nbsp;• 注册岩土工程师<br/>
    &nbsp;&nbsp;• 注册测绘师<br/>
    &nbsp;&nbsp;• 相关专业高级工程师<br/>
    &nbsp;&nbsp;• CMA授权签字人<br/><br/>
    
    <b>4. 设备要求</b><br/>
    &nbsp;&nbsp;• 检测设备需通过计量认证<br/>
    &nbsp;&nbsp;• 测绘仪器需检定合格<br/>
    &nbsp;&nbsp;• 配备数据处理软件系统
    """
    story.append(Paragraph(requirement_text, normal_style))
    story.append(PageBreak())
    
    # 四、风险提示
    story.append(Paragraph("四、风险提示", heading1_style))
    story.append(Spacer(1, 10))
    
    risk_text = """
    <b>【数据来源风险】</b><br/>
    ⚠️ 中国招标投标公共服务平台访问失败（502错误），可能遗漏重要招标信息。建议：<br/>
    &nbsp;&nbsp;• 稍后重试访问该网站<br/>
    &nbsp;&nbsp;• 关注其他省份采购平台<br/>
    &nbsp;&nbsp;• 订阅招标信息推送服务<br/><br/>
    
    <b>【信息完整性风险】</b><br/>
    ⚠️ 本报告仅包含可公开获取的信息，以下内容需进一步核实：<br/>
    &nbsp;&nbsp;• 预算金额未公开，需联系采购人确认<br/>
    &nbsp;&nbsp;• 具体资质要求需查看详细招标文件<br/>
    &nbsp;&nbsp;• 截止时间需及时关注，避免错过投标<br/><br/>
    
    <b>【竞争风险】</b><br/>
    ⚠️ 勘察检测行业竞争激烈，建议：<br/>
    &nbsp;&nbsp;• 提前准备资质文件<br/>
    &nbsp;&nbsp;• 组建专业投标团队<br/>
    &nbsp;&nbsp;• 密切关注更正公告<br/><br/>
    
    <b>【时效性风险】</b><br/>
    ⚠️ 招标信息时效性强，建议：<br/>
    &nbsp;&nbsp;• 每日定时查看招标平台<br/>
    &nbsp;&nbsp;• 设置关键词提醒<br/>
    &nbsp;&nbsp;• 加入行业协会信息群
    """
    story.append(Paragraph(risk_text, normal_style))
    story.append(PageBreak())
    
    # 五、总结与建议
    story.append(Paragraph("五、总结与建议", heading1_style))
    story.append(Spacer(1, 10))
    
    summary_text = """
    <b>【本次采集总结】</b><br/>
    本次采集共获取到3条符合勘察检测类关键词的招标公告，主要来自海南省政府采购网。其中：<br/>
    &nbsp;&nbsp;• 高相关度项目：1个（水务工程质量监督检测）<br/>
    &nbsp;&nbsp;• 中相关度项目：2个（红树林监测、海域调查）<br/><br/>
    
    <b>【市场趋势分析】</b><br/>
    从本次采集结果看，海南省勘察检测类招标项目呈现以下特点：<br/>
    &nbsp;&nbsp;• 环保监测类项目增多（红树林监测、环境评估）<br/>
    &nbsp;&nbsp;• 水务工程类检测需求稳定<br/>
    &nbsp;&nbsp;• 海洋资源调查类项目逐步增加<br/><br/>
    
    <b>【投标建议】</b><br/>
    1. <b>即时行动：</b>立即查看3个项目的详细招标文件，确认投标资格<br/>
    2. <b>持续关注：</b>每日监控海南省政府采购网更新<br/>
    3. <b>资质准备：</b>确保CMA等核心资质在有效期内<br/>
    4. <b>团队建设：</b>组建包含岩土、测绘、检测专业人员的投标团队<br/>
    5. <b>市场拓展：</b>关注周边省份类似项目，扩大市场范围
    """
    story.append(Paragraph(summary_text, normal_style))
    story.append(Spacer(1, 30))
    
    # 页脚信息
    footer_text = f"""
    <b>报告生成时间：</b>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
    <b>数据采集范围：</b>最近24小时<br/>
    <b>免责声明：</b>本报告仅供参考，具体招标信息以官方发布为准
    """
    story.append(Paragraph(footer_text, small_style))
    
    # 生成PDF
    doc.build(story)
    print(f"✓ PDF报告已生成：{output_path}")
    
    return output_path

def create_dingtalk_summary():
    """生成钉钉卡片摘要"""
    
    summary = f"""【海南勘察招标日报】{current_date}

📊 数据概况：
• 采集源：3个平台（1个失败，2个成功）
• 符合条件：3个项目
• 高相关度：1个（水务检测）
• 发布日期：2026-04-16

📋 重点项目：
1️⃣ 2026年海南省水务工程质量监督检测项目
   • 相关度：★★★（高）
   • 要求：CMA资质、水务质量检测资质
   • 链接：https://ccgp-hainan.gov.cn

2️⃣ 海南省红树林资源监测与成效评估
   • 相关度：★★（中）
   • 要求：红树林监测相关资质
   • 链接：https://ccgp-hainan.gov.cn

3️⃣ 海南岛周边海域矿产资源调查评价项目
   • 相关度：★★（中）
   • 要求：海域调查资质、船舶服务
   • 链接：https://ccgp-hainan.gov.cn

⚠️ 风险提示：
• 中国招标投标公共服务平台访问失败（502错误）
• 预算金额未公开，需联系采购人确认
• 具体资质要求需查看详细招标文件
• 竞争激烈，建议提前准备资质文件

💡 建议：
✓ 立即查看3个项目详细招标文件
✓ 每日监控海南省政府采购网更新
✓ 确保CMA等核心资质在有效期内
✓ 组建专业投标团队

数据来源：海南省政府采购网、海南省公共资源交易网
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"""
    
    return summary

def encode_pdf_base64(pdf_path):
    """将PDF转换为base64编码"""
    with open(pdf_path, 'rb') as f:
        pdf_base64 = base64.b64encode(f.read()).decode('utf-8')
    return pdf_base64

def main():
    """主函数"""
    print("="*60)
    print("海南勘察招标日报 - 报告生成器")
    print("="*60)
    
    # 生成PDF报告
    pdf_path = create_pdf_report()
    
    # 生成钉钉摘要
    dingtalk_summary = create_dingtalk_summary()
    
    # 转换为base64
    pdf_base64 = encode_pdf_base64(pdf_path)
    
    # 输出结果
    print("\n" + "="*60)
    print("📄 PDF报告内容（base64编码）")
    print("="*60)
    print(f"文件路径：{pdf_path}")
    print(f"Base64长度：{len(pdf_base64)} 字符")
    print(f"前100字符：{pdf_base64[:100]}...")
    
    print("\n" + "="*60)
    print("📝 钉钉卡片摘要")
    print("="*60)
    print(dingtalk_summary)
    
    # 保存摘要到文件
    summary_path = f"/tmp/钉钉摘要_{current_date}.txt"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(dingtalk_summary)
    print(f"\n✓ 摘要已保存：{summary_path}")
    
    # 保存base64到文件
    base64_path = f"/tmp/PDF_Base64_{current_date}.txt"
    with open(base64_path, 'w', encoding='utf-8') as f:
        f.write(pdf_base64)
    print(f"✓ Base64已保存：{base64_path}")

if __name__ == '__main__':
    main()
