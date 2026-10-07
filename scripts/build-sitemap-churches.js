#!/usr/bin/env node
// Regenerate docs/sitemap-churches.xml from docs/data/churches.json.
// Emits one <url> per church (priority 0.5, monthly changefreq).

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const OUT = path.join(__dirname, '..', 'docs', 'sitemap-churches.xml');

const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
const today = new Date().toISOString().slice(0, 10);

// A <loc> must be a valid, XML-escaped URI. 120 ids carry raw spaces or
// non-ASCII ("...-south carolina", mojibake "√≥"); written raw they made the
// sitemap invalid for every crawler. Percent-encode the id as one path segment.
// check-consistency.js decodes <loc>s before comparing, so the gate still
// matches ids exactly. Change both together or the grind's gate fails hard.
const xmlEscape = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const locFor = (id) => xmlEscape(`https://usmcmin.org/churches/${encodeURIComponent(id)}.html`);

const urls = [];
for (const c of d.churches) {
  if (!c || typeof c !== 'object' || !c.id) continue;
  urls.push(`  <url>
    <loc>${locFor(c.id)}</loc>
    <lastmod>${today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>`);
}

const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.join('\n')}
</urlset>
`;

fs.writeFileSync(OUT, xml);
console.log(`Wrote ${OUT}`);
console.log(`  ${urls.length} church URLs`);
