#!/usr/bin/env python3
"""Build docs/drafts/verse/approval-index.html from ACTUAL gate output.

Why this exists: on 2026-09-07 I "audited" this page by running the gate inside
/Users/moop_bot_pro/bible-reading-plan-bot, a checkout sitting on branch
deploy/ci-guards, 1,257 commits behind origin/main. Its on-disk drafts were old
short versions, so the gate reported 42 unfinished studies and I published a
correction saying the index had inflated its word counts. All of that was false;
the index was right. Run the gate against the tree you are actually shipping.

This script exists so the page is never hand-assembled again: it re-gates every
draft at build time and refuses to write if the gate returns nothing parseable.
"""
import re, subprocess, sys, pathlib, html as H, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
DRAFTS = ROOT / "docs/drafts/verse"
OUT = DRAFTS / "approval-index.html"

def gate():
    # index.html and approval-index.html are navigation, not studies — the gate
    # has no status line for them and would list them as "held back".
    skip = {"approval-index.html", "index.html"}
    files = sorted(str(p) for p in DRAFTS.glob("*.html") if p.name not in skip)
    r = subprocess.run(["node", str(ROOT/"bin/verse-study-gate.js"), *files],
                       capture_output=True, text=True, cwd=ROOT)
    out = r.stdout + r.stderr
    res = {}
    for m in re.finditer(r'^(pass|FAIL)\s+\S*?([a-z0-9\-]+\.html)\s+\(([^,]+), (\d+) words', out, re.M):
        res[m.group(2)] = {"pass": m.group(1) == "pass", "ref": m.group(3), "words": int(m.group(4))}
    if not res:
        sys.exit("gate produced no parseable results — refusing to write an index")
    return res

def prior():
    """Reuse the hand-written descriptions and canonical order from the old index."""
    if not OUT.exists():
        return [], {}, {}
    idx = OUT.read_text()
    order, desc, label = [], {}, {}
    for m in re.finditer(r'<a class="ref" href="([a-z0-9\-]+\.html)"[^>]*>([^<]+)</a>\s*(?:<p class="desc">(.*?)</p>)?', idx, re.S):
        s = m.group(1)
        if s in order:
            continue
        order.append(s); label[s] = m.group(2).strip()
        if m.group(3):
            desc[s] = re.sub(r"\s+", " ", m.group(3)).strip()
    return order, desc, label

CSS = """:root{--navy:#1f3352;--gold:#a8842c;--ink:#1b1815;--gray:#6b6459;--line:#ded7cb}
*{box-sizing:border-box}
body{margin:0;padding:20px 16px 60px;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:#fff;max-width:800px;margin-inline:auto}
h1{font-size:1.5rem;color:var(--navy);margin:0 0 4px}
.sub{color:var(--gray);font-size:.9rem;margin:0 0 18px}
.box{background:#f4f1ea;border-left:4px solid var(--navy);padding:12px 14px;margin:0 0 22px;font-size:.93rem}
.box b{color:var(--navy)}
h2{font-size:1.02rem;color:var(--navy);margin:26px 0 8px;padding-bottom:5px;border-bottom:2px solid var(--navy)}
.batch{font-size:.75rem;letter-spacing:.09em;text-transform:uppercase;color:var(--gold);font-weight:700;margin:22px 0 6px}
.row{padding:10px 0;border-bottom:1px solid var(--line)}
.ref{font-weight:700;color:var(--navy);text-decoration:none;font-size:1.02rem}
.ref:hover{text-decoration:underline}
.desc{margin:3px 0 0;font-size:.93rem;color:#3a352d}
.meta{font-size:.78rem;color:var(--gray);margin-top:3px}
.held{background:#fdf3f3;border-left:4px solid #a33;padding:12px 14px;margin:10px 0 0}
.held .ref{color:#a33}
.held .row{border-bottom:1px solid #eedada}
.correction{background:#fff8e6;border-left:4px solid var(--gold);padding:12px 14px;margin:0 0 22px;font-size:.9rem}"""

def main():
    res = gate()
    order, desc, label = prior()
    for s in sorted(res):
        if s not in order:
            order.append(s)
    ok  = [s for s in order if res.get(s, {}).get("pass")]
    bad = [s for s in order if s in res and not res[s]["pass"]]
    today = datetime.date.today().strftime("%-d %b %Y")

    p = []
    p.append('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">')
    p.append('<meta name="viewport" content="width=device-width,initial-scale=1">')
    p.append('<meta name="robots" content="noindex, nofollow">')
    p.append(f'<title>Verse Study Approval Queue — private</title><style>\n{CSS}\n</style></head><body>')
    p.append('<h1>Verse Study Approval Queue</h1>')
    p.append(f'<p class="sub">Private working page &middot; noindex, robots-disallowed &middot; rebuilt from gate output {today}</p>')
    p.append('<div class="correction"><p style="margin:0"><b>Note.</b> Earlier on 7 Sep this page briefly showed a '
             '&ldquo;correction&rdquo; claiming 42 of these studies were unfinished. That was my error, not the corpus&rsquo;s: '
             'I ran the gate inside a checkout 1,257 commits behind <code>origin/main</code>, so it read old short drafts. '
             'The studies were always fine. Every number below is now re-gated at build time by '
             '<code>bin/build_verse_approval_index.py</code> against the tree being shipped.</p></div>')
    p.append('<div class="box">')
    p.append(f'<p style="margin:0 0 8px"><b>{len(ok)} studies are finished, gate-clean, and waiting on you.</b> '
             f'The other {len(bad)} are real drafts but sit under the 1,200-word floor; they are held below and are not yours to review yet.</p>')
    p.append('<p style="margin:0 0 8px">The clean ones are grouped in <b>batches of five</b>, canonical order. Reply with a batch '
             'number to publish that batch (&ldquo;publish batch 3&rdquo;), or name any single verse to pull it. '
             'Nothing here is public until you say so.</p>')
    p.append('<p style="margin:0"><b>Genesis 1:1</b> is already approved and live &mdash; it is the template these were built to.</p>')
    p.append('</div>')

    for i in range(0, len(ok), 5):
        p.append(f'<p class="batch">Batch {i//5 + 1}</p>')
        for s in ok[i:i+5]:
            r = res[s]
            p.append('<div class="row">')
            p.append(f'<a class="ref" href="{s}">{H.escape(label.get(s, r["ref"]))}</a>')
            if s in desc:
                p.append(f'<p class="desc">{desc[s]}</p>')
            p.append(f'<p class="meta">{r["words"]:,} words &middot; gate PASS</p>')
            p.append('</div>')

    p.append(f'<h2>Held back &mdash; {len(bad)} not finished</h2>')
    p.append('<div class="held">')
    p.append('<p style="margin:0 0 6px">Each of these is under the 1,200-word floor for a deep study &mdash; written, but short. '
             'They are live at their URLs and noindexed. They are not in the batches and are not yours to review yet.</p>')
    for s in bad:
        r = res[s]
        p.append('<div class="row">')
        p.append(f'<a class="ref" href="{s}">{H.escape(label.get(s, r["ref"]))}</a>')
        p.append(f'<p class="meta">{r["words"]:,} words &middot; needs {1200 - r["words"]:,} more &middot; gate FAIL</p>')
        p.append('</div>')
    p.append('</div>')
    p.append('</body></html>')
    OUT.write_text("\n".join(p) + "\n")
    print(f"wrote {OUT}  ({len(ok)} clean, {len(bad)} held)")

if __name__ == "__main__":
    main()
