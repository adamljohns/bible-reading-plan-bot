#!/usr/bin/env python3
"""voice_audit_blog.py — scan blog posts (or any HTML/MD) for AI-tell phrases.

Modeled on bin/dict_drift_audit.py. Reports each AI-tell hit with file,
line context, suggested human-voice replacement, and category. Does NOT
rewrite automatically — produces a report; the human reviews and revises.

Categories of AI-tell:
  - filler          : "It's worth noting that..." / "It's important to note..."
  - empty-verb      : "delve into" / "navigate" / "embrace" / "leverage"
  - corporate       : "robust" / "comprehensive" / "seamless" / "synergy"
  - tricolon        : Three-item parallel constructions overused
  - x-not-just-y    : "X is not just Y, it's Z" / "not just A, but B"
  - transition-glue : "Furthermore," / "Moreover," / "Additionally,"
  - hedge           : "Some might argue" / "Many would say"
  - empty-intro     : "In today's world" / "In an era of"
  - weasel-quant    : "various" / "numerous" / "myriad" / "plethora"
  - therapy         : "validate" / "harmful" / "unhealthy" / "lived experience"
  - em-dash-overuse : Three or more em-dashes in a single paragraph

Cadence check (2026-11-17, Adam's ruling on "the choppiness, the two-word
sentences" and the word "actually"). For every post it also prints one
PASS/FAIL line counting:
  - pairs      : staccato pairs ("That is not X. That is Y." / "Not X. Y.")
  - turns      : the same turn inside one sentence ("is not X; it is Y")
  - frag-runs  : runs of two or more sentences of four words or fewer
  - para-runs  : one-sentence paragraphs (ten words or fewer) used in sequence
  - mean-sentence : average sentence length in words
  - actually / avoid : "actually" and the avoid list built from Adam's own
    2007-2024 posts (BLOG-VOICE-GUIDE.md, "Adam's own words")
A post FAILS on: cadence > 2.0 per 1,000 words (4 or more), avoid list > 4.0
per 1,000 words (5 or more), "actually" > 2.5 per 1,000 words (4 or more), or
a mean sentence under 13 words. Exit status is 1 when any post fails or any
hard catalog phrase is found. Quotations in <blockquote>, Scripture blocks,
pull-quotes, bylines, source lists and call-to-action boxes are not counted.

Usage:
  python3 bin/voice_audit_blog.py docs/blog/                 # all blog posts
  python3 bin/voice_audit_blog.py docs/blog/specific-post.html
  python3 bin/voice_audit_blog.py docs/blog/ --markdown > voice-audit.md
  python3 bin/voice_audit_blog.py docs/blog/ --summary       # PASS/FAIL lines only
  python3 bin/voice_audit_blog.py post.html --no-cadence     # catalog only
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# AI-tell catalog.
# Each entry: (category, pattern, severity, suggestion).
# ---------------------------------------------------------------------------

AI_TELLS: list[tuple[str, str, str, str]] = [
    # ----- filler -----
    ("filler", r"\bit['’]s worth noting that\b", "hard", "Cut entirely; if the thing's worth noting, say it."),
    ("filler", r"\bit['’]s important to (?:note|remember|understand) that\b", "hard", "Cut entirely; just say the thing."),
    ("filler", r"\bit should be noted that\b", "hard", "Cut entirely."),
    ("filler", r"\bit goes without saying that\b", "hard", "If it goes without saying, don't say it."),
    ("filler", r"\bneedless to say\b", "hard", "Cut entirely."),
    ("filler", r"\bin conclusion,\b", "hard", "Cut. End the piece with the actual conclusion."),
    ("filler", r"\bto summari[sz]e,\b", "hard", "Cut; or write the actual summary."),
    ("filler", r"\bin essence,\b", "hard", "Cut."),
    ("filler", r"\bat the end of the day,?\b", "soft", "Often filler; cut or rephrase concretely."),
    ("filler", r"\bin today['’]s (?:world|society|economy|landscape)\b", "hard", "Cliché opener; replace with specific date / event."),
    ("filler", r"\bin an era of\b", "hard", "Cliché opener; replace with specific context."),

    # ----- empty verbs -----
    ("empty-verb", r"\bdelv(?:e|ing) into\b", "hard", "Replace: explore, examine, dig into, study."),
    ("empty-verb", r"\bnavigate (?:the|this|these|complex)\b", "soft", "Often AI-corporate; replace: work through, traverse, handle."),
    ("empty-verb", r"\bembrace\b(?!\s+(?:the\s+cross|the\s+gospel|repentance|sanctification))", "soft", "Often AI-corporate; replace: accept, take up, receive."),
    ("empty-verb", r"\bleverage\b", "hard", "Corporate-speak; replace: use, draw on, take advantage of."),
    ("empty-verb", r"\bunlock (?:the\s+)?(?:potential|power)\b", "hard", "Corporate; replace with specific action."),
    ("empty-verb", r"\bgame[- ]?chang(?:e|er|ing)\b", "hard", "Cliché; replace with specific impact."),
    ("empty-verb", r"\btap into\b", "soft", "Often filler; replace: draw on, use, access."),
    ("empty-verb", r"\bharness\b", "soft", "Corporate; replace: use, channel, employ."),

    # ----- corporate buzzwords -----
    ("corporate", r"\brobust\b", "soft", "Corporate; replace: strong, sturdy, well-built, dependable."),
    ("corporate", r"\bcomprehensive\b", "soft", "Corporate; replace: full, complete, thorough, broad."),
    ("corporate", r"\bseamless\b", "soft", "Corporate; replace: smooth, uninterrupted, unbroken."),
    ("corporate", r"\bsynerg(?:y|ies|istic)\b", "hard", "Corporate-jargon; cut or rephrase concretely."),
    ("corporate", r"\bstreamlin\w+\b", "soft", "Corporate; replace: simplify, tighten, speed up."),
    ("corporate", r"\bholistic\b", "soft", "Often vague; replace: full-orbed, whole-person, complete."),
    ("corporate", r"\bcutting[- ]edge\b", "soft", "Cliché; replace: newest, latest, recent."),
    ("corporate", r"\bbest practices?\b", "soft", "Corporate; replace: proven methods, tested approaches."),
    ("corporate", r"\bvalue proposition\b", "hard", "Corporate-jargon."),

    # ----- X not just Y but Z -----
    ("x-not-just-y", r"\b(?:is|are|was|were)\s+not just\s+\w+", "soft", "Overused AI construction; vary the rhetoric."),
    ("x-not-just-y", r"\b(?:isn['’]t|aren['’]t|wasn['’]t|weren['’]t)\s+just\s+about\s+\w+", "soft", "Overused AI construction; vary the rhetoric."),
    ("x-not-just-y", r"\bmore than just\s+a\b", "soft", "Overused construction."),

    # ----- transition glue -----
    ("transition-glue", r"^\s*Furthermore,", "soft", "AI transition glue; cut or replace with concrete bridge."),
    ("transition-glue", r"^\s*Moreover,", "soft", "AI transition glue; cut."),
    ("transition-glue", r"^\s*Additionally,", "soft", "AI transition glue; cut."),
    ("transition-glue", r"^\s*Furthermore,?\s+", "soft", "AI transition glue."),
    ("transition-glue", r"\.\s+Furthermore,", "soft", "AI transition glue; restructure or cut."),
    ("transition-glue", r"\.\s+Moreover,", "soft", "AI transition glue; restructure or cut."),
    ("transition-glue", r"\.\s+Additionally,", "soft", "AI transition glue; restructure or cut."),

    # ----- hedge -----
    ("hedge", r"\bsome (?:might|would|may)\s+argue\b", "soft", "Hedge; name the actual argument or cut."),
    ("hedge", r"\bmany (?:would|might|may)\s+say\b", "soft", "Hedge; name actual speakers or cut."),
    ("hedge", r"\barguably\b", "soft", "Hedge; either argue or drop."),
    ("hedge", r"\bsome\s+(?:believe|think|argue|hold|claim)\b", "soft", "Hedge; name actual people or cut."),

    # ----- weasel quantifiers -----
    ("weasel-quant", r"\bnumerous\b", "soft", "Corporate; replace: many, several, lots of, dozens of (be specific)."),
    ("weasel-quant", r"\bmyriad\b", "soft", "Often filler; replace: many, countless (specific number if possible)."),
    ("weasel-quant", r"\bplethora\b", "hard", "AI-corporate; replace: many, lots of, surplus."),
    ("weasel-quant", r"\bvarious\b", "soft", "Often vague; replace: several / a few / specific list."),
    ("weasel-quant", r"\ba multitude of\b", "soft", "Often AI-pompous; replace: many, lots of."),

    # ----- therapy register -----
    ("therapy", r"\btrauma\b(?!tic\s+event)", "soft", "Therapy-culture; replace: suffering, affliction, the breaking of body / soul."),
    ("therapy", r"\bharmful\b(?!\s+to\s+(?:the\s+soul|the\s+body))", "soft", "Therapy-culture; replace: sinful, against God's law, against the soul's good."),
    ("therapy", r"\bsafe space\b", "hard", "Not a biblical category; reject."),
    ("therapy", r"\blived experience\b", "soft", "Therapy-culture; replace: testimony, witness."),
    ("therapy", r"\bvalidate\b", "soft", "Therapy-culture; replace: confirm, affirm, commend."),
    ("therapy", r"\bunhealthy patterns?\b", "soft", "Therapy-culture; replace: sin patterns, besetting sins."),

    # ----- empty-intro -----
    ("empty-intro", r"^(?:In|For)\s+(?:today|this day and age|the modern world|our modern world)", "hard", "AI-cliché opener; replace with specific date / event."),
    ("empty-intro", r"\bever-(?:changing|evolving|growing)\b", "soft", "AI-cliché; replace with specific change being noted."),

    # ----- mid-sentence semicolons (often AI tell when overused) — flagged as soft -----
    # (We don't ban semicolons; we just note overuse.)
]

OK_MARKER = re.compile(r"(?:#|<!--)\s*voice-ok:\s*([^:]+):\s*(.+?)(?:-->|\n|$)", re.I)


@dataclass
class Finding:
    file: str
    line_hint: int
    category: str
    severity: str
    matched: str
    context: str
    suggestion: str


def _strip_html(s: str) -> str:
    s = re.sub(r"<script\b.*?</script>", " ", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<style\b.*?</style>", " ", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"&[a-zA-Z][a-zA-Z0-9]*;", " ", s)
    return s


def _context(text: str, start: int, end: int, pad: int = 50) -> str:
    a = max(0, start - pad)
    b = min(len(text), end + pad)
    snippet = text[a:b]
    snippet = re.sub(r"\s+", " ", snippet)
    return ("..." if a > 0 else "") + snippet + ("..." if b < len(text) else "")


def _line_hint(text: str, idx: int) -> int:
    return text[:idx].count("\n") + 1


# ---------------------------------------------------------------------------
# Cadence check (added 2026-11-17).
#
# The catalog above cannot see the tell that makes a post sound generated:
# staccato pairs ("That is not X. That is Y."), runs of fragments, and
# one-line paragraphs stacked for effect. These functions read the article
# body the way a reader does (paragraph by paragraph, sentence by sentence)
# and count them. Thresholds are set from Adam's own 2007-2024 posts, which
# must pass. See BLOG-VOICE-GUIDE.md, "Cadence" and "Adam's own words".
# ---------------------------------------------------------------------------

# Words and phrases far more frequent in the machine-drafted 2026 posts than
# in Adam's own posts (rate per 10,000 words measured over the whole blog;
# see BLOG-VOICE-GUIDE.md section 0.2). "actually" is first by his own ruling.
AVOID: list[tuple[str, str]] = [
    (r"\bactually\b", "really / definitely / in fact, or cut it"),
    (r"\b(?:that|this) is not\b", "say what it is, in one sentence, with the reason attached"),
    (r"\b(?:that|this|it) is the whole\b|\bthe whole (?:point|thing|game|difference|story)\b", "'my point is' / 'the bottom line'"),
    (r"\bhere is (?:the|what|where|why|how)\b|\bhere['’]s (?:the thing|what|where|why)\b", "cut the drum-roll; say the thing"),
    (r"\bread that (?:again|twice|slowly|back)\b", "cut; let the sentence stand"),
    (r"\bis exactly\b|\bthe exact\b", "cut 'exactly' / 'the same'"),
    (r"\bquietly\b", "cut"),
    (r"\bhonest\b", "cut, or 'full disclosure' where he is owning something"),
    (r"\b(?:a|the) real\b", "'really' / 'true' / name the thing"),
    (r"\bwas never\b", "'wasn't' / 'isn't'"),
    (r"\bnot because\b", "give the reason straight: 'because'"),
    (r"\bon purpose\b", "'intentionally' / cut"),
    (r"\brather than\b", "'instead of'"),
    (r"\ba single\b", "'one' / 'a'"),
    (r"\bthe very\b", "'the same' / cut"),
    (r"\bnobody\b", "'no one'"),
    (r"\bin the room\b", "name the place"),
    (r"\bthe part (?:where|that|of|nobody|no one|we|you|i)\b", "say it directly"),
    (r"\bis where\b", "say what happens there"),
    (r"\b(?:a|the|every) man who\b", "'I' / 'we' / 'you' / 'those who', or name the man"),
    (r"\bcarries\b", "'has' / 'holds' / 'bears'"),
    (r"\bthe shape of\b|\bshaped\b", "cut; describe it"),
    (r"\btoward\b", "'towards' / 'to'"),
    (r"\bthe question is\b|\bthe only question\b", "ask the question"),
    (r"\bthis desk\b|\bformation stack\b|\bdoctrine stack\b|\blocked \w+ doctrine\b", "staff shorthand; cut"),
]

# Fail thresholds, set from the 146 posts dated 2007-2024 (which must pass).
# A post fails when a rate is over the line AND the raw count is at least the
# floor, so one stray pair in a 150-word note still passes.
CADENCE_PER_1K = 2.0   # staccato pairs + same-sentence turns + fragment runs + one-line-paragraph runs
CADENCE_FLOOR = 4
AVOID_PER_1K = 4.0     # avoid-list hits ("actually" included)
AVOID_FLOOR = 5
ACTUALLY_PER_1K = 2.5  # "actually" alone
ACTUALLY_FLOOR = 4
MEAN_SENTENCE_MIN = 13.0   # words; his posts average 24, the 2026 drafts 14
MEAN_SENTENCE_FLOOR = 12   # sentences needed before the average is judged

_SKIP_TAGS = {
    "script", "style", "nav", "footer", "blockquote", "figure", "figcaption",
    "table", "aside", "pre", "code", "form", "button", "select", "noscript",
    "svg", "audio", "video", "iframe", "header", "cite",
}
_SKIP_CLASS = re.compile(
    r"(?:^|[\s_-])(?:cta|cta-box|author-bio|post-nav|series-nav|series|byline|meta|"
    r"breadcrumb|sources?|source-card|audio-box|video-box|top-nav|back-link|back|hero|"
    r"article-hero|hero-figure|img-caption|pull|scrip|bte-scrip|credit|kicker|"
    r"series-tag|fn|footnotes?|note|blogger-post-footer|stat-card|badge|post-label|"
    r"category-tag|uiStreamSource|uiStreamPrivacyContainer|talk-box|quest-box)(?:$|[\s_-])"
)
_VOID = {"br", "img", "hr", "meta", "link", "input", "source", "wbr", "area", "col", "embed", "track"}
_INLINE = {"a", "span", "em", "strong", "i", "b", "u", "small", "sup", "sub", "abbr", "mark"}
_BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "div", "section", "ul", "ol", "dd", "dt", "td", "tr"}

from html.parser import HTMLParser  # noqa: E402
import html as _html  # noqa: E402


class _BodyBlocks(HTMLParser):
    """Collect the reader-visible blocks of an article body as (kind, text)."""

    def __init__(self, mode: str):
        super().__init__(convert_charrefs=True)
        self.mode = mode            # "article" | "content" | "all"
        self.active = mode == "all"
        self.root_tag = None
        self.root_bal = 0
        self.skip_tag = None
        self.skip_bal = 0
        self.blocks: list[tuple[str, str]] = []
        self.kind = "p"
        self.buf: list[str] = []

    def _flush(self, next_kind: str = "p"):
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        if text:
            self.blocks.append((self.kind, text))
        self.buf = []
        self.kind = next_kind

    def handle_starttag(self, tag, attrs):
        if tag in _VOID:
            if self.active and not self.skip_tag:
                self.buf.append(" ")
            return
        cls = dict(attrs).get("class") or ""
        if not self.active:
            if (self.mode == "article" and tag == "article") or (
                self.mode == "content" and tag == "div" and re.search(r"(?:^|\s)content(?:$|\s)", cls)
            ):
                self.active, self.root_tag, self.root_bal = True, tag, 1
            return
        if self.root_tag and tag == self.root_tag:
            self.root_bal += 1
        if self.skip_tag:
            if tag == self.skip_tag:
                self.skip_bal += 1
            return
        if tag in _SKIP_TAGS or (cls and tag not in _INLINE and _SKIP_CLASS.search(cls)):
            self._flush()
            self.skip_tag, self.skip_bal = tag, 1
            return
        if tag in _BLOCK:
            kind = "li" if tag in ("li", "dd", "dt", "td") else ("h" if tag[0] == "h" and len(tag) == 2 else "p")
            self._flush(kind)

    def handle_endtag(self, tag):
        if not self.active or tag in _VOID:
            return
        if self.skip_tag:
            if tag == self.skip_tag:
                self.skip_bal -= 1
                if self.skip_bal == 0:
                    self.skip_tag = None
            if self.root_tag and tag == self.root_tag:
                self.root_bal -= 1
                if self.root_bal == 0:
                    self.active = False
            return
        if self.root_tag and tag == self.root_tag:
            self.root_bal -= 1
            if self.root_bal == 0:
                self._flush()
                self.active = False
                return
        if tag in _BLOCK:
            self._flush()

    def handle_data(self, data):
        if self.active and not self.skip_tag:
            self.buf.append(data)

    def close(self):
        super().close()
        self._flush()


def body_blocks(raw: str, is_html: bool = True) -> list[tuple[str, str]]:
    """Article body as a list of (kind, text); kind is 'p', 'li' or 'h'.

    Quotations set off in <blockquote>, Scripture blocks, pull-quotes, captions,
    bylines, source lists, navigation and call-to-action boxes are left out, so
    that a quoted verse or a chart banner is never counted as the author's cadence.
    """
    if not is_html:
        out = []
        for para in re.split(r"\n\s*\n+", raw):
            t = re.sub(r"\s+", " ", para).strip()
            if not t or t.startswith(">") or t.startswith("|") or t.startswith("```"):
                continue
            kind = "h" if t.startswith("#") else ("li" if re.match(r"(?:[-*+]|\d+\.)\s", t) else "p")
            out.append((kind, re.sub(r"^(?:#+|[-*+]|\d+\.)\s*", "", t)))
        return out
    if re.search(r"<article\b", raw, re.I):
        mode = "article"
    elif re.search(r'<div[^>]*class="(?:[^"]*\s)?content(?:\s[^"]*)?"', raw, re.I):
        mode = "content"
    else:
        mode = "all"
    p = _BodyBlocks(mode)
    try:
        p.feed(raw)
        p.close()
    except Exception:
        return [("p", re.sub(r"\s+", " ", _html.unescape(_strip_html(raw))))]
    return p.blocks


_ABBR = re.compile(
    r"\b(Mr|Mrs|Ms|Dr|St|Sr|Jr|vs|etc|Lt|Col|Sgt|Capt|Gen|Maj|Cpl|Rev|Gov|No|Vol|Gen|Ex|Lev|Num|Deut|Josh|Judg|Sam|Chron|Neh|Ps|Prov|Eccl|Isa|Jer|Lam|Ezek|Dan|Matt|Rom|Cor|Gal|Eph|Phil|Col|Thess|Tim|Heb|Jas|Pet|Rev|cf|ch|vv|v|pp|p|ca|approx|Inc|Co|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.",
)
_WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’\-]*")
_SPLIT = re.compile(r"(?<=[.!?])[\"”’')\]]*\s+(?=[\"“‘'(\[]*[A-Z0-9])")


def sentences(text: str) -> list[str]:
    t = re.sub(r"^\s*(?:\d{1,2}[.)]|[A-Za-z][.)])\s+", "", text)       # list markers
    t = re.sub(r"\.{2,}|…", "\u2026", t)                               # ellipsis is a pause, not a stop
    t = re.sub(r"\b(e\.g|i\.e|a\.m|p\.m|U\.S|U\.S\.M\.C|Ph\.D|Th\.D|D\.Min|M\.Div)\.", lambda m: m.group(1).replace(".", "\u00b7") + "\u00b7", t)
    t = _ABBR.sub(lambda m: m.group(1) + "\u00b7", t)
    t = re.sub(r"\b([A-Z])\.(?=\s*[A-Z])", "\\1\u00b7", t)              # initials: C.R. Wiley, M. R. Covey
    return [s.strip() for s in _SPLIT.split(t) if _WORD.search(s)]


def _nwords(s: str) -> int:
    return len(_WORD.findall(s))


_NEG = re.compile(r"\b(?:not|never|no|nor|neither|cannot)\b|n['’]t\b", re.I)
_NEG_START = re.compile(r"^[\"“‘'(]*(?:not|no|never|nor|neither)\b", re.I)
_TURN = re.compile(
    r"\b(?:(?:is|are|was|were|am|does|do|did)\s+not|(?:is|are|was|were|does|do|did)n['’]t|(?:it|that|this|he|she|they|we)['’](?:s|re)\s+not)\b"
    r"[^.;:!?]{1,70}?(?:[;:\u2014\u2013]|\s-\s|,)\s*"
    r"(?:it|that|this|he|she|they|we|you)(?:\s+(?:is|are|was|were)\b|['’](?:s|re)\b)",
    re.I,
)


def _first_word(s: str) -> str:
    m = _WORD.search(s)
    return m.group(0).lower() if m else ""


_PRON_START = re.compile(r"^[\"“‘'(]*(?:it|that|this|he|she|they|these|those|we|you|i)\b", re.I)


def is_staccato_pair(a: str, b: str) -> bool:
    """'That is not X. That is Y.' / 'Not X. Y.' / 'X. Not Y.' in two short sentences."""
    wa, wb = _nwords(a), _nwords(b)
    if wa > 10 or wb > 10 or a.endswith("?"):
        return False
    if _NEG_START.search(a) and wa <= 6:                       # Not a factory. A vine.
        return True
    if _NEG_START.search(b) and wb <= 6:                       # Five recoveries. Not five men.
        return True
    same = _first_word(a) == _first_word(b)
    if bool(_NEG.search(a)) != bool(_NEG.search(b)) and (same or _PRON_START.search(b)):
        return True                                            # That is not courage. That is laziness. / An era explains a sin. It does not justify it.
    if wa <= 5 and wb <= 5 and same:
        return True                                            # One is a shadow. One is the light.
    return False


_REF_LEAD = re.compile(r"^(?:[1-3]\s)?[A-Z][a-z]+(?:\s[A-Z][a-z]+)?\s\d+:\d+[\d:,\-–\s]*(?:\([A-Z]+\))?\s*[:.]?\s*[\"“]")


def _is_quotation(text: str) -> bool:
    """A paragraph that is a Scripture reference plus its text, or mostly inside quotation marks."""
    if _REF_LEAD.search(text):
        return True
    quoted = sum(len(m) for m in re.findall(r"“[^”]{40,}”|\"[^\"]{40,}\"", text))
    return quoted >= 0.6 * len(text)


@dataclass
class Cadence:
    file: str
    words: int = 0
    pairs: int = 0          # staccato pairs across two sentences
    turns: int = 0          # "is not X; it is Y" inside one sentence
    frag_runs: int = 0      # runs of 2+ sentences of four words or fewer
    para_runs: int = 0      # runs of 2+ one-sentence paragraphs of ten words or fewer, each a full stop
    actually: int = 0
    avoid: int = 0
    nsent: int = 0
    avoid_hits: tuple = ()
    examples: tuple = ()

    @property
    def cadence(self) -> int:
        return self.pairs + self.turns + self.frag_runs + self.para_runs

    def per_1k(self, n: int) -> float:
        return 1000.0 * n / self.words if self.words else 0.0

    @property
    def mean_sentence(self) -> float:
        return self.words / self.nsent if self.nsent else 0.0

    def reasons(self) -> list[str]:
        out = []
        if self.cadence >= CADENCE_FLOOR and self.per_1k(self.cadence) > CADENCE_PER_1K:
            out.append(f"cadence {self.per_1k(self.cadence):.1f}/1k > {CADENCE_PER_1K}")
        if self.actually >= ACTUALLY_FLOOR and self.per_1k(self.actually) > ACTUALLY_PER_1K:
            out.append(f"'actually' x{self.actually}")
        if self.avoid >= AVOID_FLOOR and self.per_1k(self.avoid) > AVOID_PER_1K:
            out.append(f"avoid-list {self.per_1k(self.avoid):.1f}/1k > {AVOID_PER_1K}")
        if self.nsent >= MEAN_SENTENCE_FLOOR and self.mean_sentence < MEAN_SENTENCE_MIN:
            out.append(f"mean sentence {self.mean_sentence:.1f} words < {MEAN_SENTENCE_MIN}")
        return out

    @property
    def passed(self) -> bool:
        return not self.reasons()

    def line(self) -> str:
        verdict = "PASS" if self.passed else "FAIL"
        why = "" if self.passed else "  [" + "; ".join(self.reasons()) + "]"
        return (
            f"{verdict}  {os.path.basename(self.file)}  words={self.words} "
            f"pairs={self.pairs} turns={self.turns} frag-runs={self.frag_runs} para-runs={self.para_runs} "
            f"cadence/1k={self.per_1k(self.cadence):.1f} mean-sentence={self.mean_sentence:.1f} "
            f"actually={self.actually} avoid={self.avoid} ({self.per_1k(self.avoid):.1f}/1k){why}"
        )


def cadence_of(path: str, raw: str | None = None) -> Cadence:
    if raw is None:
        raw = Path(path).read_text(encoding="utf-8", errors="replace")
    is_html = path.lower().endswith((".html", ".htm"))
    blocks = [(k, t) for k, t in body_blocks(raw, is_html) if k != "h" and not _is_quotation(t)]
    c = Cadence(file=path)
    ex: list[str] = []
    prev_single: str | None = None      # previous block, if it was a one-sentence paragraph
    short_run = 0
    for kind, text in blocks:
        sents = sentences(text)
        c.words += _nwords(text)
        c.nsent += len(sents)
        # staccato pairs inside the block, and across two one-sentence paragraphs
        seq = ([prev_single] if (prev_single and kind == "p" and len(sents) == 1) else []) + sents
        for a, b in zip(seq, seq[1:]):
            if is_staccato_pair(a, b):
                c.pairs += 1
                ex.append(f"pair: {a} {b}")
        for m in _TURN.finditer(text):
            c.turns += 1
            ex.append("turn: " + text[max(0, m.start() - 20): m.end() + 30])
        # fragment runs inside the block
        run = 0
        for s in sents + [""]:
            if s and _nwords(s) <= 4:
                run += 1
                continue
            if run >= 2:
                c.frag_runs += 1
                i = sents.index(s) if s else len(sents)
                ex.append("fragments: " + " ".join(sents[i - run: i]))
            run = 0
        # one-sentence short paragraphs in sequence
        if kind == "p" and len(sents) == 1 and _nwords(text) <= 10 and re.search(r"[.!?][\"”’)]*$", text):
            short_run += 1
            if short_run == 2:
                c.para_runs += 1
                ex.append("one-line paragraphs: … " + text)
        else:
            short_run = 0
        prev_single = sents[0] if (kind == "p" and len(sents) == 1) else None
        for pat, _fix in AVOID:
            hits = re.findall(pat, text, flags=re.I)
            if hits:
                c.avoid += len(hits)
                c.avoid_hits += tuple(h.lower() if isinstance(h, str) else str(h) for h in hits)
        c.actually += len(re.findall(r"\bactually\b", text, flags=re.I))
    c.examples = tuple(ex)
    return c


def scan_file(path: str) -> list[Finding]:
    findings: list[Finding] = []
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except Exception:
        return findings

    # Allow file-level opt-out via comment.
    if "<!-- voice-audit-skip -->" in raw or "# voice-audit-skip" in raw:
        return findings

    # We scan the visible text (HTML stripped). For HTML, this loses line numbers,
    # but the matched-context is searchable in the file. Markdown files we keep raw.
    is_html = path.lower().endswith((".html", ".htm"))
    text = _strip_html(raw) if is_html else raw

    for category, pattern, severity, suggestion in AI_TELLS:
        rgx = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
        for m in rgx.finditer(text):
            findings.append(
                Finding(
                    file=path,
                    line_hint=_line_hint(text, m.start()),
                    category=category,
                    severity=severity,
                    matched=m.group(0),
                    context=_context(text, m.start(), m.end()),
                    suggestion=suggestion,
                )
            )

    # Em-dash overuse check (paragraph-level: 3+ em-dashes per paragraph)
    paragraphs = re.split(r"\n\s*\n+", text)
    for i, p in enumerate(paragraphs):
        em_count = p.count("—") + p.count("&mdash;")
        if em_count >= 3:
            findings.append(
                Finding(
                    file=path,
                    line_hint=0,
                    category="em-dash-overuse",
                    severity="soft",
                    matched=f"{em_count} em-dashes in one paragraph",
                    context=p[:120] + ("..." if len(p) > 120 else ""),
                    suggestion="Vary punctuation; em-dash overuse is an AI tell. Replace some with commas, colons, or sentence breaks.",
                )
            )

    return findings


def scan_path(path: str) -> list[Finding]:
    p = Path(path)
    if p.is_file():
        return scan_file(str(p))
    if p.is_dir():
        out: list[Finding] = []
        for child in sorted(p.rglob("*")):
            if child.is_file() and child.suffix.lower() in (".html", ".htm", ".md", ".markdown"):
                out.extend(scan_file(str(child)))
        return out
    print(f"  ERROR: {path} not found", file=sys.stderr)
    sys.exit(2)


def report_text(findings: list[Finding]) -> int:
    hard = [f for f in findings if f.severity == "hard"]
    soft = [f for f in findings if f.severity == "soft"]
    if not findings:
        print("\n  CLEAN: no AI-tell phrases found.\n")
        return 0
    print(f"\n  HITS: {len(hard)} hard / {len(soft)} soft / {len(findings)} total\n")

    by_file: dict[str, list[Finding]] = {}
    for f in findings:
        by_file.setdefault(f.file, []).append(f)

    for file, ff in by_file.items():
        print(f"\n  === {os.path.basename(file)} ({len(ff)} hits) ===")
        # Group within file by category for readability
        by_cat: dict[str, list[Finding]] = {}
        for f in ff:
            by_cat.setdefault(f.category, []).append(f)
        for cat, cf in by_cat.items():
            print(f"    --- {cat} ({len(cf)}) ---")
            for f in cf:
                mark = "[H]" if f.severity == "hard" else "[S]"
                print(f"    {mark} '{f.matched}' (~ln {f.line_hint})")
                print(f"        ctx: ...{f.context}...")
                print(f"        fix: {f.suggestion}")
    return 1 if hard else 0


def report_markdown(findings: list[Finding]) -> int:
    hard = [f for f in findings if f.severity == "hard"]
    soft = [f for f in findings if f.severity == "soft"]
    print("# Blog Voice Audit\n")
    print(f"**{len(hard)} hard hits** &middot; **{len(soft)} soft hits** &middot; **{len(findings)} total**\n")
    if not findings:
        print("\nNo AI-tell phrases found.\n")
        return 0
    by_file: dict[str, list[Finding]] = {}
    for f in findings:
        by_file.setdefault(f.file, []).append(f)
    for file, ff in sorted(by_file.items()):
        print(f"\n## {os.path.basename(file)} ({len(ff)})\n")
        print("| Severity | Category | Matched | Context | Suggestion |")
        print("|---|---|---|---|---|")
        for f in ff:
            ctx = f.context.replace("|", "&#124;")
            print(f"| {f.severity} | {f.category} | `{f.matched}` | {ctx} | {f.suggestion} |")
    return 1 if hard else 0


def _files(path: str) -> list[str]:
    p = Path(path)
    if p.is_file():
        return [str(p)]
    if p.is_dir():
        return [str(c) for c in sorted(p.rglob("*")) if c.is_file() and c.suffix.lower() in (".html", ".htm", ".md", ".markdown")]
    return []


def cadence_rows(targets: list[str]) -> list[Cadence]:
    rows = []
    for t in targets:
        for f in _files(t):
            try:
                raw = Path(f).read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if "<!-- voice-audit-skip -->" in raw or "# voice-audit-skip" in raw:
                continue
            if 'http-equiv="refresh"' in raw and len(raw) < 2500:
                continue                                    # redirect stub
            rows.append(cadence_of(f, raw))
    return rows


def report_cadence(rows: list[Cadence], markdown: bool, examples: int = 6) -> int:
    fails = [r for r in rows if not r.passed]
    if markdown:
        print("\n## Cadence and Adam's-words check\n")
        print(f"**{len(rows) - len(fails)} pass** &middot; **{len(fails)} fail** &middot; {len(rows)} posts\n")
        print("| Result | Post | Words | Pairs | Turns | Fragment runs | One-line runs | Cadence/1k | Mean sentence | actually | Avoid/1k | Why |")
        print("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for r in rows:
            print(f"| {'PASS' if r.passed else 'FAIL'} | {os.path.basename(r.file)} | {r.words} | {r.pairs} | {r.turns} | {r.frag_runs} | {r.para_runs} | "
                  f"{r.per_1k(r.cadence):.1f} | {r.mean_sentence:.1f} | {r.actually} | {r.per_1k(r.avoid):.1f} | {'; '.join(r.reasons())} |")
        return 1 if fails else 0
    print("\n  CADENCE (staccato pairs, fragment runs, one-line paragraphs, Adam's-words avoid list)")
    for r in rows:
        print("  " + r.line())
        if not r.passed or len(rows) == 1:
            for e in r.examples[:examples]:
                print("        " + e[:150])
            if r.avoid_hits:
                tally: dict[str, int] = {}
                for h in r.avoid_hits:
                    tally[h] = tally.get(h, 0) + 1
                print("        avoid: " + ", ".join(f"{k} x{v}" for k, v in sorted(tally.items(), key=lambda kv: -kv[1])[:12]))
    if len(rows) > 1:
        print(f"\n  CADENCE TOTAL: {len(rows) - len(fails)} pass / {len(fails)} fail / {len(rows)} posts")
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Scan HTML/MD for AI-tell phrases and machine cadence.")
    ap.add_argument("targets", nargs="+", help="Files or directories to scan.")
    ap.add_argument("--markdown", action="store_true", help="Output as Markdown.")
    ap.add_argument("--summary", action="store_true", help="Only the per-post PASS/FAIL lines (no catalog detail).")
    ap.add_argument("--no-cadence", action="store_true", help="Catalog phrases only (the pre-2026-11-17 behaviour).")
    args = ap.parse_args()

    for t in args.targets:
        if not Path(t).exists():
            print(f"  ERROR: {t} not found", file=sys.stderr)
            return 2

    rc = 0
    if not args.summary:
        all_findings: list[Finding] = []
        for t in args.targets:
            all_findings.extend(scan_path(t))
        rc = report_markdown(all_findings) if args.markdown else report_text(all_findings)
    if not args.no_cadence:
        rc = max(rc, report_cadence(cadence_rows(args.targets), args.markdown))
    return rc


if __name__ == "__main__":
    sys.exit(main())
