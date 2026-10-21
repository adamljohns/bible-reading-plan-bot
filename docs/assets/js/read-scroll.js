/* Daily-reading auto-scroll. Slow, Steady, Brisk, March.
   Word, Line, and Page follow the spoken word when a word-time file exists.
   No clock-guess highlight. A finger or wheel pauses the walk. */
(function () {
  if (window.__readScrollLoaded) return;
  window.__readScrollLoaded = true;
  if (!document.querySelector("section.watch")) return;

  if (!document.getElementById("read-scroll-css")) {
    var style = document.createElement("style");
    style.id = "read-scroll-css";
    style.textContent = [
      ".read-scroll-bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:0 0 16px;position:relative;z-index:25;background:#000;padding:8px 0}",
      "html.read-scroll-on .read-scroll-bar{position:absolute;width:1px;height:1px;margin:0;padding:0;overflow:hidden;clip:rect(0 0 0 0);opacity:0;pointer-events:none}",
      ".read-scroll-dock{display:none;position:fixed;top:max(8px,env(safe-area-inset-top));right:10px;z-index:40;gap:6px;align-items:center}",
      "html.read-scroll-on .read-scroll-dock{display:flex}",
      ".read-scroll-slower,.read-scroll-faster,.read-scroll-stop{min-height:36px;min-width:36px;padding:6px 10px;border-radius:999px;border:1px solid #D4AF37;background:#111;color:#D4AF37;font-family:Inter,system-ui,sans-serif;font-size:.85rem;font-weight:700}",
      ".read-scroll-dock-name{color:#D4AF37;font-size:.75rem;font-weight:700;min-width:52px;text-align:center}",
      ".read-scroll-toggle,.read-scroll-follow{appearance:none;-webkit-appearance:none;min-height:44px;padding:8px 14px;border-radius:999px;border:1px solid #333;background:#111;color:#888;font-family:Inter,system-ui,sans-serif;font-size:.85rem;font-weight:600}",
      ".read-scroll-toggle.is-on,.read-scroll-follow.is-on{background:#D4AF37;color:#000;border-color:#D4AF37}",
      ".read-scroll-speed{display:flex;flex-direction:column;gap:4px;min-width:180px;flex:1 1 180px;color:#888;font-size:.75rem}",
      ".read-scroll-speed-name{color:#D4AF37;font-weight:700;font-size:.85rem}",
      ".read-scroll-speed input{width:100%;accent-color:#D4AF37;min-height:44px}",
      ".read-scroll-ticks{display:flex;justify-content:space-between;color:#888}",
      ".watch-word.is-hot{background:#D4AF37;color:#000;border-radius:3px}",
      ".read-word-line{display:none;position:fixed;height:2px;background:#D4AF37;pointer-events:none;z-index:26}",
      "html.read-line-on .read-word-line{display:block}",
      ".read-follow-dock{display:flex;position:fixed;top:max(8px,env(safe-area-inset-top));left:10px;z-index:40;gap:6px}",
      ".read-follow-word,.read-follow-line,.read-follow-screen{min-height:32px;padding:4px 8px;border-radius:999px;border:1px solid #333;background:#111;color:#888;font-family:Inter,system-ui,sans-serif;font-size:.72rem;font-weight:700}",
      ".read-follow-word.is-on,.read-follow-line.is-on,.read-follow-screen.is-on{background:#D4AF37;color:#000;border-color:#D4AF37}",
      "@media (prefers-reduced-motion:reduce){.read-scroll-bar{display:none}}"
    ].join("");
    document.head.appendChild(style);
  }

  var KEY = "moop-read-scroll-v1";
  var SPEEDS = [
    { id: "slow", label: "Slow", px: 22 },
    { id: "steady", label: "Steady", px: 42 },
    { id: "brisk", label: "Brisk", px: 72 },
    { id: "march", label: "March", px: 110 }
  ];
  var REDUCE = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function speedIndex(id) {
    for (var i = 0; i < SPEEDS.length; i++) if (SPEEDS[i].id === id) return i;
    return 1;
  }
  function readPref() {
    try {
      var raw = JSON.parse(localStorage.getItem(KEY) || "{}");
      var speed = speedIndex(raw.speed) >= 0 && SPEEDS.some(function (s) { return s.id === raw.speed; }) ? raw.speed : "steady";
      return { on: !!raw.on, speed: speed, word: raw.word !== false, line: raw.line !== false, screen: raw.screen !== false };
    } catch (e) {
      return { on: false, speed: "steady", word: true, line: true, screen: true };
    }
  }
  function writePref(p) {
    try { localStorage.setItem(KEY, JSON.stringify(p)); } catch (e) {}
  }

  var pref = readPref();
  if (REDUCE) pref.on = false;
  var pendingPx = 0;
  var raf = 0;
  var last = 0;
  var userHoldUntil = 0;
  var words = [];
  var marks = null;
  var aligned = {};

  var bar = document.createElement("div");
  bar.className = "read-scroll-bar";
  bar.setAttribute("role", "group");
  bar.setAttribute("aria-label", "Auto scroll");
  bar.innerHTML =
    '<button type="button" class="read-scroll-toggle" aria-pressed="false">Scroll</button>' +
    '<label class="read-scroll-speed" hidden>Speed <span class="read-scroll-speed-name">Steady</span>' +
    '<input type="range" min="0" max="3" step="1" value="1" aria-label="Scroll speed" aria-valuemin="0" aria-valuemax="3" aria-valuetext="Steady">' +
    '<span class="read-scroll-ticks"><span>Slow</span><span>Steady</span><span>Brisk</span><span>March</span></span></label>' +
    '<button type="button" class="read-scroll-follow" aria-pressed="true" hidden>Follow voice</button>';
  var copyBar = document.querySelector(".copy-bar");
  if (copyBar) copyBar.insertAdjacentElement("afterend", bar);
  else {
    var box = document.querySelector(".container") || document.body;
    box.insertBefore(bar, box.firstChild);
  }

  var toggle = bar.querySelector(".read-scroll-toggle");
  var speedLabel = bar.querySelector(".read-scroll-speed");
  var slider = speedLabel.querySelector("input");
  var speedName = bar.querySelector(".read-scroll-speed-name");
  var followBtn = bar.querySelector(".read-scroll-follow");
  var dock = document.createElement("div");
  dock.className = "read-scroll-dock";
  dock.innerHTML = '<button type="button" class="read-scroll-slower" aria-label="Slower">\u2212</button><span class="read-scroll-dock-name">Steady</span><button type="button" class="read-scroll-faster" aria-label="Faster">+</button><button type="button" class="read-scroll-stop">Stop</button>';
  document.body.appendChild(dock);
  var slowerBtn = dock.querySelector(".read-scroll-slower");
  var fasterBtn = dock.querySelector(".read-scroll-faster");
  var dockName = dock.querySelector(".read-scroll-dock-name");
  var stopBtn = dock.querySelector(".read-scroll-stop");
  var followDock = document.createElement("div");
  followDock.className = "read-follow-dock";
  followDock.innerHTML = '<button type="button" class="read-follow-word">Word</button><button type="button" class="read-follow-line">Line</button><button type="button" class="read-follow-screen">Page</button>';
  document.body.appendChild(followDock);
  var lineEl = document.createElement("div");
  lineEl.className = "read-word-line";
  lineEl.setAttribute("aria-hidden", "true");
  document.body.appendChild(lineEl);

  function guideY() {
    var tabs = document.querySelector(".watch-tabs");
    var floor = tabs ? tabs.getBoundingClientRect().bottom + 36 : 140;
    return Math.max(floor + 48, Math.round(window.innerHeight * 0.46));
  }
  function activeSection() {
    var hash = (location.hash || "").replace("#", "");
    if (hash && hash !== "all") {
      var hashed = document.getElementById(hash);
      if (hashed) return hashed;
    }
    var sections = Array.prototype.slice.call(document.querySelectorAll("section.watch"));
    var mark = window.innerHeight * 0.28;
    var best = sections[0];
    sections.forEach(function (s) {
      var r = s.getBoundingClientRect();
      if (r.top < mark && r.bottom > 80) best = s;
    });
    return best;
  }

  function wrapWords(root) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        var p = node.parentElement;
        if (!p || p.closest("button, audio, script, style, .read-scroll-bar, .audio-speed")) return NodeFilter.FILTER_REJECT;
        if (p.classList && p.classList.contains("watch-word")) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function (node) {
      var frag = document.createDocumentFragment();
      node.nodeValue.split(/(\s+)/).forEach(function (part) {
        if (!part) return;
        if (!part.trim()) {
          frag.appendChild(document.createTextNode(part));
          return;
        }
        var span = document.createElement("span");
        span.className = "watch-word";
        span.textContent = part;
        frag.appendChild(span);
        words.push(span);
      });
      node.parentNode.replaceChild(frag, node);
    });
  }
  Array.prototype.forEach.call(document.querySelectorAll("section.watch"), wrapWords);

  function norm(s) {
    return String(s || "").toLowerCase().replace(/[^a-z0-9']/g, "");
  }
  function clearHot() {
    Array.prototype.forEach.call(document.querySelectorAll(".watch-word.is-hot"), function (el) {
      el.classList.remove("is-hot");
    });
  }
  function hideLine() {
    document.documentElement.classList.remove("read-line-on");
  }
  function playingAudio() {
    return Array.prototype.slice.call(document.querySelectorAll("audio")).find(function (a) {
      return !a.paused && !a.ended && a.currentTime > 0;
    }) || null;
  }
  function alignSection(section, spoken) {
    var spans = words.filter(function (w) { return section.contains(w); });
    var si = 0;
    var pairs = [];
    (spoken || []).forEach(function (sp) {
      var target = norm(sp.w);
      if (target.length < 3) return;
      var found = -1;
      var limit = Math.min(spans.length, si + 18);
      for (var j = si; j < limit; j++) {
        if (norm(spans[j].textContent) === target) { found = j; break; }
      }
      if (found >= 0) {
        pairs.push({ t: sp.t, el: spans[found] });
        si = found + 1;
      }
    });
    aligned[section.id] = pairs;
  }
  function alignAll() {
    if (!marks || !marks.watches) return;
    Array.prototype.forEach.call(document.querySelectorAll("section.watch"), function (section) {
      alignSection(section, marks.watches[section.id] || []);
    });
  }
  function spokenEl(section, time) {
    var pairs = aligned[section.id];
    if (!pairs || !pairs.length) return null;
    var best = null;
    for (var i = 0; i < pairs.length; i++) {
      if (pairs[i].t <= time + 0.08) best = pairs[i];
      else break;
    }
    return best ? best.el : null;
  }
  function placeLine(el) {
    if (!pref.line || !el) { hideLine(); return; }
    var range = document.createRange();
    range.selectNodeContents(el);
    var rects = range.getClientRects();
    var rect = rects.length ? rects[0] : el.getBoundingClientRect();
    lineEl.style.left = Math.max(8, rect.left) + "px";
    lineEl.style.width = Math.max(8, rect.width) + "px";
    lineEl.style.top = Math.round(rect.bottom - 1) + "px";
    document.documentElement.classList.add("read-line-on");
  }
  function followVoice() {
    var audio = playingAudio();
    document.documentElement.classList.toggle("read-audio-on", !!audio);
    if (!audio) { clearHot(); hideLine(); return false; }
    var section = audio.closest("section.watch");
    if (!section) return false;
    var el = spokenEl(section, audio.currentTime);
    if (!el) { clearHot(); hideLine(); return false; }
    clearHot();
    if (pref.word) el.classList.add("is-hot");
    if (pref.line) placeLine(el);
    else hideLine();
    if (pref.screen && performance.now() > userHoldUntil) {
      var dy = el.getBoundingClientRect().top - guideY();
      if (Math.abs(dy) > 28) window.scrollBy(0, Math.max(-20, Math.min(20, dy)));
    }
    return true;
  }
  function currentSpeed() {
    return SPEEDS[speedIndex(pref.speed)] || SPEEDS[1];
  }
  function tick(now) {
    if (!pref.on) return;
    if (!last) last = now;
    var dt = Math.min(64, Math.max(0, now - last));
    last = now;
    var audio = playingAudio();
    followVoice();
    if (audio && pref.screen) {
      raf = requestAnimationFrame(tick);
      return;
    }
    if (now > userHoldUntil) {
      var max = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
      pendingPx += (currentSpeed().px * dt) / 1000;
      if (window.scrollY < max - 2 && pendingPx >= 1) {
        var step = Math.floor(pendingPx);
        pendingPx -= step;
        window.scrollBy(0, step);
      } else if (window.scrollY >= max - 2 && max > 40) {
        stop(false);
        return;
      }
    }
    raf = requestAnimationFrame(tick);
  }
  function paint() {
    var speed = currentSpeed();
    var idx = speedIndex(speed.id);
    toggle.setAttribute("aria-pressed", pref.on ? "true" : "false");
    toggle.classList.toggle("is-on", pref.on);
    toggle.textContent = pref.on ? "Scrolling" : "Scroll";
    speedLabel.hidden = !pref.on;
    followBtn.hidden = true;
    ["word", "line", "screen"].forEach(function (key) {
      var btn = followDock.querySelector(".read-follow-" + key);
      btn.classList.toggle("is-on", !!pref[key]);
      btn.setAttribute("aria-pressed", pref[key] ? "true" : "false");
    });
    slider.value = String(idx);
    slider.setAttribute("aria-valuenow", String(idx));
    slider.setAttribute("aria-valuetext", speed.label);
    speedName.textContent = speed.label;
    dockName.textContent = speed.label;
    document.documentElement.classList.toggle("read-scroll-on", pref.on);
    if (!pref.line) hideLine();
  }
  function start() {
    pref.on = true;
    writePref(pref);
    paint();
    last = 0;
    pendingPx = 0;
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(tick);
  }
  function stop(clear) {
    pref.on = false;
    writePref(pref);
    cancelAnimationFrame(raf);
    if (clear !== false) clearHot();
    paint();
  }

  toggle.addEventListener("click", function () {
    if (pref.on) stop(true);
    else start();
  });
  stopBtn.addEventListener("click", function (ev) {
    ev.stopPropagation();
    stop(true);
  });
  function bump(dir) {
    var i = Math.max(0, Math.min(SPEEDS.length - 1, speedIndex(pref.speed) + dir));
    pref.speed = SPEEDS[i].id;
    last = 0;
    pendingPx = 0;
    writePref(pref);
    paint();
  }
  slowerBtn.addEventListener("click", function (ev) { ev.stopPropagation(); bump(-1); });
  fasterBtn.addEventListener("click", function (ev) { ev.stopPropagation(); bump(1); });
  slider.addEventListener("input", function () {
    pref.speed = SPEEDS[Number(slider.value) || 0].id;
    last = 0;
    pendingPx = 0;
    writePref(pref);
    paint();
  });
  ["word", "line", "screen"].forEach(function (key) {
    followDock.querySelector(".read-follow-" + key).addEventListener("click", function (ev) {
      ev.stopPropagation();
      pref[key] = !pref[key];
      writePref(pref);
      if (!pref.word) clearHot();
      if (!pref.line) hideLine();
      paint();
      followVoice();
    });
  });
  Array.prototype.forEach.call(document.querySelectorAll("audio"), function (audio) {
    ["timeupdate", "play", "seeked"].forEach(function (name) {
      audio.addEventListener(name, followVoice);
    });
    ["pause", "ended"].forEach(function (name) {
      audio.addEventListener(name, function () {
        if (!playingAudio()) { clearHot(); hideLine(); document.documentElement.classList.remove("read-audio-on"); }
      });
    });
  });
  var day = (location.pathname || "").match(/(\d{4}-\d{2}-\d{2})/);
  if (day) {
    fetch("/assets/readings/" + day[1] + "-words.json")
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) { marks = data; alignAll(); })
      .catch(function () {});
  }
  ["wheel", "touchstart"].forEach(function (name) {
    window.addEventListener(name, function (ev) {
      if (ev.target && ev.target.closest && ev.target.closest(".read-scroll-dock, .read-scroll-bar")) return;
      userHoldUntil = performance.now() + 2500;
    }, { passive: true });
  });

  paint();
  window.__readScroll = {
    start: start,
    stop: stop,
    words: words.length,
    setIndex: function (i) {
      pref.speed = SPEEDS[i].id;
      last = 0;
      pendingPx = 0;
      writePref(pref);
      paint();
    },
    spokenAt: function (sectionId, time) {
      var section = document.getElementById(sectionId);
      var el = section ? spokenEl(section, time) : null;
      return el ? el.textContent : "";
    },
    tickFor: function (ms) {
      var startY = window.scrollY;
      var t0 = performance.now();
      var now = t0;
      while (now - t0 < ms) {
        now += 16;
        tick(now);
      }
      return { startY: startY, endY: window.scrollY, label: speedName.textContent };
    }
  };
})();
