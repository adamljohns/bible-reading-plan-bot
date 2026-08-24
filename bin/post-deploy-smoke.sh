#!/usr/bin/env bash
# Post-deploy smoke gate — curl canonical live URLs; optional Telegram alert on fail.
set -euo pipefail

SITE="${1:-org}"
FAIL=0
FAILED=()

check_url() {
  local url="$1"
  local code
  code="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 25 -L "$url" || echo "000")"
  if [[ "$code" =~ ^2 ]]; then
    echo "OK  $code  $url"
  else
    echo "FAIL $code  $url" >&2
    FAIL=1
    FAILED+=("$code $url")
  fi
}

notify_telegram() {
  local body="$1"
  local token="${TELEGRAM_BOT_TOKEN:-${BOT_TOKEN:-}}"
  local chat="${TELEGRAM_CHAT_ID:-454000856}"
  [[ -n "$token" ]] || return 0
  curl -sS -X POST "https://api.telegram.org/bot${token}/sendMessage" \
    --data-urlencode "chat_id=${chat}" \
    --data-urlencode "text=${body}" >/dev/null || true
}

case "$SITE" in
  org)
    URLS=(
      "https://usmcmin.org/"
      "https://usmcmin.org/plan.html"
      "https://usmcmin.org/bible.html"
      "https://usmcmin.org/dictionary/"
      "https://usmcmin.org/churches/"
      "https://usmcmin.org/blog.html"
      "https://usmcmin.org/assessments.html"
      "https://usmcmin.org/connect.html"
      "https://usmcmin.org/grind-report.html"
      "https://usmcmin.org/manifest.json"
      "https://usmcmin.org/robots.txt"
      "https://usmcmin.org/sitemap.xml"
      "https://usmcmin.org/assets/icons/favicon.svg"
      "https://usmcmin.org/assets/og/og-main.png"
      "https://usmcmin.org/assets/media/30-mighty-men-plan-overview-v32.mp4"
      "https://usmcmin.org/data/churches-index.json"
      "https://usmcmin.org/data/qa-sample.json"
      "https://usmcmin.org/churches/1002-church.html"
      "https://usmcmin.org/wheelhouse.html"
    )
    LABEL="usmcmin.org"
    ;;
  com)
    URLS=(
      "https://usmcmin.com/"
      "https://usmcmin.com/citizen.html"
      "https://usmcmin.com/citizen-table.html"
      "https://usmcmin.com/find-my-reps.html"
      "https://usmcmin.com/changelog.html"
      "https://usmcmin.com/sitemap.xml"
      "https://usmcmin.com/robots.txt"
      "https://usmcmin.com/sw.js"
      "https://usmcmin.com/assets/css/main.min.css"
      "https://usmcmin.com/assets/js/main.js"
      "https://usmcmin.com/data/index.json"
      "https://usmcmin.com/data/states/va.json"
      "https://usmcmin.com/assets/og/og-citizen.jpg"
      "https://usmcmin.com/family-captain.html"
      "https://usmcmin.com/ai-boot-camp.html"
    )
    LABEL="usmcmin.com"
    ;;
  *)
    echo "Unknown site: $SITE (use org or com)" >&2
    exit 2
    ;;
esac

echo "== post-deploy smoke: $LABEL (${#URLS[@]} URLs) =="
for u in "${URLS[@]}"; do
  check_url "$u"
done

if [[ "$FAIL" -ne 0 ]]; then
  msg="Deploy smoke FAIL ($LABEL): ${#FAILED[@]} URL(s) bad. First: ${FAILED[0]}"
  notify_telegram "$msg"
  echo "$msg" >&2
  exit 1
fi

echo "PASS: all ${#URLS[@]} smoke URLs OK ($LABEL)"
