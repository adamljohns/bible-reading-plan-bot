#!/bin/bash
# trigger-directory-grind.sh — fleet-triggerable manual church-directory round
# (Chaps / Hermes, on Adam's request; see
# ~/.openclaw/shared-memory/context/church-directory-grind.md).
#
# Canonical source of ~/.openclaw/bin/trigger-directory-grind.sh (installed 2026-11-19). The
# old call shape is unchanged; full review is a new first word.
#
#   trigger-directory-grind.sh [batch]                 enrichment round (as before)
#   trigger-directory-grind.sh full-review [batch]     full-review DRY RUN (patch + HOLD queue, no apply)
#   trigger-directory-grind.sh full-review [batch] --live   full review + apply + ship (Adam's GO only)
#
# Every round runs in the BACKGROUND so the calling agent's turn doesn't block,
# then this returns immediately. The grind and the full review share one lock
# file, so this is always safe to call: an overlapping request starts nothing.
set -u
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
WT="$HOME/bible-reading-plan-bot-autopilot"
LOCK="/tmp/pastor-refine-local.lock"

if [ "${1:-}" = "full-review" ]; then
  BATCH="${2:-25}"
  case "$BATCH" in ''|*[!0-9]*) BATCH=25 ;; esac
  [ "$BATCH" -gt 60 ] && BATCH=60
  MODE="dry"; case " $* " in *" --live "*) MODE="live" ;; esac
  if [ "$MODE" = "live" ]; then
    GO_FILE="${FULL_REVIEW_STANDING_GO:-$HOME/.openclaw/shared-memory/context/full-review-standing-go.json}"
    node "$WT/scripts/lib/full-review-go.js" "$GO_FILE" || { echo "REFUSED: --live needs a valid standing GO from Adam at $GO_FILE. Nothing started."; exit 3; }
  fi
  RUNNER="$WT/scripts/full-review-round.sh"
  [ -f "$RUNNER" ] || { echo "ERROR: full-review runner missing at $RUNNER — tell Max."; exit 1; }
  [ -d "$LOCK" ] && { echo "A directory round is ALREADY running (lock held). Nothing started."; exit 0; }
  # Dry runs write outside git so the grind's worktree stays clean for its rebase.
  DRY_OUT="${FULL_REVIEW_OUT_DIR:-$HOME/Library/Logs/full-review-dry}"
  if [ "$MODE" = "live" ]; then
    nohup env -u FULL_REVIEW_OUT_DIR FULL_REVIEW_BATCH="$BATCH" FULL_REVIEW_MODE=live /bin/bash "$RUNNER" >/dev/null 2>&1 &
  else
    nohup env FULL_REVIEW_BATCH="$BATCH" FULL_REVIEW_MODE=dry FULL_REVIEW_OUT_DIR="$DRY_OUT" /bin/bash "$RUNNER" >/dev/null 2>&1 &
  fi
  if [ "$MODE" = "live" ]; then
    echo "STARTED: full-review round (batch $BATCH, LIVE) in the background. Auto-grade changes apply and ship; RED/BLACK, off-GREEN and lower-confidence proposals wait in data/full-review/hold-queue.json for Chaps QA. No results are known yet."
  else
    echo "STARTED: full-review DRY RUN (batch $BATCH) in the background on the local model. It writes a review patch + HOLD queue under data/full-review/ and changes nothing on the site. Log: ~/Library/Logs/full-review-round.log. No results are known yet."
  fi
  exit 0
fi

BATCH="${1:-25}"
case "$BATCH" in ''|*[!0-9]*) BATCH=25 ;; esac
[ "$BATCH" -gt 60 ] && BATCH=60   # keep a single manual round modest

RUNNER="$WT/scripts/pastor-refine-local.sh"
[ -f "$RUNNER" ] || { echo "ERROR: autopilot runner missing at $RUNNER — tell Adam."; exit 1; }

if [ -d "$LOCK" ]; then
  echo "A local enrichment round is ALREADY running (lock held). Nothing started; check the dashboard: https://usmcmin.org/grind-report.html"
  exit 0
fi

nohup env PASTOR_REFINE_BATCH="$BATCH" /bin/bash "$RUNNER" >/dev/null 2>&1 &
echo "STARTED: local enrichment round (batch $BATCH) running in the background on the local model. It fetches church sites, extracts + verbatim-verifies pastors, and pushes to origin/main in ~5-6 min. Results appear on https://usmcmin.org/grind-report.html — this did not block, and no results are known yet."
