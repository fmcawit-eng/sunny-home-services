# Sunny Home Services, developer package

Packaged {DATE}.
Preview: https://sunny-home-services.vercel.app
Client site: https://sunnyhomeservices.com

## Read this first

**Sunny Home Services page log - {STAMP}.pdf**, in the folder above this one, is
the map of the build. The numbers are at the top of page 1, and under them every one
of the 114 pages, numbered, with the menu it sits under, its address on the preview,
the HTML file that holds it, the address it lives at on the client site today, how it
differs from that live page, and anything it still needs. The last page of that PDF
is the revision log: every round of work on this build, newest first.

**Every page with a live counterpart is marked BUILT, UPDATE LIVE.** All 89 of them
differ from what is on the client's site today, so the live page has to be updated.
That is measured, not estimated: `tools/livecompare.py` downloads each live page and
compares it word by word, and the figure in the log is what it found. Most of the
difference is the West Jordan wording, the two new menu items, the new footer, and
hyphenation. Re-run it any time with `python3 tools/livecompare.py --fetch`.

`Sunny Home Services page log - {STAMP}.csv`, beside this file, is the same
information as a spreadsheet if you would rather sort and filter it.

`Sunny Home Services URL map - {STAMP}.pdf` is the short version: two columns, the
HTML file and the address it goes live at, nothing else. That is the one to work from
when you are wiring up addresses. New pages with no live counterpart yet are in orange.

## What is in here

| Where | What it is |
| --- | --- |
| `HTMLs/` | The site. 114 HTML pages, four stylesheets, one script, the assets. This is what deploys. |
| `HTMLs/_source/` | This file, the page log as a spreadsheet, the build notes, the URL map, and the Python that generated the city pages and the landing pages. None of it is needed to run or deploy the site. `_source` can be deleted before going live. |

## Running it

No build step and nothing to install.

    cd HTMLs && python3 -m http.server 8000

Then open http://localhost:8000/home-page.html. Serve it over HTTP rather than opening
the file directly: the hero video and the smooth scrolling both need a real origin.

To deploy, point a static host at `HTMLs/`. `vercel.json` is already set up for Vercel:

* `cleanUrls`, so `/plumber` serves `plumber.html`
* `/` rewrites to `/home-page`, so the root URL serves the home page
* a one year immutable cache on `/assets/`

`trailingSlash` must stay off. Every stylesheet, script and image path in these pages
is relative, so a trailing slash makes the browser look for them one folder deep
(`/millcreek-ut/css/...`) and the page loads with no styling.

There is deliberately no `index.html`. The home page is `home-page.html`, named for
what it is. On a host other than Vercel, point the root at `home-page.html` the way
that host does it: an `index` directive in nginx, a `DirectoryIndex` in Apache.
Otherwise serve the folder as plain static files and keep the file names, because
every link between pages is relative.

## How the pages are put together

The header and the footer are identical on all 114 pages, byte for byte. If you are
rebuilding this in WordPress, that is the first piece to carry over: header and footer
are one shared layout, and each page supplies only its own sections.

Sections are marked with `data-block="..."` on the `<section>` tag, so you can find
each one without reading the markup. The vocabulary is small and repeats across pages:

| `data-block` | What it is |
| --- | --- |
| `hub-hero` | Photo hero with the H1, a one-line sub, and two buttons |
| `hub-prose` | A heading and body copy |
| `hub-cards` | A heading, an intro line, and a grid of linked service cards |
| `hub-checklist` | A heading and a ticked list |
| `hub-steps` | A numbered process list |
| `hub-split` | Copy beside a full-bleed photo, alternating sides |
| `hub-faq` | Native `<details>` accordions |
| `hub-cta` | The closing banner with the two buttons |
| `primary-nav`, `footer-nav` | The shared header and footer |

Service pages use a two-column rhythm: the H2 sits in a sticky rail on the left while
its content scrolls past on the right (`.hub-rail`). Under 1040px that collapses to a
single column. Tinted and untinted bands alternate down the page.

## Fonts, CSS and JS

Four stylesheets load in a fixed order and the last one wins:

    sunny-engine.css      the base: reset, brand colors and fonts, header, footer
    sunny-landing.css     landing page pieces
    sunny-hub.css         the hub and service page system
    sunny-home.css        overrides, loads last

Two others, `sunny-home-theme.css` and `sunny-v2.css`, used to sit in `css/` but no
page loaded either one. They were removed, so what ships is only what runs. Keep the
order the pages have it in. `css/` paths are relative to the stylesheet, not
to the page, which matters if you move the folders.

Degular (display) and Rubik (body) load locally from `assets/fonts/`. Archivo Black
comes from Google Fonts. `js/sunny-engine.js` drives the nav, the
galleries and the smooth scroll, built on GSAP with ScrollTrigger and Lenis, which
load from a public address rather than being shipped here. If the host blocks outside
scripts nothing breaks: every page reads and every link works, the scroll smoothing
goes and the counters sit at their final number.

Sections no longer fade in on scroll. Everything is drawn with the page. The markup
keeps its `.reveal` classes and `data-animation` attributes, so that can be switched
back on by restoring `initSectionReveals()` in the script.

## Mobile

Every page is responsive from 360px up. There is one file per page, not a separate
mobile file: the layout adapts in CSS. All 114 pages were checked at 360, 390 and 430
with touch emulation for sideways scrolling, tap targets under 44px, text under 12px,
content stuck invisible, and whether the two-column blocks actually stack. All 114 pass.

The nav collapses to a menu button under 1024px.

## The four ad landing pages

`ac-repair-experts.html`, `ac-replacement-experts.html`, `furnace-repair-experts.html`
and `furnace-replacement-experts.html` are the pages the ads point at. Until
November 17 they were mirrors of the client's live landing pages, copied byte for byte.
The client's review listed six problems with them. Every one was on the live page
rather than in this build, because a mirror is all a mirror can be.

They are now built from the home page's own sections. The header, the footer, the
reasons strip, the van band, the membership section, the service areas and the contact
band are lifted out of `index.html` every time the pages are generated, so they cannot
drift from the rest of the site again. What the client asked for is in: the current
specials, the current-wrap van, EPA Certified and RMGA Certified with NATE gone, the
membership section as the home page has it, and furnace photographs and titles on the
heating pages instead of air conditioning ones. The wording is still the live page's
own.

Two things follow for dev. They load the site's four stylesheets now, so a global CSS
change does reach them, which it did not before. And they no longer carry the hashed
theme CSS out of `assets/wp-content/themes/`, so the phone problems that came with it
are gone: all four pass at 360, 390 and 430 with everything else.

Each page carries its own call-tracked number in the body while the header carries the
main office number, which is how the live pages do it. Confirm that is still wanted.

Almost every line on these four pages is the live landing page's own wording. A short
list is not, and it is named page by page in the page log so the client can approve it:
the headline on the furnace repair page and on the AC repair page, the first paragraph
under the furnace repair hero, the line under the furnace replacement headline, two
headings on the AC pages, and the three facts in each hero. Those three facts come from
the client's own offers and office hours.

The reviews section is out of all four. The live pages sign four reviews "Customer A"
to "Customer D" and show a five star rating, and neither has a source: Sunny is a new
company with no public reviews yet. The home page had the same block removed for the
same reason. A commented note in each file says where it went and when to put it back.
Nothing was invented in its place.

## The blog

These are two different things.

**`blog.html` is the index.** It is the one page that lists the articles, each as a
card that links through. It holds no article wording of its own. All thirteen articles
are on it.

**Each article is its own page**, `blog-<url slug>.html`. Thirteen of them, built in
full from the client's own briefs.

**`blog-template.html` is the template.** It is not a page and must not be published.
Nothing links to it. It is the file to duplicate to build post fourteen onward: 32
comments beginning `SWAP:` mark everything that changes from one post to the next, and
3 beginning `KEEP:` mark what must not be touched.

To add a post: duplicate the template, rename the copy `blog-<url slug>.html`, work
down the SWAP notes, then add a card for it on `blog.html`. The index grid is one
featured card spanning the full row plus a multiple of three, so add posts three at a
time or the last row sits short.

**No publish dates and no author byline exist anywhere in this set.** The client's
content calendar lists all thirteen as Scheduled to Post with no date, and no brief
names an author. Both have to come from the client before launch.

## A note on the copy

No claim about the client was invented. Every line traces to their live site or to a
brief they supplied. Where their own wording reads oddly it was left as written and
recorded in the page log rather than quietly changed. Three things worth knowing:

* `ac-installation.html` says "Free Estimate" in its title, hero and closing paragraph.
  That is the brief's own wording. Many contractor markets restrict the phrase, so it
  is flagged for the client rather than removed.
* The Kearns brief says "50+ years of combined HVAC and plumbing experience" while
  every Millcreek and service page brief says "over 30 years". Both are left as each
  brief wrote them. The client has to pick one.
* One blog meta description uses the British spelling "recognise". That is the brief's
  own wording.

`privacy-policy.html` and `terms-and-conditions.html` are built and styled but their
policy wording is a placeholder. The client's live site serves that text from a consent
platform rather than from the page, so it could not be pulled and nothing was invented
in its place.

## West Jordan

The client's live site had the city name swapped for the region by a find and replace.
It left page titles reading "Wasatch Front, UT", a "Wasatch Front Building and Safety
Division" that does not exist, one city's elevation applied to a 120 mile region, and
238 instances of "along Wasatch Front" missing its article.

This build puts West Jordan back where the briefs had it. The client has not yet
confirmed that direction, so do not push those strings to the live site until they do.

## The contact form

`contact.html` carries the live site's own Gravity Forms markup, kept so you have the
real field names and IDs. Gravity Forms is WordPress software and cannot run on a
static host, so the form does not send from this package. A short script near the form
stands in for the plugin: it keeps the page free of script errors and labels the form
rather than letting it look like it sends and quietly fail. Delete that script, and
`.form-stub-note` in `sunny-home.css`, once the real plugin is wired up.
