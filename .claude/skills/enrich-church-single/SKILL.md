---
name: enrich-church-single
description: Targeted enrichment of one specific church record in the MOOP Church Directory. Use whenever the user references a single church profile and asks to fix, enrich, audit, or enhance it ("Faith Baptist looks bare", "fix the Memorial Baptist page", "enrich First Pres Fredericksburg", "this church has no logo / no pastor / no sources", "audit https://usmcmin.org/churches/<slug>.html"). Identifies what is missing on the record (real pastor, exterior photo, logo, sources, geocode, quick links, social URLs), runs the targeted scrapers for the missing pieces only, regenerates the per-church page, and pushes. Faster than spinning up a full autopilot when the user has identified a specific page that needs help. Triggers in the bible-reading-plan-bot repo.
---

# Enrich Church Single

The fastest way to fix a specific church profile that the user has noticed is bare or wrong. Identifies what is missing on the one record, runs only the scrapers needed for the gaps, regenerates that page, and pushes. Used when the user has clicked into a per-church page and reported a specific issue, or wants to fully enrich one congregation before moving on.

## When to use this

- User pastes or names a specific church and asks for help on it (slug, URL, or church name + city)
- User says a per-church profile is "bare", "missing photos", "no sources", "no logo", or any single-record complaint
- Before showing a church to a stakeholder or featuring it in a blog post; one-record polish pass

## When NOT to use this

- Bulk enrichment across a state / network / nationwide (use `autopilot-launch` or the existing `church-directory-enrichment` skill instead)
- Adding new churches to the directory (use `church-directory-enrichment`)
- Theological re-rating or signature cross-reference work (use `church-directory-enrichment`)

## Workflow

### 1. Resolve the church record

Accept any of: slug, church name, name + city, or per-church URL.

```bash
bash .claude/skills/enrich-church-single/scripts/find.sh "Faith Baptist Fredericksburg"
# or
bash .claude/skills/enrich-church-single/scripts/find.sh faith-baptist-church-fredericksburg
```

The helper prints the matching record's id, name, address, website, pastor, and a "gaps" list (what fields are missing or look like placeholders).

If there is no single unambiguous match, the helper lists candidates; ask the user which one before continuing.

### 2. Audit gaps and decide what to enrich

Look at the `gaps` list from step 1. Possible gap categories and the appropriate scraper for each:

| Gap | Scraper / fix |
| --- | --- |
| `pastor` missing or placeholder | `node scripts/scrape-church-pastors.js --state <STATE> --count 1` (filter helps) |
| `image_url` (hero photo) missing | `node scripts/scrape-church-images.js --state <STATE> --count 1` |
| `image_thumb` (logo) missing | Same scraper as image_url — apple-touch-icon is the source |
| `latitude`/`longitude` missing | `scripts/geocode-va.js --state <STATE>` for batch; for single record, hit Census batch via Node inline |
| `enrichment_sources` empty | Backfill with website + Google Maps URL + cross_listed_in network URLs (see backfill helper) |
| `quick_links` empty | `node scripts/scrape-church-quicklinks.js --state <STATE> --count 1` |
| `facebook` / `youtube` missing | WebSearch for the church's social presence; manual update |

For single-record runs of the state-scoped scrapers, prefer setting `--state` to the church's actual state and `--count 1` so the Fredericksburg-first sort hits the target. If the church is not in Fredericksburg, edit churches.json to temporarily flag it OR use a custom one-shot script.

### 3. Run the targeted enrichment

Pick the minimum set of scrapers that cover the gaps from step 2. For each, the JSONL files at `/tmp/<scraper>-scrapes.jsonl` resume cleanly; the scraper will skip if this church already has an entry.

After each scraper run, call the matching merge script:

```bash
node scripts/merge-pastor-scrapes.js
node scripts/merge-image-scrapes.js
node scripts/merge-church-quicklinks.js
node scripts/merge-sbc-detail.js
```

### 4. Backfill `enrichment_sources` if needed

If `enrichment_sources` is the gap, do not run a scraper; run the inline backfill (the Fredericksburg pattern from 2026-05-28):

```bash
node .claude/skills/enrich-church-single/scripts/backfill-sources.js <church-id>
```

This writes the church's own website + Google Maps URL (from lat/lng if present, else from address) + each cross_listed_in network's directory URL into `enrichment_sources`.

### 5. Regenerate the page and verify

```bash
node generate-church-pages.js | tail -3
# Sanity check the rendered page contains what we just added:
grep -E 'church-logo|quick-link|network-chip|enrichment_sources' docs/churches/<slug>.html | head -10
```

### 6. Commit and push

Pull-rebase first, then commit with a descriptive single-record subject:

```bash
git pull --rebase --autostash
git add docs/data/churches.json docs/churches/<slug>.html
git commit -m "Enrich <Church Name> (<City>, <ST>): <comma-list of gaps filled>"
git push
```

Use the heredoc commit-message pattern if the body is multi-line. Always include the church name and city in the subject so `git log` is greppable later.

### 7. Show the user

Reply with the live URL and a one-line summary of what was added. If a scraper found nothing (some sites do not expose OG / apple-touch-icon / standard paths), say so explicitly rather than hand-waving — the user reads the page directly and will catch the gap.

## Gotchas

- **Autopilots can race you.** If a full-state autopilot is running, your single-record write can be clobbered. Check `pgrep -fl autopilot` first; if hot, pause briefly or push with retry.
- **Slug != address.** A church can have a slug like `faith-baptist-church-fredericksburg` but its actual street address in churches.json is in Spotsylvania; match by id (slug), not by address.
- **Do not invent data.** If the scraper returns no real pastor, leave the field as is and tell the user; do not fill placeholder values. Same for photos — the OG-less site case is real and common.
- **Female senior pastor → RED minimum.** If your enrichment surfaces a female senior pastor on a previously-green church, the rating MUST be downgraded along with the enrichment commit; mention it in the commit body.
