#!/usr/bin/env node
//
// apply-enrichment-round.js — apply a verified research-round result file to
// churches.json. Used by the overnight agent-research enrichment rounds.
//
// Input JSON: array of { id, pastor?, pastor_credentials?, facebook?, youtube?,
//   instagram?, enrichment_note?, review_gender?, gender_flag? }.
//
// Safety:
//   - pastor applied only if it passes the placeholder/junk filter
//   - social URLs applied only if they match the expected domain + https
//   - gender_flag === 'female-senior-pastor' on a green church -> downgrade to
//     red (per the MOOP rubric: a SOLE female senior pastor is RED minimum)
//   - review_gender (co-pastor couples etc.) records a flag for human review,
//     NOT an automatic downgrade
//
// Usage: node apply-enrichment-round.js /tmp/round-results.json

const fs = require('fs');
const path = require('path');
const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const INPUT = process.argv[2] || '/tmp/round-results.json';

const PH = /^(verify|various|unknown|see\s+website|currently|none|listed|tbd|n\/a|the\s+pastor|the\s+church|pastoral|pastor\s*\(|check |contact |not\s+(listed|published)|vacant|interim)/i;
const JUNK = /(black hawk|hawk down|enjoy|movie|video|book|sermon|story|message|search|committee|jesus|christ|^god$|^lord$|spirit|gospel|kingdom|salvation|baptism|sunday|service)/i;

function realPastor(p) {
  p = String(p || '').trim();
  if (p.length < 4) return false;
  if (PH.test(p)) return false;
  if (JUNK.test(p)) return false;
  // Must look like a human name: at least two words OR a title+name
  if (!/\s/.test(p) && !/^[A-Z][a-z]+$/.test(p)) return false;
  return true;
}

const results = JSON.parse(fs.readFileSync(INPUT, 'utf8'));
const data = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
const byId = new Map(data.churches.map(c => [String(c.id || c.slug), c]));

let pastors = 0, social = 0, downgrades = 0, flags = 0;
for (const r of results) {
  const c = byId.get(String(r.id));
  if (!c) continue;

  if (r.pastor && realPastor(r.pastor)) {
    c.pastor = r.pastor.trim();
    c.pastor_source = 'agent-research-verified';
    pastors++;
    if (r.pastor_credentials && (!c.pastor_credentials || c.pastor_credentials === 'Unknown')) {
      c.pastor_credentials = r.pastor_credentials.trim();
    }
  }
  for (const [field, host] of [['facebook','facebook.com'],['youtube','youtube.com'],['instagram','instagram.com']]) {
    const v = r[field];
    if (v && /^https:\/\//i.test(v) && v.toLowerCase().includes(host) && !c[field]) {
      c[field] = v; social++;
    }
  }
  if (r.enrichment_note) {
    if (!Array.isArray(c.enrichment_notes)) c.enrichment_notes = c.enrichment_notes ? [String(c.enrichment_notes)] : [];
    const stamp = '[agent-research] ' + r.enrichment_note;
    if (!c.enrichment_notes.includes(stamp)) c.enrichment_notes.push(stamp);
  }
  // SOLE female senior pastor -> RED per rubric
  if (r.gender_flag === 'female-senior-pastor' && c.overall_rating === 'green') {
    c.overall_rating = 'red';
    c.overall_label = 'RED — female senior pastor (rubric: complementarian leadership)';
    if (c.scores) c.scores.gender = 'red';
    downgrades++;
  }
  // Co-pastor / ambiguous gender cases -> flag for human review, no auto-change
  if (r.review_gender) { c.review_gender = true; flags++; }
}

fs.writeFileSync(CHURCHES, JSON.stringify(data, null, 2) + '\n');
console.log('Applied: +' + pastors + ' pastors, +' + social + ' social URLs, ' + downgrades + ' rubric downgrades, ' + flags + ' gender-review flags');
