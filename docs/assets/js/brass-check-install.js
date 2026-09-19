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
      '.bc-install p{margin:0;font-size:.82rem;line-height:1.45;color:#cfcfcf;}',
      '.bc-install-btns{display:flex;gap:8px;margin-top:11px;justify-content:flex-end;}',
      '.bc-install button{font:inherit;font-size:.82rem;border-radius:9px;padding:8px 15px;',
      'cursor:pointer;border:1px solid #333;background:transparent;color:#bbb;}',
      '.bc-install button.bc-go{background:#D4AF37;border-color:#D4AF37;color:#000;font-weight:700;}',
      '.bc-install button.bc-go:hover{background:#F4D470;}',
      '.bc-install button:hover{color:#fff;}',
      '.bc-share-ico{display:inline-block;vertical-align:-3px;margin:0 2px;}',
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
    var p = document.createElement('p');
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

  // ---- Android / Chromium: real install prompt -------------------------------
  var deferred = null;
  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    deferred = e;
    setTimeout(function () {
      if (!deferred || isStandalone()) return;
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
    }, SHOW_AFTER_MS);
  });

  window.addEventListener('appinstalled', function () { snooze(); });

  // ---- iOS Safari: no API, so teach the gesture ------------------------------
  if (isIos() && isSafari()) {
    var shareSvg = '<svg class="bc-share-ico" width="13" height="13" viewBox="0 0 24 24" ' +
      'fill="none" stroke="#F4D470" stroke-width="2.1" stroke-linecap="round" ' +
      'stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M12 16V4"/><path d="M8 8l4-4 4 4"/>' +
      '<path d="M4 14v5a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-5"/></svg>';
    setTimeout(function () {
      if (isStandalone()) return;
      build(
        'Add Brass Check to your Home Screen',
        'Tap ' + shareSvg + ' <strong style="color:#fff">Share</strong> at the bottom of Safari, ' +
        'then choose <strong style="color:#fff">Add to Home Screen</strong>. ' +
        'It opens full screen and works offline.',
        null, null
      );
    }, SHOW_AFTER_MS);
  }
})();
