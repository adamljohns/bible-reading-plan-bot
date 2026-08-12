#!/bin/bash
# continuous-enrichment-lane.sh — execute exactly one bounded frontier lane after
# fresh/retry/social extraction is exhausted. Called inside the autopilot lock and
# clean detached worktree; it is the sole writer for this round.
set -u
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

BATCH="${FRONTIER_BATCH:-10}"
BRAVE_BATCH="${BRAVE_DISCOVERY_BATCH:-5}"
BRAVE_DAILY_LIMIT="${BRAVE_DISCOVERY_DAILY_LIMIT:-40}"
BRAVE_LEDGER="${BRAVE_DISCOVERY_LEDGER:-$HOME/Library/Logs/brave-directory-attempts.tsv}"
WORK="${1:-/tmp/prl}"
LOG="${2:-$HOME/Library/Logs/pastor-refine-local.log}"
say() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }
die() { say "ALERT: $*"; exit 1; }

mkdir -p "$WORK"
LAST_MODE=$(node -e 'try{const s=require("./docs/data/grind-stats.json").series||[];console.log((s.at(-1)||{}).mode||"")}catch(_){console.log("")}' 2>/dev/null)
STATUS=$(node scripts/grind-lane-status.js --last-mode "$LAST_MODE") || die "lane status failed"
LANE=$(printf '%s' "$STATUS" | node -e 'let b="";process.stdin.on("data",d=>b+=d).on("end",()=>console.log(JSON.parse(b).selected))')

# Brave is quota-bounded. Once today's allowance is used, source recovery keeps
# the pipeline moving; no API key is spent beyond the configured ceiling.
if [ "$LANE" = "website-discovery" ]; then
  TODAY=$(date -u +%F)
  USED=$(awk -F '\t' -v t="$TODAY" '$1==t{n++}END{print n+0}' "$BRAVE_LEDGER" 2>/dev/null || echo 0)
  LEFT=$((BRAVE_DAILY_LIMIT - USED))
  if [ "$LEFT" -le 0 ]; then
    SRC=$(printf '%s' "$STATUS" | node -e 'let b="";process.stdin.on("data",d=>b+=d).on("end",()=>console.log(JSON.parse(b).source_recovery||0))')
    if [ "$SRC" -gt 0 ]; then LANE="source-recovery"; else LANE="monitoring"; fi
  elif [ "$BRAVE_BATCH" -gt "$LEFT" ]; then
    BRAVE_BATCH="$LEFT"
  fi
fi

if [ "${CONTINUOUS_PLAN_ONLY:-0}" = "1" ]; then
  printf 'lane=%s frontier_batch=%s brave_batch=%s brave_daily_limit=%s\n' \
    "$LANE" "$BATCH" "$BRAVE_BATCH" "$BRAVE_DAILY_LIMIT"
  exit 0
fi

ATTEMPTED=0; APPLIED=0
case "$LANE" in
  website-discovery)
    OUT="$WORK/website-discovery.txt"
    node scripts/find-church-websites.js --count "$BRAVE_BATCH" --apply --attempt-log "$BRAVE_LEDGER" >"$OUT" 2>&1 || { cat "$OUT" >>"$LOG"; die "website-discovery lane failed"; }
    cat "$OUT" >>"$LOG"
    ATTEMPTED=$(grep -oE 'website search for [0-9]+' "$OUT" | grep -oE '[0-9]+$' | head -1); ATTEMPTED=${ATTEMPTED:-0}
    APPLIED=$(grep -oE '^[0-9]+ sites found' "$OUT" | grep -oE '^[0-9]+' | head -1); APPLIED=${APPLIED:-0}
    ;;
  source-recovery)
    JSONL="$WORK/sbc-detail.jsonl"; OUT="$WORK/source-recovery.txt"; MERGE="$WORK/source-merge.txt"
    rm -f "$JSONL"
    node scripts/scrape-sbc-detail.js --count "$BATCH" --jsonl "$JSONL" >"$OUT" 2>&1 || { cat "$OUT" >>"$LOG"; die "source-recovery scrape failed"; }
    cat "$OUT" >>"$LOG"
    ATTEMPTED=$(grep -oE 'Records to fetch: [0-9]+' "$OUT" | grep -oE '[0-9]+$' | head -1); ATTEMPTED=${ATTEMPTED:-0}
    node scripts/merge-sbc-detail.js --jsonl "$JSONL" >"$MERGE" 2>&1 || { cat "$MERGE" >>"$LOG"; die "source-recovery merge failed"; }
    cat "$MERGE" >>"$LOG"
    W=$(grep -oE '\+[0-9]+ websites' "$MERGE" | grep -oE '[0-9]+' | head -1); W=${W:-0}
    G=$(grep -oE '\+[0-9]+ geocodes' "$MERGE" | grep -oE '[0-9]+' | head -1); G=${G:-0}
    P=$(grep -oE '\+[0-9]+ phones' "$MERGE" | grep -oE '[0-9]+' | head -1); P=${P:-0}
    APPLIED=$((W + G + P))
    ;;
  monitoring)
    say "no executable frontier lane; unresolved dead-site and review queues remain"
    ;;
  *) die "unknown lane selected: $LANE" ;;
esac

node scripts/append-grind-stats.js --mode "$LANE" --attempted "$ATTEMPTED" --found 0 --applied "$APPLIED" >>"$LOG" 2>&1 \
  || die "frontier grind-stats update failed"

if [ "$ATTEMPTED" -gt 0 ]; then
  node generate-church-pages.js >>"$LOG" 2>&1 || { git reset -q --hard; die "frontier regen failed"; }
  python3 scripts/build_state_shards.py >>"$LOG" 2>&1 || die "state shard rebuild failed"
  python3 scripts/build_denomination_shards.py >>"$LOG" 2>&1 || die "denomination shard rebuild failed"
  node scripts/build-directory-map.js >>"$LOG" 2>&1 || die "directory map rebuild failed"
  node scripts/build-sitemap-churches.js >>"$LOG" 2>&1 || die "sitemap rebuild failed"
  node scripts/build-church-index.js >>"$LOG" 2>&1 || die "church index rebuild failed"
  node scripts/check-consistency.js >>"$LOG" 2>&1 || { git reset -q --hard; die "frontier consistency failed"; }
fi

if [ -n "$(git status --porcelain)" ]; then
  git add docs/data/churches.json docs/data/grind-stats.json docs/churches/ docs/data/churches-index.json docs/data/churches-index-slim.json docs/data/churches/ docs/data/directory-map-points.json docs/sitemap-churches.xml 2>/dev/null || die "frontier git add failed"
  git commit -qm "Directory enrichment: $LANE ($APPLIED fields from $ATTEMPTED records)" || die "frontier commit failed"
  if ! git push -q origin HEAD:main; then
    say "frontier push rejected — rebasing and retrying"
    git fetch -q origin main && git rebase -q FETCH_HEAD && git push -q origin HEAD:main || die "frontier push failed after rebase"
  fi
fi
say "frontier lane done: $LANE attempted=$ATTEMPTED applied=$APPLIED"
