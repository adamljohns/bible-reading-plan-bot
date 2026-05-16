#!/usr/bin/env python3
"""Backfill OpenGraph / Twitter / description meta tags on blog posts.

For each docs/blog/*.html missing OG tags, derive them from existing
content and inject before </head>:

  og:title       <- <title> (stripped of " — U.S.M.C. Ministries" suffix)
  og:description <- first <p> text content (first 200 chars)
  og:image       <- existing first <img src> OR site default
  og:url         <- https://usmcmin.org/blog/<filename>
  og:type        <- article
  twitter:card   <- summary_large_image
  twitter:title  <- same as og:title
  twitter:image  <- same as og:image
  description    <- same as og:description (for SEO)

Safe behavior:
  - Doesn't add a tag that already exists
  - Doesn't modify existing meta tags
  - Inserts new block before </head>
"""
import os
import re
import html as html_lib
import glob

SITE_BASE = 'https://usmcmin.org'
DEFAULT_OG_IMAGE = 'https://usmcmin.org/assets/og/og-main.png'

TITLE_RE = re.compile(r'<title>(.*?)</title>', re.IGNORECASE | re.DOTALL)
FIRST_P_RE = re.compile(r'<p[^>]*>(.*?)</p>', re.IGNORECASE | re.DOTALL)
FIRST_IMG_RE = re.compile(r'<img[^>]+src=["\']([^"\']+\.(?:jpg|jpeg|png|webp))["\']', re.IGNORECASE)
TAGS_STRIP = re.compile(r'<[^>]+>')

EXISTS_PATTERNS = {
    'og:title':       re.compile(r'<meta[^>]*(?:property|name)\s*=\s*["\']og:title["\']', re.IGNORECASE),
    'og:description': re.compile(r'<meta[^>]*(?:property|name)\s*=\s*["\']og:description["\']', re.IGNORECASE),
    'og:image':       re.compile(r'<meta[^>]*(?:property|name)\s*=\s*["\']og:image["\']', re.IGNORECASE),
    'og:url':         re.compile(r'<meta[^>]*(?:property|name)\s*=\s*["\']og:url["\']', re.IGNORECASE),
    'og:type':        re.compile(r'<meta[^>]*(?:property|name)\s*=\s*["\']og:type["\']', re.IGNORECASE),
    'twitter:card':   re.compile(r'<meta[^>]*(?:property|name)\s*=\s*["\']twitter:card["\']', re.IGNORECASE),
    'twitter:title':  re.compile(r'<meta[^>]*(?:property|name)\s*=\s*["\']twitter:title["\']', re.IGNORECASE),
    'twitter:image':  re.compile(r'<meta[^>]*(?:property|name)\s*=\s*["\']twitter:image["\']', re.IGNORECASE),
    'description':    re.compile(r'<meta[^>]*name\s*=\s*["\']description["\']', re.IGNORECASE),
}


def extract_title(html):
    m = TITLE_RE.search(html)
    if not m:
        return None
    t = html_lib.unescape(m.group(1).strip())
    # Strip the standard suffix
    for suffix in (' — U.S.M.C. Ministries', ' - U.S.M.C. Ministries', ' | USMC Ministries', ' | U.S.M.C. Ministries'):
        if t.endswith(suffix):
            t = t[:-len(suffix)].strip()
            break
    return t


def extract_first_paragraph(html):
    # Try to find the first <p> *inside* a div.content (skip nav, header, etc.)
    content_match = re.search(r'<div\s+class\s*=\s*["\']content["\'][^>]*>(.*?)</div>',
                              html, re.IGNORECASE | re.DOTALL)
    search_zone = content_match.group(1) if content_match else html
    for m in FIRST_P_RE.finditer(search_zone):
        text = TAGS_STRIP.sub(' ', m.group(1))
        text = html_lib.unescape(text)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) >= 30:
            return text
    return None


def extract_first_img(html, source_filename):
    """Return absolute URL of first sensible content <img>."""
    for m in FIRST_IMG_RE.finditer(html):
        src = m.group(1)
        # Skip icon-style decorative images
        if '/icons/' in src or '/favicon' in src:
            continue
        if src.startswith('http'):
            return src
        if src.startswith('/'):
            return SITE_BASE + src
        # Relative -> assume from blog/
        return SITE_BASE + '/blog/' + src
    return None


def truncate_for_meta(text, max_len=200):
    if len(text) <= max_len:
        return text
    cut = text[:max_len].rsplit(' ', 1)[0]
    return cut + '…'


def attr_escape(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


def main():
    posts = sorted(glob.glob('docs/blog/*.html'))
    patched = 0
    skipped = 0

    for fp in posts:
        with open(fp, 'r', encoding='utf-8') as f:
            html = f.read()
        if '</head>' not in html:
            skipped += 1
            continue

        title = extract_title(html) or 'Adam "MOOP" Johns'
        desc = extract_first_paragraph(html) or 'Faith, discipline, family, and mission. Writings from Adam "MOOP" Johns, U.S.M.C. Ministries.'
        desc = truncate_for_meta(desc, 200)
        img = extract_first_img(html, os.path.basename(fp)) or DEFAULT_OG_IMAGE
        url = f'{SITE_BASE}/blog/{os.path.basename(fp)}'

        # Build tags only for the ones that don't already exist
        new_tags = []
        candidates = [
            ('description',    f'<meta name="description" content="{attr_escape(desc)}">'),
            ('og:title',       f'<meta property="og:title" content="{attr_escape(title)}">'),
            ('og:description', f'<meta property="og:description" content="{attr_escape(desc)}">'),
            ('og:image',       f'<meta property="og:image" content="{attr_escape(img)}">'),
            ('og:url',         f'<meta property="og:url" content="{url}">'),
            ('og:type',        '<meta property="og:type" content="article">'),
            ('twitter:card',   '<meta name="twitter:card" content="summary_large_image">'),
            ('twitter:title',  f'<meta name="twitter:title" content="{attr_escape(title)}">'),
            ('twitter:image',  f'<meta name="twitter:image" content="{attr_escape(img)}">'),
        ]
        for tag_name, tag_html in candidates:
            if not EXISTS_PATTERNS[tag_name].search(html):
                new_tags.append(tag_html)

        if not new_tags:
            skipped += 1
            continue

        # Insert before </head>
        block = '    <!-- Open Graph / Twitter (backfilled) -->\n    ' + '\n    '.join(new_tags) + '\n'
        new_html = html.replace('</head>', block + '</head>', 1)

        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_html)
        patched += 1

    print(f'Patched {patched} blog posts ({skipped} had no work needed or no </head>)')


if __name__ == '__main__':
    main()
