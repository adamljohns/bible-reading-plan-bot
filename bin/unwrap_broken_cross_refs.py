#!/usr/bin/env python3
"""Unwrap broken cross-reference <a> tags in dictionary entries.

For Related Words sections (and other inline dict-to-dict links), strip
the <a href="...">text</a> wrapper IF the href points to a non-existent
HTML file in the same directory. Leaves the inner text in place so
readers still see the word — just no broken click.

Only operates on dictionary entries. Skips:
  - External hrefs (http://, mailto:, etc.)
  - Anchor-only hrefs (#section)
  - Working same-directory hrefs (file exists)
  - hrefs to other directories or to bible.html?ref=... or similar
"""
import os
import re
import glob

DICT_DIR = 'docs/dictionary'

# Conservative: only unwrap hrefs that are simple "<slug>.html" or "<slug>.html#anchor"
# pointing at a same-directory file that doesn't exist.
LINK_RE = re.compile(
    r'<a\s+href="([a-zA-Z0-9_-]+\.html)(#[^"]*)?"([^>]*)>(.*?)</a>',
    re.IGNORECASE | re.DOTALL,
)


def main():
    existing = {os.path.basename(p) for p in glob.glob(os.path.join(DICT_DIR, '*.html'))}
    total_unwrapped = 0
    files_changed = 0

    for fp in sorted(glob.glob(os.path.join(DICT_DIR, '*.html'))):
        with open(fp, 'r', encoding='utf-8') as f:
            html = f.read()

        unwrapped_here = [0]

        def replacer(m):
            slug = m.group(1)
            inner = m.group(4)
            if slug in existing:
                return m.group(0)  # keep as-is
            unwrapped_here[0] += 1
            return inner  # unwrap to plain text

        new_html = LINK_RE.sub(replacer, html)
        if unwrapped_here[0] > 0:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_html)
            total_unwrapped += unwrapped_here[0]
            files_changed += 1

    print(f'Unwrapped {total_unwrapped} broken cross-reference links across {files_changed} files')


if __name__ == '__main__':
    main()
