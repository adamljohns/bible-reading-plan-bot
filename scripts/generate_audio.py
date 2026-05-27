#!/usr/bin/env python3
"""
Generate ElevenLabs voiceovers for daily Bible readings.

For each watch of a given day, extract the spoken content (Scripture + Context
+ Reflection + Application + Prayer + Helm/Rudder line) from data/readings/<date>.md,
strip emoji + section markers + Markdown separators, then POST to ElevenLabs
text-to-speech and save the MP3 at
  docs/assets/audio/readings/<date>-<watch_slug>.mp3

The renderer (build_reading_page_from_md.py) already references this path;
when the MP3 exists, the page auto-shows an <audio> player instead of the
"voiceover coming" placeholder.

ENVIRONMENT
  ELEVENLABS_API_KEY   required (xi-api-key header)
  ELEVENLABS_VOICE_ID  required (voice clone ID for Adam)
  ELEVENLABS_MODEL     optional, default "eleven_multilingual_v2"
                       (Creator plan supports v2 + Turbo v2.5)

USAGE
  python3 scripts/generate_audio.py 2026-01-01                # one day
  python3 scripts/generate_audio.py --watch wisdom 2026-01-01 # one watch only
  python3 scripts/generate_audio.py --date-range 2026-01-01 2026-01-07
  python3 scripts/generate_audio.py --all                     # every .md
  python3 scripts/generate_audio.py --dry-run 2026-01-01      # show what would
                                                              # be sent, no API call

QUOTA NOTE
  A typical day has ~17,000 characters across 5 watches. The Creator plan
  ($22/mo) gives 100,000 chars/month. Full year ≈ 6.2M chars → Pro ($99/mo
  for 500k) is the realistic tier; even there a year is ~12 months of quota.
  Recommend generating gradually (e.g., the upcoming week each Sunday) rather
  than batching the whole year up front.
"""
import argparse
import os
import re
import sys
import json
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "readings"
AUDIO_DIR = REPO / "docs" / "assets" / "audio" / "readings"

ELEVENLABS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
DEFAULT_MODEL = "eleven_multilingual_v2"
MAX_TTS_CHARS = 9500   # ElevenLabs hard cap is 10,000; leave a little headroom

# Watch boundaries — must match the renderer
WATCH_BOUNDARY_C = re.compile(r"^\s*📅[^—\-]*[—\-]\s*(0600|0700|1100|1500|2100)\b")
WATCH_BOUNDARY_A = re.compile(r"^\s*[🌅🕖🕚🕒🌙]\s*(0600|0700|1100|1500|2100)\b")
TIME_TO_SLUG = {"0600": "wisdom", "0700": "husband", "1100": "father",
                "1500": "citizen", "2100": "peace"}
SLUG_TO_LABEL = {"wisdom": "Morning Wisdom", "husband": "First Watch — Husband's Post",
                 "father": "Second Watch — Father's Charge",
                 "citizen": "Third Watch — Citizen's Stand",
                 "peace": "Evening Peace"}
WATCH_ORDER = ["wisdom", "husband", "father", "citizen", "peace"]


def split_watches(md_text):
    """Return {slug: body_text} for each detected watch."""
    lines = md_text.splitlines()
    boundaries = []   # (line_idx, slug)
    for i, line in enumerate(lines):
        m = WATCH_BOUNDARY_C.match(line) or WATCH_BOUNDARY_A.match(line)
        if m:
            boundaries.append((i, TIME_TO_SLUG[m.group(1)]))

    if not boundaries:
        return {}

    # Pass 2 — infer missing watches via scripture-marker fallback
    scrip_re = re.compile(r"^\s*📖\s*(?:Scripture|\*\*)", re.IGNORECASE)
    inferred = []
    for idx, (start, slug) in enumerate(boundaries):
        end = boundaries[idx + 1][0] if idx + 1 < len(boundaries) else len(lines)
        scrips = [i for i in range(start + 1, end) if scrip_re.match(lines[i])]
        inferred.append((start, slug))
        if len(scrips) <= 1:
            continue
        next_slug = boundaries[idx + 1][1] if idx + 1 < len(boundaries) else None
        try:
            cur = WATCH_ORDER.index(slug)
            nxt = WATCH_ORDER.index(next_slug) if next_slug in WATCH_ORDER else len(WATCH_ORDER)
            gap = WATCH_ORDER[cur + 1:nxt]
        except ValueError:
            continue
        for j, scr_i in enumerate(scrips[1:]):
            if j >= len(gap):
                break
            inferred.append((scr_i, gap[j]))
    inferred.sort()
    boundaries = inferred

    watches = {}
    for idx, (start, slug) in enumerate(boundaries):
        end = boundaries[idx + 1][0] if idx + 1 < len(boundaries) else len(lines)
        body = "\n".join(lines[start + 1:end])
        watches[slug] = body
    return watches


# Lines to OMIT from the audio (separators, the date header, etc.)
SKIP_LINE_RE = re.compile(
    r"^\s*(?:"
    r"⸻+"             # the ⸻ separators
    r"|---+|—{2,}"     # markdown rules / dash separators
    r"|📅\s"           # the date header line
    r"|_Converted\s"   # the PDF-conversion footnote
    r")"
)

# Strip emojis + visual markers from a kept line so TTS doesn't read them aloud
EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"  # most pictographs
    "\U00002600-\U000027BF"  # misc symbols + dingbats
    "‍️"           # ZWJ + variation selector
    "]+",
    flags=re.UNICODE,
)


def watch_text_for_tts(body):
    """Convert one watch's markdown body into clean spoken-word text."""
    out_lines = []
    for raw in body.splitlines():
        if SKIP_LINE_RE.match(raw):
            continue
        stripped = raw.strip()
        if not stripped:
            out_lines.append("")
            continue
        # Drop bullet marker but preserve the sentence
        stripped = re.sub(r"^[•\-\*]\s+", "", stripped)
        # Drop bold/italic markers
        stripped = re.sub(r"\*\*([^*]+)\*\*", r"\1", stripped)
        stripped = re.sub(r"\*([^*]+)\*", r"\1", stripped)
        # Strip emoji
        stripped = EMOJI_RE.sub("", stripped).strip()
        # Common label-only lines that are visual only — drop or rewrite
        if re.fullmatch(r"(Scripture)\s*[—\-–:]\s*.+", stripped):
            # "Scripture — John 1:1-18" → "From John chapter 1, verses 1 to 18."
            ref = re.sub(r"^Scripture\s*[—\-–:]\s*", "", stripped, flags=re.IGNORECASE)
            stripped = f"From {ref}."
        elif re.fullmatch(r"Helm Command\s*:?\s*.+", stripped, re.IGNORECASE):
            cmd = re.sub(r"^Helm Command\s*:?\s*", "", stripped, flags=re.IGNORECASE)
            stripped = f"Helm command. {cmd}"
        elif re.fullmatch(r"Rudder Steer\s*:?\s*.+", stripped, re.IGNORECASE):
            cmd = re.sub(r"^Rudder Steer\s*:?\s*", "", stripped, flags=re.IGNORECASE)
            stripped = f"Rudder steer. {cmd}"
        elif re.fullmatch(r"(Context Summary|Briefing Summary|Field Notes|Situation Report)\s*:?\s*",
                          stripped, re.IGNORECASE):
            # heading-only line — skip; the body that follows will read fine
            continue
        elif re.fullmatch(r"Reflection for .+", stripped, re.IGNORECASE):
            continue  # heading-only line, skip
        elif re.fullmatch(r"Personal Application\s*[—\-–:]?\s*.*", stripped, re.IGNORECASE):
            continue
        elif stripped.lower() in ("prayer", "amen", "amen.",):
            # keep "Amen." at end of prayer; drop the standalone "Prayer" heading
            if stripped.lower() == "prayer":
                continue
        out_lines.append(stripped)

    # Collapse multiple blank lines, then join
    text = "\n".join(out_lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def chunk_text(text, max_chars=MAX_TTS_CHARS):
    """Split text into ≤max_chars chunks at paragraph boundaries.
    Falls back to sentence boundaries if a paragraph alone exceeds max_chars."""
    if len(text) <= max_chars:
        return [text]
    paragraphs = text.split("\n\n")
    chunks, current = [], ""
    for p in paragraphs:
        candidate = (current + "\n\n" + p) if current else p
        if len(candidate) <= max_chars:
            current = candidate
            continue
        if current:
            chunks.append(current)
            current = ""
        if len(p) <= max_chars:
            current = p
        else:
            # Paragraph alone too long — split on sentence end
            sentences = re.split(r"(?<=[.!?])\s+", p)
            for s in sentences:
                cand = (current + " " + s) if current else s
                if len(cand) <= max_chars:
                    current = cand
                else:
                    if current:
                        chunks.append(current)
                    current = s
    if current:
        chunks.append(current)
    return chunks


def call_elevenlabs(text, voice_id, api_key, model=DEFAULT_MODEL):
    """POST to ElevenLabs; return MP3 bytes or raise."""
    url = ELEVENLABS_URL.format(voice_id=voice_id)
    payload = {
        "text": text,
        "model_id": model,
        "voice_settings": {
            "stability": 0.55,        # steady but not robotic
            "similarity_boost": 0.85, # tighter to Adam's voice
            "style": 0.20,            # mild expressiveness
            "use_speaker_boost": True,
        },
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


def generate_watch(date_str, slug, body, api_key, voice_id, model, force=False, dry_run=False):
    text = watch_text_for_tts(body)
    if not text:
        print(f"    [{slug}] empty after cleaning — skipped")
        return False

    out = AUDIO_DIR / f"{date_str}-{slug}.mp3"
    if out.exists() and not force:
        print(f"    [{slug}] exists ({out.stat().st_size/1024:.0f} KB) — skip (use --force to regenerate)")
        return False

    char_count = len(text)
    chunks = chunk_text(text)
    chunk_note = f" in {len(chunks)} chunks" if len(chunks) > 1 else ""
    print(f"    [{slug}] {char_count:,} chars → {out.name}{chunk_note}")
    if dry_run:
        print(f"      DRY-RUN PREVIEW (first 300 chars):")
        print("      " + text[:300].replace("\n", " ⏎ "))
        return False

    mp3_parts = []
    for idx, chunk in enumerate(chunks, 1):
        if len(chunks) > 1:
            print(f"      chunk {idx}/{len(chunks)} ({len(chunk):,} chars)")
        try:
            mp3_parts.append(call_elevenlabs(chunk, voice_id, api_key, model=model))
        except urllib.error.HTTPError as e:
            body_err = e.read().decode("utf-8", errors="replace")[:500]
            print(f"      HTTP {e.code}: {body_err}")
            return False
        except urllib.error.URLError as e:
            print(f"      Network error: {e}")
            return False

    mp3 = b"".join(mp3_parts)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(mp3)
    print(f"      ✓ wrote {len(mp3)/1024:.0f} KB")
    return True


def generate_day(date_str, watch_filter, api_key, voice_id, model, force=False, dry_run=False):
    src = DATA_DIR / f"{date_str}.md"
    if not src.exists():
        print(f"  ⚠ {src} missing — skip")
        return
    print(f"\n=== {date_str} ===")
    watches = split_watches(src.read_text())
    if not watches:
        print(f"  no watches detected")
        return
    total_chars = 0
    for slug in WATCH_ORDER:
        if slug not in watches:
            continue
        if watch_filter and slug != watch_filter:
            continue
        text = watch_text_for_tts(watches[slug])
        total_chars += len(text)
        generate_watch(date_str, slug, watches[slug], api_key, voice_id, model,
                       force=force, dry_run=dry_run)
    print(f"  day-total: ~{total_chars:,} chars billed (if all regenerated)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("date", nargs="?", help="single date like 2026-01-01")
    ap.add_argument("--all", action="store_true", help="process every .md in data/readings/")
    ap.add_argument("--date-range", nargs=2, metavar=("START", "END"))
    ap.add_argument("--watch", choices=WATCH_ORDER, help="only this watch")
    ap.add_argument("--force", action="store_true", help="overwrite existing MP3s")
    ap.add_argument("--dry-run", action="store_true", help="preview text + char-count, no API call")
    ap.add_argument("--quota", action="store_true", help="print subscription tier + remaining chars, then exit")
    args = ap.parse_args()

    if args.quota:
        api_key = os.environ.get("ELEVENLABS_API_KEY", "")
        if not api_key:
            sys.exit("ERROR: ELEVENLABS_API_KEY not set")
        import datetime
        req = urllib.request.Request(
            "https://api.elevenlabs.io/v1/user/subscription",
            headers={"xi-api-key": api_key, "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.loads(r.read())
        except urllib.error.HTTPError as e:
            sys.exit(f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:400]}")
        reset = d.get("next_character_count_reset_unix")
        reset_str = datetime.datetime.fromtimestamp(reset).strftime("%Y-%m-%d %H:%M") if reset else "?"
        used = d.get("character_count", 0)
        limit = d.get("character_limit", 0)
        remaining = limit - used
        pct = (used / limit * 100) if limit else 0
        print(f"Tier:        {d.get('tier')} ({d.get('status')})")
        print(f"Used:        {used:,} / {limit:,} chars  ({pct:.1f} %)")
        print(f"Remaining:   {remaining:,} chars")
        print(f"Resets:      {reset_str}")
        # Rough day-coverage estimate (~30k chars per full day)
        if remaining > 0:
            days = remaining / 30000.0
            print(f"Approx days: ~{days:.1f} full days at 30k chars/day (5 watches)")
        sys.exit(0)

    api_key  = os.environ.get("ELEVENLABS_API_KEY", "")
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "")
    model    = os.environ.get("ELEVENLABS_MODEL", DEFAULT_MODEL)

    if not args.dry_run:
        if not api_key:
            sys.exit("ERROR: ELEVENLABS_API_KEY not set (export it or pass --dry-run)")
        if not voice_id:
            sys.exit("ERROR: ELEVENLABS_VOICE_ID not set (your cloned-voice ID)")

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    if args.all:
        files = sorted([f for f in DATA_DIR.glob("*.md") if re.match(r"^\d{4}-\d{2}-\d{2}\.md$", f.name)])
        print(f"Processing {len(files)} day(s)")
        for f in files:
            generate_day(f.stem, args.watch, api_key, voice_id, model,
                         force=args.force, dry_run=args.dry_run)
    elif args.date_range:
        cur = datetime.fromisoformat(args.date_range[0])
        end = datetime.fromisoformat(args.date_range[1])
        while cur <= end:
            generate_day(cur.strftime("%Y-%m-%d"), args.watch, api_key, voice_id, model,
                         force=args.force, dry_run=args.dry_run)
            cur += timedelta(days=1)
    elif args.date:
        generate_day(args.date, args.watch, api_key, voice_id, model,
                     force=args.force, dry_run=args.dry_run)
    else:
        ap.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
