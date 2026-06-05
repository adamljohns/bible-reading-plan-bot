# ⚠️ Working-Tree Status & Handoff Note

**Last updated: 2026-06-02 (Claude Opus — dictionary thread)**
**origin/main is at `d9d41281f`; local HEAD == origin (0 ahead / 0 behind).**

---

## ✅ The MOOP Dictionary is fully committed and pushed — nothing is at risk

- **5,389 entries / 5,377 slugs.** Every definition is committed to `origin/main`.
- Batch run **126–141 (+160 entries this round)** is complete and pushed:
  Seven Churches, Paul's voyage, Puritans, OT towns, Continental Reformed,
  Scottish/Covenanter, hymn writers, missionaries, biblical waters, Acts figures,
  19c Reformed, valleys/wilderness, women of the Bible, gospel places, more OT
  places, mountains.
- Cross-ref infrastructure is live: lexicon **Word-of-the-Day links to its entry**,
  the forward dict→lexicon Strong's linker (`bin/autolink_dict_to_lexicon.py`),
  `<link rel="canonical">` on every page (`bin/backfill_canonical.py`), and the
  chapter cross-link sweeps.
- **There are ZERO uncommitted dictionary files.** (`docs/dictionary/`,
  `data/dictionary-batches/`, `data/dictionary-slugs.txt`, `docs/lexicon.html`.)

## 🚧 Why the working tree shows a LOT uncommitted (this is NORMAL — leave it alone)

If `git status` shows hundreds of modified files (e.g. `data/readings/*.md`,
`docs/assets/*`, `docs/churches/*`, `docs/data/*`, `CLAUDE.md`), **that is the
fleet's live autopilot work in progress** — the daily Bible-readings covenant-name
edits and the church-directory enrichment/geocode runs. It is expected. The fleet
commits these on its own cycle.

**DO NOT, under any circumstances:**
- ❌ `git reset --hard` / `git checkout -- .` / `git stash` the working tree — this
  **wipes the fleet's in-progress readings + church-directory work** (and MBT
  translation state). It is unrecoverable.
- ❌ `git add -A` or `git add .` — the tree mixes fleet readings/church work, MBT
  translation, and dictionary work. **Always stage explicit files.**
- ❌ overwrite a fleet-modified file (readings, churches, CLAUDE.md, assets).

## 📅 Next dictionary work: Thursday (next batch = 142)

Continuation lives in **`DICTIONARY-ROADMAP.md`** ("Next up" + Progress Tracker).
Quick start for the next thread:

1. `cd ~/bible-reading-plan-bot && git log --oneline -1` and
   `wc -l data/dictionary-slugs.txt` to verify state.
2. Pick a theme — **the open veins are PLACES and FIGURES**; doctrine, divine
   attributes, offerings/feasts, and core Hebrew/Greek word-studies are MATURE
   (already covered). Good 142+ candidates: more OT towns (Libnah, Debir, Eglon,
   Gath-hepher), modern Reformed teachers, more Puritans (Charnock/Goodwin/Flavel
   detail), church fathers, minor biblical figures.
3. **Always slug-check first** — many concepts exist under full-name/bare slugs
   (flavel=john-flavel, hannah, lydia, sea-of-galilee, gadara=gergesa, endor).
4. Per batch: author `data/dictionary-batches/batch-NN-topic.json` (10 entries,
   full schema, voice-lock per `DICTIONARY-VOICE-LOCK.md`), then
   `bin/batch_pipeline.sh <batch.json>` (drift-audit → generate → rebuild →
   regen-slugs → manifest), then stage **explicit** files
   (`git add docs/dictionary data/dictionary-batches/<batch>.json
   data/dictionary-slugs.txt`) → commit → push.
5. Expect ~30% of authored `related` slugs to need swapping to existing slugs
   (validate + bulk-replace before the pipeline).
6. Every ~3–5 place/biblical batches, run `python3 bin/autolink_chapters.py` and
   commit `docs/chapters/` (skip after pure-figure batches — names don't appear
   in chapter text).

## ℹ️ Unrelated note (not this repo)

The `.com` RESOLUTE Citizen scorecard refinement (`com.moop.scorecard-enhance` /
`scorecard-sweep` launchd jobs, which shell out to `claude -p`) was paused
2026-06-02 to protect Claude usage. Resume with
`~/.openclaw/RESUME-scorecard-refine.sh`. This does **not** affect this repo.
