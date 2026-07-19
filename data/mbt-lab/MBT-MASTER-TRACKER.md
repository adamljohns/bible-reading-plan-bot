# MOOP Bible Translation (MBT) — Master Tracker

**Version:** 0.1 · **Opened:** 2026-07-19  
**Account:** usmcministries2022@gmail.com (ministry)

**This GDoc:** https://docs.google.com/document/d/1icShMefpzJyVNL7ckQ7bNhPt0PnlQvO-SOwm_Raq2Is/edit
**Genesis 1 board:** https://docs.google.com/document/d/1KMdJRH7wmF5dN7x5rOhmihB-2H_mxtQgut4k5rwjasM/edit
**Site hub:** https://usmcmin.org/mbt-lab.html  
**Three-way sync (same pattern as MOOP Context v5.2):**
1. **Google Doc** (this doc) — human edit surface
2. **Website** — https://usmcmin.org/mbt-lab.html + BTE https://usmcmin.org/bible.html
3. **Repo** — `bible-reading-plan-bot/data/mbt-lab/` + `docs/assets/mbt/`

**Live BTE:** https://usmcmin.org/bible.html  
**Clean MBT pilot coverage today:** Psalms (partial), Proverbs, Ruth, Philemon (~1,090 verses). Genesis still on legacy blend.

---

## Purpose

Rebuild a copyright-safe, interlinear-aware English Bible that carries the **depth of Hebrew and Greek** into modern vernacular — occasionally using **one or two extra words** (restrained Amplified method), not AMP-everywhere. North star: January 2026 readings voice + clean Psalm MBT pilot.

---

## Style lock (working decisions)

| Decision | Default |
|----------|---------|
| Amplification | **Anchored Blend (B)** — light multi-word only where English drops meaning |
| Budget | Soft cap ~1.3–1.6× length; usually +1 word or short phrase |
| Divine name | `LORD` = YHWH; `God` = Elohim; `Lord` = Adonai; **no Yahweh** |
| Pronouns | Modern you/your; capitalize deity He/Him/His |
| Sources for generation | WEB + KJV+Strong’s + ASV/YLT + lexicon/dict — **never** NIV/ESV/NASB/NLT/MSG/AMP as inputs |
| Copyrighted translations | **Negative check only** (flag too-similar verses and rewrite) |
| Storage | Per-chapter JSON under `docs/assets/mbt/` + flat `mbt-bible.json` for BTE |

### Output fields per verse
- `text` — running English (default BTE display)
- `amp` — optional slightly fuller study form
- `notes` — H/G lemma audit trail (not shown as Scripture)

---

## Chapter queue

| Priority | Book/Chapter | Status | GDoc chapter sheet | BTE live? |
|----------|--------------|--------|--------------------|-----------|
| 1 | Genesis 1 | **In progress** | [Genesis 1 board](https://docs.google.com/document/d/1KMdJRH7wmF5dN7x5rOhmihB-2H_mxtQgut4k5rwjasM/edit) | Pending ship |
| 2 | Genesis 2 | Queued | — | — |
| 3 | Genesis 3 | Queued | — | — |
| 4 | John 1:1–18 | Optional parallel to Jan reading | — | — |
| 5 | Revelation 1 | Pilot B after Gen style lock | — | — |

---

## Workflow (per chapter)

1. Pull Strong’s/KJV chapter + WEB baseline + current legacy moop line  
2. Draft Anchored Blend verse-by-verse with notes  
3. Adam red-pen in this GDoc (or chapter GDoc)  
4. Promote signed-off `text` into `docs/assets/mbt/{book}_{ch}.json` + rebuild `mbt-bible.json`  
5. BTE auto-prefers clean MBT when key present  
6. Mint command-notebook inbox line with evidence  

---

## Specimen density (signed style target)

**Legacy Gen 1:1:** In the beginning, God created the heavens and the earth.

**Anchored Blend Gen 1:1:** In the beginning — at the head of all things — God created the heavens and the earth.

**Psalm 1:2 (clean MBT already live):** …he broods, chewing it and murmuring it low to himself, day and night.

---

## Open questions for Adam

1. Density: Gen 1:1 pilot above — denser, leaner, or just right?  
2. Default surface: put depth in `text`, or keep `text` lean and depth only in `amp`?  
3. Ship Gen 1 alone first, or Gen 1–3 as a unit?

---

## Changelog

| Date | Note |
|------|------|
| 2026-07-19 | Tracker opened; Genesis 1 draft board created; three-way sync doctrine established |
