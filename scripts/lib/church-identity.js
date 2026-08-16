/**
 * One definition of "is this the same church?" — shared by the duplicate-merge
 * engine and the denominational-roster matcher.
 *
 * Extracted verbatim from scripts/merge-duplicate-churches.js on 2026-08-16 when
 * the roster harvester needed the same question answered. Two copies would drift,
 * and the failure mode is exactly the one Adam called out: the harvester adds a
 * church the dedupe engine would have called a duplicate, and the directory grows
 * near-identical entries that differ only by a word in the name.
 *
 * Adam's rule for telling duplicates apart (2026-08-12): match on city within
 * state, then corroborate with address or pastor.
 */

// ── name normalization ───────────────────────────────────────────────────────
const norm = s => String(s || '').toLowerCase().replace(/&/g, ' and ')
  .replace(/[^a-z0-9 ]/g, ' ').replace(/\b1st\b/g, 'first').replace(/\b2nd\b/g, 'second')
  .replace(/\bmt\b/g, 'mount').replace(/\s+/g, ' ').trim();

const NOISE = new Set(['the', 'of', 'at', 'in', 'inc', 'a']);

/** Order-independent name signature: "First Baptist" === "Baptist, First". */
const sig = n => norm(n).split(' ').filter(t => t && !NOISE.has(t)).sort().join('|');

// Generic tokens — a name is DISTINCTIVE if it carries a >=5-char token outside
// this set. "Grace Baptist Church" is not distinctive (hundreds share it);
// "Massaponax Baptist Church" is.
const GENERIC = new Set(['church', 'churches', 'baptist', 'first', 'second', 'community', 'grace', 'christ', 'christian', 'fellowship', 'bible', 'ministries', 'ministry', 'chapel', 'saint', 'trinity', 'calvary', 'cornerstone', 'hope', 'faith', 'life', 'family', 'worship', 'center', 'centre', 'assembly', 'gospel', 'covenant', 'reformed', 'presbyterian', 'lutheran', 'methodist', 'pentecostal', 'catholic', 'orthodox', 'missionary', 'memorial', 'mount', 'valley', 'river', 'creek', 'lake', 'park', 'north', 'south', 'east', 'west', 'springs', 'heights', 'hills', 'grove', 'road', 'street', 'avenue', 'united', 'evangelical', 'emmanuel', 'immanuel', 'bethel', 'bethany', 'zion', 'antioch', 'shiloh', 'ebenezer', 'providence', 'redeemer', 'resurrection', 'ascension', 'nazarene', 'wesleyan', 'anglican', 'episcopal', 'apostolic', 'temple', 'tabernacle', 'house', 'living', 'light', 'truth', 'word', 'spirit', 'holy', 'good', 'shepherd', 'sovereign', 'victory', 'harvest', 'heritage', 'liberty', 'freedom', 'pleasant', 'friendship', 'union', 'central', 'highland', 'ridge', 'point', 'pointe', 'crossroads', 'journey', 'mission', 'anchor', 'lighthouse', 'kings', 'kingdom']);

const distinctive = n => norm(n).split(' ').some(t => t.length >= 5 && !GENERIC.has(t));

// ── address / identity fields ────────────────────────────────────────────────
const zipOf = c => { const m = String(c.address || '').match(/\b(\d{5})(?:-\d{4})?\s*$/); return m ? m[1] : null; };

const cityOf = c => {
  const a = String(c.address || '');
  const m = a.match(/,\s*([A-Za-z .'-]+?),?\s+(?:[A-Z]{2}|Virginia|Texas|Florida|Georgia|Alabama|Tennessee|Carolina|Kentucky|Ohio|Indiana|Illinois|Missouri|Michigan|California|Oklahoma|Arkansas|Louisiana|Mississippi|Washington|Oregon|Colorado|Arizona|Pennsylvania|York|Jersey|Maryland|Massachusetts)\b/);
  return m ? norm(m[1]) : null;
};

/**
 * cityOf(), plus the `city` field and bare "City, ST" addresses.
 *
 * cityOf() requires a comma BEFORE the city, so a record whose whole address is
 * "Charlottesville, VA" yields null and cannot be blocked on. That is fine for
 * the merge engine, which is deliberately conservative about what it will call
 * the same church, but it makes such records permanently unmatchable against a
 * roster. Kept separate rather than loosening cityOf() so merge behaviour is
 * unchanged.
 */
const cityOfLoose = c => {
  const strict = cityOf(c);
  if (strict) return strict;
  if (c.city && String(c.city).trim()) return norm(c.city);
  const m = String(c.address || '').match(/^\s*([A-Za-z .'-]{3,}?),\s*(?:[A-Z]{2}|Virginia)\b/);
  return m ? norm(m[1]) : null;
};

/** House number + first street word: "1234|main". Cheap, robust to suffix noise. */
const streetOf = c => { const m = String(c.address || '').match(/\b(\d{1,6})\s+([A-Za-z]+)/); return m ? (m[1] + '|' + m[2].toLowerCase()) : null; };

// Directionals and suffixes, so "714 S Monroe St" and "714 South Monroe Street"
// stop looking like two different addresses.
const DIRECTIONAL = { n: 'north', s: 'south', e: 'east', w: 'west', ne: 'northeast', nw: 'northwest', se: 'southeast', sw: 'southwest' };
const SUFFIX = { st: 'street', rd: 'road', ave: 'avenue', av: 'avenue', dr: 'drive', ln: 'lane', blvd: 'boulevard', hwy: 'highway', tpke: 'turnpike', pkwy: 'parkway', ct: 'court', cir: 'circle', pl: 'place', ter: 'terrace', trl: 'trail', pk: 'park' };

/**
 * Full normalized street: house number plus every road word expanded and sorted
 * out of directional/suffix abbreviation. Returns null without a house number.
 *
 * streetOf() keeps only the FIRST word after the number, which made "776
 * Viewtown Rd" and "776 View Town Road" disagree (viewtown vs view) while
 * "1111 S Carolina Ave SE" and "1111 South Carolina Avenue SE" disagreed on
 * s vs south. Both are the same building.
 */
const streetFull = c => {
  const a = String(c.address || '');
  const m = a.match(/\b(\d{1,6})\s+(.+?)(?:,|$)/);
  if (!m) return null;
  const words = m[2].toLowerCase().replace(/[^a-z0-9 ]/g, ' ').split(/\s+/).filter(Boolean)
    .map(w => DIRECTIONAL[w] || SUFFIX[w] || w);
  return m[1] + '|' + words.join('');
};

/** Do two records name streets that genuinely differ? Unknown street => false. */
const streetsDiffer = (a, b) => {
  const x = streetFull(a), y = streetFull(b);
  if (!x || !y) return false;
  if (x === y) return false;
  // Same house number and one street name contains the other ("22264 Main St"
  // vs "22264/22265 Main St") is not a conflict.
  const [xn, xs] = x.split('|'), [yn, ys] = y.split('|');
  if (xn === yn && (xs.includes(ys) || ys.includes(xs))) return false;
  return true;
};

/** Placeholder pastor — the directory's honest-blank convention. */
const isPh = p => { p = String(p || '').trim().toLowerCase(); return !p || /verify|see website|see site|not published|search in progress|to be announced|to be determined|coming soon/.test(p) || /^((the |a )?(pastor|pastors|elder|elders|staff|tbd|n\/a|none|unknown|various))$/.test(p); };

const pastorKey = c => { if (isPh(c.pastor)) return null; return norm(String(c.pastor).replace(/\b(rev|dr|pastor|elder|bro|mr|fr|bishop|min)\.?\b/gi, '')).split(' ').slice(0, 3).join(' ') || null; };

const domainOf = c => { try { const h = new URL(c.website).hostname.replace(/^www\./, ''); return h.split('.').slice(-2).join('.'); } catch (_) { return null; } };

const fbOf = c => { const m = String(c.facebook || '').match(/facebook\.com\/([^/?#]+)/i); return m ? m[1].toLowerCase() : null; };

const famCoarse = c => {
  const s = String(c.denomination_family || c.denomination || '').toLowerCase();
  for (const f of ['anabaptist', 'baptist', 'presbyterian|reformed|pca|opc', 'anglican|episcopal', 'lutheran', 'methodist|wesleyan|nazarene', 'pentecostal|charismatic|assembl|foursquare|vineyard|calvary chapel', 'catholic|orthodox']) {
    if (new RegExp(f).test(s)) return f;
  }
  return 'other';
};

module.exports = {
  norm, NOISE, sig, GENERIC, distinctive,
  zipOf, cityOf, cityOfLoose, streetOf, streetFull, streetsDiffer, isPh, pastorKey, domainOf, fbOf, famCoarse,
};
