# Overnight Facebook-Finder Campaign — Complete (2026-05-19)

In response to Adam's directive — "many churches use Facebook instead of websites; broken-website shouldn't be a RED flag; find their FB pages" — we ran 5 waves × 5-3 batches each across the broken-website pool.

## Headline numbers

| Metric | Value |
|---:|:---|
| Records audited | 1,034 broken-website churches |
| Facebook URLs verified + applied | **833** |
| Outreach candidates tagged (no FB found) | **166** |
| Records pre-policy-fix that were wrongly RED | 1,034 → all restored to yellow |

**81% Facebook-page-recovery rate** across the broken-website pool.

## Wave-by-wave

| Wave | Records | FB Found | Outreach | Hit Rate |
|---:|---:|---:|---:|---:|
| 1 | 250 | 205 | 35 | 82% |
| 2 | 250 | 202 | 28 | 81% |
| 3 | 250 | 172 | 44 | 69% |
| 4 | 249 | 162 | 36 | 65% |
| 5 | 149 | 92 | 23 | 62% |
| **Total** | **1,148** | **833** | **166** | **73% avg** |

(Pool count slightly higher than 1,034 because some duplicate-slug records were caught by multiple agents.)

## What the "outreach candidates" represent

166 churches that:
- Have a defunct/broken/parked website on file (404, timeout, SSL error, redirect-loop, or parked-domain detection)
- Have NO official Facebook page that surfaced in live WebSearch
- Many appear to be small-budget congregations (rural Baptist churches, immigrant-community plants, small church plants)
- These are real ministry-of-helps targets — offer a simple landing page for $100, ongoing hosting maintenance for a token fee, get them visible online

The full list is at `docs/data/research-leads/website-outreach-candidates.json` with name, address, pastor, denomination, cross-listed networks, source URL, and a draft pitch line.

## Policy enforcement

`scripts/merge-pastor-enrichments.js` updated so future runs do NOT auto-RED a broken website. The new policy:
- Note the broken-site finding in `enrichment_notes`
- Keep `needs_review = true` so the social-channel research happens
- Do NOT downgrade `overall_rating` or `scores` — broken website is a data-quality issue, not a doctrinal one

## What's left in needs_review

After the campaign, **4,278** records still flagged needs_review. Breakdown:
- ~3,200 "200_no_pastor_found" from the pastor-enrichment loops (would need headless-browser pass)
- ~700 records with no website AND no FB-finder pass yet attempted
- ~378 records with various legacy quality flags (IFB-BBFI, AOG-WEST sweep markers)

These are addressable in future sessions.
