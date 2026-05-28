# HANDOFF — MOOP Church Directory state

**Last updated:** 2026-05-28 by Claude (this session)
**Current version:** V7.0.3
**Record count:** 28,584 churches
**Tip commit on origin/main:** push pending (see "Pending" section below)

This file is the **single source of truth** for "where the church directory work stands." Read it first when picking up the project in a new session.

Mirror copy lives at `~/.openclaw/shared-memory/context/church-directory-handoff.md` so OpenClaw agents (preacher-john, chaps) see the same status via their `shared-context/` symlink.

---

## Quick orientation

- **Source of truth:** `docs/data/churches.json` (60 MB)
- **State shards (V7.0.2):** `docs/data/churches/by-state/{xx}.json` — 51 files (50 states + DC)
- **Denom shards (V7.0.3):** `docs/data/churches/by-denomination-family/{slug}.json` — 151 files
- **International records (V7.0.3):** `docs/data/churches/by-state/_international.json` — 831 records, classified by country
- **Truly unstated:** `docs/data/churches/by-state/_unstated.json` — 232 records (mostly city-only addresses; need agent research)

**Both shard collections carry the rubric inline** (`shard_format_version: 2`) so page consumers don't need to fetch the monolith.

---

## What just landed (V7.0.1 → V7.0.3)

### V7.0.1 (commit `fd1f1627e6`) — data quality pass
- **State backfill on 26,137 records.** Now 27,521/28,584 have a `state` field (96% coverage).
- **LGBTQ-affirming denomination rubric pass.** 3 newly flagged. Two near-disasters caught and fixed during the work (TEC matching "Pen**TEC**ostal", "Episcopal Church" matching "Reformed Episcopal Church"). The matcher now has hard-exclusion list + 23-case unit test.
- **Denomination string normalization on 1,276 records.** "SBC" / "Southern Baptist (SBC)" → "Southern Baptist Convention (SBC)". "Non-denominational" → "Non-Denominational".

### V7.0.2 (commit `650c83ebfa`) — per-state shards
- Per-state JSON shards in `docs/data/churches/by-state/`
- TX shard largest at 6.7 MB / 4,248 records
- README documents schema + invariant + JS fetch pattern

### V7.0.3 (pending push) — international + denom shards + page migration
- **International classification.** 905 of 1,063 unstated records identified by country (Canada 215, UK 140, Australia 63, PR 56, etc.). Now routed to `_international.json`.
- **Per-denomination-family shards.** 151 shards covering 28,584 records, invariant verified.
- **Regional pages migrated to shards.** churches-virginia.html, churches-fxbg.html, churches-dc.html now fetch state shards instead of the 60 MB monolith. Payload reductions:
  - churches-virginia.html: 60 MB → 3.7 MB (16× speedup)
  - churches-fxbg.html: 60 MB → 5.9 MB
  - churches-dc.html: 60 MB → 4.7 MB
- **Footer counts** on those three pages now fetch `_index.json` (few KB) instead of the monolith.
- **Rubric is now carried in every shard** (`shard_format_version: 2`), so loaders need exactly one fetch.

---

## File / script conventions

| Path | Purpose |
|------|---------|
| `docs/data/churches.json` | The monolith. Source of truth. Don't migrate away — many scripts still write to it directly. |
| `docs/data/churches/by-state/*.json` | Per-state shards. Rebuilt by `scripts/build_state_shards.py`. |
| `docs/data/churches/by-denomination-family/*.json` | Per-denom shards. Rebuilt by `scripts/build_denomination_shards.py`. |
| `scripts/build_state_shards.py` | Idempotent. Run after any change to `churches.json`. |
| `scripts/build_denomination_shards.py` | Idempotent. Run after any change to `churches.json`. |
| `scripts/v701_data_quality_pass.py` | State backfill + LGBTQ denom flagger + denom string normalizer. |
| `scripts/classify_unstated_countries.py` | Tags non-US records with country + country_code. |
| `scripts/reconcile_cori_v496.py` | Historic — reconciliation script after divergent V4.9.x branch. Don't re-run unless backing out V5+. |

### Invariants

Both shard build scripts verify and write `invariant_ok` to their `_index.json`. If you change `churches.json`, run both build scripts to keep shards consistent.

```bash
python3 scripts/build_state_shards.py
python3 scripts/build_denomination_shards.py
```

---

## Open work (next session candidates, in priority order)

### 1. Resolve the 232 stranded records in `_unstated.json`
These are records where state extraction, country extraction, and city-name extraction all failed. Mostly city-only addresses (e.g., "Conrad Hotel" with no country marker) or local-language names. Worth a small agent pass — group by likely-country heuristic, then verify via the church's network affiliation (TGC/9Marks/Acts 29 directories almost always list city + country).

### 2. SBC shard sub-sharding
`southern-baptist-sbc.json` is 21 MB / 16,713 records. Consumers that want SBC churches in one state still load all 16k. Solution: also produce `by-denomination-family/southern-baptist-sbc/{state}.json` two-level shards. Easy script to write.

### 3. Migrate the nationwide page (`churches.html`)
Currently fetches the 60 MB monolith. Hardest one to migrate because it's "all states." Two options:
  - **Lazy load** — fetch `_index.json` for initial render (counts, state-picker), then load shards on demand as user filters
  - **Aggregate index** — produce a "skinny" all-records index that has only the fields needed for cards (id, name, address, state, rating, denomination, website) and fetch that
The skinny index is probably ~10 MB and gives the page everything it needs for the card grid. Click-to-expand could lazy-fetch the full record from the appropriate shard.

### 4. directory-networks.html / directory-politicians.html migration
These do cross-cutting joins. They might genuinely need the monolith. Audit first.

### 5. Hunt the remaining "Baptist" generic denomination tags
`Baptist` (4,808 records) and `Baptist (Other)` (236 records) are catch-all buckets. Many should be SBC or BGAV or IFB — needs the same kind of agent pass that surfaced the 244 false-positive LGBTQ matches before fixing.

### 6. Pastor "Unknown" / placeholder cleanup
~6,179 records have placeholder pastor names ("Verify", "Unknown", "Check website"). The other session has been running `9Marks pastor enrichment` waves at ~28% hit rate; continue those.

---

## Known gotchas

### 1. Three rating systems coexist
Records have `overall_rating` as one of:
- Color: `green` / `yellow` / `red` / `black` / `dead` (most records)
- Numeric: `4.0` through `9.7` (~373 records, from the parallel session's numeric scoring tier)
- Hybrid: `GREEN-YELLOW` was an old BBFI compound tag, normalized in cleanup commit `7fb524661`

Page renderers handle the colors. Numeric records may render oddly. Don't auto-convert without checking with the user — the parallel session uses numeric on purpose for some BBFI/IFB-adjacent records.

### 2. Two geography fields
- `state` (uppercase 2-letter US state code) — added V7.0.1, populated on 27,521/28,584 records
- `region` (lowercase sub-state subdivision like `fxbg`, `dc-nova`, `richmond`, `hampton-roads`, plus some legacy 2-letter state codes like `tx`)

**Use `state` for state-level filtering.** Use `region` for sub-state filtering (fxbg / dc-nova). Don't conflate them.

### 3. The "Reformed Episcopal Church" trap
"Reformed Episcopal Church (REC)" is **conservative** ACNA-aligned Anglican, NOT the LGBTQ-affirming Episcopal Church (TEC). The V7.0.1 LGBTQ rubric pass has a hard-exclusion list to keep them apart. If you write any denomination scanner, copy that exclusion logic from `scripts/v701_data_quality_pass.py:lgbtq_affirming_match()`.

### 4. The 14,649 SBC bulk-load records
Recognizable by `_sbc_bulkload: true`. They have minimal data (denomination + family + address + geo + image) but no per-dimension scoring. Need pastor enrichment + score_notes population over time. The parallel session has been chewing through these.

### 5. Backup branch
`backup/cori-pre-rebase-2026-05-18` preserves the V4.9.x work pre-reconciliation. Don't delete without verification — that work is otherwise gone.

---

## Working with the other Claude Code session

The parallel session has been doing massive batch work (Phase 6 networks/speakers, 9Marks pastor enrichment waves, SBC bulk-loads, dictionary expansion). When picking up work:

1. **Always `git fetch && git pull --ff-only origin main` first.** The parallel session pushes commits frequently.
2. **Don't bump `directory_version`** without checking what the parallel session has set it to. They've been on V5.7.0 → V6.0.0 → V7.0.0 tracks; coordinate before bumping.
3. **Avoid editing the same files in parallel.** churches.json is the main collision risk. If you need to make multiple edits, batch them into one script run and one commit so the diff window is small.
4. **Don't reset main without preserving a backup branch.** See V4.9.x reconciliation playbook in `tmp/RECONCILE_PLAYBOOK.md`.

---

## Pending in this session

- Commit V7.0.3 work (state classify + denom shards + page migration + handoff docs)
- Push to origin/main
- Drop the mirror copy of this file at `~/.openclaw/shared-memory/context/church-directory-handoff.md`

---

## Session-local TODO list

When this session ends, the TaskList tool's state is also part of the handoff — but it's session-scoped. The current task IDs:

- ✅ V7.0.1 data quality pass
- ✅ V7.0.2 per-state shards
- ✅ V7.0.3 country classification of unstated
- ✅ V7.0.3 per-region page migration
- ✅ V7.0.3 per-denomination-family shards
- 🔄 V7.0.3 handoff docs (this file)
- 🔄 V7.0.3 commit + push

Subsequent sessions should consult the **"Open work"** section above, not these task IDs.
