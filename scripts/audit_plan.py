#!/usr/bin/env python3
"""Audit the daily reading plan for copy-paste / data errors.

Checks every day's per-day JSON for: full 365-day date coverage (no gaps/dupes),
5 watches per day, valid passage references (real book + in-range chapter),
duplicate passages, and passage-vs-rendered-text agreement (does the watch text
actually quote the book it claims). Reports findings; changes nothing.

  python3 scripts/audit_plan.py
"""
import glob, json, re
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DAYS = REPO / "docs" / "assets" / "readings"

# Standard chapter counts for all 66 books.
CHAP = {
    "genesis": 50, "exodus": 40, "leviticus": 27, "numbers": 36, "deuteronomy": 34,
    "joshua": 24, "judges": 21, "ruth": 4, "1 samuel": 31, "2 samuel": 24, "1 kings": 22,
    "2 kings": 25, "1 chronicles": 29, "2 chronicles": 36, "ezra": 10, "nehemiah": 13,
    "esther": 10, "job": 42, "psalms": 150, "proverbs": 31, "ecclesiastes": 12,
    "song of solomon": 8, "isaiah": 66, "jeremiah": 52, "lamentations": 5, "ezekiel": 48,
    "daniel": 12, "hosea": 14, "joel": 3, "amos": 9, "obadiah": 1, "jonah": 4, "micah": 7,
    "nahum": 3, "habakkuk": 3, "zephaniah": 3, "haggai": 2, "zechariah": 14, "malachi": 4,
    "matthew": 28, "mark": 16, "luke": 24, "john": 21, "acts": 28, "romans": 16,
    "1 corinthians": 16, "2 corinthians": 13, "galatians": 6, "ephesians": 6,
    "philippians": 4, "colossians": 4, "1 thessalonians": 5, "2 thessalonians": 3,
    "1 timothy": 6, "2 timothy": 4, "titus": 3, "philemon": 1, "hebrews": 13, "james": 5,
    "1 peter": 5, "2 peter": 3, "1 john": 5, "2 john": 1, "3 john": 1, "jude": 1, "revelation": 22,
}
ALIAS = {
    "psalm": "psalms", "song of songs": "song of solomon", "canticles": "song of solomon",
    "qoheleth": "ecclesiastes", "revelations": "revelation", "1 sam": "1 samuel", "2 sam": "2 samuel",
    "1 kgs": "1 kings", "2 kgs": "2 kings", "1 chron": "1 chronicles", "2 chron": "2 chronicles",
    "1 cor": "1 corinthians", "2 cor": "2 corinthians", "1 thess": "1 thessalonians",
    "2 thess": "2 thessalonians", "1 tim": "1 timothy", "2 tim": "2 timothy", "phil": "philippians",
    "philem": "philemon", "deut": "deuteronomy", "gen": "genesis", "exod": "exodus", "matt": "matthew",
}
BOOK_RE = re.compile(r"^\s*((?:[123]\s+)?[A-Za-z][A-Za-z ]*?)\s+(\d+)(?::([\d]+))?(?:\s*[-–]\s*(?:(\d+):)?(\d+))?\s*$")


def norm(b):
    b = re.sub(r"\s+", " ", b.strip().lower())
    return ALIAS.get(b, b)


def parse_ref(ref):
    """Return list of (book, chapter, problem|None). Tolerates &/; joins, en-dashes,
    spaced punctuation, '(annotations)', version suffixes, and book-carry across ; / &."""
    raw = ref
    ref = re.sub(r"\([^)]*\)", "", ref)                       # drop "(blended listening render)"
    ref = ref.replace("–", "-").replace("—", "-")             # normalize dashes
    ref = re.sub(r"\s*:\s*", ":", ref)                        # "38 : 1" -> "38:1"
    ref = re.sub(r"\s*-\s*", "-", ref)
    ref = re.sub(r"\s+(ESV|NKJV|KJV|NASB|NLT|NIV|AMP|CSB17?|WEB|NET|MSG|NRSVCE)\b", "", ref, flags=re.I)
    out, last_book = [], None
    for piece in re.split(r"\s*[;&]\s*", ref.strip()):
        piece = piece.strip().strip(",")
        if not piece:
            continue
        m = re.match(r"^((?:[123]\s+)?[A-Za-z][A-Za-z ]*?)\s+(\d+)", piece)
        if m:
            book, ch, last_book = norm(m.group(1)), int(m.group(2)), norm(m.group(1))
            if CHAP.get(book) == 1:                           # single-chapter book: the number is a verse
                ch = 1
        elif norm(piece) in CHAP and CHAP[norm(piece)] == 1:  # name-only single-chapter (Obadiah, Jude, 2 John)
            book, ch, last_book = norm(piece), 1, norm(piece)
        elif last_book and re.match(r"^\d", piece):           # "31:1-9" carries the previous book
            book = last_book
            ch = 1 if CHAP.get(last_book) == 1 else int(re.match(r"^(\d+)", piece).group(1))
        else:
            out.append((piece, None, f"unparseable piece in '{raw}'"))
            continue
        if book not in CHAP:
            out.append((piece, ch, f"unknown book '{book}' in '{raw}'"))
        elif not (1 <= ch <= CHAP[book]):
            out.append((book, ch, f"{book.title()} has {CHAP[book]} chapters, ref says {ch}  ('{raw}')"))
        else:
            out.append((book, ch, None))
    return out


def main():
    files = {Path(f).stem: f for f in glob.glob(str(DAYS / "2026-*.json"))}
    issues = {"missing_dates": [], "bad_ref": [], "watch_count": [], "dup_passage": [], "text_mismatch": []}

    # date coverage
    d, end = date(2026, 1, 1), date(2026, 12, 31)
    present = set(files)
    while d <= end:
        if d.isoformat() not in present:
            issues["missing_dates"].append(d.isoformat())
        d += timedelta(days=1)

    seen = {}
    for stem in sorted(files):
        day = json.load(open(files[stem], encoding="utf-8"))
        w = day.get("watches", {})
        if len(w) != 5:
            issues["watch_count"].append(f"{stem}: {len(w)} watches ({list(w)})")
        for key, wd in w.items():
            ref = (wd.get("passage") or "").strip()
            text = wd.get("text") or ""
            if not ref:
                issues["bad_ref"].append(f"{stem}/{key}: empty passage")
                continue
            for book, ch, prob in parse_ref(ref):
                if prob:
                    issues["bad_ref"].append(f"{stem}/{key}: '{ref}' -> {prob}")
                else:
                    if key in ("first", "second", "third"):   # main reading only (wisdom/peace rotate by design)
                        seen.setdefault((book, ch), []).append(f"{stem}/{key}")
                    # text-vs-passage: does the rendered text mention the book name?
                    disp = book.title().replace("Psalms", "Psalm")
                    if disp.split()[-1].lower() not in text.lower() and book not in text.lower():
                        issues["text_mismatch"].append(f"{stem}/{key}: text never names '{disp}' (ref {ref})")
    for (book, ch), where in seen.items():
        if len(where) > 1:
            issues["dup_passage"].append(f"{book.title()} {ch}: {len(where)}x -> {', '.join(where[:6])}")

    print("=" * 70)
    print("READING PLAN AUDIT")
    print("=" * 70)
    print(f"days found: {len(files)} / 365")
    for k, v in issues.items():
        print(f"\n### {k.upper()} — {len(v)}")
        for line in v[:25]:
            print("  " + line)
        if len(v) > 25:
            print(f"  ... +{len(v) - 25} more")


if __name__ == "__main__":
    main()
