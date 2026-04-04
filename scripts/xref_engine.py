#!/usr/bin/env python3
"""
Engine: reads a batch JSON file, merges into cross-references.json, commits & pushes.
Usage: python3 xref_engine.py <batch_file.json> <batch_number>
"""
import json, subprocess, os, sys

XREF = "/Users/adamjohns/bible-reading-plan-bot/docs/assets/cross-references.json"
REPO = "/Users/adamjohns/bible-reading-plan-bot"

MAX_CHAPTERS = {
    1:50,2:40,3:27,4:36,5:34,6:24,7:21,8:4,9:31,10:24,
    11:22,12:25,13:29,14:36,15:10,16:13,17:10,18:42,19:150,20:31,
    21:12,22:8,23:66,24:52,25:5,26:48,27:12,28:14,29:3,30:9,
    31:4,32:1,33:7,34:3,35:3,36:4,37:2,38:14,39:4,40:28,
    41:16,42:24,43:21,44:28,45:16,46:16,47:13,48:6,49:6,50:4,
    51:4,52:1,53:1,54:6,55:4,56:1,57:4,58:13,59:5,60:5,
    61:1,62:5,63:1,64:1,65:1,66:22
}

def valid_ref(ref):
    parts = ref.split("_")
    if len(parts) != 3: return False
    try:
        b,c,v = int(parts[0]), int(parts[1]), int(parts[2])
        return 1 <= b <= 66 and 1 <= c <= MAX_CHAPTERS.get(b,0) and v >= 1
    except: return False

def main():
    batch_file = sys.argv[1]
    batch_num = sys.argv[2]
    
    with open(batch_file) as f:
        new_refs = json.load(f)
    
    with open(XREF) as f:
        data = json.load(f)
    
    before = len(data)
    added = 0
    bad = []
    
    for k, vals in new_refs.items():
        if not valid_ref(k):
            bad.append(f"BAD KEY: {k}")
            continue
        clean = [v for v in vals if valid_ref(v)]
        for bv in [v for v in vals if not valid_ref(v)]:
            bad.append(f"BAD VAL: {bv} in {k}")
        if k not in data:
            data[k] = clean
            added += 1
        else:
            existing = set(data[k])
            for v in clean:
                if v not in existing:
                    data[k].append(v)
                    existing.add(v)
                    added += 1
    
    if bad:
        print(f"⚠️ {len(bad)} bad refs: {bad[:5]}")
    
    if added > 0:
        with open(XREF, "w") as f:
            json.dump(data, f, separators=(",",":"))
        
        os.chdir(REPO)
        subprocess.run(["git","add","-A"], check=True)
        subprocess.run(["git","commit","-m",f"BTE: cross-refs +{added} (batch {batch_num})"], check=True)
        subprocess.run(["git","push","origin","main"], check=True)
        print(f"✅ Batch {batch_num}: +{added} entries. Total: {len(data)}")
    else:
        print(f"Batch {batch_num}: no new entries")

if __name__ == "__main__":
    main()
