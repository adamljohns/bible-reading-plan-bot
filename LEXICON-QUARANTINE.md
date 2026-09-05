# Lexicon Quarantine Ledger

Pages here failed `bin/lexicon-gate.js` and were pulled out of
`docs/sitemap-lexicon.xml` and marked `noindex, nofollow`. **Nothing was
deleted.** Every page is still on disk and still returns 200 to anyone holding
the URL; it is simply no longer offered to search engines.

Restore a page once its content is fixed and the gate passes:

    node bin/lexicon-gate.js docs/lexicon/G1018.html   # must pass first
    python3 bin/lexicon-quarantine.py --restore docs/lexicon/G1018.html

Restore everything (undo the whole action):

    python3 bin/lexicon-quarantine.py --restore --all

Both paths regenerate the sitemaps, so the page returns to
docs/sitemap-lexicon.xml automatically. Lines below are machine-readable.

**0 pages currently quarantined.**

## finalized malformed redirects (48 pages, 2026-09-04)

Double-prefix GG/HH duplicates and `template.html` were converted to `lexicon-redirect` stubs pointing at the canonical G/H entry (or lexicon index). They stay noindex and out of the sitemap.

