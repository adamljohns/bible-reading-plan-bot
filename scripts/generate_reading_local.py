#!/usr/bin/env python3
"""
generate_reading_local.py — Author one day's MOOP daily reading via the LOCAL
LM Studio model, ONE WATCH PER CALL (reliable, bounded), then assemble.

Why watch-by-watch: a single ~27K-char request to the local MoE model truncated
~3/4 of the time. Five small focused calls each complete reliably. It also lets
each prompt carry only a STRUCTURAL skeleton (not the full canonical prose), which
prevents the model from copying example content, and a strict "render only this
passage" guard that prevents cross-passage scripture leakage.

Content flows model->file; only a short status line is printed.

USAGE
    python3 scripts/generate_reading_local.py 2026-03-05
    python3 scripts/generate_reading_local.py 2026-03-05 --model qwen/qwen3.6-35b-a3b --port 1234
"""
import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"
PASSAGES = Path("/tmp/backfill-passages.json")
MONTHS = ["", "January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
SEP = "⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻"

# Per-watch structural spec. order matters.
WATCHES = [
    {"key": "wisdom", "passage": "wisdom",
     "header": "🌅 0600 Morning Wisdom",
     "summary": "🧭 Context Summary",
     "refl": "🛡️ Reflection for a REAL MAN — {TRAIT}",
     "traitset": "a fitting one- or two-word virtue drawn from the passage (e.g. Treasures Wisdom, Walks Uprightly, Receives Correction)",
     "prayer": "🙏 Prayer", "close": "⚓ Helm Command:", "extra": ""},
    {"key": "first", "passage": "first",
     "header": "🕖 0700 First Watch — The Husband's Post",
     "summary": "🗺️ Briefing Summary",
     "refl": "❤️ Reflection for Your Wife — H.A.P.P.Y. Husband — {TRAIT}",
     "traitset": "exactly one of: Honest, Abiding, Protecting, Providing, Yielding",
     "prayer": "🙏 Prayer from the Stateroom", "close": "⚓ Helm Command:",
     "extra": "Speak to Adam's marriage to his wife Maria."},
    {"key": "second", "passage": "second",
     "header": "🕚 1100 Second Watch — The Father's Charge",
     "summary": "🗺️ Field Notes",
     "refl": "👨‍👧 Reflection for Your Children — F.U.L.F.I.L.L.E.D. Father — {TRAIT}",
     "traitset": "exactly one of: Faithful, Understanding, Leading, Forgiving, Instructing, Loving, Listening, Encouraging, Disciplining",
     "prayer": "🙏 Prayer from the Wardroom", "close": "⚓ Rudder Steer:",
     "extra": "Touch each child by name: Gideon (19), Boaz (14), Shiloh (5)."},
    {"key": "third", "passage": "third",
     "header": "🕒 1500 Third Watch — The Citizen's Stand",
     "summary": "🛰️ Situation Report",
     "refl": "🛡️ Reflection for a R.E.S.O.L.U.T.E. Citizen — {TRAIT}",
     "traitset": "exactly one of: Responsible, Engaged, Steadfast, Obedient, Loyal, Upright, Trustworthy, Enduring",
     "prayer": "🙏 Prayer from the Bridge", "close": "⚓ Rudder Steer:",
     "extra": "The reflection has THREE sub-paragraphs headed exactly 'Fredericksburg (local)', 'Virginia (state)', 'United States (nation)'. After the Personal Application place '🦅 This Day in American History — {MD}' with two accurate, well-documented historical events you are confident are real and correctly dated. Prefer edifying, encouraging, providential events (courage, faith, sacrifice, founding virtue, godly men and their deeds). When the honest event for this date is tragic or dark, give it a REDEMPTIVE spin — frame it under God's sovereignty, the call to repentance, or enduring hope. NEVER frame history through a social-justice, grievance, victimhood, or 'woke' lens."},
    {"key": "peace", "passage": "peace",
     "header": "🌙 2100 Evening Peace",
     "summary": None,
     "refl": "🌾 Reflection for a Man at Home and in Community",
     "traitset": None,
     "prayer": "🙏 Prayer from the Stateroom", "close": "⚓ Rudder Steer:",
     "extra": "No summary block and no Personal Application bullets. After the scripture and a ⸻ rule, write the 🌾 reflection weaving the three roles in three short paragraphs (one each beginning 'As a HAPPY husband,', 'As a FULFILLED father,', 'As a RESOLUTE citizen,'), then the prayer, then the rudder steer."},
]

VOICE = (
    "VOICE LOCKS: direct, masculine, Reformed (1689 LBCF), military-pastoral; address the reader as "
    "'brother' several times. Capitalize EVERY pronoun referring to God EVERYWHERE, including inside the "
    "quoted scripture text (He, Him, His, Himself, You, Your, Yours, Me, My, Mine, Who) — even in Psalms "
    "addressed to God. Divine name is 'the LORD' "
    "— NEVER 'Yahweh'. Em-dashes SPARINGLY; use commas at least half the time. Concrete actions over "
    "ornament. Render scripture faithfully and lightly modernized; POETRY in sense-lines, NARRATIVE in "
    "clean prose; NO verse numbers.\n"
    "WORLDVIEW: This is explicitly complementarian and patriarchal traditional Reformed content that "
    "celebrates and promotes biblical manhood — male headship, godly fatherhood, the protective and "
    "providing duties of a husband, and a man's covenant responsibility before God. Promote that vision "
    "warmly and without apology. Do NOT inject modern social-justice, egalitarian, feminist, 'woke', or "
    "progressive-political framing of any kind, and do not hedge or soften the patriarchal vision."
)


def build_watch_messages(w, ref, month, daynum):
    system = (
        "You are a Reformed Baptist pastor-writer composing ONE section of a daily devotional for a "
        "Marine-veteran father. You write reverent, wholesome content. Output ONLY the finished markdown "
        "for this one section — no preamble, no commentary, no code fences, no reasoning, no notes."
    )
    parts = []
    parts.append(f"Write ONE watch of a daily Bible reading. Output ONLY its markdown, starting with the exact header line below and ending with the {w['close']} line.\n")
    parts.append("EXACT SECTION ORDER:")
    parts.append(f"1. Header line, exactly: {w['header']}")
    parts.append("2. A one-sentence intro.")
    parts.append(f"3. A line exactly: 📖 Scripture — {ref}")
    parts.append(f"4. The scripture text of {ref} ONLY. Render only this reference. Do NOT import text from any other passage.")
    parts.append("5. A line with a single ⸻ character.")
    if w["summary"]:
        parts.append(f"6. A line exactly: {w['summary']}\n   then 2-4 sentences placing the passage.")
        parts.append("7. A line with a single ⸻ character.")
    trait_line = w["refl"]
    if w["traitset"]:
        parts.append(f"8. The reflection header exactly in this form: {trait_line}  (choose {w['traitset']} as the trait, fitting THIS passage).")
    else:
        parts.append(f"8. The reflection header exactly: {trait_line}")
    parts.append("9. 2-4 paragraphs of reflection in the voice below.")
    if w["key"] != "peace":
        parts.append("10. A line exactly: ⛏️ Personal Application — {same trait}  then four '• ' bulleted concrete actions.")
    parts.append(f"11. The prayer: a line exactly '{w['prayer']}' then a Trinitarian prayer that opens to 'Father', includes a line beginning 'By the power of Your Holy Spirit', and closes 'In the name of Jesus Christ, my Lord and Commander, ...' then 'Amen.'")
    parts.append(f"12. A final line beginning '{w['close']}' with a one-line nautical imperative.")
    if w["extra"]:
        parts.append("\nWATCH-SPECIFIC: " + w["extra"].replace("{MD}", f"{month} {daynum}"))
    parts.append("\n" + VOICE)
    parts.append("\nWrite ORIGINAL prose for THIS passage. Do not reuse phrasing from any prior reading. Begin now with the header line.")
    return [{"role": "system", "content": system}, {"role": "user", "content": "\n".join(parts)}]


def call_llm(messages, model, port, max_tokens=4000, temperature=0.6, timeout=420):
    payload = {"model": model, "messages": messages, "temperature": temperature,
               "max_tokens": max_tokens, "stream": False}
    req = urllib.request.Request(
        f"http://localhost:{port}/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]


def clean_watch(text, header):
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = text.strip()
    text = re.sub(r"^```(?:markdown|md)?\s*\n", "", text)
    text = re.sub(r"\n```\s*$", "", text)
    # trim anything before the header emoji line
    idx = text.find(header[:6])
    if idx > 0:
        text = text[idx:]
    return text.strip()


def normalize_prayer_header(body, prayer_label):
    """The local model is sloppy with the prayer-header emoji; force the
    canonical label on the short 'Prayer' header line nearest above 'Amen'."""
    lines = body.split("\n")
    amen_i = next((i for i, l in enumerate(lines) if l.strip().startswith("Amen")), None)
    if amen_i is None:
        return body
    for i in range(amen_i, -1, -1):
        s = lines[i].strip()
        if "Prayer" in s and len(s) < 40:
            lines[i] = prayer_label
            break
    return "\n".join(lines)


def watch_valid(text, w):
    return (w["header"][:6] in text
            and "📖 Scripture" in text
            and "By the power of Your Holy Spirit" in text
            and "Amen." in text
            and "⚓" in text
            and "Yahweh" not in text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("date")
    ap.add_argument("--model", default="qwen3.6-35b-a3b")
    ap.add_argument("--port", default="1235")
    args = ap.parse_args()

    passages = json.loads(PASSAGES.read_text())
    if args.date not in passages:
        sys.exit(f"no passages for {args.date}")
    d = passages[args.date]
    dt = date.fromisoformat(args.date)
    month, daynum, weekday = MONTHS[dt.month], dt.day, dt.strftime("%A")

    header = (f"MOOP's 2026 Daily Bible Readings\n"
              f"Document {dt.month} of 12; for the month of {month}\n\n"
              f"{weekday}, {month} {daynum}, 2026\n")

    sections = [header.rstrip()]
    print(f"[{args.date}] generating watch-by-watch via {args.model} :{args.port}", flush=True)
    for w in WATCHES:
        ref = d[w["passage"]]
        ok = False
        for attempt in range(1, 4):
            try:
                raw = call_llm(build_watch_messages(w, ref, month, daynum), args.model, args.port)
            except (urllib.error.HTTPError, urllib.error.URLError) as e:
                print(f"  [{w['key']}] attempt {attempt} error: {e}", flush=True)
                continue
            body = clean_watch(raw, w["header"])
            body = normalize_prayer_header(body, w["prayer"])
            if watch_valid(body, w):
                sections.append(body)
                print(f"  ✓ {w['key']} ({len(body):,} chars, attempt {attempt})", flush=True)
                ok = True
                break
            print(f"  ⚠ {w['key']} attempt {attempt} invalid, retrying", flush=True)
        if not ok:
            sys.exit(f"  ABORT: {w['key']} failed after 3 attempts — file not written")

    out = ("\n\n" + SEP + "\n\n").join(sections) + "\n"
    dest = READINGS / f"{args.date}.md"
    dest.write_text(out)

    wh = sum(out.count(h["header"][:6]) for h in WATCHES)
    tri = out.count("By the power of Your Holy Spirit")
    print(f"  ✓ wrote {dest.name}: {out.count(chr(10))+1} lines, {len(out):,} chars; "
          f"watch_headers={wh}/5 trinity={tri}/5 LORD={out.count('LORD')}")
    if wh < 5 or tri < 5:
        print("  ⚠ FINAL CHECK FAILED")
        sys.exit(2)


if __name__ == "__main__":
    main()
