#!/bin/bash
# sbc-detail-autopilot.sh — race-free SBC per-church detail enrichment.
#
# Per tick: scrape next 50 SBC.net per-church pages → merge JSONL into
# churches.json → commit + push. Same pattern as image-autopilot-v2.
#
# At 11s polite delay × ~14,649 SBC records missing website = ~45 hours of
# scrape time. PER_TICK=50 × 12s × ~600 ticks = 600 ticks × 15-min interval
# = ~150 hours of wall clock with politeness margin. Run for days.
#
# Run detached:
#     nohup bash scripts/sbc-detail-autopilot.sh > /tmp/sbc-detail-autopilot.log 2>&1 &

set -u
cd /Users/moop_bot_pro/bible-reading-plan-bot || { echo "repo not found"; exit 1; }

DURATION_HRS="${DURATION_HRS:-6}"
TICK_INTERVAL="${TICK_INTERVAL:-900}"     # 15 min
PER_TICK="${PER_TICK:-50}"                 # 50 × 11s = ~9.5 min scrape per tick
STATE="${STATE:-all}"                      # 'all' or a 2-letter code like 'VA'
LOCKFILE="/tmp/sbc-detail-autopilot.lock"
JSONL_PATH="/tmp/sbc-detail.jsonl"

if [ -e "$LOCKFILE" ]; then
  OTHER_PID=$(cat "$LOCKFILE" 2>/dev/null || echo "")
  if [ -n "$OTHER_PID" ] && kill -0 "$OTHER_PID" 2>/dev/null; then
    echo "Another sbc-detail-autopilot is already running (PID $OTHER_PID). Exiting."
    exit 1
  fi
fi
echo $$ > "$LOCKFILE"
trap 'rm -f "$LOCKFILE"; echo "[$(date -u +%H:%M:%SZ)] sbc-detail-autopilot stopped."' EXIT

ts() { date -u +%H:%M:%SZ; }

remaining_to_fetch() {
  node -e "
    const fs=require('fs');
    const d=JSON.parse(fs.readFileSync('docs/data/churches.json','utf8'));
    const done=new Set();
    if (fs.existsSync('$JSONL_PATH')) {
      for (const l of fs.readFileSync('$JSONL_PATH','utf8').split('\n').filter(Boolean)) {
        try { done.add(JSON.parse(l).id); } catch(e){}
      }
    }
    const stateFilter='$STATE';
    let n=0;
    for(const c of d.churches){
      if(!c.source_url||!c.source_url.includes('churches.sbc.net')) continue;
      if(done.has(c.id||c.slug)) continue;
      const hasWeb=c.website&&/^https?:/i.test(c.website);
      const hasGeo=typeof c.latitude==='number';
      if(hasWeb && hasGeo) continue;
      if(stateFilter!=='all' && !new RegExp(',\\\\s*'+stateFilter+'\\\\b').test(c.address||'')) continue;
      n++;
    }
    console.log(n);
  " 2>/dev/null || echo "0"
}

END_TS=$(( $(date +%s) + DURATION_HRS * 3600 ))
echo "[$(ts)] === sbc-detail-autopilot starting · duration=${DURATION_HRS}h · tick=${TICK_INTERVAL}s · per_tick=${PER_TICK} · state=${STATE} ==="

TICK=0
EMPTY_TICKS=0
while [ "$(date +%s)" -lt "$END_TS" ]; do
  TICK=$((TICK+1))
  REM=$(remaining_to_fetch)
  echo "[$(ts)] tick $TICK · $REM SBC churches missing website-or-geo remaining"
  if [ "$REM" -le 0 ]; then
    echo "[$(ts)] queue exhausted — stopping early."
    break
  fi

  echo "[$(ts)] scraping up to $PER_TICK SBC detail pages (JSONL mode, state=${STATE}) ..."
  BEFORE=$([ -f "$JSONL_PATH" ] && wc -l < "$JSONL_PATH" | tr -d ' ' || echo 0)
  STATE_ARG=""
  if [ "$STATE" != "all" ]; then STATE_ARG="--state $STATE"; fi
  node scripts/scrape-sbc-detail.js --count "$PER_TICK" --jsonl "$JSONL_PATH" $STATE_ARG 2>&1 | tail -3
  AFTER=$([ -f "$JSONL_PATH" ] && wc -l < "$JSONL_PATH" | tr -d ' ' || echo 0)
  NEW_THIS_TICK=$((AFTER - BEFORE))

  if [ "$NEW_THIS_TICK" -eq 0 ]; then
    EMPTY_TICKS=$((EMPTY_TICKS+1))
    echo "[$(ts)] 0 new scrape results (empty streak: $EMPTY_TICKS)"
    if [ "$EMPTY_TICKS" -ge 2 ]; then
      echo "[$(ts)] 2 consecutive empty ticks — stopping."
      break
    fi
  else
    EMPTY_TICKS=0
    echo "[$(ts)] +$NEW_THIS_TICK new results in JSONL"

    git pull --rebase --autostash origin main > /dev/null 2>&1 || echo "[$(ts)] pull-rebase had issues"
    echo "[$(ts)] merging $NEW_THIS_TICK results into churches.json ..."
    node scripts/merge-sbc-detail.js 2>&1 | tail -8

    git add docs/data/churches.json
    if git diff --staged --quiet; then
      echo "[$(ts)] no churches.json changes after merge"
    else
      git commit -m "SBC detail tick $TICK: +$NEW_THIS_TICK SBC.net per-church scrapes (websites + geo + phones) [$(ts)]" > /dev/null 2>&1
      if ! git push origin main > /dev/null 2>&1; then
        echo "[$(ts)] push rejected — pull-rebasing and retrying"
        git pull --rebase --autostash origin main > /dev/null 2>&1
        git push origin main > /dev/null 2>&1
      fi
      echo "[$(ts)] committed + pushed tick $TICK"
    fi
  fi

  NEXT_TS=$(( $(date +%s) + TICK_INTERVAL ))
  if [ "$NEXT_TS" -ge "$END_TS" ]; then
    REMAIN_SEC=$(( END_TS - $(date +%s) ))
    if [ "$REMAIN_SEC" -gt 30 ]; then
      echo "[$(ts)] partial final sleep of ${REMAIN_SEC}s ..."
      sleep "$REMAIN_SEC"
    fi
    break
  fi
  echo "[$(ts)] sleeping ${TICK_INTERVAL}s until next tick ..."
  sleep "$TICK_INTERVAL"
done

echo "[$(ts)] === sbc-detail-autopilot finished after $TICK tick(s) ==="
