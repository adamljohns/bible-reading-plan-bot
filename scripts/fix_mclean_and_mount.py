#!/usr/bin/env python3
"""
Apply corrections to:
  1. mclean-bible-church-vienna  — Platt stepped back from senior role; clean stale citations
  2. the-mount-church            — Fxbg campus: founded, services, youtube, scrub internal-review language
  3. the-mount-church-stafford   — Stafford campus: founded, youtube, Sauer credentials, elder governance, BGAV
  4. mt-ararat-baptist-stafford  — legacy duplicate: fix SBC mis-tag to BGAV; flag for V5.0 dedup merge
"""
import json
from pathlib import Path

CHURCHES_PATH = Path("/Users/adamjohns/bible-reading-plan-bot/docs/data/churches.json")

with CHURCHES_PATH.open() as f:
    data = json.load(f)
churches = data if isinstance(data, list) else data.get("churches", data)

by_id = {c["id"]: c for c in churches if "id" in c}

# ---------- 1. McLean Bible Vienna ----------
mclean = by_id["mclean-bible-church-vienna"]
mclean["pastor"] = "Dale Sutherland (Lead Pastor)"
mclean["pastor_credentials"] = (
    "Dale Sutherland: served alongside David Platt at McLean before stepping into the "
    "Lead Pastor role; expository-ministry trained."
)
mclean["score_notes"]["leadership"] = (
    "Confirmed plural-elder governance: Dale Sutherland (Lead Pastor) and Mike Kelsey "
    "(Lead Pastor for Preaching & Vision) lead the pastoral team. David Platt stepped "
    "back from the senior pastor role in late 2023 to focus full-time on Radical, his "
    "global-missions ministry; he retains a teaching/preaching presence but is no longer "
    "the day-to-day senior pastor. Elder team includes Jim Burris, Ken Tucker, Hooman "
    "Gharai, Sasha Varghese, Patrick Lee, and Derek Karchner — all male."
)
mclean["score_notes"]["preaching"] = (
    "Mike Kelsey carries the primary preaching load with Dale Sutherland; expository "
    "tradition continues from the Platt era. Verify current rotation post-Platt transition."
)
mclean["assessment"] = (
    "McLean Bible Church is one of the most significant evangelical churches in the DC "
    "metro area. David Platt's tenure (2017–2023) brought strong expository preaching, "
    "Calvinist theology, and Great Commission urgency. Platt stepped back from the senior "
    "pastor role in late 2023 to focus full-time on Radical (his global-missions ministry) "
    "and retains a teaching presence but is no longer the day-to-day senior pastor. Dale "
    "Sutherland now serves as Lead Pastor with Mike Kelsey carrying significant preaching "
    "and vision responsibility. The church sits in Vienna, VA — deep in progressive "
    "Northern Virginia — making it a critical outpost of biblical Christianity. Elder-led, "
    "complementarian on paper, strong missions DNA. Key open question: does the post-Platt "
    "leadership hold the doctrinal line under cultural pressure? Current public posture "
    "(elder plurality, evangelical statement of faith, expository preaching) supports a "
    "green rating, but warrants ongoing observation."
)
mclean["gender_detail"] = (
    "Complementarian in stated position — male elders only; post-Platt continuity under "
    "Sutherland and Kelsey verified through 2024 elder roster."
)
# Keep tags but also add a transition marker
if "post-platt-transition" not in mclean.get("tags", []):
    mclean.setdefault("tags", []).append("post-platt-transition")

# ---------- 2. The Mount Church (Fredericksburg Campus) ----------
mount_fxbg = by_id["the-mount-church"]
mount_fxbg["founded"] = "1907 (founded as Mount Ararat Baptist Church)"
mount_fxbg["services"] = "Sundays 9:15 AM & 10:45 AM"
mount_fxbg["youtube"] = "https://www.youtube.com/@themountva"
# Clean the score_notes.denominational of internal-review language
mount_fxbg["score_notes"]["denominational"] = (
    "Multi-site BGAV congregation (formerly Mount Ararat Baptist Church, est. 1907). "
    "BGAV publicly differentiated itself from the Southern Baptist Convention in November "
    "2023 over women in pastoral roles, and the BGAV framework permits women pastors. The "
    "Fredericksburg campus's own pastoral team is currently male, but the denominational "
    "framework and multi-site streaming model (sermon delivered via video from Stafford) "
    "keep this campus on the cautious side of yellow at the denominational dimension."
)
# Tighten gender note
mount_fxbg["score_notes"]["gender"] = (
    "BGAV denominationally permits women pastors; the Fredericksburg campus pastor is "
    "Andrew Brothers (male) and the local elder team is male. The red call here is driven "
    "by denominational framework, not by any specific local female pastor on this campus."
)
# Update pastor_credentials light cleanup
mount_fxbg["pastor_credentials"] = (
    "Andrew Brothers — B.A. in Missions, Trinity Baptist College (Jacksonville, FL); "
    "former missionary in Poland (2.5 years)."
)
# Denomination_detail clean
mount_fxbg["denomination_detail"] = (
    "Baptist General Association of Virginia (BGAV). BGAV publicly differentiated itself "
    "from the SBC in November 2023 over women in pastoral roles."
)
# Drop "fetch" / "rendered" / "held" jargon from any remaining notes if present
for k, v in list(mount_fxbg.get("score_notes", {}).items()):
    if isinstance(v, str) and ("rendered on this specific campus fetch" in v or "Red CONFIRMED at denominational level — held" in v):
        # already replaced above for "denominational"; for safety re-clean any other key
        cleaned = v.replace("rendered on this specific campus fetch", "visible on this campus page")
        cleaned = cleaned.replace("Red CONFIRMED at denominational level — held", "denominational concern stands")
        mount_fxbg["score_notes"][k] = cleaned

# ---------- 3. The Mount Church (Stafford Campus) ----------
mount_staf = by_id["the-mount-church-stafford"]
mount_staf["founded"] = "1907 (founded as Mount Ararat Baptist Church)"
mount_staf["services"] = "Sundays 8:30 AM, 10:00 AM, 11:30 AM"
mount_staf["youtube"] = "https://www.youtube.com/@themountva"
mount_staf["pastor"] = "Adam Sauer (Lead Pastor, since 2022)"
mount_staf["pastor_credentials"] = (
    "Adam Sauer — M.Div. and M.A. in Nonprofit Management, North Park Theological "
    "Seminary (Evangelical Covenant Church-affiliated, Chicago). Note: ECC seminary "
    "pipeline is unusual for a historic Baptist congregation — verify ongoing doctrinal "
    "alignment with Baptist distinctives."
)
mount_staf["denomination"] = "Baptist (BGAV)"
mount_staf["denomination_family"] = "Baptist (BGAV)"
mount_staf["denomination_detail"] = (
    "Baptist General Association of Virginia (BGAV). The congregation traces back to 1907 "
    "as Mount Ararat Baptist Church and rebranded as The Mount Church across five campuses. "
    "BGAV publicly differentiated itself from the SBC in November 2023 over women in "
    "pastoral roles."
)
mount_staf["score_notes"]["leadership"] = (
    "Plurality of elected elders per the qualifications in 1 Timothy 3:1–7 and Titus 1:5–9. "
    "Lead Pastor Adam Sauer (since 2022) preaches the primary teaching slot, which is "
    "streamed to the Fredericksburg, Bealeton, and El Monte campuses."
)
mount_staf["score_notes"]["denominational"] = (
    "BGAV-affiliated. BGAV permits women pastors and broke publicly with the SBC in November "
    "2023 over that question. The Stafford campus's own pastoral team is currently male, but "
    "the BGAV denominational framework keeps this dimension at yellow rather than green."
)
mount_staf["score_notes"]["gender"] = (
    "Male lead pastor and male elder team at the Stafford campus. BGAV denominationally "
    "permits women pastors, which is what holds the gender dimension at yellow even though "
    "this specific campus is currently complementarian in practice."
)
mount_staf["score_notes"]["preaching"] = (
    "Adam Sauer preaches the primary teaching slot from Stafford; sermons are biblically "
    "grounded but lean topical / application-driven rather than verse-by-verse expository."
)
mount_staf["score_notes"]["denominational"] = mount_staf["score_notes"]["denominational"]  # already set
# Update assessment
mount_staf["assessment"] = (
    "The Mount Church (Stafford Campus) is the flagship of the multi-site network formerly "
    "known as Mount Ararat Baptist Church (founded 1907). Adam Sauer leads, having stepped "
    "into the Lead Pastor role in 2022; his M.Div. comes from North Park Theological "
    "Seminary, which is Evangelical Covenant Church-affiliated rather than Baptist — an "
    "unusual pipeline for a historic Baptist congregation. The church is BGAV-affiliated; "
    "BGAV permits women pastors and publicly distanced itself from the SBC in November 2023 "
    "over that issue. Plural-elder governance per 1 Timothy 3 and Titus 1 is in place at the "
    "Stafford campus, the pastoral team is currently male, and the statement of faith "
    "affirms biblical inerrancy. Modern, casual, high-energy worship culture; strong "
    "volunteer network and programs (Dave Ramsey FPU, preschool, young adults). Worth a "
    "visit — go in knowing this is moderate Baptist territory under BGAV, not SBC."
)
mount_staf["type"] = "Baptist (BGAV)"
# Tags
mount_staf_tags = set(mount_staf.get("tags", []))
mount_staf_tags.discard("non-denominational")
mount_staf_tags.add("baptist")
mount_staf_tags.add("bgav")
mount_staf_tags.add("formerly-mt-ararat")
mount_staf["tags"] = sorted(mount_staf_tags)

# ---------- 4. mt-ararat-baptist-stafford (legacy duplicate) ----------
mt_ararat = by_id["mt-ararat-baptist-stafford"]
mt_ararat["denomination"] = "Baptist (BGAV)"
mt_ararat["denomination_family"] = "Baptist (BGAV)"
mt_ararat["type"] = "Baptist (BGAV)"
mt_ararat["denomination_detail"] = (
    "Baptist General Association of Virginia (BGAV). NOT Southern Baptist Convention — "
    "earlier directory entry mis-tagged this congregation as SBC. The Mount Church across "
    "five locations operates under BGAV affiliation, and BGAV broke publicly with the SBC "
    "in November 2023 over women in pastoral roles."
)
mt_ararat["score_notes"]["denominational"] = (
    "BGAV-affiliated (not SBC, despite earlier mis-tag). The Mount Church operates five "
    "campuses (Stafford, Fredericksburg, Bealeton, El Monte, Online) under BGAV."
)
mt_ararat.setdefault("review_flag", []).append(
    "DUPLICATE: this is the legacy 'Mt. Ararat Baptist' record for the Stafford campus at "
    "1112 Garrisonville Rd — same address as the-mount-church-stafford. Merge in next dedup "
    "pass; the-mount-church-stafford is the canonical record."
)
# Tags
mt_ararat_tags = set(mt_ararat.get("tags", []))
mt_ararat_tags.discard("sbc")
mt_ararat_tags.add("baptist")
mt_ararat_tags.add("bgav")
mt_ararat_tags.add("legacy-record")
mt_ararat_tags.add("duplicate-of-the-mount-church-stafford")
mt_ararat["tags"] = sorted(mt_ararat_tags)

# ---------- write back ----------
with CHURCHES_PATH.open("w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Updated:")
print("  mclean-bible-church-vienna       — Platt stepped back; pastor/leadership/preaching/assessment refreshed")
print("  the-mount-church                 — Fxbg: founded/services/youtube/clean denom note")
print("  the-mount-church-stafford        — Stafford: founded/services/youtube/Sauer creds/elder gov/BGAV")
print("  mt-ararat-baptist-stafford       — legacy: SBC mis-tag → BGAV; flagged duplicate")
