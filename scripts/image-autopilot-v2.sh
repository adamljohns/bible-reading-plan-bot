#!/bin/bash
# image-autopilot-v2.sh — RACE-FREE image enrichment driver.
#
# V1 had a race: the scraper mutated churches.json during the scrape, which
# could collide with the autopilot's own git pull --rebase --autostash. Net
# effect was ~50/60 records LOST per tick on average.
#
# V2 architecture:
#   1. Scraper writes results to /tmp/image-scrapes.jsonl ONLY (read-only on churches.json)
#   2. Merge step runs alone: reads JSONL → writes churches.json once
#   3. Commit + push
#   4. Repeat
#
# Because the scraper never writes churches.json, autostash CANNOT clobber
# uncommitted scrape work — there's no uncommitted scrape work to lose.
#
# Run detached (recommended):
#     nohup bash scripts/image-autopilot-v2.sh > /tmp/image-autopilot-v2.log 2>&1 &
#     tail -f /tmp/image-autopilot-v2.log
#     # stop: pkill -f image-autopilot-v2.sh

set -u
cd /Users/moop_bot_pro/bible-reading-plan-bot || { echo "repo not found"; exit 1; }

DURATION_HRS="${DURATION_HRS:-8}"
TICK_INTERVAL="${TICK_INTERVAL:-1200}"        # 20 min default
PER_TICK="${PER_TICK:-200}"                    # 200 churches per tick (~10 min scrape at 3s polite)
STATE="${STATE:-all}"
LOCKFILE="/tmp/image-autopilot-v2.lock"
JSONL_PATH="/tmp/image-scrapes.jsonl"

# --- single-instance lock ---
if [ -e "$LOCKFILE" ]; then
  OTHER_PID=$(cat "$LOCKFILE" 2>/dev/null || echo "")
  if [ -n "$OTHER_PID" ] && kill -0 "$OTHER_PID" 2>/dev/null; then
    echo "Another image-autopilot-v2 is already running (PID $OTHER_PID). Exiting."
    exit 1
  fi
fi
echo $$ > "$LOCKFILE"
trap 'rm -f "$LOCKFILE"; echo "[$(date -u +%H:%M:%SZ)] image-autopilot-v2 stopped."' EXIT

ts() { date -u +%H:%M:%SZ; }

remaining_to_fetch() {
  node -e "
    const fs=require('fs');
    const d=JSON.parse(fs.readFileSync('docs/data/churches.json','utf8'));
    // Build set of churches already in the JSONL so we count remaining accurately
    const done=new Set();
    if (fs.existsSync('$JSONL_PATH')) {
      for (const l of fs.readFileSync('$JSONL_PATH','utf8').split('\n').filter(Boolean)) {
        try { done.add(JSON.parse(l).id); } catch(e){}
      }
    }
    const stateFilter='$STATE';
    let n=0;
    for(const c of d.churches){
      if(stateFilter!=='all' && !new RegExp(',\\\\s*'+stateFilter+'\\\\b').test(c.address||'')) continue;
      if(c.image_url||c.image_thumb||c.image_fetched_at) continue;
      if(done.has(c.id||c.slug)) continue;
      if(!c.website||!/^https?:/i.test(c.website)) continue;
      n++;
    }
    console.log(n);
  " 2>/dev/null || echo "0"
}

END_TS=$(( $(date +%s) + DURATION_HRS * 3600 ))
echo "[$(ts)] === image-autopilot-v2 starting · duration=${DURATION_HRS}h · tick=${TICK_INTERVAL}s · per_tick=${PER_TICK} · state=${STATE} ==="

TICK=0
EMPTY_TICKS=0
while [ "$(date +%s)" -lt "$END_TS" ]; do
  TICK=$((TICK+1))
  REM=$(remaining_to_fetch)
  echo "[$(ts)] tick $TICK · $REM un-fetched website-having churches remaining (state=$STATE)"
  if [ "$REM" -le 0 ]; then
    echo "[$(ts)] no more work for state=$STATE — stopping early."
    break
  fi

  # 1) Scrape one chunk → appends to JSONL only. Churches.json untouched.
  echo "[$(ts)] scraping up to $PER_TICK images (JSONL mode) ..."
  BEFORE=$([ -f "$JSONL_PATH" ] && wc -l < "$JSONL_PATH" | tr -d ' ' || echo 0)
  node scripts/scrape-church-images.js --state "$STATE" --count "$PER_TICK" --jsonl "$JSONL_PATH" 2>&1 | tail -3
  AFTER=$([ -f "$JSONL_PATH" ] && wc -l < "$JSONL_PATH" | tr -d ' ' || echo 0)
  NEW_THIS_TICK=$((AFTER - BEFORE))

  if [ "$NEW_THIS_TICK" -eq 0 ]; then
    EMPTY_TICKS=$((EMPTY_TICKS+1))
    echo "[$(ts)] 0 new scrape results this tick (empty streak: $EMPTY_TICKS)"
    if [ "$EMPTY_TICKS" -ge 2 ]; then
      echo "[$(ts)] 2 consecutive empty ticks — queue exhausted. Stopping."
      break
    fi
  else
    EMPTY_TICKS=0
    echo "[$(ts)] +$NEW_THIS_TICK new results in JSONL"

    # 2) Pull-rebase BEFORE merge (so we have the latest churches.json from origin)
    git pull --rebase --autostash origin main > /dev/null 2>&1 || echo "[$(ts)] pull-rebase had issues"

    # 3) Merge JSONL → churches.json (single writer, no race possible)
    echo "[$(ts)] merging $NEW_THIS_TICK results into churches.json ..."
    node scripts/merge-image-scrapes.js 2>&1 | tail -5

    # 4) Commit + push
    git add docs/data/churches.json
    if git diff --staged --quiet; then
      echo "[$(ts)] no churches.json changes after merge (unexpected; continuing)"
    else
      git commit -m "Image enrichment v2 tick $TICK: +$NEW_THIS_TICK scrape results merged [$(ts)]" > /dev/null 2>&1
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

echo "[$(ts)] === image-autopilot-v2 finished after $TICK tick(s) ==="
node -e "
const d=JSON.parse(require('fs').readFileSync('docs/data/churches.json','utf8'));
const withImg=d.churches.filter(c=>c.image_url||c.image_thumb).length;
const fetched=d.churches.filter(c=>c.image_fetched_at).length;
console.log('Final: '+withImg+' churches with image · '+fetched+' total fetched');
"
