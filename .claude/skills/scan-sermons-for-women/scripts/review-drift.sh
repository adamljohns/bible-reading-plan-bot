#!/bin/bash
# review-drift.sh — turn scan-drift JSONL into a human review queue sorted by
# total signal weight, with special emphasis on GREEN-rated churches showing
# drift (those are the ones whose rating may need to come down).
#
# Usage: bash review-drift.sh /tmp/drift-scan.jsonl
set -u
JSONL="${1:-/tmp/drift-scan.jsonl}"
[ -f "$JSONL" ] || { echo "No JSONL at $JSONL"; exit 1; }

node -e "
const fs=require('fs');
const recs=[];
for(const l of fs.readFileSync('$JSONL','utf8').split('\n').filter(Boolean)){ try{recs.push(JSON.parse(l));}catch(e){} }
const scored=recs.filter(r=>r.hits&&r.hits.length).map(r=>{
  const weight=r.hits.reduce((s,h)=>s+(h.weight||1),0);
  // Boost churches currently rated green/yellow — drift there is most actionable
  const ratingBoost=(r.rating==='green')?10:(r.rating==='yellow')?4:0;
  const cats=[...new Set(r.hits.map(h=>h.category))];
  return {r,weight,score:weight+ratingBoost,cats};
}).sort((a,b)=>b.score-a.score);

console.log('=== MOOP Sermon/Site Drift Review Queue ===');
console.log('Flagged: '+scored.length+' of '+recs.length+' scanned. Sort: signal weight + current-rating boost.');
console.log('Heuristic only; confirm each before any rating change. A church may preach AGAINST these topics.');
console.log('');
let n=0;
for(const s of scored){
  n++; const r=s.r;
  console.log('--- ['+n+'] '+(r.name||r.id)+'  (rating='+(r.rating||'?')+', score '+s.score+') ---');
  console.log('  slug: '+r.id+'  | categories: '+s.cats.join(', '));
  for(const h of r.hits.slice(0,6)){
    console.log('    ['+h.category+' w'+h.weight+'] \"'+h.phrase+'\" — '+h.note);
    console.log('       ctx: ...'+(h.context||'').slice(0,110)+'...');
  }
  console.log('');
}
if(!scored.length) console.log('(no drift signals found in this scan)');
"
