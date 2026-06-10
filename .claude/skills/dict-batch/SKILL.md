---
name: dict-batch
description: Author, validate, and ship MOOP Dictionary batches toward 7,777 entries, and audit the corpus. Use whenever the user wants dictionary work — new entries/batches, "continue the dictionary", an integrity/stability check, a voice-lock (doctrinal drift) audit, or fixing dictionary cross-links. Encodes the full proven pipeline, the voice-lock rules, and the NEVER rules for this repo.
---

# MOOP Dictionary — batch authoring & corpus audit

Confessionally Reformed (1689 LBCF), KJV-honoring, complementarian,
anti-postmodern word-study dictionary at `docs/dictionary/` (live at
usmcmin.org/dictionary). Goal: **7,777 entries**. Governing doc:
`DICTIONARY-VOICE-LOCK.md`. Roadmap + progress tracker:
`DICTIONARY-ROADMAP.md`. Repo-state warnings: `WORKING-TREE-STATUS.md`.

## 0. Verify state (always first)

```bash
cd ~/bible-reading-plan-bot && git fetch origin -q
git log --oneline -1 && wc -l data/dictionary-slugs.txt
python3 bin/dict_integrity_audit.py --quiet   # must say PASS before you start
```

## 1. Pick a theme & survey slugs

- **Open veins are PLACES and FIGURES.** Doctrine, divine attributes,
  offerings/feasts, and core Hebrew/Greek word-studies are MATURE.
- **First stop:** `data/dictionary-candidates-from-dangling.txt` — the
  corpus's own demand list (slugs other entries already link to, by
  reference count). Highest counts first.
- Survey every candidate (bare AND suffixed forms — many exist as
  `john-flavel` not `flavel`, `hannah`, `lydia`, `gadara`=gergesa):

```bash
for s in slug1 slug2; do grep -ixq "^${s}$" data/dictionary-slugs.txt \
  && echo "x $s" || echo "OPEN $s"; done
```

## 2. Author the batch JSON

`data/dictionary-batches/batch-NN-topic.json` — a LIST of 10 entries, each:
`slug, word, pronunciation, pos, etymology, biblical_def (~200-250w),
webster_summary, webster_full (5 strings), scriptures (4 [ref, KJV-text]
pairs), corruption_summary, corruption_paragraphs (2), roots_summary,
roots_lines (5 STRINGS — never list-of-lists), usage (3), related (4
[slug, Label] pairs)`.

Voice-lock essentials:
- Reformed/Baptist/KJV/complementarian register; NT/OT typology where real.
- Banned: "tension between" hedges, "many/most scholars believe/argue",
  therapy-speak, progressive vocabulary in OUR voice. Full catalog in
  `bin/dict_drift_audit.py` + `DICTIONARY-VOICE-LOCK.md`.
- An entry that NAMES banned terms **to rebut them** adds top-level
  `"voice_lock_ok": ["progressive"|"histcrit"|"therapy"|...]`.
- Place/figure entries with no real postmodern corruption: 2nd corruption
  paragraph opens `<em>This entry faces no significant postmodern
  redefinition.</em>` then names the principle to recover.
- Entities: only standard named entities + `amacr emacr imacr omacr umacr
  aelig thorn`. No `&apos;` (use `&#39;`).
- Expect ~30% of authored `related` slugs to not exist — substitute existing
  slugs (bulk python `.replace()` on the JSON) until the pre-flight passes.

## 3. Run the pipeline (it enforces everything)

```bash
bin/batch_pipeline.sh data/dictionary-batches/batch-NN-topic.json
```

Stages: **pre-flight** (JSON/schema, slug collisions, entities,
related-resolution) → **drift audit** (aborts on voice-lock hard hits) →
generate → rebuild → regen slugs → manifest → **post-flight corpus
integrity audit** (must end `PASS`).

## 4. Commit + push (explicit files ONLY)

```bash
git add docs/dictionary data/dictionary-batches/batch-NN-topic.json data/dictionary-slugs.txt
git commit -q -m "Dictionary batch NN: <theme>\n\n<entry list + one-line themes>"
git push origin main
```

The fleet auto-commits every few minutes. If a push races, `git log
origin/main --oneline` — your commit usually landed. Don't panic-rebase.

## 5. Maintenance cadence

- Every ~3-5 PLACE/biblical batches: `python3 bin/autolink_chapters.py`,
  commit `docs/chapters` (skip after pure-figure batches — names don't
  appear in chapter text).
- After batches with Strong's refs: `python3 bin/autolink_dict_to_lexicon.py`.
- Update `DICTIONARY-ROADMAP.md` Progress Tracker each session.
- Corpus audits any time:
  - `python3 bin/dict_integrity_audit.py` — structure (links, canonical,
    entities, WOTD, manifest). Hard findings must be fixed.
  - `python3 bin/dict_drift_audit.py docs/dictionary` — corpus voice-lock.
    HTML scans auto-triage rebuttal quotes (headword / chip-label /
    corruption-section / own-corrector-entry / fully-quoted terms become
    soft). **Soft hits are review items — do NOT "fix" rebuttal quotes.**
  - `python3 bin/fix_dangling_chips.py --dry-run` — if related-chips ever
    rot again (curated retargets + removal; review before applying).

## NEVER

- `git add -A` or `git add .` — the working tree carries the fleet's live
  readings/church-directory work and MBT translation state.
- `git reset --hard` / `git checkout -- .` / `git stash` repo-wide.
- Recreate an existing slug (pre-flight now blocks this).
- Edit existing `data/dictionary-batches/*.json` — historical record;
  revisions go in NEW batches.
- `roots_lines` as list-of-lists (silent rendering bug).
- Overwrite fleet-modified files (readings, churches, CLAUDE.md, assets).

## Known era-debt (quantified 2026-06-09; future workstreams)

- ~316 duplicate display titles to review (mostly intentional variants).
- ~180 entries lack a Webster section; ~320 lack Modern Corruption;
  ~640 lack Usage (oldest era). Corruption-section authoring is the
  highest-value backfill (it is the dictionary's distinctive mission).
- ~778 open candidates in `data/dictionary-candidates-from-dangling.txt`.
