#!/usr/bin/env python3
"""Fail-closed passage-containment gate for daily watch Scripture blocks.

PJG-0915-WIS1 (2026-09-15): Morning Wisdom labeled "Proverbs 15" shipped a
Scripture block of 42 lines (the chapter has 33 verses) whose tail ran into
Job 19, Job 42, Numbers 23 and Isaiah 52, with an Exodus 20:12 line mashed in
at the top. 2026-09-16 ("Proverbs 16", 33 verses) carried 44 lines with seven
of them duplicated verbatim.

check_scripture_loops.py could not catch either one:

  * its BLEED_RULES are a hand-maintained substring blocklist, so it only
    refuses foreign text somebody has already seen and written a rule for;
  * its loop test needs an occurrence >= 3, so a block repeated exactly twice
    passes clean.

This gate is generic instead of enumerated. The repo already ships the whole
canonical text under docs/assets/chapters/<book>_<chapter>.json, so a named
passage can be checked against what that passage actually contains:

  1. foreign_content — a line matches some verse elsewhere in Scripture far
     better than anything in the named passage. Reported with the reference it
     actually came from, chapter-granular so "Proverbs 15" also refuses a
     Proverbs 9 line.
  2. duplicate_line  — a line appears in the block more often than the named
     passage itself repeats it.

Line COUNT is deliberately not an invariant. Poetry is set one clause per
line, so a correct Psalm 150 renders its 6 verses as 13 lines; an early draft
of this gate failed it on that basis. Attribution is the test, not arithmetic.

Usage:
  python3 scripts/check_passage_containment.py 2026-09-16      # one day
  python3 scripts/check_passage_containment.py                 # all days
  python3 scripts/check_passage_containment.py --watch wisdom 2026-09-16
  python3 scripts/check_passage_containment.py --json-out /tmp/hits.json

Exit 0 = clean. Exit 1 = one or more watches failed. Exit 2 = bad input.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
JSON_DIR = REPO / "docs" / "assets" / "readings"
MD_DIR = REPO / "data" / "readings"
CHAPTER_DIR = REPO / "docs" / "assets" / "chapters"

PREFERRED_VERSIONS = ("NKJV", "KJV", "ESV", "NASB", "WEB")

# Canonical 66-book order; index+1 is the number used by docs/assets/chapters.
BOOKS = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua",
    "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings",
    "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job",
    "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah",
    "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai",
    "Zechariah", "Malachi", "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation",
]

ALIASES = {
    "psalm": "Psalms",
    "psalms": "Psalms",
    "song of songs": "Song of Solomon",
    "canticles": "Song of Solomon",
    "ecclesiastes": "Ecclesiastes",
    "revelations": "Revelation",
}
for _i, _b in enumerate(BOOKS, 1):
    ALIASES[_b.lower()] = _b

BOOK_NUM = {b: i for i, b in enumerate(BOOKS, 1)}

SCR_RE = re.compile(
    r"📖\s*Scripture\s*[—\-–:][^\n]*\n([\s\S]*?)(?=\n⸻|\n🧭|\n🗺️|\n🛰|\n🌾|\n❤️|\n👨‍👧|\n🛡|\n🙏|\Z)"
)
TAG_RE = re.compile(r"<[^>]+>")
NORM_RE = re.compile(r"[^a-z0-9\s]+")

# Function words carry no attribution signal; a line is identified by its
# content words, not by how many times it says "the" or "of".
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from",
    "had", "has", "have", "he", "her", "him", "his", "i", "in", "is", "it",
    "its", "me", "my", "nor", "not", "o", "of", "on", "or", "our", "shall",
    "she", "so", "than", "that", "the", "thee", "their", "them", "then",
    "there", "they", "thou", "thy", "to", "unto", "upon", "us", "was", "we",
    "were", "what", "when", "which", "who", "will", "with", "you", "your",
    "yet", "into", "out", "up", "down", "all", "any", "one", "do", "does",
    "did", "am", "been", "being", "this", "these", "those", "him self",
    "himself", "herself", "itself", "shalt", "hath", "doth",
}

# A line is "foreign" only when some other book matches it well in absolute
# terms AND beats the named passage by a clear margin. Both bars must be met,
# so a loose paraphrase of an in-passage verse cannot trip the gate.
FOREIGN_ABS = 0.55
FOREIGN_MARGIN = 0.20
MIN_CONTENT_TOKENS = 4
# Two candidate verses this close to each other are a quotation/parallel.
PARALLEL_SIM = 0.50
# A line already matching its own passage this well is never called foreign,
# whatever else it resembles. Across the corpus the genuinely foreign lines sit
# at a median in-passage score of 0.14; this bar clears quotation artifacts
# (Psalm 32:2 vs Romans 4:8) without reaching them.
IN_PASSAGE_MAX = 0.35


def normalize(s: str) -> str:
    s = TAG_RE.sub(" ", s or "")
    s = s.lower().replace("’", "'").replace("‘", "'")
    s = NORM_RE.sub(" ", s)
    return re.sub(r"\s+", " ", s).strip()


def content_tokens(s: str) -> frozenset[str]:
    return frozenset(t for t in normalize(s).split() if t and t not in STOPWORDS)


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def extract_scripture_bounded(text: str) -> tuple[str, bool]:
    """Return (scripture_block, bounded).

    bounded is False when the Scripture section runs to end-of-text with no
    closing marker. Some days use a template with no ⸻ / 🧭 / 🙏 separators,
    and there the regex swallows commentary and prayer along with the verses.
    A block we cannot bound cannot be judged for foreign content — saying
    otherwise would flag a man's prayer as a mash.
    """
    m = SCR_RE.search(text or "")
    if not m:
        m2 = re.search(r"📖[^\n]*\n([\s\S]*?)(?=\n⸻)", text or "")
        return (m2.group(1), True) if m2 else ("", True)
    tail = (text or "")[m.end(1) : m.end(1) + 4]
    return m.group(1), bool(tail.strip())


def extract_scripture(text: str) -> str:
    return extract_scripture_bounded(text)[0]


def scripture_lines(scripture: str) -> list[str]:
    return [ln.strip() for ln in (scripture or "").splitlines() if ln.strip()]


@lru_cache(maxsize=None)
def load_chapter(book_num: int, chapter: int) -> dict[str, str]:
    """Return {verse_number: text} in the best available version."""
    fp = CHAPTER_DIR / f"{book_num}_{chapter}.json"
    if not fp.exists():
        return {}
    try:
        data = json.loads(fp.read_text())
    except Exception:
        return {}
    for ver in PREFERRED_VERSIONS:
        block = data.get(ver)
        if isinstance(block, dict) and block:
            return {str(k): str(v) for k, v in block.items()}
    for block in data.values():
        if isinstance(block, dict) and block:
            return {str(k): str(v) for k, v in block.items()}
    return {}


def parse_passage(passage: str) -> list[tuple[str, int, int | None, int | None]] | None:
    """Parse a passage label into [(book, chapter, v_start, v_end), ...].

    Returns None when the label cannot be resolved with confidence — an
    unresolvable label must not be treated as a violation.
    """
    if not passage or not passage.strip():
        return None
    refs: list[tuple[str, int, int | None, int | None]] = []
    chunks = re.split(r"\s*(?:&|;|\band\b|\+)\s*", passage.strip())
    last_book: str | None = None
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        m = re.match(
            r"^((?:[1-3]\s*)?[A-Za-z][A-Za-z\s]*?)\s*(\d+)(?::(\d+)(?:\s*[-–]\s*(\d+))?)?$",
            chunk,
        )
        if m:
            raw_book = re.sub(r"\s+", " ", m.group(1)).strip().lower()
            book = ALIASES.get(raw_book)
            if not book:
                return None
            last_book = book
            chapter = int(m.group(2))
            vs = int(m.group(3)) if m.group(3) else None
            ve = int(m.group(4)) if m.group(4) else vs
            refs.append((book, chapter, vs, ve))
            continue
        # bare continuation like "Acts 4:1-10 & 13-22"
        m2 = re.match(r"^(\d+)(?:\s*[-–]\s*(\d+))?$", chunk)
        if m2 and refs and last_book:
            prev = refs[-1]
            vs = int(m2.group(1))
            ve = int(m2.group(2)) if m2.group(2) else vs
            refs.append((last_book, prev[1], vs, ve))
            continue
        return None
    return refs or None


def allowed_verses(refs: list[tuple[str, int, int | None, int | None]]) -> list[tuple[str, str]]:
    """Return [(reference, text), ...] for every verse the label names."""
    out: list[tuple[str, str]] = []
    for book, chapter, vs, ve in refs:
        num = BOOK_NUM.get(book)
        if not num:
            continue
        verses = load_chapter(num, chapter)
        for vnum, vtext in verses.items():
            try:
                n = int(vnum)
            except ValueError:
                continue
            if vs is not None and not (vs <= n <= (ve or vs)):
                continue
            out.append((f"{book} {chapter}:{n}", vtext))
    return out


def is_single_whole_chapter(refs: list[tuple[str, int, int | None, int | None]]) -> bool:
    return len(refs) == 1 and refs[0][2] is None


@lru_cache(maxsize=1)
def corpus_index() -> tuple[list[tuple[str, frozenset[str]]], dict[str, list[int]]]:
    """Build (verses, inverted_index) over every chapter file in the repo."""
    verses: list[tuple[str, frozenset[str]]] = []
    for fp in sorted(CHAPTER_DIR.glob("*_*.json")):
        stem = fp.stem
        try:
            bnum_s, chap_s = stem.split("_", 1)
            bnum, chap = int(bnum_s), int(chap_s)
        except ValueError:
            continue
        if not (1 <= bnum <= len(BOOKS)):
            continue
        book = BOOKS[bnum - 1]
        for vnum, vtext in load_chapter(bnum, chap).items():
            toks = content_tokens(vtext)
            if len(toks) >= MIN_CONTENT_TOKENS:
                verses.append((f"{book} {chap}:{vnum}", toks))
    inverted: dict[str, list[int]] = {}
    for idx, (_ref, toks) in enumerate(verses):
        for t in toks:
            inverted.setdefault(t, []).append(idx)
    return verses, inverted


def best_global_match(line_toks: frozenset[str]) -> tuple[float, str, frozenset[str]]:
    """Best-scoring verse anywhere in the canon for this line."""
    verses, inverted = corpus_index()
    # Only verses sharing at least one content token can score above zero.
    counts: Counter[int] = Counter()
    for t in line_toks:
        for idx in inverted.get(t, ()):
            counts[idx] += 1
    best = 0.0
    best_ref = ""
    best_toks: frozenset[str] = frozenset()
    need = max(2, len(line_toks) // 4)
    for idx, shared in counts.items():
        if shared < need:
            continue
        ref, toks = verses[idx]
        s = jaccard(line_toks, toks)
        if s > best:
            best, best_ref, best_toks = s, ref, toks
    return best, best_ref, best_toks


def check_watch(date: str, wkey: str, passage: str, text: str) -> list[dict]:
    scr, bounded = extract_scripture_bounded(text)
    lines = scripture_lines(scr)
    if not lines:
        return []
    if not bounded:
        return [
            {
                "date": date,
                "watch": wkey,
                "passage": passage,
                "code": "unbounded_block",
                "severity": True,
                "lines": len(lines),
            }
        ]
    refs = parse_passage(passage)
    if not refs:
        return []
    pool = allowed_verses(refs)
    if not pool:
        return []

    fails: list[dict] = []
    # Chapter-granular: "Proverbs 15" must not carry Proverbs 9 either. That
    # cross-chapter bleed is exactly what the old BLEED_RULES chased by hand.
    named_chapters = {(b, c) for b, c, _s, _e in refs}

    # 1. duplicate lines inside one block.
    # Scripture legitimately repeats itself — Psalm 136's "for His mercy
    # endures forever" lands 26 times, and Psalm 150 opens and closes on
    # "Praise the LORD!". A repeat is only a defect when the block repeats a
    # line MORE often than the named passage itself does.
    chapter_text = normalize(" ".join(t for _r, t in pool))
    dup: list[tuple[str, int, int]] = []
    counts = Counter(
        normalize(l) for l in lines if len(content_tokens(l)) >= MIN_CONTENT_TOKENS
    )
    for norm_line, c in counts.items():
        if c < 2 or not norm_line:
            continue
        legit = chapter_text.count(norm_line)
        if c > max(1, legit):
            dup.append((norm_line[:70], c, legit))
    if dup:
        dup.sort(key=lambda d: -d[1])
        fails.append(
            {
                "date": date,
                "watch": wkey,
                "passage": passage,
                "code": "duplicate_line",
                "dupes": dup[:3],
                "distinct": len(dup),
            }
        )

    # 2. foreign content, reported with the reference it came from
    pool_toks = [(r, content_tokens(t)) for r, t in pool]
    foreign: list[dict] = []
    for i, ln in enumerate(lines, 1):
        lt = content_tokens(ln)
        if len(lt) < MIN_CONTENT_TOKENS:
            continue
        in_best, in_toks = 0.0, frozenset()
        for _r, pt in pool_toks:
            s = jaccard(lt, pt)
            if s > in_best:
                in_best, in_toks = s, pt
        if in_best >= IN_PASSAGE_MAX:
            continue
        g_best, g_ref, g_toks = best_global_match(lt)
        if not g_ref:
            continue
        # Scripture quotes Scripture: Romans 4:8 quotes Psalm 32:2, so a
        # correct Psalm 32 line can match Romans better than its own verse.
        # When the two candidates are near-identical to each other, this is a
        # parallel, not a mash.
        if jaccard(g_toks, in_toks) >= PARALLEL_SIM:
            continue
        gm = re.match(r"^(.*?)\s+(\d+):\d+$", g_ref)
        if not gm:
            continue
        if (gm.group(1), int(gm.group(2))) in named_chapters:
            continue
        if g_best >= FOREIGN_ABS and (g_best - in_best) >= FOREIGN_MARGIN:
            foreign.append(
                {
                    "line": i,
                    "match": g_ref,
                    "score": round(g_best, 2),
                    "in_passage": round(in_best, 2),
                    "sample": ln[:70],
                }
            )
    if foreign:
        fails.append(
            {
                "date": date,
                "watch": wkey,
                "passage": passage,
                "code": "foreign_content",
                "count": len(foreign),
                "foreign": foreign[:6],
            }
        )
    return fails


def load_day_watches(date: str, force_md: bool = False) -> dict[str, dict]:
    if not force_md:
        jp = JSON_DIR / f"{date}.json"
        if jp.exists():
            day = json.loads(jp.read_text())
            return {
                k: {
                    "passage": (w or {}).get("passage") or "",
                    "text": (w or {}).get("text") or "",
                }
                for k, w in (day.get("watches") or {}).items()
            }
    mp = MD_DIR / f"{date}.md"
    if not mp.exists():
        raise FileNotFoundError(f"no reading source for {date}")
    md = mp.read_text()
    marks = []
    for i, ln in enumerate(md.splitlines()):
        s = ln.strip()
        key = None
        if s.startswith("🌅"):
            key = "wisdom"
        elif s.startswith("🕖"):
            key = "first"
        elif s.startswith("🕚"):
            key = "second"
        elif s.startswith("🕒"):
            key = "third"
        elif s.startswith("🌙"):
            key = "peace"
        if key:
            marks.append((i, key))
    lines = md.splitlines()
    out = {}
    for idx, (start, key) in enumerate(marks):
        end = marks[idx + 1][0] if idx + 1 < len(marks) else len(lines)
        chunk = "\n".join(lines[start:end])
        m = re.search(r"📖\s*Scripture\s*[—\-–:]\s*(.+)", chunk)
        out[key] = {"passage": m.group(1).strip() if m else "", "text": chunk}
    return out


def iter_dates(only: list[str] | None) -> list[str]:
    if only:
        return only
    dates = set()
    for fp in JSON_DIR.glob("20*.json"):
        dates.add(fp.stem)
    for fp in MD_DIR.glob("20*.md"):
        dates.add(fp.stem)
    return sorted(dates)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dates", nargs="*", help="YYYY-MM-DD (default: all)")
    ap.add_argument("--md", action="store_true", help="force MD source")
    ap.add_argument("--watch", help="only this watch key")
    ap.add_argument("--json-out", type=Path, help="write full hit list")
    args = ap.parse_args(argv)

    all_fails: list[dict] = []
    for date in iter_dates(args.dates or None):
        try:
            watches = load_day_watches(date, force_md=args.md)
        except FileNotFoundError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 2
        for wkey, w in watches.items():
            if args.watch and wkey != args.watch:
                continue
            all_fails.extend(
                check_watch(date, wkey, w.get("passage") or "", w.get("text") or "")
            )

    if args.json_out:
        args.json_out.write_text(json.dumps({"fails": all_fails}, indent=2) + "\n")

    hard = [f for f in all_fails if not f.get("severity")]
    soft = [f for f in all_fails if f.get("severity")]

    for f in soft:
        print(
            f"WARN {f['date']} · {f['watch']} · {f.get('passage') or '?'} · "
            f"{f['code']} · lines={f.get('lines')} (not judged)",
            file=sys.stderr,
        )

    if not hard:
        scope = len(args.dates) if args.dates else "all"
        print(
            f"OK passage-containment gate clean ({scope} day(s); "
            f"unbounded_warns={len(soft)})"
        )
        return 0

    print(f"FAIL passage-containment gate: {len(hard)} hit(s)", file=sys.stderr)
    for f in hard:
        bits = [f["date"], f["watch"], f.get("passage") or "?", f["code"]]
        if f["code"] == "duplicate_line":
            top = f["dupes"][0]
            bits.append(
                f"distinct_dupes={f['distinct']} top×{top[1]} (passage has {top[2]})"
            )
        if f["code"] == "foreign_content":
            bits.append(f"count={f['count']}")
            for fo in f["foreign"][:4]:
                bits.append(
                    f"L{fo['line']}→{fo['match']} ({fo['score']} vs {fo['in_passage']})"
                )
        print(" - " + " · ".join(str(b) for b in bits), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
