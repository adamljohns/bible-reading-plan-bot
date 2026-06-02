"""MBT generator: Isaiah landmarks batch 2.

Book ID 23. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Isaiah 7:1-17 (17 verses) — the Immanuel sign
- Isaiah 11 (16 verses) — the Branch from Jesse; millennial peace
- Isaiah 35 (10 verses) — the desert shall blossom
- Isaiah 42 (25 verses) — the first Servant Song
- Isaiah 61 (11 verses) — "the Spirit of the Lord GOD is upon Me"

Total: 79 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Isaiah 7:1-17 — the Immanuel sign
ch7 = {
    1: "Now it came to pass in the days of Ahaz the son of Jotham, the son of Uzziah, king of Judah, that Rezin king of Syria and Pekah the son of Remaliah, king of Israel, went up to Jerusalem to make war against it, but could not prevail against it.",
    2: "And it was told to the house of David, saying, \"Syria's forces are deployed in Ephraim.\" So his heart and the heart of his people were moved as the trees of the woods are moved with the wind.",
    3: "Then the LORD said to Isaiah, \"Go out now to meet Ahaz, you and Shear-Jashub your son, at the end of the aqueduct from the upper pool, on the highway to the Fuller's Field,",
    4: "and say to him: 'Take heed, and be quiet; do not fear or be fainthearted for these two stubs of smoking firebrands, for the fierce anger of Rezin and Syria, and the son of Remaliah.",
    5: "Because Syria, Ephraim, and the son of Remaliah have plotted evil against you, saying,",
    6: "\"Let us go up against Judah and trouble it, and let us make a gap in its wall for ourselves, and set a king over them, the son of Tabel\" —",
    7: "thus says the Lord GOD: \"It shall not stand, nor shall it come to pass.",
    8: "For the head of Syria is Damascus, and the head of Damascus is Rezin. Within sixty-five years Ephraim will be broken, so that it will not be a people.",
    9: "The head of Ephraim is Samaria, and the head of Samaria is Remaliah's son. If you will not believe, surely you shall not be established.\"'\"",
    10: "Moreover the LORD spoke again to Ahaz, saying,",
    11: "\"Ask a sign for yourself from the LORD your God; ask it either in the depth or in the height above.\"",
    12: "But Ahaz said, \"I will not ask, nor will I test the LORD!\"",
    13: "Then he said, \"Hear now, O house of David! Is it a small thing for you to weary men, but will you weary my God also?",
    14: "Therefore the Lord Himself will give you a sign: Behold, the virgin shall conceive and bear a Son, and shall call His name Immanuel.",
    15: "Curds and honey He shall eat, that He may know to refuse the evil and choose the good.",
    16: "For before the Child shall know to refuse the evil and choose the good, the land that you dread will be forsaken by both her kings.",
    17: "The LORD will bring the king of Assyria upon you and your people and your father's house — days that have not come since the day that Ephraim departed from Judah.\"",
}

# Isaiah 11 — the Branch from Jesse
ch11 = {
    1: "There shall come forth a Rod from the stem of Jesse, and a Branch shall grow out of his roots.",
    2: "The Spirit of the LORD shall rest upon Him, the Spirit of wisdom and understanding, the Spirit of counsel and might, the Spirit of knowledge and of the fear of the LORD.",
    3: "His delight is in the fear of the LORD, and He shall not judge by the sight of His eyes, nor decide by the hearing of His ears;",
    4: "but with righteousness He shall judge the poor, and decide with equity for the meek of the earth; He shall strike the earth with the rod of His mouth, and with the breath of His lips He shall slay the wicked.",
    5: "Righteousness shall be the belt of His loins, and faithfulness the belt of His waist.",
    6: "\"The wolf also shall dwell with the lamb, the leopard shall lie down with the young goat, the calf and the young lion and the fatling together; and a little child shall lead them.",
    7: "The cow and the bear shall graze; their young ones shall lie down together; and the lion shall eat straw like the ox.",
    8: "The nursing child shall play by the cobra's hole, and the weaned child shall put his hand in the viper's den.",
    9: "They shall not hurt nor destroy in all My holy mountain, for the earth shall be full of the knowledge of the LORD as the waters cover the sea.",
    10: "\"And in that day there shall be a Root of Jesse, who shall stand as a banner to the people; for the Gentiles shall seek Him, and His resting place shall be glorious.\"",
    11: "It shall come to pass in that day that the Lord shall set His hand again the second time to recover the remnant of His people who are left, from Assyria and Egypt, from Pathros and Cush, from Elam and Shinar, from Hamath and the islands of the sea.",
    12: "He will set up a banner for the nations, and will assemble the outcasts of Israel, and gather together the dispersed of Judah from the four corners of the earth.",
    13: "Also the envy of Ephraim shall depart, and the adversaries of Judah shall be cut off; Ephraim shall not envy Judah, and Judah shall not harass Ephraim.",
    14: "But they shall fly down upon the shoulder of the Philistines toward the west; together they shall plunder the people of the East; they shall lay their hand on Edom and Moab; and the people of Ammon shall obey them.",
    15: "The LORD will utterly destroy the tongue of the Sea of Egypt; with His mighty wind He will shake His fist over the River, and strike it in the seven streams, and make men cross over dry-shod.",
    16: "There will be a highway for the remnant of His people who will be left from Assyria, as it was for Israel in the day that he came up from the land of Egypt.",
}

# Isaiah 35 — the desert shall blossom
ch35 = {
    1: "The wilderness and the wasteland shall be glad for them, and the desert shall rejoice and blossom as the rose;",
    2: "it shall blossom abundantly and rejoice, even with joy and singing. The glory of Lebanon shall be given to it, the excellence of Carmel and Sharon. They shall see the glory of the LORD, the excellency of our God.",
    3: "Strengthen the weak hands, and make firm the feeble knees.",
    4: "Say to those who are fearful-hearted, \"Be strong, do not fear! Behold, your God will come with vengeance, with the recompense of God; He will come and save you.\"",
    5: "Then the eyes of the blind shall be opened, and the ears of the deaf shall be unstopped.",
    6: "Then the lame shall leap like a deer, and the tongue of the dumb sing. For waters shall burst forth in the wilderness, and streams in the desert.",
    7: "The parched ground shall become a pool, and the thirsty land springs of water; in the habitation of jackals, where each lay, there shall be grass with reeds and rushes.",
    8: "A highway shall be there, and a road, and it shall be called the Highway of Holiness. The unclean shall not pass over it, but it shall be for others. Whoever walks the road, although a fool, shall not go astray.",
    9: "No lion shall be there, nor shall any ravenous beast go up on it; it shall not be found there. But the redeemed shall walk there,",
    10: "and the ransomed of the LORD shall return, and come to Zion with singing, with everlasting joy on their heads. They shall obtain joy and gladness, and sorrow and sighing shall flee away.",
}

# Isaiah 42 — the first Servant Song
ch42 = {
    1: "\"Behold! My Servant whom I uphold, My Elect One in whom My soul delights! I have put My Spirit upon Him; He will bring forth justice to the Gentiles.",
    2: "He will not cry out, nor raise His voice, nor cause His voice to be heard in the street.",
    3: "A bruised reed He will not break, and smoking flax He will not quench; He will bring forth justice for truth.",
    4: "He will not fail nor be discouraged, till He has established justice in the earth; and the coastlands shall wait for His law.\"",
    5: "Thus says God the LORD, who created the heavens and stretched them out, who spread forth the earth and that which comes from it, who gives breath to the people on it, and spirit to those who walk on it:",
    6: "\"I, the LORD, have called You in righteousness, and will hold Your hand; I will keep You and give You as a covenant to the people, as a light to the Gentiles,",
    7: "to open blind eyes, to bring out prisoners from the prison, those who sit in darkness from the prison house.",
    8: "I am the LORD, that is My name; and My glory I will not give to another, nor My praise to carved images.",
    9: "Behold, the former things have come to pass, and new things I declare; before they spring forth I tell you of them.\"",
    10: "Sing to the LORD a new song, and His praise from the ends of the earth, you who go down to the sea, and all that is in it, you coastlands and you inhabitants of them!",
    11: "Let the wilderness and its cities lift up their voice, the villages that Kedar inhabits. Let the inhabitants of Sela sing, let them shout from the top of the mountains.",
    12: "Let them give glory to the LORD, and declare His praise in the coastlands.",
    13: "The LORD shall go forth like a mighty man; He shall stir up His zeal like a man of war. He shall cry out, yes, shout aloud; He shall prevail against His enemies.",
    14: "\"I have held My peace a long time, I have been still and restrained Myself. Now I will cry like a woman in labor, I will pant and gasp at once.",
    15: "I will lay waste the mountains and hills, and dry up all their vegetation; I will make the rivers coastlands, and I will dry up the pools.",
    16: "I will bring the blind by a way they did not know; I will lead them in paths they have not known. I will make darkness light before them, and crooked places straight. These things I will do for them, and not forsake them.",
    17: "They shall be turned back, they shall be greatly ashamed, who trust in carved images, who say to the molded images, 'You are our gods.'",
    18: "\"Hear, you deaf; and look, you blind, that you may see.",
    19: "Who is blind but My servant, or deaf as My messenger whom I send? Who is blind as he who is perfect, and blind as the LORD's servant?",
    20: "Seeing many things, but you do not observe; opening the ears, but he does not hear.\"",
    21: "The LORD is well pleased for His righteousness' sake; He will exalt the law and make it honorable.",
    22: "But this is a people robbed and plundered; all of them are snared in holes, and they are hidden in prison houses; they are for prey, and no one delivers; for plunder, and no one says, \"Restore!\"",
    23: "Who among you will give ear to this? Who will listen and hear for the time to come?",
    24: "Who gave Jacob for plunder, and Israel to the robbers? Was it not the LORD, He against whom we have sinned? For they would not walk in His ways, nor were they obedient to His law.",
    25: "Therefore He has poured on him the fury of His anger and the strength of battle; it has set him on fire all around, yet he did not know; and it burned him, yet he did not take it to heart.",
}

# Isaiah 61 — "the Spirit of the Lord GOD is upon Me"
ch61 = {
    1: "\"The Spirit of the Lord GOD is upon Me, because the LORD has anointed Me to preach good tidings to the poor; He has sent Me to heal the brokenhearted, to proclaim liberty to the captives, and the opening of the prison to those who are bound;",
    2: "to proclaim the acceptable year of the LORD, and the day of vengeance of our God; to comfort all who mourn,",
    3: "to console those who mourn in Zion, to give them beauty for ashes, the oil of joy for mourning, the garment of praise for the spirit of heaviness; that they may be called trees of righteousness, the planting of the LORD, that He may be glorified.\"",
    4: "And they shall rebuild the old ruins, they shall raise up the former desolations, and they shall repair the ruined cities, the desolations of many generations.",
    5: "Strangers shall stand and feed your flocks, and the sons of the foreigner shall be your plowmen and your vinedressers.",
    6: "But you shall be named the priests of the LORD, they shall call you the servants of our God. You shall eat the riches of the Gentiles, and in their glory you shall boast.",
    7: "Instead of your shame you shall have double honor, and instead of confusion they shall rejoice in their portion. Therefore in their land they shall possess double; everlasting joy shall be theirs.",
    8: "\"For I, the LORD, love justice; I hate robbery for burnt offering; I will direct their work in truth, and will make with them an everlasting covenant.",
    9: "Their descendants shall be known among the Gentiles, and their offspring among the people. All who see them shall acknowledge them, that they are the posterity whom the LORD has blessed.\"",
    10: "I will greatly rejoice in the LORD, my soul shall be joyful in my God; for He has clothed me with the garments of salvation, He has covered me with the robe of righteousness, as a bridegroom decks himself with ornaments, and as a bride adorns herself with her jewels.",
    11: "For as the earth brings forth its bud, as the garden causes the things that are sown in it to spring forth, so the Lord GOD will cause righteousness and praise to spring forth before all the nations.",
}

ENTRIES = {}
for v, t in ch7.items():
    ENTRIES[f"23_7_{v}"] = t
for v, t in ch11.items():
    ENTRIES[f"23_11_{v}"] = t
for v, t in ch35.items():
    ENTRIES[f"23_35_{v}"] = t
for v, t in ch42.items():
    ENTRIES[f"23_42_{v}"] = t
for v, t in ch61.items():
    ENTRIES[f"23_61_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Isaiah landmarks batch 2 verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
