/* site-nav.js — shared hide-on-scroll for the sticky top nav.
 *
 * On MOBILE (viewport <= 820px) the sticky top nav (the first <nav> on the
 * page) slides up once you scroll past the top (THRESHOLD px, or past the
 * nav's own spot if it sits lower) and comes back ONLY when you return to
 * the top of the page. On desktop the nav never hides.
 *
 * Opt-out: put data-nav-reveal="scroll-up" on <body> or on the nav to keep
 * the older behaviour (hide on scroll-down, reveal on any scroll-up).
 *
 * Self-contained: it injects its own CSS, so no stylesheet edits are needed.
 * Idempotent: safe to load once per page. Added 2026-07-04 to unify the
 * scroll behaviour across the main tool/content pages. Changed 2026-10-04,
 * by Adam's request: the nav returns only at the top, not on scroll-up
 * (PJG-1004-NAV).
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

  // 2) Behaviour.
  var nav = document.querySelector('nav');
  if (!nav) return;
  var OPT = 'data-nav-reveal';
  var revealOnScrollUp = (document.body && document.body.getAttribute(OPT) === 'scroll-up')
                      || nav.getAttribute(OPT) === 'scroll-up';
  var lastY = window.scrollY || window.pageYOffset || 0, ticking = false, THRESHOLD = 60;
  // Where the nav sits in normal flow: 0 for a top bar, lower for a nav below
  // a hero (e.g. the daily-readings watch tabs). Never hide above that line,
  // or the bar slides up over the content above it before it is even stuck.
  var navTop = 0;
  function measure() {
    var cs = getComputedStyle(nav).position, pos = nav.style.position, t = 0, el;
    if (cs === 'fixed') { navTop = 0; return; }
    if (cs === 'sticky') nav.style.position = 'static'; // same footprint, no shift
    for (el = nav; el; el = el.offsetParent) t += el.offsetTop;
    nav.style.position = pos;
    navTop = t;
  }
  function mobile() { return window.matchMedia('(max-width:820px)').matches; }
  function update() {
    var y = window.scrollY || window.pageYOffset || 0;
    ticking = false;
    if (!mobile() || y <= Math.max(THRESHOLD, navTop)) { nav.classList.remove('nav-hidden'); lastY = y; return; }
    if (!revealOnScrollUp) { nav.classList.add('nav-hidden'); lastY = y; return; }
    // Opt-out (old logic): hide on scroll-down, reveal on any scroll-up.
    if (y > lastY) { nav.classList.add('nav-hidden'); }
    else if (y < lastY) { nav.classList.remove('nav-hidden'); }
    lastY = y;
  }
  measure();
  window.addEventListener('load', measure);
  window.addEventListener('resize', measure);
  window.addEventListener('scroll', function () {
    if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
  }, { passive: true });
})();
