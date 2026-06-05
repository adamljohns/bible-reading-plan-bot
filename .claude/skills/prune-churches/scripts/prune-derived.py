#!/usr/bin/env python3
"""prune-derived.py -- remove church id(s) from the DERIVED artifacts that the live
site reads: per-state shards, per-denomination-family shards, and sitemap-churches.xml.

Format-preserving: shards via json.dumps(indent=2, ensure_ascii=False) with NO trailing
newline (byte-identical to build_*_shards.py, round-trip guarded); sitemap via verbatim
<url>-block removal. Atomic writes. Scans ALL shard files, so it finds the record whatever
its state/denomination. Warns (does not edit) if an id is in directory-map-points.json --
that's a Node-written file of geocoded churches; rebuild it with build-directory-map.js.

Usage: python3 prune-derived.py [--dry-run] <id> [<id> ...]
Does NOT touch churches.json (use prune-churches.js -- Python can't reproduce its bytes)
and does NOT commit."""
import json, os, re, sys
from pathlib import Path


def find_root(start):
    d = Path(start).resolve()
    for _ in range(12):
        if (d / 'docs/data/churches.json').exists():
            return d
        if d.parent == d:
            break
        d = d.parent
    raise SystemExit('could not locate repo root above ' + str(start))


argv = sys.argv[1:]
dry = '--dry-run' in argv
ids = {str(a) for a in argv if a != '--dry-run'}
if not ids:
    raise SystemExit('usage: python3 prune-derived.py [--dry-run] <id> [<id> ...]')

ROOT = find_root(__file__)
touched = []


def edit_shard(p):
    orig = p.read_bytes()
    try:
        d = json.loads(orig)
    except json.JSONDecodeError:
        return
    if not isinstance(d, dict) or 'churches' not in d:
        return
    # Round-trip guard (shards carry NO trailing newline). If a shard isn't byte-stable under
    # our serializer, skip it rather than reformat the whole file -- regenerate via build_*_shards.py.
    if json.dumps(d, indent=2, ensure_ascii=False).encode() != orig:
        print(f'  WARN: {p.name} not byte-stable under Python serializer; skipped (regen via build_*_shards.py)')
        return
    present = [str(c.get('id')) for c in d['churches'] if str(c.get('id')) in ids]
    if not present:
        return
    rel = p.relative_to(ROOT)
    if dry:
        print(f'  [dry-run] {rel}: would remove {len(present)} {present}')
        return
    d['churches'] = [c for c in d['churches'] if str(c.get('id')) not in ids]
    if 'record_count' in d:
        d['record_count'] = len(d['churches'])
    tmp = p.with_name(p.name + '.tmp' + str(os.getpid()))
    tmp.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding='utf-8')
    os.replace(tmp, p)
    print(f'  {rel}: removed {len(present)} [{", ".join(present)}]; record_count={d.get("record_count")}')
    touched.append(str(rel))


for sub in ('docs/data/churches/by-state', 'docs/data/churches/by-denomination-family'):
    dirp = ROOT / sub
    if dirp.is_dir():
        for p in sorted(dirp.glob('*.json')):
            edit_shard(p)

# Sitemap: drop the matching <url> blocks, keep the rest verbatim and in order.
sm = ROOT / 'docs/sitemap-churches.xml'
if sm.exists():
    text = sm.read_text(encoding='utf-8')
    urls = {f'/churches/{i}.html' for i in ids}
    blocks = re.findall(r'  <url>.*?</url>', text, re.DOTALL)
    drop = [b for b in blocks if any(u in b for u in urls)]
    if drop and dry:
        print(f'  [dry-run] sitemap-churches.xml: would drop {len(drop)} <url> block(s)')
    elif drop:
        kept = [b for b in blocks if b not in drop]
        xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + '\n'.join(kept) + '\n</urlset>\n')
        tmp = sm.with_name(sm.name + '.tmp' + str(os.getpid()))
        tmp.write_text(xml, encoding='utf-8')
        os.replace(tmp, sm)
        print(f'  docs/sitemap-churches.xml: dropped {len(drop)} block(s); now {len(kept)} entries')
        touched.append('docs/sitemap-churches.xml')

# Map-points: warn only (Node-written; rebuild if a removed church was geocoded).
mp = ROOT / 'docs/data/directory-map-points.json'
if mp.exists():
    blob = mp.read_text(encoding='utf-8')
    hit = [i for i in ids if f'"{i}"' in blob]
    if hit:
        print(f'  NOTE: {hit} present in directory-map-points.json (geocoded). Rebuild the map:')
        print('        node scripts/build-directory-map.js')

print('  TOUCHED: ' + (' '.join(touched) if touched else '(no derived artifact contained these ids)'))
