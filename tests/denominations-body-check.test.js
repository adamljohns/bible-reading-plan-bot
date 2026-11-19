#!/usr/bin/env node
'use strict';
// denominations-body-check.test.js — quotes validate against the document BODY
// only (CCW-1119-DIR2 QA). Site nav, header and footer text can never make a
// quote pass; the check is case-sensitive; every snapshot has a body file
// whose hash matches its meta; QA fixes stay fixed.
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const REPO = path.join(__dirname, '..');
const D = require(path.join(REPO, 'scripts/lib/denominations.js'));

// 1. The extractor drops chrome: a footer-only sentence is not in the body.
const html = `<html><head><title>t</title></head><body><header>Site Header Words</header>
<nav><a href="/">Top navigation link text</a></nav>
<main><h1>Paragraph 120</h1><nav>In-page breadcrumb trail</nav>
<p>The mission of the Church is to make disciples.</p><footer>main-region footer note</footer></main>
<footer><p>The mission of the church is the footer tagline only.</p></footer></body></html>`;
const py = `import sys,json; sys.path.insert(0, ${JSON.stringify(path.join(REPO, 'scripts/lib'))})
from denomination_body_text import body_text
print(json.dumps(body_text(sys.stdin.read())))`;
const [body, region] = JSON.parse(execFileSync('python3', ['-I', '-c', py], { input: html }).toString());
assert.strictEqual(region, 'main');
assert.ok(body.includes('The mission of the Church is to make disciples.'), 'body text missing');
for (const chrome of ['Site Header Words', 'Top navigation link text', 'In-page breadcrumb trail', 'main-region footer note', 'footer tagline only'])
  assert.ok(!body.includes(chrome), `chrome leaked into body: ${chrome}`);

// 2. A footer-only quote FAILS the ledger even though it is on the page.
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'denom-body-'));
const crypto = require('crypto');
const sha = t => crypto.createHash('sha256').update(t).digest('hex');
const full = 'Paragraph 120 The mission of the Church is to make disciples. The mission of the church is the footer tagline only.';
fs.mkdirSync(path.join(tmp, 'zz'));
fs.writeFileSync(path.join(tmp, 'zz', 'p.txt'), full + '\n');
fs.writeFileSync(path.join(tmp, 'zz', 'p.body.txt'), body + '\n');
fs.writeFileSync(path.join(tmp, 'zz', 'p.meta.json'), JSON.stringify({ url: 'https://example.org/p', sha256_text: sha(full), sha256_body: sha(body) }));
const fake = { id: 'zz', evidence: [
  { id: 'footer-only', source: 'p', url: 'https://example.org/p', quote: 'The mission of the church is the footer tagline only.', supports: ['mission'] },
  { id: 'body', source: 'p', url: 'https://example.org/p', quote: 'The mission of the Church is to make disciples.', supports: ['mission'] },
  { id: 'wrong-case', source: 'p', url: 'https://example.org/p', quote: 'the mission of the church is to make disciples.', supports: ['mission'] },
] };
const L = Object.fromEntries(D.buildLedger(fake, tmp).map(l => [l.id, l]));
assert.strictEqual(L['footer-only'].validated, false, 'footer-only quote must FAIL');
assert.strictEqual(L['footer-only'].error, 'quote not in document body');
assert.strictEqual(L.body.validated, true, 'body quote must pass');
assert.strictEqual(L['wrong-case'].validated, false, 'case-changed quote must FAIL');
// No body snapshot = no validation.
fs.unlinkSync(path.join(tmp, 'zz', 'p.body.txt'));
assert.strictEqual(D.buildLedger(fake, tmp)[1].validated, false, 'missing body file must FAIL');
fs.rmSync(tmp, { recursive: true });

// 3. Real case: the umc.org footer tagline is in the full page but not the ¶120 body.
const s120 = D.loadSource('umc', 'bod-120-the-churches');
const tagline = 'The mission of the church is to make disciples of Jesus Christ for the transformation of the world.';
assert.ok(s120.full.includes(tagline), 'fixture: tagline should be in the full page');
assert.ok(!D.quoteInSource(tagline, s120.text), 'umc.org footer tagline must not validate');

// 4. Every snapshot has a hashed body file; every ledger row validates on it.
const SRC = D.SRC_DIR;
for (const dir of fs.readdirSync(SRC)) for (const f of fs.readdirSync(path.join(SRC, dir)).filter(f => f.endsWith('.meta.json'))) {
  const slug = f.slice(0, -'.meta.json'.length);
  const s = D.loadSource(dir, slug);
  assert.ok(s.sha_ok, `${dir}/${slug}: body/full hash mismatch or no sha256_body`);
  assert.ok(s.meta.body_region, `${dir}/${slug}: body_region not recorded`);
}
const denoms = D.loadDenominations();
for (const d of denoms) {
  const ledger = D.buildLedger(d);
  for (const l of ledger) assert.ok(l.validated, `${d.id} ${l.id}: ${l.error}`);
  const sc = D.scoreDenomination(d, ledger);
  for (const [k, v] of Object.entries(sc.scores)) if (v.grade !== 'unknown') assert.ok(v.rule && v.evidence.length, `${d.id} ${k}: ${v.grade} grade has no quote`);
}

// 5. QA fixes stay fixed.
const ev = (id, eid) => denoms.find(d => d.id === id).evidence.find(e => e.id === eid);
assert.ok(ev('umc', 'umc-mission').quote.startsWith('The mission of the Church is'), 'UMC ¶120 capital C');
assert.ok(ev('umc', 'umc-gc2024-restrictions-removed').quote.endsWith('treated with respect to their sexuality or gender identity.'), 'restrictions quote complete');
const umc = D.scoreDenomination(denoms.find(d => d.id === 'umc'), D.buildLedger(denoms.find(d => d.id === 'umc')));
assert.strictEqual(umc.scores.denominational.grade, 'red');
assert.ok(umc.scores.denominational.evidence.includes('umc-gc2024-restrictions-removed'), 'UMC accountability RED shows its quote');
const sbc = D.scoreDenomination(denoms.find(d => d.id === 'sbc'), D.buildLedger(denoms.find(d => d.id === 'sbc')));
assert.deepStrictEqual(sbc.scores.scripture.evidence, ['sbc-bfm-scripture', 'sbc-bfm-supreme-standard'], 'SBC D-SCR-1 cites inerrancy AND supreme standard');
// D-SCR-1 needs both halves.
const g = quotes => D.scoreDenomination({ id: 'zz' }, quotes.map((q, i) => ({ id: 'q' + i, quote: q, supports: ['scripture'], validated: true }))).scores.scripture.grade;
assert.strictEqual(g(['Scripture is without error.']), 'unknown', 'inerrancy alone is not GREEN');
assert.strictEqual(g(['Scripture is without error.', 'It is the supreme standard.']), 'green');
// BGAV: the Webflow PDF is linked from a captured bgav.org page.
const bgav = denoms.find(d => d.id === 'bgav');
const prov = bgav.source_provenance.find(p => p.file === 'what-va-baptists-believe');
const ql = D.loadSource('bgav', prov.linked_from_snapshot);
const pdf = D.loadSource('bgav', 'what-va-baptists-believe');
assert.ok(/^https:\/\/www\.bgav\.org\//.test(prov.linked_from) && ql.meta.url === prov.linked_from, 'BGAV linking page is bgav.org and captured');
assert.ok(ql.meta.links_to_verified === true && ql.meta.links_to === pdf.meta.url, 'BGAV linking page links the exact PDF');
assert.strictEqual(pdf.meta.linked_from, prov.linked_from);
console.log('denominations-body-check.test.js: all assertions passed');
