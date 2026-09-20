/* U.S.M.C. Ministries — Lexicon index loader (PJG-0919-LEX1)
 *
 * The front door used to bake all ~6,300 word cards into lexicon.html, which
 * made it a 1.8 MB document that had to download and parse before a man saw
 * anything. The cards now arrive as JSON and are built here.
 *
 * The rendered DOM is byte-for-byte the shape the page already used --
 * a.word-card with data-search and the four wc-* spans -- so filterWords(),
 * filterByLetter() and scrollToSection() keep working untouched. This moves
 * where the cards come from; it does not change what they are.
 *
 * Entries with a page but no lexical content are deliberately absent from the
 * index. An empty word study is worse than no word study.
 */
(function () {
  'use strict';

  var SRC = '/assets/lexicon-words.json';
  var CHUNK = 400;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c];
    });
  }

  // Must match the markup rebuild-lexicon.py emitted, exactly: the displayed
  // gloss is clipped at 40 characters so the cards keep a even height, while
  // data-search carries the full text so a search still finds the long ones.
  function cardHtml(w) {
    var code = w[0], translit = w[1], gloss = w[2], original = w[3];
    var search = [code.toLowerCase(), (translit || '').toLowerCase(),
                  (gloss || '').toLowerCase()].filter(Boolean).join(' ');
    var shown = gloss.length > 40 ? gloss.slice(0, 37) + '...' : gloss;
    return '<a href="lexicon/' + esc(code) + '.html" class="word-card" data-search="' +
      esc(search) + '">' +
      '<span class="wc-strongs">' + esc(code) + '</span>' +
      (original ? '<span class="wc-original">' + esc(original) + '</span>' : '') +
      (translit ? '<span class="wc-translit">' + esc(translit) + '</span>' : '') +
      '<span class="wc-def">' + esc(shown) + '</span></a>';
  }

  function paint(grid, words, done) {
    var i = 0;
    (function step() {
      if (i >= words.length) { done(); return; }
      var end = Math.min(i + CHUNK, words.length);
      var buf = '';
      for (; i < end; i++) buf += cardHtml(words[i]);
      grid.insertAdjacentHTML('beforeend', buf);
      // Yield between chunks so the page stays responsive while it fills.
      (window.requestAnimationFrame || window.setTimeout)(step);
    })();
  }

  function status(msg) {
    var el = document.getElementById('lexIndexStatus');
    if (el) el.textContent = msg || '';
  }

  function boot(data) {
    var words = data.words || [];
    var heb = [], grk = [];
    for (var i = 0; i < words.length; i++) {
      (words[i][0].charAt(0) === 'H' ? heb : grk).push(words[i]);
    }

    if (typeof lexApplyStats === 'function') lexApplyStats(heb.length, grk.length);
    var hs = document.getElementById('hebrew-sub');
    if (hs) hs.textContent = heb.length.toLocaleString() + ' words from the Hebrew Scriptures';
    var gs = document.getElementById('greek-sub');
    if (gs) gs.textContent = grk.length.toLocaleString() + ' words from the Greek New Testament';

    var gh = document.getElementById('hebrew-grid');
    var gg = document.getElementById('greek-grid');
    var left = 2;
    function finished() {
      if (--left) return;
      status('');
      document.body.classList.add('lex-index-ready');
      if (typeof lexMarkEmptyLetters === 'function') lexMarkEmptyLetters();
      // A deep link such as lexicon.html#greek should still land correctly.
      if (location.hash === '#greek' || location.hash === '#hebrew') {
        if (typeof scrollToSection === 'function') scrollToSection(location.hash.slice(1));
      }
    }
    if (gh) paint(gh, heb, finished); else left--;
    if (gg) paint(gg, grk, finished); else left--;
    if (!gh && !gg) status('');
  }

  status('Loading the lexicon…');
  fetch(SRC)
    .then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    })
    .then(boot)
    .catch(function (e) {
      status('The word list could not load (' + e.message + '). Try a refresh.');
    });
})();
