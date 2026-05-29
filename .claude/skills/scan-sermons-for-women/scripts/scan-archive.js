#!/usr/bin/env node
//
// scan-archive.js — fetch each in-scope church's quick_links 'Sermons' URL
// and extract apparent preacher names for human review. Produces a JSONL
// review queue at /tmp/sermon-scan.jsonl.
//
// Usage:
//   node scan-archive.js --state VA --count 50
//   node scan-archive.js --church faith-baptist-church-fredericksburg
//   node scan-archive.js --all --count 200
//
// This is a HEURISTIC scanner. Every flag needs human confirmation before
// a church's overall_rating moves. See SKILL.md for the doctrinal context.
//

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const REPO_ROOT = path.join(__dirname, '..', '..', '..', '..');
const CHURCHES = path.join(REPO_ROOT, 'docs', 'data', 'churches.json');
const NAMES_DB = path.join(__dirname, '..', 'data', 'first-names-gender.json');
const DEFAULT_JSONL = '/tmp/sermon-scan.jsonl';
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36 MOOP-Doctrinal-Vetting/1.0';
const FETCH_TIMEOUT_MS = 15_000;

// Titles that introduce a preacher's name. The pattern matcher uses these
// as anchors. Order matters: longer titles first so 'Pastor' does not eat
// 'Sr Pastor'.
const PREACHER_TITLES = [
  'Senior Pastor', 'Lead Pastor', 'Pastor Emeritus', 'Associate Pastor',
  'Teaching Pastor', 'Pastor', 'Rev. Dr.', 'Rev.', 'Reverend',
  'Dr.', 'Bishop', 'Bro.', 'Brother', 'Sis.', 'Sister',
  'Mother', 'Father', 'Elder', 'Minister', 'Speaker'
];

// Lead-in phrases for sermon attribution
const ATTRIBUTION_PATTERNS = [
  /\bpreached?\s+by\s+([A-Z][a-zA-Z'\-\.]+(?:\s+[A-Z][a-zA-Z'\-\.]+){0,3})/g,
  /\bspeaker\s*[:\-]?\s*([A-Z][a-zA-Z'\-\.]+(?:\s+[A-Z][a-zA-Z'\-\.]+){0,3})/gi,
  /\bsermon\s+by\s+([A-Z][a-zA-Z'\-\.]+(?:\s+[A-Z][a-zA-Z'\-\.]+){0,3})/gi,
  /\bmessage\s+by\s+([A-Z][a-zA-Z'\-\.]+(?:\s+[A-Z][a-zA-Z'\-\.]+){0,3})/gi,
  /\bdelivered\s+by\s+([A-Z][a-zA-Z'\-\.]+(?:\s+[A-Z][a-zA-Z'\-\.]+){0,3})/gi
];

function parseArgs() {
  const out = { state: null, church: null, all: false, count: null, jsonl: DEFAULT_JSONL };
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--state') out.state = a[++i].toUpperCase();
    else if (a[i] === '--church') out.church = a[++i];
    else if (a[i] === '--all') out.all = true;
    else if (a[i] === '--count') out.count = parseInt(a[++i], 10);
    else if (a[i] === '--jsonl') out.jsonl = a[++i];
  }
  return out;
}

function fetchText(url) {
  return new Promise((resolve, reject) => {
    let u;
    try { u = new URL(url); } catch (e) { return reject(new Error('BAD_URL')); }
    const lib = u.protocol === 'http:' ? http : https;
    const req = lib.get(url, { headers: { 'User-Agent': UA, 'Accept': 'text/html,*/*' }, timeout: FETCH_TIMEOUT_MS }, res => {
      if ((res.statusCode === 301 || res.statusCode === 302) && res.headers.location) {
        return resolve(fetchText(new URL(res.headers.location, u).href));
      }
      if (res.statusCode !== 200) return reject(new Error('HTTP_' + res.statusCode));
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => resolve(body));
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('TIMEOUT')); });
  });
}

function stripTags(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function classifyName(firstName, namesDb) {
  const lower = firstName.toLowerCase();
  if (namesDb.U.includes(lower)) return { gender: 'U', confidence: 'uncertain' };
  if (namesDb.F.includes(lower)) return { gender: 'F', confidence: 'high' };
  if (namesDb.M.includes(lower)) return { gender: 'M', confidence: 'high' };
  return { gender: '?', confidence: 'unknown' };
}

function extractNames(text, namesDb) {
  const hits = new Map(); // key = full name lowercase, val = hit record

  // Pattern 1: <Title> <FirstName> [<Middle>] <LastName>
  const titleAlt = PREACHER_TITLES.map(t => t.replace(/\./g, '\\.')).join('|');
  const titleRe = new RegExp('\\b(' + titleAlt + ')\\s+([A-Z][a-zA-Z\'\\-]+(?:\\s+[A-Z][a-zA-Z\'\\-\\.]+){0,2})', 'g');
  let m;
  while ((m = titleRe.exec(text)) !== null) {
    const title = m[1].trim();
    const nameSeq = m[2].trim();
    const parts = nameSeq.split(/\s+/);
    const first = parts[0].replace(/[^A-Za-z\-']/g, '');
    if (!first) continue;
    const cls = classifyName(first, namesDb);
    const ctxStart = Math.max(0, m.index - 60);
    const ctxEnd = Math.min(text.length, m.index + m[0].length + 60);
    const context = text.slice(ctxStart, ctxEnd).trim();
    const key = (title + ' ' + nameSeq).toLowerCase();
    if (!hits.has(key)) {
      hits.set(key, {
        name: nameSeq,
        first,
        title,
        context,
        gender: cls.gender,
        confidence: cls.confidence
      });
    }
  }

  // Pattern 2: Attribution-phrase based extraction
  for (const pat of ATTRIBUTION_PATTERNS) {
    pat.lastIndex = 0;
    while ((m = pat.exec(text)) !== null) {
      const nameSeq = m[1].trim();
      const parts = nameSeq.split(/\s+/);
      const first = parts[0].replace(/[^A-Za-z\-']/g, '');
      if (!first || first.length < 2) continue;
      const cls = classifyName(first, namesDb);
      const ctxStart = Math.max(0, m.index - 60);
      const ctxEnd = Math.min(text.length, m.index + m[0].length + 60);
      const context = text.slice(ctxStart, ctxEnd).trim();
      const key = nameSeq.toLowerCase();
      if (!hits.has(key)) {
        hits.set(key, {
          name: nameSeq,
          first,
          title: null,
          context,
          gender: cls.gender,
          confidence: cls.confidence
        });
      }
    }
  }

  return [...hits.values()];
}

function isLikelyJsRendered(html) {
  // Heuristic: if the visible text is tiny but the HTML has lots of React /
  // Vue / Squarespace / Wix markers, assume JS-rendered.
  const text = stripTags(html);
  const ratio = text.length / Math.max(html.length, 1);
  const jsMarkers = (html.match(/react-root|squarespace|wix-app|__NEXT_DATA__|<noscript>|app-root|ng-app/gi) || []).length;
  return ratio < 0.05 && jsMarkers >= 2;
}

async function scanOne(church, namesDb) {
  const sermonsLink = (church.quick_links || []).find(l => l && l.label === 'Sermons');
  if (!sermonsLink) {
    return { id: church.id || church.slug, name: church.name, archive_url: null, warning: 'no-sermons-quicklink', name_hits: [] };
  }
  const archiveUrl = sermonsLink.url;
  try {
    const html = await fetchText(archiveUrl);
    if (isLikelyJsRendered(html)) {
      return { id: church.id || church.slug, name: church.name, archive_url: archiveUrl, warning: 'likely-js-rendered', name_hits: [], scanned_at: new Date().toISOString() };
    }
    const text = stripTags(html);
    if (text.length < 200) {
      return { id: church.id || church.slug, name: church.name, archive_url: archiveUrl, warning: 'empty-archive', name_hits: [], scanned_at: new Date().toISOString() };
    }
    const hits = extractNames(text, namesDb);
    return { id: church.id || church.slug, name: church.name, archive_url: archiveUrl, warning: null, name_hits: hits, scanned_at: new Date().toISOString() };
  } catch (e) {
    return { id: church.id || church.slug, name: church.name, archive_url: archiveUrl, warning: 'fetch-failed:' + (e.message || 'unknown').slice(0,40), name_hits: [], scanned_at: new Date().toISOString() };
  }
}

async function main() {
  const args = parseArgs();
  const namesDb = JSON.parse(fs.readFileSync(NAMES_DB, 'utf8'));
  const data = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));

  // Build scope
  let pool = data.churches;
  if (args.church) {
    pool = pool.filter(c => (c.id || c.slug) === args.church);
  } else if (args.state) {
    pool = pool.filter(c => new RegExp(',\\s*' + args.state + '\\b').test(c.address || ''));
  } else if (!args.all) {
    console.error('Specify --state, --church, or --all');
    process.exit(1);
  }
  // Must have a Sermons quick_link
  pool = pool.filter(c => Array.isArray(c.quick_links) && c.quick_links.some(l => l && l.label === 'Sermons'));

  // Resume-safe: skip churches already in the JSONL
  const done = new Set();
  if (fs.existsSync(args.jsonl)) {
    for (const l of fs.readFileSync(args.jsonl, 'utf8').split('\n').filter(Boolean)) {
      try { done.add(JSON.parse(l).id); } catch (e) {}
    }
    console.log('Already scanned: ' + done.size);
  }
  pool = pool.filter(c => !done.has(c.id || c.slug));

  if (args.count) pool = pool.slice(0, args.count);

  console.log('Churches in scope to scan: ' + pool.length);
  if (!pool.length) { console.log('Nothing to do.'); return; }

  let ok = 0, fail = 0, totalHits = 0, femaleHits = 0;
  for (let i = 0; i < pool.length; i++) {
    const c = pool[i];
    process.stdout.write('[' + (i+1) + '/' + pool.length + '] ' + (c.name || '').slice(0,40).padEnd(40) + ' ');
    const result = await scanOne(c, namesDb);
    fs.appendFileSync(args.jsonl, JSON.stringify(result) + '\n');
    if (result.warning) {
      fail++;
      console.log('SKIP ' + result.warning);
    } else {
      ok++;
      const fHits = result.name_hits.filter(h => h.gender === 'F').length;
      const uHits = result.name_hits.filter(h => h.gender === 'U').length;
      const mHits = result.name_hits.filter(h => h.gender === 'M').length;
      totalHits += result.name_hits.length;
      femaleHits += fHits;
      console.log(result.name_hits.length + ' names (' + fHits + 'F / ' + uHits + 'U / ' + mHits + 'M)');
    }
    await new Promise(r => setTimeout(r, 1500));
  }

  console.log('\nDone. ' + ok + ' ok / ' + fail + ' skip. ' + totalHits + ' total names found, ' + femaleHits + ' female-high.');
  console.log('Review queue at ' + args.jsonl);
  console.log('Run: bash .claude/skills/scan-sermons-for-women/scripts/review.sh ' + args.jsonl);
}

main().catch(e => { console.error(e); process.exit(1); });
