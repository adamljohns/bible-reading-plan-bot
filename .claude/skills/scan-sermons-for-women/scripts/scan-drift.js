#!/usr/bin/env node
//
// scan-drift.js — scan a church's sermon archive (and homepage/beliefs page)
// for drift signals across the 10 MOOP rubric categories. Companion to
// scan-archive.js (which focuses on female-preacher detection). Produces a
// JSONL review queue scored by signal strength.
//
// HEURISTIC ONLY. Every hit needs human confirmation — a faithful church may
// preach critically ABOUT these topics. Output is a review queue, never an
// automated rating change.
//
// Usage:
//   node scan-drift.js --state VA --count 50 --jsonl /tmp/drift-scan.jsonl
//   node scan-drift.js --all --count 200
//

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const REPO = path.join(__dirname, '..', '..', '..', '..');
const CHURCHES = path.join(REPO, 'docs', 'data', 'churches.json');
const LEX = path.join(__dirname, '..', 'data', 'drift-lexicon.json');
const DEFAULT_JSONL = '/tmp/drift-scan.jsonl';
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36 MOOP-Doctrinal-Vetting/1.0';
const TIMEOUT = 15000;

function parseArgs() {
  const out = { state: null, all: false, count: null, jsonl: DEFAULT_JSONL };
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--state') out.state = a[++i].toUpperCase();
    else if (a[i] === '--all') out.all = true;
    else if (a[i] === '--count') out.count = parseInt(a[++i], 10);
    else if (a[i] === '--jsonl') out.jsonl = a[++i];
  }
  return out;
}

function fetchText(url, redirs = 0) {
  return new Promise(resolve => {
    let u; try { u = new URL(url); } catch (e) { return resolve(null); }
    const lib = u.protocol === 'http:' ? http : https;
    const req = lib.get(url, { headers: { 'User-Agent': UA, 'Accept': 'text/html,*/*' }, timeout: TIMEOUT }, res => {
      if ((res.statusCode === 301 || res.statusCode === 302) && res.headers.location && redirs < 3) {
        return resolve(fetchText(new URL(res.headers.location, u).href, redirs + 1));
      }
      if (res.statusCode !== 200) return resolve(null);
      let b = ''; res.on('data', c => b += c); res.on('end', () => resolve(b));
    });
    req.on('error', () => resolve(null));
    req.on('timeout', () => { req.destroy(); resolve(null); });
  });
}

function stripTags(html) {
  return String(html || '')
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&')
    .replace(/\s+/g, ' ').toLowerCase();
}

async function scanOne(church, signals) {
  // Scan the Sermons quicklink if present, else the church homepage + any Beliefs link.
  const ql = Array.isArray(church.quick_links) ? church.quick_links : [];
  const urls = [];
  const sermons = ql.find(l => l && l.label === 'Sermons');
  const beliefs = ql.find(l => l && l.label === 'Beliefs');
  if (sermons) urls.push(sermons.url);
  if (beliefs) urls.push(beliefs.url);
  if (!urls.length && church.website) urls.push(church.website);
  if (!urls.length) return { id: church.id || church.slug, name: church.name, hits: [], warning: 'no-url' };

  let text = '';
  for (const u of urls.slice(0, 2)) {
    const html = await fetchText(u);
    if (html) text += ' ' + stripTags(html);
  }
  if (text.length < 200) return { id: church.id || church.slug, name: church.name, hits: [], warning: 'empty-or-js' };

  const hits = [];
  for (const sig of signals) {
    const idx = text.indexOf(sig.phrase);
    if (idx >= 0) {
      const ctx = text.slice(Math.max(0, idx - 50), idx + sig.phrase.length + 50).trim();
      hits.push({ phrase: sig.phrase, category: sig.category, weight: sig.weight, note: sig.note, context: ctx });
    }
  }
  return { id: church.id || church.slug, name: church.name, rating: church.overall_rating, hits, warning: null, scanned_at: new Date().toISOString() };
}

async function main() {
  const args = parseArgs();
  const signals = JSON.parse(fs.readFileSync(LEX, 'utf8')).signals;
  const data = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));

  let pool = data.churches;
  if (args.state) pool = pool.filter(c => new RegExp(',\\s*' + args.state + '\\b').test(c.address || ''));
  else if (!args.all) { console.error('Specify --state or --all'); process.exit(1); }
  // Only churches we can actually read: has a Sermons/Beliefs quicklink or a website
  pool = pool.filter(c => (Array.isArray(c.quick_links) && c.quick_links.some(l => l && (l.label === 'Sermons' || l.label === 'Beliefs'))) || (c.website && /^https?:/.test(c.website)));

  const done = new Set();
  if (fs.existsSync(args.jsonl)) {
    for (const l of fs.readFileSync(args.jsonl, 'utf8').split('\n').filter(Boolean)) { try { done.add(JSON.parse(l).id); } catch (e) {} }
    console.log('Already scanned: ' + done.size);
  }
  pool = pool.filter(c => !done.has(c.id || c.slug));
  if (args.count) pool = pool.slice(0, args.count);

  console.log('Churches to scan for drift: ' + pool.length);
  if (!pool.length) { console.log('Nothing to do.'); return; }

  let withHits = 0;
  for (let i = 0; i < pool.length; i++) {
    const c = pool[i];
    process.stdout.write('[' + (i+1) + '/' + pool.length + '] ' + (c.name||'').slice(0,38).padEnd(38) + ' ');
    const r = await scanOne(c, signals);
    fs.appendFileSync(args.jsonl, JSON.stringify(r) + '\n');
    if (r.warning) console.log('skip:' + r.warning);
    else if (r.hits.length) { withHits++; console.log(r.hits.length + ' signal(s): ' + [...new Set(r.hits.map(h => h.category))].join(',')); }
    else console.log('clean');
    await new Promise(s => setTimeout(s, 1200));
  }
  console.log('\nDone. ' + withHits + '/' + pool.length + ' churches flagged with drift signals.');
  console.log('Review with: bash .claude/skills/scan-sermons-for-women/scripts/review-drift.sh ' + args.jsonl);
}

main().catch(e => { console.error(e); process.exit(1); });
