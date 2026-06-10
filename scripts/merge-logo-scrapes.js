#!/usr/bin/env node
//
// merge-logo-scrapes.js — fold scrape-church-logos.js results into churches.json,
// AND clean up cross-contaminated logos/heroes (images served from a different
// church's domain).
//
// Behaviors:
//   1. result.logo_url present  -> set image_thumb = logo_url, image_thumb_source='header-logo'
//   2. result.logo_rejected present and the church's CURRENT image_thumb is from
//      the rejected (wrong) domain -> clear image_thumb (it was contamination)
//   3. Independent hero contamination sweep: if image_url's root domain differs
//      from the website's root domain and is not a known CDN, clear image_url.
//
// Usage:
//   node merge-logo-scrapes.js [/tmp/logo-scrapes.jsonl]
//

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const JSONL = process.argv[2] || '/tmp/logo-scrapes.jsonl';

// Asset CDNs + website-builder hosts that legitimately serve a church's OWN
// logo. A logo on one of these found inside the church's own header is the
// church's logo by definition; only a logo on a different ORGANIZATION's
// primary domain is treated as cross-contamination. Keep this list broad —
// the cost of a false "contamination" clear (deleting a real logo) is higher
// than the cost of keeping an occasional mismatch for human review.
const CDN_OK = /squarespace-cdn|squarespace\.com|googleusercontent|ggpht|cloudinary|thechurchco|wixstatic|wix\.com|parastorage|wp\.com|gstatic|amazonaws|cloudfront|imgix|nucleus-cdn|cdn-website|showit\.co|snappages\.site|sg-host\.com|subsplash|churchcenter|getnetset|clover\.com|faithlife|ekklesia360|cloudfront\.net|b-cdn\.net|becdn\.net|wsimg\.com|framerusercontent|wzukusers|storage\.googleapis|tildacdn|jwwb\.nl|webador|weebly|webflow|duda|site123|godaddy|jimdo|strikingly|cargocollective|netlify|vercel|pages\.dev|github\.io|hubspot|elementor|filesusr|media-amazon|fbcdn|cdninstagram|ytimg|vimeocdn|files\.|\bcdn\d*\./i;

function rootDomain(u) {
  try {
    const h = new URL(u).hostname.replace(/^www\./, '');
    return h.split('.').slice(-2).join('.');
  } catch (e) { return null; }
}

if (!fs.existsSync(JSONL)) { console.error('No JSONL at ' + JSONL); process.exit(1); }

const results = new Map();
for (const l of fs.readFileSync(JSONL, 'utf8').split('\n').filter(Boolean)) {
  try { const r = JSON.parse(l); if (r.id) results.set(r.id, r); } catch (e) {}
}
console.log('Loaded ' + results.size + ' logo results from ' + JSONL);

// Byte-format-preserving read+write (ASCII-escaped, no trailing newline) — a plain
// JSON.stringify here used to re-encode every em-dash into a ~50k-line diff.
const { data, write: writeChurches } = require('./lib/format-preserving-write.js').makeWriter(CHURCHES);
let setLogo = 0, clearedLogo = 0, clearedHero = 0;

for (const c of data.churches) {
  const cid = c.id || c.slug;
  const r = results.get(cid);
  const webRoot = rootDomain(c.website);

  // 1 + 2: apply scraped logo result
  if (r) {
    if (r.logo_url) {
      c.image_thumb = r.logo_url;
      c.image_thumb_source = 'header-logo';
      setLogo++;
    } else if (r.logo_rejected && c.image_thumb) {
      // If the current logo is from the rejected (wrong) domain, clear it
      const curRoot = rootDomain(c.image_thumb);
      const rejRoot = rootDomain(r.logo_rejected);
      if (curRoot && curRoot === rejRoot) {
        c.image_thumb = null;
        c.image_thumb_source = 'cleared-contamination';
        clearedLogo++;
      }
    }
  }

  // 3: hero + leftover-logo contamination sweep — SCOPED to churches that were
  // actually scraped in this batch (present in the results map). We deliberately
  // do NOT sweep the whole directory: the CDN allowlist can never be exhaustive,
  // so a global sweep risks deleting real logos hosted on un-listed builder CDNs.
  // Limiting to scraped churches keeps the blast radius to what we are refining.
  if (r && c.image_url && webRoot) {
    const heroRoot = rootDomain(c.image_url);
    if (heroRoot && heroRoot !== webRoot && !CDN_OK.test(c.image_url)) {
      c.image_url = null;
      c.image_source = 'cleared-contamination';
      clearedHero++;
    }
  }
}

writeChurches(data);
console.log('Set ' + setLogo + ' header logos.');
console.log('Cleared ' + clearedLogo + ' contaminated logos, ' + clearedHero + ' contaminated heroes.');
