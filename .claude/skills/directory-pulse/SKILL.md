---
name: directory-pulse
description: Print canonical coverage metrics for the MOOP Church Directory at docs/data/churches.json. Use whenever the user asks for status / coverage / stats / pulse on the directory ("where do we stand?", "how many churches have logos?", "what's our pastor coverage?", "what's the SBC backfill at?"), or after running any enrichment pass to verify what moved. Supports optional scope filters by state, city, or network. Triggers in the bible-reading-plan-bot repo or when the user references usmcmin.org/churches.html in a stats context.
---

# Directory Pulse

A canonical coverage snapshot for the MOOP Church Directory. Replaces the inline `node -e "..."` one-liners that get rewritten every time the user asks for status.

## What it reports

- **Total churches** in the directory
- **With real pastor** (tight filter that excludes "Verify", "Unknown", "See website", and the ~20 known placeholder phrases)
- **With image_url** (scraped exterior photo via OG)
- **With image_thumb** (church logo via apple-touch-icon)
- **Geocoded** (lat/lng present)
- **With quick_links** (deep-link chips)
- **With enrichment_sources** (at least one source URL)
- **needs_review** flag count

Plus per-network breakdown via `cross_listed_in`: SBC, Founders, 9Marks, TGC, Acts 29, SGC, Pillar, Trinity.

## Usage

Call the helper directly; no Node arguments required for a full-directory pulse:

```bash
bash .claude/skills/directory-pulse/scripts/pulse.sh
```

Scope to a state, city, or network by passing one positional arg (it gets matched against address regex / cross_listed_in array, so case does not matter):

```bash
bash .claude/skills/directory-pulse/scripts/pulse.sh VA
bash .claude/skills/directory-pulse/scripts/pulse.sh Fredericksburg
bash .claude/skills/directory-pulse/scripts/pulse.sh sbc
```

## When to call this

- At the start of any enrichment session, to set a baseline
- After every autopilot tick or merge to confirm what moved
- When the user asks "where do we stand?" or any synonym
- Before answering "how many" / "what's our coverage on" questions about the directory

Do NOT make up coverage numbers from memory. Always re-run this; the autopilots commit constantly and the cached numbers in your context window go stale fast.

## What this skill does NOT do

- Does not modify churches.json
- Does not regenerate pages
- Does not commit anything

It is a read-only telemetry helper. For changes, hand off to `enrich-church-single`, `autopilot-launch`, or the existing `church-directory-enrichment` skill.
