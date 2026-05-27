#!/usr/bin/env node
// scripts/scrape-church-pastors.js
//
// For each church with a website but no real pastor name, fetch the most
// likely pastor-bearing pages and extract the senior/lead pastor's name.
//
// Approach (in order, stops at first hit):
//   1. Fetch <base>/about/ — common location for pastor bio
//   2. Fetch <base>/staff/, /our-staff/, /team/
//   3. Fetch <base>/pastors/, /elders/, /leadership/
//   4. Fall back to the homepage itself
//
// On each page, look for headings like:
//   <h*>Pastor John Smith</h*>
//   <h*>Senior Pastor: John Smith</h*>
//   <h*>Rev. John Smith</h*>
//   <h*>Dr. John Smith — Lead Pastor</h*>
//
// Plus structured-data hints:
//   <meta property="article:author" content="John Smith">
//
// Output: JSONL only (race-free; merge-pastor-scrapes.js applies).
//
// Usage:
//   node scripts/scrape-church-pastors.js --count 50 --jsonl /tmp/pastor-scrapes.jsonl
//   node scripts/scrape-church-pastors.js --state VA --count 100

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const { URL } = require('url');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const DEFAULT_JSONL = '/tmp/pastor-scrapes.jsonl';
const UA = 'Mozilla/5.0 (compatible; USMCMinistriesBot/1.0; +https://usmcmin.org/about.html) Pastor-name scraper';
const DELAY_MS = 4000;
const FETCH_TIMEOUT_MS = 18_000;
const PASTOR_PATHS = ['/about', '/about/', '/about-us', '/about-us/', '/staff', '/staff/', '/our-staff', '/team', '/team/', '/pastors', '/pastors/', '/elders', '/elders/', '/leadership', '/leadership/', '/our-pastor', '/meet-our-pastor', '/'];
// Honorifics + role markers used to anchor pastor names in HTML
const NAME_RX = /\b(?:Rev\.?|Reverend|Pastor|Dr\.?|Sr\.?\s*Pastor|Senior\s+Pastor|Lead\s+Pastor|Teaching\s+Pastor)\b\s+([A-Z][a-zA-Z'\.\-]+(?:\s+[A-Z][a-zA-Z'\.\-]+){1,3})/g;
const ROLE_RX = /([A-Z][a-zA-Z'\.\-]+(?:\s+[A-Z][a-zA-Z'\.\-]+){1,3})\s*[-—,]\s*(?:Senior\s+Pastor|Lead\s+Pastor|Pastor|Reverend)\b/g;

const PLACEHOLDER = /^(verify|various|unknown|see\s+website|currently|none|listed|tbd|n\/a|the\s+pastor|the\s+church|various\s+pastors|pastoral)/i;

function parseArgs() {
  const out = { state: 'ALL', count: null, jsonl: DEFAULT_JSONL };
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--state') out.state = a[++i].toUpperCase();
    else if (a[i] === '--count') out.count = parseInt(a[++i], 10);
    else if (a[i] === '--jsonl') out.jsonl = a[++i];
  }
  return out;
}

function fetchHead(url, maxRedirects = 3) {
  return new Promise((resolve, reject) => {
    let done = false;
    function tryUrl(u, left) {
      let p;
      try { p = new URL(u); } catch (e) { return reject(new Error('BAD_URL')); }
      const lib = p.protocol === 'http:' ? http : https;
      const req = lib.get(u, { headers: { 'User-Agent': UA, 'Accept': 'text/html,*/*' }, timeout: FETCH_TIMEOUT_MS }, res => {
        if ([301,302,303,307,308].includes(res.statusCode)) {
          if (left <= 0) return reject(new Error('REDIRECT_LIMIT'));
          const next = res.headers.location;
          if (!next) return reject(new Error('REDIRECT_NO_LOC'));
          res.resume();
          return tryUrl(new URL(next, u).href, left-1);
        }
        if (res.statusCode !== 200) return reject(new Error(`HTTP_${res.statusCode}`));
        let body = '';
        res.on('data', c => {
          if (done) return;
          body += c.toString('utf8');
          if (body.length > 250_000) { done = true; res.destroy(); resolve({ html: body, finalUrl: u }); }
        });
        res.on('end', () => { if (!done) { done = true; resolve({ html: body, finalUrl: u }); } });
      });
      req.on('error', e => { if (!done) { done = true; reject(e); } });
      req.on('timeout', () => { if (!done) { done = true; req.destroy(); reject(new Error('TIMEOUT')); } });
    }
    tryUrl(url, maxRedirects);
  });
}

// Score candidate pastor names — higher is better
function scoreCandidate(name, html, idx) {
  let score = 0;
  // Length sanity check
  const words = name.trim().split(/\s+/);
  if (words.length < 2 || words.length > 4) return -1;
  if (name.length < 5 || name.length > 50) return -1;
  // Reject obvious noise
  if (/\b(?:the|and|our|your|us|home|church|ministry|bible|study|sunday|service|prayer|worship|music)\b/i.test(name)) return -1;
  if (/[0-9]/.test(name)) return -1;
  score += 10;
  // Boost if "Senior" or "Lead" nearby in HTML (within 50 chars of the match)
  const context = html.slice(Math.max(0, idx-60), idx+name.length+60).toLowerCase();
  if (/\bsenior\s+pastor\b/.test(context)) score += 20;
  if (/\blead\s+pastor\b/.test(context)) score += 18;
  if (/\bteaching\s+pastor\b/.test(context)) score += 12;
  if (/\bfounding\s+pastor\b/.test(context)) score += 10;
  // Penalize if "assistant" or "youth" or "children"
  if (/\b(assistant|youth|children|kids|associate|worship|music)\s+pastor\b/.test(context)) score -= 15;
  return score;
}

function extractPastor(html) {
  const candidates = new Map(); // name → best score
  let m;
  NAME_RX.lastIndex = 0;
  while ((m = NAME_RX.exec(html))) {
    const name = m[1].trim();
    const s = scoreCandidate(name, html, m.index);
    if (s > 0 && (!candidates.has(name) || candidates.get(name) < s)) candidates.set(name, s);
  }
  ROLE_RX.lastIndex = 0;
  while ((m = ROLE_RX.exec(html))) {
    const name = m[1].trim();
    const s = scoreCandidate(name, html, m.index) + 5; // bonus for role-after pattern
    if (s > 0 && (!candidates.has(name) || candidates.get(name) < s)) candidates.set(name, s);
  }
  // Return best-scored candidate
  if (candidates.size === 0) return null;
  let best = null, bestScore = -1;
  for (const [n, s] of candidates) {
    if (s > bestScore) { best = n; bestScore = s; }
  }
  return bestScore >= 15 ? best : null;
}

async function main() {
  const args = parseArgs();
  const data = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));

  const alreadyDone = new Set();
  if (fs.existsSync(args.jsonl)) {
    for (const l of fs.readFileSync(args.jsonl, 'utf8').split('\n').filter(Boolean)) {
      try { const r = JSON.parse(l); if (r.id) alreadyDone.add(r.id); } catch (e) {}
    }
    console.log(`Already in JSONL: ${alreadyDone.size}`);
  }

  const stateFilter = args.state === 'ALL' ? null : args.state;
  const todo = [];
  for (const c of data.churches) {
    if (stateFilter && !new RegExp(`,\\s*${stateFilter}\\b`).test(c.address || '')) continue;
    if (alreadyDone.has(c.id || c.slug)) continue;
    if (c.pastor && !PLACEHOLDER.test(String(c.pastor).trim()) && String(c.pastor).length > 4) continue;
    if (!c.website || !/^https?:/i.test(c.website)) continue;
    todo.push(c);
  }
  if (args.count) todo.splice(args.count);
  console.log(`State filter: ${stateFilter || 'ALL'}`);
  console.log(`Records to fetch: ${todo.length}`);
  console.log(`Polite delay: ${DELAY_MS}ms per page, up to ${PASTOR_PATHS.length} paths/church`);
  if (!todo.length) { console.log('Nothing to do.'); return; }

  let ok = 0, found = 0, fail = 0;
  const start = Date.now();

  for (let i = 0; i < todo.length; i++) {
    const c = todo[i];
    if (i > 0) await new Promise(r => setTimeout(r, DELAY_MS));
    process.stdout.write(`[${i+1}/${todo.length}] ${c.name.slice(0,48).padEnd(48)} `);
    const cid = c.id || c.slug;
    let pastor = null, sourcePath = null, hitError = null;
    // Try paths in priority order, stop at first hit
    let baseUrl;
    try { baseUrl = new URL(c.website); } catch (e) {
      fs.appendFileSync(args.jsonl, JSON.stringify({ id: cid, pastor_scrape_error: 'BAD_BASE_URL', pastor_fetched_at: new Date().toISOString() }) + '\n');
      fail++; console.log(`FAIL BAD_BASE_URL`); continue;
    }
    for (const p of PASTOR_PATHS) {
      const tryUrl = new URL(p, baseUrl).href;
      try {
        const { html } = await fetchHead(tryUrl);
        const found_ = extractPastor(html);
        if (found_) { pastor = found_; sourcePath = p; break; }
        // Small sub-delay between path attempts on same domain
        await new Promise(r => setTimeout(r, 1500));
      } catch (e) {
        hitError = e.message;
        // On HTTP_404 on this path, try next. On DNS/cert failure, break (whole domain dead)
        if (/ENOTFOUND|TIMEOUT|certificate/i.test(e.message)) break;
      }
    }
    const result = { pastor_fetched_at: new Date().toISOString() };
    if (pastor) {
      result.pastor = pastor;
      result.pastor_source = `website:${sourcePath}`;
      found++;
      console.log(`OK [${pastor.slice(0,30)}] via ${sourcePath}`);
    } else {
      result.pastor_scrape_error = hitError ? hitError.slice(0, 50) : 'no-pastor-found';
      fail++;
      console.log(`no-pastor (${result.pastor_scrape_error})`);
    }
    fs.appendFileSync(args.jsonl, JSON.stringify({ id: cid, ...result }) + '\n');
    ok++;
    if ((i+1) % 25 === 0) {
      const elapsedMin = ((Date.now() - start) / 60000).toFixed(1);
      console.log(`  -- progress: ${i+1}/${todo.length} · ${found} pastors found · ${elapsedMin}m elapsed --`);
    }
  }
  console.log(`\nDone. ${ok} attempted · ${found} pastors found (${Math.round(found/ok*100)}%) · ${fail} no-pastor-or-fail.`);
}

main().catch(e => { console.error(e); process.exit(1); });
