#!/usr/bin/env node
// scripts/integrate-network-urls.js
//
// Pulls per-church deep-link URLs out of cached scrape data and writes them
// onto churches.json as `cross_listed_urls.{network}: <url>` so the
// /directory-networks.html badge renderer can deep-link instead of falling
// back to the network's directory home.
//
// Only integrates networks whose cached URL patterns are verified to deep-link
// publicly (no login walls, no broken hash anchors, no routes-to-landing).
// As of 2026-05-27, that is:
//
//   ✅ acts29     — pattern /church/{slug}/ — verified by WebFetch
//   ✅ founders   — pattern /church/{slug}/ — populated by scrape-founders-directory.js
//
// Skipped networks (cached URLs exist but don't deep-link publicly):
//
//   ❌ 9marks     — /edit/?id=N requires login
//   ❌ tgc-cn     — /church/{slug}/ now routes to directory landing
//   ❌ sgc        — hash anchors don't scroll/highlight
//   ❌ pillar     — hash anchors don't deep-link
//   ❌ trinity    — single-page list, no per-church anchor
//
// Re-running is idempotent (only writes if value differs from current).
//
// Usage:
//   node scripts/integrate-network-urls.js                 # all enabled networks
//   node scripts/integrate-network-urls.js --network acts29  # one network only

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const PHASE2 = path.join(__dirname, '..', 'docs', 'data', 'research-leads', 'phase2-network-leads.json');
const FOUNDERS_SCRAPE = '/tmp/founders-scrape.jsonl';

// Networks safe to integrate. Add a key here once you've VERIFIED that
// network's cached URL pattern actually deep-links publicly.
const ENABLED = new Set(['acts29', 'founders']);

function parseArgs() {
  const out = { networks: null };
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--network') out.networks = [a[++i]];
  }
  return out;
}

function normalizeName(s) {
  return String(s || '')
    .toLowerCase()
    .replace(/&amp;/g, '&')
    .replace(/[‘’′]/g, "'")
    .replace(/[^a-z0-9]+/g, ' ')
    .trim();
}

function extractState(addr) {
  if (!addr) return '';
  const m = String(addr).match(/,\s*([A-Z]{2})\b/);
  return m ? m[1] : '';
}

// Build a name+state index of all MOOP churches once, for fast match
function buildIndex(d) {
  const idx = new Map();
  for (const c of d.churches) {
    const state = extractState(c.address);
    const k = normalizeName(c.name) + '|' + state;
    if (!idx.has(k)) idx.set(k, []);
    idx.get(k).push(c);
  }
  return idx;
}

function pickMatch(candidates, network) {
  if (!candidates || candidates.length === 0) return null;
  if (candidates.length === 1) return candidates[0];
  // Multiple churches share name+state — prefer one already cross-listed in this network
  const tagged = candidates.filter(c => Array.isArray(c.cross_listed_in) && c.cross_listed_in.includes(network));
  if (tagged.length === 1) return tagged[0];
  if (tagged.length > 1) return tagged[0]; // accept first; logged as ambiguous
  return candidates[0];
}

function loadSourceEntries(network) {
  if (network === 'founders') {
    // Founders entries come from the live scraper's output
    if (!fs.existsSync(FOUNDERS_SCRAPE)) return [];
    const lines = fs.readFileSync(FOUNDERS_SCRAPE, 'utf8').split('\n').filter(Boolean);
    return lines.map(l => {
      try {
        const r = JSON.parse(l);
        if (!r || !r.network_url) return null;
        return {
          source_network: 'founders',
          name: r.name,
          city: r.city,
          state: r.state,
          network_url: r.network_url,
        };
      } catch (e) { return null; }
    }).filter(Boolean);
  }
  // All others come from phase2-network-leads.json
  if (!fs.existsSync(PHASE2)) return [];
  const all = JSON.parse(fs.readFileSync(PHASE2, 'utf8'));
  return all.filter(e => e.source_network === network && e.network_url);
}

function integrateNetwork(d, idx, network) {
  const entries = loadSourceEntries(network);
  if (entries.length === 0) {
    console.log(`  [${network}] no source entries found — skipping`);
    return { network, attempted: 0, matched: 0, written: 0, missed: 0 };
  }
  let matched = 0, written = 0, missed = 0, ambiguous = 0;
  for (const e of entries) {
    const state = (e.state || '').toUpperCase();
    const k = normalizeName(e.name) + '|' + state;
    const candidates = idx.get(k);
    if (!candidates) { missed++; continue; }
    const target = pickMatch(candidates, network);
    if (candidates.length > 1) ambiguous++;
    matched++;
    target.cross_listed_urls = target.cross_listed_urls || {};
    if (target.cross_listed_urls[network] !== e.network_url) {
      target.cross_listed_urls[network] = e.network_url;
      written++;
    }
  }
  console.log(`  [${network}] ${entries.length} cached · ${matched} matched · ${written} URLs written (${ambiguous} name+state collisions; ${missed} unmatched)`);
  return { network, attempted: entries.length, matched, written, missed };
}

function main() {
  const args = parseArgs();
  const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
  const idx = buildIndex(d);
  const targets = args.networks || [...ENABLED];
  console.log(`Integrating per-church URLs for: ${targets.join(', ')}`);
  console.log(`Built name+state index of ${idx.size} unique keys across ${d.churches.length} MOOP churches.\n`);

  const summary = [];
  for (const n of targets) {
    if (!ENABLED.has(n)) {
      console.log(`  [${n}] not in ENABLED set — skipping (would need verified deep-link URLs first)`);
      continue;
    }
    summary.push(integrateNetwork(d, idx, n));
  }

  const totalWritten = summary.reduce((s, r) => s + r.written, 0);
  fs.writeFileSync(CHURCHES, JSON.stringify(d, null, 2));
  console.log(`\nWrote ${CHURCHES} — ${totalWritten} per-church URLs added across ${summary.length} network(s).`);

  // Final coverage check
  let totalWithUrls = 0;
  const byNet = {};
  for (const c of d.churches) {
    if (c.cross_listed_urls && typeof c.cross_listed_urls === 'object') {
      let hasOne = false;
      for (const [k, v] of Object.entries(c.cross_listed_urls)) {
        if (v) { byNet[k] = (byNet[k]||0)+1; hasOne = true; }
      }
      if (hasOne) totalWithUrls++;
    }
  }
  console.log(`\nCurrent cross_listed_urls coverage:`);
  console.log(`  ${totalWithUrls} churches now have at least one deep-link URL`);
  for (const [n, c] of Object.entries(byNet)) console.log(`    ${n}: ${c}`);
}

main();
