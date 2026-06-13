#!/usr/bin/env node
/* generate-lbcf-pages.js — static pre-render for the 1689 LBCF on usmcmin.org
 *
 * WHY: the chapter pages were empty JS shells — crawlers, link-preview bots, and
 * no-JS readers saw a blank <div>. This bakes the full chapter (with the SAME
 * auto-links the browser renderer produces) into each shell as static HTML, plus
 * an embedded copy of the chapter JSON the renderer enhances from (no refetch,
 * no flash, offline-proof). The browser renderer clears the static fallback and
 * rebuilds identically, so interactivity (permalink/copy/print) is unchanged.
 *
 * Single source of truth: we load docs/assets/js/lbcf-render.js in a vm sandbox
 * and call window.LBCF.autoLink / linkScripture — the exact functions the page
 * uses — so static links can never drift from the live ones.
 *
 * Outputs (idempotent — safe to re-run):
 *   - docs/lbcf/chapter-NN.html   prerendered body + embedded JSON + real <title>/meta
 *   - docs/lbcf.html              prerendered chapter grid + embedded index.json
 *   - docs/lbcf-full.html         whole confession on one page (if front-matter.json present:
 *                                 preface + all chapters + signatories)
 *   - docs/lbcf/preface.html      standalone modernized preface (if front-matter.json present)
 *
 * Run: node bin/generate-lbcf-pages.js
 */
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const DOCS = path.join(ROOT, 'docs');
const LBCF_DATA = path.join(DOCS, 'assets', 'lbcf');
const RENDERER = path.join(DOCS, 'assets', 'js', 'lbcf-render.js');
const FRONT_MATTER = path.join(LBCF_DATA, 'front-matter.json');
const BUSTER = 'v=20260613';
const LASTMOD = '2026-06-13'; // sitemap <lastmod>; constant so re-runs don't churn

// ---- Load the live renderer's pure functions (one source of truth) ----------
function loadLBCF() {
  const src = fs.readFileSync(RENDERER, 'utf8');
  const sandbox = { window: {}, console };
  vm.createContext(sandbox);
  vm.runInContext(src, sandbox, { filename: 'lbcf-render.js' });
  if (!sandbox.window.LBCF || !sandbox.window.LBCF.autoLink) {
    throw new Error('Renderer did not export window.LBCF.autoLink — aborting.');
  }
  return sandbox.window.LBCF;
}
const LBCF = loadLBCF();

// ---- Small helpers ----------------------------------------------------------
const pad = (n) => String(n).padStart(2, '0');
const escText = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const escAttr = (s) => escText(s).replace(/"/g, '&quot;');
// Embed JSON safely inside <script type="application/json"> (block </script> + parser quirks)
const embedJson = (obj) =>
  JSON.stringify(obj).replace(/</g, '\\u003c').replace(/>/g, '\\u003e').replace(/&/g, '\\u0026');

function readJson(p) { return JSON.parse(fs.readFileSync(p, 'utf8')); }

// ---- Build the static body for one chapter (mirrors renderChapter) ----------
function chapterBodyHtml(chapter) {
  const n = chapter.number;
  let html = '';

  // Header
  html += '<div class="lbcf-chap-head">' +
    '<div class="lbcf-chap-num">Chapter ' + n + '</div>' +
    '<h1>' + escText(chapter.title) + '</h1>' +
    (chapter.subtitle ? '<p class="lbcf-chap-sub">' + escText(chapter.subtitle) + '</p>' : '') +
    '</div>';

  // Body — fresh dedupe Set per paragraph, exactly like the renderer
  html += '<div class="lbcf-body">';
  chapter.paragraphs.forEach((para, idx) => {
    const num = idx + 1;
    const linked = LBCF.autoLink(para.text, n, new Set());
    let proofs = '';
    if (para.prooftexts && para.prooftexts.length) {
      const refs = para.prooftexts.map((r) => LBCF.linkScripture(r)).join(' &middot; ');
      proofs = '<details class="lbcf-proofs"><summary>Proof-texts</summary><div>' + refs + '</div></details>';
    }
    html += '<section class="lbcf-para" id="p' + num + '">' +
      '<div class="lbcf-para-num">' + num +
      '<button class="lbcf-permalink" title="Copy link to this paragraph" aria-label="Copy permalink">¶</button></div>' +
      '<div class="lbcf-para-body"><p>' + linked + '</p>' + proofs + '</div>' +
      '</section>';
  });
  html += '</div>';

  // Prev / All / Next
  const prev = n > 1
    ? '<a class="lbcf-prev" href="chapter-' + pad(n - 1) + '.html">← Chapter ' + (n - 1) + '</a>'
    : '<span></span>';
  const idx = '<a class="lbcf-idx" href="../lbcf.html">All Chapters</a>';
  const next = n < 32
    ? '<a class="lbcf-next" href="chapter-' + pad(n + 1) + '.html">Chapter ' + (n + 1) + ' →</a>'
    : '<span></span>';
  html += '<div class="lbcf-chap-nav">' + prev + idx + next + '</div>';

  // Lightweight no-JS footer (JS rebuilds the full interactive footer on load)
  html += '<footer class="lbcf-chap-footer">' +
    '<p class="lbcf-chap-disclaimer">Modernized in reverent contemporary English from the ' +
    '<a href="https://www.ccel.org/ccel/anonymous/bcf.html" target="_blank" rel="noopener">1677/1689 archaic original</a>' +
    ' — a public-domain text hosted by CCEL. Free to copy, quote, and share.</p>' +
    (chapter.version ? '<p class="lbcf-chap-version">Chapter version ' + escText(chapter.version) + ' · LBCF on usmcmin.org</p>' : '') +
    '</footer>';

  return html;
}

// ---- Rewrite one chapter shell ---------------------------------------------
function processChapterShell(chapter) {
  const n = chapter.number;
  const file = path.join(DOCS, 'lbcf', 'chapter-' + pad(n) + '.html');
  let html = fs.readFileSync(file, 'utf8');

  const body = chapterBodyHtml(chapter);
  const block =
    '<!-- LBCF-PRERENDER -->\n' +
    '        <div id="lbcf-chap-target">' + body + '</div>\n' +
    '        <script type="application/json" id="lbcf-chapter-data">' + embedJson(chapter) + '</script>\n' +
    '        <!-- /LBCF-PRERENDER -->';

  if (/<!-- LBCF-PRERENDER -->[\s\S]*?<!-- \/LBCF-PRERENDER -->/.test(html)) {
    html = html.replace(/<!-- LBCF-PRERENDER -->[\s\S]*?<!-- \/LBCF-PRERENDER -->/, () => block);
  } else {
    html = html.replace('<div id="lbcf-chap-target"></div>', () => block);
  }

  // Real <title> + meta for SEO / link previews
  const titleStr = 'LBCF Chapter ' + n + ': ' + chapter.title + ' — U.S.M.C. Ministries';
  const ogTitle = 'LBCF Chapter ' + n + ': ' + chapter.title;
  const desc = (chapter.subtitle || ('Chapter ' + n + ' of the 1689 London Baptist Confession of Faith.')) +
    ' — 1689 London Baptist Confession of Faith, in modern English with linked Scripture proofs.';
  html = html.replace(/<title>[\s\S]*?<\/title>/, () => '<title>' + escText(titleStr) + '</title>');
  html = html.replace(/<meta name="description" content="[\s\S]*?">/, () => '<meta name="description" content="' + escAttr(desc) + '">');
  html = html.replace(/<meta property="og:title" content="[\s\S]*?">/, () => '<meta property="og:title" content="' + escAttr(ogTitle) + '">');
  html = html.replace(/<meta property="og:description" content="[\s\S]*?">/, () => '<meta property="og:description" content="' + escAttr(chapter.subtitle || ogTitle) + '">');

  // Keep the renderer cache-buster current
  html = html.replace(/lbcf-render\.js\?v=[0-9a-z]+/g, 'lbcf-render.js?' + BUSTER);

  fs.writeFileSync(file, html);
  return body.length;
}

// ---- Rewrite the hub grid (mirrors renderIndex) -----------------------------
function processHub(meta) {
  const file = path.join(DOCS, 'lbcf.html');
  let html = fs.readFileSync(file, 'utf8');

  let grid = '<div class="lbcf-grid">';
  meta.chapters.forEach((c) => {
    const status = c.status === 'placeholder'
      ? '<span class="lbcf-card-status placeholder">Coming soon</span>'
      : c.version
        ? '<span class="lbcf-card-status">v' + escText(c.version) + '</span>'
        : c.status === 'draft' ? '<span class="lbcf-card-status">Draft</span>' : '';
    grid += '<a class="lbcf-card" href="lbcf/chapter-' + pad(c.number) + '.html">' +
      '<div class="lbcf-card-num">Chapter ' + c.number + '</div>' +
      '<h3>' + escText(c.title) + '</h3>' +
      '<p>' + escText(c.summary || '') + '</p>' + status + '</a>';
  });
  grid += '</div>';

  const block =
    '<!-- LBCF-PRERENDER -->\n' +
    '        <div id="lbcf-grid-target">' + grid + '</div>\n' +
    '        <script type="application/json" id="lbcf-index-data">' + embedJson(meta) + '</script>\n' +
    '        <!-- /LBCF-PRERENDER -->';

  if (/<!-- LBCF-PRERENDER -->[\s\S]*?<!-- \/LBCF-PRERENDER -->/.test(html)) {
    html = html.replace(/<!-- LBCF-PRERENDER -->[\s\S]*?<!-- \/LBCF-PRERENDER -->/, () => block);
  } else {
    html = html.replace('<div id="lbcf-grid-target"></div>', () => block);
  }
  html = html.replace(/lbcf-render\.js\?v=[0-9a-z]+/g, 'lbcf-render.js?' + BUSTER);

  fs.writeFileSync(file, html);
}

// ---- Whole-confession page + standalone preface (need front-matter.json) ----
function navHtml(active) {
  const item = (href, icon, label, isActive) =>
    '<a href="' + href + '"' + (isActive ? ' class="active"' : '') + '><img src="assets/icons/' + icon +
    '" class="site-icon" alt="' + label + '" width="16" height="16"> ' + label + '</a>';
  return '<nav>' +
    item('index.html', 'shield-home-48.png', 'U.S.M.C. Ministries Home', false) +
    item('watchman.html', 'shield-bible.png', 'Watchman Bible Plan', false) +
    item('bible.html', 'shield-bible-cross-48.png', 'Bible Translation Engine', false) +
    item('lexicon.html', 'shield-alpha-omega-48.png', 'Lexicon', false) +
    item('cross-references.html', 'shield-infinity-rope-48.png', 'Cross-References', false) +
    item('dictionary/index.html', 'shield-book-greek-48.png', 'Dictionary', false) +
    item('lbcf.html', 'shield-cross.png', '1689 LBCF', active === 'lbcf') +
    item('catechism.html', 'shield-cross.png', 'Baptist Catechism', false) +
    item('institutes.html', 'shield-cross.png', 'Institutes', false) +
    item('blog.html', 'shield-scroll-quill-48.png', 'Blog', false) +
    item('connect.html', 'shield-handshake.png', 'Connect', false) +
    '</nav>';
}

// Page <head> shared by full page + preface (root-relative asset paths)
function pageHead(title, desc, canonical) {
  return '<!DOCTYPE html>\n<html lang="en">\n<head>\n' +
    '    <meta charset="UTF-8">\n' +
    '    <link rel="canonical" href="' + canonical + '">\n' +
    '    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">\n' +
    '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n' +
    '    <title>' + escText(title) + '</title>\n' +
    '    <meta name="description" content="' + escAttr(desc) + '">\n' +
    '    <meta property="og:title" content="' + escAttr(title) + '">\n' +
    '    <meta property="og:description" content="' + escAttr(desc) + '">\n' +
    '    <meta property="og:type" content="article">\n' +
    '    <meta property="og:url" content="' + canonical + '">\n' +
    '    <meta property="og:image" content="https://usmcmin.org/assets/og/og-bible.png">\n' +
    '    <meta name="twitter:card" content="summary_large_image">\n' +
    '    <link rel="preconnect" href="https://fonts.googleapis.com">\n' +
    '    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">\n' +
    '    <link rel="stylesheet" href="assets/css/lbcf.css">\n' +
    '    <link rel="manifest" href="/manifest.json">\n' +
    '    <link rel="stylesheet" href="/assets/css/light-icons.css">\n' +
    '    <link rel="stylesheet" href="/assets/css/print.css" media="print">\n' +
    THEME_STYLE +
    '</head>\n';
}

const THEME_STYLE =
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
  '        .bte-theme-toggle { position: fixed; top: 12px; right: 12px; z-index: 9999; display: flex; align-items: center; background: rgba(30,30,30,0.9); border: 1px solid #333; border-radius: 20px; padding: 4px 8px; cursor: pointer; gap: 5px; }\n' +
  '        .toggle-icon { font-size: 0.85rem; line-height:1; }\n' +
  '        .toggle-track { width: 30px; height: 16px; background: #444; border-radius: 8px; position: relative; }\n' +
  '        .toggle-knob { width: 12px; height: 12px; background: var(--gold); border-radius: 50%; position: absolute; top: 2px; left: 2px; transition: left 0.25s; }\n' +
  '        body.light-mode .toggle-knob { left: 16px; }\n' +
  '        body.light-mode { background:#F4ECD8; color:#1a1a1a; }\n' +
  '        body.light-mode nav { background:rgba(244,236,216,0.97) !important; border-bottom-color:#d4d0c8; }\n' +
  '        body.light-mode nav a { color:#555 !important; }\n' +
  '        body.light-mode nav a:hover, body.light-mode nav a.active { color:#8a6a1a !important; }\n' +
  '        body.light-mode .bte-theme-toggle { background:rgba(220,215,205,0.95); border-color:#bbb; }\n' +
  '        /* full-edition + preface specifics */\n' +
  '        .lbcf-toc { background:var(--bg-card); border:1px solid var(--border); border-radius:12px; padding:20px 24px; margin:24px 0; }\n' +
  '        .lbcf-toc h2 { color:var(--gold); font-size:1.05rem; margin-bottom:12px; }\n' +
  '        .lbcf-toc ol { columns:2; column-gap:32px; list-style-position:inside; margin:0; padding:0; }\n' +
  '        @media (max-width:640px){ .lbcf-toc ol { columns:1; } }\n' +
  '        .lbcf-toc li { font-size:0.9rem; margin-bottom:6px; break-inside:avoid; }\n' +
  '        .lbcf-toc a { color:var(--gray); text-decoration:none; }\n' +
  '        .lbcf-toc a:hover { color:var(--gold); }\n' +
  '        .lbcf-full-chap { margin:0 auto 8px; }\n' +
  '        .lbcf-front { max-width:760px; margin:0 auto; }\n' +
  '        .lbcf-front h2 { font-family:"Playfair Display",serif; color:var(--gold-light); font-size:clamp(1.4rem,3vw,2rem); text-align:center; margin:36px 0 6px; }\n' +
  '        .lbcf-front .lbcf-front-sub { text-align:center; color:var(--gold); font-size:0.95rem; margin-bottom:22px; }\n' +
  '        .lbcf-front p { color:var(--white); font-size:1.02rem; line-height:1.85; margin-bottom:16px; }\n' +
  '        body.light-mode .lbcf-front p { color:#1a1a1a; }\n' +
  '        body.light-mode .lbcf-front h2 { color:#5a4710; }\n' +
  '        .lbcf-sigs { max-width:760px; margin:36px auto 0; }\n' +
  '        .lbcf-sigs h2 { font-family:"Playfair Display",serif; color:var(--gold-light); text-align:center; font-size:1.5rem; margin-bottom:8px; }\n' +
  '        body.light-mode .lbcf-sigs h2 { color:#5a4710; }\n' +
  '        .lbcf-sigs .lbcf-sigs-intro { text-align:center; color:var(--gray); font-size:0.92rem; max-width:640px; margin:0 auto 20px; line-height:1.7; }\n' +
  '        .lbcf-sigs-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:12px; }\n' +
  '        .lbcf-sig { background:var(--bg-card); border:1px solid var(--border); border-radius:8px; padding:12px 14px; }\n' +
  '        body.light-mode .lbcf-sig { background:#fffaf0; border-color:#d4c8a8; }\n' +
  '        .lbcf-sig .lbcf-sig-name { color:var(--gold-light); font-weight:600; font-size:0.95rem; }\n' +
  '        body.light-mode .lbcf-sig .lbcf-sig-name { color:#5a4710; }\n' +
  '        .lbcf-sig .lbcf-sig-meta { color:var(--gray); font-size:0.82rem; line-height:1.5; margin-top:3px; }\n' +
  '        .lbcf-readthru { display:flex; flex-wrap:wrap; gap:10px; justify-content:center; margin:18px 0 8px; }\n' +
  '        .lbcf-readthru a { display:inline-flex; align-items:center; gap:6px; padding:8px 16px; background:rgba(212,175,55,0.08); border:1px solid rgba(212,175,55,0.3); border-radius:18px; color:var(--gold); font-size:0.85rem; font-weight:500; text-decoration:none; transition:all 0.18s; }\n' +
  '        .lbcf-readthru a:hover { background:rgba(212,175,55,0.18); color:var(--gold-light); border-color:rgba(212,175,55,0.5); }\n' +
  '        body.light-mode .lbcf-readthru a { background:rgba(138,106,26,0.08); border-color:rgba(138,106,26,0.4); color:#8a6a1a; }\n' +
  '        @media print { .lbcf-full-chap, .lbcf-sigs { break-before:page; } .lbcf-toc, .lbcf-readthru { display:none !important; } }\n' +
  '    </style>\n';

const THEME_TOGGLE_MARKUP =
  '    <div class="bte-theme-toggle" onclick="bteToggleTheme()" title="Toggle dark/light mode">\n' +
  '        <span class="toggle-icon moon-icon">🌙</span>\n' +
  '        <div class="toggle-track"><div class="toggle-knob"></div></div>\n' +
  '        <span class="toggle-icon sun-icon">☀️</span>\n' +
  '    </div>\n';

const THEME_SCRIPT =
  '    <script>\n' +
  '        function bteToggleTheme() {\n' +
  "            document.body.classList.toggle('light-mode');\n" +
  "            try { localStorage.setItem('bte-theme', document.body.classList.contains('light-mode') ? 'light' : 'dark'); } catch(e){}\n" +
  '        }\n' +
  "        try { var t = localStorage.getItem('bte-theme'); if (t === null && (t = localStorage.getItem('moop-theme')) !== null) localStorage.setItem('bte-theme', t); if (t === 'light') document.body.classList.add('light-mode'); } catch(e){}\n" +
  '    </script>\n';

// One chapter rendered for the full page (root-relative xref/idx links differ)
function fullChapterSection(chapter) {
  const n = chapter.number;
  let html = '<section class="lbcf-full-chap" id="ch-' + n + '">';
  html += '<div class="lbcf-chap-head">' +
    '<div class="lbcf-chap-num">Chapter ' + n + '</div>' +
    '<h1>' + escText(chapter.title) + '</h1>' +
    (chapter.subtitle ? '<p class="lbcf-chap-sub">' + escText(chapter.subtitle) + '</p>' : '') +
    '</div>';
  html += '<div class="lbcf-body">';
  chapter.paragraphs.forEach((para, idx) => {
    const num = idx + 1;
    const linked = LBCF.autoLink(para.text, n, new Set());
    let proofs = '';
    if (para.prooftexts && para.prooftexts.length) {
      const refs = para.prooftexts.map((r) => LBCF.linkScripture(r)).join(' &middot; ');
      proofs = '<details class="lbcf-proofs"><summary>Proof-texts</summary><div>' + refs + '</div></details>';
    }
    html += '<section class="lbcf-para" id="ch' + n + 'p' + num + '">' +
      '<div class="lbcf-para-num">' + num + '</div>' +
      '<div class="lbcf-para-body"><p>' + linked + '</p>' + proofs + '</div></section>';
  });
  html += '</div></section>';
  return html;
}

function buildFullPage(meta, chapters, front) {
  const canonical = 'https://usmcmin.org/lbcf-full.html';
  let h = pageHead(
    'The 1689 Baptist Confession — Complete Text — U.S.M.C. Ministries',
    'The complete Second London Baptist Confession of Faith (1689) on one page — all 32 chapters in modern English with linked Scripture proofs, the preface, and the signatories. Printer-friendly.',
    canonical
  );
  h += '<body>\n' + THEME_TOGGLE_MARKUP + navHtml('lbcf') + '\n    <div class="container">\n';
  // Hero
  h += '<header class="lbcf-hero"><img src="assets/icons/shield-cross.png" alt="LBCF crest">' +
    '<div class="subtitle">Second London Baptist Confession of Faith</div>' +
    '<h1>The Complete Confession</h1>' +
    '<p class="desc">All thirty-two chapters of the 1689 confession on a single page — modernized from the 1677/1689 public-domain original, with Scripture proof-texts and theological terms linked throughout. Use your browser’s print command for a clean printed copy.</p></header>';
  h += '<div class="lbcf-readthru"><a href="lbcf.html">← Chapter index</a>' +
    (front && front.preface ? '<a href="lbcf/preface.html">Read the preface</a>' : '') + '</div>';

  // TOC
  h += '<nav class="lbcf-toc" aria-label="Chapters"><h2>Contents</h2><ol>';
  if (front && front.preface) h += '<li><a href="#preface">The Preface — To the Judicious and Impartial Reader</a></li>';
  chapters.forEach((c) => {
    h += '<li><a href="#ch-' + c.number + '">' + escText(c.title) + '</a></li>';
  });
  if (front && front.signatories && front.signatories.signatories && front.signatories.signatories.length) {
    h += '<li><a href="#signatories">The Signatories</a></li>';
  }
  h += '</ol></nav>';

  // Preface
  if (front && front.preface && front.preface.modernized) {
    h += '<section class="lbcf-front" id="preface"><h2>The Preface</h2>' +
      '<p class="lbcf-front-sub">To the Judicious and Impartial Reader</p>';
    front.preface.modernized.split(/\n\s*\n/).forEach((para) => {
      const t = para.trim();
      if (t) h += '<p>' + LBCF.linkScripture(escText(t)) + '</p>';
    });
    h += '</section>';
  }

  // All chapters
  chapters.forEach((c) => { h += fullChapterSection(c); });

  // Signatories
  if (front && front.signatories && front.signatories.signatories && front.signatories.signatories.length) {
    h += '<section class="lbcf-sigs" id="signatories"><h2>The Signatories</h2>';
    if (front.signatories.intro) h += '<p class="lbcf-sigs-intro">' + escText(front.signatories.intro) + '</p>';
    h += '<div class="lbcf-sigs-grid">';
    front.signatories.signatories.forEach((s) => {
      const meta2 = [s.church, s.location].filter(Boolean).map(escText).join(' · ');
      h += '<div class="lbcf-sig"><div class="lbcf-sig-name">' + escText(s.name) + '</div>' +
        (meta2 ? '<div class="lbcf-sig-meta">' + meta2 + '</div>' : '') + '</div>';
    });
    h += '</div>';
    if (front.signatories.closing) {
      h += '<p class="lbcf-sigs-intro" style="margin-top:18px;font-style:italic;">' + escText(front.signatories.closing) + '</p>';
    }
    h += '</section>';
  }

  // Disclaimer footer
  h += '<footer class="lbcf-chap-footer" style="max-width:760px;margin:40px auto 0;">' +
    '<p class="lbcf-chap-disclaimer">Modernized in reverent contemporary English from the ' +
    '<a href="https://www.ccel.org/ccel/anonymous/bcf.html" target="_blank" rel="noopener">1677/1689 archaic original</a>' +
    ' — a public-domain text. Free to copy, quote, and share.</p></footer>';

  h += '\n    </div>\n' + THEME_SCRIPT + '</body>\n</html>\n';
  return h;
}

function buildPrefacePage(front) {
  const canonical = 'https://usmcmin.org/lbcf/preface.html';
  // preface lives under /lbcf/ so asset paths need ../ — reuse head but fix relative refs
  let head = pageHead(
    'The Preface to the 1689 Baptist Confession — U.S.M.C. Ministries',
    'The preface to the Second London Baptist Confession of Faith (1689) — "To the Judicious and Impartial Reader" — in modern English.',
    canonical
  ).replace(/href="assets\//g, 'href="../assets/');
  let h = head + '<body>\n' + THEME_TOGGLE_MARKUP.replace(/g/, 'g') +
    navHtml('lbcf').replace(/href="(?!http)([^"]+)"/g, 'href="../$1"').replace(/src="assets\//g, 'src="../assets/') +
    '\n    <div class="container"><div class="lbcf-front" id="preface">' +
    '<div class="lbcf-chap-head" style="border:none;"><div class="lbcf-chap-num">The 1689 Confession</div>' +
    '<h1>The Preface</h1><p class="lbcf-chap-sub">To the Judicious and Impartial Reader</p></div>';
  front.preface.modernized.split(/\n\s*\n/).forEach((para) => {
    const t = para.trim();
    if (t) h += '<p>' + LBCF.linkScripture(escText(t)) + '</p>';
  });
  h += '<footer class="lbcf-chap-footer" style="margin-top:30px;"><p class="lbcf-chap-disclaimer">The preface to the 1677/1689 confession, modernized in reverent contemporary English from the public-domain original. Free to copy, quote, and share.</p>' +
    (front.preface.version ? '<p class="lbcf-chap-version">Preface version ' + escText(front.preface.version) + ' · LBCF on usmcmin.org</p>' : '') + '</footer>';
  h += '<div class="lbcf-readthru" style="margin-top:18px;"><a href="../lbcf.html">← Chapter index</a><a href="../lbcf-full.html">Read the whole confession</a></div>';
  h += '</div></div>\n' + THEME_SCRIPT + '</body>\n</html>\n';
  return h;
}

// ---- Sitemap: emit sitemap-lbcf.xml + register it in the sitemap index ------
function writeSitemap(chapters, front) {
  const url = (loc, pri) =>
    '  <url>\n    <loc>https://usmcmin.org/' + loc + '</loc>\n' +
    '    <lastmod>' + LASTMOD + '</lastmod>\n    <changefreq>monthly</changefreq>\n' +
    '    <priority>' + pri + '</priority>\n  </url>\n';

  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
  xml += url('lbcf.html', '0.9');
  xml += url('lbcf-full.html', '0.8');
  if (front && front.preface) xml += url('lbcf/preface.html', '0.6');
  chapters.forEach((c) => { xml += url('lbcf/chapter-' + pad(c.number) + '.html', '0.7'); });
  xml += '</urlset>\n';
  fs.writeFileSync(path.join(DOCS, 'sitemap-lbcf.xml'), xml);

  // Register in the sitemap index (idempotent)
  const idxPath = path.join(DOCS, 'sitemap.xml');
  let idx = fs.readFileSync(idxPath, 'utf8');
  if (!idx.includes('sitemap-lbcf.xml')) {
    const entry = '  <sitemap>\n    <loc>https://usmcmin.org/sitemap-lbcf.xml</loc>\n    <lastmod>' + LASTMOD + '</lastmod>\n  </sitemap>\n';
    idx = idx.replace('</sitemapindex>', entry + '</sitemapindex>');
    fs.writeFileSync(idxPath, idx);
    console.log('Registered sitemap-lbcf.xml in sitemap.xml index.');
  } else {
    idx = idx.replace(/(<loc>https:\/\/usmcmin\.org\/sitemap-lbcf\.xml<\/loc>\s*<lastmod>)[0-9-]+(<\/lastmod>)/, '$1' + LASTMOD + '$2');
    fs.writeFileSync(idxPath, idx);
  }
  console.log('Wrote docs/sitemap-lbcf.xml (' + (chapters.length + (front && front.preface ? 3 : 2)) + ' urls).');
}

// ---- Main -------------------------------------------------------------------
function main() {
  const meta = readJson(path.join(LBCF_DATA, 'index.json'));
  const chapters = meta.chapters
    .filter((c) => c.status !== 'placeholder')
    .map((c) => readJson(path.join(LBCF_DATA, 'chapter-' + pad(c.number) + '.json')))
    .sort((a, b) => a.number - b.number);

  let totalBytes = 0;
  chapters.forEach((ch) => { totalBytes += processChapterShell(ch); });
  processHub(meta);
  console.log('Pre-rendered ' + chapters.length + ' chapter shells + hub grid (' + Math.round(totalBytes / 1024) + ' KB of static body HTML).');

  let front = null;
  if (fs.existsSync(FRONT_MATTER)) {
    front = readJson(FRONT_MATTER);
    if (front.preface && front.preface.modernized) {
      fs.writeFileSync(path.join(DOCS, 'lbcf', 'preface.html'), buildPrefacePage(front));
      console.log('Wrote docs/lbcf/preface.html');
    }
  } else {
    console.log('No front-matter.json yet — full page generated without preface/signatories.');
  }
  fs.writeFileSync(path.join(DOCS, 'lbcf-full.html'), buildFullPage(meta, chapters, front));
  console.log('Wrote docs/lbcf-full.html (' + chapters.length + ' chapters' +
    (front && front.preface ? ' + preface' : '') +
    (front && front.signatories ? ' + ' + (front.signatories.signatories || []).length + ' signatories' : '') + ').');

  writeSitemap(chapters, front);
}

main();
