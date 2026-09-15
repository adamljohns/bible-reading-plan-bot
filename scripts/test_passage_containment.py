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

# Detection is pinned with SYNTHETIC fixtures, not live days. A corpus day
# used as a must-flag case stops flagging the moment it is repaired, which is
# the whole point of the gate — an earlier version of this suite pinned
# 2026-09-18 and broke in the same commit that fixed that day.
# (name, passage, scripture_block, why)
MUST_FLAG_FIXTURES = [
    (
        "prose_run_hides_matthew",
        "Proverbs 18",
        # One long prose line, the 2026-09-18 shape. Per-line attribution
        # cannot see inside it; sentence-level attribution can.
        "A fool takes pleasure in evil conduct, but a man of understanding "
        "delights in wisdom. The name of the LORD is a strong tower; the "
        "righteous run to it and are safe. A man who isolates himself seeks "
        "his own desire and rages against all wise counsel. He who divorces "
        "his wife causes her to commit adultery, and whoever marries a "
        "divorced woman commits adultery.",
        "Matthew 5:32 hidden inside a Proverbs 18 prose run",
    ),
    (
        "foreign_verse_own_line",
        "Proverbs 27",
        "Do not boast about tomorrow, for you do not know what a day may bring "
        "forth.\nTrust in the LORD with all your heart, and lean not on your "
        "own understanding.\nIron sharpens iron, so a man sharpens the "
        "countenance of his friend.",
        "Proverbs 3:5 verbatim inside Proverbs 27",
    ),
    (
        "duplicated_line",
        "Proverbs 16",
        "The preparations of the heart belong to man, But the answer of the "
        "tongue is from the LORD.\nCommit your works to the LORD, And your "
        "thoughts will be established.\nCommit your works to the LORD, And "
        "your thoughts will be established.",
        "a line repeated more often than Proverbs 16 repeats it",
    ),
]

# (date, watch, why) — corpus days the gate MUST flag. Only days that will
# never be repaired belong here; 2026-09-15 is frozen by PJ (already delivered,
# no rebake), so it stays mashed permanently.
MUST_FLAG = [
    ("2026-09-15", "wisdom", "Prov 15 tail runs into Job/Numbers/Isaiah"),
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


def fixture_text(passage: str, block: str) -> str:
    """Wrap a raw block in the watch text shape the gate parses."""
    return f"🌅 0600 Morning Wisdom\n\n📖 Scripture — {passage}\n{block}\n\n⸻\n\n🧭 Context Summary\nfixture\n"


def main() -> int:
    failures = 0
    for name, passage, block, why in MUST_FLAG_FIXTURES:
        got = [
            f
            for f in check_watch("fixture", "wisdom", passage, fixture_text(passage, block))
            if not f.get("severity")
        ]
        if got:
            print(f"ok   flags [{name}] — {[f['code'] for f in got]}")
        else:
            print(f"FAIL missed [{name}] — {why}", file=sys.stderr)
            failures += 1
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
    total = len(MUST_FLAG_FIXTURES) + len(MUST_FLAG) + len(MUST_PASS)
    if failures:
        print(f"\n{failures}/{total} FAILED", file=sys.stderr)
        return 1
    print(f"\nall {total} passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
