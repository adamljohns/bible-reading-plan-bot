/**
 * USMC Ministries print kit — dense sepia/bronze print-ready pages.
 * Adds screen-only "Print / PDF" control. Lex/dict/xref aim one page.
 */
(function () {
  if (window.__usmcPrintKit) return;
  window.__usmcPrintKit = true;

  function ensurePrintCss() {
    if (document.querySelector('link[href*="/assets/css/print.css"]')) return;
    var link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = '/assets/css/print.css';
    link.media = 'print';
    document.head.appendChild(link);
  }

  function injectStyles() {
    if (document.getElementById('usmc-print-kit-style')) return;
    var s = document.createElement('style');
    s.id = 'usmc-print-kit-style';
    s.textContent = [
      '.print-kit-bar{display:flex;justify-content:flex-end;gap:6px;margin:0 0 8px;flex-wrap:wrap;}',
      '.print-kit-btn{display:inline-flex;align-items:center;gap:5px;font-family:Inter,system-ui,sans-serif;',
      'font-size:0.78rem;font-weight:600;padding:5px 10px;border-radius:999px;cursor:pointer;',
      'border:1px solid rgba(212,175,55,0.45);background:rgba(212,175,55,0.10);color:#D4AF37;',
      'text-decoration:none;line-height:1;}',
      '.print-kit-btn:hover{border-color:#D4AF37;background:rgba(212,175,55,0.18);}',
      'body.light-mode .print-kit-btn{color:#8A6A1A;border-color:#D4D0C8;background:rgba(184,150,12,0.10);}',
      'body.light-mode .print-kit-btn:hover{border-color:#8A6A1A;background:rgba(184,150,12,0.16);}',
      '.print-kit-btn .pk-icon{font-size:0.9rem;line-height:1;}',
      '@media print{.print-kit-bar,.print-kit-btn{display:none!important;}}'
    ].join('');
    document.head.appendChild(s);
  }

  function findMount() {
    var container = document.querySelector('.container') || document.querySelector('main') || document.body;
    var header = container.querySelector('.word-header, .result-header, #results, .hero, h1');
    return { container: container, header: header };
  }

  function alreadyMounted(container) {
    return !!(container && container.querySelector('.print-kit-bar'));
  }

  function mountButton() {
    var mount = findMount();
    if (!mount.container || alreadyMounted(mount.container)) return;

    var bar = document.createElement('div');
    bar.className = 'print-kit-bar no-print';
    bar.setAttribute('role', 'toolbar');
    bar.setAttribute('aria-label', 'Print tools');

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'print-kit-btn';
    btn.title = 'Print/PDF — dense cream paper, charcoal text, bronze accents (one-page study sheet when possible)';
    btn.innerHTML = '<span class="pk-icon" aria-hidden="true">🖨</span><span>Print / PDF</span>';
    btn.addEventListener('click', function () {
      var hadLight = document.body.classList.contains('light-mode');
      if (!hadLight) document.body.classList.add('light-mode');
      window.setTimeout(function () {
        window.print();
        if (!hadLight) document.body.classList.remove('light-mode');
      }, 30);
    });

    bar.appendChild(btn);

    if (mount.header && mount.header.parentNode === mount.container) {
      mount.container.insertBefore(bar, mount.header);
    } else if (mount.header && mount.header.parentNode) {
      mount.header.parentNode.insertBefore(bar, mount.header);
    } else {
      mount.container.insertBefore(bar, mount.container.firstChild);
    }
  }

  function boot() {
    ensurePrintCss();
    injectStyles();
    mountButton();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
