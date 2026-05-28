#!/usr/bin/env node
//
// scrape-church-quicklinks.js — find common deep-link pages on each church's
// website so the per-church profile page can offer one-click access to the
// church's "core beliefs," "sermons," "staff," etc.
//
// For each church with a real website, this script probes a small set of
// well-known paths via HEAD requests, then records which ones return 200
// as a quick_links array on the church record. The autolinker uses a tight
// label set so the chips read like a curated navigation row, not a junk
// drawer of every URL on the site.
//
// Race-free pattern (same as image / pastor / sbc-detail scrapers):
//   1. results write to a JSONL file under /tmp
//   2. a separate merge step (merge-church-quicklinks.js) folds them into
//      churches.json
//   3. churches.json is read-only during the scrape
//
// Usage:
//   node scripts/scrape-church-quicklinks.js --state VA --count 100 --jsonl /tmp/quicklinks.jsonl
//   node scripts/scrape-church-quicklinks.js --state all --count 200
//

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const DEFAULT_JSONL = '/tmp/quicklinks-scrapes.jsonl';
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36 MOOP-Church-Directory/1.0 (+https://usmcmin.org/churches.html)';
const PROBE_TIMEOUT_MS = 4500;
const POLITE_DELAY_MS = 1200;

// Path -> label mapping. Labels chosen to read naturally as chip text on the
// church-profile page. Order matters: the first match for a given label wins.
const PATH_PROBES = [
  // Beliefs / doctrine
  { paths: ['/what-we-believe', '/whatwebelieve', '/beliefs', '/our-beliefs', '/core-beliefs', '/statement-of-faith', '/doctrine', '/our-doctrine', '/faith'], label: 'Beliefs', icon: 'shield-cross.png' },
  // Sermons / messages / preaching
  { paths: ['/sermons', '/sermon-archive', '/messages', '/preaching', '/teaching', '/watch', '/listen', '/media', '/podcast'], label: 'Sermons', icon: 'shield-bible.png' },
  // Staff / leadership
  { paths: ['/staff', '/our-staff', '/team', '/our-team', '/leadership', '/our-leadership', '/elders', '/our-elders', '/pastors', '/our-pastors'], label: 'Leadership', icon: 'shield-about-person-48.png' },
  // About / story
  { paths: ['/about', '/about-us', '/who-we-are', '/our-story', '/history'], label: 'About', icon: 'shield-handshake.png' },
  // Visit / connect
  { paths: ['/visit', '/plan-a-visit', '/plan-your-visit', '/new-here', '/im-new', '/i-am-new', '/connect', '/get-connected'], label: 'Visit', icon: 'shield-handshake.png' },
  // Events / calendar
  { paths: ['/events', '/calendar', '/upcoming'], label: 'Events', icon: 'shield-calendar.png' },
  // Giving
  { paths: ['/give', '/giving', '/donate', '/tithe'], label: 'Give', icon: 'shield-heart.png' },
  // Men's ministry (high-signal for MOOP audience)
  { paths: ['/mens-ministry', '/men', '/mens', '/mens-group', '/men-of-the-church'], label: "Men's Ministry", icon: 'shield-cross.png' },
  // Kids
  { paths: ['/kids', '/childrens-ministry', '/childrens', '/children', '/kids-ministry'], label: "Kids Ministry", icon: 'shield-cross.png' },
];

function parseArgs() {
  const out = { state: null, count: null, jsonl: DEFAULT_JSONL };
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--state') out.state = a[++i].toUpperCase();
    else if (a[i] === '--count') out.count = parseInt(a[++i], 10);
    else if (a[i] === '--jsonl') out.jsonl = a[++i];
  }
  return out;
}

function probeOnce(urlStr) {
  return new Promise(resolve => {
    let u;
    try { u = new URL(urlStr); } catch (e) { return resolve({ ok: false, reason: 'BAD_URL' }); }
    const lib = u.protocol === 'http:' ? http : https;
    const req = lib.request({
      method: 'HEAD',
      hostname: u.hostname,
      port: u.port || undefined,
      path: u.pathname + (u.search || ''),
      headers: { 'User-Agent': UA, 'Accept': 'text/html,*/*' },
      timeout: PROBE_TIMEOUT_MS,
    }, res => {
      // Follow 301/302 transparently — record the FINAL url
      if ((res.statusCode === 301 || res.statusCode === 302 || res.statusCode === 308) && res.headers.location) {
        const finalUrl = new URL(res.headers.location, u).href;
        // Single redirect hop only — avoid infinite loops
        return resolve(probeOnce(finalUrl).then(r => ({ ...r, redirected_to: finalUrl })));
      }
      resolve({ ok: res.statusCode === 200, status: res.statusCode, url: urlStr });
    });
    req.on('error', () => resolve({ ok: false, reason: 'NET' }));
    req.on('timeout', () => { req.destroy(); resolve({ ok: false, reason: 'TIMEOUT' }); });
    req.end();
  });
}

async function main() {
  const args = parseArgs();
  console.log(`Loading ${CHURCHES} ...`);
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
    if (!c.website || !/^https?:\/\/[^\/\s]/i.test(c.website)) continue;
    // Skip if a quick_links array is already on the record
    if (Array.isArray(c.quick_links) && c.quick_links.length > 0) continue;
    todo.push(c);
  }
  // Fredericksburg-first stable sort within state scope
  todo.sort((a, b) => {
    const af = /Fredericksburg/i.test(a.address || '') ? 0 : 1;
    const bf = /Fredericksburg/i.test(b.address || '') ? 0 : 1;
    return af - bf;
  });
  if (args.count) todo.splice(args.count);

  console.log(`State filter: ${stateFilter || 'ALL'}`);
  console.log(`Churches to probe: ${todo.length}`);
  console.log(`Per-church paths: ~${PATH_PROBES.reduce((n, p) => n + p.paths.length, 0)}`);
  console.log(`Polite delay: ${POLITE_DELAY_MS}ms between churches`);
  if (!todo.length) { console.log('Nothing to do.'); return; }

  let okCount = 0, failCount = 0, totalLinks = 0;
  const start = Date.now();

  for (let i = 0; i < todo.length; i++) {
    const c = todo[i];
    if (i > 0) await new Promise(r => setTimeout(r, POLITE_DELAY_MS));
    process.stdout.write(`[${i+1}/${todo.length}] ${c.name.slice(0,40).padEnd(40)} `);

    const base = c.website.replace(/\/+$/, '');
    const found = [];
    let probedThisChurch = 0;

    // Probe all path-groups in parallel; within each group, probe all paths
    // in parallel and take the first successful 200. This is the big speedup
    // vs. the prior sequential version: a 9-group church is now bounded by
    // a single ~4.5s timeout window rather than 30+ sequential probes.
    const groupResults = await Promise.all(PATH_PROBES.map(async probe => {
      const probes = probe.paths.map(p => ({ url: base + p, label: probe.label, icon: probe.icon }));
      probedThisChurch += probes.length;
      const responses = await Promise.all(probes.map(async pp => {
        const r = await probeOnce(pp.url);
        return r.ok ? { ok: true, hit: pp, finalUrl: r.redirected_to || pp.url } : { ok: false };
      }));
      const winner = responses.find(r => r.ok);
      return winner ? { label: winner.hit.label, icon: winner.hit.icon, url: winner.finalUrl } : null;
    }));
    for (const g of groupResults) if (g) found.push(g);

    const result = { id: c.id || c.slug, quick_links: found, probed_at: new Date().toISOString(), paths_tried: probedThisChurch };
    fs.appendFileSync(args.jsonl, JSON.stringify(result) + '\n');

    if (found.length > 0) {
      okCount++;
      totalLinks += found.length;
      console.log(`OK ${found.length} link(s): ${found.map(f => f.label).join(', ')}`);
    } else {
      failCount++;
      console.log('no links found');
    }
  }

  const dt = ((Date.now() - start) / 1000).toFixed(0);
  console.log(`\nDone in ${dt}s. ${okCount}/${todo.length} churches got links (${totalLinks} total links).`);
  console.log(`Run merge-church-quicklinks.js to apply results from ${args.jsonl} to churches.json.`);
}

main().catch(e => { console.error(e); process.exit(1); });
