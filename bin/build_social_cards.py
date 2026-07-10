#!/usr/bin/env python3
"""Generate section-specific 1200x630 Open Graph cards for usmcmin.org.

Each major surface gets its own hero mark for share-preview variety:
- Homepage keeps the main U.S.M.C. Ministries crest
- Bible/BTE/verse pages use the BTE lighthouse hero
- Lexicon, Dictionary, Cross-Refs, Worship, etc. use their page heroes
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
OUT = ASSETS / "og"
VERSION = "2026-07-10"

SERIF = "/System/Library/Fonts/NewYork.ttf"
SANS = "/System/Library/Fonts/Supplemental/Arial.ttf"
SANS_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

# (filename_key, title_line1, title_line2, strap, hero_relpath, mark_style)
# mark_style: "full" for tall crests, "badge" for shield icons
CARDS = [
    (
        "bible",
        "MOOP BIBLE",
        "TRANSLATION ENGINE",
        "12 Translations · Interlinear · Strong's · Cross-Refs",
        "images/usmc-emblem-shield-t2026.png",
        "badge",
    ),
    (
        "lexicon",
        "MOOP",
        "LEXICON",
        "Hebrew · Greek · Strong's · Original Roots",
        "icons/shield-alpha-omega-hires.png",
        "badge",
    ),
    (
        "dictionary",
        "MOOP",
        "DICTIONARY",
        "Biblical Definitions · Theology · Word Study",
        "icons/shield-book-greek-48.png",
        "badge",
    ),
    (
        "crossrefs",
        "SCRIPTURE",
        "CROSS-REFERENCES",
        "Verse Links · Themes · Study Paths",
        "icons/shield-infinity-rope-96.png",
        "badge",
    ),
    (
        "atlas",
        "BIBLICAL",
        "ATLAS",
        "Maps · Charts · Journey Overviews",
        "icons/shield-map-hires.png",
        "badge",
    ),
    (
        "churches",
        "CHURCH",
        "DIRECTORY",
        "Find Churches · Doctrine · Leadership",
        "icons/shield-church-hires.png",
        "badge",
    ),
    (
        "worship",
        "WORSHIP",
        "& DEVOTION",
        "Songs · Scripture · Prayer",
        "icons/shield-quill-note-96.png",
        "badge",
    ),
    (
        "assessments",
        "BIBLICAL",
        "ASSESSMENTS",
        "Husbands · Fathers · Citizens",
        "icons/shield-checklist-hires.png",
        "badge",
    ),
    (
        "blog",
        "MINISTRY",
        "BLOG",
        "Faith · Family · Freedom · Fraternity",
        "icons/shield-blog-quill-hires.png",
        "badge",
    ),
    (
        "resources",
        "MINISTRY",
        "RESOURCES",
        "Tools · Studies · Downloads",
        "icons/shield-open-book-96.png",
        "badge",
    ),
    (
        "connect",
        "CONNECT",
        "WITH US",
        "Mentoring · Counseling · Brotherhood",
        "icons/shield-handshake.png",
        "badge",
    ),
    (
        "default",
        "U.S.M.C.",
        "MINISTRIES",
        "Uniting · Serving · Mentoring · Counseling",
        "usmc-crest-hero-2026.png",
        "full",
    ),
]


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def fit_mark(src: Image.Image, target_h: int, style: str) -> Image.Image:
    im = src.convert("RGBA")
    # Prefer the largest useful mark without stretching.
    scale = target_h / im.height
    if style == "full":
        # Tall crest: keep generous height on the left panel.
        scale = min(scale, 520 / im.width)
    else:
        # Badge/icon: larger centered mark.
        scale = min(max(scale, 1.0), 4.8)
        # If source is tiny, upscale hard but keep it clean.
        if im.height < 180:
            scale = target_h / im.height
    new = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.Resampling.LANCZOS)
    if style == "badge" and im.height < 300:
        new = new.filter(ImageFilter.UnsharpMask(radius=1.4, percent=130, threshold=2))
    else:
        new = new.filter(ImageFilter.UnsharpMask(radius=1.1, percent=110, threshold=3))
    return new


def make_card(key: str, line1: str, line2: str, strap: str, hero_rel: str, style: str) -> Path:
    width, height = 1200, 630
    bg = Image.new("RGBA", (width, height), (5, 6, 8, 255))

    # Soft gold glow on the left mark panel.
    for radius in range(360, 40, -10):
        alpha = int(26 * (1 - radius / 360))
        layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        ImageDraw.Draw(layer).ellipse(
            (250 - radius, 315 - radius, 250 + radius, 315 + radius),
            fill=(212, 175, 55, alpha),
        )
        bg = Image.alpha_composite(bg, layer)

    hero_path = ASSETS / hero_rel
    if not hero_path.exists():
        raise FileNotFoundError(hero_path)

    mark = fit_mark(Image.open(hero_path), 470 if style == "full" else 360, style)
    mx = max(20, (470 - mark.width) // 2)
    my = max(20, (height - mark.height) // 2)
    bg.alpha_composite(mark, (mx, my))

    draw = ImageDraw.Draw(bg)
    gold = (229, 190, 67, 255)
    white = (245, 245, 242, 255)
    gray = (176, 180, 188, 255)

    # Divider between mark and copy.
    draw.line((500, 70, 500, 560), fill=(212, 175, 55, 150), width=2)

    # Title sizing adapts to long second lines.
    t1 = load_font(SERIF, 54 if len(line1) > 12 else 60)
    t2_size = 48 if len(line2) > 16 else (52 if len(line2) > 12 else 58)
    t2 = load_font(SERIF, t2_size)
    strap_font = load_font(SANS_BOLD, 22 if len(strap) > 42 else 24)
    body_font = load_font(SANS, 22)
    url_font = load_font(SANS_BOLD, 21)

    x = 545
    draw.text((x, 108), line1, font=t1, fill=gold)
    draw.text((x, 180), line2, font=t2, fill=gold)
    draw.line((x, 268, 1140, 268), fill=(212, 175, 55, 210), width=2)
    draw.text((x, 310), strap, font=strap_font, fill=white)
    draw.text((x, 390), "Christ-centered tools for faith, family,", font=body_font, fill=gray)
    draw.text((x, 422), "freedom, and fraternity.", font=body_font, fill=gray)
    draw.rounded_rectangle((x, 500, 820, 552), radius=8, fill=(212, 175, 55, 255))
    draw.text((x + 24, 513), "usmcmin.org", font=url_font, fill=(7, 8, 10, 255))
    draw.rounded_rectangle((12, 12, width - 13, height - 13), radius=4, outline=(212, 175, 55, 210), width=2)

    out = OUT / f"og-{key}-{VERSION}.png"
    bg.convert("RGB").save(out, optimize=True)
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for item in CARDS:
        out = make_card(*item)
        im = Image.open(out)
        print(f"{out.relative_to(ROOT)} — {im.size} — {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
