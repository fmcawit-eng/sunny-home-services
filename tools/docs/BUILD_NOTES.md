# Build notes

Written for whoever picks this up next. It covers how the pages were made and the
traps that cost time the first time round.

## Where things come from

| Page group | Count | Source of the copy |
| --- | --- | --- |
| Home, service hubs, service children | 46 | The copywriter brief for each page |
| City hubs and their children | 48 | The brief for each city page |
| Blog index, articles, template | 15 | Each article's own brief doc |
| Ad landing pages | 4 | The live landing page wording, rebuilt in the site design |
| Legal and utility | 3 | Placeholder, or ours |

The city pages and the blog pages were generated rather than hand-written, so they
can be rebuilt from their briefs. Everything else was built by hand.

## Rebuilding a city page

    python3 tools/outline.py tools/row23.txt "Millcreek, UT Heating, Cooling, and Plumbing Services" tools/o23.json
    python3 tools/citypages.py tools/cityjobs.json

`outline.py` turns a brief's plain text export into an ordered outline of headings,
paragraphs and bullet lists. `citypages.py` renders that outline into a page, reusing
an existing page's header, footer and scripts so the new page cannot drift from the
rest of the site.

`cityjobs.json` is the only file you edit to add a city: the title, the URL, the H1,
the hero image, the breadcrumb, and a map of the brief's `[a]` `[b]` `[c]` footnote
markers to real page links.

How a section becomes a block:

* sub-headings that each name a service, with a paragraph under them, become a card grid
* a bullet list of `Name: description` where the names are services becomes a card grid
* anything else with bullets becomes a ticked checklist
* paragraphs alone become a prose band, and two of them per page become full-bleed splits
* the last section before the FAQ becomes the closing banner

That distinction matters. Symptom lists, decision lists and step lists read as bullets
in the brief exactly like service lists do, but they have no destination page and no
photo, so rendering them as cards produces a grid of repeated stock art. The generator
tests whether the item names map to real service pages and whether they are short
enough to be names rather than sentences.

## Rebuilding a landing page

    python3 tools/expertslp.py

That writes all four ad landing pages from scratch. It opens `index.html` and lifts
the header, the footer, the script tags after the footer, the reasons strip, the van
band, the membership section, the service areas and the contact band out of it, then
drops this page's own hero, service tiles, problem list and offers in between. Change
the home page and the landing pages follow on the next run, which is the whole point:
the earlier versions were copies and they fell behind.

Two maps near the top of that file are what you edit. `TILES` holds the four services
each season shows, with the photograph and the page each tile links to. `OFFERS` holds
the specials, copied from the client's own offers page; the heating pages lead with
$500 off a furnace installation and the cooling pages lead with the air conditioning
offer. `BANDS` holds the photograph behind each band, and the phone numbers are in the
`PAGES` list, one call-tracked number per page.

The hero headline is built one `<span class="word">` per word, the way the home page
does it, because `.hero-line` is `white-space: nowrap` and the typewriter effect needs
the words separate. Keep the lines short or they run off the side.

## Rebuilding the page log

    python3 tools/pagelog.py        # writes tools/pagelog.csv
    python3 tools/handoff_pdf.py    # renders tools/page-log.pdf from that CSV
    python3 tools/package.py        # assembles dist/ and the folder to zip

The PDF is rendered from the CSV rather than from its own data, so the two cannot
disagree. The live URL map and the list of open items live at the top of `pagelog.py`;
that is what you edit when a page goes live or a decision comes back.

## Traps

**Do not hand-edit the four `-experts` pages.** `tools/expertslp.py` overwrites all
four every time it runs. Edit the script, not the HTML. Until November 17 these pages
loaded hashed copies of the live theme CSS and no global CSS change could reach them;
that is over, they load the site's own four stylesheets now.

**`css/` paths resolve against the stylesheet, not the page.** Font paths in
`sunny-home.css` need `../assets/fonts/`, not `assets/fonts/`.

**Never edit CSS with a line based regex.** Check brace balance after any scripted
edit. Several of these stylesheets are long and a stray unbalanced block takes the
rest of the file down with it silently.

**Reveals need time to fire.** Elements with `class="reveal"` start at opacity 0 and
animate in on scroll. Any automated check has to scroll slowly, roughly 170ms per
340px, or it reports content as stuck invisible when it simply has not fired yet.

**Below-the-fold images are lazy loaded.** A broken-image check that does not scroll
the page first will report every one of them as broken.

**Grid counts.** Service card grids and the blog index grid must divide evenly by
their column count, or a card sits alone beside empty space. The city generator picks
a column count that leaves either a full last row or exactly one card, and gives that
one card the full row with `.hub-card.is-wide`.

## What was checked before packaging

* **Proofread**, all 114 pages, on extracted visible text rather than raw markup:
  typos, doubled words, double spaces, straight apostrophes, spacing before
  punctuation, British spellings, em and en dashes, placeholder text left behind.
  Clean, apart from three items in the client's own copy, all listed in the page log.
* **Mobile**, all 114 pages at 360, 390 and 430 with touch emulation: sideways
  scrolling, tap targets under 44px, text under 12px, reveals stuck invisible, broken
  images, two-column blocks failing to stack, nav reachable. All 114 clean. The four
  landing pages used to be the exception; the rebuild fixed them.
* **Links**, every relative link and image path resolves to a file that exists.
* **Structure**, tag balance on every page, and CSS brace balance after every edit.

Inline links inside a sentence are deliberately exempt from the 44px rule. Padding a
link out to 44px inside running text breaks the line it sits in, and the rule is for
controls, not for reading links.
