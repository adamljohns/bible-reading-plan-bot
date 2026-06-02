//
// address-util.js — one shared home for the MOOP Church Directory's address
// predicates, so the applier, the batch selector, and the geocoder all agree.
//
// Background: the "does this church already have a street address" test used to
// live as a hand-copied regex in three separate places, and when one copy was
// hardened the others drifted; that is how numeric/ordinal street names like
// "127 2nd Ave" and "2225 19th St" came to pass one check while silently failing
// another. Keeping the logic here means a single edit fixes every caller.
//
//   hasStreetAddress(a) — true when the string carries a real house-number +
//     street (including ordinal/numeric streets) plus a comma; false for a
//     city-only string or a bare PO box.
//   goodAddress(a) — hasStreetAddress AND a 2-letter or spelled-out US state, so
//     the geocoder can actually place it. This is the bar a researched address
//     must clear before it is written to a record.
//   normalizeAddress(a) — spelled state -> abbreviation, strip "United States",
//     repair missing commas; mirrors the geocoder's own normalization.
//

const STATE_ABBR = {
  alabama:'AL',alaska:'AK',arizona:'AZ',arkansas:'AR',california:'CA',colorado:'CO',
  connecticut:'CT',delaware:'DE',florida:'FL',georgia:'GA',hawaii:'HI',idaho:'ID',
  illinois:'IL',indiana:'IN',iowa:'IA',kansas:'KS',kentucky:'KY',louisiana:'LA',
  maine:'ME',maryland:'MD',massachusetts:'MA',michigan:'MI',minnesota:'MN',
  mississippi:'MS',missouri:'MO',montana:'MT',nebraska:'NE',nevada:'NV',
  'new hampshire':'NH','new jersey':'NJ','new mexico':'NM','new york':'NY',
  'north carolina':'NC','north dakota':'ND',ohio:'OH',oklahoma:'OK',oregon:'OR',
  pennsylvania:'PA','rhode island':'RI','south carolina':'SC','south dakota':'SD',
  tennessee:'TN',texas:'TX',utah:'UT',vermont:'VT',virginia:'VA',washington:'WA',
  'west virginia':'WV',wisconsin:'WI',wyoming:'WY','district of columbia':'DC'
};

// Built from STATE_ABBR so every state (and DC) is covered; the old inline copy
// was missing eleven states, including the two-word ones.
const SPELLED_STATE = new RegExp(
  '\\b(' + Object.keys(STATE_ABBR).map(s => s.replace(/ /g, '\\s+')).join('|') + ')\\b',
  'i'
);

// House number followed by a street name (letter-led OR ordinal/numeric-led).
function hasStreetAddress(a) {
  a = String(a == null ? '' : a);
  const hasNumberedStreet = /\d+\s+[A-Za-z]/.test(a) || /^\s*\d+\s+\d/.test(a);
  return hasNumberedStreet && /,/.test(a);
}

// A researched address fit to write + geocode: a numbered street plus a state.
function goodAddress(a) {
  a = String(a == null ? '' : a).trim();
  if (!hasStreetAddress(a)) return false;
  return /\b[A-Z]{2}\b\s*\d{0,5}/.test(a) || SPELLED_STATE.test(a);
}

function normalizeAddress(addr) {
  if (!addr) return addr;
  let s = String(addr);
  s = s.replace(/,?\s*United States of America\b/gi, '');
  s = s.replace(/,?\s*United States\b/gi, '');
  s = s.replace(/,?\s*USA\b/g, '');
  const names = Object.keys(STATE_ABBR).sort((a, b) => b.length - a.length);
  for (const name of names) {
    const re = new RegExp('\\b' + name.replace(/ /g, '\\s+') + '\\b', 'i');
    if (re.test(s)) { s = s.replace(re, STATE_ABBR[name]); break; }
  }
  s = s.replace(/([a-z])\s+([A-Z]{2})(\s+\d{5})/g, '$1, $2$3');
  s = s.replace(/,\s*,/g, ',').replace(/\s{2,}/g, ' ').trim().replace(/,\s*$/, '');
  return s;
}

module.exports = { STATE_ABBR, SPELLED_STATE, hasStreetAddress, goodAddress, normalizeAddress };
