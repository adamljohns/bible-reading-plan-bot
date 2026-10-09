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
MAX_ROUNDS="${GRIND_MAX_ROUNDS:-0}"
case "$MAX_ROUNDS" in ''|*[!0-9]*) MAX_ROUNDS=0 ;; esac
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
RUN_LOG="$HOME/Library/Logs/pastor-refine-local.log"
RUNNER="$HOME/bible-reading-plan-bot-autopilot/scripts/pastor-refine-local.sh"
SUMMARY="$HOME/bible-reading-plan-bot-autopilot/scripts/summarize-grind-session.js"
NOTIFY="$HOME/.hermes/bin/notify-adam.sh"
say() { echo "[$(date '+%F %T')] $*" >>"$LOG"; }
RUN_LOG_START=$(wc -l <"$RUN_LOG" 2>/dev/null || echo 0)
case "$RUN_LOG_START" in ''|*[!0-9]*) RUN_LOG_START=0 ;; esac
CONTENT_GAIN=0; GAIN=0; SOCIAL_GAIN=0; FRONTIER_GAIN=0; OTHER_GAIN=0
ATTEMPTED=0; PRODUCTIVE_ROUNDS=0; ZERO_ROUNDS=0; OP_CHECKPOINTS=0

# One deploy for the whole session. The rounds already pushed their content
# with [skip ci]; this empty commit is the trigger. Idempotent: it no-ops when
# no round landed anything, and runs from the trap so a killed session still
# publishes. Uses git, not `gh` — gh reads its token from the Keychain, which
# is exactly the thing that does not work from launchd.
DEPLOY_FIRED=0
publish_session_output() {
  [ "${CONTENT_GAIN:-0}" -gt 0 ] || {
    say "no validated content landed — no deploy and no completion notice"
    return 0
  }
  [ "$DEPLOY_FIRED" = "1" ] && return 0
  DEPLOY_FIRED=1
  local wt="$HOME/bible-reading-plan-bot-autopilot"

  # Dirty canonical docs mean a round failed to checkpoint its state. Do not
  # hide that defect behind an empty deploy commit or a false DONE notice.
  if ! git -C "$wt" diff --quiet -- docs 2>/dev/null; then
    say "ALERT: deploy withheld — autopilot docs hold uncommitted state"
    return 1
  fi

  # Build the deploy trigger directly on the current origin/main tree. This
  # avoids coupling publication to the detached autopilot HEAD and survives
  # unrelated writers landing between the final grind round and session close.
  local parent tree deploy_sha attempt
  for attempt in 1 2 3; do
    git -C "$wt" fetch -q origin main || {
      say "ALERT: deploy trigger fetch failed — validated output is pushed but NOT verified live"
      return 1
    }
    parent=$(git -C "$wt" rev-parse origin/main) || return 1
    tree=$(git -C "$wt" rev-parse "${parent}^{tree}") || return 1
    deploy_sha=$(printf 'deploy: publish grind session output (%s productive rounds, %s fields)\n' \
      "$PRODUCTIVE_ROUNDS" "$CONTENT_GAIN" | git -C "$wt" commit-tree "$tree" -p "$parent") || {
      say "ALERT: deploy trigger commit failed"
      return 1
    }
    if git -C "$wt" push -q origin "$deploy_sha:main"; then
      say "deploy fired: sha=$deploy_sha productive_rounds=$PRODUCTIVE_ROUNDS content_fields=$CONTENT_GAIN"
      break
    fi
    deploy_sha=""
    say "deploy trigger raced another writer — retry $attempt/3"
  done
  [ -n "$deploy_sha" ] || {
    say "ALERT: deploy trigger push failed after 3 races — validated output is pushed but NOT verified live"
    return 1
  }

  # Pushing is not publishing. Notify only after the exact trigger commit and
  # cache-busted public endpoints verify. A failed or zero-yield session remains
  # silent; its log/dashboard carry the diagnostic instead of a false receipt.
  local verifier="$HOME/Scripts/guards/publish-verify.sh"
  if [ -x "$verifier" ] && "$verifier" --lane "directory grind ($PRODUCTIVE_ROUNDS productive rounds)" \
      --repo adamljohns/bible-reading-plan-bot \
      --sha "$deploy_sha" \
      --url https://usmcmin.org/grind-report.html \
      --url https://usmcmin.org/data/grind-stats.json \
      --expect "$(date -u +%F)T" \
      --timeout 1200; then
    say "publish verified live: sha=$deploy_sha content_fields=$CONTENT_GAIN"
    [ -x "$NOTIFY" ] && "$NOTIFY" --level info --title "Directory grind — verified live result" \
      --body "$PRODUCTIVE_ROUNDS productive rounds; $CONTENT_GAIN validated fields live from $ATTEMPTED records: $GAIN pastors, $SOCIAL_GAIN socials, $FRONTIER_GAIN source-recovery contact/map fields, $OTHER_GAIN other profile fields. https://usmcmin.org/grind-report.html" >/dev/null 2>&1 || true
  else
    say "ALERT: publish NOT verified live — no completion notice sent"
    return 1
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
round_was_zero_yield() {
  tail -40 "$RUN_LOG" 2>/dev/null \
    | grep -q "zero content applied — persist operational state and advance the selector"
}

say "════ ${DURATION_H}h session START (batch $PASTOR_REFINE_BATCH, ${COOLDOWN}s cooldown, start pastors=$START_P, runner_log_line=$RUN_LOG_START) ════"
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
      say "zero-content checkpoint round (consecutive=$ZERO_STREAK); selector state persisted, continuing"
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
  [ "$MAX_ROUNDS" -gt 0 ] && [ "$ROUNDS" -ge "$MAX_ROUNDS" ] && { say "bounded verification cap reached ($MAX_ROUNDS rounds)"; break; }
  [ "$(date +%s)" -ge "$DEADLINE" ] && break
  say "cooldown ${COOLDOWN}s…"
  sleep "$COOLDOWN"
done

END_P=$(node -e '
try{const d=JSON.parse(require("fs").readFileSync(process.env.HOME+"/bible-reading-plan-bot-autopilot/docs/data/churches.json","utf8")).churches;
const ph=p=>{const s=String(p||"").trim();return !s||/^(pastors?|tbd|n\/?a|none|unknown|various|staff)\.?$/i.test(s)||/verify|see website|coming soon|^unknown/i.test(s)};
console.log(d.filter(c=>!ph(c.pastor)).length)}catch(e){console.log(0)}' 2>/dev/null || echo 0)
if [ -x "$SUMMARY" ]; then
  SUMMARY_JSON=$(node "$SUMMARY" --log "$RUN_LOG" --after-line "$RUN_LOG_START" 2>>"$LOG" || echo '{}')
else
  SUMMARY_JSON='{}'
  say "summary helper missing — refusing to infer session yield from snapshots"
fi
SUMMARY_TSV=$(node -e '
let j={};try{j=JSON.parse(process.argv[1])}catch(_){}
const n=k=>Number(j[k]||0);console.log([n("attempted"),n("content_applied"),n("pastors_applied"),n("socials_applied"),n("frontier_applied"),n("other_profile_applied"),n("productive_rounds"),n("zero_content_rounds"),n("operational_checkpoints")].join("\t"));' "$SUMMARY_JSON")
IFS=$'\t' read -r ATTEMPTED CONTENT_GAIN GAIN SOCIAL_GAIN FRONTIER_GAIN OTHER_GAIN PRODUCTIVE_ROUNDS ZERO_ROUNDS OP_CHECKPOINTS <<<"$SUMMARY_TSV"
HEAD_SHA=$(git -C "$HOME/bible-reading-plan-bot-autopilot" rev-parse HEAD 2>/dev/null || echo unknown)
ORIGIN_SHA=$(git -C "$HOME/bible-reading-plan-bot-autopilot" rev-parse origin/main 2>/dev/null || echo unknown)
SYNC_PROOF="head=$HEAD_SHA origin=$ORIGIN_SHA"
[ "$HEAD_SHA" = "$ORIGIN_SHA" ] && SYNC_PROOF="$SYNC_PROOF MATCH" || SYNC_PROOF="$SYNC_PROOF MISMATCH"
say "════ session RESULT: rounds=$ROUNDS productive=$PRODUCTIVE_ROUNDS zero=$ZERO_ROUNDS checkpoints=$OP_CHECKPOINTS attempted=$ATTEMPTED validated_fields=$CONTENT_GAIN pastors=$GAIN socials=$SOCIAL_GAIN frontier_fields=$FRONTIER_GAIN other_profile=$OTHER_GAIN total_pastors=$END_P abort=${ABORT_REASON:-none} lfs_warnings=$LFS_WARNINGS $SYNC_PROOF; live verification pending ════"
