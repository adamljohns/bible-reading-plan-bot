#!/usr/bin/env python3
"""generate-watch-audio.py — narrate a day's five watches with Kokoro (mlx-audio).

Reads each watch's canonical text from docs/assets/readings/<date>.json and renders
one MP3 per watch into docs/assets/audio/readings/<date>-<name>.mp3, where <name>
uses the human filenames the page builder and every existing file already use:
wisdom / husband / father / citizen / peace. Those MP3s are COMMITTED (this asset
dir is intentionally not gitignored — the site serves them itself at
usmcmin.org/assets/audio/readings/..., which is exactly the audio_url the delivery
JSON advertises to PJ).

After rendering, re-run:
  python3 scripts/build_reading_index.py                       (flips has_audio/audio_url)
  python3 scripts/build_reading_page_from_md.py --date <date>  (page shows the players)

Run (mlx-audio venv is Python 3.11 — the TTS stack has no cp314 wheels):
  ~/.mlx-audio-venv/bin/python bin/generate-watch-audio.py 2026-07-17 2026-07-18
Voice: Kokoro am_michael (US male) for all five watches; override with WATCH_VOICE.
"""
import json, os, re, sys, glob, tempfile, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
READINGS_JSON = os.path.join(ROOT, "docs", "assets", "readings")
OUT = os.path.join(ROOT, "docs", "assets", "audio", "readings")
MODEL_ID = os.environ.get("KOKORO_MODEL", "mlx-community/Kokoro-82M-bf16")
VOICE = os.environ.get("WATCH_VOICE", "am_michael")
LANG = os.environ.get("WATCH_LANG", "a")

FILE_KEY = {"wisdom": "wisdom", "first": "husband", "second": "father",
            "third": "citizen", "peace": "peace"}

EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF⭐✅❌️]+"
)
TIMECODE = re.compile(r"^\s*(\d{4})\s+")

def clean_for_tts(text):
    """Plain, speakable prose: drop emoji, markdown marks, and leading time codes."""
    out = []
    for raw in text.splitlines():
        line = EMOJI.sub("", raw).strip()
        line = line.replace("**", "").replace("###", "").replace("##", "").lstrip("# ")
        line = TIMECODE.sub("", line)          # "0600 Morning Wisdom" -> "Morning Wisdom"
        out.append(line)
    speak = "\n".join(out)
    speak = re.sub(r"\n{3,}", "\n\n", speak).strip()
    return speak

def render(model, gen_audio, date, key, text):
    fname = f"{date}-{FILE_KEY[key]}.mp3"
    speak = clean_for_tts(text)
    with tempfile.TemporaryDirectory(prefix="watch-") as tmp:
        gen_audio(text=speak, model=model, voice=VOICE, lang_code=LANG,
                  output_path=tmp, file_prefix="w", join_audio=True,
                  audio_format="wav", verbose=False)
        wavs = sorted(glob.glob(os.path.join(tmp, "*.wav")))
        if not wavs:
            raise RuntimeError(f"no wav for {date} {key}")
        os.makedirs(OUT, exist_ok=True)
        mp3 = os.path.join(OUT, fname)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wavs[0],
                        "-codec:a", "libmp3lame", "-b:a", "64k", "-ac", "1", mp3], check=True)
    secs = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "default=nk=1:nw=1", mp3],
                                capture_output=True, text=True).stdout.strip())
    kb = os.path.getsize(mp3) // 1024
    return fname, int(secs), kb

def main():
    dates = sys.argv[1:]
    if not dates:
        print("usage: generate-watch-audio.py <YYYY-MM-DD> [more dates]"); sys.exit(2)
    from mlx_audio.tts.utils import load_model
    from mlx_audio.tts.generate import generate_audio
    print(f"Loading Kokoro {MODEL_ID} (once), voice={VOICE}...")
    model = load_model(MODEL_ID)
    for date in dates:
        day = json.load(open(os.path.join(READINGS_JSON, f"{date}.json")))
        for key in ["wisdom", "first", "second", "third", "peace"]:
            w = day["watches"].get(key) or {}
            text = w.get("text")
            if not text:
                print(f"{date} {key}: NO TEXT — skipped"); continue
            fname, secs, kb = render(model, generate_audio, date, key, text)
            print(f"{date} {key:6} -> {fname}  {secs//60}:{secs%60:02d}, {kb} KB")

if __name__ == "__main__":
    main()
