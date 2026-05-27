#!/usr/bin/env node
// scripts/geocode-va.js
//
// Geocode every VA church in docs/data/churches.json using the US Census
// Geocoder's batch API (free, US-only, no API key required).
//
// The batch endpoint accepts a CSV of up to 10,000 records per request and
// returns a CSV of matches. We chunk into 500-record requests to stay well
// under the limit.
//
// Writes `latitude` and `longitude` fields back to each matched record,
// plus `geocoded_at` and `geocode_source` for the audit trail.
//
// Usage:
//   node scripts/geocode-va.js                # geocode VA only
//   node scripts/geocode-va.js --state TX     # any single state
//   node scripts/geocode-va.js --state all    # all 50 states (slow)
//
// Re-runs are safe — already-geocoded records are skipped unless --force.

const fs = require('fs');
const path = require('path');
const https = require('https');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');

function parseArgs() {
  const out = { state: 'VA', force: false, chunkSize: 500 };
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--state') out.state = a[++i].toUpperCase();
    else if (a[i] === '--force') out.force = true;
    else if (a[i] === '--chunk') out.chunkSize = parseInt(a[++i], 10);
  }
  return out;
}

function csvEscape(s) {
  if (s == null) return '';
  const str = String(s);
  if (/[",\n]/.test(str)) return '"' + str.replace(/"/g, '""') + '"';
  return str;
}

// Parse an address string like "500 Church St, Charlottesville, VA 22902"
// into Census-compatible components. Returns null if we can't extract enough.
function parseAddress(addr) {
  if (!addr) return null;
  // Patterns to handle:
  //   "200 Onville Rd, Stafford, VA 22556"
  //   "Stafford, VA 22556"  (no street)
  //   "Abingdon, VA 24210"
  //   "Charlottesville, VA"
  const m = addr.match(/^(.+?),\s*([A-Z][a-zA-Z\s\.\-']+?),\s*([A-Z]{2})(?:\s+(\d{5}))?(?:-\d{4})?\b/);
  if (m) {
    const [, street, city, state, zip] = m;
    // If the "street" part is really just the city (no number), treat it as city-only
    if (!/\d/.test(street)) {
      return { street: '', city: street.trim(), state, zip: zip || '' };
    }
    return { street: street.trim(), city: city.trim(), state, zip: zip || '' };
  }
  // City+state-only fallback
  const m2 = addr.match(/^([A-Z][a-zA-Z\s\.\-']+?),\s*([A-Z]{2})(?:\s+(\d{5}))?/);
  if (m2) return { street: '', city: m2[1].trim(), state: m2[2], zip: m2[3] || '' };
  return null;
}

function postCsv(url, csv, headers = {}) {
  return new Promise((resolve, reject) => {
    const boundary = '----geocode-' + Date.now();
    const body = Buffer.concat([
      Buffer.from(`--${boundary}\r\n`),
      Buffer.from(`Content-Disposition: form-data; name="addressFile"; filename="addresses.csv"\r\n`),
      Buffer.from(`Content-Type: text/csv\r\n\r\n`),
      Buffer.from(csv),
      Buffer.from(`\r\n--${boundary}\r\n`),
      Buffer.from(`Content-Disposition: form-data; name="benchmark"\r\n\r\n`),
      Buffer.from(`Public_AR_Current\r\n`),
      Buffer.from(`--${boundary}--\r\n`),
    ]);
    const u = new URL(url);
    const req = https.request({
      method: 'POST',
      hostname: u.hostname,
      path: u.pathname + u.search,
      headers: {
        'Content-Type': `multipart/form-data; boundary=${boundary}`,
        'Content-Length': body.length,
        ...headers,
      },
      timeout: 120_000,
    }, res => {
      if (res.statusCode !== 200) return reject(new Error(`HTTP ${res.statusCode}`));
      let buf = '';
      res.on('data', c => buf += c);
      res.on('end', () => resolve(buf));
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('TIMEOUT')); });
    req.write(body);
    req.end();
  });
}

// Census batch geocoder CSV format (no header):
//   Unique ID, Street address, City, State, ZIP
// Returns the same row plus match status, matched address, lat/lon, etc.
function parseGeocodeResponse(text) {
  // CSV with quoted fields; one row per input ID
  const out = {};
  const lines = text.split('\n').filter(Boolean);
  for (const line of lines) {
    // Simple CSV parse that handles quoted fields
    const cells = [];
    let cur = '', inQ = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (inQ) {
        if (ch === '"' && line[i+1] === '"') { cur += '"'; i++; }
        else if (ch === '"') inQ = false;
        else cur += ch;
      } else {
        if (ch === ',') { cells.push(cur); cur = ''; }
        else if (ch === '"') inQ = true;
        else cur += ch;
      }
    }
    cells.push(cur);
    if (cells.length < 6) continue;
    const [id, input, status, matchType, matchedAddr, lonLat] = cells;
    if (status === 'Match' && lonLat && lonLat.includes(',')) {
      const [lon, lat] = lonLat.split(',').map(parseFloat);
      out[id] = { lat, lon, matchedAddr, matchType };
    } else {
      out[id] = null;
    }
  }
  return out;
}

async function main() {
  const args = parseArgs();
  console.log(`Loading ${CHURCHES} ...`);
  const data = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));

  const stateFilter = args.state === 'ALL' ? null : args.state;
  const todo = [];
  for (const c of data.churches) {
    if (stateFilter) {
      if (!new RegExp(`,\\s*${stateFilter}\\b`).test(c.address || '')) continue;
    }
    if (!args.force && c.latitude && c.longitude) continue;
    const parsed = parseAddress(c.address);
    if (!parsed || parsed.state !== (stateFilter || parsed.state)) continue;
    if (!parsed.street && !parsed.zip) continue;  // need at least street or ZIP
    todo.push({ id: c.id || c.slug, parsed, ref: c });
  }
  console.log(`State filter: ${stateFilter || 'ALL'}`);
  console.log(`Records needing geocode: ${todo.length}`);
  if (todo.length === 0) { console.log('Nothing to do.'); return; }

  let geocoded = 0;
  let noMatch = 0;
  let chunkN = 0;
  for (let i = 0; i < todo.length; i += args.chunkSize) {
    chunkN++;
    const chunk = todo.slice(i, i + args.chunkSize);
    const csv = chunk.map(t =>
      [csvEscape(t.id), csvEscape(t.parsed.street), csvEscape(t.parsed.city),
       csvEscape(t.parsed.state), csvEscape(t.parsed.zip)].join(',')
    ).join('\n') + '\n';

    process.stdout.write(`[chunk ${chunkN}] posting ${chunk.length} records ... `);
    let resp;
    try {
      resp = await postCsv(
        'https://geocoding.geo.census.gov/geocoder/locations/addressbatch',
        csv
      );
    } catch (e) {
      console.log(`FAIL: ${e.message}`);
      continue;
    }
    const results = parseGeocodeResponse(resp);
    let chunkOk = 0, chunkMiss = 0;
    for (const t of chunk) {
      const r = results[t.id];
      if (r && r.lat && r.lon) {
        t.ref.latitude = r.lat;
        t.ref.longitude = r.lon;
        t.ref.geocoded_at = new Date().toISOString();
        t.ref.geocode_source = 'census';
        chunkOk++;
        geocoded++;
      } else {
        chunkMiss++;
        noMatch++;
      }
    }
    console.log(`${chunkOk} matched / ${chunkMiss} no-match`);
  }

  console.log(`\nWriting ${CHURCHES} (${geocoded} new coords, ${noMatch} no-match)`);
  fs.writeFileSync(CHURCHES, JSON.stringify(data, null, 2));
  console.log('Done.');
}

main().catch(e => { console.error(e); process.exit(1); });
