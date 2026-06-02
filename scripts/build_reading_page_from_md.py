#!/usr/bin/env python3
"""
Render data/readings/<date>.md  ->  docs/readings/<date>.html
(static, noindex, dark+gold theme matching chronological.html)

This is the MD-input renderer. It is INDEPENDENT of the older
build_reading_page.py (which consumed a structured JSON shape and
rendered the 2026-03-01 prototype). The .md format is what Adam writes
and what the PDF-converter produces, so this is the path going forward.

USAGE
  python3 scripts/build_reading_page_from_md.py 2026-01-01
  python3 scripts/build_reading_page_from_md.py --all
  python3 scripts/build_reading_page_from_md.py --date-range 2026-01-01 2026-02-28

PARSER ACCEPTS THREE WATCH-HEADER VARIANTS
  Format A (canonical, 2026-05-23.md):    "🌅 0600 Morning Wisdom"
  Format B (Jan 1 first conversion):      "Thursday, January 1" then "🌅 0600 Morning Wisdom"
  Format C (PDF auto-convert, Jan/Feb):   "📅 Sunday, February 15, 2026 — 0600"
                                          then "🌅 Morning Wisdom — [intro]"

OUTPUT
  Six tabs: All / Wisdom / Husband / Father / Citizen / Peace
  Sticky tab bar, URL hash persists, one watch visible at a time
  Audio slot per watch (graceful fallback when mp3 absent)
  Personalization placeholders preserved ({{name}}, {{wife}}, {{children}})
"""
import re
import sys
import argparse
from pathlib import Path
from html import escape
from datetime import datetime

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "readings"
OUT_DIR = REPO / "docs" / "readings"

# Watch metadata, in time order
WATCHES = [
    {"key": "wisdom",  "time": "0600", "title": "Morning Wisdom",                 "emoji": "🌅", "prayer_default": "Prayer",                  "command_default": "Helm Command"},
    {"key": "husband", "time": "0700", "title": "First Watch — The Husband's Post",  "emoji": "🕖", "prayer_default": "Prayer from the Stateroom", "command_default": "Helm Command"},
    {"key": "father",  "time": "1100", "title": "Second Watch — The Father's Charge", "emoji": "🕚", "prayer_default": "Prayer from the Wardroom",  "command_default": "Helm Command"},
    {"key": "citizen", "time": "1500", "title": "Third Watch — The Citizen's Stand",  "emoji": "🕒", "prayer_default": "Prayer from the Bridge",    "command_default": "Rudder Steer"},
    {"key": "peace",   "time": "2100", "title": "Evening Peace",                    "emoji": "🌙", "prayer_default": "Prayer from the Wardroom",  "command_default": "Rudder Steer"},
]
WATCH_BY_TIME = {w["time"]: w for w in WATCHES}
WATCH_BY_KEY  = {w["key"]:  w for w in WATCHES}

# Map a header-line keyword to a watch key (lowercased compare)
TITLE_KEYWORDS = {
    "morning wisdom":     "wisdom",
    "husband's post":     "husband",
    "first watch":        "husband",
    "father's charge":    "father",
    "second watch":       "father",
    "citizen's stand":    "citizen",
    "third watch":        "citizen",
    "evening peace":      "peace",
}

# Robust watch-header detection (2026-06-01) — shared logic with
# build_reading_index.py. Keys on the watch TIME CODE first (06/07/11/15/21xx),
# with a title-phrase fallback on emoji-led lines. Handles every legacy
# PDF-converted header variant (📅/⏰ two-line, 🕊/🕛/🛡 emoji, bare date-time).
_TIME_KEY_HTML = {"06": "wisdom", "07": "husband", "11": "father", "15": "citizen", "21": "peace"}
_TIME_RE = re.compile(r"(?<!\d)(06|07|11|15|21)[0-5]\d(?!\d)")
_DATETIME_LINE_RE = re.compile(r"^[A-Z][a-z]+day,?\s+\w+\s+\d+.*[—–-]\s*(?:06|07|11|15|21)[0-5]\d")


def _robust_boundary_key(line):
    """Return the watch key if this line is a watch header, else None."""
    s = line.strip()
    if not s:
        return None
    has_emoji = bool(re.match(r"^[^\w\s#>*_\-—–=.\"'(\[]", s))
    is_dt = bool(_DATETIME_LINE_RE.match(s))
    sl = s.lower()
    title_key = None
    for phrase, key in TITLE_KEYWORDS.items():
        if phrase in sl:
            title_key = key
            break
    mt = _TIME_RE.search(s)
    if mt and (has_emoji or title_key or is_dt):
        return _TIME_KEY_HTML.get(mt.group(1)) or title_key
    if has_emoji and title_key:
        return title_key
    return None

# Section markers — keyword-driven (any leading emoji/whitespace/markdown accepted).
# Emoji handling in Python regex is fragile because most are multi-codepoint
# sequences (ZWJ joined, variation selectors, skin tones). So we lead with a
# permissive prefix `^\s*\S*\s*` that swallows any leading emoji glyph, then
# match the distinctive English keyword. This is more robust than enumerating
# every emoji variant Adam/ChatGPT/the PDF converter might pick.
P = r"^\s*(?:\S+\s+)?(?:\*\*\s*)?"   # optional leading emoji token + optional **

# `P` matches an optional leading emoji/punct token + optional whitespace + optional **.
# Critical: single token only (no nested quantifiers) to prevent catastrophic backtracking.
# A "token" here = one run of non-alpha non-whitespace characters (one emoji or ⸻ block).
P = r"^\s*(?:[^\w\s\n]+\s+)?(?:\*\*\s*)?"

SECTION_PATTERNS = [
    # key,             regex
    ("scripture",      rf"{P}Scripture\s*[—\-–:]"),                              # "📖 Scripture — John 1:1-18"
    ("scripture_alt",  r"^\s*📖\s*(?:\*\*)?\s*[A-Z0-9]"),                         # "📖 Proverbs 25:15-28"  (no 'Scripture')
    ("context",        rf"{P}(?:Context Summary|Briefing Summary|Briefing|Field Notes|Situation Report)\b"),
    ("real_man",       rf"{P}Reflection for a REAL MAN\b"),
    ("happy",          rf"{P}Reflection for Your Wife\b"),
    ("fulfilled",      rf"{P}Reflection for Your Children\b"),
    ("resolute",       rf"{P}Reflection for a R\.?E\.?S\.?O\.?L\.?U\.?T\.?E\.?\s*Citizen\b"),
    ("history",        rf"{P}This Day in American History\b"),
    ("evening_ref",    rf"{P}Reflection for a Man\b"),
    ("application",    rf"{P}Personal\s+Application\b"),
    ("prayer",         rf"{P}Prayer(?:\s+from\s+the\s+\w+)?\s*$"),                 # heading line, not prose
    ("prayer_alt",     r"^\s*🙏\s*(?:\*\*)?\s*Prayer"),                            # belt-and-suspenders
    ("helm",           r"^\s*⚓\s*(?:\*\*)?\s*(?:Helm Command|Rudder Steer|Set Sail|Course Correction|Steady As She Goes|Night Orders)\b"),
]
SECTION_REGEX = [(key, re.compile(rx, re.IGNORECASE)) for key, rx in SECTION_PATTERNS]

# Expected order of watch keys for inference fallback
WATCH_ORDER = ["wisdom", "husband", "father", "citizen", "peace"]


# ────────────────────────────────────────────────────────────────────────
# PARSING
# ────────────────────────────────────────────────────────────────────────

def split_into_watches(text):
    """Yield (watch_key, intro_line, body_lines) for each detected watch in time order.

    A watch boundary is any of:
      - line matching Format C:  📅 ... — 0600|0700|1100|1500|2100
      - line matching Format A:  emoji + time + watch title  (e.g. "🌅 0600 Morning Wisdom")
      - line matching Format B:  emoji + time on its own (e.g. "🌅 0600 Morning Wisdom" after a date line)
    """
    lines = text.splitlines()

    # Pass 1 — find watch-header boundaries via the robust classifier (handles
    # modern + every legacy format). Only the FIRST header of each key counts.
    boundaries = []  # list of (line_idx, watch_key, title_emoji_line_idx)
    seen_keys = set()
    for i, line in enumerate(lines):
        key = _robust_boundary_key(line)
        if key and key not in seen_keys:
            boundaries.append((i, key, i))
            seen_keys.add(key)

    if not boundaries:
        return []

    # Pass 1.5 — INFER MISSING WATCH BOUNDARIES
    # If a slice between two consecutive boundaries contains MORE THAN ONE
    # '📖 Scripture' marker, that means a watch boundary line was dropped during
    # PDF conversion. Split at each additional scripture and assign the missing
    # slot from WATCH_ORDER between the bracketing keys.
    scripture_re = re.compile(r"^\s*📖\s*(?:Scripture|\*\*)", re.IGNORECASE)
    inferred = []
    for idx, (start, key, _) in enumerate(boundaries):
        end = boundaries[idx + 1][0] if idx + 1 < len(boundaries) else len(lines)
        # Find all scripture markers in this slice
        scrip_idxs = [i for i in range(start + 1, end) if scripture_re.match(lines[i])]
        inferred.append((start, key))
        if len(scrip_idxs) <= 1:
            continue
        # Determine the missing watch keys between THIS one and the NEXT boundary
        next_key = boundaries[idx + 1][1] if idx + 1 < len(boundaries) else None
        try:
            cur_pos = WATCH_ORDER.index(key)
        except ValueError:
            continue
        next_pos = WATCH_ORDER.index(next_key) if next_key in WATCH_ORDER else len(WATCH_ORDER)
        gap_keys = WATCH_ORDER[cur_pos + 1:next_pos]
        # Pair extra scriptures (those after the first) with missing keys
        for j, scrip_i in enumerate(scrip_idxs[1:]):
            if j >= len(gap_keys):
                break
            inferred.append((scrip_i, gap_keys[j]))
    inferred.sort(key=lambda t: t[0])
    boundaries = [(s, k, s) for s, k in inferred]

    # Pass 2 — slice each watch's body
    watches = []
    for idx, (start, key, header_idx) in enumerate(boundaries):
        end = boundaries[idx + 1][0] if idx + 1 < len(boundaries) else len(lines)
        body = lines[start + 1:end]

        # Detect intro line: first non-empty content line that is NOT a section marker.
        intro = ""
        body_start_offset = 0
        for j, raw in enumerate(body):
            s = raw.strip()
            if not s:
                body_start_offset = j + 1
                continue
            # If the line starts with a watch-title emoji + watch name (Format C: "🌅 Morning Wisdom — intro"),
            # split title from intro.
            m = re.match(r"^\s*[🌅🕖🕚🕒🌙☀]\s*(.+)$", raw)
            if m:
                rest = m.group(1).strip()
                # Strip the watch title prefix if present
                # e.g. "Morning Wisdom — gentle answer ..."
                for kw, kkey in TITLE_KEYWORDS.items():
                    pat = re.compile(r"^\s*" + re.escape(kw) + r"\b\s*(?:—|-|:)?\s*", re.IGNORECASE)
                    rest2 = pat.sub("", rest, count=1)
                    if rest2 != rest:
                        rest = rest2
                        break
                if rest:
                    intro = rest
                body_start_offset = j + 1
                break
            # If line is a section marker, no intro
            if any(rx.search(raw) for _, rx in SECTION_REGEX):
                body_start_offset = j
                break
            # Otherwise it's an intro paragraph line
            intro = s
            body_start_offset = j + 1
            break

        body_lines = body[body_start_offset:]
        watches.append((key, intro, body_lines))
    return watches


def parse_sections(body_lines):
    """Given the body of one watch (excluding header + intro), return ordered list
    of (section_key, raw_marker_line, content_lines) where content_lines do NOT include
    the marker line itself."""
    # Find section starts
    starts = []  # (line_idx, key)
    for i, line in enumerate(body_lines):
        for key, rx in SECTION_REGEX:
            if rx.search(line):
                # Avoid double-detect of scripture vs scripture_alt — first match wins
                starts.append((i, key, line))
                break

    sections = []
    for idx, (start, key, marker_line) in enumerate(starts):
        end = starts[idx + 1][0] if idx + 1 < len(starts) else len(body_lines)
        content = body_lines[start + 1:end]
        # Drop only leading ⸻ / --- separator lines and blank lines
        while content and (not content[0].strip() or content[0].strip() in ("⸻", "---")):
            content.pop(0)
        while content and (not content[-1].strip() or content[-1].strip() in ("⸻", "---")):
            content.pop()
        sections.append((key, marker_line, content))
    return sections


def extract_scripture_ref(marker_line):
    """From a scripture marker line, extract the reference (everything after '— ' or after the first ':' / leading bold).
    Examples:
      "📖 Scripture — John 1:1–18"               -> "John 1:1–18"
      "📖 **Proverbs 25:15-28**"                  -> "Proverbs 25:15-28"
      "📖 Scripture — Proverbs 15:1–15"           -> "Proverbs 15:1–15"
    """
    s = marker_line.strip()
    s = re.sub(r"^📖\s*", "", s)
    s = re.sub(r"^\*\*|\*\*$", "", s)
    s = re.sub(r"^Scripture\s*[—\-–:]\s*", "", s, flags=re.IGNORECASE)
    # strip any trailing bold/italic markers
    s = s.strip().strip("*").strip()
    return s


def extract_real_man_trait(marker_line):
    """From a REAL MAN reflection marker, pull the trait.
    'Reflection for a REAL MAN — Manages Faithfully'   -> 'Manages Faithfully'
    """
    m = re.search(r"REAL MAN\b\s*[—\-–:]\s*(.+?)\s*(?:\*\*|$)", marker_line, re.IGNORECASE)
    return m.group(1).strip() if m else ""


def extract_virtue(marker_line, framework):
    """For HAPPY / FULFILLED / RESOLUTE — pull the trait letter + virtue name when present.
    Returns (letter, virtue) or (None, "")"""
    # Common shapes:
    #   "❤️ Reflection for Your Wife — H.A.P.P.Y. Husband — Protecting"
    #   "❤️ Reflection for Your Wife — HAPPY (Honest)"
    #   "❤️ Reflection for Your Wife (Honest)"
    s = marker_line.strip()
    # Try "— <trait>" at end
    m = re.search(r"[—\-–]\s*([A-Z][a-zA-Z]+)\s*$", s)
    if m:
        v = m.group(1)
        return (v[0].upper(), v)
    # Try parenthetical
    m = re.search(r"\(([A-Z][a-zA-Z]+)\)", s)
    if m:
        v = m.group(1)
        return (v[0].upper(), v)
    return (None, "")


# ────────────────────────────────────────────────────────────────────────
# RENDERING — HTML PIECES
# ────────────────────────────────────────────────────────────────────────

def md_to_html_lines(content_lines):
    """Convert a content block to safe HTML paragraphs.
    Blank lines separate paragraphs. Strips trailing ⸻ separators."""
    paragraphs = []
    current = []
    for line in content_lines:
        s = line.rstrip()
        if not s.strip():
            if current:
                paragraphs.append(current)
                current = []
            continue
        if s.strip() in ("⸻", "---", "—"):
            if current:
                paragraphs.append(current)
                current = []
            continue
        current.append(s)
    if current:
        paragraphs.append(current)

    out = []
    for para in paragraphs:
        joined = "<br>".join(escape(line) for line in para)
        # render simple **bold** -> <strong>
        joined = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", joined)
        out.append(f"<p>{joined}</p>")
    return "\n".join(out)


def render_scripture_block(marker_line, content_lines):
    """Render Scripture as poetic sense-lines preserved (each line a separate <p>),
    grouping stanzas around blank lines."""
    ref = extract_scripture_ref(marker_line)
    # Render scripture: preserve line breaks within stanzas, blank lines = new <p> stanza
    stanzas = []
    current = []
    for line in content_lines:
        if not line.strip():
            if current:
                stanzas.append(current)
                current = []
            continue
        current.append(line.rstrip())
    if current:
        stanzas.append(current)

    body = []
    for st in stanzas:
        if len(st) == 1:
            body.append(f"<p>{escape(st[0])}</p>")
        else:
            joined = "<br>".join(escape(l) for l in st)
            body.append(f'<p class="stanza">{joined}</p>')

    return f"""<div class="scripture">
<div class="scripture-ref">📖 {escape(ref)}</div>
<div class="scripture-text">
{chr(10).join(body)}
</div>
</div>"""


def render_section(label_emoji, label_text, content_html, extra_class=""):
    cls = f"section {extra_class}".strip()
    return f"""<div class="{cls}">
<div class="section-label">{label_emoji} {escape(label_text)}</div>
{content_html}
</div>"""


def render_prayer(content_lines, title="Prayer"):
    body = md_to_html_lines(content_lines)
    return f"""<div class="prayer">
<div class="prayer-title">🙏 {escape(title)}</div>
{body}
</div>"""


def render_helm(marker_line, content_lines):
    """Helm Command / Rudder Steer line — may wrap to additional content lines.
    Always concatenate marker_line tail + content_lines for full command text."""
    s = marker_line.strip()
    m = re.match(r"^\s*⚓\s*(?:\*\*)?\s*(Helm Command|Rudder Steer|Set Sail|Course Correction|Steady As She Goes|Night Orders)\s*(?:\*\*)?\s*[:\-—]?\s*(.*)$",
                 s, re.IGNORECASE)
    if m:
        label = m.group(1)
        tail = m.group(2).strip()
    else:
        label = "Helm Command"
        tail = s.lstrip("⚓").strip()
    # Always join continuation lines so wrapped commands aren't truncated.
    # Filter out separator lines (⸻ runs, ---) that belong between watches, not
    # inside the command itself.
    keep = []
    for l in content_lines:
        s = l.strip()
        if not s:
            continue
        if re.fullmatch(r"[⸻\-—]{2,}", s):
            continue
        keep.append(s)
    extra = " ".join(keep)
    command = (tail + " " + extra).strip()
    # Strip trailing separator runs that may have hitched onto the last line
    command = re.sub(r"\s*[⸻\-—]{3,}\s*$", "", command)
    command = command.strip().strip("*").strip()
    return f'<div class="helm"><span class="helm-icon">⚓</span> <span class="helm-label">{escape(label)}:</span> {escape(command)}</div>'


def render_audio_slot(date, watch_key):
    rel = f"../assets/audio/readings/{date}-{watch_key}.mp3"
    abs_path = REPO / f"docs/assets/audio/readings/{date}-{watch_key}.mp3"
    if abs_path.exists():
        return f"""<div class="audio-slot">
  <audio controls preload="metadata" style="width:100%;max-width:560px;">
    <source src="{rel}" type="audio/mpeg">
    Your browser does not support audio.
  </audio>
  <div class="audio-cap">🎙️ ElevenLabs voiceover — {WATCH_BY_KEY[watch_key]['title']}</div>
</div>"""
    return f"""<div class="audio-slot audio-pending">
  <div class="audio-cap">🎙️ ElevenLabs voiceover — coming for this watch</div>
</div>"""


def render_watch(date, watch_key, intro, body_lines):
    """Render one full watch section to HTML."""
    w = WATCH_BY_KEY[watch_key]
    pieces = [f'<section class="watch watch-{watch_key}" id="watch-{watch_key}" data-watch="{watch_key}">']
    pieces.append(
        f'<div class="watch-header">'
        f'<span class="watch-time">{w["time"]}</span> '
        f'<h2>{escape(w["title"])}</h2></div>'
    )
    if intro:
        pieces.append(f'<p class="intro">{escape(intro)}</p>')

    pieces.append(render_audio_slot(date, watch_key))

    sections = parse_sections(body_lines)
    rendered_keys = set()

    for key, marker_line, content in sections:
        if key in ("scripture", "scripture_alt"):
            pieces.append(render_scripture_block(marker_line, content))
        elif key == "context":
            # detect which context-type from the marker text for label
            mt = marker_line.lower()
            if "briefing" in mt:
                label_emoji, label = "🗺️", "Briefing Summary"
            elif "field notes" in mt:
                label_emoji, label = "🗺️", "Field Notes"
            elif "situation report" in mt:
                label_emoji, label = "🛰️", "Situation Report"
            else:
                label_emoji, label = "🧭", "Context Summary"
            pieces.append(render_section(label_emoji, label, md_to_html_lines(content), "context"))
        elif key == "real_man":
            trait = extract_real_man_trait(marker_line)
            label = f"Reflection for a REAL MAN — {trait}" if trait else "Reflection for a REAL MAN"
            pieces.append(render_section("🛡️", label, md_to_html_lines(content), "reflection"))
        elif key == "happy":
            letter, virtue = extract_virtue(marker_line, "happy")
            label = f"Reflection for Your Wife — H.A.P.P.Y. Husband — {virtue}" if virtue else "Reflection for Your Wife — H.A.P.P.Y. Husband"
            pieces.append(render_section("❤️", label, md_to_html_lines(content), "reflection"))
        elif key == "fulfilled":
            letter, virtue = extract_virtue(marker_line, "fulfilled")
            label = f"Reflection for Your Children — F.U.L.F.I.L.L.E.D. Father — {virtue}" if virtue else "Reflection for Your Children — F.U.L.F.I.L.L.E.D. Father"
            pieces.append(render_section("👨‍👦", label, md_to_html_lines(content), "reflection"))
        elif key == "resolute":
            letter, virtue = extract_virtue(marker_line, "resolute")
            label = f"Reflection for a R.E.S.O.L.U.T.E. Citizen — {virtue}" if virtue else "Reflection for a R.E.S.O.L.U.T.E. Citizen"
            pieces.append(render_section("🛡️", label, md_to_html_lines(content), "reflection resolute"))
        elif key == "history":
            # try to pull "January 1" date from marker line
            m = re.search(r"American History\s*[—\-–]\s*(.+?)\s*$", marker_line)
            dlabel = m.group(1).strip() if m else ""
            label = f"This Day in American History — {dlabel}" if dlabel else "This Day in American History"
            pieces.append(render_section("🦅", label, md_to_html_lines(content), "history"))
        elif key == "evening_ref":
            pieces.append(render_section("🌾", "Reflection for a Man at Home and in Community", md_to_html_lines(content), "reflection"))
        elif key == "application":
            # Render as bullet list if content has bullets, else as prose.
            # A bullet may wrap across multiple lines — only the FIRST line of each
            # bullet starts with •/-/* so subsequent unmarked lines must be merged
            # back into the previous bullet (not treated as separate prose).
            bullets = []
            leading_prose = []   # any prose BEFORE the first bullet
            trailing_prose = []  # prose AFTER the last bullet
            mode = "leading"     # "leading" -> "bullets" -> "trailing"
            for line in content:
                ls = line.strip()
                if not ls:
                    continue
                if ls.startswith(("•", "-")) and not ls.startswith(("**", "---")):
                    bullets.append(ls.lstrip("•- \t"))
                    mode = "bullets"
                elif ls.startswith("*") and not ls.startswith("**"):
                    bullets.append(ls.lstrip("* \t"))
                    mode = "bullets"
                else:
                    if mode == "bullets":
                        # Continuation of the previous bullet OR trailing prose.
                        # Heuristic: if the line looks like a sentence start (Capital
                        # letter beginning + ends a thought), treat as trailing prose;
                        # if it looks like a wrap (lowercase, or no terminal punct on
                        # the previous bullet), merge into previous bullet.
                        prev_ends_clean = bullets[-1].rstrip().endswith((".", "!", "?", ":", ";"))
                        looks_like_new_sentence = ls[:1].isupper() and prev_ends_clean
                        if looks_like_new_sentence:
                            trailing_prose.append(ls)
                            mode = "trailing"
                        else:
                            bullets[-1] = bullets[-1].rstrip() + " " + ls
                    elif mode == "trailing":
                        trailing_prose.append(ls)
                    else:
                        leading_prose.append(ls)
            # Render
            prose = leading_prose + trailing_prose
            inner = []
            if bullets:
                inner.append("<ul class='application'>")
                for b in bullets:
                    # Bold any leading **label**
                    bh = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escape(b).replace("&amp;lt;", "<").replace("&amp;gt;", ">"))
                    inner.append(f"<li>{bh}</li>")
                inner.append("</ul>")
            if prose:
                p = "<br>".join(escape(p) for p in prose)
                p = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", p)
                inner.append(f"<p class='application-prose'>{p}</p>")
            pieces.append(render_section("⛏️", "Personal Application", "\n".join(inner), "application-block"))
        elif key in ("prayer", "prayer_alt"):
            # Determine prayer subtitle (might be "Prayer from the Stateroom", etc.)
            m = re.search(r"(Prayer(?:\s+from\s+the\s+\w+)?)", marker_line, re.IGNORECASE)
            title = m.group(1) if m else w["prayer_default"]
            pieces.append(render_prayer(content, title=title))
        elif key == "helm":
            pieces.append(render_helm(marker_line, content))
        rendered_keys.add(key)

    pieces.append('</section>')
    return "\n".join(pieces)


# ────────────────────────────────────────────────────────────────────────
# PAGE-LEVEL RENDER
# ────────────────────────────────────────────────────────────────────────

CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
    --bg-dark: #000000; --bg-card: #111111; --bg-card2: #161616;
    --gold: #D4AF37; --gold-light: #F4D470;
    --white: #FFFFFF; --gray: #888888; --border: #333333;
}
body {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-dark);
    color: var(--white);
    min-height: 100vh;
    line-height: 1.7;
}
h1, h2, h3 { font-family: 'Playfair Display', serif; font-weight: 700; }
.container { max-width: 820px; margin: 0 auto; padding: 24px 20px 60px; }
a { color: var(--gold); text-decoration: none; }
a:hover { color: var(--gold-light); text-decoration: underline; }

.nav-back { margin-bottom: 14px; font-size: 0.95rem; }

.hero { text-align: center; padding: 16px 0 10px; border-bottom: 1px solid var(--border); margin-bottom: 18px; }
.hero h1 { font-size: clamp(1.5rem, 4vw, 2.2rem); color: var(--white); margin-bottom: 6px; }
.hero .subtitle { color: var(--gold); font-size: 0.95rem; font-style: italic; }
.hero .doc-line { color: var(--gray); font-size: 0.82rem; margin-top: 6px; }

.watch-tabs {
    position: sticky; top: 0; z-index: 30;
    background: var(--bg-dark);
    border-bottom: 1px solid var(--border);
    display: flex; flex-wrap: wrap; gap: 6px;
    padding: 12px 0 14px;
    margin-bottom: 18px;
}
.watch-tab {
    flex: 1 1 90px;
    text-align: center;
    padding: 8px 6px;
    border: 1px solid var(--border);
    border-radius: 100px;
    background: var(--bg-card);
    color: var(--gray);
    font-size: 0.85rem; font-weight: 500;
    transition: all 0.15s ease;
    text-decoration: none !important;
    white-space: nowrap;
}
.watch-tab:hover { color: var(--white); border-color: var(--gold); text-decoration: none !important; }
.watch-tab.active { background: var(--gold); color: #000; border-color: var(--gold); font-weight: 600; }
.watch-tab .tab-time { display: block; font-size: 0.7rem; opacity: 0.7; font-family: monospace; }
.watch-tab.active .tab-time { opacity: 1; }

/* "NOW" badge — shown on the watch tab whose time window contains current local time */
.watch-tab.is-now { position: relative; box-shadow: 0 0 0 1px var(--gold-light) inset; }
.watch-tab.is-now::after {
  content: "NOW";
  position: absolute; top: -7px; right: -4px;
  background: var(--gold-light); color: #000;
  font-size: 0.55rem; font-weight: 700;
  padding: 1px 5px; border-radius: 100px;
  letter-spacing: 0.08em;
}

.watch {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 24px 22px;
    margin-bottom: 22px;
    scroll-margin-top: 80px;
}
.watch-header { display: flex; align-items: baseline; gap: 14px; margin-bottom: 10px; flex-wrap: wrap; }
.watch-time {
    background: var(--bg-card2); color: var(--gold);
    padding: 4px 12px; border-radius: 100px;
    font-family: 'Inter', monospace; font-size: 0.85rem; font-weight: 600;
    letter-spacing: 0.05em;
}
.watch-header h2 { font-size: 1.35rem; color: var(--white); }

.intro { color: var(--gray); font-style: italic; margin-bottom: 14px; }

.audio-slot {
    margin: 14px 0 18px;
    padding: 12px 14px;
    background: var(--bg-card2);
    border-radius: 8px;
    border: 1px dashed var(--border);
}
.audio-slot.audio-pending { opacity: 0.55; }
.audio-cap { font-size: 0.8rem; color: var(--gray); margin-top: 4px; }

.scripture {
    background: var(--bg-card2);
    border-left: 3px solid var(--gold);
    border-radius: 6px;
    padding: 16px 20px;
    margin: 16px 0 22px;
}
.scripture-ref { font-weight: 600; color: var(--gold); margin-bottom: 12px; font-size: 0.95rem; }
.scripture-text p { margin-bottom: 8px; }
.scripture-text p.stanza { margin-bottom: 14px; }

.section-label {
    font-family: 'Playfair Display', serif;
    color: var(--gold); font-weight: 700; font-size: 1.05rem;
    margin: 22px 0 10px; padding-top: 10px; border-top: 1px solid var(--border);
}
.section p, .context p, .reflection p, .history p, .application-block p { margin-bottom: 12px; }

ul.application { padding-left: 22px; margin: 8px 0 14px; }
ul.application li { margin-bottom: 8px; }
.application-prose { font-style: italic; color: var(--gold-light); margin-top: 12px; }

.history ul { padding-left: 22px; margin: 8px 0; }
.history li { margin-bottom: 6px; }

.prayer {
    background: var(--bg-card2);
    border-left: 3px solid var(--gold-light);
    border-radius: 6px;
    padding: 16px 20px;
    margin: 22px 0;
}
.prayer-title { color: var(--gold-light); font-weight: 600; margin-bottom: 10px; font-size: 0.95rem; }
.prayer p { line-height: 1.85; margin-bottom: 8px; }

.helm {
    background: var(--bg-card2);
    border-radius: 6px;
    padding: 12px 18px;
    margin-top: 14px;
    font-size: 0.95rem;
}
.helm-icon { color: var(--gold); font-size: 1.1rem; }
.helm-label { color: var(--gold); font-weight: 600; }

footer {
    text-align: center;
    color: var(--gray);
    font-size: 0.82rem;
    margin-top: 32px;
    padding-top: 18px;
    border-top: 1px solid var(--border);
}
footer .draft-tag {
    display: inline-block;
    background: #2a2410;
    color: var(--gold);
    padding: 4px 12px;
    border-radius: 100px;
    font-size: 0.78rem;
    margin-bottom: 8px;
    letter-spacing: 0.05em;
}

@media (max-width: 540px) {
    .watch-tab { flex: 1 1 64px; font-size: 0.78rem; padding: 6px 4px; }
    .watch-tab .tab-time { font-size: 0.65rem; }
}
"""

TAB_JS = """
(function(){
  const SLUGS = ['all','wisdom','husband','father','citizen','peace'];

  // Watch windows in local hours (each watch is "live" from its start time
  // until the NEXT watch begins). Evening peace owns 21:00 → 04:59.
  function currentWatchSlug() {
    const h = new Date().getHours();
    if (h >= 5  && h < 7)  return 'wisdom';
    if (h >= 7  && h < 11) return 'husband';
    if (h >= 11 && h < 15) return 'father';
    if (h >= 15 && h < 21) return 'citizen';
    return 'peace';                       // 21:00 – 04:59
  }
  const NOW_SLUG = currentWatchSlug();

  function markNowBadge(){
    document.querySelectorAll('.watch-tab').forEach(t => {
      t.classList.toggle('is-now', t.dataset.tab === NOW_SLUG);
    });
  }
  function showOnly(slug){
    const isAll = slug === 'all' || !SLUGS.includes(slug);
    document.querySelectorAll('section.watch').forEach(s => {
      s.style.display = (isAll || s.dataset.watch === slug) ? '' : 'none';
    });
    document.querySelectorAll('.watch-tab').forEach(t => {
      t.classList.toggle('active', t.dataset.tab === (isAll ? 'all' : slug));
    });
  }
  document.querySelectorAll('.watch-tab').forEach(t => {
    t.addEventListener('click', function(e){
      e.preventDefault();
      const slug = this.dataset.tab;
      history.replaceState(null, '', '#' + slug);
      showOnly(slug);
      window.scrollTo({top: 0, behavior:'smooth'});
    });
  });

  // Initial selection priority:
  //   1. URL hash if present  (#all / #wisdom / #husband / #father / #citizen / #peace)
  //   2. Auto-select the watch that is "live right now"
  let initial;
  if (location.hash) {
    initial = location.hash.slice(1);
  } else {
    initial = NOW_SLUG;
  }
  markNowBadge();
  showOnly(initial);
})();
"""


def render_tabs():
    tabs = [('all', 'All Watches', '')]
    for w in WATCHES:
        short = w["title"].split("—")[0].strip()  # "Morning Wisdom", "First Watch", etc.
        # Trim "First/Second/Third Watch" labels to one-word tab labels for compactness
        short_map = {"First Watch": "Husband", "Second Watch": "Father", "Third Watch": "Citizen"}
        label = short_map.get(short, short)
        tabs.append((w["key"], label, w["time"]))
    out = ['<nav class="watch-tabs" role="tablist">']
    for slug, label, time in tabs:
        active = ' active' if slug == 'all' else ''
        time_html = f'<span class="tab-time">{time}</span> ' if time else ''
        out.append(f'<a href="#{slug}" class="watch-tab{active}" data-tab="{slug}" role="tab">{time_html}<span class="tab-label">{escape(label)}</span></a>')
    out.append('</nav>')
    return "\n".join(out)


def doc_line_for(dt):
    return "MOOP's 2026 Daily Bible Readings"


def render_page(date_str, md_text):
    dt = datetime.fromisoformat(date_str)
    day_of_year = dt.timetuple().tm_yday
    date_label = dt.strftime("%A, %B ") + str(dt.day) + dt.strftime(", %Y")

    watches = split_into_watches(md_text)
    if not watches:
        print(f"  ⚠ no watches detected in {date_str}.md")
        return None

    watches_html = "\n\n".join(render_watch(date_str, key, intro, body) for key, intro, body in watches)
    tabs_html = render_tabs()

    title = escape(date_label) + " — Daily Reading | U.S.M.C. Ministries"
    doc_line = doc_line_for(dt)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="container">

<div class="nav-back">← <a href="/chronological.html">The Watchman's Chronological Plan</a></div>

<div class="hero">
<h1>{escape(date_label)}</h1>
<div class="subtitle">Daily Reading — Day {day_of_year} of 365</div>
<div class="doc-line">{escape(doc_line)}</div>
</div>

{tabs_html}

{watches_html}

<footer>
<div class="draft-tag">PROTOTYPE — sign-off pending</div>
<div>U.S.M.C. Ministries · The Watchman's Chronological Plan for the Year of our Lord 2026</div>
<div style="margin-top:6px;font-size:0.78rem;">Adam Johns &middot; rich interpretive blend &middot; divine name LORD</div>
</footer>

</div>
<script>{TAB_JS}</script>
</body>
</html>
"""
    return html


def write_inventory():
    """Scan docs/readings/*.html and write docs/assets/readings-available.json
    so chronological.html can gate the 'Open Full Reading' link."""
    import json
    dates = sorted(
        f.stem for f in OUT_DIR.glob("*.html")
        if re.match(r"^\d{4}-\d{2}-\d{2}\.html$", f.name)
    )
    inv = {
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "count": len(dates),
        "dates": dates,
    }
    inv_path = REPO / "docs" / "assets" / "readings-available.json"
    inv_path.parent.mkdir(parents=True, exist_ok=True)
    inv_path.write_text(json.dumps(inv, indent=2))
    print(f"Inventory: {len(dates)} dates -> {inv_path}")


def build_one(date_str):
    src = DATA_DIR / f"{date_str}.md"
    if not src.exists():
        print(f"  ⚠ missing: {src}")
        return False
    md_text = src.read_text()
    html = render_page(date_str, md_text)
    if html is None:
        return False
    out = OUT_DIR / f"{date_str}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    kb = out.stat().st_size / 1024
    print(f"  ✓ {date_str}  ({kb:.1f} KB)")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("date", nargs="?", help="single date like 2026-01-01")
    ap.add_argument("--all", action="store_true", help="render every .md in data/readings/")
    ap.add_argument("--date-range", nargs=2, metavar=("START", "END"), help="render range inclusive")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.all:
        files = sorted(DATA_DIR.glob("*.md"))
        # Skip the canonical reference variants (they're not actual day files)
        files = [f for f in files if re.match(r"^\d{4}-\d{2}-\d{2}\.md$", f.name)]
        print(f"Rendering {len(files)} day(s):")
        ok = 0
        for f in files:
            if build_one(f.stem):
                ok += 1
        print(f"\nDone: {ok}/{len(files)} rendered.")
        write_inventory()
    elif args.date_range:
        start = datetime.fromisoformat(args.date_range[0])
        end = datetime.fromisoformat(args.date_range[1])
        ok, total = 0, 0
        cur = start
        from datetime import timedelta
        while cur <= end:
            total += 1
            if build_one(cur.strftime("%Y-%m-%d")):
                ok += 1
            cur += timedelta(days=1)
        print(f"\nDone: {ok}/{total} rendered.")
    elif args.date:
        build_one(args.date)
    else:
        ap.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
