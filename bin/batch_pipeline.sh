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
if errs:
    print('PRE-FLIGHT FAIL:')
    for x in errs:
        print('  -', x)
    sys.exit(1)
print(f'pre-flight OK: {len(data)} entries, schema/slugs/entities/related all clean')
PY

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
  | grep -vxE 'index|names|doctrinal-anchors|biblical-order|expressly-prohibited|most-corrupted|gen-z-decoded|millennial-decoded|gen-x-decoded|boomer-decoded|changelog|baby-names|by-topic' \
  | sort > data/dictionary-slugs.txt
wc -l < data/dictionary-slugs.txt | xargs echo "slugs:"
echo "== manifest =="
python3 bin/build_dict_manifest.py 2>&1 | grep "File size"
echo "== post-flight: corpus integrity audit =="
python3 bin/dict_integrity_audit.py --quiet | tail -3
echo "== DONE =="
