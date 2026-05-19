#!/usr/bin/env node
// Generate personalized outreach email DRAFTS for the website-build candidates.
// Reads docs/data/research-leads/website-outreach-candidates.json (curated)
// and emits one personalized email per candidate to /tmp/outreach-drafts.txt.
//
// IMPORTANT: This script ONLY generates drafts. It does NOT send anything.
// The user must review and send these personally — see
// docs/data/research-leads/OUTREACH-EMAIL-TEMPLATE.md for the source
// template and persona/voice guidelines.
//
// Usage:
//   node scripts/draft-outreach-emails.js [--top N] [--out path]
//   defaults: --top 20  --out /tmp/outreach-drafts.txt

const fs = require('fs');
const path = require('path');

const CANDIDATES = path.join(__dirname, '..', 'docs', 'data', 'research-leads', 'website-outreach-candidates.json');

let topN = 20;
let outPath = '/tmp/outreach-drafts.txt';
const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--top') topN = parseInt(args[++i], 10);
  if (args[i] === '--out') outPath = args[++i];
}

const cands = JSON.parse(fs.readFileSync(CANDIDATES, 'utf8'));
const top = cands.slice(0, topN);

const STATE_NAMES = 'Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming|District of Columbia';

function extractCity(address) {
  if (!address) return null;
  // Format 1: "...Street, City StateName, ..." (most common in our data)
  const m1 = address.match(new RegExp(`,\\s*([A-Z][A-Za-z\\s\\.\\-]+?)\\s+(?:${STATE_NAMES})\\b`));
  if (m1) return m1[1].trim();
  // Format 2: "...Street, City StateCode ZIP, ..."
  const m2 = address.match(/,\s*([A-Z][A-Za-z\s\.\-]+?)\s+[A-Z]{2}\s+\d{5}/);
  if (m2) return m2[1].trim();
  // Format 3: "...Street, City, ST 12345"
  const m3 = address.match(/,\s*([A-Z][A-Za-z\s\.\-]+?),\s*[A-Z]{2}\s*\d{5}/);
  if (m3) return m3[1].trim();
  // Format 4: "...Street, City, ST" (no zip)
  const m4 = address.match(/,\s*([A-Z][A-Za-z\s\.\-]+?),\s*[A-Z]{2}\b/);
  if (m4) return m4[1].trim();
  return null;
}

function inferContactPath(c) {
  // Best contact source we have. Prefer the original (defunct) URL since
  // it likely still points to whois/registrar lookup, and the email at the
  // domain often still works even after the website is down.
  if (c.facebook) return `Facebook page (${c.facebook})`;
  if (c.source_url) return `original website domain (${c.source_url}) — try info@, pastor@, or office@ at that domain`;
  return 'church via address';
}

function draftEmailFor(c) {
  const city = extractCity(c.address) || 'your area';
  const churchName = c.name || 'your church';
  const contactPath = inferContactPath(c);

  return `=================================================================
TO:      ${contactPath}
SUBJECT: A small offer for ${churchName}

Pastor / Brothers in ${churchName},

Grace and peace from a fellow pastor down the road. I lead a small
ministry that walks alongside under-resourced churches in the work of
faithful gospel presentation online — particularly when a website has
gone down or never quite gotten built in the first place.

I came across ${churchName} in ${city} while compiling a directory of
faithful, gospel-preaching congregations across the United States. Your
church belongs in that company, but the website I had on file for you
isn't loading right now. That's a small thing in eternity, but it does
make it harder for a visiting traveler or a curious neighbor to find
your service times, your statement of faith, or your pastor's name.

If it would be useful, I'd be glad to build you a simple, durable
landing page for $100, one-time — name, address, service times,
beliefs, pastor, and a phone number. That's the whole offer; I'm not
trying to sell you a system. Hosting and basic upkeep after that we
can work out for a token monthly fee, or you can take the files and
host them yourselves. Whatever serves the church.

If this is a help, just reply and I'll send a one-page intake form.
If it isn't, I rejoice with you in whatever the Lord is doing locally
and will not bother you again.

In the bonds of the gospel,

Pastor John Wesley Graves
USMC Ministries — a ministry of helps
usmcministries2022+preacher@gmail.com

P.S. Editorial context for this church record (for the reviewer's eyes):
  ID:                 ${c.id}
  Denomination:       ${c.denomination || 'unknown'}
  Network listings:   ${(c.cross_listed_in || []).join(', ') || 'none'}
  MOOP rating:        ${c.overall_rating || 'unrated'}
  Signatures signal:  ${c.signatures_aggregate || 'none'}
`;
}

const drafts = top.map(draftEmailFor).join('\n');
fs.writeFileSync(outPath, drafts);

console.log(`Drafted ${top.length} outreach emails -> ${outPath}`);
console.log(`Top ${topN} candidates by editorial priority:`);
for (let i = 0; i < top.length; i++) {
  const c = top[i];
  const tag = c.signatures_aggregate === 'green' ? ' SIG-G' : c.signatures_aggregate === 'red' ? ' SIG-R' : '';
  console.log(`  ${String(i + 1).padStart(2)}. ${(c.name || '').slice(0, 45).padEnd(45)} ${(c.address || '').slice(0, 30).padEnd(30)} [${c.overall_rating}${tag}]`);
}
console.log('\nReview at:', outPath);
console.log('Reminder: these are DRAFTS only. Do NOT auto-send. The user reviews + sends personally.');
