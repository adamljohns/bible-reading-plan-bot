#!/usr/bin/env python3
"""mbt-build-lexicon.py

Parse all local Strong's lexicon pages (docs/lexicon/<id>.html) and emit a
compact lookup JSON at data/mbt-kits/strongs-lookup.json.

  {"G1198": {"translit": "desmios", "gloss": "prisoner, one in chains"}, ...}

Run once before your first kit build, and again after any lexicon update.
The output is gitignored (data/mbt-kits/) — regenerable from this script.

Usage:
  python3 bin/mbt-build-lexicon.py
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX   = os.path.join(ROOT, "docs", "assets", "lexicon-pages.json")
LEX_DIR = os.path.join(ROOT, "docs", "lexicon")
OUT     = os.path.join(ROOT, "data", "mbt-kits", "strongs-lookup.json")

# "G1198 — desmios (prisoner) | USMC..." or "H2617 — chesed (Lovingkindness) | ..."
RE_TITLE = re.compile(r"<title>[A-Za-z]\d+\s*[—–-]+\s*(.+?)\s*\(([^)]+)\)")
RE_GLOSS = re.compile(r'class=["\']gloss["\'][^>]*>([^<]+)')


def parse_page(path):
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None

    translit = ""
    gloss    = ""

    m = RE_TITLE.search(text)
    if m:
        translit = m.group(1).strip()
        gloss    = m.group(2).strip()

    # class="gloss" is richer (comma-separated synonyms); prefer it when present
    m2 = RE_GLOSS.search(text)
    if m2:
        rich = m2.group(1).strip()
        if rich:
            gloss = rich

    if not translit and not gloss:
        return None
    return {"translit": translit, "gloss": gloss}


def main():
    if not os.path.exists(INDEX):
        sys.exit(f"lexicon index not found: {INDEX}")

    idx = json.load(open(INDEX))
    ids = idx.get("pages", [])
    total = len(ids)
    print(f"Parsing {total} lexicon pages …")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    lookup  = {}
    missing = 0

    for i, sid in enumerate(ids, 1):
        path  = os.path.join(LEX_DIR, f"{sid}.html")
        entry = parse_page(path)
        if entry:
            lookup[sid] = entry
        else:
            missing += 1
        if i % 1000 == 0:
            print(f"  {i}/{total} …")

    json.dump(lookup, open(OUT, "w"), ensure_ascii=False, separators=(",", ":"))
    print(f"\nDone: {len(lookup)} entries built, {missing} missing/sparse")
    print(f"  -> {OUT}")


if __name__ == "__main__":
    main()
