#!/usr/bin/env node
// Audit the church-directory HTML subpages for the things that quietly rot:
//   1. broken internal links   (href -> a local .html that doesn't exist)
//   2. broken local assets      (src/href -> a local file that doesn't exist)
//   3. stale church-count numbers (hardcoded totals that no longer match churches.json)
//   4. stale "last updated" dates (reported for eyeball, not failed)
// Read-only. Exit 1 if any hard issue (broken link/asset or stale count) is found.
//
// Usage: node scripts/audit-directory-pages.js
const fs = require('fs');
const path = require('path');

const DOCS = path.join(__dirname, '..', 'docs');
const churches = JSON.parse(fs.readFileSync(path.join(DOCS, 'data/churches.json'), 'utf8'));
const TOTAL = churches.churches.length;
const TOTAL_STR = TOTAL.toLocaleString(); // "28,515"

// The pages that make up the directory experience.
const PAGES = fs.readdirSync(DOCS).filter(f =>
  /^(churches(-[a-z]+)?|directory-[a-z]+|near-me|grind-report|sitemap)\.html$/.test(f));

// Known-stale totals from earlier milestones — flag if they appear as a live count.
const STALE_COUNTS = ['13,895', '13895', '17,777', '17777', '27,777', '27777', '28,514', '28,516'];
// Count-shaped numbers 10,000–99,999 (to catch a hardcoded "X churches" that drifted).
const COUNTISH = /\b([12][0-9],[0-9]{3})\b/g;

let hardIssues = 0;
const report = [];

for (const page of PAGES) {
  const html = fs.readFileSync(path.join(DOCS, page), 'utf8');
  const issues = [];

  // 1+2. Local links & assets. Pull href/src values, skip external/anchor/template.
  const refs = [...html.matchAll(/(?:href|src)\s*=\s*["']([^"'>]+)["']/gi)].map(m => m[1]);
  for (const ref of refs) {
    if (/^(https?:|mailto:|tel:|#|data:|javascript:|\/\/)/i.test(ref)) continue;
    if (ref.includes('${') || ref.includes('{{')) continue; // client-rendered template
    const clean = ref.split('#')[0].split('?')[0].trim();
    if (!clean) continue;
    const target = clean.startsWith('/') ? path.join(DOCS, clean) : path.join(DOCS, clean);
    if (!fs.existsSync(target)) {
      // '/churches/<id>.html' templated links resolve at runtime; only flag concrete ones
      if (/\/churches\/[a-z0-9-]+\.html$/i.test(clean) && !clean.includes('$')) {
        issues.push(`broken link/asset → ${clean}`);
        hardIssues++;
      } else if (!clean.includes('/churches/')) {
        issues.push(`broken link/asset → ${clean}`);
        hardIssues++;
      }
    }
  }

  // 3. Stale counts — only when the number sits near the word "church" (a real total claim).
  for (const stale of STALE_COUNTS) {
    const idx = html.indexOf(stale);
    if (idx >= 0) {
      const window = html.slice(Math.max(0, idx - 60), idx + 80).toLowerCase();
      if (window.includes('church') || window.includes('director') || window.includes('total')) {
        issues.push(`stale count "${stale}" near a church/total claim (current is ${TOTAL_STR})`);
        hardIssues++;
      }
    }
  }
  // A count-ish number IMMEDIATELY followed by "churches" that isn't the current
  // total — a hardcoded directory total that drifted. Skip legit non-total metrics
  // (geocoded subset, network cross-listings, per-church page counts) and the
  // roadmap page's historical/aspirational milestones.
  if (page !== 'directory-roadmap.html') {
    for (const m of html.matchAll(COUNTISH)) {
      const n = m[1], idx = m.index;
      if (n === TOTAL_STR) continue;
      const after = html.slice(idx + n.length, idx + n.length + 55).toLowerCase().replace(/<[^>]+>/g, ' ').trim();
      if (/^churches\b/.test(after) && !/geocod|plotted|mapped|cross-list|network|pages\b/.test(after)) {
        issues.push(`possible stale total "${n} churches" (current is ${TOTAL_STR}) — verify`);
        hardIssues++;
      }
    }
  }

  // 4. Dates (report only).
  const dates = [...new Set([...html.matchAll(/\b(20[0-9]{2}-[01][0-9]-[0-3][0-9])\b/g)].map(m => m[1]))];
  const staleDate = dates.filter(d => d < '2026-01-01');

  if (issues.length || staleDate.length) {
    report.push({ page, issues, dates: dates.slice(-3), staleDate });
  }
}

console.log(`Directory subpage audit — ${PAGES.length} pages, current total ${TOTAL_STR} churches\n`);
if (!report.length) {
  console.log('  ✓ all pages clean: no broken links/assets, no stale counts.');
} else {
  for (const r of report) {
    console.log(`  ${r.issues.length ? '✗' : '⚠'} ${r.page}`);
    r.issues.forEach(i => console.log(`      ${i}`));
    if (r.staleDate.length) console.log(`      ⚠ pre-2026 date(s): ${r.staleDate.join(', ')} (verify not a stale "last updated")`);
  }
}
console.log(`\n${hardIssues} hard issue(s). Pages audited: ${PAGES.join(', ')}`);
process.exit(hardIssues ? 1 : 0);
