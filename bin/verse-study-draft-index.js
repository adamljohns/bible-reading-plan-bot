#!/usr/bin/env node
/* verse-study-draft-index.js — a private contents page for the draft studies.
 *
 * Adam reviews on a phone, so the drafts need one URL that lists them all with
 * an honest state next to each: what is written, what is still scaffolding.
 * noindex, nofollow, disallowed in robots.txt, linked from nothing.
 *
 * Usage: node bin/verse-study-draft-index.js
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DOCS = path.join(ROOT, 'docs');
const DRAFTS = path.join(DOCS, 'drafts', 'verse');

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function packsFor() {
  const packs = JSON.parse(fs.readFileSync(path.join(DOCS, 'data', 'memory-packs.json'), 'utf8')).packs || [];
  const map = new Map();
  packs.forEach((p) => p.verses.forEach((v) => {
    if (!map.has(v.ref)) map.set(v.ref, []);
    if (!map.get(v.ref).includes(p.name)) map.get(v.ref).push(p.name);
  }));
  return map;
}

function main() {
  if (!fs.existsSync(DRAFTS)) { console.error('no drafts directory'); process.exit(1); }
  const packMap = packsFor();
  const rows = fs.readdirSync(DRAFTS).filter((f) => f.endsWith('.html') && f !== 'index.html').map((f) => {
    const html = fs.readFileSync(path.join(DRAFTS, f), 'utf8');
    const ref = (html.match(/<meta name="verse-ref" content="([^"]*)"/) || [])[1] || f;
    const snippet = (html.match(/<meta name="verse-snippet" content="([^"]*)"/) || [])[1] || '';
    const todos = (html.match(/vs-todo/g) || []).length;
    const words = html.replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/g, '').replace(/<!--[\s\S]*?-->/g, '')
      .replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().split(' ').length;
    return { f, ref, snippet, todos, words, packs: packMap.get(ref) || [] };
  });
  // Written first — those are the ones worth a review pass.
  rows.sort((a, b) => (a.todos ? 1 : 0) - (b.todos ? 1 : 0) || a.ref.localeCompare(b.ref));
  const written = rows.filter((r) => !r.todos).length;

  const items = rows.map((r) => {
    const state = r.todos
      ? `<span class="st scaffold">scaffold · ${r.todos} slots to write</span>`
      : `<span class="st written">written · ${r.words} words</span>`;
    return `    <li>
      <a href="/drafts/verse/${esc(r.f)}">${esc(r.ref)}</a> ${state}
      ${r.packs.length ? `<span class="pk">${esc(r.packs.join(' · '))}</span>` : ''}
      ${r.snippet ? `<br><span class="sub">“${esc(r.snippet)}”</span>` : ''}
    </li>`;
  }).join('\n');

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>Verse Study Drafts (private) — U.S.M.C. Ministries</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:-apple-system,'Inter',sans-serif;background:#000;color:#fff;line-height:1.6;padding:22px 16px 60px}
  .wrap{max-width:760px;margin:0 auto}
  h1{font-family:Georgia,serif;color:#D4AF37;font-size:1.7rem;margin-bottom:.3rem}
  .lede{color:#888;font-size:.94rem;margin-bottom:.5rem}
  .banner{border:1px solid #b4553a;background:rgba(180,85,58,.12);color:#e39a80;border-radius:8px;padding:.6rem .9rem;font-size:.84rem;margin:1rem 0 1.4rem}
  ol{list-style:none;counter-reset:n}
  li{counter-increment:n;border-bottom:1px solid #222;padding:.7rem 0 .7rem 2.1rem;position:relative}
  li::before{content:counter(n);position:absolute;left:0;top:.75rem;color:#555;font-size:.78rem}
  a{color:#D4AF37;text-decoration:none;font-weight:600}
  a:hover{text-decoration:underline}
  .st{font-size:.7rem;letter-spacing:.06em;text-transform:uppercase;padding:.1rem .5rem;border-radius:20px;margin-left:.35rem;white-space:nowrap}
  .written{border:1px solid rgba(120,180,120,.5);color:#8fc98f}
  .scaffold{border:1px solid rgba(180,85,58,.5);color:#d99a83}
  .pk{color:#666;font-size:.72rem;margin-left:.35rem}
  .sub{color:#8a8a8a;font-size:.86rem}
</style>
</head>
<body>
<div class="wrap">
  <h1>Verse Study Drafts</h1>
  <p class="lede">The ${rows.length} verses in the memorize app. ${written} written, ${rows.length - written} still scaffolding.</p>
  <div class="banner">Private working page. Not indexed, not linked from the site, disallowed in robots.txt. Nothing here has been reviewed — a "scaffold" page has real Scripture, word study and confession text, but its prose slots are still empty and marked in red.</div>
  <ol>
${items}
  </ol>
</div>
</body>
</html>
`;
  fs.writeFileSync(path.join(DOCS, 'drafts', 'verse', 'index.html'), html);
  console.log(`Draft index: ${rows.length} studies (${written} written, ${rows.length - written} scaffolded) -> /drafts/verse/index.html`);
}

if (require.main === module) main();
