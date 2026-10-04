#!/usr/bin/env python3
"""Audit dictionary entries for missing standard sections.

A "complete" entry has all of these sections (case-insensitive heading match):
  - Biblical Definition
  - Webster 1828
  - Key Scripture
  - Modern Corruption
  - Related Words

Plus optional but recommended:
  - Greek & Hebrew Roots
  - Proto-Language Roots
  - Usage

Report which entries are missing required sections.

  python3 bin/audit_dict_completeness.py           # print coverage (every *.html)
  python3 bin/audit_dict_completeness.py --write   # also rewrite DICT_COMPLETENESS_AUDIT.md

--write scopes the report to live entries (data/dictionary-slugs.txt), so the
redirect stubs and section/special pages do not show up as "incomplete".
"""
import os
import re
import glob
import sys
from collections import Counter

REPORT = 'DICT_COMPLETENESS_AUDIT.md'
SLUGS_FILE = 'data/dictionary-slugs.txt'
# The three sections the written report tracks (its original scope).
REPORT_SECTIONS = ('biblical_def', 'webster', 'modern_corruption')

REQUIRED_SECTIONS = [
    ('biblical_def',     r'Biblical (Definition|Meaning)'),
    ('webster',          r'Webster 1828'),
    ('key_scripture',    r'Key Scriptures?'),
    ('modern_corruption',r'Modern Corruption'),
    ('related',          r'Related (Words|Entries|Terms)'),
]

OPTIONAL_SECTIONS = [
    ('greek_hebrew', r'Greek\s*&amp;\s*Hebrew Roots|Greek & Hebrew Roots'),
    ('proto',        r'Proto-Language Roots'),
    ('usage',        r'(?<![a-zA-Z])Usage(?![a-zA-Z])'),  # word "Usage" not part of longer word
]


def check(html, patterns):
    missing = []
    for key, pat in patterns:
        if not re.search(pat, html, re.IGNORECASE):
            missing.append(key)
    return missing


def main():
    entries = sorted(glob.glob('docs/dictionary/*.html'))
    # Skip the index file
    entries = [e for e in entries if os.path.basename(e) not in ('index.html', 'names.html')]
    print(f'Auditing {len(entries)} dictionary entries')
    print()

    required_missing_counts = Counter()
    optional_missing_counts = Counter()
    entries_with_all_required = 0
    entries_with_any_required_missing = []

    for fp in entries:
        with open(fp, 'r', encoding='utf-8') as f:
            html = f.read()
        missing_req = check(html, REQUIRED_SECTIONS)
        missing_opt = check(html, OPTIONAL_SECTIONS)
        for k in missing_req: required_missing_counts[k] += 1
        for k in missing_opt: optional_missing_counts[k] += 1
        if not missing_req:
            entries_with_all_required += 1
        else:
            entries_with_any_required_missing.append((os.path.basename(fp), missing_req))

    print('=== REQUIRED section coverage ===')
    for k, _ in REQUIRED_SECTIONS:
        missing = required_missing_counts[k]
        present = len(entries) - missing
        print(f'  {k:<20}  present in {present}/{len(entries)}  (missing in {missing})')
    print()
    print(f'Entries with ALL required sections: {entries_with_all_required}/{len(entries)}')
    print(f'Entries missing ANY required:       {len(entries_with_any_required_missing)}/{len(entries)}')
    print()

    print('=== OPTIONAL section coverage ===')
    for k, _ in OPTIONAL_SECTIONS:
        missing = optional_missing_counts[k]
        present = len(entries) - missing
        print(f'  {k:<20}  present in {present}/{len(entries)}  (missing in {missing})')
    print()

    # Show 20 examples of incomplete entries
    if entries_with_any_required_missing:
        print('=== 20 sample entries missing required sections ===')
        for fn, missing in entries_with_any_required_missing[:20]:
            print(f'  {fn:<40}  missing: {", ".join(missing)}')


def write_report():
    slugs = sorted(l.strip() for l in open(SLUGS_FILE) if l.strip())
    pats = [(k, p) for k, p in REQUIRED_SECTIONS if k in REPORT_SECTIONS]
    rows = []
    counts = Counter()
    for slug in slugs:
        fp = f'docs/dictionary/{slug}.html'
        if not os.path.exists(fp):
            continue
        with open(fp, 'r', encoding='utf-8') as f:
            missing = check(f.read(), pats)
        if missing:
            rows.append((slug, missing))
            for k in missing:
                counts[k] += 1
    out = ['# Dictionary completeness audit', '',
           f'Audit of {len(slugs)} entries against three required sections:',
           '**Biblical Definition** · **Webster 1828** · **Modern Corruption**', '',
           'Run `python3 bin/audit_dict_completeness.py --write` to regenerate.', '',
           '| Section | Missing in |', '| --- | --- |']
    out += [f'| {k} | {counts[k]} |' for k in REPORT_SECTIONS]
    out += ['', '## Entries missing one or more required sections', '',
            '| Slug | Missing |', '| --- | --- |']
    out += [f'| {slug} | {", ".join(m)} |' for slug, m in rows]
    out += ['', f'**Total incomplete: {len(rows)} entries**', '']
    with open(REPORT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print(f'\nWrote {REPORT}: {len(rows)} incomplete of {len(slugs)} entries')


if __name__ == '__main__':
    main()
    if '--write' in sys.argv[1:]:
        write_report()
