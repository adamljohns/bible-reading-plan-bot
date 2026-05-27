# MOOP Dictionary Roadmap — to 7,777 (Word-Study Completeness)

> **Mission:** grow the MOOP Dictionary from its current state to **7,777 entries**, pivoting
> toward *the actual vocabulary of the biblical text* so that **every meaningful word in the
> Bible** is covered for word study. At 7,777 the dictionary reaches the territory of a complete
> expository word-study Bible dictionary (think *Vine's*, ~6,000 entries — but larger and in the
> MOOP voice).
>
> **This is a living document.** Update the Progress Tracker at the bottom after every session.
> *(Standing preference: any multi-week plan like this gets saved as a tracked `.md`.)*

---

## 1. Where we stand (deep-search inventory, 2026-05-22)

| Metric | Value |
|---|---|
| Tracked headline count (rebuild "Total entries") | **4,777** |
| Unique word-entry slugs (`data/dictionary-slugs.txt`) | **4,768** |
| — single-word slugs | 2,176 |
| — multi-word (hyphenated) slugs | 2,592 |
| Biblical names (names index) | ~726 |
| Featured section pages | 8 (doctrinal-anchors, biblical-order, expressly-prohibited, most-corrupted, gen-z/millennial/gen-x/boomer-decoded) |
| **Target** | **7,777** |
| **Gap remaining** | **~3,000 = 150 batches of 20 ≈ 14–15 focused sessions** |

> The 9-entry gap between 4,777 and 4,768 = the 8 section pages + names index page (they aggregate
> existing entries; they are *not* new words). `index.html` is the 10th non-entry page.

### Authoritative "don't recreate" check
**`data/dictionary-slugs.txt`** holds every existing word slug, sorted. **Before authoring any
batch, grep it** (or the live `docs/dictionary/*.html`) so we never recreate an entry:
```
grep -ix 'proposed-slug' data/dictionary-slugs.txt   # exact match = already exists
```
Regenerate the list any time after a batch:
```
ls docs/dictionary/*.html | xargs -n1 basename | sed 's/.html$//' \
  | grep -vxE 'index|names|doctrinal-anchors|biblical-order|expressly-prohibited|most-corrupted|gen-z-decoded|millennial-decoded|gen-x-decoded|boomer-decoded' \
  | sort > data/dictionary-slugs.txt
```

### Alphabetical distribution (first letter of slug)
Baseline coverage by letter — useful for spotting thin zones to compare against a full biblical
wordlist later:
```
A 320  B 255  C 356  D 222  E 280  F 224  G 200  H 249  I 153  J 143  K  63
L 178  M 279  N 102  O  89  P 334  Q  20  R 194  S 482  T 273  U  45  V  75
W 147  Y  37  Z  29   (plus ~19 numeric, e.g. book chapters / 144000)
```
Thin letters (Q, K, U, V, Y, Z, N, O) are expected for English, but flag candidates for the audit.

### Domains already well-covered (do NOT re-plough; grep first)
- **Systematic theology** — heavy: 127 `-doctrine` slugs, **249 `-ism`** slugs; dense clusters on
  christ (64), spirit (60), god (73), sin (62), covenant (52), scripture (10), worship (19).
  The 2026-05 sweep (batches 73–83) finished soteriology, ecclesiology, eschatology, bibliology,
  hamartiology, pneumatology, theology-proper/decrees-providence, Christology, anthropology,
  sanctification, and worship.
- **Biblical names** — ~726 in the names index (aaron, abel, abigail, abner, absalom…).
- **Book names** — book/chapter slugs already present (1corinthians, 1john, …).
- **A real head start on biblical word-study vocabulary** — 2,176 single-word slugs already include
  abide, abiding, abhor, abomination, abound, abundance, abstain, abstinence, abyss, etc.
- **Featured sections** — doctrinal anchors, biblical order, expressly-prohibited, most-corrupted,
  and the four generational "decoded" glossaries (gen-z / millennial / gen-x / boomer).

**Implication:** because so much vocabulary already exists, the next 3,000 are driven by a
**coverage audit** (find what's *missing*) more than by free authoring. See §5.

---

## 2. Strategic pivot

The recent sweep covered *systematic-theology* vocabulary (doctrines, -isms, errors). The next
3,000 pivot to **the vocabulary of the biblical text itself** — the significant words a reader meets
in Scripture and would want to study, each anchored to its Hebrew/Greek roots — until *every
meaningful word in the Bible* is covered.

---

## 3. Coverage map (the ~3,000)

| Phase | Domain | ~Entries |
|---|---|---|
| **A** | **Biblical text vocabulary** — action verbs (abide, beseech, chasten, cleave, forsake, hallow, hearken, magnify, mortify, quicken, redeem, sojourn…), states & qualities (affliction, contrition, lovingkindness, meekness, remnant, tribulation, zeal…), relational/covenant terms (kinsman, sojourner, birthright, betrothal…), archaic KJV words (froward, gainsay, holpen, lucre, peradventure, wax, wist, wont…), original-language study words (*hesed, shalom, ruach, nephesh, kavod, agapē, charis, logos, koinōnia, metanoia…*) | ~1,300 |
| **B** | **Biblical realia** — weights/measures/money/time (shekel, talent, ephah, omer, cubit, denarius, mite, jubilee…), tabernacle/temple/priestly (mercy seat, laver, ephod, breastplate, shewbread, veil…), flora/fauna/minerals/gems (hyssop, spikenard, behemoth, coney, onyx, jacinth…), tools/warfare/music/trades (goad, sickle, buckler, chariot, psaltery, timbrel…) | ~600 |
| **C** | **Geography & persons** — places (Eden, Sinai, Zion, Gethsemane, Patmos, Babylon, Sheol, Armageddon…) + minor biblical figures to round out the names section | ~400 |
| **D** | **Worship & institutions** — feasts (Passover, Pentecost, Atonement, Tabernacles, Purim…), the five offerings, rituals & vows (Nazarite, scapegoat, kinsman-redeemer, cities of refuge, Urim & Thummim…) | ~200 |
| **E** | **Types, symbols & figures** — horn, yoke, cup, vine, leaven, salt, rock, refuge; typology; biblical numbers | ~150 |
| **F** | **Historical theology** — councils (Nicaea, Chalcedon, Dort, Westminster…), creeds & confessions, eras (Patristics, Reformation, Puritanism…), classic heresies | ~250 |
| **G** | **Apologetics & worldviews** — theism/atheism/agnosticism, naturalism, evolution, comparative religion, the major cults (for discernment) | ~150 |
| | **Total** | **~3,050** *(buffer absorbs slugs already taken)* |

---

## 4. Suggested six-week arc (pace fully adjustable)

| Week | Focus | Lands near |
|---|---|---|
| 1 | Phase A: biblical verbs + states/qualities | ~5,277 |
| 2 | Phase A: relational/covenant + archaic KJV words | ~5,777 |
| 3 | finish Phase A (original-language) + start Phase B; **run 6,000 coverage audit** | ~6,277 |
| 4 | Phase B realia + Phase C geography | ~6,777 |
| 5 | Phase C persons + Phase D worship + Phase E types/symbols | ~7,277 |
| 6 | Phase F historical theology + Phase G apologetics + **gap-fill from audit → land exactly on 7,777** | **7,777** |

Milestones to mark: **5,000 · 5,500 · 6,000 · 6,500 · 7,000 · 7,500 · 7,777.**

---

## 5. Completeness backstop — the coverage audit *(tool to build)*

We already have KJV text (with inline Strong's) embedded in `docs/assets/chapters/*.json` for 29
books, and full public-domain KJV is freely available for the rest. Build a small
**`bin/dict_coverage_audit.py`** that:
1. Extracts the KJV vocabulary → frequency-ranks the significant words (drop function words /
   proper-name variants already in the names index);
2. Diffs that master wordlist against `data/dictionary-slugs.txt`;
3. Emits a **gap report** of meaningful biblical words we don't yet have.

Run it at the **6,000** mark and again before the final push, so the last batches aim precisely at
real gaps. This turns "every meaningful word" from aspiration into a checklist.

---

## 6. Per-session workflow (how we return to this)

Adam says *"continue the dictionary roadmap"* (or names a domain). Each session:
1. Pick the next domain / sub-batch from §3–§4.
2. **Slug-availability check against `data/dictionary-slugs.txt`** (never recreate).
3. Author a **20-entry batch JSON** → `data/dictionary-batches/batch-NN-topic.json`, full schema,
   MOOP house voice.
4. Validate HTML entities (valid named refs only — beware the recurring `&erevamp;` typo; use
   `&emacr;/&omacr;/&amacr;/&umacr;/&imacr;` for macrons).
5. `python3 bin/generate_dict_entries.py <batch.json>` → `python3 rebuild-dictionary.py`.
6. Stage **specific files only** → commit (Co-Authored-By: Claude Opus 4.7) → push.
7. Regenerate `data/dictionary-slugs.txt`; update the Progress Tracker below.

### Entry schema (per the established pipeline)
`slug, word, pronunciation, pos, etymology, biblical_def (~150–250w), webster_summary,
webster_full (list), scriptures (list of [ref, text]), corruption_summary,
corruption_paragraphs (list), roots_summary, roots_lines (list of [lang, strong#, word, gloss]),
usage (list of 3), related (list of [slug, label])`. For words with no real postmodern
redefinition, use the caveat template in `corruption_summary`.

---

## 7. Progress Tracker

| Date | Batch(es) | Topic | Entries | Running total |
|---|---|---|---|---|
| 2026-05-22 | 73–83 | Systematic-theology sweep (soteriology → worship) | +219 | **4,777** ✅ baseline |
| | | *— Phase A begins —* | | |
| 2026-05-23 | 84 | Phase A wk1 b1 — biblical action verbs (beseech, chasten, hearken, mortify, discern, entreat, forgive, prevail, prophesy, purge, purify, submit, testify, tremble, wait, watch, wrestle, yield, adjure, circumcise) | +20 | **4,797** |
| 2026-05-23 | 85 | Targeted: new `radical-two-kingdoms` (R2K) entry + sharpened `two-kingdoms-theology` corruption section to draw the classical-2K vs R2K line a reader had collapsed | +1 (1 new, 1 revised) | **4,798** |
| 2026-05-23 | 86 | Phase A wk1 b2 — more biblical action verbs (harden, humble, hunger, thirst, cast, lift, cling, exhort, expound, fast, forbear, fulfill, gather, strive, grow, guard, swear, hate, kindle, labor) | +20 | **4,818** |
| 2026-05-23 | 87 | Phase A wk1 b3 — biblical states & qualities, set 1 (lowliness, tenderness, blessedness, uprightness, weight, rejoicing, fulness, poverty, riches, triumph) | +10 | **4,828** |
| 2026-05-23 | 88 | Phase A wk1 b4 — biblical states & qualities, set 2 (blamelessness, sweetness, weariness, distress, terror, indignation, shamefacedness, emptiness, treasure, reward) | +10 | **4,838** |
| 2026-05-23 | 89 | Phase A wk1 b5 — finish states & qualities (godly-sorrow, sober-mindedness, heaviness, stillness, joy-unspeakable, brotherly-love, holy-boldness, fervor, zeal-of-god, steadiness) | +10 | **4,848** |
| 2026-05-23 | 90 | Phase A wk2 b1 — relational/covenant terms (household, generations, lineage, bond-of-peace, fellow-citizen, brotherhood, bridegroom, firstborn, espousal, handmaid) | +10 | **4,858** |

> **Next up:** Phase A wk1 batch 2 — more biblical action verbs (candidates: meditate-related, intercede-related,
> hush, harm, harden, humble, haste, hire, heed, hide, hush, hunger; +states/qualities words like affliction,
> contrition, lovingkindness, meekness, remnant, tribulation, zeal). Target ~5,000 first milestone.
