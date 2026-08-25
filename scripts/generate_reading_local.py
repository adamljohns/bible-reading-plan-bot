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

# One-title prayer closes (PJG-0810-PRAYSWEEP1 / rewrite-rules item 8).
# NEVER emit "Jesus Christ, my Lord Jesus Christ" or "my Lord and Commander".
PRAYER_CLOSES = {
    "wisdom": "In Jesus' name, I pray. Amen.",
    "first": "In the name of Jesus Christ, I pray. Amen.",
    "second": "Through Christ my Savior, I pray. Amen.",
    "third": "In the name of the risen Lord Jesus, I pray. Amen.",
    "peace": "For the sake of Christ our King, I pray. Amen.",
}

# Household birthdays for age math (do not hardcode stale ages).
BIRTHDAYS = {
    "Gideon": date(2006, 8, 16),
    "Boaz": date(2011, 7, 19),
    "Shiloh": date(2021, 1, 13),
}


def age_on(name: str, on: date) -> int:
    b = BIRTHDAYS[name]
    years = on.year - b.year
    if (on.month, on.day) < (b.month, b.day):
        years -= 1
    return years


# Per-watch structural spec. order matters.
WATCHES = [
    {"key": "wisdom", "passage": "wisdom",
     "header": "🌅 0600 Morning Wisdom",
     "summary": "🧭 Context Summary",
     "refl": "🛡️ Reflection for a REAL MAN — {TRAIT}",
     "traitset": "exactly one REAL MAN spine item that fits THIS passage: Rejects Passivity, Engages Intentionally, Accepts Responsibility, Leads Courageously, Manages Faithfully, Accounts Accurately, Never Quits — NOT a unisex virtue such as Trusts God / Studies Scripture / Is Grateful",
     "prayer": "🙏 Prayer", "close": "🛡️ Watch Charge:", "extra": ""},
    {"key": "first", "passage": "first",
     "header": "🕖 0700 First Watch — The Husband's Post",
     "summary": "🗺️ Briefing Summary",
     "refl": "❤️ Reflection for Your Wife — H.A.P.P.Y. Husband — {TRAIT}",
     "traitset": "exactly one of: Honest, Abiding, Protecting, Providing, Yielding",
     "prayer": "🙏 Prayer", "close": "🛡️ Watch Charge:",
     "extra": "Speak to Adam's marriage to his wife Maria. In reflection, address the HUSBAND as 'you' "
              "(the man reading). Maria is protected/served — never the headship addressee. "
              "NEVER write 'As the head of your home, Maria' or any line that makes Maria the 'you' of headship."},
    {"key": "second", "passage": "second",
     "header": "🕚 1100 Second Watch — The Father's Charge",
     "summary": "🗺️ Field Notes",
     "refl": "👨‍👧 Reflection for Your Children — F.U.L.F.I.L.L.E.D. Father — {TRAIT}",
     "traitset": "exactly one of: Faithful, Understanding, Leading, Forgiving, Instructing, Loving, Listening, Encouraging, Disciplining",
     "prayer": "🙏 Prayer", "close": "🛡️ Watch Charge:",
     "extra": "VOICE LOCK PJG-0821-FAT1: this reflection is for the FATHER to read ABOUT his children — "
              "never a letter TO them. NEVER open with 'Dear Gideon' / 'listen closely to your father'. "
              "Address Adam as 'you'. Name each child in the third person, correctly gendered: SONS Gideon "
              "({GIDEON_AGE}) and Boaz ({BOAZ_AGE}); DAUGHTER Shiloh ({SHILOH_AGE}). Use she/her for Shiloh "
              "and aim her guidance at godly young womanhood (gentleness, modesty, a quiet and gentle spirit), "
              "never manhood. When grouping all three, say 'sons and daughter' or 'children', never 'sons'. "
              "Compute ages from birthdays only; do not invent ages. Prayer close MUST be "
              "'Through Christ my Savior, I pray. Amen.' (my, not our)."},
    {"key": "third", "passage": "third",
     "header": "🕒 1500 Third Watch — The Citizen's Stand",
     "summary": "🛰️ Situation Report",
     "refl": "🛡️ Reflection for a R.E.S.O.L.U.T.E. Citizen — {TRAIT}",
     "traitset": "exactly one of: Responsible, Engaged, Steadfast, Obedient, Loyal, Upright, Trustworthy, Enduring",
     "prayer": "🙏 Prayer", "close": "🛡️ Watch Charge:",
     "extra": "The reflection has THREE sub-paragraphs headed exactly 'Fredericksburg (local)', 'Virginia (state)', 'United States (nation)'. After the Personal Application place '🦅 This Day in American History — {MD}' with two accurate, well-documented historical events you are confident are real and correctly dated. Prefer edifying, encouraging, providential events (courage, faith, sacrifice, founding virtue, godly men and their deeds). When the honest event for this date is tragic or dark, give it a REDEMPTIVE spin — frame it under God's sovereignty, the call to repentance, or enduring hope. NEVER frame history through a social-justice, grievance, victimhood, or 'woke' lens. Do NOT choose civil-rights-movement, racial-liberation, feminist, labor-agitation, or protest-movement events or figures (such as Malcolm X, marches, or 'liberation' movements). Choose instead from founding and constitutional milestones, military valor and sacrifice, exploration and the frontier, invention and honest industry, Christian missions and revival, conservation of God's creation, or acts of personal courage and faith. Verify the date and facts are correct."},
    {"key": "peace", "passage": "peace",
     "header": "🌙 2100 Evening Peace",
     "summary": None,
     "refl": "🌾 Reflection for a Man of God",
     "traitset": None,
     "prayer": "🙏 Prayer", "close": "🛡️ Watch Charge:",
     "extra": "PJG-0824-PEACE1: header exactly '🌾 Reflection for a Man of God'. Reflection is pastor-to-the-man: you/your only — ban I/me/my/mine as the reflection speaker. Prayer stays first person (I/me/my) to God; one complete sentence per line; last line exactly 'For the sake of Christ our King, I pray. Amen.' No summary block and no Personal Application bullets. After the scripture and a ⸻ rule, write the 🌾 reflection weaving the three roles in three short paragraphs (one each beginning 'As a HAPPY husband,', 'As a FULFILLED father,', 'As a RESOLUTE citizen,'), then the prayer, then the Watch Charge. Diction = what Adam / a pastor would say aloud. Ban comic-book 'the Avenger' and do not repeat 'the avenger' in the reflection (say enemy/foe). Ban 'O the LORD' — write 'O LORD, our Lord'."},
]

VOICE = (
    "VOICE LOCKS: direct, masculine, Reformed (1689 LBCF), military-pastoral; address the reader as "
    "'brother' several times. Capitalize EVERY pronoun referring to God EVERYWHERE, including inside the "
    "quoted scripture text (He, Him, His, Himself, You, Your, Yours, Me, My, Mine, Who) — even in Psalms "
    "addressed to God. DIVINE NAME FIDELITY: where the underlying text has the covenant name YHWH "
    "(rendered 'the LORD' in small-caps tradition / KJV), you MUST render it 'the LORD' — never "
    "substitute an epithet like 'the Most High', 'the Eternal', 'the Almighty', or 'the Everlasting' "
    "for the personal covenant name. Reserve 'God' for Elohim, 'the Most High' for Elyon, 'the Almighty' "
    "for El-Shaddai, and use those ONLY where the original actually has them. NEVER write 'Yahweh'. "
    "Em-dashes SPARINGLY; use commas at least half the time. Concrete actions over "
    "ornament. SCRIPTURE RENDERING: render every passage to be MOST TRUE TO THE ORIGINAL MEANING while "
    "LIGHTLY AMPLIFIED FOR APPLICATION — faithful first, then illumined. Capture the full sense (never "
    "wooden word-for-word literalism, never loose paraphrase that drifts from the meaning); let the "
    "wording land with the interpretive clarity that drives a man toward obedience, and never soften the "
    "hard edge of the text. POETRY in sense-lines, NARRATIVE in clean prose; NO verse numbers.\n"
    "FRESH LANGUAGE: write THIS watch's closing imperative (Watch Charge only) and its "
    "reflection rooted in the SPECIFIC images, names, and scene of today's passage. Do NOT reach for "
    "stock closers — in particular NEVER use the worn phrase 'hold the line against the tide of "
    "compromise' or its close variants; coin a fresh nautical/military image from this text instead.\n"
    "REFLECTION OPENER VARIETY: Do NOT default to 'Brother, look', 'Brother, look at', 'look to', "
    "or 'look closely'. Open naturally with the text's claim, tension, scene, or question, or choose "
    "a fitting verb such as consider, notice, think about, weigh, remember, trace, picture, hear, "
    "mark, or reflect on. Do not repeat the same imperative opener used on the adjacent reading day. "
    "Use 'look' only when literal sight, vision, beholding, watching, eyes, or seeing is integral to "
    "the passage; even then, vary the syntax rather than relying on a stock formula.\n"
    "WORLDVIEW: This is explicitly patriarchal, biblical-manhood Reformed content (1689 LBCF) that "
    "celebrates and promotes biblical manhood — male headship, godly fatherhood, the protective and "
    "providing duties of a husband, and a man's covenant responsibility before God. Promote that vision "
    "warmly and without apology. This is biblical PATRIARCHY (father-rule under God), stronger than and "
    "surpassing mere 'complementarianism', and it explicitly REJECTS feminism and egalitarianism as "
    "errors to be named, not accommodated. Do NOT inject modern social-justice, egalitarian, feminist, 'woke', or "
    "progressive-political framing of any kind, and do not hedge or soften the patriarchal vision. "
    "Avoid loaded sociological vocabulary such as 'marginalized', 'privilege', 'systemic', 'social "
    "justice', 'oppressed classes', or 'underrepresented' even when describing a biblical outcast — use "
    "plain, timeless words like lowly, outcast, rejected, despised, or downtrodden instead. "
    "Do NOT use egalitarian framing such as 'the gospel transcends gender/ethnic/social barriers', "
    "'neither male nor female' applied to flatten roles, or any language that dissolves the distinction "
    "between men's and women's God-given roles. When the gospel reaches an outsider (a Samaritan, a "
    "Gentile, a sinner), frame it as God's sovereign grace reaching the undeserving — never as 'breaking "
    "down barriers' — and keep male headship and patriarchal role distinctions fully intact.\n"
    "COVENANT & FULFILLMENT: This is confessionally Reformed covenant theology, NOT dispensational. "
    "Christ is the true Israel and the fulfillment of every promise made to Israel (2 Cor 1:20); the "
    "church of believers from every nation is the Israel of God (Gal 6:16; Rom 9:6-8). The modern "
    "secular nation-state of Israel is an ordinary geopolitical state, NOT a covenant people or a "
    "locus of unfulfilled redemptive promise; never frame it as God's chosen nation and never import "
    "Christian-Zionist or dispensational expectation. Rabbinic (Talmudic) Judaism is a post-Temple "
    "religion that rejects Jesus as Messiah and is therefore not the faith of Moses and the prophets, "
    "which pointed to Christ (John 5:46); where it is in view, answer it with the gospel and a longing "
    "for its people's salvation (Rom 10:1), never ethnic contempt.\n"
    "SEXUAL ETHICS: Marriage is the one-flesh union of one man and one woman, grounded in creation "
    "(Gen 1-2; Matt 19). Homosexual practice and LGBTQ ideology are rebellion against God's created "
    "order, condemned by the Law and the Apostles (Lev 18:22; Rom 1:24-27; 1 Cor 6:9-11) and answered "
    "by the gospel that washes and remakes sinners (1 Cor 6:11). Locate the source of this rebellion "
    "where Scripture does, in the suppression of truth, idolatry, and the debased mind of a fallen "
    "world (Rom 1), NOT in any ethnic group or bloodline.\n"
    "SCOPE GUARD: Raise the covenant/Israel and sexual-ethics themes ONLY when today's passage "
    "naturally raises them; never force them into a reading that does not call for them.\n"
    "MEN-ONLY APPS (PJG-0816-MEN1 / rewrite-rules item 15 — HARD from 2026-08-17): Personal Application "
    "is for men. Unisex virtue belongs in another devotion, not this Watch. If a bullet would preach "
    "unchanged to a women's study, rewrite it on the REAL MAN spine before ship.\n"
    "REFLECTION PERSON (PJG-0824-PEACE1 — HARD from 2026-08-25): Reflections are FOR the man and "
    "read TO him. His voice is the pastor. Write you/your. Ban I/me/my/mine as the reflection speaker "
    "on ALL watches. Prayer stays I/me/my to God. Peace heading is Reflection for a Man of God. "
    "Ban comic-book the Avenger in reflection (say enemy/foe). Ban 'O the LORD' — write 'O LORD, our Lord'."
)


def build_watch_messages(w, ref, month, daynum, on_date: date):
    system = (
        "You are a Reformed Baptist pastor-writer composing ONE section of a daily devotional for a "
        "Marine-veteran father. You write reverent, wholesome content. Output ONLY the finished markdown "
        "for this one section — no preamble, no commentary, no code fences, no reasoning, no notes."
    )
    g_age = age_on("Gideon", on_date)
    b_age = age_on("Boaz", on_date)
    s_age = age_on("Shiloh", on_date)
    close_line = PRAYER_CLOSES[w["key"]]
    parts = []
    parts.append(f"Write ONE watch of a daily Bible reading. Output ONLY its markdown, starting with the exact header line below and ending with the {w['close']} line.\n")
    parts.append("EXACT SECTION ORDER:")
    parts.append(f"1. Header line, exactly: {w['header']}")
    parts.append("2. Then ONE original sentence introducing today's theme — write the actual sentence; do NOT echo this instruction text.")
    parts.append(f"3. A line exactly: 📖 Scripture — {ref}")
    parts.append(
        f"4. The scripture text of {ref} ONLY. Named passage owns Scripture. "
        "ONE translation pass, BTE NKJV primary. Do NOT dump a second English dress "
        "of the same verse (e.g. soft answer then gentle answer). Do NOT import "
        "unlabeled verses from any other chapter. Cross-refs belong in Context/Reflection only."
    )
    parts.append("5. A line with a single ⸻ character.")
    if w["summary"]:
        parts.append(f"6. A line exactly: {w['summary']}\n   then 2-4 sentences placing the passage.")
        parts.append("7. A line with a single ⸻ character.")
    trait_line = w["refl"]
    if w["traitset"]:
        parts.append(f"8. The reflection header exactly in this form: {trait_line}  (choose {w['traitset']} as the trait, fitting THIS passage).")
    else:
        parts.append(f"8. The reflection header exactly: {trait_line}")
    parts.append("9. 2-4 paragraphs of reflection in the voice below. PJG-0824-PEACE1: address the man as you/your. Do NOT write I/me/my/mine as the reflection speaker. Prayer (step 11) stays I/me/my to God.")
    if w["key"] != "peace":
        parts.append("10. A line exactly: ⛏️ Personal Application — {same trait}  then EXACTLY THREE '• ' bulleted concrete actions (never 4+). "
                     "Each bullet must be rooted in a SPECIFIC image, name, command, or scene from TODAY's passage "
                     "(not generic spiritual advice that could attach to any text), and name a concrete, doable step. "
                     "MEN-ONLY REAL MAN GATE (rewrite-rules item 15 / PJG-0816-MEN1 — HARD from 2026-08-17): "
                     "every Personal Application bullet must be specifically for men. Prefer the REAL MAN spine as the MOVE: "
                     "Reject passivity · Engage consistently/intentionally · Accept responsibility · Lead courageously · "
                     "Manage faithfully · Account accurately · Never quit. "
                     "QA: if a bullet would preach unchanged to a women's Bible study, it FAILS — rewrite. "
                     "Fail class: generic trust-God / Strong Tower / unisex virtue (women should trust God too). "
                     "Husband/father nouns are not enough if the MOVE is still a unisex devotion. "
                     "PROVEN overlap: do not target traits women already commonly carry (Principal example: open / honest). "
                     "Exhort what men must be told to become. Role-aware still holds (husband / father / citizen by watch). "
                     "Wisdom uses REAL MAN, not a gender-neutral virtue as the application heading.")
    parts.append(
        f"11. The prayer: a line exactly '{w['prayer']}' then a PERSONAL first-person prayer (I/me/my only — "
        f"never we/us/our as the praying subject; never 'Brother Adam' or any self-vocative; never 'this father'). "
        f"Open to 'Father', include a line beginning 'By the power of Your Holy Spirit', write ONE complete sentence per line "
        f"(item 9 — do not glue sentences), and close with EXACTLY: "
        f"'{close_line}' — one Christ title only, last line. BANNED closes: 'my Lord Jesus Christ', 'my Lord and Commander', "
        f"any double full Christ title stack, 'we pray'."
    )
    parts.append(f"12. A final line beginning '{w['close']}' with a one-line charge imperative (not Helm/Rudder/Course Set).")
    if w["extra"]:
        extra = (w["extra"]
                 .replace("{MD}", f"{month} {daynum}")
                 .replace("{GIDEON_AGE}", str(g_age))
                 .replace("{BOAZ_AGE}", str(b_age))
                 .replace("{SHILOH_AGE}", str(s_age)))
        parts.append("\nWATCH-SPECIFIC: " + extra)
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
    # Reject obvious instruction-text leaks so the watch retries instead of
    # shipping the prompt skeleton as content (e.g. "A one-sentence intro").
    leaks = ["A one-sentence intro", "do NOT echo", "write the actual sentence",
             "EXACT SECTION ORDER", "VOICE LOCKS", "{TRAIT}", "{same trait}"]
    if any(lk in text for lk in leaks):
        return False
    # PJG-0021: retry stock reflection openings before they enter authored content.
    # Sight-integral exceptions are judged in editorial QA; the generator should
    # not treat the old formula as a default under any watch.
    if re.search(r"(?im)^\s*(?:Adam,\s*)?Brother,\s+look(?:\s+(?:at|to|closely))?\b", text):
        return False
    # PJG-0821-FAT1: Second Watch is father-ABOUT-children, never a letter to them.
    if w["key"] == "second" and re.search(r"Dear Gideon|listen closely to your father", text, re.I):
        return False
    # PJG-0824-PEACE1: reflections are you/your; prayer stays I/me; no Marvel Avenger; no extra the.
    if re.search(r"O the LORD", text):
        return False
    if re.search(r"\bthe Avenger\b", text):
        return False
    if w["key"] == "peace" and "Reflection for a Man of God" not in text:
        return False
    refl_m = re.search(r"Reflection[^\n]*\n([\s\S]*?)(?=\n🙏|\nPrayer|\n⛏️|\nPersonal Application)", text)
    if refl_m:
        refl = refl_m.group(1)
        if re.search(r"(?m)^\s*(?:As a [A-Z0-9²³\.].*?,\s*)?(?:brother,\s*)?\bI\b", refl):
            return False
        if re.search(r"\bI find my\b|\bupon me\b|\bMy headship\b|\bI teach\b|\bI stand\b|\bI serve\b", refl):
            return False
        if re.search(r"\bthe avenger\b", refl, re.I):
            return False
    if w["key"] == "second" and re.search(r"Through Christ our Savior", text):
        return False
    # PJG-0810-PRAYSWEEP1 hard bans — refuse before file write.
    ban_res = [
        r"my Lord Jesus Christ",
        r"my Lord and Commander",
        r"Brother Adam",
        r"\bHelm Command\b",
        r"\bRudder Steer\b",
        r"\bCourse Set\b",
        r"Prayer from the (?:Stateroom|Wardroom|Bridge)",
        r"As the head of your home,\s*Maria",
    ]
    for pat in ban_res:
        if re.search(pat, text, re.I):
            return False
    # Prayer person: corporate subject banned (fail closed).
    pray_m = re.search(r"🙏[^\n]*\n([\s\S]*?)(?=\n🛡️|\n⚓|\Z)", text)
    if pray_m:
        pray = pray_m.group(1)
        if re.search(r"\b(we thank|we ask|we pray|Grant us|give this father)\b", pray, re.I):
            return False
        if re.search(r"\bBrother Adam\b|\bAdam,", pray):
            return False
    # Apps cap 3 (peace has none)
    if w["key"] != "peace":
        apps = re.findall(r"^[•\-]\s+\S", text, re.M)
        if len(apps) > 3:
            return False
    return (w["header"][:6] in text
            and "📖 Scripture" in text
            and "By the power of Your Holy Spirit" in text
            and "Amen." in text
            and ("🛡️ Watch Charge:" in text or "Watch Charge:" in text)
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

    header = (f"MOOP's 2026 Daily Bible Readings\n\n"
              f"{weekday}, {month} {daynum}, 2026\n")

    sections = [header.rstrip()]
    print(f"[{args.date}] generating watch-by-watch via {args.model} :{args.port}", flush=True)
    for w in WATCHES:
        ref = d[w["passage"]]
        ok = False
        for attempt in range(1, 4):
            try:
                raw = call_llm(build_watch_messages(w, ref, month, daynum, dt),
                               args.model, args.port)
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
