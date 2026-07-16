#!/bin/bash
# pastor-refine-local.sh — nightly ZERO-CLOUD-USAGE pastor enrichment round.
#
# select batch -> fetch church sites -> LOCAL LLM extracts pastors (validated
# mechanically; see local-pastor-extract.py) -> merge (guarded) -> regen
# (write-if-changed, so no churn) -> consistency check -> commit -> push.
#
# Runs in its own DETACHED worktree (~/bible-reading-plan-bot-autopilot) so it
# can never collide with interactive sessions or the fleet checkout. Installed
# as launchd job com.moop.pastor-refine-local (03:07 daily); alerts Adam's
# Telegram via notify-adam.sh on failure, stays silent on success.
#
# Manual run:  PASTOR_REFINE_BATCH=5 bash scripts/pastor-refine-local.sh
set -u
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

WT="$HOME/bible-reading-plan-bot-autopilot"
LOG="$HOME/Library/Logs/pastor-refine-local.log"
LOCK="/tmp/pastor-refine-local.lock"
BATCH="${PASTOR_REFINE_BATCH:-25}"
WORK="/tmp/prl"
NOTIFY="$HOME/.hermes/bin/notify-adam.sh"

say()   { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }
alert() { say "ALERT: $*"; [ -x "$NOTIFY" ] && "$NOTIFY" --level warning --title "pastor-refine-local" --body "$*" >/dev/null 2>&1; }
die()   { alert "$1"; exit 1; }

mkdir "$LOCK" 2>/dev/null || { say "lock held — another run in progress, exiting"; exit 0; }
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

[ -d "$WT" ] || die "autopilot worktree missing at $WT (git worktree add --detach $WT origin/main)"
cd "$WT" || die "cd $WT failed"

say "── round start (batch=$BATCH) ──"
git fetch -q origin main            || die "git fetch failed"
# reset --hard moves the detached HEAD to FETCH_HEAD AND overwrites local dirt in one
# unstoppable step. (A plain `checkout --detach` REFUSES a dirty tree — leftover dirt
# from one died round deadlocked EVERY later round 07-12→07-15: 16 sessions, 32
# "checkout FETCH_HEAD failed", four days of zero work.)
git reset -q --hard FETCH_HEAD      || die "reset to FETCH_HEAD failed"
git clean -qfd

mkdir -p "$WORK" && rm -f "$WORK"/*.json "$WORK"/selector.txt
# Fresh pool first; when it runs dry, automatically fall back to the RETRY pool
# (one-strike "no parseable pastor" churches — the extractor's link-discovery
# often finds the staff page the fixed paths missed). Both dry => grind complete.
MODE="fresh"
node scripts/select-enrichment-batch.js --count "$BATCH" --batches 1 --out "$WORK" >"$WORK/selector.txt" 2>&1 \
  || die "selector failed"
cat "$WORK/selector.txt" >>"$LOG"
N_BATCH=$(node -e 'console.log(require("'"$WORK"'/enrich-batch-1.json").length)' 2>/dev/null || echo 0)
POOL=$(grep -oE 'pastor-fetchable\): [0-9]+' "$WORK/selector.txt" | grep -oE '[0-9]+$' | head -1)
# MIN_FRESH floor (2026-07-11): don't burn a full round (fetch + regen + push) on a
# sub-threshold fresh trickle while thousands sit in retry/social — a 1-church fresh
# pool once spun the grind for 5 days. A skipped trickle is swept later: discovery
# refills fresh past the floor, or the final fallback below processes it when the
# deeper pools are dry.
MIN_FRESH="${MIN_FRESH:-10}"
N_FRESH_TRICKLE=0
# Cold-retry escalation (2026-07-16): the retry pool's tail is mostly dead sites —
# 25 of today's 44 rounds applied literally nothing while 6k+ guaranteed-yield
# social-fill churches waited. After RETRY_COLD_AFTER consecutive zero-yield retry
# rounds (counter kept in /tmp, reset by any yield), rounds jump to the SOCIAL tier
# first; retry still runs when social is dry, and the streak resets so it gets a
# fresh shot after social exhausts.
STREAK_FILE="/tmp/prl-retry-zero-streak"
RETRY_COLD_AFTER="${RETRY_COLD_AFTER:-3}"
RETRY_STREAK=$(cat "$STREAK_FILE" 2>/dev/null || echo 0)
case "$RETRY_STREAK" in ''|*[!0-9]*) RETRY_STREAK=0 ;; esac
if [ "$N_BATCH" -eq 0 ] || { [ -n "$POOL" ] && [ "$POOL" -lt "$MIN_FRESH" ]; }; then
  N_FRESH_TRICKLE=$N_BATCH
  [ "$N_BATCH" -gt 0 ] && say "fresh pool ($POOL) below floor ($MIN_FRESH) — deferring trickle"
  if [ "$RETRY_STREAK" -ge "$RETRY_COLD_AFTER" ]; then
    say "retry pool is cold ($RETRY_STREAK consecutive zero-yield rounds) — trying SOCIAL tier first"
    MODE="social"; SOCIAL_FLAG="--social"
    node scripts/select-enrichment-batch.js --social --count "$BATCH" --batches 1 --out "$WORK" >"$WORK/selector.txt" 2>&1 \
      || die "selector failed (social-first mode)"
    cat "$WORK/selector.txt" >>"$LOG"
    N_BATCH=$(node -e 'console.log(require("'"$WORK"'/enrich-batch-1.json").length)' 2>/dev/null || echo 0)
    if [ "$N_BATCH" -eq 0 ]; then
      say "social pool dry — returning to retry with a fresh streak"
      rm -f "$STREAK_FILE"; RETRY_STREAK=0
    fi
  fi
  if [ "$N_BATCH" -eq 0 ]; then
    MODE="retry"; SOCIAL_FLAG=""
    node scripts/select-enrichment-batch.js --retry --count "$BATCH" --batches 1 --out "$WORK" >"$WORK/selector.txt" 2>&1 \
      || die "selector failed (retry mode)"
    cat "$WORK/selector.txt" >>"$LOG"
    N_BATCH=$(node -e 'console.log(require("'"$WORK"'/enrich-batch-1.json").length)' 2>/dev/null || echo 0)
  fi
fi
# Third tier: SOCIAL-fill (churches with a website but no social link). Keeps the
# local sessions productive for a week after the pastor pools dry.
SOCIAL_FLAG=""
if [ "$N_BATCH" -eq 0 ]; then
  MODE="social"; SOCIAL_FLAG="--social"
  node scripts/select-enrichment-batch.js --social --count "$BATCH" --batches 1 --out "$WORK" >"$WORK/selector.txt" 2>&1 \
    || die "selector failed (social mode)"
  cat "$WORK/selector.txt" >>"$LOG"
  N_BATCH=$(node -e 'console.log(require("'"$WORK"'/enrich-batch-1.json").length)' 2>/dev/null || echo 0)
fi
# Final fallback: retry+social dry but a fresh trickle was deferred — process it now
# rather than declaring the grind complete with real work left.
if [ "$N_BATCH" -eq 0 ] && [ "$N_FRESH_TRICKLE" -gt 0 ]; then
  MODE="fresh"; SOCIAL_FLAG=""
  node scripts/select-enrichment-batch.js --count "$BATCH" --batches 1 --out "$WORK" >"$WORK/selector.txt" 2>&1 \
    || die "selector failed (fresh-trickle mode)"
  cat "$WORK/selector.txt" >>"$LOG"
  N_BATCH=$(node -e 'console.log(require("'"$WORK"'/enrich-batch-1.json").length)' 2>/dev/null || echo 0)
fi
if [ "$N_BATCH" -eq 0 ]; then say "fresh, retry AND social pools all empty — grind complete, nothing to do"; exit 0; fi
POOL=$(grep -oE 'pastor-fetchable\): [0-9]+' "$WORK/selector.txt" | grep -oE '[0-9]+$' | head -1)
say "mode=$MODE pool=${POOL:-?} batch=$N_BATCH"

python3 scripts/local-pastor-extract.py "$WORK/enrich-batch-1.json" "$WORK/enriched.json" >>"$LOG" 2>&1 \
  || die "extractor failed (is llama-server :1235 / LM Studio :1234 up?)"

FOUND=$(node -e 'console.log(require("'"$WORK"'/enriched.json").filter(x=>x.pastor_name).length)')
say "extracted: $FOUND verified lead(s) of $N_BATCH churches"

node scripts/merge-pastor-enrichments.js --input "$WORK/enriched.json" $SOCIAL_FLAG >"$WORK/merge.txt" 2>&1 \
  || { cat "$WORK/merge.txt" >>"$LOG"; die "merge failed"; }
cat "$WORK/merge.txt" >>"$LOG"
# Honest counts for the commit message: what the guards actually APPLIED, not what
# the extractor merely found (found-but-HELD names used to be reported as "+1 pastors").
APPLIED=$(grep -oE 'Pastors applied: +[0-9]+' "$WORK/merge.txt" | grep -oE '[0-9]+$' | head -1); APPLIED=${APPLIED:-0}
SOC_APPLIED=$(grep -oE 'Social links applied: +[0-9]+' "$WORK/merge.txt" | grep -oE '[0-9]+$' | head -1); SOC_APPLIED=${SOC_APPLIED:-0}
# Track the cold-retry streak (see escalation above): zero-yield retry rounds
# increment it; any retry yield resets it.
if [ "$MODE" = "retry" ]; then
  if [ "$APPLIED" -eq 0 ] && [ "$SOC_APPLIED" -eq 0 ]; then
    echo $((RETRY_STREAK + 1)) > "$STREAK_FILE"
  else
    echo 0 > "$STREAK_FILE"
  fi
fi

# Publish a QA sample for the fleet: the newest local-extract finds land at
# https://usmcmin.org/data/qa-sample.json so Chaps (web_fetch-only tooling) can
# audit them on his recurring QA cron — verify pastor_name appears at
# pastor_source_url AND on the directory page — and report discrepancies to Adam.
node -e '
const fs=require("fs");
const found=require("'"$WORK"'/enriched.json").filter(x=>x.pastor_name).map(x=>({
  id:x.id, pastor_name:x.pastor_name, pastor_role:x.pastor_role||null,
  pastor_source_url:x.pastor_source_url,
  page_url:"https://usmcmin.org/churches/"+x.id+".html",
  extracted_at:new Date().toISOString().slice(0,10), extractor:x.extractor||"local"}));
const P="docs/data/qa-sample.json";
let prev=[]; try{prev=JSON.parse(fs.readFileSync(P,"utf8")).sample||[]}catch(_){}
const merged=[...found,...prev.filter(p=>!found.some(f=>f.id===p.id))].slice(0,40);
fs.writeFileSync(P,JSON.stringify({updated:new Date().toISOString().slice(0,10),note:"Most recent local-LLM pastor extractions — QA audit sample for fleet verification (Chaps recurring cron): verify pastor_name appears at pastor_source_url AND on page_url.",sample:merged},null,1));
' >>"$LOG" 2>&1 || say "qa-sample update failed (non-fatal)"

# Append a row to the grind time-series (docs/data/grind-stats.json) — the fuel
# for the live before/after dashboard at usmcmin.org/grind-report.html. Records the
# TOTAL remaining enrichment work (fresh+retry+social) + US coverage, not just the
# current tier (so the dashboard never falsely shows "0 remaining").
node scripts/append-grind-stats.js --mode "$MODE" --attempted "$N_BATCH" --found "$FOUND" \
  >>"$LOG" 2>&1 || say "grind-stats update failed (non-fatal)"
node generate-church-pages.js >>"$LOG" 2>&1 \
  || { git reset -q --hard; die "regen failed — working tree reset"; }
if ! node scripts/check-consistency.js >>"$LOG" 2>&1; then
  # Self-heal (2026-07-11): sibling sessions sometimes push church ADDITIONS without
  # the non-regen derived artifacts (sitemap-churches.xml; the total_churches field) —
  # that PRE-EXISTING drift then failed this check twice and killed the whole 4h
  # session (15:07 today died on "sitemap missing 104" from a wave pushed at 14:11,
  # discarding two rounds of good enrichment). Both drifts are purely mechanical, so
  # repair them once and re-check; anything else still dies loudly like before.
  say "consistency FAILED — attempting mechanical self-heal (total_churches + sitemap + index)"
  node -e '
    const { makeWriter } = require("./scripts/lib/format-preserving-write.js");
    const { data, write } = makeWriter("docs/data/churches.json");
    if (data.total_churches !== data.churches.length) {
      data.total_churches = data.churches.length; write(data);
      console.log("self-heal: total_churches ->", data.churches.length);
    }' >>"$LOG" 2>&1
  node scripts/build-sitemap-churches.js >>"$LOG" 2>&1
  node scripts/build-church-index.js >>"$LOG" 2>&1
  node scripts/check-consistency.js >>"$LOG" 2>&1 \
    || { git reset -q --hard; die "consistency check FAILED even after self-heal — commit aborted, tree reset"; }
  say "self-heal OK — consistency GREEN"
fi

if [ -n "$(git status --porcelain)" ]; then
  git add docs/data/churches.json docs/churches/ docs/data/churches-index.json docs/data/churches/ docs/data/qa-sample.json docs/data/grind-stats.json docs/sitemap-churches.xml
  git commit -qm "Local pastor refine: +$APPLIED pastors, +$SOC_APPLIED socials applied of $N_BATCH attempted ($MODE pool, local-extract)" \
    || die "commit failed"
  if ! git push -q origin HEAD:main; then
    say "push rejected — rebasing onto fresh origin/main and retrying"
    git fetch -q origin main && git rebase -q FETCH_HEAD && git push -q origin HEAD:main \
      || die "push failed after rebase retry — commit stranded in autopilot worktree"
  fi
  say "pushed: +$APPLIED pastors, +$SOC_APPLIED socials applied ($N_BATCH attempted, $FOUND extracted)"
else
  say "no changes to commit (0 applied)"
fi
say "── round done ──"
