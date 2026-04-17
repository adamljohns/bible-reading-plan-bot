# Data quality flags — 2026-04-17 enrichment wave

Four parallel enrichment agents surfaced systemic quality issues while researching Facebook, YouTube, and pastor-verification data. The agents correctly **refused to guess** and skipped these records rather than fabricate updates. Each item below needs a manual pass.

## Pattern: website / address / pastor mismatches

Records where the website, address, or pastor name refers to a different church than the one the record claims to describe.

| ID | Claimed | Actual (per agent research) | Flag |
|----|---------|------------------------------|------|
| `faith-baptist-buford-ga` | Buford GA using `faithbaptistga.org` | `faithbaptistga.org` belongs to Faith Baptist of **Jefferson GA** (Stephen Burrell) | Wrong website |
| `faith-baptist-millen-ga` | Millen GA using `faithbaptistga.org` | Same — website belongs to Faith Baptist Jefferson GA | Wrong website |
| `first-baptist-lexington-ky` | Lexington KY, pastor Clay Hallmark | Clay Hallmark pastors FBC Lexington **TN**, not KY | Wrong pastor or wrong state |
| `first-baptist-shawnee-ok` | First Baptist Shawnee OK | Merged with Heritage Church in Nov 2022, no longer exists independently | Defunct — needs merge-or-remove |
| `first-baptist-harrisonburg-va` | FBC Harrisonburg at 501 S Main | 501 S Main is **Harrisonburg Baptist Church**, not First Baptist | Wrong address or wrong church |
| `riverside-calvary-chapel-ca` | Riverside CA using `riversidecalvary.com` | `riversidecalvary.com` resolves to **Langley BC, Canada** | Wrong website (international mixup) |
| `colonial-heights-baptist-va` | Colonial Heights VA using `colonialheights.org` | Domain actually belongs to Colonial Heights Baptist in **Ridgeland MS** | Wrong website |
| `trinity-baptist-meridian-ms` | Trinity Baptist Meridian MS using `thetrinitybaptistchurch.com` | Domain actually belongs to Trinity Baptist in **Laurel MS** | Wrong website |
| `first-baptist-beaufort-sc` | FBC Beaufort SC using `fbcbeaufort.org` | Domain actually belongs to FBC Beaufort **NC** | Wrong state (SC vs NC) |

### Recommended action
Build a verification script that, per record, fetches the `website`, extracts the church name / address / pastor mentioned on the home page (or /about), and flags any record where the fetched content doesn't name-match the record's claimed name + city. An overnight crawl could surface all similar issues across the full 4,006-church directory. Rough estimate from the skip rates: 10-15% of records may have at least one identity-field mismatch.

## Pattern: pastor identity unverifiable

Candidate churches that the new-churches agent refused to add because it could not confirm an active senior pastor via two independent sources. These are **not** existing directory records — just notes on what got skipped during expansion:

- Bridger Church (Bozeman MT) — Acts 29 plant, no senior pastor listed publicly
- Radiant Church (St Albans WV) — pastor identity unclear across source listings
- The Door Church — TLS errors on all verification attempts
- CityLight NYC — listing says Acts 29 but profile reads charismatic/seeker — rubric ambiguous
- Irvine Arabic Church — appeared on an Acts 29 listing but evidence suggests independent congregation

## Pattern: thin YouTube presence in GREEN cohort

Only **5 of 50 GREEN-rated churches** without YouTube turned out to actually have a YouTube channel. The GREEN cohort heavily uses Vimeo, SermonAudio, podcast-only distribution, and embedded players instead. Implication: YouTube is the wrong metric for GREEN-church media presence. A better composite "sermon audio available" flag that checks for SermonAudio, Vimeo, or Apple Podcasts would surface more accurate coverage of GREEN media reach.

## Denominational update

**ARBCA** (Association of Reformed Baptist Churches of America) **dissolved in 2022** following fallout from their mishandling of a long-running abuse case. The direct 1689 LBCF successor network is now the **Confessional Baptist Association (CBA)** at `cba1689.com`. Records tagged `denomination_family = "ARBCA"` should be audited — those churches may have joined CBA, may have gone independent, or may have joined other Reformed Baptist associations. This isn't a directory bug, but it's a category drift that affects how our network-based filters behave.

---

*Generated automatically from agent skip-notes during the 2026-04-17 parallel enrichment wave. This file is not consumed by the site generator — it exists for human triage only.*
