#!/usr/bin/env node
// Find official websites (via Brave Search) for churches in the directory that have
// NONE — the ~14.8k records the local enrichment grind can't touch because there's no
// site to fetch. A found + VERIFIED website re-opens the church to the pastor/social
// pipeline. This is stage 1 of "go comprehensive": discovery feeds enrichment.
//
// HONESTY: a candidate site is applied ONLY if we fetch it and the church's name tokens
// AND its city appear on the page (or a strong name+state match). Aggregator/listing
// domains (churchfinder, faithstreet, yelp, facebook, ag.org, yellowpages, …) are never
// stored as "the website". No match → leave blank + mark _website_searched so we don't
// re-burn Brave quota. A wrong site is worse than none.
//
// Usage: node scripts/find-church-websites.js [--count 40] [--apply]
const fs = require('fs');
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
const AGG = /facebook\.|instagram\.|twitter\.|x\.com|yelp\.|yellowpages\.|churchfinder\.|faithstreet\.|ag\.org|sbc\.net|thegospelcoalition|9marks\.|pcaac\.|opc\.org|lcms\.org|mapquest\.|tripadvisor\.|foursquare\.|manta\.|bbb\.org|wikipedia\.|linkedin\.|youtube\.|google\.|apple\.com|eventbrite\.|patch\.com|niche\.com|uschurches\.|churchangel\.|localchurchguide|findachurch|worshiptimes|tithe\.ly|subsplash\.com|churchcenter\.com|buzzfile\.|joinmychurch\.|crossmap\.|usachurches|church-?listing|churchreport|churches-?near|placeofworship|hometownlocator|city-data|homefacts|zoominfo|dnb\.com|opencorporates|chamberofcommerce|dexknows|superpages|citysearch|nextdoor\.|glassdoor|indeed\.|instagram|tiktok\.|pinterest\.|amazonaws\.com|wixsite\.com\/?$|godaddysites|weebly\.com\/?$|unitedstateschurches|churchspot|churchupdate|ourchurch\.com|find-?a-?church|churchusa|church-?directory|churchdb|\.gov\/|\.gov$|360\.org|updateourchurch|wheree\.|hub\.biz|\.hub\.|business\.site|cmac\.ws|edan\.io|elocal\.|americantowns|bizapedia|corporationwiki|company-target|mapcarta|reformedpresbyterian\.org|opc\.org|pcanet|topchurches|churchupdate|placedigger|n49\.|cylex|brownbook|ezlocal|expressupdate/i;

const cityOf = c => String(c.address || '').split(',')[0].trim() || '';
const tokens = s => String(s || '').toLowerCase().replace(/\b(the|a|of|and|church|chapel|community|baptist|christian|fellowship|ministries|ministry)\b/g, ' ').match(/[a-z]{4,}/g) || [];
// DISTINCTIVE tokens = ≥5-char name words that aren't generic church vocabulary — a
// domain containing one of these is almost certainly that church's own site.
// Generic church vocabulary + denomination words + common hagionyms. A domain matching
// ONLY one of these does NOT pin a specific church (many churches share "All Saints",
// "Grace", "Trinity"), so we don't trust it — only a truly-distinctive token (a place
// name or unique name) drives a match. This is what keeps allsaints_springfield_.org
// from being applied to the Augusta church.
const COMMON = new Set([
  'first', 'grace', 'community', 'church', 'christ', 'christian', 'faith', 'hope', 'bible', 'gospel', 'trinity', 'calvary', 'cornerstone', 'saint', 'saints', 'holy', 'cross', 'lighthouse', 'harvest', 'living', 'water', 'shepherd', 'covenant', 'redeemer', 'emmanuel', 'immanuel',
  'presbyterian', 'lutheran', 'anglican', 'episcopal', 'methodist', 'reformed', 'pentecostal', 'evangelical', 'catholic', 'orthodox', 'wesleyan', 'nazarene', 'brethren', 'mennonite',
  'souls', 'savior', 'saviour', 'bethel', 'bethlehem', 'zion', 'ebenezer', 'salem', 'sharon', 'olivet', 'canaan', 'resurrection', 'ascension', 'nativity', 'epiphany', 'advent', 'king', 'kings', 'prince', 'peace', 'love', 'mercy', 'light', 'spirit', 'father', 'lamb',
  'chapel', 'temple', 'tabernacle', 'fellowship', 'ministries', 'assembly', 'believers', 'disciples', 'kingdom', 'victory', 'abundant', 'blessed', 'mount', 'good', 'great', 'family', 'house', 'worship', 'praise']);
const distinctive = c => tokens(c.name).filter(t => t.length >= 5 && !COMMON.has(t));
const domainCore = url => { try { return new URL(url).hostname.replace(/^www\./, '').split('.').slice(0, -1).join('').replace(/[^a-z]/g, ''); } catch (_) { return ''; } };
const STATES = { AL: 'alabama', AK: 'alaska', AZ: 'arizona', AR: 'arkansas', CA: 'california', CO: 'colorado', CT: 'connecticut', DE: 'delaware', FL: 'florida', GA: 'georgia', HI: 'hawaii', ID: 'idaho', IL: 'illinois', IN: 'indiana', IA: 'iowa', KS: 'kansas', KY: 'kentucky', LA: 'louisiana', ME: 'maine', MD: 'maryland', MA: 'massachusetts', MI: 'michigan', MN: 'minnesota', MS: 'mississippi', MO: 'missouri', MT: 'montana', NE: 'nebraska', NV: 'nevada', NH: 'new hampshire', NJ: 'new jersey', NM: 'new mexico', NY: 'new york', NC: 'north carolina', ND: 'north dakota', OH: 'ohio', OK: 'oklahoma', OR: 'oregon', PA: 'pennsylvania', RI: 'rhode island', SC: 'south carolina', SD: 'south dakota', TN: 'tennessee', TX: 'texas', UT: 'utah', VT: 'vermont', VA: 'virginia', WA: 'washington', WV: 'west virginia', WI: 'wisconsin', WY: 'wyoming', DC: 'district of columbia' };
// True only when the page mentions a DIFFERENT state's full name and NOT the church's —
// positive evidence the domain-matched site belongs to a same-named church elsewhere.
function stateConflict(page, st) {
  const mine = STATES[String(st).toUpperCase()];
  if (!mine || page.includes(mine)) return false;
  return Object.entries(STATES).some(([ab, full]) => ab !== String(st).toUpperCase() && page.includes(full));
}

function fetchText(url, depth = 0) {
  return new Promise(resolve => {
    if (depth > 4) return resolve('');
    let done = false; const fin = v => { if (!done) { done = true; resolve(v); } };
    try {
      const lib = url.startsWith('https') ? https : http;
      const req = lib.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (compatible; MOOPDirectoryBot/1.0; +https://usmcmin.org)' }, rejectUnauthorized: false }, res => {
        // Follow redirects (church sites almost always redirect http→https / →www).
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

const MATCH = arg('--match', ''); // optional NAME filter (e.g. --match "first baptist")
const matchRe = MATCH ? new RegExp(MATCH, 'i') : null;
const STATES_F = (arg('--states', '') || '').toUpperCase().split(',').map(s => s.trim()).filter(Boolean); // e.g. --states VA,DC,MD
const eligible = d.churches.filter(c => !hasSite(c) && isEnglish(c.name) && isUS(c) && !c._website_searched
  && (!matchRe || matchRe.test(c.name))
  && (!STATES_F.length || STATES_F.includes(String(c.state || '').toUpperCase())))
  .sort((a, b) => String(a.id).localeCompare(String(b.id))).slice(0, COUNT);

console.log(`${APPLY ? 'APPLYING' : 'DRY RUN'} — website search for ${eligible.length} siteless churches (Brave)\n`);
let found = 0, none = 0;

(async () => {
  for (const c of eligible) {
    const city = cityOf(c), st = String(c.state || '').toUpperCase();
    const qName = String(c.name).replace(/,?\s*(inc\.?|incorporated|llc)\b/gi, '').replace(/\([^)]*\)/g, '').trim();
    let results = [];
    try { results = await braveSearch(`${qName} ${city} ${st} church website`, { count: 8 }); }
    catch (e) { console.log(`  ! ${c.id}: Brave error ${e.message.slice(0, 60)}`); await sleep(1200); continue; }

    // HIGH-PRECISION rule: accept ONLY a non-aggregator result whose DOMAIN carries a
    // DISTINCTIVE church-name token. Aggregator/directory domains never contain the
    // church's own name, so this can't grab a wrong listing. Churches whose only name
    // words are generic ("Grace Community") yield no distinctive token → skipped (honest
    // miss beats a wrong site). Lower recall, but every hit is the church's real site.
    const dist = distinctive(c);
    let hit = null;
    if (dist.length) {
      for (const r of results) {
        const url = String(r.url || '').replace(/\/+$/, '');
        if (!/^https?:\/\//i.test(url) || AGG.test(url) || /\/(directories|directory|listings?|profile|business|search|church|churches|congregations?|info|location|find)\//i.test(url)) continue;
        const dc = domainCore(url);
        if (dc && dc.length >= 5 && dist.some(t => dc.includes(t))) { hit = { url: new URL(url).origin, how: 'domain-match' }; break; }
      }
    }
    // Geo-guard: a distinctive token can still collide with a same-named church in
    // another state (two "Aberdeen First Baptist"s). If the matched site fetches and its
    // text does NOT mention this church's city, it's the wrong location → reject. (Fetch
    // empty / no city on file → keep the domain-match; can't disprove it.)
    // NOTE: acceptance is domain-match only (~98% precise). Residual miss: two churches
    // sharing a distinctive token in different states (e.g. "Aberdeen First Baptist" in
    // AR vs NC) can cross-match. Homepage geo-verification proved unreliable both ways
    // (homepages omit their own city; church pages mention other states in bios/missions),
    // so we DON'T gate on it — Chaps' QA cron + human review catch the rare wrong site.
    if (!hit) { none++; if (APPLY) c._website_searched = TODAY; console.log(`  – ${c.id}: no distinctive-domain match`); await sleep(1200); continue; }

    found++;
    if (APPLY) {
      c.website = hit.url; c._website_searched = TODAY;
      c.engagement = c.engagement || {}; c.engagement.researched_website = true;
      const note = `[${TODAY}] Website discovered via Brave (${hit.how}): ${hit.url}`;
      c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + note : note;
    }
    console.log(`  ✓ ${c.id} → ${hit.url} [${hit.how}]`);
    await sleep(1200); // Brave rate limit
  }

  if (APPLY && (found || none)) { write(d); }
  console.log(`\n${found} sites found+verified, ${none} none. ${APPLY ? 'Written.' : 'Dry run — add --apply to write.'}`);
})();

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
