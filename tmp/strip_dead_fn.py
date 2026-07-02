#!/usr/bin/env python3
"""
Strip the dead `function bteToggleTheme(){...}` (0 callers after old-button
removal) from lexicon pages, preserving the essential load-time IIFE in the same
<script>. String-aware brace matching; per-page assertion that load-time theme
application survives. Aborts (dry-run) on any anomaly.

Usage: python3 strip_dead_fn.py [--apply]
"""
import glob, re, sys
APPLY = "--apply" in sys.argv

def match_brace(s, open_idx):
    """Return index just past the matching } for the { at open_idx, string-aware."""
    depth = 0; i = open_idx; q = None
    while i < len(s):
        c = s[i]
        if q:
            if c == '\\': i += 2; continue
            if c == q: q = None
        elif c in "'\"`": q = c
        elif c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0: return i + 1
        i += 1
    return -1

def strip(path):
    s = open(path, encoding="utf-8").read()
    if "function bteToggleTheme" not in s:
        return s, False
    assert not re.search(r'onclick="[^"]*bteToggleTheme\(\)', s), f"{path}: has a live caller"
    had_load = bool(re.search(r"getItem\(['\"]bte-theme['\"]\)", s)) and "light-mode" in s
    out = s
    while "function bteToggleTheme" in out:
        idx = out.index("function bteToggleTheme")
        brace = out.index("{", idx)
        end = match_brace(out, brace)
        assert end != -1, f"{path}: unbalanced fn braces"
        start = idx
        while start > 0 and out[start-1] in " \t": start -= 1
        e = end
        while e < len(out) and out[e] in " \t": e += 1
        if e < len(out) and out[e] == "\n": e += 1
        out = out[:start] + out[e:]
    # assertions: dead fn gone, no caller, load-time preserved, script still closed
    assert "function bteToggleTheme" not in out, f"{path}: fn survived"
    assert "bteToggleTheme(" not in out, f"{path}: a bteToggleTheme reference remains"
    if had_load:
        assert re.search(r"getItem\(['\"]bte-theme['\"]\)", out) and "light-mode" in out, \
            f"{path}: load-time apply was destroyed!"
    assert out.count("<script") == out.count("</script>"), f"{path}: script tags unbalanced"
    # nav slider must remain
    assert "nav-theme-toggle" in out, f"{path}: nav slider lost"
    return out, (out != s)

files = glob.glob("docs/lexicon/*.html")
changed = 0; to_write = {}
for f in files:
    out, ch = strip(f)
    if ch:
        to_write[f] = out; changed += 1
print(f"lexicon pages: {len(files)} | dead fn stripped from: {changed}")
if APPLY:
    for f, o in to_write.items():
        open(f, "w", encoding="utf-8").write(o)
    print(f"WROTE {len(to_write)} files.")
else:
    print("DRY RUN.")
