#!/bin/bash
# Print a canonical coverage snapshot for the MOOP Church Directory.
# Optional arg: a state code, city name, or network slug to scope the count.
#
# Examples:
#   bash pulse.sh                # full directory
#   bash pulse.sh VA              # VA churches only
#   bash pulse.sh Fredericksburg # city scope
#   bash pulse.sh sbc            # network scope (cross_listed_in='sbc')

set -u
cd "$(dirname "$0")/../../../.." || { echo "repo root not found"; exit 1; }

export PULSE_SCOPE="${1:-}"

node -e "
const fs = require('fs');
const d = JSON.parse(fs.readFileSync('docs/data/churches.json', 'utf8'));
const arr = d.churches || d;
const scope = process.env.PULSE_SCOPE || null;

// Filter
let pool = arr;
let scopeLabel = 'ALL';
if (scope) {
  const s = String(scope);
  const sl = s.toLowerCase();
  // Network match: scope is in cross_listed_in (case-insensitive exact)
  const isNetwork = ['sbc','founders','9marks','tgc-cn','acts29','sgc','pillar-network','trinity-foundation'].includes(sl);
  if (isNetwork) {
    pool = arr.filter(c => Array.isArray(c.cross_listed_in) && c.cross_listed_in.includes(sl));
    scopeLabel = 'cross_listed_in=' + sl;
  } else if (s.length === 2) {
    // Two-letter state
    pool = arr.filter(c => new RegExp(',\\\\s*' + s.toUpperCase() + '\\\\b').test(c.address || ''));
    scopeLabel = 'state=' + s.toUpperCase();
  } else {
    // City / freeform substring
    const re = new RegExp(s.replace(/[.*+?^\${}()|[\\]\\\\]/g, '\\\\\$&'), 'i');
    pool = arr.filter(c => re.test(c.address || ''));
    scopeLabel = 'address~/' + s + '/i';
  }
}

const total = pool.length;
const pct = n => total ? ((n/total)*100).toFixed(1) + '%' : '--';

// Tight pastor filter (rejects all known placeholder phrases)
const PH = /^(verify|various|unknown|see\\s+website|currently|none|listed|tbd|n\\/a|the\\s+pastor|the\\s+church|various\\s+pastors|pastoral|pastor\\s*\\(|check |contact |not\\s+(listed|published)|vacant)/i;
const realPastor = pool.filter(c => {
  const p = (c.pastor || '').trim();
  if (!p || p.length < 4) return false;
  return !PH.test(p);
}).length;

const withImage = pool.filter(c => c.image_url && /^https?:/.test(c.image_url)).length;
const withLogo  = pool.filter(c => c.image_thumb && /^https?:/.test(c.image_thumb)).length;
const geocoded  = pool.filter(c => typeof c.latitude === 'number' && typeof c.longitude === 'number').length;
const qLinks    = pool.filter(c => Array.isArray(c.quick_links) && c.quick_links.length > 0).length;
const qLinksTotal = pool.reduce((n,c) => n + (Array.isArray(c.quick_links) ? c.quick_links.length : 0), 0);
const wSources  = pool.filter(c => Array.isArray(c.enrichment_sources) && c.enrichment_sources.length > 0).length;
const needsReview = pool.filter(c => c.needs_review === true).length;
const withWebsite = pool.filter(c => c.website && /^https?:\\/\\/[^\\/\\s]/i.test(c.website)).length;
const withFacebook = pool.filter(c => c.facebook).length;
const withYoutube = pool.filter(c => c.youtube).length;

console.log('=== MOOP Directory Pulse · scope: ' + scopeLabel + ' ===');
console.log('Total churches:           ' + total);
console.log('');
console.log('-- Data quality --');
console.log('  Real pastor (tight):    ' + realPastor + '  (' + pct(realPastor) + ')');
console.log('  Real website:           ' + withWebsite + '  (' + pct(withWebsite) + ')');
console.log('  Geocoded (lat/lng):     ' + geocoded + '  (' + pct(geocoded) + ')');
console.log('  With sources URL:       ' + wSources + '  (' + pct(wSources) + ')');
console.log('  needs_review flag:      ' + needsReview + '  (' + pct(needsReview) + ')');
console.log('');
console.log('-- Visual identity --');
console.log('  Hero photo (image_url): ' + withImage + '  (' + pct(withImage) + ')');
console.log('  Logo (image_thumb):     ' + withLogo + '  (' + pct(withLogo) + ')');
console.log('');
console.log('-- Engagement --');
console.log('  Quick-links:            ' + qLinks + '  (' + pct(qLinks) + ')  -> ' + qLinksTotal + ' total chips');
console.log('  Facebook URL:           ' + withFacebook + '  (' + pct(withFacebook) + ')');
console.log('  YouTube URL:            ' + withYoutube + '  (' + pct(withYoutube) + ')');

if (!scope) {
  console.log('');
  console.log('-- Network cross-listings --');
  for (const n of ['sbc','founders','9marks','tgc-cn','acts29','sgc','pillar-network','trinity-foundation']) {
    const c = arr.filter(x => Array.isArray(x.cross_listed_in) && x.cross_listed_in.includes(n)).length;
    console.log('  ' + n.padEnd(20) + c);
  }
}
"
