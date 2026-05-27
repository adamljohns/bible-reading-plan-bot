#!/bin/bash
# image-autopilot.sh — image enrichment driver, 30-minute tick cadence.
#
# Each tick: git pull --rebase, scrape the next ~60 church website images,
# commit + push. Sleeps 30 minutes between ticks. Stops after the configured
# duration OR when no more website-having churches remain to enrich.
#
# Run detached (recommended — survives terminal/session close):
#     nohup bash scripts/image-autopilot.sh > /tmp/image-autopilot.log 2>&1 &
#     tail -f /tmp/image-autopilot.log
#     # to stop:  pkill -f image-autopilot.sh
#
# Defaults:
#   DURATION_HRS=8     total wall-clock runtime
#   TICK_INTERVAL=1800 seconds between ticks (30 min)
#   PER_TICK=60        churches scraped per tick (60 * 3s polite = ~3 min work)
#   STATE=all          --state arg to scraper (set to VA / NC / etc. to scope)
#
# Override via env: DURATION_HRS=4 PER_TICK=30 STATE=NC bash scripts/image-autopilot.sh

set -u
cd /Users/moop_bot_pro/bible-reading-plan-bot || { echo "repo not found"; exit 1; }

DURATION_HRS="${DURATION_HRS:-8}"
TICK_INTERVAL="${TICK_INTERVAL:-1800}"
PER_TICK="${PER_TICK:-60}"
STATE="${STATE:-all}"
LOCKFILE="/tmp/image-autopilot.lock"

# --- single-instance lock ---
if [ -e "$LOCKFILE" ]; then
  OTHER_PID=$(cat "$LOCKFILE" 2>/dev/null || echo "")
  if [ -n "$OTHER_PID" ] && kill -0 "$OTHER_PID" 2>/dev/null; then
    echo "Another image-autopilot is already running (PID $OTHER_PID). Exiting."
    exit 1
  fi
fi
echo $$ > "$LOCKFILE"
trap 'rm -f "$LOCKFILE"; echo "[$(date -u +%H:%M:%SZ)] image-autopilot stopped."' EXIT

ts() { date -u +%H:%M:%SZ; }

# Count of remaining un-fetched website-having churches (for the configured state)
remaining_to_fetch() {
  node -e "
    const fs=require('fs');
    const d=JSON.parse(fs.readFileSync('docs/data/churches.json','utf8'));
    const stateFilter='$STATE';
    let n=0;
    for(const c of d.churches){
      if(stateFilter!=='all' && !new RegExp(',\\\\s*'+stateFilter+'\\\\b').test(c.address||'')) continue;
      if(c.image_url||c.image_thumb||c.image_fetched_at) continue;
      if(!c.website||!/^https?:/i.test(c.website)) continue;
      n++;
    }
    console.log(n);
  " 2>/dev/null || echo "0"
}

END_TS=$(( $(date +%s) + DURATION_HRS * 3600 ))
echo "[$(ts)] === image-autopilot starting · duration=${DURATION_HRS}h · tick=${TICK_INTERVAL}s · per_tick=${PER_TICK} · state=${STATE} ==="

TICK=0
while [ "$(date +%s)" -lt "$END_TS" ]; do
  TICK=$((TICK+1))
  REM=$(remaining_to_fetch)
  echo "[$(ts)] tick $TICK · $REM un-fetched website-having churches remaining (state=$STATE)"

  if [ "$REM" -le 0 ]; then
    echo "[$(ts)] no more work for state=$STATE — stopping early."
    break
  fi

  # 1) Pull-rebase to absorb concurrent dictionary loop commits
  git pull --rebase origin main > /dev/null 2>&1 || echo "[$(ts)] pull-rebase had issues (continuing)"

  # 2) Scrape one tick's worth of images
  echo "[$(ts)] scraping up to $PER_TICK images ..."
  node scripts/scrape-church-images.js --state "$STATE" --count "$PER_TICK" 2>&1 | tail -3

  # 3) Commit + push (only if churches.json actually changed)
  git add docs/data/churches.json
  if git diff --staged --quiet; then
    echo "[$(ts)] no changes to commit this tick"
  else
    git commit -m "Image enrichment tick $TICK: +images via OG scrape (state=$STATE) [$(ts)]" > /dev/null 2>&1
    if ! git push origin main > /dev/null 2>&1; then
      echo "[$(ts)] push rejected — pull-rebasing and retrying ..."
      git pull --rebase origin main > /dev/null 2>&1
      git push origin main > /dev/null 2>&1
    fi
    echo "[$(ts)] committed + pushed tick $TICK"
  fi

  # 4) Sleep until next tick (unless we'd exceed end time, then exit)
  NEXT_TS=$(( $(date +%s) + TICK_INTERVAL ))
  if [ "$NEXT_TS" -ge "$END_TS" ]; then
    REMAIN_SEC=$(( END_TS - $(date +%s) ))
    if [ "$REMAIN_SEC" -gt 60 ]; then
      echo "[$(ts)] partial final sleep of ${REMAIN_SEC}s remaining in window ..."
      sleep "$REMAIN_SEC"
    fi
    break
  fi
  echo "[$(ts)] sleeping ${TICK_INTERVAL}s until next tick ..."
  sleep "$TICK_INTERVAL"
done

echo "[$(ts)] === image-autopilot finished after $TICK tick(s) ==="
node -e "
const d=JSON.parse(require('fs').readFileSync('docs/data/churches.json','utf8'));
const withImg=d.churches.filter(c=>c.image_url||c.image_thumb).length;
const withFetched=d.churches.filter(c=>c.image_fetched_at).length;
console.log('Final: '+withImg+' churches with image_url/thumb · '+withFetched+' total fetched (including no-image responses)');
"
