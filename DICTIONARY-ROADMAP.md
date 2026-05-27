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
| 2026-05-23 | 91 | Phase A wk2 b2 — archaic KJV vocabulary (gainsay, holpen, lucre, peradventure, wax, wist, wont, fain, succor, twain) | +10 | **4,868** |
| 2026-05-23 | 92 | Phase A wk2 b3 — original-language anchor entries (gnosis, splagchnon, makrothumia, tapeinophrosune, paraklesis, plerophoria, kurios, theos, berith, tselem) | +10 | **4,878** |
| 2026-05-23 | 93 | Phase A wk2 b4 — more original-language anchors (bara, yare, martus, aionios, hagiasmos, apokalupsis, diakonia, presbuteros, charisma, proskuneo) | +10 | **4,888** |
| 2026-05-23 | 94 | **Phase B opener** — biblical realia (shekel, talent, cubit, mite, laver, shewbread, spikenard, coney, onyx, psaltery) | +10 | **4,898** |
| 2026-05-23 | 95 | Phase B b2 — tabernacle furnishings (ark-of-the-covenant, mercy-seat-doctrine, candlestick, veil-of-the-temple, mitre, girdle, urim-and-thummim, breastplate-of-judgment, ephod-doctrine, red-heifer) | +10 | **4,908** |
| 2026-05-23 | 96 | Phase B b3 — Israel's sacred calendar (passover-doctrine, pentecost-doctrine, firstfruits-feast, feast-of-trumpets, new-moon, sabbath-day-doctrine, weekly-sabbath, year-of-release, meat-offering, high-sabbath) | +10 | **4,918** |
| 2026-05-23 | 97 | Phase B b4 — weights, measures, coins (mina, farthing, pence, stater, bekah, gerah, cab, homer, span, furlong) | +10 | **4,928** |
| 2026-05-23 | 98 | Phase B b5 — biblical flora & fauna (vine-doctrine, shepherd-and-sheep, lamb-doctrine, lion-doctrine, dove-doctrine, balm-of-gilead, serpent-doctrine, raven-doctrine, sparrow-doctrine, almond-tree) | +10 | **4,938** |
| 2026-05-23 | 99 | Phase B b6 — biblical tools, warfare, music (sword-of-the-spirit, helmet-of-salvation, breastplate-of-righteousness, buckler, bow-and-arrow, goad, yoke-doctrine, potter-and-clay, threshingfloor, trumpet-doctrine) | +10 | **4,948** |
| 2026-05-23 | 100 | **Phase C opener** — biblical persons (melchizedek-doctrine, caleb-doctrine, boaz-doctrine, anna-the-prophetess, priscilla-and-aquila, barnabas-doctrine, cornelius-the-centurion, philemon-and-onesimus, tabitha, titus-doctrine) | +10 | **4,958** ***milestone batch 100*** |
| 2026-05-27 | — | **CROSS-LINKAGE SPRINT** — bin/build_dict_manifest.py regex fix (294 missing entries recovered) + bin/autolink_chapters.py (+33,291 dict-links across 1,181 chapters) + bin/autolink_lexicon_from_dict.py (+5,015 backlinks via Strong's numbers across 1,659 lexicon pages) + bin/autolink_blog.py (+4,122 dict-links across 153 blog posts). Total: **42,428 new cross-links across 2,993 site pages.** | linkage | 4,958 |
| 2026-05-27 | 101 | **Phase B b7 (gems)** — Rev 21:19-20 New Jerusalem foundation stones #1-10 (jasper, sapphire, chalcedony, emerald, sardonyx, sardius, chrysolite, beryl, topaz, chrysoprasus) — themed coherent batch with high-priest breastplate / Eden / theophany typology | +10 | **4,968** |
| 2026-05-27 | 102 | Phase B b8 — final 2 NJ stones (jacinth, amethyst) + OT breastplate gems (carbuncle, ligure, agate, diamond, ruby) + organic pearl + cornerstone-doctrine + gold-bible — completes the precious-stones thread with kingdom-cost (pearl), Christology (cornerstone), and the metal of God's presence (gold) | +10 | **4,978** |
| 2026-05-27 | 103 | Phase B b9 — biblical metals (silver-bible, brass-bible, iron-bible, copper, tin, lead-metal) + cosmology (abyss-doctrine, deep-bible, heavens-bible, mountains-bible) — completes the metal-by-metal theology (silver=redemption price, brass=judgment, iron=Messianic rod, copper=craftsmanship, tin/lead=dross) and opens the three-heavens cosmology | +10 | **4,988** |
| 2026-05-27 | 104 | Phase C b2 — gospel figures (joseph-of-arimathea-doctrine, nicodemus-doctrine, zacharias-prophet, elisabeth-mother-of-john, simeon-the-righteous, centurion-at-cross, malchus, jairus-the-ruler, zacchaeus-doctrine, pilate-doctrine) — supporting characters of the gospel narrative, each anchored in canonical typology | +10 | **4,998** |
| 2026-05-27 | 105 | 🎉 **5,000 MILESTONE BATCH** — Names of God and Christological titles (i-am-that-i-am, the-almighty, most-high, holy-one-of-israel, lord-of-lords, light-of-the-world, resurrection-and-life, door-of-the-sheep, branch-of-the-lord, servant-of-the-lord) — names of the One the whole dictionary is about. From the burning bush self-revelation to the I AM sayings of John to the Servant of Isaiah 53. | +10 | **5,008** 🎉 **MILESTONE CROSSED** |
| 2026-05-27 | — | Re-link sweep — chapter/blog/lexicon linkers re-run after batches 101-105 (+13,519 additional cross-links; cumulative session total ~55,947) | linkage | 5,008 |
| 2026-05-27 | 106 | Phase C/D — more Christological titles (ancient-of-days-doctrine, sun-of-righteousness, desire-of-nations, shiloh-doctrine, great-shepherd, chief-shepherd, word-made-flesh, logos-doctrine, only-begotten-doctrine, captain-of-our-salvation) — Daniel 7 throne-room, Malachi's last paragraph, Hag 2:7's second-temple promise, Gen 49:10's Shiloh, three Shepherd titles, Logos doctrine, monogenes, archēgos | +10 | **5,018** |
| 2026-05-27 | 107 | 💙 **PERSONAL / FAMILY BATCH** — moop (editor's easter-egg signature), maria (wife — Marah-typology of bitter waters made sweet by the Cross-tree), marah-doctrine (Exod 15:23-26, Jehovah-Rapha), malachi-andrew + hope-twin + mercy-twin (memorial entries for three children Adam & Maria lost to miscarriage in Okinawa 2017-2018), luanne-name (mother), ronald-name (brother), johns-family-doctrine (editor's dedication), okinawa-personal (the family's biblical place-of-grief). Plus `bin/add_personal_notes.py` injecting "In This Editor's House" sections into the 8 existing entries naming editor's living children (Gideon, Boaz, Shiloh) + siblings (David, Joshua, Hannah) + lost daughters' name-roots (Hope, Mercy). Plus NEW `docs/dictionary/baby-names.html` (86 curated boy/girl/unisex names with Hebrew/Greek meaning, linked from the main index). | +10 | **5,028** |
| 2026-05-27 | 108 | 12-tribe-sons entries (reuben, simeon, levi-son, naphtali, gad, asher, issachar, zebulun, benjamin, ephraim) — completes most of the previously-missing tribal patriarchs so baby-name lookups for these classic biblical names land on real entries | +10 | **5,038** |
| 2026-05-27 | 109 | Popular biblical female names that were missing (eve, chloe, lois, eunice, claudia, damaris, susanna, julia, asenath, huldah-prophetess) — Mars' Hill convert, Corinthian-divisions reporter, Timothy's grandmother + mother, Christ's financial supporters, Paul's Roman greeting-list women, Josiah's prophetess — all now baby-name-lookup-discoverable | +10 | **5,048** |
| 2026-05-27 | — | Expanded `bin/build_baby_names.py` from 86 → **144 curated baby names** (93 boys + 44 girls + 7 unisex); folded in batches 108-109 + ~30 existing slugs that were missed in first pass | curation | 5,048 |
| 2026-05-27 | — | 💙 **Baby-names with VARIANTS** — refactored `bin/build_baby_names.py` to accept `(slug, meaning, variants_list)` tuples. Each card now shows nicknames + language variants (English, Hebrew, Greek, Spanish, Italian, etc.). Final tally: **144 primary names + 418 variants = 562 displayed names** (Adam's target was 333; well past). Cards visually distinguish variants with a dashed border-top and gold italic styling. | curation | 5,048 |
| 2026-05-27 | — | 💙 **Baby-names v3 — SEARCH + POPULARITY + CHRISTIAN TRADITION** — per Adam: (1) JavaScript search box that filters by name + variant + meaning so typing "Susie" finds Susanna and "Pete" finds Peter; (2) 1-5 popularity stars on every card so rare vs. common names are visible at a glance; (3) new Christian-Tradition section (82 names) covering Charles, William, Henry, Catherine, Theresa, Augustine, Wesley, Calvin, Knox, Tyndale, virtue names (Faith, Hope, Charity, Grace, Joy, Trinity), and early-church saints (Cecilia, Agnes, Perpetua, Felicity, Polycarp, Ignatius). Info-only cards for non-dict entries (no broken links). New tally: **226 primary names + 612 variants = 838 displayed**. | curation | 5,048 |
| 2026-05-27 | — | 💙 **Baby-names v4 — POPULARITY RECALIBRATED against real 2024 SSA data**. Pulled actual Social Security Administration top-1000 baby-name rankings (via Today.com, Mother.ly, Sense-U) and adjusted 67 of 226 ratings. Bumped UP names with surprisingly strong modern usage (Levi #15, Asher #22, Ezra #47, Naomi #51, Sebastian #14, Owen #21, Silas #92). Bumped DOWN classic biblical names that have declined from peak (Mary, Rebekah, Rachel, Esther 5→4; Mark/Paul/Peter/Timothy/Stephen 5→4; Catherine/Margaret/Theresa/Helena/Christina 5→4). Distribution now bell-curves correctly: 46/53/54/38/35 across ★5/★4/★3/★2/★1. | curation | 5,048 |
| 2026-05-27 | — | Re-link sweep #3 — chapter/blog/lexicon linkers re-run after batches 107-109 (+6,373 chapter links + 96 blog + 161 lexicon backlinks = +6,630 additional cross-links). Big jump came from new tribal-name tokens (Reuben, Simeon, Asher, etc.) which appear constantly in OT chapter text. | linkage | 5,048 |
| 2026-05-27 | 110 | Phase C — obscure but baby-name-friendly biblical figures (hadassah, jemima, keziah, shem, eliezer, jubal, jabal, eber, cleopas, abijah-king) — Esther's covenant-Hebrew name; Job's three restored daughters; Gen 4's three culture-founder brothers; Hebrew-root patriarch Eber; Emmaus-road disciple Cleopas; Abijah's double identity (king of Judah + priestly course of Zacharias) | +10 | **5,058** |
| 2026-05-27 | — | Baby-names builder folded in batch 110 + popularity. Final session tally: **100 biblical boys + 47 biblical girls + 7 biblical unisex + 43 Christian-tradition boys + 39 Christian-tradition girls = 236 primary names, 864 total displayed with variants**. | curation | 5,058 |

> **Next up:** Continue toward 7,777 (2,719 entries to go). The baby-names directory now at 864 displayed names
> with search + popularity + Christian-tradition section. Possible next batches: more OT kings
> (Jehoshaphat, Joash, Amaziah, Ahaz, Asa-related sources), more minor characters (Cleopas's wife? other
> Emmaus-road figures?), more covenant doctrine, more biblical institutions (cities of refuge, jubilee,
> year-of-release), more Hebrew-Greek word studies, more flora/fauna/realia.
