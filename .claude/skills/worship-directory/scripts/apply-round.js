#!/usr/bin/env node
// Extract PD hymns from a workflow task output file -> write a hymns.json for assemble.
//   node apply-round.js <task-output.json> <out-hymns.json>
const fs = require('fs');
const [inp, out] = process.argv.slice(2);
const wrap = JSON.parse(fs.readFileSync(inp, 'utf8'));
let r = wrap.result != null ? wrap.result : wrap;
if (typeof r === 'string') r = JSON.parse(r);
const hymns = (r.hymns || []).filter((h) => h && h.title && h.publicDomain && h.lyrics && h.lyrics.length > 60);
fs.writeFileSync(out, JSON.stringify(hymns, null, 1));
console.log(`extracted ${hymns.length} PD hymns from ${inp}`);
