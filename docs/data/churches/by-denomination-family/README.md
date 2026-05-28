# Per-denomination-family church-directory shards

Generated from `docs/data/churches.json` by `scripts/build_denomination_shards.py`.

Companion to the per-state shards in `../by-state/`. Same self-describing schema, same invariant guarantee. These shards power the network/denomination-filtered views (directory-networks.html, politicians-to-home-churches joins).

## File layout

```
docs/data/churches/by-denomination-family/
├── _index.json                          per-family counts, generated_at, invariant
├── _empty.json                          records with no denomination_family (currently 0)
├── southern-baptist-sbc.json            largest shard — 16,713 records, 21 MB
├── baptist.json                         4,808 records
├── reformed.json                        885 records
├── non-denominational.json              838 records
├── presbyterian-pca.json                226 records
├── pca.json                             249 records (note: separate slug from above)
├── lutheran-lcms.json                   221 records
├── … 144 more shards                    one per distinct denomination_family value
```

151 shards total after merging 4 slug collisions (e.g., "Non-denominational" and "Non-Denominational" merge to `non-denominational.json`).

## Shard schema

```json
{
  "directory_version": "V7.0.3",
  "directory_updated": "2026-05-28",
  "shard_source": "docs/data/churches.json",
  "shard_generated_at": "2026-05-28T17:50:00+00:00",
  "shard_format_version": 2,
  "rubric": [ ... 10 dimensions ... ],
  "denomination_family": "Presbyterian (PCA)",
  "record_count": 226,
  "churches": [
    { "id": "...", "denomination_family": "Presbyterian (PCA)", ... }
  ]
}
```

## Invariant

```
sum(shard.record_count) + _empty.record_count
  == churches.json.total_churches
```

The build script verifies this and writes `invariant_ok` to `_index.json`.

## Naming convention (slugify)

Family names are slugified for filenames:
- lowercase
- `(`, `)`, `/`, `,` → space
- non-alphanumeric (except hyphen) → removed
- spaces and runs of hyphens → single hyphen
- leading/trailing hyphens trimmed
- empty string → `unknown`

Examples:
- `Presbyterian (PCA)` → `presbyterian-pca.json`
- `Lutheran (LCMS)` → `lutheran-lcms.json`
- `Non-Denominational` → `non-denominational.json`
- `Pentecostal / Charismatic` → `pentecostal-charismatic.json`

## Slug collisions

Four collisions caught during the V7.0.3 build and merged into single shards:

| Slug | Merged from |
|------|-------------|
| `non-denominational` | "Non-Denominational" + "Non-denominational" |
| `non-denominational-bible` | "Non-Denominational / Bible" + "Non-denominational Bible" |
| `pentecostal-charismatic` | "Pentecostal / Charismatic" + "Pentecostal/Charismatic" |
| `presbyterian-reformed` | "Presbyterian / Reformed" + "Presbyterian (Reformed)" |

If you need the original family-name distinction, read each record's `denomination_family` field directly.

## Rebuilding

```bash
python3 scripts/build_denomination_shards.py
```

Idempotent. Run after any `churches.json` change to keep shards in sync. The build script overwrites all shards in place.

## When to use these vs. state shards

| Question | Shard to fetch |
|----------|----------------|
| "Show me PCA churches in this state" | state shard + filter `denomination_family.startsWith("Presbyterian (PCA)")` |
| "Show me all SBC churches nationwide" | `southern-baptist-sbc.json` (21 MB) |
| "Show me all PCA churches nationwide" | `pca.json` + `presbyterian-pca.json` (need both — different slugs) |
| "What networks does this church belong to?" | Read the source record's `cross_listed_in` field |
| "How many Reformed-Baptist churches per state?" | `reformed-baptist.json` and group by `state` field |

## When to keep using `churches.json`

Cross-cutting analyses, dedup, bulk enrichment workflows — anything that needs the full corpus. The shards are display-path optimization, not a source-of-truth replacement.

## SBC shard size note

`southern-baptist-sbc.json` is 21 MB. This is the result of the V6.0.x SBC bulk-load (~14,649 records imported via the SBC.net per-church scrape). It's still 3× smaller than the 58 MB monolith for SBC-only consumers, but if it grows further a future split by `state` (`southern-baptist-sbc-tx.json`, etc.) is the natural next step.
