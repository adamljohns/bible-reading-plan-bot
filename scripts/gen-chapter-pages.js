#!/usr/bin/env node
/**
 * Phase 5: Per-chapter static HTML pages for the Preacher John subagent
 * and other AI consumers.
 *
 * Reads:
 *   docs/assets/moop-translation.json      (MBT primary, 99.5% coverage)
 *   docs/assets/verse-chunks/book-N.json   (NKJV fallback, 100% coverage)
 *
 * Emits:
 *   docs/chapters/<abbrev>-<chapter>.html  (1,189 files, one per chapter)
 *   docs/chapters/index.html               (sitemap for human + agent discovery)
 *
 * Page characteristics:
 *   - Single semantic <article> with chapter, book, and book-id data attrs
 *   - <ol class="verses"> with <li data-verse="N" id="vN"> per verse
 *   - <meta name="robots" content="noindex,nofollow"> — intentionally NOT in
 *     the public sitemap. Internal agent surface, not for SEO.
 *   - <link rel="canonical" href="bible.html?ref=…"> points humans who land
 *     here back to the interactive engine.
 *   - Minimal inline CSS — readable in any browser, no JS, no external deps.
 *
 * Run:  node scripts/gen-chapter-pages.js
 */

const fs = require('fs');
const path = require('path');

const REPO_ROOT = path.resolve(__dirname, '..');
const MOOP_PATH = path.join(REPO_ROOT, 'docs/assets/moop-translation.json');
const CHUNKS_DIR = path.join(REPO_ROOT, 'docs/assets/verse-chunks');
const OUT_DIR = path.join(REPO_ROOT, 'docs/chapters');

// 66-book canon ordering with display name, 3-letter SBL-ish abbreviation, and
// chapter count. Abbreviations are URL-safe lowercase, distinct, stable.
const BOOKS = [
    { id:  1, name: 'Genesis',         abbr: 'gen', chapters: 50 },
    { id:  2, name: 'Exodus',          abbr: 'exo', chapters: 40 },
    { id:  3, name: 'Leviticus',       abbr: 'lev', chapters: 27 },
    { id:  4, name: 'Numbers',         abbr: 'num', chapters: 36 },
    { id:  5, name: 'Deuteronomy',     abbr: 'deu', chapters: 34 },
    { id:  6, name: 'Joshua',          abbr: 'jos', chapters: 24 },
    { id:  7, name: 'Judges',          abbr: 'jdg', chapters: 21 },
    { id:  8, name: 'Ruth',            abbr: 'rut', chapters:  4 },
    { id:  9, name: '1 Samuel',        abbr: '1sa', chapters: 31 },
    { id: 10, name: '2 Samuel',        abbr: '2sa', chapters: 24 },
    { id: 11, name: '1 Kings',         abbr: '1ki', chapters: 22 },
    { id: 12, name: '2 Kings',         abbr: '2ki', chapters: 25 },
    { id: 13, name: '1 Chronicles',    abbr: '1ch', chapters: 29 },
    { id: 14, name: '2 Chronicles',    abbr: '2ch', chapters: 36 },
    { id: 15, name: 'Ezra',            abbr: 'ezr', chapters: 10 },
    { id: 16, name: 'Nehemiah',        abbr: 'neh', chapters: 13 },
    { id: 17, name: 'Esther',          abbr: 'est', chapters: 10 },
    { id: 18, name: 'Job',             abbr: 'job', chapters: 42 },
    { id: 19, name: 'Psalms',          abbr: 'psa', chapters: 150 },
    { id: 20, name: 'Proverbs',        abbr: 'pro', chapters: 31 },
    { id: 21, name: 'Ecclesiastes',    abbr: 'ecc', chapters: 12 },
    { id: 22, name: 'Song of Solomon', abbr: 'sng', chapters:  8 },
    { id: 23, name: 'Isaiah',          abbr: 'isa', chapters: 66 },
    { id: 24, name: 'Jeremiah',        abbr: 'jer', chapters: 52 },
    { id: 25, name: 'Lamentations',    abbr: 'lam', chapters:  5 },
    { id: 26, name: 'Ezekiel',         abbr: 'eze', chapters: 48 },
    { id: 27, name: 'Daniel',          abbr: 'dan', chapters: 12 },
    { id: 28, name: 'Hosea',           abbr: 'hos', chapters: 14 },
    { id: 29, name: 'Joel',            abbr: 'joe', chapters:  3 },
    { id: 30, name: 'Amos',            abbr: 'amo', chapters:  9 },
    { id: 31, name: 'Obadiah',         abbr: 'oba', chapters:  1 },
    { id: 32, name: 'Jonah',           abbr: 'jon', chapters:  4 },
    { id: 33, name: 'Micah',           abbr: 'mic', chapters:  7 },
    { id: 34, name: 'Nahum',           abbr: 'nah', chapters:  3 },
    { id: 35, name: 'Habakkuk',        abbr: 'hab', chapters:  3 },
    { id: 36, name: 'Zephaniah',       abbr: 'zep', chapters:  3 },
    { id: 37, name: 'Haggai',          abbr: 'hag', chapters:  2 },
    { id: 38, name: 'Zechariah',       abbr: 'zec', chapters: 14 },
    { id: 39, name: 'Malachi',         abbr: 'mal', chapters:  4 },
    { id: 40, name: 'Matthew',         abbr: 'mat', chapters: 28 },
    { id: 41, name: 'Mark',            abbr: 'mar', chapters: 16 },
    { id: 42, name: 'Luke',            abbr: 'luk', chapters: 24 },
    { id: 43, name: 'John',            abbr: 'joh', chapters: 21 },
    { id: 44, name: 'Acts',            abbr: 'act', chapters: 28 },
    { id: 45, name: 'Romans',          abbr: 'rom', chapters: 16 },
    { id: 46, name: '1 Corinthians',   abbr: '1co', chapters: 16 },
    { id: 47, name: '2 Corinthians',   abbr: '2co', chapters: 13 },
    { id: 48, name: 'Galatians',       abbr: 'gal', chapters:  6 },
    { id: 49, name: 'Ephesians',       abbr: 'eph', chapters:  6 },
    { id: 50, name: 'Philippians',     abbr: 'php', chapters:  4 },
    { id: 51, name: 'Colossians',      abbr: 'col', chapters:  4 },
    { id: 52, name: '1 Thessalonians', abbr: '1th', chapters:  5 },
    { id: 53, name: '2 Thessalonians', abbr: '2th', chapters:  3 },
    { id: 54, name: '1 Timothy',       abbr: '1ti', chapters:  6 },
    { id: 55, name: '2 Timothy',       abbr: '2ti', chapters:  4 },
    { id: 56, name: 'Titus',           abbr: 'tit', chapters:  3 },
    { id: 57, name: 'Philemon',        abbr: 'phm', chapters:  1 },
    { id: 58, name: 'Hebrews',         abbr: 'heb', chapters: 13 },
    { id: 59, name: 'James',           abbr: 'jas', chapters:  5 },
    { id: 60, name: '1 Peter',         abbr: '1pe', chapters:  5 },
    { id: 61, name: '2 Peter',         abbr: '2pe', chapters:  3 },
    { id: 62, name: '1 John',          abbr: '1jn', chapters:  5 },
    { id: 63, name: '2 John',          abbr: '2jn', chapters:  1 },
    { id: 64, name: '3 John',          abbr: '3jn', chapters:  1 },
    { id: 65, name: 'Jude',            abbr: 'jud', chapters:  1 },
    { id: 66, name: 'Revelation',      abbr: 'rev', chapters: 22 },
];

// Strip Strong's tags + other inline markup that NKJV cache preserves raw.
// Mirror docs/bible.html's cleanVerseText (simplified — agents don't need <i>).
function clean(text) {
    if (!text) return '';
    return String(text)
        .replace(/<sup>[^<]*<\/sup>/gi, '')
        .replace(/<S>\d+<\/S>/gi, '')
        .replace(/<s>[^<]*<\/s>/gi, '')
        .replace(/<strike>[^<]*<\/strike>/gi, '')
        .replace(/[̶]/g, '')
        .replace(/<br\s*\/?>/gi, ' ')
        .replace(/<[^>]+>/g, '')          // strip remaining tags (including <i>, <em>)
        .replace(/[Ⓐ-⓿①-⑳]/g, '')
        .replace(/\s*\[[a-z]\]/g, '')
        .replace(/\s*\([a-z]\)/g, '')
        .replace(/\[\d+\]/g, '')
        .replace(/(\w) [a-c](?= [A-Z])/g, '$1')
        .replace(/([a-zA-Z])(\d{2,5})(?=[\s,;:.!?'")\-]|$)/g, '$1')
        .replace(/\s*[;:]\s*(Heb\.|Gr\.|or,|that is,)[^;:.]*(?=[;:.]|$)/g, '')
        .replace(/([,;:.!?])([A-Za-z])/g, '$1 $2')
        .replace(/\s{2,}/g, ' ')
        .trim();
}

function escapeHtml(s) {
    return String(s)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function renderChapterPage(book, ch, verses, prev, next) {
    const title = `${book.name} ${ch}`;
    const refQuery = encodeURIComponent(`${book.name} ${ch}`);
    const verseList = verses.map(v => {
        const src = v.source === 'mbt' ? '' : ` data-source="${v.source}"`;
        return `      <li data-verse="${v.n}" id="v${v.n}"${src}>${escapeHtml(v.text)}</li>`;
    }).join('\n');

    const prevLink = prev ? `<a rel="prev" href="${prev.abbr}-${prev.ch}.html">← ${prev.name} ${prev.ch}</a>` : '<span></span>';
    const nextLink = next ? `<a rel="next" href="${next.abbr}-${next.ch}.html">${next.name} ${next.ch} →</a>` : '<span></span>';

    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>${title} — MOOP Bible</title>
  <meta name="robots" content="noindex,nofollow">
  <meta name="description" content="${title} — MBT primary text with NKJV fallback. Internal Bible Translation Engine surface.">
  <link rel="canonical" href="../bible.html?ref=${refQuery}">
  <link rel="prev" href="${prev ? prev.abbr + '-' + prev.ch + '.html' : '#'}">
  <link rel="next" href="${next ? next.abbr + '-' + next.ch + '.html' : '#'}">
  <style>
    body{font-family:Georgia,serif;max-width:42rem;margin:2rem auto;padding:0 1rem;color:#222;line-height:1.6;background:#fafafa}
    h1{font-size:1.4rem;margin:0 0 1rem}
    h1 small{font-size:.7rem;color:#888;font-weight:normal;display:block;margin-top:.15rem}
    ol.verses{list-style:none;padding:0;margin:0;counter-reset:verse}
    ol.verses li{padding:.2rem 0;text-indent:-2rem;padding-left:2rem}
    ol.verses li::before{content:attr(data-verse);display:inline-block;width:1.6rem;color:#aaa;font-size:.75rem;vertical-align:.25em;font-family:Inter,system-ui,sans-serif}
    ol.verses li[data-source="nkjv"]{color:#444}
    ol.verses li[data-source="nkjv"]::after{content:" [NKJV]";color:#bbb;font-size:.7rem;vertical-align:.25em}
    nav.chapnav{display:flex;justify-content:space-between;margin-top:2rem;font-size:.85rem;color:#888;border-top:1px solid #ddd;padding-top:1rem}
    nav.chapnav a{color:#444;text-decoration:none}
    nav.chapnav a:hover{text-decoration:underline}
    footer{margin-top:1.5rem;font-size:.7rem;color:#bbb;text-align:center}
    footer a{color:#888}
  </style>
</head>
<body>
  <article data-book-id="${book.id}" data-book="${book.name}" data-abbr="${book.abbr}" data-chapter="${ch}" data-verse-count="${verses.length}">
    <h1>${title}<small>Book ${book.id} of 66 · ${verses.length} verses · MBT primary, NKJV fallback where MBT pending</small></h1>
    <ol class="verses">
${verseList}
    </ol>
    <nav class="chapnav">
      ${prevLink}
      <a href="index.html">All chapters</a>
      ${nextLink}
    </nav>
  </article>
  <footer>
    Static chapter surface for AI consumers. Interactive: <a href="../bible.html?ref=${refQuery}">bible.html</a>.<br>
    Generated by scripts/gen-chapter-pages.js · MOOP Bible Translation Engine
  </footer>
</body>
</html>
`;
}

function renderIndex(allChapters, writtenSet) {
    const rows = BOOKS.map(b => {
        const chapterLinks = [];
        let missing = 0;
        for (let ch = 1; ch <= b.chapters; ch++) {
            const file = `${b.abbr}-${ch}.html`;
            if (writtenSet.has(file)) {
                chapterLinks.push(`<a href="${file}">${ch}</a>`);
            } else {
                chapterLinks.push(`<span class="missing" title="not generated — source data gap">${ch}</span>`);
                missing++;
            }
        }
        const note = missing > 0 ? ` <span class="gap-note">— ${missing} chapter${missing > 1 ? 's' : ''} pending translation</span>` : '';
        return `      <tr>
        <th scope="row">${b.id}. ${b.name} <code>(${b.abbr})</code>${note}</th>
        <td>${chapterLinks.join(' ')}</td>
      </tr>`;
    }).join('\n');

    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Chapter Index — MOOP Bible</title>
  <meta name="robots" content="noindex,nofollow">
  <meta name="description" content="Static per-chapter index for the Bible Translation Engine. Internal surface for AI consumers and direct chapter access.">
  <link rel="canonical" href="../bible.html">
  <style>
    body{font-family:Georgia,serif;max-width:60rem;margin:2rem auto;padding:0 1rem;color:#222;background:#fafafa}
    h1{font-size:1.4rem;margin:0 0 .3rem}
    p.lead{color:#666;font-size:.9rem;margin:0 0 1.5rem}
    table{width:100%;border-collapse:collapse;font-size:.85rem}
    th,td{text-align:left;vertical-align:top;padding:.4rem .6rem;border-bottom:1px solid #eee}
    th{font-weight:600;font-family:Inter,system-ui,sans-serif;width:14rem}
    th code{color:#888;font-size:.75rem;font-weight:normal}
    td a{color:#444;text-decoration:none;display:inline-block;margin-right:.4rem;font-family:Inter,system-ui,sans-serif;font-size:.78rem}
    td a:hover{text-decoration:underline;color:#000}
    td .missing{display:inline-block;margin-right:.4rem;color:#ccc;font-family:Inter,system-ui,sans-serif;font-size:.78rem;text-decoration:line-through;cursor:help}
    .gap-note{font-weight:400;color:#b58b00;font-size:.75rem;margin-left:.4rem}
    footer{margin-top:2rem;font-size:.7rem;color:#bbb;text-align:center}
    footer a{color:#888}
  </style>
</head>
<body>
  <h1>Chapter Index</h1>
  <p class="lead">Static per-chapter pages — primarily for AI agents fetching scripture deterministically. ${allChapters} chapters total across 66 books. Click any chapter number to read.</p>
  <table>
    <thead><tr><th>Book</th><th>Chapters</th></tr></thead>
    <tbody>
${rows}
    </tbody>
  </table>
  <footer>
    Interactive Bible Translation Engine: <a href="../bible.html">bible.html</a><br>
    Generated by scripts/gen-chapter-pages.js
  </footer>
</body>
</html>
`;
}

// --- main ---
function main() {
    if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

    console.log('Loading moop-translation.json…');
    const mbt = JSON.parse(fs.readFileSync(MOOP_PATH, 'utf8'));

    let chaptersWritten = 0;
    let totalVerses = 0;
    let mbtVerses = 0;
    let nkjvFallback = 0;
    let missingVerses = 0;

    // Pre-compute prev/next for cross-chapter navigation
    function nav(bookIdx, ch) {
        const book = BOOKS[bookIdx];
        let prev = null, next = null;
        if (ch > 1) {
            prev = { abbr: book.abbr, ch: ch - 1, name: book.name };
        } else if (bookIdx > 0) {
            const pb = BOOKS[bookIdx - 1];
            prev = { abbr: pb.abbr, ch: pb.chapters, name: pb.name };
        }
        if (ch < book.chapters) {
            next = { abbr: book.abbr, ch: ch + 1, name: book.name };
        } else if (bookIdx < BOOKS.length - 1) {
            const nb = BOOKS[bookIdx + 1];
            next = { abbr: nb.abbr, ch: 1, name: nb.name };
        }
        return [prev, next];
    }

    for (let i = 0; i < BOOKS.length; i++) {
        const book = BOOKS[i];
        const chunkPath = path.join(CHUNKS_DIR, `book-${book.id}.json`);
        let chunk = {};
        try {
            chunk = JSON.parse(fs.readFileSync(chunkPath, 'utf8'));
        } catch (e) {
            console.warn(`  ! ${book.name} (book-${book.id}.json) missing — NKJV fallback unavailable`);
        }

        for (let ch = 1; ch <= book.chapters; ch++) {
            // Find all verses for this chapter
            const verseNums = new Set();
            for (const k of Object.keys(chunk)) {
                const parts = k.split('_');
                if (parts.length === 3 && parseInt(parts[0], 10) === book.id && parseInt(parts[1], 10) === ch) {
                    verseNums.add(parseInt(parts[2], 10));
                }
            }
            // Also pull any verses present in MBT but missing from chunk (defensive)
            for (const k of Object.keys(mbt)) {
                const parts = k.split('_');
                if (parts.length === 3 && parseInt(parts[0], 10) === book.id && parseInt(parts[1], 10) === ch) {
                    verseNums.add(parseInt(parts[2], 10));
                }
            }

            const sortedVerses = Array.from(verseNums).sort((a, b) => a - b);
            const verses = [];
            for (const vn of sortedVerses) {
                const key = `${book.id}_${ch}_${vn}`;
                let text = null, source = null;
                if (mbt[key]) {
                    text = mbt[key];
                    source = 'mbt';
                    mbtVerses++;
                } else if (chunk[key] && chunk[key].NKJV) {
                    text = clean(chunk[key].NKJV);
                    source = 'nkjv';
                    nkjvFallback++;
                } else {
                    missingVerses++;
                    continue;  // skip verses with no source
                }
                verses.push({ n: vn, text, source });
                totalVerses++;
            }

            if (verses.length === 0) continue;

            const [prev, next] = nav(i, ch);
            const html = renderChapterPage(book, ch, verses, prev, next);
            const outPath = path.join(OUT_DIR, `${book.abbr}-${ch}.html`);
            fs.writeFileSync(outPath, html);
            chaptersWritten++;
        }
        process.stdout.write(`  ${book.name.padEnd(18)} → ${book.chapters} chapters\r`);
    }
    process.stdout.write('\n');

    // Build a set of actually-written files so the index doesn't link to 404s
    const writtenSet = new Set(fs.readdirSync(OUT_DIR).filter(f => f.endsWith('.html') && f !== 'index.html'));
    const indexHtml = renderIndex(chaptersWritten, writtenSet);
    fs.writeFileSync(path.join(OUT_DIR, 'index.html'), indexHtml);

    console.log('\n--- summary ---');
    console.log(`chapters written:  ${chaptersWritten}`);
    console.log(`total verses:      ${totalVerses}`);
    console.log(`  MBT primary:     ${mbtVerses}`);
    console.log(`  NKJV fallback:   ${nkjvFallback}`);
    console.log(`  missing (skip):  ${missingVerses}`);
    console.log(`output dir:        ${OUT_DIR}`);
}

main();
