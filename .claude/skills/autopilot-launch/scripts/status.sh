#!/bin/bash
# status.sh — show the current state of the four enrichment autopilots.
# No side effects; safe to call any time.

set -u
cd "$(dirname "$0")/../../../.." || { echo "repo root not found"; exit 1; }

echo "=== autopilot processes ==="
PROCS=$(pgrep -fl autopilot | grep -v status.sh || true)
if [ -z "$PROCS" ]; then
  echo "  (none running)"
else
  echo "$PROCS"
fi

echo ""
echo "=== last 3 commits per autopilot type (last 12hr) ==="
for kind in "Pastor" "Image" "SBC detail" "Quicklinks"; do
  echo "-- $kind --"
  git log --oneline --since='12 hours ago' --grep="$kind enrichment\|$kind tick\|$kind detail" 2>/dev/null | head -3 || true
done

echo ""
echo "=== /tmp JSONL queue depth ==="
for path in /tmp/pastor-scrapes.jsonl /tmp/image-scrapes.jsonl /tmp/sbc-detail.jsonl /tmp/quicklinks-scrapes.jsonl; do
  if [ -f "$path" ]; then
    LINES=$(wc -l < "$path" | tr -d ' ')
    echo "  $path : $LINES records"
  fi
done

echo ""
echo "=== lockfiles ==="
for lf in /tmp/pastor-autopilot.lock /tmp/image-autopilot-v2.lock /tmp/sbc-detail-autopilot.lock /tmp/quicklinks-autopilot.lock; do
  if [ -f "$lf" ]; then
    PID=$(cat "$lf")
    if kill -0 "$PID" 2>/dev/null; then
      echo "  $lf : PID $PID (alive)"
    else
      echo "  $lf : PID $PID (DEAD — stale lockfile)"
    fi
  fi
done
