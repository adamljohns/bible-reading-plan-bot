/* Brass Check — install to Home Screen (PJG-0918-PWA1)
 *
 * Android/Chrome/Edge: capture beforeinstallprompt, show our own bar, call prompt().
 * iOS Safari: no install API exists, so show the Share -> Add to Home Screen instructions.
 * Already installed (standalone): show nothing, ever.
 *
 * Dismissal is remembered. The bar never nags: it waits for a real visit, and a
 * dismissal is honoured for 60 days.
 */
(function () {
  'use strict';

  var LS_KEY = 'brasscheck.install.dismissed';
  var SNOOZE_DAYS = 60;
  var SHOW_AFTER_MS = 2500;

  function isStandalone() {
    return (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) ||
           window.navigator.standalone === true ||
           document.referrer.indexOf('android-app://') === 0;
  }

  function isIos() {
    var ua = window.navigator.userAgent || '';
    var iOSDevice = /iPad|iPhone|iPod/.test(ua);
    // iPadOS 13+ reports as Mac; detect by touch support
    var iPadDesktopUA = /Macintosh/.test(ua) && navigator.maxTouchPoints > 1;
    return iOSDevice || iPadDesktopUA;
  }

  function isAndroid() {
    return /Android/.test(window.navigator.userAgent || '');
  }

  function isSafari() {
    var ua = window.navigator.userAgent || '';
    return /Safari/.test(ua) && !/CriOS|FxiOS|EdgiOS|OPiOS|Chrome/.test(ua);
  }

  function snoozed() {
    try {
      var v = localStorage.getItem(LS_KEY);
      if (!v) return false;
      return (Date.now() - parseInt(v, 10)) < SNOOZE_DAYS * 864e5;
    } catch (e) { return false; }
  }

  function snooze() {
    try { localStorage.setItem(LS_KEY, String(Date.now())); } catch (e) {}
  }

  function injectStyles() {
    if (document.getElementById('bc-install-style')) return;
    var s = document.createElement('style');
    s.id = 'bc-install-style';
    s.textContent = [
      '.bc-install{position:fixed;left:50%;transform:translateX(-50%) translateY(140%);',
      'bottom:calc(14px + env(safe-area-inset-bottom));width:min(520px,calc(100vw - 24px));',
      'z-index:9999;background:#111;border:1px solid #D4AF37;border-radius:14px;',
      'box-shadow:0 10px 34px rgba(0,0,0,.6);padding:14px 16px;color:#fff;',
      "font-family:'Inter',system-ui,sans-serif;transition:transform .34s cubic-bezier(.2,.8,.2,1);}",
      '.bc-install.bc-show{transform:translateX(-50%) translateY(0);}',
      '.bc-install-row{display:flex;gap:12px;align-items:flex-start;}',
      '.bc-install img{width:44px;height:44px;border-radius:10px;flex:0 0 auto;}',
      '.bc-install-tx{flex:1 1 auto;min-width:0;}',
      ".bc-install h4{margin:0 0 2px;font-family:'Playfair Display',serif;color:#F4D470;",
      'font-size:1rem;font-weight:700;}',
      '.bc-install p,.bc-install-body{margin:0;font-size:.82rem;line-height:1.45;color:#cfcfcf;}',
      '.bc-install-btns{display:flex;gap:8px;margin-top:11px;justify-content:flex-end;}',
      '.bc-install button{font:inherit;font-size:.82rem;border-radius:9px;padding:8px 15px;',
      'cursor:pointer;border:1px solid #333;background:transparent;color:#bbb;}',
      '.bc-install button.bc-go{background:#D4AF37;border-color:#D4AF37;color:#000;font-weight:700;}',
      '.bc-install button.bc-go:hover{background:#F4D470;}',
      '.bc-install button:hover{color:#fff;}',
      '.bc-share-ico{display:inline-block;vertical-align:-3px;margin:0 2px;}',
      // iOS step list. Safari hides Share inside the ... menu on iOS 26, so the
      // instructions have to walk the man there instead of naming one icon.
      '.bc-steps{margin:7px 0 0;padding:0;list-style:none;counter-reset:bcstep;}',
      '.bc-steps li{position:relative;padding-left:23px;margin:0 0 5px;',
      'font-size:.82rem;line-height:1.45;color:#cfcfcf;}',
      '.bc-steps li:last-child{margin-bottom:0;}',
      '.bc-steps li::before{counter-increment:bcstep;content:counter(bcstep);',
      'position:absolute;left:0;top:1px;width:16px;height:16px;border-radius:50%;',
      'background:#D4AF37;color:#000;font-size:.66rem;font-weight:700;',
      'display:flex;align-items:center;justify-content:center;}',
      '.bc-key{color:#fff;font-weight:700;}',
      '.bc-dots{display:inline-flex;align-items:center;justify-content:center;',
      'gap:2px;vertical-align:1px;padding:2px 6px;margin:0 1px;border-radius:999px;',
      'background:#2a2a2a;border:1px solid #444;}',
      '.bc-dots i{width:3px;height:3px;border-radius:50%;background:#F4D470;display:block;}',
      // Android's overflow menu is a vertical ellipsis; iOS Safari's is horizontal.
      '.bc-dots-v{flex-direction:column;padding:5px 5px;}',
      '@media (prefers-reduced-motion: reduce){.bc-install{transition:none;}}'
    ].join('');
    document.head.appendChild(s);
  }

  function build(titleHtml, bodyHtml, primaryLabel, onPrimary) {
    injectStyles();
    var wrap = document.createElement('div');
    wrap.className = 'bc-install';
    wrap.setAttribute('role', 'dialog');
    wrap.setAttribute('aria-label', 'Install Brass Check');

    var row = document.createElement('div');
    row.className = 'bc-install-row';

    var ico = document.createElement('img');
    ico.src = '/assets/icons/brass-check-192.png';
    ico.alt = '';
    row.appendChild(ico);

    var tx = document.createElement('div');
    tx.className = 'bc-install-tx';
    var h = document.createElement('h4');
    h.textContent = titleHtml;
    // A div, not a p: the iOS body carries an <ol>, which the parser would
    // hoist straight out of a <p> and leave the panel mangled.
    var p = document.createElement('div');
    p.className = 'bc-install-body';
    p.innerHTML = bodyHtml;
    tx.appendChild(h); tx.appendChild(p);
    row.appendChild(tx);
    wrap.appendChild(row);

    var btns = document.createElement('div');
    btns.className = 'bc-install-btns';
    var no = document.createElement('button');
    no.type = 'button';
    no.textContent = 'Not now';
    no.addEventListener('click', function () { snooze(); hide(wrap); });
    btns.appendChild(no);

    if (primaryLabel) {
      var yes = document.createElement('button');
      yes.type = 'button';
      yes.className = 'bc-go';
      yes.textContent = primaryLabel;
      yes.addEventListener('click', function () { onPrimary(wrap); });
      btns.appendChild(yes);
    } else {
      no.textContent = 'Got it';
    }
    wrap.appendChild(btns);

    document.body.appendChild(wrap);
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { wrap.classList.add('bc-show'); });
    });
    return wrap;
  }

  function hide(el) {
    el.classList.remove('bc-show');
    setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 360);
  }

  if (isStandalone() || snoozed()) return;

  // Only one bar, ever — the install prompt and the how-to steps must never race
  // each other onto the screen.
  var shown = false;
  function once(fn) {
    return function () {
      if (shown || isStandalone()) return;
      shown = true;
      fn();
    };
  }

  var shareSvg = '<svg class="bc-share-ico" width="13" height="13" viewBox="0 0 24 24" ' +
    'fill="none" stroke="#F4D470" stroke-width="2.1" stroke-linecap="round" ' +
    'stroke-linejoin="round" aria-hidden="true">' +
    '<path d="M12 16V4"/><path d="M8 8l4-4 4 4"/>' +
    '<path d="M4 14v5a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-5"/></svg>';
  // Drawn, not typed: "⋮" and "•••" render as tofu or as wildly different glyphs
  // depending on the font a phone falls back to.
  function dots(vertical) {
    return '<span class="bc-dots' + (vertical ? ' bc-dots-v' : '') + '" aria-hidden="true">' +
      '<i></i><i></i><i></i></span>';
  }

  // ---- Android / Chromium: real install prompt -------------------------------
  var deferred = null;
  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    deferred = e;
    setTimeout(once(function () {
      build(
        'Add Brass Check to your Home Screen',
        'Install it as an app — opens full screen and works offline, so you can drill anywhere.',
        'Install',
        function (el) {
          hide(el);
          deferred.prompt();
          deferred.userChoice.then(function (c) {
            if (c && c.outcome !== 'accepted') snooze();
            deferred = null;
          });
        }
      );
    }), SHOW_AFTER_MS);
  });

  window.addEventListener('appinstalled', function () { snooze(); });

  // ---- iOS: no install API exists, so teach the gesture ----------------------
  // On iOS 26 the Safari toolbar reads back / tabs / address / reload / "...".
  // There is no Share icon on screen — it lives inside that "..." menu. Older iOS
  // (and the top-address-bar layout) does show Share in the toolbar, so step 1
  // names the menu first and offers the icon as the alternative.
  if (isIos()) {
    var iosSteps = isSafari()
      ? '<li>Tap ' + dots() + ' at the <span class="bc-key">bottom right</span> of Safari' +
          ' &mdash; or ' + shareSvg + ' if your toolbar shows it instead.</li>' +
        '<li>Choose <span class="bc-key">Share</span>.</li>' +
        '<li>Scroll down the list and tap <span class="bc-key">Add to Home Screen</span>.</li>'
      // Chrome / Edge / Firefox on iOS are Safari underneath, but the menu is
      // their own: three dots bottom right, then Share.
      : '<li>Tap ' + dots() + ' at the <span class="bc-key">bottom right</span> of the browser.</li>' +
        '<li>Choose <span class="bc-key">Share</span>.</li>' +
        '<li>Scroll down the list and tap <span class="bc-key">Add to Home Screen</span>.</li>';
    setTimeout(once(function () {
      build(
        'Add Brass Check to your Home Screen',
        '<ol class="bc-steps">' + iosSteps + '</ol>',
        null, null
      );
    }), SHOW_AFTER_MS);
  } else if (isAndroid()) {
    // Fallback for Android browsers that never fire beforeinstallprompt — Firefox,
    // Samsung Internet, or Chrome when it has already prompted for this origin.
    // Give it a grace window past SHOW_AFTER_MS so the real Install bar wins.
    setTimeout(once(function () {
      build(
        'Add Brass Check to your Home Screen',
        '<ol class="bc-steps">' +
          '<li>Tap ' + dots(true) + ' at the <span class="bc-key">top right</span> of the browser.</li>' +
          '<li>Tap <span class="bc-key">Add to Home screen</span>' +
            ' &mdash; some browsers call it <span class="bc-key">Install app</span>.</li>' +
          '<li>Confirm, and the shield lands on your Home Screen.</li>' +
        '</ol>',
        null, null
      );
    }), SHOW_AFTER_MS + 1800);
  }
})();
