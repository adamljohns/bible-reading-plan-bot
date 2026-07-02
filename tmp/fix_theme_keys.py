#!/usr/bin/env python3
"""
Unify theme localStorage key onto 'bte-theme' across the 378 lexicon/assessment
pages still on 'theme' or 'bteTheme', repair the 227 dead V1 toggles and the 52
corrupted V2 buttons. Deterministic, per-variant, fails loudly on any surprise.

Run with --apply to write; default is dry-run (classify + assert only).
"""
import subprocess, re, sys, os

ROOT = "/Users/moop_bot_pro/bible-reading-plan-bot"
APPLY = "--apply" in sys.argv

def grep_l(pattern, path):
    out = subprocess.run(["grep", "-rl", pattern, path, "--include=*.html"],
                         capture_output=True, text=True)
    return set(l for l in out.stdout.split("\n") if l)

# ---- Build the full off-key file universe ----
universe = grep_l(r"localStorage.\(getItem\|setItem\)('theme')", os.path.join(ROOT, "docs")) \
         | grep_l(r"localStorage.\(getItem\|setItem\)('bteTheme')", os.path.join(ROOT, "docs"))
universe = sorted(universe)

def read(p):  return open(p, encoding="utf-8").read()

def is_lex(p): return "/docs/lexicon/" in p

# ---- Classify each file into exactly one variant ----
buckets = {f"V{i}": [] for i in range(1, 6)}
unclassified = []
for p in universe:
    s = read(p)
    has_set_bteTheme = "localStorage.setItem('bteTheme'" in s
    has_set_theme    = "localStorage.setItem('theme'" in s
    has_def          = "function bteToggleTheme" in s
    has_dotbtn       = '<div class="bte-theme-toggle"' in s
    has_btn_onclick  = 'onclick="bteToggleTheme()"' in s
    has_themeToggle_el = 'id="themeToggle"' in s
    has_inline_set   = "onclick=\"document.body.classList.toggle('light-mode');localStorage.setItem('theme'," in s

    if not is_lex(p) and has_set_bteTheme:
        buckets["V5"].append(p)
    elif is_lex(p) and has_set_bteTheme:
        buckets["V2"].append(p)
    elif is_lex(p) and has_btn_onclick and not has_def and not has_set_theme and not has_set_bteTheme:
        buckets["V1"].append(p)
    elif is_lex(p) and has_inline_set:
        buckets["V3"].append(p)
    elif is_lex(p) and has_themeToggle_el and "function toggle()" in s and has_set_theme:
        buckets["V4"].append(p)
    else:
        unclassified.append(p)

print("=== Classification ===")
for k in ["V1","V2","V3","V4","V5"]:
    print(f"  {k}: {len(buckets[k])}")
print(f"  UNCLASSIFIED: {len(unclassified)}")
for u in unclassified[:20]: print("     ?", u)

total = sum(len(v) for v in buckets.values())
assert len(unclassified) == 0, "ABORT: unclassified files present"
assert total == len(universe) == 378, f"ABORT: total {total} / universe {len(universe)} != 378"
# disjointness
allf = [p for v in buckets.values() for p in v]
assert len(allf) == len(set(allf)), "ABORT: a file landed in 2 buckets"
print(f"  TOTAL {total} == 378  ✓  (disjoint ✓)")

# ===================== Canonical fragments =====================
CANON_SCRIPT = (
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

# Correct dot-slider button (matches V1's working button) to restore V2's corrupted one.
CANON_BUTTON = (
    "    </nav>\n"
    "    <div style=\"text-align:center;margin:24px auto 10px;\">\n"
    "        <div class=\"bte-theme-toggle\" onclick=\"bteToggleTheme()\" title=\"Toggle dark/light mode\" style=\"display:inline-flex;align-items:center;background:rgba(30,30,30,0.85);border:1px solid #333;border-radius:20px;padding:3px 6px;cursor:pointer;font-size:0.7rem;\">\n"
    "            <span style=\"width:18px;text-align:center;\">\U0001F319</span>\n"
    "            <div style=\"width:28px;height:14px;background:#444;border-radius:7px;position:relative;margin:0 4px;\"><div style=\"width:10px;height:10px;background:#D4AF37;border-radius:50%;position:absolute;top:2px;left:2px;transition:left 0.3s;\"></div></div>\n"
    "            <span style=\"width:18px;text-align:center;\">☀️</span>\n"
    "        </div>\n"
    "    </div>\n"
    "    <div class=\"container\">"
)
# Whitespace-tolerant matcher for V2's corrupted button fragment.
V2_CORRUPT_RE = re.compile(
    r"</nav>\s*</div>\s*<span style=\"width:18px;text-align:center;\">☀️</span>\s*</div>\s*<div class=\"container\">"
)

SCRIPT_RE = re.compile(r"<script>.*?</script>", re.S)

MIG_EXPR = ("(function(){var s=localStorage.getItem('bte-theme');"
            "if(s===null){s=localStorage.getItem('theme');"
            "if(s!==null)localStorage.setItem('bte-theme',s);}return s;})()")

# V3 exact strings
V3_OLD_ONCLICK_SET = "localStorage.setItem('theme',document.body.classList.contains('light-mode')?'light':'dark')"
V3_NEW_ONCLICK_SET = "localStorage.setItem('bte-theme',document.body.classList.contains('light-mode')?'light':'dark')"
V3_OLD_SCRIPT = "<script>if(localStorage.getItem('theme')==='light')document.body.classList.add('light-mode');</script>"
V3_NEW_SCRIPT = ("<script>(function(){var s=localStorage.getItem('bte-theme');"
                 "if(s===null){s=localStorage.getItem('theme');if(s!==null)localStorage.setItem('bte-theme',s);}"
                 "if(s==='light')document.body.classList.add('light-mode');})();</script>")

# V4 exact strings
V4_OLD_READ = "const saved = localStorage.getItem('theme');"
V4_NEW_READ = "const saved = " + MIG_EXPR + ";"
V4_OLD_SET = "localStorage.setItem('theme',isLight?'light':'dark')"
V4_NEW_SET = "localStorage.setItem('bte-theme',isLight?'light':'dark')"

# V5 strings
V5_OLD_SET = "localStorage.setItem('bteTheme'"
V5_NEW_SET = "localStorage.setItem('bte-theme'"
V5_MIG_EXPR = ("(function(){var s=localStorage.getItem('bte-theme');"
               "if(s===null){s=localStorage.getItem('bteTheme');"
               "if(s!==null)localStorage.setItem('bte-theme',s);}return s;})()")
V5_OLD_GET = "localStorage.getItem('bteTheme')"

# ===================== Transform per variant =====================
def transform(p, variant):
    s = read(p)
    orig = s
    if variant in ("V1", "V2"):
        assert len(SCRIPT_RE.findall(s)) == 1, f"{p}: expected exactly 1 <script> block"
        s = SCRIPT_RE.sub(lambda m: CANON_SCRIPT, s, count=1)
        if variant == "V2":
            assert len(V2_CORRUPT_RE.findall(s)) == 1, f"{p}: V2 corrupt-button fragment not found exactly once"
            s = V2_CORRUPT_RE.sub(lambda m: CANON_BUTTON, s, count=1)
    elif variant == "V3":
        assert s.count(V3_OLD_ONCLICK_SET) == 1, f"{p}: V3 onclick setItem not found"
        assert s.count(V3_OLD_SCRIPT) == 1, f"{p}: V3 script not found"
        s = s.replace(V3_OLD_ONCLICK_SET, V3_NEW_ONCLICK_SET).replace(V3_OLD_SCRIPT, V3_NEW_SCRIPT)
    elif variant == "V4":
        assert s.count(V4_OLD_READ) == 1, f"{p}: V4 read line not found"
        assert s.count(V4_OLD_SET) == 1, f"{p}: V4 setItem not found"
        s = s.replace(V4_OLD_READ, V4_NEW_READ).replace(V4_OLD_SET, V4_NEW_SET)
    elif variant == "V5":
        assert s.count(V5_OLD_SET) == 1, f"{p}: V5 setItem not found"
        assert s.count(V5_OLD_GET) == 1, f"{p}: V5 getItem not found once"
        s = s.replace(V5_OLD_SET, V5_NEW_SET).replace(V5_OLD_GET, V5_MIG_EXPR)

    # ---- post-conditions for this file ----
    assert "setItem('theme'" not in s, f"{p}: still writes 'theme'"
    assert "setItem('bteTheme'" not in s, f"{p}: still writes 'bteTheme'"
    assert "setItem('bte-theme'" in s, f"{p}: no bte-theme write after fix"
    # every page must read bte-theme (with migration fallback)
    assert "getItem('bte-theme')" in s, f"{p}: does not read bte-theme"
    # V1/V2 must now define the toggle
    if variant in ("V1","V2"):
        assert "function bteToggleTheme" in s, f"{p}: toggle fn missing after fix"
    assert s != orig, f"{p}: no change made"
    return s

# dry-run: transform everything in memory to surface assertion failures
results = {}
for variant in ["V1","V2","V3","V4","V5"]:
    for p in buckets[variant]:
        results[p] = transform(p, variant)
print(f"\n=== All {len(results)} files transformed in-memory with assertions passing ===")

if APPLY:
    for p, s in results.items():
        open(p, "w", encoding="utf-8").write(s)
    print(f"WROTE {len(results)} files.")
else:
    print("DRY RUN — no files written. Re-run with --apply.")
