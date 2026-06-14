#!/usr/bin/env bash
# finish-worship-icon.sh — turn a ChatGPT-generated worship icon PNG into the
# site icon set (transparent gold), matching the existing shield-*.png style.
# Does NOT wire/commit — Claude eyeballs the result first, then wires + pushes.
#
# Usage: bin/finish-worship-icon.sh [path-to-source.png]   (default ~/Documents/worship-icon-src.png)
set -euo pipefail
SRC="${1:-$HOME/Documents/worship-icon-src.png}"
ICONS="$(cd "$(dirname "$0")/.." && pwd)/docs/assets/icons"
NAME="shield-worship-music"

[ -f "$SRC" ] || { echo "!! source not found: $SRC"; echo "Generate it first — see WORSHIP-ICON-PROMPT.md"; exit 1; }

# 1) Matte the baked black box to transparency using the existing pipeline's matte().
python3 - "$SRC" "$ICONS/$NAME.png" <<'PY'
import sys, pathlib
sys.path.insert(0, str(pathlib.Path("bin").resolve()))
from PIL import Image
from matte_and_bronze_shields import matte
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src)
matte(im).save(out)
print("matted ->", out)
PY

# 2) Downscale to the set's sizes (square; sips keeps it square if source is square).
for sz in 96 48 24; do
  cp "$ICONS/$NAME.png" "$ICONS/$NAME-$sz.png"
  sips -Z "$sz" "$ICONS/$NAME-$sz.png" >/dev/null
done
echo "Wrote: $NAME.png + -96/-48/-24 in docs/assets/icons/"
echo "Next: Claude reviews the 96px, then swaps shield-quill-note -> $NAME in"
echo "  generate-worship-pages.js (rebuild) + the 36 hub-page nav links + brand-assets.html, then commits."
