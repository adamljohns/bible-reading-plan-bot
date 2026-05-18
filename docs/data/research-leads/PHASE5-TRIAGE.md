# Phase 5 — needs_review Triage Report (2026-05-18)

249 churches carry `needs_review: true`. Categorized by enrichment-note pattern:

| Bucket | Count | Priority | Action |
|---|---:|---|---|
| **IFB-BBFI quality-flag** (R-23 IFB sweep, agent admitted prior-knowledge fallback) | 27 | HIGH | Re-research each via live-fetch of bbfi.org listings + church website |
| **AOG-WEST quality-flag** (R-26 AoG sweep, same pattern) | 22 | HIGH | Re-research via aogwest.com + church websites |
| **Empty enrichment notes** | 15 | MEDIUM | Investigate origin; many may be very early skeleton records |
| **USMB self-listing default-yellow** (2026-05-16 sweep) | 10 | LOW | USMB is a vetted Mennonite Brethren conference — yellow default is conservative; could be elevated to green after individual verification |
| **Founders Phase 1 — no website surfaced** | 2 | LOW | Live-fetch the church name + state to find website |
| **Foursquare Hope Chapel Kaneohe address mismatch** | 1 | MEDIUM | Verify actual address |
| **All other / verbose notes** | 172 | varies | Individual review |

## Cleanup-6 dupe-set status (separate from needs_review)

74 real-dupe groups surfaced during the audit (74 groups / 75 redundant records). 4 named sets resolved in this Phase 5 commit:

| Dupe set | Status |
|---|---|
| Redeemer Presbyterian NYC (4 records) | Merged: 3 → 1 (main campus). East Side campus kept separate. |
| Highview Baptist Louisville (4 records) | Merged: 4 → 3 (empty-address dupe folded). Real multi-campus retained. |
| Christ Church Moscow ID (Doug Wilson; 3 records) | Merged: 3 → 1. False "PCA" tag corrected (church is CREC, not PCA). |
| Christ Covenant Matthews NC (Kevin DeYoung; 2 records) | Merged: 2 → 1 (record with full address kept). |

The remaining 70 dupe groups in `/tmp/phase5-real-dupes.json` are deferred to a follow-on cleanup pass (most are SBC-prefix duplicates from earlier sweeps that need bulk-merge logic).

## False-positive cross_listed_in tags removed

6 churches had Pentecostal/Charismatic/Assemblies-of-God denominations but were tagged into Reformed-evangelical networks (Founders / 9Marks / TGC / SGC / Pillar) due to over-aggressive name-normalization collisions. All 10 false tags removed:

- Stafford Church of God (5 tags)
- River of Life Jacksonville NC (1 tag)
- Valley Life AoG Tucson AZ (1 tag)
- Christ Church AoG Montclair NJ (1 tag)
- Victory Church AoG Lancaster PA (1 tag)
- New City AoG Dover DE (1 tag)

Prevention: `scripts/integrate-network-matches.js` now carries an `INCOMPATIBLE_DENOM_PATTERN` guard that rejects name+state matches against denominationally-incompatible MOOP records. Website-domain matches are still trusted as reliable.

## Open follow-on work

- Re-research the 49 IFB-BBFI + AOG-WEST quality-flagged churches with live fetching
- Bulk-merge the remaining 70 dupe groups (SBC-prefix variants from earlier sweeps)
- Investigate the 15 empty-notes records (likely very-early skeletons)
- Selective curation pass on the 7,796 Phase 2 network-research-leads + 136 Phase 3 speaker-home-church-leads
