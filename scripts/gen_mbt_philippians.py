"""MBT Philippians — 4 chapters, 104 verses. Book ID 50."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_PATH = ROOT / "docs" / "assets" / "mbt-nt-extra.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "Paul and Timothy, bondservants of Christ Jesus — to all the saints in Christ Jesus who are in Philippi, with the overseers and deacons:",
    2: "Grace to you, and peace from God our Father and the Lord Jesus Christ.",
    3: "I thank my God in all my remembrance of you,",
    4: "always — in every prayer of mine for you all — making my prayer with joy,",
    5: "because of your partnership in the gospel from the first day until now.",
    6: "I am confident of this very thing: that He who began a good work in you will bring it to completion at the day of Jesus Christ.",
    7: "It is right for me to think this way about all of you — because I have you in my heart, since both in my chains and in the defense and confirmation of the gospel, all of you share with me in this grace.",
    8: "For God is my witness — how I long for all of you with the affection of Christ Jesus.",
    9: "And this is my prayer: that your love may abound still more and more, in full knowledge and all discernment,",
    10: "so that you may approve the things that are excellent — that you may be sincere and blameless until the day of Christ,",
    11: "filled with the fruit of righteousness which comes through Jesus Christ — to the glory and praise of God.",
    12: "Now I want you to know, brothers, that what has happened to me has actually served to advance the gospel,",
    13: "so that my chains in Christ have become known throughout the whole praetorian guard, and to all the rest;",
    14: "and most of the brothers, having confidence in the Lord because of my chains, are much more bold to speak the word without fear.",
    15: "Some, indeed, preach Christ even out of envy and rivalry — but others out of good will.",
    16: "These do it out of love, knowing that I am put here for the defense of the gospel.",
    17: "But the others proclaim Christ out of selfish ambition, not sincerely — supposing they will add affliction to my chains.",
    18: "What then? Only that in every way, whether in pretense or in truth, Christ is proclaimed — and in this I rejoice. Yes, and I will continue to rejoice.",
    19: "For I know that this will turn out for my deliverance through your prayer and the supply of the Spirit of Jesus Christ,",
    20: "according to my eager expectation and hope — that I will not be put to shame in anything, but that with all boldness, as always, even now Christ will be magnified in my body, whether through life or through death.",
    21: "For to me, to live is Christ — and to die is gain.",
    22: "But if I am to live on in the flesh, this will mean fruitful labor for me. Yet what I shall choose, I cannot tell.",
    23: "I am hard-pressed between the two — having the desire to depart and be with Christ, for that is far better.",
    24: "But to remain in the flesh is more necessary for your sake.",
    25: "And being convinced of this, I know that I will remain — and I will continue with you all for your progress and joy in the faith,",
    26: "so that your boasting may abound in Christ Jesus on account of me, through my coming to you again.",
    27: "Only let your conduct be worthy of the gospel of Christ — so that whether I come and see you, or am absent, I may hear of your circumstances: that you stand firm in one spirit, with one mind striving together for the faith of the gospel,",
    28: "and not in any way frightened by your opponents. This is a sign of destruction to them, but of your salvation — and that from God.",
    29: "For it has been granted to you for the sake of Christ — not only to believe in Him, but also to suffer for His sake,",
    30: "having the same conflict that you saw in me, and now hear to be in me.",
}
ch2 = {
    1: "If, then, there is any encouragement in Christ, any comfort of love, any fellowship of the Spirit, any affection and compassion,",
    2: "make my joy complete — by being of the same mind, having the same love, being united in spirit, intent on one purpose.",
    3: "Do nothing from selfish ambition or empty conceit. Rather, in humility consider others as more important than yourselves.",
    4: "Do not look out only for your own interests, but also for the interests of others.",
    5: "Have this mind among yourselves, which was also in Christ Jesus —",
    6: "who, although He existed in the form of God, did not regard equality with God a thing to be grasped,",
    7: "but emptied Himself, taking the form of a bondservant, being made in the likeness of men.",
    8: "And being found in appearance as a man, He humbled Himself by becoming obedient — to the point of death, even death on a cross.",
    9: "For this reason God highly exalted Him, and bestowed on Him the name that is above every name —",
    10: "so that at the name of Jesus every knee will bow — of those in heaven, and on earth, and under the earth —",
    11: "and that every tongue will confess that Jesus Christ is Lord, to the glory of God the Father.",
    12: "Therefore, my beloved, just as you have always obeyed — not as in my presence only, but now much more in my absence — work out your salvation with fear and trembling.",
    13: "For it is God who is at work in you — both to will and to work for His good pleasure.",
    14: "Do all things without grumbling and disputing,",
    15: "so that you may be blameless and innocent — children of God without blemish, in the midst of a crooked and perverse generation, among whom you shine as lights in the world,",
    16: "holding fast the word of life — so that I may have reason to boast on the day of Christ that I did not run in vain, nor labor in vain.",
    17: "But even if I am being poured out as a drink offering on the sacrifice and service of your faith, I rejoice — and I rejoice with you all.",
    18: "And in the same way, you also should rejoice — and rejoice with me.",
    19: "But I hope in the Lord Jesus to send Timothy to you shortly — so that I also may be encouraged when I learn of your circumstances.",
    20: "For I have no one else of kindred spirit, who will genuinely care about your welfare.",
    21: "For all of them seek their own interests — not those of Christ Jesus.",
    22: "But you know of his proven worth — that as a child with a father, he served with me in the gospel.",
    23: "Therefore I hope to send him at once, as soon as I see how things go with me.",
    24: "And I trust in the Lord that I myself also will come shortly.",
    25: "But I thought it necessary to send to you Epaphroditus — my brother and fellow worker and fellow soldier — your messenger and minister to my need.",
    26: "For he was longing for all of you, and was distressed because you had heard that he was sick.",
    27: "Indeed, he was sick to the point of death. But God had mercy on him — and not on him only, but also on me, lest I should have sorrow upon sorrow.",
    28: "Therefore I have sent him all the more eagerly — that when you see him again, you may rejoice, and I may be less anxious.",
    29: "Welcome him in the Lord with all joy, and hold men like him in honor —",
    30: "because he came close to death for the work of Christ, risking his life to fill up what was lacking in your service to me.",
}
ch3 = {
    1: "Finally, my brothers, rejoice in the Lord. To write the same things again is no trouble to me — and is a safeguard for you.",
    2: "Beware of the dogs. Beware of the evil workers. Beware of the false circumcision.",
    3: "For we are the true circumcision — who worship in the Spirit of God, and glory in Christ Jesus, and put no confidence in the flesh —",
    4: "though I myself might have confidence even in the flesh. If anyone else thinks he has reason to put confidence in the flesh, I have more:",
    5: "circumcised the eighth day, of the people of Israel, of the tribe of Benjamin, a Hebrew of Hebrews; as to the law, a Pharisee;",
    6: "as to zeal, persecuting the church; as to the righteousness which is in the law, found blameless.",
    7: "But whatever things were gain to me, these I have counted as loss for the sake of Christ.",
    8: "Indeed I count all things as loss for the surpassing worth of knowing Christ Jesus my Lord — for whose sake I have suffered the loss of all things, and count them but rubbish, that I may gain Christ —",
    9: "and be found in Him, not having a righteousness of my own which is from the law, but that which is through faith in Christ — the righteousness which is from God by faith;",
    10: "that I may know Him, and the power of His resurrection, and the fellowship of His sufferings — being conformed to His death,",
    11: "if by any means I may attain to the resurrection from the dead.",
    12: "Not that I have already received it, or have already become perfect — but I press on, so that I may take hold of that for which I was also taken hold of by Christ Jesus.",
    13: "Brothers, I do not regard myself as having yet taken hold of it. But one thing I do — forgetting what lies behind, and reaching forward to what lies ahead —",
    14: "I press on toward the goal for the prize of the upward call of God in Christ Jesus.",
    15: "Therefore as many as are mature, let us think this way. And if you think differently in any way, this also God will reveal to you.",
    16: "Only let us live up to the standard we have already attained.",
    17: "Brothers, join in following my example — and observe those who walk according to the pattern you have in us.",
    18: "For many walk — of whom I have often told you, and now tell you even weeping — that they are enemies of the cross of Christ;",
    19: "whose end is destruction, whose god is their belly, whose glory is in their shame, who set their minds on earthly things.",
    20: "But our citizenship is in heaven — from which we also eagerly wait for a Savior, the Lord Jesus Christ,",
    21: "who will transform our lowly body to be conformed to His glorious body — by the working by which He is able even to subject all things to Himself.",
}
ch4 = {
    1: "Therefore, my brothers — beloved and longed-for, my joy and crown — stand firm in the Lord, my beloved.",
    2: "I plead with Euodia and I plead with Syntyche — to be of the same mind in the Lord.",
    3: "Yes, I ask you also, true companion, help these women who labored with me in the gospel — together with Clement and the rest of my fellow workers, whose names are in the Book of Life.",
    4: "Rejoice in the Lord always. I will say it again — rejoice!",
    5: "Let your gentleness be known to all people. The Lord is near.",
    6: "Be anxious for nothing — but in everything, by prayer and supplication, with thanksgiving, let your requests be made known to God.",
    7: "And the peace of God, which surpasses all understanding, will guard your hearts and minds in Christ Jesus.",
    8: "Finally, brothers, whatever is true, whatever is honorable, whatever is right, whatever is pure, whatever is lovely, whatever is of good repute — if there is any excellence and if anything worthy of praise — dwell on these things.",
    9: "The things you have learned and received and heard and seen in me — practice these things. And the God of peace will be with you.",
    10: "But I rejoiced in the Lord greatly — that now at last you have revived your concern for me. Indeed you were concerned, but you lacked opportunity.",
    11: "Not that I am speaking from need — for I have learned, in whatever circumstances I am, to be content.",
    12: "I know how to live humbly, and I know also how to live in abundance. In any and every circumstance, I have learned the secret — both how to be filled, and how to go hungry; both how to abound, and how to suffer need.",
    13: "I can do all things through Him who strengthens me.",
    14: "Nevertheless, you have done well to share with me in my affliction.",
    15: "And you yourselves know, Philippians, that at the beginning of the gospel — when I left Macedonia — no church entered into partnership with me in the matter of giving and receiving, except you only.",
    16: "For even at Thessalonica, you sent gifts more than once for my needs.",
    17: "Not that I seek the gift — but I seek the fruit that is increasing to your account.",
    18: "But I have received everything in full and have an abundance. I am amply supplied — having received from Epaphroditus the things you sent — a fragrant aroma, an acceptable sacrifice, well-pleasing to God.",
    19: "And my God will supply all your needs according to His riches in glory in Christ Jesus.",
    20: "Now to our God and Father be the glory forever and ever. Amen.",
    21: "Greet every saint in Christ Jesus. The brothers who are with me greet you.",
    22: "All the saints greet you — especially those who are of Caesar's household.",
    23: "The grace of the Lord Jesus Christ be with your spirit. Amen.",
}
CHAPTERS = {1: ch1, 2: ch2, 3: ch3, 4: ch4}

def main():
    new_entries = {f"50_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"Philippians total verses authored: {len(new_entries)}")
    with open(MBT_PATH) as f: existing = json.load(f)
    existing.update(new_entries)
    with open(MBT_PATH, "w") as f: json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"mbt-nt-extra.json: {len(existing)} total verses")
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f: json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT Philippians verses")

if __name__ == "__main__":
    main()
