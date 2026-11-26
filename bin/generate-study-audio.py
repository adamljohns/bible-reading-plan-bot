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
    --narrator SPEC  who reads everything that has no data-voice of its own:
                  "src:<key>" from the voice map's "sources" (src:adam = the
                  Principal's own cloned voice). The page can say the same with
                  data-narrator="src:adam" on its follow root; the flag wins.
    --trial       a listening copy only: MP3 to <slug>.trial.mp3 beside the
                  master, word timings to /tmp. Nothing the site serves changes.

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
    `data-voice="book:<Book name>"` names the book (a post quotes many books),
    and `data-voice="src:<key>"` uses a named source voice from the map's
    "sources" (Calvin and the 1689 Confession in their own narration voice).
    A voice change inside a paragraph starts a new unit after a short pause,
    so an inline quotation is handed over mid-sentence (2026-11-26).
  * NARRATOR. A first-person post, or a prayer he offers, is read in the
    Principal's own cloned voice (Principal 2026-11-26): data-narrator="src:adam"
    on the follow root for a whole first-person post, data-voice="src:adam" on
    a closing prayer in any other post. Engine "voicestudio" = the local
    VoiceStudio clone (~/Scripts/voicestudio-speak.py holds its text rules),
    asked sentence by sentence at the speed in the voice map (1.15).
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
                if n.text and units and state["block"] is not None and not units[-1].get("closed"):
                    units[-1]["say"] += " "  # the space between two adjacent quotations
                return
            b = block_of(n)
            v = voice_of(n)
            fresh = state["block"] is not b or not units or units[-1].get("closed")
            if fresh or units[-1]["voice"] != v:
                units.append({"say": "", "dom": [], "voice": v,
                              "kind": b.tag if b.tag in HEADINGS else "p"})
                if not fresh:
                    units[-1]["cont"] = True  # same paragraph, another voice
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
    t = expand_negatives(NON_LATIN.sub("", text))
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


NEG_IRREGULAR = {"won": "will not", "can": "cannot", "shan": "shall not"}
NEG_RE = re.compile(r"\b(won|can|shan|do|does|did|is|are|was|were|has|have|had|would|could|"
                    r"should|must|need)n[’']t\b", re.I)


def expand_negatives(text):
    """Say "would not" for "wouldn't". Kokoro can swallow the n't, and the
    sentence then says the opposite ("the line he would cross", Principal
    2026-11-26). Spoken only; the page keeps its contraction."""
    def fix(m):
        stem = m.group(1)
        out = NEG_IRREGULAR.get(stem.lower(), stem.lower() + " not")
        return out[0].upper() + out[1:] if stem[0].isupper() else out
    return NEG_RE.sub(fix, text)


# Words the Kokoro dictionary does not hold (misaki falls back to a guess) or
# under-stresses. misaki inline phonemes, American / British vowel sets. Checked
# against misaki's G2P 2026-11-26: every word here came back unknown, except
# "ye", which is known but unstressed and was being dropped ("Be ye not").
PRONOUNCE = {
    "denieth":     ("dɪnˈIəθ", "dɪnˈIəθ"),
    "ye":          ("jˈi", "jˈiː"),
    "Ye":          ("jˈi", "jˈiː"),
    "shouldest":   ("ʃˈʊdɪst", "ʃˈʊdɪst"),
    "shoelatchet": ("ʃˈulˌæʧɪt", "ʃˈuːlˌaʧɪt"),
    "Abram":       ("ˈAbɹəm", "ˈAbɹəm"),
    "heterozygeo": ("hˌɛtəɹOzˈuɡAO", "hˌɛtəɹQzˈuːɡAQ"),
    "Schaeffer":   ("ʃˈAfəɹ", "ʃˈAfə"),
    "Cyprian":     ("sˈɪpɹiən", "sˈɪpɹiən"),
    "Charis":      ("kˈɛɹɪs", "kˈaɹɪs"),
    "Wommack":     ("wˈɑmək", "wˈɒmək"),
    "Webbon":      ("wˈɛbən", "wˈɛbən"),
    "Fuentes":     ("fwˈɛntɛs", "fwˈɛntɛs"),
}
RESPELL = {"stumblingblock": "stumbling block"}


def pronounce(tts, lang, engine):
    """After apply_lexicon. Piper takes plain text, so it gets no phoneme markup."""
    for w, r in RESPELL.items():
        tts = re.sub(rf"\b{w}\b", r, tts)
    if engine == "voicestudio":
        return clone_text(plain(tts))
    if engine != "kokoro":
        return plain(tts)
    # "under his lead": the bake of 2026-11-26 said it to rhyme with "made" (heard
    # as "lade" by two whisper models). The noun after a possessive is "leed".
    tts = re.sub(r"\b(his|their|her|my|our|your|God[’']s|Christ[’']s) lead\b(?!\]\()",
                 lambda m: f"{m.group(1)} [lead](/lˈid/)", tts)  # the long-vowel form lˈiːd still came out "lade" on bm_george
    for w, (us, uk) in PRONOUNCE.items():
        tts = re.sub(rf"(?<![\[\w]){w}\b(?!\]\()", f"[{w}](/{uk if lang == 'b' else us}/)", tts)
    return tts


def clone_text(t):
    """What the cloned voice is asked to say. It reads "4:6" and "NKJV" unevenly
    (trial bake 2026-11-26: "James 4, Voy J V"), so both are spelled out, and the
    brackets round a citation go."""
    t = re.sub(r"\b(\d+):(\d+) through (\d+)\b", r"\1, verses \2 through \3", t)
    t = re.sub(r"\b(\d+):(\d+)\b", r"\1, verse \2", t)
    t = re.sub(r"\bNKJV\b", "New King James", t)
    t = re.sub(r"\bKJV\b", "King James", t)
    return re.sub(r"\s+", " ", t.replace("(", "").replace(")", "")).strip()


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


UNIT_MEAN_DB = -21.0  # every unit is levelled to this mean before the join
GAP_INLINE = 0.3      # a voice change inside a paragraph
TAIL = 0.8            # silence after the last word, so no player clips it


def source_voice(sv):
    return (sv.get("engine") or "kokoro", sv["voice"], sv.get("lang", "a"),
            1.0 / float(sv["length_scale"]) if sv.get("length_scale") else float(sv.get("speed") or 1.0))


def voice_resolver(helpers, book_voice, narrator=None):
    """voice spec on a unit -> (engine, voice, lang, speed)."""
    narr = ("kokoro", helpers.NARRATOR, helpers.NARRATOR_LANG, 1.0)
    data = json.load(open(os.path.join(ROOT, "data", "book-voices.json")))
    if narrator:
        sv = (data.get("sources") or {}).get(narrator[4:].strip()) if narrator.startswith("src:") else None
        if not isinstance(sv, dict):
            raise SystemExit(f"--narrator {narrator}: no such source in data/book-voices.json")
        narr = source_voice(sv)
        if narr[0] == "voicestudio" and not voicestudio_up():
            raise SystemExit("narrator is the VoiceStudio clone and VoiceStudio is not answering; "
                             "not baking it in another voice")
    by_name = helpers.load_voice_map()
    cache = {}

    def piper_ok(voice):
        return os.path.isfile(os.path.join(os.path.expanduser("~"), ".piper-voices", voice + ".onnx"))

    def resolve(spec):
        if spec in cache:
            return cache[spec]
        r = narr
        if spec == "book" and book_voice:
            r = ("kokoro", book_voice[0], book_voice[1], 1.0)
        elif spec.startswith("book:"):
            b = by_name.get(spec[5:].strip().lower())
            if b is None:
                print(f"WARN voice: no book '{spec[5:]}' in the voice map; narrator reads it", flush=True)
            else:
                eng = b.get("engine") or "kokoro"
                r = (eng, b["voice"], b.get("lang", "a"), float(b.get("speed") or 1.0))
                if eng == "kokoro" and b["voice"] == narr[1]:
                    r = ("kokoro",) + tuple(helpers.ALT_SCRIPTURE) + (1.0,)  # keep the handoff audible
        elif spec.startswith("src:"):
            sv = (data.get("sources") or {}).get(spec[4:].strip())
            if not isinstance(sv, dict):
                print(f"WARN voice: no source '{spec[4:]}' in the voice map; narrator reads it", flush=True)
            else:
                r = source_voice(sv)
                if r[0] == "voicestudio" and not voicestudio_up():
                    print(f"WARN voice: VoiceStudio is not answering; narrator reads {spec}", flush=True)
                    r = narr
        if r[0] == "piper" and not piper_ok(r[1]):
            print(f"WARN voice: Piper model {r[1]} missing; narrator reads {spec}", flush=True)
            r = narr
        cache[spec] = r
        return r
    return resolve


# ── the Principal's cloned voice (VoiceStudio) ───────────────────────────────
VS_SPEAK = os.path.expanduser("~/Scripts/voicestudio-speak.py")
VS_CHUNK_MAX = 240     # characters; the clone drifts on long takes
VS_GAP_SENTENCE = 0.32
VS_GAP_CLAUSE = 0.14
_vs = {}


def vs_module():
    if "m" not in _vs:
        spec = importlib.util.spec_from_file_location("voicestudio_speak", VS_SPEAK)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        _vs["m"] = m
    return _vs["m"]


def voicestudio_up():
    try:
        vs_module().ensure_up()
        return True
    except (SystemExit, Exception):
        return False


def vs_chunks(text):
    """[(chunk, gap after it)] — one sentence a take; a sentence over
    VS_CHUNK_MAX is cut at the comma or semicolon nearest its middle."""
    def cut(sent):
        if len(sent) <= VS_CHUNK_MAX:
            return [sent]
        marks = [m.end() for m in re.finditer(r"[,;:](?=\s)", sent)]
        marks = [k for k in marks if 40 <= k <= len(sent) - 40]
        if not marks:
            return [sent]
        k = min(marks, key=lambda x: abs(x - len(sent) / 2))
        return cut(sent[:k].strip()) + cut(sent[k:].strip())
    out = []
    raw = [x.strip() for x in re.split(r"(?<=[.!?…])[”\"’')\]]*\s+(?=[“\"‘(A-Z])", text) if x.strip()]
    sents = []
    for x in raw:  # "C. S. Lewis", "Mr. Enlightenment": not sentence ends
        if sents and re.search(r"(?:\b[A-Z]|\b(?:Mr|Mrs|Ms|Dr|St|Rev|Sr|Jr|vs|v))\.$", sents[-1]):
            sents[-1] += " " + x
        else:
            sents.append(x)
    for sent in sents:
        parts = cut(sent)
        for j, c in enumerate(parts):
            out.append((c, VS_GAP_SENTENCE if j == len(parts) - 1 else VS_GAP_CLAUSE))
    return out


def vs_render(text, voice, speed, seg, tmp):
    """Clone one unit into seg/p.wav. Same request as voicestudio-speak.speak(),
    with the speed from the voice map instead of the locked config's 1.0."""
    m = vs_module()
    cfg = m.load_cfg()
    if voice != cfg.get("profile_id"):
        raise SystemExit(f"voice map asks for clone profile {voice}; VoiceStudio is locked to {cfg.get('profile_id')}")
    files = []
    for k, (chunk, gap_after) in enumerate(vs_chunks(text)):
        payload = {"model": cfg.get("engine", "omnivoice"), "input": m.prep_text(chunk)[:4096],
                   "voice": voice, "response_format": "wav", "speed": float(speed or 1.0),
                   "language": cfg.get("language") or "en", "instruct": cfg.get("instruct")}
        if cfg.get("seed") is not None:
            payload["seed"] = int(cfg["seed"])
        status, headers, raw = m.api("POST", "/v1/audio/speech", data=payload, raw=True, timeout=240)
        if status != 200 or raw[:1] in (b"{", b"["):
            raise SystemExit(f"VoiceStudio synth failed: {raw[:300]!r}")
        f = os.path.join(seg, f"c{k:02d}.raw.wav")
        open(f, "wb").write(raw)
        g = os.path.join(seg, f"c{k:02d}.wav")
        # trim the take's own leading/trailing silence so the gaps are ours
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f, "-af",
                        "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,"
                        "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse",
                        "-ar", str(SAMPLE_RATE), "-ac", "1", "-c:a", "pcm_s16le", g], check=True)
        files.append(g)
        s = os.path.join(seg, f"c{k:02d}.gap.wav")
        silence(s, gap_after)
        files.append(s)
    files = files[:-1]  # the unit gap follows; no trailing pause of our own
    lst = os.path.join(seg, "list.txt")
    with open(lst, "w") as fh:
        fh.write("".join(f"file '{x}'\n" for x in files))
    out = os.path.join(tmp, os.path.basename(seg) + ".vs.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c:a", "pcm_s16le", out], check=True)
    for x in os.listdir(seg):
        os.remove(os.path.join(seg, x))
    shutil.move(out, os.path.join(seg, "p.wav"))


def render_units(units, helpers, book_voice, tmp):
    from mlx_audio.tts.utils import load_model
    from mlx_audio.tts.generate import generate_audio
    model = load_model(helpers.MODEL_ID)
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
        engine, voice, lang, speed = u["engine"], u["voice_id"], u["lang"], u["speed"]
        if i:
            gap(GAP_INLINE if u.get("cont") else
                GAP_HEADING if u["kind"] in HEADINGS else
                GAP_AFTER_HEADING if units[i - 1]["kind"] in HEADINGS else GAP)
        seg = os.path.join(tmp, f"u{i:03d}")
        os.makedirs(seg)
        if engine == "piper":
            # Same call as the watch generator's Piper books and the Institutes batch.
            subprocess.run(
                [os.path.join(os.path.expanduser("~"), ".piper-venv", "bin", "python"),
                 "-m", "piper", "-m",
                 os.path.join(os.path.expanduser("~"), ".piper-voices", voice + ".onnx"),
                 "--length-scale", str(round(1.0 / (speed or 1.0), 3)),
                 "--sentence-silence", "0.35", "-f", os.path.join(seg, "p.wav")],
                input=u["tts"].encode(), check=True, capture_output=True)
        elif engine == "voicestudio":
            vs_render(u["tts"], voice, speed, seg, tmp)
        else:
            generate_audio(text=u["tts"], model=model, voice=voice, lang_code=lang,
                           output_path=seg, file_prefix="p", join_audio=True,
                           audio_format="wav", verbose=False)
        wavs = sorted(f for f in os.listdir(seg) if f.endswith(".wav"))
        if not wavs:
            raise SystemExit(f"FAIL no audio for unit {i}: {u['say'][:60]}")
        # One sample rate / layout for the concat demuxer.
        w = os.path.join(tmp, f"u{i:03d}.wav")
        # Level each unit: the engines differ by up to 10 dB (clone -16, Kokoro
        # -26 mean on 2026-11-26) and one loudnorm over the file keeps the jump.
        vd = subprocess.run(["ffmpeg", "-hide_banner", "-i", os.path.join(seg, wavs[0]), "-af",
                             "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
        mean = re.search(r"mean_volume: (-?[\d.]+)", vd)
        peak = re.search(r"max_volume: (-?[\d.]+)", vd)
        gain = 0.0
        if mean and peak:
            gain = max(-12.0, min(12.0, UNIT_MEAN_DB - float(mean.group(1)), -1.0 - float(peak.group(1))))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(seg, wavs[0]),
                        "-af", f"volume={gain:.2f}dB",
                        "-ar", str(SAMPLE_RATE), "-ac", "1", "-c:a", "pcm_s16le", w], check=True)
        d = ffprobe_secs(w)
        u["start"], u["end"] = round(cursor, 3), round(cursor + d, 3)
        parts.append(w)
        cursor += d
        print(f"  unit {i + 1}/{len(units)} {voice} {d:5.1f}s  {u['say'][:56]}", flush=True)
    gap(TAIL)
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


def asr_diff(units, asr, limit=60):
    """Listen-back: print every place whisper heard something other than the
    script (numbers and homophones show up too; read the list, it is short).
    This is how the dropped "n't" was found on 2026-11-26."""
    script = [(t, units_i) for units_i, u in enumerate(units) for t in plain(u["tts"]).split() if norm(t)]
    a = [norm(t) for t, _ in script]
    b = [norm(w["w"]) for w in asr]
    n = 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        said = " ".join(t for t, _ in script[i1:i2])
        heard = " ".join(w["w"] for w in asr[j1:j2])
        if re.fullmatch(r"[\W\d]*", said) or re.sub(r"\D", "", said) and re.sub(r"\D", "", said) == re.sub(r"\D", "", heard):
            continue  # verse numbers
        t = asr[min(j1, len(asr) - 1)]["t"] if asr else 0
        n += 1
        if n <= limit:
            print(f"ASR DIFF {int(t // 60):02d}:{int(t % 60):02d} script=[{said}] heard=[{heard}]", flush=True)
    print(f"ASR DIFF total {n}", flush=True)


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
    narrator = (args[args.index("--narrator") + 1] if "--narrator" in args
                else root.attrs.get("data-narrator"))
    resolve = voice_resolver(helpers, book_voice, narrator)
    narr_voice = resolve("")[1]
    for u in units:
        u["engine"], u["voice_id"], u["lang"], u["speed"] = resolve(u["voice"])
        lang = u["lang"]
        if blog:
            tts = blog_after(helpers.apply_lexicon(speakable(blog_before(u["say"])), lang))
        else:
            tts = helpers.apply_lexicon(speakable(u["say"]), lang)
        tts = re.sub(r"(?<=[a-z]),(?=[A-Z])", ", ", tts)  # "Peace,<br>Adam"
        u["tts"] = pronounce(tts, lang, u["engine"])
    n_words = sum(len(plain(u["tts"]).split()) for u in units)
    print(f"{slug}: {len(units)} units, {n_words} spoken words, narrator={narr_voice}, "
          f"book voice={book_voice}, root=#{key}", flush=True)
    if opt("--dry-run"):
        for i, u in enumerate(units):
            print(f"[{i:03d} {u['kind']:>4} {u['voice_id']:>16}{'+' if u.get('cont') else ' '}] {plain(u['tts'])}")
        return

    os.makedirs(MASTER_DIR, exist_ok=True)
    os.makedirs(WORDS_DIR, exist_ok=True)
    trial = opt("--trial")
    stem = slug + (".trial" if trial else "")
    mp3 = os.path.join(MASTER_DIR, stem + ".mp3")
    units_path = os.path.join(MASTER_DIR, stem + ".units.json")
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
    asr_diff(units, asr)
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
        "voice": narr_voice,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "watches": {key: words},
    }
    words_path = (os.path.join("/tmp", slug + "-trial-words.json") if trial
                  else os.path.join(WORDS_DIR, slug + "-words.json"))
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
