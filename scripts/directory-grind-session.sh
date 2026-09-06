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
# Rounds commit every ~11 min. Each push used to trigger its own 3-minute,
# five-gate site deploy, so one 4h session queued ~22 of them back-to-back
# (concurrency group deploy-r2 is serial) and any gate failure blocked the
# whole line. Rounds now commit [skip ci]; publish_session_output below fires
# exactly ONE deploy when the session ends. 4 sessions/day = 4 deploys/day.
export GRIND_DEFER_DEPLOY=1
export PASTOR_REFINE_BATCH="${PASTOR_REFINE_BATCH:-50}"
DEADLINE=$(( $(date +%s) + DURATION_H*3600 ))

LOCK="/tmp/directory-grind-session.lock"
STOP="/tmp/directory-grind-session-stop"
LOG="$HOME/Library/Logs/directory-grind-session.log"
RUNNER="$HOME/bible-reading-plan-bot-autopilot/scripts/pastor-refine-local.sh"
NOTIFY="$HOME/.hermes/bin/notify-adam.sh"
say() { echo "[$(date '+%F %T')] $*" >>"$LOG"; }

# One deploy for the whole session. The rounds already pushed their content
# with [skip ci]; this empty commit is the trigger. Idempotent: it no-ops when
# no round landed anything, and runs from the trap so a killed session still
# publishes. Uses git, not `gh` — gh reads its token from the Keychain, which
# is exactly the thing that does not work from launchd.
DEPLOY_FIRED=0
publish_session_output() {
  [ "${ROUNDS:-0}" -gt 0 ] || { say "no rounds landed — no deploy to fire"; return 0; }
  [ "$DEPLOY_FIRED" = "1" ] && return 0
  DEPLOY_FIRED=1
  local wt="$HOME/bible-reading-plan-bot-autopilot"
  git -C "$wt" fetch -q origin main || { say "ALERT: deploy trigger fetch failed — session output is pushed but NOT deployed"; return 1; }
  if ! git -C "$wt" diff --quiet origin/main -- docs 2>/dev/null; then
    say "deploy trigger: worktree docs differ from origin/main — refusing to fire, run deploy by hand"
    return 1
  fi
  git -C "$wt" commit -q --allow-empty -m "deploy: publish grind session output ($ROUNDS rounds)" \
    || { say "ALERT: deploy trigger commit failed"; return 1; }
  if git -C "$wt" push -q origin HEAD:main; then
    say "deploy fired: one run for $ROUNDS deferred rounds"
  else
    git -C "$wt" fetch -q origin main && git -C "$wt" rebase -q FETCH_HEAD && git -C "$wt" push -q origin HEAD:main \
      && say "deploy fired after rebase: one run for $ROUNDS deferred rounds" \
      || say "ALERT: deploy trigger push failed — session output is pushed but NOT deployed"
  fi
}

mkdir "$LOCK" 2>/dev/null || { say "session lock held — a session is already running, exiting"; exit 0; }
trap 'publish_session_output; rmdir "$LOCK" 2>/dev/null' EXIT
[ -f "$RUNNER" ] || { say "FATAL: runner missing at $RUNNER"; exit 1; }

# Snapshot starting pastor count for the wrap-up delta.
START_P=$(node -e '
try{const d=JSON.parse(require("fs").readFileSync(process.env.HOME+"/bible-reading-plan-bot-autopilot/docs/data/churches.json","utf8")).churches;
const ph=p=>{const s=String(p||"").trim();return !s||/^(pastors?|tbd|n\/?a|none|unknown|various|staff)\.?$/i.test(s)||/verify|see website|coming soon|^unknown/i.test(s)};
console.log(d.filter(c=>!ph(c.pastor)).length)}catch(e){console.log(0)}' 2>/dev/null || echo 0)
START_C=$(node -e '
try{const d=JSON.parse(require("fs").readFileSync(process.env.HOME+"/bible-reading-plan-bot-autopilot/docs/data/churches.json","utf8")).churches;
const ph=p=>{const s=String(p||"").trim();return !s||/^(pastors?|tbd|n\/?a|none|unknown|various|staff)\.?$/i.test(s)||/verify|see website|coming soon|^unknown/i.test(s)};
const n=c=>(!ph(c.pastor)?1:0)+Object.keys(c.scores||{}).filter(k=>c.scores[k]).length+(String(c.assessment||"").trim()?1:0)+(c.facebook?1:0)+(c.youtube?1:0)+(c.instagram?1:0)+(c.phone?1:0)+(c.website?1:0)+(c.address?1:0)+(c.denomination_family||c.denomination?1:0);
console.log(d.reduce((a,c)=>a+n(c),0))}catch(e){console.log(0)}' 2>/dev/null || echo 0)

round_was_zero_yield() {
  tail -30 "$HOME/Library/Logs/pastor-refine-local.log" 2>/dev/null \
    | grep -q "zero applied — skip qa-sample/grind-stats/regen/commit/push"
}

say "════ ${DURATION_H}h session START (batch $PASTOR_REFINE_BATCH, ${COOLDOWN}s cooldown, start pastors=$START_P, profile_fields=$START_C) ════"
ROUNDS=0; FAILS=0; ZERO_STREAK=0; ABORT_REASON=""; LFS_WARNINGS=0
while [ "$(date +%s)" -lt "$DEADLINE" ]; do
  [ -f "$STOP" ] && { say "stop switch — ending session"; rm -f "$STOP"; break; }
  # Do not abort on a small/empty fresh pool. pastor-refine-local.sh defers
  # sub-floor trickles and the yield-gate falls through to source-recovery.
  # The 2026-08-31..09-04 stall was 17 launchd fires exiting 0 with 0 rounds
  # while source-recovery still had 9k+ eligible records.
  if /bin/bash "$RUNNER" >>"$LOG" 2>&1; then
    FAILS=0; ROUNDS=$((ROUNDS+1))
    if round_was_zero_yield; then
      ZERO_STREAK=$((ZERO_STREAK+1))
      say "zero-yield round (consecutive=$ZERO_STREAK)"
      [ "$ZERO_STREAK" -ge 3 ] && { ABORT_REASON="aborted: 3 consecutive +0 rounds"; say "$ABORT_REASON"; break; }
    else
      ZERO_STREAK=0
    fi
    LFS_WARN=$(tail -40 "$HOME/Library/Logs/pastor-refine-local.log" 2>/dev/null | grep -ci 'git lfs' || true)
    LFS_WARNINGS=$((LFS_WARNINGS + LFS_WARN))
  else
    RC=$?
    # Exit 3 = the yield gate halted the round on purpose (dead pool). That is a
    # correct outcome, not a fault: end the session cleanly instead of burning a
    # second round to prove it twice.
    if [ "$RC" -eq 3 ]; then
      ABORT_REASON="aborted: yield gate HALT (dead pool)"; say "$ABORT_REASON"; break
    fi
    FAILS=$((FAILS+1)); say "round FAILED rc=$RC (consecutive=$FAILS)"
    [ "$FAILS" -ge 2 ] && { say "two consecutive failures — ending early (alerts already sent)"; break; }
  fi
  # Extraction-pool exhaustion now advances into bounded frontier lanes. Only a
  # true monitoring heartbeat (no executable automated lane remains) ends early.
  tail -8 "$HOME/Library/Logs/pastor-refine-local.log" 2>/dev/null | grep -q "frontier lane done: monitoring" && { say "automated lanes exhausted — review/dead-site queues remain"; break; }
  [ "$(date +%s)" -ge "$DEADLINE" ] && break
  say "cooldown ${COOLDOWN}s…"
  sleep "$COOLDOWN"
done

END_P=$(node -e '
try{const d=JSON.parse(require("fs").readFileSync(process.env.HOME+"/bible-reading-plan-bot-autopilot/docs/data/churches.json","utf8")).churches;
const ph=p=>{const s=String(p||"").trim();return !s||/^(pastors?|tbd|n\/?a|none|unknown|various|staff)\.?$/i.test(s)||/verify|see website|coming soon|^unknown/i.test(s)};
console.log(d.filter(c=>!ph(c.pastor)).length)}catch(e){console.log(0)}' 2>/dev/null || echo 0)
END_C=$(node -e '
try{const d=JSON.parse(require("fs").readFileSync(process.env.HOME+"/bible-reading-plan-bot-autopilot/docs/data/churches.json","utf8")).churches;
const ph=p=>{const s=String(p||"").trim();return !s||/^(pastors?|tbd|n\/?a|none|unknown|various|staff)\.?$/i.test(s)||/verify|see website|coming soon|^unknown/i.test(s)};
const n=c=>(!ph(c.pastor)?1:0)+Object.keys(c.scores||{}).filter(k=>c.scores[k]).length+(String(c.assessment||"").trim()?1:0)+(c.facebook?1:0)+(c.youtube?1:0)+(c.instagram?1:0)+(c.phone?1:0)+(c.website?1:0)+(c.address?1:0)+(c.denomination_family||c.denomination?1:0);
console.log(d.reduce((a,c)=>a+n(c),0))}catch(e){console.log(0)}' 2>/dev/null || echo 0)
GAIN=$(( END_P - START_P ))
CONTENT_GAIN=$(( END_C - START_C ))
HEAD_SHA=$(git -C "$HOME/bible-reading-plan-bot-autopilot" rev-parse HEAD 2>/dev/null || echo unknown)
ORIGIN_SHA=$(git -C "$HOME/bible-reading-plan-bot-autopilot" rev-parse origin/main 2>/dev/null || echo unknown)
SYNC_PROOF="head=$HEAD_SHA origin=$ORIGIN_SHA"
[ "$HEAD_SHA" = "$ORIGIN_SHA" ] && SYNC_PROOF="$SYNC_PROOF MATCH" || SYNC_PROOF="$SYNC_PROOF MISMATCH"
say "════ session DONE: $ROUNDS rounds, +$CONTENT_GAIN profile fields (+$GAIN pastors; total pastors $END_P) abort=${ABORT_REASON:-none} lfs_warnings=$LFS_WARNINGS $SYNC_PROOF ════"
[ -x "$NOTIFY" ] && [ "$ROUNDS" -gt 0 ] && "$NOTIFY" --level info --title "⛏️ Directory grind session done" \
  --body "$ROUNDS rounds, +$CONTENT_GAIN profile fields (+$GAIN pastors; total pastors $END_P). Live: https://usmcmin.org/grind-report.html" >/dev/null 2>&1 || true
