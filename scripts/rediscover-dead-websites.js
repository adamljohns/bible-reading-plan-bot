#!/usr/bin/env node
// Dead-site rescue: ~1,800 churches carry "[date] Phase 6f live-fetch verdict:
// timeout/404/ssl_error" notes — their recorded website is dead. Many churches MOVED
// domains; a Brave re-search can find the current site. This script re-checks each
// dead-site church and lands on exactly one of three outcomes:
//   (a) NEW domain found — different registrable domain, Brave domain-matched with the
//       same distinctive-token precision rules as find-church-websites.js, AND the
//       fetched page's visible text carries the church's name token → REPLACE website.
//   (b) SAME domain responds 200 now (site came back, not a parked page) → keep as-is.
//   (c) nothing found / only aggregators / verification failed → keep the old (likely
//       defunct) URL recorded — deleting it would be destructive — and stamp so we
//       don't re-burn Brave quota.
// Every processed church gets `_website_rediscovered = TODAY` so batches never overlap.
//
// HONESTY: a wrong website is worse than none — precision over recall. A replacement
// is applied ONLY when (1) the candidate domain carries a distinctive church-name
// token, (2) it is NOT an aggregator/listing domain, (3) it differs from the current
// registrable domain, (4) it fetches 200, and (5) the page TEXT (tags stripped)
// mentions a distinctive name token. Any doubt → outcome (c).
//
// Usage: node scripts/rediscover-dead-websites.js [--count 40] [--apply]
// Brave HTTP 429 aborts cleanly (partial progress is written first when applying);
// the caller backs off and re-runs later — stamps make the run resumable.
const path = require('path');
const http = require('http');
const https = require('https');
const { braveSearch } = require('./lib/brave.js');
const { makeWriter } = require('./lib/format-preserving-write.js');

const TODAY = new Date().toISOString().slice(0, 10);
const arg = (k, d) => { const i = process.argv.indexOf(k); return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : d; };
const COUNT = parseInt(arg('--count', '40'), 10);
const APPLY = process.argv.includes('--apply');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const { data: d, write } = makeWriter(CHURCHES);

const AB = new Set('AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC'.split(' '));
const isUS = c => AB.has(String(c.state || '').toUpperCase().trim());
const isEnglish = n => typeof n === 'string' && !/[^\x00-\x7F]/.test(n);
const hasSite = c => typeof c.website === 'string' && /^https?:\/\//i.test(c.website);

// Domains that are directories/aggregators/socials — never "the church's website".
// (Same blocklist as find-church-websites.js; keep the two in sync when extending.)
const AGG = /facebook\.|instagram\.|twitter\.|x\.com|yelp\.|yellowpages\.|churchfinder\.|faithstreet\.|ag\.org|sbc\.net|thegospelcoalition|9marks\.|pcaac\.|opc\.org|lcms\.org|mapquest\.|tripadvisor\.|foursquare\.|manta\.|bbb\.org|wikipedia\.|linkedin\.|youtube\.|google\.|apple\.com|eventbrite\.|patch\.com|niche\.com|uschurches\.|churchangel\.|localchurchguide|findachurch|worshiptimes|tithe\.ly|subsplash\.com|churchcenter\.com|buzzfile\.|joinmychurch\.|crossmap\.|usachurches|church-?listing|churchreport|churches-?near|placeofworship|hometownlocator|city-data|homefacts|zoominfo|dnb\.com|opencorporates|chamberofcommerce|dexknows|superpages|citysearch|nextdoor\.|glassdoor|indeed\.|instagram|tiktok\.|pinterest\.|amazonaws\.com|wixsite\.com\/?$|godaddysites|weebly\.com\/?$|unitedstateschurches|churchspot|churchupdate|ourchurch\.com|find-?a-?church|churchusa|church-?directory|churchdb|\.gov\/|\.gov$|360\.org|updateourchurch|wheree\.|hub\.biz|\.hub\.|business\.site|cmac\.ws|edan\.io|elocal\.|americantowns|bizapedia|corporationwiki|company-target|mapcarta|reformedpresbyterian\.org|opc\.org|pcanet|topchurches|churchupdate|placedigger|n49\.|cylex|brownbook|ezlocal|expressupdate/i;

const tokens = s => String(s || '').toLowerCase().replace(/\b(the|a|of|and|church|chapel|community|baptist|christian|fellowship|ministries|ministry)\b/g, ' ').match(/[a-z]{4,}/g) || [];
// DISTINCTIVE tokens = ≥5-char name words that aren't generic church vocabulary — a
// domain containing one of these is almost certainly that church's own site. Generic
// church vocabulary, denomination words, and common hagionyms don't pin a specific
// church (many churches share "Grace", "Trinity"), so only a truly-distinctive token
// drives a match. Mirrors find-church-websites.js exactly.
const COMMON = new Set([
  'first', 'grace', 'community', 'church', 'christ', 'christian', 'faith', 'hope', 'bible', 'gospel', 'trinity', 'calvary', 'cornerstone', 'saint', 'saints', 'holy', 'cross', 'lighthouse', 'harvest', 'living', 'water', 'shepherd', 'covenant', 'redeemer', 'emmanuel', 'immanuel',
  'presbyterian', 'lutheran', 'anglican', 'episcopal', 'methodist', 'reformed', 'pentecostal', 'evangelical', 'catholic', 'orthodox', 'wesleyan', 'nazarene', 'brethren', 'mennonite',
  'souls', 'savior', 'saviour', 'bethel', 'bethlehem', 'zion', 'ebenezer', 'salem', 'sharon', 'olivet', 'canaan', 'resurrection', 'ascension', 'nativity', 'epiphany', 'advent', 'king', 'kings', 'prince', 'peace', 'love', 'mercy', 'light', 'spirit', 'father', 'lamb',
  'chapel', 'temple', 'tabernacle', 'fellowship', 'ministries', 'assembly', 'believers', 'disciples', 'kingdom', 'victory', 'abundant', 'blessed', 'mount', 'good', 'great', 'family', 'house', 'worship', 'praise']);
const distinctive = c => tokens(c.name).filter(t => t.length >= 5 && !COMMON.has(t));
const domainCore = url => { try { return new URL(url).hostname.replace(/^www\./, '').split('.').slice(0, -1).join('').replace(/[^a-z]/g, ''); } catch (_) { return ''; } };

// Registrable domain ("example.org" for www.example.org) — the unit of "did the
// church MOVE". Handles the handful of two-level public suffixes we ever see.
const MULTI_TLD = new Set(['co.uk', 'org.uk', 'ac.uk', 'com.au', 'net.au', 'org.au', 'co.nz', 'org.nz', 'com.mx']);
function regDomain(url) {
  try {
    const h = new URL(url).hostname.toLowerCase().replace(/^www\./, '');
    const parts = h.split('.');
    if (parts.length <= 2) return h;
    return MULTI_TLD.has(parts.slice(-2).join('.')) ? parts.slice(-3).join('.') : parts.slice(-2).join('.');
  } catch (_) { return ''; }
}

// City from the address string, for the Brave query. Addresses come in several
// shapes ("Altoona, PA 16601" / "9504 Selby Pl, Norfolk Virginia, United States
// 23503"); normalizeAddress collapses them, then the city is the comma-part just
// before the state part. A street-looking part (leading digit) is never a city.
const { normalizeAddress } = require('./lib/address-util.js');
function cityOf(c) {
  const parts = normalizeAddress(String(c.address || '')).split(',').map(s => s.trim()).filter(Boolean);
  const si = parts.findIndex(p => /^[A-Z]{2}(\s+\d{5}(-\d{4})?)?$/.test(p) || /^[A-Z]{2}\s*$/.test(p));
  let city = '';
  if (si > 0) city = parts[si - 1];
  else if (parts.length) {
    const p0 = parts[0];
    if (!/^\d/.test(p0)) city = p0.replace(/\s+[A-Z]{2}(\s+\d{5}.*)?$/, '');
  }
  // A part like "Royersford PA" (comma repair missed it) → strip trailing state.
  city = city.replace(/\s+[A-Z]{2}$/, '');
  return /^\d/.test(city) ? '' : city;
}

// Redirect-following fetch (same shape as find-church-websites.js): resolves to the
// final 200 page's HTML, or '' on any failure/non-200. Church sites almost always
// redirect http→https / →www, so redirects are followed up to 4 hops.
function fetchText(url, depth = 0) {
  return new Promise(resolve => {
    if (depth > 4) return resolve('');
    let done = false; const fin = v => { if (!done) { done = true; resolve(v); } };
    try {
      const lib = url.startsWith('https') ? https : http;
      const req = lib.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (compatible; MOOPDirectoryBot/1.0; +https://usmcmin.org)' }, rejectUnauthorized: false }, res => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          res.resume();
          let next; try { next = new URL(res.headers.location, url).href; } catch (_) { return fin(''); }
          return fetchText(next, depth + 1).then(fin);
        }
        if (res.statusCode !== 200) { res.resume(); return fin(''); }
        let b = ''; res.on('data', d => { b += d; if (b.length > 300000) req.destroy(); }); res.on('end', () => fin(b));
      });
      req.on('error', () => fin('')); req.setTimeout(10000, () => req.destroy());
    } catch (_) { fin(''); }
  });
}

// Parked/for-sale pages return 200 but are NOT "the site came back".
const PARKED = /domain (name )?(is )?for sale|buy this domain|this domain has expired|parked free|sedoparking|hugedomains\.com|dan\.com\/buy|is parked|domain broker|godaddy\.com\/forsale/i;
// Visible-ish text of a page: script/style stripped, tags stripped, lowercased.
// Used to verify the church's NAME actually appears on a candidate page — the raw
// HTML always contains its own domain (canonical links), which would self-satisfy a
// domain-token check, so the verification must run on text, not markup.
const pageText = html => String(html)
  .replace(/<script[\s\S]*?<\/script>/gi, ' ')
  .replace(/<style[\s\S]*?<\/style>/gi, ' ')
  .replace(/<[^>]+>/g, ' ')
  .replace(/&[a-z#0-9]+;/gi, ' ')
  .toLowerCase();

// ---- selection --------------------------------------------------------------
// A church qualifies when its enrichment_notes carry >=2 distinct dead-verdict
// lines (timeout|404|ssl_error), or >=1 whose [YYYY-MM-DD] date is over 14 days
// old — one recent failure could be a blip; two failures or a stale one is a dead
// site. not_a_church / redirect_loop verdicts are different problems, not "moved".
const VERDICT = /^\[(\d{4}-\d{2}-\d{2})\][^\n]*live-fetch verdict: (timeout|404|ssl_error)\b/;
function deadVerdicts(c) {
  return String(c.enrichment_notes || '').split('\n').map(l => l.match(VERDICT)).filter(Boolean);
}
function isDead(c) {
  const v = deadVerdicts(c);
  if (!v.length) return false;
  if (new Set(v.map(m => m[0])).size >= 2) return true;
  const newest = v.map(m => m[1]).sort().pop();
  return (Date.now() - new Date(newest + 'T00:00:00Z').getTime()) / 86400000 > 14;
}

const eligibleAll = d.churches.filter(c => hasSite(c) && isUS(c) && isEnglish(c.name)
  && !c._website_rediscovered && isDead(c));
const eligible = eligibleAll.slice().sort((a, b) => String(a.id).localeCompare(String(b.id))).slice(0, COUNT);

console.log(`${APPLY ? 'APPLYING' : 'DRY RUN'} — dead-site rescue for ${eligible.length} of ${eligibleAll.length} eligible churches\n`);
let replaced = 0, revived = 0, defunct = 0, processed = 0;
const note = (c, text) => { c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + text : text; };
const stamp = c => { if (APPLY) c._website_rediscovered = TODAY; processed++; };

(async () => {
  for (const c of eligible) {
    const oldSite = String(c.website).trim();
    const oldDom = regDomain(oldSite);

    // (b) first — re-check the recorded site before spending Brave quota. A live,
    // non-parked 200 means the site came back; keep it.
    const oldBody = await fetchText(oldSite);
    if (oldBody && oldBody.length >= 300 && !PARKED.test(oldBody)) {
      revived++; stamp(c);
      if (APPLY) note(c, `[${TODAY}] Dead-site rescue: site responded on re-check; keeping.`);
      console.log(`  = ${c.id}: site responded on re-check (${oldDom}) [b]`);
      continue;
    }

    // Brave re-search for the church's CURRENT site.
    const city = cityOf(c), st = String(c.state || '').toUpperCase();
    const qName = String(c.name).replace(/,?\s*(inc\.?|incorporated|llc)\b/gi, '').replace(/\([^)]*\)/g, '').trim();
    let results = [];
    try { results = await braveSearch(`${qName} ${city} ${st} church`, { count: 8 }); }
    catch (e) {
      if (/HTTP 429/.test(e.message)) {
        if (APPLY && processed) write(d);
        console.log(`\n! Brave HTTP 429 (rate/quota) — aborting cleanly after ${processed} churches` +
          `${APPLY && processed ? ' (progress written)' : ''}. Back off and re-run; stamps make this resumable.`);
        process.exit(2);
      }
      console.log(`  ! ${c.id}: Brave error ${e.message.slice(0, 60)} — skipped, not stamped`);
      await sleep(1200); continue;
    }

    // HIGH-PRECISION candidate rule (same as find-church-websites.js): a
    // non-aggregator result whose DOMAIN carries a DISTINCTIVE name token, and —
    // rescue-specific — a DIFFERENT registrable domain than the dead one.
    const dist = distinctive(c);
    let hit = null;
    if (dist.length) {
      for (const r of results) {
        const url = String(r.url || '').replace(/\/+$/, '');
        if (!/^https?:\/\//i.test(url) || AGG.test(url) || /\/(directories|directory|listings?|profile|business|search|church|churches|congregations?|info|location|find)\//i.test(url)) continue;
        const nd = regDomain(url);
        if (!nd || nd === oldDom) continue; // same domain already failed the re-check
        const dc = domainCore(url);
        if (dc && dc.length >= 5 && dist.some(t => dc.includes(t))) { hit = new URL(url).origin; break; }
      }
    }

    // (a) — but only after the candidate ITSELF fetch-verifies: live 200, not
    // parked, and the page TEXT mentions a distinctive name token. Replacing a
    // recorded website is more destructive than filling a blank, so the bar is
    // higher than discovery's. Verification fails → fall through to (c).
    if (hit) {
      const body = await fetchText(hit);
      const txt = body ? pageText(body) : '';
      if (body && !PARKED.test(body) && dist.some(t => txt.includes(t))) {
        replaced++; stamp(c);
        if (APPLY) {
          c.website = hit;
          note(c, `[${TODAY}] Dead-site rescue: previous site ${oldSite} unreachable (repeated live-fetch failures); current official site ${hit} verified via Brave domain-match + live fetch.`);
        }
        console.log(`  ✓ ${c.id}: ${oldDom} → ${hit} [a]`);
        await sleep(1200); continue;
      }
      console.log(`  ~ ${c.id}: candidate ${hit} failed live/name verification — treating as not found`);
    }

    // (c) — nothing trustworthy found. Keep the old URL on record (deleting is
    // destructive; the note tells readers it is likely defunct) and stamp.
    defunct++; stamp(c);
    if (APPLY) note(c, `[${TODAY}] Dead-site rescue: no current official site found (Brave re-search); previous site remains recorded but is likely defunct.`);
    console.log(`  – ${c.id}: no current site found (${oldDom}) [c]`);
    await sleep(1200); // Brave rate limit
  }

  if (APPLY && processed) write(d);
  console.log(`\n${replaced} replaced (a), ${revived} came back (b), ${defunct} still dead (c) — ${processed} processed.` +
    ` ${Math.max(0, eligibleAll.length - (APPLY ? processed : 0))} eligible remain.` +
    ` ${APPLY ? 'Written.' : 'Dry run — add --apply to write.'}`);
})();

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
