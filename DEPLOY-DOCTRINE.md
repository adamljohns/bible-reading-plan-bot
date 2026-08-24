# Deploy Doctrine — usmcmin.org and usmcmin.com

**Canonical. Last updated 2026-08-24.** If any other file, memory note, or lane
rule contradicts this one, this one wins and the other should be corrected.

Both sites are served from Cloudflare R2 by a Worker. GitHub Pages has been
dormant since 2026-07-02 (`.org`) and 2026-07-03 (`.com`). Any doc still saying
"GitHub Pages" is stale.

| | usmcmin.org | usmcmin.com |
|---|---|---|
| repo | `bible-reading-plan-bot` | `usmcmin-com` |
| source dir | `docs/` | repo root |
| bucket | `usmcmin-site` | `usmcmin-com-site` |
| worker | `usmcmin-site` (custom domains) | `usmcmin-com` (zone routes) |

## The five rules

**1. Deploy is `git push origin main`. Nothing else deploys.**
The Action syncs to R2 in ~2-4 min. Do not hand-upload site content with
rclone. The one exception is R2-only media — see rule 3.

**2. Never push from `~/bible-reading-plan-bot`.**
That checkout is fleet scratch space. Agents re-branch it constantly; on
2026-08-23 it sat on `ship/pxa-0807-enl25`, 746 commits behind main, and on
08-24 on `deploy/ci-guards` carrying an uncommitted edit that would have
reverted a live fix. Push from a clean worktree instead:

    git -C ~/bible-reading-plan-bot worktree add --no-checkout -b <branch> /tmp/work origin/main
    cd /tmp/work && git sparse-checkout init --cone && git sparse-checkout set <paths> && git checkout

`~/Scripts/deploy-usmcmin-org.sh` refuses to run unless the checkout is level
with `origin/main`. Do not pass `ALLOW_STALE=1` to get around that.

**3. MP4/M4A under `assets/media` and `assets/video` live in R2 ONLY.**
They are excluded from the sync, so CI never uploads them and never restores
them. Add or update them with `rclone copy` (never `sync`), and keep a local
copy — CI cannot put them back.

The exclude pattern must be **`assets/media/**.mp4`**, never
`assets/media/**/*.mp4`. In rclone the `/` in `**/*` requires at least one
intervening directory, so `**/*.mp4` does not match files sitting directly in
`assets/media` — which is where the plan videos are. That mismatch deleted the
v32 MP4 three times before it was found.

Anything that is not R2-only belongs in git, where a sync cannot orphan it.

**4. Do not "simplify" the deploy guards.**
`bin/rclone-sync-guarded.sh` dry-runs first, counts pending deletions, and
aborts above the threshold (`RCLONE_MAX_DELETES`, default 50; override with
`ALLOW-DELETES` in the commit message). It runs a self-test before every sync
that proves it can still detect a deletion. If that self-test fails, rclone's
output wording changed — fix the pattern, do not delete the check. Its call
signature is `<local> <remote> -- <max-deletes> [rclone flags...]`; the `--`
parsing is load-bearing.

Two prior "fixes" to this file looked correct in review and silently did
nothing. Assume the same of your own until you have watched the abort path fire.

**5. Verify from outside, not from inside the job.**
`bin/post-deploy-smoke.sh org|com` curls the canonical URLs. An alert that
fires inside the job it guards cannot report a failure that kills the job
first — that is how usmcmin.com deployed nothing for three runs with zero
notifications. `com.moop.deploy-watchdog` (launchd, 5 min) polls both repos
from this Mac and alerts Telegram on failure and recovery.

Never put a Telegram bot token in these repos. **Both are public**, and the
token on this Mac belongs to the Claude bridge bot, which can read Adam's
private conversation.

## Standing rules that outrank convenience

- Nothing public auto-posts. Outward-facing content waits for Adam's APPROVE.
- Never truly delete. Archive with a ledger and a restore path.
- If you find a guard, an alert, or a backup that has never been observed
  working, treat it as broken until you have made it fail on purpose.
