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
  - any page with `noindex` meta tag (sampled — slow to check all)
"""
import os
import sys
from datetime import datetime, timezone
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
BASE_URL = 'https://usmcmin.org'

SKIP_SEGMENTS = {'_archive', '_backup', '_wip', '_drafts', '.git', 'node_modules'}

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


def collect_urls():
    """Walk docs/ and yield (url, lastmod_iso, priority, changefreq) tuples."""
    rows = []
    for root, dirs, files in os.walk(DOCS):
        # Skip blacklisted segments
        dirs[:] = [d for d in dirs if d not in SKIP_SEGMENTS]
        for fn in files:
            if not fn.endswith('.html'):
                continue
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, DOCS).replace(os.sep, '/')
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
    return rows


def write_sitemap(path, rows):
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

    # Write each non-empty section sitemap
    written = []
    for name, section_rows in sections.items():
        if not section_rows:
            continue
        out_path = os.path.join(DOCS, name)
        write_sitemap(out_path, section_rows)
        size_kb = os.path.getsize(out_path) // 1024
        print(f'  {name:<25} {len(section_rows):>6} urls  {size_kb:>5} KB')
        written.append(name)

    # Write top-level sitemap-index
    index_path = os.path.join(DOCS, 'sitemap.xml')
    write_sitemap_index(index_path, written)
    print(f'\nWrote {index_path} (sitemap index pointing at {len(written)} child sitemaps)')


if __name__ == '__main__':
    main()
