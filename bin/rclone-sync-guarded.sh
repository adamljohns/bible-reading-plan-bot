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
# bash 3.2 (macOS) treats "${EXTRA[@]}" as unbound when empty under `set -u`;
# expand via ${EXTRA[@]+...} so this script runs locally as well as in CI.

COMMIT_MSG="${GITHUB_EVENT_HEAD_COMMIT_MESSAGE:-}"
if [[ -z "$COMMIT_MSG" ]] && git rev-parse --git-dir >/dev/null 2>&1; then
  COMMIT_MSG="$(git log -1 --pretty=%B 2>/dev/null || true)"
fi

echo "== rclone sync guard =="
echo "local:  $LOCAL"
echo "remote: $REMOTE"
echo "max deletes (without ALLOW-DELETES): $MAX_DELETES"

# --- guard self-test -------------------------------------------------------
# Proves, on every run, that the delete-detection pattern still matches what
# this rclone build actually prints. A guard that cannot detect a deletion is
# worse than no guard: it reports PASS while a wipe goes through.
self_test() {
  local d s_dir d_dir n
  d="$(mktemp -d)"; s_dir="$d/src"; d_dir="$d/dst"
  mkdir -p "$s_dir" "$d_dir"
  : > "$d_dir/canary-a"; : > "$d_dir/canary-b"
  n="$(rclone sync "$s_dir" "$d_dir" --dry-run --stats-one-line 2>&1 | grep -c 'Skipped delete' || true)"
  rm -rf "$d"
  if [[ "${n:-0}" -ne 2 ]]; then
    echo "FAIL: delete guard self-test expected 2 detections, got ${n:-0}." >&2
    echo "      rclone's dry-run wording changed; fix the pattern before deploying." >&2
    exit 1
  fi
  echo "self-test OK: delete detection works (2/2)"
}
self_test

DRY_LOG="$(mktemp)"
trap 'rm -f "$DRY_LOG"' EXIT

set +e
rclone sync "$LOCAL" "$REMOTE" ${EXTRA[@]+"${EXTRA[@]}"} --dry-run --stats-one-line 2>&1 | tee "$DRY_LOG"
DRY_RC=${PIPESTATUS[0]}
set -e

if [[ "$DRY_RC" -ne 0 ]]; then
  echo "FAIL: rclone dry-run exited $DRY_RC" >&2
  exit "$DRY_RC"
fi

# rclone --dry-run announces a pending deletion as:
#   NOTICE: <file>: Skipped delete as --dry-run is set (size N)
# It NEVER prints the word "Deleted" in a dry run. Grepping for "Deleted" counts
# 0 every time and silently disarms this entire guard -- that is exactly how the
# 2026-08-23 poster deletion got through. Verified against rclone on 2026-08-23.
# self_test() below fails the build if rclone ever changes this wording.
DELETE_COUNT="$(grep -c 'Skipped delete' "$DRY_LOG" 2>/dev/null || true)"
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
rclone sync "$LOCAL" "$REMOTE" ${EXTRA[@]+"${EXTRA[@]}"} --stats-one-line --stats 30s
echo "PASS: sync complete (dry-run deletes=$DELETE_COUNT)"
