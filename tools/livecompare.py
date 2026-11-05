#!/usr/bin/env python3
"""
Compares every built page against the live page of the same name.

The page log needs an honest answer to one question per page: does the live
site already say what this build says, or does the live page have to be
updated. This measures it rather than guessing, and writes tools/vs-live.json
for pagelog.py to read.

Run:  python3 tools/livecompare.py          (uses a local cache if present)
      python3 tools/livecompare.py --fetch  (re-downloads the live pages)
"""
import sys, os, re, json, html, difflib, time, urllib.request

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import pagelog as P

CACHE = os.path.join(ROOT, 'tools', '.live-cache')
OUT   = os.path.join(ROOT, 'tools', 'vs-live.json')
UA    = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36'}

DROP = re.compile(r'<(script|style|noscript|svg|head)\b.*?</\1>', re.S | re.I)
TAG  = re.compile(r'<[^>]+>')


def words(h):
    """The words a reader actually sees, normalized so quotes and non-breaking
    spaces do not read as differences."""
    h = TAG.sub(' ', DROP.sub(' ', h))
    h = html.unescape(h).replace(' ', ' ')
    h = re.sub(r'[‘’]', "'", h)
    h = re.sub(r'[“”]', '"', h)
    return [w for w in re.split(r'\s+', h.lower()) if w]


def fetch():
    os.makedirs(CACHE, exist_ok=True)
    got = 0
    for slug, path in sorted(P.LIVE_URL.items()):
        dest = os.path.join(CACHE, slug)
        if os.path.exists(dest) and os.path.getsize(dest) > 2000:
            continue
        try:
            req = urllib.request.Request(P.LIVE + path, headers=UA)
            with urllib.request.urlopen(req, timeout=40) as r:
                open(dest, 'wb').write(r.read())
            got += 1
        except Exception as e:
            print('could not fetch', slug, e)
        time.sleep(0.35)
    print(f'  downloaded {got} live pages')


def main():
    if '--fetch' in sys.argv or not os.path.isdir(CACHE):
        fetch()
    out = {}
    for slug in sorted(P.LIVE_URL):
        ours_p, live_p = os.path.join(ROOT, slug), os.path.join(CACHE, slug)
        if not (os.path.exists(ours_p) and os.path.exists(live_p)):
            continue
        a = words(open(ours_p, encoding='utf-8', errors='replace').read())
        b = words(open(live_p, encoding='utf-8', errors='replace').read())
        sm = difflib.SequenceMatcher(None, b, a, autojunk=False)
        ours_only = live_only = 0
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag in ('replace', 'insert'): ours_only += j2 - j1
            if tag in ('replace', 'delete'): live_only += i2 - i1
        out[slug] = {'same': round(sm.ratio(), 4),
                     'ours_only': ours_only, 'live_only': live_only,
                     'ours_words': len(a), 'live_words': len(b)}
    json.dump(out, open(OUT, 'w'), indent=1, sort_keys=True)
    n = len(out)
    differ = sum(1 for v in out.values() if v['ours_only'] or v['live_only'])
    print(f'{OUT}  ({n} compared, {differ} differ from live)')
    return out


if __name__ == '__main__':
    main()
