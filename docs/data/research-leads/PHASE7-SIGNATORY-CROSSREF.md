# Phase 7 — Pastor-Signatory Cross-Reference Pass — 2026-05-19

Automated cross-reference of every MOOP church pastor against 7 canonical
pastor/leadership ledger files. Operationalizes the "people is policy"
editorial doctrine: a pastor's public statement signatures and organizational
affiliations are evidence-weighted signals about doctrinal trajectory.

## Ledgers covered

| Ledger | Year | Direction | Size | Methodology |
|---|---:|---|---:|---|
| Nashville Statement | 2017 | green | 22,916 | name + state corroboration |
| Dallas Statement | 2018 | green | 13,169 | name + state corroboration |
| Warhurst Protest | 2020 | red | 109 | name + PCA denomination scope |
| AMR Leadership | 2026 | red | 17 | name + Presbyterian denom scope |
| Letter of Lament | 2025 | red | 17 | name + PCA denomination scope |
| Revoice Speakers/Endorsers | 2018–26 | red | 60 | name + denominational scope |
| CBE Egalitarian Network | 2026 | red | 241 | name + denominational scope |

Total ledger entries indexed: **36,313**.
Unique first+last name keys: **33,827**.

## False-positive guardrails

- **Strict first+last name match** after stripping honorifics (Rev./Dr./Pastor/etc.) and suffixes (Jr./Sr./III/etc.).
- **State corroboration** required for Dallas + Nashville (the only way to filter out the inevitable homonym noise across 36K entries — e.g., "John Smith" appears many times).
- **Denominational scope filter** for the 5 smaller, denomination-specific ledgers. Example: the Warhurst Protest is a PCA-internal document; a "James Miller" who signed it as a Ruling Elder in Pittsburgh Presbytery should NOT auto-tag onto a homonymous Southern Baptist pastor in Texas.
- **MERGE-not-overwrite policy**: prior editorial signature data (452 pre-Phase-7 records) is preserved when not actively contradicted. New matches are added but old ones are not silently dropped.

## Results

| Metric | Pre-Phase-7 | Post-Phase-7 | Delta |
|---|---:|---:|---:|
| Churches with any signatory match | 452 | 464 | **+12** |
| Total signatory entries | ~552 | 586 | **+34** |
| Aggregate=green (orthodox-aligned) | 374 | 379 | +5 |
| Aggregate=red (drift signal) | 65 | 72 | +7 |
| Aggregate=mixed (warrants review) | 13 | 13 | 0 |
| Aggregate=unset (data gap) | 23 | 3 | -20 |

Newly verified high-confidence green matches include: Matt Chandler (The Village Church, all campuses), Jack Graham (Prestonwood Baptist, all campuses), Daniel Akin (SEBTS), Heath Lambert (FBC Jacksonville), Kevin DeYoung (Christ Covenant), Andy Davis (FBC Durham), Phillip Bethancourt (Central Baptist College Station), Fred Luter Jr. (Franklin Avenue Baptist), Afshin Ziafat (Providence Frisco).

Newly verified red matches: 6 AMR-2026 leadership entries (David Cassidy at Spanish River; Sean Michael Lucas at Independent Presbyterian Memphis; Kyle Wells; Geoff Ziegler; Jenilyn Swett-adjacent records), plus Warhurst protest signers across the Kellerite-PCA cluster.

## Rejected matches

**1,152 candidate big-list (Nashville/Dallas) matches were rejected for missing state info on either side.** This is by design — homonym risk across 36K names is too high to commit without geographic corroboration. Some of these are likely true positives the system can't currently verify; they remain in the "could-be-true" pool for future human review when address data improves.

## Outputs

- `scripts/cross-reference-signatories.js` — reusable pass; re-runnable as new pastor data lands.
- `docs/data/churches.json` — `signatories` object + `signatures_aggregate` field populated/refreshed.
- HTML pages regenerated for the affected records (per-church template at `generate-church-pages.js:117–148` renders the badge).

## Outstanding work

1. **Recover the 1,152 state-rejected big-list matches** — needs address backfill on either the church or the signer's institution. Probably 200–400 true positives hidden here.
2. **Manual review of the 13 mixed-aggregate records** — Nashville+Warhurst overlap suggests either a pastor-trajectory-shift (rare but real) or a homonym false positive that escaped both filters. Each warrants a 30-second human check.
3. **Extend the name normalizer** for nickname collapse (Robert↔Bob, William↔Bill, Jonathan↔Jon) to recover an estimated 20–40 additional matches.
4. **Add weekend tools sweep** — periodically rerun this pass as new churches arrive via the network-leads queue.
