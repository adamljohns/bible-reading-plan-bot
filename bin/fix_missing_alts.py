#!/usr/bin/env python3
"""Add alt="" to decorative shield/icon <img> tags missing alt.

A decorative image (one that adds visual flair next to readable text but
conveys no information by itself) should have alt="" per WCAG. That tells
screen readers to skip it cleanly rather than announcing the filename.

Conservative criteria — only adds alt="" when:
  - The <img> tag has class="site-icon", OR
  - The src points at /assets/icons/ AND has an explicit width <= 64px

Leaves all other missing-alt images alone (those need human-written alt
text and shouldn't be auto-stamped).
"""
import os
import re

IMG_RE = re.compile(r'<img\s+([^>]*?)>', re.IGNORECASE | re.DOTALL)
ALT_RE = re.compile(r'\balt\s*=', re.IGNORECASE)
SITE_ICON_CLASS = re.compile(r'\bclass\s*=\s*"[^"]*\bsite-icon\b[^"]*"', re.IGNORECASE)
ICON_SRC = re.compile(r'\bsrc\s*=\s*"[^"]*/icons/[^"]*"', re.IGNORECASE)
SMALL_WIDTH = re.compile(r'\bwidth\s*=\s*"?(\d+)"?', re.IGNORECASE)

SKIP_DIRS = {'_archive', '_backup', '_wip', '_drafts', 'churches', 'lexicon', 'chapters', 'verse'}


def is_decorative(attrs):
    if SITE_ICON_CLASS.search(attrs):
        return True
    if ICON_SRC.search(attrs):
        m = SMALL_WIDTH.search(attrs)
        if m and int(m.group(1)) <= 64:
            return True
    return False


def main():
    total_added = 0
    files_changed = 0
    for root, dirs, files in os.walk('docs'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if not fn.endswith('.html'):
                continue
            fp = os.path.join(root, fn)
            with open(fp, 'r', encoding='utf-8') as f:
                html = f.read()

            added_here = [0]

            def stamp(m):
                attrs = m.group(1)
                if ALT_RE.search(attrs):
                    return m.group(0)
                if not is_decorative(attrs):
                    return m.group(0)
                added_here[0] += 1
                # Insert alt="" at the start of attrs, preserving spacing
                return f'<img alt="" {attrs.strip()}>'

            new_html = IMG_RE.sub(stamp, html)
            if added_here[0] > 0:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(new_html)
                total_added += added_here[0]
                files_changed += 1

    print(f'Added alt="" to {total_added} decorative <img> across {files_changed} files')


if __name__ == '__main__':
    main()
