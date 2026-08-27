#!/usr/bin/env python3
"""generate-mbt-audio-kokoro.py — narrate the clean MBT with Kokoro-82M via mlx-audio.

This supersedes the Piper generator (bin/generate-mbt-audio.js) for Kokoro-voiced
books. Kokoro (Apache-2.0, 54 voices) runs natively on Apple Silicon via MLX and is a
clear quality step up from Piper. Each book gets its own voice, and Proverbs is voiced
per-chapter: a male instructional voice for 1-30 ("my son, hear your father's
discipline") and a mature female voice for 31 (King Lemuel's mother / the woman of
valor). Esther stays on the Piper 'jenny' narration already live on R2 and is only
preserved in the manifest, never re-rendered here.

Source text : docs/assets/mbt/mbt-bible.json  (clean, copyright-safe MBT — never moop-translation.json)
Output      : docs/assets/bible/audio/<book>-<chapter>.mp3  (local, git-ignored)
Upload      : Cloudflare R2  ->  https://audio.usmcmin.org/bible/<book>-<chapter>.mp3
Manifest    : docs/assets/bible/audio-manifest.json  (per-book voice; the BTE reader
              probes each R2 URL and shows the chapter player once the file is live)

Run (from a repo/worktree checkout, using the mlx-audio venv):
  ~/.mlx-audio-venv/bin/python bin/generate-mbt-audio-kokoro.py            # all Kokoro books (8, 20, 57)
  ~/.mlx-audio-venv/bin/python bin/generate-mbt-audio-kokoro.py 20         # just Proverbs
  ~/.mlx-audio-venv/bin/python bin/generate-mbt-audio-kokoro.py 20:31      # one chapter
  SKIP_UPLOAD=1 ~/.mlx-audio-venv/bin/python bin/generate-mbt-audio-kokoro.py 57
"""
import os, sys, glob, json, tempfile, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs", "assets", "mbt", "mbt-bible.json")
OUT = os.path.join(ROOT, "docs", "assets", "bible", "audio")
MANIFEST = os.path.join(ROOT, "docs", "assets", "bible", "audio-manifest.json")
MODEL_ID = os.environ.get("KOKORO_MODEL", "mlx-community/Kokoro-82M-bf16")
R2_REMOTE = os.environ.get("R2_REMOTE", "r2:usmcmin-audio")
R2_PREFIX = "bible"
R2_BASE = "https://audio.usmcmin.org"
LABEL = "AI narration (MBT)"

# Per-book voice config now lives in the SHARED map data/book-voices.json — the
# same casting the daily-reading watch audio uses for Scripture passages. Books
# whose entry carries a "bte" engine override (Esther -> frozen Piper jenny) are
# only listed in the manifest here, never re-rendered. 'overrides' maps a chapter
# number to a different voice (Proverbs 31).
def _load_book_cfg():
    vm = json.load(open(os.path.join(ROOT, "data", "book-voices.json")))
    cfg = {}
    for b in vm["books"]:
        bid = str(b["id"])
        bte = b.get("bte") or {}
        cfg[bid] = {
            "name": b["name"],
            # engine: a bte override (frozen legacy audio, e.g. Esther-jenny) wins,
            # else the book's own engine (James -> piper per PJG-0018), else kokoro
            "engine": bte.get("engine") or b.get("engine") or "kokoro",
            "voice": bte.get("voice", b["voice"]) if bte else b["voice"],
            "lang": b.get("lang", "a"),
            "speed": b.get("speed") or 1.0,
            # a bte block means the live R2 audio is FROZEN as-is: manifest-only, never re-rendered
            "frozen": bool(bte),
            "overrides": b.get("overrides") or {},
        }
    return cfg

BOOK_CFG = _load_book_cfg()

# Books whose BTE audio is PUBLISHED. The shared map casts all 66, but only these
# render/advertise here. Psalms (19) publishes SPARSELY: the reader probes each
# chapter URL and only shows a player where the mp3 is live, so authored psalms
# get audio while the rest of the book stays silent.
BTE_BOOKS = {"8", "17", "19", "20", "21", "57", "59"}

# Friendly per-book voice descriptor for the manifest (metadata; reader shows LABEL).
def voice_desc(b):
    cfg = BOOK_CFG[b]
    if cfg["engine"] == "piper":
        return f"{cfg['voice']} (Piper)"
    ov = cfg.get("overrides") or {}
    if ov:
        base = f"{cfg['voice']} (Kokoro, ch 1-30)"
        extra = "; ".join(f"{o['voice']} (Kokoro, ch {c})" for c, o in sorted(ov.items(), key=lambda x: int(x[0])))
        return f"{base}; {extra}"
    return f"{cfg['voice']} (Kokoro)"


def index_source():
    data = json.load(open(SRC))
    idx = {}
    for key, text in data.items():
        b, c, v = key.split("_")
        if b not in BTE_BOOKS:
            continue
        idx.setdefault(b, {}).setdefault(c, []).append((int(v), text))
    for b in idx:
        for c in idx[b]:
            idx[b][c].sort(key=lambda t: t[0])
    return idx


def chapter_text(b, c, verses):
    header = f"{BOOK_CFG[b]['name']}, chapter {c}."
    return header + " " + " ".join(t for _, t in verses)


def voice_for(b, c):
    cfg = BOOK_CFG[b]
    ov = (cfg.get("overrides") or {}).get(str(c))
    if ov:
        return ov["voice"], ov.get("lang", cfg.get("lang", "a"))
    return cfg["voice"], cfg.get("lang", "a")


def render_chapter(model, gen_audio, b, c, verses):
    voice, lang = voice_for(b, c)
    text = chapter_text(b, c, verses)
    with tempfile.TemporaryDirectory(prefix="kokoro-") as tmp:
        if BOOK_CFG[b]["engine"] == "piper":
            # Piper-cast book (e.g. James -> SgtMaj Mac / en_US-joe-medium):
            # same invocation as generate-watch-audio.py's piper segments.
            wav = os.path.join(tmp, f"{b}-{c}.wav")
            pmodel = os.path.join(os.path.expanduser("~"), ".piper-voices", f"{voice}.onnx")
            spd = BOOK_CFG[b].get("speed") or 1.0
            subprocess.run(
                [os.path.join(os.path.expanduser("~"), ".piper-venv", "bin", "python"),
                 "-m", "piper", "-m", pmodel,
                 "--length-scale", str(1.0 / spd),
                 "--sentence-silence", "0.35", "-f", wav],
                input=text.encode(), check=True, capture_output=True)
            wavs = [wav]
        else:
            gen_audio(text=text, model=model, voice=voice, lang_code=lang,
                      output_path=tmp, file_prefix=f"{b}-{c}", join_audio=True,
                      audio_format="wav", verbose=False)
            wavs = sorted(glob.glob(os.path.join(tmp, "*.wav")))
        if not wavs:
            raise RuntimeError(f"no wav produced for {b}:{c}")
        os.makedirs(OUT, exist_ok=True)
        mp3 = os.path.join(OUT, f"{b}-{c}.mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wavs[0],
                        "-codec:a", "libmp3lame", "-b:a", "64k", "-ac", "1", mp3], check=True)
    kb = os.path.getsize(mp3) // 1024
    if not os.environ.get("SKIP_UPLOAD"):
        subprocess.run(["rclone", "copy", mp3, f"{R2_REMOTE}/{R2_PREFIX}/"], check=True)
    return mp3, voice, kb


def sync_manifest(idx):
    try:
        m = json.load(open(MANIFEST))
    except Exception:
        m = {}
    m["voice"] = "Per-book casting from data/book-voices.json — Kokoro-82M via mlx-audio; James on Piper joe; Esther frozen on Piper jenny"
    m["engine"] = "kokoro (mlx-audio) + piper (James, Esther)"
    m["label"] = LABEL
    m["base"] = R2_BASE
    m["prefix"] = R2_PREFIX
    m["note"] = ("Per-chapter MBT narration on Cloudflare R2 at <base>/<prefix>/<book>-<chapter>.mp3. "
                 "Casting follows data/book-voices.json (books follow their agents): Ruth=bf_emma, "
                 "Psalms=am_adam (sparse — only authored psalms have audio), Proverbs=bm_george ch1-30 + "
                 "af_heart ch31, Ecclesiastes=bm_lewis, Philemon=am_onyx on Kokoro-82M; James=en_US-joe "
                 "(Piper, SgtMaj Mac); Esther keeps its frozen Piper 'jenny' narration. The reader probes "
                 "each URL and shows the player once the file is live.")
    m["books"] = {}
    for b in sorted(BOOK_CFG, key=int):
        if b not in idx:
            continue
        maxch = max(int(c) for c in idx[b])
        m["books"][b] = {"name": BOOK_CFG[b]["name"], "chapters": maxch, "voice": voice_desc(b)}
    with open(MANIFEST, "w") as f:
        json.dump(m, f, indent=2)
        f.write("\n")


def main():
    from mlx_audio.tts.utils import load_model
    from mlx_audio.tts.generate import generate_audio

    idx = index_source()

    # Targets: bare book id, or book:chapter. Default = all Kokoro books.
    args = sys.argv[1:]
    targets = []
    for a in args:
        if ":" in a:
            b, c = a.split(":"); targets.append((b, c))
        elif a in idx:
            targets += [(a, c) for c in sorted(idx[a], key=int)]
    if not targets:
        for b, cfg in BOOK_CFG.items():
            if not cfg["frozen"] and b in idx:
                targets += [(b, c) for c in sorted(idx[b], key=int)]

    print(f"Loading Kokoro model {MODEL_ID} (once)...")
    model = load_model(MODEL_ID)
    print(f"Rendering {len(targets)} chapter(s)...")
    for b, c in targets:
        if BOOK_CFG.get(b, {}).get("frozen"):
            print(f"skip {b}:{c} (frozen legacy audio — manifest-only)"); continue
        verses = idx.get(b, {}).get(str(c))
        if not verses:
            print(f"skip {b}:{c} (no MBT text)"); continue
        mp3, voice, kb = render_chapter(model, generate_audio, b, str(c), verses)
        tag = "" if os.environ.get("SKIP_UPLOAD") else " [R2]"
        print(f"{BOOK_CFG[b]['name']} {c} -> bible/{b}-{c}.mp3  voice={voice}  {kb} KB{tag}")

    sync_manifest(idx)
    print("manifest updated:", MANIFEST)


if __name__ == "__main__":
    main()
