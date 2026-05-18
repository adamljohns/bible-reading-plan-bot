#!/usr/bin/env node
// Phase-status tracker for PROJECT-NETWORKS-SPEAKERS.md
//
// Reads the markdown, counts checked vs total checkboxes per phase,
// writes percentages and progress bars back into the marker spans.
//
// Usage:
//   node scripts/phase-status.js                    # refresh percentages in-place
//   node scripts/phase-status.js --check 1 3        # check off Phase 1 item #3
//   node scripts/phase-status.js --uncheck 2 5      # uncheck Phase 2 item #5
//   node scripts/phase-status.js --print            # print summary, don't write

const fs = require('fs');
const path = require('path');

const MD = path.join(__dirname, '..', 'PROJECT-NETWORKS-SPEAKERS.md');
let md = fs.readFileSync(MD, 'utf8');

const args = process.argv.slice(2);
let printOnly = false;
let checkPhase = null;
let checkItem = null;
let uncheckPhase = null;
let uncheckItem = null;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--print') printOnly = true;
  if (args[i] === '--check') { checkPhase = parseInt(args[++i]); checkItem = parseInt(args[++i]); }
  if (args[i] === '--uncheck') { uncheckPhase = parseInt(args[++i]); uncheckItem = parseInt(args[++i]); }
}

function getPhaseSections() {
  const out = [];
  const re = /(## Phase (\d+) — [^\n]+\n[\s\S]*?)(?=\n## Phase \d+ —|\n## How to run|\n## Pre-flight|\n---\n\n|$)/g;
  let m;
  while ((m = re.exec(md)) !== null) {
    out.push({ num: parseInt(m[2]), body: m[1], start: m.index, end: m.index + m[1].length });
  }
  return out;
}

function toggleItem(phaseNum, itemNum, checked) {
  const sections = getPhaseSections();
  const sec = sections.find(s => s.num === phaseNum);
  if (!sec) { console.error(`Phase ${phaseNum} not found`); return; }
  const lines = sec.body.split('\n');
  let count = 0;
  for (let i = 0; i < lines.length; i++) {
    if (/^- \[[ x]\]/.test(lines[i])) {
      count++;
      if (count === itemNum) {
        lines[i] = lines[i].replace(/^- \[[ x]\]/, checked ? '- [x]' : '- [ ]');
        break;
      }
    }
  }
  md = md.slice(0, sec.start) + lines.join('\n') + md.slice(sec.end);
}

if (checkPhase != null) toggleItem(checkPhase, checkItem, true);
if (uncheckPhase != null) toggleItem(uncheckPhase, uncheckItem, false);

const sections = getPhaseSections();
const phaseStats = {};
let totalChecked = 0, totalTotal = 0;
for (const sec of sections) {
  const checked = (sec.body.match(/^- \[x\]/gm) || []).length;
  const total = (sec.body.match(/^- \[[ x]\]/gm) || []).length;
  phaseStats[sec.num] = { checked, total, pct: total ? Math.round((checked / total) * 100) : 0 };
  totalChecked += checked; totalTotal += total;
}
const overallPct = totalTotal ? Math.round((totalChecked / totalTotal) * 100) : 0;

function bar(pct) {
  const filled = Math.round((pct / 100) * 50);
  return '█'.repeat(filled) + ' '.repeat(50 - filled);
}

md = md.replace(/<!-- OVERALL_PCT:START -->.*?<!-- OVERALL_PCT:END -->/, `<!-- OVERALL_PCT:START -->${overallPct}%<!-- OVERALL_PCT:END -->`);
md = md.replace(/<!-- OVERALL_COUNT:START -->.*?<!-- OVERALL_COUNT:END -->/, `<!-- OVERALL_COUNT:START -->${totalChecked} of ${totalTotal}<!-- OVERALL_COUNT:END -->`);

const phaseLabels = {
  1: 'Phase 1 — Founders cross-reference',
  2: 'Phase 2 — Other networks',
  3: 'Phase 3 — Conference speakers',
  4: 'Phase 4 — Networks page',
  5: 'Phase 5 — Cleanup + polish',
};
const barsBlock = [
  '```',
  ...Object.keys(phaseLabels).map(n => {
    const s = phaseStats[n] || { pct: 0 };
    return `[${bar(s.pct)}] ${String(s.pct).padStart(3)}% ${phaseLabels[n]}`;
  }),
  '```',
].join('\n');
md = md.replace(/```\n\[[^\n]*Phase 1[^\n]+\n[\s\S]*?```/, barsBlock);

for (const num of Object.keys(phaseStats)) {
  const s = phaseStats[num];
  md = md.replace(new RegExp(`<!-- P${num}_PCT:START -->.*?<!-- P${num}_PCT:END -->`), `<!-- P${num}_PCT:START -->${s.pct}%<!-- P${num}_PCT:END -->`);
  md = md.replace(new RegExp(`<!-- P${num}_COUNT:START -->.*?<!-- P${num}_COUNT:END -->`), `<!-- P${num}_COUNT:START -->${s.checked}/${s.total}<!-- P${num}_COUNT:END -->`);
}

md = md.replace(/\*\*Status as of:\*\* \*\(auto-updated below\)\*/, `**Status as of:** ${new Date().toISOString().slice(0, 16).replace('T', ' ')} UTC`);
md = md.replace(/\*\*Status as of:\*\* [\d\- :]+UTC/, `**Status as of:** ${new Date().toISOString().slice(0, 16).replace('T', ' ')} UTC`);

if (!printOnly) fs.writeFileSync(MD, md);

console.log(`\nNetworks + Speakers — overall: ${overallPct}% (${totalChecked}/${totalTotal})`);
for (const num of [1, 2, 3, 4, 5]) {
  const s = phaseStats[num];
  if (s) console.log(`  Phase ${num}: ${String(s.pct).padStart(3)}% (${s.checked}/${s.total}) — ${phaseLabels[num]}`);
}
console.log(printOnly ? '\n(--print mode; file not written)' : `\nUpdated ${path.relative(process.cwd(), MD)}`);
