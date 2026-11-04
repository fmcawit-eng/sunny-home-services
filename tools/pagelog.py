#!/usr/bin/env python3
"""
Writes the page log: one row per page, saying what it is, where it lives on
the client's site, which file holds it, where its copy came from, and what
still needs a decision.

Run:  python3 tools/pagelog.py
Out:  tools/pagelog.csv  (handoff_pdf.py renders the PDF from this)
"""
import csv, os, re, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = 'https://sunnyhomeservices.com'
PREV = 'https://sunny-home-services.vercel.app'
TODAY = datetime.date.today()

# ---------------------------------------------------------------- nav map
NAV = [
    ('Cooling', 'air-conditioner.html', [
        ('Air Conditioner Repair', 'ac-repair.html'),
        ('Air Conditioner Installation', 'ac-installation.html'),
        ('Air Conditioner Maintenance', 'ac-maintenance.html'),
        ('Mini-Splits', 'mini-splits.html'),
        ('Heat Pumps', 'heat-pumps.html'),
        ('Emergency Air Conditioner Repair', 'emergency-ac-repair.html')]),
    ('Heating', 'heating.html', [
        ('Furnace Repair', 'furnace-repair.html'),
        ('Furnace Installation', 'furnace-installation.html'),
        ('Furnace Maintenance', 'furnace-maintenance.html'),
        ('Heat Pumps', 'heat-pumps.html'),
        ('Emergency Heating Repair', 'emergency-heating-repair.html')]),
    ('Plumbing', 'plumber.html', [
        ('Water Heater Repair', 'water-heater-repair.html'),
        ('Water Heater Installation', 'water-heater-installation.html'),
        ('Water Heater Maintenance', 'water-heater-maintenance.html'),
        ('Tankless Water Heaters', 'tankless-water-heaters.html'),
        ('Gas Lines', 'gas-lines.html'),
        ('Garbage Disposals', 'garbage-disposals.html'),
        ('Toilets', 'toilets.html'),
        ('Plumbing Fixtures', 'plumbing-fixtures.html'),
        ('Leak Detection', 'leak-detection.html'),
        ('Emergency Plumbing Repair', 'emergency-plumbing-repair.html')]),
    ('Sewer and Drains', 'sewer-and-drains.html', [
        ('Drain Cleaning', 'drain-cleaning.html'),
        ('Sewer Line Repair', 'sewer-line-repair.html'),
        ('Sewer Line Installation', 'sewer-line-installation.html'),
        ('Trenchless Sewer Line Repair', 'trenchless-sewer-line-repair.html'),
        ('Hydro Jetting', 'hydro-jetting.html'),
        ('Camera Inspection', 'camera-inspection.html')]),
    ('Air Quality', 'indoor-air-quality.html', [
        ('Duct Cleaning', 'duct-cleaning.html'),
        ('Whole Home Humidifiers', 'whole-home-humidifiers.html'),
        ('Whole-House Air Purifier', 'whole-house-air-purifier.html'),
        ('Thermostats', 'thermostats.html'),
        ('Ductwork', 'ductwork.html')]),
    ('About Us', 'about.html', [
        ('Meet the Team', 'meet-the-team.html'),
        ('Service Area', 'service-area.html'),
        ('Offers', 'offers.html'),
        ('Membership', 'membership.html'),
        ('Financing', 'financing.html'),
        ('Blog', 'blog.html')]),
    ('Contact Us', 'contact.html', []),
]

# ---------------------------------------------------------------- live URLs
LIVE_URL = {
    'index.html': '/', 'air-conditioner.html': '/air-conditioner/',
    'ac-repair.html': '/air-conditioner/repair/',
    'ac-installation.html': '/air-conditioner/installation/',
    'ac-maintenance.html': '/air-conditioner/maintenance/',
    'emergency-ac-repair.html': '/air-conditioner/emergency-ac-repair/',
    'mini-splits.html': '/mini-splits/', 'heat-pumps.html': '/heat-pumps/',
    'heating.html': '/heating/',
    'furnace-repair.html': '/heating/furnace-repair/',
    'furnace-installation.html': '/heating/furnace-installation/',
    'furnace-maintenance.html': '/heating/furnace-maintenance/',
    'emergency-heating-repair.html': '/heating/emergency-heating-repair/',
    'plumber.html': '/plumber/',
    'water-heater-repair.html': '/plumber/water-heater-repair/',
    'water-heater-installation.html': '/plumber/water-heater-installation/',
    'water-heater-maintenance.html': '/plumber/water-heater-maintenance/',
    'tankless-water-heaters.html': '/plumber/tankless-water-heaters/',
    'gas-lines.html': '/plumber/gas-lines/',
    'garbage-disposals.html': '/plumber/garbage-disposals/',
    'toilets.html': '/plumber/toilets/',
    'plumbing-fixtures.html': '/plumber/fixtures/',
    'leak-detection.html': '/plumber/leak-detection/',
    'emergency-plumbing-repair.html': '/plumber/emergency/',
    'sewer-and-drains.html': '/plumber/sewer-drains/',
    'drain-cleaning.html': '/plumber/drain-cleaning/',
    'sewer-line-repair.html': '/plumber/sewer-line-repair/',
    'sewer-line-installation.html': '/plumber/sewer-line-installation/',
    'trenchless-sewer-line-repair.html': '/plumber/trenchless-sewer-line-repair/',
    'hydro-jetting.html': '/plumber/hydro-jetting/',
    'camera-inspection.html': '/plumber/camera-inspection/',
    'indoor-air-quality.html': '/indoor-air-quality/',
    'duct-cleaning.html': '/indoor-air-quality/duct-cleaning/',
    'whole-home-humidifiers.html': '/indoor-air-quality/whole-home-humidifiers/',
    'thermostats.html': '/indoor-air-quality/thermostats/',
    'ductwork.html': '/indoor-air-quality/ductwork/',
    'about.html': '/about/', 'meet-the-team.html': '/about/meet-the-team/',
    'offers.html': '/about/offers/', 'membership.html': '/about/membership/',
    'financing.html': '/about/financing/', 'service-area.html': '/service-area/',
    'blog.html': '/blog/', 'contact.html': '/contact/',
    'privacy-policy.html': '/privacy-policy/',
    'terms-and-conditions.html': '/terms-and-conditions/',
    'ac-repair-experts.html': '/ac-repair-experts/',
    'ac-replacement-experts.html': '/ac-replacement-experts/',
    'furnace-repair-experts.html': '/furnace-repair-experts/',
    'furnace-replacement-experts.html': '/furnace-replacement-experts/',
}
CITIES = ['cottonwood-heights', 'draper', 'herriman', 'lehi', 'midvale',
          'riverton', 'salt-lake-city', 'sandy', 'south-jordan',
          'taylorsville', 'west-valley']
for c in CITIES:
    LIVE_URL[f'{c}-ut.html'] = f'/{c}-ut/'
    for child in ('air-conditioning', 'heating', 'plumber'):
        LIVE_URL[f'{c}-ut-{child}.html'] = f'/{c}-ut/{child}/'
# Salt Lake City's three children are new; so are Millcreek and Kearns.
for k in ('salt-lake-city-ut-air-conditioning.html',
          'salt-lake-city-ut-heating.html', 'salt-lake-city-ut-plumber.html'):
    LIVE_URL.pop(k, None)

NICE = {
    'index.html': 'Home', 'plumber.html': 'Plumbing',
    'indoor-air-quality.html': 'Air Quality',
    'sewer-and-drains.html': 'Sewer and Drains',
    'air-conditioner.html': 'Cooling', 'heating.html': 'Heating',
    'about.html': 'About Us', 'contact.html': 'Contact Us',
    'coming-soon.html': 'Coming Soon (placeholder)',
    'blog-template.html': 'Blog Template (for dev to duplicate)',
}
def pretty(slug):
    if slug in NICE: return NICE[slug]
    s = slug[:-5]
    s = re.sub(r'^blog-', '', s)
    s = re.sub(r'-ut-', ', UT ', s)
    s = re.sub(r'-ut$', ', UT', s)
    s = s.replace('-', ' ')
    small = {'a','an','and','the','or','for','to','in','of','vs','on','a'}
    out = []
    for i, w in enumerate(s.split()):
        out.append(w if (w.lower() in small and i) else
                   (w.upper() if w.lower() in ('ut','ac','hvac','iaq') else w.capitalize()))
    return ' '.join(out).replace(', Ut', ', UT')

# ---------------------------------------------------------------- what needs a decision
# Keyed by file. Each entry is (what still needs doing, who decides).
NEEDS = {}

for f in ('ac-repair-experts.html', 'ac-replacement-experts.html',
          'furnace-repair-experts.html', 'furnace-replacement-experts.html'):
    NEEDS[f] = ('Mirror of the live ad landing page, kept byte for byte. Its menu '
                'button, Book Now and BBB badge are under 44px on a phone and the '
                'review attributions are 10px. Those come from the live theme, not '
                'from this build, and cannot be reached from our stylesheet.',
                'Client, if they want the live page fixed')

for f in ('privacy-policy.html', 'terms-and-conditions.html'):
    NEEDS[f] = ('Built and styled, but the policy wording is a placeholder. The live '
                'site serves this text from a consent platform rather than the page, '
                'so it could not be pulled and nothing was invented.',
                'Client supplies the wording')

NEEDS['ac-installation.html'] = (
    '"Free Estimate" appears in the page title, the hero line and the closing '
    'paragraph. It is the brief\'s own wording, left as written. Many contractor '
    'markets restrict that phrase, so confirm it before launch.',
    'Client confirms')

NEEDS['blog.html'] = (
    'No publish dates and no author byline anywhere in this set. The content '
    'calendar lists all 13 posts as Scheduled to Post with no date, and no brief '
    'names an author. Also carries the spelling "recognise" in one card, which is '
    'the brief\'s own wording.',
    'Client supplies dates and an author')

NEEDS['blog-template.html'] = (
    'Not a page. This is the file dev duplicates for post 14 onward. It carries '
    'SWAP notes for what changes per post and KEEP notes for what does not.',
    'Dev reference only')

NEEDS['coming-soon.html'] = (
    'Placeholder destination. Every nav or body link whose page is not built yet '
    'points here rather than nowhere.',
    'Resolves as pages get built')

NEEDS['kearns-ut.html'] = (
    'Its brief says "50+ years of combined HVAC and plumbing experience" while '
    'every Millcreek and service page brief says "over 30 years". Both are left as '
    'each brief wrote them. The three Kearns child pages (AC, heating, plumbers) '
    'have no copy yet, so those links point at Coming Soon.',
    'Client decides 30 or 50')

NEEDS['salt-lake-city-ut-plumber.html'] = (
    'The Whole Home Water Filtration tile has nowhere to point: there is no '
    'water filtration page in the build and no brief for one. It goes to Coming '
    'Soon like the other unbuilt services.',
    'Client supplies water filtration copy')

NEEDS['millcreek-ut.html'] = (
    'The Millcreek AC page has no brief yet, so that one link points at Coming '
    'Soon. Heating and Plumbers are built.',
    'Client supplies Millcreek AC copy')

# New pages need nothing; the Status column already says BUILT, NEW.

def copy_source(slug):
    if slug.startswith('blog-') and slug != 'blog-template.html':
        return 'Its own brief doc, verbatim'
    if slug.endswith('-experts.html'):
        return 'Mirrored from the live page'
    if slug in ('privacy-policy.html', 'terms-and-conditions.html'):
        return 'PLACEHOLDER, not real policy text'
    if slug in ('coming-soon.html', 'blog-template.html'):
        return 'Ours (scaffolding, no claims)'
    if re.match(r'^(millcreek|kearns)-ut', slug):
        return 'Its own brief doc, verbatim'
    if re.match(r'^salt-lake-city-ut-', slug) or slug == 'whole-house-air-purifier.html':
        return 'Its own brief doc, verbatim'
    if slug == 'index.html':
        return 'Client brief and their live home page'
    return 'The copywriter brief for this page'

def status(slug):
    if slug == 'blog-template.html': return 'TEMPLATE'
    if slug == 'coming-soon.html': return 'PLACEHOLDER'
    if slug in ('privacy-policy.html', 'terms-and-conditions.html'): return 'PLACEHOLDER'
    if slug not in LIVE_URL: return 'BUILT, NEW'
    return 'BUILT'

def nav_place(slug):
    for top, href, kids in NAV:
        if href == slug: return (top, '')
        for kt, kh in kids:
            if kh == slug: return ('', top)
    if slug == 'index.html': return ('Home (logo)', '')
    if re.match(r'^blog-', slug) and slug != 'blog-template.html': return ('', 'Blog index')
    if re.search(r'-ut(-|\.)', slug): return ('', 'Service Area')
    return ('', '')

# ---------------------------------------------------------------- revisions
REVISIONS = [
    ('November 4, 2026', 'No flat bands',
     'Every band on a service or city page now carries a washed texture. The '
     'alternating tone bands were a flat fill with their texture switched off, '
     'and 22 bands across 21 pages had no texture at all.'),
    ('November 4, 2026', 'Lists and steps',
     'Ticked items read as cards with a gold edge rather than loose lines, so a '
     'short item no longer sits beside empty space. Numbered steps run across in '
     'one row. On the Salt Lake City plumbing page the service list became linked '
     'tiles, so each service reaches its own page; it was prose with no way '
     'through. That page lost 600px.'),
    ('November 4, 2026', 'Bold',
     'The body font mapped every weight onto one medium file, so bold text '
     'rendered no differently from the text around it. The 700 weight was already '
     'in assets/fonts and unused; it is now wired to weights 600 and above.'),
    ('November 4, 2026', 'Service tiles, round two',
     'The West Jordan plumbing page moved from eight photo cards to the same '
     'tiles the city pages use, run across the full column so every service '
     'title fits one line. Its eight mismatched illustrations came out; the '
     'twelve links inside that copy were kept. That section went from 2,046px '
     'to 791px.'),
    ('November 4, 2026', 'Checklists',
     'A ticked list inside a heading rail ran as one tall column, so a short '
     'item held a whole line and left the rest empty. Two columns now, with a '
     'lone last item taking the full width. The sub-headings that follow a list '
     'no longer sit straight on top of it, and the line that introduces a list '
     'reads as a lead-in rather than body copy.'),
    ('November 4, 2026', 'Artwork',
     'Removed the three remaining plumbing illustrations that used a stand-in '
     'sun with the wrong cap. Nothing references them now. The corrected '
     'fixtures illustration stays in assets/services/ and is not in use.'),
    ('November 4, 2026', 'Service tiles',
     'Replaced the photo service cards on the city pages with compact tiles. A '
     'photo per service made those sections three screens tall and forced the '
     'same artwork onto unrelated services. Each set now lands in two rows.'),
    ('November 4, 2026', 'Artwork',
     'Redrew the plumbing fixtures card. The earlier one had a stand-in sun '
     'character with the wrong cap rather than the brand mascot. The gas line, '
     'garbage disposal and toilet cards on the plumbing page still have the same '
     'problem and are waiting on a decision.'),
    ('November 4, 2026', 'Typography',
     'Turned 136 straight apostrophes into curly ones across 22 pages, which had '
     'been mixed with 1,630 curly ones, and closed three stray spaces before a '
     'comma or a period. No wording changed. The four mirrored pages were left '
     'untouched so they still match the live site.'),
    ('November 4, 2026', 'Millcreek and Kearns',
     'Built four service-area pages from the approved briefs: the Millcreek hub, '
     'Millcreek heating, Millcreek plumbers and the Kearns hub. Both cities added '
     'to the grids on the home page and the service area page.'),
    ('November 4, 2026', 'Phones',
     'Raised every tap target to 44px across all pages: menu button, header and '
     'footer links, breadcrumbs, service area chips, buttons, ZIP titles, form '
     'submits and card links. Fixed a checklist tick that sat level with the '
     'middle of a wrapped line instead of its first line.'),
    ('November 4, 2026', 'Page rhythm',
     'Rolled the Kliemann-style layout across the service pages: a sticky heading '
     'rail beside the text, alternating tinted bands, and full-bleed photo splits, '
     'so a page no longer reads as one centered column all the way down.'),
    ('November 4, 2026', 'Housekeeping',
     'Corrected three pages whose developer comment still carried Lehi\'s '
     'production URL. Gave a lone trailing service card the full row.'),
    ('November 3, 2026', 'Blog',
     'Built the blog: an index, 13 articles from their briefs, and an annotated '
     'template for dev to duplicate. Restructured the article layout into '
     'two-column chapters after review.'),
    ('November 3, 2026', 'Client notes',
     'Added license number 14291812-5501 and Instagram and Facebook links to the '
     'footer of every page. Evened out the service card icons and turned the '
     'bulleted copy back into paragraphs on the two pages named.'),
    ('November 3, 2026', 'New pages',
     'Built Salt Lake City AC, heating and plumber, plus the whole-house air '
     'purifier page, from the supplied briefs.'),
    ('November 3, 2026', 'West Jordan',
     'Put West Jordan back where the briefs had it. The live site had the city '
     'swapped for the region by a find and replace, which left titles reading '
     '"Wasatch Front, UT", a "Wasatch Front Building and Safety Division" that '
     'does not exist, and one city\'s elevation applied to a 120-mile region. '
     'Not yet confirmed by the client.'),
]

def main():
    files = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, '*.html')))
    rows = []
    for slug in files:
        top, parent = nav_place(slug)
        live = LIVE_URL.get(slug, '')
        need, who = NEEDS.get(slug, ('', ''))
        rows.append({
            'Page Name': pretty(slug),
            'Nav Bar': top,
            'Drop Down Parent': parent,
            'Status': status(slug),
            'HTML File': slug if slug != 'index.html' else 'home-page.html',
            'Preview URL': PREV + ('/' if slug == 'index.html'
                                   else '/' + slug[:-5]),
            'Live Page Today': (LIVE + live) if live else 'Not live yet',
            'Where Copy Came From': copy_source(slug),
            'Needs a Change or a Decision': need,
            'Who Decides': who,
        })

    out = os.path.join(ROOT, 'tools', 'pagelog.csv')
    with open(out, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow([f'Sunny Home Services, Developer Handoff'])
        w.writerow(['Generated', TODAY.strftime('%B %-d, %Y'),
                    'Preview', PREV, 'Live site', LIVE])
        w.writerow([])
        w.writerow(['SUMMARY'])
        total = len(rows)
        built = sum(1 for r in rows if r['Status'].startswith('BUILT'))
        new   = sum(1 for r in rows if r['Status'] == 'BUILT, NEW')
        ph    = sum(1 for r in rows if r['Status'] == 'PLACEHOLDER')
        needs = sum(1 for r in rows if r['Who Decides'].startswith(('Client', 'Dev '))
                    and r['Who Decides'] != 'Dev reference only')
        w.writerow(['HTML files in this package', total])
        w.writerow(['  of those, BUILT and matching a live page', built - new])
        w.writerow(['  of those, BUILT and NEW (no live page yet)', new])
        w.writerow(['  of those, PLACEHOLDER (wording still needed)', ph])
        w.writerow(['  of those, a TEMPLATE for dev to duplicate',
                    sum(1 for r in rows if r['Status'] == 'TEMPLATE')])
        w.writerow(['Pages waiting on a client decision', needs])
        w.writerow([])
        w.writerow(['STATUS KEY'])
        w.writerow(['BUILT', 'Finished. A page of the same name is already live.'])
        w.writerow(['BUILT, NEW', 'Finished. Nothing like it is live yet.'])
        w.writerow(['PLACEHOLDER', 'Built and styled, but the wording is not real yet.'])
        w.writerow(['TEMPLATE', 'Not a page. The file dev duplicates to make more.'])
        w.writerow([])
        w.writerow(['COPY POLICY'])
        w.writerow(['', 'No claim about the client was invented. Every line traces to '
                        'their live site or to a brief they supplied.'])
        w.writerow(['', 'Where their own copy reads oddly it was left as written and '
                        'listed in the column below, never quietly changed.'])
        w.writerow([])
        w.writerow(list(rows[0].keys()))
        for r in rows:
            w.writerow(list(r.values()))
        w.writerow([])
        w.writerow(['REVISION LOG'])
        w.writerow(['Date', 'Area', 'What changed'])
        for d, a, t in REVISIONS:
            w.writerow([d, a, t])
    open_items = sum(1 for r in rows if r['Who Decides'].startswith('Client'))
    print(f'{out}  ({len(rows)} pages, {open_items} waiting on the client)')
    return rows

if __name__ == '__main__':
    main()
