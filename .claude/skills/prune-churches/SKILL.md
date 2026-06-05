---
name: prune-churches
description: Safely remove PHANTOM (non-existent) or DUPLICATE church records from the MOOP Church Directory (docs/data/churches.json), keeping every derived artifact in sync. Use whenever the user wants to delete/remove a church that doesn't exist, prune phantom campuses of a multisite church, or merge/dedup duplicate records — e.g. "this campus isn't real", "X has two entries", "dedup the directory", "remove the fake/ghost churches", "that church closed", "CCV doesn't have a Goodyear campus". Handles verification against the org's official campus/location list, the phantom/duplicate tells, the format-preserving surgical edits across churches.json + by-state + by-denomination-family shards + sitemap-churches.xml + orphan HTML, the total_churches resync, and the race-safe commit/rebase/push against the geocode autopilot. The counterpart to the add-network-or-denomination / enrich skills. Triggers in the bible-reading-plan-bot repo.
---

# Prune Churches (phantom + duplicate removal)

The end-to-end workflow for **removing** church records and keeping the directory's derived
artifacts consistent. Proven 2026-06-02 removing four bad CCV (Christ's Church of the Valley)
records — two phantom campuses (Goodyear, San Tan Valley), one more phantom (Gilbert, where
CCV only owned land), and one duplicate (a bare "Peoria, AZ" stub of the real flagship).

The hard part isn't deleting from `churches.json` — it's that **four other artifacts also carry
the record and none auto-update**: the per-state shard, the per-denomination shard,
`sitemap-churches.xml`, and the pre-generated per-church HTML page. Leaving any of them is how
phantoms linger in the live per-state / per-network views.

## When to use this skill

- A church/campus **does not exist** (no real address, not on the org's official site).
- **Duplicate** records for the same church (e.g. a full-address record + a city-only stub).
- The user says "remove / delete / get rid of" a church, "dedup", "this isn't real", "merge these two".

## When NOT to use this skill

- **Adding** churches → `enrich-churches`, `add-network-or-denomination`, `enrich-church-single`.
- **Re-rating** a real church (gender/denominational downgrade) → edit `churches.json` scores directly.
- A real church that **renamed or merged** into another real church → don't delete; use a
  `successor: "<new-slug>"` + `predecessor_ids: [...]` pointer (CLAUDE.md "Renamed/merged churches").
- Bulk cleanup of `state: "unknown"` → that's an enrichment/parse pass, not a prune.

## Step 1 — VERIFY it's really phantom/duplicate (never delete on a hunch)

CLAUDE.md: deletion needs a **verification trail in the commit**. Confirm before removing.

**Phantom tells** (any one is a flag; several together is conclusive):
- `address` is bare `"City, ST"` with **no street number**.
- `website` is an org root (e.g. `ccv.church`) and `facebook` is a generic network page
  (`ccvonline`) — i.e. not campus-specific.
- An `[agent-research] REVIEW:` line already sits in `enrichment_notes`, or `needs_review: true`.

**For a multisite church** (megachurch with campuses): fetch its **official locations page**
(e.g. `WebFetch ccv.church/where-we-are`) and treat that as ground truth. Any directory record
for a campus *not* on that list, with a city-only address, is a phantom. Cross-check Wikipedia /
Yelp / FaithStreet if the official page is JS-heavy.

**For duplicates:** same name + city, two records — keep the one with a real **street address**
(the "gold"), drop the bare city-only stub. Confirm the keeper is the real one first.

List every related record before acting:
```bash
python3 -c "import json; d=json.load(open('docs/data/churches.json'));
[print(repr(str(c['id'])),'|',c.get('name'),'|',c.get('address')) for c in d['churches']
 if str(c.get('id','')).startswith('PREFIX')]"   # e.g. PREFIX='ccv-'
```

## Step 2 — Remove across all artifacts (one command)

```bash
# Preview first:
bash .claude/skills/prune-churches/scripts/prune.sh --dry-run <id> [<id> ...]
# Then apply:
bash .claude/skills/prune-churches/scripts/prune.sh <id> [<id> ...]
```

This edits, format-preserving + atomically: `churches.json` (Node — Python can't reproduce its
byte layout; re-syncs `total_churches`), every `by-state/` and `by-denomination-family/` shard
that contains the id (updates `record_count`), and `sitemap-churches.xml` (drops the `<url>`
blocks); then removes each orphan `docs/churches/<id>.html`. Each JSON edit is **round-trip
guarded** — if the serializer wouldn't reproduce a file byte-for-byte, that file is skipped
rather than mass-reformatted. It does **not** commit, and it does **not** run `git add`.

If the script reports an id is in `directory-map-points.json` (a geocoded church), also run
`node scripts/build-directory-map.js` to rebuild the map.

## Step 3 — Review the diff is small and scoped

```bash
git diff --numstat -- docs/    # each record ≈ ~100 churches.json lines + ~80 per shard; sitemap = 6 lines/record
git diff -- docs/data/churches.json | grep -E '^\+' | grep -v '"'   # sanity: only total_churches + braces added
```
A **large** diff (thousands of lines) means a reformat or that you raced the autopilot — stop and investigate.

## Step 4 — Commit + push (race-safe against the autopilot)

An autopilot commits `churches.json` every ~20 min, so stage **only** the files prune.sh listed
as `TOUCHED` plus the removed HTML — never `git add -A docs/` (it would sweep in autopilot churn).

```bash
git add docs/data/churches.json docs/data/churches/by-state/<st>.json \
        docs/data/churches/by-denomination-family/<fam>.json docs/sitemap-churches.xml docs/churches/
git commit -m "Remove N phantom/duplicate church records (...)

<verification trail: official-list URL checked, phantom tells, what each id was, what covers the area>
Total: <before> -> <after>.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
git pull --rebase origin main && git push origin main
git merge-base --is-ancestor HEAD origin/main && echo "✓ durable on origin"
```
A direct push may be *rejected* as "already at X" while your commit still rides to origin on the
autopilot's push — that's why the `merge-base --is-ancestor` check is the real confirmation.

## Common gotchas

- **`churches.json` is Node-serialized; the shards are Python-serialized.** Edit churches.json
  with Node (`JSON.stringify(d,null,2)+'\n'`) and the shards with Python
  (`json.dumps(indent=2, ensure_ascii=False)`, **no** trailing newline). The scripts already do
  this; don't "simplify" to one language — Python reformats churches.json (float layout differs).
- **`generate-church-pages.js` does NOT delete orphans.** A removed record's HTML lingers until
  you `rm` it — prune.sh handles this.
- **`total_churches` drives the live footer.** `churches.html` reads it before the array length,
  so it must equal `churches.length` after a removal (prune-churches.js re-syncs it).
- **Don't run `bin/generate_sitemap.py` for a churches-only change** — it's site-wide and also
  rebuilds the dictionary/lexicon/chapter sitemaps. `build-sitemap-churches.js` reorders the file
  (array order vs the file's plain-id sort). For pruning, the surgical block removal here is right.
- **Phantom ≠ merge.** A campus that never existed gets **deleted** with a verification trail. A
  real church that became another real church gets `successor`/`predecessor_ids`, not deletion.
