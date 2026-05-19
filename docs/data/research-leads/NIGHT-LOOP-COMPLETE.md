# Overnight Enrichment Loop — Complete (2026-05-19)

The recurring 10-minute enrichment loop (cron `14e4e771`) ran from
**03:08 UTC** (11:08 PM EDT Mon) through **09:14 UTC** (5:14 AM EDT Tue),
covering 17 rounds of pastor live-fetch enrichment plus interspersed
MOOP rubric audits.

## Final state (commit `bd901ab57`)

| | Start of loop | End of loop |
|---|---:|---:|
| Total churches | 13,969 | 13,969 |
| needs_review | 5,260 | **4,244** |
| Real pastors | 7,815 | **~8,800** |
| green | 4,331 | 4,330 |
| yellow | 8,175 | ~7,800 |
| red | 774 | ~960 |
| black | 276 | 276 |

**1,016 needs_review records cleared by loops** (-19.3%).

## Why we stopped

The "eligible pool" (records with placeholder pastor + working website + not yet attempted) is now **0**. The remaining 4,244 needs_review records fall into:

- **200_no_pastor_found** (~3,300): live websites where pastor name is rendered via JavaScript (Squarespace/Wix/React), in image alt-text, or buried in PDFs. Plain HTML fetch can't extract these — would need a headless-browser pass.
- **No website / non-http URL** (~700): records with empty website field, "verify" placeholder, Facebook-only, or other non-resolvable URL.
- **Various other patterns** (~244): legacy quality flags (IFB-BBFI sweep, AOG-WEST sweep), USMB defaults, etc.

## Quality stats per round

17 rounds of 3 parallel agents × 100 records each (some short-batched to 58 at the end). Total ~5,000 live-fetch attempts. Average ~25% pastor-found hit rate. Best batch: R5-B at 45/100. Worst: R9-A and R10-A at 10-16/100 (JS-heavy SPAs).

## MOOP rubric enforcement

- 39 additional female senior-pastor records flagged RED across the night (compounding the original 20 from Phase 6)
- 0 new prosperity-gospel BLACK flags (already exhaustive after the initial named-pastor sweep)
- ~600 broken-website downgrades from red flags (sites returned 404/timeout/SSL-error/parked)

## What's next for these 4,244 records

**Headless-browser enrichment pass** would crack the 3,300 200_no_pastor_found bucket. Tools: Playwright or Puppeteer rendering each page before scraping. Estimated 60-70% additional yield.

**Manual research** for the ~700 no-website records — many can be found via Google search or denominational directories.

**Quality flag deprecation** for the legacy ~244 (the IFB-BBFI and AOG-WEST sweeps from earlier rounds) — these have been live for months and probably can be either re-researched or de-flagged.
