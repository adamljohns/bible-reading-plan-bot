#!/usr/bin/env node
'use strict';
// denominations-links.test.js — Phase 3 (CCW-1119-DIR2): the denomination is
// clickable wherever it renders (church pages, directory cards, search results,
// filters, map popups) and only when a graded page exists; generic labels stay
// plain text; denomination pages list their churches and every listed church
// links back.
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const crypto = require('crypto');
const REPO = path.join(__dirname, '..');
const DOCS = path.join(REPO, 'docs');
const D = require(path.join(REPO, 'scripts/lib/denominations.js'));

// 1. The generated client helper.
const js = fs.readFileSync(path.join(DOCS, 'assets/js/denomination-links.js'), 'utf8');
const win = {};
vm.runInNewContext(js, { window: win });
const DL = win.DenomLinks;
assert.ok(DL && typeof DL.lookup === 'function' && typeof DL.html === 'function');
const amap = D.loadAliasMap();
// Every mapped body has a page now: graded, or a "Not yet graded" stub (CCW-1119-DIR3).
const gradedPages = new Set(amap.doc.bodies.map(b => b.id));
for (const l of amap.doc.labels) {
  const hit = DL.lookup(l.label);
  if (l.status === 'body' && gradedPages.has(l.id)) {
    assert.ok(hit && hit.id === l.id, `label "${l.label}" should link to ${l.id}`);
    assert.ok(fs.existsSync(path.join(DOCS, hit.page.replace(/^\//, ''))), `${hit.page} missing`);
    assert.ok(DL.html(l.label).startsWith(`<a class="denom-link" href="${hit.page}"`), `"${l.label}" not rendered as a link`);
  } else {
    assert.strictEqual(hit, null, `label "${l.label}" (${l.status}${l.id ? ' ' + l.id : ''}) must stay plain text`);
    assert.ok(!DL.html(l.label).includes('<a'), `"${l.label}" must not render a link`);
  }
}
for (const g of ['Baptist', 'Methodist', 'Non-Denominational', 'Independent Baptist', '', null, undefined])
  assert.strictEqual(DL.lookup(g), null, `${g} must not link`);
assert.strictEqual(DL.html('<img src=x onerror=1>'), '&lt;img src=x onerror=1&gt;', 'labels are escaped');
assert.ok(DL.html('United Methodist Church (Virginia Conference)').includes('event.stopPropagation()'), 'card link must not toggle the card');
// A mapped body without a grade links to its stub page (CCW-1119-DIR3).
assert.strictEqual((DL.lookup('Free Methodist Church') || {}).id, 'fmc');
// Loose match uses the same key as the alias map (case/spacing/punctuation).
assert.strictEqual((DL.lookup('united methodist church  (virginia conference)') || {}).id, 'umc');

// 2. Client and church pages agree with church-links.json for every church.
const churches = JSON.parse(fs.readFileSync(path.join(DOCS, 'data/churches.json'), 'utf8'));
const list = Array.isArray(churches) ? churches : churches.churches;
const links = JSON.parse(fs.readFileSync(path.join(DOCS, 'data/denominations/church-links.json'), 'utf8')).links;
let linked = 0;
for (const c of list) {
  const hit = DL.lookup(c.denomination, c.id);
  assert.strictEqual(hit ? hit.id : undefined, links[c.id], `${c.id} "${c.denomination}": client and church page disagree`);
  if (hit) linked++;
}
assert.ok(linked > 5000, `only ${linked} churches link`);

// 2b. Refine-filter families: link only when every church with that value links
// to the same body, and the value names that body; generic families stay plain.
const fam = new Map();
for (const c of list) { const v = c.denomination_family || c.denomination; if (!v) continue; const id = links[c.id] || null; fam.set(v, fam.has(v) && fam.get(v) !== id ? null : id); }
for (const [v, id] of fam) {
  const hit = DL.lookupFamily(v);
  if (hit) {
    assert.strictEqual(hit.id, id, `family "${v}" links to ${hit.id} but its churches map to ${id}`);
    assert.notStrictEqual(D.classifyDenomination(v, amap).status, 'generic', `generic family "${v}" must stay plain`);
  }
}
for (const g of ['Baptist', 'Methodist', 'Mainline Protestant / Methodist', 'Wesleyan / Methodist', 'Non-Denominational'])
  assert.strictEqual(DL.lookupFamily(g), null, `family "${g}" must stay plain`);
assert.strictEqual((DL.lookupFamily('Baptist (SBC)') || {}).id, 'sbc');
// Its only two churches are the excluded former-UMC congregations (link exclusions), so it stays plain.
assert.strictEqual(DL.lookupFamily('United Methodist (UMC)'), null);
assert.ok(fs.readFileSync(path.join(DOCS, 'churches.html'), 'utf8').includes('updateDenomFilterLink(filters.subdenom, true)'), 'Refine filter uses family lookup');

// 3. Consumer pages load the helper at its current content version and use it.
const ver = crypto.createHash('sha256').update(js).digest('hex').slice(0, 10);
const uses = {
  'churches.html': ['denomHtml(church.denomination, church.id)', 'updateDenomFilterLink(filters.subdenom, true)', 'id="denom-filter-link"'],
  'churches-fxbg.html': ['denomHtml(church.denomination, church.id)', 'updateDenomFilterLink(filters.denomination)', 'id="denom-filter-link"'],
  'churches-virginia.html': ['denomHtml(church.denomination, church.id)', 'updateDenomFilterLink(filters.denomination)', 'id="denom-filter-link"'],
  'churches-dc.html': ['denomHtml(church.denomination, church.id)', 'updateDenomFilterLink(filters.denomination)', 'id="denom-filter-link"'],
  'directory-map.html': ['DenomLinks.htmlFamily(p.d, p.id)', 'DenomLinks.lookupFamily(denom)', 'id="denom-filter-link"'],
};
for (const [f, needles] of Object.entries(uses)) {
  const h = fs.readFileSync(path.join(DOCS, f), 'utf8');
  assert.ok(h.includes(`<script src="/assets/js/denomination-links.js?v=${ver}"></script>`), `${f}: helper missing or stale ?v=`);
  assert.ok(h.indexOf('denomination-links.js') < h.indexOf('</head>'), `${f}: helper must load before the page scripts`);
  for (const n of needles) assert.ok(h.includes(n), `${f}: missing ${n}`);
  assert.ok(!h.includes("${esc(church.denomination) || 'Independent'}"), `${f}: plain denomination left in a card`);
}

// The map page is generated: its template must keep the helper and the links.
const mapGen = fs.readFileSync(path.join(REPO, 'scripts/build-directory-map.js'), 'utf8');
for (const n of ['denomination-links.js?v=${DENOM_JS_VER}', 'DenomLinks.htmlFamily(p.d, p.id)', 'DenomLinks.lookupFamily(denom)']) assert.ok(mapGen.includes(n), `build-directory-map.js template lost ${n}`);
assert.ok(DL.htmlFamily('Baptist (SBC)').startsWith('<a class="denom-link" href="/denominations/sbc.html"'));
assert.strictEqual(DL.htmlFamily('Baptist'), 'Baptist');

// 4. Church pages: the label links when (and only when) a graded page exists.
const byBody = {};
for (const [cid, id] of Object.entries(links)) (byBody[id] = byBody[id] || []).push(cid);
for (const [id, cids] of Object.entries(byBody)) for (const cid of cids.slice(0, 15)) {
  const h = fs.readFileSync(path.join(DOCS, `churches/${cid}.html`), 'utf8');
  assert.ok(new RegExp(`<span class="fact-value"><a class="denom-link" href="/denominations/${id}\\.html"`).test(h), `${cid}: denomination label not linked`);
}
const generic = list.filter(c => c.denomination === 'Baptist' && fs.existsSync(path.join(DOCS, `churches/${c.id}.html`))).slice(0, 15);
assert.ok(generic.length > 5, 'fixture: generic Baptist church pages');
for (const c of generic) {
  const h = fs.readFileSync(path.join(DOCS, `churches/${c.id}.html`), 'utf8');
  assert.ok(!h.includes('class="denom-link"') && !h.includes('href="/denominations/'), `${c.id}: generic label must stay plain`);
}

// 5. Two-way: each denomination page lists all its churches; each listed church links back.
const idx = fs.readFileSync(path.join(DOCS, 'denominations/index.html'), 'utf8');
for (const [id, cids] of Object.entries(byBody)) {
  const page = fs.readFileSync(path.join(DOCS, `denominations/${id}.html`), 'utf8');
  assert.ok(page.includes('id="churches"'), `${id}: no churches section`);
  assert.ok(idx.includes(`href="/denominations/${id}.html#churches"`), `index: ${id} count not linked to its church list`);
  const listed = new Set([...page.matchAll(/href="\/churches\/([^"]+)\.html"/g)].map(m => m[1]));
  for (const cid of cids) {
    assert.ok(listed.has(cid), `${id} page does not list ${cid}`);
    const h = fs.readFileSync(path.join(DOCS, `churches/${cid}.html`), 'utf8');
    assert.ok(h.includes(`href="/denominations/${id}.html"`), `${cid} does not link back to ${id}`);
  }
  for (const cid of listed) assert.strictEqual(links[cid], id, `${id} page lists ${cid}, which is not mapped to ${id}`);
}

// 6. Link check: every internal href on the denomination pages resolves.
let n = 0;
for (const f of fs.readdirSync(path.join(DOCS, 'denominations')).filter(f => f.endsWith('.html'))) {
  const h = fs.readFileSync(path.join(DOCS, 'denominations', f), 'utf8');
  for (const m of h.matchAll(/href="(\/[^"#?]*)/g)) {
    n++;
    const p = path.join(DOCS, decodeURIComponent(m[1]));
    assert.ok(fs.existsSync(p.endsWith('/') ? path.join(p, 'index.html') : p) || fs.existsSync(path.join(p, 'index.html')), `${f}: broken link ${m[1]}`);
  }
}
assert.ok(n > 5000, `link check saw only ${n} hrefs`);
// 7. Approved exclusions (data/crosslinks/denomination-link-exclusions.json):
// former-UMC churches never link to umc.html anywhere (CCW-1119-DIR2 Phase 4 QA).
const EXCL = JSON.parse(fs.readFileSync(path.join(REPO, 'data/crosslinks/denomination-link-exclusions.json'), 'utf8')).exclusions;
for (const must of ['highland-park-united-methodist-dallas-tx', 'first-united-methodist-midland-tx'])
  assert.ok(EXCL.some(x => x.church_id === must && x.evidence.length), `${must} missing from link exclusions`);
for (const x of EXCL) {
  const c = list.find(r => r.id === x.church_id);
  assert.ok(c, `exclusion ${x.church_id} not in churches.json`);
  assert.strictEqual(links[x.church_id], undefined, `${x.church_id} still in church-links.json`);
  assert.strictEqual(DL.lookup(c.denomination, c.id), null, `${x.church_id}: client card still links`);
  assert.ok(!DL.html(c.denomination, '', c.id).includes('<a'), `${x.church_id}: card renders a link`);
  assert.ok(!DL.htmlFamily(c.denomination_family || c.denomination, c.id).includes('<a'), `${x.church_id}: map popup renders a link`);
  const page = path.join(DOCS, `churches/${x.church_id}.html`);
  if (fs.existsSync(page)) assert.ok(!fs.readFileSync(page, 'utf8').includes(`/denominations/${x.denomination}.html`), `${x.church_id} page still links ${x.denomination}.html`);
  assert.ok(!fs.readFileSync(path.join(DOCS, `denominations/${x.denomination}.html`), 'utf8').includes(`/churches/${x.church_id}.html`), `${x.denomination} page still lists ${x.church_id}`);
}
const pol = fs.readFileSync(path.join(DOCS, 'directory-politicians.html'), 'utf8');
for (const addr of ['3300 Mockingbird Lane, Dallas', '300 N Main Street, Midland'])
  for (const line of pol.split('\n').filter(l => l.includes(addr))) assert.ok(!line.includes('umc.html'), `politicians: ${addr} label still links umc.html`);
console.log(`denominations-links.test.js: all assertions passed (${linked} churches linked, ${n} denomination-page hrefs resolve)`);
