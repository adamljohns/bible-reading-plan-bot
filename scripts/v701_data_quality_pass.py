#!/usr/bin/env python3
"""
V7.0.1 data quality pass — three deterministic fixes:

  1. STATE FIELD BACKFILL (high impact, ~20,268 records)
     Currently only 1,384 records have a `state` field and 6,873 have a
     `region` field. 21,664 have neither. But 20,268 of those have a
     parseable state via slug suffix (`-tx`, `-va`, etc.) or address
     regex. Backfill canonical 2-letter uppercase `state` while keeping
     `region` for sub-state subdivisions (fxbg / dc-nova / richmond etc).

  2. LGBTQ-AFFIRMING DENOMINATION RUBRIC PASS (251 records)
     Per MOOP rubric, denominations that have officially affirmed LGBTQ
     ordination/marriage (PCUSA, UMC post-2024, ELCA's Reconciling-in-
     Christ, TEC, UCC, MCC, DOC, CBF, ABCUSA, Alliance of Baptists)
     default to RED minimum on the denominational dimension. 427
     records match; 251 are not already flagged red/black/dead. Set
     `scores.denominational = "red"` with rubric citation in
     `score_notes.denominational` and an enrichment_notes audit line.
     Does NOT auto-flip overall_rating — that requires the parallel-
     session rubric pass since other dimensions may stay green.

  3. DENOMINATION STRING NORMALIZATION (~1,970 records)
     Three strings collapse to "Southern Baptist Convention (SBC)":
       - "SBC" (862)
       - "Southern Baptist (SBC)" (198)
       - "Southern Baptist Convention (SBC)" (910 — already canonical)
     Plus "Non-denominational" (216) → "Non-Denominational" (777
     canonical).
"""
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path("/Users/adamjohns/bible-reading-plan-bot")
CHURCHES = ROOT / "docs/data/churches.json"
TODAY = date.today().isoformat()

US_STATES = set('AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC'.split())

SLUG_STATE_RE = re.compile(r'-([a-z]{2})$', re.IGNORECASE)
ADDR_STATE_RE = re.compile(r'\b([A-Z]{2})\s+\d{5}|,\s*([A-Z]{2})\s*$|,\s*([A-Z]{2}),', re.IGNORECASE)
# Also support "City Virginia, United States" style
LONG_STATE_NAMES = {
    'alabama': 'AL', 'alaska': 'AK', 'arizona': 'AZ', 'arkansas': 'AR',
    'california': 'CA', 'colorado': 'CO', 'connecticut': 'CT', 'delaware': 'DE',
    'florida': 'FL', 'georgia': 'GA', 'hawaii': 'HI', 'idaho': 'ID',
    'illinois': 'IL', 'indiana': 'IN', 'iowa': 'IA', 'kansas': 'KS',
    'kentucky': 'KY', 'louisiana': 'LA', 'maine': 'ME', 'maryland': 'MD',
    'massachusetts': 'MA', 'michigan': 'MI', 'minnesota': 'MN', 'mississippi': 'MS',
    'missouri': 'MO', 'montana': 'MT', 'nebraska': 'NE', 'nevada': 'NV',
    'new hampshire': 'NH', 'new jersey': 'NJ', 'new mexico': 'NM', 'new york': 'NY',
    'north carolina': 'NC', 'north dakota': 'ND', 'ohio': 'OH', 'oklahoma': 'OK',
    'oregon': 'OR', 'pennsylvania': 'PA', 'rhode island': 'RI', 'south carolina': 'SC',
    'south dakota': 'SD', 'tennessee': 'TN', 'texas': 'TX', 'utah': 'UT',
    'vermont': 'VT', 'virginia': 'VA', 'washington': 'WA', 'west virginia': 'WV',
    'wisconsin': 'WI', 'wyoming': 'WY', 'district of columbia': 'DC',
}

LGBTQ_AFFIRMING_PATTERNS = [
    ('PCUSA', 'PCUSA (Presbyterian Church (USA)) has formally permitted LGBTQ ordination since 2011 and same-sex marriage since 2015.'),
    ('Presbyterian Church (USA)', 'PCUSA has formally permitted LGBTQ ordination since 2011 and same-sex marriage since 2015.'),
    ('Presbyterian Church USA', 'PCUSA has formally permitted LGBTQ ordination since 2011 and same-sex marriage since 2015.'),
    ('UMC', 'United Methodist Church removed restrictions on LGBTQ clergy and same-sex marriage in 2024 General Conference.'),
    ('United Methodist Church', 'UMC removed restrictions on LGBTQ clergy and same-sex marriage in 2024 General Conference.'),
    ('ELCA', 'ELCA permits LGBTQ ordination (2009) and has many Reconciling in Christ congregations.'),
    ('Evangelical Lutheran Church in America', 'ELCA permits LGBTQ ordination (2009) and has many Reconciling in Christ congregations.'),
    ('TEC', 'The Episcopal Church (TEC) has permitted LGBTQ ordination since 2003 and same-sex marriage since 2015.'),
    ('Episcopal Church', 'The Episcopal Church has permitted LGBTQ ordination since 2003 and same-sex marriage since 2015.'),
    ('ECUSA', 'The Episcopal Church (ECUSA) has permitted LGBTQ ordination since 2003 and same-sex marriage since 2015.'),
    ('Disciples of Christ', 'Disciples of Christ (DOC) is Open and Affirming-friendly with no denominational restriction on LGBTQ clergy.'),
    ('UCC', 'United Church of Christ formally adopted Open and Affirming policy in 1985, oldest mainline LGBTQ-affirming.'),
    ('United Church of Christ', 'UCC formally adopted Open and Affirming policy in 1985, oldest mainline LGBTQ-affirming.'),
    ('MCC', 'Metropolitan Community Church was founded in 1968 specifically as an LGBTQ-affirming denomination.'),
    ('Metropolitan Community', 'MCC was founded in 1968 specifically as an LGBTQ-affirming denomination.'),
    ('CBF', 'Cooperative Baptist Fellowship permits congregations to ordain women and varies on LGBTQ policy by congregation; broke from SBC over progressive trajectory.'),
    ('Cooperative Baptist Fellowship', 'CBF permits congregations to ordain women and varies on LGBTQ policy by congregation; broke from SBC over progressive trajectory.'),
    ('Alliance of Baptists', 'Alliance of Baptists is explicitly LGBTQ-affirming and egalitarian; left SBC over conservative resurgence.'),
    ('ABCUSA', 'American Baptist Churches USA permits congregations to call LGBTQ clergy and varies on policy by congregation.'),
    ('ABC-USA', 'American Baptist Churches USA permits congregations to call LGBTQ clergy and varies on policy by congregation.'),
    ('American Baptist Churches', 'American Baptist Churches USA permits congregations to call LGBTQ clergy and varies on policy by congregation.'),
]


def extract_state(church):
    """Return ('SOURCE', 'XX') tuple or (None, None) if cannot determine."""
    # 1) slug suffix
    cid = church.get('id', '')
    m = SLUG_STATE_RE.search(cid)
    if m and m.group(1).upper() in US_STATES:
        return ('slug', m.group(1).upper())

    # 2) address regex (short form: ", VA 22407" or "VA 22407" or ", VA,")
    addr = church.get('address') or ''
    m = ADDR_STATE_RE.search(addr)
    if m:
        s = (m.group(1) or m.group(2) or m.group(3) or '').upper()
        if s in US_STATES:
            return ('address-short', s)

    # 3) Long state name in address ("Norfolk Virginia, United States 23503")
    addr_lower = addr.lower()
    for long_name, code in LONG_STATE_NAMES.items():
        if long_name in addr_lower:
            return ('address-long', code)

    # 4) region field — if it's already a 2-letter code matching a US state
    region = (church.get('region') or '').lower()
    if region and region.upper() in US_STATES:
        return ('region', region.upper())

    return (None, None)


def normalize_denomination(denom):
    """Return the canonical denomination string, or original if no change."""
    if not denom or not isinstance(denom, str):
        return denom
    d = denom.strip()
    # SBC variants
    if d == 'SBC' or d == 'Southern Baptist (SBC)':
        return 'Southern Baptist Convention (SBC)'
    # Non-denominational case
    if d == 'Non-denominational':
        return 'Non-Denominational'
    return d


_LGBTQ_PATTERN_RES = None
def _compile_lgbtq_patterns():
    """Compile each pattern with word-boundary regex to avoid substring
    false positives. The original substring scan was matching 'TEC' inside
    'Pentecostal/Charismatic' — devastating false positive rate."""
    global _LGBTQ_PATTERN_RES
    if _LGBTQ_PATTERN_RES is not None:
        return _LGBTQ_PATTERN_RES
    compiled = []
    for pattern, citation in LGBTQ_AFFIRMING_PATTERNS:
        # Use word boundaries around the pattern. For multi-word patterns we
        # need to escape any regex metachars inside the pattern.
        escaped = re.escape(pattern)
        # \b before and after, case-insensitive. Note: \b treats `(`, `)`,
        # `-`, and other punctuation as word boundaries already, so the
        # word-boundary trick works for tokens like "ABC-USA" too.
        pat_re = re.compile(rf'(?<![a-zA-Z]){escaped}(?![a-zA-Z])', re.IGNORECASE)
        compiled.append((pat_re, pattern, citation))
    _LGBTQ_PATTERN_RES = compiled
    return compiled


def lgbtq_affirming_match(denom, family):
    """Return (pattern, citation) if matched, else (None, None).

    Uses word-boundary regex to avoid 'TEC' matching inside 'Pentecostal'.
    Also screens out known conservative-Anglican exclusions and post-UMC
    departures (records that left the affirming denomination)."""
    combined_raw = f'{denom or ""} {family or ""}'
    combined_lower = combined_raw.lower()

    # Hard exclusions — record is in a related but NOT-LGBTQ-affirming body.
    # Order matters: if any of these strings appear, skip all LGBTQ matching.
    HARD_EXCLUSIONS = [
        'reformed episcopal church',  # REC is conservative ACNA-aligned, NOT TEC
        'rec /',                       # "REC / ACNA" combo
        '(rec)',                       # "Reformed Episcopal Church (REC)"
        'rec)',                        # same
        'acna',                        # Anglican Church in North America is conservative
        'formerly united methodist',   # post-UMC departure
        'formerly umc',                # same
        'post-umc',                    # same
        'left umc',                    # same
        'post-united methodist',       # same
        'gmc',                         # Global Methodist Church is the conservative post-UMC body
        'global methodist',            # same
        'methodist (gmc)',             # same
        'umc/gmc status not surfaced', # ambiguous — don't auto-flag
        'cbe-affirming',               # has its own scoring, don't pile on
        'lcmc',                        # Lutheran Congregations in Mission for Christ — left ELCA over LGBTQ
        'naluc',                       # North American Lutheran Church — conservative ELCA exodus
        'nalc',                        # same
        'eco ',                        # ECO Presbyterian (left PCUSA over LGBTQ)
        'eco-',                        # same
        '(eco)',                       # same
        'ecpc',                        # Evangelical Covenant Order Presbyterian — same
    ]
    for excl in HARD_EXCLUSIONS:
        if excl in combined_lower:
            return (None, None)

    for pat_re, pattern, citation in _compile_lgbtq_patterns():
        m = pat_re.search(combined_raw)
        if m:
            # Avoid false positive: "non-PCUSA" or "not PCUSA"
            start = m.start()
            prefix = combined_lower[max(0, start-5):start]
            if 'non-' in prefix or 'not ' in prefix:
                continue
            return (pattern, citation)
    return (None, None)


def main():
    data = json.loads(CHURCHES.read_text())
    churches = data.get('churches', [])

    # === Counters ===
    state_backfilled = {'slug': 0, 'address-short': 0, 'address-long': 0, 'region': 0}
    state_unrecoverable = 0
    state_already_set = 0
    lgbtq_flagged = 0
    lgbtq_already_red = 0
    denom_normalized = {'SBC variant': 0, 'Non-Denominational case': 0}

    # === Pass 1: State backfill ===
    for c in churches:
        if c.get('state'):
            state_already_set += 1
            continue
        source, state_code = extract_state(c)
        if state_code:
            c['state'] = state_code
            state_backfilled[source] += 1
        else:
            state_unrecoverable += 1

    # === Pass 2: LGBTQ-affirming denom rubric ===
    for c in churches:
        pattern, citation = lgbtq_affirming_match(
            c.get('denomination'),
            c.get('denomination_family'),
        )
        if not pattern:
            continue
        sc = c.setdefault('scores', {})
        # Skip if already red on denominational
        if sc.get('denominational') == 'red' or sc.get('denominational') == 'black':
            lgbtq_already_red += 1
            continue
        # Skip if record is already dead/red/black overall
        if c.get('overall_rating') in ('dead', 'red', 'black'):
            lgbtq_already_red += 1
            continue
        sc['denominational'] = 'red'
        sn = c.setdefault('score_notes', {})
        if isinstance(sn, dict):
            # Don't overwrite a substantive existing note — append if present
            existing = sn.get('denominational') or ''
            if existing and len(existing) > 30:
                sn['denominational'] = existing + f'\n\nMOOP rubric (V7.0.1): {citation}'
            else:
                sn['denominational'] = f'MOOP rubric: {citation}'
        c['enrichment_notes'] = (c.get('enrichment_notes') or '') + (
            f"\n--- {TODAY} V7.0.1 LGBTQ-affirming-denom rubric pass: "
            f"matched '{pattern}' → denominational dimension set to red. "
            f"{citation} Overall rating NOT auto-flipped — leaves other "
            f"dimensions intact for separate review."
        )
        lgbtq_flagged += 1

    # === Pass 3: Denomination string normalization ===
    for c in churches:
        old = c.get('denomination')
        new = normalize_denomination(old)
        if new != old:
            c['denomination'] = new
            if old in ('SBC', 'Southern Baptist (SBC)'):
                denom_normalized['SBC variant'] += 1
            elif old == 'Non-denominational':
                denom_normalized['Non-Denominational case'] += 1

    # === Bump version + write ===
    data['directory_version'] = 'V7.0.1'
    data['directory_updated'] = TODAY
    CHURCHES.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    # === Report ===
    print('V7.0.1 data quality pass:\n')

    print('1. State field backfill')
    print(f'   already set (skipped):     {state_already_set:>6}')
    for source, n in state_backfilled.items():
        print(f'   backfilled via {source:14} {n:>6}')
    print(f'   unrecoverable (logged):    {state_unrecoverable:>6}')
    print(f'   TOTAL backfilled:          {sum(state_backfilled.values()):>6}')
    print()

    print('2. LGBTQ-affirming denom rubric')
    print(f'   newly flagged (denominational=red): {lgbtq_flagged:>6}')
    print(f'   already red/black/dead (skipped):   {lgbtq_already_red:>6}')
    print()

    print('3. Denomination string normalization')
    for k, v in denom_normalized.items():
        print(f'   {k:30} {v:>6}')
    print(f'   TOTAL normalized:               {sum(denom_normalized.values()):>6}')
    print()
    print(f'Version bumped to V7.0.1')


if __name__ == '__main__':
    main()
