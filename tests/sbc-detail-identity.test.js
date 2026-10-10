'use strict';

const assert = require('assert');
const test = require('node:test');
const { extractSourcePostal, validateSourceIdentity, isIdentityCompleteResult } = require('../scripts/lib/sbc-detail-identity.js');

test('extracts the SBC detail postal code from heading address HTML', () => {
  const html = '<h3 class="heading__address">220 E Main St<br/> Seminary, MS 39479</h3>';
  assert.strictEqual(extractSourcePostal(html), '39479');
});

test('accepts a source result when canonical and source postal codes match', () => {
  assert.strictEqual(validateSourceIdentity(
    { address: '120 Main St, Beaumont, MS 39423' },
    { sbc_detail_source_postal: '39423' }
  ), null);
});

test('accepts ZIP+4 when its first five digits match', () => {
  assert.strictEqual(validateSourceIdentity(
    { address: '120 Main St, Beaumont, MS 39423-1234' },
    { sbc_detail_source_postal: '39423' }
  ), null);
});

test('rejects same-name SBC detail results from a different postal code', () => {
  assert.match(validateSourceIdentity(
    { address: 'Beaumont, MS 39423' },
    { sbc_detail_source_postal: '39479' }
  ), /postal mismatch: canonical 39423, source 39479/);
});

test('fails closed when a successful source result lacks identity evidence', () => {
  assert.match(validateSourceIdentity(
    { address: 'Beaumont, MS 39423' },
    { website: 'https://example.org' }
  ), /missing source postal/);
});

test('fails closed when the canonical record lacks a postal code', () => {
  assert.match(validateSourceIdentity(
    { address: 'Beaumont, MS' },
    { sbc_detail_source_postal: '39423' }
  ), /missing canonical postal/);
});

test('persistent scrape ledger retries only legacy successful rows without identity evidence', () => {
  assert.strictEqual(isIdentityCompleteResult({ id: 'legacy', website: 'https://example.org' }), false);
  assert.strictEqual(isIdentityCompleteResult({ id: 'current', sbc_detail_source_postal: '39423' }), true);
  assert.strictEqual(isIdentityCompleteResult({ id: 'failed', sbc_detail_error: 'TIMEOUT' }), false);
});
