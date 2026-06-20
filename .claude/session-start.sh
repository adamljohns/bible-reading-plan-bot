#!/usr/bin/env bash
# SessionStart preflight for bible-reading-plan-bot — fast, non-blocking, ALWAYS exits 0.
# Reports toolchain + one critical rule. Never scans the (large) data files or gates.
cd "${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}" 2>/dev/null || true

echo "🔧 bible-reading-plan-bot preflight (MOOP Church Directory → usmcmin.org)"

if command -v node >/dev/null 2>&1; then
  echo "  ✓ node $(node --version 2>&1) / npm $(npm --version 2>/dev/null)"
  [ -d node_modules ] && echo "  ✓ node_modules present" || echo "  ⚠ node_modules missing — run: npm install"
else
  echo "  ⚠ node not found — install: brew install node"
fi
if command -v python3 >/dev/null 2>&1; then
  echo "  ✓ $(python3 --version 2>&1) (aux scripts: pip3 install -r requirements.txt)"
else
  echo "  ⚠ python3 not found — needed for shard/sitemap scripts"
fi

echo "  ! churches.json has a ~20-min autopilot — 'git pull --rebase origin main' before push;"
echo "    never hand-edit docs/churches/*.html (regenerate). Full schema rules: CLAUDE.md."

exit 0
