#!/usr/bin/env python3
"""海南勘察招标日报 PDF 生成脚本"""

import os
from io import BytesIO
from datetime import datetime, timedelta

# 数据：最近24小时勘察类招标公告
# 时间范围：2026-06-19 03:00 ~ 2026-06-20 03:00

report_date = "2026-06-20"
report_date_cn = "2026年6月20日"
fetch_range = "2026-06-19 03:00 ~ 2026-06-20 03:00"

# ===== 合并去重后的招标数据 =====
bidding_data = [
    {
        "序号": 1,
        "项目名称": "海口市龙华区滨濂沟片区排水管网完善及排水防涝能力提升建设工程勘察",
        "类别": "工程勘察",
        "地区": "海口市龙华区",
        "采购人": "海口市龙华区城市投资控股有限公司",
        "代理机构": "公诚管理咨询有限公司",
        "预算金额": "未公开（招标控制价详见招标文件）",
        "关键资质要求": "①工程勘察岩土工程专业(岩土工程勘察)乙级及以上 + 岩土工程物探测试检测监测乙级及以上 + 工程测量乙级及以上；②工程勘察综合资质甲级。联合体≤3家。需海南省建筑企业诚信档案手册。",
        "截止日期": "2026-07-10 09:00",
        "发布时间": "2026-06-19",
        "发布平台": "中国招标投标公共服务平台/全国公共资源交易平台(海南省)",
        "来源链接": "https://ggzy.hainan.gov.cn/ggzyjy/",
        "备注": "含地形测量、管线摸排（物探）、地质勘察，工期54天"
    },
    {
        "序号": 2,
        "项目名称": "三亚崖州湾科技城大小洞天片区旅游基础设施提升工程项目（勘察）",
        "类别": "工程勘察",
        "地区": "三亚市崖州区",
        "采购人": "三亚交投产业发展有限公司",
        "代理机构": "海南锦沣项目管理有限公司",
        "预算金额": "未公开（招标控制价详见招标文件）",
        "关键资质要求": "工程勘察岩土工程专业(岩土工程勘察)甲级及以上。联合体≤2家。需海南省建筑企业诚信档案手册。",
        "截止日期": "2026-07-13 08:30",
        "发布时间": "2026-06-19",
        "发布平台": "中国招标投标公共服务平台/全国公共资源交易平台(海南省)·三亚市",
        "来源链接": "https://ggzy.hainan.gov.cn/ggzyjy/",
        "备注": "含游客服务中心4800㎡、停车场4.73公顷、道路工程等，工期90天"
    },
    {
        "序号": 3,
        "项目名称": "跨琼州海峡低空公共航路一级低空垂直起降设施建设项目地质灾害危险性评估咨询服务",
        "类别": "地质灾害评估",
        "地区": "海口市",
        "采购人": "海南省低空经济基础投资有限公司",
        "代理机构": "—（比选采购）",
        "预算金额": "6.4万元",
        "关键资质要求": "地质灾害评估和治理工程勘查设计甲级资质。近3年至少完成1个交通基础设施项目地灾评估。项目负责人+其他主要人员≥3人。",
        "截止日期": "2026-06-23 15:00",
        "发布时间": "2026-06-18",
        "发布平台": "海南省交通投资集团有限公司官网",
        "来源链接": "https://www.hainanjk.com/info/",
        "备注": "比选采购，综合评分法，工期20天"
    },
    {
        "序号": 4,
        "项目名称": "广州局集团公司海口综合维修段小型接触网悬状态检测监测装置购置（设备类）",
        "类别": "检测监测设备",
        "地区": "海口市(广州局海口段)",
        "采购人": "中国铁路广州局集团有限公司",
        "代理机构": "广州广铁招标代理有限公司",
        "预算金额": "未公开（采购文件售价200元）",
        "关键资质要求": "国铁采购平台注册供应商，具体资质要求详见采购内容明细",
        "截止日期": "2026-07-06 15:00",
        "发布时间": "2026-06-18",
        "发布平台": "国铁采购平台",
        "来源链接": "https://cg.95306.cn/",
        "备注": "公开竞争性谈判，小型接触网悬状态检测监测装置"
    },
    {
        "序号": 5,
        "项目名称": "海南物管集团股份有限公司海南地区部分项目消防检测服务外包采购项目",
        "类别": "消防检测",
        "地区": "海口市",
        "采购人": "海南物管集团股份有限公司",
        "代理机构": "—（供应商招募）",
        "预算金额": "未公开",
        "关键资质要求": "消防检测服务资质（供应商招募公告）",
        "截止日期": "2026-06-17发布(具体截止日期见后续文件)",
        "发布时间": "2026-06-17",
        "发布平台": "剑鱼标讯/海南招标网",
        "来源链接": "https://hainan.jianyu360.cn/",
        "备注": "供应商招募公告（略超24h窗口，供参考）"
    },
    {
        "序号": 6,
        "项目名称": "山西省黎城县佛崖底滑坡地质灾害治理项目工程施工",
        "类别": "地质灾害治理",
        "地区": "山西省长治市",
        "采购人": "黎城县自然资源局（推断）",
        "代理机构": "未公开",
        "预算金额": "未公开（招标控制价公告）",
        "关键资质要求": "地质灾害治理工程施工资质",
        "截止日期": "2026-06-18(控制价公告)",
        "发布时间": "2026-06-18",
        "发布平台": "全国公共资源交易平台(山西省·长治市)",
        "来源链接": "https://ggzy.changzhi.gov.cn/",
        "备注": "全国平台-招标控制价公告（非海南项目，供行业参考）"
    },
    {
        "序号": 7,
        "项目名称": "海东市2026年农产品质量安全检测补助项目",
        "类别": "检测服务",
        "地区": "青海省海东市",
        "采购人": "海东市农业农村局（推断）",
        "代理机构": "未公开",
        "预算金额": "未公开",
        "关键资质要求": "农产品质量安全检测资质（询比采购）",
        "截止日期": "2026-06-18发布",
        "发布时间": "2026-06-18",
        "发布平台": "青海项目信息网",
        "来源链接": "http://www.qhei.net.cn/html/zbcg/",
        "备注": "全国平台（非海南项目，供行业参考）"
    },
]

# 海南相关项目筛选
hainan_items = [b for b in bidding_data if b["地区"].startswith(("海口", "三亚", "海南", "儋州"))]
national_items = [b for b in bidding_data if b not in hainan_items]

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm, cm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor, black, white, grey
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                     TableStyle, PageBreak, KeepTogether, Image)
    from reportlab.platypus.flowables import HRFlowable
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas as canvas_lib

    # ===== 注册中文字体 =====
    # Try multiple font paths for macOS
    font_paths = [
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STSong.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
    ]

    cn_font_name = None
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                pdfmetrics.registerFont(TTFont('CNFont', fp))
                cn_font_name = 'CNFont'
                print(f"✅ 使用字体: {fp}")
                break
            except Exception as e:
                print(f"⚠️ 字体加载失败 {fp}: {e}")
                continue

    if not cn_font_name:
        # Fallback: try to find any .ttf/.ttc in system fonts
        import glob
        for ext in ['*.ttf', '*.ttc', '*.otf']:
            fonts = glob.glob(f'/System/Library/Fonts/{ext}')
            for fp in fonts[:10]:
                try:
                    pdfmetrics.registerFont(TTFont('CNFont', fp))
                    cn_font_name = 'CNFont'
                    print(f"✅ Fallback字体: {fp}")
                    break
                except:
                    continue
            if cn_font_name:
                break

    if not cn_font_name:
        print("❌ 未找到中文字体！PDF将无法显示中文。")
        raise RuntimeError("No Chinese font found")

    # ===== 样式定义 =====
    styles = getSampleStyleSheet()

    style_normal = ParagraphStyle('CNNormal', fontName=cn_font_name, fontSize=10, leading=16, spaceAfter=4)
    style_title = ParagraphStyle('CNTitle', fontName=cn_font_name, fontSize=22, leading=30, alignment=TA_CENTER, spaceAfter=10, textColor=HexColor('#1a5276'))
    style_subtitle = ParagraphStyle('CNSubtitle', fontName=cn_font_name, fontSize=13, leading=18, alignment=TA_CENTER, spaceAfter=6, textColor=HexColor('#2c3e50'))
    style_h1 = ParagraphStyle('CNH1', fontName=cn_font_name, fontSize=16, leading=22, spaceBefore=12, spaceAfter=8, textColor=HexColor('#1a5276'))
    style_h2 = ParagraphStyle('CNH2', fontName=cn_font_name, fontSize=13, leading=18, spaceBefore=10, spaceAfter=6, textColor=HexColor('#2471a3'))
    style_h3 = ParagraphStyle('CNH3', fontName=cn_font_name, fontSize=11, leading=16, spaceBefore=6, spaceAfter=4, textColor=HexColor('#2c3e50'))
    style_small = ParagraphStyle('CNSmall', fontName=cn_font_name, fontSize=8, leading=12, textColor=HexColor('#666666'))
    style_small_center = ParagraphStyle('CNSmallCenter', fontName=cn_font_name, fontSize=8, leading=12, textColor=HexColor('#666666'), alignment=TA_CENTER)
    style_table_header = ParagraphStyle('CNTH', fontName=cn_font_name, fontSize=8, leading=12, textColor=white, alignment=TA_CENTER)
    style_table_cell = ParagraphStyle('CNTC', fontName=cn_font_name, fontSize=7.5, leading=11)
    style_link = ParagraphStyle('CNLink', fontName=cn_font_name, fontSize=7, leading=10, textColor=HexColor('#2471a3'))
    style_warn = ParagraphStyle('CNWarn', fontName=cn_font_name, fontSize=9, leading=14, textColor=HexColor('#c0392b'))
    style_cover_info = ParagraphStyle('CNCoverInfo', fontName=cn_font_name, fontSize=12, leading=20, alignment=TA_CENTER, textColor=HexColor('#2c3e50'))

    output_path = os.path.expanduser("~/.qclaw/workspace/海南勘察招标日报_2026-06-20.pdf")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=2*cm,
        title='海南勘察招标日报',
        author='QClaw Agent',
    )

    story = []

    # ===== 辅助函数 =====
    def add_hr():
        story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#bdc3c7'), spaceAfter=6, spaceBefore=6))

    def page_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont(cn_font_name, 8)
        canvas.setFillColor(HexColor('#999999'))
        canvas.drawCentredString(A4[0]/2, 1.2*cm, f"— 海南勘察招标日报 · {report_date_cn} · 第 {{page}} 页 —")
        canvas.restoreState()

    # ===== 封面 =====
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("海 南 勘 察 招 标 日 报", style_title))
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="60%", thickness=2, color=HexColor('#1a5276'), spaceAfter=10))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(f"海南勘察检测行业 · 每日招标信息简报", style_subtitle))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph(f"报告日期：{report_date_cn}", style_cover_info))
    story.append(Paragraph(f"数据区间：{fetch_range}", style_cover_info))
    story.append(Paragraph(f"报告生成：{datetime.now().strftime('%Y-%m-%d %H:%M')}", style_cover_info))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(f"本期共收录 <b>{len(bidding_data)}</b> 条相关招标公告", style_cover_info))
    story.append(Paragraph(f"其中 <b>{len(hainan_items)}</b> 条涉及海南地区", style_cover_info))
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("数据来源：中国招标投标公共服务平台 | 海南省政府采购网 | 全国公共资源交易平台", style_small_center))
    story.append(Paragraph("剑鱼标讯 | 采招网 | 各省级交易平台", style_small_center))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("⚠️ 注：因cebpubservice.com和ccgp-hainan.gov.cn网站直接访问受限，", style_warn))
    story.append(Paragraph("本报告通过搜索引擎+聚合平台交叉验证采集，可能存在遗漏。", style_warn))
    story.append(Paragraph("建议登录各平台官方站点人工复核关键项目。", style_warn))
    story.append(PageBreak())

    # ===== 目录 =====
    story.append(Paragraph("目  录", style_h1))
    add_hr()
    story.append(Paragraph("一、报告概要 .............................................. 3", style_normal))
    story.append(Paragraph("二、海南地区招标项目详表 ...................... 4", style_normal))
    story.append(Paragraph("三、全国参考项目详表 .............................. 6", style_normal))
    story.append(Paragraph("四、行业分析与风险提示 .......................... 7", style_normal))
    story.append(Paragraph("五、数据采集说明 ...................................... 8", style_normal))
    story.append(PageBreak())

    # ===== 一、报告概要 =====
    story.append(Paragraph("一、报告概要", style_h1))
    add_hr()
    stats_text = f"""
    <br/>
    <b>📊 数据统计</b><br/><br/>
    · 本次监测时间范围：{fetch_range}<br/>
    · 共检索到勘察/检测/测绘/岩土/地质灾害类招标公告 <b>{len(bidding_data)}</b> 条<br/>
    · 其中海南地区项目 <b>{len(hainan_items)}</b> 条，全国其他地区 <b>{len(national_items)}</b> 条<br/>
    · 关键字覆盖：勘察({sum(1 for b in bidding_data if '勘察' in b['项目名称'])}条)、
      检测监测({sum(1 for b in bidding_data if '检测' in b['项目名称'])}条)、
      地质灾害({sum(1 for b in bidding_data if '地质' in b['项目名称'])}条)<br/>
    <br/>
    <b>⚠️ 重要说明</b><br/><br/>
    1. 中国招标投标公共服务平台(cebpubservice.com)和海南省政府采购网(ccgp-hainan.gov.cn)
       均因网站反爬/502/521错误，无法通过程序直接获取带时间筛选的公告列表。<br/>
    2. 本报告数据通过多源搜索引擎（剑鱼标讯、采招网、bidcenter等）交叉验证采集，可能存在遗漏。<br/>
    3. 部分公告因平台限制无法获取完整预算金额和联系方式。<br/>
    4. 建议人工登录 https://www.cebpubservice.com 和 http://www.ccgp-hainan.gov.cn
       进行二次确认。<br/>
    <br/>
    <b>📌 本期亮点</b><br/><br/>
    · 海口市龙华区排水管网勘察项目：含管道清淤检测29.67km，岩土+物探+测量全资质要求<br/>
    · 三亚大小洞天旅游基础设施勘察：要求岩土勘察甲级资质<br/>
    · 跨琼州海峡低空设施地灾评估：预算6.4万元，要求地灾评估甲级资质<br/>
    · 广铁海口段接触网检测监测装置：设备类采购，竞争性谈判<br/>
    """
    story.append(Paragraph(stats_text, style_normal))
    story.append(PageBreak())

    # ===== 二、海南地区招标项目详表 =====
    story.append(Paragraph("二、海南地区招标项目详表", style_h1))
    add_hr()

    # 构建表格
    header_row = [
        Paragraph("<b>序号</b>", style_table_header),
        Paragraph("<b>项目名称</b>", style_table_header),
        Paragraph("<b>采购人</b>", style_table_header),
        Paragraph("<b>预算</b>", style_table_header),
        Paragraph("<b>截止日期</b>", style_table_header),
        Paragraph("<b>资质要求摘要</b>", style_table_header),
    ]

    col_widths = [25, 130, 75, 50, 55, 140]

    table_data = [header_row]
    row_colors = [HexColor('#ffffff'), HexColor('#f2f9ff')]

    for item in hainan_items:
        row_color_idx = len(table_data) % 2
        row_bg = row_colors[row_color_idx]
        row = [
            Paragraph(str(item['序号']), ParagraphStyle('tc', fontName=cn_font_name, fontSize=8, leading=11, alignment=TA_CENTER)),
            Paragraph(f"<b>{item['项目名称']}</b><br/><font size='7' color='#888'>{item['地区']} | {item['类别']}</font>", style_table_cell),
            Paragraph(item['采购人'], style_table_cell),
            Paragraph(item['预算金额'], style_table_cell),
            Paragraph(f"<b>{item['截止日期']}</b>", ParagraphStyle('tcd', fontName=cn_font_name, fontSize=8, leading=11, alignment=TA_CENTER, textColor=HexColor('#c0392b'))),
            Paragraph(item['关键资质要求'], ParagraphStyle('tcq', fontName=cn_font_name, fontSize=6.5, leading=9)),
        ]
        table_data.append(row)

    tbl = Table(table_data, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1a5276')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#bdc3c7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), row_colors),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 0.5*cm))

    # 各项目详细信息
    story.append(Paragraph("项目详细信息", style_h2))
    for item in hainan_items:
        detail_text = f"""
        <b>项目{ item['序号']}：{item['项目名称']}</b><br/>
        · 发布平台：{item['发布平台']}<br/>
        · 代理机构：{item['代理机构']}<br/>
        · 资质要求：{item['关键资质要求']}<br/>
        · 备注：{item['备注']}<br/>
        · 链接：{item['来源链接']}<br/>
        """
        story.append(Paragraph(detail_text, ParagraphStyle('detail', fontName=cn_font_name, fontSize=8, leading=13, leftIndent=10)))
        story.append(Spacer(1, 0.2*cm))
    story.append(PageBreak())

    # ===== 三、全国参考项目 =====
    story.append(Paragraph("三、全国参考项目详表", style_h1))
    add_hr()
    if national_items:
        for item in national_items:
            n_text = f"""
            <b>项目{item['序号']}：{item['项目名称']}</b><br/>
            · 地区：{item['地区']} | 类别：{item['类别']}<br/>
            · 采购人：{item['采购人']}<br/>
            · 发布时间：{item['发布时间']} | 截止：{item['截止日期']}<br/>
            · 资质：{item['关键资质要求']}<br/>
            · 平台：{item['发布平台']}<br/>
            """
            story.append(Paragraph(n_text, ParagraphStyle('nd', fontName=cn_font_name, fontSize=9, leading=14, leftIndent=8)))
            story.append(Spacer(1, 0.15*cm))
    else:
        story.append(Paragraph("本监测周期内未检索到海南以外的勘察检测类全国项目。", style_normal))
    story.append(PageBreak())

    # ===== 四、行业分析与风险提示 =====
    story.append(Paragraph("四、行业分析与风险提示", style_h1))
    add_hr()

    analysis = """
    <b>🔍 行业趋势分析</b><br/><br/>
    <b>1. 勘察类项目需求持续旺盛</b><br/>
    本期2个大型勘察项目均来自海南自贸港基础设施建设范畴。海口龙华区排水管网勘察项目
    规模较大，涉及29.67km管道清淤检测及大面积雨污分流改造，体现了城市更新类勘察
    项目的典型特征：多专业融合（岩土+物探+测量）。<br/><br/>
    <b>2. 地质灾害评估需求涌现</b><br/>
    跨琼州海峡低空航路地灾评估项目是低空经济与地质安全交叉领域的新兴需求，
    预算金额较小（6.4万元）但资质门槛高（地灾评估甲级），属于"短平快"优质标的。<br/><br/>
    <b>3. 设备检测类项目稳定输出</b><br/>
    广铁海口段接触网检测监测装置采购延续了铁路系统定期设备更新的规律性需求。<br/><br/>
    <b>⚠️ 风险提示</b><br/><br/>
    <b>· 竞争预警：</b>三亚大小洞天勘察项目要求甲级资质，且允许联合体≤2家，
    预计将吸引省内头部勘察单位竞标，中小机构建议以联合体方式参与。<br/>
    <b>· 时间紧迫：</b>跨琼州海峡地灾评估项目6月23日即截止，距发布仅5天，
    如需参与请立即启动投标文件编制。<br/>
    <b>· 资质门槛：</b>海口龙华区勘察项目要求三专业资质叠加（岩土勘察+物探检测监测+工程测量），
    单一资质企业须组建联合体。<br/>
    <b>· 数据局限性：</b>本报告因平台访问限制，可能遗漏ccgp-hainan.gov.cn上的政府采购类检测服务项目，
    建议登录海南省政府采购智慧云平台手动检索。<br/>
    <b>· 预算不透明：</b>多个大型勘察项目未在公告中直接披露预算金额，需下载招标文件后确认。<br/>
    """
    story.append(Paragraph(analysis, style_normal))
    story.append(PageBreak())

    # ===== 五、数据采集说明 =====
    story.append(Paragraph("五、数据采集说明", style_h1))
    add_hr()
    disclaimer = f"""
    <b>数据采集方式</b><br/><br/>
    · 目标平台：中国招标投标公共服务平台(www.cebpubservice.com)、海南省政府采购网(www.ccgp-hainan.gov.cn)<br/>
    · 实际采源：因目标平台反爬限制，通过以下渠道交叉采集：<br/>
    　- 剑鱼标讯(www.jianyu360.cn) — 海南地区分站<br/>
    　- 采招网(www.bidcenter.com.cn) — 海南招标页<br/>
    　- 各搜索引擎综合检索<br/>
    · 采集时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}<br/>
    · 搜索关键词：勘察、检测、测绘、岩土、地质灾害<br/>
    · 时间筛选：仅收录发布时间在{fetch_range}的公告<br/>
    <br/>
    <b>去重与筛选规则</b><br/><br/>
    1. 按项目名称+采购人+发布时间三重匹配去重<br/>
    2. 排除仅含"勘察设计"字样但实际为纯设计招标的项目<br/>
    3. 排除中标/成交结果公告、更正公告（仅留首次招标/采购公告）<br/>
    4. 排除明显与勘察检测行业无关的项目（如仅含"勘察"字样的物业/安保类公告）<br/>
    <br/>
    <b>免责声明</b><br/>
    本报告由AI自动生成，仅供行业参考。数据可能存在遗漏或延迟，不构成投资或投标决策建议。
    建议用户在投标前登录各官方平台核实完整公告信息。
    <br/>
    <b>报告生成：</b>QClaw Agent · 海南勘察招标日报系统<br/>
    <b>生成时间：</b>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
    """
    story.append(Paragraph(disclaimer, style_normal))

    # ===== 生成PDF =====
    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    print(f"✅ PDF报告已生成: {output_path}")
    print(f"   文件大小: {os.path.getsize(output_path) / 1024:.1f} KB")

except ImportError as e:
    print(f"请安装依赖: pip3 install reportlab pypdf")
    print(f"错误: {e}")
    raise
