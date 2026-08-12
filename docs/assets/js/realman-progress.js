/* realman-progress.js — opt-in, persistent 31-day progress tracker for the
 * REAL MAN Proverbs Devotional (usmcmin.org). Pure client-side (localStorage),
 * matching the site's xxxCompletionLog convention (cf. study-progress.js).
 *
 * Fully self-contained: include one <script defer src=".../realman-progress.js">
 * on any devotional page and it wires itself up by context —
 *   - a DAY page (has .day-header): injects a "Mark Day N Complete" toggle
 *     after the Prayer card, and reflects saved state.
 *   - the GRID (proverbs/index.html .grid, or proverbs.html .chapters-grid):
 *     injects a progress banner (X of 31 + bar + "continue" + reset) and marks
 *     completed cards with a gold ring + shield-star.
 * No backend, no dependencies. Degrades to a no-op if localStorage is blocked.
 */
(function () {
  'use strict';
  var KEY = 'realmanProverbsLog';           // house convention: array of completed day numbers
  var TOTAL = 31;
  // icons live at docs/assets/icons; day pages + index sit in /proverbs/, the landing in /docs/
  var ASSET = /\/proverbs\//.test(location.pathname) ? '../assets/' : 'assets/';

  function load() {
    try { var v = JSON.parse(localStorage.getItem(KEY) || '[]'); return Array.isArray(v) ? v : []; }
    catch (e) { return []; }
  }
  function save(list) { try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) {} }
  function has(list, n) { return list.indexOf(n) !== -1; }
  function toggle(n) {
    var list = load(), i = list.indexOf(n);
    if (i === -1) list.push(n); else list.splice(i, 1);
    list.sort(function (a, b) { return a - b; });
    save(list);
    return list;
  }
  function firstIncomplete(list) {
    for (var d = 1; d <= TOTAL; d++) if (!has(list, d)) return d;
    return TOTAL; // all done
  }

  function injectStyle() {
    if (document.getElementById('rmp-style')) return;
    var css =
      '.rmp-complete-wrap{text-align:center;margin:2.25rem 0 0.5rem;}' +
      '.rmp-complete-btn{display:inline-flex;align-items:center;gap:.6rem;cursor:pointer;' +
        'font-family:Inter,-apple-system,sans-serif;font-weight:700;font-size:.92rem;' +
        'letter-spacing:.04em;border-radius:8px;padding:.8rem 1.6rem;transition:all .18s ease;' +
        'border:1px solid rgba(212,168,67,.5);background:rgba(212,168,67,.10);color:#e8c46a;}' +
      '.rmp-complete-btn:hover{background:rgba(212,168,67,.18);border-color:#d4a843;}' +
      '.rmp-complete-btn.is-done{background:#d4a843;color:#0d1117;border-color:#d4a843;}' +
      '.rmp-complete-btn img{width:18px;height:18px;vertical-align:middle;}' +
      '.rmp-complete-sub{color:#8b949e;font-size:.78rem;margin-top:.5rem;}' +
      '.rmp-complete-sub a{color:#58a6ff;text-decoration:none;} .rmp-complete-sub a:hover{text-decoration:underline;}' +
      '.rmp-banner{background:linear-gradient(135deg,rgba(212,168,67,.12),rgba(22,27,34,0) 65%);' +
        'border:1px solid rgba(212,168,67,.3);border-radius:12px;padding:1.25rem 1.5rem;margin:0 auto 1.5rem;}' +
      '.rmp-banner-top{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;flex-wrap:wrap;}' +
      '.rmp-banner-title{font-family:"Playfair Display",Georgia,serif;font-weight:700;color:#e6edf3;font-size:1.05rem;}' +
      '.rmp-banner-count{color:#d4a843;font-weight:700;font-size:.9rem;white-space:nowrap;}' +
      '.rmp-bar{height:9px;border-radius:5px;background:rgba(255,255,255,.07);overflow:hidden;margin:.8rem 0 .6rem;}' +
      '.rmp-bar-fill{height:100%;border-radius:5px;background:linear-gradient(90deg,#d4a843,#e8c46a);' +
        'width:0;transition:width .5s ease;}' +
      '.rmp-banner-actions{display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap;}' +
      '.rmp-continue{display:inline-flex;align-items:center;gap:.4rem;background:#d4a843;color:#0d1117;' +
        'font-weight:700;font-size:.82rem;text-decoration:none;padding:.5rem 1rem;border-radius:7px;}' +
      '.rmp-continue:hover{opacity:.9;}' +
      '.rmp-reset{background:none;border:none;color:#6e7681;font-size:.75rem;cursor:pointer;text-decoration:underline;}' +
      '.rmp-reset:hover{color:#8b949e;}' +
      '.rmp-done-card{position:relative;}' +
      '.rmp-done-card::after{content:"";position:absolute;inset:0;border:2px solid #d4a843;border-radius:inherit;' +
        'pointer-events:none;box-shadow:0 0 0 1px rgba(212,168,67,.25) inset;}' +
      '.rmp-check{position:absolute;top:6px;right:6px;width:15px;height:15px;z-index:2;}' +
      '@media (prefers-reduced-motion:reduce){.rmp-complete-btn,.rmp-bar-fill{transition:none;}}';
    var s = document.createElement('style');
    s.id = 'rmp-style'; s.textContent = css;
    document.head.appendChild(s);
  }

  /* ---- DAY page: a "Mark Day N Complete" toggle after the Prayer card ---- */
  function initDayPage(day) {
    var cards = document.querySelectorAll('.content-card');
    var anchor = document.querySelector('.chapter-nav') || (cards.length ? cards[cards.length - 1] : null);
    if (!anchor) return;
    var wrap = document.createElement('div');
    wrap.className = 'rmp-complete-wrap';
    var btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'rmp-complete-btn';
    var sub = document.createElement('div');
    sub.className = 'rmp-complete-sub';
    wrap.appendChild(btn); wrap.appendChild(sub);
    // place it just before the chapter-nav (end of the day's content)
    anchor.parentNode.insertBefore(wrap, anchor);

    function render() {
      var list = load(), done = has(list, day);
      btn.classList.toggle('is-done', done);
      btn.setAttribute('aria-pressed', done ? 'true' : 'false');
      btn.innerHTML = (done
        ? '<img src="' + ASSET + 'icons/shield-star.png" alt=""> Day ' + day + ' Complete'
        : 'Mark Day ' + day + ' Complete');
      var n = list.length;
      if (done) {
        var nxt = day < TOTAL ? day + 1 : null;
        sub.innerHTML = n + ' of ' + TOTAL + ' days complete' +
          (nxt ? ' &middot; <a href="' + nxt + '.html">On to Day ' + nxt + ' &rarr;</a>'
               : ' &middot; you finished the journey. Begin again at <a href="1.html">Day 1</a>.');
      } else {
        sub.innerHTML = 'Tap when you have read the chapter and worked through today.';
      }
    }
    btn.addEventListener('click', function () { toggle(day); render(); });
    render();
  }

  /* ---- GRID (index / landing): progress banner + mark completed cards ---- */
  function cardDay(a) {
    var m = (a.getAttribute('href') || '').match(/(\d+)\.html/);
    return m ? parseInt(m[1], 10) : null;
  }
  function initGrid(gridSel, mountBeforeSel) {
    var grid = document.querySelector(gridSel);
    if (!grid) return;
    var list = load();

    // decorate completed cards
    Array.prototype.forEach.call(grid.querySelectorAll('a[href]'), function (a) {
      var d = cardDay(a);
      if (d && has(list, d)) {
        a.classList.add('rmp-done-card');
        if (!a.querySelector('.rmp-check')) {
          var img = document.createElement('img');
          img.className = 'rmp-check'; img.alt = 'completed'; img.src = ASSET + 'icons/shield-star.png';
          a.appendChild(img);
        }
      }
    });

    // progress banner, inserted before the grid (or its section label)
    var mount = (mountBeforeSel && document.querySelector(mountBeforeSel)) || grid;
    var banner = document.createElement('div');
    banner.className = 'rmp-banner';
    banner.innerHTML =
      '<div class="rmp-banner-top"><span class="rmp-banner-title">Your 31-Day Journey</span>' +
      '<span class="rmp-banner-count"></span></div>' +
      '<div class="rmp-bar"><div class="rmp-bar-fill"></div></div>' +
      '<div class="rmp-banner-actions"><a class="rmp-continue" href="#"></a>' +
      '<button type="button" class="rmp-reset">Reset progress</button></div>';
    mount.parentNode.insertBefore(banner, mount);

    var count = banner.querySelector('.rmp-banner-count');
    var fill = banner.querySelector('.rmp-bar-fill');
    var cont = banner.querySelector('.rmp-continue');
    var reset = banner.querySelector('.rmp-reset');
    var hrefPrefix = /\/proverbs\//.test(location.pathname) ? '' : 'proverbs/'; // landing links into subdir

    function render() {
      var l = load(), n = l.length, pct = Math.round((n / TOTAL) * 100);
      count.textContent = n + ' of ' + TOTAL + ' days';
      fill.style.width = pct + '%';
      var nextDay = firstIncomplete(l);
      if (n === 0) { cont.textContent = 'Start Day 1 →'; cont.href = hrefPrefix + '1.html'; }
      else if (n >= TOTAL) { cont.textContent = 'Read it again →'; cont.href = hrefPrefix + '1.html'; }
      else { cont.textContent = 'Continue — Day ' + nextDay + ' →'; cont.href = hrefPrefix + nextDay + '.html'; }
    }
    reset.addEventListener('click', function () {
      if (!confirm('Reset your 31-day progress? This clears every completed day on this device.')) return;
      save([]);
      Array.prototype.forEach.call(grid.querySelectorAll('.rmp-done-card'), function (a) {
        a.classList.remove('rmp-done-card');
        var c = a.querySelector('.rmp-check'); if (c) c.remove();
      });
      render();
    });
    render();
  }

  function boot() {
    injectStyle();
    var dayHeader = document.querySelector('.day-header h2');
    if (dayHeader) {
      var m = dayHeader.textContent.match(/Day\s+(\d+)/);
      if (m) { initDayPage(parseInt(m[1], 10)); return; }
    }
    if (document.querySelector('.grid')) initGrid('.grid', '.grid');            // proverbs/index.html
    else if (document.querySelector('.chapters-grid')) initGrid('.chapters-grid', '.section-label'); // proverbs.html
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
