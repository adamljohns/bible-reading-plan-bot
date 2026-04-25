"""MBT 1 Peter — 5 chapters, 105 verses. Book ID 60."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_PATH = ROOT / "docs" / "assets" / "mbt-nt-extra.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "Peter, an apostle of Jesus Christ — to the elect exiles of the dispersion in Pontus, Galatia, Cappadocia, Asia, and Bithynia,",
    2: "according to the foreknowledge of God the Father, by the sanctification of the Spirit, for obedience and sprinkling with the blood of Jesus Christ: Grace and peace be multiplied to you.",
    3: "Blessed be the God and Father of our Lord Jesus Christ — who according to His great mercy has given us new birth into a living hope through the resurrection of Jesus Christ from the dead,",
    4: "to an inheritance imperishable, undefiled, and unfading — kept in heaven for you,",
    5: "who through faith are being guarded by the power of God for the salvation ready to be revealed in the last time.",
    6: "In this you greatly rejoice — though now, for a little while if necessary, you have been distressed by various trials,",
    7: "so that the proven character of your faith — more precious than gold which is perishable, even though tested by fire — may be found to result in praise, glory, and honor at the revelation of Jesus Christ.",
    8: "Whom not having seen, you love; in whom, though you do not see Him now, you believe — and rejoice with joy unspeakable and full of glory,",
    9: "obtaining as the outcome of your faith the salvation of your souls.",
    10: "Concerning this salvation, the prophets — who prophesied of the grace that was to come to you — sought and searched diligently,",
    11: "inquiring as to what time, or what kind of time, the Spirit of Christ within them was pointing to, when He testified beforehand of the sufferings of Christ and the glories that would follow.",
    12: "It was revealed to them that they were not serving themselves, but you — in these things which now have been announced to you, through those who preached the gospel to you by the Holy Spirit sent from heaven; things into which angels long to look.",
    13: "Therefore, gird up the loins of your mind. Be sober. Set your hope completely on the grace to be brought to you at the revelation of Jesus Christ.",
    14: "As obedient children, do not be conformed to the desires of your former ignorance,",
    15: "but as the One who called you is holy, you also be holy in all your conduct;",
    16: "because it is written, \"Be holy, for I am holy.\"",
    17: "And if you call on the Father — who without partiality judges according to each one's deeds — conduct yourselves in fear during the time of your pilgrimage,",
    18: "knowing that you were not redeemed with perishable things, like silver or gold, from the futile way of life inherited from your fathers,",
    19: "but with the precious blood of Christ — as of a lamb without blemish or spot.",
    20: "He was foreknown before the foundation of the world, but has appeared in these last times for your sake,",
    21: "who through Him are believers in God — who raised Him from the dead and gave Him glory — so that your faith and hope are in God.",
    22: "Since you have purified your souls by your obedience to the truth — for sincere love of the brothers — love one another earnestly from a pure heart,",
    23: "having been born again — not of perishable seed but of imperishable — through the living and abiding word of God.",
    24: "For \"all flesh is like grass, and all its glory like the flower of grass. The grass withers, and the flower falls,",
    25: "but the word of the Lord remains forever.\" And this is the word that was preached to you.",
}
ch2 = {
    1: "Therefore, putting aside all malice, all deceit, hypocrisy, envy, and all slander,",
    2: "like newborn babies, long for the pure milk of the word — that by it you may grow up to salvation,",
    3: "if indeed you have tasted that the Lord is good.",
    4: "Coming to Him — a living stone, rejected by men, but in the sight of God chosen and precious —",
    5: "you yourselves, like living stones, are being built up as a spiritual house — to be a holy priesthood, to offer up spiritual sacrifices acceptable to God through Jesus Christ.",
    6: "For it stands in Scripture: \"Behold, I am laying in Zion a chosen stone, a precious cornerstone — and the one who believes in Him will not be put to shame.\"",
    7: "Therefore the precious value is for you who believe. But to those who do not believe — \"the stone the builders rejected has become the chief cornerstone\" —",
    8: "and \"a stone of stumbling and a rock of offense.\" They stumble because they are disobedient to the word — to which they were also appointed.",
    9: "But you are a chosen race, a royal priesthood, a holy nation, a people for God's own possession — that you may proclaim the excellencies of Him who called you out of darkness into His marvelous light.",
    10: "Once you were not a people, but now you are God's people. Once you had not received mercy, but now you have received mercy.",
    11: "Beloved, I urge you as foreigners and pilgrims — abstain from fleshly lusts, which wage war against the soul.",
    12: "Keep your conduct among the Gentiles excellent — so that, in the very thing they slander you for as evildoers, they may by your good deeds, as they observe them, glorify God on the day of visitation.",
    13: "Submit yourselves for the Lord's sake to every human institution — whether to the king as supreme,",
    14: "or to governors as those sent by him to punish those who do evil and to praise those who do good.",
    15: "For this is the will of God: that by doing good you should silence the ignorance of foolish men.",
    16: "Live as free people — not using your freedom as a covering for evil, but as bondservants of God.",
    17: "Honor everyone. Love the brotherhood. Fear God. Honor the king.",
    18: "Servants, submit yourselves with all respect to your masters — not only to those who are good and gentle, but also to those who are unreasonable.",
    19: "For this is commendable — if for the sake of conscience toward God a person bears up under sorrows when suffering unjustly.",
    20: "For what credit is it if, when you sin and are beaten for it, you endure? But if you do what is right and suffer for it, and you endure — this is commendable before God.",
    21: "For to this you were called — because Christ also suffered for you, leaving you an example, that you should follow in His steps.",
    22: "He committed no sin, nor was deceit found in His mouth.",
    23: "When He was reviled, He did not revile in return. When He suffered, He did not threaten — but kept entrusting Himself to the One who judges righteously.",
    24: "He Himself bore our sins in His body on the tree — so that we, having died to sins, might live to righteousness. By His wounds you have been healed.",
    25: "For you were like sheep going astray — but you have now returned to the Shepherd and Overseer of your souls.",
}
ch3 = {
    1: "Likewise, wives — be subject to your own husbands, so that even if some are disobedient to the word, they may be won without a word by the conduct of their wives,",
    2: "as they observe your pure and reverent conduct.",
    3: "Let your adornment not be the outward — braiding the hair, wearing gold jewelry, or putting on fine clothing —",
    4: "but the hidden person of the heart, with the imperishable beauty of a gentle and quiet spirit, which in God's sight is very precious.",
    5: "For this is the way the holy women in former times — who hoped in God — adorned themselves, by being subject to their own husbands.",
    6: "Just as Sarah obeyed Abraham, calling him lord — and you have become her children if you do good and are not frightened by any fear.",
    7: "You husbands likewise — live with your wives in an understanding way, as with the weaker vessel, granting her honor as a fellow heir of the grace of life — so that your prayers may not be hindered.",
    8: "Finally, all of you — be of one mind, sympathetic, loving as brothers, tenderhearted, humble in mind.",
    9: "Not returning evil for evil, or insult for insult — but on the contrary, blessing. For to this you were called — that you may inherit a blessing.",
    10: "For \"the one who desires to love life and see good days, let him keep his tongue from evil and his lips from speaking deceit.",
    11: "Let him turn away from evil and do good. Let him seek peace and pursue it.",
    12: "For the eyes of the Lord are toward the righteous, and His ears are attentive to their prayer. But the face of the Lord is against those who do evil.\"",
    13: "And who is going to harm you, if you become zealous for what is good?",
    14: "But even if you should suffer for the sake of righteousness — you are blessed. \"Do not fear what they fear, and do not be troubled.\"",
    15: "But sanctify Christ as Lord in your hearts — always being ready to give a defense to anyone who asks you for an account of the hope that is in you, yet with gentleness and reverence.",
    16: "Have a good conscience — so that those who slander your good behavior in Christ may be put to shame in the very thing they speak against.",
    17: "For it is better, if it is the will of God, to suffer for doing what is right rather than for doing what is wrong.",
    18: "For Christ also suffered once for sins — the righteous for the unrighteous — that He might bring us to God; being put to death in the flesh, but made alive in the spirit;",
    19: "in which also He went and made proclamation to the spirits in prison —",
    20: "those who once were disobedient when the patience of God kept waiting in the days of Noah, during the construction of the ark, in which a few — that is, eight souls — were brought safely through the water.",
    21: "Corresponding to this, baptism now saves you — not the removal of dirt from the flesh, but the appeal to God for a good conscience — through the resurrection of Jesus Christ,",
    22: "who is at the right hand of God, having gone into heaven — angels and authorities and powers having been subjected to Him.",
}
ch4 = {
    1: "Therefore, since Christ has suffered in the flesh, arm yourselves also with the same purpose — for the one who has suffered in the flesh has ceased from sin —",
    2: "so as to live the rest of his time in the flesh no longer for human lusts, but for the will of God.",
    3: "For the time already past is sufficient for having carried out the desire of the Gentiles — having pursued a course of sensuality, lusts, drunkenness, carousing, drinking parties, and abominable idolatries.",
    4: "In all this they are surprised that you do not run with them into the same flood of debauchery — and they malign you.",
    5: "But they will give an account to Him who is ready to judge the living and the dead.",
    6: "For this reason the gospel was preached even to those who are dead — that though they are judged in the flesh as men, they may live in the spirit according to the will of God.",
    7: "The end of all things is near. Therefore be sober-minded and self-controlled for prayer.",
    8: "Above all, keep fervent in your love for one another — because love covers a multitude of sins.",
    9: "Be hospitable to one another without complaint.",
    10: "As each one has received a gift, employ it in serving one another — as good stewards of the manifold grace of God.",
    11: "Whoever speaks, let him do so as one who utters the words of God. Whoever serves, let him do so by the strength which God supplies — so that in everything God may be glorified through Jesus Christ. To Him belong the glory and dominion forever and ever. Amen.",
    12: "Beloved, do not be surprised at the fiery trial that is taking place among you for your testing — as though something strange were happening to you.",
    13: "But to the degree that you share the sufferings of Christ, rejoice — so that also at the revelation of His glory, you may rejoice with great gladness.",
    14: "If you are reviled for the name of Christ, you are blessed — because the Spirit of glory and of God rests on you.",
    15: "By no means let any of you suffer as a murderer, or thief, or evildoer, or as a meddler in other people's affairs.",
    16: "But if anyone suffers as a Christian, let him not be ashamed — but let him glorify God in this name.",
    17: "For it is time for judgment to begin with the household of God. And if it begins with us first, what will be the end of those who do not obey the gospel of God?",
    18: "And \"if the righteous one is scarcely saved, what will become of the ungodly and the sinner?\"",
    19: "Therefore, let those who suffer according to the will of God entrust their souls to a faithful Creator in doing what is right.",
}
ch5 = {
    1: "Therefore I exhort the elders among you, as your fellow elder and witness of the sufferings of Christ, and a partaker also of the glory that is to be revealed:",
    2: "Shepherd the flock of God among you — exercising oversight, not under compulsion but voluntarily, according to the will of God; nor for sordid gain, but with eagerness;",
    3: "nor as lording it over those allotted to your charge, but as examples to the flock.",
    4: "And when the Chief Shepherd appears, you will receive the unfading crown of glory.",
    5: "Likewise, you younger men — be subject to your elders. And all of you, clothe yourselves with humility toward one another — for \"God opposes the proud, but gives grace to the humble.\"",
    6: "Therefore humble yourselves under the mighty hand of God — that He may exalt you at the proper time.",
    7: "Casting all your anxieties on Him, because He cares for you.",
    8: "Be sober-minded. Be watchful. Your adversary, the devil, prowls around like a roaring lion, seeking someone to devour.",
    9: "Resist him — firm in your faith — knowing that the same kinds of suffering are being accomplished by your brothers who are in the world.",
    10: "And after you have suffered for a little while, the God of all grace — who called you to His eternal glory in Christ — will Himself perfect, confirm, strengthen, and establish you.",
    11: "To Him be dominion forever and ever. Amen.",
    12: "By Silvanus — our faithful brother, as I regard him — I have written to you briefly, exhorting and bearing witness that this is the true grace of God. Stand firm in it.",
    13: "She who is in Babylon, chosen together with you, sends you greetings — and so does Mark, my son.",
    14: "Greet one another with a kiss of love. Peace be to you all who are in Christ.",
}
CHAPTERS = {1: ch1, 2: ch2, 3: ch3, 4: ch4, 5: ch5}

def main():
    new_entries = {f"60_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"1 Peter total verses authored: {len(new_entries)}")
    with open(MBT_PATH) as f: existing = json.load(f)
    existing.update(new_entries)
    with open(MBT_PATH, "w") as f: json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"mbt-nt-extra.json: {len(existing)} total verses")
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f: json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT 1 Peter verses")

if __name__ == "__main__":
    main()
