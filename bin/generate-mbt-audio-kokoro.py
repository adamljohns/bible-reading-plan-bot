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

# Per-book voice config. engine 'kokoro' books are rendered here; 'piper' books
# (Esther) are only listed in the manifest — their MP3s already live on R2.
# 'overrides' maps a chapter number to a different voice (Proverbs 31).
BOOK_CFG = {
    "8":  {"name": "Ruth",     "engine": "kokoro", "voice": "bf_emma",    "lang": "b"},
    "17": {"name": "Esther",   "engine": "piper",  "voice": "en_GB-jenny_dioco-medium"},
    "20": {"name": "Proverbs", "engine": "kokoro", "voice": "am_michael", "lang": "a",
           "overrides": {"31": {"voice": "af_heart", "lang": "a"}}},
    "57": {"name": "Philemon", "engine": "kokoro", "voice": "bm_daniel",  "lang": "b"},
}

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
        if b not in BOOK_CFG:
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
    m["voice"] = "Kokoro-82M via mlx-audio, per book; Esther on Piper en_GB-jenny"
    m["engine"] = "kokoro (mlx-audio) + piper (Esther)"
    m["label"] = LABEL
    m["base"] = R2_BASE
    m["prefix"] = R2_PREFIX
    m["note"] = ("Per-chapter MBT narration on Cloudflare R2 at <base>/<prefix>/<book>-<chapter>.mp3. "
                 "Kokoro-82M (Apache-2.0) via mlx-audio on Apple Silicon voices Ruth/Proverbs/Philemon; "
                 "Proverbs is voiced per-chapter (male for 1-30, mature female for 31). Esther keeps its "
                 "Piper 'jenny' narration. The reader probes each URL and shows the player once live.")
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
            if cfg["engine"] == "kokoro" and b in idx:
                targets += [(b, c) for c in sorted(idx[b], key=int)]

    print(f"Loading Kokoro model {MODEL_ID} (once)...")
    model = load_model(MODEL_ID)
    print(f"Rendering {len(targets)} chapter(s)...")
    for b, c in targets:
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
