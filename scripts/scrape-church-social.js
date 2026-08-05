#!/usr/bin/env node
//
// scrape-church-social.js — harvest each church's own social profiles
// (Facebook / YouTube / Instagram / X / TikTok) straight off its website.
//
// The directory's single biggest hole is social: of 28,713 churches only a
// few thousand carry any handle at all, yet we already hold ~15,000 church
// website URLs. Almost every church site links its own profiles from the
// footer, so this is a deterministic harvest — no model calls, no guessing.
//
// Unlike the image/quicklinks scrapers we cannot stop at </head>: social
// links live in the footer, so we read the whole document (capped).
//
// Race-free pattern (same as image / pastor / sbc-detail / quicklinks):
//   1. results append to a JSONL file under /tmp
//   2. a separate merge step (merge-church-social.js) folds them in
//   3. churches.json is read-only during the scrape
//
// Usage:
//   node scripts/scrape-church-social.js --state VA --count 100
//   node scripts/scrape-church-social.js --state all --count 2000 --concurrency 12
//   node scripts/scrape-church-social.js --state all --count 500 --jsonl /tmp/social.jsonl
//

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const DEFAULT_JSONL = '/tmp/social-scrapes.jsonl';
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36 MOOP-Church-Directory/1.0 (+https://usmcmin.org/churches.html)';
const FETCH_TIMEOUT_MS = 9000;
const MAX_BODY = 500_000;
const PLATFORMS = ['facebook', 'youtube', 'instagram', 'x_twitter', 'tiktok'];

// ---------------------------------------------------------------------------
// Handles that are never a specific church's own profile. A church site that
// links "facebook.com/sbc" in its footer is pointing at its denomination, not
// itself — recording that as the church's page would be worse than a null.
// ---------------------------------------------------------------------------
const GENERIC_HANDLES = new Set([
  'facebook', 'youtube', 'instagram', 'twitter', 'tiktok', 'home', 'login',
  'signup', 'share', 'sharer', 'help', 'about', 'privacy', 'policies', 'terms',
  'watch', 'results', 'feed', 'explore', 'pages', 'profile.php', 'people',
  'sbc', 'namb', 'lifeway', 'imb', 'erlc', 'sbcannualmeeting',
  'pcanet', 'pcaac', 'thegospelcoalition', 'gospelcoalition', 'desiringgod',
  'ligonier', 'crossway', 'wordpress', 'wixcom', 'squarespace', 'godaddy',
  'churchtrac', 'subsplash', 'planningcenter', 'tithely', 'givelify',
  'sharefaith', 'ministrybrands', 'faithlife', 'sermonaudio', 'youversion',
  'elexio', 'clover', 'easytithe', 'pushpay', 'breeze', 'ministryplatform',
]);

function parseArgs() {
  const args = process.argv.slice(2);
  const out = { state: 'all', count: 100, jsonl: DEFAULT_JSONL, concurrency: 8, delay: 250 };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--state') out.state = args[++i];
    else if (a === '--count') out.count = parseInt(args[++i], 10);
    else if (a === '--jsonl') out.jsonl = args[++i];
    else if (a === '--concurrency') out.concurrency = parseInt(args[++i], 10);
    else if (a === '--delay') out.delay = parseInt(args[++i], 10);
  }
  return out;
}

function fetchPage(url, maxRedirects = 4) {
  return new Promise((resolve, reject) => {
    let done = false;
    function tryUrl(u, redirectsLeft) {
      let parsed;
      try { parsed = new URL(u); } catch (e) { return reject(new Error('BAD_URL')); }
      if (!/^https?:$/.test(parsed.protocol)) return reject(new Error('BAD_PROTO'));
      const lib = parsed.protocol === 'http:' ? http : https;
      const req = lib.get(u, {
        headers: { 'User-Agent': UA, 'Accept': 'text/html,*/*', 'Accept-Language': 'en-US,en;q=0.9' },
        timeout: FETCH_TIMEOUT_MS,
      }, res => {
        if ([301, 302, 303, 307, 308].includes(res.statusCode)) {
          if (redirectsLeft <= 0) { res.resume(); return reject(new Error('REDIRECT_LIMIT')); }
          const next = res.headers.location;
          if (!next) { res.resume(); return reject(new Error('REDIRECT_NO_LOC')); }
          let nextUrl;
          try { nextUrl = new URL(next, u).href; } catch (e) { return reject(new Error('BAD_REDIRECT')); }
          res.resume();
          return tryUrl(nextUrl, redirectsLeft - 1);
        }
        if (res.statusCode !== 200) { res.resume(); return reject(new Error(`HTTP_${res.statusCode}`)); }
        const ctype = String(res.headers['content-type'] || '');
        if (ctype && !/html|xml|text/i.test(ctype)) { res.resume(); return reject(new Error('NOT_HTML')); }
        let body = '';
        let size = 0;
        res.setEncoding('utf8');
        res.on('data', chunk => {
          if (done) return;
          size += chunk.length;
          body += chunk;
          if (size > MAX_BODY) { done = true; res.destroy(); resolve({ html: body, finalUrl: u }); }
        });
        res.on('end', () => { if (!done) { done = true; resolve({ html: body, finalUrl: u }); } });
        res.on('error', e => { if (!done) { done = true; reject(e); } });
      });
      req.on('error', e => { if (!done) { done = true; reject(e); } });
      req.on('timeout', () => { if (!done) { done = true; req.destroy(); reject(new Error('TIMEOUT')); } });
    }
    tryUrl(url, maxRedirects);
  });
}

// --- per-platform normalizers -------------------------------------------------
// Each returns a canonical profile URL or null. Null means "this href was a
// share widget / embed / generic platform link", which we deliberately drop.

function firstSeg(pathname) {
  const seg = pathname.replace(/^\/+/, '').split('/')[0] || '';
  return decodeURIComponent(seg).trim();
}

function isGeneric(handle) {
  const h = handle.toLowerCase().replace(/^@/, '');
  return !h || h.length < 2 || GENERIC_HANDLES.has(h);
}

function normFacebook(u) {
  if (!/(^|\.)facebook\.com$/i.test(u.hostname) && !/(^|\.)fb\.com$/i.test(u.hostname)) return null;
  const p = u.pathname;
  if (/\/(sharer|share|dialog|plugins|tr|l\.php|login|watch|events|groups|photo|hashtag)/i.test(p)) return null;
  // profile.php?id=123 is a legitimate (if ugly) page identifier — keep it whole.
  if (/^\/profile\.php$/i.test(p)) {
    const id = u.searchParams.get('id');
    return id && /^\d+$/.test(id) ? `https://www.facebook.com/profile.php?id=${id}` : null;
  }
  const parts = p.replace(/^\/+/, '').split('/').filter(Boolean);
  let handle = parts[0] || '';
  const prefix = handle.toLowerCase();
  if (prefix === 'pages' || prefix === 'people') {
    // /pages/Name/12345 and /people/Name/12345 → the numeric id is the stable
    // identifier; the slug in the middle is decorative and often stale.
    const id = parts[parts.length - 1];
    return /^\d+$/.test(id) ? `https://www.facebook.com/${id}` : null;
  }
  if (prefix === 'pg') {
    // /pg/PageName/posts → the real handle is the SECOND segment, not "pg".
    handle = parts[1] || '';
  }
  if (isGeneric(handle)) return null;
  return `https://www.facebook.com/${handle}`;
}

function normYouTube(u) {
  if (!/(^|\.)youtube\.com$/i.test(u.hostname)) return null;
  const p = u.pathname;
  // We want the church's CHANNEL, not an individual sermon video or embed.
  if (/^\/(watch|embed|playlist|results|shorts|feed|redirect|oembed)/i.test(p)) return null;
  const parts = p.replace(/^\/+/, '').split('/').filter(Boolean);
  if (!parts.length) return null;
  const head = parts[0];
  if (head.startsWith('@')) {
    return isGeneric(head) ? null : `https://www.youtube.com/${head}`;
  }
  if (/^(channel|c|user)$/i.test(head)) {
    const name = parts[1];
    if (!name || isGeneric(name)) return null;
    return `https://www.youtube.com/${head.toLowerCase()}/${name}`;
  }
  return null;
}

function normInstagram(u) {
  if (!/(^|\.)instagram\.com$/i.test(u.hostname)) return null;
  const p = u.pathname;
  if (/^\/(p|reel|reels|tv|explore|stories|accounts|direct)/i.test(p)) return null;
  const handle = firstSeg(p).replace(/^@/, '');
  if (isGeneric(handle)) return null;
  return `https://www.instagram.com/${handle}`;
}

function normX(u) {
  if (!/(^|\.)(twitter\.com|x\.com)$/i.test(u.hostname)) return null;
  const p = u.pathname;
  if (/^\/(intent|share|hashtag|search|home|i|privacy|tos)/i.test(p)) return null;
  const handle = firstSeg(p).replace(/^@/, '');
  if (isGeneric(handle)) return null;
  return `https://x.com/${handle}`;
}

function normTikTok(u) {
  if (!/(^|\.)tiktok\.com$/i.test(u.hostname)) return null;
  const handle = firstSeg(u.pathname);
  if (!handle.startsWith('@') || isGeneric(handle)) return null;
  return `https://www.tiktok.com/${handle}`;
}

const NORMALIZERS = {
  facebook: normFacebook,
  youtube: normYouTube,
  instagram: normInstagram,
  x_twitter: normX,
  tiktok: normTikTok,
};

function extractSocial(html, baseUrl) {
  const found = {};
  const counts = {};
  const hrefRe = /(?:href|content)\s*=\s*["']([^"']+)["']/gi;
  let m;
  while ((m = hrefRe.exec(html)) !== null) {
    const raw = m[1];
    if (!/facebook|fb\.com|youtube|instagram|twitter|x\.com|tiktok/i.test(raw)) continue;
    let u;
    try { u = new URL(raw, baseUrl); } catch (e) { continue; }
    for (const platform of PLATFORMS) {
      const norm = NORMALIZERS[platform](u);
      if (!norm) continue;
      counts[platform] = counts[platform] || new Map();
      counts[platform].set(norm, (counts[platform].get(norm) || 0) + 1);
    }
  }
  // A page can link several profiles per platform (church + pastor + school).
  // Take the most-repeated one — the church's own profile is the one echoed in
  // header and footer, while a one-off link is usually somebody else's.
  for (const platform of PLATFORMS) {
    const c = counts[platform];
    if (!c || !c.size) continue;
    const best = [...c.entries()].sort((a, b) => b[1] - a[1] || a[0].length - b[0].length)[0];
    found[platform] = best[0];
  }
  return found;
}

function pickTargets(churches, state, count) {
  const wanted = String(state).toLowerCase();
  const out = [];
  for (const c of churches) {
    if (!c || !c.id) continue;
    if (c.defunct) continue;
    if (wanted !== 'all' && String(c.state || '').toLowerCase() !== wanted) continue;
    const site = c.website;
    if (!site || typeof site !== 'string' || !/^https?:\/\//i.test(site)) continue;
    // Skip churches that already carry a handle for every platform we harvest,
    // and skip ones a previous run already visited.
    if (c._social_scraped) continue;
    const missing = PLATFORMS.filter(p => !c[p]);
    if (!missing.length) continue;
    out.push(c);
    if (out.length >= count) break;
  }
  return out;
}

async function main() {
  const opts = parseArgs();
  const db = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
  const churches = db.churches || [];

  // Never re-scrape an id already present in the JSONL — makes reruns cheap
  // and lets a killed run resume where it stopped.
  const already = new Set();
  if (fs.existsSync(opts.jsonl)) {
    for (const line of fs.readFileSync(opts.jsonl, 'utf8').split('\n')) {
      if (!line.trim()) continue;
      try { already.add(JSON.parse(line).id); } catch (e) { /* skip bad line */ }
    }
  }

  const targets = pickTargets(churches, opts.state, opts.count + already.size)
    .filter(c => !already.has(c.id))
    .slice(0, opts.count);

  console.log(`churches: ${churches.length} | already scraped: ${already.size} | this run: ${targets.length}`);
  console.log(`jsonl: ${opts.jsonl} | concurrency: ${opts.concurrency}\n`);
  if (!targets.length) { console.log('Nothing to do.'); return; }

  const stream = fs.createWriteStream(opts.jsonl, { flags: 'a' });
  const stats = { ok: 0, hits: 0, empty: 0, err: 0 };
  const byPlatform = Object.fromEntries(PLATFORMS.map(p => [p, 0]));

  let cursor = 0;
  async function worker(wid) {
    while (cursor < targets.length) {
      const c = targets[cursor++];
      const n = cursor;
      let rec = { id: c.id, name: c.name, website: c.website, scraped_at: new Date().toISOString() };
      try {
        const { html, finalUrl } = await fetchPage(c.website);
        const social = extractSocial(html, finalUrl);
        rec = { ...rec, ...social, final_url: finalUrl, status: Object.keys(social).length ? 'found' : 'none' };
        stats.ok++;
        if (Object.keys(social).length) {
          stats.hits++;
          for (const p of PLATFORMS) if (social[p]) byPlatform[p]++;
        } else stats.empty++;
      } catch (e) {
        rec.status = 'error';
        rec.error = String(e.message || e).slice(0, 80);
        stats.err++;
      }
      stream.write(JSON.stringify(rec) + '\n');
      if (n % 25 === 0 || n === targets.length) {
        console.log(`[${n}/${targets.length}] ok=${stats.ok} hits=${stats.hits} empty=${stats.empty} err=${stats.err}`);
      }
      if (opts.delay) await new Promise(r => setTimeout(r, opts.delay));
    }
  }

  await Promise.all(Array.from({ length: Math.max(1, opts.concurrency) }, (_, i) => worker(i)));
  stream.end();

  console.log(`\nDone. fetched=${stats.ok} withSocial=${stats.hits} noSocial=${stats.empty} errors=${stats.err}`);
  console.log('By platform:', PLATFORMS.map(p => `${p}=${byPlatform[p]}`).join(' '));
  console.log(`\nNext: node scripts/merge-church-social.js --input ${opts.jsonl}`);
}

main().catch(e => { console.error(e); process.exit(1); });
