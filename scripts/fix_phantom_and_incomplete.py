#!/usr/bin/env python3
"""
V4.9.5 cleanup pass:
  - 3 incomplete-address greens get full street addresses
  - 1 incomplete-address green (Good Shepherd Anglican Roanoke) gets
    walked back to yellow + review flag because the site doesn't resolve
    and there's no public ACNA listing — possibly phantom from V4.9.4
    green-hunter
  - 5 phantom-flagged records from V4.9.3 get final disposition:
    defunct/dead, address fix, or stay-yellow-with-stronger-notes

References:
  - Lord of Life Lutheran Fairfax: 5114 Twinbrook Rd verified via DDG
  - Christ Community Church Leesburg: 818 S King St verified on church site
  - Reston Community Church PCA: 2620 Reston Pkwy in Herndon (not Reston)
    verified on church site
  - Good Shepherd Anglican Roanoke: no working URL, no Wayback snap, no
    DDG hits, no Mid-Atlantic Diocese listing - mark as review-flagged
  - FBC Lynchburg: building sold Oct 2024 to ACNA Church of the Good
    Shepherd; site fbclva.com fails TLS in 2026 (last Wayback 2025-06)
  - Providence Baptist Glen Allen: SBCV directory has 4956 Dominion Blvd
    (record had wrong address 4175 Mountain Rd which is Glen Allen
    Baptist, a different congregation)
  - Cornerstone Bible Sterling: site offline, last Wayback 2024-04;
    keep yellow with phantom-warning notes, no green-light disposition
  - Freedom Church AG (Spotsylvania): domain 301-redirects to
    mosaicfortworth.com (TX); no replacement site - mark defunct
  - Short Pump Baptist: site refuses connection on all paths; closest
    valid candidates at the address are Grace Community Baptist (SBC)
    and North Gayton Baptist (BGAV) - mark as likely-defunct
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path("/Users/adamjohns/bible-reading-plan-bot")
CHURCHES = ROOT / "docs/data/churches.json"
TODAY = date.today().isoformat()


def main():
    data = json.loads(CHURCHES.read_text())
    churches = data if isinstance(data, list) else data.get("churches", data)
    by_id = {c["id"]: c for c in churches if "id" in c}

    changes = []

    # === INCOMPLETE-ADDRESS GREENS ===

    # Lord of Life Lutheran Fairfax (LCMS)
    rec = by_id["lord-of-life-lutheran-fairfax"]
    rec["address"] = "5114 Twinbrook Rd, Fairfax, VA 22032"
    rec["enrichment_notes"] = (rec.get("enrichment_notes") or "") + (
        f"\n--- {TODAY} V4.9.5 cleanup: address backfilled to "
        "5114 Twinbrook Rd, Fairfax, VA 22032 (verified via DDG search; "
        "LCMS Northern Virginia)."
    )
    changes.append(("lord-of-life-lutheran-fairfax", "address", "Fairfax, VA",
                    "5114 Twinbrook Rd, Fairfax, VA 22032"))

    # Christ Community Church Leesburg (LCMS)
    rec = by_id["christ-community-church-leesburg"]
    rec["address"] = "818 South King Street, Leesburg, VA 20175"
    rec["enrichment_notes"] = (rec.get("enrichment_notes") or "") + (
        f"\n--- {TODAY} V4.9.5 cleanup: address backfilled to "
        "818 South King Street, Leesburg, VA 20175 (verified on church "
        "site /church/ page). Also operates Christ Community Christian "
        "School at this campus."
    )
    changes.append(("christ-community-church-leesburg", "address", "Leesburg, VA",
                    "818 South King Street, Leesburg, VA 20175"))

    # Reston Community Church PCA — actually meets in Herndon
    rec = by_id["reston-community-pca"]
    rec["address"] = "2620 Reston Parkway, Herndon, VA 20171"
    rec["enrichment_notes"] = (rec.get("enrichment_notes") or "") + (
        f"\n--- {TODAY} V4.9.5 cleanup: address backfilled to "
        "2620 Reston Parkway, Herndon, VA 20171 (verified on reston.cc). "
        "Note: church meets in Herndon despite the 'Reston' brand. "
        "Sunday service 4:30 PM (single service)."
    )
    rec["services"] = "Sundays 4:30 PM"
    changes.append(("reston-community-pca", "address", "Reston, VA",
                    "2620 Reston Parkway, Herndon, VA 20171"))

    # Good Shepherd Anglican Roanoke — likely phantom
    rec = by_id["good-shepherd-anglican-roanoke-va"]
    rec["overall_rating"] = "yellow"
    rec["overall_label"] = "ACNA — UNVERIFIED, possibly phantom record"
    rec["review_flag"] = {
        "flagged": True,
        "reason": (
            "V4.9.4 green-hunter agent listed this church but no working "
            "URL was found in V4.9.5 cleanup pass. goodshepherdroanoke.org "
            "does not resolve; no Wayback Machine snapshots exist; "
            "no Mid-Atlantic Diocese parish listing surfaces. "
            "Possibly conflated with Church of the Good Shepherd "
            "Lynchburg (the ACNA congregation that purchased FBC "
            "Lynchburg's building at 1100 Court St in October 2024). "
            "Recommend deletion or replacement with the actual Lynchburg "
            "Good Shepherd record."
        ),
        "website_status": "dead",
    }
    if "needs-review" not in (rec.get("tags") or []):
        rec.setdefault("tags", []).append("needs-review")
    if "possible-phantom" not in (rec.get("tags") or []):
        rec.setdefault("tags", []).append("possible-phantom")
    rec["enrichment_notes"] = (rec.get("enrichment_notes") or "") + (
        f"\n--- {TODAY} V4.9.5 cleanup: walked back from green to yellow. "
        "Cannot verify existence: site does not resolve, no Wayback, no "
        "DDG hits, no ACNA Mid-Atlantic Diocese listing. May be conflated "
        "with Church of the Good Shepherd Lynchburg (different parish, "
        "took over FBC Lynchburg building Oct 2024)."
    )
    changes.append(("good-shepherd-anglican-roanoke-va", "rating", "green",
                    "yellow + review_flag (possible phantom)"))

    # === PHANTOM-FLAGGED RECORDS FROM V4.9.3 ===

    # FBC Lynchburg — building sold to ACNA Oct 2024
    rec = by_id["first-baptist-lynchburg-va"]
    rec["overall_rating"] = "dead"
    rec["overall_label"] = "DEFUNCT — historic building sold Oct 2024 to ACNA Good Shepherd"
    rec["review_flag"] = {
        "flagged": True,
        "reason": (
            "Historic 1100 Court St building was sold to ACNA Church of "
            "the Good Shepherd in October 2024. fbclva.com fails TLS in "
            "2026 (cert mismatched); last Wayback snapshot June 2025. "
            "No replacement web presence detected; congregation appears "
            "to have dissolved or relocated without forwarding signal. "
            "Recommend removal in next dedup pass OR conversion to a "
            "redirect to the ACNA Good Shepherd successor record."
        ),
        "website_status": "dead",
    }
    if "needs-review" not in (rec.get("tags") or []):
        rec.setdefault("tags", []).append("needs-review")
    if "defunct" not in (rec.get("tags") or []):
        rec.setdefault("tags", []).append("defunct")
    rec["enrichment_notes"] = (rec.get("enrichment_notes") or "") + (
        f"\n--- {TODAY} V4.9.5 cleanup: marked dead. Building at "
        "1100 Court St was sold October 2024 to ACNA's Church of the "
        "Good Shepherd; FBC Lynchburg congregation status post-sale "
        "is unverified (likely dissolved or relocated; no successor "
        "web presence found). fbclva.com no longer resolves with valid TLS."
    )
    changes.append(("first-baptist-lynchburg-va", "rating", "yellow",
                    "dead + needs-review (building sold, congregation gone)"))

    # Providence Baptist Glen Allen — fix address per SBCV
    rec = by_id["providence-baptist-church-glen-allen"]
    rec["address"] = "4956 Dominion Blvd, Glen Allen, VA 23060"
    # Clear the prior review_flag since we now have the correct address
    if rec.get("review_flag"):
        rec["review_flag"] = {
            "flagged": False,
            "resolution": (
                "V4.9.5 cleanup: address corrected from 4175 Mountain Rd "
                "(which is Glen Allen Baptist Church, a different "
                "congregation with female pastor Dr. Melissa Fallon) "
                "to 4956 Dominion Blvd per SBCV directory."
            ),
            "website_status": "still-down-but-record-now-distinct",
        }
    rec["enrichment_notes"] = (rec.get("enrichment_notes") or "") + (
        f"\n--- {TODAY} V4.9.5 cleanup: address corrected from "
        "'4175 Mountain Rd' (which is Glen Allen Baptist, a different "
        "BGAV-aligned congregation with a female pastor) to "
        "4956 Dominion Blvd per SBCV directory. pbcva.org still "
        "ECONNREFUSED in 2026; congregation listing remains in SBCV "
        "but website is down."
    )
    changes.append(("providence-baptist-church-glen-allen", "address",
                    "4175 Mountain Road, Glen Allen, VA 23060",
                    "4956 Dominion Blvd, Glen Allen, VA 23060"))

    # Cornerstone Bible Sterling — keep yellow, document Wayback last seen
    rec = by_id["cornerstone-bible-church-sterling"]
    rec["enrichment_notes"] = (rec.get("enrichment_notes") or "") + (
        f"\n--- {TODAY} V4.9.5 cleanup: site still offline; last Wayback "
        "snapshot 2024-04-25 (built on Weebly editmysite). Held yellow "
        "with phantom-warning. If still offline at next sweep, recommend "
        "demotion to dead."
    )
    if "phantom-warning" not in (rec.get("tags") or []):
        rec.setdefault("tags", []).append("phantom-warning")
    changes.append(("cornerstone-bible-church-sterling", "tag",
                    "(none)", "phantom-warning + persistent yellow"))

    # Freedom Church AG (Spotsylvania) — defunct
    rec = by_id["fredericksburg-assembly-of-god-spotsylvania"]
    rec["overall_rating"] = "dead"
    rec["overall_label"] = "DEFUNCT — domain redirects to Texas church"
    rec["review_flag"] = {
        "flagged": True,
        "reason": (
            "Domain freedomchurchag.com 301-redirects to "
            "mosaicfortworth.com (a Texas church) with UTM 'Domains' "
            "campaign tag — the Spotsylvania AG's domain was sold or "
            "parked. No replacement web presence detected; congregation "
            "status remains unverifiable. Recommend removal in next "
            "dedup pass."
        ),
        "website_status": "dead",
    }
    if "needs-review" not in (rec.get("tags") or []):
        rec.setdefault("tags", []).append("needs-review")
    if "defunct" not in (rec.get("tags") or []):
        rec.setdefault("tags", []).append("defunct")
    rec["enrichment_notes"] = (rec.get("enrichment_notes") or "") + (
        f"\n--- {TODAY} V4.9.5 cleanup: marked dead. Domain "
        "freedomchurchag.com redirects to a Texas church and has been "
        "sold/parked; no replacement site detected for Spotsylvania."
    )
    changes.append(("fredericksburg-assembly-of-god-spotsylvania", "rating",
                    "yellow", "dead + needs-review (domain sold to TX)"))

    # Short Pump Baptist — likely defunct
    rec = by_id["short-pump-baptist-church"]
    rec["overall_rating"] = "dead"
    rec["overall_label"] = "DEFUNCT — no web presence, no congregation found at address"
    rec["review_flag"] = {
        "flagged": True,
        "reason": (
            "shortpumpbaptist.org refuses connection on all paths; "
            "no Wayback snapshots ever; not in BGAV or SBCV directories. "
            "Closest valid Baptist congregations at this address range "
            "are Grace Community Baptist (2400 Pump Rd, SBC) and "
            "North Gayton Baptist (3244 Pump Rd, BGAV). The 'Short Pump "
            "Baptist' tag at 3555 Pump Rd appears to be either a never-"
            "launched plant or a record-creation error. Recommend removal."
        ),
        "website_status": "never-existed",
    }
    if "needs-review" not in (rec.get("tags") or []):
        rec.setdefault("tags", []).append("needs-review")
    if "defunct" not in (rec.get("tags") or []):
        rec.setdefault("tags", []).append("defunct")
    rec["enrichment_notes"] = (rec.get("enrichment_notes") or "") + (
        f"\n--- {TODAY} V4.9.5 cleanup: marked dead. No web presence ever "
        "detected; not in denomination directories; Pump Rd Baptist "
        "presence is covered by Grace Community Baptist (SBC) and "
        "North Gayton Baptist (BGAV)."
    )
    changes.append(("short-pump-baptist-church", "rating", "yellow",
                    "dead + needs-review (no evidence of existence)"))

    # === Write ===
    CHURCHES.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"V4.9.5 cleanup applied: {len(changes)} record changes")
    print()
    for cid, kind, old, new in changes:
        print(f"  [{kind:7}] {cid}")
        print(f"            {old}")
        print(f"         -> {new}")
        print()


if __name__ == "__main__":
    main()
