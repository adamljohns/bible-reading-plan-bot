#!/usr/bin/env python3
"""Sweep all dictionary entry HTML files to fix the disclosure UX:
  1. Replace the buggy JS that hides the section-summary on expand
     with a label-toggling JS that swaps "expand to see more" ↔ "show less".
  2. Replace grey browser-default disclosure markers with custom yellow
     triangles (▼ rotated 90° when collapsed, 0° when open).

Operates idempotently: runs the new patterns whether the file has the old
JS, the new JS, or any mix. Files without a recognizable details summary
are left alone.
"""
import os, re, sys

DICT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        'docs', 'dictionary')

# === The buggy JS pattern (any whitespace tolerance) ============
OLD_JS_PAT = re.compile(
    r"document\.querySelectorAll\('details'\)\.forEach\(function\(d\)\{\s*"
    r"d\.addEventListener\('toggle',\s*function\(\)\{\s*"
    r"var sum = d\.previousElementSibling;\s*"
    r"if\(sum && sum\.classList\.contains\('section-summary'\)\)\{\s*"
    r"sum\.style\.display = d\.open \? 'none' : '';\s*"
    r"\}\s*\}\);\s*\}\);",
    re.DOTALL
)

NEW_JS = """document.querySelectorAll('details').forEach(function(d){
        var label = d.querySelector('summary em');
        if(!label) return;
        var update = function(){
            label.textContent = d.open ? 'show less' : 'expand to see more';
        };
        update();
        d.addEventListener('toggle', update);
    });"""

# === Old details summary CSS (no marker styling) ================
OLD_CSS_PAT = re.compile(
    r"details\s*\{\s*margin-top:8px;\s*\}\s*"
    r"details summary\s*\{\s*color:var\(--gold\);\s*font-size:0\.85rem;\s*cursor:pointer;\s*user-select:none;\s*padding:4px 0;\s*\}\s*"
    r"details summary:hover\s*\{\s*color:var\(--gold-light\);\s*\}\s*"
    r"details\[open\] summary\s*\{\s*margin-bottom:8px;\s*\}"
)

NEW_CSS = """details { margin-top:8px; }
        details summary { color:var(--gold); font-size:0.85rem; cursor:pointer; user-select:none; padding:4px 0;
                          list-style:none; display:inline-flex; align-items:center; gap:8px; }
        details summary::-webkit-details-marker { display:none; }
        details summary::before {
            content:""; display:inline-block; width:0; height:0;
            border-left:5px solid transparent; border-right:5px solid transparent;
            border-top:7px solid var(--gold);
            transition:transform 0.18s ease;
            transform:rotate(-90deg);
        }
        details[open] summary::before { transform:rotate(0deg); }
        details summary:hover { color:var(--gold-light); }
        details summary:hover::before { border-top-color:var(--gold-light); }
        details[open] summary { margin-bottom:8px; }"""

# === Older Gen-Z template (uses --gen-light instead of --gold) ===
OLD_GENZ_CSS_PAT = re.compile(
    r"details\s*\{\s*margin-top:8px;\s*\}\s*"
    r"details summary\s*\{\s*color:var\(--gen-light\);\s*font-size:0\.85rem;\s*cursor:pointer;\s*user-select:none;\s*padding:4px 0;\s*\}\s*"
    r"details summary:hover\s*\{\s*color:var\(--gen\);\s*\}\s*"
    r"details\[open\] summary\s*\{\s*margin-bottom:8px;\s*\}"
)

NEW_GENZ_CSS = """details { margin-top:8px; }
        details summary { color:var(--gen-light); font-size:0.85rem; cursor:pointer; user-select:none; padding:4px 0;
                          list-style:none; display:inline-flex; align-items:center; gap:8px; }
        details summary::-webkit-details-marker { display:none; }
        details summary::before {
            content:""; display:inline-block; width:0; height:0;
            border-left:5px solid transparent; border-right:5px solid transparent;
            border-top:7px solid var(--gen-light);
            transition:transform 0.18s ease;
            transform:rotate(-90deg);
        }
        details[open] summary::before { transform:rotate(0deg); }
        details summary:hover { color:var(--gen); }
        details summary:hover::before { border-top-color:var(--gen); }
        details[open] summary { margin-bottom:8px; }"""


NEW_JS_MARKER = 'label.textContent = d.open'
INJECT_PAT = re.compile(r'(\s*)</script>\s*</body>', re.DOTALL)


def fix_file(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()

    changed = False
    new_html, n = OLD_JS_PAT.subn(NEW_JS, html, count=1)
    if n:
        html = new_html
        changed = True

    new_html, n = OLD_CSS_PAT.subn(NEW_CSS, html, count=1)
    if n:
        html = new_html
        changed = True

    new_html, n = OLD_GENZ_CSS_PAT.subn(NEW_GENZ_CSS, html, count=1)
    if n:
        html = new_html
        changed = True

    # Fallback: entry has <details> + 'expand to see more' but no toggle JS yet.
    if (NEW_JS_MARKER not in html
            and '<details>' in html
            and 'expand to see more' in html):
        inject_js = ('document.querySelectorAll(\'details\').forEach(function(d){'
                     'var label=d.querySelector(\'summary em\');'
                     'if(!label)return;'
                     'var update=function(){label.textContent=d.open?\'show less\':\'expand to see more\';};'
                     'update();d.addEventListener(\'toggle\',update);});')
        m = INJECT_PAT.search(html)
        if m:
            html = html[:m.start()] + inject_js + html[m.start():]
            changed = True
        elif '</body>' in html:
            # No <script> tag at all — wrap in a fresh one before </body>.
            inject = '<script>' + inject_js + '</script>'
            html = html.replace('</body>', inject + '\n</body>', 1)
            changed = True

    if changed:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(html)
    return changed


def main():
    n_files = 0
    n_changed = 0
    for fn in sorted(os.listdir(DICT_DIR)):
        if not fn.endswith('.html') or fn in ('index.html', 'template.html'):
            continue
        fp = os.path.join(DICT_DIR, fn)
        n_files += 1
        if fix_file(fp):
            n_changed += 1
    print(f"Scanned {n_files} files; modified {n_changed}")


if __name__ == '__main__':
    main()
