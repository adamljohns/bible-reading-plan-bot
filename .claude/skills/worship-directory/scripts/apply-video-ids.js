#!/usr/bin/env node
// Validate researched YouTube IDs and merge them into docs/data/worship-overrides.json.
// Run from the repo root.
//   node apply-video-ids.js <researched.json>
//
// <researched.json> is [{slug, youtube, confidence, why}] — typically the
// `videos` array out of a video-link workflow round.
//
// Rejects (loudly, never silently):
//   - malformed IDs (YouTube IDs are exactly 11 chars of [A-Za-z0-9_-])
//   - slugs not in the directory
//   - low confidence (agent unsure = no link; a wrong video is worse than none)
//   - duplicate IDs — the classic agent failure is pasting one popular video
//     onto several songs, so an ID already used anywhere is refused.
const fs = require('fs');
const path = require('path');
const REPO = process.cwd();
const inp = process.argv[2];
const songs = JSON.parse(fs.readFileSync(path.join(REPO, 'docs/data/worship-songs.json'), 'utf8'));
const known = new Set(songs.map((s) => s.slug));
const OV_PATH = path.join(REPO, 'docs/data/worship-overrides.json');
const ov = fs.existsSync(OV_PATH) ? JSON.parse(fs.readFileSync(OV_PATH, 'utf8')) : {};

const usedIds = new Set();
for (const k of Object.keys(ov)) if (ov[k] && ov[k].youtube) usedIds.add(ov[k].youtube);
for (const s of songs) if (s.youtube) usedIds.add(s.youtube);

let raw = JSON.parse(fs.readFileSync(inp, 'utf8'));
if (raw && !Array.isArray(raw)) raw = raw.videos || raw.result || [];

const ID = /^[A-Za-z0-9_-]{11}$/;
let added = 0; const rejected = [];
for (const v of raw) {
  const slug = (v && v.slug || '').trim();
  const id = (v && v.youtube || '').trim();
  if (!ID.test(id)) { rejected.push(`${slug}: malformed id "${id}"`); continue; }
  if (!known.has(slug)) { rejected.push(`${slug}: not in directory`); continue; }
  if (v.confidence && /low|unsure|guess/i.test(v.confidence)) { rejected.push(`${slug}: low confidence`); continue; }
  if (usedIds.has(id)) { rejected.push(`${slug}: id ${id} already used by another song`); continue; }
  if (ov[slug] && ov[slug].youtube) { rejected.push(`${slug}: already has a video`); continue; }
  ov[slug] = Object.assign({}, ov[slug], { youtube: id });
  usedIds.add(id); added++;
}
fs.writeFileSync(OV_PATH, JSON.stringify(ov, null, 1));
console.log(`applied ${added} video links (${rejected.length} rejected)`);
for (const r of rejected) console.log('  reject:', r);
