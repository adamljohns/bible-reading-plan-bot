---
name: add-network-or-denomination
description: Add a new Reformed/evangelical network or denomination tag to the MOOP Church Directory, including downloading its official logo and wiring it into the directory-networks page. Use whenever the user wants to add a new network ("add OPC as a network", "include the PCA brand", "add the URCNA logo", "wire in Converge Network"), tag churches with a new network slug, or refresh an existing network's logo. Handles the apple-touch-icon scrape with Google favicon fallback, NETWORK_META + NETWORK_ORDER updates in scripts/build-directory-networks.js, and the inline NETWORK_BRANDING update in generate-church-pages.js so per-church pages also pick up the new logo. Triggers in the bible-reading-plan-bot repo.
---

# Add Network or Denomination

The end-to-end workflow for adding a new entry to the seven-network methodology page and to the per-church hero chip row. Replicates the SBC + tonight's-eight-logos pattern from 2026-05-28; the same recipe scales to any Reformed/evangelical network the user wants represented.

## When to use this skill

- User asks to "add" a network or denomination by name or acronym
- User asks to "wire in" or "include" a network's branding
- User asks to refresh / re-download a network's logo (Google favicon caches go stale)
- After integrating a new network's per-church URLs and wanting to surface the brand identity

## When NOT to use this skill

- Just tagging an EXISTING network onto more churches (use churches.json edits + the existing `church-directory-enrichment` skill)
- Adding a network's METHODOLOGY text only (edit `scripts/build-directory-networks.js` `NETWORK_META[<slug>].methodology` directly)
- Changing color palette of an existing network (one-liner edit to the color field)

## Workflow

### 1. Pick a network slug

Lowercase, dash-separated, short. Conventions used so far: `sbc`, `founders`, `9marks`, `tgc-cn`, `acts29`, `sgc`, `pillar-network`, `trinity-foundation`. If adding a denomination, use the lowercase acronym: `opc`, `pca`, `arp`, `urcna`, `lcms`, etc.

### 2. Download the logo

```bash
bash .claude/skills/add-network-or-denomination/scripts/fetch-logo.sh <slug> <domain>
```

Example: `bash .claude/skills/add-network-or-denomination/scripts/fetch-logo.sh opc opc.org`

The script tries `https://DOMAIN/apple-touch-icon.png` first (highest quality, usually 180x180), falls back to `apple-touch-icon-precomposed.png`, then to Google's favicon service at 128px. Writes to `docs/assets/icons/networks/<slug>.png`. Verifies the result is a valid PNG (catches the "HTML 404 page disguised as a PNG" trap that hit Founders earlier today).

### 3. Add the NETWORK_META entry

Edit `scripts/build-directory-networks.js`:

- Add an entry to `NETWORK_META` with these fields:
  - `label` — full name shown in card headers ("Orthodox Presbyterian Church")
  - `shortLabel` — chip text ("OPC")
  - `color` — hex; pick from the established palette so the page stays cohesive
  - `logo` — `'/assets/icons/networks/<slug>.png'`
  - `directoryUrl` — the public directory URL
  - `description` — one-line summary, 100-150 chars
  - `methodology` — full paragraph; include vetting strength rating (HIGH / MEDIUM / LOW)
- Add the slug to `NETWORK_ORDER` (controls render order on the page)

### 4. Mirror into the per-church template

Edit `generate-church-pages.js` `NETWORK_BRANDING` constant. Add `'<slug>': { short: '<shortLabel>', logo: '/assets/icons/networks/<slug>.png' }`. This is what renders the chip on per-church pages.

### 5. Regenerate + commit + push

```bash
node scripts/build-directory-networks.js
node generate-church-pages.js | tail -3
git pull --rebase --autostash
git add docs/assets/icons/networks/<slug>.png \
        scripts/build-directory-networks.js \
        generate-church-pages.js \
        docs/directory-networks.html \
        docs/churches/
git commit -m "Add <Network Name> as network/denomination tag in directory"
git push
```

### 6. Verify live

After the GitHub Pages deploy lands (typically 1-2 minutes), visit:

- `https://usmcmin.org/directory-networks.html#meth-<slug>` — should show the new methodology card with logo
- Any per-church page where the church is tagged `cross_listed_in: ['<slug>']` — should show the new chip in the hero

## Common gotchas

- **Logo as HTML 404**: some `/apple-touch-icon.png` URLs return an HTML error page with a `Content-Type: image/png` header. The fetch script checks `file -b` to reject non-PNG payloads. If it fails, try the homepage HTML grep path (curl the homepage, grep for `apple-touch-icon`, fetch the resolved URL).
- **Sizes vary**: some networks ship 100x100, some 192x192, some 180x180. The page CSS handles all sizes via `object-fit: contain` in a fixed-size frame; do not resize the source PNG.
- **Color collisions**: existing networks use brown / blue / green / red / purple / blue-gray / brown / gold. Pick a hex that visually contrasts with whatever is alphabetically adjacent.
- **Tagging churches**: this skill adds the network entity; it does NOT tag churches with the new slug. For that, you typically run a separate integration pass that matches the network's directory entries to MOOP churches by name + city (the `integrate-network-urls.js` pattern from 2026-05-28).
