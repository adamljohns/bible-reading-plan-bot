/**
 * USMC Ministries — Assessment Template Engine
 * Renders the full assessment page from structured data.
 * Each assessment page defines ASSESSMENT_DATA and calls AssessmentTemplate.render().
 *
 * Data contract:
 *   ASSESSMENT_DATA = {
 *     id: string           — used for localStorage keys
 *     title: string        — e.g., 'R.E.A.L. M.A.N.'
 *     subtitle: string     — e.g., 'The REAL M.A.N.'
 *     badge: string        — e.g., 'Men\'s Formation'
 *     tagline: string      — italic quote shown below the title
 *     navTitle: string     — e.g., 'Real Man Assessment'
 *     chartTitle: string   — e.g., 'R.E.A.L. M.A.N. Radar'
 *     shareTitle: string   — e.g., 'R.E.A.L. M.A.N. ASSESSMENT'
 *     shareUrl: string     — e.g., 'https://usmcmin.org/real-man-assessment.html'
 *     sharePartner: string — e.g., 'Accountability Partner'
 *     axes: [{
 *       letter: string     — e.g., 'R'
 *       word: string       — e.g., 'Reject Passivity'
 *       subword: string    — e.g., 'Leading, not waiting'
 *       summary: string    — shown as slider label
 *       text: string       — question body text
 *       questions: [string] — sub-questions (bulleted)
 *       scripture: string  — e.g., 'Ezekiel 22:30'
 *       rubrics: [{range, text}] — 4 tiers
 *       formation: {habit, prayer, convo, memory, memRef}
 *     }]
 *     scoring: {type: 'single'|'multi', defaultScore: number}
 *       single: one score per axis (AXIS_SCORES array)
 *       multi: one score per question (SCORES array)
 *     formationCount: number — how many weak areas to show (2 or 3)
 *     questionHeader: string — e.g., 'The Hard Questions'
 *     questionSub: string
 *     chartSub: string     — e.g., 'Rate yourself 1–10…'
 *     framingNote: string  — two-week framing text
 *     historyEmpty: string — empty history message
 *     formationSub: string — formation plan subtitle
 *     formationSubtitle: string
 *     historySub: string   — progress log subtitle
 *     tierNames: [[threshold, label, color], ...]
 *     weakLabel: string    — e.g., 'TOP 3 FOCUS AREAS:'
 *     shareLinkLabel: string — e.g., '🔗 Take the assessment:'
 *   }
 */
(function (global) {
  'use strict';

  var STORAGE_PREFIX = 'bte-theme';

  // ── Helpers ───────────────────────────────────────────────────────────
  function bibleHref(ref) {
    if (!ref) return 'bible.html';
    var cleaned = String(ref).replace(/\u2013|\u2014/g, '-').trim();
    return 'bible.html?ref=' + encodeURIComponent(cleaned);
  }

  function extractPassageLabel(memoryText, fallback) {
    if (!memoryText) return fallback || 'Open passage';
    var m = String(memoryText).match(/(?:—|–|-)\s*([A-Za-z0-9\s:.\-–—]+)\s*$/);
    if (m && m[1]) return m[1].trim();
    return fallback || 'Open passage';
  }

  function applyStoredTheme() {
    var s = localStorage.getItem(STORAGE_PREFIX);
    if (s === null) {
      s = localStorage.getItem('bteTheme');
      if (s !== null) localStorage.setItem(STORAGE_PREFIX, s);
    }
    if (s === 'light') document.body.classList.add('light-mode');
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
    try { var raw = localStorage.getItem(storageKey); var parsed = JSON.parse(raw || '[]'); return Array.isArray(parsed) ? parsed : []; }
    catch (e) { return []; }
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text).catch(function () { return fallbackCopy(text); });
    }
    return Promise.resolve(fallbackCopy(text));
  }

  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly', '');
    ta.style.position = 'fixed'; ta.style.left = '-9999px';
    document.body.appendChild(ta); ta.select();
    var ok = false; try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(ta); return ok;
  }

  function stripHtml(s) {
    return String(s || '').replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();
  }

  // ── Nav HTML ──────────────────────────────────────────────────────────
  function navHtml(activeLabel, activeHref) {
    return '<nav>\n' +
      '    <a href="index.html"><img src="assets/icons/shield-home-48.png" class="site-icon" alt="" width="16" height="16"> U.S.M.C. Ministries Home</a>\n' +
      '    <a href="watchman.html"><img src="assets/icons/shield-bible.png" class="site-icon" alt="" width="16" height="16"> Watchman Bible Plan</a>\n' +
      '    <a href="bible.html"><img src="assets/icons/shield-bible-cross-48.png" class="site-icon" alt="" width="16" height="16"> Bible Translation Engine</a>\n' +
      '    <a href="assessments.html"><img src="assets/icons/shield-checklist-48.png" class="site-icon" alt="" width="16" height="16"> Assessments</a>\n' +
      (activeLabel ? '<a href="' + activeHref + '" class="active">' + activeLabel + '</a>' : '') +
      '    <a href="connect.html"><img src="assets/icons/shield-handshake.png" class="site-icon" alt="" width="16" height="16"> Connect</a>\n' +
      '<div class="bte-theme-toggle nav-theme-toggle" onclick="bteToggleTheme()" title="Toggle dark/light mode">\n' +
      '        <span class="toggle-icon moon-icon">\uD83C\uDF19</span>\n' +
      '        <div class="toggle-track"><div class="toggle-knob"></div></div>\n' +
      '        <span class="toggle-icon sun-icon">\u2600\uFE0F</span>\n' +
      '    </div></nav>';
  }

  // ── Build questions block ─────────────────────────────────────────────
  function buildQuestions(d, axes) {
    var block = document.getElementById('questionsBlock');
    axes.forEach(function (axis, i) {
      var subQHtml = axis.questions ? axis.questions.map(function (q) { return '<li>' + q + '</li>'; }).join('') : '';
      var div = document.createElement('div');
      div.className = 'question-block';
      div.innerHTML =
        '<div class="q-header">' +
          '<div class="q-letter">' + axis.letter + '</div>' +
          '<div class="q-meta">' +
            '<div class="q-word">' + axis.word + (axis.subword ? ' <span class="q-subword">— ' + axis.subword + '</span>' : '') + '</div>' +
          '</div>' +
        '</div>' +
        '<div class="q-text">' + axis.text + '</div>' +
        (subQHtml ? '<ul class="q-subquestions">' + subQHtml + '</ul>' : '') +
        '<a class="q-scripture" href="' + bibleHref(axis.scripture) + '" target="_blank" rel="noopener">' +
          '<img src="assets/icons/shield-bible.png" alt="" width="16" height="16" style="vertical-align:middle;margin-right:3px;"> ' + axis.scripture +
        '</a>';
      block.appendChild(div);
    });
  }

  // ── Build chart ───────────────────────────────────────────────────────
  var RADAR_CHART_REF = null;

  function buildChart(d, axes, getScoreData) {
    var ctx = document.getElementById('radarChart').getContext('2d');
    var isLight = document.body.classList.contains('light-mode');
    RADAR_CHART_REF = new Chart(ctx, {
      type: 'radar',
      data: {
        labels: axes.map(function (a) { return a.letter; }),
        datasets: [{
          label: 'Your Score',
          data: getScoreData(),
          backgroundColor: 'rgba(212,175,55,0.18)',
          borderColor: '#D4AF37',
          borderWidth: 2.5,
          pointBackgroundColor: '#D4AF37',
          pointRadius: 5,
          pointHoverRadius: 7
        }]
      },
      options: {
        responsive: true,
        animation: { duration: 200 },
        scales: {
          r: {
            min: 0, max: 10,
            ticks: { stepSize: 2, color: isLight ? '#666' : '#888', backdropColor: 'transparent', font: { size: 11 } },
            grid: { color: isLight ? '#ddd' : '#2a2a2a' },
            angleLines: { color: isLight ? '#ccc' : '#333' },
            pointLabels: {
              color: '#D4AF37',
              font: { size: 13, family: 'Playfair Display, serif', weight: '700' }
            }
          }
        },
        plugins: { legend: { display: false } }
      }
    });
  }

  function updateChartTheme(isLight) {
    if (!RADAR_CHART_REF) return;
    var r = RADAR_CHART_REF.options.scales.r;
    r.grid.color = isLight ? '#ddd' : '#2a2a2a';
    r.angleLines.color = isLight ? '#ccc' : '#333';
    r.ticks.color = isLight ? '#666' : '#888';
    RADAR_CHART_REF.update('none');
  }

  function updateChart(d, axes, getScoreData, getOverall, getTier) {
    RADAR_CHART_REF.data.datasets[0].data = getScoreData();
    RADAR_CHART_REF.update();
    var avg = getOverall();
    document.getElementById('overallScore').textContent = avg.toFixed(1);
    var tier = getTier(avg);
    var el = document.getElementById('scoreTier');
    el.textContent = tier.label;
    el.style.color = tier.color;
  }

  // ── Build sliders ─────────────────────────────────────────────────────
  function buildSliders(d, axes, getAxisAvg, onSliderCb) {
    var grid = document.getElementById('sliderGrid');
    axes.forEach(function (axis, i) {
      var rubricRows = axis.rubrics.map(function (r) {
        return '<div class="rubric-row"><span class="rubric-range">' + r.range + '</span> <span class="rubric-text">' + r.text + '</span></div>';
      }).join('');
      var block = document.createElement('div');
      block.className = 'axis-block';
      block.innerHTML =
        '<div class="axis-block-header">' +
          '<span class="axis-letter-label">' + axis.letter + '</span>' +
          '<span class="axis-name">' + axis.word + '</span>' +
          (axis.subword ? '<span class="axis-sub">— ' + axis.subword + '</span>' : '') +
          '<span class="axis-avg" id="avg-' + i + '">' + getAxisAvg(i).toFixed(1) + '</span>' +
        '</div>' +
        '<div class="slider-row">' +
          '<div class="slider-label">' +
            '<span class="label-text">' + axis.summary + '</span>' +
            '<span class="score-val" id="val-' + i + '">' + getAxisAvg(i) + '</span>' +
          '</div>' +
          '<input type="range" min="1" max="10" value="' + getAxisAvg(i) + '"' +
            ' id="slider-' + i + '"' +
            ' oninput="onSlider(' + i + ', this.value)"' +
            ' aria-label="' + axis.word + ' score">' +
        '</div>' +
        '<button class="rubric-toggle" id="rtoggle-' + i + '" onclick="toggleRubric(' + i + ')" type="button">' +
          '<span class="rtri">\u25B6</span> What does this score mean?' +
        '</button>' +
        '<div class="rubric-body" id="rbody-' + i + '">' + rubricRows + '</div>';
      grid.appendChild(block);
    });
  }

  // ── Build formation plan ──────────────────────────────────────────────
  function buildFormationPlan(d, axes, getAxisAvg, getScoreData) {
    var indexed = axes.map(function (_, i) { return { s: getAxisAvg(i), i: i }; }).sort(function (a, b) { return a.s - b.s; });
    var weak = [];
    var count = d.formationCount || 3;
    for (var w = 0; w < count && w < indexed.length; w++) weak.push(indexed[w].i);

    var plan = document.getElementById('formation-plan');
    var content = document.getElementById('formationContent');
    content.innerHTML = '';

    weak.forEach(function (idx, rank) {
      var axis = axes[idx];
      var f = axis.formation;
      var div = document.createElement('div');
      div.className = 'formation-area';
      var memLabel = extractPassageLabel(f.memory, f.word || 'Scripture');
      var memRef = f.memRef || '';
      div.innerHTML =
        '<h3><img src="assets/icons/shield-chain-sword-48.png" alt="" width="16" height="16" style="vertical-align:middle;margin-right:3px;"> #' + (rank + 1) + ' Priority \u2014 ' + axis.letter + ': ' + axis.word + ' <span style="font-size:0.8rem;color:var(--gray);font-weight:400">(Avg: ' + getAxisAvg(idx).toFixed(1) + '/10)</span></h3>' +
        '<div class="formation-item">' +
          '<div class="formation-icon"><img src="assets/icons/shield-calendar.png" alt="" width="16" height="16" style="vertical-align:middle;margin-right:3px;"></div>' +
          '<div><div class="formation-label">This Week\'s Micro-Habit</div><div class="formation-text">' + f.habit + '</div></div>' +
        '</div>' +
        '<div class="formation-item">' +
          '<div class="formation-icon">\uD83D\uDE4F</div>' +
          '<div><div class="formation-label">Prayer Prompt</div><div class="formation-text">' + f.prayer + '</div></div>' +
        '</div>' +
        '<div class="formation-item">' +
          '<div class="formation-icon"><img src="assets/icons/shield-broadcast-48.png" alt="" width="16" height="16" style="vertical-align:middle;margin-right:3px;"></div>' +
          '<div><div class="formation-label">Conversation Starter</div><div class="formation-text">' + f.convo + '</div></div>' +
        '</div>' +
        '<div class="formation-item">' +
          '<div class="formation-icon"><img src="assets/icons/shield-bible.png" alt="" width="16" height="16" style="vertical-align:middle;margin-right:3px;"></div>' +
          '<div><div class="formation-label">Scripture to Memorize</div><div class="formation-text">' + f.memory + '</div>' +
            (memRef ? '<a class="formation-scripture" href="' + bibleHref(f.memRef) + '" target="_blank" rel="noopener">' + memLabel + ' \u2192</a>' : '') +
          '</div>' +
        '</div>';
      content.appendChild(div);
    });

    plan.style.display = 'block';
    plan.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // Auto-persist
    try {
      var history = getHistory(d.id + 'History');
      history.unshift({ date: new Date().toISOString(), scores: getScoreData() });
      if (history.length > 20) history = history.slice(0, 20);
      localStorage.setItem(d.id + 'History', JSON.stringify(history));
      if (typeof renderHistory === 'function') renderHistory();
    } catch (e) {}
  }

  // ── Build progress history ────────────────────────────────────────────
  function buildHistory(d, axes) {
    var history = getHistory(d.id + 'History');
    var el = document.getElementById('progressContent');
    if (!history.length) {
      el.innerHTML = '<p id="no-history" style="color:var(--gray);font-size:0.9rem;font-style:italic;">' + (d.historyEmpty || 'No previous assessments on this device.') + '</p>';
      return;
    }
    var latest = history[0];
    var prev = history[1] || null;

    var html = '<p style="font-size:0.92rem; color:var(--gray-mid); margin-bottom:12px;">' +
      'Last assessment: <strong style="color:var(--white)">' + weeksAgo(latest.date) + '</strong>' +
      (prev ? ' \u2014 Previous: ' + weeksAgo(prev.date) : '') +
      '</p>';

    html += '<div class="history-card"><div class="history-meta">' + new Date(latest.date).toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) + '</div><div class="history-scores">';
    axes.forEach(function (a, i) {
      var cur = latest.scores[i] !== undefined ? parseFloat(latest.scores[i]).toFixed(1) : '\u2014';
      var old = (prev && prev.scores[i] !== undefined) ? parseFloat(prev.scores[i]) : null;
      var delta = '';
      if (old !== null && cur !== '\u2014') {
        var diff = parseFloat(cur) - old;
        if (diff > 0.05) delta = '<div class="delta up">\u25B2' + diff.toFixed(1) + '</div>';
        else if (diff < -0.05) delta = '<div class="delta down">\u25BC' + Math.abs(diff).toFixed(1) + '</div>';
        else delta = '<div class="delta same">\u2014</div>';
      }
      html += '<div class="history-badge"><div class="h-letter">' + a.letter + '</div><div class="h-score">' + cur + '</div>' + delta + '</div>';
    });
    html += '</div></div>';

    if (history.length > 1) {
      html += '<details style="margin-top:14px;"><summary style="cursor:pointer;color:var(--gray);font-size:0.85rem;">View full history (' + history.length + ' entries)</summary>';
      history.slice(1).forEach(function (h) {
        html += '<div class="history-card" style="margin-top:8px;">' +
          '<div class="history-meta">' + new Date(h.date).toLocaleDateString('en-US', { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' }) + '</div>' +
          '<div class="history-scores">';
        axes.forEach(function (a, i) {
          html += '<div class="history-badge"><div class="h-letter">' + a.letter + '</div><div class="h-score">' + (h.scores[i] !== undefined ? parseFloat(h.scores[i]).toFixed(1) : '\u2014') + '</div></div>';
        });
        html += '</div></div>';
      });
      html += '</details>';
    }
    el.innerHTML = html;
  }

  // ── Share modal ───────────────────────────────────────────────────────
  var shareModalRef = null;
  var shareModalWire = null;

  function buildShareModal(d) {
    var modalId = 'share-modal';
    var modal = document.getElementById(modalId);
    if (!modal) return;
    var ta = modal.querySelector('textarea');
    if (ta) ta.setAttribute('rows', '16');

    function close() {
      modal.classList.remove('open');
      document.body.classList.remove('modal-open');
    }
    function open() {
      modal.classList.add('open');
      document.body.classList.add('modal-open');
      if (ta) { setTimeout(function () { ta.focus(); ta.select(); }, 30); }
    }

    modal.addEventListener('click', function (e) { if (e.target === modal) close(); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modal.classList.contains('open')) close();
    });

    window.openShareModal = function () {
      var avg = getOverallAvg();
      var tier = getTier(avg);
      var date = new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
      var text = (d.shareTitle || d.title) + ' ASSESSMENT \u2014 ' + date + '\n';
      text += '='.repeat(42) + '\n\n';
      text += 'Overall Score: ' + avg.toFixed(1) + '/10  \u2014  ' + stripHtml(tier.label) + '\n\n';
      ASSESSMENT_DATA.axes.forEach(function (a, i) {
        text += a.letter + ' \u2014 ' + a.word + ': ' + getAxisAvg(i).toFixed(1) + '/10\n';
      });
      var indexed = ASSESSMENT_DATA.axes.map(function (_, i) { return { s: getAxisAvg(i), i: i }; }).sort(function (a, b) { return a.s - b.s; });
      var weakCount = d.formationCount || 3;
      var weakLabels = d.weakLabel || 'TOP ' + weakCount + ' FOCUS AREAS:';
      text += '\n\U0001F4CC ' + weakLabels + '\n';
      for (var w = 0; w < weakCount && w < indexed.length; w++) {
        var idx = indexed[w].i;
        text += '\u2022 ' + ASSESSMENT_DATA.axes[idx].letter + ' \u2014 ' + ASSESSMENT_DATA.axes[idx].word + ' (' + getAxisAvg(idx).toFixed(1) + '/10)\n';
      }
      text += '\n' + (d.shareLinkLabel || '\U0001F517 Take the assessment:') + ' ' + (d.shareUrl || window.location.href) + '\n';
      text += '\n[Shared via USMC Ministries ' + d.shareTitle + ']';
      ta.value = text;
      open();
    };

    window.closeShareModal = close;
  }

  function copyShareText(evt) {
    var modal = document.getElementById('share-modal');
    if (!modal) return;
    var ta = modal.querySelector('textarea');
    if (!ta) return;
    ta.select();
    copyText(ta.value).then(function () {
      var btn = (evt && evt.currentTarget) || null;
      if (btn) {
        var prev = btn.textContent;
        btn.textContent = 'Copied';
        setTimeout(function () { btn.textContent = prev; }, 2000);
      }
    }).catch(function () {
      var btn = (evt && evt.currentTarget) || null;
      if (btn) {
        var prev = btn.textContent;
        btn.textContent = 'Copied';
        setTimeout(function () { btn.textContent = prev; }, 2000);
      }
    });
  }

  function saveProgress(evt) {
    var history = getHistory(ASSESSMENT_DATA.id + 'History');
    history.unshift({ date: new Date().toISOString(), scores: getRadarData() });
    if (history.length > 20) history = history.slice(0, 20);
    localStorage.setItem(ASSESSMENT_DATA.id + 'History', JSON.stringify(history));
    renderHistory();
    var btn = (evt && evt.currentTarget) || null;
    if (btn) {
      var prev = btn.textContent;
      btn.textContent = 'Saved';
      setTimeout(function () { btn.textContent = prev; }, 2000);
    }
  }

  function toggleRubric(i) {
    var body = document.getElementById('rbody-' + i);
    var toggle = document.getElementById('rtoggle-' + i);
    var isOpen = body.classList.contains('open');
    body.classList.toggle('open', !isOpen);
    toggle.classList.toggle('open', !isOpen);
  }

  function runAssessment() {
    buildFormationPlan(ASSESSMENT_DATA, ASSESSMENT_DATA.axes, getAxisAvg, getRadarData);
  }

  function printSummary() {
    window.print();
  }

  // ── Theme toggle ──────────────────────────────────────────────────────
  var _radarChartRef = null;
  function bteToggleTheme() {
    document.body.classList.toggle('light-mode');
    var isLight = document.body.classList.contains('light-mode');
    localStorage.setItem(STORAGE_PREFIX, isLight ? 'light' : 'dark');
    if (_radarChartRef) updateChartTheme(isLight);
  }

  // ── Render ────────────────────────────────────────────────────────────
  function render(ASSESSMENT_DATA) {
    window.ASSESSMENT_DATA = ASSESSMENT_DATA;

    // Apply stored theme
    applyStoredTheme();

    // Helper functions for the template
    window.getAxisAvg = function getAxisAvg(i) { return ASSESSMENT_DATA.axisScores[i]; };
    window.getRadarData = function getRadarData() { return ASSESSMENT_DATA.axes.map(function (_, i) { return getAxisAvg(i); }); };
    window.getOverallAvg = function getOverallAvg() { var d = getRadarData(); return d.reduce(function (a, b) { return a + b; }, 0) / d.length; };
    window.getTier = function getTier(avg) {
      var tiers = ASSESSMENT_DATA.tierNames || [
        [9, 'Walking in Strength', '#27ae60'],
        [7, 'Gaining Ground', '#2ecc71'],
        [4, 'In the Fight', '#D4AF37'],
        [0, 'Under Siege', '#c0392b']
      ];
      for (var t = 0; t < tiers.length; t++) { if (avg >= tiers[t][0]) return { label: tiers[t][1], color: tiers[t][2] }; }
      return { label: tiers[tiers.length - 1][1], color: tiers[tiers.length - 1][2] };
    };

    // On-slider handler
    window.onSlider = function onSlider(axisIdx, val) {
      ASSESSMENT_DATA.axisScores[axisIdx] = parseInt(val);
      document.getElementById('val-' + axisIdx).textContent = val;
      document.getElementById('avg-' + axisIdx).textContent = getAxisAvg(axisIdx).toFixed(1);
      updateChart();
    };

    // Build DOM
    var body = document.body;

    // Inject nav
    var nav = document.createElement('nav');
    var activeLabel = ASSESSMENT_DATA.navTitle || ASSESSMENT_DATA.title;
    var activeHref = ASSESSMENT_DATA.navTitle ? undefined : undefined;
    nav.innerHTML = navHtml(ASSESSMENT_DATA.title, '');
    body.insertBefore(nav, body.firstChild);

    // Build title/hero
    var hero = document.createElement('div');
    hero.className = 'hero';
    hero.innerHTML =
      '<div class="hero-badge">' + ASSESSMENT_DATA.badge + '</div>' +
      '<h1>The <span>' + ASSESSMENT_DATA.title + '</span></h1>' +
      '<div class="acronym-row">' +
        ASSESSMENT_DATA.axes.map(function (a) {
          return '<div class="acronym-pill"><span class="acronym-letter">' + a.letter + '</span><span class="acronym-word">' + a.word + '</span></div>';
        }).join('') +
      '</div>' +
      '<p class="tagline">' + ASSESSMENT_DATA.tagline + '</p>';
    body.appendChild(hero);

    // Build main wrapper
    var main = document.createElement('main');

    // Questions section
    var qCard = document.createElement('div');
    qCard.className = 'section-card';
    qCard.innerHTML =
      '<div class="section-title"><div class="dot"></div><div><h2>' + (ASSESSMENT_DATA.questionHeader || 'The Hard Questions') + '</h2><div class="subtitle">' + (ASSESSMENT_DATA.questionSub || 'Read each one slowly. Sit with it. Answer what\'s actually true, not what you wish were true.') + '</div></div></div>' +
      '<div id="questionsBlock"></div>';
    main.appendChild(qCard);

    // Chart + Sliders section
    var csCard = document.createElement('div');
    csCard.className = 'section-card';
    csCard.innerHTML =
      '<div class="section-title"><div class="dot"></div><div><h2>' + ASSESSMENT_DATA.chartTitle + '</h2><div class="subtitle">' + ASSESSMENT_DATA.chartSub + '</div></div></div>' +
      '<div class="framing-note">\u23F1 Rate yourself based on the <strong>PAST TWO WEEKS</strong> \u2014 not your best day, not your best intentions. Where have you actually been?</div>' +
      '<div class="chart-wrapper"><canvas id="radarChart"></canvas></div>' +
      '<div class="overall-score-wrap">' +
        '<div class="overall-score-num" id="overallScore">\u2014</div>' +
        '<div class="overall-score-label">Overall Score / 10</div>' +
        '<div class="score-tier" id="scoreTier"></div>' +
      '</div>' +
      '<div class="slider-grid" id="sliderGrid"></div>' +
      '<div class="btn-row" id="print-hide">' +
        '<button class="btn btn-primary" onclick="runAssessment()">\u2705 Generate Formation Plan</button>' +
        '<button class="btn btn-ghost" onclick="saveProgress(event)">\uD83D\uDCBE Save Progress</button>' +
      '</div>';
    main.appendChild(csCard);

    // Formation Plan section
    var fCard = document.createElement('div');
    fCard.className = 'section-card';
    fCard.id = 'formation-plan';
    fCard.style.display = 'none';
    fCard.innerHTML =
      '<div class="section-title"><div class="dot"></div><div><h2>Formation Plan</h2><div class="subtitle">' + (ASSESSMENT_DATA.formationSubtitle || 'Your ' + (ASSESSMENT_DATA.formationCount || 3) + ' weakest areas. Micro-habits, prayers, and conversation starters. No excuses.') + '</div></div></div>' +
      '<div id="formationContent"></div>' +
      '<div class="btn-row" id="print-hide2">' +
        '<button class="btn btn-outline" onclick="printSummary()">\uD83D\uDDA8\uFE0F Print Summary</button>' +
        '<button class="btn btn-ghost" onclick="openShareModal()">\uD83D\uDCE4 Share with ' + (ASSESSMENT_DATA.sharePartner || 'Accountability Partner') + '</button>' +
        (ASSESSMENT_DATA.extraButtons || '') +
      '</div>';
    main.appendChild(fCard);

    // Progress section
    var pCard = document.createElement('div');
    pCard.className = 'section-card';
    pCard.innerHTML =
      '<div class="section-title"><div class="dot"></div><div><h2>Progress Log</h2><div class="subtitle">' + ASSESSMENT_DATA.historySub + '</div></div></div>' +
      '<div id="progressContent"><p id="no-history" style="color:var(--gray);font-size:0.9rem;font-style:italic;">' + (ASSESSMENT_DATA.historyEmpty || 'No previous assessments on this device.') + '</p></div>';
    main.appendChild(pCard);

    body.appendChild(main);

    // Share modal
    buildShareModal(ASSESSMENT_DATA);

    // Build all
    buildQuestions(ASSESSMENT_DATA, ASSESSMENT_DATA.axes);
    buildChart(ASSESSMENT_DATA, ASSESSMENT_DATA.axes, getRadarData);
    _radarChartRef = RADAR_CHART_REF;
    buildSliders(ASSESSMENT_DATA, ASSESSMENT_DATA.axes, getAxisAvg, null);

    // Restore history
    renderHistory = function renderHistory() { buildHistory(ASSESSMENT_DATA, ASSESSMENT_DATA.axes); };
    renderHistory();

    // Wire up updateChart
    function updateChart() {
      updateChart(ASSESSMENT_DATA, ASSESSMENT_DATA.axes, getRadarData, getOverallAvg, getTier);
    }

    // Expose to window
    window.updateChart = updateChart;
  }

  global.AssessmentTemplate = { render: render };
})(typeof window !== 'undefined' ? window : this);
