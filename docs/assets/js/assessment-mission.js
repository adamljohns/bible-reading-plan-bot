/**
 * USMC Ministries — shared mission timer + XP for template assessments.
 * Ported from proven-assessment.html (wall-clock timer, not decorative).
 */
(function (global) {
  'use strict';

  function init(d, helpers) {
    if (!d || !d.mission) return null;

    var axes = helpers.axes || d.axes || [];
    var getAxisAvg = helpers.getAxisAvg;
    var getRadarData = helpers.getRadarData;
    var onFormation = helpers.onFormationComplete || function () {};

    var xpKey = d.id + 'MissionXP';
    var selectedMinutes = d.mission.defaultDuration != null ? d.mission.defaultDuration : 18;
    var missionStarted = false;
    var timerEndMs = null;
    var timerPausedLeftMs = null;
    var timerRaf = null;
    var timerRunning = false;
    var xp = parseInt(localStorage.getItem(xpKey) || '0', 10) || 0;

    function $(id) { return document.getElementById(id); }

    function rankFromXp(x) {
      if (x >= 400) return 'Elder (XP)';
      if (x >= 250) return 'Leader (XP)';
      if (x >= 120) return 'Man (XP)';
      if (x >= 40) return 'Cadet (XP)';
      return 'Recruit';
    }

    function addXp(n) {
      xp += n;
      localStorage.setItem(xpKey, String(xp));
      updateXpUi();
    }

    function awardBadge(id) {
      var el = $('badge-' + id);
      if (el && !el.classList.contains('earned')) el.classList.add('earned');
    }

    function updateXpUi() {
      var fill = $('xpFill');
      var label = $('xpLabel');
      var rank = $('rankLabel');
      if (!fill || !label) return;
      var next = xp < 40 ? 40 : xp < 120 ? 120 : xp < 250 ? 250 : xp < 400 ? 400 : xp + 100;
      var prev = xp < 40 ? 0 : xp < 120 ? 40 : xp < 250 ? 120 : xp < 400 ? 250 : 400;
      var pct = Math.min(100, Math.round(((xp - prev) / Math.max(1, next - prev)) * 100));
      fill.style.width = pct + '%';
      label.textContent = xp + ' XP';
      if (rank) rank.textContent = rankFromXp(xp);
    }

    function drawTimerRing(frac) {
      var c = $('timerCanvas');
      if (!c) return;
      var ctx = c.getContext('2d');
      var w = c.width, h = c.height, cx = w / 2, cy = h / 2, rad = 52;
      ctx.clearRect(0, 0, w, h);
      ctx.beginPath();
      ctx.arc(cx, cy, rad, 0, Math.PI * 2);
      ctx.strokeStyle = '#333';
      ctx.lineWidth = 10;
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(cx, cy, rad, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * Math.max(0, Math.min(1, frac)));
      ctx.strokeStyle = frac < 0.15 ? '#c0392b' : '#D4AF37';
      ctx.lineWidth = 10;
      ctx.lineCap = 'round';
      ctx.stroke();
    }

    function renderTimerMs(left, total) {
      var s = Math.ceil(left / 1000);
      var m = Math.floor(s / 60);
      var r = s % 60;
      var disp = $('timerDisplay');
      if (disp) disp.textContent = String(m).padStart(2, '0') + ':' + String(r).padStart(2, '0');
      drawTimerRing(total > 0 ? left / total : 0);
    }

    function tickTimer() {
      if (!timerRunning || !timerEndMs) return;
      var left = timerEndMs - Date.now();
      var total = selectedMinutes * 60 * 1000;
      if (left <= 0) {
        renderTimerMs(0, total);
        timerRunning = false;
        var state = $('timerState');
        var phase = $('timerPhase');
        if (state) state.textContent = 'Expired';
        if (phase) phase.textContent = 'Clock hit zero — finish strong anyway.';
        var hud = $('mission-hud');
        if (hud) hud.classList.add('urgent');
        return;
      }
      renderTimerMs(left, total);
      var hud = $('mission-hud');
      if (hud) {
        if (left < 2 * 60 * 1000) hud.classList.add('urgent');
        else hud.classList.remove('urgent');
      }
      timerRaf = requestAnimationFrame(tickTimer);
    }

    function selectDuration(min, btn) {
      selectedMinutes = min;
      document.querySelectorAll('.dur-btn').forEach(function (b) { b.classList.remove('selected'); });
      if (btn) btn.classList.add('selected');
    }

    function startMission() {
      missionStarted = true;
      var hud = $('mission-hud');
      if (hud) hud.style.display = 'block';
      addXp(10);
      awardBadge('started');
      if (selectedMinutes > 0) {
        awardBadge('timer');
        timerEndMs = Date.now() + selectedMinutes * 60 * 1000;
        timerPausedLeftMs = null;
        timerRunning = true;
        addXp(10);
        var phase = $('timerPhase');
        if (phase) phase.textContent = 'Ends at ' + new Date(timerEndMs).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
        tickTimer();
      } else {
        var disp = $('timerDisplay');
        var state = $('timerState');
        var phase = $('timerPhase');
        var pause = $('btnPause');
        if (disp) disp.textContent = '∞';
        if (state) state.textContent = 'Open';
        if (phase) phase.textContent = 'Self-paced — no countdown';
        if (pause) pause.style.display = 'none';
        drawTimerRing(1);
      }
      updateXpUi();
      var briefing = $('briefing-screen');
      if (briefing) briefing.style.display = 'none';
    }

    function togglePause() {
      if (selectedMinutes <= 0) return;
      var btn = $('btnPause');
      var state = $('timerState');
      var phase = $('timerPhase');
      if (timerRunning) {
        timerPausedLeftMs = Math.max(0, timerEndMs - Date.now());
        timerRunning = false;
        timerEndMs = null;
        if (btn) btn.textContent = 'Resume';
        if (state) state.textContent = 'Paused';
        if (timerRaf) cancelAnimationFrame(timerRaf);
      } else {
        timerEndMs = Date.now() + (timerPausedLeftMs || 0);
        timerPausedLeftMs = null;
        timerRunning = true;
        if (btn) btn.textContent = 'Pause';
        if (state) state.textContent = 'Mission';
        if (phase) phase.textContent = 'Ends at ' + new Date(timerEndMs).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
        tickTimer();
      }
    }

    function addFiveMinutes() {
      if (selectedMinutes <= 0) return;
      if (timerRunning && timerEndMs) {
        timerEndMs += 5 * 60 * 1000;
        var phase = $('timerPhase');
        if (phase) phase.textContent = 'Ends at ' + new Date(timerEndMs).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }) + ' (+5)';
      } else if (timerPausedLeftMs != null) {
        timerPausedLeftMs += 5 * 60 * 1000;
        renderTimerMs(timerPausedLeftMs, selectedMinutes * 60 * 1000);
      }
    }

    function renderReadings(weakIndices) {
      var el = $('readingContent');
      var section = $('reading-plan');
      if (!el || !d.readings || !d.readings.length) return;
      el.innerHTML = '';
      var shown = {};
      weakIndices.forEach(function (idx) {
        if (shown[idx] || !d.readings[idx]) return;
        shown[idx] = true;
        var r = d.readings[idx];
        var axis = axes[idx];
        var card = document.createElement('div');
        card.className = 'read-card';
        card.innerHTML =
          '<h4>' + (axis ? axis.letter + ': ' + axis.word + ' — ' : '') + r.title + '</h4>' +
          (r.why ? '<p>' + r.why + '</p>' : '') +
          (r.start ? '<p class="read-meta"><strong>This week:</strong> ' + r.start + '</p>' : '') +
          (r.alsoHtml ? '<p class="read-meta">' + r.alsoHtml + '</p>' : '') +
          (r.link ? '<p><a href="' + r.link + '" target="_blank" rel="noopener">Open assignment →</a></p>' : '');
        el.appendChild(card);
      });
      if (section) section.style.display = 'block';
    }

    function renderConnect() {
      awardBadge('brother');
      var el = $('connectContent');
      var section = $('brotherhood');
      if (!el || !d.connectCards || !d.connectCards.length) return;
      el.innerHTML = d.connectCards.map(function (c) {
        return '<a class="connect-card" href="' + c.href + '" target="' + (c.external ? '_blank' : '_self') + '" rel="noopener">' +
          '<h4>' + c.title + '</h4><p>' + c.blurb + '</p></a>';
      }).join('');
      if (d.crossLinks && d.crossLinks.length) {
        el.innerHTML += '<p style="grid-column:1/-1;font-size:0.82rem;color:var(--gray);margin-top:8px;">Related assessments: ' +
          d.crossLinks.map(function (l) {
            return '<a href="' + l.href + '" style="color:var(--gold);margin-right:10px;">' + l.title + '</a>';
          }).join('') + '</p>';
      }
      if (section) section.style.display = 'block';
    }

    function pathwayButton(idx) {
      if (!d.pathway) return '';
      var week = (d.pathway.weekByAxisIndex && d.pathway.weekByAxisIndex[idx]) || (idx + 1);
      var anchor = (d.pathway.weekAnchors && d.pathway.weekAnchors[idx]) || ('week-' + week);
      var url = d.pathway.planUrl + '#' + anchor;
      var label = d.pathway.startLabel ? (d.pathway.startLabel + ' ' + week) : ('Start Week ' + week);
      return '<p style="margin-top:12px;"><a class="btn btn-primary" href="' + url + '" style="display:inline-block;text-decoration:none;">' + label + '</a></p>';
    }

    function wrapFormationComplete(weakIndices) {
      awardBadge('honest');
      awardBadge('plan');
      if (timerRunning && timerEndMs && timerEndMs > Date.now()) { addXp(40); awardBadge('finish'); }
      addXp(30);
      renderReadings(weakIndices);
      renderConnect();
      onFormation(weakIndices);
    }

    global.selectDuration = selectDuration;
    global.startMission = startMission;
    global.togglePause = togglePause;
    global.addFiveMinutes = addFiveMinutes;

    updateXpUi();

    return {
      startMission: startMission,
      renderReadings: renderReadings,
      renderConnect: renderConnect,
      wrapFormationComplete: wrapFormationComplete,
      pathwayButton: pathwayButton,
      isStarted: function () { return missionStarted; },
      ensureStarted: function () { if (!missionStarted) startMission(); }
    };
  }

  global.AssessmentMission = { init: init };
})(typeof window !== 'undefined' ? window : this);
