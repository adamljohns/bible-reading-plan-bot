#!/usr/bin/env bash
# setup.sh — stand up the prayer-wall Worker. Run this once, from a terminal
# where you can complete a browser login.
#
#   cd ~/bible-reading-plan-bot/workers/prayer-wall && ./setup.sh
#
# It creates the KV namespace, prompts for the three secrets, and deploys.
# It NEVER writes a PIN to disk, to git, or to your shell history — each one is
# read from a hidden prompt and piped straight to `wrangler secret put`.
#
# Safe to re-run: creating an existing namespace is reported and skipped, and
# re-entering a secret just overwrites it.

set -uo pipefail
cd "$(dirname "$0")"

say() { printf '\n\033[1m%s\033[0m\n' "$*"; }

# --- 0. auth ---------------------------------------------------------------
if ! wrangler whoami >/dev/null 2>&1; then
  say "Not logged in to Cloudflare. Opening the browser login…"
  wrangler login || { echo "Login failed."; exit 1; }
fi
say "Authenticated as:"
wrangler whoami 2>/dev/null | tail -3

# --- 1. KV namespace -------------------------------------------------------
if grep -q 'REPLACE_WITH_KV_NAMESPACE_ID' wrangler.toml; then
  say "Creating the PRAYER KV namespace…"
  out=$(wrangler kv namespace create PRAYER 2>&1) || { echo "$out"; exit 1; }
  echo "$out"
  id=$(printf '%s' "$out" | grep -oE '[0-9a-f]{32}' | head -1)
  if [ -z "$id" ]; then
    echo "Could not read the namespace id from that output — paste it into wrangler.toml by hand."
    exit 1
  fi
  # macOS sed needs the empty -i argument.
  sed -i '' "s/REPLACE_WITH_KV_NAMESPACE_ID/$id/" wrangler.toml
  echo "wrangler.toml now points at namespace $id (an identifier, not a secret — safe to commit)."
else
  say "KV namespace already set in wrangler.toml — skipping."
fi

# --- 2. secrets ------------------------------------------------------------
put_secret() {
  local name="$1" prompt="$2" value=""
  printf '\n%s' "$prompt"
  read -rs value
  printf '\n'
  if [ -z "$value" ]; then
    echo "  (blank — skipped, existing value left alone)"
    return
  fi
  printf '%s' "$value" | wrangler secret put "$name" >/dev/null 2>&1 \
    && echo "  $name set." \
    || echo "  $name FAILED to set."
  unset value
}

say "Secrets (input is hidden; nothing is echoed or saved)"
put_secret WALL_PIN       "Group PIN the men will use: "
put_secret MOD_PIN        "Your moderator PIN (must differ from the group PIN): "

printf '\nSession signing secret — press Enter to generate one for you: '
read -rs sess; printf '\n'
[ -z "$sess" ] && sess=$(openssl rand -hex 32) && echo "  generated."
printf '%s' "$sess" | wrangler secret put SESSION_SECRET >/dev/null 2>&1 \
  && echo "  SESSION_SECRET set." || echo "  SESSION_SECRET FAILED."
unset sess

# --- 3. deploy -------------------------------------------------------------
say "Deploying…"
wrangler deploy || { echo "Deploy failed."; exit 1; }

# --- 4. prove it -----------------------------------------------------------
say "Checking the live endpoint (expect 401 Locked, NOT 503 not-configured)"
code=$(curl -s -o /tmp/pw-check.json -w '%{http_code}' https://usmcmin.org/api/prayer/session)
echo "  GET /api/prayer/session -> HTTP $code"
case "$code" in
  401) echo "  Correct: the wall is live and locked. Open https://usmcmin.org/prayer/wall.html and sign in." ;;
  503) echo "  The Worker is up but a secret is missing — re-run and set all three." ;;
  404) echo "  Route not attached. Check the routes block in wrangler.toml against your zone." ;;
  *)   echo "  Unexpected. Body:"; cat /tmp/pw-check.json ;;
esac
rm -f /tmp/pw-check.json
