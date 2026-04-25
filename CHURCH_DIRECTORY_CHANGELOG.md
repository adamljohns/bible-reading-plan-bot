# MOOP Church Directory — Changelog

Theological due-diligence tool for American churches. Tracks orthodox confessional commitment, elder plurality, men's discipleship, cultural stance, denominational accountability, and 5 other dimensions across 4,179+ churches.

Rubric: 4-tier threat-zone system (green / yellow / red / black) × 10 scoring dimensions.

Stewarded at **[usmcmin.org/churches.html](https://usmcmin.org/churches.html)**.

---

## V4.9.2 — 2026-04-25 · Strict denom-correction sweep + dedup

- **53 records flipped** to corrected denominations via strict-affirmative filter on V4.9 detector output (314 proposals → 53 auto-applied; 261 await agent verification)
  - 9 SBC → ABCUSA (FBC Birmingham MI, FBC Boise, FBC Denver, FBC Indianapolis, FBC Manchester NH, FBC Omaha, FBC Sioux Falls, FBC Syracuse, Tremont Temple Boston, Columbia Street Bangor ME, etc.)
  - 14 LCMS → ELCA (Concordia Manchester CT, Ebenezer Chicago, First LCMS Topeka, Mt Olive Las Vegas, Mt Olive Minneapolis, Prince of Peace Augusta ME, etc.)
  - 12 SBC → CBF (Colonial Avenue Roanoke / Radiance, FBC Abilene, FBC Athens GA, FBC Augusta GA, FBC St. Pete, FBC Vestavia Hills, Gambrell Street Fort Worth, Trinity Baptist San Antonio, etc.)
  - 3 SBC → BGAV (Bedford, Bonsack Roanoke, Petersburg Baptist)
  - 2 PCA → EPC (Faith PCA Germantown, Sunset Presbyterian Portland)
  - 2 PCA → PCUSA (Grace Pres Las Vegas, Jackson Hole, Media PCA)
  - 1 SBC → UMC (Stonebridge McKinney TX — post-split UMC remainer)
- **Dedup**: brock-road-baptist-church → chancellor-christian-church-spotsylvania merged (same address, same pastor, same site; legacy slug from pre-V4.9 misidentification)
- **Mt. Ararat / The Mount Stafford** earlier-day merge (legacy SBC mis-tag → BGAV, same 1112 Garrisonville Rd address)
- **McLean Bible Vienna** Platt walk-back: removed stale "David Platt (Lead Pastor)" citation; Platt stepped back from senior role late 2023 to focus full-time on Radical
- **The Mount Fredericksburg** corrections: founded 1907 (as Mount Ararat Baptist), services 9:15 & 10:45 AM, YouTube link fixed, internal-review jargon scrubbed from scorecard, BGAV/SBC distinction clarified
- Directory: 4,181 → 4,179
- Scripts added: `build_denom_corrections_strict.py`, `apply_denom_corrections_strict.py`, `fix_mclean_and_mount.py`

## V4.9 — 2026-04-25 · Massive 10-agent push (+33 churches, +173 URLs, 31 VA flips)

- **WORKSTREAM 1: Bulk URL recovery (4 agents, 233 priority no-URL records)**
  - 173 URLs assigned (78% recovery rate across green/red/black-rated records)
  - 10 confirmed defunct, 47 address-mismatch flagged, 20 need deeper research
  - Surfaced ~50 denomination mis-tags during research (FBC downtown churches in Lincoln/Seattle/Mobile/Macon/Madison/Omaha/Billings/Des Moines/Sacramento/Providence are American Baptist not SBC)
  - Notable rebrands caught: Mars Hill (sold to Quest), Hope Chapel Kaneohe → Anchor Church, Spring Arbor FM → The Arbor, FBC Birmingham MI → Sanctuary, Valley Christian Center Dublin → Brave Church, FBC Boise → True Hope Downtown, FBC Sacramento → Midtown Collective, Sovereign Grace Frederick MD → Living Hope Community
- **WORKSTREAM 2: Virginia deep-dive (4 agents, 67 yellow VA churches)**
  - 31 VA rating flips: 13 yellow→green, 18 yellow→red
  - Greens: Calvary Chapel Manassas (full SOF + complementarian), Liberty Live Hampton (Grant Ethridge ex-NSBCP president), McLean Bible Vienna (later partially walked back — Platt stepped down), Trinity Lutheran Richmond (LCMS confirmed), Christiansburg Baptist (BFM2000 + dual SBC/SBCV), Rock Hill Baptist Stafford (SBCV), FBC Springfield, Grundy Baptist, Great Hope Baptist Chesapeake (IFB), Redeemer Anglican Richmond (ACNA, male-only clergy), London Bridge Baptist VA Beach (SBC/SBCV + 1784 founding), Northwest Baptist Roanoke (Nashville Statement affirmed)
  - Reds: Hebron Baptist Spotsylvania (Carol Markham licensed to preach), Glen Allen Baptist (3 named female pastors + CBF VA), FBC Waynesboro (triple SBC+BGAV+CBF + female Associate Pastor), Grace Covenant Chantilly (Every Nation + 2 named female pastors), Grace Baptist Richmond (Lauryn Everic female Acting Senior Pastor + Alliance of Baptists), Hylton Memorial Chapel (NAR/Paula White conference + apostolic-covering), Hope Pres Fredericksburg (Pauline Johnson female elder preaching), Bridge Community/Bridge RVA (Vineyard + Becky Peters Co-Pastor), MVMNT Cville (Jeff & Kristy Nicolette husband-wife co-pastors), Haymarket Baptist (CBF + BGAV + women ordained), New Life Christian Chantilly (Restoration Movement)
  - 12 phantom records flagged
  - URL/data corrections during VA deep-dive: 10210 Leavells Rd is Open Door Baptist (not "Leavells Baptist"); Remnant Church Richmond at remnantrva.com (Bryan Laughlin, NOT Joel Brooks of Birmingham); Great Bridge Baptist transitioning to Chuck Lawless (former SEBTS Dean of Doctoral Studies); FBC Norfolk data conflation (fbcnorfolk.org redirects to historic Black Baptist BGCVA + Lott Carey, NOT the SBC megachurch at Kempsville); River City Baptist Richmond is SBCV (was tagged PCA); Brock Road Baptist actually Stone-Campbell Restoration Movement; peninsulabaptist.com → Mooresville NC (not Hampton VA); newlifewesleyan.org → Fayetteville TN (not La Plata MD)
- **WORKSTREAM 3: Conservative Anglican + small Reformed adds (1 agent, +33 churches)**
  - CANA/CONNAM: 3 (incl. Holy Trinity Cathedral Houston, Bp. Celestine Ironna)
  - AMiA: 6 (Bp. Robert Cook, Bp. Philip Jones)
  - ACC (Anglican Catholic Church): 8 (1928 BCP traditionalist)
  - RCUS: 8 (Aberdeen SD, Vermillion SD with Heidelberg Seminary, Hope Reformed Sutton NE est. 1908)
  - KAPC: 6 (Sarang Anaheim, Sarang LA Koreatown, Joong Ang NYC)
  - REC: 2 (Bp. Ray Sutton's diocese parishes)
- **WORKSTREAM 4: Denomination-correction sweep (1 agent)**
  - 314 denomination mis-tag suspects detected (241 high-confidence, 73 medium); proposals saved to `tmp/denom_correction_proposals.json` for V4.9.2 application
- 12 confessional networks now meaningfully covered: PCA, OPC, URCNA, CREC, ARP, WELS, RPCNA, SGC, CBA, HRC, FRCNA, RPCGA, CMA, IFCA, BPC, CANA, AMiA, ACC, RCUS, KAPC, REC

## V4.8 — 2026-04-24 · Confessional expansion 2 (+96 churches) + Wayback fill

- 96 new confessional Reformed/Presbyterian/Lutheran churches added
- 87 URLs archived to Wayback Machine across 63 new churches (665 snapshots total)

## V4.7 — 2026-04-24 · Phase 2 Wayback snapshot batch

- Bulk Wayback Machine archival across enrichment_sources arrays
- Sources & Evidence card now points to archived snapshots so cited evidence persists if a church website changes or goes dark

## V4.6 — 2026-04-23 · Dedup sweep (R57 yellow-only + 75 duplicates merged)

- 75 true-duplicate records merged via `find_true_duplicates.py` + `apply_dedup_plan.py`
- Tightened dedup matcher to require same domain + same normalized name + same city/state + same street number (prevents false-merge of Life.Church / Gateway / Village multi-site campuses)
- R57 yellow-only enrichment round (60 patches)

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
