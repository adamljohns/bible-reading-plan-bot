#!/usr/bin/env node
//
// classify-logos.js — measure each scraped church logo so the directory can
// render it professionally instead of as a blank white box.
//
// The white-box bug: a logo that is white (or very light) on a transparent
// background is invisible on the page's white logo chip. And a wide wordmark
// logo crammed into an 86x86 square shrinks to an unreadable sliver. This tool
// downloads each church's image_thumb, uses sharp to compute the average
// brightness of the VISIBLE (non-transparent) pixels and the aspect ratio, and
// records:
//   image_thumb_lum    : 'light' | 'dark'   (light logos render on a dark chip)
//   image_thumb_aspect : width / height      (wide logos get a wide chip)
//   image_thumb_bad    : true                (essentially-empty/blank logo -> hide)
//
// Rendering (generate-church-pages.js) reads these. Re-run safely; it skips
// logos already classified unless --force.
//
// Usage: node scripts/classify-logos.js [--limit N] [--force] [--id <churchId>]

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const sharp = require('sharp');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i >= 0 && process.argv[i + 1] && !process.argv[i + 1].startsWith('--') ? process.argv[i + 1] : d; };
const LIMIT = parseInt(arg('limit', '100000'), 10);
const FORCE = process.argv.includes('--force');
const ONLY_ID = arg('id', null);
const CONCURRENCY = 8;
const LIGHT_THRESHOLD = 150; // avg luminance 0-255; above this the logo needs a dark chip

function download(url, redirects = 0) {
  return new Promise((resolve, reject) => {
    if (redirects > 4) return reject(new Error('too many redirects'));
    const lib = url.startsWith('http://') ? http : https;
    const req = lib.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Macintosh) MOOP-Directory/1.0', 'Accept': 'image/*' }, timeout: 15000 }, res => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        res.resume();
        const next = new URL(res.headers.location, url).href;
        return resolve(download(next, redirects + 1));
      }
      if (res.statusCode !== 200) { res.resume(); return reject(new Error('HTTP ' + res.statusCode)); }
      const chunks = [];
      let size = 0;
      res.on('data', c => { size += c.length; if (size > 12 * 1024 * 1024) { req.destroy(); reject(new Error('too large')); } else chunks.push(c); });
      res.on('end', () => resolve(Buffer.concat(chunks)));
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
  });
}

async function classify(buf) {
  const meta = await sharp(buf).metadata();
  const aspect = meta.width && meta.height ? +(meta.width / meta.height).toFixed(2) : 1;
  // Downscale to <=64px for a fast average, force RGBA so alpha is present.
  const { data, info } = await sharp(buf).resize(64, 64, { fit: 'inside', withoutEnlargement: true }).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  let lumWeighted = 0, alphaSum = 0, opaque = 0;
  const total = info.width * info.height;
  for (let i = 0; i < data.length; i += 4) {
    const a = data[i + 3];
    if (a < 24) continue; // treat near-transparent as background
    const lum = 0.2126 * data[i] + 0.7152 * data[i + 1] + 0.0722 * data[i + 2];
    lumWeighted += lum * a; alphaSum += a; opaque++;
  }
  const avgLum = alphaSum ? lumWeighted / alphaSum : 0;
  const opaqueFrac = total ? opaque / total : 0;
  // A logo with almost nothing opaque is blank/degenerate; hide it.
  const bad = opaqueFrac < 0.012;
  return { lum: avgLum >= LIGHT_THRESHOLD ? 'light' : 'dark', aspect, bad, avgLum: Math.round(avgLum), opaqueFrac: +opaqueFrac.toFixed(3), w: meta.width, h: meta.height };
}

async function main() {
  const data = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
  let queue = data.churches.filter(c => c.image_thumb && /^https?:/i.test(c.image_thumb));
  if (ONLY_ID) queue = queue.filter(c => String(c.id || c.slug) === ONLY_ID);
  else if (!FORCE) queue = queue.filter(c => !c.image_thumb_lum && !c.image_thumb_bad);
  queue = queue.slice(0, LIMIT);
  console.log('Logos to classify: ' + queue.length);
  if (!queue.length) { console.log('Nothing to do.'); return; }

  let done = 0, light = 0, dark = 0, badN = 0, fail = 0;
  let idx = 0;
  async function worker() {
    while (idx < queue.length) {
      const c = queue[idx++];
      try {
        const buf = await download(c.image_thumb);
        const r = await classify(buf);
        c.image_thumb_lum = r.lum;
        c.image_thumb_aspect = r.aspect;
        if (r.bad) { c.image_thumb_bad = true; badN++; } else { delete c.image_thumb_bad; }
        if (r.lum === 'light') light++; else dark++;
        if (ONLY_ID) console.log('  ' + c.id + ': lum=' + r.lum + ' (avg ' + r.avgLum + ') aspect=' + r.aspect + ' opaque=' + r.opaqueFrac + (r.bad ? ' BAD' : ''));
      } catch (e) {
        fail++;
        // leave unclassified so a later run can retry
      }
      done++;
      if (done % 100 === 0) console.log('  ' + done + '/' + queue.length + ' (light ' + light + ', dark ' + dark + ', bad ' + badN + ', fail ' + fail + ')');
    }
  }
  await Promise.all(Array.from({ length: CONCURRENCY }, worker));
  fs.writeFileSync(CHURCHES, JSON.stringify(data, null, 2) + '\n');
  console.log('Classified ' + done + ': ' + light + ' light, ' + dark + ' dark, ' + badN + ' blank/hidden, ' + fail + ' failed (left for retry).');
}

main().catch(e => { console.error(e); process.exit(1); });
