"""Export the Biblical Atlas figures as standalone, print-quality posters.

Each <section class="figure" id="..."> in docs/atlas.html holds one inline SVG.
Inline SVGs rely on the page for two things a standalone file lacks:
  1. the brand CSS custom properties (var(--gold) etc.) defined in :root, and
  2. a dark page background (the figures use light text).
This script extracts each figure's SVG, resolves the var() colors to hex,
adds an opaque dark background and a small site watermark, then writes:
  docs/assets/atlas/<id>.svg   — standalone vector poster (scales forever)
  docs/assets/atlas/<id>.png   — 2400px-wide raster (print/share), via rsvg-convert

Fonts: rsvg-convert renders via fontconfig/pango, so Playfair Display + Inter
must be installed locally for full fidelity (brew install --cask font-playfair-display
font-inter); otherwise pango falls back to the serif/sans fallbacks already in the
font-family lists.

Usage:  python3 scripts/export_atlas_posters.py
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "docs" / "atlas.html"
OUT = ROOT / "docs" / "assets" / "atlas"
PNG_WIDTH = 2400  # poster raster width in px

# Brand custom properties, mirrored from atlas.html :root
VARS = {
    "--bg": "#000000", "--bg-card": "#0e0e0e",
    "--gold": "#D4AF37", "--gold-light": "#F4D470",
    "--white": "#e8e8e8", "--gray": "#888888", "--gray-light": "#aaaaaa",
    "--border": "#333333",
    "--babylon": "#D4AF37", "--persia": "#9fb4c9", "--greece": "#c98f4b",
    "--rome": "#8a8f98", "--israel": "#c0726b", "--judah": "#D4AF37",
    "--j1": "#5BA8A0", "--j2": "#C98F4B", "--j3": "#A98BC5", "--j4": "#C0726B",
}

# HTML named entities used in the figures that are NOT predefined in XML/SVG.
# A standalone .svg is parsed as XML, so these must become literal Unicode
# (only &amp; &lt; &gt; &quot; &apos; are valid XML entities and are left alone).
HTML_ENTITIES = {
    "&ldquo;": "“", "&rdquo;": "”", "&lsquo;": "‘", "&rsquo;": "’",
    "&mdash;": "—", "&ndash;": "–", "&middot;": "·", "&hellip;": "…",
    "&rsaquo;": "›", "&lsaquo;": "‹", "&nbsp;": " ", "&times;": "×",
}


def normalize_entities(s: str) -> str:
    for ent, ch in HTML_ENTITIES.items():
        s = s.replace(ent, ch)
    return s


FIGURE_RE = re.compile(
    r'<section class="figure"[^>]*\bid="([^"]+)"[^>]*>(.*?)</section>', re.DOTALL)
SVG_RE = re.compile(r'(<svg\b.*?</svg>)', re.DOTALL)
H2_RE = re.compile(r'<h2>(.*?)</h2>', re.DOTALL)
VIEWBOX_RE = re.compile(r'viewBox="0 0 ([\d.]+) ([\d.]+)"')


def resolve_vars(svg: str) -> str:
    def sub(m):
        name = m.group(1).strip()
        return VARS.get(name, "#cccccc")
    return re.sub(r'var\(\s*(--[a-z0-9-]+)\s*\)', sub, svg)


def make_standalone(svg: str) -> str:
    svg = resolve_vars(svg)
    m = VIEWBOX_RE.search(svg)
    vbw, vbh = (float(m.group(1)), float(m.group(2))) if m else (1100.0, 600.0)
    # ensure the xmlns (inline HTML svg omits it) and strip the min-width style
    svg = re.sub(r'\sstyle="[^"]*"', '', svg, count=1)
    if "xmlns=" not in svg.split(">", 1)[0]:
        svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" ', 1)
    # opaque dark background as the first painted child + footer watermark
    bg = f'<rect x="0" y="0" width="{vbw:g}" height="{vbh:g}" fill="#0c0c0c"/>'
    mark = (f'<text x="{vbw/2:g}" y="{vbh-8:g}" text-anchor="middle" '
            f'font-family="Inter, Helvetica, Arial, sans-serif" font-size="11" '
            f'fill="#5a5340">usmcmin.org &middot; the MOOP Bible Translation Engine</text>')
    # insert bg right after the opening <svg ...> tag; watermark just before </svg>
    svg = re.sub(r'(<svg\b[^>]*>)', r'\1' + bg, svg, count=1)
    svg = svg.replace("</svg>", mark + "</svg>", 1)
    svg = normalize_entities(svg)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + svg


def main():
    html = ATLAS.read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    have_rsvg = subprocess.run(["which", "rsvg-convert"], capture_output=True).returncode == 0
    if not have_rsvg:
        print("WARN: rsvg-convert not found — will write .svg only (no .png).")
    figs = FIGURE_RE.findall(html)
    if not figs:
        print("No figures found."); sys.exit(1)
    for fid, body in figs:
        sm = SVG_RE.search(body)
        if not sm:
            print(f"  {fid}: no <svg> — skipped"); continue
        title = re.sub(r'<[^>]+>', '', H2_RE.search(body).group(1)).strip() if H2_RE.search(body) else fid
        standalone = make_standalone(sm.group(1))
        svg_path = OUT / f"{fid}.svg"
        svg_path.write_text(standalone, encoding="utf-8")
        line = f"  {fid:16s} \"{title}\"  -> {svg_path.relative_to(ROOT)}"
        if have_rsvg:
            png_path = OUT / f"{fid}.png"
            r = subprocess.run(
                ["rsvg-convert", "-w", str(PNG_WIDTH), "-b", "#0c0c0c", "-o", str(png_path), str(svg_path)],
                capture_output=True, text=True)
            if r.returncode == 0:
                kb = png_path.stat().st_size // 1024
                line += f" + {png_path.name} ({kb} KB)"
            else:
                line += f"  PNG FAILED: {r.stderr.strip()[:80]}"
        print(line)
    print(f"\nDone. Posters in {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
