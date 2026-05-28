#!/usr/bin/env node
// scripts/scrape-church-images.js
//
// Visit each church's website and extract the image they chose to represent
// themselves — the og:image meta tag, with twitter:image as fallback and the
// apple-touch-icon as a square thumbnail backup.
//
// Stores back to churches.json as:
//   image_url   — main hero (og:image, twitter:image)
//   image_thumb — square thumb (apple-touch-icon)
//   image_source— 'website-og', 'website-twitter', 'website-touch-icon', or null
//   image_fetched_at
//
// Polite: 3s delay between requests, single connection, custom User-Agent.
// Crash-safe: writes churches.json every 25 records so a kill loses minimal work.
//
// Usage:
//   node scripts/scrape-church-images.js --state VA            # default, 1 state
//   node scripts/scrape-church-images.js --state VA --count 20 # cap fetches
//   node scripts/scrape-church-images.js --state all           # all states
//   node scripts/scrape-church-images.js --refetch             # ignore image_url; refetch all

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const { URL } = require('url');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const UA = 'Mozilla/5.0 (compatible; USMCMinistriesBot/1.0; +https://usmcmin.org/about.html) Image-fetcher for MOOP Church Directory';
const DELAY_MS = 3000;
const SAVE_EVERY = 25;
const FETCH_TIMEOUT_MS = 20_000;

function parseArgs() {
  const out = { state: 'VA', count: null, refetch: false, jsonl: null };
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--state') out.state = a[++i].toUpperCase();
    else if (a[i] === '--count') out.count = parseInt(a[++i], 10);
    else if (a[i] === '--refetch') out.refetch = true;
    // --jsonl <path> : RACE-FREE MODE. Results append to JSONL; churches.json
    // is read-only (only to build the queue). Use with merge-image-scrapes.js.
    else if (a[i] === '--jsonl') out.jsonl = a[++i];
  }
  return out;
}

function fetchHead(url, maxRedirects = 3) {
  return new Promise((resolve, reject) => {
    let resolved = false;
    function tryUrl(u, redirectsLeft) {
      let parsedUrl;
      try { parsedUrl = new URL(u); } catch (e) { return reject(new Error('BAD_URL')); }
      const lib = parsedUrl.protocol === 'http:' ? http : https;
      const req = lib.get(u, {
        headers: { 'User-Agent': UA, 'Accept': 'text/html,*/*' },
        timeout: FETCH_TIMEOUT_MS,
      }, res => {
        if ([301, 302, 303, 307, 308].includes(res.statusCode)) {
          if (redirectsLeft <= 0) return reject(new Error('REDIRECT_LIMIT'));
          const next = res.headers.location;
          if (!next) return reject(new Error('REDIRECT_NO_LOC'));
          const nextUrl = new URL(next, u).href;
          res.resume();
          return tryUrl(nextUrl, redirectsLeft - 1);
        }
        if (res.statusCode !== 200) return reject(new Error(`HTTP_${res.statusCode}`));
        // Read up to 200KB of the response — that's plenty for <head>
        let body = '';
        let size = 0;
        const MAX = 200_000;
        res.on('data', chunk => {
          if (resolved) return;
          size += chunk.length;
          body += chunk.toString('utf8');
          // Stop reading once we have the closing </head>
          if (body.length > 4000 && /<\/head>/i.test(body)) {
            resolved = true;
            res.destroy();
            resolve({ html: body, finalUrl: u });
            return;
          }
          if (size > MAX) {
            resolved = true;
            res.destroy();
            resolve({ html: body, finalUrl: u });
          }
        });
        res.on('end', () => { if (!resolved) { resolved = true; resolve({ html: body, finalUrl: u }); } });
      });
      req.on('error', e => { if (!resolved) { resolved = true; reject(e); } });
      req.on('timeout', () => { if (!resolved) { resolved = true; req.destroy(); reject(new Error('TIMEOUT')); } });
    }
    tryUrl(url, maxRedirects);
  });
}

function extractMeta(html, finalUrl) {
  // Match meta tags by property/name attributes in any order
  function metaContent(attr, key) {
    const rx = new RegExp(`<meta[^>]+${attr}=["']${key}["'][^>]+content=["']([^"']+)["']`, 'i');
    const m = html.match(rx);
    if (m) return m[1];
    // Try reversed order: content first, then property
    const rx2 = new RegExp(`<meta[^>]+content=["']([^"']+)["'][^>]+${attr}=["']${key}["']`, 'i');
    const m2 = html.match(rx2);
    return m2 ? m2[1] : null;
  }
  function linkHref(rel) {
    const rx = new RegExp(`<link[^>]+rel=["']${rel}["'][^>]+href=["']([^"']+)["']`, 'i');
    const m = html.match(rx);
    if (m) return m[1];
    const rx2 = new RegExp(`<link[^>]+href=["']([^"']+)["'][^>]+rel=["']${rel}["']`, 'i');
    const m2 = html.match(rx2);
    return m2 ? m2[1] : null;
  }
  function resolve(url) {
    if (!url) return null;
    try { return new URL(url, finalUrl).href; } catch (e) { return null; }
  }
  // Drop CMS-default favicons + dataURIs + obvious "not a real church image" artifacts.
  // These give the false impression of having a unique image when they're shared templates.
  function clean(u) {
    if (!u) return null;
    if (u.startsWith('data:')) return null;
    const low = u.toLowerCase();
    const cmsDefaults = [
      'assets.squarespace.com/universal/default',
      'parastorage.com/client/pfavico',
      'parastorage.com/services/santa-resources',
      'wix.com/media/site-icon',
      'wp-content/themes/.*?/favicon',
      'wp-includes/images/favicon',
    ];
    for (const pat of cmsDefaults) { if (new RegExp(pat).test(low)) return null; }
    return u;
  }
  return {
    og:        clean(resolve(metaContent('property', 'og:image')) || resolve(metaContent('name', 'og:image'))),
    twitter:   clean(resolve(metaContent('name', 'twitter:image')) || resolve(metaContent('property', 'twitter:image'))),
    touchIcon: clean(resolve(linkHref('apple-touch-icon')) || resolve(linkHref('apple-touch-icon-precomposed')) || resolve(linkHref('icon'))),
  };
}

async function main() {
  const args = parseArgs();
  const jsonlMode = !!args.jsonl;
  console.log(`Loading ${CHURCHES} ...`);
  const data = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));

  // In JSONL mode, build a Set of already-processed church IDs so we resume
  // cleanly across autopilot ticks without re-fetching the same churches.
  const alreadyDone = new Set();
  if (jsonlMode && fs.existsSync(args.jsonl)) {
    const lines = fs.readFileSync(args.jsonl, 'utf8').split('\n').filter(Boolean);
    for (const l of lines) {
      try { const r = JSON.parse(l); if (r.id) alreadyDone.add(r.id); } catch (e) {}
    }
    console.log(`JSONL mode: ${alreadyDone.size} church IDs already in ${args.jsonl}`);
  }

  const stateFilter = args.state === 'ALL' ? null : args.state;
  const todo = [];
  for (const c of data.churches) {
    if (stateFilter && !new RegExp(`,\\s*${stateFilter}\\b`).test(c.address || '')) continue;
    const cid = c.id || c.slug;
    if (jsonlMode) {
      // JSONL mode: skip records already in our JSONL output (resume-safe).
      if (alreadyDone.has(cid)) continue;
      // Also skip records that ALREADY have an image (legacy churches.json data
      // from the pre-refactor scrape — no point re-fetching).
      if (!args.refetch && (c.image_url || c.image_thumb || c.image_fetched_at)) continue;
    } else {
      // Legacy mode (churches.json direct-write): skip records that have an image.
      if (!args.refetch && (c.image_url || c.image_thumb)) continue;
    }
    if (!c.website || !/^https?:/i.test(c.website)) continue;
    todo.push(c);
  }
  // Fredericksburg-first priority sort within whatever state scope is in effect.
  todo.sort((a, b) => {
    const af = /Fredericksburg/i.test(a.address || '') ? 0 : 1;
    const bf = /Fredericksburg/i.test(b.address || '') ? 0 : 1;
    return af - bf;
  });
  if (args.count) todo.splice(args.count);
  console.log(`State filter: ${stateFilter || 'ALL'}`);
  console.log(`Records to fetch: ${todo.length}`);
  console.log(`Polite delay: ${DELAY_MS}ms — est ${(todo.length * (DELAY_MS+1000) / 60000).toFixed(1)} min`);
  if (jsonlMode) console.log(`JSONL output: ${args.jsonl} (churches.json will NOT be modified — use merge-image-scrapes.js)`);
  if (!todo.length) { console.log('Nothing to do.'); return; }

  let ok = 0, fail = 0, foundOg = 0, foundTwitter = 0, foundTouch = 0;
  const start = Date.now();

  // In JSONL mode, write a result line per outcome and DO NOT mutate the
  // in-memory church record. In legacy mode, mutate c directly + periodic save.
  function emit(c, result) {
    if (jsonlMode) {
      fs.appendFileSync(args.jsonl, JSON.stringify({ id: c.id || c.slug, ...result }) + '\n');
      return;
    }
    Object.assign(c, result);
    // On refetch, explicitly clear stale fields if the new result didn't supply them
    if (args.refetch) {
      if (!('image_url'   in result)) delete c.image_url;
      if (!('image_thumb' in result)) delete c.image_thumb;
    }
  }

  for (let i = 0; i < todo.length; i++) {
    const c = todo[i];
    if (i > 0) await new Promise(r => setTimeout(r, DELAY_MS));
    process.stdout.write(`[${i+1}/${todo.length}] ${c.name.slice(0,50).padEnd(50)} `);
    try {
      const { html, finalUrl } = await fetchHead(c.website);
      const m = extractMeta(html, finalUrl);
      const heroUrl = m.og || m.twitter || null;
      const source = m.og ? 'website-og' : m.twitter ? 'website-twitter' : null;
      const result = { image_fetched_at: new Date().toISOString() };
      if (heroUrl) {
        result.image_url = heroUrl;
        result.image_source = source;
        if (m.og) foundOg++;
        else if (m.twitter) foundTwitter++;
      }
      if (m.touchIcon) {
        result.image_thumb = m.touchIcon;
        foundTouch++;
      }
      if (heroUrl || m.touchIcon) {
        emit(c, result);
        ok++;
        const got = [heroUrl ? (m.og?'og':'tw') : null, m.touchIcon ? 'tch' : null].filter(Boolean).join('+');
        console.log(`OK [${got}]`);
      } else {
        // Page was reachable but had no usable image at all
        result.image_url = null;
        result.image_thumb = null;
        result.image_source = 'website-no-image';
        emit(c, result);
        fail++;
        console.log(`no-image`);
      }
    } catch (e) {
      // Network error / DNS / timeout / cert / redirect-loop / etc.
      // Mark attempted-and-failed so autopilot doesn't infinite-retry.
      emit(c, {
        image_fetched_at: new Date().toISOString(),
        image_source: 'fetch-failed:' + (e.message || 'unknown').slice(0, 60),
        image_url: null,
        image_thumb: null,
      });
      fail++;
      console.log(`FAIL ${e.message}`);
    }
    if (!jsonlMode && (i+1) % SAVE_EVERY === 0) {
      fs.writeFileSync(CHURCHES, JSON.stringify(data, null, 2));
      const elapsedMin = ((Date.now() - start) / 60000).toFixed(1);
      console.log(`  -- checkpoint saved (${i+1} done, ${ok} ok, ${fail} fail, ${elapsedMin}m elapsed) --`);
    }
  }
  if (!jsonlMode) {
    fs.writeFileSync(CHURCHES, JSON.stringify(data, null, 2));
  }
  console.log(`\nDone. ${ok} ok / ${fail} fail. ${foundOg} og + ${foundTwitter} twitter + ${foundTouch} touch-icon.`);
  if (jsonlMode) console.log(`Run merge-image-scrapes.js to apply ${ok+fail} results from ${args.jsonl} to churches.json.`);
}

main().catch(e => { console.error(e); process.exit(1); });
