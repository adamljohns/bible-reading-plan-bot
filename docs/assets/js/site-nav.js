/* site-nav.js — shared hide-on-scroll for the sticky top nav.
 *
 * Ports the exact behaviour proven on bible.html (the BTE) to every page
 * that links this file: on MOBILE (viewport <= 820px) the sticky top nav
 * slides up when you scroll down and slides back when you scroll up. On
 * desktop the nav never hides — identical to the BTE.
 *
 * Self-contained: it injects its own CSS, so no stylesheet edits are needed.
 * Idempotent: safe to load once per page. Added 2026-07-04 to unify the
 * scroll behaviour the BTE already had across the main tool/content pages.
 */
(function () {
  // 1) CSS — add the slide transition + the hidden state. Each page's own
  //    `nav { position: sticky; top: 0 }` rule is untouched; we only append
  //    the transform bits, and .nav-hidden (element+class) wins on specificity.
  if (!document.getElementById('site-nav-hide-css')) {
    var css = 'nav{transition:transform .3s ease;will-change:transform}'
            + 'nav.nav-hidden{transform:translateY(-100%)}';
    var style = document.createElement('style');
    style.id = 'site-nav-hide-css';
    style.textContent = css;
    (document.head || document.documentElement).appendChild(style);
  }

  // 2) Behaviour — byte-for-byte the same logic as the BTE's hide-on-scroll.
  var nav = document.querySelector('nav');
  if (!nav) return;
  var lastY = window.scrollY || window.pageYOffset || 0, ticking = false, THRESHOLD = 60;
  function mobile() { return window.matchMedia('(max-width:820px)').matches; }
  function update() {
    var y = window.scrollY || window.pageYOffset || 0;
    if (!mobile()) { nav.classList.remove('nav-hidden'); lastY = y; ticking = false; return; }
    if (y <= THRESHOLD) { nav.classList.remove('nav-hidden'); lastY = y; ticking = false; return; }
    if (y > lastY && y > THRESHOLD) { nav.classList.add('nav-hidden'); }
    else if (y < lastY) { nav.classList.remove('nav-hidden'); }
    lastY = y <= 0 ? 0 : y; ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
  }, { passive: true });
})();
