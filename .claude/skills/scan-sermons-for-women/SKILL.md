---
name: scan-sermons-for-women
description: Scan a church's archived sermon page for evidence of women preaching, as input to MOOP's complementarian doctrinal vetting. Use whenever the user asks to "check if [church] has women preaching", "scan sermon archives for women", "look for egalitarian drift in [church or scope]", "audit pulpit composition", or wants to verify a green-rated church has not quietly started hosting women in the pulpit. Operates over the quick_links 'Sermons' chip URL when present; scrapes the page HTML for preacher attributions; extracts names; classifies by first-name gender against a US-census-derived dataset; flags hits for human review. Triggers in the bible-reading-plan-bot repo or when the user references a church's preaching ministry.
---

# Scan Sermons For Women

A complementarian-vetting helper. Per MOOP rubric, a female senior pastor downgrades a church to RED minimum; the same posture applies to a church that regularly hosts women in the pulpit even without a female senior pastor on staff. This skill scans sermon archive pages for evidence of women preaching so the rating team can investigate and adjust.

## What this skill IS

- A heuristic that scrapes a sermon archive's HTML and surfaces apparent female preacher names for human review
- A way to scale doctrinal-drift detection from "check one church manually" to "scan an N-church cohort overnight"
- A tool that always produces a REVIEW QUEUE, not an automated rating change

## What this skill is NOT

- An automated rating-change pipeline; every flag needs human confirmation before the church's `overall_rating` moves
- A reliable detector for JavaScript-rendered sermon CMSes (Squarespace, Wix, custom video platforms); those archives often need a headless browser pass that this skill does not provide
- A judgment about whether a guest woman preacher equals an egalitarian church; the rating team makes that theological call

## Why this matters doctrinally

Many self-identified "complementarian" churches have quietly drifted, hosting women preachers periodically or normalizing female pastoral teaching. The sermon archive is the public record of who actually steps into the pulpit, regardless of what the website's "what we believe" page says. This skill turns that public record into a queryable signal.

## Workflow

### 1. Pick the scope

Churches in scope must have a `quick_links` entry labeled "Sermons"; that gives the scraper a starting URL. Run `directory-pulse` first to confirm how many churches in the requested scope have a Sermons chip; that is the achievable universe for this pass.

Suggested scopes:
- A single church the user named: `--church <slug>`
- A cohort: `--state VA` or `--network 9marks` or `--rating green`
- All directory-wide: `--all` (slow; use the autopilot pattern for this)

### 2. Run the scanner

```bash
node .claude/skills/scan-sermons-for-women/scripts/scan-archive.js --state VA --count 50 --jsonl /tmp/sermon-scan.jsonl
```

The scanner reads each in-scope church's Sermons URL, fetches the HTML, extracts likely preacher names via three patterns (a title-prefix pattern, a "Speaker:" / "Preached by" pattern, and a names-near-sermon-titles heuristic), classifies each extracted first name against the bundled female / male / unisex dataset, and writes one JSONL record per church.

Each record looks like:

```json
{
  "id": "first-baptist-XYZ",
  "archive_url": "https://example.com/sermons",
  "scanned_at": "2026-05-28T22:50:00Z",
  "name_hits": [
    {"name": "Mary Lou Smith", "first": "Mary", "title": "Pastor", "context": "Pastor Mary Lou Smith preached on...", "gender": "F", "confidence": "high"},
    {"name": "Chris Jones", "first": "Chris", "title": "Rev.", "context": "...message by Rev. Chris Jones", "gender": "U", "confidence": "uncertain"}
  ],
  "warning": null
}
```

`warning` is set to one of `"likely-js-rendered"`, `"empty-archive"`, or `"fetch-failed"` when the scrape did not produce parseable preacher text.

### 3. Filter the review queue

```bash
bash .claude/skills/scan-sermons-for-women/scripts/review.sh /tmp/sermon-scan.jsonl > /tmp/sermon-review-queue.txt
```

`review.sh` filters out churches with zero name hits, sorts by signal strength (number of female-high hits descending), and emits a human-readable review queue. Each entry shows the church name, slug, archive URL, and each name hit with context so the rating team can click through and confirm.

### 4. Human review

For each entry in the queue, the rating team:

1. Visits the archive_url
2. Confirms the named individual really preached (vs. led music, gave announcements, etc.)
3. Confirms the gender classification (especially for unisex names)
4. If the church regularly hosts women in the pulpit, downgrade to YELLOW or RED per the existing rating playbook (see `CLAUDE.md` at repo root for the threshold rules)
5. Updates `score_notes`, `assessment`, and `overall_rating` via the existing edit pattern; the commit message should reference the sermon-scan evidence

### 5. Re-scan periodically

The drift signal is real but slow-moving. A monthly re-scan of green-rated churches is a reasonable cadence; weekly is overkill, quarterly is too sparse.

## Heuristic caveats

These are limitations the user should know about before trusting any single hit:

- **Unisex first names** (Pat, Chris, Taylor, Jordan, Casey, Sam, Robin, Terry, Jamie, Alex) produce `confidence: "uncertain"`. Do not act on these without confirming via photo or pronoun in the page text.
- **Title context** sharpens signal: "Pastor Mary" reads stronger than just "Mary" because most complementarian churches reserve "Pastor" for male leadership. The scanner uses title presence as a boost.
- **Guest preachers** (visiting missionaries, parachurch speakers) may be female without representing an egalitarian-drift pattern. Look for repetition across the archive; a one-off guest is different from a regular rotation.
- **Family member acknowledgments** can trigger false positives ("Pastor John was joined by his wife Sarah") — the scanner extracts both names. Read the context field.
- **JS-rendered archives** are not visible to the HTML scraper. The output's `warning` field flags these so the user knows to check manually.
- **Catholic / Anglican / mainline naming conventions** differ ("Mother", "Sister", "Father") — the scanner uses these as gender-signal hints but does not classify them as preachers in the Reformed-evangelical sense.

## Data sources

- `data/first-names-gender.json` — first-name → gender map seeded from US Social Security baby-name records (top 500 male, top 500 female, plus a unisex list). This file lives alongside the skill; expand it if you find common preacher names being misclassified.
- `data/preacher-titles.json` — title strings the scanner watches for ("Pastor", "Rev.", "Dr.", "Bro.", "Sis.", "Mother", "Father", "Sister", "Brother", "Elder", "Minister")
