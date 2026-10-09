#!/usr/bin/env node
'use strict';

const fs = require('fs');

function summarizeLines(lines) {
  const result = {
    attempted: 0,
    content_applied: 0,
    pastors_applied: 0,
    socials_applied: 0,
    frontier_applied: 0,
    productive_rounds: 0,
    zero_content_rounds: 0,
    operational_checkpoints: 0,
  };

  for (const line of lines) {
    let m = line.match(/pushed: \+(\d+) content fields \((\d+) pastors, (\d+) socials\).*\((\d+) attempted\)/);
    if (m) {
      const [, content, pastors, socials, attempted] = m.map(Number);
      result.attempted += attempted;
      result.content_applied += content;
      result.pastors_applied += pastors;
      result.socials_applied += socials;
      if (content > 0) result.productive_rounds += 1;
      else result.zero_content_rounds += 1;
      continue;
    }

    m = line.match(/frontier lane done: [\w-]+ attempted=(\d+) applied=(\d+)/);
    if (m) {
      const attempted = Number(m[1]);
      const applied = Number(m[2]);
      result.attempted += attempted;
      result.content_applied += applied;
      result.frontier_applied += applied;
      if (applied > 0) result.productive_rounds += 1;
      else result.zero_content_rounds += 1;
      continue;
    }

    m = line.match(/operational checkpoint pushed: mode=[\w-]+ attempted=(\d+) mutated=(\d+)/);
    if (m) {
      result.attempted += Number(m[1]);
      result.zero_content_rounds += 1;
      result.operational_checkpoints += Number(m[2]) > 0 ? 1 : 0;
    }
  }

  result.other_profile_applied = Math.max(
    0,
    result.content_applied - result.pastors_applied - result.socials_applied - result.frontier_applied,
  );
  return result;
}

function parseArgs(argv) {
  const args = { afterLine: 0 };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === '--log') args.log = argv[++i];
    else if (argv[i] === '--after-line') args.afterLine = Number(argv[++i] || 0);
  }
  if (!args.log) throw new Error('usage: summarize-grind-session.js --log PATH [--after-line N]');
  return args;
}

if (require.main === module) {
  try {
    const args = parseArgs(process.argv.slice(2));
    const lines = fs.readFileSync(args.log, 'utf8').split(/\r?\n/).slice(args.afterLine);
    process.stdout.write(`${JSON.stringify(summarizeLines(lines))}\n`);
  } catch (error) {
    console.error(`summarize-grind-session: ${error.message}`);
    process.exit(2);
  }
}

module.exports = { summarizeLines };
