# MOOP Church Directory — Changelog

Theological due-diligence tool for American churches. Tracks orthodox confessional commitment, elder plurality, men's discipleship, cultural stance, denominational accountability, and 5 other dimensions across 4,127+ churches.

Rubric: 4-tier threat-zone system (green / yellow / red / black) × 10 scoring dimensions.

Stewarded at **[usmcmin.org/churches.html](https://usmcmin.org/churches.html)**.

---

## V4.5 — 2026-04-24 · Confessional-network expansion

- **+123 new confessional Reformed churches added:**
  - URCNA: 0 → 22 (all 8 classes represented)
  - OPC: 5 → 33 (presbyteries: Philadelphia, NJ/PR, MI/ON, Mid-Atlantic, Northwest)
  - CREC: 4 → 18 (incl. Peter Leithart's Saint Peter Presbyterian Bristol TN, Ralph Smith's Reformation Covenant Oregon City)
  - ARP: 12 → 35 (incl. Richland ARP Rosemark TN est. 1782, Ballston Center NY oldest northern ARP)
  - WELS: 1 → 14 (incl. Wisconsin Lutheran Seminary Chapel Mequon)
  - RPCNA: 1 → 12 (incl. Reformed Presbyterian Theological Seminary Pittsburgh; every record cites exclusive a cappella psalmody)
  - SGC: 2 → 14 (incl. Sovereign Grace Louisville — C.J. Mahaney anchor + Covenant Life Gaithersburg MD)
- **38 systematic enrichment rounds** (R19–R56) with parallel-agent pipeline producing ~960 total rating changes
- **URL-mismatch hunt** caught dozens of directory-pollution cases: wrong-state (FBC Hope AR→IN, FBC Beaufort SC→NC, Two Rivers Baptist Nashville→King George VA), wrong-entity (Oak Park Mobile→Jonesboro GA, Canvas Church Austin→Montana, FBC Jackson MS→TN), ghost records (Wesleyan HQ Fishers, True Life Denver Acts 29 stub)
- **Denomination mis-tag corrections**: multiple FBC-Chattanooga / FBC-Lexington-NC / FBC-Mount-Airy / Hope Sioux Falls → ELCA caught as CBF or egalitarian misclassifications
- **CRT + spiritual-formation drift vectors** catalogued: New Birth Missionary Baptist (Ibram X. Kendi Book of the Month), FBC Columbus MS (John Mark Comer "Practicing the Way"), Journey St. Louis (scripture "limited by biases" framing)
- Score_notes schema fix across 37 CREC+ARP records (per-dimension dict)

## V4.0 — 2026-03-15 · Validation maturity

- Rubric label updates: "Denominational Accountability" → "Accountability Structure" (elder plurality + one network tie suffices); "Concern" → "WARNING!" for red-rated churches
- Unified scorecard layout across 4 main pages (all-churches, FXBG, VA, DC Metro)
- VA sub-region filters built (Fxbg / DC-NoVA / Richmond / Charlottesville / Hampton Roads / Lynchburg / Shenandoah / Peninsula / Virginia-Other)
- Thin-green pool exhausted after 20+ validation rounds — every green record with avg-note-length <150 chars re-verified
- Region-based classification system with address-based auto-tagging

## V3.5 — 2026-02-01 · RC/EO + cross-denomination audits

- **33 Roman Catholic and Eastern Orthodox parishes** added to Virginia
- Denomination mis-tag sweeps: SBC ↔ CBF/ABCUSA/Alliance/NBC; LCMS ↔ ELCA/LCMC/WELS; PCA ↔ PCUSA/EPC/ECO; ACNA ↔ TEC
- Willow Creek flipped black → red (egalitarian governance ≠ apostate)
- Phantom-detection rubric formalized: multi-source search failure (denomination directory + ChurchFinder + Wikipedia + news + obit) = removal candidate
- Directory reached **4,004 churches**

## V3.0 — 2025-12-15 · Parallel-agent enrichment pipeline

- 18 enrichment rounds using 4 parallel agents × 25-50 churches per batch
- 2,880+ churches with concrete evidence per scorecard dimension
- 620+ rating changes via systematic evidence-gathering
- Established `moop-site-tools` repo for Hermes/OpenClaw agent reuse
- Incremental-write-every-5 pattern added to agent template (survives session timeouts)
- Anti-fabrication rule formalized: "yellow + 'Not stated on available sources' always beats green + guess"

## V2.5 — 2025-11-01 · Quality audit + rubric refinement

- Pastor field fixes (e.g., succession transitions, emeritus updates)
- Ghost-record removals (defunct / merged / relocated congregations)
- Deduplication pass
- Added `pastor_credentials`, `enrichment_notes`, `engagement{}` fields
- Verification badge system for MOOP-verified churches

## V2.0 — 2025-10-01 · Nationwide pivot

- First 50-state SBC/PCA/LCMS roll-up to ~2,000 churches
- Denomination normalization + `denomination_detail` field added
- Clean filter categories

## V1.5 — 2025-09-15 · Regional expansion

- Added Richmond, Hampton Roads, Charlottesville, Lynchburg, Peninsula, DC/NoVA/MD
- ~100 new regional churches

## V1.0 — 2025-09-01 · Initial FXBG directory

- Selah Church first entry; 40 FXBG-area churches
- 4-tier threat-zone system (green/yellow/red/black) + 10-dimension scoring rubric
- Gender rubric v1 (biblical patriarchy standard)
- Engagement tracking framework

---

## Attribution

- Stewarded by Adam Johns ([@alj4000bc31oct1517sep78](https://instagram.com/alj4000bc31oct1517sep78))
- Built for the brotherhood — "Watch, stand fast in the faith, be brave, be strong." ([1 Cor 16:13](https://usmcmin.org/bible.html?ref=1+Corinthians+16:13))
- Parallel-agent enrichment pipeline packaged in [moop-site-tools](https://github.com/adamljohns/moop-site-tools) for reuse on other directory projects
