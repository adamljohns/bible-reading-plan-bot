#!/usr/bin/env python3
"""
f5_generate_watch.py — Generate one watch of audio via F5-TTS-MLX.

Chunks the watch text at sentence boundaries, runs F5 with explicit
duration per chunk (calculated from char count to prevent over-extension
and filler hallucination), then ffmpeg-concats all chunk MP3s into the
final per-watch MP3.

USAGE
    python3 scripts/f5_generate_watch.py 2026-05-29 wisdom \
        --voice chatgpt   # or "adam" for the personal-commentary register

VOICE OPTIONS
    chatgpt  — 15 sec from Feb 18 YouTube reading (clean teaching cadence)
    adam     — 12 sec from June 5 2023 memo (his real voice reading Exodus)

OUTPUT
    docs/assets/audio/readings/<date>-<watch>.mp3
"""
import argparse
import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AUDIO_DIR = REPO / "docs" / "assets" / "audio" / "readings"
F5_TESTS = Path.home() / "Documents" / "05-Voice" / "f5tts-tests"

# Reference clips + their transcripts
VOICES = {
    "chatgpt": {
        "ref": F5_TESTS / "adam-ref-yt.wav",  # 15 sec, YouTube Feb 18 @ 2:00
        "text": "The wise man runs to the name of the Lord. Notice the order. Pride precedes collapse. Humility precedes honor. Engagement is not noise, it is disciplined presence. It is choosing to enter conversations with restraint to work with diligence.",
        "ref_sec": 15.0,
    },
    "adam": {
        "ref": F5_TESTS / "adam-ref-scripture.wav",  # 12 sec, June 5 2023 memo @ 3:00
        "text": "Why should the Egyptians say he brought them out with an evil intent to kill them in the mountains and eliminate them from the face of Earth?",
        "ref_sec": 12.0,
    },
}

FRAMES_PER_SEC = 93.75
READING_CHARS_PER_SEC = 12.0  # measured reading pace, slightly slower than natural
CHUNK_MAX = 300


def load_tts_text(date: str, watch: str) -> str:
    """Reuse the same TTS text extraction as the ElevenLabs pipeline."""
    spec = importlib.util.spec_from_file_location(
        "m", REPO / "scripts" / "generate_audio.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    md = (REPO / "data" / "readings" / f"{date}.md").read_text()
    watches = mod.split_watches(md)
    if watch not in watches:
        sys.exit(f"ERROR: watch {watch!r} not found in {date}")
    return mod.watch_text_for_tts(watches[watch])


def chunk_at_sentences(text: str, max_chars: int = CHUNK_MAX) -> list[str]:
    """Greedy-pack sentences into <=max_chars chunks. Doesn't split sentences."""
    import re
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks, current = [], ""
    for s in sentences:
        cand = (current + " " + s) if current else s
        if len(cand) <= max_chars or not current:
            current = cand
        else:
            chunks.append(current)
            current = s
    if current:
        chunks.append(current)
    return chunks


def f5_generate_chunk(text: str, voice: dict, out_wav: Path, venv_python: Path):
    """Call F5-TTS-MLX with explicit duration to prevent over-extension."""
    # Target duration = ref + (gen_chars / reading_pace)
    gen_secs = max(3.0, len(text) / READING_CHARS_PER_SEC)
    total_secs = voice["ref_sec"] + gen_secs
    duration_frames = int(total_secs * FRAMES_PER_SEC)

    cmd = [
        str(venv_python), "-m", "f5_tts_mlx.generate",
        "--text", text,
        "--ref-audio", str(voice["ref"]),
        "--ref-text", voice["text"],
        "--duration", str(duration_frames),
        "--cfg", "2.0",          # default — over-tuning hurt faithfulness
        "--steps", "32",
        "--output", str(out_wav),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: f5 returned {result.returncode}", file=sys.stderr)
        print(result.stderr[:600], file=sys.stderr)
        return False
    return True


def trim_ref_echo(wav_in: Path, wav_out: Path, ref_sec: float):
    """Strip the first ref_sec seconds (F5 prepends the reference audio)."""
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-ss", f"{ref_sec:.2f}", "-i", str(wav_in),
        "-c", "copy", str(wav_out),
    ]
    subprocess.run(cmd, check=True)


def ffmpeg_concat_to_mp3(chunk_wavs: list[Path], out_mp3: Path):
    """ffmpeg concat demuxer + MP3 encode in one step."""
    with tempfile.TemporaryDirectory() as tmp:
        listing = Path(tmp) / "concat.txt"
        listing.write_text(
            "\n".join(f"file '{w}'" for w in chunk_wavs) + "\n"
        )
        cmd = [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "concat", "-safe", "0", "-i", str(listing),
            "-ac", "1", "-ar", "24000", "-b:a", "128k",
            str(out_mp3),
        ]
        subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("date", help="YYYY-MM-DD")
    ap.add_argument("watch", choices=["wisdom", "husband", "father", "citizen", "peace"])
    ap.add_argument("--voice", choices=list(VOICES.keys()), default="chatgpt",
                    help="Reference voice (chatgpt for wisdom/peace, adam for h/f/c)")
    args = ap.parse_args()

    voice = VOICES[args.voice]
    if not voice["ref"].exists():
        sys.exit(f"ERROR: reference clip missing at {voice['ref']}")

    venv_python = Path.home() / ".venvs" / "f5tts" / "bin" / "python"
    if not venv_python.exists():
        sys.exit(f"ERROR: f5tts venv missing at {venv_python}")

    # Load text + chunk
    text = load_tts_text(args.date, args.watch)
    chunks = chunk_at_sentences(text)
    total_chars = sum(len(c) for c in chunks)
    expected_audio_sec = total_chars / READING_CHARS_PER_SEC
    print(f"=== {args.date} {args.watch} via F5 ({args.voice} voice) ===")
    print(f"  {total_chars:,} chars across {len(chunks)} chunks")
    print(f"  Expected audio: {expected_audio_sec/60:.1f} min")
    print(f"  Expected F5 compute (4x real-time): {expected_audio_sec*4/60:.1f} min")
    print()

    # Generate each chunk
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        trimmed_wavs = []
        for i, chunk in enumerate(chunks, 1):
            print(f"  [{i}/{len(chunks)}] {len(chunk):3d} chars: {chunk[:60]!r}...")
            raw_wav = tmp / f"chunk_{i:03d}.wav"
            if not f5_generate_chunk(chunk, voice, raw_wav, venv_python):
                sys.exit(f"  ABORT at chunk {i}")
            trimmed_wav = tmp / f"chunk_{i:03d}_trim.wav"
            trim_ref_echo(raw_wav, trimmed_wav, voice["ref_sec"])
            trimmed_wavs.append(trimmed_wav)

        # Concat all chunks into final MP3
        AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        out_mp3 = AUDIO_DIR / f"{args.date}-{args.watch}.mp3"
        print(f"\n  Concatenating {len(trimmed_wavs)} chunks → {out_mp3.name}")
        ffmpeg_concat_to_mp3(trimmed_wavs, out_mp3)

        size_mb = out_mp3.stat().st_size / 1024 / 1024
        print(f"  ✓ {out_mp3} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
