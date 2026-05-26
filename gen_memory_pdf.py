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
RED_DARK    = colors.HexColor('#A62639')
RED_LIGHT   = colors.HexColor('#FAD7DC')
TEAL_DARK   = colors.HexColor('#0E7B7B')
TEAL_LIGHT  = colors.HexColor('#D0F0F0')
WHITE       = colors.white
GRAY_TEXT   = colors.HexColor('#555555')
LIGHT_GRAY  = colors.HexColor('#F5F5F5')

W, H = A4

def S(name, parent='Normal', **kw):
    return ParagraphStyle(name, parent=styles[parent], fontName=cn_font, **kw)

def sp(h=6):
    return Spacer(1, h)

def hr_line(color=BLUE_MID, thickness=0.5):
    return HRFlowable(width='100%', thickness=thickness, color=color, spaceAfter=6)

def section_banner(text, bg=BLUE_MID):
    tbl = Table([[Paragraph(text, S('SecT','Normal',fontSize=14,leading=19,textColor=WHITE))]],
                colWidths=[W - 4*cm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),
        ('TOPPADDING',(0,0),(-1,-1),10),
        ('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',(0,0),(-1,-1),16),
    ]))
    return tbl

def colored_box(rows, bg=BLUE_LIGHT, border=BLUE_MID):
    tbl = Table([[r] for r in rows], colWidths=[W - 4*cm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),
        ('TOPPADDING',(0,0),(-1,-1),8),
        ('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),14),
        ('RIGHTPADDING',(0,0),(-1,-1),14),
        ('BOX',(0,0),(-1,-1),1.5,border),
    ]))
    return tbl

def on_page(canvas_obj, doc):
    cnv = canvas_obj
    cnv.saveState()
    cnv.setFillColor(BLUE_DARK)
    cnv.rect(0, H - 18, W, 18, fill=1, stroke=0)
    cnv.setFillColor(WHITE)
    cnv.setFont(cn_font, 8)
    cnv.drawString(2*cm, H - 12, '\u6d77\u9a6c\u4f53\u529f\u80fd\u89e3\u6790\u4e0e\u8bb0\u5fc6\u529b\u6539\u5584\u65b9\u6848 \u00b7 2026')
    cnv.drawRightString(W - 2*cm, H - 12, f'\u7b2c {doc.page} \u9875')
    cnv.setFillColor(LIGHT_GRAY)
    cnv.rect(0, 0, W, 20, fill=1, stroke=0)
    cnv.setFillColor(GRAY_TEXT)
    cnv.setFont(cn_font, 8)
    cnv.drawCentredString(W/2, 6, '\u672c\u65b9\u6848\u4ec5\u4f9b\u53c2\u8003\uff0c\u4e0d\u6784\u6210\u533b\u5b66\u8bca\u65ad\u5efa\u8bae')
    cnv.restoreState()

# ── Cover ──────────────────────────────────────────────────────
def build_cover():
    elems = []
    t = Table([
        [Paragraph('\U0001f9db  \u521d\u4e8c\u7537\u751f\u8bb0\u5fc6\u529b\u504f\u5f31',
                   S('C1','Normal',fontSize=20,leading=26,textColor=WHITE,alignment=TA_CENTER))],
        [Paragraph('\u6d77\u9a6c\u4f53\u529f\u80fd\u89e3\u6790\u4e0e\u6539\u5584\u65b9\u6848',
                   S('C2','Normal',fontSize=26,leading=34,textColor=WHITE,alignment=TA_CENTER,bold=1))],
        [Paragraph('\u9488\u5bf9\u5bb6\u957f\u63d0\u95ee\u7684\u4e13\u4e1a\u7b54\u590d',
                   S('C3','Normal',fontSize=12,leading=16,textColor=colors.HexColor('#A8D0F0'),alignment=TA_CENTER))],
    ], colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),BLUE_DARK),
        ('TOPPADDING',(0,0),(-1,-1),24),
        ('BOTTOMPADDING',(0,0),(-1,-1),24),
    ]))
    elems.append(t)
    elems.append(sp(16))

    cards = [
        (BLUE_MID,   '\U0001f9db', '\u79d1\u5b66\u754c\u5b9a',
         '\u6e05\u91ca\u201c\u6d77\u9a6c\u4f53\u95ee\u9898\u201d\u8bf4\u6cd5\n\u533a\u5206\u5668\u8d28\u6027\u75c5\u53d8\u4e0e\u529f\u80fd\u6027\u4f4e\u6548'),
        (GREEN_DARK, '\U0001f634', '\u7761\u7720\u4f18\u5148',
         '\u6df1\u5ea6\u7761\u7720\u4e0d\u8db3\u662f\u9057\u5fd8\u4e3b\u56e0\n\u7761\u524d\u8bb0\u5fc6\u6cd5\u76f4\u63a5\u6fc0\u6d3b\u6d77\u9a6c\u4f53'),
        (ORANGE_DARK,'\U0001f3c3', '\u8fd0\u52a8\u517b\u8111',
         '\u9ad8\u5f3a\u95f4\u6b47\u8fd0\u52a8\u5206\u6ccc\u9b44\u7d2b\u7d20\n\u4fc3\u8fdb\u6d77\u9a6c\u4f53\u795e\u7ecf\u751f\u957f'),
        (TEAL_DARK,  '\U0001f957', '\u7cbe\u51c6\u8425\u517b',
         '\u7ef4\u751f\u7d20D\u5173\u4e4e\u6d77\u9a6c\u4f53\u53d1\u80c3\nOmega-3 \u8102\u80aa\u9178\u52a9\u529b\u8bb0\u5fc6'),
    ]
    cw = (W - 4*cm) / 4 - 3
    card_data = [[Paragraph(f'<b>{ic}</b><br/>{ti}<br/>{de}',
                             S(f'CD{i}','Normal',fontSize=9,leading=13,
                               textColor=WHITE,alignment=TA_CENTER))]
                  for i,(color,ic,ti,de) in enumerate(cards)]
    ct = Table([card_data], colWidths=[cw]*4, rowHeights=[95])
    for i2,(color,_,_,_) in enumerate(cards):
        ct.setStyle(TableStyle([
            ('BACKGROUND',(i2,0),(i2,0),color),
            ('TOPPADDING',(i2,0),(i2,0),10),
            ('BOTTOMPADDING',(i2,0),(i2,0),10),
            ('LEFTPADDING',(i2,0),(i2,0),5),
            ('RIGHTPADDING',(i2,0),(i2,0),5),
            ('BOX',(i2,0),(i2,0),0.5,WHITE),
        ]))
    elems.append(ct)
    elems.append(sp(18))
    elems.append(hr_line(BLUE_LIGHT, 1))
    elems.append(sp(8))
    elems.append(Paragraph(f'\U0001f4c5 \u5236\u5b9a\u65e5\u671f\uff1a2026\u5e744\u670812\u65e5',
                            S('DT','Normal',fontSize=10,textColor=GRAY_TEXT,alignment=TA_CENTER)))
    elems.append(PageBreak())
    return elems

# ── Section 1 ──────────────────────────────────────────────────
def build_section1():
    elems = []
    elems.append(section_banner('\u4e00\u3001\u5173\u4e8e\u201c\u6d77\u9a6c\u4f53\u5b58\u5728\u95ee\u9898\u201d\u8bf4\u6cd5\u7684\u79d1\u5b66\u7116\u5b9a',BLUE_MID))
    elems.append(sp(10))
    elems.append(Paragraph(
        '\u5bb6\u957f\u5173\u6ce8\u7684\u8fd9\u4e2a\u8bf4\u6cd5\uff0c\u65e2\u5bf9\u4e5f\u4e0d\u5b8c\u5168\u5bf9\uff0c\u8bf7\u5148\u660e\u786e\u6982\u5ff5\u4ee5\u907f\u514d\u7109\u601d\uff1a',
        S('I1','Normal',fontSize=10.5,leading=16,textColor=BLUE_DARK,spaceAfter=8)))

    cards1 = [
        (BLUE_LIGHT, BLUE_MID, '\u2705  \u6b63\u786e\u7684\u903b\u8f91',
         '\u6d77\u9a6c\u4f53\u662f\u5927\u8111\u8d1f\u8d23\u5c06\u201c\u77ac\u65e5\u8bb0\u5fc6\u201d\u56fa\u5316\u4e3a\u201c\u957f\u671f\u8bb0\u5fc6\u201d\u7684\u6838\u5fc3\u5668\u5b98\u3002'),
        (RED_LIGHT, RED_DARK, '\u26a0  \u9700\u8981\u4fee\u6b63\u7684\u8ba4\u77e5',
         '\u4e34\u5e8a\u610f\u4e49\u4e0a\u7684\u201c\u6d77\u9a6c\u4f53\u5b58\u5728\u95ee\u9898\u201d\u6307\u5668\u8d28\u6027\u75c5\u53d8\uff08\u5982\u840e\u7f29\u3001\u7f3a\u8840\uff09\uff0c'
         '\u5728\u9752\u5c11\u5e74\u4e2d\u6781\u5171\u5e73\u89c1\uff0c\u4e14\u4f1a\u964b\u968f\u4e25\u91cd\u7684\u5b9a\u5411\u969c\u788e\u6216\u766a\u75c5\u53d1\u4f5c\u3002'),
        (GREEN_LIGHT, GREEN_DARK,'\U0001f3af  \u51c6\u786e\u63cf\u8ff0',
         '\u521d\u4e8c\u7537\u751f\u7684\u6d77\u9a6c\u4f53\u7ed3\u6784\u5b8c\u597d\uff0c\u4ec5\u56e0\u73af\u5883\u4e0e\u6fc0\u7d20\u56e0\u7d20\u6682\u65f6\u5904\u4e8e\u201c\u4f4e\u529f\u8017\u5de5\u4f5c\u6a21\u5f0f\u201d\u3002'),
    ]
    for idx, (bg, border, title, body_txt) in enumerate(cards1):
        t2 = Table([
            [Paragraph(title, S(f'S1T{idx}','Normal',fontSize=11,leading=15,textColor=border,bold=1)), ''],
            [Paragraph(body_txt, S(f'S1B{idx}','Normal',fontSize=10.5,leading=16,textColor=colors.HexColor('#2C2C2C'))), ''],
        ], colWidths=[W - 4.6*cm, 0.4*cm])
        t2.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,-1),bg),
            ('TOPPADDING',(0,0),(-1,-1),8),
            ('BOTTOMPADDING',(0,0),(-1,-1),8),
            ('LEFTPADDING',(0,0),(-1,-1),14),
            ('SPAN',(0,0),(1,0)),
            ('SPAN',(0,1),(1,1)),
            ('BOX',(0,0),(-1,-1),1.5,border),
        ]))
        elems.append(t2)
        elems.append(sp(8))
    elems.append(sp(4))
    elems.append(hr_line())
    return elems

# ── Section 2 ──────────────────────────────────────────────────
def build_section2():
    elems = []
    elems.append(section_banner('\u4e8c\u3001\u521d\u4e8c\u7537\u751f\u8bb0\u5fc6\u529b\u504f\u5f31\u7684\u4e09\u5927\u771f\u5b9e\u5143\u51f6\u72b6\uff08\u975e\u6d77\u9a6c\u4f53\u75c5\u53d8\uff09',TEAL_DARK))
    elems.append(sp(10))

    bullets2 = [
        (ORANGE_DARK, ORANGE_LIGHT, '\U0001f534  \u7b2c\u4e00\u5143\u51f6\uff1a\u7761\u7720\u526a\u6740\uff08\u9996\u8981\u539f\u56e0\uff09', [
            '\u6df1\u5ea6\u7761\u7720\u671f\u95f4\uff0c\u6d77\u9a6c\u4f53\u624d\u5c06\u767d\u5929\u77e5\u8bc6\u642c\u8fd0\u81f3\u5927\u8111\u76ae\u5c42\u6c38\u4e45\u50a8\u5b58\u3002',
            '\u521d\u4e8c\u8bfe\u4e1a\u91cd\u3001\u624b\u673a\u5e72\u6270\u5bfc\u81f4\u6df1\u5ea6\u7761\u7720\u4e0d\u8db3 \u2192 \u6d77\u9a6c\u4f53\u201c\u642c\u8fd0\u5931\u8d25\u201d\uff0c\u8bb0\u5fc6\u4e22\u5931\u3002',
        ]),
        (RED_DARK, RED_LIGHT, '\U0001f7fe  \u7b2c\u4e8c\u5143\u51f6\uff1a\u76ae\u8d28\u9187\u5e72\u6270\uff08\u60c5\u7eea\u4e0e\u538b\u529b\uff09', [
            '\u9752\u6625\u671f\u654f\u611f\u3001\u5b66\u4e1a\u538b\u529b\u5bfc\u81f4\u4f53\u5185\u538b\u529b\u6fc0\u7d20\uff08\u76ae\u8d28\u9187\uff09\u5347\u9ad8\u3002',
            '\u9ad8\u6fc0\u5ea6\u76ae\u8d28\u9187\u4f1a\u76f4\u63a5\u62d6\u5236\u6d77\u9a6c\u4f53\u795e\u7ecf\u5143\u518d\u751f\uff0c\u9020\u6210\u201c\u80cc\u5c31\u5fd8\u4e86\u201d\u3002',
        ]),
        (PURPLE_DARK, PURPLE_LIGHT, '\U0001f7e3  \u7b2c\u4e09\u5143\u51f6\uff1a\u8bb0\u5fc6\u7b56\u7565\u672a\u8f6c\u578b', [
            '\u521d\u4e8c\u77e5\u8bc6\u9700\u4ece\u5c0f\u5b66\u7684\u201c\u58f0\u97f3\u8bb0\u5fc6\uff08\u6b7b\u8bb0\u786c\u80cc\uff09\u201d\u8f6c\u5411\u201c\u903b\u8f91\u56fe\u50cf\u8bb0\u5fc6\u201d\u3002',
            '\u82e5\u7ee7\u7eed\u6cbf\u7528\u8001\u65b9\u6cd5\uff0c\u6d77\u9a6c\u4f53\u5bf9\u67af\u71e5\u7eaf\u6587\u5b57\u4fe1\u606f\u63a5\u6536\u6548\u7387\u6781\u4f4e\u3002',
        ]),
    ]
    for idx, (dark, light, title, pts) in enumerate(bullets2):
        box_rows = [Paragraph(title, S(f'S2T{idx}','Normal',fontSize=12,leading=16,textColor=dark,bold=1))]
        for pt in pts:
            box_rows.append(Paragraph(f'<b>\u25b8</b> {pt}',
                                      S(f'S2P{idx}','Normal',fontSize=10.5,leading=17,
                                        textColor=colors.HexColor('#2C2C2C'))))
        elems.append(colored_box(box_rows, bg=light, border=dark))
        elems.append(sp(10))

    elems.append(sp(4))
    elems.append(hr_line())
    return elems

# ── Section 3 ──────────────────────────────────────────────────
def build_section3():
    elems = []
    elems.append(section_banner('\u4e09\u3001\u79d1\u5b66\u6539\u5584\u6d77\u9a6c\u4f53\u529f\u80fd\u7684\u5b9e\u64cd\u65b9\u6848\uff08\u9488\u5bf9\u521d\u4e8c\u7537\u751f\uff09',GREEN_DARK))
    elems.append(sp(12))

    plans = [
        {'prio':'\u7b2c\u4e00\u4f18\u5148\u7ea7','color':BLUE_MID,'bg':BLUE_LIGHT,
         'icon':'\U0001f634','title':'\u5229\u7528\u201c\u7761\u7720\u8bb0\u5fc6\u6cd5\u201d\u6fc0\u6d3b\u6d77\u9a6c\u4f53',
         'points':[
             ('\u9ec4\u91d1\u65f6\u6bb5','\u7761\u524d 15 \u5206\u949f'),
             ('\u5177\u4f53\u64cd\u4f5c','\u4e0d\u505a\u9898\uff0c\u53ea\u80cc\u5355\u8bcd\u3001\u53e4\u6587\u6216\u5386\u53f2\u5e74\u4ee3\u3002\u95ed\u773c\u542c\u82f1\u6587\u6216\u53e4\u6587\u6fc0\u8386\u97f3\u9891\u3002'),
             ('\u6b21\u65e5\u5f3a\u5316','\u65e9\u8d77\u82b1 5 \u5206\u949f\u5feb\u901f\u6d4f\u89c8\u665a\u4e0a\u5185\u5bb9\u3002'),
             ('\u9884\u671f\u6548\u679c','\u5229\u7528\u6d77\u9a6c\u4f53\u7761\u7720\u671f\u5904\u7406\u673a\u5236\uff0c\u9057\u5fd8\u7387\u663e\u8457\u964d\u4f4e\uff0c\u6548\u679c\u4f18\u4e8e\u767d\u5929 1 \u5c0f\u65f6\u6b7b\u8bb0\u786c\u80cc\u3002'),
         ],
         'tip':'\U0001f3c6 \u9ec4\u91d1\u6cd5\u5219\uff1a\u7761\u524d\u4e0d\u5237\u624b\u673a\uff0c\u4e0d\u770b\u89c6\u9891\uff0c\u53ea\u505a\u7eaf\u8bb0\u5fc6\u8f93\u5165\u3002'},
        {'prio':'\u7b2c\u4e8c\u4f18\u5148\u7ea7','color':ORANGE_DARK,'bg':ORANGE_LIGHT,
         'icon':'\U0001f3c3','title':'\u8fd0\u52a8\u5206\u6ccc\u201c\u6d77\u9a6c\u4f53\u517b\u6599\u201d',
         'points':[
             ('\u79d1\u5b66\u539f\u7406','\u9ad8\u5f3a\u5ea6\u95f4\u6b47\u8fd0\u52a8\u4ea7\u751f\u7684\u201c\u9b44\u7d2b\u7d20\u201d\u53ef\u76f4\u63a5\u4fc3\u8fdb\u6d77\u9a6c\u4f53\u795e\u7ecf\u751f\u957f\u3002'),
             ('\u5177\u4f53\u64cd\u4f5c','\u653e\u5b66\u540e\u3001\u665a\u996d\u524d\u8fdb\u884c 15 \u5206\u949f\u5267\u70c8\u8fd0\u52a8\uff08\u51b2\u523a\u8dd1\u697c\u68af\u3001\u8df3\u7ef3\u53cc\u6447\u3001\u9ad8\u62ac\u817f\u81f3\u6c14\u559d\uff09\u3002'),
             ('\u65f6\u95f4\u5b89\u6392','\u8fd0\u52a8\u540e\u534a\u5c0f\u65f6\u518d\u8fdb\u9910\u3001\u5199\u4f5c\u4e1a\u3002'),
         ],
         'tip':'\u26a1 \u5173\u952e\u662f\u201c\u6c14\u559d\u54cd\u54cd\u201d\u2014\u2014\u6709\u6c27\u5f3a\u5ea6\u4e0d\u8db3\u5219\u9b44\u7d2b\u7d20\u5206\u6ccc\u4e0d\u8db3\u3002'},
        {'prio':'\u7b2c\u4e09\u4f18\u5148\u7ea7','color':PURPLE_DARK,'bg':PURPLE_LIGHT,
         'icon':'\U0001f9e9','title':'\u5c06\u7b79\u8c61\u6587\u5b57\u8f6c\u5316\u4e3a\u201c\u52a8\u4f5c\u4e0e\u7a7a\u95f4\u201d\uff08\u53d1\u6325\u7537\u5b69\u8bb0\u5fc6\u4f18\u52bf\uff09',
         'points':[
             ('\u8bb0\u5386\u53f2\u4e8b\u4ef6','\u7528\u4e50\u9ad8\u5c0f\u4eba\u6216\u706b\u68d2\u4eba\u6a21\u62df\u6218\u4e89\u8def\u7ebf\u4e0e\u903b\u8f91\uff0c\u6fc0\u6d3b\u6d77\u9a6c\u4f53\u7a7a\u95f4\u8bb0\u5fc6\u533a\u3002'),
             ('\u8bb0\u5730\u7406\u5730\u5f62','\u95ed\u773c\u60f3\u8c61\u65e0\u4eba\u673a\u89c6\u89d2\uff0c\u7528\u624b\u5728\u7a7a\u4e2d\u52fe\u52d2\u5c71\u8109\u8d70\u5411\u3002'),
         ],
         'tip':'\U0001f9e0 \u7537\u5b69\u5929\u751f\u7a7a\u95f4\u611f\u5f3a\uff0c\u5584\u7528\u8fd9\u4e00\u4f18\u52bf\u6bd4\u786c\u80cc\u6709\u6548 3 \u500d\u4ee5\u4e0a\u3002'},
        {'prio':'\u7b2c\u56db\u4f18\u5148\u7ea7','color':TEAL_DARK,'bg':TEAL_LIGHT,
         'icon':'\U0001f957','title':'\u7cbe\u51c6\u8425\u517b\u652f\u6301',
         'points':[
             ('\u7ef4\u751f\u7d20 D','\u4e2d\u56fd\u521d\u4e2d\u751f\u6d45\u9047\u5e38\u89c1\uff0c\u5efa\u8bae\u6bcf\u65e5\u8865\u5145 400-800 IU\uff0c\u5173\u4e4e\u6d77\u9a6c\u4f53\u4f53\u79ef\u53d1\u80c3\u3002'),
             ('DHA \u6765\u6e90','\u4e0d\u7231\u5403\u9c7c\u8005\u53ef\u6bcf\u5468\u98df\u7528 2-3 \u6b21\u6838\u6843\u6216\u4e9a\u9ebb\u7c92\u6cb9\u51c9\u62cc\u83dc\u3002'),
         ],
         'tip':'\U0001f48a \u5efa\u8bae\u5148\u505a\u8840\u6e05\u7ef4\u751f\u7d20D\u68c0\u6d4b\uff0c\u518d\u9075\u533b\u5631\u8865\u5145\u5242\u91cf\u3002'},
    ]

    for plan_idx, plan in enumerate(plans):
        badge_row = Table([[
            Paragraph(f'{plan["icon"]}  {plan["prio"]}',
                     S(f'Badge{plan_idx}','Normal',fontSize=9.5,textColor=WHITE,alignment=TA_CENTER)),
            Paragraph(plan['title'], S(f'PT{plan_idx}','Normal',fontSize=12,leading=16,
                                        textColor=plan['color'],bold=1)),
        ]], colWidths=[2.5*cm, W - 7*cm])
        badge_row.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(0,0),plan['color']),
            ('BACKGROUND',(1,0),(1,0),plan['bg']),
            ('TOPPADDING',(0,0),(-1,-1),10),
            ('BOTTOMPADDING',(0,0),(-1,-1),10),
            ('LEFTPADDING',(0,0),(0,0),6),
            ('LEFTPADDING',(1,0),(1,0),12),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ]))
        elems.append(badge_row)

        pt_rows = []
        for pj, (lbl, cnt) in enumerate(plan['points']):
            pt_rows.append([
                Paragraph(f'<b>{lbl}</b>', S(f'PL{plan_idx}_{pj}','Normal',fontSize=10,
                                             textColor=plan['color'],alignment=TA_CENTER)),
                Paragraph(cnt, S(f'PC{plan_idx}_{pj}','Normal',fontSize=10.5,leading=16,
                                 textColor=colors.HexColor('#2C2C2C'))),
            ])
        ptbl = Table(pt_rows, colWidths=[2.5*cm, W - 7*cm])
        ptbl.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,-1),plan['bg']),
            ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#CCCCCC')),
            ('TOPPADDING',(0,0),(-1,-1),6),
            ('BOTTOMPADDING',(0,0),(-1,-1),6),
            ('LEFTPADDING',(0,0),(-1,-1),10),
            ('RIGHTPADDING',(0,0),(-1,-1),10),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('FONTNAME',(0,0),(0,-1),cn_font),
        ]))
        elems.append(ptbl)
        elems.append(sp(4))
        elems.append(Paragraph(f'\U0001f4a1 {plan["tip"]}',
                               S(f'Tip{plan_idx}','Normal',fontSize=9.5,leading=14,
                                 textColor=plan['color'],leftIndent=10)))
        elems.append(sp(14))

    elems.append(hr_line())
    return elems

# ── Section 4 ──────────────────────────────────────────────────
def build_section4():
    elems = []
    elems.append(section_banner('\u56db\u3001\u7ed9\u5bb6\u957f\u7684\u7b2c\u4e00\u4e2a\u5b9e\u8df5\u5efa\u8bae\uff1a\u4eca\u665a\u5373\u53ef\u8fdb\u884c\u7684\u5c0f\u5b9e\u9a8c',ORANGE_DARK))
    elems.append(sp(12))
    elems.append(Paragraph(
        '\u8bf7\u4eca\u665a\u5c31\u5f00\u59cb\u2014\u2014\u5b69\u5b50\u5c06\u8eab\u4ece\u9a8c\u8bc1\u201c\u5e76\u975e\u81ea\u5df1\u8111\u5b50\u67af\uff0c\u800c\u662f\u65b9\u6cd5\u9700\u8c03\u6574\u201d\uff1a',
        S('S4I','Normal',fontSize=10.5,leading=16,textColor=ORANGE_DARK,bold=1,spaceAfter=10)
    ))
    steps4 = [
        ('\U0001f319  \u4eca\u665a\u7761\u89c9\u524d', '\u8ba9\u5b69\u5b50\u53ea\u80cc 5 \u4e2a\u6700\u96be\u7684\u5355\u8bcd\uff0c\u80cc\u5b8c\u7acb\u523b\u5173\u706f\u7761\u89c9\u3002'),
        ('\u2600\ufe0f  \u660e\u65e9\u8d77\u5e8a\u540e', '\u7acb\u5373\u542c\u5199\u8fd9 5 \u4e2a\u5355\u8bcd\uff08\u4e0d\u8981\u770b\u4e66\uff0c\u76f4\u63a5\u5199\uff09\u3002'),
        ('\U0001f4ca  \u8bc4\u4f30\u7ed3\u679c', '\u82e5\u6548\u679c\u663e\u8457 \u2192 \u5b69\u5b50\u5c06\u5efa\u7acb\u4fe1\u5fc3\uff1b\u82e5\u6548\u679c\u4e0d\u4f73 \u2192 \u6392\u9664\u7761\u7720\u95ee\u9898\u5f71\u54cd\u3002'),
    ]
    for si, (lbl, cnt) in enumerate(steps4):
        tr = Table([[Paragraph(lbl, S(f'S4L{si}','Normal',fontSize=11,leading=16,
                                       textColor=ORANGE_DARK,bold=1)),
                     Paragraph(cnt, S(f'S4C{si}','Normal',fontSize=10.5,leading=16,
                                      textColor=colors.HexColor('#2C2C2C')))]],
                   colWidths=[3.5*cm, W - 7*cm])
        tr.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,-1),ORANGE_LIGHT),
            ('TOPPADDING',(0,0),(-1,-1),9),
            ('BOTTOMPADDING',(0,0),(-1,-1),9),
            ('LEFTPADDING',(0,0),(-1,-1),12),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('BOX',(0,0),(-1,-1),1,ORANGE_DARK),
        ]))
        elems.append(tr)
        elems.append(sp(6))
    elems.append(sp(10))
    elems.append(colored_box([
        Paragraph('\U0001f3c6  \u6838\u5fc3\u610f\u4e49', S('SigT','Normal',fontSize=11,leading=16,textColor=GREEN_DARK,bold=1)),
        Paragraph('\u5efa\u7acb\u4fe1\u5fc3\u662f\u540e\u7eed\u4e00\u5207\u6539\u5584\u63aa\u65bd\u7684\u57fa\u7840\u3002'
                  '\u5f53\u5b69\u5b50\u76f8\u4fe1\u81ea\u5df1\u201c\u80fd\u8bb0\u4f4f\u201d\u65f6\uff0c\u6d77\u9a6c\u4f53\u4f1a\u81ea\u52a8\u63d0\u5347\u4fe1\u606f\u63a5\u6536\u6548\u7387\u3002',
                  S('SigB','Normal',fontSize=10.5,leading=16,textColor=colors.HexColor('#2C2C2C'))),
    ], bg=GREEN_LIGHT, border=GREEN_DARK))
    elems.append(sp(4))
    elems.append(hr_line())
    return elems

# ── Section 5 ──────────────────────────────────────────────────
def build_section5():
    elems = []
    elems.append(section_banner('\u4e94\u3001\u603b\u7ed3\u5bc4\u8bed',PURPLE_DARK))
    elems.append(sp(12))
    elems.append(colored_box([
        Paragraph('\U0001f4cb  \u8bf7\u5bb6\u957f\u5bbd\u5fc3', S('ST','Normal',fontSize=13,leading=18,textColor=PURPLE_DARK,bold=1)),
        Spacer(1,4),
        Paragraph(
            '\u5b69\u5b50\u5927\u8111<b>\u4e0d\u5b58\u5728\u5668\u8d28\u6027\u75c5\u53d8</b>\uff0c\u4ec5\u662f\u8fd0\u884c\u6a21\u5f0f\u672a\u9002\u914d\u521d\u4e8c\u9636\u6bb5\u7684\u5b66\u4e60\u8981\u6c42\u3002'
            '\u901a\u8fc7\u8c03\u6574\u7761\u7720\u8282\u5f8b\u3001\u8fd0\u52a8\u673a\u65f6\u4e0e\u8bb0\u5fc6\u7b56\u7565\uff0c\u6d77\u9a6c\u4f53\u7684\u5de5\u4f5c\u6548\u7387\u5c06\u83b7\u5f97\u660e\u663e\u63d0\u5347\u3002',
            S('SB','Normal',fontSize=11,leading=18,textColor=colors.HexColor('#2C2C2C'))),
        Spacer(1,10),
        Paragraph('\U0001f44d  \u4e09\u4e2a\u5173\u952e\u8bcd\uff1a\u5145\u8db3\u7761\u7720 \u2022 \u9593\u6b47\u8fd0\u52a8 \u2022 \u56fe\u50cf\u8bb0\u5fc6',
                  S('SK','Normal',fontSize=11,leading=16,textColor=PURPLE_DARK,bold=1)),
    ], bg=PURPLE_LIGHT, border=PURPLE_DARK))
    elems.append(sp(14))
    elems.append(hr_line(ORANGE_LIGHT, 1))
    elems.append(sp(6))
    elems.append(Paragraph('\u2713  \u884c\u52a8\u6e05\u5355\uff08\u672c\u5468\u5f00\u59cb\uff09',
                            S('ChkT','Normal',fontSize=12,leading=16,textColor=BLUE_DARK,bold=1)))
    elems.append(sp(6))
    check_items = [
        ('\u4eca\u665a', '\u6267\u884c\u201c5\u5355\u8bcd\u7761\u524d\u8bb0\u5fc6\u201d\u5b9e\u9a8c\uff0c\u8bb0\u5f55\u7ed3\u679c\u3002'),
        ('\u672c\u5468', '\u6bcf\u5929\u786e\u4fdd\u5b69\u5b50 22:00 \u524d\u4e0a\u5e8a\uff0c\u7761\u524d 1 \u5c0f\u65f6\u7981\u7528\u624b\u673a\u3002'),
        ('\u672c\u5468', '\u5b89\u6392\u6bcf\u5929 15 \u5206\u949f\u9ad8\u5f3a\u5ea6\u95f4\u6b47\u8fd0\u52a8\uff08\u8df3\u7ef3/\u51b2\u523a\u8dd1\u697c\u68af\uff09\u3002'),
        ('\u672c\u5468', '\u4e0e\u5b69\u5b50\u4e00\u8d77\u5c06\u672c\u5468\u6700\u96be\u80cc\u7684 3 \u4e2a\u77e5\u8bc6\u70b9\u5236\u4f5c\u6210\u201c\u56fe\u50cf\u8bb0\u5fc6\u5361\u201d\u3002'),
        ('\u672c\u6708', '\u5b89\u6392\u8840\u6e05\u7ef4\u751f\u7d20 D \u68c0\u6d4b\uff0c\u6709\u5fc5\u8981\u65f6\u8865\u5145\u8425\u517b\u8865\u5242\u3002'),
    ]
    for ci, (when, item) in enumerate(check_items):
        elems.append(Paragraph(f'\u2610  <b>{when}</b>\uff1a{item}',
                                S(f'Chk{ci}','Normal',fontSize=10.5,leading=16,
                                  textColor=colors.HexColor('#2C2C2C'),leftIndent=10,spaceAfter=5)))
    elems.append(sp(16))
    elems.append(colored_box([
        Paragraph('\U0001f4c4  \u672c\u65b9\u6848\u9002\u7528\u8bf4\u660e',
                   S('FNt','Normal',fontSize=10,leading=14,textColor=GRAY_TEXT)),
        Paragraph(
            '\u672c\u65b9\u6848\u57fa\u4e8e\u795e\u7ecf\u79d1\u5b66\u6587\u732e\u4e0e\u4e34\u5e8a\u7ecf\u9a8c\u5236\u5b9a\uff0c\u9002\u7528\u4e8e\u8bb0\u5fc6\u529b\u6682\u65f6\u504f\u5f31\u4f46\u65e0\u5668\u8d28\u6027\u75c5\u53d8\u7684\u9752\u5c11\u5e74\u3002'
            '\u82e5\u5b69\u5b50\u51fa\u73b0\u6301\u7eed\u4e25\u91cd\u9057\u5fd8\u3001\u65b9\u5411\u611f\u4e22\u5931\u3001\u9891\u7e41\u766a\u75c5\u53d1\u4f5c\u7b49\u60c5\u51b5\uff0c\u8bf7\u53ca\u65f6\u5c31\u533b\u8fdb\u884c\u4e13\u4e1a\u8bc4\u4f30\u3002',
            S('FNB','Normal',fontSize=10,leading=14,textColor=GRAY_TEXT)),
    ], bg=LIGHT_GRAY, border=colors.HexColor('#AAAAAA')))
    return elems

# ── Build ──────────────────────────────────────────────────────
out_path = os.path.join(os.path.expanduser('~'), 'Desktop',
                        '\u521d\u4e8c\u7537\u751f\u8bb0\u5fc6\u529b\u6539\u5584\u65b9\u6848_\u56fe\u6587\u7248.pdf')

doc = SimpleDocTemplate(
    out_path, pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=1.8*cm, bottomMargin=1.2*cm,
    title='\u521d\u4e8c\u7537\u751f\u8bb0\u5fc6\u529b\u504f\u5f31\uff1a\u6d77\u9a6c\u4f53\u529f\u80fd\u89e3\u6790\u4e0e\u6539\u5584\u65b9\u6848',
    author='QClaw AI Assistant',
    subject='\u8bb0\u5fc6\u529b\u6539\u5584',
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
