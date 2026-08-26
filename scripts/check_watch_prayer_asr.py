#!/usr/bin/env python3
"""PJG-0825-PEACE1 — ASR gate vs JSON prayer sentences.

Refuse R2 if any published prayer sentence (or named close) is missing from
the prayer-region transcript, or if stray narration appears before Father,.

Staff proof only. Principal ear remains CLOSE.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

WHISPER = os.environ.get("WHISPER_CLI", "/opt/homebrew/bin/whisper-cli")
MODEL = os.environ.get(
    "WHISPER_MODEL",
    os.path.expanduser("~/.openclaw/whisper_models/ggml-small.en.bin"),
)
WATCHES = ("wisdom", "husband", "father", "citizen", "peace")
# Per-day JSON keys are wisdom/first/second/third/peace.
# MP3 stems are wisdom/husband/father/citizen/peace.
JSON_KEY = {
    "wisdom": "wisdom",
    "husband": "first",
    "father": "second",
    "citizen": "third",
    "peace": "peace",
}
NAMED = (
    "grant us the grace",
    "in the name of jesus christ",
    "through jesus christ our lord",
    "when a man",
    "hold maria",
)
# Whole-watch MP3s always speak Personal Application / Reflection before the
# prayer. Those are not stray. Heading leak in the prayer region is.
STRAY = (
    "prayer from the",
)


def sentences(prayer: str) -> list[str]:
    body = re.sub(r"^🙏?\s*Prayer\b[^\n]*\n?", "", prayer.strip(), flags=re.I)
    parts = re.split(r"(?<=[.!?])\s+", body)
    out = []
    for p in parts:
        p = re.sub(r"\s+", " ", p).strip()
        if p:
            out.append(p)
    return out


def extract_prayer(text: str) -> str:
    lines = text.splitlines()
    buf, st = [], "before"
    hdr = re.compile(r"^🙏?\s*Prayer\b", re.I)
    charge = re.compile(r"^(⚓|🛡️)?\s*(Helm Command|Watch Charge|The Charge|Rudder Steer)\b", re.I)
    amen = re.compile(r"\bAmen\.?\s*$", re.I)
    for line in lines:
        if st == "before" and hdr.match(line.strip()):
            st = "prayer"
            continue
        if st == "prayer" and charge.match(line.strip()):
            break
        if st == "prayer":
            buf.append(line)
            if amen.search(line.strip()):
                break
    return "\n".join(buf).strip()


def asr(mp3: Path, tail_sec: int = 110) -> str:
    if not Path(WHISPER).is_file():
        raise SystemExit(f"ASR-GATE: missing whisper-cli at {WHISPER}")
    if not Path(MODEL).is_file():
        raise SystemExit(f"ASR-GATE: missing model at {MODEL}")
    tmp = Path(tempfile.mkdtemp(prefix="pjg-asr-"))
    wav = tmp / "prayer.wav"
    # Prayer sits at the end of the watch (before Watch Charge). Whole-file
    # ASR treats Reflection / Personal Application as stray-before-Father.
    subprocess.run(
        ["/opt/homebrew/bin/ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
         "-sseof", f"-{int(tail_sec)}", "-i", str(mp3),
         "-ac", "1", "-ar", "16000", str(wav)],
        check=True,
    )
    out_prefix = tmp / "asr"
    r = subprocess.run(
        [WHISPER, "-m", MODEL, "-f", str(wav), "-otxt", "-of", str(out_prefix),
         "-l", "en", "-nt"],
        capture_output=True, text=True,
    )
    txt = Path(str(out_prefix) + ".txt")
    if not txt.is_file():
        raise SystemExit(f"ASR-GATE: whisper produced no text rc={r.returncode} {(r.stderr or r.stdout)[-400:]}")
    return txt.read_text(errors="replace")


def norm(s: str) -> str:
    s = s.lower()
    s = s.replace("ah-men", "amen").replace("ah men", "amen")
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def tokens(s: str) -> list[str]:
    return [t for t in norm(s).split() if t not in {"the", "a", "an", "and", "of", "to", "in"}]


def present(needle: str, hay: str) -> bool:
    n = tokens(needle)
    if len(n) < 3:
        return norm(needle) in hay
    # sliding window
    h = hay.split()
    need = n[:6]
    for i in range(0, max(1, len(h) - len(need) + 1)):
        window = h[i:i + len(need) + 2]
        if all(t in window for t in need):
            return True
    return False


def check_watch(day: str, key: str, json_path: Path, mp3: Path) -> list[str]:
    fails = []
    data = json.loads(json_path.read_text())
    jkey = JSON_KEY.get(key, key)
    watch = (data.get("watches") or {}).get(jkey) or {}
    text = watch.get("text") or ""
    prayer = extract_prayer(text)
    if not prayer:
        fails.append(f"{key}: no published prayer block (json {jkey})")
        return fails
    sents = sentences(prayer)
    if not sents:
        fails.append(f"{key}: prayer sentences empty")
        return fails
    if not mp3.is_file():
        fails.append(f"{key}: missing {mp3}")
        return fails
    raw = asr(mp3)
    hay = norm(raw)
    # Last Father in the prayer-region tail is the listen-script opener.
    father_i = hay.rfind("father")
    if father_i < 0:
        fails.append(f"{key}: ASR never said Father")
    else:
        prefix = hay[:father_i]
        for s in STRAY:
            if s in prefix:
                fails.append(f"{key}: stray narration before Father, ({s!r})")
    for sent in sents:
        if not present(sent, hay):
            fails.append(f"{key}: missing sentence {sent[:80]!r}")
    joined = " ".join(sents).lower()
    for named in NAMED:
        if named in joined and named not in hay and not present(named, hay):
            fails.append(f"{key}: named clause missing {named!r}")
    return fails


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: check_watch_prayer_asr.py YYYY-MM-DD [repo]", file=sys.stderr)
        return 2
    day = argv[1]
    root = Path(argv[2]) if len(argv) > 2 else Path.cwd()
    js = root / "docs" / "assets" / "readings" / f"{day}.json"
    if not js.is_file():
        print(f"ASR-GATE: missing {js}", file=sys.stderr)
        return 2
    fails = []
    for key in WATCHES:
        mp3 = root / "docs" / "assets" / "audio" / "readings" / f"{day}-{key}.mp3"
        fails.extend(check_watch(day, key, js, mp3))
    if fails:
        print("ASR-GATE FAIL", day)
        for f in fails:
            print(" -", f)
        return 12
    print("ASR-GATE PASS", day)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
