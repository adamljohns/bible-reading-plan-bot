#!/usr/bin/env python3
"""Backfill OpenGraph / Twitter / description meta tags on dictionary entries.

Same pattern as backfill_blog_og_tags.py, tuned for dictionary entries:

  og:title       <- <title> ("WORD — The MOOP Dictionary" -> "WORD")
  og:description <- "<word>: <biblical_def first sentence>"
  og:image       <- /assets/blog/blog-foster-cathedral.png (site default)
                    (dict entries rarely have inline images)
  og:url         <- https://usmcmin.org/dictionary/<filename>
  og:type        <- article
  twitter:card   <- summary
  description    <- same as og:description (for SEO snippets)
"""
import os
import re
import html as html_lib
import glob

SITE_BASE = 'https://usmcmin.org'
DEFAULT_OG_IMAGE = 'https://usmcmin.org/assets/icons/icon-512.png'

TITLE_RE = re.compile(r'<title>(.*?)</title>', re.IGNORECASE | re.DOTALL)
WORD_TITLE_RE = re.compile(r'<div\s+class\s*=\s*["\']word-title["\'][^>]*>(.*?)</div>', re.IGNORECASE | re.DOTALL)
BIBLICAL_DEF_RE = re.compile(
    r'<h[1-6][^>]*>(?:[^<]*)?Biblical (?:Definition|Meaning)(?:[^<]*)?</h[1-6]>(.*?)(?:<h[1-6]|<div\s+class\s*=\s*["\']section)',
    re.IGNORECASE | re.DOTALL,
)
TAGS_STRIP = re.compile(r'<[^>]+>')

EXISTS_PATTERNS = {
    'og:title':       re.compile(r'<meta[^>]*(?:property|name)\s*=\s*["\']og:title["\']', re.IGNORECASE),
    'og:description': re.compile(r'<meta[^>]*(?:property|name)\s*=\s*["\']og:description["\']', re.IGNORECASE),
    'og:image':       re.compile(r'<meta[^>]*(?:property|name)\s*=\s*["\']og:image["\']', re.IGNORECASE),
    'og:url':         re.compile(r'<meta[^>]*(?:property|name)\s*=\s*["\']og:url["\']', re.IGNORECASE),
    'og:type':        re.compile(r'<meta[^>]*(?:property|name)\s*=\s*["\']og:type["\']', re.IGNORECASE),
    'twitter:card':   re.compile(r'<meta[^>]*(?:property|name)\s*=\s*["\']twitter:card["\']', re.IGNORECASE),
    'description':    re.compile(r'<meta[^>]*name\s*=\s*["\']description["\']', re.IGNORECASE),
}


def extract_word(html):
    """Extract the word being defined."""
    m = WORD_TITLE_RE.search(html)
    if m:
        return html_lib.unescape(TAGS_STRIP.sub('', m.group(1))).strip()
    # Fallback: parse from <title>
    m = TITLE_RE.search(html)
    if not m:
        return None
    t = html_lib.unescape(m.group(1).strip())
    for suffix in (' — The MOOP Dictionary', ' - The MOOP Dictionary', ' — U.S.M.C. Ministries',
                   ' | MOOP Dictionary', ' — MOOP Dictionary'):
        if t.endswith(suffix):
            t = t[:-len(suffix)].strip()
            break
    return t


def extract_description(html, word):
    """Get the first sentence of Biblical Definition for the description."""
    m = BIBLICAL_DEF_RE.search(html)
    if not m:
        return f'{word} — Biblical definition from The MOOP Dictionary at usmcmin.org.'
    text = TAGS_STRIP.sub(' ', m.group(1))
    text = html_lib.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    # Take first sentence or first 200 chars
    if not text:
        return f'{word} — entry in The MOOP Dictionary.'
    first_sentence_match = re.search(r'^.+?[.!?](?:\s|$)', text)
    if first_sentence_match:
        first = first_sentence_match.group(0).strip()
        if len(first) > 30:
            return truncate(f'{word}: {first}', 240)
    return truncate(f'{word}: {text}', 240)


def truncate(text, max_len=240):
    if len(text) <= max_len:
        return text
    cut = text[:max_len].rsplit(' ', 1)[0]
    return cut + '…'


def attr_escape(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


def main():
    entries = sorted(glob.glob('docs/dictionary/*.html'))
    entries = [e for e in entries if os.path.basename(e) not in ('index.html', 'names.html')]
    print(f'Processing {len(entries)} dictionary entries')
    patched = 0

    for fp in entries:
        with open(fp, 'r', encoding='utf-8') as f:
            html = f.read()
        if '</head>' not in html:
            continue

        word = extract_word(html) or 'Entry'
        desc = extract_description(html, word)
        url = f'{SITE_BASE}/dictionary/{os.path.basename(fp)}'
        title = f'{word} — The MOOP Dictionary'

        candidates = [
            ('description',    f'<meta name="description" content="{attr_escape(desc)}">'),
            ('og:title',       f'<meta property="og:title" content="{attr_escape(title)}">'),
            ('og:description', f'<meta property="og:description" content="{attr_escape(desc)}">'),
            ('og:image',       f'<meta property="og:image" content="{DEFAULT_OG_IMAGE}">'),
            ('og:url',         f'<meta property="og:url" content="{url}">'),
            ('og:type',        '<meta property="og:type" content="article">'),
            ('twitter:card',   '<meta name="twitter:card" content="summary">'),
            ('twitter:title',  f'<meta name="twitter:title" content="{attr_escape(title)}">'),
            ('twitter:image',  f'<meta name="twitter:image" content="{DEFAULT_OG_IMAGE}">'),
        ]
        new_tags = []
        for tag_name, tag_html in candidates:
            check_key = tag_name if tag_name in EXISTS_PATTERNS else tag_name.replace('twitter:title', 'twitter:card').replace('twitter:image', 'twitter:card')
            pat = EXISTS_PATTERNS.get(tag_name)
            if pat and pat.search(html):
                continue
            new_tags.append(tag_html)

        if not new_tags:
            continue

        block = '    <!-- Open Graph / Twitter (auto-generated) -->\n    ' + '\n    '.join(new_tags) + '\n'
        new_html = html.replace('</head>', block + '</head>', 1)

        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_html)
        patched += 1

    print(f'Patched {patched} dictionary entries')


if __name__ == '__main__':
    main()
