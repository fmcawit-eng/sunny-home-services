#!/usr/bin/env python3
"""
Turns a photoless card grid into the service tiles used across the site, and
lifts its section out of the narrow heading rail onto the full column.

A card grid with photographs is left alone: the picture is the point there.

Run:  python3 tools/cards_to_tiles.py [--dry]
"""
import re, sys, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = '--dry' in sys.argv

def match_tag(html, start, tag='div'):
    """Index just past the tag that closes the one opening at `start`."""
    o, c = f'<{tag}', f'</{tag}>'
    i, depth = start, 0
    while i < len(html):
        if html.startswith(o, i) and (i + len(o) >= len(html) or html[i + len(o)] in ' >/'):
            depth += 1; i += len(o)
        elif html.startswith(c, i):
            depth -= 1; i += len(c)
            if depth == 0:
                return i
        else:
            i += 1
    return -1


def match_div(html, start):
    return match_tag(html, start, 'div')


def parse_cards(grid_html):
    """Each card as {title, body, href}. The body keeps its paragraphs, its
    bullet lists and every link inside them, so nothing written is lost."""
    cards = []
    for m in re.finditer(r'<(div|a) class="hub-card(?: [^"]*)?"[^>]*>', grid_html):
        tag = m.group(1)
        end = match_tag(grid_html, m.start(), tag)
        if end < 0:
            return []
        card_href = re.search(r'href="([^"]+)"', m.group(0))
        inner = grid_html[m.end():end - (len(tag) + 3)]
        bm = re.search(r'<div class="hub-card-body">', inner)
        if bm:
            bend = match_div(inner, bm.start())
            body = inner[bm.end():bend - 6]
        else:
            body = inner          # some cards hold their content directly
        tm = re.search(r'<(h3|div) class="hub-card-title">(.*?)</\1>', body, re.S)
        if not tm:
            return []
        rest = (body[:tm.start()] + body[tm.end():]).strip()
        if '<img' in rest:
            return []             # a card carrying a picture is not a text tile
        href = card_href.group(1) if card_href else None
        lm = re.search(r'<a class="hub-card-link" href="([^"]+)">.*?</a>', rest, re.S)
        if lm:
            href = href or lm.group(1)
            rest = (rest[:lm.start()] + rest[lm.end():]).strip()
        # a card that was a link carries its label in a span instead
        rest = re.sub(r'<span class="hub-card-link"[^>]*>.*?</span>', '', rest, flags=re.S).strip()
        title = tm.group(2).strip()
        # A title that is nothing but a link means the card's destination was
        # written inside the heading. The tile should carry it, or the link ends
        # up as a 23px tap target inside a heading.
        only_link = re.fullmatch(r'<a href="([^"]+)"[^>]*>(.*?)</a>', title, re.S)
        if only_link:
            href = href or only_link.group(1)
            title = only_link.group(2).strip()
        cards.append({'title': title, 'body': rest, 'href': href})
    return cards


def columns(n):
    """At most two rows, tiles wide enough to read, nothing stranded."""
    if n <= 4:
        return n
    return min(5, -(-n // 2))


def build(cards, per):
    n = len(cards)
    gap = (-n) % per
    out = [f'      <div class="hub-tiles hub-tiles-{per}">']
    for i, c in enumerate(cards):
        wide = ' is-wide' if (gap == 1 and i == n - 1) else ''
        href = c.get('href')
        if href:
            head = f'<a class="hub-tile-title" href="{href}">{c["title"]}</a>'
            foot = f'\n          <a class="hub-tile-go" href="{href}">Learn More &rsaquo;</a>'
            cls = f'hub-tile reveal{wide}'
        else:
            head = f'<span class="hub-tile-title">{c["title"]}</span>'
            foot = ''
            cls = f'hub-tile is-static reveal{wide}'
        out.append(f'        <div class="{cls}" data-animation="fade-up">\n'
                   f'          {head}\n'
                   f'          <div class="hub-tile-desc">{c["body"]}</div>{foot}\n'
                   f'        </div>')
    out.append('      </div>')
    return '\n'.join(out)


def convert_section(sec):
    """Returns the rebuilt section, or None if this one should be left alone."""
    if 'hub-card-media' in sec:
        return None                      # a grid of photographs stays as it is
    gm = re.search(r'<div class="hub-cards[^"]*">', sec)
    if not gm:
        return None
    gend = match_div(sec, gm.start())
    if gend < 0:
        return None

    grid_start, grid_end = gm.start(), gend
    grid_inner = sec[gm.end():gend - 6]
    cards = parse_cards(grid_inner)
    if not cards or len(cards) != len(re.findall(r'<(?:div|a) class="hub-card[ "]', grid_inner)):
        return None                      # shape we do not recognize: do not touch it

    h2m = re.search(r'<h2 class="display-h2[^>]*>(.*?)</h2>', sec, re.S)
    if not h2m:
        return None
    h2 = h2m.group(1).strip()

    # prose before the grid becomes the lead-in; prose after it is kept as it is
    before = sec[:grid_start]
    after = sec[grid_end:]
    lead = re.findall(r'<div class="hub-prose[^"]*"[^>]*>(.*?)</div>', before, re.S)
    lead_html = ''
    if lead:
        paras = re.findall(r'<p>(.*?)</p>', lead[-1], re.S)
        if paras:
            lead_html = f'      <p class="hub-lead-in reveal" data-animation="fade-up">{paras[0].strip()}</p>\n'
            extra = ''.join(f'      <p>{p.strip()}</p>\n' for p in paras[1:])
            lead_html += extra
    tail = ''
    for m in re.finditer(r'<div class="hub-prose[^"]*"[^>]*>.*?</div>', after, re.S):
        tail += '      ' + m.group(0).strip() + '\n'

    opening = re.match(r'(<section[^>]*>)\s*(<div class="section-bg[^>]*>.*?</div>)?', sec, re.S)
    head = opening.group(0).rstrip()
    per = columns(len(cards))
    body = (f'\n    <div class="container">\n'
            f'      <h2 class="display-h2 reveal" data-animation="fade-up">{h2}</h2>\n'
            f'{lead_html}'
            f'{build(cards, per)}\n'
            f'{tail}'
            f'    </div>\n  </section>')
    return (head + body).replace('data-block="hub-cards"', 'data-block="hub-tiles"', 1)


def main():
    changed, grids = [], 0
    for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        if os.path.basename(f).startswith('blog'):
            continue
        s = open(f, encoding='utf-8').read()
        out, pos, n = [], 0, 0
        for m in re.finditer(r'<section[^>]*data-block="hub-cards"[^>]*>.*?\n  </section>', s, re.S):
            new = convert_section(m.group(0))
            if new is None:
                continue
            out.append((m.start(), m.end(), new))
            n += 1
        if not out:
            continue
        for a, b, new in reversed(out):
            s = s[:a] + new + s[b:]
        if not DRY:
            open(f, 'w', encoding='utf-8').write(s)
        changed.append((os.path.basename(f), n))
        grids += n
    print(f'{"would convert" if DRY else "converted"} {grids} grids on {len(changed)} pages')
    for f, n in changed:
        print(f'   {f:44} {n}')


if __name__ == '__main__':
    main()
