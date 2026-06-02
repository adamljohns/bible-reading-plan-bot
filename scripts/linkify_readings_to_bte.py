"""Embed BTE links into every chronological daily-reading page.

Each reading page has scripture references like:
    <div class="scripture-ref">📖 Psalm 119:1-8</div>
This wraps the reference text in a link to the Bible Translation Engine:
    <div class="scripture-ref">📖 <a class="bte-ref-link"
        href="/bible.html?ref=Psalm%20119%3A1-8" target="_blank" rel="noopener">Psalm 119:1-8</a></div>

Handles:
  • simple refs, verse ranges, chapter ranges
  • en/em dashes normalized to '-' in the URL (BTE expects hyphen ranges); display keeps original
  • compound refs ("Isaiah 7:14 & Isaiah 11:1-10", "Prov 1:1-7; 31:1-9") — linked whole;
    the BTE's separator-aware ref parser splits them (same as the Read-All widget does)
  • descriptive refs ("Job 11 (selected...)", "Scripture (Genesis 23 — ...)") — the
    scripture portion is extracted; if none is parseable the ref is left as plain text

Idempotent: a div already containing <a> is skipped. A one-line CSS rule is injected
into each page's <style> once.

Usage:
  python3 scripts/linkify_readings_to_bte.py            # all pages
  python3 scripts/linkify_readings_to_bte.py <file>     # one page (for testing)
"""
import html as _html
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINGS = ROOT / "docs" / "readings"

REF_DIV = re.compile(r'(<div class="scripture-ref">)(.*?)(</div>)', re.DOTALL)
EMOJI = "📖"
# A scripture reference: optional leading book number, Book name (1-3 words incl. "of"),
# chapter, optional :verse, optional range end.
SCRIPTURE_RE = re.compile(
    r'((?:[1-3]\s)?[A-Z][a-zA-Z]+(?:\s(?:of\s)?[A-Z][a-zA-Z]+){0,2}\s+\d+(?::\d+)?(?:\s*[-–—]\s*\d+(?::\d+)?)?)'
)
CSS_RULE = (".scripture-ref a.bte-ref-link{color:var(--gold,#D4AF37);text-decoration:none;"
            "border-bottom:1px dotted rgba(212,175,55,.55)}"
            ".scripture-ref a.bte-ref-link:hover{border-bottom-style:solid}")


def url_ref(display_ref: str) -> str | None:
    """From the human display ref, derive the BTE ?ref= value, or None if unparseable."""
    text = _html.unescape(display_ref).strip()          # &amp; -> &, etc.
    text = text.lstrip(EMOJI).strip()
    if "(" in text:
        before = text.split("(", 1)[0].strip()
        if re.search(r"[A-Za-z].*\d", before):
            text = before
        else:
            m = SCRIPTURE_RE.search(text)
            if not m:
                return None
            text = m.group(1).strip()
    # Single-chapter books are valid refs with no chapter number.
    SINGLE_CHAPTER = {"obadiah", "philemon", "jude", "2 john", "3 john"}
    if text.lower() in SINGLE_CHAPTER:
        return text
    # Otherwise a real ref must contain a letter and a digit.
    if not re.search(r"[A-Za-z]", text) or not re.search(r"\d", text):
        return None
    # normalize dashes for the engine's range parser
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"\s*-\s*", "-", text)
    return text


def linkify_div_inner(inner: str) -> str:
    if "<a " in inner or "</a>" in inner:
        return inner  # already linked
    # split optional emoji prefix from the ref text
    m = re.match(r'^(\s*' + re.escape(EMOJI) + r'\s*)(.*)$', inner, re.DOTALL)
    prefix, ref_disp = (m.group(1), m.group(2)) if m else ("", inner)
    ref_disp_stripped = ref_disp.strip()
    if not ref_disp_stripped:
        return inner
    target = url_ref(ref_disp_stripped)
    if not target:
        return inner  # leave descriptive/non-parseable refs as plain text
    href = "/bible.html?ref=" + urllib.parse.quote(target, safe="")
    link = ('<a class="bte-ref-link" href="' + href + '" target="_blank" rel="noopener">'
            + ref_disp_stripped + '</a>')
    # preserve any trailing whitespace structure
    return prefix + link


def process(path: Path) -> tuple[int, bool]:
    text = path.read_text(encoding="utf-8")
    n_links = [0]

    def repl(mobj):
        inner_new = linkify_div_inner(mobj.group(2))
        if inner_new != mobj.group(2):
            n_links[0] += 1
        return mobj.group(1) + inner_new + mobj.group(3)

    new_text = REF_DIV.sub(repl, text)
    css_injected = False
    if n_links[0] and "bte-ref-link" in new_text and CSS_RULE not in new_text:
        # inject the CSS rule once, just before the first </style>
        idx = new_text.find("</style>")
        if idx != -1:
            new_text = new_text[:idx] + CSS_RULE + "\n" + new_text[idx:]
            css_injected = True
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return n_links[0], css_injected


def main():
    args = sys.argv[1:]
    files = [Path(args[0])] if args else sorted(READINGS.glob("20*.html"))
    total_links, total_pages, css_pages = 0, 0, 0
    for f in files:
        links, css = process(f)
        if links:
            total_pages += 1
            total_links += links
        if css:
            css_pages += 1
    print(f"Pages updated: {total_pages}/{len(files)} | links added: {total_links} | css injected: {css_pages}")


if __name__ == "__main__":
    main()
