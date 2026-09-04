#!/usr/bin/env python3
"""Quarantine lexicon pages that fail bin/lexicon-gate.js — reversibly.

Governance rule 4 (reversibility): never truly delete. A quarantined page stays
on disk and stays reachable; it loses only its invitation to be indexed.

The ONLY thing this tool writes to a page is a `noindex, nofollow` robots meta.
It does not edit any sitemap. bin/generate_sitemap.py already drops every page
carrying that meta (see _has_noindex), so the sitemap is a derived artifact and
is simply regenerated. That matters: docs/sitemap-lexicon.xml gets rebuilt as a
side effect of the dictionary batch pipeline, so a quarantine implemented by
editing the sitemap would be silently undone on the next batch. The meta on the
page is the single source of truth and survives regeneration.

  quarantine:  bin/lexicon-quarantine.py --apply /tmp/list.txt --reason "..."
  restore one: bin/lexicon-quarantine.py --restore docs/lexicon/G1018.html
  restore all: bin/lexicon-quarantine.py --restore --all
  status:      bin/lexicon-quarantine.py --status
"""
import argparse
import json
import os
import re
import sys
from datetime import date

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(REPO, "LEXICON-QUARANTINE.md")
ROBOTS = '    <meta name="robots" content="noindex, nofollow">\n'
# Not line-anchored on purpose: some lexicon pages are minified onto one line
# (docs/lexicon/H4520.html), and a ^...$ anchor silently skips those.
CHARSET = re.compile(r'<meta\s+charset="UTF-8"\s*/?>', re.I)
HEAD_OPEN = re.compile(r'<head[^>]*>', re.I)
HAS_ROBOTS = re.compile(r'<meta\s+name="robots"', re.I)

LEDGER_HEADER = """# Lexicon Quarantine Ledger

Pages here failed `bin/lexicon-gate.js` and were pulled out of
`docs/sitemap-lexicon.xml` and marked `noindex, nofollow`. **Nothing was
deleted.** Every page is still on disk and still returns 200 to anyone holding
the URL; it is simply no longer offered to search engines.

Restore a page once its content is fixed and the gate passes:

    node bin/lexicon-gate.js docs/lexicon/G1018.html   # must pass first
    python3 bin/lexicon-quarantine.py --restore docs/lexicon/G1018.html

Restore everything (undo the whole action):

    python3 bin/lexicon-quarantine.py --restore --all

Both paths regenerate the sitemaps, so the page returns to
docs/sitemap-lexicon.xml automatically. Lines below are machine-readable.

"""


def load_ledger():
    if not os.path.exists(LEDGER):
        return {}
    body = open(LEDGER, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"^<!--ENTRY (\{.*\}) -->$", body, re.M):
        try:
            rec = json.loads(m.group(1))
            out[rec["path"]] = rec
        except (ValueError, KeyError):
            continue
    return out


def write_ledger(entries):
    lines = [LEDGER_HEADER]
    lines.append(f"**{len(entries)} pages currently quarantined.**\n\n")
    by_reason = {}
    for rec in entries.values():
        by_reason.setdefault(rec.get("reason", "unspecified"), []).append(rec)
    for reason, recs in sorted(by_reason.items()):
        lines.append(f"## {reason}\n\n")
        lines.append(f"{len(recs)} pages, quarantined {recs[0].get('date','?')}.\n\n")
        for rec in sorted(recs, key=lambda r: r["path"]):
            lines.append(f"<!--ENTRY {json.dumps(rec, sort_keys=True)} -->\n")
        lines.append("\n")
    open(LEDGER, "w", encoding="utf-8").write("".join(lines))


def add_noindex(fp):
    """Insert the robots meta. Returns 'added', 'already', or 'FAILED'."""
    src = open(fp, encoding="utf-8").read()
    if HAS_ROBOTS.search(src):
        return "already"
    tag = '<meta name="robots" content="noindex, nofollow">'
    m = CHARSET.search(src) or HEAD_OPEN.search(src)
    if not m:
        return "FAILED"
    # Match the file's own formatting: indent on multi-line pages, inline on
    # minified ones. generate_sitemap.py only reads the first 4096 bytes, so
    # the meta must go high in <head> either way.
    nl = "\n" in src[m.end():m.end() + 200]
    ins = ("\n    " + tag) if nl else tag
    new = src[:m.end()] + ins + src[m.end():]
    open(fp, "w", encoding="utf-8").write(new)
    return "added"


def strip_noindex(fp):
    src = open(fp, encoding="utf-8").read()
    new = re.sub(r'\n?[ \t]*<meta\s+name="robots"\s+content="noindex,\s*nofollow">', "", src, count=1)
    if new == src:
        return False
    open(fp, "w", encoding="utf-8").write(new)
    return True


def regenerate_sitemaps():
    """The sitemap is derived from the pages. Rebuild it rather than edit it."""
    import subprocess
    r = subprocess.run([sys.executable, os.path.join(REPO, "bin", "generate_sitemap.py")],
                       capture_output=True, text=True, cwd=REPO)
    if r.returncode != 0:
        print("WARNING: generate_sitemap.py failed; sitemap NOT updated:", file=sys.stderr)
        print(r.stderr.strip()[:800], file=sys.stderr)
        return False
    tail = [l for l in r.stdout.strip().splitlines() if l.strip()]
    for l in tail[-4:]:
        print("  " + l)
    return True


def cmd_apply(paths, reason):
    ledger = load_ledger()
    today = date.today().isoformat()
    marked = skipped = 0
    failures = []
    for rel in paths:
        fp = os.path.join(REPO, rel)
        if not os.path.exists(fp):
            print(f"  missing, skipped: {rel}", file=sys.stderr)
            skipped += 1
            continue
        # Re-attempt anything the ledger claims is quarantined but that does
        # not actually carry the meta: a ledger line is a record, not proof.
        if rel in ledger and HAS_ROBOTS.search(open(fp, encoding="utf-8").read(4096)):
            skipped += 1
            continue
        res = add_noindex(fp)
        if res == "FAILED":
            failures.append(rel)
            ledger.pop(rel, None)   # never record a page we could not mark
            continue
        if res == "added":
            marked += 1
        ledger[rel] = {"path": rel, "date": today, "reason": reason}
    write_ledger(ledger)
    print(f"quarantined {len(paths)} pages: {marked} newly noindexed, "
          f"{skipped} already handled/missing")
    regenerate_sitemaps()

    # Governance rule 6: a run that could not do its job must not exit 0.
    # Verify every page named actually carries the meta now, rather than
    # trusting the write path.
    unmarked = [r for r in paths
                if os.path.exists(os.path.join(REPO, r))
                and not HAS_ROBOTS.search(open(os.path.join(REPO, r), encoding="utf-8").read(4096))]
    if failures or unmarked:
        print(f"\nFAILED to mark {len(set(failures) | set(unmarked))} page(s):", file=sys.stderr)
        for r in sorted(set(failures) | set(unmarked))[:20]:
            print(f"  {r}", file=sys.stderr)
        return 1
    print(f"verified: all {len(paths)} pages carry noindex within the first 4096 bytes")
    return 0


def cmd_restore(paths):
    ledger = load_ledger()
    restored = 0
    for rel in paths:
        rec = ledger.get(rel)
        if not rec:
            print(f"  not quarantined: {rel}", file=sys.stderr)
            continue
        fp = os.path.join(REPO, rel)
        if os.path.exists(fp):
            strip_noindex(fp)
        del ledger[rel]
        restored += 1
    write_ledger(ledger)
    print(f"restored {restored} pages")
    regenerate_sitemaps()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", metavar="LISTFILE")
    ap.add_argument("--reason", default="failed bin/lexicon-gate.js")
    ap.add_argument("--restore", nargs="?", const="", metavar="PATH")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()

    if a.status:
        led = load_ledger()
        print(f"{len(led)} pages quarantined")
        for reason in sorted({r.get('reason') for r in led.values()}):
            n = sum(1 for r in led.values() if r.get('reason') == reason)
            print(f"  {n:>5}  {reason}")
        return 0

    if a.apply:
        paths = [l.strip() for l in open(a.apply) if l.strip()]
        if not paths:
            print("refusing to run on an empty list", file=sys.stderr)
            return 2
        return cmd_apply(paths, a.reason)

    if a.restore is not None:
        if a.all:
            cmd_restore(sorted(load_ledger()))
        elif a.restore:
            cmd_restore([a.restore])
        else:
            print("--restore needs a path, or --all", file=sys.stderr)
            return 2
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
