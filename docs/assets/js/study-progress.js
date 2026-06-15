/* study-progress.js — opt-in, persistent reading-progress tracker for usmcmin.org
 *
 * Gamified, traceable, toggle-on/off progress through any sectioned reading
 * (the Baptist Catechism today; the LBCF / Institutes next). Pure client-side
 * (localStorage) — matches the site's readingCompletionLog convention. No backend.
 *
 * Per-item "mark learned" checkmarks (shown only when tracking is ON), a live
 * progress bar, per-section rollups, and a printable Certificate of Completion
 * unlocked at 100%.
 *
 * Usage (the page provides the mount points + calls init):
 *   StudyProgress.init({
 *     storeKey:    'catechismCompletionLog',  // localStorage key (house: xxxCompletionLog)
 *     trackKey:    'catechism-track',          // localStorage key for the on/off toggle
 *     itemSelector:'.cat-q',                   // each trackable item (must have an id)
 *     sectionSelector:'.cat-section',          // optional, for per-section rollups
 *     labelSingular:'question', labelPlural:'questions',
 *     workTitle:   'The Baptist Catechism',
 *     workSubtitle:'A U.S.M.C. Ministries Edition',
 *     certVerse:   '"...the holy Scriptures..." — 2 Timothy 3:15',
 *     toggleMount: '#study-toggle-mount',
 *     progressMount:'#study-progress-mount'
 *   });
 */
(function () {
  'use strict';

  function loadLog(key) {
    try { const v = JSON.parse(localStorage.getItem(key) || '[]'); return Array.isArray(v) ? v : []; }
    catch (e) { return []; }
  }
  function saveLog(key, log) { try { localStorage.setItem(key, JSON.stringify(log)); } catch (e) {} }
  function getBool(key) { try { return localStorage.getItem(key) === '1'; } catch (e) { return false; } }
  function setBool(key, v) { try { localStorage.setItem(key, v ? '1' : '0'); } catch (e) {} }

  function init(cfg) {
    const items = Array.prototype.slice.call(document.querySelectorAll(cfg.itemSelector))
      .filter((el) => el.id);
    if (!items.length) return;
    const total = items.length;
    const sections = cfg.sectionSelector
      ? Array.prototype.slice.call(document.querySelectorAll(cfg.sectionSelector)) : [];

    // ---- state ----
    let log = loadLog(cfg.storeKey);                 // [{id, ts}]
    const doneSet = new Set(log.map((e) => e.id));
    let tracking = getBool(cfg.trackKey);

    // ---- build the toggle ----
    const toggleMount = document.querySelector(cfg.toggleMount);
    const progressMount = document.querySelector(cfg.progressMount);
    if (!toggleMount || !progressMount) return;

    toggleMount.innerHTML =
      '<div class="study-toggle">' +
      '<div class="study-toggle-text"><strong>Track my progress</strong>' +
      '<span class="study-toggle-sub">Check off each ' + cfg.labelSingular +
      ' as you learn it — saved on this device — and print a certificate when you finish.</span></div>' +
      '<button type="button" class="study-switch" id="study-switch" role="switch" aria-label="Toggle progress tracking">' +
      '<span class="study-switch-knob"></span></button></div>';

    // ---- build the progress card (hidden until tracking on) ----
    progressMount.innerHTML =
      '<div class="study-progress" id="study-progress" hidden>' +
        '<div class="study-progress-info">' +
          '<span class="study-progress-count" id="study-count"></span>' +
          '<span class="study-progress-pct" id="study-pct"></span>' +
        '</div>' +
        '<div class="study-bar-bg"><div class="study-bar-fill" id="study-fill" style="width:0%"></div></div>' +
        '<div class="study-progress-actions">' +
          '<button type="button" class="study-btn" id="study-reset">Reset progress</button>' +
          '<button type="button" class="study-btn study-btn-cert" id="study-cert-btn" disabled>Print Certificate of Completion</button>' +
        '</div>' +
        '<p class="study-milestone" id="study-milestone" hidden></p>' +
      '</div>';

    const switchEl = document.getElementById('study-switch');
    const progEl = document.getElementById('study-progress');
    const countEl = document.getElementById('study-count');
    const pctEl = document.getElementById('study-pct');
    const fillEl = document.getElementById('study-fill');
    const certBtn = document.getElementById('study-cert-btn');
    const resetBtn = document.getElementById('study-reset');
    const milestoneEl = document.getElementById('study-milestone');

    // ---- inject per-item check buttons + per-section badges ----
    items.forEach((el) => {
      if (el.querySelector('.study-check')) return;
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'study-check';
      btn.setAttribute('aria-label', 'Mark this ' + cfg.labelSingular + ' as learned');
      btn.addEventListener('click', function () { toggleItem(el.id); });
      el.appendChild(btn);
    });
    sections.forEach((sec) => {
      if (sec.querySelector('.study-sec-badge')) return;
      const head = sec.querySelector('.cat-section-head') || sec;
      const badge = document.createElement('div');
      badge.className = 'study-sec-badge';
      head.appendChild(badge);
    });

    function toggleItem(id) {
      if (doneSet.has(id)) {
        doneSet.delete(id);
        log = log.filter((e) => e.id !== id);
      } else {
        doneSet.add(id);
        log.push({ id: id, ts: new Date().toISOString() });
      }
      saveLog(cfg.storeKey, log);
      render();
    }

    function setTracking(on) {
      tracking = on;
      setBool(cfg.trackKey, on);
      render();
    }

    function render() {
      document.body.classList.toggle('study-tracking', tracking);
      switchEl.classList.toggle('on', tracking);
      switchEl.setAttribute('aria-checked', tracking ? 'true' : 'false');
      progEl.hidden = !tracking;

      // per-item state
      items.forEach((el) => {
        const done = doneSet.has(el.id);
        el.classList.toggle('study-done', done);
        const btn = el.querySelector('.study-check');
        if (btn) {
          btn.classList.toggle('checked', done);
          btn.textContent = done ? '✓' : '';
          btn.title = done ? 'Learned — click to unmark' : 'Mark as learned';
        }
      });
      // per-section rollups
      sections.forEach((sec) => {
        const secItems = Array.prototype.slice.call(sec.querySelectorAll(cfg.itemSelector));
        const d = secItems.filter((el) => doneSet.has(el.id)).length;
        const badge = sec.querySelector('.study-sec-badge');
        if (badge) {
          const complete = secItems.length > 0 && d === secItems.length;
          badge.textContent = complete ? '✓ ' + d + '/' + secItems.length : d + '/' + secItems.length;
          badge.classList.toggle('complete', complete);
        }
      });
      // overall progress
      const done = doneSet.size;
      const pct = total ? Math.round((done / total) * 100) : 0;
      countEl.textContent = done + ' of ' + total + ' ' + (total === 1 ? cfg.labelSingular : cfg.labelPlural) + ' learned';
      pctEl.textContent = pct + '%';
      fillEl.style.width = pct + '%';
      const complete = done === total && total > 0;
      certBtn.disabled = !complete;
      certBtn.title = complete ? 'Print your certificate' : 'Complete all ' + total + ' to unlock your certificate';
      fillEl.classList.toggle('complete', complete);
      // milestone encouragement
      if (tracking && done > 0) {
        milestoneEl.hidden = false;
        if (complete) milestoneEl.textContent = '🎉 You’ve completed the whole catechism. Well done, good and faithful servant — print your certificate below.';
        else if (pct >= 75) milestoneEl.textContent = 'The home stretch — ' + (total - done) + ' to go.';
        else if (pct >= 50) milestoneEl.textContent = 'Halfway home. Keep at it.';
        else if (pct >= 25) milestoneEl.textContent = 'A quarter learned — a good and steady start.';
        else milestoneEl.textContent = 'Begun is half done. One ' + cfg.labelSingular + ' at a time.';
      } else {
        milestoneEl.hidden = true;
      }
    }

    switchEl.addEventListener('click', function () { setTracking(!tracking); });
    resetBtn.addEventListener('click', function () {
      if (!confirm('Reset your progress on ' + cfg.workTitle + '? This clears every checkmark on this device.')) return;
      log = []; doneSet.clear(); saveLog(cfg.storeKey, log); render();
    });
    certBtn.addEventListener('click', function () { printCertificate(cfg, log, total); });

    render();
  }

  // ---- Certificate of Completion (print) ----
  function printCertificate(cfg, log, total) {
    let name = '';
    try { name = localStorage.getItem('study-cert-name') || ''; } catch (e) {}
    name = (window.prompt('Name to print on the certificate:', name) || '').trim();
    if (!name) return;
    try { localStorage.setItem('study-cert-name', name); } catch (e) {}

    // completion date = latest timestamp in the log
    let when = new Date();
    try {
      const ts = log.map((e) => e.ts).filter(Boolean).sort();
      if (ts.length) when = new Date(ts[ts.length - 1]);
    } catch (e) {}
    const dateStr = when.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });

    let cert = document.getElementById('study-cert');
    if (cert) cert.remove();
    cert = document.createElement('div');
    cert.id = 'study-cert';
    cert.className = 'study-cert';
    cert.innerHTML =
      '<div class="study-cert-inner">' +
        '<img class="study-cert-crest" src="/assets/icons/shield-cross.png" alt="">' +
        '<div class="study-cert-org">U.S.M.C. Ministries</div>' +
        '<h1 class="study-cert-title">Certificate of Completion</h1>' +
        '<div class="study-cert-rule"></div>' +
        '<p class="study-cert-line">This certifies that</p>' +
        '<p class="study-cert-name">' + escapeHtml(name) + '</p>' +
        '<p class="study-cert-body">has read and studied <strong>' + escapeHtml(cfg.workTitle) + '</strong>' +
          (cfg.workSubtitle ? ', ' + escapeHtml(cfg.workSubtitle) + ',' : '') +
          ' &mdash; all ' + total + ' ' + cfg.labelPlural + ' &mdash; to the glory of God.</p>' +
        (cfg.certVerse ? '<p class="study-cert-verse">' + escapeHtml(cfg.certVerse) + '</p>' : '') +
        '<div class="study-cert-foot"><span>Completed ' + dateStr + '</span><span>usmcmin.org &middot; Soli Deo Gloria</span></div>' +
      '</div>';
    document.body.appendChild(cert);

    document.body.classList.add('study-printing-cert');
    const cleanup = function () { document.body.classList.remove('study-printing-cert'); window.removeEventListener('afterprint', cleanup); };
    window.addEventListener('afterprint', cleanup);
    window.print();
    setTimeout(cleanup, 1500); // fallback for browsers without afterprint
  }

  function escapeHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  window.StudyProgress = { init: init };
})();
