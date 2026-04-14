# Weekly Church Directory Enrichment — Remote Trigger Config

**Status:** Ready to deploy. Auth failed on first attempt — retry from new machine or via claude.ai/code/scheduled web UI.

## Setup URL

https://claude.ai/code/scheduled

## Trigger Configuration

**Name:** Weekly Church Directory Enrichment
**Cron:** `0 13 * * 6` (Saturday 9am America/New_York = 1pm UTC)
**Enabled:** true
**Model:** claude-sonnet-4-6
**Repo:** https://github.com/adamljohns/bible-reading-plan-bot
**Environment:** Default (env_01P8BjzNpRPoZt4MqENghkD4)
**Allowed tools:** Bash, Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Task

## Prompt

```
You are running the weekly Church Directory enrichment wave for MOOP's (Adam Johns, U.S.M.C. Ministries) theological church directory at usmcmin.org. The current target is 7,777 verified churches, currently at ~3,940.

## Your job

Spend session budget expanding and enriching the directory at docs/data/churches.json. Quality > quantity. Every change must be verified via WebSearch — no fabricated data.

## Step 1: Assess current state

Run this bash command and tell me the results:
node -e "const d=JSON.parse(require('fs').readFileSync('docs/data/churches.json','utf8')); console.log('Total:',d.churches.length); console.log('FB:',d.churches.filter(c=>c.facebook).length); console.log('YT:',d.churches.filter(c=>c.youtube).length); console.log('Real pastors:',d.churches.filter(c=>c.pastor&&c.pastor!=='See website'&&c.pastor!=='Verify').length); console.log('Need FB:',d.churches.filter(c=>!c.facebook&&c.website&&String(c.website).startsWith('http')).length);"

## Step 2: Launch 4 parallel enrichment waves (Task tool, run_in_background:true)

**Wave 1: Social media enrichment** — Find 50 churches with website but no Facebook. For each, WebSearch for '[name] [city] [state] facebook instagram youtube' and extract VERIFIED social URLs (facebook.com/..., youtube.com/@..., instagram.com/..., x.com/...). Update top-level fields: facebook, youtube, instagram, twitter.

**Wave 2: YouTube scan** — Find 50 GREEN-rated churches without YouTube. Scrape church websites for embedded youtube.com/ URLs. Only add verified channels.

**Wave 3: Pastor data** — Find 50 churches where pastor == 'See website' or 'Verify'. WebSearch for pastor name, update pastor field. Also find pastor_facebook, pastor_twitter, pastor_instagram, pastor_linkedin if public.

**Wave 4: Expansion** — Add 50-75 NEW verified churches. Target denominations with thin coverage: Methodist (UMC) 0.06%, Pentecostal 0.17%, Independent Baptist 0.15%, Baptist Other 0.6%, Wesleyan 0.9%, Churches of Christ 0.5%. Every new church needs verified pastor + website + Facebook. No placeholders. Full schema with all fields: id, name, address, pastor, denomination, denomination_family, website, facebook, overall_rating, scores (10 keys), score_notes, assessment, tags, engagement, slug.

## Schema rules (CRITICAL)

- All IDs compared as String(c.id)
- Social fields are top-level (facebook, youtube, instagram, twitter, pastor_facebook, pastor_twitter, pastor_instagram, pastor_linkedin) — NOT nested in a 'social' object
- denomination_family must be one of 27 clean families: Southern Baptist (SBC), Non-Denominational, Baptist (Other), Reformed Baptist, Independent Baptist, Presbyterian (PCA), Presbyterian (OPC), Presbyterian (EPC), Presbyterian (PCUSA), Presbyterian (Other), Calvary Chapel, Lutheran (LCMS), Lutheran (ELCA), Lutheran (Other), Anglican (ACNA), Episcopal (TEC), EFCA, Church of Christ, Wesleyan / Nazarene, Methodist (UMC), Acts 29, Pentecostal / Charismatic, Christian & Missionary Alliance, Converge, Progressive Mainline, Catholic, Other
- MOOP rubric: GREEN = 6+ greens in core categories (Christology, Scripture, Soteriology, Gender, Leadership, Men's Discipleship) + no reds. RED minimum for female pastors/elders, egalitarian. BLACK for LGBTQ-affirming, apostate, prosperity gospel, feminized theology. Flag female pastors, CBF affiliation, PCUSA/ELCA/UMC-post-split/TEC as RED/BLACK.
- NEVER add churches that don't actually exist. If WebSearch can't verify a church, skip it.

## Step 3: After agents complete

Run these bash commands in order:
rm -f enrich*.js ny*.js sw*.js yt*.js fb*.js quality*.js expand*.js
node generate-church-pages.js 2>&1 | tail -3
git add docs/data/churches.json docs/churches/
git commit -m "Weekly enrichment: [stats]"
git push origin main

## Step 4: Report

Output a final summary: total churches before/after, social media totals, notable additions or finds (female pastors caught, denomination mismatches, scandals), and estimated weeks remaining to 7,777 target at current pace.

## Budget awareness

You are running weekly on the user's ~20% of weekly subscription budget. Don't burn the entire budget — aim for 200-300 churches touched (mix of enriched + added), then stop and push. If the wave is going well and budget allows, launch a second round of 4 agents. If budget is tight, finish the first round cleanly and push.
```

## Manual Setup Instructions

1. Go to https://claude.ai/code/scheduled
2. Click "Create New Trigger"
3. Set name: "Weekly Church Directory Enrichment"
4. Set cron: `0 13 * * 6`
5. Set repo: https://github.com/adamljohns/bible-reading-plan-bot
6. Paste the prompt above
7. Save and enable

## Alternative: Retry via Claude Code

Once you're on the new M5 Max Thursday and logged into Claude Code fresh, run:
```
/schedule
```
And select "Create new trigger" — auth should work on a fresh session.
