#!/usr/bin/env python3
"""
Rebuilds the four "-experts" ad landing pages in the site design.

These four pages used to be straight copies of the client's live landing pages.
The client's review asked for them to match the main page, so this script builds
them from the home page's own blocks: the header, the trust strip, the van band,
the Family Plan band, the service areas and the footer are lifted out of
index.html at build time, so they can never drift away from the home page again.

Everything else (hero, offers, the problem lists, the service tiles, the closing
call to action) is written per page from that page's own live copy, kept word for
word except where the review asked for a change.

Run:  python3 tools/expertslp.py
"""
import os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.join(ROOT, 'index.html')


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


def phone_href(p):
    return '+1' + re.sub(r'\D', '', p)


# ------------------------------------------------------------------- page copy

PAGES = [
    dict(
        slug='furnace-repair-experts',
        title='Furnace Repair Along the Wasatch Front | Sunny Home Services',
        desc='Furnace down? Sunny Home Services gives you a fast diagnosis, upfront '
             'flat-rate repair options and same-day heating service across the Wasatch Front.',
        live='https://sunnyhomeservices.com/furnace-repair-experts/',
        phone='(385) 398-6742',
        season='heating',
        h1=[('Furnace Down?', False),
            ('Let&rsquo;s Get the Heat', True),
            ('Back On.', True)],
        lede='Sunny Home Services fixes any furnace&nbsp;problem.',
        intro_h='Wasatch Front Furnace Repair&nbsp;Experts',
        intro_p=['When your furnace stops working, you need answers fast. We will diagnose '
                 'the problem, explain exactly what&rsquo;s wrong, and give you upfront '
                 'repair options before any work&nbsp;begins.',
                 'Sunny Home Services provides fast, friendly, and dependable heating '
                 'service throughout Salt Lake City, Ogden, and surrounding Northern Utah '
                 'communities. Our experienced technicians will diagnose the problem, '
                 'explain your options, and work quickly to restore comfort to your&nbsp;home.'],
        col1_h='We Fix All Heating Problems&nbsp;Fast',
        col1_p='One furnace problem can quickly turn into an emergency, and the sooner you '
               'call, the more you save. Don&rsquo;t wait to reach out if your furnace&nbsp;is:',
        col1_l=['Not providing heat', 'Making strange sounds', 'Vibrating excessively',
                'Turning on and off too quickly', 'Releasing burning or gas&nbsp;odors'],
        col1_f='If the pilot light won&rsquo;t stay on or your CO alarm goes off, that&rsquo;s '
               'an emergency. Call for help&nbsp;immediately.',
        col1_alert=True,
        col2_h='We Keep Your Home&nbsp;Safe',
        col2_p='When bitter cold grips the region, you need a reliable furnace repair '
               'company. Any time of day, you can count on us&nbsp;for:',
        col2_l=['Same-day heating repair across the Wasatch Front',
                'Furnace, heat pump, and mini-split service',
                'Parts for every system and&nbsp;brand'],
        col2_f='Every repair includes a final test and safety inspection, so your furnace '
               'runs efficiently with no&nbsp;hazards.',
        cta_h='Call Today for Fast Heating&nbsp;Repairs',
        cta_p='Contact Sunny Home Services and we&rsquo;ll be at your home to resolve your '
              'heating emergency, fast. Our well-trained technicians diagnose and fix any '
              'issue. Call or contact us online now for furnace repair in Northern&nbsp;Utah.',
        why_h='Fast, Dependable Furnace Repair&nbsp;Service',
        strip=['Same-Day Heating Repair', 'Furnace, Heat Pump, Mini-Split',
               'Parts For Every System', 'Upfront Flat-Rate Pricing'],
    ),
    dict(
        slug='furnace-replacement-experts',
        title='Furnace Replacement Along the Wasatch Front | Sunny Home Services',
        desc='Sunny Home Services sizes and installs energy-efficient furnaces across the '
             'Wasatch Front, with transparent pricing and a 100% satisfaction guarantee.',
        live='https://sunnyhomeservices.com/furnace-replacement-experts/',
        phone='(385) 404-2530',
        season='heating',
        h1=[('Comfort You Can', False),
            ('Count On All', True),
            ('Season Long', True)],
        lede='Professional furnace replacement along the Wasatch&nbsp;Front.',
        intro_h='Reliable Furnace Replacements for Utah&nbsp;Winters',
        intro_p=['Is your furnace showing its age? Sunny Home Services makes the process '
                 'simple. We&rsquo;ll help you choose a reliable, energy-efficient system '
                 'that is properly sized for your home, with transparent pricing, prompt '
                 'service, and a 100% satisfaction&nbsp;guarantee.',
                 'When your furnace is outdated, struggling to keep up, or no longer '
                 'dependable, Sunny Home Services makes replacement simple. We will assess '
                 'the needs of your home, explain your options clearly, and install a '
                 'properly sized, energy-efficient furnace designed to keep your home '
                 'comfortable through even the coldest Wasatch Front&nbsp;winters.'],
        col1_h='Think You Need a New&nbsp;Furnace?',
        col1_p='Old furnaces can leave you with a lot of headaches. In as little as a day, '
               'we can install a new one, especially if you&rsquo;re dealing with issues&nbsp;like:',
        col1_l=['Frequent repairs', 'High energy bills', 'Inconsistent heating',
                'Unusual odors', 'Constant noises'],
        col1_f='',
        col2_h='How Furnace Replacement Can Be&nbsp;Worth It',
        col2_p='Replacing your heating system brings immediate and long-term benefits. The '
               'upfront cost, which can be offset by manufacturer rebates, utility rebates, '
               'and seasonal promotions, is a direct path&nbsp;to:',
        col2_l=['Up to 40% less on your gas bill (condensing&nbsp;furnace)',
                'Increased safety (sealed combustion, better&nbsp;ventilation)',
                'Improved comfort (modulating burners, variable&nbsp;blowers)'],
        col2_f='Furnaces rated up to 98% AFUE that qualify for rebates and credits offer the '
               'best opportunities to&nbsp;save.',
        cta_h='Call for Furnace Replacements Done&nbsp;Right',
        cta_p='From evaluating your home&rsquo;s heating needs and properly sizing your new '
              'furnace to installation and final system testing, Sunny Home Services handles '
              'every step. Contact our experienced team for clear recommendations and a '
              'straightforward furnace replacement&nbsp;estimate.',
        why_h='Fast, Dependable Furnace Installation',
        strip=['Properly Sized Systems', 'Up To 98% AFUE', 'Financing Available',
               '100% Satisfaction Guarantee'],
    ),
    dict(
        slug='ac-repair-experts',
        title='AC Repair Along the Wasatch Front | Sunny Home Services',
        desc='Sunny Home Services pinpoints the problem and repairs your air conditioner '
             'with upfront flat-rate pricing and same-day service across the Wasatch Front.',
        live='https://sunnyhomeservices.com/ac-repair-experts/',
        phone='(385) 398-6692',
        season='cooling',
        h1=[('Here in the Wasatch', False),
            ('We&rsquo;ll Get Your AC', True),
            ('Running Today', True)],
        lede='Our Utah AC repair experts are here to&nbsp;help.',
        intro_h='Quality Air Conditioner Repairs Along the Wasatch&nbsp;Front',
        intro_p=['In the Wasatch Front&rsquo;s hot, dry summers, AC problems always seem to '
                 'strike at the worst time. Our well-trained professionals pinpoint the issue '
                 'and deliver reliable repairs with upfront, flat-rate pricing and fast, '
                 'same-day&nbsp;service.',
                 'Utah summers can be extremely hot, placing greater demand on your AC '
                 'system. The harder it works, the more likely a small issue can turn into an '
                 'unexpected breakdown. Sunny Home Services keeps your home cool and '
                 'comfortable with flat-rate pricing, same-day appointments, and fast, '
                 'dependable&nbsp;service.'],
        col1_h='Is It Time to Call an AC Repair&nbsp;Company?',
        col1_p='One AC problem can quickly turn into a bigger one, and the sooner you call, '
               'the more you save. Don&rsquo;t wait to reach out if your&nbsp;AC:',
        col1_l=['Starts blowing warm air', 'Refuses to turn on',
                'Doesn&rsquo;t respond to the&nbsp;thermostat',
                'Runs in short cycles or makes loud&nbsp;noises',
                'Leaks water or refrigerant'],
        col1_f='A sudden jump in your electricity bill can also mean your air conditioner '
               'needs professional&nbsp;care.',
        col2_h='How We Fix Your&nbsp;AC',
        col2_p='Our technicians service all makes and models. They arrive promptly in fully '
               'stocked vehicles, diagnose the issue, provide a quote, and begin repairs as '
               'soon as you&nbsp;approve.',
        col2_l=['Capacitor replacement and coil&nbsp;cleaning',
                'Refrigerant recharge and valve&nbsp;repair',
                'Fan motor, blower and compressor&nbsp;repair'],
        col2_f='Experienced and extensively trained, our team also handles condensate drains, '
               'thermostat replacement, electrical components, and much&nbsp;more.',
        cta_h='Call Sunny Home Services&nbsp;Today',
        cta_p='If you live along the Wasatch Front, you can trust us for dependable AC '
              'repairs. Call or book online and we will be out to get your home cool&nbsp;again.',
        why_h='Fast, dependable AC repair service, and lasting comfort through hot,&nbsp;dry&nbsp;summers',
        strip=['Same-Day AC Repair', 'All Makes And Models',
               'Fully Stocked Vehicles', 'Upfront Flat-Rate Pricing'],
    ),
    dict(
        slug='ac-replacement-experts',
        title='AC Replacement Along the Wasatch Front | Sunny Home Services',
        desc='Sunny Home Services sizes and installs high-efficiency air conditioners across '
             'the Wasatch Front, with upfront flat-rate pricing and financing available.',
        live='https://sunnyhomeservices.com/ac-replacement-experts/',
        phone='(385) 398-6646',
        season='cooling',
        h1=[('A New AC System', False),
            ('Built to Last', True)],
        lede='Our Wasatch Front AC installers are here to&nbsp;help.',
        intro_h='Fast, Dependable AC Replacement in the Wasatch&nbsp;Front',
        intro_p=['Needing an AC replacement is often unexpected, but it doesn&rsquo;t have to '
                 'feel overwhelming. Our experienced team keeps the process simple and '
                 'stress-free, from helping you choose the right system to completing a '
                 'smooth, professional&nbsp;installation.',
                 'Sunny Home Services is your go-to AC company in Northern Utah, whether '
                 'you&rsquo;re replacing your existing system or adding air conditioning to '
                 'your home for the first time. We understand that a new AC system is a major '
                 'investment, so our friendly, knowledgeable team will guide you through your '
                 'options, answer your questions, and keep the entire process simple from the '
                 'initial consultation through&nbsp;installation.'],
        col1_h='Time for a New Air&nbsp;Conditioner?',
        col1_p='If your AC is less than a decade old, repairing it usually makes sense. We '
               'generally recommend a replacement if your air&nbsp;conditioner:',
        col1_l=['Is 12 to 15+ years&nbsp;old', 'Often needs repairs',
                'Doesn&rsquo;t cool your entire&nbsp;home', 'Uses R-22 refrigerant',
                'Stops running efficiently'],
        col1_f='If repairs cost 50% or more of a new system, or energy bills spike with no '
               'change in usage, replacement can save you&nbsp;more.',
        col2_h='Why Replacing Your AC Is a Good&nbsp;Idea',
        col2_p='Utah&rsquo;s dry air strains cooling systems over time. Beyond avoiding '
               'repairs, a new AC&nbsp;brings:',
        col2_l=['Lower energy bills (high-SEER&nbsp;systems)',
                'Improved comfort (Manual J load&nbsp;calculation)',
                'Full coverage (warranty and workmanship&nbsp;guarantee)'],
        col2_f='We offer financing, so your replacement is covered with low monthly payments. '
               'Discounts, rebates, and tax credits may also be&nbsp;available.',
        cta_h='Schedule an In-Home Assessment&nbsp;Today',
        cta_p='Our team calculates your home cooling needs and recommends the best AC options '
              'with upfront, flat-rate pricing. For same-day service and a free quote, contact '
              'Sunny Home Services&nbsp;today.',
        why_h='Fast, dependable AC replacement service, and lasting comfort through hot,&nbsp;dry&nbsp;summers',
        strip=['Properly Sized Systems', 'High-SEER Systems', 'Financing Available',
               'Warranty And Workmanship Guarantee'],
    ),
]

# The review asked for the furnace sections to stop showing air conditioning.
TILES = {
    'heating': ('Furnace Service to Beat the&nbsp;Cold', [
        ('card-heating-repair.webp', 'Furnace Repair', 'furnace-repair.html',
         'Fast, dependable repairs for all makes and&nbsp;models.'),
        ('card-heating-install.webp', 'Furnace Installation', 'furnace-installation.html',
         'High-efficiency systems sized right for your home, with financing&nbsp;available.'),
        ('card-heating-maintenance.webp', 'Furnace Tune-Up', 'furnace-maintenance.html',
         'A seasonal inspection that keeps the heat on through a Utah&nbsp;winter.'),
        ('card-heating-emergency.webp', 'Emergency Heating Repair', 'emergency-heating-repair.html',
         'No heat overnight or on a weekend. We answer and we&nbsp;come.'),
    ]),
    'cooling': ('AC Service Built for Utah&nbsp;Summers', [
        ('card-ac-repair.webp', 'AC Repair', 'ac-repair.html',
         'Fast, dependable repairs for all makes and&nbsp;models.'),
        ('card-ac-install.webp', 'AC Installation', 'ac-installation.html',
         'High-efficiency systems sized right for your home, with financing&nbsp;available.'),
        ('card-ac-maintenance.webp', 'AC Tune-Up', 'ac-maintenance.html',
         'A seasonal inspection that heads off a breakdown in July.'),
        ('card-ac-emergency.webp', 'Emergency AC Repair', 'emergency-ac-repair.html',
         'No cool air on the hottest day of the year. We answer and we&nbsp;come.'),
    ]),
}

BANDS = {
    'heating': dict(intro='heroes/heating.webp',
                    problems='heroes/furnace-repair.webp',
                    hero='hero-van.webp',
                    heroalt='Sunny Home Services branded service van',
                    icon1='flame', icon2='shield'),
    'cooling': dict(intro='heroes/cooling.webp',
                    problems='heroes/ac-repair.webp',
                    hero='hero-van.webp',
                    heroalt='Sunny Home Services branded service van',
                    icon1='spark', icon2='clock'),
}

TEAM_PHOTO = {'heating': ('team-heating.webp', 'Sunny Home Services technician servicing a furnace'),
              'cooling': ('team-air-conditioning.webp', 'Sunny Home Services technician servicing an air conditioner')}

# Offers come from the live offers page. Heating pages lead with heating.
OFFERS_HEATING = [
    ('is-gold', '$500', '', 'Off a New Furnace Install'),
    ('is-sky', '$49', '', 'Furnace Tune-Up'),
    ('is-gold', '$98', '', 'Super Tune-Up (AC &amp; Furnace)'),
    ('is-sky', '$1,500', 'is-long', 'Off a New High-Efficiency Full System Install'),
    ('is-gold', 'Don&rsquo;t Pay<br>Till 2027', 'is-small', 'Financing'),
    ('is-sky', '10%', '', 'Off Any Repair'),
]

OFFERS_COOLING = [
    ('is-sky', '$1,500', 'is-long', 'Off a New High-Efficiency Full System Install'),
    ('is-gold', '$49', '', 'A/C Tune-Up'),
    ('is-sky', '$98', '', 'Super Tune-Up (AC &amp; Furnace)'),
    ('is-gold', 'Don&rsquo;t Pay<br>Till 2027', 'is-small', 'Financing'),
    ('is-sky', '10%', '', 'Off Any Repair'),
    ('is-gold', '$500', '', 'Off a New Furnace Install'),
]
OFFERS = {'heating': OFFERS_HEATING, 'cooling': OFFERS_COOLING}

SAME_DAY = {'heating': 'Same-day response for no-heat emergencies, with clear '
                       'arrival&nbsp;windows.',
            'cooling': 'Same-day response for no-cool emergencies, with clear '
                       'arrival&nbsp;windows.'}

WHY_POINTS = [
    ('Friendly, well-trained technicians:', 'Background-checked and drug-tested, with an '
     'arrival text and a technician bio sent before we knock on your&nbsp;door.'),
    ('Licensed, insured, and bonded:', 'EPA- and RMGA-certified, so your technician is '
     'trained to industry standards and works to&nbsp;code.'),
    ('Upfront, flat-rate pricing:', 'You see the price and approve it before any work '
     'begins, so there are no surprises on the&nbsp;bill.'),
]


# --------------------------------------------------------------------- render

HEAD = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <!-- Production URL: {live} -->
  <!-- Ad landing page. It is not in the menu; traffic comes from ads only.
       Rebuilt {date} in the site design. The page it replaced was a copy of the
       client's live landing page and carried air conditioning tiles under a
       furnace heading, a NATE badge, an EPA "Approved" badge and four
       placeholder reviews. See tools/expertslp.py. -->
  <!-- The call-tracked number for this page is {phone}. The header keeps the main
       office number, the way the live landing page has it. -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo+Black&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/sunny-engine.css?v=7">
  <link rel="stylesheet" href="css/sunny-landing.css?v=7">
  <link rel="stylesheet" href="css/sunny-hub.css?v=4">
  <link rel="stylesheet" href="css/sunny-home.css?v=2">
</head>
<body>
'''

HERO = '''
  <!-- 01 Hero -->
  <section class="section section-hero section-hero-split has-lp-strip" id="hero">
    <div class="hero-art"><img src="assets/hero-brand-art.webp" alt=""></div>
    <div class="hero-scrim"></div>
    <div class="hero-van-panel">
      <img class="hero-video" src="assets/{heroimg}" alt="{heroalt}">
    </div>

    <div class="container hero-content">
      <h1 class="display-hero hero-title-interactive" id="hero-title">
{h1}      </h1>
      <p class="lead lead-on-video">{lede}</p>
      <div class="cta-row">
        <a class="btn btn-primary btn-pill btn-lg" href="#contact">Book&nbsp;Now</a>
        <a class="btn btn-outline-light btn-pill btn-lg btn-call-lp" href="tel:{tel}">Call&nbsp;{phone}</a>
      </div>
      <p class="lp-hero-meta">Same-day appointments. Open 7am to 7pm, Monday to&nbsp;Friday.</p>
    </div>

    <!-- The strip answers the question someone with no heat is actually asking.
         Every line is the client's own wording from this page. -->
    <div class="hero-subnav lp-hero-strip">
      <div class="container subnav-track">{strip}</div>
    </div>
  </section>
'''

INTRO = '''
  <!-- 03 Opening copy, word for word from the live landing page. The photo
       behind it carries the season: a furnace on the heating pages. -->
  <section class="section lp-band lp-band-intro{cool} reveal" data-animation="fade-up" id="intro">
    <div class="section-bg"><img src="assets/{bg}" alt="" data-parallax="12"></div>
    <div class="lp-wash"></div>
    <div class="container">
      <h2 class="display-h1 align-center">{h}</h2>
      <div class="hub-prose">{p}</div>
    </div>
  </section>
'''

SPLIT = '''
  <!-- 04 The two lists from the live landing page, on cards over a seasonal
       photo. They used to sit on a flat grey fill. -->
  <section class="section lp-band lp-band-problems reveal" data-animation="fade-up" id="problems">
    <div class="section-bg"><img src="assets/{bg}" alt="" data-parallax="14"></div>
    <div class="lp-wash"></div>
    <div class="container">
      <div class="lp-grid">
        <div class="lp-card is-warm">
          <div class="lp-card-icon" aria-hidden="true">{icon1}</div>
          <h2 class="display-h2">{h1}</h2>
          <div class="hub-prose"><p>{p1}</p></div>
          <ul class="check-list">{l1}</ul>
          {f1}
        </div>
        <div class="lp-card is-cool">
          <div class="lp-card-icon" aria-hidden="true">{icon2}</div>
          <h2 class="display-h2">{h2}</h2>
          <div class="hub-prose"><p>{p2}</p></div>
          <ul class="check-list">{l2}</ul>
          {f2}
        </div>
      </div>
    </div>
  </section>
'''

SVG = dict(
    flame='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="M12 2s4 4.5 4 8a4 4 0 0 1-8 0c0-1.3.5-2.4 1-3.2"/>'
          '<path d="M8.5 13A5.5 5.5 0 0 0 12 22a5.5 5.5 0 0 0 3.5-9"/></svg>',
    shield='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" '
           'stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 4 5.5v6c0 5 3.4 9.2 8 10.5 '
           '4.6-1.3 8-5.5 8-10.5v-6L12 2z"/><path d="m9 12 2 2 4-4"/></svg>',
    clock='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" '
          'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/>'
          '<path d="M12 7v5l3 2"/></svg>',
    spark='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"/></svg>',
    alert='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>'
          '<path d="M12 9v4"/><path d="M12 17h.01"/></svg>',
)

TILESEC = '''
  <!-- 05 Service tiles. Every tile on a heating page is a heating service. -->
  <section class="section section-services reveal" data-animation="fade-up" id="services" data-block="service-tiles">
    <div class="section-bg section-bg-faint"><img src="assets/bg/neighborhood.webp" alt="" data-parallax="12"></div>
    <div class="bg-orb bg-orb-sky" style="top:-200px; left:-200px; width:540px;"></div>
    <div class="bg-orb bg-orb-orange" style="bottom:-220px; right:-100px; width:420px;"></div>
    <div class="container">
      <h2 class="display-h1 align-center">{h}</h2>
      <div class="ac-tiles">{tiles}</div>
    </div>
  </section>
'''

WHY = '''
  <!-- 06 Why choose us, the live landing page's four reasons -->
  <section class="section section-why reveal" data-animation="fade-up" id="why" data-block="why-split">
    <div class="section-bg section-bg-faint"><img src="assets/bg/tools.webp" alt="" data-parallax="12"></div>
    <div class="container">
      <div class="hub-split">
        <div>
          <h2 class="display-h2">Why Choose Sunny Home&nbsp;Services</h2>
          <div class="hub-prose"><p>{sub}</p></div>
          <ul class="check-list">{points}</ul>
          <div class="cta-row" style="margin-top:28px;">
            <a class="btn btn-primary btn-pill btn-lg" href="#contact">Book&nbsp;Now</a>
            <a class="btn btn-outline btn-pill btn-lg btn-call-lp" href="tel:{tel}">Call&nbsp;{phone}</a>
          </div>
        </div>
        <div class="hub-split-media">
          <img src="assets/services/{img}" alt="{alt}" data-parallax="6">
        </div>
      </div>
    </div>
  </section>
'''

SPECIALS = '''
  <!-- 07 Offers, from the live offers page. Heating offers lead on a heating page. -->
  <section class="section section-specials reveal" data-animation="fade-up" id="specials">
    <div class="section-bg"><img src="assets/bg/ac-unit.png" alt="" data-parallax="15"></div>
    <div class="accent-stripe accent-stripe-orange"></div>
    <div class="bg-orb bg-orb-sky" style="top:-100px; right:-100px; width:460px;"></div>
    <div class="bg-orb bg-orb-orange" style="bottom:-160px; left:-120px; width:320px;"></div>
    <div class="container">
      <h2 class="display-h1 align-center">Current Specials and&nbsp;Offers</h2>
      <p class="lead align-center">Mention the one you want when&nbsp;you&nbsp;call.</p>
      <div class="offers-marquee">
        <div class="marquee-track" data-duration="46">{chips}</div>
      </div>
      <p class="align-center" style="margin-top:22px;">
        <a class="btn btn-outline btn-pill btn-lg" href="offers.html">View All&nbsp;Offers</a>
      </p>
    </div>
  </section>
'''

CTA = '''
  <!-- 09 Closing call to action, word for word from the live landing page -->
  <section class="section section-cta-banner reveal" data-animation="fade-up" id="cta" data-block="final-cta">
    <div class="section-bg"><img src="assets/bg/neighborhood.webp" alt="" data-parallax="15"></div>
    <div class="cta-overlay"></div>
    <div class="container">
      <h2 class="display-h1">{h}</h2>
      <p>{p}</p>
      <div class="cta-row-center">
        <a class="btn btn-primary btn-pill btn-lg" href="#contact">Book&nbsp;Now</a>
        <a class="btn btn-outline-light btn-pill btn-lg btn-call-lp" href="tel:{tel}">Call&nbsp;{phone}</a>
      </div>
    </div>
  </section>
'''

NO_REVIEWS = '''
  <!-- Reviews. The live landing page carries four reviews signed "Customer A" to
       "Customer D" and a five star rating. None of it is real: Sunny is a new
       company with no public reviews yet, and the rating has no source. The same
       block was removed from the home page for the same reason (see index.html).
       The client's review asked for actual reviews. Restore this section the day
       real ones exist. Sister-company reviews are not usable: different business. -->
'''


def headline(lines):
    """Hero title, built the way the home page builds it: one span per word, so
    the shared hover styling and the white type both apply. Each line stays on
    one line, so no single word is left stranded at the end."""
    out = ''
    for n, (text, alt) in enumerate(lines, 1):
        cls = 'hero-line hero-line-' + ('2' if alt else '1')
        words = ''.join(
            f'<span class="word{" alt-font" if alt else ""}">{w}</span>\n          '
            for w in text.split(' '))
        out += f'        <span class="{cls}">\n          {words.rstrip()}\n        </span>\n'
    return out


def chip(tone, value, size, label):
    sz = (' ' + size) if size else ''
    return (f'''
          <div class="offer-chip-wrap">
            <div class="offer-chip {tone}">
              <div class="offer-chip-stub"><div class="offer-chip-value{sz}">{value}</div></div>
              <div class="offer-chip-main"><div class="offer-chip-label">{label}</div></div>
            </div>
          </div>''')


def checks(items):
    out = ''
    for it in items:
        if isinstance(it, tuple):
            body = f'<strong>{it[0]}</strong> {it[1]}'
        else:
            body = it
        out += (f'''
            <li class="check"><span class="check-badge">&#10003;</span>'''
                f'''<span class="check-text">{body}</span></li>''')
    return out


def strip(items):
    out = ''
    for n, it in enumerate(items):
        if n:
            out += '<span class="dot"></span>'
        out += f'<span>{it}</span>'
    return out


def footnote(text, alert):
    """The line that closes a list. The one about a CO alarm is an emergency, so
    it is set apart rather than left to read as one more bullet."""
    if not text:
        return ''
    if alert:
        return f'<p class="lp-alert">{SVG["alert"]}<span>{text}</span></p>'
    return f'<p class="lp-note">{text}</p>'


def tile(img, name, href, desc):
    return (f'''
        <a class="ac-tile" href="{href}">
          <div class="ac-tile-img" data-parallax="6" style="background-image:url('assets/services/{img}')"></div>
          <div class="ac-tile-body">
            <div class="ac-tile-title">{name}</div>
            <div class="ac-tile-desc">{desc}</div>
          </div>
        </a>''')


def build(page, home, date):
    tel = phone_href(page['phone'])
    ph = page['phone'].replace(' ', '&nbsp;')

    header = block(home, 'class="site-header"', 'header')
    footer = block(home, '<footer', 'footer')
    # Everything after the footer: the same library tags the home page loads.
    # Lifted rather than retyped, so a version change there reaches these pages.
    tail = home[home.find('</footer>') + len('</footer>'):]
    trust = block(home, 'section-trust-marquee')
    van = block(home, 'about-van-split')
    family = block(home, 'section-family-plan')
    areas = block(home, 'section-areas')
    contact = block(home, 'section-contact')

    # The landing page uses its own tracked number in the body.
    contact = contact.replace('+13858538116', tel).replace('385.853.8116', ph)
    contact = contact.replace('Let&rsquo;s Get Your<br>Home&nbsp;Comfortable',
                              'Request Your Service&nbsp;Now')
    van = van.replace('href="#contact">Meet The&nbsp;Family',
                      'href="#contact">Book&nbsp;Now')

    tiles_h, tiles = TILES[page['season']]
    band = BANDS[page['season']]
    parts = [
        HEAD.format(title=page['title'], desc=page['desc'], live=page['live'],
                    phone=page['phone'], date=date),
        header,
        HERO.format(h1=headline(page['h1']), lede=page['lede'], tel=tel, phone=ph,
                    strip=strip(page['strip']),
                    heroimg=band['hero'], heroalt=band['heroalt']),
        trust,
        INTRO.format(h=page['intro_h'],
                     p=''.join(f'<p>{x}</p>' for x in page['intro_p']),
                     bg=band['intro'],
                     cool=' is-cooling' if page['season'] == 'cooling' else ''),
        SPLIT.format(bg=band['problems'],
                     icon1=SVG[band['icon1']], icon2=SVG[band['icon2']],
                     h1=page['col1_h'], p1=page['col1_p'], l1=checks(page['col1_l']),
                     f1=footnote(page['col1_f'], page.get('col1_alert')),
                     h2=page['col2_h'], p2=page['col2_p'], l2=checks(page['col2_l']),
                     f2=footnote(page['col2_f'], False)),
        TILESEC.format(h=tiles_h, tiles=''.join(tile(*t) for t in tiles)),
        WHY.format(sub=page['why_h'] + '.',
                   points=checks(WHY_POINTS + [('Same-day appointments:',
                                                SAME_DAY[page['season']])]),
                   img=TEAM_PHOTO[page['season']][0],
                   alt=TEAM_PHOTO[page['season']][1], tel=tel, phone=ph),
        van,
        SPECIALS.format(chips=''.join(chip(*c) for c in OFFERS[page['season']]) * 2),
        family,
        NO_REVIEWS,
        CTA.format(h=page['cta_h'], p=page['cta_p'], tel=tel, phone=ph),
        areas,
        contact,
        footer,
        tail,
    ]
    return '\n'.join(parts)


def main():
    import datetime
    date = datetime.date.today().strftime('%B %-d, %Y')
    home = read(HOME)
    for page in PAGES:
        out = os.path.join(ROOT, page['slug'] + '.html')
        open(out, 'w', encoding='utf-8').write(build(page, home, date))
        print('wrote', page['slug'] + '.html')


if __name__ == '__main__':
    main()
