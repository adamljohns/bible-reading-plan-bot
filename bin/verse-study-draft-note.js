/* verse-study-draft-note.js — the one draft marker every unreviewed verse study carries.
 *
 * Adam 2026-11-20: drafts may be listed on the public index (labelled, noindex on
 * the page); draft note is yellow at the bottom, never red.
 *
 * Modelled on the "Original Draft Prototype" tag in the footer of the daily
 * readings pages (docs/readings/*.html, footer .draft-tag / .draft-note): a gold
 * pill on dark olive, one grey line under it, centred, after the last content.
 *
 * The class stays `vs-draft-banner` on purpose: bin/verse-study-gate.js fails an
 * approved study that still contains it, so renaming it would quietly disable
 * that check. Used by bin/verse-study-render.js and bin/verse-study-draft.js.
 */
'use strict';

const DRAFT_NOTE_CSS = `      .vs-draft-banner { text-align:center; margin:1.6rem 0 0; padding:1rem 0 .4rem; line-height:1.35; }
      .vs-draft-banner .vs-draft-tag { display:inline-block; background:#2a2410; color:#D4AF37; padding:4px 12px; border-radius:100px; font-size:.78rem; letter-spacing:.05em; margin-bottom:6px; }
      .vs-draft-banner .vs-draft-sub { color:var(--gray); font-size:.78rem; }
      body.light-mode .vs-draft-banner .vs-draft-tag { background:#f3e3a3; color:#6b5000; }
`;

const DRAFT_NOTE_HTML = `  <div class="vs-draft-banner"><div class="vs-draft-tag">Draft Study</div><div class="vs-draft-sub">Not yet reviewed by Adam</div></div>
`;

module.exports = { DRAFT_NOTE_CSS, DRAFT_NOTE_HTML };
