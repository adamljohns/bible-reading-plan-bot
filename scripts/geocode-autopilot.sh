#!/bin/bash
# geocode-autopilot.sh — grind through ungeocoded street-address churches.
#
# Per tick: geocode a chunk (Census batch + one-line; Nominatim optional) ->
# regenerate the map -> commit + push. Census batch is fast, so chunks are
# large. Runs until the street-address queue empties or the duration closes.
#
# Run detached:
#     DURATION_HRS=8 nohup bash scripts/geocode-autopilot.sh > /tmp/geocode-autopilot.log 2>&1 &

set -u
cd /Users/moop_bot_pro/bible-reading-plan-bot || { echo "repo not found"; exit 1; }

DURATION_HRS="${DURATION_HRS:-8}"
TICK_INTERVAL="${TICK_INTERVAL:-120}"   # 2 min between ticks (batch is fast)
PER_TICK="${PER_TICK:-500}"
STATE="${STATE:-}"
NOMINATIM="${NOMINATIM:-0}"             # 0 = skip Nominatim for speed; 1 = include
LOCKFILE="/tmp/geocode-autopilot.lock"

if [ -e "$LOCKFILE" ]; then
  OTHER_PID=$(cat "$LOCKFILE" 2>/dev/null || echo "")
  if [ -n "$OTHER_PID" ] && kill -0 "$OTHER_PID" 2>/dev/null; then
    echo "Another geocode-autopilot already running (PID $OTHER_PID). Exiting."; exit 1
  fi
fi
echo $$ > "$LOCKFILE"
trap 'rm -f "$LOCKFILE"; echo "[$(date -u +%H:%M:%SZ)] geocode-autopilot stopped."' EXIT
ts() { date -u +%H:%M:%SZ; }

remaining() {
  node -e "
    const fs=require('fs');
    const STATE_ABBR={alabama:'AL',alaska:'AK',arizona:'AZ',arkansas:'AR',california:'CA',colorado:'CO',connecticut:'CT',delaware:'DE',florida:'FL',georgia:'GA',hawaii:'HI',idaho:'ID',illinois:'IL',indiana:'IN',iowa:'IA',kansas:'KS',kentucky:'KY',louisiana:'LA',maine:'ME',maryland:'MD',massachusetts:'MA',michigan:'MI',minnesota:'MN',mississippi:'MS',missouri:'MO',montana:'MT',nebraska:'NE',nevada:'NV','new hampshire':'NH','new jersey':'NJ','new mexico':'NM','new york':'NY','north carolina':'NC','north dakota':'ND',ohio:'OH',oklahoma:'OK',oregon:'OR',pennsylvania:'PA','rhode island':'RI','south carolina':'SC','south dakota':'SD',tennessee:'TN',texas:'TX',utah:'UT',vermont:'VT',virginia:'VA',washington:'WA','west virginia':'WV',wisconsin:'WI',wyoming:'WY','district of columbia':'DC'};
    function norm(a){if(!a)return a;let s=String(a);s=s.replace(/,?\\s*United States of America\\b/gi,'').replace(/,?\\s*United States\\b/gi,'').replace(/,?\\s*USA\\b/g,'');for(const n of Object.keys(STATE_ABBR).sort((x,y)=>y.length-x.length)){const re=new RegExp('\\\\b'+n.replace(/ /g,'\\\\s+')+'\\\\b','i');if(re.test(s)){s=s.replace(re,STATE_ABBR[n]);break;}}return s;}
    const d=JSON.parse(fs.readFileSync('docs/data/churches.json','utf8'));
    let n=0; const st='$STATE';
    for(const c of d.churches){ if(typeof c.latitude==='number')continue; const a=norm(c.address||''); if(st&&!new RegExp(',\\\\s*'+st+'\\\\b').test(a))continue; if(/\\d+\\s+\\w/.test(a)&&/,/.test(a))n++; }
    console.log(n);
  " 2>/dev/null || echo 0
}

END_TS=$(( $(date +%s) + DURATION_HRS * 3600 ))
echo "[$(ts)] === geocode-autopilot · duration=${DURATION_HRS}h · per_tick=${PER_TICK} · state=${STATE:-ALL} · nominatim=${NOMINATIM} ==="

TICK=0
while [ "$(date +%s)" -lt "$END_TS" ]; do
  TICK=$((TICK+1))
  REM=$(remaining)
  echo "[$(ts)] tick $TICK · $REM street-address churches still ungeocoded"
  if [ "$REM" -le 0 ]; then echo "[$(ts)] queue exhausted — stopping."; break; fi

  ARGS="--count $PER_TICK"
  [ -n "$STATE" ] && ARGS="$ARGS --state $STATE"
  [ "$NOMINATIM" = "0" ] && ARGS="$ARGS --no-nominatim"

  echo "[$(ts)] geocoding up to $PER_TICK ..."
  node scripts/geocode-all.js $ARGS 2>&1 | tail -4

  git pull --rebase --autostash origin main > /dev/null 2>&1 || true
  echo "[$(ts)] regenerating map ..."
  node scripts/build-directory-map.js 2>&1 | grep -E 'points\)' || true

  git add docs/data/churches.json docs/data/directory-map-points.json docs/directory-map.html
  if git diff --staged --quiet; then
    echo "[$(ts)] no changes this tick"
  else
    git commit -m "Geocode autopilot tick $TICK: more churches placed on the map [$(ts)]" > /dev/null 2>&1
    if ! git push origin main > /dev/null 2>&1; then
      git pull --rebase --autostash origin main > /dev/null 2>&1; git push origin main > /dev/null 2>&1
    fi
    echo "[$(ts)] committed + pushed tick $TICK"
  fi

  NEXT_TS=$(( $(date +%s) + TICK_INTERVAL ))
  if [ "$NEXT_TS" -ge "$END_TS" ]; then break; fi
  sleep "$TICK_INTERVAL"
done
echo "[$(ts)] === geocode-autopilot finished after $TICK tick(s) ==="
