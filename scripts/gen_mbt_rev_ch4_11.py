"""MBT Revelation 4-11 — Throne room, scroll, seals, 144,000, trumpets,
two witnesses. 8 chapters, 123 verses. Book ID 66."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_PATH = ROOT / "docs" / "assets" / "mbt-nt-extra.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch4 = {
    1: "After these things I looked — and behold, a door standing open in heaven. And the first voice I had heard, like a trumpet speaking with me, said, \"Come up here, and I will show you what must take place after these things.\"",
    2: "Immediately I was in the Spirit — and behold, a throne stood in heaven, and One sitting on the throne.",
    3: "And the One sitting there had the appearance of jasper and carnelian. And a rainbow encircled the throne, like an emerald in appearance.",
    4: "Around the throne were twenty-four other thrones — and on the thrones I saw twenty-four elders sitting, clothed in white garments, with golden crowns on their heads.",
    5: "Out of the throne came flashes of lightning and rumblings and peals of thunder. And before the throne were burning seven lamps of fire — which are the seven Spirits of God.",
    6: "And before the throne was, as it were, a sea of glass — like crystal. And in the midst of the throne, and around the throne, were four living creatures full of eyes in front and behind.",
    7: "The first living creature was like a lion. The second living creature was like a calf. The third living creature had a face like a man. And the fourth living creature was like a flying eagle.",
    8: "And the four living creatures, each having six wings, were full of eyes around and within. And they have no rest, day or night, saying: \"Holy, holy, holy is the Lord God Almighty — who was, and who is, and who is to come!\"",
    9: "And whenever the living creatures give glory and honor and thanks to the One sitting on the throne — the One who lives forever and ever —",
    10: "the twenty-four elders fall down before the One sitting on the throne, and worship the One who lives forever and ever. And they cast their crowns before the throne, saying:",
    11: "\"Worthy are You, our Lord and our God, to receive the glory, and the honor, and the power — for You created all things, and on account of Your will they existed and were created.\"",
}
ch5 = {
    1: "And I saw in the right hand of the One sitting on the throne a scroll written within and on the back, sealed up with seven seals.",
    2: "And I saw a strong angel proclaiming with a loud voice: \"Who is worthy to open the scroll and to break its seals?\"",
    3: "And no one in heaven, nor on earth, nor under the earth, was able to open the scroll or to look into it.",
    4: "And I began to weep greatly, because no one was found worthy to open the scroll or to look into it.",
    5: "And one of the elders said to me, \"Stop weeping. Behold, the Lion that is from the tribe of Judah — the Root of David — has overcome, so as to open the scroll and its seven seals.\"",
    6: "And I saw, in the midst of the throne and the four living creatures, and in the midst of the elders, a Lamb standing — as if slain — having seven horns and seven eyes, which are the seven Spirits of God sent out into all the earth.",
    7: "And He came and took the scroll out of the right hand of the One sitting on the throne.",
    8: "And when He took the scroll, the four living creatures and the twenty-four elders fell down before the Lamb, each having a harp and golden bowls full of incense — which are the prayers of the saints.",
    9: "And they sang a new song, saying: \"Worthy are You to take the scroll and to break its seals — for You were slain, and You purchased for God by Your blood people from every tribe, tongue, people, and nation.",
    10: "And You have made them to be a kingdom and priests to our God; and they will reign on the earth.\"",
    11: "And I looked, and I heard the voice of many angels around the throne, and the living creatures, and the elders. The number of them was myriads of myriads, and thousands of thousands —",
    12: "saying with a loud voice: \"Worthy is the Lamb that was slain to receive the power, and riches, and wisdom, and might, and honor, and glory, and blessing!\"",
    13: "And every created thing that is in heaven, and on the earth, and under the earth, and on the sea, and all things in them — I heard them saying: \"To the One sitting on the throne, and to the Lamb, be the blessing, and the honor, and the glory, and the dominion forever and ever.\"",
    14: "And the four living creatures kept saying, \"Amen.\" And the elders fell down and worshiped.",
}
ch6 = {
    1: "And I saw when the Lamb broke one of the seven seals — and I heard one of the four living creatures saying, as with a voice of thunder, \"Come!\"",
    2: "And I looked, and behold, a white horse — and the one sitting on it had a bow. And a crown was given to him, and he went out conquering and to conquer.",
    3: "And when He broke the second seal, I heard the second living creature saying, \"Come!\"",
    4: "And another, a fiery red horse, came out. And to the one sitting on it, it was granted to take peace from the earth, and that men would slaughter one another. And a great sword was given to him.",
    5: "And when He broke the third seal, I heard the third living creature saying, \"Come!\" And I looked, and behold, a black horse — and the one sitting on it had a pair of scales in his hand.",
    6: "And I heard, as it were, a voice in the midst of the four living creatures, saying: \"A quart of wheat for a denarius, and three quarts of barley for a denarius — and do not damage the oil and the wine!\"",
    7: "And when He broke the fourth seal, I heard the voice of the fourth living creature saying, \"Come!\"",
    8: "And I looked, and behold, a pale-green horse. The one sitting on it — his name was Death, and Hades was following with him. And authority was given to them over a fourth of the earth — to kill with sword, and with famine, and with plague, and by the wild beasts of the earth.",
    9: "And when He broke the fifth seal, I saw underneath the altar the souls of those who had been slain because of the word of God and because of the testimony they had maintained.",
    10: "And they cried out with a loud voice, saying, \"How long, O Master — holy and true — until You judge and avenge our blood from those who dwell on the earth?\"",
    11: "And there was given to each of them a white robe — and they were told to rest yet a little while longer, until the number of their fellow servants and of their brothers — who were about to be killed even as they had been — would be completed.",
    12: "And I saw when He broke the sixth seal — and there was a great earthquake. And the sun became black as sackcloth made of hair, and the whole moon became like blood,",
    13: "and the stars of heaven fell to the earth, as a fig tree drops its unripe figs when shaken by a great wind.",
    14: "And the sky was split apart, like a scroll being rolled up. And every mountain and island was moved out of its place.",
    15: "And the kings of the earth, and the great men, and the commanders, and the rich, and the strong, and every slave and free man — hid themselves in the caves and among the rocks of the mountains.",
    16: "And they said to the mountains and to the rocks: \"Fall on us! And hide us from the face of the One sitting on the throne, and from the wrath of the Lamb!",
    17: "For the great day of Their wrath has come — and who is able to stand?\"",
}
ch7 = {
    1: "After this I saw four angels standing at the four corners of the earth — holding back the four winds of the earth, so that no wind would blow on the earth, or on the sea, or on any tree.",
    2: "And I saw another angel ascending from the rising of the sun, having the seal of the living God. And he cried out with a loud voice to the four angels to whom it had been granted to harm the earth and the sea,",
    3: "saying, \"Do not harm the earth, the sea, or the trees — until we have sealed the bondservants of our God on their foreheads.\"",
    4: "And I heard the number of those who were sealed: a hundred and forty-four thousand sealed — from every tribe of the sons of Israel.",
    5: "From the tribe of Judah, twelve thousand were sealed; from the tribe of Reuben, twelve thousand; from the tribe of Gad, twelve thousand;",
    6: "from the tribe of Asher, twelve thousand; from the tribe of Naphtali, twelve thousand; from the tribe of Manasseh, twelve thousand;",
    7: "from the tribe of Simeon, twelve thousand; from the tribe of Levi, twelve thousand; from the tribe of Issachar, twelve thousand;",
    8: "from the tribe of Zebulun, twelve thousand; from the tribe of Joseph, twelve thousand; from the tribe of Benjamin, twelve thousand were sealed.",
    9: "After these things I looked — and behold, a great multitude that no one could number, from every nation and all tribes and peoples and tongues, standing before the throne and before the Lamb. They were clothed in white robes, and palm branches were in their hands.",
    10: "And they cry out with a loud voice, saying: \"Salvation belongs to our God who sits on the throne, and to the Lamb!\"",
    11: "And all the angels were standing around the throne and around the elders and the four living creatures. And they fell on their faces before the throne and worshiped God,",
    12: "saying: \"Amen! The blessing, and the glory, and the wisdom, and the thanksgiving, and the honor, and the power, and the might, be to our God forever and ever. Amen.\"",
    13: "And one of the elders responded — saying to me, \"These who are clothed in the white robes — who are they, and where have they come from?\"",
    14: "And I said to him, \"My lord, you know.\" And he said to me, \"These are the ones who come out of the great tribulation. And they have washed their robes, and made them white, in the blood of the Lamb.",
    15: "For this reason, they are before the throne of God — and they serve Him day and night in His temple. And the One sitting on the throne will spread His tabernacle over them.",
    16: "They will hunger no more, neither thirst anymore. The sun will not strike them, nor any heat —",
    17: "for the Lamb in the midst of the throne will shepherd them, and will lead them to springs of the waters of life. And God will wipe away every tear from their eyes.\"",
}
ch8 = {
    1: "And when He broke the seventh seal, there was silence in heaven for about half an hour.",
    2: "And I saw the seven angels who stand before God — and seven trumpets were given to them.",
    3: "And another angel came and stood at the altar, having a golden censer. And much incense was given to him, so that he might add it to the prayers of all the saints — on the golden altar that is before the throne.",
    4: "And the smoke of the incense, with the prayers of the saints, went up before God out of the angel's hand.",
    5: "And the angel took the censer, and filled it with the fire of the altar, and threw it to the earth. And there were peals of thunder and rumblings and flashes of lightning and an earthquake.",
    6: "And the seven angels who had the seven trumpets prepared themselves to sound them.",
    7: "The first sounded — and there came hail and fire mixed with blood, and they were thrown to the earth. And a third of the earth was burned up, and a third of the trees were burned up, and all the green grass was burned up.",
    8: "And the second angel sounded — and something like a great mountain burning with fire was thrown into the sea. And a third of the sea became blood;",
    9: "and a third of the creatures in the sea — those that had life — died; and a third of the ships were destroyed.",
    10: "And the third angel sounded — and a great star fell from heaven, blazing like a torch. And it fell on a third of the rivers and on the springs of waters.",
    11: "And the name of the star is called Wormwood. And a third of the waters became wormwood — and many people died from the waters, because they had been made bitter.",
    12: "And the fourth angel sounded — and a third of the sun was struck, and a third of the moon, and a third of the stars, so that a third of them was darkened. And the day did not shine for a third of it — and the night likewise.",
    13: "And I looked, and I heard an eagle flying in midheaven, saying with a loud voice: \"Woe, woe, woe to those who dwell on the earth — because of the remaining trumpet blasts of the three angels who are about to sound!\"",
}
ch9 = {
    1: "And the fifth angel sounded — and I saw a star from heaven that had fallen to the earth. And the key of the shaft of the abyss was given to him.",
    2: "And he opened the shaft of the abyss — and smoke went up out of the shaft, like the smoke of a great furnace. And the sun and the air were darkened by the smoke of the shaft.",
    3: "And out of the smoke came forth locusts on the earth — and authority was given to them, like the authority of scorpions of the earth.",
    4: "And they were told not to harm the grass of the earth, nor any green plant, nor any tree — but only the men who do not have the seal of God on their foreheads.",
    5: "And it was given to them not to kill them — but to torment them for five months. And their torment was like the torment of a scorpion when it stings a man.",
    6: "And in those days, men will seek death and will not find it. They will long to die — and death will flee from them.",
    7: "And the appearance of the locusts was like horses prepared for battle. And on their heads were what looked like crowns of gold, and their faces were like the faces of men.",
    8: "And they had hair like the hair of women — and their teeth were like the teeth of lions.",
    9: "And they had breastplates like breastplates of iron — and the sound of their wings was like the sound of chariots, of many horses rushing into battle.",
    10: "And they had tails like scorpions, and stings — and in their tails was their authority to harm men for five months.",
    11: "They have over them a king — the angel of the abyss. His name in Hebrew is Abaddon, and in Greek he has the name Apollyon.",
    12: "The first woe is past. Behold, two more woes are still coming after these things.",
    13: "And the sixth angel sounded — and I heard a single voice from the four horns of the golden altar that is before God,",
    14: "saying to the sixth angel who had the trumpet, \"Release the four angels who are bound at the great river Euphrates.\"",
    15: "And the four angels were released — those who had been prepared for the hour and day and month and year — to kill a third of mankind.",
    16: "And the number of the troops of the cavalry was two hundred million. I heard their number.",
    17: "And this is how I saw the horses in the vision, and those sitting on them: they had breastplates the color of fire, and of hyacinth, and of brimstone. And the heads of the horses were like the heads of lions — and out of their mouths proceeded fire and smoke and brimstone.",
    18: "By these three plagues, a third of mankind was killed — by the fire and the smoke and the brimstone that came out of their mouths.",
    19: "For the authority of the horses is in their mouths and in their tails — for their tails are like serpents, having heads, and with them they do harm.",
    20: "And the rest of mankind, who were not killed by these plagues, did not repent of the works of their hands — that they should not worship demons and the idols of gold and silver and bronze and stone and wood, which can neither see nor hear nor walk.",
    21: "And they did not repent of their murders, nor of their sorceries, nor of their immorality, nor of their thefts.",
}
ch10 = {
    1: "And I saw another mighty angel coming down from heaven — clothed with a cloud, and a rainbow was on his head. His face was like the sun, and his feet like pillars of fire.",
    2: "And he had in his hand a little scroll, opened. And he placed his right foot on the sea, and his left on the land —",
    3: "and he cried out with a loud voice, like the roaring of a lion. And when he cried out, the seven thunders uttered their voices.",
    4: "And when the seven thunders had spoken, I was about to write — and I heard a voice from heaven saying, \"Seal up the things which the seven thunders have spoken — and do not write them.\"",
    5: "And the angel whom I saw standing on the sea and on the land lifted up his right hand to heaven,",
    6: "and swore by the One who lives forever and ever — who created heaven and the things in it, and the earth and the things in it, and the sea and the things in it — that there will be delay no longer.",
    7: "But in the days of the voice of the seventh angel, when he is about to sound, then the mystery of God is finished — as He proclaimed to His servants the prophets.",
    8: "And the voice that I heard from heaven, I heard again, speaking to me — and saying, \"Go, take the scroll that is open in the hand of the angel who is standing on the sea and on the land.\"",
    9: "And I went to the angel, telling him to give me the little scroll. And he said to me, \"Take it and eat it — and it will make your stomach bitter, but in your mouth it will be sweet as honey.\"",
    10: "And I took the little scroll out of the angel's hand, and ate it. And in my mouth it was sweet as honey — but when I had eaten it, my stomach was made bitter.",
    11: "And he said to me, \"You must prophesy again about many peoples and nations and tongues and kings.\"",
}
ch11 = {
    1: "And there was given to me a measuring rod, like a staff. And he said, \"Get up and measure the temple of God, and the altar, and those who worship in it.",
    2: "But the court that is outside the temple, leave it out — and do not measure it. For it has been given to the nations, and they will trample the holy city for forty-two months.",
    3: "And I will give authority to My two witnesses — and they will prophesy for one thousand two hundred and sixty days, clothed in sackcloth.\"",
    4: "These are the two olive trees and the two lampstands that stand before the Lord of the earth.",
    5: "And if anyone wants to harm them, fire flows out of their mouth and devours their enemies — and if anyone wants to harm them, in this manner he must be killed.",
    6: "These have authority to shut up the sky, so that rain does not fall during the days of their prophesying. And they have authority over the waters, to turn them into blood — and to strike the earth with every plague, as often as they desire.",
    7: "And when they have finished their testimony, the beast that comes up out of the abyss will make war with them — and will overcome them and kill them.",
    8: "And their dead bodies will lie in the street of the great city — which spiritually is called Sodom and Egypt — where also their Lord was crucified.",
    9: "And those from the peoples and tribes and tongues and nations look at their dead bodies for three and a half days. And they do not permit their dead bodies to be laid in a tomb.",
    10: "And those who dwell on the earth will rejoice over them and celebrate — and they will send gifts to one another, because these two prophets had tormented those who dwell on the earth.",
    11: "And after the three and a half days, the breath of life from God came into them — and they stood on their feet. And great fear fell upon those who saw them.",
    12: "And they heard a loud voice from heaven, saying to them, \"Come up here.\" And they went up into heaven in the cloud — and their enemies watched them.",
    13: "And in that hour there was a great earthquake — and a tenth of the city fell. And seven thousand people were killed in the earthquake. And the rest were terrified, and gave glory to the God of heaven.",
    14: "The second woe is past. Behold, the third woe is coming quickly.",
    15: "And the seventh angel sounded — and there were loud voices in heaven, saying: \"The kingdom of the world has become the kingdom of our Lord and of His Christ — and He will reign forever and ever.\"",
    16: "And the twenty-four elders, who sit on their thrones before God, fell on their faces and worshiped God,",
    17: "saying: \"We give You thanks, O Lord God Almighty — the One who is and who was — because You have taken Your great power and have begun to reign.",
    18: "And the nations were enraged — and Your wrath came, and the time came for the dead to be judged, and to give the reward to Your bondservants the prophets, and to the saints, and to those who fear Your name — the small and the great — and to destroy those who destroy the earth.\"",
    19: "And the temple of God in heaven was opened, and the ark of His covenant was seen in His temple. And there were flashes of lightning and rumblings and peals of thunder and an earthquake and great hail.",
}
CHAPTERS = {4: ch4, 5: ch5, 6: ch6, 7: ch7, 8: ch8, 9: ch9, 10: ch10, 11: ch11}

def main():
    new_entries = {f"66_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"Revelation 4-11 verses authored: {len(new_entries)}")
    with open(MBT_PATH) as f: existing = json.load(f)
    existing.update(new_entries)
    with open(MBT_PATH, "w") as f: json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"mbt-nt-extra.json: {len(existing)} total verses")
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f: json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT Revelation 4-11 verses")

if __name__ == "__main__":
    main()
