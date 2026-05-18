# Research Leads

This directory holds candidate churches surfaced by network-directory scrapes that did NOT match an existing MOOP record. They are **leads for human curation**, not auto-added to the directory.

The MOOP Church Directory is the source of truth. External network directories influence what we research, but every entry in the public directory goes through MOOP's own due diligence — schema, scoring, signatory checks, live-fetch citation, etc.

## phase2-network-leads.json

7,796 candidates from Phase 2 network scrapes (2026-05-18 / 2026-05-19):

| Source network | Count | Notes |
|---|---:|---|
| 9marks | 5,693 | Self-submitted listings on 9marks.org church-search; 0.1% pastor coverage. Largest pool. |
| tgc-cn | 970 | TGC's open Church Directory (sponsored by Midwestern Seminary); no formal vetting; 0% pastor coverage. |
| pillar-network | 538 | Pillar Network (thepillarnetwork.com); 100% pastor coverage; Salesforce-Lightning widget. |
| acts29 | 486 | Acts 29 vetted member roster; 98.7% pastor coverage. |
| sgc | 62 | Sovereign Grace Churches; 87% website coverage. |
| trinity-foundation | 47 | Trinity Foundation Church Registry (vetted clearinghouse). |
| **Total** | **7,796** | |

## Schema (per entry)

```json
{
  "source_network": "acts29",
  "name": "Example Church",
  "city": "Austin",
  "state": "TX",          // 2-letter US; null for non-US
  "country": "USA",        // or country name for non-US
  "website": "https://example.org",
  "pastor": "John Doe",   // null if network doesn't surface it
  "address": "...",
  "network_url": "https://acts29.com/church/example/",
  "proposed_slug": "example-church-austin-tx"
}
```

## How to use

Pick a network bucket → research each candidate independently:
- Confirm doctrinal position via live-fetch of the church's website
- Verify pastor + service times
- Score on the 10 dimensions (christology, scripture, gender, leadership, soteriology, cultural, preaching, mission, mens_discipleship, denominational)
- Check for signatories on the 7 canonical signatory ledgers
- Add full record to `docs/data/churches.json` with `cross_listed_in: ["<source_network>"]`

This is intentionally slow work. The goal is curated quality, not coverage at any cost.
