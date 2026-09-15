#!/usr/bin/env python3
"""Regression suite for the passage-containment gate.

The gate refuses audio bakes, so a false positive costs a man his Scripture
that morning and a false negative ships a mashed quote. Both directions are
pinned here against real days in the corpus. Every MUST_PASS case below is a
false positive an earlier draft of the gate actually produced.

Run: python3 scripts/test_passage_containment.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from check_passage_containment import check_watch  # noqa: E402

JSON_DIR = REPO / "docs" / "assets" / "readings"

# (date, watch, why) — the gate MUST flag these.
MUST_FLAG = [
    ("2026-09-15", "wisdom", "Prov 15 tail runs into Job/Numbers/Isaiah"),
    ("2026-09-18", "wisdom", "Matthew 5:32 divorce line inside a Proverbs 18 prose run"),
    ("2026-09-27", "wisdom", "Proverbs 3:5 verbatim inside Proverbs 27"),
    ("2026-12-22", "peace", "Psalm 113:4 verbatim inside Psalm 146"),
]

# (date, watch, why) — the gate MUST stay silent. Each was a real false
# positive during development.
MUST_PASS = [
    ("2026-12-31", "wisdom", "correct Psalm 150: 6 verses set as 13 poetic half-lines"),
    ("2026-12-31", "third", "correct Psalm 121 set as half-lines"),
    ("2026-02-04", "peace", "Psalm 32 flagged because Romans 4:8 quotes it"),
    ("2026-12-21", "wisdom", "Rev 21:6 clause matched shorter Rev 22:13 after sentence split"),
    ("2026-12-26", "second", "Psalm 135:14 sits wholly inside Deuteronomy 32:36"),
    ("2026-07-09", "first", "'Thus says the Lord GOD' formula shared with Jeremiah"),
    ("2026-09-16", "wisdom", "repaired to canonical Proverbs 16"),
    ("2026-09-17", "wisdom", "repaired to canonical Proverbs 17"),
    ("2026-09-18", "peace", "repaired to Isaiah 49:1-7, range honored"),
]


def hits(date: str, watch: str) -> list[dict]:
    day = json.loads((JSON_DIR / f"{date}.json").read_text())
    w = (day.get("watches") or {}).get(watch) or {}
    return [
        f
        for f in check_watch(date, watch, w.get("passage") or "", w.get("text") or "")
        if not f.get("severity")
    ]


def main() -> int:
    failures = 0
    for date, watch, why in MUST_FLAG:
        got = hits(date, watch)
        if got:
            print(f"ok   flags {date} {watch} — {[f['code'] for f in got]}")
        else:
            print(f"FAIL missed {date} {watch} — {why}", file=sys.stderr)
            failures += 1
    for date, watch, why in MUST_PASS:
        got = hits(date, watch)
        if not got:
            print(f"ok   clean {date} {watch}")
        else:
            print(
                f"FAIL false positive {date} {watch} — {why} — got "
                f"{[f['code'] for f in got]}",
                file=sys.stderr,
            )
            failures += 1
    total = len(MUST_FLAG) + len(MUST_PASS)
    if failures:
        print(f"\n{failures}/{total} FAILED", file=sys.stderr)
        return 1
    print(f"\nall {total} passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
