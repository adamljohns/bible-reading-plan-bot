#!/usr/bin/env python3
"""
V5.7.2 data quality cleanup:

  1. 67 records have score_notes as a STRING instead of a dict. The
     page renderer expects score_notes to be a per-dimension dict
     (christology/scripture/gender/leadership/etc.) — when it's a
     string, the dimension-by-dimension scorecard doesn't render
     properly. All 67 are Wesleyan-Holiness adds from the parallel
     session with the same shape; convert each string into a dict
     with the content placed on the most-relevant dimension.

  2. 544 records have uppercase overall_rating ("GREEN", "YELLOW",
     "BLACK"). The page CSS keys off lowercase class names
     (`rating-green`, `rating-yellow`, etc.) — uppercase values
     work because the CSS-class generator lowercases, but they're
     inconsistent in the JSON, break sort comparisons, and confuse
     audit scripts. Normalize all to lowercase.
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path("/Users/adamjohns/bible-reading-plan-bot")
CHURCHES = ROOT / "docs/data/churches.json"
TODAY = date.today().isoformat()


def main():
    data = json.loads(CHURCHES.read_text())
    churches = data.get("churches", [])

    string_sn_fixed = 0
    uc_rating_fixed = 0

    for c in churches:
        # ---- Fix string score_notes ----
        sn = c.get("score_notes")
        if isinstance(sn, str) and sn.strip():
            # Determine which dimension is most appropriate based on content
            text = sn.lower()
            best_dim = "denominational"  # default
            if any(k in text for k in ["soteriology", "monergism", "synergistic", "prevenient grace", "entire sanctification", "free will", "elect"]):
                best_dim = "soteriology"
            elif any(k in text for k in ["women's ordination", "ordains women", "female pastor", "egalitarian", "complementarian", "gender"]):
                best_dim = "gender"
            elif any(k in text for k in ["expository", "preaching", "sermon"]):
                best_dim = "preaching"
            elif any(k in text for k in ["elder", "polity", "governance"]):
                best_dim = "leadership"
            elif any(k in text for k in ["inerran", "scripture", "biblical authority"]):
                best_dim = "scripture"
            elif any(k in text for k in ["denomination", "affiliated", "wesleyan", "holiness", "polity"]):
                best_dim = "denominational"

            # Construct dict — assign the original string to the best dimension
            # AND put a small note on denominational (since most relevant for Wesleyan)
            new_sn = {best_dim: sn}
            # If best_dim isn't denominational and content mentions denominational issues, also add to denominational
            if best_dim != "denominational" and any(k in text for k in ["polity", "discipline", "ordination", "wesleyan", "holiness", "denomination"]):
                new_sn["denominational"] = sn
            c["score_notes"] = new_sn
            string_sn_fixed += 1
            # Audit marker
            c["enrichment_notes"] = (c.get("enrichment_notes") or "") + (
                f"\n--- {TODAY} V5.7.2: score_notes was a string; converted "
                f"to dict with content on '{best_dim}' dimension."
            )

        # ---- Lowercase uppercase ratings ----
        r = c.get("overall_rating")
        if isinstance(r, str) and r != r.lower() and r.lower() in ("green", "yellow", "red", "black"):
            c["overall_rating"] = r.lower()
            uc_rating_fixed += 1

        # ---- Also lowercase any uppercase per-dimension scores ----
        sc = c.get("scores")
        if isinstance(sc, dict):
            for dim, val in list(sc.items()):
                if isinstance(val, str) and val != val.lower() and val.lower() in ("green", "yellow", "red", "black"):
                    sc[dim] = val.lower()

    # Write back
    CHURCHES.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    print(f"V5.7.2 cleanup:")
    print(f"  String -> dict score_notes:  {string_sn_fixed}")
    print(f"  Uppercase -> lowercase rating: {uc_rating_fixed}")


if __name__ == "__main__":
    main()
