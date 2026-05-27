#!/usr/bin/env python3
"""dedup_dict_links.py — strip duplicate dict-link anchors from blog HTML.

The autolinker had a bug where each re-run picked up the next un-linked
occurrence of a popular word; over many runs, common words like "salvation"
or "scripture" ended up with 2-4 links per post, while the dictionary's
long tail of less-common words sat unlinked.

This script unwraps every dict-link anchor after the FIRST one per slug per
post, leaving the rest as plain text. Run once to clean up; the fixed
autolinker won't re-introduce the duplicates.

Usage:
  python3 bin/dedup_dict_links.py            # all blog posts
  python3 bin/dedup_dict_links.py --dry-run
  python3 bin/dedup_dict_links.py --verbose
"""
import argparse
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(ROOT, 'docs', 'blog')

# Match a dict-link anchor: <a class="dict-link" href="../dictionary/SLUG.html">TEXT</a>
DICT_LINK_RE = re.compile(
    r'<a\s+class="dict-link"\s+href="\.\./dictionary/([^"]+)\.html">([^<]+)</a>',
    re.IGNORECASE,
)


def dedup_post(html):
    """Keep the first dict-link per slug; replace subsequent ones with plain text.

    Returns (new_html, removed_count, slugs_touched).
    """
    seen_slugs = set()
    removed = 0
    slugs_touched = set()

    def _replace(m):
        nonlocal removed
        slug = m.group(1).lower()
        text = m.group(2)
        if slug in seen_slugs:
            removed += 1
            slugs_touched.add(slug)
            return text  # unwrap: keep the inner text, drop the anchor
        seen_slugs.add(slug)
        return m.group(0)  # keep the anchor as-is

    new_html = DICT_LINK_RE.sub(_replace, html)
    return new_html, removed, slugs_touched


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--pattern', default='*.html')
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(BLOG_DIR, args.pattern)))
    print(f'Processing {len(files)} blog files…')

    total_removed = 0
    files_changed = 0
    for fp in files:
        with open(fp, 'r', encoding='utf-8') as f:
            html = f.read()
        new_html, removed, slugs = dedup_post(html)
        if removed == 0:
            continue
        files_changed += 1
        total_removed += removed
        if args.verbose:
            print(f'  {os.path.basename(fp)}: -{removed} duplicate links across {len(slugs)} slug(s)')
        if not args.dry_run:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_html)

    print()
    print(f'Done. {"DRY-RUN" if args.dry_run else "Wrote in place"}.')
    print(f'  Duplicate dict-links removed: {total_removed}')
    print(f'  Files affected:               {files_changed}/{len(files)}')


if __name__ == '__main__':
    main()
