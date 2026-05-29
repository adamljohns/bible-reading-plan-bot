"""Expand pericope-map.json to cover all 24 MBT-authored NT books.

Already mapped (preserved): John (43), 1 John (62), 2 John (63), 3 John (64)
Newly added by this script: Acts, Romans, 1-2 Cor, Gal, Eph, Phil, Col,
1-2 Thess, 1-2 Tim, Titus, Phlm, Heb, James, 1-2 Pet, Jude, Revelation

Anchored on NKJV + ESV section-header consensus.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "docs" / "assets" / "pericope-map.json"

def S(start, end, title):
    return {"start": start, "end": end, "title": title}

# Book 44: Acts (28 chapters)
ACTS = {
    1:  [S(1,5,"Prologue: Promise of the Spirit"), S(6,11,"The Ascension"), S(12,26,"Matthias Chosen")],
    2:  [S(1,13,"The Day of Pentecost"), S(14,41,"Peter's Sermon"), S(42,47,"Fellowship of the Early Church")],
    3:  [S(1,10,"Healing of the Lame Man"), S(11,26,"Peter Speaks in Solomon's Portico")],
    4:  [S(1,22,"Peter and John Before the Council"), S(23,31,"The Believers' Prayer"), S(32,37,"All Things in Common")],
    5:  [S(1,11,"Ananias and Sapphira"), S(12,16,"Many Signs and Wonders"), S(17,42,"The Apostles Arrested")],
    6:  [S(1,7,"Seven Chosen to Serve"), S(8,15,"Stephen Seized")],
    7:  [S(1,53,"Stephen's Speech"), S(54,60,"The Stoning of Stephen")],
    8:  [S(1,3,"Saul Persecutes the Church"), S(4,25,"Philip in Samaria"), S(26,40,"The Ethiopian Eunuch")],
    9:  [S(1,19,"The Conversion of Saul"), S(20,31,"Saul Preaches at Damascus"), S(32,43,"Aeneas and Dorcas")],
    10: [S(1,8,"Cornelius the Centurion"), S(9,23,"Peter's Vision"), S(24,48,"Peter at Cornelius's House")],
    11: [S(1,18,"Peter Explains to the Church"), S(19,30,"The Church at Antioch")],
    12: [S(1,19,"James Killed and Peter Imprisoned"), S(20,25,"The Death of Herod")],
    13: [S(1,3,"Barnabas and Saul Commissioned"), S(4,12,"On Cyprus"), S(13,52,"Paul and Barnabas at Pisidian Antioch")],
    14: [S(1,7,"In Iconium"), S(8,20,"In Lystra and Derbe"), S(21,28,"Strengthening the Churches")],
    15: [S(1,21,"The Jerusalem Council"), S(22,35,"The Council's Letter"), S(36,41,"Paul and Barnabas Separate")],
    16: [S(1,5,"Timothy Joins Paul and Silas"), S(6,10,"The Macedonian Call"), S(11,15,"Conversion of Lydia"), S(16,40,"Paul and Silas in Prison")],
    17: [S(1,9,"In Thessalonica"), S(10,15,"In Berea"), S(16,34,"Paul in Athens")],
    18: [S(1,17,"Paul in Corinth"), S(18,28,"In Ephesus and Antioch; Apollos")],
    19: [S(1,10,"Paul in Ephesus"), S(11,22,"Sons of Sceva"), S(23,41,"The Riot at Ephesus")],
    20: [S(1,12,"Paul in Macedonia and Greece; Eutychus"), S(13,38,"Farewell to the Ephesian Elders")],
    21: [S(1,16,"Paul Goes to Jerusalem"), S(17,26,"Paul Visits James"), S(27,40,"Paul Arrested in the Temple")],
    22: [S(1,21,"Paul's Defense Before the Crowd"), S(22,30,"Paul and the Roman Tribune")],
    23: [S(1,11,"Paul Before the Council"), S(12,22,"A Plot to Kill Paul"), S(23,35,"Paul Sent to Felix")],
    24: [S(1,9,"Paul Accused Before Felix"), S(10,21,"Paul's Defense Before Felix"), S(22,27,"Paul Kept in Custody")],
    25: [S(1,12,"Paul Appeals to Caesar"), S(13,27,"Paul Before Agrippa and Bernice")],
    26: [S(1,23,"Paul's Defense Before Agrippa"), S(24,32,"Paul Almost Persuades Agrippa")],
    27: [S(1,12,"Paul Sails for Rome"), S(13,38,"The Storm at Sea"), S(39,44,"The Shipwreck")],
    28: [S(1,10,"Paul on Malta"), S(11,16,"Paul Arrives at Rome"), S(17,31,"Paul Preaches in Rome")],
}

# Book 45: Romans (16 chapters)
ROMANS = {
    1:  [S(1,7,"Greeting"), S(8,17,"Longing to Go to Rome"), S(18,32,"God's Wrath on Unrighteousness")],
    2:  [S(1,11,"God's Righteous Judgment"), S(12,16,"The Law and the Conscience"), S(17,29,"The Jews and the Law")],
    3:  [S(1,8,"God's Faithfulness"), S(9,20,"No One Is Righteous"), S(21,31,"The Righteousness of God Through Faith")],
    4:  [S(1,12,"Abraham Justified by Faith"), S(13,25,"The Promise Realized Through Faith")],
    5:  [S(1,11,"Peace With God Through Faith"), S(12,21,"Death in Adam, Life in Christ")],
    6:  [S(1,14,"Dead to Sin, Alive to God"), S(15,23,"Slaves to Righteousness")],
    7:  [S(1,6,"Released From the Law"), S(7,25,"The Law and Sin")],
    8:  [S(1,17,"Life in the Spirit"), S(18,30,"Future Glory"), S(31,39,"More Than Conquerors")],
    9:  [S(1,5,"Paul's Sorrow for Israel"), S(6,29,"God's Sovereign Choice"), S(30,33,"Israel's Unbelief")],
    10: [S(1,13,"Salvation for All"), S(14,21,"Israel's Rejection of the Gospel")],
    11: [S(1,10,"The Remnant of Israel"), S(11,24,"Gentiles Grafted In"), S(25,36,"All Israel Will Be Saved")],
    12: [S(1,2,"A Living Sacrifice"), S(3,8,"Gifts of Grace"), S(9,21,"Marks of the True Christian")],
    13: [S(1,7,"Submission to the Authorities"), S(8,14,"Love Fulfills the Law")],
    14: [S(1,12,"Do Not Pass Judgment on One Another"), S(13,26,"Do Not Cause Another to Stumble")],
    15: [S(1,13,"The Example of Christ"), S(14,33,"Paul the Minister to the Gentiles")],
    16: [S(1,16,"Personal Greetings"), S(17,20,"Final Instructions and Greetings"), S(21,27,"Doxology")],
}

# Book 46: 1 Corinthians (16 chapters)
CORINTH1 = {
    1:  [S(1,9,"Greeting and Thanksgiving"), S(10,17,"Divisions in the Church"), S(18,31,"Christ the Wisdom and Power of God")],
    2:  [S(1,5,"Proclaiming Christ Crucified"), S(6,16,"Wisdom From the Spirit")],
    3:  [S(1,9,"Divisions in the Church"), S(10,23,"God's Foundation in Christ")],
    4:  [S(1,13,"The Ministry of Apostles"), S(14,21,"Paul's Fatherly Care")],
    5:  [S(1,13,"Sexual Immorality Defiles the Church")],
    6:  [S(1,11,"Lawsuits Against Believers"), S(12,20,"Glorify God in Your Body")],
    7:  [S(1,16,"Principles for Marriage"), S(17,24,"Live as You Are Called"), S(25,40,"The Unmarried and Widows")],
    8:  [S(1,13,"Food Offered to Idols")],
    9:  [S(1,18,"Paul Surrenders His Rights"), S(19,27,"All Things to All People")],
    10: [S(1,13,"Warning Against Idolatry"), S(14,22,"The Cup of Blessing"), S(23,33,"Do All to the Glory of God")],
    11: [S(1,16,"Head Coverings"), S(17,34,"The Lord's Supper")],
    12: [S(1,11,"Spiritual Gifts"), S(12,31,"One Body With Many Members")],
    13: [S(1,13,"The Way of Love")],
    14: [S(1,25,"Prophecy and Tongues"), S(26,40,"Orderly Worship")],
    15: [S(1,11,"The Resurrection of Christ"), S(12,34,"The Resurrection of the Dead"), S(35,49,"The Resurrection Body"), S(50,58,"Mystery and Victory")],
    16: [S(1,4,"The Collection for the Saints"), S(5,12,"Plans for Travel"), S(13,24,"Final Greetings")],
}

# Book 47: 2 Corinthians (13 chapters)
CORINTH2 = {
    1:  [S(1,11,"The God of All Comfort"), S(12,24,"Paul's Change of Plans")],
    2:  [S(1,11,"Forgive the Sinner"), S(12,17,"Triumph in Christ")],
    3:  [S(1,18,"Ministers of a New Covenant")],
    4:  [S(1,6,"The Light of the Gospel"), S(7,18,"Treasure in Jars of Clay")],
    5:  [S(1,10,"Our Heavenly Dwelling"), S(11,21,"The Ministry of Reconciliation")],
    6:  [S(1,13,"Now Is the Day of Salvation"), S(14,18,"The Temple of the Living God")],
    7:  [S(1,16,"Paul's Joy in Their Comfort")],
    8:  [S(1,15,"Encouragement to Give Generously"), S(16,24,"Titus Sent to Corinth")],
    9:  [S(1,15,"The Cheerful Giver")],
    10: [S(1,18,"Paul Defends His Ministry")],
    11: [S(1,15,"Paul and the False Apostles"), S(16,33,"Paul's Sufferings as an Apostle")],
    12: [S(1,10,"Paul's Vision and Thorn"), S(11,21,"Concern for the Corinthian Church")],
    13: [S(1,10,"Final Warnings"), S(11,14,"Final Greetings")],
}

# Book 48: Galatians (6 chapters)
GAL = {
    1:  [S(1,5,"Greeting"), S(6,10,"No Other Gospel"), S(11,24,"Paul Called by God")],
    2:  [S(1,10,"Paul Accepted by the Apostles"), S(11,21,"Paul Confronts Cephas")],
    3:  [S(1,14,"By Faith, Not by Works of the Law"), S(15,29,"The Law and the Promise")],
    4:  [S(1,11,"Sons and Heirs"), S(12,20,"Paul's Concern for the Galatians"), S(21,31,"Hagar and Sarah")],
    5:  [S(1,15,"Christ Has Set Us Free"), S(16,26,"Walk by the Spirit")],
    6:  [S(1,10,"Bear One Another's Burdens"), S(11,18,"Final Warning and Benediction")],
}

# Book 49: Ephesians (6 chapters)
EPH = {
    1:  [S(1,2,"Greeting"), S(3,14,"Spiritual Blessings in Christ"), S(15,23,"Thanksgiving and Prayer")],
    2:  [S(1,10,"By Grace Through Faith"), S(11,22,"One in Christ")],
    3:  [S(1,13,"The Mystery of the Gospel Revealed"), S(14,21,"Prayer for Spiritual Strength")],
    4:  [S(1,16,"Unity in the Body of Christ"), S(17,32,"The New Life in Christ")],
    5:  [S(1,21,"Walk in Love and Light"), S(22,33,"Wives and Husbands")],
    6:  [S(1,4,"Children and Parents"), S(5,9,"Bondservants and Masters"), S(10,20,"The Whole Armor of God"), S(21,24,"Final Greetings")],
}

# Book 50: Philippians (4 chapters)
PHIL = {
    1:  [S(1,11,"Greeting and Thanksgiving"), S(12,26,"The Advance of the Gospel"), S(27,30,"Worthy of the Gospel")],
    2:  [S(1,11,"Christ's Example of Humility"), S(12,18,"Lights in the World"), S(19,30,"Timothy and Epaphroditus")],
    3:  [S(1,11,"Righteousness Through Faith in Christ"), S(12,21,"Press On Toward the Goal")],
    4:  [S(1,9,"Rejoice in the Lord Always"), S(10,23,"God's Provision; Final Greetings")],
}

# Book 51: Colossians (4 chapters)
COL = {
    1:  [S(1,14,"Greeting and Thanksgiving"), S(15,23,"The Preeminence of Christ"), S(24,29,"Paul's Ministry to the Church")],
    2:  [S(1,7,"Alive in Christ"), S(8,23,"Christ Versus False Philosophy")],
    3:  [S(1,17,"Put On the New Self"), S(18,25,"Rules for Christian Households")],
    4:  [S(1,6,"Further Instructions"), S(7,18,"Final Greetings")],
}

# Book 52: 1 Thessalonians (5 chapters)
THESS1 = {
    1:  [S(1,10,"Greeting and Thanksgiving")],
    2:  [S(1,12,"Paul's Ministry to the Thessalonians"), S(13,16,"Receiving the Word"), S(17,20,"Paul's Longing to See Them")],
    3:  [S(1,13,"Timothy's Encouraging Report")],
    4:  [S(1,12,"A Life Pleasing to God"), S(13,18,"The Coming of the Lord")],
    5:  [S(1,11,"The Day of the Lord"), S(12,22,"Final Instructions"), S(23,28,"Benediction")],
}

# Book 53: 2 Thessalonians (3 chapters)
THESS2 = {
    1:  [S(1,2,"Greeting"), S(3,12,"Thanksgiving and the Judgment at Christ's Coming")],
    2:  [S(1,12,"The Man of Lawlessness"), S(13,17,"Chosen for Salvation")],
    3:  [S(1,5,"Pray for Us"), S(6,15,"Warning Against Idleness"), S(16,18,"Benediction")],
}

# Book 54: 1 Timothy (6 chapters)
TIM1 = {
    1:  [S(1,2,"Greeting"), S(3,11,"Warning Against False Teachers"), S(12,17,"Christ Jesus Came to Save Sinners"), S(18,20,"Fight the Good Fight")],
    2:  [S(1,7,"Pray for All People"), S(8,15,"Instructions for Men and Women")],
    3:  [S(1,7,"Qualifications for Overseers"), S(8,13,"Qualifications for Deacons"), S(14,16,"The Mystery of Godliness")],
    4:  [S(1,5,"Some Will Depart from the Faith"), S(6,16,"A Good Servant of Christ Jesus")],
    5:  [S(1,16,"Instructions for Widows and Elders"), S(17,25,"Honor and Discipline of Elders")],
    6:  [S(1,2,"Bondservants and Masters"), S(3,10,"False Teachers and the Love of Money"), S(11,21,"Fight the Good Fight of Faith")],
}

# Book 55: 2 Timothy (4 chapters)
TIM2 = {
    1:  [S(1,7,"Greeting and Thanksgiving; Guard the Deposit"), S(8,14,"Not Ashamed of the Gospel"), S(15,18,"Onesiphorus's Faithfulness")],
    2:  [S(1,13,"A Good Soldier of Christ Jesus"), S(14,26,"An Approved Workman")],
    3:  [S(1,9,"Godlessness in the Last Days"), S(10,17,"All Scripture Is Breathed Out by God")],
    4:  [S(1,8,"Preach the Word"), S(9,18,"Personal Instructions"), S(19,22,"Final Greetings")],
}

# Book 56: Titus (3 chapters)
TITUS = {
    1:  [S(1,4,"Greeting"), S(5,9,"Qualifications for Elders"), S(10,16,"Rebuke False Teachers")],
    2:  [S(1,10,"Teach Sound Doctrine"), S(11,15,"The Grace of God Has Appeared")],
    3:  [S(1,8,"Be Ready for Every Good Work"), S(9,11,"Avoid Foolish Controversies"), S(12,15,"Final Greetings")],
}

# Book 57: Philemon (1 chapter)
PHLM = {
    1:  [S(1,3,"Greeting"), S(4,7,"Philemon's Love and Faith"), S(8,22,"Paul's Plea for Onesimus"), S(23,25,"Final Greetings")],
}

# Book 58: Hebrews (13 chapters)
HEB = {
    1:  [S(1,4,"The Supremacy of God's Son"), S(5,14,"The Son Superior to Angels")],
    2:  [S(1,4,"Warning Against Neglecting Salvation"), S(5,18,"Jesus Made Like His Brothers")],
    3:  [S(1,6,"Jesus Greater Than Moses"), S(7,19,"A Rest for the People of God")],
    4:  [S(1,13,"Striving to Enter God's Rest"), S(14,16,"Jesus the Great High Priest")],
    5:  [S(1,10,"Christ a High Priest Forever"), S(11,14,"Warning Against Apostasy")],
    6:  [S(1,12,"Press On to Maturity"), S(13,20,"The Certainty of God's Promise")],
    7:  [S(1,10,"The Priestly Order of Melchizedek"), S(11,28,"Jesus, A Priest Forever")],
    8:  [S(1,13,"Jesus, High Priest of a Better Covenant")],
    9:  [S(1,14,"The Earthly and Heavenly Sanctuaries"), S(15,28,"Christ's Once-for-All Sacrifice")],
    10: [S(1,18,"Christ's Sacrifice Once for All"), S(19,39,"The Full Assurance of Faith")],
    11: [S(1,7,"By Faith — Abel, Enoch, Noah"), S(8,22,"By Faith — Abraham and Sarah"), S(23,40,"By Faith — Moses and the Prophets")],
    12: [S(1,13,"Run With Endurance"), S(14,29,"A Kingdom That Cannot Be Shaken")],
    13: [S(1,17,"Sacrifices Pleasing to God"), S(18,25,"Benediction")],
}

# Book 59: James (5 chapters)
JAMES = {
    1:  [S(1,1,"Greeting"), S(2,18,"Testing of Your Faith"), S(19,27,"Hearing and Doing the Word")],
    2:  [S(1,13,"The Sin of Partiality"), S(14,26,"Faith Without Works Is Dead")],
    3:  [S(1,12,"Taming the Tongue"), S(13,18,"Wisdom From Above")],
    4:  [S(1,12,"Warning Against Worldliness"), S(13,17,"Boasting About Tomorrow")],
    5:  [S(1,6,"Warning to the Rich"), S(7,12,"Patience in Suffering"), S(13,20,"The Prayer of Faith")],
}

# Book 60: 1 Peter (5 chapters)
PETER1 = {
    1:  [S(1,2,"Greeting"), S(3,12,"Born Again to a Living Hope"), S(13,25,"Called to Be Holy")],
    2:  [S(1,10,"A Living Stone and a Holy People"), S(11,25,"Submission to Authorities and Suffering")],
    3:  [S(1,7,"Wives and Husbands"), S(8,22,"Suffering for Righteousness' Sake")],
    4:  [S(1,11,"Stewards of God's Grace"), S(12,19,"Suffering as a Christian")],
    5:  [S(1,5,"Shepherd the Flock of God"), S(6,11,"Humility and Endurance"), S(12,14,"Final Greetings")],
}

# Book 61: 2 Peter (3 chapters)
PETER2 = {
    1:  [S(1,2,"Greeting"), S(3,11,"Make Your Calling and Election Sure"), S(12,21,"Eyewitnesses of His Majesty")],
    2:  [S(1,22,"False Prophets and Teachers")],
    3:  [S(1,13,"The Day of the Lord Will Come"), S(14,18,"Final Words")],
}

# Book 65: Jude (1 chapter)
JUDE = {
    1:  [S(1,2,"Greeting"), S(3,4,"Contend for the Faith"), S(5,16,"Judgment on False Teachers"), S(17,23,"A Call to Persevere"), S(24,25,"Doxology")],
}

# Book 66: Revelation (22 chapters)
REV = {
    1:  [S(1,8,"Prologue and Greeting"), S(9,20,"Vision of the Son of Man")],
    2:  [S(1,7,"To Ephesus"), S(8,11,"To Smyrna"), S(12,17,"To Pergamum"), S(18,29,"To Thyatira")],
    3:  [S(1,6,"To Sardis"), S(7,13,"To Philadelphia"), S(14,22,"To Laodicea")],
    4:  [S(1,11,"The Throne in Heaven")],
    5:  [S(1,14,"The Scroll and the Lamb")],
    6:  [S(1,8,"The Seven Seals — First Four"), S(9,17,"The Fifth and Sixth Seals")],
    7:  [S(1,8,"The 144,000 of Israel Sealed"), S(9,17,"A Great Multitude From Every Nation")],
    8:  [S(1,5,"The Seventh Seal and the Golden Censer"), S(6,13,"The First Four Trumpets")],
    9:  [S(1,12,"The Fifth Trumpet — Locusts"), S(13,21,"The Sixth Trumpet — Horsemen")],
    10: [S(1,11,"The Mighty Angel and the Little Scroll")],
    11: [S(1,14,"The Two Witnesses"), S(15,19,"The Seventh Trumpet")],
    12: [S(1,17,"The Woman and the Dragon")],
    13: [S(1,10,"The Beast From the Sea"), S(11,18,"The Beast From the Earth")],
    14: [S(1,5,"The Lamb and the 144,000"), S(6,13,"The Messages of the Three Angels"), S(14,20,"The Harvest of the Earth")],
    15: [S(1,8,"The Seven Angels With Seven Plagues")],
    16: [S(1,21,"The Seven Bowls of God's Wrath")],
    17: [S(1,18,"The Great Prostitute and the Beast")],
    18: [S(1,24,"The Fall of Babylon")],
    19: [S(1,10,"Rejoicing in Heaven"), S(11,21,"The Rider on a White Horse")],
    20: [S(1,6,"The Thousand Years"), S(7,15,"The Defeat of Satan and Final Judgment")],
    21: [S(1,8,"The New Heaven and the New Earth"), S(9,27,"The New Jerusalem")],
    22: [S(1,5,"The River of Life"), S(6,21,"Jesus Is Coming")],
}

NEW_MAPS = {
    "44": ACTS, "45": ROMANS, "46": CORINTH1, "47": CORINTH2, "48": GAL,
    "49": EPH, "50": PHIL, "51": COL, "52": THESS1, "53": THESS2,
    "54": TIM1, "55": TIM2, "56": TITUS, "57": PHLM, "58": HEB,
    "59": JAMES, "60": PETER1, "61": PETER2, "65": JUDE, "66": REV,
}

def main():
    with open(MAP_PATH) as f:
        pmap = json.load(f)
    before_books = sum(1 for k in pmap if not k.startswith('_'))
    before_sections = sum(
        sum(len(pmap[k][c]) for c in pmap[k])
        for k in pmap if not k.startswith('_')
    )
    print(f"Before: {before_books} books, {before_sections} sections")

    # Validate each newly-mapped book: contiguous, well-formed
    for bk, ch_map in NEW_MAPS.items():
        for ch, sections in ch_map.items():
            for i, s in enumerate(sections):
                if s['start'] > s['end']:
                    raise ValueError(f"Book {bk} ch {ch} section {i}: start>end")
                if i > 0 and s['start'] != sections[i-1]['end'] + 1:
                    print(f"  WARN Book {bk} ch {ch}: gap/overlap between section {i-1} and {i}")

    # Merge, with new maps converted to string-keyed dicts for JSON
    for bk, ch_map in NEW_MAPS.items():
        if bk not in pmap:
            pmap[bk] = {}
        for ch, sections in ch_map.items():
            pmap[bk][str(ch)] = sections

    after_books = sum(1 for k in pmap if not k.startswith('_'))
    after_sections = sum(
        sum(len(pmap[k][c]) for c in pmap[k])
        for k in pmap if not k.startswith('_')
    )
    print(f"After:  {after_books} books, {after_sections} sections")
    print(f"Delta:  +{after_books - before_books} books, +{after_sections - before_sections} sections")

    with open(MAP_PATH, "w") as f:
        json.dump(pmap, f, indent=2, ensure_ascii=False)
    print(f"Wrote {MAP_PATH}")

if __name__ == "__main__":
    main()
