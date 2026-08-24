#!/usr/bin/env bash
# Guarded rclone sync: dry-run delete count, abort if over threshold unless ALLOW-DELETES.
set -euo pipefail

usage() {
  echo "Usage: $0 <local-path> <remote-spec> [-- max-deletes] [rclone sync args...]" >&2
  echo "  remote-spec example: r2:usmcmin-site" >&2
  exit 2
}

[[ $# -ge 2 ]] || usage

LOCAL="$1"
REMOTE="$2"
shift 2

MAX_DELETES="${RCLONE_MAX_DELETES:-50}"
if [[ "${1:-}" == "--" ]]; then
  shift
  MAX_DELETES="${1:-$MAX_DELETES}"
  shift
fi

EXTRA=("$@")

COMMIT_MSG="${GITHUB_EVENT_HEAD_COMMIT_MESSAGE:-}"
if [[ -z "$COMMIT_MSG" ]] && git rev-parse --git-dir >/dev/null 2>&1; then
  COMMIT_MSG="$(git log -1 --pretty=%B 2>/dev/null || true)"
fi

echo "== rclone sync guard =="
echo "local:  $LOCAL"
echo "remote: $REMOTE"
echo "max deletes (without ALLOW-DELETES): $MAX_DELETES"

DRY_LOG="$(mktemp)"
trap 'rm -f "$DRY_LOG"' EXIT

set +e
rclone sync "$LOCAL" "$REMOTE" "${EXTRA[@]}" --dry-run --stats-one-line 2>&1 | tee "$DRY_LOG"
DRY_RC=${PIPESTATUS[0]}
set -e

if [[ "$DRY_RC" -ne 0 ]]; then
  echo "FAIL: rclone dry-run exited $DRY_RC" >&2
  exit "$DRY_RC"
fi

DELETE_COUNT="$(grep -c 'Deleted' "$DRY_LOG" 2>/dev/null || true)"
DELETE_COUNT="${DELETE_COUNT:-0}"
echo "dry-run delete count: $DELETE_COUNT"

if [[ "$DELETE_COUNT" -gt "$MAX_DELETES" ]]; then
  if [[ "$COMMIT_MSG" == *ALLOW-DELETES* ]]; then
    echo "WARN: $DELETE_COUNT deletes > $MAX_DELETES but commit has ALLOW-DELETES — proceeding"
  else
    echo "FAIL: would delete $DELETE_COUNT objects (limit $MAX_DELETES)." >&2
    echo "Add ALLOW-DELETES to the commit message if intentional, or fix excludes." >&2
    exit 1
  fi
fi

echo "== rclone sync (live) =="
rclone sync "$LOCAL" "$REMOTE" "${EXTRA[@]}" --stats-one-line --stats 30s
echo "PASS: sync complete (dry-run deletes=$DELETE_COUNT)"
