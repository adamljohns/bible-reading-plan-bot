/* follow-player.js — narration player for a page with read-scroll.js word follow.
 *
 * Markup (bin/verse-study-render.js writes it for any study that has audio):
 *   <div class="audio-slot" data-follow-player data-no-follow data-read-scroll-anchor>
 *     <audio controls preload="metadata"><source src="...mp3" type="audio/mpeg"></audio>
 *     <div class="audio-speed"><button class="audio-speed-btn" data-rate="1">…</button>…</div>
 *   </div>
 * plus <link rel="stylesheet" href="/assets/css/follow-player.css"> and, AFTER
 * this script, /assets/js/read-scroll.js (it mounts Word/Line/Page in the
 * .read-follow-host this script creates).
 *
 * What it adds to the readings player:
 *   - the same 1 / 1.25 / 1.5 / 2x chips, sharing the readings' saved rate;
 *   - a bottom mini bar (play/pause, time, seek, speed, Word/Line/Page) that
 *     slides up once the inline player leaves the screen or playback starts,
 *     because the page scrolls itself away from the inline controls while the
 *     voice is followed, and the top of the screen belongs to the site nav;
 *   - lock-screen title via the Media Session API.
 * Glyph-free icons (inline SVG): iOS turns the play-triangle character into an emoji.
 */
(function () {
  if (window.__followPlayerLoaded) return;
  window.__followPlayerLoaded = true;
  var slot = document.querySelector("[data-follow-player]");
  var audio = slot && slot.querySelector("audio");
  if (!audio) return;

  /* ── speed: same key, rates and snapping as the readings page ─────────── */
  var SPEED_KEY = "moop-readings-playback-rate";
  var RATES = [1, 1.25, 1.5, 2];
  function normalizeRate(v) {
    var n = parseFloat(v), best = 1, bestD = Infinity;
    if (!isFinite(n)) return 1;
    RATES.forEach(function (r) { var d = Math.abs(r - n); if (d < bestD) { best = r; bestD = d; } });
    return best;
  }
  var rate = 1;
  try { rate = normalizeRate(localStorage.getItem(SPEED_KEY) || "1"); } catch (e) {}
  function label(r) { return String(r).replace(/^1$/, "1") + "×"; }
  function applyRate(r) {
    rate = r;
    try { audio.playbackRate = r; } catch (e) {}
    Array.prototype.forEach.call(slot.querySelectorAll(".audio-speed-btn"), function (btn) {
      var on = Math.abs(normalizeRate(btn.getAttribute("data-rate")) - r) < 0.001;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
    if (rateBtn) { rateBtn.textContent = label(r); rateBtn.setAttribute("aria-label", "Playback speed " + r + " times"); }
  }
  function saveRate(r) { try { localStorage.setItem(SPEED_KEY, String(r)); } catch (e) {} }
  slot.addEventListener("click", function (ev) {
    var btn = ev.target.closest && ev.target.closest(".audio-speed-btn");
    if (!btn) return;
    ev.preventDefault();
    var r = normalizeRate(btn.getAttribute("data-rate"));
    saveRate(r);
    applyRate(r);
  });
  function reassert() { if (Math.abs(audio.playbackRate - rate) > 0.01) { try { audio.playbackRate = rate; } catch (e) {} } }
  audio.addEventListener("loadedmetadata", reassert);
  audio.addEventListener("play", reassert);

  /* ── mini bar ──────────────────────────────────────────────────────────── */
  var PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5v15a1 1 0 0 0 1.5.86l12-7.5a1 1 0 0 0 0-1.72l-12-7.5A1 1 0 0 0 7 4.5z"/></svg>';
  var PAUSE = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5.5" y="4" width="4.5" height="16" rx="1"/><rect x="14" y="4" width="4.5" height="16" rx="1"/></svg>';
  var bar = document.createElement("div");
  bar.className = "follow-mini";
  bar.setAttribute("role", "region");
  bar.setAttribute("aria-label", "Narration player");
  bar.setAttribute("data-follow-ui", "");
  bar.setAttribute("data-no-follow", "");
  bar.innerHTML =
    '<input type="range" class="follow-mini-scrub" min="0" max="1000" step="1" value="0" aria-label="Seek">' +
    '<div class="follow-mini-row">' +
    '<button type="button" class="follow-mini-play" aria-label="Play">' + PLAY + "</button>" +
    '<span class="follow-mini-time" aria-live="off">0:00</span>' +
    '<button type="button" class="follow-mini-rate">1×</button>' +
    '<div class="read-follow-host"></div>' +
    "</div>";
  document.body.appendChild(bar);
  var playBtn = bar.querySelector(".follow-mini-play");
  var timeEl = bar.querySelector(".follow-mini-time");
  var scrub = bar.querySelector(".follow-mini-scrub");
  var rateBtn = bar.querySelector(".follow-mini-rate");
  applyRate(rate);

  function fmt(s) {
    if (!isFinite(s) || s < 0) s = 0;
    s = Math.floor(s);
    var h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), x = s % 60;
    return (h ? h + ":" + (m < 10 ? "0" : "") : "") + m + ":" + (x < 10 ? "0" : "") + x;
  }
  var dragging = false;
  function dur() { return isFinite(audio.duration) && audio.duration > 0 ? audio.duration : 0; }
  function paintTime() {
    var d = dur();
    timeEl.textContent = fmt(audio.currentTime) + (d ? " / " + fmt(d) : "");
    if (!dragging && d) scrub.value = String(Math.round((audio.currentTime / d) * 1000));
  }
  var started = false;
  var slotVisible = true;
  function paintShown() {
    document.documentElement.classList.toggle("follow-mini-on", started || !slotVisible);
  }
  function paintPlay() {
    var on = !audio.paused && !audio.ended;
    playBtn.innerHTML = on ? PAUSE : PLAY;
    playBtn.setAttribute("aria-label", on ? "Pause" : "Play");
  }
  playBtn.addEventListener("click", function () {
    if (audio.paused || audio.ended) {
      var p = audio.play();
      if (p && p.catch) p.catch(function () {});
    } else audio.pause();
  });
  rateBtn.addEventListener("click", function () {
    var r = RATES[(RATES.indexOf(rate) + 1) % RATES.length];
    saveRate(r);
    applyRate(r);
  });
  scrub.addEventListener("input", function () {
    dragging = true;
    var d = dur();
    if (d) timeEl.textContent = fmt((scrub.value / 1000) * d) + " / " + fmt(d);
  });
  scrub.addEventListener("change", function () {
    var d = dur();
    if (d) audio.currentTime = (scrub.value / 1000) * d;
    dragging = false;
  });
  ["timeupdate", "durationchange", "loadedmetadata", "seeked"].forEach(function (n) { audio.addEventListener(n, paintTime); });
  ["play", "pause", "ended"].forEach(function (n) { audio.addEventListener(n, paintPlay); });
  audio.addEventListener("play", function () { started = true; paintShown(); });

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      slotVisible = entries[entries.length - 1].isIntersecting;
      paintShown();
    }).observe(slot);
  }

  /* Lock screen / Control Center title on iPhone. */
  if ("mediaSession" in navigator && window.MediaMetadata) {
    var h1 = document.querySelector("h1");
    try {
      navigator.mediaSession.metadata = new MediaMetadata({
        title: (h1 ? h1.textContent.trim() : document.title) + " — Verse Study",
        artist: "U.S.M.C. Ministries",
        album: "Deep Verse Studies"
      });
      navigator.mediaSession.setActionHandler("seekbackward", function () { audio.currentTime = Math.max(0, audio.currentTime - 15); });
      navigator.mediaSession.setActionHandler("seekforward", function () { audio.currentTime = Math.min(dur() || 1e9, audio.currentTime + 15); });
    } catch (e) {}
  }

  paintTime();
  paintPlay();
  paintShown();
  window.__followPlayer = { audio: audio, bar: bar };
})();
