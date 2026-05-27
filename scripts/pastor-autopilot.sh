#!/bin/bash
# pastor-autopilot.sh — race-free pastor-name enrichment driver.
#
# Per tick: scrape next 40 church websites for pastor name → merge → commit.
# Each church takes 5-15s (multiple paths attempted with sub-delays).
#
# STARTING SCOPE: VA only (lifts the 340 missing-pastor VA churches first).
# Override with STATE=all to crawl nationwide once VA is done.
#
# Run detached:
#     STATE=VA nohup bash scripts/pastor-autopilot.sh > /tmp/pastor-autopilot.log 2>&1 &

set -u
cd /Users/moop_bot_pro/bible-reading-plan-bot || { echo "repo not found"; exit 1; }

DURATION_HRS="${DURATION_HRS:-6}"
TICK_INTERVAL="${TICK_INTERVAL:-1200}"      # 20 min
PER_TICK="${PER_TICK:-40}"                   # 40 churches × ~10s each = ~7 min
STATE="${STATE:-VA}"                         # default to VA backfill first
LOCKFILE="/tmp/pastor-autopilot.lock"
JSONL_PATH="/tmp/pastor-scrapes.jsonl"

if [ -e "$LOCKFILE" ]; then
  OTHER_PID=$(cat "$LOCKFILE" 2>/dev/null || echo "")
  if [ -n "$OTHER_PID" ] && kill -0 "$OTHER_PID" 2>/dev/null; then
    echo "Another pastor-autopilot already running (PID $OTHER_PID). Exiting."
    exit 1
  fi
fi
echo $$ > "$LOCKFILE"
trap 'rm -f "$LOCKFILE"; echo "[$(date -u +%H:%M:%SZ)] pastor-autopilot stopped."' EXIT

ts() { date -u +%H:%M:%SZ; }

remaining_to_fetch() {
  node -e "
    const fs=require('fs');
    const d=JSON.parse(fs.readFileSync('docs/data/churches.json','utf8'));
    const PH=/^(verify|various|unknown|see\\s+website|currently|none|listed|tbd|n\\/a|the\\s+pastor|the\\s+church|various\\s+pastors|pastoral)/i;
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
      if(c.pastor && !PH.test(String(c.pastor).trim()) && String(c.pastor).length > 4) continue;
      if(!c.website||!/^https?:/i.test(c.website)) continue;
      n++;
    }
    console.log(n);
  " 2>/dev/null || echo "0"
}

END_TS=$(( $(date +%s) + DURATION_HRS * 3600 ))
echo "[$(ts)] === pastor-autopilot starting · duration=${DURATION_HRS}h · tick=${TICK_INTERVAL}s · per_tick=${PER_TICK} · state=${STATE} ==="

TICK=0
EMPTY_TICKS=0
while [ "$(date +%s)" -lt "$END_TS" ]; do
  TICK=$((TICK+1))
  REM=$(remaining_to_fetch)
  echo "[$(ts)] tick $TICK · $REM churches missing pastor (state=$STATE)"
  if [ "$REM" -le 0 ]; then
    echo "[$(ts)] no more candidates for state=$STATE — stopping."
    break
  fi

  echo "[$(ts)] scraping up to $PER_TICK pastor pages ..."
  BEFORE=$([ -f "$JSONL_PATH" ] && wc -l < "$JSONL_PATH" | tr -d ' ' || echo 0)
  node scripts/scrape-church-pastors.js --state "$STATE" --count "$PER_TICK" --jsonl "$JSONL_PATH" 2>&1 | tail -3
  AFTER=$([ -f "$JSONL_PATH" ] && wc -l < "$JSONL_PATH" | tr -d ' ' || echo 0)
  NEW_THIS_TICK=$((AFTER - BEFORE))

  if [ "$NEW_THIS_TICK" -eq 0 ]; then
    EMPTY_TICKS=$((EMPTY_TICKS+1))
    if [ "$EMPTY_TICKS" -ge 2 ]; then
      echo "[$(ts)] 2 consecutive empty ticks — stopping."
      break
    fi
  else
    EMPTY_TICKS=0
    git pull --rebase --autostash origin main > /dev/null 2>&1 || true
    echo "[$(ts)] merging $NEW_THIS_TICK results ..."
    node scripts/merge-pastor-scrapes.js 2>&1 | tail -5

    git add docs/data/churches.json
    if git diff --staged --quiet; then
      echo "[$(ts)] no changes"
    else
      git commit -m "Pastor enrichment tick $TICK: +$NEW_THIS_TICK website scrapes (state=$STATE) [$(ts)]" > /dev/null 2>&1
      if ! git push origin main > /dev/null 2>&1; then
        git pull --rebase --autostash origin main > /dev/null 2>&1
        git push origin main > /dev/null 2>&1
      fi
      echo "[$(ts)] committed + pushed tick $TICK"
    fi
  fi

  NEXT_TS=$(( $(date +%s) + TICK_INTERVAL ))
  if [ "$NEXT_TS" -ge "$END_TS" ]; then break; fi
  echo "[$(ts)] sleeping ${TICK_INTERVAL}s ..."
  sleep "$TICK_INTERVAL"
done

echo "[$(ts)] === pastor-autopilot finished after $TICK tick(s) ==="
