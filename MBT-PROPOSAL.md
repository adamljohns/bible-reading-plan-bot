# MOOP Bible Translation (MBT) — Phase 0 Proposal

**Status:** Draft for Adam's review (2026-05-22). Nothing generated at scale yet. No files changed in `docs/`. No git push.
**Goal:** One original, copyright-SAFE blended English Bible (all 66 books / 1,189 chapters) the OpenClaw fleet can quote freely and completely, delivered as a hidden, fetchable index on usmcmin.org.

---

## 1. What I found (the lay of the land)

**The current MBT is copyright-tainted and must be rebuilt.**
- `docs/assets/moop-translation.json` (30,943 verses, all 66 books) plus `mbt-john.json`, `mbt-1-3-john.json`, `mbt-nt-extra.json` are LLM paraphrases generated with **NKJV as the base (~33–70% weight)** plus ESV / NASB / NLT / CSB — all copyrighted. Several generators fall back to emitting **raw NKJV verbatim**. Genesis 1:1 and Psalm 23:1 come out byte-identical to NKJV. This is a derivative of copyrighted text and is unsafe for the agents to quote.
- The BTE (`docs/bible.html` v6.3) does **not** blend live — it just looks up `moop-translation.json` by `book_ch_verse` and displays it. `detectMoopSources()` only reverse-engineers a "blended from…" label after the fact. So swapping in a clean MBT = regenerate the lookup file; the display layer barely changes.

**We already own a clean public-domain base — locally.**
- `docs/assets/verse-cache.json` holds 11 translations keyed `B_C_V → {TRANS: text}`. Two of them are public domain and cover **all 66 books**: **WEB** (World English Bible, 30,700 verses — modern, formal-equivalence, derived from ASV 1901) and **KJV 1769** (30,706 verses — traditional cadence). We extract only these (plus ASV/YLT, fetched) into a clean source store and **never let the copyrighted columns touch generation**. (Bonus: the copyrighted columns become a *negative* check — see §5.)
- Strong's-tagged KJV (`shepherd<S>7462</S>`) already exists for the 441 existing chapters (`docs/assets/chapters/*.json`); we fetch the tagged KJV for the remaining ~748 chapters from `bolls.life` (the same API `gen_blended_parallels.py` already uses).

**The reading order is solved.**
- `docs/assets/plan-data.js` (`window.PLAN_DATA`) is the single source of truth: 365 date-keyed days (2026-01-01 → 12-31), each with 5 ordered watches `{wisdom, first, second, third, peace}` + notes. Genuinely thematic/chronological ("The Maiden Voyage"), whole-Bible across the year. This is what we sequence the MBT against.

**The house style already exists in your own work.**
- Your January daily readings (e.g. Psalm 1: *"he chews on His instruction day and night"* for `hagah`; John 1:1: *"the Word already was"* for the durative imperfect ἦν) are the style north star: poetic sense-lines, modern reverent English, divine name **LORD**, modern pronouns, light **inline** amplification surfacing the precise Hebrew/Greek sense. The MBT text should read like January — but be provably rebuilt from public-domain sources.

---

## 2. (a) Source recipe — how to get NKJV-like readability, legally

| Role | Source | License | Status |
|---|---|---|---|
| Modern readable base | **WEB** (World English Bible) | Public domain | Local (all 66 books) |
| Traditional cadence + word anchor | **KJV 1769 + Strong's** | Public domain | Local (441 ch) + fetch rest |
| Literal tie-breaker | **ASV 1901**, **YLT** | Public domain | Fetch |
| Optional dignity check | **Darby**, **Webster 1833** | Public domain | Fetch if needed |
| Meaning / amplification anchor | **Strong's**, **Thayer's** (Gk), **BDB / Gesenius** (Heb) | Public domain | Fetch lexica |

**Why this works legally and stylistically:** WEB already sits in the modern register Adam likes (it's a public-domain modernization of the ASV, reading close to NKJV/ESV in feel) and KJV supplies the traditional dignity. Blending WEB's cadence + KJV's gravity + word choices **anchored to Strong's/lexica** lands the text in the "NKJV neighborhood" without ever touching NKJV. The amplifications come from public-domain *lexical data*, not from the Amplified Bible's copyrighted brackets — so the Amplified-style *method* is reproduced while the *expression* stays original and ours.

**Hard rule:** NKJV / ESV / NASB / NLT / CSB / AMP / MSG / NIV / NRSVCE are **never** inputs to generation. Their only role is the post-hoc originality check in §5.

**Textual basis decision:** KJV (TR) + WEB (Majority Text) lean Byzantine/Majority — which sits comfortably with a confessional Reformed posture. Recommend we keep that lean rather than chasing the critical text. *(Your call.)*

---

## 3. (b) House style guide — decisions to lock

Each item below is a decision. My recommendation is bolded; alternatives noted.

1. **Divine names — recommend `LORD` (small caps) = YHWH; `God` = Elohim; `Lord` = Adonai; `LORD God` = YHWH Elohim.** Matches your January readings. We explicitly **reject WEB's "Yahweh"** (the March readings drifted into it — that's the inconsistency we're fixing).
2. **Pronouns — recommend modern (`you/your`), with deity pronouns capitalized (`He/Him/His`).** Matches January. (Reformed practice varies on capitalizing deity pronouns; you've been doing it, so we keep it.)
3. **Formal vs. readable — recommend "as literal as possible, as free as necessary."** Formal-equivalence skeleton (LSB/NASB fidelity), readable cadence (NLT-level flow), reverent register (never The Message / Passion looseness).
4. **Amplification method — THE key decision.** Three settings, shown on Psalm 37:4 in §6:
   - **A — Clean Blend:** spare formal-equivalence, no expansion.
   - **B — Anchored Blend (recommended default):** light *inline* amplification, em-dash continuations in your prose voice, surfacing the one precise meaning.
   - **C — Study/Amplified:** *bracketed* expansions `[ ]` carrying the fuller sense and multiple applications.
   I recommend **B as the default**, with the data also carrying an optional **C-style `amp` field** so agents quote the clean verse as "Scripture" but can pull the amplified form when teaching. This is how we honor both "agents quote Scripture cleanly" and your "I'm fine with every verse twice as long."
5. **Expansion budget — recommend: amplify only where English drops meaning the Hebrew/Greek carries; default soft cap ~1.5–2× length; per-verse discretion allowed.** No padding for its own sake.
6. **Layout — recommend poetic sense-lines for poetry/prophecy, prose paragraphs for narrative.** (Matches January.)
7. **Verse numbers — recommend numbers live as JSON keys; agent-facing text is clean (no inline numbers).** Optional `[n]` markers if you want them visible.
8. **Psalm superscriptions — recommend include** (they are part of the Hebrew text). **Editorial section headings — recommend exclude from MBT text** (not Scripture; they belong in the readings layer).
9. **Red-letter — recommend none in the data** (agents quote plain text); the BTE could optionally render red-letter at display time.
10. **Alternate renderings / "multiple applications" — recommend an optional per-verse `notes` field** to hold the open-handed applications you want to preserve without bloating the verse.

---

## 4. (c) Storage & delivery format

**Per-chapter files (agent-fetchable), mirroring the existing chapter pattern:**
```
docs/assets/mbt/<bookId>_<chapter>.json     e.g. docs/assets/mbt/19_37.json  (Psalm 37)
```
```json
{
  "book": 19, "chapter": 37, "version": "MBT v0.1",
  "verses": {
    "4": {
      "text": "Take exquisite delight in the LORD, and He will give you the desires of your heart.",
      "amp": "Take exquisite delight in the LORD [luxuriate in Him; make Him your supreme gladness], and He will give you the desires of your heart [both the longings He plants when He is your treasure, and their fulfillment].",
      "notes": "Heb. hit'annag (H6026) = take exquisite/soft delight; mish'alot (H4862) = the heart's petitions."
    }
  }
}
```
- `text` = clean, copyright-safe, no HTML, no Strong's cruft — the default agent quote. `amp` and `notes` optional.

**Plus two convenience artifacts:**
- `docs/assets/mbt/mbt-bible.json` — flat `B_C_V → text`, a drop-in replacement for the tainted `moop-translation.json` so the BTE can display the clean MBT.
- `docs/assets/mbt/plan-index.json` — derived from `plan-data.js`: each of 365 days → ordered passages → resolved verse keys, so agents/readers traverse in Maiden-Voyage order.
- `docs/assets/mbt/manifest.json` — books/chapters present, version, and the license line: *"MOOP Bible Translation © U.S.M.C. Ministries — derived from public-domain sources; free to quote in full."*

**Hidden, not featured:** lives under `assets/`, excluded from nav and sitemaps. Agent fetch URL pattern (documented for the fleet): `https://usmcmin.org/assets/mbt/<bookId>_<chapter>.json`.

**Cleanup:** delete the tainted `moop-translation.json`, `mbt-john.json`, `mbt-1-3-john.json`, `mbt-nt-extra.json` once the clean build covers their books.

---

## 5. (d) Fidelity & verification + batch workflow

**Workflow (modeled on the proven dictionary pipeline):**
1. Build a clean per-verse PD source table: `{KJV+Strong's, WEB, ASV, YLT}` + lexicon glosses. (One-time gather; WEB+KJV already local.)
2. Author in **batches** (per book, or per chapter for big books). A generator drafts each verse from the PD sources + Strong's/lexicon + the house-style guide + few-shot examples from the signed-off pilot — using the Claude API you already shell out to, fed **only** PD inputs.
3. Editorial pass to house style (the `text`/`amp`/`notes` shape).
4. Rebuild script writes chapter JSON + updates manifests + the flat file.
5. Commit per batch (specific files only); push deploys live — **confirm with you before the first push.**
6. Track a running count toward 1,189 chapters.

**Fidelity guardrails:**
- **Defensibility:** every rendering must be justifiable from the PD base + Strong's. No free invention.
- **Originality check (turns the copyrighted cache into a safety net):** diff each MBT verse against the NKJV/ESV/etc. columns; flag any verse too similar to a copyrighted translation and rewrite it. This *proves* the MBT is not reproducing copyrighted text.
- **Structural checks:** verse-count parity vs. KJV/WEB (no dropped/added verses), divine-name consistency, length-ratio sanity.
- **Human + doctrinal review:** spot-review per book; Reformed reading verified on key texts; you sign off.

---

## 6. Specimen — Psalm 37:4 (your example), three settings

> Your reading: *"when we delight in God, He gives us the desires our heart is supposed to have."* All three are built only from KJV/WEB + Strong's (`hit'annag` H6026 = take exquisite/soft delight; `mish'alot` H4862 = the heart's petitions; `natan` H5414 = give/grant).

**A — Clean Blend**
> Delight yourself in the LORD, and He will give you the desires of your heart.

**B — Anchored Blend (recommended default)**
> Take exquisite delight in the LORD, and He will give you the desires of your heart — for when He Himself becomes your joy, He both shapes and satisfies what your heart most wants.

**C — Study / Amplified**
> Delight yourself in the LORD [luxuriate in Him; make the LORD your supreme gladness], and He will give you the desires of your heart [both the longings He plants there when He is your treasure, and their fulfillment].

**And a fuller passage in the recommended setting — Psalm 1:1–3** (note `hagah` H1897 surfaced as "chews over / murmurs," echoing your January rendering):
> How blessed is the man
> who does not walk in step with the counsel of the wicked,
> nor stand in the path that sinners take,
> nor sit down in the seat of mockers.
> But his delight is in the law of the LORD,
> and on that law he meditates — chewing it over, murmuring it — day and night.
> He is like a tree transplanted beside channels of water,
> yielding its fruit in its season,
> its leaf never withering;
> and in all that he does, he thrives.

---

## 7. Recommended Phase 1 pilot

Pilot **Psalm 37** (your own example verse, self-contained, poetic, 40 verses) to lock the poetry style; optionally add a short **narrative** book — **Ruth** (4 ch) or **Jonah** (4 ch) — to validate prose before scaling. You review and sign off on style, then Phase 2 scales book-by-book in the Maiden-Voyage order.

---

## 8. Decisions I need from you

1. Amplification default — **A, B, or C** (I recommend **B**, with a `C`-style `amp` field carried alongside)?
2. Keep deity-pronoun capitalization and `LORD` (no "Yahweh")? *(I recommend yes.)*
3. Storage shape — per-chapter files + flat file + plan-index, as in §4? Any change to the hidden URL pattern?
4. Pilot — Psalm 37 alone, or Psalm 37 + Ruth/Jonah?
5. Should the public BTE eventually switch its on-screen text to the clean MBT, or stay NKJV-based for the word-study tool while only the agents use the MBT index?
