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
git checkout -q --detach FETCH_HEAD || die "checkout FETCH_HEAD failed"
git reset -q --hard FETCH_HEAD
git clean -qfd

mkdir -p "$WORK" && rm -f "$WORK"/*.json
node scripts/select-enrichment-batch.js --count "$BATCH" --batches 1 --out "$WORK" >>"$LOG" 2>&1 \
  || die "selector failed"
[ -s "$WORK/enrich-batch-1.json" ] || die "selector produced no batch file"

N_BATCH=$(node -e 'console.log(require("'"$WORK"'/enrich-batch-1.json").length)')
if [ "$N_BATCH" -eq 0 ]; then say "eligible pool empty — nothing to do"; exit 0; fi

python3 scripts/local-pastor-extract.py "$WORK/enrich-batch-1.json" "$WORK/enriched.json" >>"$LOG" 2>&1 \
  || die "extractor failed (is llama-server :1235 / LM Studio :1234 up?)"

FOUND=$(node -e 'console.log(require("'"$WORK"'/enriched.json").filter(x=>x.pastor_name).length)')
say "extracted: $FOUND verified lead(s) of $N_BATCH churches"

node scripts/merge-pastor-enrichments.js --input "$WORK/enriched.json" >>"$LOG" 2>&1 \
  || die "merge failed"

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
node generate-church-pages.js >>"$LOG" 2>&1 \
  || { git reset -q --hard; die "regen failed — working tree reset"; }
node scripts/check-consistency.js >>"$LOG" 2>&1 \
  || { git reset -q --hard; die "consistency check FAILED — commit aborted, tree reset"; }

if [ -n "$(git status --porcelain)" ]; then
  git add docs/data/churches.json docs/churches/ docs/data/churches-index.json docs/data/churches/ docs/data/qa-sample.json
  git commit -qm "Nightly local pastor refine: +$FOUND pastors of $N_BATCH attempted (local-extract)" \
    || die "commit failed"
  if ! git push -q origin HEAD:main; then
    say "push rejected — rebasing onto fresh origin/main and retrying"
    git fetch -q origin main && git rebase -q FETCH_HEAD && git push -q origin HEAD:main \
      || die "push failed after rebase retry — commit stranded in autopilot worktree"
  fi
  say "pushed: +$FOUND pastors ($N_BATCH attempted)"
else
  say "no changes to commit (0 applied)"
fi
say "── round done ──"
