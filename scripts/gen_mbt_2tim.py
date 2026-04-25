"""MBT 2 Timothy — 4 chapters, 83 verses. Book ID 55. Paul's last letter."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_PATH = ROOT / "docs" / "assets" / "mbt-nt-extra.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "Paul, an apostle of Christ Jesus by the will of God, according to the promise of life that is in Christ Jesus —",
    2: "to Timothy, my beloved son: Grace, mercy, and peace from God the Father and Christ Jesus our Lord.",
    3: "I thank God, whom I serve with a clear conscience as my forefathers did — as I constantly remember you in my prayers, night and day.",
    4: "Recalling your tears, I long to see you, that I may be filled with joy.",
    5: "I am reminded of the sincere faith within you — which first lived in your grandmother Lois and your mother Eunice, and now, I am persuaded, lives in you also.",
    6: "For this reason I remind you to fan into flame the gift of God, which is in you through the laying on of my hands.",
    7: "For God has not given us a spirit of fear, but of power, and of love, and of a sound mind.",
    8: "Therefore do not be ashamed of the testimony of our Lord, nor of me His prisoner — but share with me in suffering for the gospel, by the power of God,",
    9: "who has saved us and called us with a holy calling — not according to our works, but according to His own purpose and the grace given to us in Christ Jesus before the ages of time began,",
    10: "and now has been revealed through the appearing of our Savior Christ Jesus — who has abolished death and brought life and immortality to light through the gospel,",
    11: "for which I was appointed a herald, an apostle, and a teacher.",
    12: "For this reason I also suffer these things — but I am not ashamed, for I know whom I have believed, and I am persuaded that He is able to guard what I have entrusted to Him until that Day.",
    13: "Hold fast the pattern of sound words that you have heard from me — in the faith and love that are in Christ Jesus.",
    14: "Guard the good deposit entrusted to you, by the Holy Spirit who lives in us.",
    15: "You know this: that all who are in Asia have turned away from me — among them Phygelus and Hermogenes.",
    16: "May the Lord grant mercy to the household of Onesiphorus — for he often refreshed me, and was not ashamed of my chains.",
    17: "But when he was in Rome, he sought me out diligently and found me.",
    18: "May the Lord grant him to find mercy from the Lord on that Day. And you know very well how many ways he served at Ephesus.",
}
ch2 = {
    1: "You therefore, my son, be strong in the grace that is in Christ Jesus.",
    2: "And the things you have heard from me through many witnesses — entrust these to faithful men, who will be able to teach others also.",
    3: "Share in suffering, as a good soldier of Christ Jesus.",
    4: "No one engaged in warfare entangles himself with the affairs of civilian life, so that he may please the one who enlisted him.",
    5: "And if anyone competes in athletics, he is not crowned unless he competes according to the rules.",
    6: "The hardworking farmer ought to be the first to share in the crops.",
    7: "Consider what I say — for the Lord will give you understanding in everything.",
    8: "Remember Jesus Christ, raised from the dead, descended from David, according to my gospel —",
    9: "for which I am suffering hardship to the point of being chained as a criminal. But the word of God is not chained.",
    10: "Therefore I endure all things for the sake of the chosen ones — so that they too may obtain the salvation that is in Christ Jesus, with eternal glory.",
    11: "This saying is faithful: For if we have died with Him, we shall also live with Him.",
    12: "If we endure, we shall also reign with Him. If we deny Him, He also will deny us.",
    13: "If we are faithless, He remains faithful — for He cannot deny Himself.",
    14: "Remind them of these things — charging them in the presence of God not to wrangle about words. It is to no profit, only the ruin of those who hear.",
    15: "Be diligent to present yourself approved to God — a worker who has no need to be ashamed, rightly handling the word of truth.",
    16: "But avoid worldly and empty chatter, for it will lead to more ungodliness,",
    17: "and their word will spread like gangrene. Among them are Hymenaeus and Philetus,",
    18: "who have strayed from the truth — saying that the resurrection has already taken place. They are upsetting the faith of some.",
    19: "Nevertheless, the firm foundation of God stands — having this seal: \"The Lord knows those who are His,\" and, \"Let everyone who names the name of the Lord turn away from unrighteousness.\"",
    20: "Now in a great house there are not only vessels of gold and silver, but also of wood and earthenware — some for honorable use, some for common.",
    21: "Therefore, if anyone cleanses himself from these things, he will be a vessel for honor — sanctified, useful to the Master, prepared for every good work.",
    22: "Flee youthful lusts. And pursue righteousness, faith, love, peace — with those who call on the Lord out of a pure heart.",
    23: "But have nothing to do with foolish and ignorant disputes — knowing that they generate strife.",
    24: "And the Lord's bondservant must not be quarrelsome — but kind to all, able to teach, patient when wronged,",
    25: "in gentleness correcting those who are in opposition. Perhaps God will grant them repentance, leading to a full knowledge of the truth,",
    26: "and they may come to their senses — escaping the snare of the devil, who has held them captive to do his will.",
}
ch3 = {
    1: "But know this: that in the last days perilous times will come.",
    2: "For people will be lovers of self, lovers of money, boastful, arrogant, abusive, disobedient to parents, ungrateful, unholy,",
    3: "without natural affection, unforgiving, slanderers, without self-control, brutal, despisers of good,",
    4: "treacherous, reckless, conceited — lovers of pleasure rather than lovers of God,",
    5: "having a form of godliness, but denying its power. Avoid such people.",
    6: "For from these are those who creep into households and captivate weak women weighed down with sins, led away by various lusts —",
    7: "always learning, and never able to come to the full knowledge of the truth.",
    8: "Just as Jannes and Jambres opposed Moses, so these also oppose the truth — men of corrupt mind, disqualified concerning the faith.",
    9: "But they will not advance further. For their folly will be plain to all, just as also that of those men became.",
    10: "But you have followed my teaching, my conduct, my purpose, my faith, my patience, my love, my steadfastness,",
    11: "my persecutions, my sufferings — what happened to me at Antioch, at Iconium, at Lystra. What persecutions I endured! Yet out of them all the Lord rescued me.",
    12: "Indeed, all who desire to live godly in Christ Jesus will be persecuted.",
    13: "But evil men and impostors will go from bad to worse — deceiving and being deceived.",
    14: "But as for you — continue in the things you have learned and have been assured of, knowing from whom you have learned them.",
    15: "And how from infancy you have known the holy Scriptures, which are able to make you wise for salvation through faith in Christ Jesus.",
    16: "All Scripture is breathed out by God, and is profitable for teaching, for reproof, for correction, for training in righteousness —",
    17: "so that the man of God may be complete, equipped for every good work.",
}
ch4 = {
    1: "I solemnly charge you in the presence of God and of Christ Jesus — who will judge the living and the dead, and by His appearing and His kingdom:",
    2: "Preach the word. Be ready in season and out of season. Reprove, rebuke, exhort — with all patience and instruction.",
    3: "For the time will come when they will not endure sound doctrine — but according to their own desires they will accumulate for themselves teachers, having itching ears.",
    4: "And they will turn their ears away from the truth, and turn aside to myths.",
    5: "But you, be sober in all things. Endure suffering. Do the work of an evangelist. Fulfill your ministry.",
    6: "For I am already being poured out as a drink offering, and the time of my departure has come.",
    7: "I have fought the good fight. I have finished the race. I have kept the faith.",
    8: "Henceforth there is laid up for me the crown of righteousness, which the Lord — the righteous Judge — will give to me on that Day. And not only to me, but also to all who have loved His appearing.",
    9: "Be diligent to come to me quickly.",
    10: "For Demas, having loved this present world, has forsaken me and gone to Thessalonica. Crescens has gone to Galatia, Titus to Dalmatia.",
    11: "Only Luke is with me. Get Mark and bring him with you, for he is useful to me for ministry.",
    12: "Tychicus I have sent to Ephesus.",
    13: "When you come, bring the cloak that I left at Troas with Carpus — and the books, especially the parchments.",
    14: "Alexander the coppersmith did me much harm. The Lord will repay him according to his deeds.",
    15: "You also be on guard against him — for he greatly opposed our message.",
    16: "At my first defense, no one stood with me — all forsook me. May it not be charged against them.",
    17: "But the Lord stood by me and strengthened me — so that through me the proclamation might be fully accomplished, and that all the Gentiles might hear it. And I was rescued from the lion's mouth.",
    18: "And the Lord will rescue me from every evil deed, and bring me safely into His heavenly kingdom. To Him be the glory forever and ever. Amen.",
    19: "Greet Prisca and Aquila, and the household of Onesiphorus.",
    20: "Erastus stayed in Corinth. Trophimus I left sick at Miletus.",
    21: "Be diligent to come before winter. Eubulus greets you, as do Pudens and Linus and Claudia, and all the brothers.",
    22: "The Lord be with your spirit. Grace be with you all. Amen.",
}
CHAPTERS = {1: ch1, 2: ch2, 3: ch3, 4: ch4}

def main():
    new_entries = {f"55_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"2 Timothy total verses authored: {len(new_entries)}")
    with open(MBT_PATH) as f: existing = json.load(f)
    existing.update(new_entries)
    with open(MBT_PATH, "w") as f: json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"mbt-nt-extra.json: {len(existing)} total verses")
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f: json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT 2 Timothy verses")

if __name__ == "__main__":
    main()
