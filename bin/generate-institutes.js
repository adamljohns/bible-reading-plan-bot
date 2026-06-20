#!/usr/bin/env node
/* generate-institutes.js — static chapter pages for Calvin's Institutes (Beveridge).
 *
 * Reads docs/assets/institutes/index.json (books + titles) + b{B}c{CC}.json
 * (parsed by parse-institutes.js). Emits docs/institutes/b{B}-c{CC}.html — 80
 * static, SEO-complete reading pages with auto-linked Scripture + dictionary
 * terms (reusing the LBCF link engine via vm), per-section proof-texts, the
 * "Sections" overview, and prev/next across book boundaries. Writes
 * sitemap-institutes.xml and flips index.json statuses placeholder -> beveridge.
 *
 * Run: node bin/generate-institutes.js   (re-run after re-parsing or modernizing)
 */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const DOCS = path.join(ROOT, 'docs');
const DATA = path.join(DOCS, 'assets', 'institutes');
const RENDERER = path.join(DOCS, 'assets', 'js', 'lbcf-render.js');
const LASTMOD = '2026-06-16';

function loadLBCF() {
  const src = fs.readFileSync(RENDERER, 'utf8');
  const sandbox = { window: {}, console };
  vm.createContext(sandbox);
  vm.runInContext(src, sandbox, { filename: 'lbcf-render.js' });
  return sandbox.window.LBCF;
}
const LBCF = loadLBCF();

const pad = (n) => String(n).padStart(2, '0');
const escText = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const escAttr = (s) => escText(s).replace(/"/g, '&quot;');
const chFile = (b, c) => 'b' + b + '-c' + pad(c) + '.html';

// Audio is served from Cloudflare R2 via the custom domain in the manifest's
// `base` (https://audio.usmcmin.org): R2 sends Content-Type: audio/mpeg + range
// support + free egress, and keeps the ~1GB+ of MP3s out of the Pages repo.
// (The GitHub Releases CDN served application/octet-stream with no CORS, which
// Safari refused to decode.) Falls back to the same-origin /assets path if `base`
// is absent. The manifest's `chapters` map is the source of truth for which
// chapters have audio.
const AUDIO_MANIFEST = (() => {
  try { return JSON.parse(fs.readFileSync(path.join(DATA, 'audio-manifest.json'), 'utf8')); }
  catch (e) { return { chapters: {} }; }
})();
function audioUrl(book, chapter) {
  const f = AUDIO_MANIFEST.chapters && AUDIO_MANIFEST.chapters['b' + book + 'c' + pad(chapter)];
  if (!f) return null;
  const base = (AUDIO_MANIFEST.base || '/assets/institutes/audio').replace(/\/$/, '');
  return base + '/' + f;
}

function nav() {
  const item = (href, icon, label, active) =>
    '<a href="' + href + '"' + (active ? ' class="active"' : '') + '><img src="../assets/icons/' + icon +
    '" class="site-icon" alt="' + label + '" width="16" height="16"> ' + label + '</a>';
  return '<nav>' +
    item('../index.html', 'shield-home-48.png', 'U.S.M.C. Ministries Home', false) +
    item('../watchman.html', 'shield-bible.png', 'Watchman Bible Plan', false) +
    item('../bible.html', 'shield-bible-cross-48.png', 'Bible Translation Engine', false) +
    item('../lexicon.html', 'shield-alpha-omega-48.png', 'Lexicon', false) +
    item('../dictionary/index.html', 'shield-book-greek-48.png', 'Dictionary', false) +
    item('../lbcf.html', 'shield-cross.png', '1689 LBCF', false) +
    item('../catechism.html', 'shield-cross.png', 'Baptist Catechism', false) +
    item('../institutes.html', 'shield-cross.png', 'Institutes', true) +
    item('../blog.html', 'shield-scroll-quill-48.png', 'Blog', false) +
    item('../connect.html', 'shield-handshake.png', 'Connect', false) +
    // theme toggle lives inside the nav (sticky, top-right via light-icons.css
    // .nav-theme-toggle margin-left:auto) — uniform with the rest of the site.
    '<div class="bte-theme-toggle nav-theme-toggle" onclick="instToggleTheme()" title="Toggle dark/light mode" role="button" tabindex="0" aria-label="Toggle dark/light mode"></div>' +
    '</nav>';
}

const STYLE =
  '    <style>\n' +
  '        * { margin:0; padding:0; box-sizing:border-box; }\n' +
  '        :root { --bg-dark:#000; --bg-card:#111; --gold:#D4AF37; --gold-light:#F4D470; --white:#FFF; --gray:#888; --border:#333; }\n' +
  "        body { font-family:'Inter',sans-serif; background:var(--bg-dark); color:var(--white); min-height:100vh; line-height:1.65; }\n" +
  '        nav { display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:4px 8px; padding:10px 16px; border-bottom:1px solid var(--border); position:sticky; top:0; background:rgba(0,0,0,0.95); backdrop-filter:blur(8px); z-index:100; }\n' +
  '        nav a { color:var(--gray); text-decoration:none; font-size:0.8rem; display:inline-flex; align-items:center; gap:3px; padding:3px 6px; border-radius:6px; transition:color 0.2s; }\n' +
  '        nav a:hover, nav a.active { color:var(--gold); }\n' +
  '        .site-icon { vertical-align:middle; opacity:0.85; margin-right:3px; }\n' +
  '        body.light-mode .site-icon { filter:brightness(0.55); }\n' +
  '        body.light-mode img[src*="/icons/shield-"]:not([src*="-bronze"]) { filter:brightness(.72) saturate(1.18) hue-rotate(-12deg); }\n' +
  '        .container { max-width:1100px; margin:0 auto; padding:24px 20px 60px; }\n' +
  '        body.light-mode { background:#F4ECD8; color:#1a1a1a; }\n' +
  '        body.light-mode nav { background:rgba(244,236,216,0.97) !important; border-bottom-color:#d4d0c8; }\n' +
  '        body.light-mode nav a { color:#555 !important; }\n' +
  '        body.light-mode nav a:hover, body.light-mode nav a.active { color:#8a6a1a !important; }\n' +
  '    </style>\n';

const SCRIPT =
  '    <script>\n' +
  '        function instToggleTheme(){document.body.classList.toggle("light-mode");try{localStorage.setItem("bte-theme",document.body.classList.contains("light-mode")?"light":"dark");}catch(e){}}\n' +
  '        try{var t=localStorage.getItem("bte-theme");if(t===null&&(t=localStorage.getItem("moop-theme"))!==null)localStorage.setItem("bte-theme",t);if(t==="light")document.body.classList.add("light-mode");}catch(e){}\n' +
  '        document.querySelectorAll(".inst-permalink").forEach(function(a){a.addEventListener("click",function(e){e.preventDefault();var u=location.origin+location.pathname+a.getAttribute("href");if(navigator.clipboard)navigator.clipboard.writeText(u).then(function(){a.classList.add("copied");var o=a.textContent;a.textContent="✓";setTimeout(function(){a.classList.remove("copied");a.textContent=o;},1200);});});});\n' +
  '    </script>\n' +
  '    <script>if("serviceWorker" in navigator){navigator.serviceWorker.register("/sw.js")}</script>\n';

function chapterPage(ch, prev, next) {
  const canonical = 'https://usmcmin.org/institutes/' + chFile(ch.book, ch.chapter);
  const romanBook = ['', 'I', 'II', 'III', 'IV'][ch.book];
  const _modSecs = (ch.modernized && ch.sectionsModern && ch.sectionsModern.length) ? ch.sectionsModern : ch.sections;
  const descSrc = ch.argument || (_modSecs[0] && _modSecs[0].paragraphs[0]) || ch.title;
  const desc = 'Calvin’s Institutes, Book ' + ch.book + ', Chapter ' + ch.chapter + ': ' + ch.title +
    ' — Henry Beveridge translation (public domain), with linked Scripture and theological terms. ' +
    String(descSrc).slice(0, 120);
  const isModern = !!(ch.modernized && ch.sectionsModern && ch.sectionsModern.length);
  const src = isModern ? ch.sectionsModern : ch.sections;
  const audUrl = audioUrl(ch.book, ch.chapter);

  let h = '<!DOCTYPE html>\n<html lang="en">\n<head>\n' +
    '    <meta charset="UTF-8">\n' +
    '    <link rel="canonical" href="' + canonical + '">\n' +
    '    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">\n' +
    '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n' +
    '    <title>Institutes ' + romanBook + '.' + ch.chapter + ': ' + escText(ch.title) + ' — Calvin (Beveridge)</title>\n' +
    '    <meta name="description" content="' + escAttr(desc) + '">\n' +
    '    <meta property="og:title" content="Calvin’s Institutes ' + romanBook + '.' + ch.chapter + ': ' + escAttr(ch.title) + '">\n' +
    '    <meta property="og:description" content="' + escAttr(ch.title) + ' — Book ' + ch.book + ', Chapter ' + ch.chapter + ' (Beveridge translation).">\n' +
    '    <meta property="og:type" content="article">\n    <meta property="og:url" content="' + canonical + '">\n' +
    '    <meta property="og:image" content="https://usmcmin.org/assets/og/og-bible.png">\n' +
    '    <meta name="twitter:card" content="summary_large_image">\n' +
    '    <link rel="preconnect" href="https://fonts.googleapis.com">\n' +
    '    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">\n' +
    '    <link rel="stylesheet" href="../assets/css/lbcf.css">\n' +
    '    <link rel="stylesheet" href="../assets/css/institutes.css">\n' +
    '    <link rel="manifest" href="/manifest.json">\n' +
    '    <link rel="stylesheet" href="/assets/css/light-icons.css">\n' +
    '    <link rel="stylesheet" href="/assets/css/print.css" media="print">\n' +
    STYLE + '</head>\n<body>\n' + nav() + '\n    <div class="container">\n';

  // book argument once (chapter 1 of each book)
  if (ch.bookArgument) {
    h += '<section class="inst-argument" style="max-width:760px;margin:18px auto 0;text-align:center;"><strong>Book ' +
      ch.book + ' — Argument.</strong> ' + escText(ch.bookArgument) + '</section>';
  }

  h += '<header class="inst-chap-head">' +
    '<div class="inst-chap-eyebrow">Book ' + ch.book + ' · Chapter ' + ch.chapter + ' · ' +
      (isModern ? 'USMC modern English' : 'Beveridge 1845') + '</div>' +
    '<h1>' + escText(ch.title) + '</h1>' +
    (ch.argument ? '<p class="inst-argument">' + escText(ch.argument) + '</p>' : '') +
    '</header>';

  if (audUrl) {
    h += '<div class="inst-audio"><div class="inst-audio-label">▶ Listen — read by Alan' +
      (isModern ? ' (modernized for 2026)' : '') + '</div>' +
      '<audio controls preload="none"><source src="' + audUrl + '" type="audio/mpeg">' +
      'Your browser cannot play this audio. <a href="' + audUrl + '" download>Download the MP3</a>.</audio></div>';
  }

  if (ch.sectionSummaries && ch.sectionSummaries.length) {
    h += '<details class="inst-summaries"><summary>Sections in this chapter</summary><ol>';
    ch.sectionSummaries.forEach((s) => { h += '<li>' + escText(s) + '</li>'; });
    h += '</ol></details>';
  }

  h += '<div class="inst-body">';
  src.forEach((sec) => {
    h += '<section class="inst-section" id="s' + sec.n + '">' +
      '<div class="inst-sec-num">' + sec.n + '<a class="inst-permalink" href="#s' + sec.n + '" title="Copy link to this section" aria-label="Copy permalink">¶</a></div>' +
      '<div class="inst-sec-body">';
    sec.paragraphs.forEach((p) => { h += '<p>' + LBCF.autoLink(p, 0, new Set()) + '</p>'; });
    if (sec.prooftexts && sec.prooftexts.length) {
      const refs = sec.prooftexts.map((r) => LBCF.linkScripture(r)).join(' &middot; ');
      h += '<details class="lbcf-proofs"><summary>Scripture cited</summary><div>' + refs + '</div></details>';
    }
    h += '</div></section>';
  });
  h += '</div>';

  if (ch.application) {
    h += '<aside class="inst-application"><div class="inst-application-head">A Word for 2026 · U.S.M.C. Ministries</div><p>' + escText(ch.application) + '</p></aside>';
  }

  const prevLink = prev ? '<a class="inst-prev" href="' + chFile(prev.book, prev.chapter) + '">← ' + (prev.book !== ch.book ? 'Book ' + prev.book + ' ' : '') + 'Ch. ' + prev.chapter + '</a>' : '<span></span>';
  const nextLink = next ? '<a class="inst-next" href="' + chFile(next.book, next.chapter) + '">' + (next.book !== ch.book ? 'Book ' + next.book + ' ' : '') + 'Ch. ' + next.chapter + ' →</a>' : '<span></span>';
  h += '<div class="inst-chap-nav">' + prevLink + '<a class="inst-idx" href="../institutes.html">All Books</a>' + nextLink + '</div>';

  h += '<footer class="inst-chap-foot"><p class="inst-chap-disclaimer">From the <strong>Henry Beveridge</strong> translation (1845) of Calvin’s <em>Institutes</em> (1559), a public-domain text from <a href="https://www.ccel.org/ccel/calvin/institutes.html" target="_blank" rel="noopener">CCEL</a>. Free to copy, quote, and share. Scripture and theological terms are linked for study.</p></footer>';

  h += '\n    </div>\n' + SCRIPT + '</body>\n</html>\n';
  return h;
}

function writeSitemap(order) {
  const url = (loc, pri) => '  <url>\n    <loc>https://usmcmin.org/' + loc + '</loc>\n    <lastmod>' + LASTMOD +
    '</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>' + pri + '</priority>\n  </url>\n';
  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
  xml += url('institutes.html', '0.9');
  order.forEach((c) => { xml += url('institutes/' + chFile(c.book, c.chapter), '0.6'); });
  xml += '</urlset>\n';
  fs.writeFileSync(path.join(DOCS, 'sitemap-institutes.xml'), xml);
  const idxPath = path.join(DOCS, 'sitemap.xml');
  let idx = fs.readFileSync(idxPath, 'utf8');
  if (!idx.includes('sitemap-institutes.xml')) {
    idx = idx.replace('</sitemapindex>', '  <sitemap>\n    <loc>https://usmcmin.org/sitemap-institutes.xml</loc>\n    <lastmod>' + LASTMOD + '</lastmod>\n  </sitemap>\n</sitemapindex>');
    fs.writeFileSync(idxPath, idx);
    console.log('Registered sitemap-institutes.xml');
  }
  console.log('Wrote sitemap-institutes.xml (' + (order.length + 1) + ' urls)');
}

function main() {
  const index = JSON.parse(fs.readFileSync(path.join(DATA, 'index.json'), 'utf8'));
  // ordered list of all chapters across books
  const order = [];
  index.books.forEach((b) => b.chapters.forEach((c) => order.push({ book: b.number, chapter: c.number })));
  // load chapter JSONs
  const chapters = order.map((o) => JSON.parse(fs.readFileSync(path.join(DATA, 'b' + o.book + 'c' + pad(o.chapter) + '.json'), 'utf8')));
  fs.mkdirSync(path.join(DOCS, 'institutes'), { recursive: true });
  let written = 0;
  chapters.forEach((ch, i) => {
    const html = chapterPage(ch, chapters[i - 1] || null, chapters[i + 1] || null);
    fs.writeFileSync(path.join(DOCS, 'institutes', chFile(ch.book, ch.chapter)), html);
    written++;
  });
  // flip index.json statuses to beveridge (so the hub links + chips update)
  let flipped = 0;
  index.books.forEach((b) => b.chapters.forEach((c) => { if (c.status === 'placeholder') { c.status = 'beveridge'; flipped++; } }));
  fs.writeFileSync(path.join(DATA, 'index.json'), JSON.stringify(index, null, 2));
  writeSitemap(order);
  console.log('Wrote ' + written + ' chapter pages; flipped ' + flipped + ' statuses placeholder->beveridge.');
}
main();
