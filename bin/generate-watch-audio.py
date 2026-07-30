#!/usr/bin/env python3
"""generate-watch-audio.py — narrate a day's five watches with Kokoro (mlx-audio),
THREE-VOICE edition (2026-07-29 product lock; PJG-0018 2026-07-30 polish):
  - narrator (Kokoro, PJ/watch desk) = intro + context/reflection/apps + charge
  - book voice (data/book-voices.json) = Scripture passage
  - Adam clone (F5-TTS-MLX) = Prayer body only

Segments per watch:
  [narrator: intro + "Scripture — <ref>" announcement]
  [book voice: the passage itself]
  [narrator: summary/reflection/application]
  [adam-clone F5: Prayer]   # when USE_ADAM_PRAYER=1 (default) and F5 ref present
  [narrator: Watch Charge]

A watch with no recognizable Scripture block renders entirely in the narrator
(still splits prayer to Adam clone when available).
If a passage's book voice IS the narrator voice, the passage swaps to am_michael
so the handoff stays audible.
Set USE_ADAM_PRAYER=0 to keep prayer on narrator (faster / offline fallback).

Name pronunciation: misaki honors inline [word](/phonemes/) markup, so household
names are locked in a lexicon (Maria = muh-REE-uh, Boaz = BOH-az, Shiloh =
SHY-loh, Gideon = GID-ee-un) instead of trusting the model's guess.

Output: docs/assets/audio/readings/<date>-<name>.mp3 (committed; site-served) —
names wisdom/husband/father/citizen/peace. After rendering re-run
  python3 scripts/build_reading_index.py && python3 scripts/build_reading_page_from_md.py <date>

Run (mlx-audio venv is Python 3.11 — the TTS stack has no cp314 wheels):
  ~/.mlx-audio-venv/bin/python bin/generate-watch-audio.py 2026-07-17 2026-07-18
"""
import json, os, re, sys, glob, tempfile, subprocess, shutil

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
USE_ADAM_PRAYER = os.environ.get("USE_ADAM_PRAYER", "1") not in ("0", "false", "False", "no")
F5_REF = os.path.expanduser(os.environ.get(
    "F5_REF_AUDIO", "~/Documents/05-Voice/f5tts-tests/ref-calm.wav"))
F5_REFTEXT_PATH = os.path.expanduser(os.environ.get(
    "F5_REF_TEXT", "~/Documents/05-Voice/f5tts-tests/ref-calm.txt"))
F5_VENV_PY = os.path.expanduser(os.environ.get(
    "F5_VENV_PY", "~/.venvs/f5tts/bin/python"))
F5_REF_SEC = float(os.environ.get("F5_REF_SEC", "15.0"))
F5_CPS = float(os.environ.get("F5_CPS", "12.5"))
F5_BUFFER = float(os.environ.get("F5_BUFFER", "0.6"))
F5_STEPS = int(os.environ.get("F5_STEPS", "32"))
F5_CHUNK_MAX = int(os.environ.get("F5_CHUNK_MAX", "160"))
SAMPLE_RATE = 24000
GAP_SECONDS = 0.65  # PJG-0018: slightly longer handoff cushion (clone/narrator)

FILE_KEY = {"wisdom": "wisdom", "first": "husband", "second": "father",
            "third": "citizen", "peace": "peace"}

# Household-name lexicon (misaki inline phoneme markup).
LEXICON = {
    "Maria":  "[Maria](/məɹˈiə/)",
    "Boaz":   "[Boaz](/bˈOæz/)",
    "Shiloh": "[Shiloh](/ʃˈIlO/)",
    "Gideon": "[Gideon](/ɡˈɪdiən/)",
}

# PJG-0018 (2026-07-30): homage "bow" must be /baʊ/, never long-o /boʊ/.
# Applied via context rewrite before phoneme markup (see apply_bow_homage).
BOW_HOMAGE_RE = re.compile(
    r"\b[Bb]ow(?:ed|ing)?\b(?=\s+(?:down|before|to|unto|low|themselves|himself|herself|myself|ourselves|yourselves))",
    re.I,
)
BOW_HOMAGE_RE2 = re.compile(
    r"\b(?:and|they|he|she|we|ye|you|I)\s+[Bb]owed\b",
    re.I,
)

def apply_bow_homage(text: str) -> str:
    """Force homage/bow-down readings to /baʊ/ (not /boʊ/ as in bow-and-arrow)."""
    def _sub(m):
        w = m.group(0)
        low = w.lower()
        if low == "bow":
            return "[bow](/baʊ/)"
        if low == "bowed":
            return "[bowed](/baʊd/)"
        if low == "bowing":
            return "[bowing](/ˈbaʊɪŋ/)"
        return w
    text = BOW_HOMAGE_RE.sub(_sub, text)
    # bare "bowed" after pronouns still homage in Esther narrative
    def _sub2(m):
        full = m.group(0)
        return re.sub(r"[Bb]owed", "[bowed](/baʊd/)", full)
    text = BOW_HOMAGE_RE2.sub(_sub2, text)
    return text


def force_declarative_amen(text: str) -> str:
    """Final Amen must be statement, never rising question (Adam 2026-07-30)."""
    # Strip ?/! after Amen anywhere; ensure terminal period; lock falling stress.
    text = re.sub(r"\bAmen\b\s*[?!]+", "Amen.", text, flags=re.I)
    text = re.sub(r"\bAmen\b(?!\s*\.|\s*\[/)", "Amen.", text, flags=re.I)
    text = re.sub(r"\bAmen\.(?=\s|$)", "[Amen](/ˈɑːmɛn/).", text, flags=re.I)
    return text

EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF⭐✅❌️🸻]+"
)
TIMECODE = re.compile(r"^\s*(\d{4})\s+")
SEPARATOR = re.compile(r"^[\s⸻⸏—\-·•]+$")
SCRIPTURE_HDR = re.compile(r"^Scripture\s*[—\-]\s*(.+?)\s*$")
SECTION_HDR = re.compile(
    r"^(Context Summary|Briefing Summary|Field Notes|Situation Report|Reflection\b.*|"
    r"Personal Application\b.*|Prayer\b.*|Helm Command\b.*|Watch Charge\b.*|"
    r"The Charge\b.*|Rudder Steer\b.*)")
PRAYER_HDR = re.compile(r"^Prayer\b.*", re.I)
CHARGE_HDR = re.compile(r"^(Helm Command|Watch Charge|The Charge|Rudder Steer)\b.*", re.I)


def load_voice_map():
    data = json.load(open(VOICE_MAP))
    banned_voices = set(data.get("banned_voices") or [])
    banned_agents = set(data.get("banned_scripture_agents") or ["coach-arnie"])
    # Hard fallback if map still carries a banned agent/voice (defense in depth).
    FALLBACK_BOOK = {
        "voice": "am_onyx", "lang": "a", "engine": "kokoro",
        "agent": "bg-hartwell",
        "note": "auto-fallback: banned scripture voice/agent blocked (PJG-0018)",
    }
    by_name = {}
    for b in data["books"]:
        bb = dict(b)
        if bb.get("agent") in banned_agents or bb.get("voice") in banned_voices:
            bb = {**bb, **FALLBACK_BOOK, "name": b["name"],
                  "aliases": b.get("aliases", []), "id": b.get("id")}
            print(f"WARN voice-map: blocked banned cast on {b.get('name')} "
                  f"({b.get('agent')}/{b.get('voice')}) → {bb['agent']}/{bb['voice']}",
                  flush=True)
        for n in [bb["name"]] + bb.get("aliases", []):
            by_name[n.lower()] = bb
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
    text = apply_bow_homage(text)
    for word, marked in LEXICON.items():
        text = re.sub(rf"\b{word}\b", marked, text)
    text = force_declarative_amen(text)
    return text


def f5_prep(text):
    text = text.replace("LORD", "Lord")
    text = re.sub(r"[—–]", ", ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = force_declarative_amen(text)
    # strip misaki markup for F5 (clone stack is plain text)
    text = re.sub(r"\[([^\]]+)\]\(/[^/)]+/\)", r"\1", text)
    return text.strip()


def f5_chunks(text, mx=None):
    mx = mx or F5_CHUNK_MAX
    sents = re.split(r"(?<=[.!?])\s+", text)
    out, cur = [], ""
    for s in sents:
        cand = (cur + " " + s).strip() if cur else s
        if len(cand) <= mx or not cur:
            cur = cand
        else:
            out.append(cur)
            cur = s
    if cur:
        out.append(cur)
    final = []
    for c in out:
        while len(c) > mx + 60:
            cut = c.rfind(",", 0, mx)
            cut = cut if cut > 40 else mx
            final.append(c[:cut].strip())
            c = c[cut:].strip(" ,")
        if c:
            final.append(c)
    return [c for c in final if c]


def adam_prayer_ready():
    return (USE_ADAM_PRAYER
            and os.path.isfile(F5_REF)
            and os.path.isfile(F5_VENV_PY)
            and os.path.isfile(F5_REFTEXT_PATH))


def join_lines(ls):
    t = "\n".join(l for l in ls if l != "")
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def split_prayer(post_lines):
    """Split post-scripture body into before / prayer / after.

    Prayer ends at the first Amen line (or Charge header). Anything after
    Amen (e.g. "This Day in American History") returns to narrator — never
    into Adam's clone voice.
    """
    before, prayer, after = [], [], []
    st = "before"
    amen_end = re.compile(r"\bAmen\.?\s*$", re.I)
    for line in post_lines:
        if st == "before" and PRAYER_HDR.match(line):
            st = "prayer"
            prayer.append(line)
            continue
        if st == "prayer" and CHARGE_HDR.match(line):
            st = "after"
            after.append(line)
            continue
        if st == "before":
            before.append(line)
        elif st == "prayer":
            prayer.append(line)
            if amen_end.search(line):
                st = "after"
        else:
            after.append(line)
    return before, prayer, after


def segment_watch(text, by_name):
    """Return (segs, handoff_info). segs = (voice, lang, engine, speed, text)."""
    lines = clean_lines(text)
    pre, passage, post = [], [], []
    state = "pre"
    ref = None
    for line in lines:
        if state == "pre":
            m = SCRIPTURE_HDR.match(line)
            pre.append(line)
            if m:
                ref = m.group(1)
                state = "passage"
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

    entry = book_for_ref(by_name, ref) if ref else None
    pre_t, pas_t = join_lines(pre), join_lines(passage)
    NARR_SEG = (NARRATOR, NARRATOR_LANG, "kokoro", 1.0)
    ADAM_SEG = ("adam-clone", "a", "f5", 1.0)
    use_adam = adam_prayer_ready()

    def append_post(segs, post_lines):
        before, prayer, after = split_prayer(post_lines)
        if join_lines(before):
            segs.append(NARR_SEG + (apply_lexicon(join_lines(before)),))
        if join_lines(prayer):
            if use_adam:
                segs.append(ADAM_SEG + (f5_prep(join_lines(prayer)),))
            else:
                segs.append(NARR_SEG + (apply_lexicon(join_lines(prayer)),))
        if join_lines(after):
            segs.append(NARR_SEG + (apply_lexicon(join_lines(after)),))
        return bool(join_lines(prayer) and use_adam)

    if not entry or not pas_t:
        body_lines = [l for l in lines if not SEPARATOR.match(l)]
        segs = []
        had_prayer = append_post(segs, body_lines)
        if not segs:
            segs = [NARR_SEG + (apply_lexicon(join_lines(body_lines)),)]
        tag = "+adam-prayer" if had_prayer else ""
        return segs, (None, None, tag) if tag else None

    sv, sl = entry["voice"], entry.get("lang", "a")
    se, ssp = entry.get("engine", "kokoro"), float(entry.get("speed") or 1.0)
    if sv == NARRATOR:
        sv, sl = ALT_SCRIPTURE
        se, ssp = "kokoro", 1.0
    segs = []
    if pre_t:
        segs.append(NARR_SEG + (apply_lexicon(pre_t),))
    segs.append((sv, sl, se, ssp, apply_lexicon(pas_t)))
    had_prayer = append_post(segs, post)
    tag_extra = "+adam-prayer" if had_prayer else ""
    return segs, (entry["name"], sv, tag_extra)


def render_f5_text(text, out_wav):
    """Render prayer text with Adam's F5 clone; write 24k mono wav."""
    reftext = open(F5_REFTEXT_PATH).read().strip()
    chunks = f5_chunks(text)
    if not chunks:
        raise RuntimeError("empty F5 prayer text")
    tmp = tempfile.mkdtemp(prefix="f5prayer-")
    try:
        parts = []
        for i, c in enumerate(chunks):
            raw = os.path.join(tmp, f"c{i:02d}.wav")
            dur = round(F5_REF_SEC + len(c) / F5_CPS + F5_BUFFER)
            cmd = [F5_VENV_PY, "-m", "f5_tts_mlx.generate",
                   "--text", c, "--ref-audio", F5_REF, "--ref-text", reftext,
                   "--duration", str(dur), "--steps", str(F5_STEPS),
                   "--output", raw]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if not os.path.isfile(raw):
                raise RuntimeError(
                    f"F5 failed chunk {i}: {(r.stderr or r.stdout or '')[-400:]}")
            rw = os.path.join(tmp, f"c{i:02d}_24.wav")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw,
                            "-ar", str(SAMPLE_RATE), "-ac", "1", rw], check=True)
            parts.append(rw)
        if len(parts) == 1:
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", parts[0],
                            "-ar", str(SAMPLE_RATE), "-ac", "1", out_wav], check=True)
        else:
            lst = os.path.join(tmp, "list.txt")
            open(lst, "w").write("\n".join(f"file '{p}'" for p in parts))
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat",
                            "-safe", "0", "-i", lst, "-ar", str(SAMPLE_RATE),
                            "-ac", "1", out_wav], check=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def render_watch(model, gen_audio, date, key, segs):
    with tempfile.TemporaryDirectory(prefix="watch-") as tmp:
        sil = os.path.join(tmp, "sil.wav")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                        "-i", f"anullsrc=r={SAMPLE_RATE}:cl=mono",
                        "-t", str(GAP_SECONDS), sil], check=True)
        parts = []
        for i, (voice, lang, engine, spd, text) in enumerate(segs):
            seg_dir = os.path.join(tmp, f"s{i}")
            os.makedirs(seg_dir)
            if engine == "piper":
                pw = os.path.join(seg_dir, "p.wav")
                pmodel = os.path.join(os.path.expanduser("~"),
                                      ".piper-voices", f"{voice}.onnx")
                subprocess.run(
                    [os.path.join(os.path.expanduser("~"), ".piper-venv", "bin", "python"),
                     "-m", "piper", "-m", pmodel,
                     "--length-scale", str(1.0 / (spd or 1.0)),
                     "--sentence-silence", "0.35", "-f", pw],
                    input=text.encode(), check=True, capture_output=True)
                rw = os.path.join(seg_dir, "p24.wav")
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", pw,
                                "-ar", str(SAMPLE_RATE), "-ac", "1", rw], check=True)
                wavs = [rw]
            elif engine == "f5":
                fw = os.path.join(seg_dir, "p24.wav")
                try:
                    render_f5_text(text, fw)
                    wavs = [fw]
                except Exception as e:
                    print(f"  WARN F5 prayer failed ({e}); "
                          f"falling back to narrator for this segment", flush=True)
                    gen_audio(text=apply_lexicon(text), model=model, voice=NARRATOR,
                              lang_code=NARRATOR_LANG, output_path=seg_dir,
                              file_prefix="p", join_audio=True,
                              audio_format="wav", verbose=False)
                    wavs = sorted(glob.glob(os.path.join(seg_dir, "*.wav")))
            else:
                gen_audio(text=text, model=model, voice=voice, lang_code=lang,
                          output_path=seg_dir, file_prefix="p", join_audio=True,
                          audio_format="wav", verbose=False)
                wavs = sorted(glob.glob(os.path.join(seg_dir, "*.wav")))
            if not wavs:
                raise RuntimeError(f"no wav for {date} {key} segment {i} ({voice})")
            if parts:
                parts.append(sil)
            parts.append(wavs[0])
        os.makedirs(OUT, exist_ok=True)
        mp3 = os.path.join(OUT, f"{date}-{FILE_KEY[key]}.mp3")
        # Soft-join segments: short acrossfades reduce clone/prayer cut-outs (PJG-0018).
        if len(parts) == 1:
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", parts[0],
                            "-codec:a", "libmp3lame", "-b:a", "64k", "-ac", "1", mp3],
                           check=True)
        else:
            # Build filter: [0][1]acrossfade ... then encode.
            # parts alternate speech, silence, speech, silence... — acrossfade only
            # speech→speech would remove intentional pauses; keep concat + pad silence,
            # but apply a 25ms fade-in/out on each speech file before concat.
            faded = []
            for i, part in enumerate(parts):
                fw = os.path.join(tmp, f"fade{i}.wav")
                # silence parts stay flat; speech gets tiny edge fades
                is_sil = os.path.basename(part).startswith("sil") or part.endswith("sil.wav")
                if is_sil:
                    faded.append(part)
                else:
                    subprocess.run([
                        "ffmpeg", "-y", "-loglevel", "error", "-i", part,
                        "-af", "afade=t=in:st=0:d=0.035,areverse,afade=t=in:st=0:d=0.05,areverse",
                        fw
                    ], check=True)
                    faded.append(fw)
            lst = os.path.join(tmp, "list.txt")
            open(lst, "w").write("\n".join(f"file '{p}'" for p in faded))
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat",
                            "-safe", "0", "-i", lst, "-codec:a", "libmp3lame",
                            "-b:a", "64k", "-ac", "1", mp3], check=True)
    secs = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nk=1:nw=1", mp3],
        capture_output=True, text=True).stdout.strip())
    return os.path.basename(mp3), int(secs), os.path.getsize(mp3) // 1024


def main():
    dates = sys.argv[1:]
    if not dates:
        print("usage: generate-watch-audio.py <YYYY-MM-DD> [more dates]")
        sys.exit(2)
    from mlx_audio.tts.utils import load_model
    from mlx_audio.tts.generate import generate_audio
    by_name = load_voice_map()
    prayer_mode = "adam-clone-F5" if adam_prayer_ready() else "narrator-fallback"
    print(f"Loading Kokoro {MODEL_ID} (once); narrator={NARRATOR}; "
          f"prayer={prayer_mode}...", flush=True)
    model = load_model(MODEL_ID)
    for date in dates:
        day = json.load(open(os.path.join(READINGS_JSON, f"{date}.json")))
        for key in ["wisdom", "first", "second", "third", "peace"]:
            w = day["watches"].get(key) or {}
            text = w.get("text")
            if not text:
                print(f"{date} {key}: NO TEXT — skipped")
                continue
            segs, handoff = segment_watch(text, by_name)
            fname, secs, kb = render_watch(model, generate_audio, date, key, segs)
            if handoff and handoff[0]:
                tag = f"scripture={handoff[0]}:{handoff[1]}{handoff[2]}"
            elif handoff:
                tag = f"single-voice{handoff[2]}"
            else:
                tag = "single-voice"
            print(f"{date} {key:6} -> {fname}  {secs//60}:{secs%60:02d}, "
                  f"{kb} KB  [{tag}]", flush=True)


if __name__ == "__main__":
    main()
