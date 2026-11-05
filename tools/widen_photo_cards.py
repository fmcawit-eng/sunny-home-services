#!/usr/bin/env python3
"""
Lifts a grid of photograph cards out of the narrow heading rail onto the full
column, and gives it a column count that lands the set in at most two rows.

The cards keep their photographs. Only the wrapper and the column count change.
"""
import re, os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cards_to_tiles import match_div

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def columns(n):
    if n <= 4:
        return n
    return min(4, -(-n // 2))


def convert(sec):
    if 'hub-card-media' not in sec or 'hub-rail' not in sec:
        return None
    gm = re.search(r'<div class="hub-cards[^"]*">', sec)
    if not gm:
        return None
    gend = match_div(sec, gm.start())
    inner = sec[gm.end():gend - 6]
    n = len(re.findall(r'<(?:div|a) class="hub-card[ "]', inner))
    if not n:
        return None
    per = columns(n)
    gap = (-n) % per
    if gap == 1:                       # close a short last row
        last = list(re.finditer(r'<(?:div|a) class="hub-card([ ][^"]*)?"', inner))[-1]
        cls = last.group(1) or ''
        inner = inner[:last.start()] + last.group(0).replace(
            f'class="hub-card{cls}"', f'class="hub-card{cls} is-wide"') + inner[last.end():]

    h2m = re.search(r'<h2 class="display-h2[^>]*>(.*?)</h2>', sec, re.S)
    if not h2m:
        return None
    before, after = sec[:gm.start()], sec[gend:]
    lead = re.findall(r'<div class="hub-prose[^"]*"[^>]*>(.*?)</div>', before, re.S)
    lead_html = ''
    if lead:
        paras = re.findall(r'<p>(.*?)</p>', lead[-1], re.S)
        if paras:
            lead_html = f'      <p class="hub-lead-in reveal" data-animation="fade-up">{paras[0].strip()}</p>\n'
            lead_html += ''.join(f'      <p>{p.strip()}</p>\n' for p in paras[1:])
    tail = ''.join('      ' + m.group(0).strip() + '\n'
                   for m in re.finditer(r'<div class="hub-prose[^"]*"[^>]*>.*?</div>', after, re.S))

    opening = re.match(r'(<section[^>]*>)\s*(<div class="section-bg[^>]*>.*?</div>)?', sec, re.S)
    return (opening.group(0).rstrip() +
            '\n    <div class="container">\n'
            f'      <h2 class="display-h2 reveal" data-animation="fade-up">{h2m.group(1).strip()}</h2>\n'
            f'{lead_html}'
            f'      <div class="hub-cards hub-cards-{per}">{inner}\n      </div>\n'
            f'{tail}'
            '    </div>\n  </section>')


def main():
    total, pages = 0, []
    for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        if os.path.basename(f).startswith('blog'):
            continue
        s = open(f, encoding='utf-8').read()
        hits = []
        for m in re.finditer(r'<section[^>]*data-block="hub-cards"[^>]*>.*?\n  </section>', s, re.S):
            new = convert(m.group(0))
            if new:
                hits.append((m.start(), m.end(), new))
        if not hits:
            continue
        for a, b, new in reversed(hits):
            s = s[:a] + new + s[b:]
        open(f, 'w', encoding='utf-8').write(s)
        pages.append((os.path.basename(f), len(hits)))
        total += len(hits)
    print(f'lifted {total} photo grids on {len(pages)} pages')
    for f, n in pages:
        print(f'   {f:40} {n}')


if __name__ == '__main__':
    main()
