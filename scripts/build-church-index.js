#!/usr/bin/env node
// Build docs/data/churches-index.json — the slim payload churches.html actually renders.
//
// churches.json is ~61 MB pretty-printed and the directory page used to download ALL of it
// on every visit (twice — main load + footer count). This index carries only the fields the
// card grid renders, minified, with scores compacted to a 10-char string in rubric order
// (g=green y=yellow r=red b=black, '-'=unscored/gray). Result is ~15 MB raw / ~2-3 MB gzipped.
//
// What is deliberately EXCLUDED (lives on the per-church pages, not the card grid):
// enrichment_notes, signatories, engagement, sources, quick_links, image_url, image_thumb,
// last_reviewed, pastor_transition, slug, url_research_status, social links.
//
// Usage:
//   node scripts/build-church-index.js          # standalone rebuild
// Also invoked automatically at the end of generate-church-pages.js (including --only runs),
// so the index can never drift from churches.json under the standard regen-then-push workflow.

const fs = require('fs');
const path = require('path');

// Card fields copied verbatim when non-empty (churches.html buildCardEl + filter index).
const FIELDS = [
  'id', 'name', 'overall_rating', 'denomination', 'denomination_family', 'founded',
  'pastor', 'pastors', 'pastor_credentials', 'address', 'website', 'services',
  'has_mens_ministry', 'has_kids_ministry', 'tags',
  'score_notes', 'gender_detail', 'assessment', 'region', 'type',
];

const COLOR_CHAR = { green: 'g', yellow: 'y', red: 'r', black: 'b', gray: '-' };

function compactScores(scores, rubric, warnings) {
  return rubric.map(r => {
    const v = scores ? scores[r.id] : undefined;
    if (v === undefined || v === null || v === '') return '-';
    const c = COLOR_CHAR[String(v).toLowerCase().trim()];
    if (!c) { warnings.add(String(v)); return '-'; }
    return c;
  }).join('');
}

function isEmpty(v) {
  if (v === undefined || v === null || v === '') return true;
  if (Array.isArray(v)) return v.length === 0;
  if (typeof v === 'object') return Object.keys(v).length === 0;
  return v === false; // booleans: absent reads as false on the page, so drop false
}

function buildIndex(data) {
  const rubric = data.rubric || [];
  const warnings = new Set();
  const churches = data.churches.map(c => {
    const slim = {};
    for (const k of FIELDS) {
      if (!isEmpty(c[k])) slim[k] = c[k];
    }
    const sc = compactScores(c.scores, rubric, warnings);
    if (sc.replace(/-/g, '') !== '') slim.scores = sc; // all-gray ⇒ omit entirely
    return slim;
  });
  if (warnings.size) {
    console.warn(`⚠️  Unrecognized score values mapped to gray: ${[...warnings].join(', ')}`);
  }
  return {
    directory_version: data.directory_version,
    directory_updated: data.directory_updated,
    total_churches: data.total_churches,
    rubric,
    churches,
  };
}

// ASCII-escaped (repo canon for data files), minified, no trailing newline.
function writeIndex(data, outPath) {
  const esc = s => s.replace(/[^\x00-\x7F]/g, ch => '\\u' + ch.charCodeAt(0).toString(16).padStart(4, '0'));
  const buf = esc(JSON.stringify(buildIndex(data)));
  fs.writeFileSync(outPath, buf);
  return Buffer.byteLength(buf);
}

module.exports = { buildIndex, writeIndex };

if (require.main === module) {
  const REPO_ROOT = path.resolve(__dirname, '..');
  const data = JSON.parse(fs.readFileSync(path.join(REPO_ROOT, 'docs/data/churches.json'), 'utf8'));
  const outPath = path.join(REPO_ROOT, 'docs/data/churches-index.json');
  const bytes = writeIndex(data, outPath);
  console.log(`✅ churches-index.json — ${data.churches.length} churches, ${(bytes / 1048576).toFixed(1)} MB`);
}
