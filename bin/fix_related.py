#!/usr/bin/env python3
"""Drop related-chip targets that do not resolve to a real entry page.

Authoring at volume, roughly one related target in forty names a slug that
sounds obvious but was never created (`gentiles`, `crowd`, `divorce`). The
pre-flight rightly refuses those. Rather than hand-substitute each one, drop
the unresolvable target: a chip that goes nowhere is worse than one fewer
chip. Refuses to leave an entry with under two, so a stripped entry is
reported instead of silently impoverished.

Usage: python3 bin/fix_related.py data/dictionary-batches/batch-NNN-*.json
"""
import json, os, sys

def main():
    pages = {f[:-5] for f in os.listdir('docs/dictionary') if f.endswith('.html')}
    allnew = set()
    for p in sys.argv[1:]:
        for e in json.load(open(p)):
            allnew.add(e.get('slug'))
    total = 0
    for p in sys.argv[1:]:
        data = json.load(open(p))
        changed = False
        for e in data:
            keep, drop = [], []
            for pair in e.get('related', []):
                if isinstance(pair, list) and len(pair) == 2 and (
                        pair[0] in pages or pair[0] in allnew):
                    keep.append(pair)
                else:
                    drop.append(pair[0] if isinstance(pair, list) and pair else pair)
            if drop:
                if len(keep) < 2:
                    print(f'  !! {e["slug"]}: only {len(keep)} related left after '
                          f'dropping {drop} — add more by hand')
                e['related'] = keep
                changed = True
                total += len(drop)
                print(f'  dropped {drop} from {e["slug"]}')
        if changed:
            json.dump(data, open(p, 'w'), ensure_ascii=False, indent=1)
    print(f'fix_related: dropped {total} unresolvable target(s)')

if __name__ == '__main__':
    main()
