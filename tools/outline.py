#!/usr/bin/env python3
"""Turn a brief into an ordered outline: [{h2, blocks:[...], subs:[{h3, blocks}]}]."""
import re, sys, json

def load(path):
    t = open(path, encoding='utf-8').read().replace('﻿','')
    notes = {m.group(1): m.group(2).strip()
             for m in re.finditer(r'^\[([a-z])\](.*)$', t, re.M)}
    t = re.sub(r'^\[[a-z]\].*$', '', t, flags=re.M)
    # The copy block is the tail of the doc. It begins at the LAST "Meta Description:"
    # line, or when the doc puts meta at the top, right after the client-notes block.
    md = [m.start() for m in re.finditer(r'^Meta Descriptions?:', t, re.M|re.I)]
    if md:
        body = t[md[-1]:]
        meta = re.match(r'^Meta Descriptions?:\s*(.*)', body, re.I).group(1).strip()
        body = body.split('\n', 1)[1]
    else:
        # row26 shape: meta at top, copy starts after the last "Pages that should link"
        anchor = list(re.finditer(r'Pages that should link to this page[^\n]*\n', t))
        body = t[anchor[-1].end():] if anchor else t
        mm = re.search(r'^Meta Description:\s*(.*)$', t, re.M)
        meta = mm.group(1).strip() if mm else ''
    return body, meta, notes

def is_heading(s):
    if not s or s.startswith('*'): return False
    if len(s) > 115: return False
    if s.endswith(('.', ',', ':', ';')): return False
    if s.endswith('!') and not re.match(r'^[A-Z][\w\s,&/\'’-]+!$', s): return False
    return True

def outline(body, h1):
    lines = [l.rstrip() for l in body.split('\n')]
    # strip everything before the H1 line
    for i, l in enumerate(lines):
        if l.strip().rstrip('?') == h1.rstrip('?') or l.strip() == h1:
            lines = lines[i+1:]; break
    secs = []
    lead = []           # prose that sits above the first H2
    cur = None          # current h2 dict
    sub = None          # current h3 dict
    buf = []
    def blocks_from(buf):
        out, bl = [], []
        for ln in buf:
            s = ln.strip()
            if not s: continue
            if s.startswith('* '):
                bl.append(s[2:].strip())
            else:
                if bl: out.append(['ul', bl]); bl = []
                out.append(['p', s])
        if bl: out.append(['ul', bl])
        return out
    def flush():
        nonlocal buf
        if buf:
            if sub is not None or cur is not None:
                tgt = sub if sub is not None else cur
                tgt['blocks'] += blocks_from(buf)
            else:
                lead.extend(blocks_from(buf))
        buf = []
    for ln in lines:
        s = ln.strip()
        if is_heading(s):
            # Heading level: a line that is Title Case with 3+ capitalized words,
            # or ends in '?' inside the FAQ, is an H2. Sentence-case short lines
            # that sit under an H2 and are followed by prose are H3.
            words = [w for w in re.findall(r'[A-Za-z][\w&/-]*', s)]
            caps = sum(1 for w in words if w[:1].isupper())
            h2ish = (len(words) >= 3 and caps >= max(3, int(len(words)*0.55))) or s.endswith('?')
            flush()
            if h2ish or cur is None:
                cur = {'h2': s, 'blocks': [], 'subs': []}; secs.append(cur); sub = None
            else:
                sub = {'h3': s, 'blocks': []}; cur['subs'].append(sub)
        else:
            buf.append(ln)
    flush()
    return secs, lead

if __name__ == '__main__':
    body, meta, notes = load(sys.argv[1])
    h1 = sys.argv[2]
    secs, lead = outline(body, h1)
    print('META:', meta)
    print('LEAD:', [b[1][:150] for b in lead])
    print('NOTES:', notes)
    for s in secs:
        print(f'\nH2  {s["h2"]}')
        for b in s['blocks']:
            print(f'      {b[0]:3} {(b[1][:2] if b[0]=="ul" else b[1][:85])}' + (f'  (+{len(b[1])-2} more)' if b[0]=='ul' and len(b[1])>2 else ''))
        for u in s['subs']:
            print(f'   H3  {u["h3"]}')
            for b in u['blocks']:
                print(f'         {b[0]:3} {(b[1][:2] if b[0]=="ul" else b[1][:78])}')
    json.dump({'meta':meta,'notes':notes,'lead':lead,'secs':secs}, open(sys.argv[3],'w'), indent=1)
