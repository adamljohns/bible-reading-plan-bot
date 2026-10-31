#!/usr/bin/env node
// Reject US church records whose address carries the "US Minor Outlying Islands"
// country label or a ", UM" token (9Marks listings mis-coded UM instead of US).
// Applies when country_code is US or empty (empty means US).
//
// Usage:
//   node scripts/check-um-address.js            # exit 1 if any record matches
//   node scripts/check-um-address.js --report   # list matches, always exit 0

const fs = require('fs');
const path = require('path');

const FILE = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const REPORT = process.argv.includes('--report');
const BAD = /US Minor Outlying Islands|,\s*UM\b/i;

const { churches } = JSON.parse(fs.readFileSync(FILE, 'utf8'));
const hits = churches.filter(c => {
  const cc = String(c.country_code || '').trim().toUpperCase();
  return (cc === '' || cc === 'US') && typeof c.address === 'string' && BAD.test(c.address);
});

console.log(`check-um-address: ${hits.length} record(s) with a UM/Minor Outlying Islands address`);
for (const c of hits) console.log(`  ${c.id}\t${c.address}`);
process.exit(hits.length && !REPORT ? 1 : 0);
