#!/bin/bash
# quicklinks-autopilot.sh — race-free deep-link discovery driver.
#
# Per tick: scrape next N church websites for /beliefs, /sermons, /staff,
# /about, /visit, /events, /give, /mens-ministry, /kids paths → merge JSONL
# into churches.json → regenerate per-church pages → commit + push.
#
# Run detached:
#     STATE=VA DURATION_HRS=1 nohup bash scripts/quicklinks-autopilot.sh > /tmp/quicklinks-autopilot.log 2>&1 &

set -u
cd /Users/moop_bot_pro/bible-reading-plan-bot || { echo "repo not found"; exit 1; }

DURATION_HRS="${DURATION_HRS:-1}"
TICK_INTERVAL="${TICK_INTERVAL:-900}"   # 15 min between ticks
PER_TICK="${PER_TICK:-30}"               # 30 churches per tick (~8-10 min scrape)
STATE="${STATE:-all}"
LOCKFILE="/tmp/quicklinks-autopilot.lock"
JSONL_PATH="/tmp/quicklinks-scrapes.jsonl"

if [ -e "$LOCKFILE" ]; then
  OTHER_PID=$(cat "$LOCKFILE" 2>/dev/null || echo "")
  if [ -n "$OTHER_PID" ] && kill -0 "$OTHER_PID" 2>/dev/null; then
    echo "Another quicklinks-autopilot already running (PID $OTHER_PID). Exiting."
    exit 1
  fi
fi
echo $$ > "$LOCKFILE"
trap 'rm -f "$LOCKFILE"; echo "[$(date -u +%H:%M:%SZ)] quicklinks-autopilot stopped."' EXIT

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
      if(stateFilter!=='all' && !new RegExp(',\\\\s*'+stateFilter+'\\\\b').test(c.address||'')) continue;
      if(done.has(c.id||c.slug)) continue;
      if(!c.website||!/^https?:\\/\\/[^\\/\\s]/i.test(c.website)) continue;
      if(Array.isArray(c.quick_links) && c.quick_links.length > 0) continue;
      n++;
    }
    console.log(n);
  " 2>/dev/null || echo "0"
}

END_TS=$(( $(date +%s) + DURATION_HRS * 3600 ))
echo "[$(ts)] === quicklinks-autopilot starting · duration=${DURATION_HRS}h · tick=${TICK_INTERVAL}s · per_tick=${PER_TICK} · state=${STATE} ==="

TICK=0
EMPTY_TICKS=0
while [ "$(date +%s)" -lt "$END_TS" ]; do
  TICK=$((TICK+1))
  REM=$(remaining_to_fetch)
  echo "[$(ts)] tick $TICK · $REM churches missing quick_links remaining (state=${STATE})"
  if [ "$REM" -le 0 ]; then
    echo "[$(ts)] queue exhausted — stopping early."
    break
  fi

  echo "[$(ts)] scraping up to $PER_TICK church websites (state=${STATE}) ..."
  BEFORE=$([ -f "$JSONL_PATH" ] && wc -l < "$JSONL_PATH" | tr -d ' ' || echo 0)
  STATE_ARG=""
  if [ "$STATE" != "all" ]; then STATE_ARG="--state $STATE"; fi
  node scripts/scrape-church-quicklinks.js --count "$PER_TICK" --jsonl "$JSONL_PATH" $STATE_ARG 2>&1 | tail -3
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
    node scripts/merge-church-quicklinks.js 2>&1 | tail -3

    echo "[$(ts)] regenerating per-church pages ..."
    node generate-church-pages.js 2>&1 | tail -2

    git add docs/data/churches.json docs/churches/
    if git diff --staged --quiet; then
      echo "[$(ts)] no changes after merge+regen"
    else
      git commit -m "Quicklinks tick $TICK: +$NEW_THIS_TICK church-website deep-link scrapes (state=${STATE}) [$(ts)]" > /dev/null 2>&1
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

echo "[$(ts)] === quicklinks-autopilot finished after $TICK tick(s) ==="
