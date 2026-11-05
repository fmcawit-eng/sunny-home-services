#!/usr/bin/env python3
"""
Renders the page log as a PDF.

Reads tools/pagelog.csv, so the PDF and the spreadsheet can never disagree.
Run:  python3 tools/pagelog.py && python3 tools/handoff_pdf.py
"""
import csv, os, re, sys, datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph,
                                Spacer, PageBreak, KeepTogether)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV  = os.path.join(ROOT, 'tools', 'pagelog.csv')

SKY    = colors.HexColor('#03A6CC')
SKY_D  = colors.HexColor('#0288a8')
GOLD   = colors.HexColor('#FFC704')
ORANGE = colors.HexColor('#F17601')
INK    = colors.HexColor('#454545')
MUTED  = colors.HexColor('#6B7480')
LINE   = colors.HexColor('#DBE3E6')
TINT   = colors.HexColor('#F3FBFE')
SAND   = colors.HexColor('#FAF4ED')
AMBER  = colors.HexColor('#8a5a00')

S = lambda **k: ParagraphStyle(**dict({'alignment': TA_LEFT}, **k))
H1    = S(name='H1', fontName='Helvetica-Bold', fontSize=19, leading=23, textColor=SKY_D)
SUB   = S(name='SUB', fontName='Helvetica', fontSize=9.5, leading=13, textColor=MUTED)
H2    = S(name='H2', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=SKY_D,
          spaceBefore=11, spaceAfter=4)
BODY  = S(name='BODY', fontName='Helvetica', fontSize=9, leading=12.5, textColor=INK, spaceAfter=5)
CELL  = S(name='CELL', fontName='Helvetica', fontSize=6.6, leading=7.7, textColor=INK)
CELLM = S(name='CELLM', fontName='Helvetica', fontSize=6.3, leading=7.5, textColor=MUTED)
CELLB = S(name='CELLB', fontName='Helvetica-Bold', fontSize=6.6, leading=7.7, textColor=SKY_D)
NUM   = S(name='NUM', fontName='Helvetica', fontSize=6.1, leading=7.7,
          textColor=colors.HexColor('#9aa8b0'), alignment=TA_RIGHT)
HEADC = S(name='HEADC', fontName='Helvetica-Bold', fontSize=6.9, leading=8.4, textColor=colors.white)
HEADN = S(name='HEADN', fontName='Helvetica-Bold', fontSize=6.9, leading=8.4,
          textColor=colors.HexColor('#CFEFF8'), alignment=TA_RIGHT)

STATUS = {
    'BUILT':       (colors.HexColor('#e2f4fa'), SKY_D),
    'BUILT, NEW':  (colors.HexColor('#fff6d6'), AMBER),
    'PLACEHOLDER': (SAND, ORANGE),
    'TEMPLATE':    (colors.HexColor('#eef1f2'), MUTED),
}
PAD = [('TOPPADDING', (0,0), (-1,-1), 2.4), ('BOTTOMPADDING', (0,0), (-1,-1), 2.4),
       ('LEFTPADDING', (0,0), (-1,-1), 5), ('RIGHTPADDING', (0,0), (-1,-1), 5)]


class Numbered(canvas.Canvas):
    def __init__(self, *a, **k):
        super().__init__(*a, **k); self._pages = []
    def showPage(self):
        self._pages.append(dict(self.__dict__)); self._startPage()
    def save(self):
        n = len(self._pages)
        for st in self._pages:
            self.__dict__.update(st); self._draw(n); super().showPage()
        super().save()
    def _draw(self, n):
        self.setFont('Helvetica', 7.2); self.setFillColor(MUTED)
        self.drawRightString(landscape(letter)[0] - 34, 22, f'{self._pageNumber} of {n}')
        self.drawString(34, 22, 'Sunny Home Services, developer handoff')


def chrome(canv, doc):
    w, h = landscape(letter)
    canv.setFillColor(SKY_D); canv.rect(0, h - 26, w, 26, stroke=0, fill=1)
    canv.setFillColor(GOLD);  canv.rect(0, h - 29, w, 3, stroke=0, fill=1)


def esc(t):
    return (str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def main():
    rows = list(csv.reader(open(CSV, encoding='utf-8')))
    hi = next(i for i, r in enumerate(rows) if r and r[0] == 'Page Name')
    header = rows[hi]
    body = [r for r in rows[hi+1:] if r and r[0] and r[0] != 'REVISION LOG']
    body = [r for r in body if len(r) == len(header)]
    meta = {r[0]: (r[1] if len(r) > 1 else '') for r in rows[:hi] if r}
    revs = []
    for i, r in enumerate(rows):
        if r and r[0] == 'REVISION LOG':
            revs = [x for x in rows[i+2:] if x and len(x) >= 3]
            break

    out = os.path.join(ROOT, 'tools', 'page-log.pdf')
    doc = SimpleDocTemplate(out, pagesize=landscape(letter),
                            leftMargin=34, rightMargin=34, topMargin=40, bottomMargin=34,
                            title='Sunny Home Services page log',
                            author='Ad Leverage')
    W = doc.width
    F = []

    # ---------------- page 1: summary, what is waiting, how to run it
    F.append(Paragraph('Sunny Home Services, developer handoff', H1))
    F.append(Paragraph(
        f"Packaged {meta.get('Generated', '')}. "
        f"Preview: {esc('https://sunny-home-services.vercel.app')} &nbsp;&middot;&nbsp; "
        f"Live site: {esc('https://sunnyhomeservices.com')}", SUB))
    F.append(Spacer(1, 12))

    counts = [(r[0].strip(), r[1]) for r in rows[:hi]
              if r and len(r) > 1 and r[0].strip() and r[1].isdigit()]
    cw = (W - 18) / 2.0
    tiles = [[Paragraph(f'<b><font size="15" color="#0288a8">{v}</font></b><br/>'
                        f'<font size="8" color="#6B7480">{esc(k)}</font>', BODY)
              for k, v in counts[i:i+3]] for i in range(0, len(counts), 3)]
    for trow in tiles:
        while len(trow) < 3: trow.append('')
        t = Table([trow], colWidths=[W/3.0]*3)
        t.setStyle(TableStyle(PAD + [('VALIGN', (0,0), (-1,-1), 'TOP'),
                                     ('BOTTOMPADDING', (0,0), (-1,-1), 9)]))
        F.append(t)
    F.append(Spacer(1, 4))

    F.append(Paragraph('What is waiting on a decision', H2))
    openrows = [r for r in body if r[9].startswith('Client')]
    data = [[Paragraph('Page', HEADC), Paragraph('What it is', HEADC),
             Paragraph('Who decides', HEADC)]]
    for r in openrows:
        data.append([Paragraph(f'<b>{esc(r[0])}</b>', CELL),
                     Paragraph(esc(r[8]), CELL),
                     Paragraph(esc(r[9]), CELLM)])
    t = Table(data, colWidths=[W*0.20, W*0.58, W*0.22], repeatRows=1)
    t.setStyle(TableStyle(PAD + [
        ('BACKGROUND', (0,0), (-1,0), SKY_D),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBELOW', (0,0), (-1,-1), 0.4, LINE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, TINT]),
        ('TOPPADDING', (0,1), (-1,-1), 4), ('BOTTOMPADDING', (0,1), (-1,-1), 4)]))
    F.append(t)

    F.append(Paragraph('Running it', H2))
    F.append(Paragraph(
        'No build step and nothing to install. Open <b>HTMLs/home-page.html</b> in a '
        'browser, or serve the folder: <font face="Courier">cd HTMLs &amp;&amp; '
        'python3 -m http.server 8000</font>. To deploy, point a static host at '
        '<b>HTMLs/</b>. <b>vercel.json</b> is already set up: clean URLs, so '
        '/plumber serves plumber.html, and the root serves the home page.', BODY))
    F.append(Paragraph(
        'There is deliberately no index.html. The home page is <b>home-page.html</b>, '
        'named for what it is. Every link between pages is relative, so keep the file '
        'names as they are.', BODY))
    F.append(Paragraph(
        'The header and the footer are identical on all 114 pages. If you are '
        'rebuilding this in WordPress, that is the piece to carry over first: header '
        'and footer are one shared layout, and each page supplies only its own '
        'sections.', BODY))

    F.append(PageBreak())

    # ---------------- page 2: revision log
    F.append(Paragraph('What changed, most recent first', H1))
    F.append(Spacer(1, 8))
    data = [[Paragraph('Date', HEADC), Paragraph('Area', HEADC),
             Paragraph('What changed', HEADC)]]
    for d, a, txt in [(r[0], r[1], r[2]) for r in revs]:
        data.append([Paragraph(esc(d), CELL), Paragraph(f'<b>{esc(a)}</b>', CELLB),
                     Paragraph(esc(txt), CELL)])
    t = Table(data, colWidths=[W*0.13, W*0.15, W*0.72], repeatRows=1)
    t.setStyle(TableStyle(PAD + [
        ('BACKGROUND', (0,0), (-1,0), SKY_D),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBELOW', (0,0), (-1,-1), 0.4, LINE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, TINT]),
        ('TOPPADDING', (0,1), (-1,-1), 5), ('BOTTOMPADDING', (0,1), (-1,-1), 5)]))
    F.append(t)

    F.append(PageBreak())

    # ---------------- page 3 onward: every page
    F.append(Paragraph('Every page in this package', H1))
    F.append(Paragraph('Menu, page, the file that holds it, and where it lives on the '
                       'client site today.', SUB))
    F.append(Spacer(1, 8))

    cols = ['#', 'Page', 'Menu', 'Under', 'Status', 'HTML file',
            'Live page today', 'Copy from', 'Needs a decision']
    widths = [W*0.025, W*0.15, W*0.065, W*0.065, W*0.065, W*0.145,
              W*0.145, W*0.11, W*0.23]
    data = [[Paragraph('#', HEADN)] + [Paragraph(c, HEADC) for c in cols[1:]]]
    style = [('BACKGROUND', (0,0), (-1,0), SKY_D),
             ('VALIGN', (0,0), (-1,-1), 'TOP'),
             ('LINEBELOW', (0,0), (-1,-1), 0.35, LINE)] + PAD
    for i, r in enumerate(body, 1):
        bg, fg = STATUS.get(r[3], (colors.white, INK))
        st = ParagraphStyle(name=f's{i}', parent=CELL, textColor=fg,
                            fontName='Helvetica-Bold', fontSize=6.1, leading=7.3)
        live = r[6]
        live_s = live.replace('https://sunnyhomeservices.com', '') if live.startswith('http') else live
        data.append([
            Paragraph(str(i), NUM),
            Paragraph(f'<b>{esc(r[0])}</b>', CELL),
            Paragraph(esc(r[1]), CELLM),
            Paragraph(esc(r[2]), CELLM),
            Paragraph(esc(r[3]), st),
            Paragraph(f'<font face="Courier" size="5.9">{esc(r[4])}</font>', CELL),
            Paragraph(f'<font size="6">{esc(live_s)}</font>', CELLM),
            Paragraph(esc(r[7]), CELLM),
            Paragraph(esc(r[8]), CELLM),
        ])
        style.append(('BACKGROUND', (4, i), (4, i), bg))
        if i % 2 == 0:
            style.append(('BACKGROUND', (0, i), (3, i), TINT))
            style.append(('BACKGROUND', (5, i), (-1, i), TINT))
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle(style))
    F.append(t)

    doc.build(F, onFirstPage=chrome, onLaterPages=chrome, canvasmaker=Numbered)
    print(out)

if __name__ == '__main__':
    main()
