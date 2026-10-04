/**
 * USMC Ministries — Assessment Core
 * Shared helpers for self-assessment tools (R.E.A.L. M.A.N., HA²PPY, FULFILLED,
 * P.U.R.E. H.E.A.R.T.S., R.E.S.O.L.U.T.E.). Keeps history, share, theme, and
 * scripture-link behavior consistent across pages.
 *
 * Pages still own their data + scoring; this module owns plumbing.
 */
(function (global) {
  'use strict';

  var THEME_KEY = 'bte-theme';
  var THEME_LEGACY = 'bteTheme';
  var CHART_CDN = 'https://cdn.jsdelivr.net/npm/chart.js@4.5.1/dist/chart.umd.min.js';

  function bibleHref(ref) {
    if (!ref) return 'bible.html';
    var cleaned = String(ref).replace(/\u2013|\u2014/g, '-').replace(/\+/g, ' ').trim();
    // Prefer human-readable passage text for BTE deep links.
    return 'bible.html?ref=' + encodeURIComponent(cleaned);
  }

  function extractPassageLabel(memoryText, fallback) {
    if (!memoryText) return fallback || 'Open passage';
    var m = String(memoryText).match(/(?:—|–|-)\s*([A-Za-z0-9\s:.\-–—]+)\s*$/);
    if (m && m[1]) return m[1].trim();
    return fallback || 'Open passage';
  }

  function migrateThemeKey() {
    var s = localStorage.getItem(THEME_KEY);
    if (s === null) {
      s = localStorage.getItem(THEME_LEGACY);
      if (s !== null) localStorage.setItem(THEME_KEY, s);
    }
    return s;
  }

  function applyStoredTheme() {
    if (migrateThemeKey() === 'light') {
      document.body.classList.add('light-mode');
      return true;
    }
    return false;
  }

  function toggleTheme(radarChart) {
    document.body.classList.toggle('light-mode');
    var isLight = document.body.classList.contains('light-mode');
    localStorage.setItem(THEME_KEY, isLight ? 'light' : 'dark');
    updateChartTheme(radarChart, isLight);
    return isLight;
  }

  function updateChartTheme(radarChart, isLight) {
    if (!radarChart || !radarChart.options || !radarChart.options.scales || !radarChart.options.scales.r) return;
    var r = radarChart.options.scales.r;
    r.grid = r.grid || {};
    r.angleLines = r.angleLines || {};
    r.ticks = r.ticks || {};
    r.grid.color = isLight ? '#ddd' : '#2a2a2a';
    r.angleLines.color = isLight ? '#ccc' : '#333';
    r.ticks.color = isLight ? '#666' : '#888';
    radarChart.update('none');
  }

  function weeksAgo(iso) {
    var ms = Date.now() - new Date(iso).getTime();
    var days = Math.floor(ms / 86400000);
    if (days <= 0) return 'Today';
    if (days === 1) return '1 day ago';
    if (days < 7) return days + ' days ago';
    var weeks = Math.floor(days / 7);
    return weeks === 1 ? '1 week ago' : weeks + ' weeks ago';
  }

  function getHistory(storageKey) {
    try {
      var raw = localStorage.getItem(storageKey);
      var parsed = JSON.parse(raw || '[]');
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
      return [];
    }
  }

  function saveHistoryEntry(storageKey, scores, maxEntries) {
    maxEntries = maxEntries || 20;
    var history = getHistory(storageKey);
    history.unshift({
      date: new Date().toISOString(),
      scores: Array.isArray(scores) ? scores.slice() : scores
    });
    if (history.length > maxEntries) history = history.slice(0, maxEntries);
    localStorage.setItem(storageKey, JSON.stringify(history));
    return history;
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text).catch(function () {
        return fallbackCopy(text);
      });
    }
    return Promise.resolve(fallbackCopy(text));
  }

  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }

  function wireShareModal(modalId, options) {
    var modal = document.getElementById(modalId);
    if (!modal) return;
    options = options || {};

    function close() {
      modal.classList.remove('open');
      document.body.classList.remove('modal-open');
      if (options.onClose) options.onClose();
    }
    function open() {
      modal.classList.add('open');
      document.body.classList.add('modal-open');
      var ta = modal.querySelector('textarea');
      if (ta) {
        setTimeout(function () { ta.focus(); ta.select(); }, 30);
      }
      if (options.onOpen) options.onOpen();
    }

    modal.addEventListener('click', function (e) {
      if (e.target === modal) close();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modal.classList.contains('open')) close();
    });

    return { open: open, close: close, el: modal };
  }

  function stripHtml(s) {
    return String(s || '').replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();
  }

  function pinChartCdnNote() {
    return CHART_CDN;
  }

  // Mark 12:30 rings. Letters stay the spokes. Color says which part of the man the dent is.
  var RINGS = {
    heart: { key: 'heart', name: 'Heart', color: '#c45c5c' },
    soul: { key: 'soul', name: 'Soul', color: '#8b73c7' },
    mind: { key: 'mind', name: 'Mind', color: '#4f8fbf' },
    strength: { key: 'strength', name: 'Strength', color: '#c4922a' }
  };
  var RING_INDEX = {
    realMan: ['soul', 'heart', 'soul', 'mind', 'mind', 'strength', 'heart'],
    happyHusband: ['heart', 'mind', 'soul', 'heart', 'strength', 'strength', 'heart'],
    fulfilledFather: ['soul', 'mind', 'heart', 'heart', 'strength', 'mind', 'strength', 'heart', 'mind'],
    pureHearts: ['soul', 'soul', 'strength', 'mind', 'heart', 'strength', 'strength', 'heart', 'mind', 'strength'],
    proven: ['heart', 'heart', 'soul', 'strength', 'mind', 'strength'],
    resolute: ['mind', 'strength', 'soul', 'strength', 'heart', 'mind', 'strength', 'soul']
  };

  function ringsFor(assessmentId, count) {
    var map = RING_INDEX[assessmentId] || [];
    var out = [];
    for (var i = 0; i < count; i++) out.push(RINGS[map[i]] || RINGS.soul);
    return out;
  }

  function paintRingRead(hostId, scores, rings, labels) {
    var host = document.getElementById(hostId);
    if (!host) return;
    var order = ['heart', 'soul', 'mind', 'strength'];
    var html = '<p class="ring-legend">Love the Lord with all your heart, soul, mind, and strength. A dent names that letter. The color names the ring.</p><div class="ring-bars">';
    order.forEach(function (key) {
      var vals = [];
      rings.forEach(function (ring, i) {
        if (ring.key === key) vals.push(Number(scores[i]) || 0);
      });
      if (!vals.length) return;
      var avg = vals.reduce(function (a, b) { return a + b; }, 0) / vals.length;
      var ring = RINGS[key];
      html += '<div class="ring-bar"><span class="ring-name" style="color:' + ring.color + '">' + ring.name + '</span><span class="ring-track"><span class="ring-fill" style="width:' + (avg * 10) + '%;background:' + ring.color + '"></span></span><span class="ring-avg">' + avg.toFixed(1) + '</span></div>';
    });
    html += '</div><div class="ring-callouts">';
    var indexed = scores.map(function (s, i) { return { s: Number(s) || 0, i: i }; }).sort(function (a, b) { return a.s - b.s; });
    var n;
    for (n = 0; n < 2 && n < indexed.length; n++) {
      var ix = indexed[n].i;
      var spoke = rings[ix];
      html += '<p class="ring-callout"><strong style="color:' + spoke.color + '">' + labels[ix] + '</strong> is ' + spoke.name + '. Score ' + indexed[n].s.toFixed(1) + '.</p>';
    }
    html += '</div>';
    host.innerHTML = html;
  }

  global.USMCAssessment = {
    bibleHref: bibleHref,
    extractPassageLabel: extractPassageLabel,
    applyStoredTheme: applyStoredTheme,
    toggleTheme: toggleTheme,
    updateChartTheme: updateChartTheme,
    weeksAgo: weeksAgo,
    getHistory: getHistory,
    saveHistoryEntry: saveHistoryEntry,
    copyText: copyText,
    wireShareModal: wireShareModal,
    stripHtml: stripHtml,
    CHART_CDN: CHART_CDN,
    pinChartCdnNote: pinChartCdnNote,
    ringsFor: ringsFor,
    paintRingRead: paintRingRead
  };
})(typeof window !== 'undefined' ? window : this);
