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
1. **PPT projection slides** — 135 decks (~50 MB) found in
   `~/Documents/BU2TB-Archive/iCloud-Consolidation/Ministry (TTF)/Worship Songs (ppt)`.
   32+ match songs by title. **Decision needed:** (a) copy the `.ppt` into the repo as-is
   (+50 MB to the Pages repo), (b) install LibreOffice and convert to lightweight PDFs
   (needs a download + ~minutes), or (c) host slides elsewhere and link out. Not committed
   tonight to avoid bloating the repo / installing software without your call. Override
   mechanism is ready either way.
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
