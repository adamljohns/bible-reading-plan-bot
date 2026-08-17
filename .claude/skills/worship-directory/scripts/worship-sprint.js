export const meta = {
  name: 'worship-sprint',
  description: 'Source public-domain hymns/psalms per category toward the worship songbook target',
  phases: [{ title: 'Source' }],
}
const A = typeof args === 'string' ? JSON.parse(args) : (args || {})
const CATS = A.cats || []
const ROUND = A.round || '?'

const SCHEMA = {
  type: 'object',
  properties: {
    hymns: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          title: { type: 'string' },
          author: { type: 'string' },
          year: { type: 'string' },
          publicDomain: { type: 'boolean' },
          key: { type: 'string' },
          lyrics: { type: 'string' },
          source: { type: 'string' },
        },
        required: ['title', 'author', 'year', 'publicDomain', 'key', 'lyrics', 'source'],
      },
    },
  },
  required: ['hymns'],
}

const catPrompt = (name) => `Build up a church worship-song directory with **public-domain hymns and gospel songs** a congregation sings. Your niche (round ${ROUND}):

CATEGORY: ${name}

Return up to 25 hymns. Hard requirements:
- **Public domain ONLY** (published before 1929, or author AND translator died 70+ years ago). When unsure about copyright, set publicDomain=false and skip.
- **Accurate lyrics** — use WebSearch to pull faithful lyrics from a public-domain source (Hymnary.org, hymnal.net, CyberHymnal/Hymntime, Timeless Truths, Wikisource). 2-5 well-known verses, separated by a blank line. NEVER invent or paraphrase lyrics; if you cannot verify the real text, omit the hymn.
- **Go DEEP, not famous**: assume the ~400 most common public-domain hymns (Amazing Grace, Holy Holy Holy, It Is Well, Be Thou My Vision, all the Watts/Wesley/Crosby/Newton warhorses, common doxologies, famous Christmas carols, well-known Sacred Harp tunes) are ALREADY in the directory. Your job is layer 2-3: solid, singable, historically loved hymns in this niche that congregations still use but most directories miss.
- Give author, approx year, a common singing key, and your source URL.

Return JSON per the schema. 18 rock-solid verified hymns beat 25 shaky ones. Skip any hymn you cannot source real lyrics for.`

const psalterPrompt = (range) => `You are building the metrical-psalm section of a church worship directory from the **1650 Scottish Metrical Psalter** (public domain).

YOUR RANGE: Psalms ${range}

For EACH psalm in your range, return one entry:
- title: the psalm's metrical first line + " (Psalm N)" — e.g. "The Lord's My Shepherd, I'll Not Want (Psalm 23)"
- author: "Scottish Metrical Psalter"
- year: "1650"
- publicDomain: true
- key: the common singing key of a tune traditionally paired with it (e.g. Crimond in D for Psalm 23); if unknown use "C"
- lyrics: 2-6 stanzas of the ACTUAL 1650 metrical text, stanzas separated by a blank line — use WebSearch to pull the genuine text (Hymnary.org, Wikisource, thewestminsterstandard.org, ccel.org). NEVER invent or modernize the text.
- source: the URL you verified against

Skip any psalm whose genuine metrical text you cannot verify — accuracy over coverage. Return JSON per the schema.`

const verifyPrompt = (batch) => `You are AUDITING lyrics already published in a church worship directory for fidelity to their public-domain sources. For each song below, WebSearch its authoritative source (Hymnary.org, thewestminsterstandard.org, Wikisource, CyberHymnal) and compare against the published text.

SONGS (JSON): ${batch}

Return per the schema: for each song, set title = the song title, source = URL you checked, publicDomain = true if the published text is faithful (minor punctuation/spelling variance OK), false if it has REAL errors (wrong words, invented lines, missing famous verses, wrong author/year), and put a one-line description of any problem found in the lyrics field (or "OK" if faithful). Do not rewrite lyrics.`

// Video mode: research the official recording for each song in a worklist batch.
// Returns {videos:[{slug, youtube, confidence, why}]} — apply-video-ids.js is the
// gatekeeper that validates and merges them.
const VIDEO_SCHEMA = {
  type: 'object',
  properties: {
    videos: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          slug: { type: 'string' },
          youtube: { type: 'string' },
          confidence: { type: 'string' },
          why: { type: 'string' },
        },
        required: ['slug', 'youtube', 'confidence', 'why'],
      },
    },
  },
  required: ['videos'],
}

const videoPrompt = (batch) => `Find the best YouTube video for each worship song below, so a worship leader can hear it.

SONGS (JSON): ${batch}

For EACH song, WebSearch (and WebFetch the YouTube watch page when useful) to identify the video, then return:
- slug: EXACTLY the slug given — never invent or alter it
- youtube: the 11-character video ID only (from watch?v=<ID> or youtu.be/<ID>), NOT a full URL
- confidence: "high" only if you are confident the video is that exact song by that artist; "low" otherwise
- why: the video title + channel you matched, so a human can audit it

Rules that matter more than coverage:
- **Prefer the official artist/label channel**, then a well-known lyric video, then a reputable live worship recording.
- **Right song, right artist.** Many worship songs share titles (there are a dozen different "Great Are You Lord"). Match the writers/artist given.
- For public-domain hymns, a well-produced hymn recording or congregational singing video is ideal; avoid random amateur uploads.
- **A wrong video is worse than no video.** If you cannot confirm, set confidence "low" — it will be discarded, and that is the correct outcome.
- Never reuse one video ID for multiple songs.

Return JSON per the schema. Skip nothing — return an entry per song, using low confidence where unsure.`

phase('Source')
const results = await parallel(
  CATS.map((c, i) => () =>
    agent(
      c.type === 'psalter' ? psalterPrompt(c.range)
        : c.type === 'verify' ? verifyPrompt(c.batch)
        : c.type === 'video' ? videoPrompt(c.batch)
        : catPrompt(c.name),
      {
        label: `r${ROUND}:${c.type === 'psalter' ? 'ps' + c.range : c.type === 'verify' ? 'verify' + i : c.type === 'video' ? 'video' + i : c.name.slice(0, 28)}`,
        phase: 'Source',
        schema: c.type === 'video' ? VIDEO_SCHEMA : SCHEMA,
      }
    )
  )
)
if (A.mode === 'video') {
  const videos = results.filter(Boolean).flatMap((r) => r.videos || [])
  log(`round ${ROUND}: ${videos.length} video candidates`)
  return { round: ROUND, videos }
}
const hymns = results.filter(Boolean).flatMap((r) => r.hymns || [])
const pd = hymns.filter((h) => h && h.publicDomain !== undefined && h.lyrics && h.lyrics.length > (A.mode === 'verify' ? 1 : 60))
const seen = new Set(); const unique = []
for (const h of pd) { const k = (h.title || '').toLowerCase().replace(/[^a-z0-9]/g, ''); if (!k || seen.has(k)) continue; seen.add(k); unique.push(h) }
log(`round ${ROUND}: ${hymns.length} raw, ${pd.length} kept, ${unique.length} unique`)
return { round: ROUND, raw: hymns.length, unique: unique.length, hymns: A.mode === 'verify' ? hymns : unique.filter((h) => h.publicDomain) }
