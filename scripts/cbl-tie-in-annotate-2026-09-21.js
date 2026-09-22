#!/usr/bin/env node
// CCW-0921-CBL1 — annotate four live records + post-add enrichment lines.
const path = require('path');
const { makeWriter } = require('./lib/format-preserving-write.js');

const TODAY = '2026-09-21';
const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const { data: d, write } = makeWriter(CHURCHES);

const byId = new Map(d.churches.map(c => [c.id, c]));

function appendNote(c, line) {
  if (c.enrichment_notes && c.enrichment_notes.includes(line.slice(0, 48))) return;
  const stamp = `[${TODAY}] ${line}`;
  c.enrichment_notes = c.enrichment_notes ? `${c.enrichment_notes}\n${stamp}` : stamp;
}

function ensureTag(c, tag) {
  if (!Array.isArray(c.tags)) c.tags = [];
  if (!c.tags.includes(tag)) c.tags.push(tag);
}

// --- Four LIVE annotations ---
const ctk = byId.get('christ-the-king-church-fort-thomas-ky');
if (!ctk) throw new Error('missing christ-the-king-church-fort-thomas-ky');
ctk.pastor = 'Michael Clary';
ctk.pastor_credentials = 'Lead Pastor (Center for Baptist Leadership author bio + christthekingnky.com)';
appendNote(
  ctk,
  'Contributes to the Center for Baptist Leadership (advisory board + contributing scholar). Positive tie-in. CBL is an independent center supported by American Reformer. Pastor Michael Clary verified via https://centerforbaptistleadership.org/author/michael-clary/ and church site.'
);
ensureTag(ctk, 'cbl-tie-in-2026-09-21');

const village = byId.get('village-church-richmond-va');
if (!village) throw new Error('missing village-church-richmond-va');
appendNote(
  village,
  'Dr. Steve Gentry (Lead Pastor) contributes to the Center for Baptist Leadership (advisory board). Dr. Chris Bolt (Equipping and Training Pastor, on roster) contributes to CBL as a contributing scholar. Positive tie-in. CBL is an independent center supported by American Reformer.'
);
ensureTag(village, 'cbl-tie-in-2026-09-21');

const elgin = byId.get('grace-reformed-baptist-elgin-ok');
if (!elgin) throw new Error('missing grace-reformed-baptist-elgin-ok');
if (!Array.isArray(elgin.pastors)) elgin.pastors = [];
const hasDeevers = elgin.pastors.some(p => /deevers/i.test(p.name || ''));
if (!hasDeevers) {
  elgin.pastors.push({ name: 'Dusty Deevers', role: 'Pastor (CBL team page; additional to preaching elder Tod Narcomey)' });
}
appendNote(
  elgin,
  'Tod Narcomey remains primary preaching elder per church site review 2026-05-10. Dusty Deevers named as a pastor at this church on CBL our-team (2026-09-21) — listed in pastors roster, not replacing Narcomey. Contributes to the Center for Baptist Leadership (advisory). Positive tie-in.'
);
ensureTag(elgin, 'cbl-tie-in-2026-09-21');

const truth = byId.get('truth-family-bible-church-middleton-id');
if (!truth) throw new Error('missing truth-family-bible-church-middleton-id');
appendNote(
  truth,
  'Pastor Danny Steinmeyer serves on the TruthScript board (truthscript.com/about) and pastors this congregation. Positive TruthScript tie-in — explicit Church Finder / board connection.'
);
ensureTag(truth, 'truthscript-church-finder');
ensureTag(truth, 'cbl-tie-in-2026-09-21');

const cityZip = {
  'grace-baptist-church-cape-coral': { city: 'Cape Coral', zip: '33991' },
  'woodlawn-baptist-church-baton-rouge': { city: 'Baton Rouge', zip: '70817' },
  'the-well-church': { city: 'Boulder', zip: '80305' },
  'cumberland-homesteads-baptist-church': { city: 'Crossville', zip: '38572' },
};
for (const [id, loc] of Object.entries(cityZip)) {
  const c = byId.get(id);
  if (c) {
    if (!c.city) c.city = loc.city;
    if (!c.zip) c.zip = loc.zip;
  }
}

// --- Six directory targets (four new slugs + two existing dedups) ---
const newAnnotations = {
  'grace-baptist-church-cape-coral': c =>
    appendNote(
      c,
      'Contributes to the Center for Baptist Leadership (advisory / author). Positive. Tom Ascol — Founders Ministries president. Do not confuse with generic grace-baptist-church.html (BGAV / Wingate). CBL is an independent center supported by American Reformer.'
    ),
  'woodlawn-baptist-church-baton-rouge': c =>
    appendNote(
      c,
      'Contributes to the Center for Baptist Leadership (advisory board). Positive. Lewis Richerson — Senior Pastor since 2012 (church contributor page + CBL). Not woodlawn-baptist-church.html (Tony Lowery / BGAV).'
    ),
  'university-park-baptist-church-houston-texas': c =>
    appendNote(
      c,
      'Sam Webb (elder, not preaching pastor) contributes to CBL (advisory board). Travis Cardwell is Preaching Pastor per church elders page. Positive CBL tie-in. Josh Abbotoy is a member, not pastor.'
    ),
  'the-well-church': c =>
    appendNote(
      c,
      'Contributes to the Center for Baptist Leadership (contributing scholar — Chase Davis named on CBL scholars page). Positive. Pastor string held empty until leadership page prints name verbatim on church site.'
    ),
  'cumberland-homesteads-baptist-church': c =>
    appendNote(
      c,
      'Contributes to the Center for Baptist Leadership (contributing scholar). Positive. Dr. Jared Moore, Senior Pastor — verified on church staff page.'
    ),
  'stone-mountain-baptist-1689-nampa-id': c =>
    appendNote(
      c,
      'Contributes to TruthScript (contributor / co-host). Positive. Gabriel Render — Primary Preaching and Vocational Elder per church leadership page. Not stone-mountain-baptist-church.html (Greg Lamb / BGAV).'
    ),
};

for (const [id, fn] of Object.entries(newAnnotations)) {
  const c = byId.get(id);
  if (!c) {
    console.warn(`WARN: expected new slug ${id} not found — run add-discovered first`);
    continue;
  }
  fn(c);
  ensureTag(c, 'cbl-tie-in-2026-09-21');
}

if ('total_churches' in d) d.total_churches = d.churches.length;
write(d);
console.log('CBL tie-in annotations written.');
