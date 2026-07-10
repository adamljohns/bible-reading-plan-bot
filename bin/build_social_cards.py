#!/usr/bin/env python3
"""Generate consistent 1200x630 Open Graph section cards for usmcmin.org.

Run locally (requires Pillow). Generated PNGs are committed; CI does not run this.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
OUT = ASSETS / "og"
CREST = ASSETS / "usmc-crest-hero-2026.png"

CARDS = {
    "default": ("U.S.M.C.", "MINISTRIES", "Uniting · Serving · Mentoring · Counseling"),
    "bible": ("BIBLE", "TOOLS", "Translation · Reading Plans · Word Study"),
    "dictionary": ("MOOP", "DICTIONARY", "Biblical Definitions · Theology · Word Study"),
    "churches": ("CHURCH", "DIRECTORY", "Find Churches · Doctrine · Leadership"),
    "worship": ("WORSHIP", "& DEVOTION", "Songs · Scripture · Prayer"),
    "assessments": ("BIBLICAL", "ASSESSMENTS", "Husbands · Fathers · Citizens"),
    "blog": ("MINISTRY", "BLOG", "Faith · Family · Freedom · Fraternity"),
    "resources": ("MINISTRY", "RESOURCES", "Tools · Studies · Downloads"),
    "connect": ("CONNECT", "WITH US", "Mentoring · Counseling · Brotherhood"),
}

SERIF = "/System/Library/Fonts/NewYork.ttf"
SANS = "/System/Library/Fonts/Supplemental/Arial.ttf"
SANS_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def make_card(key: str, line1: str, line2: str, strap: str) -> Path:
    width, height = 1200, 630
    bg = Image.new("RGB", (width, height), (5, 6, 8)).convert("RGBA")

    # Restrained gold glow behind the redesigned crest.
    for radius in range(400, 40, -8):
        alpha = int(28 * (1 - radius / 400))
        layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.ellipse((245-radius, 315-radius, 245+radius, 315+radius),
                   fill=(212, 175, 55, alpha))
        bg = Image.alpha_composite(bg, layer)

    crest_src = Image.open(CREST).convert("RGB")
    scale = 570 / crest_src.height
    crest = crest_src.resize((round(crest_src.width * scale), 570), Image.Resampling.LANCZOS)
    crest = crest.filter(ImageFilter.UnsharpMask(radius=1.2, percent=115, threshold=3))
    bg.alpha_composite(crest.convert("RGBA"), (28, 30))

    draw = ImageDraw.Draw(bg)
    gold = (229, 190, 67, 255)
    white = (245, 245, 242, 255)
    gray = (176, 180, 188, 255)
    draw.line((490, 72, 490, 558), fill=(212, 175, 55, 150), width=2)

    title1 = ImageFont.truetype(SERIF, 60)
    title2 = ImageFont.truetype(SERIF, 58 if len(line2) < 12 else 50)
    strap_font = ImageFont.truetype(SANS_BOLD, 25)
    body_font = ImageFont.truetype(SANS, 22)
    url_font = ImageFont.truetype(SANS_BOLD, 21)

    x = 540
    draw.text((x, 120), line1, font=title1, fill=gold)
    draw.text((x, 192), line2, font=title2, fill=gold)
    draw.line((x, 275, 1130, 275), fill=(212, 175, 55, 210), width=2)
    draw.text((x, 320), strap, font=strap_font, fill=white)
    draw.text((x, 400), "Christ-centered tools for faith, family,", font=body_font, fill=gray)
    draw.text((x, 432), "freedom, and fraternity.", font=body_font, fill=gray)
    draw.rounded_rectangle((x, 505, 810, 557), radius=8, fill=(212, 175, 55, 255))
    draw.text((x + 24, 518), "usmcmin.org", font=url_font, fill=(7, 8, 10, 255))
    draw.rounded_rectangle((12, 12, width-13, height-13), radius=4,
                           outline=(212, 175, 55, 210), width=2)

    out = OUT / f"og-{key}-2026-07.png"
    bg.convert("RGB").save(out, optimize=True, quality=95)
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for key, values in CARDS.items():
        out = make_card(key, *values)
        print(f"{out.relative_to(ROOT)} — {Image.open(out).size} — {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
