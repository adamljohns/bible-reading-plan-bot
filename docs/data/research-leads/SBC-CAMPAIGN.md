# SBC Bulk-Load Campaign

Goal: every active SBC congregation in the MOOP Church Directory before the
SBC Annual Meeting in June 2026.

## State of play (2026-05-20)

- **SBC.net universe (active sitemap):** 34,501 congregations across 35 sitemap shards
- **Already in directory:** 2,114 SBC-tagged + 2,198 fuzzy-name matches = ~4,300
- **Net-new TODO:** 32,267 URLs queued in `/tmp/sbc-todo.json`
- **Already scraped (test run):** 5 records as a pipeline test, merged into churches.json

## Time math

- SBC.net robots.txt requires 10-second crawl-delay. Our scraper uses 11s buffer.
- 32,267 URLs × 11s = **~99 hours** of single-threaded scraping
- At 8 hr/night for 28 nights = comfortably fits inside the 4-week window
- At 24 hr/day continuous = ~4.1 days

## Pipeline (4 stages, all scripts in `scripts/`)

```
┌─────────────────────────────────────┐
│ 1. sbc-fetch-sitemap.js             │  ~40s one-shot
│    → /tmp/sbc-all-urls.json         │  Pulls all 35 SBC sitemaps in one pass.
└─────────────────────────────────────┘  No crawl-delay needed for sitemap XML.
              │
              ▼
┌─────────────────────────────────────┐
│ 2. sbc-dedup.js                     │  ~1s
│    → /tmp/sbc-todo.json             │  Compares against churches.json. Drops
│    → /tmp/sbc-existing-matches.json │  exact slug + fuzzy name+state matches.
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ 3. sbc-scrape-batch.js              │  long-running, 11s/URL
│    --start N --count M              │  Crash-safe (.jsonl append). Resume-able.
│    --resume                         │  Outputs /tmp/sbc-scraped/batch-X-Y.jsonl
│    → /tmp/sbc-scraped/*.jsonl       │
│    → /tmp/sbc-scrape-progress.json  │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ 4. sbc-merge.js                     │  fast, idempotent
│    → docs/data/churches.json        │  Builds proper schema, dedups again,
└─────────────────────────────────────┘  bumps directory_updated stamp.
              │
              ▼
   generate-church-pages.js (existing)
   scripts/build-sitemap-churches.js (existing)
              │
              ▼
        commit + push
```

## How to run

### One-time setup (already done as of 2026-05-20)
```bash
node scripts/sbc-fetch-sitemap.js      # → 34,501 URLs
node scripts/sbc-dedup.js              # → 32,267 net-new TODO
```

### Daily scrape session
```bash
# Resume scraping from wherever you left off, batches of ~1000 per session
node scripts/sbc-scrape-batch.js --resume --count 1000

# Periodically merge scraped batches into churches.json
node scripts/sbc-merge.js

# When ready to publish a checkpoint:
node generate-church-pages.js                  # rebuild per-church HTML
node scripts/build-sitemap-churches.js         # update sitemap
git add docs/data/churches.json docs/churches/ docs/sitemap-churches.xml
git commit -m "SBC bulk-load: +N records (cumulative N/$32267)"
git push origin main
```

### Status check anytime
```bash
node scripts/sbc-status.js
```

## What gets imported (minimal schema)

Each new record carries:
- `id` / `slug` — SBC's own URL slug (preserves continuity)
- `name` — cleaned (HTML entities decoded, " – SBC Churches Directory" suffix stripped)
- `address` — "City, State ZIP"
- `pastor` — `"Verify on church website"` (no pastor data in sitemap)
- `denomination` — `"Baptist"`
- `denomination_family` — `"Southern Baptist (SBC)"`
- `cross_listed_in` — `["sbc"]`
- `overall_rating` — `"yellow"` (default; awaiting evaluation)
- `signatures_aggregate` — `"none"`
- `needs_review` — `true`
- `source_url` — original SBC.net URL
- `notes` — array including bulk-load date
- `engagement.researched_website` — `false`
- `scores` / `score_notes` / `assessment` — empty (so generate-church-pages.js renders cleanly)
- `_sbc_bulkload` — date stamp (so we can identify and re-enrich these later)

## Post-Convention enrichment plan

Once the 32K bulk-load is complete, the records are at **Tier A** (listed,
not evaluated). Subsequent passes move records up the tiers:

- **Tier B** — pastor extraction (web fetch + parse). Realistic target:
  60-70% of records, ~20,000 with pastor names.
- **Tier C** — full rubric evaluation. Slowest. Realistic target:
  3,000-5,000 records in the first 90 days post-Convention.

The bulk-load gives us the universe. The enrichment is what makes the
directory editorial.

## Polite scraping notes

- SBC.net robots.txt: 10s crawl-delay, sitemaps allowed
- Our User-Agent identifies us with a contact email so the SBC's webmaster
  can reach us if there's ever an issue: `MOOP-Church-Directory-Scraper/1.0
  (contact: bowandarrowstudiollc@gmail.com)`
- The scraper is single-threaded by design — no parallel requests
- If the SBC ever asks us to stop, we stop immediately. This is a directory
  built FOR the local church, not against it.
