#!/usr/bin/env python3
"""
Add load-time theme application to the 9 themed lexicon pages that have the
redesign's nav toggle (click works) but no load-time read, so a returning
visitor's saved light-mode applies on load. Purely additive: insert one load
IIFE before </body>, matching the redesign's working-page pattern. Read-only
to everything else.
"""
import glob, re, sys
APPLY = "--apply" in sys.argv

LOAD = "<script>(function(){if(localStorage.getItem('bte-theme')==='light')document.body.classList.add('light-mode');})();</script>"

A = []
for f in glob.glob("docs/lexicon/*.html"):
    s = open(f, encoding="utf-8").read()
    has_load = bool(re.search(r"getItem\(['\"]bte-theme['\"]\)", s)) and "light-mode" in s
    if not has_load and "nav-theme-toggle" in s:
        A.append(f)
A.sort()
print(f"group-A pages (nav toggle, no load-time): {len(A)}")
assert len(A) == 9, f"ABORT: expected 9, got {len(A)}"

results = {}
for f in A:
    s = open(f, encoding="utf-8").read()
    assert s.count("</body>") == 1, f"{f}: not exactly one </body>"
    assert "getItem('bte-theme')" not in s and 'getItem("bte-theme")' not in s, f"{f}: already has load read"
    out = s.replace("</body>", "    " + LOAD + "\n</body>", 1)
    # post-conditions
    assert out.count("getItem('bte-theme')") == 1, f"{f}: load read not added once"
    assert "document.body.classList.add('light-mode')" in out
    assert out != s
    results[f] = out

print("all transformed; assertions passed.")
if APPLY:
    for f, s in results.items():
        open(f, "w", encoding="utf-8").write(s)
    print(f"WROTE {len(results)} files:", [f.split('/')[-1] for f in results])
else:
    print("DRY RUN.")
