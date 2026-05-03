# MOOP Dictionary Changelog

## V5.3 — 2026-05-03 · Disclosure UX + BTE-John Pilot

### What changed

Three improvements after Adam noticed UX issues with the corruption section's expand/collapse pattern:

#### 1. Disclosure UX fixed across all 3,777 entries

**Old (buggy) behavior:**
- Click "expand to see more" → the helpful italic blurb above disappears
- The label still says "expand to see more" even when expanded
- Disclosure triangle is browser-default grey

**New behavior:**
- Italic blurb stays visible always (it provides context for the expanded text)
- Label toggles "expand to see more" ↔ "show less"
- Custom yellow CSS triangle that rotates -90° (collapsed) ↔ 0° (open)
- Cross-browser consistent (no `::-webkit-details-marker` reliance)

Tooling:
- `bin/fix_details_ux.py` — one-time sweep that handles three template variants
  (new generator output, older one-line CSS, and stub entries with `<details>`
  but no toggle JS at all). Modified 3,382 + 339 entries in two passes.
- Generator template (`bin/generate_dict_entries.py`) updated so new batches
  get the correct CSS + JS automatically.

#### 2. BTE-John Dictionary Integration (pilot)

Adam's vision: clicking dictionary-defined words inside Bible verses should
surface the dictionary entry. First experiment scoped to the Gospel of John
(bookId 43) to feel out the UX before expanding.

**How it works:**
- `bin/build_dict_manifest.py` builds `/dictionary/manifest.json` —
  a 97 KB lookup with 1,905 single-word tokens + 1,299 multi-word phrases
  mapping lowercased headwords to their slug.
- `docs/bible.html` (BTE viewer) gained:
  - CSS for `.dict-link` (subtle gold dotted underline; gold-on-hover)
  - `loadDictManifest()` lazy-fetch (caches after first request)
  - `enrichDictionaryLinks(bookId)` post-render hook that walks each
    `.verse-text` span via TreeWalker on text-nodes (preserves existing
    inline HTML like translator-italics), wraps matched words in
    `<a class="dict-link">` to `/dictionary/<slug>.html`
  - John-only gate via `DICT_ENABLED_BOOKS = new Set([43])` so other books
    render unchanged during the pilot
  - One-time toast: "Dictionary lit up — tap dotted words to explore (John pilot)"

**Smoke-test on John 1-3 sample verses:** 12 dictionary links across 7 verses.
Words like `Word`, `Light`, `Darkness`, `begotten`, `everlasting`, `Jesus`,
`truth`, `Father` light up. Words that didn't match (`life`, `beginning`,
`world`, `believeth`) are dictionary content gaps — entries to add later.

**v2 candidates:**
- Multi-word phrase matching (`son of god`, `lamb of god`, `born again`,
  `kingdom of god`) — manifest already includes the phrases array,
  highlighter just needs a phrase-pass
- KJV verb-form normalization (`loveth` → `love`, `believeth` → `believe`)
- Hover preview popovers (fetch entry's biblical_def into a tooltip without
  navigating away)
- Expand from John to other books once UX is confirmed

#### 3. Generator docstring documents the editorial rule

`bin/generate_dict_entries.py` docstring now carries the Modern Corruption
editorial principle (postmodern redefinition, NOT orthodox teaching restated)
with examples — so future batches don't regress.

### Files changed

- `bin/audit_corruption_sections.py` (new — V5.2)
- `bin/fix_corruption_sections.py` (new — V5.2)
- `bin/fix_details_ux.py` (new)
- `bin/build_dict_manifest.py` (new)
- `bin/generate_dict_entries.py` (template + docstring updated)
- `docs/bible.html` (BTE viewer; CSS + dict-integration JS)
- `docs/dictionary/manifest.json` (new — 97 KB lookup table)
- 3,777 dictionary entries (corruption-section fixes + disclosure-UX fixes)

---

## V5.1 — 2026-05-03 · The 3,777 Push

### What changed

Continuation of V5.0 the same evening: **+316 net new entries** across 13 batches (20-32), bringing the dictionary to exactly **3,777 entries** — the round target the user requested.

| Batch | Theme | Count |
|---|---|---:|
| 20 | Top dangling chips, set 1 | 25 |
| 21 | Top dangling chips, set 2 | 25 |
| 22 | Top dangling chips, set 3 | 24 |
| 23 | Doctrinal anchors | 25 |
| 24 | Bible places & people | 25 |
| 25 | OT concepts (offerings, furnishings, vows) | 25 |
| 26 | NT concepts (apocalyptic, gospel) | 25 |
| 27 | **Scoff cluster** (user request) | 26 |
| 28 | Christian ethics | 25 |
| 29 | Letter gap fills (Q/Y/Z/U/V/K) | 26 |
| 30 | Wisdom + pastoral office | 25 |
| 31 | Worship & liturgy | 25 |
| 32 | Closeout (Hebrews, Israel, Money, etc.) | 15 |

### Highlights

- **Scoff cluster** (batch 27): user noticed `scoff` was missing and asked for the surrounding family. Resulted in 26 entries: scoff, scoffer, scorner, mock, mocker, derision, ridicule, jest, taunt, jeer, sneer, gainsayer, railer, reviler, blasphemer, impudent, insolent, arrogant, haughty, presumptuous, fool-biblical, psalm-1, froward, stiff-necked, rebuke-biblical, unteachable.
- **Doctrinal anchors** (batch 23): eternality, effectual-call, indwelling, divine-impassibility, definitive-sanctification, mystical-union, spiritual-union, forensic-justification, active-obedience, passive-obedience, doctrines-of-grace, special-grace, saving-grace, moral-influence, governmental-theory, classical-theism, eternal-procession, nestorianism, eutychianism, augustinianism, socinianism, homoiousion, semi-arianism, limited-omniscience, prevenient.
- **Worship & liturgy** (batch 31): votum, salutation, invocation, call-to-worship, prayer-of-confession, assurance-of-pardon, collect, te-deum, kyrie-eleison, plus all the major liturgical seasons (Advent, Epiphany, Lent, Pentecost, Trinity, Ordinary Time, Christ the King, Reformation, All Saints, Maundy Thursday, Holy Saturday, Ascension Day).
- **Lexicon stub backstop**: every entry continues to use the `<a href>` link where the H#### / G#### file exists and a plain `<span class="lexicon-link">` where it doesn't, so future lexicon stub generation will upgrade these without re-editing entries.

### Letter coverage — V5.1 final

| Letter | Count | | Letter | Count |
|---|---:|---|---|---:|
| A | 296 | | N | 92 |
| B | 200 | | O | 102 |
| C | 313 | | P | 281 |
| D | 165 | | Q | 16 |
| E | 169 | | R | 159 |
| F | 144 | | S | 379 |
| G | 146 | | T | 213 |
| H | 161 | | U | 38 |
| I | 132 | | V | 63 |
| J | 119 | | W | 120 |
| K | 47 | | Y | 21 |
| L | 124 | | Z | 21 |
| M | 224 | | | |

Q/Y/Z still thinnest but improved noticeably.

### Files

- 13 new JSON batches in `data/dictionary-batches/` (batch-20-top-chips-1.json through batch-32-closeout.json) preserved as source-of-truth.
- All 316 HTML entries generated by `bin/generate_dict_entries.py`.
- `rebuild-dictionary.py` ran clean against the full 3,777 corpus.
- All entries carry V5.0 footer (V5.1 is changelog version, not on-page; update unnecessary at this scale).

---

## V5.0 — 2026-05-02 · Pastoral Lexicon Edition

### What changed

This release is the largest single expansion of the MOOP Dictionary in its history: **+481 net new entries** across two large pushes, finishing the dictionary at **3,461 entries**.

#### Push 1 (early session): +301 entries (12 thematic batches + hearth)

Cluster build-out following the user's Apr 29 worship-posture / OT-figure batch:

| Batch | Theme | Count |
|---|---|---:|
| ad-hoc | hearth | 1 |
| 1 | Hospitality / hearth / fire | 25 |
| 2 | Letter-gap fills (Q/Y/Z/U/V) | 25 |
| 3 | Worship postures continued | 25 |
| 4 | NT figures | 25 |
| 5 | Fruit-of-spirit virtues | 25 |
| 6 | Marine / military-faith bridges | 25 |
| 7 | Stewardship / work | 25 |
| 8 | Prophetic vocabulary | 25 |
| 9 | Covenant terms | 25 |
| 10 | Liturgical / sacrament | 25 |
| 11 | Spiritual warfare | 25 |
| 12 | Family / marriage / headship | 25 |

#### Push 2 (later session): +180 entries (7 thematic batches + 3 user-requested)

| Batch | Theme | Count |
|---|---|---:|
| 13 | Church history figures | 25 |
| 13b | User-requested words (`intelligible`, `nothingness`, `absolute`) | 3 |
| 14 | Eschatology | 25 |
| 15 | Hermeneutics | 25 |
| 16 | Biblical-theology motifs | 26 |
| 17 | More OT figures | 25 |
| 18 | More NT figures | 25 |
| 19 | Apologetics vocabulary | 26 |

### Infrastructure changes

- **`bin/generate_dict_entries.py`** added — JSON-driven HTML generator. Each batch lives as a JSON file in `data/dictionary-batches/`; the generator emits the HTML files matching the existing `selah.html` / `hearth.html` template. Future batches need only the JSON content, not the 200-line HTML boilerplate per entry.
- **`bin/audit_dangling_chips.py`** added — scans every entry's related-words chips for slugs that don't have corresponding `.html` files. Current count: 1,541 distinct dangling targets, 2,732 total dangling references. These are the natural follow-up — most are real concept-slugs that should become future dictionary entries.
- **V4.0 → V5.0 footer migration** — all 3,461 entries now read `MOOP Dictionary V5.0 · Pastoral Lexicon Edition`. The previous footer drift between `var(--gold)` and `#D4AF37` color variants was caught and fixed (two `sed` patterns covered both).
- **`rebuild-dictionary.py`** ran clean against the full corpus.

### Forms backend setup (FormSubmit.co)

Audited and fixed three forms across two repos:

- **`docs/freedom/intake.html`** (bible-reading-plan-bot) — replaced `mailto:adam@usmcmin.org` with FormSubmit AJAX (`adam.l.johns@gmail.com`). Matches the working pattern in `docs/serving-intake.html`, `docs/mentoring-intake.html`, etc.
- **`shop.html`** (usmcmin-com) — replaced `action="#"` with FormSubmit AJAX (`usmcministries2022@gmail.com`) for the "Notify Me" launch-list signup.
- **`citizen.html`** (usmcmin-com) — added a new "Submit a Tip / Score Update" form (FormSubmit AJAX → `usmcministries2022@gmail.com`).

The dictionary's Suggest-a-Word form was already wired to FormSubmit (`usmcministries2022@gmail.com`) and survives `rebuild-dictionary.py` runs because the form is embedded in the rebuild template.

### Known follow-ups (not addressed in V5.0)

1. **Featured sections lost from index.** The pre-cfb7e52ed `index.html` carried Most Corrupted Words, Gen-Z Decoded, Millennial Decoded, Gen X Decoded, Boomer Decoded, Doctrinal Anchors, and a Word-of-the-Day widget. `rebuild-dictionary.py`'s template does not include them, so each rebuild wipes them. The pre-rebuild `index.html` is preserved at `docs/dictionary/_archive/index-with-featured-sections.html.bak` for restoration. Recommended fix: extract the featured-section HTML blocks and inject them into `rebuild-dictionary.py`'s template so they survive future rebuilds.

2. **Dangling related-chip targets (1,541).** Most are reasonable concept-slugs that should become future entries (e.g., `parables`, `lord-supper`, `deity-of-christ`, `image-of-god`, `mammon`, `isaiah-53`, `blood-of-christ`, `fear-of-the-lord`). Run `python3 bin/audit_dangling_chips.py` to see the prioritized list. The top 50 would be a productive next batch.

3. **Lexicon stub back-fill.** Several Hebrew/Greek references in roots-sections render as plain `<span>` rather than `<a href>` because the corresponding `H####.html` / `G####.html` lexicon entry doesn't exist locally (e.g., `H4670` *miftan*, `H4168` *moqed*, `G2625` *kataklino*, `G5381` *philoxenia*). Generating lexicon stubs would unlock these links.

4. **Letter coverage still uneven.** Even after V5.0: Q (~10), Y (~12), Z (~19), K (~40), U (~29), V (~51) remain the thinnest letters. Future batches might continue to fill these.

5. **Cross-reference audit.** Scripture `<a href="../bible.html?ref=...">` links and Strong's `<a href="../lexicon/...">` links should be swept for correctness across the whole corpus. Not all current references have been verified.

6. **Mobile/accessibility audit.** Each entry uses inline CSS-in-page (~70 lines per entry). Worth a one-pass review of mobile rendering and the `<details>` collapse pattern's screen-reader behavior. Not done in V5.0.

### Source-controlled batch JSONs

All 19 batch JSON files preserved in `data/dictionary-batches/`. Each is the source-of-truth for its batch; the HTML files are deterministic outputs. To regenerate any batch: `python3 bin/generate_dict_entries.py data/dictionary-batches/batch-N-name.json`.

---

## Pre-V5.0 — incremental growth

The dictionary grew from ~489 entries (the first rebuild commit, `bd9cd4466`) to 2,981 entries by the start of this session through many smaller batches across 2024-2026. Earlier batches included Apr 17-29 enrichments (worship postures, OT figures, El-names, kings) and various cross-reference / signature work in the church-directory side of the same repo.

For pre-V5 detail, see `git log --oneline -- docs/dictionary/`.
