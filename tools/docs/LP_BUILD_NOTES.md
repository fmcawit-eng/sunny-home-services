# Build notes, ad landing pages

Written for whoever picks these up next.

## Do not hand-edit these four files

`tools/expertslp.py` writes all four from scratch and overwrites whatever is there.
Edit the script, not the HTML.

    python3 tools/expertslp.py

It opens the site's home page and lifts the header, the footer, the script tags after
the footer, the reasons strip, the van band, the membership section, the service areas
and the contact band out of it, then drops each page's own hero, lead band, service
tiles, problem cards and specials in between. Change the home page and the landing
pages follow on the next run. That is the whole point: the earlier versions were
copies, and they fell behind.

Three maps near the top of that file are what you edit:

* `PAGES` holds each page's title, description, headline, body copy and its own
  call-tracked phone number.
* `TILES` holds the four services each season shows, with the photograph and the page
  each tile links to.
* `OFFERS` holds the specials, copied from the client's own offers page. The heating
  pages lead with $500 off a furnace installation; the cooling pages lead with the air
  conditioning offer.
* `BANDS` holds the photograph behind each band.

## Traps

**The hero headline is one `<span class="word">` per word.** That is how the home page
does it, because `.hero-line` is `white-space: nowrap` and the typewriter effect needs
the words separate. Keep each line short or it runs off the side. Three short lines
beat two long ones.

**The hero H1 is white only because of `.hero-title-interactive`.** Drop that class
and the heading renders dark grey over the van photo and cannot be read.

**Never edit CSS with a line based regex.** Check brace balance after any scripted
edit. `sunny-home.css` is long and one unbalanced block takes the rest of the file
down silently.

**`.cta-row .btn` beats `.btn-call-lp`.** Two classes beat one, so a rule inside a
media query on the row wins over the button's own rule. That is why the phone number
button needs `.cta-row .btn.btn-call-lp` to stop the number wrapping across two lines.

**The hero strip is absolutely positioned on a phone.** `.section-hero-split` is a
flex container, so setting the strip to `position: static` turns it into a narrow
column beside the copy instead of a band under it. It sits at `bottom: 0` with
`.has-lp-strip .hero-content` padded out of its way.

**Reveals need time to fire.** Elements with `class="reveal"` start at opacity 0 and
animate in on scroll. Any automated check has to scroll slowly, roughly 170ms per
340px, or it reports content as stuck invisible when it simply has not fired yet.

**Below-the-fold images are lazy loaded.** A broken-image check that does not scroll
the page first will report every one of them as broken.

**Inline links inside a sentence are exempt from the 44px rule.** Padding a link out
to 44px inside running text breaks the line it sits in. The rule is for controls.

## Rebuilding this package

    python3 tools/pagelog.py      # writes tools/pagelog.csv, the source for everything
    python3 tools/urlmap.py       # writes tools/urlmap.csv
    python3 tools/lppdf.py        # assembles the package and renders both PDFs

`lppdf.py` calls `lppackage.py`, which collects the files these pages load by reading
the pages, then the stylesheets they load, then the script. Nothing is matched by file
name, because the script builds some paths at runtime. Check a fresh unzip in a browser
before sending it.

## What was checked before packaging

* **Proofread** on extracted visible text rather than raw markup: typos, doubled words,
  double spaces, straight apostrophes, British spellings, em and en dashes.
* **Mobile**, all four at 360, 390 and 430 with touch emulation.
* **Links and images**, every relative path resolves to a file that is in the package.
* **Copy**, every line compared word by word against the live landing page, so the log
  can say exactly which lines are the client's and which are ours.
