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
   * African Methodist Episcopal, 2nd Episcopal District -- DC, Maryland,
   * Virginia and North Carolina, which covers two rungs of the ladder at once.
   *
   * AME publishes no national roster: ame-church.com/directory/find-a-church is
   * only a map linking to 14 district sites, so the districts are the real
   * sources. The 2nd District posts a plain HTML table:
   *   [County] | Church | Address | City | State | Zip | website | Pastor
   * The website and Pastor columns exist but are empty for every one of the 360
   * rows, so this adapter yields location only -- honestly blank, and the
   * website-discovery lane can work them later.
   *
   * Names are the short forms AME itself uses ('Metropolitan', 'St. Paul',
   * 'Allen Chapel'). They are kept verbatim rather than expanded to
   * '<name> A.M.E. Church', which would be inventing a name the source does not
   * state; the denomination field carries the affiliation instead.
   */
  'ame-2nd': {
    label: 'AME Church, 2nd Episcopal District',
    denomination: 'African Methodist Episcopal (AME)',
    async collect(ctx) {
      const html = await ctx.fetchRaw('https://ame2.com/churches-list/', 'ame2-list');
      const out = [];
      for (const r of html.match(/<tr>[\s\S]*?<\/tr>/g) || []) {
        const tds = [...r.matchAll(/<td[^>]*>([\s\S]*?)<\/td>/g)]
          .map(c => ctx.decode(c[1]).replace(/\s+/g, ' ').trim());
        // Data rows carry a church in column 1 and a 2-letter state in column 4;
        // county headers and the header row fail one of those tests.
        if (tds.length < 6 || !tds[1] || /^church$/i.test(tds[1])) continue;
        const state = (tds[4] || '').toUpperCase();
        if (!/^[A-Z]{2}$/.test(state)) continue;
        const zip = (String(tds[5] || '').match(/\b(\d{5})\b/) || [])[1] || '';
        // The roster's short forms ('First', 'Bethel', 'Mission') are unusable as
        // directory entries on their own and collide by substring with the
        // Baptist and Lutheran churches of the same name in the same city. AME
        // names every congregation '<name> A.M.E. Church', and this table states
        // the affiliation for every row, so the suffix is the source's own fact
        // rather than an inference. The verbatim roster name is preserved in
        // roster_name so the transformation stays auditable and reversible.
        const short = tds[1];
        const name = /a\.?m\.?e\.?\b/i.test(short) ? short : `${short} A.M.E. Church`;
        out.push({
          detail_url: 'https://ame2.com/churches-list/',
          name, roster_name: short, street: tds[2] || '', city: tds[3] || '', state,
          // The roster has real ZIP errors -- Allen Chapel in DC is listed with
          // 21223, a Baltimore ZIP. Keep only ZIPs the state can actually have.
          zip: ctx.zipFitsState(zip, state) ? zip : '',
          website: '', pastor: '',
        });
      }
      const byState = out.reduce((a, c) => (a[c.state] = (a[c.state] || 0) + 1, a), {});
      console.log(`  ${out.length} congregations: ${Object.entries(byState).map(([k, v]) => k + ' ' + v).join(', ')}`);
      console.log(`  ${out.filter(c => !c.zip).length} with no usable ZIP (blank or failed the state check)`);
      return out;
    },
  },

  /**
   * Archdiocese of Washington -- the Catholic body covering DC and five
   * Maryland counties. FacetWP again, but with NO pagination: all 147 parishes
   * render on the single finder page, each with coordinates and a detail link.
   * Detail pages carry Pastor, Phone and the parish's own website.
   *
   * Scope note: the directory is already ecumenically broad (40 Catholic and 28
   * Episcopal parishes were present before this adapter), so these are in scope.
   * Intake does not rate anything -- the MOOP rubric is applied downstream.
   */
  adw: {
    label: 'Archdiocese of Washington (Catholic)',
    denomination: 'Roman Catholic',
    listUrl: () => 'https://adw.org/parishes-masses/parish-mass-finder/',
    parseList(html) {
      const out = [];
      const re = /data-lat="([-\d.]*)"\s+data-lng="([-\d.]*)">\s*<h4[^>]*>\s*<a href="([^"]+)">([\s\S]*?)<\/a>[\s\S]*?<em>Address:<\/em>\s*([\s\S]*?)<\/p>/g;
      let m;
      while ((m = re.exec(html))) {
        const addr = decode(m[5]).replace(/\s+/g, ' ').trim();
        // "<street> <City>, <ST>, <ZIP>" -- but the street may itself contain a
        // comma before a DC quadrant ("... Avenue, SE Washington, DC, 20032"),
        // so a naive comma split yields the city "SE Washington". Cut the street
        // at its suffix (plus optional quadrant) and take the rest as the city.
        // Tolerant of ADW's own malformed tails: a truncated or space-split
        // ZIP+4 ("20774-370", "20735- 4564") and a missing comma before the ZIP.
        const tail = addr.match(/^(.*?),\s*([A-Z]{2}),?\s*(\d{5})(?:\s*-\s*\d{1,4})?$/);
        let street = '', city = '', state = '', zip = '';
        if (tail) {
          state = tail[2]; zip = tail[3];
          const head = tail[1];
          const cut = head.match(/^(.*?(?:Road|Street|Avenue|Drive|Lane|Place|Boulevard|Court|Terrace|Way|Circle|Highway|Pike|Parkway|Rd|St|Ave|Dr|Ln|Pl|Blvd|Ct)\.?(?:,\s*(?:NW|NE|SE|SW))?)\s+(.+)$/i);
          if (cut) { street = cut[1].trim(); city = cut[2].trim(); }
          else { city = head.trim(); }
        } else {
          // 24 of the 147 use a second, Google-Places-shaped format instead:
          // a trailing ", USA", commas after the street, an optional leading
          // parish name, and sometimes no ZIP at all --
          //   "Holy Redeemer Church, 4902 Berwyn Road, College Park, MD 20740, USA"
          //   "6330 Linway Terrace, McLean, VA, USA"
          const g = addr.replace(/,\s*USA\s*$/i, '')
            .match(/^(.*),\s*([^,]+),\s*([A-Z]{2})(?:\s+(\d{5})(?:-\d{4})?)?$/);
          if (g) {
            city = g[2].trim(); state = g[3]; zip = g[4] || '';
            // Drop any leading chunks that are not the street itself (the parish
            // name); the street is the first chunk that begins with a number.
            const parts = g[1].split(',').map(s => s.trim()).filter(Boolean);
            const i = parts.findIndex(p => /^\d/.test(p));
            street = (i >= 0 ? parts.slice(i) : parts).join(', ');
          }
        }
        out.push({
          detail_url: m[3], name: decode(m[4]).replace(/\s+/g, ' ').trim(),
          street, city, state, zip,
          latitude: m[1] || '', longitude: m[2] || '',
        });
      }
      return out;
    },
    parseDetail(html) {
      const body = html.replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/gi, '');
      const txt = decode(body).replace(/\n+/g, ' ');
      const grab = re => { const m = txt.match(re); return m ? m[1].trim() : ''; };
      // Prefer the anchor's href for the website: the visible text is a bare
      // hostname ("stmatthewscathedral.org") with no scheme.
      const site = (html.match(/href="(https?:\/\/(?!(?:www\.)?adw\.org|adwcatholicschools|adwyouth|highland\.tools|secure\.ethicspoint)[^"]+)"[^>]*>\s*(?:https?:\/\/)?[\w.-]+\.(?:org|com|net)/i) || [])[1] || '';
      return {
        pastor: grab(/\bPastor:\s*((?:Rev\.|Msgr\.|Fr\.|Father|Very Rev\.)?[^:]{3,60}?)\s*(?:Parochial|Canonically|Deacon|In Residence|Phone|Email|Website|Weekend|Mass|$)/i),
        phone: grab(/Phone:\s*([\d\-().+ ]{7,20})/),
        website: /^https?:\/\//i.test(site) ? site : '',
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

  /**
   * Baltimore-Washington Conference UMC. Covers DC, most of Maryland, and the
   * WV eastern panhandle -- the remaining DC Methodist gap on the coverage ladder.
   *
   * Server-rendered locator at /church-locator/?page=N (~30 per page, 21 pages).
   * Each card's details block is HTML-escaped inside a <p> and carries the
   * church's real name (h4), street, city/state/ZIP, phone, and website.
   * Prefer that block over the map query-string: Asbury Annapolis's map pin
   * is a Seaford DE mailing drop, while the Address field is 87 West St.
   * Clergy is only on the /arena-group/ detail page ("Clergy: Ronald Bell").
   */
  bwcumc: {
    label: 'Baltimore-Washington Conference UMC',
    denomination: 'United Methodist Church (BWC)',
    listUrl: p => `https://www.bwcumc.org/church-locator/?page=${p}`,
    parseList(html) {
      const out = [];
      for (const art of html.match(/<article>[\s\S]*?<\/article>/g) || []) {
        const href = (art.match(/href='(\/arena-group\/[^']+)'/) || [])[1];
        if (!href) continue;
        const listing = decode((art.match(/<h5><a[^>]*>([\s\S]*?)<\/a>/) || [])[1] || '').replace(/\s+/g, ' ').trim();
        const raw = (art.match(/<div class='details'><p>([\s\S]*?)<\/p>/) || [])[1] || '';
        const ENT = { lt: '<', gt: '>', amp: '&', quot: '"', apos: "'", '#39': "'" };
        const unesc = raw.replace(/&(lt|gt|amp|quot|apos|#39);/g, (_, k) => ENT[k]);
        let name = decode((unesc.match(/<h4>([\s\S]*?)<\/h4>/) || [])[1] || '').replace(/\s+/g, ' ').trim();
        // A few BWC cards put a person's last name in <h4> ("Gorman", "littlejohn").
        // Fall back to the listing title when the h4 is not a church name.
        const looksLikeChurch = /\b(umc|church|mission|chapel|fellowship|community|initiative|korean)\b/i.test(name);
        if (!looksLikeChurch && listing) {
          const head = listing.split(',')[0].trim();
          name = /\b(umc|church|chapel|mission|fellowship)\b/i.test(head) ? head : `${head} UMC`;
        }
        const details = decode(unesc);
        const addrBlock = (details.match(/Address:\s*([\s\S]*?)\s*Phone:/i) || [])[1] || '';
        const lines = addrBlock.split('\n').map(s => s.trim()).filter(Boolean);
        const cityLine = lines[lines.length - 1] || '';
        const cm = cityLine.match(/^(.*?),\s*([A-Za-z]{2})\s+(\d{5})/i);
        let street = '', city = '', state = '', zip = '';
        if (cm) {
          city = cm[1].trim();
          state = cm[2].toUpperCase();
          zip = cm[3];
          street = lines.slice(0, -1).join(', ');
          if (!street) {
            const one = cityLine.match(/^(.*)\s+(.+),\s*([A-Za-z]{2})\s+(\d{5})/i);
            if (one) { street = one[1].trim(); city = one[2].trim(); }
          }
        }
        const phone = (details.match(/Phone:\s*([\d\-().+ ]{7,20})/) || [])[1] || '';
        // After tag-strip, "</p><p>" leaves no space, so the URL can glue to
        // "Our Services". Prefer the still-tagged href/text, then fall back.
        const rawSite = (unesc.match(/Website:\s*<\/strong>\s*(?:<a[^>]*href="([^"]+)"[^>]*>)?([^<\s]*)/i) || [])[1]
          || (unesc.match(/Website:\s*<\/strong>\s*([^<\s]*)/i) || [])[1]
          || '';
        let website = String(rawSite || '').replace(/&#x0*d;|\r/gi, '').replace(/[.,;]+$/g, '').trim();
        if (/facebook/i.test(website) || /forministry\/com/i.test(website) || /@/.test(website)) website = '';
        if (website && /\.[a-z]{2,}(\/|$)/i.test(website)) {
          website = /^https?:\/\//i.test(website) ? website : `https://${website.replace(/^\/+/, '')}`;
          website = website.replace(/\/+$/, '');
        } else {
          website = '';
        }
        if (!name) continue;
        // Bermuda and other non-US BWC affiliates have no US state/ZIP.
        if (!state || !/^(MD|DC|WV|VA|DE)$/.test(state)) continue;
        out.push({
          detail_url: `https://www.bwcumc.org${href}`,
          name, street, city, state, zip,
          phone, website,
        });
      }
      return out;
    },
    parseDetail(html) {
      const m = html.match(/<strong>Clergy:<\/strong>\s*([^<]+)/i);
      const pastor = decode(m ? m[1] : '').replace(/\s+/g, ' ').trim();
      const where = decode((html.match(/<strong>Where:<\/strong>\s*<a[^>]*>([\s\S]*?)<\/a>/i) || [])[1] || '');
      const wm = where.match(/^(.*?)\s+([^,]+),\s*([A-Za-z]{2})\s+(\d{5})/);
      const extra = {};
      if (wm) {
        extra._where_street = wm[1].trim();
        extra._where_city = wm[2].trim();
        extra._where_state = wm[3].toUpperCase();
        extra._where_zip = wm[4];
      }
      // BWC sometimes lists a whole clergy team in one field. The directory's
      // pastor column is the senior/lead name; take the first listed person
      // rather than stuffing five names into one field. The rest stay on-page.
      if (pastor && pastor.includes(',')) pastor = pastor.split(',')[0].trim();
      extra.pastor = pastor && !/^(n\/?a|none|vacant|tbd|-+)$/i.test(pastor) ? pastor : '';
      return extra;
    },
  },

  /**
   * Christian Methodist Episcopal. Official finder is an Agile Store Locator
   * embed; load_all=1 returns the full connectional roster as JSON. description
   * is the appointed pastor. No websites. Phase-1 filter: DC / MD / VA only.
   */
  cme: {
    label: 'Christian Methodist Episcopal Church',
    denomination: 'Christian Methodist Episcopal (CME)',
    async collect(ctx) {
      const states = new Set((ctx.opt('--states', 'DC,MD,VA') || '').split(',').map(s => s.trim().toUpperCase()).filter(Boolean));
      const file = path.join(CACHE, 'cme-asl-all.txt');
      let body;
      if (!REFRESH && fs.existsSync(file)) {
        body = fs.readFileSync(file, 'utf8');
      } else {
        const res = await fetch('https://thecmechurch.org/wp-admin/admin-ajax.php', {
          method: 'POST',
          headers: { 'User-Agent': UA, 'Content-Type': 'application/x-www-form-urlencoded' },
          body: 'action=asl_load_stores&load_all=1',
        });
        if (!res.ok) throw new Error(`HTTP ${res.status} on CME asl_load_stores`);
        body = await res.text();
        fs.writeFileSync(file, body);
        await ctx.sleep(ctx.DELAY || DELAY);
      }
      const rows = JSON.parse(body);
      const out = [];
      for (const r of rows) {
        const state = String(r.state || '').toUpperCase();
        if (states.size && !states.has(state)) continue;
        const zipM = String(r.postal_code || '').match(/\b(\d{5})\b/);
        const zip = zipM ? zipM[1] : '';
        const pastor = String(r.description || '').replace(/\s+/g, ' ').trim();
        out.push({
          detail_url: `https://thecmechurch.org/find-a-cme-church/#${r.slug || r.id}`,
          name: String(r.title || '').trim(),
          street: String(r.street || '').trim(),
          city: String(r.city || '').trim(),
          state,
          zip: ctx.zipFitsState(zip, state) ? zip : '',
          phone: String(r.phone || '').trim(),
          website: '',
          pastor: pastor && !/^(n\/?a|none|vacant|tbd|-+)$/i.test(pastor) ? pastor : '',
          latitude: r.lat || '', longitude: r.lng || '',
        });
      }
      console.log(`  ${rows.length} connectional; ${out.length} in ${[...states].join('/') || 'all states'}`);
      return out;
    },
  },

  /**
   * A.M.E. Zion. Official locator is a Digital Church map; the public wp-json
   * location CPT is the real roster (816 published). Address/lat/lng/phone live
   * on meta.location_address (JSON string) and meta.location_phone. Pastor,
   * website, and email live on meta_box. Phase-1 filter: DC / MD / VA only.
   */
  amez: {
    label: 'A.M.E. Zion Church',
    denomination: 'African Methodist Episcopal Zion (AME Zion)',
    async collect(ctx) {
      const states = new Set((ctx.opt('--states', 'DC,MD,VA') || '').split(',').map(s => s.trim().toUpperCase()).filter(Boolean));
      const all = [];
      for (let page = 1; page <= 20; page++) {
        const url = `https://amezion.org/wp-json/wp/v2/location?per_page=100&page=${page}`;
        const { html, cached } = await ctx.fetchPage(url);
        const rows = JSON.parse(html);
        if (!Array.isArray(rows) || !rows.length) break;
        all.push(...rows);
        console.log(`  page ${page}: ${rows.length}${cached ? ' (cached)' : ''}`);
        if (rows.length < 100) break;
      }
      // OSM strings put the house number in its own comma slot, then the road,
      // then neighborhood / ward / county, then city. The LAST 5-digit token is
      // the ZIP. A standalone 5-digit part is never a house number.
      const zipState = (z) => {
        if (/^20[0-5]\d{2}$/.test(z)) return 'DC';
        if (/^(20[6-9]|21[0-9])\d{2}$/.test(z)) return 'MD';
        if (/^(22[0-9]|23[0-9]|24[0-6])\d{2}$/.test(z)) return 'VA';
        return '';
      };
      const parseAddr = (raw, lat, lng) => {
        const s = String(raw || '').replace(/\s+/g, ' ').trim().replace(/,?\s*United States\s*$/i, '');
        if (/\b(North Carolina|South Carolina|Michigan|West Virginia|Tennessee|Pennsylvania)\b|,\s*(NC|SC|MI|WV|TN|PA)\b/i.test(s)) {
          return { street: '', city: '', state: '', zip: '' };
        }
        const zips = [...s.matchAll(/\b(\d{5})(?:-\d{4})?\b/g)].map(m => m[1]);
        const zip = zips.length ? zips[zips.length - 1] : '';
        let state = '';
        if (/\bDistrict of Columbia\b|,\s*DC\b/i.test(s)) state = 'DC';
        else if (/\bMaryland\b|,\s*MD\b/i.test(s)) state = 'MD';
        else if (/\bVirginia\b|,\s*VA\b/i.test(s)) state = 'VA';
        const zs = zipState(zip);
        if (!state) state = zs;
        if (state && zs && state !== zs) return { street: '', city: '', state: '', zip: '' };
        const la = Number(lat), ln = Number(lng);
        if (Number.isFinite(la) && Number.isFinite(ln) && la && ln && !(la >= 36.5 && la <= 39.75 && ln >= -83.7 && ln <= -75.0)) {
          return { street: '', city: '', state: '', zip: '' };
        }
        if (!state) return { street: '', city: '', state: '', zip: '' };
        const ROAD = /\b(street|st|avenue|ave|road|rd|drive|dr|lane|ln|blvd|boulevard|way|place|pl|circle|cir|highway|hwy|court|ct)\b/i;
        const SKIP = /county|ward\b|circle\/|shaw|houston|eisenhower|district of columbia|maryland|virginia|^[A-Z]{2}$|united states|church|chapel|temple|zion|memorial/i;
        let street = '', city = '';
        const clay = s.match(/^(\d{1,5}\s+(?:[NEWS]\s+)?[^,]+?\b(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd))\s+([A-Za-z .']+),\s*(VA|MD|DC)\s+(\d{5})/i);
        if (clay && (s.match(/,/g) || []).length <= 1) {
          street = clay[1].trim();
          city = clay[2].trim();
        } else {
          const parts = s.split(',').map(p => p.trim()).filter(Boolean);
          const house = parts.find(p => /^\d{1,4}$/.test(p));
          const road = parts.find(p => ROAD.test(p) && !/^\d{5}$/.test(p));
          if (house && road) street = `${house} ${road.replace(/^\d+\s+/, '')}`;
          else if (parts[0] && /^\d+\s+\S/.test(parts[0])) street = parts[0];
          else if (road) street = road;
          if (state === 'DC') city = 'Washington';
          else {
            const named = parts.find(p => !SKIP.test(p) && !/^\d/.test(p) && !ROAD.test(p));
            city = named || '';
          }
        }
        if (state === 'DC') city = 'Washington';
        return { street, city, state, zip };
      };
      const out = [];
      for (const it of all) {
        let loc = {};
        try { loc = JSON.parse((it.meta && it.meta.location_address) || '{}') || {}; } catch (_) { loc = {}; }
        const parsed = parseAddr(loc.address || '', loc.lat, loc.lng);
        const state = parsed.state;
        if (states.size && !states.has(state)) continue;
        const street = parsed.street;
        const city = parsed.city;
        const zip = parsed.zip;
        if (!street || !city) continue;
        const mb = it.meta_box || {};
        const pastor = String(mb.location_pastor || '').replace(/\s+/g, ' ').trim();
        let website = String(mb.location_website || '').trim();
        if (/amezion\.org\/location\//i.test(website) || /facebook/i.test(website)) website = '';
        if (website && !/^https?:\/\//i.test(website)) website = `https://${website.replace(/^\/+/, '')}`;
        let name = decode((it.title && it.title.rendered) || '').replace(/\s+/g, ' ').trim();
        if (name && !/\b(church|chapel|temple|memorial|zion|mission)\b/i.test(name)) {
          name = `${name} A.M.E. Zion Church`;
        }
        if (!name) continue;
        out.push({
          detail_url: it.link || `https://amezion.org/location/${it.slug}/`,
          name,
          street,
          city,
          state,
          zip: ctx.zipFitsState(zip, state) ? zip : '',
          phone: String((it.meta && it.meta.location_phone) || '').trim(),
          website,
          email: String(mb.location_email || '').trim(),
          pastor: pastor && !/^(n\/?a|none|vacant|tbd|-+)$/i.test(pastor) ? pastor : '',
          latitude: loc.lat || '', longitude: loc.lng || '',
        });
      }
      console.log(`  ${all.length} published; ${out.length} in ${[...states].join('/') || 'all states'}`);
      return out;
    },
  },

  /**
   * Baptist General Association of Virginia. Webflow CMS directory at
   * /find-a-church-directory?9a15e0c3_page=N (~24 per page, 52 pages).
   * Each card already carries name, street+city+ZIP, pastor, and phone, so the
   * list pass is the roster. Detail pages add website/email when present;
   * most are empty. "Pastor" as a placeholder name is dropped.
   */
  bgav: {
    label: 'Baptist General Association of Virginia (BGAV)',
    denomination: 'Baptist General Association of Virginia (BGAV)',
    listUrl: p => p <= 1
      ? 'https://www.bgav.org/find-a-church-directory'
      : `https://www.bgav.org/find-a-church-directory?9a15e0c3_page=${p}`,
    parseList(html) {
      const out = [];
      for (const card of html.split('church-dirctory-item w-dyn-item').slice(1)) {
        const name = decode((card.match(/<div class="church-directory-church-name">([\s\S]*?)<\/div>/) || [])[1] || '');
        const addr = decode((card.match(/<div class="church-directory-church-address">([\s\S]*?)<\/div>/) || [])[1] || '');
        const href = (card.match(/href="(\/church-directory\/[^"]+)"/) || [])[1];
        if (!name || !href) continue;
        const phones = [...card.matchAll(/<div class="church-directory-church-address phone">([\s\S]*?)<\/div>/g)].map(m => decode(m[1]));
        let pastor = '', phone = '';
        for (const p of phones) {
          if (/[\d]{3}/.test(p) && /[\d\-().+ ]{7,}/.test(p) && !/[A-Za-z]{3,}/.test(p.replace(/ext\.?\s*\d+/i, ''))) phone = p;
          else if (p && !/^(pastor|senior pastor|n\/?a|none|tbd|-+)$/i.test(p)) pastor = p;
        }
        // Cards are "11058 Dutch Hollow Rd  Culpeper, Virginia 22701".
        // decode() collapses the double space, so take everything before
        // ", Virginia ZIP" and split street/city on the last road suffix.
        const loc = addr.match(/^(.*?),\s*(Virginia|VA)\s+(\d{5})(?:-\d{4})?$/i);
        if (!loc) continue; // Tennessee / New York / malformed — not VA
        const left = loc[1].trim();
        const zip = loc[3];
        // Greedy so we split on the LAST road suffix, not the first ("Creek Rd").
        // Hollow/Ridge/Point are not suffixes — they are place-name words.
        const sm = left.match(/^(.*\b(?:Road|Rd|Street|St|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Place|Pl|Parkway|Pkwy|Highway|Hwy|Turnpike|Tpk|Circle|Cir|Pike|Trail|Terrace|Ter|Square|Sq)\.?(?:\s+(?:Northeast|Northwest|Southeast|Southwest|NE|NW|SE|SW))?)\s+(.+)$/i);
        let street = sm ? sm[1].trim() : left;
        let city = sm ? sm[2].trim() : '';
        if (!city) {
          const fb = left.match(/^(.+)\s+([A-Z][A-Za-z .']+)$/);
          if (fb) { street = fb[1].trim(); city = fb[2].trim(); }
        }
        out.push({
          detail_url: `https://www.bgav.org${href}`,
          name, street, city, state: 'VA', zip,
          pastor, phone, website: '',
        });
      }
      return out;
    },
    parseDetail(html) {
      const grab = (label) => {
        const re = new RegExp(`>${label}<\\/div>\\s*(?:<div class="strategitst-name directory">([\\s\\S]*?)<\\/div>|<a href="([^"]*)" class="strategitst-name directory">([\\s\\S]*?)<\\/a>)`, 'i');
        const m = html.match(re);
        if (!m) return { text: '', href: '' };
        return { text: decode(m[1] || m[3] || ''), href: m[2] || '' };
      };
      const site = grab('WEBSITE');
      let website = site.href && site.href !== '#' ? site.href : site.text;
      if (/w-dyn-bind-empty|#|^$/.test(website) || /facebook/i.test(website)) website = '';
      if (website && !/^https?:\/\//i.test(website)) website = `https://${website.replace(/^\/+/, '')}`;
      const pastor = grab('PASTOR').text;
      const phone = grab('Phone').text || grab('PHONE').text;
      return {
        pastor: pastor && !/^(pastor|senior pastor|n\/?a|none|tbd|-+)$/i.test(pastor) ? pastor : '',
        phone: phone || '',
        website,
      };
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
