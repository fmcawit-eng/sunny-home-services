#!/usr/bin/env python3
"""
The two PDFs for the landing page package: the log and the URL map.

Reads the same pagelog.csv and urlmap.csv as everything else, so none of these
documents can disagree with each other.

Run:  python3 tools/pagelog.py && python3 tools/lppackage.py && python3 tools/lppdf.py
"""
import os, sys, datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph,
                                Spacer, PageBreak)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lppackage as L

ROOT  = L.ROOT
STAMP = L.STAMP
DATE  = L.DATE

SKY_D  = colors.HexColor('#0288a8')
ORANGE = colors.HexColor('#F17601')
INK    = colors.HexColor('#454545')
MUTED  = colors.HexColor('#6B7480')
LINE   = colors.HexColor('#DBE3E6')
TINT   = colors.HexColor('#F3FBFE')
GOLD   = colors.HexColor('#FFC704')

S = lambda **k: ParagraphStyle(**dict({'alignment': TA_LEFT}, **k))
H1   = S(name='H1', fontName='Helvetica-Bold', fontSize=19, leading=23, textColor=SKY_D)
H2   = S(name='H2', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=SKY_D,
         spaceBefore=12, spaceAfter=5)
SUB  = S(name='SUB', fontName='Helvetica', fontSize=9.5, leading=13, textColor=MUTED)
BODY = S(name='BODY', fontName='Helvetica', fontSize=9, leading=12.5, textColor=INK)
CELL = S(name='CELL', fontName='Helvetica', fontSize=8, leading=10.2, textColor=INK)
CELLM= S(name='CELLM', fontName='Helvetica', fontSize=7.8, leading=10, textColor=MUTED)
CELLB= S(name='CELLB', fontName='Helvetica-Bold', fontSize=8, leading=10.2, textColor=SKY_D)
HEADC= S(name='HEADC', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white)
PAD = [('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
       ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6)]

esc = lambda t: str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


class Numbered(canvas.Canvas):
    def __init__(self, *a, **k):
        super().__init__(*a, **k); self._pages = []
    def showPage(self):
        self._pages.append(dict(self.__dict__)); self._startPage()
    def save(self):
        n = len(self._pages)
        for p in self._pages:
            self.__dict__.update(p); self._foot(n); super().showPage()
        super().save()
    def _foot(self, n):
        self.setFont('Helvetica', 7.5); self.setFillColor(MUTED)
        self.drawString(34, 22, self._title_text)
        self.drawRightString(self._pagesize[0] - 34, 22,
                             f'{self._pageNumber} of {n}')


def chrome(c, d):
    w, h = c._pagesize
    c.setFillColor(SKY_D); c.rect(0, h - 26, w, 26, stroke=0, fill=1)
    c.setFillColor(GOLD);  c.rect(0, h - 30, w, 4, stroke=0, fill=1)


def build(out, title, flow):
    Numbered._title_text = title
    doc = SimpleDocTemplate(out, pagesize=landscape(letter), leftMargin=34,
                            rightMargin=34, topMargin=44, bottomMargin=34,
                            title=title, author='Ad Leverage')
    doc.build(flow, onFirstPage=chrome, onLaterPages=chrome, canvasmaker=Numbered)
    print(out)
    return doc


def tiles(W, pairs):
    out = []
    for i in range(0, len(pairs), 3):
        row = [Paragraph(f'<b><font size="15" color="#0288a8">{v}</font></b><br/>'
                         f'<font size="8" color="#6B7480">{esc(k)}</font>', BODY)
               for k, v in pairs[i:i+3]]
        while len(row) < 3: row.append('')
        t = Table([row], colWidths=[W/3.0]*3)
        t.setStyle(TableStyle(PAD + [('VALIGN', (0,0), (-1,-1), 'TOP'),
                                     ('BOTTOMPADDING', (0,0), (-1,-1), 9)]))
        out.append(t)
    return out


def main():
    pkg, assets, links, head, body, revs, mine, theirs = L.main()
    SRC = os.path.join(pkg, 'HTMLs', '_source')
    W = landscape(letter)[0] - 68

    # ---------------------------------------------- the log
    F = [Paragraph(L.HEADING, H1),
         Paragraph(f'Packaged {DATE}. {L.BLURB} Every address in the Link column hangs off '
                   f'https://sunny-home-services.vercel.app, and every address in the '
                   f'Live column off {L.LIVE}.', SUB),
         Spacer(1, 12)]
    one = len(L.PAGES) == 1
    F += tiles(W, [('Landing page in this package' if one else
                    'Landing pages in this package', str(len(L.PAGES))),
                   ('Files it loads (images, fonts, CSS, script)' if one else
                    'Files they load (images, fonts, CSS, script)', str(len(assets))),
                   ('Pages its header and footer link to' if one else
                    'Pages their header and footer link to', str(len(links))),
                   ('Finished, not live yet' if one else
                    'All four, live page needs updating', str(len(body))),
                   ('Waiting on the client', str(sum(1 for r in body if r[9].strip()))),
                   ('Rounds of work on it today' if one else
                    'Rounds of work on them today', str(len(revs)))])
    F.append(Spacer(1, 6))
    F.append(Paragraph('The page' if one else 'The four pages', H2))

    cols = ['Page', 'Status', 'Link on the preview', 'HTML file',
            'Live page today', 'How it differs from the live page', 'Note']
    widths = [W*0.095, W*0.065, W*0.145, W*0.150, W*0.100, W*0.135, W*0.310]
    data = [[Paragraph(c, HEADC) for c in cols]]
    style = [('BACKGROUND', (0,0), (-1,0), SKY_D), ('VALIGN', (0,0), (-1,-1), 'TOP'),
             ('LINEBELOW', (0,0), (-1,-1), 0.35, LINE)] + PAD
    for i, r in enumerate(body, 1):
        live = r[6].replace(L.LIVE, '') if r[6].startswith('http') else r[6]
        prev = r[5].replace('https://sunny-home-services.vercel.app', '') or '/'
        st = ParagraphStyle(name=f's{i}', parent=CELL, textColor=ORANGE,
                            fontName='Helvetica-Bold', fontSize=7.4, leading=9)
        data.append([Paragraph(f'<b>{esc(r[0])}</b>', CELL),
                     Paragraph(esc(r[3]), st),
                     Paragraph(f'<font face="Courier" size="6.6">{esc(prev)}</font>', CELL),
                     Paragraph(f'<font face="Courier" size="6.6">{esc(r[4])}</font>', CELL),
                     Paragraph(f'<font size="7.4">{esc(live)}</font>', CELLM),
                     Paragraph(esc(r[8]), CELLM),
                     Paragraph(esc(r[9]), CELLM)])
        if i % 2 == 0:
            style.append(('BACKGROUND', (0, i), (-1, i), TINT))
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle(style)); F.append(t)

    if revs:
        F.append(PageBreak())
        F.append(Paragraph('What changed, newest first', H1))
        F.append(Paragraph(
            f'Every round of work on this page. {len(revs)} entries.' if one
            else f'Every round of work on these four pages. {len(revs)} entries.', SUB))
        F.append(Spacer(1, 10))
        rd = [[Paragraph('Date', HEADC), Paragraph('What', HEADC),
               Paragraph('What changed', HEADC)]]
        rs = [('BACKGROUND', (0,0), (-1,0), SKY_D), ('VALIGN', (0,0), (-1,-1), 'TOP'),
              ('LINEBELOW', (0,0), (-1,-1), 0.35, LINE)] + PAD
        for i, r in enumerate(revs, 1):
            rd.append([Paragraph(esc(r[0]), CELLM),
                       Paragraph(esc(r[1]), CELLB),
                       Paragraph(esc(r[2]), CELL)])
            if i % 2 == 0:
                rs.append(('BACKGROUND', (0, i), (-1, i), TINT))
        rt = Table(rd, colWidths=[W*0.10, W*0.17, W*0.73], repeatRows=1)
        rt.setStyle(TableStyle(rs)); F.append(rt)

    log_pdf = os.path.join(pkg, f'Sunny Home Services {L.LABEL} log - {STAMP}.pdf')
    build(log_pdf, L.HEADING, F)
    shutil.copy2 = __import__('shutil').copy2

    # ---------------------------------------------- the URL map, two columns
    F = [Paragraph(f'Sunny Home Services, {L.LABEL} URL map', H1),
         Paragraph(f'{DATE}. Each HTML file and the address it goes live at. '
                   + ('This package\u2019s page is at the top. Under it, every page its '
                      'header and footer link to, ' if one else
                      'The four landing pages are at the top. Under them, every page their '
                      'header and footer link to, ')
                   + f'so you know where each link lands. The '
                   f'addresses in orange have no live page yet, so they need a yes from '
                   f'dev before they are used.', SUB),
         Spacer(1, 12)]
    URL_NEW = S(name='URL_NEW', fontName='Helvetica-Bold', fontSize=8, leading=10.2,
                textColor=colors.HexColor('#C25A00'))
    for heading, rows in ((('This page' if one else 'The four landing pages'), mine),
                          (('Pages it links to' if one else 'Pages they link to'), theirs)):
        F.append(Paragraph(heading, H2))
        d = [[Paragraph('HTML file', HEADC), Paragraph('URL', HEADC)]]
        st = [('BACKGROUND', (0,0), (-1,0), SKY_D), ('VALIGN', (0,0), (-1,-1), 'TOP'),
              ('GRID', (0,0), (-1,-1), 0.4, LINE)] + PAD
        for i, (f, u) in enumerate(rows, 1):
            new = f in NEWSET
            d.append([Paragraph(f'<font face="Courier" size="7.6">{esc(f)}</font>', CELL),
                      Paragraph(esc(u), URL_NEW if new else CELLB)])
            if i % 2 == 0:
                st.append(('BACKGROUND', (0, i), (-1, i), TINT))
        t = Table(d, colWidths=[W*0.38, W*0.62], repeatRows=1)
        t.setStyle(TableStyle(st)); F.append(t)

    map_pdf = os.path.join(SRC, f'Sunny Home Services {L.LABEL} URL map - {STAMP}.pdf')
    build(map_pdf, f'Sunny Home Services, {L.LABEL} URL map', F)
    return pkg


# Which files have no live page yet. Read off the page log's Status column
# rather than guessed: BUILT, NEW is the status for a page with no live
# counterpart, so its address is a proposal until dev says yes.
import csv as _csv
_rows = list(_csv.reader(open(os.path.join(ROOT, 'tools', 'pagelog.csv'), encoding='utf-8')))
_hi = next(i for i, r in enumerate(_rows) if r and r[0] == 'Page Name')
_h = _rows[_hi]
_fi, _si = _h.index('HTML File'), _h.index('Status')
NEWSET = {r[_fi] for r in _rows[_hi + 1:]
          if r and len(r) == len(_h) and r[_si] == 'BUILT, NEW'}

if __name__ == '__main__':
    import shutil
    main()
