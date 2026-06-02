"""MBT generator: Isaiah landmark chapters.

Book ID 23. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Isaiah 6 (13 verses) — the throne vision, "Holy, holy, holy"
- Isaiah 9:1-7 (7 verses) — "For unto us a Child is born"
- Isaiah 40 (31 verses) — "Comfort, comfort My people"
- Isaiah 53 (12 verses) — the Suffering Servant
- Isaiah 55 (13 verses) — "Ho, every one who thirsts"

Total: 76 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Isaiah 6 — Isaiah's throne vision and commission
ch6 = {
    1: "In the year that King Uzziah died, I saw the Lord sitting on a throne, high and lifted up, and the train of His robe filled the temple.",
    2: "Above it stood seraphim; each one had six wings: with two he covered his face, with two he covered his feet, and with two he flew.",
    3: "And one cried to another and said: \"Holy, holy, holy is the LORD of hosts; the whole earth is full of His glory!\"",
    4: "And the posts of the door were shaken by the voice of him who cried out, and the house was filled with smoke.",
    5: "So I said: \"Woe is me, for I am undone! Because I am a man of unclean lips, and I dwell in the midst of a people of unclean lips; for my eyes have seen the King, the LORD of hosts.\"",
    6: "Then one of the seraphim flew to me, having in his hand a live coal which he had taken with the tongs from the altar.",
    7: "And he touched my mouth with it, and said: \"Behold, this has touched your lips; your iniquity is taken away, and your sin purged.\"",
    8: "Also I heard the voice of the Lord, saying: \"Whom shall I send, and who will go for Us?\" Then I said, \"Here am I! Send me.\"",
    9: "And He said, \"Go, and tell this people: 'Keep on hearing, but do not understand; keep on seeing, but do not perceive.'",
    10: "Make the heart of this people dull, and their ears heavy, and shut their eyes; lest they see with their eyes, and hear with their ears, and understand with their heart, and return and be healed.\"",
    11: "Then I said, \"Lord, how long?\" And He answered: \"Until the cities are laid waste and without inhabitant, the houses are without a man, the land is utterly desolate,",
    12: "the LORD has removed men far away, and the forsaken places are many in the midst of the land.",
    13: "But yet a tenth will be in it, and will return and be for consuming, as a terebinth tree or as an oak, whose stump remains when it is cut down. So the holy seed shall be its stump.\"",
}

# Isaiah 9:1-7 — The Child is born
ch9 = {
    1: "Nevertheless the gloom will not be upon her who is distressed, as when at first He lightly esteemed the land of Zebulun and the land of Naphtali, and afterward more heavily oppressed her, by the way of the sea, beyond the Jordan, in Galilee of the Gentiles.",
    2: "The people who walked in darkness have seen a great light; those who dwelt in the land of the shadow of death — upon them a light has shined.",
    3: "You have multiplied the nation and increased its joy; they rejoice before You according to the joy of harvest, as men rejoice when they divide the spoil.",
    4: "For You have broken the yoke of his burden and the staff of his shoulder, the rod of his oppressor, as in the day of Midian.",
    5: "For every warrior's sandal from the noisy battle, and garments rolled in blood, will be used for burning and fuel of fire.",
    6: "For unto us a Child is born, unto us a Son is given; and the government will be upon His shoulder. And His name will be called Wonderful, Counselor, Mighty God, Everlasting Father, Prince of Peace.",
    7: "Of the increase of His government and peace there will be no end, upon the throne of David and over His kingdom, to order it and establish it with judgment and justice from that time forward, even forever. The zeal of the LORD of hosts will perform this.",
}

# Isaiah 40 — "Comfort, comfort My people"
ch40 = {
    1: "\"Comfort, yes, comfort My people!\" says your God.",
    2: "\"Speak comfort to Jerusalem, and cry out to her, that her warfare is ended, that her iniquity is pardoned; for she has received from the LORD's hand double for all her sins.\"",
    3: "The voice of one crying in the wilderness: \"Prepare the way of the LORD; make straight in the desert a highway for our God.",
    4: "Every valley shall be exalted and every mountain and hill brought low; the crooked places shall be made straight and the rough places smooth;",
    5: "the glory of the LORD shall be revealed, and all flesh shall see it together; for the mouth of the LORD has spoken.\"",
    6: "The voice said, \"Cry out!\" And he said, \"What shall I cry?\" \"All flesh is grass, and all its loveliness is like the flower of the field.",
    7: "The grass withers, the flower fades, because the breath of the LORD blows upon it; surely the people are grass.",
    8: "The grass withers, the flower fades, but the word of our God stands forever.\"",
    9: "O Zion, you who bring good tidings, get up into the high mountain; O Jerusalem, you who bring good tidings, lift up your voice with strength, lift it up, be not afraid. Say to the cities of Judah, \"Behold your God!\"",
    10: "Behold, the Lord GOD shall come with a strong hand, and His arm shall rule for Him; behold, His reward is with Him, and His work before Him.",
    11: "He will feed His flock like a shepherd; He will gather the lambs with His arm, and carry them in His bosom, and gently lead those who are with young.",
    12: "Who has measured the waters in the hollow of His hand, measured heaven with a span and calculated the dust of the earth in a measure? Who has weighed the mountains in scales and the hills in a balance?",
    13: "Who has directed the Spirit of the LORD, or as His counselor has taught Him?",
    14: "With whom did He take counsel, and who instructed Him, and taught Him in the path of justice? Who taught Him knowledge, and showed Him the way of understanding?",
    15: "Behold, the nations are as a drop in a bucket, and are counted as the small dust on the scales; look, He lifts up the isles as a very little thing.",
    16: "And Lebanon is not sufficient to burn, nor its beasts sufficient for a burnt offering.",
    17: "All nations before Him are as nothing, and they are counted by Him less than nothing and worthless.",
    18: "To whom then will you liken God? Or what likeness will you compare to Him?",
    19: "The workman molds an image, the goldsmith overspreads it with gold, and the silversmith casts silver chains.",
    20: "Whoever is too impoverished for such a contribution chooses a tree that will not rot; he seeks for himself a skillful workman to prepare a carved image that will not totter.",
    21: "Have you not known? Have you not heard? Has it not been told you from the beginning? Have you not understood from the foundations of the earth?",
    22: "It is He who sits above the circle of the earth, and its inhabitants are like grasshoppers, who stretches out the heavens like a curtain, and spreads them out like a tent to dwell in.",
    23: "He brings the princes to nothing; He makes the judges of the earth useless.",
    24: "Scarcely shall they be planted, scarcely shall they be sown, scarcely shall their stock take root in the earth, when He will also blow on them, and they will wither, and the whirlwind will take them away like stubble.",
    25: "\"To whom then will you liken Me, or to whom shall I be equal?\" says the Holy One.",
    26: "Lift up your eyes on high, and see who has created these things, who brings out their host by number; He calls them all by name, by the greatness of His might and the strength of His power; not one is missing.",
    27: "Why do you say, O Jacob, and speak, O Israel: \"My way is hidden from the LORD, and my just claim is passed over by my God\"?",
    28: "Have you not known? Have you not heard? The everlasting God, the LORD, the Creator of the ends of the earth, neither faints nor is weary. His understanding is unsearchable.",
    29: "He gives power to the weak, and to those who have no might He increases strength.",
    30: "Even the youths shall faint and be weary, and the young men shall utterly fall;",
    31: "but those who wait on the LORD shall renew their strength; they shall mount up with wings like eagles, they shall run and not be weary, they shall walk and not faint.",
}

# Isaiah 53 — The Suffering Servant
ch53 = {
    1: "Who has believed our report? And to whom has the arm of the LORD been revealed?",
    2: "For He shall grow up before Him as a tender plant, and as a root out of dry ground. He has no form or comeliness; and when we see Him, there is no beauty that we should desire Him.",
    3: "He is despised and rejected by men, a Man of sorrows and acquainted with grief. And we hid, as it were, our faces from Him; He was despised, and we did not esteem Him.",
    4: "Surely He has borne our griefs and carried our sorrows; yet we esteemed Him stricken, smitten by God, and afflicted.",
    5: "But He was wounded for our transgressions, He was bruised for our iniquities; the chastisement for our peace was upon Him, and by His stripes we are healed.",
    6: "All we like sheep have gone astray; we have turned, every one, to his own way; and the LORD has laid on Him the iniquity of us all.",
    7: "He was oppressed and He was afflicted, yet He opened not His mouth; He was led as a lamb to the slaughter, and as a sheep before its shearers is silent, so He opened not His mouth.",
    8: "He was taken from prison and from judgment, and who will declare His generation? For He was cut off from the land of the living; for the transgressions of My people He was stricken.",
    9: "And they made His grave with the wicked — but with the rich at His death, because He had done no violence, nor was any deceit in His mouth.",
    10: "Yet it pleased the LORD to bruise Him; He has put Him to grief. When You make His soul an offering for sin, He shall see His seed, He shall prolong His days, and the pleasure of the LORD shall prosper in His hand.",
    11: "He shall see the labor of His soul, and be satisfied. By His knowledge My righteous Servant shall justify many, for He shall bear their iniquities.",
    12: "Therefore I will divide Him a portion with the great, and He shall divide the spoil with the strong, because He poured out His soul unto death, and He was numbered with the transgressors, and He bore the sin of many, and made intercession for the transgressors.",
}

# Isaiah 55 — The open invitation
ch55 = {
    1: "\"Ho! Everyone who thirsts, come to the waters; and you who have no money, come, buy and eat. Yes, come, buy wine and milk without money and without price.",
    2: "Why do you spend money for what is not bread, and your wages for what does not satisfy? Listen carefully to Me, and eat what is good, and let your soul delight itself in abundance.",
    3: "Incline your ear, and come to Me. Hear, and your soul shall live; and I will make an everlasting covenant with you — the sure mercies of David.",
    4: "Indeed I have given him as a witness to the people, a leader and commander for the people.",
    5: "Surely you shall call a nation you do not know, and nations who do not know you shall run to you, because of the LORD your God, and the Holy One of Israel; for He has glorified you.\"",
    6: "Seek the LORD while He may be found, call upon Him while He is near.",
    7: "Let the wicked forsake his way, and the unrighteous man his thoughts; let him return to the LORD, and He will have mercy on him; and to our God, for He will abundantly pardon.",
    8: "\"For My thoughts are not your thoughts, nor are your ways My ways,\" says the LORD.",
    9: "\"For as the heavens are higher than the earth, so are My ways higher than your ways, and My thoughts than your thoughts.",
    10: "For as the rain comes down, and the snow from heaven, and do not return there, but water the earth, and make it bring forth and bud, that it may give seed to the sower and bread to the eater,",
    11: "so shall My word be that goes forth from My mouth; it shall not return to Me void, but it shall accomplish what I please, and it shall prosper in the thing for which I sent it.",
    12: "For you shall go out with joy, and be led out with peace; the mountains and the hills shall break forth into singing before you, and all the trees of the field shall clap their hands.",
    13: "Instead of the thorn shall come up the cypress tree, and instead of the brier shall come up the myrtle tree; and it shall be to the LORD for a name, for an everlasting sign that shall not be cut off.\"",
}

ENTRIES = {}
for v, t in ch6.items():
    ENTRIES[f"23_6_{v}"] = t
for v, t in ch9.items():
    ENTRIES[f"23_9_{v}"] = t
for v, t in ch40.items():
    ENTRIES[f"23_40_{v}"] = t
for v, t in ch53.items():
    ENTRIES[f"23_53_{v}"] = t
for v, t in ch55.items():
    ENTRIES[f"23_55_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Isaiah landmark verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
