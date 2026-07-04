#!/bin/bash
# directory-grind-session.sh — a bounded multi-hour local enrichment SESSION.
#
# Loops pastor-refine-local.sh rounds (each: select fresh→retry, fetch church
# sites, local-LLM extract + verbatim-verify pastors, harvest socials, merge,
# regen, consistency, commit, push) with cooldowns until either the duration
# deadline or both enrichment pools run dry.
#
# Called by launchd 4×/day at 4h each = ~16h/day of local-model work (Adam
# 2026-07-04: "make this $7k machine earn its keep"). A session lock prevents
# overlap; each round has its own lock too. `caffeinate` keeps the Mac awake.
#
# Usage: directory-grind-session.sh [duration_hours]   (default 4)
#   env: PASTOR_REFINE_BATCH (default 50), GRIND_COOLDOWN secs (default 540 = 9 min)
set -u
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

DURATION_H="${1:-4}"
case "$DURATION_H" in ''|*[!0-9]*) DURATION_H=4 ;; esac
COOLDOWN="${GRIND_COOLDOWN:-540}"
export PASTOR_REFINE_BATCH="${PASTOR_REFINE_BATCH:-50}"
DEADLINE=$(( $(date +%s) + DURATION_H*3600 ))

LOCK="/tmp/directory-grind-session.lock"
STOP="/tmp/directory-grind-session-stop"
LOG="$HOME/Library/Logs/directory-grind-session.log"
RUNNER="$HOME/bible-reading-plan-bot-autopilot/scripts/pastor-refine-local.sh"
NOTIFY="$HOME/.hermes/bin/notify-adam.sh"
say() { echo "[$(date '+%F %T')] $*" >>"$LOG"; }

mkdir "$LOCK" 2>/dev/null || { say "session lock held — a session is already running, exiting"; exit 0; }
trap 'rmdir "$LOCK" 2>/dev/null' EXIT
[ -f "$RUNNER" ] || { say "FATAL: runner missing at $RUNNER"; exit 1; }

# Snapshot starting pastor count for the wrap-up delta.
START_P=$(node -e '
try{const d=JSON.parse(require("fs").readFileSync(process.env.HOME+"/bible-reading-plan-bot-autopilot/docs/data/churches.json","utf8")).churches;
const ph=p=>{const s=String(p||"").trim();return !s||/^(pastors?|tbd|n\/?a|none|unknown|various|staff)\.?$/i.test(s)||/verify|see website|coming soon|^unknown/i.test(s)};
console.log(d.filter(c=>!ph(c.pastor)).length)}catch(e){console.log(0)}' 2>/dev/null || echo 0)

say "════ ${DURATION_H}h session START (batch $PASTOR_REFINE_BATCH, ${COOLDOWN}s cooldown, start pastors=$START_P) ════"
ROUNDS=0; FAILS=0
while [ "$(date +%s)" -lt "$DEADLINE" ]; do
  [ -f "$STOP" ] && { say "stop switch — ending session"; rm -f "$STOP"; break; }
  if /bin/bash "$RUNNER" >>"$LOG" 2>&1; then
    FAILS=0; ROUNDS=$((ROUNDS+1))
  else
    FAILS=$((FAILS+1)); say "round FAILED (consecutive=$FAILS)"
    [ "$FAILS" -ge 2 ] && { say "two consecutive failures — ending early (alerts already sent)"; break; }
  fi
  # pastor-refine-local.sh prints "grind complete" to its own log when both pools dry.
  tail -6 "$HOME/Library/Logs/pastor-refine-local.log" 2>/dev/null | grep -q "grind complete" && { say "pools dry — nothing left to enrich, ending session early"; break; }
  [ "$(date +%s)" -ge "$DEADLINE" ] && break
  say "cooldown ${COOLDOWN}s…"
  sleep "$COOLDOWN"
done

END_P=$(node -e '
try{const d=JSON.parse(require("fs").readFileSync(process.env.HOME+"/bible-reading-plan-bot-autopilot/docs/data/churches.json","utf8")).churches;
const ph=p=>{const s=String(p||"").trim();return !s||/^(pastors?|tbd|n\/?a|none|unknown|various|staff)\.?$/i.test(s)||/verify|see website|coming soon|^unknown/i.test(s)};
console.log(d.filter(c=>!ph(c.pastor)).length)}catch(e){console.log(0)}' 2>/dev/null || echo 0)
GAIN=$(( END_P - START_P ))
say "════ session DONE: $ROUNDS rounds, +$GAIN pastors this session (total $END_P) ════"
[ -x "$NOTIFY" ] && [ "$ROUNDS" -gt 0 ] && "$NOTIFY" --level info --title "⛏️ Directory grind session done" \
  --body "$ROUNDS rounds, +$GAIN pastors (total $END_P). Live: https://usmcmin.org/grind-report.html" >/dev/null 2>&1 || true
