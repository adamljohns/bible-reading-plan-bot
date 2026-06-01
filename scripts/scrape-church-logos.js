#!/usr/bin/env node
//
// scrape-church-logos.js — find a church's REAL header logo, not just its
// apple-touch-icon (which is often a favicon-quality square that looks bad
// rendered at 86px on the profile page).
//
// Strategy, in priority order:
//   1. <img> in <header>/<nav> whose class/id/src/alt contains "logo"
//   2. any <img> whose src/alt/class contains "logo" sitewide
//   3. og:image ONLY if it looks like a logo (small, square-ish, has "logo")
//   4. apple-touch-icon as last resort (existing behavior)
//
// Critically: every candidate URL's domain is checked against the church's
// own website domain. A logo served from a DIFFERENT root domain (the
// Mosaic-Fort-Worth cross-contamination case) is REJECTED unless it is a
// known asset CDN for the site's platform. This prevents wrong-church logos.
//
// Race-free JSONL pattern. Writes { id, logo_url, logo_source, logo_rejected }.
//
// Usage:
//   node scrape-church-logos.js --state VA --count 50 --jsonl /tmp/logo-scrapes.jsonl
//   node scrape-church-logos.js --church faith-baptist-church-fredericksburg
//

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const DEFAULT_JSONL = '/tmp/logo-scrapes.jsonl';
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36 MOOP-Church-Directory/1.0';
const FETCH_TIMEOUT_MS = 15_000;
const POLITE_DELAY_MS = 1500;

// Known asset CDNs + website-builder hosts that legitimately serve a church's
// OWN logo even though the hostname differs from the church's primary domain.
// A logo found inside the church's own site header that resolves to one of
// these is the church's logo by definition; only a logo on a DIFFERENT
// organization's primary domain (e.g. another church's WordPress site) is
// treated as cross-contamination.
const CDN_OK = /squarespace-cdn|squarespace\.com|googleusercontent|ggpht|cloudinary|thechurchco|wixstatic|wix\.com|parastorage|wp\.com|gstatic|amazonaws|cloudfront|imgix|nucleus-cdn|cdn-website|showit\.co|snappages\.site|sg-host\.com|subsplash|churchcenter|getnetset|clover\.com|faithlife|ekklesia360|cloudfront\.net|b-cdn\.net|files\.|\bcdn\d*\./i;

// CMS-default favicons / template junk we never want as a "logo"
const TEMPLATE_JUNK = /assets\.squarespace\.com\/universal\/default|parastorage\.com\/client\/pfavico|wp-includes\/images\/favicon|gravatar\.com\/avatar|\/favicon\.(ico|png)(\?|$)|cropped-favicon/i;

function parseArgs() {
  const out = { state: null, church: null, count: null, jsonl: DEFAULT_JSONL, refetch: false };
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--state') out.state = a[++i].toUpperCase();
    else if (a[i] === '--church') out.church = a[++i];
    else if (a[i] === '--count') out.count = parseInt(a[++i], 10);
    else if (a[i] === '--jsonl') out.jsonl = a[++i];
    else if (a[i] === '--refetch') out.refetch = true;
  }
  return out;
}

function fetchText(url, redirects = 0) {
  return new Promise((resolve, reject) => {
    let u;
    try { u = new URL(url); } catch (e) { return reject(new Error('BAD_URL')); }
    const lib = u.protocol === 'http:' ? http : https;
    const req = lib.get(url, { headers: { 'User-Agent': UA, 'Accept': 'text/html,*/*' }, timeout: FETCH_TIMEOUT_MS }, res => {
      if ((res.statusCode === 301 || res.statusCode === 302 || res.statusCode === 308) && res.headers.location && redirects < 4) {
        return resolve(fetchText(new URL(res.headers.location, u).href, redirects + 1).then(r => ({ ...r })));
      }
      if (res.statusCode !== 200) return reject(new Error('HTTP_' + res.statusCode));
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => resolve({ html: body, finalUrl: res.responseUrl || url }));
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('TIMEOUT')); });
  });
}

function rootDomain(u) {
  try {
    const h = new URL(u).hostname.replace(/^www\./, '');
    const parts = h.split('.');
    return parts.slice(-2).join('.');
  } catch (e) { return null; }
}

// Extract candidate logo URLs from HTML, ranked best-first.
function extractLogoCandidates(html, baseUrl) {
  const candidates = [];
  const resolve = (u) => { try { return new URL(u, baseUrl).href; } catch (e) { return null; } };

  // Grab the <header>...</header> and <nav>...</nav> regions (first of each)
  const headerMatch = html.match(/<header[\s\S]{0,4000}?<\/header>/i);
  const navMatch = html.match(/<nav[\s\S]{0,4000}?<\/nav>/i);
  const headerRegion = (headerMatch ? headerMatch[0] : '') + (navMatch ? navMatch[0] : '');

  // Pattern A: <img> with "logo" in any attribute, inside header/nav (best)
  const imgRe = /<img\b[^>]*>/gi;
  function scoreImgTag(tag, inHeader) {
    const srcM = tag.match(/\bsrc\s*=\s*["']([^"']+)["']/i) || tag.match(/\bdata-src\s*=\s*["']([^"']+)["']/i);
    if (!srcM) return null;
    const src = resolve(srcM[1]);
    if (!src) return null;
    const low = (tag + ' ' + src).toLowerCase();
    let score = 0;
    if (/logo/.test(low)) score += 10;
    if (inHeader) score += 5;
    if (/\.svg(\?|$)/i.test(src)) score += 3;     // SVG logos are crisp
    if (/header|brand|site-?title|navbar/.test(low)) score += 2;
    if (/icon|favicon|sprite|spinner|loading|placeholder|avatar/.test(low)) score -= 8;
    if (/banner|hero|slide|background|bg-/.test(low)) score -= 4;
    return { src, score };
  }

  let m;
  while ((m = imgRe.exec(headerRegion)) !== null) {
    const s = scoreImgTag(m[0], true);
    if (s && s.score > 0) candidates.push(s);
  }
  // Also scan the whole doc for "logo" imgs (lower base score)
  imgRe.lastIndex = 0;
  while ((m = imgRe.exec(html)) !== null) {
    const s = scoreImgTag(m[0], false);
    if (s && s.score >= 8) candidates.push(s);  // require the "logo" keyword sitewide
  }

  // De-dup by URL, keep highest score
  const byUrl = new Map();
  for (const c of candidates) {
    if (TEMPLATE_JUNK.test(c.src)) continue;
    const prev = byUrl.get(c.src);
    if (!prev || c.score > prev.score) byUrl.set(c.src, c);
  }
  return [...byUrl.values()].sort((a, b) => b.score - a.score);
}

async function scrapeOne(church) {
  const website = church.website;
  if (!website || !/^https?:\/\/[^\/\s]/i.test(website)) {
    return { id: church.id || church.slug, logo_url: null, logo_source: 'no-website' };
  }
  const churchRoot = rootDomain(website);
  let html, finalUrl;
  try {
    const r = await fetchText(website);
    html = r.html; finalUrl = r.finalUrl || website;
  } catch (e) {
    return { id: church.id || church.slug, logo_url: null, logo_source: 'fetch-failed:' + (e.message || '').slice(0,30) };
  }

  const candidates = extractLogoCandidates(html, finalUrl);
  // Pick the best candidate whose domain matches the church (or is a known CDN)
  for (const cand of candidates) {
    const cd = rootDomain(cand.src);
    const domainOk = (cd === churchRoot) || CDN_OK.test(cand.src);
    if (domainOk) {
      return { id: church.id || church.slug, logo_url: cand.src, logo_source: 'header-logo', logo_score: cand.score, scanned_at: new Date().toISOString() };
    }
  }
  // No domain-safe header logo found
  const rejected = candidates.length > 0 ? candidates[0].src : null;
  return { id: church.id || church.slug, logo_url: null, logo_source: 'no-safe-logo', logo_rejected: rejected, scanned_at: new Date().toISOString() };
}

async function main() {
  const args = parseArgs();
  const data = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));

  const done = new Set();
  if (fs.existsSync(args.jsonl)) {
    for (const l of fs.readFileSync(args.jsonl, 'utf8').split('\n').filter(Boolean)) {
      try { done.add(JSON.parse(l).id); } catch (e) {}
    }
    console.log('Already in JSONL: ' + done.size);
  }

  let pool = data.churches;
  if (args.church) pool = pool.filter(c => (c.id || c.slug) === args.church);
  else if (args.state) pool = pool.filter(c => new RegExp(',\\s*' + args.state + '\\b').test(c.address || ''));
  pool = pool.filter(c => c.website && /^https?:\/\/[^\/\s]/i.test(c.website));
  pool = pool.filter(c => !done.has(c.id || c.slug));
  // Fredericksburg-first
  pool.sort((a, b) => (/Fredericksburg/i.test(a.address||'')?0:1) - (/Fredericksburg/i.test(b.address||'')?0:1));
  if (args.count) pool = pool.slice(0, args.count);

  console.log('Churches to scan for header logos: ' + pool.length);
  if (!pool.length) { console.log('Nothing to do.'); return; }

  let found = 0, none = 0;
  for (let i = 0; i < pool.length; i++) {
    const c = pool[i];
    if (i > 0) await new Promise(r => setTimeout(r, POLITE_DELAY_MS));
    process.stdout.write('[' + (i+1) + '/' + pool.length + '] ' + (c.name||'').slice(0,40).padEnd(40) + ' ');
    const r = await scrapeOne(c);
    fs.appendFileSync(args.jsonl, JSON.stringify(r) + '\n');
    if (r.logo_url) { found++; console.log('OK (score ' + r.logo_score + ') ' + r.logo_url.slice(0,60)); }
    else { none++; console.log(r.logo_source + (r.logo_rejected ? ' [rejected ' + rootDomain(r.logo_rejected) + ']' : '')); }
  }

  console.log('\nDone. ' + found + ' header logos found / ' + none + ' none. JSONL: ' + args.jsonl);
  console.log('Merge with: node scripts/merge-logo-scrapes.js ' + args.jsonl);
}

main().catch(e => { console.error(e); process.exit(1); });
