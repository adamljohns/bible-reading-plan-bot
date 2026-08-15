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

phase('Source')
const results = await parallel(
  CATS.map((c, i) => () =>
    agent(
      c.type === 'psalter' ? psalterPrompt(c.range) : c.type === 'verify' ? verifyPrompt(c.batch) : catPrompt(c.name),
      {
        label: `r${ROUND}:${c.type === 'psalter' ? 'ps' + c.range : c.type === 'verify' ? 'verify' + i : c.name.slice(0, 28)}`,
        phase: 'Source',
        schema: SCHEMA,
      }
    )
  )
)
const hymns = results.filter(Boolean).flatMap((r) => r.hymns || [])
const pd = hymns.filter((h) => h && h.publicDomain !== undefined && h.lyrics && h.lyrics.length > (A.mode === 'verify' ? 1 : 60))
const seen = new Set(); const unique = []
for (const h of pd) { const k = (h.title || '').toLowerCase().replace(/[^a-z0-9]/g, ''); if (!k || seen.has(k)) continue; seen.add(k); unique.push(h) }
log(`round ${ROUND}: ${hymns.length} raw, ${pd.length} kept, ${unique.length} unique`)
return { round: ROUND, raw: hymns.length, unique: unique.length, hymns: A.mode === 'verify' ? hymns : unique.filter((h) => h.publicDomain) }
