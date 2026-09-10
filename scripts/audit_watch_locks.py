#!/usr/bin/env python3
"""audit_watch_locks.py — deterministic gate for the two First/Second Watch locks.

Why this exists
---------------
Both locks were already written into scripts/generate_reading_local.py as prompt
instructions to the local model (PJG-0826-HAPPY1 at HAPPY_WEEKDAY, and the
FULFILLED-father voice rules). A prompt is not enforcement: the model complies
most of the time and silently does not the rest of the time, and nothing catches
it. The BAN-LIST gate in pj-deliver-watch.sh only refuses naval vocabulary, so a
wrong HAPPY letter or a vocative aimed at a child ships clean.

This audit is the missing mechanical check. It reads the authored markdown and
fails closed.

LOCK 1 — PJG-0826-HAPPY1 (First Watch, 🕖)
    The H.A.P.P.Y. letter is the WEEKDAY, never the passage theme:
    Mon Honest · Tue Honors · Wed Abiding · Thu Adoring
    Fri Protecting · Sat Providing · Sun Yields

LOCK 2 — PJG-0909-FAT2 / FAT1 (Second Watch, 🕚)
    In the Father's Charge, "you/your" is the FATHER. The children are spoken of
    in the third person. A vocative aimed at a child ("Gideon, at nineteen,
    you...") turns the watch into a letter the son overhears, which is a
    different product. The prayer is I/me to God ABOUT them.

USAGE
    python3 scripts/audit_watch_locks.py                      # today -> +365d
    python3 scripts/audit_watch_locks.py --range 2026-09-10 2026-12-31
    python3 scripts/audit_watch_locks.py --range ... --json report.json
    python3 scripts/audit_watch_locks.py --lock happy         # one lock only

Exit 0 when clean, 1 when any violation is found.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"

# LOCK 1 — weekday letter. Monday == 0.
HAPPY_WEEKDAY = {
    0: "Honest",
    1: "Honors",
    2: "Abiding",
    3: "Adoring",
    4: "Protecting",
    5: "Providing",
    6: "Yields",
}

SPLIT = re.compile(r"\n(?=🌅|🕖|🕚|🕒|🌙)")
FIRST = "🕖"
SECOND = "🕚"

# The trait is carried on the wife-reflection heading of the First Watch.
HAPPY_HEAD = re.compile(
    r"Reflection for Your Wife[^\n]*?H\.?A\.?P\.?P\.?Y\.?[^\n]*?—\s*([A-Za-z]+)"
)

CHILDREN = r"(?:Gideon|Boaz|Shiloh)"

# LOCK 2 violations. Each pattern describes a vocative aimed AT a child.
VOCATIVE_PATTERNS = [
    # "Gideon, you ..." / "Gideon, at nineteen, you ..." / "Boaz, my son, you ..."
    (
        "name-comma-you",
        re.compile(rf"\b{CHILDREN}\b\s*,(?:[^.\n]{{0,60}}?,)?\s*you\b", re.I),
    ),
    # "Dear Gideon"
    ("dear-name", re.compile(rf"\bDear\s+{CHILDREN}\b", re.I)),
    # "Gideon, my son" / "Shiloh, my little one"
    ("name-comma-my", re.compile(rf"\b{CHILDREN}\b\s*,\s*my\b", re.I)),
    # direct imperative to the child
    ("listen-closely", re.compile(r"\blisten closely\b", re.I)),
]


def iter_dates(start: date, end: date):
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)


def section(text: str, glyph: str) -> str | None:
    for part in SPLIT.split(text):
        if part.startswith(glyph):
            return part
    return None


def check_happy(ds: str, d: date, text: str) -> dict | None:
    sec = section(text, FIRST)
    if not sec:
        return None
    m = HAPPY_HEAD.search(sec)
    want = HAPPY_WEEKDAY[d.weekday()]
    got = m.group(1) if m else None
    # "Yields" is sometimes authored as "Yielding"; treat as the same letter.
    norm = {"Yielding": "Yields"}.get(got or "", got)
    if norm == want:
        return None
    return {
        "date": ds,
        "weekday": d.strftime("%a"),
        "lock": "happy",
        "want": want,
        "got": got,
    }


def check_father(ds: str, text: str) -> list[dict]:
    sec = section(text, SECOND)
    if not sec:
        return []
    out = []
    for name, pat in VOCATIVE_PATTERNS:
        for m in pat.finditer(sec):
            out.append(
                {
                    "date": ds,
                    "lock": "father",
                    "pattern": name,
                    "quote": " ".join(
                        sec[max(0, m.start() - 40) : m.end() + 40].split()
                    ),
                }
            )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--range", nargs=2, metavar=("START", "END"))
    ap.add_argument("--lock", choices=["happy", "father", "all"], default="all")
    ap.add_argument("--json", metavar="PATH")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if args.range:
        start = date.fromisoformat(args.range[0])
        end = date.fromisoformat(args.range[1])
    else:
        start = date.today()
        end = start + timedelta(days=365)

    happy: list[dict] = []
    father: list[dict] = []
    checked = 0

    for d in iter_dates(start, end):
        ds = d.isoformat()
        p = READINGS / f"{ds}.md"
        if not p.exists():
            continue
        checked += 1
        text = p.read_text(encoding="utf-8")
        if args.lock in ("happy", "all"):
            hit = check_happy(ds, d, text)
            if hit:
                happy.append(hit)
        if args.lock in ("father", "all"):
            father.extend(check_father(ds, text))

    report = {
        "range": [start.isoformat(), end.isoformat()],
        "dates_checked": checked,
        "happy_violations": happy,
        "father_violations": father,
        "ok": not happy and not father,
    }

    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=1, ensure_ascii=False))

    if not args.quiet:
        print(f"dates checked: {checked}")
        print(f"LOCK 1 HAPPY weekday   — violations: {len(happy)}")
        for h in happy[:20]:
            print(f"    {h['date']} {h['weekday']}  got={h['got']!r} want={h['want']!r}")
        if len(happy) > 20:
            print(f"    ... and {len(happy) - 20} more")
        dates_f = sorted({f["date"] for f in father})
        print(
            f"LOCK 2 father vocative — violations: {len(father)} "
            f"across {len(dates_f)} dates"
        )
        for f in father[:20]:
            print(f"    {f['date']} [{f['pattern']}] …{f['quote']}…")
        if len(father) > 20:
            print(f"    ... and {len(father) - 20} more")
        print("RESULT:", "PASS" if report["ok"] else "FAIL")

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
