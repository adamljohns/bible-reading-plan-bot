#!/usr/bin/env python3
"""Fail-closed: every public theme toggle must load the custom tomb/cross icons.

The house chrome is light-icons.css: gold-cross shield (dark) and bronze empty
tomb (bright). New blog posts have shipped twice with the old moon/sun pill
because they omitted that stylesheet. This audit blocks that regression.

A page BREACHES when it carries a theme toggle and does not load
/assets/css/light-icons.css. Markup may still contain 🌙/☀️ fallbacks; the
stylesheet hides those children and paints the custom shields.

Usage:
  python3 bin/check_theme_toggle_icons.py
  python3 bin/check_theme_toggle_icons.py --root docs
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

TOGGLE_MARKERS = (
    "bte-theme-toggle",
    'class="theme-toggle"',
    "id=\"themeToggle\"",
    "id='themeToggle'",
)
CSS_GUARD = "light-icons.css"
SKIP_DIRS = {".git", "node_modules"}


def has_toggle(html: str) -> bool:
    return any(marker in html for marker in TOGGLE_MARKERS)


def audit(root: Path) -> list[str]:
    breaches: list[str] = []
    for path in sorted(root.rglob("*.html")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        if has_toggle(html) and CSS_GUARD not in html:
            breaches.append(str(path.relative_to(root)))
    return breaches


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="docs")
    args = parser.parse_args()
    root = Path(args.root)
    if not root.is_dir():
        print(f"ERROR: {root} is not a directory", file=sys.stderr)
        return 2
    breaches = audit(root)
    if breaches:
        print(f"FAIL: {len(breaches)} theme toggle(s) missing {CSS_GUARD}:")
        for rel in breaches:
            print(f"  {rel}")
        print("Fix: python3 bin/add_blog_light_mode.py  (blog posts)")
        print("     or add  <link rel=\"stylesheet\" href=\"/assets/css/light-icons.css\">")
        return 1
    print(f"PASS: every theme toggle under {root} loads {CSS_GUARD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
