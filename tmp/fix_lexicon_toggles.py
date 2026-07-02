#!/usr/bin/env python3
"""
Repair the 2,933 lexicon pages whose theme <script> is broken (dangling else{
syntax error, load-only IIFE, or missing). All share the dot-slider button wired
to bteToggleTheme(). Fix: strip every (theme-only) <script> block and insert one
canonical dot-animating + migrating script before </body>.

Run with --apply to write; default dry-run.
"""
import glob, re, sys

APPLY = "--apply" in sys.argv

# Canonical script — identical to the one shipped to the 279 V1/V2 lexicon pages.
CANON = (
    "<script>\n"
    "        function bteToggleTheme(){\n"
    "            document.body.classList.toggle('light-mode');\n"
    "            localStorage.setItem('bte-theme', document.body.classList.contains('light-mode') ? 'light' : 'dark');\n"
    "            const dot = document.querySelector('.bte-theme-toggle div div');\n"
    "            if(dot) dot.style.left = document.body.classList.contains('light-mode') ? '16px' : '2px';\n"
    "        }\n"
    "        (function(){\n"
    "            var saved = localStorage.getItem('bte-theme');\n"
    "            if(saved === null){ saved = localStorage.getItem('bteTheme'); if(saved === null) saved = localStorage.getItem('theme'); if(saved !== null) localStorage.setItem('bte-theme', saved); }\n"
    "            if(saved === 'light'){\n"
    "                document.body.classList.add('light-mode');\n"
    "                const dot = document.querySelector('.bte-theme-toggle div div');\n"
    "                if(dot) dot.style.left = '16px';\n"
    "            }\n"
    "        })();\n"
    "    </script>"
)

SCRIPT_RE = re.compile(r"[ \t]*<script[^>]*>.*?</script>\n?", re.S)
BODY_RE = re.compile(r"</body>")

def is_theme(blk_inner):
    b = blk_inner.strip()
    return (b == "" or b.startswith("else{") or "bte-theme" in b or "bteToggleTheme" in b
            or "bteTheme" in b or ("light-mode" in b and "classList" in b)
            or re.search(r"getItem\(['\"]theme['\"]\)", b))

# Re-derive the dead set from scratch (don't trust a temp file).
dead = []
for f in glob.glob("docs/lexicon/*.html"):
    s = open(f, encoding="utf-8").read()
    if 'onclick="bteToggleTheme()"' in s and "function bteToggleTheme" not in s:
        dead.append(f)
dead.sort()
print(f"Dead pages re-derived: {len(dead)}")
assert len(dead) == 2933, f"ABORT: expected 2933, got {len(dead)}"

def transform(p):
    s = open(p, encoding="utf-8").read()
    orig = s
    # Safety: every <script> in this file must be theme-only (verified globally already).
    for m in re.finditer(r"<script[^>]*>(.*?)</script>", s, re.S):
        assert is_theme(m.group(1)), f"{p}: refusing to delete a NON-theme script"
    assert 'onclick="bteToggleTheme()"' in s, f"{p}: button onclick missing"
    assert s.count("</body>") == 1, f"{p}: expected exactly one </body>"
    # remove all script blocks
    s = SCRIPT_RE.sub("", s)
    assert "<script" not in s, f"{p}: a <script> survived removal"
    # insert canonical before </body>
    s = BODY_RE.sub("    " + CANON + "\n</body>", s, count=1)
    # post-conditions
    assert s.count("function bteToggleTheme") == 1, f"{p}: canonical fn not inserted once"
    assert s.count("<script>") == 1, f"{p}: not exactly one script after fix"
    assert "getItem('bte-theme')" in s, f"{p}: no bte-theme read"
    assert "setItem('bte-theme'" in s, f"{p}: no bte-theme write"
    assert 'onclick="bteToggleTheme()"' in s, f"{p}: button lost"
    assert s.count("</body>") == 1 and s.count("</html>") >= 1, f"{p}: body/html broken"
    assert s != orig
    return s

results = {}
for p in dead:
    results[p] = transform(p)
print(f"All {len(results)} transformed in-memory; assertions passed.")

if APPLY:
    for p, s in results.items():
        open(p, "w", encoding="utf-8").write(s)
    print(f"WROTE {len(results)} files.")
else:
    print("DRY RUN — re-run with --apply.")
