"""MBT 1 Thessalonians — 5 chapters, 89 verses. Book ID 52."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_PATH = ROOT / "docs" / "assets" / "mbt-nt-extra.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "Paul, Silvanus, and Timothy — to the church of the Thessalonians, in God the Father and the Lord Jesus Christ: Grace to you, and peace.",
    2: "We give thanks to God always for all of you, mentioning you in our prayers,",
    3: "constantly remembering before our God and Father your work of faith, your labor of love, and your steadfastness of hope in our Lord Jesus Christ.",
    4: "Knowing, brothers — beloved by God — your election;",
    5: "for our gospel did not come to you in word only, but also in power, and in the Holy Spirit, and with full conviction — just as you know what kind of men we became among you for your sake.",
    6: "And you became imitators of us and of the Lord, having received the word in much affliction, with the joy of the Holy Spirit —",
    7: "so that you became an example to all the believers in Macedonia and in Achaia.",
    8: "For from you the word of the Lord has sounded forth — not only in Macedonia and Achaia, but in every place your faith toward God has gone out, so that we have no need to say anything.",
    9: "For they themselves report concerning us what kind of welcome we had among you — and how you turned to God from idols, to serve a living and true God,",
    10: "and to wait for His Son from heaven — whom He raised from the dead — Jesus, who delivers us from the wrath to come.",
}
ch2 = {
    1: "For you yourselves know, brothers, that our coming to you was not in vain.",
    2: "But after we had previously suffered and been treated shamefully at Philippi — as you know — we had courage in our God to speak to you the gospel of God, in the midst of much opposition.",
    3: "For our exhortation does not come from error, or from impurity, or by way of deceit;",
    4: "but just as we have been approved by God to be entrusted with the gospel, so we speak — not as pleasing men, but God who tests our hearts.",
    5: "For we never came with flattering speech, as you know — nor with a pretext for greed; God is witness.",
    6: "Nor did we seek glory from people — neither from you, nor from others — when we could have made demands as apostles of Christ.",
    7: "But we were gentle in your midst, like a nursing mother caring for her own children.",
    8: "So, having a deep affection for you, we were well-pleased to share with you not only the gospel of God, but also our own lives — because you had become beloved to us.",
    9: "For you remember, brothers, our toil and hardship — laboring night and day so as not to be a burden to any of you, while we proclaimed to you the gospel of God.",
    10: "You are witnesses, and so is God — how holy, righteous, and blameless was our conduct toward you who believe.",
    11: "Just as you know how, like a father with his own children, we were exhorting each one of you, and encouraging and imploring you,",
    12: "that you should walk in a manner worthy of God, who calls you into His own kingdom and glory.",
    13: "And for this reason we also constantly thank God — that when you received the word of God which you heard from us, you accepted it not as the word of men, but as it truly is, the word of God — which also is at work in you who believe.",
    14: "For you, brothers, became imitators of the churches of God in Christ Jesus that are in Judea — for you also suffered the same things from your own countrymen as they did from the Jews,",
    15: "who killed both the Lord Jesus and their own prophets, and drove us out — and they do not please God, and are hostile to all people,",
    16: "hindering us from speaking to the Gentiles so that they may be saved. Thus they always fill up the measure of their sins. But the wrath has come upon them at last.",
    17: "But we, brothers — having been torn away from you for a short time, in person but not in heart — were all the more eager and longing to see your face.",
    18: "For we wanted to come to you — I, Paul, more than once — but Satan hindered us.",
    19: "For who is our hope, our joy, or our crown of boasting? Is it not even you, in the presence of our Lord Jesus at His coming?",
    20: "For you are our glory and joy.",
}
ch3 = {
    1: "Therefore, when we could endure it no longer, we thought it best to be left behind in Athens alone,",
    2: "and we sent Timothy — our brother and God's fellow worker in the gospel of Christ — to strengthen you and encourage you concerning your faith,",
    3: "so that no one would be unsettled by these afflictions. For you yourselves know that we are appointed to this.",
    4: "For indeed, when we were with you, we kept telling you in advance that we were going to suffer affliction — just as it has come to pass, as you know.",
    5: "For this reason, when I could endure it no longer, I sent to find out about your faith — for fear that the tempter might have tempted you, and our labor would be in vain.",
    6: "But now Timothy has come to us from you and brought us good news of your faith and love — and that you always have good remembrance of us, longing to see us, just as we long to see you.",
    7: "For this reason, brothers — in all our affliction and distress — we were comforted concerning you through your faith.",
    8: "For now we live, if you stand firm in the Lord.",
    9: "For what thanksgiving can we render to God for you, for all the joy with which we rejoice on your account before our God,",
    10: "as we keep praying earnestly night and day that we may see your face and supply what is lacking in your faith?",
    11: "Now may our God and Father Himself, and our Lord Jesus, direct our way to you.",
    12: "And may the Lord cause you to increase and abound in love for one another and for all people, just as we also do for you,",
    13: "so that He may strengthen your hearts blameless in holiness before our God and Father at the coming of our Lord Jesus with all His saints.",
}
ch4 = {
    1: "Finally, then, brothers, we ask and exhort you in the Lord Jesus — that as you have received from us instruction concerning how you ought to walk and please God (just as you are doing) — that you excel still more.",
    2: "For you know what commands we gave you through the Lord Jesus.",
    3: "For this is the will of God: your sanctification — that you abstain from sexual immorality;",
    4: "that each of you know how to possess his own vessel in sanctification and honor;",
    5: "not in the passion of lust, like the Gentiles who do not know God;",
    6: "and that no one transgress and defraud his brother in this matter — because the Lord is the avenger in all these things, just as we also told you before and warned solemnly.",
    7: "For God did not call us for impurity, but for sanctification.",
    8: "Therefore he who rejects this is not rejecting man, but God — who gives His Holy Spirit to you.",
    9: "But concerning brotherly love, you have no need for anyone to write to you — for you yourselves are taught by God to love one another.",
    10: "For indeed you do practice it toward all the brothers throughout Macedonia. But we urge you, brothers, to excel still more,",
    11: "and to make it your ambition to live a quiet life, to mind your own business, and to work with your own hands — just as we commanded you,",
    12: "so that you may walk properly toward outsiders, and have need of nothing.",
    13: "But we do not want you to be uninformed, brothers, about those who have fallen asleep — so that you may not grieve like the rest, who have no hope.",
    14: "For if we believe that Jesus died and rose again, even so, through Jesus, God will bring with Him those who have fallen asleep.",
    15: "For this we say to you by the word of the Lord: that we who are alive — who remain until the coming of the Lord — will by no means precede those who have fallen asleep.",
    16: "For the Lord Himself will descend from heaven with a shout — with the voice of an archangel and with the trumpet of God — and the dead in Christ will rise first.",
    17: "Then we who are alive and remain will be caught up together with them in the clouds to meet the Lord in the air. And so we shall always be with the Lord.",
    18: "Therefore, comfort one another with these words.",
}
ch5 = {
    1: "Now concerning the times and the seasons, brothers, you have no need that anything be written to you.",
    2: "For you yourselves know full well that the day of the Lord will come like a thief in the night.",
    3: "When they say, \"Peace and safety!\" — then sudden destruction will come upon them, like labor pains upon a pregnant woman, and they will not escape.",
    4: "But you, brothers, are not in darkness — that the day should overtake you like a thief.",
    5: "You are all sons of light and sons of the day. We are not of the night, nor of darkness.",
    6: "So then, let us not sleep, as do the others — but let us watch and be sober.",
    7: "For those who sleep, sleep at night; and those who get drunk, are drunk at night.",
    8: "But since we are of the day, let us be sober — putting on the breastplate of faith and love, and as a helmet, the hope of salvation.",
    9: "For God did not appoint us to wrath — but to obtain salvation through our Lord Jesus Christ,",
    10: "who died for us, so that whether we are awake or asleep, we may live together with Him.",
    11: "Therefore encourage one another and build one another up — just as you also are doing.",
    12: "Now we ask you, brothers, to acknowledge those who labor among you, and are over you in the Lord, and admonish you;",
    13: "and esteem them very highly in love, because of their work. Be at peace among yourselves.",
    14: "And we urge you, brothers — admonish those who are unruly, encourage the fainthearted, help the weak, be patient with all.",
    15: "See that no one repays evil for evil — but always seek what is good for one another and for all people.",
    16: "Rejoice always.",
    17: "Pray without ceasing.",
    18: "In everything give thanks — for this is the will of God in Christ Jesus for you.",
    19: "Do not quench the Spirit.",
    20: "Do not despise prophecies.",
    21: "Test all things — hold fast to what is good.",
    22: "Abstain from every form of evil.",
    23: "Now may the God of peace Himself sanctify you completely. And may your whole spirit, soul, and body be preserved blameless at the coming of our Lord Jesus Christ.",
    24: "Faithful is He who calls you — He will also do it.",
    25: "Brothers, pray for us.",
    26: "Greet all the brothers with a holy kiss.",
    27: "I solemnly charge you by the Lord that this letter be read to all the brothers.",
    28: "The grace of our Lord Jesus Christ be with you. Amen.",
}
CHAPTERS = {1: ch1, 2: ch2, 3: ch3, 4: ch4, 5: ch5}

def main():
    new_entries = {f"52_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"1 Thessalonians total verses authored: {len(new_entries)}")
    with open(MBT_PATH) as f: existing = json.load(f)
    existing.update(new_entries)
    with open(MBT_PATH, "w") as f: json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"mbt-nt-extra.json: {len(existing)} total verses")
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f: json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT 1 Thess verses")

if __name__ == "__main__":
    main()
