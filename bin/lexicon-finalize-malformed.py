#!/usr/bin/env python3
"""Convert quarantined GG*/HH* duplicate lexicon pages into redirect stubs.

Malformed double-prefix pages duplicate live G*/H* entries. This replaces each
with a minimal 301-style refresh stub (same pattern as church merged-redirects)
and removes them from LEXICON-QUARANTINE.md.

Usage:
  python3 bin/lexicon-finalize-malformed.py [--dry-run]
"""
import argparse
import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEX = os.path.join(REPO, "docs", "lexicon")
LEDGER = os.path.join(REPO, "LEXICON-QUARANTINE.md")

MALFORMED = re.compile(r"^(G{2}|H{2})(\d+)\.html$")


def target_code(bad: str) -> str | None:
    m = MALFORMED.match(bad)
    if not m:
        return None
    prefix = "G" if m.group(1).startswith("G") else "H"
    return f"{prefix}{m.group(2)}"


def redirect_stub(from_code: str, to_code: str) -> str:
    url = f"/lexicon/{to_code}.html"
    canon = f"https://usmcmin.org/lexicon/{to_code}.html"
    return (
        f'<!doctype html><!-- lexicon-redirect malformed:{from_code} -->\n'
        f'<html><head><meta charset="utf-8">\n'
        f'<meta name="robots" content="noindex, nofollow">\n'
        f'<meta http-equiv="refresh" content="0; url={url}">\n'
        f'<link rel="canonical" href="{canon}">\n'
        f"<title>Strong's {from_code} → {to_code}</title></head>\n"
        f'<body><p>Malformed Strong&rsquo;s code. '
        f'<a href="{url}">Continue to {to_code} &rarr;</a></p></body></html>\n'
    )


def template_stub() -> str:
    return (
        '<!doctype html><!-- lexicon-redirect template -->\n'
        '<html><head><meta charset="utf-8">\n'
        '<meta name="robots" content="noindex, nofollow">\n'
        '<meta http-equiv="refresh" content="0; url=/lexicon/index.html">\n'
        '<link rel="canonical" href="https://usmcmin.org/lexicon/index.html">\n'
        '<title>Lexicon template</title></head>\n'
        '<body><p>Authoring scaffold only. '
        '<a href="/lexicon/index.html">Go to lexicon index &rarr;</a></p></body></html>\n'
    )


def load_ledger_paths():
    if not os.path.exists(LEDGER):
        return []
    body = open(LEDGER, encoding="utf-8").read()
    paths = []
    for m in re.finditer(r"^<!--ENTRY (\{.*\}) -->$", body, re.M):
        try:
            paths.append(json.loads(m.group(1))["path"])
        except (ValueError, KeyError):
            continue
    return paths


def clear_ledger(finalized: list[str]):
    header = """# Lexicon Quarantine Ledger

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
    note = (
        f"**0 pages currently quarantined.**\n\n"
        f"## finalized malformed redirects ({len(finalized)} pages, 2026-09-04)\n\n"
        "Double-prefix GG/HH duplicates and `template.html` were converted to "
        "`lexicon-redirect` stubs pointing at the canonical G/H entry (or lexicon index). "
        "They stay noindex and out of the sitemap.\n\n"
    )
    open(LEDGER, "w", encoding="utf-8").write(header + note)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ledger_paths = load_ledger_paths()
    if not ledger_paths:
        # Fall back: every GG/HH on disk + template
        ledger_paths = [
            f"docs/lexicon/{f}"
            for f in os.listdir(LEX)
            if MALFORMED.match(f) or f == "template.html"
        ]

    converted = []
    skipped = []
    for rel in sorted(ledger_paths):
        base = os.path.basename(rel)
        fp = os.path.join(REPO, rel)
        if base == "template.html":
            stub = template_stub()
        else:
            to = target_code(base)
            if not to:
                skipped.append(rel)
                continue
            correct = os.path.join(LEX, f"{to}.html")
            if not os.path.exists(correct):
                print(f"SKIP (no target): {base} -> {to}", file=sys.stderr)
                skipped.append(rel)
                continue
            stub = redirect_stub(base.replace(".html", ""), to)

        converted.append(rel)
        if args.dry_run:
            print(f"would convert {rel}")
        else:
            open(fp, "w", encoding="utf-8").write(stub)

    if args.dry_run:
        print(f"\nDry run: {len(converted)} convert, {len(skipped)} skip")
        return 0

    clear_ledger(converted)
    print(f"Converted {len(converted)} pages to redirect stubs")
    if skipped:
        print(f"Skipped {len(skipped)}", file=sys.stderr)

    r = subprocess.run(
        [sys.executable, os.path.join(REPO, "bin", "generate_sitemap.py")],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        print(r.stderr[:800], file=sys.stderr)
        return 1
    for line in r.stdout.strip().splitlines()[-4:]:
        print(" ", line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
