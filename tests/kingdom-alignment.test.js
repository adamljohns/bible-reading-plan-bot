#!/usr/bin/env node
const assert = require('assert');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const read = rel => fs.readFileSync(path.join(root, rel), 'utf8');

const dictionary = ['kingdom-of-god', 'new-apostolic-reformation', 'prosperity-gospel', 'critical-theory'];
const dictionaryCanonicals = Object.fromEntries(dictionary.map(slug =>
  [slug, `https://usmcmin.org/dictionary/${slug}.html`]));
const zones = ['index', 'green', 'yellow', 'red', 'black'];
const scores = ['index', 'christology', 'scripture', 'mens-discipleship', 'soteriology',
  'gender-biblical-design', 'leadership-structure', 'preaching-style', 'mission-clarity',
  'kingdom-alignment', 'accountability-structure'];

for (const slug of dictionary) {
  const html = read(`docs/dictionary/${slug}.html`);
  for (const heading of ['Biblical Definition', 'Webster 1828 Definition', 'Key Scripture', 'Modern Corruption', 'Usage', 'Related']) {
    assert(html.includes(heading), `${slug} missing ${heading}`);
  }
  for (const asset of ['/assets/css/light-icons.css', '/assets/css/print.css', '../assets/js/moop-tools.js', '/assets/js/print-kit.js']) {
    assert(html.includes(asset), `${slug} missing shared asset ${asset}`);
  }
  assert(html.includes(`<link rel="canonical" href="${dictionaryCanonicals[slug]}">`), `${slug} missing canonical URL`);
  assert(html.includes('../bible.html?ref='), `${slug} missing Bible Engine link`);
}

for (const slug of zones) assert(fs.existsSync(path.join(root, `docs/churches/zones/${slug}.html`)), `missing zone ${slug}`);
for (const slug of scores) assert(fs.existsSync(path.join(root, `docs/churches/scorecard/${slug}.html`)), `missing score ${slug}`);

for (const slug of [...zones.slice(1).map(s => `zones/${s}`), ...scores.slice(1).map(s => `scorecard/${s}`)]) {
  const html = read(`docs/churches/${slug}.html`);
  for (const marker of ['Plain-Speech Definition', 'Signals', 'Primary Source: Scripture', 'MOOP Dictionary',
    'What the Counterfeit Looks Like', 'Questions to Ask', 'Related Categories &amp; Zones', '/connect.html']) {
    assert(html.includes(marker), `${slug} missing ${marker}`);
  }
}

const generator = read('generate-church-pages.js');
assert(generator.includes("cultural: { label: 'Kingdom Alignment'"), 'missing cultural compatibility presentation');
assert(generator.includes("denominational: { label: 'Accountability Structure'"), 'missing accountability compatibility presentation');
assert(generator.includes('/churches/scorecard/${presentation.slug}.html'), 'score label is not linked');
assert(generator.includes('/churches/zones/${zone}.html'), 'zone badge is not linked');

const data = JSON.parse(read('docs/data/churches.json'));
assert(data.rubric.some(r => r.id === 'cultural'), 'legacy cultural key was migrated');
assert(data.rubric.some(r => r.id === 'denominational'), 'legacy denominational key was migrated');
assert(!data.rubric.some(r => r.id === 'kingdom_alignment'), 'P4 schema migration was performed');

const { buildSlimIndex } = require('../scripts/build-church-index');
const fixtureSlim = buildSlimIndex({
  directory_version: 'test',
  directory_updated: '2026-08-29',
  total_churches: 1,
  rubric: [
    { id: 'cultural', label: 'Cultural Alignment', description: 'DEI/CRT language? Social justice crowding out gospel?' },
    { id: 'denominational', label: 'Accountability Structure', description: 'x' }
  ],
  churches: [{ id: 'sample', name: 'Sample', overall_rating: 'yellow' }]
});
const fixtureCultural = fixtureSlim.rubric.find(r => r.id === 'cultural');
assert(fixtureCultural, 'slim builder dropped cultural rubric id');
assert.strictEqual(fixtureCultural.id, 'cultural', 'P4 schema-id rename leaked into slim builder');
assert.strictEqual(fixtureCultural.label, 'Kingdom Alignment', 'slim builder must present cultural as Kingdom Alignment');
assert.ok(!fixtureSlim.rubric.some(r => r.id === 'kingdom_alignment'), 'P4 schema migration leaked into slim builder');

const slim = JSON.parse(read('docs/data/churches-index-slim.json'));
const slimCultural = slim.rubric.find(r => r.id === 'cultural');
assert(slimCultural, 'slim index missing cultural rubric id');
assert.strictEqual(slimCultural.id, 'cultural', 'P4 schema-id rename leaked into slim index');
assert.strictEqual(slimCultural.label, 'Kingdom Alignment', 'slim index cultural display label is not Kingdom Alignment');
assert.ok(!slim.rubric.some(r => r.id === 'kingdom_alignment'), 'P4 schema migration leaked into slim index');

console.log('Kingdom Alignment P1-P3 regression checks passed.');
