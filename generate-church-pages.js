#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'docs/data/churches.json'), 'utf8'));
const outDir = path.join(__dirname, 'docs/churches');

function colorClass(score) {
  if (score === 'green') return 'score-green';
  if (score === 'red') return 'score-red';
  if (score === 'black') return 'score-black';
  return 'score-yellow';
}

// Inline icon helper
function ico(name, size=16) {
  return `<img class="site-icon" src="/assets/icons/${name}" alt="" width="${size}" height="${size}" style="vertical-align:middle;">`;
}

function colorLabel(score) {
  if (score === 'green') return `${ico('shield-chain-salvation-48.png')} Strong`;
  if (score === 'red') return `${ico('shield-warning-48.png')} Concern`;
  if (score === 'black') return `${ico('shield-warning-48.png')} Disqualifier`;
  return `${ico('shield-chain-faith-48.png')} Caution`;
}

function ratingBadgeClass(r) {
  if (r === 'green') return 'rating-green';
  if (r === 'red') return 'rating-red';
  if (r === 'black') return 'rating-black';
  return 'rating-yellow';
}

function ratingIcon(r) {
  if (r === 'green') return ico('shield-chain-salvation-48.png', 18);
  if (r === 'red') return ico('shield-warning-48.png', 18);
  if (r === 'black') return ico('shield-warning-48.png', 18);
  return ico('shield-chain-faith-48.png', 18);
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// Iraq threat zone badge — prominently display overall rating
function threatBadge(church) {
  const cls = ratingBadgeClass(church.overall_rating);
  const icon = ratingIcon(church.overall_rating);
  const label = escapeHtml(church.overall_label || church.overall_rating.toUpperCase());
  return `<div class="threat-badge ${cls}">
    <span class="threat-icon">${icon}</span>
    <span class="threat-label">${label}</span>
  </div>`;
}

// Verification badge — shows how this church was verified
function verificationBadge(church) {
  const e = church.engagement || {};
  if (e.attended_personally || e.attended_services || e.know_members_personally || e.visited_facility) {
    return `<div class="verification-badge moop-verified" title="Personally verified by MOOP">
      <img src="/assets/icons/shield-chain-faith-48.png" alt="" width="14" height="14" style="vertical-align:middle;filter:brightness(1.5);"> MOOP Verified
    </div>`;
  }
  if (e.researched_website || e.viewed_online_services || (church.website && String(church.website).startsWith('http'))) {
    return `<div class="verification-badge web-verified" title="Verified via website and public data">
      <img src="/assets/icons/shield-checklist-48.png" alt="" width="14" height="14" style="vertical-align:middle;filter:brightness(1.3);"> Web Verified
    </div>`;
  }
  return `<div class="verification-badge unverified" title="Not yet verified — data is preliminary">
      <img src="/assets/icons/shield-chain-faith-48.png" alt="" width="14" height="14" style="vertical-align:middle;opacity:0.5;"> Unverified
  </div>`;
}

// Engagement detail section — explains exactly how verification was done
function engagementSection(church) {
  const e = church.engagement || {};
  const checks = [
    { key: 'visited_facility', label: 'Visited the facility in person', icon: ico('shield-church-48.png', 14) },
    { key: 'attended_services', label: 'Attended a worship service', icon: ico('shield-cross-48.png', 14) },
    { key: 'viewed_online_services', label: 'Watched online sermons/services', icon: ico('shield-globe-48.png', 14) },
    { key: 'researched_website', label: 'Researched church website', icon: ico('shield-checklist-48.png', 14) },
    { key: 'know_members_personally', label: 'Personally knows church members', icon: ico('shield-handshake-48.png', 14) },
    { key: 'interacted_with_leadership', label: 'Interacted with church leadership', icon: ico('shield-about-person-48.png', 14) },
  ];

  const hasAny = checks.some(c => e[c.key]);
  if (!hasAny) return '';

  // Only show rows that are checked (true) — no greyed-out items
  const rows = checks.filter(c => e[c.key]).map(c => {
    return `<div class="engage-row" style="display:flex;align-items:center;gap:8px;padding:6px 0;">
      <span style="color:var(--green);font-weight:700;font-size:0.9rem;">&#10003;</span>
      <span style="color:var(--white);font-size:0.85rem;">${escapeHtml(c.label)}</span>
    </div>`;
  }).join('');

  return `<div class="card" style="margin-top:28px;">
    <div class="card-title"><img class="site-icon" src="/assets/icons/shield-chain-faith-48.png" alt="" width="20" height="20"> MOOP Engagement Tracker</div>
    <p style="color:var(--gray);font-size:0.82rem;margin-bottom:12px;">How this church was personally verified by the MOOP directory team:</p>
    ${rows}
  </div>`;
}

function mapSrc(address) {
  return `https://maps.google.com/maps?q=${encodeURIComponent(address)}&output=embed`;
}

const NAV = `<nav class="top-nav">
    <a href="/churches.html">← Church Directory</a>
    <a href="/index.html">Home</a>
    <a href="/bible.html">Bible Translation Engine</a>
    <a href="/usmc-ministries.html">U.S.M.C. Ministries</a>
    <a href="/about.html">About</a>
    <a href="/connect.html">Connect</a>
</nav>`;

const CSS = `
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  :root {
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
  }
  body {
    font-family: 'Inter', sans-serif;
    background: var(--bg);
    color: var(--white);
    line-height: 1.7;
    min-height: 100vh;
  }
  h1, h2, h3, h4 { font-family: 'Playfair Display', serif; }

  /* Nav */
  .top-nav {
    display: flex; flex-wrap: wrap; gap: 6px;
    justify-content: center; padding: 14px 20px;
    border-bottom: 1px solid var(--border);
    background: rgba(0,0,0,0.95);
    position: sticky; top: 0; z-index: 100;
  }
  .top-nav a {
    color: var(--gray); text-decoration: none; font-size: 0.85rem;
    font-weight: 500; padding: 5px 12px; border-radius: 20px;
    border: 1px solid transparent; transition: all 0.2s; white-space: nowrap;
  }
  .top-nav a:hover { color: var(--gold); border-color: var(--border); }
  .top-nav a:first-child { color: var(--gold); border-color: var(--border); }

  /* Verification badge */
  .verification-badge {
    position: absolute;
    top: 16px;
    right: 16px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }
  .verification-badge.moop-verified {
    background: rgba(212,175,55,0.2);
    border: 1px solid var(--gold);
    color: var(--gold-light);
  }
  .verification-badge.web-verified {
    background: rgba(100,149,237,0.15);
    border: 1px solid #6495ED;
    color: #8BB8FF;
  }
  .verification-badge.unverified {
    background: rgba(80,80,80,0.3);
    border: 1px solid #555;
    color: #888;
  }
  .verify-icon { font-size: 0.9rem; }

  /* Hero */
  .hero {
    position: relative;
    padding: 48px 24px 36px;
    text-align: center;
    background: linear-gradient(180deg, rgba(212,175,55,0.08) 0%, transparent 100%);
    border-bottom: 1px solid var(--border);
  }
  .hero h1 {
    font-size: clamp(1.6rem, 4vw, 2.6rem);
    color: var(--white);
    margin-bottom: 8px;
    letter-spacing: 0.5px;
  }
  .hero h1 span { color: var(--gold); }
  .hero .denom-tag {
    display: inline-block;
    background: rgba(212,175,55,0.1);
    border: 1px solid rgba(212,175,55,0.25);
    color: var(--gold-light);
    font-size: 0.75rem; font-weight: 600;
    letter-spacing: 1.5px; text-transform: uppercase;
    padding: 3px 12px; border-radius: 20px; margin-bottom: 16px;
  }
  .hero .address {
    color: var(--gray-light);
    font-size: 0.95rem;
    margin-bottom: 18px;
  }

  /* Threat / Rating badge */
  .threat-badge {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 8px 20px; border-radius: 8px;
    font-weight: 700; font-size: 0.95rem;
    letter-spacing: 0.5px; margin-top: 8px;
    border: 1.5px solid;
  }
  .threat-badge.rating-green { background: rgba(76,175,80,0.18); border-color: var(--green); color: #7edd80; }
  .threat-badge.rating-yellow { background: rgba(255,193,7,0.15); border-color: var(--yellow); color: #ffd85a; }
  .threat-badge.rating-red { background: rgba(244,67,54,0.15); border-color: var(--red); color: #ff7c74; }
  .threat-badge.rating-black { background: rgba(50,50,50,0.6); border-color: #555; color: #aaa; }
  .threat-icon { font-size: 1.3rem; }

  /* Main layout */
  .page-body {
    max-width: 960px;
    margin: 0 auto;
    padding: 36px 24px 60px;
  }

  /* Cards */
  .card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 28px;
  }
  .card-title {
    font-size: 1.0rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--gold);
    margin-bottom: 18px;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
  }

  /* Quick Facts */
  .facts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 14px;
  }
  .fact-item { display: flex; flex-direction: column; gap: 3px; }
  .fact-label { font-size: 0.8rem; color: var(--gray); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
  .fact-value { font-size: 0.92rem; color: var(--white); font-weight: 500; }
  .fact-value a { color: var(--gold); text-decoration: none; }
  .fact-value a:hover { text-decoration: underline; }
  .has-yes { color: #7edd80; font-weight: 600; }
  .has-no { color: var(--gray); }

  /* Scorecard */
  .score-row {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 12px;
    align-items: start;
    padding: 14px 0;
    border-bottom: 1px solid #1e1e1e;
  }
  .score-row:last-child { border-bottom: none; }
  .score-info { display: flex; flex-direction: column; gap: 4px; }
  .score-label { font-weight: 600; font-size: 0.95rem; color: var(--white); }
  .score-desc { font-size: 0.82rem; color: var(--gray-light); }
  .score-note { font-size: 0.82rem; color: #aaa; margin-top: 4px; font-style: italic; }
  .gender-detail { font-size: 0.8rem; color: #bbb; margin-top: 4px; padding: 6px 10px; background: rgba(212,175,55,0.06); border-left: 2px solid var(--gold); border-radius: 0 4px 4px 0; }
  .score-badge {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 4px 12px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700; white-space: nowrap;
    border: 1px solid;
  }
  .score-green { background: rgba(76,175,80,0.15); border-color: var(--green); color: #7edd80; }
  .score-yellow { background: rgba(255,193,7,0.12); border-color: var(--yellow); color: #ffd85a; }
  .score-red { background: rgba(244,67,54,0.12); border-color: var(--red); color: #ff7c74; }
  .score-black { background: rgba(50,50,50,0.6); border-color: #555; color: #aaa; }

  /* Notes */
  .note-block {
    padding: 14px 16px;
    border-radius: 8px;
    margin-bottom: 12px;
    border-left: 3px solid;
    font-size: 0.9rem;
    line-height: 1.7;
  }
  .note-assessment {
    background: rgba(212,175,55,0.06);
    border-color: var(--gold);
    color: var(--gray-light);
  }
  .note-tag-row {
    display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px;
  }
  .tag {
    background: #1a1a1a; border: 1px solid #333;
    color: var(--gray); font-size: 0.8rem;
    padding: 3px 10px; border-radius: 20px;
  }
  .social-links {
    display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px;
  }
  .social-link {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 8px 16px; border-radius: 8px; font-size: 0.85rem;
    font-weight: 600; text-decoration: none; border: 1px solid var(--border);
    transition: all 0.2s;
  }
  .social-link:hover { border-color: var(--gold); color: var(--gold-light); }
  .social-link.facebook { color: #8B9DC3; }
  .social-link.youtube { color: #FF6B6B; }
  .social-link.instagram { color: #C77DBA; }
  .social-link.twitter { color: #AAA; }

  /* Map */
  .map-wrap {
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid var(--border);
    margin-bottom: 28px;
  }
  .map-wrap iframe {
    width: 100%; height: 320px; border: none; display: block;
    filter: invert(0.9) hue-rotate(180deg);
  }

  /* Buttons */
  .btn-row { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 28px; }
  .btn-gold {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--gold); color: #000;
    font-weight: 700; font-size: 0.9rem;
    padding: 11px 22px; border-radius: 8px;
    text-decoration: none; border: none; cursor: pointer;
    transition: background 0.2s;
  }
  .btn-gold:hover { background: var(--gold-light); }
  .btn-outline {
    display: inline-flex; align-items: center; gap: 8px;
    background: transparent; color: var(--gold);
    font-weight: 600; font-size: 0.9rem;
    padding: 11px 22px; border-radius: 8px;
    text-decoration: none; border: 1.5px solid var(--gold);
    cursor: pointer; transition: all 0.2s;
  }
  .btn-outline:hover { background: rgba(212,175,55,0.1); }

  /* Footer */
  .back-row {
    text-align: center;
    padding: 20px 0 10px;
    border-top: 1px solid var(--border);
    margin-top: 20px;
  }
  .back-row a { color: var(--gold); text-decoration: none; font-weight: 600; font-size: 0.9rem; }
  .back-row a:hover { text-decoration: underline; }

  footer {
    text-align: center;
    padding: 24px;
    color: var(--gray);
    font-size: 0.8rem;
    border-top: 1px solid var(--border);
  }
</style>
`;

const FONTS = `
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
`;

function buildPage(church) {
  const rubricMap = {};
  data.rubric.forEach(r => rubricMap[r.id] = r);

  // Build scorecard rows
  const scorecardRows = data.rubric.map(rubric => {
    const score = church.scores[rubric.id] || 'yellow';
    const note = church.score_notes && church.score_notes[rubric.id] ? church.score_notes[rubric.id] : '';
    const gd = (rubric.id === 'gender' && church.gender_detail) ? church.gender_detail : '';
    return `
      <div class="score-row">
        <div class="score-info">
          <div class="score-label">${escapeHtml(rubric.label)}</div>
          <div class="score-desc">${escapeHtml(rubric.description)}</div>
          ${note ? `<div class="score-note">${escapeHtml(note)}</div>` : ''}
          ${gd ? `<div class="gender-detail">${ico('shield-about-person-48.png', 14)} ${escapeHtml(gd)}</div>` : ''}
        </div>
        <div>
          <span class="score-badge ${colorClass(score)}">${colorLabel(score)}</span>
        </div>
      </div>`;
  }).join('');

  // Notes / assessment
  const assessment = church.assessment || '';
  const tags = (church.tags || []);

  // Map — handle addresses with dashes/unknowns
  const hasRealAddress = church.address && !church.address.toLowerCase().includes('unconfirmed') && !church.address.toLowerCase().includes('unknown');
  const mapEmbed = hasRealAddress ? `
    <div class="map-wrap">
      <iframe
        src="${mapSrc(church.address)}"
        allowfullscreen="" loading="lazy"
        referrerpolicy="no-referrer-when-downgrade"
        title="Map for ${escapeHtml(church.name)}">
      </iframe>
    </div>` : '';

  // Website button
  const websiteBtn = church.website ? `<a href="${escapeHtml(church.website)}" target="_blank" rel="noopener" class="btn-gold">${ico('shield-globe-48.png', 14)} Visit Their Website</a>` : '';

  // Church social media links
  const socialLinks = [];
  if (church.facebook) socialLinks.push(`<a href="${escapeHtml(church.facebook)}" target="_blank" rel="noopener" class="social-link facebook" title="Facebook">Facebook</a>`);
  if (church.youtube) socialLinks.push(`<a href="${escapeHtml(church.youtube)}" target="_blank" rel="noopener" class="social-link youtube" title="YouTube">YouTube</a>`);
  if (church.instagram) socialLinks.push(`<a href="${escapeHtml(church.instagram)}" target="_blank" rel="noopener" class="social-link instagram" title="Instagram">Instagram</a>`);
  if (church.twitter) socialLinks.push(`<a href="${escapeHtml(church.twitter)}" target="_blank" rel="noopener" class="social-link twitter" title="X/Twitter">X/Twitter</a>`);
  const socialHtml = socialLinks.length ? `<div class="social-links"><div style="font-size:0.8rem;text-transform:uppercase;letter-spacing:1px;color:var(--gray);margin-bottom:6px;font-weight:600;">Church Social Media</div>${socialLinks.join('')}</div>` : '';

  // Pastor social media links
  const pastorSocial = [];
  if (church.pastor_facebook) pastorSocial.push(`<a href="${escapeHtml(church.pastor_facebook)}" target="_blank" rel="noopener" class="social-link facebook" title="Pastor Facebook">Pastor FB</a>`);
  if (church.pastor_twitter) pastorSocial.push(`<a href="${escapeHtml(church.pastor_twitter)}" target="_blank" rel="noopener" class="social-link twitter" title="Pastor X/Twitter">Pastor X</a>`);
  if (church.pastor_instagram) pastorSocial.push(`<a href="${escapeHtml(church.pastor_instagram)}" target="_blank" rel="noopener" class="social-link instagram" title="Pastor Instagram">Pastor IG</a>`);
  if (church.pastor_linkedin) pastorSocial.push(`<a href="${escapeHtml(church.pastor_linkedin)}" target="_blank" rel="noopener" class="social-link" style="color:#0A66C2;" title="Pastor LinkedIn">Pastor LinkedIn</a>`);
  const pastorSocialHtml = pastorSocial.length ? `<div class="social-links" style="margin-top:8px;"><div style="font-size:0.8rem;text-transform:uppercase;letter-spacing:1px;color:var(--gray);margin-bottom:6px;font-weight:600;">Pastor Social Media</div>${pastorSocial.join('')}</div>` : '';

  // Defunct marker
  const isDefunct = church.services && church.services.toLowerCase().includes('no longer');
  const isNotFound = church.overall_label && (church.overall_label.toLowerCase().includes('not found') || church.overall_label.toLowerCase().includes('defunct') || church.overall_label.toLowerCase().includes('search result'));

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/icons/favicon-16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
  <link rel="manifest" href="/manifest.json">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="${escapeHtml(church.name)} — Theological due diligence scorecard for Christian men in Fredericksburg, VA.">
  <meta property="og:title" content="${escapeHtml(church.name)} — Church Directory | USMC Ministries">
  <meta property="og:description" content="10-point theological scorecard: ${escapeHtml(church.overall_label || '')}">
  <meta property="og:type" content="website">
  <title>${escapeHtml(church.name)} — Church Directory | USMC Ministries</title>
  ${FONTS}
  ${CSS}
</head>
<body>
${NAV}

<div class="hero">
  ${verificationBadge(church)}
  <div class="denom-tag">${escapeHtml(church.type || church.denomination || 'Church')}</div>
  <h1>${escapeHtml(church.name)}</h1>
  <div class="address">${ico('shield-map-48.png', 14)} ${escapeHtml(church.address)}</div>
  ${threatBadge(church)}
</div>

<div class="page-body">

  <!-- Quick Facts -->
  <div class="card">
    <div class="card-title">${ico('shield-checklist-48.png', 20)} Quick Facts</div>
    <div class="facts-grid">
      <div class="fact-item">
        <span class="fact-label">Pastor</span>
        <span class="fact-value">${escapeHtml(church.pastor || 'Unknown')}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Founded</span>
        <span class="fact-value">${escapeHtml(church.founded || 'Unknown')}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Denomination</span>
        <span class="fact-value">${escapeHtml(church.denomination || 'Unknown')}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Service Times</span>
        <span class="fact-value">${escapeHtml(church.services || 'See website')}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Men's Ministry</span>
        <span class="fact-value ${church.has_mens_ministry ? 'has-yes' : 'has-no'}">${church.has_mens_ministry ? 'Yes' : 'No'}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Kids Ministry</span>
        <span class="fact-value ${church.has_kids_ministry ? 'has-yes' : 'has-no'}">${church.has_kids_ministry ? 'Yes' : 'No'}</span>
      </div>
      ${church.website ? `<div class="fact-item">
        <span class="fact-label">Website</span>
        <span class="fact-value"><a href="${escapeHtml(church.website)}" target="_blank" rel="noopener">${escapeHtml(church.website.replace(/^https?:\/\//, ''))}</a></span>
      </div>` : ''}
      ${church.pastor_credentials && church.pastor_credentials !== 'Unknown' ? `<div class="fact-item" style="grid-column: 1 / -1;">
        <span class="fact-label">Pastor Credentials</span>
        <span class="fact-value" style="color: var(--gray-light); font-size: 0.88rem;">${escapeHtml(church.pastor_credentials)}</span>
      </div>` : ''}
    </div>
  </div>

  <!-- 10-Point Scorecard -->
  <div class="card">
    <div class="card-title">${ico('shield-checklist-48.png', 20)} 10-Point Theological Scorecard</div>
    ${scorecardRows}
  </div>

  <!-- Assessment / Notes -->
  ${assessment ? `<div class="card">
    <div class="card-title">${ico('shield-blog-quill-48.png', 20)} Assessment</div>
    <div class="note-block note-assessment">${escapeHtml(assessment)}</div>
    ${tags.length > 0 ? `<div class="note-tag-row">${tags.map(t => `<span class="tag">#${escapeHtml(t)}</span>`).join('')}</div>` : ''}
  </div>` : ''}

  <!-- Map -->
  ${mapEmbed}

  <!-- Buttons -->
  <div class="btn-row">
    ${websiteBtn}
    <a href="/churches.html" class="btn-outline">← Back to Church Directory</a>
  </div>
  ${socialHtml}
  ${pastorSocialHtml}

  ${engagementSection(church)}

  <!-- Page metadata -->
  <div style="margin-top:28px;padding:16px;border-top:1px solid var(--border);display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px;">
    <div style="color:var(--gray);font-size:0.78rem;">
      ${ico('shield-checklist-48.png', 12)} Last reviewed: <strong style="color:var(--gray-light);">${data.meta.updated}</strong>
      <span style="margin-left:8px;opacity:0.6;">— Annual review recommended</span>
    </div>
    <div id="page-views" style="color:var(--gray);font-size:0.78rem;"></div>
  </div>

  <div class="back-row">
    <a href="/churches.html">← Return to Full Church Directory</a>
  </div>
</div>

<footer>
  <p>Fredericksburg Church Directory &mdash; Theological Due Diligence for Christian Men &mdash; <a href="https://usmcmin.org" style="color: var(--gold);">usmcmin.org</a></p>
  <p style="margin-top: 6px;">Last updated: ${data.meta.updated}</p>
</footer>
<script data-goatcounter="https://usmcmin.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
<script>
// Show page view count from GoatCounter public counter API
// Requires "Allow public counter" enabled in GoatCounter Settings
var pvEl = document.getElementById('page-views');
if (pvEl) {
  var countImg = document.createElement('img');
  countImg.src = 'https://usmcmin.goatcounter.com/counter/' + encodeURIComponent(location.pathname) + '.svg';
  countImg.alt = 'page views';
  countImg.style.cssText = 'height:14px;vertical-align:middle;opacity:0.7;';
  countImg.onerror = function() { pvEl.textContent = ''; };
  pvEl.appendChild(countImg);
}
</script>
</body>
</html>`;
}

// Generate all church pages
let count = 0;
data.churches.forEach(church => {
  const html = buildPage(church);
  const outPath = path.join(outDir, `${church.id}.html`);
  fs.writeFileSync(outPath, html);
  count++;
  console.log(`✅ ${church.id}.html`);
});

// Generate index redirect
const indexHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=/churches.html">
  <title>Redirecting to Church Directory...</title>
</head>
<body>
  <p>Redirecting to <a href="/churches.html">Church Directory</a>...</p>
  <script>window.location.href = '/churches.html';</script>
</body>
</html>`;
fs.writeFileSync(path.join(outDir, 'index.html'), indexHtml);
console.log(`✅ index.html (redirect)`);

console.log(`\n🎉 Generated ${count} church pages + index.html`);
