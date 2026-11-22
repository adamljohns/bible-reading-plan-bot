#!/usr/bin/env node
'use strict';
// website-discovery-matcher.test.js — regression suite for CM-1122-WEBDISC.
//
// The old website-discovery rule accepted a search hit whose domain merely CONTAINED
// one name token (`dist.some(t => dc.includes(t))`) with the homepage geo-guard off.
// It wrote brown.edu / clevelandbrowns.com on 11-15 (reverted 11-16) and then 519
// wrong sites 11-16..22 (liberty.edu x12, providence.org x11, thenorthface.com x8 …).
// This suite pins:
//   * the 14 cases from 11-15 (9 wrong must FAIL, 5 right must PASS domain + page)
//   * every 11-16..22 record that landed on a shared domain must FAIL
//   * the guards added during the re-check (denomination conflict, other state,
//     subdomain, institution, shared domain, page address in another state)
//   * the discovery and rescue scripts actually use the checker (no substring rule)
// Offline: homepage fixtures were captured 2026-11-22 (tags stripped).

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const M = require('../scripts/lib/church-website-match.js');

const FIX = path.join(__dirname, 'fixtures', 'website-match');
const cases = JSON.parse(fs.readFileSync(path.join(FIX, 'cases.json'), 'utf8'));
let pass = 0, fail = 0;
function t(name, fn) {
  try { fn(); pass++; console.log(`  ok  ${name}`); }
  catch (e) { fail++; console.log(`  FAIL ${name}\n       ${e.message}`); }
}

console.log('11-15 wrong discoveries (must fail)');
assert.strictEqual(cases.wrong_1115.length, 9);
for (const c of cases.wrong_1115) {
  t(`${c.id} ✗ ${c.website}`, () => {
    const v = M.domainVerdict(c, c.website);
    assert.strictEqual(v.ok, false, `accepted ${c.website} (${v.reason} ${v.segs || ''})`);
  });
}

console.log('11-15 right discoveries (must pass domain + homepage)');
assert.strictEqual(cases.right_1115.length, 5);
for (const c of cases.right_1115) {
  t(`${c.id} ✓ ${c.website}`, () => {
    const v = M.domainVerdict(c, c.website);
    assert.strictEqual(v.ok, true, `rejected ${c.website}: ${v.reason}`);
    const html = fs.readFileSync(path.join(FIX, `${c.id}.html`), 'utf8');
    const p = M.pageVerdict(c, html);
    assert.strictEqual(p.ok, true, `homepage rejected: ${p.reason}`);
  });
}

console.log('11-16..22 shared-domain discoveries (must fail)');
const all = cases.shared_1116_1122;
assert.ok(all.length >= 100, `expected the full shared-domain fixture, got ${all.length}`);
const assigned = M.buildAssignedDomains(all);
const byDomain = {};
for (const c of all) (byDomain[M.regDomain(c.website)] = byDomain[M.regDomain(c.website)] || []).push(c);
for (const [dom, list] of Object.entries(byDomain)) {
  t(`${dom} x${list.length}`, () => {
    for (const c of list) {
      const v = M.domainVerdict(c, c.website, { assigned });
      assert.strictEqual(v.ok, false, `${c.id} accepted ${c.website}`);
    }
  });
}
for (const dom of ['liberty.edu', 'providence.org', 'centraltransport.com', 'thenorthface.com', 'crossroads.net', 'roundpointmortgage.com', 'concord.net', 'crosspointreader.com', 'hebronbrick.com']) {
  t(`${dom} fails on the token rule alone (no shared-domain help)`, () => {
    const list = byDomain[dom] || [];
    assert.ok(list.length, `fixture has no ${dom} rows`);
    for (const c of list) assert.strictEqual(M.domainVerdict(c, c.website).ok, false, `${c.id} accepted ${c.website}`);
  });
}

console.log('guards');
const rec = (name, address, state, extra = {}) => ({ id: name.toLowerCase().replace(/\W+/g, '-'), name, address, state, ...extra });
t('single-token domain rejected (liberty.edu even without .edu rule)', () => {
  const c = rec('Liberty Baptist Church', '1525 Pennington Rd, Trenton, NJ 08618', 'NJ');
  assert.strictEqual(M.domainVerdict(c, 'https://www.liberty.org').ok, false);
  assert.strictEqual(M.domainVerdict(c, 'https://www.liberty.edu').reason, 'edu-gov-tld');
});
t('whole-token two-word domain accepted', () => {
  const c = rec('Liberty Baptist Church', '1525 Pennington Rd, Trenton, NJ 08618', 'NJ');
  assert.strictEqual(M.domainVerdict(c, 'https://www.libertybaptisttrenton.org').ok, true);
});
t('substring inside another word rejected (thenorthface / hebronbrick)', () => {
  assert.strictEqual(M.domainVerdict(rec('North Baptist Church', '1 Main St, Dover, DE 19901', 'DE'), 'https://www.thenorthface.com').ok, false);
  assert.strictEqual(M.domainVerdict(rec('Hebron Baptist Church', '1 Main St, Dacula, GA 30019', 'GA'), 'https://hebronbrick.com').ok, false);
});
t('non-www subdomain rejected (login.concord.net)', () => {
  const c = rec('Concord Baptist Church', '1 Main St, Concord, NC 28025', 'NC');
  assert.strictEqual(M.domainVerdict(c, 'https://login.concordbaptist.net').reason, 'subdomain');
});
t('school / k12 / city / county hosts rejected', () => {
  const c = rec('Buchanan Baptist Church', '19730 Main St, Buchanan, VA 24066', 'VA');
  for (const u of ['https://buchanan.livoniapublicschools.org', 'https://buchananbaptistacademy.org', 'https://www.buchanank12.org', 'https://www.cityofbuchanan.com', 'https://www.co.buchanan.va.us', 'https://buchanan.va.gov'])
    assert.strictEqual(M.domainVerdict(c, u).ok, false, u);
});
t('institution word allowed when it is the church\'s own name (College Park Baptist)', () => {
  const c = rec('College Park Baptist Church', '1 Main St, Orlando, FL 32804', 'FL');
  assert.strictEqual(M.domainVerdict(c, 'https://collegeparkbaptist.org').ok, true);
});
t('domain already on another church rejected', () => {
  const a = rec('Macedonia A.M.E. Church', '1 Church Rd, Accomac, VA 23301', 'VA');
  const b = { ...rec('Macedonia A.M.E. Church', '1 Smith Neck Rd, Carrollton, VA 23314', 'VA'), id: 'macedonia-2' };
  const asg = M.buildAssignedDomains([{ ...a, website: 'https://www.macedoniaame.com' }]);
  assert.strictEqual(M.domainVerdict(b, 'https://www.macedoniaame.com', { assigned: asg }).reason, 'domain-assigned-to-other-church');
  assert.strictEqual(M.domainVerdict(a, 'https://www.macedoniaame.com', { assigned: asg }).ok, true, 'own assignment is not a conflict');
});
t('denomination conflict rejected (First Baptist Wylie → wyliechurchofchrist.org)', () => {
  const c = rec('First Baptist Church Wylie', '200 N Ballard Ave, Wylie, TX 75098', 'TX', { denomination: 'Southern Baptist Convention (SBC)' });
  assert.strictEqual(M.domainVerdict(c, 'https://wyliechurchofchrist.org').reason, 'denomination-conflict');
  assert.strictEqual(M.facebookSlugVerdict(rec('Ontario First Baptist Church', '1 Main St, Ontario, OR 97914', 'OR'), 'FirstChristianChurchOntario').ok, false);
});
t('another state in the domain rejected (Clinton UMC, MD → clintonumcil.org)', () => {
  const c = rec('Clinton UMC', '10700 Brandywine Rd, Clinton, MD 20735', 'MD');
  assert.strictEqual(M.domainVerdict(c, 'https://clintonumcil.org').reason, 'other-state-in-domain');
});
t('homepage: church word AND city/state required; other-state street address rejected', () => {
  const c = rec('Clover UMC', '1 Main St, Clover, VA 24534', 'VA');
  assert.strictEqual(M.pageVerdict(c, '<title>Clover Outlet</title><body>Shop shoes in Clover today</body>').reason, 'no-church-word');
  assert.strictEqual(M.pageVerdict(c, '<body>Clover church worship Sunday</body>').ok, true);
  assert.strictEqual(M.pageVerdict(c, '<body>Clover church worship. 112 Bethel Street Clover, SC 29710</body>').reason, 'address-in-other-state');
  assert.strictEqual(M.pageVerdict(c, '<body>A church that worships in Texas</body>').reason, 'no-city-or-state');
  assert.strictEqual(M.pageVerdict(c, '').reason, 'fetch-empty');
});
t('facebook slug: whole tokens, page-id suffix ignored, substring rejected', () => {
  assert.strictEqual(M.facebookSlugVerdict(rec('Delmont UMC', '1 Main St, Delmont, PA 15626', 'PA'), 'Delmont-United-Methodist-Church-228133737209700').ok, true);
  assert.strictEqual(M.facebookSlugVerdict(rec('Liberty Baptist Church', '1 Main St, Trenton, NJ 08618', 'NJ'), 'LibertyUniversity').ok, false);
});

console.log('callers use the checker');
const repo = path.join(__dirname, '..');
for (const f of ['scripts/find-church-websites.js', 'scripts/rediscover-dead-websites.js']) {
  t(`${f} uses church-website-match and has no substring domain rule`, () => {
    const src = fs.readFileSync(path.join(repo, f), 'utf8').split('\n').filter(l => !/^\s*\/\//.test(l)).join('\n');
    assert.ok(/require\('\.\/lib\/church-website-match\.js'\)/.test(src), 'checker not required');
    assert.ok(/WM\.checkCandidate\(/.test(src), 'checkCandidate not called');
    assert.ok(!/dist\.some\(t => (dc|slug)\.includes\(t\)\)/.test(src), 'substring rule still present');
  });
}

console.log('grind accounting');
t('summarizer counts website-discovery hits only with the checker tag', () => {
  const { summarizeLines } = require('../scripts/summarize-grind-session.js');
  const old = summarizeLines(['[2026-11-20 03:07:59] frontier lane done: website-discovery attempted=25 applied=20']);
  assert.strictEqual(old.content_applied, 0); assert.strictEqual(old.unchecked_discovery, 20);
  const now = summarizeLines([`[2026-11-23 03:07:59] frontier lane done: website-discovery attempted=25 applied=2 checker=${M.CHECKER}`]);
  assert.strictEqual(now.content_applied, 2); assert.strictEqual(now.unchecked_discovery, 0);
  const src = summarizeLines(['[2026-11-23 03:07:59] frontier lane done: source-recovery attempted=25 applied=4']);
  assert.strictEqual(src.content_applied, 4, 'other frontier lanes unaffected');
});
t('discovery lane refuses output without the checker tag', () => {
  const src = fs.readFileSync(path.join(repo, 'scripts/continuous-enrichment-lane.sh'), 'utf8');
  assert.ok(/checker=church-website-match\/v\[0-9\]\+/.test(src) && /\|\| die "website-discovery ran without the whole-token website checker/.test(src));
  assert.ok(fs.readFileSync(path.join(repo, 'scripts/find-church-websites.js'), 'utf8').includes('checker=${WM.CHECKER}'));
});

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
