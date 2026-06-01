#!/bin/bash
# contact-sheet.sh — build an HTML grid of every church's logo + hero in a
# scope, so a human (or vision pass) can eyeball them all at once for
# wrong-church / low-quality images. Writes /tmp/logo-sheet.html and prints
# the path; open it in a browser and screenshot.
#
# Usage:
#   bash contact-sheet.sh Fredericksburg
#   bash contact-sheet.sh VA

set -u
cd "$(dirname "$0")/../../../.." || { echo "repo root not found"; exit 1; }

export SHEET_SCOPE="${1:-Fredericksburg}"
OUT="/tmp/logo-sheet.html"

node -e "
const fs = require('fs');
const scope = process.env.SHEET_SCOPE;
const d = JSON.parse(fs.readFileSync('docs/data/churches.json','utf8'));
let pool = d.churches.filter(c => new RegExp(scope, 'i').test(c.address||''));
pool.sort((a,b)=> (a.name||'').localeCompare(b.name||''));

const esc = s => String(s||'').replace(/[&<>\"]/g, ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[ch]));
let cells = '';
for (const c of pool) {
  const logo = c.image_thumb && /^https?:/.test(c.image_thumb) ? c.image_thumb : '';
  const hero = c.image_url && /^https?:/.test(c.image_url) ? c.image_url : '';
  cells += '<div class=cell>' +
    '<div class=name>' + esc(c.name) + '</div>' +
    '<div class=imgs>' +
      '<div class=logo>' + (logo ? '<img src=\"'+esc(logo)+'\" loading=lazy>' : '<span class=none>no logo</span>') + '<div class=lbl>logo</div></div>' +
      '<div class=hero>' + (hero ? '<img src=\"'+esc(hero)+'\" loading=lazy>' : '<span class=none>no hero</span>') + '<div class=lbl>hero</div></div>' +
    '</div>' +
  '</div>';
}

const html = '<!DOCTYPE html><html><head><meta charset=utf-8><style>' +
  'body{background:#111;color:#ddd;font-family:system-ui,sans-serif;margin:0;padding:16px;}' +
  'h1{color:#D4AF37;font-size:18px;margin:0 0 14px;}' +
  '.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;}' +
  '.cell{background:#1a1a1a;border:1px solid #333;border-radius:8px;padding:10px;}' +
  '.name{font-size:12px;color:#F4D470;margin-bottom:8px;height:30px;overflow:hidden;line-height:1.25;}' +
  '.imgs{display:flex;gap:8px;}' +
  '.logo,.hero{flex:1;text-align:center;}' +
  '.logo img{width:64px;height:64px;object-fit:contain;background:#fff;border-radius:6px;padding:3px;}' +
  '.hero img{width:100%;height:64px;object-fit:cover;border-radius:6px;}' +
  '.lbl{font-size:9px;color:#888;margin-top:3px;text-transform:uppercase;letter-spacing:1px;}' +
  '.none{display:inline-flex;align-items:center;justify-content:center;width:64px;height:64px;background:#0a0a0a;border:1px dashed #444;border-radius:6px;font-size:9px;color:#666;}' +
  '.hero .none{width:100%;}' +
  '</style></head><body>' +
  '<h1>Image contact sheet — ' + esc(scope) + ' (' + pool.length + ' churches)</h1>' +
  '<div class=grid>' + cells + '</div></body></html>';

fs.writeFileSync('$OUT', html);
console.log('Wrote $OUT (' + pool.length + ' churches)');
"
echo "$OUT"
