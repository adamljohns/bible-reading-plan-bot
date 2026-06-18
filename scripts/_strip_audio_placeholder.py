#!/usr/bin/env python3
"""One-off: strip the 'voiceover coming for this watch' placeholder block from
already-rendered reading pages so screen/TTS readers (Speechify) stop reading it.
The renderer (build_reading_page_from_md.py) no longer emits it for new renders."""
import re, glob

PAT = re.compile(
    r'[ \t]*<div class="audio-slot audio-pending">\s*'
    r'<div class="audio-cap">[^<]*</div>\s*</div>\n?',
    re.DOTALL,
)

def main():
    changed = total = 0
    for f in sorted(glob.glob("docs/readings/*.html")):
        s = open(f, encoding="utf-8").read()
        hits = len(PAT.findall(s))
        if hits:
            open(f, "w", encoding="utf-8").write(PAT.sub("", s))
            changed += 1
            total += hits
    print(f"files changed: {changed}, placeholders removed: {total}")

if __name__ == "__main__":
    main()
