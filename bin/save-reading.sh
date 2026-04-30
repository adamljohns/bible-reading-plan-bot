#!/usr/bin/env bash
# save-reading.sh — append a generated reading to today's docs/readings file
# and commit/push to origin/main. Used by the daily SDG-4 reading crons so
# the cron prompt no longer carries shell-substitution literals.
#
# Usage:    cat reading.md | ~/bible-reading-plan-bot/bin/save-reading.sh "Morning Wisdom"
# Reads:    full reading content from stdin (markdown).
# Writes:   docs/readings/YYYY-MM-DD.md (appends if file exists, with a blank
#           line separator between watches).
# Side fx:  pull --rebase, git add, commit, push origin main.

set -euo pipefail

LABEL="${1:-Daily Reading}"
REPO="${HOME}/bible-reading-plan-bot"
TODAY="$(date +%Y-%m-%d)"
FILE="${REPO}/docs/readings/${TODAY}.md"

mkdir -p "$(dirname "${FILE}")"

if [ -s "${FILE}" ]; then
  printf '\n\n' >> "${FILE}"
fi
cat >> "${FILE}"

cd "${REPO}"
git pull --rebase --quiet origin main || true
git add "docs/readings/${TODAY}.md"

if git diff --cached --quiet; then
  echo "save-reading: nothing new staged for ${TODAY}; no commit." >&2
  exit 0
fi

git commit --quiet -m "Daily reading: ${TODAY} (${LABEL})"
git push --quiet origin main
echo "save-reading: pushed ${FILE} (${LABEL})"
