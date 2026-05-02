#!/usr/bin/env bash
# Regenerate church HTML pages, then commit + pull-rebase + push.
#
# Usage:
#   regen-and-commit.sh "<commit title>" "<commit body>"
#
# Example:
#   regen-and-commit.sh "Round 4: LCMS Midwest +49" "$(cat <<'EOF'
#   State distribution: IN 8, OH 7, WI 6, MN 5, IA 6, NE 6, MO 5, KS 6.
#
#   Notable heritage adds: Trinity Soulard St. Louis (1839 LCMS mother church),
#   Trinity Freistadt Mequon WI (12/31/1839 founding congregation).
#
#   Total: 4715 -> 4764 (+49).
#   EOF
#   )"
#
# Behavior:
# - Runs node generate-church-pages.js
# - Reports any orphan HTML for IDs no longer in churches.json (does NOT auto-delete)
# - git add -A docs/
# - Builds the commit message via heredoc with single-quoted EOF (avoids shell-escape gotchas)
# - Appends the standard Co-Authored-By trailer
# - git pull --rebase origin main (handles cross-thread coordination)
# - git push origin main
#
# Exits non-zero if any step fails. Safe to re-run after fixing issues.

set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: regen-and-commit.sh \"<title>\" \"<body>\"" >&2
  exit 2
fi

TITLE="$1"
BODY="$2"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
cd "$REPO_ROOT"

echo "=== Regenerating church HTML pages ==="
node generate-church-pages.js | tail -5

echo
echo "=== Orphan HTML check (in docs/churches/ but not in churches.json) ==="
EXISTING_IDS="$(jq -r '.churches[].id' docs/data/churches.json | sort -u)"
ORPHANS=()
while IFS= read -r html_file; do
  slug="$(basename "$html_file" .html)"
  if [[ "$slug" == "index" ]]; then continue; fi
  if ! echo "$EXISTING_IDS" | grep -qFx "$slug"; then
    ORPHANS+=("docs/churches/$slug.html")
  fi
done < <(find docs/churches -maxdepth 1 -name '*.html' -type f)

if [[ ${#ORPHANS[@]} -gt 0 ]]; then
  echo "Found ${#ORPHANS[@]} orphan HTML file(s) — review and delete manually if appropriate:"
  printf '  %s\n' "${ORPHANS[@]}"
  echo "(Not auto-deleted — orphans may be from intentional deletes that need a verification trail in the commit body.)"
else
  echo "No orphans."
fi

echo
echo "=== Staging and committing ==="
git add -A docs/

if git diff --cached --quiet; then
  echo "Nothing staged. Skipping commit + push."
  exit 0
fi

COMMIT_MSG="$(printf '%s\n\n%s\n\nCo-Authored-By: Claude <noreply@anthropic.com>' "$TITLE" "$BODY")"
git commit -m "$COMMIT_MSG"

echo
echo "=== Pull-rebase (cross-thread coordination) ==="
git pull --rebase origin main

echo
echo "=== Pushing to origin/main ==="
git push origin main

echo
echo "Done. Latest commit:"
git log --oneline -1
