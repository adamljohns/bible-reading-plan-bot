#!/usr/bin/env python3
"""generate-watch-audio.py — narrate a day's five watches with Kokoro (mlx-audio),
TWO-VOICE edition: the narrator reads the watch, and the Scripture passage is
handed off to that BOOK's own voice from the shared map (data/book-voices.json —
the same casting the BTE chapter audio uses), then the narrator returns.

Segments per watch:  [narrator: intro + "Scripture — <ref>" announcement]
                     [book voice: the passage itself]
                     [narrator: summary/reflection/application/prayer/charge]
A watch with no recognizable Scripture block renders entirely in the narrator.
If a passage's book voice IS the narrator voice (Proverbs 1-30 = am_michael),
the passage swaps to bm_george so the handoff stays audible.

Name pronunciation: misaki honors inline [word](/phonemes/) markup, so household
names are locked in a lexicon (Maria = muh-REE-uh, Boaz = BOH-az, Shiloh =
SHY-loh, Gideon = GID-ee-un) instead of trusting the model's guess.

Output: docs/assets/audio/readings/<date>-<name>.mp3 (committed; site-served) —
names wisdom/husband/father/citizen/peace. After rendering re-run
  python3 scripts/build_reading_index.py && python3 scripts/build_reading_page_from_md.py <date>

Run (mlx-audio venv is Python 3.11 — the TTS stack has no cp314 wheels):
  ~/.mlx-audio-venv/bin/python bin/generate-watch-audio.py 2026-07-17 2026-07-18
"""
import json, os, re, sys, glob, tempfile, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
READINGS_JSON = os.path.join(ROOT, "docs", "assets", "readings")
VOICE_MAP = os.path.join(ROOT, "data", "book-voices.json")
OUT = os.path.join(ROOT, "docs", "assets", "audio", "readings")
MODEL_ID = os.environ.get("KOKORO_MODEL", "mlx-community/Kokoro-82M-bf16")
def _map_narrator():
    try:
        n = json.load(open(VOICE_MAP)).get("narrator") or {}
        return n.get("voice", "am_michael")
    except Exception:
        return "am_michael"

NARRATOR = os.environ.get("WATCH_VOICE") or _map_narrator()
NARRATOR_LANG = os.environ.get("WATCH_LANG") or ("b" if NARRATOR.startswith("b") else "a")
ALT_SCRIPTURE = ("am_michael", "a")  # used when a book's voice collides with the narrator
SAMPLE_RATE = 24000
GAP_SECONDS = 0.5

FILE_KEY = {"wisdom": "wisdom", "first": "husband", "second": "father",
            "third": "citizen", "peace": "peace"}

# Household-name lexicon (misaki inline phoneme markup).
LEXICON = {
    "Maria":  "[Maria](/məɹˈiə/)",
    "Boaz":   "[Boaz](/bˈOæz/)",
    "Shiloh": "[Shiloh](/ʃˈIlO/)",
    "Gideon": "[Gideon](/ɡˈɪdiən/)",
}

EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF⭐✅❌️🸻]+"
)
TIMECODE = re.compile(r"^\s*(\d{4})\s+")
SEPARATOR = re.compile(r"^[\s⸻⸏—\-·•]+$")
SCRIPTURE_HDR = re.compile(r"^Scripture\s*[—\-]\s*(.+?)\s*$")
SECTION_HDR = re.compile(
    r"^(Context Summary|Briefing Summary|Field Notes|Situation Report|Reflection\b.*|"
    r"Personal Application\b.*|Prayer\b.*|Helm Command\b.*|The Charge\b.*|Rudder Steer\b.*)")

def load_voice_map():
    data = json.load(open(VOICE_MAP))
    by_name = {}
    for b in data["books"]:
        for n in [b["name"]] + b.get("aliases", []):
            by_name[n.lower()] = b
    return by_name

def book_for_ref(by_name, ref):
    # "Ezekiel 41", "1 Samuel 3:1-10", "Song of Solomon 2" -> map entry
    name = re.sub(r"\s+\d.*$", "", ref).strip().lower()
    return by_name.get(name)

def clean_lines(text):
    out = []
    for raw in text.splitlines():
        line = EMOJI.sub("", raw).strip()
        line = line.replace("**", "").replace("###", "").replace("##", "").lstrip("# ")
        line = TIMECODE.sub("", line)
        out.append(line)
    return out

def apply_lexicon(text):
    for word, marked in LEXICON.items():
        text = re.sub(rf"\b{word}\b", marked, text)
    return text

def segment_watch(text, by_name):
    """Return ([(voice, lang, text), ...], handoff_info) — narrator/scripture/narrator."""
    lines = clean_lines(text)
    pre, passage, post = [], [], []
    state = "pre"
    ref = None
    for line in lines:
        if state == "pre":
            m = SCRIPTURE_HDR.match(line)
            pre.append(line)
            if m:
                ref = m.group(1); state = "passage"
            continue
        if state == "passage":
            if SEPARATOR.match(line) or SECTION_HDR.match(line):
                state = "post"
                if not SEPARATOR.match(line):
                    post.append(line)
                continue
            passage.append(line)
            continue
        if not SEPARATOR.match(line):
            post.append(line)

    def join(ls):
        t = "\n".join(l for l in ls if l != "")
        return re.sub(r"\n{3,}", "\n\n", t).strip()

    entry = book_for_ref(by_name, ref) if ref else None
    pre_t, pas_t, post_t = join(pre), join(passage), join(post)
    NARR_SEG = (NARRATOR, NARRATOR_LANG, "kokoro", 1.0)
    if not entry or not pas_t:
        whole = join([l for l in lines if not SEPARATOR.match(l)])
        return [NARR_SEG + (apply_lexicon(whole),)], None
    sv, sl = entry["voice"], entry.get("lang", "a")
    se, ssp = entry.get("engine", "kokoro"), float(entry.get("speed") or 1.0)
    if sv == NARRATOR:
        sv, sl = ALT_SCRIPTURE
        se, ssp = "kokoro", 1.0
    segs = []
    if pre_t:  segs.append(NARR_SEG + (apply_lexicon(pre_t),))
    segs.append((sv, sl, se, ssp, apply_lexicon(pas_t)))
    if post_t: segs.append(NARR_SEG + (apply_lexicon(post_t),))
    return segs, (entry["name"], sv)

def render_watch(model, gen_audio, date, key, segs):
    with tempfile.TemporaryDirectory(prefix="watch-") as tmp:
        sil = os.path.join(tmp, "sil.wav")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                        "-i", f"anullsrc=r={SAMPLE_RATE}:cl=mono", "-t", str(GAP_SECONDS), sil], check=True)
        parts = []
        for i, (voice, lang, engine, spd, text) in enumerate(segs):
            seg_dir = os.path.join(tmp, f"s{i}"); os.makedirs(seg_dir)
            if engine == "piper":
                pw = os.path.join(seg_dir, "p.wav")
                pmodel = os.path.join(os.path.expanduser("~"), ".piper-voices", f"{voice}.onnx")
                subprocess.run([os.path.join(os.path.expanduser("~"), ".piper-venv", "bin", "python"),
                                "-m", "piper", "-m", pmodel, "--length-scale", str(1.0 / (spd or 1.0)),
                                "--sentence-silence", "0.35", "-f", pw],
                               input=text.encode(), check=True, capture_output=True)
                # piper renders 22.05k; resample to the kokoro concat rate
                rw = os.path.join(seg_dir, "p24.wav")
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", pw,
                                "-ar", str(SAMPLE_RATE), "-ac", "1", rw], check=True)
                wavs = [rw]
            else:
                gen_audio(text=text, model=model, voice=voice, lang_code=lang,
                          output_path=seg_dir, file_prefix="p", join_audio=True,
                          audio_format="wav", verbose=False)
                wavs = sorted(glob.glob(os.path.join(seg_dir, "*.wav")))
            if not wavs:
                raise RuntimeError(f"no wav for {date} {key} segment {i} ({voice})")
            if parts: parts.append(sil)
            parts.append(wavs[0])
        lst = os.path.join(tmp, "list.txt")
        open(lst, "w").write("\n".join(f"file '{p}'" for p in parts))
        os.makedirs(OUT, exist_ok=True)
        mp3 = os.path.join(OUT, f"{date}-{FILE_KEY[key]}.mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                        "-i", lst, "-codec:a", "libmp3lame", "-b:a", "64k", "-ac", "1", mp3], check=True)
    secs = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "default=nk=1:nw=1", mp3], capture_output=True, text=True).stdout.strip())
    return os.path.basename(mp3), int(secs), os.path.getsize(mp3) // 1024

def main():
    dates = sys.argv[1:]
    if not dates:
        print("usage: generate-watch-audio.py <YYYY-MM-DD> [more dates]"); sys.exit(2)
    from mlx_audio.tts.utils import load_model
    from mlx_audio.tts.generate import generate_audio
    by_name = load_voice_map()
    print(f"Loading Kokoro {MODEL_ID} (once); narrator={NARRATOR}...")
    model = load_model(MODEL_ID)
    for date in dates:
        day = json.load(open(os.path.join(READINGS_JSON, f"{date}.json")))
        for key in ["wisdom", "first", "second", "third", "peace"]:
            w = day["watches"].get(key) or {}
            text = w.get("text")
            if not text:
                print(f"{date} {key}: NO TEXT — skipped"); continue
            segs, handoff = segment_watch(text, by_name)
            fname, secs, kb = render_watch(model, generate_audio, date, key, segs)
            tag = f"scripture={handoff[0]}:{handoff[1]}" if handoff else "single-voice"
            print(f"{date} {key:6} -> {fname}  {secs//60}:{secs%60:02d}, {kb} KB  [{tag}]")

if __name__ == "__main__":
    main()
