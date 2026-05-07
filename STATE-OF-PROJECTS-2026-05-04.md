# Bible Products — State of the Projects

**Date:** 2026-05-04
**Owner:** Adam Johns (USMC Ministries)
**Scope:** Audit of two in-flight products on `usmcmin.org` and recommended path to ship.

---

## Executive Summary

The two products you flagged as "in work" are at radically different completion levels:

| Product | Completion | Effort to MVP |
| --- | --- | --- |
| **Chronological Plan** | ~95% | 1–2 sessions of polish |
| **Proverbs Devotional (R.E.A.L. M.A.N.)** | ~9% | 29 days × original devotional writing + audio |

This invalidates the framing of "ship them in parallel." The chronological plan is effectively ready to ship — the work it needs is *publishing* and *announcing*, not building. The Proverbs devotional needs **substantive content writing**, which is the slowest, most personal kind of work. You should ship one and *finish the other on cadence*, not split focus.

**Recommended sequence:** Polish + announce Chronological now → Use that as a content cadence to write Proverbs Days 3–7 (Week 1 MVP) → Public-launch Proverbs at Day 7 with the rest as a weekly drip.

---

## Product 1 — MOOP's Chronological Bible (Maiden Voyage 2026)

### Current state

- `docs/chronological.html` — full UI: calendar nav, date picker, month view, 5-watch reading cards, progress bar, mark-complete (localStorage), dark/light theme toggle, sticky nav, print stylesheet, responsive layout.
- `docs/assets/plan-data.js` — **all 365 days populated** with all 5 watches (`wisdom`, `first`, `second`, `third`, `peace`). 82 of 365 days have `notes` annotations. Zero placeholders, zero TBDs.
- `docs/manifest-chronological.json` — present (PWA manifest).
- `docs/assets/og/og-chronological.png` — present (social share).
- Architecture: data file is the single source of truth, consumed by **both** `chronological.html` and `bible.html` (V5.5 BTE) via `window.PLAN_DATA`. Each ref renders as a deep link into the BTE (`bible.html?ref=...`).

### Gaps (none are blocking ship)

1. No "intro" / "what is this plan" landing copy. New visitors see the calendar and a first day's readings but no rationale for the 5-watch structure.
2. No streak / completion summary view. You log days to `localStorage` but never surface aggregate progress.
3. No social-share for "today's readings."
4. No audio component (and no plan to add one — verify if intentional).
5. Notes only on 82 of 365 days. The rest are silent. Worth a polish pass for milestone days (book completions, holidays, anchor passages).

### Risk tier

**Low.** This is a public-facing JS-only static page with no auth, no payments, no user data egress beyond optional `localStorage`. Brittleness comes from one place: the ref-link parser in `chronological.html` (line 428–437) splits on `&` and `+` — if a future ref string contains an unusual separator, links could mis-render. Worth a sanity test before announcing.

### MVP-ship scope

1. Add an intro/explainer section above the calendar — describes the 5-watch frame (Wisdom / Husband / Father / Citizen / Peace), why 2026 is the "Maiden Voyage," and how to use the page.
2. Add a "Today" snapshot block to the homepage (`docs/index.html`) linking to `chronological.html`.
3. Run a verification pass: load every day in a headless browser, confirm no broken refs.
4. Announce.

That's a 1–2 session of work, not weeks.

---

## Product 2 — Proverbs Devotional (R.E.A.L. M.A.N. — 31 Days)

### Current state

- `docs/proverbs.html` — landing page, themed, 31-chapter grid linking to `proverbs/1.html` … `proverbs/31.html`. Includes a banner promoting the R.E.A.L. M.A.N. devotional.
- `docs/proverbs/`:
  - `index.html` — alternate landing (269 lines).
  - `intro.html` — **full content** (360 lines): explains the framework, all 7 letters, "How to Use This Devotional."
  - `1.html` — **full devotional**: Day 1, Proverbs 1, "R — Reject Passivity." All sections present (Focus / Read / Key Verse / Observation / Application / Prayer / Audio).
  - `2.html` — **full devotional**: Day 2, Proverbs 2, "E — Engage Consistently." Same structure.
  - `3.html` through `31.html` — **stubs.** All 29 files are byte-identical 93-line redirects that auto-bounce to the BTE. **No devotional content for Days 3–31.**
- Audio: `proverbs-intro.mp3`, `proverbs-day01.mp3`, `proverbs-day03.mp3`.
  - **Mismatch:** Day 3 audio exists but Day 3 has no devotional content. Either an orphan recording or you stopped mid-stream.

### Gaps

1. **29 days of original devotional writing missing.** Each existing day is ~400-600 words across 6 sections. Estimated: ~11,600–17,400 words of original content for full v1.
2. R.E.A.L. M.A.N. → chapter mapping not yet documented. Day 1 = R. Day 2 = E. The intro implies a deliberate alignment of the 7 qualities to specific chapters across 31 days. **Decision required: which letter maps to which chapter?** Until that's locked, you can't write Days 3–31 consistently.
3. Audio: 1 of 31 day-recordings exists (proverbs-day01). Day 3 audio is orphaned. Audio is a substantial production cost — recording, levels, hosting.
4. The R.E.A.L. M.A.N. assessment page (`docs/real-man-assessment.html`) exists but isn't audited here; verify it's wired to the devotional landing.
5. SEO/social-share: Day 1 has og tags. Day 2 should be checked for parity. Stub days have no og data.

### Risk tier

**Medium.** This is a content-quality risk, not a technical one. The two real days (1 and 2) are well-written, theologically careful, and consistent with your "respect biblical authority, intellectual seriousness, no trend-driven cultural framing" guideline. **The risk is that days 3–31 either don't get written, or get written quickly and lose that quality bar.** That would devalue the brand of the whole piece.

### MVP-ship scope (recommended)

Per your earlier choice ("Ship MVP + roadmap for the rest"):

**Phase 1 (Week 1 MVP):**

1. Lock the R.E.A.L. M.A.N. → chapter mapping for all 31 chapters. Document it in a single file (`docs/proverbs/REAL-MAN-MAP.md` or in `intro.html`).
2. Write Days 3–7 to complete Week 1. Same 6-section structure as Day 1.
3. Record audio for Days 2–7 (or punt audio to v1.1 — see open questions).
4. Update each stub (`3.html`–`7.html`) into a real devotional page.
5. Update `proverbs.html` and `proverbs/index.html` to clearly mark Week 1 as live and Weeks 2–4 as "coming weekly."

**Phase 2–4 (Weeks 2–4):**

6. Ship 7 days/week on a fixed cadence (e.g., post by Sunday for the upcoming week).
7. Same author voice, same structure.

**Phase 5 (close-out):**

8. Day 31 ships → directory marked "Complete" → public re-announce as the finished devotional.
9. Optional: compile the full 31 days + intro into a downloadable PDF / printable booklet. (`pdf` skill is available.)

### What I'd push back on

You said "both in parallel." After this audit, parallel doesn't actually mean what it sounded like. The chronological plan needs ~2 sessions; the devotional needs ~30 days of disciplined writing cadence. Parallelizing those isn't a 50/50 split of attention — it's a 5/95 split, and you'd just be checking the chronological box once. Better to **declare chronological shipped this week** and put 100% of the remaining attention on Proverbs cadence.

---

## Shared Infrastructure

The two products and the V5.5 Bible Translation Engine (`bible.html`) share more than expected, which is good news for maintenance:

- `assets/plan-data.js` — single source of truth for the chronological plan, consumed by both `chronological.html` and `bible.html`. Don't fork it.
- `bible.html?ref=<reference>` — the deep-link contract. Both Proverbs days and chronological watches use it to drop the user into the BTE on the right verse.
- Style tokens: `--gold`, `--bg-dark`, `--bg-card`, `--border`, `Playfair Display + Inter`. Consistent across products.
- Icon set: `assets/icons/shield-*.png`. Shared.
- Footer / dark-light toggle: same pattern, copy-pasted into multiple pages. **Brittle — a future redesign would touch many files.** Long-term: extract to a shared `_footer.html` partial via a small build step. Not urgent.

---

## Open Questions for You

Before any execution, three decisions:

1. **R.E.A.L. M.A.N. → Proverbs chapter mapping.** What's the canonical mapping you've already designed (or do you want me to propose one based on chapter content)? This blocks Phase 1.
2. **Audio for Days 2–7 in MVP, or punt to v1.1?** Audio is a 5-10× content effort multiplier (you have to record, edit, host). I'd punt it.
3. **Hard publish target?** I recommend Sunday 2026-05-10 for the chronological announce + Proverbs Week 1 launch. Gives you 6 days. Want a different date?

---

## Recommended Sequence (decision framework)

```
This week (2026-05-04 → 2026-05-10):
  D1-D2  : Chronological polish — intro section, today snapshot,
           link verification, og image check.
  D2     : Lock R.E.A.L. M.A.N. → chapter mapping (you decide; I propose a draft).
  D3-D6  : Write Proverbs Days 3-7 (text only). One day per session.
  D7     : Ship Chronological MVP + Proverbs Week 1 MVP.
           Public announcement.

Week 2 (2026-05-11 → 2026-05-17):
  Write & ship Proverbs Days 8-14 (Week 2).

Week 3:
  Days 15-21 (Week 3).

Week 4:
  Days 22-28 (Week 4).

Week 5 (close):
  Days 29-31. Mark devotional COMPLETE. Optional PDF package.
```

If you'd rather front-load all writing into one big push, that's also fine — but historically that's where you've gotten distracted. A weekly cadence is durable; binge-writing is brittle.

---

## What I'm NOT recommending

- **Don't build new tooling first.** No new dashboards, no new build pipelines, no schema migrations. The infra is fine. Ship the content.
- **Don't redesign the layout.** Day 1 and Day 2 look good. Match that template across Days 3–31. Consistency > novelty.
- **Don't add audio for all 31 days as part of v1.** Audio belongs in v1.1 once the text is locked, especially given the orphan day-03 audio file shows the cost of recording out-of-sync with content.
- **Don't extend to other Bible books yet.** Proverbs first. Then evaluate.

---

## Next action

Tell me how you want to handle the three open questions, then I'll start on Phase 1.

— Audit by Cowork, 2026-05-04.
