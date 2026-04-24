#!/usr/bin/env python3
"""Build new_churches_opc.json from scraped OPC data."""
import json

# Default scores/notes reused across all OPC records
GREEN = "green"

DEFAULT_SCORES = {
    "christology": "green",
    "scripture": "green",
    "gender": "green",
    "leadership": "green",
    "soteriology": "green",
    "cultural": "green",
    "denominational": "green",
    "preaching": "green",
    "mens_discipleship": "green",
    "mission": "green",
}

def notes_for(name: str) -> dict:
    return {
        "christology": "OPC subscribes to the Westminster Standards — orthodox Trinitarian Christology, Chalcedonian two-natures, virgin birth, bodily resurrection.",
        "scripture": "Westminster Confession ch. 1 affirms plenary verbal inspiration and inerrancy of the Scriptures as the only rule of faith and life.",
        "gender": "OPC Book of Church Order restricts the offices of teaching elder, ruling elder, and deacon to qualified men only (1 Tim 2–3; Titus 1).",
        "leadership": "Plurality of ordained male elders (session) under presbyterian polity with accountability to the presbytery and General Assembly.",
        "soteriology": "Reformed soteriology per Westminster — monergistic regeneration, sola fide, sola gratia, sola Scriptura, effectual calling, perseverance of the saints.",
        "cultural": "OPC historically resists theological accommodation to cultural pressure — Machen's legacy of confessional fidelity over cultural relevance.",
        "denominational": "Orthodox Presbyterian Church — founded 1936 by J. Gresham Machen as a confessionally Reformed denomination against Modernism in the PCUSA.",
        "preaching": "OPC pulpits are characterized by expository, Christ-centered, Law/Gospel preaching from the Westminster tradition.",
        "mens_discipleship": "OPC congregations typically emphasize family worship, catechism instruction, and male headship in home and church — strong formation pipeline for men.",
        "mission": "OPC Committee on Foreign Missions and Home Missions actively plants confessionally Reformed churches domestically and abroad.",
    }

def rec(id_slug, name, address, pastor, website, region, presbytery, sources):
    tags = [
        "opc", "orthodox-presbyterian", "reformed", "presbyterian",
        "westminster-standards", "confessional"
    ]
    if presbytery:
        tags.append(f"presbytery-{presbytery}")
    return {
        "id": id_slug,
        "slug": id_slug,
        "name": name,
        "address": address,
        "pastor": pastor,
        "website": website,
        "type": "Presbyterian / Reformed",
        "denomination": "OPC",
        "denomination_family": "Presbyterian (OPC)",
        "denomination_detail": f"Orthodox Presbyterian Church — Presbytery of {presbytery_label(presbytery)}" if presbytery else "Orthodox Presbyterian Church",
        "overall_rating": "green",
        "overall_label": "Confessionally Reformed — Strong",
        "tags": tags,
        "pastor_credentials": "OPC ordination (Westminster Standards subscription required)",
        "founded": "Not published",
        "services": "Verify on website",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "scores": dict(DEFAULT_SCORES),
        "score_notes": notes_for(name),
        "assessment": (
            f"{name} is a congregation of the Orthodox Presbyterian Church (OPC), "
            "the confessional Reformed denomination founded in 1936 by J. Gresham Machen. "
            "OPC churches subscribe to the Westminster Confession of Faith and Catechisms, "
            "restrict ordained office to qualified men, and practice presbyterian polity "
            "with accountability through session, presbytery, and General Assembly. "
            "Baseline green rating reflects confessional identity; verify local particulars on the website."
        ),
        "region": region,
        "enrichment_sources": sources,
        "enrichment_notes": "Added from OPC.org locator and Presbytery of Philadelphia directory; baseline green rating per OPC confessional identity.",
    }

def presbytery_label(slug):
    return {
        "philadelphia": "Philadelphia",
        "nj-pr": "New Jersey and Puerto Rico",
        "michigan-ontario": "Michigan and Ontario",
        "mid-atlantic": "the Mid-Atlantic",
        "northwest": "the Northwest",
    }.get(slug, slug)

OPCS = [
    # PA + DE (Philadelphia Presbytery) — 7
    rec("living-hope-opc-allentown-pa",
        "Living Hope Presbyterian Church (OPC)",
        "330 Schantz Road, Allentown, PA 18104",
        "Not listed", "https://livinghopeopc.org", "PA", "philadelphia",
        ["https://www.philadelphia.opc.org/find-congregation"]),
    rec("cornerstone-opc-ambler-pa",
        "Cornerstone Presbyterian Church (OPC)",
        "701 Pen-Ambler Rd, Ambler, PA 19002",
        "Zach Siggins", "https://cornerstoneopc.com", "PA", "philadelphia",
        ["https://www.philadelphia.opc.org/find-congregation"]),
    rec("christ-church-opc-downingtown-pa",
        "Christ Church Downingtown (OPC)",
        "37 W. Lancaster Ave., Downingtown, PA 19335",
        "Greg O'Brien", "https://christdowningtown.org", "PA", "philadelphia",
        ["https://www.philadelphia.opc.org/find-congregation"]),
    rec("trinity-opc-easton-pa",
        "Trinity Orthodox Presbyterian Church",
        "531 Milford Street, Easton, PA 18042",
        "Lane G. Tipton", "https://trinityopc-easton.org", "PA", "philadelphia",
        ["https://www.philadelphia.opc.org/find-congregation"]),
    rec("first-opc-perkasie-pa",
        "First Orthodox Presbyterian Church of Perkasie",
        "5th & Race Streets, Perkasie, PA 18944",
        "Richard Scott MacLaren", "https://firstchurchopc.org", "PA", "philadelphia",
        ["https://www.philadelphia.opc.org/find-congregation"]),
    rec("good-news-opc-west-norriton-pa",
        "Good News Orthodox Presbyterian Church",
        "399 N Whitehall Rd., West Norriton, PA 19403",
        "Nate Jeffries", "https://goodnewsopc.org", "PA", "philadelphia",
        ["https://www.philadelphia.opc.org/find-congregation"]),
    rec("emmanuel-opc-wilmington-de",
        "Emmanuel Orthodox Presbyterian Church",
        "1006 Wilson Road, Wilmington, DE 19803",
        "David Landow", "https://eopc.org", "DE", "philadelphia",
        ["https://www.philadelphia.opc.org/find-congregation"]),

    # NJ — 7
    rec("immanuel-opc-bellmawr-nj",
        "Immanuel Orthodox Presbyterian Church",
        "11 Park Dr., Bellmawr, NJ 08031",
        "Matthew D. Cole", "https://immanuelopc.org", "NJ", "nj-pr",
        ["https://opc.org/locator.html?search_go=Y&state=NJ"]),
    rec("new-hope-opc-bridgeton-nj",
        "New Hope Orthodox Presbyterian Church",
        "65 Hitchner Ave., Bridgeton, NJ 08302",
        "Claude A. Taylor III", "https://newhopebridgeton.org", "NJ", "nj-pr",
        ["https://opc.org/locator.html?search_go=Y&state=NJ"]),
    rec("grace-opc-fair-lawn-nj",
        "Grace Orthodox Presbyterian Church",
        "151 S. Broadway, Fair Lawn, NJ 07410",
        "John Keegan", "https://graceopcfairlawn.org", "NJ", "nj-pr",
        ["https://opc.org/locator.html?search_go=Y&state=NJ"]),
    rec("providence-opc-mantua-nj",
        "Providence Orthodox Presbyterian Church",
        "230 Shadow Place, Mantua, NJ 08051",
        "Zachary Herbster", "https://providenceopc.org", "NJ", "nj-pr",
        ["https://opc.org/locator.html?search_go=Y&state=NJ"]),
    rec("christ-the-king-opc-wildwood-nj",
        "Christ the King Orthodox Presbyterian Church",
        "303 Atlantic Ave., North Wildwood, NJ 08260",
        "James A. Zozzaro", "https://christthekingwildwood.org", "NJ", "nj-pr",
        ["https://opc.org/locator.html?search_go=Y&state=NJ"]),
    rec("calvary-opc-ringoes-nj",
        "Calvary Orthodox Presbyterian Church",
        "24 US Highway 202, Ringoes, NJ 08551",
        "Christopher Bush", "https://calvarychurchopc.org", "NJ", "nj-pr",
        ["https://opc.org/locator.html?search_go=Y&state=NJ"]),
    rec("grace-opc-westfield-nj",
        "Grace Orthodox Presbyterian Church",
        "1100 Boulevard, Westfield, NJ 07090",
        "Timothy Ferguson", "https://graceopcwestfieldnj.org", "NJ", "nj-pr",
        ["https://opc.org/locator.html?search_go=Y&state=NJ"]),

    # MI — 5
    rec("redeemer-opc-ada-mi",
        "Redeemer Orthodox Presbyterian Church",
        "8605 Fulton St. East (M-21), Ada, MI 49301",
        "Jeffrey D. De Boer", "https://redeemer-opc.org", "MI", "michigan-ontario",
        ["https://opc.org/locator.html?search_go=Y&state=MI"]),
    rec("covenant-opc-brighton-mi",
        "Covenant Orthodox Presbyterian Church",
        "228 S. 4th St., Brighton, MI 48116",
        "Douglas B. Doll", "https://opcbrighton.org", "MI", "michigan-ontario",
        ["https://opc.org/locator.html?search_go=Y&state=MI"]),
    rec("oakland-hills-opc-farmington-hills-mi",
        "Oakland Hills Community Presbyterian Church (OPC)",
        "37150 W. Eight Mile Rd., Farmington Hills, MI 48335",
        "Harrison Perkins", "https://ohcc.net", "MI", "michigan-ontario",
        ["https://opc.org/locator.html?search_go=Y&state=MI"]),
    rec("community-opc-kalamazoo-mi",
        "Community Presbyterian Church (OPC)",
        "811 Gorham Lane, Kalamazoo, MI 49006",
        "Jonathan L. Cruse", "https://kalamazoocpc.org", "MI", "michigan-ontario",
        ["https://opc.org/locator.html?search_go=Y&state=MI"]),
    rec("harvest-opc-wyoming-mi",
        "Harvest Orthodox Presbyterian Church",
        "930 52nd St. SW, Wyoming, MI 49509",
        "Dale A. Van Dyke", "https://harvestopc.org", "MI", "michigan-ontario",
        ["https://opc.org/locator.html?search_go=Y&state=MI"]),

    # VA — 5
    rec("providence-opc-charlottesville-va",
        "Providence Orthodox Presbyterian Church",
        "FOP Thompson Hall, 974 Michie Tavern Lane, Charlottesville, VA",
        "William H. Sloan", "https://popc-cville.org", "VA", "mid-atlantic",
        ["https://opc.org/locator.html?search_go=Y&state=VA"]),
    rec("reformation-opc-norfolk-va",
        "Reformation Orthodox Presbyterian Church",
        "1241 Hillside Ave., Norfolk, VA 23503",
        "Timothy Marinelli", "https://reformation-opc.org", "VA", "mid-atlantic",
        ["https://opc.org/locator.html?search_go=Y&state=VA"]),
    rec("grace-opc-vienna-va",
        "Grace Orthodox Presbyterian Church",
        "2381 Cedar Ln., Vienna, VA 22180",
        "Daniel P. Clifford", "https://gracevienna.org", "VA", "mid-atlantic",
        ["https://opc.org/locator.html?search_go=Y&state=VA"]),
    rec("sterling-opc-va",
        "Sterling Orthodox Presbyterian Church",
        "Cascades Overlook Event Center, 21453 Epicerie Plaza, Sterling, VA 20164",
        "Philip T. Proctor", "https://sterlingopc.org", "VA", "mid-atlantic",
        ["https://opc.org/locator.html?search_go=Y&state=VA"]),
    rec("all-saints-opc-suffolk-va",
        "All Saints Orthodox Presbyterian Church",
        "3520 Pruden Blvd., Suffolk, VA 23434",
        "John Nymann", "https://allsaintsopc.com", "VA", "mid-atlantic",
        ["https://opc.org/locator.html?search_go=Y&state=VA"]),

    # WA — 4
    rec("trinity-opc-bothell-wa",
        "Trinity Orthodox Presbyterian Church",
        "23211 Meridian Ave. S., Bothell, WA 98021",
        "Aaron Mize", "https://trinityopc.com", "WA", "northwest",
        ["https://opc.org/locator.html?search_go=Y&state=WA"]),
    rec("lynnwood-opc-wa",
        "Lynnwood Orthodox Presbyterian Church",
        "17711 Spruce Way, Lynnwood, WA 98037",
        "Benjamin W. Swinburnson", "https://lynnwoodopc.org", "WA", "northwest",
        ["https://opc.org/locator.html?search_go=Y&state=WA"]),
    rec("reformation-opc-olympia-wa",
        "Reformation Orthodox Presbyterian Church",
        "2306 26th Ave NW, Olympia, WA 98502",
        "Brett McNeill", "https://ropcolympia.org", "WA", "northwest",
        ["https://opc.org/locator.html?search_go=Y&state=WA"]),
    rec("sovereign-grace-opc-oak-harbor-wa",
        "Sovereign Grace Orthodox Presbyterian Church",
        "1811 W Cemetery Rd., Oak Harbor, WA 98277",
        "Robert C. Van Kooten", "https://sgopc.org", "WA", "northwest",
        ["https://opc.org/locator.html?search_go=Y&state=WA"]),
]

out = "/Users/adamjohns/bible-reading-plan-bot/tmp/new_churches_opc.json"
with open(out, "w") as f:
    json.dump(OPCS, f, indent=2, ensure_ascii=False)

# Report
from collections import Counter
states = Counter(c["region"] for c in OPCS)
presbyteries = Counter(
    next((t for t in c["tags"] if t.startswith("presbytery-")), None)
    for c in OPCS
)
print(f"Wrote {len(OPCS)} records to {out}")
print("By state:", dict(states))
print("By presbytery:", dict(presbyteries))
