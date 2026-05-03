# MOOP Dictionary Changelog

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
