#!/usr/bin/env python3
"""mbt-verify-fidelity.py [bookId ...]

Deterministic (zero-token) Hebrew/Greek fidelity check for authored MBT batches.
For every "translit (H####)" / "translit (G####)" citation in a verse's notes,
verify the transliteration matches the verified lexicon lookup for that Strong's
number. Catches the dominant authoring error: a translit that belongs to a
DIFFERENT Strong's number than the one cited (e.g. "yashar (H3476)" when H3476 is
yosher). Also flags same-translit / different-number collisions within a chapter.

Romanization is normalized (lowercase; drop diacritics/apostrophes/hyphens; kh->ch,
final-h and w/v folded) so ordinary spelling variants are NOT flagged — only genuine
word mismatches. Numbers absent from the lookup are reported as 'unverifiable', not
errors.

Usage:
  python3 bin/mbt-verify-fidelity.py            # all book-20 (Proverbs) batches
  python3 bin/mbt-verify-fidelity.py 20 8 57    # specific books
"""
import json, os, re, sys, glob, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOOKUP = json.load(open(os.path.join(ROOT, "data", "mbt-kits", "strongs-lookup.json")))

CITE = re.compile(r"([A-Za-z’'`ʾʿ-]{2,})\s*\((H\d{1,5}|G\d{1,5})\)")
# Words that are prose, not transliterations (the regex sometimes grabs the word
# just before a parenthetical Strong's number, e.g. "the LORD (YHWH, H3068)").
ENGLISH = set("the lord god he him his she her they them it a an of to and or but for "
              "verb noun root form word name here same both each all who whom which "
              "cf see also her his its one two three sing".split())

def norm(s):
    # strip ALL diacritics via NFKD decomposition, then keep ascii letters only
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z]", "", s)      # drop apostrophes/ayin/aleph marks, hyphens, spaces
    s = s.replace("kh", "ch")         # romanization: kh == ch (khakham == chakham)
    s = s.replace("w", "v")           # waw as w or v
    s = re.sub(r"h$", "", s)          # trailing mater lectionis
    s = re.sub(r"(.)\1+", r"\1", s)   # collapse doubled letters (dagesh forte)
    return s

def related(a, b):
    """True if two normalized translits are plausibly the SAME lemma (variant/inflection)."""
    if not a or not b:
        return True
    if a == b:
        return True
    short, long = sorted((a, b), key=len)
    # inflection/participle: shorter stem sits inside the longer, or they share a
    # 3-letter consonantal root prefix (Hebrew triliteral)
    if len(short) >= 3 and short in long:
        return True
    if len(a) >= 3 and len(b) >= 3 and a[:3] == b[:3]:
        return True
    # near-identical (single-letter edit) — tolerate one romanization slip
    if abs(len(a) - len(b)) <= 1 and sum(x != y for x, y in zip(a, b)) <= 1:
        return True
    return False

STRONG = re.compile(r"\[([HG]\d{1,5})")   # kit tags: word[H#### ...]  ->  H####

def kit_numbers(book, ch):
    """Set of Strong's numbers tagged in each verse of the kit: {verse: {H####,...}}."""
    kf = os.path.join(ROOT, "data", "mbt-kits", f"{book}_{ch}.kit.json")
    out = {}
    if not os.path.exists(kf):
        return out
    k = json.load(open(kf))
    for v, e in k.get("verses", {}).items():
        out[v] = set(STRONG.findall(e.get("kjv_strongs", "")))
    return out

def check_book(book):
    hard, soft, unverifiable = [], [], 0
    for bf in sorted(glob.glob(os.path.join(ROOT, "data", "mbt-batches", f"{book}_*.json"))):
        d = json.load(open(bf))
        ch = d["chapter"]
        kn = kit_numbers(book, ch)
        for v, o in d.get("verses", {}).items():
            notes = o.get("notes", "") or ""
            versekit = kn.get(v, set())
            for m in CITE.finditer(notes):
                translit, num = m.group(1), m.group(2)
                if translit.lower() in ENGLISH:
                    continue
                # cross-reference context: if a book/chapter:verse or "cf." marker
                # sits just before the citation, the number legitimately points at
                # ANOTHER verse (e.g. "Proverbs 16:31 ... ateret (H5850)") -- not an error.
                pre = notes[max(0, m.start() - 45):m.start()]
                is_xref = bool(re.search(r"(cf\.|Prov|Ps|Psalm|Gen|Isa|Deut|\d+:\d+)", pre))
                nt = norm(translit)
                if not nt:
                    continue
                entry = LOOKUP.get(num)
                lem = norm(entry["translit"]) if (entry and entry.get("translit")) else None
                translit_ok = (lem is None) or related(nt, lem)
                # HARD signal: the cited number is NOT tagged anywhere in this verse's
                # kit AND the translit doesn't match the lexicon lemma for that number.
                # That is the 'lets (H3917)' class — a wrong Strong's number.
                # only a MEANINGFUL "not tagged" when we actually have this verse's
                # kit tags to check against (else we cannot verify — treat as soft).
                have_kit = v in kn and bool(versekit)
                if have_kit and num not in versekit and not translit_ok and not is_xref:
                    hard.append(f"  {book}:{ch}:{v}  notes '{translit} ({num})' -- {num} is NOT "
                                f"tagged in this verse; lexicon {num} = "
                                f"'{entry['translit'] if entry else '?'}' "
                                f"({(entry or {}).get('gloss','')[:35]})")
                elif not translit_ok:
                    soft.append(f"  {book}:{ch}:{v}  '{translit} ({num})' vs lexicon "
                                f"'{entry['translit']}' (likely inflection/variant)")
                if not entry or not entry.get("translit"):
                    unverifiable += 1
    return hard, soft, unverifiable

def main():
    books = [int(x) for x in sys.argv[1:]] or [20]
    show_soft = "--soft" in sys.argv
    total = 0
    for book in books:
        if not str(book).isdigit():
            continue
        hard, soft, unver = check_book(book)
        print(f"=== book {book}: {len(hard)} HARD (likely-wrong number), "
              f"{len(soft)} soft (inflection/variant), {unver} unverifiable ===")
        for f in hard:
            print("X", f)
        if show_soft:
            for f in soft:
                print(" ~", f)
        total += len(hard)
    print(f"\nTOTAL HARD FLAGS: {total}")
    sys.exit(1 if total else 0)

if __name__ == "__main__":
    main()
