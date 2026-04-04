#!/usr/bin/env python3
"""Add 50 new FXBG/Spotsylvania/Stafford churches in batches of 10."""

import json
import os
import subprocess
from pathlib import Path

REPO = Path("/Users/adamjohns/bible-reading-plan-bot")
CHURCHES_JSON = REPO / "docs/data/churches.json"
HTML_DIR = REPO / "docs/churches"

def load_data():
    with open(CHURCHES_JSON) as f:
        return json.load(f)

def save_data(data):
    with open(CHURCHES_JSON, "w") as f:
        json.dump(data, f, indent=2)

def generate_html(church):
    c = church
    rating = c["overall_rating"]  # green, yellow, red
    label = c["overall_label"]
    
    if rating == "green":
        icon = "✅"
        badge_class = "rating-green"
    elif rating == "yellow":
        icon = "⚠️"
        badge_class = "rating-yellow"
    else:
        icon = "🚫"
        badge_class = "rating-red"
    
    score_labels = {
        "christology": ("Christology", "Is Jesus the only way? (John 14:6)"),
        "scripture": ("Scripture", "Inerrancy affirmed? Final authority?"),
        "gender": ("Gender / Sexuality", "Biblical manhood &amp; womanhood? Male-only elders/pastors? Patriarchal household vision?"),
        "leadership": ("Leadership Structure", "Male elders/pastors? Accountability?"),
        "soteriology": ("Soteriology", "Faith alone? How is salvation presented?"),
        "cultural": ("Cultural Alignment", "DEI/CRT language? Social justice crowding out gospel?"),
        "denomination": ("Denominational Accountability", "Sent/accountable or independent?"),
        "preaching": ("Preaching Style", "Expository or topical/therapeutic?"),
        "mens": ("Men's Discipleship", "Intentional formation for men?"),
        "mission": ("Mission Clarity", "Great Commission central?"),
    }
    
    score_rows = ""
    for key, (lbl, desc) in score_labels.items():
        score_val = c["scores"].get(key, "yellow")
        note = c.get("score_notes", {}).get(key, "")
        gender_detail = c.get("gender_detail", "") if key == "gender" else ""
        
        if score_val == "green":
            badge_cls = "score-green"
            badge_text = "✅ Strong"
        elif score_val == "yellow":
            badge_cls = "score-yellow"
            badge_text = "⚠️ Caution"
        elif score_val == "red":
            badge_cls = "score-red"
            badge_text = "🚫 Concern"
        else:
            badge_cls = "score-black"
            badge_text = "— Unknown"
        
        note_html = f'<div class="score-note">{note}</div>' if note else ""
        gender_html = f'<div class="gender-detail">👤 {gender_detail}</div>' if gender_detail and key == "gender" else ""
        
        score_rows += f"""
      <div class="score-row">
        <div class="score-info">
          <div class="score-label">{lbl}</div>
          <div class="score-desc">{desc}</div>
          {note_html}
          {gender_html}
        </div>
        <div>
          <span class="score-badge {badge_cls}">{badge_text}</span>
        </div>
      </div>"""
    
    tags_html = "".join(f'<span class="tag">#{t}</span>' for t in c.get("tags", []))
    website = c.get("website", "")
    website_html = f'<a href="{website}" target="_blank" rel="noopener">{website.replace("https://","").replace("http://","").rstrip("/")}</a>' if website else "Not Available"
    
    has_mens = '<span class="fact-value has-yes">✅ Yes</span>' if c.get("has_mens_ministry") else '<span class="fact-value has-no">✗ No</span>'
    has_kids = '<span class="fact-value has-yes">✅ Yes</span>' if c.get("has_kids_ministry") else '<span class="fact-value has-no">✗ No</span>'
    
    map_q = c["address"].replace(" ", "%20").replace(",", "%2C")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/icons/favicon-16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
  <link rel="manifest" href="/manifest.json">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{c['name']} — Theological due diligence scorecard for Christian men in Fredericksburg, VA.">
  <meta property="og:title" content="{c['name']} — Church Directory | USMC Ministries">
  <meta property="og:description" content="10-point theological scorecard: {label}">
  <meta property="og:type" content="website">
  <title>{c['name']} — Church Directory | USMC Ministries</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

  
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  :root {{
    --bg: #000000;
    --bg-card: #111111;
    --gold: #D4AF37;
    --gold-light: #F4D470;
    --white: #e8e8e8;
    --gray: #888888;
    --gray-light: #aaaaaa;
    --border: #333333;
    --green: #4CAF50;
    --yellow: #FFC107;
    --red: #f44336;
    --green-bg: rgba(76,175,80,0.12);
    --yellow-bg: rgba(255,193,7,0.12);
    --red-bg: rgba(244,67,54,0.12);
    --black-bg: rgba(26,26,26,0.95);
  }}
  body {{
    font-family: 'Inter', sans-serif;
    background: var(--bg);
    color: var(--white);
    line-height: 1.7;
    min-height: 100vh;
  }}
  h1, h2, h3, h4 {{ font-family: 'Playfair Display', serif; }}

  .top-nav {{
    display: flex; flex-wrap: wrap; gap: 6px;
    justify-content: center; padding: 14px 20px;
    border-bottom: 1px solid var(--border);
    background: rgba(0,0,0,0.95);
    position: sticky; top: 0; z-index: 100;
  }}
  .top-nav a {{
    color: var(--gray); text-decoration: none; font-size: 0.85rem;
    font-weight: 500; padding: 5px 12px; border-radius: 20px;
    border: 1px solid transparent; transition: all 0.2s; white-space: nowrap;
  }}
  .top-nav a:hover {{ color: var(--gold); border-color: var(--border); }}
  .top-nav a:first-child {{ color: var(--gold); border-color: var(--border); }}

  .hero {{
    padding: 48px 24px 36px;
    text-align: center;
    background: linear-gradient(180deg, rgba(212,175,55,0.08) 0%, transparent 100%);
    border-bottom: 1px solid var(--border);
  }}
  .hero h1 {{
    font-size: clamp(1.6rem, 4vw, 2.6rem);
    color: var(--white);
    margin-bottom: 8px;
    letter-spacing: 0.5px;
  }}
  .hero h1 span {{ color: var(--gold); }}
  .hero .denom-tag {{
    display: inline-block;
    background: rgba(212,175,55,0.1);
    border: 1px solid rgba(212,175,55,0.25);
    color: var(--gold-light);
    font-size: 0.75rem; font-weight: 600;
    letter-spacing: 1.5px; text-transform: uppercase;
    padding: 3px 12px; border-radius: 20px; margin-bottom: 16px;
  }}
  .hero .address {{
    color: var(--gray-light);
    font-size: 0.95rem;
    margin-bottom: 18px;
  }}

  .threat-badge {{
    display: inline-flex; align-items: center; gap: 8px;
    padding: 8px 20px; border-radius: 8px;
    font-weight: 700; font-size: 0.95rem;
    letter-spacing: 0.5px; margin-top: 8px;
    border: 1.5px solid;
  }}
  .threat-badge.rating-green {{ background: rgba(76,175,80,0.18); border-color: var(--green); color: #7edd80; }}
  .threat-badge.rating-yellow {{ background: rgba(255,193,7,0.15); border-color: var(--yellow); color: #ffd85a; }}
  .threat-badge.rating-red {{ background: rgba(244,67,54,0.15); border-color: var(--red); color: #ff7c74; }}
  .threat-icon {{ font-size: 1.3rem; }}

  .page-body {{
    max-width: 960px;
    margin: 0 auto;
    padding: 36px 24px 60px;
  }}

  .card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 28px;
  }}
  .card-title {{
    font-size: 1.0rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--gold);
    margin-bottom: 18px;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
  }}

  .facts-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 14px;
  }}
  .fact-item {{ display: flex; flex-direction: column; gap: 3px; }}
  .fact-label {{ font-size: 0.72rem; color: var(--gray); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }}
  .fact-value {{ font-size: 0.92rem; color: var(--white); font-weight: 500; }}
  .fact-value a {{ color: var(--gold); text-decoration: none; }}
  .fact-value a:hover {{ text-decoration: underline; }}
  .has-yes {{ color: #7edd80; font-weight: 600; }}
  .has-no {{ color: var(--gray); }}

  .score-row {{
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 12px;
    align-items: start;
    padding: 14px 0;
    border-bottom: 1px solid #1e1e1e;
  }}
  .score-row:last-child {{ border-bottom: none; }}
  .score-info {{ display: flex; flex-direction: column; gap: 4px; }}
  .score-label {{ font-weight: 600; font-size: 0.95rem; color: var(--white); }}
  .score-desc {{ font-size: 0.82rem; color: var(--gray-light); }}
  .score-note {{ font-size: 0.82rem; color: #aaa; margin-top: 4px; font-style: italic; }}
  .gender-detail {{ font-size: 0.8rem; color: #bbb; margin-top: 4px; padding: 6px 10px; background: rgba(212,175,55,0.06); border-left: 2px solid var(--gold); border-radius: 0 4px 4px 0; }}
  .score-badge {{
    display: inline-flex; align-items: center; gap: 5px;
    padding: 4px 12px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700; white-space: nowrap;
    border: 1px solid;
  }}
  .score-green {{ background: rgba(76,175,80,0.15); border-color: var(--green); color: #7edd80; }}
  .score-yellow {{ background: rgba(255,193,7,0.12); border-color: var(--yellow); color: #ffd85a; }}
  .score-red {{ background: rgba(244,67,54,0.12); border-color: var(--red); color: #ff7c74; }}
  .score-black {{ background: rgba(50,50,50,0.6); border-color: #555; color: #aaa; }}

  .note-block {{
    padding: 14px 16px;
    border-radius: 8px;
    margin-bottom: 12px;
    border-left: 3px solid;
    font-size: 0.9rem;
    line-height: 1.7;
  }}
  .note-assessment {{
    background: rgba(212,175,55,0.06);
    border-color: var(--gold);
    color: var(--gray-light);
  }}
  .note-tag-row {{
    display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px;
  }}
  .tag {{
    background: #1a1a1a; border: 1px solid #333;
    color: var(--gray); font-size: 0.72rem;
    padding: 3px 10px; border-radius: 20px;
  }}

  .map-wrap {{
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid var(--border);
    margin-bottom: 28px;
  }}
  .map-wrap iframe {{
    width: 100%; height: 320px; border: none; display: block;
    filter: invert(0.9) hue-rotate(180deg);
  }}

  .btn-row {{ display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 28px; }}
  .btn-gold {{
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--gold); color: #000;
    font-weight: 700; font-size: 0.9rem;
    padding: 11px 22px; border-radius: 8px;
    text-decoration: none; border: none; cursor: pointer;
    transition: background 0.2s;
  }}
  .btn-gold:hover {{ background: var(--gold-light); }}
  .btn-outline {{
    display: inline-flex; align-items: center; gap: 8px;
    background: transparent; color: var(--gold);
    font-weight: 600; font-size: 0.9rem;
    padding: 11px 22px; border-radius: 8px;
    text-decoration: none; border: 1.5px solid var(--gold);
    cursor: pointer; transition: all 0.2s;
  }}
  .btn-outline:hover {{ background: rgba(212,175,55,0.1); }}

  .back-row {{
    text-align: center;
    padding: 20px 0 10px;
    border-top: 1px solid var(--border);
    margin-top: 20px;
  }}
  .back-row a {{ color: var(--gold); text-decoration: none; font-weight: 600; font-size: 0.9rem; }}
  .back-row a:hover {{ text-decoration: underline; }}

  footer {{
    text-align: center;
    padding: 24px;
    color: var(--gray);
    font-size: 0.8rem;
    border-top: 1px solid var(--border);
  }}
</style>

</head>
<body>
<nav class="top-nav">
    <a href="/churches.html">← Church Directory</a>
    <a href="/index.html">Home</a>
    <a href="/bible.html">Bible Translation Engine</a>
    <a href="/usmc-ministries.html">U.S.M.C. Ministries</a>
    <a href="/about.html">About</a>
    <a href="/connect.html">Connect</a>
</nav>

<div class="hero">
  <div class="denom-tag">{c['type']}</div>
  <h1>{c['name']}</h1>
  <div class="address">📍 {c['address']}</div>
  <div class="threat-badge {badge_class}">
    <span class="threat-icon">{icon}</span>
    <span class="threat-label">{label}</span>
  </div>
</div>

<div class="page-body">

  <!-- Quick Facts -->
  <div class="card">
    <div class="card-title">📋 Quick Facts</div>
    <div class="facts-grid">
      <div class="fact-item">
        <span class="fact-label">Pastor</span>
        <span class="fact-value">{c.get('pastor', 'Unknown')}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Founded</span>
        <span class="fact-value">{c.get('founded', 'Unknown')}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Denomination</span>
        <span class="fact-value">{c.get('denomination', 'Unknown')}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Service Times</span>
        <span class="fact-value">{c.get('services', 'Check website for times')}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Men's Ministry</span>
        {has_mens}
      </div>
      <div class="fact-item">
        <span class="fact-label">Kids Ministry</span>
        {has_kids}
      </div>
      <div class="fact-item">
        <span class="fact-label">Website</span>
        <span class="fact-value">{website_html}</span>
      </div>
      <div class="fact-item" style="grid-column: 1 / -1;">
        <span class="fact-label">Pastor Credentials</span>
        <span class="fact-value" style="color: var(--gray-light); font-size: 0.88rem;">{c.get('pastor_credentials', 'Unknown')}</span>
      </div>
    </div>
  </div>

  <!-- 10-Point Scorecard -->
  <div class="card">
    <div class="card-title">📊 10-Point Theological Scorecard</div>
    {score_rows}
  </div>

  <!-- Assessment / Notes -->
  <div class="card">
    <div class="card-title">📝 Assessment</div>
    <div class="note-block note-assessment">{c.get('assessment', 'No assessment available.')}</div>
    <div class="note-tag-row">{tags_html}</div>
  </div>

  <!-- Map -->
  
    <div class="map-wrap">
      <iframe
        src="https://maps.google.com/maps?q={map_q}&output=embed"
        allowfullscreen="" loading="lazy"
        referrerpolicy="no-referrer-when-downgrade"
        title="Map for {c['name']}">
      </iframe>
    </div>

  <!-- Buttons -->
  <div class="btn-row">
    {'<a href="' + website + '" target="_blank" rel="noopener" class="btn-gold">🌐 Visit Their Website</a>' if website else ''}
    <a href="/churches.html" class="btn-outline">← Back to Church Directory</a>
  </div>

  <div class="back-row">
    <a href="/churches.html">← Return to Full Church Directory</a>
  </div>
</div>

<footer>
  <p>Fredericksburg Church Directory &mdash; Theological Due Diligence for Christian Men &mdash; <a href="https://usmcmin.org" style="color: var(--gold);">usmcmin.org</a></p>
  <p style="margin-top: 6px;">Last updated: 2026-04-04</p>
</footer>
</body>
</html>"""
    return html


# ===================== BATCH 1 =====================
batch1 = [
    {
        "id": "northside-baptist-fredericksburg",
        "name": "Northside Baptist Church (Fredericksburg)",
        "address": "445 Woodford St, Fredericksburg, VA 22401",
        "pastor": "Pastor Andrew Wheelis",
        "pastor_credentials": "Southern Baptist Convention ordained; seminary trained",
        "founded": "Unknown",
        "type": "Baptist / SBC",
        "denomination": "Southern Baptist Convention",
        "website": "https://www.northsidebaptist.net",
        "services": "Sunday School 9:30 AM, Morning 10:30 AM, Evening 5:30 PM, Wed 6:30 PM",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — SBC Affiliation, Verify Theology",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "green"
        },
        "score_notes": {
            "scripture": "SBC affirms inerrancy in BFM2000, but local adherence varies.",
            "gender": "SBC allows complementarianism but some churches drift on women's roles.",
            "denomination": "SBC — historically sound but has experienced TGC influence and social justice debates."
        },
        "assessment": "Northside Baptist Church is a Southern Baptist congregation located in Fredericksburg. As an SBC church, they subscribe to the Baptist Faith and Message 2000, which affirms biblical inerrancy and complementarian leadership. However, the SBC has faced significant theological drift in recent years, with some churches embracing TGC social justice frameworks and weakening on gender roles. This church should be visited and vetted personally. The multiple service times suggest an active, traditional Baptist schedule. Verify the pastor's theology on gender, Scripture, and the sufficiency of the gospel before committing.",
        "tags": ["sbc", "baptist", "fredericksburg", "traditional", "22401"],
        "gender_detail": "SBC complementarian by confession — local practice requires verification",
        "denomination_detail": "Southern Baptist Convention member church",
        "engagement": {
            "researched_website": True,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "spotsylvania-baptist-church",
        "name": "Spotsylvania Baptist Church",
        "address": "9223 Spotsylvania Baptist Rd, Spotsylvania, VA 22553",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist / SBC",
        "denomination": "Southern Baptist Convention",
        "website": "https://www.facebook.com/spotsylvaniabaptistchurch",
        "services": "Sundays (times unconfirmed — check Facebook page)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information Available",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Member of SBC and Southern Baptist Conservatives of Virginia — a more conservative SBC branch.",
            "cultural": "SBCV membership suggests conservative direction; verify locally."
        },
        "assessment": "Spotsylvania Baptist Church is a member of the Southern Baptist Convention and the Southern Baptist Conservatives of Virginia (SBCV), which is the more theologically conservative branch of the SBC in Virginia. SBCV affiliation is a positive signal — they have pushed back against progressive drift within the SBC. However, limited information is available on this congregation, so personal investigation is required. The SBCV connection warrants a cautious optimism. Visit and verify.",
        "tags": ["sbc", "sbcv", "baptist", "spotsylvania", "22553"],
        "gender_detail": "SBCV conservative SBC member — likely complementarian",
        "denomination_detail": "SBC / Southern Baptist Conservatives of Virginia",
        "engagement": {
            "researched_website": True,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "calvary-baptist-spotsylvania",
        "name": "Calvary Baptist Church (Spotsylvania)",
        "address": "10606 Benchmark Rd, Spotsylvania, VA 22553",
        "pastor": "Unknown (formerly Pastor Ron Owens)",
        "pastor_credentials": "Crown College of the Bible (Powell, TN) — IFB-adjacent training",
        "founded": "Unknown",
        "type": "Independent Baptist",
        "denomination": "Independent Baptist",
        "website": "https://www.clvry.org",
        "services": "Sundays (check website for times)",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Solid — Independent Baptist, KJV-Friendly",
        "scores": {
            "christology": "green",
            "scripture": "green",
            "gender": "green",
            "leadership": "green",
            "soteriology": "green",
            "cultural": "green",
            "denomination": "green",
            "preaching": "green",
            "mens": "green",
            "mission": "green"
        },
        "score_notes": {
            "scripture": "Crown College of the Bible is an independent fundamental Baptist institution affirming KJV and strict inerrancy.",
            "gender": "IFB tradition is strongly complementarian with male-only pastoral leadership.",
            "denomination": "Independent Baptist — no denominational accountability but historically maintains conservative doctrine.",
            "preaching": "IFB tradition emphasizes expository and evangelistic preaching."
        },
        "assessment": "Calvary Baptist Church Spotsylvania is an independent Baptist congregation whose leadership has been trained at Crown College of the Bible in Powell, TN — an institution associated with independent fundamental Baptist convictions, including KJV-only theology in many cases. The church has a strong heritage of conservative doctrine: male-only pastoral leadership, high view of Scripture, and traditional Baptist ecclesiology. The church plant that grew from this congregation speaks to the ministry fruitfulness of its model. This is one of the stronger conservative options in Spotsylvania County. Highly recommended for investigation.",
        "tags": ["independent-baptist", "ifb", "spotsylvania", "conservative", "22553"],
        "gender_detail": "Independent Baptist — male-only pastoral leadership is standard in this tradition",
        "denomination_detail": "Independent Baptist Church — no denominational affiliation",
        "engagement": {
            "researched_website": True,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "craigs-baptist-church",
        "name": "Craigs Baptist Church",
        "address": "14120 W Catharpin Rd, Spotsylvania, VA 22553",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist / SBC",
        "denomination": "Southern Baptist Convention",
        "website": "https://www.facebook.com/craigschurch",
        "services": "Sundays (services held at Community Life Center — check Facebook)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — SBC, Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "SBC affiliation — verify local theological stance independently.",
            "cultural": "No information on DEI/social justice language available."
        },
        "assessment": "Craigs Baptist Church is a Baptist congregation in Spotsylvania County meeting at their Community Life Center on West Catharpin Road. Limited doctrinal information is available publicly. As with many SBC-affiliated churches, the denominational label provides a framework (BFM2000) but does not guarantee conservative local practice. This church should be visited in person to assess preaching content, gender leadership, and cultural alignment. The rural/suburban Spotsylvania location may favor more traditional practice.",
        "tags": ["sbc", "baptist", "spotsylvania", "22553"],
        "gender_detail": "Unknown — SBC affiliation requires local verification",
        "denomination_detail": "Southern Baptist Convention",
        "engagement": {
            "researched_website": True,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "travelers-rest-baptist-spotsylvania",
        "name": "Travelers Rest Baptist Church",
        "address": "6823 Partlow Rd, Spotsylvania, VA 22553",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "https://www.facebook.com/TravelersRestBC",
        "services": "Sundays (check Facebook for times)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — Traditional Baptist, Limited Data",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "green"
        },
        "score_notes": {
            "mission": "Church mission statement emphasizes proclaiming truth and extending God's Kingdom.",
            "denomination": "Baptist affiliation — specific convention membership unclear."
        },
        "assessment": "Travelers Rest Baptist Church is located on Partlow Road in the rural Spotsylvania area. Their stated mission — 'Glorifying God and extending His Kingdom by living and proclaiming His truth to the world' — is solid and gospel-centered. The rural Spotsylvania location typically correlates with more traditional Baptist practice. Limited information is available on this congregation, so a personal visit is the best way to assess pastoral leadership, theological stance, and congregational culture. Worth investigating given the strong mission language.",
        "tags": ["baptist", "spotsylvania", "partlow", "rural", "22553"],
        "gender_detail": "Unknown — verify pastoral gender and leadership structure",
        "denomination_detail": "Baptist — specific convention affiliation unclear",
        "engagement": {
            "researched_website": True,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "kings-highway-baptist-fredericksburg",
        "name": "Kings Highway Baptist Church",
        "address": "15 Pine Rd, Fredericksburg, VA 22405",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": False,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Baptist affiliation — specific convention unknown.",
            "scripture": "No website or public doctrinal statement found."
        },
        "assessment": "Kings Highway Baptist Church is located on Pine Road in the Fredericksburg area (22405 zip). Limited public information is available for this congregation. No website was found during research. The Baptist name and Fredericksburg-area location suggest a traditional evangelical congregation, but doctrinal stance, pastoral leadership, and theological orientation cannot be confirmed without a personal visit. Recommend visiting in person to assess.",
        "tags": ["baptist", "fredericksburg", "22405"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Baptist — convention affiliation unknown",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "temple-baptist-fredericksburg",
        "name": "Temple Baptist Church",
        "address": "300 White Oak Rd, Fredericksburg, VA 22405",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Baptist name suggests traditional evangelical roots.",
            "scripture": "No public doctrinal information found."
        },
        "assessment": "Temple Baptist Church is located on White Oak Road in the Fredericksburg (22405) area. The 'Temple' name is common among traditional, conservative Baptist congregations — often associated with the independent or Southern Baptist tradition. Limited public information is available. No public website was found during research. A personal visit is required to assess the theological stance, pastoral leadership, and congregational health of this church.",
        "tags": ["baptist", "fredericksburg", "white-oak-road", "22405"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Baptist — specific convention unknown",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "ferry-farm-baptist-church",
        "name": "Ferry Farm Baptist Church",
        "address": "1 Westmoreland Dr, Fredericksburg, VA 22405",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist / SBC",
        "denomination": "Southern Baptist Convention",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed — located near Ferry Farm historic site)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — SBC, Limited Data",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "SBC affiliation likely — Baptist church in the Fredericksburg corridor.",
            "scripture": "No public doctrinal statement found."
        },
        "assessment": "Ferry Farm Baptist Church is located near the historic Ferry Farm property (George Washington's boyhood home) on the Stafford County side of Fredericksburg. Limited public information is available for this congregation. Baptist churches in this corridor are typically traditional in practice, but a personal visit is required to verify the pastoral theology, gender leadership, and doctrinal stance. The historic Fredericksburg-area location suggests traditional Baptist roots.",
        "tags": ["baptist", "sbc", "fredericksburg", "ferry-farm", "22405"],
        "gender_detail": "Unknown — SBC affiliation requires local verification",
        "denomination_detail": "Southern Baptist Convention (presumed based on location and Baptist listing)",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "friendship-baptist-fredericksburg",
        "name": "Friendship Baptist Church",
        "address": "11 Ridge Pointe Ln, Fredericksburg, VA 22405",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": False,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Baptist affiliation — specific convention unknown.",
            "cultural": "No public information on cultural or social justice stances."
        },
        "assessment": "Friendship Baptist Church is located on Ridge Pointe Lane in the Fredericksburg area (22405). The 'Friendship' name is common among African-American Baptist congregations in the South, though this cannot be confirmed from available data. Limited public information is available. No website was located during research. A personal visit is the best way to assess this congregation. The Fredericksburg-area location and Baptist name suggest a traditional evangelical background.",
        "tags": ["baptist", "fredericksburg", "22405"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Baptist — convention affiliation unknown",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "berea-baptist-church-fredericksburg",
        "name": "Berea Baptist Church",
        "address": "28 Fleet Rd, Fredericksburg, VA 22406",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "scripture": "The name 'Berea' references Acts 17:11 — Bereans who searched the Scriptures daily — a strong signal of high regard for biblical authority.",
            "denomination": "Baptist affiliation — convention membership unclear."
        },
        "assessment": "Berea Baptist Church is located on Fleet Road in the Fredericksburg area (22406 zip, western Fredericksburg/Culpeper County line). The name 'Berea' is drawn from Acts 17:11, where the Bereans were praised for examining the Scriptures daily — this is often chosen by congregations with a high view of biblical authority and expository preaching. A promising signal, though limited information is available. No public website was found. Recommend visiting to verify the theological stance and leadership structure.",
        "tags": ["baptist", "fredericksburg", "berea", "22406"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Baptist — specific convention unknown",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    }
]

# ===================== BATCH 2 =====================
batch2 = [
    {
        "id": "stafford-baptist-church",
        "name": "Stafford Baptist Church",
        "address": "478 Ramoth Church Rd, Stafford, VA 22554",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist / SBC",
        "denomination": "Southern Baptist Convention",
        "website": "https://www.staffordbaptistchurch.org",
        "services": "Sundays (check website for times)",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — SBC, Verify Theology",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "green"
        },
        "score_notes": {
            "mission": "Church description emphasizes Christ-centered worship and biblical teaching.",
            "denomination": "SBC member — holds to BFM2000 in principle, local practice requires verification."
        },
        "assessment": "Stafford Baptist Church is a Christ-centered SBC congregation in Stafford County, describing themselves as committed to 'Christ-centered worship, biblical teaching, and community for the whole family.' This is positive language that aligns with gospel-centered ministry. As an SBC church, they nominally hold to the Baptist Faith and Message 2000, which affirms complementarianism and biblical inerrancy. However, SBC drift in recent years means local practice must be verified. This church has a functional website and active ministry programs. Visit in person and assess the preaching content and gender leadership structure.",
        "tags": ["sbc", "baptist", "stafford", "22554"],
        "gender_detail": "SBC complementarian by confession — local practice requires personal verification",
        "denomination_detail": "Southern Baptist Convention",
        "engagement": {
            "researched_website": True,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "ramoth-baptist-church-stafford",
        "name": "Ramoth Baptist Church",
        "address": "478 Ramoth Church Rd, Stafford, VA 22554",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist / SBC",
        "denomination": "Southern Baptist Convention",
        "website": "https://rbcstafford.org",
        "services": "Sundays (check website for times; bilingual Spanish services available)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — SBC, Bilingual Ministry",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "green"
        },
        "score_notes": {
            "mission": "Church offers Polyglossia real-time translation — actively seeking to reach Spanish-speaking communities.",
            "cultural": "Bilingual ministry is commendable outreach, though Spanish-language congregations can sometimes trend charismatic or prosperity-adjacent."
        },
        "assessment": "Ramoth Baptist Church is a Stafford County SBC congregation that offers bilingual English and Spanish worship services using real-time translation technology (Polyglossia). The outreach to Hispanic communities is a gospel-centered mission initiative. The church is named 'Ramoth,' a biblical city of refuge (Joshua 20:8), suggesting traditional Baptist rootedness. However, bilingual SBC churches can sometimes reflect New Baptist Covenant or social justice influence. The Spanish-speaking ministry focus is positive for evangelism, but theology should be verified. Recommend a personal visit.",
        "tags": ["sbc", "baptist", "stafford", "bilingual", "spanish", "22554"],
        "gender_detail": "SBC affiliation — complementarian by confession, local verification needed",
        "denomination_detail": "Southern Baptist Convention",
        "engagement": {
            "researched_website": True,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "north-stafford-baptist-church",
        "name": "North Stafford Baptist Church",
        "address": "11 Meadowood Dr, Stafford, VA 22554",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist / SBC",
        "denomination": "Southern Baptist Convention",
        "website": "https://www.sbcv.org/churches/north-stafford-baptist-church/",
        "services": "Sundays (times unconfirmed — check for updated schedule)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — SBC, Limited Direct Data",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "SBC member listed with SBCV (Southern Baptist Conservatives of Virginia) — positive denominational signal.",
            "scripture": "No independent doctrinal statement reviewed."
        },
        "assessment": "North Stafford Baptist Church is a Southern Baptist congregation listed with the Southern Baptist Conservatives of Virginia (SBCV) — the more theologically conservative wing of Virginia SBC churches. SBCV membership is a positive indicator of theological conservatism. Located in the northern Stafford area, near the Meadowood development. Limited direct congregational data is available, but SBCV affiliation warrants optimistic investigation. Recommend a personal visit to verify pastoral theology and congregational practice.",
        "tags": ["sbc", "sbcv", "baptist", "stafford", "north-stafford", "22554"],
        "gender_detail": "SBCV member — complementarian by confession, likely conservative",
        "denomination_detail": "SBC / Southern Baptist Conservatives of Virginia",
        "engagement": {
            "researched_website": True,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "shiloh-new-site-stafford-va",
        "name": "Shiloh New Site Baptist Church (Stafford)",
        "address": "Stafford, VA 22554",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "https://www.shilohnsstaffordva.org",
        "services": "Sundays (check website for times)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — Traditional Baptist, Limited Data",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "green"
        },
        "score_notes": {
            "mission": "Church describes itself as serving God and His people with daily prayer and praise.",
            "denomination": "Baptist with Stafford County roots — specific convention affiliation unclear."
        },
        "assessment": "Shiloh New Site Baptist Church in Stafford is described as 'a body of baptized believers that serve God and His people with daily prayer and praise, with the knowledge that the power of God is moving in our lives.' This is traditional, Spirit-focused language consistent with the historic African-American Baptist tradition. The Shiloh name is common in Virginia Baptist history. Their emphasis on prayer and praise is commendable. Limited theological data is available. Recommend visiting to assess doctrinal stance and leadership structure. Note: This church is separate from the Fredericksburg Shiloh Baptist churches already in the directory.",
        "tags": ["baptist", "stafford", "traditional", "prayer", "22554"],
        "gender_detail": "Unknown — no public leadership information available",
        "denomination_detail": "Baptist — specific convention affiliation unclear",
        "engagement": {
            "researched_website": True,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "rock-hill-baptist-stafford",
        "name": "Rock Hill Baptist Church",
        "address": "12 Van Horn Ln, Stafford, VA 22556",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": False,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Baptist — convention affiliation unknown.",
            "scripture": "No public doctrinal information found."
        },
        "assessment": "Rock Hill Baptist Church is located in the northern Stafford County area (22556 zip). Limited public information is available. The 'Rock Hill' name is common in rural Virginia Baptist churches with colonial or Revolutionary-era roots. No website was found during research. A personal visit is required to assess the congregational theology, pastoral leadership, and doctrinal stance. The northern Stafford location is within the growth corridor between Stafford and Quantico.",
        "tags": ["baptist", "stafford", "22556"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Baptist — convention affiliation unknown",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "good-hope-church-spotsylvania",
        "name": "Good Hope Church (Spotsylvania)",
        "address": "5601 Courthouse Rd, Spotsylvania Courthouse, VA 22551",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist / SBC",
        "denomination": "Southern Baptist Convention",
        "website": "https://www.sbcv.org/churches/good-hope-church-spotsylvania/",
        "services": "Sundays (check website for times)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — SBC, Near Courthouse Area",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Listed with SBCV — the conservative wing of Virginia SBC.",
            "scripture": "SBC confessional standards affirm inerrancy via BFM2000."
        },
        "assessment": "Good Hope Church is an SBC congregation located near Spotsylvania Courthouse on Courthouse Road. The church is listed with the Southern Baptist Conservatives of Virginia (SBCV), a positive theological signal indicating alignment with the more conservative wing of the SBC in Virginia. The Spotsylvania Courthouse area has historic roots as a county seat, and this church likely serves the broader Spotsylvania community. SBCV listing warrants cautious optimism. Recommend visiting for personal theological assessment.",
        "tags": ["sbc", "sbcv", "spotsylvania", "courthouse", "22551"],
        "gender_detail": "SBCV member — likely complementarian in practice",
        "denomination_detail": "SBC / Southern Baptist Conservatives of Virginia",
        "engagement": {
            "researched_website": True,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "hebron-baptist-spotsylvania",
        "name": "Hebron Baptist Church (Spotsylvania)",
        "address": "Spotsylvania, VA 22551",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "https://www.facebook.com/hebronchurch",
        "services": "Sundays (check Facebook for times)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — Traditional Baptist, Near Lake Anna",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "green"
        },
        "score_notes": {
            "mission": "Facebook page states 'a church that loves Jesus Christ' — mission-focused language.",
            "denomination": "Baptist congregation near Lake Anna in Spotsylvania County."
        },
        "assessment": "Hebron Baptist Church is a Baptist congregation located near Lake Anna in Spotsylvania County. Their Facebook page describes them as 'a church that loves Jesus Christ' — simple, Christ-centered identity. 'Hebron' is a biblically significant name (site of Abraham's covenant with God in Canaan), chosen by many traditional Baptist churches with deep roots. The Lake Anna area of Spotsylvania is rural and traditionally conservative. Limited information is available, so a personal visit is recommended to assess theology and leadership. The rural setting typically favors more traditional Baptist practice.",
        "tags": ["baptist", "spotsylvania", "lake-anna", "rural", "22551"],
        "gender_detail": "Unknown — rural Baptist, likely traditional in practice",
        "denomination_detail": "Baptist — convention affiliation unclear",
        "engagement": {
            "researched_website": True,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "sylvania-heights-baptist",
        "name": "Sylvania Heights Baptist Church",
        "address": "150 Church St, Fredericksburg, VA 22408",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": False,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Baptist affiliation — specific convention unknown.",
            "scripture": "No public doctrinal information found."
        },
        "assessment": "Sylvania Heights Baptist Church is located on Church Street in the Fredericksburg area (22408 zip code, east/south Fredericksburg). The 22408 zip encompasses areas near the Route 1 corridor including the Massaponax and South Stafford areas. Limited public information is available for this congregation. No website was found during research. A personal visit is required to assess the theology, pastoral leadership, and congregational culture. The 'Heights' name and Baptist affiliation suggest a neighborhood congregation.",
        "tags": ["baptist", "fredericksburg", "22408"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Baptist — convention affiliation unknown",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "cornerstone-baptist-fredericksburg",
        "name": "Cornerstone Baptist Church (Fredericksburg)",
        "address": "56 McWhirt Loop, Fredericksburg, VA 22406",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Baptist — convention affiliation unknown. Note: distinct from Cornerstone Chapel (Apostolic) already in directory.",
            "scripture": "No public doctrinal statement found."
        },
        "assessment": "Cornerstone Baptist Church is located on McWhirt Loop in the western Fredericksburg area (22406 zip). This is distinct from the Cornerstone Chapel, an Apostolic Church already in the directory. The 'Cornerstone' name references Christ as the chief cornerstone (Ephesians 2:20) — a common name among conservative evangelical Baptist churches. McWhirt Loop area is in the western Fredericksburg growth corridor. No public website was found during research. A personal visit is recommended to assess theology and leadership structure.",
        "tags": ["baptist", "fredericksburg", "22406"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Baptist — convention affiliation unknown",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "hartwood-presbyterian-church",
        "name": "Hartwood Presbyterian Church",
        "address": "50 Hartwood Church Rd, Fredericksburg, VA 22406",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "1741",
        "type": "Presbyterian",
        "denomination": "Presbyterian Church (USA) — Historical",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed — historic rural church)",
        "has_mens_ministry": False,
        "has_kids_ministry": False,
        "overall_rating": "yellow",
        "overall_label": "Caution — Historic Church, PCUSA Affiliation Concerns",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "red",
            "leadership": "red",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "red",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Hartwood Presbyterian is historically associated with PCUSA which is a liberal mainline denomination that ordains women and affirms LGBTQ+ clergy.",
            "gender": "PCUSA ordains women as pastors and elders — automatic concern.",
            "scripture": "PCUSA does not affirm biblical inerrancy — significant doctrinal weakness.",
            "cultural": "PCUSA formally affirmed same-sex marriage in 2015 — a serious disqualifier."
        },
        "assessment": "Hartwood Presbyterian Church is one of the oldest Presbyterian congregations in Virginia, dating to 1741. The church is located on the historic Hartwood Church Road in the rural western Fredericksburg area. While the historic Calvinist roots of this congregation are noteworthy, if affiliated with the Presbyterian Church (USA) — PCUSA — this church has serious theological disqualifiers. The PCUSA ordains women as pastors and elders and formally affirmed same-sex marriage in 2015. Historic congregations sometimes retain PCUSA affiliation while holding more conservative views, but the denominational framework is compromised. Investigate actual current leadership and doctrinal stance before visiting.",
        "tags": ["presbyterian", "pcusa", "historic", "fredericksburg", "22406", "1741"],
        "gender_detail": "PCUSA ordains women as pastors and elders — does not hold to complementarianism",
        "denomination_detail": "Presbyterian Church (USA) — liberal mainline denomination",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    }
]

# ===================== BATCH 3 =====================
batch3 = [
    {
        "id": "spotsylvania-presbyterian-church",
        "name": "Spotsylvania Presbyterian Church",
        "address": "11121 Leavells Rd, Fredericksburg, VA 22407",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Presbyterian",
        "denomination": "Presbyterian — Affiliation Unknown",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": False,
        "overall_rating": "yellow",
        "overall_label": "Caution — Presbyterian Affiliation Requires Verification",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Presbyterian affiliation — must verify whether PCA, EPC, PCUSA, or independent. This is critical for rating.",
            "gender": "If PCA/EPC: male-only ordination. If PCUSA: ordains women. Must verify.",
            "scripture": "Reformed theology affirms inerrancy (WCF), but PCUSA has abandoned this historically."
        },
        "assessment": "Spotsylvania Presbyterian Church is located on Leavells Road in the Fredericksburg/Spotsylvania area. The critical question for this congregation is denominational affiliation: if PCA (Presbyterian Church in America) or EPC (Evangelical Presbyterian Church), this church would be a strong green candidate with Reformed theology, male-only ordination, and high regard for Scripture. If PCUSA (Presbyterian Church USA), it would be red due to female ordination and affirmation of same-sex marriage. No website was found to confirm. This must be verified before any recommendation can be made.",
        "tags": ["presbyterian", "spotsylvania", "leavells-road", "22407"],
        "gender_detail": "Unknown — critical to determine PCA/EPC vs PCUSA affiliation",
        "denomination_detail": "Presbyterian — affiliation (PCA vs PCUSA) must be verified",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "bethlehem-baptist-spotsylvania",
        "name": "Bethlehem Baptist Church (Spotsylvania)",
        "address": "Spotsylvania, VA 22551",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "https://www.facebook.com/p/Bethlehem-Baptist-Church-Spotsylvania-VA-100064781374186",
        "services": "Sundays (check Facebook for times)",
        "has_mens_ministry": False,
        "has_kids_ministry": False,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Baptist — Spotsylvania area, convention affiliation unclear.",
            "scripture": "No doctrinal statement available from Facebook page."
        },
        "assessment": "Bethlehem Baptist Church in Spotsylvania is a Baptist congregation with a limited online presence (Facebook only). The name 'Bethlehem' — 'house of bread' — is historically significant and common among traditional Baptist churches. Located in Spotsylvania County. Limited information is available beyond a basic Facebook page with approximately 389 followers. This suggests a smaller, traditional Baptist congregation. A personal visit is the best way to assess the church's theology, pastoral leadership, and congregational health. Note: distinct from Bethlehem Baptist Richmond in the directory.",
        "tags": ["baptist", "spotsylvania", "22551"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Baptist — convention affiliation unknown",
        "engagement": {
            "researched_website": True,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "fellowship-baptist-spotsylvania",
        "name": "Fellowship Baptist Church (Spotsylvania)",
        "address": "13737 Post Oak Rd, Spotsylvania, VA 22553",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": False,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Baptist congregation in rural Spotsylvania on Post Oak Road.",
            "scripture": "No website or public doctrinal information found."
        },
        "assessment": "Fellowship Baptist Church is located on Post Oak Road in Spotsylvania County (22553). 'Fellowship' is a common Baptist name emphasizing community in Christ. Located in the rural/semi-rural Spotsylvania area. No website was found during research. A personal visit is required to assess this congregation. Rural Spotsylvania Baptist churches typically lean more traditional and conservative than urban counterparts, but this should be verified personally.",
        "tags": ["baptist", "spotsylvania", "22553"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Baptist — convention affiliation unknown",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "fairview-baptist-fredericksburg",
        "name": "Fairview Baptist Church",
        "address": "900 Charlotte St, Fredericksburg, VA 22401",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": False,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Baptist congregation on Charlotte Street in central Fredericksburg.",
            "scripture": "No public doctrinal information found."
        },
        "assessment": "Fairview Baptist Church is located on Charlotte Street in central Fredericksburg (22401). Charlotte Street is in the historic district area of Fredericksburg. 'Fairview' is a common traditional Baptist church name in Virginia. Limited public information is available. No website was found. The central Fredericksburg location means this church likely serves a neighborhood congregation. A personal visit is required to assess the theology and leadership structure.",
        "tags": ["baptist", "fredericksburg", "22401"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Baptist — convention affiliation unknown",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "kingdom-baptist-fredericksburg",
        "name": "Kingdom Baptist Church",
        "address": "1717 Stafford Ave, Fredericksburg, VA 22401",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": False,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "green"
        },
        "score_notes": {
            "mission": "The 'Kingdom' name emphasizes the reign of God — typically mission-focused.",
            "denomination": "Baptist — specific convention unknown."
        },
        "assessment": "Kingdom Baptist Church is located on Stafford Avenue in Fredericksburg (22401). 'Kingdom Baptist' is a name that emphasizes the Kingdom of God, which can reflect either a Reformed/gospel-centered theology (Kingdom as Christ's redemptive reign) or a kingdom dominion/social justice framework. The Stafford Avenue corridor connects Fredericksburg to the surrounding area. Limited public information is available. No website was found during research. A personal visit and pastoral interview would help determine the theological direction of this congregation.",
        "tags": ["baptist", "fredericksburg", "stafford-ave", "22401"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Baptist — convention affiliation unknown",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "new-destiny-baptist-fredericksburg",
        "name": "New Destiny Baptist Church",
        "address": "Fredericksburg, VA 22401",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "https://www.newdestinyva.org",
        "services": "Sundays (check website for times)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — 'Destiny' Language Warrants Verification",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "green"
        },
        "score_notes": {
            "mission": "Website emphasizes 'bringing glory to God by making disciples of Jesus who follow Him, are changed by Him, and are committed to His mission' — strong Great Commission language.",
            "soteriology": "The emphasis on being 'changed by Him' suggests a sanctification-aware soteriology.",
            "cultural": "'Destiny' language can signal Word of Faith or charismatic/prosperity influence — requires verification."
        },
        "assessment": "New Destiny Baptist Church in Fredericksburg has a website with strong disciple-making language: 'bringing glory to God by making disciples of Jesus who follow Him, are changed by Him, and are committed to His mission.' This is excellent Great Commission framing. However, the word 'Destiny' in a church name — particularly in Baptist/charismatic contexts — can sometimes signal Word of Faith, prosperity gospel, or New Apostolic Reformation influence. This must be verified. The discipleship emphasis is encouraging. Recommend a website review for doctrinal statement, and a personal visit to assess preaching and culture.",
        "tags": ["baptist", "fredericksburg", "22401", "destiny"],
        "gender_detail": "Unknown — no public leadership gender data available",
        "denomination_detail": "Baptist — convention affiliation unclear",
        "engagement": {
            "researched_website": True,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "mt-hope-baptist-fredericksburg",
        "name": "Mt. Hope Baptist Church (Fredericksburg)",
        "address": "6823 Harrison Rd, Fredericksburg, VA 22407",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": False,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Baptist congregation on Harrison Road in western Fredericksburg area.",
            "scripture": "No public website or doctrinal information found."
        },
        "assessment": "Mt. Hope Baptist Church is located on Harrison Road in the western Fredericksburg area (22407). 'Mt. Hope' or 'Mount Hope' is a traditional Virginia Baptist church name, often associated with African-American Baptist congregations. The 22407 zip encompasses the western Fredericksburg growth corridor including areas around Plank Road and Harrison Road. Limited information is available. No website found. A personal visit is required to assess this congregation.",
        "tags": ["baptist", "fredericksburg", "22407", "harrison-road"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Baptist — convention affiliation unknown",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "first-christian-fredericksburg",
        "name": "First Christian Church (Fredericksburg)",
        "address": "1501 Washington Ave, Fredericksburg, VA 22401",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Christian Church / Disciples of Christ",
        "denomination": "Christian Church (Disciples of Christ) or Churches of Christ",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — Denomination Affiliation Requires Verification",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Critical distinction: 'Churches of Christ' (non-instrumental) = conservative; 'Christian Church/Disciples of Christ' (DOC) = liberal mainline. Must determine which.",
            "gender": "DOC ordains women; conservative Churches of Christ are typically male-only leadership.",
            "scripture": "DOC has abandoned biblical inerrancy; conservative Church of Christ affirms biblical authority."
        },
        "assessment": "First Christian Church on Washington Avenue in Fredericksburg could belong to either the conservative Churches of Christ (acapella, non-instrumental) tradition or the liberal Christian Church/Disciples of Christ (DOC) denomination. This distinction is critically important: the DOC is a liberal mainline denomination that ordains women, affirms LGBTQ+ inclusion, and does not affirm biblical inerrancy. The conservative Churches of Christ, while holding some distinctive practices (acapella worship, baptismal regeneration), maintain male-only leadership and high regard for Scripture. This church requires immediate verification of denominational affiliation before any recommendation can be made.",
        "tags": ["christian-church", "fredericksburg", "washington-ave", "22401"],
        "gender_detail": "Unknown — critical to determine DOC vs conservative Churches of Christ affiliation",
        "denomination_detail": "Denomination affiliation unknown — must verify: DOC (liberal) vs Churches of Christ (conservative)",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "second-new-hope-baptist",
        "name": "Second New Hope Baptist Church",
        "address": "3836 Summit Crossing Rd, Fredericksburg, VA 22408",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": False,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Baptist — convention affiliation unknown.",
            "scripture": "No public doctrinal information available."
        },
        "assessment": "Second New Hope Baptist Church is located on Summit Crossing Road in the Fredericksburg area (22408), near the Route 1 South corridor. 'New Hope' is a historic name among Virginia Baptist churches, and the 'Second' prefix indicates a church plant or breakaway from an original New Hope congregation — a common pattern in African-American Baptist church history. Limited public information is available. No website was found. A personal visit is required to assess this congregation's theology and pastoral leadership.",
        "tags": ["baptist", "fredericksburg", "22408"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Baptist — convention affiliation unknown",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "open-door-baptist-leavells",
        "name": "Open Door Baptist Church (Leavells Rd)",
        "address": "10210 Leavells Rd, Fredericksburg, VA 22407",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": False,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Baptist congregation on Leavells Road in western Fredericksburg.",
            "scripture": "No public website or doctrinal statement found."
        },
        "assessment": "Open Door Baptist Church is located on Leavells Road in the Fredericksburg area (22407 zip), the western growth corridor of the city. The 'Open Door' name can reference Revelation 3:8 — Christ setting before the church an open door — a positive missional image. However, it can also suggest an overly inclusive or seeker-driven approach to ministry. No public website was found. Limited information is available. A personal visit is required to assess this congregation. Note: distinct from Open Door Community Church already in the directory.",
        "tags": ["baptist", "fredericksburg", "leavells-road", "22407"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Baptist — convention affiliation unknown",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    }
]

# ===================== BATCH 4 =====================
batch4 = [
    {
        "id": "zoan-baptist-church",
        "name": "Zoan Baptist Church",
        "address": "5888 Plank Rd, Fredericksburg, VA 22407",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": False,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Baptist congregation on Plank Road in western Fredericksburg.",
            "scripture": "No public website or doctrinal information found."
        },
        "assessment": "Zoan Baptist Church is located on Plank Road in the Fredericksburg area (22407). 'Zoan' is a biblical name — an ancient Egyptian city mentioned in Numbers 13:22 and the Psalms. Churches using obscure biblical place names are often steeped in deep scriptural knowledge. The Plank Road corridor (Route 3 west) is a growth area for Fredericksburg churches. No public website was found. A personal visit is required to assess the theological direction and pastoral leadership of this congregation.",
        "tags": ["baptist", "fredericksburg", "plank-road", "22407"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Baptist — convention affiliation unknown",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "choice-baptist-church-fredericksburg",
        "name": "Choice Baptist Church",
        "address": "16 Burton Loop, Fredericksburg, VA 22406",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": False,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Baptist congregation in the western Fredericksburg area (22406).",
            "scripture": "No public website or doctrinal statement found."
        },
        "assessment": "Choice Baptist Church is located on Burton Loop in the Fredericksburg area (22406), the rural/western Fredericksburg corridor. The name 'Choice' is an unusual one for a Baptist church — it may reference Joshua 24:15 ('choose this day whom you will serve') or reflect a particular emphasis on personal decision. Limited public information is available. No website was found. A personal visit is required to assess the theology, pastoral leadership, and congregational direction of this church.",
        "tags": ["baptist", "fredericksburg", "22406"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Baptist — convention affiliation unknown",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "liberty-baptist-stafford",
        "name": "Liberty Baptist Church (Stafford)",
        "address": "Stafford, VA 22554",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Baptist",
        "denomination": "Baptist",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Baptist congregation in Stafford County — specific convention unknown.",
            "cultural": "'Liberty' churches in the Baptist tradition often have strong First Amendment and Christian freedom convictions."
        },
        "assessment": "Liberty Baptist Church in Stafford is listed in local directories for the Stafford, VA 22554 area. 'Liberty Baptist' churches in Virginia are often conservative, patriotic-leaning congregations with strong commitments to religious freedom and First Amendment rights. The name can also reference freedom in Christ (Galatians 5:1). Limited public information is available. No website was found. Recommend a personal visit to assess the theology and pastoral leadership. Liberty Baptist churches in the Virginia tradition are often traditional and evangelistic.",
        "tags": ["baptist", "stafford", "22554", "liberty"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Baptist — convention affiliation unknown",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "abundant-life-assembly-stafford",
        "name": "Abundant Life Assembly of God",
        "address": "200 Onville Rd, Stafford, VA 22556",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Pentecostal / Assembly of God",
        "denomination": "Assemblies of God",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — AG/Pentecostal, Verify Leadership Structure",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "green"
        },
        "score_notes": {
            "gender": "Assemblies of God officially permits women as pastors — a concern for complementarian men.",
            "scripture": "AG affirms biblical inspiration but is not a strict inerrancy denomination.",
            "soteriology": "AG holds an Arminian soteriology — salvation can be lost.",
            "mission": "AG churches are typically very missions-focused with strong evangelism emphasis.",
            "denomination": "Assemblies of God is a well-organized Pentecostal denomination with accountability structures."
        },
        "assessment": "Abundant Life Assembly of God is an Assemblies of God congregation in Stafford County (22556). The AG is the world's largest Pentecostal denomination, known for strong evangelism, missions commitment, and charismatic worship. However, the AG officially permits women as pastors and elders — a significant concern for those committed to complementarian church government. 'Abundant Life' language can also signal Word of Faith or prosperity gospel influence, though this is not universal in the AG. The name warrants verification of the church's stance on prosperity theology and women's ordination before investing.",
        "tags": ["assemblies-of-god", "pentecostal", "stafford", "22556"],
        "gender_detail": "Assemblies of God permits women as pastors — complementarianism not guaranteed",
        "denomination_detail": "Assemblies of God — Pentecostal denomination",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "north-stafford-church-of-christ",
        "name": "North Stafford Church of Christ",
        "address": "325 Courthouse Rd, Stafford, VA 22554",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Church of Christ",
        "denomination": "Churches of Christ (Non-Instrumental)",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — Conservative but Distinct Soteriology",
        "scores": {
            "christology": "green",
            "scripture": "green",
            "gender": "green",
            "leadership": "green",
            "soteriology": "yellow",
            "cultural": "green",
            "denomination": "yellow",
            "preaching": "green",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "scripture": "Churches of Christ hold a high view of Scripture as final authority, though not typically framed as 'inerrancy.'",
            "gender": "Conservative Churches of Christ maintain male-only leadership — elders and deacons must be men.",
            "soteriology": "Churches of Christ typically hold to baptismal regeneration (baptism required for salvation) — a significant doctrinal distinction.",
            "denomination": "Non-instrumental Churches of Christ have no formal denominational hierarchy — each congregation is autonomous.",
            "leadership": "Elder-led structure with male-only elders is standard in conservative Churches of Christ."
        },
        "assessment": "North Stafford Church of Christ is a non-instrumental Church of Christ congregation on Courthouse Road in Stafford County. The conservative Churches of Christ tradition has much to commend it: high regard for Scripture, male-only eldership and deaconship, acapella worship emphasizing textual authority, strong doctrinal commitment, and anti-cultural-drift. However, the key theological distinction is baptismal regeneration — the belief that water baptism is essential for salvation. This differs from evangelical Protestant doctrine that salvation is by grace alone through faith alone. This theological difference is significant and should be discussed with potential members before joining. Complementarian men will find the male leadership structure affirming.",
        "tags": ["church-of-christ", "stafford", "22554", "non-instrumental", "conservative"],
        "gender_detail": "Male-only elders and deacons — strongly complementarian in practice",
        "denomination_detail": "Churches of Christ (non-instrumental) — autonomous congregation",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "winding-creek-community-stafford",
        "name": "Winding Creek Community Church",
        "address": "392 Garrisonville Rd, Stafford, VA 22554",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Non-Denominational / Community Church",
        "denomination": "Non-Denominational",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — Non-Denominational, Verify Theology",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Non-denominational community church — no external doctrinal accountability.",
            "cultural": "Winding Creek is a community name in the Garrisonville corridor of Stafford — likely a neighborhood church."
        },
        "assessment": "Winding Creek Community Church is a non-denominational congregation on Garrisonville Road in Stafford (22554). The Garrisonville corridor is a major growth area in Stafford County. 'Community Church' designations are typically non-denominational and can range from solidly evangelical to therapeutic/progressive in theology. The lack of denominational affiliation means all theological verification must be done locally. No website was found during research. A personal visit and review of statement of faith are essential before joining or recommending this church.",
        "tags": ["non-denominational", "stafford", "garrisonville", "22554"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Non-denominational — independent congregation",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "living-word-fellowship-fredericksburg",
        "name": "Living Word Fellowship Church",
        "address": "1500 Stafford Ave, Fredericksburg, VA 22401",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Non-Denominational / Charismatic",
        "denomination": "Non-Denominational",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — 'Living Word' Name May Signal Charismatic/WoF",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "scripture": "'Living Word' can reference John 1:1 (Christ as the Word) or can be associated with charismatic/Word of Faith movements that emphasize prophetic 'living words.'",
            "soteriology": "Word of Faith churches often teach a distorted prosperity gospel — requires verification.",
            "denomination": "Non-denominational — no external doctrinal accountability."
        },
        "assessment": "Living Word Fellowship Church is located on Stafford Avenue in Fredericksburg (22401). The name 'Living Word' can be richly theological — referencing Christ as the Living Word (John 1) or the Bible as the living and active Word (Hebrews 4:12). However, 'Living Word' combined with 'Fellowship' is also a common naming pattern in Word of Faith and charismatic renewal circles. No website was found to verify doctrinal content. A thorough investigation is warranted before engagement — review any available statement of faith and attend a service to assess preaching content and worship culture.",
        "tags": ["non-denominational", "fredericksburg", "stafford-ave", "22401"],
        "gender_detail": "Unknown — no public information available",
        "denomination_detail": "Non-denominational — independent congregation",
        "engagement": {
            "researched_website": False,
            "attended_personally": False,
            "attended_services": False,
            "visited_facility": False,
            "interacted_with_leadership": False,
            "know_members_personally": False,
            "viewed_online_services": False
        }
    },
    {
        "id": "riverside-church-fredericksburg",
        "name": "Riverside Church (Fredericksburg)",
        "address": "3461 Fall Hill Ave, Fredericksburg, VA 22401",
        "pastor": "Unknown",
        "pastor_credentials": "Unknown",
        "founded": "Unknown",
        "type": "Non-Denominational",
        "denomination": "Non-Denominational",
        "website": "Not Available",
        "services": "Sundays (times unconfirmed)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — Limited Information",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
