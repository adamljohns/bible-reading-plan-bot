#!/bin/bash
# find.sh — locate a single church record in churches.json by slug, name,
# or freeform query; print id + address + website + pastor + gap list.
#
# Usage:
#   bash find.sh faith-baptist-church-fredericksburg
#   bash find.sh "Faith Baptist Fredericksburg"

set -u
cd "$(dirname "$0")/../../../.." || { echo "repo root not found"; exit 1; }

QUERY="${1:-}"
if [ -z "$QUERY" ]; then echo "Usage: $0 <slug-or-name-query>"; exit 1; fi

export QUERY

node -e "
const fs = require('fs');
const q = process.env.QUERY;
const d = JSON.parse(fs.readFileSync('docs/data/churches.json', 'utf8'));
const arr = d.churches || d;

// First try exact slug match
let hits = arr.filter(c => c.slug === q || c.id === q);
if (hits.length === 0) {
  // Then freeform substring match on name + address
  const re = new RegExp(q.replace(/[.*+?^\${}()|[\\]\\\\]/g, '\\\\\$&').replace(/\\s+/g, '.{0,3}'), 'i');
  hits = arr.filter(c => re.test((c.name || '') + ' ' + (c.address || '')));
}

if (hits.length === 0) {
  console.log('NO MATCH for: ' + q);
  process.exit(2);
}

if (hits.length > 1) {
  console.log('MULTIPLE candidates (' + hits.length + '):');
  for (const c of hits.slice(0, 10)) {
    console.log('  ' + (c.slug || c.id).padEnd(50) + ' | ' + (c.name || '').slice(0,35).padEnd(35) + ' | ' + (c.address || '').slice(0,40));
  }
  if (hits.length > 10) console.log('  ...and ' + (hits.length-10) + ' more');
  console.log('');
  console.log('Re-run with the slug of the intended match.');
  process.exit(3);
}

const c = hits[0];
const PH = /^(verify|various|unknown|see\\s+website|currently|none|listed|tbd|n\\/a|the\\s+pastor|the\\s+church|various\\s+pastors|pastoral|pastor\\s*\\(|check |contact |not\\s+(listed|published)|vacant)/i;

console.log('=== ' + (c.name || 'unknown') + ' ===');
console.log('id:                 ' + (c.id || c.slug));
console.log('slug:               ' + (c.slug || c.id));
console.log('address:            ' + (c.address || '(none)'));
console.log('website:            ' + (c.website || '(none)'));
console.log('pastor:             ' + (c.pastor || '(none)'));
console.log('denomination:       ' + (c.denomination || '(none)'));
console.log('cross_listed_in:    ' + (Array.isArray(c.cross_listed_in) ? c.cross_listed_in.join(', ') : '(none)'));
console.log('overall_rating:     ' + (c.overall_rating || '(none)'));
console.log('latitude/longitude: ' + (c.latitude || '?') + ' / ' + (c.longitude || '?'));
console.log('');

// Gap list
const gaps = [];
if (!c.pastor || PH.test(String(c.pastor).trim()) || String(c.pastor).length < 5) gaps.push('pastor');
if (!c.image_url || !/^https?:/.test(c.image_url)) gaps.push('image_url (hero photo)');
if (!c.image_thumb || !/^https?:/.test(c.image_thumb)) gaps.push('image_thumb (logo)');
if (typeof c.latitude !== 'number' || typeof c.longitude !== 'number') gaps.push('latitude/longitude');
if (!Array.isArray(c.enrichment_sources) || c.enrichment_sources.length === 0) gaps.push('enrichment_sources');
if (!Array.isArray(c.quick_links) || c.quick_links.length === 0) gaps.push('quick_links');
if (!c.facebook) gaps.push('facebook');
if (!c.youtube) gaps.push('youtube');
if (!c.website || !/^https?:/.test(c.website)) gaps.push('website');

if (gaps.length === 0) {
  console.log('No obvious gaps; record looks complete.');
} else {
  console.log('GAPS to consider filling:');
  for (const g of gaps) console.log('  - ' + g);
}
"
