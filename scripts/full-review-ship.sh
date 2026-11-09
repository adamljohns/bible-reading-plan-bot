#!/bin/bash
# full-review-ship.sh — path-scoped commit + push for an APPLIED full-review round.
#
# Called only by apply-full-review-patch.js --apply --ship (Adam's GO). Follows
# DEPLOY-DOCTRINE.md: never from ~/bible-reading-plan-bot (fleet scratch); only
# from the autopilot worktree the grind already ships from (or an explicit
# FULL_REVIEW_SHIP_TREE that is level with origin/main); only the directory
# paths below are staged — never `git add -A`. The rebase/salvage logic is the
# same as pastor-refine-local.sh's land_head_on_main (generated-index conflicts
# are rebuilt from canonical churches.json; anything else aborts cleanly).
set -u
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
MSG="${1:-Directory full review}"
ROOT="$(cd "$(dirname "$0")/.." && pwd -P)"
ALLOWED="${FULL_REVIEW_SHIP_TREE:-$HOME/bible-reading-plan-bot-autopilot}"
cd "$ROOT" || exit 1

if [ "$ROOT" = "$(cd "$HOME/bible-reading-plan-bot" 2>/dev/null && pwd -P)" ]; then
  echo "REFUSED: ~/bible-reading-plan-bot is fleet scratch (DEPLOY-DOCTRINE rule 2)."; exit 1
fi
if [ "$ROOT" != "$(cd "$ALLOWED" 2>/dev/null && pwd -P)" ]; then
  echo "REFUSED: ship tree is $ALLOWED, not $ROOT. Apply the round there (or set FULL_REVIEW_SHIP_TREE)."; exit 1
fi

PATHS=(docs/data/churches.json docs/churches docs/data/churches-index.json docs/data/churches-index-slim.json
       docs/data/churches docs/sitemap-churches.xml data/full-review docs/data/full-review-stats.json)

land_head_on_main() {
  git fetch -q origin main || return 1
  git diff --quiet || git restore --worktree --source=HEAD -- docs/data/churches-index-slim.json || true
  git diff --quiet || { echo "unstaged changes block rebase"; return 1; }
  if ! git rebase -q FETCH_HEAD; then
    UNMERGED=$(git diff --name-only --diff-filter=U)
    BAD=$(printf '%s\n' "$UNMERGED" | grep -Ev '^(docs/data/churches-index(-slim)?\.json|docs/data/churches/(by-state|by-denomination-family|detail)/.+)$' || true)
    if [ -n "$UNMERGED" ] && [ -z "$BAD" ]; then
      python3 scripts/build_state_shards.py && python3 scripts/build_denomination_shards.py && node scripts/build-church-index.js \
        || { git rebase --abort >/dev/null 2>&1; return 1; }
      git add -A docs/data/churches-index.json docs/data/churches-index-slim.json docs/data/churches/by-state docs/data/churches/by-denomination-family docs/data/churches/detail
      GIT_EDITOR=true git rebase --continue || { git rebase --abort >/dev/null 2>&1; return 1; }
    else
      git rebase --abort >/dev/null 2>&1; echo "non-generated rebase conflict; aborted cleanly"; return 1
    fi
  fi
  git push -q origin HEAD:main
}

for p in "${PATHS[@]}"; do [ -e "$p" ] && git add -- "$p"; done
git diff --cached --quiet && { echo "nothing staged — no ship"; exit 0; }
git commit -qm "$MSG" || exit 1
git push -q origin HEAD:main || land_head_on_main || { echo "push failed after rebase retry — commit kept locally for salvage"; exit 1; }
echo "shipped: $(git rev-parse --short HEAD). Not live until the served URL returns 200 (DEPLOY-DOCTRINE rule 1)."
