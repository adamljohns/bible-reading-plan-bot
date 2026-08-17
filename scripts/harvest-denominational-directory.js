#!/usr/bin/env node
/**
 * Denominational-directory harvester — the coverage-ladder engine.
 *
 * Adam's ladder (2026-08-12): every church in Fredericksburg, then every church
 * in DC, then every church in Virginia. Brave domain-guessing cannot get there:
 * it only finds churches that already have a findable website, and it cannot
 * tell you a church's actual affiliation. Denominations publish authoritative
 * rosters of their own congregations -- name, address, and often the pastor --
 * which is both broader coverage and better provenance than anything scraped
 * off a church's own site.
 *
 * Two products from one crawl:
 *   1. NEW churches the directory is missing        -> discovered-<source>.json
 *      (feeds scripts/add-discovered-churches.js)
 *   2. PASTOR/affiliation leads for churches we      -> leads-<source>.json
 *      ALREADY have but left blank
 *
 * (2) matters as much as (1): the enrichment lanes ran dry on 2026-08-16 with
 * ~17.7k churches still carrying no pastor. A denominational roster fills those
 * from the denomination's own records.
 *
 * NO GUESSING. Every field is copied verbatim out of the fetched roster page,
 * and every record carries the exact URL it came from. Nothing is inferred, so
 * there is no hallucination surface at all -- this is a parser, not a model.
 *
 * Polite by construction: sequential fetches, a delay between them, an on-disk
 * cache so re-runs and resumes cost the source nothing, and a hard --max cap.
 *
 * Usage:
 *   node scripts/harvest-denominational-directory.js --source sbcv [--max 40]
 *        [--delay 1500] [--pages 3] [--out /tmp] [--no-detail] [--refresh]
 */
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 && args[i + 1] ? args[i + 1] : d; };
const has = n => args.includes(n);

const SOURCE = opt('--source', 'sbcv');
const MAX = parseInt(opt('--max', '0'), 10) || Infinity;   // cap on DETAIL fetches
const PAGES = parseInt(opt('--pages', '0'), 10) || Infinity; // cap on list pages
const DELAY = parseInt(opt('--delay', '1500'), 10);
const OUT = opt('--out', '/tmp');
const NO_DETAIL = has('--no-detail');
const REFRESH = has('--refresh');

const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36';
const CACHE = path.join('/tmp', `denom-cache-${SOURCE}`);
fs.mkdirSync(CACHE, { recursive: true });

const sleep = ms => new Promise(r => setTimeout(r, ms));
const cacheKey = url => path.join(CACHE, Buffer.from(url).toString('base64url').slice(0, 180) + '.html');

async function fetchPage(url) {
  const ck = cacheKey(url);
  if (!REFRESH && fs.existsSync(ck)) return { html: fs.readFileSync(ck, 'utf8'), cached: true };
  const res = await fetch(url, { headers: { 'User-Agent': UA, 'Accept': 'text/html' }, redirect: 'follow' });
  if (!res.ok) throw new Error(`HTTP ${res.status} on ${url}`);
  const html = await res.text();
  fs.writeFileSync(ck, html);
  await sleep(DELAY);
  return { html, cached: false };
}

// USPS 3-digit ZIP prefix ranges, used to reject a ZIP that cannot belong to the
// state a record claims. Only the states the adapters actually harvest need an
// entry; an unknown state accepts anything rather than silently dropping data.
const ZIP_RANGES = {
  VA: [[201, 201], [220, 246]], DC: [[200, 200], [202, 205]], MD: [[206, 219]],
  WV: [[247, 268]], NC: [[269, 289]], PA: [[150, 196]], DE: [[197, 199]],
  SC: [[290, 299]], TN: [[370, 385]], GA: [[300, 319], [398, 399]],
};
function zipFitsState(zip, state) {
  const r = ZIP_RANGES[String(state || '').toUpperCase()];
  if (!r) return true;
  const p = parseInt(String(zip).slice(0, 3), 10);
  return r.some(([lo, hi]) => p >= lo && p <= hi);
}

/** GET a URL, returning the body as text, cached under an explicit key. */
async function fetchRaw(url, key) {
  const ck = path.join(CACHE, key.replace(/[^a-z0-9_-]/gi, '_') + '.txt');
  if (!REFRESH && fs.existsSync(ck)) return fs.readFileSync(ck, 'utf8');
  const res = await fetch(url, { headers: { 'User-Agent': UA, 'Accept': 'application/json, text/html' } });
  if (!res.ok) throw new Error(`HTTP ${res.status} on ${url}`);
  const body = await res.text();
  fs.writeFileSync(ck, body);
  await sleep(DELAY);
  return body;
}

/** POST a form-encoded body (the OPC locator's interface). */
async function postForm(url, fields, key) {
  const ck = path.join(CACHE, key.replace(/[^a-z0-9_-]/gi, '_') + '.html');
  if (!REFRESH && fs.existsSync(ck)) return fs.readFileSync(ck, 'utf8');
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'User-Agent': UA, 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams(fields).toString(),
    redirect: 'follow',
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} on ${url}`);
  const html = await res.text();
  fs.writeFileSync(ck, html);
  await sleep(DELAY);
  return html;
}

const decode = s => String(s || '')
  // OPC's locator emits a malformed CLOSING break tag ("</br >") between address
  // lines. Without matching it the lines run together and produce streets like
  // "FOP Thompson Hall974 Michie Tavern Lane".
  .replace(/<\/?br\s*\/?\s*>/gi, '\n').replace(/<[^>]+>/g, '')
  .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&#8217;|&rsquo;/g, "'")
  .replace(/&#8216;|&lsquo;/g, "'").replace(/&quot;|&#8220;|&#8221;/g, '"')
  .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n))
  .replace(/[ \t]+/g, ' ').trim();

/* ------------------------------------------------------------------ adapters */

const ADAPTERS = {
  /**
   * Southern Baptists of Virginia. FacetWP listing, ?_paged=N, 50 per page.
   * Detail pages carry "Pastor:", "Phone:", "E-Mail:" and the mailing address.
   */
  sbcv: {
    label: 'Southern Baptists of Virginia (SBCV)',
    denomination: 'Southern Baptist Convention (SBCV)',
    listUrl: p => `https://www.sbcv.org/churches/?_paged=${p}`,
    parseList(html) {
      const out = [];
      const re = /<a class="church" href="([^"]+)">\s*<h6 class="church-name">(.*?)<\/h6>\s*<span class="church-address">(.*?)<\/span>/gs;
      let m;
      while ((m = re.exec(html))) {
        const addrLines = decode(m[3]).split('\n').map(s => s.trim()).filter(Boolean);
        const cityLine = addrLines[addrLines.length - 1] || '';
        let cm = cityLine.match(/^(.*?),\s*([A-Z]{2})\s+(\d{5})/);
        let street = addrLines.slice(0, -1).join(', ');
        // Some rows carry the whole address on ONE line with no <br> ("85 Summit
        // View Dr, Ruckersville, VA 22968-2786"), which left city and zip empty
        // and broke the matcher's city blocking. Recover city/state/zip from the
        // tail and keep whatever precedes it as the street.
        if (!cm) {
          const one = cityLine.match(/^(.*),\s*([A-Za-z .'-]+),\s*([A-Z]{2})\s+(\d{5})/);
          if (one) { street = one[1].trim(); cm = [null, one[2], one[3], one[4]]; }
        }
        out.push({
          detail_url: m[1],
          name: decode(m[2]),
          street: street || '',
          city: cm ? cm[1].trim() : '',
          state: cm ? cm[2] : 'VA',
          zip: cm ? cm[3] : '',
        });
      }
      return out;
    },
    parseDetail(html) {
      const body = html.replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/gi, '');
      const txt = decode(body).replace(/\n+/g, ' ');
      const grab = re => { const m = txt.match(re); return m ? m[1].trim() : ''; };
      // NO website. SBCV detail pages carry no church website field -- the only
      // external link is the site developer's footer credit, and a first pass
      // that grabbed "the first non-social external link" stamped
      // innovativefaith.org onto all 6 test records. A wrong website is how the
      // Stafford mis-merge happened (a church carrying another church's URL), so
      // this adapter returns an honest blank and lets the website-discovery lane
      // do that job properly.
      return {
        pastor: grab(/Pastor:\s*([A-Za-z.'\- ]{3,60}?)\s*(?:Phone:|E-Mail:|Email:|Meeting|Address|$)/i),
        phone: grab(/Phone:\s*([\d\-().+ ]{7,20})/),
        email: grab(/E-?Mail:\s*([^\s]+@[^\s]+)/i),
        website: '',
      };
    },
  },

  /**
   * Orthodox Presbyterian Church. A plain POST form (search_go=Y, state=XX)
   * whose results come back as AddPointQ('lat','lng','address','html',...)
   * JavaScript calls. Richest source so far: name, street, coordinates, phone,
   * email AND website all in one response, no per-church fetch needed.
   *
   * OPC is small (~380 congregations nationally), so one POST per state covers
   * the whole denomination cheaply.
   */
  opc: {
    label: 'Orthodox Presbyterian Church (OPC)',
    denomination: 'Orthodox Presbyterian Church (OPC)',
    async collect(ctx) {
      const states = (ctx.opt('--states', 'VA,DC,MD,WV,NC') || '').split(',').map(s => s.trim().toUpperCase()).filter(Boolean);
      const out = [];
      for (const st of states) {
        const html = await ctx.postForm('https://opc.org/locator.html', { search_go: 'Y', zipcode: '', state: st, presbytery_id: '' }, `opc-${st}`);
        // AddPointQ('lat','lng','address','<html>','C','color','City, ST','NAME');
        const re = /AddPointQ\('([-\d.]*)','([-\d.]*)','((?:[^'\\]|\\.)*)','((?:[^'\\]|\\.)*)','[^']*','[^']*','((?:[^'\\]|\\.)*)','((?:[^'\\]|\\.)*)'\)/g;
        let m, n = 0;
        while ((m = re.exec(html))) {
          const unesc = s => String(s).replace(/\\"/g, '"').replace(/\\'/g, "'").replace(/\\\//g, '/').replace(/\\n/g, ' ');
          const block = unesc(m[4]);
          const rawAddr = ctx.decode(unesc(m[3]));
          const cityState = ctx.decode(unesc(m[5]));
          // The final AddPointQ argument is an ALL-CAPS sort key ("BETHEL
          // REFORMED"); the <h5> inside the popup carries the church's real
          // capitalisation. Prefer the <h5> and keep the caps form as fallback.
          const h5 = (block.match(/<h5>([\s\S]*?)<\/h5>/i) || [])[1];
          const name = ctx.decode(h5 || unesc(m[6]));
          // "Meeting At" paragraph holds the street lines; the map's own address
          // string is the geocoder input and is often mangled, so prefer the
          // paragraph and keep the map string only as a fallback.
          const meet = block.match(/Meeting At<\/h6>\s*<p[^>]*>([\s\S]*?)<\/p>/i);
          // Congregations meeting in rented venues have their SERVICE TIME folded
          // into the same paragraph ("10 a.m.:, Bennett's Funeral Home, ..."),
          // which otherwise ends up inside the street address.
          const lines = (meet ? ctx.decode(meet[1]).split('\n') : [])
            .map(s => s.replace(/^\s*\d{1,2}(:\d{2})?\s*[ap]\.?m\.?\s*:?\s*/i, '').trim())
            .filter(s => s && !/^\d{1,2}(:\d{2})?\s*[ap]\.?m\.?$/i.test(s));
          const cm = cityState.match(/^(.*?),\s*([A-Z]{2})$/);
          const stAbbr = cm ? cm[2] : st;
          // The map's address string is a geocoder INPUT and sometimes carries a
          // stray number that looks like a ZIP: West Creek (Henrico VA) came back
          // as 11020, a New York ZIP. Take every 5-digit candidate and keep only
          // one whose prefix actually belongs to the state.
          const zm = [...rawAddr.matchAll(/\b(\d{5})(?:-\d{4})?\b/g)]
            .map(x => x[1]).find(z => ctx.zipFitsState(z, stAbbr));
          const site = (block.match(/Website:\s*<a[^>]*href="([^"]+)"/i) || [])[1] || '';
          out.push({
            detail_url: 'https://opc.org/locator.html',
            name: name.replace(/\s+/g, ' ').trim(),
            street: lines.length > 1 ? lines.slice(0, -1).join(', ') : (lines[0] || ''),
            city: cm ? cm[1].trim() : '',
            state: cm ? cm[2] : st,
            zip: zm || '',
            phone: (block.match(/Phone:\s*([\d\-().+ ]{7,20})/) || [])[1] || '',
            website: /^https?:\/\//i.test(site) ? site : '',
            pastor: '',                       // OPC's locator does not publish it
            latitude: m[1] || '', longitude: m[2] || '',
          });
          n++;
        }
        console.log(`  ${st}: ${n} congregations`);
      }
      return out;
    },
  },

  /**
   * ACNA, Diocese of the Mid-Atlantic — the diocese covering Virginia, DC and
   * Maryland, which is exactly the coverage ladder's territory.
   *
   * ACNA publishes no national roster: anglicanchurch.net/find-a-church is a
   * navigation page with no data in it, and the denomination is organised by
   * diocese. DOMA runs on Squarespace, whose documented ?format=json returns the
   * collection behind the map, paginated 20 at a time via nextPageOffset.
   */
  'acna-doma': {
    label: 'ACNA Diocese of the Mid-Atlantic',
    denomination: 'Anglican Church in North America (ACNA)',
    async collect(ctx) {
      const out = [];
      let url = 'https://www.anglicandoma.org/map-of-churches?format=json';
      for (let page = 1; page <= 20; page++) {
        const j = JSON.parse(await ctx.fetchRaw(url, `doma-p${page}`));
        for (const it of (j.items || [])) {
          const loc = it.location || {};
          const body = ctx.decode(it.body || '').replace(/\n+/g, ' ');
          const line2 = String(loc.addressLine2 || '');
          const cm = line2.match(/^(.*?),\s*([A-Z]{2})(?:,\s*(\d{5}))?/);
          const site = (String(it.body || '').match(/Website:\s*(?:<a[^>]*href="([^"]+)"|([^\s<]+))/i) || []);
          const rawSite = site[1] || site[2] || '';
          out.push({
            detail_url: `https://www.anglicandoma.org/map-of-churches/${it.urlId}`,
            name: String(it.title || '').trim(),
            street: String(loc.addressLine1 || '').trim(),
            city: cm ? cm[1].trim() : '',
            state: cm ? cm[2] : '',
            zip: cm && cm[3] ? cm[3] : ((line2.match(/\b(\d{5})\b/) || [])[1] || ''),
            phone: (body.match(/Phone:\s*([\d\-().+ ]{7,20})/) || [])[1] || '',
            email: (body.match(/([\w.+-]+@[\w.-]+\.\w{2,})/) || [])[1] || '',
            website: rawSite ? (/^https?:\/\//i.test(rawSite) ? rawSite : `https://${rawSite.replace(/^\/+/, '')}`) : '',
            pastor: '',                       // DOMA lists clergy per-parish, not here
            latitude: loc.markerLat || '', longitude: loc.markerLng || '',
          });
        }
        const p = j.pagination || {};
        console.log(`  page ${page}: ${(j.items || []).length} parishes${p.nextPage ? '' : ' (last)'}`);
        if (!p.nextPage || !p.nextPageOffset) break;
        url = `https://www.anglicandoma.org/map-of-churches?format=json&offset=${p.nextPageOffset}`;
      }
      return out;
    },
  },
};

/* --------------------------------------------------------------------- main */

(async () => {
  const A = ADAPTERS[SOURCE];
  if (!A) { console.error(`unknown --source ${SOURCE}. known: ${Object.keys(ADAPTERS).join(', ')}`); process.exit(1); }

  console.log(`Harvesting ${A.label}`);
  console.log(`  cache ${CACHE}${REFRESH ? ' (refreshing)' : ''} | delay ${DELAY}ms | detail cap ${MAX === Infinity ? 'none' : MAX}\n`);

  // Adapters whose source is not a paginated HTML list (a POST form, a JSON
  // collection) implement collect() and return the whole roster themselves.
  if (typeof A.collect === 'function') {
    const rows = await A.collect({ fetchRaw, postForm, fetchPage, decode, sleep, opt, DELAY, zipFitsState });
    const seen = new Set();
    const roster = rows.filter(r => {
      if (!r.name) return false;
      const k = `${r.name}|${r.city}|${r.state}`.toLowerCase();
      if (seen.has(k)) return false;
      seen.add(k); return true;
    });
    console.log(`\nRoster: ${roster.length} congregations (${rows.length - roster.length} dup/blank dropped)`);
    console.log(`  ${roster.filter(r => r.website).length} with website, ${roster.filter(r => r.pastor).length} with pastor\n`);
    const f = path.join(OUT, `roster-${SOURCE}.json`);
    fs.writeFileSync(f, JSON.stringify({
      source: A.label, source_key: SOURCE, denomination: A.denomination,
      harvested: new Date().toISOString().slice(0, 10),
      count: roster.length, churches: roster,
    }, null, 2));
    console.log(`Wrote ${f}`);
    console.log(`Next: node scripts/match-roster-to-directory.js --roster ${f}`);
    return;
  }

  // ---- stage 1: paginate the roster
  const roster = [];
  const seenUrl = new Set();
  for (let p = 1; p <= PAGES; p++) {
    let html;
    try { ({ html } = await fetchPage(A.listUrl(p))); }
    catch (e) { console.log(`  page ${p}: ${e.message} — stopping`); break; }
    const rows = A.parseList(html);
    const fresh = rows.filter(r => !seenUrl.has(r.detail_url));
    fresh.forEach(r => seenUrl.add(r.detail_url));
    console.log(`  page ${p}: ${rows.length} parsed, ${fresh.length} new`);
    roster.push(...fresh);
    if (!rows.length || !fresh.length) break;
  }
  console.log(`\nRoster: ${roster.length} congregations\n`);

  // ---- stage 2: detail pages (pastor / phone / website)
  if (!NO_DETAIL) {
    const n = Math.min(roster.length, MAX);
    for (let i = 0; i < n; i++) {
      const r = roster[i];
      try {
        const { html, cached } = await fetchPage(r.detail_url);
        Object.assign(r, A.parseDetail(html));
        if ((i + 1) % 25 === 0 || i === n - 1) console.log(`  detail ${i + 1}/${n}${cached ? ' (cached)' : ''}`);
      } catch (e) { r.detail_error = e.message; }
    }
  }

  const withPastor = roster.filter(r => r.pastor).length;
  const withSite = roster.filter(r => r.website).length;
  console.log(`\nDetail: ${withPastor} with pastor, ${withSite} with website\n`);

  const f = path.join(OUT, `roster-${SOURCE}.json`);
  fs.writeFileSync(f, JSON.stringify({
    source: A.label, source_key: SOURCE, denomination: A.denomination,
    harvested: new Date().toISOString().slice(0, 10),
    count: roster.length, churches: roster,
  }, null, 2));
  console.log(`Wrote ${f}`);
  console.log(`Next: node scripts/match-roster-to-directory.js --roster ${f}`);
})();
