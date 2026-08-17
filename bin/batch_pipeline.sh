#!/bin/bash
# batch_pipeline.sh — run the per-batch dictionary pipeline for one batch JSON.
# Usage: bin/batch_pipeline.sh data/dictionary-batches/batch-NN-topic.json
#
# Stages:
#   pre-flight  : JSON/schema validity, slug collisions, HTML entities,
#                 related-chip resolution (all targets must exist or be
#                 in-batch) — fails fast BEFORE anything is generated.
#   drift audit : voice-lock scan (aborts on hard hits).
#   generate -> rebuild -> regen slugs -> manifest.
#   post-flight : full corpus integrity audit (bin/dict_integrity_audit.py)
#                 so every batch session ends verified-stable.
#
# Does NOT commit (caller commits explicitly with a proper message).
set -e
cd "$(dirname "$0")/.."
BATCH="$1"
[ -z "$BATCH" ] && { echo "usage: batch_pipeline.sh <batch.json>"; exit 2; }

echo "== pre-flight =="
python3 - "$BATCH" <<'PY'
import json, re, sys, os, html.entities
batch = sys.argv[1]
raw = open(batch, encoding='utf-8').read()
data = json.loads(raw)                      # crashes loudly on bad JSON
errs = []
REQ = ['slug','word','pronunciation','pos','etymology','biblical_def',
       'webster_summary','webster_full','scriptures','corruption_summary',
       'corruption_paragraphs','roots_summary','roots_lines','usage','related']
ents = set(re.findall(r'&([a-zA-Z][a-zA-Z0-9]*);', raw))
valid = set(html.entities.name2codepoint) | {'amacr','emacr','imacr','omacr',
                                             'umacr','aelig','thorn'}
bad = sorted(ents - valid)
if bad:
    errs.append(f'invalid HTML entities: {bad}')
slugs = {l.strip() for l in open('data/dictionary-slugs.txt') if l.strip()}
# Also block re-creating a slug that was MERGED AWAY (it is a redirect stub now,
# absent from slugs.txt — without this the nightly run could resurrect a dup).
try:
    slugs |= {l.split('->')[0].strip() for l in open('data/dictionary-redirects.txt') if '->' in l}
except FileNotFoundError:
    pass
pages = {f[:-5] for f in os.listdir('docs/dictionary') if f.endswith('.html')}
own = {e.get('slug') for e in data}
for e in data:
    s = e.get('slug', '(missing)')
    miss = [k for k in REQ if k not in e]
    if miss:
        errs.append(f'{s}: missing fields {miss}')
    if s in slugs:
        errs.append(f'{s}: SLUG COLLISION — already exists; never recreate a slug')
    rl = e.get('roots_lines', [])
    if not all(isinstance(x, str) for x in rl):
        errs.append(f'{s}: roots_lines must be a list of STRINGS (silent render bug)')
    for pair in e.get('related', []):
        if not (isinstance(pair, list) and len(pair) == 2):
            errs.append(f'{s}: malformed related pair {pair}'); continue
        tgt = pair[0]
        if tgt not in pages and tgt not in own:
            errs.append(f'{s}: related target "{tgt}" does not exist '
                        f'(substitute an existing slug before generating)')
    rels = [p[0] for p in e.get('related', []) if isinstance(p, list) and p]
    if len(rels) != len(set(rels)):
        errs.append(f'{s}: duplicate related targets {rels}')
# PERSON-DUP GUARD (2026-07-01): a new slug must not be a VARIANT FORM of an
# existing entry. The 6/30 nightly suffixed john-preston-puritan around the
# existing john-preston (same man) 22 times. If the entity is the SAME, skip it
# — never define twice. If genuinely distinct (brook-kanah vs kanah the town),
# acknowledge with "distinct_from": ["<slug>"] on the entry and the guard passes.
SUFF = ('-puritan','-theologian','-hymnwriter','-reformer','-missionary','-scribe',
        '-rom16','-daughter','-princeton','-scottish','-divine','-pastor','-preacher',
        '-covenanter','-martyr','-bishop','-elder','-deacon','-evangelist')
STOP = {'son','king','duke','gate','town','pool','tower','mount','brook','city',
        'daughter','place','stone','month','book','figure','prophet','priest','queen',
        'well','spring','rock','hill','valley','river','sea','land','house'}
for e in data:
    s = e.get('slug', '')
    cands = set()
    for suf in SUFF:
        if s.endswith(suf):
            cands.add(s[:len(s)-len(suf)])
    parts = s.split('-')
    if len(parts) >= 3:
        cands.add('-'.join(parts[:2]))
        cands.add('-'.join(parts[-2:]))
    if len(parts) >= 2 and parts[-1] not in STOP and len(parts[-1]) > 3:
        cands.add(parts[-1])
    ack = set(e.get('distinct_from', []))
    hits = sorted(c for c in cands if c in slugs and c not in ack and c != s and c not in own)
    if hits:
        errs.append(f'{s}: VARIANT-FORM of existing entr(ies) {hits} — if the SAME '
                    f'person/thing, SKIP (never define twice); if genuinely distinct, '
                    f'add "distinct_from": {hits} to this entry')
# INFLECTION GUARD (2026-08-16): the guard above only knows person-name
# suffixes, so it waved through come/cometh, draw/drew and appear/appearance —
# a new lemma authored beside an inflection of itself that was already live.
# Both directions must be checked: the new slug may be an inflection of a live
# entry, OR a live entry may be an inflection of the new slug. Reuses the same
# morphology table the gap miner uses, so the two stay in step. This is a
# PROMPT, not a prohibition — the dictionary deliberately covers archaic forms
# (dureth, cometh, asketh) — but the author must say so with distinct_from.
import importlib.util as _ilu
_ws = 'bin/kjv_wordlist.py'
if os.path.exists(_ws):
    _sp = _ilu.spec_from_file_location('kw', _ws)
    _kw = _ilu.module_from_spec(_sp); _sp.loader.exec_module(_kw)
    _live_lemmas = {}
    for _l in slugs:
        for _lem in _kw.lemma_slugs(_l):
            _live_lemmas.setdefault(_lem, []).append(_l)
    for e in data:
        s = e.get('slug', '')
        ack = set(e.get('distinct_from', []))
        hits = {c for c in _kw.lemma_slugs(s) if c in slugs}          # new is inflection of live
        hits |= {l for l in _live_lemmas.get(s, [])}                   # live is inflection of new
        hits = sorted(h for h in hits if h != s and h not in ack and h not in own)
        if hits:
            errs.append(f'{s}: INFLECTION of / inflected by existing entr(ies) {hits} — '
                        f'if the SAME word, SKIP and enrich the existing entry; if the '
                        f'archaic form deserves its own study, add "distinct_from": '
                        f'{hits} and cross-link them in "related"')
if errs:
    print('PRE-FLIGHT FAIL:')
    for x in errs:
        print('  -', x)
    sys.exit(1)
print(f'pre-flight OK: {len(data)} entries, schema/slugs/entities/related all clean')
PY

echo "== KJV fidelity gate =="
# Runs BEFORE generation: a batch quoting non-KJV text must never reach the
# corpus. Its absence here is why 207 live entries across batches 415-436
# carry NASB/LSB/ESV renderings against VOICE-LOCK 5.3, and why a batch
# written in an unparseable ref style ("Psalm 22:1") used to sail through
# reporting "0 verified, 0 mismatched" — a pass that examined nothing.
if ! python3 bin/verify_kjv_quotes.py "$BATCH"; then
  echo "ABORT: KJV fidelity gate failed. Quote the Authorized Version verbatim"
  echo "       (pull text with bin/kjv_lookup.py) and write refs in 3-letter"
  echo "       form (Psa 22:1, Joh 1:14, Php 2:6). Nothing was generated."
  exit 1
fi

echo "== drift audit =="
if ! python3 bin/dict_drift_audit.py "$BATCH" 2>&1 | grep -qE "0 HARD hit|CLEAN"; then
  echo "ABORT: hard hits present. Fix before generating."
  python3 bin/dict_drift_audit.py "$BATCH" 2>&1 | grep -E "\[H\]" | head -20
  exit 1
fi

echo "== generate =="
python3 bin/generate_dict_entries.py "$BATCH" 2>&1 | tail -1
echo "== rebuild =="
python3 rebuild-dictionary.py 2>&1 | grep "Total entries"
echo "== regen slugs =="
ls docs/dictionary/*.html | xargs -n1 basename | sed 's/.html$//' \
  | grep -vxE 'index|manifest|names|doctrinal-anchors|biblical-order|expressly-prohibited|most-corrupted|gen-z-decoded|millennial-decoded|gen-x-decoded|boomer-decoded|christianese-decoded|jesus-generation|changelog|baby-names|by-topic' \
  | grep -vxFf <(awk '{print $1}' data/dictionary-redirects.txt 2>/dev/null) \
  | sort > data/dictionary-slugs.txt
wc -l < data/dictionary-slugs.txt | xargs echo "slugs:"
echo "== manifest =="
python3 bin/build_dict_manifest.py 2>&1 | grep "File size"
echo "== sitemaps (excludes redirect stubs; keeps search engines current) =="
python3 bin/generate_sitemap.py 2>&1 | grep -E 'sitemap-dictionary|sitemap index'
echo "== enhance entry pages (anchors, In-the-Text, disambiguation) =="
python3 bin/enhance_entry_pages.py 2>&1 | tail -4
echo "== post-flight: corpus integrity audit =="
python3 bin/dict_integrity_audit.py --quiet | tail -3
echo "== DONE =="
