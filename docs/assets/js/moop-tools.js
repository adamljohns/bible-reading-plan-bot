/* moop-tools.js — site-wide interactive toolkit (share / bookmark / amen / feedback)
 *
 * Borrowed from the BTE toolset (bte-bookmarks, share + toast patterns) and
 * generalized for the reference surfaces: Dictionary, Lexicon, Cross-References,
 * Church Directory. Self-contained: injects its own styles, uses the page's
 * existing CSS variables (--gold, --card, --border) so dark/light both work.
 *
 * Storage (localStorage, site-wide "moop-" family, coexists with "bte-"):
 *   moop-bookmarks  [{u,t,k,ts}]  saved pages (url, title, kind, timestamp)
 *   moop-amens      {slug:1}      one Amen per visitor per page
 *
 * Amen counts are progressive-enhancement: the button POSTs to /api/amen and
 * GETs /api/amen?slug= IF that endpoint exists (future Cloudflare Worker + KV);
 * until then every network call fails silently and the button works locally.
 */
(function () {
  'use strict';
  if (document.querySelector('meta[content*="MERGED-REDIRECT"]')) return; // stubs
  if (window.__moopTools) return; window.__moopTools = 1;

  /* ---------- page identity ---------- */
  var path = location.pathname.replace(/\/+$/, '');
  var page = path.split('/').pop() || 'index.html';
  var slugBase = page.replace(/\.html?$/, '') || 'index';
  var kind = /\/dictionary\//.test(path) ? 'dictionary'
           : /\/lexicon\//.test(path)    ? 'lexicon'
           : /\/churches\//.test(path)   ? 'church'
           : /cross-references/.test(page) ? 'cross-references'
           : 'page';
  var slug = (kind === 'page' ? slugBase : kind + ':' + slugBase);
  var canonEl = document.querySelector('link[rel="canonical"]');
  var canonical = (canonEl && canonEl.href) || (location.origin + location.pathname);
  var wordEl = document.querySelector('.word-title, h1');
  var title = (wordEl ? wordEl.textContent.trim() : document.title.replace(/\s*[—-].*$/, '')) || slugBase;
  var isEntry = !!document.querySelector('.word-title');

  /* ---------- tiny utils ---------- */
  function store(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function load(k, d) { try { return JSON.parse(localStorage.getItem(k)) || d; } catch (e) { return d; } }
  function toast(msg) {
    var t = document.getElementById('moop-toast');
    if (!t) { t = document.createElement('div'); t.id = 'moop-toast'; document.body.appendChild(t); }
    t.textContent = msg; t.classList.add('show');
    clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove('show'); }, 2200);
  }
  function copyText(txt, okMsg) {
    function done() { toast(okMsg || 'Copied'); }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(txt).then(done, function () { legacy(); });
    } else { legacy(); }
    function legacy() {
      var ta = document.createElement('textarea');
      ta.value = txt; ta.style.cssText = 'position:fixed;opacity:0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); done(); } catch (e) { toast('Copy failed'); }
      ta.remove();
    }
  }

  /* ---------- styles (uses page vars; sane fallbacks) ---------- */
  var css = [
    '.moop-toolbar{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:14px auto 4px;max-width:820px;padding:0 10px}',
    '.moop-toolbar button,.moop-toolbar a{font:500 0.82rem Inter,sans-serif;cursor:pointer;text-decoration:none;',
    ' background:var(--card,#111);color:var(--white,#eee) !important;border:1px solid var(--border,#333);',
    ' border-radius:20px;padding:6px 14px;display:inline-flex;align-items:center;gap:6px;transition:border-color .2s,color .2s}',
    '.moop-toolbar button:hover,.moop-toolbar a:hover{border-color:var(--gold,#D4AF37);color:var(--gold,#D4AF37) !important}',
    '.moop-toolbar .on{border-color:var(--gold,#D4AF37);color:var(--gold,#D4AF37) !important}',
    '#moop-toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%) translateY(20px);opacity:0;',
    ' background:var(--gold,#D4AF37);color:#000;font:600 0.85rem Inter,sans-serif;padding:9px 20px;border-radius:22px;',
    ' pointer-events:none;transition:all .25s;z-index:9999;box-shadow:0 4px 18px rgba(0,0,0,.45)}',
    '#moop-toast.show{opacity:1;transform:translateX(-50%) translateY(0)}',
    '.moop-seclink{margin-left:8px;font-size:0.8rem;opacity:0;text-decoration:none;cursor:pointer;transition:opacity .15s}',
    '.section:hover .moop-seclink,.moop-seclink:focus{opacity:.75}.moop-seclink:hover{opacity:1}',
    '#moop-saved{position:fixed;top:64px;right:14px;width:min(340px,92vw);max-height:70vh;overflow:auto;z-index:9998;',
    ' background:var(--card,#141414);border:1px solid var(--gold,#D4AF37);border-radius:12px;padding:14px 16px;',
    ' box-shadow:0 8px 30px rgba(0,0,0,.5);font-family:Inter,sans-serif;color:var(--white,#eee)}',
    '#moop-saved h4{color:var(--gold,#D4AF37);font-size:0.95rem;margin:0 0 10px}',
    '#moop-saved .mi{display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid var(--border,#2a2a2a);font-size:0.84rem}',
    '#moop-saved .mi a{color:var(--white,#eee) !important;text-decoration:none;flex:1}',
    '#moop-saved .mi a:hover{color:var(--gold,#D4AF37) !important}',
    '#moop-saved .mi .k{font-size:0.66rem;color:var(--gray,#888);text-transform:uppercase;letter-spacing:.5px}',
    '#moop-saved .mi button{background:none;border:none;color:var(--gray,#888);cursor:pointer;font-size:0.9rem}',
    '#moop-saved .mi button:hover{color:#e66}',
    '#moop-saved .actions{display:flex;gap:10px;margin-top:10px}',
    '#moop-saved .actions button{font:500 0.75rem Inter;background:none;border:1px solid var(--border,#333);',
    ' border-radius:14px;color:var(--gray,#999);padding:4px 12px;cursor:pointer}',
    '#moop-saved .actions button:hover{border-color:var(--gold,#D4AF37);color:var(--gold,#D4AF37)}',
    '@media print{.moop-toolbar,#moop-saved,#moop-toast,.moop-seclink{display:none !important}}'
  ].join('');
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  /* ---------- bookmarks ---------- */
  var BK = 'moop-bookmarks';
  function bookmarks() { return load(BK, []); }
  function isSaved() { return bookmarks().some(function (b) { return b.u === canonical; }); }
  function toggleSave() {
    var list = bookmarks();
    if (isSaved()) { list = list.filter(function (b) { return b.u !== canonical; }); toast('Bookmark removed'); }
    else {
      list.unshift({ u: canonical, t: title, k: kind, ts: Date.now() });
      if (list.length > 300) list = list.slice(0, 300);
      toast('Saved to your bookmarks');
    }
    store(BK, list); paintSave(); paintPanel();
  }
  function paintSave() {
    var b = document.getElementById('moop-bk'); if (!b) return;
    var on = isSaved();
    b.classList.toggle('on', on);
    b.innerHTML = ico(ICON.bookmark) + (on ? ' Saved' : ' Bookmark');
    var s = document.getElementById('moop-savedbtn');
    if (s) s.innerHTML = ico(ICON.saved) + ' My Saved (' + bookmarks().length + ')';
  }
  function paintPanel() {
    var p = document.getElementById('moop-saved'); if (!p) return;
    var list = bookmarks();
    var rows = list.map(function (b, i) {
      return '<div class="mi"><a href="' + b.u + '">' + b.t.replace(/</g, '&lt;') +
             ' <span class="k">' + b.k + '</span></a><button data-i="' + i + '" title="Remove">&#10005;</button></div>';
    }).join('') || '<p style="font-size:0.82rem;color:var(--gray,#888)">Nothing saved yet. Tap Bookmark on any entry.</p>';
    p.innerHTML = '<h4>' + ico(ICON.saved) + ' My Saved</h4>' + rows +
      '<div class="actions"><button id="moop-copyall">Copy list</button><button id="moop-clearall">Clear all</button><button id="moop-closep">Close</button></div>';
    p.querySelectorAll('.mi button').forEach(function (x) {
      x.onclick = function () { var l = bookmarks(); l.splice(+x.dataset.i, 1); store(BK, l); paintSave(); paintPanel(); };
    });
    p.querySelector('#moop-copyall').onclick = function () {
      copyText(list.map(function (b) { return b.t + ' — ' + b.u; }).join('\n'), 'Bookmark list copied');
    };
    p.querySelector('#moop-clearall').onclick = function () {
      if (confirm('Clear all saved bookmarks?')) { store(BK, []); paintSave(); paintPanel(); }
    };
    p.querySelector('#moop-closep').onclick = function () { p.remove(); };
  }
  function togglePanel() {
    var p = document.getElementById('moop-saved');
    if (p) { p.remove(); return; }
    p = document.createElement('div'); p.id = 'moop-saved'; document.body.appendChild(p); paintPanel();
  }

  /* ---------- amen (local now; /api/amen when the Worker lands) ---------- */
  var AM = 'moop-amens';
  function amened() { return !!load(AM, {})[slug]; }
  function paintAmen(count) {
    var b = document.getElementById('moop-amen'); if (!b) return;
    var on = amened();
    b.classList.toggle('on', on);
    b.innerHTML = ico(ICON.amen) + ' Amen' + (on ? ' &#10003;' : '') + (count ? ' &middot; ' + count : '');
  }
  function doAmen() {
    if (amened()) { toast('You already said Amen to this one'); return; }
    var m = load(AM, {}); m[slug] = 1; store(AM, m);
    paintAmen(); toast('Amen recorded — thank you!');
    try {
      fetch('/api/amen', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slug: slug }) })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (d) { if (d && d.count) paintAmen(d.count); })
        .catch(function () {});
    } catch (e) {}
  }
  function fetchAmenCount() {
    try {
      var ctl = ('AbortController' in window) ? new AbortController() : null;
      if (ctl) setTimeout(function () { ctl.abort(); }, 1800);
      fetch('/api/amen?slug=' + encodeURIComponent(slug), ctl ? { signal: ctl.signal } : {})
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (d) { if (d && d.count) paintAmen(d.count); })
        .catch(function () {});
    } catch (e) {}
  }

  /* ---------- share / copy ---------- */
  function defText() {
    var d = document.querySelector('.biblical-def p, .word-header + .section p');
    return d ? d.textContent.trim() : '';
  }
  function doShare() {
    var text = title + ' — The MOOP Dictionary';
    if (navigator.share) {
      navigator.share({ title: text, text: defText().slice(0, 140), url: canonical }).catch(function () {});
    } else {
      copyText(canonical, 'Link copied — paste anywhere');
    }
  }
  function doCopyDef() {
    var d = defText();
    copyText('“' + title + '” — ' + (d ? d + '\n\n' : '') + canonical, 'Definition copied with link');
  }

  /* ---------- section permalinks (added after ico() is ready; see bottom) ---------- */
  function addSectionLinks() {
    document.querySelectorAll('.section[id] > h3').forEach(function (h) {
      var id = h.parentElement.id; if (!id) return;
      var a = document.createElement('a');
      a.className = 'moop-seclink'; a.href = '#' + id; a.title = 'Copy link to this section';
      a.innerHTML = ico('shield-infinity-rope-16.png', 12);
      a.addEventListener('click', function (ev) {
        ev.preventDefault();
        copyText(canonical + '#' + id, 'Section link copied');
        history.replaceState(null, '', '#' + id);
      });
      h.appendChild(a);
    });
  }

  /* ---------- feedback + brand icons (no stock emojis — house shield set) ---------- */
  var depth = (path.match(/\//g) || []).length > 1 ? '../' : '';
  var feedbackHref = depth + 'connect.html?about=' + encodeURIComponent(slug);
  function ico(name, size) {
    size = size || 15;
    return '<img src="' + depth + 'assets/icons/' + name + '" width="' + size + '" height="' + size +
           '" alt="" style="vertical-align:-3px" loading="lazy">';
  }
  var ICON = {
    share:   'shield-infinity-rope-24.png',
    copy:    'shield-quill-note-24.png',
    bookmark:'shield-save-48.png',
    amen:    'shield-chain-prayer-48.png',
    feedback:'shield-handshake.png',
    saved:   'shield-star.png'
  };

  /* ---------- toolbar ---------- */
  var bar = document.createElement('div');
  bar.className = 'moop-toolbar';
  bar.innerHTML =
    '<button id="moop-share" title="Share this page">' + ico(ICON.share) + ' Share</button>' +
    (isEntry && defText() ? '<button id="moop-copydef" title="Copy the definition with a link">' + ico(ICON.copy) + ' Copy Definition</button>' : '') +
    '<button id="moop-bk" title="Save to your bookmarks">' + ico(ICON.bookmark) + ' Bookmark</button>' +
    (isEntry ? '<button id="moop-amen" title="This entry blessed you — add your Amen">' + ico(ICON.amen) + ' Amen</button>' : '') +
    '<a id="moop-fb" href="' + feedbackHref + '" title="Suggest an improvement to this entry">' + ico(ICON.feedback) + ' Feedback</a>' +
    '<button id="moop-savedbtn" title="Open your saved bookmarks">' + ico(ICON.saved) + ' My Saved</button>';

  var anchor = document.querySelector('.word-header') || document.querySelector('.dict-back-nav') || document.querySelector('nav');
  if (anchor) anchor.insertAdjacentElement('afterend', bar); else document.body.prepend(bar);

  document.getElementById('moop-share').onclick = doShare;
  var cd = document.getElementById('moop-copydef'); if (cd) cd.onclick = doCopyDef;
  document.getElementById('moop-bk').onclick = toggleSave;
  var am = document.getElementById('moop-amen'); if (am) am.onclick = doAmen;
  document.getElementById('moop-savedbtn').onclick = togglePanel;

  paintSave(); paintAmen(); addSectionLinks();
  if (isEntry) fetchAmenCount();
})();
