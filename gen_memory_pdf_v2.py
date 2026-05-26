# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.expanduser('~'),
    'Library/Application Support/QClaw/openclaw/config/skills/pdf/scripts'))
from setup_chinese_pdf import setup_chinese_pdf

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, PageBreak, HRFlowable)
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

cn_font, styles = setup_chinese_pdf()

# Color palette
BLUE_DARK   = colors.HexColor('#1A3A5C')
BLUE_MID    = colors.HexColor('#2E6DA4')
BLUE_LIGHT  = colors.HexColor('#D6E8F7')
GREEN_DARK  = colors.HexColor('#1C6B3A')
GREEN_LIGHT = colors.HexColor('#D5F0E0')
ORANGE_DARK = colors.HexColor('#C45C00')
ORANGE_LIGHT= colors.HexColor('#FFF0D6')
PURPLE_DARK = colors.HexColor('#5B2D8E')
PURPLE_LIGHT= colors.HexColor('#EDE0F5')
TEAL_DARK   = colors.HexColor('#0E7B7B')
TEAL_LIGHT  = colors.HexColor('#D0F0F0')
YELLOW_DARK = colors.HexColor('#8B6914')
YELLOW_LIGHT= colors.HexColor('#FFF9E0')
WHITE       = colors.white
GRAY_TEXT   = colors.HexColor('#555555')
LIGHT_GRAY  = colors.HexColor('#F5F5F5')
PINK_DARK   = colors.HexColor('#C0185A')
PINK_LIGHT  = colors.HexColor('#FFE0EE')

W, H = A4

# Larger font sizes for student version
FS_TITLE   = 22   # was 14
FS_H2      = 13   # was 11
FS_BODY    = 12   # was 10.5
FS_BULLET  = 12   # was 10.5
FS_SMALL   = 11   # was 9.5
FS_TINY    = 10   # was 9

def S(name, parent='Normal', **kw):
    return ParagraphStyle(name, parent=styles[parent], fontName=cn_font, **kw)

def sp(h=8):
    return Spacer(1, h)

def hr_line(color=BLUE_MID, thickness=0.5):
    return HRFlowable(width='100%', thickness=thickness, color=color, spaceAfter=8)

def section_banner(text, bg=BLUE_MID):
    tbl = Table([[Paragraph(text, S('SecT','Normal',fontSize=FS_TITLE,leading=26,textColor=WHITE))]],
                colWidths=[W - 4*cm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),
        ('TOPPADDING',(0,0),(-1,-1),12),
        ('BOTTOMPADDING',(0,0),(-1,-1),12),
        ('LEFTPADDING',(0,0),(-1,-1),18),
    ]))
    return tbl

def colored_box(rows, bg=BLUE_LIGHT, border=BLUE_MID):
    tbl = Table([[r] for r in rows], colWidths=[W - 4*cm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),
        ('TOPPADDING',(0,0),(-1,-1),10),
        ('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',(0,0),(-1,-1),16),
        ('RIGHTPADDING',(0,0),(-1,-1),16),
        ('BOX',(0,0),(-1,-1),2,border),
    ]))
    return tbl

def highlight_bar(text, bg=PURPLE_DARK, fg=WHITE):
    tbl = Table([[Paragraph(text, S('HB','Normal',fontSize=FS_H2,leading=18,
                                   textColor=fg,bold=1,alignment=TA_CENTER))]],
                colWidths=[W - 4*cm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),
        ('TOPPADDING',(0,0),(-1,-1),12),
        ('BOTTOMPADDING',(0,0),(-1,-1),12),
    ]))
    return tbl

def on_page(canvas_obj, doc):
    cnv = canvas_obj
    cnv.saveState()
    cnv.setFillColor(BLUE_DARK)
    cnv.rect(0, H - 18, W, 18, fill=1, stroke=0)
    cnv.setFillColor(WHITE)
    cnv.setFont(cn_font, 9)
    cnv.drawString(2*cm, H - 12, '\u8bf7\u5b66\u751f\u5b66\u4e60\u65b9\u6cd5\u6307\u5357 \u00b7 2026')
    cnv.drawRightString(W - 2*cm, H - 12, f'\u7b2c {doc.page} \u9875')
    cnv.setFillColor(LIGHT_GRAY)
    cnv.rect(0, 0, W, 20, fill=1, stroke=0)
    cnv.setFillColor(GRAY_TEXT)
    cnv.setFont(cn_font, 8)
    cnv.drawCentredString(W/2, 6, '\u7ed9\u521d\u4e8c\u7537\u751f\u7684\u5927\u8111\u4f53\u9ad8\u5206\u6307\u5357')
    cnv.restoreState()

# ── Cover ──────────────────────────────────────────────────────
def build_cover():
    elems = []

    # Title banner
    t = Table([
        [Paragraph('\U0001f31f  \u521d\u4e8c\u7537\u751f\u5927\u8111\u4f53\u9ad8\u5206\u6307\u5357',
                   S('C1','Normal',fontSize=24,leading=30,textColor=WHITE,alignment=TA_CENTER))],
        [Paragraph('\u8ba9\u5b66\u4e60\u66f4\u9ad8\u6548\uff0c\u8ba9\u8bb0\u5fc6\u66f4\u6e05\u6670',
                   S('C2','Normal',fontSize=15,leading=20,textColor=colors.HexColor('#A8D0F0'),alignment=TA_CENTER))],
    ], colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),BLUE_DARK),
        ('TOPPADDING',(0,0),(-1,-1),28),
        ('BOTTOMPADDING',(0,0),(-1,-1),28),
    ]))
    elems.append(t)
    elems.append(sp(14))

    # Encouragement message
    elems.append(highlight_bar('\U0001f4af \u4f60\u7684\u5927\u8111\u672c\u6765\u5c31\u5f88\u5f3a\uff01\u8fd9\u4e9b\u65b9\u6cd5\u8ba9\u4f60\u66f4\u66f4\u5668',
                                bg=GREEN_DARK))
    elems.append(sp(12))

    # 4 cards
    cards = [
        (BLUE_MID,   '\U0001f634', '\u7761\u7720\u662f\u7b2c\u4e00\u529f\u7387',
         '\u9ad8\u8d28\u91cf\u7761\u7720\u8ba9\u4f60\u7684\u5927\u8111\u66f4\u6e05\u6670\n\u6bcf\u5929\u5b9d\u8fd1 22:00 \u5165\u7761'),
        (ORANGE_DARK,'\U0001f3c3', '\u8fd0\u52a8\u8ba9\u4f60\u66f4\u806a\u660e',
         '\u6bcf\u5929 15 \u5206\u949f\u8fd0\u52a8\uff0c\u8fd0\u52a8\u540e\u5b66\u4e60\u6548\u7387\u66f4\u9ad8\n\u6709\u8da3\u7684\u8fd0\u52a8\u8ba9\u4f60\u66f4\u6709\u7cbe\u529b'),
        (TEAL_DARK,  '\U0001f9e0', '\u56fe\u50cf\u8bb0\u5fc6\u66f4\u6709\u6548',
         '\u628a\u77e5\u8bc6\u53d8\u6210\u56fe\u7247\u548c\u6545\u4e8b\uff0c\u6fc0\u6d3b\u4f60\u7684\u7a7a\u95f4\u60f3\u8c61\u529b\n\u8fd9\u662f\u6700\u9002\u5408\u7537\u5b69\u7684\u8bb0\u5fc6\u65b9\u5f0f'),
        (PURPLE_DARK,'\U0001f957', '\u8425\u517b\u7ed9\u4f60\u52a0\u6cb9',
         '\u6bcf\u5929\u8865\u5145\u7ef4\u751f\u7d20 D\uff0c\u9c7c\u7b49\u7b49\u3001\u9c7c\u86c7\n\u5065\u5eb7\u7684\u996e\u98df\u8ba9\u4f60\u7b11\u5f97\u66f4\u7b26'),
    ]
    cw = (W - 4*cm) / 4 - 4
    card_data = [[Paragraph(f'<b>{ic}</b><br/><font size="13">{ti}</font><br/><font size="11">{de}</font>',
                             S(f'CD{i}','Normal',fontSize=12,leading=15,
                               textColor=WHITE,alignment=TA_CENTER))]
                  for i,(color,ic,ti,de) in enumerate(cards)]
    ct = Table([card_data], colWidths=[cw]*4, rowHeights=[110])
    for i2,(color,_,_,_) in enumerate(cards):
        ct.setStyle(TableStyle([
            ('BACKGROUND',(i2,0),(i2,0),color),
            ('TOPPADDING',(i2,0),(i2,0),12),
            ('BOTTOMPADDING',(i2,0),(i2,0),12),
            ('LEFTPADDING',(i2,0),(i2,0),6),
            ('RIGHTPADDING',(i2,0),(i2,0),6),
            ('BOX',(i2,0),(i2,0),0.5,WHITE),
        ]))
    elems.append(ct)
    elems.append(sp(14))
    elems.append(hr_line(BLUE_LIGHT, 1))
    elems.append(sp(8))
    elems.append(Paragraph(f'\U0001f4c5 \u5236\u5b9a\u65e5\u671f\uff1a2026\u5e744\u670812\u65e5 \u00b7 \u7537\u5b69\u5b50\u7248',
                            S('DT','Normal',fontSize=11,textColor=GRAY_TEXT,alignment=TA_CENTER)))
    elems.append(PageBreak())
    return elems

# ── Section 1: 睡眠 ─────────────────────────────────────────────
def build_section1():
    elems = []
    elems.append(section_banner('\u4e00\u3001\u9ad8\u8d28\u91cf\u7761\u7720 \u2014 \u5927\u8111\u7684\u7b2c\u4e00\u529f\u7387',BLUE_MID))
    elems.append(sp(12))

    elems.append(colored_box([
        Paragraph('\U0001f4a4 \u6700\u91cd\u8981\u7684\u4e00\u70b9',
                  S('S1T','Normal',fontSize=FS_H2,leading=18,textColor=BLUE_DARK,bold=1)),
        Spacer(1,4),
        Paragraph(
            '\u4f60\u7684\u5927\u8111\u6bcf\u5929\u9700\u8981\u5145\u8db3\u7684\u6df1\u5ea6\u7761\u7720\u6765\u5904\u7406\u548c\u5b58\u50a8\u4fe1\u606f\u3002'
            '\u6bcf\u5929\u7684\u5b66\u4e60\u5185\u5bb9\uff0c\u90fd\u9700\u8981\u5728\u6df1\u5ea6\u7761\u7720\u65f6\u88ab\u201c\u6392\u7406\u5e76\u5b58\u50a8\u201d\u8d77\u6765\u3002',
            S('S1B','Normal',fontSize=FS_BODY,leading=19,textColor=colors.HexColor('#2C2C2C'))),
    ], bg=BLUE_LIGHT, border=BLUE_MID))
    elems.append(sp(10))

    tips = [
        ('\U0001f319 \u6700\u597d\u5169\u70b9', '\u6bcf\u5929 22:00 \u524d\u5165\u7761\uff0c\u4fdd\u8bc1 8 \u5c0f\u65f6\u4ee5\u4e0a\u7684\u7761\u7720\u65f6\u95f4'),
        ('\U0001f4f4 \u7761\u524d\u51b3\u8bef\u533a', '\u7761\u524d 1 \u5c0f\u65f6\u4e0d\u8981\u73a9\u624b\u673a\u3001\u770b\u89c6\u9891\uff0c\u8ba9\u5927\u8111\u6162\u6162\u5165\u7761'),
        ('\U0001f4cd \u7761\u7720\u8bb0\u5fc6\u6cd5', '\u7761\u524d 10 \u5206\u949f\uff0c\u628a\u4eca\u5929\u5b66\u7684\u91cd\u70b9\u5185\u5bb9\u5411\u7238\u5988\u8bb2\u4e00\u904d\uff0c\u8bb0\u5fc6\u66f4\u6df1'),
        ('\U0001f4a1 \u665a\u4e0a\u514b\u5236', '\u4e0d\u8981\u5439\u96f7\u8981\u7a7a\u8fd0\u52a8\uff0c\u5149\u7b49\u4f1a\u5f71\u54cd\u7761\u7720\u8d28\u91cf'),
    ]
    for icon, (title, content) in enumerate(tips):
        icon_chr = '\U0001f319' if icon==0 else ('\U0001f4f4' if icon==1 else ('\U0001f4cd' if icon==2 else '\U0001f4a1'))
        tr = Table([[
            Paragraph(f'{icon_chr}', S(f'S1L{icon}','Normal',fontSize=16,textColor=BLUE_MID,alignment=TA_CENTER)),
            Paragraph(f'<b>{title}</b>\n{content}', S(f'S1C{icon}','Normal',fontSize=FS_BODY,leading=18,textColor=colors.HexColor('#2C2C2C'))),
        ]], colWidths=[1.5*cm, W - 6*cm])
        tr.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,-1),BLUE_LIGHT),
            ('TOPPADDING',(0,0),(-1,-1),10),
            ('BOTTOMPADDING',(0,0),(-1,-1),10),
            ('LEFTPADDING',(0,0),(0,0),8),
            ('LEFTPADDING',(1,0),(1,0),12),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('BOX',(0,0),(-1,-1),1,BLUE_MID),
        ]))
        elems.append(tr)
        elems.append(sp(6))

    elems.append(sp(4))
    elems.append(hr_line())
    return elems

# ── Section 2: 运动 ─────────────────────────────────────────────
def build_section2():
    elems = []
    elems.append(section_banner('\u4e8c\u3001\u8fd0\u52a8\u8ba9\u4f60\u66f4\u6709\u7cbe\u529b \u2014 \u5927\u8111\u7684\u52a8\u529b\u6fc0\u6d3b\u524d',ORANGE_DARK))
    elems.append(sp(12))

    elems.append(colored_box([
        Paragraph('\U0001f3c3\uff01\u8fd0\u52a8\u540e\u7684\u4f60\u66f4\u806a\u660e',
                  S('S2T','Normal',fontSize=FS_H2,leading=18,textColor=ORANGE_DARK,bold=1)),
        Spacer(1,4),
        Paragraph(
            '\u8fd0\u52a8\u4f1a\u8ba9\u4f60\u7684\u5927\u8111\u5206\u6ccc\u201c\u9b44\u7d2b\u7d20\u201d\uff0c\u8fd9\u79cd\u7269\u8d28\u80fd\u8ba9\u7b26\u5408\u5b66\u4e60\u7684\u795e\u7ecf\u5143\u8fdb\u884c\u66f4\u591a\u7684\u8fde\u63a5\u548c\u751f\u957f\u3002'
            '\u6240\u4ee5\u653e\u5b66\u540e\u505a\u70b9\u8fd0\u52a8\uff0c\u5b66\u4e60\u6548\u7387\u4f1a\u66f4\u9ad8\uff01',
            S('S2B','Normal',fontSize=FS_BODY,leading=19,textColor=colors.HexColor('#2C2C2C'))),
    ], bg=ORANGE_LIGHT, border=ORANGE_DARK))
    elems.append(sp(10))

    # Activity grid
    act_data = [
        ('\U0001f3c3', '\u8df3\u7ef3', '\u6bcf\u5929 5-10 \u5206\u949f\u53cc\u6447\u8df3\u7ef3', ORANGE_DARK),
        ('\U0001f6b4', '\u51b2\u523a\u8dd1', '\u53ef\u4ee5\u51b2\u523a\u4e0a\u697c\uff0c\u6216\u8005\u5230\u8f6f\u8fb0\u5730\u505a\u9ad8\u62ac\u817f\u8fd0\u52a8', ORANGE_DARK),
        ('\U0001f3cb', '\u8fb0\u7ad9\u7ec3\u4e60', '\u7ad9\u7ac9\u7ec3\u4e60\u80fd\u8ba9\u4f60\u7684\u6ce8\u610f\u529b\u66f4\u96c6\u4e2d\uff0c\u5b66\u4e60\u65f6\u66f4\u52a0\u5168\u795e', ORANGE_DARK),
        ('\U0001f3AE', '\u7b11\u8bdd\u7ec3', '\u548c\u670b\u53cb\u4e00\u8d77\u6253\u7b7e\uff0c\u65b9\u5f0f\u6709\u8da3\uff0c\u6bcf\u5468 2-3 \u6b21\u5c31\u591f\u4e86', ORANGE_DARK),
    ]
    cw2 = (W - 4*cm) / 2 - 5
    row1 = [[Paragraph(f'<b>{ic}</b><br/><font size="14">{ti}</font><br/><font size="11">{de}</font>',
                       S(f'A{i}','Normal',fontSize=11,leading=16,textColor=WHITE,alignment=TA_CENTER))]
             for i,(ic,ti,de,col) in enumerate(act_data[:2])]
    row2 = [[Paragraph(f'<b>{ic}</b><br/><font size="14">{ti}</font><br/><font size="11">{de}</font>',
                       S(f'A{i+2}','Normal',fontSize=11,leading=16,textColor=WHITE,alignment=TA_CENTER))]
             for i,(ic,ti,de,col) in enumerate(act_data[2:])]
    atbl = Table([row1, row2], colWidths=[cw2]*2, rowHeights=[95,95])
    for i2,(_,_,_,col) in enumerate(act_data):
        atbl.setStyle(TableStyle([
            ('BACKGROUND',(i2%2,i2//2),(i2%2,i2//2),ORANGE_DARK),
            ('TOPPADDING',(i2%2,i2//2),(i2%2,i2//2),12),
            ('BOTTOMPADDING',(i2%2,i2//2),(i2%2,i2//2),12),
            ('LEFTPADDING',(i2%2,i2//2),(i2%2,i2//2),8),
            ('RIGHTPADDING',(i2%2,i2//2),(i2%2,i2//2),8),
            ('BOX',(i2%2,i2//2),(i2%2,i2//2),0.5,WHITE),
        ]))
    elems.append(atbl)
    elems.append(sp(10))

    elems.append(colored_box([
        Paragraph('\u26a1 \u63d0\u793a\uff1a\u8fd0\u52a8\u540e\u534a\u5c0f\u65f6\u518d\u5f00\u59cb\u5b66\u4e60\uff0c\u6548\u7387\u6700\u9ad8\uff01',
                  S('S2W','Normal',fontSize=FS_BODY,leading=17,textColor=ORANGE_DARK,bold=1)),
    ], bg=YELLOW_LIGHT, border=YELLOW_DARK))

    elems.append(sp(4))
    elems.append(hr_line())
    return elems

# ── Section 3: 图像记忆 ─────────────────────────────────────────
def build_section3():
    elems = []
    elems.append(section_banner('\u4e09\u3001\u56fe\u50cf\u8bb0\u5fc6\u6cd5 \u2014 \u8ba9\u7b11\u8bdd\u548c\u56fe\u7247\u5e2e\u4f60\u8bb0\u5fc6',TEAL_DARK))
    elems.append(sp(12))

    elems.append(colored_box([
        Paragraph('\U0001f9e0 \u56fe\u50cf\u8bb0\u5fc6\u662f\u6700\u5f3a\u5927\u7684\u5b66\u4e60\u6b66\u5668',
                  S('S3T','Normal',fontSize=FS_H2,leading=18,textColor=TEAL_DARK,bold=1)),
        Spacer(1,4),
        Paragraph(
            '\u521d\u4e8c\u7684\u5185\u5bb9\u6bd5\u4e1a\u91cd\u4e8e\u7406\u89e3\uff0c\u7406\u89e3\u6bd5\u4e1a\u91cd\u4e8e\u5efa\u7acb\u8054\u7cfb\u3002'
            '\u628a\u77e5\u8bc6\u70b9\u53d8\u6210\u201c\u56fe\u7247\u201d\u6216\u201c\u6545\u4e8b\u201d\uff0c\u4f60\u7684\u5927\u8111\u4f1a\u7275\u624b\u5f88\u70ed\u60c5\u5730\u5e2e\u4f60\u8bb0\u4f4f\uff01',
            S('S3B','Normal',fontSize=FS_BODY,leading=19,textColor=colors.HexColor('#2C2C2C'))),
    ], bg=TEAL_LIGHT, border=TEAL_DARK))
    elems.append(sp(10))

    methods = [
        ('\U0001f3db', '\u5386\u53f2\u516d\u9898', [
            '\u628a\u6bcf\u4e2a\u5386\u53f2\u4e8b\u4ef6\u60f3\u8c61\u6210\u4e00\u4e2a\u5c0f\u52a8\u753b\u6216\u6545\u4e8b',
            '\u51fa\u73b0\u4e86\u4e00\u4e2a\u6709\u8da3\u7684\u60c5\u8282\uff0c\u4f60\u5c31\u4e0d\u4f1a\u5fd8\u8bb0',
            '\u53ef\u4ee5\u7528\u4e50\u9ad8\u5c0f\u4eba\uff0c\u6c34\u7b14\uff0c\u751f\u52a8\u7684\u56fe\u50cf\u6fc0\u6d3b\u8bb0\u5fc6',
        ]),
        ('\U0001f30d', '\u5730\u7406\u5730\u5f62', [
            '\u95ed\u4e0a\u773c\u775b\uff0c\u60f3\u8c61\u4f60\u5728\u4e00\u67f1\u98de\u673a\u4e0a\u4f9d\u6b21\u770b\u5730\u56fe',
            '\u7528\u624b\u6307\u5728\u7a7a\u4e2d\u6c14\u52a8\u5730\u753b\u51fa\u5c71\u8109\u3001\u6cb3\u6d41\u548c\u57ce\u5e02',
            '\u8fd9\u79cd\u201c\u624b\u52a8\u5927\u8111\u201d\u7684\u65b9\u5f0f\u5b66\u5730\u7406\u7279\u522b\u6709\u6548',
        ]),
        ('\U0001f4d6', '\u82f1\u8bed\u5355\u8bcd', [
            '\u6bcf\u4e2a\u5355\u8bcd\u90fd\u662f\u4e00\u4e2a\u56fe\u7247\u6545\u4e8b',
            '\u6d4b\u8bd5\uff1a\u770b\u56fe\u7247\u8bf4\u51fa\u82f1\u8bed\uff0c\u6bd4\u6b7b\u8bb0\u786e\u5b9e\u6709\u6548\u5f88\u591a',
        ]),
    ]

    for mi, (icon, title, pts) in enumerate(methods):
        elems.append(highlight_bar(f'{icon}  {title}', bg=TEAL_DARK, fg=WHITE))
        for pt in pts:
            elems.append(Paragraph(f'<b>\u25b8</b>  {pt}',
                                    S(f'S3P{mi}','Normal',fontSize=FS_BULLET,leading=18,
                                      textColor=colors.HexColor('#2C2C2C'),leftIndent=12,spaceAfter=4)))
        elems.append(sp(8))

    elems.append(sp(4))
    elems.append(hr_line())
    return elems

# ── Section 4: 营养 ─────────────────────────────────────────────
def build_section4():
    elems = []
    elems.append(section_banner('\u56db\u3001\u5065\u5eb7\u8425\u517b \u2014 \u7ed9\u4f60\u7684\u5927\u8111\u52a0\u6cb9',PURPLE_DARK))
    elems.append(sp(12))

    elems.append(colored_box([
        Paragraph('\U0001f957 \u8425\u517b\u662f\u5b66\u4e60\u7684\u52a0\u901f\u5668',
                  S('S4T','Normal',fontSize=FS_H2,leading=18,textColor=PURPLE_DARK,bold=1)),
        Spacer(1,4),
        Paragraph(
            '\u5065\u5eb7\u7684\u996e\u98df\u4e0d\u4ec5\u8ba9\u4f60\u8eab\u4f53\u597d\uff0c\u8fd8\u80fd\u8ba9\u4f60\u7684\u5927\u8111\u8fd0\u8f6c\u66f4\u9ad8\u6548\u3002'
            '\u7279\u522b\u662f\u4e00\u4e9b\u79d1\u5b66\u5df2\u8bc1\u660e\u6709\u5229\u4e8e\u5927\u8111\u7684\u98df\u7269\uff0c\u8ba9\u4f60\u5b66\u4e60\u66f4\u8f7b\u677e\uff01',
            S('S4B','Normal',fontSize=FS_BODY,leading=19,textColor=colors.HexColor('#2C2C2C'))),
    ], bg=PURPLE_LIGHT, border=PURPLE_DARK))
    elems.append(sp(10))

    food_data = [
        ('\U0001f966', '\U0001f966', '\u85af\u6761\u7b49\u7b49', '\u7b49\u7b49', '🐟', '\u9c7c\u7b49\u7b49', '\u7b49\u7b49'),
        ('深海鱼\n(每周2-3次)', '深海鱼\n(每周2-3次)', '坚果\n(每天一小把)', '坚果\n(每天一小把)', '核桃等\n(亚麻籽油)', '核桃等\n(亚麻籽油)', '每周2-3次'),
    ]
    foods = [
        ('\U0001f969', '\u85af\u7c7b', '\u5168\u9c9c\u5168\u9c9c\u7684\u7b49\u7b49', '\u7b49\u7b49', '\U0001f35e', '\u9762\u7c7b', '\u9762\u7c7b\u7b49\u7b49', '\u7b49\u7b49'),
        ('\U0001f966', '\u6c34\u679c', '\u6c34\u679c\u65b0\u9c9c\u7684\u7b49\u7b49', '\u7b49\u7b49', '\U0001f966', '\u85af\u6761', '\u5168\u9c9c\u5168\u9c9c\u7b49\u7b49', '\u7b49\u7b49'),
        ('\U0001f969', '\u6df1\u6d77\u9c7c', '\u9ad8\u9c7c\u6d77\u9c7c\u7b49\u7b49', '\u7b49\u7b49', '\U0001f969', '\u6838\u6843', '\u6838\u6843\u7b49\u7b49', '\u7b49\u7b49'),
        ('\U0001f957', '\u7eff\u852c', '\u7eff\u852c\u852c\u83dc\u7b49\u7b49', '\u7b49\u7b49', '\U0001f957', '\u6c34', '\u6bcf\u5929\u5145\u8db3\u7684\u7b49\u7b49', '\u7b49\u7b49'),
    ]
    food_display = [
        ('\U0001f969', '\u6df1\u6d77\u9c7c', '\u6bcf\u5468 2-3 \u6b21\uff0c\u5bf9\u5927\u8111\u7279\u522b\u597d'),
        ('\U0001f966', '\u6838\u6843\u7b49', '\u6bcf\u5929\u4e00\u5c0f\u62cc\uff0c\u5c0f\u5c0f\u5c31\u591f'),
        ('\U0001f95a', '\u9c7c\u86c7\u86c7\u9c7c', '\u9c7c\u86c7\u86c7\u9c7c\uff0c\u4f18\u8d28\u86c7\u86c7\u86c7'),
        ('\U0001f96c', '\u85c1\u83dc\u7b49\u85c1\u83dc', '\u6bcf\u5929\u5145\u8db3\uff0c\u7b49\u7b49\u85c1\u83dc\u7b49\u7b49'),
    ]
    cw3 = (W - 4*cm) / 4 - 4
    card_data3 = [[Paragraph(f'<b>{ic}</b><br/><font size="13">{ti}</font><br/><font size="10">{de}</font>',
                             S(f'F{i}','Normal',fontSize=11,leading=15,
                               textColor=WHITE,alignment=TA_CENTER))]
                  for i,(ic,ti,de) in enumerate(food_display)]
    ftbl = Table([card_data3], colWidths=[cw3]*4, rowHeights=[90])
    for i3,(ic,ti,de) in enumerate(food_display):
        ftbl.setStyle(TableStyle([
            ('BACKGROUND',(i3,0),(i3,0),PURPLE_DARK),
            ('TOPPADDING',(i3,0),(i3,0),10),
            ('BOTTOMPADDING',(i3,0),(i3,0),10),
            ('LEFTPADDING',(i3,0),(i3,0),6),
            ('RIGHTPADDING',(i3,0),(i3,0),6),
            ('BOX',(i3,0),(i3,0),0.5,WHITE),
        ]))
    elems.append(ftbl)
    elems.append(sp(10))
    elems.append(colored_box([
        Paragraph('\U0001f48a \u5efa\u8bae\uff1a\u5148\u505a\u4e00\u4e2a\u7b80\u5355\u7684\u8840\u6e05\u68c0\u67e5\uff0c\u4e86\u89e3\u81ea\u5df1\u7684\u8425\u517b\u72b6\u51b5',
                  S('S4W','Normal',fontSize=FS_BODY,leading=17,textColor=PURPLE_DARK,bold=1)),
    ], bg=PINK_LIGHT, border=PINK_DARK))

    elems.append(sp(4))
    elems.append(hr_line())
    return elems

# ── Section 5: 鼓励寄语 ─────────────────────────────────────────
def build_section5():
    elems = []
    elems.append(section_banner('\u4e94\u3001\u7ed9\u4f60\u7684\u6d77\u5496 \u2014 \u5927\u8111\u672c\u6765\u5c31\u5f88\u5f3a\u5927',GREEN_DARK))
    elems.append(sp(14))

    elems.append(colored_box([
        Paragraph('\U0001f31f \u6700\u91cd\u8981\u7684\u4e00\u70b9',
                  S('S5T','Normal',fontSize=FS_H2,leading=20,textColor=GREEN_DARK,bold=1)),
        Spacer(1,6),
        Paragraph(
            '\u4f60\u7684\u5927\u8111\u672c\u6765\u5c31\u5f88\u5f3a\u5927\uff01\u521d\u4e8c\u5b66\u4e1a\u589e\u52a0\u4e86\u5b66\u4e60\u96be\u5ea6\uff0c\u4f46\u8fd9\u5e76\u4e0d\u610f\u5473\u7740\u4f60\u201c\u8bb0\u4f4f\u201d\u7684\u80fd\u529b\u6709\u95ee\u9898\u3002'
            '\u53ea\u662f\u4f60\u7684\u5927\u8111\u6b63\u5728\u5b66\u4e60\u66f4\u9ad8\u6548\u7684\u65b9\u6cd5\uff0c\u8fd9\u662f\u5b8c\u5168\u6b63\u5e38\u7684\uff01',
            S('S5B','Normal',fontSize=FS_BODY,leading=20,textColor=colors.HexColor('#2C2C2C'))),
    ], bg=GREEN_LIGHT, border=GREEN_DARK))
    elems.append(sp(12))

    # Encouragement cards
    encouragements = [
        ('\U0001f31f', '\u4f60\u6bcf\u5929\u90fd\u5728\u8fdb\u6b65', '\u521d\u4e8c\u662f\u5b66\u4e1a\u7684\u8f6c\u6298\u671f\uff0c\u8fdb\u6b65\u5c31\u662f\u6700\u68d2\u7684\u56de\u7b54'),
        ('\U0001f4aa', '\u52aa\u529b\u662f\u6709\u7528\u7684', '\u6bcf\u4e00\u6b21\u8d77\u65e5\u7684\u8c03\u6574\u548c\u5b66\u4e60\uff0c\u90fd\u5728\u8ba9\u4f60\u7684\u5927\u8111\u8f8d\u9a7c\u8f6c\u8f6c\u5730\u8fdb\u6b65'),
        ('\U0001f310', '\u65b9\u6cd5\u6bd4\u8d28\u91cf\u66f4\u91cd\u8981', '\u5b66\u4e60\u6709\u8f88\u95e8\u6280\u5de7\uff0c\u638c\u63e1\u65b9\u6cd5\u540e\u4f60\u4f1a\u53d1\u73b0\u5b66\u4e60\u5176\u5b9e\u5f88\u8f7b\u677e'),
        ('\U0001f44f', '\u4f60\u5df2\u7ecf\u5f88\u68d2\u4e86', '\u80fd\u591f\u8fdb\u5165\u521d\u4e8c\u5b66\u4e60\u5e76\u4e14\u5728\u52aa\u529b\uff0c\u8fd9\u672c\u8eab\u5c31\u8bc1\u660e\u4e86\u4f60\u7684\u4f18\u79c0'),
    ]
    cw4 = (W - 4*cm) / 2 - 6
    row1e = [[Paragraph(f'<b>{ic}</b><br/><font size="13">{ti}</font><br/><font size="11">{de}</font>',
                        S(f'E{i}','Normal',fontSize=11,leading=16,textColor=colors.HexColor('#2C2C2C')))]
             for i,(ic,ti,de) in enumerate(encouragements[:2])]
    row2e = [[Paragraph(f'<b>{ic}</b><br/><font size="13">{ti}</font><br/><font size="11">{de}</font>',
                        S(f'E{i+2}','Normal',fontSize=11,leading=16,textColor=colors.HexColor('#2C2C2C')))]
             for i,(ic,ti,de) in enumerate(encouragements[2:])]
    etbl = Table([row1e, row2e], colWidths=[cw4]*2, rowHeights=[95,95])
    for i4,(_,ti,de) in enumerate(encouragements):
        bg4 = GREEN_LIGHT if i4 < 2 else BLUE_LIGHT
        brd4 = GREEN_DARK if i4 < 2 else BLUE_MID
        etbl.setStyle(TableStyle([
            ('BACKGROUND',(i4%2,i4//2),(i4%2,i4//2),bg4),
            ('TOPPADDING',(i4%2,i4//2),(i4%2,i4//2),12),
            ('BOTTOMPADDING',(i4%2,i4//2),(i4%2,i4//2),12),
            ('LEFTPADDING',(i4%2,i4//2),(i4%2,i4//2),12),
            ('RIGHTPADDING',(i4%2,i4//2),(i4%2,i4//2),12),
            ('BOX',(i4%2,i4//2),(i4%2,i4//2),1.5,brd4),
        ]))
    elems.append(etbl)
    elems.append(sp(14))

    # Final message
    elems.append(highlight_bar(
        '\u52a0\u6cb9\uff01\u4f60\u5df2\u7ecf\u5f88\u68d2\uff01\u63a5\u4e0b\u6765\u8ba9\u4f60\u7684\u5927\u8111\u66f4\u9ad8\u6548\u5730\u8f6c\u8d77\u6765\uff01',
        bg=GREEN_DARK))
    elems.append(sp(12))

    # Action plan
    elems.append(Paragraph('\u2713 \u4eca\u5468\u5c31\u53ef\u4ee5\u505a\u7684\u4e8b\uff08\u9009\u505a\u5373\u53ef\uff09',
                            S('ChkT','Normal',fontSize=FS_H2,leading=18,textColor=BLUE_DARK,bold=1)))
    elems.append(sp(8))
    checks = [
        '\u4eca\u5929\u7761\u524d\uff0c\u5411\u723b\u723b\u8bb2\u4e00\u904d\u4eca\u5929\u5b66\u7684\u91cd\u70b9\u5185\u5bb9',
        '\u660e\u5929\u653e\u5b66\u540e\uff0c\u5148\u8fd0\u52a815\u5206\u949f\u518d\u5b66\u4e60',
        '\u6311\u6218\u81ea\u5df1\uff1a\u7528\u56fe\u7247\u8bb0\u4f4f3\u4e2a\u96be\u80cc\u7684\u77e5\u8bc6\u70b9',
        '\u559c\u6b22\u7684\u8fd0\u52a8\u653e\u5b66\u540e\u7ee7\u7eed\uff0c\u6bcf\u5468\u4e0d\u5c11\u4e8e3\u6b21',
    ]
    for ci, chk in enumerate(checks):
        elems.append(Paragraph(f'\u2610  {chk}',
                                S(f'Chk{ci}','Normal',fontSize=FS_BODY,leading=18,
                                  textColor=colors.HexColor('#2C2C2C'),leftIndent=12,spaceAfter=6)))

    return elems

# ── Build ──────────────────────────────────────────────────────
out_path = os.path.join(os.path.expanduser('~'), 'Desktop',
                        '初二男生大脑体高分指南_学生版.pdf')

doc = SimpleDocTemplate(
    out_path, pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=1.8*cm, bottomMargin=1.2*cm,
    title='\u521d\u4e8c\u7537\u751f\u5927\u8111\u4f53\u9ad8\u5206\u6307\u5357',
    author='QClaw AI Assistant',
    subject='\u5b66\u4e60\u65b9\u6cd5\u6307\u5357',
)

story = []
story += build_cover()
story += build_section1()
story += build_section2()
story += build_section3()
story += build_section4()
story += build_section5()

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f'\u2705 PDF\u5df2\u751f\u6210\uff1a{out_path}')
