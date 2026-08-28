#!/usr/bin/env python3
"""mbt-lexicon-harvest.py

Backfill the Strong's lookup from our own authored MBT batches.

The local lexicon pages (docs/lexicon/<id>.html) cover ~6,200 numbers; the
other ~1,500 either have no page or only a stub title, which leaves
bin/mbt-verify-fidelity.py unable to verify citations against them
("unverifiable") and leaves kit tags bare ("[H6953]") for future authoring.

Every shipped batch, however, carries verified scholarship in its notes:
    "qoheleth (H6953), from the root for 'assembly' ..."
This script harvests those `translit (H####)` citations across
data/mbt-batches/*.json, votes on the most frequent spelling per number, and
writes a supplement:

    data/mbt-kits/strongs-supplement.json
    {"H6953": {"translit": "qoheleth", "gloss": "", "source": "mbt-batches", "n": 3}, ...}

bin/mbt-build-lexicon.py merges this in AFTER the page parse — page-derived
entries always win; the supplement only fills numbers the pages cannot.
Re-run this after shipping new books, then re-run mbt-build-lexicon.py.

Usage:
  python3 bin/mbt-lexicon-harvest.py
"""
import json, os, glob, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCHES = os.path.join(ROOT, "data", "mbt-batches")
OUT = os.path.join(ROOT, "data", "mbt-kits", "strongs-supplement.json")

# word immediately before "(H####)" / "(G####)" — the citation shape the
# fidelity checker verifies. Allow letters, apostrophes, hyphens.
CITE = re.compile(r"([A-Za-z][A-Za-z'\-]{1,28})\s*\(([HG]\d{1,4})\)")

# English prose words that legitimately precede a bare number in notes
# ("... the KJV margin (H1234)" never occurs, but guard anyway) — anything in
# this set is discarded as a candidate transliteration.
ENGLISH = {
    "the", "and", "margin", "verse", "word", "words", "number", "cf",
    "see", "kjv", "web", "heb", "gr", "in", "of", "a", "an", "chapter",
    "psalm", "prov", "gen", "isa", "matt", "john", "root", "form",
}


def main():
    votes = collections.defaultdict(collections.Counter)
    files = sorted(glob.glob(os.path.join(BATCHES, "*.json")))
    for f in files:
        try:
            d = json.load(open(f))
        except Exception:
            continue
        for v in d.get("verses", {}).values():
            for m in CITE.finditer(v.get("notes", "")):
                translit, num = m.group(1), m.group(2)
                if translit.lower() in ENGLISH:
                    continue
                votes[num][translit.lower()] += 1

    supplement = {}
    for num, counter in sorted(votes.items()):
        translit, n = counter.most_common(1)[0]
        supplement[num] = {
            "translit": translit,
            "gloss": "",
            "source": "mbt-batches",
            "n": n,
        }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(supplement, fh, indent=1, ensure_ascii=False)
    print(f"Harvested {len(supplement)} numbers from {len(files)} batches -> {OUT}")


if __name__ == "__main__":
    main()
