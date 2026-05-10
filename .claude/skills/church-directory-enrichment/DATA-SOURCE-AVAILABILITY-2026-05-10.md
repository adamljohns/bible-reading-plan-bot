# Data-Source Availability Notes — 2026-05-10

This note tracks denomination-directory websites that returned non-fetchable
content during Round 12 of V5.5→V5.7 enrichment work. All findings courtesy
of the CMA-MIX agent's honest abort report on 2026-05-10.

## Sites unreachable via WebFetch

- **cmalliance.org** — homepage 200, but `/find-a-church/`, `/about`,
  `/locations/`, `/district*`, `/church-search` all return 403
- **vineyardusa.org** — only `/` resolves; `/about/find-a-vineyard/`,
  `/find-a-church/`, `/about/locations/` all return 404
- **churches.efca.org** — search form is JavaScript-rendered; no data in
  static HTML
- **lcmc.net find-a-congregation** — JavaScript-rendered (per Round 11
  Lutheran agent report)
- **thenalc.org find-a-congregation** — JavaScript-rendered (per Round 11
  Lutheran agent report)

## Individual church sites consistently failing

The following church URLs returned ECONNREFUSED through the WebFetch proxy
during the Round 12 CMA sweep:

- firstalliancetoledo.org
- mansfieldalliance.com
- chapelmadison.org
- canvasdayton.com
- allegheny-center.org
- thechapelnyack.org
- gateway-alliance.com
- easterndistrict.efca.org
- allianceconnect.cmalliance.org

## Workarounds for future rounds

1. **Browser-tool agent** — use the Claude-in-Chrome MCP tools or the
   OpenClaw browser tool to execute JS-rendered search forms on
   cmalliance.org / churches.efca.org / lcmc.net / thenalc.org.
2. **State-association sites** — many of these denominations have state
   chapters whose static HTML directories are reachable (e.g. CMA Eastern
   PA District site at allianceconnect-easternpa.org sometimes resolves).
3. **Tribune / press sources** — Religion News Service and the Christian
   Index (SBC) regularly cover denominational milestone events that name
   senior pastors.
4. **Foundation lookups** — Cooperative Program contributor lists and
   foundation-grantee public records can corroborate church identity +
   leadership.

## Recommendation for Round 13+

Skip CMA + LCMC + NALC + Vineyard backfill until a browser-tool agent is
available. Continue with denominations whose directories ARE reachable
(SBC, PCA, ACNA, Reformed Baptist via founders.org + arbca.com, Wesleyan
Church via wesleyan.org, AoG via ag.org, Calvary Chapel via cgn.org).
