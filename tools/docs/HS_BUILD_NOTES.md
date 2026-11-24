# Build notes, heating services landing page

Written for whoever picks this up next.

## Do not hand-edit this file

`tools/heatinglp.py` writes `heating-services.html` from scratch and overwrites
whatever is there. Edit the script, not the HTML.

    python3 tools/heatinglp.py

It opens the site's home page and lifts the header, the footer, the script tags after
the footer, the van band and the service areas out of it, then drops this page's own
sections in between. Change the home page and this page follows on the next run. That
is the point: the earlier landing pages were copies, and they fell behind.

The copy lives in named blocks near the top of that file, one per section of the
client's copy doc, so you can see at a glance which section you are editing. The
coupons are in `OFFERS`, the three installation cards in `INSTALL_CARDS`, the reviews
in `REVIEWS`, and the phone number in `PHONE`.

## Traps

**The hero headline is one `<span class="word">` per word.** That is how the home page
does it, because `.hero-line` is `white-space: nowrap` and the typewriter effect needs
the words separate. Keep each line short or it runs off the side.

**The hero H1 is white only because of `.hero-title-interactive`.** Drop that class and
the heading renders dark gray over the van photo and cannot be read.

**The van panel sits above the hero scrim.** `.hero-van-panel` is z-index 2 and
`.hero-scrim` is z-index 1, so by default nothing darkens the van itself. This page
needs it darkened, because the headline is large enough to run across the van, so the
scrim is lifted to z-index 3 and the copy to 4. If you change the hero, check the gold
line still reads where it crosses the bright blue of the wrap.

**`.lp-band-problems .lp-grid` is two classes.** A one-class override like
`.lp-grid-stack` will never beat it. Any grid change in that band needs
`.lp-band-problems` in front of it. This cost time twice.

**`.check-list` carries `max-width: 720px`** for a reading column. A list inside a
full width card needs that lifted or the second column sits in the middle with half the
card empty beside it.

**Media queries add no specificity.** The phone sizing for the coupons has to sit after
the rules it overrides, which is why it is near the end of `sunny-home.css` with a note
saying so. Add a base rule for `.hs-coupon` below it and the phone layout breaks again.

**Never edit CSS with a line based regex.** Check brace balance after any scripted
edit. `sunny-home.css` is long and one unbalanced block takes the rest of the file
down silently.

**Reveals need time to fire.** Elements with `class="reveal"` start at opacity 0 and
animate in on scroll. Any automated check has to scroll slowly, roughly 170ms per
340px, or it reports content as stuck invisible when it simply has not fired yet.

**Below-the-fold images are lazy loaded.** A broken-image check that does not scroll
the page first will report every one of them as broken.

**Inline links inside a sentence are exempt from the 44px rule.** Padding a link out to
44px inside running text breaks the line it sits in. The rule is for controls.

## Rebuilding this package

    python3 tools/heatinglp.py                      # writes the page
    python3 tools/pagelog.py                        # writes tools/pagelog.csv
    python3 tools/urlmap.py                         # writes tools/urlmap.csv
    python3 tools/lppdf.py heating-services         # the folder and both PDFs

`lppdf.py` calls `lppackage.py`, which collects the files the page loads by reading the
page, then the stylesheets it loads, then the script. Nothing is matched by file name,
because the script builds some paths at runtime. Check a fresh unzip in a browser
before sending it.

The same two scripts build the four-page package: pass `landing-pages` instead.

## What was checked before packaging

* **Proofread** on extracted visible text rather than raw markup: typos, doubled words,
  double spaces, straight apostrophes, British spellings, em and en dashes. Clean.
* **Mobile** at 360, 390 and 430 with touch emulation. Clean.
* **Orphans**, no single word left alone on a last line, at 1440 and 390. Clean.
* **Images**, every one resolves, and no image is used twice on the page apart from the
  logo in the header and the footer.
* **Copy**, every line checked against the client's copy doc.
