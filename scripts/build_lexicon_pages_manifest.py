#!/usr/bin/env python3
"""
Scan docs/lexicon/ for all H#.html and G#.html files (Hebrew + Greek Strong's
lexicon pages), and write docs/assets/lexicon-pages.json as a simple manifest
that bible.html loads on startup to know which Strong's IDs link to our own
lexicon vs fall back to external sites.

Run from repo root:
    python3 scripts/build_lexicon_pages_manifest.py
"""
import json
import re
from pathlib import Path
from datetime import date

REPO = Path(__file__).resolve().parent.parent
LEX_DIR = REPO / "docs/lexicon"
OUT = REPO / "docs/assets/lexicon-pages.json"

STRONGS_FILE_PATTERN = re.compile(r"^([HG]\d+)\.html$")


def sortkey(s: str):
    """Sort H1 < H2 < ... < H8674 < G1 < ... < G5624 (alphabetical prefix, numeric body)."""
    return (s[0], int(s[1:]))


def main():
    if not LEX_DIR.exists():
        raise SystemExit(f"ERROR: {LEX_DIR} not found")

    strongs_ids = []
    for f in LEX_DIR.iterdir():
        m = STRONGS_FILE_PATTERN.match(f.name)
        if m:
            strongs_ids.append(m.group(1))

    strongs_ids.sort(key=sortkey)
    hebrew = [s for s in strongs_ids if s.startswith("H")]
    greek = [s for s in strongs_ids if s.startswith("G")]

    manifest = {
        "generated": date.today().isoformat(),
        "schema": "list of Strong's IDs that have local lexicon/<id>.html pages",
        "count": len(strongs_ids),
        "hebrew_count": len(hebrew),
        "greek_count": len(greek),
        "pages": strongs_ids,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2) + "\n")

    size_kb = OUT.stat().st_size / 1024
    print(f"Wrote {OUT}  ({size_kb:.1f} KB)")
    print(f"  Hebrew (H#):  {len(hebrew):,}")
    print(f"  Greek  (G#):  {len(greek):,}")
    print(f"  Total:        {len(strongs_ids):,}")
    print(f"  First 3: {strongs_ids[:3]}")
    print(f"  Last 3:  {strongs_ids[-3:]}")


if __name__ == "__main__":
    main()
