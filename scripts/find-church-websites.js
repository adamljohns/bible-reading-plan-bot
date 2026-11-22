#!/usr/bin/env node
// Find official websites (via Brave Search) for churches in the directory that have
// NONE — the ~14.8k records the local enrichment grind can't touch because there's no
// site to fetch. A found + VERIFIED website re-opens the church to the pastor/social
// pipeline. This is stage 1 of "go comprehensive": discovery feeds enrichment.
//
// HONESTY: a candidate is applied ONLY when scripts/lib/church-website-match.js passes
// it: the domain segments into WHOLE name/church/geo words (>= 2 counted tokens, >= 1
// distinctive name token, no other state, no conflicting denomination); it is not
// .edu/.gov/school/city/county, not a subdomain, not an aggregator, and not already
// assigned to another church; and the fetched homepage carries a church word AND the
// record's city or state, with no street address in another state. No match → leave
// blank + mark _website_searched. A wrong site is worse than none.
// (CM-1122-WEBDISC: the old substring rule `dist.some(t => dc.includes(t))` with the
// geo-guard off wrote 519 wrong sites 2026-11-16..22 — thenorthface.com, liberty.edu…)
//
// Usage: node scripts/find-church-websites.js [--count 40] [--apply]
const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');
const { braveSearch } = require('./lib/brave.js');
const { searxSearch } = require('./lib/searx.js');
// Backend: SEARCH_BACKEND=brave|searx (default searx = local, free, no quota; Principal 2026-10-31).
const BACKEND = (process.env.SEARCH_BACKEND || 'searx').toLowerCase() === 'brave' ? 'brave' : 'searx';
const webSearch = BACKEND === 'brave' ? braveSearch : searxSearch;
const ENGINE = BACKEND === 'brave' ? 'Brave' : 'SearXNG';
const { makeWriter } = require('./lib/format-preserving-write.js');
const lanes = require('./lib/grind-lanes.js');
const WM = require('./lib/church-website-match.js');

const TODAY = new Date().toISOString().slice(0, 10);
const arg = (k, d) => { const i = process.argv.indexOf(k); return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : d; };
const COUNT = parseInt(arg('--count', '40'), 10);
const APPLY = process.argv.includes('--apply');
const ATTEMPT_LOG = arg('--attempt-log', '');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const { data: d, write } = makeWriter(CHURCHES);


const AGG = WM.AGG;
const cityOf = WM.cityOf;
const distinctive = c => WM.distinctiveTokens(c);
const fetchText = url => require('./lib/site-fetch.js').fetchText(url);
// Every domain already on a church in the directory; a second church never gets it.
const ASSIGNED = WM.buildAssignedDomains(d.churches);

const MATCH = arg('--match', ''); // optional NAME filter (e.g. --match "first baptist")
const matchRe = MATCH ? new RegExp(MATCH, 'i') : null;
const STATES_F = (arg('--states', '') || '').toUpperCase().split(',').map(s => s.trim()).filter(Boolean); // e.g. --states VA,DC,MD
const eligible = d.churches.filter(c => lanes.websiteDiscoveryEligible(c)
  && (!matchRe || matchRe.test(c.name))
  && (!STATES_F.length || STATES_F.includes(String(c.state || '').toUpperCase())))
  .sort((a, b) => String(a.id).localeCompare(String(b.id))).slice(0, COUNT);

console.log(`${APPLY ? 'APPLYING' : 'DRY RUN'} — website search for ${eligible.length} siteless churches (${ENGINE})\n`);
let found = 0, none = 0;

(async () => {
  for (const c of eligible) {
    const city = cityOf(c), st = String(c.state || '').toUpperCase();
    const qName = String(c.name).replace(/,?\s*(inc\.?|incorporated|llc)\b/gi, '').replace(/\([^)]*\)/g, '').trim();
    let results = [];
    if (ATTEMPT_LOG) fs.appendFileSync(ATTEMPT_LOG, `${TODAY}\t${c.id}\n`);
    try { results = await webSearch(`${qName} ${city} ${st} church website`, { count: 10 }); }
    catch (e) { console.log(`  ! ${c.id}: ${ENGINE} error ${e.message.slice(0, 60)}`); await sleep(BACKEND === 'brave' ? 1200 : 300); continue; }

    // HIGH-PRECISION rule (lib/church-website-match.js): whole-token domain match +
    // institution/shared-domain rejects + homepage church-word and city/state check.
    // Candidates are tried in result order; the first that passes every check wins.
    const dist = distinctive(c);
    let hit = null; const why = [];
    if (dist.length) {
      for (const r of results) {
        const url = String(r.url || '').replace(/\/+$/, '');
        const v = await WM.checkCandidate(c, url, { assigned: ASSIGNED, fetchText });
        if (v.ok) { hit = { url: new URL(url).origin, how: `whole-token ${v.segs.join('+')}, ${v.reason}` }; break; }
        if (v.reason !== 'aggregator' && v.reason !== 'not-http') why.push(`${WM.regDomain(url) || url}:${v.reason}`);
      }
    }
    if (!hit) {
      // No own-domain site. A Facebook PAGE whose path carries a distinctive name token
      // is recorded as social presence (c.facebook), never as the website. Groups/posts
      // are skipped. (Principal 2026-10-31: "as long as they have social media or some
      // kind of online presence".)
      if (dist.length && !c.facebook) {
        for (const r of results) {
          const url = String(r.url || '');
          const m = url.match(/^https?:\/\/(?:www\.|m\.)?facebook\.com\/([A-Za-z0-9._-]{3,})\/?(?:\?.*)?$/i);
          if (!m) continue;
          const slug = m[1].toLowerCase();
          if (WM.facebookSlugVerdict(c, slug).ok) {
            if (APPLY) {
              c.facebook = `https://www.facebook.com/${m[1]}`;
              const note = `[${TODAY}] Facebook page discovered via ${ENGINE} (slug-match): ${c.facebook}`;
              c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + note : note;
            }
            console.log(`  ~ ${c.id} → facebook ${m[1]} [slug-match]`);
            break;
          }
        }
      }
      none++; if (APPLY) c._website_searched = TODAY; console.log(`  – ${c.id}: no verified match${why.length ? ' (' + why.slice(0, 4).join(', ') + ')' : ''}`); await sleep(BACKEND === 'brave' ? 1200 : 300); continue;
    }

    found++;
    { const rd = WM.regDomain(hit.url); if (!ASSIGNED.has(rd)) ASSIGNED.set(rd, new Set()); ASSIGNED.get(rd).add(c.id); }
    if (APPLY) {
      c.website = hit.url; c._website_searched = TODAY;
      c.engagement = c.engagement || {}; c.engagement.researched_website = true;
      const note = `[${TODAY}] Website discovered via ${ENGINE} (${hit.how}): ${hit.url}`;
      c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + note : note;
    }
    console.log(`  ✓ ${c.id} → ${hit.url} [${hit.how}]`);
    await sleep(BACKEND === 'brave' ? 1200 : 300); // Brave 1 q/s; SearXNG is local
  }

  if (APPLY && (found || none)) { write(d); }
  console.log(`\n${found} sites found+verified, ${none} none. ${APPLY ? 'Written.' : 'Dry run — add --apply to write.'}`);
})();

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
