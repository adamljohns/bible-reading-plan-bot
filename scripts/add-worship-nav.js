#!/usr/bin/env node
/*
 * add-worship-nav.js — insert a "Worship" link into the Bible Tools nav on the
 * site's root hub pages, right after the Dictionary link. Idempotent: pages that
 * already have a Worship link are skipped. Only touches docs/*.html (root level);
 * the dictionary/ and churches/ subtrees are left to their own generators.
 *
 *   node scripts/add-worship-nav.js
 */
'use strict';
const fs = require('fs');
const path = require('path');

const DOCS = path.join(__dirname, '..', 'docs');
const LINK = '\n        <a href="worship.html"><img src="assets/icons/shield-quill-note-48.png" class="site-icon" alt="" width="16" height="16"> Worship</a>';
// Matches all four Dictionary-anchor variants in use, capturing the full anchor.
const DICT_RE = /(<a href="dictionary\/index\.html">.*?> Dictionary<\/a>)/;

let changed = 0, skipped = 0, nomatch = 0;
for (const f of fs.readdirSync(DOCS)) {
  if (!f.endsWith('.html')) continue;
  if (f === 'worship.html') continue;
  const p = path.join(DOCS, f);
  let html = fs.readFileSync(p, 'utf8');
  if (/> Worship<\/a>/.test(html)) { skipped++; continue; }
  if (!DICT_RE.test(html)) { nomatch++; continue; }
  html = html.replace(DICT_RE, '$1' + LINK);   // replaces first occurrence only
  fs.writeFileSync(p, html);
  changed++;
}
console.log(`Worship nav: ${changed} pages updated, ${skipped} already had it, ${nomatch} had no Dictionary nav (left untouched).`);
