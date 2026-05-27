#!/bin/bash
# founders-autopilot.sh — cron-style chunked Founders directory scraper.
#
# Each tick: scrape one chunk of Founders pages, integrate matched URLs to
# churches.json, regenerate the networks page, commit + push. Sleeps 10
# minutes between ticks. Stops after configured duration OR when no new
# pages return church listings.
#
# Run detached (recommended):
#     nohup bash scripts/founders-autopilot.sh > /tmp/founders-autopilot.log 2>&1 &
#     tail -f /tmp/founders-autopilot.log
#     # to stop: pkill -f founders-autopilot.sh
#
# Founders has ~1,423 churches across ~24 pages (60/page). At PAGES_PER_TICK=4
# and 10 minute ticks, full crawl needs ~6 ticks = ~1 hour. Default DURATION
# of 3 hours gives plenty of headroom plus retry budget for any failed pages.

set -u
cd /Users/moop_bot_pro/bible-reading-plan-bot || { echo "repo not found"; exit 1; }

DURATION_HRS="${DURATION_HRS:-3}"
TICK_INTERVAL="${TICK_INTERVAL:-600}"        # 10 min
PAGES_PER_TICK="${PAGES_PER_TICK:-4}"
LOCKFILE="/tmp/founders-autopilot.lock"
SCRAPE_OUT="/tmp/founders-scrape.jsonl"

# --- single-instance lock ---
if [ -e "$LOCKFILE" ]; then
  OTHER_PID=$(cat "$LOCKFILE" 2>/dev/null || echo "")
  if [ -n "$OTHER_PID" ] && kill -0 "$OTHER_PID" 2>/dev/null; then
    echo "Another founders-autopilot is already running (PID $OTHER_PID). Exiting."
    exit 1
  fi
fi
echo $$ > "$LOCKFILE"
trap 'rm -f "$LOCKFILE"; echo "[$(date -u +%H:%M:%SZ)] founders-autopilot stopped."' EXIT

ts() { date -u +%H:%M:%SZ; }

# Where does the next page start? Read /tmp/founders-scrape.jsonl to count
# distinct URLs scraped so far, divide by 60-per-page, add 1.
next_page() {
  node -e "
    const fs=require('fs');
    if (!fs.existsSync('$SCRAPE_OUT')) { console.log(1); process.exit(0); }
    const lines = fs.readFileSync('$SCRAPE_OUT','utf8').split('\n').filter(Boolean);
    const urls = new Set();
    for (const l of lines) { try { const r = JSON.parse(l); if (r.network_url) urls.add(r.network_url); } catch(e){} }
    const start = Math.floor(urls.size / 60) + 1;
    console.log(start);
  " 2>/dev/null || echo "1"
}

END_TS=$(( $(date +%s) + DURATION_HRS * 3600 ))
echo "[$(ts)] === founders-autopilot starting · duration=${DURATION_HRS}h · tick=${TICK_INTERVAL}s · pages/tick=${PAGES_PER_TICK} ==="

TICK=0
EMPTY_TICKS=0
while [ "$(date +%s)" -lt "$END_TS" ]; do
  TICK=$((TICK+1))
  START_PAGE=$(next_page)
  echo "[$(ts)] tick $TICK · resuming at page $START_PAGE"

  # 1) Pull-rebase to absorb concurrent commits from other automations
  git pull --rebase --autostash origin main > /dev/null 2>&1 || echo "[$(ts)] pull-rebase had issues (continuing)"

  # 2) Scrape a chunk of pages
  BEFORE_LINES=$([ -f "$SCRAPE_OUT" ] && wc -l < "$SCRAPE_OUT" | tr -d ' ' || echo 0)
  echo "[$(ts)] scraping pages $START_PAGE..$((START_PAGE + PAGES_PER_TICK - 1)) ..."
  node scripts/scrape-founders-directory.js --start "$START_PAGE" --pages "$PAGES_PER_TICK" 2>&1 | tail -3
  AFTER_LINES=$([ -f "$SCRAPE_OUT" ] && wc -l < "$SCRAPE_OUT" | tr -d ' ' || echo 0)
  NEW_THIS_TICK=$((AFTER_LINES - BEFORE_LINES))

  if [ "$NEW_THIS_TICK" -eq 0 ]; then
    EMPTY_TICKS=$((EMPTY_TICKS+1))
    echo "[$(ts)] 0 new URLs this tick (empty streak: $EMPTY_TICKS)"
    if [ "$EMPTY_TICKS" -ge 2 ]; then
      echo "[$(ts)] 2 consecutive empty ticks — directory exhausted. Stopping early."
      break
    fi
  else
    EMPTY_TICKS=0
    echo "[$(ts)] +$NEW_THIS_TICK new church URLs scraped"

    # 3) Integrate into churches.json (writes cross_listed_urls.founders)
    echo "[$(ts)] integrating ..."
    INTEGRATE_OUT=$(node scripts/integrate-network-urls.js --network founders 2>&1)
    echo "$INTEGRATE_OUT" | grep -E "matched|written|coverage" | head -3

    # 4) Regenerate networks page
    node scripts/build-directory-networks.js > /dev/null 2>&1

    # 5) Commit + push (churches.json + networks HTML)
    git add docs/data/churches.json docs/directory-networks.html
    if git diff --staged --quiet; then
      echo "[$(ts)] no changes to commit"
    else
      git commit -m "Founders autopilot tick $TICK: +Founders deep-links via directory scrape (+$NEW_THIS_TICK URLs) [$(ts)]" > /dev/null 2>&1
      if ! git push origin main > /dev/null 2>&1; then
        echo "[$(ts)] push rejected — pull-rebasing and retrying ..."
        git pull --rebase --autostash origin main > /dev/null 2>&1
        git push origin main > /dev/null 2>&1
      fi
      echo "[$(ts)] committed + pushed tick $TICK"
    fi
  fi

  # 6) Sleep until next tick (unless past end window)
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

echo "[$(ts)] === founders-autopilot finished after $TICK tick(s) ==="
if [ -f "$SCRAPE_OUT" ]; then
  TOTAL=$(wc -l < "$SCRAPE_OUT" | tr -d ' ')
  echo "Final: $TOTAL Founders church URLs in $SCRAPE_OUT"
fi
