# Custom Worship nav icon — generate + finish

The Worship link currently reuses `shield-quill-note`. This makes a dedicated icon in the
house style (photoreal 3D gold shield), matching the existing `docs/assets/icons/shield-*.png` set.

## Step 1 — generate in ChatGPT (your USMC Ministries project, ~60 sec)
Open chatgpt.com → the pinned **"C) USMC Ministries"** project. **Upload `docs/assets/icons/shield-quill-note.png`
as a style reference**, then paste this prompt:

> Create a single app icon in the exact same style as the attached reference: a photorealistic,
> 3D-rendered, beveled and embossed **polished gold** emblem centered on a dark (near-black) heater
> shield with a thick polished gold beveled border, soft studio lighting and subtle gold glow,
> on a plain black background, perfectly square, centered, high resolution.
> The emblem is **an open hymnal / songbook with a few musical notes rising from its pages** —
> clearly "worship music." Same metal, lighting, bevel depth, and proportions as the reference shield.
> No text, no words, no watermark. One icon only.

(Alt emblem ideas if you want a different read: a **harp/lyre** (David's harp) with a musical note,
or **raised hands with a musical note**. Pick one — keep everything else identical.)

Download the result to: **`~/Documents/worship-icon-src.png`**

## Step 2 — tell me "icon's ready"
I run `bin/finish-worship-icon.sh ~/Documents/worship-icon-src.png`, which:
1. mattes the black box to transparency + derives bronze and `-lm` light-mode variants
   (via the existing `bin/matte_and_bronze_shields.py`, so it matches the set pixel-for-pixel),
2. `sips`-downscales to `shield-worship-music-96/48/24.png` (+ bare `.png`) in `docs/assets/icons/`,
3. swaps the Worship nav/hero/footer icon in `generate-worship-pages.js` from `shield-quill-note`
   to `shield-worship-music`, rebuilds the 1,439 pages + index,
4. swaps the icon in the Worship nav link on the ~36 hub pages,
5. adds the new icon to the brand gallery `docs/brand-assets.html`,
6. commits (scoped) and pushes.

Net: you paste one prompt and save one file; I do the rest.
