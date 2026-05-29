#!/usr/bin/env python3
"""strip_em_dashes.py — replace em-dashes in selected blog posts per @blader's rule.

The @blader/humanizer rule (Wikipedia Signs of AI Writing): em-dashes are
one of the strongest AI tells. Replace in this order of preference:
  1. Period (new sentence) — when both sides are independent clauses
  2. Comma (tight aside) — when the em-dash is parenthetical mid-sentence
  3. Colon (introducing) — when introducing an explanation
  4. Parentheses (true aside) — when a matched pair of em-dashes brackets an aside

This script applies a conservative heuristic:
  - spaced em-dash followed by a capital letter that starts an independent clause: PERIOD
  - all other spaced em-dashes: COMMA
  - matched-pair em-dashes around a parenthetical: COMMAS (becomes a "tight aside")

Targets blog HTML files passed on the command line. Operates inside <p>,
<blockquote>, <li>, headings. Avoids touching <nav>, <footer>, <style>,
<script>. Replaces both raw em-dashes (—) and the HTML entity &mdash;.

Usage:
  python3 bin/strip_em_dashes.py docs/blog/your-post.html [more.html ...]
  python3 bin/strip_em_dashes.py --dry-run docs/blog/your-post.html

Per Adam's standing decision 2026-05-28:
  - Pre-2024 blog posts: untouched (authentic Adam voice)
  - 2026 AI-assisted posts: em-dashes stripped per @blader rule
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Content-bearing blocks we'll modify.
LINKABLE_BLOCK_PAT = re.compile(
    r"(<(?:p|h2|h3|h4|h5|h6|blockquote|li)\b[^>]*>)(.*?)(</(?:p|h2|h3|h4|h5|h6|blockquote|li)>)",
    re.DOTALL | re.IGNORECASE,
)
NAV_FOOTER_PAT = re.compile(
    r"(<(?:nav|footer|header|style|script)\b[^>]*>.*?</(?:nav|footer|header|style|script)>)",
    re.DOTALL | re.IGNORECASE,
)
ANY_TAG_PAT = re.compile(r"<[^>]+>")

# Normalize both forms to one token, then operate on that, then restore.
EMDASH_FORMS = ("—", "&mdash;")
TOKEN = "\x00EMD\x00"  # internal sentinel


def normalize(text: str) -> tuple[str, str]:
    """Return (normalized-with-token, original-emdash-form-preferred).

    We pick the dominant form in the file so restored em-dashes (if any)
    use the file's house style. But we won't restore any in this script
    — we're stripping all of them.
    """
    if "&mdash;" in text:
        canonical = "&mdash;"
    else:
        canonical = "—"
    norm = text.replace("&mdash;", TOKEN).replace("—", TOKEN)
    return norm, canonical


def replace_emdashes_in_paragraph(body: str) -> tuple[str, int]:
    """Replace em-dash tokens inside one paragraph body."""
    # Mask all HTML tags so we never inject inside attributes.
    masks: list[str] = []

    def store(s: str) -> str:
        masks.append(s)
        return f"\x01M{len(masks)-1}\x01"

    work = ANY_TAG_PAT.sub(lambda m: store(m.group(0)), body)

    count = 0

    # Pattern 1: " {TOKEN} " (spaced em-dash).
    # Decision (revised after first test broke a parenthetical-pair sentence):
    # ALWAYS use comma. Mechanical period-substitution breaks too many
    # parenthetical-aside em-dashes (where both sides go together).
    # Comma-substitution may produce a longer sentence, but never breaks
    # the grammar. Adam can review and split into multiple sentences manually
    # where it improves the rhythm.
    def replace_spaced(m: re.Match) -> str:
        nonlocal count
        count += 1
        after = m.group(1)
        return f", {after}"

    work = re.sub(r"\s*" + re.escape(TOKEN) + r"\s*(\S?)", replace_spaced, work)

    # Pattern 2: any stragglers (no whitespace) get comma.
    while TOKEN in work:
        work = work.replace(TOKEN, ", ", 1)
        count += 1

    # Restore masked tags.
    def restore(m: re.Match) -> str:
        return masks[int(m.group(1))]

    work = re.sub(r"\x01M(\d+)\x01", restore, work)

    # Clean up double-spaces, comma-followed-by-period, etc.
    work = re.sub(r" +([,.])", r"\1", work)  # space-comma → comma
    work = re.sub(r"  +", " ", work)  # collapse double spaces
    work = re.sub(r"\.\s+\.", ".", work)  # ". ." → "."
    work = re.sub(r",\s*,", ",", work)  # ", ," → ","

    return work, count


def process_html(html: str) -> tuple[str, int]:
    # Mask nav/footer/style/script.
    region_masks: list[str] = []

    def store_region(m: re.Match) -> str:
        region_masks.append(m.group(0))
        return f"\x02Z{len(region_masks)-1}\x02"

    work = NAV_FOOTER_PAT.sub(store_region, html)
    # Tokenize em-dashes for unambiguous handling.
    work_tok, _ = normalize(work)

    total_count = 0

    def per_block(m: re.Match) -> str:
        nonlocal total_count
        open_t, body, close_t = m.group(1), m.group(2), m.group(3)
        new_body, n = replace_emdashes_in_paragraph(body)
        total_count += n
        return open_t + new_body + close_t

    new_work = LINKABLE_BLOCK_PAT.sub(per_block, work_tok)

    # Restore regions.
    def restore_region(m: re.Match) -> str:
        return region_masks[int(m.group(1))]

    new_html = re.sub(r"\x02Z(\d+)\x02", restore_region, new_work)
    # Any remaining tokens (outside content blocks) get left as-is by restoring.
    new_html = new_html.replace(TOKEN, "&mdash;")
    return new_html, total_count


def process_file(path: str, dry_run: bool = False) -> int:
    p = Path(path)
    if not p.exists():
        print(f"  ERROR: {path} not found", file=sys.stderr)
        return 0
    html = p.read_text(encoding="utf-8")
    new_html, count = process_html(html)
    if count > 0 and not dry_run and new_html != html:
        p.write_text(new_html, encoding="utf-8")
    return count


def main() -> int:
    ap = argparse.ArgumentParser(description="Strip em-dashes from blog posts per @blader's rule.")
    ap.add_argument("targets", nargs="+", help="Blog HTML files to process.")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    print(f"Processing {len(args.targets)} file(s)..." +
          (" (dry-run; no writes)" if args.dry_run else ""))
    total = 0
    affected = 0
    for t in args.targets:
        n = process_file(t, dry_run=args.dry_run)
        if n > 0:
            print(f"  {Path(t).name}: {n} em-dashes replaced")
            affected += 1
            total += n
        else:
            print(f"  {Path(t).name}: 0")
    print()
    print(f"Total em-dashes replaced: {total}")
    print(f"Files affected:           {affected}/{len(args.targets)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
