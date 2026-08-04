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

console.log('Kingdom Alignment P1-P3 regression checks passed.');
