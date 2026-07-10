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
    var cleaned = String(ref).replace(/\u2013|\u2014/g, '-').trim();
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
    pinChartCdnNote: pinChartCdnNote
  };
})(typeof window !== 'undefined' ? window : this);
