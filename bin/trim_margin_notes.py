#!/usr/bin/env python3
"""Trim trailing translator margin-note stubs from filled batch scriptures.

The verse cache aggregates chapter files that carry KJV marginal notes appended
after the verse text ('...became a living soul. of the'). They are not part of
the verse. Dropping one leaves a strict PREFIX of the cached text, which still
substring-matches in verify_kjv_quotes.py, so fidelity is preserved.

Only ever trims; never rewrites words. Run AFTER bin/fill_scriptures.py.
Usage: python3 bin/trim_margin_notes.py <batch.json> [...]
"""
import json, re, sys

# a trailing fragment, after sentence-final punctuation, that starts lowercase
# and never begins a real KJV sentence -- i.e. a marginal note stub.
# A margin stub follows sentence-final punctuation, starts lowercase, is short,
# and -- crucially -- does NOT end with sentence-final punctuation of its own.
# That last test is what distinguishes 'soul. of the' (a note) from
# 'righteousness: for they shall be filled.' (the verse continuing).
TAIL = re.compile(r'(?<=[.!?])\s+(?![A-Z])([a-z][A-Za-z0-9\'\u2019 ,:;\-]{0,79})$')

# The other KJV margin-note shape: a catchword from the verse, a colon, and an
# explicit note marker ("that is," / "Heb." / "Gr." / "or," / "to wit,").
# Unambiguous -- no verse continues with one of these formulas after a catchword.
NOTE = re.compile(
    r'(?<=[;.,:])\s+[A-Za-z][^.;:]{0,45}:\s+'
    r'(?:that is|Heb\.|Gr\.|Chal\.|or,|to wit)\b.*$')

def trim(text):
    prev = None
    out = text
    while prev != out:
        prev = out
        out = NOTE.sub('', out).rstrip()
        out = TAIL.sub('', out).rstrip()
    return out

def main():
    total = 0
    for path in sys.argv[1:]:
        entries = json.load(open(path))
        n = 0
        for e in entries:
            for pair in e.get('scriptures', []):
                if not isinstance(pair, list) or len(pair) < 2 or not pair[1]:
                    continue
                t = trim(pair[1])
                if t != pair[1]:
                    print(f'  trimmed {e.get("slug","?"):16} {pair[0]:12} '
                          f'-> ...{pair[1][len(t):][:60]!r}')
                    pair[1] = t
                    n += 1
        if n:
            json.dump(entries, open(path, 'w'), ensure_ascii=False, indent=2)
        print(f'{path.split("/")[-1]}: trimmed {n}')
        total += n
    return 0

if __name__ == '__main__':
    sys.exit(main())
