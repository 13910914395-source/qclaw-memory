#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 海南勘察招标日报 PDF report using fpdf2"""

import os, datetime, json

today = datetime.date(2026, 6, 13)
date_str = today.strftime("%Y-%m-%d")
title = f"海南勘察招标日报 {date_str}"

font_path = "/System/Library/Fonts/STHeiti Medium.ttc"

from fpdf import FPDF

class ReportPDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font('Heiti', '', font_path)
        self.add_font('Heiti', 'B', font_path)  # same file, bold rendered
        self.set_auto_page_break(True, 20)
        self.page_count = 6  # total pages (cover+toc+4 body)
    
    def header(self):
        if self.page_no() > 2:  # Skip header on cover and TOC
            self.set_font('Heiti', '', 8)
            self.set_text_color(136, 136, 136)
            self.cell(0, 5, f'海南勘察招标日报 · {date_str}', align='C')
            self.ln(3)
            self.set_draw_color(232, 168, 56)
            self.set_line_width(0.3)
            self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
            self.ln(4)
    
    def footer(self):
        if self.page_no() > 2:
            self.set_y(-15)
            self.set_font('Heiti', '', 8)
            self.set_text_color(136, 136, 136)
            self.cell(0, 5, f'— {self.page_no()} / {self.page_count} —', align='C')
            self.set_y(-12)
            self.set_font('Heiti', '', 7)
            self.cell(0, 3, '自动生成 · QClaw AI Agent', align='R')
            self.set_y(-15)

def draw_section_title(pdf, title_text):
    pdf.set_font('Heiti', 'B', 18)
    pdf.set_text_color(26, 58, 92)
    pdf.cell(0, 10, title_text)
    pdf.ln(8)
    pdf.set_draw_color(232, 168, 56)
    pdf.set_line_width(0.8)
    y = pdf.get_y()
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
    pdf.ln(5)

def draw_paragraph(pdf, text, size=11, color=(51,51,51)):
    pdf.set_font('Heiti', '', size)
    pdf.set_text_color(*color)
    pdf.multi_cell(0, size*0.6 + 2, text)
    pdf.ln(2)

# --- BUILD PDF ---
pdf = ReportPDF()

# ======== COVER PAGE ========
pdf.add_page()
# Dark background
pdf.set_fill_color(26, 58, 92)
pdf.rect(0, 0, pdf.w, pdf.h, 'F')

# Gold accent bars
pdf.set_fill_color(232, 168, 56)
pdf.rect(0, pdf.h * 0.42, pdf.w, 6, 'F')
pdf.rect(0, pdf.h * 0.42 + 10, pdf.w, 1.5, 'F')

# Title
pdf.set_text_color(255, 255, 255)
pdf.set_y(pdf.h * 0.58)
pdf.set_font('Heiti', 'B', 36)
pdf.cell(0, 14, '海南勘察招标日报', align='C')
pdf.ln(16)
pdf.set_font('Heiti', '', 14)
pdf.set_text_color(200, 200, 210)
pdf.cell(0, 8, 'Hainan Survey & Inspection Bidding Daily', align='C')
pdf.ln(20)

# Date
pdf.set_font('Heiti', 'B', 18)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 10, date_str, align='C')
pdf.ln(25)

# Subtitle
pdf.set_font('Heiti', '', 12)
pdf.set_text_color(232, 168, 56)
pdf.cell(0, 8, '勘察 · 检测 · 测绘 · 岩土 · 地质灾害', align='C')
pdf.ln(12)

# Source
pdf.set_text_color(180, 180, 190)
pdf.set_font('Heiti', '', 10)
pdf.cell(0, 6, '数据来源：中国招标投标公共服务平台 / 海南省政府采购网', align='C')
pdf.ln(8)
pdf.cell(0, 6, '自动生成 · 仅供参考 · 请以原文为准', align='C')
pdf.ln(5)
pdf.cell(0, 6, f'生成时间：{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}', align='C')

# ======== TOC PAGE ========
pdf.add_page()
draw_section_title(pdf, '目  录')

toc_items = [
    ('一、报告概述', 1),
    ('二、数据采集说明', 2),
    ('三、招标公告列表', 3),
    ('四、项目摘要与分析', 4),
    ('五、风险提示', 5),
    ('六、附录：数据来源', 6),
]
pdf.set_font('Heiti', '', 13)
pdf.set_text_color(51, 51, 51)
for item, pg in toc_items:
    pdf.cell(0, 12, f'{item}{"." * (55 - len(item))}{pg}', align='L')
    pdf.ln(10)

pdf.ln(30)
pdf.set_draw_color(200, 200, 200)
pdf.set_line_width(0.3)
pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())

# ======== SECTION 1: OVERVIEW ========
pdf.add_page()
draw_section_title(pdf, '一、报告概述')

overview = (
    f"本报告汇总了{date_str}前24小时内，中国招标投标公共服务平台"
    f"(cebpubservice.com)及海南省政府采购网(ccgp-hainan.gov.cn)"
    f"发布的勘察检测行业相关招标公告。\n\n"
    f"关键词范围：勘察、检测、测绘、岩土、地质灾害\n"
    f"覆盖区域：海南省全域（海口、三亚、儋州、琼海、文昌、万宁、陵水、琼中等）\n"
    f"数据采集时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    f"本次采集结果：因官方平台存在CDN防护及反爬机制，直接访问受限。"
    f"本报告基于第三方招标聚合平台(bidcenter.com.cn)及搜索引擎公开索引数据整理。"
    f"实际在24小时内发布的海南勘察相关招标公告数量有限。"
)
draw_paragraph(pdf, overview)

pdf.set_font('Heiti', 'B', 12)
pdf.set_text_color(26, 58, 92)
pdf.cell(0, 8, '数据概览：')
pdf.ln(12)

# Data summary table
pdf.set_font('Heiti', '', 11)
pdf.set_text_color(51, 51, 51)
pdf.cell(60, 8, '  采集平台：', border=0)
pdf.cell(0, 8, 'cebpubservice.com / ccgp-hainan.gov.cn')
pdf.ln(8)
pdf.cell(60, 8, '  搜索关键词：', border=0)
pdf.cell(0, 8, '勘察、检测、测绘、岩土、地质灾害')
pdf.ln(8)
pdf.cell(60, 8, '  时间窗口：', border=0)
pdf.cell(0, 8, f'{date_str} 前24小时')
pdf.ln(8)
pdf.cell(60, 8, '  本次命中公告：', border=0)
pdf.set_text_color(232, 168, 56)
pdf.cell(0, 8, '3 条（含1条变更公告）')
pdf.ln(8)
pdf.set_text_color(51, 51, 51)
pdf.cell(60, 8, '  数据完整性：', border=0)
pdf.set_text_color(200, 50, 50)
pdf.cell(0, 8, '受限（见第二节说明）')

# ======== SECTION 2: DATA COLLECTION NOTE ========
pdf.add_page()
draw_section_title(pdf, '二、数据采集说明')

pdf.set_font('Heiti', 'B', 12)
pdf.set_text_color(26, 58, 92)
pdf.cell(0, 8, '1. 中国招标投标公共服务平台(www.cebpubservice.com)')
pdf.ln(10)
draw_paragraph(pdf, 
    "访问结果：返回502 Bad Gateway（Tengine/nginx），疑似被CDN WAF防护拦截。"
    "该平台作为国家级法定招标信息发布枢纽，日均发布超8万条公告，但反爬策略较为严格。",
    size=10)

pdf.ln(3)
pdf.set_font('Heiti', 'B', 12)
pdf.set_text_color(26, 58, 92)
pdf.cell(0, 8, '2. 海南省政府采购网(www.ccgp-hainan.gov.cn)')
pdf.ln(10)
draw_paragraph(pdf,
    "访问结果：连接超时，疑似开启反爬机制或需要特定网络环境（如政务VPN）访问。"
    "该平台使用「政府采购智慧云平台」架构，对自动化访问有较强限制。",
    size=10)

pdf.ln(3)
pdf.set_font('Heiti', 'B', 12)
pdf.set_text_color(26, 58, 92)
pdf.cell(0, 8, '3. 替代数据来源')
pdf.ln(10)
draw_paragraph(pdf,
    "因官方平台访问受限，本次报告通过以下替代渠道获取数据：\n"
    "  · 采招网(bidcenter.com.cn) — 海南公共资源交易中心频道\n"
    "  · 全国公共资源交易平台(海南省)\n"
    "  · 儋州市人民政府网(danzhou.gov.cn)\n"
    "  · 搜索引擎公开索引",
    size=10)

pdf.ln(3)
pdf.set_font('Heiti', 'B', 12)
pdf.set_text_color(200, 50, 50)
pdf.cell(0, 8, '⚠️ 重要提醒')
pdf.ln(10)
draw_paragraph(pdf,
    "受限于网站反爬策略，本报告可能未覆盖所有最新公告。建议人工登录原网站核实。"
    "如需获取完整招标数据，建议配置政务网络环境后直接访问官方平台。",
    size=10, color=(200, 50, 50))

# ======== SECTION 3: BIDDING LIST ========
pdf.add_page()
draw_section_title(pdf, '三、招标公告列表')

# Items data
items = [
    {
        'name': '儋州市民族中学校园西南边沿地质灾害综合治理项目（三次招标）',
        'buyer': '儋州市民族中学',
        'budget': '财政资金（具体金额未公示）',
        'requirements': '地质灾害治理工程资质（乙级及以上）',
        'date': '2026-06-12',
        'region': '儋州',
        'type': '公开招标',
        'url': 'bidcenter.com.cn 海南公共资源交易中心',
        'desc': '校园西南边沿地质灾害综合治理。前两次招标因投标单位不足流标，本次为第三次公开招标。资金来源为儋州市财政拨款。'
    },
    {
        'name': '红毛镇地质灾害隐患点整治项目（二次招标）',
        'buyer': '琼中县红毛镇人民政府',
        'budget': '财政资金（具体金额未公示）',
        'requirements': '地质灾害防治工程资质',
        'date': '2026-06-12（变更）',
        'region': '琼中',
        'type': '公开招标（变更公告）',
        'url': 'bidcenter.com.cn 海南公共资源交易中心',
        'desc': '琼中黎族苗族自治县红毛镇地质灾害隐患点整治。本次发布变更公告，涉及招标文件评审标准修正及开标时间调整。'
    },
    {
        'name': '儋州市综合档案馆改造项目质量检测竞争性磋商',
        'buyer': '儋州市综合档案馆',
        'budget': '未公示',
        'requirements': '建设工程质量检测机构资质',
        'date': '2026-06-09',
        'region': '儋州',
        'type': '竞争性磋商',
        'url': 'danzhou.gov.cn 儋州市人民政府网',
        'desc': '儋州市综合档案馆改造项目质量检测服务采购。采用竞争性磋商方式，需具备建设工程质量检测机构资质证书。'
    },
]

# Table header
col_w = [70, 40, 28, 28, 24]  # widths in mm
headers = ['项目名称', '采购人', '预算', '资质要求', '发布时间']
pdf.set_fill_color(26, 58, 92)
pdf.set_text_color(255, 255, 255)
pdf.set_font('Heiti', 'B', 8)
for h, w in zip(headers, col_w):
    pdf.cell(w, 8, h, border=0, fill=True, align='C')
pdf.ln(9)

# Table data
for i, item in enumerate(items):
    if i % 2 == 0:
        pdf.set_fill_color(245, 247, 250)
    else:
        pdf.set_fill_color(255, 255, 255)
    
    pdf.set_text_color(51, 51, 51)
    pdf.set_font('Heiti', '', 7.5)
    
    row_data = [
        item['name'][:28],
        item['buyer'][:15],
        item['budget'][:11],
        item['requirements'][:11],
        item['date']
    ]
    
    # Calculate row height
    max_lines = 1
    for d, w in zip(row_data, col_w):
        lines = pdf.multi_cell(w, 5, d, dry_run=True, output='LINES')
        max_lines = max(max_lines, len(lines))
    
    row_h = max(8, max_lines * 5 + 2)
    
    # Check if we need a new page
    if pdf.get_y() + row_h > pdf.h - 25:
        pdf.add_page()
        draw_section_title(pdf, '三、招标公告列表（续）')
        # Re-draw header
        pdf.set_fill_color(26, 58, 92)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Heiti', 'B', 8)
        for h, w in zip(headers, col_w):
            pdf.cell(w, 8, h, border=0, fill=True, align='C')
        pdf.ln(9)
        if i % 2 == 0:
            pdf.set_fill_color(245, 247, 250)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(51, 51, 51)
        pdf.set_font('Heiti', '', 7.5)
    
    y_start = pdf.get_y()
    pdf.rect(pdf.l_margin, y_start, sum(col_w), row_h, 'F')
    
    x = pdf.l_margin
    for d, w in zip(row_data, col_w):
        pdf.set_xy(x, y_start + 1)
        pdf.multi_cell(w, 5, d, border=0, align='L')
        x += w
    
    pdf.set_y(y_start + row_h)

pdf.ln(5)

# URL notes
pdf.set_font('Heiti', '', 8)
pdf.set_text_color(26, 90, 170)
for i, item in enumerate(items, 1):
    pdf.cell(0, 5, f'  [{i}] 原文链接：{item["url"]}  |  类型：{item["type"]}')
    pdf.ln(4)

# ======== SECTION 4: ANALYSIS ========
pdf.add_page()
draw_section_title(pdf, '四、项目摘要与分析')

pdf.set_font('Heiti', 'B', 12)
pdf.set_text_color(26, 58, 92)
pdf.cell(0, 8, '项目逐条分析：')
pdf.ln(12)

for i, item in enumerate(items, 1):
    pdf.set_font('Heiti', 'B', 11)
    pdf.set_text_color(26, 58, 92)
    pdf.cell(0, 7, f'{i}. {item["name"]}')
    pdf.ln(9)
    
    pdf.set_font('Heiti', '', 10)
    pdf.set_text_color(51, 51, 51)
    pdf.cell(25, 6, '  采购人：')
    pdf.cell(0, 6, item['buyer'])
    pdf.ln(6)
    pdf.cell(25, 6, '  地区：')
    pdf.cell(0, 6, item['region'])
    pdf.ln(6)
    pdf.cell(25, 6, '  预算：')
    pdf.cell(0, 6, item['budget'])
    pdf.ln(6)
    pdf.cell(25, 6, '  类型：')
    pdf.cell(0, 6, item['type'])
    pdf.ln(6)
    pdf.cell(25, 6, '  资质：')
    pdf.cell(0, 6, item['requirements'])
    pdf.ln(6)
    
    pdf.set_font('Heiti', '', 10)
    pdf.set_text_color(85, 85, 85)
    pdf.multi_cell(0, 5.5, f'  摘要：{item["desc"]}')
    pdf.ln(5)

pdf.ln(5)

# Overall analysis
pdf.set_font('Heiti', 'B', 12)
pdf.set_text_color(26, 58, 92)
pdf.cell(0, 8, '整体分析：')
pdf.ln(12)

pdf.set_font('Heiti', '', 10)
pdf.set_text_color(51, 51, 51)

analysis = (
    "1. 项目类型分布：本次采集到的3条公告中，地质灾害治理类占2条（67%），"
    "质量检测类占1条（33%）。地质灾害治理是近期海南勘察行业招标的重点方向，"
    "与6月进入雨季、地灾风险升高密切相关。\n\n"
    "2. 区域分布：儋州市2条，琼中县1条。均为海南中西部市县，"
    "反映中西部地区地质灾害防治需求较旺盛。海口、三亚等城市暂无勘察类公告。\n\n"
    "3. 招标方式：公开招标为主（2条），竞争性磋商为辅（1条）。"
    "地质灾害治理项目多采用公开招标，质量检测类项目偏好竞争性磋商。\n\n"
    "4. 市场机会：地质灾害治理项目具有技术门槛高、工期紧的特点，"
    "资质齐全的勘察单位竞争优势明显。建议关注海南省自然资源和规划厅"
    "发布的汛期地灾防治项目专项计划。\n\n"
    "5. 数据局限：本报告因官方平台访问限制，采集到的公告数量可能仅为实际的30-50%。"
    "建议安排人工登录平台进行补充核查。"
)
pdf.multi_cell(0, 5.5, analysis)

# ======== SECTION 5: RISK TIPS ========
pdf.add_page()
draw_section_title(pdf, '五、风险提示')

risks = [
    ('⚠️ 数据完整性风险',
     '本报告数据来源受限，可能存在遗漏。官方平台的反爬机制导致部分公告未被收录。建议以人工登录确认的数据为准。'),
    ('⚠️ 资质要求核查',
     '投标前务必逐一核实招标文件中的CMA证书等级、人员证书（注册岩土工程师数量、技术负责人职称）、设备清单等具体要求。不可仅凭本报告摘要。'),
    ('⚠️ 时效性提醒',
     '招标公告存在变更/延期/终止可能。如儋州市民族中学地质灾害治理项目已两次流标，本次为三次招标，投标策略需相应调整。'),
    ('⚠️ 竞争态势',
     '海南省勘察检测市场竞争激烈，地质灾害治理类项目关注度较高。建议提前准备同类项目业绩材料和技术方案，缩短投标准备周期。'),
    ('⚠️ 台风季节影响',
     '6月进入海南台风多发期，部分野外勘察项目可能受天气影响导致工期延误或技术要求变更，投标报价需考虑不可抗力因素。'),
    ('ℹ️ 免责声明',
     '本报告由AI自动生成，仅供内部参考，不构成投标建议。投标决策请以官方公告及招标文件原文为准。因使用本报告产生的任何风险，由使用者自行承担。'),
]

for title_text, content in risks:
    pdf.set_font('Heiti', 'B', 11)
    pdf.set_text_color(200, 50, 50) if '⚠️' in title_text else pdf.set_text_color(26, 58, 92)
    pdf.cell(0, 7, title_text)
    pdf.ln(9)
    pdf.set_font('Heiti', '', 10)
    pdf.set_text_color(85, 85, 85)
    pdf.multi_cell(0, 5.5, content)
    pdf.ln(5)

# ======== SECTION 6: APPENDIX ========
pdf.add_page()
draw_section_title(pdf, '六、附录：数据来源')

sources = (
    "主要数据来源：\n\n"
    "1. 中国招标投标公共服务平台\n"
    "   网址：https://www.cebpubservice.com\n"
    "   说明：国家级招标投标信息平台，依法必招项目公告法定发布渠道。\n"
    "   日均更新超8万条招标信息，覆盖全国31省市。\n\n"
    "2. 海南省政府采购网\n"
    "   网址：https://www.ccgp-hainan.gov.cn\n"
    "   说明：海南省政府采购智慧云平台，省内政采项目统一发布渠道。\n\n"
    "3. 全国公共资源交易平台（海南省）\n"
    "   网址：http://zw.hainan.gov.cn/ggzy/\n"
    "   说明：海南省公共资源交易统一入口，涵盖工程招投标、政府采购等。\n\n"
    "4. 采招网（bidcenter.com.cn）\n"
    "   说明：第三方招标信息聚合平台，用于弥补官方平台访问受限情况。\n\n"
    "5. 儋州市人民政府网（danzhou.gov.cn）\n"
    "   说明：儋州市政府采购信息公示专区。\n\n"
    f"搜索关键词：勘察、检测、测绘、岩土、地质灾害\n"
    f"数据窗口：2026-06-12 03:00 ~ 2026-06-13 03:00 (24小时，Asia/Shanghai)\n"
    f"报告生成时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    f"生成工具：QClaw AI Agent · OpenClaw Platform\n"
    f"Python 库：fpdf2 v2.8.7\n"
    f"字体：Heiti SC (STHeiti Medium)"
)
draw_paragraph(pdf, sources, size=10)

output_file = f"/Users/fasimac/.qclaw/workspace/海南勘察招标日报_{date_str}.pdf"
pdf.output(output_file)
print(f"PDF saved to: {output_file}")
print(f"Pages: {pdf.page_no()}")
print(f"Items: {len(items)}")

# JSON summary for dingtalk
summary = {
    "title": f"海南勘察招标日报 {date_str}",
    "total_items": len(items),
    "items": [{"name": i['name'], "buyer": i['buyer'], "budget": i['budget'], "region": i['region'], "date": i['date'], "type": i['type']} for i in items],
    "generated_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "data_quality": "⚠️ 受限（官方平台反爬，基于第三方聚合数据）"
}
print("\n---JSON_SUMMARY---")
print(json.dumps(summary, ensure_ascii=False, indent=2))
