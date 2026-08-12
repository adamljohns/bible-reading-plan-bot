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

// Canonical book order for the index (same ids as generate-verse-pages.js).
const BOOK_IDS = {
  'genesis':1,'exodus':2,'leviticus':3,'numbers':4,'deuteronomy':5,'joshua':6,'judges':7,'ruth':8,
  '1 samuel':9,'2 samuel':10,'1 kings':11,'2 kings':12,'1 chronicles':13,'2 chronicles':14,
  'ezra':15,'nehemiah':16,'esther':17,'job':18,'psalms':19,'psalm':19,'proverbs':20,'ecclesiastes':21,
  'song of solomon':22,'song of songs':22,'isaiah':23,'jeremiah':24,'lamentations':25,'ezekiel':26,
  'daniel':27,'hosea':28,'joel':29,'amos':30,'obadiah':31,'jonah':32,'micah':33,'nahum':34,
  'habakkuk':35,'zephaniah':36,'haggai':37,'zechariah':38,'malachi':39,
  'matthew':40,'mark':41,'luke':42,'john':43,'acts':44,'romans':45,'1 corinthians':46,'2 corinthians':47,
  'galatians':48,'ephesians':49,'philippians':50,'colossians':51,'1 thessalonians':52,'2 thessalonians':53,
  '1 timothy':54,'2 timothy':55,'titus':56,'philemon':57,'hebrews':58,'james':59,'1 peter':60,'2 peter':61,
  '1 john':62,'2 john':63,'3 john':64,'jude':65,'revelation':66,
};
function sortKey(ref) {
  const m = ref.match(/^(.+?)\s+(\d+):(\d+)/);
  if (!m) return [99, 0, 0];
  return [BOOK_IDS[m[1].trim().toLowerCase()] || 99, parseInt(m[2], 10), parseInt(m[3], 10)];
}

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
  const files = fs.readdirSync(VERSE_DIR).filter((f) => f.endsWith('.html') && f !== 'index.html');
  const entries = files.map((f) => {
    const html = fs.readFileSync(path.join(VERSE_DIR, f), 'utf8');
    const rm = html.match(/id="refInput"\s+value="([^"]+)"/);
    const ref = rm ? rm[1] : f;
    // Verse text lives in the baked meta description: `REF — “SNIPPET” Interlinear…`.
    const sm = html.match(/name="description" content="[^"]*?— “([^”]+)”/);
    return { f, ref, snippet: sm ? sm[1] : '' };
  });
  entries.sort((a, b) => {
    const ka = sortKey(a.ref), kb = sortKey(b.ref);
    return ka[0] - kb[0] || ka[1] - kb[1] || ka[2] - kb[2];
  });
  const items = entries.map((e) => {
    const sub = e.snippet ? `<br><span class="inst-sub">“${e.snippet}”</span>` : '';
    return `    <li><a href="${e.f}">${e.ref}</a>${sub}</li>`;
  });
  // Replace the contiguous <li><a href="*.html"> block with the regenerated list.
  const re = /(?:^[ \t]*<li><a href="[^"]+\.html">[^<]+<\/a>(?:<br><span class="inst-sub">[^<]*<\/span>)?<\/li>\n)+/m;
  if (!re.test(idx)) throw new Error('index.html: listing block not found');
  idx = idx.replace(re, items.join('\n') + '\n');
  fs.writeFileSync(idxPath, idx);
  return entries;
}

// Emit the verse→study map: docs/verse/studies.json plus the baked VERSE_STUDIES
// object in bible.html (between VERSE-STUDIES-MAP markers) that powers the
// "Go deeper" pill on covered verses. Range refs expand to one key per verse.
function emitStudiesMap(entries) {
  const map = {};
  entries.forEach((e) => {
    const m = e.ref.match(/^(.+?)\s+(\d+):(\d+)(?:[-–](\d+))?$/);
    if (!m) return;
    const b = BOOK_IDS[m[1].trim().toLowerCase()];
    if (!b) return;
    const v2 = m[4] ? parseInt(m[4], 10) : parseInt(m[3], 10);
    for (let v = parseInt(m[3], 10); v <= v2; v++) map[`${b}:${m[2]}:${v}`] = e.f;
  });
  fs.writeFileSync(path.join(VERSE_DIR, 'studies.json'), JSON.stringify(map, null, 1));
  const biblePath = path.join(ROOT, 'docs', 'bible.html');
  let bh = fs.readFileSync(biblePath, 'utf8');
  const re = /(\/\/ VERSE-STUDIES-MAP[^\n]*\n)[\s\S]*?(\n[ \t]*\/\/ \/VERSE-STUDIES-MAP)/;
  if (re.test(bh)) {
    bh = bh.replace(re, (_, a, z) => `${a}        var VERSE_STUDIES = ${JSON.stringify(map)};${z}`);
    fs.writeFileSync(biblePath, bh);
    console.log(`bible.html VERSE_STUDIES: ${Object.keys(map).length} verse keys baked.`);
  } else {
    console.log('bible.html: VERSE-STUDIES-MAP markers not found — map not baked.');
  }
}

const refs = process.argv.slice(2);
refs.forEach((r) => { const res = addPage(r); console.log(`${res.status}: ${res.slug} (${res.ref})`); });
if (refs.length) {
  console.log('Baking SSR blocks + metas...');
  execFileSync('node', [path.join(__dirname, 'generate-verse-pages.js')], { stdio: 'inherit' });
}
// Index rebuild runs after the bake so snippets read the fresh meta descriptions.
const entries = rebuildIndex();
console.log(`index.html rebuilt: ${entries.length} verse pages listed.`);
emitStudiesMap(entries);
