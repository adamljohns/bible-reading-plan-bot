---
name: refine-church-images
description: Audit and fix the logo + hero photo quality on MOOP Church Directory records — catch cross-contamination (a church showing a DIFFERENT church's logo/photo), replace bare favicons with real header logos, and flag images that need a human eyeball. Use whenever the user says the images or logos "aren't right", "look off", "are the wrong church", "are low quality", or asks to "finalize", "clean up", "polish", or "refine" a church's or a region's visual identity. Distinct from the bulk image autopilot (which only fills missing images); this skill QUALITY-CHECKS what is already there and corrects it. Includes a header-logo scraper that finds a site's real logo (not just its apple-touch-icon) with domain-safety checks. Triggers in the bible-reading-plan-bot repo.
---

# Refine Church Images

The quality-control counterpart to the image autopilot. The autopilot answers "does this church have an image?"; this skill answers "is the image actually correct and good?" It catches three failure modes that pass a not-null check but look wrong on the page:

1. **Cross-contamination** — the church is showing a *different* church's logo or photo because the scraper followed a shared CMS template or an embedded third-party site (the canonical case: a small Assembly of God church whose site embeds a Mosaic Fort Worth template, so its logo resolved to `mosaicfortworth.com`).
2. **Bare favicons posing as logos** — `favicon.ico` / `favicon.png` / `cropped-favicon` rendered at 86px on the profile page looks like garbage. A real header logo is far better.
3. **Stock / template hero images** — a generic theme banner or stock photo where a real building photo or no photo would be more honest.

## When to use this skill

- User reports images/logos "look wrong", "off", "low quality", or "the wrong church"
- User asks to "finalize" / "polish" / "clean up" a church or a city/state's visual identity
- After a bulk image autopilot run, as a QC pass over what it captured
- Periodically, as drift control (CMS template changes can silently swap a logo)

## When NOT to use this skill

- Filling churches that simply have NO image yet (use `autopilot-launch` / image-autopilot-v2)
- Non-image enrichment — pastor, sources, quick_links (use `enrich-church-single` or `autopilot-launch`)

## The tools

| Script | Purpose |
| --- | --- |
| `scripts/audit.sh [scope]` | Print a per-church image/logo audit for a scope: flags domain mismatches (contamination), bare favicons, missing logos/heroes. Read-only. |
| `../../../scripts/scrape-church-logos.js` | Find a site's REAL header logo (the `<img>` in header/nav with "logo" in its attrs), with a domain-safety gate that rejects logos served from a different church's domain. |
| `../../../scripts/merge-logo-scrapes.js` | Apply scraped logos to `image_thumb`, AND clear cross-contaminated logos+heroes (domain != website domain, not a known CDN). |

## Workflow

### 1. Audit the scope

```bash
bash .claude/skills/refine-church-images/scripts/audit.sh Fredericksburg
```

This prints, per church: website domain, logo domain + verdict, hero domain + verdict. Verdicts:
- `OK` — domain matches the church's own site or a known asset CDN
- `CONTAMINATION` — image is served from a *different* church's root domain (must fix)
- `BARE-FAVICON` — logo is a favicon.ico/png (replace with a real header logo)
- `MISSING` — no image in this field

### 2. Scrape real header logos

For the scope, run the header-logo scraper. It is Fredericksburg-first within a state scope.

```bash
node scripts/scrape-church-logos.js --state VA --count 83 --jsonl /tmp/logo-fxbg.jsonl
# or a single church:
node scripts/scrape-church-logos.js --church <slug> --jsonl /tmp/logo-one.jsonl
```

The scraper writes one JSONL record per church with either a domain-safe `logo_url` or a `logo_rejected` URL (when the only logo it found was on a foreign domain).

### 3. Merge — apply good logos, clean contamination

```bash
node scripts/merge-logo-scrapes.js /tmp/logo-fxbg.jsonl
```

This:
- Sets `image_thumb` to the real header logo where one was found
- Clears `image_thumb` where the existing value was the rejected foreign-domain logo
- Sweeps ALL churches in the file (not just scraped ones) for hero contamination: clears `image_url` whose domain does not match the website and is not a known CDN

### 4. Eyeball the ambiguous ones (browser)

Some calls need a human (or vision) look: is this header `<img>` actually the logo, or a sponsor badge? Is the hero a building photo or a stock banner? Open the candidates in a browser and look.

- Prefer a connected browser via the Chrome MCP (`mcp__Claude_in_Chrome__*`) or open the image URLs directly.
- For a fast batch eyeball, build a scratch HTML page that renders all the scope's logos in a grid and screenshot it (see `scripts/contact-sheet.sh` if present, or write the church name + `<img>` rows to `/tmp/logo-sheet.html` and open it).
- When an image is wrong but the scraper could not find a better one, clear the field rather than leave the wrong one. An honest blank beats a wrong logo.

### 5. Regenerate, verify, commit

```bash
node generate-church-pages.js | tail -3
# spot check a fixed church:
grep 'church-logo' docs/churches/<slug>.html | head -1
git pull --rebase --autostash
git add docs/data/churches.json docs/churches/
git commit -m "Refine <scope> church logos: +N real header logos, cleared M contaminated"
git push
```

## The doctrine of honest blanks

A church page with no logo is fine; a church page showing the WRONG church's logo is a credibility hit, because the directory's entire value proposition is careful, accurate vetting. When in doubt, clear the field. The `cleared-contamination` source value marks records that were cleaned, so a later pass can revisit them and try to find a correct logo.

## Gotchas

- **Shared CMS templates**: Assembly of God, some Baptist church-plant networks, and white-label church website builders (nucleus, thechurchco, Subsplash) embed a template whose logo points at the template owner. The domain-safety gate handles the obvious cases; the CDN allowlist in both scripts must stay in sync.
- **SVG logos**: crisp and preferred; the scraper scores them higher. They render fine in the 86px frame.
- **A real logo on a CDN**: a church's genuine logo hosted on squarespace-cdn / cloudinary / wp.com is allowed through the gate via the CDN allowlist, because the church really does serve its own assets there. The risk is a CDN that hosts MANY churches' assets under one domain (thechurchco) — there, domain match cannot confirm identity, so eyeball those.
- **Keep the two allowlists in sync**: `scrape-church-logos.js` and `merge-logo-scrapes.js` each carry a `CDN_OK` regex. If you add a CDN to one, add it to the other.
