#!/usr/bin/env python3
"""
Stops a single word being left alone on the last line.

Ties the final two words of every heading, paragraph, list item, button and
label together with a non-breaking space, so they always wrap as a pair. This
holds at any screen width, which patching the widths we happen to test does not.

No wording changes: the only thing inserted is the space character itself.

Run:  python3 tools/widont.py [--dry]
"""
import re, os, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = '--dry' in sys.argv

# Mirrors of the client's live pages. They match the live site byte for byte.
SKIP_FILES = {'ac-repair-experts.html', 'ac-replacement-experts.html',
              'furnace-repair-experts.html', 'furnace-replacement-experts.html'}

TAGS = r'h1|h2|h3|h4|p|li|summary|figcaption|blockquote'
CLASSES = r'btn|check-text|hub-tile-title|hub-card-title|hub-lead-in|hub-tile-go|hub-card-link|hub-step-desc|hub-card-desc'

OPEN = re.compile(
    rf'<(?:(?P<t>{TAGS})\b[^>]*>)|<(?P<t2>span|a|div)\b[^>]*class="[^"]*\b(?:{CLASSES})\b[^"]*"[^>]*>')


def close_of(html, start, tag):
    o, c = f'<{tag}', f'</{tag}>'
    i, depth = start, 0
    while i < len(html):
        if html.startswith(o, i) and (i + len(o) >= len(html) or html[i + len(o)] in ' >/'):
            depth += 1; i += len(o)
        elif html.startswith(c, i):
            depth -= 1; i += len(c)
            if depth == 0:
                return i - len(c)
        else:
            i += 1
    return -1


WORD = r"[0-9A-Za-zÀ-ɏ&#;’'’\-\.\,\!\?\:\)\("


def bind_last_two(inner, allow_nb=True):
    """Replace the final word space with a non-breaking one."""
    if not inner.strip():
        return inner, False
    # positions that sit outside any tag
    outside, depth = [], 0
    i = 0
    while i < len(inner):
        if inner[i] == '<':
            depth += 1
        elif inner[i] == '>':
            depth -= 1
        elif depth == 0:
            outside.append(i)
        i += 1
    if not outside:
        return inner, False
    text_pos = set(outside)
    # walk back from the end looking for a plain space between two words
    last_word_end = None
    j = len(inner) - 1
    while j >= 0:
        if j in text_pos and not inner[j].isspace():
            last_word_end = j
            break
        j -= 1
    if last_word_end is None:
        return inner, False
    # the space that starts the final word
    k = last_word_end
    seen_word = False
    while k >= 0:
        if k in text_pos:
            ch = inner[k]
            if ch.isspace():
                if seen_word:
                    break
            else:
                seen_word = True
        k -= 1
    if k < 0 or not inner[k].isspace():
        return inner, False
    # already bound, or the space is not a plain one
    if inner[k] != ' ':
        return inner, False
    before = inner[:k]
    if before.rstrip().endswith('&nbsp;'):
        return inner, False
    # there has to be something before it to bind to
    if not re.search(r'\S', re.sub(r'<[^>]*>', '', before)):
        return inner, False
    tail = inner[k + 1:]
    # A hyphen is a legal place to break, so a final word like "tune-ups."
    # can still split and leave its own tail alone on the last line. Tying
    # the pair does not stop that; only nowrap does.
    if allow_nb and '-' in re.sub(r'<[^>]*>', '', tail) and 'class="nb"' not in tail:
        m_tail = re.fullmatch(r'([^<]*?)(\s*)$', tail, re.S)
        if m_tail and m_tail.group(1).strip():
            tail = f'<span class="nb">{m_tail.group(1)}</span>{m_tail.group(2)}'
    return before + '&nbsp;' + tail, True


def process(html):
    """Collect one edit per element, then drop any that sits inside another.

    A list item and the span inside it both qualify, and editing both corrupts
    the outer one: the inner edit shifts every offset after it, so the outer
    replacement then cuts into a closing tag. Only the innermost element is
    edited, which is the one whose last line actually renders.
    """
    found = []
    for m in OPEN.finditer(html):
        tag = m.group('t') or m.group('t2')
        end = close_of(html, m.start(), tag)
        if end < 0:
            continue
        inner = html[m.end():end]
        if re.search(r'<(p|div|ul|ol|li|h[1-4]|section|table)\b', inner):
            continue                       # holds blocks of its own
        found.append((m.end(), end, inner, tag))

    # keep only the innermost of any nested pair
    innermost = []
    for a, b, inner, tag in found:
        if any(a2 >= a and b2 <= b and (a2, b2) != (a, b) for a2, b2, _, _ in found):
            continue
        innermost.append((a, b, inner, tag))

    edits, n = [], 0
    for a, b, inner, tag in innermost:
        # A FAQ summary is a flex row, so a span added inside it becomes a
        # second flex item and gets pushed to the far side of the row.
        new_inner, changed = bind_last_two(inner)
        if changed:
            if tag == 'summary' and 'faq-q' not in inner:
                # A FAQ summary is a flex row whose text is an anonymous item,
                # so a nowrap span added inside it would become a second item
                # and get pushed to the far side. Giving the text its own span
                # makes it one item again, and the nowrap then behaves.
                new_inner = f'<span class="faq-q">{new_inner}</span>'
            edits.append((a, b, new_inner)); n += 1

    edits.sort(key=lambda e: e[0])
    for i in range(1, len(edits)):
        if edits[i][0] < edits[i - 1][1]:
            raise SystemExit('overlapping edits, refusing to write')

    for a, b, new_inner in reversed(edits):
        html = html[:a] + new_inner + html[b:]
    return html, n


def main():
    total, pages = 0, 0
    for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        if os.path.basename(f) in SKIP_FILES:
            continue
        s = open(f, encoding='utf-8').read()
        new, n = process(s)
        if n:
            if not DRY:
                open(f, 'w', encoding='utf-8').write(new)
            total += n; pages += 1
    print(f'{"would bind" if DRY else "bound"} {total} last word pairs on {pages} pages')


if __name__ == '__main__':
    main()
