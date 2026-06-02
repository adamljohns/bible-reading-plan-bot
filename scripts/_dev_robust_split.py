#!/usr/bin/env python3
"""DEV: develop + validate a robust watch splitter that handles BOTH the modern
emoji-header format and the legacy PDF-converted formats. Goal: every 2026 day
slices into exactly 5 watches (wisdom/first/second/third/peace) with substantial
text, with no mis-slicing. Once proven, port robust_split() into
build_reading_index.py and build_reading_page_from_md.py.

Run: python3 scripts/_dev_robust_split.py
"""
import re
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"

HEADER_EMOJI = "📅🌅☀🌞🌄🕖🕚🕒🌙⏰🧭"
# hour-prefix -> watch key (06xx Morning, 07xx Husband, 11xx Father, 15xx Citizen, 21xx Peace)
TIME_KEY = {"06": "wisdom", "07": "first", "11": "second", "15": "third", "21": "peace"}
TIME_RE = re.compile(r"(?<!\d)(06|07|11|15|21)[0-5]\d(?!\d)")
TITLE_PATTERNS = [
    ("wisdom", re.compile(r"morning wisdom", re.I)),
    ("first",  re.compile(r"first watch|husband'?s post|h\.?a\.?²?p\.?p\.?y", re.I)),
    ("second", re.compile(r"second watch|father'?s charge", re.I)),
    ("third",  re.compile(r"third watch|citizen'?s (stand|post)", re.I)),
    ("peace",  re.compile(r"evening peace", re.I)),
]
DATETIME_LINE_RE = re.compile(r"^[A-Z][a-z]+day,?\s+\w+\s+\d+.*[—–-]\s*(?:06|07|11|15|21)[0-5]\d")


def classify_line(ln):
    """Return watch key if this line is a watch header, else None.

    Robust across modern + legacy formats. The strongest signal is a watch
    TIME CODE (06/07/11/15/21xx) on a header-like line; the fallback is a
    title phrase on an emoji-led line. We deliberately do NOT trigger on a
    bare title keyword in body prose (e.g. a reflection that says 'father')."""
    s = ln.strip()
    if not s:
        return None
    # leading char is an emoji / non-word, non-markdown-punct glyph
    has_emoji = bool(re.match(r"^[^\w\s#>*_\-—–=.\"'(\[]", s))
    is_datetime = bool(DATETIME_LINE_RE.match(s))
    title_key = None
    for key, pat in TITLE_PATTERNS:
        if pat.search(s):
            title_key = key
            break
    mt = TIME_RE.search(s)
    # Header if a time code appears on a header-like line (emoji / title / date line)...
    if mt and (has_emoji or title_key or is_datetime):
        return TIME_KEY.get(mt.group(1)) or title_key
    # ...or an emoji-led line carrying an unambiguous watch title.
    if has_emoji and title_key:
        return title_key
    return None


def robust_split(md_text):
    lines = md_text.splitlines()
    marks = []
    seen = set()
    for i, ln in enumerate(lines):
        key = classify_line(ln)
        if key and key not in seen:
            marks.append((i, key))
            seen.add(key)
    marks.sort()
    out = {}
    for idx, (start, key) in enumerate(marks):
        end = marks[idx + 1][0] if idx + 1 < len(marks) else len(lines)
        body = "\n".join(lines[start:end]).rstrip()
        body = re.sub(r"\n⸻{3,}\s*$", "", body).rstrip()
        out[key] = body
    return out


def main():
    cur, end = date(2026, 1, 1), date(2026, 12, 31)
    days = []
    while cur <= end:
        days.append(cur.isoformat()); cur += timedelta(days=1)

    bad = []
    thin = []
    total = 0
    for ds in days:
        p = READINGS / f"{ds}.md"
        if not p.exists():
            continue
        total += 1
        w = robust_split(p.read_text())
        if set(w.keys()) != {"wisdom", "first", "second", "third", "peace"}:
            bad.append((ds, sorted(w.keys())))
        else:
            for k, t in w.items():
                # flag suspiciously short recovered text (< 200 chars likely mis-slice)
                if len(t) < 200:
                    thin.append((ds, k, len(t)))

    print(f"Days: {total}")
    print(f"Days NOT yielding exactly 5 watches: {len(bad)}")
    for ds, ks in bad[:20]:
        print(f"  {ds}: {ks}")
    print(f"\nThin watches (<200 chars, possible mis-slice): {len(thin)}")
    for ds, k, n in thin[:20]:
        print(f"  {ds} [{k}]: {n} chars")


if __name__ == "__main__":
    main()
