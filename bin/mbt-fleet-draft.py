#!/usr/bin/env python3
"""mbt-fleet-draft.py <bookId> <chapter>

LOCAL drafting step of the MBT pipeline — runs entirely on the M5 Max via LM Studio
(OpenAI-compatible API on :1234). ZERO Claude/Anthropic tokens. A local model drafts
each verse as an MBT-style blend (text + amp + notes), anchored to the Strong's-tagged
Greek/Hebrew in the chapter kit. Claude then POLISHES the draft (the only Claude cost).

  python3 bin/mbt-chapter-kit.py 57 1      # assemble the source kit first
  python3 bin/mbt-fleet-draft.py  57 1     # local model drafts -> data/mbt-drafts/57_1.draft.json

Env:
  MBT_MODEL   LM Studio model id      (default: qwen2.5-32b-instruct)
  MBT_API     endpoint                (default: http://localhost:1234/v1/chat/completions)
  MBT_CHUNK   verses per call         (default: 5 — local models draft best in focused batches)
  MBT_TEMP    sampling temperature    (default: 0.35 — low, for translation fidelity)
"""
import json, os, re, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = os.environ.get("MBT_MODEL", "qwen2.5-32b-instruct")
API   = os.environ.get("MBT_API", "http://localhost:1234/v1/chat/completions")
CHUNK = int(os.environ.get("MBT_CHUNK", "5"))
TEMP  = float(os.environ.get("MBT_TEMP", "0.35"))

SYSTEM = """You are a Reformed Bible translator producing the "MOOP Bible Translation" (MBT) -- an ORIGINAL, copyright-safe English rendering. For each verse you receive two PUBLIC-DOMAIN sources: the Strong's-tagged KJV (each word's original-language number in [G####]/[H####] -- your anchor to the precise meaning) and the WEB (clean modern phrasing). Render each verse FRESH in your own words. NEVER copy a modern translation.

VOICE:
- Reverent, modern, readable English with the cadence of the classic translations; formal-equivalence lean (faithful to the original) but flowing, not wooden.
- Divine name: "the LORD" for YHWH. Capitalize pronouns for God/Christ (He, Him, His).
- Render the sense, not a word gloss. A verse may run a little longer than the source.

DEPTH (the heart of the method):
- Anchor every rendering to the original via the [G####]/[H####] tags. Where ONE original word carries layered meaning AND the good translations legitimately split between two genuinely good English words, fold BOTH in (a doublet, e.g. "urge or press"). Do this ONLY where the original earns it -- never decorate, never pad. Most words take a single good word.
- Surface real wordplay the original contains.

OUTPUT -- STRICT JSON ONLY, nothing before or after:
{"verses": {"<n>": {"text": "...", "amp": "...", "notes": "..."}, ...}}
- text  = the MBT reading line (ALWAYS present).
- amp   = OPTIONAL amplified study form: the verse with bracketed original-language anchors, e.g. "...made effectual [energes (G1756) -- actively at work]...". Include only where it adds real depth; omit otherwise.
- notes = OPTIONAL 1-2 sentences of exegetical/cultural insight citing Strong's (e.g. G1756). Include only where genuinely illuminating.
Return ONLY the JSON object for the verses requested."""

# One few-shot example (Adam-approved Ruth) so the model sees target format + quality.
FEWSHOT_USER = """Draft MBT for Ruth 1, verses 16-16. Sources:

v16:
  KJV+Strongs: And Ruth said, Intreat[H6293] me not to leave[H5800] thee, or to return[H7725] from following after thee: for whither thou goest[H1980], I will go[H1980]; and where thou lodgest[H3885], I will lodge[H3885]: thy people[H5971] shall be my people, and thy God[H430] my God:
  WEB: Don't urge me to leave you, and to return from following you, for where you go, I will go; and where you stay, I will stay. Your people will be my people, and your God my God."""

FEWSHOT_ASSISTANT = json.dumps({"verses": {"16": {
  "text": "Do not urge or press me to leave you behind, or to turn back from following you. For wherever you go, I will go; and wherever you stay, I will stay. Your people will be my people, and your God my God.",
  "amp": "Do not urge or press me [paga' (H6293) -- to fall upon, press, entreat] to leave you behind; for where you go, I will go, and where you stay [lun (H3885) -- to lodge, settle, remain] I will stay -- your people my people, and your God [Elohim (H430)] my God.",
  "notes": "paga' (H6293) holds both the insistence and the pleading, so 'urge or press' folds in both. halak (H1980, go) and lun (H3885, lodge/stay) form a go-vs-stay merism kept crisp -- 'stay' over 'lodge' preserves the antithesis."
}}}, ensure_ascii=False)


def post(messages, max_tokens):
    body = json.dumps({"model": MODEL, "messages": messages, "temperature": TEMP,
                       "max_tokens": max_tokens, "stream": False}).encode()
    req = urllib.request.Request(API, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)


def extract_json(text):
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    start = text.find("{")
    if start < 0:
        raise ValueError("no JSON object in model output")
    depth, instr, esc = 0, False, False
    for i in range(start, len(text)):
        c = text[i]
        if instr:
            if esc: esc = False
            elif c == "\\": esc = True
            elif c == '"': instr = False
        else:
            if c == '"': instr = True
            elif c == "{": depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(text[start:i+1])
    raise ValueError("unbalanced JSON in model output")


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: mbt-fleet-draft.py <bookId> <chapter>")
    book_id, chapter = int(sys.argv[1]), int(sys.argv[2])
    kit = json.load(open(os.path.join(ROOT, "data", "mbt-kits", f"{book_id}_{chapter}.kit.json")))
    name, verses = kit["bookName"], kit["verses"]
    vnums = sorted(verses.keys(), key=int)

    print(f"Drafting {name} {chapter} ({len(vnums)} verses) on LOCAL model '{MODEL}' "
          f"in chunks of {CHUNK}  [0 Claude tokens]")
    drafted, total_completion, t0 = {}, 0, time.time()
    for i in range(0, len(vnums), CHUNK):
        batch = vnums[i:i+CHUNK]
        lines = [f"Draft MBT for {name} {chapter}, verses {batch[0]}-{batch[-1]}. Sources:\n"]
        for v in batch:
            e = verses[v]
            lines.append(f"v{v}:\n  KJV+Strongs: {e['kjv_strongs']}\n  WEB: {e['web']}\n")
        messages = [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": FEWSHOT_USER},
            {"role": "assistant", "content": FEWSHOT_ASSISTANT},
            {"role": "user", "content": "\n".join(lines)},
        ]
        ct = time.time()
        try:
            resp = post(messages, max_tokens=900 * len(batch))
            content = resp["choices"][0]["message"]["content"]
            obj = extract_json(content)
            got = obj.get("verses", obj)
            for v in batch:
                if str(v) in got:
                    drafted[str(v)] = got[str(v)]
            usage = resp.get("usage", {})
            total_completion += usage.get("completion_tokens", 0)
            print(f"  v{batch[0]}-{batch[-1]}: {len([v for v in batch if str(v) in got])}/{len(batch)} "
                  f"ok  ({time.time()-ct:.0f}s, {usage.get('completion_tokens','?')} local tok)")
        except Exception as ex:
            print(f"  v{batch[0]}-{batch[-1]}: FAILED -> {ex}")

    out = {"book": book_id, "bookName": name, "chapter": chapter,
           "version": "MBT v0.4-fleetdraft", "model": MODEL,
           "style": "LOCAL fleet draft (Qwen on M5 Max) -- awaiting Claude polish",
           "sources": ["KJV1769+Strongs", "WEB"], "verses": drafted}
    outdir = os.path.join(ROOT, "data", "mbt-drafts")
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, f"{book_id}_{chapter}.draft.json")
    json.dump(out, open(outpath, "w"), ensure_ascii=False, indent=1)
    elapsed = time.time() - t0
    print(f"\nDrafted {len(drafted)}/{len(vnums)} verses in {elapsed:.0f}s on the M5 Max.")
    print(f"Local completion tokens: ~{total_completion} (Claude tokens: 0)")
    print(f"  -> {outpath}")

if __name__ == "__main__":
    main()
