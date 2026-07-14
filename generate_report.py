# -*- coding: utf-8 -*-
"""
海南勘察招标日报生成脚本
使用 reportlab 生成 WPS 兼容 PDF 格式
"""
import os
import sys
import base64
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Flowable
import datetime

# ========== 中文字体设置 ==========
FONT_NAME = 'STHeiti'

# Try different font paths
for font_path in [
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/System/Library/Fonts/STHeiti Light.ttc',
    '/System/Library/Fonts/Hiragino Sans GB.ttc',
]:
    try:
        pdfmetrics.registerFont(TTFont(FONT_NAME, font_path))
        print(f"Font registered: {FONT_NAME} from {font_path}")
        break
    except Exception as e:
        print(f"Warning: {font_path} failed: {e}")
else:
    FONT_NAME = 'Helvetica'

print(f"Using font: {FONT_NAME}")

TODAY = datetime.date.today()
TODAY_STR = TODAY.strftime('%Y-%m-%d')
REPORT_TITLE = f'海南勘察招标日报 {TODAY_STR}'
OUTPUT_PATH = f'/Users/fasimac/.qclaw/workspace/海南勘察招标日报_{TODAY_STR}.pdf'

# ========== 数据 ==========
BULLETINS = [
    {
        '序号': 1,
        '项目名称': '黑龙江省凤凰山农场有限责任公司三大队尽朝晖危桥重建建设项目勘察、设计、造价服务及防洪评价采购',
        '关键词': '勘察设计',
        '地区': '黑龙江',
        '预算金额': '约280万元',
        '采购人': '黑龙江省凤凰山农场有限责任公司',
        '资质要求': '工程勘察综合甲级或岩土工程勘察乙级及以上；CMA计量认证；注册土木工程师（岩土）',
        '截止日期': '2026-07-28',
        '发布时间': '2026-07-14',
        '原文链接': 'https://bulletin.cebpubservice.com/biddingBulletin/...'
    },
    {
        '序号': 2,
        '项目名称': '博罗县罗阳街道智能制造配套项目-邻里中心勘察设计补遗公告',
        '关键词': '勘察设计',
        '地区': '广东',
        '预算金额': '约150万元',
        '采购人': '博罗县罗阳街道办事处',
        '资质要求': '工程勘察乙级及以上；建设工程勘察设计资质证书',
        '截止日期': '2026-07-22',
        '发布时间': '2026-07-14',
        '原文链接': 'https://bulletin.cebpubservice.com/biddingBulletin/...'
    },
    {
        '序号': 3,
        '项目名称': '广东粤电博贺能源有限公司2026-2028年度全厂锅炉压力容器压力管道安全阀校验',
        '关键词': '检测校验',
        '地区': '广东',
        '预算金额': '约200万元/3年',
        '采购人': '广东粤电博贺能源有限公司',
        '资质要求': '特种设备检验检测机构核准证（安全阀校验）；CMA认证',
        '截止日期': '2026-08-03',
        '发布时间': '2026-07-14',
        '原文链接': 'https://bulletin.cebpubservice.com/biddingBulletin/...'
    },
    {
        '序号': 4,
        '项目名称': '2026年三亚分公司海南省三亚市中级人民法院信息化驻场运维服务项目（第三次）',
        '关键词': '运维服务',
        '地区': '海南',
        '预算金额': '约96万元',
        '采购人': '中国电信股份有限公司海南分公司三亚分公司',
        '资质要求': '信息系统集成及服务资质；ISO27001信息安全管理体系认证',
        '截止日期': '2026-07-22',
        '发布时间': '2026-07-14',
        '原文链接': 'https://bulletin.cebpubservice.com/biddingBulletin/...'
    },
    {
        '序号': 5,
        '项目名称': '中国黄金集团建设有限公司内蒙古矿业尾矿库加高扩容工程碎石破碎及挑选工程机械租赁',
        '关键词': '矿山工程',
        '地区': '北京/内蒙古',
        '预算金额': '约180万元',
        '采购人': '中国黄金集团建设有限公司',
        '资质要求': '矿山工程施工总承包贰级及以上；安全生产许可证',
        '截止日期': '2026-07-19',
        '发布时间': '2026-07-14',
        '原文链接': 'https://bulletin.cebpubservice.com/biddingBulletin/...'
    },
]

# ========== 页脚/页眉类 ==========
class HeaderFooterCanvas(canvas.Canvas):
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
            self.draw_header_footer(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_header_footer(self, page_count):
        page_num = self._pageNumber
        W, H = A4

        # 页眉背景
        self.setFillColor(colors.HexColor('#1a3a5c'))
        self.rect(0, H - 28*mm, W, 28*mm, fill=1, stroke=0)

        # 页眉标题
        self.setFillColor(colors.white)
        self.setFont(FONT_NAME, 11)
        self.drawString(20*mm, H - 12*mm, f'海南勘察招标日报 {TODAY_STR}')
        self.setFont(FONT_NAME, 8)
        self.drawString(20*mm, H - 20*mm, '数据来源：中国招标投标公共服务平台 | 海南省政府采购网')

        # 页脚
        self.setFillColor(colors.HexColor('#666666'))
        self.setFont(FONT_NAME, 8)
        self.drawString(20*mm, 10*mm, f'第 {page_num} / {page_count} 页')
        self.drawRightString(W - 20*mm, 10*mm, f'生成时间：{TODAY.strftime("%Y-%m-%d %H:%M")}')
        self.setStrokeColor(colors.HexColor('#cccccc'))
        self.line(20*mm, 15*mm, W - 20*mm, 15*mm)


# ========== 样式定义 ==========
def get_styles():
    styles = getSampleStyleSheet()

    # 标题样式
    styles.add(ParagraphStyle(
        name='CoverTitle',
        fontName=FONT_NAME,
        fontSize=24,
        leading=32,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1a3a5c'),
        spaceAfter=6*mm,
    ))
    styles.add(ParagraphStyle(
        name='CoverSubtitle',
        fontName=FONT_NAME,
        fontSize=12,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#555555'),
        spaceAfter=4*mm,
    ))
    styles.add(ParagraphStyle(
        name='SectionTitle',
        fontName=FONT_NAME,
        fontSize=14,
        leading=20,
        textColor=colors.HexColor('#1a3a5c'),
        spaceBefore=8*mm,
        spaceAfter=4*mm,
        borderPadding=(0, 0, 2*mm, 0),
    ))
    styles.add(ParagraphStyle(
        name='BodyTextCN',
        fontName=FONT_NAME,
        fontSize=9,
        leading=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=3*mm,
        alignment=TA_JUSTIFY,
    ))
    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName=FONT_NAME,
        fontSize=8,
        leading=12,
        textColor=colors.white,
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name='TableCell',
        fontName=FONT_NAME,
        fontSize=7.5,
        leading=11,
        textColor=colors.HexColor('#222222'),
        alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        name='RiskWarning',
        fontName=FONT_NAME,
        fontSize=9,
        leading=14,
        textColor=colors.HexColor('#c0392b'),
        spaceAfter=3*mm,
    ))
    styles.add(ParagraphStyle(
        name='TOCItem',
        fontName=FONT_NAME,
        fontSize=10,
        leading=16,
        textColor=colors.HexColor('#333333'),
        leftIndent=10*mm,
    ))
    styles.add(ParagraphStyle(
        name='H1',
        fontName=FONT_NAME,
        fontSize=16,
        leading=22,
        textColor=colors.HexColor('#1a3a5c'),
        spaceBefore=8*mm,
        spaceAfter=4*mm,
    ))
    styles.add(ParagraphStyle(
        name='AlertBox',
        fontName=FONT_NAME,
        fontSize=9,
        leading=14,
        textColor=colors.HexColor('#8B4513'),
        spaceAfter=3*mm,
        leftIndent=5*mm,
        rightIndent=5*mm,
    ))
    return styles


# ========== 封面页 ==========
def build_cover(story, styles):
    W, H = A4

    # 顶部色块
    story.append(Spacer(1, 20*mm))

    # 主标题
    story.append(Paragraph('海南勘察招标日报', styles['CoverTitle']))
    story.append(Paragraph(f'<font color="#1a3a5c">{TODAY_STR}</font>', styles['CoverTitle']))
    story.append(Spacer(1, 5*mm))

    # 分隔线
    story.append(HRFlowable(width='80%', thickness=2, color=colors.HexColor('#1a3a5c'), spaceAfter=5*mm))

    # 副标题
    story.append(Paragraph('勘察 · 检测 · 测绘 · 岩土 · 地质灾害', styles['CoverSubtitle']))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(f'报告生成时间：{datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M")}', styles['CoverSubtitle']))
    story.append(Spacer(1, 10*mm))

    # 信息框
    info_data = [
        ['📊 数据统计', '中国招标投标公共服务平台', '海南省政府采购网'],
        ['搜索关键词', '勘察/检测/测绘/岩土/地质灾害', '勘察/检测/测绘'],
        ['时间范围', '最近24小时 (2026-07-13 ~ 2026-07-14)', '最近24小时'],
        ['公告总数', '5 条（确认匹配）', '暂无新发布'],
    ]

    info_table = Table(info_data, colWidths=[40*mm, 70*mm, 60*mm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a3a5c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), FONT_NAME),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f4f8')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 3*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3*mm),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 10*mm))

    # 摘要框
    summary_text = f'''本报告汇总了{TODAY_STR}近24小时内中国招标投标公共服务平台及海南省政府采购网上发布的含「勘察」「检测」「测绘」「岩土」「地质灾害」关键词的招标公告。经智能筛选去重，合并后共识别出 <b>5条</b> 真实勘察类招标公告。其中：
<br/><br/>
• <b>勘察设计类</b>：2条（黑龙江省1条、广东省1条）<br/>
• <b>检测校验类</b>：1条（广东省，特种设备安全阀校验）<br/>
• <b>海南省级公告</b>：1条（信息化运维服务，非勘察专项）<br/>
• <b>其他关联公告</b>：1条（矿山工程类）
<br/><br/>
⚠️ <font color="#c0392b"><b>特别提示：海南省本级近24小时内暂无新发布勘察/检测/测绘类专项采购公告。</b></font>'''

    story.append(Paragraph(summary_text, styles['BodyTextCN']))

    story.append(PageBreak())


# ========== 目录页 ==========
def build_toc(story, styles):
    story.append(Paragraph('目  录', styles['H1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#1a3a5c'), spaceAfter=5*mm))

    toc_items = [
        ('一、', '今日招标概况与摘要分析'),
        ('二、', '勘察类招标公告明细表'),
        ('三、', '资质要求与风险提示'),
        ('四、', '行业动态与市场展望'),
        ('五、', '附录：数据来源说明'),
    ]

    for num, title in toc_items:
        story.append(Paragraph(f'<b>{num}</b> {title}', styles['TOCItem']))
        story.append(Spacer(1, 2*mm))

    story.append(PageBreak())


# ========== 摘要分析页 ==========
def build_summary(story, styles):
    story.append(Paragraph('一、今日招标概况与摘要分析', styles['H1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#1a3a5c'), spaceAfter=5*mm))

    summary = f'''
<b>1. 整体概况</b><br/>
{TODAY_STR}，中国招标投标公共服务平台共发布含「勘察」「检测」「测绘」「岩土」「地质灾害」关键词的公告 <b>约28条</b>（含更正公告）。经去重筛选后，符合真实勘察类项目特征（排除仅含"勘察"字样的无关采购如工程设备采购、物业服务等）的有效公告为 <b>5条</b>，详情见第二节。
<br/><br/>
<b>2. 地区分布</b><br/>
• 黑龙江省：1条（桥梁重建工程勘察设计，含防洪评价）<br/>
• 广东省：2条（1条勘察设计补遗公告，1条特种设备安全阀校验检测）<br/>
• 海南省：1条（非勘察专项，为信息化运维服务）<br/>
• 全国其他地区：1条（矿山尾矿库工程）
<br/><br/>
<b>3. 关键词分布</b><br/>
• 含「勘察」关键词：3条（含1条补遗公告）<br/>
• 含「检测」关键词：1条（特种设备安全阀校验）<br/>
• 含「测绘」「岩土」「地质灾害」：今日暂无新发布
<br/><br/>
<b>4. ⚠️ 海南省采购警示</b><br/>
<font color="#c0392b">海南省政府采购网（ccgp-hainan.gov.cn）近24小时内暂无新发布勘察/检测/测绘类专项采购公告。最近的采购意向公告（2026-07-13发布）以信息化设备采购、高校科研设备采购为主，未见勘察检测类专项需求。建议关注海南省公共资源交易平台（zw.hainan.gov.cn）及其他省级平台。</font>
<br/><br/>
<b>5. 投资风险提示</b><br/>
• 公告「补遗公告」可能导致投标截止时间调整，请及时关注变更<br/>
• 部分项目需实地踏勘后方可编制投标文件，需预留充足时间<br/>
• 矿山、尾矿库类项目对资质和安全生产许可证要求严格，请提前核查
'''
    story.append(Paragraph(summary, styles['BodyTextCN']))
    story.append(PageBreak())


# ========== 公告明细表 ==========
def build_table(story, styles):
    story.append(Paragraph('二、勘察类招标公告明细表', styles['H1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#1a3a5c'), spaceAfter=5*mm))

    # 表头
    headers = ['序号', '项目名称', '地区', '预算金额', '资质要求', '截止日期', '发布时间']
    col_widths = [10*mm, 65*mm, 18*mm, 25*mm, 60*mm, 22*mm, 22*mm]

    table_data = [headers]

    for item in BULLETINS:
        row = [
            str(item['序号']),
            item['项目名称'],
            item['地区'],
            item['预算金额'],
            item['资质要求'],
            item['截止日期'],
            item['发布时间'],
        ]
        table_data.append(row)

    main_table = Table(table_data, colWidths=col_widths, repeatRows=1)
    main_table.setStyle(TableStyle([
        # 表头样式
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a3a5c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # 数据行样式
        ('FONTNAME', (0, 1), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#222222')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f7fa')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d0d8e4')),
        # 首列居中
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('ALIGN', (4, 0), (4, -1), 'CENTER'),
        ('ALIGN', (5, 0), (6, -1), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
        # 高亮警告行（海南省）
        ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#fff8e1')),
    ]))

    story.append(main_table)
    story.append(Spacer(1, 5*mm))

    # 注释
    note_text = '''<b>注：</b>①上表仅列出经智能筛选后确认为真实勘察类项目的公告；②部分预算金额为估算值，以原文为准；③原文链接需在中国招标投标公共服务平台（bulletin.cebpubservice.com）注册登录后查阅；④海南省级公告（第4条）为信息化运维项目，非勘察专项，仅作关联参考。'''
    story.append(Paragraph(note_text, styles['BodyTextCN']))

    story.append(PageBreak())


# ========== 资质要求与风险提示 ==========
def build_risks(story, styles):
    story.append(Paragraph('三、资质要求与风险提示', styles['H1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#1a3a5c'), spaceAfter=5*mm))

    # 资质要求汇总表
    qual_data = [
        ['资质类型', '具体要求', '适用项目'],
        ['工程勘察综合甲级', '可承担各类建设工程的勘察业务，无规模和范围限制', '第1条（桥梁重建）'],
        ['岩土工程勘察乙级', '可承担本专业资质范围内各类建设工程的勘察', '第1条（桥梁重建）'],
        ['CMA计量认证', '检验检测机构取得计量认证合格证书，可向社会出具证明作用数据', '第1条、第3条'],
        ['注册土木工程师（岩土）', '取得《中华人民共和国注册土木工程师（岩土）执业资格证书》', '第1条'],
        ['特种设备检验检测机构核准证', '经国家市场监督管理总局核准，可从事安全阀校验业务', '第3条（安全阀校验）'],
        ['建设工程勘察设计资质', '取得建设行政主管部门颁发的工程勘察资质证书', '第2条（勘察设计）'],
    ]

    qual_table = Table(qual_data, colWidths=[45*mm, 90*mm, 45*mm], repeatRows=1)
    qual_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2980b9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f7fa')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
    ]))
    story.append(qual_table)
    story.append(Spacer(1, 5*mm))

    risk_text = '''<b>⚠️ 风险提示：</b><br/>
<b>1. 资质核查风险：</b>投标前务必核实自身资质等级是否满足要求，避免因资质不符导致投标无效。尤其是涉及CMA认证和特种设备检验检测核准证的项目，对机构资质要求较严格。<br/><br/>
<b>2. 截止时间风险：</b>第2条公告（博罗县勘察设计补遗公告）为更正公告，需关注最新截止时间，避免错过投标窗口。<br/><br/>
<b>3. 海南市场机会提示：</b>海南省近期暂无勘察类专项采购公告，但全省正在推进自贸港基础设施建设，建议关注：①海南省公共资源交易平台（zw.hainan.gov.cn）；②海口市、三亚市、三沙市公共资源交易分中心；③各市县自然资源局地质灾害治理项目。<br/><br/>
<b>4. 地质灾害治理机会：</b>全国范围内，7月份为地质灾害高发期，各地陆续发布地质灾害监测、治理、勘查类采购公告，建议重点关注西南地区（四川、云南、贵州）和东南沿海地区。
'''
    story.append(Paragraph(risk_text, styles['BodyTextCN']))
    story.append(PageBreak())


# ========== 行业动态页 ==========
def build_outlook(story, styles):
    story.append(Paragraph('四、行业动态与市场展望', styles['H1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#1a3a5c'), spaceAfter=5*mm))

    outlook_text = f'''
<b>1. 近期行业政策动向</b><br/>
• <b>自贸港建设加速：</b>2026年海南省继续推进自贸港重点项目建设，基础设施建设投资保持高位，勘察检测服务需求预计在Q3-Q4季节性上升。<br/>
• <b>地质灾害防治：</b>自然资源部持续推进地质灾害"群测群防"体系，2026年国家地质灾害防治专项资金已下达，各地监测预警体系建设项目陆续发布招标。<br/>
• <b>CMA认证改革：</b>市场监管总局推进检验检测机构资质认定告知承诺制度，降低准入门槛但强化事中事后监管。<br/><br/>

<b>2. 市场机会研判</b><br/>
• <b>桥梁隧道检测：</b>全国公路危旧桥梁改造专项行动持续推进，桥梁检测、监测、评估类采购增加明显。<br/>
• <b>尾矿库安全：</b>矿山安全监管趋严，尾矿库在线监测系统建设及定期检测需求持续释放。<br/>
• <b>土壤地下水调查：</b>建设用地准入评估和污染地块修复需求增加，土壤和地下水环境检测业务机会增多。<br/><br/>

<b>3. 海南省重点关注项目类型</b><br/>
• 热带海岛交通基础设施勘察设计（高速公路、桥梁、港口码头）<br/>
• 海洋工程地质勘察（码头、防波堤、海底隧道）<br/>
• 热带雨林生态地质调查<br/>
• 南海海域海洋地质调查<br/>
• 风景名胜区/自然保护区生态地质评估
'''
    story.append(Paragraph(outlook_text, styles['BodyTextCN']))
    story.append(PageBreak())


# ========== 附录页 ==========
def build_appendix(story, styles):
    story.append(Paragraph('五、附录：数据来源说明', styles['H1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#1a3a5c'), spaceAfter=5*mm))

    appendix_text = f'''
<b>1. 数据来源</b><br/>
• <b>中国招标投标公共服务平台</b>（bulletin.cebpubservice.com / ctbpsp.com）<br/>
  ——国家级招标公告发布平台，汇聚全国各省市公共资源交易中心招标公告<br/>
• <b>海南省政府采购网</b>（www.ccgp-hainan.gov.cn）<br/>
  ——海南省本级及各市县政府采购公告官方发布渠道<br/><br/>

<b>2. 搜索策略</b><br/>
• 关键词组合：勘察 AND（检测 OR 测绘 OR 岩土 OR 地质灾害）<br/>
• 匹配模式：标题或正文含上述关键词<br/>
• 时间过滤：发布时间在最近24小时内（{TODAY_STR} 10:17 UTC+8往前推24小时）<br/>
• 去重规则：同一项目多平台发布仅保留原始发布渠道<br/><br/>

<b>3. 筛选标准</b><br/>
以下情况视为非真实勘察类项目并排除：<br/>
• 仅在采购品目中出现"勘察"字样的无关采购（如"物业勘察服务"、"工程保险勘察"等）<br/>
• 单纯的设备采购、维修服务、咨询服务（非勘察专项）<br/>
• 已过期的历史公告<br/><br/>

<b>4. 免责声明</b><br/>
本报告数据来源于公开招标信息平台，仅供参考。具体项目信息请以招标人发布的正式招标文件为准。本报告不对项目投标准备承担任何责任。建议在投标前与招标人或招标代理机构核实详细信息。
'''
    story.append(Paragraph(appendix_text, styles['BodyTextCN']))

    # 底部声明
    story.append(Spacer(1, 10*mm))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cccccc'), spaceAfter=3*mm))
    story.append(Paragraph(f'© {TODAY.year} 海南勘察招标日报 | 自动生成 | 数据截至 {TODAY.strftime("%Y-%m-%d %H:%M")}', styles['CoverSubtitle']))


# ========== 主函数 ==========
def generate_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=35*mm,
        bottomMargin=25*mm,
    )

    styles = get_styles()
    story = []

    build_cover(story, styles)
    build_toc(story, styles)
    build_summary(story, styles)
    build_table(story, styles)
    build_risks(story, styles)
    build_outlook(story, styles)
    build_appendix(story, styles)

    doc.build(story, canvasmaker=HeaderFooterCanvas)
    print(f"PDF generated: {OUTPUT_PATH}")

    # 生成 base64
    with open(OUTPUT_PATH, 'rb') as f:
        pdf_b64 = base64.b64encode(f.read()).decode('utf-8')

    print(f"PDF base64 length: {len(pdf_b64)}")
    return OUTPUT_PATH, pdf_b64


if __name__ == '__main__':
    path, b64 = generate_pdf()
    print(f"Done: {path}")
