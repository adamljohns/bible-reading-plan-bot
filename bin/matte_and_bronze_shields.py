#!/usr/bin/env python3
"""Shield icon light-mode pipeline.

1. MATTE: remove the baked-in black background from gold shield PNGs.
   Flood-fill from the borders through dark pixels (luma < T) marks the
   background region; that region gets luminosity alpha (preserves the soft
   gold glow), everything else stays fully opaque (preserves dark interior
   detail like die pips). Background-region pixels are unpremultiplied so
   edge/glow color survives compositing onto light backgrounds.
2. BRONZE: derive antique-bronze variants (HSV shift) for the dictionary set.

Usage:
  python3 bin/matte_and_bronze_shields.py --preview   # contact sheet only, no writes
  python3 bin/matte_and_bronze_shields.py --apply     # matte in place + write bronzes
"""
import sys
from collections import deque
from pathlib import Path
from PIL import Image, ImageFilter

ICONS = Path(__file__).resolve().parent.parent / "docs" / "assets" / "icons"
FLOOD_T = 60          # flood passes through pixels with max-channel < this
GLOW_FLOOR = 10       # subtract from luminosity alpha to kill near-black noise
BRONZE_HUE_SHIFT = -9     # PIL hue units (256 = 360deg) ~ -12.7deg toward copper
BRONZE_SAT = 1.18
BRONZE_VAL = 0.72

# The 8 dictionary shields that get bronze variants (base + size variants found on disk)
BRONZE_SET = ["shield-diamond", "shield-die", "shield-search", "shield-quill-note",
              "shield-map", "shield-open-book", "shield-bible-cross", "shield-scroll-quill"]


def matte(im):
    """Return RGBA with background flood region converted to luminosity alpha."""
    im = im.convert("RGB")
    w, h = im.size
    px = im.load()
    # flood fill from all border pixels through dark pixels
    bg = bytearray(w * h)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if max(px[x, y]) < FLOOD_T and not bg[y * w + x]:
                bg[y * w + x] = 1
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if max(px[x, y]) < FLOOD_T and not bg[y * w + x]:
                bg[y * w + x] = 1
                q.append((x, y))
    while q:
        x, y = q.popleft()
        for nx, ny in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
            if 0 <= nx < w and 0 <= ny < h and not bg[ny * w + nx] and max(px[nx, ny]) < FLOOD_T:
                bg[ny * w + nx] = 1
                q.append((nx, ny))
    # interior mask (255 = keep opaque), feather edge 1px
    mask = Image.frombytes("L", (w, h), bytes(0 if b else 255 for b in bg))
    mask = mask.filter(ImageFilter.GaussianBlur(0.8))
    mpx = mask.load()
    out = Image.new("RGBA", (w, h))
    opx = out.load()
    scale = 255.0 / (255 - GLOW_FLOOR)
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            interior = mpx[x, y]
            if interior >= 250:
                opx[x, y] = (r, g, b, 255)
                continue
            lum = max(0, max(r, g, b) - GLOW_FLOOR) * scale
            a = max(int(lum), interior)
            if a <= 0:
                opx[x, y] = (0, 0, 0, 0)
                continue
            # unpremultiply glow color (it was rendered over black)
            f = 255.0 / a
            opx[x, y] = (min(255, int(r * f)), min(255, int(g * f)), min(255, int(b * f)), a)
    return out


def bronze(rgba):
    """Gold -> antique bronze: hue toward copper, richer sat, darker value."""
    rgb = rgba.convert("RGB")
    hsv = rgb.convert("HSV")
    hch, s, v = hsv.split()
    hch = hch.point(lambda p: (p + BRONZE_HUE_SHIFT) % 256)
    s = s.point(lambda p: min(255, int(p * BRONZE_SAT)))
    v = v.point(lambda p: int(p * BRONZE_VAL))
    out = Image.merge("HSV", (hch, s, v)).convert("RGB")
    out.putalpha(rgba.getchannel("A"))
    return out


def needs_matte(p):
    return Image.open(p).mode != "RGBA"


def targets():
    """All top-level gold shields lacking alpha (skip bw/, originals/, bronze files)."""
    out = []
    for p in sorted(ICONS.glob("shield-*.png")) + [ICONS / "wings-naval-aviator.png"]:
        if p.is_file() and "-bronze" not in p.name and needs_matte(p):
            out.append(p)
    return out


def preview():
    cell = 120
    names = [f"{b}-48.png" for b in BRONZE_SET]
    sheet = Image.new("RGB", (cell * len(names), cell * 2), (245, 243, 239))  # light-mode bg
    for i, n in enumerate(names):
        m = matte(Image.open(ICONS / n)).resize((96, 96), Image.LANCZOS)
        bz = bronze(m)
        sheet.paste(m, (i * cell + 12, 12), m)
        sheet.paste(bz, (i * cell + 12, cell + 12), bz)
    sheet.save("/tmp/bronze-preview.png")
    print("wrote /tmp/bronze-preview.png (top=matted gold, bottom=bronze, on light bg)")


def apply():
    files = targets()
    print(f"matting {len(files)} files in place...")
    for p in files:
        matte(Image.open(p)).save(p)
    print("writing bronze variants...")
    n = 0
    for base in BRONZE_SET:
        for suffix in ("", "-96", "-48", "-24"):
            src = ICONS / f"{base}{suffix}.png"
            if src.exists():
                bronze(Image.open(src).convert("RGBA")).save(ICONS / f"{base}-bronze{suffix}.png")
                n += 1
    print(f"done: {len(files)} matted, {n} bronze files")


if __name__ == "__main__":
    if "--apply" in sys.argv:
        apply()
    else:
        preview()
