'use strict';
// church-website-match.js — the ONE checker that decides whether a URL is a church's
// own website. Used by find-church-websites.js (discovery), rediscover-dead-websites.js
// (dead-site rescue) and scripts/recheck-discovered-websites.js (audit / revert).
//
// Why this exists (CM-1122-WEBDISC): the old rule accepted a search hit when the
// domain merely CONTAINED one name token as a substring (`dc.includes(t)`), with the
// homepage geo-guard switched off. "North" matched thenorthface.com, "Liberty" matched
// liberty.edu, "Providence" matched providence.org — 283 of 603 discoveries from
// 2026-11-16..21 landed on a domain shared with another church, and the social and
// profile lanes then copied those companies' socials/phones onto the churches.
//
// The rule now (all must hold):
//   1. DOMAIN — the registrable label must segment, end to end, into WHOLE words
//      drawn from the church's own name, church vocabulary, its city/state, or
//      neutral filler ("the", "of"), with at most one unknown chunk of <= 4 letters
//      (e.g. "esva" in broadwaybaptistesva.com). At least TWO counted tokens (name
//      words or church vocabulary) must appear, and at least ONE of them must be a
//      DISTINCTIVE name token (not generic church vocabulary). A single-word domain
//      (liberty, providence, crossroads, concord) can never match.
//   2. REJECT — .edu / .gov / .mil, any k12, school, academy, college, university,
//      city / county / town government shapes, any non-www subdomain, aggregators,
//      and any domain already assigned to ANOTHER church in the directory.
//   3. PAGE — the fetched homepage text must contain a church word AND the record's
//      city or state, AND at least one distinctive name token. Empty fetch = reject
//      (an unverifiable site is not written; a wrong site is worse than none).

const { normalizeAddress } = require('./address-util.js');

const STATES = { AL: 'alabama', AK: 'alaska', AZ: 'arizona', AR: 'arkansas', CA: 'california', CO: 'colorado', CT: 'connecticut', DE: 'delaware', FL: 'florida', GA: 'georgia', HI: 'hawaii', ID: 'idaho', IL: 'illinois', IN: 'indiana', IA: 'iowa', KS: 'kansas', KY: 'kentucky', LA: 'louisiana', ME: 'maine', MD: 'maryland', MA: 'massachusetts', MI: 'michigan', MN: 'minnesota', MS: 'mississippi', MO: 'missouri', MT: 'montana', NE: 'nebraska', NV: 'nevada', NH: 'new hampshire', NJ: 'new jersey', NM: 'new mexico', NY: 'new york', NC: 'north carolina', ND: 'north dakota', OH: 'ohio', OK: 'oklahoma', OR: 'oregon', PA: 'pennsylvania', RI: 'rhode island', SC: 'south carolina', SD: 'south dakota', TN: 'tennessee', TX: 'texas', UT: 'utah', VT: 'vermont', VA: 'virginia', WA: 'washington', WV: 'west virginia', WI: 'wisconsin', WY: 'wyoming', DC: 'district of columbia' };

// Directory / aggregator / social domains — never "the church's website".
const AGG = /facebook\.|instagram\.|twitter\.|x\.com|yelp\.|yellowpages\.|churchfinder\.|faithstreet\.|ag\.org|sbc\.net|thegospelcoalition|9marks\.|pcaac\.|opc\.org|lcms\.org|mapquest\.|tripadvisor\.|foursquare\.|manta\.|bbb\.org|wikipedia\.|linkedin\.|youtube\.|google\.|apple\.com|eventbrite\.|patch\.com|niche\.com|uschurches\.|churchangel\.|localchurchguide|findachurch|worshiptimes|tithe\.ly|subsplash\.com|churchcenter\.com|buzzfile\.|joinmychurch\.|crossmap\.|usachurches|church-?listing|churchreport|churches-?near|placeofworship|hometownlocator|city-data|homefacts|zoominfo|dnb\.com|opencorporates|chamberofcommerce|dexknows|superpages|citysearch|nextdoor\.|glassdoor|indeed\.|tiktok\.|pinterest\.|amazonaws\.com|wixsite\.com|godaddysites|weebly\.com|unitedstateschurches|churchspot|churchupdate|ourchurch\.com|find-?a-?church|churchusa|church-?directory|churchdb|360\.org|updateourchurch|wheree\.|hub\.biz|\.hub\.|business\.site|cmac\.ws|edan\.io|elocal\.|americantowns|bizapedia|corporationwiki|company-target|mapcarta|reformedpresbyterian\.org|pcanet|topchurches|placedigger|n49\.|cylex|brownbook|ezlocal|expressupdate/i;
const LISTING_PATH = /\/(directories|directory|listings?|profile|business|search|church|churches|congregations?|info|location|find)\//i;

// Schools, universities, governments. Matched against the full hostname.
const INSTITUTION_WORDS = ['k12', 'isd', 'cusd', 'school', 'academy', 'college', 'universit', 'cityof', 'countyof', 'townof', 'villageof', 'township', 'municipal', 'countygov', 'citygov', 'govt'];
const GOV_HOST_SHAPE = /(^|\.)(ci|co|city|county|town|vil)\.[a-z-]+\.[a-z]{2}\.us$|\.[a-z]{2}\.us$/i;
const GOV_TLD = /\.(edu|gov|mil)$|\.(gov|edu|mil|ac)\.[a-z]{2}$/i;

const MULTI_TLD = new Set(['co.uk', 'org.uk', 'ac.uk', 'com.au', 'net.au', 'org.au', 'co.nz', 'org.nz', 'com.mx', 'com.br', 'co.za', 'or.kr', 'co.kr']);

const STOP = new Set(['the', 'a', 'an', 'of', 'and', 'at', 'in', 'on', 'for', 'to', 'inc', 'incorporated', 'llc', 'corp', 'co']);
// Generic church vocabulary. Counts toward the 2-token floor, never as distinctive.
const CHURCH_VOCAB = new Set([
  'church', 'churches', 'chapel', 'ministries', 'ministry', 'fellowship', 'baptist', 'baptists', 'methodist', 'umc', 'ame', 'amez', 'cme', 'lutheran', 'elca', 'lcms', 'presbyterian', 'pca', 'pcusa', 'epc', 'opc', 'episcopal', 'anglican', 'catholic', 'parish', 'pentecostal', 'cogic', 'cog', 'assembly', 'assemblies', 'nazarene', 'wesleyan', 'reformed', 'evangelical', 'christian', 'community', 'congregation', 'congregational', 'ucc', 'tabernacle', 'temple', 'worship', 'faith', 'gospel', 'bible', 'missionary', 'mission', 'united', 'holiness', 'apostolic', 'fbc', 'mbc', 'umcs', 'cc', 'bc', 'pc', 'sbc',
  'first', 'grace', 'christ', 'hope', 'trinity', 'calvary', 'cornerstone', 'saint', 'saints', 'holy', 'cross', 'lighthouse', 'harvest', 'living', 'water', 'shepherd', 'covenant', 'redeemer', 'emmanuel', 'immanuel', 'orthodox', 'brethren', 'mennonite', 'souls', 'savior', 'saviour', 'bethel', 'bethlehem', 'zion', 'ebenezer', 'salem', 'sharon', 'olivet', 'canaan', 'resurrection', 'ascension', 'nativity', 'epiphany', 'advent', 'king', 'kings', 'prince', 'peace', 'love', 'mercy', 'light', 'spirit', 'father', 'lamb', 'believers', 'disciples', 'kingdom', 'victory', 'abundant', 'blessed', 'mount', 'good', 'great', 'family', 'house', 'praise', 'new', 'life', 'missionary', 'free', 'will', 'full', 'iglesia', 'bautista', 'primera', 'korean', 'hispanic']);
// Neutral filler allowed in a domain; does not count toward the floor.
const FILLER = new Set(['the', 'of', 'and', 'at', 'in', 'st', 'mt', 'ste', 'online', 'home', 'live', 'my', 'our', 'your', 'org', 'inc', 'us', 'usa', 'net', 'web', 'site', 'go', 'join', 'visit', 'info', 'today', 'church', 'a']);

const words = s => String(s || '').toLowerCase().replace(/[’']/g, '').replace(/&/g, ' and ').replace(/[^a-z0-9]+/g, ' ').trim().split(/\s+/).filter(Boolean);

// City from the address string. Shapes vary ("Altoona, PA 16601", "9504 Selby Pl,
// Norfolk Virginia, United States 23503"); normalizeAddress collapses them and the
// city is the comma-part before the state part. A street-looking part is never a city.
function cityOf(c) {
  const parts = normalizeAddress(String(c.address || '')).split(',').map(s => s.trim()).filter(Boolean);
  const si = parts.findIndex(p => /^[A-Z]{2}(\s+\d{5}(-\d{4})?)?$/.test(p));
  let city = '';
  if (si > 0) city = parts[si - 1];
  else if (parts.length) {
    const p0 = parts[0];
    if (!/^\d/.test(p0)) city = p0.replace(/\s+[A-Z]{2}(\s+\d{5}.*)?$/, '');
  }
  city = city.replace(/\s+[A-Z]{2}$/, '');
  return /^\d/.test(city) ? '' : city;
}
function stateOf(c) {
  let st = String(c.state || '').toUpperCase();
  if (!STATES[st]) { const m = String(c.address || '').match(/\b([A-Z]{2})\s+\d{5}/); if (m && STATES[m[1]]) st = m[1]; }
  return STATES[st] ? st : '';
}

function nameWords(c) { return words(c.name).filter(w => !STOP.has(w) && /[a-z]/.test(w)); }
// Distinctive = a name word of >= 4 letters that is not generic church vocabulary.
function distinctiveTokens(c) { return [...new Set(nameWords(c).filter(w => /^[a-z]{4,}$/.test(w) && !CHURCH_VOCAB.has(w) && !FILLER.has(w)))]; }

function hostOf(url) { try { return new URL(url).hostname.toLowerCase().replace(/\.$/, ''); } catch (_) { return ''; } }
function regDomain(url) {
  const h = hostOf(url).replace(/^(www|m)\./, '');
  if (!h) return '';
  const p = h.split('.');
  if (p.length <= 2) return h;
  return MULTI_TLD.has(p.slice(-2).join('.')) ? p.slice(-3).join('.') : p.slice(-2).join('.');
}

// Map registrable domain -> Set(church ids) for every website in the directory.
function buildAssignedDomains(churches) {
  const m = new Map();
  for (const c of churches) {
    if (!c || !c.website) continue;
    const rd = regDomain(c.website);
    if (!rd) continue;
    if (!m.has(rd)) m.set(rd, new Set());
    m.get(rd).add(c.id);
  }
  return m;
}

// Vocabulary for segmenting one church's domain label. Priority dist > name > church > geo > filler.
function vocabFor(c) {
  const v = new Map();
  const put = (w, kind) => { if (!w || w.length < 2) return; const rank = { dist: 5, name: 4, church: 3, geo: 2, filler: 1 }; if (!v.has(w) || rank[kind] > rank[v.get(w)]) v.set(w, kind); };
  for (const w of FILLER) put(w, 'filler');
  const st = stateOf(c);
  if (st) { put(st.toLowerCase(), 'geo'); const full = STATES[st]; put(full.replace(/\s+/g, ''), 'geo'); for (const w of full.split(' ')) put(w, 'geo'); }
  const city = words(cityOf(c));
  if (city.length) { put(city.join(''), 'geo'); for (const w of city) if (w.length >= 3) put(w, 'geo'); }
  for (const w of CHURCH_VOCAB) put(w, 'church');
  const nw = nameWords(c);
  for (const w of nw) put(w, CHURCH_VOCAB.has(w) ? 'church' : (FILLER.has(w) ? 'filler' : 'name'));
  // Adjacent name words written together ("newhope", "mtzion") are one token.
  for (let i = 0; i + 1 < nw.length; i++) put(nw[i] + nw[i + 1], 'name');
  for (const w of distinctiveTokens(c)) put(w, 'dist');
  return v;
}

// Segment a label into vocab words with at most one unknown chunk (<= 4 chars).
// Returns the best segmentation or null.
function segmentLabel(label, vocab) {
  const s = label.replace(/[^a-z]/g, '');
  if (!s) return null;
  const vw = [...vocab.keys()].sort((a, b) => b.length - a.length);
  let best = null, explored = 0;
  const score = seg => {
    const counted = new Set(seg.filter(x => x.kind !== 'geo' && x.kind !== 'filler' && x.kind !== 'unknown').map(x => x.w));
    const hasDist = seg.some(x => x.kind === 'dist');
    const unknown = seg.filter(x => x.kind === 'unknown').reduce((n, x) => n + x.w.length, 0);
    return { counted: counted.size, hasDist, unknown, seg };
  };
  const better = (a, b) => !b || (a.hasDist !== b.hasDist ? a.hasDist : a.counted !== b.counted ? a.counted > b.counted : a.unknown < b.unknown);
  (function dfs(i, usedUnknown, seg) {
    if (++explored > 20000) return;
    if (i === s.length) { const sc = score(seg); if (better(sc, best)) best = sc; return; }
    for (const w of vw) if (s.startsWith(w, i)) dfs(i + w.length, usedUnknown, seg.concat({ w, kind: vocab.get(w) }));
    if (!usedUnknown) for (let n = 1; n <= 4 && i + n <= s.length; n++) dfs(i + n, true, seg.concat({ w: s.slice(i, i + n), kind: 'unknown' }));
  })(0, false, []);
  return best;
}

// Denomination families. A domain/slug that names a DIFFERENT family than the record
// ("First Baptist Church Wylie" -> wyliechurchofchrist.org) is another church.
const FAMILY = [
  ['baptist', /\b(baptist|baptists|bautista|fbc|mbc|sbc|bc)\b/],
  ['methodist', /\b(methodist|umc|ame|amez|amec|cme|wesleyan)\b|a\s*m\s*e\b/],
  ['presbyterian', /\b(presbyterian|pca|pcusa|epc|opc|arp)\b/],
  ['lutheran', /\b(lutheran|elca|lcms)\b/],
  ['church-of-christ', /\bchurch of christ\b|\bchurchofchrist\b|\bcoc\b/],
  ['christian-church', /\bchristian church\b|\bdisciples of christ\b/],
  ['church-of-god', /\bchurch of god\b|\bcogic\b|\bcog\b/],
  ['episcopal', /\b(episcopal|anglican)\b/],
  ['catholic', /\b(catholic|parish)\b/],
  ['nazarene', /\bnazarene\b/],
  ['mennonite', /\b(mennonite|brethren|amish)\b/],
  ['pentecostal', /\b(pentecostal|assembly of god|assemblies of god)\b/],
];
const familiesIn = text => new Set(FAMILY.filter(([, re]) => re.test(text)).map(([f]) => f));
function recordFamilies(c) {
  const t = words([c.name, c.denomination, c.type, c.denomination_family].filter(Boolean).join(' ')).join(' ');
  return familiesIn(t);
}
// Families named by a segmented label ("wylie+church+of+christ").
function segFamilies(segWords) { return familiesIn(segWords.join(' ')); }
function familyConflict(c, segWords) {
  const mine = recordFamilies(c), theirs = segFamilies(segWords);
  if (!mine.size || !theirs.size) return null;
  for (const f of theirs) if (!mine.has(f)) return f;
  return null;
}
const STATE_ABBR = new Set(Object.keys(STATES).map(s => s.toLowerCase()));
// An unknown chunk that is another state's abbreviation ("clintonumcil" = IL) is a
// same-named church in that state.
function otherStateChunk(c, seg) {
  const mine = stateOf(c).toLowerCase();
  const x = seg.find(x => x.kind === 'unknown' && STATE_ABBR.has(x.w) && x.w !== mine);
  return x ? x.w.toUpperCase() : null;
}

// Domain-level verdict. opts.assigned = Map from buildAssignedDomains (optional).
function domainVerdict(c, url, opts = {}) {
  const u = String(url || '').trim();
  if (!/^https?:\/\//i.test(u)) return { ok: false, reason: 'not-http' };
  const host = hostOf(u);
  if (!host) return { ok: false, reason: 'bad-url' };
  if (AGG.test(u)) return { ok: false, reason: 'aggregator' };
  if (LISTING_PATH.test(u)) return { ok: false, reason: 'listing-path' };
  if (GOV_TLD.test(host)) return { ok: false, reason: 'edu-gov-tld' };
  if (GOV_HOST_SHAPE.test(host)) return { ok: false, reason: 'school-or-government-host' };
  { // An institution word is fine only when the church's own name/city carries it
    // ("College Park Baptist", "University Baptist").
    const own = nameWords(c).concat(words(cityOf(c))).join(' ');
    const w = INSTITUTION_WORDS.find(x => host.includes(x) && !own.includes(x));
    if (w) return { ok: false, reason: 'school-or-government-host', word: w };
  }
  const rd = regDomain(u);
  const bare = host.replace(/^(www|m)\./, '');
  if (bare !== rd) return { ok: false, reason: 'subdomain' };
  if (opts.assigned && opts.assigned.has(rd)) {
    const others = [...opts.assigned.get(rd)].filter(id => id !== c.id);
    if (others.length) return { ok: false, reason: 'domain-assigned-to-other-church', others };
  }
  const label = rd.split('.')[0];
  const vocab = vocabFor(c);
  const parts = label.split('-').filter(Boolean);
  let counted = new Set(), hasDist = false, unknown = 0, segs = [], segWords = [];
  for (const p of parts) {
    const b = segmentLabel(p, vocab);
    if (!b) return { ok: false, reason: 'label-not-segmentable', label };
    const os = otherStateChunk(c, b.seg);
    if (os) return { ok: false, reason: 'other-state-in-domain', label, state: os };
    segWords.push(...b.seg.map(x => x.w));
    for (const x of b.seg) { if (x.kind === 'dist') hasDist = true; if (!['geo', 'filler', 'unknown'].includes(x.kind)) counted.add(x.w); }
    unknown += b.unknown; segs.push(b.seg.map(x => x.kind === 'unknown' ? `?${x.w}` : x.w).join('+'));
  }
  if (unknown > 4) return { ok: false, reason: 'label-has-unknown-words', label, segs };
  if (!hasDist) return { ok: false, reason: 'no-distinctive-name-token', label, segs };
  if (counted.size < 2) return { ok: false, reason: 'fewer-than-2-whole-tokens', label, segs };
  const fc = familyConflict(c, segWords);
  if (fc) return { ok: false, reason: 'denomination-conflict', label, segs, family: fc };
  return { ok: true, reason: 'domain-ok', label, segs, tokens: [...counted] };
}

const PARKED = /domain (name )?(is )?for sale|buy this domain|this domain has expired|parked free|sedoparking|hugedomains\.com|dan\.com\/buy|is parked|domain broker|godaddy\.com\/forsale/i;
const CHURCH_WORD = /\b(church|churches|worship|sermons?|pastor|pastors|ministry|ministries|congregation|gospel|jesus|christ|parish|chapel|bible|sunday school|service times|baptist|methodist|lutheran|presbyterian|episcopal|iglesia)\b/;
const rawText = html => String(html || '')
  .replace(/<script[\s\S]*?<\/script>/gi, ' ').replace(/<style[\s\S]*?<\/style>/gi, ' ')
  .replace(/<noscript[\s\S]*?<\/noscript>/gi, ' ')
  .replace(/<[^>]+>/g, ' ').replace(/&nbsp;|&#160;/gi, ' ').replace(/&amp;/gi, '&').replace(/&#0?39;|&rsquo;|&#8217;/gi, "'").replace(/&[a-z#0-9]+;/gi, ' ').replace(/\s+/g, ' ');
const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

// Page-level verdict on fetched homepage HTML.
function pageVerdict(c, html) {
  if (!html) return { ok: false, reason: 'fetch-empty' };
  if (PARKED.test(html)) return { ok: false, reason: 'parked' };
  const raw = rawText(html), txt = raw.toLowerCase();
  // Title/meta description carry the church name/city on many JS-built sites.
  const meta = (String(html).match(/<title[^>]*>[\s\S]*?<\/title>|<meta[^>]+(name|property)=["'](description|og:title|og:description|og:site_name)["'][^>]*>/gi) || []).join(' ').toLowerCase();
  const hay = txt + ' ' + meta;
  if (!CHURCH_WORD.test(hay)) return { ok: false, reason: 'no-church-word' };
  const city = cityOf(c).toLowerCase().trim(), st = stateOf(c);
  const cityHit = city && new RegExp(`\\b${esc(city).replace(/\s+/g, '\\s+')}\\b`).test(hay);
  const stHit = st && (new RegExp(`\\b${esc(STATES[st])}\\b`).test(hay) || new RegExp(`(,\\s*|\\s)${st}\\.?\\s+\\d{5}\\b|,\\s*${st}\\b`).test(raw));
  if (!cityHit && !stHit) return { ok: false, reason: 'no-city-or-state' };
  // Street-address evidence: "Clinton, IL 61727" on a page for a Maryland church.
  const addrStates = [...raw.matchAll(/,\s*([A-Z]{2})\.?\s+\d{5}(?:-\d{4})?\b/g)].map(m => m[1]).filter(x => STATES[x]);
  if (st && addrStates.length && !addrStates.includes(st)) return { ok: false, reason: 'address-in-other-state', states: [...new Set(addrStates)] };
  const dist = distinctiveTokens(c);
  if (dist.length && !dist.some(t => hay.includes(t))) return { ok: false, reason: 'no-name-token-on-page' };
  return { ok: true, reason: cityHit ? 'page-ok-city' : 'page-ok-state' };
}

// Full check. fetchText(url) -> Promise<string html>. Returns { ok, reason, ... }.
async function checkCandidate(c, url, opts = {}) {
  const dv = domainVerdict(c, url, opts);
  if (!dv.ok) return dv;
  if (!opts.fetchText) return { ...dv, ok: false, reason: 'no-fetcher' };
  let origin; try { origin = new URL(url).origin; } catch (_) { return { ok: false, reason: 'bad-url' }; }
  const html = await opts.fetchText(origin);
  const pv = pageVerdict(c, html);
  return { ...dv, ok: pv.ok, reason: pv.ok ? pv.reason : pv.reason, page: pv.reason };
}

// Facebook PAGE slug (facebook.com/<slug>): same whole-token rule as a domain label.
function facebookSlugVerdict(c, slug) {
  const s = String(slug || '').toLowerCase();
  if (/^(groups|events|pages|profile\.php|people|watch|marketplace|share|hashtag|login|public)$/.test(s)) return { ok: false, reason: 'not-a-page' };
  const vocab = vocabFor(c);
  const parts = s.split(/[._-]+/).filter(Boolean);
  let counted = new Set(), hasDist = false, unknown = 0, segWords = [];
  for (const p0 of parts) {
    const p = p0.replace(/[0-9]/g, '');
    if (!p) continue; // numeric page-id suffix ("...-Church-228133737209700")
    const b = segmentLabel(p, vocab);
    if (!b) return { ok: false, reason: 'slug-not-segmentable' };
    if (otherStateChunk(c, b.seg)) return { ok: false, reason: 'other-state-in-slug' };
    segWords.push(...b.seg.map(x => x.w));
    for (const x of b.seg) { if (x.kind === 'dist') hasDist = true; if (!['geo', 'filler', 'unknown'].includes(x.kind)) counted.add(x.w); }
    unknown += b.unknown;
  }
  if (unknown > 4) return { ok: false, reason: 'slug-has-unknown-words' };
  if (!hasDist) return { ok: false, reason: 'no-distinctive-name-token' };
  if (counted.size < 2) return { ok: false, reason: 'fewer-than-2-whole-tokens' };
  if (familyConflict(c, segWords)) return { ok: false, reason: 'denomination-conflict' };
  return { ok: true, reason: 'slug-ok' };
}

module.exports = { AGG, STATES, cityOf, stateOf, distinctiveTokens, regDomain, hostOf, buildAssignedDomains, domainVerdict, pageVerdict, checkCandidate, facebookSlugVerdict, segmentLabel, vocabFor, rawText };
