# Networks + Speakers Expansion — 5-Phase Plan

> **Schedule:**
> - Phase 1 → Mon evening 2026-05-18
> - Phases 2 & 3 → Tue 2026-05-19
> - Phases 4 & 5 → Wed 2026-05-20
>
> **Tracker:** Run `node scripts/phase-status.js` to refresh the auto-counted percentages below.
> **Status as of:** 2026-05-18 21:40 UTC

---

## Overall completion: <!-- OVERALL_PCT:START -->0%<!-- OVERALL_PCT:END --> (<!-- OVERALL_COUNT:START -->0 of 38<!-- OVERALL_COUNT:END --> checkboxes)

```
[                                                  ]   0% Phase 1 — Founders cross-reference
[                                                  ]   0% Phase 2 — Other networks
[                                                  ]   0% Phase 3 — Conference speakers
[                                                  ]   0% Phase 4 — Networks page
[                                                  ]   0% Phase 5 — Cleanup + polish
```

*(Bars auto-update when you run `node scripts/phase-status.js`.)*

---

## Phase 1 — Founders Ministries cross-reference

**Target:** Mon evening 2026-05-18. ETA 2-3 hrs.
**Completion:** <!-- P1_PCT:START -->0%<!-- P1_PCT:END --> (<!-- P1_COUNT:START -->0/8<!-- P1_COUNT:END -->)

- [ ] Add `cross_listed_in` field to schema (array of network slugs, top-level on each church record)
- [ ] Document the field in the schema reference (a quick comment in any schema doc; or just on the directory-overview page)
- [ ] Scrape founders.org/find-a-church (or pivot to per-state pages if the main directory is JS-rendered)
- [ ] Build a {name, city, state, website, founders-id} index of all Founders churches
- [ ] Match index against existing MOOP records (by website domain + name+city fuzzy)
- [ ] Update matched records with `cross_listed_in: ["founders"]`
- [ ] Add Founders churches NOT in MOOP as new records (target: 80-120 new)
- [ ] Verify + tag Alex Kachman's PA church specifically (he's an elder; author of *Ordered Love*; Founders-affiliated)

**Single-commit target at end of Phase 1.**

---

## Phase 2 — Other network cross-references

**Target:** Tue 2026-05-19 (alongside Phase 3). ETA 2-3 hrs.
**Completion:** <!-- P2_PCT:START -->0%<!-- P2_PCT:END --> (<!-- P2_COUNT:START -->0/8<!-- P2_COUNT:END -->)

Each network → one parallel agent. Each adds `cross_listed_in` tag + adds missing churches.

- [ ] **9Marks** — `9marks.org` church finder (Mark Dever's network; complementarian + congregationalist polity)
- [ ] **TGC Church Network** — `thegospelcoalition.org/about/cn` (broader Reformed-evangelical)
- [ ] **G3 Ministries** — `g3min.org/network` (Josh Buice; conservative confessional)
- [ ] **Acts 29** — `acts29.com/find-a-church` (already have many; mark existing + add missing)
- [ ] **Sovereign Grace Churches** — `sovereigngrace.com/churches` (already have many; mark + add missing)
- [ ] **Reformation Charlotte / Reformation 21 network** — if a formal church-list exists
- [ ] **The Trinity Foundation** Reformed Baptist Network — if exists
- [ ] **Pillar Church Network** (Adam visited Pillar Stafford; this is the Pillar church-planting movement)

---

## Phase 3 — Conference speakers research

**Target:** Tue 2026-05-19. ETA 2-3 hrs.
**Completion:** <!-- P3_PCT:START -->0%<!-- P3_PCT:END --> (<!-- P3_COUNT:START -->0/8<!-- P3_COUNT:END -->)

For each conference: pull speaker list → map each speaker to their home church → if church is in MOOP, add `notable_attendees` entry with `branch: "religious"` and `association: "home_church"`; include "conference speaker at <Conference>" in `title`.

- [ ] **250th Anniversary event** (National Mall, kicked off 2026-05-16) — research speakers list (Adam caught the tail end)
- [ ] **G3 Conference** (annual; Josh Buice)
- [ ] **Together for the Gospel (T4G)** — Dever, Mohler, Mahaney, Duncan; check if still active or paused
- [ ] **The Gospel Coalition National** (TGC25/27 etc.)
- [ ] **Sing! Conference** (Getty Music, Nashville)
- [ ] **Cross Conference** (missions; Piper)
- [ ] **Shepherds' Conference** (MacArthur / Master's Seminary)
- [ ] **CBMW National Conference** (complementarianism)

---

## Phase 4 — Build /docs/directory-networks.html

**Target:** Wed 2026-05-20. ETA 1.5 hrs.
**Completion:** <!-- P4_PCT:START -->0%<!-- P4_PCT:END --> (<!-- P4_COUNT:START -->0/8<!-- P4_COUNT:END -->)

Similar to `directory-politicians.html` (already shipped — 103 entries, 85 churches, 6 filter buckets). Networks page would:

- [ ] Build generator script `scripts/build-directory-networks.js` (reads churches.json, extracts cross_listed_in)
- [ ] Stats hero: # networks tracked, # churches with ≥1 network membership, # cross-listed
- [ ] Filter UI: chips for each network (Founders / 9Marks / TGC-CN / G3 / Acts 29 / SGC / Pillar)
- [ ] Sort options: by network, by state, by rating
- [ ] Link each church to its detail page
- [ ] Editorial: per-network methodology notes (what each affiliation means doctrinally)
- [ ] Add nav entry to existing pages (Home / Directory / Overview / Politicians / **Networks** / Roadmap / About)
- [ ] Final commit + push as "v6.0 networks + speakers"

---

## Phase 5 — Cleanup + editorial polish

**Target:** Wed 2026-05-20. ETA 1 hr.
**Completion:** <!-- P5_PCT:START -->0%<!-- P5_PCT:END --> (<!-- P5_COUNT:START -->0/6<!-- P5_COUNT:END -->)

- [ ] Verify all `cross_listed_in` entries point at currently-active network membership (some churches have left networks over time)
- [ ] Add per-network methodology notes to the networks page editorial
- [ ] Update directory-overview.html to highlight the new feature
- [ ] Cleanup-6: resolve the major dupe sets surfaced during SPEAKERS-1 (Redeemer NYC x9, Highview Louisville x4, Christ Church Moscow x3, Christ Covenant Matthews x2)
- [ ] Triage the ~253 needs_review flags accumulated through R31
- [ ] Final v6.0 commit + sitemap update

---

## Pre-flight reality checks (read before Phase 1)

1. **JS-rendered directories will be slow.** Many denomination/network "Find a Church" pages are React/Vue SPAs that return empty HTML. When an agent hits this, pivot to per-state subpages (often static) or per-church live-fetches. We saw this in R18 with arbca.com and anglicanchurch.net.
2. **Founders has overlap with existing MOOP records.** Don't dedup just on slug — check website domain too. Many existing Reformed Baptist records are likely Founders-affiliated already.
3. **Alex Kachman's church may need a name lookup.** Adam remembers PA + *Ordered Love* + Founders connection. Quick agent task before Phase 1 starts.
4. **Speakers data overlaps with Founders/9Marks lists.** Mark Dever (Capitol Hill Baptist) is both a speaker AND a 9Marks founder. Notable_attendees entry and cross_listed_in tag are complementary.

---

## How to run the tracker

```bash
# Refresh percentages after you check off items:
node scripts/phase-status.js

# Or pass --check <phase> <item-number> to check off an item programmatically:
node scripts/phase-status.js --check 1 3   # marks Phase 1 item #3 as done
```
