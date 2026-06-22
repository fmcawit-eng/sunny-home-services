# Sunny Home Services — Homepage Prototype

A static HTML prototype for the **Sunny Home Services** website — a sister brand to **Sunny Garage Doors** (Northern Utah & Southern Idaho). Mirrors the Figma design with brand-color decorations, an interactive video hero, animated reveals, a 7-item mega-menu nav, and a working contact form.

## Pages

| File | Page |
|---|---|
| **`index.html`** | **Homepage (current)** — built from the latest Figma |
| `ac-installation.html` | AC Installation / Replacement landing page |
| `ac-repair.html` | AC Repair landing page |
| `furnace-repair.html` | Furnace Repair landing page |
| `furnace-replacement.html` | Furnace Installation / Replacement landing page |
| `index.html` | Original V2 homepage (superseded by `index.html`) |

All pages share `css/sunny-engine.css` + `sunny-landing.css` + `sunny-home-theme.css` + `sunny-v2.css` and `js/sunny-engine.js`. The nav and footer links are unified across every page.

## Stack

- **HTML + CSS + JS** (vanilla, no build step)
- **Lenis** — smooth scroll
- **GSAP + ScrollTrigger** — section reveals, marquee, counters, hero animations
- **Degular (display) + Rubik (body)** — loaded locally via `@font-face` (`assets/fonts/`)

## Run locally

```bash
# From the prototype/ folder
python3 -m http.server 8889
# Open http://localhost:8889
```

Must be served over HTTP (not opened as `file://`) — the hero video and Lenis require a real origin.

## Page sections

| Order | Section | Notes |
|---|---|---|
| 01 | Nav | Logo + mascot, phone, Book Now |
| 02 | Hero | Full-cover `Hero.mp4` video bg, interactive title (hover / click / mouse-parallax) |
| 03 | Trust marquee | 8 credential pills auto-scrolling |
| 04 | Services | 2-column split (HVAC left, Plumbing right) with vertical hairline divider |
| 05 | Booking | Sand bg, 5-step indicator, interactive service tiles |
| 06 | About Us | Mr. Sunny in a **rotating CSS sun-burst** with sister-brand copy + 3 stat cards |
| 07 | Specials | Bold filled coupons with "Sunny Deal" ribbon |
| 08 | Family Plan | Membership benefits on dark cyan |
| 09 | Testimonials | 3 reviews (placeholder copy) |
| 10 | Service Areas | Real Google Maps image + 15+ Utah cities |
| 11 | Contact Form | Form fields + contact info card |
| 12 | Footer | 4-col link grid |

## Interactive elements

- **Hero title**: each word is its own `<span>`. Hover lifts + tilts + glows yellow with underline. Click triggers a bouncy pop. Mouse-move parallaxes the whole title block opposite the cursor.
- **Service rows** lift on hover with subtle shadow.
- **Booking tiles** swap active state on click (only one selected at a time).
- **About Us mascot**: 14-point CSS clip-path star rotates over 60s; mascot counter-rotates to stay upright.
- **Coupons** lift on hover with shadow.
- **Contact form** shows a `✓ Thanks` confirmation on submit (no backend wired).
- **Lenis** + **GSAP ScrollTrigger** drive section reveals + auto-scrolling trust marquee + scroll-triggered stat counter.

## Asset notes

- `assets/hero.mp4` — 10s, 1920×1080 h.264 (~25 MB). The H.264 codec autoplays muted in all modern browsers. For production, consider transcoding to AV1 + a poster image.
- `assets/map.png` — Google Maps screenshot of the Marriott-Slaterville office area with the Mr. Sunny pin.
- `assets/sunny-logo.png` / `assets/sunny-mascot.png` — brand assets.

## Companion Figma file

Layout was designed in Figma first — that file is the **source of truth for the design**, with its own version history. This repo holds the **code** built from it.

**Figma:** https://www.figma.com/design/3EDkJCu1UQF5m0q2aptfix/

The file contains the homepage (desktop + mobile), the four landing pages (desktop + mobile), and a 🧩 Components page (button/coupon/nav-dropdown/mobile-menu components) for dev handoff.

## Roadmap (not yet wired)

- Wire the contact form to a real endpoint (Formspree / Netlify Forms / custom API).
- Replace placeholder testimonial copy with real Google / Yelp reviews.
- Real photography for the hero video and any additional service photos.
- Mobile breakpoints exist for most sections; needs a full pass on small-screen polish.
- Port to **Elementor / WordPress** for the production site.
