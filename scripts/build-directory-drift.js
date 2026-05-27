#!/usr/bin/env node
// Generates docs/directory-drift.html — the editorial drift watchlist page.
// Surfaces records whose signals are in tension (a pastor who signed
// statements in opposite directions), records whose rubric rating may be
// stale (legacy numeric ratings predating the categorical rubric), and
// records that warrant ongoing editorial monitoring.
//
// Pulls live data from docs/data/churches.json + statement-lists-manifest.json
// so the page's claims always match the underlying directory state.
// Re-run after enrichment passes that touch ratings or signatories.

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const MANIFEST = path.join(__dirname, '..', 'docs', 'data', 'statement-lists-manifest.json');
const OUTPUT   = path.join(__dirname, '..', 'docs', 'directory-drift.html');

const TODAY = new Date().toISOString().slice(0, 10);

const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
const manifest = JSON.parse(fs.readFileSync(MANIFEST, 'utf8'));

// ---- Ledger direction map (from manifest) ----
const GREEN_LEDGERS = new Set();
const RED_LEDGERS = new Set();
for (const l of manifest.lists) {
  if (l.direction === 'green') GREEN_LEDGERS.add(l.key);
  else if (l.direction === 'red') RED_LEDGERS.add(l.key);
}

// Pretty label for each ledger key
const LEDGER_LABEL = {};
for (const l of manifest.lists) LEDGER_LABEL[l.key] = l.label;

// ---- Helpers ----
function sigKeys(c) {
  if (!c.signatories || typeof c.signatories !== 'object') return [];
  return Object.entries(c.signatories)
    .filter(([k, v]) => Array.isArray(v) && v.length > 0)
    .map(([k]) => k);
}

function totalSigs(c) {
  if (!c.signatories || typeof c.signatories !== 'object') return 0;
  return Object.values(c.signatories).reduce((s, v) => s + (Array.isArray(v) ? v.length : 0), 0);
}

function locationOf(c) {
  const a = c.address || '';
  // Try to extract "City, ST" or "City, StateName"
  const m1 = a.match(/([A-Za-z\.\s\-]+),\s*([A-Z]{2})(?:\s+\d{5})?/);
  if (m1) return `${m1[1].trim()}, ${m1[2]}`;
  const last = a.split(',').slice(-2).join(',').trim();
  return last || 'Location pending';
}

function slugLink(c) {
  return `/churches/${encodeURIComponent(c.slug || c.id)}.html`;
}

function escapeHtml(s) {
  return String(s || '').replace(/[&<>"']/g, ch => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[ch]));
}

// ---- Compute drift buckets ----
const buckets = {
  mixedSignals: [],            // signed BOTH green-direction and red-direction ledgers
  greenSignerInDriftedChurch: [], // signed green ledger but church now rated red/black
  redSignerInGreenChurch: [],  // signed red-direction ledger but church still rated green
  legacyNumericRating: [],     // numeric overall_rating (un-normalized)
  highSigsLowRating: [],       // 2+ signatures total but rated red or black
  unverifiedPastor: 0          // tracked for stat only
};

const PLACEHOLDER = /^(verify|various|unknown|see\s+website|currently|none|listed|tbd|n\/a|the\s+pastor|the\s+church|various\s+pastors|pastoral)/i;

for (const c of d.churches) {
  const keys = sigKeys(c);
  const hasGreenSig = keys.some(k => GREEN_LEDGERS.has(k));
  const hasRedSig = keys.some(k => RED_LEDGERS.has(k));
  const sigsTotal = totalSigs(c);

  if (hasGreenSig && hasRedSig) buckets.mixedSignals.push(c);
  if (hasGreenSig && (c.overall_rating === 'red' || c.overall_rating === 'black')) {
    buckets.greenSignerInDriftedChurch.push(c);
  }
  if (hasRedSig && !hasGreenSig && c.overall_rating === 'green') {
    buckets.redSignerInGreenChurch.push(c);
  }
  if (typeof c.overall_rating === 'number' ||
      (typeof c.overall_rating === 'string' && /^[0-9.]+$/.test(c.overall_rating))) {
    buckets.legacyNumericRating.push(c);
  }
  if (sigsTotal >= 2 && (c.overall_rating === 'red' || c.overall_rating === 'black')) {
    buckets.highSigsLowRating.push(c);
  }
  if (!c.pastor || PLACEHOLDER.test(c.pastor)) buckets.unverifiedPastor++;
}

const total = d.churches.length;
const fmt = n => n.toLocaleString();

// ---- Sort each bucket for stable, useful presentation ----
buckets.mixedSignals.sort((a, b) => (a.name || '').localeCompare(b.name || ''));
buckets.greenSignerInDriftedChurch.sort((a, b) => {
  // Black first, then red
  const rOrder = { black: 0, red: 1 };
  return (rOrder[a.overall_rating] ?? 9) - (rOrder[b.overall_rating] ?? 9)
    || (a.name || '').localeCompare(b.name || '');
});
buckets.redSignerInGreenChurch.sort((a, b) => (a.name || '').localeCompare(b.name || ''));
buckets.legacyNumericRating.sort((a, b) => {
  // Group by denom, then name
  return (a.denomination_family || '').localeCompare(b.denomination_family || '')
    || (a.name || '').localeCompare(b.name || '');
});
buckets.highSigsLowRating.sort((a, b) => totalSigs(b) - totalSigs(a));

// ---- Render helpers ----
function ledgerBadges(c, filter = null) {
  const keys = sigKeys(c);
  const filtered = filter ? keys.filter(filter) : keys;
  return filtered.map(k => {
    const count = c.signatories[k].length;
    const dir = GREEN_LEDGERS.has(k) ? 'green' : RED_LEDGERS.has(k) ? 'red' : 'neutral';
    return `<span class="ledger-badge ${dir}">${escapeHtml(LEDGER_LABEL[k] || k)}${count > 1 ? ` &times;${count}` : ''}</span>`;
  }).join(' ');
}

function recordCard(c, opts = {}) {
  const rating = c.overall_rating || '—';
  const ratingClass = typeof rating === 'string' ? rating : 'numeric';
  const denom = c.denomination_family || c.denomination || '';
  const loc = locationOf(c);
  const ledgerHtml = opts.showLedgers === false ? '' : ledgerBadges(c, opts.ledgerFilter);
  return `<div class="record">
    <div class="record-head">
      <span class="rating-pill ${ratingClass}">${escapeHtml(String(rating))}</span>
      <a class="record-name" href="${slugLink(c)}">${escapeHtml(c.name || c.id)}</a>
    </div>
    <div class="record-meta">${escapeHtml(loc)}${denom ? ` &middot; ${escapeHtml(denom)}` : ''}</div>
    ${ledgerHtml ? `<div class="record-ledgers">${ledgerHtml}</div>` : ''}
  </div>`;
}

function bucketSection(id, title, count, summary, items, opts = {}) {
  const limit = opts.limit ?? Infinity;
  const shown = items.slice(0, limit);
  const overflow = items.length - shown.length;
  return `<section class="section" id="${id}">
    <h2><span class="bucket-count">${fmt(count)}</span> ${escapeHtml(title)}</h2>
    <p class="bucket-summary">${summary}</p>
    <div class="record-list">
      ${shown.map(c => recordCard(c, opts)).join('\n')}
    </div>
    ${overflow > 0 ? `<p class="bucket-overflow">+ ${fmt(overflow)} more records in this bucket — full list available on request via <a href="/connect.html">the connect form</a>.</p>` : ''}
  </section>`;
}

// ---- Top denominations in the numeric-rating bucket (for the summary table) ----
const numericByDenom = {};
for (const c of buckets.legacyNumericRating) {
  const k = c.denomination_family || 'Unknown';
  numericByDenom[k] = (numericByDenom[k] || 0) + 1;
}
const numericDenomTop = Object.entries(numericByDenom).sort((a, b) => b[1] - a[1]).slice(0, 8);

// ---- HTML ----
const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/icons/favicon-16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
  <link rel="manifest" href="/manifest.json">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Drift watchlist for the MOOP Church Directory — records where doctrinal signals are in tension, ratings may be stale, or ongoing editorial monitoring is warranted.">
  <meta property="og:title" content="Drift Watchlist | MOOP Church Directory | USMC Ministries">
  <meta property="og:description" content="Where the editorial signals are in tension. The records we are actively monitoring across the directory.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://usmcmin.org/directory-drift.html">
  <meta property="og:image" content="https://usmcmin.org/assets/icons/icon-512.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Drift Watchlist | MOOP Church Directory">
  <meta name="twitter:image" content="https://usmcmin.org/assets/icons/icon-512.png">
  <title>Drift Watchlist | MOOP Church Directory | USMC Ministries</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    :root { --bg:#000; --card:#111; --card2:#1a1a1a; --gold:#D4AF37; --gold-light:#F4D470; --white:#e8e8e8; --gray:#888; --border:#333; --green:#3ea14a; --yellow:#d4a437; --red:#c0392b; --black:#444; }
    body { font-family:'Inter',sans-serif; background:var(--bg); color:var(--white); min-height:100vh; line-height:1.65; }
    h1,h2,h3 { font-family:'Playfair Display',serif; }
    nav { display:flex; flex-wrap:wrap; gap:6px; justify-content:center; padding:14px 20px; border-bottom:1px solid var(--border); background:rgba(0,0,0,0.95); backdrop-filter:blur(8px); position:sticky; top:0; z-index:100; }
    nav a { color:var(--gray); text-decoration:none; font-size:0.85rem; font-weight:500; padding:5px 12px; border-radius:20px; border:1px solid transparent; transition:all 0.2s; white-space:nowrap; }
    nav a:hover { color:var(--gold); border-color:var(--border); }
    nav a.active { color:var(--gold) !important; border-color:var(--gold); }

    .container { max-width:1000px; margin:0 auto; padding:40px 22px 60px; }
    .hero { text-align:center; padding:30px 0 36px; border-bottom:1px solid var(--border); margin-bottom:36px; }
    .hero .breadcrumb { color:var(--gray); font-size:0.85rem; margin-bottom:12px; letter-spacing:1px; }
    .hero .breadcrumb a { color:var(--gold); text-decoration:none; }
    .hero h1 { font-size:clamp(2rem, 5vw, 2.8rem); color:var(--gold-light); margin:8px 0 14px; letter-spacing:0.5px; }
    .hero .subtitle { color:var(--gray); max-width:780px; margin:0 auto 22px; font-size:1.02rem; font-style:italic; }

    .stat-row { display:grid; grid-template-columns:repeat(auto-fit, minmax(160px, 1fr)); gap:14px; margin-top:22px; }
    .stat-card { background:var(--card); border:1px solid var(--border); border-radius:12px; padding:18px 14px; text-align:center; }
    .stat-card .stat-num { color:var(--gold); font-size:1.65rem; font-weight:700; font-family:'Playfair Display',serif; }
    .stat-card .stat-lbl { color:var(--gray); font-size:0.72rem; text-transform:uppercase; letter-spacing:1.2px; margin-top:6px; }

    .toc { background:var(--card); border:1px solid var(--border); border-radius:12px; padding:18px 22px; margin:24px 0 32px; }
    .toc h3 { color:var(--gold-light); font-size:1rem; margin-bottom:10px; }
    .toc ol { margin:0 0 0 22px; color:var(--white); }
    .toc li { padding:4px 0; font-size:0.92rem; }
    .toc a { color:var(--gold); text-decoration:none; border-bottom:1px dotted #555; }
    .toc a:hover { color:var(--gold-light); border-bottom-color:var(--gold-light); }

    section.section { margin:48px 0; }
    .section h2 { color:var(--gold-light); font-size:1.5rem; margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid var(--border); }
    .section h2 .bucket-count { display:inline-block; min-width:54px; padding:3px 12px; margin-right:12px; background:var(--card); color:var(--gold); border:1px solid var(--gold); border-radius:6px; font-size:1rem; font-family:'Playfair Display',serif; font-weight:700; vertical-align:middle; }
    .bucket-summary { color:var(--white); font-size:0.96rem; line-height:1.78; margin-bottom:22px; }
    .bucket-summary strong { color:var(--gold-light); }
    .bucket-summary code { background:#0a0a0a; color:var(--gold-light); padding:2px 7px; border-radius:4px; font-family:'SF Mono', Menlo, Consolas, monospace; font-size:0.86em; }
    .section a { color:var(--gold); text-decoration:none; border-bottom:1px dotted #555; }
    .section a:hover { color:var(--gold-light); border-bottom-color:var(--gold-light); }

    .record-list { display:grid; gap:10px; margin-top:18px; }
    .record { background:var(--card); border:1px solid var(--border); border-left:3px solid var(--gray); border-radius:8px; padding:14px 18px; transition:border-left-color 0.15s; }
    .record:hover { border-left-color:var(--gold); }
    .record-head { display:flex; align-items:center; gap:12px; margin-bottom:6px; flex-wrap:wrap; }
    .record-name { color:var(--white); font-weight:600; font-size:1rem; text-decoration:none; border-bottom:1px dotted transparent; }
    .record-name:hover { color:var(--gold-light); border-bottom-color:var(--gold-light); }
    .record-meta { color:var(--gray); font-size:0.85rem; margin-bottom:6px; }
    .record-ledgers { display:flex; flex-wrap:wrap; gap:6px; margin-top:6px; }

    .rating-pill { display:inline-block; padding:2px 10px; border-radius:12px; font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; border:1px solid; }
    .rating-pill.green { color:var(--green); border-color:rgba(62,161,74,0.5); background:rgba(62,161,74,0.08); }
    .rating-pill.yellow { color:var(--yellow); border-color:rgba(212,164,55,0.5); background:rgba(212,164,55,0.08); }
    .rating-pill.red { color:var(--red); border-color:rgba(192,57,43,0.5); background:rgba(192,57,43,0.08); }
    .rating-pill.black { color:#aaa; border-color:#555; background:#222; }
    .rating-pill.dead { color:#666; border-color:#444; background:transparent; }
    .rating-pill.numeric { color:var(--gold); border-color:rgba(212,175,55,0.5); background:rgba(212,175,55,0.08); }

    .ledger-badge { display:inline-block; padding:2px 9px; border-radius:4px; font-size:0.72rem; font-weight:600; border:1px solid; }
    .ledger-badge.green { color:var(--green); border-color:rgba(62,161,74,0.45); background:rgba(62,161,74,0.06); }
    .ledger-badge.red { color:var(--red); border-color:rgba(192,57,43,0.45); background:rgba(192,57,43,0.06); }
    .ledger-badge.neutral { color:var(--gray); border-color:var(--border); background:transparent; }

    .bucket-overflow { color:var(--gray); font-size:0.88rem; font-style:italic; margin-top:14px; text-align:center; }

    .callout { background:var(--card); border-left:4px solid var(--gold); border-radius:8px; padding:16px 20px; margin:22px 0; }
    .callout p { margin-bottom:0; color:var(--white); font-size:0.95rem; }
    .callout strong { color:var(--gold-light); }

    .denom-table { background:var(--card); border:1px solid var(--border); border-radius:8px; padding:14px 20px; margin:18px 0; }
    .denom-table .row { display:flex; justify-content:space-between; padding:5px 0; font-size:0.92rem; border-bottom:1px dashed var(--border); }
    .denom-table .row:last-child { border-bottom:none; }
    .denom-table .row .label { color:var(--white); }
    .denom-table .row .val { color:var(--gold); font-variant-numeric:tabular-nums; font-weight:600; }

    .updated-stamp { color:var(--gray); font-size:0.82rem; text-align:center; margin-top:50px; padding-top:24px; border-top:1px dashed var(--border); line-height:1.8; }
    .updated-stamp a { color:var(--gold); text-decoration:none; }
    .updated-stamp a:hover { color:var(--gold-light); }
    .updated-stamp .sep { color:#555; margin:0 8px; }

    footer { padding:30px 20px; text-align:center; color:var(--gray); font-size:0.78rem; border-top:1px solid var(--border); margin-top:60px; }
    footer a { color:var(--gold); text-decoration:none; }

    @media (max-width:600px) {
      .container { padding:28px 16px 50px; }
      .stat-row { grid-template-columns:repeat(2, 1fr); }
      .section h2 { font-size:1.2rem; }
      .section h2 .bucket-count { font-size:0.85rem; padding:2px 8px; min-width:44px; }
    }
  </style>
</head>
<body>
  <nav>
    <a href="/">Home</a>
    <a href="/churches.html">Directory</a>
    <a href="/directory-overview.html">Overview</a>
    <a href="/directory-politicians.html">Politicians</a>
    <a href="/directory-networks.html">Networks</a>
    <a href="/directory-map.html">Map</a>
    <a href="/directory-methodology.html">Methodology</a>
    <a href="/directory-drift.html" class="active">Drift</a>
    <a href="/directory-roadmap.html">Roadmap</a>
    <a href="/about.html">About</a>
  </nav>

  <div class="container">
    <div class="hero">
      <div class="breadcrumb"><a href="/">USMC Ministries</a> &middot; <a href="/churches.html">Church Directory</a> &middot; Drift Watchlist</div>
      <h1>Drift Watchlist</h1>
      <p class="subtitle">Records where the editorial signals are in tension — pastors whose public theological positions point in opposite directions, churches where a 2017 conviction may no longer describe a 2026 reality, ratings that predate the current rubric. This is the ledger of what we are actively monitoring.</p>
      <div class="stat-row">
        <div class="stat-card"><div class="stat-num">${fmt(buckets.mixedSignals.length)}</div><div class="stat-lbl">mixed-signal records</div></div>
        <div class="stat-card"><div class="stat-num">${fmt(buckets.greenSignerInDriftedChurch.length)}</div><div class="stat-lbl">drifted-church signers</div></div>
        <div class="stat-card"><div class="stat-num">${fmt(buckets.redSignerInGreenChurch.length)}</div><div class="stat-lbl">stale-rating candidates</div></div>
        <div class="stat-card"><div class="stat-num">${fmt(buckets.legacyNumericRating.length)}</div><div class="stat-lbl">legacy numeric ratings</div></div>
      </div>
    </div>

    <div class="toc">
      <h3>What's on this page</h3>
      <ol>
        <li><a href="#mixed-signals">Mixed-signal records</a> — pastors who signed both green-direction and red-direction statements (${fmt(buckets.mixedSignals.length)})</li>
        <li><a href="#green-signer-drifted">Conservative-statement signers at drifted churches</a> — 2017 signers, 2026 red/black ratings (${fmt(buckets.greenSignerInDriftedChurch.length)})</li>
        <li><a href="#red-signer-green">Progressive-statement signers at still-green churches</a> — stale-rating candidates (${fmt(buckets.redSignerInGreenChurch.length)})</li>
        <li><a href="#high-sigs-low-rating">Heavy signers at low-rated churches</a> — disproportionate-signature drift (${fmt(buckets.highSigsLowRating.length)})</li>
        <li><a href="#legacy-numeric">Legacy numeric ratings</a> — pre-rubric records awaiting normalization (${fmt(buckets.legacyNumericRating.length)})</li>
        <li><a href="#methodology">Methodology &amp; corrections</a></li>
      </ol>
    </div>

    <section class="section">
      <h2>What "drift" means here</h2>
      <p class="bucket-summary">Drift is not a single phenomenon. In this directory, it has at least five distinct shapes — each surfaced as its own bucket below.</p>
      <p class="bucket-summary">A pastor who signed the <strong>Nashville Statement</strong> in 2017 and then signed the <strong>Warhurst Protest</strong> in 2020 has not necessarily moved positions — but his signatures point in opposite directions, and the tension deserves a closer look. A church whose pastor signed Nashville but which now rates red is a 2017-2026 trajectory that may reflect a leadership transition, a denominational drift, or a quiet realignment. A church rated green where a staff member signed a soft-progressive PCA letter may be a rating that hasn't caught up to the new evidence — or it may be a legitimate single-staff outlier. Each bucket has a different explanation, and each warrants a different follow-up.</p>
      <div class="callout">
        <p><strong>This page is the editorial honesty layer.</strong> A directory that doesn't surface its own internal tensions is not a directory anyone should trust. These records are exactly the ones where our rating, our cross-references, or our research are doing the hardest work — and they are exactly the ones a careful reader should examine for themselves.</p>
      </div>
    </section>

    ${bucketSection(
      'mixed-signals',
      'Mixed-signal records',
      buckets.mixedSignals.length,
      `Each of these churches has staff or pastoral leadership who signed at least one <span class="ledger-badge green">green-direction</span> statement (Nashville 2017 or Dallas 2018) <em>and</em> at least one <span class="ledger-badge red">red-direction</span> statement (Warhurst, AMR, Letter of Lament, Revoice, or CBE). The most common pairing is <strong>Nashville 2017 &times; Warhurst Protest 2020</strong> — pastors who held the 2017 line on biblical sexuality but later signed the 2020 protest against PCA discipline of a Revoice-friendly minister. That combination is not a clean contradiction (a man can hold both positions in principle), but it is a meaningful tension worth flagging.`,
      buckets.mixedSignals,
      { limit: 30 }
    )}

    ${bucketSection(
      'green-signer-drifted',
      'Conservative-statement signers at drifted churches',
      buckets.greenSignerInDriftedChurch.length,
      `Pastors or staff who signed the Nashville Statement, the Dallas Statement, or both — but whose church currently rates <strong>red</strong> or <strong>black</strong> in our rubric. The drift drivers vary: leadership transitions (the signer retired, moved, or died and a successor pastors differently), denominational drift (church called a female pastor or adopted egalitarian leadership), mission drift (prosperity-adjacent teaching, ministry collapse, full progressive realignment). For the editorial narrative around this bucket, see the <a href="/blog/where-the-nashville-statement-signers-lead-today.html">"Where the Nashville Statement Signers Lead Today"</a> blog post.`,
      buckets.greenSignerInDriftedChurch,
      { limit: 30, ledgerFilter: k => GREEN_LEDGERS.has(k) }
    )}

    ${bucketSection(
      'red-signer-green',
      'Progressive-statement signers at still-green churches',
      buckets.redSignerInGreenChurch.length,
      `Pastors or staff who signed a red-direction statement (most commonly the Warhurst Protest) but whose church currently rates <strong>green</strong> in our rubric. These records are <em>stale-rating candidates</em>. Possible explanations: a single staff signature on a multi-staff church (the senior pastor may hold a different line), the church has since corrected and the signature is historical context only, or our rubric rating is out of date. Each of these warrants a fresh look at the church's current statement of faith, current preaching, and current elder team.`,
      buckets.redSignerInGreenChurch
    )}

    ${bucketSection(
      'high-sigs-low-rating',
      'Heavy signers at low-rated churches',
      buckets.highSigsLowRating.length,
      `Churches with <strong>two or more total signer entries</strong> across the ledgers but rated red or black. The "two or more" threshold is what makes this bucket distinct from the simpler green-signer-drift bucket above: a church with multiple signature entries was, at one point, a significant institutional carrier of public theological statements. If it has drifted, the drift is correspondingly more significant. These records get manual review priority.`,
      buckets.highSigsLowRating
    )}

    <section class="section" id="legacy-numeric">
      <h2><span class="bucket-count">${fmt(buckets.legacyNumericRating.length)}</span> Legacy numeric ratings</h2>
      <p class="bucket-summary">${fmt(buckets.legacyNumericRating.length)} records still carry a <strong>numeric overall_rating</strong> (e.g. <code>6</code>, <code>7</code>, <code>8.5</code>) — a holdover from an earlier 1-10 scoring scheme that predates the current categorical rubric (green / yellow / red / black / dead). These records are not unrated; they are <em>differently</em> rated, on a scheme that the current public methodology no longer documents. They will be re-evaluated against the categorical rubric in a future enrichment pass.</p>
      <p class="bucket-summary">The legacy ratings concentrate in specific denominational families that received bulk-import enrichment under the older scoring model:</p>
      <div class="denom-table">
        ${numericDenomTop.map(([k, v]) => `<div class="row"><span class="label">${escapeHtml(k)}</span><span class="val">${fmt(v)}</span></div>`).join('\n        ')}
      </div>
      <p class="bucket-summary">In the meantime, any user-facing rating display for these records uses the literal numeric value rather than mapping it onto the categorical scale — the rubric translation is intentionally deferred until a human review pass can confirm each record individually. For one-off corrections, use the feedback form on the relevant church profile page.</p>
    </section>

    <section class="section" id="methodology">
      <h2>Methodology &amp; corrections</h2>
      <p class="bucket-summary">Drift detection runs against the live <code>docs/data/churches.json</code> file every time <code>scripts/build-directory-drift.js</code> is invoked. The script reads ledger directions from <code>docs/data/statement-lists-manifest.json</code> — green-direction ledgers (Nashville Statement 2017, Dallas Statement 2018) and red-direction ledgers (Warhurst Protest 2020, AMR Leadership 2026, PCA Letter of Lament 2025, Revoice 2018–2026, CBE Egalitarian Network 2026) are tagged in the manifest itself rather than hardcoded.</p>
      <p class="bucket-summary">A record can appear in multiple buckets — a heavy signer at a drifted church may show up in both the green-signer-drift bucket and the high-sigs-low-rating bucket, and that's intentional. Buckets are perspectives, not categories.</p>
      <p class="bucket-summary">If you believe a record on this page has been misclassified, or you can correct a stale rating with primary-source evidence (statement of faith URL, sermon timestamp, denominational announcement), please submit the correction via the <strong>feedback form on the individual church's profile page</strong>. The directory's editorial discipline is to accept evidence-bearing corrections within one enrichment cycle.</p>
      <div class="callout">
        <p><strong>A drift listing is not an accusation.</strong> It is a signal that the record's editorial confidence is lower than the directory's median — that the available evidence does not all point in the same direction. Some of these records will resolve toward green on closer examination; some will resolve toward red. The point of the watchlist is to make the unresolved cases visible rather than to bury them inside a confident-looking aggregate.</p>
      </div>
    </section>

    <div class="updated-stamp">
      Generated <strong>${TODAY}</strong> from live directory state.<span class="sep">·</span>
      <a href="/directory-methodology.html">Methodology</a><span class="sep">·</span>
      <a href="/directory-networks.html">Network cross-reference</a><span class="sep">·</span>
      <a href="/directory-overview.html">Overview</a><span class="sep">·</span>
      <a href="/churches.html">Browse all ${fmt(total)} churches</a>
    </div>
  </div>

  <footer>
    <a href="/usmc-ministries.html">U.S.M.C. Ministries</a> &middot;
    <a href="/churches.html">Church Directory</a> &middot;
    <a href="/blog.html">Blog</a><br>
    <span style="margin-top:6px;display:block;">&copy; 2026 U.S.M.C. Ministries &middot; Fredericksburg, VA</span>
  </footer>
</body>
</html>
`;

fs.writeFileSync(OUTPUT, html);
console.log(`Wrote ${OUTPUT}`);
console.log(`Drift buckets:`);
console.log(`  Mixed signals: ${buckets.mixedSignals.length}`);
console.log(`  Green-signer-drifted: ${buckets.greenSignerInDriftedChurch.length}`);
console.log(`  Red-signer-green:    ${buckets.redSignerInGreenChurch.length}`);
console.log(`  High-sigs-low-rating: ${buckets.highSigsLowRating.length}`);
console.log(`  Legacy numeric:      ${buckets.legacyNumericRating.length}`);
