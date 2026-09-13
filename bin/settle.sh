#!/bin/bash
# settle.sh "<commit message>" <batch.json ...> [extra repo files to include, e.g. bin/x.py]
#   1. ALWAYS drops the five other-lane sitemaps (blog/churches/lexicon/main/chapters) — they collide on rebase
#   2. refuses to commit unless the integrity audit prints RESULT: PASS
#   3. stages ONLY the named files + whitelisted dictionary paths (one pathspec-file add; never git add -A)
#   4. STOPs if origin has incoming DICTIONARY commits — never rebase a dict run over a dict run
#   5. add+commit in one invocation, rebase over other lanes' commits, push HEAD:main
# DRY=1 stops after showing what would be staged.
set -o pipefail
WT=$(git rev-parse --show-toplevel) || exit 1; cd "$WT" || exit 1
WL='^(docs/dictionary/|docs/lexicon/|data/dictionary|docs/sitemap|docs/dictionary-manifest|docs/assets/dictionary)'
MSG="$1"; shift
[ -n "$MSG" ] || { echo "usage: settle.sh \"<msg>\" <batch.json ...>"; exit 2; }
[ $# -ge 1 ] || { echo "no batch files named"; exit 2; }
for b in "$@"; do [ -f "$b" ] || { echo "missing: $b"; exit 2; }; done
T=/tmp/settle.$$
for sm in docs/sitemap-blog.xml docs/sitemap-churches.xml docs/sitemap-lexicon.xml docs/sitemap-main.xml docs/sitemap-chapters.xml; do
  git diff --quiet -- "$sm" 2>/dev/null && continue
  git checkout -- "$sm"; echo "DROP $sm (another lane's artifact)"
done
python3 bin/dict_integrity_audit.py > "$T.audit" 2>&1
grep -E '^RESULT:' "$T.audit"
grep -q '^RESULT: PASS' "$T.audit" || { echo "AUDIT NOT PASS — refusing to commit"; rm -f "$T".*; exit 3; }
git status --porcelain | awk '{print $2}' | grep -E "$WL" > "$T.paths" || true
for b in "$@"; do echo "$b" >> "$T.paths"; done
sort -u "$T.paths" -o "$T.paths"
git add --pathspec-from-file="$T.paths"
git diff --cached --quiet && { echo "nothing staged — refusing silent no-op"; rm -f "$T".*; exit 4; }
git diff --cached --name-only | grep -vE "$WL" | grep -vxF -f <(printf '%s\n' "$@") > "$T.bad"
if [ -s "$T.bad" ]; then echo "STAGED OUTSIDE WHITELIST — aborting:"; cat "$T.bad"; git reset -q; rm -f "$T".*; exit 5; fi
echo "staged: $(git diff --cached --name-only | wc -l | tr -d ' ') files"
if [ -n "$DRY" ]; then echo "DRY run — not committing"; git diff --cached --stat | tail -1; rm -f "$T".*; exit 0; fi
git fetch -q origin
git log --oneline HEAD..origin/main -- data/dictionary-batches docs/dictionary > "$T.inc"
if [ -s "$T.inc" ]; then echo "STOP: incoming dictionary commit(s) on origin — start over from origin/main and renumber:"; head "$T.inc"; rm -f "$T".*; exit 6; fi
git commit -q -m "$MSG" || { echo "commit failed"; rm -f "$T".*; exit 7; }
echo "committed $(git rev-parse --short HEAD): $(git show --stat --oneline HEAD | tail -1)"
git rebase -q origin/main || { echo "REBASE CONFLICT — aborting rebase, commit kept locally"; git rebase --abort; rm -f "$T".*; exit 8; }
git push -q origin HEAD:main || { echo "push failed"; rm -f "$T".*; exit 9; }
echo "PUSHED $(git rev-parse --short HEAD)  slugs=$(wc -l < data/dictionary-slugs.txt | tr -d ' ')"
rm -f "$T".*
