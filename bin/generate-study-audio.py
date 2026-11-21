#!/usr/bin/env python3
"""generate-study-audio.py — narrated audio + word-follow timings for a study page.

    ~/.mlx-audio-venv/bin/python bin/generate-study-audio.py <slug> [options]

    --page PATH   page to narrate (default: docs/verse/<slug>.html, else
                  docs/drafts/verse/<slug>.html)
    --dry-run     print the narration script and stop (no TTS, no files)
    --upload      after the bake, `rclone copy` the MP3 to R2 (refuses unless
                  the deploy-r2.yml exclude for assets/media/studies/ is on main)
    --upload-only skip the bake; just copy the existing local master to R2
    --reuse-mp3   skip TTS; re-time the existing local master MP3 (needs the
                  .units.json written by a previous bake)
    --blog        a blog post: page docs/blog/<slug>.html, MP3 under
                  assets/media/blog/, words in docs/assets/blog/<slug>-words.json

Built for the deep verse studies; works on any page that marks a follow root.

BLOG MODE (--blog, 2026-11-20). The post marks its own follow root (the
<article>, with data-read-follow and an id) and data-no-follow on the dateline,
the sources list, the call-to-action box and the post nav. On top of the rules
below, blog mode reads each <figure> as one short line, "Graphic: <first
sentence of its first image's alt text>", and skips the figure's caption; and in a <blockquote> that
carries data-say-before, the trailing "(citation)" is not spoken, because the
attribution was already said in front of the quotation. Raw URLs are never
spoken (speakable() drops them).

WHAT IT READS. The page itself, the same DOM the reader's follow-along JS
(docs/assets/js/read-scroll.js) wraps word by word:
  * the element with a `data-read-follow` attribute is the follow root; its id
    is the key in the words file (the readings pages use the watch id);
  * text inside `[data-no-follow]`, button, audio, script, style and nav is not
    spoken (draft banner, the WEB rendering, citations, the player itself);
  * `data-say="..."` replaces what an element's subtree says aloud (a word-study
    headline is spoken as "heterozugeo, rendered: unequally yoked together");
  * `data-say-before="..."` speaks a short line before an element (the spoken
    attribution in front of a quotation: "The 1689 Confession says:");
  * `data-voice="book"` reads that element in the book's Scripture voice from
    data/book-voices.json, the way the daily watches hand the passage over.
The renderer (bin/verse-study-render.js) emits these attributes on every study.

VOICE. The daily-watch narrator (data/book-voices.json "narrator", bm_george on
2026-11-20) on Kokoro-82M via mlx-audio, locally, no cloud model. Text prep is
the watch generator's own apply_lexicon (Scripture refs, homographs, acronyms).

TIMINGS. The same pipeline as the daily readings' <day>-words.json: whisper
small.en word stamps cut at pauses by ~/Scripts/pj-words-chunked.py, run on the
finished MP3. The whisper words are then lined up with the narration script and
the script with the page's own words (difflib), so each {t, w} in the output
carries the page's spelling of the word. read-scroll.js aligns those to the
spans exactly as it does for a reading; whisper's "6.14" or "hetero zugeo"
never has to match the page by luck. Shape: {"watches": {<root id>: [{t, w}]}}.

STORAGE. The MP3 is R2-only media (deploy doctrine rule 3; ~10 MB per study is
too much for git across 120 studies): master copy at
~/usmcmin-org-media-local/assets/media/studies/<slug>.mp3, served from
https://usmcmin.org/assets/media/studies/<slug>.mp3. The words file goes in git
at docs/assets/studies/<slug>-words.json; its presence is what tells the
renderer to include the player. Blog posts: the same with "blog" for "studies"
(the player markup is added to the post by hand; there is no blog renderer).
"""
import difflib
import hashlib
import html.parser
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
WORDS_DIR = os.path.join(DOCS, "assets", "studies")
MEDIA_REL = "assets/media/studies"
MASTER_DIR = os.path.expanduser(os.environ.get(
    "STUDY_AUDIO_MASTER", "~/usmcmin-org-media-local/" + MEDIA_REL))
SITE = "https://usmcmin.org"
R2_DEST = "r2:usmcmin-site/" + MEDIA_REL + "/"


def configure_blog():
    """--blog: same pipeline, blog paths. Study defaults above stay as they were."""
    global WORDS_DIR, MEDIA_REL, MASTER_DIR, R2_DEST
    WORDS_DIR = os.path.join(DOCS, "assets", "blog")
    MEDIA_REL = "assets/media/blog"
    MASTER_DIR = os.path.expanduser(os.environ.get(
        "BLOG_AUDIO_MASTER", "~/usmcmin-org-media-local/" + MEDIA_REL))
    R2_DEST = "r2:usmcmin-site/" + MEDIA_REL + "/"


WHISPER_MODEL = os.path.expanduser(os.environ.get(
    "WHISPER_MODEL", "~/.openclaw/whisper_models/ggml-small.en.bin"))
CHUNKED = os.path.expanduser(os.environ.get("WORDS_CHUNKED", "~/Scripts/pj-words-chunked.py"))
SAMPLE_RATE = 24000
GAP = 0.55            # between paragraphs
GAP_HEADING = 1.1     # before a heading
GAP_AFTER_HEADING = 0.5

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "source", "track", "wbr"}
SKIP_TAGS = {"script", "style", "button", "audio", "nav", "noscript", "svg", "template"}
BLOCK_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "div", "blockquote",
              "footer", "section", "article", "ul", "ol", "dd", "dt", "td", "th",
              "figcaption", "pre", "header", "main", "aside", "figure", "table"}
HEADINGS = {"h1", "h2", "h3", "h4"}


def watch_helpers():
    """The daily watch generator's text prep — one pronunciation rulebook."""
    spec = importlib.util.spec_from_file_location(
        "generate_watch_audio", os.path.join(ROOT, "bin", "generate-watch-audio.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── page parsing ─────────────────────────────────────────────────────────────
class Node:
    __slots__ = ("tag", "attrs", "children", "parent", "text")

    def __init__(self, tag, attrs=None, parent=None, text=None):
        self.tag, self.attrs, self.parent, self.text = tag, dict(attrs or {}), parent, text
        self.children = []

    def cls(self):
        return (self.attrs.get("class") or "").split()


class Tree(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root")
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(Node("#text", parent=self.cur, text=data))


def find(node, pred):
    if pred(node):
        return node
    for c in node.children:
        hit = find(c, pred)
        if hit:
            return hit
    return None


def skipped(node):
    return (node.tag in SKIP_TAGS or "data-no-follow" in node.attrs
            or "audio-speed" in node.cls() or "read-scroll-bar" in node.cls())


def text_tokens(node):
    """Every word span read-scroll.js would make inside node, in order."""
    out = []
    if node.tag == "#text":
        if node.text and node.text.strip():
            out.extend(node.text.split())
        return out
    if skipped(node):
        return out
    for c in node.children:
        out.extend(text_tokens(c))
    return out


def raw_text(node):
    if node.tag == "#text":
        return node.text or ""
    if skipped(node):
        return ""
    return "".join(raw_text(c) for c in node.children)


def attributed_quote(n):
    """The <blockquote data-say-before> holding n, if any."""
    while n is not None:
        if n.tag == "blockquote":
            return "data-say-before" in n.attrs
        n = n.parent
    return False


def extract_units(follow_root, blog=False):
    """Speech units in document order: {say, dom, voice, kind}."""
    units = []
    state = {"block": None}

    def voice_of(n):
        while n is not None:
            if "data-voice" in n.attrs:
                return n.attrs["data-voice"]
            n = n.parent
        return "narrator"

    def block_of(n):
        n = n.parent
        while n is not None and n is not follow_root.parent:
            if n.tag in BLOCK_TAGS:
                return n
            n = n.parent
        return follow_root

    def walk(n):
        if n.tag == "#text":
            if not (n.text and n.text.strip()):
                return
            b = block_of(n)
            if state["block"] is not b or not units or units[-1].get("closed"):
                units.append({"say": "", "dom": [], "voice": voice_of(n),
                              "kind": b.tag if b.tag in HEADINGS else "p"})
                if blog and attributed_quote(n):
                    units[-1]["quote"] = True
                state["block"] = b
            units[-1]["say"] += n.text
            units[-1]["dom"].extend(n.text.split())
            return
        if skipped(n):
            return
        if blog and n.tag == "figure":
            # One brief line per figure: the first sentence of the first image's
            # alt (dark/light twins share it). The full alt stays for screen readers.
            img = find(n, lambda x: x.tag == "img" and (x.attrs.get("alt") or "").strip())
            if img:
                alt = img.attrs["alt"].strip()
                brief = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", alt, maxsplit=1)[0]
                units.append({"say": "Graphic: " + brief, "dom": [],
                              "voice": "narrator", "kind": "cue", "closed": True})
            state["block"] = None
            return
        before = n.attrs.get("data-say-before")
        if before:
            units.append({"say": before, "dom": [], "voice": "narrator",
                          "kind": "cue", "closed": True})
            state["block"] = None
        if "data-say" in n.attrs:
            units.append({"say": n.attrs["data-say"], "dom": text_tokens(n),
                          "voice": voice_of(n), "kind": n.tag if n.tag in HEADINGS else "p",
                          "closed": True})
            state["block"] = None
            return
        if n.tag in BLOCK_TAGS:
            state["block"] = None  # a block boundary always starts a new unit
        for c in n.children:
            walk(c)
        if n.tag in BLOCK_TAGS:
            state["block"] = None

    walk(follow_root)
    for u in units:
        u["say"] = re.sub(r"\s+", " ", u["say"]).strip()
        if u.pop("quote", False):
            # The attribution was spoken before the quote; drop the "(source)" after it.
            u["say"] = re.sub(r"\s*\([^()]*\)\s*$", "", u["say"])
        u.pop("closed", None)
    return [u for u in units if re.search(r"[A-Za-z0-9]", u["say"])]


# ── spoken-text prep ─────────────────────────────────────────────────────────
NON_LATIN = re.compile(r"[Ͱ-Ͽἀ-῿֐-׿יִ-ﭏ]+")


def speakable(text):
    """Page text -> what the narrator says. Spoken only; the page is untouched."""
    t = NON_LATIN.sub("", text)
    t = re.sub(r"Strong[’']s\s+[GH]\d{1,5}\b", "", t)
    t = re.sub(r"\b[GH]\d{1,5}\b", "this word", t)
    t = re.sub(r"\bi\.e\.,?", "that is,", t)
    t = re.sub(r"\be\.g\.,?", "for example,", t)
    t = re.sub(r"\bcf\.", "compare", t)
    t = re.sub(r"\bch\.\s*(?=\d)", "chapter ", t)
    t = re.sub(r"\bvv?\.\s*(?=\d)", "verse ", t)
    t = t.replace("LORD", "Lord").replace("·", ",")
    t = re.sub(r"\bNT\b", "New Testament", t)
    t = re.sub(r"\bOT\b", "Old Testament", t)
    t = re.sub(r"\b([A-Za-z]{2,})/([A-Za-z]{2,})\b", r"\1 or \2", t)
    t = re.sub(r"https?://\S+", "", t)
    # Transliterations carry macrons and accents (koinōnia, anomía).
    t = "".join(ch for ch in unicodedata.normalize("NFKD", t) if not unicodedata.combining(ch))
    t = re.sub(r"\s+([,.;:])", r"\1", t)
    t = re.sub(r"(,\s*){2,}", ", ", t)
    return re.sub(r"\s+", " ", t).strip(" ,")


def blog_before(text):
    """Blog-only spoken tweaks, before speakable(). Every Scripture ref in a post
    is "(Book 1:2, KJV)"; the version tag twenty times over is noise in the ear."""
    t = re.sub(r",\s*KJV\)", ")", text)
    return re.sub(r"\bv\.(?=\s+[A-Z])", "versus", t)  # Roe v. Wade


def blog_after(tts):
    """After apply_lexicon: its prayer rule puts a period after every Amen; in
    running prose ("We say amen to the sentence") that is a false full stop."""
    return re.sub(r"\bAmen\.(?=\s+[a-z])", "amen", tts)


MARKUP = re.compile(r"\[([^\]]+)\]\(/[^)]*/\)")


def plain(spoken_with_markup):
    return MARKUP.sub(r"\1", spoken_with_markup)


def norm(s):
    """Same key as read-scroll.js norm()."""
    s = str(s or "").lower().replace("’", "").replace("'", "")
    return re.sub(r"[^a-z0-9]", "", s)


# ── audio ────────────────────────────────────────────────────────────────────
def ffprobe_secs(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nk=1:nw=1", path], capture_output=True, text=True)
    return float(out.stdout.strip())


def silence(path, secs):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                    f"anullsrc=r={SAMPLE_RATE}:cl=mono", "-t", f"{secs:.3f}",
                    "-c:a", "pcm_s16le", path], check=True)


def render_units(units, helpers, book_voice, tmp):
    from mlx_audio.tts.utils import load_model
    from mlx_audio.tts.generate import generate_audio
    model = load_model(helpers.MODEL_ID)
    narr = (helpers.NARRATOR, helpers.NARRATOR_LANG)
    parts, cursor = [], 0.0
    sil_cache = {}

    def gap(secs):
        nonlocal cursor
        key = round(secs, 2)
        if key not in sil_cache:
            sil_cache[key] = os.path.join(tmp, f"sil{key}.wav")
            silence(sil_cache[key], key)
        parts.append(sil_cache[key])
        cursor += ffprobe_secs(sil_cache[key])

    for i, u in enumerate(units):
        voice, lang = book_voice if u["voice"] == "book" and book_voice else narr
        if i:
            gap(GAP_HEADING if u["kind"] in HEADINGS else
                GAP_AFTER_HEADING if units[i - 1]["kind"] in HEADINGS else GAP)
        seg = os.path.join(tmp, f"u{i:03d}")
        os.makedirs(seg)
        generate_audio(text=u["tts"], model=model, voice=voice, lang_code=lang,
                       output_path=seg, file_prefix="p", join_audio=True,
                       audio_format="wav", verbose=False)
        wavs = sorted(f for f in os.listdir(seg) if f.endswith(".wav"))
        if not wavs:
            raise SystemExit(f"FAIL no audio for unit {i}: {u['say'][:60]}")
        # One sample rate / layout for the concat demuxer.
        w = os.path.join(tmp, f"u{i:03d}.wav")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(seg, wavs[0]),
                        "-ar", str(SAMPLE_RATE), "-ac", "1", "-c:a", "pcm_s16le", w], check=True)
        d = ffprobe_secs(w)
        u["start"], u["end"], u["voice_id"] = round(cursor, 3), round(cursor + d, 3), voice
        parts.append(w)
        cursor += d
        print(f"  unit {i + 1}/{len(units)} {voice} {d:5.1f}s  {u['say'][:56]}", flush=True)
    return parts


def encode(parts, mp3, tmp):
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        f.write("".join(f"file '{p}'\n" for p in parts))
    joined = os.path.join(tmp, "joined.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", lst, "-c:a", "pcm_s16le", joined], check=True)
    # Two-pass loudnorm to -16 LUFS like media-pipeline/normalize-audio.sh, but
    # without its silence trim: a trimmed head would shift every word time.
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", joined, "-af",
                          "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = json.loads(err[err.rindex("{"):err.rindex("}") + 1])
    af = ("loudnorm=I=-16:TP=-1.5:LRA=11:linear=true:"
          f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
          f"offset={m['target_offset']}")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", joined, "-af", af,
                    "-ar", str(SAMPLE_RATE), "-ac", "1", "-codec:a", "libmp3lame",
                    "-b:a", "64k", mp3], check=True)


# ── timings ──────────────────────────────────────────────────────────────────
def whisper_words(mp3, tmp):
    wav = os.path.join(tmp, "asr16k.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3, "-ar", "16000",
                    "-ac", "1", wav], check=True)
    out = os.path.join(tmp, "asr.json")
    subprocess.run(["python3", CHUNKED, wav, WHISPER_MODEL, out], check=True)
    words = []
    for s in json.load(open(out))["transcription"]:
        w = (s.get("text") or "").strip()
        if w:
            words.append({"t": round(s["offsets"]["from"] / 1000.0, 2), "w": w})
    return words


def interpolate(times, lo, hi):
    """Fill None gaps linearly between known neighbours (lo/hi bound the ends)."""
    n = len(times)
    known = [(i, t) for i, t in enumerate(times) if t is not None]
    anchors = [(-1, lo)] + known + [(n, hi)]
    out = list(times)
    for (i0, t0), (i1, t1) in zip(anchors, anchors[1:]):
        for k in range(i0 + 1, i1):
            out[k] = t0 + (t1 - t0) * (k - i0) / (i1 - i0)
    return out


def build_timings(units, asr):
    """whisper words -> narration script -> page words. Returns ({t,w} list, report)."""
    sp = []  # (unit index, key)
    for ui, u in enumerate(units):
        for tok in plain(u["tts"]).split():
            sp.append((ui, norm(tok)))
    a = [norm(w["w"]) for w in asr]
    b = [k for _, k in sp]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    sp_t = [None] * len(sp)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            ai, bi = blk.a + k, blk.b + k
            u = units[sp[bi][0]]
            t = asr[ai]["t"]
            if b[bi] and u["start"] - 1.5 <= t <= u["end"] + 1.0:
                sp_t[bi] = t
    out, report, pos = [], [], 0
    for ui, u in enumerate(units):
        toks = plain(u["tts"]).split()
        times = sp_t[pos:pos + len(toks)]
        keys = b[pos:pos + len(toks)]
        pos += len(toks)
        real = [k for k in keys if len(k) >= 3]
        heard = sum(1 for k, t in zip(keys, times) if len(k) >= 3 and t is not None)
        report.append((ui, heard, len(real)))
        if not u["dom"]:
            continue
        times = interpolate(times, u["start"], u["end"])
        dk = [norm(d) for d in u["dom"]]
        dm = difflib.SequenceMatcher(None, keys, dk, autojunk=False)
        dt = [None] * len(dk)
        for blk in dm.get_matching_blocks():
            for k in range(blk.size):
                if dk[blk.b + k]:
                    dt[blk.b + k] = times[blk.a + k]
        # Page words with no spoken twin ("10:20–21" said as "10:20 through 21")
        # take a time between matched neighbours; trailing ones stay untimed.
        idx = [i for i, t in enumerate(dt) if t is not None]
        if idx:
            first, last = idx[0], idx[-1]
            filled = interpolate(dt[first:last + 1], dt[first], dt[last])
            dt[first:last + 1] = filled
        prev = out[-1]["t"] if out else 0.0
        for d, t in zip(u["dom"], dt):
            if t is None or not norm(d):
                continue
            t = max(prev, round(t, 2))
            out.append({"t": t, "w": d})
            prev = t
    return out, report


# ── main ─────────────────────────────────────────────────────────────────────
def page_for(slug, override, blog=False):
    if override:
        return override
    if blog:
        p = os.path.join(DOCS, "blog", slug + ".html")
        if os.path.isfile(p):
            return p
        raise SystemExit(f"no blog post for {slug} (looked for {p})")
    for p in (os.path.join(DOCS, "verse", slug + ".html"),
              os.path.join(DOCS, "drafts", "verse", slug + ".html")):
        if os.path.isfile(p):
            return p
    raise SystemExit(f"no page for {slug} (looked in docs/verse and docs/drafts/verse)")


def book_voice_for(page_html):
    m = re.search(r'<meta name="verse-ref" content="([^"]+)"', page_html)
    if not m:
        return None
    ref = m.group(1)
    data = json.load(open(os.path.join(ROOT, "data", "book-voices.json")))
    for b in data.get("books", []):
        names = [b["name"]] + list(b.get("aliases") or [])
        if any(ref.startswith(n + " ") for n in sorted(names, key=len, reverse=True)):
            if (b.get("engine") or "kokoro") != "kokoro":
                return None  # Piper books: keep the narrator for the one verse
            return (b["voice"], b.get("lang", "a"))
    return None


def exclude_on_main():
    for remote in ("cowork-https", "origin"):
        if subprocess.run(["git", "-C", ROOT, "fetch", "-q", remote, "main"],
                          capture_output=True).returncode == 0:
            wf = subprocess.run(["git", "-C", ROOT, "show", "FETCH_HEAD:.github/workflows/deploy-r2.yml"],
                                capture_output=True, text=True).stdout
            return MEDIA_REL + "/**" in wf
    return False


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("-"):
        print(__doc__.split("\n\n")[1])
        sys.exit(2)
    slug = args[0].replace(".html", "")
    opt = lambda f: f in args
    blog = opt("--blog")
    if blog:
        configure_blog()
    if opt("--upload-only"):
        upload(slug)
        return
    page_override = args[args.index("--page") + 1] if "--page" in args else None
    page = page_for(slug, page_override, blog)
    src = open(page, encoding="utf-8").read()
    tree = Tree()
    tree.feed(src)
    root = find(tree.root, lambda n: "data-read-follow" in n.attrs)
    if root is None:
        raise SystemExit(f"{page}: no [data-read-follow] element — re-render the page first")
    key = root.attrs.get("id") or ("post" if blog else "study")
    helpers = watch_helpers()
    book_voice = None if blog else book_voice_for(src)
    units = extract_units(root, blog)
    for u in units:
        lang = book_voice[1] if (u["voice"] == "book" and book_voice) else helpers.NARRATOR_LANG
        if blog:
            u["tts"] = blog_after(helpers.apply_lexicon(speakable(blog_before(u["say"])), lang))
        else:
            u["tts"] = helpers.apply_lexicon(speakable(u["say"]), lang)
    n_words = sum(len(plain(u["tts"]).split()) for u in units)
    print(f"{slug}: {len(units)} units, {n_words} spoken words, narrator={helpers.NARRATOR}, "
          f"book voice={book_voice}, root=#{key}", flush=True)
    if opt("--dry-run"):
        for i, u in enumerate(units):
            print(f"[{i:03d} {u['kind']:>4} {u['voice']:>8}] {plain(u['tts'])}")
        return

    os.makedirs(MASTER_DIR, exist_ok=True)
    os.makedirs(WORDS_DIR, exist_ok=True)
    mp3 = os.path.join(MASTER_DIR, slug + ".mp3")
    units_path = os.path.join(MASTER_DIR, slug + ".units.json")
    t0 = time.time()
    with tempfile.TemporaryDirectory(prefix=f"study-audio-{slug}-") as tmp:
        if opt("--reuse-mp3"):
            old = json.load(open(units_path))
            if [u["say"] for u in old] != [u["say"] for u in units]:
                raise SystemExit("--reuse-mp3: page text changed since the bake; run a full bake")
            units = old
        else:
            parts = render_units(units, helpers, book_voice, tmp)
            t_tts = time.time() - t0
            encode(parts, mp3, tmp)
            json.dump(units, open(units_path, "w"), ensure_ascii=False, indent=1)
            print(f"TTS + encode {t_tts:.0f}s / {time.time() - t0:.0f}s", flush=True)
        t1 = time.time()
        asr = whisper_words(mp3, tmp)
        print(f"whisper {len(asr)} words in {time.time() - t1:.0f}s", flush=True)
    words, report = build_timings(units, asr)
    dur = ffprobe_secs(mp3)
    sha = hashlib.sha1(open(mp3, "rb").read()).hexdigest()[:10]
    # ASR check, the study's version of the watch prayer gate: a unit whose
    # words whisper mostly did not hear may be a TTS skip. Warn, with the text.
    weak = [(ui, h, n) for ui, h, n in report if n >= 8 and h / n < 0.5]
    heard = sum(h for _, h, _ in report)
    total = sum(n for _, _, n in report)
    for ui, h, n in weak:
        print(f"ASR WARN unit {ui}: heard {h}/{n} — {units[ui]['say'][:80]}")
    out = {
        "slug": slug,
        "source": "whisper-small.en (pj-words-chunked) aligned to page text",
        "audio": f"{SITE}/{MEDIA_REL}/{slug}.mp3?v={sha}",
        "duration": round(dur, 2),
        "voice": helpers.NARRATOR,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "watches": {key: words},
    }
    words_path = os.path.join(WORDS_DIR, slug + "-words.json")
    with open(words_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    dom_total = sum(1 for u in units for d in u["dom"] if len(norm(d)) >= 3)
    timed = sum(1 for w in words if len(norm(w["w"])) >= 3)
    print(f"DONE {slug}: {dur / 60:.1f} min, {os.path.getsize(mp3) // 1024} KB -> {mp3}")
    print(f"  words {timed}/{dom_total} page words timed; whisper heard {heard}/{total} "
          f"script words ({100 * heard / max(1, total):.0f}%); weak units {len(weak)}")
    print(f"  {words_path} ({os.path.getsize(words_path) // 1024} KB) audio={out['audio']}")
    print(f"  total {time.time() - t0:.0f}s")

    if opt("--upload"):
        upload(slug)


def upload(slug):
    """rclone COPY (never sync) the master to R2. The local master stays put:
    CI cannot restore R2-only media."""
    mp3 = os.path.join(MASTER_DIR, slug + ".mp3")
    if not os.path.isfile(mp3):
        raise SystemExit(f"no master at {mp3} — bake first")
    if not exclude_on_main():
        raise SystemExit("REFUSE upload: deploy-r2.yml on main has no "
                         f"'{MEDIA_REL}/**' exclude — the next deploy would delete it")
    subprocess.run(["rclone", "copy", mp3, R2_DEST, "--checksum", "--s3-no-check-bucket", "-v"],
                   check=True)
    print(f"UPLOADED {R2_DEST}{slug}.mp3 (master kept at {mp3})")


if __name__ == "__main__":
    main()
