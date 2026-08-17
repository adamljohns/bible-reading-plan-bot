#!/usr/bin/env python3
"""Audit (and with --apply, repair) scripture quote blocks on the LIVE
dictionary pages against docs/assets/verse-cache.json.

The batch JSONs are the source of truth for entry content, but pages drift:
the 8/06 AV restoration patched pages by exact-substring and logged misses,
enhancement passes rewrite page HTML after generation, and the oldest entries
predate the batch system entirely. This tool audits what visitors actually
read. Quote blocks are the uniform generator markup:

    <p><a href="../bible.html?ref=..." class="verse-ref">REF</a> &mdash;
    <em>"QUOTE"</em></p>

A quote passes if every ellipsis-separated fragment appears in order in the
punctuation-stripped AV cache text (same standard as repair_kjv_quotes.py).
Failures are re-quoted from the cache: elisions rebuilt verbatim span-by-span,
paraphrases replaced with the cited verse's full (clause-clipped) text.

Usage:
  python3 bin/audit_page_quotes.py            # report only
  python3 bin/audit_page_quotes.py --apply    # rewrite failing quotes
"""
import glob, html, importlib.util, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _load(name):
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(ROOT, f'bin/{name}.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

V = _load('verify_kjv_quotes')
R = _load('repair_kjv_quotes')

QUOTE_RE = re.compile(
    r'(<a href="\.\./bible\.html\?ref=[^"]*" class="verse-ref">([^<]+)</a>'
    r'\s*&mdash;\s*<em>)(.*?)(</em>)', re.S)

# The generational-decoder pages carry a second quote shape: a "Scripture
# says:" reframe box whose italic quote paragraph is followed by an
# attribution anchor ("&mdash; Matthew 11:28-30"). The Gen-Z box shares the
# same paragraph styling but has no verse-ref anchor after it, so requiring
# the attribution keeps this from ever touching the slang side.
REFRAME_RE = re.compile(
    r'(<p style="[^"]*font-style:italic;">&ldquo;)(.*?)(&rdquo;</p>\s*'
    r'<p style="[^"]*"><a href="\.\./bible\.html\?ref=[^"]*" '
    r'class="verse-ref">&mdash;\s*([^<]+)</a>)', re.S)

# Prose-embedded quotes: an editorial sentence quoting scripture inline with
# a parenthesized ref — '"For by grace you have been saved" (Eph 2:8-9)'.
# Three delimiter conventions exist in the corpus. A quote under 8 words is
# woven into the sentence's own grammar, so it is only ever repaired when its
# words locate verbatim in the AV — never replaced with a whole verse.
_REFPAT = r'((?:cf\.\s*|see\s+)?)((?:[1-3]\s?)?[A-Za-z][A-Za-z.\s]{1,22}?\s?\d+:\d+(?:[-–]\d+)?)'
_ANCHOR = r'(<a href="\.\./bible\.html\?ref=[^"]*" class="verse-ref">[^<]+</a>)'
# kind 'text': paren ref is plain text (groups: quote, cf-prefix, ref).
# kind 'anchor': paren ref is a verse-ref anchor (groups: quote, anchor-html).
PROSE_RES = [
    (re.compile(r'&ldquo;([^&]{15,400}?)&rdquo;\s*\(' + _REFPAT + r'\)'), '&ldquo;', '&rdquo;', 'text'),
    (re.compile(r'"([^"<>]{15,400})"\s*\(' + _REFPAT + r'\)'), '"', '"', 'text'),
    (re.compile(r'“([^”<>]{15,400})”\s*\(' + _REFPAT + r'\)'), '“', '”', 'text'),
    (re.compile(r'&ldquo;([^&]{8,400}?)&rdquo;\s*\(' + _ANCHOR + r'\)'), '&ldquo;', '&rdquo;', 'anchor'),
    (re.compile(r'"([^"<>]{8,400})"\s*\(' + _ANCHOR + r'\)'), '"', '"', 'anchor'),
]

# Oldest Key Scripture format: bullet line with straight quotes, no <em>.
BULLET_RE = re.compile(
    r'(<a href="\.\./bible\.html\?ref=[^"]*" class="verse-ref">([^<]+)</a>'
    r'\s*&mdash;\s*")([^"<]{10,600})(")')

def unwrap(emtext):
    """The em content minus its outer typographic quotes."""
    t = html.unescape(emtext).strip()
    return t.strip('"“”‘’\'')

def main():
    apply_ = '--apply' in sys.argv
    review_out = None
    if '--review' in sys.argv:
        review_out = sys.argv[sys.argv.index('--review') + 1]
    cache = json.load(open(os.path.join(ROOT, 'docs/assets/verse-cache.json')))
    ok = fixed = prose_ok = prose_fixed = 0
    skipped, uncached, unfixable, prose_manual = [], [], [], []
    samples, prose_samples = [], []
    pages_touched = 0

    for page in sorted(glob.glob(os.path.join(ROOT, 'docs/dictionary/*.html'))):
        name = os.path.basename(page)
        if name == 'manifest.html':
            continue
        h = open(page, encoding='utf-8').read()
        out, changed = h, False
        blocks = [(m, m.group(2), m.group(3), m.group(1), m.group(4), '"%s"')
                  for m in QUOTE_RE.finditer(h)]
        blocks += [(m, m.group(4), m.group(2), m.group(1), m.group(3), '%s')
                   for m in REFRAME_RE.finditer(h)]
        blocks += [(m, m.group(2), m.group(3), m.group(1), m.group(4), '%s')
                   for m in BULLET_RE.finditer(h)]
        for m, ref, body, prefix, suffix, wrap in blocks:
            ref = ref.strip()
            if 'title' in ref:
                continue
            parsed = V.parse_ref(ref)
            if not parsed:
                skipped.append((name, ref))
                continue
            kjv_raw = V.cache_text(cache, *parsed)
            if not kjv_raw:
                uncached.append((name, ref))
                continue
            quote = unwrap(body)
            if not quote:
                continue
            if R.hard_ordered(quote, kjv_raw):
                ok += 1
                continue
            new = R.rebuild_elision(quote, kjv_raw) or R.clipped_verse(kjv_raw)
            if not new or not R.hard_ordered(new, kjv_raw):
                unfixable.append((name, ref, quote[:80]))
                continue
            if len(samples) < 10:
                samples.append((name, ref, quote[:76], new[:76]))
            out = out.replace(m.group(0), prefix + (wrap % new) + suffix)
            fixed += 1
            changed = True

        for pat, qopen, qclose, kind in PROSE_RES:
            for m in pat.finditer(h):
                quote = html.unescape(m.group(1))
                if kind == 'anchor':
                    ref = re.sub(r'<[^>]+>', '', m.group(2)).strip()
                    paren = f'({m.group(2)})'
                else:
                    ref = m.group(3).strip()
                    paren = f'({m.group(2)}{m.group(3)})'
                parsed = V.parse_ref(ref)
                if not parsed:
                    continue
                kjv_raw = V.cache_text(cache, *parsed)
                if not kjv_raw:
                    continue
                plain = re.sub(r'<[^>]+>', '', quote)
                if R.hard_ordered(plain, kjv_raw):
                    prose_ok += 1
                    continue
                new = R.rebuild_elision(plain, kjv_raw)
                if not new and len(plain.split()) >= 8:
                    new = R.clipped_verse(kjv_raw)
                if not new or not R.hard_ordered(new, kjv_raw):
                    prose_manual.append((name, ref, plain[:80]))
                    continue
                if len(prose_samples) < 8:
                    prose_samples.append((name, ref, plain[:70], new[:70]))
                out = out.replace(
                    m.group(0), f'{qopen}{new}{qclose} {paren}')
                prose_fixed += 1
                changed = True
        if changed:
            pages_touched += 1
            if apply_:
                open(page, 'w', encoding='utf-8').write(out)

    print(f'quotes OK          : {ok}')
    print(f'FIXED              : {fixed}   (pages touched: {pages_touched})')
    print(f'prose quotes OK    : {prose_ok}')
    print(f'PROSE FIXED        : {prose_fixed}')
    print(f'prose left manual  : {len(prose_manual)}   (phrase woven into grammar; listed below)')
    print(f'non-scripture refs : {len(skipped)}   (left alone)')
    print(f'uncached           : {len(uncached)}')
    print(f'unfixable          : {len(unfixable)}')
    for name, ref, q in prose_manual[:20]:
        print(f'  ~~ {name} | {ref} | {q}')
    if len(prose_manual) > 20:
        print(f'  ~~ ... and {len(prose_manual) - 20} more')
    for name, ref, q in unfixable[:15]:
        print(f'  !! {name} | {ref} | {q}')
    if uncached:
        for name, ref in uncached[:10]:
            print(f'  ?? uncached {name} | {ref}')
    if samples:
        print('\nsamples:')
        for name, ref, before, after in samples:
            print(f'  {name}  {ref}\n     was: {before}\n     now: {after}')
    if prose_samples:
        print('\nprose samples:')
        for name, ref, before, after in prose_samples:
            print(f'  {name}  {ref}\n     was: {before}\n     now: {after}')
    if review_out:
        with open(review_out, 'w') as f:
            f.write('# Prose phrase-quotes needing editorial review — short quoted\n'
                    '# phrases woven into sentence grammar that do not match the AV.\n'
                    '# Two populations: (a) modern-version phrase quotes to re-render\n'
                    '# or version-label, (b) etymology/name-meaning glosses the pattern\n'
                    '# over-captured — skip those.\n')
            for name, ref, q in prose_manual:
                f.write(f'{name} | {ref} | {q}\n')
        print(f'\nwrote {len(prose_manual)} review items -> {review_out}')
    if not apply_:
        print('\n(report only — pass --apply to write)')

if __name__ == '__main__':
    main()
