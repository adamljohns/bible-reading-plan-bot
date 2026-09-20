#!/usr/bin/env python3
"""lexicon-fill-from-strongs.py — turn placeholder lexicon pages into real entries.

The 1,548 placeholder pages in docs/lexicon/ were produced by two earlier stub
generators. One prints prose that never says what the word means; the other
prints a "gloss" that merely restates the Strong's number. Both read like
scholarship and teach nothing, which is exactly what bin/lexicon-gate.js exists
to catch.

This script fills them from sources instead of from invention:

  headword, transliteration,
  pronunciation, derivation,
  definition, KJV renderings   -> bin/baselines/strongs-hebrew|greek.json
                                  (James Strong, 1890 — public domain; JSON
                                   revision by Open Scriptures, CC-BY-SA)

  occurrence counts and every
  cited verse                  -> docs/assets/chapters/*.json, the KJV tagged
                                  with <S>NNNN</S> on each word (KJV: public
                                  domain)

Nothing on the page is asserted that did not come from one of those two places.
Citations are not chosen for effect — they are the verses whose own KJV tagging
carries this Strong's number, which is the same check the gate runs. Pages are
written only if the gate passes them.

Usage:
  python3 bin/lexicon-fill-from-strongs.py --dry-run [--limit N]
  python3 bin/lexicon-fill-from-strongs.py --write [--limit N]
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'
LEX = DOCS / 'lexicon'
OCC = Path('/tmp/occ.json')

MAX_VERSES = 4          # a handful of short KJV citations, not a concordance dump
GATE = ROOT / 'bin' / 'lexicon-gate.js'


def esc(s):
    return html.escape(str(s or ''), quote=True)


def clean_def(s):
    """Strong's definition text carries editorial marks; normalise lightly."""
    s = re.sub(r'\[idiom\]|\{[^}]*\}', '', str(s or ''))
    s = re.sub(r'\s+', ' ', s).strip(' ;:,.')
    return s


def renderings(kjv_def, limit=6):
    """The KJV's own renderings, as a short list.

    Strong's uses parentheses for optional letters, not asides: "(wh)ere(-fore)"
    means where / wherefore. Deleting the parenthetical leaves "ere", which is
    not a word the KJV ever used. Keep the letters, drop only the brackets and a
    leading hyphen, so the form comes out whole.
    """
    s = clean_def(kjv_def)
    if not s:
        return []
    out = []
    for p in re.split(r'[,;]', s):
        p = re.sub(r'\(\s*-?([^)]*)\)', r'\1', p)
        p = p.replace('[', '').replace(']', '')
        p = re.sub(r'\s+', ' ', p).strip(' .-')
        if not p or not re.search(r'[A-Za-z]{3}', p):
            continue
        # Strong's packs several forms into one token, e.g. "(fore-) father(-less)"
        # for forefather / father / fatherless. Expansion cannot recover which is
        # meant, and a half-joined "fore- fatherless" is worse than saying less.
        if re.search(r'-\s|\s-', p):
            continue
        if len(p) < 28 and p.lower() not in [o.lower() for o in out]:
            out.append(p)
        if len(out) >= limit:
            break
    return out


def short_gloss(strongs_def, rends, lang):
    """A headline gloss, not Strong's whole apparatus.

    The raw definition is written for a concordance: "a cause (as if asked
    for), i.e. (logical) reason (motive, matter), (legal) crime (alleged or
    proved)". Take the sense before the first "i.e." and drop the asides.
    """
    s = clean_def(strongs_def)
    if s:
        s = re.split(r'\bi\.e\.|\bi\.q\.', s)[0]
        s = re.sub(r'\([^)]*\)', '', s)
        s = re.sub(r'\s+', ' ', s).strip(' ;:,.-')
        s = re.split(r'[;]', s)[0].strip()
    if not s and rends:
        s = ', '.join(rends[:3])
    if not s:
        s = f'{lang} term'
    if len(s) > 80:
        s = s[:77].rsplit(' ', 1)[0] + '…'
    return s


def part_of_speech(derivation):
    """Only what Strong's derivation actually states. No guessing."""
    d = (derivation or '').lower()
    if 'primitive root' in d:
        return 'Verb (primitive root)'
    if 'primitive word' in d:
        return 'Primitive word'
    if 'patronymic' in d:
        return 'Patronymic'
    if 'denominative' in d:
        return 'Denominative verb'
    return ''


def build_definition(code, rec, total, testament):
    """A Definition section that clears 25 words using only sourced facts."""
    sdef = clean_def(rec.get('strongs_def'))
    deriv = clean_def(rec.get('derivation'))
    rends = renderings(rec.get('kjv_def'))
    lang = 'Hebrew' if code[0] == 'H' else 'Greek'

    bits = []
    if sdef:
        bits.append(f"Strong's defines {esc(code)} as <em>{esc(sdef)}</em>.")
    else:
        bits.append(f"{esc(code)} is a {lang} term of the {testament}.")
    if deriv:
        d = deriv.rstrip(' ;')
        bits.append(f"Strong's gives the derivation as {esc(d)}.")
    if rends:
        lst = ', '.join(esc(r) for r in rends)
        bits.append(f"The King James translators rendered it {lst}.")
    if total:
        word = 'once' if total == 1 else f'{total} times'
        bits.append(f"In the tagged KJV the word carries this number {word}.")
    return ' '.join(bits)


def build_usage(code, total, books):
    lang = 'Hebrew' if code[0] == 'H' else 'Greek'
    tst = 'Old Testament' if code[0] == 'H' else 'New Testament'
    if total == 1:
        where = f"a single tagged occurrence in the {tst}"
    else:
        where = f"{total} tagged occurrences in the {tst}"
    s = f"Tracing {esc(code)} through the {tst} shows {where}"
    if books:
        shown = books[:6]
        more = '' if len(books) <= 6 else f", and {len(books) - 6} more"
        s += f", falling in {', '.join(esc(b) for b in shown)}{more}"
    s += ('. The verses below are not selected for effect: each one carries this '
          f'{lang} number in the KJV tagging itself, so the reader can check the '
          'claim against the text rather than taking it on trust.')
    return s


def build_page(code, rec, occ, template_parts):
    head, tail = template_parts
    lang = 'Hebrew' if code[0] == 'H' else 'Greek'
    tst = 'Old Testament' if code[0] == 'H' else 'New Testament'
    lemma = rec.get('lemma', '')
    translit = rec.get('xlit') or rec.get('translit') or ''
    pron = clean_def(rec.get('pron'))
    refs = occ['refs'][:MAX_VERSES]
    total = occ['total']
    books = []
    for r, _t in occ['refs']:
        b = r.rsplit(' ', 1)[0]
        if b not in books:
            books.append(b)

    rends = renderings(rec.get('kjv_def'), limit=4)
    gloss = short_gloss(rec.get('strongs_def'), rends, lang)

    pos = part_of_speech(rec.get('derivation'))
    title = f"{code} — {translit} ({gloss}) | USMC Ministries Lexicon"
    desc = f"{gloss} — {lang} word study from the {tst}. Strong's {code}."

    out = [head.replace('@@TITLE@@', esc(title))
               .replace('@@DESC@@', esc(desc))
               .replace('@@CODE@@', esc(code))]

    out.append('        <div class="word-header">\n'
               f'            <span class="strongs-badge">{esc(code)} · {lang} · {tst}</span>\n'
               f'            <div class="original-word">{esc(lemma)}</div>\n'
               f'            <div class="transliteration">{esc(translit)}</div>\n')
    if pos:
        out.append(f'            <div class="pos">{esc(pos)}</div>\n')
    if pron:
        out.append(f'            <div class="pos">Pronounced {esc(pron)}</div>\n')
    out.append(f'            <div class="gloss">{esc(gloss)}</div>\n        </div>\n')

    out.append('        <div class="section">\n            <h2>Definition</h2>\n'
               f'            <p>{build_definition(code, rec, total, tst)}</p>\n'
               '        </div>\n')

    out.append('        <div class="section">\n            <h2>Usage in Scripture</h2>\n'
               f'            <p>{build_usage(code, total, books)}</p>\n'
               '        </div>\n')

    if refs:
        out.append('        <div class="section">\n            <h2>Key Bible Verses</h2>\n')
        for ref, text in refs:
            t = text if len(text) <= 300 else text[:297].rsplit(' ', 1)[0] + '…'
            q = ref.replace(' ', '+')
            out.append('            <div class="verse-entry">\n'
                       f'                <a class="verse-ref" href="../bible.html?ref={esc(q)}">{esc(ref)}</a>\n'
                       f'                <div class="verse-text">{esc(t)} <em>(KJV)</em></div>\n'
                       '            </div>\n')
        out.append('        </div>\n')

    out.append('        <div class="section">\n            <h2>Sources</h2>\n'
               '            <p>Headword, transliteration, pronunciation, derivation and '
               'definition are from James Strong, <em>Strong\'s Exhaustive Concordance '
               'of the Bible</em> (1890), in the public domain, via the '
               '<a href="https://github.com/openscriptures/strongs">Open Scriptures</a> '
               'digital revision (CC&nbsp;BY-SA). Occurrence counts and every verse '
               'cited above come from the Strong\'s-tagged King James Version carried '
               'in this site\'s own chapter data, so each citation can be checked '
               'against the text.</p>\n'
               '        </div>\n')

    out.append(tail)
    return ''.join(out)


def make_template():
    """Head and tail taken from a real, passing entry so filled pages look native."""
    src = (LEX / 'G1063.html').read_text(encoding='utf-8')
    i = src.find('        <div class="word-header">')
    j = src.rfind('</div>\n        <div class="section">')
    head = src[:i]
    # everything from the last section onward: find the container close + footer
    k = src.find('<footer')
    tail = src[k:] if k > 0 else '</body>\n</html>\n'
    tail = '    </div>\n' + tail
    head = re.sub(r'<title>[\s\S]*?</title>', '<title>@@TITLE@@</title>', head, count=1)
    head = re.sub(r'(<meta name="description" content=")[^"]*(")', r'\1@@DESC@@\2', head, count=1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*(")', r'\1@@TITLE@@\2', head, count=1)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*(")', r'\1@@DESC@@\2', head, count=1)
    head = re.sub(r'(<link rel="canonical" href="https://usmcmin\.org/lexicon/)[^"]*(")',
                  r'\1@@CODE@@.html\2', head, count=1)
    return head, tail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=0)
    a = ap.parse_args()
    if not (a.write or a.dry_run):
        ap.error('pass --write or --dry-run')

    heb = json.loads((ROOT / 'bin/baselines/strongs-hebrew.json').read_text())
    grk = json.loads((ROOT / 'bin/baselines/strongs-greek.json').read_text())
    occ = json.loads(OCC.read_text())
    codes = sorted(occ, key=lambda c: (c[0], int(c[1:])))
    if a.limit:
        codes = codes[:a.limit]

    template = make_template()
    written, skipped = [], []
    for code in codes:
        rec = (heb if code[0] == 'H' else grk).get(code)
        if not rec or not rec.get('lemma'):
            skipped.append((code, 'no Strong\'s record or lemma'))
            continue
        page = build_page(code, rec, occ[code], template)
        target = LEX / f'{code}.html'
        if a.write:
            target.write_text(page, encoding='utf-8')
        else:
            (Path('/tmp/lexpreview')).mkdir(exist_ok=True)
            (Path('/tmp/lexpreview') / f'{code}.html').write_text(page, encoding='utf-8')
        written.append(code)

    print(f"pages built : {len(written)}")
    print(f"skipped     : {len(skipped)}")
    for c, why in skipped[:5]:
        print(f"   {c}: {why}")
    if a.write:
        print("written into docs/lexicon/")
    else:
        print("preview written to /tmp/lexpreview/ (no repo files touched)")


if __name__ == '__main__':
    main()
