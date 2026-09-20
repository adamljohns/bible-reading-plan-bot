#!/usr/bin/env node
// CCW-0919 — bounded FXBG own-site ministry flag pass (Chaps strike ticket)
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { makeWriter } = require('./lib/format-preserving-write.js');

const CHURCHES = path.join(__dirname, '..', 'docs/data/churches.json');
const TODAY = '2026-09-19';
const KIDS_RE = /\b(nursery|children'?s?\s+ministr|kids?\s+ministr|youth\s+(group|ministr)|vacation\s+bible\s+school|\bvbs\b|sunday\s+school|junior\s+worship|boys?\s+brigade|pioneer\s+girls)\b/i;
const MEN_RE = /\b(men'?s?\s+(ministr|fellowship|group|discipleship|retreat|breakfast|bible\s+study)|christian\s+service\s+brigade|boys?\s+brigade|battalion)\b/i;

function fetchText(url) {
  try {
    const out = execFileSync('curl', ['-sL', '--max-time', '12', '-A', 'MOOP-ChurchDirectory/1.0', url], {
      encoding: 'utf8',
      maxBuffer: 2 * 1024 * 1024,
    });
    return out.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ');
  } catch (_) {
    return '';
  }
}

function noteAppend(church, line) {
  const prev = church.enrichment_notes || '';
  church.enrichment_notes = prev ? `${prev}\n${line}` : line;
}

const { data, write } = makeWriter(CHURCHES);
const churches = data.churches;
const flips = [];
const manual = {
  'new-life-in-christ-church-fredericksburg': {
    has_kids_ministry: true,
    has_mens_ministry: true,
    kids_url: 'https://nlicc.org/childrens-ministry',
    mens_url: 'https://nlicc.org/childrens-ministry',
    mens_note: 'Christian Service Brigade / Boys Brigade (fathers+sons) on own site',
  },
};

for (const id of Object.keys(manual)) {
  const c = churches.find(x => (x.slug || x.id) === id);
  if (!c) continue;
  const m = manual[id];
  if (m.has_kids_ministry && !c.has_kids_ministry) {
    c.has_kids_ministry = true;
    flips.push({ slug: id, flag: 'kids', url: m.kids_url });
    noteAppend(c, `[${TODAY}] Quick Facts Kids→Yes: own site lists nursery, Sunday school, VBS (${m.kids_url}).`);
  }
  if (m.has_mens_ministry && !c.has_mens_ministry) {
    c.has_mens_ministry = true;
    flips.push({ slug: id, flag: 'mens', url: m.mens_url });
    noteAppend(c, `[${TODAY}] Quick Facts Men's→Yes: ${m.mens_note} (${m.mens_url}).`);
  }
  if (c.engagement) c.engagement.researched_website = true;
}

const targets = churches.filter(c =>
  c.region === 'fxbg' &&
  typeof c.website === 'string' &&
  /^https?:\/\//i.test(c.website) &&
  (c.has_kids_ministry === false || c.has_mens_ministry === false) &&
  !manual[c.slug || c.id]
);

for (const c of targets) {
  const id = c.slug || c.id;
  const urls = new Set([c.website.replace(/\/$/, '')]);
  for (const ql of c.quick_links || []) {
    if (ql && ql.url && /ministr|children|kids|youth|men|family|nursery/i.test(`${ql.label} ${ql.url}`)) {
      urls.add(ql.url);
    }
  }
  let blob = '';
  const hitUrls = { kids: [], mens: [] };
  for (const url of urls) {
    const text = fetchText(url);
    if (!text) continue;
    blob += ' ' + text;
    if (KIDS_RE.test(text)) hitUrls.kids.push(url);
    if (MEN_RE.test(text)) hitUrls.mens.push(url);
    if (hitUrls.kids.length && hitUrls.mens.length) break;
  }
  if (c.has_kids_ministry === false && hitUrls.kids.length) {
    c.has_kids_ministry = true;
    const u = hitUrls.kids[0];
    flips.push({ slug: id, flag: 'kids', url: u });
    noteAppend(c, `[${TODAY}] Quick Facts Kids→Yes: own-site crawl (${u}).`);
  }
  if (c.has_mens_ministry === false && hitUrls.mens.length) {
    c.has_mens_ministry = true;
    const u = hitUrls.mens[0];
    flips.push({ slug: id, flag: 'mens', url: u });
    noteAppend(c, `[${TODAY}] Quick Facts Men's→Yes: own-site crawl (${u}).`);
  }
}

write(data);
console.log(JSON.stringify({ flipped: flips.length, flips }, null, 2));
