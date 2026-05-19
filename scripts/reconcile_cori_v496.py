#!/usr/bin/env python3
"""
V4.9.6 reconciliation: re-apply V4.9.1-V4.9.5 changes that got lost or
reverted by the parallel session's Phase 6 / Round 3 / dedup rebases.

This script:
  1. Re-applies Mount Fxbg + Mount Stafford scalar corrections (founded,
     services, YouTube, denomination, pastor credentials)
  2. Re-merges mt-ararat-baptist-stafford -> the-mount-church-stafford
     (audit trail preserved; legacy ID removed)
  3. Re-merges brock-road-baptist-church -> chancellor-christian-church-spotsylvania
  4. Re-applies Bedford Baptist + Bedford Road Baptist SBC -> BGAV (notes
     already document this conclusion but denomination field was reset)
  5. Re-applies 10 VA yellow flips from V4.9.3 (6 green + 4 red)
  6. Fixes Garden City Roanoke pastor: Brian Willard -> Charlie Lanier
     (SEBTS M.Div. 2003) — name correction lost in the rebase
  7. Re-adds 23 confessional VA records from V4.9.4 backup
     (PCA/OPC/ARP/REC/ACNA/LCMS); upgrades 2 existing yellows to green;
     skips 2 already-green-equivalent

Skips deliberately (parallel session has stronger calls):
  - lord-of-life-lutheran-fairfax (parallel: black — they found bad evidence)
  - christ-community-church-leesburg (parallel: red — they found issues)
"""
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path("/Users/adamjohns/bible-reading-plan-bot")
CHURCHES = ROOT / "docs/data/churches.json"
BACKUP_GH = Path("/tmp/backup_green_hunter.json")
TODAY = date.today().isoformat()


def main():
    data = json.loads(CHURCHES.read_text())
    churches = data.get("churches", [])
    by_id = {c["id"]: c for c in churches if "id" in c}

    backup_green_hunter = json.loads(BACKUP_GH.read_text())
    backup_gh_by_id = {r["id"]: r for r in backup_green_hunter}

    changes = []

    def log(cid, action, detail):
        changes.append((cid, action, detail))

    # === 1. Mount Fxbg scalar corrections ===
    if "the-mount-church" in by_id:
        rec = by_id["the-mount-church"]
        rec["founded"] = "1907 (founded as Mount Ararat Baptist Church)"
        rec["services"] = "Sundays 9:15 AM & 10:45 AM"
        rec["youtube"] = "https://www.youtube.com/@themountva"
        rec["denomination_detail"] = (
            "Baptist General Association of Virginia (BGAV). BGAV publicly "
            "differentiated itself from the SBC in November 2023 over women in "
            "pastoral roles."
        )
        # Scrub internal-review jargon if present
        sn = rec.get("score_notes") or {}
        if isinstance(sn, dict):
            for k, v in list(sn.items()):
                if isinstance(v, str):
                    if "rendered on this specific campus fetch" in v or "Red CONFIRMED at denominational level — held" in v:
                        v = v.replace("rendered on this specific campus fetch", "visible on this campus page")
                        v = v.replace("Red CONFIRMED at denominational level — held", "denominational concern stands")
                        sn[k] = v
            # Replace denominational note with cleaner version
            sn["denominational"] = (
                "Multi-site BGAV congregation (formerly Mount Ararat Baptist "
                "Church, est. 1907). BGAV publicly differentiated itself from "
                "the Southern Baptist Convention in November 2023 over women "
                "in pastoral roles, and the BGAV framework permits women "
                "pastors. The Fredericksburg campus's own pastoral team is "
                "currently male, but the denominational framework and "
                "multi-site streaming model keep this campus on the cautious "
                "side of yellow at the denominational dimension."
            )
        log("the-mount-church", "scalar-fix", "founded 1907, services, YouTube @themountva, denom_detail BGAV")

    # === 2. Mount Stafford scalar corrections ===
    if "the-mount-church-stafford" in by_id:
        rec = by_id["the-mount-church-stafford"]
        rec["founded"] = "1907 (founded as Mount Ararat Baptist Church)"
        rec["services"] = "Sundays 8:30 AM, 10:00 AM, 11:30 AM"
        rec["youtube"] = "https://www.youtube.com/@themountva"
        rec["pastor"] = "Adam Sauer (Lead Pastor, since 2022)"
        rec["pastor_credentials"] = (
            "Adam Sauer — M.Div. and M.A. in Nonprofit Management, North Park "
            "Theological Seminary (Evangelical Covenant Church-affiliated, "
            "Chicago). Note: ECC seminary pipeline is unusual for a historic "
            "Baptist congregation — verify ongoing doctrinal alignment with "
            "Baptist distinctives."
        )
        rec["denomination"] = "Baptist (BGAV)"
        rec["denomination_family"] = "Baptist (BGAV)"
        rec["denomination_detail"] = (
            "Baptist General Association of Virginia (BGAV). The congregation "
            "traces back to 1907 as Mount Ararat Baptist Church and rebranded "
            "as The Mount Church across five campuses. BGAV publicly "
            "differentiated itself from the SBC in November 2023 over women "
            "in pastoral roles."
        )
        sn = rec.get("score_notes") or {}
        if isinstance(sn, dict):
            sn["leadership"] = (
                "Plurality of elected elders per the qualifications in "
                "1 Timothy 3:1–7 and Titus 1:5–9. Lead Pastor Adam Sauer "
                "(since 2022) preaches the primary teaching slot, which is "
                "streamed to the Fredericksburg, Bealeton, and El Monte "
                "campuses."
            )
            sn["denominational"] = (
                "BGAV-affiliated. BGAV permits women pastors and broke "
                "publicly with the SBC in November 2023 over that question. "
                "The Stafford campus's own pastoral team is currently male, "
                "but the BGAV denominational framework keeps this dimension "
                "at yellow rather than green."
            )
            sn["gender"] = (
                "Male lead pastor and male elder team at the Stafford campus. "
                "BGAV denominationally permits women pastors, which is what "
                "holds the gender dimension at yellow even though this "
                "specific campus is currently complementarian in practice."
            )
        rec["type"] = "Baptist (BGAV)"
        tags = set(rec.get("tags") or [])
        tags.discard("non-denominational")
        tags.update(["baptist", "bgav", "formerly-mt-ararat"])
        rec["tags"] = sorted(tags)
        log("the-mount-church-stafford", "scalar-fix",
            "founded 1907, services, YouTube, Sauer ECC creds, denom BGAV, score_notes leadership/denominational/gender")

    # === 3. Merge mt-ararat-baptist-stafford -> the-mount-church-stafford ===
    if "mt-ararat-baptist-stafford" in by_id and "the-mount-church-stafford" in by_id:
        canon = by_id["the-mount-church-stafford"]
        dup = by_id["mt-ararat-baptist-stafford"]
        # Merge audit fields
        canon_notes = canon.get("enrichment_notes") or ""
        dup_notes = dup.get("enrichment_notes") or ""
        if dup_notes and dup_notes not in canon_notes:
            canon["enrichment_notes"] = (canon_notes + "\n--- Merged from mt-ararat-baptist-stafford: " + dup_notes).strip()
        # Union sources
        c_srcs = canon.get("enrichment_sources") or []
        d_srcs = dup.get("enrichment_sources") or []
        seen = set()
        unioned = []
        for u in c_srcs + d_srcs:
            if u and u not in seen:
                seen.add(u)
                unioned.append(u)
        canon["enrichment_sources"] = unioned
        # Track merge metadata
        existing_merged = canon.get("merged_from") or []
        canon["merged_from"] = existing_merged + ["mt-ararat-baptist-stafford"]
        # Remove the dup from the directory
        churches[:] = [c for c in churches if c.get("id") != "mt-ararat-baptist-stafford"]
        log("the-mount-church-stafford", "merge",
            "absorbed mt-ararat-baptist-stafford (same 1112 Garrisonville Rd address)")

    # === 4. Merge brock-road-baptist-church -> chancellor-christian-church-spotsylvania ===
    # Refresh by_id since we removed a record
    by_id = {c["id"]: c for c in churches if "id" in c}
    if "brock-road-baptist-church" in by_id and "chancellor-christian-church-spotsylvania" in by_id:
        canon = by_id["chancellor-christian-church-spotsylvania"]
        dup = by_id["brock-road-baptist-church"]
        # Same logic as Mt. Ararat merge
        canon_notes = canon.get("enrichment_notes") or ""
        dup_notes = dup.get("enrichment_notes") or ""
        if dup_notes and dup_notes not in canon_notes:
            canon["enrichment_notes"] = (canon_notes + "\n--- Merged from brock-road-baptist-church: " + dup_notes).strip()
        c_srcs = canon.get("enrichment_sources") or []
        d_srcs = dup.get("enrichment_sources") or []
        seen = set()
        unioned = []
        for u in c_srcs + d_srcs:
            if u and u not in seen:
                seen.add(u)
                unioned.append(u)
        canon["enrichment_sources"] = unioned
        existing_merged = canon.get("merged_from") or []
        canon["merged_from"] = existing_merged + ["brock-road-baptist-church"]
        churches[:] = [c for c in churches if c.get("id") != "brock-road-baptist-church"]
        log("chancellor-christian-church-spotsylvania", "merge",
            "absorbed brock-road-baptist-church (same 11409 Brock Rd, same pastor Mark Dunn, same website)")

    # Refresh by_id again after second removal
    by_id = {c["id"]: c for c in churches if "id" in c}

    # === 5. Bedford Baptist + Bedford Road Baptist SBC -> BGAV ===
    for cid in ["bedford-baptist-church", "bedford-road-baptist-bedford"]:
        rec = by_id.get(cid)
        if rec and rec.get("denomination") == "SBC":
            rec["denomination"] = "Baptist (BGAV)"
            rec["denomination_family"] = "Baptist (BGAV)"
            rec["denomination_detail"] = (
                "Baptist General Association of Virginia (BGAV). BGAV "
                "publicly differentiated itself from the SBC in November "
                "2023 over women in pastoral roles. Prior enrichment notes "
                "documented BGAV-only affiliation but the denomination field "
                "was not propagated."
            )
            rec["enrichment_notes"] = (rec.get("enrichment_notes") or "") + (
                f"\n--- {TODAY} V4.9.6: denomination corrected SBC -> "
                "Baptist (BGAV). BGAV-only post-November 2023 places this "
                "congregation on the BGAV-not-SBC side of the November 2023 "
                "split over women in pastoral roles."
            )
            log(cid, "denom-fix", "SBC -> Baptist (BGAV)")

    # === 6. Garden City Roanoke pastor + green flip ===
    rec = by_id.get("garden-city-baptist-roanoke")
    if rec:
        if rec.get("pastor") == "Brian Willard":
            rec["pastor"] = "Charlie Lanier"
            rec["pastor_credentials"] = "Charlie Lanier — M.Div., Southeastern Baptist Theological Seminary (SEBTS), 2003."
            log("garden-city-baptist-roanoke", "pastor-fix", "Brian Willard -> Charlie Lanier (SEBTS M.Div. 2003)")
        if rec.get("overall_rating") == "yellow":
            rec["overall_rating"] = "green"
            rec["overall_label"] = "BFM2000 affirmation + SEBTS-trained pastor + all-male elders"
            sc = rec.get("scores") or {}
            for dim in ["christology", "scripture", "gender", "leadership", "soteriology", "preaching", "mission", "denominational"]:
                sc[dim] = "green"
            rec["scores"] = sc
            sn = rec.get("score_notes") or {}
            if isinstance(sn, dict):
                sn["denominational"] = "SBC + SBCV via BFM2000 affirmation; founded under Baptist Faith and Message framework."
                sn["leadership"] = "Charlie Lanier (SEBTS M.Div.) + plural-elder governance, all male."
                sn["preaching"] = "Expository tradition per SEBTS pipeline."
                sn["gender"] = "Male pastor; SBC complementarian framework."
            rec["enrichment_notes"] = (rec.get("enrichment_notes") or "") + (
                f"\n--- {TODAY} V4.9.6: yellow -> green. BFM2000 affirmation "
                "confirmed; pastor corrected to Charlie Lanier (SEBTS M.Div. "
                "2003); all-male elder team."
            )
            log("garden-city-baptist-roanoke", "rating-flip", "yellow -> green (BFM2000 + SEBTS + all-male)")

    # === 7. VA yellow -> GREEN flips from V4.9.3 ===
    green_flips = {
        "first-baptist-clintwood": {
            "label": "SBC/SBCV + BFM2000 + founded 1894",
            "notes": "BFM2000 affirmation; SBC/SBCV affiliation; founded 1894. Mountain Baptist congregation in coalfield region.",
            "key_notes": {
                "denominational": "SBC and SBCV aligned; founded 1894.",
                "scripture": "BFM2000 explicitly affirms biblical inerrancy.",
                "gender": "BFM2000 restricts the office of pastor to men.",
            },
        },
        "hillsville-baptist": {
            "label": "BFM 1963 + 1998 affirmations + SBC",
            "notes": "First Baptist Church of Hillsville (carmel-yellow→green): explicit BFM 1963 + 1998 affirmations on About page; SBC affiliation confirmed.",
            "key_notes": {
                "denominational": "SBC; explicit BFM 1963 and 1998 affirmations on About page.",
                "scripture": "BFM 1963/1998 affirms biblical inerrancy.",
            },
        },
        "hopeful-baptist-mechanicsville": {
            "label": "SBCV affiliation + male leadership; correct domain hopefulbc.com",
            "notes": "SBCV affiliation confirmed via external directory. NOTE: The correct domain is hopefulbc.com (the prior URL pointed to a Florida church). All-male staff.",
            "key_notes": {
                "denominational": "SBCV affiliation confirmed.",
                "leadership": "All-male staff confirmed; plural elder governance.",
            },
        },
        "christ-community-church-chesterfield": {
            "label": "Christian & Missionary Alliance (C&MA)",
            "notes": "Christian & Missionary Alliance (C&MA) — moderate-conservative evangelical network with complementarian denominational stance.",
            "key_notes": {
                "denominational": "Christian & Missionary Alliance (C&MA) — confessional evangelical network.",
            },
        },
        "harvest-bible-chapel-glen-allen": {
            "label": "Now Harvest Bible Church — plural-elder all-male",
            "notes": "Rebranded to Harvest Bible Church (harvestbiblechurch.org); pastor Jon Walters; plural-elder governance, all-male leadership.",
            "key_notes": {
                "leadership": "Plural-elder governance; Pastor Jon Walters; all-male elder team.",
                "denominational": "Independent Bible church (formerly Harvest Bible Fellowship).",
            },
        },
    }
    for cid, info in green_flips.items():
        rec = by_id.get(cid)
        if not rec:
            continue
        if rec.get("overall_rating") == "yellow":
            rec["overall_rating"] = "green"
            rec["overall_label"] = info["label"]
            sc = rec.get("scores") or {}
            for dim in ["christology", "scripture", "gender", "leadership", "soteriology", "preaching", "mission", "denominational"]:
                sc[dim] = "green"
            rec["scores"] = sc
            sn = rec.get("score_notes") or {}
            if isinstance(sn, dict):
                for k, v in info["key_notes"].items():
                    sn[k] = v
            rec["enrichment_notes"] = (rec.get("enrichment_notes") or "") + (
                f"\n--- {TODAY} V4.9.6: yellow -> green. {info['notes']}"
            )
            log(cid, "rating-flip", f"yellow -> green ({info['label']})")

    # === 8. VA yellow -> RED flips from V4.9.3 ===
    red_flips = {
        "buena-vista-baptist": {
            "label": "CBF + husband-wife pastoral team",
            "notes": "CBF (Cooperative Baptist Fellowship) affiliation + husband-wife pastoral team Scott Covington / Danika Deva. CBF egalitarian stance + husband-wife co-pastor model are MOOP red signals.",
            "key_notes": {
                "denominational": "CBF (Cooperative Baptist Fellowship) — progressive Baptist network.",
                "gender": "Husband-wife pastoral team (Scott Covington / Danika Deva) — egalitarian model.",
                "leadership": "Co-pastor structure with named female pastor — MOOP automatic red.",
            },
        },
        "arc-heights-church-richmond-va": {
            "label": "ARC affiliation + husband-wife co-pastors",
            "notes": "Association of Related Churches (ARC) affiliation + husband-wife co-pastors Josh & Crystal Whitlow. ARC is a MOOP automatic-red signal for charismatic/apostolic-covering network plus sermon-stealing controversies. Husband-wife co-pastor structure compounds.",
            "key_notes": {
                "denominational": "Association of Related Churches (ARC) — MOOP automatic-red signal (charismatic/apostolic-covering network).",
                "gender": "Husband-wife co-pastors Josh & Crystal Whitlow; named female pastor.",
                "leadership": "Co-pastor structure with named female pastor — MOOP automatic red.",
            },
        },
        "first-baptist-lebanon": {
            "label": "BGAV-only post-Nov 2023 (not SBC)",
            "notes": "Lebanon Baptist Church (Lebanon VA): BGAV affiliation confirmed via BGAV directory. BGAV publicly differentiated itself from the SBC in November 2023 over women in pastoral roles, placing BGAV-only churches in the red category per the post-split MOOP rubric.",
            "key_notes": {
                "denominational": "BGAV-only post-November 2023; BGAV split from SBC over women in pastoral roles.",
                "gender": "BGAV denominationally permits women pastors.",
            },
        },
    }
    for cid, info in red_flips.items():
        rec = by_id.get(cid)
        if not rec:
            continue
        if rec.get("overall_rating") == "yellow":
            rec["overall_rating"] = "red"
            rec["overall_label"] = info["label"]
            sc = rec.get("scores") or {}
            for dim in ["gender", "leadership", "denominational"]:
                sc[dim] = "red"
            rec["scores"] = sc
            sn = rec.get("score_notes") or {}
            if isinstance(sn, dict):
                for k, v in info["key_notes"].items():
                    sn[k] = v
            rec["enrichment_notes"] = (rec.get("enrichment_notes") or "") + (
                f"\n--- {TODAY} V4.9.6: yellow -> red. {info['notes']}"
            )
            log(cid, "rating-flip", f"yellow -> red ({info['label']})")

    # === 9. Upgrade 2 existing confessional VA records yellow -> green ===
    confessional_upgrades = {
        "grace-covenant-presbyterian-church-blacksburg-va": {
            "label": "PCA — confessional Reformed, 12 named pastors+elders all male",
            "notes": "PCA congregation in Blacksburg; verified all-male elder/pastor roster (12 named); confessional Westminster Standards.",
        },
        "providence-presbyterian-church-pca-christiansburg-va": {
            "label": "PCA — confessional Reformed (NRV)",
            "notes": "PCA congregation in Christiansburg (New River Valley); Westminster Standards; all-male elders.",
        },
    }
    for cid, info in confessional_upgrades.items():
        rec = by_id.get(cid)
        if not rec:
            continue
        cur = rec.get("overall_rating")
        if cur == "yellow":
            rec["overall_rating"] = "green"
            rec["overall_label"] = info["label"]
            sc = rec.get("scores") or {}
            for dim in ["christology", "scripture", "gender", "leadership", "soteriology", "preaching", "denominational"]:
                sc[dim] = "green"
            rec["scores"] = sc
            rec["enrichment_notes"] = (rec.get("enrichment_notes") or "") + (
                f"\n--- {TODAY} V4.9.6 upgrade: {info['notes']}"
            )
            log(cid, "rating-flip", f"yellow -> green ({info['label']})")

    # === 10. Re-add 23 missing V4.9.4 confessional VA records ===
    # Records that match by name on origin and are skipped here:
    skip_ids = {
        "pca-grace-covenant-blacksburg-va",      # upgraded above
        "pca-providence-christiansburg-va",      # upgraded above
        "opc-peninsula-reformed-yorktown-va",    # already green on origin under different ID
        "arp-wellspring-daleville-va",           # already green-equivalent (7.9) on origin
    }
    added = 0
    for backup_rec in backup_green_hunter:
        bid = backup_rec["id"]
        if bid in skip_ids:
            continue
        if bid in by_id:
            continue  # Already on origin under same ID
        # Add audit marker
        backup_rec.setdefault("enrichment_notes", "")
        backup_rec["enrichment_notes"] = backup_rec["enrichment_notes"] + (
            f"\n--- {TODAY} V4.9.6: re-added from V4.9.4 green-hunter backup "
            "(record was lost in the parallel-session rebase chain)."
        )
        churches.append(backup_rec)
        log(bid, "add", f"new VA confessional record ({backup_rec.get('denomination','')[:30]})")
        added += 1

    # === Write ===
    data["churches"] = churches
    data["total_churches"] = len(churches)
    CHURCHES.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    # Report
    print(f"V4.9.6 reconciliation: {len(changes)} record actions")
    print(f"Directory: {len(churches)} records (was 13948)")
    print()
    by_action = {}
    for cid, action, detail in changes:
        by_action.setdefault(action, []).append((cid, detail))
    for action, items in by_action.items():
        print(f"--- {action} ({len(items)}) ---")
        for cid, detail in items:
            print(f"  {cid:55} {detail[:80]}")
        print()


if __name__ == "__main__":
    main()
