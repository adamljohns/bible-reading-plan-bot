---
name: dedup-guard
description: Prevent and catch DUPLICATE church records in the MOOP Church Directory (docs/data/churches.json) — the red/yellow/green "three Bent Trees" problem, where the same physical church gets added two or three times under slightly different ids/names with conflicting ratings. Use this skill BEFORE adding any church (run the pre-insert check so enrichment updates the existing record instead of creating a copy), and AFTER any enrichment/import/add batch and before pushing (run the duplicate audit, then prune what it finds). Triggers whenever a church is about to be added, a scraper/import/network load runs, an agent (e.g. Hermes) hand-adds a church, or the user reports "we have two/three of the same church", "duplicate records", "don't let this happen again". The counterpart to the add (enrich-churches / enrich-church-single / add-network-or-denomination) and remove (prune-churches) skills. Repo: bible-reading-plan-bot.
---

# Dedup Guard (prevent + catch duplicate church records)

A church gets duplicated when an adder — an SBC/9Marks/network bulk import, a manual Hermes
add, an enrichment scraper — inserts a record the directory ALREADY holds under a different
id or a slightly different name (e.g. `bent-tree-bible-carrollton-tx` vs
`bent-tree-bible-fellowship-carrollton` vs `bc-bent-tree-bible-fellowship-carrollton-tx`, all
one church at 4141 International Pkwy). Because each adder re-rates from scratch, the copies
disagree (one green, one yellow, one red) and the worst rating is the one a visitor might miss.
On 2026-06-04 a single pass removed 64 such duplicates.

The fix is two cheap habits: **check before you add**, and **audit before you push.**

## 1. BEFORE adding a church — check it isn't already here

```bash
node scripts/check-duplicate.js --name "<Church Name>" --city "<City>" --state <ST> \
     [--website <https://...>] [--address "<street, city, ST zip>"]
# or:  node scripts/check-duplicate.js --json '{"name":"...","address":"...","website":"..."}'
```

- Exit **1** + a printed list = a likely duplicate exists. **Do NOT add.** Open that record and
  enrich it instead (enrich-church-single). Matching is fuzzy on purpose: it strips church-type
  words and the city out of the name, so "Bent Tree Bible Church" still matches an existing
  "Bent Tree Bible Fellowship Carrollton". It also matches on website-domain + street number.
- Exit **0** = no match; safe to add.

Any code path that adds churches should call this first. `require()` it for programmatic use:
`const { findDuplicates } = require('./scripts/check-duplicate');` returns the matching records.

## 2. AFTER any add/enrichment batch, BEFORE pushing — audit the whole file

```bash
python3 scripts/find_true_duplicates.py     # conservative: same website domain + same street
less tmp/dedup_report.md                     # groups + a "rating conflicts need human attention" section
```

This only flags HIGH-CONFIDENCE duplicates (same domain AND same street fingerprint AND same
normalized name+city), so its output is safe to act on. It picks the richest record as the
keeper. **Re-rate conflicts by the rubric, not by richness:** if a kept record would be green
but a dropped copy was red/black, verify the real church before trusting the keeper (a female
senior pastor / egalitarian eldership is RED on Gender; an affirming/prosperity church is BLACK).

## 3. Remove what the audit finds — via the prune-churches skill

```bash
node -e "const p=require('./tmp/dedup_plan.json');const ids=[];for(const m of p)for(const d of m.duplicates)ids.push(d.id);process.stdout.write(ids.join(' '))" > /tmp/dupe-ids.txt
bash .claude/skills/prune-churches/scripts/prune.sh --dry-run $(cat /tmp/dupe-ids.txt)   # review
bash .claude/skills/prune-churches/scripts/prune.sh $(cat /tmp/dupe-ids.txt)             # apply
node scripts/build-directory-map.js          # if any removed id had a map pin
```

prune.sh keeps the canonical and removes the copies across churches.json + by-state /
by-denomination-family shards + sitemap + per-church HTML, format-preserving and race-safe
(its serializer self-adapts to the file's exact byte layout — ASCII-escaped, no trailing
newline — so a removal never explodes into a 50k-line em-dash diff). Commit with a verification
trail (see the prune-churches skill).

## Keeping it honest going forward

- Whenever a NEW add path is written (a new scraper, a new network importer), wire step 1 into it.
- Worth automating step 2: run `find_true_duplicates.py` as a post-enrichment step or a daily
  cron and alert (notify-adam.sh) if the count is non-zero, so duplicates can't silently pile up
  between manual audits. ~34 enabled crons already follow this alert-on-failure pattern.
- The detector is conservative (domain + street), so a duplicate with NO shared website or a
  city-only address can still slip past it; the name+city pre-insert check in step 1 is the
  catch for those.
