#!/usr/bin/env node
'use strict';
// One fetch timeout must NOT stamp _dead_site; two consecutive timeouts must.
// A hard verdict (404) still stamps on the first observation, and a good
// fetch between timeouts resets the run. Synthetic churches.json only.

const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const cp = require('child_process');

const MERGE = path.join(__dirname, '..', 'scripts/merge-pastor-enrichments.js');
const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'dead-site-'));
const churchesPath = path.join(dir, 'churches.json');
const base = { name: 'Sample Church', state: 'VA', website: 'https://sample.example', pastor: '', enrichment_notes: '' };
fs.writeFileSync(churchesPath, JSON.stringify({ total_churches: 3, churches: [
  { ...base, id: 'slow' }, { ...base, id: 'gone' }, { ...base, id: 'flaky' },
] }, null, 2));

function merge(entries) {
  const input = path.join(dir, `in-${Date.now()}-${Math.random()}.json`);
  fs.writeFileSync(input, JSON.stringify(entries));
  const r = cp.spawnSync(process.execPath, [MERGE, '--input', input],
    { env: { ...process.env, MERGE_CHURCHES_PATH: churchesPath }, encoding: 'utf8' });
  assert.strictEqual(r.status, 0, r.stderr);
  const d = JSON.parse(fs.readFileSync(churchesPath, 'utf8'));
  return Object.fromEntries(d.churches.map(c => [c.id, c]));
}

let by = merge([
  { id: 'slow', website_status: 'timeout' },
  { id: 'gone', website_status: '404' },
  { id: 'flaky', website_status: 'timeout' },
]);
assert.ok(!by.slow._dead_site, 'ONE timeout must not stamp _dead_site');
assert.strictEqual(by.slow._site_timeout_strikes, 1);
assert.ok(by.gone._dead_site, 'a 404 is a hard verdict and still stamps');

by = merge([
  { id: 'slow', website_status: 'timeout' },
  { id: 'flaky', website_status: '200_no_pastor_found' },
]);
assert.ok(by.slow._dead_site, 'two consecutive timeouts must stamp _dead_site');
assert.ok(!by.slow._site_timeout_strikes, 'the strike counter clears once stamped');
assert.ok(!by.flaky._site_timeout_strikes, 'a good fetch resets the timeout run');

by = merge([{ id: 'flaky', website_status: 'timeout' }]);
assert.ok(!by.flaky._dead_site, 'timeout, good fetch, timeout is not two consecutive');

console.log('merge-dead-site-timeout: all assertions passed');
