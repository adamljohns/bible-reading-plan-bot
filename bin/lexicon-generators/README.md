# Lexicon generator scripts

Moved here from `docs/lexicon/` on 2026-09-03. `docs/` is the published site
root and is synced verbatim to R2, so these one-off generators and their
`hebrew_words.json` input were being served publicly at
`usmcmin.org/lexicon/generate.py` and friends. Nothing referenced them.

They are kept because they are the provenance of the lexicon corpus: the
misfiled-Strong's-code defect the 2026-09-03 audit found (content written under
a neighbouring code) originates in these one-off scripts, not in the dictionary
pipeline, which does not share them.

`lexicon-manifest.json` deliberately stayed in `docs/lexicon/` — it is fetched
by `docs/sitemap.html` and `docs/timeline.html`.
