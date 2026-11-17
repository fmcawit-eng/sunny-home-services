#!/usr/bin/env python3
"""
The URL map: one row per HTML file, with the web address it goes live at.

Reads tools/pagelog.csv, so this and the page log can never disagree. Writes a
spreadsheet and a PDF of the same table.

Run:  python3 tools/pagelog.py && python3 tools/urlmap.py
"""
import csv, os, datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle as S
from reportlab.lib.enums import TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV  = os.path.join(ROOT, 'tools', 'pagelog.csv')
LIVE = 'https://sunnyhomeservices.com'
_TODAY = datetime.date.today()
DATE  = _TODAY.strftime('%B %-d, %Y')
STAMP = _TODAY.strftime('%m-%d-%Y')

# Addresses for the pages with no live page yet. Each one follows a pattern the
# live site already uses, so none of this invents a structure. Dev confirms them.
NEW = {
    'kearns-ut.html':                         ('/kearns-ut/', 'Same shape as the other city pages, like /sandy-ut/.'),
    'millcreek-ut.html':                      ('/millcreek-ut/', 'Same shape as the other city pages, like /sandy-ut/.'),
    'millcreek-ut-heating.html':              ('/millcreek-ut/heating/', 'Same shape as /sandy-ut/heating/.'),
    'millcreek-ut-plumber.html':              ('/millcreek-ut/plumber/', 'Same shape as /sandy-ut/plumber/.'),
    'salt-lake-city-ut-air-conditioning.html':('/salt-lake-city-ut/air-conditioning/', 'Same shape as /sandy-ut/air-conditioning/. The parent /salt-lake-city-ut/ is already live.'),
    'salt-lake-city-ut-heating.html':         ('/salt-lake-city-ut/heating/', 'Same shape as /sandy-ut/heating/. The parent /salt-lake-city-ut/ is already live.'),
    'salt-lake-city-ut-plumber.html':         ('/salt-lake-city-ut/plumber/', 'Same shape as /sandy-ut/plumber/. The parent /salt-lake-city-ut/ is already live.'),
    'whole-house-air-purifier.html':          ('/indoor-air-quality/whole-house-air-purifier/', 'Same shape as /indoor-air-quality/whole-home-humidifiers/.'),
}
NOPUB = {
    'blog-template.html': 'Not a page. Dev duplicates this file to build article 14 and onward.',
    'coming-soon.html':   'A holding page. The four pages still waiting on copy point at it.',
}

HEAD = ['HTML File', 'URL On The Live Site', 'Is That URL Live Now?',
        'Page Name', 'Menu Section', 'Link To Preview It', 'Notes']


def build():
    src = list(csv.reader(open(CSV, encoding='utf-8')))
    hi = next(i for i, r in enumerate(src) if r and r[0] == 'Page Name')
    rows = [r for r in src[hi+1:] if len(r) > 6 and r[4].strip().endswith('.html')]
    out = []
    for x in rows:
        f, name, nav, parent = x[4].strip(), x[0], x[1], x[2]
        prev, live = x[5], x[6].strip()
        section = nav or parent or ''
        if live and live != 'Not live yet':
            url, is_live, note = live, 'Yes', ''
        elif f in NOPUB:
            url, is_live, note = 'No URL. Do not publish.', 'No', NOPUB[f]
        elif f.startswith('blog-'):
            url = LIVE + '/blog/' + f[5:-5] + '/'
            is_live = 'No, new page'
            note = 'Article slug from the client brief. It sits under /blog/, like the live blog index.'
        elif f in NEW:
            url, is_live = LIVE + NEW[f][0], 'No, new page'
            note = NEW[f][1]
        else:
            url, is_live, note = '', 'No, new page', 'Needs a URL decision.'
        out.append([f, url, is_live, name, section, prev, note])
    out.sort(key=lambda r: ('' if r[0] == 'home-page.html' else r[0]))
    return out


SKY_D  = colors.HexColor('#0288a8')
GOLD   = colors.HexColor('#FFC704')
INK    = colors.HexColor('#454545')
MUTED  = colors.HexColor('#6B7480')
LINE   = colors.HexColor('#DBE3E6')
TINT   = colors.HexColor('#F3FBFE')
AMBER  = colors.HexColor('#8a5a00')

H1    = S(name='H1', fontName='Helvetica-Bold', fontSize=19, leading=23, textColor=SKY_D)
SUB   = S(name='SUB', fontName='Helvetica', fontSize=9.5, leading=13, textColor=MUTED)
BODY  = S(name='BODY', fontName='Helvetica', fontSize=9, leading=12.5, textColor=INK, spaceAfter=5)
CELL  = S(name='CELL', fontName='Helvetica', fontSize=7.4, leading=9, textColor=INK)
CELLM = S(name='CELLM', fontName='Helvetica', fontSize=7.4, leading=9, textColor=MUTED)
CELLB = S(name='CELLB', fontName='Helvetica-Bold', fontSize=7.4, leading=9, textColor=SKY_D)
NUM   = S(name='NUM', fontName='Helvetica', fontSize=6.1, leading=8,
          textColor=colors.HexColor('#9aa8b0'), alignment=TA_RIGHT)
HEADC = S(name='HEADC', fontName='Helvetica-Bold', fontSize=7.6, leading=9.2, textColor=colors.white)
HEADN = S(name='HEADN', fontName='Helvetica-Bold', fontSize=6.9, leading=8.4,
          textColor=colors.HexColor('#CFEFF8'), alignment=TA_RIGHT)


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
        self.drawRightString(letter[0] - 42, 22, f'{self._pageNumber} of {n}')
        self.drawString(42, 22, 'Sunny Home Services, URL map')


def chrome(canv, doc):
    w, h = letter
    canv.setFillColor(SKY_D); canv.rect(0, h - 26, w, 26, stroke=0, fill=1)
    canv.setFillColor(GOLD);  canv.rect(0, h - 29, w, 3, stroke=0, fill=1)


def esc(t):
    return str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def main():
    data = build()
    out_csv = os.path.join(ROOT, 'tools', 'urlmap.csv')
    with open(out_csv, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['HTML File', 'URL'])
        w.writerows([[r[0], r[1]] for r in data])

    out_pdf = os.path.join(ROOT, 'tools', 'url-map.pdf')
    doc = SimpleDocTemplate(out_pdf, pagesize=letter,
                            leftMargin=42, rightMargin=42, topMargin=46, bottomMargin=36,
                            title='Sunny Home Services URL map', author='Ad Leverage')
    W = doc.width
    new = sum(1 for r in data if r[2].startswith('No,'))
    st = [Paragraph('Sunny Home Services, URL Map', H1),
          Paragraph(f'{DATE}. Each HTML file in the handoff package and the address '
                    f'it goes live at. The {new} shown in orange have no live page yet, '
                    f'so that address needs a yes from dev before it is used.', SUB),
          Spacer(1, 14)]

    tbl = [[Paragraph('HTML file', HEADC), Paragraph('URL', HEADC)]]
    style = [('BACKGROUND', (0, 0), (-1, 0), SKY_D),
             ('VALIGN', (0, 0), (-1, -1), 'TOP'),
             ('TOPPADDING', (0, 0), (-1, -1), 3.5),
             ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
             ('LEFTPADDING', (0, 0), (-1, -1), 6),
             ('RIGHTPADDING', (0, 0), (-1, -1), 6),
             ('GRID', (0, 0), (-1, -1), 0.4, LINE)]
    URL_NEW = S(name='URL_NEW', fontName='Helvetica-Bold', fontSize=7.4,
                leading=9, textColor=colors.HexColor('#C25A00'))
    for i, r in enumerate(data, 1):
        if not r[1].startswith('http'):
            u = Paragraph(esc(r[1]), CELLM)
        else:
            u = Paragraph(esc(r[1]), CELLB if r[2] == 'Yes' else URL_NEW)
        tbl.append([Paragraph(esc(r[0]), CELL), u])
        row = len(tbl) - 1
        if i % 2 == 0:
            style.append(('BACKGROUND', (0, row), (-1, row), TINT))
    t = Table(tbl, colWidths=[W*0.40, W*0.60], repeatRows=1)
    t.setStyle(TableStyle(style))
    st.append(t)

    doc.build(st, onFirstPage=chrome, onLaterPages=chrome, canvasmaker=Numbered)
    print(out_csv)
    print(out_pdf, len(data), 'rows')


if __name__ == '__main__':
    main()
