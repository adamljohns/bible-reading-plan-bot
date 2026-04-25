"""MBT Colossians — 4 chapters, 95 verses. Book ID 51."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_PATH = ROOT / "docs" / "assets" / "mbt-nt-extra.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "Paul, an apostle of Christ Jesus by the will of God, and Timothy our brother —",
    2: "to the saints and faithful brothers in Christ at Colossae: Grace to you, and peace from God our Father.",
    3: "We give thanks to God, the Father of our Lord Jesus Christ, always praying for you,",
    4: "since we heard of your faith in Christ Jesus and of the love that you have for all the saints,",
    5: "because of the hope laid up for you in heaven — of which you have heard before in the word of the truth, the gospel,",
    6: "which has come to you. Just as in all the world, it is bearing fruit and growing — as it has been doing among you also, since the day you heard and came to know the grace of God in truth,",
    7: "just as you learned it from Epaphras, our beloved fellow servant, who is a faithful minister of Christ on our behalf,",
    8: "and who has made known to us your love in the Spirit.",
    9: "For this reason, since the day we heard, we have not ceased to pray for you and to ask that you may be filled with the full knowledge of His will, in all spiritual wisdom and understanding —",
    10: "so that you may walk in a manner worthy of the Lord, fully pleasing to Him: bearing fruit in every good work, and growing in the full knowledge of God,",
    11: "being strengthened with all power, according to the might of His glory, for all endurance and patience with joy —",
    12: "giving thanks to the Father, who has qualified you to share in the inheritance of the saints in light;",
    13: "who has rescued us from the dominion of darkness and transferred us into the kingdom of His beloved Son,",
    14: "in whom we have redemption — the forgiveness of sins.",
    15: "He is the image of the invisible God — the firstborn over all creation;",
    16: "for in Him all things were created — in heaven and on earth, visible and invisible — whether thrones or dominions or rulers or authorities. All things have been created through Him and for Him.",
    17: "And He is before all things, and in Him all things hold together.",
    18: "And He is the head of the body — the church. He is the beginning, the firstborn from among the dead — so that in everything He may have the preeminence.",
    19: "For God was pleased to have all His fullness dwell in Him,",
    20: "and through Him to reconcile to Himself all things — whether things on earth or things in heaven — having made peace through the blood of His cross.",
    21: "And although you were once alienated and hostile in mind, doing evil deeds —",
    22: "yet now He has reconciled you in His body of flesh through death — to present you holy, blameless, and beyond reproach before Him,",
    23: "if indeed you continue in the faith, firmly grounded and steadfast — not moved away from the hope of the gospel which you have heard, which has been proclaimed in all creation under heaven, and of which I, Paul, became a minister.",
    24: "I now rejoice in my sufferings for your sake, and in my flesh I fill up what is lacking in the afflictions of Christ — for the sake of His body, which is the church —",
    25: "of which I became a minister, according to the stewardship from God which was given to me for you, to fully carry out the word of God:",
    26: "the mystery hidden from ages and from generations, but now revealed to His saints,",
    27: "to whom God willed to make known what are the riches of the glory of this mystery among the Gentiles — which is Christ in you, the hope of glory.",
    28: "Him we proclaim — admonishing every person and teaching every person in all wisdom — so that we may present every person mature in Christ.",
    29: "For this I labor — striving according to His working which works in me with power.",
}
ch2 = {
    1: "For I want you to know how great a struggle I have for you and for those at Laodicea, and for all who have not seen my face in person —",
    2: "that their hearts may be encouraged, having been knit together in love and reaching all the riches of full assurance of understanding — to the full knowledge of God's mystery: Christ,",
    3: "in whom are hidden all the treasures of wisdom and knowledge.",
    4: "I say this so that no one may deceive you with persuasive arguments.",
    5: "For though I am absent in body, yet I am with you in spirit — rejoicing to see your good order and the firmness of your faith in Christ.",
    6: "Therefore, just as you received Christ Jesus the Lord, so walk in Him —",
    7: "rooted and built up in Him, and established in the faith, just as you were taught — overflowing in thanksgiving.",
    8: "See to it that no one takes you captive through philosophy and empty deception, according to the tradition of men, according to the elementary principles of the world, and not according to Christ.",
    9: "For in Him dwells all the fullness of the deity bodily,",
    10: "and you are made full in Him — who is the head of every ruler and authority.",
    11: "In Him also you were circumcised with a circumcision not made with hands — by the putting off of the body of the flesh — by the circumcision of Christ.",
    12: "Buried with Him in baptism, in which you were also raised with Him through faith in the working of God, who raised Him from the dead.",
    13: "And you, who were dead in your trespasses and the uncircumcision of your flesh — God made alive together with Him, having forgiven us all our trespasses,",
    14: "having canceled the certificate of debt with its decrees that stood against us — and which was hostile to us. He has taken it out of the way, having nailed it to the cross.",
    15: "Having disarmed the rulers and authorities, He made a public spectacle of them — triumphing over them in the cross.",
    16: "Therefore, let no one judge you in food and drink, or with regard to a feast, a new moon, or a Sabbath day —",
    17: "things which are a shadow of what is to come; but the substance belongs to Christ.",
    18: "Let no one disqualify you, taking pleasure in self-abasement and the worship of angels — going on in detail about visions he has seen, vainly puffed up by his fleshly mind,",
    19: "and not holding fast to the Head — from whom the whole body, nourished and held together by joints and ligaments, grows with the growth that is from God.",
    20: "If you died with Christ to the elementary principles of the world, why — as if you were still living in the world — do you submit yourselves to its decrees:",
    21: "\"Do not handle, do not taste, do not touch\"?",
    22: "(All these things refer to what perishes with use, in accord with the commandments and teachings of men.)",
    23: "These things have indeed an appearance of wisdom in self-imposed worship, false humility, and severity to the body — but are of no value against fleshly indulgence.",
}
ch3 = {
    1: "Therefore, if you have been raised with Christ, seek the things above — where Christ is, seated at the right hand of God.",
    2: "Set your minds on things above, not on things on the earth.",
    3: "For you have died, and your life is hidden with Christ in God.",
    4: "When Christ — who is our life — appears, then you also will appear with Him in glory.",
    5: "Therefore put to death whatever is earthly in you: sexual immorality, impurity, lust, evil desire, and greed — which is idolatry.",
    6: "On account of these things the wrath of God is coming upon the sons of disobedience —",
    7: "in which you yourselves once walked when you lived in them.",
    8: "But now, you yourselves are to put off all of these things: anger, wrath, malice, slander, and filthy speech from your mouth.",
    9: "Do not lie to one another, since you have put off the old self with its practices,",
    10: "and have put on the new self — which is being renewed in knowledge according to the image of Him who created him —",
    11: "where there is no Greek or Jew, circumcised or uncircumcised, barbarian, Scythian, slave, or free — but Christ is all, and is in all.",
    12: "Therefore, as God's chosen ones — holy and beloved — put on hearts of compassion, kindness, humility, gentleness, and patience.",
    13: "Bearing with one another, and forgiving one another — if anyone has a complaint against another. Just as the Lord forgave you, so you also must forgive.",
    14: "And above all these things, put on love — which is the bond of perfection.",
    15: "And let the peace of Christ rule in your hearts — to which indeed you were called in one body. And be thankful.",
    16: "Let the word of Christ dwell in you richly, in all wisdom — teaching and admonishing one another with psalms, hymns, and spiritual songs — singing with thankfulness in your hearts to God.",
    17: "And whatever you do, in word or in deed, do all in the name of the Lord Jesus, giving thanks to God the Father through Him.",
    18: "Wives, submit to your husbands, as is fitting in the Lord.",
    19: "Husbands, love your wives, and do not be embittered against them.",
    20: "Children, obey your parents in everything — for this is well-pleasing to the Lord.",
    21: "Fathers, do not provoke your children — so that they may not lose heart.",
    22: "Bondservants, obey in everything your earthly masters — not with eye-service, as people-pleasers, but with sincerity of heart, fearing the Lord.",
    23: "Whatever you do, do your work heartily — as for the Lord, and not for men;",
    24: "knowing that from the Lord you will receive the reward of the inheritance. It is the Lord Christ whom you serve.",
    25: "For the one who does wrong will be repaid for the wrong he has done — and there is no partiality.",
}
ch4 = {
    1: "Masters, treat your bondservants justly and fairly — knowing that you also have a Master in heaven.",
    2: "Devote yourselves to prayer — keeping alert in it, with thanksgiving.",
    3: "Pray for us at the same time — that God may open to us a door for the word, to speak the mystery of Christ, on account of which I am imprisoned —",
    4: "that I may make it clear, in the way I ought to speak.",
    5: "Walk in wisdom toward outsiders — making the most of the time.",
    6: "Let your speech always be with grace, seasoned with salt — so that you will know how you should answer each one.",
    7: "All my affairs Tychicus will make known to you — beloved brother, faithful minister, and fellow bondservant in the Lord.",
    8: "I have sent him to you for this very purpose — that you may know about us, and that he may encourage your hearts.",
    9: "He is coming with Onesimus — the faithful and beloved brother who is one of you. They will tell you about everything here.",
    10: "Aristarchus, my fellow prisoner, sends you greetings — and so does Mark, the cousin of Barnabas (concerning whom you received instructions: if he comes to you, welcome him);",
    11: "and Jesus who is called Justus. These are the only fellow workers from the circumcision for the kingdom of God — and they have been a comfort to me.",
    12: "Epaphras, who is one of you, a bondservant of Christ Jesus, sends you greetings — always wrestling on your behalf in his prayers, that you may stand mature and fully assured in all the will of God.",
    13: "For I bear him witness that he has worked hard for you, for those in Laodicea, and for those in Hierapolis.",
    14: "Luke, the beloved physician, sends you greetings — as does Demas.",
    15: "Greet the brothers in Laodicea, and Nympha and the church in her house.",
    16: "And when this letter has been read among you, see that it is read also in the church of the Laodiceans — and that you in turn read the letter from Laodicea.",
    17: "And say to Archippus, \"Take care to fulfill the ministry that you have received in the Lord.\"",
    18: "I, Paul, write this greeting with my own hand. Remember my chains. Grace be with you. Amen.",
}
CHAPTERS = {1: ch1, 2: ch2, 3: ch3, 4: ch4}

def main():
    new_entries = {f"51_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"Colossians total verses authored: {len(new_entries)}")
    with open(MBT_PATH) as f: existing = json.load(f)
    existing.update(new_entries)
    with open(MBT_PATH, "w") as f: json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"mbt-nt-extra.json: {len(existing)} total verses")
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f: json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT Colossians verses")

if __name__ == "__main__":
    main()
