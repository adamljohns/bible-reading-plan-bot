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

// Validate a researched street address: needs a street number, a city, and a
// 2-letter state (so the geocoder can place it). Rejects city-only strings.
function goodAddress(a) {
  a = String(a || '').trim();
  if (!/\d+\s+[A-Za-z]/.test(a) && !/^\d+\s+\d/.test(a)) return false;  // house number + street name, incl. numeric/ordinal streets ("127 2nd Ave")
  if (!/,/.test(a)) return false;                      // has comma-separated parts
  if (!/\b[A-Z]{2}\b\s*\d{0,5}/.test(a) && !/\b(Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|Ohio|Oregon|Pennsylvania|Tennessee|Texas|Utah|Vermont|Virginia|Washington|Wisconsin|Wyoming)\b/i.test(a)) return false;
  return true;
}

let pastors = 0, social = 0, downgrades = 0, flags = 0, addresses = 0;
for (const r of results) {
  const c = byId.get(String(r.id));
  if (!c) continue;

  // Address: set only when the church currently lacks a street address and the
  // researched one is a real, geocodable street address. Clear _geocode_failed
  // so the geocode autopilot re-attempts this church on its next tick.
  if (r.address && goodAddress(r.address)) {
    const curHasStreet = /\d+\s+[A-Za-z]/.test(c.address || '') && /,/.test(c.address || '');
    if (!curHasStreet) {
      c.address = r.address.trim();
      c.address_source = 'agent-research-verified';
      delete c._geocode_failed;
      addresses++;
    }
  }

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
console.log('Applied: +' + addresses + ' addresses, +' + pastors + ' pastors, +' + social + ' social URLs, ' + downgrades + ' rubric downgrades, ' + flags + ' gender-review flags');
