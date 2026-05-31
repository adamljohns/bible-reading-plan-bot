#!/bin/bash
# publish_reading.sh — one-command publish for a single day's reading.
#
# After you write data/readings/<date>.md, run:
#   bash scripts/publish_reading.sh 2026-05-24
#
# This will:
#   1. Render data/readings/<date>.md  ->  docs/readings/<date>.html
#   2. Update docs/assets/readings-available.json inventory
#   3. Generate ElevenLabs audio for each watch (5 watches × ~5k chars each)
#       — skip --audio with the --no-audio flag
#       — first run prints a quota check so you know if it'll fit
#   4. Stage + commit + push all the new/changed files
#   5. Telegram-ping you when it's live
#
# Flags:
#   --no-audio       skip ElevenLabs (just render + commit + push)
#   --no-push        skip git push (commit only)
#   --dry-run        preview what would happen, no API calls, no git
#
# Requires (read once from macOS Keychain — no setup):
#   ELEVENLABS_API_KEY  via security find-generic-password OPENCLAW_ELEVENLABS_API_KEY
#   ELEVENLABS_VOICE_ID hardcoded to g2aOBFToLERDXa3F0cHV (Adam's pro clone)

set -eu

REPO="/Users/moop_bot_pro/bible-reading-plan-bot"
cd "$REPO"

# ─── Args ──────────────────────────────────────────────────────────────────
DATE=""
NO_AUDIO=0
NO_PUSH=0
DRY_RUN=0

while [ $# -gt 0 ]; do
  case "$1" in
    --no-audio) NO_AUDIO=1; shift ;;
    --no-push)  NO_PUSH=1; shift ;;
    --dry-run)  DRY_RUN=1; shift ;;
    --help|-h)
      sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *) DATE="$1"; shift ;;
  esac
done

if [ -z "$DATE" ]; then
  echo "Usage: $0 <YYYY-MM-DD> [--no-audio] [--no-push] [--dry-run]" >&2
  exit 1
fi

MD="$REPO/data/readings/${DATE}.md"
HTML="$REPO/docs/readings/${DATE}.html"

if [ ! -f "$MD" ]; then
  echo "ERROR: $MD does not exist. Write the reading first." >&2
  exit 1
fi

echo "==[ publish $DATE ]=========================================="

# ─── Render ───────────────────────────────────────────────────────────────
echo
echo "[1/5] Render MD -> HTML"
if [ "$DRY_RUN" -eq 1 ]; then
  echo "  DRY-RUN: would run build_reading_page_from_md.py $DATE"
else
  python3 scripts/build_reading_page_from_md.py "$DATE"
fi

# ─── Inventory ────────────────────────────────────────────────────────────
echo
echo "[2/5] Update readings-available.json inventory"
if [ "$DRY_RUN" -eq 1 ]; then
  echo "  DRY-RUN: would rewrite docs/assets/readings-available.json"
else
  python3 -c "
import importlib.util
spec = importlib.util.spec_from_file_location('m', 'scripts/build_reading_page_from_md.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
mod.write_inventory()
"
  echo "  Rebuild reading index (per-day JSON + master)"
  python3 scripts/build_reading_index.py "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --date "$DATE" | sed 's/^/  /'
fi

# ─── Audio ────────────────────────────────────────────────────────────────
if [ "$NO_AUDIO" -eq 1 ]; then
  echo
  echo "[3/5] Skipping audio (--no-audio)"
else
  echo
  echo "[3/5] Generate ElevenLabs audio"
  export ELEVENLABS_API_KEY="$(security find-generic-password -s "OPENCLAW_ELEVENLABS_API_KEY" -w 2>/dev/null)"
  export ELEVENLABS_VOICE_ID="g2aOBFToLERDXa3F0cHV"
  if [ -z "$ELEVENLABS_API_KEY" ]; then
    echo "  WARN: keychain key 'OPENCLAW_ELEVENLABS_API_KEY' not found — skipping audio"
  elif [ "$DRY_RUN" -eq 1 ]; then
    python3 scripts/generate_audio.py --dry-run "$DATE" | sed 's/^/  /'
  else
    echo "  Quota check:"
    python3 scripts/generate_audio.py --quota | sed 's/^/    /'
    echo
    python3 scripts/generate_audio.py "$DATE" | sed 's/^/  /'
  fi
fi

# ─── Re-render so <audio> tags pick up the just-generated MP3s ────────────
if [ "$NO_AUDIO" -eq 0 ] && [ "$DRY_RUN" -eq 0 ]; then
  echo
  echo "[3.5] Re-render HTML now that audio files exist"
  python3 scripts/build_reading_page_from_md.py "$DATE"
fi

# ─── Commit + push ────────────────────────────────────────────────────────
echo
echo "[4/5] Stage + commit"
FILES=("data/readings/${DATE}.md" "docs/readings/${DATE}.html" "docs/assets/readings-available.json" "docs/assets/readings/${DATE}.json" "docs/assets/reading-index.json")
if [ "$NO_AUDIO" -eq 0 ]; then
  for w in wisdom husband father citizen peace; do
    f="docs/assets/audio/readings/${DATE}-${w}.mp3"
    [ -f "$f" ] && FILES+=("$f")
  done
fi

if [ "$DRY_RUN" -eq 1 ]; then
  echo "  DRY-RUN: would stage:"
  for f in "${FILES[@]}"; do echo "    $f"; done
else
  git add "${FILES[@]}"
  # Compose commit message
  COUNT_AUDIO=$(ls docs/assets/audio/readings/${DATE}-*.mp3 2>/dev/null | wc -l | tr -d ' ')
  MSG="Daily readings: publish ${DATE}"
  if [ "$COUNT_AUDIO" -gt 0 ]; then
    MSG="${MSG} (with ${COUNT_AUDIO} watch audio files)"
  fi
  git commit -m "$(cat <<COMMIT_EOF
${MSG}

- data/readings/${DATE}.md
- docs/readings/${DATE}.html
$([ "$COUNT_AUDIO" -gt 0 ] && echo "- ${COUNT_AUDIO} ElevenLabs MP3 voiceovers")

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
COMMIT_EOF
)"
fi

echo
echo "[5/5] Push + ping"
if [ "$DRY_RUN" -eq 1 ]; then
  echo "  DRY-RUN: would push to origin/main"
elif [ "$NO_PUSH" -eq 1 ]; then
  echo "  --no-push: skipped"
else
  git push origin main
  # Ping Adam that it's live
  bash /Users/moop_bot_pro/.hermes/bin/notify-adam.sh \
       --level info \
       --title "📖 Daily reading published — ${DATE}" \
       --body "Live now at https://usmcmin.org/readings/${DATE}.html" \
    2>/dev/null || true
fi

echo
echo "==[ done ]==========================================================="
