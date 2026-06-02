#!/usr/bin/env python3
"""
find_broken_watches.py — Inventory every watch that is missing or corrupt:
  NULL   — watch has no text at all (genuine content gap)
  LEAK   — watch text contains prompt-skeleton instruction leakage
  SHORT  — watch text is suspiciously short (likely truncated/partial)

For each, resolve the intended passage (from the watch's own "📖 Scripture —"
line if present, else from plan-data.js) so it can be regenerated.

Writes data/broken-watches.json and prints a summary.
"""
import json
import re
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"
PLAN = REPO / "docs" / "assets" / "plan-data.js"
OUT = REPO / "data" / "broken-watches.json"

import sys
sys.path.insert(0, str(REPO / "scripts"))
from build_reading_index import split_watches  # robust splitter

WATCH_ORDER = ["wisdom", "first", "second", "third", "peace"]
SCRIP_RE = re.compile(r"📖\s*Scripture\s*[—\-–:]\s*(.+)")
LEAK_MARKERS = [
    "A one-sentence intro", "Render only this reference", "A line with a single",
    "A line exactly:", "2-4 sentences placing", "2-4 paragraphs of reflection",
    "four '• ' bulleted", "do NOT import text from any other", "{TRAIT}",
    "{same trait}", "EXACT SECTION ORDER", "do NOT echo this instruction",
]


def load_plan_passages():
    text = PLAN.read_text()
    out = {}
    for m in re.finditer(r'"(\d{4}-\d{2}-\d{2})"\s*:\s*(\{[^}]*\})', text):
        try:
            out[m.group(1)] = json.loads(m.group(2))
        except json.JSONDecodeError:
            pass
    return out


def passage_of(wtext, ds, wk, plan):
    if wtext:
        m = SCRIP_RE.search(wtext)
        if m:
            cand = m.group(1).strip()
            # reject a leaked "Scripture — <ref> ONLY..." tail
            cand = re.split(r"\s+ONLY\b", cand)[0].strip()
            if cand and "import text" not in cand:
                return cand
    p = plan.get(ds, {})
    return p.get(wk)


def main():
    plan = load_plan_passages()
    broken = []
    cur, end = date(2026, 1, 1), date(2026, 12, 31)
    while cur <= end:
        ds = cur.isoformat(); cur += timedelta(days=1)
        p = READINGS / f"{ds}.md"
        if not p.exists():
            continue
        watches = split_watches(p.read_text())
        for wk in WATCH_ORDER:
            wtext = watches.get(wk)
            kind = None
            if not wtext or not wtext.strip():
                kind = "NULL"
            elif any(mk in wtext for mk in LEAK_MARKERS):
                kind = "LEAK"
            elif len(wtext) < 900:   # full watch is ~3-6k chars; <900 is truncated
                kind = "SHORT"
            if kind:
                broken.append({
                    "date": ds, "watch": wk, "kind": kind,
                    "passage": passage_of(wtext, ds, wk, plan),
                    "len": len(wtext or ""),
                })
    OUT.write_text(json.dumps(broken, ensure_ascii=False, indent=1))
    from collections import Counter
    by_kind = Counter(b["kind"] for b in broken)
    no_passage = [b for b in broken if not b["passage"]]
    print(f"Broken watches: {len(broken)}  ({dict(by_kind)})")
    print(f"  without a resolvable passage: {len(no_passage)}")
    for b in broken:
        pp = b["passage"] or "??? NO PASSAGE"
        print(f"  {b['date']} [{b['watch']:6}] {b['kind']:5} len={b['len']:5}  {pp}")


if __name__ == "__main__":
    main()
