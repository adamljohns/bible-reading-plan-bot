#!/usr/bin/env node
// "Which churches did I drive by?" — match a travel route against the directory's
// geocoded churches and report every church you passed within a given radius.
//
// Source-agnostic: feed it any of these and it extracts the lat/lng breadcrumb —
//   • GPX            (.gpx)   — <trkpt>/<wpt>/<rtept> from any GPS logger / Apple Shortcut
//   • Google Takeout (.json)  — Records.json (latitudeE7/longitudeE7) OR the newer
//                               Timeline/Semantic export (recursively scraped)
//   • CSV            (.csv)   — "lat,lng[,iso-time]" per line
//
// Usage:
//   node scripts/churches-near-route.js <route-file> [--radius 400] [--out trip.json] [--rating green,yellow]
//
//   --radius   meters; how close counts as "drove by" (default 400 ≈ ¼ mile)
//   --out      also write full results as JSON
//   --rating   only report churches with these overall_ratings (comma list)
//
// Everything runs locally — your location file never leaves the machine.

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const file = args.find((a) => !a.startsWith('--'));
const opt = (name, def) => { const i = args.indexOf('--' + name); return i >= 0 ? args[i + 1] : def; };
const RADIUS = parseFloat(opt('radius', '400'));
const OUT = opt('out', null);
const RATINGS = (opt('rating', '') || '').split(',').map((s) => s.trim()).filter(Boolean);

if (!file) {
  console.error('Usage: node scripts/churches-near-route.js <route.gpx|.json|.csv> [--radius 400] [--out trip.json] [--rating green,yellow]');
  process.exit(1);
}

// ---- extract route breadcrumb as [{lat, lng, t?}] from whatever format ----
function extractPoints(filePath) {
  const raw = fs.readFileSync(filePath, 'utf8');
  const ext = path.extname(filePath).toLowerCase();
  const pts = [];
  const push = (lat, lng, t) => {
    lat = +lat; lng = +lng;
    if (Number.isFinite(lat) && Number.isFinite(lng) && Math.abs(lat) <= 90 && Math.abs(lng) <= 180 && (lat || lng)) pts.push({ lat, lng, t });
  };

  if (ext === '.gpx' || raw.trimStart().startsWith('<')) {
    // attribute order varies (lat before lon or after) — capture both
    const re = /<(?:trkpt|wpt|rtept)\b[^>]*?\blat="(-?[\d.]+)"[^>]*?\blon="(-?[\d.]+)"|<(?:trkpt|wpt|rtept)\b[^>]*?\blon="(-?[\d.]+)"[^>]*?\blat="(-?[\d.]+)"/g;
    let m;
    while ((m = re.exec(raw))) push(m[1] ?? m[4], m[2] ?? m[3]);
    return pts;
  }
  if (ext === '.csv' || (!raw.trimStart().startsWith('{') && !raw.trimStart().startsWith('['))) {
    for (const line of raw.split(/\r?\n/)) {
      const c = line.split(',');
      if (c.length >= 2 && /^-?[\d.]+$/.test(c[0].trim())) push(c[0], c[1], c[2]);
    }
    return pts;
  }
  // JSON — recursively scrape any coordinate shape Google (or anything) uses.
  const data = JSON.parse(raw);
  (function walk(node) {
    if (!node || typeof node !== 'object') {
      if (typeof node === 'string') {
        let g = node.match(/geo:(-?[\d.]+),(-?[\d.]+)/) || node.match(/^\s*(-?[\d.]+)°?\s*,\s*(-?[\d.]+)°?\s*$/);
        if (g) push(g[1], g[2]);
      }
      return;
    }
    if ('latitudeE7' in node && 'longitudeE7' in node) push(node.latitudeE7 / 1e7, node.longitudeE7 / 1e7, node.timestamp || node.timestampMs);
    else if ('latitude' in node && 'longitude' in node && typeof node.latitude === 'number') push(node.latitude, node.longitude, node.timestamp);
    else if ('lat' in node && ('lng' in node || 'lon' in node) && typeof node.lat === 'number') push(node.lat, node.lng ?? node.lon, node.time);
    for (const k of Object.keys(node)) walk(node[k]);
  })(data);
  return pts;
}

// ---- haversine (meters) ----
const R = 6371000, rad = (d) => (d * Math.PI) / 180;
function dist(aLat, aLng, bLat, bLng) {
  const dLat = rad(bLat - aLat), dLng = rad(bLng - aLng);
  const x = Math.sin(dLat / 2) ** 2 + Math.cos(rad(aLat)) * Math.cos(rad(bLat)) * Math.sin(dLng / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(x));
}

const route = extractPoints(path.resolve(file));
if (!route.length) { console.error('No coordinates found in ' + file + ' — is it a GPX / Google Takeout / lat,lng CSV?'); process.exit(1); }

// ---- grid-index the geocoded churches so we don't compare every point to all 28k ----
const d = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'docs', 'data', 'churches.json'), 'utf8'));
let geo = d.churches.filter((c) => c && c.latitude != null && c.longitude != null);
if (RATINGS.length) geo = geo.filter((c) => RATINGS.includes(c.overall_rating));
const CELL = 0.02; // ~2.2 km cells
const key = (la, ln) => Math.floor(la / CELL) + ':' + Math.floor(ln / CELL);
const grid = new Map();
for (const c of geo) { const k = key(+c.latitude, +c.longitude); (grid.get(k) || grid.set(k, []).get(k)).push(c); }
const span = Math.ceil(RADIUS / (CELL * 111320)) + 1; // cells to scan around each route point

// ---- for each route point, find nearby churches; keep each church's closest approach ----
const hits = new Map(); // id -> { church, meters, t }
for (const p of route) {
  const cLa = Math.floor(p.lat / CELL), cLn = Math.floor(p.lng / CELL);
  for (let i = -span; i <= span; i++) for (let j = -span; j <= span; j++) {
    const bucket = grid.get((cLa + i) + ':' + (cLn + j));
    if (!bucket) continue;
    for (const c of bucket) {
      const m = dist(p.lat, p.lng, +c.latitude, +c.longitude);
      if (m <= RADIUS) {
        const prev = hits.get(c.id);
        if (!prev || m < prev.meters) hits.set(c.id, { church: c, meters: m, t: p.t });
      }
    }
  }
}

// ---- report ----
const fmtT = (t) => { if (t == null) return ''; const n = Number(t); const iso = Number.isFinite(n) && String(t).length >= 10 ? new Date(n < 1e12 ? n * 1000 : n).toISOString() : String(t); return iso.slice(0, 16).replace('T', ' '); };
const found = [...hits.values()].sort((a, b) => a.meters - b.meters);
const mi = (m) => (m / 1609.34).toFixed(2);

console.log(`\nRoute: ${route.length.toLocaleString()} points · radius ${RADIUS} m (${mi(RADIUS)} mi) · ${geo.length.toLocaleString()} geocoded churches scanned${RATINGS.length ? ' (' + RATINGS.join('/') + ' only)' : ''}`);
console.log(`Churches you passed: ${found.length}\n`);
for (const h of found.slice(0, 60)) {
  const c = h.church;
  const where = [c.city, c.state].filter(Boolean).join(', ');
  console.log(`  ${String(Math.round(h.meters)).padStart(4)} m  ${(c.overall_rating || '?').padEnd(6)} ${c.name}${where ? ' — ' + where : ''}${h.t ? '  [' + fmtT(h.t) + ']' : ''}`);
  console.log(`          https://usmcmin.org/churches/${c.id}.html`);
}
if (found.length > 60) console.log(`  …and ${found.length - 60} more (use --out to write them all)`);

if (OUT) {
  const rows = found.map((h) => ({ id: h.church.id, name: h.church.name, city: h.church.city, state: h.church.state, rating: h.church.overall_rating, meters: Math.round(h.meters), nearest_time: h.t ? fmtT(h.t) : null, url: `https://usmcmin.org/churches/${h.church.id}.html` }));
  fs.writeFileSync(OUT, JSON.stringify(rows, null, 2));
  console.log(`\nWrote ${rows.length} churches to ${OUT}`);
}
console.log('');
