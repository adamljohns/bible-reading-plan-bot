---
name: church-directory-enrichment
description: Run an enrichment session on the MOOP Church Directory at docs/data/churches.json — add new verified churches via parallel research agents, verify pastor names, run the signature cross-reference for cultural-drift detection, or apply denomination corrections. Use whenever the user wants to grow the directory toward 7,777, expand any denomination ("add more PCA," "expand LCMS in the Midwest," "fill in URCNA"), verify pastors ("check who's pastor at X"), look for cultural drift ("re-run the signature pass"), correct denomination mismatches, or do address normalization. Also use when the user says "enrich the directory," "growing the directory," "the church directory work," "thin denomination," "Hampton Roads sweep," or names a Reformed/conservative federation by acronym (PCA, OPC, ARP, EPC, URCNA, LCMS, RB, SGC, etc.). Triggers in the bible-reading-plan-bot repo or when the user mentions usmcmin.org/churches.html.
---

# MOOP Church Directory Enrichment

You are about to do enrichment work on the MOOP Church Directory. The full operating manual is in `CLAUDE.md` at the repo root — **read it once at the start of any session** for schema invariants, the denomination_family mess, the rubric, drift-watch rules, and forbidden actions.

This skill packages the proven multi-agent workflow plus reusable scripts that live alongside this file in `scripts/` and `templates/`. Use the bundled scripts; do not recreate them in `/tmp/`.

## At-a-glance: what's in this skill

| Path (relative to this SKILL.md) | Purpose |
| --- | --- |
| `scripts/stats.sh` | Print current directory stats (total, denom families, verify-pastor count, etc.). Run first. |
| `scripts/integrate-patch.js <patch-path>` | Generic integrator — takes a `{"new_churches": [...]}` patch and adds with default-fills. Handles vacancy auto-yellow. |
| `scripts/signature-crossref.js` | Builds `/tmp/signature-matches.json` report by matching pastor names across the 7 reference signature lists. |
| `scripts/apply-signatures.js` | Applies the report — populates `signatories` field, recomputes `signatures_aggregate`. Drift downgrades require a state-corroborated red match (driven from `confirmed-red-drift.json` if present). |
| `scripts/regen-and-commit.sh "<commit title>" "<commit body>"` | Runs the generator + git add/commit/push with the heredoc-EOF pattern + pull-rebase. |
| `templates/expansion-agent-prompt.md` | Parameterized prompt for spawning a denomination-expansion research agent. Fill in the bracketed placeholders. |

## The workflow (proven 2026-04-30, +250 churches in 11 commits)

### 1. Orient (always do this first)

```bash
.claude/skills/church-directory-enrichment/scripts/stats.sh
git log --oneline -5
git status --short
```

If any uncommitted work shows, deal with it before starting.

### 2. Plan the round

Decide what the round will accomplish. Typical rounds:
- **Expansion**: spawn 2–4 background agents on thin denominations (use `templates/expansion-agent-prompt.md`)
- **Pastor verification**: foreground WebFetch on `pastor: "Verify"` records in a specific federation
- **Signature cross-reference**: re-run after expansion adds new pastors
- **Denomination correction**: scan for `overall_label`-vs-`denomination_family` mismatches and write a per-record correction script
- **Drift sweep**: spawn an agent on a single signature list and confirm matches

For expansion rounds, **always prefer multi-agent + foreground in parallel** — agents do scoped research in background, foreground does data-quality work, integration happens as patches land.

### 3. Spawn expansion agents (background)

Read `templates/expansion-agent-prompt.md`, fill in the placeholders for each scope, and launch via the `Agent` tool with `run_in_background: true`. Each agent writes to `/tmp/patch-<scope-slug>.json`. Do NOT let agents touch `churches.json` directly.

### 4. Foreground while agents run

Pick non-overlapping work:
- WebFetch staff/leadership pages for `pastor: "Verify"` records in federations the agents AREN'T touching
- Investigate `overall_label` mismatches surfaced from prior research
- Re-run signature cross-reference if it's been ≥3 commits

### 5. Integrate patches as they land

```bash
node .claude/skills/church-directory-enrichment/scripts/integrate-patch.js /tmp/patch-<scope-slug>.json
```

The script:
- Skips ID collisions (logs them)
- Fills schema defaults: `slug`, `engagement` (researched_website=true), `signatories` (7-key shape), `signatures_aggregate=none`, `region` (parsed from address), `url_research_status`
- Strips empty social placeholders (`facebook: ""`)
- Auto-downgrades to YELLOW with `pulpit-vacant` + `needs-rating-review` tags if `pastor` starts with "Vacant"
- Bumps `total_churches` and `directory_updated`

### 6. Regen + commit + push

```bash
.claude/skills/church-directory-enrichment/scripts/regen-and-commit.sh \
  "Round N: <title>" \
  "$(cat <<'EOF'
[Multi-line body — adds, state distribution, notable finds, drift markers, scandal flags]

Total: <before> -> <after>.
EOF
)"
```

The script handles: `node generate-church-pages.js`, `git add -A docs/`, the heredoc commit with `Co-Authored-By` line, `git pull --rebase origin main`, and `git push`.

### 7. Brief the user

Under 200 words per round. Lead with the count delta. Highlight notable adds (heritage parishes, well-known pastors, drift markers caught). Flag false-positive risks for any signature matches without state corroboration.

### 8. After every 3–5 commits — signature cross-reference

```bash
node .claude/skills/church-directory-enrichment/scripts/signature-crossref.js
# Inspect /tmp/signature-matches.json
# Especially look at the red_only and mixed direction breakdowns
node .claude/skills/church-directory-enrichment/scripts/apply-signatures.js
```

The apply script populates `signatories` for ALL matches but only triggers rating downgrades for confirmed-red drift cases. Hardcode known confirmed-red IDs in `apply-signatures.js` or maintain `confirmed-red-drift.json` next to it.

## Drift watch — non-negotiable rules

A pastor name matching a red-direction signature list (`warhurst_protest_2020`, `amr_2026`, `letter_of_lament_2025`, `revoice_2018_2026`, `cbe_egalitarian_2026`) means:

1. **Without state/presbytery corroboration** → populate `signatories` only, no rating change. Common-name false positives are real (22,901 Nashville signers; "John Smith" matches plenty).
2. **With state/presbytery corroboration** → set `scores.cultural = "red"`, downgrade `overall_rating` to `"yellow"` if it was green, add tags `needs-rating-review` + `cultural-drift-flag`, write a `score_notes.cultural` justification.

Confirmed cases from 2026-04-30 baseline (do not undo):
- `christ-church-santa-fe-pca-nm` (Greg Schneeberger, Warhurst, Rio Grande Pby)
- `trinity-pres-pca-fort-worth-tx` (Brian Davis, Warhurst, North Texas Pby)
- `christ-central-pres-centreville-pca-va` (Owen Lee, Lament 2025, Potomac)
- `redeemer-church-indianapolis` (Charles Anderson, Warhurst, Central Indiana Pby)

## Forbidden actions

- **Don't edit `churches.json` directly from a background agent.** Write a patch.
- **Don't invent new `denomination_family` labels.** Use the dominant label from CLAUDE.md or `Other`.
- **Don't auto-apply red signatures without state corroboration.**
- **Don't skip `node generate-church-pages.js`** after a JSON change.
- **Don't delete records** without a verification trail in the commit message.
- **Don't bump `directory_version`** unless you're closing out a meaningful release (last bump 2026-04-30 V4.9.6 → V4.9.7).
- **Don't hand-edit HTML** in `docs/churches/`. Edit JSON, regen.

## Personal-connection guard

Adam knows several pastors personally. Don't downgrade these without strong cause; flag for his review instead. Current list lives in the `project_church_directory.md` memory file (Connection Buda, Veritas Federal Way, Forest Baptist Louisville, Salt Hartfield, Grace Bible Wappingers, FRDM Stafford, FUMC Millville Jack Fosbenner, etc.).

## Cross-thread coordination

A separate Claude Code thread sometimes runs cross-pollination work between `usmcmin.com/citizen.html` ↔ `usmcmin.org/churches.html`. If `git pull --rebase` shows a conflict on `churches.html` or shared files, **resolve cleanly** — that thread's intent is additive (UI/UX), not data-overwriting. The `regen-and-commit.sh` script handles this automatically.
