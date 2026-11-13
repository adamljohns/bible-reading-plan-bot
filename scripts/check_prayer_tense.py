#!/usr/bin/env python3
"""check_prayer_tense.py — fail-closed gate: confess in the true tense (Principal 2026-11-13).

The man praying is a justified believer. His former state (guilty, condemned,
dead in sin, no fear of God, enemy, under wrath, mouth stopped) is PAST tense.
This gate scans the 🙏 Prayer section of each watch ONLY and refuses any
present-tense unregenerate confession.

USAGE
  python3 scripts/check_prayer_tense.py 2026-11-14
  python3 scripts/check_prayer_tense.py 2026-11-14:2026-12-31
Exit 0 = clean. Exit 2 = hits. Exit 1 = usage/IO (missing file).
"""
from __future__ import annotations

import re
import sys
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"

TENSE_BANS = [
    ("present_guilty", re.compile(
        r"\bI (?:stand|am) (?:guilty|condemned|under (?:Your )?wrath|dead in)\b", re.I)),
    ("no_fear_of_god", re.compile(r"there is no fear of God before my eyes", re.I)),
    ("present_enemy", re.compile(r"\bI am (?:Your )?enemy\b", re.I)),
    ("mouth_stopped", re.compile(r"\bmy mouth (?:is )?stopped\b", re.I)),
]

WATCH_SPLIT = re.compile(r"\n(?=🌅|🕖|🕚|🕒|🌙)")
PRAYER_BLOCK = re.compile(
    r"🙏[^\n]*\n([\s\S]*?)(?=\n(?:🛡️ Watch Charge|🔑|🕊|⚓|⸻|---|🌅|🕖|🕚|🕒|🌙)|\Z)"
)


def prayer_tense_hits(text: str) -> list[tuple[str, str]]:
    """Return (ban_name, offending line) for every hit inside prayer blocks."""
    out: list[tuple[str, str]] = []
    for sec in WATCH_SPLIT.split(text):
        for pm in PRAYER_BLOCK.finditer(sec):
            for ln in pm.group(1).splitlines():
                for name, rx in TENSE_BANS:
                    if rx.search(ln):
                        out.append((name, ln.strip()))
    return out


def iter_dates(args: list[str]) -> list[str]:
    out: list[str] = []
    for a in args:
        m = re.match(r"(\d{4}-\d{2}-\d{2}):(\d{4}-\d{2}-\d{2})$", a)
        if m:
            cur, end = date.fromisoformat(m.group(1)), date.fromisoformat(m.group(2))
            while cur <= end:
                out.append(cur.isoformat())
                cur += timedelta(days=1)
        elif re.match(r"\d{4}-\d{2}-\d{2}$", a):
            out.append(a)
    return sorted(set(out))


def main() -> int:
    dates = iter_dates(sys.argv[1:])
    if not dates:
        print(__doc__, file=sys.stderr)
        return 1
    bad = missing = 0
    for ds in dates:
        p = READINGS / f"{ds}.md"
        if not p.exists():
            print(f"MISS {ds}")
            missing += 1
            continue
        hits = prayer_tense_hits(p.read_text(encoding="utf-8"))
        if hits:
            bad += 1
            print(f"FAIL {ds} ({len(hits)})")
            for name, ln in hits:
                print(f"  - PRAYER-TENSE:{name}: {ln}")
        else:
            print(f"PASS {ds}")
    if bad:
        print(f"\nREFUSE publish: present-tense unregenerate confession in {bad} day(s)")
        return 2
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
