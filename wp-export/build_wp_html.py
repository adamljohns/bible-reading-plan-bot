#!/usr/bin/env python3
"""
Convert usmcmin.org blog HTML files into clean WordPress-ready HTML.

Uses a balanced-div parser so nested divs (source-card → source-title) don't
cause the regex to over-match and eat content.
"""
import re
import os

POSTS = [
    ("the-dl-five-ds-five-ls.html",
     "The DL: Six D's That Kill a Dream (and Seven L's That Bring It Back)"),
    ("a-philosopher-diagnosed-the-problem-heres-what-hes-missing.html",
     "A Philosopher Diagnosed the Problem. Here's What He's Missing."),
    ("resolute-citizen-7580-candidates-all-50-states-one-standard.html",
     "RESOLUTE Citizen: 7,580 Candidates. All 50 States. One Standard."),
]

SRC_DIR = "/Users/adamjohns/bible-reading-plan-bot/docs/blog"
OUT_DIR = "/Users/adamjohns/bible-reading-plan-bot/wp-export"
SITE = "https://usmcmin.org"


def find_balanced_div(html: str, start: int) -> int:
    """Given index of an opening <div, return index after the matching </div>."""
    depth = 0
    i = start
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1
            # Skip to end of this opening tag
            close = html.find('>', i)
            if close == -1:
                return -1
            i = close + 1
        elif html[i:i+6] == '</div>':
            depth -= 1
            i += 6
            if depth == 0:
                return i
        else:
            i += 1
    return -1


def find_divs_with_class(html: str, class_name: str):
    """Yield (start, end, inner) tuples for each top-level div with the given class."""
    pattern = re.compile(r'<div\s+class="' + re.escape(class_name) + r'(?:\s[^"]*)?"[^>]*>')
    pos = 0
    while True:
        m = pattern.search(html, pos)
        if not m:
            break
        start = m.start()
        end = find_balanced_div(html, start)
        if end == -1:
            pos = m.end()
            continue
        # Inner content is between m.end() and end-6 (length of </div>)
        inner = html[m.end():end-6]
        yield (start, end, inner)
        pos = end


def replace_divs(html: str, class_name: str, replace_fn) -> str:
    """Replace all top-level divs with given class via replace_fn(inner) → str."""
    matches = list(find_divs_with_class(html, class_name))
    # Replace from the end backwards so indices stay valid
    for start, end, inner in reversed(matches):
        replacement = replace_fn(inner)
        html = html[:start] + replacement + html[end:]
    return html


# ── Replacement functions ──

def stage_card_to_h3(inner: str) -> str:
    num = re.search(r'class="stage-num">(\d+)<', inner)
    title = re.search(r'class="stage-title">(.*?)</div>', inner, re.DOTALL)
    sub = re.search(r'class="stage-sub">(.*?)</div>', inner, re.DOTALL)
    out = '<h3>'
    if num:
        out += f'{num.group(1)}. '
    if title:
        out += title.group(1).strip()
    out += '</h3>'
    if sub:
        out += f'<p><em>{sub.group(1).strip()}</em></p>'
    return out


def source_card_to_p(inner: str) -> str:
    title = re.search(r'class="source-title">(.*?)</div>', inner, re.DOTALL)
    author = re.search(r'class="source-author">(.*?)</div>', inner, re.DOTALL)
    out = '<p>'
    if title:
        out += f'<strong>{title.group(1).strip()}</strong>'
    if author:
        out += f'<br><em>{author.group(1).strip()}</em>'
    # Pick up any standalone link/timestamp from the inner content (outside the title/author divs)
    rest = inner
    if title:
        rest = rest.replace(title.group(0), '')
    if author:
        rest = rest.replace(author.group(0), '')
    extra_link = re.search(r'<a\s+href="([^"]+)"[^>]*>([^<]+)</a>', rest)
    if extra_link and 'class="timestamp"' not in extra_link.group(0):
        out += f' <a href="{extra_link.group(1)}">{extra_link.group(2)}</a>'
    out += '</p>'
    return out


def pattern_visual_to_p(inner: str) -> str:
    pills = re.findall(r'class="[dl]-pill">([^<]+)</span>', inner)
    labels = re.findall(r'class="pattern-label"[^>]*>([^<]+)</', inner)
    note = re.search(r'class="pattern-note">(.*?)</', inner, re.DOTALL)
    out = '<p>'
    if labels and len(pills) >= 6:
        d_pills = pills[:6]
        l_pills = pills[6:]
        out += f'<strong>{labels[0]}:</strong> ' + ' → '.join(d_pills)
        if len(labels) > 1 and l_pills:
            out += f'<br><strong>{labels[1]}:</strong> ' + ' · '.join(l_pills)
    else:
        out += ' → '.join(pills)
    out += '</p>'
    if note:
        out += f'<p><em>{note.group(1).strip()}</em></p>'
    return out


def cta_box_to_blockquote(inner: str) -> str:
    text = re.search(r'<p[^>]*>(.*?)</p>', inner, re.DOTALL)
    link = re.search(r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>', inner, re.DOTALL)
    out = '<blockquote>'
    if text:
        out += f'<p>{text.group(1).strip()}</p>'
    if link:
        out += f'<p><strong><a href="{link.group(1)}">{link.group(2).strip()}</a></strong></p>'
    out += '</blockquote>'
    return out


def category_legend_to_ol(inner: str) -> str:
    """Convert the RESOLUTE Citizen 7-category legend grid to an ordered list."""
    items = []
    for m in find_divs_with_class(inner, 'cat-item'):
        block = m[2]
        name = re.search(r'class="cat-name">([^<]+)<', block)
        desc = re.search(r'class="cat-desc">([^<]+)<', block)
        if name:
            line = f'<strong>{name.group(1).strip()}</strong>'
            if desc:
                line += f' &mdash; {desc.group(1).strip()}'
            items.append(line)
    if not items:
        return ''
    return '<ol>\n' + '\n'.join(f'  <li>{it}</li>' for it in items) + '\n</ol>'


def modules_grid_to_ul(inner: str) -> str:
    """Convert the 3-module grid to a simple list."""
    items = []
    for m in find_divs_with_class(inner, 'module-card'):
        block = m[2]
        name = re.search(r'class="module-name">([^<]+)<', block)
        desc = re.search(r'class="module-desc">([^<]+)<', block)
        # Find the parent <a href= if present (we have inner only, look for href in raw)
        href = re.search(r'href="([^"]+)"', block)
        if name:
            line = f'<strong>{name.group(1).strip()}</strong>'
            if desc:
                line += f' &mdash; {desc.group(1).strip()}'
            items.append(line)
    if not items:
        return ''
    return '<ul>\n' + '\n'.join(f'  <li>{it}</li>' for it in items) + '\n</ul>'


def scorecard_demo_to_p(inner: str) -> str:
    """Convert the RESOLUTE Citizen scorecard table demo to a simple list of links."""
    rows = []
    # Find each <a class="sc-candidate" ...> entry
    pattern = re.compile(r'<a\s+href="([^"]+)"\s+class="sc-candidate"[^>]*>(.*?)</a>', re.DOTALL)
    for m in pattern.finditer(inner):
        href = m.group(1)
        body = m.group(2)
        name = re.search(r'class="name">([^<]+)<', body)
        office = re.search(r'class="office">([^<]+)<', body)
        total = re.search(r'class="sc-total[^"]*">([^<]+)<', body)
        if name:
            line = f'<a href="{href}"><strong>{name.group(1).strip()}</strong></a>'
            if office:
                line += f' &mdash; {office.group(1).strip()}'
            if total:
                line += f' &mdash; <strong>{total.group(1).strip()}</strong>'
            rows.append(line)
    if not rows:
        return '<p><em>(See live scorecard at <a href="https://usmcmin.com/citizen.html">usmcmin.com/citizen.html</a>)</em></p>'
    return '<p><strong>Sample from the live scorecard (Virginia local officials):</strong></p>\n<ul>\n' + '\n'.join(f'  <li>{r}</li>' for r in rows) + '\n</ul>'


def profile_card_to_h3(inner: str) -> str:
    """Convert candidate profile cards to compact summaries."""
    juris = re.search(r'class="jurisdiction">([^<]+)<', inner)
    name = re.search(r'class="candidate-name">([^<]+)<', inner)
    score_num = re.search(r'class="profile-score-num[^"]*">([^<]+)<', inner)
    score_max = re.search(r'class="profile-score-max">([^<]+)<', inner)
    bio_p = re.search(r'<p[^>]*>([^<]+(?:<[^/][^>]*>[^<]*</[^>]+>[^<]*)*)</p>', inner)
    link = re.search(r'class="profile-link"[^>]*href="([^"]+)"', inner)

    out = '<h3>'
    if name:
        out += name.group(1).strip()
    if juris:
        out += f' <em>({juris.group(1).strip()})</em>'
    out += '</h3>\n'
    if score_num and score_max:
        out += f'<p><strong>Score: {score_num.group(1).strip()}{score_max.group(1).strip()}</strong></p>\n'
    if bio_p:
        out += f'<p>{bio_p.group(1).strip()}</p>\n'
    if link:
        out += f'<p><a href="{link.group(1)}">View Full Profile &amp; Sources →</a></p>'
    return out


def howto_steps_to_ol(inner: str) -> str:
    items = []
    for m in find_divs_with_class(inner, 'howto-step'):
        block = m[2]
        text = re.search(r'<p[^>]*>(.*?)</p>', block, re.DOTALL)
        if text:
            items.append(text.group(1).strip())
    if not items:
        return ''
    return '<ol>\n' + '\n'.join(f'  <li>{it}</li>' for it in items) + '\n</ol>'


# ── Pipeline ──

def rewrite_links(content: str) -> str:
    content = re.sub(r'href="(/[^"]+)"', rf'href="{SITE}\1"', content)
    content = re.sub(r'src="(/[^"]+)"', rf'src="{SITE}\1"', content)
    return content


def remove_first_h1_and_byline(content: str) -> str:
    content = re.sub(r'<div class="meta">.*?</div>', '', content, count=1, flags=re.DOTALL)
    content = re.sub(r'<div class="byline">.*?</div>', '', content, count=1, flags=re.DOTALL)
    content = re.sub(r'<h1[^>]*>.*?</h1>', '', content, count=1, flags=re.DOTALL)
    return content


def clean_attributes(content: str) -> str:
    """Strip class and inline style attributes for WordPress compatibility."""
    content = re.sub(r'\s+style="[^"]*"', '', content)
    content = re.sub(r'\s+class="[^"]*"', '', content)
    # Remove sup.fn class footnote links — but keep them as plain superscripts
    content = re.sub(r'<sup>\s*<a([^>]*?)>(\d+)</a>\s*</sup>', r'<sup><a\1>\2</a></sup>', content)
    return content


def collapse_whitespace(content: str) -> str:
    content = re.sub(r'\n[ \t]*\n[ \t]*\n+', '\n\n', content)
    content = re.sub(r'^\s+', '', content, flags=re.MULTILINE)
    return content.strip()


def convert(slug, title):
    src_path = os.path.join(SRC_DIR, slug)
    with open(src_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract article body
    m = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
    if not m:
        raise ValueError(f"No <article> in {slug}")
    article = m.group(1)

    # Apply transformations using balanced div replacement
    article = replace_divs(article, 'stage-card d-stage', stage_card_to_h3)
    article = replace_divs(article, 'stage-card l-stage', stage_card_to_h3)
    article = replace_divs(article, 'source-card', source_card_to_p)
    article = replace_divs(article, 'pattern-visual', pattern_visual_to_p)
    article = replace_divs(article, 'cta-box', cta_box_to_blockquote)
    article = replace_divs(article, 'category-legend', category_legend_to_ol)
    article = replace_divs(article, 'modules-grid', modules_grid_to_ul)
    article = replace_divs(article, 'scorecard-demo', scorecard_demo_to_p)
    article = replace_divs(article, 'profile-card', profile_card_to_h3)
    article = replace_divs(article, 'howto-steps', howto_steps_to_ol)

    article = remove_first_h1_and_byline(article)
    article = clean_attributes(article)
    article = rewrite_links(article)
    article = collapse_whitespace(article)

    out_path = os.path.join(OUT_DIR, slug.replace('.html', '.wp.html'))
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f'<!-- Title: {title} -->\n')
        f.write(f'<!-- Source: {SITE}/blog/{slug} -->\n')
        f.write('<!-- Paste this into the WordPress Gutenberg "Custom HTML" block, or switch to Code Editor mode. -->\n\n')
        f.write(article)
    print(f"  ✓ {os.path.basename(out_path)} ({len(article):,} chars)")
    return out_path


if __name__ == "__main__":
    print(f"Converting {len(POSTS)} posts to WordPress-ready HTML...\n")
    for slug, title in POSTS:
        convert(slug, title)
    print(f"\nOutput directory: {OUT_DIR}")
