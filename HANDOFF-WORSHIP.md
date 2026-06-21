# Worship Songbook — Handoff

**Live:** https://usmcmin.org/worship.html (linked in the Bible Tools nav + footer + sitemap)
**Built:** 2026-06-13 overnight, autonomously, from Adam's request to turn his decades-old
chord archive into "the ultimate worship leader resource."

## What it is
A searchable directory of **1,439 songs** with the chords charted right over the lyrics —
faithful to Adam's original monospace charts. Each song page supports:
- **Transpose** up/down a half-step (chords shift, column alignment preserved)
- **Font size** +/- for stage reading
- **Chords on/off** (lyrics-only view)
- **Print** a clean sheet
- **Find on YouTube** deep-link (search), or an embedded video once curated
- Light/dark mode + mobile, matching the rest of the site

Counts: 1,162 praise & worship, 261 guitar tabs, 22 Christmas. 1,300 have an auto-detected key.

**Search by artist + popularity (2026-06-15):** the index search now matches **artist** too
(108 curated songs tagged from the YouTube log + cleaned `.crd` authors; artist shows on cards
and song pages). A **popularity score** (curated video +60, slides +25, key +10, praise +5)
powers a **"Best known" sort** and a **"★ Well-known only"** filter (≈139 songs with a video or
slides) — so the old deep-cut charts nobody leads can be hidden. To tag an artist by hand, add
`"artist":"..."` to a song in worship-overrides.json and rebuild.

## Source of truth
Archive: `~/Documents/01-Faith-Ministry/USMC-Ministries/Documents/Worship Songs (doc)/1) Indexes`
(1,178 `.crd` chord charts + 261 `.tab` guitar tabs). An identical copy lives under
`Ministry-Archive/`. The build reads `.crd`/`.tab`, never modifies the originals.

## Files (all in this repo)
- `generate-worship-pages.js` — the generator. Ingests the archive → `docs/data/worship-songs.json`,
  then emits `docs/worship.html` + `docs/worship/<slug>.html` (1,439 pages) + `docs/sitemap-worship.xml`.
- `docs/data/worship-songs.json` — the canonical song database (raw chart text + parsed metadata).
  The build is reproducible from this without the external archive.
- `docs/data/worship-overrides.json` — **hand-edited enrichment** (YouTube/slides/key per slug).
- `scripts/add-worship-nav.js` — inserts the Worship nav link on root hub pages (idempotent).

## Regenerate
```bash
cd ~/bible-reading-plan-bot
node generate-worship-pages.js            # rebuild pages from existing JSON
node generate-worship-pages.js --ingest   # re-read the archive (after adding/editing charts)
node generate-worship-pages.js --pages    # pages only, skip ingest (fastest)
```

## How to add a favorite YouTube version or slides (the vision)
Edit `docs/data/worship-overrides.json`, keyed by the song's slug (the filename under
`docs/worship/`, minus `.html`):
```json
{ "amazing-grace": { "youtube": "CDdvReNKKuk", "slides": "amazing-grace.pdf", "key": "G" } }
```
Then `node generate-worship-pages.js --pages`. A `youtube` value embeds the player;
a `slides` value adds a download button (drop the file in `docs/worship/slides/`).

## Open backlog (decisions for Adam)
1. **PPT projection slides — DONE (2026-06-14).** Adam approved: installed LibreOffice,
   converted the decks to PDF (104 song decks, only **5.9 MB** total — far under the 50 MB
   estimate). PDFs live in `docs/worship/slides/`. 32 decks whose title exactly matches a
   chord chart link inline on the song page ("📽 Projection slides (PDF)"); all 104 are
   browsable at **`/worship-slides.html`** (linked from the songbook hero). Re-convert:
   `/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to pdf --outdir docs/worship/slides "<deck>.ppt"`.
   To link a deck to a song, set `"slides":"<file>.pdf"` in worship-overrides.json + rebuild.
   ~70 decks are for songs we have no chord chart for yet (browsable in the library; could
   become new song pages later).
2. **The 16 `.doc` songbooks** (e.g. `Songbook.doc`, `Alphabetic index+songs.doc`) — could be
   converted (`textutil`) and offered as downloadable reference compilations.
3. **Duplicate songs** (e.g. `amazing-grace`, `amazing-grace-2`, `amazing-grace-tab`) — could
   be cross-linked as "other versions of this song."
4. **Tab-diagram detection** — files heavy with ASCII fret diagrams render faithfully but a few
   diagram lines get the lyric color instead of chord color. Cosmetic only.
5. **Custom hero/nav icon** — currently reuses the existing `shield-quill-note` (quill + note).
   A dedicated photoreal-gold worship icon could be generated in your ChatGPT image workflow.

## Commit scoping note
The repo carries thousands of uncommitted `docs/dictionary/` files from the fleet's crons.
Worship commits stage **only** worship paths + the 36 root nav edits — never `docs/dictionary/`.
Always `git add` explicit worship paths; never `git add -A` here.

---

## Sprint status — Phase A COMPLETE (2026-06-17)

24h sprint, 8-hour Phase A block. All shipped, verified, pushed, live:
- **A1 Full-text lyric search** — `docs/data/worship-search.json` (lazy-loaded), search matches title/artist/lyric.
- **A2 Credits & attribution** — songwriter / CCLI # / copyright parsed from charts → song data + a Credits block on each page + site-wide CCLI notice. (277 writers, 128 CCLI, 385 copyrights.)
- **A3 Project mode** — fullscreen lyrics-only for congregation (📽 button, every song).
- **A4 Stage mode** — fullscreen chords for the leader, transpose retained, auto-scroll (🎤 button).
- **A5 Set List builder** — `docs/worship-setlist.html`: add (search or "＋ Add to set list"), reorder, per-song key, shareable URL (`#s=slug~key,…`), combined print sheet.
- **A6 Data-quality sweep** — default-on "Worship only" filter hides ~156 non-worship rock/alt charts (high-precision flag; reversible; nothing deleted). Titles confirmed clean (no mojibake).
- **A7 QA** — 0 broken links, all controls compose, mobile/light verified.
- Earlier same arc: 132 curated YouTube videos (incl. 22 Christmas), 104 slide PDFs + library, version cross-linking, artist tags (108), popularity sort + well-known filter.

Index controls now: search (title/artist/lyric) · type chips · A–Z/Best-known sort · ★ Well-known only · 🎵 Worship only · alpha bar. Plus Projection slides library + Set List builder linked from the hero.

### Still open for Adam
- **Gold worship nav icon** — generate via his ChatGPT session (`WORSHIP-ICON-PROMPT.md`), then `bin/finish-worship-icon.sh`. Currently reuses `shield-quill-note`.

### Remaining backlog (Phase B & C — for a future run-block)
**Phase B (enrich the data):** ~~theme tags + Theme filter~~ ✅ · ~~scripture-reference detection → bible.html~~ ✅ (both shipped 2026-06-20, see below) · expand artist tagging (still ~108 curated) · tighten key detection.
**Phase C (power features & polish):** guitar chord diagrams + capo calculator · deepen YouTube coverage · index sections ("Most-used / Recently added / By theme") · whole-songbook PDF export · per-song OG/SEO · wire the gold icon.

Operating contract (unchanged): edit `generate-worship-pages.js` only (never hand-edit generated HTML); `node generate-worship-pages.js --pages` (or `--ingest` if parsing changed; confirm 1439); verify in preview; commit SCOPED worship paths only — NEVER `git add -A`, NEVER `docs/dictionary/`; `git fetch origin main` + fast-forward push.

---

## Phase B — partial (2026-06-20, single 30-min block, commit `1def7b438`)

Shipped, verified in preview, pushed live:
- **Theme tags + Theme filter.** 12 service-moment themes derived from each song's
  title+lyrics at page-build (Cross & Blood 100, Praise & Adoration 75, Holy Spirit
  77, Love of God 62, Grace & Salvation 38, Surrender 36, Christmas 34, Thanksgiving
  33, King & Majesty 32, Comfort & Trust 27, Communion 20, Resurrection 16). **437
  songs tagged (30%)**, high-precision per-theme thresholds (`min` hits in `THEMES`).
  New **Theme** chip row on the index (with counts) + `?theme=<key>` deep-link; each
  song page shows its theme chips, linking back to the filtered index.
- **Scripture-reference detection → bible.html.** Charts that cite "Book Ch:V"
  (or the idiomatic "Psalm 23") get a 📖 Scripture row deep-linking to
  `bible.html?ref=...`. Recognized-books-only (`SCRIPTURE_BOOKS` map) so no dead
  links; requires a colon for precision. ~40 song pages carry refs so far.

All derived at page-build — **no re-ingest needed**; `node generate-worship-pages.js
--pages` regenerates. To tune a theme, edit its `words`/`min` in the `THEMES` array
and rebuild. To recognize more scripture book abbreviations, add to `SCRIPTURE_BOOKS`.

**Still open in Phase B:** expand artist tagging (only ~108 curated; could parse more
from `.crd` authors / the YouTube log) · tighten key detection (1,300/1,439 have a key).
Then Phase C (chord diagrams, capo calc, deeper YouTube, songbook PDF, wire gold icon).

---

## Purge + additions (2026-06-21, commit `bcf54b457`) — directory now 1,474 songs

**Purge (Adam: "purge non-worship, KEEP Christian music").** Investigated the 156
charts the "Worship only" filter hides — they turned out to be almost entirely
Adam's **1990s Christian-rock/alt collection** (Caedmon's Call, DC Talk, Delirious?,
Bride, Dogwood, Stavesacre, Audio Adrenaline, Big Tent Revival, even a Psalm 23
setting), NOT secular junk. Per his call, **kept all of those** (still hidden behind
the filter) and purged only the genuinely-secular **Jeremy Enigk solo album**
(5 tracks: carnival, explain, lewis-hollow, lizard, return-of-the-frog-queen).
Purge is the `PURGED` set in the generator — durable across re-ingest, reversible
(archive untouched; clear a slug + `--ingest` to restore).
⚠️ Do NOT mass-delete the filtered set — it's Christian music Adam wants kept.

**Additions — 40 worship standards.** We had projection slides but no chord chart
for ~41 modern standards; added them as **lyrics-only pages** (How Great Is Our God,
Mighty to Save, Open the Eyes of My Heart, Heart of Worship, In Christ Alone, Be Thou
My Vision, Indescribable, God of Wonders, Agnus Dei, Blessed Assurance, Come Thou
Fount, …). Lyrics extracted from the slide PDFs via `scripts/build-worship-extras.js`
(re-runnable); each links its projection deck; writer credits added for the
well-known ones. Lyrics-only pages hide the Transpose/Chords controls
(`song.lyricsOnly`). Stored in **`docs/data/worship-extra-songs.json`** and **merged
at ingest** (see `EXTRA_JSON` in the generator) so they survive a re-ingest.
To add chords later: set `youtube`/`key` etc. in worship-overrides.json, or replace
the body with a real chart and drop `lyricsOnly`.

**Still available as future song sources:** ~31 more slide decks loosely match an
existing chart (skipped as probable dupes — worth a manual pass); the 16 `.doc`
songbooks; deepening chord charts on the 40 lyrics-only standards.
