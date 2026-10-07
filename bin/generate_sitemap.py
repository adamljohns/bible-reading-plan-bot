#!/usr/bin/env python3
"""Generate sitemap.xml for usmcmin.org.

Walks docs/, writes one entry per .html page. Splits into a sitemap-index
+ multiple sub-sitemaps when total URL count exceeds 45,000 (Google's
50K-per-file limit, with headroom).

Priority heuristic by location:
  /                       1.0  (home + indices)
  /blog/                  0.8
  /dictionary/            0.6
  /lexicon/               0.5
  /churches/              0.5
  /chapters/, /verse/     0.4

Excludes:
  - _archive/, _backup/, _wip/  paths
  - .git/, node_modules/        if any
  - any page whose HTML contains a noindex robots meta tag
"""
import os
import re
import subprocess
import sys
from urllib.parse import unquote
from datetime import datetime, timezone
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
BASE_URL = 'https://usmcmin.org'

SKIP_SEGMENTS = {'_archive', '_backup', '_wip', '_drafts', '.git', 'node_modules'}

# PIN-theater / family-ops pages: listed on sitemap.html as Private, not for crawlers.
SKIP_FILES = {
    'lexicon-template.html',  # source for rebuild-lexicon.py; lexicon.html is the page (2026-10-06)
    'workflows.html',
    'tacc.html',
    'first-officer.html',
    'crew-quarters.html',
    'family-meeting.html',
    'contacts.html',
    'brand-assets.html',
    'dev-resources.html',
    # PIN-gated pages found in sitemap-main.xml 2026-10-03 (MBP-1003-NIGHT freshness).
    'ops-status.html',
    'psa-roster.html',
    'chores-boaz.html',
    'chores-gideon.html',
    'chores-shiloh.html',
    'tax-prep.html',
    'drive-map.html',
    'account-map.html',  # also noindex now; family financial account map
}

PRIORITY_BY_PREFIX = [
    ('blog/',       '0.8',   'weekly'),
    ('dictionary/', '0.6',   'monthly'),
    ('lexicon/',    '0.5',   'monthly'),
    ('churches/',   '0.5',   'monthly'),
    ('chapters/',   '0.4',   'monthly'),
    ('verse/',      '0.4',   'monthly'),
    ('readings/',   '0.4',   'monthly'),
    ('proverbs/',   '0.6',   'monthly'),
    ('freedom/',    '0.5',   'monthly'),
    ('lbcf/',       '0.5',   'monthly'),
    ('slides/',     '0.5',   'monthly'),
]


def priority_and_freq(rel_path):
    """Return (priority, changefreq) for a rel path under docs/."""
    if '/' not in rel_path:
        # Top-level (e.g. index.html, blog.html)
        if rel_path == 'index.html':
            return ('1.0', 'weekly')
        return ('0.9', 'weekly')
    for prefix, prio, freq in PRIORITY_BY_PREFIX:
        if rel_path.startswith(prefix):
            return (prio, freq)
    return ('0.5', 'monthly')


def _redirected_slugs():
    reg = os.path.join(os.path.dirname(__file__), '..', 'data', 'dictionary-redirects.txt')
    if os.path.exists(reg):
        return {l.split('->')[0].strip() for l in open(reg) if '->' in l}
    return set()


def _has_noindex(full_path):
    """True if page declares noindex or is a meta-refresh redirect stub
    (skip sitemap — avoids crawl conflicts). Refresh stubs added 2026-10-04:
    wheelhouse, consulting, husband-course, usmc-ministries were listed."""
    try:
        with open(full_path, encoding='utf-8', errors='ignore') as f:
            head = f.read(4096).lower()
        return 'noindex' in head or 'http-equiv="refresh"' in head
    except OSError:
        return False


def collect_urls():
    """Walk docs/ and yield (url, lastmod_iso, priority, changefreq) tuples."""
    redirected = _redirected_slugs()
    rows = []
    skipped_noindex = 0
    for root, dirs, files in os.walk(DOCS):
        # Skip blacklisted segments
        dirs[:] = [d for d in dirs if d not in SKIP_SEGMENTS]
        for fn in files:
            if not fn.endswith('.html'):
                continue
            if fn in SKIP_FILES:
                continue
            full = os.path.join(root, fn)
            if _has_noindex(full):
                skipped_noindex += 1
                continue
            rel = os.path.relpath(full, DOCS).replace(os.sep, '/')
            # Skip merged-away dictionary entries — they are no-index redirect stubs
            if rel.startswith('dictionary/') and rel[len('dictionary/'):-5] in redirected:
                continue
            url_path = rel
            # Map index.html to its dir
            if url_path == 'index.html':
                url = BASE_URL + '/'
            elif url_path.endswith('/index.html'):
                url = BASE_URL + '/' + url_path[:-len('index.html')]
            else:
                url = BASE_URL + '/' + url_path
            mtime = datetime.fromtimestamp(os.path.getmtime(full), tz=timezone.utc)
            lastmod = mtime.strftime('%Y-%m-%d')
            prio, freq = priority_and_freq(rel)
            rows.append((url, lastmod, prio, freq))
    if skipped_noindex:
        print(f'Skipped {skipped_noindex} noindex pages')
    return rows


def _tracked_absent_docs():
    """Paths under docs/ that git tracks but that are not on disk.

    In a sparse worktree (overnight workers check out only docs/dictionary etc.)
    every blog/main page is tracked-but-absent. Walking docs/ alone would drop
    all of them from the sitemaps (2026-10-06: 37k main URLs and the whole
    sitemap-blog.xml lost in one run). Returns None when git is unavailable.
    """
    try:
        out = subprocess.run(['git', '-C', ROOT, 'ls-files', '-z', '--', 'docs'],
                             capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    absent = set()
    for rel in out.decode('utf-8', 'surrogateescape').split('\0'):
        if rel.endswith('.html') and not os.path.exists(os.path.join(ROOT, rel)):
            absent.add(rel[len('docs/'):])
    return absent


def _url_to_rel(url):
    path = unquote(url[len(BASE_URL):].lstrip('/'))
    if path == '' or path.endswith('/'):
        path += 'index.html'
    return path


_URL_BLOCK = re.compile(r'<url>.*?</url>', re.S)
_LOC = re.compile(r'<loc>(.*?)</loc>', re.S)


def _carried_blocks(path, new_urls, absent):
    """Existing <url> blocks in `path` that this run would drop although their
    page is still tracked in git (just not checked out). Kept verbatim."""
    if not os.path.exists(path):
        return []
    keep = []
    for block in _URL_BLOCK.findall(open(path, encoding='utf-8').read()):
        m = _LOC.search(block)
        if not m:
            continue
        url = m.group(1).strip().replace('&amp;', '&')
        if url not in new_urls and _url_to_rel(url) in absent:
            keep.append(block)
    return keep


def write_sitemap(path, rows, carried=()):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url, lastmod, prio, freq in rows:
            f.write('  <url>\n')
            f.write(f'    <loc>{escape(url)}</loc>\n')
            f.write(f'    <lastmod>{lastmod}</lastmod>\n')
            f.write(f'    <changefreq>{freq}</changefreq>\n')
            f.write(f'    <priority>{prio}</priority>\n')
            f.write('  </url>\n')
        for block in carried:
            f.write('  ' + block + '\n')
        f.write('</urlset>\n')


def write_sitemap_index(path, sitemap_paths):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        today = datetime.now(tz=timezone.utc).strftime('%Y-%m-%d')
        for sp in sitemap_paths:
            url = f'{BASE_URL}/{sp}'
            f.write('  <sitemap>\n')
            f.write(f'    <loc>{escape(url)}</loc>\n')
            f.write(f'    <lastmod>{today}</lastmod>\n')
            f.write('  </sitemap>\n')
        f.write('</sitemapindex>\n')


def main():
    print('Collecting URLs...')
    rows = collect_urls()
    print(f'Found {len(rows)} HTML pages')

    # Group by section for split sitemaps
    sections = {
        'sitemap-main.xml':       [],
        'sitemap-blog.xml':       [],
        'sitemap-dictionary.xml': [],
        'sitemap-lexicon.xml':    [],
        'sitemap-churches.xml':   [],
        'sitemap-chapters.xml':   [],
    }
    for row in rows:
        url = row[0]
        url_path = url[len(BASE_URL):].lstrip('/')
        if url_path.startswith('blog/'):
            sections['sitemap-blog.xml'].append(row)
        elif url_path.startswith('dictionary/'):
            sections['sitemap-dictionary.xml'].append(row)
        elif url_path.startswith('lexicon/'):
            sections['sitemap-lexicon.xml'].append(row)
        elif url_path.startswith('churches/'):
            sections['sitemap-churches.xml'].append(row)
        elif url_path.startswith('chapters/') or url_path.startswith('verse/'):
            sections['sitemap-chapters.xml'].append(row)
        else:
            sections['sitemap-main.xml'].append(row)

    # Sparse-checkout guard: never drop a URL whose page git still tracks.
    absent = _tracked_absent_docs()
    if absent is None:
        print('WARNING: git unavailable; sparse-checkout guard is off', file=sys.stderr)
        absent = set()
    elif absent:
        print(f'Sparse checkout: {len(absent)} tracked pages not on disk; '
              'their existing sitemap rows are carried forward')

    # Write each non-empty section sitemap
    written = []
    carried_total = 0
    for name, section_rows in sections.items():
        out_path = os.path.join(DOCS, name)
        carried = _carried_blocks(out_path, {r[0] for r in section_rows}, absent)
        if not section_rows and not carried:
            continue
        write_sitemap(out_path, section_rows, carried)
        carried_total += len(carried)
        size_kb = os.path.getsize(out_path) // 1024
        extra = f'  (+{len(carried)} carried, not checked out)' if carried else ''
        print(f'  {name:<25} {len(section_rows) + len(carried):>6} urls  {size_kb:>5} KB{extra}')
        written.append(name)

    # Keep any child sitemap the current index lists that this generator does
    # not own (worship, confessions, lbcf, institutes ...) so the index never
    # loses one.
    index_path = os.path.join(DOCS, 'sitemap.xml')
    if os.path.exists(index_path):
        for loc in _LOC.findall(open(index_path, encoding='utf-8').read()):
            child = loc.strip()[len(BASE_URL):].lstrip('/')
            if child not in written and os.path.exists(os.path.join(DOCS, child)):
                written.append(child)
                print(f'  {child:<25} kept in index (not generated here)')

    # Write top-level sitemap-index
    write_sitemap_index(index_path, written)
    print(f'\nWrote {index_path} (sitemap index pointing at {len(written)} child sitemaps)')


if __name__ == '__main__':
    main()
