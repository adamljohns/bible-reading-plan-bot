# Operating manual for agents working on this repo

This file is auto-loaded for any Claude Code agent that opens this directory. The original `README.md` documents the daily Bible-reading plan generator (`plan.py`) — a separate concern. **This file documents the MOOP Church Directory**, which is the primary product shipped from this repo to `usmcmin.org/churches.html` via GitHub Pages from `docs/`.

Owner: Adam Johns (U.S.M.C. Ministries). Target: 7,777 verified churches. **Current state: 4,911 (V4.9.7, 2026-04-30)**.

## What lives where

| Path | Purpose |
| --- | --- |
| `docs/data/churches.json` | **Single source of truth.** All church objects. Top-level keys: `meta`, `rubric`, `churches`, `total_churches`, `directory_version`, `directory_updated`, `directory_changelog`. |
| `docs/data/{warhurst,amr,lament,revoice,cbe,dallas,nashville}*.json` | Seven reference signature lists used for cultural-drift scoring. |
| `docs/data/statement-lists-manifest.json` | Maps signature-list `key` → file + array path + direction (red/green) + label. **Always loop the manifest, never hardcode list names.** |
| `generate-church-pages.js` | Node script — regenerates `docs/churches/<slug>.html` from `churches.json`. Run after every data change. |
| `docs/churches.html`, `docs/churches-{fxbg,dc,virginia}.html` | Hand-authored region pages that read `churches.json` at runtime via fetch. |
| `WEEKLY-ENRICHMENT-TRIGGER-CONFIG.md` | The Saturday cron prompt + auth setup. **Note:** its "27 canonical families" list is now stale — see real list below. |
| `HUMAN-TODO.md` | Human-attention queue — items autonomous agents could not safely resolve. Append new items here; mark resolved with `[x]` + ~strikethrough~. |
| `~/.claude/commands/enrich-churches.md` | The `/enrich-churches` slash command (4-wave parallel pattern; user-invokable). |

The repo is a regular git checkout. `main` deploys via GitHub Pages from `docs/`. There is **no CI** — `git push origin main` is the deploy.

## Schema invariants — NEVER violate these

These are non-negotiable. Every breakage has historically broken either the live site, the page generator, or downstream filtering.

1. **`slug` MUST equal `id`.** The generator uses `church.id` for the HTML filename. Mismatch creates orphan pages and broken cross-links.
2. **All ID comparisons use `String(c.id)`.** Some legacy entries have numeric IDs.
3. **Social fields are TOP-LEVEL.** `facebook`, `youtube`, `instagram`, `twitter`, `vimeo`, `pastor_facebook`, `pastor_twitter`, `pastor_instagram`, `pastor_linkedin`. **Never** nest them in a `social` object.
4. **`engagement` defaults: all-false except `researched_website: true`.** When you research a church via WebFetch you've earned the true on `researched_website`. Don't claim the others.
5. **`signatories` has exactly 7 keys**, all empty arrays by default: `warhurst_protest_2020`, `amr_2026`, `letter_of_lament_2025`, `revoice_2018_2026`, `cbe_egalitarian_2026`, `dallas_statement_2018`, `nashville_statement_2017`.
6. **`signatures_aggregate` is `"none" | "green" | "red" | "mixed"`** — recomputed from current signatories: any red-direction list populated → `red`; any green → `green`; both → `mixed`; neither → `none`.
7. **No fabricated churches.** If WebSearch can't verify the church, skip it. If you can't verify the pastor, set `pastor: "Verify"` rather than guess.
8. **Directory HTML uses `escapeHtml()` everywhere** — never inject unescaped church data into HTML. The generator does this for you; don't hand-write HTML for a church.

## `denomination_family` — known mess (fix in flight)

The repo has accumulated **73 distinct values** where it should have ~30. There are duplicate labels for the same federation. Until a consolidation refactor lands, use the **dominant label** for each federation when adding new entries:

| Use this | Avoid these duplicates |
| --- | --- |
| `Presbyterian (PCA)` (209) | `PCA` (58) |
| `Presbyterian (OPC)` (68) | `OPC` (55) |
| `Presbyterian (ARP)` (45) | `ARP` (37) |
| `Presbyterian (EPC)` (27) | `EPC` (19) |
| `Presbyterian (URCNA)` (43) | `URCNA` (split count) |
| `Lutheran (LCMS)` (171) | `LCMS` (3) |
| `Anglican (ACNA)` (77) | `ACNA` (2) |
| `Reformed Baptist` (170) | `RB` (3), `Reformed` (1), `ARBCA / Reformed Baptist (1689)` (12) |
| `Independent Baptist` (71) | `IFB` (1) |
| `Southern Baptist (SBC)` (1823) | `SBC` (3); be careful with subtypes |
| `Conservative Congregational (CCCC)` (7) | `CCCC` (1) |
| `Anglican (REC — Reformed Episcopal)` | `Reformed Episcopal (REC)` |
| `Free Reformed Churches of North America / Three Forms of Unity` | `Free Reformed Churches` |
| `Heritage Reformed Congregations / Three Forms of Unity` | `Heritage Reformed` |
| `Reformed (RCUS / German Reformed)` | `RCUS` |
| `RPCNA / Covenanter` | `RPCNA` |

**Other valid families** (no current splits): `Non-Denominational`, `Baptist (Other)`, `Calvary Chapel`, `Sovereign Grace Churches`, `EFCA`, `Church of Christ`, `Wesleyan / Nazarene`, `Acts 29`, `Pentecostal / Charismatic`, `Methodist (GMC)`, `Methodist (UMC)`, `Christian & Missionary Alliance`, `Catholic`, `Lutheran (ELCA)`, `Lutheran (Other)`, `Episcopal (TEC)`, `Progressive Mainline`, `Presbyterian (PCUSA)`, `Presbyterian (KAPC / Korean American)`, `Presbyterian (CREC)`, `Presbyterian (BPC)`, `Presbyterian (Other)`, `Bible Presbyterian Church`, `CREC`, `IFCA International`, `Restoration Movement`, `WELS`, `PRCA`, `NRC (Netherlands Reformed)`, `Anglican (AMiA)`, `Anglican (CANA / CONNAM)`, `Anglican (ACC — Continuing)`, `Converge`, `RPCGA / Westminster Standards`, `Orthodox`, `Other`.

**Do not invent new family labels.** If a church doesn't fit, use `Other` and explain in `denomination_detail`.

## Rubric & ratings (10 categories)

`scores.{christology,scripture,soteriology,gender,leadership,preaching,mission,cultural,mens_discipleship,denominational}` — each `green | yellow | red | black`. `overall_rating` rolls them up. Cheat sheet:

- **GREEN**: 6+ greens in core categories (Christology, Scripture, Soteriology, Gender, Leadership, Men's Discipleship) + no reds.
- **YELLOW**: mixed signal; safe-default for unverified.
- **RED minimum** for: female pastors/elders, egalitarian gender stance, CBF/ABCUSA/PCUSA/UMC-post-split/TEC affiliation.
- **BLACK** for: LGBTQ-affirming, denial of orthodox Christology (Oneness Pentecostal, Mormon, JW), prosperity gospel, Side B platforming, apostate.

`overall_label` is a short human-readable summary string (e.g., `"PCA — Confessional Westminster Presbyterian"`). Generator displays it on the church card.

## Cultural-drift watch (signature lists)

The 7 reference lists have a **direction** (red or green) defined in the manifest. Loop the manifest, never hardcode.

| Direction | Lists | Meaning |
| --- | --- | --- |
| **red** | warhurst_protest_2020, amr_2026, letter_of_lament_2025, revoice_2018_2026, cbe_egalitarian_2026 | Soft-progressive PCA wing, Side B sexuality, egalitarian advocacy |
| **green** | dallas_statement_2018, nashville_statement_2017 | Orthodox sexual ethics + anti-CRT alignment |

**Drift downgrade rule** (proven 2026-04-30): a pastor matching a **red** list **with state/presbytery corroboration** triggers:
- `scores.cultural = "red"`
- `overall_rating: "yellow"` if it was green
- tags `needs-rating-review` + `cultural-drift-flag`

**Without state corroboration, only populate the signatories field — do not change the rating.** Common-name false-positives (e.g., "John Smith" matching one of 22,901 Nashville signers) are real; the bar for rating impact is geographic match.

The driver scripts from the 2026-04-30 session live in `/tmp/signature-crossref.js` (report) and `/tmp/apply-signatures.js` (apply). They were one-shot — recreate as needed.

## Change workflow — the SAFE pattern

Every data change goes through this pipeline. Skipping steps will desynchronize HTML pages from the JSON.

```bash
# 1. Make your data change (preferably via a Node script — see template below)
node /tmp/your-change.js

# 2. Regenerate ALL HTML pages
node generate-church-pages.js

# 3. If you DELETED a church, also remove its orphan HTML
rm docs/churches/<deleted-slug>.html

# 4. Stage + commit + push
git add -A docs/
git commit -m "$(cat <<'EOF'
Round N: <descriptive title>

[Body — adds, state distribution, notable finds, drift markers, scandal flags]

Total: <before> -> <after>.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git pull --rebase origin main   # other threads may have committed
git push origin main
```

Use the heredoc form with **single-quoted EOF** to avoid shell-escape gotchas in commit bodies.

## Multi-agent expansion pattern (proven 2026-04-30, +250 churches in 11 commits)

For thin-denomination expansion or large enrichment passes, **never edit `churches.json` directly from background agents**. The pattern:

1. Spawn 2–4 background research agents in parallel via the `Agent` tool with `run_in_background: true`. Each agent:
   - Researches a specific denomination/region scope
   - Writes a patch file to `/tmp/patch-<slug>.json` with shape `{"new_churches": [...]}`
   - Does NOT touch `churches.json`, does NOT regen, does NOT commit
2. Foreground does data-quality work (pastor verification, cross-reference, dedup hunting) while agents run.
3. As each patch lands, **integrate via a fill-defaults script**, then regen + commit. Template:

```javascript
#!/usr/bin/env node
const fs = require('fs');
const path = '/Users/moop_bot_pro/bible-reading-plan-bot/docs/data/churches.json';
const data = JSON.parse(fs.readFileSync(path, 'utf8'));
const patch = JSON.parse(fs.readFileSync('/tmp/patch-<slug>.json', 'utf8'));

const baseEng = {
  visited_facility: false, attended_services: false, viewed_online_services: false,
  researched_website: true, know_members_personally: false,
  interacted_with_leadership: false, attended_personally: false,
};
const baseSig = {
  warhurst_protest_2020: [], amr_2026: [], letter_of_lament_2025: [],
  revoice_2018_2026: [], cbe_egalitarian_2026: [],
  dallas_statement_2018: [], nashville_statement_2017: [],
};

function fill(c) {
  for (const k of ['facebook','youtube','instagram','twitter','vimeo']) {
    if (c[k] === '' || c[k] === null) delete c[k]; // strip empty social placeholders
  }
  const stateMatch = (c.address || '').match(/, ([A-Z]{2}) \d{5}/);
  const stateCode = stateMatch ? stateMatch[1] : null;
  return {
    ...c,
    slug: c.id,
    engagement: c.engagement || baseEng,
    signatories: c.signatories || baseSig,
    signatures_aggregate: c.signatures_aggregate || 'none',
    region: c.region || (stateCode ? stateCode.toLowerCase() : 'rest_of_us'),
    url_research_status: c.url_research_status || 'verified',
  };
}

const existingIds = new Set(data.churches.map(c => String(c.id)));
let added = 0, skipped = 0, vacancyDowngrades = 0;
for (const c of patch.new_churches) {
  if (existingIds.has(String(c.id))) { skipped++; continue; }
  const filled = fill(c);
  // Vacancy auto-downgrade
  if (typeof filled.pastor === 'string' && /^vacant/i.test(filled.pastor)) {
    filled.overall_rating = 'yellow';
    filled.tags = [...(filled.tags || []), 'needs-rating-review', 'pulpit-vacant'];
    vacancyDowngrades++;
  }
  data.churches.push(filled);
  existingIds.add(String(c.id));
  added++;
}
data.total_churches = data.churches.length;
data.directory_updated = new Date().toISOString().slice(0,10);
fs.writeFileSync(path, JSON.stringify(data, null, 2) + '\n');
console.log(`Added ${added}; skipped ${skipped}; vacancy-downgrades ${vacancyDowngrades}; total ${data.churches.length}`);
```

After every 3–5 commits, **re-run the signature cross-reference** so new pastors get attributed. Run the report first, eyeball the matches (especially the red/mixed ones), then apply.

## Things to flag, never auto-fix

- **URL mismatch / address mismatch records.** A `review_flag.website_status: "dead"` or `overall_label` containing "URL mismatch" means prior research caught a problem that needs human-judgment investigation. Don't paper over by silently changing the website. Append to `HUMAN-TODO.md` if you discover a new one.
- **Renamed/merged churches.** Use a `successor: "<new-slug>"` and `predecessor_ids: [...]` pointer rather than deleting. See `first-baptist-shawnee-ok` → `heritage-church-shawnee-ok` precedent.
- **Phantom churches.** If WebSearch confirms the church does not exist (no website, no facebook, no traceable address), it's safe to delete — but log the deletion in the commit message with the verification trail.
- **Female senior pastor in SBC-listed church** → BLACK + `credentials-committee-referral` note (Saddleback / Fern Creek / Bayside precedent).
- **PCA pastor on Warhurst / AMR / Lament list** → YELLOW with `cultural=red`, plus `needs-rating-review` tag (proven pattern).
- **Pulpit transitions / leadership scandals** → `scandal_flag` field (free text) + `needs-rating-review` tag.

## Things NOT to do

- **Don't edit `churches.json` directly from a background agent** — write a patch, foreground integrates.
- **Don't invent new `denomination_family` labels** — pick the dominant one from the table above or use `Other`.
- **Don't auto-apply red-direction signature matches without state/presbytery corroboration** — common-name FP risk.
- **Don't skip `node generate-church-pages.js`** after a JSON change — the regional pages read JSON at runtime, but the per-church pages under `docs/churches/<slug>.html` are pre-generated and will go stale.
- **Don't delete records to "clean up" without a verification trail.** Use defunct flags + successor pointers.
- **Don't bump `directory_version`** unless you're closing out a meaningful release. Multiple commits at the same version is normal.
- **Don't hand-edit HTML in `docs/churches/`** — those are generator output. Edit the JSON and regen.

## Personal connections — rate with care

Adam knows several pastors personally. Don't downgrade these without strong cause; flag for his review instead. See the memory file `project_church_directory.md` for the current list (Connection Church Buda TX, Veritas Federal Way WA, Forest Baptist Louisville KY, Salt Church Hartfield VA, Grace Bible Wappingers Falls NY, FRDM Stafford VA, etc.).

## Cross-thread coordination

A separate Claude Code thread sometimes runs cross-pollination work between `usmcmin.com/citizen.html` ↔ `usmcmin.org/churches.html`. If `git pull --rebase` shows a conflict on `churches.html` or other shared files, **resolve cleanly** — that thread's intent is additive (UI/UX), not data-overwriting.
