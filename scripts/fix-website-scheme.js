#!/usr/bin/env node
// fix-website-scheme.js — repair church `website` fields that are not URLs.
//
// Two defect classes, both of which render as a RELATIVE href on the church
// page (`<a href="cbcws.org">`, `<a href="Verify">`) and therefore 404 against
// /churches/<junk>. Proven live 2026-10-03:
//   https://usmcmin.org/churches/falmouth-united-methodist-church.html -> 200
//   and contains href="Unknown"; https://usmcmin.org/churches/Unknown -> 404.
//
//   A. placeholder prose ("Verify", "Unknown", "N/A — church dissolved in 2014")
//      -> cleared to "". Nothing is invented; the record keeps needs_review.
//   B. bare domain ("cbcws.org", "www.fbcmarco.com")
//      -> promoted to https://<domain> ONLY when a live fetch proved it
//         resolves. Unreachable ones are cleared and marked _dead_site.
//
// Verdicts come from an HTTP sweep file (status<TAB>id<TAB>url); this script
// never guesses a reachability it did not observe.
//
// Usage: node fix-website-scheme.js <classA.tsv> <classB-http.tsv> [--apply]

const fs = require('fs');
const path = require('path');

const [, , aPath, bPath, ...rest] = process.argv;
const APPLY = rest.includes('--apply');
const DATA = path.join(__dirname, 'docs', 'data', 'churches.json');
const TODAY = new Date().toISOString().slice(0, 10);

const readTSV = p =>
  fs.readFileSync(p, 'utf8').split('\n').filter(l => l.trim() && !l.startsWith('DONE'))
    .map(l => l.split('\t'));

// id -> "" (placeholder prose)
const clearIds = new Map(readTSV(aPath).map(([id, val]) => [id, val]));

// id -> {url, code}; a code we never observed must not be treated as alive.
const ALIVE = /^(200|201|202|203|204|301|302|303|307|308|401|403|405|406|429)$/;
const bRows = readTSV(bPath).map(([code, id, url]) => ({ code, id, url }));
const promote = new Map();
const deadDomain = new Map();
for (const r of bRows) {
  if (ALIVE.test(r.code)) promote.set(r.id, r.url);
  else deadDomain.set(r.id, { url: r.url, code: r.code });
}

const raw = JSON.parse(fs.readFileSync(DATA, 'utf8'));
const arr = Array.isArray(raw) ? raw : raw.churches;

let cleared = 0, promoted = 0, deadCleared = 0, unseen = 0;
const log = [];

for (const c of arr) {
  const w = typeof c.website === 'string' ? c.website.trim() : '';
  if (!w) continue;
  if (/^https?:\/\//i.test(w)) continue; // already a real URL

  if (clearIds.has(c.id)) {
    log.push(`CLEAR-placeholder\t${c.id}\t${JSON.stringify(w)}`);
    c.website = '';
    c.needs_review = true;
    cleared++;
  } else if (promote.has(c.id)) {
    const url = promote.get(c.id);
    log.push(`PROMOTE\t${c.id}\t${w} -> ${url}`);
    c.website = url;
    promoted++;
  } else if (deadDomain.has(c.id)) {
    const { url, code } = deadDomain.get(c.id);
    log.push(`CLEAR-dead\t${c.id}\t${w} (fetch ${code} for ${url})`);
    c.website = '';
    c._dead_site = true;
    c.needs_review = true;
    c.url_research_status = `unreachable ${code} on ${TODAY}`;
    deadCleared++;
  } else {
    // Not covered by either sweep file — leave it alone rather than guess.
    log.push(`SKIP-unverified\t${c.id}\t${JSON.stringify(w)}`);
    unseen++;
  }
}

console.log(`promoted to https:// (verified live): ${promoted}`);
console.log(`cleared placeholder prose:            ${cleared}`);
console.log(`cleared unreachable bare domain:      ${deadCleared}`);
console.log(`left alone (no fetch evidence):       ${unseen}`);
console.log(`total records touched:                ${promoted + cleared + deadCleared}`);

fs.writeFileSync('/tmp/website-fix-ledger.tsv', log.join('\n') + '\n');
console.log('ledger -> /tmp/website-fix-ledger.tsv');

if (APPLY) {
  // Match the repo convention exactly (merge-pastor-enrichments.js:142) or the
  // diff becomes the whole 76 MB file instead of the records actually touched.
  fs.writeFileSync(DATA, JSON.stringify(raw, null, 2) + '\n');
  console.log('APPLIED to', DATA);
} else {
  console.log('(dry run — pass --apply to write)');
}
