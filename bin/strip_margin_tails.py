#!/usr/bin/env python3
"""Trim 1611 margin-note remnants from the end of scripture quote blocks.

The verse cache's KJV field carries the translators' margin notes after the
verse ("...he shall rule over thee. to thy: or, subject to thy husband").
Earlier re-quote passes clipped those notes only partly, leaving tails such as
"living soul. of the" or "fell: Heb. went forth" on live pages. This tool
finds the verse's true end in the cache (the first ' lemma: Heb.|or,|Gr.'
marker), and trims a quote tail ONLY when (a) the quote text before the tail
ends with the verse's real last 15 characters and (b) the tail is a prefix
of the cached note. Nothing else is touched.

Usage: python3 bin/strip_margin_tails.py [--apply]
"""
import glob, html, importlib.util, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('a', os.path.join(ROOT, 'bin/audit_page_quotes.py'))
A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
V = A.V
NOTE = re.compile(r"(?<=[.;:,?!])\s+[A-Za-z'\- ]{1,40}?:\s+(?:Heb\.|or,|Gr\.|Chald\.|Called\b)")

def plain(s):
    s = re.sub(r'<sup>.*?</sup>', '', s, flags=re.S)
    s = re.sub(r'<[^>]+>', '', html.unescape(s))
    s = re.sub(r'\d+', '', s)
    return re.sub(r'\s+', ' ', s).strip()

def main():
    apply_ = '--apply' in sys.argv
    cache = json.load(open(os.path.join(ROOT, 'docs/assets/verse-cache.json')))
    fixed, pages = 0, 0
    for page in sorted(glob.glob(os.path.join(ROOT, 'docs/dictionary/*.html'))):
        h = open(page, encoding='utf-8').read()
        out = h
        for rx in (A.QUOTE_RE, A.BULLET_RE, A.BULLET_CURLY_RE):
            for m in rx.finditer(h):
                ref, body = m.group(2).strip(), m.group(3)
                p = V.parse_ref(ref)
                raw = V.cache_text(cache, *p) if p else None
                if not raw:
                    continue
                raw = plain(raw)
                n = NOTE.search(raw)
                if not n:
                    continue
                verse, note = raw[:n.start()].rstrip(), raw[n.start():].strip()
                b = body.rstrip()
                closing = ''
                mq = re.search(r'(&rdquo;|"|”)$', b)
                if mq:
                    closing = mq.group(1); b = b[:-len(closing)]
                q = html.unescape(b)
                best = None
                for k in range(1, min(len(q), len(note) + 2)):
                    tail = q[-k:]
                    head = q[:-k].rstrip()
                    if tail.strip() and note.startswith(tail.strip()) and head.endswith(verse[-15:]):
                        best = head
                if best is None:
                    continue
                newbody = html.escape(best, quote=False) if '&' not in b else None
                if newbody is None:
                    # body carries entities; cut the same number of plain chars from the escaped string's tail
                    cut = html.unescape(b)[len(best):]
                    if not b.endswith(cut):
                        continue
                    newbody = b[:-len(cut)].rstrip()
                old = m.group(0)
                new = m.group(1) + newbody + closing + body[len(body.rstrip()):] + m.group(4)
                if old in out:
                    out = out.replace(old, new, 1); fixed += 1
                    print(f'{os.path.basename(page)} | {ref} | ...{q[-50:]!r} -> ...{best[-30:]!r}')
        if out != h:
            pages += 1
            if apply_:
                open(page, 'w', encoding='utf-8').write(out)
    print(f'trimmed {fixed} quote tails on {pages} pages' + ('' if apply_ else ' (report only)'))

if __name__ == '__main__':
    main()
