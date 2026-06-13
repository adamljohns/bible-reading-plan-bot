#!/usr/bin/env node
/* generate-catechism.js — static page for the 1693 Baptist Catechism on usmcmin.org
 *
 * Single rich static page (/catechism.html): hero, about, section drill-down TOC +
 * jump-to-question box, all 114 Q&A grouped by editorial section, each answer and
 * proof-text auto-linked to the Bible engine + dictionary. Fully baked (SEO/no-JS
 * complete); inline JS only adds theme toggle, jump, and permalink copy.
 *
 * Reuses the LBCF renderer's link logic (loaded in a vm) so scripture/term links
 * are identical to the rest of the site — one source of truth.
 *
 * Data: docs/assets/catechism/catechism.json  (questions + sections + meta)
 * Run:  node bin/generate-catechism.js   (re-run after editing the JSON)
 */
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const DOCS = path.join(ROOT, 'docs');
const DATA = path.join(DOCS, 'assets', 'catechism', 'catechism.json');
const RENDERER = path.join(DOCS, 'assets', 'js', 'lbcf-render.js');
const LASTMOD = '2026-06-13';

// ---- reuse the LBCF link engine ----
function loadLBCF() {
  const src = fs.readFileSync(RENDERER, 'utf8');
  const sandbox = { window: {}, console };
  vm.createContext(sandbox);
  vm.runInContext(src, sandbox, { filename: 'lbcf-render.js' });
  if (!sandbox.window.LBCF || !sandbox.window.LBCF.autoLink) throw new Error('LBCF.autoLink missing');
  return sandbox.window.LBCF;
}
const LBCF = loadLBCF();

const escText = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const escAttr = (s) => escText(s).replace(/"/g, '&quot;');

function navHtml() {
  const item = (href, icon, label, active) =>
    '<a href="' + href + '"' + (active ? ' class="active"' : '') + '><img src="assets/icons/' + icon +
    '" class="site-icon" alt="' + label + '" width="16" height="16"> ' + label + '</a>';
  return '<nav>' +
    item('index.html', 'shield-home-48.png', 'U.S.M.C. Ministries Home', false) +
    item('watchman.html', 'shield-bible.png', 'Watchman Bible Plan', false) +
    item('bible.html', 'shield-bible-cross-48.png', 'Bible Translation Engine', false) +
    item('lexicon.html', 'shield-alpha-omega-48.png', 'Lexicon', false) +
    item('cross-references.html', 'shield-infinity-rope-48.png', 'Cross-References', false) +
    item('dictionary/index.html', 'shield-book-greek-48.png', 'Dictionary', false) +
    item('lbcf.html', 'shield-cross.png', '1689 LBCF', false) +
    item('catechism.html', 'shield-cross.png', 'Baptist Catechism', true) +
    item('institutes.html', 'shield-cross.png', 'Institutes', false) +
    item('blog.html', 'shield-scroll-quill-48.png', 'Blog', false) +
    item('connect.html', 'shield-handshake.png', 'Connect', false) +
    '</nav>';
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
  '        body.light-mode .lbcf-hero h1 { color:#5a4710; }\n' +
  '        body.light-mode .lbcf-hero .subtitle { color:#8a6a1a; }\n' +
  '        body.light-mode .lbcf-hero .desc { color:#555; }\n' +
  '    </style>\n';

const THEME_TOGGLE =
  '    <div class="bte-theme-toggle" onclick="catToggleTheme()" title="Toggle dark/light mode">\n' +
  '        <span class="toggle-icon moon-icon">🌙</span>\n' +
  '        <div class="toggle-track"><div class="toggle-knob"></div></div>\n' +
  '        <span class="toggle-icon sun-icon">☀️</span>\n' +
  '    </div>\n';

const INLINE_JS =
  '    <script>\n' +
  '        function catToggleTheme() {\n' +
  "            document.body.classList.toggle('light-mode');\n" +
  "            try { localStorage.setItem('bte-theme', document.body.classList.contains('light-mode') ? 'light' : 'dark'); } catch(e){}\n" +
  '        }\n' +
  "        try { var t = localStorage.getItem('bte-theme'); if (t === null && (t = localStorage.getItem('moop-theme')) !== null) localStorage.setItem('bte-theme', t); if (t === 'light') document.body.classList.add('light-mode'); } catch(e){}\n" +
  '        function catJump() {\n' +
  "            var v = parseInt((document.getElementById('cat-jump-input')||{}).value, 10);\n" +
  '            if (!v || v < 1 || v > 114) return;\n' +
  "            var el = document.getElementById('q' + v);\n" +
  "            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });\n" +
  '        }\n' +
  '        document.addEventListener("DOMContentLoaded", function () {\n' +
  "            var jb = document.getElementById('cat-jump-input');\n" +
  "            if (jb) jb.addEventListener('keydown', function(e){ if (e.key === 'Enter') catJump(); });\n" +
  "            document.querySelectorAll('.cat-permalink').forEach(function(a){\n" +
  "                a.addEventListener('click', function(e){\n" +
  '                    e.preventDefault();\n' +
  "                    var url = window.location.origin + window.location.pathname + a.getAttribute('href');\n" +
  '                    if (navigator.clipboard) navigator.clipboard.writeText(url).then(function(){\n' +
  "                        a.classList.add('copied'); var o = a.textContent; a.textContent = '✓';\n" +
  "                        setTimeout(function(){ a.classList.remove('copied'); a.textContent = o; }, 1200);\n" +
  '                    });\n' +
  '                });\n' +
  '            });\n' +
  '        });\n' +
  '    </script>\n';

function qaHtml(q) {
  const answer = LBCF.autoLink(q.answer, 0, new Set());
  let proofs = '';
  if (q.prooftexts && q.prooftexts.length) {
    const refs = q.prooftexts.map((r) => LBCF.linkScripture(r)).join(' &middot; ');
    proofs = '<details class="lbcf-proofs"><summary>Proof-texts</summary><div>' + refs + '</div></details>';
  }
  return '<div class="cat-q" id="q' + q.number + '">' +
    '<p class="cat-q-q"><span class="cat-q-num">Q' + q.number + '.</span> ' + escText(q.question) +
    ' <a class="cat-permalink" href="#q' + q.number + '" title="Copy link to this question" aria-label="Copy permalink">¶</a></p>' +
    '<p class="cat-q-a"><span class="cat-a-label">A.</span> ' + answer + '</p>' + proofs +
    '</div>';
}

function build(data) {
  const canonical = 'https://usmcmin.org/catechism.html';
  const desc = 'The Baptist Catechism of 1693 (Keach’s Catechism) — all 114 questions and answers in full, with Scripture proof-texts linked to the Bible engine and theological terms to the dictionary. The catechism companion to the 1689 confession.';
  const byNum = new Map(data.questions.map((q) => [q.number, q]));

  let h = '<!DOCTYPE html>\n<html lang="en">\n<head>\n' +
    '    <meta charset="UTF-8">\n' +
    '    <link rel="canonical" href="' + canonical + '">\n' +
    '    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">\n' +
    '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n' +
    '    <title>The Baptist Catechism (1693) — U.S.M.C. Ministries</title>\n' +
    '    <meta name="description" content="' + escAttr(desc) + '">\n' +
    '    <meta property="og:title" content="The Baptist Catechism (1693)">\n' +
    '    <meta property="og:description" content="' + escAttr(desc) + '">\n' +
    '    <meta property="og:type" content="article">\n' +
    '    <meta property="og:url" content="' + canonical + '">\n' +
    '    <meta property="og:image" content="https://usmcmin.org/assets/og/og-bible.png">\n' +
    '    <meta name="twitter:card" content="summary_large_image">\n' +
    '    <link rel="preconnect" href="https://fonts.googleapis.com">\n' +
    '    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">\n' +
    '    <link rel="stylesheet" href="assets/css/lbcf.css">\n' +
    '    <link rel="stylesheet" href="assets/css/catechism.css">\n' +
    '    <link rel="manifest" href="/manifest.json">\n' +
    '    <link rel="stylesheet" href="/assets/css/light-icons.css">\n' +
    '    <link rel="stylesheet" href="/assets/css/print.css" media="print">\n' +
    THEME_STYLE + '</head>\n<body>\n' + THEME_TOGGLE + navHtml() + '\n    <div class="container">\n';

  // Hero
  h += '<header class="lbcf-hero"><img src="assets/icons/shield-cross.png" alt="Catechism crest">' +
    '<div class="subtitle">Commonly called Keach’s Catechism</div>' +
    '<h1>The Baptist Catechism</h1>' +
    '<figure class="signatory-frontispiece"><img src="assets/lbcf/portraits/benjamin-keach.png" class="signatory-portrait" alt="Benjamin Keach (1640–1704), to whom the catechism is traditionally attributed">' +
    '<figcaption>Benjamin Keach &middot; 1640–1704 &middot; the catechism bears his name</figcaption></figure>' +
    '<p class="desc">Adopted by the Particular Baptist General Assembly in 1693 and modeled on the Westminster Shorter Catechism, the Baptist Catechism teaches the faith of the 1689 confession in 114 questions and answers — written to be learned by heart, in families and in the church.</p>' +
    '<p class="lbcf-stats"><span>' + data.questions.length + '</span> questions &middot; <span>' + (data.sections ? data.sections.length : 0) + '</span> sections &middot; with Scripture proofs</p></header>';

  h += '<div class="lbcf-readthru"><a href="lbcf.html">The 1689 Confession</a><a href="bible.html">Bible Translation Engine</a><a href="dictionary/index.html">Dictionary</a></div>';

  // About
  h += '<section class="lbcf-intro"><h2>About this catechism</h2>' +
    '<p>The Baptist Catechism was commissioned by the 1693 General Assembly of Particular Baptists and is traditionally attributed to Benjamin Keach, though it was likely drafted by William Collins, Keach’s fellow author of the 1689 confession. It follows the order and much of the wording of the <a href="https://en.wikipedia.org/wiki/Westminster_Shorter_Catechism" target="_blank" rel="noopener">Westminster Shorter Catechism</a>, departing where Baptist conviction requires — most notably on baptism.</p>' +
    '<p>Each answer’s Scripture proof-texts link into the <a href="bible.html">MOOP Bible Translation Engine</a>, and theological terms link to the <a href="dictionary/index.html">MOOP Dictionary</a>. The text is the original 114-question version, in the public domain.</p>' +
    '<p style="font-size:0.85rem;color:var(--gray);"><strong>Note on sections:</strong> the original catechism has no printed section titles; the headings below are editorial reading aids that follow the catechism’s clear structure. The questions and answers themselves are the received historic text, unaltered.</p>' +
    '</section>';

  // Controls: jump + section TOC
  h += '<div class="cat-controls"><h2>Find a question</h2>' +
    '<div class="cat-jump"><label for="cat-jump-input">Jump to question</label>' +
    '<input id="cat-jump-input" type="number" min="1" max="114" placeholder="1–114" inputmode="numeric">' +
    '<button type="button" onclick="catJump()">Go</button></div>';
  if (data.sections && data.sections.length) {
    h += '<nav class="cat-toc" aria-label="Sections"><ol>';
    data.sections.forEach((s, i) => {
      h += '<li><a href="#sec-' + (i + 1) + '">' + escText(s.title) +
        ' <span class="cat-toc-range">(Q' + s.start + '–' + s.end + ')</span></a></li>';
    });
    h += '</ol></nav>';
  }
  h += '</div>';

  // Q&A by section (fall back to a single ungrouped run if no sections)
  const sections = (data.sections && data.sections.length)
    ? data.sections
    : [{ title: 'Questions and Answers', start: 1, end: data.questions.length }];
  sections.forEach((s, i) => {
    h += '<section class="cat-section" id="sec-' + (i + 1) + '">' +
      '<div class="cat-section-head"><div class="cat-section-eyebrow">Section ' + (i + 1) + '</div>' +
      '<h2>' + escText(s.title) + '</h2>' +
      '<div class="cat-section-range">Questions ' + s.start + '–' + s.end + '</div></div>' +
      '<div class="cat-qa">';
    for (let n = s.start; n <= s.end; n++) {
      const q = byNum.get(n);
      if (q) h += qaHtml(q);
    }
    h += '</div></section>';
  });

  // Footer
  h += '<footer class="lbcf-chap-footer" style="max-width:820px;margin:40px auto 0;">' +
    '<p class="lbcf-chap-disclaimer">The Baptist Catechism of 1693 — the original 114-question public-domain text. Free to copy, quote, and share. Scripture proofs and terms are linked for study.</p>' +
    (data.version ? '<p class="lbcf-chap-version">Catechism edition ' + escText(data.version) + ' &middot; usmcmin.org</p>' : '') +
    '</footer>';

  h += '\n    </div>\n' + INLINE_JS + '</body>\n</html>\n';
  return h;
}

function registerSitemap() {
  const p = path.join(DOCS, 'sitemap-main.xml');
  if (!fs.existsSync(p)) return;
  let xml = fs.readFileSync(p, 'utf8');
  if (xml.includes('usmcmin.org/catechism.html')) return;
  const entry = '  <url>\n    <loc>https://usmcmin.org/catechism.html</loc>\n    <lastmod>' + LASTMOD +
    '</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.9</priority>\n  </url>\n';
  xml = xml.replace('</urlset>', entry + '</urlset>');
  fs.writeFileSync(p, xml);
  console.log('Registered /catechism.html in sitemap-main.xml');
}

function main() {
  const data = JSON.parse(fs.readFileSync(DATA, 'utf8'));
  fs.writeFileSync(path.join(DOCS, 'catechism.html'), build(data));
  const links = data.questions.reduce((a, q) => a + (q.prooftexts ? q.prooftexts.length : 0), 0);
  console.log('Wrote docs/catechism.html — ' + data.questions.length + ' Q&A, ' +
    (data.sections ? data.sections.length : 0) + ' sections, ' + links + ' proof-text refs.');
  registerSitemap();
}

main();
