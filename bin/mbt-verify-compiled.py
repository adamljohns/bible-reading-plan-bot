#!/usr/bin/env python3
"""mbt-verify-compiled.py — drift guard between MBT source batches and served files.

The batches under data/mbt-batches/ are the ONLY source of truth for the MBT.
This check recomputes what build-mbt.py would serve and diffs it against what
is actually in docs/assets/mbt/, catching the Proverbs-15 class of bug
(2026-08-27): a compiled per-chapter file hand-edited on main — with a process
marker leaked into the served notes — while the batch and the flat file said
otherwise.

Checks, per batch:
  1. docs/assets/mbt/<book>_<chapter>.json exists and its verses match the
     batch (text/amp/notes after em-dash normalization), chapterNote included.
  2. mbt-bible.json (the flat file bible.html reads) agrees with the batch
     text for every verse.
  3. manifest.json lists the chapter.

Exit 0 clean, exit 1 with a drift report. Zero tokens, zero network.

Usage:
  python3 bin/mbt-verify-compiled.py            # all batches
  python3 bin/mbt-verify-compiled.py 20         # one book
"""
import json, os, glob, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCHES = os.path.join(ROOT, "data", "mbt-batches")
SERVED = os.path.join(ROOT, "docs", "assets", "mbt")


def emdash(s):
    if not isinstance(s, str):
        return s
    s = s.replace(" -- ", " — ")
    if s.endswith(" --"):
        s = s[:-3] + " —"
    return s


def main():
    only_books = {int(a) for a in sys.argv[1:] if a.isdigit()}
    flat = json.load(open(os.path.join(SERVED, "mbt-bible.json")))
    manifest = json.load(open(os.path.join(SERVED, "manifest.json")))
    man_chapters = set()
    for ch in manifest.get("chapters", []):
        if isinstance(ch, dict):
            man_chapters.add((int(ch.get("book", 0)), int(ch.get("chapter", 0))))
        elif isinstance(ch, str):
            m = re.match(r"(\d+)_(\d+)$", ch)
            if m:
                man_chapters.add((int(m.group(1)), int(m.group(2))))

    drift = []
    checked = 0
    for bf in sorted(glob.glob(os.path.join(BATCHES, "*.json"))):
        b = json.load(open(bf))
        book, ch = int(b["book"]), int(b["chapter"])
        if only_books and book not in only_books:
            continue
        checked += 1
        served_path = os.path.join(SERVED, f"{book}_{ch}.json")
        if not os.path.exists(served_path):
            drift.append(f"{book}_{ch}: compiled file MISSING")
            continue
        served = json.load(open(served_path))

        want_note = emdash(b.get("chapterNote", ""))
        got_note = served.get("chapterNote", "")
        if want_note and want_note != got_note:
            drift.append(f"{book}_{ch}: chapterNote drift")

        sv = served.get("verses", {})
        for vnum, obj in b["verses"].items():
            for field in ("text", "amp", "notes"):
                want = emdash(obj.get(field, ""))
                got = (sv.get(vnum) or {}).get(field, "")
                if want != got:
                    drift.append(f"{book}_{ch}_{vnum}.{field}: per-chapter drift")
            fkey = f"{book}_{ch}_{vnum}"
            if flat.get(fkey) != emdash(obj.get("text", "")):
                drift.append(f"{fkey}: flat mbt-bible.json drift")

        if man_chapters and (book, ch) not in man_chapters:
            drift.append(f"{book}_{ch}: absent from manifest.json")

    if drift:
        print(f"DRIFT: {len(drift)} finding(s) across {checked} batch(es):")
        for d in drift[:50]:
            print("  ", d)
        if len(drift) > 50:
            print(f"   ... and {len(drift) - 50} more")
        print("\nFix: edit the BATCH (source of truth), run build-mbt.py, ship the")
        print("recompiled outputs. Never edit docs/assets/mbt/* by hand.")
        sys.exit(1)
    print(f"CLEAN: {checked} batch(es) — per-chapter, flat, and manifest all match the batches.")


if __name__ == "__main__":
    main()
