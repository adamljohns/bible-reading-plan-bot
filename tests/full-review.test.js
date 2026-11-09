#!/usr/bin/env node
// Full-review gates (2026-11-08). Runs the patch builder and the applier against
// a tiny synthetic churches.json — never the real one.
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const cp = require('child_process');

const ROOT = path.join(__dirname, '..');
const lanes = require(path.join(ROOT, 'scripts/lib/grind-lanes.js'));
const { denomPrior } = require(path.join(ROOT, 'scripts/lib/denomination-priors.js'));

// priors: look-alikes must not read as affirming mainline
const dp = d => (denomPrior({ denomination: d }) || {}).key || null;
assert.strictEqual(dp('The Episcopal Church (Diocese of Virginia)'), 'tec');
assert.strictEqual(dp('Reformed Episcopal Church'), 'acna');
assert.strictEqual(dp('African Methodist Episcopal'), 'ame');
assert.strictEqual(dp('Global Methodist Church'), 'gmc');
assert.strictEqual(dp('United Methodist Church (Virginia Conference)'), 'umc');
assert.strictEqual(dp('Presbyterian Church in America'), 'pca');
assert.strictEqual(dp('Presbyterian Church (USA)'), 'pcusa');
assert.strictEqual(dp('Christian Churches and Churches of Christ'), 'restoration');
assert.strictEqual(dp('Southern Baptist Convention'), null);

// eligibility
const base = { id: 'x', name: 'X Church', state: 'VA', website: 'https://x.example' };
assert.ok(lanes.fullReviewEligible(base));
assert.ok(!lanes.fullReviewEligible({ ...base, website: '', facebook: '' }));
assert.ok(lanes.fullReviewEligible({ ...base, website: '', facebook: 'https://www.facebook.com/x' }));
assert.ok(!lanes.fullReviewEligible({ ...base, full_review_at: new Date().toISOString().slice(0, 10) }));
assert.ok(!lanes.fullReviewEligible({ ...base, full_review_hold: '2026-11-08' }));

// builder gates on synthetic data
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'fr-test-'));
const churches = { churches: [
  { id: 'aff', name: 'St. A', service_times: 'SUNDAY WORSHIP (Traditional) 10:30 AM', address: '1 Main St, Townville, VA 22401', state: 'VA', denomination: 'The Episcopal Church', pastor: '', overall_rating: 'yellow', scores: {} },
  { id: 'fem', name: 'B Church', address: '2 Oak St, Townville, VA 22401', state: 'VA', denomination: 'Independent', pastor: 'John Old', overall_rating: 'green', scores: { gender: 'green' } },
  { id: 'nameonly', name: 'D Church', address: '4 Ash St, Townville, VA 22401', state: 'VA', denomination: 'Independent', pastor: '', overall_rating: 'yellow', scores: {} },
  { id: 'wrong', name: 'C Church', address: '3 Elm St, Farcity, IL 60301', state: 'IL', denomination: 'EFCA', pastor: 'Pat Other', website: 'https://c.example', overall_rating: 'yellow', scores: {} },
] };
const CJ = path.join(tmp, 'churches.json');
fs.writeFileSync(CJ, JSON.stringify(churches, null, 2)); // canonical shape for makeWriter
const page = (url, text) => ({ url, kind: 'inner', chars: text.length, text });
const obs = { model: 'test', observations: [
  { id: 'aff', name: 'St. A', status: 'reviewed', source_kind: 'website', final_url: 'https://a.example/',
    pages: [page('https://a.example/about', 'St. A Episcopal Church, 1 Main St, Townville. The Rev. Sam Jones is our Rector. We celebrate Pride Sunday every June. Our service meets on Sundays at 10:30 AM.'),
      page('https://a.example/about/clergy', 'Clergy. The Rev. Jane Roe is our Associate Rector. She leads Morning Prayer.'),
      page('https://a.example/ministries', 'Young Adult Ministry with Bethel Episcopal Church meets monthly, led by Fr. Sam or Fr. James Rickenbaker.')],
    identity: { status: 'confirmed', matched: ['city:Townville'], stored: { city: 'Townville', state: 'VA' } },
    signals: { affiliation: [{ quote: 'St. A Episcopal Church, 1 Main St, Townville.', url: 'https://a.example/about' }] },
    llm: { lead_pastor: { name: 'Sam Jones', role: 'Rector', pronoun: 'he', quote: 'The Rev. Sam Jones is our Rector.', url: 'https://a.example/about' },
      lgbt_affirming: { quote: 'We celebrate Pride Sunday every June.', url: 'https://a.example/about' },
      service_times: { quote: 'Our service meets on Sundays at 10:30 AM.', url: 'https://a.example/about' },
      roster: [{ name: 'Sam Jones', role: 'Rector' }, { name: 'Jane Roe', role: 'The Rev.' }, { name: 'James Rickenbaker', role: 'Fr.' }],
      // a rubric lean with no URL must never become a change
      rubric: { mission: { lean: 'green', quote: 'unsourced', url: null },
        preaching: { lean: 'yellow', quote: 'The Rev. Sam Jones is our Rector.', url: 'https://a.example/about' } } } },
  { id: 'nameonly', name: 'D Church', status: 'reviewed', source_kind: 'website', final_url: 'https://d.example/',
    pages: [page('https://d.example/staff', 'Townville. Pastor Mary Brown, Senior Pastor.')],
    identity: { status: 'confirmed', matched: ['city:Townville'], stored: { city: 'Townville', state: 'VA' } },
    llm: { lead_pastor: { name: 'Mary Brown', role: 'Senior Pastor', pronoun: 'unknown', quote: 'Pastor Mary Brown, Senior Pastor.', url: 'https://d.example/staff' } } },
  { id: 'fem', name: 'B Church', status: 'reviewed', source_kind: 'website', final_url: 'https://b.example/',
    pages: [page('https://b.example/staff', 'Townville. Rev. Mary Smith, Senior Pastor. She has served since 2020.')],
    identity: { status: 'confirmed', matched: ['city:Townville'], stored: { city: 'Townville', state: 'VA' } },
    llm: { lead_pastor: { name: 'Mary Smith', role: 'Senior Pastor', pronoun: 'she', quote: 'Rev. Mary Smith, Senior Pastor.', url: 'https://b.example/staff' } } },
  { id: 'wrong', name: 'C Church', status: 'identity_mismatch', source_kind: 'website', final_url: 'https://c.example/',
    pages: [page('https://c.example/', 'Pat Other, Senior Pastor. Located in Lakeside, Minnesota.')],
    identity: { status: 'contradicted', matched: [], stored: { city: 'Farcity', state: 'IL' }, conflicting_locations: [{ quote: 'Located in Lakeside, Minnesota.', url: 'https://c.example/' }] },
    llm: { lead_pastor: { name: 'Pat Other', role: 'Senior Pastor', pronoun: 'unknown', quote: 'Pat Other, Senior Pastor.', url: 'https://c.example/' } },
    recovery: { query: 'q', candidates: [], site: null } },
] };
const OBS = path.join(tmp, 'obs.json');
fs.writeFileSync(OBS, JSON.stringify(obs));
const before = fs.readFileSync(CJ);
const env = { ...process.env, FULL_REVIEW_CHURCHES_PATH: CJ };
cp.execFileSync('node', [path.join(ROOT, 'scripts/full-review-build-patch.js'), '--input', OBS, '--round', 't1', '--out', path.join(tmp, 'out'), '--stats', path.join(tmp, 'stats.json'), '--dry-run'], { env, stdio: 'pipe' });
assert.ok(before.equals(fs.readFileSync(CJ)), 'builder must not touch churches.json');
const patch = JSON.parse(fs.readFileSync(path.join(tmp, 'out/rounds/t1/review-patch.json'), 'utf8'));
const get = id => patch.churches.find(c => c.id === id);
const ch = (id, f) => get(id).changes.find(x => x.field === f);

// every change has quote + url
for (const c of patch.churches) for (const x of c.changes) assert.ok(x.evidence.quote && x.evidence.url, `${x.change_id} lacks evidence`);
// affirming parish: rules support RED (TEC on the published list), held; the
// model's BLACK becomes a separate needs-ruling item; rule text is cited
assert.strictEqual(ch('aff', 'overall_rating').new, 'red');
assert.strictEqual(ch('aff', 'overall_rating').gate, 'hold');
assert.ok(/RED minimum/.test(ch('aff', 'overall_rating').rule.text));
assert.ok(get('aff').rulings.some(r => r.title === 'needs-ruling: model suggests BLACK' && /Pride Sunday/.test(r.evidence.quote)));
assert.ok(!get('aff').changes.some(x => x.new === 'black'), 'no BLACK without a published rule');
assert.ok(!ch('aff', 'scores.preaching'), 'off-topic quote must not score preaching');
assert.ok(!ch('aff', 'scores.scripture'), 'denomination rule does not score scripture');
// same service-time SET in different words: no change
assert.ok(!ch('aff', 'service_times'), 'same {Sun 10:30 AM} set must not propose a change');
// roster: real role (not an honorific), joint-ministry name excluded, lead cited by full name
const team = ch('aff', 'pastors').new;
assert.deepStrictEqual(team.map(p => p.name), ['Sam Jones', 'Jane Roe']);
assert.strictEqual(team[1].role, 'Associate Rector');
assert.ok(/Sam Jones/.test(ch('aff', 'pastors').evidence.quote));
assert.ok(get('aff').roster.excluded.some(x => x.name === 'James Rickenbaker' && /Bethel/.test(x.why)));
assert.strictEqual(ch('aff', 'pastor').new, 'Sam Jones');
assert.strictEqual(ch('aff', 'pastor').gate, 'auto');
assert.ok(!ch('aff', 'scores.mission'), 'unsourced lean must not become a change');
// female lead off GREEN: pastor + RED both held
assert.strictEqual(ch('fem', 'pastor').gate, 'hold');
assert.strictEqual(ch('fem', 'overall_rating').new, 'red');
assert.strictEqual(ch('fem', 'overall_rating').gate, 'hold');
assert.ok(/She has served/.test(ch('fem', 'overall_rating').evidence.quote), 'gender evidence must be the pronoun bio');
// first-name list only: no rating, an unconfirmed HOLD item, pastor held
assert.ok(!ch('nameonly', 'overall_rating'));
assert.ok(get('nameonly').rulings.some(r => r.type === 'unconfirmed'));
assert.strictEqual(ch('nameonly', 'pastor').gate, 'hold');
// wrong-church data: flagged, everything held, nothing scored from that site
assert.ok(get('wrong').flags.some(f => f.type === 'data_belongs_to_other_church'));
assert.ok(get('wrong').changes.every(x => x.gate === 'hold'));
assert.ok(!get('wrong').changes.some(x => x.field.startsWith('scores.') || x.field === 'overall_rating'));

// applier refuses a dry-run patch without the explicit flag, and preview writes nothing
const P = path.join(tmp, 'out/rounds/t1/review-patch.json');
let refused = false;
try { cp.execFileSync('node', [path.join(ROOT, 'scripts/apply-full-review-patch.js'), '--patch', P, '--holds', path.join(tmp, 'out/hold-queue.json')], { env, stdio: 'pipe' }); } catch (e) { refused = e.status === 3; }
assert.ok(refused, 'dry-run patch must be refused');
cp.execFileSync('node', [path.join(ROOT, 'scripts/apply-full-review-patch.js'), '--patch', P, '--holds', path.join(tmp, 'out/hold-queue.json'), '--accept-dry-run-patch'], { env, stdio: 'pipe' });
assert.ok(before.equals(fs.readFileSync(CJ)), 'preview must not touch churches.json');
console.log('full-review tests OK');
