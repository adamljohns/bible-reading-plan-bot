#!/usr/bin/env python3
"""
regen_broken_watches.py — Regenerate every NULL / skeleton / truncated watch
via the (improved) local generator, splice it back into the day's markdown by
reconstructing the day in canonical format, and rebuild that day's JSON.

Reuses generate_reading_local.py's machinery so the new watches inherit the
divine-name / fresh-closer / passage-specific-application rules.

Run (from repo root, LM Studio serving on :1235):
  python3 scripts/regen_broken_watches.py            # all broken watches
  python3 scripts/regen_broken_watches.py --date 2026-01-18
  python3 scripts/regen_broken_watches.py --limit 3  # first 3 dates (smoke)
"""
import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"
sys.path.insert(0, str(REPO / "scripts"))

import generate_reading_local as G
from build_reading_index import split_watches

WATCH_ORDER = ["wisdom", "first", "second", "third", "peace"]
WATCH_BY_KEY = {w["key"]: w for w in G.WATCHES}
SEP = "⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻"
MONTHS = G.MONTHS
MODEL = "qwen3.6-35b-a3b"
PORT = "1235"


def preamble_for(ds):
    dt = date.fromisoformat(ds)
    return (f"MOOP's 2026 Daily Bible Readings\n\n"
            f"{dt.strftime('%A')}, {MONTHS[dt.month]} {dt.day}, 2026")


def regen_one(ds, wk, passage):
    """Generate a single clean watch (with up to 3 retries). Returns text|None."""
    w = WATCH_BY_KEY[wk]
    dt = date.fromisoformat(ds)
    month, daynum = MONTHS[dt.month], dt.day
    for attempt in range(1, 4):
        try:
            raw = G.call_llm(G.build_watch_messages(w, passage, month, daynum), MODEL, PORT)
        except Exception as e:
            print(f"    [{wk}] attempt {attempt} llm error: {e}", flush=True)
            continue
        body = G.clean_watch(raw, w["header"])
        body = G.normalize_prayer_header(body, w["prayer"])
        if G.watch_valid(body, w):
            return body
        print(f"    [{wk}] attempt {attempt} invalid, retrying", flush=True)
    return None


def process_date(ds, broken_for_date):
    md_path = READINGS / f"{ds}.md"
    existing = split_watches(md_path.read_text()) if md_path.exists() else {}
    # Resolve passage per broken watch
    new_watches = dict(existing)
    for b in broken_for_date:
        wk = b["watch"]
        passage = b["passage"]
        if not passage:
            print(f"  {ds} [{wk}] SKIP — no passage", flush=True)
            return False
        print(f"  {ds} [{wk}] regenerating ({passage}) ...", flush=True)
        text = regen_one(ds, wk, passage)
        if not text:
            print(f"  {ds} [{wk}] FAILED after retries — leaving as-is", flush=True)
            return False
        new_watches[wk] = text
        print(f"  {ds} [{wk}] ✓ {len(text):,} chars", flush=True)

    # Reconstruct the day in canonical format (preamble + SEP-joined watches)
    sections = [preamble_for(ds)]
    for k in WATCH_ORDER:
        if k in new_watches and new_watches[k] and new_watches[k].strip():
            sections.append(new_watches[k].strip())
    out = ("\n\n" + SEP + "\n\n").join(sections) + "\n"
    md_path.write_text(out)
    # Rebuild this day's JSON
    subprocess.run([sys.executable, "scripts/build_reading_index.py",
                    "regen", "--date", ds], cwd=REPO, capture_output=True)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    # Fresh inventory of broken watches
    subprocess.run([sys.executable, "scripts/find_broken_watches.py"],
                   cwd=REPO, capture_output=True)
    broken = json.loads((REPO / "data" / "broken-watches.json").read_text())

    by_date = {}
    for b in broken:
        by_date.setdefault(b["date"], []).append(b)

    dates = sorted(by_date)
    if args.date:
        dates = [args.date] if args.date in by_date else []
    if args.limit:
        dates = dates[:args.limit]

    print(f"Regenerating broken watches across {len(dates)} date(s) "
          f"({sum(len(by_date[d]) for d in dates)} watches)\n", flush=True)
    ok = 0
    for ds in dates:
        if process_date(ds, by_date[ds]):
            ok += 1
    print(f"\nDone: {ok}/{len(dates)} dates fully regenerated.", flush=True)


if __name__ == "__main__":
    main()
