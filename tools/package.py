#!/usr/bin/env python3
"""
Assembles the developer package and zips it.

  <client>-home-page-MM-DD-YYYY/
    <Client> page log - MM-DD-YYYY.pdf
    HTMLs/                 the site as it deploys, home-page.html, vercel.json
      _source/             read me, build notes, the page log as a spreadsheet,
                           and the Python that built the generated pages

Run:  python3 tools/pagelog.py && python3 tools/handoff_pdf.py && python3 tools/package.py
"""
import os, re, shutil, subprocess, datetime, glob, sys

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today()
STAMP = TODAY.strftime('%m-%d-%Y')
NAME  = f'sunny-home-services-home-page-{STAMP}'
DIST  = os.path.join(ROOT, 'dist')
PKG   = os.path.join(DIST, NAME)
SITE  = os.path.join(PKG, 'HTMLs')
SRC   = os.path.join(SITE, '_source')

# trailingSlash must stay off. Every stylesheet, script and image path in these
# pages is relative, so a trailing slash makes the browser resolve them one
# folder deep ("/millcreek-ut/css/...") and the page loads unstyled.
VERCEL = '''{
  "cleanUrls": true,
  "rewrites": [
    { "source": "/", "destination": "/home-page" }
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

def main():
    if os.path.isdir(PKG):
        shutil.rmtree(PKG)
    os.makedirs(SRC, exist_ok=True)

    # ---- the site itself
    for f in glob.glob(os.path.join(ROOT, '*.html')):
        shutil.copy2(f, SITE)
    for d in ('assets', 'css', 'js'):
        shutil.copytree(os.path.join(ROOT, d), os.path.join(SITE, d))

    # the home page is named for what it is
    os.rename(os.path.join(SITE, 'index.html'), os.path.join(SITE, 'home-page.html'))
    n = 0
    for f in glob.glob(os.path.join(SITE, '*.html')):
        s = open(f, encoding='utf-8').read()
        if 'index.html' in s:
            n += s.count('index.html')
            open(f, 'w', encoding='utf-8').write(s.replace('index.html', 'home-page.html'))
    print(f'  home-page.html, {n} links repointed')

    open(os.path.join(SITE, 'vercel.json'), 'w').write(VERCEL)

    # ---- the source folder
    shutil.copy2(os.path.join(ROOT, 'tools', 'pagelog.csv'),
                 os.path.join(SRC, f'Sunny Home Services page log - {STAMP}.csv'))
    tools_out = os.path.join(SRC, 'build-tools')
    os.makedirs(tools_out, exist_ok=True)
    for f in glob.glob(os.path.join(ROOT, 'tools', '*')):
        if os.path.isfile(f) and not f.endswith(('.pdf',)):
            shutil.copy2(f, tools_out)
    shutil.copytree(os.path.join(ROOT, 'tools', 'docs'),
                    os.path.join(tools_out, 'docs'))

    # ---- the URL map: two columns, the HTML file and the address it goes live at.
    # The PDF only. Dev asked for one short sheet, not a second spreadsheet.
    urlmap = os.path.join(ROOT, 'tools', 'url-map.pdf')
    if os.path.exists(urlmap):
        shutil.copy2(urlmap, os.path.join(SRC, f'Sunny Home Services URL map - {STAMP}.pdf'))

    # ---- the two documents that explain it. These live in the repo at
    # tools/docs/ so a package can be rebuilt months from now.
    DOCS = os.path.join(ROOT, 'tools', 'docs')
    # {DATE} and {STAMP} in those files are filled in here, so a doc written
    # months ago cannot still be naming last package's date.
    stamps = {'{DATE}': TODAY.strftime('%B %-d, %Y'), '{STAMP}': STAMP}
    for src_name, out_name in (('READ_ME_FIRST.md', 'READ ME FIRST.md'),
                               ('BUILD_NOTES.md', 'BUILD NOTES.md')):
        txt = open(os.path.join(DOCS, src_name), encoding='utf-8').read()
        for k, v in stamps.items():
            txt = txt.replace(k, v)
        open(os.path.join(SRC, out_name), 'w', encoding='utf-8').write(txt)

    # ---- the page log, at the top where it is seen first
    pdf = os.path.join(ROOT, 'tools', 'page-log.pdf')
    shutil.copy2(pdf, os.path.join(PKG, f'Sunny Home Services page log - {STAMP}.pdf'))

    return PKG

if __name__ == '__main__':
    pkg = main()
    print(' ', pkg)
