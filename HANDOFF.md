# Sunny Home Services — Build Spec (WordPress / Elementor)

**Live preview:** https://sunny-home-services.vercel.app
**Sitemap / SEO source of truth:** the **Sunny Home Services SEO Workbook** (spreadsheet) — the authoritative page list, production URLs, nav, keyword targets, and service areas. This doc mirrors it; when they differ, the spreadsheet wins.
**Design source of truth:** the Figma file (link in [README](README.md)).
**Visual QA references:** [`handoff/home-full.jpg`](handoff/home-full.jpg) · [`handoff/hub-air-conditioner-full.jpg`](handoff/hub-air-conditioner-full.jpg) · [`handoff/child-ac-repair-full.jpg`](handoff/child-ac-repair-full.jpg) · [`handoff/service-area-full.jpg`](handoff/service-area-full.jpg) · [`handoff/coming-soon-full.jpg`](handoff/coming-soon-full.jpg)

This repo is the approved static prototype (West Jordan / Wasatch Front, UT —
HVAC + Plumbing, leading with HVAC). It was authored as **Elementor-ready
markup** — the CSS already carries a token system mapped to Elementor's Global
roles. Treat it as a **build spec, not a mockup**: a port into Elementor, not a
redesign.

**Ground rules**
1. **Copy is final** — use the text in the pages. Don't rewrite.
2. **Phone is `385.853.8116`** everywhere (`tel:+13858538116`).
3. **Build 3–4 templates**, not one-off pages — the whole site is templated
   (Homepage · Service Hub · Service Child · Service Area). Populate them **per
   the SEO Workbook sitemap.**
4. **Not-yet-built pages route to `coming-soon.html`** until their content ships.

---

## 1. Global settings (do this first)

Tokens live in [`css/sunny-engine.css`](css/sunny-engine.css) `:root`, already
annotated with their Elementor role. Put them in **Elementor → Site Settings →
Global Colors / Fonts**.

### Colors

| Token | Hex | Elementor role / use |
|---|---|---|
| `--sky` | `#04cfff` | **Sunny Blue** — brand blue, links, accents |
| `--sky-deep` | `#03A6CC` | **Elementor Primary** — dark section backgrounds |
| `--sky-darker` | `#0288a8` | deepest blue, gradient ends |
| `--yellow` / `--sun-gold` | `#FFC704` | **Elementor Secondary** — CTA / warm accent |
| `--orange` | `#F17601` | sun-gradient start, coupon accents |
| `--ink` / `--charcoal` | `#454545` | **Elementor Text** — body copy |
| `--muted` | `#6B7480` | secondary text |
| `--off-sky` | `#e6fbff` | light blue tint backgrounds |
| `--sand` | `#FAF4ED` | warm section background (specials) |
| `--white` | `#ffffff` | paper |
| `--hairline` | `#DBE3E6` | borders, dividers |
| `--sun-gradient` | `linear-gradient(90deg, #F17601 0%, #FFC704 100%)` | signature orange→yellow "sun" gradient (CTAs, ribbons, accents) |

**Container:** `1280px` (`--container`).

### Fonts

| Role | Font | Notes |
|---|---|---|
| Display | **Degular** | headlines; local `@font-face`. **Licensed foundry font** — confirm the client's web license or substitute + upload as an Elementor Custom Font. |
| Body | **Rubik** | body copy. Free Google Font → Global Font. |
| Accent | **Archivo Black** | a few display accents; free Google Font. |

### Buttons / motifs
Primary CTA = the **sun-gradient pill** (`--sun-gradient`, white text, pill
radius, hover lift). Recurring motifs: trust marquee, rotating sun-burst behind
Mr. Sunny (About), scroll reveals. Reuse the CSS in `css/`.

---

## 2. Production URL structure & full sitemap (from the SEO Workbook)

**Heads-up — filenames ≠ production URLs.** The prototype uses flat filenames
(`ac-repair.html`); the production site uses **nested URLs**. Build the nested
hierarchy below in WordPress; the flat files are just the prototype.

### Batch 1 — BUILT (this mockup)

| Prototype file | → Production URL | Template |
|---|---|---|
| `index.html` | `/` | Homepage |
| `air-conditioner.html` | `/air-conditioner/` | Hub (Cooling) |
| `ac-repair.html` | `/air-conditioner/repair/` | Child |
| `ac-installation.html` | `/air-conditioner/installation/` | Child |
| `ac-maintenance.html` | `/air-conditioner/maintenance/` | Child |
| `emergency-ac-repair.html` | `/air-conditioner/emergency-ac-repair/` | Child |
| `mini-splits.html` | `/mini-splits/` | Hub/Child |
| `heat-pumps.html` | `/heat-pumps/` | Hub/Child |
| `heating.html` | `/heating/` | Hub (Heating) |
| `furnace-repair.html` | `/heating/furnace-repair/` | Child |
| `furnace-installation.html` | `/heating/furnace-installation/` | Child |
| `furnace-maintenance.html` | `/heating/furnace-maintenance/` | Child |
| `emergency-heating-repair.html` | `/heating/emergency-heating-repair/` | Child |
| `indoor-air-quality.html` | `/indoor-air-quality/` | Hub (IAQ) |
| `service-area.html` | `/service-area/` | Service Area hub |
| `coming-soon.html` | (placeholder) | Coming-soon |

### Planned — NOT yet built (link these to `coming-soon.html` for now)

- **Plumbing hub** `/plumber/` + children: water-heater-repair / -installation /
  -maintenance, tankless-water-heaters, gas-lines, garbage-disposals, toilets,
  fixtures, leak-detection, emergency
- **Sewer & Drains** `/plumber/sewer-drains/` + children: drain-cleaning,
  sewer-line-repair, sewer-line-installation, trenchless-sewer-line-repair,
  hydro-jetting, camera-inspection
- **IAQ children:** `/indoor-air-quality/` duct-cleaning, whole-home-humidifiers,
  thermostats, ductwork
- **About** `/about/` + meet-the-team, plus Offers, Membership, Financing, Blog
  (+ blog post / category / author templates)
- **City pages** (per the Service Area hub — city + city-service templates)
- 404, Privacy Policy, HTML Sitemap

> The full, current list of pages + priorities lives in the SEO Workbook. Build
> from it; this table is the snapshot at handoff.

### Nav mega-menu (authoritative — from the Workbook, already in the markup)

7 groups: **Cooling** (`/air-conditioner/`) · **Heating** (`/heating/`) ·
**Plumbing** (`/plumber/`) · **Sewer & Drains** (`/plumber/sewer-drains/`) ·
**Air Quality** (`/indoor-air-quality/`) · **About Us** (`/about/`) · **Contact
Us** (`/contact/`). Each dropdown's children match §2's URLs. Build as an
Elementor Mega-Menu header template; unbuilt items point to `coming-soon.html`.
Footer = 4-column link grid + contact (footer template).

---

## 3. Homepage template (`index.html`) — 12 sections

Container `1280px`, top to bottom:

| # | Section (id/class) | Background | What it is | Elementor |
|---|---|---|---|---|
| 1 | `hero` | full-cover **video** (`assets/hero2.mp4`) | Interactive headline "HVAC & Plumbing Company in West Jordan, UT" + CTAs | Video-bg section; headline interactivity = keep `sunny-engine.js` (§5) |
| 2 | `section-trust-marquee` | dark blue | 8 auto-scrolling credential pills | Marquee (JS) or wrap row |
| 3 | `intro` | white | "HVAC & Plumbing Built for the Wasatch Front" + copy | Heading + Text |
| 4 | `services` | white | Service grid (image cards) | Image-box grid; `#services` anchor |
| 5 | `why` | white | "Experienced HVAC & Plumbing team…" + tools photo | 2-col text + image |
| 6 | `about` | image bg | Van + sister-brand copy + **3 stat cards** (scroll counters) | Section; counters = JS or Counter widget |
| 7 | `specials` | **sand** `#FAF4ED` | Coupons ($49 tune-up, $50 off) + "Sunny Deal" ribbon | Container + custom CSS; `#specials` |
| 8 | `family-plan` | dark cyan | Membership benefits | Section; `#family-plan` |
| 9 | `locations` | image bg | Map + city links | Image + links; `#locations` |
| 10 | `faq` | white | FAQ accordion | Accordion widget |
| 11 | `cta` | dark/gradient | "Schedule … Today" + CTAs | Section + buttons |
| 12 | `contact` | image bg | Contact form + info card | Form widget; `#contact` |

The **rotating sun-burst mascot** (About) is the signature visual — keep the CSS
star; the mascot counter-rotates to stay upright.

---

## 4. Hub, Child, Service-Area & Coming-Soon templates

- **Hub / category** (e.g. `air-conditioner.html`) — `hero` (page hero from
  `assets/heroes/…`) → `intro` → `services` (child cards linking down) →
  `what-to-expect` → `why` → `cta` → `faq`. One template; swap hero/copy/cards per hub.
- **Child / service** (e.g. `ac-repair.html`) — `hero` → `intro` → `certified` →
  `common-problems` → `repair-vs-replace` → `why` → `what-to-expect` → `specials`
  → `cta` → `faq`. One template; swap per page. Some children omit a block or two.
- **Service Area** (`service-area.html`) — hero → "Services Near You" + **city
  pills** → services overview → positioning → CTA. Feeds the future **City pages**.
- **Coming-Soon** (`coming-soon.html`) — "This Page Is Coming Soon" + CTAs +
  "Explore Our Services" cards. All unbuilt sitemap links route here.

**Per-page assets are organized:** `assets/heroes/<page>.jpg` (page heroes),
`assets/services/card-*.jpg` (service cards), `assets/bg/*` (section bg photos),
brand (`sunny-logo.png`, `sunny-mascot.png`, `brand-logo.png`, `brand-ray.png`,
`van2-current.jpg`, community-van / service-area images), `assets/fonts/`.

---

## 5. Animation & interactions

All JS is in [`js/sunny-engine.js`](js/sunny-engine.js) (Lenis + GSAP/ScrollTrigger):

| Feature | Elementor approach |
|---|---|
| Hero interactive headline (type-in, hover-lift, click-pop, parallax) | **no native equivalent — keep this JS.** The signature moment. |
| Section reveals (`.reveal`) | native entrance animations |
| Parallax (`[data-parallax]`) | native scrolling effects |
| Trust marquee, stat counters | keep JS, or marquee / Counter widget |
| Booking / family-plan tiles | small JS, or Tabs |
| Contact form success | Form widget success + real endpoint |

Keep `sunny-engine.js` for the hero + marquee + counters; use native motion for
generic reveals. Everything degrades gracefully without JS
(`prefers-reduced-motion` respected).

---

## 6. Service areas & SEO context (from the Workbook)

- **Serve:** Salt Lake, Utah, Davis, Weber Counties — **Provo → Ogden**. Start
  near West Jordan. GBP cities: West Valley, West Jordan, Lehi, Sandy, South
  Jordan, Herriman, Taylorsville, Draper, Riverton, Midvale, Cottonwood Heights,
  Salt Lake City, Copperton, Magna, North Salt Lake, West Bountiful, Kearns,
  Bountiful, Millcreek, Bluffdale. (These drive the City-page rollout.)
- **Demand (Utah AMSV ≈ 258K/mo across 3,770 keywords):** Plumbing (40%) and
  Cooling (32%) are the biggest categories; **"Repair" ≈ 31% of all demand** —
  prioritize repair pages/content. ~82% of demand is **bottom-funnel /
  transactional**; ~32% is **"near me"** — lean into local + emergency framing.
- **Positioning (for About / homepage copy):** fast, same-day emergency response;
  **upfront flat-rate pricing you approve before work**; tech-driven (job photos,
  arrival texts, technician bios); background-checked, certified crew; one company
  for HVAC + plumbing; genuinely local. Leading with **HVAC** (Plumbing next,
  Electrical later).

---

## 7. Keeping this in sync as pages are added

- **Repo + live site:** automatic. Push new page files → Vercel auto-redeploys →
  the live preview updates. No manual step.
- **This handoff doc:** manual, but rarely needs edits — the site is **templated**
  and the page list is **driven by the SEO Workbook**. Adding a planned service
  page (a Plumbing child, etc.) is just another **Child-template** instance and
  needs **no change here**. Only a genuinely **new template type** (Blog, Blog
  Post, Blog Category, Author, City, City-Service, Meet-the-Team, Membership,
  Offers, Financing) warrants a short addition to §4.
- **QA screenshots** in `handoff/` are point-in-time; regenerate if you want fresh
  visuals after a redesign.

---

## 8. Dev checklist

- [ ] Global Colors + Fonts set from §1 (tokens pre-mapped to Elementor roles).
- [ ] **Degular license** confirmed for web, or substituted + uploaded as Custom Font.
- [ ] Templates built: Homepage · Hub · Child · Service Area (+ Coming-Soon). Not one-off pages.
- [ ] Header mega-menu + footer built as Theme parts; **nested production URLs** per §2.
- [ ] Phone `385.853.8116` everywhere; `tel:+13858538116`.
- [ ] Unbuilt sitemap pages route to `coming-soon.html`.
- [ ] Hero interaction + marquee + counters ported from `sunny-engine.js`; generic reveals native.
- [ ] Contact form wired to a real endpoint (roadmap).
- [ ] Build the remaining sitemap pages **from the SEO Workbook**, prioritizing Plumbing + Repair per §6.
- [ ] Build matches `handoff/*-full.jpg` and the live preview.
