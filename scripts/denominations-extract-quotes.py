#!/usr/bin/env python3
"""Local-model quote extraction for a denomination's captured official sources.

  python3 scripts/denominations-extract-quotes.py <denom_id> [--model M]

For each snapshot in data/denominations/sources/<denom_id>/, finds passages
that touch a MOOP category (keyword windows), asks a LOCAL model on LM Studio
(http://127.0.0.1:1234, no cloud credits) to copy verbatim sentences stating
the body's official position, and validates every returned quote word for
word against the snapshot (same normalization as scripts/lib/denominations.js).

Writes data/denominations/proposals/<denom_id>.json. Proposals are not
evidence: a human/rule review copies validated proposals into
data/denominations/<id>.json, and the builder re-validates them. A model
quote that is not verbatim in the snapshot is kept with validated=false and
can never be used.
"""
import argparse, datetime, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LM = os.environ.get("LMSTUDIO_URL", "http://127.0.0.1:1234/v1/chat/completions")

CATS = {
    "scripture": ("the authority, inspiration or inerrancy of the Bible", r"scripture|bible|inerran|without (any mixture of )?error|infallib|word of god"),
    "christology": ("the person of Jesus Christ (God and man)", r"truly god|very god|fully god|fully man|incarnat|godhead and manhood"),
    "soteriology": ("salvation and justification (grace, faith, works)", r"justif|accounted righteous|saved by grace|by faith|salvation"),
    "gender": ("whether women are ordained or may be pastors", r"ordain|ordination|women|pastor/elder|limited to men|clergy rights"),
    "leadership": ("who may serve as pastor or elder, and who decides that", r"elder|overseer|pastor|local church matter|ordination of women"),
    "cultural": ("marriage and human sexuality", r"marriage|one man and one woman|sexual|homosex|two adult"),
    "denominational": ("whether the body affirms or forbids same-sex practice for members or clergy", r"homosex|same-sex|sexual orientation|practicing|cooperation with the convention"),
    "mission": ("the body's official mission statement", r"mission|great commission|make disciples|all nations"),
    "governance": ("whether the body's decisions bind local churches, or churches are autonomous", r"autonom|binding|authority over|connectional|trust clause|local church matter|sovereign"),
}
NRM = [("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"), (" ", " ")]

def nrm(s):
    for a, b in NRM: s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip().lower()

def validated(q, text):
    q2 = re.sub(r"^[\s.,;:\"']+|[\s.,;:\"']+$", "", nrm(q))
    return len(q2) >= 12 and q2 in nrm(text)

def windows(text, pattern, width=1400, cap=6):
    out, last = [], -10**9
    for m in re.finditer(pattern, text, re.I):
        if m.start() - last < width: continue
        last = m.start()
        out.append(text[max(0, m.start() - width // 2): m.start() + width // 2])
        if len(out) >= cap: break
    return out

def ask(model, body, topic, passage):
    prompt = (f"Passage from an official document of the {body}:\n\"\"\"\n{passage}\n\"\"\"\n\n"
              f"Copy, character for character, up to 3 complete sentences from the passage that state the body's "
              f"official position on {topic}. Do not paraphrase, shorten, fix or join sentences. Skip menu text, "
              f"headings and scripture references. If no sentence states a position on that topic, return an empty list.\n"
              f"Reply with JSON only: {{\"quotes\": [\"...\"]}}")
    req = {"model": model, "temperature": 0, "max_tokens": 900,
           "messages": [{"role": "system", "content": "You extract exact quotations. /no_think"}, {"role": "user", "content": prompt}]}
    r = urllib.request.urlopen(urllib.request.Request(LM, data=json.dumps(req).encode(), headers={"Content-Type": "application/json"}), timeout=300)
    content = json.load(r)["choices"][0]["message"]["content"] or ""
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.S)
    m = re.search(r"\{.*\}", content, re.S)
    try: return [q for q in json.loads(m.group(0)).get("quotes", []) if isinstance(q, str)] if m else []
    except Exception: return []

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("denom"); ap.add_argument("--model", default="gemma-4-31b-it")
    ap.add_argument("--body", default=None)
    ap.add_argument("--extra", action="append", default=[], help="CATEGORY=REGEX: only run these targeted windows (for passages the default windows skipped); results are appended to the existing proposals file")
    a = ap.parse_args()
    extra = [x.split("=", 1) for x in a.extra]
    d = os.path.join(ROOT, "data", "denominations", "sources", a.denom)
    body = a.body or a.denom.upper()
    props = []
    for f in sorted(os.listdir(d)):
        if not f.endswith(".txt"): continue
        slug = f[:-4]; text = open(os.path.join(d, f)).read()
        meta = json.load(open(os.path.join(d, slug + ".meta.json")))
        jobs = [(c, CATS[c][0], rx) for c, rx in extra] if extra else [(c, t, rx) for c, (t, rx) in CATS.items()]
        for cat, topic, pat in jobs:
            for w in windows(text, pat):
                for q in ask(a.model, body, topic, w):
                    props.append({"source": slug, "url": meta["url"], "category": cat, "quote": q.strip(),
                                  "validated": validated(q, text), "model": a.model, "endpoint": "lmstudio-local"})
            print(f"{slug} {cat}: {sum(1 for p in props if p['source']==slug and p['category']==cat)} proposals", file=sys.stderr)
    out_file = os.path.join(ROOT, "data", "denominations", "proposals", a.denom + ".json")
    if extra and os.path.exists(out_file): props = json.load(open(out_file))["proposals"] + props
    seen, uniq = set(), []
    for p in props:
        k = (p["source"], p["category"], nrm(p["quote"]))
        if k not in seen: seen.add(k); uniq.append(p)
    out = os.path.join(ROOT, "data", "denominations", "proposals"); os.makedirs(out, exist_ok=True)
    doc = {"denomination": a.denom, "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
           "model": a.model, "endpoint": "LM Studio 127.0.0.1:1234 (local; no cloud credits)",
           "note": "Proposals only. Evidence rows are reviewed copies of validated proposals; the builder re-validates every quote.",
           "proposals": uniq}
    json.dump(doc, open(os.path.join(out, a.denom + ".json"), "w"), indent=1, ensure_ascii=False)
    print(f"{a.denom}: {len(uniq)} proposals, {sum(p['validated'] for p in uniq)} verbatim-valid")

if __name__ == "__main__":
    main()
