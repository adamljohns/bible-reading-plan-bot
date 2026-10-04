#!/usr/bin/env node
/* generate-confessions.js — static reading pages for Augustine's Confessions (Pilkington 1876).
 *
 * Reads docs/assets/confessions/index.json + b{1..13}.json (parsed by parse-confessions.js).
 * Emits docs/confessions/b{B}.html — ONE PAGE PER BOOK, 13 pages, with Augustine's short
 * chapters as the sections inside. That differs from the Institutes (one page per chapter)
 * on purpose: a Confessions chapter is often a single paragraph, so 276 separate pages would
 * be a worse read and a worse index, and people reach for this book by BOOK — Book VIII for
 * the conversion in the garden, Book X for memory, Book XI for time.
 *
 * Reuses the LBCF link engine via vm (Scripture -> BTE, theological terms -> dictionary),
 * exactly as generate-institutes.js does. Augustine's Apocrypha citations (Wisdom, Sirach)
 * pass through linkScripture as plain text — verified, no broken links.
 *
 * Also writes docs/confessions.html (the hub) and docs/sitemap-confessions.xml.
 *
 * Run: node bin/generate-confessions.js   (re-run after re-parsing)
 */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const DOCS = path.join(ROOT, 'docs');
const DATA = path.join(DOCS, 'assets', 'confessions');
const RENDERER = path.join(DOCS, 'assets', 'js', 'lbcf-render.js');
const LASTMOD = '2026-10-04';

function loadLBCF() {
  const src = fs.readFileSync(RENDERER, 'utf8');
  const sandbox = { window: {}, console };
  vm.createContext(sandbox);
  vm.runInContext(src, sandbox, { filename: 'lbcf-render.js' });
  return sandbox.window.LBCF;
}
const LBCF = loadLBCF();

const ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII'];
const escText = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const escAttr = (s) => escText(s).replace(/"/g, '&quot;');
const bookFile = (b) => 'b' + b + '.html';

// A one-line hook for each book, so the hub reads like a shelf rather than a table.
// These are editorial labels for navigation, not translated content.
const BOOK_HOOKS = {
  1: 'Infancy and boyhood — “Thou hast formed us for Thyself, and our hearts are restless till they find rest in Thee.”',
  2: 'The sixteenth year: the stolen pears, and sin loved for its own sake.',
  3: 'Carthage, the theatre, Cicero’s Hortensius, and nine years among the Manichees.',
  4: 'Teaching rhetoric, the death of a friend, and the first book he ever wrote.',
  5: 'Faustus disappoints him; Rome, then Milan, and Ambrose in the pulpit.',
  6: 'Monica arrives; Ambrose read silently; the long wrestle with ambition and marriage.',
  7: 'The Platonists, the problem of evil, and why he still could not find the Mediator.',
  8: 'The garden at Milan — “Take up and read” — and the will finally undivided.',
  9: 'Baptism, Ostia, and the death of Monica.',
  10: 'What memory is, and how a man seeks God in the fields and vast palaces of it.',
  11: 'Time: “What then is time? If no one asks me, I know.”',
  12: 'Heaven and earth, formless matter, and the humility of reading Genesis charitably.',
  13: 'The days of creation read as the shape of grace and of the Church.',
};

function nav() {
  const item = (href, icon, label, active) =>
    '<a href="' + href + '"' + (active ? ' class="active"' : '') + '><img src="../assets/icons/' + icon +
    '" class="site-icon" alt="' + label + '" width="16" height="16"> ' + label + '</a>';
  return '<nav>' +
    item('../index.html', 'shield-home-48.png', 'Uniting, Serving, Mentoring and Counseling Ministries Home', false) +
    item('../watchman.html', 'shield-bible.png', 'Watchman Bible Plan', false) +
    item('../bible.html', 'shield-bible-cross-48.png', 'Bible Translation Engine', false) +
    item('../lexicon.html', 'shield-alpha-omega-48.png', 'Lexicon', false) +
    item('../dictionary/index.html', 'shield-book-greek-48.png', 'Dictionary', false) +
    item('../lbcf.html', 'shield-cross.png', '1689 LBCF', false) +
    item('../catechism.html', 'shield-cross.png', 'Baptist Catechism', false) +
    item('../institutes.html', 'shield-cross.png', 'Institutes', false) +
    item('../confessions.html', 'shield-cross.png', 'Confessions', true) +
    item('../blog.html', 'shield-scroll-quill-48.png', 'Blog', false) +
    item('../connect.html', 'shield-handshake.png', 'Connect', false) +
    '<div class="bte-theme-toggle nav-theme-toggle" onclick="confToggleTheme()" title="Toggle dark/light mode" role="button" tabindex="0" aria-label="Toggle dark/light mode"></div>' +
    '</nav>';
}
// The hub sits at docs/confessions.html, so its nav needs root-relative asset paths.
const navHub = () => nav().replace(/\.\.\//g, '').replace(/src="assets\//g, 'src="assets/');

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
  '        function confToggleTheme(){document.body.classList.toggle("light-mode");try{localStorage.setItem("bte-theme",document.body.classList.contains("light-mode")?"light":"dark");}catch(e){}}\n' +
  '        try{var t=localStorage.getItem("bte-theme");if(t===null&&(t=localStorage.getItem("moop-theme"))!==null)localStorage.setItem("bte-theme",t);if(t==="light")document.body.classList.add("light-mode");}catch(e){}\n' +
  '        document.querySelectorAll(".conf-permalink").forEach(function(a){a.addEventListener("click",function(e){e.preventDefault();var u=location.origin+location.pathname+a.getAttribute("href");if(navigator.clipboard)navigator.clipboard.writeText(u).then(function(){a.classList.add("copied");var o=a.textContent;a.textContent="\\u2713";setTimeout(function(){a.classList.remove("copied");a.textContent=o;},1200);});});});\n' +
  '    </script>\n' +
  '    <script>if("serviceWorker" in navigator){navigator.serviceWorker.register("/sw.js")}</script>\n';

function head(title, desc, canonical, cssPrefix) {
  return '<!DOCTYPE html>\n<html lang="en">\n<head>\n' +
    '    <meta charset="UTF-8">\n' +
    '    <link rel="canonical" href="' + canonical + '">\n' +
    '    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">\n' +
    '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n' +
    '    <title>' + escText(title) + '</title>\n' +
    '    <meta name="description" content="' + escAttr(desc) + '">\n' +
    '    <meta property="og:title" content="' + escAttr(title) + '">\n' +
    '    <meta property="og:description" content="' + escAttr(desc) + '">\n' +
    '    <meta property="og:type" content="article">\n    <meta property="og:url" content="' + canonical + '">\n' +
    '    <meta property="og:image" content="https://usmcmin.org/assets/og/og-bible.png">\n' +
    '    <meta name="twitter:card" content="summary_large_image">\n' +
    '    <link rel="preconnect" href="https://fonts.googleapis.com">\n' +
    '    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">\n' +
    '    <link rel="stylesheet" href="' + cssPrefix + 'assets/css/lbcf.css">\n' +
    '    <link rel="stylesheet" href="' + cssPrefix + 'assets/css/confessions.css">\n' +
    '    <link rel="stylesheet" href="/assets/css/listen.css">\n' +
    '    <link rel="manifest" href="/manifest.json">\n' +
    '    <link rel="stylesheet" href="/assets/css/light-icons.css">\n' +
    '    <link rel="stylesheet" href="/assets/css/print.css" media="print">\n' +
    STYLE + '</head>\n<body>\n';
}

const PROVENANCE =
  'From <strong>J.G. Pilkington\u2019s</strong> translation (1876) of Augustine\u2019s <em>Confessions</em> (c. 400), ' +
  'as published in <em>Nicene and Post-Nicene Fathers</em>, Series I, Volume 1, edited by Philip Schaff (1886) \u2014 ' +
  'a public-domain text from <a href="https://www.ccel.org/ccel/schaff/npnf101.html" target="_blank" rel="noopener">CCEL</a>. ' +
  'Free to copy, quote, and share. Scripture and theological terms are linked for study.';

function bookPage(doc, prev, next) {
  const b = doc.book;
  const canonical = 'https://usmcmin.org/confessions/' + bookFile(b);
  const desc = 'Augustine\u2019s Confessions, Book ' + ROMAN[b] + ' \u2014 ' + String(doc.argument).slice(0, 150);
  let h = head('Confessions, Book ' + ROMAN[b] + ' \u2014 Augustine (Pilkington)', desc, canonical, '../') +
    nav() + '\n    <div class="container">\n';

  h += '<header class="conf-book-head">' +
    '<div class="conf-book-eyebrow">Augustine \u00b7 Confessions \u00b7 Book ' + ROMAN[b] + '</div>' +
    '<h1>Book ' + ROMAN[b] + '</h1>' +
    (BOOK_HOOKS[b] ? '<p class="conf-book-hook">' + escText(BOOK_HOOKS[b]) + '</p>' : '') +
    '<p class="conf-argument">' + escText(doc.argument) + '</p>' +
    '<div class="conf-chip">Pilkington 1876</div>' +
    '</header>';

  // Chapter index — Book X has 43 chapters, so a reader needs a way in.
  h += '<details class="conf-toc"><summary>The ' + doc.chapters.length + ' chapters of Book ' + ROMAN[b] + '</summary><ol>';
  doc.chapters.forEach((c) => {
    h += '<li><a href="#c' + c.n + '">' + escText(c.title) + '</a></li>';
  });
  h += '</ol></details>';

  h += '<div class="conf-body">';
  doc.chapters.forEach((c) => {
    h += '<article class="conf-chapter" id="c' + c.n + '">' +
      '<header class="conf-chap-head">' +
      '<div class="conf-chap-num">Chapter ' + c.n +
      '<a class="conf-permalink" href="#c' + c.n + '" title="Copy link to this chapter" aria-label="Copy permalink">\u00b6</a></div>' +
      '<h2>' + escText(c.title) + '</h2>' +
      '</header>';
    c.sections.forEach((sec) => {
      h += '<section class="conf-section"' + (sec.n != null ? ' id="s' + sec.n + '"' : '') + '>' +
        (sec.n != null ? '<div class="conf-sec-num">' + sec.n + '</div>' : '<div class="conf-sec-num"></div>') +
        '<div class="conf-sec-body">';
      sec.paragraphs.forEach((p) => { h += '<p>' + LBCF.autoLink(p, 0, new Set()) + '</p>'; });
      h += '</div></section>';
    });
    if (c.prooftexts && c.prooftexts.length) {
      const refs = c.prooftexts.map((r) => LBCF.linkScripture(r)).join(' &middot; ');
      h += '<details class="lbcf-proofs"><summary>Scripture cited in this chapter</summary><div>' + refs + '</div></details>';
    }
    h += '</article>';
  });
  h += '</div>';

  const prevLink = prev ? '<a class="conf-prev" href="' + bookFile(prev) + '">\u2190 Book ' + ROMAN[prev] + '</a>' : '<span></span>';
  const nextLink = next ? '<a class="conf-next" href="' + bookFile(next) + '">Book ' + ROMAN[next] + ' \u2192</a>' : '<span></span>';
  h += '<div class="conf-book-nav">' + prevLink + '<a class="conf-idx" href="../confessions.html">All Books</a>' + nextLink + '</div>';

  h += '<footer class="conf-foot"><p class="conf-disclaimer">' + PROVENANCE + '</p></footer>';
  h += '\n    </div>\n' + SCRIPT + '</body>\n</html>\n';
  return h;
}

function hubPage(index) {
  const canonical = 'https://usmcmin.org/confessions.html';
  const totalCh = index.books.reduce((a, b) => a + b.chapters, 0);
  const desc = 'Augustine\u2019s Confessions in J.G. Pilkington\u2019s public-domain translation (1876) \u2014 all 13 books, ' +
    totalCh + ' chapters, with every Scripture reference linked for study. Free to read on usmcmin.org.';
  let h = head('Augustine\u2019s Confessions \u2014 Uniting, Serving, Mentoring and Counseling Ministries', desc, canonical, '') +
    navHub() + '\n    <div class="container">\n';

  h += '<header class="conf-hub-head">' +
    '<div class="conf-book-eyebrow">A free, linked, mobile-clean edition</div>' +
    '<h1>The Confessions of St. Augustine</h1>' +
    '<p class="conf-hub-lede">Written around the year 400, the <em>Confessions</em> is the first real autobiography in ' +
    'Western literature and still the most searching \u2014 but Augustine wrote it as a prayer, addressed to God from ' +
    'the first line to the last. It is here because Calvin leaned on Augustine more heavily than on any other human ' +
    'author, and because a Reformed library ought to carry the fathers it stands on.</p>' +
    '<p class="conf-hub-meta">All 13 books \u00b7 ' + totalCh + ' chapters \u00b7 ' +
    index.books.reduce((a, b) => a + b.refs, 0) + ' linked Scripture references \u00b7 ' +
    '<strong>Pilkington 1876</strong>, public domain</p>' +
    '</header>';

  h += '<div class="conf-grid">';
  index.books.forEach((b) => {
    h += '<a class="conf-card" href="confessions/' + bookFile(b.number) + '">' +
      '<div class="conf-card-num">Book ' + ROMAN[b.number] + '</div>' +
      (BOOK_HOOKS[b.number] ? '<div class="conf-card-hook">' + escText(BOOK_HOOKS[b.number]) + '</div>' : '') +
      '<div class="conf-card-meta">' + b.chapters + ' chapters \u00b7 ' + b.refs + ' refs</div>' +
      '</a>';
  });
  h += '</div>';

  h += '<aside class="conf-note"><div class="conf-note-head">A note on the translation</div>' +
    '<p>We publish Pilkington\u2019s 1876 translation, printed in Schaff\u2019s <em>Nicene and Post-Nicene Fathers</em> ' +
    'in 1886 and long out of copyright. The better-known modern renderings \u2014 Outler, Sheed, Chadwick, Boulding \u2014 ' +
    'are all still under copyright, whatever a given website may assert about them, so they cannot be given away freely. ' +
    'Pilkington can, and he is faithful and readable. Scripture citations throughout are his own footnotes, linked here ' +
    'to the Bible Translation Engine; a handful of them have been corrected where the digital source mis-parsed his ' +
    'Roman numerals.</p></aside>';

  h += '<footer class="conf-foot"><p class="conf-disclaimer">' + PROVENANCE + '</p></footer>';
  h += '\n    </div>\n' + SCRIPT + '</body>\n</html>\n';
  return h;
}

function writeSitemap(index) {
  const url = (loc, pri) => '  <url>\n    <loc>https://usmcmin.org/' + loc + '</loc>\n    <lastmod>' + LASTMOD +
    '</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>' + pri + '</priority>\n  </url>\n';
  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
  xml += url('confessions.html', '0.9');
  index.books.forEach((b) => { xml += url('confessions/' + bookFile(b.number), '0.6'); });
  xml += '</urlset>\n';
  fs.writeFileSync(path.join(DOCS, 'sitemap-confessions.xml'), xml);
  const idxPath = path.join(DOCS, 'sitemap.xml');
  let idx = fs.readFileSync(idxPath, 'utf8');
  if (!idx.includes('sitemap-confessions.xml')) {
    idx = idx.replace('</sitemapindex>', '  <sitemap>\n    <loc>https://usmcmin.org/sitemap-confessions.xml</loc>\n    <lastmod>' + LASTMOD + '</lastmod>\n  </sitemap>\n</sitemapindex>');
    fs.writeFileSync(idxPath, idx);
    console.log('Registered sitemap-confessions.xml in sitemap.xml');
  }
  console.log('Wrote sitemap-confessions.xml (' + (index.books.length + 1) + ' urls)');
}

function main() {
  const index = JSON.parse(fs.readFileSync(path.join(DATA, 'index.json'), 'utf8'));
  const docs = index.books.map((b) => JSON.parse(fs.readFileSync(path.join(DATA, 'b' + b.number + '.json'), 'utf8')));
  fs.mkdirSync(path.join(DOCS, 'confessions'), { recursive: true });

  let links = 0;
  docs.forEach((doc, i) => {
    const html = bookPage(doc, i > 0 ? docs[i - 1].book : null, i + 1 < docs.length ? docs[i + 1].book : null);
    fs.writeFileSync(path.join(DOCS, 'confessions', bookFile(doc.book)), html);
    links += (html.match(/class="lbcf-scrip"/g) || []).length;
    console.log('  Book ' + String(doc.book).padStart(2) + ': ' + String(doc.chapters.length).padStart(2) +
      ' chapters, ' + (html.length / 1024).toFixed(0) + ' KB');
  });
  fs.writeFileSync(path.join(DOCS, 'confessions.html'), hubPage(index));
  writeSitemap(index);
  console.log('Wrote 13 book pages + confessions.html; ' + links + ' linked Scripture references rendered.');
}
main();
