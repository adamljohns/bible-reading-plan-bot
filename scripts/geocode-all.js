#!/usr/bin/env node
//
// geocode-all.js — robust nationwide geocoder for the MOOP Church Directory.
//
// Strategy (best coverage per the 2026-06-01 findings):
//   1. normalizeAddress() — 'Virginia'->'VA', strip 'United States', fix commas
//   2. Census BATCH endpoint (fast, free, bulk up to ~1000/req) for the chunk
//   3. Census ONE-LINE endpoint for batch no-matches (catches format edge cases)
//   4. OpenStreetMap Nominatim for the residual (better local-street coverage,
//      rate-limited to 1 req/sec per their usage policy)
//
// Processes ONE chunk per invocation (default 400 churches) so it plays nicely
// with an autopilot loop that commits between chunks. Resume-safe: only touches
// churches missing lat/lng that have a street address.
//
// Usage:
//   node geocode-all.js                 # next 400 ungeocoded (street-address) churches, nationwide
//   node geocode-all.js --count 1000    # bigger chunk
//   node geocode-all.js --state VA      # scope to a state
//   node geocode-all.js --no-nominatim  # skip the slow Nominatim residual pass
//

const fs = require('fs');
const path = require('path');
const https = require('https');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');

const STATE_ABBR = {
  alabama:'AL',alaska:'AK',arizona:'AZ',arkansas:'AR',california:'CA',colorado:'CO',
  connecticut:'CT',delaware:'DE',florida:'FL',georgia:'GA',hawaii:'HI',idaho:'ID',
  illinois:'IL',indiana:'IN',iowa:'IA',kansas:'KS',kentucky:'KY',louisiana:'LA',
  maine:'ME',maryland:'MD',massachusetts:'MA',michigan:'MI',minnesota:'MN',
  mississippi:'MS',missouri:'MO',montana:'MT',nebraska:'NE',nevada:'NV',
  'new hampshire':'NH','new jersey':'NJ','new mexico':'NM','new york':'NY',
  'north carolina':'NC','north dakota':'ND',ohio:'OH',oklahoma:'OK',oregon:'OR',
  pennsylvania:'PA','rhode island':'RI','south carolina':'SC','south dakota':'SD',
  tennessee:'TN',texas:'TX',utah:'UT',vermont:'VT',virginia:'VA',washington:'WA',
  'west virginia':'WV',wisconsin:'WI',wyoming:'WY','district of columbia':'DC'
};

function normalizeAddress(addr) {
  if (!addr) return addr;
  let s = String(addr);
  s = s.replace(/,?\s*United States of America\b/gi, '');
  s = s.replace(/,?\s*United States\b/gi, '');
  s = s.replace(/,?\s*USA\b/g, '');
  const names = Object.keys(STATE_ABBR).sort((a,b)=>b.length-a.length);
  for (const name of names) {
    const re = new RegExp('\\b' + name.replace(/ /g,'\\s+') + '\\b', 'i');
    if (re.test(s)) { s = s.replace(re, STATE_ABBR[name]); break; }
  }
  s = s.replace(/([a-z])\s+([A-Z]{2})(\s+\d{5})/g, '$1, $2$3');
  s = s.replace(/,\s*,/g, ',').replace(/\s{2,}/g, ' ').trim().replace(/,\s*$/, '');
  return s;
}

function parseAddress(addr) {
  if (!addr) return null;
  addr = normalizeAddress(addr);
  const m = addr.match(/^(.+?),\s*([A-Z][a-zA-Z\s\.\-']+?),\s*([A-Z]{2})(?:\s+(\d{5}))?(?:-\d{4})?\b/);
  if (m) {
    const [, street, city, state, zip] = m;
    if (!/\d/.test(street)) return { street:'', city:street.trim(), state, zip:zip||'' };
    return { street: street.trim(), city: city.trim(), state, zip: zip || '' };
  }
  return null;
}

function parseArgs() {
  const out = { count: 400, state: null, nominatim: true };
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--count') out.count = parseInt(a[++i], 10);
    else if (a[i] === '--state') out.state = a[++i].toUpperCase();
    else if (a[i] === '--no-nominatim') out.nominatim = false;
  }
  return out;
}

function inUSBounds(lat, lng) {
  return lat >= 17 && lat <= 72 && lng >= -180 && lng <= -64;
}

// --- Census batch endpoint (multipart form upload of a CSV) ---
function censusBatch(rows) {
  // rows: [{id, street, city, state, zip}]
  const csv = rows.map(r => [r.id, r.street, r.city, r.state, r.zip].map(v => {
    v = String(v == null ? '' : v);
    return /[",\n]/.test(v) ? '"' + v.replace(/"/g,'""') + '"' : v;
  }).join(',')).join('\n') + '\n';

  const boundary = '----MOOPGeo' + rows.length + 'x' + (rows[0] ? rows[0].id : '0');
  const parts = [
    Buffer.from('--' + boundary + '\r\nContent-Disposition: form-data; name="addressFile"; filename="a.csv"\r\nContent-Type: text/csv\r\n\r\n'),
    Buffer.from(csv),
    Buffer.from('\r\n--' + boundary + '\r\nContent-Disposition: form-data; name="benchmark"\r\n\r\nPublic_AR_Current\r\n--' + boundary + '--\r\n'),
  ];
  const body = Buffer.concat(parts);

  return new Promise(resolve => {
    const req = https.request('https://geocoding.geo.census.gov/geocoder/locations/addressbatch', {
      method: 'POST',
      headers: { 'Content-Type': 'multipart/form-data; boundary=' + boundary, 'Content-Length': body.length },
      timeout: 120000,
    }, res => {
      let s = '';
      res.on('data', c => s += c);
      res.on('end', () => {
        const out = {};
        for (const line of s.split('\n').filter(Boolean)) {
          // "id","input","Match|No_Match","Exact|...","matched","lon,lat",...
          const m = line.match(/^"([^"]*)","[^"]*","(Match|Tie|No_Match)"(?:,"([^"]*)","([^"]*)","([^"]*)")?/);
          if (!m) continue;
          const [, id, status, , , lonlat] = m;
          if (status === 'Match' && lonlat) {
            const [lon, lat] = lonlat.split(',').map(parseFloat);
            if (isFinite(lat) && isFinite(lon)) out[id] = { lat, lng: lon };
          }
        }
        resolve(out);
      });
    });
    req.on('error', () => resolve({}));
    req.on('timeout', () => { req.destroy(); resolve({}); });
    req.write(body);
    req.end();
  });
}

function censusOneline(addr) {
  return new Promise(resolve => {
    const url = 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=' + encodeURIComponent(addr) + '&benchmark=Public_AR_Current&format=json';
    https.get(url, { timeout: 20000 }, r => {
      let s = ''; r.on('data', c => s += c); r.on('end', () => {
        try { const j = JSON.parse(s); const m = j.result.addressMatches; resolve(m[0] ? { lat: m[0].coordinates.y, lng: m[0].coordinates.x } : null); }
        catch (e) { resolve(null); }
      });
    }).on('error', () => resolve(null)).on('timeout', function(){ this.destroy(); resolve(null); });
  });
}

function nominatim(addr) {
  return new Promise(resolve => {
    const url = 'https://nominatim.openstreetmap.org/search?format=json&limit=1&countrycodes=us&q=' + encodeURIComponent(addr);
    https.get(url, { headers: { 'User-Agent': 'MOOP-Church-Directory/1.0 (usmcmin.org church mapping)' }, timeout: 20000 }, r => {
      let s = ''; r.on('data', c => s += c); r.on('end', () => {
        try { const j = JSON.parse(s); resolve(j[0] ? { lat: parseFloat(j[0].lat), lng: parseFloat(j[0].lon) } : null); }
        catch (e) { resolve(null); }
      });
    }).on('error', () => resolve(null)).on('timeout', function(){ this.destroy(); resolve(null); });
  });
}

async function main() {
  const args = parseArgs();
  const data = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));

  // Build the work queue: ungeocoded churches with a parseable street address
  // that have NOT already failed a full geocode attempt (so the autopilot does
  // not spin on the same un-geocodable residual every tick).
  const queue = [];
  for (const c of data.churches) {
    if (typeof c.latitude === 'number' && typeof c.longitude === 'number') continue;
    if (c._geocode_failed) continue;
    if (args.state && !new RegExp(',\\s*' + args.state + '\\b').test(normalizeAddress(c.address || ''))) continue;
    const p = parseAddress(c.address);
    if (!p || !p.street) continue;
    queue.push({ church: c, parsed: p, id: String(c.id || c.slug) });
  }
  const chunk = queue.slice(0, args.count);
  console.log('Ungeocoded street-address churches: ' + queue.length + ' (processing ' + chunk.length + ' this run)');
  if (!chunk.length) { console.log('Nothing to do.'); return; }

  const byId = new Map(chunk.map(t => [t.id, t]));
  let placed = 0;

  // Phase 1: Census batch
  console.log('Phase 1: Census batch ...');
  const batchRows = chunk.map(t => ({ id: t.id, street: t.parsed.street, city: t.parsed.city, state: t.parsed.state, zip: t.parsed.zip }));
  const batchOut = await censusBatch(batchRows);
  for (const [id, coord] of Object.entries(batchOut)) {
    const t = byId.get(id);
    if (t && inUSBounds(coord.lat, coord.lng)) { t.church.latitude = coord.lat; t.church.longitude = coord.lng; t.church.geocode_source = 'census-batch'; t.done = true; placed++; }
  }
  console.log('  batch placed ' + placed);

  // Phase 2: Census one-line for batch misses
  const miss1 = chunk.filter(t => !t.done);
  console.log('Phase 2: Census one-line for ' + miss1.length + ' misses ...');
  for (const t of miss1) {
    const r = await censusOneline(normalizeAddress(t.church.address));
    if (r && inUSBounds(r.lat, r.lng)) { t.church.latitude = r.lat; t.church.longitude = r.lng; t.church.geocode_source = 'census-oneline'; t.done = true; placed++; }
    await new Promise(s => setTimeout(s, 250));
  }
  console.log('  total placed ' + placed);

  // Phase 3: Nominatim residual
  if (args.nominatim) {
    const miss2 = chunk.filter(t => !t.done);
    console.log('Phase 3: Nominatim for ' + miss2.length + ' residual ...');
    for (const t of miss2) {
      const r = await nominatim(normalizeAddress(t.church.address));
      if (r && inUSBounds(r.lat, r.lng)) { t.church.latitude = r.lat; t.church.longitude = r.lng; t.church.geocode_source = 'nominatim'; t.done = true; placed++; }
      await new Promise(s => setTimeout(s, 1100)); // respect 1 req/sec
    }
  }

  // Mark churches that failed every geocoder this run as _geocode_failed, but
  // ONLY when Nominatim was part of the chain (a full attempt). With
  // --no-nominatim we leave them unmarked so a later Nominatim pass can try.
  let marked = 0;
  if (args.nominatim) {
    for (const t of chunk) {
      if (!t.done) { t.church._geocode_failed = true; marked++; }
    }
  }

  fs.writeFileSync(CHURCHES, JSON.stringify(data, null, 2) + '\n');
  console.log('\nPlaced ' + placed + ' / ' + chunk.length + ' this run' + (marked ? (', marked ' + marked + ' as failed') : '') + '. ' + (queue.length - chunk.length) + ' street-address churches still queued.');
}

main().catch(e => { console.error(e); process.exit(1); });
