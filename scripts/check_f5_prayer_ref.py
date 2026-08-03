#!/usr/bin/env python3
"""Fail-closed F5 prayer-ref + prayer-text ban list (PJG-0803-PIN1).

2026-08-03: ~/.openclaw/voice/f5tts-tests/ref-calm.txt was Studio Command
dashboard copy (studios + PIN). F5 used it as --ref-text and bled that copy
into every Adam-clone prayer segment on 2026-08-03 watches.

Canonical ref pair ONLY:
  ~/.openclaw/voice/f5tts-tests/ref-calm.wav
  ~/.openclaw/voice/f5tts-tests/ref-calm.txt   # Psalm 23 (or equivalent calm Scripture)

Usage:
  python3 scripts/check_f5_prayer_ref.py              # check default resolved paths
  python3 scripts/check_f5_prayer_ref.py --text FILE  # also scan a prayer source text
  python3 scripts/check_f5_prayer_ref.py --transcript FILE  # post-bake whisper txt
  python3 scripts/check_f5_prayer_ref.py --wav PATH --txt PATH

Exit 0 clean · Exit 1 ban hit · Exit 2 missing/unreadable ref
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

DEFAULT_WAV = Path.home() / ".openclaw/voice/f5tts-tests/ref-calm.wav"
DEFAULT_TXT = Path.home() / ".openclaw/voice/f5tts-tests/ref-calm.txt"
LEGACY_WAV = Path.home() / "Documents/05-Voice/f5tts-tests/ref-calm.wav"
LEGACY_TXT = Path.home() / "Documents/05-Voice/f5tts-tests/ref-calm.txt"

# Hard ban — studio/PIN/product bleed. Do NOT put the live PIN digits here as a
# standalone pattern (false positives on years/verses). Phrase-level only.
BAN_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("studio_cosner", re.compile(r"cosner'?s?", re.I)),
    ("studio_liberty_list", re.compile(r"\bliberty\b.*\baquia\b|\baquia\b.*\bliberty\b", re.I)),
    ("studio_aquia", re.compile(r"\baquia\b", re.I)),
    ("three_studios", re.compile(r"three\s+studios", re.I)),
    ("not_public_website", re.compile(r"not\s+a\s+public\s+website", re.I)),
    ("pin_is_phrase", re.compile(r"\bpin\s+is\b|\bp\.?\s*i\.?\s*n\.?\s+is\b", re.I)),
    ("studio_command", re.compile(r"studio\s+command", re.I)),
    ("fit20_product", re.compile(r"\bfit\s*20\b", re.I)),
    ("private_dashboard", re.compile(r"private\s+dashboard", re.I)),
    # digit-spelled PIN style from the bad ref ("two zero two")
    ("spelled_pin_digits", re.compile(r"two\s+zero\s+two(?:\s+zero)?", re.I)),
]

# Liberty alone is a real English/political word (citizen watch). Only flag bare
# Liberty when co-occurring with studio markers in the same text.
SOFT_LIBERTY = re.compile(r"\bliberty\b", re.I)
STUDIO_COCONTEXT = re.compile(
    r"studio|cosner|aquia|fit\s*20|public\s+website|\bpin\b|dashboard", re.I
)


def first_readable(*paths: Path) -> Path | None:
    for p in paths:
        try:
            if p and p.is_file() and os.access(p, os.R_OK):
                with open(p, "rb") as fh:
                    fh.read(16)
                return p
        except OSError:
            continue
    return None


def scan_text(label: str, text: str) -> list[str]:
    hits: list[str] = []
    for code, pat in BAN_PATTERNS:
        if pat.search(text or ""):
            hits.append(f"{label}:{code}")
    # bare liberty only with studio co-context
    if SOFT_LIBERTY.search(text or "") and STUDIO_COCONTEXT.search(text or ""):
        # avoid double-count if already hit liberty_list
        if not any(h.endswith("studio_liberty_list") for h in hits):
            hits.append(f"{label}:liberty_with_studio_context")
    return hits


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--wav", type=Path, help="override ref wav")
    ap.add_argument("--txt", type=Path, help="override ref txt")
    ap.add_argument("--text", type=Path, action="append", default=[], help="prayer source text file(s)")
    ap.add_argument("--transcript", type=Path, action="append", default=[], help="post-bake transcript(s)")
    ap.add_argument("--allow-missing-wav", action="store_true", help="only used for dry text scans")
    args = ap.parse_args(argv)

    wav = args.wav or first_readable(DEFAULT_WAV, LEGACY_WAV)
    txt = args.txt or first_readable(DEFAULT_TXT, LEGACY_TXT)

    errors: list[str] = []
    hits: list[str] = []

    if not args.allow_missing_wav:
        if wav is None:
            errors.append("missing_ref_wav")
        if txt is None:
            errors.append("missing_ref_txt")

    if txt is not None:
        try:
            ref_text = txt.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            errors.append(f"ref_txt_unreadable:{e}")
            ref_text = ""
        if ref_text.strip():
            hits.extend(scan_text("ref_txt", ref_text))
            # Psalm-ish sanity: calm ref should look like Scripture, not product
            if re.search(r"studio coordinator|coach arnie|version one point", ref_text, re.I):
                hits.append("ref_txt:product_demo_voice")
        else:
            errors.append("ref_txt_empty")

    if wav is not None and wav.stat().st_size < 50_000:
        errors.append(f"ref_wav_too_small:{wav.stat().st_size}")

    # Prefer TCC-safe path when both exist
    if wav is not None and "Documents/05-Voice" in str(wav) and DEFAULT_WAV.is_file():
        print(f"WARN: resolved legacy Documents wav; prefer {DEFAULT_WAV}", file=sys.stderr)

    for p in args.text:
        try:
            hits.extend(scan_text(f"prayer_src:{p.name}", p.read_text(encoding="utf-8", errors="replace")))
        except OSError as e:
            errors.append(f"prayer_src_unreadable:{p}:{e}")

    for p in args.transcript:
        try:
            hits.extend(scan_text(f"transcript:{p.name}", p.read_text(encoding="utf-8", errors="replace")))
        except OSError as e:
            errors.append(f"transcript_unreadable:{p}:{e}")

    if wav:
        print(f"ref_wav={wav}")
    if txt:
        print(f"ref_txt={txt}")

    if errors:
        print("FAIL f5-prayer-ref: " + ", ".join(errors), file=sys.stderr)
        return 2
    if hits:
        print("FAIL f5-prayer-ref ban hits:", file=sys.stderr)
        for h in hits:
            print(f" - {h}", file=sys.stderr)
        return 1

    print("OK f5-prayer-ref clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
