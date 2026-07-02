#!/usr/bin/env python3
"""
Eliminate the dead/fragile bteToggleTheme function across lexicon pages. The nav
slider handles clicks via its own inline onclick; bteToggleTheme has no live
caller (45 pages call it from a load script where it throws on now-removed
elements). Remove every <script> containing it, then guarantee each page has
exactly the standard load IIFE (old-key read-fallback preserves saved prefs).

Usage: python3 eliminate_dead_fn.py [--apply]
"""
import glob, re, sys
APPLY = "--apply" in sys.argv

LOAD = ("<script>(function(){var s=localStorage.getItem('bte-theme')||"
        "localStorage.getItem('bteTheme')||localStorage.getItem('theme');"
        "if(s==='light')document.body.classList.add('light-mode');})();</script>")
SCRIPT_BLOCK = re.compile(r'[ \t]*<script\b[^>]*>.*?</script>\n?', re.S)
LOAD_PRESENT = re.compile(r"getItem\(['\"]bte-theme['\"]\)[^<]*light-mode|"
                          r"light-mode[^<]*getItem\(['\"]bte-theme['\"]\)", re.S)

def has_load(s):
    return bool(re.search(r"getItem\(['\"]bte-theme['\"]\)", s)) and \
           "classList.add('light-mode')" in s.replace('"', "'")

def fix(path):
    s = open(path, encoding="utf-8").read()
    if "function bteToggleTheme" not in s:
        return s, False
    assert not re.search(r'onclick="[^"]*bteToggleTheme\(\)', s), f"{path}: live onclick caller"
    # remove every <script> block that defines bteToggleTheme
    def _sub(m):
        return "" if "function bteToggleTheme" in m.group(0) else m.group(0)
    out = SCRIPT_BLOCK.sub(_sub, s)
    assert "function bteToggleTheme" not in out, f"{path}: fn survived"
    assert "bteToggleTheme" not in out, f"{path}: a bteToggleTheme reference remains"
    # ensure a load-time apply exists; if not, add the standard one before </body>
    if not has_load(out):
        assert out.count("</body>") == 1, f"{path}: no single </body> to anchor load script"
        out = out.replace("</body>", "    " + LOAD + "\n</body>", 1)
    assert has_load(out), f"{path}: load-time apply missing after fix"
    assert "nav-theme-toggle" in out, f"{path}: nav slider lost"
    assert out.count("<script") == out.count("</script>"), f"{path}: script tags unbalanced"
    return out, (out != s)

files = glob.glob("docs/lexicon/*.html")
to_write = {}
added_load = 0
for f in files:
    out, ch = fix(f)
    if ch:
        to_write[f] = out
print(f"lexicon pages: {len(files)} | pages cleaned of dead fn: {len(to_write)}")
# sanity: how many pages will end with the standard load IIFE vs already had one
if APPLY:
    for f, o in to_write.items():
        open(f, "w", encoding="utf-8").write(o)
    print(f"WROTE {len(to_write)} files.")
else:
    print("DRY RUN.")
