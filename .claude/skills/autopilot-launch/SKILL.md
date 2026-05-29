---
name: autopilot-launch
description: Launch a coordinated set of background enrichment autopilots for the MOOP Church Directory and monitor their progress. Use whenever the user asks to spin up, kick off, run, drive, or grind enrichment for some duration ("run enrichment for the next hour", "kick off VA autopilots", "let's get more quick-links", "spin up a 2-hour image pass on North Carolina"). Picks the right combination of pastor / image / sbc-detail / quicklinks autopilots based on what scope and what the directory needs most, sets the duration + per-tick + state scope, launches them detached, verifies they are alive, and writes a status summary. Also handles relaunch + shutdown semantics. Triggers in the bible-reading-plan-bot repo.
---

# Autopilot Launch

Wraps the launch + monitor + shutdown lifecycle of the four background enrichment autopilots. Replaces the manual sequence of "kill existing, decide PER_TICK, build env-var soup, `nohup` four scripts, verify all alive, monitor". Used when the user wants to drive enrichment for a stretch of time without micromanaging each scraper.

## The four autopilots and what each does

| Autopilot | Script | What it does each tick |
| --- | --- | --- |
| pastor | `scripts/pastor-autopilot.sh` | Scrape /staff, /team, /pastors etc. on church websites for pastor names; merge JSONL into churches.json; commit |
| image-v2 | `scripts/image-autopilot-v2.sh` | Scrape OG image + apple-touch-icon from church websites; populates image_url (hero) + image_thumb (logo); commit |
| sbc-detail | `scripts/sbc-detail-autopilot.sh` | Scrape SBC.net per-church pages for website + geocode + phone; commit |
| quicklinks | `scripts/quicklinks-autopilot.sh` | Probe ~58 common deep-link paths per church website (beliefs / sermons / staff / etc.); merge + regenerate pages; commit |

All four follow the same race-free JSONL pattern (scrape → JSONL → merge → commit → push), single-instance lockfile under `/tmp`, and accept these env vars:

- `STATE` — 2-letter state code (e.g. `VA`) or `all` for nationwide; defaults to script-specific
- `DURATION_HRS` — how long the autopilot runs before exiting cleanly
- `PER_TICK` — churches processed per tick
- `TICK_INTERVAL` — seconds between ticks

## When to use this skill

- User asks for any timed enrichment block ("run for the next hour", "go for two hours overnight")
- User asks to expand enrichment scope ("now do NC", "spread to all 50 states")
- Resuming enrichment after a previous window ended cleanly
- Switching active scope mid-session ("pivot from VA to TX")

## When NOT to use this skill

- Single-church enrichment (use `enrich-church-single`)
- New-church expansion or signature cross-reference (use `church-directory-enrichment`)
- Status-only queries with no launch ("where do we stand?") — use `directory-pulse` instead

## Workflow

### 1. Check current autopilot state

```bash
bash .claude/skills/autopilot-launch/scripts/status.sh
```

The helper prints: which autopilots are running, what their start time + scope + duration is, last commit each pushed, and JSONL queue size each is processing.

### 2. Decide the launch shape

Default shape for a "run for the next hour" request, scope = current Fredericksburg/VA focus:

```
STATE=VA DURATION_HRS=1 PER_TICK=60 TICK_INTERVAL=600 quicklinks-autopilot.sh
STATE=VA DURATION_HRS=1                              image-autopilot-v2.sh
STATE=VA DURATION_HRS=1                              pastor-autopilot.sh
```

Defaults the user might ask you to tweak:

- **Wider scope**: `STATE=all` for nationwide, but then drop PER_TICK or extend DURATION_HRS to avoid burning CPU/network
- **Longer overnight run**: bump DURATION_HRS to 6 or 8; reduce PER_TICK on quicklinks if the page regeneration cost adds up
- **Pivoting active scope**: kill running autopilots first, then relaunch with new STATE (lockfile cleanup is automatic via the EXIT trap)

### 3. Kill any running autopilots that conflict

If the user is changing scope or duration, stop existing instances first:

```bash
pkill -f pastor-autopilot.sh
pkill -f image-autopilot-v2.sh
pkill -f sbc-detail-autopilot.sh
pkill -f quicklinks-autopilot.sh
# wait, then clean lockfiles in case the EXIT trap did not fire
sleep 3
rm -f /tmp/*-autopilot*.lock
```

### 4. Launch in parallel (detached)

```bash
bash .claude/skills/autopilot-launch/scripts/launch.sh VA 1 60
```

Args (positional, all optional):
1. STATE (default: VA)
2. DURATION_HRS (default: 1)
3. PER_TICK for quicklinks (default: 60)

The launcher runs the right four scripts via `nohup ... < /dev/null & disown`, redirects each log to a known `/tmp/*-autopilot*.log` path, sleeps 4 seconds, then prints the `pgrep` confirmation + first 3 lines of each log so the operator can verify start-up.

### 5. Optional: pick a single autopilot

If only one autopilot makes sense (e.g. queue is exhausted for the others), launch just that one:

```bash
nohup env STATE=VA DURATION_HRS=1 bash scripts/quicklinks-autopilot.sh > /tmp/quicklinks-autopilot.log 2>&1 < /dev/null & disown
```

### 6. Monitor on a sane cadence

Do NOT poll constantly. Each autopilot commits on its own tick interval; let the commits land. A reasonable check pattern:

- 5-10 minutes after launch: confirm all expected autopilots are alive and tick 1 has run
- Once per tick interval after that: check log tails, no action required
- At end of window: run `directory-pulse` to confirm what moved

### 7. Wind down

When all autopilots exit (their windows close, their queues exhaust, or the user calls a stop), there is nothing to do. The EXIT trap removes the lockfiles. Commits are already pushed. The work is done.

## Common gotchas

- **Race with other workstreams**: if you have inline scripts writing to churches.json while an autopilot is running, the autopilot's pull-rebase will either auto-stash or reject. Quiet your workstreams during long enrichment windows.
- **JSONL accumulation**: `/tmp/*-scrapes.jsonl` files accumulate across sessions. They are the resume-safe set. Do NOT delete them mid-run; do clear them if you want to re-scrape churches that were already processed.
- **`directory-pulse` after each window**: gives the user a clean view of what moved. The autopilot logs alone do not show net coverage; the pulse does.
- **Image-thumb is also the logo**: image-v2 captures both image_url (hero) and image_thumb (apple-touch-icon, which is the logo). Running image-v2 helps logo coverage even if you do not care about hero photos.
- **Pastor enrichment hit rate is low** (~5-10% per tick) because most placeholder records correspond to churches that simply do not publish pastor names on their website. Expect a slow climb.
