#!/usr/bin/env bash
# Quick stats on the MOOP Church Directory.
# Auto-locates the data file relative to this script, so it works from anywhere.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
DATA="$REPO_ROOT/docs/data/churches.json"

if [[ ! -f "$DATA" ]]; then
  echo "ERROR: $DATA not found." >&2
  exit 1
fi

echo "=== MOOP Church Directory stats ==="
jq -r '"Total: \(.total_churches // (.churches | length))\nVersion: \(.directory_version // "n/a")\nUpdated: \(.directory_updated // "n/a")\nChangelog entries: \(.directory_changelog | length)"' "$DATA"

echo
echo "=== Top 15 denomination_family by count ==="
jq -r '[.churches[] | .denomination_family] | group_by(.) | map({fam: .[0], count: length}) | sort_by(-.count) | .[0:15] | .[] | "\(.count)\t\(.fam)"' "$DATA"

echo
echo "=== Quality counters ==="
jq -r '
  [.churches[]] as $all
  | "Verify-pastor records: \([$all[] | select(.pastor // "" | test("verify"; "i"))] | length)"
  + "\nEmpty/null pastor: \([$all[] | select((.pastor // "") == "" or .pastor == null)] | length)"
  + "\nWith Facebook: \([$all[] | select(.facebook)] | length)"
  + "\nWith YouTube: \([$all[] | select(.youtube)] | length)"
  + "\nWith Sermon Archive URL: \([$all[] | select(.sermon_archive_url)] | length)"
  + "\nNeeds-review tagged: \([$all[] | select(.tags // [] | index("needs-review") or index("needs-rating-review"))] | length)"
  + "\nDenom-family corrected (2026-04-30 batch): \([$all[] | select(.tags // [] | index("denomination-corrected-2026-04-30"))] | length)"
  + "\nCultural-drift flagged: \([$all[] | select(.tags // [] | index("cultural-drift-flag"))] | length)"
' "$DATA"

echo
echo "=== Signatures aggregate distribution ==="
jq -r '[.churches[] | .signatures_aggregate // "missing"] | group_by(.) | map({k: .[0], v: length}) | .[] | "\(.v)\t\(.k)"' "$DATA"

echo
echo "=== Unique denomination_family count (canonical target ~30) ==="
jq -r '[.churches[] | .denomination_family] | unique | length' "$DATA"

TOTAL=$(jq '.churches | length' "$DATA")
TARGET=7777
GAP=$((TARGET - TOTAL))
echo
echo "Progress: $TOTAL / $TARGET (gap: $GAP)"
