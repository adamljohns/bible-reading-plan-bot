# Phase 6 — Network Lead Promotion (2026-05-18 evening, autonomous 3-hr block)

Adam's directive: "those other networks include churches I don't have in my directory and I do in fact want those churches in my directory; I just want to make sure I'm not creating duplicates."

The 9,067 Phase 2 + Phase 3 research leads queued from earlier in the session became the actual work-pool of Phase 6. The goal was to selectively promote them into MOOP records with rigorous dedup (no duplicates), giving Adam comprehensive network-cross-referenced coverage.

## Phase 6 timeline (single-session)

| Sub-phase | Action | Net add | Cumulative |
|---|---|---:|---:|
| Phase 6a | Trinity Foundation + SGC + Acts 29 + Pillar full-add | +912 | 8,502 |
| Phase 6b | Phase 3 speaker home-churches promoted (39 unique) | +39 | 8,541 |
| Phase 6c | TGC Church Directory bulk-add | +865 | 9,406 |
| Phase 6d | 9Marks Church-Search bulk-add | +4,542 | 13,948 |
| Phase 6e | Regenerate 6,554 per-church HTML pages + sitemap | (no church count change) | 13,948 |
| Phase 6f | Live-fetch pastor enrichment (10 parallel agents × 50 records) | (quality boost, no add) | 13,948 |

**Final directory: 13,948 churches (was 7,400 at Phase 1 start — +6,548 net across the day's work).**

## Dedup methodology

Each lead went through `scripts/dedup-and-prep-leads.js` against the LIVE churches.json:
1. Website-domain canonical match (highest confidence)
2. Phone number match (when present)
3. Name + city + state precise match (denomination-family guarded — rejects Pentecostal/Catholic vs Reformed-network collisions)
4. Name + state fuzzy (uniquely-resolvable only, denom-guarded)

Pre-add audit on the 6 lead pools:

| Network | Leads in pool | Safe to add | Newly matched (dup) | Skipped (no data) |
|---|---:|---:|---:|---:|
| Trinity Foundation | 47 | 34 | 0 | 13 |
| SGC | 62 | 44 | 0 | 18 |
| Acts 29 | 486 | 387 | 0 | 99 |
| Pillar | 538 | 461 | 0 | 77 |
| TGC-CN | 970 | 964 | 6 | 0 |
| 9Marks | 5,693 | 5,498 | 53 | 142 |
| **Total** | **7,796** | **7,388** | **59** | **349** |

After the integrate's own second-pass dedup (which catches cross-network domain overlap as additional tags rather than new records), final adds were lower than the safe-pool counts — and that's correct: when an Acts 29 record was added, then Pillar's lead with the same website domain became a tag-only operation rather than a duplicate add.

## Quality calibration

Vetted-network records (Trinity / SGC / Acts 29 / Pillar — formal membership + doctrinal vetting):
- Default green scoring (10 dimensions)
- `needs_review: true` set ONLY when pastor is missing in the source scrape
- `overall_label` cites the specific network's vetting standard

Self-listing records (9Marks Church-Search, TGC Directory):
- Default **yellow** scoring (10 dimensions) — appropriate epistemic posture since neither network individually vets entries
- `needs_review: true` for nearly all (no pastor data from source)
- `overall_label` explicitly notes "self-listing, not vetted"

This calibration means a user filtering the directory for "green-rated churches" sees a curated set unchanged by Phase 6; a user filtering for "any cross-listed church" sees the full 7,474+ list.

## Phase 6f — Live-fetch pastor enrichment (in flight as of commit)

10 parallel agents are live-fetching 50 9Marks records each (500 total). Each agent visits the church website's /about /staff /leaders /pastors pages, extracts the senior/lead pastor name, and reports website health (200 / 404 / timeout / not_a_church). Results merge via `scripts/merge-pastor-enrichments.js`:

- Real pastor found → `pastor` field set, `enrichment_sources` appended, `needs_review` cleared if that was the sole flag
- Broken website (404 / timeout / SSL / not_a_church) → `overall_rating` downgraded to red, `needs_review` retained
- No pastor parseable but site alive → note appended, `needs_review` retained

This is the start of the post-bulk-add quality-pass. Subsequent passes can extend the same pattern to TGC, Acts 29 (the 1.3% missing pastor), Pillar (the 0% rare missing), etc.

## What's next (for future sessions)

1. Apply current Phase 6f enrichments → commit.
2. Continue pastor-enrichment in larger waves for the remaining ~5,000 9Marks records.
3. Denomination-detection pass — the 9Marks/TGC adds defaulted to "Baptist" or "Reformed Evangelical" but reality is more varied (Presbyterian, Anglican, Congregational, etc.).
4. Signatory check pass — all Phase 6 adds have empty signatory arrays; need to cross-reference against the 7 canonical ledgers (Nashville 2017, Dallas 2018, Revoice 2018-2026, Warhurst 2020, Letter of Lament 2025, AMR 2026, CBE Egalitarian 2026).
5. Continue selective curation of remaining 9,067 - 6,358 ≈ 2,700 leads still in research-leads/.
6. Bulk-merge the 70 remaining duplicate sets surfaced in Phase 5 audit.
7. Re-research the 49 IFB-BBFI + AOG-WEST quality-flagged churches (R-23 + R-26).
