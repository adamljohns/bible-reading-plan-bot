#!/usr/bin/env node
'use strict';
// denominations-phaseB.test.js — CCW-1119-DIR3.
//  1. Limited-evidence rule: < 5 of 10 categories graded => overall "limited" (grey) + caveat.
//  2. "Why" line names the categories that set the grade (GMC: gender + leadership only).
//  3. Stub pages: every mapped ungraded body has a page with the banner, no grade, no quotes,
//     an official-site link only when verified 200 + same domain, and links to its churches.
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const REPO = path.join(__dirname, '..');
const DOCS = path.join(REPO, 'docs');
const D = require(path.join(REPO, 'scripts/lib/denominations.js'));

// 1. Unit: the rule itself.
const mk = grades => Object.fromEntries(D.CATEGORIES.map((c, i) => [c, { grade: grades[i] || 'unknown' }]));
let o = D.overallGrade(mk(['green', 'green']));
assert.deepStrictEqual([o.overall_grade, o.limited_evidence, o.graded_count], ['limited', true, 2]);
o = D.overallGrade(mk(['green', 'green', 'red', 'green']));
assert.strictEqual(o.overall_grade, 'limited', '4 graded is still limited');
o = D.overallGrade(mk(['green', 'green', 'red', 'green', 'yellow']));
assert.deepStrictEqual([o.overall_grade, o.limited_evidence], ['red', false], '5 graded gets a color');
assert.deepStrictEqual(o.because, ['gender']);
o = D.overallGrade(mk([]));
assert.strictEqual(o.overall_grade, 'limited');

// 1b. Data: SBCV shows Limited evidence, not green.
const idx = JSON.parse(fs.readFileSync(path.join(DOCS, 'data/denominations/index.json'), 'utf8')).denominations;
const by = Object.fromEntries(idx.map(d => [d.id, d]));
assert.strictEqual(by.sbcv.overall_grade, 'limited');
const sbcv = fs.readFileSync(path.join(DOCS, 'denominations/sbcv.html'), 'utf8');
assert.ok(sbcv.includes('<span class="pill g-limited">Limited evidence</span>'), 'sbcv pill');
assert.ok(/Only \d of 10 categories have an official quote\. This is not a full assessment\./.test(sbcv), 'sbcv caveat');
assert.ok(!/Overall grade <span class="pill g-green">/.test(sbcv), 'sbcv must not show an overall green');

// 2. Why line. GMC is red because of gender + leadership only.
assert.deepStrictEqual(by.gmc.because, ['gender', 'leadership']);
const gmc = fs.readFileSync(path.join(DOCS, 'denominations/gmc.html'), 'utf8');
assert.ok(gmc.includes('Red because of: Gender &amp; Ordination; Leadership &amp; Elders.'), 'gmc why line');
const index = fs.readFileSync(path.join(DOCS, 'denominations/index.html'), 'utf8');
for (const d of idx.filter(x => !x.stub)) {
  const page = fs.readFileSync(path.join(DOCS, d.page.replace(/^\//, '')), 'utf8');
  assert.ok(/class="why"/.test(page), `${d.id}: no why line`);
  if (!d.limited_evidence) assert.ok(index.includes(`>${d.overall_grade.charAt(0).toUpperCase() + d.overall_grade.slice(1)} because of: `), `${d.id}: index row has no why line`);
}
assert.ok(index.includes('Red because of: Gender &amp; Ordination; Leadership &amp; Elders.'), 'index gmc why');

// 3. Stubs.
const amap = D.loadAliasMap();
const graded = new Set(D.loadDenominations().map(d => d.id));
const sites = JSON.parse(fs.readFileSync(path.join(REPO, 'data/denominations/sites/official-sites.json'), 'utf8'));
const links = JSON.parse(fs.readFileSync(path.join(DOCS, 'data/denominations/church-links.json'), 'utf8')).links;
let n = 0;
for (const b of amap.doc.bodies.filter(x => !graded.has(x.id))) {
  n++;
  const f = path.join(DOCS, 'denominations', `${b.id}.html`);
  assert.ok(fs.existsSync(f), `${b.id}: stub missing`);
  const h = fs.readFileSync(f, 'utf8');
  assert.ok(h.includes('Not yet graded. Official statements are being reviewed.'), `${b.id}: banner`);
  assert.ok(!/class="pill g-(green|yellow|red|black|limited)"/.test(h), `${b.id}: stub shows a grade`);
  assert.ok(!h.includes('<blockquote>'), `${b.id}: stub shows quotes`);
  const v = sites.verified[b.id];
  const ok = !!(v && v.ok && v.http_status === 200 && v.url === sites.proposed[b.id]);
  if (ok) {
    const host = new URL(v.url).hostname.replace(/^www\./, '');
    const fin = new URL(v.final_url).hostname.replace(/^www\./, '');
    assert.ok(fin === host || fin.endsWith('.' + host), `${b.id}: verified site redirects off-domain`);
    assert.ok(h.includes(`Official site: <a href="${v.url}"`), `${b.id}: verified site not linked`);
  } else {
    assert.ok(h.includes('Official site: not yet verified, so no link is shown.'), `${b.id}: unverified site must not link`);
  }
  for (const [cid, id] of Object.entries(links)) if (id === b.id && fs.existsSync(path.join(DOCS, 'churches', `${cid}.html`)))
    assert.ok(h.includes(`href="/churches/${cid}.html"`), `${b.id}: church ${cid} not listed`);
  assert.ok(index.includes(`href="/denominations/${b.id}.html"`), `${b.id}: not on index`);
}
assert.ok(n >= 100, `only ${n} stubs`);
// Stubs never invent a grade in the public index either.
for (const d of idx.filter(x => x.stub)) assert.strictEqual(d.context_grade, null, `${d.id}: stub has a grade`);
console.log(`denominations-phaseB.test.js: all assertions passed (${n} stubs)`);
