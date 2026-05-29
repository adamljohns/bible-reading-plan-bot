#!/bin/bash
# review.sh — turn the scan-archive JSONL into a human-readable review queue
# sorted by signal strength (female-high hit count descending).
#
# Usage:
#   bash review.sh /tmp/sermon-scan.jsonl
#   bash review.sh /tmp/sermon-scan.jsonl > /tmp/review-queue.txt

set -u
JSONL="${1:-/tmp/sermon-scan.jsonl}"
if [ ! -f "$JSONL" ]; then echo "No JSONL at $JSONL"; exit 1; fi

node -e "
const fs = require('fs');
const recs = [];
for (const l of fs.readFileSync('$JSONL', 'utf8').split('\n').filter(Boolean)) {
  try { recs.push(JSON.parse(l)); } catch (e) {}
}

// Score each record: weight female-high hits highest, female-uncertain lower,
// drop pure male / unknown noise from the queue
const scored = recs.map(r => {
  const hits = r.name_hits || [];
  const fHigh = hits.filter(h => h.gender === 'F' && h.confidence === 'high').length;
  const fAny  = hits.filter(h => h.gender === 'F').length;
  const uTitle = hits.filter(h => h.gender === 'U' && h.title).length;
  // Title-prefixed unisex names are weak signal worth surfacing
  const score = fHigh * 10 + (fAny - fHigh) * 5 + uTitle * 1;
  return { rec: r, score, fHigh, fAny, uTitle };
}).filter(s => s.score > 0);

scored.sort((a, b) => b.score - a.score);

console.log('=== MOOP Sermon-Archive Review Queue ===');
console.log('Total records in queue: ' + scored.length + ' (of ' + recs.length + ' scanned)');
console.log('Sort: female-high hits, then female-uncertain, then unisex-with-title');
console.log('');
console.log('Heuristic flags only; every entry needs human confirmation before any rating change.');
console.log('');

let n = 0;
for (const s of scored) {
  n++;
  const r = s.rec;
  console.log('--- [' + n + '] ' + (r.name || r.id) + ' (score ' + s.score + ') ---');
  console.log('  slug: ' + r.id);
  console.log('  archive: ' + r.archive_url);
  console.log('  female-high: ' + s.fHigh + '  female-any: ' + s.fAny + '  unisex-with-title: ' + s.uTitle);
  const fHits = (r.name_hits || []).filter(h => h.gender === 'F').slice(0, 5);
  const uHits = (r.name_hits || []).filter(h => h.gender === 'U' && h.title).slice(0, 3);
  for (const h of fHits) {
    console.log('    F: ' + (h.title || '') + ' ' + h.name + '  [' + h.confidence + ']');
    console.log('       ctx: ' + (h.context || '').slice(0, 150));
  }
  for (const h of uHits) {
    console.log('    U: ' + (h.title || '') + ' ' + h.name + '  [unisex first name]');
    console.log('       ctx: ' + (h.context || '').slice(0, 150));
  }
  console.log('');
}

if (scored.length === 0) {
  console.log('(no female / unisex-with-title hits found in this scan)');
}
"
