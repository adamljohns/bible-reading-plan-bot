#!/usr/bin/env node
'use strict';
const fs = require('fs');
const path = require('path');
const lanes = require('./lib/grind-lanes.js');
const root = path.join(__dirname, '..');
const churches = JSON.parse(fs.readFileSync(path.join(root, 'docs/data/churches.json'), 'utf8')).churches;
const arg = (name, fallback) => {
  const i = process.argv.indexOf(name);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
};
const counts = lanes.countLanes(churches);
const selected = lanes.chooseLane(counts, arg('--last-mode', ''));
if (process.argv.includes('--mode-only')) console.log(selected);
else console.log(JSON.stringify({ selected, ...counts }, null, 2));
