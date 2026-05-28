#!/usr/bin/env python3
"""
Classify the 1,063 "unstated" records by country.

After V7.0.1 state-backfill, the 1,063 records with no `state` field were
suspected of being mostly international. This script:

  1. Extracts country from each record's name + address using a regex
     scan against known country names + 2-letter Canadian provinces.
  2. Adds `country` field (full name, e.g. "Canada", "United Kingdom").
  3. Adds `country_code` field (ISO 3166-1 alpha-2, e.g. "CA", "GB").
  4. For records still genuinely unidentifiable, leaves them alone in
     _unstated.json.

The state-shard build script will then route international records to
a new _international.json shard, leaving _unstated.json only for the
truly stranded.
"""
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path("/Users/adamjohns/bible-reading-plan-bot")
CHURCHES = ROOT / "docs/data/churches.json"
TODAY = date.today().isoformat()

# Country patterns: regex pattern → (country name, ISO code)
COUNTRY_PATTERNS = [
    # Puerto Rico — US commonwealth, route to US country with PR territory tag
    (r', PR\b|, Puerto Rico\b|\bPuerto Rico\b|-pr$|-pr-', 'Puerto Rico (US)', 'US'),
    (r'\bCanada\b|, (?:ON|QC|BC|AB|MB|SK|NS|NB|NL|PE|YT|NT|NU)\b|-(?:on|qc|bc|ab|mb|sk|ns|nb|nl|pe|yt|nt|nu)$|, (?:Ontario|Quebec|British Columbia|Alberta|Manitoba|Saskatchewan|Nova Scotia|New Brunswick|Newfoundland|Prince Edward Island|Yukon|Northwest Territories|Nunavut)\b|-(?:toronto|vancouver|calgary|ottawa|montreal|edmonton|winnipeg|halifax|hamilton-on|kingston-on|saskatoon)$', 'Canada', 'CA'),
    (r'\bUnited Kingdom\b|\bUK\b|\bEngland\b|\bScotland\b|\bWales\b|\bNorthern Ireland\b|\bGreat Britain\b|-(?:london|edinburgh|liverpool|birmingham|manchester|glasgow|belfast|inverness|bristol-uk|cardiff|sheffield|leeds|leicester|nottingham|coventry|bradford|stoke|wolverhampton|plymouth|derby|swansea|aberdeen|portsmouth|york|oxford|cambridge-uk)$', 'United Kingdom', 'GB'),
    (r'\bAustralia\b|, (?:NSW|VIC|QLD|WA|SA|TAS|ACT|NT)\b|-(?:nsw|vic|qld|tas|act|sydney|melbourne|brisbane|perth|adelaide|hobart|darwin|wellington-au|gold-coast|newcastle-au|canberra)$', 'Australia', 'AU'),
    (r'-(?:auckland|wellington-nz|christchurch|hamilton-nz)$', 'New Zealand', 'NZ'),
    (r'-(?:paris|lyon|marseille|toulouse|nice|nantes|strasbourg|montpellier|bordeaux)$', 'France', 'FR'),
    (r'-(?:moscow|st-petersburg-ru|saint-petersburg|novosibirsk|yekaterinburg)$', 'Russia', 'RU'),
    (r'\bMadagascar\b', 'Madagascar', 'MG'),
    (r'\bSerbia\b|\bVojvodina\b', 'Serbia', 'RS'),
    (r'\bCroatia\b', 'Croatia', 'HR'),
    (r'\bMacedonia\b|\bNorth Macedonia\b', 'North Macedonia', 'MK'),
    (r'\bMoldova\b', 'Moldova', 'MD'),
    (r'\bBelarus\b', 'Belarus', 'BY'),
    (r'\bBulgaria\b', 'Bulgaria', 'BG'),
    (r'\bSlovenia\b', 'Slovenia', 'SI'),
    (r'\bSlovakia\b', 'Slovakia', 'SK'),
    (r'\bAlbania\b', 'Albania', 'AL'),
    (r'\bMorocco\b', 'Morocco', 'MA'),
    (r'\bAlgeria\b', 'Algeria', 'DZ'),
    (r'\bTunisia\b', 'Tunisia', 'TN'),
    (r'\bSenegal\b', 'Senegal', 'SN'),
    (r'\bCameroon\b', 'Cameroon', 'CM'),
    (r'\bIvory Coast\b|\bCote d.{1,2}Ivoire\b', "Côte d'Ivoire", 'CI'),
    (r'\bMozambique\b', 'Mozambique', 'MZ'),
    (r'\bZimbabwe\b', 'Zimbabwe', 'ZW'),
    (r'\bMalawi\b', 'Malawi', 'MW'),
    (r'\bZambia\b', 'Zambia', 'ZM'),
    (r'\bRwanda\b', 'Rwanda', 'RW'),
    (r'\bBurundi\b', 'Burundi', 'BI'),
    (r'\bSudan\b', 'Sudan', 'SD'),
    (r'\bAngola\b', 'Angola', 'AO'),
    (r'\bSomalia\b', 'Somalia', 'SO'),
    (r'\bLiberia\b', 'Liberia', 'LR'),
    (r'\bBolivia\b', 'Bolivia', 'BO'),
    (r'\bUruguay\b', 'Uruguay', 'UY'),
    (r'\bParaguay\b', 'Paraguay', 'PY'),
    (r'\bEcuador\b', 'Ecuador', 'EC'),
    (r'\bNicaragua\b', 'Nicaragua', 'NI'),
    (r'\bBelize\b', 'Belize', 'BZ'),
    (r'\bTrinidad\b', 'Trinidad and Tobago', 'TT'),
    (r'\bBarbados\b', 'Barbados', 'BB'),
    (r'\bBahamas\b', 'Bahamas', 'BS'),
    (r'\bPakistan\b', 'Pakistan', 'PK'),
    (r'\bBangladesh\b', 'Bangladesh', 'BD'),
    (r'\bSri Lanka\b', 'Sri Lanka', 'LK'),
    (r'\bNepal\b', 'Nepal', 'NP'),
    (r'\bMyanmar\b|\bBurma\b', 'Myanmar', 'MM'),
    (r'\bCambodia\b', 'Cambodia', 'KH'),
    (r'\bLaos\b', 'Laos', 'LA'),
    (r'\bMongolia\b', 'Mongolia', 'MN'),
    (r'\bKazakhstan\b', 'Kazakhstan', 'KZ'),
    (r'\bUzbekistan\b', 'Uzbekistan', 'UZ'),
    (r'\bIran\b', 'Iran', 'IR'),
    (r'\bIraq\b', 'Iraq', 'IQ'),
    (r'\bJordan\b', 'Jordan', 'JO'),
    (r'\bLebanon\b', 'Lebanon', 'LB'),
    (r'\bSyria\b', 'Syria', 'SY'),
    (r'\bKuwait\b', 'Kuwait', 'KW'),
    (r'\bQatar\b', 'Qatar', 'QA'),
    (r'\bBahrain\b', 'Bahrain', 'BH'),
    (r'\bOman\b', 'Oman', 'OM'),
    (r'\bYemen\b', 'Yemen', 'YE'),
    (r'\bPapua New Guinea\b|\bPNG\b', 'Papua New Guinea', 'PG'),
    (r'\bFiji\b', 'Fiji', 'FJ'),
    (r'\bGuam\b|, GU\b|-gu$', 'Guam (US)', 'US'),  # US territory → US country
    (r'\bAmerican Samoa\b|, AS\b', 'American Samoa (US)', 'US'),
    (r'\bNorthern Mariana\b|, MP\b', 'Northern Mariana Islands (US)', 'US'),
    (r'\b(?:St\.?\s*Thomas|St\.?\s*Croix|St\.?\s*John|US Virgin Islands|U\.S\. Virgin Islands)\b|, VI\b|-vi$', 'US Virgin Islands', 'US'),
    (r'\bNew Zealand\b|\bNZ\b', 'New Zealand', 'NZ'),
    (r'\bIreland\b(?!\s*Northern)|\bRepublic of Ireland\b', 'Ireland', 'IE'),
    (r'\bSouth Africa\b', 'South Africa', 'ZA'),
    (r'\bKenya\b', 'Kenya', 'KE'),
    (r'\bNigeria\b', 'Nigeria', 'NG'),
    (r'\bGhana\b', 'Ghana', 'GH'),
    (r'\bUganda\b', 'Uganda', 'UG'),
    (r'\bTanzania\b', 'Tanzania', 'TZ'),
    (r'\bEthiopia\b', 'Ethiopia', 'ET'),
    (r'\bSingapore\b', 'Singapore', 'SG'),
    (r'\bHong Kong\b', 'Hong Kong', 'HK'),
    (r'\bJapan\b', 'Japan', 'JP'),
    (r'\bKorea\b|\bSouth Korea\b', 'South Korea', 'KR'),
    (r'\bPhilippines\b', 'Philippines', 'PH'),
    (r'\bIndia\b', 'India', 'IN'),
    (r'\bIndonesia\b', 'Indonesia', 'ID'),
    (r'\bMalaysia\b', 'Malaysia', 'MY'),
    (r'\bThailand\b', 'Thailand', 'TH'),
    (r'\bVietnam\b', 'Vietnam', 'VN'),
    (r'\bChina\b', 'China', 'CN'),
    (r'\bTaiwan\b', 'Taiwan', 'TW'),
    (r'\bMexico\b', 'Mexico', 'MX'),
    (r'\bBrazil\b', 'Brazil', 'BR'),
    (r'\bArgentina\b', 'Argentina', 'AR'),
    (r'\bColombia\b', 'Colombia', 'CO'),
    (r'\bChile\b', 'Chile', 'CL'),
    (r'\bPeru\b', 'Peru', 'PE'),
    (r'\bVenezuela\b', 'Venezuela', 'VE'),
    (r'\bGuatemala\b', 'Guatemala', 'GT'),
    (r'\bHonduras\b', 'Honduras', 'HN'),
    (r'\bEl Salvador\b', 'El Salvador', 'SV'),
    (r'\bCosta Rica\b', 'Costa Rica', 'CR'),
    (r'\bPanama\b', 'Panama', 'PA'),
    (r'\bDominican Republic\b', 'Dominican Republic', 'DO'),
    (r'\bPuerto Rico\b', 'Puerto Rico', 'PR'),
    (r'\bHaiti\b', 'Haiti', 'HT'),
    (r'\bJamaica\b', 'Jamaica', 'JM'),
    (r'\bCuba\b', 'Cuba', 'CU'),
    (r'\bGermany\b', 'Germany', 'DE'),
    (r'\bFrance\b', 'France', 'FR'),
    (r'\bSpain\b', 'Spain', 'ES'),
    (r'\bItaly\b', 'Italy', 'IT'),
    (r'\bNetherlands\b|\bHolland\b', 'Netherlands', 'NL'),
    (r'\bBelgium\b', 'Belgium', 'BE'),
    (r'\bSwitzerland\b', 'Switzerland', 'CH'),
    (r'\bAustria\b', 'Austria', 'AT'),
    (r'\bSweden\b', 'Sweden', 'SE'),
    (r'\bNorway\b', 'Norway', 'NO'),
    (r'\bDenmark\b', 'Denmark', 'DK'),
    (r'\bFinland\b', 'Finland', 'FI'),
    (r'\bIceland\b', 'Iceland', 'IS'),
    (r'\bPoland\b', 'Poland', 'PL'),
    (r'\bRussia\b', 'Russia', 'RU'),
    (r'\bUkraine\b', 'Ukraine', 'UA'),
    (r'\bRomania\b', 'Romania', 'RO'),
    (r'\bHungary\b', 'Hungary', 'HU'),
    (r'\bCzech Republic\b|\bCzechia\b', 'Czech Republic', 'CZ'),
    (r'\bGreece\b', 'Greece', 'GR'),
    (r'\bIsrael\b', 'Israel', 'IL'),
    (r'\bUAE\b|\bUnited Arab Emirates\b|\bDubai\b|\bAbu Dhabi\b', 'United Arab Emirates', 'AE'),
    (r'\bSaudi Arabia\b', 'Saudi Arabia', 'SA'),
    (r'\bTurkey\b', 'Turkey', 'TR'),
    (r'\bEgypt\b', 'Egypt', 'EG'),
]
COMPILED = [(re.compile(p, re.IGNORECASE), name, code) for p, name, code in COUNTRY_PATTERNS]


def detect_country(record):
    """Return (country_name, country_code) or (None, None)."""
    haystack = ' '.join([
        record.get('id', ''),
        record.get('name', ''),
        record.get('address', ''),
        record.get('denomination_detail', ''),
    ])
    for pat, name, code in COMPILED:
        if pat.search(haystack):
            return (name, code)
    return (None, None)


def main():
    data = json.loads(CHURCHES.read_text())
    churches = data.get('churches', [])

    classified = 0
    already_us = 0
    truly_unstated = 0
    country_counts = {}

    for c in churches:
        # Skip records that already have a US state (don't overwrite)
        state = c.get('state')
        if state and isinstance(state, str) and len(state) == 2 and state.upper() == state:
            # Mark as US
            if not c.get('country'):
                c['country'] = 'United States'
                c['country_code'] = 'US'
            already_us += 1
            continue

        # Already has a country tag — preserve
        if c.get('country_code') and c.get('country_code') != 'US':
            country_counts[c.get('country')] = country_counts.get(c.get('country'), 0) + 1
            continue

        # No state — try to detect country
        country_name, country_code = detect_country(c)
        if country_name:
            c['country'] = country_name
            c['country_code'] = country_code
            country_counts[country_name] = country_counts.get(country_name, 0) + 1
            c['enrichment_notes'] = (c.get('enrichment_notes') or '') + (
                f"\n--- {TODAY} V7.0.3: country detected as {country_name} ({country_code}) "
                "from name + address. Routed to international shard rather than _unstated."
            )
            classified += 1
        else:
            # Truly unknown
            truly_unstated += 1

    # Bump version
    data['directory_version'] = 'V7.0.3'
    data['directory_updated'] = TODAY
    CHURCHES.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    print(f"V7.0.3 country classification:\n")
    print(f"  US records tagged country='United States': {already_us}")
    print(f"  Newly classified as international:         {classified}")
    print(f"  Truly unstated (no state, no country):     {truly_unstated}")
    print()
    print("Top countries detected:")
    for country, n in sorted(country_counts.items(), key=lambda x: -x[1])[:15]:
        print(f"  {country:30} {n}")


if __name__ == '__main__':
    main()
