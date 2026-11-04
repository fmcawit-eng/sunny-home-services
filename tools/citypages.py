#!/usr/bin/env python3
"""
Builds a city service-area page from its approved brief.

Takes the outline JSON that tools/outline.py produces and a scaffold page whose
header, footer and scripts are reused byte for byte, so a new city page shares
one header and one footer with the other 110 pages.

Copy is the brief's own wording. Nothing is written here that the brief does not
say. The only strings this file invents are structural labels (the "Learn More"
on a card, the breadcrumb) which match the existing pages.
"""
import json, re, sys, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PHONE_TEL   = '+13858538116'
PHONE_LABEL = '385.853.8116'

# Smart punctuation, so generated copy matches the pages written by hand.
def ent(t):
    t = (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
          .replace('’', '&rsquo;').replace('‘', '&lsquo;')
          .replace('“', '&ldquo;').replace('”', '&rdquo;')
          .replace('…', '&hellip;').replace('®', '&reg;')
          .replace('·', '&middot;').replace(' ', '&nbsp;'))
    # straight quotes the brief left behind
    t = re.sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", '&rsquo;', t)
    t = re.sub(r"(?<=[A-Za-z])'(?=\s|$)", '&rsquo;', t)
    # no em or en dashes anywhere
    t = t.replace('—', ', ').replace('–', ' to ')
    return t

def resolve_markers(t, links):
    """Replace 'phrase[a]' with 'phrase' linked, using the links map."""
    def rep(m):
        key = m.group(2)
        href = links.get(key)
        phrase = m.group(1)
        if not href:
            return phrase
        return f'<a href="{href}">{phrase}</a>'
    # the phrase is the run of words directly before the marker, up to 6 words
    return re.sub(r'((?:[A-Za-z0-9&’\'-]+ ){0,5}[A-Za-z0-9&’\'-]+)\[([a-z])\]', rep, t)

def split_named(item):
    """'Cooling services: we do x' -> ('Cooling services', 'we do x')."""
    m = re.match(r'^([A-Z][^:]{2,60}):\s+(.*)$', item)
    return (m.group(1), m.group(2)) if m else (None, item)

def P(text, links):   return f'<p>{ent(resolve_markers(text, links))}</p>'

def rail(h2, inner, tone, sid, bg):
    t = ' is-tone' if tone else ''
    return f'''  <section class="section-hub{t} section-hub-tint" id="{sid}" data-block="hub-cards">
    <div class="section-bg"><img src="{bg}" alt="" data-parallax="15"></div>
    <div class="container">
      <div class="hub-rail">
        <div class="hub-rail-head reveal" data-animation="fade-up">
          <h2 class="display-h2 reveal" data-animation="fade-up">{h2}</h2>
        </div>
        <div class="hub-rail-body">
{inner}
        </div>
      </div>
    </div>
  </section>
'''

def cards(items, imgmap, links):
    """items = [(title, desc)]"""
    n = len(items)
    # Pick a column count that leaves either a full last row or exactly one
    # card on it, and let that one card span the row. Never a stranded card
    # beside empty space.
    if   n % 4 == 0: per = 4
    elif n % 3 == 0: per = 3
    elif n % 2 == 0: per = 2
    elif n % 3 == 1: per = 3
    else:            per = 2
    if n <= 2: per = n
    wide = n % per == 1 and n > per
    out = [f'      <div class="hub-cards hub-cards-{per}">']
    for idx, (title, desc) in enumerate(items):
        img, href = imgmap(title)
        last = (idx == n - 1)
        body = (f'<div class="hub-card-body"><div class="hub-card-title">{ent(title)}</div>'
                f'<p class="hub-card-desc">{ent(resolve_markers(desc, links))}</p>'
                f'<span class="hub-card-link">Learn More &rsaquo;</span></div>')
        cls = 'hub-card has-media reveal' + (' is-wide' if (wide and last) else '')
        out.append(f'''        <a class="{cls}" data-animation="fade-up" href="{href}">
          <div class="hub-card-media"><img src="{img}" alt="{ent(title)}"></div>
          {body}
        </a>''')
    out.append('      </div>')
    return '\n'.join(out)

def checks(items, links):
    out = ['      <ul class="check-list">']
    for it in items:
        name, rest = split_named(it)
        if name:
            inner = f'<strong>{ent(name)}:</strong> {ent(resolve_markers(rest, links))}'
        else:
            inner = ent(resolve_markers(it, links))
        out.append('        <li class="check reveal" data-animation="fade-up">'
                   '<span class="check-badge">&#10003;</span>'
                   f'<span class="check-text">{inner}</span></li>')
    out.append('      </ul>')
    return '\n'.join(out)

def subs_prose(subs, links):
    """H3 + prose + bullets, for sub-sections that are not services."""
    out = []
    for u in subs:
        out.append(f'      <h3 class="hub-sub-h3 reveal" data-animation="fade-up">{ent(u["h3"])}</h3>')
        for b in u['blocks']:
            if b[0] == 'p':
                out.append('      ' + P(b[1], links))
            else:
                out.append(checks(b[1], links))
    return '\n'.join(out)

def prose_section(h2, paras, tone, sid, bg, links):
    t = ' is-tone' if tone else ''
    body = '\n        '.join(P(p, links) for p in paras)
    return f'''  <section class="section-hub{t}" id="{sid}" data-block="hub-prose">
    <div class="section-bg section-bg-faint"><img src="{bg}" alt="" data-parallax="12"></div>
    <div class="container">
      <h2 class="display-h2 reveal" data-animation="fade-up">{h2}</h2>
      <div class="hub-prose reveal" data-animation="fade-up">
        {body}
      </div>
    </div>
  </section>
'''

def split_section(h2, paras, img, flip, sid, links):
    body = '\n          '.join(f'<div class="hub-prose">{P(p, links)}</div>' for p in paras)
    f = ' is-flipped' if flip else ''
    return f'''  <section class="section-hub has-bleed" id="{sid}" data-block="hub-split">
    <div class="container">
      <div class="hub-split is-bleed{f}">
        <div class="hub-split-copy reveal" data-animation="fade-up">
          <h2 class="display-h2">{h2}</h2>
          {body}
        </div>
        <div class="hub-split-media"><img src="{img}" alt="" data-parallax="10"></div>
      </div>
    </div>
  </section>
'''

def cta_section(h2, paras, links):
    body = '\n      '.join(P(p, links) for p in paras)
    return f'''  <section class="section section-cta-banner" id="cta" data-block="hub-cta">
    <div class="section-bg"><img src="assets/bg/neighborhood.webp" alt="" data-parallax="15"></div>
    <div class="cta-overlay"></div>
    <div class="container">
      <h2 class="display-h2 reveal" data-animation="fade-up">{h2}</h2>
      <div class="hub-prose on-dark reveal" data-animation="fade-up">{body}</div>
      <div class="cta-row cta-row-center reveal" data-animation="fade-up">
        <a class="btn btn-primary btn-pill btn-lg book_button" href="coming-soon.html">Book Now</a>
        <a class="btn btn-outline-light btn-pill btn-lg" href="tel:{PHONE_TEL}">Call {PHONE_LABEL}</a>
      </div>
    </div>
  </section>
'''

def faq_section(qas):
    rows = []
    for q, a in qas:
        rows.append('        <details class="reveal" data-animation="fade-up">'
                    f'<summary>{ent(q)}</summary>'
                    f'<div class="hub-faq-body">{ent(a)}</div></details>')
    return '''  <section class="section-hub" id="faq" data-block="hub-faq">
    <div class="section-bg section-bg-soft"><img src="assets/bg/tools.webp" alt="" data-parallax="10"></div>
    <div class="container">
      <h2 class="display-h2 reveal" data-animation="fade-up">Frequently Asked Questions</h2>
      <div class="hub-faq">
''' + '\n'.join(rows) + '''
      </div>
    </div>
  </section>
'''

# ---------------------------------------------------------------- page assembly

BGS = ['assets/bg/wasatch.webp', 'assets/bg/tools.webp', 'assets/bg/ac-unit.png',
       'assets/bg/skyline.webp']

CARD_IMG = [
    (r'cool|air condition|\bac\b',        'assets/services/card-ac-repair.webp',        'air-conditioner.html'),
    (r'heat pump',                        'assets/services/heatpump-service.webp',      'heat-pumps.html'),
    (r'mini.?split|ductless',             'assets/services/minisplit-system.webp',      'mini-splits.html'),
    (r'heating|furnace',                  'assets/services/card-heating-install.webp',  'heating.html'),
    (r'air quality|iaq|filtration|filter','assets/services/air-quality.webp',           'indoor-air-quality.html'),
    (r'drain clean',                      'assets/services/drains.webp',                'drain-cleaning.html'),
    (r'hydro.?jet',                       'assets/services/drains.webp',                'hydro-jetting.html'),
    (r'tankless',                         'assets/services/water-heater.webp',          'tankless-water-heaters.html'),
    (r'water heater',                     'assets/services/water-heater.webp',          'water-heater-repair.html'),
    (r'leak detect',                      'assets/services/plumbing.webp',              'leak-detection.html'),
    (r'sewer',                            'assets/services/drains.webp',                'sewer-and-drains.html'),
    (r'camera inspect',                   'assets/services/drains.webp',                'camera-inspection.html'),
    (r'trenchless',                       'assets/services/drains.webp',                'trenchless-sewer-line-repair.html'),
    (r'fixture|faucet|toilet|disposal',   'assets/services/card-plumbing-fixtures.webp','plumbing-fixtures.html'),
    (r'gas line',                         'assets/services/card-plumbing-gas-lines.webp','gas-lines.html'),
    (r'emergency',                        'assets/services/card-heating-emergency.webp','emergency-plumbing-repair.html'),
    (r'plumb',                            'assets/services/plumbing.webp',              'plumber.html'),
]

def is_service_set(titles):
    """Cards carry a photo and a destination, so they are only right for a list
    of services. A list of symptoms, problems or steps gets a checklist."""
    # A service name is a short noun phrase. A sentence is a symptom or a step.
    if any(len(t.split()) > 5 for t in titles):
        return False
    hit = sum(1 for t in titles if card_target(t)[1] != 'coming-soon.html')
    return hit >= max(2, int(len(titles) * 0.6))

def card_target(title):
    low = title.lower()
    for pat, img, href in CARD_IMG:
        if re.search(pat, low):
            return img, href
    return 'assets/services/why-team.webp', 'coming-soon.html'

def build(outline_json, scaffold, out_file, cfg):
    o = json.load(open(outline_json))
    scaf = open(os.path.join(ROOT, scaffold), encoding='utf-8').read()

    head_end = scaf.index('<section class="hub-hero"')
    foot_start = scaf.index('<footer')
    head, foot = scaf[:head_end], scaf[foot_start:]

    head = re.sub(r'<title>.*?</title>', f'<title>{ent(cfg["title"])}</title>', head, flags=re.S)
    head = re.sub(r'<meta name="description" content=".*?">',
                  f'<meta name="description" content="{ent(o["meta"])}">', head, flags=re.S)
    head = re.sub(r'<!-- Production URL: \S+ -->',
                  f'<!-- Production URL: https://sunnyhomeservices.com{cfg["url"]} -->', head)

    hero = f'''<section class="hub-hero" id="hero" data-block="hub-hero">
    <div class="hub-hero-bg"><img src="{cfg['hero']}" alt="" data-parallax="8"></div>
    <div class="container">
      <div class="hub-hero-copy">
        <div class="hub-crumb"><span><span><a href="index.html">Home</a></span>{cfg['crumb']}</span></div>
        <h1 class="reveal" data-animation="fade-up">{ent(cfg['h1'])}</h1>
        <p class="hub-hero-sub reveal" data-animation="fade-up">{ent(cfg['sub'])}</p>
        <div class="cta-row reveal" data-animation="fade-up">
          <a class="btn btn-primary btn-pill btn-lg" href="coming-soon.html">{ent(cfg['cta'])}</a>
          <a class="btn btn-outline-light btn-pill btn-lg" href="tel:{PHONE_TEL}">Call {PHONE_LABEL}</a>
        </div>
      </div>
    </div>
  </section>
'''

    links = cfg['links']
    secs = o['secs']

    # Split the FAQ questions off the tail: everything after "Frequently Asked Questions"
    faq = []
    body_secs = []
    in_faq = False
    for s in secs:
        if re.fullmatch(r'Frequently Asked Questions', s['h2'].strip()):
            in_faq = True
            continue
        if in_faq:
            text = ' '.join(b[1] for b in s['blocks'] if b[0] == 'p')
            faq.append((s['h2'], text))
        else:
            body_secs.append(s)

    # The lead paragraph: the first section's opening prose becomes the intro band
    out = [hero]
    lead = cfg.get('lead')
    if lead:
        out.append(f'''  <section class="section-hub" id="intro" data-block="hub-prose">
    <div class="section-bg section-bg-faint"><img src="assets/bg/wasatch.webp" alt="" data-parallax="12"></div>
    <div class="container">
      <div class="hub-prose hub-intro-lead reveal" data-animation="fade-up" style="max-width:820px;margin:0 auto;">{P(lead, links)}</div>
    </div>
  </section>
''')

    tone = True
    split_used = 0
    for i, s in enumerate(body_secs):
        h2 = ent(resolve_markers(s['h2'], links))
        sid = re.sub(r'[^a-z0-9]+', '-', s['h2'].lower()).strip('-')[:28]
        paras = [b[1] for b in s['blocks'] if b[0] == 'p']
        uls = [b[1] for b in s['blocks'] if b[0] == 'ul']
        subs = s['subs']

        # 1. sub-headings each with prose -> a card per sub-heading
        if subs:
            items = [(u['h3'], ' '.join(b[1] for b in u['blocks'] if b[0] == 'p')) for u in subs]
            inner = ''
            if paras:
                inner += '      ' + P(paras[0], links) + '\n'
            if is_service_set([t for t, _ in items]):
                inner += cards(items, card_target, links)
                extra = [it for u in subs for b in u['blocks'] if b[0] == 'ul' for it in b[1]]
                if extra:
                    inner += '\n' + checks(extra, links)
            else:
                inner += subs_prose(subs, links)
            for p in paras[1:]:
                inner += '\n      ' + P(p, links)
            out.append(rail(h2, inner, tone, sid, BGS[i % len(BGS)]))
            tone = not tone
            continue

        # 2. a bullet list of "Name: description" -> a card per bullet
        if uls:
            flat = uls[0]
            named = [split_named(x) for x in flat]
            titled = [t for t, _ in named if t]
            if len(titled) >= max(2, len(named) - 1) and is_service_set(titled):
                items = [(t or d[:40], d) for t, d in named]
                inner = ('      ' + P(paras[0], links) + '\n' if paras else '') + cards(items, card_target, links)
                for p in paras[1:]:
                    inner += '\n      ' + P(p, links)
                out.append(rail(h2, inner, tone, sid, BGS[i % len(BGS)]))
                tone = not tone
                continue
            # 3. plain bullets -> a checklist
            inner = ('      ' + P(paras[0], links) + '\n' if paras else '') + checks(flat, links)
            for p in paras[1:]:
                inner += '\n      ' + P(p, links)
            out.append(rail(h2, inner, tone, sid, BGS[i % len(BGS)]).replace('data-block="hub-cards"',
                                                                             'data-block="hub-checklist"'))
            tone = not tone
            continue

        # 4. prose only. The last one is the CTA band; two get the full-bleed split.
        if i == len(body_secs) - 1:
            out.append(cta_section(h2, paras, links))
            continue
        if split_used < 2 and len(paras) >= 1 and i > 0:
            out.append(split_section(h2, paras, cfg['splits'][split_used], split_used % 2 == 1, sid, links))
            split_used += 1
            tone = not tone
            continue
        out.append(prose_section(h2, paras, tone, sid, BGS[i % len(BGS)], links))
        tone = not tone

    if faq:
        out.append(faq_section(faq))

    page = head + ''.join(out) + ' <!-- Footer - landing-style centered -->\n  \n  ' + foot
    open(os.path.join(ROOT, out_file), 'w', encoding='utf-8').write(page)
    return page

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1]))
    for job in spec:
        page = build(job['outline'], job['scaffold'], job['out'], job)
        words = len(re.findall(r'[A-Za-z0-9’\'-]+',
                    re.sub(r'<[^>]+>', ' ', page[page.index('<section class="hub-hero"'):])))
        print(f'  {job["out"]:38} {len(page):7,} bytes  ~{words:,} words')
