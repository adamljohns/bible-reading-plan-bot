# Watchman Plan → Daily Reading Personalization Spec

*Draft for Adam's review — 2026-05-31. Not published (repo root, not under docs/).*

## 1. The picture

We now have a **complete authored corpus** (365 days × 5 watches) plus a
**day-keyed JSON index**. The corpus is written as **Adam's personal master**
(his wife Maria; his sons Gideon, Boaz; his daughter Shiloh; Fredericksburg /
Virginia / United States). The Watchman form (`docs/watchman.html`) collects a
rich profile per new user. **Personalization = taking Adam's master reading for a
given day and swapping his specifics for the new user's specifics**, at whatever
depth the data and budget justify.

```
corpus (Adam's master, .md)  ──build_reading_index.py──►  per-day JSON
        │                                                  (text + personal_tokens
        │                                                   + passage + trait + audio)
        ▼
  personalization layer  ◄── Watchman form profile (wife name, kids, location, …)
        │
        ▼
  the user's daily reading  ──►  email / Telegram / PDF
```

The index already exposes, per watch, the **`personal_tokens`** that appear in
the text (e.g. `["Maria","Gideon","Boaz","Shiloh"]`) — so the swap layer knows
exactly what to replace. PJ's crons are the **first consumer** of this same
pattern (group crons already generalize Maria→"your wife", kids→"your children").

## 2. Three tiers of personalization (cheapest → deepest)

| Tier | What it does | Mechanism | Cost |
|------|--------------|-----------|------|
| **T1 — Swap** | Replace Adam's proper nouns with the user's | String substitution on corpus text using token maps | ~free, instant, reliable |
| **T2 — Select / reframe** | Skip or reshape watches the user can't use; emphasize their goal/struggle | Conditional assembly + a tailored application bullet | cheap |
| **T3 — Regenerate** | Re-author a watch's *reflection* in the user's archetype/denomination/translation | Local model (qwen3.6) with a personalization prompt seeded by the corpus reflection | minutes/user/day of GPU |

Recommendation: **ship T1 first** (it already feels personal), layer T2, treat
T3 as premium ("Deep Devotional" tier the form already sells).

## 3. Form field → what it personalizes

### Identity & household (T1 swaps — highest impact, lowest cost)
| Form field | Personalizes | How |
|---|---|---|
| `firstName` | Delivery greeting | "Good morning, {firstName}." prepended |
| `maritalStatus` + `wifeName` | **Husband's Post** watch | swap `Maria` → `wifeName`; if single → see §5 |
| `wifeBirthday`, `otherFamily` birthdays | Birthday-blessing inserts | on matching calendar dates, prepend a blessing |
| `hasChildren` + `children[]` (name/gender/age) | **Father's Charge** watch | swap `Gideon/Boaz/Shiloh` → user's children by name+gender; if none → see §5 |
| `location` | **Citizen's Stand** watch | swap `Fredericksburg`→city, `Virginia`→state, `United States`→nation (needs a `location_tokens` add — §4) |
| `lastName` | PDF cover / archive | cosmetic |

### Calibration (T2 select / T3 tone)
| Form field | Personalizes | Tier |
|---|---|---|
| `readingPace` (10-15 … 60+ min) | How many watches delivered / abbreviated vs full | T2 |
| `spiritualGoal`, `struggle` | Which watch is foregrounded + a tailored application bullet | T2 |
| `archetype` (Captain/Maestro/Contractor/CEO/Pastor/Professor) | Metaphor register — the corpus is nautical-military ("Helm Command"); Maestro/Professor want different imagery | T3 |
| `bibleVersion` (NKJV/ESV/…/Blended) | Scripture rendering — re-pull from BTE chapter JSON (12 translations) in their version | T2 (BTE already has all 12) |
| `denomination` / `theologicalLean` | Depth of Reformed distinctives. NOTE: product is **explicitly Reformed/1689/patriarchal** — calibrate emphasis, do **not** dilute the core | T3 (Adam decides scope) |
| `seasonOfLife`, `prayerLife`, `bibleReadingHistory` | Tone/maturity of reflection | T3 |
| `militaryService` + `branch` | Military metaphor density (veteran → keep; civilian → soften) | T3 |
| `occupation`, `hobbies` | Concrete application examples | T3 |
| `lifeVerse`, `topBooksOfBible` | Optional woven references | T3 |
| `avoidTopics` | Tone-down list for sensitive areas | T2/T3 |
| `startDate` | Day 1 mapping (startDate → plan Day 1, or → real calendar date) | T2 |
| `deliveryMethod` + `contact` | Channel (email / Telegram / PDF) | plumbing |

### Already collected, not yet reading-relevant
`age, marriageYears, marriageStrength, childFocusAreas, leadershipRoles,
mentoringOthers, hasMentor, fastingPractice, worshipStyle, biggestFear,
financialStewardship, tithingPractice, screenTime, fiveYearVision,
legacyStatement, greaterPurpose, biggestRegret, menYouAdmire` — these are
gold for T3 "north-star" framing (the form even labels `legacyStatement` "the
north star for your personalized reflections") but require regeneration to use.

## 4. Index enhancements needed to support this

1. **`location_tokens`** per watch — like `personal_tokens`, list where
   `Fredericksburg`/`Virginia`/`United States` appear so the citizen swap is
   surgical. (Small add to `build_reading_index.py`.)
2. **Templated base option** — optionally emit a `text_template` per watch with
   `{{WIFE}}`, `{{CHILD_1}}`, `{{CITY}}`, `{{STATE}}`, `{{NATION}}` placeholders
   (produced by substituting Adam's tokens at build time). Pure templating then
   replaces a fragile find-replace at serve time. **Recommended for production.**
3. **`role_flags`** per watch — mark which watches assume `married` / `has_children`
   so T2 can skip/reframe cleanly.

## 5. Open decisions for Adam

1. **Single men** — the Husband's Post watch assumes a wife. Options: (a) skip it,
   (b) reframe to "the husband you are preparing to be," (c) substitute a
   brotherhood/purity focus. Which?
2. **Childless men** — same question for Father's Charge.
3. **Denomination scope** — how far do we flex for non-Reformed/non-patriarchal
   users? (Recommendation: calibrate warmth/emphasis, never the core conviction —
   that's the product's spine.)
4. **Where personalization runs** — the form already POSTs to a Mac Mini API
   (`192.168.1.166:8080`, `/api/save-email`, `/api/bible-intake`). That box is the
   natural home for the personalization service (it can read the corpus/index and
   the user's saved profile, then render + deliver). Confirm that's the host.
5. **Generic public version** — the SDG-4 group already needs a names-generalized
   build. Worth producing a single canonical **generic** corpus (T1 with role
   words) that doubles as (a) the group feed and (b) the default for users who
   skip the form.

## 6. Suggested build order

1. **T1 swap service** on the Mac Mini API: input = day's per-day JSON + user
   profile; output = personalized text (names + location). Ship to email/Telegram.
2. Add `location_tokens` + `role_flags` to the index builder.
3. **T2**: pace-based assembly, single/childless reframing, goal/struggle bullet,
   bibleVersion re-render via BTE.
4. **T3** (premium): per-profile reflection regeneration with the local model,
   seeded by `legacyStatement` + `archetype` + `struggle`.

The corpus + index are the foundation; everything above is a layer on top of
files that already exist and are already serving PJ.
