#!/usr/bin/env node
// scripts/merge-pastor-scrapes.js — apply pastor-scrape JSONL to churches.json.
// Same race-free pattern as merge-image-scrapes.js and merge-sbc-detail.js.

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const DEFAULT_JSONL = '/tmp/pastor-scrapes.jsonl';

function parseArgs() {
  const out = { jsonl: DEFAULT_JSONL, force: false };
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--jsonl') out.jsonl = a[++i];
    else if (a[i] === '--force') out.force = true;
  }
  return out;
}

const PLACEHOLDER = /^(verify|various|unknown|see\s+website|currently|none|listed|tbd|n\/a|the\s+pastor|the\s+church|various\s+pastors|pastoral)/i;

function main() {
  const args = parseArgs();
  if (!fs.existsSync(args.jsonl)) {
    console.log(`No JSONL at ${args.jsonl} — nothing to merge.`);
    return;
  }
  const lines = fs.readFileSync(args.jsonl, 'utf8').split('\n').filter(Boolean);
  const data = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
  const byId = new Map();
  for (const c of data.churches) byId.set(c.id || c.slug, c);

  let applied = 0, added = 0, missing = 0, skipped = 0;
  for (const line of lines) {
    let r; try { r = JSON.parse(line); } catch (e) { continue; }
    const c = byId.get(r.id);
    if (!c) { missing++; continue; }
    if (r.pastor) {
      // Only overwrite placeholder pastors, never a curated/real pastor
      const cur = c.pastor && String(c.pastor).trim();
      if (!cur || PLACEHOLDER.test(cur) || cur.length < 5 || args.force) {
        c.pastor = r.pastor;
        c.pastor_source = r.pastor_source || 'website-scrape';
        added++;
      } else {
        skipped++;
      }
    }
    if (r.pastor_fetched_at) c.pastor_fetched_at = r.pastor_fetched_at;
    if (r.pastor_scrape_error) c.pastor_scrape_error = r.pastor_scrape_error;
    applied++;
  }
  fs.writeFileSync(CHURCHES, JSON.stringify(data, null, 2));

  console.log(`Applied ${applied} pastor-scrape results from ${args.jsonl}`);
  console.log(`  +${added} pastor names written`);
  console.log(`  ${skipped} skipped (existing curated pastor preserved)`);
  if (missing) console.log(`  ${missing} JSONL records had no matching church.id`);

  // Coverage check
  const real = data.churches.filter(c => c.pastor && !PLACEHOLDER.test(c.pastor.trim()) && c.pastor.length > 4).length;
  console.log(`\nReal-pastor coverage now: ${real} / ${data.churches.length} (${Math.round(real/data.churches.length*100)}%)`);
}

main();
