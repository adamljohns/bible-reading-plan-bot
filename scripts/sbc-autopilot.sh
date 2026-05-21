#!/bin/bash
# sbc-autopilot.sh — unattended SBC bulk-load driver.
#
# Scrapes the SBC.net sitemap in chunks. After each chunk it merges the new
# records into churches.json, regenerates the per-church pages + sitemap, and
# commits + pushes. Because every completed chunk is pushed before the next one
# starts, a kill (session end, machine sleep, Ctrl-C) only ever costs the
# in-flight chunk — and even that is recoverable from the crash-safe JSONL on
# the next run.
#
# Run attended (Claude-driven, dies with the session):
#     bash scripts/sbc-autopilot.sh
#
# Run DETACHED (survives terminal/session close — recommended for overnight):
#     nohup bash scripts/sbc-autopilot.sh > /tmp/sbc-autopilot.log 2>&1 &
#     tail -f /tmp/sbc-autopilot.log      # watch progress
#     # to stop it later:  pkill -f sbc-autopilot.sh
#
# Only ONE instance should run at a time — two scrapers hitting SBC.net
# simultaneously would violate the polite crawl-delay. The lockfile below
# enforces that.

set -u
cd /Users/moop_bot_pro/bible-reading-plan-bot || { echo "repo not found"; exit 1; }

CHUNK="${SBC_CHUNK:-1500}"          # URLs per chunk (override: SBC_CHUNK=1000 bash ...)
MAX_CHUNKS="${SBC_MAX_CHUNKS:-100}" # safety cap so it can never loop forever
LOCKFILE="/tmp/sbc-autopilot.lock"
TODO="/tmp/sbc-todo.json"
SCRAPE_DIR="/tmp/sbc-scraped"

# --- single-instance lock ---
if [ -e "$LOCKFILE" ]; then
  OTHER_PID=$(cat "$LOCKFILE" 2>/dev/null || echo "")
  if [ -n "$OTHER_PID" ] && kill -0 "$OTHER_PID" 2>/dev/null; then
    echo "Another autopilot is already running (PID $OTHER_PID). Exiting."
    exit 1
  fi
fi
echo $$ > "$LOCKFILE"
trap 'rm -f "$LOCKFILE"; echo "[$(date -u +%H:%M:%SZ)] autopilot stopped."' EXIT

ts() { date -u +%H:%M:%SZ; }

# Count URLs in the TODO that have NOT been scraped yet.
remaining() {
  node -e "
    const fs=require('fs'),path=require('path');
    const todo=JSON.parse(fs.readFileSync('$TODO','utf8'));
    const dir='$SCRAPE_DIR';
    const done=new Set();
    if(fs.existsSync(dir)){
      for(const f of fs.readdirSync(dir)){
        if(!f.endsWith('.jsonl'))continue;
        for(const l of fs.readFileSync(path.join(dir,f),'utf8').split('\n').filter(Boolean)){
          try{done.add(JSON.parse(l).slug)}catch(e){}
        }
      }
    }
    console.log(todo.urls.filter(u=>!done.has(u.slug)).length);
  " 2>/dev/null || echo "0"
}

echo "[$(ts)] === SBC autopilot starting · chunk=$CHUNK · max_chunks=$MAX_CHUNKS ==="

for (( c=1; c<=MAX_CHUNKS; c++ )); do
  REM=$(remaining)
  echo "[$(ts)] chunk $c/$MAX_CHUNKS · $REM URLs remaining in queue"
  if [ "$REM" -le 0 ]; then
    echo "[$(ts)] queue empty — bulk-load complete. Stopping."
    break
  fi

  # 1) Scrape one chunk (crash-safe; resumes from first un-scraped URL)
  echo "[$(ts)] scraping up to $CHUNK URLs ..."
  node scripts/sbc-scrape-batch.js --resume --count "$CHUNK" 2>&1 | tail -3

  # 2) Merge into churches.json
  echo "[$(ts)] merging ..."
  MERGE_OUT=$(node scripts/sbc-merge.js 2>&1)
  ADDED=$(echo "$MERGE_OUT" | grep -oE "Added \(net-new\): +[0-9]+" | grep -oE "[0-9]+" | head -1)
  ADDED="${ADDED:-0}"
  echo "$MERGE_OUT" | grep -E "Found|Added|Skipped|Wrote"

  if [ "$ADDED" -eq 0 ]; then
    echo "[$(ts)] 0 net-new this chunk (all dupes or fetch errors). Skipping commit."
    continue
  fi

  # 3) Regenerate per-church pages + sitemap
  echo "[$(ts)] regenerating pages + sitemap ..."
  node generate-church-pages.js > /dev/null 2>&1
  node scripts/build-sitemap-churches.js > /dev/null 2>&1

  # 4) Commit + push (pull-rebase first to absorb concurrent dictionary commits)
  TOTAL=$(node -e "console.log(JSON.parse(require('fs').readFileSync('docs/data/churches.json','utf8')).churches.length)" 2>/dev/null || echo "?")
  git add docs/data/churches.json docs/churches/ docs/sitemap-churches.xml 2>/dev/null
  git commit -m "SBC autopilot: +$ADDED records (chunk $c, $TOTAL total) [$(ts)]" > /dev/null 2>&1
  # Rebase onto any commits the dictionary loop pushed while we scraped, then push
  if ! git push origin main > /dev/null 2>&1; then
    echo "[$(ts)] push rejected — pull-rebasing and retrying ..."
    git pull --rebase origin main > /dev/null 2>&1
    git push origin main > /dev/null 2>&1
  fi
  echo "[$(ts)] committed +$ADDED · directory now $TOTAL churches · pushed."

  sleep 3
done

echo "[$(ts)] === SBC autopilot finished after $((c-1)) chunk(s) ==="
node scripts/sbc-status.js | head -12
