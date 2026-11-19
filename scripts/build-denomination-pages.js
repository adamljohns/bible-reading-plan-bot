#!/usr/bin/env node
'use strict';
// build-denomination-pages.js — generate the denomination directory from
// data/denominations/*.json + captured official source snapshots.
//
//   docs/data/denominations/index.json        public summary (scores, governance, ledger)
//   docs/data/denominations/<id>.json         one denomination, full evidence ledger
//   docs/data/denominations/church-links.json church_id -> denomination id (alias-normalized)
//   docs/denominations/index.html             index page
//   docs/denominations/<id>.html              detail page (lists its directory churches)
//   docs/data/denominations/label-links.json  label -> graded page (alias map)
//   docs/assets/js/denomination-links.js      DenomLinks.html(label) for cards/filters/map
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
  D.aliasIndex(denoms); // throws on any alias collision
  const churches = loadChurches();
  const byId = new Map(churches.map(c => [c.id, c]));
  const errors = [];
  const out = [];
  // Link targets: bodies the alias map marks graded_page AND that have a ledger
  // here (so the page is built by this script). Any other label stays plain text.
  const graded = new Set(denoms.map(d => d.id));
  const amap = D.loadAliasMap();
  for (const b of amap.doc.bodies) if (b.graded_page && !graded.has(b.id)) errors.push(`alias map marks ${b.id} graded_page but data/denominations/${b.id}.json is missing`);
  // Stub pages (CCW-1119-DIR3): every mapped body without a ledger gets a
  // "Not yet graded" page, so every mapped label links. No grade, no quotes.
  const stubBodies = amap.doc.bodies.filter(b => !graded.has(b.id));
  const linkable = new Set([...amap.doc.bodies.filter(b => b.graded_page && graded.has(b.id)).map(b => b.id), ...stubBodies.map(b => b.id)]);
  // Approved exclusions (data/crosslinks/denomination-link-exclusions.json):
  // churches whose label names a graded body but which have left it or are not
  // confirmed current. Fail closed: an unknown id, a missing evidence URL or a
  // body this script does not build refuses the build.
  const exclude = new Set();
  for (const x of EXCLUSIONS) {
    if (!byId.has(x.church_id)) errors.push(`link exclusion ${x.church_id}: not in churches.json`);
    if (!(x.evidence || []).length) errors.push(`link exclusion ${x.church_id}: no evidence`);
    if (!linkable.has(x.denomination)) errors.push(`link exclusion ${x.church_id}: unknown body ${x.denomination}`);
    exclude.add(x.church_id);
  }
  const links = {};
  for (const c of churches) {
    if (exclude.has(c.id)) continue;
    const k = D.classifyDenomination(c.denomination, amap);
    if (k.status === 'body' && linkable.has(k.id)) links[c.id] = k.id;
  }
  // The main directory's Refine filter groups by denomination_family (falling
  // back to the label). A family value links only when EVERY church carrying it
  // links to the same body; mixed or unmapped families stay plain text.
  const famIds = new Map();
  for (const c of churches) {
    const v = c.denomination_family || c.denomination;
    if (!v || exclude.has(c.id)) continue; // excluded churches render plain via EXCLUDE in the helper
    const id = links[c.id] || null;
    famIds.set(v, famIds.has(v) && famIds.get(v) !== id ? null : id);
  }
  const familyLinks = {};
  // The value must also name the body itself (alias map says so, or it carries the
  // body's short name) and must not be a generic family or a disputed alignment.
  const shortOf = new Map([...amap.doc.bodies.map(b => [b.id, b.short_name]), ...denoms.map(d => [d.id, d.short_name])]);
  for (const [v, id] of [...famIds].sort((a, b) => a[0].localeCompare(b[0]))) {
    if (!id) continue;
    const k = D.classifyDenomination(v, amap);
    if (k.status === 'generic' || /disputed|dual|likely/i.test(v)) continue;
    const sn = String(shortOf.get(id) || '').replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    if ((k.status === 'body' && k.id === id) || (sn && new RegExp(`\\b${sn}\\b`).test(v))) familyLinks[v] = id;
  }
  // Same decision, keyed by label, for the client-side cards, filters and map.
  const labelLinks = { exact: {}, loose: {} };
  for (const l of amap.doc.labels) {
    if (l.status !== 'body' || !linkable.has(l.id)) continue;
    labelLinks.exact[l.label] = l.id;
    const lk = amap.loose.get(D.aliasKey(l.label));
    if (lk && lk.status === 'body' && lk.id === l.id) labelLinks.loose[D.aliasKey(l.label)] = l.id;
  }
  for (const d of denoms) {
    const ledger = D.buildLedger(d);
    ledger.filter(l => !l.validated).forEach(l => errors.push(`${d.id}: evidence ${l.id}: ${l.error}`));
    const scored = D.scoreDenomination(d, ledger);
    for (const [cat, s] of Object.entries(scored.scores)) {
      if (!D.GRADES.includes(s.grade)) errors.push(`${d.id}: ${cat} grade ${s.grade} outside schema`);
      if (s.grade !== 'unknown' && (!s.rule || !(s.evidence || []).length)) errors.push(`${d.id}: ${cat} graded without rule+evidence`);
    }
    if (scored.governance.strength && !D.GOVERNANCE.includes(scored.governance.strength)) errors.push(`${d.id}: governance outside schema`);
    const congregations = D.verifyCongregations(d, byId);
    congregations.filter(v => !v.validated).forEach(v => errors.push(`${d.id}: congregation ${v.church_id}: ${v.error}`));
    const members = Object.entries(links).filter(([, id]) => id === d.id).map(([cid]) => cid);
    const memberRows = members.map(cid => byId.get(cid)).filter(c => c && fs.existsSync(path.join(ROOT, 'docs', 'churches', `${c.id}.html`)))
      .map(c => ({ id: c.id, name: c.name, city: c.city || '', state: c.state || '', label: c.denomination }))
      .sort((a, b) => (a.state || '~').localeCompare(b.state || '~') || a.name.localeCompare(b.name));
    out.push({ id: d.id, name: d.name, short_name: d.short_name, aliases: d.aliases, official_site: d.official_site,
      source_policy: d.source_policy, nuance: d.nuance || null, ...scored, ledger, verified_congregations: congregations, directory_church_count: members.length,
      page: `/denominations/${d.id}.html`, churches: memberRows });
  }
  const memberRowsOf = id => Object.entries(links).filter(([, x]) => x === id).map(([cid]) => byId.get(cid))
    .filter(c => c && fs.existsSync(path.join(ROOT, 'docs', 'churches', `${c.id}.html`)))
    .map(c => ({ id: c.id, name: c.name, city: c.city || '', state: c.state || '', label: c.denomination }))
    .sort((a, b) => (a.state || '~').localeCompare(b.state || '~') || a.name.localeCompare(b.name));
  const stubs = stubBodies.map(b => {
    const v = SITES.verified[b.id];
    const site = v && v.ok && v.http_status === 200 && v.url === SITES.proposed[b.id] ? v.url : null;
    const members = Object.values(links).filter(x => x === b.id).length;
    return { id: b.id, name: b.name, short_name: b.short_name, family: b.family || null, stub: true, official_site: site,
      official_site_checked: site ? v.checked_at : null, directory_church_count: members, page: `/denominations/${b.id}.html`, churches: memberRowsOf(b.id) };
  }).sort((a, b) => b.directory_church_count - a.directory_church_count || a.name.localeCompare(b.name));
  return { out, stubs, links, labelLinks, familyLinks, exclude: [...exclude].sort(), errors };
}
const SITES = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'denominations', 'sites', 'official-sites.json'), 'utf8'));
const EXCLUSIONS = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'crosslinks', 'denomination-link-exclusions.json'), 'utf8')).exclusions;

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
    .g-green{background:var(--green);color:#fff}.g-yellow{background:var(--yellow);color:#000}.g-red{background:var(--red);color:#fff}.g-black{background:var(--black);color:#fff}.g-unknown{background:#2a2a2a;color:var(--gray);border:1px solid var(--border)}.g-limited{background:#6b6b6b;color:#fff}.g-stub{background:#2a2a2a;color:var(--gray);border:1px dashed var(--gray)}
    .why{margin:-4px 0 10px;font-size:.95rem}.banner{background:#1a1a1a;border:1px dashed var(--gold);border-radius:10px;padding:14px 18px;margin:14px 0}
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
// Internal cross-links (CCW-1119-DIR2 Phase 4). Source: data/crosslinks/denomination-related-links.json.
// A link whose page is not in docs/ refuses the build, so this block can never ship a 404.
const RELATED = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'crosslinks', 'denomination-related-links.json'), 'utf8'));
const relatedErrors = [];
function relatedHtml(id) {
  const links = [...(RELATED[id] || []), ...(RELATED._all || [])];
  for (const l of links) {
    const rel = l.href.replace(/^\//, '');
    const file = path.join(ROOT, 'docs', rel.endsWith('/') ? rel + 'index.html' : rel);
    if (!l.href.startsWith('/') || !fs.existsSync(file)) relatedErrors.push(`related-links ${id}: ${l.href} has no page in docs/`);
  }
  if (!links.length) return '';
  return `    <h2>Related on this site</h2>
    <ul style="margin-left:20px">${links.map(l => `<li><a href="${esc(l.href)}">${esc(l.label)}</a></li>`).join('')}</ul>
`;
}
const pill = g => `<span class="pill g-${esc(g)}">${esc(g === 'limited' ? 'Limited evidence' : g)}</span>`;
const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
// "Red because of: Gender & Ordination; Leadership & Elders." (CCW-1119-DIR3)
function whyLine(d) {
  const cats = (d.because || []).map(c => LABEL[c] || c).join('; ');
  if (d.limited_evidence) return `Only ${d.graded_count} of ${D.CATEGORIES.length} categories have an official quote. This is not a full assessment.` + (cats ? ` Graded so far (${esc(d.context_grade)}): ${esc(cats)}.` : '');
  return `${cap(d.overall_grade)} because of: ${esc(cats)}.`;
}

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
    </div>` : (d.nuance ? `
    <h2>${esc(d.nuance.title)}</h2>
    <div class="card">
      ${(d.nuance.paragraphs || []).map(p => `<p>${esc(p)}</p>`).join('\n      ')}
      ${(d.nuance.evidence || []).map(id => ev.get(id)).filter(l => l && l.validated).map(l => `<blockquote>&ldquo;${esc(l.quote)}&rdquo; &mdash; <a href="${esc(l.url)}" rel="noopener">${esc(l.url.replace(/^https?:\/\/(www\.)?/, '').split('/')[0])}</a></blockquote>`).join('\n      ')}
    </div>` : '');
  const congs = d.verified_congregations.map(v => `<li><a href="/churches/${esc(v.church_id)}.html">${esc(v.name)}</a> (${esc([v.city, v.state].filter(Boolean).join(', '))}) &mdash; <span class="note">affiliation stated on the church's own site:</span><blockquote>&ldquo;${esc(v.quote)}&rdquo; &mdash; <a href="${esc(v.url)}" rel="noopener">${esc(v.url.replace(/^https?:\/\//, ''))}</a></blockquote></li>`).join('\n');
  const ledgerRows = d.ledger.map(l => `<tr><td>${esc(l.id)}</td><td>&ldquo;${esc(l.quote)}&rdquo;<div class="note"><a href="${esc(l.url)}" rel="noopener">${esc(l.url)}</a>${l.linked_from ? ` (linked from <a href="${esc(l.linked_from)}" rel="noopener">${esc(l.linked_from.replace(/^https?:\/\//, ''))}</a>)` : ''}</div></td><td class="note">${esc((l.retrieved_at || '').slice(0, 10))}<br>${esc(l.extractor || '')}<br>checked against: ${esc(l.body_region ? 'document body (' + l.body_region + ')' : 'document body')}<br>model: ${esc(l.model || 'none')}<br>confidence ${l.confidence}</td></tr>`).join('\n');
  const churchList = churchListHtml(d.churches);
  return pageHead(`${d.name} (${d.short_name})`, d.page, `${d.name}: MOOP denomination context, official-source evidence, governance strength.`) + `
    <div class="crumb"><a href="/churches.html">Church Directory</a> &rsaquo; <a href="/denominations/">Denominations</a> &rsaquo; ${esc(d.short_name)}</div>
    <h1>${esc(d.name)}</h1>
    <p>Overall grade ${pill(d.overall_grade)} &middot; Governance: <strong>${esc((gov.strength || 'unknown').toUpperCase())}</strong> &middot; <a href="#churches">${d.directory_church_count} churches</a> in the directory list this denomination.</p>
    <p class="why"><strong>${d.limited_evidence ? 'Limited evidence.' : 'Why this grade.'}</strong> ${whyLine(d)}</p>
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
    <h2 id="churches">Churches in the directory (${d.churches.length})</h2>
    <p class="note">Churches whose listed denomination maps to the ${esc(d.short_name)}. Listing is context only; each church page carries its own grade from its own evidence.</p>
${churchList || '<p class="note">None listed.</p>'}
    <h2>Evidence ledger</h2>
    <p class="note">Every quote below is checked, word for word, against a snapshot of the official page taken on the date shown. ${esc(d.source_policy)}</p>
    <table><tr><th>ID</th><th>Quote and source</th><th>Retrieved / extractor</th></tr>
${ledgerRows}
    </table>
${relatedHtml(d.id)}` + pageFoot;
}

function churchListHtml(churches) {
  const byState = new Map();
  for (const c of churches) { const k = c.state || 'Other'; if (!byState.has(k)) byState.set(k, []); byState.get(k).push(c); }
  return [...byState].map(([st, cs]) => `<details><summary><strong>${esc(st)}</strong> (${cs.length})</summary><ul style="margin:6px 0 10px 20px">${cs.map(c => `<li><a href="/churches/${esc(c.id)}.html">${esc(c.name)}</a>${c.city ? ` <span class="note">${esc(c.city)}</span>` : ''}</li>`).join('')}</ul></details>`).join('\n');
}

function stubHtml(s) {
  const site = s.official_site
    ? `<p>Official site: <a href="${esc(s.official_site)}" rel="noopener">${esc(s.official_site.replace(/^https?:\/\/(www\.)?/, '').replace(/\/$/, ''))}</a> <span class="note">(checked ${esc((s.official_site_checked || '').slice(0, 10))})</span></p>`
    : '<p class="note">Official site: not yet verified, so no link is shown.</p>';
  return pageHead(`${s.name} (${s.short_name})`, s.page, `${s.name}: not yet graded. Churches in the MOOP directory that list this denomination.`) + `
    <div class="crumb"><a href="/churches.html">Church Directory</a> &rsaquo; <a href="/denominations/">Denominations</a> &rsaquo; ${esc(s.short_name)}</div>
    <h1>${esc(s.name)}</h1>
    <div class="banner"><span class="pill g-stub">Not yet graded</span> <strong>Not yet graded. Official statements are being reviewed.</strong>
      <p class="note" style="margin-top:6px">This page carries no grade and no quotes yet. A grade appears only when an official statement, quoted word for word, maps to a published rule. Until then, judge each church by its own page.</p></div>
    ${site}
    <p><a href="#churches">${s.directory_church_count} churches</a> in the directory list this denomination.</p>
    <h2 id="churches">Churches in the directory (${s.churches.length})</h2>
    <p class="note">Churches whose listed denomination maps to the ${esc(s.short_name)}. Each church page carries its own grade from its own evidence.</p>
${churchListHtml(s.churches) || '<p class="note">None listed.</p>'}
` + pageFoot;
}

function indexHtml(list, stubs) {
  const stubRows = stubs.map(s => `<tr><td><a href="${esc(s.page)}">${esc(s.name)}</a> (${esc(s.short_name)})</td><td><a href="${esc(s.page)}#churches">${s.directory_church_count}</a></td><td>${s.official_site ? `<a href="${esc(s.official_site)}" rel="noopener">${esc(s.official_site.replace(/^https?:\/\/(www\.)?/, '').replace(/\/$/, ''))}</a>` : '<span class="note">not verified</span>'}</td></tr>`).join('\n');
  const rows = list.map(d => `<tr><td><a href="${esc(d.page)}">${esc(d.name)}</a> (${esc(d.short_name)})<div class="note">${whyLine(d)}</div></td><td>${pill(d.overall_grade)}</td><td>${esc((d.governance.strength || 'unknown').toUpperCase())}</td><td><a href="${esc(d.page)}#churches">${d.directory_church_count}</a></td><td>${Object.values(d.scores).filter(s => s.grade === 'unknown').length} of ${D.CATEGORIES.length}</td></tr>`).join('\n');
  return pageHead('Denominations', '/denominations/', 'MOOP denomination directory: official-source evidence, category context grades and governance strength.') + `
    <div class="crumb"><a href="/churches.html">Church Directory</a> &rsaquo; Denominations</div>
    <h1>Denominations</h1>
    <p>Each denomination page grades the body's <em>official</em> statements against written rules, with the exact quote and source for every grade. A category with no supporting official quote is shown as unknown.</p>
    <div class="card note"><strong>Context only.</strong> A denomination grade never sets a church's rating. Church pages link here for context; the church's own evidence wins.</div>
    <table><tr><th>Denomination</th><th>Overall grade</th><th>Governance</th><th>Churches listed</th><th>Unknown categories</th></tr>
${rows}
    </table>
    <p class="note" style="margin-top:10px">"Limited evidence" means fewer than ${D.MIN_GRADED} of ${D.CATEGORIES.length} categories have an official quote, so no overall color is given.</p>
    <h2 id="not-yet-graded">Not yet graded (${stubs.length})</h2>
    <p class="note">These bodies have a page listing their directory churches, but no grade yet. Official statements are being reviewed; a grade appears only when a word-for-word official quote maps to a published rule.</p>
    <table><tr><th>Denomination</th><th>Churches listed</th><th>Official site</th></tr>
${stubRows}
    </table>
    <p class="note" style="margin-top:18px">Governance strength: <strong>binding</strong> (decisions bind every congregation), <strong>mixed</strong> (a required common confession; practice decided locally), <strong>advisory</strong> (guidance only), <strong>autonomous</strong> (no required common confession).</p>
${relatedHtml('_index')}` + pageFoot;
}

const { out, stubs, links, labelLinks, familyLinks, exclude, errors } = build();
if (errors.length) { console.error('DENOMINATION BUILD REFUSED:\n  ' + errors.join('\n  ')); process.exit(1); }
const files = {
  [path.join(OUT_DATA, 'index.json')]: JSON.stringify({ generated_from: 'data/denominations/*.json', schema: { categories: D.CATEGORIES, grades: D.GRADES, governance: D.GOVERNANCE }, denominations: [...out.map(d => ({ id: d.id, name: d.name, short_name: d.short_name, context_grade: d.context_grade, overall_grade: d.overall_grade, limited_evidence: d.limited_evidence, graded_count: d.graded_count, because: d.because, governance: d.governance.strength, page: d.page, directory_church_count: d.directory_church_count })),
    ...stubs.map(s => ({ id: s.id, name: s.name, short_name: s.short_name, stub: true, context_grade: null, overall_grade: 'not_yet_graded', official_site: s.official_site, page: s.page, directory_church_count: s.directory_church_count }))] }, null, 1) + '\n',
  [path.join(OUT_DATA, 'church-links.json')]: JSON.stringify({ note: 'church_id -> denomination id (exact alias match). Context only; the church page grade comes from local evidence.', links }, null, 0) + '\n',
  [path.join(OUT_HTML, 'index.html')]: indexHtml(out, stubs),
};
// Client helper for cards, search results, filters and map popups. Generated
// here so it can only name pages this script builds; consumer pages load it with
// ?v=<content hash> (site assets are cached immutable), rewritten below.
const pagesById = Object.fromEntries([...out, ...stubs].map(d => [d.id, { page: d.page, short_name: d.short_name, name: d.name }]));
const linksJs = `/* GENERATED by scripts/build-denomination-pages.js - do not edit. */
(function () {
  'use strict';
  var EXACT = ${JSON.stringify(labelLinks.exact)};
  var LOOSE = ${JSON.stringify(labelLinks.loose)};
  var FAMILY = ${JSON.stringify(familyLinks)};
  var PAGES = ${JSON.stringify(pagesById)};
  // Church ids that never link (data/crosslinks/denomination-link-exclusions.json).
  var EXCLUDE = ${JSON.stringify(Object.fromEntries(exclude.map(id => [id, 1])))};
  function key(s) {
    return String(s || '').replace(/[\\u2018\\u2019]/g, "'").replace(/[\\u201c\\u201d]/g, '"').replace(/[\\u2013\\u2014]/g, '-')
      .replace(/\\u00a0/g, ' ').replace(/\\s+/g, ' ').trim().toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  }
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  // Graded page for a raw directory label, or null (generic labels stay plain text).
  function lookup(label, churchId) {
    if (label == null || label === '') return null;
    if (churchId && Object.prototype.hasOwnProperty.call(EXCLUDE, churchId)) return null;
    var s = String(label);
    var id = Object.prototype.hasOwnProperty.call(EXACT, s) ? EXACT[s] : (Object.prototype.hasOwnProperty.call(EXACT, s.trim()) ? EXACT[s.trim()] : LOOSE[key(s)]);
    return id && PAGES[id] ? { id: id, page: PAGES[id].page, short_name: PAGES[id].short_name, name: PAGES[id].name } : null;
  }
  // Refine-filter value (denomination_family or label): links only when every
  // church carrying that value links to the same graded page.
  function lookupFamily(value, churchId) {
    if (value == null || value === '') return null;
    if (churchId && Object.prototype.hasOwnProperty.call(EXCLUDE, churchId)) return null;
    var id = Object.prototype.hasOwnProperty.call(FAMILY, value) ? FAMILY[value] : null;
    return id && PAGES[id] ? { id: id, page: PAGES[id].page, short_name: PAGES[id].short_name, name: PAGES[id].name } : null;
  }
  // Escaped label, wrapped in a link to its denomination page when one exists.
  function html(label, fallback, churchId) {
    var hit = lookup(label, churchId);
    var text = esc(label || fallback || '');
    if (!hit) return text;
    return '<a class="denom-link" href="' + hit.page + '" title="' + esc(hit.name) + ': denomination context (context only)" onclick="event.stopPropagation()">' + text + '</a>';
  }
  // Same, for a denomination_family-keyed value (Refine filter, map points).
  function htmlFamily(value, churchId) {
    var hit = lookupFamily(value, churchId);
    var text = esc(value || '');
    if (!hit) return text;
    return '<a class="denom-link" href="' + hit.page + '" title="' + esc(hit.name) + ': denomination context (context only)" onclick="event.stopPropagation()">' + text + '</a>';
  }
  window.DenomLinks = { lookup: lookup, lookupFamily: lookupFamily, html: html, htmlFamily: htmlFamily };
})();
`;
const JS_FILE = path.join(ROOT, 'docs', 'assets', 'js', 'denomination-links.js');
const jsVer = require('crypto').createHash('sha256').update(linksJs).digest('hex').slice(0, 10);
files[JS_FILE] = linksJs;
files[path.join(OUT_DATA, 'label-links.json')] = JSON.stringify({ note: 'raw directory label -> denomination id with a graded page (alias map; generic labels absent). exact first, then loose = aliasKey(label).', ...labelLinks, family: familyLinks, exclude, pages: pagesById }, null, 1) + '\n';
const CONSUMERS = ['churches.html', 'churches-fxbg.html', 'churches-virginia.html', 'churches-dc.html', 'directory-map.html'];
for (const name of CONSUMERS) {
  const f = path.join(ROOT, 'docs', name);
  const cur = fs.readFileSync(f, 'utf8');
  const re = /<script src="\/assets\/js\/denomination-links\.js\?v=[0-9a-f]+"><\/script>/;
  if (!re.test(cur)) { errors.push(`docs/${name} does not load /assets/js/denomination-links.js`); continue; }
  files[f] = cur.replace(re, `<script src="/assets/js/denomination-links.js?v=${jsVer}"></script>`);
}
if (errors.length) { console.error('DENOMINATION BUILD REFUSED:\n  ' + errors.join('\n  ')); process.exit(1); }
for (const d of out) {
  files[path.join(OUT_DATA, `${d.id}.json`)] = JSON.stringify(d, null, 1) + '\n';
  files[path.join(OUT_HTML, `${d.id}.html`)] = detailHtml(d);
}
for (const s of stubs) files[path.join(OUT_HTML, `${s.id}.html`)] = stubHtml(s);
if (relatedErrors.length) { console.error('DENOMINATION BUILD REFUSED:\n  ' + [...new Set(relatedErrors)].join('\n  ')); process.exit(1); }
let stale = 0;
for (const [f, body] of Object.entries(files)) {
  const cur = fs.existsSync(f) ? fs.readFileSync(f, 'utf8') : null;
  if (cur === body) continue;
  stale++;
  if (!CHECK) { fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, body); }
}
console.log(`stubs: ${stubs.length} not-yet-graded pages, ${stubs.filter(s => s.official_site).length} with a verified official site, ${stubs.reduce((n, s) => n + s.directory_church_count, 0)} churches`);
for (const d of out) {
  const g = Object.entries(d.scores).map(([k, s]) => `${k}=${s.grade}`).join(' ');
  console.log(`${d.id}: overall=${d.overall_grade} context=${d.context_grade} governance=${d.governance.strength} ledger=${d.ledger.length}/${d.ledger.filter(l => l.validated).length} valid churches=${d.directory_church_count} verified_congregations=${d.verified_congregations.length}\n  ${g}`);
}
if (CHECK) { console.log(stale ? `STALE: ${stale} generated file(s) differ` : 'denomination pages up to date'); process.exit(stale ? 1 : 0); }
console.log(`wrote ${stale} file(s)`);
