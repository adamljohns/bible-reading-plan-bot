#!/usr/bin/env node
'use strict';
// denomination-aliases.test.js — Phase 1 alias map (CCW-1119-DIR2):
// complete coverage of churches.json labels, generic labels never graded,
// separate bodies kept separate, hedged/multi labels left unmapped, sub-fields,
// agreement with the EFCA page, no new pages, rules independent of the model.
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const cp = require('child_process');
const REPO = path.join(__dirname, '..');
const D = require(path.join(REPO, 'scripts/lib/denominations.js'));
const R = require(path.join(REPO, 'scripts/lib/denomination-alias-rules.js'));

// 1. The committed map is exactly what the rules produce today.
cp.execFileSync('node', [path.join(REPO, 'scripts/build-denomination-alias-map.js'), '--check'], { stdio: 'pipe' });

const map = D.loadAliasMap();
const raw = JSON.parse(fs.readFileSync(path.join(REPO, 'docs/data/churches.json'), 'utf8'));
const churches = Array.isArray(raw) ? raw : raw.churches;
const cls = l => D.classifyDenomination(l, map);

// 2. Every church's label is classified; counts add up.
const labels = new Set(churches.map(c => c.denomination == null ? '' : String(c.denomination)));
for (const l of labels) assert.ok(map.exact.has(l), `label missing from alias map: ${JSON.stringify(l)}`);
assert.strictEqual(map.doc.labels.length, labels.size);
assert.strictEqual(map.doc.labels.reduce((n, l) => n + l.count, 0), churches.length);
for (const l of map.doc.labels) assert.ok(['body', 'generic', 'unresolved'].includes(l.status), l.label);

// 3. Generic / placeholder labels never map to a body and never get a graded page.
for (const l of ['Baptist', 'Non-Denominational', 'Unverified', 'verify', 'Unknown', '', 'Reformed Evangelical', 'Reformed Baptist',
  'Independent Baptist', 'Presbyterian', 'Lutheran', 'Methodist', 'Reformed', 'Independent', 'Bible Church', 'Anglican', 'Episcopal', 'IFB'])
  assert.strictEqual(cls(l).status, 'generic', `${JSON.stringify(l)} must be generic`);
for (const g of map.doc.generic) assert.strictEqual(g.graded_page, false, g.family);

// 4. Separate bodies stay separate; sub-fields carry conference/presbytery/diocese.
const body = (l, id, extra = {}) => { const r = cls(l); assert.strictEqual(r.status, 'body', `${l}: ${JSON.stringify(r)}`); assert.strictEqual(r.id, id, l); for (const [k, v] of Object.entries(extra)) assert.strictEqual(r[k], v, `${l} ${k}`); };
body('Southern Baptist Convention (SBC)', 'sbc');
body('Southern Baptist Convention (SBCV)', 'sbcv');
body('Baptist General Association of Virginia (BGAV)', 'bgav');
body('United Methodist Church (Virginia Conference)', 'umc', { conference: 'Virginia Annual Conference' });
body('United Methodist Church (BWC)', 'umc', { conference: 'Baltimore-Washington Conference' });
body('GMC', 'gmc');
body('African Methodist Episcopal (AME)', 'ame');
body('African Methodist Episcopal Zion (AME Zion)', 'amez');
body('PCA', 'pca');
body('Presbyterian Church in America (PCA) — Korean Southwest Presbytery', 'pca', { presbytery: 'Korean Southwest Presbytery' });
body('Cumberland Presbyterian Church in America', 'cpca');
body('ECO: A Covenant Order of Evangelical Presbyterians', 'eco');
body('Orthodox Presbyterian Church (OPC) — Presbytery of the Southeast', 'opc', { presbytery: 'Presbytery of the Southeast' });
body('ARP', 'arp');
body('Anglican Church in North America (ACNA) — Diocese of the Mid-Atlantic', 'acna', { diocese: 'Diocese of the Mid-Atlantic' });
body('The Episcopal Church (Diocese of Virginia)', 'tec', { diocese: 'Diocese of Virginia' });
body('Reformed Episcopal Church', 'rec');
body('ABCUSA (American Baptist Churches USA, NOT SBC)', 'abcusa');
body('Free Will Baptist (NOT SBC)', 'nafwb');
body('Fellowship of Grace Brethren Churches (FGBC)', 'charis');
body('Charis Fellowship', 'charis');

// 5. Hedged, multi-affiliated and conflicting labels stay unmapped.
for (const l of ['SBC (verify)', 'Southern Baptist (SBC) — disfellowshipped 2023', 'Formerly UMC / now independent Glide Foundation',
  'SBC + BGAV (dual-aligned)', 'Southern Baptist (BGAV)', 'BGAV/CBF', 'NBC/PNBC', 'Federated UCC/Presbyterian',
  'Non-Denominational (Reformed, dispensational-leaning; EFCA-tagged)', 'Presbyterian (PCA) — unverified',
  'Reformed Episcopal Church (REC) / Anglican Church in North America (ACNA)', 'Non-Denominational (AG roots)', 'Independent Methodist (post-UMC, NOT GMC-affiliated)'])
  assert.strictEqual(cls(l).status, 'unresolved', `${l} must stay unresolved: ${JSON.stringify(cls(l))}`);
// Lower-case negation names no body (caught by the local model's review pass).
assert.notStrictEqual(cls('Baptist (not SBC -- historically Black Baptist)').id, 'sbc');
assert.strictEqual(cls('Some label nobody has used').status, 'unresolved');

// 6. One alias, one body (the page builder's own normalization).
D.aliasIndex(map.doc.bodies.map(b => ({ id: b.id, aliases: b.aliases })));
assert.strictEqual(new Set(map.doc.bodies.map(b => b.id)).size, map.doc.bodies.length);
for (const b of map.doc.bodies) assert.ok(/^[a-z0-9]+(-[a-z0-9]+)*$/.test(b.id) && b.name && b.short_name && b.aliases.length, b.id);

// 7. The map agrees with every existing page: same churches, no new pages.
const pageDenoms = D.loadDenominations();
const pageIdx = D.aliasIndex(pageDenoms);
for (const d of pageDenoms) {
  const viaPage = churches.filter(c => D.normalizeDenomination(c.denomination, pageIdx) === d.id).length;
  const b = map.bodies.get(d.id);
  assert.ok(b, `${d.id} missing from alias map`);
  assert.strictEqual(b.church_count, viaPage, `${d.id}: alias map ${b.church_count} vs page links ${viaPage}`);
}
const pageIds = new Set(pageDenoms.map(d => d.id));
for (const b of map.doc.bodies) assert.strictEqual(b.graded_page, pageIds.has(b.id), `${b.id} graded_page`);

// 8. Phase 2 bodies are all present and ranked by count.
const cov = JSON.parse(fs.readFileSync(path.join(REPO, 'data/denominations/aliases/alias-coverage.json'), 'utf8'));
for (const id of ['sbc', 'bgav', 'sbcv', 'umc', 'gmc', 'ame', 'pca', 'opc', 'arp', 'acna'])
  assert.ok(map.bodies.get(id) && map.bodies.get(id).church_count > 0, `${id} has no churches`);
for (let i = 1; i < cov.ranking.length; i++) assert.ok(cov.ranking[i - 1].church_count >= cov.ranking[i].church_count);
const c = cov.counts;
assert.strictEqual(c.mapped.labels + c.generic.labels + c.unresolved.labels, c.labels);
assert.strictEqual(c.mapped.churches + c.generic.churches + c.unresolved.churches, c.churches);
assert.strictEqual(cov.unresolved.length, c.unresolved.labels);

// 9. The rules never read the local model's proposals.
for (const f of ['scripts/lib/denomination-alias-rules.js', 'scripts/lib/denominations.js'])
  assert.ok(!/(readFileSync|require|existsSync)\([^)]*proposals/.test(fs.readFileSync(path.join(REPO, f), 'utf8')), `${f} must not read model proposals`);
assert.ok(typeof R.classifyLabel === 'function');

console.log(`denomination-aliases: OK (${c.labels} labels: ${c.mapped.labels} mapped / ${c.generic.labels} generic / ${c.unresolved.labels} unresolved; ${c.bodies} bodies)`);
