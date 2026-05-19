# Phase 5b — Bulk Auto-Merge of Dupe Groups — 2026-05-19

The Phase 5 audit (2026-05-18) had identified 74 real-dupe groups but only
4 had been resolved manually. This bulk pass closed the remaining 70 (+
3 stragglers re-introduced afterwards) via automated survivor-selection
and field-merge, taking the directory from **13,969 → 13,895** churches.

## Algorithm

Per group:

1. **Survivor selection** — pick the record with the highest `fieldScore`
   (weighted by populated schema fields: address +2, real-pastor +3,
   signatories +2, notable_attendees +2, etc.). Ties broken by better
   rating (green > yellow > red > unrated), then by shorter slug
   (cleaner ID wins).
2. **Field merge** — for each non-survivor source:
   - Pastor: longer, non-placeholder string wins.
   - Empty simple fields filled from source (website, facebook, etc.).
   - Better rating wins (green > yellow > red > black > dead > unrated).
   - Arrays (cross_listed_in, notable_attendees, tags, enrichment_sources)
     get union'd.
   - `signatories` object gets deep-merged per-ledger; aggregate recomputed.
   - `needs_review` flag is OR'd.
3. **Audit trail** — survivor's `enrichment_notes` gets a "Phase 5b auto-merge"
   line citing the absorbed IDs and the dupe group key.
4. **Source deletion** — non-survivor records removed from
   `docs/data/churches.json`; their HTML pages backed up to
   `/tmp/orphan-backup-2026-05-19/` and deleted.

## Results

| Metric | Pre-Phase-5b | Post-Phase-5b | Delta |
|---|---:|---:|---:|
| Total churches | 13,969 | 13,895 | **-74** |
| Dupe groups remaining | 70 | 0 | -70 (+3 stragglers also closed) |
| Sitemap URL count | 13,969 | 13,895 | -74 |
| Orphan HTML files | 74 | 0 | cleaned |
| Networks-page cross-listed total | 7,557 | 7,474 | -83 (downstream of merges) |

## Notable handled cases

- **First Baptist Church Charlotte NC** — 3-way merge: `first-baptist-charlotte-nc` survived; absorbed `first-baptist-church-charlotte-sbc-nc` and `first-baptist-church-charlotte`. Survivor had GREEN rating + real pastor (Jon Akin, interim).
- **"evergreen-church-bloomington-mn" stale slug** — record's actual `name`/`address` fields had been updated to "Eagle Brook Church / Lino Lakes MN" but slug never re-aligned. Merged into `eagle-brook-church-lino-lakes-mn`.
- **ARBCA Reformed Baptist mass-dedup** — ~6 records with `arbca-` prefix slugs merged into canonical slugs.
- **Brentwood Baptist Brentwood TN** — stale-pastor case: one record had Mike Glenn (former senior); the survivor record had Jay Strother (successor since Sept 2023). Both retained in audit trail.

## Outstanding

1. **Re-run the dupe-audit script** to confirm no NEW dupes exist post-merge. (Some merges may have created new key-collisions if cross-listed records had the same canonical key.)
2. **Spot-check the 28 "conflicting pastor" cases** that the merger now wrapped silently: most were stale-data cases like Brentwood Baptist (former vs current senior pastor), but a few may merit explicit pastor-history notes in `enrichment_notes`.
3. **Review the 4 "PCA"-slugged but actually-PCUSA records** discovered during Phase-7 cross-reference (e.g., `pca-first-presbyterian-salt-lake-city-ut`). These have misleading slugs that should eventually be re-aligned to match their actual denomination.
