#!/usr/bin/env node
// backfill-sources.js — populate the enrichment_sources array on ONE church
// record from the things we already know about it: the church's own website,
// a Google Maps deep link built from lat/lng (or address), and the directory
// URL for any network it cross-lists into.
//
// Usage:
//   node .claude/skills/enrich-church-single/scripts/backfill-sources.js <church-id>

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', '..', '..', '..', 'docs', 'data', 'churches.json');

const NETWORK_URLS = {
  sbc: 'https://www.sbc.net/',
  acts29: 'https://www.acts29.com/find-a-church/',
  '9marks': 'https://www.9marks.org/church-search/',
  'tgc-cn': 'https://www.thegospelcoalition.org/churches/',
  founders: 'https://church.founders.org/churches',
  'pillar-network': 'https://thepillarnetwork.com/directory',
  sgc: 'https://sovereigngrace.com/churches',
  'trinity-foundation': 'https://trinityfoundation.org/churchapproved.php',
};

const id = process.argv[2];
if (!id) { console.error('Usage: backfill-sources.js <church-id>'); process.exit(1); }

const data = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
const c = data.churches.find(x => (x.id || x.slug) === id);
if (!c) { console.error('No church found with id ' + id); process.exit(2); }

const srcs = [];
if (c.website && /^https?:\/\/[^\/\s]/i.test(c.website)) srcs.push(c.website);
if (typeof c.latitude === 'number' && typeof c.longitude === 'number') {
  srcs.push(`https://www.google.com/maps/search/?api=1&query=${c.latitude},${c.longitude}`);
} else if (c.address) {
  srcs.push(`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(c.address)}`);
}
if (Array.isArray(c.cross_listed_in)) {
  for (const n of c.cross_listed_in) if (NETWORK_URLS[n]) srcs.push(NETWORK_URLS[n]);
}

const uniq = [...new Set(srcs)];
if (uniq.length === 0) {
  console.log('No sources could be inferred for ' + id);
  process.exit(0);
}

c.enrichment_sources = uniq;
fs.writeFileSync(CHURCHES, JSON.stringify(data, null, 2) + '\n');

console.log('Backfilled enrichment_sources for ' + (c.name || id) + ':');
for (const s of uniq) console.log('  - ' + s);
console.log('');
console.log('Next: node generate-church-pages.js && git add docs/data/churches.json docs/churches/<slug>.html && git commit/push');
