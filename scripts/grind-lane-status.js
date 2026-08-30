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
const streaks = lanes.loadEmptyStreaks(root);
const planCounts = process.argv.includes('--dry-run') && process.env.GRIND_DRY_RUN_COUNTS
  ? { ...counts, ...JSON.parse(process.env.GRIND_DRY_RUN_COUNTS) }
  : counts;
const selected = lanes.chooseLane(planCounts, arg('--last-mode', ''), streaks);

if (process.argv.includes('--dry-run')) {
  if (selected === 'nothing-to-grind') console.log('NOTHING TO GRIND');
  else console.log(JSON.stringify({ selected, lane_empty_streaks: streaks, ...planCounts }, null, 2));
  process.exit(0);
}

if (process.argv.includes('--mode-only')) console.log(selected);
else console.log(JSON.stringify({ selected, lane_empty_streaks: streaks, ...counts }, null, 2));
