#!/usr/bin/env python3
"""One-shot patcher: removes the stray </div> that some 503 dictionary
entries have right after the corruption-inner close.

The bug pattern is:
    <div class="corruption-inner">
        <p>...</p>
    </div>                              <- correct close of corruption-inner
                            </div>       <- STRAY: prematurely closes <div class="container">
    </details>
</div>

After the stray </div>, everything below (Greek/Hebrew Roots,
Proto-Language Roots, Related Words) renders outside .container at body width.

The fix: drop the second </div> that lives between corruption-inner's close
and </details>.
"""
import os
import re
import glob

DICT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs', 'dictionary')

# Match: corruption-inner opener, its content, its close, then a STRAY </div>,
# then </details>. Capture the keep-parts; drop the stray.
BUG_PATTERN = re.compile(
    r'(<div class="corruption-inner">.*?</div>)\s*</div>\s*(</details>)',
    re.DOTALL
)


def fix_file(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
    if 'corruption-inner' not in html:
        return False
    new_html, n = BUG_PATTERN.subn(r'\1\n            \2', html, count=1)
    if n == 0:
        return False
    if new_html == html:
        return False
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_html)
    return True


def main():
    files = sorted(glob.glob(os.path.join(DICT_DIR, '*.html')))
    fixed = 0
    skipped = 0
    for fp in files:
        name = os.path.basename(fp)
        if name in ('index.html', 'names.html'):
            continue
        if fix_file(fp):
            fixed += 1
        else:
            skipped += 1
    print(f"Patched: {fixed}")
    print(f"Untouched (no bug or no corruption-inner): {skipped}")


if __name__ == '__main__':
    main()
