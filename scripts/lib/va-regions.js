/**
 * Virginia region classifier — ZIP-first, city-fallback.
 *
 * Regions were originally assigned ad hoc by whichever import wave created the
 * record, which is why 326 VA churches sat in "virginia-other" and ~68 in the
 * Roanoke / far-southwest had no home at all (Adam, 2026-08-16: add a real
 * "Roanoke / Southwest VA" region rather than folding them into Shenandoah).
 *
 * ZIP is the primary signal because it is mechanical and unambiguous; city name
 * is the fallback for records whose address has no parseable ZIP. Nothing here
 * guesses: a record that yields neither ZIP nor recognizable city stays
 * 'virginia-other' rather than being filed somewhere plausible-but-wrong.
 *
 * Virginia ZIP geography (USPS):
 *   201xx, 220xx-223xx  Northern Virginia .......... dc-nova
 *   224xx-225xx         Fredericksburg ............. fxbg
 *   226xx               Winchester ................. shenandoah
 *   227xx               Culpeper ................... virginia-other (piedmont)
 *   228xx               Harrisonburg ............... shenandoah
 *   229xx               Charlottesville ............ charlottesville
 *   230xx-232xx         Richmond ................... richmond
 *   233xx-235xx         Norfolk / Virginia Beach ... hampton-roads
 *   236xx               Newport News / Williamsburg  peninsula
 *   237xx               Portsmouth ................. hampton-roads
 *   238xx-239xx         Petersburg / Farmville ..... virginia-other (southside)
 *   240xx-243xx, 246xx  Roanoke + far southwest .... roanoke-swva
 *   244xx               Staunton / Lexington ....... shenandoah (upper valley)
 *   245xx               Lynchburg .................. lynchburg
 */

const REGIONS = [
  'fxbg', 'dc-nova', 'richmond', 'charlottesville', 'hampton-roads',
  'peninsula', 'shenandoah', 'roanoke-swva', 'lynchburg', 'virginia-other',
];

// 244xx straddles two worlds: Staunton/Lexington are canonically Shenandoah
// Valley, while the Alleghany Highlands (Covington, Clifton Forge, Hot Springs)
// look west to Roanoke. Split by city rather than pretending the ZIP decides.
const ALLEGHANY = /^(covington|clifton forge|hot springs|iron gate|low moor|callaghan)$/i;

// Cities whose ZIP prefix lies on the far side of a river or a mountain from
// where the town actually belongs. A named city is a more specific signal than
// a three-digit prefix, so these are consulted BEFORE the ZIP table.
//
// Found by spot-checking the 2026-08-16 dry run: 230xx reaches across the York
// River, so the Middle Peninsula (Gloucester, Hayes, White Marsh) was being
// filed as Richmond; and 229xx reaches over the Blue Ridge, so Waynesboro —
// canonically Shenandoah Valley — was being pulled into Charlottesville.
const CITY_OVERRIDE = new Map(Object.entries({
  // Middle Peninsula / Historic Triangle — 230xx & 231xx, but peninsula
  gloucester: 'peninsula', 'gloucester point': 'peninsula', hayes: 'peninsula',
  'white marsh': 'peninsula', ordinary: 'peninsula', mathews: 'peninsula',
  williamsburg: 'peninsula', toano: 'peninsula', lightfoot: 'peninsula',
  norge: 'peninsula', yorktown: 'peninsula', poquoson: 'peninsula',
  seaford: 'peninsula', grafton: 'peninsula',
  // West of the Blue Ridge despite a 229xx (Charlottesville) ZIP
  waynesboro: 'shenandoah', 'stuarts draft': 'shenandoah', crimora: 'shenandoah',
}));

// Cities used only when a record has no parseable ZIP.
const CITY_REGION = new Map(Object.entries({
  // Roanoke / Southwest
  roanoke: 'roanoke-swva', salem: 'roanoke-swva', blacksburg: 'roanoke-swva',
  christiansburg: 'roanoke-swva', radford: 'roanoke-swva', pulaski: 'roanoke-swva',
  wytheville: 'roanoke-swva', bristol: 'roanoke-swva', abingdon: 'roanoke-swva',
  marion: 'roanoke-swva', galax: 'roanoke-swva', vinton: 'roanoke-swva',
  'rocky mount': 'roanoke-swva', daleville: 'roanoke-swva', troutville: 'roanoke-swva',
  bluefield: 'roanoke-swva', tazewell: 'roanoke-swva', richlands: 'roanoke-swva',
  'big stone gap': 'roanoke-swva', norton: 'roanoke-swva', wise: 'roanoke-swva',
  lebanon: 'roanoke-swva', 'natural bridge': 'roanoke-swva', covington: 'roanoke-swva',
  'clifton forge': 'roanoke-swva', floyd: 'roanoke-swva', hillsville: 'roanoke-swva',
  // Shenandoah
  winchester: 'shenandoah', harrisonburg: 'shenandoah', staunton: 'shenandoah',
  waynesboro: 'shenandoah', lexington: 'shenandoah', 'front royal': 'shenandoah',
  strasburg: 'shenandoah', woodstock: 'shenandoah', luray: 'shenandoah',
  'buena vista': 'shenandoah', 'penn laird': 'shenandoah', bridgewater: 'shenandoah',
  // Lynchburg
  lynchburg: 'lynchburg', bedford: 'lynchburg', forest: 'lynchburg',
  amherst: 'lynchburg', altavista: 'lynchburg',
}));

/** Extract a 5-digit ZIP from any address shape we carry. */
function zipOf(c) {
  const hay = `${c.address || ''} ${c.zip || ''} ${c.postal_code || ''}`;
  const m = hay.match(/\b(2[0-4]\d{3})\b/);
  return m ? m[1] : null;
}

/** Extract a city, tolerating "City, VA 22222", "City Virginia, ...", bare city fields. */
function cityOf(c) {
  if (c.city && String(c.city).trim()) return String(c.city).trim();
  const a = String(c.address || '');
  const pats = [
    /,\s*([A-Za-z .'-]{3,}?),?\s*(?:VA|Virginia)\b/i,
    /\b([A-Za-z .'-]{3,}?)\s+(?:VA|Virginia)\s*,?\s*\d{5}/i,
  ];
  for (const p of pats) { const m = a.match(p); if (m) return m[1].trim(); }
  return '';
}

/**
 * Classify a Virginia church into a region.
 * Returns one of REGIONS. Never guesses — unknown stays 'virginia-other'.
 */
function regionOf(c) {
  const override = CITY_OVERRIDE.get(cityOf(c).toLowerCase());
  if (override) return override;
  const zip = zipOf(c);
  if (zip) {
    const p3 = zip.slice(0, 3);
    if (p3 === '201' || (p3 >= '220' && p3 <= '223')) return 'dc-nova';
    if (p3 === '224' || p3 === '225') return 'fxbg';
    if (p3 === '226' || p3 === '228') return 'shenandoah';
    if (p3 === '229') return 'charlottesville';
    if (p3 >= '230' && p3 <= '232') return 'richmond';
    if (p3 >= '233' && p3 <= '235') return 'hampton-roads';
    if (p3 === '236') return 'peninsula';
    if (p3 === '237') return 'hampton-roads';
    if (p3 === '245') return 'lynchburg';
    if (p3 === '244') return ALLEGHANY.test(cityOf(c)) ? 'roanoke-swva' : 'shenandoah';
    if ((p3 >= '240' && p3 <= '243') || p3 === '246') return 'roanoke-swva';
    return 'virginia-other'; // 227xx piedmont, 238xx-239xx southside
  }
  const city = cityOf(c).toLowerCase();
  return CITY_REGION.get(city) || 'virginia-other';
}

/**
 * Region to actually WRITE for an existing record — regionOf() plus a
 * no-demotion guard.
 *
 * regionOf() returns 'virginia-other' for two very different situations: a
 * record genuinely in the piedmont/southside, and a record whose address we
 * simply could not parse. The dry run on 2026-08-16 showed the second case
 * dominating — 35 Richmond, 14 dc-nova and 9 fxbg churches carried curated
 * regions but unparseable addresses, and a naive overwrite would have dumped
 * all 58 into the catch-all. A classifier shrug must never overwrite a
 * curated answer, so 'virginia-other' is only ever written over an empty or
 * already-'virginia-other' region.
 *
 * Returns null when nothing should change.
 */
function reclassify(c) {
  const cur = c.region || '';
  const next = regionOf(c);
  if (next === cur) return null;
  if (next === 'virginia-other' && cur && cur !== 'va') return null; // shrug — keep curated
  return next;
}

module.exports = { REGIONS, regionOf, reclassify, cityOf, zipOf };
