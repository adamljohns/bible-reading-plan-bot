#!/usr/bin/env node
// SBC bulk-load progress monitor.
// Reads /tmp/sbc-todo.json, /tmp/sbc-scraped/*.jsonl, and the directory
// to report where we are vs. the SBC universe of 34,501 active congregations.

const fs = require('fs');
const path = require('path');

const TODO = '/tmp/sbc-todo.json';
const SCRAPED_DIR = '/tmp/sbc-scraped';
const CHURCHES = path.join(__dirname, '..', 'docs/data/churches.json');

const todoData = fs.existsSync(TODO) ? JSON.parse(fs.readFileSync(TODO, 'utf8')) : null;
const churches = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));

let scrapedTotal = 0;
let scrapedOk = 0;
let scrapedErr = 0;
const scrapedSlugs = new Set();
if (fs.existsSync(SCRAPED_DIR)) {
  for (const f of fs.readdirSync(SCRAPED_DIR)) {
    if (!f.endsWith('.jsonl')) continue;
    const lines = fs.readFileSync(path.join(SCRAPED_DIR, f), 'utf8').split('\n').filter(Boolean);
    for (const line of lines) {
      try {
        const o = JSON.parse(line);
        scrapedTotal++;
        if (o.fetch_error) scrapedErr++;
        else { scrapedOk++; if (o.slug) scrapedSlugs.add(o.slug); }
      } catch {}
    }
  }
}

const sbcInDirectory = churches.churches.filter(c => /SBC|Southern Baptist/i.test(c.denomination_family || '')).length;
const bulkLoadedCount = churches.churches.filter(c => c._sbc_bulkload).length;

console.log('=== SBC Bulk-Load Campaign Status ===');
console.log('');
if (todoData) {
  console.log(`Universe (SBC.net active sitemap):  ${todoData.count + (churches.churches.filter(c => /SBC|Southern Baptist/i.test(c.denomination_family || '') && !c._sbc_bulkload).length)} estimated`);
  console.log(`Net-new TODO (post-dedup):          ${todoData.count}`);
}
console.log(`Scraped so far:                     ${scrapedTotal}  (${scrapedOk} ok / ${scrapedErr} fail)`);
if (todoData) {
  const pct = ((scrapedOk / todoData.count) * 100).toFixed(1);
  console.log(`Scrape progress:                    ${pct}%`);
  const remaining = todoData.count - scrapedOk;
  const hoursRemaining = (remaining * 11 / 3600).toFixed(1);
  console.log(`Estimated time to complete (11s):   ${hoursRemaining} hours`);
}
console.log('');
console.log(`Bulk-loaded into churches.json:     ${bulkLoadedCount}`);
console.log(`Total SBC records in directory:     ${sbcInDirectory}`);
console.log(`Total churches in directory:        ${churches.churches.length}`);
console.log('');

// Progress file
const PROGRESS = '/tmp/sbc-scrape-progress.json';
if (fs.existsSync(PROGRESS)) {
  const p = JSON.parse(fs.readFileSync(PROGRESS, 'utf8'));
  console.log('Last scraper run:');
  console.log(`  Updated at: ${p.updated_at || p.completed_at}`);
  if (p.last_index !== undefined) console.log(`  Last index: ${p.last_index}`);
  if (p.last_slug) console.log(`  Last slug:  ${p.last_slug}`);
  if (p.completed_range) console.log(`  Completed range: [${p.completed_range[0]}, ${p.completed_range[1]}]`);
}
