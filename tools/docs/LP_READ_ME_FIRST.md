# Sunny Home Services, ad landing pages

Packaged {DATE}.
Preview: https://sunny-home-services.vercel.app
Client site: https://sunnyhomeservices.com

This package holds the four pages the ads point at, and nothing else. The rest of the
site is in the full site package.

## Read this first

**Sunny Home Services landing pages log - {STAMP}.pdf**, in the folder above this one,
is the map. Page 1 has the four pages, where each one lives on the preview and on the
client site today, how far it has moved from the live page, and what it still needs.
Page 2 is the revision log: what changed on these pages and why.

`Sunny Home Services landing pages log - {STAMP}.csv`, beside this file, is the same
information as a spreadsheet.

`Sunny Home Services landing pages URL map - {STAMP}.pdf` is two columns, the HTML
file and the address it goes live at. The four pages are at the top. Under them is
every page their header and footer link to, so you can see where each link lands.

## The four pages

| File | What it is |
| --- | --- |
| `furnace-repair-experts.html` | Furnace repair. The winter lead page. |
| `furnace-replacement-experts.html` | Furnace replacement. |
| `ac-repair-experts.html` | Air conditioner repair. |
| `ac-replacement-experts.html` | Air conditioner replacement. |

## What changed, in one paragraph

These four used to be mirrors of the client's live landing pages, copied byte for
byte. The client's review listed six problems with them. Every one was on the live
page rather than in this build, because a mirror is all a mirror can be. They are now
built from the home page's own sections, so they cannot drift from the rest of the
site again. What the client asked for is in: the current specials, the current-wrap
van, EPA Certified and RMGA Certified with NATE gone, the membership section as the
home page has it, and furnace photographs and titles on the heating pages instead of
air conditioning ones.

## Three things to decide before these go live

**Reviews are out of all four pages.** The live pages sign four reviews "Customer A"
to "Customer D" under a five star rating. Neither has a source: Sunny is a new company
with no public reviews yet. The home page had the same block removed for the same
reason. A comment in each file says where it went and when to put it back. Nothing was
invented in its place.

**Two phone numbers per page.** The header carries the main office number,
385.853.8116, and the body carries that page's own call-tracked number. That is how
the live pages do it. The log names the number on each page. Confirm it is still
wanted.

**A few lines are ours, not the client's.** Almost every line on these pages is the
live landing page's own wording. The short list that is not is named page by page in
the log's Note column: a headline on two of the pages, one paragraph, two headings,
and the three facts in each hero. Those three facts come from the client's own offers
and office hours. They need the client's yes.

## Running it

No build step and nothing to install.

    cd HTMLs && python3 -m http.server 8000

Then open http://localhost:8000/furnace-repair-experts.html. Serve it over HTTP rather
than opening the file directly: the smooth scrolling needs a real origin.

To deploy, point a static host at `HTMLs/`. `vercel.json` is set up for Vercel:

* `cleanUrls`, so `/furnace-repair-experts` serves the file
* `/` opens the furnace repair page, since this package has no home page. That is a
  convenience for the preview link, not a decision about the site.
* a one year immutable cache on `/assets/`

`trailingSlash` must stay off. Every stylesheet, script and image path in these pages
is relative, so a trailing slash makes the browser look for them one folder deep and
the page loads with no styling.

## The links that leave these pages

The header and the footer are the site's own, so they link to the other 60 pages of
the site. Those files are not in this package, so those links will not resolve here.
Every one of them is listed in the URL map with the address it points at on the client
site, which is what you wire up in WordPress. Drop these four files into the full site
package and every link resolves.

## How the pages are put together

The header and the footer are identical to every other page on the site, byte for
byte. If you are building this in WordPress, header and footer are one shared layout
and each page supplies only its own sections.

Sections are marked with `data-block="..."` on the `<section>` tag. Down the page:

| Section | What it is |
| --- | --- |
| Hero | Photo of the van, the headline, three facts, two buttons, and a strip of reasons |
| Lead band | The heading and the two paragraphs that open the page |
| Service tiles | The four services for that season, each linking to its service page |
| Problem bands | Two cards: the signs to call, and what we do about them |
| Reasons | EPA Certified, RMGA Certified, licensed, bonded, insured |
| Van | The current-wrap van beside the copy |
| Specials | The current offers, copied from the client's offers page |
| Membership | The Sunny Family Plan, as the home page has it |
| Service areas | The cities and ZIP codes |
| Contact | The form and the office details |

Four stylesheets load in a fixed order and the last one wins:

    sunny-engine.css      the base: reset, brand colors and fonts, header, footer
    sunny-landing.css     landing page pieces
    sunny-hub.css         the hub and service page system
    sunny-home.css        overrides, loads last

Keep that order. `css/` paths resolve against the stylesheet, not the page, which
matters if you move the folders.

Degular (display) and Rubik (body) load locally from `assets/fonts/`.
`js/sunny-engine.js` drives the nav and the smooth scroll, built on GSAP with
ScrollTrigger and Lenis, which load from a public address rather than being shipped
here. If the host blocks outside scripts nothing breaks: every page reads and every
link works, and the scroll smoothing goes.

## Mobile

One file per page, not a separate mobile file: the layout adapts in CSS. All four were
checked at 360, 390 and 430 with touch emulation for sideways scrolling, tap targets
under 44px, text under 12px, content stuck invisible, and broken images. All four pass.

These pages used to load hashed copies of the live theme CSS, which put the menu
button at 46x42, the Book Now button at 40px tall and the BBB badge at 41px. The
rebuild removes that stylesheet, so those are gone.

## A note on the copy

No claim about the client was invented. One sentence in the client's own copy on
`furnace-repair-experts.html` ends on a comma: "high-quality heating repairs,". It is
their wording, left as written and recorded in the log rather than quietly changed.
