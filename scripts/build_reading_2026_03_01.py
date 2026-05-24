#!/usr/bin/env python3
"""
Build the prototype daily reading JSON for 2026-03-01 from authored meditation content
+ MBT scripture (Prov 1, Ps 56) + WEB scripture (Num 6, 7) text.

Output: data/readings/2026-03-01.json

Day 60 of the year. Sunday.
Virtue rotation: HAPPY=Yielding, FULFILLED=Loving, RESOLUTE=Obedient.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CACHE = json.load(open(REPO / "docs/assets/verse-cache.json"))
MBT_PROV1 = json.load(open(REPO / "data/mbt-batches/20_001.json"))
MBT_PS56  = json.load(open(REPO / "data/mbt-batches/19_056.json"))


def mbt_text(mbt_file, vstart, vend):
    """Return list of {verse, text} from an MBT chapter file."""
    out = []
    for v in range(vstart, vend + 1):
        if str(v) in mbt_file["verses"]:
            out.append({"v": v, "text": mbt_file["verses"][str(v)]["text"]})
    return out


def web_text(book, chap_start, vstart, chap_end, vend):
    """Return list of {ch, v, text} (WEB) for a verse range, possibly spanning chapters."""
    out = []
    chap = chap_start
    while chap <= chap_end:
        v_lo = vstart if chap == chap_start else 1
        v_hi = vend if chap == chap_end else 200
        for v in range(v_lo, v_hi + 1):
            k = f"{book}_{chap}_{v}"
            if k in CACHE and "WEB" in CACHE[k]:
                out.append({"ch": chap, "v": v, "text": CACHE[k]["WEB"].strip()})
            elif chap == chap_end and v > vend:
                break
        chap += 1
    return out


reading = {
    "date": "2026-03-01",
    "weekday": "Sunday",
    "day_of_year": 60,
    "month_doc": "MOOP's 2026 Daily Bible Readings -- Document 3 of 12; for the month of March",
    "virtue_rotation": {
        "happy": "Adoring",
        "happy_letter": "A",
        "happy_cycle": ["Honest", "Honors", "Abiding", "Adoring", "Protecting", "Providing", "Yields"],
        "fulfilled": "Listening",
        "fulfilled_letter": "L",
        "fulfilled_cycle": ["Faithful", "Understanding", "Loving", "Fun", "Intentional", "Listening", "Leading", "Encouraging", "Discipling"],
        "resolute": "Obedient",
        "resolute_letter": "O",
        "resolute_cycle": ["Responsible", "Engaged", "Steadfast", "Obedient", "Loyal", "Upright", "Trustworthy", "Enduring"],
    },

    "watches": {

        # ────────────────────────────────────────────────────────────
        "morning_wisdom": {
            "time": "0600",
            "title": "Morning Wisdom",
            "passages": ["Proverbs 1:8-33"],
            "intro": "We open the month inside Solomon's first lecture, where two voices contend for the man -- the gang's invitation and Wisdom's public cry.",
            "scripture": {
                "source": "MBT",
                "reference": "Proverbs 1:8-33",
                "verses": mbt_text(MBT_PROV1, 8, 33),
            },
            "context_summary": (
                "Solomon writes to his son with two voices ringing in the same chapter. "
                "The first voice is the enticement: a gang offers brotherhood, easy plunder, a "
                "shared purse -- all the trappings of loyalty pointed at murder. The second voice "
                "is Wisdom herself, calling aloud in the street, refusing to whisper. She has been "
                "calling a long time; her warning is unmistakable, and her offer is real. The "
                "chapter ends with the man who listens dwelling secure, undisturbed by dread."
            ),
            "real_man_theme": "Reject the Enticement",
            "reflection": (
                "A REAL MAN who Rejects the Enticement is honest about how the offer comes to him. "
                "It rarely arrives as evil announcing itself. It arrives dressed as brotherhood: "
                "the group chat that mocks the wife at home, the colleagues who drink past the line "
                "and assume you will too, the scroll that promises clarity but delivers contempt. "
                "Solomon does not ask the son to despise his peers; he asks him to refuse to walk "
                "their road. Wisdom has been calling the whole time, out in the open, where any "
                "man can hear her if he stops moving long enough to listen. The man who rejects "
                "the enticement today is not the man with the hardest jaw -- he is the man who "
                "knows the two voices apart and has already chosen which one he answers."
            ),
            "application": [
                "Name one 'gang' invitation you have been quietly entertaining -- a circle, a habit, a feed -- and decline it out loud, in writing, to one accountable man today.",
                "Find the public square where Wisdom is calling: open the Word before you open a screen, and stay there until you hear a sentence you cannot un-hear.",
                "Identify the bait you keep returning to (status, plunder, brotherhood-without-godliness) and confess in prayer that the price tag on it is your own life (v. 19).",
            ],
            "application_close": (
                "The enticement is not your problem; the listening is. Wisdom is shouting. Stop walking long enough to answer her."
            ),
            "prayer": (
                "Father of all wisdom,\n"
                "thank You that You do not whisper Your warnings from the shadows; You shout them in the open street.\n"
                "By the power of Your Holy Spirit, sharpen my ears today.\n"
                "Let me hear Wisdom's voice over the noise of every invitation that smells like brotherhood but smells more like blood.\n"
                "Teach me to fear You as the very first thing of all my knowing,\n"
                "so that no plunder, no purse, no peer pressure can pry me off the path that leads home.\n"
                "I pray this in the name of Jesus Christ, the Wisdom of God made flesh,\n"
                "by the power of the Holy Spirit. Amen."
            ),
            "helm_command": (
                "All ahead one-third toward Wisdom's voice -- step off the path of the enticer "
                "before lunch, and tell one man you did it."
            ),
        },

        # ────────────────────────────────────────────────────────────
        "first_watch": {
            "time": "0700",
            "title": "First Watch -- The Husband's Post",
            "passages": ["Numbers 6:22-7:17"],
            "happy_letter": "A",
            "happy_virtue": "Adoring",
            "intro": (
                "We pick up Numbers at the priestly blessing the LORD Himself dictates -- the words "
                "Aaron is to lay on the people -- and then the tabernacle is dedicated and the tribal "
                "offerings begin, Judah first."
            ),
            "scripture": {
                "source": "WEB",
                "reference": "Numbers 6:22-27; 7:1-17",
                "verses": web_text(4, 6, 22, 6, 27) + web_text(4, 7, 1, 7, 17),
            },
            "briefing": (
                "Before the tribes bring a single offering, God gives Aaron a blessing to speak over the "
                "people. It is not a wish; it is a placement of the divine Name upon them, channeled through "
                "the priest. Then chapter 7 opens with the tabernacle finally set up, anointed, consecrated -- "
                "and the leaders of the twelve tribes step forward over twelve days with identical offerings. "
                "Day one is Judah's. No tribe tries to outdo another; no tribe is allowed to skip. The order "
                "is fixed, the gift is the same, and God receives each one by name."
            ),
            "reflection_for_wife": (
                "A HA²PPY husband who is Adoring does not look at his wife the way familiarity teaches "
                "him to look. Familiarity rounds Maria down to roles -- the cook, the laundry, the schedule, "
                "the second pair of hands on the kids -- until the wonder of her is buried under the function. "
                "Adoring is the deliberate refusal to let that burial happen. The Aaronic blessing in Numbers "
                "6:24-26 is exactly the right tool for it: you stand in front of her and ask the LORD to keep "
                "her, to make His face shine upon her, to lift up His countenance upon her, to give her peace. "
                "You are not summarizing her; you are placing the divine Name on her, treasure by treasure, "
                "and listening to yourself say the words. Adoration is the moment you remember that she is "
                "not the household manager living in your house -- she is the woman God gave you, marked by "
                "His blessing, worth all this trouble of putting His Name on her again today."
            ),
            "application": (
                "Speak the Aaronic blessing over Maria today, by name, out loud, with your hand on her "
                "shoulder or her head -- not as a performance, but as a real act of priesthood in your home. "
                "If you cannot remember the words, read them off Numbers 6:24-26. Then linger for one full "
                "minute and look at her the way you looked at her the first month you knew her -- letting "
                "the wonder land before the next task pulls you away. Tell her one specific thing you adore "
                "about her, today, that has nothing to do with what she does for the household."
            ),
            "prayer_title": "Prayer from the Stateroom",
            "prayer": (
                "Father, our Great High Priest,\n"
                "thank You for putting Your blessing in the mouths of ordinary men so that ordinary homes "
                "can be marked with Your Name.\n"
                "Forgive me for letting familiarity round my wife down to her usefulness; restore the "
                "wonder I had at the start.\n"
                "By the power of Your Holy Spirit, make me a husband who looks at Maria today with the "
                "eyes You have for Your bride -- adoring, attentive, refusing the boredom that pride pretends "
                "is wisdom.\n"
                "Bless her, keep her, shine on her, lift Your face toward her, and give her peace today.\n"
                "Through Jesus Christ, my Lord and Commander,\n"
                "by the power of the Holy Spirit. Amen."
            ),
            "helm_command": (
                "Stand by to adore before you stand by to lead -- lay your hand on your wife, put God's "
                "Name on her, and look at her long enough for the wonder to land."
            ),
        },

        # ────────────────────────────────────────────────────────────
        "second_watch": {
            "time": "1100",
            "title": "Second Watch -- The Father's Charge",
            "passages": ["Numbers 7:18-53"],
            "fulfilled_letter": "L",
            "fulfilled_virtue": "Listening",
            "intro": (
                "Numbers 7 continues with the second through sixth days of tribal offerings -- each tribe's "
                "gift recorded individually, in full, even though every offering is identical."
            ),
            "scripture": {
                "source": "WEB",
                "reference": "Numbers 7:18-53",
                "verses": web_text(4, 7, 18, 7, 53),
            },
            "field_notes": (
                "Five tribes, five days, five identical offerings: one silver dish, one silver bowl, one "
                "gold pan, the same animals, the same grain. The narrator could have summarized -- 'and the "
                "next five tribes brought the same' -- and saved the scribe a great deal of ink. Instead, "
                "the LORD has Moses record each tribe by name, each day by date, each item by weight. The "
                "repetition is not a bug; it is the doctrine. Before this God, no tribe is summarized, "
                "no offering is skimmed, and no name is folded into 'and the others.'"
            ),
            "reflection_for_children": {
                "intro": (
                    "As a FULFILLED Father who is Listening today, you read Numbers 7 the way God reads it -- "
                    "one tribe at a time, the whole offering set down on its own page, the LORD attending to "
                    "each one as if it were the only one. That is the model for the father who Listens. "
                    "Listening fatherhood is not the gift of letting the words wash over you while you check "
                    "your phone; it is the deliberate, patient act of letting one child at a time finish a "
                    "sentence -- and then asking the second question that proves you heard the first answer. "
                    "Your three children sound the same when you stop listening; they sound completely "
                    "different the moment you start."
                ),
                "gideon": (
                    "Gideon -- listen for what Gideon is actually saying under what he says. At nineteen, "
                    "what comes out of his mouth is usually the surface of something deeper. Ask one "
                    "question today, then a second question about his answer, then a third -- and resist "
                    "the urge to redirect, advise, or fix. The father who genuinely heard him once will be "
                    "the father he calls when life gets hard."
                ),
                "boaz": (
                    "Boaz -- pray that Boaz, who lives between an older brother and a younger sister, is "
                    "heard for who Boaz is today, not for where he sits in the lineup. Ask him about "
                    "something specific to him -- a class, a friend, a hard thing he hasn't told you. Then "
                    "do the hardest thing a father does at fourteen: close your mouth and let him finish."
                ),
                "shiloh": (
                    "Shiloh -- get on her level today and listen to whatever five-year-old story she tells "
                    "you, all the way through, without rushing her toward the punch line. She is rehearsing "
                    "the kind of conversations she will have with men her whole life; let her first one be "
                    "with a daddy who listens like the offering matters."
                ),
            },
            "application": (
                "Today, set the phone face-down and listen to each of your three children one at a time, "
                "long enough to ask a follow-up question that proves you heard the answer. No multitasking, "
                "no interrupting, no advice volunteered. Then, in prayer tonight, name each of them in a "
                "separate sentence and tell the Father what you heard them say today -- not what you wished "
                "they had said. Listening means the offering registers in your ledger the way it registers "
                "in His."
            ),
            "prayer": (
                "Father, who recorded twelve identical offerings as twelve separate gifts,\n"
                "thank You that You hear my three children one voice at a time, not as a chorus to be tuned out.\n"
                "Forgive me for the times I have nodded without listening, redirected without hearing, "
                "and fixed answers to questions they never asked.\n"
                "Hear Gideon, hear Boaz, hear Shiloh -- and by the power of Your Holy Spirit, give me the "
                "patient, attentive ears of a father who reads each ledger fully.\n"
                "In the name of Jesus Christ, my Lord and Commander,\n"
                "by the Holy Spirit. Amen."
            ),
            "helm_command": (
                "Pipe each child aboard separately today -- one face, one question, one quiet pause for "
                "the answer to land, the way the LORD attends to each tribe's offering by name."
            ),
        },

        # ────────────────────────────────────────────────────────────
        "third_watch": {
            "time": "1500",
            "title": "Third Watch -- The Citizen's Stand",
            "passages": ["Numbers 7:54-89"],
            "resolute_virtue": "Obedient",
            "intro": (
                "Numbers 7 closes with the final tribal offerings (days 7 through 12) and then verse 89, "
                "where Moses enters the Tent of Meeting and hears the voice of God speaking from between "
                "the cherubim above the mercy seat."
            ),
            "scripture": {
                "source": "WEB",
                "reference": "Numbers 7:54-89",
                "verses": web_text(4, 7, 54, 7, 89),
            },
            "situation_report": (
                "Twelve days, twelve tribes, one prescribed order. No tribe negotiates a unique offering; "
                "no leader campaigns for higher visibility; no day is skipped. And at the end of the "
                "twelve days of patient obedience -- after every gift is brought in its appointed time -- "
                "Moses enters the Tent and the voice of God speaks to him from between the cherubim above "
                "the ark. Obedience to the prescribed form is what opens the door to the speaking presence. "
                "The order is the path; the voice is the destination."
            ),
            "resolute_reflection": {
                "fredericksburg": (
                    "As a RESOLUTE Citizen who is Obedient today, you treat the small obediences in "
                    "Fredericksburg as the path to a speaking God, not as bureaucratic friction. The "
                    "stop sign at the corner of Princess Anne. The trash pickup on Tuesday. The way you "
                    "speak about the city manager when nobody is recording. Obedience here is not a "
                    "show; it is the same patient ledger as Numbers 7 -- one obedience at a time, "
                    "logged by the One who keeps records."
                ),
                "virginia": (
                    "Across Virginia, an Obedient citizen submits to lawful authority as a man under "
                    "orders from a higher Commander -- not because the state is sacred, but because the "
                    "God who orders the state is. Pay your taxes. Vote your conscience. Speak truthfully "
                    "in public. Where the state's command conflicts with God's command, obey God -- but "
                    "where it does not, obey the state cheerfully, the way a sailor obeys the watch bill."
                ),
                "united_states": (
                    "For America, Obedient citizenship is the rarest virtue at the moment. A culture "
                    "that prizes self-expression treats obedience as servile and disobedience as brave. "
                    "Numbers 7 corrects that: twelve identical obediences were not boring repetition -- "
                    "they were the path to the speaking presence at the heart of the camp. The "
                    "Resolute citizen knows that a republic built on every man obeying nothing collapses; "
                    "a republic built on every man obeying God endures. Stand at your post and obey."
                ),
            },
            "this_day_in_american_history": {
                "date": "March 1",
                "events": [
                    {
                        "year": 1781,
                        "headline": "The Articles of Confederation are ratified -- the first written constitution of the United States takes effect.",
                    },
                    {
                        "year": 1872,
                        "headline": "Yellowstone is established as the first national park, placing two million acres under the obedience of public stewardship.",
                    },
                ],
                "tie": (
                    "Both shout Obedience: the first by binding thirteen jealous states to a shared "
                    "framework of law, the second by binding the next generations to steward what their "
                    "fathers received. A citizen who is Obedient sees both kinds of obedience -- the "
                    "constitutional and the stewardly -- as the same patient ledger God recorded in "
                    "Numbers 7."
                ),
            },
            "application": (
                "Take one small obedience today that nobody will see -- pay the bill you owe, return the "
                "cart, send the email you have been avoiding because honesty is harder than silence -- and "
                "do it cheerfully, as a man under orders. Then, before the sun goes down, ask the LORD what "
                "He has been saying that you have been refusing to hear; the speaking voice in Numbers 7:89 "
                "follows the patient obedience of the twelve days."
            ),
            "prayer_title": "Prayer from the Bridge",
            "prayer": (
                "Father, Sovereign over nations and cities and quiet streets,\n"
                "thank You for ordering Your tabernacle one day, one tribe, one obedience at a time -- "
                "and for speaking from between the cherubim when the twelve days were done.\n"
                "By the power of Your Holy Spirit, make me a Resolute Citizen today, Obedient to the "
                "small commands of Fredericksburg, of Virginia, and of the United States, so long as none "
                "of them set themselves against You.\n"
                "Where my obedience to the state must yield to my obedience to You, give me the courage to "
                "stand; where it need not, give me the humility to comply without complaining.\n"
                "I ask this in the name of Jesus Christ, my Lord and Commander. Amen."
            ),
            "rudder_steer": (
                "Hold your post today -- no rebellion against light commands, no servile flattery of "
                "unjust ones; just steady obedience under the One whose voice still speaks from above the ark."
            ),
        },

        # ────────────────────────────────────────────────────────────
        "evening_peace": {
            "time": "2100",
            "title": "Evening Peace",
            "passages": ["Psalm 56"],
            "intro": (
                "We close the day with David at his lowest -- captured by the Philistines at Gath, scared, "
                "watched, slandered -- and learning to trust the God who keeps count of every wandering "
                "and saves every tear in a bottle."
            ),
            "scripture": {
                "source": "MBT",
                "reference": "Psalm 56",
                "verses": mbt_text(MBT_PS56, 1, 13),
            },
            "integrated_reflection": {
                "intro": (
                    "Psalm 56 was written by a man who had every reason to be afraid, and the psalm does "
                    "not pretend the fear away. It admits the fear and answers it with trust: 'On the day "
                    "I am afraid, I will put my trust in You.' For a man at home and in community, this "
                    "psalm threads through all three of today's posts."
                ),
                "happy_husband": (
                    "As a HA²PPY husband who is Adoring, Psalm 56 teaches you to take the day's fear "
                    "to God before you take it home. A husband whose fear leaks out as control or as "
                    "distraction leaves his wife dealing with a man who is not really there; a husband "
                    "whose fear has already been collected in God's bottle comes home present and free "
                    "to look at his wife with wonder again, the way the morning Aaronic blessing put "
                    "God's Name on her."
                ),
                "fulfilled_father": (
                    "As a FULFILLED father who is Listening, this psalm models what to do in front of "
                    "your children when the news is bad and the threat is real. They do not need a "
                    "father who pretends he is unafraid; they need a father whose ears stay open and "
                    "whose mouth stays slow even when his stomach is tight. Pray Psalm 56 out loud "
                    "where Gideon, Boaz, and Shiloh can hear it -- and then close your mouth and "
                    "listen to whatever they say back."
                ),
                "resolute_citizen": (
                    "As a RESOLUTE citizen who is Obedient, Psalm 56 inoculates you against the "
                    "panicked obedience the culture demands -- the rage-clicks, the fear-shares, the "
                    "tribal alarms that whip you into someone else's reaction. David is captured by the "
                    "Philistines; the right response is not louder fear but deeper trust. A Resolute "
                    "citizen who knows God keeps his tears in a bottle does not need to keep his outrage "
                    "in a megaphone."
                ),
            },
            "prayer_title": "Prayer from the Wardroom",
            "prayer": (
                "Father, who hears the cry of David at Gath and the cry of every man at the end of his day,\n"
                "thank You that You count every wandering, gather every tear, and write each one in Your book.\n"
                "By the power of Your Holy Spirit, settle me tonight in the truth that You are for me.\n"
                "Take the day's enticements, the day's failures, the day's fears -- and seal them in the "
                "bottle of Your remembrance, where nothing is forgotten and nothing is wasted.\n"
                "Tomorrow let me walk before You in the light of the living, as a man rescued and put back "
                "on his feet by Your hand.\n"
                "In the name of Jesus Christ, my Lord and Commander,\n"
                "depending on the Spirit's help for the night. Amen."
            ),
            "rudder_steer": (
                "Ease back to anchor tonight -- name today's fear, hand it over, and let the God who "
                "bottles tears keep the night watch while you sleep."
            ),
        },
    },

    "meta": {
        "authored": "2026-05-23 (Claude Code Opus, sign-off pending)",
        "voice_anchor": "Adam Johns's Jan/Feb 2026 readings; rich interpretive blend; em-dashes sparingly; divine name LORD",
        "mbt_used_for": ["Proverbs 1:8-33", "Psalm 56"],
        "web_used_for": ["Numbers 6:22-27", "Numbers 7:1-89"],
        "mbt_pending_for": ["Numbers 6", "Numbers 7"],
    },
}

OUT = REPO / "data/readings/2026-03-01.json"
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(reading, indent=2, ensure_ascii=False) + "\n")
print(f"Wrote {OUT}")
print(f"  watches: {len(reading['watches'])}")
total_verses = sum(len(w['scripture']['verses']) for w in reading['watches'].values())
print(f"  total scripture verses embedded: {total_verses}")
size_kb = OUT.stat().st_size / 1024
print(f"  file size: {size_kb:.1f} KB")
