#!/usr/bin/env node
//
// select-address-batch.js — pick the next batch of city-only churches for an
// address-finding round and split it into per-agent group files. Replaces the
// hand-written one-liner the rounds used to inline, and shares the SAME
// hasStreetAddress predicate as the applier and geocoder so the "needs a street"
// definition can never drift between selection and validation.
//
// A church is eligible when it has a name, its address carries a comma (a real
// city line, not an empty field), it lacks a street-level address, and its id is
// not already in the done-list.
//
// Usage:
//   node scripts/select-address-batch.js [--count 24] [--groups 4] \
//        [--done /tmp/addr-done-ids.txt] [--out /tmp/addr-batch.json] \
//        [--group-prefix /tmp/addr-grp-]
//
// Writes the flat batch to --out and one file per group to
// <group-prefix>1.json .. <group-prefix>N.json, then prints the names.

const fs = require('fs');
const path = require('path');
const { hasStreetAddress } = require('./lib/address-util');

function arg(name, def) {
  const i = process.argv.indexOf('--' + name);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : def;
}

const COUNT = parseInt(arg('count', '24'), 10);
const GROUPS = parseInt(arg('groups', '4'), 10);
const DONE = arg('done', '/tmp/addr-done-ids.txt');
const OUT = arg('out', '/tmp/addr-batch.json');
const PREFIX = arg('group-prefix', '/tmp/addr-grp-');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
const done = fs.existsSync(DONE)
  ? new Set(fs.readFileSync(DONE, 'utf8').split('\n').filter(Boolean))
  : new Set();

const eligible = d.churches.filter(c => {
  const id = String(c.id || c.slug);
  return c.name && /,/.test(c.address || '') && !hasStreetAddress(c.address || '') && !done.has(id);
});

const batch = eligible.slice(0, COUNT).map(c => ({
  id: String(c.id || c.slug),
  name: c.name,
  city: c.address,
  denomination: c.denomination || c.denomination_family || '',
  website: c.website || null,
}));

fs.writeFileSync(OUT, JSON.stringify(batch, null, 2));
const per = Math.ceil(batch.length / GROUPS);
for (let i = 0; i < GROUPS; i++) {
  fs.writeFileSync(PREFIX + (i + 1) + '.json', JSON.stringify(batch.slice(i * per, i * per + per), null, 2));
}

console.log('Selected ' + batch.length + ' city-only churches (' + eligible.length + ' truly city-only remaining) into ' + GROUPS + ' groups');
console.log(batch.map(c => c.name + ' — ' + c.city).join('\n'));
