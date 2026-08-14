#!/usr/bin/env node
/* build-memory-packs.js — compile the Pressure Check memory packs.
 *
 * docs/assets/verse-cache.json is 49 MB and holds the whole Bible in 11
 * translations. A man memorizing twelve verses should not download that, so
 * this pulls only the referenced verses into a small pack file the page can
 * fetch and then keep offline.
 *
 * Packs are declared here rather than hand-authored as JSON so the reference
 * list stays readable and the verse text can never drift from the cache.
 *
 * usage: node scripts/build-memory-packs.js
 */
'use strict';

const fs = require('fs');
const path = require('path');

const REPO = path.dirname(__dirname);
const CACHE = path.join(REPO, 'docs/assets/verse-cache.json');
const OUT = path.join(REPO, 'docs/data/memory-packs.json');

/* Translations offered for memorization. KJV first: it is public domain and is
   the text the Navigators method was built on. The rest ride along because BTE
   already serves them from this same cache. */
const TRANSLATIONS = ['KJV', 'ESV', 'NKJV', 'NASB', 'NIV', 'NLT', 'CSB17', 'WEB'];

const BOOKNUM = {
  Gen:1,Exo:2,Lev:3,Num:4,Deu:5,Jos:6,Jdg:7,Rut:8,'1Sa':9,'2Sa':10,'1Ki':11,'2Ki':12,
  '1Ch':13,'2Ch':14,Ezr:15,Neh:16,Est:17,Job:18,Psa:19,Pro:20,Ecc:21,Son:22,Isa:23,
  Jer:24,Lam:25,Eze:26,Dan:27,Hos:28,Joe:29,Amo:30,Oba:31,Jon:32,Mic:33,Nah:34,Hab:35,
  Zep:36,Hag:37,Zec:38,Mal:39,Mat:40,Mar:41,Luk:42,Joh:43,Act:44,Rom:45,'1Co':46,
  '2Co':47,Gal:48,Eph:49,Php:50,Col:51,'1Th':52,'2Th':53,'1Ti':54,'2Ti':55,Tit:56,
  Phm:57,Heb:58,Jas:59,'1Pe':60,'2Pe':61,'1Jn':62,'2Jn':63,'3Jn':64,Jud:65,Rev:66,
};
const FULLNAME = {
  Gen:'Genesis',Exo:'Exodus',Lev:'Leviticus',Num:'Numbers',Deu:'Deuteronomy',Jos:'Joshua',
  Psa:'Psalm',Pro:'Proverbs',Isa:'Isaiah',Jer:'Jeremiah',Lam:'Lamentations',Eze:'Ezekiel',
  Dan:'Daniel',Mic:'Micah',Hab:'Habakkuk',Zep:'Zephaniah',Mat:'Matthew',Mar:'Mark',
  Luk:'Luke',Joh:'John',Act:'Acts',Rom:'Romans','1Co':'1 Corinthians','2Co':'2 Corinthians',
  Gal:'Galatians',Eph:'Ephesians',Php:'Philippians',Col:'Colossians','1Th':'1 Thessalonians',
  '2Th':'2 Thessalonians','1Ti':'1 Timothy','2Ti':'2 Timothy',Tit:'Titus',Heb:'Hebrews',
  Jas:'James','1Pe':'1 Peter','2Pe':'2 Peter','1Jn':'1 John',Jud:'Jude',Rev:'Revelation',
  Job:'Job',Ecc:'Ecclesiastes',Neh:'Nehemiah','2Ch':'2 Chronicles','1Sa':'1 Samuel',
};

/* A pack is an ordered list. `mode:'verse'` drills each entry on its own;
   `mode:'passage'` still grades verse by verse but presents them in sequence so
   a long passage can be extended a chunk at a time. */
const PACKS = [
  {
    id: 'in-the-chamber',
    name: 'In the Chamber',
    mode: 'verse',
    blurb: 'A round chambered before you need it. Temptation, fear, and the answer already loaded.',
    refs: ['1Co 10:13','Jas 4:7','Eph 6:11','2Co 10:5','Psa 119:11','Isa 41:10',
           'Pro 3:5','Php 4:6','2Ti 1:7','Joh 16:33','Rom 8:1','1Pe 5:8'],
  },
  {
    id: 'foundations',
    name: 'Foundations',
    mode: 'verse',
    blurb: 'The Navigators pattern — the load-bearing verses first. Assurance, lordship, the word.',
    /* 1Jn 5:13 is the classic TMS assurance verse, but all of 1 John 5 is one
       of ~323 verses absent from verse-cache.json. Substituted 1Jn 1:9, which
       is also TMS Series A and is present. Restore 5:13 when the cache gap is
       filled — see data/kjv-gap.json. */
    refs: ['Joh 3:16','Rom 3:23','Rom 6:23','Rom 5:8','Eph 2:8','Rom 10:9',
           '1Jn 1:9','Joh 14:6','2Co 5:17','Gal 2:20','Luk 9:23','2Ti 3:16'],
  },
  {
    id: 'the-gospel-unashamed',
    name: 'Unashamed',
    mode: 'verse',
    blurb: 'The gospel you are not ashamed of, and the righteousness that comes by faith.',
    /* Ranges are one card. Some verses only preach as a pair — Romans 1:16
       without 17 loses the "for therein", and the Great Commission is one
       sentence — so they are drilled the way they are quoted. */
    refs: ['Rom 1:16-17','1Pe 3:15','Mat 28:19-20','Act 1:8'],
  },
  {
    id: 'family-captain',
    name: 'Family Captain',
    mode: 'verse',
    blurb: 'What a man owes the people under his roof.',
    refs: ['Jos 24:15','Eph 5:25','Eph 6:4','Deu 6:6','Deu 6:7','Pro 22:6',
           '1Ti 3:4','Col 3:19','Psa 127:3','1Co 16:13'],
  },
  {
    id: 'sermon-on-the-mount',
    name: 'Sermon on the Mount',
    mode: 'passage',
    blurb: 'The long haul. Matthew 5 start to finish, a chunk at a time.',
    refs: Array.from({ length: 16 }, (_, i) => `Mat 5:${i + 1}`),
  },
];

/* The cache stores KJV with inline Strong's markup — "yourselves<S>5293</S>
   therefore<S>3767</S>" — while ESV and NIV come through clean. Shipping that
   raw would ask a man to memorize concordance numbers, so every translation is
   scrubbed and then gated below. Mirrors bin/kjv_lookup.py's clean(). */
function cleanVerse(s) {
  return s
    .replace(/<S>\d+<\/S>/g, '')           // Strong's tags
    .replace(/<[^>]+>/g, '')               // any other markup (italics for supplied words)
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/\s+([,.;:!?])/g, '$1')       // space pushed before punctuation by tag removal
    /* KJV translators' marginal glosses ride at the end of the verse text:
       "...that ye may be able to bear it. common: or, moderate" and
       "...to the obedience of Christ; imaginations: or, reasonings".
       They are apparatus, not Scripture, and a man drilling word-perfect would
       dutifully memorize them. Same rule as bin/kjv_lookup.py's clean(). */
    .replace(/\s+[A-Za-z][\w-]*:\s+(?:or|Heb|Gr|Gk|Chald|Chal|Called)\b.*$/, '')
    .replace(/\s+/g, ' ')
    .trim();
}

/* No markup, no stray digits, no doubled spaces may reach a memory card. */
function assertClean(ref, tr, text) {
  if (/[<>]/.test(text)) throw new Error(`${ref} ${tr}: markup survived cleaning -> ${text.slice(0, 80)}`);
  if (/\s{2,}/.test(text)) throw new Error(`${ref} ${tr}: doubled whitespace`);
  if (/\s[,.;:]/.test(text)) throw new Error(`${ref} ${tr}: space before punctuation`);
  if (/\b[a-z][\w-]*:\s+(or|Heb|Gr|Gk|Chald|Chal|Called)\b/.test(text))
    throw new Error(`${ref} ${tr}: KJV margin note survived -> ${text.slice(-60)}`);
}

/* "Rom 1:16" or "Rom 1:16-17". A range is ONE card: some verses only preach as
   a pair, and a man quotes them together, so he should drill them together. */
function parseRef(ref) {
  const m = ref.match(/^(\d?[A-Za-z]+)\s+(\d+):(\d+)(?:-(\d+))?$/);
  if (!m) throw new Error(`bad ref: ${ref}`);
  const bn = BOOKNUM[m[1]];
  if (!bn) throw new Error(`unknown book in ref: ${ref}`);
  const from = +m[3], to = m[4] ? +m[4] : from;
  if (to < from) throw new Error(`reversed range: ${ref}`);
  const keys = [];
  for (let v = from; v <= to; v++) keys.push(`${bn}_${m[2]}_${v}`);
  return { keys, book: m[1], ch: +m[2], from, to };
}

const display = (p) =>
  `${FULLNAME[p.book] || p.book} ${p.ch}:${p.from}${p.to > p.from ? `-${p.to}` : ''}`;

function main() {
  console.log('reading verse cache (49 MB)…');
  const cache = JSON.parse(fs.readFileSync(CACHE, 'utf8'));

  const out = { built: new Date().toISOString().slice(0, 10), translations: TRANSLATIONS, packs: [] };
  let missing = 0;

  for (const pack of PACKS) {
    const verses = [];
    for (const ref of pack.refs) {
      const p = parseRef(ref);
      const entries = p.keys.map(k => cache[k]);
      if (entries.some(e => !e)) { console.warn(`  MISS ${ref}`); missing++; continue; }

      const text = {};
      for (const t of TRANSLATIONS) {
        const parts = entries.map(e => (e[t] || '').trim());
        if (parts.some(x => !x)) continue;      // all-or-nothing per translation
        const cleaned = parts.map(cleanVerse).join(' ');
        assertClean(ref, t, cleaned);
        text[t] = cleaned;
      }
      if (!text.KJV) { console.warn(`  MISS KJV ${ref}`); missing++; continue; }

      verses.push({ ref: display(p),
        slug: `${p.book}-${p.ch}-${p.from}${p.to > p.from ? `-${p.to}` : ''}`.toLowerCase(), text });
    }
    out.packs.push({ id: pack.id, name: pack.name, mode: pack.mode, blurb: pack.blurb, verses });
    console.log(`  ${pack.name.padEnd(24)} ${verses.length}/${pack.refs.length} verses`);
  }

  if (missing) throw new Error(`${missing} verse(s) missing from cache — refusing to ship a pack with holes`);

  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(out));
  const kb = (fs.statSync(OUT).size / 1024).toFixed(0);
  console.log(`\nwrote ${path.relative(REPO, OUT)}  ${kb} KB  ${out.packs.length} packs`);
}

main();
