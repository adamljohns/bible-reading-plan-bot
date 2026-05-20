#!/usr/bin/env node
// Stage 1 of SBC bulk-load: pull all 35 SBC church sitemaps in one pass.
// Sitemaps are explicitly meant for crawlers; we don't need a delay between
// sitemap-XML fetches (only between individual page-HTML fetches).
//
// Output: /tmp/sbc-all-urls.json — array of { url, slug, lastmod } objects
// for every church URL the SBC publishes in its sitemap index.
//
// Re-run periodically (weekly is plenty) — the SBC adds/retires churches
// continuously but the sitemap index reflects whatever is current.

const fs = require('fs');
const https = require('https');
const path = require('path');

const SITEMAP_BASE = 'https://churches.sbc.net';
const NUM_SHARDS = 35; // observed from sitemaps.xml
const OUT = '/tmp/sbc-all-urls.json';

function fetchText(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'MOOP-Church-Directory-Scraper/1.0 (contact: bowandarrowstudiollc@gmail.com)' } }, res => {
      if (res.statusCode !== 200) {
        return reject(new Error(`${url}: HTTP ${res.statusCode}`));
      }
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => resolve(body));
    }).on('error', reject);
  });
}

function parseUrls(xml) {
  const urls = [];
  // Match each <url>…</url> block
  const blockRx = /<url>([\s\S]*?)<\/url>/g;
  let m;
  while ((m = blockRx.exec(xml)) !== null) {
    const block = m[1];
    const locMatch = block.match(/<loc>([^<]+)<\/loc>/);
    const lastmodMatch = block.match(/<lastmod>([^<]+)<\/lastmod>/);
    if (locMatch) {
      const url = locMatch[1].trim();
      // Only keep /church/<slug>/ URLs (skip the sitemap's own self-refs etc.)
      const slugMatch = url.match(/\/church\/([^/]+)\/?$/);
      if (slugMatch) {
        urls.push({ url, slug: slugMatch[1], lastmod: lastmodMatch ? lastmodMatch[1].trim() : null });
      }
    }
  }
  return urls;
}

async function main() {
  console.log(`Fetching ${NUM_SHARDS} SBC church sitemaps…`);
  const all = [];
  for (let i = 1; i <= NUM_SHARDS; i++) {
    const url = `${SITEMAP_BASE}/church-sitemap${i}.xml`;
    try {
      const xml = await fetchText(url);
      const urls = parseUrls(xml);
      console.log(`  shard ${i}/${NUM_SHARDS}: ${urls.length} church URLs`);
      all.push(...urls);
    } catch (e) {
      console.error(`  shard ${i}/${NUM_SHARDS} FAILED: ${e.message}`);
    }
    // Short pause (1s) between sitemap fetches — they're cheap but be polite
    await new Promise(r => setTimeout(r, 1000));
  }
  console.log(`\nTotal church URLs collected: ${all.length}`);
  fs.writeFileSync(OUT, JSON.stringify({ fetched_at: new Date().toISOString(), count: all.length, urls: all }, null, 2));
  console.log(`Wrote ${OUT}`);
}

main().catch(e => { console.error(e); process.exit(1); });
