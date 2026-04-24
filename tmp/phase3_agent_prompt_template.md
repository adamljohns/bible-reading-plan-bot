# Phase 3 Agent Prompt Template (Wayback-at-fetch-time)

Use this template for R58 and all future validation rounds. The
only change from the current template is **steps 4-5 and a revised
schema requirement**: every WebFetch URL must also be captured as a
Wayback snapshot at the time of fetch, and the patch must include
`enrichment_sources_archived` mapping original→snapshot.

---

```
R{N} VALIDATION AUDIT. {COUNT} yellow-rated churches.

Inputs: `/Users/adamjohns/bible-reading-plan-bot/tmp/r{N}_batch_{B}.json`
Output: `/Users/adamjohns/bible-reading-plan-bot/tmp/r{N}_out_{B}.json`
        (bare JSON array of patches)

**Rules:**
1. ONE WebFetch per church. On fail: flag `website_status: "dead"`.
2. ENVIRONMENTAL_FAILURE only on 3+ CONSECUTIVE safety-blocks. Per-site
   errors (ECONNREFUSED, 403, timeouts) are NOT environmental.
3. Incremental writes to the output file every 5 churches.
4. NEW (Phase 3 — Wayback capture): after each successful WebFetch,
   submit the SAME URL to the Wayback Save Page Now endpoint:
      https://web.archive.org/save/<URL>
   Wayback will respond with a redirect to the snapshot URL of the
   form `https://web.archive.org/web/<TIMESTAMP>/<URL>`. Record that
   snapshot URL.
   - If Wayback save fails (rate limited, 5xx), check the availability
     API for any existing snapshot as fallback:
        https://archive.org/wayback/available?url=<URL>
   - If neither produces a snapshot, just proceed without one.
5. ~25 tool uses total (one WebFetch + one Wayback call per church,
   roughly). Never fabricate.

**Framing:**
YELLOW — flip green on substantive orthodox evidence (confessional +
elder plurality + network tie, OR BFM2000 + men's ministry for SBC);
flip red on red flags (women senior pastors, ARC, egalitarian
governance, affirming language, CBF "freedoms" rhetoric,
URL-mismatch-to-unrelated-church, Comer "Practicing the Way"
curriculum, Kendi/DiAngelo CRT books).

**Each patch MUST include:**
- `id` (required)
- ONLY changed score fields
- NEW: `enrichment_sources` (if adding) — include BOTH the live URL
  AND the Wayback snapshot URL when available. Format:
  ```json
  "enrichment_sources": [
    "https://web.archive.org/web/20260424113607/https://example.com/beliefs"
  ],
  "enrichment_sources_live": [
    "https://example.com/beliefs"
  ]
  ```
  The `enrichment_sources` list should contain the ARCHIVED URLs;
  `enrichment_sources_live` preserves originals for audit.
  (If no snapshot was obtained, include the live URL in both arrays.)

**Report (under 200 words):**
yellows_flipped_green, yellows_flipped_red, yellows_held, dead count,
wayback_snapshots_captured, notable findings.
```

---

## Why this matters

Every validation claim going forward gets an archived-URL trail. No
more "we looked at their homepage on 2026-04-24" with no proof —
instead, "here's the Wayback snapshot we took at the moment we
scored this church."

Retro-actively applied to all ~4,100 churches, we'll need many
years of enrichment to cover them all this way. But **every new
round is self-archiving from R58 forward**, so the problem decays
rather than grows.
