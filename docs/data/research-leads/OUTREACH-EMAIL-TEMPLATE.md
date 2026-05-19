# Outreach Email Template — "$100 Website Build" Ministry Offer

**Persona:** Pastor John Wesley Graves
**Outbound address:** `usmcministries2022+preacher@gmail.com`
**Target audience:** Small US churches in MOOP whose website is defunct AND who don't have an active Facebook page as a workaround.
**Source list:** `docs/data/research-leads/website-outreach-candidates.json` (143 records, US-only, sorted by editorial priority).

## Voice/style notes

- **Pastoral, warm, brotherly.** Adam's directive: "maybe when I email these people I could offer to build them a website for a hundred bucks or something to get them working well." Treat this as ministry-of-helps, not sales.
- **Avoid sales jargon.** No "value-add," no "drive engagement," no "leveraging digital presence." Just plain English about a real practical need.
- **Acknowledge the small thing.** A broken website is a small thing in eternity — say so. This frames the offer as service, not solving a crisis they didn't know they had.
- **Single ask, single reply.** One short question, one easy yes/no path. No multi-step funnel.
- **Identify a real person.** Pastor John Wesley Graves writes; not "the team at" or a faceless org.
- **Brief.** Sub-400 words.

## The template

```
TO:      [varies — try info@, pastor@, or office@ at their former domain;
         or DM via Facebook if they have one]
SUBJECT: A small offer for [Church Name]

Pastor / Brothers in [Church Name],

Grace and peace from a fellow pastor down the road. I lead a small
ministry that walks alongside under-resourced churches in the work of
faithful gospel presentation online — particularly when a website has
gone down or never quite gotten built in the first place.

I came across [Church Name] in [City] while compiling a directory of
faithful, gospel-preaching congregations across the United States. Your
church belongs in that company, but the website I had on file for you
isn't loading right now. That's a small thing in eternity, but it does
make it harder for a visiting traveler or a curious neighbor to find
your service times, your statement of faith, or your pastor's name.

If it would be useful, I'd be glad to build you a simple, durable
landing page for $100, one-time — name, address, service times,
beliefs, pastor, and a phone number. That's the whole offer; I'm not
trying to sell you a system. Hosting and basic upkeep after that we
can work out for a token monthly fee, or you can take the files and
host them yourselves. Whatever serves the church.

If this is a help, just reply and I'll send a one-page intake form.
If it isn't, I rejoice with you in whatever the Lord is doing locally
and will not bother you again.

In the bonds of the gospel,

Pastor John Wesley Graves
USMC Ministries — a ministry of helps
usmcministries2022+preacher@gmail.com
```

## Workflow for using this template

1. Run `node scripts/draft-outreach-emails.js --top 20` to generate
   personalized drafts for the top 20 candidates (sorted by editorial
   priority — orthodox-leaning + GREEN/YELLOW + network-cross-listed
   first). Output goes to `/tmp/outreach-drafts.txt`.
2. **Review every draft** before sending. The script can't know what's
   right for a particular church (e.g., if you have personal context
   about the pastor's tradition, adjust tone accordingly).
3. Send via the `usmcministries2022+preacher@gmail.com` Gmail alias.
   Recommended: Boomerang or a similar tool to schedule sends 2–3 minutes
   apart so they don't all hit at once.
4. Track replies in a follow-up sheet. Don't re-email a church that
   declined; respect the "and will not bother you again" promise.

## Doctrinal compass

The Top 20 sort order prioritizes:

1. `signatures_aggregate=green` (any Nashville/Dallas signature)
2. Then by `overall_rating` (green > yellow > red > black)
3. Then by # of conservative-network cross-listings (Founders, 9Marks,
   TGC, Acts 29, SGC, Pillar, Trinity)
4. Then alphabetical

This pushes the most-likely-doctrinally-aligned candidates first. If
you'd rather expand to all 143 with `--top 143`, do it deliberately —
the long tail will include records where the rating is lower-confidence.

## When NOT to send

- If a record is rated `red` or `black` and `signatures_aggregate` is
  also `red`, the doctrinal trajectory probably isn't a fit for what
  Pastor John Wesley Graves can endorse with his name. Skip.
- If the church has updated their website OR added an active Facebook
  page since the curation ran (worth a 30-second check before sending),
  the offer is moot. The script's curation step already filters those,
  but data drifts.
- If you have prior context that the church doesn't want this kind of
  outreach. Personal context overrides the script.
