"""OT pericope enrichment batch 3 — the remaining books (completes the Bible).

Adds editorial section breaks to the books still at chapter-level after batches
1-2: Leviticus, Numbers, Joshua, Judges, 1-2 Samuel, 1-2 Kings, 1-2 Chronicles,
Ezra, Nehemiah, Esther, Job (full dialogue structure), and the landmark chapters
of Jeremiah and Ezekiel.

NON-DESTRUCTIVE: never downgrades a chapter already subdivided (preserves batches
1-2 and any concurrent fleet edits). Reads true verse counts from the chapter
JSONs so section ends are exact. Idempotent.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "docs" / "assets" / "pericope-map.json"
CH_DIR = ROOT / "docs" / "assets" / "chapters"

def S(start, title): return (start, title)

LEVITICUS = {
    1:[S(1,"The Burnt Offering")],2:[S(1,"The Grain Offering")],3:[S(1,"The Peace Offering")],
    4:[S(1,"The Sin Offering")],5:[S(1,"The Guilt Offering")],
    6:[S(1,"Laws for the Offerings"),S(8,"Instructions for the Priests")],7:[S(1,"More Offering Laws")],
    8:[S(1,"The Ordination of Aaron and His Sons")],9:[S(1,"The Priests Begin Their Ministry")],
    10:[S(1,"The Death of Nadab and Abihu")],11:[S(1,"Clean and Unclean Foods")],
    12:[S(1,"Purification After Childbirth")],13:[S(1,"Laws About Skin Diseases")],
    14:[S(1,"Cleansing from Skin Disease")],15:[S(1,"Bodily Discharges")],
    16:[S(1,"The Day of Atonement")],17:[S(1,"The Sanctity of Blood")],
    18:[S(1,"Unlawful Sexual Relations")],19:[S(1,"Holiness and Justice")],
    20:[S(1,"Punishments for Sin")],21:[S(1,"Rules for Priests")],22:[S(1,"Holy Offerings")],
    23:[S(1,"The Appointed Feasts")],24:[S(1,"The Lampstand, Bread, and Blasphemy")],
    25:[S(1,"The Sabbath Year and the Jubilee")],26:[S(1,"Blessings and Curses")],
    27:[S(1,"Vows and Dedications")],
}
NUMBERS = {
    1:[S(1,"The Census of Israel")],2:[S(1,"The Tribal Camps")],3:[S(1,"The Levites")],
    4:[S(1,"Duties of the Levites")],5:[S(1,"Purity of the Camp")],
    6:[S(1,"The Nazirite Vow"),S(22,"The Priestly Blessing")],7:[S(1,"Offerings at the Dedication")],
    8:[S(1,"The Lampstand; Levites Set Apart")],9:[S(1,"The Second Passover"),S(15,"The Cloud Over the Tabernacle")],
    10:[S(1,"The Silver Trumpets"),S(11,"Israel Leaves Sinai")],11:[S(1,"The People Complain")],
    12:[S(1,"Miriam and Aaron Oppose Moses")],13:[S(1,"The Twelve Spies")],14:[S(1,"The People Rebel")],
    15:[S(1,"Laws About Offerings")],16:[S(1,"Korah's Rebellion")],17:[S(1,"Aaron's Staff Buds")],
    18:[S(1,"Duties of Priests and Levites")],19:[S(1,"The Red Heifer")],
    20:[S(1,"Water from the Rock; Miriam Dies"),S(14,"Edom Refuses Passage"),S(22,"The Death of Aaron")],
    21:[S(1,"The Bronze Serpent")],22:[S(1,"Balaam and Balak")],23:[S(1,"Balaam's Oracles")],
    24:[S(1,"Balaam's Final Oracles")],25:[S(1,"Israel's Sin at Peor")],26:[S(1,"The Second Census")],
    27:[S(1,"The Daughters of Zelophehad"),S(12,"Joshua to Succeed Moses")],28:[S(1,"Daily and Sabbath Offerings")],
    29:[S(1,"Offerings at the Feasts")],30:[S(1,"Laws About Vows")],31:[S(1,"War Against Midian")],
    32:[S(1,"The Tribes East of the Jordan")],33:[S(1,"Israel's Journey Recounted")],
    34:[S(1,"The Boundaries of Canaan")],35:[S(1,"Towns for the Levites; Cities of Refuge")],
    36:[S(1,"Inheritance of Zelophehad's Daughters")],
}
JOSHUA = {
    1:[S(1,"God Commissions Joshua")],2:[S(1,"Rahab and the Spies")],3:[S(1,"Crossing the Jordan")],
    4:[S(1,"Memorial Stones")],5:[S(1,"Circumcision and Passover"),S(13,"The Commander of the Lord's Army")],
    6:[S(1,"The Fall of Jericho")],7:[S(1,"Achan's Sin")],8:[S(1,"The Fall of Ai"),S(30,"The Covenant Renewed")],
    9:[S(1,"The Gibeonite Deception")],10:[S(1,"The Sun Stands Still"),S(28,"Southern Cities Conquered")],
    11:[S(1,"Northern Kings Defeated")],12:[S(1,"The Kings Defeated by Israel")],
    13:[S(1,"Land Still to Be Conquered")],14:[S(1,"Division of the Land; Caleb's Inheritance")],
    15:[S(1,"Allotment for Judah")],16:[S(1,"Allotment for Ephraim")],17:[S(1,"Allotment for Manasseh")],
    18:[S(1,"Allotment for the Remaining Tribes")],19:[S(1,"Allotments Completed")],
    20:[S(1,"The Cities of Refuge")],21:[S(1,"Towns for the Levites")],22:[S(1,"The Eastern Tribes Return")],
    23:[S(1,"Joshua's Farewell to the Leaders")],24:[S(1,"The Covenant at Shechem"),S(29,"The Death of Joshua")],
}
JUDGES = {
    1:[S(1,"Israel Fights the Remaining Canaanites")],2:[S(1,"Israel's Disobedience"),S(6,"The Death of Joshua")],
    3:[S(1,"Othniel, Ehud, and Shamgar")],4:[S(1,"Deborah and Barak")],5:[S(1,"The Song of Deborah")],
    6:[S(1,"Gideon")],7:[S(1,"Gideon Defeats Midian")],8:[S(1,"Gideon's Final Years")],9:[S(1,"Abimelech")],
    10:[S(1,"Tola and Jair"),S(6,"Israel Oppressed Again")],11:[S(1,"Jephthah")],
    12:[S(1,"Jephthah, Ibzan, Elon, and Abdon")],13:[S(1,"The Birth of Samson")],14:[S(1,"Samson's Marriage")],
    15:[S(1,"Samson Defeats the Philistines")],16:[S(1,"Samson and Delilah")],17:[S(1,"Micah's Idols")],
    18:[S(1,"The Tribe of Dan")],19:[S(1,"The Levite and His Concubine")],20:[S(1,"Israel Punishes Benjamin")],
    21:[S(1,"Wives for the Benjamites")],
}
SAMUEL1 = {
    1:[S(1,"The Birth of Samuel")],2:[S(1,"Hannah's Prayer"),S(12,"Eli's Wicked Sons")],
    3:[S(1,"The Lord Calls Samuel")],4:[S(1,"The Ark Is Captured")],5:[S(1,"The Ark Among the Philistines")],
    6:[S(1,"The Ark Returned to Israel")],7:[S(1,"Samuel Subdues the Philistines")],8:[S(1,"Israel Demands a King")],
    9:[S(1,"Saul Meets Samuel")],10:[S(1,"Saul Anointed King")],11:[S(1,"Saul Defeats the Ammonites")],
    12:[S(1,"Samuel's Farewell Address")],13:[S(1,"Saul's Unlawful Sacrifice")],14:[S(1,"Jonathan's Victory")],
    15:[S(1,"Saul Rejected as King")],16:[S(1,"David Anointed"),S(14,"David in Saul's Court")],
    17:[S(1,"David and Goliath")],18:[S(1,"Saul's Growing Jealousy")],19:[S(1,"Saul Tries to Kill David")],
    20:[S(1,"David and Jonathan's Covenant")],21:[S(1,"David at Nob and Gath")],22:[S(1,"David's Refuge; the Priests Killed")],
    23:[S(1,"David Saves Keilah")],24:[S(1,"David Spares Saul's Life")],25:[S(1,"David, Nabal, and Abigail")],
    26:[S(1,"David Again Spares Saul")],27:[S(1,"David Among the Philistines")],28:[S(1,"Saul and the Medium at Endor")],
    29:[S(1,"The Philistines Reject David")],30:[S(1,"David Destroys the Amalekites")],31:[S(1,"The Death of Saul")],
}
SAMUEL2 = {
    1:[S(1,"David Hears of Saul's Death")],2:[S(1,"David Anointed King of Judah")],3:[S(1,"War and the Death of Abner")],
    4:[S(1,"Ish-bosheth Murdered")],5:[S(1,"David King Over All Israel"),S(6,"David Captures Jerusalem")],
    6:[S(1,"The Ark Brought to Jerusalem")],7:[S(1,"God's Covenant with David")],8:[S(1,"David's Victories")],
    9:[S(1,"David's Kindness to Mephibosheth")],10:[S(1,"David Defeats the Ammonites")],11:[S(1,"David and Bathsheba")],
    12:[S(1,"Nathan Rebukes David")],13:[S(1,"Amnon and Tamar")],14:[S(1,"Absalom Returns to Jerusalem")],
    15:[S(1,"Absalom's Conspiracy")],16:[S(1,"David Flees; Shimei Curses David")],17:[S(1,"Ahithophel and Hushai")],
    18:[S(1,"The Death of Absalom")],19:[S(1,"David Returns to Jerusalem")],20:[S(1,"Sheba Rebels")],
    21:[S(1,"The Gibeonites Avenged")],22:[S(1,"David's Song of Deliverance")],23:[S(1,"David's Last Words; His Mighty Men")],
    24:[S(1,"David's Census and the Plague")],
}
KINGS1 = {
    1:[S(1,"Adonijah Sets Himself Up; Solomon Made King")],2:[S(1,"David's Charge; Solomon's Throne Established")],
    3:[S(1,"Solomon Asks for Wisdom")],4:[S(1,"Solomon's Officials and Provisions")],5:[S(1,"Preparations for the Temple")],
    6:[S(1,"Solomon Builds the Temple")],7:[S(1,"Solomon's Palace and the Temple Furnishings")],
    8:[S(1,"The Ark Brought to the Temple"),S(22,"Solomon's Prayer of Dedication")],9:[S(1,"The Lord Appears to Solomon")],
    10:[S(1,"The Queen of Sheba")],11:[S(1,"Solomon's Wives and Idolatry"),S(26,"Jeroboam's Rebellion")],
    12:[S(1,"The Kingdom Divided")],13:[S(1,"The Man of God from Judah")],
    14:[S(1,"Prophecy Against Jeroboam"),S(21,"Rehoboam Reigns in Judah")],
    15:[S(1,"Abijam and Asa of Judah"),S(25,"Nadab and Baasha of Israel")],16:[S(1,"Kings of Israel"),S(29,"Ahab Becomes King")],
    17:[S(1,"Elijah and the Drought")],18:[S(1,"Elijah on Mount Carmel")],19:[S(1,"Elijah Flees to Horeb")],
    20:[S(1,"Ahab Defeats Ben-Hadad")],21:[S(1,"Naboth's Vineyard")],22:[S(1,"Micaiah Prophesies; the Death of Ahab")],
}
KINGS2 = {
    1:[S(1,"Elijah and King Ahaziah")],2:[S(1,"Elijah Taken Up; Elisha Succeeds")],3:[S(1,"War with Moab")],
    4:[S(1,"Elisha's Miracles")],5:[S(1,"The Healing of Naaman")],
    6:[S(1,"The Floating Axe Head; Aram's Raids"),S(24,"The Siege of Samaria")],7:[S(1,"The Siege Lifted")],
    8:[S(1,"The Shunammite's Land; Hazael")],9:[S(1,"Jehu Anointed King")],10:[S(1,"Jehu Destroys Ahab's House")],
    11:[S(1,"Athaliah and Joash")],12:[S(1,"Joash Repairs the Temple")],13:[S(1,"Jehoahaz and Jehoash of Israel")],
    14:[S(1,"Amaziah of Judah; Jeroboam II")],15:[S(1,"Kings of Judah and Israel")],16:[S(1,"Ahaz of Judah")],
    17:[S(1,"Israel Exiled to Assyria")],18:[S(1,"Hezekiah of Judah"),S(13,"Sennacherib Threatens Jerusalem")],
    19:[S(1,"Jerusalem Delivered")],20:[S(1,"Hezekiah's Illness and Pride")],21:[S(1,"Manasseh and Amon of Judah")],
    22:[S(1,"The Book of the Law Found")],23:[S(1,"Josiah's Reforms"),S(31,"The Last Kings of Judah")],
    24:[S(1,"Babylon Besieges Jerusalem")],25:[S(1,"The Fall of Jerusalem")],
}
CHRON1 = {
    1:[S(1,"From Adam to Abraham")],2:[S(1,"Israel's Sons; the Line of Judah")],3:[S(1,"The Descendants of David")],
    4:[S(1,"Descendants of Judah and Simeon")],5:[S(1,"The Tribes East of the Jordan")],6:[S(1,"The Descendants of Levi")],
    7:[S(1,"Other Tribes")],8:[S(1,"The Descendants of Benjamin")],9:[S(1,"The Returned Exiles; Saul's Line")],
    10:[S(1,"The Death of Saul")],11:[S(1,"David Made King; Jerusalem Captured")],12:[S(1,"David's Mighty Warriors")],
    13:[S(1,"Bringing Back the Ark")],14:[S(1,"David's House and Victories")],15:[S(1,"The Ark Brought to Jerusalem")],
    16:[S(1,"The Ark Placed; David's Psalm of Thanks")],17:[S(1,"God's Covenant with David")],18:[S(1,"David's Victories")],
    19:[S(1,"War with the Ammonites")],20:[S(1,"More Philistine Wars")],21:[S(1,"David's Census")],
    22:[S(1,"Preparations for the Temple")],23:[S(1,"The Divisions of the Levites")],24:[S(1,"The Divisions of the Priests")],
    25:[S(1,"The Temple Musicians")],26:[S(1,"Gatekeepers and Treasurers")],27:[S(1,"Military and Civil Officials")],
    28:[S(1,"David's Charge to Solomon")],29:[S(1,"Gifts for the Temple; David's Death")],
}
CHRON2 = {
    1:[S(1,"Solomon Asks for Wisdom")],2:[S(1,"Preparations for the Temple")],3:[S(1,"Solomon Builds the Temple")],
    4:[S(1,"The Temple Furnishings")],5:[S(1,"The Ark Brought to the Temple")],6:[S(1,"Solomon's Prayer of Dedication")],
    7:[S(1,"The Dedication of the Temple")],8:[S(1,"Solomon's Achievements")],9:[S(1,"The Queen of Sheba; Solomon's Death")],
    10:[S(1,"The Kingdom Divided")],11:[S(1,"Rehoboam of Judah")],12:[S(1,"Egypt Attacks Judah")],
    13:[S(1,"Abijah and Jeroboam")],14:[S(1,"Asa of Judah")],15:[S(1,"Asa's Reforms")],16:[S(1,"Asa's Last Years")],
    17:[S(1,"Jehoshaphat of Judah")],18:[S(1,"Micaiah Prophesies Against Ahab")],19:[S(1,"Jehoshaphat's Reforms")],
    20:[S(1,"Jehoshaphat Defeats Moab and Ammon")],21:[S(1,"Jehoram of Judah")],22:[S(1,"Ahaziah; Athaliah")],
    23:[S(1,"Joash Crowned King")],24:[S(1,"Joash Repairs the Temple")],25:[S(1,"Amaziah of Judah")],
    26:[S(1,"Uzziah of Judah")],27:[S(1,"Jotham of Judah")],28:[S(1,"Ahaz of Judah")],
    29:[S(1,"Hezekiah Cleanses the Temple")],30:[S(1,"Hezekiah Keeps the Passover")],31:[S(1,"Reforms and Offerings")],
    32:[S(1,"Sennacherib Threatens; Hezekiah's Pride")],33:[S(1,"Manasseh and Amon")],
    34:[S(1,"Josiah's Reforms; the Book Found")],35:[S(1,"Josiah Keeps the Passover; His Death")],
    36:[S(1,"The Fall of Jerusalem"),S(22,"The Decree of Cyrus")],
}
EZRA = {
    1:[S(1,"Cyrus Helps the Exiles Return")],2:[S(1,"The List of Returned Exiles")],
    3:[S(1,"Rebuilding the Altar and the Temple")],4:[S(1,"Opposition to the Rebuilding")],
    5:[S(1,"Tattenai's Letter to Darius")],6:[S(1,"The Temple Completed and Dedicated")],
    7:[S(1,"Ezra Comes to Jerusalem")],8:[S(1,"Ezra's Companions and the Journey")],
    9:[S(1,"Ezra's Prayer About Intermarriage")],10:[S(1,"The People Confess Their Sin")],
}
NEHEMIAH = {
    1:[S(1,"Nehemiah's Prayer")],2:[S(1,"Nehemiah Sent to Jerusalem")],3:[S(1,"The Builders of the Wall")],
    4:[S(1,"Opposition to the Rebuilding")],5:[S(1,"Nehemiah Helps the Poor")],6:[S(1,"The Wall Completed")],
    7:[S(1,"The List of Returned Exiles")],8:[S(1,"Ezra Reads the Law")],9:[S(1,"The Israelites Confess Their Sins")],
    10:[S(1,"The Covenant Sealed")],11:[S(1,"The Residents of Jerusalem")],12:[S(1,"Priests and Levites; the Wall Dedicated")],
    13:[S(1,"Nehemiah's Final Reforms")],
}
ESTHER = {
    1:[S(1,"Queen Vashti Deposed")],2:[S(1,"Esther Made Queen"),S(19,"Mordecai Uncovers a Plot")],
    3:[S(1,"Haman's Plot Against the Jews")],4:[S(1,"Mordecai Persuades Esther to Help")],
    5:[S(1,"Esther's Banquet; Haman's Rage")],6:[S(1,"Mordecai Honored")],7:[S(1,"Haman Hanged")],
    8:[S(1,"The King's Edict for the Jews")],9:[S(1,"The Jews Triumph; Purim Instituted")],10:[S(1,"The Greatness of Mordecai")],
}
JOB = {
    1:[S(1,"Job's Character and the First Test")],2:[S(1,"Job's Second Test"),S(11,"Job's Three Friends")],
    3:[S(1,"Job Laments His Birth")],4:[S(1,"Eliphaz: Can Mortals Be Righteous?")],5:[S(1,"Eliphaz Continues")],
    6:[S(1,"Job Replies to Eliphaz")],7:[S(1,"Job Continues")],8:[S(1,"Bildad Speaks")],9:[S(1,"Job Replies to Bildad")],
    10:[S(1,"Job Continues")],11:[S(1,"Zophar Speaks")],12:[S(1,"Job Replies to Zophar")],13:[S(1,"Job Continues")],
    14:[S(1,"Job on the Brevity of Life")],15:[S(1,"Eliphaz's Second Speech")],16:[S(1,"Job Replies")],17:[S(1,"Job Continues")],
    18:[S(1,"Bildad's Second Speech")],19:[S(1,"Job: I Know That My Redeemer Lives")],20:[S(1,"Zophar's Second Speech")],
    21:[S(1,"Job Replies")],22:[S(1,"Eliphaz's Third Speech")],23:[S(1,"Job Replies")],24:[S(1,"Job Continues")],
    25:[S(1,"Bildad's Third Speech")],26:[S(1,"Job Replies")],27:[S(1,"Job Maintains His Integrity")],
    28:[S(1,"A Hymn to Wisdom")],29:[S(1,"Job's Final Defense")],30:[S(1,"Job's Present Suffering")],
    31:[S(1,"Job's Oath of Innocence")],32:[S(1,"Elihu Speaks")],33:[S(1,"Elihu Rebukes Job")],34:[S(1,"Elihu Continues")],
    35:[S(1,"Elihu Continues")],36:[S(1,"Elihu Exalts God's Greatness")],37:[S(1,"Elihu on God's Majesty")],
    38:[S(1,"The Lord Answers Job")],39:[S(1,"The Lord Continues")],40:[S(1,"Job Humbled"),S(6,"The Lord Continues")],
    41:[S(1,"The Lord Describes Leviathan")],42:[S(1,"Job's Repentance and Restoration")],
}
# Long prophets — landmark chapters (others remain accurate chapter-level).
JEREMIAH = {
    1:[S(1,"The Call of Jeremiah")],7:[S(1,"The Temple Sermon")],18:[S(1,"At the Potter's House")],
    19:[S(1,"The Broken Flask")],23:[S(1,"The Righteous Branch"),S(9,"Lying Prophets")],
    29:[S(1,"A Letter to the Exiles")],31:[S(1,"The New Covenant")],32:[S(1,"Jeremiah Buys a Field")],
    36:[S(1,"The Scroll Read and Burned")],39:[S(1,"The Fall of Jerusalem")],52:[S(1,"The Fall of Jerusalem Recounted")],
}
EZEKIEL = {
    1:[S(1,"The Vision of the Living Creatures")],2:[S(1,"Ezekiel's Call")],8:[S(1,"Idolatry in the Temple")],
    10:[S(1,"God's Glory Departs the Temple")],18:[S(1,"The Soul Who Sins Shall Die")],
    34:[S(1,"The Shepherds of Israel")],36:[S(1,"A New Heart and a New Spirit")],
    37:[S(1,"The Valley of Dry Bones"),S(15,"One Nation Under One King")],38:[S(1,"The Prophecy Against Gog")],
    40:[S(1,"The Vision of the New Temple")],47:[S(1,"The River from the Temple")],
}

AUTHORED = {
    "3":LEVITICUS,"4":NUMBERS,"6":JOSHUA,"7":JUDGES,"9":SAMUEL1,"10":SAMUEL2,
    "11":KINGS1,"12":KINGS2,"13":CHRON1,"14":CHRON2,"15":EZRA,"16":NEHEMIAH,
    "17":ESTHER,"18":JOB,"24":JEREMIAH,"26":EZEKIEL,
}
BOOK_NAMES = {3:"Leviticus",4:"Numbers",6:"Joshua",7:"Judges",9:"1 Samuel",10:"2 Samuel",
    11:"1 Kings",12:"2 Kings",13:"1 Chronicles",14:"2 Chronicles",15:"Ezra",16:"Nehemiah",
    17:"Esther",18:"Job",24:"Jeremiah",26:"Ezekiel"}

def last_verse(bid, ch):
    d = json.loads((CH_DIR / f"{bid}_{ch}.json").read_text())
    verses = d.get("NKJV") or next(iter(d.values()), {})
    return max(int(k) for k in verses.keys()) if verses else 1

def main():
    pmap = json.loads(MAP_PATH.read_text())
    added, preserved, problems = 0, 0, 0
    for bk, chmap in AUTHORED.items():
        pmap.setdefault(bk, {})
        bid = int(bk)
        for ch, starts in chmap.items():
            chs = str(ch)
            existing = pmap[bk].get(chs)
            if existing and len(existing) > 1:
                preserved += 1
                continue
            clast = last_verse(bid, ch)
            if starts[0][0] != 1:
                print(f"  ERR {bk} {ch}: first start != 1"); problems += 1
            secs = []
            for i, (start, title) in enumerate(starts):
                end = (starts[i+1][0] - 1) if i+1 < len(starts) else clast
                if start > end:
                    print(f"  ERR {bk} {ch}: start {start} > end {end} (last verse {clast})"); problems += 1
                secs.append({"start": start, "end": end, "title": title})
            pmap[bk][chs] = secs
            added += 1
    if problems:
        raise SystemExit(f"{problems} problem(s) — not writing.")
    total = sum(sum(len(pmap[k][c]) for c in pmap[k]) for k in pmap if not k.startswith('_'))
    ot_detailed = sum(1 for b in range(1,40) if str(b) in pmap and any(len(pmap[str(b)][c])>1 for c in pmap[str(b)]))
    print(f"Batch 3: +{added} chapters subdivided, {preserved} preserved.")
    print(f"OT books with subdivisions: {ot_detailed}/39 | total sections: {total}")
    MAP_PATH.write_text(json.dumps(pmap, indent=2, ensure_ascii=False))
    print(f"Wrote {MAP_PATH}")

if __name__ == "__main__":
    main()
