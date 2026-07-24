# Sunny Home Services — Build Spec (WordPress / Elementor)

**Live preview:** https://sunny-home-services.vercel.app
**Design source of truth:** the Figma file (link in [README](README.md)) → this repo is the **code** built from it.
**Visual QA references:** [`handoff/home-full.jpg`](handoff/home-full.jpg) · [`handoff/hub-air-conditioner-full.jpg`](handoff/hub-air-conditioner-full.jpg) · [`handoff/child-ac-repair-full.jpg`](handoff/child-ac-repair-full.jpg)

This repo is the approved static prototype for the Sunny Home Services site
(West Jordan / Wasatch Front, UT — HVAC + Plumbing). It was authored as
**Elementor-ready markup** — the CSS already carries a token system mapped to
Elementor's Global roles. Treat this as a **build spec, not a mockup**: it's a
port into Elementor, not a redesign.

**Ground rules**
1. **Copy is final** — use the text as written in the pages. Don't rewrite.
2. **Phone is `385.853.8116`** everywhere (`tel:+13858538116`).
3. **Three page templates** cover all 15 pages — build the templates once
   (Elementor Theme Builder / Loop templates), not 15 pages by hand.

---

## 1. Global settings (do this first)

The design tokens live in [`css/sunny-engine.css`](css/sunny-engine.css) `:root`
and are already annotated with their Elementor role. Put these in
**Elementor → Site Settings → Global Colors / Fonts**.

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
| `--sun-gradient` | `linear-gradient(90deg, #F17601 0%, #FFC704 100%)` | the signature orange→yellow "sun" gradient (CTAs, ribbons, accents) |

**Container width:** `1280px` (`--container`). Set Elementor's content width to match.

### Fonts

| Role | Font | Notes |
|---|---|---|
| Display | **Degular** | headlines. Loaded locally via `@font-face` (`assets/fonts/`). **Degular is a licensed foundry font (Nice Type)** — confirm the client's license covers web use, or substitute (Elementor: upload the licensed webfont as a Custom Font). Fallback stack in CSS: `'Arial Narrow', sans-serif`. |
| Body | **Rubik** | all body copy. Free Google Font — set as an Elementor Global Font. Local woff2 in `assets/fonts/`. |
| Accent | **Archivo Black** | a couple of display accents; free Google Font (already loaded from Google in the pages). |

### Buttons & the sun gradient

Primary CTA = the **orange→yellow sun gradient** pill (see `.btn` / `.cta`
rules in `css/sunny-v2.css`). Build it as an Elementor global button style:
gradient background `--sun-gradient`, white text, pill radius, subtle lift +
shadow on hover. Secondary = outline / white-on-dark.

### Recurring motifs (reusable)
- **Sun-gradient** accents (buttons, coupon ribbons, underlines).
- **Trust marquee** — auto-scrolling row of credential pills.
- **Rotating sun-burst** behind Mr. Sunny in the About section (CSS clip-path
  star, rotates 60s; mascot counter-rotates to stay upright).
- **Section reveals** — fade/slide up on scroll (GSAP; Elementor entrance
  animations are the native equivalent).

---

## 2. Page inventory — 3 templates cover 15 pages

Build **three Elementor templates** and populate them; don't hand-build 15 pages.

| Template | Pages | Count |
|---|---|---|
| **Homepage** | `index.html` | 1 |
| **Hub / category** | `air-conditioner.html`, `heating.html`, `indoor-air-quality.html`, `heat-pumps.html`, `mini-splits.html` | 5 |
| **Child / service landing** | `ac-repair.html`, `ac-installation.html`, `ac-maintenance.html`, `emergency-ac-repair.html`, `furnace-repair.html`, `furnace-installation.html`, `furnace-maintenance.html`, `emergency-heating-repair.html` | 8 |

`sunny-home-services-markup-2.html` is the **old V2 homepage (superseded)** —
ignore it for the build.

**Not yet built (roadmap):** the Plumbing hub + its children. In the nav, all
Plumbing items currently point to `index.html#services` as placeholders — wire
them to real pages when Plumbing content is ready.

### Shared nav + footer (build once as Elementor Theme parts)

- **Header/nav:** logo + Mr. Sunny mascot, a **mega-menu** with Cooling /
  Heating / Plumbing groups (each listing its child services), phone
  `385.853.8116`, and a **Book Now** CTA. Sticky. Mobile = slide-in menu.
  **Elementor:** Mega Menu widget (Pro) or JetMenu; build as a Header template.
- **Footer:** 4-column link grid + contact. Build as a Footer template.
- **Link map** (all internal links already correct in the markup):
  Cooling hub → `air-conditioner.html`; its children → `ac-repair.html`,
  `ac-installation.html`, `ac-maintenance.html`, `emergency-ac-repair.html`,
  `mini-splits.html`, `heat-pumps.html`. Heating hub → `heating.html`; children →
  `furnace-repair.html`, `furnace-installation.html`, `furnace-maintenance.html`,
  `emergency-heating-repair.html`, `heat-pumps.html`. IAQ hub →
  `indoor-air-quality.html`. Homepage anchors: `#services`, `#about`,
  `#specials`, `#family-plan`, `#locations`, `#contact`.

---

## 3. Homepage template (`index.html`) — 12 sections

Container `1280px`. Order top to bottom:

| # | Section (id/class) | Background | What it is | Elementor |
|---|---|---|---|---|
| 1 | `hero` | full-cover **video** (`assets/hero2.mp4`) | Interactive headline "HVAC & Plumbing Company in West Jordan, UT", sub-copy, Book Now + Call CTAs | Section with video background; headline interactivity = keep `sunny-engine.js` (see §5) |
| 2 | `section-trust-marquee` | dark blue | 8 auto-scrolling credential pills | Marquee (JS) or a plain wrap row |
| 3 | `intro` | white | "HVAC & Plumbing Built for the Wasatch Front" + intro copy | Heading + Text |
| 4 | `services` | white | Service grid (AC, Heating, Plumbing, Drains, Water Heaters, Air Quality) — image cards | Image Box grid / Loop Grid; this is the `#services` anchor |
| 5 | `why` | white | "Experienced HVAC & Plumbing team…" + tools photo | 2-col: text + image |
| 6 | `about` | image bg | Van + sister-brand copy (Sunny Garage Doors) + **3 stat cards** with scroll-counters | Section; counters = JS (§5) or Counter widget |
| 7 | `specials` | **sand** `#FAF4ED` | Bold filled coupons ($49 tune-up, $50 off) with "Sunny Deal" ribbon | Inner Section, coupon = Container w/ custom CSS; `#specials` anchor |
| 8 | `family-plan` | dark cyan | Membership benefits (Sunny Family Plan) | Section; `#family-plan` anchor |
| 9 | `locations` | image bg | Google Maps image + 15+ Utah city links | Image + link list; `#locations` anchor |
| 10 | `faq` | white | Accordion of FAQs | Accordion widget |
| 11 | `cta` | dark/gradient | "Schedule HVAC or Plumbing Services… Today" + CTAs | Section + buttons |
| 12 | `contact` | image bg | Contact form + contact-info card | Form widget; `#contact` anchor |
| — | footer | dark | 4-col links | Footer template |

The **About sun-burst mascot** (§6) is the signature visual — a rotating CSS
star behind Mr. Sunny. Rebuild with the CSS in `css/`, or as a rotating
background image; the mascot must stay upright (counter-rotates).

---

## 4. Hub & Child templates

### Hub / category template (e.g. `air-conditioner.html`) — 7 sections
`hero` (page-specific hero image from `assets/heroes/…`) → `intro` → `services`
(the child services as cards, e.g. AC Repair / Install / Maintenance / Emergency
linking to child pages) → `what-to-expect` → `why` → `cta` → `faq`.
Build once as an Elementor template; swap the hero image, headline, intro, and
the service-card set per hub.

### Child / service landing template (e.g. `ac-repair.html`) — 10 sections
`hero` → `intro` → `certified` (credentials) → `common-problems` →
`repair-vs-replace` (comparison) → `why` → `what-to-expect` (process steps) →
`specials` → `cta` → `faq`.
Build once; per page, swap the hero image (`assets/heroes/<page>.jpg`), the
headline/intro, the common-problems list, and the FAQ. Not every child uses every
block — some omit `repair-vs-replace` or `certified` (see each file).

**Per-page assets are already organized:**
- Hero images: `assets/heroes/<page-name>.jpg` (one per hub/child page).
- Service card images: `assets/services/card-*.jpg` (grouped ac / heating / iaq / ms).
- Section backgrounds: `assets/bg/` (skyline, neighborhood, tools, wasatch, ac-unit).
- Brand: `assets/sunny-logo.png`, `assets/sunny-mascot.png`, `assets/brand-logo.png`, `assets/brand-ray.png`, `assets/van2-current.jpg`.

---

## 5. Animation & interactions

All the JS is in **[`js/sunny-engine.js`](js/sunny-engine.js)** (289 lines,
already modular and commented). It uses **Lenis** (smooth scroll) + **GSAP /
ScrollTrigger**. Mapping to the WordPress build:

| Feature (`sunny-engine.js` fn) | What it does | Elementor approach |
|---|---|---|
| `Lenis` init | smooth scroll | optional; a smooth-scroll plugin, or drop it |
| `initInteractiveHero` + `typeInTitle` | hero headline: types in, words hover-lift/tilt/glow, click-pop, mouse-parallax | **no native equivalent — keep this JS** (enqueue `sunny-engine.js`, or a trimmed hero-only version). This is the signature moment. |
| `initSectionReveals` (`.reveal`) | fade/slide up on scroll | Elementor **entrance animations** (Motion Effects) per widget |
| `initParallax` (`[data-parallax]`) | background parallax | Elementor **scrolling effects** |
| `initMarquee` | auto-scroll trust pills | keep JS, or a marquee widget |
| `initCounters` | stat numbers count up on scroll | Elementor **Counter** widget, or keep JS |
| `initBookingTiles` / `initFamilyPlanTiles` | click-to-select tiles (one active) | small JS, or Elementor Tabs/Toggle |
| contact form `✓ Thanks` | submit confirmation (no backend) | Form widget's native success message + real endpoint |

**Recommendation:** keep `sunny-engine.js` enqueued for the hero interaction,
marquee, and counters (they're cheap and distinctive); use native Elementor
motion for the generic section reveals/parallax. Everything degrades gracefully
without JS.

---

## 6. Assets

Organized under `assets/`:

| Folder / file | Contents |
|---|---|
| `assets/hero2.mp4` | homepage hero video (~muted autoplay H.264). For prod: transcode + add a poster image. |
| `assets/heroes/*.jpg` | one hero image per hub/child page |
| `assets/services/*.jpg` | service + card images (card-ac-*, card-heating-*, card-iaq-*, card-ms-*) |
| `assets/bg/*` | section background photos (skyline, neighborhood, tools, wasatch, ac-unit) |
| `assets/sunny-logo.png`, `sunny-mascot.png`, `brand-logo.png`, `brand-ray.png`, `van2-current.jpg` | brand assets / Mr. Sunny / van |
| `assets/fonts/` | Degular (display) + Rubik (body) webfonts |
| `assets/PHOTO-PROMPTS.md` | notes on the imagery |

---

## 7. Dev checklist

- [ ] Global Colors + Fonts set from §1 (tokens are pre-mapped to Elementor roles).
- [ ] **Degular license** confirmed for web, or substitute + upload as Custom Font.
- [ ] Three templates built (Homepage, Hub, Child) — not 15 hand-built pages.
- [ ] Header + Footer built as Theme parts; nav mega-menu wired to the link map in §2.
- [ ] Phone `385.853.8116` everywhere; `tel:+13858538116`.
- [ ] Hero interaction + marquee + counters ported from `sunny-engine.js`; generic reveals use native Elementor motion.
- [ ] Contact form wired to a real endpoint (roadmap item — currently front-end only).
- [ ] Plumbing hub/children: placeholders (`#services`) rewired when content exists.
- [ ] Build matches `handoff/*-full.jpg` and the live preview.
