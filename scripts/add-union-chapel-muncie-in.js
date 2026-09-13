#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const churchesPath = path.join(__dirname, '../docs/data/churches.json');
const data = JSON.parse(fs.readFileSync(churchesPath, 'utf8'));

const id = 'union-chapel-muncie-in';
if (data.churches.some((c) => String(c.id) === id)) {
  console.log(`SKIP: ${id} already exists`);
  process.exit(0);
}

const baseEng = {
  visited_facility: false,
  attended_services: false,
  viewed_online_services: false,
  researched_website: true,
  know_members_personally: false,
  interacted_with_leadership: false,
  attended_personally: false,
};

const baseSig = {
  warhurst_protest_2020: [],
  amr_2026: [],
  letter_of_lament_2025: [],
  revoice_2018_2026: [],
  dallas_statement_2018: [],
  nashville_statement_2017: [],
  cbe_egalitarian_2026: [],
};

const campaignNote =
  'Campaign-stewardship caution (live FAQ, one-unionchapel.com/the-one-fund, fetched 2026-09-13): ' +
  'The One Initiative / Making Room at the Well — $12.5M two-year One Fund campaign. ' +
  'Debt FAQ: "Being in debt does not, however, \'excuse\' someone from being obedient in giving as a follower of Christ." ' +
  'Unemployment/limited-finances FAQ: "We believe that God calls us to action in times of hardship just as much as He does in times of abundance" and invites members in tight seasons to "sell things, pick up odd jobs" to meet giving commitments. ' +
  'Not a theological RED — male Lead Pastor Christopher Glotzbach per unionchapel.com/staff.';

const record = {
  id,
  slug: id,
  name: 'Union Chapel',
  address: '4622 North Broadway Avenue, Muncie, IN 47303',
  pastor: 'Christopher Glotzbach',
  pastors: [
    { name: 'Christopher Glotzbach', role: 'Lead Pastor' },
    { name: 'Glenn Greiner', role: 'Associate Pastor' },
    { name: 'Jeff Hughes', role: 'Connections Pastor' },
    { name: 'Candace Ford', role: 'Executive Director' },
  ],
  pastor_credentials: 'Not listed on website',
  founded: '1970 (per church timeline)',
  type: 'Church',
  denomination: 'Non-Denominational',
  denomination_family: 'Non-Denominational',
  denomination_detail:
    'UMC-origin congregation; disaffiliated from the United Methodist Church June 2022 (per unionchapel.com/about-us timeline). Established 99 Network church planting organization August 2023.',
  website: 'https://www.unionchapel.com/',
  services: {
    sunday_morning: '8:30, 10:00, and 11:30 a.m.',
  },
  phone: '765-288-8383',
  has_mens_ministry: false,
  has_kids_ministry: true,
  overall_rating: 'yellow',
  overall_label: 'YELLOW — live-fetched; campaign-stewardship caution; full rubric pending',
  scores: {
    christology: 'yellow',
    scripture: 'yellow',
    gender: 'yellow',
    leadership: 'yellow',
    soteriology: 'yellow',
    cultural: 'yellow',
    preaching: 'yellow',
    mission: 'yellow',
    mens_discipleship: 'yellow',
    denominational: 'yellow',
  },
  score_notes: {
    gender:
      'Lead Pastor Christopher Glotzbach (male) per unionchapel.com/staff. Executive Director Candace Ford is not senior pastor.',
    denominational:
      'Disaffiliated UMC 2022; 99 Network planting org 2023 — independent accountability structure.',
  },
  assessment:
    'Union Chapel, Muncie IN — large independent congregation (UMC-origin, disaffiliated 2022). Lead Pastor Christopher Glotzbach. Public campaign: The One Initiative / Making Room at the Well ($12.5M two-year One Fund). ' +
    campaignNote,
  tags: [
    'muncie',
    'indiana',
    'non-denominational',
    'campaign-stewardship-caution',
    'religion-business-2026',
    'needs-rating-review',
  ],
  gender_detail:
    'Male Lead Pastor Christopher Glotzbach. Female Executive Director Candace Ford — not treated as senior pastor.',
  notes: [campaignNote],
  engagement: baseEng,
  signatories: baseSig,
  signatures_aggregate: 'none',
  region: 'in',
  url_research_status: 'verified',
  enrichment_sources: [
    'https://www.unionchapel.com/',
    'https://www.unionchapel.com/staff',
    'https://www.unionchapel.com/about-us',
    'https://www.one-unionchapel.com/',
    'https://www.one-unionchapel.com/the-one-fund',
    'https://www.youtube.com/watch?v=eRyNeGznv-0',
  ],
  enrichment_notes:
    '[2026-09-13] Added via Cursor strike ticket (Chaplain Chuck / Religion Business short eRyNeGznv-0). Live-fetched unionchapel.com + one-unionchapel.com. Do not confuse with Jacob\'s Well Church, Green Bay WI (separate "Making Room at the Well" drive). Generic SBC stub union-chapel-church (Tutwiler MS) left untouched.',
  state: 'IN',
  country: 'United States',
  country_code: 'US',
  needs_review: true,
};

data.churches.push(record);
data.total_churches = data.churches.length;
data.directory_updated = '2026-09-13';

fs.writeFileSync(churchesPath, JSON.stringify(data, null, 2) + '\n');
console.log(`Added ${id}; total ${data.churches.length}`);
