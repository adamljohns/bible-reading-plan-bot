#!/usr/bin/env node
// Phase 4 — Build docs/directory-networks.html
//
// Reads churches.json, extracts every record with `cross_listed_in`,
// groups by network, and renders a static HTML page with stats hero,
// per-network filter chips, sort options, and methodology notes.
//
// Output: docs/directory-networks.html

const fs = require('fs');
const path = require('path');
const { editorialRailHtml, editorialRailCss } = require('./editorial-rail');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const OUT = path.join(__dirname, '..', 'docs', 'directory-networks.html');

const NETWORK_META = {
  founders: {
    label: 'Founders Ministries',
    shortLabel: 'Founders',
    color: '#8B5E3C',
    directoryUrl: 'https://founders.org/our-network/',
    description: 'Reformed-Baptist confessional network ("Founders Friendly") affirming the 1689 LBC and complementarian polity.',
    methodology: 'Founders Ministries publishes a vetted "Founders Friendly" directory at <a href="https://founders.org" target="_blank" rel="noopener">founders.org</a>. Each listed church voluntarily affirms the 1689 London Baptist Confession + complementarian polity. <strong>Vetting strength: HIGH.</strong>',
  },
  '9marks': {
    label: '9Marks Church-Search',
    shortLabel: '9Marks',
    color: '#3F6F8F',
    directoryUrl: 'https://www.9marks.org/church-search/',
    description: '9Marks self-listing directory (Mark Dever) — churches self-identifying with the 9 Marks of a Healthy Church.',
    methodology: '9Marks publishes a Google-Maps backed church-finder at <a href="https://www.9marks.org/church-search/" target="_blank" rel="noopener">9marks.org/church-search</a>. <strong>Listings are user-submitted; 9Marks editorial staff does NOT individually vet entries.</strong> Treat inclusion as a self-attested signal of alignment with the 9 Marks (expositional preaching, congregational polity, complementarianism, biblical church discipline, meaningful membership, etc.) — <strong>not</strong> a 9Marks certification.',
  },
  'tgc-cn': {
    label: 'TGC Church Directory',
    shortLabel: 'TGC',
    color: '#4A7A4A',
    directoryUrl: 'https://www.thegospelcoalition.org/churches/',
    description: 'The Gospel Coalition\'s open Church Directory (sponsored by Midwestern Seminary) — broader Reformed-evangelical tent.',
    methodology: 'The Gospel Coalition publishes an open self-listing Church Directory at <a href="https://www.thegospelcoalition.org/churches/" target="_blank" rel="noopener">thegospelcoalition.org/churches</a>. <strong>~52% of listings carry no formal network affiliation</strong>; the rest declare Acts 29, SEND Network, Harbor Network, Converge, or Redeemer City to City. Directory presence does NOT imply TGC Foundation Documents vetting; verify complementarianism + inerrancy independently.',
  },
  acts29: {
    label: 'Acts 29',
    shortLabel: 'Acts 29',
    color: '#9F4A4A',
    directoryUrl: 'https://www.acts29.com/find-a-church/',
    description: 'Acts 29 church-planting network — Reformed-leaning evangelical, complementarian, missional. Globally distributed.',
    methodology: 'Acts 29 vets each church-planter through a residency before granting network membership. Distinctives: gospel-centered, Reformed soteriology, complementarian, missional church-planting, Spirit-empowered. Mark Driscoll was expelled in 2014; current leadership emphasizes accountability + elder plurality. <strong>Vetting strength: HIGH.</strong>',
  },
  sgc: {
    label: 'Sovereign Grace Churches',
    shortLabel: 'SGC',
    color: '#6A4A8A',
    directoryUrl: 'https://www.sovereigngrace.com/our-churches',
    description: 'Sovereign Grace Churches (C.J. Mahaney heritage) — Reformed-Baptist-flavored, continuationist-friendly, complementarian.',
    methodology: 'Sovereign Grace Churches requires confessional alignment with SGC\'s Statement of Faith and Polity for membership; tracked via the SGC office. Distinctives: doctrines of grace, continuationist (open to charismatic gifts within an orderly worship frame), complementarian, gospel-centered church-planting. <strong>Vetting strength: HIGH.</strong>',
  },
  'pillar-network': {
    label: 'Pillar Network',
    shortLabel: 'Pillar',
    color: '#5A7A9A',
    directoryUrl: 'https://thepillarnetwork.com/find-a-church/',
    description: 'Pillar Network — church-planting + revitalization, SBC-cooperating, Reformed-leaning, complementarian.',
    methodology: 'Pillar Network (<a href="https://thepillarnetwork.com" target="_blank" rel="noopener">thepillarnetwork.com</a>) is a church-planting and church-revitalization network headquartered in Wake Forest, NC. Members affirm shared doctrine and commit to plant or revitalize churches; partners with NAMB on certain plants. <strong>Vetting strength: HIGH.</strong>',
  },
  'trinity-foundation': {
    label: 'Trinity Foundation Registry',
    shortLabel: 'Trinity',
    color: '#7A5A3A',
    directoryUrl: 'https://trinityfoundation.org/churchapproved.php',
    description: 'Trinity Foundation Church Registry & Clearinghouse (Gordon Clark / John Robbins tradition) — vetted confessional Reformed clearinghouse.',
    methodology: 'The Trinity Foundation publishes a screened Church Registry & Clearinghouse at <a href="https://trinityfoundation.org/churchapproved.php" target="_blank" rel="noopener">trinityfoundation.org/churchapproved.php</a>. Explicit disclaimer: "We are not establishing a new denomination." Each entry is vetted against confessional Reformed standards (1689 LBCF, Westminster Confession of Faith 1729, or Three Forms of Unity). Smaller in scope but highly confessional. <strong>Vetting strength: HIGH.</strong>',
  },
};

const NETWORK_ORDER = ['founders', '9marks', 'tgc-cn', 'acts29', 'sgc', 'pillar-network', 'trinity-foundation'];

function escapeHtml(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function ratingClass(r) {
  if (!r) return 'pill-grey';
  const t = String(r).toLowerCase();
  if (t === 'green') return 'pill-green';
  if (t === 'yellow') return 'pill-yellow';
  if (t === 'red') return 'pill-red';
  if (t === 'black') return 'pill-black';
  return 'pill-grey';
}

function ratingLabel(r) {
  return r ? String(r).toUpperCase() : '—';
}

function loadData() {
  const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
  const records = d.churches.filter(c =>
    c && typeof c === 'object' && c.id &&
    Array.isArray(c.cross_listed_in) && c.cross_listed_in.length > 0
  );
  return { records, total_churches: d.churches.length };
}

function summarize(records) {
  const byNetwork = {};
  for (const k of NETWORK_ORDER) byNetwork[k] = 0;
  for (const r of records) {
    for (const n of r.cross_listed_in) {
      byNetwork[n] = (byNetwork[n] || 0) + 1;
    }
  }
  const multiListed = records.filter(r => r.cross_listed_in.length >= 2).length;
  return { byNetwork, multiListed };
}

function renderEntry(c) {
  const networks = c.cross_listed_in.filter(n => NETWORK_META[n]);
  const chips = networks.map(n => {
    const meta = NETWORK_META[n];
    // Clickable badge — opens the network's directory in a new tab so the user
    // can find this specific church within it. Title attribute gives a hover hint.
    const href = meta.directoryUrl || '#';
    return `<a class="net-chip" href="${escapeHtml(href)}" target="_blank" rel="noopener" style="--net-color:${meta.color};" data-net="${n}" title="Open ${escapeHtml(meta.label)} directory in a new tab">${escapeHtml(meta.shortLabel)}</a>`;
  }).join('');
  const dataNetworks = networks.join(' ');
  const stateMatch = String(c.address || '').match(/,\s*([A-Z]{2})\b/);
  const state = stateMatch ? stateMatch[1] : '';
  const detailHref = `/churches/${encodeURIComponent(c.id)}.html`;
  const pastor = c.pastor && c.pastor !== 'Verify on church website' ? c.pastor : '';
  const addressShort = String(c.address || '').replace(/\s+/g, ' ').trim();

  return `<article class="entry" data-networks="${dataNetworks}" data-state="${state}" data-rating="${escapeHtml(c.overall_rating || '')}" data-multi="${networks.length >= 2 ? '1' : '0'}" data-name="${escapeHtml((c.name || '').toLowerCase())}">
  <div class="entry-head">
    <h3><a href="${detailHref}">${escapeHtml(c.name || 'Untitled')}</a></h3>
    <span class="pill ${ratingClass(c.overall_rating)}">${ratingLabel(c.overall_rating)}</span>
  </div>
  <div class="addr">${escapeHtml(addressShort)}</div>
  ${pastor ? `<div class="pastor">Pastor: ${escapeHtml(pastor)}</div>` : ''}
  <div class="nets">${chips}</div>
</article>`;
}

function renderHtml({ records, summary, total_churches }) {
  records.sort((a, b) => {
    const al = a.cross_listed_in.length, bl = b.cross_listed_in.length;
    if (bl !== al) return bl - al;
    return String(a.name || '').localeCompare(String(b.name || ''));
  });

  const entriesHtml = records.map(renderEntry).join('\n');

  const chipFilters = NETWORK_ORDER.map(n => {
    const meta = NETWORK_META[n];
    const count = summary.byNetwork[n] || 0;
    return `<button class="filter-btn" data-filter-net="${n}" style="--net-color:${meta.color};"><span class="dot" style="background:${meta.color}"></span>${escapeHtml(meta.shortLabel)} <span class="count-suffix">(${count})</span></button>`;
  }).join('');

  const methodologyBlocks = NETWORK_ORDER.map(n => {
    const meta = NETWORK_META[n];
    const count = summary.byNetwork[n] || 0;
    return `<section class="meth-card" id="meth-${n}">
      <h3 style="border-left-color:${meta.color}"><span class="dot" style="background:${meta.color}"></span>${escapeHtml(meta.label)} <span class="count">${count} listed</span></h3>
      <p>${meta.methodology}</p>
    </section>`;
  }).join('');

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
  <meta name="description" content="Churches in the MOOP Directory cross-listed with major Reformed-evangelical networks — Founders, 9Marks, TGC, Acts 29, SGC, Pillar, Trinity Foundation.">
  <meta property="og:title" content="Church Networks | MOOP Church Directory">
  <meta property="og:description" content="Where MOOP churches appear in major Reformed-evangelical network directories, with methodology notes on each network's vetting standard.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://usmcmin.org/directory-networks.html">
  <title>Church Networks | MOOP Church Directory | USMC Ministries</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    :root { --bg:#000; --card:#111; --card2:#1a1a1a; --gold:#D4AF37; --gold-light:#F4D470; --white:#e8e8e8; --gray:#888; --border:#333; --green:#3ea14a; --yellow:#d4a437; --red:#c0392b; --black:#444; }
    body { font-family:'Inter',sans-serif; background:var(--bg); color:var(--white); min-height:100vh; line-height:1.6; }
    h1,h2,h3 { font-family:'Playfair Display',serif; }
    nav { display:flex; flex-wrap:wrap; gap:6px; justify-content:center; padding:14px 20px; border-bottom:1px solid var(--border); background:rgba(0,0,0,0.95); backdrop-filter:blur(8px); position:sticky; top:0; z-index:100; }
    nav a { color:var(--gray); text-decoration:none; font-size:0.85rem; font-weight:500; padding:5px 12px; border-radius:20px; border:1px solid transparent; transition:all 0.2s; white-space:nowrap; }
    nav a:hover { color:var(--gold); border-color:var(--border); }
    nav a.active { color:var(--gold) !important; border-color:var(--gold); }

    .container { max-width:1280px; margin:0 auto; padding:40px 20px 60px; }
    .hero { text-align:center; padding:30px 0 40px; border-bottom:1px solid var(--border); margin-bottom:30px; }
    .hero .breadcrumb { color:var(--gray); font-size:0.85rem; margin-bottom:12px; letter-spacing:1px; }
    .hero .breadcrumb a { color:var(--gold); text-decoration:none; }
    .hero h1 { font-size:clamp(1.9rem, 4.5vw, 2.6rem); color:var(--gold-light); margin:8px 0 14px; letter-spacing:0.5px; }
    .hero p { color:var(--gray); max-width:780px; margin:0 auto 18px; font-size:0.96rem; }

    .stat-row { display:grid; grid-template-columns:repeat(auto-fit, minmax(150px, 1fr)); gap:14px; margin:24px 0 8px; }
    .stat-card { background:var(--card); border:1px solid var(--border); border-radius:12px; padding:18px 14px; text-align:center; }
    .stat-card .stat-num { color:var(--gold); font-size:1.5rem; font-weight:700; font-family:'Playfair Display',serif; }
    .stat-card .stat-lbl { color:var(--gray); font-size:0.7rem; text-transform:uppercase; letter-spacing:1.2px; margin-top:6px; }

    .filter-bar { display:flex; flex-wrap:wrap; gap:8px; justify-content:center; padding:14px; background:var(--card); border:1px solid var(--border); border-radius:12px; margin:20px 0; }
    .filter-bar label { color:var(--gray); font-size:0.78rem; margin-right:6px; align-self:center; }
    .filter-btn { padding:6px 12px; background:transparent; color:var(--gray); border:1px solid var(--border); border-radius:18px; cursor:pointer; font-size:0.8rem; font-family:inherit; transition:all 0.2s; display:inline-flex; align-items:center; gap:6px; }
    .filter-btn .dot { width:8px; height:8px; border-radius:50%; display:inline-block; }
    .filter-btn .count-suffix { color:#666; font-size:0.7rem; }
    .filter-btn:hover { color:var(--gold-light); border-color:var(--gold); }
    .filter-btn.active { background:rgba(212,175,55,0.12); color:var(--gold-light); border-color:var(--gold); }

    .sort-bar { display:flex; flex-wrap:wrap; gap:10px; justify-content:center; align-items:center; margin:0 0 18px; color:var(--gray); font-size:0.84rem; }
    .sort-bar select { background:var(--card); color:var(--white); border:1px solid var(--border); border-radius:14px; padding:5px 10px; font-family:inherit; font-size:0.84rem; cursor:pointer; }
    .sort-bar input[type="search"] { background:var(--card); color:var(--white); border:1px solid var(--border); border-radius:14px; padding:5px 12px; font-family:inherit; font-size:0.84rem; min-width:200px; }
    .sort-bar input[type="search"]::placeholder { color:#666; }

    #visible-count { color:var(--gold-light); font-weight:600; }

    .entries-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(320px, 1fr)); gap:14px; margin-top:20px; }
    .entry { background:var(--card); border:1px solid var(--border); border-radius:10px; padding:16px; transition:border-color 0.2s; }
    .entry:hover { border-color:#555; }
    .entry.hidden { display:none; }
    .entry-head { display:flex; align-items:flex-start; gap:8px; justify-content:space-between; margin-bottom:6px; }
    .entry h3 { font-size:1.05rem; font-family:'Playfair Display',serif; line-height:1.3; flex:1; }
    .entry h3 a { color:var(--gold); text-decoration:none; }
    .entry h3 a:hover { color:var(--gold-light); text-decoration:underline; }
    .entry .pill { font-size:0.65rem; padding:2px 8px; border-radius:8px; font-weight:600; white-space:nowrap; flex:none; }
    .pill-green { background:#1d4926; color:#90e6a4; }
    .pill-yellow { background:#3c2f0e; color:#f4d470; }
    .pill-red { background:#3f1614; color:#e89c93; }
    .pill-black { background:#222; color:#888; }
    .pill-grey { background:#222; color:#888; }
    .entry .addr { color:var(--gray); font-size:0.8rem; line-height:1.4; margin:4px 0; }
    .entry .pastor { color:var(--gray); font-size:0.78rem; margin:4px 0 8px; }
    .entry .nets { display:flex; flex-wrap:wrap; gap:5px; margin-top:8px; padding-top:8px; border-top:1px dashed var(--border); }
    .net-chip { font-size:0.66rem; padding:2px 7px; border-radius:8px; border:1px solid var(--net-color, var(--border)); color:var(--net-color, var(--gray)); background:rgba(255,255,255,0.02); letter-spacing:0.4px; font-weight:500; text-decoration:none; cursor:pointer; transition:background 0.15s, color 0.15s; display:inline-block; }
    .net-chip:hover { background:var(--net-color, var(--gold)); color:#000; }
    .net-chip:focus { outline:1px solid var(--net-color, var(--gold)); outline-offset:2px; }

    .methodology { margin-top:50px; }
    .methodology h2 { color:var(--gold-light); font-size:1.4rem; margin-bottom:16px; }
    .meth-grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(340px, 1fr)); gap:14px; }
    .meth-card { background:var(--card2); border:1px solid var(--border); border-left:4px solid var(--gold); border-radius:10px; padding:18px; }
    .meth-card h3 { color:var(--gold-light); font-size:1.05rem; margin-bottom:8px; display:flex; align-items:center; gap:8px; }
    .meth-card h3 .dot { width:10px; height:10px; border-radius:50%; }
    .meth-card h3 .count { color:var(--gray); font-size:0.72rem; font-family:'Inter',sans-serif; font-weight:400; margin-left:auto; }
    .meth-card p { color:var(--gray); font-size:0.86rem; line-height:1.55; }
    .meth-card p a { color:var(--gold); text-decoration:none; border-bottom:1px dotted #555; }
    .meth-card p a:hover { color:var(--gold-light); border-color:var(--gold-light); }

    footer { padding:30px 20px; text-align:center; color:var(--gray); font-size:0.78rem; border-top:1px solid var(--border); margin-top:60px; }
    footer a { color:var(--gold); text-decoration:none; }

    @media (max-width:600px) {
      .container { padding:28px 14px 50px; }
      .entries-grid { grid-template-columns:1fr; }
      .sort-bar { flex-direction:column; align-items:stretch; }
      .sort-bar input[type="search"] { min-width:0; }
    }
    ${editorialRailCss}
  </style>
</head>
<body>
  <nav>
    <a href="/">Home</a>
    <a href="/churches.html">Directory</a>
    <a href="/directory-overview.html">Overview</a>
    <a href="/directory-politicians.html">Politicians</a>
    <a href="/directory-map.html">Map</a>
    <a href="/directory-networks.html" class="active">Networks</a>
    <a href="/directory-methodology.html">Methodology</a>
    <a href="/directory-drift.html">Drift</a>
    <a href="/directory-roadmap.html">Roadmap</a>
    <a href="/about.html">About</a>
  </nav>

  ${editorialRailHtml()}

  <div class="container">
    <div class="hero">
      <div class="breadcrumb"><a href="/">USMC Ministries</a> · <a href="/churches.html">Church Directory</a></div>
      <h1>Church Networks</h1>
      <p>Where MOOP churches appear in major Reformed-evangelical network directories — Founders, 9Marks, TGC, Acts 29, Sovereign Grace, Pillar, and the Trinity Foundation Registry. Each network has its own vetting standard; we surface presence as a discoverability signal alongside MOOP's own scoring, not as a doctrinal endorsement.</p>
      <div class="stat-row">
        <div class="stat-card"><div class="stat-num">${NETWORK_ORDER.length}</div><div class="stat-lbl">networks tracked</div></div>
        <div class="stat-card"><div class="stat-num">${records.length}</div><div class="stat-lbl">churches listed</div></div>
        <div class="stat-card"><div class="stat-num">${summary.multiListed}</div><div class="stat-lbl">multi-network</div></div>
        <div class="stat-card"><div class="stat-num">${total_churches.toLocaleString()}</div><div class="stat-lbl">total in MOOP</div></div>
      </div>
    </div>

    <div class="filter-bar">
      <label>Filter by network:</label>
      ${chipFilters}
      <button class="filter-btn" data-filter-net="multi"><span class="dot" style="background:#D4AF37"></span>Multi-network only</button>
      <button class="filter-btn" data-filter-net="__all__">All</button>
    </div>

    <div class="sort-bar">
      <label for="sort">Sort:</label>
      <select id="sort">
        <option value="multi">Cross-listings (most first)</option>
        <option value="name">Name (A-Z)</option>
        <option value="state">State</option>
        <option value="rating">Rating (green first)</option>
      </select>
      <input type="search" id="q" placeholder="Search name or state…">
      <span><span id="visible-count">${records.length}</span> of ${records.length} shown</span>
    </div>

    <div class="entries-grid" id="entries-grid">
${entriesHtml}
    </div>

    <section class="methodology">
      <h2>Network Methodology Notes</h2>
      <div class="meth-grid">
        ${methodologyBlocks}
      </div>
    </section>
  </div>

  <footer>
    Generated ${new Date().toISOString().slice(0, 10)} · <a href="/">USMC Ministries</a> · MOOP Church Directory · cross-references built by automated scrape + match (Founders / 9Marks / TGC / Acts 29 / SGC / Pillar / Trinity Foundation directories)
  </footer>

  <script>
    (function() {
      const grid = document.getElementById('entries-grid');
      const entries = Array.from(grid.querySelectorAll('.entry'));
      const sortSel = document.getElementById('sort');
      const search = document.getElementById('q');
      const counter = document.getElementById('visible-count');
      const filterBtns = Array.from(document.querySelectorAll('.filter-btn'));
      let activeFilter = '__all__';

      function applyFilter() {
        const q = (search.value || '').toLowerCase().trim();
        let visible = 0;
        for (const el of entries) {
          const nets = (el.dataset.networks || '').split(/\\s+/);
          const passFilter = activeFilter === '__all__'
            ? true
            : activeFilter === 'multi'
              ? el.dataset.multi === '1'
              : nets.includes(activeFilter);
          const passQ = !q
            || (el.dataset.name || '').includes(q)
            || (el.dataset.state || '').toLowerCase().includes(q);
          if (passFilter && passQ) { el.classList.remove('hidden'); visible++; }
          else { el.classList.add('hidden'); }
        }
        counter.textContent = visible.toLocaleString();
      }

      function applySort() {
        const mode = sortSel.value;
        const sorted = entries.slice().sort((a, b) => {
          if (mode === 'name') return (a.dataset.name || '').localeCompare(b.dataset.name || '');
          if (mode === 'state') return (a.dataset.state || '').localeCompare(b.dataset.state || '');
          if (mode === 'rating') {
            const order = { green:0, yellow:1, red:2, black:3, '':4 };
            return (order[a.dataset.rating] ?? 5) - (order[b.dataset.rating] ?? 5);
          }
          const al = (a.dataset.networks || '').split(/\\s+/).length;
          const bl = (b.dataset.networks || '').split(/\\s+/).length;
          if (bl !== al) return bl - al;
          return (a.dataset.name || '').localeCompare(b.dataset.name || '');
        });
        for (const el of sorted) grid.appendChild(el);
      }

      filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          filterBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          activeFilter = btn.dataset.filterNet;
          applyFilter();
        });
      });

      sortSel.addEventListener('change', applySort);
      search.addEventListener('input', applyFilter);

      // Default: All active
      const allBtn = document.querySelector('.filter-btn[data-filter-net="__all__"]');
      if (allBtn) allBtn.classList.add('active');
    })();
  </script>
</body>
</html>
`;
}

function main() {
  const { records, total_churches } = loadData();
  const summary = summarize(records);
  const html = renderHtml({ records, summary, total_churches });
  fs.writeFileSync(OUT, html);
  console.log(`Wrote ${OUT}`);
  console.log(`  ${records.length} churches with network cross-listings`);
  console.log(`  ${summary.multiListed} multi-network`);
  console.log(`  Networks: ${NETWORK_ORDER.map(n => `${NETWORK_META[n].shortLabel}:${summary.byNetwork[n]||0}`).join(' / ')}`);
}

if (require.main === module) main();
