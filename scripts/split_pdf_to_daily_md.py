#!/usr/bin/env python3
"""
Split Adam's Jan/Feb PDF daily reading docs into per-day .md files.

Source PDFs (already extracted to /tmp/bible_jan_clean.txt, /tmp/bible_feb_clean.txt):
  /Users/moop_bot_pro/Documents/BU2TB-Archive/TRANSFER_PACKAGE_FRESH_2026-03-04/workspace-memory/
    bible_plan_january.pdf
    bible_plan_february.pdf

Output: /Users/moop_bot_pro/bible-reading-plan-bot/data/readings/<YYYY-MM-DD>.md

Strategy:
  - Find the FIRST occurrence of each date (the start of that day's content)
  - Chunk the text from that line up to the next day's start line
  - Preserve original text faithfully — Adam can edit later if anything reads rough

Usage:  python3 scripts/split_pdf_to_daily_md.py
"""
import re
from pathlib import Path
from datetime import date

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "data/readings"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Day-marker patterns:
#   Optional "📅 " prefix
#   Weekday (Sunday..Saturday)
#   Optional comma
#   Month name + day number
#   Optional ", 2026"
#   Optional " — HHMM"
WEEKDAYS = r"(?:Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday)"
DATE_RE = re.compile(
    rf"^(?:📅\s+)?{WEEKDAYS},?\s+(January|February)\s+(\d{{1,2}})(?:,\s*\d{{4}})?(?:\s*—\s*\d{{3,4}})?\s*$"
)


def find_day_starts(lines, month_name):
    """Walk lines, return [(day_num, line_idx), ...] for the FIRST occurrence of each day."""
    seen = set()
    starts = []
    for i, line in enumerate(lines):
        m = DATE_RE.match(line)
        if not m:
            continue
        if m.group(1) != month_name:
            continue
        day = int(m.group(2))
        if day in seen:
            continue
        seen.add(day)
        starts.append((day, i))
    return starts


def split_month(text_path, year, month_num, month_name, expected_days):
    text = Path(text_path).read_text()
    # Strip form-feed (\x0c) chars that pdftotext inserts at page boundaries — they break ^ anchoring
    text = text.replace("\x0c", "")
    lines = text.split("\n")
    starts = find_day_starts(lines, month_name)
    print(f"\n--- {month_name} ---")
    print(f"  found day-start markers: {len(starts)} (expected {expected_days})")

    # If we found fewer, surface which days are missing
    found_days = {d for d, _ in starts}
    missing = [d for d in range(1, expected_days + 1) if d not in found_days]
    if missing:
        print(f"  MISSING day-start markers for: {missing}")
        print(f"  (these days won't get split out automatically; flag for manual recovery)")

    # Build (day_num, start_line, end_line) tuples
    chunks = []
    for idx, (day, ln) in enumerate(starts):
        end_ln = starts[idx + 1][1] if idx + 1 < len(starts) else len(lines)
        chunks.append((day, ln, end_ln))

    written = []
    for day, start, end in chunks:
        body = "\n".join(lines[start:end]).rstrip() + "\n"
        # Header inserted at top so the .md file is self-contained
        date_iso = f"{year:04d}-{month_num:02d}-{day:02d}"
        weekday_name = date(year, month_num, day).strftime("%A")
        doc_n = 1 if month_num == 1 else 2
        front = (
            f"# MOOP's 2026 Daily Bible Readings\n"
            f"## Document {doc_n} of 12; for the month of {month_name}\n\n"
            f"## {weekday_name}, {month_name} {day}, {year}\n\n"
            f"_Converted from PDF source on 2026-05-23. Original .pages file: "
            f"~/Library/Mobile Documents/com~apple~Pages/Documents/{doc_n}) MOOP's "
            f"{'daily Bible Readings - January' if month_num == 1 else 'DBR - Feb'}.pages_\n\n"
            f"---\n\n"
        )
        out_path = OUT_DIR / f"{date_iso}.md"
        out_path.write_text(front + body)
        written.append((date_iso, len(body)))

    print(f"  wrote: {len(written)} .md files")
    for d, sz in written[:3]:
        print(f"    {d}: {sz} chars")
    if len(written) > 3:
        print(f"    ... ({len(written) - 3} more)")
    return written, missing


def main():
    jan_results, jan_missing = split_month("/tmp/bible_jan_clean.txt", 2026, 1, "January", 31)
    feb_results, feb_missing = split_month("/tmp/bible_feb_clean.txt", 2026, 2, "February", 28)

    print(f"\n=== TOTAL ===")
    print(f"  Wrote: {len(jan_results) + len(feb_results)} per-day .md files to {OUT_DIR}")
    print(f"  Missing: {len(jan_missing) + len(feb_missing)} (Jan: {jan_missing}, Feb: {feb_missing})")


if __name__ == "__main__":
    main()
