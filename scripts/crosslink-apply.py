#!/usr/bin/env python3
"""Apply a reviewed cross-link proposal file (CCW-1119-DIR2 Phase 4).

  python3 scripts/crosslink-apply.py <proposals.json> --site org|com --root <site dir> --ledger <out.md> [--check]

Each proposal: {file, find, replace, anchor, target, rationale, [count]}.
A proposal is applied only when
  * the target URL answers HTTP 200 on the live site (browser user agent), and
  * `find` occurs exactly `count` times in the file (default 1), and
  * the edit only adds an <a> element: with tags stripped, `find` and `replace`
    must carry the same visible text unless the proposal sets "adds_label": true
    (a link-only line such as a button, where the label is the target's own name).
Anything else is skipped and reported; nothing is written with --check.
The ledger records every proposal with its target status and outcome.
"""
import argparse, json, os, re, subprocess, sys
BASE = {'org': 'https://usmcmin.org', 'com': 'https://usmcmin.com'}
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
_cache = {}
def status(url):
    if url not in _cache:
        r = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '-A', UA, '--max-time', '25', url], capture_output=True, text=True)
        _cache[url] = r.stdout.strip() or '000'
    return _cache[url]
def absolute(site, target):
    return target if target.startswith('http') else BASE[site] + (target if target.startswith('/') else '/' + target)
def text(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('proposals'); ap.add_argument('--site', required=True, choices=BASE)
    ap.add_argument('--root', required=True); ap.add_argument('--ledger', required=True)
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    props = json.load(open(a.proposals))
    rows, applied, skipped = [], 0, 0
    for p in props:
        url = absolute(a.site, p['target']); code = status(url)
        path = os.path.join(a.root, p['file']); n = p.get('count', 1); why = ''
        if p.get('via'):                      # rendered by a generator from source data
            outcome = 'generator' if code == '200' else 'SKIP target ' + code
        else:
            body = open(path, encoding='utf-8').read()
            done = body.count(p['replace']); have = body.count(p['find'])
            is_done = done == n and (have == 0 or p['find'] in p['replace'])
            if code != '200': why = 'target ' + code
            elif p['target'] not in p['replace']: why = 'replace does not carry target'
            elif not p.get('adds_label') and text(p['find']) != text(p['replace']): why = 'visible text changes'
            elif not is_done and have != n: why = f'find matched {have}, expected {n}'
            if why: outcome = 'SKIP ' + why
            elif is_done: outcome = 'already applied'
            else:
                outcome = 'applied'
                if not a.check: open(path, 'w', encoding='utf-8').write(body.replace(p['find'], p['replace']))
        links = n if not outcome.startswith('SKIP') else 0
        applied += links; skipped += outcome.startswith('SKIP')
        rows.append((p['file'], p['anchor'], p['target'], code, str(n), outcome, p['rationale']))
        if outcome.startswith('SKIP'): print('SKIP', p['file'], '|', p['anchor'], '|', outcome, file=sys.stderr)
    with open(a.ledger, 'w', encoding='utf-8') as f:
        f.write(f"# Cross-link ledger: usmcmin.{a.site} (CCW-1119-DIR2 Phase 4, 2026-11-19)\n\n")
        f.write(f"Proposed by Fable (claude-fable-5-2); applied by `scripts/crosslink-apply.py`. {applied} link insertions across {len(set(r[0] for r in rows if not r[5].startswith('SKIP')))} pages; {skipped} proposals skipped.\n\n")
        f.write("Rules: target must return HTTP 200 live; anchor is existing page text (or the target's own name on a link-only line); no prose added; no links inside quotations or Scripture.\n\n")
        f.write("| Source page | Anchor | Target | Target status | Links | Outcome | Rationale |\n|---|---|---|---|---|---|---|\n")
        for r in rows: f.write('| ' + ' | '.join(x.replace('|', '\\|') for x in r) + ' |\n')
    print(f"{applied} link insertions, {skipped} skipped, ledger {a.ledger}")
    sys.exit(1 if skipped else 0)
main()
