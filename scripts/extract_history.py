#!/usr/bin/env python3
"""
extract_history.py — Pull every "🦅 This Day in American History" event from the
Citizen's Stand (third) watch across the corpus, for fact verification.

Each event line looks like:   • 1789 — First U.S. presidential election begins...
The block runs from the 🦅 header to the next section marker (⚓/⛏/🙏/separator).

Writes data/history-events.json: [{date, md_date_label, year, event}].
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"
OUT = REPO / "data" / "history-events.json"

HDR_RE = re.compile(r"🦅\s*This Day in American History\s*[—\-–]?\s*(.*)$")
STOP_RE = re.compile(r"^\s*(⚓|⛏|🙏|🌙|🦅|⸻|#|📖|🛡|🧭|🗺|🛰|❤|👨|✝)")
YEAR_RE = re.compile(r"\b(1[6-9]\d\d|20[0-2]\d)\b")


def extract(md):
    """Capture every history CLAIM after the header, in BOTH formats:
    bulleted '• 1789 — ...' and prose 'On July 4, 1776, ...' / 'In 1831, ...'.
    Each non-blank, non-stop line/paragraph is one claim."""
    out = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        m = HDR_RE.search(lines[i])
        if not m:
            i += 1
            continue
        label = m.group(1).strip()
        j = i + 1
        while j < len(lines):
            ln = lines[j].strip()
            if ln == "":
                j += 1
                continue
            if STOP_RE.match(ln):
                break
            claim = re.sub(r"^•\s*", "", ln)
            ym = YEAR_RE.search(claim)
            out.append((label, ym.group(1) if ym else None, claim))
            j += 1
        i = j
    return out


def main():
    events = []
    for p in sorted(READINGS.glob("2026-*.md")):
        ds = p.stem
        for label, year, ev in extract(p.read_text()):
            events.append({"date": ds, "label": label, "year": year, "event": ev})
    OUT.write_text(json.dumps(events, ensure_ascii=False, indent=1))
    days = len({e["date"] for e in events})
    print(f"Extracted {len(events)} history events across {days} days -> {OUT.name}")
    # quick distribution
    from collections import Counter
    per = Counter(e["date"] for e in events)
    print(f"  events/day: min={min(per.values())} max={max(per.values())} "
          f"avg={sum(per.values())/len(per):.1f}")


if __name__ == "__main__":
    main()
