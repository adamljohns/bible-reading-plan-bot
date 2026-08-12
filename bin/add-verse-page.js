#!/usr/bin/env node
/* add-verse-page.js — clone a new curated verse landing page from the template.
 *
 * The 22 original pages are pure template: the only per-page content is the
 * identity fields (canonical, og:url, titles, h1, refInput) plus the SSR block
 * and description metas, and those last two are rebuilt by generate-verse-pages.js.
 * So a new page is: clone template → swap identity fields → run the SSG baker.
 *
 * Usage: node bin/add-verse-page.js "Philippians 4:13" "Psalm 23:1-6" ...
 * Then:  node bin/generate-verse-pages.js
 *
 * Also rebuilds the <li> listing in docs/verse/index.html from the directory
 * (alphabetical by filename, ref text read from each page's refInput).
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const VERSE_DIR = path.join(ROOT, 'docs', 'verse');
const TEMPLATE = path.join(VERSE_DIR, 'luke-14-33.html');
const TPL_REF = 'Luke 14:33';
const TPL_SLUG = 'luke-14-33.html';

const slugFor = (ref) => ref.toLowerCase().replace(/[–—]/g, '-').replace(/[ :]/g, '-') + '.html';

function addPage(ref) {
  const slug = slugFor(ref);
  const fp = path.join(VERSE_DIR, slug);
  if (fs.existsSync(fp)) return { ref, slug, status: 'exists' };
  let html = fs.readFileSync(TEMPLATE, 'utf8');
  html = html.split(TPL_SLUG).join(slug);
  html = html.split(TPL_REF).join(ref);
  fs.writeFileSync(fp, html);
  return { ref, slug, status: 'created' };
}

function rebuildIndex() {
  const idxPath = path.join(VERSE_DIR, 'index.html');
  let idx = fs.readFileSync(idxPath, 'utf8');
  const files = fs.readdirSync(VERSE_DIR).filter((f) => f.endsWith('.html') && f !== 'index.html').sort();
  const items = files.map((f) => {
    const m = fs.readFileSync(path.join(VERSE_DIR, f), 'utf8').match(/id="refInput"\s+value="([^"]+)"/);
    return `    <li><a href="${f}">${m ? m[1] : f}</a></li>`;
  });
  // Replace the contiguous <li><a href="*.html"> block with the regenerated list.
  const re = /(?:^[ \t]*<li><a href="[^"]+\.html">[^<]+<\/a><\/li>\n)+/m;
  if (!re.test(idx)) throw new Error('index.html: listing block not found');
  idx = idx.replace(re, items.join('\n') + '\n');
  fs.writeFileSync(idxPath, idx);
  return files.length;
}

const refs = process.argv.slice(2);
if (!refs.length) { console.log('Usage: node bin/add-verse-page.js "Book C:V[-V2]" ...'); process.exit(1); }
refs.forEach((r) => { const res = addPage(r); console.log(`${res.status}: ${res.slug} (${res.ref})`); });
const n = rebuildIndex();
console.log(`index.html rebuilt: ${n} verse pages listed.`);
console.log('Baking SSR blocks + metas...');
execFileSync('node', [path.join(__dirname, 'generate-verse-pages.js')], { stdio: 'inherit' });
