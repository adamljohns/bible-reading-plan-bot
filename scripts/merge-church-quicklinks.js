#!/usr/bin/env node
//
// merge-church-quicklinks.js — fold scrape-church-quicklinks.js results into
// churches.json. Same idempotent JSONL merge pattern as image / pastor.
//

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const JSONL = process.argv[2] || '/tmp/quicklinks-scrapes.jsonl';

if (!fs.existsSync(JSONL)) { console.error(`No JSONL at ${JSONL}`); process.exit(1); }

const results = new Map();
for (const l of fs.readFileSync(JSONL, 'utf8').split('\n').filter(Boolean)) {
  try {
    const r = JSON.parse(l);
    if (r.id) results.set(r.id, r);
  } catch (e) {}
}
console.log(`Loaded ${results.size} unique church results from ${JSONL}`);

const data = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
let touched = 0, linksTotal = 0;
for (const c of data.churches) {
  const cid = c.id || c.slug;
  const r = results.get(cid);
  if (!r) continue;
  // Skip churches that already have a curated quick_links array (preserve manual edits)
  if (Array.isArray(c.quick_links) && c.quick_links.length > 0 && !c._quicklinks_auto) continue;
  if (Array.isArray(r.quick_links) && r.quick_links.length > 0) {
    c.quick_links = r.quick_links;
    c._quicklinks_auto = r.probed_at;
    touched++;
    linksTotal += r.quick_links.length;
  }
}

fs.writeFileSync(CHURCHES, JSON.stringify(data, null, 2) + '\n');
console.log(`Updated ${touched} churches with ${linksTotal} total quick links.`);
