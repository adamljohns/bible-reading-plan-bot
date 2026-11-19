#!/bin/bash
# full-review-round.sh — ONE local-model full-review round of the church directory.
#
#   select (--full-review) -> fetch + local-model read of each church's own site
#   -> review patch + HOLD queue -> [live only] apply auto + QA-approved changes,
#   regenerate, consistency check, path-scoped push.
#
# DRY RUN IS THE DEFAULT. A dry run writes the patch, the HOLD queue and the
# public dashboard counts row (docs/data/full-review-stats.json) and keeps the
# patch + HOLD queue under data/full-review/ (not published), and proves churches.json is
# byte-identical before and after (sha256). It never commits or pushes.
#
#   FULL_REVIEW_BATCH=25          batch size (default 25, max 60)
#   FULL_REVIEW_INCLUDE=id1,id2   force these ids to the front of the batch
#   FULL_REVIEW_MODE=dry|live     live = apply + ship (Adam's GO only)
#   FULL_REVIEW_MODEL=gemma-4-31b-it   LM Studio model (the grind's extractor)
#   GRIND_SCOPE_STATE / GRIND_SCOPE_REGION   same scope filters as the grind
#   FULL_REVIEW_OUT_DIR=<dir>     dry runs only: write patch + HOLD queue + stats
#                                 OUTSIDE the git tree, so a scheduled dry run never
#                                 dirties the autopilot worktree the grind rebases in
#   FULL_REVIEW_STANDING_GO=<file>  live mode needs this file (default
#                                 ~/.openclaw/shared-memory/context/full-review-standing-go.json)
#                                 with "live_allowed": true and an unexpired "expires"
#
# Shares the grind's lock (/tmp/pastor-refine-local.lock): one local-model
# consumer at a time, and never two writers of churches.json.
set -u -o pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
ROOT="$(cd "$(dirname "$0")/.." && pwd -P)"
MODE="${FULL_REVIEW_MODE:-dry}"
BATCH="${FULL_REVIEW_BATCH:-25}"
case "$BATCH" in ''|*[!0-9]*) BATCH=25 ;; esac
[ "$BATCH" -gt 60 ] && BATCH=60
[ "$BATCH" -lt 1 ] && BATCH=1
LOCK="${FULL_REVIEW_LOCK:-/tmp/pastor-refine-local.lock}"
LOG="$HOME/Library/Logs/full-review-round.log"
ROUND="fr-$(date '+%Y%m%d-%H%M')"
WORK="/tmp/full-review/$ROUND"
say() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }
die() { say "ABORT: $*"; exit 1; }

mkdir "$LOCK" 2>/dev/null || { say "lock held ($LOCK) — a grind or review round is running; nothing started"; exit 0; }
trap 'rmdir "$LOCK" 2>/dev/null' EXIT
cd "$ROOT" || die "cd $ROOT"
if [ "$MODE" = "live" ]; then
  GO_FILE="${FULL_REVIEW_STANDING_GO:-$HOME/.openclaw/shared-memory/context/full-review-standing-go.json}"
  node "$ROOT/scripts/lib/full-review-go.js" "$GO_FILE" >>"$LOG" 2>&1 \
    || die "live mode refused: no valid standing GO at $GO_FILE (Adam's GO only)"
  [ -n "${FULL_REVIEW_OUT_DIR:-}" ] && die "FULL_REVIEW_OUT_DIR is for dry runs only"
  [ "$ROOT" = "$(cd "$HOME/bible-reading-plan-bot" 2>/dev/null && pwd -P)" ] && die "live mode refuses ~/bible-reading-plan-bot (fleet scratch)"
  git fetch -q origin main || die "git fetch failed"
  [ -z "$(git status --porcelain)" ] || die "live mode needs a clean tree"
  [ "$(git rev-parse HEAD)" = "$(git rev-parse FETCH_HEAD)" ] || die "live mode needs HEAD level with origin/main"
fi
mkdir -p "$WORK"
CJ="docs/data/churches.json"
SHA_BEFORE=$(shasum -a 256 "$CJ" | cut -d' ' -f1)
say "── full review $ROUND start (mode=$MODE batch=$BATCH) churches.json sha256=$SHA_BEFORE"

SCOPE_ARGS=""
[ -n "${GRIND_SCOPE_STATE:-}" ]  && SCOPE_ARGS="$SCOPE_ARGS --state $GRIND_SCOPE_STATE"
[ -n "${GRIND_SCOPE_REGION:-}" ] && SCOPE_ARGS="$SCOPE_ARGS --region $GRIND_SCOPE_REGION"
INC=""; [ -n "${FULL_REVIEW_INCLUDE:-}" ] && INC="--include $FULL_REVIEW_INCLUDE"
node scripts/select-enrichment-batch.js --full-review $SCOPE_ARGS $INC --count "$BATCH" --out "$WORK" | tee -a "$LOG" \
  || die "selector failed"
python3 scripts/full-review-fetch.py "$WORK/full-review-batch.json" "$WORK/observations.json" --model "${FULL_REVIEW_MODEL:-gemma-4-31b-it}" 2>&1 | tee -a "$LOG"
[ -s "$WORK/observations.json" ] || die "fetch produced no observations (LM Studio :1234 up?)"
DRYFLAG=""; [ "$MODE" = "live" ] || DRYFLAG="--dry-run"
OUTDIR="data/full-review"; STATS_ARGS=""; HOLDS_ARGS=""
if [ -n "${FULL_REVIEW_OUT_DIR:-}" ]; then
  OUTDIR="$FULL_REVIEW_OUT_DIR"; mkdir -p "$OUTDIR"
  # Seed the out-of-tree queue from the tracked one so pending holds still dedupe.
  [ -f "$OUTDIR/hold-queue.json" ] || cp data/full-review/hold-queue.json "$OUTDIR/hold-queue.json"
  STATS_ARGS="--stats $OUTDIR/full-review-stats.json"; HOLDS_ARGS="--holds $OUTDIR/hold-queue.json --stats $OUTDIR/full-review-stats.json"
fi
node scripts/full-review-build-patch.js --input "$WORK/observations.json" --round "$ROUND" --out "$OUTDIR" $STATS_ARGS $DRYFLAG 2>&1 | tee -a "$LOG"
SHA_AFTER=$(shasum -a 256 "$CJ" | cut -d' ' -f1)
say "churches.json sha256 before=$SHA_BEFORE after=$SHA_AFTER $([ "$SHA_BEFORE" = "$SHA_AFTER" ] && echo UNCHANGED || echo CHANGED)"
[ "$SHA_BEFORE" = "$SHA_AFTER" ] || die "churches.json changed during a review build — that must never happen"

PATCH="$OUTDIR/rounds/$ROUND/review-patch.json"
if [ "$MODE" = "live" ]; then
  node scripts/apply-full-review-patch.js --patch "$PATCH" --apply --ship 2>&1 | tee -a "$LOG" || die "apply/ship failed"
else
  node scripts/apply-full-review-patch.js --patch "$PATCH" --accept-dry-run-patch $HOLDS_ARGS 2>&1 | tail -3 | tee -a "$LOG"
  say "DRY RUN complete — nothing applied, committed or pushed. Patch: $PATCH"
fi
say "── full review $ROUND done ──"
