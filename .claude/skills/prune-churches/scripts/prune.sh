#!/usr/bin/env bash
# prune.sh -- remove phantom/duplicate church record(s) across every artifact, end-to-end.
# Edits only; reviews, commit, and push stay manual (see SKILL.md). Pass --dry-run to preview.
# Usage: bash .claude/skills/prune-churches/scripts/prune.sh [--dry-run] <church-id> [<church-id> ...]
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$DIR/../../../.." && pwd)"   # .claude/skills/prune-churches/scripts -> repo root
[ "$#" -ge 1 ] || { echo "usage: prune.sh [--dry-run] <church-id> [<church-id> ...]"; exit 2; }

case " $* " in *" --dry-run "*) DRY=1;; *) DRY=0;; esac

echo "== 1. churches.json (source of truth) =="
node "$DIR/prune-churches.js" "$@"
echo "== 2. derived artifacts (shards + sitemap) =="
python3 "$DIR/prune-derived.py" "$@"

echo "== 3. orphan per-church HTML =="
for id in "$@"; do
  [ "$id" = "--dry-run" ] && continue
  f="$ROOT/docs/churches/$id.html"
  if [ -f "$f" ]; then
    if [ "$DRY" = "1" ]; then echo "  [dry-run] would rm docs/churches/$id.html"; else rm -f "$f"; echo "  removed docs/churches/$id.html"; fi
  else echo "  (no page for $id)"; fi
done

echo ""
echo "Next (manual — review FIRST; an autopilot commits churches.json every ~20 min):"
echo "  git diff --numstat -- docs/        # expect a SMALL scoped diff (records + count fields)"
echo "  git add <the TOUCHED files above + the removed HTML>   # NOT 'git add -A docs/' (autopilot churn)"
echo "  git commit                          # for deletions, include the verification trail (see SKILL.md)"
echo "  git pull --rebase origin main && git push origin main"
echo "  git merge-base --is-ancestor HEAD origin/main && echo '✓ durable on origin'"
