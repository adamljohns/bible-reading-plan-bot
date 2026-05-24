#!/usr/bin/env python3
"""
Render data/readings/<date>.json -> docs/readings/<date>.html (static, noindex).
Matches chronological.html's dark+gold theme.

v2 (2026-05-23):
  - Scripture rendered as flowing prose, NO verse number sups
  - Tabbed watch-focus UI: 5 watch tabs + "All" tab; one watch at a time by default
  - Audio slot per watch (currently placeholder; wires to ElevenLabs once API key + voice ID arrive)
  - HA²PPY acronym rendered with proper superscript on A

Usage:  python3 scripts/build_reading_page.py 2026-03-01
"""
import json
import sys
from pathlib import Path
from html import escape

REPO = Path(__file__).resolve().parent.parent

# Slug used for tab IDs / URL hash
WATCH_SLUGS = {
    "morning_wisdom": "wisdom",
    "first_watch":    "husband",
    "second_watch":   "father",
    "third_watch":    "citizen",
    "evening_peace":  "peace",
}
WATCH_LABELS = {
    "morning_wisdom": ("0600", "Morning Wisdom"),
    "first_watch":    ("0700", "Husband"),
    "second_watch":   ("1100", "Father"),
    "third_watch":    ("1500", "Citizen"),
    "evening_peace":  ("2100", "Evening Peace"),
}


def render_scripture(scr):
    """Flowing scripture text (no verse numbers). Joins all verses into prose."""
    src_label = "MOOP Bible Translation (v0.3-pilot)" if scr["source"] == "MBT" else "World English Bible (WEB) -- public domain"
    parts = ['<div class="scripture">',
             f'<div class="scripture-ref">{escape(scr["reference"])} <span class="scripture-src">-- {escape(src_label)}</span></div>',
             '<div class="scripture-text">']
    # Group verses into ~3-verse paragraphs for readability; preserve psalm-line layout for poetic books
    for vobj in scr["verses"]:
        text = escape(vobj["text"])
        parts.append(f'<p>{text}</p>')
    parts.extend(['</div>', '</div>'])
    return "\n".join(parts)


def render_audio_slot(date, watch_key):
    """Placeholder for ElevenLabs voiceover. When the asset exists at
    docs/assets/audio/readings/<date>-<slug>.mp3 it renders the player;
    otherwise it renders a 'voiceover coming' hint."""
    slug = WATCH_SLUGS[watch_key]
    rel = f"../assets/audio/readings/{date}-{slug}.mp3"
    abs_path = REPO / f"docs/assets/audio/readings/{date}-{slug}.mp3"
    if abs_path.exists():
        return f'''<div class="audio-slot">
  <audio controls preload="metadata" style="width:100%;max-width:560px;">
    <source src="{rel}" type="audio/mpeg">
    Your browser does not support audio.
  </audio>
  <div class="audio-cap">ElevenLabs voiceover -- {WATCH_LABELS[watch_key][1]}</div>
</div>'''
    return f'''<div class="audio-slot audio-pending">
  <div class="audio-cap">🎙️ ElevenLabs voiceover -- coming for this watch</div>
</div>'''


def render_application(app):
    if isinstance(app, list):
        items = "\n".join(f'<li>{escape(item)}</li>' for item in app)
        return f'<ul class="application">{items}</ul>'
    return f'<p class="application-prose">{escape(app)}</p>'


def render_prayer(text, title="Prayer"):
    body = "<br>".join(escape(line) for line in text.split("\n"))
    return f'<div class="prayer"><div class="prayer-title">🙏 {escape(title)}</div><p>{body}</p></div>'


def render_helm(label, command):
    return f'<div class="helm"><span class="helm-icon">⚓</span> <span class="helm-label">{escape(label)}:</span> {escape(command)}</div>'


def render_virtue_label(framework, letter, virtue):
    """Render a virtue tag like 'HA²PPY -- A (Adoring)'.  framework is 'happy'|'fulfilled'|'resolute'."""
    if framework == "happy":
        acronym = 'HA<sup>2</sup>PPY'
    elif framework == "fulfilled":
        acronym = 'F.U.L.F.I.L.L.E.D.'
    elif framework == "resolute":
        acronym = 'R.E.S.O.L.U.T.E.'
    else:
        acronym = framework.upper()
    return f'<span class="virtue-tag">{acronym} &nbsp;·&nbsp; <strong>{escape(letter)}</strong> ({escape(virtue)})</span>'


def render_watch(date, key, w):
    slug = WATCH_SLUGS[key]
    pieces = [f'<section class="watch watch-{slug}" id="watch-{slug}" data-watch="{slug}">']
    pieces.append(f'<div class="watch-header"><span class="watch-time">{escape(w["time"])}</span> <h2>{escape(w["title"])}</h2></div>')

    if "intro" in w:
        pieces.append(f'<p class="intro">{escape(w["intro"])}</p>')

    # Audio slot at top of each watch (above scripture)
    pieces.append(render_audio_slot(date, key))

    pieces.append(render_scripture(w["scripture"]))

    # Context-style sections
    for ctx_key, ctx_icon, ctx_label in (
        ("context_summary", "🌅", "Context"),
        ("briefing", "🖼", "Briefing"),
        ("field_notes", "🌅", "Field Notes"),
        ("situation_report", "🏞", "Situation Report"),
    ):
        if ctx_key in w:
            pieces.append(f'<div class="context"><div class="section-label">{ctx_icon} {ctx_label}</div><p>{escape(w[ctx_key])}</p></div>')

    # Reflection blocks
    if "real_man_theme" in w:
        theme = w["real_man_theme"]
        pieces.append(f'<div class="reflection"><div class="section-label">🛡 Reflection for a REAL MAN &nbsp;·&nbsp; <em>{escape(theme)}</em></div><p>{escape(w["reflection"])}</p></div>')

    if "happy_virtue" in w:
        letter = w.get("happy_letter", w["happy_virtue"][0].upper())
        tag = render_virtue_label("happy", letter, w["happy_virtue"])
        pieces.append(f'<div class="reflection"><div class="section-label">❤️ Reflection for Your Wife &nbsp;·&nbsp; {tag}</div><p>{escape(w["reflection_for_wife"])}</p></div>')

    if "fulfilled_virtue" in w:
        letter = w.get("fulfilled_letter", w["fulfilled_virtue"][0].upper())
        tag = render_virtue_label("fulfilled", letter, w["fulfilled_virtue"])
        rfc = w["reflection_for_children"]
        pieces.append(f'<div class="reflection"><div class="section-label">👨‍👦 Reflection for Your Children &nbsp;·&nbsp; {tag}</div>')
        pieces.append(f'<p>{escape(rfc["intro"])}</p>')
        for child_key in ("gideon", "boaz", "shiloh"):
            if child_key in rfc:
                pieces.append(f'<p><strong>{child_key.capitalize()}.</strong> {escape(rfc[child_key])}</p>')
        pieces.append('</div>')

    if "resolute_virtue" in w:
        letter = w.get("resolute_letter", w["resolute_virtue"][0].upper())
        tag = render_virtue_label("resolute", letter, w["resolute_virtue"])
        rr = w["resolute_reflection"]
        pieces.append(f'<div class="reflection"><div class="section-label">🛡 Reflection for a RESOLUTE Citizen &nbsp;·&nbsp; {tag}</div>')
        for loc_key, loc_label in (("fredericksburg", "Fredericksburg (local)"),
                                    ("virginia", "Virginia (state)"),
                                    ("united_states", "United States (nation)")):
            if loc_key in rr:
                pieces.append(f'<p><strong>{loc_label}.</strong> {escape(rr[loc_key])}</p>')
        pieces.append('</div>')

        if "this_day_in_american_history" in w:
            tdh = w["this_day_in_american_history"]
            pieces.append(f'<div class="history"><div class="section-label">🦅 This Day in American History &nbsp;·&nbsp; {escape(tdh["date"])}</div><ul>')
            for ev in tdh["events"]:
                pieces.append(f'<li><strong>{ev["year"]}</strong> &nbsp;·&nbsp; {escape(ev["headline"])}</li>')
            pieces.append('</ul>')
            if "tie" in tdh:
                pieces.append(f'<p class="history-tie">{escape(tdh["tie"])}</p>')
            pieces.append('</div>')

    if "integrated_reflection" in w:
        ir = w["integrated_reflection"]
        pieces.append(f'<div class="reflection"><div class="section-label">🍃 Reflection for a Man at Home and in Community</div>')
        pieces.append(f'<p>{escape(ir["intro"])}</p>')
        for k, label in (("happy_husband", "As a HA²PPY husband"),
                          ("fulfilled_father", "As a FULFILLED father"),
                          ("resolute_citizen", "As a RESOLUTE citizen")):
            if k in ir:
                pieces.append(f'<p><strong>{label}.</strong> {escape(ir[k])}</p>')
        pieces.append('</div>')

    if "application" in w:
        pieces.append(f'<div class="application-block"><div class="section-label">⛏ Personal Application</div>')
        pieces.append(render_application(w["application"]))
        if "application_close" in w:
            pieces.append(f'<p class="application-prose">{escape(w["application_close"])}</p>')
        pieces.append('</div>')

    if "prayer" in w:
        pieces.append(render_prayer(w["prayer"], title=w.get("prayer_title", "Prayer")))

    if "helm_command" in w:
        pieces.append(render_helm("Helm Command", w["helm_command"]))
    if "rudder_steer" in w:
        pieces.append(render_helm("Rudder Steer", w["rudder_steer"]))

    pieces.append('</section>')
    return "\n".join(pieces)


def render_tabs(default_slug="all"):
    """Top-of-page tabs: All + 5 watches."""
    tabs = [('all', 'All Watches', '')]
    for key, slug in WATCH_SLUGS.items():
        time, short = WATCH_LABELS[key]
        tabs.append((slug, short, time))
    out = ['<nav class="watch-tabs" role="tablist">']
    for slug, label, time in tabs:
        active = ' active' if slug == default_slug else ''
        time_html = f'<span class="tab-time">{time}</span> ' if time else ''
        out.append(f'<a href="#{slug}" class="watch-tab{active}" data-tab="{slug}" role="tab">{time_html}<span class="tab-label">{label}</span></a>')
    out.append('</nav>')
    return "\n".join(out)


def render_page(date):
    src = REPO / f"data/readings/{date}.json"
    if not src.exists():
        sys.exit(f"ERROR: {src} not found. Build the data file first.")
    data = json.loads(src.read_text())

    from datetime import datetime
    dt = datetime.fromisoformat(date)
    date_label = dt.strftime("%A, %B %-d, %Y")

    watches_html = "\n\n".join(render_watch(date, k, w) for k, w in data["watches"].items())

    rotation = data["virtue_rotation"]
    rotation_line = (
        f"<strong>HA<sup>2</sup>PPY:</strong> {rotation['happy']} &nbsp;·&nbsp; "
        f"<strong>FULFILLED:</strong> {rotation['fulfilled']} &nbsp;·&nbsp; "
        f"<strong>RESOLUTE:</strong> {rotation['resolute']}"
    )

    tabs_html = render_tabs(default_slug="all")

    # JS for tab switching + URL hash persistence
    tab_js = """
<script>
(function(){
  const SLUGS = ['all','wisdom','husband','father','citizen','peace'];
  function showOnly(slug){
    const isAll = slug === 'all' || !SLUGS.includes(slug);
    document.querySelectorAll('section.watch').forEach(s => {
      s.style.display = (isAll || s.dataset.watch === slug) ? '' : 'none';
    });
    document.querySelectorAll('.watch-tab').forEach(t => {
      t.classList.toggle('active', t.dataset.tab === (isAll ? 'all' : slug));
    });
  }
  document.querySelectorAll('.watch-tab').forEach(t => {
    t.addEventListener('click', function(e){
      e.preventDefault();
      const slug = this.dataset.tab;
      history.replaceState(null, '', '#' + slug);
      showOnly(slug);
      window.scrollTo({top: 0, behavior:'smooth'});
    });
  });
  // Initial: from hash, else 'all'
  const initial = (location.hash || '#all').slice(1);
  showOnly(initial);
})();
</script>
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow">
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
    <title>{escape(date_label)} -- Daily Reading | U.S.M.C. Ministries</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{
            --bg-dark: #000000; --bg-card: #111111; --bg-card2: #161616;
            --gold: #D4AF37; --gold-light: #F4D470;
            --white: #FFFFFF; --gray: #888888; --border: #333333;
        }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-dark);
            color: var(--white);
            min-height: 100vh;
            line-height: 1.7;
        }}
        h1, h2, h3 {{ font-family: 'Playfair Display', serif; font-weight: 700; }}
        .container {{ max-width: 820px; margin: 0 auto; padding: 24px 20px 60px; }}
        a {{ color: var(--gold); text-decoration: none; }}
        a:hover {{ color: var(--gold-light); text-decoration: underline; }}

        .nav-back {{ margin-bottom: 14px; font-size: 0.95rem; }}

        .hero {{ text-align: center; padding: 16px 0 10px; border-bottom: 1px solid var(--border); margin-bottom: 18px; }}
        .hero h1 {{ font-size: clamp(1.5rem, 4vw, 2.2rem); color: var(--white); margin-bottom: 6px; }}
        .hero .subtitle {{ color: var(--gold); font-size: 0.95rem; font-style: italic; }}
        .hero .doc-line {{ color: var(--gray); font-size: 0.82rem; margin-top: 6px; }}
        .hero .rotation {{ color: var(--gray); font-size: 0.85rem; margin-top: 8px; }}
        .hero .rotation strong {{ color: var(--gold); font-weight: 600; }}
        .hero .rotation sup {{ color: var(--gold-light); font-size: 0.65em; vertical-align: super; }}

        /* TABS */
        .watch-tabs {{
            position: sticky; top: 0; z-index: 30;
            background: var(--bg-dark);
            border-bottom: 1px solid var(--border);
            display: flex; flex-wrap: wrap; gap: 6px;
            padding: 12px 0 14px;
            margin-bottom: 18px;
        }}
        .watch-tab {{
            flex: 1 1 90px;
            text-align: center;
            padding: 8px 6px;
            border: 1px solid var(--border);
            border-radius: 100px;
            background: var(--bg-card);
            color: var(--gray);
            font-size: 0.85rem; font-weight: 500;
            transition: all 0.15s ease;
            text-decoration: none !important;
            white-space: nowrap;
        }}
        .watch-tab:hover {{
            color: var(--white);
            border-color: var(--gold);
            text-decoration: none !important;
        }}
        .watch-tab.active {{
            background: var(--gold); color: #000; border-color: var(--gold);
            font-weight: 600;
        }}
        .watch-tab .tab-time {{
            display: block; font-size: 0.7rem; opacity: 0.7;
            font-family: monospace;
        }}
        .watch-tab.active .tab-time {{ opacity: 1; }}

        .watch {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 24px 22px;
            margin-bottom: 22px;
            scroll-margin-top: 80px;
        }}
        .watch-header {{ display: flex; align-items: baseline; gap: 14px; margin-bottom: 10px; flex-wrap: wrap; }}
        .watch-time {{
            background: var(--bg-card2); color: var(--gold);
            padding: 4px 12px; border-radius: 100px;
            font-family: 'Inter', monospace; font-size: 0.85rem; font-weight: 600;
            letter-spacing: 0.05em;
        }}
        .watch-header h2 {{ font-size: 1.35rem; color: var(--white); }}

        .intro {{ color: var(--gray); font-style: italic; margin-bottom: 14px; }}

        .audio-slot {{
            margin: 14px 0 18px;
            padding: 12px 14px;
            background: var(--bg-card2);
            border-radius: 8px;
            border: 1px dashed var(--border);
        }}
        .audio-slot.audio-pending {{ opacity: 0.55; }}
        .audio-cap {{ font-size: 0.8rem; color: var(--gray); margin-top: 4px; }}

        .scripture {{
            background: var(--bg-card2);
            border-left: 3px solid var(--gold);
            border-radius: 6px;
            padding: 16px 20px;
            margin: 16px 0 22px;
        }}
        .scripture-ref {{ font-weight: 600; color: var(--gold); margin-bottom: 12px; font-size: 0.95rem; }}
        .scripture-src {{ color: var(--gray); font-weight: 400; font-size: 0.82rem; }}
        .scripture-text p {{ margin-bottom: 8px; }}

        .section-label {{
            font-family: 'Playfair Display', serif;
            color: var(--gold); font-weight: 700; font-size: 1.05rem;
            margin: 22px 0 10px; padding-top: 10px; border-top: 1px solid var(--border);
        }}
        .section-label em {{ color: var(--white); font-style: italic; }}
        .virtue-tag {{ font-family: 'Inter', sans-serif; color: var(--gold-light); font-size: 0.9rem; font-weight: 500; }}
        .virtue-tag strong {{ color: var(--white); font-weight: 700; }}
        .virtue-tag sup {{ font-size: 0.65em; vertical-align: super; color: var(--gold-light); }}

        .context p, .reflection p, .history p, .application-block p {{ margin-bottom: 12px; }}

        ul.application {{ padding-left: 22px; margin: 8px 0 14px; }}
        ul.application li {{ margin-bottom: 8px; }}
        .application-prose {{ font-style: italic; color: var(--gold-light); margin-top: 12px; }}

        .history ul {{ padding-left: 22px; margin: 8px 0; }}
        .history li {{ margin-bottom: 6px; }}
        .history-tie {{ font-style: italic; color: var(--gray); margin-top: 8px; }}

        .prayer {{
            background: var(--bg-card2);
            border-left: 3px solid var(--gold-light);
            border-radius: 6px;
            padding: 16px 20px;
            margin: 22px 0;
        }}
        .prayer-title {{ color: var(--gold-light); font-weight: 600; margin-bottom: 10px; font-size: 0.95rem; }}
        .prayer p {{ line-height: 1.85; }}

        .helm {{
            background: var(--bg-card2);
            border-radius: 6px;
            padding: 12px 18px;
            margin-top: 14px;
            font-size: 0.95rem;
        }}
        .helm-icon {{ color: var(--gold); font-size: 1.1rem; }}
        .helm-label {{ color: var(--gold); font-weight: 600; }}

        footer {{
            text-align: center;
            color: var(--gray);
            font-size: 0.82rem;
            margin-top: 32px;
            padding-top: 18px;
            border-top: 1px solid var(--border);
        }}
        footer .draft-tag {{
            display: inline-block;
            background: #2a2410;
            color: var(--gold);
            padding: 4px 12px;
            border-radius: 100px;
            font-size: 0.78rem;
            margin-bottom: 8px;
            letter-spacing: 0.05em;
        }}

        @media (max-width: 540px) {{
            .watch-tab {{ flex: 1 1 64px; font-size: 0.78rem; padding: 6px 4px; }}
            .watch-tab .tab-time {{ font-size: 0.65rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">

        <div class="nav-back">← <a href="/chronological.html">The Watchman's Chronological Plan</a></div>

        <div class="hero">
            <h1>{escape(date_label)}</h1>
            <div class="subtitle">Daily Reading -- Day {data['day_of_year']} of 365</div>
            <div class="doc-line">{escape(data['month_doc'])}</div>
            <div class="rotation">{rotation_line}</div>
        </div>

        {tabs_html}

        {watches_html}

        <footer>
            <div class="draft-tag">PROTOTYPE -- sign-off pending</div>
            <div>U.S.M.C. Ministries · The Watchman's Chronological Plan for the Year of our Lord 2026</div>
            <div style="margin-top:6px;font-size:0.78rem;">{escape(data['meta']['voice_anchor'])}</div>
        </footer>

    </div>
    {tab_js}
</body>
</html>
"""

    out = REPO / f"docs/readings/{date}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print(f"Wrote {out}  ({out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    date = sys.argv[1] if len(sys.argv) > 1 else "2026-03-01"
    render_page(date)
