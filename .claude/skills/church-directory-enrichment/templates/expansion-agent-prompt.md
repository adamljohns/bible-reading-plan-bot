# Expansion-agent prompt template

Copy this prompt into an `Agent` tool call with `run_in_background: true` and fill in the placeholders. The agent writes a patch to `/tmp/patch-<scope-slug>.json` — it does NOT modify `churches.json` directly. Foreground integrates via `scripts/integrate-patch.js`.

## Placeholders to fill

- `<DENOMINATION_LABEL>` — human-readable name, e.g. "Reformed Baptist (1689)" or "PCA"
- `<SCOPE_SLUG>` — kebab-case slug for the patch filename, e.g. "rb-midatl-midwest" or "pca-mtn-plains"
- `<TARGET_STATES>` — list of states the agent should focus on, e.g. "Idaho (ID), Nevada (NV), Utah (UT), Kansas (KS)"
- `<TARGET_COUNT_RANGE>` — e.g. "20-40"
- `<DENOMINATION_FAMILY_VALUE>` — the EXACT canonical label from CLAUDE.md (e.g. `Presbyterian (PCA)`, `Lutheran (LCMS)`, `Reformed Baptist`, `Sovereign Grace Churches`)
- `<DENOMINATION_VALUE>` — the short denomination string for the `denomination` field (e.g. `PCA`, `LCMS`, `URCNA`)
- `<RUBRIC_DEFAULT_RATING>` — usually `green` for confessional Reformed/Presbyterian/LCMS; `yellow` for SBC/Acts 29 unverified
- `<OFFICIAL_DIRECTORY_URLS>` — primary federation directory(ies), e.g. "https://locator.lcms.org/", "https://opc.org/locator.html", "https://www.urcna.org/"
- `<DEFAULT_ASSESSMENT_TONE>` — 1-line guidance for the assessment paragraph

## Prompt

```
You are researching <DENOMINATION_LABEL> congregations for the MOOP Church
Directory at /Users/moop_bot_pro/bible-reading-plan-bot. Do NOT modify
churches.json directly — write a patch file to /tmp/patch-<SCOPE_SLUG>.json
with shape {"new_churches": [...]}.

GOAL: Find <TARGET_COUNT_RANGE> verified <DENOMINATION_LABEL> congregations
in these states where the directory is currently thin:
<TARGET_STATES>

IDENTIFICATION CRITERIA:
- Use the official federation directory: <OFFICIAL_DIRECTORY_URLS>
- Each candidate church must be confirmed federation-affiliated
- Cross-reference any per-presbytery / per-classis / per-district sites

DEDUP — before adding any church, check it's not already in the directory:
```
jq -r '.churches[] | select(.denomination_family == "<DENOMINATION_FAMILY_VALUE>") | "\(.id)|\(.name)|\(.address // "")"' \
  /Users/moop_bot_pro/bible-reading-plan-bot/docs/data/churches.json \
  | grep -i "candidate-name-or-city"
```
Note: some federations have label splits — also dedup against alternate
labels per the CLAUDE.md table at the repo root.

VERIFICATION REQUIRED PER CHURCH:
1. Live website OR live federation directory listing (note "no-website" tag if listing-only)
2. Real pastor name from /staff or /about page (or federation directory)
3. Physical address: street + city + state + zip
4. NO defunct churches, NO fabricated data — if WebSearch can't verify, SKIP

OUTPUT — each new_churches[i] object:
{
  "id": "slug-form-name-city-st",
  "name": "Church Name",
  "address": "123 Main St, City, ST 12345",
  "pastor": "Pastor Name (verified)",
  "pastor_credentials": "Unknown" or seminary/credentials,
  "founded": "YYYY" (omit if unknown),
  "type": "<DENOMINATION_LABEL>",
  "denomination": "<DENOMINATION_VALUE>",
  "denomination_family": "<DENOMINATION_FAMILY_VALUE>",
  "website": "https://...",
  "facebook": "https://..." (top-level if found, OMIT field if not — never set to ""),
  "youtube": "..." (top-level),
  "instagram": "..." (top-level),
  "has_mens_ministry": true | false,
  "has_kids_ministry": true | false,
  "overall_rating": "<RUBRIC_DEFAULT_RATING>",
  "overall_label": "<DENOMINATION_LABEL> — <one-line denominational descriptor>",
  "scores": {
    "christology": "green", "scripture": "green", "soteriology": "green",
    "gender": "green", "leadership": "green", "preaching": "green",
    "mission": "green", "cultural": "green",
    "mens_discipleship": "green" or "yellow" if no men's group,
    "denominational": "green"
  },
  "score_notes": {
    "denominational": "<one-line denominational tradition note>",
    "gender": "Male-only ordination per <denominational standard>",
    "mens_discipleship": "..." brief
  },
  "assessment": "2-4 sentences. <DEFAULT_ASSESSMENT_TONE>",
  "tags": ["<denomination-slug>", "<tradition-slug>", "<city-slug>", "<state-slug>"],
  "gender_detail": "...",
  "denomination_detail": "<DENOMINATION_LABEL> — <presbytery/classis/district if known>",
  "enrichment_notes": "Verified via <federation-directory> + church website on YYYY-MM-DD.",
  "enrichment_sources": ["https://federation-directory", "https://church-site"]
}

DRIFT WATCH — if a pastor name appears on any of these lists, flag in
enrichment_notes (do not auto-rate; foreground will run the cross-reference):
- Warhurst Protest 2020 (red), AMR 2026 (red), Letter of Lament 2025 (red)
- Revoice 2018-2026 (red), CBE Egalitarian Network 2026 (red)
- Dallas Statement 2018 (green), Nashville Statement 2017 (green)

PROCESS:
1. Pull the federation roster for <TARGET_STATES>
2. For each candidate, WebFetch the church website to verify pastor + address
3. Build the patch incrementally with rolling dedup checks
4. Quality > quantity — skip ambiguous candidates with a note in your final summary

OUTPUT: write final patch to /tmp/patch-<SCOPE_SLUG>.json. Print a brief
end-of-run summary with state counts and any notable churches/finds.
Time budget: ~25-35 minutes.

DO NOT modify churches.json. DO NOT run the page generator. DO NOT commit.
```

## Tips for the foreground operator

- Spawn 2–4 of these in parallel via `run_in_background: true` so foreground can do other work while they research.
- Pick non-overlapping states/federations across agents. If two agents target the same federation, they'll waste effort on dedup.
- After each agent completes, run `node scripts/integrate-patch.js /tmp/patch-<SCOPE_SLUG>.json` from the repo root, then `scripts/regen-and-commit.sh` with a descriptive title and body.
- After every 3–5 commits, run `scripts/signature-crossref.js` followed by `scripts/apply-signatures.js` so newly-added pastors get cross-referenced.
