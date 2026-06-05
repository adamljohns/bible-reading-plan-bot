#!/usr/bin/env node
//
// check-duplicate.js — the PREVENTION guard. Run this BEFORE adding a church so enrichment
// updates the existing record instead of creating a second (or third) copy. Duplicate records
// with conflicting ratings — the red/yellow/green "three Bent Trees" problem — happen when an
// adder (a scraper, a network import, a manual Hermes add) inserts a church the directory
// already has under a slightly different id/name. This catches that at insert time.
//
// A candidate is flagged as a likely duplicate of an existing record when EITHER:
//   (a) same normalized name + same city  (names compared with church-type words and the city
//       token stripped, so "Bent Tree Bible Fellowship Carrollton" == "Bent Tree Bible Church"), OR
//   (b) same website domain + same street number/name.
//
// Usage:
//   node scripts/check-duplicate.js --name "Truth Bible Church" --city "Hollywood" --state MD \
//        [--website https://truthbiblechurch.com] [--address "24404 Three Notch Rd, Hollywood, MD 20636"]
//   node scripts/check-duplicate.js --json '{"name":"...","address":"...","website":"..."}'
// Exit code 1 (+ prints the existing record(s)) if a likely duplicate exists; 0 if it looks new.

const fs = require('fs');
const path = require('path');
const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');

const STRIP = ['church', 'chapel', 'baptist', 'sbc', 'pca', 'fellowship', 'community', 'ministries', 'ministry'];
const rxEsc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

function normName(name) {
  let n = String(name || '').toLowerCase();
  for (const w of STRIP) n = n.replace(new RegExp('\\b' + w + '\\b', 'g'), '');
  return n.replace(/[^a-z0-9]+/g, ' ').trim();
}
function nameKey(name, city) {
  let k = normName(name);
  for (const t of String(city || '').toLowerCase().split(/\s+/)) {
    if (t.length >= 4) k = k.replace(new RegExp('\\b' + rxEsc(t) + '\\b', 'g'), '');
  }
  return k.replace(/\s+/g, ' ').trim();
}
function domain(url) {
  const m = String(url || '').match(/https?:\/\/(?:www\.)?([^/?#]+)/i);
  return m ? m[1].toLowerCase() : '';
}
function cityOf(addr) {
  const p = String(addr || '').split(',');
  return p.length >= 2 ? p[p.length - 2].trim().toLowerCase() : '';
}
function streetFp(addr) {
  const s = String(addr || '').split(',')[0] || '';
  const m = s.match(/^(\d+)\s+(\w+)/);
  return m ? (m[1] + '-' + m[2].toLowerCase()) : '';
}

// Returns existing records that the candidate would duplicate.
function findDuplicates(cand, churches) {
  const city = String(cand.city || cityOf(cand.address) || '').toLowerCase().trim();
  const nk = nameKey(cand.name, city);
  const dom = domain(cand.website);
  const fp = streetFp(cand.address);
  const hits = [];
  for (const c of churches) {
    const cCity = cityOf(c.address);
    let reason = '';
    if (nk && cCity === city && nameKey(c.name, cCity) === nk) reason = 'same name + city';
    else if (dom && fp && domain(c.website) === dom && streetFp(c.address) === fp) reason = 'same website + street';
    if (reason) hits.push({ id: String(c.id || c.slug), name: c.name, address: c.address, rating: c.overall_rating, reason });
  }
  return hits;
}

module.exports = { findDuplicates, normName, nameKey, domain, streetFp };

if (require.main === module) {
  const arg = k => { const i = process.argv.indexOf('--' + k); return i >= 0 ? process.argv[i + 1] : undefined; };
  const cand = arg('json') ? JSON.parse(arg('json'))
    : { name: arg('name'), city: arg('city'), state: arg('state'), website: arg('website'), address: arg('address') };
  if (!cand.name && !cand.address) {
    console.error('usage: check-duplicate.js --name "X" --city "Y" [--state ST] [--website Z] [--address A]');
    process.exit(2);
  }
  const data = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
  const hits = findDuplicates(cand, data.churches);
  if (hits.length) {
    console.log('DUPLICATE LIKELY — ' + hits.length + ' existing record(s). ENRICH one of these instead of adding a new church:');
    for (const h of hits) console.log('   [' + h.rating + '] ' + h.id + '  "' + h.name + '"  ::  ' + (h.address || '') + '   (' + h.reason + ')');
    process.exit(1);
  }
  console.log('OK — no existing match; safe to add "' + (cand.name || cand.address) + '".');
  process.exit(0);
}
