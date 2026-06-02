#!/usr/bin/env node
//
// geocode-recover.js — recover map pins for US churches whose address is real
// but mis-formatted so the standard parser/geocoder cannot read it (a missing
// comma between street and city, a spelled-out state next to the city, a
// trailing "United States", an inline PO box). These are genuine US churches
// that simply never made it onto the map for a punctuation reason.
//
// It repairs the address string (format only, never the actual street/city/
// state/zip), geocodes the repaired form via the Census batch endpoint, and on
// a US-bounds match writes both the cleaned address and the coordinates. A
// repaired address that does not geocode is left untouched (no harm, no guess).
//
// Safety: repairs are applied ONLY to churches that do not currently parse, so
// already-good records are never rewritten. The Census geocoder validates the
// result, so a bad repair simply yields no match.
//
// Usage: node scripts/geocode-recover.js [--limit 500] [--dry]

const fs = require('fs');
const path = require('path');
const https = require('https');
const { STATE_ABBR, normalizeAddress } = require('./lib/address-util');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const LIMIT = (() => { const i = process.argv.indexOf('--limit'); return i >= 0 ? parseInt(process.argv[i + 1], 10) : 1000; })();
const DRY = process.argv.includes('--dry');

const stateNames = Object.keys(STATE_ABBR).sort((a, b) => b.length - a.length);

const FOREIGN = /\b[A-Za-z]\d[A-Za-z]\s*\d[A-Za-z]\d\b|\b[A-Za-z]{1,2}\d[A-Za-z\d]?\s+\d[A-Za-z]{2}\b|,\s*(?:ON|QC|BC|AB|MB|SK|NS|NB|NL|PE)\b|\b(?:United Kingdom|Canada|Australia|New Zealand|India|Kenya|Nigeria|Romania|Germany|Netherlands|Philippines|Singapore|Uganda|Tanzania|Pakistan|Bangladesh|Ukraine|Switzerland|Ireland|Belgium|Austria|Hungary|Portugal|France|Italy|Spain|Mexico|Brazil|China|Japan|Korea|Nairobi|Dublin)\b/i;

function repair(addr) {
  let s = String(addr || '');
  s = s.replace(/,?\s*United States of America\b/gi, '').replace(/,?\s*United States\b/gi, '').replace(/,?\s*USA\b/g, '');
  s = s.replace(/,?\s*P\.?\s*O\.?\s*Box\s+\d+/gi, '');                 // drop inline PO box
  // spelled state -> abbr ONLY in state position (followed by optional comma + 5-digit zip or end), so street names like "Virginia Ave" stay intact
  for (const name of stateNames) {
    const re = new RegExp('\\b' + name.replace(/ /g, '\\s+') + '\\b(\\s*,?\\s*\\d{5}(?:-\\d{4})?\\s*|\\s*$)', 'i');
    if (re.test(s)) { s = s.replace(re, (m, tail) => STATE_ABBR[name] + tail); break; }
  }
  s = s.replace(/([a-zA-Z])\s+([A-Z]{2})(\s+\d{5}\b|\s*$)/, '$1, $2$3'); // comma between city and trailing state
  s = s.replace(/(\b(?:Blvd|Boulevard|Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Way|Court|Ct|Place|Pl|Highway|Hwy|Parkway|Pkwy|Circle|Cir|Trail|Trl|Terrace|Ter)\.?)\s+([A-Z][a-zA-Z]+)(,\s*[A-Z]{2}\b)/, '$1, $2$3'); // comma between street suffix and city
  s = s.replace(/,\s*,/g, ',').replace(/\s{2,}/g, ' ').trim().replace(/,\s*$/, '');
  return s;
}

function parseAddr(addr) {
  if (!addr) return null;
  addr = normalizeAddress(addr);
  const m = addr.match(/^(.+?),\s*([A-Z][a-zA-Z\s\.\-']+?),\s*([A-Z]{2})(?:\s+(\d{5}))?(?:-\d{4})?\b/);
  if (m) { const [, street, city, state, zip] = m; if (!/\d/.test(street)) return null; return { street: street.trim(), city: city.trim(), state, zip: zip || '' }; }
  return null;
}

function inUSBounds(lat, lng) { return lat >= 17 && lat <= 72 && lng >= -180 && lng <= -64; }

function censusBatch(rows) {
  const csv = rows.map(r => [r.id, r.street, r.city, r.state, r.zip].map(v => { v = String(v == null ? '' : v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }).join(',')).join('\n') + '\n';
  const boundary = '----MOOPRecover' + rows.length;
  const body = Buffer.concat([
    Buffer.from('--' + boundary + '\r\nContent-Disposition: form-data; name="addressFile"; filename="a.csv"\r\nContent-Type: text/csv\r\n\r\n'),
    Buffer.from(csv),
    Buffer.from('\r\n--' + boundary + '\r\nContent-Disposition: form-data; name="benchmark"\r\n\r\nPublic_AR_Current\r\n--' + boundary + '--\r\n'),
  ]);
  return new Promise(resolve => {
    const req = https.request('https://geocoding.geo.census.gov/geocoder/locations/addressbatch', { method: 'POST', headers: { 'Content-Type': 'multipart/form-data; boundary=' + boundary, 'Content-Length': body.length }, timeout: 120000 }, res => {
      let s = ''; res.on('data', c => s += c); res.on('end', () => {
        const out = {};
        for (const line of s.split('\n').filter(Boolean)) {
          const m = line.match(/^"([^"]*)","[^"]*","(Match|Tie|No_Match)"(?:,"([^"]*)","([^"]*)","([^"]*)")?/);
          if (!m) continue;
          const [, id, status, , , lonlat] = m;
          if (status === 'Match' && lonlat) { const [lon, lat] = lonlat.split(',').map(parseFloat); if (isFinite(lat) && isFinite(lon)) out[id] = { lat, lng: lon }; }
        }
        resolve(out);
      });
    });
    req.on('error', () => resolve({})); req.on('timeout', () => { req.destroy(); resolve({}); });
    req.write(body); req.end();
  });
}

async function main() {
  const data = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
  const hasStreet = s => (/\d+\s+[A-Za-z]/.test(s || '') || /^\d+\s+\d/.test(s || '')) && /,/.test(s || '');

  // Targets: no coords, has a digit, not failed, not foreign, NOT currently
  // parseable, but parseable after repair.
  const targets = [];
  for (const c of data.churches) {
    if (typeof c.latitude === 'number' && typeof c.longitude === 'number') continue;
    if (c._geocode_failed) continue;
    if (!/\d/.test(c.address || '')) continue;
    if (FOREIGN.test(c.address || '')) continue;
    if (parseAddr(c.address)) continue;            // autopilot already handles these
    const fixed = repair(c.address);
    const p = parseAddr(fixed);
    if (p && p.street) targets.push({ church: c, id: String(c.id || c.slug), fixed, parsed: p });
    if (targets.length >= LIMIT) break;
  }
  console.log('Recoverable (repair makes parseable): ' + targets.length);
  if (DRY) { targets.slice(0, 20).forEach(t => console.log('  ' + t.church.address + '  =>  ' + t.fixed)); return; }
  if (!targets.length) { console.log('Nothing to recover.'); return; }

  const byId = new Map(targets.map(t => [t.id, t]));
  let placed = 0;
  for (let i = 0; i < targets.length; i += 300) {
    const chunk = targets.slice(i, i + 300);
    const out = await censusBatch(chunk.map(t => ({ id: t.id, street: t.parsed.street, city: t.parsed.city, state: t.parsed.state, zip: t.parsed.zip })));
    for (const [id, coord] of Object.entries(out)) {
      const t = byId.get(id);
      if (t && inUSBounds(coord.lat, coord.lng)) {
        t.church.address = t.fixed;                // write the cleaned address
        t.church.latitude = coord.lat; t.church.longitude = coord.lng;
        t.church.geocode_source = 'census-recover';
        placed++;
      }
    }
    console.log('  batch ' + (i / 300 + 1) + ': placed ' + placed + ' / ' + Math.min(i + 300, targets.length));
  }
  fs.writeFileSync(CHURCHES, JSON.stringify(data, null, 2) + '\n');
  console.log('Recovered + mapped ' + placed + ' churches (cleaned address + coordinates).');
}

main().catch(e => { console.error(e); process.exit(1); });
