#!/usr/bin/env python3
"""PJG-0011 — two-voice watch MP3: Bible voice on Scripture, Watch male A on rest + loudnorm.

Uses F5-TTS-MLX via f5_generate_watch voice map:
  scripture → chatgpt (teaching/narrator ref)
  commentary → adam (scripture-memo ref)  # distinct from chatgpt

USAGE
  python3 scripts/gen_two_voice_watch.py 2026-07-23 peace
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AUDIO_DIR = REPO / "docs" / "assets" / "audio" / "readings"
FFMPEG = "/opt/homebrew/bin/ffmpeg"
NORM = Path.home() / "Scripts" / "media-pipeline" / "normalize-audio.sh"
F5_GEN = REPO / "scripts" / "f5_generate_watch.py"
LOG = Path.home() / ".openclaw" / "logs" / "pjg-0011-two-voice.log"


def log(msg: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    line = msg.rstrip() + "\n"
    print(line, end="", flush=True)
    with LOG.open("a") as fh:
        fh.write(line)


def load_mod(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def split_scripture_commentary(body: str) -> tuple[str, str]:
    """Return (scripture_tts, commentary_tts) from a watch body (post-header)."""
    g = load_mod(REPO / "scripts" / "generate_audio.py", "gen_audio")
    lines = body.splitlines()
    # Find scripture header
    scrip_i = None
    for i, ln in enumerate(lines):
        if re.search(r"📖\s*Scripture", ln) or re.match(r"^\s*Scripture\s*[—\-–:]", ln):
            scrip_i = i
            break
    if scrip_i is None:
        # whole body as commentary fallback
        return "", g.watch_text_for_tts(body)

    # passage title line
    title = lines[scrip_i]
    # scripture runs until separator ⸻ or next major section marker
    end = len(lines)
    for j in range(scrip_i + 1, len(lines)):
        s = lines[j].strip()
        if s.startswith("⸻") or s.startswith("---"):
            end = j
            break
        if re.match(r"^[🌾🛡🙏🛰️⛏️]", s):
            end = j
            break
        if re.search(r"Reflection|Situation Report|Personal Application|Prayer|Watch Charge|Helm", s) and j > scrip_i + 2:
            end = j
            break

    scrip_block = "\n".join(lines[scrip_i:end]).strip()
    before = "\n".join(lines[:scrip_i]).strip()
    after = "\n".join(lines[end:]).strip()
    commentary_raw = (before + "\n\n" + after).strip()

    scrip_tts = g.watch_text_for_tts(scrip_block)
    comm_tts = g.watch_text_for_tts(commentary_raw) if commentary_raw else ""
    return scrip_tts, comm_tts


VOICES = {
    # Distinct refs both from Adam corpus — different takes = different timbre/cadence
    "bible": {
        "ref": Path.home() / "Documents/05-Voice/f5tts-tests/ref-clean.wav",
        "text": (Path.home() / "Documents/05-Voice/f5tts-tests/ref-clean.txt").read_text().strip(),
        "ref_sec": 17.0,
    },
    "watch": {
        "ref": Path.home() / "Documents/05-Voice/f5tts-tests/ref-calm.wav",
        "text": (Path.home() / "Documents/05-Voice/f5tts-tests/ref-calm.txt").read_text().strip(),
        "ref_sec": 15.0,
    },
}


def f5_synthesize(text: str, voice: str, out_mp3: Path, work: Path) -> None:
    """F5-TTS-MLX synth for arbitrary text using distinct voice refs."""
    f5 = load_mod(F5_GEN, "f5gen")
    if voice not in VOICES:
        raise SystemExit(f"unknown voice {voice}; have {list(VOICES)}")
    v = VOICES[voice]
    if not Path(v["ref"]).exists():
        raise SystemExit(f"missing ref wav: {v['ref']}")

    # Use f5_voice style generation if available for verified chunks; else f5_generate_watch chunk path
    # Prefer f5_generate_watch's pipeline functions if present
    text = text.replace("LORD", "Lord")
    chunks = f5.chunk_at_sentences(text, max_chars=220)
    log(f"  voice={voice} chunks={len(chunks)} chars={len(text)}")
    chunk_paths = []
    tmp = work / f"{voice}-chunks"
    tmp.mkdir(parents=True, exist_ok=True)

    # Load f5-tts-mlx runner from f5_generate_watch if defined
    if hasattr(f5, "synth_chunk"):
        for i, c in enumerate(chunks):
            wav = tmp / f"c{i:03d}.wav"
            f5.synth_chunk(c, voice, wav)
            chunk_paths.append(wav)
    else:
        # Inline F5 call matching f5_generate_watch patterns
        import math
        py = str(Path.home() / ".venvs/f5tts/bin/python")
        for i, c in enumerate(chunks):
            # duration = ref_sec + chars/cps + buffer, but f5-tts-mlx --duration is TOTAL
            ref_sec = float(v["ref_sec"])
            gen_sec = max(2.0, len(c) / 12.0 + 0.6)
            duration = ref_sec + gen_sec
            raw = tmp / f"c{i:03d}-raw.wav"
            outw = tmp / f"c{i:03d}.wav"
            cmd = [
                py, "-m", "f5_tts_mlx.generate",
                "--text", c,
                "--ref-audio", str(v["ref"]),
                "--ref-text", v["text"],
                "--duration", str(duration),
                "--output", str(raw),
                "--steps", "32",
            ]
            log(f"    [{i+1}/{len(chunks)}] {c[:60]!r}")
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0 or not raw.exists():
                log(f"    F5 FAIL: {r.stderr[-400:]}")
                raise SystemExit(f"F5 failed chunk {i}")
            # take gen portion? f5-tts-mlx with duration outputs gen-only when configured;
            # normalize sample rate
            subprocess.run(
                [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", str(raw),
                 "-ac", "1", "-ar", "24000", str(outw)],
                check=True,
            )
            chunk_paths.append(outw)

    if not chunk_paths:
        raise SystemExit("no chunks")
    lst = work / f"{voice}-list.txt"
    lst.write_text("".join(f"file '{c}'\n" for c in chunk_paths))
    subprocess.run(
        [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", str(lst), "-c:a", "libmp3lame", "-q:a", "2", str(out_mp3)],
        check=True,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("date")
    ap.add_argument("watch", help="wisdom|husband|father|citizen|peace (or first/second/third aliases)")
    args = ap.parse_args()
    alias = {"first": "husband", "second": "father", "third": "citizen"}
    watch = alias.get(args.watch, args.watch)

    g = load_mod(REPO / "scripts" / "generate_audio.py", "gen_audio")
    md = (REPO / "data" / "readings" / f"{args.date}.md").read_text()
    watches = g.split_watches(md)
    if watch not in watches:
        raise SystemExit(f"watch {watch} not in {args.date}: {list(watches)}")

    scrip, comm = split_scripture_commentary(watches[watch])
    log(f"=== two-voice {args.date} {watch} ===")
    log(f"scripture_chars={len(scrip)} commentary_chars={len(comm)}")
    if not scrip:
        log("WARN: no scripture split; commentary-only")

    work = Path(tempfile.mkdtemp(prefix=f"tv-{args.date}-{watch}-"))
    parts = []
    if scrip:
        sp = work / "scripture.mp3"
        f5_synthesize(scrip, "bible", sp, work)
        parts.append(sp)
    if comm:
        cp = work / "commentary.mp3"
        f5_synthesize(comm, "watch", cp, work)
        parts.append(cp)
    if not parts:
        raise SystemExit("nothing to synth")

    # 0.35s gap between voices
    gap = work / "gap.wav"
    subprocess.run(
        [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
         "-i", "anullsrc=r=24000:cl=mono", "-t", "0.35", gap],
        check=True,
    )
    stitched = work / "stitched.mp3"
    lst = work / "final.txt"
    lines = []
    for i, pth in enumerate(parts):
        lines.append(f"file '{pth}'\n")
        if i < len(parts) - 1:
            lines.append(f"file '{gap}'\n")
    lst.write_text("".join(lines))
    subprocess.run(
        [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", str(lst), "-c:a", "libmp3lame", "-q:a", "2", str(stitched)],
        check=True,
    )

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    out = AUDIO_DIR / f"{args.date}-{watch}.mp3"
    # also write husband/first aliases if needed — peace is peace
    raw_out = work / "pre-norm.mp3"
    subprocess.run(
        [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", str(stitched),
         "-c:a", "libmp3lame", "-q:a", "2", str(raw_out)],
        check=True,
    )
    if NORM.exists():
        subprocess.run(["bash", str(NORM), str(raw_out), str(out)], check=True)
    else:
        out.write_bytes(raw_out.read_bytes())

    # loudness proof
    measure = subprocess.run(
        [FFMPEG, "-hide_banner", "-i", str(out),
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    log(measure.stderr[-800:])
    log(f"WROTE {out} size={out.stat().st_size}")
    log(f"VOICE_MAP scripture=bible(ref-clean) commentary=watch(ref-calm)")
    print(out)


if __name__ == "__main__":
    main()
