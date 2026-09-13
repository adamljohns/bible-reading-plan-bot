#!/bin/bash
# runbatch.sh <batch.json> — fill refs → trim margin notes → drop dead chips → validate → full pipeline
set -o pipefail
WT=$(git rev-parse --show-toplevel) || exit 1; cd "$WT" || exit 1
B="$1"; mkdir -p /tmp/dictlogs; L=/tmp/dictlogs/log-$(basename "$B" .json).txt
python3 bin/fill_scriptures.py "$B" || { echo "FILL FAILED"; exit 1; }
python3 bin/trim_margin_notes.py "$B" | tail -2
python3 bin/fix_related.py "$B" | tail -2
python3 bin/validate_batches.py "$B" || { echo "VALIDATE FAILED"; exit 1; }
bash bin/batch_pipeline.sh "$B" > "$L" 2>&1; rc=$?
grep -E '^== |verified|mismatch|unresolv|FAIL|HARD|RESULT|slugs:|Total entries|GUARD|refus' "$L" | head -30
echo "pipeline rc=$rc  (log: $L)"; exit $rc
