/* scripture-preview.js — inline verse-preview popovers for proof-text links.
 *
 * Brings a BTE-style feature to the confessional library: hover (desktop) or tap
 * (touch) any Scripture proof-text link and a small popover shows the actual verse
 * text, so you can study the confession/catechism without leaving your place.
 *
 * Standalone + dependency-free. Uses delegated listeners on `document`, so it works
 * on baked pages (catechism, lbcf-full) and client-rendered chapter pages alike —
 * any <a> whose href points at /bible.html?ref=... is wired automatically.
 *
 * Verse text is pulled from the BTE chapter store (/assets/chapters/<bookId>_<ch>.json)
 * and shown in the PUBLIC-DOMAIN World English Bible (WEB), falling back to KJV/ASV.
 * Copyrighted translations are never inlined; the link itself still opens the BTE
 * with all twelve.
 */
(function () {
  'use strict';
  if (typeof document === 'undefined' || !document.addEventListener) return;

  var BOOK_IDS = {
    'genesis':1,'gen':1,'exodus':2,'exod':2,'exo':2,'ex':2,'leviticus':3,'lev':3,'numbers':4,'num':4,
    'deuteronomy':5,'deut':5,'dt':5,'joshua':6,'josh':6,'judges':7,'judg':7,'ruth':8,
    '1 samuel':9,'1 sam':9,'2 samuel':10,'2 sam':10,'1 kings':11,'1 kgs':11,'2 kings':12,'2 kgs':12,
    '1 chronicles':13,'1 chron':13,'1 chr':13,'2 chronicles':14,'2 chron':14,'2 chr':14,
    'ezra':15,'nehemiah':16,'neh':16,'esther':17,'esth':17,'est':17,'job':18,
    'psalms':19,'psalm':19,'ps':19,'proverbs':20,'prov':20,'pr':20,'ecclesiastes':21,'eccl':21,'ecc':21,
    'song of solomon':22,'song of songs':22,'song':22,'sos':22,'cant':22,'canticles':22,
    'isaiah':23,'isa':23,'is':23,'jeremiah':24,'jer':24,'lamentations':25,'lam':25,'ezekiel':26,'ezek':26,'eze':26,
    'daniel':27,'dan':27,'hosea':28,'hos':28,'joel':29,'amos':30,'obadiah':31,'obad':31,'jonah':32,'jon':32,
    'micah':33,'mic':33,'nahum':34,'nah':34,'habakkuk':35,'hab':35,'zephaniah':36,'zeph':36,
    'haggai':37,'hag':37,'zechariah':38,'zech':38,'malachi':39,'mal':39,
    'matthew':40,'matt':40,'mt':40,'mark':41,'mk':41,'luke':42,'lk':42,'john':43,'jn':43,'acts':44,
    'romans':45,'rom':45,'1 corinthians':46,'1 cor':46,'2 corinthians':47,'2 cor':47,'galatians':48,'gal':48,
    'ephesians':49,'eph':49,'philippians':50,'phil':50,'php':50,'colossians':51,'col':51,
    '1 thessalonians':52,'1 thess':52,'1 th':52,'2 thessalonians':53,'2 thess':53,'2 th':53,
    '1 timothy':54,'1 tim':54,'2 timothy':55,'2 tim':55,'titus':56,'tit':56,'philemon':57,'philem':57,'phlm':57,
    'hebrews':58,'heb':58,'james':59,'jas':59,'1 peter':60,'1 pet':60,'2 peter':61,'2 pet':61,
    '1 john':62,'1 jn':62,'2 john':63,'2 jn':63,'3 john':64,'3 jn':64,'jude':65,'revelation':66,'rev':66
  };
  var PD_TRANSLATIONS = ['WEB', 'KJV', 'ASV'];   // public-domain only — safe to inline
  var MAX_VERSES = 5;                            // cap inlined verses per popover
  var SHOW_DELAY = 180, HIDE_DELAY = 240;

  var cache = {};                 // "id_ch" -> Promise<translations|null>
  var pop = null, showTimer = null, hideTimer = null, current = null;
  var coarse = window.matchMedia && window.matchMedia('(hover: none)').matches;

  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }

  function ensurePop() {
    if (pop) return pop;
    pop = document.createElement('div');
    pop.className = 'lbcf-verse-pop';
    pop.setAttribute('role', 'tooltip');
    pop.addEventListener('mouseenter', function () { clearTimeout(hideTimer); });
    pop.addEventListener('mouseleave', scheduleHide);
    document.body.appendChild(pop);
    return pop;
  }

  // Parse the ref out of a /bible.html?ref=... href.
  function refFromHref(href) {
    if (!href) return null;
    var m = href.match(/[?&]ref=([^&#]+)/);
    if (!m) return null;
    var ref;
    try { ref = decodeURIComponent(m[1].replace(/\+/g, ' ')); } catch (e) { return null; }
    var p = ref.match(/^\s*((?:[1-3]\s)?[A-Za-z][A-Za-z.\s]*?)\s+(\d+)(?::([\d,\-–—\s]+))?\s*$/);
    if (!p) return null;
    var id = BOOK_IDS[p[1].trim().toLowerCase()];
    if (!id) return null;
    return { id: id, ch: p[2], verses: p[3] ? p[3].trim() : null, label: ref.trim() };
  }

  // "6,128" / "1-3" / "22-23" -> [6,128] / [1,2,3] / [22,23]  (capped)
  function verseList(spec) {
    var out = [];
    spec.split(',').forEach(function (part) {
      part = part.trim();
      var r = part.match(/^(\d+)\s*[\-–—]\s*(\d+)$/);
      if (r) {
        var a = +r[1], b = +r[2];
        for (var v = a; v <= b && out.length < MAX_VERSES * 2; v++) out.push(v);
      } else if (/^\d+$/.test(part)) {
        out.push(+part);
      }
    });
    return out;
  }

  function loadChapter(id, ch) {
    var key = id + '_' + ch;
    if (!cache[key]) {
      cache[key] = fetch('/assets/chapters/' + key + '.json')
        .then(function (r) { return r.ok ? r.json() : null; })
        .catch(function () { return null; });
    }
    return cache[key];
  }

  function pickTranslation(data) {
    for (var i = 0; i < PD_TRANSLATIONS.length; i++) {
      if (data[PD_TRANSLATIONS[i]]) return PD_TRANSLATIONS[i];
    }
    return null; // no public-domain translation available — don't inline copyrighted text
  }

  function renderInto(ref, data) {
    var tr = pickTranslation(data);
    if (!tr) return null;
    var verses = data[tr];
    var nums = ref.verses ? verseList(ref.verses) : Object.keys(verses).map(Number);
    if (!nums.length) return null;
    var shown = nums.slice(0, MAX_VERSES);
    var parts = shown.map(function (v) {
      return verses[v] ? '<span class="lbcf-vp-v"><b>' + v + '</b> ' + esc(verses[v]) + '</span>' : '';
    }).filter(Boolean);
    if (!parts.length) return null;
    var more = nums.length > shown.length ? ' <span class="lbcf-vp-more">+' + (nums.length - shown.length) + ' more</span>' : '';
    return '<div class="lbcf-vp-ref">' + esc(ref.label) + '</div>' +
      '<div class="lbcf-vp-text">' + parts.join(' ') + more + '</div>' +
      '<div class="lbcf-vp-foot">' + tr + ' &middot; <span class="lbcf-vp-open">open in Bible engine →</span></div>';
  }

  function position(link) {
    var r = link.getBoundingClientRect();
    var pw = pop.offsetWidth, ph = pop.offsetHeight;
    var sx = window.pageXOffset, sy = window.pageYOffset;
    var left = sx + r.left + (r.width / 2) - (pw / 2);
    left = Math.max(sx + 8, Math.min(left, sx + document.documentElement.clientWidth - pw - 8));
    var above = r.top > ph + 12;
    var top = above ? (sy + r.top - ph - 8) : (sy + r.bottom + 8);
    pop.style.left = left + 'px';
    pop.style.top = top + 'px';
    pop.classList.toggle('below', !above);
  }

  function show(link) {
    var ref = refFromHref(link.getAttribute('href'));
    if (!ref) return;
    current = link;
    ensurePop();
    pop.innerHTML = '<div class="lbcf-vp-text lbcf-vp-loading">Loading…</div>';
    pop.classList.add('show');
    position(link);
    loadChapter(ref.id, ref.ch).then(function (data) {
      if (current !== link) return;
      var html = data && renderInto(ref, data);
      if (!html) { hide(); return; }
      pop.innerHTML = html;
      position(link);
    });
  }

  function hide() {
    current = null;
    if (pop) pop.classList.remove('show');
  }
  function scheduleHide() { clearTimeout(hideTimer); hideTimer = setTimeout(hide, HIDE_DELAY); }

  function isScripLink(el) {
    if (!el || !el.getAttribute) return null;
    var a = el.closest && el.closest('a[href*="bible.html?ref="]');
    return a || null;
  }

  // Desktop: hover. (Click still navigates normally.)
  if (!coarse) {
    document.addEventListener('mouseover', function (e) {
      var a = isScripLink(e.target);
      if (!a) return;
      clearTimeout(hideTimer); clearTimeout(showTimer);
      showTimer = setTimeout(function () { show(a); }, SHOW_DELAY);
    });
    document.addEventListener('mouseout', function (e) {
      var a = isScripLink(e.target);
      if (!a) return;
      clearTimeout(showTimer);
      scheduleHide();
    });
  }

  // Touch / coarse pointer: first tap previews, second tap (or the footer link) opens.
  document.addEventListener('click', function (e) {
    var a = isScripLink(e.target);
    // Tapping the "open in Bible engine" footer always navigates.
    if (a && e.target.closest && e.target.closest('.lbcf-vp-open')) return;
    if (!a) { if (pop && pop.classList.contains('show') && !(e.target.closest && e.target.closest('.lbcf-verse-pop'))) hide(); return; }
    if (coarse) {
      if (current === a) { return; }        // second tap → let it navigate
      e.preventDefault();
      show(a);
    }
  });

  window.addEventListener('scroll', function () { if (pop && pop.classList.contains('show')) hide(); }, { passive: true });
  // Let a tap inside the popover footer navigate to the link.
  document.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('.lbcf-vp-open') && current) {
      window.location.href = current.getAttribute('href');
    }
  });
})();
