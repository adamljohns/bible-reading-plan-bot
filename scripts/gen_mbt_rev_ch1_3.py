"""MBT Revelation 1-3 — Opening vision + Letters to the Seven Churches.
3 chapters, 71 verses. Book ID 66.

Style notes for Revelation specifically:
- Apocalyptic imagery preserved literally (no flattening of symbols)
- Christ's titles ('the Alpha and the Omega', 'the First and the Last',
  'who walks among the seven golden lampstands') kept distinct as the
  letters use the exact opening title from ch 1
- Reverential caps for all divine pronouns
- Direct address: 'I know your works' kept as exact opening across letters
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_PATH = ROOT / "docs" / "assets" / "mbt-nt-extra.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "The Revelation of Jesus Christ — which God gave Him to show to His bondservants the things that must shortly take place. He made it known by sending it through His angel to His bondservant John,",
    2: "who bore witness to the word of God and to the testimony of Jesus Christ — to all that he saw.",
    3: "Blessed is the one who reads, and those who hear the words of this prophecy and keep what is written in it — for the time is near.",
    4: "John — to the seven churches that are in Asia: Grace to you, and peace, from Him who is, and who was, and who is to come; and from the seven Spirits who are before His throne;",
    5: "and from Jesus Christ — the faithful witness, the firstborn from the dead, and the ruler of the kings of the earth. To Him who loves us and freed us from our sins by His blood —",
    6: "and made us a kingdom, priests to His God and Father — to Him be the glory and the dominion forever and ever. Amen.",
    7: "Behold, He is coming with the clouds — and every eye will see Him, including those who pierced Him. And all the tribes of the earth will mourn over Him. Yes, Amen.",
    8: "\"I am the Alpha and the Omega,\" says the Lord God, \"who is, and who was, and who is to come — the Almighty.\"",
    9: "I, John — your brother and fellow partaker in the tribulation, kingdom, and steadfast endurance which are in Jesus — was on the island called Patmos, because of the word of God and the testimony of Jesus.",
    10: "I came to be in the Spirit on the Lord's day — and I heard behind me a loud voice, like a trumpet,",
    11: "saying, \"Write what you see in a scroll, and send it to the seven churches — to Ephesus, Smyrna, Pergamum, Thyatira, Sardis, Philadelphia, and Laodicea.\"",
    12: "Then I turned to see the voice that was speaking with me. And having turned, I saw seven golden lampstands —",
    13: "and in the midst of the lampstands, One like a Son of Man — clothed in a robe down to His feet, and girded around the chest with a golden sash.",
    14: "His head and His hair were white like wool, white as snow. His eyes were like a flame of fire.",
    15: "His feet were like burnished bronze, refined as in a furnace. And His voice was like the sound of many waters.",
    16: "He had in His right hand seven stars, and out of His mouth came a sharp two-edged sword. And His face was like the sun shining in its strength.",
    17: "When I saw Him, I fell at His feet as one dead. And He laid His right hand on me, saying, \"Do not be afraid. I am the First and the Last,",
    18: "and the Living One. I was dead — and behold, I am alive forevermore. And I have the keys of Death and of Hades.",
    19: "Therefore, write the things you have seen, and the things that are, and the things that shall take place after these.",
    20: "As for the mystery of the seven stars you saw in My right hand, and of the seven golden lampstands: the seven stars are the angels of the seven churches, and the seven lampstands are the seven churches.\"",
}
ch2 = {
    1: "\"To the angel of the church in Ephesus write: These are the words of the One who holds the seven stars in His right hand — the One who walks in the midst of the seven golden lampstands:",
    2: "I know your deeds, your toil, and your steadfastness — and that you cannot tolerate evil men. You have tested those who call themselves apostles and are not, and have found them to be false.",
    3: "And you have steadfastness, and have endured for My name's sake, and have not grown weary.",
    4: "But I have this against you: that you have left your first love.",
    5: "Therefore, remember from where you have fallen — and repent, and do the deeds you did at first. Otherwise, I am coming to you, and I will remove your lampstand out of its place — unless you repent.",
    6: "But you have this in your favor: that you hate the deeds of the Nicolaitans, which I also hate.",
    7: "The one who has an ear, let him hear what the Spirit says to the churches: To the one who overcomes, I will grant to eat of the tree of life, which is in the paradise of God.\"",
    8: "\"And to the angel of the church in Smyrna write: These are the words of the First and the Last — the One who was dead, and has come to life:",
    9: "I know your tribulation and your poverty (yet you are rich) — and the slander of those who say they are Jews, and are not, but are a synagogue of Satan.",
    10: "Do not fear what you are about to suffer. Behold, the devil is about to throw some of you into prison, so that you may be tested. And you will have tribulation for ten days. Be faithful unto death, and I will give you the crown of life.",
    11: "The one who has an ear, let him hear what the Spirit says to the churches: The one who overcomes will not be hurt at all by the second death.\"",
    12: "\"And to the angel of the church in Pergamum write: These are the words of the One who has the sharp two-edged sword:",
    13: "I know where you live — where Satan's throne is. And you hold fast to My name, and did not deny My faith — even in the days of Antipas, My faithful witness, who was killed among you, where Satan dwells.",
    14: "But I have a few things against you: you have there those who hold to the teaching of Balaam — who taught Balak to put a stumbling block before the sons of Israel, to eat things sacrificed to idols and to commit sexual immorality.",
    15: "So you also have those who hold to the teaching of the Nicolaitans, in the same way.",
    16: "Therefore repent — or else I am coming to you quickly, and I will wage war against them with the sword of My mouth.",
    17: "The one who has an ear, let him hear what the Spirit says to the churches: To the one who overcomes, I will give some of the hidden manna. And I will give him a white stone — and on the stone, a new name written, which no one knows but the one who receives it.\"",
    18: "\"And to the angel of the church in Thyatira write: These are the words of the Son of God — whose eyes are like a flame of fire, and whose feet are like burnished bronze:",
    19: "I know your deeds — your love, faith, service, and steadfastness — and that your latest deeds are greater than the first.",
    20: "But I have this against you: that you tolerate the woman Jezebel — who calls herself a prophetess and teaches and seduces My bondservants to commit sexual immorality and to eat things sacrificed to idols.",
    21: "I gave her time to repent — and she does not want to repent of her immorality.",
    22: "Behold, I am throwing her on a sickbed — and those who commit adultery with her into great tribulation, unless they repent of her deeds.",
    23: "And I will kill her children with pestilence. Then all the churches will know that I am the One who searches the minds and hearts — and I will give to each of you according to your deeds.",
    24: "But to you I say — to the rest in Thyatira who do not hold to this teaching, who have not learned 'the deep things of Satan,' as they call them — I am laying no other burden on you;",
    25: "only hold fast to what you have, until I come.",
    26: "And the one who overcomes, and who keeps My deeds until the end — to him I will give authority over the nations.",
    27: "And he shall rule them with a rod of iron — as vessels of pottery are shattered — just as I also have received from My Father.",
    28: "And I will give him the morning star.",
    29: "The one who has an ear, let him hear what the Spirit says to the churches.\"",
}
ch3 = {
    1: "\"And to the angel of the church in Sardis write: These are the words of the One who has the seven Spirits of God and the seven stars: I know your deeds — that you have a name that you are alive, but you are dead.",
    2: "Be watchful — and strengthen the things that remain, which were about to die. For I have not found your deeds completed in the sight of My God.",
    3: "Therefore, remember what you have received and heard — and keep it, and repent. Therefore, if you do not watch, I will come like a thief, and you will not know at what hour I will come upon you.",
    4: "Yet you have a few names in Sardis who have not soiled their garments. They will walk with Me in white, because they are worthy.",
    5: "The one who overcomes will be clothed in white garments. And I will not erase his name from the Book of Life — and I will confess his name before My Father and before His angels.",
    6: "The one who has an ear, let him hear what the Spirit says to the churches.\"",
    7: "\"And to the angel of the church in Philadelphia write: These are the words of the Holy One, the True One — who has the key of David, who opens and no one will shut, and who shuts and no one opens:",
    8: "I know your deeds. Behold, I have set before you an open door, which no one is able to shut. For you have a little power, and have kept My word, and have not denied My name.",
    9: "Behold, I will cause those of the synagogue of Satan — who say they are Jews and are not, but lie — behold, I will make them to come and bow down at your feet, and to know that I have loved you.",
    10: "Because you have kept the word of My patient endurance, I also will keep you from the hour of testing — that hour which is about to come upon the whole world, to test those who dwell on the earth.",
    11: "I am coming quickly. Hold fast what you have, so that no one may take your crown.",
    12: "The one who overcomes — I will make him a pillar in the temple of My God, and he will not go out from it anymore. And I will write on him the name of My God, and the name of the city of My God — the new Jerusalem, which comes down out of heaven from My God — and My new name.",
    13: "The one who has an ear, let him hear what the Spirit says to the churches.\"",
    14: "\"And to the angel of the church in Laodicea write: These are the words of the Amen — the faithful and true Witness, the Beginning of God's creation:",
    15: "I know your deeds — that you are neither cold nor hot. I wish you were cold or hot.",
    16: "So because you are lukewarm — and neither hot nor cold — I am about to spit you out of My mouth.",
    17: "Because you say, 'I am rich, and have prospered, and have need of nothing' — and do not know that you are wretched, miserable, poor, blind, and naked —",
    18: "I counsel you to buy from Me gold refined by fire, that you may be rich; and white garments, that you may clothe yourself, and the shame of your nakedness may not be revealed; and salve to anoint your eyes, that you may see.",
    19: "Those whom I love, I rebuke and discipline. Therefore, be zealous and repent.",
    20: "Behold, I stand at the door and knock. If anyone hears My voice and opens the door, I will come in to him, and dine with him — and he with Me.",
    21: "The one who overcomes — I will grant to him to sit with Me on My throne, just as I also overcame and sat down with My Father on His throne.",
    22: "The one who has an ear, let him hear what the Spirit says to the churches.\"",
}
CHAPTERS = {1: ch1, 2: ch2, 3: ch3}

def main():
    new_entries = {f"66_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"Revelation 1-3 verses authored: {len(new_entries)}")
    with open(MBT_PATH) as f: existing = json.load(f)
    existing.update(new_entries)
    with open(MBT_PATH, "w") as f: json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"mbt-nt-extra.json: {len(existing)} total verses")
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f: json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT Revelation 1-3 verses")

if __name__ == "__main__":
    main()
