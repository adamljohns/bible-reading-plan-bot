#!/bin/bash
# deploy-rclone-guard.test.sh
#
# The rclone pin guard in .github/workflows/deploy-r2.yml failed ~2% of deploys
# while printing the CORRECT version immediately above its own FAIL line:
#
#     rclone v1.68.2
#     FAIL: expected rclone v1.68.2
#
# Cause: `rclone version | head -1 | grep -q "$VER"` under `set -o pipefail`.
# grep -q exits on first match -> pipe closes -> head/rclone take SIGPIPE (141)
# -> pipefail reports 141 as the pipeline status -> the || branch fires BECAUSE
# the match succeeded. Intermittent because rclone's short output usually wins
# the race into the 64K pipe buffer.
#
# Per rclone-guards-must-be-tested: a guard that has only ever passed has not
# been tested. The REJECT cases run first and carry the weight.
set -uo pipefail
PIN="v1.68.2"
pass=0; fail=0
ok(){ if [ "$2" = "$3" ]; then echo "  ok   $1"; pass=$((pass+1)); else echo "  FAIL $1 (want $3, got $2)"; fail=$((fail+1)); fi; }

# The guard exactly as the workflow runs it.
guard() {
  local out="$1"
  ( set -euo pipefail
    rclone_out="$out"
    rclone_line="${rclone_out%%$'\n'*}"
    # shellcheck disable=SC2086
    set -- $rclone_line
    [ "${2:-}" = "${PIN}" ] ) >/dev/null 2>&1
  echo $?
}

echo "must REJECT (the halt path):"
ok "stale apt build"        "$(guard 'rclone v1.60.0
- os/version: ubuntu 24.04')" 1
ok "empty output"           "$(guard '')" 1
ok "near-miss version v1.68.20 is NOT v1.68.2" "$(guard 'rclone v1.68.20')" 1
ok "prefix near-miss v1.68"  "$(guard 'rclone v1.68')" 1
ok "wrong tool entirely"    "$(guard 'rsync  version 3.2.7')" 1
ok "pin only on a later line, not line 1" "$(guard 'rclone v1.60.0
built with v1.68.2')" 1

echo "must ACCEPT:"
ok "exact pinned version"   "$(guard 'rclone v1.68.2
- os/version: ubuntu 24.04
- go/version: go1.23')" 0
ok "single-line output"     "$(guard 'rclone v1.68.2')" 0

# The regression itself: 300 consecutive runs, zero false failures.
echo "no-false-failure soak (the actual bug):"
false_fails=0
for _ in $(seq 1 300); do
  [ "$(guard 'rclone v1.68.2
- os/version: ubuntu 24.04
- os/kernel: 6.8
- go/version: go1.23')" != "0" ] && false_fails=$((false_fails+1))
done
ok "300 runs, correct version, zero false failures" "$false_fails" 0

# Structural check. The soak above cannot reliably reproduce the original race
# (it is timing-dependent -- with rclone's short output it loses maybe 2% of the
# time), so the durable guarantee is that the workflow no longer pipes into a
# short-circuiting matcher at all. SIGPIPE cannot happen without a pipe.
echo "structure (why the race cannot recur):"
WF="$(dirname "$0")/../.github/workflows/deploy-r2.yml"
step="$(sed -n '/Fail loudly rather than silently/,/^      - name:/p' "$WF")"
case "$step" in
  *"| grep -q"*|*"|grep -q"*) echo "  FAIL pin check pipes into grep -q again"; fail=$((fail+1)) ;;
  *) echo "  ok   pin check does not pipe into grep -q"; pass=$((pass+1)) ;;
esac
case "$step" in
  *'rclone_out="$(rclone version)"'*) echo "  ok   version captured before matching"; pass=$((pass+1)) ;;
  *) echo "  FAIL version no longer captured before matching"; fail=$((fail+1)) ;;
esac

echo
echo "rclone version guard: $pass passed, $fail failed."
[ "$fail" -eq 0 ] || exit 1
