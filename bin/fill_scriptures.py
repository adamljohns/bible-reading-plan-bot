#!/usr/bin/env python3
"""Fill empty scripture texts in a batch JSON from docs/assets/verse-cache.json.

DON'T TRANSCRIBE SCRIPTURE — GENERATE IT. Entries are authored with refs only
(['Isa 30:14', '']); this pulls the Authorized Version through the verifier's
own resolver and writes it in, so a transcription defect is structurally
impossible. Any unresolvable or uncached ref is a hard failure: fix the ref,
never hand-type the verse.

Usage: python3 bin/fill_scriptures.py data/dictionary-batches/batch-NN-*.json [...]
"""
import json, os, sys, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _load(name):
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(ROOT, f'bin/{name}.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

V = _load('verify_kjv_quotes')
R = _load('repair_kjv_quotes')

def main():
    cache = json.load(open(os.path.join(ROOT, 'docs/assets/verse-cache.json')))
    failures = 0
    for path in sys.argv[1:]:
        entries = json.load(open(path))
        filled = 0
        for e in entries:
            for pair in e.get('scriptures', []):
                if not isinstance(pair, list) or len(pair) < 2 or pair[1]:
                    continue
                parsed = V.parse_ref(pair[0])
                raw = V.cache_text(cache, *parsed) if parsed else None
                if not raw:
                    print(f'FAIL {e.get("slug","?")}: cannot fill {pair[0]!r}')
                    failures += 1
                    continue
                pair[1] = R.clean_kjv(raw)
                filled += 1
        if not failures:
            json.dump(entries, open(path, 'w'), ensure_ascii=False, indent=2)
        print(f'{os.path.basename(path)}: filled {filled}')
    sys.exit(1 if failures else 0)

if __name__ == '__main__':
    main()
