#!/usr/bin/env node
// Generates docs/directory-methodology.html — the public-facing executive
// summary / methodology page for the MOOP Church Directory.
//
// Pulls live stats from docs/data/churches.json + the statement-lists
// manifest so the numbers in the prose match reality. Re-run after any
// enrichment pass that changes the headline counts.

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const MANIFEST = path.join(__dirname, '..', 'docs', 'data', 'statement-lists-manifest.json');
const OUTPUT   = path.join(__dirname, '..', 'docs', 'directory-methodology.html');

const TODAY = new Date().toISOString().slice(0, 10);

const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
const manifest = JSON.parse(fs.readFileSync(MANIFEST, 'utf8'));

// ---- Compute live stats ----
const total = d.churches.length;
const fileSize = (fs.statSync(CHURCHES).size / (1024 * 1024)).toFixed(1);

const PLACEHOLDER = /^(verify|various|unknown|see\s+website|currently|none|listed|tbd|n\/a|the\s+pastor|the\s+church|various\s+pastors|pastoral)/i;
const isRealPastor = p => p && typeof p === 'string' && p.length >= 5 && !PLACEHOLDER.test(p);
const realPastors = d.churches.filter(c => isRealPastor(c.pastor)).length;

const facebook = d.churches.filter(c => c.facebook && /^https?:/i.test(c.facebook || '')).length;
const youtube  = d.churches.filter(c => c.youtube  && /^https?:/i.test(c.youtube  || '')).length;
const instagram = d.churches.filter(c => c.instagram && /^https?:/i.test(c.instagram || '')).length;

const ratingCounts = { green: 0, yellow: 0, red: 0, black: 0, dead: 0, other: 0 };
for (const c of d.churches) {
  const r = c.overall_rating;
  if (ratingCounts.hasOwnProperty(r)) ratingCounts[r]++;
  else ratingCounts.other++;
}

const sigCounts = { green: 0, red: 0, mixed: 0, none: 0 };
for (const c of d.churches) {
  const s = c.signatures_aggregate || 'none';
  if (sigCounts.hasOwnProperty(s)) sigCounts[s]++;
}
const sigTotal = sigCounts.green + sigCounts.red + sigCounts.mixed;

const networkCounts = {};
let crossListedAny = 0, crossListedMulti = 0;
for (const c of d.churches) {
  const nets = Array.isArray(c.cross_listed_in) ? c.cross_listed_in : [];
  if (nets.length) { crossListedAny++; if (nets.length > 1) crossListedMulti++; }
  for (const n of nets) networkCounts[n] = (networkCounts[n] || 0) + 1;
}

const needsReview = d.churches.filter(c => c.needs_review).length;
const totalSignerEntries = manifest.lists.reduce((sum, l) => sum + (l.size || 0), 0);

// Notable attendees count (records that have a non-empty notable_attendees array)
let notableCount = 0;
const notableNames = new Set();
for (const c of d.churches) {
  if (Array.isArray(c.notable_attendees) && c.notable_attendees.length) {
    notableCount++;
    for (const na of c.notable_attendees) if (na && na.name) notableNames.add(na.name);
  }
}

// ---- Helpers ----
const fmt = n => n.toLocaleString();
const pct = (n, d2) => Math.round(n / d2 * 100);

// ---- Build the HTML ----
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
  <meta name="description" content="Methodology behind the MOOP Church Directory — how ${fmt(total)} US churches are doctrinally vetted, what editorial signals each record carries, and where the data is still incomplete.">
  <meta property="og:title" content="Methodology | MOOP Church Directory | USMC Ministries">
  <meta property="og:description" content="How this directory is built, what makes its claims defendable, and where it's still incomplete.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://usmcmin.org/directory-methodology.html">
  <meta property="og:image" content="https://usmcmin.org/assets/icons/icon-512.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Methodology | MOOP Church Directory">
  <meta name="twitter:image" content="https://usmcmin.org/assets/icons/icon-512.png">
  <title>Methodology | MOOP Church Directory | USMC Ministries</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    :root { --bg:#000; --card:#111; --card2:#1a1a1a; --gold:#D4AF37; --gold-light:#F4D470; --white:#e8e8e8; --gray:#888; --border:#333; --green:#3ea14a; --yellow:#d4a437; --red:#c0392b; --black:#444; }
    body { font-family:'Inter',sans-serif; background:var(--bg); color:var(--white); min-height:100vh; line-height:1.75; }
    h1,h2,h3 { font-family:'Playfair Display',serif; }
    nav { display:flex; flex-wrap:wrap; gap:6px; justify-content:center; padding:14px 20px; border-bottom:1px solid var(--border); background:rgba(0,0,0,0.95); backdrop-filter:blur(8px); position:sticky; top:0; z-index:100; }
    nav a { color:var(--gray); text-decoration:none; font-size:0.85rem; font-weight:500; padding:5px 12px; border-radius:20px; border:1px solid transparent; transition:all 0.2s; white-space:nowrap; }
    nav a:hover { color:var(--gold); border-color:var(--border); }
    nav a.active { color:var(--gold) !important; border-color:var(--gold); }

    .container { max-width:880px; margin:0 auto; padding:40px 22px 60px; }
    .hero { text-align:center; padding:30px 0 36px; border-bottom:1px solid var(--border); margin-bottom:36px; }
    .hero .breadcrumb { color:var(--gray); font-size:0.85rem; margin-bottom:12px; letter-spacing:1px; }
    .hero .breadcrumb a { color:var(--gold); text-decoration:none; }
    .hero h1 { font-size:clamp(2rem, 5vw, 2.8rem); color:var(--gold-light); margin:8px 0 14px; letter-spacing:0.5px; }
    .hero .subtitle { color:var(--gray); max-width:720px; margin:0 auto 22px; font-size:1.02rem; font-style:italic; }

    .stat-row { display:grid; grid-template-columns:repeat(auto-fit, minmax(160px, 1fr)); gap:14px; margin-top:22px; }
    .stat-card { background:var(--card); border:1px solid var(--border); border-radius:12px; padding:18px 14px; text-align:center; }
    .stat-card .stat-num { color:var(--gold); font-size:1.65rem; font-weight:700; font-family:'Playfair Display',serif; }
    .stat-card .stat-lbl { color:var(--gray); font-size:0.72rem; text-transform:uppercase; letter-spacing:1.2px; margin-top:6px; }

    section.section { margin:40px 0; }
    .section h2 { color:var(--gold-light); font-size:1.45rem; margin-bottom:18px; padding-bottom:8px; border-bottom:1px solid var(--border); }
    .section p { color:var(--white); font-size:0.96rem; line-height:1.78; margin-bottom:16px; }
    .section p code { background:#0a0a0a; color:var(--gold-light); padding:2px 7px; border-radius:4px; font-family:'SF Mono', Menlo, Consolas, monospace; font-size:0.86em; }
    .section a { color:var(--gold); text-decoration:none; border-bottom:1px dotted #555; }
    .section a:hover { color:var(--gold-light); border-bottom-color:var(--gold-light); }

    .section ul { margin:14px 0 18px 0; list-style:none; padding:0; }
    .section li { color:var(--white); padding:10px 14px; margin-bottom:8px; background:rgba(255,255,255,0.02); border-left:3px solid var(--border); border-radius:6px; font-size:0.93rem; line-height:1.65; }
    .section li strong { color:var(--gold-light); }
    .section li:hover { border-left-color:var(--gold); background:rgba(212,175,55,0.04); }

    .callout { background:var(--card); border-left:4px solid var(--gold); border-radius:8px; padding:16px 20px; margin:22px 0; }
    .callout p { margin-bottom:0; }
    .callout strong { color:var(--gold-light); }

    .rubric-list li { border-left-color:var(--gold); background:rgba(212,175,55,0.04); }
    .rubric-list li.green-pill { border-left-color:var(--green); }
    .rubric-list li.red-pill { border-left-color:var(--red); }
    .rubric-list li.black-pill { border-left-color:var(--black); }
    .rubric-list li strong { color:var(--gold-light); }

    .updated-stamp { color:var(--gray); font-size:0.82rem; text-align:center; margin-top:40px; padding-top:24px; border-top:1px dashed var(--border); line-height:1.8; }
    .updated-stamp a { color:var(--gold); text-decoration:none; }
    .updated-stamp a:hover { color:var(--gold-light); }
    .updated-stamp .sep { color:#555; margin:0 8px; }

    footer { padding:30px 20px; text-align:center; color:var(--gray); font-size:0.78rem; border-top:1px solid var(--border); margin-top:60px; }
    footer a { color:var(--gold); text-decoration:none; }

    @media (max-width:600px) {
      .container { padding:28px 16px 50px; }
      .stat-row { grid-template-columns:repeat(2, 1fr); }
      .section li { font-size:0.88rem; padding:10px 12px; }
    }
  </style>
</head>
<body>
  <nav>
    <a href="/">Home</a>
    <a href="/churches.html">Directory</a>
    <a href="/directory-overview.html">Overview</a>
    <a href="/directory-politicians.html">Politicians</a>
    <a href="/directory-map.html">Map</a>
    <a href="/directory-networks.html">Networks</a>
    <a href="/directory-methodology.html" class="active">Methodology</a>
    <a href="/directory-drift.html">Drift</a>
    <a href="/directory-roadmap.html">Roadmap</a>
    <a href="/about.html">About</a>
  </nav>

  <div class="container">
    <div class="hero">
      <div class="breadcrumb"><a href="/">USMC Ministries</a> · <a href="/churches.html">Church Directory</a> · Methodology</div>
      <h1>Methodology</h1>
      <p class="subtitle">How this directory is built, what makes its claims defendable, and where we know it's still incomplete.</p>
      <div class="stat-row">
        <div class="stat-card"><div class="stat-num">${fmt(total)}</div><div class="stat-lbl">churches</div></div>
        <div class="stat-card"><div class="stat-num">${fmt(ratingCounts.green)}</div><div class="stat-lbl">rated green</div></div>
        <div class="stat-card"><div class="stat-num">${fmt(crossListedAny)}</div><div class="stat-lbl">network cross-listings</div></div>
        <div class="stat-card"><div class="stat-num">${fmt(sigTotal)}</div><div class="stat-lbl">with pastor-signature matches</div></div>
      </div>
    </div>

    <section class="section">
      <h2>I. What this directory is</h2>
      <p>A doctrinally-vetted, US-wide registry of <strong>${fmt(total)} churches</strong>, hosted as a structured-data corner of <code>usmcmin.org</code>. It started around 7,400 records in early 2026 and has roughly doubled across six enrichment phases plus an ongoing dupe-cleanup pass.</p>
      <p>The data lives in one canonical file — <code>docs/data/churches.json</code>, ~${fileSize} MB — and every record fans out into a per-church HTML page at <code>usmcmin.org/churches/&lt;slug&gt;.html</code>, plus a row in the sitemap, plus (when applicable) tags on cross-listed network pages.</p>
      <div class="callout">
        <p>The point of difference vs. ChurchFinder.com, GotChurches, or Yellow Pages: every record carries an <strong>editorial signal</strong> — a doctrinal rating, signature cross-references, network membership — not just a name and address. Where other directories list, we evaluate.</p>
      </div>
    </section>

    <section class="section">
      <h2>II. The signal layer</h2>
      <p>For each record, the schema attempts to populate these distinguishing fields. Some are fully covered; others are partial:</p>
      <ul>
        <li><strong>Pastor name</strong> — real, non-placeholder pastor on <strong>${fmt(realPastors)} of ${fmt(total)} records (${pct(realPastors, total)}%)</strong>. The remaining records are mostly JavaScript-rendered Squarespace / Wix / Webflow staff pages that resist plain HTTP fetching; cracking those is queued behind a headless-browser extraction pass.</li>
        <li><strong>Social presence</strong> — ${fmt(facebook)} Facebook URLs, ${fmt(youtube)} YouTube channels, ${fmt(instagram)} Instagram accounts, plus scattered Twitter. A 2026-Q2 Facebook recovery campaign turned roughly 830 dead-website records into active social-channel records.</li>
        <li><strong>MOOP rubric rating</strong> — categorical (green / yellow / red / black / dead). Current distribution: <strong>${fmt(ratingCounts.green)} green</strong> · ${fmt(ratingCounts.yellow)} yellow · ${fmt(ratingCounts.red)} red · ${fmt(ratingCounts.black)} black · ${ratingCounts.dead} dead.</li>
        <li><strong>Cross-listed networks</strong> — registrations in seven Reformed-evangelical networks: Founders (${fmt(networkCounts.founders || 0)}), 9Marks (${fmt(networkCounts['9marks'] || 0)}), TGC (${fmt(networkCounts['tgc-cn'] || 0)}), Acts 29 (${fmt(networkCounts.acts29 || 0)}), Sovereign Grace Churches (${fmt(networkCounts.sgc || 0)}), Pillar Network (${fmt(networkCounts['pillar-network'] || 0)}), Trinity Foundation Registry (${fmt(networkCounts['trinity-foundation'] || 0)}). <strong>${fmt(crossListedAny)} churches</strong> are cross-listed in at least one network; <strong>${fmt(crossListedMulti)}</strong> in multiple. Surfaced on <a href="/directory-networks.html">directory-networks.html</a>.</li>
        <li><strong>Pastor-signature cross-references</strong> — pastors are matched against 7 canonical statement-signer ledgers (Nashville Statement 2017, Dallas Statement 2018, Warhurst Protest 2020, AMR Leadership 2026, PCA Letter of Lament 2025, Revoice speakers / endorsers, CBE Egalitarian Network). <strong>${fmt(totalSignerEntries)} signer entries</strong> indexed. Strict first+last name match, state corroboration on the two large lists, and denominational scope filtering on the small ones keep the false-positive rate low. Currently <strong>${fmt(sigCounts.green)} churches green-aggregate</strong>, ${fmt(sigCounts.red)} red, ${sigCounts.mixed} mixed — that's where the rare-but-decisive <em>"this pastor signed Nashville"</em> or <em>"this pastor signed Revoice"</em> call-outs come from.</li>
        <li><strong>Notable attendees</strong> — politicians, justices, and religious figures cross-referenced to their home churches. ${fmt(notableNames.size)} distinct individuals across ${fmt(notableCount)} churches. Powers the "where they worship" cross-reference on the <a href="/blog/resolute-citizen-7580-candidates-all-50-states-one-standard.html">RESOLUTE Citizen blog post</a> and the <a href="/directory-politicians.html">Politicians cross-reference page</a>.</li>
        <li><strong>Enrichment notes + sources</strong> — every editorial decision (rubric flag, denomination correction, dupe merge, signature match) appends a dated note and cites the source URL. The audit trail is the unique editorial defense — every claim is traceable.</li>
      </ul>
    </section>

    <section class="section">
      <h2>III. The MOOP rubric</h2>
      <p>MOOP is a doctrinal lens, not a neutral one. Records receive a categorical rating — <strong>green</strong> (recommended), <strong>yellow</strong> (caution / verify), <strong>red</strong> (significant concerns), or <strong>black</strong> (avoid — significant cultural or doctrinal drift). Automatic flags get applied by pattern detection wherever the underlying signal is unambiguous:</p>
      <ul class="rubric-list">
        <li class="red-pill"><strong>Female senior pastor → RED minimum.</strong> The directory holds a complementarian position on the church office of elder / pastor.</li>
        <li class="red-pill"><strong>LGBTQ-affirming denomination → RED minimum.</strong> Applies to PCUSA, ELCA, the United Methodist Church (post-Charlotte 2024), The Episcopal Church, the United Church of Christ, the Christian Church (Disciples of Christ), the mainline Reformed Church in America, and Mennonite Church USA. Conservative cousin denominations (PCA, OPC, ARP, EPC, LCMS, WELS, ACNA, Reformed Episcopal, URCNA, PRCA, etc.) are explicitly excluded by the auto-flagger.</li>
        <li class="black-pill"><strong>Prosperity gospel → BLACK.</strong> Includes campuses of Elevation, the Potter's House (T. D. Jakes), Lakewood (Joel Osteen), Joyce Meyer, and their affiliates.</li>
        <li><strong>Broken website alone is NOT a doctrinal flag.</strong> Many small churches operate primarily through Facebook; a dead website is a data-quality issue (note + needs_review), not a doctrinal red. We will not penalize a faithful small congregation for not having a tech volunteer.</li>
      </ul>
      <p>Manual review handles edge cases the rubric can't auto-decide.</p>
    </section>

    <section class="section">
      <h2>IV. What's still incomplete</h2>
      <p>An honest accounting of the known gaps:</p>
      <ul>
        <li><strong>${fmt(needsReview)} records flagged for follow-up review.</strong> The hardest pool is roughly 3,200 JavaScript-rendered SPA sites where pastor extraction needs a headless browser (Playwright pass pending). The next-hardest is around 700 churches with no website AND no Facebook — researchable only by phone or address.</li>
        <li><strong>Some legacy numeric ratings haven't been normalized.</strong> A small subset of pre-2026 records carry rating values on a 0–10 scale that pre-date the current categorical (green / yellow / red / black) system. Cosmetic but irritating on the per-church pages.</li>
        <li><strong>Some misleading slugs.</strong> A handful of record IDs carry stale tradition tags from earlier classification — the underlying denomination data is correct; only the URL slug hasn't been re-aligned.</li>
        <li><strong>Conservative-network bias — by design.</strong> The directory's editorial center is Reformed-evangelical and orthodox-Protestant. Affirming-denomination records exist but are sparse. We are not a neutral catalog; we name our compass so readers can calibrate.</li>
        <li><strong>No portfolio yet for the small-church website-build ministry offer.</strong> The data identifies hundreds of small churches without working web presence — the next step is sample-site demos and an intake-form / build pipeline before any outreach goes wide.</li>
      </ul>
    </section>

    <section class="section">
      <h2>V. What this is positioned for</h2>
      <p>In one sentence: <strong>it's a directory other directories can't compete with, because every record carries a defendable editorial verdict with citations.</strong> Three downstream uses:</p>
      <ul>
        <li><strong>Editorial pieces</strong> — the <a href="/blog/resolute-citizen-7580-candidates-all-50-states-one-standard.html">RESOLUTE Citizen post</a> cross-references 83 federal officials to their churches. More posts of that shape are possible: <em>Where the Nashville Statement Signers Lead Today</em>, <em>The Geographic Distribution of Egalitarian Theology in American Evangelicalism</em>, and similar.</li>
        <li><strong>Ministry outreach</strong> — small-church support work uses the editorial layer as a relationship-opener. The signature cross-reference, in particular, makes <em>"we noticed your pastor signed [statement]"</em> a natural lead-in. The website-build ministry to under-resourced churches is one concrete example in development.</li>
        <li><strong>Search engine presence</strong> — ${fmt(total)} pages at <code>usmcmin.org/churches/&lt;slug&gt;</code> are registered in the sitemap, each a substantive evaluation of a specific congregation. When a searcher Googles "<em>Grace Baptist Cape Coral pastor</em>," the MOOP page is built to rank — and to be the most informative result.</li>
      </ul>
    </section>

    <div class="updated-stamp">
      Last refreshed ${TODAY}
      <br>
      <a href="/churches.html">← Back to the church directory</a>
      <span class="sep">·</span>
      <a href="/directory-networks.html">Network cross-reference</a>
      <span class="sep">·</span>
      <a href="/directory-politicians.html">Where leaders worship</a>
      <span class="sep">·</span>
      <a href="/directory-drift.html">Drift watchlist</a>
      <span class="sep">·</span>
      <a href="/directory-roadmap.html">Roadmap</a>
    </div>
  </div>

  <footer>
    USMC Ministries · MOOP Church Directory · this page is regenerated from live data by <code>scripts/build-directory-methodology.js</code> · <a href="/">Home</a>
  </footer>
</body>
</html>
`;

fs.writeFileSync(OUTPUT, html);
console.log('Wrote', OUTPUT);
console.log('  Total churches:        ', fmt(total));
console.log('  Real pastors:          ', fmt(realPastors), '(' + pct(realPastors, total) + '%)');
console.log('  Facebook URLs:         ', fmt(facebook));
console.log('  YouTube channels:      ', fmt(youtube));
console.log('  Network cross-listings:', fmt(crossListedAny), '(' + fmt(crossListedMulti) + ' multi-network)');
console.log('  Signature aggregate:   ', fmt(sigCounts.green), 'green |', fmt(sigCounts.red), 'red |', sigCounts.mixed, 'mixed');
console.log('  Needs_review:          ', fmt(needsReview));
console.log('  Total signer entries:  ', fmt(totalSignerEntries));
console.log('  Notable attendees:     ', fmt(notableNames.size), 'across', fmt(notableCount), 'churches');
