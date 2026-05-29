"""Integrate the MBT pilot's `text` field into moop-translation.json
so the BTE serves the higher-quality authored prose.

The pilot's `amp` (amplified) and `notes` (lexical) fields stay in the
standalone mbt.html working-manuscript view — only the clean `text` is
promoted into the main runtime layer.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"
PILOT_DIR = ROOT / "docs" / "assets" / "mbt"
MANIFEST = PILOT_DIR / "manifest.json"

def main():
    with open(MOOP_PATH) as f:
        moop = json.load(f)

    with open(MANIFEST) as f:
        man = json.load(f)

    n_promoted = 0
    n_chapters = 0
    diffs = []
    for chapter_meta in man["chapters"]:
        book = chapter_meta["book"]
        chapter = chapter_meta["chapter"]
        pilot_path = PILOT_DIR / f"{book}_{chapter}.json"
        if not pilot_path.exists():
            print(f"  SKIP {book}_{chapter}: pilot file missing")
            continue
        with open(pilot_path) as f:
            pilot = json.load(f)
        verses = pilot.get("verses", {})
        n_chapters += 1
        for v_str, vobj in verses.items():
            text = vobj.get("text", "").strip()
            if not text:
                continue
            key = f"{book}_{chapter}_{v_str}"
            existing = moop.get(key, "")
            if existing != text:
                diffs.append((key, existing[:60], text[:60]))
            moop[key] = text
            n_promoted += 1

    with open(MOOP_PATH, "w") as f:
        json.dump(moop, f, ensure_ascii=False)
    print(f"\nPromoted {n_promoted} verses from {n_chapters} pilot chapters.")
    print(f"Replaced {len(diffs)} existing verses with higher-quality text.")
    if diffs[:5]:
        print(f"\nSample replacements:")
        for key, before, after in diffs[:5]:
            print(f"  {key}")
            print(f"    BEFORE: {before}...")
            print(f"    AFTER:  {after}...")

if __name__ == "__main__":
    main()
