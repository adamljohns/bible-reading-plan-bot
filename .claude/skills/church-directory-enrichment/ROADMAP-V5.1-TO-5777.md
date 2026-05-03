# Roadmap 5,024 → 5,777 — The "V5.1 → V5.7" Sub-Cycle

**Version target:** V5.0.0 (current 5,024) → V5.7.0 (~5,777 churches).
**Net additions target:** ~753 net new churches.
**Designed for:** **Wednesday-after-midnight reset firing window** — DO NOT FIRE BEFORE WED MIDNIGHT (budget reset). Adam currently >50% used, prioritizing remaining budget for Hermes / OpenClaw agent setup.
**Operator:** Claude Code with `church-directory-enrichment` skill loaded; 4 parallel research agents per round.
**Pace:** Weekend / off-peak Tuesday → Thursday firing — single 3-5 hour session is plenty.
**Apply pattern:** each round writes one or more `/tmp/patch-<slug>.json` files; foreground validates + applies via `node .claude/skills/church-directory-enrichment/scripts/integrate-patch.js`, regenerates via `node generate-church-pages.js`, commits + pushes.

---

## Why this cycle exists

We just crossed 5,000 churches. The original "V8.0 = 7,777" milestone in `directory-roadmap.html` is the long-term target. **5,777** is a useful intermediate — large enough to feel like real progress, small enough to fit one focused sprint. The sub-cycle from V5.0 to V5.7 fills the most-glaring gaps that surfaced after the 5,000-cross:

| Gap discovered post-5,000 | Current | Target | Rationale |
|---|---:|---:|---|
| GMC nationwide (post-VA) | 51 | ~250 | VA agent took us 0→17; rest of country still mostly empty |
| WELS nationwide (post-VA) | 17 | ~120 | VA agent took us 1→3; ~1,200 churches nationally |
| Foursquare nationwide | 2 | ~80 | VA agent opened with 2; nationally ~1,700 |
| Vineyard nationwide | 6 | ~80 | VA agent took us 1→6; nationally ~600 |
| Free Will Baptist nationwide | 18 | ~150 | VA agent opened with 18; ~2,200 nationally |
| Conservative Mennonite nationwide | 30 | ~150 | VA agent took us 2→26; nationally ~1,500 |
| Acts 29 nationwide | 80 | ~180 | originally Round A2 in V5→V6 plan |
| Remaining 85 PCA Warhurst signers | 4 attributed | ~80 | originally Round A3 in V5→V6 plan |
| Pastor-verification (post-VA spike) | ~470 | ~50 | data quality |
| Address normalization (post-VA spike) | ~1,640 | ~500 | data quality |

---

## Sequencing (8 rounds → ~750 net new + ~600 data-quality updates)

### Round 1: GMC nationwide expansion (4 agents, target +120)
**State scope split:**
- **Agent 1.1** — Southeast (TX/LA/MS/AL/GA/FL/SC/NC/TN/KY) — heaviest UMC defection
- **Agent 1.2** — Mid-Atlantic + Northeast (WV/MD/PA/OH/NY/NJ/DE/DC + New England) — VA already done, exclude VA
- **Agent 1.3** — Midwest + Plains (IL/IN/WI/MN/IA/MO/KS/NE/ND/SD/OK + AR)
- **Agent 1.4** — Mountain West + West Coast + AK/HI (CO/UT/WY/MT/ID/AZ/NM/NV/CA/OR/WA + AK/HI)

Source: globalmethodist.org/find-a-church + state GMC conference directories.

Drift watch: female-clergy holdovers from UMC era → YELLOW gender (don't auto-BLACK; GMC formed 2022 so some congregations are mid-transition).

**Expected delta:** 5,024 → ~5,144

---

### Round 2: WELS + ELS nationwide (4 agents, target +90)
- **Agent 2.1** — Wisconsin + Michigan WELS (heavy density)
- **Agent 2.2** — Minnesota + Dakotas + Iowa + Nebraska WELS
- **Agent 2.3** — Texas + Florida + Arizona + California WELS
- **Agent 2.4** — Pacific NW + Mountain West + remaining states WELS + ELS (Evangelical Lutheran Synod, very small)

Source: wels.net find-a-church. Default GREEN — most-confessional Lutheran body.

**Expected delta:** ~5,144 → ~5,234

---

### Round 3: Foursquare + Vineyard nationwide (4 agents, target +110)
**Foursquare (2 agents):**
- **Agent 3.1** — California Foursquare (heaviest; ICFG founding region)
- **Agent 3.2** — non-CA Foursquare nationwide

**Vineyard (2 agents):**
- **Agent 3.3** — California + Pacific NW + Mountain West Vineyard (Wimber-tradition founding region)
- **Agent 3.4** — South + Midwest + Northeast Vineyard

Drift watch: both denominations ordain women; default YELLOW gender. Vineyard cessationism/continuationism varies; YELLOW preaching unless verified.

**Expected delta:** ~5,234 → ~5,344

---

### Round 4: Free Will Baptist + Conservative Mennonite nationwide (4 agents, target +180)
**FWB (2 agents):**
- **Agent 4.1** — Southeast FWB (NC/SC/TN/KY/AL/GA/FL/MS/LA — historic stronghold)
- **Agent 4.2** — Texas + Oklahoma + Arkansas + Mid-Atlantic + Midwest FWB

**Conservative Mennonite + Brethren (2 agents):**
- **Agent 4.3** — Pennsylvania + Ohio + Indiana + Iowa + Kansas Plain congregations (Lancaster county density)
- **Agent 4.4** — Eastern PA Mennonite Church + Midwest BMA + Beachy Amish-Mennonite outside VA/Shenandoah

**Expected delta:** ~5,344 → ~5,524

---

### Round 5: Acts 29 nationwide (carried over from V5→V6 plan) (4 agents, target +60)
- **Agent 5.1** — California / Arizona / Nevada / Colorado Acts 29
- **Agent 5.2** — Texas / Oklahoma / New Mexico Acts 29
- **Agent 5.3** — Pacific Northwest (WA/OR/ID/MT/AK) Acts 29
- **Agent 5.4** — Midwest urban (IL/MN/OH/MI/WI/IN) Acts 29

Source: acts29.com/find-a-church.

**Expected delta:** ~5,524 → ~5,584

---

### Round 6: PCA Warhurst-signer drift documentation (4 agents, target +60)
- **Agent 6.1** — Northeast/Mid-Atlantic Warhurst PCA (Chesapeake, NJ, NY, PA presbyteries)
- **Agent 6.2** — Southeast Warhurst PCA (SC, GA, FL, NC, AL presbyteries)
- **Agent 6.3** — Texas + Mississippi + Louisiana Warhurst PCA presbyteries
- **Agent 6.4** — California + Korean PCA presbyteries Warhurst signers

Source: `docs/data/pca-warhurst-signers-2020.json` — 109 signers; 4 already attributed in V5.0; ~85 remaining.

Each adds church with YELLOW + cultural=red + populated `signatories.warhurst_protest_2020`.

**Expected delta:** ~5,584 → ~5,644

---

### Round 7: Pastor verification + address normalization sweep (4 agents, ~0 net add but ~700 updates)
- **Agent 7.1** — Pastor verification on 50K+ town SBC `Verify`-pastor records (post-2024 staff page check + LinkedIn cross-ref)
- **Agent 7.2** — Address normalization on Mountain West / Plains / Midwest incomplete records (denomination directory cross-check)
- **Agent 7.3** — ARP placeholder pastor sweep (35 ARP records with empty pastor field per NAPARC directory)
- **Agent 7.4** — Hampton Roads + Carolinas incomplete-address fills (highest Adam-personal-relevance)

**Expected delta:** ~5,644 → ~5,644 (data quality, no count delta)

---

### Round 8: Final 5,777 closer (4 agents, target +130)
Whatever remains undefined at this point — fill the gap to 5,777 with whichever denomination family yielded the most surprises in Rounds 1-6:

**Most likely targets:**
- **GMC** if Round 1 underperformed
- **More ARP non-SC** if Round 7 created appetite
- **Calvary Chapel non-CCA nationwide** (currently ~96)
- **REC (Reformed Episcopal Church)** nationwide
- **Conservative SBC Bible Belt fill** (state-by-state county seats)
- **EPC nationwide** (currently 27)

**Expected delta:** ~5,644 → ~5,777 ✅

---

### Round 9: V5.7.0 close-out
- Bump `directory_version` to V5.7.0 in `churches.json`
- Update changelog with Rounds 1-8 summary
- Update `directory-overview.html` roadmap "current" marker to "5,000 → 6,000"
- Update `directory-roadmap.html` V5.0 card to add 5,777 sub-milestone
- Optional: write a blog post celebrating the 5,777 cross
- Refresh dedup files for the next sprint

---

## Pre-flight checklist (run before kicking off Round 1, **after Wed midnight**)

```bash
cd /Users/moop_bot_pro/bible-reading-plan-bot

# 1. Pull latest (in case Adam committed dictionary work in between)
git pull --rebase origin main

# 2. Refresh dedup files
python3 -c "
import json
d = json.load(open('docs/data/churches.json'))
all_slugs = sorted([c.get('slug', c.get('id','??')) for c in d['churches']])
open('/tmp/all_existing_slugs.txt','w').write('\n'.join(all_slugs))
print(f'Refreshed {len(all_slugs)} slugs')
"

# 3. Refresh per-denomination dedup files (one for each round's target)
python3 -c "
import json
d = json.load(open('docs/data/churches.json'))
def emit(name, predicate):
    matches = [{'name': c.get('name',''), 'address': c.get('address',''), 'slug': c.get('slug', c.get('id',''))} for c in d['churches'] if predicate(c)]
    open(f'/tmp/existing_{name}.json','w').write(json.dumps(matches, indent=2))
    print(f'{name}: {len(matches)}')
emit('gmc', lambda c: 'GMC' in c.get('denomination','') or 'Global Methodist' in c.get('denomination',''))
emit('wels', lambda c: 'WELS' in c.get('denomination',''))
emit('foursquare', lambda c: 'Foursquare' in c.get('denomination',''))
emit('vineyard', lambda c: 'Vineyard' in c.get('denomination',''))
emit('fwb', lambda c: 'Free Will Baptist' in c.get('denomination',''))
emit('mennonite', lambda c: 'Mennonite' in c.get('denomination','') or 'Brethren' in c.get('denomination',''))
emit('acts29', lambda c: 'Acts 29' in c.get('denomination',''))
"

# 4. Verify schema template
python3 -c "import json; print(list(json.load(open('/tmp/SCHEMA_TEMPLATE.json')).keys()))"

# 5. Verify integrate-patch.js works
node .claude/skills/church-directory-enrichment/scripts/integrate-patch.js 2>&1 | head

# 6. Confirm clean working tree
git status
```

---

## Wednesday-fire-time prompt (drop into a fresh session)

```
Execute Roadmap V5.1 → 5,777 starting at Round 1 (GMC nationwide expansion). Pre-flight checks first per .claude/skills/church-directory-enrichment/ROADMAP-V5.1-TO-5777.md. Apply each agent patch as it lands; commit + push immediately. Brief under 200 words after each round. Stop and brief Adam at 60% usage so there's headroom for follow-up work.
```

---

## Estimated session budget

| Phase | Rounds | Agents | Tokens (est) | New churches |
|---|---:|---:|---:|---:|
| New denoms (1-4) | 4 | 16 | 2.5M | ~500 |
| Drift docs (5-6) | 2 | 8 | 1.2M | ~120 |
| Data quality (7) | 1 | 4 | 0.6M | 0 (~700 updates) |
| 5,777 closer (8) | 1 | 4 | 0.6M | ~130 |
| Close-out (9) | 1 | 0 | 0.05M | 0 |
| **TOTAL** | **9** | **32** | **~5M** | **~750 + ~700 updates** |

Comfortable inside fresh weekly 20x budget. Designed to stop at 60% usage with headroom for the next sprint (5,777 → V6.0 / 6,000).

---

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Foursquare requires login for full directory | Public find-a-church search returns ~80% of churches; skip private-only entries |
| Vineyard directory restricts public access | Pull from publicly-indexed church websites; cross-ref with Society of Vineyard Scholars roster |
| GMC site goes offline (still relatively new) | Fall back to per-state GMC conference directories (gmctexas.org etc.) |
| Org weekly-usage limit hits mid-round | Round-by-round commits mean no work is lost; resume next session |
| New denomination_family value triggers generator break | Test with one record first; add new family to STATEMENT_META in generate-church-pages.js if needed |
| /tmp scripts cleared between sessions | Pre-flight checklist re-creates them |

---

## Personal note for Adam

This sub-cycle is the natural follow-on from the 5,000-cross. The biggest pending item is GMC — Virginia alone showed there's a denomination-sized hole nationally. The 5,777 target is **776 net new from current** which is a single weekend's good work with fresh budget.

If you want to prioritize differently, the highest-marginal-value rounds (per gap-vs-effort) are:
1. **Round 1 (GMC)** — closes a denomination-wide hole, easy directories, fast wins
2. **Round 4 (FWB + Mennonite)** — fills two large historic-Protestant streams that the directory currently barely represents
3. **Round 6 (PCA Warhurst)** — completes a high-information-value drift dataset that already exists

Skip-or-defer candidates if budget tight:
- Round 7 (data quality) — important but doesn't change the church count; can be deferred to a maintenance week
- Round 8 (final closer) — only matters if you want the round number 5,777 specifically; we'll likely overshoot anyway

---

## Status when this doc was written (2026-05-03 morning)

- Directory at **5,024 churches** post Beech Island add (Adam's friend Greg Williams's church under pulpit transition; first primary-source-engagement record)
- Adam over 50% weekly usage; reserving rest for **Hermes / OpenClaw agent setup** (separate work stream — Chaps had tool-config issue today, Adam wants to fix)
- This doc parked. Wednesday after midnight = green light.
