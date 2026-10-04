#!/usr/bin/env python3
"""Bring lexicon entry pages toward the dictionary family (CID MBP-1004-CRAWL).
Pure string replacement of template CSS/markup; no entry content is touched. Idempotent."""
import sys,glob,re,collections
NAV_OLD = re.compile(r'<a href="\.\./index\.html">Home</a>\s*<a href="\.\./bible\.html">Bible Translation Engine</a>\s*<a href="\.\./lexicon\.html" (?:class="active"|style="color:#D4AF37;border:1px solid #D4AF37;border-radius:20px;padding:5px 12px;")>Lexicon</a>\s*<a href="\.\./blog\.html">Blog</a>\s*<a href="\.\./connect\.html">Connect</a>')
NAV_NEW = '''<a href="../index.html"><img src="../assets/icons/shield-home-48.png" class="site-icon" alt="" width="16" height="16"> Home</a>
        <a href="../watchman.html"><img src="../assets/icons/shield-bible.png" class="site-icon" alt="" width="16" height="16"> Watchman</a>
        <a href="../bible.html"><img src="../assets/icons/shield-bible-cross-48.png" class="site-icon" alt="" width="16" height="16"> BTE</a>
        <a href="../lexicon.html" class="active"><img src="../assets/icons/shield-alpha-omega-48.png" class="site-icon" alt="" width="16" height="16"> Lexicon</a>
        <a href="../cross-references.html"><img src="../assets/icons/shield-infinity-rope-48.png" class="site-icon" alt="" width="16" height="16"> Cross-Refs</a>
        <a href="../dictionary/index.html"><img src="../assets/icons/shield-book-greek-48.png" class="site-icon" alt="" width="16" height="16"> Dictionary</a>
        <a href="../blog.html"><img src="../assets/icons/shield-scroll-quill-48.png" class="site-icon" alt="" width="16" height="16"> Blog</a>
        <a href="../connect.html"><img src="../assets/icons/shield-handshake.png" class="site-icon" alt="" width="16" height="16"> Connect</a>'''
CSS = [
 # nav: same rule the dictionary index uses (icon + label inline)
 ('nav a { color:var(--gray); text-decoration:none; font-size:0.85rem; font-weight:500; padding:5px 12px; border-radius:20px; border:1px solid transparent; transition:all 0.2s; white-space:nowrap; }',
  'nav a { color:var(--gray); text-decoration:none; font-size:0.85rem; font-weight:500; padding:5px 12px; border-radius:20px; border:1px solid transparent; transition:all 0.2s; white-space:nowrap; display:inline-flex; align-items:center; gap:4px; }\n        .site-icon { vertical-align:middle; opacity:0.8; }\n        @media (max-width:640px) { nav { gap:4px 6px; padding:10px 12px; } nav a { padding:3px 7px; font-size:0.8rem; } }'),
 # container: dictionary width and padding
 ('.container { max-width:800px; margin:0 auto; padding:20px; }',
  '.container { max-width:820px; margin:0 auto; padding:28px 20px 60px; }'),
 ('@media (max-width:640px) { .container { padding:15px; } .original-word { font-size:2.2rem; } }',
  '@media (max-width:640px) { .original-word { font-size:2.2rem; } }'),
 # cards: dictionary radius, padding and rhythm
 ('.section { background:var(--bg-card); border:1px solid var(--border); border-radius:12px; padding:28px; margin-bottom:24px; }',
  '.section { background:var(--bg-card); border:1px solid var(--border); border-radius:10px; padding:18px 22px; margin:18px 0; }\n        .section p a:not([class]) { color:var(--gold); }'),
 ('.section h2 { color:var(--gold); font-size:1.3rem; margin-bottom:16px; }',
  '.section h2 { color:var(--gold); font-size:1.15rem; margin-bottom:12px; }'),
 # verse links: dictionary style (gold, semibold, underline on hover only)
 ('.verse-ref { color:var(--gold); text-decoration:none; font-weight:600; font-size:0.9rem; display:inline-block; margin-bottom:4px; border-bottom:1px dotted var(--gold); }',
  '.verse-ref { color:var(--gold); text-decoration:none; font-weight:600; font-size:0.9rem; display:inline-block; margin-bottom:4px; }'),
 ('.verse-ref:hover { color:var(--gold-light); border-bottom-style:solid; }',
  '.verse-ref:hover { color:var(--gold-light); text-decoration:underline; }'),
 # back link: centred with a rule, like the dictionary's "Back to Dictionary"
 ('.back-link { display:inline-block; color:var(--gold); text-decoration:none; margin-bottom:20px; font-size:0.9rem; }',
  '.back-link { display:block; text-align:center; color:var(--gold); text-decoration:none; margin-bottom:22px; padding:10px 0; border-bottom:1px solid var(--border); font-size:0.88rem; font-weight:500; }'),
]
def transform(s, stats=None):
    if 'http-equiv="refresh"' in s: return s
    out = s
    if 'class="site-icon"' not in out.split('</nav>')[0]:
        out, n = NAV_OLD.subn(NAV_NEW, out, count=1)
        if stats is not None: stats['nav'] += n
    for i,(a,b) in enumerate(CSS):
        if a in out and b not in out:
            out = out.replace(a, b, 1)
            if stats is not None: stats['css%d'%i] += 1
    return out
if __name__ == '__main__':
    files = sys.argv[1:]
    stats = collections.Counter(); changed = 0
    for p in files:
        s = open(p, encoding='utf-8').read(); t = transform(s, stats)
        if t != s:
            open(p, 'w', encoding='utf-8').write(t); changed += 1
    print('files', len(files), 'changed', changed, dict(stats))
