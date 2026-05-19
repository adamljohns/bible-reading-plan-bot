# Cori → main reconciliation playbook
**Created:** 2026-05-18 during the cori-pre-rebase audit
**Pause window:** ~3 hours while parallel Claude Code session keeps working

## Safety net
- Backup branch: `backup/cori-pre-rebase-2026-05-18` (preserves all V4.9.1–V4.9.5 work in case anything goes wrong)
- Dirty files at pause time (safe to ignore):
  - `tmp/denom_corrections_auto_safe.json`
  - `tmp/existing_va_namesonly.json`

## State at pause
- **Local main HEAD:** `90e4de64f` (V4.9.5 / 4,377 churches)
- **Origin main HEAD:** `485d64365` (V5.7.0 / 7,596 churches)
- **Parallel session pushed +25 commits, +3,219 churches since 2026-04-25**
- Major parallel additions:
  - Founders Ministries cross-reference (+196 churches, +170 tags)
  - R26–R31 famous-politician + notable-attendees rounds
  - `/directory-politicians.html` (R29)
  - OPC nationwide expansion + Hampton Roads non-Pres sweep
  - Numeric rating scale (4.0–9.7) layered onto green/yellow/red/black
  - Networks + Speakers 5-Phase tracker
  - Multiple dedup passes, normalization

## When we resume — re-audit step

Re-run this audit before any merge attempt (parallel session may have moved further):

```bash
cd /Users/adamjohns/bible-reading-plan-bot && git fetch origin && \
python3 -c "
import json, subprocess
r = subprocess.run(['git', 'show', 'origin/main:docs/data/churches.json'], capture_output=True, text=True)
data = json.loads(r.stdout)
churches = data.get('churches', [])
by_id = {c['id']: c for c in churches if 'id' in c}
ids = [
  'mclean-bible-church-vienna','the-mount-church','the-mount-church-stafford',
  'mt-ararat-baptist-stafford','brock-road-baptist-church',
  'chancellor-christian-church-spotsylvania','bedford-baptist-church',
  'first-baptist-clintwood','arc-heights-church-richmond-va',
  'first-baptist-lebanon','garden-city-baptist-roanoke','buena-vista-baptist',
  'pca-christ-the-king-roanoke-va','opc-bethel-leesburg-va',
  'arp-redeemer-blacksburg-va','lcms-our-savior-lynchburg-va',
  'lord-of-life-lutheran-fairfax','christ-community-church-leesburg',
]
for cid in ids:
    rec = by_id.get(cid)
    if rec:
        print(f'{cid:50} denom={rec.get(\"denomination\",\"\")[:25]:25} rating={rec.get(\"overall_rating\")}')
    else:
        print(f'{cid:50} MISSING')
"
```

## Changes to re-apply (audit findings as of 2026-05-18 pre-pause)

### Confirmed already-on-origin (DO NOT re-apply unless audit shows regression):
- `first-baptist-lynchburg-va` → dead ✓
- `fredericksburg-assembly-of-god-spotsylvania` → dead ✓
- `short-pump-baptist-church` → dead ✓
- `concordia-lutheran-church-manchester-ct` → ELCA black ✓
- `stonebridge-church-mckinney-tx` → UMC black ✓
- `colonial-avenue-baptist-roanoke` → black (parallel went further than my red)
- `first-baptist-church-boise-id` → ABCUSA black ✓
- `reston-community-pca` → green ✓
- `cornerstone-bible-church-sterling` → still yellow ✓

### DO NOT regress these (parallel has stronger calls):
- `lord-of-life-lutheran-fairfax` → BLACK on origin (my green-hunter was wrong; LGBTQ-affirming or female pastor probably)
- `christ-community-church-leesburg` → RED on origin (LCMS but with issues my green-hunter missed)

### Re-apply if origin still doesn't have these:

**McLean Vienna Platt walk-back** — verify score_notes.leadership doesn't still cite "David Platt (Lead Pastor)"; Platt stepped back late 2023 to Radical, Dale Sutherland + Mike Kelsey now lead.

**The Mount Fxbg** scalar fixes:
- `founded`: "1907 (founded as Mount Ararat Baptist Church)"
- `services`: "Sundays 9:15 AM & 10:45 AM"
- `youtube`: "https://www.youtube.com/@themountva"
- score_notes.denominational: scrub "rendered/fetch/held" jargon (V4.9.1)

**The Mount Stafford** scalar fixes:
- `founded`: "1907 (founded as Mount Ararat Baptist Church)"
- `services`: "Sundays 8:30 AM, 10:00 AM, 11:30 AM"
- `youtube`: "https://www.youtube.com/@themountva"
- `pastor`: "Adam Sauer (Lead Pastor, since 2022)"
- `pastor_credentials`: "Adam Sauer — M.Div. and M.A. in Nonprofit Management, North Park Theological Seminary (ECC-affiliated, Chicago). Unusual pipeline for a historic Baptist congregation."
- `denomination`: "Baptist (BGAV)"
- `denomination_family`: "Baptist (BGAV)"
- score_notes.leadership: "Plurality of elected elders per 1 Tim 3:1–7 and Titus 1:5–9. Lead Pastor Adam Sauer (since 2022)…"

**Mt. Ararat dedup** — merge `mt-ararat-baptist-stafford` into `the-mount-church-stafford` (same address 1112 Garrisonville Rd; fix SBC → BGAV mis-tag). Replace `docs/churches/mt-ararat-baptist-stafford.html` with redirect HTML to `the-mount-church-stafford.html` (note: parallel session may have rebuilt this page; verify before overwriting).

**Brock Road dedup** — merge `brock-road-baptist-church` into `chancellor-christian-church-spotsylvania` (same name, address 11409 Brock Rd, pastor Mark Dunn, website chancellorchristian.org). Replace `brock-road-baptist-church.html` with redirect to `chancellor-christian-church-spotsylvania.html` (note: parallel session may have rebuilt this page too).

**Bedford Baptist + Bonsack Roanoke** SBC→BGAV per V4.9.2.

**VA yellow→GREEN flips from V4.9.3** (verify each still yellow on origin before flipping):
- `first-baptist-clintwood` → BFM2000 est 1894
- `hillsville-baptist` → BFM 1963 + 1998
- `hopeful-baptist-mechanicsville` → SBCV, all-male staff, hopefulbc.com (not hopefulbaptist.com)
- `garden-city-baptist-roanoke` → BFM2000 + Charlie Lanier SEBTS (pastor name correction from Brian Willard)
- `christ-community-church-chesterfield` → C&MA
- `harvest-bible-chapel-glen-allen` → now Harvest Bible Church (harvestbiblechurch.org), Jon Walters

**VA yellow→RED flips from V4.9.3** (verify each still yellow on origin):
- `buena-vista-baptist` → CBF + husband-wife co-pastors Scott Covington/Danika Deva
- `arc-heights-church-richmond-va` → ARC + husband-wife co-pastors Josh & Crystal Whitlow (ARC = MOOP auto-red)
- `first-baptist-lebanon` → BGAV-only post-Nov-2023
- `bedford-road-baptist-bedford` → BGAV-only post-Nov-2023

**V4.9.4 confessional VA adds (27 records)** — record IDs are listed in `tmp/va_green_hunter_out.json` if it still exists; otherwise the IDs are:
- 12 PCA: pca-christ-the-king-roanoke-va, pca-westminster-roanoke-va, pca-providence-roanoke-salem-va, pca-boonsboro-lynchburg-va, pca-mercy-forest-va, pca-fellowship-bedford-va, pca-grace-covenant-blacksburg-va, pca-providence-christiansburg-va, pca-holy-cross-staunton-va, pca-drapers-valley-draper-va, pca-christ-presbyterian-harrisonburg-va, pca-eagle-heights-winchester-va
- 10 OPC: opc-bethel-reformed-fredericksburg-va, opc-west-creek-henrico-va, opc-bethel-leesburg-va, opc-grace-lynchburg-va, opc-acacia-reformed-manassas-va, opc-knox-reformed-mechanicsville-va, opc-garst-mill-roanoke-va, opc-staunton-va, opc-peninsula-reformed-yorktown-va, opc-ketoctin-purcellville-va
- 2 ARP: arp-redeemer-blacksburg-va, arp-wellspring-daleville-va
- 1 REC: rec-all-saints-lynchburg-va
- 1 ACNA: acna-good-shepherd-charlottesville-va
- 1 LCMS: lcms-our-savior-lynchburg-va

For each MISSING from origin: pull full record from backup branch.

### Address fixes from V4.9.5 (verify each):
- `lord-of-life-lutheran-fairfax` → 5114 Twinbrook Rd, Fairfax, VA 22032 (but DON'T touch the rating — parallel has it black)
- `christ-community-church-leesburg` → 818 South King Street, Leesburg, VA 20175 (don't touch rating)
- `reston-community-pca` → 2620 Reston Parkway, Herndon, VA 20171 (rating green already correct)
- `good-shepherd-anglican-roanoke-va` → if origin doesn't have it, walk back from green to yellow + review_flag (possible phantom; conflated with Lynchburg Good Shepherd)

## Wayback bug fixes to address (per pause-time audit)
- 102 records with `enrichment_sources` vs `enrichment_sources_live` length mismatch
- 57 records with wayback URL in sources[i] not matching its paired live URL in sources_live[i]
- 4,649 records with sources but zero Wayback coverage (95% of cited evidence is live URLs)

Recommended fix: replace `generate-church-pages.js → sourcesSection()` index-based pairing with a parser that extracts the original URL from the wayback URL itself (it's embedded after the timestamp).

## Source-of-truth files for restoration
If anything is missing, pull from backup branch:
```bash
git show backup/cori-pre-rebase-2026-05-18:docs/data/churches.json > /tmp/backup_churches.json
git show backup/cori-pre-rebase-2026-05-18:tmp/va_green_hunter_out.json > /tmp/backup_green_hunter.json
git show backup/cori-pre-rebase-2026-05-18:tmp/va_deepdive_v50_out.json > /tmp/backup_va_deepdive.json
git show backup/cori-pre-rebase-2026-05-18:tmp/denom_corrections_strict.json > /tmp/backup_denom_corrections.json
```

## Resume procedure
1. `git fetch origin && git log --oneline HEAD..origin/main | head -20` — see what parallel session added
2. Re-run audit block above to see which V4.9.x changes are still missing
3. Reset main to origin/main: `git reset --hard origin/main`
4. Re-apply only the changes that are still missing
5. Generate pages, commit, push

## Open questions to confirm with user before proceeding
- Numeric rating scale (4.0–9.7) on origin — preserve it or replace with V4.9.x green/yellow/red/black for records I touch?
- Do they want the Mt. Ararat / Brock Road dedups re-attempted, or accept the parallel session's split records?
- VA page filter — they noted "278 in Virginia" but my rollups show 364; figure out the filter rule and decide if Fxbg should be excluded.
