#!/usr/bin/env python3
"""
Fix empty-bullet pattern in data/readings/*.md files.

Bug source: pdftotext put PDF bullet markers on separate lines from their content,
producing patterns like:

    ⛏ Husband's Application — Honoring
    •
    •
    •
    •

    Block a real Sabbath window this week: worship, rest, and screens down.
    Choose one "willing heart" gift today—money, time, service—without broadcasting it.
    Apply one skill to bless your wife before the day ends (fix, plan, clean, lead prayer).
    Say it plainly: "Our home stops for God and gives for God."

Fix: merge each empty bullet with its corresponding content line so it renders as:

    • Block a real Sabbath window this week: ...
    • Choose one "willing heart" gift today: ...
    • etc.

Strategy:
  1. Find runs of N ≥ 2 consecutive lines that are exactly "•"
  2. Skip blank lines
  3. Take the next N non-blank lines that don't start with structural markers
     (⛏ 🙏 ⚓ 🛡 🧭 🌅 🕖 🕚 🕒 🌙 📖 🦅 ❤️ 👨‍👦 🍃 🗺 🏞 ✝️ #)
  4. Replace the empty bullets + content lines with merged "• content" lines
  5. Write back, report changes

Run from repo root:
    python3 scripts/fix_empty_bullets.py [--dry-run]
"""
import re
import sys
import glob
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS_DIR = REPO / "data/readings"

# Lines that look like section/structural markers — don't consume these as bullet content
STRUCTURAL_PREFIXES = ("⛏", "🙏", "⚓", "🛡", "🧭", "🌅", "🕖", "🕚", "🕒", "🌙",
                       "📖", "🦅", "❤️", "👨", "🍃", "🗺", "🏞", "✝", "📅", "💍",
                       "#", "---", "⸻")


def is_structural(line: str) -> bool:
    s = line.lstrip()
    return any(s.startswith(p) for p in STRUCTURAL_PREFIXES)


def fix_file(path: Path, dry_run: bool = False):
    lines = path.read_text().split("\n")
    out = []
    i = 0
    fix_count = 0
    while i < len(lines):
        line = lines[i]
        # Detect a run of consecutive "•" lines (with optional trailing whitespace)
        if line.strip() == "•":
            run_start = i
            run = 0
            while i < len(lines) and lines[i].strip() == "•":
                run += 1
                i += 1
            if run < 2:
                # Single lone bullet — keep as-is, don't try to merge
                out.extend(lines[run_start:i])
                continue

            # Skip blank lines after the bullet run
            blanks_after = []
            while i < len(lines) and lines[i].strip() == "":
                blanks_after.append(lines[i])
                i += 1

            # Collect up to `run` non-structural non-empty lines as bullet content
            content_lines = []
            j = i
            while j < len(lines) and len(content_lines) < run:
                cand = lines[j]
                if cand.strip() == "":
                    j += 1
                    continue
                if is_structural(cand):
                    break
                content_lines.append(cand.rstrip())
                j += 1

            if len(content_lines) == run:
                # Clean merge: replace bullets + (consumed) content lines with merged bullets
                for c in content_lines:
                    out.append(f"• {c}")
                # Preserve a blank line after the bullet list if there was one
                out.append("")
                fix_count += 1
                i = j  # consumed content lines
            else:
                # Couldn't find matching content — keep original as-is and flag
                print(f"  ⚠️  {path.name}: block at line {run_start+1} has {run} bullets but only {len(content_lines)} content lines available — left as-is for manual review")
                out.extend(lines[run_start:i])  # original bullets
                out.extend(blanks_after)
                # don't consume content lines — leave for next iteration
        else:
            out.append(line)
            i += 1

    if fix_count and not dry_run:
        path.write_text("\n".join(out))
    return fix_count


def main():
    dry = "--dry-run" in sys.argv
    files = sorted(READINGS_DIR.glob("2026-0[12]-*.md"))
    print(f"Scanning {len(files)} files{' (dry-run)' if dry else ''}...")
    total = 0
    fixed_files = 0
    for f in files:
        fixed = fix_file(f, dry_run=dry)
        if fixed:
            print(f"  ✓ {f.name}: {fixed} block(s) merged")
            fixed_files += 1
            total += fixed
    print(f"\nTotal: {total} block(s) merged across {fixed_files} file(s)")
    if dry:
        print("(dry-run — no files written)")


if __name__ == "__main__":
    main()
