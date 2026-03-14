# QA Audit Report — USMC Ministries Website

**Generated:** 2026-03-14 15:55:00 EDT  
**Scope:** All 55 HTML files in `/docs/`  
**Target Version:** V4.8  
**Auditor:** MbPro (automated)

---

## Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟡 Warning | 7 |
| 🔵 Info | 24 |
| **Total** | **31** |

> **Note:** 48 initial "Critical: Broken Link" findings were false positives — all were JavaScript string concatenation/template literals that build `href` values dynamically at runtime (e.g., `href="' + url + '"`, `href="${url}"`). These are valid JS patterns, not broken static links.

---

## Detailed Findings

### 📄 `wheelhouse.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Wrong Version | 🟡 Warning | 501 | `BTE V4.7` displayed in stats section | Change to `V4.8` |
| Wrong Version | 🟡 Warning | 513 | Link text says `MOOP Bible V4.7` | Change to `V4.8` |

### 📄 `index.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Duplicate ID (JS-generated) | 🟡 Warning | 512-553 | `id="stepInput"` appears in 6 template literal branches — only one renders at a time in wizard, but screen readers/querySelector may misbehave | Consider using unique IDs per step or `data-` attributes |
| Missing Labels | 🟡 Warning | — | 17 visible form inputs but only 14 labels/aria-labels/placeholders | Add `<label>` or `aria-label` to unlabeled inputs |
| alert() calls | 🔵 Info | 597, 654, 661, 669, 749, 758, 760, 770, 775 | 9 `alert()` calls in production code (form validation feedback) | Consider replacing with inline toast/notification UI |

### 📄 `bible.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Missing alt | 🟡 Warning | 1606 | `<img>` tag without `alt` attribute | Add descriptive alt text |
| console.log | 🔵 Info | 333, 334, 340, 341, 354, 356 | 6 `console.log` statements (translation engine debugging) | Remove or guard with `if(DEBUG)` for production |
| Version comments (NOT user-facing) | 🔵 Info | various | Code comments reference `v3.3`, `v3.4`, `v4.0`, `v4.1`, `v4.2` — these document feature history in JS comments, not user-visible version strings | No action needed — these are developer notes |

### 📄 `chronological.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Missing Labels | 🟡 Warning | — | 1 visible form input without label/aria-label/placeholder | Add `<label>` or `aria-label` |

### 📄 `family-meeting.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| alert() calls | 🔵 Info | 1405, 1571, 1610, 1618 | 4 `alert()` calls in production code | Consider replacing with inline UI notifications |

### 📄 `counseling-intake.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| alert() call | 🔵 Info | 601 | 1 `alert()` call for form validation | Consider inline validation message |

### 📄 `assets/icons/preview.html`

| Issue | Severity | Line | Details | Fix |
|-------|----------|------|---------|-----|
| Missing alt (×19) | 🟡 Warning | 18-36 | 19 `<img>` tags without `alt` attributes | Add alt text (e.g., `alt="shield anchor icon"`) |
| No Viewport | 🔵 Info | — | Missing viewport meta tag | Add viewport meta — though this is likely an internal dev preview page |

---

## ✅ Clean Files (No Issues Found) — 33 files

- `about.html`
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
- `fitness.html`
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
- All 22 `verse/*.html` files (dynamically-built links are valid JS)

---

## ✅ Checks That Passed Globally

| Check | Result |
|-------|--------|
| **Broken static links** | ✅ All static `href` targets exist |
| **Missing assets** | ✅ All `src` references resolve to existing files |
| **Missing CSS** | ✅ All stylesheet references valid (all CSS is inline) |
| **Localhost/test URLs** | ✅ None found in any file |
| **Form actions** | ✅ No forms post to invalid/localhost URLs |
| **Viewport meta** | ✅ Present in all 54 user-facing pages (only missing in internal `assets/icons/preview.html`) |
| **Mobile responsiveness** | ✅ All pages use inline responsive CSS with media queries |
| **Hardcoded test data** | ✅ No test/debug URLs detected |

---

## Recommended Priority Actions

### 🟡 Should Fix (Warnings)

1. **`wheelhouse.html` lines 501, 513** — Update version from V4.7 → V4.8 (2 occurrences)
2. **`bible.html` line 1606** — Add `alt` attribute to `<img>` tag
3. **`index.html`** — Add labels to 3 unlabeled form inputs
4. **`chronological.html`** — Add label to 1 form input
5. **`assets/icons/preview.html`** — Add alt text to 19 icon preview images

### 🔵 Nice to Have (Info)

6. **`index.html`, `family-meeting.html`, `counseling-intake.html`** — Replace `alert()` calls with inline UI notifications (14 total)
7. **`bible.html`** — Remove/guard 6 `console.log` statements
8. **`index.html`** — Consider unique IDs per wizard step instead of reusing `stepInput`

---

## Audit Methodology

1. **Internal Links** — All `href` attributes checked against filesystem (JS-generated dynamic hrefs excluded as false positives)
2. **Asset References** — All `src` and stylesheet `href` verified against filesystem
3. **Anchor Fragments** — `#fragment` links matched to `id` attributes in same file
4. **JavaScript** — Scanned for `console.log`, `alert()`, undefined variables, syntax patterns
5. **Accessibility** — Missing `alt` tags on `<img>`, form label coverage checked
6. **Mobile** — Viewport meta tag and responsive CSS patterns verified
7. **Version** — All version strings checked against V4.8 target (code comments excluded)
8. **Localhost** — Scanned for `localhost`, `127.0.0.1`, `0.0.0.0` in all contexts
9. **Duplicate IDs** — All `id` attributes checked for uniqueness per document
10. **Form Actions** — All `<form action>` values validated for proper targets

**Total files audited:** 55  
**Overall health:** 🟢 Excellent — no critical issues, only minor warnings
