#!/usr/bin/env python3
"""
Generate DC/NoVA church HTML pages from JSON data.
Run from repo root: python3 scripts/generate_dcnova_churches.py
"""

import json, os, re, html as html_mod
from datetime import date

CHURCHES = [
    {
        "id": "mclean-bible-church",
        "name": "McLean Bible Church",
        "address": "8925 Leesburg Pike, Vienna, VA 22182",
        "pastor": "Dr. David Platt (Lead Pastor)",
        "pastor_credentials": "B.A. University of Georgia; M.Div., Th.M., Ph.D. New Orleans Baptist Theological Seminary; former President, International Mission Board (SBC)",
        "founded": "1961",
        "type": "Nondenominational Evangelical",
        "denomination": "Independent / Nondenominational",
        "website": "https://mcleanbible.org",
        "services": "Sundays at 9:00 AM & 11:00 AM (multiple campuses: Tysons/Vienna, Arlington, Loudoun, Montgomery County)",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Cautious Commendation — Vetted Preacher, Watch Cultural Drift",
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
            "mens": "green",
            "mission": "green"
        },
        "score_notes": {
            "gender": "David Platt is complementarian in theology, but MBC faced controversy (2022) over leadership practices and lack of elder accountability. Large nondenominational church — gender stance depends heavily on current elder board.",
            "leadership": "No SBC or denominational accountability. Elder-governed, but past leadership controversies around Platt's tenure raised questions about elder oversight and transparency.",
            "cultural": "MBC is in the DC suburbs — high-pressure cultural context. Platt's preaching is solidly biblical, but the church operates in a highly progressive metro area. Watch for social justice drift in ministries.",
            "denomination": "Fully independent nondenominational — no external accountability structure. Leadership accountability is internal only."
        },
        "assessment": "David Platt is one of the most serious Bible expositors in America — author of 'Radical,' former IMB president, passionate for global missions. His preaching is Scripture-saturated and Christ-exalting. MBC is a large multi-campus church that reaches thousands in the DC metro area. Caution: the nondenominational structure means no external accountability, and the DC-area context creates constant pressure toward cultural accommodation. Platt himself has been involved in some controversy (2022 elder/governance disputes). Evaluate the local campus leadership, not just the platform pastor. For a man wanting solid Word ministry and global mission vision, MBC is worth attending — but watch the ministry culture, not just the Sunday sermon.",
        "tags": ["non-denom", "multi-campus", "expository", "david-platt", "missions", "dc-metro", "megachurch"],
        "gender_detail": "Male lead pastor (David Platt); elder-governed; complementarian in theology but nondenominational governance means no external gender policy accountability",
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
        "id": "capitol-hill-baptist-church",
        "name": "Capitol Hill Baptist Church",
        "address": "525 A Street NE, Washington, DC 20002",
        "pastor": "Dr. Mark Dever (Senior Pastor)",
        "pastor_credentials": "B.A. Duke University; M.Div. Gordon-Conwell Theological Seminary; Th.M. Southern Baptist Theological Seminary; Ph.D. Ecclesiastical History, Cambridge University",
        "founded": "1878",
        "type": "Southern Baptist",
        "denomination": "Southern Baptist Convention (SBC)",
        "website": "https://www.capitolhillbaptist.org",
        "services": "Sundays: Core Seminars 9:30 AM; Main Service 10:30 AM; Evening Prayer & Praise 5:00 PM",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Theological Alignment — Exemplary Church Health Model",
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
            "gender": "CHBC holds a clear complementarian position — male-only pastors and elders. Dever has written extensively on biblical manhood/womanhood and church polity.",
            "preaching": "Mark Dever is one of the foremost expository preachers in America, founder of 9Marks Ministries which exists to equip healthy churches worldwide.",
            "denomination": "SBC — Baptist Faith & Message 2000. Strong accountability, complementarian polity baked in.",
            "cultural": "Located in Washington DC, literally 6 blocks from the U.S. Capitol. Despite the pressure cooker environment, CHBC is known for holding firm on doctrine and refusing cultural capitulation."
        },
        "assessment": "Capitol Hill Baptist Church under Mark Dever is arguably the gold standard for Baptist church health in America. Dever founded 9Marks Ministries, wrote 'Nine Marks of a Healthy Church,' and has trained hundreds of pastors in biblical ecclesiology. CHBC is distinguished by its serious commitment to church membership, regenerate membership rolls, elder-led governance, verse-by-verse expository preaching, and robust congregational accountability. Six blocks from the U.S. Capitol in one of the most politically charged zip codes in America — and it holds the line. Sunday evening service (5 PM Prayer & Praise) is unusual and notable — a mark of serious congregational commitment. If you want to see what a doctrinally healthy Baptist church looks like in practice, CHBC is the blueprint.",
        "tags": ["sbc", "southern-baptist", "9marks", "mark-dever", "expository", "complementarian", "church-health", "dc"],
        "gender_detail": "Male-only pastors and elders (SBC — BF&M 2000 complementarian); Dever is a leading voice for biblical gender roles in the church",
        "denomination_detail": "Southern Baptist Convention — SBC of Virginia; strong accountability structure",
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
        "id": "the-falls-church-anglican",
        "name": "The Falls Church Anglican",
        "address": "6565 Arlington Blvd, Suite 300, Falls Church, VA 22042",
        "pastor": "The Rev. Samuel D. Ferguson (Rector, since 2019)",
        "pastor_credentials": "Drexel University (B.S.); ordained Anglican priest; served on staff since 2011 before becoming rector",
        "founded": "1734 (historic colonial parish; re-planted as Anglican after 2012 legal battle)",
        "type": "Anglican (ACNA)",
        "denomination": "Anglican Church in North America (ACNA) — Diocese of the Mid-Atlantic",
        "website": "https://tfcanglican.org",
        "services": "Sundays: 8:00 AM (Communion, Cranmer Chapel), 9:00 AM & 11:00 AM (Main Services)",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Theological Alignment — Historic Anglican Orthodoxy",
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
            "gender": "ACNA holds male-only ordination to the priesthood. TFC Anglican is complementarian in practice and theology. The church famously left The Episcopal Church (TEC) over its embrace of homosexuality and female ordination.",
            "denomination": "ACNA — Anglican Church in North America. Orthodox Anglican body formed in 2009 by congregations departing TEC over theological drift. Strong accountability and confessional standards (39 Articles, BCP).",
            "preaching": "The Falls Church Anglican has a legacy of expository preaching and serious biblical engagement dating back to John Wesley who preached here in the colonial era.",
            "cultural": "TFC left a denomination (TEC) over cultural capitulation — their departure cost them their historic building after a court battle. That willingness to lose property rather than compromise doctrine speaks volumes."
        },
        "assessment": "The Falls Church Anglican has one of the most remarkable stories in American Christianity. As one of America's oldest churches (1734), it separated from The Episcopal Church over homosexuality and women's ordination, fought a legal battle that cost them their historic building, and re-planted as a faithful Anglican congregation. They now worship at an office building — having chosen doctrinal integrity over real estate. Rector Sam Ferguson leads a congregation with deep roots in biblical Anglicanism, liturgical worship rooted in Scripture, and a legacy of sending. ACNA accountability, male-only priesthood, complementarian household vision. For a man who values covenantal worship, historic liturgy, and a congregation that has paid a price for orthodoxy — this is worth serious consideration.",
        "tags": ["anglican", "acna", "orthodox", "complementarian", "liturgical", "historic", "church-planting", "dc-nova"],
        "gender_detail": "Male-only ordination (ACNA policy); complementarian in doctrine and practice; left TEC specifically over female ordination and gay marriage",
        "denomination_detail": "ACNA — Diocese of the Mid-Atlantic; accountable to orthodox Anglican confessional standards (39 Articles, Book of Common Prayer)",
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
        "id": "immanuel-bible-church-springfield",
        "name": "Immanuel Bible Church",
        "address": "6911 Braddock Road, Springfield, VA 22151",
        "pastor": "Jesse Johnson (Teaching Pastor / Dean, The Master's Seminary DC)",
        "pastor_credentials": "The Master's Seminary; Dean of The Master's Seminary Washington DC campus; author of 'City of Man, Kingdom of God'; blogger at thecripplegate.com",
        "founded": "1964",
        "type": "Nondenominational Evangelical",
        "denomination": "Independent / Nondenominational (Master's Seminary affiliation)",
        "website": "https://immanuelbible.church",
        "services": "Sundays (multiple services — see website for current times)",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Theological Alignment — Master's Seminary Preaching Quality",
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
            "denomination": "Nondenominational — no external denominational accountability. However, the Master's Seminary affiliation provides strong theological oversight and confessional alignment with MacArthur's tradition.",
            "preaching": "Jesse Johnson is Dean of The Master's Seminary DC extension — trained under John MacArthur's model. Expect rigorous, verse-by-verse expository preaching. Sermons available on SermonAudio.",
            "gender": "Complementarian by conviction and Master's Seminary formation. Male-only pastors and elders. Hispanic congregation also present at same location.",
            "cultural": "IBC specifically calls out 'strong exegetical preaching' as identity marker — the antithesis of therapeutic, topical felt-needs preaching."
        },
        "assessment": "Immanuel Bible Church is a gem in Northern Virginia. Founded 1964, it's served the Springfield area for over 60 years with a consistent commitment to Scripture. Teaching Pastor Jesse Johnson is Dean of The Master's Seminary Washington DC campus — that's John MacArthur's seminary, and it means the preaching at IBC will be expository, word-saturated, and doctrinally serious. IBC also hosts a Hispanic congregation, which is a mark of genuine community engagement. For a man who wants a smaller-to-mid-size church with rigorous biblical preaching, discipleship infrastructure (small groups emphasized), and a clear theological north star — IBC is an excellent choice in the NoVA corridor.",
        "tags": ["non-denom", "expository", "masters-seminary", "jesse-johnson", "complementarian", "springfield", "nova"],
        "gender_detail": "Male-only pastors and elders; complementarian by conviction; Hispanic congregation also on campus",
        "denomination_detail": "Independent nondenominational — affiliated with The Master's Seminary tradition (John MacArthur); no formal denominational structure",
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
        "id": "national-community-church-dc",
        "name": "National Community Church",
        "address": "700 M Street SE, Washington, DC 20003 (multiple campuses)",
        "pastor": "Dr. Mark Batterson (Lead Pastor)",
        "pastor_credentials": "Central Bible College (B.A.); M.Div. from a pentecostal seminary; author of 'The Circle Maker,' 'In a Pit with a Lion,' and 20+ books; NYT bestselling author",
        "founded": "1996",
        "type": "Assemblies of God / Pentecostal Multi-Site",
        "denomination": "Assemblies of God USA",
        "website": "https://national.cc",
        "services": "Sundays: 9:00 AM & 11:00 AM (multiple DC/NoVA campuses)",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — Solid Gospel Emphasis, Charismatic Framework",
        "region": "dc-nova",
        "scores": {
            "christology": "green",
            "scripture": "yellow",
            "gender": "yellow",
            "leadership": "yellow",
            "soteriology": "yellow",
            "cultural": "yellow",
            "denomination": "yellow",
            "preaching": "yellow",
            "mens": "yellow",
            "mission": "green"
        },
        "score_notes": {
            "scripture": "Assemblies of God affirms Scripture inerrancy, but charismatic framework adds extra-biblical 'words of knowledge,' prophecy, and experience-driven spirituality that can compete with Scripture's authority.",
            "gender": "Assemblies of God historically has allowed women in pastoral roles. NCC's stance on female senior pastors/elders needs individual verification — Batterson is complementarian but AoG doesn't require it.",
            "soteriology": "AoG affirms faith alone for salvation (sola fide), but may add 'second blessing' / baptism of the Holy Spirit with tongues as normative expectation. Salvation clearly gospel-centered but framework can add layers.",
            "denomination": "Assemblies of God — provides accountability, but AoG's charismatic framework introduces tensions around gender roles and extra-biblical spiritual gifts.",
            "preaching": "Batterson is a gifted communicator and visionary thinker. However, his style is more topical/narrative than expository. He's an ideas guy and cultural connector, not a verse-by-verse expositor.",
            "cultural": "NCC operates in the DC political ecosystem and intentionally engages culture — both a strength (marketplace presence) and risk (drift). Language around 'justice' should be evaluated.",
            "mens": "NCC has life groups and men's engagement, but no dedicated men's discipleship infrastructure as the primary vehicle."
        },
        "assessment": "National Community Church under Mark Batterson is culturally influential, evangelistically aggressive, and Batterson himself is clearly Christ-centered in his books and preaching. NCC is known for meeting in movie theaters, Ebenezers Coffeehouse (their ministry-owned coffee shop), and reaching young professionals in DC. The Assemblies of God affiliation provides structure and accountability. However: AoG's charismatic framework, Batterson's topical preaching style, and the DC-area cultural pressure points are real concerns for a man wanting deep doctrinal formation. Visit with discernment. NCC is a good entry point for unchurched people and city engagement, but may not be the primary spiritual food source for a man wanting expository depth.",
        "tags": ["assemblies-of-god", "pentecostal", "multi-campus", "mark-batterson", "charismatic", "dc", "marketplace-ministry"],
        "gender_detail": "AoG allows women in ministry roles — NCC's specific elder/pastoral gender policy needs verification; Batterson is personally complementarian but AoG denominational policy allows female ordination",
        "denomination_detail": "Assemblies of God USA — provides accountability but within charismatic theological framework",
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
        "id": "columbia-baptist-church-falls-church",
        "name": "Columbia Baptist Church",
        "address": "103 West Columbia Street, Falls Church, VA 22046",
        "pastor": "Dr. Jim Baucom (Senior Pastor)",
        "pastor_credentials": "Senior Pastor; pastoral leadership background; long-serving at Columbia",
        "founded": "Est. early 20th century (Falls Church area SBC church)",
        "type": "Southern Baptist",
        "denomination": "Southern Baptist Convention (SBC)",
        "website": "https://columbia.church",
        "services": "Multiple weekend services including Saturday evening and Sunday services; see website for current times",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Theological Alignment — SBC Accountability, Multi-Service",
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
            "mens": "yellow",
            "mission": "green"
        },
        "score_notes": {
            "cultural": "Falls Church, VA is a progressive-leaning municipality — SBC churches in NoVA face significant cultural pressure. Verify that cultural accommodation hasn't crept into programming or language.",
            "mens": "Large multi-service church — men's ministry programming should be confirmed directly with the church. The size and resources suggest it exists but specifics need verification.",
            "denomination": "SBC — Baptist Faith & Message 2000 complementarian accountability. BGAV (Baptist General Association of Virginia) affiliate."
        },
        "assessment": "Columbia Baptist Church is a well-established SBC congregation in Falls Church with a multi-service model serving the NoVA community. Dr. Jim Baucom leads with an executive director (Brett Flanders) supporting operations — a sign of a well-structured, resource-rich church. The SBC affiliation provides theological accountability with the Baptist Faith & Message 2000 framework: male-only pastors, inerrancy, evangelism focus. Columbia's NoVA location means they minister in a high-density, politically progressive context — which creates both opportunity (reach) and risk (drift). For a man in Falls Church or the Arlington/McLean corridor, Columbia Baptist is a solid landing spot with SBC credibility and size to support robust ministry programs.",
        "tags": ["sbc", "southern-baptist", "falls-church", "nova", "multi-service", "complementarian"],
        "gender_detail": "Male-only pastors and elders (SBC — Baptist Faith & Message 2000); complementarian church governance",
        "denomination_detail": "Southern Baptist Convention — BGAV affiliate; strong complementarian and inerrancy accountability",
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
        "id": "cornerstone-chapel-leesburg",
        "name": "Cornerstone Chapel",
        "address": "650 Battlefield Parkway SE, Leesburg, VA 20175",
        "pastor": "Gary Hamrick (Senior Pastor, since 1991 founding)",
        "pastor_credentials": "Founded Cornerstone Chapel in 1991 with 18 charter members; over 30 years of pastoral leadership; known for expository Bible teaching through books of the Bible",
        "founded": "1991",
        "type": "Calvary Chapel Association / Nondenominational",
        "denomination": "Calvary Chapel Association",
        "website": "https://cornerstonechapel.net",
        "services": "Sundays (multiple services, see website); Wednesday evenings 7:00 PM (Gary Hamrick teaching)",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Alignment — Verse-by-Verse Bible Teaching, 30+ Year Track Record",
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
            "denomination": "Calvary Chapel Association — provides loose accountability and fellowship but less formal than SBC or Presbyterian structures. Calvary Chapel tradition is consistent on male-only pastors and verse-by-verse teaching.",
            "preaching": "Gary Hamrick teaches verse-by-verse through entire books of the Bible — Wednesday night services are particularly known for deep, chapter-by-chapter exposition. This is the Calvary Chapel DNA.",
            "gender": "Calvary Chapel tradition is complementarian — male pastors and elders. Hamrick has been consistent on biblical gender roles throughout his 30+ year ministry.",
            "cultural": "Cornerstone Chapel is located in Leesburg (more conservative NoVA corridor) — less cultural pressure than Arlington/DC proper. Hamrick is known for speaking plainly on cultural issues from Scripture."
        },
        "assessment": "Cornerstone Chapel under Gary Hamrick is one of the strongest Bible-teaching churches in Northern Virginia. Founded in 1991 with 18 charter members, Hamrick has grown it into a thriving congregation through verse-by-verse exposition through every book of the Bible — the Calvary Chapel way. His Wednesday night teaching is particularly notable: a mid-week deep dive that many men would find more satisfying than a typical Sunday service. 30+ years of consistent, doctrinally sound, culturally clear pastoral leadership is rare and valuable. The Calvary Chapel association maintains complementarian polity and a high view of Scripture. For a man in Loudoun County or the western NoVA corridor, Cornerstone Chapel is a top-tier option. Note: task brief mentioned 'Skip Heitzig' — that is Pastor Skip Heitzig of Calvary Church in Albuquerque, NM. Gary Hamrick is Cornerstone Chapel's pastor.",
        "tags": ["calvary-chapel", "gary-hamrick", "expository", "verse-by-verse", "leesburg", "loudoun-county", "nova"],
        "gender_detail": "Male-only pastors and elders (Calvary Chapel tradition); complementarian by conviction; Hamrick has been consistent on gender roles for 30+ years",
        "denomination_detail": "Calvary Chapel Association — loose fellowship/accountability; less formal than SBC but consistent on theological essentials",
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
        "id": "restoration-city-church-arlington",
        "name": "Restoration City Church",
        "address": "Gunston Middle School, Arlington, VA (mailing: PO Box 7418, Arlington, VA 22207)",
        "pastor": "John McGowan (Lead Pastor / Church Planter)",
        "pastor_credentials": "7 years college ministry leadership; 3 years teaching pastor young adults ministry; 1-year church planting residency with The Summit Church (J.D. Greear); planted Restoration City",
        "founded": "2015 (church plant from Summit Church network)",
        "type": "Southern Baptist / Church Plant",
        "denomination": "Southern Baptist Convention (SBC of Virginia)",
        "website": "https://restorationcity.church",
        "services": "Sundays at 10:00 AM at Gunston Middle School, Arlington, VA",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Alignment — Gospel-Centered SBC Church Plant",
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
            "denomination": "SBC of Virginia — Summit Church planting network (J.D. Greear). Strong Great Commission accountability with church-planting DNA built in.",
            "preaching": "John McGowan trained through Summit Church's church planting residency — Summit is known for expository, gospel-centered preaching in the 9Marks tradition.",
            "cultural": "Arlington, VA is one of the most progressive zip codes in the country. RCC plants into hostile territory with a clear gospel — that takes courage and doctrinal clarity.",
            "mission": "RCC's mission language ('see people restored by Jesus') is explicitly Christocentric. Church planting DNA from Summit means multiplying churches is built into the vision.",
            "mens": "Elder/pastor leadership with covenant membership model (per website) — evidence of healthy ecclesiology that produces serious male discipleship."
        },
        "assessment": "Restoration City Church is a young, growing SBC church plant in Arlington, VA — one of the toughest ministry environments in America (heavily progressive, young professional population). Lead pastor John McGowan trained through The Summit Church (J.D. Greear) planting residency, giving him 9Marks-adjacent ecclesiological formation. The church meets at a middle school — a sign of missional flexibility and willingness to sacrifice comfort for reach. Covenant membership model and elder-led structure signal serious ecclesiology. For a man wanting a younger, doctrinally serious, Great Commission-focused church in the Arlington/DC corridor, Restoration City is an excellent choice. Small enough for genuine community; serious enough theologically.",
        "tags": ["sbc", "church-plant", "summit-church", "arlington", "dc-metro", "gospel-centered", "covenant-membership"],
        "gender_detail": "Male-only pastors and elders (SBC — BF&M 2000); elder-led governance; covenant membership model",
        "denomination_detail": "SBC of Virginia — Summit Church planting network; strong accountability and Great Commission focus",
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
        "id": "church-at-clarendon-arlington",
        "name": "The Church at Clarendon",
        "address": "1210 North Highland Street, Arlington, VA 22201",
        "pastor": "Pastor Danielle Bridgeforth (Senior Pastor)",
        "pastor_credentials": "Senior Pastor at The Church at Clarendon; preaching ministry focused on biblical relevance and community engagement",
        "founded": "Est. (First Baptist Church of Clarendon heritage)",
        "type": "Baptist / American Baptist",
        "denomination": "American Baptist Churches (ABC)",
        "website": "https://www.1bc.org",
        "services": "Sundays: 9:00 AM (Adults), 9:15 AM (Children, twice monthly); Wednesday evenings (Bible study)",
        "has_mens_ministry": False,
        "has_kids_ministry": True,
        "overall_rating": "red",
        "overall_label": "Not Recommended — Female Senior Pastor, Doctrinal Concerns",
        "region": "dc-nova",
        "scores": {
            "christology": "green",
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
            "gender": "Senior Pastor Danielle Bridgeforth is a woman — a clear violation of the biblical pattern of male-only pastoral eldership (1 Tim 2:12, 3:1-7; Titus 1:6). This is a disqualifying marker for a church committed to biblical complementarianism.",
            "leadership": "Female senior pastor is the leadership structure — incompatible with a male-elder-only ecclesiology. No indication of a qualifying male elder board.",
            "denomination": "American Baptist Churches USA (ABC) — not to be confused with SBC. ABC is a theologically moderate-to-liberal denomination that ordains women and has significant theological diversity within its membership.",
            "cultural": "Described as 'amazingly diverse' with culturally relevant preaching style — in the progressive Arlington context, this language often signals accommodation rather than confrontation of cultural norms.",
            "mens": "No dedicated men's ministry found. Female lead pastor context makes robust biblical men's discipleship unlikely.",
            "soteriology": "ABC does not have a uniform confession of faith — theological positions on salvation vary by congregation. Without verification, soteriology cannot be confirmed."
        },
        "assessment": "The Church at Clarendon has a female senior pastor — Pastor Danielle Bridgeforth — which places it outside the bounds of biblical complementarianism (1 Tim 2:12; 3:1-7). The American Baptist Churches USA (ABC) denomination is theologically moderate-to-liberal and affirms women's ordination, contrasting sharply with the SBC's Baptist Faith & Message 2000. The church may have sincere believers and Christ-centered sermons, but the pastoral leadership structure contradicts clear New Testament instruction on male-only elder/pastor roles. For a man serious about building his spiritual life in a doctrinally sound environment, The Church at Clarendon is not recommended as a primary home church.",
        "tags": ["abc", "american-baptist", "arlington", "female-pastor", "not-recommended", "moderate-liberal"],
        "gender_detail": "Female senior pastor (Danielle Bridgeforth) — ABC denomination affirms women's ordination; incompatible with male-elder-only ecclesiology",
        "denomination_detail": "American Baptist Churches USA (ABC) — theologically moderate; affirms female ordination; distinct from SBC",
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
        "id": "del-ray-baptist-church-alexandria",
        "name": "Del Ray Baptist Church",
        "address": "2405 Russell Road, Alexandria, VA 22301",
        "pastor": "Garrett Kell (Pastor)",
        "pastor_credentials": "Reformed Baptist pastor; Council member of The Gospel Coalition; known for pastoral counseling, expository preaching, and leadership in gospel-centered circles",
        "founded": "Established (Del Ray neighborhood historic Baptist church)",
        "type": "Southern Baptist",
        "denomination": "Southern Baptist Convention (SBC of Virginia)",
        "website": "https://www.delraybaptist.org",
        "services": "Sundays: multiple services (see website; typically 9:00 AM & 11:00 AM)",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Theological Alignment — Gospel-Centered, TGC-Connected Pastor",
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
            "preaching": "Garrett Kell is a Council member of The Gospel Coalition — he runs in circles with Tim Keller, D.A. Carson, John Piper alumni. Expect expository, gospel-saturated preaching.",
            "denomination": "SBC of Virginia — BF&M 2000 complementarian accountability.",
            "gender": "SBC complementarian — male-only pastors. Kell himself is a clear complementarian voice in his writing and ministry.",
            "cultural": "Del Ray is an Alexandria neighborhood with significant progressive demographics. DRBC holds the line doctrinally while engaging the community — a sign of missional courage.",
            "soteriology": "Reformed-leaning (Kell's TGC connections) — faith alone, grace alone, Christ alone, clearly articulated."
        },
        "assessment": "Del Ray Baptist Church under Garrett Kell is a doctrinally serious, gospel-centered SBC church in the Del Ray neighborhood of Alexandria. Kell's Gospel Coalition Council membership signals that he's in the network of serious expositors and reformed-leaning evangelicals. DRBC self-describes as 'Bible-teaching, Gospel-centered, Christ-exalting, God-glorifying' — exactly the right markers. The Alexandria context (diverse, historically rich neighborhood) gives the church missional opportunity without compromising doctrinal integrity. Kell is known for pastoral warmth combined with theological seriousness — the combination that builds men. A strong choice for a man in the Alexandria/Arlington corridor.",
        "tags": ["sbc", "southern-baptist", "gospel-coalition", "garrett-kell", "expository", "reformed", "alexandria", "nova"],
        "gender_detail": "Male-only pastors and elders (SBC BF&M 2000); Garrett Kell is a clear complementarian in his preaching and writing",
        "denomination_detail": "Southern Baptist Convention — SBC of Virginia; Gospel Coalition-adjacent theological orientation",
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
        "id": "truro-anglican-church-fairfax",
        "name": "Truro Anglican Church",
        "address": "10520 Main Street, Fairfax, VA 22030",
        "pastor": "Rev. Jamie Brown (Rector, since September 2022)",
        "pastor_credentials": "B.A. Psychology, George Mason University; M.A. Religion, Reformed Theological Seminary; ordained priest, Anglican Church in North America (ACNA)",
        "founded": "1843 (historic Fairfax Anglican parish; joined ACNA after departing TEC)",
        "type": "Anglican (ACNA)",
        "denomination": "Anglican Church in North America (ACNA) — Diocese of the Mid-Atlantic",
        "website": "https://truroanglican.com",
        "services": "Sundays: 7:30 AM, 9:00 AM & 11:00 AM (see website for current schedule)",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Theological Alignment — Historic ACNA Parish, Reformed Anglican",
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
            "denomination": "ACNA — Anglican Church in North America. Truro is a historic parish that departed The Episcopal Church over theological drift on human sexuality and female ordination. ACNA maintains 39 Articles and Book of Common Prayer confessional accountability.",
            "gender": "ACNA male-only ordination policy. Truro specifically departed TEC over female ordination and homosexuality — gender clarity is core to their identity.",
            "preaching": "Rector Jamie Brown has Reformed theological training (RTS) — expect Scripture-saturated, theologically grounded preaching in the Anglican liturgical tradition.",
            "mission": "Truro founded The Lamb Center in 1992 — a local ministry to the homeless. Decades of community mission built into church DNA.",
            "cultural": "Like TFC Anglican, Truro paid a price to leave TEC — that institutional courage signals a congregation willing to take costly positions."
        },
        "assessment": "Truro Anglican Church is one of the great orthodox Anglican congregations in Northern Virginia. Founded 1843, it has a rich history including connection to national leaders (George Mason was a parishioner of the historic Truro parish). After departing The Episcopal Church over homosexuality and female ordination, Truro joined ACNA and has continued its legacy of faithful biblical Anglicanism. Rector Jamie Brown (since 2022) brings Reformed theological training from RTS combined with Anglican liturgical practice. The Lamb Center (founded 1992 by Truro) demonstrates a long legacy of gospel-motivated community service. Three Sunday services, including an early service — a sign of serious congregational life. For a man wanting orthodox Anglican liturgy, doctrinal clarity, and a congregation with institutional courage, Truro Anglican is excellent.",
        "tags": ["anglican", "acna", "orthodox", "complementarian", "fairfax", "reformed", "liturgical", "historic"],
        "gender_detail": "Male-only ordination (ACNA policy); Truro departed TEC specifically over female ordination — gender clarity is central to their identity",
        "denomination_detail": "ACNA — Diocese of the Mid-Atlantic; 39 Articles and Book of Common Prayer confessional accountability",
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
        "id": "burke-community-church",
        "name": "Burke Community Church",
        "address": "9900 Old Keene Mill Road, Burke, VA 22015",
        "pastor": "Dr. Marty Baker (Senior Pastor)",
        "pastor_credentials": "B.A. Religion, Azusa Pacific University; Th.M. Old Testament, Dallas Theological Seminary; D.Min. Apologetics, Southern Evangelical Seminary; 30+ years pastoral experience",
        "founded": "Est. (long-standing Burke area nondenominational church)",
        "type": "Nondenominational Evangelical",
        "denomination": "Independent / Nondenominational",
        "website": "https://www.burkecommunity.com",
        "services": "Sundays at 9:00 AM & 10:45 AM",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Alignment — Dallas Seminary Pedigree, Solid Expository Preaching",
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
            "denomination": "Nondenominational — no external denominational accountability. However, Dr. Baker's Dallas Theological Seminary (DTS) Th.M. and Southern Evangelical D.Min. represent strong Reformed/conservative evangelical formation.",
            "preaching": "Dallas Seminary Th.M. in Old Testament combined with D.Min. in Apologetics — Dr. Baker is equipped for serious expository, theologically grounded preaching. 30+ years of track record.",
            "gender": "Nondenominational, but Baker's DTS and Southern Evangelical formation are complementarian. Staff page shows 'Senior Pastor' as male-led; Women's Ministry Director is female (appropriate complementarian structure).",
            "mission": "BCC hosted GO Conference 2025 (May) — a DC-area missions conference — indicating active Great Commission engagement."
        },
        "assessment": "Burke Community Church under Dr. Marty Baker is a nondenominational evangelical church with impressive pastoral credentials. A Dallas Theological Seminary Th.M. in Old Testament and a Southern Evangelical Seminary D.Min. in Apologetics — that's serious academic formation in a conservative evangelical tradition. Baker has served over 30 years, which means this is not a personality-driven flash-in-the-pan; it's a stable, long-tenured pastoral ministry. BCC is known for its 'family feel' in a church that serves a community area effectively. Two Sunday services, men's and women's ministry infrastructure, and hosting a regional missions conference all signal a healthy, outward-focused congregation. For a man in Burke, Fairfax County, or Springfield, BCC is a strong nondenominational option.",
        "tags": ["non-denom", "dallas-seminary", "apologetics", "marty-baker", "expository", "burke", "fairfax-county", "nova"],
        "gender_detail": "Male senior pastor; Women's Ministry Director (female, appropriate complementarian structure); DTS/Southern Evangelical formation is complementarian",
        "denomination_detail": "Independent nondenominational — no formal denominational structure; conservative evangelical by formation (DTS, Southern Evangelical)",
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
        "id": "reston-bible-church",
        "name": "Reston Bible Church",
        "address": "45650 Oakbrook Court, Dulles (Sterling), VA 20166",
        "pastor": "Jim Supp (Senior Teaching Pastor)",
        "pastor_credentials": "Senior Teaching Pastor; founded 1975 by Mike Minter (Pastor Emeritus); Supp succeeded Minter as primary teaching leader",
        "founded": "1975",
        "type": "Nondenominational Evangelical",
        "denomination": "Independent / Nondenominational",
        "website": "https://www.restonbible.org",
        "services": "Sundays at 9:00 AM & 10:45 AM (per Yelp/schedule info)",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Alignment — 50-Year Bible Teaching Legacy, Missions-Focused",
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
            "denomination": "Nondenominational — no external denominational accountability. However, 50 years of ministry history with a consistent biblical focus provides institutional stability.",
            "preaching": "Founded on biblical preaching as the core ministry — 'know Christ and make Him known' through 'biblical preaching, teaching, and authentic Christian community.' Jim Supp continues this tradition.",
            "mission": "Explicit worldwide mission focus baked into the church's core mission statement — Northern Virginia AND around the world.",
            "mens": "Fellowship groups and small group infrastructure — men's discipleship through community is emphasized. Verify dedicated men's ministry with the church directly."
        },
        "assessment": "Reston Bible Church has 50+ years of consistent Bible-teaching ministry in Northern Virginia — founded 1975 by Mike Minter, whose legacy continues under Senior Teaching Pastor Jim Supp. The church is officially located in Dulles/Sterling (the Oakbrook Court address) though still widely known as 'Reston Bible.' RBC's stated purpose — 'know Christ and make Him known through biblical preaching, teaching, and authentic Christian community in Northern Virginia and around the world' — is a solid evangelical mission statement. Two Sunday services, community groups infrastructure, and a strong local/global mission orientation. For a man in the Reston, Herndon, Sterling, or Ashburn corridor, RBC is a proven, established option with deep community roots and consistent biblical teaching.",
        "tags": ["non-denom", "expository", "reston", "nova", "missions", "50-year-legacy", "dulles-corridor"],
        "gender_detail": "Male senior pastor (Jim Supp); nondenominational with conservative evangelical orientation; complementarian in practice",
        "denomination_detail": "Independent nondenominational — 50-year track record provides institutional stability without formal denominational accountability",
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
        "id": "centreville-baptist-church",
        "name": "Centreville Baptist Church",
        "address": "15100 Lee Highway, Centreville, VA 20120",
        "pastor": "Josh Vincent (Pastor)",
        "pastor_credentials": "SBC-trained pastor; leading CBC's disciple-making discipleship model",
        "founded": "Established (long-standing Centreville area SBC church)",
        "type": "Southern Baptist",
        "denomination": "Southern Baptist Convention (SBC of Virginia)",
        "website": "https://centrevillebaptist.org",
        "services": "Sundays: Community Groups & Equip Classes 9:00 AM; Worship Gathering 10:30 AM",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "green",
        "overall_label": "Strong Alignment — SBC Church with Disciple-Making DNA",
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
            "denomination": "SBC of Virginia — Baptist Faith & Message 2000 complementarian accountability.",
            "preaching": "CBC's mission — 'glorifying God by making disciple-making disciples' — is a multiplication-oriented Great Commission framework. Preaching serves disciple-making, not entertainment.",
            "mission": "The disciple-making language is core to CBC's identity — not just personal discipleship but disciples who make disciples. Strong multiplicative mission DNA.",
            "mens": "Community Groups structure and 'Equip Classes' before the main service signal serious investment in formation infrastructure for men and families.",
            "cultural": "Centreville is a diverse, increasingly competitive suburb — SBC church holding the line doctrinally in a challenging context."
        },
        "assessment": "Centreville Baptist Church under Pastor Josh Vincent is a solid SBC congregation with a clear disciple-making mission: 'glorifying God by making disciple-making disciples.' That's not just a slogan — the Sunday structure (Community Groups + Equip Classes at 9 AM before the 10:30 AM worship gathering) shows a church that takes formation seriously, not just attendance. SBC of Virginia affiliation provides BF&M 2000 accountability on gender, soteriology, and Scripture. For a man in Centreville, Chantilly, or the Route 29/Lee Highway corridor, CBC is a strong choice with clear mission identity and solid evangelical foundations. The disciple-making language is exactly the right frame for a man wanting a church that will develop him, not just entertain him.",
        "tags": ["sbc", "southern-baptist", "disciple-making", "centreville", "nova", "community-groups", "complementarian"],
        "gender_detail": "Male-only pastors and elders (SBC BF&M 2000); complementarian church governance",
        "denomination_detail": "Southern Baptist Convention — SBC of Virginia; strong accountability structure with BF&M 2000 confessional baseline",
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
        "id": "grace-covenant-church-chantilly",
        "name": "Grace Covenant Church — Chantilly Campus",
        "address": "4600 Brookfield Corporate Drive, Chantilly, VA 20151",
        "pastor": "Multi-campus church — Chantilly campus pastor under GCC leadership network",
        "pastor_credentials": "Grace Covenant Church is an Every Nation Churches affiliate with multiple DC-area campuses (Chantilly, Sterling, Latino, Korean, Capitol Hill, Brookland, Georgetown, Tenleytown, East River)",
        "founded": "Est. (multi-campus church with DC-area roots)",
        "type": "Every Nation Churches / Charismatic Evangelical",
        "denomination": "Every Nation Churches (global charismatic network)",
        "website": "https://www.gracecov.org",
        "services": "Sundays: 9:00 AM & 11:00 AM; Wednesdays: 7:00 PM",
        "has_mens_ministry": True,
        "has_kids_ministry": True,
        "overall_rating": "yellow",
        "overall_label": "Caution — Every Nation Affiliation, Charismatic Framework, Diversity Emphasis",
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
            "denomination": "Every Nation Churches — global charismatic/evangelical network. Has faced historical scrutiny around authoritarian leadership models and high-control church culture in some regions. The DC/NoVA expression may differ significantly from global patterns.",
            "scripture": "Charismatic framework with emphasis on prophecy, tongues, and extra-biblical spiritual experience. Scripture inerrancy affirmed, but experiential elements can compete with Scripture's final authority.",
            "gender": "Every Nation Churches historically has allowed women in various ministry roles. Campus pastor gender and elder composition needs local verification. The Chantilly campus men's outreach event ('men of Grace and their sons') suggests some intentional male leadership.",
            "cultural": "Grace Covenant explicitly identifies as 'multi-cultural, multi-ethnic, multi-generational' and describes itself as wanting to look like 'Heaven' — this language can be gospel-driven or DEI-driven; context and preaching content determine which.",
            "preaching": "Every Nation charismatic context typically produces more topical/vision-casting preaching than verse-by-verse exposition. Verify with the Chantilly campus specifically.",
            "mens": "Men's events mentioned (men + sons cleanup day) — positive sign. Dedicated men's discipleship needs verification."
        },
        "assessment": "Grace Covenant Church Chantilly is part of the Every Nation Churches global network — a charismatic evangelical movement with significant presence in campus ministry (Victory Youth/Every Nation Campus) and multi-ethnic church planting. The positive: clear gospel proclamation, multi-campus reach, men's engagement events, and multiple Sunday services signal an active congregation. The concerns: Every Nation has faced scrutiny globally for authoritarian leadership and high-control church culture (less relevant in a US suburban context, but worth knowing); the charismatic framework introduces extra-biblical spiritual practices; and the diversity-first language ('looks like Heaven') needs examination to ensure gospel-centrality drives it. Visit with discernment and evaluate Chantilly campus leadership specifically — multi-campus networks can vary significantly by campus.",
        "tags": ["every-nation", "charismatic", "multi-campus", "multi-ethnic", "chantilly", "nova", "cautious-commendation"],
        "gender_detail": "Every Nation allows women in ministry — verify Chantilly campus elder/pastor composition; men's events suggest intentional male engagement but full complementarian framework unclear",
        "denomination_detail": "Every Nation Churches — global charismatic network; US expression generally more evangelical than some international counterparts",
        "engagement": {
            "visited_facility": False,
            "attended_services": False,
            "viewed_online_services": False,
            "researched_website": False,
            "know_members_personally": False,
            "interacted_with_leadership": False,
            "attended_personally": False
        }
    }
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

    # Build scorecard rows
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

    # Tags
    tags_html = "".join(f'<span class="tag">#{t}</span>' for t in c.get("tags", []))

    # Engagement rows
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

    # Map iframe — encode address for URL
    map_addr = address.replace('"', '').replace("'", "")
    map_url = f"https://maps.google.com/maps?q={map_addr.replace(' ', '%20')}&output=embed"

    # Quick facts
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
  <meta name="description" content="{name} — Theological due diligence scorecard for Christian men in the DC/Northern Virginia area.">
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
    --bg: #000000;
    --bg-card: #111111;
    --gold: #D4AF37;
    --gold-light: #F4D470;
    --white: #e8e8e8;
    --gray: #888888;
    --gray-light: #aaaaaa;
    --border: #333333;
    --green: #4CAF50;
    --yellow: #FFC107;
    --red: #f44336;
    --green-bg: rgba(76,175,80,0.12);
    --yellow-bg: rgba(255,193,7,0.12);
    --red-bg: rgba(244,67,54,0.12);
    --black-bg: rgba(26,26,26,0.95);
  }}
  body {{
    font-family: 'Inter', sans-serif;
    background: var(--bg);
    color: var(--white);
    line-height: 1.7;
    min-height: 100vh;
  }}
  h1, h2, h3, h4 {{ font-family: 'Playfair Display', serif; }}

  /* Nav */
  .top-nav {{
    display: flex; flex-wrap: wrap; gap: 6px;
    justify-content: center; padding: 14px 20px;
    border-bottom: 1px solid var(--border);
    background: rgba(0,0,0,0.95);
    position: sticky; top: 0; z-index: 100;
  }}
  .top-nav a {{
    color: var(--gray); text-decoration: none; font-size: 0.85rem;
    font-weight: 500; padding: 5px 12px; border-radius: 20px;
    border: 1px solid transparent; transition: all 0.2s; white-space: nowrap;
  }}
  .top-nav a:hover {{ color: var(--gold); border-color: var(--border); }}
  .top-nav a:first-child {{ color: var(--gold); border-color: var(--border); }}

  /* Hero */
  .hero {{
    padding: 48px 24px 36px;
    text-align: center;
    background: linear-gradient(180deg, rgba(212,175,55,0.08) 0%, transparent 100%);
    border-bottom: 1px solid var(--border);
  }}
  .hero h1 {{
    font-size: clamp(1.6rem, 4vw, 2.6rem);
    color: var(--white);
    margin-bottom: 8px;
    letter-spacing: 0.5px;
  }}
  .hero h1 span {{ color: var(--gold); }}
  .hero .denom-tag {{
    display: inline-block;
    background: rgba(212,175,55,0.1);
    border: 1px solid rgba(212,175,55,0.25);
    color: var(--gold-light);
    font-size: 0.75rem; font-weight: 600;
    letter-spacing: 1.5px; text-transform: uppercase;
    padding: 3px 12px; border-radius: 20px; margin-bottom: 16px;
  }}
  .hero .address {{
    color: var(--gray-light);
    font-size: 0.95rem;
    margin-bottom: 18px;
  }}

  /* Threat / Rating badge */
  .threat-badge {{
    display: inline-flex; align-items: center; gap: 8px;
    padding: 8px 20px; border-radius: 8px;
    font-weight: 700; font-size: 0.95rem;
    letter-spacing: 0.5px; margin-top: 8px;
    border: 1.5px solid;
  }}
  .threat-badge.rating-green {{ background: rgba(76,175,80,0.18); border-color: var(--green); color: #7edd80; }}
  .threat-badge.rating-yellow {{ background: rgba(255,193,7,0.15); border-color: var(--yellow); color: #ffd85a; }}
  .threat-badge.rating-red {{ background: rgba(244,67,54,0.15); border-color: var(--red); color: #ff7c74; }}
  .threat-icon {{ font-size: 1.3rem; }}

  /* Main layout */
  .page-body {{
    max-width: 960px;
    margin: 0 auto;
    padding: 36px 24px 60px;
  }}

  /* Cards */
  .card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 28px;
  }}
  .card-title {{
    font-size: 1.0rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--gold);
    margin-bottom: 18px;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
  }}

  /* Quick Facts */
  .facts-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 14px;
  }}
  .fact-item {{ display: flex; flex-direction: column; gap: 3px; }}
  .fact-label {{ font-size: 0.72rem; color: var(--gray); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }}
  .fact-value {{ font-size: 0.92rem; color: var(--white); font-weight: 500; }}
  .fact-value a {{ color: var(--gold); text-decoration: none; }}
  .fact-value a:hover {{ text-decoration: underline; }}
  .has-yes {{ color: #7edd80; font-weight: 600; }}
  .has-no {{ color: var(--gray); }}

  /* Scorecard */
  .score-row {{
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 12px;
    align-items: start;
    padding: 14px 0;
    border-bottom: 1px solid #1e1e1e;
  }}
  .score-row:last-child {{ border-bottom: none; }}
  .score-info {{ display: flex; flex-direction: column; gap: 4px; }}
  .score-label {{ font-weight: 600; font-size: 0.95rem; color: var(--white); }}
  .score-desc {{ font-size: 0.82rem; color: var(--gray-light); }}
  .score-note {{ font-size: 0.82rem; color: #aaa; margin-top: 4px; font-style: italic; }}
  .gender-detail {{ font-size: 0.8rem; color: #bbb; margin-top: 4px; padding: 6px 10px; background: rgba(212,175,55,0.06); border-left: 2px solid var(--gold); border-radius: 0 4px 4px 0; }}
  .score-badge {{
    display: inline-flex; align-items: center; gap: 5px;
    padding: 4px 12px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700; white-space: nowrap;
    border: 1px solid;
  }}
  .score-green {{ background: rgba(76,175,80,0.15); border-color: var(--green); color: #7edd80; }}
  .score-yellow {{ background: rgba(255,193,7,0.12); border-color: var(--yellow); color: #ffd85a; }}
  .score-red {{ background: rgba(244,67,54,0.12); border-color: var(--red); color: #ff7c74; }}
  .score-black {{ background: rgba(50,50,50,0.6); border-color: #555; color: #aaa; }}

  /* Notes */
  .note-block {{
    padding: 14px 16px;
    border-radius: 8px;
    margin-bottom: 12px;
    border-left: 3px solid;
    font-size: 0.9rem;
    line-height: 1.7;
  }}
  .note-assessment {{
    background: rgba(212,175,55,0.06);
    border-color: var(--gold);
    color: var(--gray-light);
  }}
  .note-tag-row {{
    display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px;
  }}
  .tag {{
    background: #1a1a1a; border: 1px solid #333;
    color: var(--gray); font-size: 0.72rem;
    padding: 3px 10px; border-radius: 20px;
  }}

  /* Map */
  .map-wrap {{
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid var(--border);
    margin-bottom: 28px;
  }}
  .map-wrap iframe {{
    width: 100%; height: 320px; border: none; display: block;
    filter: invert(0.9) hue-rotate(180deg);
  }}

  /* Buttons */
  .btn-row {{ display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 28px; }}
  .btn-gold {{
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--gold); color: #000;
    font-weight: 700; font-size: 0.9rem;
    padding: 11px 22px; border-radius: 8px;
    text-decoration: none; border: none; cursor: pointer;
    transition: background 0.2s;
  }}
  .btn-gold:hover {{ background: var(--gold-light); }}
  .btn-outline {{
    display: inline-flex; align-items: center; gap: 8px;
    background: transparent; color: var(--gold);
    font-weight: 600; font-size: 0.9rem;
    padding: 11px 22px; border-radius: 8px;
    text-decoration: none; border: 1.5px solid var(--gold);
    cursor: pointer; transition: all 0.2s;
  }}
  .btn-outline:hover {{ background: rgba(212,175,55,0.1); }}

  /* Footer */
  .back-row {{
    text-align: center;
    padding: 20px 0 10px;
    border-top: 1px solid var(--border);
    margin-top: 20px;
  }}
  .back-row a {{ color: var(--gold); text-decoration: none; font-weight: 600; font-size: 0.9rem; }}
  .back-row a:hover {{ text-decoration: underline; }}

  footer {{
    text-align: center;
    padding: 24px;
    color: var(--gray);
    font-size: 0.8rem;
    border-top: 1px solid var(--border);
  }}
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

  <!-- Quick Facts -->
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
    {eng_rows}
  </div>

  <!-- Map -->
  <div class="map-wrap">
    <iframe
      src="{map_url}"
      allowfullscreen="" loading="lazy"
      referrerpolicy="no-referrer-when-downgrade"
      title="Map for {name}">
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
  <p>DC/Northern Virginia Church Directory &mdash; Theological Due Diligence for Christian Men &mdash; <a href="https://usmcmin.org" style="color: var(--gold);">usmcmin.org</a></p>
  <p style="margin-top: 6px;">Last updated: {today}</p>
</footer>
</body>
</html>"""


def main():
    out_dir = os.path.join(os.path.dirname(__file__), "..", "docs", "churches")
    json_path = os.path.join(os.path.dirname(__file__), "..", "docs", "data", "churches.json")

    # Load existing churches.json
    with open(json_path, "r") as f:
        data = json.load(f)

    existing_ids = {c["id"] for c in data["churches"]}

    added = 0
    updated = 0

    for church in CHURCHES:
        # Write HTML
        html_path = os.path.join(out_dir, f"{church['id']}.html")
        html_content = render_page(church)
        with open(html_path, "w") as f:
            f.write(html_content)
        print(f"✅ Wrote {html_path}")

        # Add to JSON if not exists
        if church["id"] not in existing_ids:
            data["churches"].append(church)
            added += 1
            existing_ids.add(church["id"])
        else:
            # Update existing
            for i, c in enumerate(data["churches"]):
                if c["id"] == church["id"]:
                    data["churches"][i] = church
                    updated += 1
                    break

    # Write updated churches.json
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n✅ churches.json updated: {added} added, {updated} updated")
    print(f"Total churches: {len(data['churches'])}")


if __name__ == "__main__":
    main()
