# Bible Products & Site — State of the Projects

**Date:** 2026-05-22
**Owner:** Adam Johns (USMC Ministries)
**Scope:** Current state of in-flight projects on usmcmin.org and usmcmin.com as of today.
**Predecessor snapshot:** [`STATE-OF-PROJECTS-2026-05-04.md`](STATE-OF-PROJECTS-2026-05-04.md) (18 days prior; kept as a historical record, not revised).

---

## What changed in the last 18 days

The two biggest shifts since the May 4 audit: a new product (MBT) was built from scratch, and the build strategy pivoted from "ship Chronological + write Proverbs" to "produce daily readings day-by-day starting where January and February left off." Specifically:

- "Maiden Voyage" retired in favor of **"The Watchman's Chronological Plan for the Year of our Lord 2026"** — deployed live today (`59557dd`).
- A new product added: **MOOP Bible Translation (MBT)** — copyright-safe original blend, pilot live with Psalms 1, 23, 37 at [usmcmin.org/mbt.html](https://usmcmin.org/mbt.html) (`02112f8`).
- The **Master Navigation workbook** was located (`Bible plan master navigation doc.pages` + `chronological-bible-plan-2026-FINAL.pdf` in personal Drive) and now defines the full personalization model.
- Proverbs Devotional: still stalled at Day 2 — unchanged.
- Church Directory: SBC autopilot continues running; ~26,169 records as of today.

| Product | May 4 | May 22 |
| --- | --- | --- |
| Chronological Plan | ~95% live, "Maiden Voyage" | LIVE under new name; nav model documented |
| Proverbs R.E.A.L. M.A.N. | ~9% (Days 1–2 only) | Unchanged |
| **MOOP Bible Translation (MBT)** | did not exist | Pilot live: Psalms 1, 23, 37 |
| **Daily Reading docs** | off-roadmap | on-roadmap: March/April/May next |
| Church Directory | 4,911 churches | ~26,169 records via SBC autopilot |

---

## Product 1 — The Watchman's Chronological Plan for the Year of our Lord 2026

### Current state

- `docs/chronological.html` — full UI: calendar nav, date picker, month view, 5-watch reading cards, progress bar, mark-complete (localStorage), dark/light toggle. **Today:** hero icon swapped from anchor to calendar; Today button = compass (heading), Month button = calendar (calendar-as-month overview).
- `docs/assets/plan-data.js` — all 365 days populated; final-day note updated to new plan name.
- `docs/manifest-chronological.json` — PWA manifest description updated to new plan name.
- `docs/moop-context.html` — three references updated; "maiden voyage" dropped from active military-vocabulary list.
- Live URLs all returning 200 after deploy.

### Master Navigation Document — found and ingested

`chronological-bible-plan-2026-FINAL.pdf` in personal Drive is the **passage spine** (matches `plan-data.js`). A separate `Bible plan master navigation doc.pages` (now exported to `/tmp/master-nav-export.pdf`, 17 pages) defines the **personalization workbook structure**:

- **Subscriber profile:** Name, Year, City, State, Nation, Wife's Name, Children's Names + character themes, Translation Preferences (Primary / Secondary / Tertiary — blended by the LLM).
- **Virtue Rotation Maps** (one per daily watch, rotating through each acronym):
  - **Husband (HAPPY):** Honest, Abiding, Protecting, Providing, Yielding.
  - **Father (FULFILLED):** Faithful, Understanding, Leading, Forgiving, Instructing, Loving, Listening, Encouraging, Disciplining.
  - **Citizen (RESOLUTE):** Responsible, Engaged, Steadfast, Obedient, Loyal, Upright, Trustworthy, Enduring (three rotated each day: City → State → Nation).
- **Child Reflection Maps** per child (Gideon → purpose/mission/direction; Boaz → humility/restraint/right ambition; Shiloh → peace/presence/emotional regulation; plus user-fillable).
- **Spousal Reflection Map:** Her Strengths, Her Wounds, Her Needs, How Scripture should shape your leadership; cross-reference to "105 Prayers for My Wife."
- **Nautical Commands Library** and **Shipboard Prayer Locations.**
- **The Five Daily Watch Templates** (Morning Wisdom, Husband, Father, Citizen, Evening Peace) — each a structured shape with Intro line, Scripture reference, Passage, Context Summary, themed Reflection, Application (the rotating virtue), Prayer, and Nautical Command.
- **Special-Day Overrides:** Birthdays, Anniversaries, High Holy Days, Equinoxes, Solstices, Full/New Moon, National Days.
- **Commissioning Page:** subscriber signs the covenant *"I will show up daily. I will open the Word. I will lead my home. I will guard my city. I will stand my post."*

### Gaps

1. **No commentary rendered on the page yet.** The chronological page shows passage refs only. Print works mechanically but only prints the refs. "Reading + commentary on a single page" requires the meditation layer to be loadable inline — that becomes feasible day-by-day as March readings come online.
2. The "Today's Watchman Readings" widget on the homepage links to the chronological page but doesn't pull the day's content inline.
3. Husband watch icon (`shield-anchor.png` with `alt="helmet"`) is a placeholder mismatch — should be a husband-appropriate icon (e.g. `shield-cord.png` for cord-of-three, marriage covenant).

### Risk

**Low.** Live static page, no PII handling. The plan-data.js ref-link parser still relies on `&`/`+` splitting and has not misfired in production.

---

## Product 2 — MOOP Bible Translation (MBT)  *[NEW since May 4]*

### Current state

- Pilot live: Psalms 1, 23, 37 at [usmcmin.org/mbt.html](https://usmcmin.org/mbt.html) (hidden reader, noindex). Two views: Read and Reading-Plan-Order.
- Agent fetch URLs: `/assets/mbt/<bookId>_<chapter>.json` (per chapter), `/assets/mbt/mbt-bible.json` (flat), `/assets/mbt/manifest.json`.
- Pipeline: `data/mbt-batches/*.json` → `build-mbt.py` (validates, compiles, runs near-verbatim originality check + divine-name discipline + length parity vs KJV) → served files + `mbt-progress.json` (3 / 1,189 chapters, ~0.25 %).
- Originality gate: **0 verses near-verbatim** vs NKJV/ESV. Standing rule: flag only word-for-word reproductions, not phrase overlap.
- Sources: KJV 1769 + Strong's, World English Bible — both public-domain, already local in `verse-cache.json`.
- Voice locked: rich interpretive blend (the Ps 37:4 standard) in every verse; em-dashes sparing; interpretation must earn its place; double-tap only for genuine dual meaning.

### Architecture

- The MBT is **separate from the BTE** by Adam's directive. The BTE (`docs/bible.html`, 12 translations including NKJV) stays as the word-study tool. The MBT is the agent-fed text for daily-reading delivery.
- Old `docs/assets/moop-translation.json` (NKJV-tainted, 30,943 verses) **should be deleted/superseded** once enough MBT chapters cover its scope.

### Gaps

1. Only 3 of 1,189 chapters translated. Need the rest, sequenced day-by-day per the chronological plan (not Genesis-to-Revelation).
2. The tainted NKJV-based files still sit under `/assets/` and should be deleted when unused.

### Risk

**Low.** Hidden product, agent-only consumers so far. Copyright-safety is the gate; it's enforced in `build-mbt.py`.

---

## Product 3 — Daily Reading Documents (Jan/Feb live; March/April/May in queue)  *[NEW priority]*

### Current state

- **January 2026** authored as `MOOP's 2026 Daily Bible Readings — Document 1 of 12` (Pages, in personal iCloud Pages dir and Drive PDF). 31 days × 5 watches × full content (Scripture text + Briefing + themed Reflection + Personal Application + Prayer + Helm Command).
- **February 2026** same structure, exists as a `.pages` file.
- **March / April / May 2026** do not exist yet — this is the next major build deliverable.
- Authoring voice is set: original-language anchored (e.g. Psalm 1's `hagah` rendered "chews on His instruction"), reverent military-pastoral cadence, themed through the virtue rotation maps from the Master Nav.

### Bot delivery model

The OpenClaw Watchman / PSA bots **deliver** pre-authored static readings, personalized per subscriber by role tags. Bots do not improvise content at runtime; readings are deliberately authored, reviewed, and frozen as the day's content.

### Gaps

1. Ten months of daily content still to author.
2. The data shape the bot consumes needs to be locked (one JSON per day, structured into five watches with role-tagged content blocks).
3. Subscriber-profile storage and personalization logic at the bot layer is not yet built; flag for the personalization wiring sprint.

---

## Product 4 — Proverbs Devotional (R.E.A.L. M.A.N. — 31 Days)

**Unchanged since the 2026-05-04 audit.** Days 1 and 2 live; Days 3–31 still stubs; audio out-of-sync. Status preserved for the record. Recommend leaving on hold until daily-reading authoring cadence is established, then revisit.

---

## Shared infrastructure

- `assets/plan-data.js` — single source of truth for plan order (unchanged shape; only the final-day note updated).
- `bible.html?ref=<reference>` — BTE deep-link contract (unchanged).
- `assets/icons/shield-*.png` — extensive icon library (130+ files). Today: hero anchor → calendar; Today button calendar → compass.
- `verse-cache.json` — contains KJV + WEB (public-domain) for all 66 books; the MBT base lives here.
- Drive integration is scoped to **personal account only** (`adam.l.johns@gmail.com`); the `usmcministries` account is not visible unless added to the same integration.

---

## Open decisions

1. **Start authoring March 2026 daily readings?** Recommend 2026-03-01 as the prototype day, end-to-end — all five watches, both the structured data file and the rendered page.
2. **Personalization layer:** does the bot get a subscriber profile schema now (so content blocks are tagged from day one), or do we author Adam's personal version first and add multi-tenant later?
3. **Old NKJV-tainted `moop-translation.json`:** delete it now (replaced by hidden MBT) or keep as legacy fallback until the MBT covers more chapters?
4. **Husband watch icon** still mis-matches (`shield-anchor.png` + `alt="helmet"`). Recommend `shield-cord.png` (cord-of-three, marriage covenant) — but happy to defer to Adam's pick.
5. **Print "reading + commentary on a single page"** — requires embedding the meditation layer in the chronological page. Will be possible day-by-day as March readings come online. Worth designing the print layout in parallel.

---

## Next 7 days — recommended

```
This week (2026-05-22 → 2026-05-29):
  Day 1 (today)  : Rename complete. Hero icon → calendar. Today → compass.
                   STATE-OF-PROJECTS refreshed (this file).
  Day 2-3        : Author 2026-03-01 as the prototype daily reading,
                   end-to-end. Lock the data shape + meditation voice.
  Day 4-5        : Author 2026-03-02 through 2026-03-05 (Week 1 of March).
                   MBT translates each day's passages as the watches need them.
  Day 6-7        : Publish March Week 1 as hidden /readings/<date>.html pages,
                   wire the chronological page to link to them.

End-of-week deliverable:
  - 5 complete days of March readings live.
  - Subscriber-facing daily layout proven end-to-end.
  - Style sign-off locked for the rest of March.
```

---

## What I'm NOT recommending

- **Don't translate the whole Psalter as a standalone unit.** The day-by-day chronological strategy pulls Psalms into Evening Peace as the year proceeds.
- **Don't replace the BTE.** It and the MBT serve different audiences (word-study vs. daily-reading delivery).
- **Don't backfill January and February into the MBT pipeline.** They already exist as authored readings; pick up at March 1.
- **Don't tackle Proverbs Days 3–31 right now.** Daily-reading authoring takes 100 % of the editorial attention; Proverbs would compete for the same writing muscle.

---

*Updated by Claude Code (Opus 4.7, 1M context), 2026-05-22. The previous snapshot ([STATE-OF-PROJECTS-2026-05-04.md](STATE-OF-PROJECTS-2026-05-04.md)) is preserved as a historical record.*
