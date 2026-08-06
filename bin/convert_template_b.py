#!/usr/bin/env python3
"""Convert 'template B' dictionary pages onto the house shell.

201 of the published dictionary entries (data/template-b-entries.txt) came off a
different generator.  Their *content* is fine; the shell around it is foreign --
different CSS, a five-item nav, a left-aligned <h1>, no prev/next, and a
"Biblical Meaning" heading where the rest of the corpus says "Biblical
Definition".  Because ``moop-tools.js`` decides a page is an entry with
``document.querySelector('.word-title')``, template B pages also silently lose
the Copy Definition and Amen buttons.

This script rewrites the PUBLISHED HTML in place.  It deliberately does NOT
regenerate from the batch JSON: ``generate_dict_entries.py`` emits sections
without the ``id="definition"`` / ``"scriptures"`` / ``"corruption"`` anchors
that the live pages carry, and nothing in the repo puts them back (proven
2026-08-06).

Safety properties
-----------------
* **Dry run by default.**  Nothing is written without ``--apply``.
* **Idempotent.**  A page already carrying ``class="word-title"`` is reported as
  ``already-house`` and skipped, so re-running is a no-op.
* **Refuses to lose text.**  Every content payload lifted off the source must
  reappear verbatim in the output, and the output's word multiset must cover the
  source's (minus the headings we intentionally rename).  Any shortfall aborts
  that page with ``TEXT-LOSS`` and leaves it untouched.

The house shell (style block, nav, footer, trailing scripts) is read at runtime
from a reference house page rather than hardcoded, so converted pages cannot
drift from the corpus they are supposed to match.

Usage
-----
    python3 bin/convert_template_b.py amos alien-righteousness      # dry run
    python3 bin/convert_template_b.py --apply amos
    python3 bin/convert_template_b.py --all --apply
"""

from __future__ import annotations

import argparse
import collections
import html as htmllib
import os
import re
import sys
import urllib.parse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = os.path.join(REPO, "docs", "dictionary")
SLUG_LIST = os.path.join(REPO, "data", "dictionary-slugs.txt")
TEMPLATE_B_LIST = os.path.join(REPO, "data", "template-b-entries.txt")
DEFAULT_REFERENCE = "wrath"

# Headings that are intentionally renamed or dropped.  Their words are excluded
# from the word-multiset comparison; everything else must survive.
RENAMED_HEADINGS = [
    "Etymology &amp; Webster 1828",
    "Etymology & Webster 1828",
    "Biblical Meaning",
    "Key Scriptures",
    "Related Entries",
]

SCRIPTURE_REF = re.compile(
    r"^(?:[1-3]\s+)?[A-Z][A-Za-z]+(?:\s+of\s+[A-Z][a-z]+)?\.?\s+\d+(?:[:.]\d+)?"
)


# --------------------------------------------------------------------------- #
# text helpers
# --------------------------------------------------------------------------- #

def visible_text(fragment: str) -> str:
    """Strip tags/scripts and normalise whitespace + entities."""
    fragment = re.sub(r"<(script|style)\b.*?</\1>", " ", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<!--.*?-->", " ", fragment, flags=re.S)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    fragment = htmllib.unescape(fragment)
    fragment = fragment.replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", fragment).strip()


def words(text: str) -> collections.Counter:
    return collections.Counter(re.findall(r"[0-9A-Za-z']+", text))


def esc(text: str) -> str:
    return htmllib.escape(text, quote=True)


# --------------------------------------------------------------------------- #
# house shell, read from a real house page
# --------------------------------------------------------------------------- #

class HouseShell:
    def __init__(self, path: str):
        src = open(path, encoding="utf-8").read()
        if 'class="word-title"' not in src:
            raise SystemExit(f"reference page {path} is not a house page")
        self.style = self._grab(src, r"<style>.*?</style>", "style block")
        self.fonts = self._grab(
            src, r'<link href="https://fonts\.googleapis\.com[^>]*>', "fonts link"
        )
        self.nav = self._grab(src, r"<nav>.*?</nav>", "nav")
        self.footer = self._grab(src, r"<footer>.*?</footer>", "footer")
        # everything between </footer> and </body>: the theme/details scripts
        m = re.search(r"</footer>(.*?)</body>", src, re.S)
        if not m:
            raise SystemExit("could not read trailing scripts from reference page")
        self.scripts = m.group(1).rstrip()

    @staticmethod
    def _grab(src: str, pattern: str, what: str) -> str:
        m = re.search(pattern, src, re.S)
        if not m:
            raise SystemExit(f"could not read {what} from reference page")
        return m.group(0)


# --------------------------------------------------------------------------- #
# neighbours for the prev/next rail
# --------------------------------------------------------------------------- #

class Neighbours:
    def __init__(self):
        slugs = [l.strip() for l in open(SLUG_LIST, encoding="utf-8") if l.strip()]
        self.live = sorted(s for s in slugs if os.path.exists(os.path.join(DICT, s + ".html")))
        self.index = {s: i for i, s in enumerate(self.live)}
        self._titles: dict[str, str] = {}

    def title(self, slug: str) -> str:
        if slug not in self._titles:
            path = os.path.join(DICT, slug + ".html")
            text = ""
            try:
                page = open(path, encoding="utf-8").read()
                m = re.search(r'<div class="word-title">(.*?)</div>', page, re.S) or re.search(
                    r"<h1[^>]*>(.*?)</h1>", page, re.S
                )
                if m:
                    text = visible_text(m.group(1))
            except OSError:
                pass
            self._titles[slug] = text or slug.replace("-", " ").title()
        return self._titles[slug]

    def around(self, slug: str):
        i = self.index.get(slug)
        if i is None:
            return None, None
        prev = self.live[i - 1] if i > 0 else None
        nxt = self.live[i + 1] if i + 1 < len(self.live) else None
        return prev, nxt


# --------------------------------------------------------------------------- #
# parsing a template B page
# --------------------------------------------------------------------------- #

class ParseError(Exception):
    pass


def parse_template_b(src: str) -> dict:
    def need(pattern, what, flags=re.S):
        m = re.search(pattern, src, flags)
        if not m:
            raise ParseError(f"missing {what}")
        return m

    data = {}
    data["word"] = visible_text(need(r"<h1>(.*?)</h1>", "<h1> title").group(1))
    m = re.search(r'<div class="pron">(.*?)</div>', src, re.S)
    data["pron"] = visible_text(m.group(1)) if m else ""
    m = re.search(r'<div class="pos">(.*?)</div>', src, re.S)
    data["pos"] = visible_text(m.group(1)) if m else ""

    card = need(r'<div class="card">(.*?)</div>', "etymology card").group(1)
    em = re.search(r"<p>(.*?)</p>", card, re.S)
    if not em:
        raise ParseError("missing etymology paragraph")
    data["etymology"] = em.group(1).strip()

    defn = need(r"<h2>Biblical Meaning</h2>(.*?)<h2>", "Biblical Meaning block").group(1)
    dm = re.search(r"<p>(.*?)</p>", defn, re.S)
    if not dm:
        raise ParseError("missing Biblical Meaning paragraph")
    data["definition"] = dm.group(1).strip()

    scripts_block = need(
        r"<h2>Key Scriptures</h2>(.*?)<h2>", "Key Scriptures block"
    ).group(1)
    scriptures = []
    for sm in re.finditer(
        r'<div class="scripture">(.*?)<span class="ref">(.*?)</span>\s*</div>',
        scripts_block,
        re.S,
    ):
        quote = sm.group(1).strip()
        ref = re.sub(r"^[—–-]\s*", "", visible_text(sm.group(2))).strip()
        scriptures.append((quote, ref))
    if not scriptures:
        raise ParseError("no scripture blocks parsed")
    data["scriptures"] = scriptures

    rel = need(
        r'<h2>Related Entries</h2>\s*<div class="related">(.*?)</div>', "Related Entries"
    ).group(1)
    related = []
    for token in re.split(r"(<a\b.*?</a>)", rel, flags=re.S):
        if not token or not token.strip():
            continue
        am = re.match(r'<a href="([^"]+)"[^>]*>(.*?)</a>', token, re.S)
        if am:
            related.append(("link", am.group(1), visible_text(am.group(2))))
        else:
            for chunk in re.split(r"(?<=[a-z\)])(?=[A-Z])", visible_text(token)):
                chunk = chunk.strip()
                if chunk:
                    related.append(("plain", None, chunk))
    data["related"] = related

    m = re.search(r"(<!-- IN-THE-TEXT-START -->.*?<!-- IN-THE-TEXT-END -->)", src, re.S)
    data["in_the_text"] = m.group(1) if m else ""

    # head fragments worth carrying across untouched
    data["canonical"] = _opt(src, r'<link rel="canonical"[^>]*>')
    data["ldjson"] = _opt(src, r'<script type="application/ld\+json">.*?</script>')
    data["description"] = _opt(src, r'<meta name="description"[^>]*>')
    og = re.findall(r'<meta (?:property="og:|name="twitter:)[^>]*>', src)
    data["og"] = og
    return data


def _opt(src: str, pattern: str) -> str:
    m = re.search(pattern, src, re.S)
    return m.group(0) if m else ""


# --------------------------------------------------------------------------- #
# rendering the house page
# --------------------------------------------------------------------------- #

def scripture_link(ref: str) -> str:
    if not SCRIPTURE_REF.match(ref):
        return f"<strong>{esc(ref)}</strong>"
    q = urllib.parse.quote(ref, safe=":,").replace("%20", "+")
    return f'<a href="../bible.html?ref={q}" class="verse-ref">{esc(ref)}</a>'


def render(data: dict, slug: str, shell: HouseShell, neigh: Neighbours) -> str:
    word = data["word"]
    prev, nxt = neigh.around(slug)
    rail = []
    if prev:
        rail.append(f'<a href="{prev}.html">&#8592; {esc(neigh.title(prev))}</a>')
    rail.append(
        '<div class="dict-back-center"><a href="index.html">&#8592; Back to Dictionary</a></div>'
    )
    if nxt:
        rail.append(f'<a href="{nxt}.html">{esc(neigh.title(nxt))} &#8594;</a>')

    head = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '    <meta charset="UTF-8">',
    ]
    if data["canonical"]:
        head.append("    " + data["canonical"])
    head.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    head.append(f"    <title>{esc(word)} &mdash; The MOOP Dictionary</title>")
    if data["ldjson"]:
        head.append("    " + data["ldjson"])
    head.append("    " + shell.style)
    head.append("    " + shell.fonts)
    head.append("    <!-- Open Graph / Twitter (auto-generated) -->")
    if data["description"]:
        head.append("    " + data["description"])
    for tag in data["og"]:
        head.append("    " + tag)
    head.append('    <link rel="stylesheet" href="/assets/css/light-icons.css">')
    head.append('    <link rel="stylesheet" href="/assets/css/print.css" media="print">')
    head.append("</head>")

    body = [
        "<body>",
        "    " + shell.nav,
        '    <div class="container">',
        '        <div class="dict-back-nav">' + "".join(rail) + "</div>",
        '        <div class="word-header">',
        f'            <div class="word-title">{esc(word)}</div>',
    ]
    if data["pron"]:
        body.append(f'            <div class="pronunciation">{esc(data["pron"])}</div>')
    if data["pos"]:
        body.append(f'            <span class="pos">{esc(data["pos"])}</span>')
    body.append(f'            <div class="etymology">{data["etymology"]}</div>')
    body.append("        </div>")
    body.append("")

    body.append('        <div class="section" id="definition">')
    body.append(
        '            <h3><img src="../assets/icons/shield-open-book-24.png" alt="" width="20" '
        'height="20" style="vertical-align:middle;margin-right:6px;">Biblical Definition</h3>'
    )
    body.append('            <div class="biblical-def">')
    body.append(f'                <p>{data["definition"]}</p>')
    body.append("            </div>")
    body.append("        </div>")
    body.append("")

    body.append('        <div class="section" id="scriptures">')
    body.append(
        '            <h3><img src="../assets/icons/shield-bible-cross-24.png" alt="" width="20" '
        'height="20" style="vertical-align:middle;margin-right:6px;">Key Scripture</h3>'
    )
    for quote, ref in data["scriptures"]:
        body.append(f"            <p>{scripture_link(ref)} &mdash; {quote}</p>")
    body.append("        </div>")
    body.append("")

    if data["in_the_text"]:
        for line in data["in_the_text"].splitlines():
            body.append("        " + line.strip() if line.strip() else "")
        body.append("")

    body.append('        <div class="section" id="related">')
    body.append("            <h3>Related Words</h3>")
    body.append('            <div class="related">')
    for kind, href, label in data["related"]:
        if kind == "link":
            body.append(f'                <a href="{href}">{esc(label)}</a>')
        else:
            body.append(
                '                <span style="border:1px solid var(--border);padding:6px 14px;'
                'border-radius:20px;color:var(--gray);font-size:0.85rem;">'
                f"{esc(label)}</span>"
            )
    body.append("            </div>")
    body.append("        </div>")
    body.append("    </div>")
    body.append("")
    body.append("    " + shell.footer)
    body.append(shell.scripts)
    body.append("</body>")
    body.append("</html>")
    return "\n".join(head + body) + "\n"


# --------------------------------------------------------------------------- #
# the no-text-loss guard
# --------------------------------------------------------------------------- #

def content_region(page: str) -> str:
    """The part of the page a reader reads -- nav/footer boilerplate excluded."""
    m = re.search(r"<body>(.*?)</body>", page, re.S)
    region = m.group(1) if m else page
    # nav and footer are boilerplate and are *supposed* to change shape here
    for chunk in (r"<nav\b.*?</nav>", r"<footer\b.*?</footer>"):
        region = re.sub(chunk, " ", region, flags=re.S)
    return region


def check_no_loss(before: str, after: str, data: dict) -> list[str]:
    """Return a list of complaints; empty means nothing was lost."""
    problems = []
    src_text = visible_text(content_region(before))
    out_text = visible_text(content_region(after))

    # 1. every content payload must survive verbatim
    payloads = [("title", data["word"]), ("etymology", visible_text(data["etymology"])),
                ("definition", visible_text(data["definition"]))]
    if data["pron"]:
        payloads.append(("pronunciation", data["pron"]))
    if data["pos"]:
        payloads.append(("part of speech", data["pos"]))
    for i, (quote, ref) in enumerate(data["scriptures"]):
        payloads.append((f"scripture {i + 1} quote", visible_text(quote)))
        payloads.append((f"scripture {i + 1} ref", ref))
    for kind, _href, label in data["related"]:
        payloads.append((f"related ({kind})", label))
    for what, payload in payloads:
        if payload and payload not in out_text:
            problems.append(f"{what} missing from output: {payload[:70]!r}")

    # 2. word-level sweep, ignoring the headings we deliberately rename
    src_words = words(src_text)
    for heading in RENAMED_HEADINGS:
        src_words.subtract(words(visible_text(heading)))
    out_words = words(out_text)
    dropped = {w: c for w, c in (src_words - out_words).items() if c > 0}
    # Template B runs adjacent unlinked "Related Entries" together with no
    # separator ("Biblical MasculinityModern Manhood"), so the source tokenises
    # as one glued word where the converted page correctly has two.  That is a
    # gain, not a loss -- exempt it, but only for genuinely glued tokens whose
    # letters all survive, so a real deletion still trips the guard.
    if dropped:
        out_nospace = re.sub(r"\s+", "", out_text)
        dropped = {
            w: c for w, c in dropped.items()
            if not (re.search(r"[a-z)][A-Z]", w) and w in out_nospace)
        }
    if dropped:
        sample = ", ".join(f"{w}x{c}" for w, c in sorted(dropped.items())[:12])
        problems.append(f"{sum(dropped.values())} word(s) dropped: {sample}")
    return problems


# --------------------------------------------------------------------------- #
# driver
# --------------------------------------------------------------------------- #

def convert(slug: str, shell: HouseShell, neigh: Neighbours, apply: bool) -> str:
    path = os.path.join(DICT, slug + ".html")
    if not os.path.exists(path):
        print(f"  MISSING     {slug}: no such page")
        return "missing"
    src = open(path, encoding="utf-8").read()

    if 'class="word-title"' in src or "Biblical Definition" in src:
        print(f"  already-house {slug}")
        return "already-house"
    if "Biblical Meaning" not in src:
        print(f"  SKIP        {slug}: neither marker present, not template B")
        return "not-template-b"

    try:
        data = parse_template_b(src)
    except ParseError as exc:
        print(f"  PARSE-FAIL  {slug}: {exc}")
        return "parse-fail"

    out = render(data, slug, shell, neigh)
    problems = check_no_loss(src, out, data)
    if problems:
        print(f"  TEXT-LOSS   {slug}: refusing to write")
        for p in problems:
            print(f"                - {p}")
        return "text-loss"

    notes = []
    if re.search(r"webster", visible_text(data["etymology"]), re.I):
        notes.append("etymology mentions Webster - review whether it should be split out")
    prev, nxt = neigh.around(slug)
    if not prev or not nxt:
        notes.append("at the edge of the corpus; prev/next incomplete")

    if apply:
        open(path, "w", encoding="utf-8").write(out)
        verb = "converted  "
    else:
        verb = "would convert"
    print(f"  {verb} {slug}  ({len(data['scriptures'])} scriptures, "
          f"{len(data['related'])} related, in-the-text={'yes' if data['in_the_text'] else 'no'})")
    for n in notes:
        print(f"                note: {n}")
    return "converted" if apply else "would-convert"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slugs", nargs="*", help="entry slugs to convert")
    ap.add_argument("--all", action="store_true",
                    help="convert every slug in data/template-b-entries.txt")
    ap.add_argument("--apply", action="store_true",
                    help="actually write files (default is a dry run)")
    ap.add_argument("--reference", default=DEFAULT_REFERENCE,
                    help=f"house page to take the shell from (default: {DEFAULT_REFERENCE})")
    args = ap.parse_args()

    slugs = list(args.slugs)
    if args.all:
        slugs += [l.strip() for l in open(TEMPLATE_B_LIST, encoding="utf-8") if l.strip()]
    if not slugs:
        ap.error("give at least one slug, or --all")

    shell = HouseShell(os.path.join(DICT, args.reference + ".html"))
    neigh = Neighbours()

    mode = "APPLY" if args.apply else "DRY RUN (no files written; pass --apply to write)"
    print(f"convert_template_b -- {mode}")
    print(f"house shell from: {args.reference}.html\n")

    tally = collections.Counter()
    for slug in dict.fromkeys(slugs):
        tally[convert(slug, shell, neigh, args.apply)] += 1

    print("\nsummary: " + ", ".join(f"{k}={v}" for k, v in sorted(tally.items())))
    bad = tally["text-loss"] + tally["parse-fail"] + tally["missing"]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
