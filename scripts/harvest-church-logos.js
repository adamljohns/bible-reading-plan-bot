#!/usr/bin/env node
// harvest-church-logos.js — for churches that HAVE a website, harvest a logo/image URL
// from the church's OWN homepage into a SIDECAR file: docs/data/church-logos.json.
// churches.json is READ-ONLY here — the enrichment autopilot mutates it continuously,
// and the sidecar keeps this pipeline conflict-free (renderer wiring comes later).
//
// Candidate priority per church:
//   og:image → twitter:image → apple-touch-icon (largest) → <link rel="icon"> (largest,
//   prefer non-.ico) → header/nav <img> whose src/alt matches /logo/i.
// Relative URLs resolve against the FINAL homepage URL (after redirects). Every winner
// is VERIFIED — HEAD (ranged-GET fallback) must return 200 + image/* — and domain-
// guarded: a candidate on a different registrable domain than the church's site is
// rejected unless it lives on a known website-builder/asset CDN (wp.com, squarespace,
// wixstatic, cloudfront, imgix, fbcdn, wsimg …) — the Mosaic-Fort-Worth
// cross-contamination lesson from scrape-church-logos.js.
//
// Output shape (ASCII-only JSON, slugs sorted so diffs stay small; load-and-merge —
// prior finds are never clobbered):
//   {"generated":"<iso>","logos":{"<slug>":{"url":"…","kind":"og|touch|icon|img","page":"<final homepage url>"}}}
//
// Usage: node scripts/harvest-church-logos.js [--count 100] [--states VA,DC,MD]
//        [--match <name regex>] [--only-missing false] [--concurrency 3]
const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');

const arg = (k, d) => { const i = process.argv.indexOf(k); return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : d; };
const COUNT = parseInt(arg('--count', '100'), 10);
const ONLY_MISSING = arg('--only-missing', 'true') !== 'false';
const CONCURRENCY = Math.max(1, parseInt(arg('--concurrency', '3'), 10));
const MATCH = arg('--match', '');
const matchRe = MATCH ? new RegExp(MATCH, 'i') : null;
const STATES_F = (arg('--states', '') || '').toUpperCase().split(',').map(s => s.trim()).filter(Boolean);

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const SIDECAR = path.join(__dirname, '..', 'docs', 'data', 'church-logos.json');
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36 MOOP-Church-Directory/1.0';
const TIMEOUT_MS = 12_000;
const MAX_REDIRECTS = 4;
const MAX_VALIDATIONS = 6;     // candidates HEAD-checked per church before giving up
const POLITE_DELAY_MS = 300;   // pause per worker between churches (~3 workers)

const hasSite = c => typeof c.website === 'string' && /^https?:\/\//i.test(c.website);
const slugOf = c => String(c.slug || c.id || '');

// ---------------------------------------------------------------- state filter
// Addresses look like "9504 Selby Place, Norfolk Virginia, United States 23503" or
// "840 Mustang Dr, Grapevine, TX 76051" or "Detroit, MI" — the state (full name or
// abbrev) sits near the END, before optional country + zip. Strip trailing zip/country
// junk, then read the last token (abbrev) or a trailing full state name.
const STATES = { AL: 'alabama', AK: 'alaska', AZ: 'arizona', AR: 'arkansas', CA: 'california', CO: 'colorado', CT: 'connecticut', DE: 'delaware', FL: 'florida', GA: 'georgia', HI: 'hawaii', ID: 'idaho', IL: 'illinois', IN: 'indiana', IA: 'iowa', KS: 'kansas', KY: 'kentucky', LA: 'louisiana', ME: 'maine', MD: 'maryland', MA: 'massachusetts', MI: 'michigan', MN: 'minnesota', MS: 'mississippi', MO: 'missouri', MT: 'montana', NE: 'nebraska', NV: 'nevada', NH: 'new hampshire', NJ: 'new jersey', NM: 'new mexico', NY: 'new york', NC: 'north carolina', ND: 'north dakota', OH: 'ohio', OK: 'oklahoma', OR: 'oregon', PA: 'pennsylvania', RI: 'rhode island', SC: 'south carolina', SD: 'south dakota', TN: 'tennessee', TX: 'texas', UT: 'utah', VT: 'vermont', VA: 'virginia', WA: 'washington', WV: 'west virginia', WI: 'wisconsin', WY: 'wyoming', DC: 'district of columbia' };
const AB = new Set(Object.keys(STATES));
// Longest names first so "west virginia" wins over "virginia", "north carolina" over …
const NAMES_DESC = Object.entries(STATES).sort((a, b) => b[1].length - a[1].length);
function stateOfAddress(addr) {
  let a = String(addr || '').trim();
  for (let i = 0; i < 3; i++) {
    a = a.replace(/[\s,.;]+$/, '');
    a = a.replace(/\b\d{5}(?:-\d{4})?$/, '').replace(/[\s,.;]+$/, '');
    a = a.replace(/\b(?:united states(?: of america)?|u\.?s\.?a\.?|u\.?s\.?)$/i, '').replace(/[\s,.;]+$/, '');
  }
  const tok = (a.split(/[\s,]+/).pop() || '').replace(/\./g, '');
  if (/^[A-Z]{2}$/.test(tok) && AB.has(tok)) return tok;
  const low = a.toLowerCase();
  for (const [ab, full] of NAMES_DESC) if (low.endsWith(full)) return ab;
  return null;
}
const inStates = c => !STATES_F.length
  || STATES_F.includes(stateOfAddress(c.address) || '')
  || STATES_F.includes(String(c.state || '').toUpperCase().trim());

// ------------------------------------------------------------------- fetching
// Same helper pattern as find-church-websites.js: follow ANY 3xx+Location up to 4 hops
// (church sites almost always redirect http→https / →www), resolve relative Locations
// against the current URL, drain redirect bodies, never reject — resolve null instead.
// rejectUnauthorized:false because small-church SSL is chronically expired/misnamed.
// Returns { html, finalUrl } so relative candidates resolve against the REAL page.
function fetchPage(url, depth = 0) {
  return new Promise(resolve => {
    if (depth > MAX_REDIRECTS) return resolve(null);
    let done = false; const fin = v => { if (!done) { done = true; resolve(v); } };
    try {
      const lib = /^https:/i.test(url) ? https : http;
      const req = lib.get(url, { headers: { 'User-Agent': UA, 'Accept': 'text/html,*/*' }, rejectUnauthorized: false }, res => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          res.resume();
          let next; try { next = new URL(res.headers.location, url).href; } catch (_) { return fin(null); }
          return fetchPage(next, depth + 1).then(fin);
        }
        if (res.statusCode !== 200) { res.resume(); return fin(null); }
        let b = '';
        res.on('data', d => {
          b += d;
          if (b.length > 500000) { fin({ html: b, finalUrl: url }); req.destroy(); } // <head> is long gone by 500KB — keep what we have
        });
        res.on('end', () => fin({ html: b, finalUrl: url }));
      });
      req.on('error', () => fin(null));
      req.setTimeout(TIMEOUT_MS, () => req.destroy());
    } catch (_) { fin(null); }
  });
}

// Verify a candidate actually serves an image: HEAD → 200 + image/* (206 for the ranged
// fallback). Hosts that refuse HEAD (405/403/wrong-CT) get one ranged GET, headers only —
// we destroy the socket before the body arrives. Follows redirects like fetchPage.
// "SVG served as text/html" (and every other non-image/*) fails here by construction.
function checkImage(url, method = 'HEAD', depth = 0) {
  return new Promise(resolve => {
    if (depth > MAX_REDIRECTS) return resolve(null);
    let done = false; const fin = v => { if (!done) { done = true; resolve(v); } };
    try {
      const lib = /^https:/i.test(url) ? https : http;
      const headers = { 'User-Agent': UA, 'Accept': 'image/*,*/*' };
      if (method === 'GET') headers.Range = 'bytes=0-0';
      const req = lib.request(url, { method, headers, rejectUnauthorized: false }, res => {
        const sc = res.statusCode;
        if (sc >= 300 && sc < 400 && res.headers.location) {
          res.resume();
          let next; try { next = new URL(res.headers.location, url).href; } catch (_) { return fin(null); }
          return checkImage(next, method, depth + 1).then(fin);
        }
        const ct = String(res.headers['content-type'] || '').split(';')[0].trim().toLowerCase();
        const pass = (sc === 200 || sc === 206) && ct.startsWith('image/');
        res.resume();
        if (pass) { fin({ ok: true, contentType: ct }); req.destroy(); return; }
        if (method === 'HEAD' && sc !== 404 && sc !== 410) return checkImage(url, 'GET', depth).then(fin); // HEAD-hostile host? one ranged retry
        fin(null); req.destroy();
      });
      req.on('error', () => { if (method === 'HEAD') checkImage(url, 'GET', depth).then(fin); else fin(null); });
      req.setTimeout(TIMEOUT_MS, () => req.destroy());
      req.end();
    } catch (_) { fin(null); }
  });
}

// ------------------------------------------------------------------ extraction
const attr = (tag, name) => {
  const m = tag.match(new RegExp('(?:^|[\\s"\'/])' + name + '\\s*=\\s*(?:"([^"]*)"|\'([^\']*)\'|([^\\s"\'>]+))', 'i'));
  const v = m ? (m[1] !== undefined ? m[1] : (m[2] !== undefined ? m[2] : m[3])) : null;
  return v === null || v === undefined ? null : v.trim();
};
const decodeEntities = s => String(s)
  .replace(/&amp;/gi, '&').replace(/&#0*38;/g, '&').replace(/&#x0*26;/gi, '&')
  .replace(/&quot;/gi, '"').replace(/&#0*39;/g, "'").replace(/&#x0*2f;/gi, '/');
const largestSize = sizes => Math.max(0, ...String(sizes || '').split(/\s+/).map(s => parseInt(s, 10) || 0));
const lastSrcset = ss => { const parts = String(ss || '').split(',').map(p => p.trim().split(/\s+/)[0]).filter(Boolean); return parts.length ? parts[parts.length - 1] : null; };

// Candidates in strict priority order (spec): og → twitter → touch → icon → header img.
function extractCandidates(html, baseUrl) {
  const out = []; const seen = new Set();
  const add = (raw, kind) => {
    if (!raw) return;
    const cleaned = decodeEntities(raw).trim();
    if (!cleaned || /^data:/i.test(cleaned) || /^javascript:/i.test(cleaned)) return; // data: URIs are never harvested
    let abs; try { abs = new URL(cleaned, baseUrl).href; } catch (_) { return; }
    if (!/^https?:\/\//i.test(abs) || seen.has(abs)) return;
    seen.add(abs); out.push({ url: abs, kind });
  };

  // 1+2: social preview metas (property= or name=, either attribute order)
  const ogs = [], twitters = [];
  for (const tag of html.match(/<meta\b[^>]*>/gi) || []) {
    const key = ((attr(tag, 'property') || attr(tag, 'name')) || '').toLowerCase().trim();
    const content = attr(tag, 'content');
    if (!content) continue;
    if (key === 'og:image' || key === 'og:image:url' || key === 'og:image:secure_url') ogs.push(content);
    else if (key === 'twitter:image' || key === 'twitter:image:src') twitters.push(content);
  }
  ogs.forEach(u => add(u, 'og'));
  twitters.forEach(u => add(u, 'og'));

  // 3+4: touch icons (largest first) then rel=icon (prefer non-.ico, then largest)
  const touch = [], icons = [];
  for (const tag of html.match(/<link\b[^>]*>/gi) || []) {
    const rel = (attr(tag, 'rel') || '').toLowerCase();
    const href = attr(tag, 'href');
    if (!href) continue;
    const size = largestSize(attr(tag, 'sizes'));
    if (/apple-touch-icon/.test(rel)) touch.push({ href, size });
    else if (/(^|\s)(shortcut )?icon(\s|$)/.test(rel) || /mask-icon/.test(rel)) icons.push({ href, size, ico: /\.ico(\?|$)/i.test(href) ? 1 : 0 });
  }
  touch.sort((a, b) => b.size - a.size).forEach(t => add(t.href, 'touch'));
  icons.sort((a, b) => (a.ico - b.ico) || (b.size - a.size)).forEach(i => add(i.href, 'icon'));

  // 5: header/nav <img> whose src or alt smells like a logo
  const headerRegion = ((html.match(/<header[\s\S]{0,8000}?<\/header>/i) || [''])[0])
    + ((html.match(/<nav[\s\S]{0,8000}?<\/nav>/i) || [''])[0]);
  for (const tag of headerRegion.match(/<img\b[^>]*>/gi) || []) {
    const src = attr(tag, 'src') || attr(tag, 'data-src') || attr(tag, 'data-lazy-src') || lastSrcset(attr(tag, 'srcset'));
    if (!src) continue;
    const alt = attr(tag, 'alt') || '';
    if (/logo/i.test(src) || /logo/i.test(alt)) add(src, 'img');
  }
  return out;
}

// ------------------------------------------------------------------ the guards
// Registrable-domain check (naive last-two-labels, same as scrape-church-logos.js —
// fine for the .com/.org world US churches live in). Candidates on a foreign domain
// are cross-contamination risk UNLESS the host is a website-builder/asset CDN that
// legitimately serves the site's own images.
function rootDomain(u) {
  try { return new URL(u).hostname.replace(/^www\./, '').split('.').slice(-2).join('.').toLowerCase(); }
  catch (_) { return null; }
}
const CDN_OK = /(^|\.)(wp\.com|wordpress\.com|squarespace-cdn\.com|squarespace\.com|sqspcdn\.com|wixstatic\.com|wix\.com|parastorage\.com|cloudfront\.net|imgix\.net|fbcdn\.net|cdninstagram\.com|wsimg\.com|secureservercdn\.net|godaddysites\.com|googleusercontent\.com|ggpht\.com|gstatic\.com|amazonaws\.com|b-cdn\.net|cloudinary\.com|editmysite\.com|weebly\.com|weeblycloud\.com|jimcdn\.com|nucleuschurch\.com|nucleus-cdn\.com|cdn-website\.com|dudaone\.com|snappages\.site|showit\.co|sg-host\.com|kxcdn\.com|netdna-ssl\.com|rackcdn\.com|akamaized\.net|twimg\.com|subsplash\.com|churchcenter\.com|thechurchco\.com|ekklesia360\.com|faithlife\.com|sitecdn\.com|websitebuilder\.com|1and1\.com|ionos\.space|shopify\.com|nitrocdn\.com|sirv\.com|imagekit\.io|netlify\.app|vercel\.app|githubusercontent\.com)$/i;
// URLs that smell like tracking pixels / analytics beacons, never logos.
const TRACKING = /(^|\/)(pixel|spacer|blank|clear|transparent|beacon|track(ing)?)\.(gif|png)(\?|$)|\b1x1\b|facebook\.com\/tr\b|google-analytics\.|googletagmanager\.|doubleclick\.|quantserve\.|scorecardresearch\.|bat\.bing\.|px\.ads\./i;
// CMS-default favicons / template junk (from scrape-church-logos.js) — a Squarespace
// default favicon or gravatar is not "the church's logo" even though it validates.
const TEMPLATE_JUNK = /assets\.squarespace\.com\/universal\/default|parastorage\.com\/client\/pfavico|wp-includes\/images\/favicon|gravatar\.com\/avatar|placeholder|\/wp-content\/plugins\//i;
// Domain-parking / for-sale landers. An expired church domain redirects HERE, so the
// parking page becomes the "final URL" and its og:image sails through the domain guard
// (the christ-covenant-chesapeake HugeDomains case). If the homepage lands on one of
// these, the site is dead — harvest nothing.
const PARKED = /hugedomains\.com|domainmarket\.com|buydomains\.com|sedo(parking)?\.com|\bdan\.com|afternic\.|parkingcrew\.|\bbodis\.com|parklogic\.|above\.com|park-web\.godaddy|godaddy\.com\/domainsearch|domainnamesales|uniregistry|squadhelp\.|brandbucket\.|dynadot\.com|expireddomains|snapnames|dropcatch\.com|namebright\.com|domain(sponsor|activate)/i;

async function harvestOne(c) {
  const page = await fetchPage(c.website);
  if (!page || !page.html) return { status: 'fetch-failed' };
  if (PARKED.test(page.finalUrl)) return { status: 'parked' };
  const siteRoot = rootDomain(page.finalUrl);
  const cands = extractCandidates(page.html, page.finalUrl);
  if (!cands.length) return { status: 'no-candidates' };
  let tried = 0, foreign = 0;
  for (const cand of cands) {
    if (tried >= MAX_VALIDATIONS) break;
    if (TRACKING.test(cand.url) || TEMPLATE_JUNK.test(cand.url) || PARKED.test(cand.url)) continue;
    const croot = rootDomain(cand.url);
    let chost = ''; try { chost = new URL(cand.url).hostname; } catch (_) { continue; }
    if (croot !== siteRoot && !CDN_OK.test(chost)) { foreign++; continue; }
    tried++;
    const v = await checkImage(cand.url);
    if (v && v.ok) return { status: 'found', url: cand.url, kind: cand.kind, page: page.finalUrl };
  }
  return { status: (foreign && !tried) ? 'domain-rejected' : 'not-validated' };
}

// ------------------------------------------------------------------ sidecar IO
function loadSidecar() {
  if (!fs.existsSync(SIDECAR)) return {};
  try { return JSON.parse(fs.readFileSync(SIDECAR, 'utf8')).logos || {}; }
  catch (e) { console.error(`! could not parse existing ${SIDECAR}: ${e.message} — refusing to clobber`); process.exit(1); }
}
// ASCII-only, one line per slug, slugs sorted — small stable diffs.
function writeSidecar(logos) {
  const slugs = Object.keys(logos).sort();
  const lines = ['{', `"generated": ${JSON.stringify(new Date().toISOString())},`, '"logos": {'];
  slugs.forEach((s, i) => {
    const e = logos[s];
    lines.push(` ${JSON.stringify(s)}: ${JSON.stringify({ url: e.url, kind: e.kind, page: e.page })}${i < slugs.length - 1 ? ',' : ''}`);
  });
  lines.push('}', '}', '');
  const text = lines.join('\n').replace(/[\u007f-\uffff]/g, ch => '\\u' + ch.charCodeAt(0).toString(16).padStart(4, '0'));
  JSON.parse(text); // self-check: never write a sidecar the renderer can't parse
  fs.writeFileSync(SIDECAR, text);
}

// ------------------------------------------------------------------------ main
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8')); // READ ONLY — never written back
  const prior = loadSidecar();
  const logos = { ...prior };

  const eligible = d.churches.filter(c => hasSite(c) && slugOf(c)
    && (!matchRe || matchRe.test(String(c.name || '')))
    && inStates(c)
    && (!ONLY_MISSING || !prior[slugOf(c)]))
    .sort((a, b) => slugOf(a).localeCompare(slugOf(b)))
    .slice(0, COUNT);

  console.log(`Logo harvest — ${eligible.length} churches (states: ${STATES_F.join(',') || 'all'}, only-missing: ${ONLY_MISSING}, prior sidecar entries: ${Object.keys(prior).length})\n`);
  const stats = { attempted: 0, found: 0, byKind: { og: 0, touch: 0, icon: 0, img: 0 }, skipped: {} };
  let sinceFlush = 0, doneN = 0;

  await Promise.all(Array.from({ length: Math.min(CONCURRENCY, eligible.length) }, async () => {
    while (eligible.length) {
      const c = eligible.shift();
      stats.attempted++;
      const r = await harvestOne(c);
      const n = ++doneN;
      if (r.status === 'found') {
        stats.found++; stats.byKind[r.kind]++;
        logos[slugOf(c)] = { url: r.url, kind: r.kind, page: r.page };
        console.log(`  ✓ [${n}] ${slugOf(c)} [${r.kind}] ${r.url.slice(0, 90)}`);
        if (++sinceFlush >= 25) { sinceFlush = 0; writeSidecar(logos); } // crash-safe checkpoint
      } else {
        stats.skipped[r.status] = (stats.skipped[r.status] || 0) + 1;
        console.log(`  – [${n}] ${slugOf(c)} (${r.status})`);
      }
      await sleep(POLITE_DELAY_MS);
    }
  }));

  if (stats.found) writeSidecar(logos);
  const pct = stats.attempted ? (100 * stats.found / stats.attempted).toFixed(1) : '0.0';
  console.log(`\nAttempted ${stats.attempted} | found ${stats.found} (og ${stats.byKind.og}, touch ${stats.byKind.touch}, icon ${stats.byKind.icon}, img ${stats.byKind.img}) | skipped ${stats.attempted - stats.found} ${JSON.stringify(stats.skipped)}`);
  console.log(`Hit-rate: ${pct}% | sidecar now ${Object.keys(logos).length} logos → ${SIDECAR}`);
})();
