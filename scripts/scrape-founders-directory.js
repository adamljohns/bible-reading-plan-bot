#!/usr/bin/env node
// scripts/scrape-founders-directory.js
//
// Crawl the public Founders Ministries church directory at
//   https://church.founders.org/churches/
// to extract every listed church's deep-link URL + name + location.
//
// Per-church URL pattern (verified via WebFetch 2026-05-27):
//   https://church.founders.org/church/{slug}/
//
// Pagination (WordPress): /churches/page/{N}/ with 60 churches per page.
// Total listings: ~1,423 → ~24 pages → ~75s at 3s polite delay.
//
// Output: /tmp/founders-scrape.jsonl  (crash-safe append, one record per line)
//   { name, city, state, location_raw, network_url, fetched_at }
//
// Usage:
//   node scripts/scrape-founders-directory.js            # full crawl, --resume implicit
//   node scripts/scrape-founders-directory.js --pages 5  # cap to N pages
//   node scripts/scrape-founders-directory.js --start 10 # start at page 10

const fs = require('fs');
const https = require('https');

const BASE = 'https://church.founders.org/churches';
const OUT = '/tmp/founders-scrape.jsonl';
const UA = 'Mozilla/5.0 (compatible; USMCMinistriesBot/1.0; +https://usmcmin.org/about.html) Founders-directory crawler';
const DELAY_MS = 3000;
const FETCH_TIMEOUT_MS = 25_000;

function parseArgs() {
  const out = { start: 1, pages: null };
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--start') out.start = parseInt(a[++i], 10);
    else if (a[i] === '--pages') out.pages = parseInt(a[++i], 10);
  }
  return out;
}

function fetchText(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { headers: { 'User-Agent': UA, 'Accept': 'text/html,*/*' }, timeout: FETCH_TIMEOUT_MS }, res => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        return reject(new Error(`Redirect ${res.statusCode} → ${res.headers.location || '?'}`));
      }
      if (res.statusCode !== 200) return reject(new Error(`HTTP ${res.statusCode}`));
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => resolve(body));
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('TIMEOUT')); });
  });
}

// Parse a directory page. Founders uses the WP-Job-Manager "employer-card"
// template — each church is an <article> wrapping:
//
//   <article class="... employer_location-{state-slug}" data-latitude="..." data-longitude="...">
//     <h2 class="employer-title">
//       <a href="https://church.founders.org/church/{slug}/" rel="bookmark">CHURCH NAME</a>
//     </h2>
//     ...
//     <a href="https://church.founders.org/church-location/florida/">Florida</a>
//   </article>
//
// We anchor on <h2 class="employer-title"> (one per church on the page, no
// duplicates) and pull URL + name from the inner <a>, then look forward up
// to ~1.5KB for the location anchor.
function parseListings(html) {
  const out = [];
  const rx = /<h2[^>]+class="employer-title"[^>]*>\s*<a[^>]+href="(https:\/\/church\.founders\.org\/church\/[^"]+\/)"[^>]*>\s*([\s\S]+?)\s*<\/a>\s*<\/h2>/gi;
  let m;
  while ((m = rx.exec(html))) {
    const network_url = m[1];
    const name = m[2]
      .replace(/<[^>]+>/g, '')   // strip any inner tags
      .replace(/&amp;/g, '&')
      .replace(/&#039;/g, "'")
      .replace(/&#8217;/g, "'")
      .replace(/&quot;/g, '"')
      .replace(/\s+/g, ' ')
      .trim();
    // Look ~1500 chars after the H2 for the location anchor (state name in href + text)
    const tail = html.slice(m.index, m.index + 1500);
    const locM = tail.match(/href="https:\/\/church\.founders\.org\/church-location\/[^"]+\/"[^>]*>\s*([^<]+?)\s*</);
    const location_raw = locM ? locM[1].trim() : '';
    out.push({ name, location_raw, network_url });
  }
  return out;
}

function appendJsonl(file, obj) {
  fs.appendFileSync(file, JSON.stringify(obj) + '\n');
}

function readScrapedUrls() {
  if (!fs.existsSync(OUT)) return new Set();
  const lines = fs.readFileSync(OUT, 'utf8').split('\n').filter(Boolean);
  const set = new Set();
  for (const l of lines) {
    try { const r = JSON.parse(l); if (r.network_url) set.add(r.network_url); } catch (e) {}
  }
  return set;
}

// Convert location_raw (state name) to 2-letter state code
const US_STATES = {
  'alabama':'AL','alaska':'AK','arizona':'AZ','arkansas':'AR','california':'CA','colorado':'CO',
  'connecticut':'CT','delaware':'DE','florida':'FL','georgia':'GA','hawaii':'HI','idaho':'ID',
  'illinois':'IL','indiana':'IN','iowa':'IA','kansas':'KS','kentucky':'KY','louisiana':'LA',
  'maine':'ME','maryland':'MD','massachusetts':'MA','michigan':'MI','minnesota':'MN','mississippi':'MS',
  'missouri':'MO','montana':'MT','nebraska':'NE','nevada':'NV','new hampshire':'NH','new jersey':'NJ',
  'new mexico':'NM','new york':'NY','north carolina':'NC','north dakota':'ND','ohio':'OH','oklahoma':'OK',
  'oregon':'OR','pennsylvania':'PA','rhode island':'RI','south carolina':'SC','south dakota':'SD',
  'tennessee':'TN','texas':'TX','utah':'UT','vermont':'VT','virginia':'VA','washington':'WA',
  'west virginia':'WV','wisconsin':'WI','wyoming':'WY','district of columbia':'DC',
};

function normalizeLocation(loc) {
  if (!loc) return { state: '', country: '' };
  const k = loc.toLowerCase().trim();
  if (US_STATES[k]) return { state: US_STATES[k], country: 'USA' };
  // Non-US: country in the location field
  return { state: '', country: loc };
}

async function main() {
  const args = parseArgs();
  const alreadyScraped = readScrapedUrls();
  console.log(`Founders directory crawl · already-scraped URLs: ${alreadyScraped.size}`);

  let totalFound = 0, totalNew = 0, totalFail = 0;
  let pageEmpty = 0;
  const MAX_EMPTY_BEFORE_STOP = 2; // stop if 2 consecutive pages return nothing

  for (let p = args.start; ; p++) {
    if (args.pages && (p - args.start) >= args.pages) {
      console.log(`Reached --pages limit (${args.pages}). Stopping.`);
      break;
    }
    const url = p === 1 ? `${BASE}/` : `${BASE}/page/${p}/`;
    process.stdout.write(`[page ${p}] ${url} ... `);
    let html;
    try {
      html = await fetchText(url);
    } catch (e) {
      console.log(`FAIL ${e.message}`);
      totalFail++;
      pageEmpty++;
      if (pageEmpty >= MAX_EMPTY_BEFORE_STOP) {
        console.log(`${MAX_EMPTY_BEFORE_STOP} consecutive failures — stopping.`);
        break;
      }
      await new Promise(r => setTimeout(r, DELAY_MS));
      continue;
    }
    const listings = parseListings(html);
    totalFound += listings.length;
    let newOnPage = 0;
    for (const l of listings) {
      if (alreadyScraped.has(l.network_url)) continue;
      const { state, country } = normalizeLocation(l.location_raw);
      const rec = {
        name: l.name,
        city: '',          // directory listing doesn't include city; matcher uses name+state
        state,
        country,
        location_raw: l.location_raw,
        network_url: l.network_url,
        fetched_at: new Date().toISOString(),
      };
      appendJsonl(OUT, rec);
      alreadyScraped.add(l.network_url);
      newOnPage++;
      totalNew++;
    }
    console.log(`${listings.length} listings (${newOnPage} new)`);
    if (listings.length === 0) {
      pageEmpty++;
      if (pageEmpty >= MAX_EMPTY_BEFORE_STOP) {
        console.log(`${MAX_EMPTY_BEFORE_STOP} consecutive empty pages — end of directory.`);
        break;
      }
    } else {
      pageEmpty = 0;
    }
    await new Promise(r => setTimeout(r, DELAY_MS));
  }

  console.log(`\nDone. ${totalFound} listings scanned · ${totalNew} new URLs written · ${totalFail} fetch errors.`);
  console.log(`Output: ${OUT}`);
}

main().catch(e => { console.error(e); process.exit(1); });
