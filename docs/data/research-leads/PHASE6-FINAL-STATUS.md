# Phase 6 Final Status — 2026-05-18 ~22:00 ET

Adam's 3-hour autonomous block. Mission: aggressively promote network-research leads into MOOP records (with rigorous dedup) and enrich the bulk-added records' quality (pastor names via live-fetch + social media + MOOP rubric flagging).

## Headline numbers

| Metric | Phase 1 start | Phase 6 start | Phase 6 end (~22:00) | Delta |
|---|---:|---:|---:|---:|
| Total churches | 7,400 | 7,590 | 13,948 | **+6,548** |
| Real pastors | ~7,400 | 7,466 | 7,686 | +220 (live-fetched) |
| Facebook URLs | — | 4,833 | 4,933+ | +100 |
| YouTube channels | — | 1,298 | 1,805+ | +507 |
| Cross-listed (any network) | 0 | 1,654 | 7,557+ | +5,903 |
| Multi-network listings | 0 | 430 | 1,256+ | +826 |
| Notable_attendees | 87 | 124 | 124+ | +37 (Phase 3 speakers) |

## Phase 6 sub-phases delivered

| Sub-phase | Action | Commits |
|---|---|---|
| 6a | Trinity + SGC + Acts 29 + Pillar full-add | 99044f573 |
| 6b+6c | Speaker home-churches + TGC bulk-add | 809947c78 |
| 6d | 9Marks bulk-add (+4,542 new) | faca18f7a |
| 6e | Per-church HTML pages + sitemap regen | 09313b427 |
| 6f-merge-1..4 | 9Marks pastor enrichment (314 pastors) | e273c137c, ca75168d7, e1c2efa9c, 5beace11f |
| 6f-WaveA | TGC pastor enrichment (76 pastors) | e74f26157 |
| 6f-WaveB | FB×2 + YT-1 skill enrichment | 78f428330, 586803e74 |
| 6f-WaveC | 9Marks batches 16-19 (88 pastors) | 7977fc7f7 |
| 6f-WaveD | 9Marks batches 20, 22, 23, 24 (56 pastors) | a8e856cb2 |
| MOOP rubric | Female pastor RED (20), prosperity-gospel BLACK (10) | e16fe5fd8, 70e6214db |
| Quality | Denom auto-detect (268), vetted-intl needs_review clear (244) | f18565770, 367ce1380 |

## MOOP rubric enforcement

**Auto-flagged via this session's pattern detection:**
- 20 records → RED for female senior pastor (high-confidence first name only; unisex names like Ashley/Kelly/Lynn excluded to avoid false positives)
- 10 records → BLACK for prosperity-gospel pastor (Steven Furtick × 6 Elevation campuses; T.D. Jakes / Potter's House; Joyce Meyer)
- 0 records auto-flagged for LGBTQ-affirming (would require denomination-level rubric pass)

**Manual review queue surfaced:**
- "Bishop" / "Apostle" / "Prophet" title patterns on 30+ records (mostly false positives: ACNA legitimate bishop titles, surname Bishop)
- 7 churches with female-name patterns NOT auto-flagged (unisex names)
- Black-Baptist NBC churches with "Bishop" titles (Sharon Baptist Philadelphia, FBC Frankfort) — legitimate within their tradition

## Enrichment quality data

Across 1,100+ 9Marks records live-fetched for pastor names:
- 314 pastor names successfully extracted (~28% hit rate)
- 171 broken websites detected and downgraded to red
- ~600 alive sites where pastor isn't parseable (JS-rendered Squarespace/Wix/Webflow staff pages)

Across 200 TGC records:
- 76 pastors extracted (38% hit rate — higher than 9Marks because TGC churches tend to have better-equipped sites)
- 18 broken websites flagged

## Outstanding work for future sessions

1. **Continue pastor live-fetch waves** — ~2,500 9Marks records still placeholder (estimated 700 more pastors recoverable at current hit rate)
2. **TGC pastor batches 4+** — 765 TGC records still need pastor enrichment
3. **Female pastor scan with unisex names** — manual review needed for Ashley/Kelly/Lynn/Tracy/Chris/Jamie/Jordan first-names
4. **LGBTQ-affirming denomination pass** — flag PCUSA, UMC, ELCA, ECUSA records as RED minimum
5. **Cleanup-7**: Phase 5 surfaced 74 real-dupe groups; only 4 named sets resolved in Phase 5. ~70 more bulk-merge candidates.
6. **Per-church HTML page regen** — already done for all 13,948. Sitemap-churches.xml has all 13,948.
7. **Pastor "Unknown" cleanup** — 431 legacy records with literal "Unknown" pastor need re-research.
8. **Signatory cross-reference pass** — all Phase 6 adds have empty signatories arrays. The 7 ledgers (Nashville, Dallas, Revoice, Warhurst, Letter of Lament, AMR 2026, CBE Egalitarian 2026) need scan against the new 6,358 records.
9. **9,067 research-leads inventory** — Phase 2 + Phase 3 leads files now mostly consumed; some "non-US" + "non-website" subsets remain.

## Repository final state

Last commit: a8e856cb2 (Phase 6f Wave D)

```
docs/data/churches.json           13,948 records, 43+ MB
docs/data/research-leads/         9,067 historical + PHASE5-TRIAGE + PHASE6-NARRATIVE
docs/directory-networks.html     7,557+ cross-listed churches with filter UI
docs/sitemap-churches.xml         13,948 URLs
docs/churches/<id>.html          13,948 per-church detail pages
scripts/integrate-network-matches.js  (with denom-family guard)
scripts/integrate-speakers.js         (with dedup-augment)
scripts/build-directory-networks.js
scripts/build-sitemap-churches.js     (new)
scripts/merge-pastor-enrichments.js
scripts/merge-dupes.js
scripts/dedup-and-prep-leads.js       (new)
scripts/promote-speaker-churches.js   (new)
scripts/fix-denom-from-name.js        (new)
PROJECT-NETWORKS-SPEAKERS.md          (5-phase plan, 100% / 38 of 38)
```
