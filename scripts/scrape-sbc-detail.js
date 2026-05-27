#!/usr/bin/env node
// scripts/scrape-sbc-detail.js
//
// For every SBC church in churches.json with source_url=https://churches.sbc.net/...
// but missing website, refetch the SBC.net per-church page and extract:
//
//   - website URL (from <p class="heading__website"><a href="...">)
//   - latitude + longitude (from <div class="marker" data-lat="..." data-lng="...">)
//   - phone (from <p class="heading__phone">) when not already present
//
// Output: JSONL only (race-free; merge-sbc-detail.js applies to churches.json
// in a separate step, same pattern as image-autopilot-v2).
//
// Usage:
//   node scripts/scrape-sbc-detail.js --count 100 --jsonl /tmp/sbc-detail.jsonl
//   node scripts/scrape-sbc-detail.js                            (full crawl, default JSONL path)

const fs = require('fs');
const path = require('path');
const https = require('https');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const DEFAULT_JSONL = '/tmp/sbc-detail.jsonl';
const UA = 'Mozilla/5.0 (compatible; USMCMinistriesBot/1.0; +https://usmcmin.org/about.html) SBC.net detail crawler';
const DELAY_MS = 11_000; // SBC.net polite delay (same as original bulk scrape)
const FETCH_TIMEOUT_MS = 25_000;

function parseArgs() {
  const out = { count: null, jsonl: DEFAULT_JSONL };
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--count') out.count = parseInt(a[++i], 10);
    else if (a[i] === '--jsonl') out.jsonl = a[++i];
  }
  return out;
}

function fetchText(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { headers: { 'User-Agent': UA, 'Accept': 'text/html,*/*' }, timeout: FETCH_TIMEOUT_MS }, res => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        return reject(new Error(`Redirect ${res.statusCode}`));
      }
      if (res.statusCode !== 200) return reject(new Error(`HTTP_${res.statusCode}`));
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => resolve(body));
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('TIMEOUT')); });
  });
}

function parseDetail(html) {
  const out = {};
  // Website link
  const webM = html.match(/<p[^>]+class="heading__website"[^>]*>\s*<a[^>]+href="([^"]+)"/i);
  if (webM) out.website = webM[1];
  // Lat/lng
  const latM = html.match(/<div[^>]+class="[^"]*marker[^"]*"[^>]+data-lat="([\-0-9.]+)"[^>]+data-lng="([\-0-9.]+)"/i);
  if (latM) { out.latitude = parseFloat(latM[1]); out.longitude = parseFloat(latM[2]); }
  // Phone — extract digits-only pattern from heading__phone elements
  const phoneM = html.match(/<p[^>]+class="heading__phone"[^>]*>\s*([\(\)\d\-\s\.]+?)\s*<\/p>/i);
  if (phoneM) {
    const digits = phoneM[1].replace(/[^\d]/g, '');
    if (digits.length === 10) out.phone = phoneM[1].trim();
  }
  return out;
}

async function main() {
  const args = parseArgs();
  console.log(`Loading ${CHURCHES} ...`);
  const data = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));

  // Set of IDs already processed in JSONL
  const alreadyDone = new Set();
  if (fs.existsSync(args.jsonl)) {
    for (const l of fs.readFileSync(args.jsonl, 'utf8').split('\n').filter(Boolean)) {
      try { const r = JSON.parse(l); if (r.id) alreadyDone.add(r.id); } catch (e) {}
    }
    console.log(`Already in JSONL: ${alreadyDone.size}`);
  }

  // Build queue: SBC records with sbc.net source_url and missing website
  const todo = [];
  for (const c of data.churches) {
    if (!c.source_url || !c.source_url.includes('churches.sbc.net')) continue;
    const cid = c.id || c.slug;
    if (alreadyDone.has(cid)) continue;
    // Skip if record already has BOTH website and lat/lng — nothing to add
    const hasWebsite = c.website && /^https?:/i.test(c.website);
    const hasGeo = typeof c.latitude === 'number' && typeof c.longitude === 'number';
    if (hasWebsite && hasGeo) continue;
    todo.push(c);
  }
  if (args.count) todo.splice(args.count);
  console.log(`Records to fetch: ${todo.length}`);
  console.log(`Polite delay: ${DELAY_MS}ms — est ${(todo.length * (DELAY_MS+500) / 60000).toFixed(1)} min`);
  if (!todo.length) { console.log('Nothing to do.'); return; }

  let ok = 0, fail = 0, gotWebsite = 0, gotGeo = 0, gotPhone = 0;
  const start = Date.now();

  for (let i = 0; i < todo.length; i++) {
    const c = todo[i];
    if (i > 0) await new Promise(r => setTimeout(r, DELAY_MS));
    process.stdout.write(`[${i+1}/${todo.length}] ${c.name.slice(0,50).padEnd(50)} `);
    const cid = c.id || c.slug;
    try {
      const html = await fetchText(c.source_url);
      const detail = parseDetail(html);
      const result = { sbc_detail_fetched_at: new Date().toISOString() };
      if (detail.website) { result.website = detail.website; gotWebsite++; }
      if (typeof detail.latitude === 'number') { result.latitude = detail.latitude; result.longitude = detail.longitude; result.geocode_source = 'sbc.net'; gotGeo++; }
      if (detail.phone) { result.phone = detail.phone; gotPhone++; }
      fs.appendFileSync(args.jsonl, JSON.stringify({ id: cid, ...result }) + '\n');
      ok++;
      const got = [detail.website ? 'web' : null, detail.latitude ? 'geo' : null, detail.phone ? 'ph' : null].filter(Boolean).join('+') || 'no-data';
      console.log(`OK [${got}]`);
    } catch (e) {
      fs.appendFileSync(args.jsonl, JSON.stringify({ id: cid, sbc_detail_fetched_at: new Date().toISOString(), sbc_detail_error: e.message.slice(0,60) }) + '\n');
      fail++;
      console.log(`FAIL ${e.message}`);
    }
    if ((i+1) % 25 === 0) {
      const elapsedMin = ((Date.now() - start) / 60000).toFixed(1);
      console.log(`  -- progress: ${i+1} done · ${ok} ok / ${fail} fail · ${gotWebsite} websites, ${gotGeo} geo, ${gotPhone} phones · ${elapsedMin}m elapsed --`);
    }
  }
  console.log(`\nDone. ${ok} ok / ${fail} fail. ${gotWebsite} websites + ${gotGeo} geo + ${gotPhone} phones.`);
  console.log(`Run merge-sbc-detail.js to apply ${ok+fail} results to churches.json.`);
}

main().catch(e => { console.error(e); process.exit(1); });
