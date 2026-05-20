#!/usr/bin/env node
// Stage 2 of SBC bulk-load: dedup 34,501 SBC sitemap URLs against our
// existing 2,114 SBC records + the broader 13,895 directory.
//
// Strategy (in order of confidence):
//   1. Exact slug match (SBC slug === existing slug)
//   2. Normalized-name match where existing record looks like an SBC
//      congregation (already tagged or strongly suggestive name)
//
// Output:
//   /tmp/sbc-todo.json  — URLs we still need to scrape (net-new)
//   /tmp/sbc-existing-matches.json — URLs that already have records;
//      potentially eligible for enrichment (mark as SBC if not already)
//
// Run after sbc-fetch-sitemap.js.

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs/data/churches.json');
const ALL_URLS = '/tmp/sbc-all-urls.json';
const OUT_TODO = '/tmp/sbc-todo.json';
const OUT_MATCHES = '/tmp/sbc-existing-matches.json';

function normalizeForMatch(s) {
  // Strip common church-name boilerplate so "First Baptist Church of Dallas"
  // and "first-baptist-dallas-tx" can collide. This is intentionally lossy.
  return String(s || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, ' ')
    .replace(/\b(the|a|an|of|at|on|in|for|to|and|&)\b/g, ' ')
    .replace(/\b(church|baptist|first|community|fellowship|chapel|missionary|memorial|grace|new|life|hope|cornerstone|trinity|calvary)\b/g, ' ')
    .replace(/\b[a-z]{1,2}\b/g, ' ') // strip 1-2 letter tokens (state codes, etc.)
    .replace(/\s+/g, ' ')
    .trim();
}

function slugToName(slug) {
  return slug.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
const sitemapData = JSON.parse(fs.readFileSync(ALL_URLS, 'utf8'));
const sitemapUrls = sitemapData.urls;

console.log(`Loaded ${d.churches.length} existing churches.`);
console.log(`Loaded ${sitemapUrls.length} SBC sitemap URLs.`);

// Build lookup indexes from existing records
const slugIndex = new Map();
const nameIndex = new Map();
for (const c of d.churches) {
  const slug = c.slug || c.id;
  if (slug) slugIndex.set(slug.toLowerCase(), c);
  const norm = normalizeForMatch(c.name);
  if (norm && norm.length > 4) {
    if (!nameIndex.has(norm)) nameIndex.set(norm, []);
    nameIndex.get(norm).push(c);
  }
}
console.log(`Built indexes: ${slugIndex.size} slugs, ${nameIndex.size} normalized names.`);

const todo = [];
const slugMatches = [];
const nameMatches = [];

for (const item of sitemapUrls) {
  const sbcSlug = item.slug.toLowerCase();
  if (slugIndex.has(sbcSlug)) {
    slugMatches.push({ url: item.url, slug: item.slug, existing: slugIndex.get(sbcSlug).id || slugIndex.get(sbcSlug).slug });
    continue;
  }
  // Try normalized-name match (lossy — only acts as a hint)
  const inferredName = slugToName(item.slug);
  const norm = normalizeForMatch(inferredName);
  if (norm && norm.length > 4 && nameIndex.has(norm)) {
    const candidates = nameIndex.get(norm);
    // Conservative: only count as match if candidate is already SBC-tagged
    // (so we don't accidentally mark unrelated denomination as SBC).
    const sbcCandidate = candidates.find(c => /SBC|Southern Baptist/i.test(c.denomination_family || c.denomination || ''));
    if (sbcCandidate) {
      nameMatches.push({ url: item.url, slug: item.slug, inferred_name: inferredName, existing: sbcCandidate.id || sbcCandidate.slug });
      continue;
    }
  }
  // Net-new
  todo.push({ url: item.url, slug: item.slug, lastmod: item.lastmod });
}

console.log(`\nResults:`);
console.log(`  Slug exact matches:  ${slugMatches.length}`);
console.log(`  Name fuzzy matches:  ${nameMatches.length}`);
console.log(`  Net-new (need scrape): ${todo.length}`);

fs.writeFileSync(OUT_TODO, JSON.stringify({ generated_at: new Date().toISOString(), count: todo.length, urls: todo }, null, 2));
fs.writeFileSync(OUT_MATCHES, JSON.stringify({
  generated_at: new Date().toISOString(),
  slug_matches: slugMatches,
  name_fuzzy_matches: nameMatches
}, null, 2));
console.log(`\nWrote ${OUT_TODO}`);
console.log(`Wrote ${OUT_MATCHES}`);
