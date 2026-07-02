#!/usr/bin/env python3
"""
Remove dead/orphan theme-toggle markup from standard-template lexicon pages,
leaving ONLY the redesign's nav slider (.nav-theme-toggle) + the load-time
script. Targets: old non-nav .bte-theme-toggle buttons (anywhere), legacy
centered wrappers, orphan emoji/entity spans, and the stray </div> debris
between </nav> and the content container. DOM-balance asserted per page.

Usage: python3 clean_lexicon_debris.py [--apply] [file ...]
  no files  -> all standard-template lexicon pages
  --apply   -> write (default dry-run)
"""
import glob, re, sys

APPLY = "--apply" in sys.argv
argfiles = [a for a in sys.argv[1:] if not a.startswith("--")]

EMOJI_SPAN = re.compile(r'<span style="width:18px;text-align:center;">[^<]{0,24}</span>')
# empty centered wrapper left after removing the old button (margin:…auto, margin:10px 0 0, etc.)
LEGACY_WRAP_EMPTY = re.compile(r'<div style="[^"]*text-align:center[^"]*">\s*</div>')
DIV_TOK = re.compile(r'<div\b[^>]*>|</div>')
OLD_BTN_OPEN = re.compile(r'<div class="bte-theme-toggle"(?![^>]*nav-theme-toggle)[^>]*>')

def find_div_end(s, start):
    depth = 0
    for m in DIV_TOK.finditer(s, start):
        if m.group().startswith("</div"):
            depth -= 1
            if depth == 0:
                return m.end()
        else:
            depth += 1
    return -1

def body_div_balance(s):
    b = s[s.find("<body"):s.rfind("</body>")]
    return len(re.findall(r"<div\b", b)) - len(re.findall(r"</div>", b))

def emoji_only(txt):
    # the inner content removed must be only sun/moon emoji or entities — never real words
    return re.fullmatch(r'(?:\s|☀️|☀|🌙|🌑|🌕|\U0001F319|&#9728;|&#65039;|&#127769;)*', txt) is not None

def clean(path):
    s = open(path, encoding="utf-8").read()
    orig = s
    bal_before = body_div_balance(s)

    # 1) Remove every old non-nav .bte-theme-toggle button (matched divs; handles nested dot)
    removed_btns = 0
    while True:
        m = OLD_BTN_OPEN.search(s)
        if not m: break
        end = find_div_end(s, m.start())
        assert end != -1, f"{path}: unbalanced old button div"
        inner = s[m.end():end-6]  # between > and </div>
        # safety: an old button only contains spans/divs with emoji — no prose
        txt = re.sub(r"<[^>]+>", "", inner)
        assert emoji_only(txt), f"{path}: old button had unexpected text {txt!r}"
        s = s[:m.start()] + s[end:]
        removed_btns += 1
        assert removed_btns < 10, f"{path}: too many old buttons"

    # 2) Remove orphan emoji/entity spans (now bare), verifying they hold only emoji
    def _span_sub(mm):
        txt = re.sub(r"<[^>]+>", "", mm.group(0))
        assert emoji_only(txt) or txt in ("☀️","🌙"), f"{path}: emoji-span had text {txt!r}"
        return ""
    s = EMOJI_SPAN.sub(_span_sub, s)

    # 3) Remove now-empty legacy centered wrappers
    s = LEGACY_WRAP_EMPTY.sub("", s)

    # Steps 1-3 above are balance-neutral (matched divs / inline spans). The visible
    # orphan glyphs + duplicate toggles are now gone regardless of div structure.
    bal_mid = body_div_balance(s)

    # 4) Try to also remove leftover stray </div> + whitespace between </nav> and the
    #    content container — but ONLY if doing so yields a fully balanced page. Pages
    #    with compensating errors elsewhere (e.g. G3056) keep their div structure.
    repaired_divs = False
    m = re.search(r'</nav>(.*?)<div class="container">', s, re.S)
    if m and re.fullmatch(r'(?:\s|</div>)*', m.group(1)):
        cand = s[:m.start()] + '</nav>\n    <div class="container">' + s[m.end():]
        if body_div_balance(cand) == 0:
            s = cand
            repaired_divs = True

    # ---- assertions ----
    assert 'nav-theme-toggle' in s, f"{path}: nav slider lost"
    assert OLD_BTN_OPEN.search(s) is None, f"{path}: an old button survived"
    assert EMOJI_SPAN.search(s) is None, f"{path}: an emoji span survived"
    bal_after = body_div_balance(s)
    # never make balance worse than it already was
    assert abs(bal_after) <= abs(bal_before), f"{path}: balance worsened {bal_before}->{bal_after}"
    assert ('word-header' in s or 'class="container"' in s), f"{path}: content container missing"
    return s, orig, removed_btns, bal_before, repaired_divs

files = argfiles if argfiles else [f for f in glob.glob("docs/lexicon/*.html")
                                    if "<nav>" in open(f, encoding="utf-8").read()]
files.sort()
changed = 0; div_repaired = 0; total_btns = 0; skipped = 0; partial = 0
to_write = {}
for f in files:
    s, orig, nb, bb, rep = clean(f)
    if s != orig:
        to_write[f] = s; changed += 1; total_btns += nb
        if rep: div_repaired += 1
        elif bb != 0: partial += 1   # visible junk removed but div structure left (compensating errors)
    else:
        skipped += 1
print(f"files scanned: {len(files)} | changed: {changed} | unchanged: {skipped}")
print(f"old buttons removed: {total_btns} | div-structure repaired: {div_repaired} | "
      f"glyph-only (divs left, pre-existing imbalance): {partial}")
if APPLY:
    for f, s in to_write.items():
        open(f, "w", encoding="utf-8").write(s)
    print(f"WROTE {len(to_write)} files.")
else:
    print("DRY RUN — re-run with --apply.")
