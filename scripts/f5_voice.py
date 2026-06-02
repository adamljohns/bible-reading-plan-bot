#!/usr/bin/env python3
"""
f5_voice.py — Generate a watch's audio in Adam's cloned voice via F5-TTS-MLX,
then SELF-VERIFY faithfulness with Whisper (no human ears required).

Solved config (2026-06-02):
  - F5 --duration is TOTAL SECONDS (ref + gen), output is the GEN portion only.
    duration = REF_SEC + chars/CPS + BUFFER. Passing frames made F5 over-stretch
    and hallucinate; passing the right seconds gives WER 0.0.
  - "LORD" -> "Lord" for the TTS text (all-caps makes F5 spell it "Lord-D").
  - No trim (output has no ref echo when --duration is set).
  - Reference: Adam's clean Psalm 1 reading (ref-clean.wav, 17s) -> speaker
    similarity 0.871 vs his voice (ceiling 0.941, generic floor 0.655).

USAGE
  python3 scripts/f5_voice.py 2026-06-02 wisdom            # one watch -> mp3 + WER
  python3 scripts/f5_voice.py 2026-06-02 wisdom --verify-only /path.mp3
"""
import argparse, contextlib, importlib.util, json, re, subprocess, sys, tempfile, wave
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VOICE_DIR = Path.home() / "Documents" / "05-Voice" / "f5tts-tests"
REF = VOICE_DIR / "ref-clean.wav"
REFTEXT = (VOICE_DIR / "ref-clean.txt").read_text().strip() if (VOICE_DIR / "ref-clean.txt").exists() else ""
REF_SEC = 17.0
CPS = 12.5          # chars/sec target pace (empirically faithful)
BUFFER = 0.6        # seconds of headroom so the first word isn't clipped
STEPS = 32
CHUNK_MAX = 200     # chars per F5 call (144 verified WER 0.0; keep margin)
AUDIO_OUT = REPO / "docs" / "assets" / "audio" / "readings"

VENV_PY = str(Path.home() / ".venvs/f5tts/bin/python")
WHISPER = "/opt/homebrew/bin/whisper-cli"
WMODEL = str(Path.home() / ".openclaw/whisper_models/ggml-small.en.bin")
FFMPEG = "/opt/homebrew/bin/ffmpeg"


def _gen_mod():
    spec = importlib.util.spec_from_file_location("g", REPO / "scripts" / "generate_audio.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def watch_tts_text(date, watch):
    """Reuse the ElevenLabs pipeline's clean TTS extraction, then F5-prep."""
    g = _gen_mod()
    md = (REPO / "data" / "readings" / f"{date}.md").read_text()
    watches = g.split_watches(md)
    # generate_audio.py keys watches by wisdom/husband/father/citizen/peace
    alias = {"first": "husband", "second": "father", "third": "citizen"}
    key = alias.get(watch, watch)
    if key not in watches:
        sys.exit(f"watch {watch} not in {date}")
    text = g.watch_text_for_tts(watches[key])
    return f5_prep(text)


def f5_prep(text):
    text = text.replace("LORD", "Lord")          # all-caps confuses F5 pronunciation
    text = re.sub(r"[—–]", ", ", text)           # em/en dashes -> comma pause
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def chunk(text, mx=CHUNK_MAX):
    sents = re.split(r"(?<=[.!?])\s+", text)
    out, cur = [], ""
    for s in sents:
        cand = (cur + " " + s).strip() if cur else s
        if len(cand) <= mx or not cur:
            cur = cand
        else:
            out.append(cur); cur = s
    if cur:
        out.append(cur)
    # hard-split any monster chunk
    final = []
    for c in out:
        while len(c) > mx + 60:
            cut = c.rfind(",", 0, mx)
            cut = cut if cut > 40 else mx
            final.append(c[:cut].strip()); c = c[cut:].strip(" ,")
        final.append(c)
    return [c for c in final if c]


def f5_chunk(text, out_wav):
    dur = round(REF_SEC + len(text) / CPS + BUFFER)
    cmd = [VENV_PY, "-m", "f5_tts_mlx.generate", "--text", text, "--ref-audio", str(REF),
           "--ref-text", REFTEXT, "--duration", str(dur), "--steps", str(STEPS),
           "--output", str(out_wav)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not Path(out_wav).exists():
        print(r.stderr[-400:], file=sys.stderr); return False
    return True


def transcribe(wav16):
    out = subprocess.run([WHISPER, "-m", WMODEL, "-f", wav16], capture_output=True, text=True)
    txt = []
    for l in out.stdout.splitlines():
        m = re.match(r"^\s*\[[\d:.\->\s]+\]\s*(.*)", l)
        if m and m.group(1).strip():
            txt.append(m.group(1).strip())
    return " ".join(txt)


def wer(ref, hyp):
    def n(t): return re.sub(r"[^a-z0-9 ]", " ", t.lower()).split()
    r, h = n(ref), n(hyp)
    d = [[0]*(len(h)+1) for _ in range(len(r)+1)]
    for i in range(len(r)+1): d[i][0] = i
    for j in range(len(h)+1): d[0][j] = j
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            c = 0 if r[i-1] == h[j-1] else 1
            d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+c)
    return d[len(r)][len(h)]/max(1, len(r))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("date"); ap.add_argument("watch")
    ap.add_argument("--out")
    args = ap.parse_args()

    text = watch_tts_text(args.date, args.watch)
    chunks = chunk(text)
    out_mp3 = Path(args.out) if args.out else AUDIO_OUT / f"{args.date}-{args.watch}.mp3"
    out_mp3.parent.mkdir(parents=True, exist_ok=True)
    print(f"[{args.date} {args.watch}] {len(text)} chars -> {len(chunks)} chunks", flush=True)

    with tempfile.TemporaryDirectory() as tmp:
        wavs = []
        for i, c in enumerate(chunks):
            w = f"{tmp}/c{i:02d}.wav"
            print(f"  chunk {i+1}/{len(chunks)} ({len(c)} chars)", flush=True)
            if not f5_chunk(c, w):
                sys.exit(f"  chunk {i} failed")
            wavs.append(w)
        listing = f"{tmp}/list.txt"
        Path(listing).write_text("\n".join(f"file '{w}'" for w in wavs) + "\n")
        subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat",
                        "-safe", "0", "-i", listing, "-ac", "1", "-ar", "24000", "-b:a", "128k",
                        str(out_mp3)], check=True)
        # self-verify
        wav16 = f"{tmp}/full16.wav"
        subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", str(out_mp3),
                        "-ac", "1", "-ar", "16000", wav16], check=True)
        with contextlib.closing(wave.open(wav16)) as f:
            dur = f.getnframes()/f.getframerate()
        heard = transcribe(wav16)
        w = wer(text, heard)
    print(json.dumps({"mp3": str(out_mp3), "audio_sec": round(dur, 1),
                      "wer": round(w, 3), "cps": round(len(text)/max(dur, 0.1), 1)}))
    if w > 0.12:
        print("  ⚠ WER high — review", file=sys.stderr); sys.exit(2)


if __name__ == "__main__":
    main()
