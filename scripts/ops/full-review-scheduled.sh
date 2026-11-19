#!/bin/bash
# full-review-scheduled.sh — the bounded DAILY full-review trigger (launchd
# com.moop.full-review-daily). One DRY-RUN round per day, 10-20 churches.
#
#  * Dry run only. This wrapper never passes live mode; a live round still needs
#    the manual trigger plus a valid standing GO (scripts/lib/full-review-go.js).
#  * Output goes OUTSIDE git (FULL_REVIEW_OUT_DIR), so the autopilot worktree the
#    ordinary grind rebases in stays clean.
#  * Shares the grind's lock: if a grind round holds it, this skips (exit 0) and
#    records "skipped-lock"; the next day's slot tries again.
#  * Writes a health record (last run, verdict, rows) for the dashboard/watchdog.
set -u
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
WT="${FULL_REVIEW_WT:-$HOME/bible-reading-plan-bot-autopilot}"
LOCK="${FULL_REVIEW_LOCK:-/tmp/pastor-refine-local.lock}"
OUT="${FULL_REVIEW_OUT_DIR:-$HOME/Library/Logs/full-review-dry}"
HEALTH="${FULL_REVIEW_HEALTH:-$HOME/Library/Logs/full-review-health.json}"
BATCH="${FULL_REVIEW_DAILY_BATCH:-15}"
case "$BATCH" in ''|*[!0-9]*) BATCH=15 ;; esac
[ "$BATCH" -lt 10 ] && BATCH=10
[ "$BATCH" -gt 20 ] && BATCH=20
TODAY=$(date +%F)
mkdir -p "$OUT"
health() { # verdict detail
  printf '{"job":"full-review-daily","date":"%s","at":"%s","verdict":"%s","batch":%s,"mode":"dry","out_dir":"%s","detail":"%s"}\n' \
    "$TODAY" "$(date -u +%FT%TZ)" "$1" "$BATCH" "$OUT" "$2" > "$HEALTH"
}
# One round per calendar day.
if grep -q "\"date\":\"$TODAY\".*\"verdict\":\"ok\"" "$HEALTH" 2>/dev/null; then
  echo "full-review-daily: already ran today"; exit 0
fi
if [ -d "$LOCK" ]; then health skipped-lock "grind lock held"; echo "full-review-daily: lock held, skipped"; exit 0; fi
RUNNER="$WT/scripts/full-review-round.sh"
[ -f "$RUNNER" ] || { health error "runner missing at $RUNNER"; exit 1; }
if [ "${FULL_REVIEW_PLAN_ONLY:-0}" = "1" ]; then
  echo "plan: runner=$RUNNER batch=$BATCH mode=dry out=$OUT"; exit 0
fi
env -u FULL_REVIEW_STANDING_GO FULL_REVIEW_MODE=dry FULL_REVIEW_BATCH="$BATCH" FULL_REVIEW_OUT_DIR="$OUT" \
  /bin/bash "$RUNNER"; RC=$?
if [ $RC -eq 0 ]; then
  ROUND=$(ls -1t "$OUT/rounds" 2>/dev/null | head -1)
  health ok "round ${ROUND:-none} rc=0"
else
  health error "runner rc=$RC (see ~/Library/Logs/full-review-round.log)"
fi
exit $RC
