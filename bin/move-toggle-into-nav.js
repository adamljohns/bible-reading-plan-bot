#!/usr/bin/env node
/* move-toggle-into-nav.js — uniform theme-toggle placement, site-wide.
 *
 * The 2026-06-13 pill redesign (light-icons.css) forces every .bte-theme-toggle
 * to position:relative !important, which dropped the old fixed top-right toggles
 * into document flow (top-left / centered, "out of place"). A fixed-position
 * pill can't reserve space in a wrapping nav, so it overlaps nav links on mobile.
 * The clean fix at every width is to move the toggle INSIDE the <nav> as its last
 * child with class "nav-theme-toggle" — light-icons.css then floats it top-right
 * (margin-left:auto) and the flex nav wraps to accommodate it. No overlap.
 *
 * This moves a standalone .bte-theme-toggle / .theme-toggle into the first <nav>.
 * It is idempotent (skips toggles already in-nav with the class). Inline
 * position CSS left on the page is harmless — light-icons.css overrides it.
 *
 * Usage: node bin/move-toggle-into-nav.js [--apply] <file ...>
 *        (default = dry run; prints what it WOULD change)
 */
'use strict';
const fs = require('fs');

const APPLY = process.argv.includes('--apply');
const files = process.argv.slice(2).filter((a) => a !== '--apply');

// Extract the full toggle element (balanced over its own tag type).
function findToggle(html) {
  const re = /<(div|button)\b[^>]*class="[^"]*\b(?:bte-theme-toggle|theme-toggle)\b[^"]*"[^>]*>/i;
  const m = re.exec(html);
  if (!m) return null;
  const tag = m[1].toLowerCase();
  const start = m.index;
  const lower = html.toLowerCase();
  const openTok = '<' + tag;
  const closeTok = '</' + tag + '>';
  let i = start + m[0].length;
  let depth = 1;
  while (i < html.length && depth > 0) {
    const nextOpen = lower.indexOf(openTok, i);
    const nextClose = lower.indexOf(closeTok, i);
    if (nextClose === -1) return null; // malformed
    if (nextOpen !== -1 && nextOpen < nextClose) {
      const c = html[nextOpen + openTok.length];
      if (c === ' ' || c === '>' || c === '\t' || c === '\n' || c === '/') depth++;
      i = nextOpen + openTok.length;
    } else {
      depth--;
      i = nextClose + closeTok.length;
    }
  }
  if (depth !== 0) return null;
  return { start, end: i, html: html.slice(start, i), tag, startTag: m[0] };
}

function withNavClass(toggleHtml) {
  return toggleHtml.replace(/(<(?:div|button)\b[^>]*class=")([^"]*)(")/i, (full, pre, cls, post) => {
    if (/\bnav-theme-toggle\b/.test(cls)) return full;
    return pre + cls.trim() + ' nav-theme-toggle' + post;
  });
}

let fixed = 0, skipped = 0;
for (const f of files) {
  let html;
  try { html = fs.readFileSync(f, 'utf8'); } catch (e) { console.log('skip (read):', f); skipped++; continue; }
  const navOpen = /<nav\b[^>]*>/i.exec(html);
  if (!navOpen) { console.log('skip (no <nav>):', f); skipped++; continue; }
  const tog = findToggle(html);
  if (!tog) { console.log('skip (no toggle):', f); skipped++; continue; }

  const navCloseIdx = html.toLowerCase().indexOf('</nav>', navOpen.index);
  const insideNav = navCloseIdx !== -1 && tog.start > navOpen.index && tog.end <= navCloseIdx;
  const hasClass = /\bnav-theme-toggle\b/.test(tog.startTag);
  if (insideNav && hasClass) { console.log('ok (already in-nav):', f); skipped++; continue; }

  // 1) remove the toggle from its current location
  let out = html.slice(0, tog.start) + html.slice(tog.end);
  // 2) find the nav close in the modified string and insert before it
  const navOpen2 = /<nav\b[^>]*>/i.exec(out);
  const navCloseIdx2 = out.toLowerCase().indexOf('</nav>', navOpen2.index);
  if (navCloseIdx2 === -1) { console.log('skip (no nav close):', f); skipped++; continue; }
  const newToggle = withNavClass(tog.html);
  out = out.slice(0, navCloseIdx2) + newToggle + out.slice(navCloseIdx2);

  if (APPLY) { fs.writeFileSync(f, out); console.log('FIXED:', f); }
  else { console.log('WOULD FIX:', f); }
  fixed++;
}
console.log('\n' + (APPLY ? 'fixed' : 'would fix') + ': ' + fixed + ' | skipped: ' + skipped);
