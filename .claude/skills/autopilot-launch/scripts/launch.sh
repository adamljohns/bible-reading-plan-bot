#!/bin/bash
# launch.sh — start the four enrichment autopilots in parallel.
#
# Args (positional, optional):
#   $1 STATE              — 2-letter code or 'all'              (default: VA)
#   $2 DURATION_HRS       — how long each autopilot runs        (default: 1)
#   $3 QUICKLINKS_PER_TICK — quicklinks PER_TICK                (default: 60)
#
# Examples:
#   bash launch.sh                # VA, 1h, PER_TICK=60
#   bash launch.sh NC 2           # NC, 2h, PER_TICK=60
#   bash launch.sh all 8 30       # nationwide, 8h overnight, smaller per-tick

set -u
cd "$(dirname "$0")/../../../.." || { echo "repo root not found"; exit 1; }

STATE="${1:-VA}"
DUR="${2:-1}"
QL_PER_TICK="${3:-60}"

echo "=== launching autopilots: STATE=$STATE  DURATION_HRS=$DUR  quicklinks PER_TICK=$QL_PER_TICK ==="

# Sanity: refuse to launch if any of the 4 are already running, to avoid
# duplicating work or fighting lockfiles. Operator must kill first.
if pgrep -fl autopilot | grep -vE 'launch.sh|status.sh' > /dev/null 2>&1; then
  echo ""
  echo "ERROR: at least one autopilot is already running:"
  pgrep -fl autopilot | grep -vE 'launch.sh|status.sh'
  echo ""
  echo "Stop the existing autopilots first (pkill -f <name>-autopilot.sh) and"
  echo "remove stale lockfiles (rm -f /tmp/*-autopilot*.lock) before relaunching."
  exit 1
fi

nohup env STATE="$STATE" DURATION_HRS="$DUR" PER_TICK="$QL_PER_TICK" TICK_INTERVAL=600 \
  bash scripts/quicklinks-autopilot.sh > /tmp/quicklinks-autopilot.log 2>&1 < /dev/null &
disown

nohup env STATE="$STATE" DURATION_HRS="$DUR" \
  bash scripts/image-autopilot-v2.sh > /tmp/image-autopilot-v2.log 2>&1 < /dev/null &
disown

nohup env STATE="$STATE" DURATION_HRS="$DUR" \
  bash scripts/pastor-autopilot.sh > /tmp/pastor-autopilot.log 2>&1 < /dev/null &
disown

nohup env STATE="$STATE" DURATION_HRS="$DUR" \
  bash scripts/sbc-detail-autopilot.sh > /tmp/sbc-detail-autopilot.log 2>&1 < /dev/null &
disown

sleep 4

echo ""
echo "=== running ==="
pgrep -fl autopilot | grep -vE 'launch.sh|status.sh'

echo ""
echo "=== first lines of each log ==="
for log in /tmp/quicklinks-autopilot.log /tmp/image-autopilot-v2.log /tmp/pastor-autopilot.log /tmp/sbc-detail-autopilot.log; do
  echo "--- $log ---"
  head -3 "$log" 2>/dev/null
done

echo ""
echo "Window closes in $DUR hour(s). Use directory-pulse to check progress; do not poll."
