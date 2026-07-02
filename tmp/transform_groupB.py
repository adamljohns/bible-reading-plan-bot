#!/usr/bin/env python3
"""
Bring the 100 group-B lexicon pages (old black-bg, no-nav template) onto the
standard template: nav + slider + theme CSS + word-header + sections + footer +
load-time script. Reuses the canonical blocks from a clean standard page (H986).
Content (badge/orig/trans/pos/gloss + sections) is copied from each group-B page.

Usage: python3 transform_groupB.py [--apply]
"""
import glob, re, sys, html

APPLY = "--apply" in sys.argv
SKEL = "docs/lexicon/H986.html"
sk = open(SKEL, encoding="utf-8").read()

# --- extract canonical reusable blocks from the skeleton ---
STYLE = re.search(r'<style>.*?</style>', sk, re.S).group(0)
NAV   = re.search(r'<nav>.*?</nav>', sk, re.S).group(0)
FOOTER= re.search(r'<footer>.*?</footer>', sk, re.S).group(0)
SCRIPT= re.search(r'<script>\(function\(\)\{if\(localStorage\.getItem\([^\n]*</script>', sk).group(0)
HEADICONS = (
    '    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">\n'
    '    <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">\n'
    '    <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">\n'
    '    <link rel="manifest" href="/manifest.json">\n'
)
FONTS = (
    '    <link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">\n'
)

def field(s, cls):
    m = re.search(rf'<div class="{cls}">(.*?)</div>', s, re.S)
    return m.group(1).strip() if m else ""

def attr(x):  # safe for an HTML attribute value
    return html.escape(html.unescape(x), quote=True)

def transform(path):
    s = open(path, encoding="utf-8").read()
    sid = path.split("/")[-1][:-5]
    badge = re.search(r'<span class="badge">(.*?)</span>', s, re.S).group(1).strip()
    orig  = field(s, "orig")
    trans = field(s, "trans")
    pos   = field(s, "pos")
    gloss = field(s, "gloss")
    lang  = "Greek" if sid.startswith("G") else "Hebrew"
    # sections: identical .section>h2+p structure — copy verbatim, re-indented
    sections = re.findall(r'<div class="section">.*?</div>', s, re.S)
    assert sections, f"{path}: no sections"
    sec_html = "\n\n        ".join(re.sub(r'\s+', ' ', x).replace('> <', '>\n            <').strip()
                                   for x in sections)
    # rebuild each section cleanly: <div class="section"><h2>..</h2><p>..</p>..</div>
    secs = []
    for x in sections:
        h2 = re.search(r'<h2>(.*?)</h2>', x, re.S).group(1).strip()
        ps = re.findall(r'<p>(.*?)</p>', x, re.S)
        body = "\n            ".join(f"<p>{p.strip()}</p>" for p in ps)
        secs.append(f'<div class="section">\n            <h2>{h2}</h2>\n            {body}\n        </div>')
    sections_block = "\n\n        ".join(secs)

    title = f"{sid} — {trans} ({gloss}) | USMC Ministries Lexicon"
    desc  = f"{gloss} — {lang} word study. Strong's {sid}. USMC Ministries Greek & Hebrew Lexicon."

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="canonical" href="https://usmcmin.org/lexicon/{sid}.html">
{HEADICONS}    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="{attr(f'{sid} — {trans}')} | USMC Ministries Lexicon">
    <meta property="og:description" content="{attr(desc)}">
    <meta name="description" content="{attr(desc)}">
    <title>{html.escape(title)}</title>
{FONTS}    {STYLE}
    <link rel="stylesheet" href="/assets/css/light-icons.css">
</head>
<body>
    {NAV}
    <div class="container">
        <a href="../lexicon.html" class="back-link">← Back to Lexicon</a>

        <div class="word-header">
            <span class="strongs-badge">{badge}</span>
            <div class="original-word">{orig}</div>
            <div class="transliteration">{trans}</div>
            <div class="pos">{pos}</div>
            <div class="gloss">{gloss}</div>
        </div>

        {sections_block}
    </div>
    {FOOTER}
{SCRIPT}
</body>
</html>
"""
    # assertions
    assert "nav-theme-toggle" in page
    assert page.count("<title>") == 1
    assert orig and trans and gloss, f"{path}: missing core fields"
    assert "getItem('bte-theme')" in page
    assert "class=\"container\"" in page
    return page

gb = [f for f in glob.glob("docs/lexicon/*.html") if "<nav>" not in open(f, encoding="utf-8").read()]
gb.sort()
print(f"group-B pages: {len(gb)}")
out = {f: transform(f) for f in gb}
print(f"transformed {len(out)} in-memory; assertions passed.")
print("\n--- sample (G2307) head+header ---")
print(out["docs/lexicon/G2307.html"][:200] if "docs/lexicon/G2307.html" in out else "n/a")
if APPLY:
    for f, p in out.items():
        open(f, "w", encoding="utf-8").write(p)
    print(f"\nWROTE {len(out)} files.")
else:
    print("\nDRY RUN.")
