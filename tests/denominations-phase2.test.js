#!/usr/bin/env node
'use strict';
// denominations-phase2.test.js — SBC, BGAV, SBCV, UMC, GMC (CCW-1119-DIR2 Phase 2).
// Official-source-only ledgers, every quote verbatim in its snapshot and
// traceable to a local-model proposal, rule-based grades, explicit governance,
// church pages link only to pages that exist, and rules never fire on
// look-alike wording.
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const REPO = path.join(__dirname, '..');
const D = require(path.join(REPO, 'scripts/lib/denominations.js'));

const OFFICIAL = {
  sbc: /^https:\/\/(bfm\.sbc\.net|www\.sbc\.net)\//,
  bgav: /^https:\/\/(www\.bgav\.org\/|cdn\.prod\.website-files\.com\/5fd7b0e7b3bae9a027784605\/)/, // bgav.org's own Webflow asset host
  sbcv: /^https:\/\/www\.sbcv\.org\//,
  umc: /^https:\/\/www\.umc\.org\//,
  gmc: /^https:\/\/(www\.globalmethodist\.org\/|irp\.cdn-website\.com\/1876eae9\/)/, // globalmethodist.org's own file host
};
const WANT = {
  sbc: { gov: 'autonomous', ctx: 'green', s: { scripture: 'green', christology: 'green', soteriology: 'green', gender: 'green', leadership: 'green', cultural: 'green', denominational: 'green', mission: 'green', preaching: 'unknown', mens_discipleship: 'unknown' } },
  bgav: { gov: 'autonomous', ctx: 'yellow', s: { scripture: 'unknown', christology: 'unknown', soteriology: 'unknown', gender: 'yellow', leadership: 'yellow', cultural: 'green', denominational: 'green', mission: 'unknown' } },
  sbcv: { gov: 'autonomous', ctx: 'green', s: { scripture: 'green', mission: 'green', gender: 'unknown', cultural: 'unknown', christology: 'unknown' } },
  umc: { gov: 'binding', ctx: 'red', s: { scripture: 'unknown', christology: 'green', soteriology: 'green', gender: 'red', leadership: 'red', cultural: 'red', denominational: 'red', mission: 'green' } },
  gmc: { gov: 'binding', ctx: 'red', s: { scripture: 'unknown', christology: 'green', soteriology: 'green', gender: 'red', leadership: 'red', cultural: 'green', denominational: 'green', mission: 'green' } },
};

const denoms = D.loadDenominations();
const idx = D.aliasIndex(denoms); // throws on any alias collision
const nrm = s => D.nrm(s);
for (const [id, want] of Object.entries(WANT)) {
  const d = denoms.find(x => x.id === id);
  assert.ok(d, `${id} missing`);
  const ledger = D.buildLedger(d);
  assert.ok(ledger.length >= 5, `${id}: thin ledger`);
  const props = JSON.parse(fs.readFileSync(path.join(REPO, 'data/denominations/proposals', `${id}.json`), 'utf8'));
  assert.ok(/127\.0\.0\.1:1234/.test(props.endpoint), `${id}: proposals must come from local LM Studio`);
  for (const l of ledger) {
    assert.ok(l.validated, `${id} ${l.id}: ${l.error}`);
    assert.ok(OFFICIAL[id].test(l.url), `${id} ${l.id}: ${l.url} is not an official ${id} source`);
    assert.ok(l.model && l.retrieved_at && l.source_sha256 && l.confidence === 1, `${id} ${l.id}: provenance`);
    const ev = d.evidence.find(e => e.id === l.id);
    assert.ok(props.proposals.some(p => p.validated && p.source === ev.source && nrm(p.quote).includes(nrm(ev.quote))),
      `${id} ${l.id}: not a verbatim-valid local-model proposal`);
  }
  const sc = D.scoreDenomination(d, ledger);
  for (const [k, v] of Object.entries(want.s)) assert.strictEqual(sc.scores[k].grade, v, `${id} ${k}`);
  for (const s of Object.values(sc.scores)) if (s.grade !== 'unknown' && !(s.rule && s.rule.id === 'D-DEN-1')) assert.ok(s.rule && s.evidence.length, `${id}: graded without rule+evidence`);
  assert.strictEqual(sc.governance.strength, want.gov, `${id} governance`);
  assert.ok(sc.governance.evidence.length, `${id}: governance without a quote`);
  assert.strictEqual(sc.context_grade, want.ctx, `${id} context`);
}

// Separate bodies stay separate.
assert.strictEqual(D.normalizeDenomination('Southern Baptist Convention (SBC)', idx), 'sbc');
assert.strictEqual(D.normalizeDenomination('Southern Baptist Conservatives of Virginia (SBCV)', idx), 'sbcv');
assert.strictEqual(D.normalizeDenomination('Baptist General Association of Virginia (BGAV)', idx), 'bgav');
assert.strictEqual(D.normalizeDenomination('United Methodist Church (Virginia Conference)', idx), 'umc');
assert.strictEqual(D.normalizeDenomination('Global Methodist Church (GMC)', idx), 'gmc');
for (const l of ['Baptist', 'Independent Baptist', 'Methodist', 'Free Methodist Church', 'Non-Denominational'])
  assert.strictEqual(D.normalizeDenomination(l, idx), null, `${l} must not map to a body`);

// Rules do not fire on look-alike wording.
const q = (quote, cat) => [{ id: 'x', quote, supports: [cat], validated: true }];
const grade = (quote, cat, id = 'zz') => D.scoreDenomination({ id }, q(quote, cat)).scores[cat].grade;
assert.strictEqual(grade('The office of deacon is open to both men and women.', 'gender'), 'unknown');
assert.strictEqual(grade('Marriage is a covenant between one man and one woman.', 'cultural'), 'green');
assert.strictEqual(grade('Marriage brings two people of faith into union.', 'cultural'), 'unknown');
assert.strictEqual(grade('We are saved by grace through faith.', 'soteriology'), 'unknown');
assert.strictEqual(D.scoreDenomination({ id: 'zz' }, q('Our churches are autonomous.', 'governance')).governance.strength, 'autonomous');
assert.strictEqual(D.scoreDenomination({ id: 'zz' }, q('The bishop decides.', 'governance')).governance.strength, null);

// Pages: built, linked from the index, and church pages link only to pages that exist.
const links = JSON.parse(fs.readFileSync(path.join(REPO, 'docs/data/denominations/church-links.json'), 'utf8')).links;
const idxHtml = fs.readFileSync(path.join(REPO, 'docs/denominations/index.html'), 'utf8');
for (const id of Object.keys(WANT)) {
  assert.ok(fs.existsSync(path.join(REPO, `docs/denominations/${id}.html`)), `${id} page missing`);
  assert.ok(idxHtml.includes(`href="/denominations/${id}.html"`), `${id} not on index`);
  assert.ok(Object.values(links).filter(v => v === id).length > 100, `${id}: too few church links`);
}
const pageIds = new Set(fs.readdirSync(path.join(REPO, 'docs/denominations')).filter(f => f.endsWith('.html') && f !== 'index.html').map(f => f.slice(0, -5)));
for (const v of new Set(Object.values(links))) assert.ok(pageIds.has(v), `church-links points at missing page ${v}`);
const sample = Object.entries(links).filter(([, v]) => v === 'umc').slice(0, 25);
for (const [cid] of sample) {
  const h = fs.readFileSync(path.join(REPO, `docs/churches/${cid}.html`), 'utf8');
  assert.ok(h.includes('href="/denominations/umc.html"') && h.includes('context only'), `${cid} lacks UMC context link`);
}
console.log('denominations-phase2.test.js: all assertions passed');
