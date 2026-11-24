#!/usr/bin/env python3
"""
Builds heating-services.html, the general heating ad landing page.

The copy is the client's own, from "Unbounce Landing Page Copy - Sunny Home
Services - Heating Services Landing Page" (received November 24, 2026). Every
heading, paragraph and bullet below is their wording. Nothing was invented.

The page is built the same way as the four "-experts" landing pages: the header,
the van band, the service areas and the footer are lifted out of index.html at
build time, so they can never drift away from the rest of the site. Everything
else is this page's own copy, laid out in the same design.

Run:  python3 tools/heatinglp.py
"""
import os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.join(ROOT, 'index.html')
SLUG = 'heating-services'
LIVE = 'https://sunnyhomeservices.com/heating-services'

# This page's own call-tracked number. The copy doc puts it in the header too,
# unlike the four "-experts" pages, which keep the main office number up top.
PHONE = '(385) 438-4462'
TEL = '+1' + re.sub(r'\D', '', PHONE)
PH = PHONE.replace(' ', '&nbsp;')

TITLE = 'Heating Services in West Jordan, UT | Sunny Home Services'
DESC = ('Sunny Home Services installs, repairs, and maintains gas and electric '
        'furnaces, heat pumps, and ductless mini-splits from top brands for '
        'homeowners in the Salt Lake City area.')


# ---------------------------------------------------------------- shared parts

def read(p):
    return open(p, encoding='utf-8').read()


def block(src, needle, tag='section'):
    """The whole <tag> element that contains `needle`, lifted verbatim."""
    i = src.find(needle)
    if i < 0:
        raise SystemExit('block not found: ' + needle)
    start = i if src.startswith('<' + tag, i) else src.rfind('<' + tag, 0, i)
    end = src.find('</' + tag + '>', i)
    if start < 0 or end < 0:
        raise SystemExit('could not bound block: ' + needle)
    return src[start:end + len(tag) + 3]


# ------------------------------------------------------------------- page copy

H1_LINES = [('Heating Services', False), ('in West Jordan,&nbsp;UT', True)]
SUBHEAD = ('Installation, Maintenance, and Emergency Repairs from a '
           'Local&nbsp;Company')
HERO_P = ('It&rsquo;s only a matter of time before sub-zero temperatures strike the '
          'Wasatch Front. Sunny Home Services is a dependable heating company in West '
          'Jordan you can count on for expert heating solutions. We find long-term '
          'heating solutions and ensure your system runs smoothly when you need it the '
          'most, from Furnaces to Heat&nbsp;Pumps.')

# The two offers the copy doc puts in the hero. The labels are the doc's. The
# fine print is not in the doc, so it is taken word for word from the client's
# own offers page (offers.html), where both coupons already live.
HERO_OFFERS = [
    ('is-sky', '$49', 'Furnace&nbsp;Tune-Up', 'Mention this coupon when you&nbsp;book.'),
    ('is-gold', '$98', 'Heating &amp; AC&nbsp;Tune-Up', 'AC and furnace, tuned&nbsp;together.'),
]

WHY = ['Locally Owned&nbsp;Company',
       '50+ Years Combined&nbsp;Experience',
       'Licensed, Bonded, and&nbsp;Insured',
       'Same-Day Emergency&nbsp;Response',
       'Upfront, Flat-Rate&nbsp;Pricing',
       'EPA, RMGA&nbsp;Certified',
       'Background-Checked&nbsp;Technicians',
       'Financing&nbsp;Available']

INTRO_H = 'Quality Heating Service in the Salt Lake City&nbsp;Area'
INTRO_P = ('When you need an expert heating company, Sunny Home Services is here to '
           'help. You can count on our team for emergency heating repairs during a cold '
           'snap, expert installation, or preventive heater maintenance. Extreme '
           'temperatures and valley air pollution can strain your heating system, but '
           'our local knowledge and solutions ensure your heater lasts and is energy '
           '&nbsp;efficient.'.replace(' &nbsp;efficient.', '&nbsp;efficient.'))

INSTALL_H = 'Heating&nbsp;Installation'
INSTALL_P = ('Is it your first time installing a furnace or heater? Or does your '
             'struggling system need to be replaced? Factoring in your home, budget, '
             'and energy goals, we&rsquo;ll help you find the perfect system. We offer '
             'many makes and models from the top brands, specializing&nbsp;in:')
INSTALL_CARDS = [
    ('heroes/furnace-installation.webp',
     'A Sunny Home Services technician installing a gas furnace',
     'Gas and Electric&nbsp;Furnaces',
     'We install energy-efficient furnaces with an annual fuel utilization efficiency '
     '(AFUE) of up to 98%, meaning they turn up to 98% of the fuel used into heat. Our '
     'RMGA-certified technicians install gas furnaces if you have a natural gas '
     'connection. Electric furnaces are suited for smaller homes without gas&nbsp;service.'),
    ('heroes/heat-pumps.webp',
     'An outdoor heat pump unit beside a Utah home',
     'Heat&nbsp;Pumps',
     'Modern air-source heat pumps perform well in Utah&rsquo;s temperature extremes and '
     'semi-arid climate. A cold-climate heat pump is an effective year-round home comfort '
     'option. Replacing your HVAC with a single heating and cooling solution reduces '
     'energy usage, making it a great investment in even an older&nbsp;home.'),
    ('heroes/mini-splits.webp',
     'A wall-mounted ductless mini-split indoor unit',
     'Ductless&nbsp;Mini-Splits',
     'Whether your home doesn&rsquo;t have ductwork, it&rsquo;s too costly or disruptive '
     'to install it, or you need heating or cooling for a single room or area, we can '
     'install a ductless mini-split system. Multiple indoor units are often installed in '
     'local homes for zoned, room-by-room comfort. These units mount to a wall or the '
     'ceiling and connect to a single outdoor&nbsp;compressor.'),
]
INSTALL_NOTE = ('Every install starts with a Manual J&reg; load calculation to ensure '
                'your heater isn&rsquo;t oversized or undersized for your&nbsp;home.')

REPAIR_H = 'Heating&nbsp;Repair'
REPAIR_P = ('Our technicians know exactly what it takes to keep your home warm. '
            'Temperatures in the Salt Lake Valley often drop into the teens and single '
            'digits during winter. Sunny Home Services provides prompt heating repair '
            'with same-day appointments, flat-rate pricing, and skilled technicians who '
            'can&nbsp;address:')
REPAIR_L = ['Cracked heat&nbsp;exchangers', 'Dirty or failing&nbsp;ignitors',
            'Clogged air&nbsp;filters', 'Issues related to short&nbsp;cycling']
SIGNS_H = 'Call Us for Furnace Repair Right&nbsp;Away'
SIGNS_P = 'Call us for furnace repair right away if you notice the following&nbsp;signs:'
SIGNS_L = ['Your home doesn&rsquo;t reach the right&nbsp;temperature.',
           'You smell gas, burning plastic, or a metallic&nbsp;odor.',
           'The furnace shuts down too&nbsp;quickly.',
           'The carbon monoxide alarm goes&nbsp;off.',
           'A yellow or orange pilot&nbsp;light.',
           'Combustion or electronic ignition&nbsp;failures.',
           'Banging, rattling, grinding, or screeching&nbsp;noises.',
           'An increase in energy bills with no change in&nbsp;usage.']

MAINT_H = 'Heating System Preventative&nbsp;Maintenance'
MAINT_P = ['The climate along the Wasatch Front puts a great deal of strain on heaters. '
           'We provide heating maintenance to help your furnace last through a long, '
           'chilly winter and reduce the effects of dry, dusty&nbsp;air.',
           'Routine annual tune-ups help your heater run more efficiently, reduce the '
           'risk of mid-winter breakdowns, and&nbsp;include:']
MAINT_L = ['Thorough equipment&nbsp;inspections.',
           'Cleaning burners, flame sensors, and blower&nbsp;motors.',
           'Combustion tests to ensure efficient&nbsp;ignition.',
           'Thermostat calibration and smart thermostat&nbsp;setup.',
           'Gas pressure and line&nbsp;inspection.',
           'Condensate drain&nbsp;check.',
           'Air filter inspection and&nbsp;replacement.',
           'Safety and limit switch&nbsp;testing.']

EMERG_H = 'Emergency Heating&nbsp;Repair'
EMERG_P = ['Winters here can be brutally cold, adding to the strain on your furnace. '
           'West Jordan&rsquo;s 4,300-foot elevation and inversion events create '
           'conditions that can add to the strain, causing your furnace to break down '
           '&nbsp;unexpectedly.'.replace(' &nbsp;unexpectedly.', '&nbsp;unexpectedly.'),
           'Indoor temperatures can drop fast, causing dangerous problems in your home. '
           'That&rsquo;s why Sunny Home Services is always prepared to dispatch a team '
           'for prompt heating service. Once you call, we send a technician to diagnose '
           'the problem. They arrive in a fully stocked truck, so most issues can be '
           'fixed on the&nbsp;spot.']
EMERG_L = ['No&nbsp;heat', 'Strange&nbsp;smells', 'Unusual&nbsp;noises',
           'Ice on the&nbsp;heater', 'Carbon monoxide&nbsp;alarm']
EMERG_LEAD = 'Signs of an emergency&nbsp;include:'

CTA_H = 'Call Sunny Home Services for Expert Heating&nbsp;Solutions'
CTA_P = ['We&rsquo;re your go-to heating professionals along the Wasatch Front. Our team '
         'ensures you&rsquo;re never without heat during a cold snap, from providing '
         'emergency repairs to routine maintenance. Sunny Home Services knows how to '
         'keep your home comfortable&nbsp;year-round.',
         'Contact us today for prompt service, upfront pricing, and expert&nbsp;solutions.']

# Real reviews, supplied in the copy doc with the reviewer's name. The doc gives
# no city and no platform for any of them, so none is shown: nothing here is
# filled in from guesswork. There is no overall star rating on this page either,
# for the same reason it is absent from the home page.
REVIEWS = [
    ('Josh at Sunny Home Services was fantastic today! Straightforward and honest, and '
     'told me all I need to know about my&nbsp;furnace.', 'Samuel M.'),
    ('Wowza! We had the brightest technician come to repair our furnace! His name is '
     'Josh. We were ready to sell the cars so we could buy a new furnace. They have a '
     'fantastic maintenance program we are joining. We had good fortune with Sunny Home '
     'Services! Thank you, thank&nbsp;you!!!', 'Annette D.'),
    ('Sunny Home Services was amazing to work with. They took the time to educate me on '
     'my options, and they had a great price for great equipment. I worked with Tyler on '
     'finding the right equipment, and Dave came and did our install for a new AC/Heat '
     'Pump. Both were very professional and easy to work with. I would definitely '
     'recommend Sunny Home&nbsp;Services.', 'Jared H.'),
]

SERVICES = [('Cooling', 'air-conditioner.html'), ('Heating', 'heating.html'),
            ('Plumbing', 'plumber.html'), ('Sewer and Drains', 'sewer-and-drains.html'),
            ('Air Quality', 'indoor-air-quality.html'), ('Mini Splits', 'mini-splits.html'),
            ('Heat Pumps', 'heat-pumps.html')]

CONSENT = ('By checking the &ldquo;Yes, please text me!&rdquo; box, I am providing express '
           'written consent to receive auto-dialed and pre-recorded calls, texts, and '
           'SMS/MMS with marketing communications from SUNNY HOME SERVICES regarding home '
           'improvement services at the phone number provided above, even if the number is '
           'on a corporate, state, or national Do Not Call list. Consent is not a condition '
           'to purchase services or products.')

BOTTOM_BAR = 'Emergency Heating Repair in Wasatch Front&nbsp;Communities'

MAP = ('https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3558.049617962597'
       '!2d-111.97534098789858!3d40.59744677129181!2m3!1f0!2f0!3f0!3m2!1i1024!2i768'
       '!4f13.1!3m3!1m2!1s0x87528f07da3cbdb7%3A0xac103968c1a5ce79'
       '!2sSunny%20Home%20Services!5e1!3m2!1sen!2sus!4v1789492771759!5m2!1sen!2sus')

SVG_ALERT = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.9 1.8 18a2 2 0 0 0 '
             '1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4"/>'
             '<path d="M12 17h.01"/></svg>')
SVG_WRENCH = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" '
              'stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 1 '
              '5.3 5.2l-8.4 8.4a2.4 2.4 0 0 1-3.4-3.4l8.4-8.4z"/><path d="M9 7 4 2 2 4l5 5"/></svg>')


# --------------------------------------------------------------------- render

def checks(items, cls='check-list'):
    out = ''
    for it in items:
        out += ('\n            <li class="check"><span class="check-badge">&#10003;</span>'
                f'<span class="check-text">{it}</span></li>')
    return out


def headline(lines):
    """One span per word, the way the home page builds its hero title, so the
    white type and the hover treatment both apply."""
    out = ''
    for text, alt in lines:
        cls = 'hero-line hero-line-' + ('2' if alt else '1')
        words = ''.join(f'<span class="word{" alt-font" if alt else ""}">{w}</span>\n          '
                        for w in text.split(' '))
        out += f'        <span class="{cls}">\n          {words.rstrip()}\n        </span>\n'
    return out


def build():
    date = datetime.date.today().strftime('%B %-d, %Y')
    home = read(HOME)

    header = block(home, 'class="site-header"', 'header')
    footer = block(home, '<footer', 'footer')
    tail = home[home.find('</footer>') + len('</footer>'):]
    van = block(home, 'about-van-split')
    areas = block(home, 'section-areas')

    # This page carries its own tracked number everywhere, including the header,
    # which is what the copy doc asks for.
    header = header.replace('+13858538116', TEL).replace('385.853.8116', PH)
    footer = footer.replace('+13858538116', TEL).replace('385.853.8116', PH)
    van = van.replace('+13858538116', TEL).replace('385.853.8116', PH)
    areas = areas.replace('+13858538116', TEL).replace('385.853.8116', PH)
    van = van.replace('href="#contact">Meet The&nbsp;Family', 'href="#contact">Book&nbsp;Now')

    offers = ''.join(f'''
          <div class="hs-offer {tone}">
            <div class="hs-offer-value">{value}</div>
            <div class="hs-offer-label">{label}</div>
            <div class="hs-offer-fine">{fine}</div>
          </div>''' for tone, value, label, fine in HERO_OFFERS)

    cards = ''.join(f'''
          <article class="hs-card">
            <div class="hs-card-media"><img src="assets/{img}" alt="{alt}" loading="lazy" data-parallax="6"></div>
            <div class="hs-card-body">
              <h4 class="hs-card-title">{t}</h4>
              <p>{p}</p>
            </div>
          </article>''' for img, alt, t, p in INSTALL_CARDS)

    revs = ''.join(f'''
          <figure class="testimonial">
            <div class="stars" aria-label="Five out of five stars">&#9733; &#9733; &#9733; &#9733; &#9733;</div>
            <blockquote class="quote">&ldquo;{q}&rdquo;</blockquote>
            <figcaption class="testi-meta">
              <div class="avatar" aria-hidden="true">{n[0]}</div>
              <div><div class="name">{n}</div></div>
            </figcaption>
          </figure>''' for q, n in REVIEWS)

    svc = ''.join(f'\n          <a class="hs-svc" href="{href}">{name}</a>'
                  for name, href in SERVICES)

    parts = [f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{TITLE}</title>
  <meta name="description" content="{DESC}">
  <!-- Production URL: {LIVE} -->
  <!-- The general heating ad landing page. It is not in the menu; traffic comes
       from ads only. Built {date} from the client's copy doc, "Unbounce Landing
       Page Copy - Sunny Home Services - Heating Services Landing Page". Every
       heading, paragraph and bullet is their wording. See tools/heatinglp.py.
       Do not hand-edit: that script overwrites this file. -->
  <!-- This page's call-tracked number is {PHONE}. The copy doc puts it in the
       header as well as the body, which is different from the four "-experts"
       landing pages, where the header keeps the main office number. -->
  <!-- The copy doc has a "Branding Video" block. No branding video was supplied
       and the two clips in assets/ are a plumbing crawlspace and an air
       conditioner, neither branded nor heating, so the block is left out rather
       than filled with a play button that plays the wrong thing. -->
  <!-- The copy doc also has an "AWARDS/CERTIFICATIONS" block with nothing in it.
       The only certifications we can source are EPA and RMGA, and both are
       already in the Why Sunny Home Services list below. Nothing was invented. -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo+Black&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/sunny-engine.css?v=7">
  <link rel="stylesheet" href="css/sunny-landing.css?v=7">
  <link rel="stylesheet" href="css/sunny-hub.css?v=4">
  <link rel="stylesheet" href="css/sunny-home.css?v=2">
</head>
<body>
''', header, f'''
  <!-- 01 Hero -->
  <section class="section section-hero section-hero-split has-hs-hero" id="hero">
    <div class="hero-art"><img src="assets/hero-brand-art.webp" alt=""></div>
    <div class="hero-scrim"></div>
    <div class="hero-van-panel">
      <img class="hero-video" src="assets/hero-van.webp" alt="Sunny Home Services branded service van">
    </div>

    <div class="container hero-content">
      <h1 class="display-hero hero-title-interactive" id="hero-title">
{headline(H1_LINES)}      </h1>
      <p class="hs-subhead">{SUBHEAD}</p>
      <p class="lead lead-on-video">{HERO_P}</p>
      <div class="cta-row">
        <a class="btn btn-primary btn-pill btn-lg" href="#contact">Book&nbsp;Now</a>
        <a class="btn btn-outline-light btn-pill btn-lg btn-call-lp" href="tel:{TEL}">Call&nbsp;{PH}</a>
      </div>
      <div class="hs-offers">{offers}
      </div>
    </div>
  </section>
''', f'''
  <!-- 02 Why Sunny Home Services, the copy doc's eight lines -->
  <section class="section section-why reveal" data-animation="fade-up" id="why" data-block="why-split">
    <div class="section-bg section-bg-faint"><img src="assets/bg/tools.webp" alt="" data-parallax="12"></div>
    <div class="container">
      <div class="hub-split">
        <div>
          <h2 class="display-h2">Why Sunny Home&nbsp;Services</h2>
          <ul class="check-list hs-why-grid">{checks(WHY)}
          </ul>
          <div class="cta-row" style="margin-top:28px;">
            <a class="btn btn-primary btn-pill btn-lg" href="#contact">Book&nbsp;Now</a>
            <a class="btn btn-outline btn-pill btn-lg btn-call-lp" href="tel:{TEL}">Call&nbsp;{PH}</a>
          </div>
        </div>
        <div class="hub-split-media">
          <img src="assets/services/why-team.webp" alt="The Sunny Home Services team" data-parallax="6">
        </div>
      </div>
    </div>
  </section>
''', f'''
  <!-- 03 Opening copy -->
  <section class="section lp-band lp-band-intro reveal" data-animation="fade-up" id="intro">
    <div class="section-bg"><img src="assets/heroes/heating.webp" alt="" data-parallax="12"></div>
    <div class="lp-wash"></div>
    <div class="container">
      <h2 class="display-h1 align-center">{INTRO_H}</h2>
      <div class="hub-prose"><p>{INTRO_P}</p></div>
    </div>
  </section>
''', f'''
  <!-- 04 Heating installation, and the three systems the copy doc names -->
  <section class="section section-services reveal" data-animation="fade-up" id="installation" data-block="install">
    <div class="section-bg section-bg-faint"><img src="assets/bg/neighborhood.webp" alt="" data-parallax="12"></div>
    <div class="bg-orb bg-orb-sky" style="top:-200px; left:-200px; width:540px;"></div>
    <div class="bg-orb bg-orb-orange" style="bottom:-220px; right:-100px; width:420px;"></div>
    <div class="container">
      <h3 class="display-h1 align-center">{INSTALL_H}</h3>
      <div class="hub-prose hs-prose-center"><p>{INSTALL_P}</p></div>
      <div class="hs-cards">{cards}
      </div>
      <p class="lp-note hs-note-center">{INSTALL_NOTE}</p>
    </div>
  </section>
''', f'''
  <!-- 05 Heating repair. Two cards stacked at full width rather than side by
       side: the second list has eight items and the first has four, and in a
       half-width card eight items in two columns wrap to three lines each. -->
  <section class="section lp-band lp-band-problems reveal" data-animation="fade-up" id="repair">
    <div class="section-bg"><img src="assets/heroes/furnace-repair.webp" alt="" data-parallax="14"></div>
    <div class="lp-wash"></div>
    <div class="container">
      <h3 class="display-h1 align-center hs-band-title">{REPAIR_H}</h3>
      <div class="lp-grid lp-grid-stack">
        <div class="lp-card is-cool">
          <div class="lp-card-icon" aria-hidden="true">{SVG_WRENCH}</div>
          <div class="hub-prose"><p>{REPAIR_P}</p></div>
          <ul class="check-list hs-why-grid">{checks(REPAIR_L)}
          </ul>
        </div>
        <div class="lp-card is-warm">
          <div class="lp-card-icon" aria-hidden="true">{SVG_ALERT}</div>
          <h4 class="display-h2">{SIGNS_H}</h4>
          <div class="hub-prose"><p>{SIGNS_P}</p></div>
          <ul class="check-list hs-why-grid">{checks(SIGNS_L)}
          </ul>
        </div>
      </div>
    </div>
  </section>
''', f'''
  <!-- 06 Preventative maintenance -->
  <section class="section section-why reveal" data-animation="fade-up" id="maintenance" data-block="maintenance">
    <div class="section-bg section-bg-faint"><img src="assets/heroes/furnace-maintenance.webp" alt="" data-parallax="12"></div>
    <div class="container">
      <div class="hub-split hub-split-flip">
        <div class="hub-split-media">
          <img src="assets/services/heating-work.webp" alt="A technician servicing a furnace during a tune-up" data-parallax="6">
        </div>
        <div>
          <h3 class="display-h2">{MAINT_H}</h3>
          <div class="hub-prose">{''.join(f'<p>{p}</p>' for p in MAINT_P)}</div>
          <ul class="check-list hs-why-grid">{checks(MAINT_L)}
          </ul>
        </div>
      </div>
    </div>
  </section>
''', f'''
  <!-- 07 Emergency heating repair -->
  <section class="section lp-band lp-band-problems reveal" data-animation="fade-up" id="emergency">
    <div class="section-bg"><img src="assets/heroes/emergency-heating-repair.webp" alt="" data-parallax="14"></div>
    <div class="lp-wash"></div>
    <div class="container">
      <div class="lp-grid lp-grid-emergency">
        <div class="lp-card is-warm">
          <div class="lp-card-icon" aria-hidden="true">{SVG_ALERT}</div>
          <h3 class="display-h2">{EMERG_H}</h3>
          <div class="hub-prose">{''.join(f'<p>{p}</p>' for p in EMERG_P)}</div>
          <p class="hs-lead-in">{EMERG_LEAD}</p>
          <ul class="check-list hs-signs-row">{checks(EMERG_L)}
          </ul>
          <div class="cta-row" style="margin-top:26px;">
            <a class="btn btn-primary btn-pill btn-lg btn-call-lp" href="tel:{TEL}">Call&nbsp;{PH}</a>
          </div>
        </div>
      </div>
    </div>
  </section>
''', van, f'''
  <!-- 08 Closing call to action -->
  <section class="section section-cta-banner reveal" data-animation="fade-up" id="cta" data-block="final-cta">
    <div class="section-bg"><img src="assets/bg/wasatch.webp" alt="" data-parallax="15"></div>
    <div class="cta-overlay"></div>
    <div class="container">
      <h2 class="display-h1">{CTA_H}</h2>
      {''.join(f'<p>{p}</p>' for p in CTA_P)}
      <div class="cta-row-center">
        <a class="btn btn-primary btn-pill btn-lg" href="#contact">Book&nbsp;Now</a>
        <a class="btn btn-outline-light btn-pill btn-lg btn-call-lp" href="tel:{TEL}">Call&nbsp;{PH}</a>
      </div>
    </div>
  </section>
''', f'''
  <!-- 09 Reviews. Three real reviews, supplied by the client with the reviewer's
       name. No city and no platform were given for any of them, so none is
       shown, and there is no overall star rating anywhere on this page. -->
  <section class="section section-testimonials reveal" data-animation="fade-up" id="reviews">
    <div class="section-bg section-bg-faint"><img src="assets/heroes/community-van-golden.webp" alt="" data-parallax="12"></div>
    <div class="accent-stripe accent-stripe-sky"></div>
    <div class="container">
      <h2 class="display-h1 align-center">What Our Customers&nbsp;Think</h2>
      <div class="testimonials-grid">{revs}
      </div>
    </div>
  </section>
''', f'''
  <!-- 10 Our services, the seven the copy doc lists -->
  <section class="section section-hs-services reveal" data-animation="fade-up" id="our-services">
    <div class="section-bg section-bg-faint"><img src="assets/heroes/service-area.webp" alt="" data-parallax="10"></div>
    <div class="container">
      <h2 class="display-h1 align-center">Our&nbsp;Services</h2>
      <div class="hs-svc-strip">{svc}
      </div>
      <div class="cta-row-center" style="margin-top:30px;">
        <a class="btn btn-primary btn-pill btn-lg" href="#contact">Book&nbsp;Now</a>
        <a class="btn btn-outline btn-pill btn-lg btn-call-lp" href="tel:{TEL}">Call&nbsp;{PH}</a>
      </div>
    </div>
  </section>
''', areas, f'''
  <!-- 11 The form, with the fields the copy doc lists, then the map -->
  <section class="section section-contact reveal" data-animation="fade-up" id="contact">
    <div class="section-bg"><img src="assets/bg/skyline.webp" alt="" data-parallax="15"></div>
    <div class="accent-stripe accent-stripe-orange"></div>
    <div class="bg-orb bg-orb-sky" style="top:-100px; right:-200px; width:480px;"></div>
    <div class="bg-orb bg-orb-gold" style="bottom:-200px; left:-200px; width:420px;"></div>

    <div class="container">
      <h2 class="display-h1 align-center">Request Your Service&nbsp;Now</h2>

      <div class="contact-grid">
        <form class="contact-form" onsubmit="event.preventDefault(); this.querySelector('.form-success').classList.add('is-visible');">
          <div class="form-consent hs-text-opt">
            <input id="cf-text" type="checkbox">
            <label for="cf-text">Would you like to communicate by text message? Yes, please text&nbsp;me!</label>
          </div>
          <div class="form-row">
            <div class="form-field">
              <label for="cf-first">First Name</label>
              <input id="cf-first" type="text" placeholder="Jane" required>
            </div>
            <div class="form-field">
              <label for="cf-last">Last Name</label>
              <input id="cf-last" type="text" placeholder="Smith" required>
            </div>
          </div>
          <div class="form-row">
            <div class="form-field">
              <label for="cf-phone">Phone Number</label>
              <input id="cf-phone" type="tel" placeholder="(801) 555-0000" required>
            </div>
            <div class="form-field">
              <label for="cf-email">Email</label>
              <input id="cf-email" type="email" placeholder="jane@email.com" required>
            </div>
          </div>
          <div class="form-field">
            <label for="cf-help">How Can We Help&nbsp;You?</label>
            <textarea id="cf-help" rows="4" placeholder="Tell us what your heating system is doing." required></textarea>
          </div>
          <button type="submit" class="btn btn-primary btn-pill btn-lg btn-full">Submit</button>
          <p class="form-fine">{CONSENT}</p>
          <p class="form-legal"><a href="privacy-policy.html">Privacy Policy</a> &middot; <a href="terms-and-conditions.html">Terms and&nbsp;Conditions</a></p>
          <div class="form-success">&#10003; Thanks - we&rsquo;ll be in touch within one business&nbsp;day.</div>
        </form>

        <aside class="contact-info">
          <h3>Reach Us&nbsp;Directly</h3>
          <div class="info-block">
            <div class="info-label">Phone</div>
            <a class="info-value-big" href="tel:{TEL}">{PH}</a>
          </div>
          <div class="info-block">
            <div class="info-label">Email</div>
            <a class="info-value" href="mailto:hello@sunnyhomeservices.com">hello@sunnyhomeservices.com</a>
          </div>
          <div class="info-block">
            <div class="info-label">Office</div>
            <div class="info-value">8461 Old Bingham Hwy<br>West Jordan, UT 84088</div>
          </div>
          <div class="info-block">
            <div class="info-label">Hours</div>
            <div class="info-value">Mon-Fri &middot; 7am - 7pm<br>Sat-Sun &middot; By appointment</div>
          </div>
        </aside>
      </div>

      <div class="contact-map reveal" data-animation="fade-up" style="margin-top:36px; border-radius:18px; overflow:hidden; box-shadow:0 18px 40px rgba(5,8,18,0.18); position:relative; z-index:1;">
        <iframe title="Sunny Home Services on Google Maps" width="100%" height="360" style="border:0; display:block;" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="{MAP}"></iframe>
      </div>
    </div>
  </section>
''', footer, f'''
<!-- The full width bar the copy doc puts at the very bottom of the page -->
<div class="hs-bottom-bar">{BOTTOM_BAR}</div>
''', tail]

    return '\n'.join(parts)


def main():
    out = os.path.join(ROOT, SLUG + '.html')
    open(out, 'w', encoding='utf-8').write(build())
    print('wrote', SLUG + '.html')


if __name__ == '__main__':
    main()
