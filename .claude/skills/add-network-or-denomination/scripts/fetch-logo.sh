#!/bin/bash
# fetch-logo.sh — download a network's logo to docs/assets/icons/networks/<slug>.png.
# Tries apple-touch-icon first (highest quality), falls back to Google's favicon
# service at 128px. Validates the result is a real PNG, not an HTML 404 in disguise.
#
# Usage:
#   bash fetch-logo.sh <slug> <domain>
#   bash fetch-logo.sh opc opc.org

set -u
cd "$(dirname "$0")/../../../.." || { echo "repo root not found"; exit 1; }

SLUG="${1:-}"
DOMAIN="${2:-}"
if [ -z "$SLUG" ] || [ -z "$DOMAIN" ]; then
  echo "Usage: $0 <slug> <domain>"
  echo "Example: $0 opc opc.org"
  exit 1
fi

OUT="docs/assets/icons/networks/${SLUG}.png"
mkdir -p "$(dirname "$OUT")"
rm -f "$OUT"

UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'

is_png() {
  [ -s "$1" ] && file -b "$1" | grep -qi '^PNG image data'
}

# Attempt 1: /apple-touch-icon.png
echo "[1/3] Trying https://${DOMAIN}/apple-touch-icon.png ..."
curl -sfLo "$OUT" --max-time 15 -A "$UA" "https://${DOMAIN}/apple-touch-icon.png" 2>/dev/null || true
if is_png "$OUT"; then
  echo "  -> OK ($(file -b "$OUT"))"
  echo "$OUT"
  exit 0
fi
rm -f "$OUT"

# Attempt 2: /apple-touch-icon-precomposed.png
echo "[2/3] Trying https://${DOMAIN}/apple-touch-icon-precomposed.png ..."
curl -sfLo "$OUT" --max-time 15 -A "$UA" "https://${DOMAIN}/apple-touch-icon-precomposed.png" 2>/dev/null || true
if is_png "$OUT"; then
  echo "  -> OK ($(file -b "$OUT"))"
  echo "$OUT"
  exit 0
fi
rm -f "$OUT"

# Attempt 3: Google favicon service (128x128)
echo "[3/3] Falling back to Google favicon service at 128x128 ..."
curl -sfLo "$OUT" --max-time 15 -A "$UA" "https://www.google.com/s2/favicons?domain=${DOMAIN}&sz=128" 2>/dev/null || true
if is_png "$OUT"; then
  echo "  -> OK ($(file -b "$OUT"))"
  echo "$OUT"
  exit 0
fi
rm -f "$OUT"

echo "FAIL: none of the three logo sources returned a valid PNG for ${DOMAIN}."
echo "Try manually:"
echo "  curl -sL https://${DOMAIN}/ | grep -iE 'apple-touch-icon|og:image' | head -5"
echo "then fetch the resolved URL by hand."
exit 1
