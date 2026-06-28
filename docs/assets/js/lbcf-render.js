/* LBCF Renderer v1.3 — usmcmin.org
 * v1.3 (2026-06-13): progressive enhancement — when bin/generate-lbcf-pages.js has
 *   baked static content + embedded chapter/index JSON into the shell, render from
 *   that (no network, no flash, offline-proof) after clearing the static fallback;
 *   fall back to fetch when absent. Dropped the unused index.json fetch on chapters.
 * v1.2 (2026-06-12): chapters lifted draft→final after the 32-chapter fidelity
 *   audit; hub counter now counts all non-placeholder chapters.
 * v1.1 (2026-06-12): root-absolute link targets (relative paths 404ed from /lbcf/),
 *   added Exod/Esth/Cant abbreviations, fixed dictionary slugs to existing pages.
 *
 * Loads /assets/lbcf/index.json (chapter metadata) for the index page,
 * and /assets/lbcf/chapter-NN.json for individual chapter pages.
 *
 * Auto-links:
 *   1. Scripture refs ("Hebrews 4:12", "1 Cor 13:1") → bible.html?ref=...
 *   2. Theological terms (covenant, trinity, etc.) → dictionary/<slug>.html
 *   3. Cross-refs to other LBCF chapters ("Chapter 7" mentioned in body) → lbcf/chapter-NN.html
 *
 * Public API (window.LBCF):
 *   - renderIndex(targetEl)        — renders the chapter grid on lbcf.html
 *   - renderChapter(chNum, targetEl) — renders a single chapter page
 *   - linkScripture(text)          — string → string with anchor tags
 *   - linkDictionary(text)         — same, for theological terms
 */

(function () {
  'use strict';

  // ---- 66-book name → numeric ID (matches BTE schema) -----------------
  const BOOK_IDS = {
    'genesis': 1, 'gen': 1,
    'exodus': 2, 'exo': 2, 'ex': 2,
    'leviticus': 3, 'lev': 3,
    'numbers': 4, 'num': 4,
    'deuteronomy': 5, 'deut': 5, 'dt': 5,
    'joshua': 6, 'josh': 6,
    'judges': 7, 'judg': 7,
    'ruth': 8,
    '1 samuel': 9, '1 sam': 9, '1sam': 9,
    '2 samuel': 10, '2 sam': 10, '2sam': 10,
    '1 kings': 11, '1 kgs': 11, '1kgs': 11,
    '2 kings': 12, '2 kgs': 12, '2kgs': 12,
    '1 chronicles': 13, '1 chron': 13, '1 chr': 13,
    '2 chronicles': 14, '2 chron': 14, '2 chr': 14,
    'ezra': 15,
    'nehemiah': 16, 'neh': 16,
    'esther': 17, 'est': 17,
    'job': 18,
    'psalms': 19, 'psalm': 19, 'ps': 19,
    'proverbs': 20, 'prov': 20, 'pr': 20,
    'ecclesiastes': 21, 'eccl': 21, 'ecc': 21,
    'song of solomon': 22, 'song of songs': 22, 'song': 22, 'sos': 22,
    'isaiah': 23, 'isa': 23, 'is': 23,
    'jeremiah': 24, 'jer': 24,
    'lamentations': 25, 'lam': 25,
    'ezekiel': 26, 'ezek': 26, 'eze': 26,
    'daniel': 27, 'dan': 27,
    'hosea': 28, 'hos': 28,
    'joel': 29,
    'amos': 30,
    'obadiah': 31, 'obad': 31,
    'jonah': 32, 'jon': 32,
    'micah': 33, 'mic': 33,
    'nahum': 34, 'nah': 34,
    'habakkuk': 35, 'hab': 35,
    'zephaniah': 36, 'zeph': 36,
    'haggai': 37, 'hag': 37,
    'zechariah': 38, 'zech': 38,
    'malachi': 39, 'mal': 39,
    'matthew': 40, 'matt': 40, 'mt': 40,
    'mark': 41, 'mk': 41,
    'luke': 42, 'lk': 42,
    'john': 43, 'jn': 43,
    'acts': 44,
    'romans': 45, 'rom': 45,
    '1 corinthians': 46, '1 cor': 46, '1cor': 46,
    '2 corinthians': 47, '2 cor': 47, '2cor': 47,
    'galatians': 48, 'gal': 48,
    'ephesians': 49, 'eph': 49,
    'philippians': 50, 'phil': 50, 'php': 50,
    'colossians': 51, 'col': 51,
    '1 thessalonians': 52, '1 thess': 52, '1 th': 52,
    '2 thessalonians': 53, '2 thess': 53, '2 th': 53,
    '1 timothy': 54, '1 tim': 54, '1ti': 54,
    '2 timothy': 55, '2 tim': 55, '2ti': 55,
    'titus': 56, 'tit': 56,
    'philemon': 57, 'philem': 57, 'phlm': 57,
    'hebrews': 58, 'heb': 58,
    'james': 59, 'jas': 59,
    '1 peter': 60, '1 pet': 60, '1pet': 60,
    '2 peter': 61, '2 pet': 61, '2pet': 61,
    '1 john': 62, '1 jn': 62, '1jn': 62,
    '2 john': 63, '2 jn': 63, '2jn': 63,
    '3 john': 64, '3 jn': 64, '3jn': 64,
    'jude': 65,
    'revelation': 66, 'rev': 66,
  };

  // ---- LBCF-relevant dictionary auto-link whitelist -----------------------
  // Each entry: regex pattern (lowercase) → dictionary slug (no extension).
  // The regex MUST match WHOLE words. Order matters — longer phrases first.
  const DICT_TERMS = [
    // Multi-word phrases (longest first)
    ['abrahamic covenant', 'abrahamic-covenant'],
    ['covenant of works', 'covenant-of-works'],
    ['covenant of grace', 'covenant-of-grace'],
    ['covenant of redemption', 'covenant-of-redemption'],
    ['day of atonement', 'atonement-day'],
    ['decree of god', 'decree-of-god'],
    ['effectual calling', 'effectual-calling'],
    ['effectual call', 'effectual-calling'],
    ['eternal decree', 'eternal-decree'],
    ['eternal generation', 'eternal-generation'],
    ['eternal procession', 'eternal-procession'],
    ['extra calvinisticum', 'extra-calvinisticum'],
    ['five solas', 'five-solas'],
    ['hypostatic union', 'hypostatic-union'],
    ['holy spirit', 'holy-spirit'],
    ['holy ghost', 'holy-spirit'],
    ['imputed righteousness', 'imputed-righteousness'],
    ['kingdom of god', 'kingdom-of-god'],
    ['lord’s supper', 'lords-supper'],
    ["lord's supper", 'lords-supper'],
    ['means of grace', 'means-of-grace'],
    ['ordo salutis', 'ordo-salutis'],
    ['original sin', 'original-sin'],
    ['particular atonement', 'definite-atonement'],
    ['definite atonement', 'definite-atonement'],
    ['limited atonement', 'limited-atonement'],
    ['perseverance of the saints', 'perseverance-saints'],
    ['regulative principle', 'regulative-principle'],
    ['second coming', 'second-coming'],
    ['sola scriptura', 'sola-scriptura'],
    ['sola fide', 'sola-fide'],
    ['sola gratia', 'sola-gratia'],
    ['solus christus', 'solus-christus'],
    ['soli deo gloria', 'soli-deo-gloria'],
    ['son of god', 'son-of-god'],
    ['total depravity', 'total-depravity'],
    ['ten commandments', 'ten-commandments'],
    ['the lord jesus christ', 'christ'],
    ['jesus christ', 'christ'],
    ['unconditional election', 'unconditional-election'],
    ['virgin birth', 'virgin-birth'],
    ['westminster confession', 'westminster-confession'],
    // Single-word (common LBCF terms with definite dictionary entries)
    ['adoption', 'adoption'],
    ['arianism', 'arianism'],
    ['ascension', 'ascension'],
    ['aseity', 'aseity'],
    ['assurance', 'assurance'],
    ['atonement', 'atonement'],
    ['baptism', 'baptism-doctrine'],
    ['baptize', 'baptism-doctrine'],
    ['baptized', 'baptism-doctrine'],
    ['canon', 'canon'],
    ['cessationism', 'cessationism'],
    ['christ', 'christ'],
    ['church', 'church'],
    ['communion', 'communion'],
    ['conversion', 'conversion'],
    ['covenant', 'covenant'],
    ['covenants', 'covenant'],
    ['creed', 'creed'],
    ['decree', 'decree-of-god'],
    ['decrees', 'decree-of-god'],
    ['depravity', 'depravity'],
    ['election', 'election'],
    ['eternity', 'eternity'],
    ['faith', 'faith'],
    ['glorification', 'glorification'],
    ['glory', 'glory'],
    ['gospel', 'gospel'],
    ['grace', 'grace'],
    ['holiness', 'holiness'],
    ['immutability', 'immutability'],
    ['impassibility', 'impassibility'],
    ['imputation', 'imputation'],
    ['imputed', 'imputation'],
    ['incarnation', 'incarnation'],
    ['justification', 'justification'],
    ['justified', 'justification'],
    ['kingdom', 'kingdom'],
    ['liberty', 'christian-liberty'],
    ['mediator', 'mediator'],
    ['mercy', 'mercy'],
    ['modalism', 'modalism'],
    ['ordinance', 'ordinance'],
    ['ordinances', 'ordinance'],
    ['pelagianism', 'pelagianism'],
    ['perichoresis', 'perichoresis'],
    ['predestination', 'predestination'],
    ['propitiation', 'propitiation'],
    ['providence', 'providence'],
    ['redemption', 'redemption'],
    ['regeneration', 'regeneration'],
    ['repent', 'repentance'],
    ['repentance', 'repentance'],
    ['reprobation', 'reprobation'],
    ['resurrection', 'resurrection'],
    ['righteousness', 'righteousness'],
    ['sabbath', 'sabbath'],
    ['sacrament', 'sacrament'],
    ['salvation', 'salvation'],
    ['sanctification', 'sanctification'],
    ['sanctified', 'sanctification'],
    ['scripture', 'scripture'],
    ['scriptures', 'scripture'],
    ['sin', 'sin'],
    ['sins', 'sin'],
    ['socinianism', 'socinianism'],
    ['sovereignty', 'sovereignty'],
    ['transubstantiation', 'transubstantiation'],
    ['trinity', 'trinity'],
    ['truth', 'truth'],
    ['worship', 'worship'],
    // Added 2026-06-28 — confessional doctrine terms now defined (live slugs)
    ['mortification', 'mortification'],
    ['image of god', 'image-of-god'],
    ['the moral law', 'moral-law'],
    ['moral law', 'moral-law'],
    ['ceremonial law', 'ceremonial-law'],
    ['excommunication', 'excommunication'],
    ['church discipline', 'church-discipline'],
    ['communion of saints', 'communion-of-saints'],
    ['final judgment', 'final-judgment'],
    ['last judgment', 'final-judgment'],
    ['resurrection of the dead', 'resurrection'],
    ['eternal life', 'eternal-life'],
    ['good works', 'good-works'],
    ['liberty of conscience', 'christian-liberty'],
    ['christian liberty', 'christian-liberty'],
    ['apostasy', 'apostasy'],
    ['antichrist', 'antichrist'],
    ['lawful oath', 'oath'],
    ['effectual grace', 'effectual-calling'],
    ['imputed sin', 'original-sin'],
    ['federal headship', 'federal-headship'],
    ['covenant theology', 'covenant-theology'],
    ['perseverance', 'perseverance-saints'],
  ];

  // Build a single regex of the union for matching. Word boundaries; case-insensitive.
  const _escapeRe = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const DICT_RE = new RegExp(
    '\\b(' + DICT_TERMS.map(([t]) => _escapeRe(t)).join('|') + ')\\b',
    'gi'
  );
  // Build slug lookup
  const _DICT_LOOKUP = Object.fromEntries(DICT_TERMS.map(([t, s]) => [t.toLowerCase(), s]));

  // ---- Scripture-ref auto-link ----------------------------------------------
  // Match patterns like: "John 3:16", "1 Cor 13:1-3", "Hebrews 4:12-13", "Genesis 1"
  const SCRIPTURE_RE = new RegExp(
    '\\b((?:[1-3]\\s)?(?:Genesis|Gen|Exodus|Exod|Exo|Ex|Leviticus|Lev|Numbers|Num|Deuteronomy|Deut|Dt|Joshua|Josh|Judges|Judg|Ruth|Samuel|Sam|Kings|Kgs|Chronicles|Chron|Chr|Ezra|Nehemiah|Neh|Esther|Esth|Est|Job|Psalms?|Ps|Proverbs|Prov|Pr|Ecclesiastes|Eccl|Ecc|Song of Solomon|Song of Songs|Canticles|Cant|Song|SoS|Isaiah|Isa|Is|Jeremiah|Jer|Lamentations|Lam|Ezekiel|Ezek|Eze|Daniel|Dan|Hosea|Hos|Joel|Amos|Obadiah|Obad|Jonah|Jon|Micah|Mic|Nahum|Nah|Habakkuk|Hab|Zephaniah|Zeph|Haggai|Hag|Zechariah|Zech|Malachi|Mal|Matthew|Matt|Mt|Mark|Mk|Luke|Lk|John|Jn|Acts|Romans|Rom|Corinthians|Cor|Galatians|Gal|Ephesians|Eph|Philippians|Phil|Php|Colossians|Col|Thessalonians|Thess|Th|Timothy|Tim|Ti|Titus|Tit|Philemon|Philem|Phlm|Hebrews|Heb|James|Jas|Peter|Pet|John|Jn|Jude|Revelation|Rev))\\s(\\d+)(?::(\\d+(?:[–—-]\\d+)?(?:,\\s*\\d+(?:[–—-]\\d+)?)*))?\\b',
    'g'
  );

  // Abbreviations the BTE ref parser doesn't know — normalize in the URL only
  // (displayed text keeps the prooftext's own abbreviation).
  const URL_BOOK_FIX = {
    'cant': 'Song', 'canticles': 'Song',
    'song of solomon': 'Song', 'song of songs': 'Song',
  };

  // Single-chapter books: a citation like "Jude 4" means verse 4 of the one
  // chapter, not chapter 4. When no explicit verse is present, reinterpret the
  // captured number as a verse so the BTE URL points at "Jude 1:4" (chapter 1).
  // Keyed by every lowercase name/abbrev these books can appear under.
  const SINGLE_CHAPTER = new Set([
    'obadiah', 'obad', 'philemon', 'philem', 'phlm',
    '2 john', '2 jn', '2jn', '3 john', '3 jn', '3jn',
    'jude',
  ]);

  function refToUrl(book, chapter, verses) {
    const fixed = URL_BOOK_FIX[book.toLowerCase()] || book;
    let ch = chapter, vs = verses;
    // Short-form single-chapter ref ("Jude 4" / "Jude 6-7"): number is the verse.
    if (!vs && SINGLE_CHAPTER.has(book.toLowerCase())) {
      vs = ch;
      ch = '1';
    }
    let ref = (fixed + ' ' + ch + (vs ? ':' + vs : '')).trim();
    // Root-absolute: chapter pages live at /lbcf/, so relative URLs 404.
    return '/bible.html?ref=' + encodeURIComponent(ref);
  }

  function linkScripture(html, seen) {
    return html.replace(SCRIPTURE_RE, (m, book, ch, vs) => {
      // Skip if already inside an <a> tag (basic guard — the renderer also segments to avoid double-wrap)
      if (seen) {
        const key = 'scrip:' + (book + ' ' + ch + (vs ? ':' + vs : '')).toLowerCase();
        if (seen.has(key)) return m;
        seen.add(key);
      }
      return '<a class="lbcf-scrip" href="' + refToUrl(book, ch, vs) + '" title="Open in BTE">' + m + '</a>';
    });
  }

  function linkDictionary(html, seen) {
    return html.replace(DICT_RE, (m) => {
      const slug = _DICT_LOOKUP[m.toLowerCase()];
      if (!slug) return m;
      if (seen) {
        const key = 'dict:' + slug;
        if (seen.has(key)) return m;
        seen.add(key);
      }
      return '<a class="lbcf-dict" href="/dictionary/' + slug + '.html" title="Definition">' + m + '</a>';
    });
  }

  // Cross-link "Chapter N" mentions to other LBCF chapters
  function linkChapterRefs(html, currentCh) {
    return html.replace(/\bchapter\s+(\d{1,2})\b/gi, (m, n) => {
      const num = parseInt(n, 10);
      if (num < 1 || num > 32 || num === currentCh) return m;
      const padded = String(num).padStart(2, '0');
      return '<a class="lbcf-xref" href="/lbcf/chapter-' + padded + '.html">' + m + '</a>';
    });
  }

  // Apply auto-linkers in safe order: scripture first (won't match dictionary terms), then dictionary, then chapter xrefs.
  // `seen` is an optional Set used to dedupe links — first occurrence of each term/ref linked, subsequent ones plain.
  function autoLink(text, currentCh, seen) {
    let s = text;
    s = linkScripture(s, seen);
    // Apply dictionary linking ONLY outside existing anchor tags
    s = s.replace(/(<a [^>]*>.*?<\/a>)|([^<]+)/g, (m, anchor, plain) =>
      anchor ? anchor : linkDictionary(plain, seen)
    );
    s = linkChapterRefs(s, currentCh || 0);
    return s;
  }

  // ---- Loaders ---------------------------------------------------------------
  async function loadJson(path) {
    const r = await fetch(path);
    if (!r.ok) throw new Error('Failed to load ' + path + ': ' + r.status);
    return r.json();
  }

  // ---- Render: index page (chapter grid) -----------------------------------
  async function renderIndex(targetEl) {
    // Prefer index.json embedded by the static pre-render; else fetch.
    let meta = null;
    try {
      const embedded = document.getElementById('lbcf-index-data');
      if (embedded && embedded.textContent.trim()) meta = JSON.parse(embedded.textContent);
    } catch (e) { meta = null; }
    if (!meta) meta = await loadJson('assets/lbcf/index.json');
    targetEl.innerHTML = ''; // clear any pre-rendered grid before rebuilding
    const grid = document.createElement('div');
    grid.className = 'lbcf-grid';
    meta.chapters.forEach((c) => {
      const padded = String(c.number).padStart(2, '0');
      const card = document.createElement('a');
      card.className = 'lbcf-card';
      card.href = 'lbcf/chapter-' + padded + '.html';
      // Status chip: placeholder → "Coming soon"; version present → "v<num>"; else fallback to "Draft"
      const status = c.status === 'placeholder'
        ? '<span class="lbcf-card-status placeholder">Coming soon</span>'
        : c.version
          ? '<span class="lbcf-card-status">v' + c.version + '</span>'
          : c.status === 'draft'
            ? '<span class="lbcf-card-status">Draft</span>'
            : '';
      card.innerHTML =
        '<div class="lbcf-card-num">Chapter ' + c.number + '</div>' +
        '<h3>' + c.title + '</h3>' +
        '<p>' + (c.summary || '') + '</p>' +
        status;
      grid.appendChild(card);
    });
    targetEl.appendChild(grid);

    // Wire intro stats
    const totalEl = document.getElementById('lbcf-total-chapters');
    if (totalEl) totalEl.textContent = String(meta.chapters.length);
    const draftedCount = meta.chapters.filter(c => c.status !== 'placeholder').length;
    const draftedEl = document.getElementById('lbcf-drafted-count');
    if (draftedEl) draftedEl.textContent = String(draftedCount);
  }

  // ---- Render: single chapter page -----------------------------------------
  async function renderChapter(chNum, targetEl) {
    const padded = String(chNum).padStart(2, '0');
    // Progressive enhancement: prefer the chapter JSON embedded by the static
    // pre-render (no network, no flash, works offline); fall back to fetch.
    let chapter = null;
    try {
      const embedded = document.getElementById('lbcf-chapter-data');
      if (embedded && embedded.textContent.trim()) {
        const parsed = JSON.parse(embedded.textContent);
        if (Number(parsed.number) === Number(chNum)) chapter = parsed;
      }
      if (!chapter) chapter = await loadJson('../assets/lbcf/chapter-' + padded + '.json');
    } catch (e) {
      targetEl.innerHTML = '<div class="lbcf-empty"><h2>This chapter is not yet drafted.</h2>' +
        '<p>It is part of the scaffolding pass. Body text and proof-texts are coming.</p>' +
        '<p><a href="../lbcf.html">← Back to confession index</a></p></div>';
      return;
    }

    // Replace any static pre-rendered fallback so we never duplicate it.
    targetEl.innerHTML = '';

    // Header
    const head = document.createElement('div');
    head.className = 'lbcf-chap-head';
    head.innerHTML =
      '<div class="lbcf-chap-num">Chapter ' + chapter.number + '</div>' +
      '<h1>' + chapter.title + '</h1>' +
      (chapter.subtitle ? '<p class="lbcf-chap-sub">' + chapter.subtitle + '</p>' : '');
    targetEl.appendChild(head);

    // Paragraphs
    const body = document.createElement('div');
    body.className = 'lbcf-body';
    chapter.paragraphs.forEach((para, idx) => {
      const num = idx + 1;
      const anchorId = 'p' + num;
      const wrap = document.createElement('section');
      wrap.className = 'lbcf-para';
      wrap.id = anchorId;
      // Fresh dedupe Set per paragraph — first occurrence of each scripture ref / dictionary term gets linked, the rest stay plain text.
      const seenInParagraph = new Set();
      const linkedText = autoLink(para.text, chapter.number, seenInParagraph);
      let proofTextHtml = '';
      if (para.prooftexts && para.prooftexts.length) {
        const refs = para.prooftexts.map((r) => linkScripture(r)).join(' &middot; ');
        proofTextHtml = '<details class="lbcf-proofs"><summary>Proof-texts</summary><div>' + refs + '</div></details>';
      }
      wrap.innerHTML =
        '<div class="lbcf-para-num">' + num +
        '<button class="lbcf-permalink" title="Copy link to this paragraph" aria-label="Copy permalink">¶</button></div>' +
        '<div class="lbcf-para-body"><p>' + linkedText + '</p>' + proofTextHtml + '</div>';
      body.appendChild(wrap);
    });
    targetEl.appendChild(body);

    // Prev / Next nav
    const nav = document.createElement('div');
    nav.className = 'lbcf-chap-nav';
    const prev = chapter.number > 1
      ? '<a class="lbcf-prev" href="chapter-' + String(chapter.number - 1).padStart(2,'0') + '.html">← Chapter ' + (chapter.number - 1) + '</a>'
      : '<span></span>';
    const idx = '<a class="lbcf-idx" href="../lbcf.html">All Chapters</a>';
    const next = chapter.number < 32
      ? '<a class="lbcf-next" href="chapter-' + String(chapter.number + 1).padStart(2,'0') + '.html">Chapter ' + (chapter.number + 1) + ' →</a>'
      : '<span></span>';
    nav.innerHTML = prev + idx + next;
    targetEl.appendChild(nav);

    // Chapter footer — copy/share actions + modernization disclaimer + PD source link
    targetEl.appendChild(renderChapterFooter(chapter));

    // Page title
    document.title = 'LBCF Chapter ' + chapter.number + ': ' + chapter.title + ' — U.S.M.C. Ministries';

    // Permalink button click handlers
    targetEl.querySelectorAll('.lbcf-permalink').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const para = btn.closest('.lbcf-para');
        const url = window.location.origin + window.location.pathname + '#' + para.id;
        navigator.clipboard.writeText(url).then(() => {
          btn.classList.add('copied');
          btn.textContent = '✓';
          setTimeout(() => { btn.classList.remove('copied'); btn.textContent = '¶'; }, 1300);
        });
      });
    });

    // Keyboard arrows for prev/next
    document.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      if (e.key === 'ArrowLeft' && chapter.number > 1) {
        window.location.href = 'chapter-' + String(chapter.number - 1).padStart(2,'0') + '.html';
      }
      if (e.key === 'ArrowRight' && chapter.number < 32) {
        window.location.href = 'chapter-' + String(chapter.number + 1).padStart(2,'0') + '.html';
      }
    });
  }

  // ---- Chapter footer: copy/share actions + disclaimer + PD source link ------
  // Build a plain-text representation of the chapter suitable for clipboard.
  function buildChapterPlainText(chapter) {
    let out = 'Second London Baptist Confession of Faith (1689)\n';
    out += 'Chapter ' + chapter.number + '. ' + chapter.title + '\n';
    if (chapter.subtitle) out += chapter.subtitle + '\n';
    out += '\n';
    chapter.paragraphs.forEach((p, i) => {
      out += (i + 1) + '. ' + p.text + '\n';
      if (p.prooftexts && p.prooftexts.length) {
        out += '   Proof-texts: ' + p.prooftexts.join('; ') + '\n';
      }
      out += '\n';
    });
    out += '— Modernized from the 1677/1689 archaic public-domain original.\n';
    out += 'Source: ' + window.location.href + '\n';
    return out;
  }

  function _flashCopied(btn, originalLabel) {
    const labelEl = btn.querySelector('.lbcf-action-label');
    btn.classList.add('copied');
    if (labelEl) labelEl.textContent = 'Copied!';
    setTimeout(() => {
      btn.classList.remove('copied');
      if (labelEl) labelEl.textContent = originalLabel;
    }, 1500);
  }

  function renderChapterFooter(chapter) {
    const footer = document.createElement('footer');
    footer.className = 'lbcf-chap-footer';

    // SVG icons (24x24 viewBox, scaled down via attrs)
    const copyTextSvg = '<svg class="lbcf-action-icon" viewBox="0 0 24 24" width="14" height="14" fill="currentColor" aria-hidden="true"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>';
    const copyLinkSvg = '<svg class="lbcf-action-icon" viewBox="0 0 24 24" width="14" height="14" fill="currentColor" aria-hidden="true"><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"/></svg>';
    const printSvg = '<svg class="lbcf-action-icon" viewBox="0 0 24 24" width="14" height="14" fill="currentColor" aria-hidden="true"><path d="M19 8H5c-1.66 0-3 1.34-3 3v6h4v4h12v-4h4v-6c0-1.66-1.34-3-3-3zm-3 11H8v-5h8v5zm3-7c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm-1-9H6v4h12V3z"/></svg>';

    const versionLine = chapter.version
      ? '<p class="lbcf-chap-version">Chapter version ' + chapter.version + ' &middot; LBCF on usmcmin.org</p>'
      : '';

    footer.innerHTML =
      '<div class="lbcf-chap-actions">' +
        '<button type="button" class="lbcf-action-btn" data-action="copy-text" title="Copy the full chapter text to your clipboard">' +
          copyTextSvg + '<span class="lbcf-action-label">Copy text</span>' +
        '</button>' +
        '<button type="button" class="lbcf-action-btn" data-action="copy-link" title="Copy a link to this chapter">' +
          copyLinkSvg + '<span class="lbcf-action-label">Copy link</span>' +
        '</button>' +
        '<button type="button" class="lbcf-action-btn" data-action="print" title="Print this chapter">' +
          printSvg + '<span class="lbcf-action-label">Print</span>' +
        '</button>' +
      '</div>' +
      '<p class="lbcf-chap-disclaimer">' +
        'Modernized in reverent contemporary English from the ' +
        '<a href="https://www.ccel.org/ccel/anonymous/bcf.html" target="_blank" rel="noopener">1677/1689 archaic original</a>' +
        ' — a public-domain text hosted by CCEL. Free to copy, quote, and share.' +
      '</p>' +
      versionLine;

    // Wire up handlers
    const copyTextBtn = footer.querySelector('[data-action="copy-text"]');
    copyTextBtn.addEventListener('click', () => {
      const text = buildChapterPlainText(chapter);
      navigator.clipboard.writeText(text).then(() => _flashCopied(copyTextBtn, 'Copy text'))
        .catch(() => alert('Copy failed — your browser may not support clipboard access. Try selecting text manually.'));
    });

    const copyLinkBtn = footer.querySelector('[data-action="copy-link"]');
    copyLinkBtn.addEventListener('click', () => {
      const url = window.location.origin + window.location.pathname;
      navigator.clipboard.writeText(url).then(() => _flashCopied(copyLinkBtn, 'Copy link'))
        .catch(() => alert('Copy failed.'));
    });

    const printBtn = footer.querySelector('[data-action="print"]');
    printBtn.addEventListener('click', () => window.print());

    return footer;
  }

  // ---- Public API ------------------------------------------------------------
  window.LBCF = {
    renderIndex,
    renderChapter,
    renderChapterFooter,
    buildChapterPlainText,
    linkScripture,
    linkDictionary,
    autoLink,
  };
})();
