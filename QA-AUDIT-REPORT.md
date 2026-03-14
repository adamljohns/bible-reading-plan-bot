# QA Audit Report — USMC Ministries Website
**Generated:** 2026-03-14 15:51:58 
**Scope:** All 55 HTML files in `/docs/`
**Target Version:** V4.8

---

## Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 48 |
| 🟡 Warning | 47 |
| 🔵 Info | 20 |
| **Total** | **115** |

### Top Files by Issue Count

- **`bible.html`** — 25 issues (2C/17W/6I)
- **`assets/icons/preview.html`** — 20 issues (0C/20W/0I)
- **`index.html`** — 16 issues (0C/7W/9I)
- **`family-meeting.html`** — 4 issues (0C/0W/4I)
- **`chronological.html`** — 2 issues (1C/1W/0I)
- **`verse/1-corinthians-6-19.html`** — 2 issues (2C/0W/0I)
- **`verse/1-timothy-4-12.html`** — 2 issues (2C/0W/0I)
- **`verse/2-chronicles-20-12.html`** — 2 issues (2C/0W/0I)
- **`verse/2-timothy-1-7.html`** — 2 issues (2C/0W/0I)
- **`verse/2-timothy-4-7.html`** — 2 issues (2C/0W/0I)

---

## Detailed Findings

### 📄 `assets/icons/preview.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Missing alt | 🟡 Warning | 18 | `<img>` without `alt` attribute | Add descriptive alt text |
| Missing alt | 🟡 Warning | 19 | `<img>` without `alt` attribute | Add descriptive alt text |
| Missing alt | 🟡 Warning | 20 | `<img>` without `alt` attribute | Add descriptive alt text |
| Missing alt | 🟡 Warning | 21 | `<img>` without `alt` attribute | Add descriptive alt text |
| Missing alt | 🟡 Warning | 22 | `<img>` without `alt` attribute | Add descriptive alt text |
| Missing alt | 🟡 Warning | 23 | `<img>` without `alt` attribute | Add descriptive alt text |
| Missing alt | 🟡 Warning | 24 | `<img>` without `alt` attribute | Add descriptive alt text |
| Missing alt | 🟡 Warning | 25 | `<img>` without `alt` attribute | Add descriptive alt text |
| Missing alt | 🟡 Warning | 26 | `<img>` without `alt` attribute | Add descriptive alt text |
| Missing alt | 🟡 Warning | 27 | `<img>` without `alt` attribute | Add descriptive alt text |
| Missing alt | 🟡 Warning | 28 | `<img>` without `alt` attribute | Add descriptive alt text |
| Missing alt | 🟡 Warning | 29 | `<img>` without `alt` attribute | Add descriptive alt text |
| Missing alt | 🟡 Warning | 30 | `<img>` without `alt` attribute | Add descriptive alt text |
| Missing alt | 🟡 Warning | 31 | `<img>` without `alt` attribute | Add descriptive alt text |
| Missing alt | 🟡 Warning | 32 | `<img>` without `alt` attribute | Add descriptive alt text |
| Missing alt | 🟡 Warning | 33 | `<img>` without `alt` attribute | Add descriptive alt text |
| Missing alt | 🟡 Warning | 34 | `<img>` without `alt` attribute | Add descriptive alt text |
| Missing alt | 🟡 Warning | 35 | `<img>` without `alt` attribute | Add descriptive alt text |
| Missing alt | 🟡 Warning | 36 | `<img>` without `alt` attribute | Add descriptive alt text |
| No Viewport | 🟡 Warning | — | Missing `<meta name="viewport">` tag | Add `<meta name="viewport" content="width=device-width, initial-scale=1">` |

### 📄 `bible.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 1447 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 1456 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |
| Wrong Version | 🟡 Warning | 1042 | Found `v3.4` — should be V4.8 | Update version to V4.8 |
| Wrong Version | 🟡 Warning | 1235 | Found `v4.2` — should be V4.8 | Update version to V4.8 |
| Wrong Version | 🟡 Warning | 1240 | Found `v3.4` — should be V4.8 | Update version to V4.8 |
| Wrong Version | 🟡 Warning | 1263 | Found `v3.4` — should be V4.8 | Update version to V4.8 |
| Wrong Version | 🟡 Warning | 1270 | Found `v4.1` — should be V4.8 | Update version to V4.8 |
| Wrong Version | 🟡 Warning | 1424 | Found `v3.4` — should be V4.8 | Update version to V4.8 |
| Wrong Version | 🟡 Warning | 1427 | Found `v3.4` — should be V4.8 | Update version to V4.8 |
| Missing alt | 🟡 Warning | 1606 | `<img>` without `alt` attribute | Add descriptive alt text |
| Wrong Version | 🟡 Warning | 313 | Found `v4.0` — should be V4.8 | Update version to V4.8 |
| Wrong Version | 🟡 Warning | 316 | Found `v4.0` — should be V4.8 | Update version to V4.8 |
| Wrong Version | 🟡 Warning | 318 | Found `v4.0` — should be V4.8 | Update version to V4.8 |
| Wrong Version | 🟡 Warning | 336 | Found `v4.1` — should be V4.8 | Update version to V4.8 |
| Wrong Version | 🟡 Warning | 343 | Found `v4.1` — should be V4.8 | Update version to V4.8 |
| Wrong Version | 🟡 Warning | 343 | Found `v4.2` — should be V4.8 | Update version to V4.8 |
| Wrong Version | 🟡 Warning | 359 | Found `v4.1` — should be V4.8 | Update version to V4.8 |
| Wrong Version | 🟡 Warning | 416 | Found `v3.3` — should be V4.8 | Update version to V4.8 |
| Wrong Version | 🟡 Warning | 818 | Found `v4.2` — should be V4.8 | Update version to V4.8 |
| console.log | 🔵 Info | 333 | console.log in production code | Remove or disable for production |
| console.log | 🔵 Info | 334 | console.log in production code | Remove or disable for production |
| console.log | 🔵 Info | 340 | console.log in production code | Remove or disable for production |
| console.log | 🔵 Info | 341 | console.log in production code | Remove or disable for production |
| console.log | 🔵 Info | 354 | console.log in production code | Remove or disable for production |
| console.log | 🔵 Info | 356 | console.log in production code | Remove or disable for production |

### 📄 `chronological.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 723 | `href="${url}"` — target not found | Fix path or create missing file |
| Missing Labels | 🟡 Warning | — | 1 visible form inputs but only 0 labels/aria-labels/placeholders | Add `<label>` or `aria-label` to all form inputs |

### 📄 `counseling-intake.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| alert() call | 🔵 Info | 601 | alert() in production code | Remove for production |

### 📄 `family-meeting.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| alert() call | 🔵 Info | 1405 | alert() in production code | Remove for production |
| alert() call | 🔵 Info | 1571 | alert() in production code | Remove for production |
| alert() call | 🔵 Info | 1610 | alert() in production code | Remove for production |
| alert() call | 🔵 Info | 1618 | alert() in production code | Remove for production |

### 📄 `fitness.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 1043 | `href="${sc.href}"` — target not found | Fix path or create missing file |

### 📄 `index.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Wrong Version | 🟡 Warning | 475 | Found `v4.0` — should be V4.8 | Update version to V4.8 |
| Wrong Version | 🟡 Warning | 504 | Found `v4.0` — should be V4.8 | Update version to V4.8 |
| Duplicate ID | 🟡 Warning | 512 | `id="stepInput"` appears 6 times (lines 512, 515, 518, 521, 525, 553) | Make IDs unique |
| Wrong Version | 🟡 Warning | 556 | Found `v4.0` — should be V4.8 | Update version to V4.8 |
| Wrong Version | 🟡 Warning | 673 | Found `v4.0` — should be V4.8 | Update version to V4.8 |
| Wrong Version | 🟡 Warning | 679 | Found `v4.0` — should be V4.8 | Update version to V4.8 |
| Missing Labels | 🟡 Warning | — | 17 visible form inputs but only 14 labels/aria-labels/placeholders | Add `<label>` or `aria-label` to all form inputs |
| alert() call | 🔵 Info | 597 | alert() in production code | Remove for production |
| alert() call | 🔵 Info | 654 | alert() in production code | Remove for production |
| alert() call | 🔵 Info | 661 | alert() in production code | Remove for production |
| alert() call | 🔵 Info | 669 | alert() in production code | Remove for production |
| alert() call | 🔵 Info | 749 | alert() in production code | Remove for production |
| alert() call | 🔵 Info | 758 | alert() in production code | Remove for production |
| alert() call | 🔵 Info | 760 | alert() in production code | Remove for production |
| alert() call | 🔵 Info | 770 | alert() in production code | Remove for production |
| alert() call | 🔵 Info | 775 | alert() in production code | Remove for production |

### 📄 `verse/1-corinthians-6-19.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/1-timothy-4-12.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 915 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 923 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/2-chronicles-20-12.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/2-timothy-1-7.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/2-timothy-4-7.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/deuteronomy-32-35.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/deuteronomy-6-6-7.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/ephesians-5-14-16.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/ephesians-5-25.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/ephesians-6-10-18.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/ezekiel-33-7.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/ezekiel-36-26.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/hebrews-12-2-3.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/jeremiah-29-11.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/jeremiah-29-7.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/john-3-16.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/luke-14-33.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/proverbs-22-6.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/proverbs-27-17.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 917 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 925 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/proverbs-3-5-6.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 918 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 926 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/romans-12-19-21.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `verse/romans-8-28-30.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Broken Link | 🔴 Critical | 916 | `href="' + url + '"` — target not found | Fix path or create missing file |
| Broken Link | 🔴 Critical | 924 | `href="' + stepBibleUrl(c.strongs) + '"` — target not found | Fix path or create missing file |

### 📄 `wheelhouse.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Wrong Version | 🟡 Warning | 501 | Found `V4.7` — should be V4.8 | Update version to V4.8 |
| Wrong Version | 🟡 Warning | 513 | Found `V4.7` — should be V4.8 | Update version to V4.8 |

---

## ✅ Clean Files (No Issues)

- `about.html`
- `blog-christian-localism.html`
- `cert-cnc.html`
- `cert-cpt.html`
- `cert-fit20.html`
- `cert-pes.html`
- `cert-wls.html`
- `consulting.html`
- `counseling.html`
- `crew-quarters.html`
- `finance.html`
- `financial-intake.html`
- `first-officer.html`
- `links.html`
- `mentoring-intake.html`
- `mentoring.html`
- `mops.html`
- `retirement.html`
- `serving-intake.html`
- `serving.html`
- `stays/index.html`
- `trainer.html`
- `uniting.html`
- `usmc-ministries.html`
- `usmcmin-com.html`

---

## Audit Methodology

1. **Internal Links** — All `href` attributes checked against filesystem
2. **Asset References** — All `src` and stylesheet `href` verified
3. **Anchor Fragments** — `#fragment` links matched to `id` attributes
4. **JavaScript** — Scanned for console.log, alert(), obvious bugs
5. **Accessibility** — Missing `alt` tags, form labels checked
6. **Mobile** — Viewport meta tag presence verified
7. **Version** — All version strings checked against V4.8
8. **Localhost** — Scanned for test/dev URLs
9. **Duplicate IDs** — All `id` attributes checked for uniqueness
10. **Form Actions** — All `<form action>` values validated

**Total files audited:** 55
