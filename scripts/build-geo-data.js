#!/usr/bin/env node
// Build the two static geo tables behind the "City, State or ZIP" church lookup:
//
//   docs/data/geo/zcta-centroids.json  — 5-digit ZIP (ZCTA) -> [lat, lng]  (~33k)
//   docs/data/geo/places.json          — ["Houston","TX",29.786,-95.389]   (~32k)
//
// Source: U.S. Census Bureau national Gazetteer files (PUBLIC DOMAIN), e.g.
//   https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2025_Gazetteer/2025_Gaz_zcta_national.zip
//   https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2025_Gazetteer/2025_Gaz_place_national.zip
// Pipe-delimited; coordinates are the INTPTLAT/INTPTLONG internal points.
//
// The outputs are committed; the raw gazetteer txts are NOT (rebuild is a
// once-a-year affair when the Census refreshes the gazetteer).
//
// Usage: node scripts/build-geo-data.js <Gaz_zcta_national.txt> <Gaz_place_national.txt>

const fs = require('fs');
const path = require('path');

const [zctaTxt, placeTxt] = process.argv.slice(2);
if (!zctaTxt || !placeTxt) {
  console.error('usage: node scripts/build-geo-data.js <Gaz_zcta_national.txt> <Gaz_place_national.txt>');
  process.exit(1);
}

const REPO_ROOT = path.resolve(__dirname, '..');
const OUT_DIR = path.join(REPO_ROOT, 'docs/data/geo');
fs.mkdirSync(OUT_DIR, { recursive: true });

// Repo canon: data files are ASCII-escaped (Puerto Rico place names carry ñ/á).
const esc = s => s.replace(/[^\x00-\x7F]/g, ch => '\\u' + ch.charCodeAt(0).toString(16).padStart(4, '0'));
const TODAY = new Date().toISOString().slice(0, 10);
const round3 = n => Math.round(parseFloat(n) * 1000) / 1000; // ~110 m — plenty for radius search

const rows = f => fs.readFileSync(f, 'utf8').split('\n').slice(1).map(l => l.replace(/\s+$/, '')).filter(Boolean).map(l => l.split('|'));

// ── ZCTA centroids ───────────────────────────────────────────────────────────
// GEOID|GEOIDFQ|ALAND|AWATER|ALAND_SQMI|AWATER_SQMI|INTPTLAT|INTPTLONG
const zcta = {};
for (const r of rows(zctaTxt)) {
  const zip = r[0];
  if (!/^\d{5}$/.test(zip)) continue;
  zcta[zip] = [round3(r[6]), round3(r[7])];
}

// ── Places ───────────────────────────────────────────────────────────────────
// USPS|GEOID|GEOIDFQ|ANSICODE|NAME|LSAD|FUNCSTAT|ALAND|AWATER|ALAND_SQMI|AWATER_SQMI|INTPTLAT|INTPTLONG
// NAME carries a lowercase legal designator suffix ("Abbeville city", "Abanda CDP");
// strip it CASE-SENSITIVELY so real names survive ("Carson City" keeps its City,
// "Boise City city" -> "Boise City"). Balance-of-county entries strip "(balance)".
const SUFFIX = / (city|town|village|borough|municipality|comunidad|zona urbana|census area|city and borough|consolidated government|metropolitan government|metro government|metro township|unified government|urban county|charter township|township|plantation|gore|grant|location|purchase|reservation|CDP)$/;
const cleanName = n => {
  n = n.replace(/ \(balance\)$/i, '').trim();
  const m = n.match(SUFFIX);
  return m ? n.slice(0, m.index).trim() : n;
};

// One entry per (name, state): a handful of states carry e.g. both a "X city" and
// an adjacent "X CDP" — keep the larger by land area (the one people mean).
const best = new Map();
for (const r of rows(placeTxt)) {
  const st = r[0], name = cleanName(r[4]), aland = parseInt(r[7], 10) || 0;
  const lat = round3(r[11]), lng = round3(r[12]);
  if (!name || !isFinite(lat) || !isFinite(lng)) continue;
  const key = name.toLowerCase() + '|' + st;
  const prev = best.get(key);
  if (!prev || aland > prev.aland) best.set(key, { name, st, lat, lng, aland });
}
// 5th element = land area in sq mi (1 dp) — the autocomplete's prominence rank, so
// "fredericksburg" suggests Fredericksburg VA (10.5 sq mi city) above the same-named
// 1-sq-mi towns that used to win on state-alphabetical order.
const places = [...best.values()]
  .sort((a, b) => a.name.localeCompare(b.name) || a.st.localeCompare(b.st))
  .map(p => [p.name, p.st, p.lat, p.lng, Math.round(p.aland / 2589988.11 * 10) / 10]);

fs.writeFileSync(path.join(OUT_DIR, 'zcta-centroids.json'),
  esc(JSON.stringify({ updated: TODAY, source: 'US Census Gazetteer (public domain)', zcta })));
fs.writeFileSync(path.join(OUT_DIR, 'places.json'),
  esc(JSON.stringify({ updated: TODAY, source: 'US Census Gazetteer (public domain)', places })));

const kb = f => (fs.statSync(path.join(OUT_DIR, f)).size / 1024).toFixed(0);
console.log(`✅ zcta-centroids.json — ${Object.keys(zcta).length} ZIPs, ${kb('zcta-centroids.json')} KB`);
console.log(`✅ places.json — ${places.length} places, ${kb('places.json')} KB`);
