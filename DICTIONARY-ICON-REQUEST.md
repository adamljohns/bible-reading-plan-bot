# Shield-Icon Request — replace dictionary emojis with the shield set

**Goal:** the MOOP Dictionary UI currently uses a few raw emojis (💎 🎲 📖 🔍 etc.)
in places where the rest of usmcmin.org uses the custom **gold-on-dark heraldic
shield** icon set. This brief is for generating the missing shields (e.g. with
ChatGPT / DALL·E or a designer) so everything matches.

## The existing set (style reference)

- Location: `docs/assets/icons/`  ·  **96 shield icons already exist.**
- Naming convention: `shield-<name>-48.png` (also `-24`, `-96`, `-hires`, and a
  bare `.png`). Examples already in use by the dictionary:
  `shield-book-greek-48.png`, `shield-blog-quill-48.png`,
  `shield-chain-salvation-48.png`, `shield-chain-fire-48.png`,
  `shield-alpha-omega-48.png`.
- Master vector: `docs/assets/icons/icon-shield.svg`.

## Visual style (put this in the image prompt)

> A heraldic **shield** silhouette (rounded top corners, pointed base) in matte
> charcoal/near-black, with a single centered emblem rendered in **antique gold
> line-art** (`#D4AF37`), clean even stroke weight, slight inner bevel, no text,
> **transparent background (PNG)**, square canvas, crisp at 48×48 and 96×96. The
> emblem reads instantly as a silhouette. Match the existing
> `shield-*-48.png` set exactly in shield shape, gold tone, and stroke weight.

Generate each at **96×96** (then downscale to 48 and 24).

## Icons to create (emoji → shield)

| Emoji | U+ | Where it's used | Proposed filename | Emblem to draw |
|---|---|---|---|---|
| 💎 | 1F48E | "Special Directories" heading | `shield-diamond-48.png` | a faceted gem / diamond |
| 🎲 | 1F3B2 | "Random" entry button | `shield-die-48.png` | a single pip-die (dice) |
| 📖 | 1F4D6 | "In the Text" concordance heading (1,861 entry pages) | `shield-open-book-48.png` | an open book |
| 🔍 | 1F50D | search box (dictionary + lexicon) | `shield-search-48.png` | a magnifying glass |
| 📝 | 1F4DD | "Suggest a Word" form heading | `shield-quill-note-48.png` | a memo/quill-on-page (distinct from the blog quill) |
| 🗺 | 1F5FA | topic/section accents | `shield-map-48.png` | a folded map |
| 🌙 | 1F319 | dark-mode toggle | `shield-moon-48.png` | a crescent moon |
| ☀ | 2600 | light-mode toggle | `shield-sun-48.png` | a sun |
| ↔ | 2194 | "Biblical Order" (headship · roles) accent | `shield-balance-48.png` | scales/balance (order, roles) |

(💠 the user calls it "diamond" — it is rendered as 💎 `U+1F48E`, gem stone.)

## After the PNGs exist

Drop them in `docs/assets/icons/`, then swap the emoji for an `<img>` in
`rebuild-dictionary.py` (the index template) and `bin/enhance_entry_pages.py`
(the "In the Text" heading), matching the existing pattern, e.g.:

```html
<h3><img src="../assets/icons/shield-diamond-48.png" alt="" width="20" height="20"> Special Directories</h3>
```

Then `python3 rebuild-dictionary.py` and `python3 bin/enhance_entry_pages.py`
to propagate. (Leave the dark/light toggle emojis last — they're tiny and
low-priority.)
