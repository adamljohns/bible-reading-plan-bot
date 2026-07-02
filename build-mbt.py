#!/usr/bin/env python3
"""
build-mbt.py -- Compile authored MOOP Bible Translation (MBT) batches into the
served, agent-fetchable index, and run fidelity + copyright-originality checks.

INPUT  : data/mbt-batches/<book>_<chapter>.json   (hand-authored content)
OUTPUT : docs/assets/mbt/<book>_<chapter>.json     (clean per-chapter, agent fetch)
         docs/assets/mbt/mbt-bible.json            (flat B_C_V -> text, BTE drop-in)
         docs/assets/mbt/manifest.json             (inventory + version + license)
         mbt-progress.json                          (running count toward 1189)

CHECKS : verse-count parity vs public-domain KJV (from verse-cache.json),
         divine-name discipline (no 'Yahweh'/'Jehovah' leakage),
         ORIGINALITY -- similarity of each MBT verse vs the COPYRIGHTED NKJV/ESV
         columns, purely to PROVE the MBT does not reproduce them. Those columns
         are read here only for this negative check; they never author text.

Copyright-safe: authored solely from public-domain KJV(1769)+Strong's and WEB.
"""
import json, re, sys, glob, os
from collections import defaultdict

REPO = os.path.dirname(os.path.abspath(__file__))
BATCH_DIR = os.path.join(REPO, "data", "mbt-batches")
OUT_DIR   = os.path.join(REPO, "docs", "assets", "mbt")
CACHE     = os.path.join(REPO, "docs", "assets", "verse-cache.json")
PROGRESS  = os.path.join(REPO, "mbt-progress.json")
TOTAL_CHAPTERS = 1189
LICENSE = ("MOOP Bible Translation (MBT) (c) U.S.M.C. Ministries. Derived solely "
           "from public-domain sources (KJV 1769 + Strong's, World English Bible) "
           "and public-domain lexica. Free to quote and reproduce in full.")
# Every copyrighted column in verse-cache.json — the near-verbatim gate checks ALL
# of them (these columns are read ONLY for this negative check; they never author).
COPYRIGHTED_COLS = ["NKJV", "ESV", "NASB", "NLT", "CSB17", "NIV", "AMP", "MSG",
                    "NET", "NRSVCE"]

_word = re.compile(r"[a-z]+")
STOP = set("the a an of in on and or but to for with his my your their its it he she "
           "they you i we him them me us is are was were be been being will shall would "
           "do does did not no when that which who whom this these those as at by from "
           "into up out over under so then than before after all any if".split())
def clean(s):
    s = (s or "").lower()
    s = re.sub(r"<s>\d+</s>", " ", s)   # strip Strong's tag AND its number
    s = re.sub(r"<[^>]+>", " ", s)       # strip any remaining markup
    return s
def emdash(s):
    """Authoring uses ' -- ' as an ASCII-safe em-dash placeholder; emit a real
    em-dash so verses read right on screen AND in narration (Piper reads the flat
    file). Applied to every served string field (text/amp/notes/chapterNote).
    Handles mid-clause ' -- ' and a trailing/enjambment ' --' at string end."""
    if not isinstance(s, str):
        return s
    s = s.replace(" -- ", " — ")
    if s.endswith(" --"):
        s = s[:-3] + " —"
    return s
def toks(s):
    return _word.findall(clean(s))
def bigrams(t):
    return {f"{t[i]} {t[i+1]}" for i in range(len(t)-1)}
def content(bg):
    w1, w2 = bg.split(); return not (w1 in STOP and w2 in STOP)

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("Loading verse-cache (for parity + originality check only)...")
    cache = json.load(open(CACHE))

    batch_files = sorted(glob.glob(os.path.join(BATCH_DIR, "*.json")))
    if not batch_files:
        print("No batch files found in", BATCH_DIR); sys.exit(1)

    flat = {}                # B_C_V -> text  (drop-in for moop-translation.json)
    manifest_chapters = []   # inventory entries
    errors = []              # hard failures
    warnings = []            # soft flags for review
    sim_report = []          # (key, jacc_nkjv, jacc_esv, run_nkjv, run_esv)

    for bf in batch_files:
        b = json.load(open(bf))
        book, ch = b["book"], b["chapter"]
        verses = b["verses"]

        # ---- parity vs public-domain KJV in the cache
        kjv_keys = [k for k in cache
                    if k.startswith(f"{book}_{ch}_") and cache[k].get("KJV")]
        kjv_vnums = sorted(int(k.split("_")[2]) for k in kjv_keys)
        mbt_vnums = sorted(int(v) for v in verses)
        if kjv_vnums and mbt_vnums != kjv_vnums:
            missing = sorted(set(kjv_vnums) - set(mbt_vnums))
            extra   = sorted(set(mbt_vnums) - set(kjv_vnums))
            if missing: errors.append(f"{book}_{ch}: missing verses {missing}")
            if extra:   warnings.append(f"{book}_{ch}: extra verses not in KJV {extra}")

        for vnum, obj in verses.items():
            key = f"{book}_{ch}_{vnum}"
            text = obj.get("text", "")
            amp  = obj.get("amp", "")
            flat[key] = emdash(text)

            # ---- divine-name discipline (hard fail on leakage; notes included --
            #      the translit "YHWH" is fine, the vocalized forms are not)
            blob = (text + " " + amp + " " + obj.get("notes", "")).lower()
            if "yahweh" in blob or "jehovah" in blob:
                errors.append(f"{key}: divine-name leak ('Yahweh'/'Jehovah' present)")

            # ---- length sanity vs KJV
            kjv = clean(cache.get(key, {}).get("KJV", ""))
            if kjv.strip():
                ratio = len(text) / max(len(kjv), 1)
                if ratio > 2.6:
                    warnings.append(f"{key}: text {ratio:.1f}x KJV length (review)")

            # ---- ORIGINALITY (near-verbatim only): copyright only requires that
            #      a verse not be word-for-word a modern copyrighted translation.
            #      We flag a verse only if it is near-identical (>=85% bigram
            #      overlap) to ANY copyrighted column in the cache. Sharing
            #      ordinary phrasing is fine. (Was NKJV/ESV-only until 2026-07-01;
            #      that gate missed 39 verses that matched NASB/NIV/AMP/CSB/NRSVCE.)
            mb = bigrams(toks(text))
            def _jac(col):
                ob = bigrams(toks(cache.get(key, {}).get(col, "")))
                return len(mb & ob) / len(mb | ob) if (mb and ob) else 0.0
            overlaps = {col: _jac(col) for col in COPYRIGHTED_COLS}
            src = max(overlaps, key=overlaps.get)
            verbatim = overlaps[src]
            sim_report.append((key, verbatim, src))
            if verbatim >= 0.85:
                warnings.append(f"{key}: near-verbatim to {src} ({verbatim*100:.0f}% overlap) "
                                f"-- change wording so it is not word-for-word")

        # ---- write served per-chapter file (clean, agent-facing); normalize em-dashes
        def _norm_verse(o):
            return {k: (emdash(v) if k in ("text", "amp", "notes") else v)
                    for k, v in o.items()}
        out = {
            "book": book, "bookName": b.get("bookName"), "chapter": ch,
            "version": b.get("version"), "license": LICENSE,
            "sources": b.get("sources"),
            "chapterNote": emdash(b.get("chapterNote")),
            "verses": {v: _norm_verse(verses[v]) for v in sorted(verses, key=int)},
        }
        out = {k: v for k, v in out.items() if v is not None}
        with open(os.path.join(OUT_DIR, f"{book}_{ch}.json"), "w") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        manifest_chapters.append({
            "book": book, "bookName": b.get("bookName"), "chapter": ch,
            "verses": len(verses), "version": b.get("version"),
            "url": f"assets/mbt/{book}_{ch}.json",
        })

    # ---- write flat file + manifest + progress
    with open(os.path.join(OUT_DIR, "mbt-bible.json"), "w") as f:
        json.dump(flat, f, ensure_ascii=False)
    books_done = sorted({c["book"] for c in manifest_chapters})
    manifest = {
        "translation": "MOOP Bible Translation (MBT)",
        "license": LICENSE,
        "fetch_url_pattern": "https://usmcmin.org/assets/mbt/<bookId>_<chapter>.json",
        "fields": {"text": "default clean verse (style B)",
                   "amp": "amplified/study form (style C)",
                   "notes": "lexical/Strong's anchor"},
        "chapters_present": len(manifest_chapters),
        "books_present": books_done,
        "chapters": sorted(manifest_chapters, key=lambda c: (c["book"], c["chapter"])),
    }
    with open(os.path.join(OUT_DIR, "manifest.json"), "w") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    progress = {
        "chapters_done": len(manifest_chapters),
        "total_chapters": TOTAL_CHAPTERS,
        "percent": round(100*len(manifest_chapters)/TOTAL_CHAPTERS, 2),
        "books_present": books_done,
        "verses_done": len(flat),
    }
    with open(PROGRESS, "w") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

    # ---- report
    print(f"\nBuilt {len(manifest_chapters)} chapter(s), {len(flat)} verses -> {OUT_DIR}")
    print(f"Progress: {progress['chapters_done']}/{TOTAL_CHAPTERS} chapters ({progress['percent']}%)")
    sim_report.sort(key=lambda r: r[1], reverse=True)
    n = len(sim_report)
    flagged = sum(1 for r in sim_report if r[1] >= 0.85)
    print(f"\nORIGINALITY (near-verbatim check vs {len(COPYRIGHTED_COLS)} copyrighted versions):")
    print("  policy: a verse is fine unless it is word-for-word a modern version.")
    print(f"  verses near-verbatim (>=85% overlap): {flagged}/{n}")
    print("  closest verses to a copyrighted version:")
    for key, verbatim, src in sim_report[:5]:
        print(f"    {key:12s} max {verbatim*100:3.0f}%  (vs {src})")
    print(f"\nERRORS: {len(errors)}")
    for e in errors: print("  X", e)
    print(f"WARNINGS (review, not blocking): {len(warnings)}")
    for w in warnings: print("  !", w)
    print("\nDivine-name discipline:", "PASS (no Yahweh/Jehovah leakage)"
          if not any('divine-name' in e for e in errors) else "FAIL")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
