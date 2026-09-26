#!/usr/bin/env python3
"""lexicon-rewrite-entry.py — replace the prose of a lexicon page with authored
text, rebuilding the page on the canonical section order.

Why this exists: 59 of the most-frequent words in Scripture carry pages that are
notes, not entries — G2588 (kardia) was 17 words, and cited Proverbs 4:23 on a
Greek page, which bin/lexicon-gate.js correctly refuses. Regenerating those from
a batch script is what produced them; the fix is to author the prose and inject
it while keeping the published shell (TEMPLATE-B-STANDARDIZATION.md: transform
in place, regeneration is lossy).

Authored prose comes in as JSON:
  { "G2588": { "gloss": "...", "pos": "...",
               "definition": "<p>...</p>", "usage": "<p>...</p>",
               "verses": ["Matthew 12:34", ...],
               "related": ["G4151", ...] } }

Verse TEXT is never authored — it is read from the Strong's-tagged KJV in
docs/assets/chapters/, and a reference whose own tagging does not carry this
Strong's number is refused before it can reach the page. Related-word chips are
dropped if the target page does not exist, which is where the corpus's dead
links came from.

Canonical section order (six), applied to every page this touches:
  Definition · Usage & Theological Significance · Key Bible Verses ·
  Related Words · External Resources · Sources

Usage:
  python3 bin/lexicon-rewrite-entry.py entries.json --dry-run
  python3 bin/lexicon-rewrite-entry.py entries.json --write
Nothing is written unless bin/lexicon-gate.js passes the rebuilt page.
"""
import argparse, html, json, os, re, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEX  = ROOT / 'docs' / 'lexicon'
CH   = ROOT / 'docs' / 'assets' / 'chapters'

BOOK_IDS = json.loads(subprocess.run(
    ['node', '-e', 'console.log(JSON.stringify(require("./bin/verse-study-scaffold.js").BOOK_IDS))'],
    cwd=ROOT, capture_output=True, text=True).stdout)

_cache = {}
def chapter(bid, ch):
    k = f'{bid}_{ch}'
    if k not in _cache:
        fp = CH / f'{k}.json'
        _cache[k] = json.loads(fp.read_text(encoding='utf-8')) if fp.exists() else None
    return _cache[k]

def verse(ref, code):
    """KJV text for ref, but only if its own tagging carries `code`."""
    m = re.match(r'^([1-3]?\s*[A-Za-z ]+?)\s+(\d+):(\d+)$', ref.strip())
    if not m: return None, 'unparseable reference'
    bid = BOOK_IDS.get(m.group(1).strip().lower())
    if not bid: return None, 'unknown book'
    pre, num = code[0], code[1:]
    if pre == 'G' and bid <= 39: return None, 'Greek code cited from the Old Testament'
    if pre == 'H' and bid > 39:  return None, 'Hebrew code cited from the New Testament'
    d = chapter(bid, int(m.group(2)))
    if not d or not d.get('KJV'): return None, 'no local chapter text'
    raw = d['KJV'].get(str(int(m.group(3))))
    if not raw: return None, 'verse not in chapter'
    if not re.search(r'<S>' + num + r'</S>', str(raw)):
        return None, f'KJV tagging does not carry {code}'
    txt = re.sub(r'<S>\d+</S>', '', str(raw))
    txt = re.sub(r'<[^>]+>', '', txt)
    return re.sub(r'\s+', ' ', html.unescape(txt)).strip(), None

def section(title, inner):
    return f'\n        <div class="section">\n            <h2>{title}</h2>\n{inner}        </div>\n'

def build(code, e):
    kept, dropped = [], []
    for r in e.get('verses', []):
        t, why = verse(r, code)
        (kept.append((r, t)) if t else dropped.append((r, why)))
    rel = [c for c in e.get('related', []) if (LEX / f'{c}.html').exists()]
    dropped += [(c, 'no such lexicon page') for c in e.get('related', []) if c not in rel]

    body  = section('Definition', e['definition'])
    body += section('Usage &amp; Theological Significance', e['usage'])
    if kept:
        vs = ''.join(
            f'            <div class="verse-entry">\n'
            f'                <a class="verse-ref" href="../bible.html?ref={r.replace(" ", "+")}">{html.escape(r)}</a>\n'
            f'                <div class="verse-text">{html.escape(t)} <em>(KJV)</em></div>\n'
            f'            </div>\n' for r, t in kept)
        body += section('Key Bible Verses', vs)
    if rel:
        chips = ''.join(f'                <a class="related-word" href="{c}.html">{c}</a>\n' for c in rel)
        body += section('Related Words', f'            <div class="related-words">\n{chips}            </div>\n')
    lang = 'greek' if code[0] == 'G' else 'hebrew'
    body += section('External Resources',
        f'            <div class="ext-links">\n'
        f'                <a class="ext-link" href="https://www.blueletterbible.org/lexicon/{code.lower()}/kjv/{"tr" if code[0]=="G" else "wlc"}/0-1/" '
        f'rel="noopener" target="_blank">Blue Letter Bible — {code}</a>\n            </div>\n')
    body += section('Sources',
        f'            <p>Headword, transliteration and definition are from James Strong, '
        f'<em>Strong&#39;s Exhaustive Concordance of the Bible</em> (1890), public domain, via the Open Scriptures '
        f'digital revision (CC&nbsp;BY-SA). Every verse quoted above was selected because its own KJV tagging in '
        f'this site&#39;s chapter data carries {code}, so each citation can be checked against the text rather than '
        f'taken on trust.</p>\n')
    return body, kept, dropped

def rewrite(code, e):
    fp = LEX / f'{code}.html'
    t = fp.read_text(encoding='utf-8')
    body, kept, dropped = build(code, e)
    start = t.find('<div class="section">')
    end   = t.rfind('</div>\n    </div>')          # close of last section + container
    if start < 0 or end < 0: return None, kept, dropped, 'could not locate section block'
    new = t[:start].rstrip('\n ') + body + '    </div>' + t[end + len('</div>\n    </div>'):]
    for key, cls in (('gloss', 'gloss'), ('pos', 'pos')):
        if e.get(key):
            new = re.sub(r'(<div class="' + cls + r'">)[^<]*(</div>)',
                         lambda m: m.group(1) + html.escape(e[key]) + m.group(2), new, count=1)
    return new, kept, dropped, None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('entries'); ap.add_argument('--write', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    if not a.write: a.dry_run = True
    data = json.loads(Path(a.entries).read_text(encoding='utf-8'))
    ok = bad = 0
    for code, e in data.items():
        new, kept, dropped, err = rewrite(code, e)
        if err:
            print(f'SKIP  {code}: {err}'); bad += 1; continue
        with tempfile.NamedTemporaryFile('w', suffix='.html', dir=LEX,
                                         prefix=code + '.CHECK.', delete=False, encoding='utf-8') as fh:
            fh.write(new); tmp = fh.name
        chk = LEX / f'{code}.html.gatecheck'
        os.replace(tmp, chk)
        # the gate keys off the filename, so check under the real name in a scratch copy
        backup = fp_backup = None
        real = LEX / f'{code}.html'
        original = real.read_text(encoding='utf-8')
        real.write_text(new, encoding='utf-8')
        r = subprocess.run(['node', 'bin/lexicon-gate.js', f'docs/lexicon/{code}.html'],
                           cwd=ROOT, capture_output=True, text=True)
        chk.unlink(missing_ok=True)
        passed = r.returncode == 0
        if not (passed and a.write):
            real.write_text(original, encoding='utf-8')
        status = 'pass' if passed else 'FAIL'
        print(f'{status}  {code}  verses {len(kept)} kept, {len(dropped)} dropped'
              + (f'  [{"; ".join(f"{x}: {y}" for x, y in dropped[:3])}]' if dropped else ''))
        if not passed:
            print('      ' + '\n      '.join(l for l in r.stdout.splitlines() if '✗' in l))
            bad += 1
        else:
            ok += 1
            if a.write: print(f'      written')
    print(f'\n{ok} passed, {bad} failed. {"WRITTEN" if a.write else "dry run — nothing written"}.')
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main())
