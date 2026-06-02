#!/bin/bash
# batch_pipeline.sh — run the per-batch dictionary pipeline for one batch JSON.
# Usage: bin/batch_pipeline.sh data/dictionary-batches/batch-NN-topic.json
# Does: drift-audit (abort on hard hits) -> generate -> rebuild -> regen slugs -> manifest.
# Does NOT commit (caller commits explicitly with a proper message).
set -e
cd "$(dirname "$0")/.."
BATCH="$1"
[ -z "$BATCH" ] && { echo "usage: batch_pipeline.sh <batch.json>"; exit 2; }

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
echo "== DONE =="
