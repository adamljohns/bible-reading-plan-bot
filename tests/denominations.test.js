#!/usr/bin/env node
'use strict';
// denominations.test.js — schema, alias normalization, quote-in-source
// validation, rule scoring (unknown without a quote), governance, page links.
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const cp = require('child_process');
const REPO = path.join(__dirname, '..');
const D = require(path.join(REPO, 'scripts/lib/denominations.js'));

const denoms = D.loadDenominations();
const idx = D.aliasIndex(denoms);
const efca = denoms.find(d => d.id === 'efca');

// 1. Alias normalization: every stored EFCA label maps; look-alikes do not.
for (const l of ['EFCA', 'Evangelical Free Church of America (EFCA)', 'evangelical free church of america', 'Independent Evangelical Free', 'Evangelical Free (independent Free Church)', 'E.F.C.A.'])
  assert.strictEqual(D.normalizeDenomination(l, idx), 'efca', `${l} should map to efca`);
for (const l of ['Non-Denominational (Reformed, dispensational-leaning; EFCA-tagged)', 'Evangelical Covenant Church', 'Free Will Baptist', 'Evangelical Lutheran Church in America', '', null])
  // Look-alikes must not map to EFCA (other bodies may get their own pages via the grind).
  assert.notStrictEqual(D.normalizeDenomination(l, idx), 'efca', `${l} must NOT map to efca`);
// Alias collisions are a hard error.
assert.throws(() => D.aliasIndex([{ id: 'a', aliases: ['X'] }, { id: 'b', aliases: ['x'] }]), /maps to both/);

// 2. Every EFCA ledger row validates against its official snapshot, and every
//    source is efca.org (official-only policy).
const ledger = D.buildLedger(efca);
assert.ok(ledger.length >= 10);
for (const l of ledger) {
  assert.ok(l.validated, `${l.id}: ${l.error}`);
  assert.ok(/^https:\/\/www\.efca\.org\//.test(l.url), `${l.id} is not an official efca.org source`);
  assert.ok(l.retrieved_at && l.source_sha256 && l.extractor && l.model === null && l.confidence === 1);
}

// 3. A tampered quote fails validation and its category drops to unknown.
{
  const bad = JSON.parse(JSON.stringify(efca));
  bad.evidence = bad.evidence.map(e => e.id === 'efca-sof-christ' ? { ...e, quote: 'We believe that Jesus Christ is fully God and fully man and also an angel.' } : e);
  const bl = D.buildLedger(bad);
  assert.strictEqual(bl.find(l => l.id === 'efca-sof-christ').validated, false);
  assert.strictEqual(D.scoreDenomination(bad, bl).scores.christology.grade, 'unknown');
}
// A quote with no snapshot / wrong URL fails too.
{
  const bad = JSON.parse(JSON.stringify(efca));
  bad.evidence = [{ ...bad.evidence[0], url: 'https://example.com/sof' }];
  assert.strictEqual(D.buildLedger(bad)[0].validated, false);
}

// 4. Scores: rule-backed grades, unknown where no official quote exists.
const sc = D.scoreDenomination(efca, ledger);
const want = { scripture: 'green', christology: 'green', soteriology: 'green', gender: 'green', leadership: 'yellow',
  cultural: 'green', mission: 'green', denominational: 'green', preaching: 'unknown', mens_discipleship: 'unknown' };
for (const [k, v] of Object.entries(want)) assert.strictEqual(sc.scores[k].grade, v, `${k}`);
for (const s of Object.values(sc.scores)) if (s.grade !== 'unknown') assert.ok(s.rule && s.evidence.length, 'graded without rule+evidence');
assert.strictEqual(sc.governance.strength, 'mixed');
assert.ok(D.GOVERNANCE.includes(sc.governance.strength));
// Leadership nuance: without the "local church decides" quote, leadership is not YELLOW.
{
  const l2 = ledger.filter(l => !['efca-tp-no-local-policy', 'efca-tp-local-decides'].includes(l.id));
  assert.strictEqual(D.scoreDenomination(efca, l2).scores.leadership.grade, 'unknown');
}
// Affirming-list rule fires on id alone, and a women-ordaining body is RED on gender.
{
  const fake = { id: 'elca', evidence: [] };
  assert.strictEqual(D.scoreDenomination(fake, []).scores.denominational.grade, 'red');
  const q = [{ id: 'x', quote: 'The church ordains women and men to the ministry of Word and Sacrament.', supports: ['gender'], validated: true }];
  assert.strictEqual(D.scoreDenomination({ id: 'zz' }, q).scores.gender.grade, 'red');
}

// 5. Build is clean and generated files are current.
const r = cp.spawnSync(process.execPath, [path.join(REPO, 'scripts/build-denomination-pages.js'), '--check'], { encoding: 'utf8' });
assert.strictEqual(r.status, 0, r.stdout + r.stderr);

// 6. Pages: index links detail; detail page states context-only + the nuance;
//    every internal href resolves to a file under docs/.
const idxHtml = fs.readFileSync(path.join(REPO, 'docs/denominations/index.html'), 'utf8');
const det = fs.readFileSync(path.join(REPO, 'docs/denominations/efca.html'), 'utf8');
assert.ok(idxHtml.includes('href="/denominations/efca.html"'));
assert.ok(/Context only/.test(det) && /local evidence wins/.test(det));
assert.ok(det.includes('Elders are a local decision') && det.includes('Ordination is for men'));
for (const html of [idxHtml, det]) {
  for (const m of html.matchAll(/href="(\/[^"#?]*)"/g)) {
    let p = m[1]; if (p.endsWith('/')) p += 'index.html';
    assert.ok(fs.existsSync(path.join(REPO, 'docs', p)), `broken internal link ${m[1]}`);
  }
}

// 7. Church links: Grace Fellowship (EFCA, verified on its own site) links;
//    Grace Church of Fredericksburg (Independent, no EFCA evidence) does not.
const links = JSON.parse(fs.readFileSync(path.join(REPO, 'docs/data/denominations/church-links.json'), 'utf8')).links;
assert.strictEqual(links['grace-fellowship-efca-fredericksburg'], 'efca');
assert.strictEqual(links['grace-church-fredericksburg'], undefined);
const gf = fs.readFileSync(path.join(REPO, 'docs/churches/grace-fellowship-efca-fredericksburg.html'), 'utf8');
assert.ok(gf.includes('href="/denominations/efca.html"') && gf.includes('context only'));
assert.ok(!fs.readFileSync(path.join(REPO, 'docs/churches/grace-church-fredericksburg.html'), 'utf8').includes('/denominations/'));
// The denomination link never changes a church's stored rating.
const churches = JSON.parse(fs.readFileSync(path.join(REPO, 'docs/data/churches.json'), 'utf8'));
const arr = Array.isArray(churches) ? churches : churches.churches;
assert.ok(arr.every(c => !('denomination_grade' in c)), 'denomination grade must not be written into church records');
console.log('denominations: all assertions passed');
