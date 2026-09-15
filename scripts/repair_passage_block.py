#!/usr/bin/env python3
"""Rewrite a watch's Scripture block from the canonical text in this repo.

PJG-0915-WIS1: watch Scripture blocks were pre-generated in bulk and some
carry foreign verses, cross-chapter bleed and duplicated lines (see
scripts/check_passage_containment.py). The named passage owns the quote, so
the repair is to re-lay that block straight from
docs/assets/chapters/<book>_<chapter>.json — the same canonical text the Bible
Text Engine serves — instead of hand-patching individual bad lines.

Only the block under "📖 Scripture — <passage>" is touched. Context Summary,
Application, Prayer and Watch Charge are left exactly as written; cross
references belong in Context, and this tool never edits it.

Usage:
  python3 scripts/repair_passage_block.py 2026-09-16 --watch wisdom
  python3 scripts/repair_passage_block.py 2026-09-16 --watch wisdom --apply
  python3 scripts/repair_passage_block.py 2026-09-16 --all-watches --apply

Without --apply this prints a diff summary and writes nothing.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from check_passage_containment import (  # noqa: E402
    BOOK_NUM,
    TAG_RE,
    extract_scripture_bounded,
    load_chapter,
    parse_passage,
    scripture_lines,
)

JSON_DIR = REPO / "docs" / "assets" / "readings"
MD_DIR = REPO / "data" / "readings"


def clean_verse(text: str) -> str:
    """Canonical verse text as a single rendered line."""
    s = TAG_RE.sub("", text or "")
    s = s.replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def canonical_block(passage: str) -> str | None:
    refs = parse_passage(passage)
    if not refs:
        return None
    out: list[str] = []
    for book, chapter, vs, ve in refs:
        num = BOOK_NUM.get(book)
        if not num:
            return None
        verses = load_chapter(num, chapter)
        if not verses:
            return None
        for vnum in sorted(verses, key=lambda k: int(k)):
            n = int(vnum)
            if vs is not None and not (vs <= n <= (ve or vs)):
                continue
            line = clean_verse(verses[vnum])
            if line:
                out.append(line)
    return "\n".join(out) if out else None


def repair_text(text: str, passage: str) -> tuple[str, int, int] | None:
    """Return (new_text, old_line_count, new_line_count) or None."""
    scr, bounded = extract_scripture_bounded(text)
    if not scr or not bounded:
        return None
    block = canonical_block(passage)
    if not block:
        return None
    old_n = len(scripture_lines(scr))
    new_n = len(scripture_lines(block))
    # Preserve the surrounding newline shape exactly.
    lead = len(scr) - len(scr.lstrip("\n"))
    trail = len(scr) - len(scr.rstrip("\n"))
    replacement = ("\n" * lead) + block + ("\n" * trail)
    return text.replace(scr, replacement, 1), old_n, new_n


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("date")
    ap.add_argument("--watch", action="append", default=[])
    ap.add_argument("--all-watches", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv)

    jp = JSON_DIR / f"{args.date}.json"
    mp = MD_DIR / f"{args.date}.md"
    if not jp.exists():
        print(f"ERROR: {jp} missing", file=sys.stderr)
        return 2

    raw = jp.read_text(encoding="utf-8")
    day = json.loads(raw)
    watches = day.get("watches") or {}
    targets = list(watches) if args.all_watches else args.watch
    if not targets:
        print("ERROR: pass --watch KEY or --all-watches", file=sys.stderr)
        return 2

    md = mp.read_text() if mp.exists() else None
    changed = False

    for wkey in targets:
        w = watches.get(wkey)
        if not w:
            print(f"skip {wkey}: not in day", file=sys.stderr)
            continue
        passage = w.get("passage") or ""
        res = repair_text(w.get("text") or "", passage)
        if not res:
            print(f"skip {wkey} ({passage}): unresolvable or unbounded", file=sys.stderr)
            continue
        new_text, old_n, new_n = res
        if new_text == w.get("text"):
            print(f"ok   {wkey} ({passage}): already canonical ({new_n} lines)")
            continue
        print(f"FIX  {wkey} ({passage}): {old_n} lines -> {new_n} canonical verses")
        if args.apply:
            old_scr, bounded = extract_scripture_bounded(w.get("text") or "")
            new_scr, _b = extract_scripture_bounded(new_text)
            # Surgical raw edit: the readings JSON is written with indent=1 and
            # a re-serialize would reformat every unrelated line in the file.
            for enc in (False, True):
                needle = json.dumps(old_scr, ensure_ascii=enc)[1:-1]
                if needle and raw.count(needle) == 1:
                    raw = raw.replace(
                        needle, json.dumps(new_scr, ensure_ascii=enc)[1:-1], 1
                    )
                    break
            else:
                print(f"     ERROR: {wkey} block not uniquely locatable in JSON",
                      file=sys.stderr)
                return 3
            if md is not None:
                if bounded and old_scr and md.count(old_scr) == 1:
                    md = md.replace(old_scr, new_scr, 1)
                else:
                    print(f"     WARN: md block for {wkey} not matched; md untouched",
                          file=sys.stderr)
            changed = True

    if args.apply and changed:
        json.loads(raw)  # refuse to write anything that is not valid JSON
        jp.write_text(raw, encoding="utf-8")
        if md is not None:
            mp.write_text(md)
        print(f"wrote {jp}" + (f" and {mp}" if md is not None else ""))
    elif not args.apply:
        print("(dry run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
