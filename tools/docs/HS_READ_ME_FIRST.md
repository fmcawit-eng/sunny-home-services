# Sunny Home Services, heating services landing page

Packaged {DATE}.
Live: https://sunny-home-services.vercel.app/heating-services
Client site: https://sunnyhomeservices.com

This package holds one page, `heating-services.html`. The four other ad landing
pages are in their own package, and the rest of the site is in the full site
package.

## Read this first

**Sunny Home Services heating services landing page log - {STAMP}.pdf**, in the folder
above this one, is the map. Page 1 has the page, where it lives on the preview, the
address it is meant to go live at, and everything it still needs. Page 2 is the
revision log: what changed and why.

The same information is beside this file as a spreadsheet, and
**Sunny Home Services heating services landing page URL map - {STAMP}.pdf** is the short
version: two columns, the HTML file and the address it goes live at.

## What this page is

The general heating landing page. It covers furnaces, heat pumps and ductless
mini-splits in one place, where `furnace-repair-experts.html` and
`furnace-replacement-experts.html` each cover a single job.

Every heading, paragraph and bullet is the client's own wording, from their copy doc
"Unbounce Landing Page Copy - Sunny Home Services - Heating Services Landing Page".
Nothing was invented.

## Four things the copy doc left open

| In the doc | What was done |
| --- | --- |
| An AWARDS and CERTIFICATIONS block with nothing in it | Left out. The only certifications we can source are EPA and RMGA, and both are already in the Why Sunny Home Services list. |
| A Branding Video block | Left out. No branding video was supplied, and the two clips in `assets/` are a plumbing crawlspace and an air conditioner, neither branded nor heating. A play button that plays the wrong thing is worse than no block. |
| "*fine print" under both tune-up coupons | Taken word for word from the client's own offers page, where both coupons already live. |
| The phone number in the header | Used as written. This page's call-tracked number, (385) 438-4462, is in the header as well as the body. The other four landing pages keep the main office number up top, so this one differs. Confirm it. |

## Reviews

The three reviews are real and came with the copy doc, signed Samuel M., Annette D.
and Jared H. The doc gives no city and no platform for any of them, so none is shown,
and there is no overall star rating anywhere on the page.

One thing worth knowing: the Google map embed near the foot of this page reports 5.0
from 89 Google reviews. That is the first sourced rating we have seen for this client.
Everywhere else on the site a reviews block was removed for having no source. If the
client confirms that rating, those blocks can come back.

## Running it

No build step and nothing to install.

    cd HTMLs && python3 -m http.server 8000

Then open http://localhost:8000/heating-services.html. Serve it over HTTP rather than
opening the file directly: the smooth scrolling needs a real origin.

To deploy, point a static host at `HTMLs/`. `vercel.json` is set up for Vercel:

* `cleanUrls`, so `/heating-services` serves the file
* `/` opens this page, since the package has no home page. That is a convenience for
  the preview link, not a decision about the site.
* a one year immutable cache on `/assets/`

`trailingSlash` must stay off. Every stylesheet, script and image path on this page is
relative, so a trailing slash makes the browser look for them one folder deep and the
page loads with no styling.

## The links that leave this page

The header and the footer are the site's own, so they link to the rest of the site.
Those files are not in this package, so those links will not resolve here. Every one
of them is in the URL map with the address it points at on the client site, which is
what you wire up in WordPress. Drop this file into the full site package and every
link resolves.

## How the page is put together

The header and the footer are identical to every other page on the site, byte for
byte. If you are building this in WordPress, header and footer are one shared layout
and each page supplies only its own sections.

Down the page:

| Section | What it is |
| --- | --- |
| Hero | The van photo, the headline, the subhead, the opening paragraph and two buttons |
| Current Specials and Offers | The two tune-up coupons |
| Why Sunny Home Services | The copy doc's eight lines, beside a photo |
| Quality Heating Service | The heading and paragraph that open the body |
| Heating Installation | Three cards: gas and electric furnaces, heat pumps, ductless mini-splits |
| Heating Repair | What we fix, and the eight signs to call about, each beside a photo |
| Preventative Maintenance | The tune-up checklist, beside a photo |
| Emergency Heating Repair | The signs of an emergency, beside a photo |
| Van | The current-wrap van band, shared with the home page |
| Closing call | The copy doc's closing section |
| Reviews | The three real reviews |
| Our Services | The seven services the copy doc lists |
| Service areas | The cities and ZIP codes, shared with the home page |
| Request Your Service Now | The form the copy doc specifies, then the map |
| Bottom bar | The full width line the copy doc puts at the very bottom |

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
here. If the host blocks outside scripts nothing breaks: the page reads and every link
works, and the scroll smoothing goes.

## The form

The fields are the ones the copy doc lists: a "Yes, please text me!" checkbox, first
name, last name, phone number, email, and "How can we help you?". The consent
paragraph under the button is the doc's wording, word for word.

It does not send. This is a static page with no form handler. Wire it to whatever the
live site uses and delete the small inline `onsubmit` on the `<form>` tag.

## Mobile

One file, not a separate mobile file: the layout adapts in CSS. Checked at 360, 390
and 430 with touch emulation for sideways scrolling, tap targets under 44px, text
under 12px, content stuck invisible, and broken images. All clean.
