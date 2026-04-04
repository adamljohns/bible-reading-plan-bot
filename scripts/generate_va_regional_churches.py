#!/usr/bin/env python3
"""
Generate Virginia regional church HTML pages (Lynchburg, Shenandoah Valley, Peninsula).
Run from repo root: python3 scripts/generate_va_regional_churches.py
"""

import json, os, re, html as html_mod
from datetime import date

CHURCHES = [
    # ─────────────────────────────────────────────────
    # LYNCHBURG AREA (5)
    # ─────────────────────────────────────────────────
    {
        "id": "thomas-road-baptist-lynchburg",
        "name": "Thomas Road Baptist Church",
        "address": "1 Mountain View Rd, Lynchburg, VA 24502",
        "pastor": "Rev. Jonathan Falwell (Senior Pastor)",
        "pastor_credentials": "Son of TRBC founder Jerry Falwell Sr.; succeeded his father in 2007; Th.B. Liberty University; long-tenured pastoral ministry in Lynchburg; affiliated with SBC of Virginia",
        "founded": "1956",
        "type": "Southern Baptist",
        "denomination": "Southern Baptist Convention (SBC)",
        "website": "https://trbc.org",
        "services": "Sundays at 9:00 AM & 11:00 AM (multiple services + online); Wednesday midweek services",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Cautious Commendation — Megachurch Dynamics, SBC Accountability",
        "region": "lynchburg",
        "scores": {
            "christology": "green",
            "scripture": "green",
            "gender": "green",
            "leadership": "yellow",
            "soteriology": "green",
            "cultural": "yellow",
            "denomination": "green",
            "preaching": "yellow",
            "mens": "green",
            "mission": "green"
        },
        "score_notes": {
            "leadership": "Jonathan Falwell leads a massive congregation (24,200 members, ~9,000 weekly) — megachurch scale raises questions about pastoral accessibility and accountability depth. The Falwell family brand carries baggage from Jerry Falwell Jr.'s highly publicized 2020 scandal (as Liberty University president). TRBC and Jonathan Falwell are distinct from LU's leadership crisis, but the association is unavoidable.",
            "cultural": "TRBC operates at the intersection of evangelical Christianity and political culture (Moral Majority legacy). This creates both platform opportunity and ongoing pressure to conflate political conservatism with the gospel. Watch for political identity crowding out Scripture-centricity.",
            "preaching": "Jonathan Falwell is a capable communicator, but megachurch style tends toward accessible, motivational preaching rather than verse-by-verse exposition. TRBC has a broadcast ministry tradition (Old Time Gospel Hour) that shaped its communication culture.",
            "denomination": "SBC — Baptist Faith & Message 2000 complementarian accountability. Strong denominational structure."
        },
        "assessment": "Thomas Road Baptist Church is one of the most historically significant evangelical churches in America, founded in 1956 by Jerry Falwell Sr. with 35 members and growing to over 24,000 members. Jonathan Falwell has led since his father's death in 2007, maintaining SBC affiliation and complementarian doctrine. TRBC has a rich legacy of bold public Christianity and global missions. The concerns are real: megachurch scale (9,000+ weekly) makes genuine discipleship harder; the Falwell family name carries significant cultural baggage following Jerry Falwell Jr.'s 2020 resignation from Liberty University amid scandal (though TRBC and LU are distinct); and the political-evangelical fusion of the Moral Majority era still shapes the church's culture. For a man wanting SBC accountability with strong outreach and missions emphasis in Lynchburg, TRBC is a viable option — but go in with eyes open about megachurch limitations.",
        "tags": ["sbc", "megachurch", "lynchburg", "jonathan-falwell", "jerry-falwell", "liberty-university", "southern-baptist"],
        "gender_detail": "Male-only pastors and elders (SBC BF&M 2000); complementarian in doctrine and governance",
        "denomination_detail": "Southern Baptist Convention — SBC of Virginia; Baptist Faith & Message 2000 complementarian accountability",
        "engagement": {
            "visited_facility": False,
            "attended_services": False,
            "viewed_online_services": False,
            "researched_website": False,
            "know_members_personally": False,
            "interacted_with_leadership": False,
            "attended_personally": False
        }
    },
    {
        "id": "heritage-baptist-lynchburg",
        "name": "Heritage Baptist Church",
        "address": "219 Breezewood Dr, Lynchburg, VA 24502",
        "pastor": "Pastor Nathan Smith",
        "pastor_credentials": "Pastor Nathan Smith leads with co-pastor Mike Crump; independent Baptist tradition; KJV-aligned congregation",
        "founded": "Est. (long-standing independent Baptist congregation in Lynchburg)",
        "type": "Independent Fundamental Baptist",
        "denomination": "Independent Baptist (KJV-aligned)",
        "website": "https://hbclynchburg.com",
        "services": "Sundays at 9:30 AM & 11:00 AM; additional midweek services",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — Independent Baptist, KJV-Only Leanings, Verify Doctrinal Specifics",
        "region": "lynchburg",
        "scores": {
            "christology": "green",
            "scripture": "green",
            "gender": "green",
            "leadership": "yellow",
            "soteriology": "green",
            "cultural": "green",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "Independent Baptist — no external denominational accountability. Operates on congregational authority only. KJV-alignment noted from church directory listings. IFB tradition can vary widely from healthy expository local church to legalistic separatist culture.",
            "leadership": "Two-pastor structure (Nathan Smith + Mike Crump) is unusual — verify elder/deacon board structure and accountability framework. Independent congregation means all governance is internal.",
            "preaching": "Independent Baptist tradition is typically expository and Word-heavy, but preaching quality varies enormously. Verify content and style with personal visit.",
            "cultural": "HBC describes itself as 'church of broken people, blessed in Christ, to be a blessing to the world' — encouraging gospel-centered language. Church motto focused on disciplemaking is positive.",
            "mens": "Men's ministry needs verification — independent Baptist churches vary widely in structured men's discipleship infrastructure."
        },
        "assessment": "Heritage Baptist Church is an independent Baptist congregation in Lynchburg led by Pastor Nathan Smith and co-pastor Mike Crump. The church describes itself as 'a church family of broken people under God's grace who make disciples of Jesus Christ' — language that signals gospel-centeredness. Independent Baptist churches can be excellent, gospel-preaching local churches, but they require more personal evaluation since there is no external denominational accountability or confessional standard to default to. The KJV-alignment noted in church directories should be clarified — it can indicate a healthy traditionalism or a KJV-only secondary separation stance. Visit personally, evaluate the preaching content, and ask directly about their confession of faith, elder structure, and discipleship philosophy before committing.",
        "tags": ["independent-baptist", "lynchburg", "kjv-aligned", "complementarian", "local-church", "nathan-smith"],
        "gender_detail": "Male pastors (Nathan Smith, Mike Crump); independent Baptist tradition is complementarian; male-only pastoral leadership",
        "denomination_detail": "Independent Baptist — no denominational accountability; KJV-aligned; governance is entirely congregational",
        "engagement": {
            "visited_facility": False,
            "attended_services": False,
            "viewed_online_services": False,
            "researched_website": False,
            "know_members_personally": False,
            "interacted_with_leadership": False,
            "attended_personally": False
        }
    },
    {
        "id": "rivermont-evangelical-presbyterian-lynchburg",
        "name": "Rivermont Evangelical Presbyterian Church",
        "address": "2424 Rivermont Ave, Lynchburg, VA 24503",
        "pastor": "Dr. David Weber (Senior Pastor)",
        "pastor_credentials": "Senior Pastor; Evangelical Presbyterian Church (EPC); preaches regularly on Westminster Confession theology; long-tenured at Rivermont",
        "founded": "1881",
        "type": "Evangelical Presbyterian Church (EPC)",
        "denomination": "Evangelical Presbyterian Church (EPC) — New River Presbytery",
        "website": "https://www.rivermont.org",
        "services": "Sundays (see website for current times); Women's Bible Study Wednesday & Thursday",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Theological Alignment — Reformed Presbyterian, Westminster Confession, 140-Year Legacy",
        "region": "lynchburg",
        "scores": {
            "christology": "green",
            "scripture": "green",
            "gender": "green",
            "leadership": "green",
            "soteriology": "green",
            "cultural": "green",
            "denomination": "green",
            "preaching": "green",
            "mens": "green",
            "mission": "green"
        },
        "score_notes": {
            "denomination": "EPC — Evangelical Presbyterian Church. Member of New River Presbytery. Beliefs summarized in the Westminster Confession of Faith and Catechisms. EPC provides strong confessional accountability while maintaining evangelical warmth.",
            "scripture": "Westminster Confession of Faith — inerrancy and infallibility affirmed within Reformed confessional framework.",
            "gender": "EPC maintains male-only ordained ministry. Rivermont is Presbyterian in governance — male elders and pastors. Westminster Standards are complementarian in their framework of church order.",
            "preaching": "Dr. David Weber is described by church members as a preacher whose sermons are 'truly amazing' — Westminster-confession formed Reformed preaching tradition.",
            "mission": "Campus Outreach ministry on-site (Regional Director of Campus Outreach on staff) — indicates intentional reaching of the college/university population in Lynchburg."
        },
        "assessment": "Rivermont Evangelical Presbyterian Church is one of Lynchburg's most theologically distinguished congregations. Founded in 1881 — over 140 years of ministry in the same Lynchburg neighborhood — Rivermont operates under the Westminster Confession of Faith and Catechisms within the EPC (Evangelical Presbyterian Church). Dr. David Weber's preaching is highly regarded by long-time members. The church's membership in the New River Presbytery provides genuine external accountability, confessional standards, and doctrinal oversight absent in independent churches. For a man wanting Reformed theology, historic confessional Christianity, and a church with deep Lynchburg roots and community presence, Rivermont EPC is a top-tier choice. The Campus Outreach ministry on staff signals a heart for the next generation.",
        "tags": ["epc", "evangelical-presbyterian", "reformed", "westminster-confession", "lynchburg", "historic", "david-weber"],
        "gender_detail": "Male-only ordained ministry (EPC — Westminster Standards); elder-governed; complementarian in theology and church polity",
        "denomination_detail": "Evangelical Presbyterian Church (EPC) — New River Presbytery; Westminster Confession of Faith and Catechisms as confessional standard",
        "engagement": {
            "visited_facility": False,
            "attended_services": False,
            "viewed_online_services": False,
            "researched_website": False,
            "know_members_personally": False,
            "interacted_with_leadership": False,
            "attended_personally": False
        }
    },
    {
        "id": "grace-church-lynchburg-efca",
        "name": "Grace Church Lynchburg (EFCA)",
        "address": "257 Trojan Rd, Madison Heights, VA 24572 (meets at Monelison Middle School)",
        "pastor": "Lead Pastor (see graceefc.net for current leadership)",
        "pastor_credentials": "Evangelical Free Church of America (EFCA) congregation; founded by a church plant from Lynchburg area; currently building permanent facility across from Monelison Middle School",
        "founded": "1988",
        "type": "Evangelical Free Church of America (EFCA)",
        "denomination": "Evangelical Free Church of America (EFCA)",
        "website": "https://graceefc.net",
        "services": "Sundays at 10:00 AM at Monelison Middle School, Madison Heights; Wednesday Youth 6:30 PM",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Theological Alignment — EFCA Accountability, Missional Church Plant DNA",
        "region": "lynchburg",
        "scores": {
            "christology": "green",
            "scripture": "green",
            "gender": "green",
            "leadership": "green",
            "soteriology": "green",
            "cultural": "green",
            "denomination": "green",
            "preaching": "green",
            "mens": "green",
            "mission": "green"
        },
        "score_notes": {
            "denomination": "EFCA — Evangelical Free Church of America. The EFCA's Statement of Faith is one of the strongest evangelical confessional statements among nondenominational-style networks. Clear on inerrancy, complementarian, Great Commission focused.",
            "scripture": "EFCA Statement of Faith: Scripture is 'the supreme authority in all matters of belief and practice.' Inerrancy affirmed.",
            "gender": "EFCA holds complementarian position — male-only senior pastors. Grace Church Lynchburg aligns with EFCA complementarian policy.",
            "mission": "The church has transitioned through six rented facilities over its 35+ year history — a mark of missional flexibility and commitment to community presence over institutional comfort. Now building a permanent home.",
            "preaching": "EFCA churches are known for expository, Bible-centered preaching. Verify current lead pastor and preaching style with a personal visit."
        },
        "assessment": "Grace Church Lynchburg is an Evangelical Free Church of America congregation with 35+ years of faithful ministry in the Lynchburg/Madison Heights corridor. Founded in 1988, Grace Church has served through six rented facilities and is now building a permanent home across from its current meeting place at Monelison Middle School — a sign of a congregation committed to long-term community investment. The EFCA is one of the strongest evangelical networks for theological accountability: clear confessional statement on inerrancy, male-only senior pastors, Great Commission mission, and strong doctrinal formation. For a man in the Madison Heights/Lynchburg area wanting a smaller, community-embedded church with solid evangelical credentials, Grace Church EFCA is worth visiting.",
        "tags": ["efca", "evangelical-free", "lynchburg", "madison-heights", "church-plant", "complementarian", "building-new"],
        "gender_detail": "Male-only senior pastor (EFCA policy); complementarian in structure; elder-governed local church",
        "denomination_detail": "Evangelical Free Church of America (EFCA) — strong confessional accountability, complementarian policy, inerrancy affirmed",
        "engagement": {
            "visited_facility": False,
            "attended_services": False,
            "viewed_online_services": False,
            "researched_website": False,
            "know_members_personally": False,
            "interacted_with_leadership": False,
            "attended_personally": False
        }
    },
    {
        "id": "grace-memorial-baptist-bedford",
        "name": "Grace Memorial Baptist Church",
        "address": "1737 Robertson Road, Bedford, VA 24523",
        "pastor": "Pastor Greg Rogers (Senior Pastor, since 2000)",
        "pastor_credentials": "Senior Pastor since 2000; long-tenured shepherd of a rural Bedford County congregation; SBC-affiliated; motto: 'A Friendly Place to Grow in Grace'",
        "founded": "Est. (Bedford area SBC congregation; documented four-pastor history)",
        "type": "Southern Baptist",
        "denomination": "Southern Baptist Convention (SBC of Virginia)",
        "website": "https://www.gmbcbedford.org",
        "services": "Sundays (see website for current times); midweek services",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Alignment — SBC Accountability, Long-Tenured Pastor, Rural Bedford Community",
        "region": "lynchburg",
        "scores": {
            "christology": "green",
            "scripture": "green",
            "gender": "green",
            "leadership": "green",
            "soteriology": "green",
            "cultural": "green",
            "denomination": "green",
            "preaching": "green",
            "mens": "green",
            "mission": "green"
        },
        "score_notes": {
            "denomination": "SBC of Virginia — Baptist Faith & Message 2000. Complementarian accountability baked in.",
            "leadership": "Greg Rogers has served as pastor since 2000 — 25+ years of stable, long-tenured pastoral ministry. That track record is rare and valuable. Long-tenured pastors build genuine community and deep discipleship.",
            "mission": "GMBC describes itself as a 'Discernment' church (discernement logo) focused on missions — SBC's international mission focus is present.",
            "cultural": "Rural Bedford County context — less cultural pressure toward progressive accommodation than urban/suburban churches. Small-town evangelical culture with genuine community ties."
        },
        "assessment": "Grace Memorial Baptist Church in Bedford is a rural SBC congregation with exactly the kind of pastoral stability that builds genuine community: Pastor Greg Rogers has served since 2000 — over 25 years of faithful shepherd ministry in the same Bedford County community. The church's motto ('A Friendly Place to Grow in Grace') reflects a congregation known for genuine warmth and welcome. SBC of Virginia affiliation provides Baptist Faith & Message 2000 accountability on Scripture, gender, and soteriology. For a man looking for a smaller, community-rooted SBC church outside of Lynchburg proper, with a long-tenured pastor and genuine Bedford County connections, Grace Memorial Baptist is an excellent option.",
        "tags": ["sbc", "southern-baptist", "bedford", "lynchburg-area", "rural", "long-tenured-pastor", "greg-rogers"],
        "gender_detail": "Male-only pastors and elders (SBC BF&M 2000); complementarian governance",
        "denomination_detail": "Southern Baptist Convention — SBC of Virginia; Baptist Faith & Message 2000 complementarian accountability",
        "engagement": {
            "visited_facility": False,
            "attended_services": False,
            "viewed_online_services": False,
            "researched_website": False,
            "know_members_personally": False,
            "interacted_with_leadership": False,
            "attended_personally": False
        }
    },

    # ─────────────────────────────────────────────────
    # WINCHESTER / SHENANDOAH VALLEY (5)
    # ─────────────────────────────────────────────────
    {
        "id": "blue-ridge-grace-brethren-winchester",
        "name": "Blue Ridge Grace Brethren Church",
        "address": "1025 Cedar Creek Grade, Winchester, VA 22602",
        "pastor": "Pastor Ermold Davey",
        "pastor_credentials": "Lead pastor of Blue Ridge Grace Brethren Church; FGBC (Fellowship of Grace Brethren Churches) tradition; Bible-teaching, dispensational framework",
        "founded": "1925 (as First Brethren Church of Winchester)",
        "type": "Grace Brethren / Fellowship of Grace Brethren Churches",
        "denomination": "Fellowship of Grace Brethren Churches (FGBC)",
        "website": "https://brgrace.com",
        "services": "Sundays (see website for current times)",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Alignment — 100-Year History, Grace Brethren Bible Teaching Tradition",
        "region": "shenandoah",
        "scores": {
            "christology": "green",
            "scripture": "green",
            "gender": "green",
            "leadership": "green",
            "soteriology": "green",
            "cultural": "green",
            "denomination": "yellow",
            "preaching": "green",
            "mens": "green",
            "mission": "green"
        },
        "score_notes": {
            "denomination": "Fellowship of Grace Brethren Churches (FGBC) — a conservative evangelical denomination with a dispensational theological framework. Smaller denomination than SBC, but provides genuine confessional accountability. Less external scrutiny than SBC megastructures.",
            "scripture": "FGBC affirmation: Scripture is the inspired, inerrant Word of God — final authority in all matters of faith and practice. Dispensational hermeneutic applied.",
            "gender": "Grace Brethren tradition is complementarian — male-only ordained ministry. Blue Ridge GBC governance reflects this.",
            "preaching": "Grace Brethren churches are known for verse-by-verse, dispensationally informed Bible teaching — similar DNA to Dallas Seminary tradition.",
            "mission": "The church was founded by a community that met at a farm to worship, then built their own meetinghouse — 100 years of Winchester community presence is significant."
        },
        "assessment": "Blue Ridge Grace Brethren Church has a remarkable 100-year history in Winchester, Virginia — founded in 1925 as the First Brethren Church of Winchester after a pioneering group of believers sold homemade cruellers to fund construction. This is the kind of sacrificial church-building story that marks a serious congregation. The Fellowship of Grace Brethren Churches provides accountability within a conservative evangelical, dispensationally informed tradition. Bible teaching is central to Grace Brethren DNA, with a doctrinal affirmation of Scripture's inerrancy and final authority. The Winchester Shenandoah Valley context gives this church a community role stretching back a century. For a man in Winchester or Frederick County wanting a smaller, doctrinally stable evangelical church with deep local roots, Blue Ridge Grace Brethren is worth visiting.",
        "tags": ["grace-brethren", "fgbc", "winchester", "shenandoah-valley", "dispensational", "100-year-history", "ermold-davey"],
        "gender_detail": "Male-only ordained ministry (FGBC tradition); complementarian church polity; elder/deacon governance structure",
        "denomination_detail": "Fellowship of Grace Brethren Churches (FGBC) — conservative evangelical; dispensational theology; inerrancy affirmed",
        "engagement": {
            "visited_facility": False,
            "attended_services": False,
            "viewed_online_services": False,
            "researched_website": False,
            "know_members_personally": False,
            "interacted_with_leadership": False,
            "attended_personally": False
        }
    },
    {
        "id": "calvary-baptist-winchester",
        "name": "Calvary Baptist Church Winchester",
        "address": "844 Amherst St, Winchester, VA 22601",
        "pastor": "Pastor Philip King",
        "pastor_credentials": "Senior Pastor; SBC of Virginia listed pastor at Calvary Baptist Winchester; complementarian SBC tradition",
        "founded": "Est. (long-standing Winchester SBC congregation)",
        "type": "Southern Baptist",
        "denomination": "Southern Baptist Convention (SBC of Virginia)",
        "website": "https://calvarywinchester.org",
        "services": "Sundays (see website for current times); Wednesday midweek",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Alignment — SBC Accountability, Winchester Community Church",
        "region": "shenandoah",
        "scores": {
            "christology": "green",
            "scripture": "green",
            "gender": "green",
            "leadership": "green",
            "soteriology": "green",
            "cultural": "green",
            "denomination": "green",
            "preaching": "green",
            "mens": "yellow",
            "mission": "green"
        },
        "score_notes": {
            "denomination": "SBC of Virginia — Baptist Faith & Message 2000 complementarian accountability. Standard SBC governance and doctrinal framework.",
            "preaching": "SBC church with youth pastor background in the area — active preaching ministry. Verify expository depth with personal visit.",
            "mens": "Men's ministry programming should be confirmed directly. Winchester is a smaller market than NoVA — programming size may vary.",
            "cultural": "Winchester is a historically conservative Shenandoah Valley city — less progressive pressure than Northern Virginia corridor."
        },
        "assessment": "Calvary Baptist Church Winchester is a Southern Baptist congregation serving the Winchester area with SBC of Virginia affiliation. Pastor Philip King leads the congregation at 844 Amherst Street — well-situated for Winchester's residential neighborhoods. The SBC affiliation guarantees Baptist Faith & Message 2000 accountability: male-only pastors, inerrancy, evangelical soteriology, and Great Commission mission emphasis. Winchester's Shenandoah Valley context means a more traditional evangelical culture without the NoVA progressive pressures. For a man in Winchester or Frederick County wanting a solid, accountable SBC congregation, Calvary Baptist is a reliable option.",
        "tags": ["sbc", "southern-baptist", "winchester", "shenandoah-valley", "complementarian", "philip-king"],
        "gender_detail": "Male-only pastors and elders (SBC BF&M 2000); complementarian church governance",
        "denomination_detail": "Southern Baptist Convention — SBC of Virginia; Baptist Faith & Message 2000 complementarian accountability",
        "engagement": {
            "visited_facility": False,
            "attended_services": False,
            "viewed_online_services": False,
            "researched_website": False,
            "know_members_personally": False,
            "interacted_with_leadership": False,
            "attended_personally": False
        }
    },
    {
        "id": "covenant-presbyterian-harrisonburg",
        "name": "Covenant Presbyterian Church",
        "address": "546 West Mosby Road, Harrisonburg, VA 22801",
        "pastor": "Rev. Todd Pruitt (Pastor)",
        "pastor_credentials": "PCA-ordained pastor; served at Covenant Presbyterian Harrisonburg; Blue Ridge Presbytery (PCA); known writer and Reformed voice in evangelical circles",
        "founded": "Est. (PCA congregation in Harrisonburg, Blue Ridge Presbytery)",
        "type": "Presbyterian Church in America (PCA)",
        "denomination": "Presbyterian Church in America (PCA) — Blue Ridge Presbytery",
        "website": "https://cov-pres.org",
        "services": "English Services: 8:30–9:45 AM & 11:15 AM–12:30 PM Sundays",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Theological Alignment — PCA Reformed, Westminster Standards, Dual Services",
        "region": "shenandoah",
        "scores": {
            "christology": "green",
            "scripture": "green",
            "gender": "green",
            "leadership": "green",
            "soteriology": "green",
            "cultural": "green",
            "denomination": "green",
            "preaching": "green",
            "mens": "green",
            "mission": "green"
        },
        "score_notes": {
            "denomination": "PCA — Presbyterian Church in America. One of the most theologically rigorous denominations in American evangelicalism. Westminster Confession of Faith and Catechisms as doctrinal standard. Blue Ridge Presbytery provides strong accountability.",
            "scripture": "Westminster Confession: Scripture is 'the only infallible rule of faith and practice.' Inerrancy, infallibility, and final authority affirmed within the strongest Reformed confessional framework.",
            "gender": "PCA maintains male-only ordination (TE/RE — Teaching Elders and Ruling Elders are male). Todd Pruitt is a known complementarian voice.",
            "preaching": "PCA/Westminster tradition means expository, theologically rich preaching informed by the catechisms and confessions. Todd Pruitt's Reformed orientation shapes preaching content.",
            "mission": "Dual Sunday services demonstrate serious congregational investment — two full morning services signal sufficient size to sustain robust ministry programs."
        },
        "assessment": "Covenant Presbyterian Church Harrisonburg is a PCA congregation under the Blue Ridge Presbytery — arguably the gold standard for Reformed evangelical accountability in American denominational life. The Westminster Confession of Faith provides the most rigorous doctrinal framework of any evangelical denomination. Rev. Todd Pruitt is a known Reformed voice who brings theological seriousness to pastoral ministry. Two full morning services (8:30 AM and 11:15 AM) signal a congregation of meaningful size with the infrastructure to support solid men's, children's, and discipleship ministries. The James Madison University context (Harrisonburg is a college town) gives Covenant opportunities for campus ministry and young adult outreach alongside its established membership. For a man in Harrisonburg or the Shenandoah Valley wanting the strongest Reformed confessional accountability available, Covenant Presbyterian is the benchmark.",
        "tags": ["pca", "presbyterian", "reformed", "westminster-confession", "harrisonburg", "shenandoah", "todd-pruitt", "complementarian"],
        "gender_detail": "Male-only ordination (PCA — Teaching Elders and Ruling Elders); complementarian in doctrine and polity; Todd Pruitt is a known Reformed complementarian voice",
        "denomination_detail": "Presbyterian Church in America (PCA) — Blue Ridge Presbytery; Westminster Confession of Faith and Catechisms as confessional standard",
        "engagement": {
            "visited_facility": False,
            "attended_services": False,
            "viewed_online_services": False,
            "researched_website": False,
            "know_members_personally": False,
            "interacted_with_leadership": False,
            "attended_personally": False
        }
    },
    {
        "id": "grace-covenant-church-harrisonburg",
        "name": "Grace Covenant Church",
        "address": "3337 Emmaus Road, Harrisonburg, VA 22801",
        "pastor": "Mike Souder (Lead Pastor, Elder)",
        "pastor_credentials": "Lead Pastor and Elder; Spanish-language ministry under Associate Pastor Cesar Gomez; third service capacity with multiple Sunday times",
        "founded": "Est. (Harrisonburg multiethnic evangelical church)",
        "type": "Evangelical / Nondenominational",
        "denomination": "Independent / Nondenominational (evangelical)",
        "website": "https://gcch.org",
        "services": "Sundays at 8:30 AM, 10:00 AM & 11:30 AM; 'Grace en Español' Spanish service",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — Female Associate Pastor, No Denominational Accountability, Positive Gospel Language",
        "region": "shenandoah",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "green",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "green"
        },
        "score_notes": {
            "gender": "The church lists Katherine Johnson as 'Associate Pastor' — a woman in a pastoral role. This is a yellow flag for those holding a male-elder-only (complementarian) ecclesiology based on 1 Timothy 2:12 and 3:1-7. Lead Pastor Mike Souder is male, but the staff structure includes a female associate pastor which indicates a non-complementarian or egalitarian pastoral framework.",
            "denomination": "Fully independent nondenominational — no external accountability structure. All governance is internal. No confessional standard to default to.",
            "leadership": "Elder governance structure (Mike Souder listed as Lead Pastor, Elder) — positive indicator. But the female associate pastor raises questions about the elder board's gender composition.",
            "cultural": "Three Sunday services and a Spanish-language congregation (Grace en Español) indicate a growing, outward-focused congregation. The multi-ethnic reach is a strength.",
            "preaching": "Evangelical nondenominational preaching — verify expository depth. Three services suggest a popular teaching style rather than a smaller, deeper discipleship model.",
            "mission": "Strong missional indicators: three services, bilingual ministry, active small groups, children's ministry. The mission language ('Love Big, Grow Deep, Go Out') is solid."
        },
        "assessment": "Grace Covenant Church Harrisonburg is a growing evangelical congregation with genuine strengths: male lead pastor with elder title (Mike Souder), three Sunday services including a Spanish-language service (Grace en Español under Pastor Cesar Gomez), active small groups, and a clear missional orientation. The church's tagline ('Love Big, Grow Deep, Go Out') reflects a healthy balance of inward formation and outward reach. However, the staff directory lists Katherine Johnson as 'Associate Pastor' — a female in a pastoral office. For a man holding a complementarian conviction based on Scripture's pattern of male-only pastoral eldership, this is a concern that warrants direct conversation with the church about their theology of eldership and gender. If the 'associate pastor' role is staff-level rather than ordained eldership, that changes the assessment — but verification is needed. Worth visiting with discernment.",
        "tags": ["non-denom", "harrisonburg", "shenandoah", "bilingual", "multiethnic", "mike-souder", "three-services", "caution"],
        "gender_detail": "Male Lead Pastor (Mike Souder, Elder); female Associate Pastor (Katherine Johnson) — indicates non-complementarian or egalitarian pastoral framework; needs direct clarification",
        "denomination_detail": "Independent nondenominational — no external accountability; internal elder governance; no confessional standard",
        "engagement": {
            "visited_facility": False,
            "attended_services": False,
            "viewed_online_services": False,
            "researched_website": False,
            "know_members_personally": False,
            "interacted_with_leadership": False,
            "attended_personally": False
        }
    },
    {
        "id": "calvary-baptist-staunton",
        "name": "Calvary Baptist Church Staunton",
        "address": "105 Garland Dr, Staunton, VA 24401",
        "pastor": "Pastor Stewart McCarter",
        "pastor_credentials": "Senior Pastor; SBC of Virginia listed pastor at Calvary Baptist Staunton; long-serving evangelical pastor in the Staunton/Augusta County area",
        "founded": "Est. (established Staunton-area SBC congregation)",
        "type": "Southern Baptist",
        "denomination": "Southern Baptist Convention (SBC of Virginia)",
        "website": "https://www.cbcstaunton.org",
        "services": "Sundays (see website for current times); midweek Bible study",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Alignment — SBC Accountability, Staunton Valley Community Church",
        "region": "shenandoah",
        "scores": {
            "christology": "green",
            "scripture": "green",
            "gender": "green",
            "leadership": "green",
            "soteriology": "green",
            "cultural": "green",
            "denomination": "green",
            "preaching": "green",
            "mens": "green",
            "mission": "green"
        },
        "score_notes": {
            "denomination": "SBC of Virginia — Baptist Faith & Message 2000. Standard SBC complementarian and doctrinal accountability.",
            "cultural": "Staunton is a historic Shenandoah Valley city (birthplace of Woodrow Wilson) with a traditional community character. Less progressive cultural pressure than Northern Virginia.",
            "mission": "SBC Great Commission mission focus built into denominational DNA — support for NAMB (North American Mission Board) and IMB (International Mission Board).",
            "preaching": "SBC tradition — preaching quality should be verified with a personal visit. Expository preaching is the SBC ideal.",
            "mens": "Men's ministry programming should be confirmed directly with the church."
        },
        "assessment": "Calvary Baptist Church Staunton serves the historic Shenandoah Valley city of Staunton (Augusta County) under Pastor Stewart McCarter. The SBC of Virginia affiliation provides Baptist Faith & Message 2000 accountability — inerrancy, male-only pastors, evangelical soteriology, and Great Commission mission emphasis are built into the denominational framework. Staunton's traditional Virginia context means a more conservative evangelical culture, and being 20 miles from Harrisonburg (James Madison University) gives the church crossroads access to both rural communities and college-area demographics. For a man in the Staunton/Waynesboro/Augusta County area wanting a solid, accountable SBC church, Calvary Baptist Staunton is the standard choice.",
        "tags": ["sbc", "southern-baptist", "staunton", "shenandoah-valley", "augusta-county", "complementarian", "stewart-mccarter"],
        "gender_detail": "Male-only pastors and elders (SBC BF&M 2000); complementarian church governance",
        "denomination_detail": "Southern Baptist Convention — SBC of Virginia; Baptist Faith & Message 2000 complementarian accountability",
        "engagement": {
            "visited_facility": False,
            "attended_services": False,
            "viewed_online_services": False,
            "researched_website": False,
            "know_members_personally": False,
            "interacted_with_leadership": False,
            "attended_personally": False
        }
    },

    # ─────────────────────────────────────────────────
    # WILLIAMSBURG / PENINSULA (5)
    # ─────────────────────────────────────────────────
    {
        "id": "bruton-parish-episcopal-williamsburg",
        "name": "Bruton Parish Episcopal Church",
        "address": "201 W Duke of Gloucester St, Williamsburg, VA 23185",
        "pastor": "Rev. Bill Watson (Interim Rector)",
        "pastor_credentials": "Interim Rector serving during clergy leadership transition; previously served in Dioceses of Kentucky, Southwestern Virginia, and South Carolina; Episcopal (TEC) ordained priest",
        "founded": "1674",
        "type": "Episcopal (The Episcopal Church — TEC)",
        "denomination": "The Episcopal Church (TEC) — Diocese of Southern Virginia",
        "website": "https://www.brutonparish.org",
        "services": "Multiple services including weekday worship; Sunday services (see website for current schedule)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "red",
        "overall_label": "Not Recommended — Episcopal (TEC) Denomination, Progressive Theological Drift",
        "region": "peninsula",
        "scores": {
            "christology": "yellow",
            "scripture": "yellow",
            "gender": "red",
            "leadership": "red",
            "soteriology": "yellow",
            "cultural": "red",
            "denomination": "red",
            "preaching": "yellow",
            "mens": "red",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "The Episcopal Church (TEC) is one of the most theologically liberal mainline Protestant denominations in America. TEC has officially endorsed gay marriage, female bishops and priests, and has moved significantly away from biblical sexual ethics and complementarian church polity. Bruton Parish remains within TEC — despite the denomination's trajectory.",
            "gender": "TEC ordains women as priests and bishops. Bruton Parish currently has an interim rector (male) during transition, but the denomination officially allows and practices female ordination at all levels including bishops.",
            "cultural": "TEC has been a leader among mainline denominations in embracing progressive cultural norms — LGBTQ affirmation, inclusive language for God, and departure from historic Anglican sexual ethics are TEC institutional positions.",
            "christology": "TEC's theological diversity allows significant variation in congregational beliefs — from evangelical Anglicanism to universalism. Bruton Parish's own theology needs direct investigation, as TEC does not enforce doctrinal uniformity.",
            "soteriology": "TEC does not hold a uniform soteriology. Without specific knowledge of Bruton Parish's preaching and doctrinal commitments, soteriology cannot be confirmed as orthodox.",
            "mens": "No dedicated men's ministry found. TEC context makes robust biblical men's discipleship formation less likely."
        },
        "assessment": "Bruton Parish Episcopal Church is one of America's most historically significant churches — established 1674, it hosted George Washington, Thomas Jefferson, Patrick Henry, and George Mason during the colonial era. The building is a National Historic Landmark in Colonial Williamsburg. However, historical significance does not equal current theological fidelity. Bruton Parish remains within The Episcopal Church (TEC) — a denomination that has departed from biblical sexual ethics, ordains women to all levels of ministry including bishop, officially endorses same-sex marriage, and has seen wholesale theological drift from orthodox Christianity. The congregation is currently in transition (interim rector). For a man committed to biblical inerrancy, male-only pastoral leadership, and historic Christian sexual ethics, Bruton Parish's TEC affiliation disqualifies it as a primary home church. Worth visiting as a historic site — not recommended as a spiritual home.",
        "tags": ["episcopal", "tec", "williamsburg", "historic", "not-recommended", "colonial-era", "mainline-liberal", "bruton-parish"],
        "gender_detail": "TEC ordains women as priests and bishops — denomination is fully egalitarian; current interim rector is male but TEC policy is non-complementarian",
        "denomination_detail": "The Episcopal Church (TEC) — Diocese of Southern Virginia; TEC is theologically liberal mainline, endorses gay marriage and female ordination at all levels",
        "engagement": {
            "visited_facility": False,
            "attended_services": False,
            "viewed_online_services": False,
            "researched_website": False,
            "know_members_personally": False,
            "interacted_with_leadership": False,
            "attended_personally": False
        }
    },
    {
        "id": "williamsburg-community-chapel",
        "name": "Williamsburg Community Chapel",
        "address": "3899 John Tyler Highway, Williamsburg, VA 23185",
        "pastor": "Lead Pastor (see wcchapel.org for current leadership)",
        "pastor_credentials": "Interdenominational family of faith; pastor(s) identified on wcchapel.org/about-us/what-we-believe/staff",
        "founded": "Est. (long-standing interdenominational Williamsburg congregation)",
        "type": "Interdenominational Evangelical",
        "denomination": "Interdenominational / Independent",
        "website": "https://wcchapel.org",
        "services": "Sundays (see website for current times)",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Cautious Commendation — Interdenominational, Evangelical Statement, No External Accountability",
        "region": "peninsula",
        "scores": {
            "christology": "green",
            "scripture": "green",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "green",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "green"
        },
        "score_notes": {
            "denomination": "Fully interdenominational — no external denominational accountability or confessional standard. All governance is internal. WCC's constitution declares it 'interdenominational... wherein all of those who love Jesus Christ... may join in one common effort.' No external creed or confession imposed beyond broad evangelical Christianity.",
            "scripture": "WCC's Statement of Faith adheres to 'all of the great historic confessions of the true church of Jesus Christ' — this is broad language suggesting evangelical orthodoxy, but requires direct investigation of specific commitments to inerrancy and biblical authority.",
            "gender": "Interdenominational context means gender polity needs direct verification — no denominational standard enforces complementarian or egalitarian positions. Check current pastoral/elder composition.",
            "preaching": "Interdenominational setting — preaching style and doctrinal depth need direct evaluation with a personal visit. Cannot assume expository or topical tradition.",
            "mens": "Men's ministry and discipleship infrastructure should be confirmed directly with the church.",
            "mission": "WCC's mission statement — making disciples by getting people into God's Word and preparing believers for works of service — is solid evangelical language."
        },
        "assessment": "Williamsburg Community Chapel has served the Williamsburg community as an interdenominational evangelical congregation for many years. The church's constitutional foundation — 'interdenominational church wherein all of those who love Jesus Christ and desire to serve Him may join in one common effort' — reflects a broad evangelical unity emphasis. The statement of faith appeals to 'all of the great historic confessions' of the Church, which is encouraging. The caution: interdenominational means no external accountability, no confessional standard enforced by a denomination, and significant variance in theological commitments is possible. For a man visiting Williamsburg or settling in the area, WCC is worth investigating directly — evaluate the current pastor, the specific doctrinal commitments, gender polity of the elder board, and preaching content before committing.",
        "tags": ["interdenominational", "williamsburg", "peninsula", "evangelical", "community-chapel", "non-denom"],
        "gender_detail": "Interdenominational — gender polity needs direct verification; no denominational standard for pastoral gender; check current elder/pastor composition",
        "denomination_detail": "Interdenominational / Independent — no external accountability; Statement of Faith references 'historic confessions' but no specific confessional standard enforced",
        "engagement": {
            "visited_facility": False,
            "attended_services": False,
            "viewed_online_services": False,
            "researched_website": False,
            "know_members_personally": False,
            "interacted_with_leadership": False,
            "attended_personally": False
        }
    },
    {
        "id": "grace-covenant-presbyterian-williamsburg",
        "name": "Grace Covenant Presbyterian Church",
        "address": "1677 Jamestown Rd, Williamsburg, VA 23185",
        "pastor": "Lead Pastor (see gracecovpca.org for current pastor)",
        "pastor_credentials": "PCA congregation in Williamsburg; Blue Ridge Presbytery or Potomac Presbytery (PCA); Westminster Confession accountability",
        "founded": "Est. (PCA congregation serving greater Williamsburg area)",
        "type": "Presbyterian Church in America (PCA)",
        "denomination": "Presbyterian Church in America (PCA)",
        "website": "https://www.gracecovpca.org",
        "services": "Sundays (see website for current times)",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Theological Alignment — PCA Reformed, Westminster Standards",
        "region": "peninsula",
        "scores": {
            "christology": "green",
            "scripture": "green",
            "gender": "green",
            "leadership": "green",
            "soteriology": "green",
            "cultural": "green",
            "denomination": "green",
            "preaching": "green",
            "mens": "green",
            "mission": "green"
        },
        "score_notes": {
            "denomination": "PCA — Presbyterian Church in America. Westminster Confession of Faith and Catechisms as doctrinal standard. Presbytery oversight provides external accountability. One of the strongest Reformed evangelical denominations in America.",
            "scripture": "Westminster Confession: Scripture is 'the only infallible rule of faith and practice.' Inerrancy, infallibility, and final authority fully affirmed.",
            "gender": "PCA maintains male-only ordination for Teaching Elders and Ruling Elders. Complementarian in doctrine and polity — no women in pastoral or elder roles.",
            "mission": "PCA mission DNA: Great Commission oriented with MTW (Mission to the World) as the international mission arm and RUF (Reformed University Fellowship) for campus ministry — both strong mission vehicles.",
            "preaching": "PCA tradition — expository, theologically rich preaching informed by the Westminster Catechisms and Confession. Reformed hermeneutics applied to biblical exposition."
        },
        "assessment": "Grace Covenant Presbyterian Church Williamsburg is a PCA congregation serving the Williamsburg/James City County area — bringing the full weight of PCA Reformed accountability to the Peninsula. The Presbyterian Church in America is one of the theologically strongest Reformed denominations in evangelical Christianity: Westminster Confession of Faith and Catechisms, male-only ordained ministry, expository preaching tradition, and active missions through MTW and Reformed University Fellowship. The Williamsburg context (College of William & Mary nearby) creates natural opportunities for campus engagement. PCA churches are consistently among the most doctrinally sound options in any geographic area. For a man on the Peninsula wanting Reformed evangelical accountability and confessional worship, Grace Covenant PCA is a top-tier option.",
        "tags": ["pca", "presbyterian", "reformed", "williamsburg", "peninsula", "westminster-confession", "complementarian"],
        "gender_detail": "Male-only ordination (PCA — Teaching Elders and Ruling Elders); complementarian in doctrine and polity; no women in pastoral or elder offices",
        "denomination_detail": "Presbyterian Church in America (PCA) — Westminster Confession of Faith and Catechisms; presbytery external accountability",
        "engagement": {
            "visited_facility": False,
            "attended_services": False,
            "viewed_online_services": False,
            "researched_website": False,
            "know_members_personally": False,
            "interacted_with_leadership": False,
            "attended_personally": False
        }
    },
    {
        "id": "first-baptist-newport-news",
        "name": "First Baptist Church Newport News",
        "address": "12716 Warwick Blvd, Newport News, VA 23606",
        "pastor": "Dr. Randy Shepley III (Pastor)",
        "pastor_credentials": "Pastor of FBC Newport News; BGAV (Baptist General Association of Virginia) affiliated; established Newport News congregation since 1881",
        "founded": "1881 (organized as Newport News Baptist Church; formally constituted 1883)",
        "type": "Baptist (BGAV — Baptist General Association of Virginia)",
        "denomination": "Baptist General Association of Virginia (BGAV)",
        "website": "https://www.fbcnn.org",
        "services": "Sundays (see website for current times)",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — BGAV Affiliation (Moderate Baptist), Verify Doctrinal Stance",
        "region": "peninsula",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "green",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "yellow"
        },
        "score_notes": {
            "denomination": "BGAV (Baptist General Association of Virginia) — the moderate Baptist body in Virginia, distinct from the more conservative SBC of Virginia. BGAV is associated with CBF (Cooperative Baptist Fellowship) and has a more theologically diverse, moderate stance than the SBC. BGAV churches vary significantly in their theological positions, particularly on Scripture, gender, and cultural accommodation.",
            "scripture": "BGAV does not require inerrancy — while many congregations hold to biblical authority, the denominational framework is more theologically moderate than the SBC's Baptist Faith & Message 2000.",
            "gender": "BGAV is more egalitarian than SBC — allows and affirms women in pastoral roles at the denominational level. First Baptist Newport News specific stance needs direct verification.",
            "cultural": "Newport News is a diverse Hampton Roads city — the urban context and BGAV's moderate posture increase risk of progressive cultural accommodation in programming and preaching.",
            "preaching": "First Baptist Newport News has a 140-year history — but BGAV affiliation means the preaching culture needs direct evaluation to determine whether it's expository or therapeutic/topical.",
            "mens": "Men's ministry and discipleship infrastructure needs direct verification given BGAV's more moderate denominational context."
        },
        "assessment": "First Baptist Church Newport News has a remarkable 140-year history on the Virginia Peninsula, organized in 1881 and formally constituted in 1883. Dr. Randy Shepley III leads this historic congregation. The concern is the BGAV affiliation — the Baptist General Association of Virginia is the moderate Baptist body in Virginia, distinct from the more conservative SBC of Virginia. BGAV is connected with the Cooperative Baptist Fellowship and takes a theologically moderate stance that allows greater diversity on Scripture, gender roles, and cultural issues than the SBC's Baptist Faith & Message 2000. This doesn't make FBCNN a bad church — but it means verification is required. Visit, listen to the preaching, ask directly about their stance on Scripture's authority and complementarian convictions before committing. The historic pedigree is impressive; the denominational framework is less clearly conservative.",
        "tags": ["bgav", "moderate-baptist", "newport-news", "peninsula", "historic", "randy-shepley", "caution"],
        "gender_detail": "BGAV allows women in pastoral roles — First Baptist Newport News specific stance needs direct verification; complementarian conviction cannot be assumed",
        "denomination_detail": "Baptist General Association of Virginia (BGAV) — moderate Baptist body; associated with CBF; more theologically diverse than SBC; inerrancy not required",
        "engagement": {
            "visited_facility": False,
            "attended_services": False,
            "viewed_online_services": False,
            "researched_website": False,
            "know_members_personally": False,
            "interacted_with_leadership": False,
            "attended_personally": False
        }
    },
    {
        "id": "new-hope-baptist-hampton",
        "name": "New Hope Baptist Church",
        "address": "1415 Big Bethel Road, Hampton, VA 23666",
        "pastor": "Pastor (see newhopebaptisthampton.org for current pastor)",
        "pastor_credentials": "Established Hampton Baptist congregation; documented ministries including evangelism team, seniors' ministry, tutorial ministry; active community engagement",
        "founded": "Est. early 1970s (50th anniversary recognized by Congress ~2018)",
        "type": "Baptist (Independent / National Baptist tradition)",
        "denomination": "Independent Baptist",
        "website": "https://newhopebaptisthampton.org",
        "services": "Sundays (Sunday School and main worship service); midweek Bible study",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — Independent Baptist, Verify Doctrinal Specifics and Leadership Structure",
        "region": "peninsula",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "green",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "green"
        },
        "score_notes": {
            "denomination": "Independent Baptist congregation — no external denominational accountability. National Baptist or independent Baptist tradition based on church culture and leadership language. All governance is internal.",
            "leadership": "Church previously served by Dr. Christopher C. Carter Sr. (installed 1995); current leadership needs verification via newhopebaptisthampton.org. Independent congregational governance means all accountability is internal.",
            "gender": "Independent Baptist tradition varies — needs direct verification of pastoral/elder gender composition. Cannot assume complementarian framework without direct inquiry.",
            "cultural": "Hampton is a diverse Hampton Roads city with significant African American community heritage. The church serves as a community anchor, which is a strength — but the cultural context requires evaluating how the church navigates progressive pressures.",
            "mission": "Congressional record notes the church's 50th anniversary and multiple community ministries (evangelism team, tutorial ministry, seniors' ministry) — genuine community mission presence.",
            "preaching": "Preaching content and style need direct evaluation via personal visit. Independent Baptist tradition varies widely.",
            "mens": "Men's ministry infrastructure needs direct verification."
        },
        "assessment": "New Hope Baptist Church has served the Hampton, Virginia community for approximately 50+ years, recognized by Congress for its 50th anniversary with documented community ministries including evangelism teams, tutorial programs, and seniors' ministry. The church's community presence and active ministry programs are genuine strengths. As an independent Baptist congregation, however, there is no external denominational accountability or confessional standard — all doctrine, governance, and gender polity is determined internally. The current pastoral leadership needs verification via the church website. For a man in the Hampton/Big Bethel Road area, New Hope Baptist is worth investigating directly: visit, evaluate the preaching, ask about their confession of faith and elder/deacon structure, and assess whether it provides the kind of doctrinally serious environment needed for men's formation.",
        "tags": ["independent-baptist", "hampton", "peninsula", "community-ministry", "50-year-history", "hampton-roads"],
        "gender_detail": "Independent Baptist tradition — gender polity varies; needs direct verification of pastor/elder gender composition",
        "denomination_detail": "Independent Baptist — no external accountability; congregational governance; no confessional standard enforced externally",
        "engagement": {
            "visited_facility": False,
            "attended_services": False,
            "viewed_online_services": False,
            "researched_website": False,
            "know_members_personally": False,
            "interacted_with_leadership": False,
            "attended_personally": False
        }
    },
]

SCORE_LABELS = {
    "green": ("score-green", "✅ Strong"),
    "yellow": ("score-yellow", "⚠️ Caution"),
    "red": ("score-red", "❌ Concern"),
    "black": ("score-black", "—  Unknown"),
}

OVERALL_CSS = {
    "green": "rating-green",
    "yellow": "rating-yellow",
    "red": "rating-red",
}

OVERALL_ICON = {
    "green": "✅",
    "yellow": "⚠️",
    "red": "🚫",
}

RUBRIC = [
    ("christology", "Christology", "Is Jesus the only way? (John 14:6)"),
    ("scripture", "Scripture", "Inerrancy affirmed? Final authority?"),
    ("gender", "Gender / Sexuality", "Biblical manhood & womanhood? Male-only elders/pastors? Patriarchal household vision?"),
    ("leadership", "Leadership Structure", "Male elders/pastors? Accountability?"),
    ("soteriology", "Soteriology", "Faith alone? How is salvation presented?"),
    ("cultural", "Cultural Alignment", "DEI/CRT language? Social justice crowding out gospel?"),
    ("denomination", "Denominational Accountability", "Sent/accountable or independent?"),
    ("preaching", "Preaching Style", "Expository or topical/therapeutic?"),
    ("mens", "Men's Discipleship", "Intentional formation for men?"),
    ("mission", "Mission Clarity", "Great Commission central?"),
]

ENGAGEMENT_KEYS = [
    ("visited_facility", "Visited the Facility"),
    ("attended_services", "Attended Sunday Services"),
    ("viewed_online_services", "Viewed Online Services"),
    ("researched_website", "Researched Website"),
    ("know_members_personally", "Know Members Personally"),
    ("interacted_with_leadership", "Interacted with Leadership"),
    ("attended_personally", "Attended Personally"),
]

def h(s):
    return html_mod.escape(str(s))

def render_score_badge(rating):
    css, label = SCORE_LABELS.get(rating, SCORE_LABELS["black"])
    return f'<span class="score-badge {css}">{label}</span>'

def render_page(church):
    c = church
    today = date.today().isoformat()
    name = h(c["name"])
    denom_tag = h(c["type"])
    address = h(c["address"])
    overall = c["overall_rating"]
    overall_css = OVERALL_CSS.get(overall, "rating-yellow")
    overall_icon = OVERALL_ICON.get(overall, "⚠️")
    overall_label = h(c["overall_label"])
    website = c["website"]
    website_display = website.replace("https://", "").replace("http://", "")

    score_rows = ""
    for key, label, desc in RUBRIC:
        rating = c["scores"].get(key, "black")
        note = c.get("score_notes", {}).get(key, "")
        gender_detail = c.get("gender_detail", "") if key == "gender" else ""
        badge = render_score_badge(rating)
        note_html = f'<div class="score-note">{h(note)}</div>' if note else ""
        gd_html = f'<div class="gender-detail">👤 {h(gender_detail)}</div>' if gender_detail and key == "gender" else ""
        score_rows += f"""
      <div class="score-row">
        <div class="score-info">
          <div class="score-label">{h(label)}</div>
          <div class="score-desc">{h(desc)}</div>
          {note_html}
          {gd_html}
        </div>
        <div>{badge}</div>
      </div>"""

    tags_html = "".join(f'<span class="tag">#{t}</span>' for t in c.get("tags", []))

    eng = c.get("engagement", {})
    eng_rows = ""
    for key, label in ENGAGEMENT_KEYS:
        val = eng.get(key, False)
        if val:
            badge_style = 'color:#7edd80; border-color:#7edd80; background:rgba(76,175,80,0.15);'
            badge_text = "✅ Yes"
        else:
            badge_style = 'color:#888888; border-color:#888888; background:rgba(50,50,50,0.6);'
            badge_text = "❌ No"
        eng_rows += f"""
      <div class="score-row">
        <div class="score-info">
          <div class="score-label">{h(label)}</div>
        </div>
        <div>
          <span class="score-badge" style="{badge_style}">{badge_text}</span>
        </div>
      </div>"""

    map_addr = address.replace('"', '').replace("'", "")
    map_url = f"https://maps.google.com/maps?q={map_addr.replace(' ', '%20')}&output=embed"

    has_mens = "✅ Yes" if c.get("has_mens_ministry") else "❌ No"
    has_kids = "✅ Yes" if c.get("has_kids_ministry") else "❌ No"
    has_mens_cls = "has-yes" if c.get("has_mens_ministry") else "has-no"
    has_kids_cls = "has-yes" if c.get("has_kids_ministry") else "has-no"

    denom_detail = h(c.get("denomination_detail", c.get("denomination", "")))
    pastor_creds = h(c.get("pastor_credentials", ""))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/icons/favicon-16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
  <link rel="manifest" href="/manifest.json">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{name} — Theological due diligence scorecard for Christian men.">
  <meta property="og:title" content="{name} — Church Directory | USMC Ministries">
  <meta property="og:description" content="10-point theological scorecard: {overall_label}">
  <meta property="og:type" content="website">
  <title>{name} — Church Directory | USMC Ministries</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  :root {{
    --bg: #000000; --bg-card: #111111; --gold: #D4AF37; --gold-light: #F4D470;
    --white: #e8e8e8; --gray: #888888; --gray-light: #aaaaaa; --border: #333333;
    --green: #4CAF50; --yellow: #FFC107; --red: #f44336;
  }}
  body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--white); line-height: 1.7; min-height: 100vh; }}
  h1, h2, h3, h4 {{ font-family: 'Playfair Display', serif; }}
  .top-nav {{
    display: flex; flex-wrap: wrap; gap: 6px; justify-content: center;
    padding: 14px 20px; border-bottom: 1px solid var(--border);
    background: rgba(0,0,0,0.95); position: sticky; top: 0; z-index: 100;
  }}
  .top-nav a {{
    color: var(--gray); text-decoration: none; font-size: 0.85rem; font-weight: 500;
    padding: 5px 12px; border-radius: 20px; border: 1px solid transparent;
    transition: all 0.2s; white-space: nowrap;
  }}
  .top-nav a:hover {{ color: var(--gold); border-color: var(--border); }}
  .top-nav a:first-child {{ color: var(--gold); border-color: var(--border); }}
  .hero {{
    padding: 48px 24px 36px; text-align: center;
    background: linear-gradient(180deg, rgba(212,175,55,0.08) 0%, transparent 100%);
    border-bottom: 1px solid var(--border);
  }}
  .hero h1 {{ font-size: clamp(1.6rem, 4vw, 2.6rem); color: var(--white); margin-bottom: 8px; letter-spacing: 0.5px; }}
  .hero .denom-tag {{
    display: inline-block; background: rgba(212,175,55,0.1); border: 1px solid rgba(212,175,55,0.25);
    color: var(--gold-light); font-size: 0.75rem; font-weight: 600; letter-spacing: 1.5px;
    text-transform: uppercase; padding: 3px 12px; border-radius: 20px; margin-bottom: 16px;
  }}
  .hero .address {{ color: var(--gray-light); font-size: 0.95rem; margin-bottom: 18px; }}
  .threat-badge {{
    display: inline-flex; align-items: center; gap: 8px; padding: 8px 20px;
    border-radius: 8px; font-weight: 700; font-size: 0.95rem; letter-spacing: 0.5px;
    margin-top: 8px; border: 1.5px solid;
  }}
  .threat-badge.rating-green {{ background: rgba(76,175,80,0.18); border-color: var(--green); color: #7edd80; }}
  .threat-badge.rating-yellow {{ background: rgba(255,193,7,0.15); border-color: var(--yellow); color: #ffd85a; }}
  .threat-badge.rating-red {{ background: rgba(244,67,54,0.15); border-color: var(--red); color: #ff7c74; }}
  .threat-icon {{ font-size: 1.3rem; }}
  .page-body {{ max-width: 960px; margin: 0 auto; padding: 36px 24px 60px; }}
  .card {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 24px; margin-bottom: 28px; }}
  .card-title {{ font-size: 1.0rem; text-transform: uppercase; letter-spacing: 2px; color: var(--gold); margin-bottom: 18px; font-family: 'Inter', sans-serif; font-weight: 700; }}
  .facts-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 14px; }}
  .fact-item {{ display: flex; flex-direction: column; gap: 3px; }}
  .fact-label {{ font-size: 0.72rem; color: var(--gray); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }}
  .fact-value {{ font-size: 0.92rem; color: var(--white); font-weight: 500; }}
  .fact-value a {{ color: var(--gold); text-decoration: none; }}
  .fact-value a:hover {{ text-decoration: underline; }}
  .has-yes {{ color: #7edd80; font-weight: 600; }}
  .has-no {{ color: var(--gray); }}
  .score-row {{
    display: grid; grid-template-columns: 1fr auto; gap: 12px;
    align-items: start; padding: 14px 0; border-bottom: 1px solid #1e1e1e;
  }}
  .score-row:last-child {{ border-bottom: none; }}
  .score-info {{ display: flex; flex-direction: column; gap: 4px; }}
  .score-label {{ font-weight: 600; font-size: 0.95rem; color: var(--white); }}
  .score-desc {{ font-size: 0.82rem; color: var(--gray-light); }}
  .score-note {{ font-size: 0.82rem; color: #aaa; margin-top: 4px; font-style: italic; }}
  .gender-detail {{ font-size: 0.8rem; color: #bbb; margin-top: 4px; padding: 6px 10px; background: rgba(212,175,55,0.06); border-left: 2px solid var(--gold); border-radius: 0 4px 4px 0; }}
  .score-badge {{ display: inline-flex; align-items: center; gap: 5px; padding: 4px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; white-space: nowrap; border: 1px solid; }}
  .score-green {{ background: rgba(76,175,80,0.15); border-color: var(--green); color: #7edd80; }}
  .score-yellow {{ background: rgba(255,193,7,0.12); border-color: var(--yellow); color: #ffd85a; }}
  .score-red {{ background: rgba(244,67,54,0.12); border-color: var(--red); color: #ff7c74; }}
  .score-black {{ background: rgba(50,50,50,0.6); border-color: #555; color: #aaa; }}
  .note-block {{ padding: 14px 16px; border-radius: 8px; margin-bottom: 12px; border-left: 3px solid; font-size: 0.9rem; line-height: 1.7; }}
  .note-assessment {{ background: rgba(212,175,55,0.06); border-color: var(--gold); color: var(--gray-light); }}
  .note-tag-row {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; }}
  .tag {{ background: #1a1a1a; border: 1px solid #333; color: var(--gray); font-size: 0.72rem; padding: 3px 10px; border-radius: 20px; }}
  .map-wrap {{ border-radius: 8px; overflow: hidden; border: 1px solid var(--border); margin-bottom: 28px; }}
  .map-wrap iframe {{ width: 100%; height: 320px; border: none; display: block; filter: invert(0.9) hue-rotate(180deg); }}
  .btn-row {{ display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 28px; }}
  .btn-gold {{ display: inline-flex; align-items: center; gap: 8px; background: var(--gold); color: #000; font-weight: 700; font-size: 0.9rem; padding: 11px 22px; border-radius: 8px; text-decoration: none; transition: background 0.2s; }}
  .btn-gold:hover {{ background: var(--gold-light); }}
  .btn-outline {{ display: inline-flex; align-items: center; gap: 8px; background: transparent; color: var(--gold); font-weight: 600; font-size: 0.9rem; padding: 11px 22px; border-radius: 8px; text-decoration: none; border: 1.5px solid var(--gold); transition: all 0.2s; }}
  .btn-outline:hover {{ background: rgba(212,175,55,0.1); }}
  .back-row {{ text-align: center; padding: 20px 0 10px; border-top: 1px solid var(--border); margin-top: 20px; }}
  .back-row a {{ color: var(--gold); text-decoration: none; font-weight: 600; font-size: 0.9rem; }}
  footer {{ text-align: center; padding: 24px; color: var(--gray); font-size: 0.8rem; border-top: 1px solid var(--border); }}
</style>
</head>
<body>
<nav class="top-nav">
  <a href="/churches.html">← Church Directory</a>
  <a href="/index.html">Home</a>
  <a href="/bible.html">Bible Translation Engine</a>
  <a href="/usmc-ministries.html">U.S.M.C. Ministries</a>
  <a href="/about.html">About</a>
  <a href="/connect.html">Connect</a>
</nav>

<div class="hero">
  <div class="denom-tag">{denom_tag}</div>
  <h1>{name}</h1>
  <div class="address">📍 {address}</div>
  <div class="threat-badge {overall_css}">
    <span class="threat-icon">{overall_icon}</span>
    <span class="threat-label">{overall_label}</span>
  </div>
</div>

<div class="page-body">
  <div class="card">
    <div class="card-title">📋 Quick Facts</div>
    <div class="facts-grid">
      <div class="fact-item">
        <span class="fact-label">Pastor</span>
        <span class="fact-value">{h(c["pastor"])}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Founded</span>
        <span class="fact-value">{h(c["founded"])}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Denomination</span>
        <span class="fact-value">{h(c["denomination"])}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Service Times</span>
        <span class="fact-value">{h(c["services"])}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Men's Ministry</span>
        <span class="fact-value {has_mens_cls}">{has_mens}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Kids Ministry</span>
        <span class="fact-value {has_kids_cls}">{has_kids}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Website</span>
        <span class="fact-value"><a href="{h(website)}" target="_blank" rel="noopener">{h(website_display)}</a></span>
      </div>
      <div class="fact-item" style="grid-column: 1 / -1;">
        <span class="fact-label">Pastor Credentials</span>
        <span class="fact-value" style="color: var(--gray-light); font-size: 0.88rem;">{pastor_creds}</span>
      </div>
    </div>
  </div>

  <div class="card">
    <div class="card-title">📊 10-Point Theological Scorecard</div>
    {score_rows}
  </div>

  <div class="card">
    <div class="card-title">📝 Assessment</div>
    <div class="note-block note-assessment">{h(c["assessment"])}</div>
    <div class="note-tag-row">{tags_html}</div>
  </div>

  <div class="card">
    <div class="card-title">🎯 My Engagement</div>
    <p style="font-size:0.82rem; color:var(--gray-light); margin-bottom:16px;">Moop's personal engagement with this church — updated as visits and interactions occur.</p>
    {eng_rows}
  </div>

  <div class="map-wrap">
    <iframe src="{map_url}" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Map for {name}"></iframe>
  </div>

  <div class="btn-row">
    <a href="{h(website)}" target="_blank" rel="noopener" class="btn-gold">🌐 Visit Their Website</a>
    <a href="/churches.html" class="btn-outline">← Back to Church Directory</a>
  </div>

  <div class="back-row">
    <a href="/churches.html">← Return to Full Church Directory</a>
  </div>
</div>

<footer>
  <p>Virginia Church Directory — Theological Due Diligence for Christian Men — <a href="https://usmcmin.org" style="color: var(--gold);">usmcmin.org</a></p>
  <p style="margin-top: 6px;">Last updated: {today}</p>
</footer>
</body>
</html>"""


def main():
    repo_root = os.path.join(os.path.dirname(__file__), "..")
    out_dir = os.path.join(repo_root, "docs", "churches")
    json_path = os.path.join(repo_root, "docs", "data", "churches.json")

    with open(json_path, "r") as f:
        data = json.load(f)

    existing_ids = {c["id"] for c in data["churches"]}
    added = 0
    updated = 0

    for church in CHURCHES:
        html_path = os.path.join(out_dir, f"{church['id']}.html")
        html_content = render_page(church)
        with open(html_path, "w") as f:
            f.write(html_content)
        print(f"✅ Wrote {html_path}")

        if church["id"] not in existing_ids:
            data["churches"].append(church)
            added += 1
            existing_ids.add(church["id"])
        else:
            for i, c in enumerate(data["churches"]):
                if c["id"] == church["id"]:
                    data["churches"][i] = church
                    updated += 1
                    break

    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n✅ churches.json updated: {added} added, {updated} updated")
    print(f"Total churches: {len(data['churches'])}")


if __name__ == "__main__":
    main()
