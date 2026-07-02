#!/usr/bin/env python3
"""generate-realman-devotional.py [day ...]

Generate the REAL MAN Proverbs devotional day pages (docs/proverbs/<N>.html) from
compact per-day content in data/realman-devotional.json. The page shell (CSS, nav,
header, card structure, footer) is lifted VERBATIM from the hand-authored Day 1
(docs/proverbs/1.html) so every generated day matches Days 1-2 exactly.

Days 1 and 2 are hand-authored originals and are NEVER regenerated. Pass day numbers
to generate a subset; with no args, generates every day present in the JSON.

  python3 bin/generate-realman-devotional.py          # all days in the JSON
  python3 bin/generate-realman-devotional.py 3 4 5    # just these
"""
import json, os, re, sys, html as _html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROV = os.path.join(ROOT, "docs", "proverbs")
DATA = os.path.join(ROOT, "data", "realman-devotional.json")

# R.E.A.L. M.A.N. — one quality per day, cycling every 7 days (Day 1 = R, Day 2 = E …)
QUALITIES = [
    ("R", "Reject Passivity"),
    ("E", "Engage Consistently"),
    ("A", "Accept Responsibility"),
    ("L", "Lead Courageously"),
    ("M", "Manage Faithfully"),
    ("A", "Account Accurately"),
    ("N", "Never Quit"),
]
# Thematic week titles (7 days each; week 5 is the short finish, days 29-31).
WEEK_THEMES = {
    1: "Wisdom Speaks",
    2: "Two Roads",
    3: "The Weighed Heart",
    4: "The Proven Man",
    5: "Hold the Line",
}

def quality(n):      return QUALITIES[(n - 1) % 7]
def week_num(n):     return (n - 1) // 7 + 1
def week_span(n):
    w = week_num(n)
    lo = (w - 1) * 7 + 1
    hi = min(lo + 6, 31)
    return lo, hi
def week_label(n):
    w = week_num(n)
    lo, hi = week_span(n)
    return f"Week {w} — {WEEK_THEMES[w]} (Days {lo}–{hi})"

def extract_style(day1_html):
    m = re.search(r"<style>.*?</style>", day1_html, re.S)
    if not m:
        raise SystemExit("could not extract <style> from docs/proverbs/1.html")
    return m.group(0)

def paras(text_or_list):
    items = text_or_list if isinstance(text_or_list, list) else [text_or_list]
    return "\n      ".join(f"<p>{p}</p>" for p in items)

def page(n, d, style):
    letter, qual = quality(n)
    wl = week_label(n)
    nn = f"{n:02d}"
    prev_href = "intro.html" if n == 1 else f"{n-1}.html"
    prev_label = "← Introduction" if n == 1 else f"← Day {n-1}"
    next_href = "index.html" if n >= 31 else f"{n+1}.html"
    next_label = "All Chapters →" if n >= 31 else f"Day {n+1} →"
    kv = d["keyVerse"]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="canonical" href="https://usmcmin.org/proverbs/{n}.html">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Proverbs {n} — REAL MAN Devotional Day {n}</title>

  <!-- Open Graph / Social Sharing -->
  <meta property="og:title" content="Proverbs {n} — REAL MAN Devotional Day {n}: {qual}">
  <meta property="og:description" content="Day {n} of the REAL MAN Proverbs Devotional. {letter} = {qual}. Proverbs {n} — USMC Ministries.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://usmcmin.org/proverbs/{n}">
  <meta property="og:site_name" content="USMC Ministries">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="Proverbs {n} — REAL MAN Devotional Day {n}">
  <meta name="twitter:description" content="Day {n} of the REAL MAN Proverbs Devotional. {letter} = {qual}.">
  <meta name="description" content="Day {n} of the REAL MAN Proverbs Devotional — Proverbs {n}, {qual}. USMC Ministries.">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

  {style}
</head>
<body>

  <!-- NAV -->
  <nav>
    <span class="logo">✝️</span>
    <span class="brand">USMC Ministries</span>
    <span class="sep">·</span>
    <a href="index.html">Proverbs</a>
    <span class="sep">·</span>
    <a href="../bible.html?ref=Proverbs%20{n}:1">Bible Training Environment</a>
  </nav>

  <div class="page-wrapper">

    <!-- PAGE HEADER -->
    <div class="page-header">
      <div class="eyebrow">REAL MAN Proverbs Devotional</div>
      <h1>Proverbs — 31 Days of Manhood</h1>
      <p class="subhead">One chapter a day. Seven qualities. One framework that changes everything.</p>
    </div>

    <!-- WEEK {week_num(n)} / DAY {n} -->
    <div class="day-header">
      <div class="week-label">{wl}</div>
      <h2>Day {n}: Proverbs {n}</h2>
      <div class="focus-tag">{letter} — {qual}</div>
    </div>

    <!-- REAL MAN FOCUS -->
    <div class="content-card">
      <h3><span class="section-icon"><img src="../assets/icons/shield-target.png" alt="" width="16" height="16" style="vertical-align:middle;margin-right:3px;"></span> REAL MAN Focus</h3>
      {paras(d["focus"])}
    </div>

    <!-- READ -->
    <div class="content-card">
      <h3><span class="section-icon"><img src="../assets/icons/shield-bible.png" alt="" width="16" height="16" style="vertical-align:middle;margin-right:3px;"></span> Read</h3>
      <div class="read-badge">
        <span class="read-icon">\U0001F4DC</span>
        Proverbs {n} — full chapter
      </div>
      <p style="margin-bottom:0.5rem; color: var(--gray); font-size: 0.88rem;">Open the whole chapter. Don't skim. Let it land.</p>
      <a style="display:inline-flex; align-items:center; gap:0.5rem; color:var(--accent); text-decoration:none; font-size:0.88rem;" href="../bible.html?ref=Proverbs%20{n}:1"><img src="../assets/icons/shield-bible.png" alt="" width="16" height="16" style="vertical-align:middle;margin-right:3px;"> Read Proverbs {n} in the Bible Training Environment →</a>
    </div>

    <!-- KEY VERSE -->
    <div class="content-card">
      <h3><span class="section-icon">\U0001F511</span> Key Verse</h3>
      <div class="key-verse">
        <blockquote>“{kv["text"]}”</blockquote>
        <cite>— Proverbs {kv["ref"]}</cite>
      </div>
    </div>

    <!-- OBSERVATION -->
    <div class="content-card">
      <h3><span class="section-icon"><img src="../assets/icons/shield-compass.png" alt="" width="16" height="16" style="vertical-align:middle;margin-right:3px;"></span> Observation</h3>
      {paras(d["observation"])}
    </div>

    <!-- APPLICATION -->
    <div class="content-card">
      <h3><span class="section-icon">⚡</span> Application</h3>
      {paras(d["application"])}
    </div>

    <!-- PRAYER -->
    <div class="content-card">
      <h3><span class="section-icon">\U0001F64F</span> Prayer</h3>
      <div class="prayer-block">
        {paras(d["prayer"])}
      </div>
    </div>

    <!-- AUDIO PLAYER -->
    <div class="audio-section">
      <h3>\U0001F399️ Listen to Day {n}</h3>
      <p style="color:var(--gray); font-size:0.85rem; margin-bottom:1rem;">Read by Adam Johns</p>
      <audio controls style="width:100%; max-width:500px;" id="day{n}-audio">
        <source src="../assets/audio/proverbs-day{nn}.mp3" type="audio/mpeg">
        Your browser does not support the audio element.
      </audio>
      <p id="audio-coming" style="color:var(--gray); font-size:0.8rem; font-style:italic; margin-top:0.5rem;">Audio coming soon</p>
    </div>

    <script>
      // Hide "coming soon" text if audio file loads successfully
      var audio = document.getElementById('day{n}-audio');
      var notice = document.getElementById('audio-coming');
      if (audio) {{
        audio.addEventListener('canplay', function() {{ if(notice) notice.style.display='none'; }});
        audio.addEventListener('error', function() {{ audio.style.display='none'; }});
      }}
    </script>

    <!-- CHAPTER NAVIGATION -->
    <div class="chapter-nav">
      <a href="{prev_href}">{prev_label}</a>
      <span class="center-link">Day {n} of 31</span>
      <a href="{next_href}">{next_label}</a>
    </div>

  </div><!-- /page-wrapper -->

  <!-- FOOTER -->
  <footer>
    <p><a href="index.html">Proverbs</a> · <a href="../bible.html">Bible Training Environment</a> · <a href="https://usmcmin.org">USMC Ministries</a></p>
    <p style="margin-top:0.4rem;">REAL MAN Proverbs Devotional — 31 Days of Wisdom</p>
  </footer>

</body>
</html>
"""

def main():
    content = json.load(open(DATA))
    style = extract_style(open(os.path.join(PROV, "1.html")).read())
    want = [int(x) for x in sys.argv[1:]] or sorted(int(k) for k in content)
    wrote = 0
    for n in want:
        if n in (1, 2):
            print(f"  skip Day {n} (hand-authored original)"); continue
        d = content.get(str(n))
        if not d:
            print(f"  Day {n}: no content in JSON — skipped"); continue
        for f in ("focus", "keyVerse", "observation", "application", "prayer"):
            if not d.get(f):
                raise SystemExit(f"Day {n} missing '{f}'")
        open(os.path.join(PROV, f"{n}.html"), "w").write(page(n, d, style))
        letter, qual = quality(n)
        print(f"  Day {n:2d}  Proverbs {n:<2d}  {letter} — {qual:<22}  ({week_label(n)})")
        wrote += 1
    print(f"\nGenerated {wrote} day page(s) -> {PROV}")

if __name__ == "__main__":
    main()
