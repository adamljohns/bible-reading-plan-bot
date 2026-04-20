# Enrichment rubric — USMC Ministries Church Directory

You are enriching an existing entry in the MOOP church directory. Your goal is to replace placeholder "Verify" / "Unknown" score notes with **concrete, evidence-based** notes derived from the church's own public materials (their website's About / What-We-Believe / Staff-and-Leadership / Ministries pages), supplemented with targeted web search where needed.

**Hard rules:**

1. **Never fabricate.** If the church's website doesn't state its position, write the note as "Not stated on available sources — verify in person" and keep the score at **yellow** (caution). Do NOT invent a position.
2. **Be frugal with web calls.** Target: 1 WebFetch of the church's main site (or /about, /beliefs page) per church. Use WebSearch only when the website is bare or specific claims can't be verified from it.
3. **Cite what you saw.** Each concrete note should reference the evidence ("Statement of Faith affirms inerrancy", "Pastor Jane Doe listed as Senior Pastor on Staff page").
4. **Upgrade or downgrade the score if the evidence supports it.** A church currently marked `overall_rating: green` that turns out to have a female lead pastor is `red`. A `red`-rated church that turns out to be solid Reformed is `green`. Update both the scorecard score AND the overall rating/label if warranted.
5. **Flag defunct or moved churches** by setting `flag_for_review: true` and explaining in `review_reason` (e.g., "Website returns 404", "Congregation disbanded per local news", "Pastor moved to different church").

## Rubric definitions (score each of 10 dimensions)

### christology
- **green**: Trinitarian, affirms Apostles'/Nicene Creed, affirms Christ's deity and exclusivity (John 14:6)
- **yellow**: Orthodox but vaguely stated; creeds not named
- **red**: Christ's deity not clearly affirmed; universalist/pluralist trajectory
- **black**: Denies Trinity (Oneness Pentecostal, JW-style), modalism, or Arian — a disqualifier

### scripture
- **green**: Explicit inerrancy (Chicago Statement level), Scripture as final authority
- **yellow**: "Bible is authoritative" without clear inerrancy statement
- **red**: Scripture plus tradition/experience as co-equal authority
- **black**: Rejects inerrancy or openly liberal hermeneutic

### soteriology
- **green**: Protestant sola fide, substitutionary atonement, justification by grace through faith alone
- **yellow**: Generic evangelical language without clarity
- **red**: Works-based salvation, prosperity gospel, sacramental regeneration, Federal Vision
- **black**: Universalism, religious pluralism, denies substitutionary atonement

### gender (Biblical Design)
- **green**: Patriarchal household vision, male headship, anti-feminist, household-centered
- **yellow**: Complementarian (male-only elders/pastors but adopts "role-based" rather than designed-nature framing)
- **red**: Egalitarian — women pastors or elders
- **black**: Affirms gender ideology (LGBTQ+-affirming), feminist theology, anti-patriarchy

### leadership
- **green**: Plurality of male elders, transparent accountability structure
- **yellow**: Elder-led but single dominant personality
- **red**: Single-pastor model with no elder accountability
- **black**: Cult-like control structure, documented abuse patterns

### preaching
- **green**: Expository / verse-by-verse, Christ-centered
- **yellow**: Mixed expository-topical
- **red**: Primarily topical/therapeutic/seeker-sensitive, felt-needs driven
- **black**: Word of Faith, prosperity, pure motivational

### mission
- **green**: Clear gospel focus, Great Commission central, missions giving visible
- **yellow**: Mission stated but generic
- **red**: Social-justice replaces gospel mission
- **black**: Gospel denial or works-salvation distortion

### cultural
- **green**: No DEI/CRT language; conservative biblical stance
- **yellow**: Mixed/ambiguous — some social-issue language without clear framing
- **red**: DEI/CRT language, "biblical justice" per Revoice/Side-B patterns, woke vocabulary
- **black**: Fully captured by progressive theology (affirming, Revoice conferences, Moore-Hill trajectory)

### mens_discipleship
- **green**: Dedicated men's ministry with regular discipleship; men's retreats, groups
- **yellow**: Men's group exists but minimal info
- **red**: No men's focus; sentimentalized or effeminate culture
- (no black tier for this dimension)

### denominational
- **green**: Confessional denomination with real accountability (PCA, OPC, SBC-confessional, CREC, LCMS, ACNA with Jerusalem Declaration)
- **yellow**: Independent but visible affiliations (Founders, 9Marks, Acts 29)
- **red**: Fully independent with no accountability structure
- **black**: Liberal mainline (PCUSA, ELCA, TEC, UCC, UMC post-2022 split, CBF, BGAV-progressive, DOC)

## Output schema (per church)

```json
{
  "id": "church-id-goes-here",
  "flag_for_review": false,
  "review_reason": "",
  "website_status": "alive | dead | redirects | parked",
  "overall_rating": "green | yellow | red | black",
  "overall_label": "Short label under 60 chars",
  "scores": {
    "christology": "green|yellow|red|black",
    "scripture": "...", "soteriology": "...", "gender": "...",
    "leadership": "...", "preaching": "...", "mission": "...",
    "cultural": "...", "mens_discipleship": "...", "denominational": "..."
  },
  "score_notes": {
    "christology": "1-2 concrete sentences with evidence",
    "scripture": "...", "soteriology": "...", "gender": "...",
    "leadership": "...", "preaching": "...", "mission": "...",
    "cultural": "...", "mens_discipleship": "...", "denominational": "..."
  },
  "pastor": "Only update if current field is wrong or 'Unknown'",
  "pastor_credentials": "Only update if discoverable; else 'Not published'",
  "founded": "Year or 'Not published'",
  "denomination_detail": "Concrete affiliation detail",
  "gender_detail": "Concrete summary of gender/leadership stance with names",
  "sources_consulted": ["https://...", "https://..."],
  "enrichment_notes": "Optional short note on what was surprising or required judgment"
}
```

Leave any field as `null` if you have no change to make. Only include fields you're confident about — don't echo unchanged data.
