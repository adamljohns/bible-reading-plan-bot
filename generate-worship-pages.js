#!/usr/bin/env node
/*
 * generate-worship-pages.js
 * -------------------------------------------------------------------------
 * Builds the USMC Ministries "Worship" section from Adam's decades-old
 * chord-chart archive (chords typed above the word where they're played).
 *
 * Phase 1 (ingest):  read .crd / .tab charts from the archive
 *                    -> docs/data/worship-songs.json   (canonical, in-repo)
 * Phase 2 (generate): JSON -> docs/worship.html  +  docs/worship/<slug>.html
 *
 * Usage:
 *   node generate-worship-pages.js            # ingest if JSON missing, then build
 *   node generate-worship-pages.js --ingest   # force re-ingest from the archive
 *   node generate-worship-pages.js --pages    # skip ingest, rebuild pages from JSON
 *
 * Optional per-song enrichment (added by hand, survives re-ingest):
 *   docs/data/worship-overrides.json  ->  { "<slug>": { "youtube": "<id|url>",
 *                                                        "slides": "<file.pdf>",
 *                                                        "key": "G" } }
 * -------------------------------------------------------------------------
 */
'use strict';
const fs = require('fs');
const path = require('path');

const REPO = __dirname;
// Canonical source: the USMC-Ministries copy of the worship archive.
const SRC = '/Users/moop_bot_pro/Documents/01-Faith-Ministry/USMC-Ministries/Documents/Worship Songs (doc)/1) Indexes';
const DATA_DIR = path.join(REPO, 'docs/data');
const DATA_JSON = path.join(DATA_DIR, 'worship-songs.json');
const OVERRIDES_JSON = path.join(DATA_DIR, 'worship-overrides.json');
const OUT_DIR = path.join(REPO, 'docs/worship');
const INDEX_HTML = path.join(REPO, 'docs/worship.html');
const BUILD_DATE = new Date().toLocaleDateString('en-CA', { timeZone: 'America/New_York' });

const args = process.argv.slice(2);
const FORCE_INGEST = args.includes('--ingest');
const PAGES_ONLY = args.includes('--pages');

/* ───────────────────────── text + parsing helpers ───────────────────────── */

// Charts are decades old — mostly ASCII, but some carry Mac-Roman / Win-1252
// smart punctuation. Read as latin1 (byte-faithful) and normalize gently.
function readText(file) {
  let s = fs.readFileSync(file).toString('latin1');
  s = s.replace(/\r\n?/g, '\n');
  s = s.replace(/[’]/g, "'")
       .replace(/[“”]/g, '"')
       .replace(/[–—]/g, '-')
       .replace(/ /g, ' ')
       .replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, '');
  // Trim trailing whitespace per line (alignment is left-anchored).
  s = s.split('\n').map(l => l.replace(/\s+$/,'')).join('\n');
  // Strip leading mbox / usenet header cruft — many charts were emailed in the
  // 1990s and still carry "From user@host <date>" + "Subject:/Date:/X-…" headers.
  const MBOX = /^From \S+@\S+|^From .+\b(19|20)\d\d\s*$/;
  const HDR = /^(Date|Subject|Newsgroups|Path|Message-ID|Sender|Reply-To|Reply To|Organization|Lines|References|Return-Path|Received|To|Cc|From|In-Reply-To|MIME-Version|Content-Type|Content-Transfer-Encoding|X-[\w-]+):\s/i;
  let lines = s.split('\n');
  let i = 0;
  while (i < lines.length && (lines[i].trim() === '' || MBOX.test(lines[i]) || HDR.test(lines[i]))) i++;
  if (i > 0 && i < lines.length) lines = lines.slice(i);
  s = lines.join('\n');
  s = s.replace(/^\n+/, '').replace(/\n{3,}/g, '\n\n').replace(/\n+$/,'');
  return s;
}

function escapeHtml(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
                  .replace(/"/g,'&quot;');
}

function slugify(s) {
  return s.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'').slice(0,80) || 'song';
}

function prettyName(base) {
  return base.replace(/\.(crd|tab)$/i,'').replace(/[_]+/g,' ').replace(/\s+/g,' ').trim()
             .replace(/\b([a-z])/g, (m,c)=>c.toUpperCase());
}

// A single chord token, e.g.  C  Am7  F#m7b5  Dsus4  G/B  N.C.  (Bb)
const CHORD = /^[\(\[]?(?:[A-G][#b]?(?:maj|min|m|sus|aug|dim|add|M)?\d{0,2}(?:[#b]?\d{1,2})?(?:sus|add|maj|min|dim|aug)?\d{0,2}(?:\/[A-G][#b]?)?)[\)\]]?[,]?$/;
const BARSYM = /^(?:\|+|:?\|:?|x\d+|\(x\d+\)|\d+x|N\.?C\.?|-{2,}|={2,}|%|\/{2,})$/i;

function isChordToken(t){ return CHORD.test(t); }
function isChordOrBar(t){ return CHORD.test(t) || BARSYM.test(t); }

function isChordLine(line) {
  const t = line.trim();
  if (!t) return false;
  const toks = t.split(/\s+/);
  let good = 0;
  for (const tk of toks) if (isChordOrBar(tk)) good++;
  return good >= 1 && good / toks.length >= 0.6;
}

const SECTION_RE = /^(intro|verse|chorus|pre-?chorus|bridge|tag|interlude|outro|ending|refrain|coda|instrumental|solo|vamp|turnaround|hook|chant|response|repeat|capo|key)\b/i;
function isSectionLine(line) {
  const t = line.trim();
  return !!t && t.length < 42 && SECTION_RE.test(t) && !isChordLine(line);
}

// Pull leading metadata lines (Title:, Author:, Key:, CCLI, ©, etc.) off the
// top of the file so they don't duplicate the page heading. Returns {meta, body}.
const META_RE = /^(title|song|author|artist|by|words?|music|words?\s*&\s*music|key|tempo|time|ccli|group\s*\/?\s*cd|group|cd|album|transcribed by|arr\.?|arranged by|from)\b\s*[:.-]?\s*(.*)$/i;
function parseMeta(raw) {
  const lines = raw.split('\n');
  const meta = {};
  let i = 0;
  for (; i < lines.length && i < 8; i++) {
    const ln = lines[i];
    if (ln.trim() === '') { if (Object.keys(meta).length) { i++; break; } continue; }
    const m = ln.match(META_RE);
    if (!m) break;
    const key = m[1].toLowerCase().replace(/\s+/g,' ').trim();
    if (!meta[key]) meta[key] = m[2].trim();
  }
  // Only strip the leading meta block if we actually found Title/Song there.
  const body = (meta.title || meta.song) ? lines.slice(i).join('\n').replace(/^\n+/,'') : raw;
  return { meta, body };
}

function detectKey(meta, body) {
  if (meta.key) return meta.key.split(/[\s,(]/)[0].trim();
  for (const line of body.split('\n')) {
    if (!isChordLine(line)) continue;
    for (const tk of line.trim().split(/\s+/)) {
      const m = tk.match(/^[\(\[]?([A-G][#b]?)/);
      if (m && isChordToken(tk)) return m[1];
    }
  }
  return '';
}

/* ───────────────────────────── ingest phase ───────────────────────────── */

function walk(dir, acc) {
  for (const name of fs.readdirSync(dir)) {
    if (name.startsWith('.')) continue;
    const p = path.join(dir, name);
    let st; try { st = fs.statSync(p); } catch { continue; }
    if (st.isDirectory()) walk(p, acc);
    else if (/\.(crd|tab)$/i.test(name)) acc.push(p);
  }
  return acc;
}

function ingest() {
  console.log('Ingesting chord archive from:\n  ' + SRC);
  if (!fs.existsSync(SRC)) {
    console.error('!! Source archive not found. Aborting ingest.');
    process.exit(1);
  }
  const files = walk(SRC, []).sort((a, b) => {
    // Praise charts before tabs, so plain song slugs win the un-suffixed name.
    const pa = /\/Praise\//i.test(a) ? 0 : 1;
    const pb = /\/Praise\//i.test(b) ? 0 : 1;
    return pa - pb || a.localeCompare(b);
  });

  const songs = [];
  const slugs = new Set();
  let skipped = 0;

  for (const file of files) {
    let raw;
    try { raw = readText(file); } catch { skipped++; continue; }
    if (!raw.trim()) { skipped++; continue; }

    const ext = path.extname(file).slice(1).toLowerCase();      // crd | tab
    // The content format is the truth: a .crd is a chord chart even when it
    // lives in the tab/ folder. Only true .tab files are labeled guitar tabs.
    const type = ext === 'tab' ? 'tab' : 'praise';
    const christmas = /\/christmas\//i.test(file);
    const base = path.basename(file);

    const { meta, body } = parseMeta(raw);
    let title = (meta.title || meta.song || prettyName(base)).replace(/\s+/g, ' ').trim();
    // Some headers read "Song Title: ..." — the meta regex captures "Song" and
    // leaves "Title:" in the value. Strip any leaked label, then wrapping quotes.
    title = title.replace(/^(song\s+title|title|song)\s*[:.\-]\s*/i, '');
    title = title.replace(/^["'`\s]+/, '').replace(/["'`\s]+$/, '').trim();
    // If a meta line parsed into junk (no leading alphanumeric, or too short),
    // fall back to the filename — it's the most reliable title source.
    if (!/^[A-Za-z0-9(]/.test(title) || title.length < 2) title = prettyName(base);
    const author = meta.author || meta.artist || meta.by || meta['words & music'] || meta.words || meta.music || '';
    const key = detectKey(meta, body);

    let slug = slugify(title);
    if (slugs.has(slug)) {
      let cand = type === 'tab' ? slug + '-tab' : slug + '-2';
      let n = 2;
      while (slugs.has(cand)) cand = slug + '-' + (++n);
      slug = cand;
    }
    slugs.add(slug);

    const letter = (title.match(/[A-Za-z]/) || ['#'])[0].toUpperCase();

    // Drop a leading body line that just repeats the title (it's already the H1).
    let bodyClean = body;
    const norm = (x) => x.toLowerCase().replace(/[^a-z0-9]/g, '');
    const firstLine = body.split('\n').find(l => l.trim()) || '';
    if (firstLine && norm(firstLine) === norm(title)) {
      bodyClean = body.replace(/^[^\n]*\n?/, '').replace(/^\n+/, '');
    }

    songs.push({
      slug, title, type, christmas,
      key, author,
      letter: /[A-Z]/.test(letter) ? letter : '#',
      ext,
      src: path.relative(SRC, file),
      body: bodyClean,
      youtube: null,
      slides: null,
    });
  }

  songs.sort((a, b) => a.title.toLowerCase().localeCompare(b.title.toLowerCase()));
  fs.mkdirSync(DATA_DIR, { recursive: true });
  fs.writeFileSync(DATA_JSON, JSON.stringify(songs, null, 1));
  console.log(`Ingested ${songs.length} charts (${skipped} skipped) -> ${path.relative(REPO, DATA_JSON)}`);
  return songs;
}

/* ───────────────────────── shared HTML fragments ───────────────────────── */

function pageHead(title, desc, canonicalPath, depth) {
  const root = depth ? '../' : '';
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="canonical" href="https://usmcmin.org/${canonicalPath}">
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
    <link rel="manifest" href="/manifest.json">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="${escapeHtml(title)}">
    <meta property="og:description" content="${escapeHtml(desc)}">
    <meta property="og:image" content="https://usmcmin.org/assets/og/og-lexicon.png?v=51">
    <meta name="description" content="${escapeHtml(desc)}">
    <title>${escapeHtml(title)}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/assets/css/light-icons.css">
    <link rel="stylesheet" href="/assets/css/print.css" media="print">`;
}

function navBlock(depth) {
  const r = depth ? '../' : '';
  const cls = (p) => p === 'worship' ? ' class="active"' : '';
  const link = (href, icon, label, key) =>
    `        <a href="${r}${href}"${cls(key)}><img src="${r}assets/icons/${icon}" class="site-icon" alt="" width="16" height="16"> ${label}</a>`;
  return `<nav>
${link('index.html','shield-home-48.png','Home','home')}
${link('watchman.html','shield-bible.png','Watchman','watchman')}
${link('bible.html','shield-bible-cross-48.png','BTE','bte')}
${link('lexicon.html','shield-alpha-omega-48.png','Lexicon','lexicon')}
${link('cross-references.html','shield-infinity-rope-48.png','Cross-Refs','xref')}
${link('dictionary/index.html','shield-book-greek-48.png','Dictionary','dict')}
${link('worship.html','shield-quill-note-48.png','Worship','worship')}
${link('blog.html','shield-scroll-quill-48.png','Blog','blog')}
${link('connect.html','shield-handshake.png','Connect','connect')}
    </nav>
    <div style="text-align:center; margin-top:8px; margin-bottom:4px;">
        <div class="bte-theme-toggle" onclick="bteToggleTheme()" title="Toggle dark/light mode">
            <span class="toggle-icon moon-icon">🌙</span>
            <div class="toggle-track"><div class="toggle-knob"></div></div>
            <span class="toggle-icon sun-icon">☀️</span>
        </div>
    </div>`;
}

function footerBlock(depth) {
  const r = depth ? '../' : '';
  return `<footer style="text-align:center; padding:28px 20px; border-top:1px solid var(--border,#333); margin-top:40px; color:var(--gray,#888); font-size:0.88rem;">
    <div style="margin-bottom:10px;"><img src="${r}assets/icons/shield-quill-note-48.png" alt="" width="36" height="36" style="opacity:0.6;"></div>
    <p><a href="${r}index.html" style="color:var(--gray,#888);text-decoration:none;"><img src="${r}assets/icons/shield-home-48.png" style="vertical-align:middle;opacity:0.8;" alt="" width="16" height="16"> Home</a> &middot;
        <a href="${r}worship.html" style="color:var(--gray,#888);text-decoration:none;"><img src="${r}assets/icons/shield-quill-note-48.png" style="vertical-align:middle;opacity:0.8;" alt="" width="16" height="16"> Worship</a> &middot;
        <a href="${r}bible.html" style="color:var(--gray,#888);text-decoration:none;"><img src="${r}assets/icons/shield-bible-cross-48.png" style="vertical-align:middle;opacity:0.8;" alt="" width="16" height="16"> BTE</a> &middot;
        <a href="${r}blog.html" style="color:var(--gray,#888);text-decoration:none;"><img src="${r}assets/icons/shield-scroll-quill-48.png" style="vertical-align:middle;opacity:0.8;" alt="" width="16" height="16"> Blog</a> &middot;
        <a href="${r}connect.html" style="color:var(--gray,#888);text-decoration:none;"><img src="${r}assets/icons/shield-handshake.png" style="vertical-align:middle;opacity:0.8;" alt="" width="16" height="16"> Connect</a></p>
    <p style="margin-top:8px;font-size:0.78rem;color:#555;">&ldquo;Sing to the Lord a new song.&rdquo; &mdash; <a href="${r}bible.html?ref=Psalm+96:1" style="color:var(--gold,#D4AF37);text-decoration:underline;">Psalm 96:1</a> &middot; Built for worship leaders &middot; ${BUILD_DATE}</p>
</footer>`;
}

// Shared CSS tokens + nav/toggle styling, replicated from the site's tool pages.
const BASE_CSS = `
        * { margin:0; padding:0; box-sizing:border-box; }
        :root { --bg-dark:#000; --bg-card:#111; --gold:#D4AF37; --gold-light:#F4D470; --white:#FFF; --gray:#888; --border:#333; --scarlet:#CC0000; }
        body { font-family:'Inter',sans-serif; background:var(--bg-dark); color:var(--white); min-height:100vh; line-height:1.6; }
        h1,h2,h3 { font-family:'Playfair Display',serif; font-weight:700; }
        a { color:var(--gold); }
        .container { max-width:1000px; margin:0 auto; padding:20px; }
        .site-icon { vertical-align:middle; margin-right:4px; }
        nav { display:flex; flex-wrap:wrap; gap:6px; justify-content:center; padding:14px 20px; border-bottom:1px solid var(--border); background:rgba(0,0,0,0.95); position:sticky; top:0; z-index:100; }
        nav a { color:var(--gray); text-decoration:none; font-size:0.85rem; font-weight:500; padding:5px 12px; border-radius:20px; border:1px solid transparent; transition:all 0.2s; white-space:nowrap; }
        nav a:hover { color:var(--gold); border-color:var(--border); }
        nav a:link,nav a:visited,nav a:active { color:var(--gray) !important; text-decoration:none !important; }
        nav a.active { color:var(--gold) !important; border-color:var(--gold); }
        .bte-theme-toggle { display:flex;align-items:center;justify-content:center;margin:8px auto 0;width:fit-content;background:rgba(30,30,30,0.85);border:1px solid #333;border-radius:20px;padding:3px 6px;cursor:pointer;font-size:0.7rem;user-select:none; }
        .bte-theme-toggle:hover{border-color:#D4AF37;}
        .bte-theme-toggle .toggle-icon{width:18px;text-align:center;}
        .bte-theme-toggle .toggle-track{width:28px;height:14px;background:#444;border-radius:7px;position:relative;margin:0 4px;}
        .bte-theme-toggle .toggle-knob{width:10px;height:10px;background:#D4AF37;border-radius:50%;position:absolute;top:2px;left:2px;transition:left 0.3s;}
        body.light-mode .bte-theme-toggle{background:rgba(240,238,233,0.9);border-color:#ccc;}
        body.light-mode .bte-theme-toggle .toggle-track{background:#bbb;}
        body.light-mode .bte-theme-toggle .toggle-knob{left:16px;}
        body.light-mode { background:#FAF8F5; color:#1a1a1a; }
        body.light-mode nav { background:rgba(250,248,245,0.97); }
        body.light-mode .site-icon { filter:brightness(0.6); }
        body.light-mode img[src*="/icons/shield-"]:not([src*="-bronze"]) { filter:brightness(.72) saturate(1.18) hue-rotate(-12deg); }`;

const THEME_RESTORE = `<script>(function(){if(localStorage.getItem("bte-theme")==="light")document.body.classList.add("light-mode");})();</script>
<script>function bteToggleTheme(){document.body.classList.toggle("light-mode");localStorage.setItem("bte-theme",document.body.classList.contains("light-mode")?"light":"dark");}</script>`;

/* ───────────────────────── render a chord chart ───────────────────────── */

function renderChart(body) {
  return body.split('\n').map(line => {
    if (line.trim() === '') return `<span class="ln ln-blank">\n</span>`;
    const esc = escapeHtml(line);
    if (isSectionLine(line)) return `<span class="ln ln-sec">${esc}\n</span>`;
    if (isChordLine(line))   return `<span class="ln ln-chord" data-orig="${esc}">${esc}\n</span>`;
    return `<span class="ln ln-lyric">${esc}\n</span>`;
  }).join('');
}

/* ───────────────────────────── song pages ───────────────────────────── */

const SONG_CSS = `
        .crumb { font-size:.8rem; color:var(--gray); margin-bottom:6px; }
        .crumb a { color:var(--gray); text-decoration:none; }
        .crumb a:hover { color:var(--gold); }
        .song-head { display:flex; flex-wrap:wrap; align-items:baseline; gap:10px 14px; margin:6px 0 4px; }
        .song-head h1 { font-size:clamp(1.5rem,3.5vw,2.1rem); color:var(--white); }
        body.light-mode .song-head h1 { color:#1a1a1a; }
        .badge { background:rgba(212,175,55,.15); color:var(--gold); font-size:.78rem; font-weight:600; padding:3px 10px; border-radius:12px; }
        .sub { color:var(--gray); font-size:.86rem; margin-bottom:14px; }
        .toolbar { display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin:0 0 16px; padding:10px 12px; background:var(--bg-card); border:1px solid var(--border); border-radius:10px; position:sticky; top:60px; z-index:50; }
        body.light-mode .toolbar { background:#fff; border-color:#d4d0c8; }
        .tb-group { display:flex; align-items:center; gap:4px; }
        .tb-label { font-size:.7rem; text-transform:uppercase; letter-spacing:.5px; color:var(--gray); margin-right:2px; }
        .tb-btn { background:transparent; color:var(--gold); border:1px solid var(--gold); border-radius:8px; padding:4px 10px; font-size:.8rem; font-weight:600; cursor:pointer; transition:all .15s; font-family:'Inter',sans-serif; }
        .tb-btn:hover { background:rgba(212,175,55,.15); }
        .tb-btn.active { background:var(--gold); color:#000; }
        .tb-readout { min-width:34px; text-align:center; font-size:.82rem; color:var(--gold-light); font-weight:600; }
        pre.chart { font-family:'JetBrains Mono','SFMono-Regular',Menlo,Consolas,monospace; font-size:15px; line-height:1.55; white-space:pre; overflow-x:auto; tab-size:8; -moz-tab-size:8; color:var(--white); background:var(--bg-card); border:1px solid var(--border); border-radius:12px; padding:20px 18px; }
        body.light-mode pre.chart { background:#fff; color:#1a1a1a; border-color:#d4d0c8; }
        .ln-chord { color:var(--gold); font-weight:600; }
        .ln-sec { color:var(--gold-light); font-weight:700; }
        body.light-mode .ln-chord { color:#a6801a; }
        body.light-mode .ln-sec { color:#7a5c00; }
        .chart.hide-chords .ln-chord { display:none; }
        .media { margin:22px 0; }
        .media iframe { width:100%; aspect-ratio:16/9; border:0; border-radius:12px; }
        .dl-row { display:flex; flex-wrap:wrap; gap:10px; margin:18px 0; }
        .dl-btn { color:var(--gold); text-decoration:none; padding:8px 16px; border:1px solid var(--border); border-radius:8px; display:inline-flex; align-items:center; gap:6px; transition:all .2s; font-size:.9rem; }
        .dl-btn:hover { border-color:var(--gold); background:rgba(212,175,55,.1); }
        .note { color:var(--gray); font-size:.82rem; font-style:italic; margin-top:8px; }
        @media (max-width:600px){ .toolbar{ top:54px; } pre.chart{ font-size:13px; padding:14px 12px; } }
        /* Print: clean sheet that matches the original directory chart — monospace
           preserved, chords bold black, no chrome. */
        @media print {
            nav, .crumb, .sub, .toolbar, .media, .dl-row, footer, .bte-theme-toggle { display:none !important; }
            .container { max-width:none; margin:0; padding:0; }
            .song-head { margin:0 0 2px; }
            .song-head h1 { font-size:18pt !important; color:#000 !important; }
            .badge { background:#fff !important; color:#000 !important; border:1px solid #000; font-size:10pt; }
            pre.chart { border:0 !important; background:#fff !important; color:#000 !important; padding:0 !important; margin:6px 0 0; font-size:10.5pt; line-height:1.35; white-space:pre; overflow:visible !important; }
            .ln-chord, .ln-sec { color:#000 !important; font-weight:700 !important; }
            .ln-lyric { color:#000 !important; }
        }`;

function youtubeId(v) {
  if (!v) return '';
  const m = String(v).match(/(?:youtu\.be\/|v=|embed\/|shorts\/)([A-Za-z0-9_-]{6,})/);
  return m ? m[1] : (/^[A-Za-z0-9_-]{6,}$/.test(v) ? v : '');
}

function songPage(song) {
  const tagLabel = song.type === 'tab' ? 'Guitar Tab' : (song.christmas ? 'Christmas' : 'Praise & Worship');
  const subBits = [];
  if (song.author) subBits.push(escapeHtml(song.author));
  subBits.push(tagLabel);
  const yt = youtubeId(song.youtube);
  const media = yt
    ? `\n        <div class="media"><iframe src="https://www.youtube-nocookie.com/embed/${yt}" title="${escapeHtml(song.title)} — video" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>`
    : '';
  const slides = song.slides
    ? `<a class="dl-btn" href="slides/${encodeURIComponent(song.slides)}" download><img src="../assets/icons/shield-quill-note-48.png" width="16" height="16" alt=""> Download slides</a>`
    : '';
  const ytSearch = 'https://www.youtube.com/results?search_query=' + encodeURIComponent(song.title + ' worship song');
  const ytBtn = `<a class="dl-btn" href="${ytSearch}" target="_blank" rel="noopener"><span style="color:#ff4d4d">▶</span> ${yt ? 'More versions on YouTube' : 'Find on YouTube'}</a>`;
  // Tab/chord site deep-link — same idea as BTE linking out to Blue Letter Bible.
  const ugSearch = 'https://www.ultimate-guitar.com/search.php?search_type=title&value=' + encodeURIComponent(song.title);
  const ugBtn = `<a class="dl-btn" href="${ugSearch}" target="_blank" rel="noopener">🎸 Tabs &amp; chords on Ultimate Guitar</a>`;

  return `${pageHead(song.title + ' — Chords & Lyrics | USMC Ministries',
      'Chord chart and lyrics for ' + song.title + (song.key ? ' (key of ' + song.key + ')' : '') + '. Free worship leader resource from USMC Ministries.',
      'worship/' + song.slug + '.html', 1)}
    <style>${BASE_CSS}${SONG_CSS}</style>
</head>
<body>
    ${navBlock(1)}
    <div class="container">
        <div class="crumb"><a href="../worship.html">&larr; Worship Directory</a></div>
        <div class="song-head">
            <h1>${escapeHtml(song.title)}</h1>
            ${song.key ? `<span class="badge" id="keyBadge">Key: ${escapeHtml(song.key)}</span>` : ''}
        </div>
        <div class="sub">${subBits.join(' &middot; ')}</div>
${media}
        <div class="toolbar">
            <div class="tb-group"><span class="tb-label">Transpose</span>
                <button class="tb-btn" onclick="transpose(-1)" title="Down a half step">&minus;</button>
                <span class="tb-readout" id="semiReadout">0</span>
                <button class="tb-btn" onclick="transpose(1)" title="Up a half step">+</button>
                <button class="tb-btn" onclick="resetTranspose()" title="Reset">↺</button>
            </div>
            <div class="tb-group"><span class="tb-label">Size</span>
                <button class="tb-btn" onclick="fontStep(-1)">A&minus;</button>
                <button class="tb-btn" onclick="fontStep(1)">A+</button>
            </div>
            <div class="tb-group">
                <button class="tb-btn" id="chordsBtn" onclick="toggleChords()">Chords: On</button>
                <button class="tb-btn" onclick="window.print()" title="Print a clean chart, just like the directory">🖨 Print Chart</button>
            </div>
        </div>
        <pre class="chart" id="chart">${renderChart(song.body)}</pre>
        <div class="dl-row">
            ${slides}
            ${ytBtn}
            ${ugBtn}
            <a class="dl-btn" href="../worship.html#random" onclick="event.preventDefault();location.href='../worship.html?random=1'">🎲 Random song</a>
        </div>
        ${!yt ? '<!-- No video linked yet. Add { "'+song.slug+'": { "youtube": "<id>" } } to docs/data/worship-overrides.json and re-run the generator. -->' : ''}
    </div>
    ${footerBlock(1)}
    ${THEME_RESTORE}
    <script>
    /* ── chord chart controls: transpose / font size / show-hide chords ── */
    var SHARP=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];
    var FLAT ={'Db':'C#','Eb':'D#','Gb':'F#','Ab':'G#','Bb':'A#'};
    var semi=0, fontPx=15, chordsOn=true;
    var chart=document.getElementById('chart');
    function shiftRoot(root,n){
      var norm = FLAT[root] || root;
      var i = SHARP.indexOf(norm);
      if(i<0) return root;
      return SHARP[((i+n)%12+12)%12];
    }
    var CHORD_TOK=/^[\\(\\[]?([A-G][#b]?)((?:maj|min|m|sus|aug|dim|add|M)?\\d{0,2}(?:[#b]?\\d{1,2})?(?:sus|add|maj|min|dim|aug)?\\d{0,2})(\\/[A-G][#b]?)?([\\)\\],]?)$/;
    function transposeChord(tok,n){
      var m=tok.match(CHORD_TOK); if(!m) return tok;
      var lead=tok.charAt(0)==='('||tok.charAt(0)==='['?tok.charAt(0):'';
      var root=shiftRoot(m[1],n);
      var bass=m[3]?'/'+shiftRoot(m[3].slice(1),n):'';
      return lead+root+m[2]+bass+m[4];
    }
    function transposeLine(line,n){
      var parts=line.match(/(\\s+|\\S+)/g)||[];
      var out='';
      for(var i=0;i<parts.length;i++){
        var p=parts[i];
        if(/^\\s+$/.test(p)){ out+=p; continue; }
        if(CHORD_TOK.test(p)){
          var t=transposeChord(p,n), diff=t.length-p.length;
          out+=t;
          if(diff!==0 && i+1<parts.length && /^\\s+$/.test(parts[i+1])){
            var ws=parts[i+1];
            parts[i+1]= diff>0 ? (ws.length-diff>=1?ws.slice(0,ws.length-diff):' ')
                               : ws+Array(-diff+1).join(' ');
          }
        } else out+=p;
      }
      return out;
    }
    function applyTranspose(){
      var lines=chart.querySelectorAll('.ln-chord');
      for(var i=0;i<lines.length;i++){
        var orig=lines[i].getAttribute('data-orig');
        lines[i].firstChild ? null : null;
        lines[i].textContent = (semi===0?orig:transposeLine(orig,semi))+'\\n';
      }
      document.getElementById('semiReadout').textContent=(semi>0?'+':'')+semi;
      var kb=document.getElementById('keyBadge');
      if(kb && kb.dataset.basekey===undefined) kb.dataset.basekey=kb.textContent.replace('Key: ','');
      if(kb){ var bk=kb.dataset.basekey.match(/^[A-G][#b]?/);
        if(bk){ kb.textContent='Key: '+shiftRoot(FLAT[bk[0]]||bk[0],semi)+kb.dataset.basekey.slice(bk[0].length); } }
    }
    function transpose(d){ semi=((semi+d)%12); applyTranspose(); }
    function resetTranspose(){ semi=0; applyTranspose(); }
    function fontStep(d){ fontPx=Math.max(10,Math.min(28,fontPx+d)); chart.style.fontSize=fontPx+'px'; }
    function toggleChords(){ chordsOn=!chordsOn; chart.classList.toggle('hide-chords',!chordsOn);
      document.getElementById('chordsBtn').textContent='Chords: '+(chordsOn?'On':'Off'); }
    </script>
</body>
</html>`;
}

/* ───────────────────────────── index page ───────────────────────────── */

const INDEX_CSS = `
        .hero { text-align:center; padding:42px 20px 20px; }
        .hero img { display:block; margin:0 auto 14px; }
        .hero h1 { font-size:clamp(1.8rem,4vw,2.5rem); color:var(--white); margin-bottom:10px; }
        body.light-mode .hero h1 { color:#1a1a1a; }
        .hero p { color:var(--gray); max-width:620px; margin:0 auto; font-size:.96rem; }
        .stat { color:var(--gold); font-weight:600; }
        .sotd { background:linear-gradient(135deg,rgba(212,175,55,.08),rgba(212,175,55,.02)); border:1px solid rgba(212,175,55,.25); border-radius:14px; padding:16px 22px; margin:18px auto 0; max-width:560px; text-align:center; }
        .sotd .lbl { color:var(--gold); font-size:.7rem; text-transform:uppercase; letter-spacing:1.5px; }
        .sotd a.sotd-title { color:var(--white); text-decoration:none; font-family:'Playfair Display',serif; font-size:1.5rem; display:block; margin:5px 0 3px; }
        .sotd a.sotd-title:hover { color:var(--gold); }
        body.light-mode .sotd a.sotd-title { color:#1a1a1a; }
        .sotd .meta { color:var(--gray); font-size:.82rem; }
        .search-box { position:relative; max-width:560px; margin:18px auto 6px; }
        .search-box input { width:100%; padding:13px 132px 13px 44px; background:var(--bg-card); border:1px solid var(--border); border-radius:30px; color:var(--white); font-size:1rem; font-family:'Inter',sans-serif; }
        .random-btn { position:absolute; right:6px; top:50%; transform:translateY(-50%); background:var(--gold); color:#000; border:none; border-radius:24px; padding:9px 16px; font-size:.8rem; font-weight:700; cursor:pointer; display:inline-flex; align-items:center; gap:5px; font-family:'Inter',sans-serif; transition:background .15s; }
        .random-btn:hover { background:var(--gold-light); }
        .search-box input:focus { outline:none; border-color:var(--gold); }
        body.light-mode .search-box input { background:#fff; color:#1a1a1a; border-color:#d4d0c8; }
        .search-icon { position:absolute; left:16px; top:50%; transform:translateY(-50%); color:var(--gray); }
        .chips { display:flex; flex-wrap:wrap; gap:6px; justify-content:center; margin:14px 0 6px; }
        .chip { background:transparent; color:var(--gray); border:1px solid var(--border); border-radius:20px; padding:5px 14px; font-size:.82rem; font-weight:600; cursor:pointer; transition:all .15s; font-family:'Inter',sans-serif; }
        .chip:hover { border-color:var(--gold); color:var(--gold); }
        .chip.active { background:var(--gold); color:#000; border-color:var(--gold); }
        .alpha-bar { display:flex; flex-wrap:wrap; gap:4px; justify-content:center; padding:8px 10px 0; }
        .alpha-btn { min-width:30px; background:transparent; border:1px solid var(--border); border-radius:7px; padding:5px 0; color:var(--gold-light); font-size:.85rem; font-weight:600; cursor:pointer; transition:all .15s; font-family:'Inter',sans-serif; }
        .alpha-btn:hover { border-color:var(--gold); }
        .alpha-btn.active { background:rgba(212,175,55,.18); border-color:var(--gold); }
        .alpha-btn.disabled { opacity:.25; pointer-events:none; }
        .count { text-align:center; color:var(--gray); font-size:.82rem; margin:16px 0 8px; }
        .song-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); gap:10px; margin-bottom:30px; }
        .song-card { display:flex; justify-content:space-between; align-items:center; gap:8px; background:var(--bg-card); border:1px solid var(--border); border-radius:10px; padding:12px 14px; text-decoration:none; transition:all .18s; }
        .song-card:hover { border-color:var(--gold); transform:translateY(-2px); box-shadow:0 0 15px rgba(212,175,55,.1); }
        body.light-mode .song-card { background:#fff; border-color:#d4d0c8; }
        .song-title { color:var(--white); font-weight:500; font-size:.93rem; line-height:1.3; }
        body.light-mode .song-title { color:#1a1a1a; }
        .song-meta { display:flex; gap:6px; align-items:center; flex-shrink:0; }
        .song-key { background:rgba(212,175,55,.15); color:var(--gold); font-size:.68rem; font-weight:600; padding:2px 7px; border-radius:9px; }
        .song-tag { font-size:.58rem; text-transform:uppercase; letter-spacing:.5px; color:var(--gray); border:1px solid var(--border); border-radius:6px; padding:1px 5px; }
        .more { text-align:center; margin:6px 0 30px; }
        .more button { background:transparent; color:var(--gold); border:1px solid var(--gold); border-radius:20px; padding:8px 22px; font-size:.85rem; font-weight:600; cursor:pointer; }
        .more button:hover { background:rgba(212,175,55,.12); }
        .no-results { text-align:center; color:var(--gray); padding:40px 20px; display:none; }`;

function indexPage(songs) {
  const total = songs.length;
  const praise = songs.filter(s => s.type === 'praise' && !s.christmas).length;
  const tabs = songs.filter(s => s.type === 'tab').length;
  const xmas = songs.filter(s => s.christmas).length;
  // Lightweight client index: [slug, title, type(p/t), christmas(0/1), letter, key]
  const idx = songs.map(s => [s.slug, s.title, s.type === 'tab' ? 't' : 'p', s.christmas ? 1 : 0, s.letter, s.key || '']);

  return `${pageHead('Worship — Chords & Lyrics | USMC Ministries',
      'A searchable library of ' + total + ' worship songs with chords charted over the lyrics — the ultimate worship leader resource. Praise & worship, guitar tabs, and Christmas songs.',
      'worship.html', 0)}
    <style>${BASE_CSS}${INDEX_CSS}</style>
</head>
<body>
    ${navBlock(0)}
    <div class="hero">
        <img src="assets/icons/shield-quill-note-96.png" alt="Worship" width="84" height="84">
        <h1>Worship Songbook</h1>
        <p>Chords charted right over the words — the way they should be. <span class="stat">${total}</span> songs from decades of leading worship: <span class="stat">${praise}</span> praise &amp; worship, <span class="stat">${tabs}</span> guitar tabs, <span class="stat">${xmas}</span> Christmas. Transpose to any key, hide the chords, print a clean sheet.</p>
    </div>
    <div class="container">
        <div class="sotd" id="sotd"></div>
        <div class="search-box">
            <span class="search-icon">🔍</span>
            <input type="search" id="q" placeholder="Search ${total} songs by title…" autocomplete="off">
            <button class="random-btn" onclick="randomSong()" title="Open a random song"><img src="assets/icons/shield-die-48.png" width="15" height="15" alt="" style="vertical-align:-2px"> Random</button>
        </div>
        <div class="chips" id="chips">
            <button class="chip active" data-f="all">All</button>
            <button class="chip" data-f="p">Praise &amp; Worship</button>
            <button class="chip" data-f="t">Guitar Tabs</button>
            <button class="chip" data-f="x">Christmas</button>
        </div>
        <div class="alpha-bar" id="alpha"></div>
        <div class="count" id="count"></div>
        <div class="song-grid" id="grid"></div>
        <div class="more" id="more" style="display:none;"><button onclick="showMore()">Show more songs</button></div>
        <div class="no-results" id="noResults">No songs match your search. Try a different word.</div>
    </div>
    ${footerBlock(0)}
    ${THEME_RESTORE}
    <script>
    var SONGS=${JSON.stringify(idx)};
    var PAGE=120, shown=PAGE, filter='all', letter='', term='';
    var grid=document.getElementById('grid'), countEl=document.getElementById('count'),
        moreEl=document.getElementById('more'), nr=document.getElementById('noResults');
    function matches(s){
      if(filter==='p' && (s[2]!=='p'||s[3])) return false;
      if(filter==='t' && s[2]!=='t') return false;
      if(filter==='x' && !s[3]) return false;
      if(letter && s[4]!==letter) return false;
      if(term && s[1].toLowerCase().indexOf(term)<0) return false;
      return true;
    }
    function tagFor(s){ return s[3]?'Xmas':(s[2]==='t'?'Tab':'Praise'); }
    function render(){
      var list=SONGS.filter(matches);
      countEl.textContent=list.length+' song'+(list.length===1?'':'s');
      nr.style.display=list.length?'none':'block';
      var slice=list.slice(0,shown), html='';
      for(var i=0;i<slice.length;i++){ var s=slice[i];
        html+='<a class="song-card" href="worship/'+s[0]+'.html"><span class="song-title">'+
          s[1].replace(/&/g,'&amp;').replace(/</g,'&lt;')+'</span><span class="song-meta">'+
          (s[5]?'<span class="song-key">'+s[5]+'</span>':'')+
          '<span class="song-tag">'+tagFor(s)+'</span></span></a>';
      }
      grid.innerHTML=html;
      moreEl.style.display=list.length>shown?'block':'none';
    }
    function showMore(){ shown+=PAGE; render(); }
    function setFilter(f){ filter=f; shown=PAGE; render();
      var c=document.getElementById('chips').children;
      for(var i=0;i<c.length;i++) c[i].classList.toggle('active',c[i].dataset.f===f); }
    document.getElementById('chips').addEventListener('click',function(e){
      if(e.target.dataset.f) setFilter(e.target.dataset.f); });
    document.getElementById('q').addEventListener('input',function(e){
      term=e.target.value.toLowerCase().trim(); shown=PAGE; render(); });
    // Alpha bar
    (function(){
      var present={}; for(var i=0;i<SONGS.length;i++) present[SONGS[i][4]]=1;
      var letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split(''); if(present['#']) letters.push('#');
      var bar=document.getElementById('alpha'), html='<button class="alpha-btn active" data-l="">All</button>';
      for(var j=0;j<letters.length;j++){ var L=letters[j];
        html+='<button class="alpha-btn'+(present[L]?'':' disabled')+'" data-l="'+L+'">'+L+'</button>'; }
      bar.innerHTML=html;
      bar.addEventListener('click',function(e){ if(e.target.dataset.l===undefined) return;
        letter=e.target.dataset.l; shown=PAGE;
        var b=bar.children; for(var k=0;k<b.length;k++) b[k].classList.toggle('active',b[k].dataset.l===letter);
        render(); });
    })();
    render();
    // Random song (also reachable via ?random=1 from a song page)
    function randomSong(){ var s=SONGS[Math.floor(Math.random()*SONGS.length)]; location.href='worship/'+s[0]+'.html'; }
    if(/[?&]random=1/.test(location.search)) randomSong();
    // Song of the Day — deterministic per calendar day, prefers a song with a key.
    (function(){
      var day=Math.floor(Date.now()/86400000);
      var keyed=SONGS.filter(function(s){return s[5];}); var pool=keyed.length?keyed:SONGS;
      var s=pool[day%pool.length];
      var tag=s[3]?'Christmas':(s[2]==='t'?'Guitar Tab':'Praise & Worship');
      document.getElementById('sotd').innerHTML='<div class="lbl">🎵 Song of the Day</div>'+
        '<a class="sotd-title" href="worship/'+s[0]+'.html">'+s[1].replace(/&/g,'&amp;').replace(/</g,'&lt;')+'</a>'+
        '<div class="meta">'+(s[5]?'Key of '+s[5]+' &middot; ':'')+tag+'</div>';
    })();
    </script>
</body>
</html>`;
}

/* ───────────────────────────── build phase ───────────────────────────── */

function applyOverrides(songs) {
  if (!fs.existsSync(OVERRIDES_JSON)) return 0;
  let ov;
  try { ov = JSON.parse(fs.readFileSync(OVERRIDES_JSON, 'utf8')); }
  catch (e) { console.warn('!! overrides JSON unreadable: ' + e.message); return 0; }
  let n = 0;
  for (const s of songs) {
    const o = ov[s.slug];
    if (!o) continue;
    if (o.youtube) { s.youtube = o.youtube; n++; }
    if (o.slides)  { s.slides = o.slides; }
    if (o.key)     { s.key = o.key; }
  }
  return n;
}

function build(songs) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const enriched = applyOverrides(songs);
  // Prune stale song pages from prior runs (e.g. renamed slugs).
  const keep = new Set(songs.map(s => s.slug + '.html'));
  let pruned = 0;
  for (const f of fs.readdirSync(OUT_DIR)) {
    if (f.endsWith('.html') && !keep.has(f)) { fs.unlinkSync(path.join(OUT_DIR, f)); pruned++; }
  }
  if (pruned) console.log(`Pruned ${pruned} stale song pages.`);
  let written = 0;
  for (const song of songs) {
    fs.writeFileSync(path.join(OUT_DIR, song.slug + '.html'), songPage(song));
    written++;
  }
  fs.writeFileSync(INDEX_HTML, indexPage(songs));
  writeSitemap(songs);
  console.log(`Built ${written} song pages + worship.html (${enriched} with video/slides).`);
}

function writeSitemap(songs) {
  const url = (loc, pri) => `  <url>\n    <loc>https://usmcmin.org/${loc}</loc>\n    <lastmod>${BUILD_DATE}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>${pri}</priority>\n  </url>`;
  const body = [url('worship.html', '0.8')]
    .concat(songs.map(s => url('worship/' + s.slug + '.html', '0.5')))
    .join('\n');
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`;
  fs.writeFileSync(path.join(REPO, 'docs/sitemap-worship.xml'), xml);
}

/* ───────────────────────────────── main ───────────────────────────────── */

(function main() {
  let songs;
  if (PAGES_ONLY && fs.existsSync(DATA_JSON)) {
    songs = JSON.parse(fs.readFileSync(DATA_JSON, 'utf8'));
    console.log(`Loaded ${songs.length} songs from JSON.`);
  } else if (FORCE_INGEST || !fs.existsSync(DATA_JSON)) {
    songs = ingest();
  } else {
    songs = JSON.parse(fs.readFileSync(DATA_JSON, 'utf8'));
    console.log(`Loaded ${songs.length} songs from existing JSON (use --ingest to rebuild).`);
  }
  build(songs);
  console.log('Done.');
})();
