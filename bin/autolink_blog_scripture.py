#!/usr/bin/env python3
"""autolink_blog_scripture.py — link Scripture refs in blog posts to BTE.

Walks `docs/blog/*.html` and inside the content region wraps matched
canonical Scripture references in `<a class="bte-scrip">` elements
pointing to `../bible.html?ref=<encoded>`.

Match patterns (full canonical references only — no bare book names,
no chapter-only refs):
  - "John 3:16"
  - "1 Cor 13:1-3"
  - "Hebrews 4:12-13"
  - "Genesis 1:1-31"
  - "Psalm 23:1-6"
  - "1 Peter 5:8"

Uses the same regex pattern as docs/assets/js/lbcf-render.js for
consistency across the Reformed Digital Library.

Same masking pattern as autolink_blog.py:
  1. Mask existing <a>...</a> anchors so we never nest
  2. Mask all HTML tags so we never link inside attributes (img src, etc.)
  3. Match and wrap canonical Scripture refs
  4. Restore masks

Idempotent: existing bte-scrip anchors are detected and skipped because
the matched text inside an existing anchor will be masked.

Usage:
  python3 bin/autolink_blog_scripture.py                # all blog posts
  python3 bin/autolink_blog_scripture.py --dry-run
  python3 bin/autolink_blog_scripture.py --limit 10 --verbose
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(ROOT, "docs", "blog")

# Match content-bearing block elements. We only link inside these.
LINKABLE_BLOCK_PAT = re.compile(
    r"(<(?:p|h2|h3|h4|h5|h6|blockquote|li)\b[^>]*>)(.*?)(</(?:p|h2|h3|h4|h5|h6|blockquote|li)>)",
    re.DOTALL | re.IGNORECASE,
)
ANCHOR_PAT = re.compile(r"<a\b[^>]*>.*?</a>", re.DOTALL | re.IGNORECASE)
ANY_TAG_PAT = re.compile(r"<[^>]+>")
NAV_FOOTER_PAT = re.compile(
    r"(<(?:nav|footer|header|style|script)\b[^>]*>.*?</(?:nav|footer|header|style|script)>)",
    re.DOTALL | re.IGNORECASE,
)

# Mirror of SCRIPTURE_RE in docs/assets/js/lbcf-render.js. Canonical
# references only: book + chapter + (optional) verse(s) with possible
# range or list.
BOOK_ALTERNATIVES = (
    r"(?:[1-3]\s)?"  # Optional 1/2/3 prefix
    r"(?:Genesis|Gen|Exodus|Exo|Ex|Leviticus|Lev|Numbers|Num|Deuteronomy|Deut|Dt|"
    r"Joshua|Josh|Judges|Judg|Ruth|Samuel|Sam|Kings|Kgs|"
    r"Chronicles|Chron|Chr|Ezra|Nehemiah|Neh|Esther|Est|Job|"
    r"Psalms?|Ps|Proverbs|Prov|Pr|Ecclesiastes|Eccl|Ecc|"
    r"Song of Solomon|Song of Songs|Song|SoS|"
    r"Isaiah|Isa|Is|Jeremiah|Jer|Lamentations|Lam|"
    r"Ezekiel|Ezek|Eze|Daniel|Dan|"
    r"Hosea|Hos|Joel|Amos|Obadiah|Obad|Jonah|Jon|"
    r"Micah|Mic|Nahum|Nah|Habakkuk|Hab|Zephaniah|Zeph|"
    r"Haggai|Hag|Zechariah|Zech|Malachi|Mal|"
    r"Matthew|Matt|Mt|Mark|Mk|Luke|Lk|John|Jn|Acts|"
    r"Romans|Rom|Corinthians|Cor|Galatians|Gal|Ephesians|Eph|"
    r"Philippians|Phil|Php|Colossians|Col|"
    r"Thessalonians|Thess|Th|Timothy|Tim|Ti|Titus|Tit|"
    r"Philemon|Philem|Phlm|Hebrews|Heb|"
    r"James|Jas|Peter|Pet|Jude|Revelation|Rev)"
)

# Canonical reference: book + space + chapter + colon + verse(s).
# We REQUIRE a verse part (no chapter-only refs) for precision.
SCRIPTURE_RE = re.compile(
    r"\b(" + BOOK_ALTERNATIVES + r")\s(\d+):(\d+(?:[–—-]\d+)?(?:,\s*\d+(?:[–—-]\d+)?)*)\b",
    re.IGNORECASE,
)


def ref_to_url(book: str, chapter: str, verses: str) -> str:
    ref = f"{book.strip()} {chapter}:{verses}"
    return "../bible.html?ref=" + urllib.parse.quote(ref)


def mask_and_link(text: str, used_refs: set[str], counts: dict[str, int]) -> tuple[str, int]:
    """Mask existing anchors + tags, then auto-link Scripture refs."""
    masks: list[str] = []

    def store(s: str) -> str:
        masks.append(s)
        return f"\x00MASK{len(masks)-1}\x00"

    # Step 1: mask existing <a>...</a> anchors entirely.
    work = ANCHOR_PAT.sub(lambda m: store(m.group(0)), text)
    # Step 2: mask all remaining HTML tags so we never inject inside attributes.
    work = ANY_TAG_PAT.sub(lambda m: store(m.group(0)), work)

    added = 0

    def replace_ref(m: re.Match) -> str:
        nonlocal added
        full = m.group(0)
        book = m.group(1)
        chapter = m.group(2)
        verses = m.group(3)
        # First-occurrence-per-page rule (canonical key normalized).
        key = (book.lower().strip() + " " + chapter + ":" + verses).strip()
        if key in used_refs:
            return full
        used_refs.add(key)
        counts["added"] = counts.get("added", 0) + 1
        added += 1
        url = ref_to_url(book, chapter, verses)
        link = f'<a class="bte-scrip" href="{url}" title="Open in BTE">{full}</a>'
        return store(link)

    work = SCRIPTURE_RE.sub(replace_ref, work)

    # Step 3: restore masks (back-to-back substitution).
    def restore(s: str) -> str:
        def _r(m: re.Match) -> str:
            return masks[int(m.group(1))]

        for _ in range(3):  # multiple passes in case masks contained MASK markers
            s, n = re.subn(r"\x00MASK(\d+)\x00", _r, s)
            if n == 0:
                break
        return s

    return restore(work), added


def process_blog_html(path: str, dry_run: bool = False, verbose: bool = False) -> int:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # First, mask the nav/footer/header/style/script zones so we don't touch them.
    region_masks: list[str] = []

    def store_region(m: re.Match) -> str:
        region_masks.append(m.group(0))
        return f"\x01ZONE{len(region_masks)-1}\x01"

    work = NAV_FOOTER_PAT.sub(store_region, html)

    # Per-page first-occurrence dedupe.
    used_refs: set[str] = set()
    counts: dict[str, int] = {"added": 0}

    def linkify_block(m: re.Match) -> str:
        open_tag, body, close_tag = m.group(1), m.group(2), m.group(3)
        new_body, _ = mask_and_link(body, used_refs, counts)
        return open_tag + new_body + close_tag

    new_work = LINKABLE_BLOCK_PAT.sub(linkify_block, work)

    # Restore nav/footer/etc. zones.
    def restore_region(m: re.Match) -> str:
        return region_masks[int(m.group(1))]

    new_html = re.sub(r"\x01ZONE(\d+)\x01", restore_region, new_work)

    added = counts.get("added", 0)
    if added > 0 and not dry_run and new_html != html:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)
    if verbose and added > 0:
        print(f"  {os.path.basename(path)}: +{added} scripture links")
    return added


def main() -> int:
    ap = argparse.ArgumentParser(description="Auto-link Scripture refs in blog posts to BTE.")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    blog_files = sorted(glob.glob(os.path.join(BLOG_DIR, "*.html")))
    if args.limit > 0:
        blog_files = blog_files[: args.limit]

    print(f"Processing {len(blog_files)} blog files...")
    total = 0
    files_affected = 0
    for path in blog_files:
        added = process_blog_html(path, dry_run=args.dry_run, verbose=args.verbose)
        total += added
        if added > 0:
            files_affected += 1

    print()
    print("Done." + (" (dry run — no files written)" if args.dry_run else " Wrote in place."))
    print(f"  Total scripture links added: {total}")
    print(f"  Files affected:              {files_affected}/{len(blog_files)}")
    print(
        f"  Avg links per affected file: "
        + (f"{total / files_affected:.1f}" if files_affected else "n/a")
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
