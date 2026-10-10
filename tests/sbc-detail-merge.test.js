'use strict';

const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const test = require('node:test');

test('SBC detail merge applies only postal-corroborated results', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'sbc-detail-merge-'));
  try {
    fs.mkdirSync(path.join(root, 'scripts', 'lib'), { recursive: true });
    fs.mkdirSync(path.join(root, 'docs', 'data'), { recursive: true });
    fs.copyFileSync(path.join(__dirname, '..', 'scripts', 'merge-sbc-detail.js'), path.join(root, 'scripts', 'merge-sbc-detail.js'));
    fs.copyFileSync(path.join(__dirname, '..', 'scripts', 'lib', 'sbc-detail-identity.js'), path.join(root, 'scripts', 'lib', 'sbc-detail-identity.js'));

    const churches = { churches: [
      { id: 'mismatch', address: 'Beaumont, MS 39423' },
      { id: 'legacy', address: 'Beaumont, MS 39423' },
      { id: 'match', address: 'Beaumont, MS 39423-2437' },
      { id: 'error', address: 'Beaumont, MS 39423' },
    ] };
    fs.writeFileSync(path.join(root, 'docs', 'data', 'churches.json'), JSON.stringify(churches));
    const jsonl = path.join(root, 'results.jsonl');
    fs.writeFileSync(jsonl, [
      { id: 'mismatch', sbc_detail_source_postal: '39479', website: 'https://wrong.example', latitude: 31.56, longitude: -89.49, phone: '601-555-0000', sbc_detail_fetched_at: '2026-10-10T08:04:14.080Z' },
      { id: 'legacy', website: 'https://unproven.example', sbc_detail_fetched_at: '2026-10-10T08:04:14.080Z' },
      { id: 'match', sbc_detail_source_postal: '39423', website: 'https://right.example', latitude: 31.20, longitude: -89.01, phone: '601-555-1212', sbc_detail_fetched_at: '2026-10-10T08:04:14.080Z' },
      { id: 'error', sbc_detail_error: 'TIMEOUT', sbc_detail_failed_at: '2026-10-10T08:05:00.000Z' },
    ].map(JSON.stringify).join('\n') + '\n');

    const output = execFileSync(process.execPath, [path.join(root, 'scripts', 'merge-sbc-detail.js'), '--jsonl', jsonl], { encoding: 'utf8' });
    execFileSync(process.execPath, [path.join(root, 'scripts', 'merge-sbc-detail.js'), '--jsonl', jsonl], { encoding: 'utf8' });
    const merged = JSON.parse(fs.readFileSync(path.join(root, 'docs', 'data', 'churches.json'), 'utf8')).churches;
    const byId = Object.fromEntries(merged.map(c => [c.id, c]));

    assert.strictEqual(byId.mismatch.website, undefined);
    assert.strictEqual(byId.mismatch._hold_review, 'sbc-source-identity-mismatch');
    assert.match(byId.mismatch.sbc_detail_error, /postal mismatch/);
    assert.strictEqual(byId.legacy.website, undefined);
    assert.strictEqual(byId.legacy._hold_review, undefined);
    assert.strictEqual(byId.match.website, 'https://right.example');
    assert.strictEqual(byId.match.geocode_source, 'sbc.net');
    assert.strictEqual(byId.match.phone, '601-555-1212');
    assert.strictEqual(byId.match.sbc_detail_fetched_at, '2026-10-10T08:04:14.080Z');
    assert.strictEqual(byId.error._sbc_detail_failures, 1, 're-merging one historical error must be idempotent');
    assert.strictEqual(byId.error.sbc_detail_failed_at, '2026-10-10T08:05:00.000Z');
    assert.match(output, /1 held for source-identity review/);
    assert.match(output, /1 legacy results skipped without identity evidence/);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
