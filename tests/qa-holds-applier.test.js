#!/usr/bin/env node
// Regression test for scripts/apply-pastor-qa-holds.js actions (hold/clear/set/stamp/text)
// on a scratch tree — never touches the real churches.json.
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const root = fs.mkdtempSync(path.join(os.tmpdir(), 'qa-holds-'));
fs.mkdirSync(path.join(root, 'scripts/lib'), { recursive: true });
fs.mkdirSync(path.join(root, 'docs/data'), { recursive: true });
const src = path.join(__dirname, '..', 'scripts');
// The scratch copy points its lock check at a path inside the scratch tree so the
// test runs while the grind holds the real lock; the real script is unchanged.
const lockRef = "'/tmp/directory-grind-session.lock'";
const appSrc = fs.readFileSync(path.join(src, 'apply-pastor-qa-holds.js'), 'utf8');
assert.ok(appSrc.includes(`fs.existsSync(${lockRef})`), 'applier must still refuse under the session lock');
fs.writeFileSync(path.join(root, 'scripts/apply-pastor-qa-holds.js'), appSrc.split(lockRef).join(JSON.stringify(path.join(root, 'no-such.lock'))));
fs.copyFileSync(path.join(src, 'lib/format-preserving-write.js'), path.join(root, 'scripts/lib/format-preserving-write.js'));

const churches = [
  { id: 'a', pastor: 'Jane Roe', pastors: [{ name: 'Jane Roe', role: 'Pastor' }] },
  { id: 'b', pastor: 'Office Admin' },
  { id: 'c', pastor: 'Dr. Long (prose)', pastors: [{ name: 'Dr. Long (prose)', role: 'Senior Pastor' }] },
  { id: 'd', pastor: 'Kept Name' },
  { id: 'e', pastor: 'X', score_notes: { leadership: '9 pastors (A, B, Z)' } },
  { id: 'f', pastor: 'Moved On' },
];
const dataFile = path.join(root, 'docs/data/churches.json');
fs.writeFileSync(dataFile, JSON.stringify({ churches }, null, 2) + '\n');
const holds = [
  { id: 'a', pastor: 'Jane Roe', source: 's', evidence: 'e' },
  { id: 'b', pastor: 'Office Admin', action: 'clear', role: 'Parish Administrator', source: 's' },
  { id: 'c', pastor: 'Dr. Long (prose)', action: 'set', value: 'Dr. Long', source: 's' },
  { id: 'd', pastor: 'Kept Name', action: 'stamp', reason: 'r.', source: 's' },
  { id: 'e', action: 'text', field: 'score_notes.leadership', find: '9 pastors (A, B, Z)', replace: '8 pastors (A, B)', source: 's' },
  { id: 'f', pastor: 'Someone Else', action: 'set', value: 'Nope', source: 's' },
  { id: 'f', pastor: 'Moved On', action: 'typo', source: 's' },
];
const holdsFile = path.join(root, 'holds.json');
fs.writeFileSync(holdsFile, JSON.stringify(holds));
const run = () => execFileSync('node', [path.join(root, 'scripts/apply-pastor-qa-holds.js'), '--holds', holdsFile, '--apply'], { encoding: 'utf8' });

const out1 = run();
assert.match(out1, /applied 5 correction/);
const by = Object.fromEntries(JSON.parse(fs.readFileSync(dataFile, 'utf8')).churches.map(c => [c.id, c]));
assert.strictEqual(by.a.pastor, ''); assert.ok(by.a._hold_review); assert.strictEqual(by.a.pastors, undefined);
assert.strictEqual(by.b.pastor, ''); assert.strictEqual(by.b._hold_review, undefined); assert.strictEqual(by.b.needs_review, true);
assert.strictEqual(by.c.pastor, 'Dr. Long'); assert.strictEqual(by.c.pastors[0].name, 'Dr. Long');
assert.strictEqual(by.d.pastor, 'Kept Name'); assert.ok(by.d._hold_review); assert.match(by.d.enrichment_notes, /QA hold: r\./);
assert.strictEqual(by.e.score_notes.leadership, '8 pastors (A, B)');
assert.strictEqual(by.f.pastor, 'Moved On'); assert.match(out1, /SKIP f — unknown action "typo"/);

const out2 = run();
assert.match(out2, /applied 0 correction/);
console.log('qa-holds-applier: all assertions passed');
