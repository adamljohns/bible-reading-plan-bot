#!/usr/bin/env python3
"""approval_gate.py — make "hidden until APPROVE" a mechanism, not an honor system.

Adam's standing rule (MOOP-MASTER-PLAN, governance #1): nothing outward-facing
goes public without his explicit APPROVE. Until now that was a convention, and it
failed three times — 11 MHA drafts crawlable since July, 33 empty scaffold pages
wired into the sitemap on 8/07, and four blog posts shipped with no recorded
approval. This tool closes that hole.

A page is a BREACH when it is publicly indexable AND not fit to be public:

  scaffold   visible text carries a placeholder marker ("Text pending",
             "coming soon", "lorem ipsum", "TODO") — an empty shell
  thin       sitemapped page with less visible text than --min-chars, which is
             how a scaffold hides when nobody wrote the word "pending"
  unapproved blog post that is live and absent from the approval ledger

"Publicly indexable" means: NOT carrying <meta name="robots" content="noindex">,
and NOT sitting under a path robots.txt already disallows.

The ledger is APPROVALS.md at the repo root. One line per approved page:
    2026-08-07 | docs/blog/neither-rot-nor-break.html | APPROVE (Telegram)
Lines that do not start with a date are ignored, so prose around them is fine.

Usage:
  python3 bin/approval_gate.py --audit              # report; exit 1 on breach
  python3 bin/approval_gate.py --audit --quiet      # summary + breaches only
  python3 bin/approval_gate.py --fix-scaffolds      # add noindex to scaffold/thin
  python3 bin/approval_gate.py --fix path/a.html    # add noindex to named files
  python3 bin/approval_gate.py --release path/a.html  # REMOVE noindex (on APPROVE)

--fix* rewrites files in place. It only ever ADDS a noindex meta tag; it never
deletes content, and re-running is a no-op. --release is the deliberate inverse
and refuses to act on a page that is still a scaffold.
"""
import argparse
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
LEDGER = os.path.join(ROOT, 'APPROVALS.md')
ROBOTS = os.path.join(DOCS, 'robots.txt')

# Placeholder text that means "this page is not written yet."
#
# Every marker here must be SELF-REFERENTIAL — a statement the page makes about
# itself. Vague phrases do not work on a Bible site: a bare "coming soon" match
# flagged 18 finished lexicon and dictionary pages, because Revelation 22:20 is
# "Yes, I am coming soon." A bare "placeholder text" flagged a church review
# that was describing *the church's* website. Keep these unambiguous.
SCAFFOLD_MARKERS = [
    'text pending',
    'this page is scaffolding',
    'lorem ipsum',
    'content tbd',
    'content coming soon',
    'page coming soon',
    'this is placeholder',
]

# NOTE: "under construction" was tried and removed too — the church-directory
# reviews use it to describe *the church's own* website ("site appears
# partially under construction"), not this page.

# A sitemapped page thinner than this is a scaffold that forgot to say so.
DEFAULT_MIN_CHARS = 900

# A scaffold marker only means "empty shell" on a SHORT page. A long, finished
# essay that happens to contain the words "coming soon" is not a breach, and
# flagging it trains everyone to ignore the audit.
SCAFFOLD_MAX_CHARS = 3000

# The thin-page test applies to teaching content, where a short page means
# unfinished work. It does NOT apply to app screens, assessments, or utility
# pages (404, offline), which are legitimately brief or rendered by JS.
CONTENT_PREFIXES = ('blog/', 'confessions/', 'bfm/', 'chapters/',
                    'institutes/', 'lbcf/', 'catechism/')

# Adam set the approval gate on 2026-07-09. Posts published before that are his
# legacy archive (some go back to the 2007 Iraq deployment) and are out of
# scope — retroactively flagging 196 of them would bury the four that matter.
GATE_EPOCH = '2026-07-09'
PUBLISHED_RE = re.compile(
    r'<meta\s+name=["\']article:published_time["\']\s+content=["\'](\d{4}-\d{2}-\d{2})',
    re.I)

# Legacy posts carry no meta tag but do render their own date, e.g.
#   <div class="meta">March 16, 2007 &middot; <span class="category-tag">...
# This beats the git fallback, which misreads any file that was re-committed
# later — 46s-trip-to-iraq.html is a 2007 post that git dates to 2026-07-18.
MONTHS = {m: i for i, m in enumerate(
    ['january', 'february', 'march', 'april', 'may', 'june', 'july',
     'august', 'september', 'october', 'november', 'december'], 1)}
META_DATE_RE = re.compile(
    r'<div class=["\']meta["\']>\s*([A-Z][a-z]+)\s+(\d{1,2}),\s*(\d{4})')


def rendered_date(html):
    """The date the page shows the reader, as YYYY-MM-DD, or None."""
    m = META_DATE_RE.search(html)
    if not m:
        return None
    mon = MONTHS.get(m.group(1).lower())
    if not mon:
        return None
    return f'{int(m.group(3)):04d}-{mon:02d}-{int(m.group(2)):02d}'

NOINDEX_TAG = '    <meta name="robots" content="noindex, nofollow">'
NOINDEX_RE = re.compile(r'<meta\s+name=["\']robots["\'][^>]*noindex', re.I)

# Blog posts are the gated surface; these are infrastructure, not content.
BLOG_EXEMPT = {'index.html'}

# docs/verse/ holds two different kinds of page needing different rules:
#   * hand-authored DEEP STUDIES (1,200-4,000 words) -- outward-facing doctrinal
#     teaching, exactly what governance rule 1 covers, so they carry the
#     approval gate like blog posts.
#   * short generated verse LANDING pages (~100-140 words, from
#     bin/add-verse-page.js) -- site furniture like dictionary entries.
# Length separates them. Gating the whole prefix sweeps in the landing pages and
# fails the deploy on them as "thin". Adam ruled on this split 2026-09-04.
DEEP_STUDY_MIN_CHARS = 6000        # ~1,000 words of visible text


def is_approval_gated(docs_path, visible):
    """Does this page need an APPROVE line before it may be indexable?"""
    if docs_path.startswith('blog/'):
        return True
    if docs_path.startswith('verse/'):
        return len(visible) >= DEEP_STUDY_MIN_CHARS
    return False


def visible_text(html):
    """Approximate what a reader (and a crawler) actually sees."""
    h = re.sub(r'<script.*?</script>', ' ', html, flags=re.S | re.I)
    h = re.sub(r'<style.*?</style>', ' ', h, flags=re.S | re.I)
    h = re.sub(r'<!--.*?-->', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    return ' '.join(h.split())


def rel(path):
    return os.path.relpath(path, ROOT)


def git_added_dates(*subdirs):
    """Map repo-relative path -> date the file was FIRST committed.

    Most posts (199 of 214) carry no article:published_time, so the meta tag
    alone cannot tell a 2007 archive post from an unapproved draft written last
    month. First-commit date can: the legacy archive was migrated in one pass on
    2026-03-15, while the MHA drafts land 2026-07-12. One git walk, not one call
    per file.
    """
    dates = {}
    try:
        out = subprocess.run(
            ['git', 'log', '--diff-filter=A', '--name-only', '--format=%ad',
             '--date=short', '--', *subdirs],
            cwd=ROOT, capture_output=True, text=True, timeout=120).stdout
    except (OSError, subprocess.SubprocessError):
        return dates
    cur = None
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', line):
            cur = line
        elif cur:
            # git log walks newest first, so the LAST write wins = first commit.
            dates[line] = cur
    return dates


def load_ledger():
    """Read APPROVALS.md -> (approved, logged).

    approved  Adam said APPROVE. The page is legitimately public.
    logged    a gap already surfaced to Adam and awaiting his ruling. Reported
              every run, but it does NOT fail the audit — a weekly alarm that
              re-screams the same known 14 items forever is an alarm everyone
              learns to ignore, which is how the gate got breached in the first
              place. Only NEW breaches fail.
    """
    approved, logged = set(), set()
    if not os.path.exists(LEDGER):
        return approved, logged
    with open(LEDGER, encoding='utf-8') as fh:
        for line in fh:
            if not re.match(r'^\s*\d{4}-\d{2}-\d{2}\s*\|', line):
                continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 3:
                continue
            verb = parts[2].upper()
            if 'LOGGED-GAP' in verb:
                logged.add(parts[1])
            elif 'APPROVE' in verb:
                approved.add(parts[1])
    return approved, logged


def robots_disallowed():
    """Path prefixes robots.txt already blocks — those are legitimately hidden."""
    prefixes = []
    if not os.path.exists(ROBOTS):
        return prefixes
    with open(ROBOTS, encoding='utf-8') as fh:
        for line in fh:
            m = re.match(r'^\s*Disallow:\s*(\S+)', line, re.I)
            if m and m.group(1) != '/':
                prefixes.append(m.group(1))
    return prefixes


def sitemapped():
    """Every URL path listed in any sitemap-*.xml, as a docs-relative path."""
    paths = set()
    for name in os.listdir(DOCS):
        if not (name.startswith('sitemap') and name.endswith('.xml')):
            continue
        with open(os.path.join(DOCS, name), encoding='utf-8', errors='replace') as fh:
            for loc in re.findall(r'<loc>\s*(.*?)\s*</loc>', fh.read(), re.S):
                p = re.sub(r'^https?://[^/]+', '', loc.strip()).lstrip('/')
                if p.endswith('.html'):
                    paths.add(p)
    return paths


def has_noindex(html):
    return bool(NOINDEX_RE.search(html))


def is_hidden_by_robots(docs_path, prefixes):
    url = '/' + docs_path
    return any(url.startswith(p) for p in prefixes)


def scan(min_chars):
    """Walk docs/ and classify every page. Returns (breaches, stats)."""
    approved, logged = load_ledger()
    prefixes = robots_disallowed()
    smap = sitemapped()
    # Must cover every approval-gated prefix. Until 2026-09-04 this walked
    # docs/blog only, so a docs/verse/ page got published=None and the breach
    # test below (`published and published >= GATE_EPOCH`) could never fire --
    # which made the verse gate a silent no-op. Caught by planting an
    # unapproved deep study and watching the audit pass it.
    added = git_added_dates('docs/blog', 'docs/verse')

    breaches = []
    stats = {'pages': 0, 'noindex': 0, 'sitemapped': len(smap)}

    for dirpath, dirnames, filenames in os.walk(DOCS):
        dirnames[:] = [d for d in dirnames if not d.startswith('_') and d != 'node_modules']
        for fn in sorted(filenames):
            if not fn.endswith('.html'):
                continue
            full = os.path.join(dirpath, fn)
            docs_path = os.path.relpath(full, DOCS)
            stats['pages'] += 1

            try:
                with open(full, encoding='utf-8', errors='replace') as fh:
                    html = fh.read()
            except OSError:
                continue

            if has_noindex(html):
                stats['noindex'] += 1
                continue
            if is_hidden_by_robots(docs_path, prefixes):
                continue

            text = visible_text(html)
            low = text.lower()
            marker = next((m for m in SCAFFOLD_MARKERS if m in low), None)

            if marker and len(text) < SCAFFOLD_MAX_CHARS:
                breaches.append(('scaffold', docs_path, f'"{marker}" — {len(text)} chars visible'))
                continue

            pm = PUBLISHED_RE.search(html)
            published = (pm.group(1) if pm else
                         rendered_date(html) or added.get(rel(full)))

            # Legacy blog posts predate the gate. Many are genuinely short —
            # 2007 deployment photo posts — and finished. Not breaches.
            legacy_blog = docs_path.startswith('blog/') and (
                published is None or published < GATE_EPOCH)

            is_content = docs_path.startswith(CONTENT_PREFIXES)
            if is_content and not legacy_blog and docs_path in smap and len(text) < min_chars:
                breaches.append(('thin', docs_path, f'{len(text)} chars visible, in sitemap'))
                continue

            # Blog posts and deep verse studies carry the approval gate;
            # everything else is site furniture. Until 2026-09-04 this tested
            # blog/ only, so docs/verse/ deep studies were ungated entirely.
            if is_approval_gated(docs_path, text) and fn not in BLOG_EXEMPT:
                r = rel(full)
                if published and published >= GATE_EPOCH and r not in approved:
                    kind = 'pending' if r in logged else 'unapproved'
                    breaches.append((kind, docs_path,
                                     f'published {published}, no APPROVE on record'))

    return breaches, stats


def add_noindex(full):
    """Insert the noindex meta after <meta charset>. Returns True if changed."""
    with open(full, encoding='utf-8', errors='replace') as fh:
        html = fh.read()
    if has_noindex(html):
        return False
    m = re.search(r'<meta\s+charset=[^>]*>', html, re.I)
    if m:
        idx = m.end()
    else:
        m = re.search(r'<head[^>]*>', html, re.I)
        if not m:
            return False
        idx = m.end()
    out = html[:idx] + '\n' + NOINDEX_TAG + html[idx:]
    with open(full, 'w', encoding='utf-8') as fh:
        fh.write(out)
    return True


def remove_noindex(full):
    with open(full, encoding='utf-8', errors='replace') as fh:
        html = fh.read()
    out = re.sub(r'[ \t]*<meta\s+name=["\']robots["\'][^>]*noindex[^>]*>\s*\n?', '', html, flags=re.I)
    if out == html:
        return False
    with open(full, 'w', encoding='utf-8') as fh:
        fh.write(out)
    return True


def resolve(arg):
    """Accept repo-relative, docs-relative, or absolute paths."""
    for cand in (arg, os.path.join(ROOT, arg), os.path.join(DOCS, arg)):
        if os.path.isfile(cand):
            return os.path.abspath(cand)
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--audit', action='store_true', help='report breaches; exit 1 if any')
    ap.add_argument('--fix-scaffolds', action='store_true',
                    help='add noindex to every scaffold/thin breach found')
    ap.add_argument('--fix', nargs='+', metavar='PATH', help='add noindex to named files')
    ap.add_argument('--release', nargs='+', metavar='PATH',
                    help='remove noindex (use only after an APPROVE is logged)')
    ap.add_argument('--min-chars', type=int, default=DEFAULT_MIN_CHARS,
                    help=f'thin-page threshold (default {DEFAULT_MIN_CHARS})')
    ap.add_argument('--quiet', action='store_true', help='summary + breaches only')
    args = ap.parse_args()

    if args.fix:
        changed = 0
        for a in args.fix:
            full = resolve(a)
            if not full:
                print(f'  SKIP (not found) {a}')
                continue
            if add_noindex(full):
                changed += 1
                print(f'  noindex + {rel(full)}')
        print(f'\nnoindex added to {changed} file(s).')
        return 0

    if args.release:
        for a in args.release:
            full = resolve(a)
            if not full:
                print(f'  SKIP (not found) {a}')
                continue
            with open(full, encoding='utf-8', errors='replace') as fh:
                low = visible_text(fh.read()).lower()
            if any(m in low for m in SCAFFOLD_MARKERS):
                print(f'  REFUSED {rel(full)} — still a scaffold; write the text first')
                continue
            if rel(full) not in load_ledger()[0]:
                print(f'  REFUSED {rel(full)} — no APPROVE line in APPROVALS.md')
                continue
            print(f'  released {rel(full)}' if remove_noindex(full)
                  else f'  already public {rel(full)}')
        return 0

    breaches, stats = scan(args.min_chars)

    if args.fix_scaffolds:
        targets = [b for b in breaches if b[0] in ('scaffold', 'thin')]
        changed = 0
        for kind, docs_path, _ in targets:
            if add_noindex(os.path.join(DOCS, docs_path)):
                changed += 1
                print(f'  noindex + {docs_path}  [{kind}]')
        print(f'\nnoindex added to {changed} of {len(targets)} scaffold/thin page(s).')
        return 0

    # ── audit report ──────────────────────────────────────────────────────
    by_kind = {}
    for kind, docs_path, why in breaches:
        by_kind.setdefault(kind, []).append((docs_path, why))

    print('=' * 68)
    print('APPROVAL GATE AUDIT')
    print('=' * 68)
    print(f'  pages scanned    {stats["pages"]}')
    print(f'  already noindex  {stats["noindex"]}')
    print(f'  sitemapped URLs  {stats["sitemapped"]}')
    _appr, _log = load_ledger()
    print(f'  approved         {len(_appr)}')
    print(f'  logged gaps      {len(_log)}')
    print()

    labels = {
        'scaffold': 'SCAFFOLD — placeholder text, publicly indexable',
        'thin': f'THIN — sitemapped, under {args.min_chars} chars of visible text',
        'unapproved': 'UNAPPROVED — live blog post with no APPROVE on record',
        'pending': 'PENDING — gap already logged, awaiting Adam\'s ruling (does not fail)',
    }
    for kind in ('scaffold', 'thin', 'unapproved', 'pending'):
        items = by_kind.get(kind, [])
        if not items:
            continue
        print(f'{labels[kind]}  ({len(items)})')
        show = items if not args.quiet else items[:15]
        for docs_path, why in show:
            print(f'    {docs_path}  — {why}')
        if len(show) < len(items):
            print(f'    ... and {len(items) - len(show)} more')
        print()

    hard = [b for b in breaches if b[0] != 'pending']
    npend = len(breaches) - len(hard)
    if hard:
        print(f'RESULT: FAIL — {len(hard)} page(s) publicly indexable that should not be.')
        print('Fix: python3 bin/approval_gate.py --fix-scaffolds')
        return 1
    tail = f' ({npend} logged gap(s) still awaiting Adam)' if npend else ''
    print(f'RESULT: PASS — no new breach.{tail}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
