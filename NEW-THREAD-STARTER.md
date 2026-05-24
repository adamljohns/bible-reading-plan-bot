# Handoff prompt — paste into a fresh Claude Code thread if this one gets blocked

Use this if a thread gets safety-filter-blocked (false positive) and you need a clean restart. Paste the block below as your first message in the new thread.

---

```
# Handoff from previous Claude Code thread — MOOP Bible Translation + Watchman's Chronological Plan

**Project:** Adam Johns (MOOP), U.S.M.C. Ministries, Fredericksburg VA. Building a year-long daily Bible reading system on usmcmin.org. Reformed (1689 LBCF). M5 Max Mac, user `moop_bot_pro`.

**Repo:** `/Users/moop_bot_pro/bible-reading-plan-bot` — GitHub Pages deploys from `docs/` to https://usmcmin.org.

## READ THESE FIRST (auto-memory + repo)
1. `MEMORY.md` (auto-loads) — index
2. `project_mbt_translation.md` (full project state + decisions)
3. `feedback_mbt_translation_method.md` (style rules — copyright stance, em-dash rule, interpretation must earn place, double-tap rule)
4. `feedback_prose_style.md` (Adam's voice preferences)
5. Repo root: `MBT-PROPOSAL.md`, `STATE-OF-PROJECTS-2026-05-22.md`

## The big picture

Each day has 5 watches: 0600 Morning Wisdom, 0700 Husband's Post, 1100 Father's Charge, 1500 Citizen's Stand, 2100 Evening Peace. Each watch carries a Scripture passage plus a meditation wrapper (intro, themed reflection on a rotating virtue, application, prayer, "Helm Command"). The Watchman bot DELIVERS pre-authored static content per subscriber; bots do NOT improvise at runtime. Personalization = delivery-time role tagging.

## What's LIVE on usmcmin.org

- **The Watchman's Chronological Plan for the Year of our Lord 2026** at `/chronological.html` — renamed from "Maiden Voyage" on 2026-05-22 (commit 59557dd). Hero icon = calendar shield, Today = compass, Month = calendar.
- **MBT pilot (hidden)** at `/mbt.html` — Psalms 1, 23, 37 only so far (3 of 1,189 chapters). Read + Reading-Plan-Order tabs.
- **Agent fetch URLs**: `/assets/mbt/<bookId>_<chapter>.json`, `/assets/mbt/manifest.json`, `/assets/mbt/mbt-bible.json` (flat).
- **BTE** at `/bible.html` — 12-translation word-study tool. Stays SEPARATE from MBT work; do not touch.

## What exists as files but NOT yet as web pages

- **January 2026 daily readings**: `1) MOOP's daily Bible Readings - January.pages` in `~/Library/Mobile Documents/com~apple~Pages/Documents/`. Also as PDF at `/Users/moop_bot_pro/Documents/BU2TB-Archive/TRANSFER_PACKAGE_FRESH_2026-03-04/workspace-memory/bible_plan_january.pdf` (readable directly). 31 days × 5 watches × full content (Scripture + briefing + themed reflection + application + prayer + helm command). Authored via ChatGPT.
- **February 2026 daily readings**: `2) MOOP's DBR - Feb.pages` in same iCloud Pages dir. 28 days, same format.
- **Master Nav workbook**: `~/Downloads/Bible plan master navigation doc.pages` — defines personalization (subscriber profile, virtue rotations HAPPY/FULFILLED/RESOLUTE, child themes, Five Daily Templates, Commissioning covenant). To extract: `osascript` Pages → export to `/tmp/master-nav-export.pdf` (this worked in the prior session).
- **Master passage spine PDF**: Google Drive file ID `1XdDWJa9yciN_xTfwatFLFr3d4dnwk7Sl` — matches `plan-data.js`.

## Locked rules — don't relitigate

1. MBT sources = public domain only (KJV 1769 + Strong's, WEB). Never feed NKJV/ESV/NASB/NLT/CSB into generation. All in `docs/assets/verse-cache.json` already.
2. Copyright stance = verbatim-only: a verse must not be word-for-word a modern copyrighted version; one different word clears it. Don't dodge phrase overlap. `build-mbt.py` enforces an 85% bigram-overlap gate.
3. MBT verse style = interpretive blend in EVERY verse's `text` field (the Ps 37:4 standard), not bare modernization. The bracketed Amplified-style form lives in the `amp` field. Notes for Strong's anchors.
4. Style: em-dashes used sparingly (overuse = AI tell — commas at least half the time); interpretation must earn its place (no ornament); double-tap only for genuine dual meaning; divine name = LORD (small caps), never "Yahweh"; deity pronouns capitalized.
5. Git: stage specific files (never `git add -A`); commit per batch; co-author line `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`; pushing deploys live.

## Pipeline files

- Authored content: `data/mbt-batches/<book>_<chapter>.json`
- Compiler + validator: `build-mbt.py` (run from repo root)
- Diagnostic probe: `scripts/mbt_originality_probe.py`
- Served output: `docs/assets/mbt/`
- Hidden reader: `docs/mbt.html`
- Plan data: `docs/assets/plan-data.js` (window.PLAN_DATA, 365 days)

## Drive integration note

The Google Drive MCP is scoped to Adam's PERSONAL account (`adam.l.johns@gmail.com`) only. The `usmcministries` account isn't visible. Master Nav PDF and Jan PDF are already accessible.

## Adam's open question (answer this first)

After getting the MBT pilot live and the rename deployed, the prior thread proposed authoring `2026-03-01` as the next prototype daily reading. Adam pushed back:

> "Have we built out days Jan 1 to Feb 28 with our content already though? Seems like that would make sense prior to doing March 1st, doesn't it?"

He's right. Jan and Feb meditation content already exists in his voice — it just isn't on the site yet. Backfilling Jan/Feb first means: data shape gets validated against proven sign-off-locked content, the chronological page lights up fully for the first ~60 days, the MBT grows chapter coverage naturally as Jan/Feb passages are translated, and March 1 starts from "we know exactly what the published format looks like."

## First concrete action

Pilot the Jan/Feb backfill on a SINGLE day:

1. Read the January PDF (path above) — focus on Thursday January 1, 2026 (5 watches: John 1:1-18 / Genesis 1:1-23 / Genesis 1:24-31 / Genesis 2:1-25 / Psalm 1).
2. Parse Day 1 into `data/readings/2026-01-01.json` — structured shape (date, watches{morning_wisdom, first_watch, second_watch, third_watch, evening_peace}, each with passages, scripture_text, intro, context_summary, reflection{theme, body}, application, prayer, helm_command).
3. Translate the day's passages into MBT (Psalm 1 already done; John 1 + Genesis 1-2 need new MBT chapter files in `data/mbt-batches/`).
4. Render as `docs/readings/2026-01-01.html` — hidden, noindex; chronological page links to it.
5. Show Adam, get sign-off on data shape + page format.
6. Then batch Jan 2-31, then Feb 1-28.

Start by confirming with Adam this is the right approach, then check git status and begin the Jan 1 prototype.
```

---

**Last updated:** 2026-05-23 (after the prior thread hit a safety-filter false positive).
