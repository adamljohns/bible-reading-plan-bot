#!/usr/bin/env python3
"""Local-LLM pastor extraction — the zero-cloud-usage enrichment worker.

Reads a batch file from select-enrichment-batch.js, fetches each church's
website (homepage + likely leadership pages), asks a LOCAL model (llama-server
on :1235, falling back to LM Studio on :1234) to extract the pastor roster,
and emits a merge-pastor-enrichments.js-compatible JSON array.

HONESTY ENFORCEMENT (the reason a small local model can be trusted here):
every extracted name must pass MECHANICAL validation —
  1. the name must appear VERBATIM (whitespace/case-normalized) in the fetched
     page text, so the model cannot hallucinate a name that isn't on the page;
  2. junk-shape rules identical to looksJunkName() in merge-pastor-enrichments.js
     (2-5 tokens, <=32 chars, no ministry-word tail, starts uppercase, no markup);
  3. a lead whose role looks non-lead (youth/kids/worship/executive/...) is
     demoted to other_pastors — never published as THE pastor.
Anything failing a gate becomes null / is dropped. The merge script re-checks
everything again (defense in depth) and a typically-female first name on the
lead is HELD for manual MOOP-rubric review there.

Usage: local-pastor-extract.py BATCH.json OUT.json [--llm http://127.0.0.1:1235/v1]
"""
import json, re, ssl, sys, time, urllib.request, urllib.error

UA = {"User-Agent": "Mozilla/5.0 (compatible; MOOPDirectoryBot/1.0; +https://usmcmin.org/churches.html)"}
CTX = ssl._create_unverified_context()  # read-only public pages; church TLS is often broken
PATHS = ["", "/about", "/about-us", "/staff", "/leadership", "/our-team", "/team", "/pastors", "/elders", "/leaders"]
MINISTRY_TAIL = re.compile(r"^(equipping|ministries|ministry|worship|connect|missions|discipleship|outreach|groups|media|communications|operations|administration|families|students|children|youth|music|preaching|teaching|counseling|evangelism|education|admin|online|campus|creative|tech|production|next|steps|generations|kids|college|network|resources|giving|generosity|connections|nursery)$", re.I)
NONLEAD_ROLE = re.compile(r"youth|kids|children|students|worship|music|executive|associate|assistant|admin|connect|outreach|discipleship|equipping|missions|family|women|creative|tech|media|next\s*gen|college|groups|care|counseling|education|operations", re.I)

# ── Deterministic social-link capture (2026-07-03) ──────────────────────────
# Harvested by REGEX from the raw fetched HTML — no LLM involved, so no trust
# question. merge-pastor-enrichments.js re-validates host patterns and only
# fills EMPTY fields. 7k+ churches have a website but no social link on file.
SOCIAL_RE = {
    "facebook": re.compile(r'https?://(?:www\.|m\.)?facebook\.com/[A-Za-z0-9_.\-]{3,}/?', re.I),
    "instagram": re.compile(r'https?://(?:www\.)?instagram\.com/[A-Za-z0-9_.\-]{2,}/?', re.I),
    "youtube": re.compile(r'https?://(?:www\.)?youtube\.com/(?:@[\w.\-]+|channel/[\w\-]+|c/[\w.\-]+|user/[\w.\-]+)/?', re.I),
}
BAD_SOCIAL = re.compile(r'facebook\.com/(?:sharer|share|plugins|dialog|login|events|photo|watch|hashtag|policies|help|tr\b|profile\.php)|instagram\.com/(?:p|reel|explore|accounts)/', re.I)


def harvest_socials(raw, found):
    for k, rx in SOCIAL_RE.items():
        if k in found:
            continue
        for m in rx.finditer(raw):
            u = m.group(0).rstrip('/&"\'')
            if BAD_SOCIAL.search(u):
                continue
            found[k] = u.split("?")[0].split("#")[0]
            break


# ── Same-host staff-page discovery (2026-07-03) ─────────────────────────────
# The fixed PATHS list misses churches whose staff page lives at a custom slug
# ("/our-church/meet-the-team"). Harvest same-host links whose path looks
# leadership-ish from the homepage and try those too — this is what makes the
# --retry pass over one-strike "no parseable pastor" churches worthwhile.
HREF_RE = re.compile(r'href=["\']([^"\'#?]+)', re.I)
STAFFY = re.compile(r'staff|leader|team|about|elder|pastor|minist|who-we-are|meet', re.I)


def discover_links(raw, base):
    from urllib.parse import urljoin, urlparse
    host = urlparse(base).netloc.lower().replace("www.", "")
    out, seen = [], set()
    for m in HREF_RE.finditer(raw):
        u = urljoin(base + "/", m.group(1)).split("#")[0]
        pu = urlparse(u)
        if pu.netloc.lower().replace("www.", "") != host:
            continue
        if not STAFFY.search(pu.path):
            continue
        if re.search(r"\.(pdf|jpe?g|png|gif|svg|mp[34]|css|js|ico)$", pu.path, re.I):
            continue
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out[:4]

SYSTEM_PROMPT = (
    "You extract pastor names from church website text. Reply with ONLY a JSON object, no prose:\n"
    '{"lead_pastor": {"name": "...", "role": "..."} , "other_pastors": [{"name": "...", "role": "..."}]}\n'
    "Rules: (1) Every name must appear VERBATIM in the provided text — never guess or complete a name. "
    "(2) lead_pastor is ONLY the senior/lead/preaching pastor or the sole pastor; if none is clearly identified, use null. "
    "(3) other_pastors lists other pastors/elders with their exact titles (max 8). "
    "(4) Use full names as written (keep Dr./Rev. if present). (5) If the text names no pastors at all, both fields are null/empty."
)


def fetch(url, timeout=12):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        return r.read(400_000).decode("utf-8", "replace")


def to_text(html):
    html = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    import html as h
    return re.sub(r"\s+", " ", h.unescape(html)).strip()


def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def looks_junk(name):
    s = str(name or "").strip()
    if not s or len(s) > 32 or re.search(r"[\n;<>{}|]|https?:", s, re.I):
        return True
    if re.match(r"^[a-z]", s):  # ASCII-lowercase start only — non-Latin names are fine
        return True
    t = s.split()
    if len(t) < 2 or len(t) > 5:
        return True
    if MINISTRY_TAIL.match(t[-1]):
        return True
    return False


def pick_llm(cli_base=None):
    bases = [cli_base] if cli_base else ["http://127.0.0.1:1235/v1", "http://127.0.0.1:1234/v1"]
    for b in [x for x in bases if x]:
        try:
            with urllib.request.urlopen(b.rstrip("/") + "/models", timeout=5) as r:
                j = json.load(r)
                # OpenAI shape {"data":[{"id":...}]} (LM Studio, llama-server) OR
                # Ollama shape {"models":[{"name"/"model":...}]} (Hermes :1235 proxy)
                models = j.get("data") or j.get("models") or []
                # skip embedding models (LM Studio lists them alongside chat models)
                names = [m.get("id") or m.get("model") or m.get("name") for m in models]
                names = [n for n in names if n and "embed" not in n.lower()]
                if names:
                    return b.rstrip("/"), names[0]
        except Exception:
            continue
    return None, None


def llm_extract(base, model, text):
    body = json.dumps({
        "model": model, "temperature": 0, "max_tokens": 500,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT},
                     {"role": "user", "content": "CHURCH WEBSITE TEXT:\n" + text[:14000]}],
    }).encode()
    req = urllib.request.Request(base + "/chat/completions", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=240) as r:
        content = json.load(r)["choices"][0]["message"]["content"]
    # first balanced {...} block
    start = content.find("{")
    if start < 0:
        return {}
    depth = 0
    for i, ch in enumerate(content[start:], start):
        depth += ch == "{"
        depth -= ch == "}"
        if depth == 0:
            try:
                return json.loads(content[start:i + 1])
            except json.JSONDecodeError:
                return {}
    return {}


def main():
    batch_path, out_path = sys.argv[1], sys.argv[2]
    cli_base = sys.argv[sys.argv.index("--llm") + 1] if "--llm" in sys.argv else None
    base, model = pick_llm(cli_base)
    if not base:
        sys.exit("NO_LOCAL_LLM: neither :1235 (llama-server) nor :1234 (LM Studio) answered /v1/models")
    print(f"extractor: {model} @ {base}")

    churches = json.load(open(batch_path))
    out = []
    for i, ch in enumerate(churches, 1):
        cid, site = ch["id"], str(ch.get("website") or "").rstrip("/")
        entry = {"id": cid, "pastor_name": None, "pastor_role": None, "other_pastors": [],
                 "pastor_source_url": None, "website_status": "timeout",
                 "extractor": "local-" + model.split("/")[-1][:40]}
        pages, last_err, socials = [], "timeout", {}
        candidates = [site + p for p in PATHS]
        tried, links_harvested = set(), False
        idx = 0
        while idx < len(candidates) and len(pages) < 4 and len(tried) < 9:
            url = candidates[idx]
            idx += 1
            if url in tried:
                continue
            tried.add(url)
            try:
                raw = fetch(url)
            except urllib.error.HTTPError as e2:
                last_err = "404" if e2.code in (404, 410) else "timeout"
                continue
            except Exception:
                last_err = "timeout"
                continue
            harvest_socials(raw, socials)
            if not links_harvested:  # discover staff-ish pages from the first page that loads
                links_harvested = True
                candidates.extend(u for u in discover_links(raw, site) if u not in tried)
            txt = to_text(raw)
            if len(txt) > 400:
                pages.append((url, txt[:6000]))
        entry.update(socials)  # deterministic finds ride along even when no pastor parses
        if not pages:
            entry["website_status"] = last_err
            out.append(entry)
            print(f"  [{i}/{len(churches)}] {cid}: fetch failed ({last_err})")
            continue

        combined = " \n ".join(t for _, t in pages)
        try:
            res = llm_extract(base, model, combined)
        except Exception as e3:
            print(f"  [{i}/{len(churches)}] {cid}: LLM error {e3}")
            entry["website_status"] = "200_no_pastor_found"
            out.append(entry)
            continue

        def verify(name):
            """Name must appear verbatim in a fetched page; returns source URL or None."""
            n = norm(str(name or ""))
            n2 = re.sub(r"^(dr|rev|pastor)\.? ", "", n)
            for url, t in pages:
                tl = norm(t)
                if n and n in tl or (n2 and n2 in tl):
                    return url
            return None

        lead = res.get("lead_pastor") if isinstance(res, dict) else None
        others_in = res.get("other_pastors") if isinstance(res, dict) else None
        others = []
        for p in (others_in or [])[:8]:
            if isinstance(p, dict) and not looks_junk(p.get("name")) and verify(p.get("name")):
                others.append({"name": str(p["name"]).strip(),
                               "role": str(p.get("role") or "Pastor").strip()[:60]})
        if isinstance(lead, dict) and lead.get("name"):
            name, role = str(lead["name"]).strip(), str(lead.get("role") or "").strip()
            src = verify(name)
            if src and not looks_junk(name):
                if role and NONLEAD_ROLE.search(role):
                    others.insert(0, {"name": name, "role": role[:60]})  # demote: not the lead
                else:
                    entry.update(pastor_name=name, pastor_role=(role or "Lead Pastor")[:60],
                                 pastor_source_url=src)
        entry["other_pastors"] = others
        entry["website_status"] = "200_pastor_found" if entry["pastor_name"] else "200_no_pastor_found"
        out.append(entry)
        print(f"  [{i}/{len(churches)}] {cid}: {entry['pastor_name'] or '(no verified lead)'}"
              + (f" +{len(others)} others" if others else "")
              + (f" [socials: {'/'.join(sorted(socials))}]" if socials else ""))
        time.sleep(0.3)

    json.dump(out, open(out_path, "w"), indent=1)
    found = sum(1 for e in out if e["pastor_name"])
    soc = sum(1 for e in out if e.get("facebook") or e.get("youtube") or e.get("instagram"))
    print(f"wrote {out_path}: {found}/{len(out)} leads verified, {soc} with socials")


if __name__ == "__main__":
    main()
