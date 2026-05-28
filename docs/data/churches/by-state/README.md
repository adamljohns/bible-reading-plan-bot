# Per-state church-directory shards

Generated from `docs/data/churches.json` by `scripts/build_state_shards.py`.

The monolithic `churches.json` (58 MB and growing — GitHub warns past 50 MB) is the source of truth. These shards exist so that pages and scripts which only need one state's records can fetch a single ~1-7 MB file instead of the full monolith.

## File layout

```
docs/data/churches/by-state/
├── _index.json          ← summary: per-state counts, generated_at, invariant check
├── _unstated.json       ← records with no `state` field (1,063 after V7.0.1)
├── _foreign.json        ← records with non-US state codes (currently 0)
├── al.json              ← Alabama
├── ak.json              ← Alaska
├── ...                  ← 50 states + DC
├── tx.json              ← Texas (largest shard at ~6.7 MB / 4,248 records)
└── wy.json              ← Wyoming
```

## Shard schema

Each shard has the same top-level shape:

```json
{
  "directory_version": "V7.0.2",
  "directory_updated": "2026-05-28",
  "shard_source": "docs/data/churches.json",
  "shard_generated_at": "2026-05-28T12:59:00+00:00",
  "shard_format_version": 1,
  "state": "TX",
  "record_count": 4248,
  "churches": [
    { "id": "...", "name": "...", "address": "...", "state": "TX", ... },
    ...
  ]
}
```

Records inside `churches[]` are byte-identical to their counterpart in the source `churches.json` — no field stripping, no transformation. The shard is just a state-filtered subset.

## Invariant

```
sum(shard.record_count for shard in *.json) + _unstated.record_count + _foreign.record_count
  == churches.json.total_churches
```

The build script verifies this on every run and writes the result to `_index.json` under the `invariant_ok` key. If `invariant_ok: false`, the shards are stale — re-run the build script.

## Rebuilding

```bash
python3 scripts/build_state_shards.py
```

Idempotent — safe to run after any change to `churches.json`. Overwrites all shards in place.

## Using shards from JavaScript

```js
// Fetch only the state you care about
const r = await fetch('/data/churches/by-state/tx.json');
const { state, record_count, churches } = await r.json();

// The full _index for navigation/state-picker UIs
const idx = await (await fetch('/data/churches/by-state/_index.json')).json();
// idx.by_state.TX.count === 4248
```

## When to keep using `churches.json` instead

- Cross-state queries (e.g. directory-politicians.html joining politicians to home churches without knowing the state up front)
- Dedup passes
- Bulk enrichment workflows
- Anything that needs the full corpus in memory

The shards are an optimization for the **read-only display path**, not a replacement for the source of truth.

## Records without a state

The 1,063 records in `_unstated.json` are stranded after the V7.0.1 backfill — slug-suffix extraction, address-regex extraction, and long-state-name extraction all failed. Most are records where the address field is empty, abbreviated to a city name only, or contains a non-US locale. Candidates for a future per-record agent verification pass.
