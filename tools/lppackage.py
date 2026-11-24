#!/usr/bin/env python3
"""
A landing page package: the pages, everything they need to run, and the two
documents that explain them.

  sunny-home-services-<set>-MM-DD-YYYY/
    Sunny Home Services <set> log - MM-DD-YYYY.pdf
    HTMLs/            the pages, the stylesheets, the script, their images
      _source/        read me, build notes, the log as a spreadsheet, the URL
                      map, and the Python that builds the pages

Two sets are defined below. Pass the one you want:

  python3 tools/pagelog.py && python3 tools/lppdf.py landing-pages
  python3 tools/pagelog.py && python3 tools/lppdf.py heating-services

lppdf.py assembles the folder and renders both PDFs, so that is the one to
run. This file on its own writes the folder without them.
"""
import csv, os, re, json, shutil, glob, sys, datetime

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today()
STAMP = TODAY.strftime('%m-%d-%Y')
DATE  = TODAY.strftime('%B %-d, %Y')
DIST  = os.path.join(ROOT, 'dist')
LIVE  = 'https://sunnyhomeservices.com'

# The root of a package has no home page in it, so it opens on the page named
# as "root" below. That is a convenience for the preview link, not a decision
# about the site. trailingSlash stays off: every asset path is relative.
PRESETS = {
    'landing-pages': dict(
        label='ad landing pages',
        heading='Sunny Home Services, ad landing pages',
        blurb='The four pages the ads point at, rebuilt in the site design.',
        pages=['furnace-repair-experts.html', 'furnace-replacement-experts.html',
               'ac-repair-experts.html', 'ac-replacement-experts.html'],
        root='furnace-repair-experts',
        docs=('LP_READ_ME_FIRST.md', 'LP_BUILD_NOTES.md'),
        builder='expertslp.py',
    ),
    'heating-services': dict(
        label='heating services landing page',
        heading='Sunny Home Services, heating services landing page',
        blurb='The general heating landing page, built from the client\u2019s copy doc.',
        pages=['heating-services.html'],
        root='heating-services',
        docs=('HS_READ_ME_FIRST.md', 'HS_BUILD_NOTES.md'),
        builder='heatinglp.py',
    ),
}

KIND = next((a for a in sys.argv[1:] if a in PRESETS), 'landing-pages')
P = PRESETS[KIND]
LABEL, HEADING, BLURB = P['label'], P['heading'], P['blurb']
PAGES, BUILDER = P['pages'], P['builder']
NAME = f'sunny-home-services-{KIND}-{STAMP}'
PKG  = os.path.join(DIST, NAME)
SITE = os.path.join(PKG, 'HTMLs')
SRC  = os.path.join(SITE, '_source')

VERCEL = '''{
  "cleanUrls": true,
  "rewrites": [
    { "source": "/", "destination": "/''' + P['root'] + '''" }
  ],
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
'''

ATTR = re.compile(r'(?:href|src|srcset|poster|data-src|content)\s*=\s*"([^"]+)"', re.I)
URLF = re.compile(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)')


def referenced():
    """Every file these pages actually load, found by reading them, then the
    stylesheets they load, then the script. Nothing is matched by file name."""
    need, out_links = set(), set()

    def add(u, base=''):
        u = u.strip().split('#')[0].split('?')[0]
        if not u or u.startswith(('http', '//', 'mailto:', 'tel:', 'data:', 'javascript:')):
            return
        p = os.path.normpath(os.path.join(base, u))
        if p.endswith('.html'):
            out_links.add(os.path.basename(p))
            return
        if os.path.isfile(os.path.join(ROOT, p)):
            need.add(p)

    for f in PAGES:
        s = open(os.path.join(ROOT, f), encoding='utf-8').read()
        for raw in ATTR.findall(s):
            for part in raw.split(','):
                add(part.strip().split(' ')[0])
        for u in URLF.findall(s):
            add(u)

    for c in sorted(p for p in list(need) if p.endswith('.css')):
        s = open(os.path.join(ROOT, c), encoding='utf-8').read()
        for u in URLF.findall(s):
            add(u, os.path.dirname(c))

    for j in sorted(p for p in list(need) if p.endswith('.js')):
        s = open(os.path.join(ROOT, j), encoding='utf-8').read()
        for u in re.findall(r'["\']((?:assets|css|js)/[^"\']+)["\']', s):
            add(u)

    return sorted(need), sorted(out_links)


def log_rows():
    """These pages' rows out of the full page log, so the two cannot disagree."""
    rows = list(csv.reader(open(os.path.join(ROOT, 'tools', 'pagelog.csv'), encoding='utf-8')))
    hi = next(i for i, r in enumerate(rows) if r and r[0] == 'Page Name')
    head = rows[hi]
    body = [r for r in rows[hi + 1:] if r and len(r) == len(head) and r[4] in PAGES]
    revs = []
    for i, r in enumerate(rows):
        if r and r[0] == 'REVISION LOG':
            revs = [x for x in rows[i + 2:] if x and len(x) >= 3 and x[0] == DATE]
            break
    return head, sorted(body, key=lambda r: PAGES.index(r[4])), revs


def url_map(out_links):
    """Two columns: the HTML file, and the address it goes live at. This
    package's pages first, then every page their header and footer link to."""
    rows = list(csv.reader(open(os.path.join(ROOT, 'tools', 'urlmap.csv'), encoding='utf-8')))
    hi = next(i for i, r in enumerate(rows) if r and r[0] == 'HTML File')
    by_file = {r[0]: r for r in rows[hi + 1:] if r and r[0]}
    mine, theirs = [], []
    for f in PAGES:
        r = by_file.get(f)
        if r: mine.append((f, r[1]))
    for f in sorted(out_links):
        key = 'home-page.html' if f == 'index.html' else f
        r = by_file.get(key)
        if r: theirs.append((key, r[1]))
    return mine, theirs


def main():
    if os.path.isdir(PKG):
        shutil.rmtree(PKG)
    os.makedirs(SRC, exist_ok=True)

    assets, out_links = referenced()
    for f in PAGES:
        shutil.copy2(os.path.join(ROOT, f), SITE)
    for rel in assets:
        dest = os.path.join(SITE, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(os.path.join(ROOT, rel), dest)
    open(os.path.join(SITE, 'vercel.json'), 'w').write(VERCEL)

    head, body, revs = log_rows()
    mine, theirs = url_map(out_links)

    # the log as a spreadsheet
    with open(os.path.join(SRC, f'Sunny Home Services {LABEL} log - {STAMP}.csv'),
              'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow([HEADING])
        w.writerow(['Generated', DATE, 'Preview', 'https://sunny-home-services.vercel.app',
                    'Live site', LIVE])
        w.writerow([])
        w.writerow(head)
        for r in body:
            w.writerow(r)
        w.writerow([])
        w.writerow(['REVISION LOG'])
        w.writerow(['Date', 'What', 'What changed'])
        for r in revs:
            w.writerow(r[:3])

    # the two documents that explain it. {DATE} and {STAMP} are filled in
    # here, so a doc written months ago cannot still name an older package.
    DOCS = os.path.join(ROOT, 'tools', 'docs')
    stamps = {'{DATE}': DATE, '{STAMP}': STAMP}
    for src_name, out_name in zip(P['docs'], ('READ ME FIRST.md', 'BUILD NOTES.md')):
        txt = open(os.path.join(DOCS, src_name), encoding='utf-8').read()
        for k, v in stamps.items():
            txt = txt.replace(k, v)
        open(os.path.join(SRC, out_name), 'w', encoding='utf-8').write(txt)

    # the build tools these pages come from
    tools_out = os.path.join(SRC, 'build-tools')
    os.makedirs(tools_out, exist_ok=True)
    for f in (BUILDER, 'pagelog.py', 'handoff_pdf.py', 'urlmap.py',
              'lppackage.py', 'lppdf.py', 'widont.py', 'livecompare.py'):
        p = os.path.join(ROOT, 'tools', f)
        if os.path.isfile(p):
            shutil.copy2(p, tools_out)

    return PKG, assets, out_links, head, body, revs, mine, theirs


if __name__ == '__main__':
    pkg, assets, links, head, body, revs, mine, theirs = main()
    print(' ', pkg)
    print('  set', KIND, ' pages', len(PAGES), ' files they load', len(assets),
          ' pages they link to', len(links))
