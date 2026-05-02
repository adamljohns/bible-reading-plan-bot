# Roadmap V5.0 → V6.0 — The 4,911 → ~5,911 Sprint

**Version target:** V5.0.0 (current 4,911) → V5.5.0 mid-cycle → V6.0.0 at ~6,000 churches.
**Net additions target:** ~1,000 new churches + ~500 data-quality updates = ~1,500 total directory deltas.
**Designed for:** weekend / Tue–Wed firing window before Wed-midnight 20x-subscription reset.
**Operator:** Claude Code with `church-directory-enrichment` skill loaded; 4 parallel research agents per round.
**Apply pattern:** each round writes one or more `/tmp/patch-<slug>.json` files, foreground validates + applies via `python3 /tmp/apply_patch.py`, regenerates via `node generate-church-pages.js`, commits + pushes.

---

## Why this shape

Gap analysis run 2026-05-02 against `docs/data/churches.json` shows the largest leverage points:

| Denomination / target | Current | National scale | Gap-leverage |
|---|---:|---:|---|
| GMC (Global Methodist Church) | 31 | ~5,500 | **largest** |
| WELS (Wisconsin Evang Lutheran) | 14 | ~1,200 | very large |
| Foursquare (conservative wing) | 0 | ~1,700 | very large |
| Mennonite / Brethren orthodox | 6 | ~1,500 | very large |
| Vineyard (conservative) | 1 | ~600 | large |
| Acts 29 nationwide | 80 | ~250 | medium |
| Verify-pastor records | 462 | — | data-quality |
| Incomplete-address records | 1,666 | — | data-quality |

The 5,000 → 6,000 milestone in `directory-overview.html` calls out: "SBC megachurch coverage + denominational drift documentation (Saddleback / Bayside / Fern Creek precedents) + Acts 29 nationwide." This roadmap honors that and adds the Wesleyan/Holiness/Anabaptist phase work that was originally slated for 6,000 → 7,000 — pulling it forward because GMC is unusually well-organized post-2022 split and produces fast verifiable adds.

---

## Sequencing rules

1. **Always 4 agents in parallel** per round; each agent owns a non-overlapping geographic or denominational scope.
2. **Foreground works data-quality** while agents run (pastor verification, address normalization).
3. **Apply patches as they land** — don't wait for all four. Each lands its own commit.
4. **Refresh `/tmp/all_existing_slugs.txt` + per-denomination dedup files before each round.**
5. **Commit cadence:** one commit per agent patch (4–8 commits per round). Push immediately so partial work survives context loss.
6. **Cross-reference signature lists every 3 rounds** — this is cheap and high-yield.
7. **Bump to V5.x.x sub-versions every ~3 rounds** so the changelog tracks granular progress.
8. **Final V6.0.0 close-out** when total ≥ 5,950 with comprehensive denomination + state coverage on the new families.

---

## Round-by-round plan (16 rounds → ~1,000 net new churches)

### Phase A — Drift documentation (~150 net adds, ~6 commits)

#### Round A1: SBC megachurch female-pastor drift sweep — **30–50 churches**
**Why:** The directory documents the precedent (Saddleback, Bayside, Fern Creek) but the universe of similar SBC churches with female senior/teaching/co-pastors is much larger. These are critical drift markers.

**Agents (4):**
- **Agent A1.1** — California megachurches: Saddleback satellites, NewSong Irvine, Mariners Church, Bayside Granite Bay successors. Search SBC megachurch lists + recent female-pastor news 2023–2026.
- **Agent A1.2** — Texas megachurches: cross-reference SBC churches with female senior pastors using SBC megachurch lists; Houston/Dallas/Austin focus.
- **Agent A1.3** — Florida megachurches: Tampa/Miami/Orlando/Jacksonville SBC drift candidates.
- **Agent A1.4** — Mid-South + Carolinas megachurches: Charlotte/Atlanta/Nashville/Memphis SBC drift candidates.

Each agent: BLACK rating + credentials-committee-referral note + scandal_flag.

#### Round A2: Acts 29 nationwide expansion — **40–60 churches**
**Why:** Currently 80 in directory; Acts 29 has ~250 globally, ~180 US. Many are missing especially West Coast + Mountain West + Midwest urban plants.

**Agents (4):**
- **Agent A2.1** — California / Arizona / Nevada / Colorado urban Acts 29 plants
- **Agent A2.2** — Texas / Oklahoma / New Mexico Acts 29 plants
- **Agent A2.3** — Pacific Northwest (WA/OR/ID/MT/AK) Acts 29 plants
- **Agent A2.4** — Midwest urban (IL/MN/OH/MI/WI/IN) Acts 29 plants

Source: acts29.com/find-a-church.

#### Round A3: PCA Warhurst-signer drift documentation — **40 churches**
**Why:** 90 Warhurst signer churches identified at sprint start; only 4 hand-added. Remaining ~85 need YELLOW + cultural=red treatment with populated `signatories.warhurst_protest_2020`.

**Agents (4):**
- **Agent A3.1** — Northeast/Mid-Atlantic Warhurst PCA presbyteries (Chesapeake, NJ, NY, PA)
- **Agent A3.2** — Southeast Warhurst PCA presbyteries (SC, GA, FL, NC, AL)
- **Agent A3.3** — Texas + Mississippi + Louisiana Warhurst PCA presbyteries
- **Agent A3.4** — California + Korean PCA presbyteries Warhurst signers

Source: `docs/data/pca-warhurst-signers-2020.json`.

---

### Phase B — New denomination families (~600 net adds, ~16 commits)

#### Round B1: GMC (Global Methodist Church) nationwide first pass — **150–200 churches**
**Why:** GMC formed 2022 from UMC orthodox split. ~5,500 churches. Currently 31 in directory — essentially a denomination we haven't covered. Highest single-target ROI in plan.

**Agents (4):**
- **Agent B1.1** — Southeast GMC (TX/LA/MS/AL/GA/FL/SC/NC/TN/KY)
- **Agent B1.2** — Mid-Atlantic + Northeast GMC (VA/WV/MD/PA/OH/NY/NJ/DE/DC + New England)
- **Agent B1.3** — Midwest + Plains GMC (IL/IN/WI/MN/IA/MO/KS/NE/ND/SD/OK + AR)
- **Agent B1.4** — Mountain West + West Coast GMC (CO/UT/WY/MT/ID/AZ/NM/NV/CA/OR/WA + AK/HI)

Source: globalmethodist.org/find-a-church. Note: GMC is complementarian by polity but watch for transitional female-clergy holdovers from UMC era — flag those YELLOW.

#### Round B2: WELS (Wisconsin Evangelical Lutheran Synod) nationwide — **60–80 churches**
**Why:** Confessional Lutheran (more conservative than LCMS on close communion + women's roles). ~1,200 nationally; 14 in directory. Particularly thin outside Wisconsin/Minnesota/Michigan.

**Agents (4):**
- **Agent B2.1** — Wisconsin + Michigan WELS (heavy density)
- **Agent B2.2** — Minnesota + Dakotas + Iowa + Nebraska WELS
- **Agent B2.3** — Texas + Florida + Arizona + California WELS
- **Agent B2.4** — Pacific NW + Mountain West + remaining states WELS

Source: wels.net/find-a-church.

#### Round B3: Conservative Mennonite + Brethren orthodox — **40–60 churches**
**Why:** Anabaptist tradition almost entirely absent (6 records). Restrict to confessionally orthodox bodies; skip mainline/progressive Mennonite USA.

**Agents (4):**
- **Agent B3.1** — Conservative Mennonite Conference (CMC) + Biblical Mennonite Alliance churches
- **Agent B3.2** — Charity Christian Fellowship + Eastern Pennsylvania Mennonite Church + Nationwide Fellowship
- **Agent B3.3** — Old Order / Old Brethren / German Baptist Brethren conservative streams
- **Agent B3.4** — Brethren in Christ orthodox + Evangelical Mennonite Conference

Skip: Mennonite USA (mainline drift), Mennonite Church Canada (mainline drift). Source: cmcrosedale.org, charity-christianfellowship.org, anabaptistmennonites.com directories.

#### Round B4: Foursquare conservative wing — **40–60 churches**
**Why:** Foursquare = ~1,700 churches; 0 in directory. Heritage = Aimee Semple McPherson's pentecostal ICFG. Distinguish conservative orthodox congregations from mainstream Foursquare drift. Pre-screen for confessional orthodoxy and complementarian polity (Foursquare ordains women so default YELLOW gender + cultural=yellow). Some congregations are quite orthodox (Jack Hayford's old Church on the Way tradition).

**Agents (4):**
- **Agent B4.1** — California Foursquare (heaviest concentration)
- **Agent B4.2** — Pacific NW + Mountain West Foursquare
- **Agent B4.3** — Texas + Florida + Southeast Foursquare
- **Agent B4.4** — Northeast + Midwest + remaining Foursquare

Source: foursquare.org/find-a-church. Default rating YELLOW per women-in-ministry polity; rare GREEN if congregation explicitly affirms male-only senior leadership.

#### Round B5: Vineyard conservative wing — **30–40 churches**
**Why:** Vineyard = ~600 churches; only 1 in directory. Wimber-tradition charismatic-evangelical. Mixed bag theologically — many on cessationism/continuationism spectrum, some women-in-ministry drift. Default YELLOW unless verified confessional + complementarian.

**Agents (4):**
- **Agent B5.1** — California Vineyard (founding region)
- **Agent B5.2** — Mountain West + Plains Vineyard
- **Agent B5.3** — Southeast + Texas Vineyard
- **Agent B5.4** — Midwest + Northeast Vineyard

Source: vineyardusa.org/find-a-church.

---

### Phase C — Thin-state SBC megachurch fills (~200 net adds, ~8 commits)

#### Round C1: West Coast SBC megachurch coverage — **60–80 churches**
**Why:** SBC West Coast presence is real but underdocumented vs. the directory's heavy Southeast SBC. Saddleback's drift made the news but there are dozens of orthodox-holding SBC megas in CA/WA/OR.

**Agents (4):**
- **Agent C1.1** — California SBC megachurches (LA / SF Bay / San Diego / Sacramento / Inland Empire) — exclude already-flagged drift cases
- **Agent C1.2** — Pacific NW SBC (WA/OR/ID/AK) megachurches
- **Agent C1.3** — Mountain West SBC (CO/AZ/NV/UT/NM/MT/WY) megachurches
- **Agent C1.4** — Hawaii SBC + Texas-border CA SBC + Cross-cultural ministries

Source: sbc.net church directory + 12-Stone-style megachurch lists.

#### Round C2: Texas / Florida SBC megachurch + lead-pastor fill — **50–70 churches**
**Why:** Heaviest SBC density states; current directory has many but with `Verify` pastors. Twin task: add missing megas + verify all existing TX/FL SBC megachurch pastors.

**Agents (4):**
- **Agent C2.1** — Houston / Dallas / Austin / SA / FW Metroplex SBC megachurches missing
- **Agent C2.2** — Florida East Coast (Miami / Orlando / Jacksonville / Tampa Bay / Daytona) SBC megas
- **Agent C2.3** — Florida Panhandle + West Coast (Pensacola / Naples / Sarasota / Ft. Myers) SBC
- **Agent C2.4** — Texas non-metro SBC megas (Lubbock / El Paso / Corpus / Beaumont / Tyler / Waco)

#### Round C3: Northeast thin-state evangelical fill — **40–60 churches**
**Why:** NY/NJ/MA/CT/RI/VT/NH/ME are evangelical thin nationally but have orthodox enclaves (Redeemer NYC network, GraceLife Boston, etc.). Most current directory entries here are confessional Reformed.

**Agents (4):**
- **Agent C3.1** — NYC + NJ + Long Island evangelical (Redeemer plants, EFCA, SBC, Acts 29)
- **Agent C3.2** — New England (MA/CT/RI/VT/NH/ME) confessional evangelical
- **Agent C3.3** — Upstate NY + Hudson Valley evangelical
- **Agent C3.4** — Tri-state non-Manhattan urban orthodox evangelical (Brooklyn/Queens/Newark)

#### Round C4: Carolinas SBC backfill — **30–40 churches**
**Why:** NC/SC SBC density is very high but coverage is uneven. Specifically target 50K+ population towns where the FBC isn't yet in directory.

**Agents (2 agents are sufficient given narrower scope):**
- **Agent C4.1** — North Carolina SBC missing-FBCs in 50K+ towns
- **Agent C4.2** — South Carolina SBC missing-FBCs in 50K+ towns
- **Agent C4.3** — bonus: NC/SC ARP backfill (still SC-skewed even after Round 2 work)
- **Agent C4.4** — bonus: NC PCA Central Carolina presbytery completion

---

### Phase D — Data quality (~50 net adds, mostly updates, ~6 commits)

#### Round D1: Pastor verification batch sweep — **0 net adds, 200+ updates**
**Why:** 462 records still have `Verify` or empty pastor fields. Each one is data-quality debt.

**Agents (4):**
- **Agent D1.1** — North Carolina + South Carolina + Georgia Verify-pastor sweep (largest concentration from Round 1 SBC pastor-fill)
- **Agent D1.2** — Texas + Florida Verify-pastor sweep
- **Agent D1.3** — ARP placeholder pastor sweep (35+ ARP records with empty pastor field per NAPARC directory)
- **Agent D1.4** — California + Mountain West + Pacific NW Verify-pastor sweep

Each agent uses church website /staff page + LinkedIn cross-reference to verify.

#### Round D2: Address normalization batch sweep — **0 net adds, 300+ updates**
**Why:** 1,666 records have incomplete addresses (just City, ST without street/ZIP). Each is data-quality debt.

**Agents (4):**
- **Agent D2.1** — Virginia + DC + Maryland incomplete-address fills (highest Adam-personal-relevance)
- **Agent D2.2** — North Carolina + South Carolina + Georgia incomplete-address fills
- **Agent D2.3** — Texas + Florida incomplete-address fills
- **Agent D2.4** — Remaining states incomplete-address fills

#### Round D3: Sermon archive backfill for top GREEN churches — **0 net adds, ~100 updates**
**Why:** `sermon_archive_url` and `sermon_archive_platform` fields exist (added 2026-04-17) but mostly empty. Top GREEN churches should have these populated to support discernment.

**Agents (4):**
- **Agent D3.1** — Top 100 GREEN PCA + OPC + EPC + ARP sermon archives
- **Agent D3.2** — Top 100 GREEN Reformed Baptist + Founders + LCMS sermon archives
- **Agent D3.3** — Top 100 GREEN SBC + Acts 29 sermon archives
- **Agent D3.4** — Top 50 GREEN ACNA + GMC sermon archives

Source: each church's website /sermons or /media URL + platform identification (YouTube channel / Vimeo / SermonAudio / Apple Podcasts / RSS).

---

### Phase E — Cross-reference + close-out (~8 commits)

#### Round E1: Full signature cross-reference pass
Re-run the 7-list signature-cross-reference against the new ~1,000 churches. Expect ~100 new attributions across Nashville Statement (initial signers only), Dallas Statement (initial signers only), Warhurst (curated PCA list), AMR, Lament, Revoice, CBE.

#### Round E2: V5.5.0 mid-version bump + changelog
After Round B1 (GMC) lands, bump to V5.5.0. Update `directory-overview.html` roadmap to mark "5,000" milestone done, "5,500" current.

#### Round E3: V6.0.0 close-out
After total ≥ 5,950 with comprehensive new-denomination coverage, bump to V6.0.0. Update changelog with full Phase A-E summary. Update `directory-overview.html`:
- Mark "5,000 → 6,000" done
- Mark "6,000 → 7,000" current
- Move next-phase work (Anabaptist orthodox / GMC nationwide / Pentecostal-Charismatic conservative) above to "done" since pulled forward
- Add new milestone description for what 6,000 → 7,000 will now be (Eastern Orthodox conservative, conservative Anglican REC, RPCNA, conservative Lutheran ELS, etc.)

---

## Per-round agent prompt template

```
You are research-Agent {AGENT-ID} in a 4-agent parallel sweep building the
MOOP church directory at /Users/moop_bot_pro/bible-reading-plan-bot.

GOAL: {SPECIFIC TARGET — denomination, region, count}.

EXISTING (read /tmp/existing_{denom}.json — N entries) — DO NOT DUPLICATE.
DEDUP RULE: Read /tmp/all_existing_slugs.txt before finalizing any slug.

SOURCES (priority):
1. {primary denominational find-a-church}
2. {secondary directories}
3. Individual church websites for pastor verification

QUALITY BAR:
- Verified pastor name (no placeholders)
- Working https website
- Real street address
- Confirmed denominational affiliation

DRIFT WATCH (denomination-specific):
- {GMC: female-clergy holdover from UMC era → YELLOW gender}
- {Foursquare: women in ministry → YELLOW default}
- {Vineyard: cessationism/continuationism mixed → YELLOW preaching}
- {SBC: female senior pastor → BLACK + credentials-referral}

OUTPUT: `/tmp/patch-{slug}.json`:
```json
{ "new_churches": [...], "agent": "{AGENT-ID}", "states": [...], "notes": "..." }
```

SCHEMA: Read /tmp/SCHEMA_TEMPLATE.json. Specifics:
- `id` == `slug`
- `denomination`: "{DENOM-TAG}"
- `denomination_family`: "{FAMILY}"
- `type`: "{full denomination string}"
- `gender_detail`: "{denomination's gender polity in 1 sentence}"
- score_notes reference {denomination's confessional standards}
- Scores green default; cultural/preaching yellow if not verified
- `signatories`: 7 keys all empty arrays. `signatures_aggregate`: "none"
- Social fields top-level
- `enrichment_sources`: church website + denomination directory URL
- `tags`: include denomination, state, city, distinctive

TARGET: {N} verified churches. Quality > quantity.

DO NOT modify churches.json. ONLY write patch. Report under 200 words.
```

---

## Estimated session budget

| Phase | Rounds | Agents | Tokens (est) | New churches |
|---|---:|---:|---:|---:|
| A — Drift docs | 3 | 12 | 1.5M | 130 |
| B — New denoms | 5 | 20 | 3.0M | 350 |
| C — SBC fills | 4 | 14 | 2.0M | 220 |
| D — Data quality | 3 | 12 | 1.8M | 0 (updates) |
| E — Close-out | 3 | 4 | 0.4M | 0 |
| **TOTAL** | **18** | **62** | **8.7M** | **~700 net + ~500 updates** |

The "1,000" target is ambitious because each new church is fully verified (not bulk-imported). Closer to 700 net new + 500 data-quality updates is realistic, totaling ~1,200 directory deltas. If we want a hard 1,000 net new, add another ~12 agents in Phase B6 (additional Foursquare states, Vineyard regions) and/or Phase B7 (REC / Reformed Episcopal Church + RPCNA expansion).

---

## Pre-flight checklist (run before kicking off Round A1)

```bash
cd /Users/moop_bot_pro/bible-reading-plan-bot

# 1. Pull latest
git pull --rebase origin main

# 2. Refresh dedup files
python3 -c "
import json
d = json.load(open('docs/data/churches.json'))
all_slugs = sorted([c.get('slug', c.get('id','??')) for c in d['churches']])
open('/tmp/all_existing_slugs.txt','w').write('\n'.join(all_slugs))
print(f'Refreshed {len(all_slugs)} slugs')
# Plus per-denomination dedup files for each round's target...
"

# 3. Verify schema template
python3 -c "import json; print(list(json.load(open('/tmp/SCHEMA_TEMPLATE.json')).keys()))"

# 4. Verify apply scripts work
ls /tmp/apply_patch.py /tmp/apply_pastor_updates.py

# 5. Dry-run generate (no writes)
node generate-church-pages.js --dry-run 2>&1 | tail -3 || node generate-church-pages.js 2>&1 | tail -3

# 6. Confirm clean working tree
git status
```

---

## Wednesday-fire-time notes

- **Session-start prompt to drop in:** "Execute Roadmap V5-to-V6 starting at Round A1. Pre-flight checks first. Apply each agent patch as it lands; commit + push immediately. Brief under 200 words after each round."
- **Pace:** Plan to spend ~3 hours per phase if running in foreground, OR ~1 hour per phase if launching all 4 agents in parallel and only foreground-applying. With 5 phases, that's 5–15 hours of session work depending on parallelism — well within a fresh 20x budget.
- **Stopping rules:** stop and brief at 60% usage so there's headroom. If something goes wrong (e.g., V5.5.0 fails to push, or a denomination directory is offline), pivot to data-quality (Phase D) which doesn't depend on external research.
- **Don't fire on Wednesday before midnight.** Reset is post-midnight Wed → Thu. Fire Thursday morning so the full 7-day cycle is available.

---

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| GMC find-a-church goes offline mid-round | Fall back to per-conference directories (gmcSouthwest.org, gmcInteriorWest.org, etc.) |
| Foursquare requires login to access full directory | Pull from publicly-indexed find-a-church + denominational reports; skip private-only entries |
| Org-monthly-usage limit hits mid-round | Round-by-round commits mean no work is lost; resume next session from last commit |
| Generator breaks on new denomination_family value | Add the new family to `STATEMENT_META` in `generate-church-pages.js` before applying patch |
| Schema drift in agent output (signatories as dict vs string) | `apply_patch.py` already handles defaults; flatten dict signatories to strings before calling |
| Church count crosses 5,000 mid-Round B1 — confusion on overview milestone | After 5,000 lands, immediately bump `directory-overview.html` to mark milestone done |

---

## Personal-engagement bookmark

Adam: there is currently **1** church marked `engagement.attended_personally: true` in the directory. The roadmap doesn't directly enrich personal-engagement (you're the only one who can do that), but every record you do attend should be batched into a quarterly `personal-engagement-update.md` and applied via a small foreground commit. That's the single most differentiated data point in the directory and worth protecting.
