#!/usr/bin/env node
'use strict';
// build-denomination-pages.js — generate the denomination directory from
// data/denominations/*.json + captured official source snapshots.
//
//   docs/data/denominations/index.json        public summary (scores, governance, ledger)
//   docs/data/denominations/<id>.json         one denomination, full evidence ledger
//   docs/data/denominations/church-links.json church_id -> denomination id (alias-normalized)
//   docs/denominations/index.html             index page
//   docs/denominations/<id>.html              detail page
//
// Refuses to write (exit 1) if any evidence row fails quote-in-source
// validation, any verified congregation fails, or a value is outside the schema.
// Read-only on churches.json.
const fs = require('fs');
const path = require('path');
const D = require('./lib/denominations.js');

const ROOT = path.join(__dirname, '..');
const OUT_DATA = path.join(ROOT, 'docs', 'data', 'denominations');
const OUT_HTML = path.join(ROOT, 'docs', 'denominations');
const CHECK = process.argv.includes('--check');

const esc = s => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const LABEL = { scripture: 'Scripture', christology: 'Christology', gender: 'Gender & Ordination', soteriology: 'Soteriology',
  preaching: 'Preaching', cultural: 'Cultural Engagement (marriage & sexuality)', leadership: 'Leadership & Elders', mission: 'Mission',
  mens_discipleship: "Men's Discipleship", denominational: 'Accountability Structure' };

function loadChurches() {
  const raw = JSON.parse(fs.readFileSync(path.join(ROOT, 'docs', 'data', 'churches.json'), 'utf8'));
  return Array.isArray(raw) ? raw : raw.churches;
}

function build() {
  const denoms = D.loadDenominations();
  const index = D.aliasIndex(denoms);
  const churches = loadChurches();
  const byId = new Map(churches.map(c => [c.id, c]));
  const errors = [];
  const out = [];
  const links = {};
  for (const c of churches) {
    const id = D.normalizeDenomination(c.denomination, index);
    if (id) links[c.id] = id;
  }
  for (const d of denoms) {
    const ledger = D.buildLedger(d);
    ledger.filter(l => !l.validated).forEach(l => errors.push(`${d.id}: evidence ${l.id}: ${l.error}`));
    const scored = D.scoreDenomination(d, ledger);
    for (const [cat, s] of Object.entries(scored.scores)) {
      if (!D.GRADES.includes(s.grade)) errors.push(`${d.id}: ${cat} grade ${s.grade} outside schema`);
      if (s.grade !== 'unknown' && (!s.rule || !(s.evidence || []).length) && !(s.rule && s.rule.id === 'D-DEN-1')) errors.push(`${d.id}: ${cat} graded without rule+evidence`);
    }
    if (scored.governance.strength && !D.GOVERNANCE.includes(scored.governance.strength)) errors.push(`${d.id}: governance outside schema`);
    const congregations = D.verifyCongregations(d, byId);
    congregations.filter(v => !v.validated).forEach(v => errors.push(`${d.id}: congregation ${v.church_id}: ${v.error}`));
    const members = Object.entries(links).filter(([, id]) => id === d.id).map(([cid]) => cid);
    out.push({ id: d.id, name: d.name, short_name: d.short_name, aliases: d.aliases, official_site: d.official_site,
      source_policy: d.source_policy, ...scored, ledger, verified_congregations: congregations, directory_church_count: members.length,
      page: `/denominations/${d.id}.html` });
  }
  return { out, links, errors };
}

const pageHead = (title, canonical, desc) => `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="canonical" href="https://usmcmin.org${canonical}">
  <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
  <meta name="description" content="${esc(desc)}">
  <title>${esc(title)} | MOOP Church Directory | USMC Ministries</title>
  <style>
    *{margin:0;padding:0;box-sizing:border-box}
    :root{--bg:#000;--card:#111;--gold:#D4AF37;--gold-light:#F4D470;--white:#e8e8e8;--gray:#9a9a9a;--border:#333;--green:#3ea14a;--yellow:#d4a437;--red:#c0392b;--black:#555}
    body{font-family:Inter,system-ui,sans-serif;background:var(--bg);color:var(--white);line-height:1.7}
    h1,h2,h3{font-family:'Playfair Display',Georgia,serif;color:var(--gold-light)}
    nav{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;padding:14px 20px;border-bottom:1px solid var(--border)}
    nav a{color:var(--gray);text-decoration:none;font-size:.85rem;padding:5px 12px}
    nav a:hover{color:var(--gold)}
    .container{max-width:900px;margin:0 auto;padding:36px 22px 60px}
    .crumb{color:var(--gray);font-size:.85rem}.crumb a{color:var(--gold);text-decoration:none}
    h1{font-size:clamp(1.8rem,4.5vw,2.5rem);margin:8px 0 10px}
    h2{font-size:1.35rem;margin:34px 0 12px}
    .card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:16px 18px;margin:12px 0}
    .note{color:var(--gray);font-size:.9rem}
    .pill{display:inline-block;padding:2px 10px;border-radius:12px;font-size:.78rem;font-weight:600;text-transform:uppercase;letter-spacing:.5px}
    .g-green{background:var(--green);color:#fff}.g-yellow{background:var(--yellow);color:#000}.g-red{background:var(--red);color:#fff}.g-black{background:var(--black);color:#fff}.g-unknown{background:#2a2a2a;color:var(--gray);border:1px solid var(--border)}
    table{width:100%;border-collapse:collapse;font-size:.92rem}td,th{border-bottom:1px solid var(--border);padding:9px 6px;text-align:left;vertical-align:top}
    blockquote{border-left:3px solid var(--gold);padding:4px 12px;margin:6px 0;color:#d8d8d8;font-style:italic}
    a{color:var(--gold)}
    footer{border-top:1px solid var(--border);padding:22px;text-align:center;color:var(--gray);font-size:.85rem}
  </style>
</head>
<body>
  <nav><a href="/">Home</a><a href="/churches.html">Church Directory</a><a href="/denominations/">Denominations</a><a href="/directory-methodology.html">Methodology</a></nav>
  <main class="container">`;
const pageFoot = `  </main>
  <footer>MOOP Nationwide Church Directory &middot; U.S.M.C. Ministries &middot; <a href="/directory-methodology.html">Methodology</a></footer>
</body>
</html>
`;
const pill = g => `<span class="pill g-${esc(g)}">${esc(g)}</span>`;

function detailHtml(d) {
  const ev = new Map(d.ledger.map(l => [l.id, l]));
  const rows = D.CATEGORIES.map(cat => {
    const s = d.scores[cat];
    const quotes = (s.evidence || []).map(id => ev.get(id)).filter(Boolean)
      .map(l => `<blockquote>&ldquo;${esc(l.quote)}&rdquo; &mdash; <a href="${esc(l.url)}" rel="noopener">${esc(l.url.replace(/^https?:\/\//, ''))}</a></blockquote>`).join('');
    const rule = s.rule ? `<div class="note">Rule ${esc(s.rule.id)}: ${esc(s.rule.text)}</div>` : `<div class="note">${esc(s.note)}</div>`;
    return `<tr><td><strong>${esc(LABEL[cat] || cat)}</strong></td><td>${pill(s.grade)}</td><td>${rule}${quotes}</td></tr>`;
  }).join('\n');
  const gov = d.governance;
  const govQuotes = (gov.evidence || []).map(id => ev.get(id)).filter(Boolean)
    .map(l => `<blockquote>&ldquo;${esc(l.quote)}&rdquo; &mdash; <a href="${esc(l.url)}" rel="noopener">${esc(l.url.replace(/^https?:\/\//, ''))}</a></blockquote>`).join('');
  const nuanceIds = ['efca-tp-no-women-ordination', 'efca-tp-ordination-males', 'efca-tp-women-certificate', 'efca-tp-elders-usually-men', 'efca-tp-no-local-policy', 'efca-tp-local-decides'];
  const nuance = d.id === 'efca' ? `
    <h2>Gender and leadership: the nuance</h2>
    <div class="card">
      <p>The EFCA's own statements draw three different lines, and they are not the same line:</p>
      <ol style="margin:10px 0 10px 22px">
        <li><strong>Ordination is for men.</strong> The 1988 General Conference decision and the credentialing booklet restrict the Certificate of Ordination to qualified men. That is binding on the denomination's own credentials.</li>
        <li><strong>Women serve in non-ordained vocational ministry.</strong> The EFCA grants women a Certificate of Christian Ministry. That is a staff role, not the pastoral office.</li>
        <li><strong>Elders are a local decision.</strong> Most EFCA churches restrict elders to men, but the EFCA states there is no official policy for local churches; each congregation decides.</li>
      </ol>
      <p class="note">So a given EFCA church can still have women elders. Leadership is graded YELLOW (mixed) at the denomination level for that reason, and the church's own page decides it.</p>
      ${nuanceIds.map(id => ev.get(id)).filter(Boolean).map(l => `<blockquote>&ldquo;${esc(l.quote)}&rdquo; &mdash; <a href="${esc(l.url)}" rel="noopener">efca.org</a></blockquote>`).join('\n      ')}
    </div>` : '';
  const congs = d.verified_congregations.map(v => `<li><a href="/churches/${esc(v.church_id)}.html">${esc(v.name)}</a> (${esc([v.city, v.state].filter(Boolean).join(', '))}) &mdash; <span class="note">affiliation stated on the church's own site:</span><blockquote>&ldquo;${esc(v.quote)}&rdquo; &mdash; <a href="${esc(v.url)}" rel="noopener">${esc(v.url.replace(/^https?:\/\//, ''))}</a></blockquote></li>`).join('\n');
  const ledgerRows = d.ledger.map(l => `<tr><td>${esc(l.id)}</td><td>&ldquo;${esc(l.quote)}&rdquo;<div class="note"><a href="${esc(l.url)}" rel="noopener">${esc(l.url)}</a></div></td><td class="note">${esc((l.retrieved_at || '').slice(0, 10))}<br>${esc(l.extractor || '')}<br>model: none<br>confidence ${l.confidence}</td></tr>`).join('\n');
  return pageHead(`${d.name} (${d.short_name})`, d.page, `${d.name}: MOOP denomination context, official-source evidence, governance strength.`) + `
    <div class="crumb"><a href="/churches.html">Church Directory</a> &rsaquo; <a href="/denominations/">Denominations</a> &rsaquo; ${esc(d.short_name)}</div>
    <h1>${esc(d.name)}</h1>
    <p>Context grade ${pill(d.context_grade)} &middot; Governance: <strong>${esc((gov.strength || 'unknown').toUpperCase())}</strong> &middot; ${d.directory_church_count} churches in the directory list this denomination.</p>
    <div class="card note"><strong>Context only.</strong> This grade describes the denomination's official statements. It is not any church's rating. Each church page is graded from that church's own evidence, and local evidence wins. A category is "unknown" when no official quote supports it.</div>
    <h2>MOOP categories</h2>
    <table><tr><th>Category</th><th>Grade</th><th>Rule and official evidence</th></tr>
${rows}
    </table>
    <h2>Governance strength</h2>
    <div class="card"><p>${pill((gov.strength || 'unknown'))} ${gov.rule ? esc(gov.rule.text) : 'No validated quote maps to a governance rule.'}</p>${govQuotes}</div>
${nuance}
    <h2>Verified congregations in this directory</h2>
    <ul style="margin-left:20px">${congs || '<li class="note">None verified yet.</li>'}</ul>
    <h2>Evidence ledger</h2>
    <p class="note">Every quote below is checked, word for word, against a snapshot of the official page taken on the date shown. ${esc(d.source_policy)}</p>
    <table><tr><th>ID</th><th>Quote and source</th><th>Retrieved / extractor</th></tr>
${ledgerRows}
    </table>
` + pageFoot;
}

function indexHtml(list) {
  const rows = list.map(d => `<tr><td><a href="${esc(d.page)}">${esc(d.name)}</a> (${esc(d.short_name)})</td><td>${pill(d.context_grade)}</td><td>${esc((d.governance.strength || 'unknown').toUpperCase())}</td><td>${d.directory_church_count}</td><td>${Object.values(d.scores).filter(s => s.grade === 'unknown').length} of ${D.CATEGORIES.length}</td></tr>`).join('\n');
  return pageHead('Denominations', '/denominations/', 'MOOP denomination directory: official-source evidence, category context grades and governance strength.') + `
    <div class="crumb"><a href="/churches.html">Church Directory</a> &rsaquo; Denominations</div>
    <h1>Denominations</h1>
    <p>Each denomination page grades the body's <em>official</em> statements against written rules, with the exact quote and source for every grade. A category with no supporting official quote is shown as unknown.</p>
    <div class="card note"><strong>Context only.</strong> A denomination grade never sets a church's rating. Church pages link here for context; the church's own evidence wins.</div>
    <table><tr><th>Denomination</th><th>Context grade</th><th>Governance</th><th>Churches listed</th><th>Unknown categories</th></tr>
${rows}
    </table>
    <p class="note" style="margin-top:18px">Governance strength: <strong>binding</strong> (decisions bind every congregation), <strong>mixed</strong> (a required common confession; practice decided locally), <strong>advisory</strong> (guidance only), <strong>autonomous</strong> (no required common confession).</p>
` + pageFoot;
}

const { out, links, errors } = build();
if (errors.length) { console.error('DENOMINATION BUILD REFUSED:\n  ' + errors.join('\n  ')); process.exit(1); }
const files = {
  [path.join(OUT_DATA, 'index.json')]: JSON.stringify({ generated_from: 'data/denominations/*.json', schema: { categories: D.CATEGORIES, grades: D.GRADES, governance: D.GOVERNANCE }, denominations: out.map(d => ({ id: d.id, name: d.name, short_name: d.short_name, context_grade: d.context_grade, governance: d.governance.strength, page: d.page, directory_church_count: d.directory_church_count })) }, null, 1) + '\n',
  [path.join(OUT_DATA, 'church-links.json')]: JSON.stringify({ note: 'church_id -> denomination id (exact alias match). Context only; the church page grade comes from local evidence.', links }, null, 0) + '\n',
  [path.join(OUT_HTML, 'index.html')]: indexHtml(out),
};
for (const d of out) {
  files[path.join(OUT_DATA, `${d.id}.json`)] = JSON.stringify(d, null, 1) + '\n';
  files[path.join(OUT_HTML, `${d.id}.html`)] = detailHtml(d);
}
let stale = 0;
for (const [f, body] of Object.entries(files)) {
  const cur = fs.existsSync(f) ? fs.readFileSync(f, 'utf8') : null;
  if (cur === body) continue;
  stale++;
  if (!CHECK) { fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, body); }
}
for (const d of out) {
  const g = Object.entries(d.scores).map(([k, s]) => `${k}=${s.grade}`).join(' ');
  console.log(`${d.id}: context=${d.context_grade} governance=${d.governance.strength} ledger=${d.ledger.length}/${d.ledger.filter(l => l.validated).length} valid churches=${d.directory_church_count} verified_congregations=${d.verified_congregations.length}\n  ${g}`);
}
if (CHECK) { console.log(stale ? `STALE: ${stale} generated file(s) differ` : 'denomination pages up to date'); process.exit(stale ? 1 : 0); }
console.log(`wrote ${stale} file(s)`);
