#!/usr/bin/env python3
"""
Generate 15 more DC/NoVA/Maryland church HTML pages.
Batch 2 — adds: Village Church DC, Redeemer Church of Arlington, River of Grace Lutheran,
Christ the Redeemer Anglican (Fairfax), Grace Reformed Church DC, HOPE Church (Clarksville MD),
Passion City Church DC, Christ Kirk DC, HOPE MD ECO, Pohick Church,
Vienna Presbyterian, Leesburg Community Church, River of Grace Lutheran NoVA,
The Village DC (Lewis Tait), Sojourn Church Fairfax (now RGC)
"""

import json, os, html as html_mod
from datetime import date

CHURCHES = [
    {
        "id": "village-church-dc",
        "name": "The Village DC",
        "address": "Washington, DC (online & house churches)",
        "pastor": "Rev. Dr. Lewis T. Tait, Jr. (Senior Pastor)",
        "pastor_credentials": "B.B.A. Hardin-Simmons University (1982); M.Div., Called to ministry 1984 under Bishop Lewis T. Tait, Sr.",
        "founded": "1984",
        "type": "Evangelical / Nondenominational",
        "denomination": "Independent / Nondenominational",
        "website": "https://www.thevillagedc.church",
        "services": "Sundays — check website for current schedule",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Cautious Commendation — Community-Focused, Verify Doctrine",
        "region": "dc-nova",
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
            "scripture": "Community-focused, urban ministry church. Biblical preaching appears solid but doctrinal statements are not prominently published — verify directly.",
            "gender": "Male senior pastor; church structure appears complementarian in practice but lacks published policy on gender roles in leadership.",
            "leadership": "Long-established DC church with multi-generational legacy. Independent governance — no external denominational accountability.",
            "cultural": "Active in DC civic engagement and community ministry including work with Catholic Charities and returning citizens. Watch for social gospel drift.",
            "denomination": "Fully independent. No external accountability structure beyond local elder/deacon governance."
        },
        "assessment": "The Village DC is a community-rooted, long-standing evangelical church in Washington, DC led by Rev. Dr. Lewis T. Tait, Jr., who carries on a legacy from his father Bishop Lewis T. Tait, Sr. The church has deep roots in DC urban ministry and active community engagement. It works collaboratively with other DC congregations on returning citizens ministry and neighborhood outreach — signs of genuine mission commitment. Caution: as an independent nondenominational church, there is no external doctrinal accountability. Verify their published statement of faith and ask about their views on gender roles and Scripture before committing. A solid option for DC-based men wanting community-rooted ministry, pending doctrinal verification.",
        "tags": ["non-denom", "urban-ministry", "dc-community", "returning-citizens", "legacy-church"],
        "gender_detail": "Male senior pastor; governance structure not publicly detailed — verify complementarian stance directly",
        "denomination_detail": "Fully independent nondenominational — no external denominational accountability",
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
        "id": "redeemer-church-of-arlington",
        "name": "Redeemer Church of Arlington",
        "address": "1125 Patrick Henry Drive, Arlington, VA 22205",
        "pastor": "Marshall Griffin (Lead Pastor)",
        "pastor_credentials": "M.Div. Southeastern Baptist Theological Seminary; Acts 29 Network church planter",
        "founded": "2012",
        "type": "Nondenominational / Acts 29",
        "denomination": "Acts 29 Network (nondenominational church planting network)",
        "website": "https://redeemerarlington.com",
        "services": "Sundays at 10:30 AM",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Recommended — Gospel-Centered, Acts 29 Plant",
        "region": "dc-nova",
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
            "denomination": "Acts 29 is a church planting network, not a denomination — member churches are autonomous. Network provides some peer accountability but no formal denominational structure.",
            "cultural": "Arlington, VA is a high-pressure, progressive-leaning metro context. Acts 29 churches generally hold well on biblical doctrine in cultural pressure situations."
        },
        "assessment": "Redeemer Church of Arlington is an Acts 29 church plant in Arlington, VA led by Marshall Griffin. Acts 29 is a respected church planting network founded by Mark Driscoll (now independent of him) focused on Gospel-centered, expository preaching and disciple-making. The church's stated mission — 'making disciples who follow Jesus into His Word, His world, and His family' — reflects a healthy integrative understanding of discipleship. Marshall Griffin was trained at Southeastern Baptist Theological Seminary, a conservative SBC school. For a man in the Arlington/DC metro area seeking a complementarian, Gospel-centered church with strong discipleship culture, Redeemer Arlington is a solid recommendation. Verify current elder board and ministry culture directly.",
        "tags": ["acts-29", "church-plant", "arlington", "expository", "discipleship", "gospel-centered"],
        "gender_detail": "Male lead pastor; Acts 29 network affirms complementarian gender theology — male eldership, women serve in broad ministry roles",
        "denomination_detail": "Acts 29 Network — autonomous member church with peer accountability through network; not a formal denomination",
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
        "id": "river-of-grace-lutheran-nova",
        "name": "River of Grace Lutheran Church",
        "address": "15012 Dumfries Road, Manassas, VA 20112",
        "pastor": "Pastor (verify current — church small, warm community)",
        "pastor_credentials": "ELCA-ordained pastor",
        "founded": "Est. 1990s",
        "type": "Lutheran (ELCA)",
        "denomination": "Evangelical Lutheran Church in America (ELCA)",
        "website": "https://rognova.com",
        "services": "Sundays — check website for current times",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "red",
        "overall_label": "Not Recommended — ELCA Denominational Apostasy",
        "region": "dc-nova",
        "scores": {
            "christology": "yellow",
            "scripture": "red",
            "gender": "red",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "red",
            "denomination": "red",
            "preaching": "yellow",
            "mens": "red",
            "mission": "yellow"
        },
        "score_notes": {
            "scripture": "ELCA does not hold to biblical inerrancy. Scripture viewed through historical-critical lens with significant accommodation to progressive culture.",
            "gender": "ELCA ordained women as pastors since 1970 and actively promotes LGBTQ+ clergy and same-sex marriage since 2009. This is a fundamental departure from biblical sexuality and gender.",
            "cultural": "ELCA has fully capitulated to progressive cultural accommodation including same-sex blessings, LGBTQ+ ordination, and social justice theology as core identity.",
            "denomination": "ELCA is the most theologically liberal Lutheran denomination in North America. Full communion with several other mainline denominations (PCUSA, Episcopal, UCC, Reformed Church in America).",
            "mens": "No robust men's discipleship culture in ELCA. Progressive gender ideology undermines biblical masculine leadership formation."
        },
        "assessment": "River of Grace Lutheran Church is affiliated with the ELCA (Evangelical Lutheran Church in America), the largest but most theologically liberal Lutheran denomination in North America. In 2009 the ELCA voted to ordain practicing homosexuals and allow blessing of same-sex unions — a clear departure from biblical sexuality (Romans 1, 1 Corinthians 6). The ELCA also rejects biblical inerrancy and has absorbed progressive social justice theology. Individual congregations may have faithful pastors who preach soundly despite the denomination, but the institutional framework provides no protection and active opposition to biblical sexuality. For a man wanting a doctrinally sound church with biblical authority and complementarian gender theology, an ELCA church is not recommended without careful individual investigation. Consider Missouri Synod or Wisconsin Synod Lutheran alternatives in the area.",
        "tags": ["elca", "lutheran", "manassas", "mainline", "theological-drift", "nova"],
        "gender_detail": "ELCA ordains women and LGBTQ+ clergy at the denominational level — local practice varies",
        "denomination_detail": "ELCA — Evangelical Lutheran Church in America; mainline Lutheran body with full affirmation of LGBTQ+ clergy and same-sex marriage",
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
        "id": "christ-the-redeemer-anglican-fairfax",
        "name": "Christ the Redeemer Anglican Church",
        "address": "PO Box 523218, Springfield, VA 22152 (meets in Fairfax, VA 22031)",
        "pastor": "The Rev. Dean Schultz (Rector)",
        "pastor_credentials": "ACNA-ordained Rector; Diocese of the Mid-Atlantic",
        "founded": "Est. 2000s",
        "type": "Anglican (ACNA)",
        "denomination": "Anglican Church in North America (ACNA) — Diocese of the Mid-Atlantic",
        "website": "https://ctranglican.church",
        "services": "Sundays at 4:00 PM on Zoom (liturgical online congregation; contact for in-person fellowship)",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Recommended — ACNA, Liturgical Orthodox, Faithful Anglican",
        "region": "dc-nova",
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
            "mens": "Small congregation with online-primary format may limit in-person men's community. Verify current in-person gatherings and fellowship opportunities.",
            "denomination": "ACNA was formed in 2009 as a biblically faithful alternative to the Episcopal Church (TEC). Affirms biblical sexuality and complementarian gender theology."
        },
        "assessment": "Christ the Redeemer Anglican is an ACNA congregation in Fairfax, VA under Rector Dean Schultz in the Diocese of the Mid-Atlantic. ACNA was formed as a breakaway from the Episcopal Church to preserve biblical Anglicanism — it holds to the authority of Scripture, the orthodox creeds, the Nicene faith, and biblical complementarianism (male eldership). The church follows the Sunday liturgy in the Book of Common Prayer including psalm-singing, Scripture readings, preaching, the Lord's Table, and intercessory prayer. Currently meeting primarily online via Zoom, which limits in-person community building. For men who value liturgical Anglican worship rooted in Scripture with ACNA accountability, this is a sound option — though the online-primary format warrants verification of current in-person fellowship opportunities.",
        "tags": ["acna", "anglican", "liturgical", "fairfax", "reformed-anglican", "bcp", "online"],
        "gender_detail": "Male rector; ACNA affirms complementarian gender theology and male-only ordained priesthood in diocesan policy",
        "denomination_detail": "Anglican Church in North America (ACNA) — Diocese of the Mid-Atlantic; orthodox Anglican body separate from liberal Episcopal Church (TEC)",
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
        "id": "grace-reformed-church-dc",
        "name": "Grace Reformed Church",
        "address": "1405 15th Street NW, Washington, DC 20005",
        "pastor": "Pastor (UCC — verify current pastor on website)",
        "pastor_credentials": "UCC-ordained minister",
        "founded": "1877",
        "type": "Liberal Mainline (UCC)",
        "denomination": "United Church of Christ (UCC)",
        "website": "https://gracereformedchurchdc.org",
        "services": "Sundays — check website",
        "has_mens_ministry": False,
        "has_kids_ministry": False,
        "overall_rating": "red",
        "overall_label": "Not Recommended — UCC Denomination, Theological Liberalism",
        "region": "dc-nova",
        "scores": {
            "christology": "yellow",
            "scripture": "red",
            "gender": "red",
            "leadership": "red",
            "soteriology": "red",
            "cultural": "red",
            "denomination": "red",
            "preaching": "red",
            "mens": "red",
            "mission": "red"
        },
        "score_notes": {
            "scripture": "UCC rejects biblical inerrancy and embraces historical-critical hermeneutics. Scripture is treated as a human document reflecting evolving faith community, not the authoritative Word of God.",
            "gender": "UCC fully affirms LGBTQ+ clergy, same-sex marriage, and was one of the first denominations to do so (1970s-1980s). 'Open and Affirming' is a standard UCC congregation designation.",
            "soteriology": "UCC typically embraces universalism or inclusivist soteriology. Exclusive claims of Christ (John 14:6) are routinely softened or rejected.",
            "cultural": "Grace Reformed DC has historically positioned itself as a politically liberal congregation in the heart of DC. Political-social engagement often supersedes evangelical mission.",
            "denomination": "UCC is the most theologically liberal mainline Protestant denomination in America. Formed from merger of Congregational Christian Churches and Evangelical and Reformed Church (1957). Full LGBTQ+ affirmation from top to bottom.",
            "mission": "Missions focus is predominantly social justice activism rather than evangelical proclamation of the Gospel."
        },
        "assessment": "Grace Reformed Church is a historic Washington DC congregation with a fascinating history — it was the church of President Theodore Roosevelt during his time in the White House. Originally an Evangelical and Reformed Church congregation, it merged into the United Church of Christ (UCC) in 1957. Today the UCC is one of the most theologically liberal denominations in America, fully affirming LGBTQ+ clergy and same-sex marriage, rejecting biblical inerrancy, and embracing pluralistic soteriology. Individual UCC congregations vary in their degree of liberalism, but the denomination provides no orthodox accountability. The historic building and Roosevelt connection make it interesting from a historical standpoint, but for a man seeking biblically sound Word ministry and gospel-centered community, Grace Reformed DC is not recommended. Seek out Reformed churches in the area that have maintained confessional integrity.",
        "tags": ["ucc", "mainline", "liberal-theology", "dc", "historic", "theodore-roosevelt", "not-recommended"],
        "gender_detail": "UCC fully ordains women and LGBTQ+ clergy — no complementarian stance",
        "denomination_detail": "United Church of Christ (UCC) — far-left mainline Protestant denomination with full LGBTQ+ affirmation, pluralistic theology",
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
        "id": "hope-church-clarksville-md",
        "name": "HOPE Church (Clarksville, MD)",
        "address": "Clarksville, MD (house churches throughout DC Metro area; Sunday gatherings in Clarksville)",
        "pastor": "Pastor Q (co-lead pastor)",
        "pastor_credentials": "ECO-affiliated pastor; focused on youth and discipleship",
        "founded": "Est. 2000s",
        "type": "Presbyterian (ECO)",
        "denomination": "ECO: A Covenant Order of Evangelical Presbyterians",
        "website": "https://hopemd.church",
        "services": "Fridays — house churches; Sundays — corporate gathering in Clarksville, MD",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Recommended — ECO Presbyterian, House Church Model, Solid Doctrine",
        "region": "dc-nova",
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
            "denomination": "ECO (A Covenant Order of Evangelical Presbyterians) was formed in 2012 as a theologically conservative alternative within Presbyterian polity, separate from the liberal PCUSA. ECO holds to Westminster Standards and biblical complementarianism.",
            "leadership": "House church model provides strong accountability and discipleship culture — every member integrated into a small covenant community meeting weekly."
        },
        "assessment": "HOPE Church (House of Prayer for Everyone) in Clarksville, MD is an ECO (Evangelical Covenant Order Presbyterian) congregation built around a house church model. Every member is integrated into a weekly house church gathering for dinner, fellowship, prayer, and Scripture — with corporate Sunday worship. ECO was formed in 2012 as a theologically conservative alternative to the PCUSA, affirming the Westminster Confession and biblical gender theology. This church's approach — Scripture-centered, prayer-saturated, community-integrated — reflects healthy early church patterns (Acts 2:42-46). For a man in the DC/Maryland area wanting deep discipleship, genuine community, and doctrinally sound Reformed theology, HOPE Church is a strong recommendation. The house church structure particularly builds the kind of accountable brotherhood that produces mature men.",
        "tags": ["eco", "presbyterian", "house-church", "discipleship", "clarksville-md", "prayer", "reformed"],
        "gender_detail": "Male pastor leadership; ECO affirms biblical complementarianism — male eldership, women serve broadly in ministry",
        "denomination_detail": "ECO: A Covenant Order of Evangelical Presbyterians — conservative Reformed body formed 2012 as alternative to liberal PCUSA",
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
        "id": "passion-city-church-dc",
        "name": "Passion City Church DC",
        "address": "620 T Street NW, Washington, DC 20001",
        "pastor": "Ben Stuart (Pastor)",
        "pastor_credentials": "M.A. Historical Theology, Dallas Theological Seminary; former Executive Director, Breakaway Ministries at Texas A&M; author of 'Single, Dating, Engaged, Married'",
        "founded": "2017",
        "type": "Nondenominational Evangelical",
        "denomination": "Independent / Nondenominational (Passion City Church network)",
        "website": "https://passioncitychurch.com/dc",
        "services": "Sundays at 9:30 AM and 11:30 AM (in-person and online)",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Cautious Commendation — Strong Preacher, Watch Megachurch Culture",
        "region": "dc-nova",
        "scores": {
            "christology": "green",
            "scripture": "green",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "green",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "green",
            "mens": "yellow",
            "mission": "green"
        },
        "score_notes": {
            "gender": "Ben Stuart is complementarian in his own theology and publications. However, Passion City Church's multi-site model and Atlanta roots (Louie Giglio) introduce ambiguity — verify current elder board gender policy.",
            "leadership": "Independent church network affiliated with Passion City Atlanta (Louie Giglio). No formal denominational accountability. Watch for celebrity culture dynamics in multi-site structure.",
            "cultural": "DC campus operates in NW Washington, a highly progressive context. Ben Stuart's preaching is generally biblically sound but the church culture in such environments can drift toward cultural accommodation over time.",
            "denomination": "Passion City Church is a multi-site network, not a denomination. Ben Stuart as DC city pastor operates with some autonomy but under Passion City's broader governance.",
            "mens": "Strong young adult and college ministry presence. Men's specific discipleship programs should be verified directly."
        },
        "assessment": "Passion City Church DC is the DC campus of Passion City Church (Atlanta), led by Ben Stuart as city pastor. Ben Stuart is a compelling teacher with solid biblical scholarship — his book 'Single, Dating, Engaged, Married' demonstrates theological depth and pastoral care. He earned his M.A. in historical theology at Dallas Theological Seminary. Passion City Church originated from the Passion movement (Louie Giglio) which is evangelical and mission-focused. Strengths: gifted communicator, strong young adult/college ministry, passion for global missions. Cautions: multi-site model disperses local eldership accountability; DC context creates constant pressure toward cultural accommodation; large church culture can undermine deep community. For a man in DC wanting strong preaching and young adult community, Passion City DC is worth attending — evaluate the elder structure and men's ministry depth before committing long-term.",
        "tags": ["non-denom", "multi-campus", "passion-city", "ben-stuart", "young-adults", "dc-nw", "missions"],
        "gender_detail": "Male city pastor (Ben Stuart); complementarian in personal theology — verify current elder board policy",
        "denomination_detail": "Passion City Church network — independent nondenominational; no formal denominational structure or external accountability",
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
        "id": "christ-kirk-dc",
        "name": "Christ Kirk DC",
        "address": "Washington, DC (check website for current meeting location)",
        "pastor": "Pastor Garrett Craw",
        "pastor_credentials": "Westminster Confession of Faith affirming pastor; affiliated with Christ Church Moscow (Doug Wilson) tradition; CREC-adjacent",
        "founded": "2020s",
        "type": "Reformed / Confessional Evangelical",
        "denomination": "Independent / Affiliated with Christ Church Moscow tradition",
        "website": "https://christkirkdc.com",
        "services": "Sundays at 10:30 AM",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Cautious Commendation — Strong Doctrine, Watch Association with Controversy",
        "region": "dc-nova",
        "scores": {
            "christology": "green",
            "scripture": "green",
            "gender": "green",
            "leadership": "yellow",
            "soteriology": "green",
            "cultural": "green",
            "denomination": "yellow",
            "preaching": "green",
            "mens": "green",
            "mission": "green"
        },
        "score_notes": {
            "leadership": "Christ Kirk DC is associated with the Christ Church Moscow (Doug Wilson) tradition and the CREC (Confederation of Reformed Evangelical Churches). Doug Wilson is a gifted theologian who has attracted significant controversy — men should evaluate critically. The DC church has been the target of organized protests by activist groups.",
            "denomination": "CREC is a loose confederation of Reformed evangelical churches — not a formal denomination with strong central authority. Offers some peer accountability but limited institutional oversight.",
            "gender": "Strong complementarian stance — one of the clearest in the DC metro area. Affirms male-only ordination and headship in family and church."
        },
        "assessment": "Christ Kirk DC is a confessional Reformed, evangelical church in Washington, DC affiliated with the Christ Church Moscow tradition (Doug Wilson, author and theologian). The church affirms the Apostles' Creed, Nicene Creed, Chalcedonian Definition, and Westminster Confession of Faith — a strong confessional foundation. Preaching from Pastor Garrett Craw is expository, Word-centered, and theologically serious. Strengths: genuine commitment to Reformation doctrine, strong complementarianism, serious men's discipleship, winsome confessional faith in an antagonistic cultural context. Caution: the Doug Wilson association brings controversy — Wilson's provocative cultural commentary and church planting theology attract both admirers and fierce critics; men should evaluate this association thoughtfully. The church has been targeted by progressive activist groups, which speaks to both its clear doctrinal stance and its cultural visibility. For a man wanting serious Reformed theology and strong masculine leadership culture in DC, Christ Kirk is worth serious consideration.",
        "tags": ["reformed", "confessional", "crec", "doug-wilson", "complementarian", "westminster", "dc", "controversial"],
        "gender_detail": "Male-only ordained leadership; strong complementarian theology; women serve in broad ministry roles",
        "denomination_detail": "CREC (Confederation of Reformed Evangelical Churches) — Reformed confessional network; associated with Christ Church Moscow tradition",
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
        "id": "pohick-church-lorton",
        "name": "Pohick Church",
        "address": "9301 Richmond Highway, Lorton, VA 22079",
        "pastor": "Rev. (verify current rector — Episcopal church)",
        "pastor_credentials": "Episcopal Church (TEC) ordained rector",
        "founded": "1641 (one of the oldest churches in Virginia; George Washington's parish)",
        "type": "Episcopal (TEC)",
        "denomination": "Episcopal Church (The Episcopal Church, USA — TEC)",
        "website": "https://pohick.org",
        "services": "Sundays — traditional Anglican liturgy; check website for times",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "red",
        "overall_label": "Not Recommended — TEC Denominational Apostasy",
        "region": "dc-nova",
        "scores": {
            "christology": "yellow",
            "scripture": "red",
            "gender": "red",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "red",
            "denomination": "red",
            "preaching": "yellow",
            "mens": "red",
            "mission": "yellow"
        },
        "score_notes": {
            "scripture": "TEC (Episcopal Church) officially rejects biblical inerrancy and embraces progressive hermeneutics. Homosexuality, same-sex marriage, and LGBTQ+ ordination are fully affirmed at the denominational level.",
            "gender": "TEC has ordained women as deacons, priests, and bishops since the 1970s-1980s. Same-sex marriage rites are standard. Presiding Bishop (2015-2024) was Michael Curry — charismatic preacher but progressive theologically.",
            "cultural": "TEC is a mainline denomination that has fully accommodated progressive cultural norms on gender, sexuality, and social justice.",
            "denomination": "The Episcopal Church has been in institutional crisis since 2003 (ordination of Gene Robinson as openly gay bishop). Multiple dioceses have left TEC to join the ACNA. TEC has sued departing congregations over property rights."
        },
        "assessment": "Pohick Church is one of the oldest and most historically significant churches in Northern Virginia — originally built in 1774 and known as the parish of George Washington, George Mason, and other Virginia Founders. It is a landmark of American religious history. However, it remains affiliated with the Episcopal Church (TEC), which has undergone systematic theological abandonment since the 1970s — ordaining women as priests and bishops, affirming same-sex marriage, and ordaining LGBTQ+ clergy. The historic beauty of this church and its colonial American legacy are genuinely compelling, but the TEC institutional framework is doctrinally unreliable. Men seeking sound biblical preaching and complementarian theology should consider ACNA alternatives in Northern Virginia (such as The Falls Church Anglican or Truro Anglican), which left TEC precisely over these issues. Visit Pohick as a history lesson; find a sound church for your soul.",
        "tags": ["episcopal", "tec", "historic", "george-washington", "colonial", "lorton", "northern-virginia", "not-recommended"],
        "gender_detail": "TEC ordains women as priests and bishops at all levels; same-sex marriage fully affirmed denominationally",
        "denomination_detail": "The Episcopal Church (TEC) — mainline Anglican body in USA; fully affirms LGBTQ+ clergy, same-sex marriage; in full communion with liberal Anglican provinces",
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
        "id": "vienna-presbyterian-church",
        "name": "Vienna Presbyterian Church",
        "address": "124 Park Street NE, Vienna, VA 22180",
        "pastor": "Rev. Peter Barnes (Senior Pastor — verify for current)",
        "pastor_credentials": "PCUSA-ordained; Ph.D. — verify current leadership at viennapres.org",
        "founded": "1867",
        "type": "Presbyterian (PCUSA)",
        "denomination": "Presbyterian Church (U.S.A.) — PCUSA",
        "website": "https://viennapres.org",
        "services": "Sundays at 8:00 AM, 9:30 AM, and 11:00 AM",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "red",
        "overall_label": "Not Recommended — PCUSA Denomination, Theological Drift",
        "region": "dc-nova",
        "scores": {
            "christology": "yellow",
            "scripture": "red",
            "gender": "red",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "red",
            "denomination": "red",
            "preaching": "yellow",
            "mens": "red",
            "mission": "yellow"
        },
        "score_notes": {
            "scripture": "PCUSA officially affirmed same-sex marriage and LGBTQ+ ordination (2015). The denomination has moved away from confessional Reformed standards despite nominally retaining the Westminster Standards.",
            "gender": "PCUSA ordains women as elders and pastors (since 1956/1964) and affirmed same-sex marriage in 2015. The denomination's confessional commitment to complementarian theology has been formally abandoned.",
            "cultural": "Vienna Presbyterian serves an affluent Northern Virginia community. The church's cultural engagement prioritizes inclusivity and progressive values alignment.",
            "denomination": "PCUSA is one of the mainline 'Seven Sisters' denominations. It has lost 40%+ of its membership since 1970 due to progressive drift. Many faithful PCA and ECO churches exist as orthodox alternatives.",
            "soteriology": "PCUSA broadly affirms evangelical soteriology in its creeds but increasing universalist and inclusivist tendencies at the denominational level."
        },
        "assessment": "Vienna Presbyterian Church is a historic PCUSA congregation in Vienna, VA. The PCUSA (Presbyterian Church USA) is the mainline Presbyterian denomination that voted in 2015 to approve same-sex marriage and has long ordained women as elders and pastors. This represents a fundamental departure from the Westminster Confession of Faith, the Reformed theological tradition, and biblical authority on sexuality. Individual PCUSA congregations vary — some maintain more conservative pastoral leadership despite the denomination's drift. However, the denominational framework means that membership contributions flow toward an institution that actively promotes positions contrary to biblical sexuality and clear scriptural authority. For men wanting Reformed theology with denominational integrity, the PCA (Presbyterian Church in America), the OPC (Orthodox Presbyterian Church), or ECO are the sound alternatives. Vienna has multiple PCA and ACNA options that hold the confessional line.",
        "tags": ["pcusa", "presbyterian", "mainline", "liberal-drift", "vienna-va", "northern-virginia", "not-recommended"],
        "gender_detail": "PCUSA ordains women as pastors and elders; same-sex marriage affirmed denominationally since 2015",
        "denomination_detail": "Presbyterian Church (U.S.A.) — mainline Presbyterian body; departed from confessional Reformed standards on gender and sexuality",
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
        "id": "leesburg-community-church",
        "name": "Leesburg Community Church",
        "address": "Leesburg, VA (multiple campuses — check leesburgcc.org)",
        "pastor": "Lead Pastor (verify at leesburgcc.org)",
        "pastor_credentials": "Contemporary evangelical church — verify pastoral credentials directly",
        "founded": "Est. 1990s",
        "type": "Nondenominational Evangelical",
        "denomination": "Independent / Nondenominational",
        "website": "https://leesburgcc.org",
        "services": "Sundays at 9:00 AM and 10:45 AM (Contemporary); 9:00 AM (Spanish)",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Cautious Commendation — Multi-Language, Community Church",
        "region": "dc-nova",
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
            "scripture": "Appears to be evangelical in doctrinal orientation. Explicit statement of faith on biblical inerrancy and authority should be verified directly on website.",
            "gender": "Nondenominational church — gender theology and ordination policy should be verified directly. Contemporary evangelical churches vary significantly.",
            "leadership": "Independent governance — no external denominational accountability. Elder/pastoral structure should be confirmed.",
            "cultural": "Leesburg/Loudoun County is a rapidly growing and diversifying DC suburb. The church's multi-language ministry (English/Spanish) reflects genuine missional engagement with the community.",
            "denomination": "Fully independent nondenominational — no external accountability structure."
        },
        "assessment": "Leesburg Community Church is a multi-congregation evangelical church in Leesburg, VA serving the growing Loudoun County community. Its Spanish-language ministry demonstrates genuine cross-cultural missions commitment. The church appears to be evangelical in orientation but as a nondenominational church, detailed doctrinal positions on Scripture, soteriology, and gender require direct verification. Leesburg/Loudoun County is one of the fastest-growing areas in the DC metro, and LCC appears to be actively engaging this growth. For men in the Leesburg/Lansdowne/Ashburn corridor: investigate their doctrinal statement, elder governance structure, and men's discipleship culture before committing. The multi-language ministry and community focus are positive signs of outward mission. Compare with Cornerstone Chapel (Leesburg) as another large regional option.",
        "tags": ["non-denom", "leesburg", "loudoun-county", "multi-language", "spanish", "nova", "community-church"],
        "gender_detail": "Verify gender theology and women in leadership policy directly with church leadership",
        "denomination_detail": "Independent nondenominational — no denominational affiliation or external accountability",
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
        "id": "grace-mosaic-dc",
        "name": "Grace Mosaic Church",
        "address": "1423 Girard Street NE, Washington, DC 20017",
        "pastor": "Lead Pastor (verify current at gracemosaic.org)",
        "pastor_credentials": "Evangelical church — verify pastoral credentials at gracemosaic.org",
        "founded": "Est. 2010s",
        "type": "Nondenominational Evangelical",
        "denomination": "Independent / Nondenominational",
        "website": "https://gracemosaic.org",
        "services": "Sundays — check website for current times",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Cautious Commendation — DC Urban Evangelical, Verify Doctrine",
        "region": "dc-nova",
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
            "scripture": "Evangelical in stated orientation — detailed statement of faith should be reviewed directly. Name suggests multi-ethnic/diverse church community focus.",
            "gender": "Nondenominational — gender theology and women in leadership must be verified directly. Urban evangelical churches in DC trend toward egalitarian positions.",
            "cultural": "NE Washington DC is a predominantly Black urban neighborhood. Multi-ethnic church focus reflects genuine engagement with DC's diverse community.",
            "denomination": "Independent nondenominational — verify elder governance structure and accountability mechanisms.",
            "mission": "Urban location and apparent multi-ethnic focus suggest active local mission engagement in DC neighborhoods."
        },
        "assessment": "Grace Mosaic Church is located in NE Washington, DC — a diverse urban neighborhood — and appears to be an evangelical congregation seeking to be both theologically grounded and culturally engaged in DC's multi-ethnic community. The 'Mosaic' name and NE DC location suggest intentional multi-ethnic ministry and neighborhood engagement. As a nondenominational church, direct verification of their doctrinal positions is essential — particularly on Scripture, soteriology, and gender roles. Urban evangelical churches in DC face significant cultural pressure toward progressive theological accommodation. For a man considering Grace Mosaic: review their statement of faith, ask about their view of Scripture's authority, and inquire about men's discipleship structure before committing. A promising urban church that warrants further investigation.",
        "tags": ["non-denom", "urban", "dc-ne", "multi-ethnic", "mosaic", "community-ministry"],
        "gender_detail": "Verify gender theology and women in ordination policy directly — urban evangelical context often trends egalitarian",
        "denomination_detail": "Independent nondenominational — no external denominational affiliation or accountability",
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
        "id": "washington-community-fellowship",
        "name": "Washington Community Fellowship",
        "address": "907 Maryland Avenue NE, Washington, DC 20002",
        "pastor": "Pastor (verify current — Mennonite-rooted community church)",
        "pastor_credentials": "Evangelical Mennonite / Anabaptist tradition",
        "founded": "Est. 1940s",
        "type": "Evangelical / Mennonite Tradition",
        "denomination": "Independent / Mennonite-rooted (verify current affiliation)",
        "website": "https://wcfchurch.org",
        "services": "Sundays at 9:30 AM (Nurture Hour) and 10:30 AM (Worship)",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Cautious Commendation — Anabaptist Heritage, Community-Focused",
        "region": "dc-nova",
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
            "scripture": "Mennonite/Anabaptist tradition is orthodox on Christology and typically holds Scripture in high regard, but hermeneutical approaches vary widely. Verify current doctrinal commitments.",
            "gender": "Mennonite tradition historically has more egalitarian views on women in ministry. Verify current policy on women in leadership at WCF specifically.",
            "cultural": "NE DC location — Capitol Hill area — creates both opportunities (congressional staffers, policy community) and pressures (progressive cultural accommodation).",
            "denomination": "Anabaptist heritage is one of the Reformation streams — distinct from Lutheran, Reformed, and Anglican. Emphasizes community, peace theology, discipleship. Verify current denominational or network affiliation.",
            "mission": "WCF's stated vision of 'formed by Jesus together for others' reflects genuine incarnational community mission. DC location provides significant missional opportunity."
        },
        "assessment": "Washington Community Fellowship is a long-standing evangelical congregation in NE Washington, DC (Capitol Hill area) with Mennonite/Anabaptist roots, describing itself as 'Christ-centered' and called to personal transformation, authentic community, and social impact. The Anabaptist tradition (Mennonite, Brethren) is one of the historic Reformation streams, historically emphasizing discipleship, community, peacemaking, and radical following of Jesus. Strengths: genuine community emphasis, NE DC neighborhood engagement, ecumenical but Christ-centered orientation. Cautions: Anabaptist traditions vary widely on Scripture's authority and gender roles; many Mennonite-affiliated churches have moved toward egalitarian and progressive positions. Review their current statement of faith, pastoral authority structure, and specific positions on gender and sexuality. A community-focused church with historic roots — warrants direct investigation.",
        "tags": ["anabaptist", "mennonite", "capitol-hill", "dc-ne", "community", "social-impact", "evangelical"],
        "gender_detail": "Mennonite/Anabaptist tradition tends toward egalitarian — verify women in leadership policy directly at WCF",
        "denomination_detail": "Independent/Mennonite-rooted evangelical community — verify current denominational affiliation at wcfchurch.org",
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
        "id": "redeeming-grace-church-fairfax",
        "name": "Redeeming Grace Church (Fairfax)",
        "address": "4101 Pickett Road, Fairfax, VA 22032",
        "pastor": "Justin Pearson (Lead Pastor)",
        "pastor_credentials": "M.Div. from Southern Baptist Theological Seminary; SBC-trained, Acts 29 / Sojourn Network background; church planter",
        "founded": "2021 (merger of Sojourn Fairfax and Redeeming Grace Church)",
        "type": "Southern Baptist (SBC)",
        "denomination": "Southern Baptist Convention (SBC) — SBC of Virginia",
        "website": "https://rgcfairfax.org",
        "services": "Sundays at 10:30 AM",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Recommended — SBC, Gospel-Centered, Expository Church",
        "region": "dc-nova",
        "scores": {
            "christology": "green",
            "scripture": "green",
            "gender": "green",
            "leadership": "green",
            "soteriology": "green",
            "cultural": "yellow",
            "denomination": "green",
            "preaching": "green",
            "mens": "green",
            "mission": "green"
        },
        "score_notes": {
            "cultural": "Fairfax is a high-pressure DC suburb. The church holds to biblical complementarianism but operates in a strongly egalitarian and progressive cultural environment.",
            "denomination": "SBC (Southern Baptist Convention) — conservative evangelical denomination. SBC has faced internal debates on gender, race, and abuse accountability in recent years but its confessional stance (Baptist Faith & Message 2000) remains biblically orthodox."
        },
        "assessment": "Redeeming Grace Church Fairfax was formed in 2021 through the merger of Sojourn Church Fairfax (Justin Pearson, planted 2012) and Redeeming Grace Church Fairfax. It is affiliated with the SBC of Virginia, grounding it in the Southern Baptist Convention's confessional framework (Baptist Faith & Message 2000). Justin Pearson planted and pastored Sojourn Fairfax through the Acts 29 and Sojourn Network. The merger created a stronger combined congregation in Fairfax County. SBC affiliation provides meaningful confessional accountability — BF&M 2000 affirms biblical inerrancy, complementarian gender theology, and exclusive salvation through Jesus Christ. For a man in the Fairfax/Burke/Springfield area wanting a SBC-affiliated, Gospel-centered church with solid preaching and discipleship culture, RGC Fairfax is a solid recommendation. Verify current elder structure and men's ministry programs directly.",
        "tags": ["sbc", "southern-baptist", "fairfax", "church-plant", "expository", "complementarian", "nova"],
        "gender_detail": "Male lead pastor; SBC affirms complementarian gender theology — male-only pastors/elders, women serve broadly in ministry",
        "denomination_detail": "Southern Baptist Convention (SBC) — largest Protestant denomination in US; confessionally conservative (Baptist Faith & Message 2000)",
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
        "id": "clarendon-presbyterian-church",
        "name": "Clarendon Presbyterian Church",
        "address": "1305 N. Jackson Street, Arlington, VA 22201",
        "pastor": "Pastor Alice (verify current pastor at clarendonpresbyterian.org)",
        "pastor_credentials": "PCUSA-ordained; egalitarian theological framework",
        "founded": "Est. 1920s",
        "type": "Presbyterian (PCUSA) — Progressive",
        "denomination": "Presbyterian Church (U.S.A.) — PCUSA",
        "website": "https://clarendonpresbyterian.org",
        "services": "Sundays at 10:00 AM (in-person and Zoom)",
        "has_mens_ministry": False,
        "has_kids_ministry": False,
        "overall_rating": "red",
        "overall_label": "Not Recommended — LGBTQ+ Affirming, PCUSA Liberal",
        "region": "dc-nova",
        "scores": {
            "christology": "yellow",
            "scripture": "red",
            "gender": "red",
            "leadership": "red",
            "soteriology": "red",
            "cultural": "red",
            "denomination": "red",
            "preaching": "red",
            "mens": "red",
            "mission": "red"
        },
        "score_notes": {
            "scripture": "PCUSA embraces progressive hermeneutics. Clarendon PC explicitly promotes LGBTQ+ inclusion as a core identity — rejecting biblical teaching on sexuality as binding.",
            "gender": "Clarendon explicitly identifies as LGBTQ+ affirming ('celebrating church community embracing those with faith and doubt'). Women as pastors/elders is standard. Same-sex marriage is affirmed.",
            "leadership": "Female pastor (Alice); explicitly LGBTQ+ affirming congregation. The church's self-description places inclusive identity above confessional doctrine.",
            "soteriology": "Progressive Presbyterian theology at this church level typically embraces pluralistic or inclusivist soteriology. Faith in Christ as the exclusive way of salvation is unlikely to be clearly proclaimed.",
            "cultural": "Full cultural accommodation to progressive values — LGBTQ+, progressive politics, social justice as primary identity rather than Gospel proclamation.",
            "mens": "No men's ministry structure; progressive theological framework undermines biblical masculine identity and discipleship."
        },
        "assessment": "Clarendon Presbyterian Church in Arlington explicitly markets itself as an 'LGBTQ+ celebrating church community' and identifies women in pastoral leadership as core to its identity. As a PCUSA congregation, it operates within a denomination that has formally abandoned the Westminster Confession of Faith on sexuality and gender (2015 vote on same-sex marriage, decades-long ordination of women). This is a straightforward not-recommended church for men seeking doctrinally sound, biblically faithful worship. The Word of God is clear on these matters (Romans 1:24-27; 1 Corinthians 6:9-11; 1 Timothy 2:12-14). Arlington has multiple sound evangelical and Reformed options including Redeemer Church of Arlington (Acts 29) and previously The Church at Clarendon. A man seeking genuine discipleship and biblical community should look elsewhere.",
        "tags": ["pcusa", "presbyterian", "lgbtq-affirming", "progressive", "arlington", "egalitarian", "not-recommended"],
        "gender_detail": "Female pastor; LGBTQ+ affirming congregation; no complementarian theology present",
        "denomination_detail": "PCUSA — liberal mainline Presbyterian denomination; Clarendon is among its most progressive congregations",
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
    "christology": ("Christology", "Biblical doctrine of Christ — deity, humanity, resurrection, return"),
    "scripture": ("Scripture & Authority", "Biblical inerrancy, sufficiency, and authority in faith and practice"),
    "gender": ("Gender & Leadership", "Complementarian theology — male-only eldership, biblical sexuality"),
    "leadership": ("Accountability Structure", "Denominational or elder oversight, governance, and transparency"),
    "soteriology": ("Soteriology", "Salvation by grace through faith in Christ alone"),
    "cultural": ("Cultural Resistance", "Ability to hold biblical positions under progressive cultural pressure"),
    "denomination": ("Denominational Health", "Orthodoxy of the broader denomination or network"),
    "preaching": ("Preaching Quality", "Expository, Christ-centered, Scripture-saturated preaching"),
    "mens": ("Men's Discipleship", "Robust men's ministry, accountability, and masculine spiritual formation"),
    "mission": ("Mission & Evangelism", "Commitment to local and global Great Commission ministry"),
}

BADGE_ICONS = {"green": "✅", "yellow": "⚠️", "red": "🚨", "black": "⬛"}
BADGE_LABELS = {"green": "Pass", "yellow": "Caution", "red": "Fail", "black": "N/A"}
OVERALL_ICONS = {"green": "✅", "yellow": "⚠️", "red": "🚨"}


def h(s):
    return html_mod.escape(str(s)) if s else ""


def render_page(c):
    name = c["name"]
    overall = c.get("overall_rating", "yellow")
    overall_label = c.get("overall_label", "")
    overall_icon = OVERALL_ICONS.get(overall, "⚠️")
    website = c.get("website", "#")
    address = c.get("address", "")
    pastor = c.get("pastor", "")
    pastor_creds = c.get("pastor_credentials", "")
    founded = c.get("founded", "")
    denom = c.get("denomination", "")
    church_type = c.get("type", "")
    services = c.get("services", "")
    has_mens = c.get("has_mens_ministry", False)
    has_kids = c.get("has_kids_ministry", False)

    # Map embed
    map_query = h(address).replace(" ", "+")
    map_url = f"https://www.google.com/maps/embed/v1/place?key=AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY&q={map_query}"

    # Score rows
    score_rows = ""
    scores = c.get("scores", {})
    score_notes = c.get("score_notes", {})
    gender_detail = c.get("gender_detail", "")
    for key, (label, desc) in SCORE_LABELS.items():
        val = scores.get(key, "yellow")
        icon = BADGE_ICONS.get(val, "⚠️")
        badge_label = BADGE_LABELS.get(val, "Caution")
        note = score_notes.get(key, "")
        note_html = f'<div class="score-note">{h(note)}</div>' if note else ""
        gd_html = f'<div class="gender-detail">👤 {h(gender_detail)}</div>' if key == "gender" and gender_detail else ""
        score_rows += f"""
    <div class="score-row">
      <div class="score-info">
        <span class="score-label">{h(label)}</span>
        <span class="score-desc">{h(desc)}</span>
        {note_html}
        {gd_html}
      </div>
      <span class="score-badge score-{val}">{icon} {badge_label}</span>
    </div>"""

    # Tags
    tags_html = "".join(f'<span class="tag">#{h(t)}</span>' for t in c.get("tags", []))

    # Engagement rows
    eng = c.get("engagement", {})
    eng_labels = {
        "visited_facility": "Visited Facility",
        "attended_services": "Attended Services",
        "viewed_online_services": "Viewed Online Services",
        "researched_website": "Researched Website",
        "know_members_personally": "Know Members Personally",
        "interacted_with_leadership": "Interacted with Leadership",
        "attended_personally": "Attended Personally",
    }
    eng_rows = ""
    for k, label in eng_labels.items():
        val = eng.get(k, False)
        icon = "✅" if val else "☐"
        css = "has-yes" if val else "has-no"
        eng_rows += f'<div class="fact-item"><span class="fact-label">{h(label)}</span><span class="fact-value {css}">{icon} {"Yes" if val else "Not yet"}</span></div>\n'

    has_mens_str = "Yes" if has_mens else "Not confirmed"
    has_kids_str = "Yes" if has_kids else "Not confirmed"

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
  <meta name="description" content="{h(name)} — Theological due diligence scorecard for Christian men in the DC/Northern Virginia area.">
  <meta property="og:title" content="{h(name)} — Church Directory | USMC Ministries">
  <meta property="og:description" content="10-point theological scorecard: {h(overall_label)}">
  <meta property="og:type" content="website">
  <title>{h(name)} — Church Directory | USMC Ministries</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  :root {{
    --bg: #000000; --bg-card: #111111; --gold: #D4AF37; --gold-light: #F4D470;
    --white: #e8e8e8; --gray: #888888; --gray-light: #aaaaaa; --border: #333333;
    --green: #4CAF50; --yellow: #FFC107; --red: #f44336;
    --green-bg: rgba(76,175,80,0.12); --yellow-bg: rgba(255,193,7,0.12); --red-bg: rgba(244,67,54,0.12);
  }}
  body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--white); line-height: 1.7; min-height: 100vh; }}
  h1, h2, h3, h4 {{ font-family: 'Playfair Display', serif; }}
  .top-nav {{ display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; padding: 14px 20px; border-bottom: 1px solid var(--border); background: rgba(0,0,0,0.95); position: sticky; top: 0; z-index: 100; }}
  .top-nav a {{ color: var(--gray); text-decoration: none; font-size: 0.85rem; font-weight: 500; padding: 5px 12px; border-radius: 20px; border: 1px solid transparent; transition: all 0.2s; white-space: nowrap; }}
  .top-nav a:hover {{ color: var(--gold); border-color: var(--border); }}
  .top-nav a:first-child {{ color: var(--gold); border-color: var(--border); }}
  .hero {{ padding: 48px 24px 36px; text-align: center; background: linear-gradient(180deg, rgba(212,175,55,0.08) 0%, transparent 100%); border-bottom: 1px solid var(--border); }}
  .hero h1 {{ font-size: clamp(1.6rem, 4vw, 2.6rem); color: var(--white); margin-bottom: 8px; letter-spacing: 0.5px; }}
  .hero h1 span {{ color: var(--gold); }}
  .hero .denom-tag {{ display: inline-block; background: rgba(212,175,55,0.1); border: 1px solid rgba(212,175,55,0.25); color: var(--gold-light); font-size: 0.75rem; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; padding: 3px 12px; border-radius: 20px; margin-bottom: 16px; }}
  .hero .address {{ color: var(--gray-light); font-size: 0.95rem; margin-bottom: 18px; }}
  .threat-badge {{ display: inline-flex; align-items: center; gap: 8px; padding: 8px 20px; border-radius: 8px; font-weight: 700; font-size: 0.95rem; letter-spacing: 0.5px; margin-top: 8px; border: 1.5px solid; }}
  .threat-badge.rating-green {{ background: rgba(76,175,80,0.18); border-color: var(--green); color: #7edd80; }}
  .threat-badge.rating-yellow {{ background: rgba(255,193,7,0.15); border-color: var(--yellow); color: #ffd85a; }}
  .threat-badge.rating-red {{ background: rgba(244,67,54,0.15); border-color: var(--red); color: #ff7c74; }}
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
  .score-row {{ display: grid; grid-template-columns: 1fr auto; gap: 12px; align-items: start; padding: 14px 0; border-bottom: 1px solid #1e1e1e; }}
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
  .note-block {{ padding: 14px 16px; border-radius: 8px; margin-bottom: 12px; border-left: 3px solid; font-size: 0.9rem; line-height: 1.7; }}
  .note-assessment {{ background: rgba(212,175,55,0.06); border-color: var(--gold); color: var(--gray-light); }}
  .note-tag-row {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; }}
  .tag {{ background: #1a1a1a; border: 1px solid #333; color: var(--gray); font-size: 0.72rem; padding: 3px 10px; border-radius: 20px; }}
  .map-wrap {{ border-radius: 8px; overflow: hidden; border: 1px solid var(--border); margin-bottom: 28px; }}
  .map-wrap iframe {{ width: 100%; height: 320px; border: 0; display: block; }}
  .btn-row {{ display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin-bottom: 28px; }}
  .btn-gold {{ background: var(--gold); color: #000; font-weight: 700; padding: 10px 24px; border-radius: 8px; text-decoration: none; font-size: 0.9rem; transition: all 0.2s; }}
  .btn-gold:hover {{ background: var(--gold-light); }}
  .btn-outline {{ border: 1.5px solid var(--border); color: var(--gray-light); padding: 10px 24px; border-radius: 8px; text-decoration: none; font-size: 0.9rem; transition: all 0.2s; }}
  .btn-outline:hover {{ border-color: var(--gold); color: var(--gold); }}
  .back-row {{ text-align: center; margin-top: 20px; }}
  .back-row a {{ color: var(--gray); font-size: 0.85rem; text-decoration: none; }}
  .back-row a:hover {{ color: var(--gold); }}
  footer {{ text-align: center; padding: 32px 24px; border-top: 1px solid var(--border); color: var(--gray); font-size: 0.82rem; }}
  footer a {{ color: var(--gold); text-decoration: none; }}
</style>
</head>
<body>
<nav class="top-nav">
  <a href="/churches.html">⛪ Church Directory</a>
  <a href="/index.html">📖 Bible Plan</a>
  <a href="/wheelhouse.html">⚓ Wheelhouse</a>
  <a href="/lexicon.html">📚 Lexicon</a>
</nav>

<div class="hero">
  <div class="denom-tag">{h(church_type)}</div>
  <h1><span>{h(name)}</span></h1>
  <div class="address">📍 {h(address)}</div>
  <div class="threat-badge rating-{overall}">
    <span class="threat-icon">{overall_icon}</span>
    <span>{h(overall_label)}</span>
  </div>
</div>

<div class="page-body">

  <!-- Quick Facts -->
  <div class="card">
    <div class="card-title">📋 Quick Facts</div>
    <div class="facts-grid">
      <div class="fact-item">
        <span class="fact-label">Pastor</span>
        <span class="fact-value">{h(pastor)}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Denomination</span>
        <span class="fact-value">{h(denom)}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Founded</span>
        <span class="fact-value">{h(founded)}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Services</span>
        <span class="fact-value">{h(services)}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Website</span>
        <span class="fact-value"><a href="{h(website)}" target="_blank" rel="noopener">{h(website)}</a></span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Men's Ministry</span>
        <span class="fact-value {'has-yes' if has_mens else 'has-no'}">{has_mens_str}</span>
      </div>
      <div class="fact-item">
        <span class="fact-label">Kids Ministry</span>
        <span class="fact-value {'has-yes' if has_kids else 'has-no'}">{has_kids_str}</span>
      </div>
      <div class="fact-item" style="grid-column: 1 / -1;">
        <span class="fact-label">Pastor Credentials</span>
        <span class="fact-value" style="color: var(--gray-light); font-size: 0.88rem;">{h(pastor_creds)}</span>
      </div>
    </div>
  </div>

  <!-- 10-Point Scorecard -->
  <div class="card">
    <div class="card-title">📊 10-Point Theological Scorecard</div>
    {score_rows}
  </div>

  <!-- Assessment / Notes -->
  <div class="card">
    <div class="card-title">📝 Assessment</div>
    <div class="note-block note-assessment">{h(c["assessment"])}</div>
    <div class="note-tag-row">{tags_html}</div>
  </div>

  <!-- Personal Engagement -->
  <div class="card">
    <div class="card-title">🎯 My Engagement</div>
    <p style="font-size:0.82rem; color:var(--gray-light); margin-bottom:16px;">Moop's personal engagement with this church — updated as visits and interactions occur.</p>
    <div class="facts-grid">
    {eng_rows}
    </div>
  </div>

  <!-- Map -->
  <div class="map-wrap">
    <iframe
      src="{map_url}"
      allowfullscreen="" loading="lazy"
      referrerpolicy="no-referrer-when-downgrade"
      title="Map for {h(name)}">
    </iframe>
  </div>

  <!-- Buttons -->
  <div class="btn-row">
    <a href="{h(website)}" target="_blank" rel="noopener" class="btn-gold">🌐 Visit Their Website</a>
    <a href="/churches.html" class="btn-outline">← Back to Church Directory</a>
  </div>

  <div class="back-row">
    <a href="/churches.html">← Return to Full Church Directory</a>
  </div>
</div>

<footer>
  <p>USMC Ministries Church Directory — Theological Due Diligence for Christian Men</p>
  <p style="margin-top:6px;"><a href="/churches.html">← All Churches</a> &nbsp;|&nbsp; <a href="/index.html">Bible Plan</a> &nbsp;|&nbsp; <a href="/wheelhouse.html">Wheelhouse</a></p>
</footer>
</body>
</html>"""


def main():
    out_dir = os.path.join(os.path.dirname(__file__), "..", "docs", "churches")
    json_path = os.path.join(os.path.dirname(__file__), "..", "docs", "data", "churches.json")

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
