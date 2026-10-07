#!/usr/bin/env node
// Female-lead HOLD guard + sitemap <loc> encoding. Both regressed silently once.
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const cp = require('child_process');

const ROOT = path.join(__dirname, '..');
const { looksFemaleFirstName, FEMALE_FIRST } = require(path.join(ROOT, 'scripts/lib/female-first-names.js'));

// The three names the grind published on 2026-10-03 must now be held.
for (const n of ['Elisabeth Chapin', 'Sandy Kessinger', 'Lynn Carter', 'Pastor Lynn Carter', 'Rev. Dr. Megan Collins']) {
  assert.ok(looksFemaleFirstName(n), `guard must hold "${n}"`);
}
for (const n of ['Tim Feaser', 'Dr. Bill Shuler', 'Reverend Francis de Rosa', 'Andrew (Andy) Jagow', 'Jay Serafin']) {
  assert.ok(!looksFemaleFirstName(n), `guard must pass "${n}"`);
}

// Both appliers must use the one shared list, not a private copy.
for (const f of ['scripts/merge-pastor-enrichments.js', 'scripts/apply-roster-pastor-leads.js']) {
  const src = fs.readFileSync(path.join(ROOT, f), 'utf8');
  assert.match(src, /require\('\.\/lib\/female-first-names\.js'\)/, `${f} must use scripts/lib/female-first-names.js`);
  assert.doesNotMatch(src, /const FEMALE_FIRST = (new Set\(\[|\/\^)/, `${f} must not carry a private name list`);
}
assert.ok(FEMALE_FIRST.has('maria') && FEMALE_FIRST.has('olivia') && FEMALE_FIRST.has('lynn'), 'union keeps both legacy lists');

// Sitemap: builder percent-encodes ids, consistency gate decodes before comparing.
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'dirguard-'));
fs.mkdirSync(path.join(tmp, 'scripts'), { recursive: true });
fs.mkdirSync(path.join(tmp, 'docs', 'data'), { recursive: true });
for (const f of ['build-sitemap-churches.js', 'check-consistency.js']) fs.copyFileSync(path.join(ROOT, 'scripts', f), path.join(tmp, 'scripts', f));
fs.writeFileSync(path.join(tmp, 'docs/data/churches.json'), JSON.stringify({ total_churches: 3, churches: [
  { id: 'plain-church-va' }, { id: 'abide-fellowship-beaufort-south carolina' }, { id: 'iglesia-monte-sión' },
] }));
cp.execFileSync('node', ['scripts/build-sitemap-churches.js'], { cwd: tmp });
const xml = fs.readFileSync(path.join(tmp, 'docs/sitemap-churches.xml'), 'utf8');
const locs = [...xml.matchAll(/<loc>([^<]*)<\/loc>/g)].map(m => m[1]);
assert.strictEqual(locs.length, 3);
for (const u of locs) assert.doesNotMatch(u, /[^\x21-\x7e]/, `<loc> must be ASCII with no spaces: ${u}`);
assert.ok(locs.includes('https://usmcmin.org/churches/abide-fellowship-beaufort-south%20carolina.html'));
const out = cp.spawnSync('node', ['scripts/check-consistency.js'], { cwd: tmp, encoding: 'utf8' }).stdout;
assert.match(out, /sitemap-churches\.xml\s+3 <loc> \| missing 0/, 'gate must match encoded <loc>s');
// A raw legacy sitemap must still pass, so a round on the old builder never trips the gate.
fs.writeFileSync(path.join(tmp, 'docs/sitemap-churches.xml'), xml.replace(/%20/g, ' ').replace(/si%C3%B3n/g, 'sión'));
const out2 = cp.spawnSync('node', ['scripts/check-consistency.js'], { cwd: tmp, encoding: 'utf8' }).stdout;
assert.match(out2, /sitemap-churches\.xml\s+3 <loc> \| missing 0/, 'gate must still accept raw legacy <loc>s');
fs.rmSync(tmp, { recursive: true, force: true });

console.log('directory-guards: all assertions passed');
