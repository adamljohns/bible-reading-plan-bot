#!/usr/bin/env python3
"""repair_kjv_quotes.py — replace substantively non-KJV scripture text in batch
JSONs with the verbatim Authorized Version of the reference the author cited.

VOICE-LOCK 5.3 requires the AV verbatim, but 1,156 quotes across the corpus are
modern-version renderings -- 946 of them in batches 400-499, where the guard was
silently skipping everything it could not parse. The reference is the author's
own editorial choice; only the text is wrong. So the repair is deterministic:
fetch that reference from the verse cache and use it.

DELIBERATELY CONSERVATIVE. It repairs only quotes that are:
  * resolvable to a cached KJV verse, and
  * currently FAILING the verifier, and
  * NOT merely cosmetic (punctuation/hyphenation artifacts of normalization),
    since rewriting those changes real text to fix a comparison artifact, and
  * NOT an ellipsis elision -- those are intentional partial quotes, and
    swapping in a whole verse would silently rewrite the author's point.

Every repair is verified against the cache before being written, and the file is
only rewritten if at least one quote in it actually changed.

Usage:
  python3 bin/repair_kjv_quotes.py --dry-run
  python3 bin/repair_kjv_quotes.py --dry-run --range 400 499
  python3 bin/repair_kjv_quotes.py --apply --range 400 499
"""
import json, re, os, glob, html, argparse, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'docs/assets/verse-cache.json')
BATCHES = os.path.join(ROOT, 'data/dictionary-batches')

_spec = importlib.util.spec_from_file_location(
    'v', os.path.join(ROOT, 'bin/verify_kjv_quotes.py'))
V = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V)


def strip_tags(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', html.unescape(s))).strip()


def clean_kjv(raw):
    """Cache text carries Strong's tags and translator margin notes; the page
    wants the plain Authorized Version sentence."""
    s = html.unescape(raw)
    s = re.sub(r'<sup>.*?</sup>', '', s, flags=re.S)
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\d+', '', s)
    s = re.sub(r'\s+[A-Za-z][\w-]*:\s+(?:or|Heb|Gr|Gk|Chald|Chal|Called)\b.*$', '', s)
    s = re.sub(r'\s+([,.;:!?])', r'\1', s)   # Strong's stripping leaves gaps
    return re.sub(r'\s+', ' ', s).strip()


def hard(s):
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', '', V.norm(s))).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--range', nargs=2, type=int, metavar=('LO', 'HI'))
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()
    if not args.apply:
        args.dry_run = True

    cache = json.load(open(CACHE))
    stats = dict(files=0, repaired=0, cosmetic=0, elision=0, unresolved=0, ok=0)
    samples, touched = [], 0

    for path in sorted(glob.glob(os.path.join(BATCHES, '*.json'))):
        m = re.search(r'batch-(\d+)', os.path.basename(path))
        n = int(m.group(1)) if m else -1
        if args.range and not (args.range[0] <= n <= args.range[1]):
            continue
        try:
            entries = json.load(open(path))
        except Exception:
            continue
        stats['files'] += 1
        changed = False

        for e in entries:
            for pair in e.get('scriptures', []):
                if not isinstance(pair, list) or len(pair) < 2:
                    continue
                ref, text = pair[0], pair[1]
                if 'title' in ref:
                    continue
                mm = V.REF_RE.match(ref)
                bn = V.resolve_book(mm.group(1)) if mm else None
                if not bn:
                    stats['unresolved'] += 1
                    continue
                kjv_raw = V.cache_text(cache, bn, mm.group(2), mm.group(3), mm.group(4))
                if not kjv_raw:
                    stats['unresolved'] += 1
                    continue
                if V.quote_matches(text, kjv_raw):
                    stats['ok'] += 1
                    continue
                if re.search(r'\.{3}|…', text):
                    stats['elision'] += 1      # intentional partial quote — leave it
                    continue
                if hard(text)[:90] in hard(kjv_raw):
                    stats['cosmetic'] += 1     # artifact, not wrong text
                    continue

                fixed = clean_kjv(kjv_raw)
                if not fixed or not V.quote_matches(fixed, kjv_raw):
                    continue                   # refuse to write something unverified
                if args.limit and stats['repaired'] >= args.limit:
                    continue
                if len(samples) < 8:
                    samples.append((e.get('slug', '?'), ref,
                                    strip_tags(text)[:78], fixed[:78]))

                # Patch the PUBLISHED page too, by direct substitution.
                # Regenerating from the batch JSON would be the obvious route
                # and is wrong: generate_dict_entries.py emits sections without
                # the id="definition"/"scriptures"/"corruption" anchors that
                # 7,639 live pages carry, and nothing in the repo puts them
                # back — a one-off pass added them. Regeneration is therefore
                # lossy, so the quote text is replaced in place instead.
                page = os.path.join(ROOT, 'docs/dictionary', f"{e.get('slug','')}.html")
                if os.path.exists(page):
                    h = open(page, encoding='utf-8').read()
                    if text in h:
                        if args.apply:
                            open(page, 'w', encoding='utf-8').write(h.replace(text, fixed))
                        stats['pages'] = stats.get('pages', 0) + 1
                    else:
                        stats['page_miss'] = stats.get('page_miss', 0) + 1

                pair[1] = fixed
                stats['repaired'] += 1
                changed = True

        if changed:
            touched += 1
            if args.apply:
                json.dump(entries, open(path, 'w'), ensure_ascii=False, indent=2)

    print(f"batch files scanned : {stats['files']}")
    print(f"quotes already OK   : {stats['ok']}")
    print(f"REPAIRED            : {stats['repaired']}   (files touched: {touched})")
    print(f"left — elisions     : {stats['elision']}   (intentional partial quotes)")
    print(f"left — cosmetic     : {stats['cosmetic']}   (normalisation artifacts, text is fine)")
    print(f"left — unresolvable : {stats['unresolved']}")
    print(f"live pages patched  : {stats.get('pages', 0)}"
          f"   (quote not found on page: {stats.get('page_miss', 0)})")
    if samples:
        print('\nsamples:')
        for slug, ref, before, after in samples:
            print(f'  {slug}  {ref}')
            print(f'     was: {before}')
            print(f'     now: {after}')
    if args.dry_run:
        print('\n--dry-run: nothing written.')


if __name__ == '__main__':
    main()
