# 201 entries are on a second page template

**Found:** 2026-08-06 · **List:** `data/template-b-entries.txt`

Adam: *"find entries that don't fit our framework, our theme, our look — we want
it all standardized and beautifully laid out."*

This is that. **201 of 7,873 entries render as a visibly different website.**
Not thin, not broken — the content is often excellent. They came off a
different generator, and a reader who lands on one sees a different site.

## What the reader actually sees

| | House template (7,594) | Template B (201) |
|---|---|---|
| Nav | Home · Watchman · BTE · Lexicon · Cross-Refs · Dictionary · Blog · Connect, with shield icons | MOOP · BTE · Lexicon · Dictionary · Cross-Refs, no icons |
| Prev/next entry | yes (`← Wrath of God … Wreckage →`) | **none** |
| Title | centred | left-aligned |
| Etymology | centred prose under the title | merged into one **"Etymology & Webster 1828"** box |
| Definition heading | **"Biblical Definition"**, boxed, shield icon | **"Biblical Meaning"**, plain heading, no box |
| Action buttons | 6 — incl. Copy Definition and Amen | 4 — **no Copy Definition, no Amen** |

Losing prev/next and the Amen button matters beyond looks: those are engagement
surfaces the rest of the corpus has.

## Why the layout audit under-reported this

`bin/dict_layout_audit.py` fingerprints house markup (`class="webster-inner"`,
`class="pronunciation"` …). Template B carries the same *content* under
different markup and headings, so it scored as "missing 5 sections" when
nothing is missing — it is a different shape. The audit's 204-entry group is
almost exactly this set.

**The two are cleanly separable** — every page has "Biblical Definition" or
"Biblical Meaning", never both, so conversion can be driven off that marker.

## Converting — and the trap

Do NOT regenerate these from batch JSON. `generate_dict_entries.py` emits
sections **without** the `id="definition"` / `"scriptures"` / `"corruption"`
anchors that 7,639 live pages carry, and nothing in the repo restores them —
they came from a one-off pass. Regeneration is lossy (proven 2026-08-06).

Convert by transforming the published HTML in place:

1. Split the merged **"Etymology & Webster 1828"** box into the house
   `etymology` block plus a `Webster 1828 Definition` section.
2. Rename **"Biblical Meaning"** → **"Biblical Definition"** and wrap it in the
   house `.section` + `.biblical-def` container with the shield icon.
3. Swap the minimal nav for the house nav.
4. Add prev/next entry links (alphabetical neighbours from
   `data/dictionary-slugs.txt`).
5. Add the missing Copy Definition and Amen buttons.
6. Stamp the `id=` anchors so the audits and `find_concept_duplicates.py` can
   read them.

Do a handful first and eyeball them in a browser before running the batch —
these pages have good content and are worth not breaking.
