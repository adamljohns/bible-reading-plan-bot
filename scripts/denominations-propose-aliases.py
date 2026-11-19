#!/usr/bin/env python3
"""denominations-propose-aliases.py — ask the LOCAL model (LM Studio :1234)
to propose a canonical body for every distinct churches.json denomination label.

The model only proposes. Nothing reads its output to decide a mapping:
scripts/build-denomination-alias-map.js applies the deterministic rules in
scripts/lib/denomination-alias-rules.js and reports where the model agrees or
disagrees, so a reviewer can tighten a rule. No cloud model is ever called.

  python3 scripts/denominations-propose-aliases.py [--batch 25] [--model gemma-4-31b-it]

Writes data/denominations/aliases/alias-proposals.json. Read-only on churches.json.
"""
import argparse, json, os, re, subprocess, sys, time, urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'denominations', 'aliases', 'alias-proposals.json')
URL = 'http://127.0.0.1:1234/v1/chat/completions'


def labels_and_bodies():
    js = r'''
const R=require("./scripts/lib/denomination-alias-rules.js");
const raw=require("./docs/data/churches.json");const cs=Array.isArray(raw)?raw:raw.churches;
const m={};for(const c of cs){const k=c.denomination==null?"":String(c.denomination);m[k]=(m[k]||0)+1}
console.log(JSON.stringify({labels:Object.entries(m).sort((a,b)=>b[1]-a[1]),bodies:R.BODIES.map(b=>({id:b.id,name:b.name,short:b.short_name}))}));'''
    return json.loads(subprocess.check_output(['node', '-e', js], cwd=ROOT))


def ask(model, bodies, batch):
    body_list = '\n'.join(f"{b['id']}: {b['name']} ({b['short']})" for b in bodies)
    numbered = '\n'.join(f'{i}. {l}' for i, l in enumerate(batch))
    prompt = (
        'You classify church denomination labels. Canonical bodies (id: name):\n' + body_list +
        '\n\nFor each numbered label answer with ONE of: a body id from the list; "generic" if it names only a '
        'family or no body (e.g. Baptist, Non-Denominational, Reformed Baptist, Independent Baptist, Unverified); '
        'or "unresolved" if it is hedged (verify, likely, formerly, disfellowshipped), names two or more bodies, '
        'or names a body not in the list. Do not guess.\n\nLabels:\n' + numbered +
        '\n\nReply with JSON only: {"0":"<answer>","1":"<answer>",...}')
    req = urllib.request.Request(URL, data=json.dumps({
        'model': model, 'temperature': 0, 'max_tokens': 2000,
        'messages': [{'role': 'user', 'content': prompt}]}).encode(), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=600) as r:
        txt = json.load(r)['choices'][0]['message']['content']
    m = re.search(r'\{.*\}', txt, re.S)
    return json.loads(m.group(0)) if m else {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--batch', type=int, default=25)
    ap.add_argument('--model', default='gemma-4-31b-it')
    a = ap.parse_args()
    data = labels_and_bodies()
    ids = {b['id'] for b in data['bodies']}
    labels = [l for l, _ in data['labels']]
    out = {}
    for i in range(0, len(labels), a.batch):
        batch = labels[i:i + a.batch]
        ans = {}
        for attempt in range(2):
            try:
                ans = ask(a.model, data['bodies'], batch); break
            except Exception as e:  # noqa: BLE001 — a failed batch stays unproposed
                print(f'batch {i}: {e}', file=sys.stderr); time.sleep(2)
        for j, l in enumerate(batch):
            v = str(ans.get(str(j), '')).strip().lower()
            out[l] = v if (v in ids or v in ('generic', 'unresolved')) else None
        print(f'{min(i + a.batch, len(labels))}/{len(labels)}', file=sys.stderr, flush=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = {'_note': 'Local-model PROPOSALS only. The deterministic rules decide; see alias-map.json.',
           'model': a.model, 'endpoint': URL, 'generated_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
           'proposals': [{'label': l, 'proposed': out[l]} for l in labels]}
    with open(OUT, 'w') as f:
        json.dump(doc, f, indent=1, ensure_ascii=False); f.write('\n')
    print(f'wrote {OUT}: {sum(1 for v in out.values() if v)} proposals / {len(labels)} labels', file=sys.stderr)


if __name__ == '__main__':
    main()
