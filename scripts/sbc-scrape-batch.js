#!/usr/bin/env node
// Stage 3 of SBC bulk-load: scrape individual SBC church pages, respecting
// the site's 10-second crawl-delay (we use 11s buffer).
//
// Usage:
//   node sbc-scrape-batch.js --start 0 --count 100
//   node sbc-scrape-batch.js --resume
//
// Output:
//   /tmp/sbc-scraped/batch-<start>-<end>.jsonl — one church record per line
//   /tmp/sbc-scrape-progress.json — { last_index, fetched, failed }
//
// Each fetched record contains: { url, slug, name, city, state, zip,
// raw_address, fetched_at, fetch_error? }
//
// Crash-safe: writes to .jsonl one line at a time (appended), so killing
// the process mid-batch leaves the partial work intact. Re-run with
// --resume to continue from the next URL after the last successful write.

const fs = require('fs');
const https = require('https');
const path = require('path');

const TODO = '/tmp/sbc-todo.json';
const OUT_DIR = '/tmp/sbc-scraped';
const PROGRESS = '/tmp/sbc-scrape-progress.json';

const DELAY_MS = 11_000; // 11s; SBC robots.txt asks for 10s, we add 1s buffer
const UA = 'MOOP-Church-Directory-Scraper/1.0 (contact: bowandarrowstudiollc@gmail.com)';

if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

function parseArgs() {
  const a = process.argv.slice(2);
  const out = { start: null, count: null, resume: false };
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--start') out.start = parseInt(a[++i], 10);
    else if (a[i] === '--count') out.count = parseInt(a[++i], 10);
    else if (a[i] === '--resume') out.resume = true;
  }
  return out;
}

function fetchText(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { headers: { 'User-Agent': UA }, timeout: 30_000 }, res => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        // Don't follow redirects automatically — note and move on
        return reject(new Error(`Redirect ${res.statusCode} → ${res.headers.location || '?'}`));
      }
      if (res.statusCode !== 200) {
        return reject(new Error(`HTTP ${res.statusCode}`));
      }
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => resolve(body));
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('TIMEOUT')); });
  });
}

// SBC.net church pages are WordPress with the church name in the H1 / title
// and the address in the body. Extract conservatively — if we can't be sure,
// flag it rather than guessing.
function parseChurchPage(html, slug) {
  const result = { name: null, city: null, state: null, zip: null, raw_address: null };

  // Title pattern: usually "<Name> - SBC Churches Directory"
  const titleMatch = html.match(/<title>([^<]+?)\s*[-–|]\s*SBC Churches Directory<\/title>/i)
                  || html.match(/<title>([^<]+?)<\/title>/i);
  if (titleMatch) result.name = titleMatch[1].trim();

  // Fallback: H1
  if (!result.name) {
    const h1 = html.match(/<h1[^>]*>([^<]+)<\/h1>/i);
    if (h1) result.name = h1[1].trim();
  }

  // Address: look for a US-style "City, ST 12345" pattern in the body
  // The SBC pages typically render this in a simple paragraph
  const addrPatterns = [
    /([A-Z][A-Za-z\s\.\-']+),\s*([A-Z]{2})\s+(\d{5})(?:-\d{4})?/g,
    /([A-Z][A-Za-z\s\.\-']+),\s*([A-Z]{2})\b/g,
  ];
  for (const rx of addrPatterns) {
    const matches = [...html.matchAll(rx)];
    // Skip matches that are inside <script> blocks (false positives)
    for (const m of matches) {
      const idx = m.index;
      const before = html.slice(Math.max(0, idx - 200), idx);
      if (/<script[^>]*>[^<]*$/i.test(before)) continue;
      const cityCandidate = m[1].trim();
      // City names that are clearly noise — skip
      if (/copyright|all rights|terms|privacy|©|powered by/i.test(cityCandidate)) continue;
      if (cityCandidate.length < 2 || cityCandidate.length > 40) continue;
      result.city = cityCandidate;
      result.state = m[2];
      result.zip = m[3] || null;
      result.raw_address = m[0];
      break;
    }
    if (result.city) break;
  }

  return result;
}

function appendJsonl(file, obj) {
  fs.appendFileSync(file, JSON.stringify(obj) + '\n');
}

function readScrapedSlugs() {
  // Read all .jsonl files in OUT_DIR and return a set of slugs already done
  const done = new Set();
  for (const f of fs.readdirSync(OUT_DIR)) {
    if (!f.endsWith('.jsonl')) continue;
    const lines = fs.readFileSync(path.join(OUT_DIR, f), 'utf8').split('\n').filter(Boolean);
    for (const line of lines) {
      try {
        const o = JSON.parse(line);
        if (o.slug) done.add(o.slug);
      } catch {}
    }
  }
  return done;
}

async function main() {
  const args = parseArgs();
  const todoData = JSON.parse(fs.readFileSync(TODO, 'utf8'));
  const urls = todoData.urls;
  console.log(`TODO: ${urls.length} URLs total.`);

  let start, end;
  if (args.resume) {
    const done = readScrapedSlugs();
    console.log(`Resume: ${done.size} slugs already scraped.`);
    // Find the first index in urls whose slug is NOT in done
    const firstUnscraped = urls.findIndex(u => !done.has(u.slug));
    if (firstUnscraped === -1) {
      console.log('All URLs already scraped. Nothing to do.');
      return;
    }
    start = firstUnscraped;
    end = args.count ? Math.min(start + args.count, urls.length) : urls.length;
  } else {
    start = args.start !== null ? args.start : 0;
    end = args.count !== null ? Math.min(start + args.count, urls.length) : urls.length;
  }
  console.log(`Scraping range: ${start} … ${end} (${end - start} URLs)`);

  const outFile = path.join(OUT_DIR, `batch-${String(start).padStart(6, '0')}-${String(end).padStart(6, '0')}.jsonl`);
  console.log(`Output: ${outFile}`);

  const doneSlugs = readScrapedSlugs();
  let fetched = 0;
  let failed = 0;
  let skipped = 0;
  const startTime = Date.now();

  for (let i = start; i < end; i++) {
    const item = urls[i];
    if (doneSlugs.has(item.slug)) {
      skipped++;
      continue;
    }
    if (fetched > 0 || failed > 0) {
      // Wait the polite delay between fetches (not before the first)
      await new Promise(r => setTimeout(r, DELAY_MS));
    }
    try {
      const html = await fetchText(item.url);
      const parsed = parseChurchPage(html, item.slug);
      const rec = {
        url: item.url,
        slug: item.slug,
        ...parsed,
        fetched_at: new Date().toISOString(),
      };
      appendJsonl(outFile, rec);
      fetched++;
      if (fetched % 10 === 0) {
        const elapsedMin = ((Date.now() - startTime) / 60_000).toFixed(1);
        const ratePerMin = fetched / Math.max(1, (Date.now() - startTime) / 60_000);
        const remaining = end - i - 1;
        const etaMin = (remaining / ratePerMin).toFixed(0);
        console.log(`  [${i}/${end}] ${item.slug}  →  ${parsed.name || '?'} / ${parsed.city || '?'}, ${parsed.state || '?'}  · ${fetched} ok / ${failed} fail  · ${elapsedMin}m elapsed, ~${etaMin}m remaining`);
      }
    } catch (e) {
      appendJsonl(outFile, {
        url: item.url,
        slug: item.slug,
        fetch_error: e.message,
        fetched_at: new Date().toISOString(),
      });
      failed++;
      console.warn(`  [${i}/${end}] ${item.slug}  ✗ ${e.message}`);
    }

    // Update progress sidecar every 10 fetches
    if ((fetched + failed) % 10 === 0) {
      fs.writeFileSync(PROGRESS, JSON.stringify({
        last_index: i,
        last_slug: item.slug,
        fetched,
        failed,
        skipped,
        updated_at: new Date().toISOString(),
      }, null, 2));
    }
  }

  fs.writeFileSync(PROGRESS, JSON.stringify({
    last_index: end - 1,
    fetched,
    failed,
    skipped,
    completed_range: [start, end],
    completed_at: new Date().toISOString(),
  }, null, 2));

  const elapsedMin = ((Date.now() - startTime) / 60_000).toFixed(1);
  console.log(`\nDone. ${fetched} fetched, ${failed} failed, ${skipped} skipped. ${elapsedMin}m elapsed.`);
}

main().catch(e => { console.error(e); process.exit(1); });
