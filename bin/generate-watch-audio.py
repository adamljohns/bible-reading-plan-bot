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
# Prefer TCC-safe path under ~/.openclaw (Documents/ is often denied to agent/LaunchAgent).
_F5_DEFAULT_WAV = os.path.expanduser("~/.openclaw/voice/f5tts-tests/ref-calm.wav")
_F5_LEGACY_WAV = os.path.expanduser("~/Documents/05-Voice/f5tts-tests/ref-calm.wav")
_F5_DEFAULT_TXT = os.path.expanduser("~/.openclaw/voice/f5tts-tests/ref-calm.txt")
_F5_LEGACY_TXT = os.path.expanduser("~/Documents/05-Voice/f5tts-tests/ref-calm.txt")
def _first_readable(*paths):
    for pth in paths:
        try:
            if pth and os.path.isfile(pth) and os.access(pth, os.R_OK):
                # probe open (TCC can exist+stat but deny read)
                with open(pth, "rb") as fh:
                    fh.read(16)
                return pth
        except OSError:
            continue
    return paths[0]

F5_REF = os.path.expanduser(os.environ.get("F5_REF_AUDIO") or "") or _first_readable(
    _F5_DEFAULT_WAV, _F5_LEGACY_WAV)
F5_REFTEXT_PATH = os.path.expanduser(os.environ.get("F5_REF_TEXT") or "") or _first_readable(
    _F5_DEFAULT_TXT, _F5_LEGACY_TXT)
F5_VENV_PY = os.path.expanduser(os.environ.get(
    "F5_VENV_PY", "~/.venvs/f5tts/bin/python"))
F5_REF_SEC = float(os.environ.get("F5_REF_SEC", "15.0"))
F5_CPS = float(os.environ.get("F5_CPS", "11.0"))  # MBP-0827: slower so tails/Amen are not clipped
F5_BUFFER = float(os.environ.get("F5_BUFFER", "1.4"))  # was 0.6; last-word cutoff
F5_STEPS = int(os.environ.get("F5_STEPS", "32"))
F5_CHUNK_MAX = int(os.environ.get("F5_CHUNK_MAX", "120"))  # PJG-0811: tighter chunks vs prayer dropout
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
    """Final Amen is the ordinary word Amen. (PJG-0823-AMEN3).

    SOUND target stays AH-men (item 19). Listen-script SPELLING is the human
    word Amen. attached to I pray. — same as the published page.
    Do not write AH-men / AH men / uh-MEN / a-MEN / IPA / dash / letter spelling.
    Never isolate Amen as its own chunk.
    """
    # Collapse phonetic cues back to the ordinary word.
    text = re.sub(
        r"\b(?:AH-men|AH men|Ah men|a-MEN|uh-MEN|uh MENN|uh MEN|a MEN)\b",
        "Amen",
        text,
        flags=re.I,
    )
    # Strip IPA markup on Amen — F5 reads the cue aloud.
    text = re.sub(r"\[Amen\]\(/[^/)]+/\)", "Amen", text, flags=re.I)
    # Strip ?/! after Amen anywhere; ensure terminal period.
    text = re.sub(r"\bAmen\b\s*[?!]+", "Amen.", text, flags=re.I)
    text = re.sub(r"\bAmen\b(?!\s*\.)", "Amen.", text, flags=re.I)
    return text


def apply_homograph_context(text: str) -> str:
    """Context-aware homograph disambiguation before synth (PJG-0802-AUD2).

    Kokoro honors [word](/ipa/) markup. Expand seed list as ear QA hits.
    Order matters: more specific patterns first.
    """
    # --- live: /lɪv/ dwell/reside vs /laɪv/ alive/broadcast ---
    # PJG-0809-PRAY1: Prov 9 "Forsake foolishness and live" = dwell/lɪv (not broadcast/laɪv)
    text = re.sub(
        r"\b([Aa]nd)\s+live\b(?=\s*[,;:.?!]|$)",
        lambda m: f"{m.group(1)} [live](/lɪv/)",
        text,
    )
    text = re.sub(
        r"\bForsake\s+foolishness\s+and\s+live\b",
        "Forsake foolishness and [live](/lɪv/)",
        text,
        flags=re.I,
    )
    # dwell sense
    text = re.sub(
        r"\b([Ll])ive\b(?=\s+(?:in|with|among|at|on|by|under|through|as|for|out|together|alone|here|there|forever|peaceably|securely))",
        lambda m: f"[{m.group(1)}ive](/lɪv/)",
        text,
    )
    text = re.sub(
        r"\b([Ll])ives\b(?=\s+(?:in|with|among|at|on|by|under|through|as|for|out|together|alone|here|there))",
        lambda m: f"[{m.group(1)}ives](/lɪvz/)",
        text,
    )
    text = re.sub(
        r"\b([Ll])iving\b(?=\s+(?:in|with|among|at|on|by|under|through|as|for|out|water|God|stone))",
        lambda m: f"[{m.group(1)}iving](/ˈlɪvɪŋ/)",
        text,
    )
    # alive / broadcast sense (default for "live" is often wrong in prayer/commentary)
    text = re.sub(
        r"\b([Ll])ive\b(?=\s+(?:broadcast|stream|feed|wire|ammo|fire|oak|recording|audience|show|event|performance|music|band))",
        lambda m: f"[{m.group(1)}ive](/laɪv/)",
        text,
    )
    text = re.sub(
        r"\b([Aa])live\b",
        lambda m: f"[{m.group(1)}live](/əˈlaɪv/)",
        text,
    )

    # --- read: past /rɛd/ vs present /riːd/ ---
    text = re.sub(
        r"\b([Rr])ead\b(?=\s+(?:the|this|aloud|Scripture|Word|chapter|verse|again|through|from))",
        lambda m: f"[{m.group(1)}ead](/riːd/)",
        text,
    )
    text = re.sub(
        r"\b([Hh]ave|[Hh]as|[Hh]ad|[Bb]een)\s+([Rr])ead\b",
        lambda m: f"{m.group(1)} [{m.group(2)}ead](/rɛd/)",
        text,
    )

    # --- lead: /liːd/ guide vs /lɛd/ metal (rare in corpus) ---
    text = re.sub(
        r"\b([Ll])ead\b(?=\s+(?:me|us|them|your|the|my|our|his|her|a|an|into|out|on|away|home|well))",
        lambda m: f"[{m.group(1)}ead](/liːd/)",
        text,
    )
    text = re.sub(
        r"\b([Ll])ead\s+(pipe|pipes|poisoning|weight|weights|bullet)\b",
        lambda m: f"[lead](/lɛd/) {m.group(2)}",
        text,
        flags=re.I,
    )

    # --- tear: /tɪr/ cry vs /tɛr/ rip ---
    text = re.sub(
        r"\b([Tt])ears\b(?=\s+(?:of|from|in\s+his|in\s+her|in\s+my|fell|stream|down))",
        lambda m: f"[{m.group(1)}ears](/tɪrz/)",
        text,
    )
    text = re.sub(
        r"\b([Tt])ear\b(?=\s+(?:down|apart|open|up|away|off|into))",
        lambda m: f"[{m.group(1)}ear](/tɛr/)",
        text,
    )

    # --- wind: /wɪnd/ air vs /waɪnd/ coil ---
    text = re.sub(
        r"\b([Ww])ind\b(?=\s+(?:of|from|blew|blows|blowing|howled|against|through|upon))",
        lambda m: f"[{m.group(1)}ind](/wɪnd/)",
        text,
    )
    text = re.sub(
        r"\b([Ww])ind\b(?=\s+(?:up|down|the\s+clock|the\s+path|around))",
        lambda m: f"[{m.group(1)}ind](/waɪnd/)",
        text,
    )

    # --- wound: /wuːnd/ injury vs /waʊnd/ past of wind ---
    text = re.sub(
        r"\b([Ww])ound\b(?=\s+(?:of|from|in|up|around|tight|tightly))",
        lambda m: f"[{m.group(1)}ound](/waʊnd/)" if "up" in m.group(0).lower() or "around" in (m.string[m.end():m.end()+10].lower()) else f"[{m.group(1)}ound](/wuːnd/)",
        text,
    )
    # simpler wound injury default
    text = re.sub(
        r"\b([Ww])ounds\b",
        lambda m: f"[{m.group(1)}ounds](/wuːndz/)",
        text,
    )
    text = re.sub(
        r"\b([Ww])ounded\b",
        lambda m: f"[{m.group(1)}ounded](/ˈwuːndɪd/)",
        text,
    )

    # --- close: /kloʊs/ near vs /kloʊz/ shut ---
    text = re.sub(
        r"\b([Cc])lose\b(?=\s+(?:to|by|at\s+hand|beside|with|friends|friend|quarters))",
        lambda m: f"[{m.group(1)}lose](/kloʊs/)",
        text,
    )
    text = re.sub(
        r"\b([Cc])lose\b(?=\s+(?:the|your|his|her|my|our|this|that|up|down|out|off))",
        lambda m: f"[{m.group(1)}lose](/kloʊz/)",
        text,
    )

    # --- present: /ˈprɛzənt/ gift/now vs /prɪˈzɛnt/ introduce ---
    text = re.sub(
        r"\b([Pp])resent\b(?=\s+(?:yourself|yourselves|him|her|them|the\s+gospel|your\s+bodies))",
        lambda m: f"[{m.group(1)}resent](/prɪˈzɛnt/)",
        text,
    )
    text = re.sub(
        r"\b([Pp])resent\b(?=\s+(?:age|moment|time|day|hour|world|help|distress))",
        lambda m: f"[{m.group(1)}resent](/ˈprɛzənt/)",
        text,
    )

    # --- record: /ˈrɛkərd/ noun vs /rɪˈkɔrd/ verb ---
    text = re.sub(
        r"\b([Rr])ecord\b(?=\s+(?:of|in|from|book|books))",
        lambda m: f"[{m.group(1)}ecord](/ˈrɛkərd/)",
        text,
    )
    text = re.sub(
        r"\b([Rr])ecord\b(?=\s+(?:this|these|it|them|my|his|her))",
        lambda m: f"[{m.group(1)}ecord](/rɪˈkɔrd/)",
        text,
    )

    # --- refuse: /rɪˈfjuz/ reject vs /ˈrɛfjus/ trash ---
    text = re.sub(
        r"\b([Rr])efuse\b(?=\s+(?:to|him|her|them|me|us|it|this|that))",
        lambda m: f"[{m.group(1)}efuse](/rɪˈfjuz/)",
        text,
    )

    # --- desert: /ˈdɛzərt/ arid vs /dɪˈzɜrt/ abandon ---
    text = re.sub(
        r"\b([Dd])esert\b(?=\s+(?:place|places|land|lands|of|wilderness))",
        lambda m: f"[{m.group(1)}esert](/ˈdɛzərt/)",
        text,
    )
    text = re.sub(
        r"\b([Dd])esert\b(?=\s+(?:me|us|them|him|her|the\s+post|your\s+post|the\s+watch))",
        lambda m: f"[{m.group(1)}esert](/dɪˈzɜrt/)",
        text,
    )

    # --- object: /ˈɑbdʒɛkt/ thing vs /əbˈdʒɛkt/ protest ---
    text = re.sub(
        r"\b([Oo])bject\b(?=\s+(?:to|when|if))",
        lambda m: f"[{m.group(1)}bject](/əbˈdʒɛkt/)",
        text,
    )
    text = re.sub(
        r"\b([Oo])bject\b(?=\s+(?:of|lesson|lessons))",
        lambda m: f"[{m.group(1)}bject](/ˈɑbdʒɛkt/)",
        text,
    )

    # --- content: /ˈkɑntɛnt/ substance vs /kənˈtɛnt/ satisfied ---
    text = re.sub(
        r"\b([Cc])ontent\b(?=\s+(?:with|to))",
        lambda m: f"[{m.group(1)}ontent](/kənˈtɛnt/)",
        text,
    )
    text = re.sub(
        r"\b([Cc])ontent\b(?=\s+(?:of|and|is|was|for))",
        lambda m: f"[{m.group(1)}ontent](/ˈkɑntɛnt/)",
        text,
    )

    # --- minute: /ˈmɪnɪt/ time vs /maɪˈnjuːt/ tiny ---
    text = re.sub(
        r"\b([Mm])inute\b(?=\s+(?:detail|details|particle|examination))",
        lambda m: f"[{m.group(1)}inute](/maɪˈnjuːt/)",
        text,
    )
    text = re.sub(
        r"\b([Mm])inutes\b",
        lambda m: f"[{m.group(1)}inutes](/ˈmɪnɪts/)",
        text,
    )

    # --- attribute: noun /ˈætrɪbjuːt/ vs verb /əˈtrɪbjuːt/ ---
    text = re.sub(
        r"\b([Aa])ttribute\b(?=\s+(?:to|it|them|this))",
        lambda m: f"[{m.group(1)}ttribute](/əˈtrɪbjuːt/)",
        text,
    )
    text = re.sub(
        r"\b([Aa])ttributes\b(?=\s+(?:of|and))",
        lambda m: f"[{m.group(1)}ttributes](/ˈætrɪbjuːts/)",
        text,
    )

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
    text = apply_homograph_context(text)
    for word, marked in LEXICON.items():
        text = re.sub(rf"\b{word}\b", marked, text)
    text = force_declarative_amen(text)
    return text


def f5_prep(text):
    """Plain-text prep for F5 clone. Markup stripped; Amen kept attached.

    PJG-0823-AMEN3: listen-script spelling is ordinary Amen. attached to
    I pray. SOUND target stays AH-men. Isolated Amen still banned.
    Published page/JSON stays human Amen.
    """
    text = text.replace("LORD", "Lord")
    text = re.sub(r"[—–]", ", ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = force_declarative_amen(text)
    # F5 cannot use misaki IPA — strip markup first
    text = re.sub(r"\[([^\]]+)\]\(/[^/)]+/\)", r"\1", text)
    # Collapse leftover phonetic Amen cues.
    text = re.sub(
        r"\b(?:AH-men|AH men|Ah men|a-MEN|uh-MEN|uh MENN|uh MEN|a MEN)\b",
        "Amen",
        text,
        flags=re.I,
    )
    # Keep Amen ATTACHED to "I pray." — never isolate. Ordinary word only.
    text = re.sub(
        r"\bAmen\b\s*[.?!]*\s*$",
        "Amen.",
        text,
        flags=re.I | re.M,
    )
    if re.search(r"I pray\.?\s+Amen\.", text, flags=re.I):
        return text.strip()
    text = re.sub(
        r"I pray\.?\s*(?:Amen|AH-men|uh-MEN)?\.?\s*$",
        "I pray. Amen.",
        text,
        flags=re.I | re.M,
    )
    return text.strip()


def f5_chunks(text, mx=None):
    """One sentence per F5 chunk. NEVER isolate terminal Amen as its own chunk.

    PJG-0823-AMEN3 / item 9: pack-joins were eating last words. Keep each
    complete sentence as its own chunk. Keep "I pray. Amen." as ONE chunk.
    Solo Amen sentences glue to previous with ". Amen." not a new chunk.
    """
    mx = mx or F5_CHUNK_MAX
    sents = re.split(r"(?<=[.!?])\s+", text) if text else []
    out, cur = [], ""
    amen_only = re.compile(
        r"(?:AH-men|AH men|Ah men|a-MEN|uh MENN|uh-MEN|uh MEN|a MEN|Amen)\s*[.?!]*$",
        flags=re.I,
    )
    for s in sents:
        if not s:
            continue
        if amen_only.fullmatch(s.strip()):
            amen = "Amen."
            if cur:
                base = cur.rstrip()
                if not base.endswith((".", "!", "?")):
                    base += "."
                cur = f"{base} {amen}".strip()
            elif out:
                base = out[-1].rstrip()
                if not base.endswith((".", "!", "?")):
                    base += "."
                out[-1] = f"{base} {amen}".strip()
            else:
                cur = amen
            continue
        # PJG-0825-PEACE1: start-clip eats mid-prayer openers when they begin
        # a new F5 take. Glue named skip-prone sentences onto the previous chunk.
        skip_open = re.match(
            r"^(Grant us|In the name|Through Jesus|Through Christ|For the sake|Hold Maria|When a man)\b",
            s.strip(),
            flags=re.I,
        )
        if skip_open and (cur or out):
            if cur:
                out.append(cur)
                cur = ""
            base = out[-1].rstrip()
            if not base.endswith((".", "!", "?")):
                base += "."
            out[-1] = f"{base} {s.strip()}".strip()
            continue
        # Close line starts with Through/In/For + I pray. Amen. — do not let
        # that sentence open a new F5 chunk (start-clip eats the title).
        close_line = re.search(r"I pray\.?\s+Amen\.?\s*$", s.strip(), flags=re.I)
        if close_line and (cur or out):
            if cur:
                out.append(cur)
                cur = ""
            base = out[-1].rstrip()
            if not base.endswith((".", "!", "?")):
                base += "."
            out[-1] = f"{base} {s.strip()}".strip()
            continue
        # One sentence per chunk so joins cannot clip a line tail.
        if cur:
            out.append(cur)
        cur = s.strip()
    if cur:
        out.append(cur)
    # PJG-0823-AMEN3: last-chunk start-clip was eating "Through Christ our Savior".
    # Glue the close sentence onto the previous prayer sentence so the title
    # is not the first words of a new F5 take.
    if len(out) >= 2 and re.search(r"I pray\.\s+Amen\.$", out[-1], flags=re.I):
        out[-2] = f"{out[-2].rstrip()} {out[-1]}".strip()
        out.pop()
    final = []
    for c in out:
        while len(c) > mx + 60:
            # do not split inside a trailing "Amen."
            cut = c.rfind(",", 0, mx)
            cut = cut if cut > 40 else mx
            # if remaining would be only Amen, don't cut
            rest = c[cut:].strip(" ,")
            if re.fullmatch(r"Amen\.?", rest, flags=re.I):
                break
            final.append(c[:cut].strip())
            c = rest
        if c:
            final.append(c)
    chunks = [c for c in final if c]
    # PJG-0826-AUD1: F5 start-clip eats ~10 words at the head of every take.
    # Duplicate the opener (chunk 0) and overlap the previous tail (later
    # chunks) so the published sentence still lands after the clip.
    if not chunks:
        return chunks
    overlapped = []
    for i, c in enumerate(chunks):
        words = c.split()
        if i == 0:
            n = min(12, max(4, len(words) // 2 or 4))
            overlapped.append(" ".join(words[:n]) + " " + c)
        else:
            prev = chunks[i - 1].split()
            n = min(10, len(prev))
            overlapped.append(" ".join(prev[-n:]) + " " + c)
    return overlapped




def adam_prayer_ready():
    if not USE_ADAM_PRAYER:
        return False
    ok = True
    for label, path in (("ref_wav", F5_REF), ("ref_txt", F5_REFTEXT_PATH), ("f5_py", F5_VENV_PY)):
        try:
            if not path or not os.path.isfile(path):
                ok = False
                continue
            with open(path, "rb") as fh:
                fh.read(8)
        except OSError as exc:
            print(f"WARN adam_prayer_ready: {label} unreadable ({exc})", flush=True)
            ok = False
    if not ok:
        return False
    # PJG-0803-PIN1: never bake Adam-clone prayer against a poisoned ref
    gate = os.path.join(ROOT, "scripts", "check_f5_prayer_ref.py")
    if os.path.isfile(gate):
        r = subprocess.run(
            [sys.executable, gate, "--wav", F5_REF, "--txt", F5_REFTEXT_PATH],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            msg = (r.stderr or r.stdout or "").strip()
            print(f"REFUSE adam-prayer: F5 ref ban-gate failed rc={r.returncode} {msg[:300]}", flush=True)
            return False
    return True


def join_lines(ls):
    t = "\n".join(l for l in ls if l != "")
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def split_prayer(post_lines):
    """Split post-scripture body into before / prayer / after.

    Prayer ends at the first Amen line (or Charge header). Anything after
    Amen (e.g. "This Day in American History") returns to narrator — never
    into Adam's clone voice.

    PJG-0825-PEACE1: the Prayer heading (emoji / "Prayer from the Stateroom" /
    leftover reflection title) is NOT spoken. Listen-script starts at Father,.
    """
    before, prayer, after = [], [], []
    st = "before"
    amen_end = re.compile(r"\b(?:Amen|AH-men|AH men|a-MEN|a MEN|uh-MEN|uh MEN|uh MENN)\.?\s*$", re.I)
    for line in post_lines:
        if st == "before" and PRAYER_HDR.match(line):
            st = "prayer"
            # Do not append the heading. Stray narration before Father, is FAIL.
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
                # PJG-0826-AUD1: one glued Kokoro take truncated the Father
                # prayer at ~500 chars (dropped the close). Sentence chunks.
                for sent in re.split(r"(?<=[.!?])\s+", join_lines(prayer)):
                    sent = sent.strip()
                    if sent:
                        segs.append(NARR_SEG + (apply_lexicon(sent),))
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


def render_voicestudio_text(text, out_wav):
    """Primary Adam clone via local VoiceStudio (MBP-0827). Returns True on success."""
    script = os.path.expanduser("~/Scripts/voicestudio-speak.py")
    if not os.path.isfile(script):
        return False
    try:
        r = subprocess.run(
            [sys.executable, script, "--text", text, "--out", out_wav],
            capture_output=True, text=True, timeout=240,
        )
        if r.returncode != 0 or not os.path.isfile(out_wav):
            print(f"  WARN VoiceStudio prayer failed: {(r.stderr or r.stdout or '')[-300:]}", flush=True)
            return False
        if out_wav.lower().endswith(".wav"):
            tmpw = out_wav + ".24k.wav"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out_wav,
                            "-ac", "1", "-ar", str(SAMPLE_RATE), tmpw], check=True)
            os.replace(tmpw, out_wav)
        print("  VoiceStudio prayer ok", flush=True)
        return True
    except Exception as e:
        print(f"  WARN VoiceStudio prayer exception ({e})", flush=True)
        return False


def render_f5_text(text, out_wav):
    """Fallback Adam clone via F5-TTS-MLX; write 24k mono wav."""
    # PJG-0803-PIN1 hard gate at bake time (ref + prayer body)
    gate = os.path.join(ROOT, "scripts", "check_f5_prayer_ref.py")
    if os.path.isfile(gate):
        import tempfile as _tf
        with _tf.NamedTemporaryFile("w", suffix="-prayer.txt", delete=False) as fh:
            fh.write(text or "")
            prayer_path = fh.name
        try:
            r = subprocess.run(
                [sys.executable, gate, "--wav", F5_REF, "--txt", F5_REFTEXT_PATH,
                 "--text", prayer_path],
                capture_output=True, text=True,
            )
        finally:
            try:
                os.unlink(prayer_path)
            except OSError:
                pass
        if r.returncode != 0:
            raise RuntimeError(
                f"F5 ban-gate refused prayer bake: {(r.stderr or r.stdout or '')[-500:]}")
    reftext = ""
    for pth in (F5_REFTEXT_PATH, _F5_DEFAULT_TXT):
        try:
            if pth and os.path.isfile(pth):
                reftext = open(pth).read().strip()
                if reftext:
                    break
        except OSError:
            continue
    if not reftext:
        raise RuntimeError("F5 ref text unreadable (TCC/Documents deny)")
    chunks = f5_chunks(text)
    if not chunks:
        raise RuntimeError("empty F5 prayer text")
    tmp = tempfile.mkdtemp(prefix="f5prayer-")
    try:
        parts = []
        for i, c in enumerate(chunks):
            raw = os.path.join(tmp, f"c{i:02d}.wav")
            # Floor duration so tiny tails cannot bake as ~0.04s silence/garbage
            dur = max(5, round(F5_REF_SEC + len(c) / F5_CPS + F5_BUFFER))
            if len(c) < 24:
                dur = max(dur, 7)
            if re.search(r"Ah men\.?\s*$", c, flags=re.I):
                dur = max(dur, 8)
            cmd = [F5_VENV_PY, "-m", "f5_tts_mlx.generate",
                   "--text", c, "--ref-audio", F5_REF, "--ref-text", reftext,
                   "--duration", str(dur), "--steps", str(F5_STEPS),
                   "--output", raw]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if not os.path.isfile(raw):
                raise RuntimeError(
                    f"F5 failed chunk {i}: {(r.stderr or r.stdout or '')[-400:]}")
            # PJG-0826-AUD1: silent/tiny F5 takes were concatenating as a skip.
            # Raise so render_watch falls back to narrator for this prayer.
            try:
                dur_s = float(subprocess.run(
                    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=nk=1:nw=1", raw],
                    capture_output=True, text=True, check=True).stdout.strip() or "0")
            except Exception:
                dur_s = 0.0
            if dur_s < 1.5:
                raise RuntimeError(f"F5 chunk {i} too short ({dur_s:.2f}s): {c[:60]!r}")
            rw = os.path.join(tmp, f"c{i:02d}_24.wav")
            # Pad each prayer sentence so concat/fade cannot eat the last word.
            padded = os.path.join(tmp, f"c{i:02d}_pad.wav")
            subprocess.run([
                "ffmpeg", "-y", "-loglevel", "error", "-i", raw,
                "-af", "apad=pad_dur=0.70",
                "-ar", str(SAMPLE_RATE), "-ac", "1", padded
            ], check=True)
            parts.append(padded)
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
                    # MBP-0827: VoiceStudio is primary Adam clone; F5 is fallback.
                    if not render_voicestudio_text(text, fw):
                        render_f5_text(text, fw)
                    wavs = [fw]
                except Exception as e:
                    print(f"  WARN Adam-clone prayer failed ({e}); "
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
        print("usage: generate-watch-audio.py <YYYY-MM-DD> [more dates] [--watch wisdom|first|second|third|peace]")
        sys.exit(2)
    # Optional single-watch filter: --watch <key>
    watch_filter = None
    if "--watch" in dates:
        i = dates.index("--watch")
        try:
            watch_filter = dates[i + 1]
        except IndexError:
            print("usage: --watch requires a key", file=sys.stderr)
            sys.exit(2)
        del dates[i:i + 2]
    # PJG-0803-LOOP1: fail closed before baking audio from looped Scripture
    import subprocess as _sp
    gate = os.path.join(ROOT, "scripts", "check_scripture_loops.py")
    if os.path.isfile(gate) and dates:
        g = _sp.run([sys.executable, gate, *dates], cwd=ROOT)
        if g.returncode != 0:
            print("REFUSE audio: scripture-loop gate failed", file=sys.stderr)
            sys.exit(g.returncode or 1)
    from mlx_audio.tts.utils import load_model
    from mlx_audio.tts.generate import generate_audio
    by_name = load_voice_map()
    prayer_mode = "adam-clone-F5" if adam_prayer_ready() else "narrator-fallback"
    print(f"Loading Kokoro {MODEL_ID} (once); narrator={NARRATOR}; "
          f"prayer={prayer_mode}...", flush=True)
    if prayer_mode.startswith("adam"):
        print(f"F5 ref wav={F5_REF}\nF5 ref txt={F5_REFTEXT_PATH}", flush=True)
    model = load_model(MODEL_ID)
    for date in dates:
        day = json.load(open(os.path.join(READINGS_JSON, f"{date}.json")))
        keys = ["wisdom", "first", "second", "third", "peace"]
        if watch_filter:
            if watch_filter not in keys and watch_filter not in FILE_KEY:
                # allow husband/father/citizen aliases
                rev = {v: k for k, v in FILE_KEY.items()}
                watch_filter = rev.get(watch_filter, watch_filter)
            keys = [watch_filter]
        for key in keys:
            w = day["watches"].get(key) or {}
            text = w.get("text")
            if not text:
                print(f"{date} {key}: NO TEXT — skipped")
                continue
            # Never speak HTML stamp/version comments (PJG-0810).
            text = re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()
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
