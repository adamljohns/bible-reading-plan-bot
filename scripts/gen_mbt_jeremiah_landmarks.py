"""MBT generator: Jeremiah landmark chapters.

Book ID 24. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Jeremiah 17 (27 verses) — trusting in man vs the LORD; the deceitful heart
- Jeremiah 29 (32 verses) — letter to the exiles; "thoughts of peace"
- Jeremiah 33 (26 verses) — "Call to Me, and I will answer you"

Total: 85 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Jeremiah 17 — the heart and the two trees
ch17 = {
    1: "\"The sin of Judah is written with a pen of iron; with the point of a diamond it is engraved on the tablet of their heart, and on the horns of your altars,",
    2: "while their children remember their altars and their wooden images by the green trees on the high hills.",
    3: "O My mountain in the field, I will give as plunder your wealth, all your treasures, and your high places of sin within all your borders.",
    4: "And you, even yourself, shall let go of your heritage which I gave you; and I will cause you to serve your enemies in the land which you do not know; for you have kindled a fire in My anger which shall burn forever.\"",
    5: "Thus says the LORD: \"Cursed is the man who trusts in man and makes flesh his strength, whose heart departs from the LORD.",
    6: "For he shall be like a shrub in the desert, and shall not see when good comes, but shall inhabit the parched places in the wilderness, in a salt land which is not inhabited.",
    7: "\"Blessed is the man who trusts in the LORD, and whose hope is the LORD.",
    8: "For he shall be like a tree planted by the waters, which spreads out its roots by the river, and will not fear when heat comes; but its leaf will be green, and will not be anxious in the year of drought, nor will cease from yielding fruit.",
    9: "\"The heart is deceitful above all things, and desperately wicked; who can know it?",
    10: "I, the LORD, search the heart, I test the mind, even to give every man according to his ways, according to the fruit of his doings.",
    11: "As a partridge that broods but does not hatch, so is he who gets riches, but not by right; it will leave him in the midst of his days, and at his end he will be a fool.\"",
    12: "A glorious high throne from the beginning is the place of our sanctuary.",
    13: "O LORD, the hope of Israel, all who forsake You shall be ashamed. \"Those who depart from Me shall be written in the earth, because they have forsaken the LORD, the fountain of living waters.\"",
    14: "Heal me, O LORD, and I shall be healed; save me, and I shall be saved, for You are my praise.",
    15: "Indeed they say to me, \"Where is the word of the LORD? Let it come now!\"",
    16: "As for me, I have not hurried away from being a shepherd who follows You, nor have I desired the woeful day; You know what came out of my lips; it was right there before You.",
    17: "Do not be a terror to me; You are my hope in the day of doom.",
    18: "Let them be ashamed who persecute me, but do not let me be put to shame; let them be dismayed, but do not let me be dismayed. Bring on them the day of doom, and destroy them with double destruction!",
    19: "Thus the LORD said to me: \"Go and stand in the gate of the children of the people, by which the kings of Judah come in and by which they go out, and in all the gates of Jerusalem;",
    20: "and say to them, 'Hear the word of the LORD, you kings of Judah, and all Judah, and all the inhabitants of Jerusalem, who enter by these gates.",
    21: "Thus says the LORD: \"Take heed to yourselves, and bear no burden on the Sabbath day, nor bring it in by the gates of Jerusalem;",
    22: "nor carry a burden out of your houses on the Sabbath day, nor do any work, but hallow the Sabbath day, as I commanded your fathers.",
    23: "But they did not obey nor incline their ear, but made their neck stiff, that they might not hear nor receive instruction.",
    24: "\"And it shall be, if you heed Me carefully,\" says the LORD, \"to bring no burden through the gates of this city on the Sabbath day, but hallow the Sabbath day, to do no work in it,",
    25: "then shall enter the gates of this city kings and princes sitting on the throne of David, riding in chariots and on horses, they and their princes, accompanied by the men of Judah and the inhabitants of Jerusalem; and this city shall remain forever.",
    26: "And they shall come from the cities of Judah and from the places around Jerusalem, from the land of Benjamin and from the lowland, from the mountains and from the South, bringing burnt offerings and sacrifices, grain offerings and incense, bringing sacrifices of praise to the house of the LORD.",
    27: "\"But if you will not heed Me to hallow the Sabbath day, such as not carrying a burden when entering the gates of Jerusalem on the Sabbath day, then I will kindle a fire in its gates, and it shall devour the palaces of Jerusalem, and it shall not be quenched.\"'\"",
}

# Jeremiah 29 — letter to the exiles
ch29 = {
    1: "Now these are the words of the letter that Jeremiah the prophet sent from Jerusalem to the remainder of the elders who were carried away captive — to the priests, the prophets, and all the people whom Nebuchadnezzar had carried away captive from Jerusalem to Babylon.",
    2: "(This happened after Jeconiah the king, the queen mother, the eunuchs, the princes of Judah and Jerusalem, the craftsmen, and the smiths had departed from Jerusalem.)",
    3: "The letter was sent by the hand of Elasah the son of Shaphan, and Gemariah the son of Hilkiah, whom Zedekiah king of Judah sent to Babylon, to Nebuchadnezzar king of Babylon, saying,",
    4: "Thus says the LORD of hosts, the God of Israel, to all who were carried away captive, whom I have caused to be carried away from Jerusalem to Babylon:",
    5: "\"Build houses and dwell in them; plant gardens and eat their fruit.",
    6: "Take wives and beget sons and daughters; and take wives for your sons and give your daughters to husbands, so that they may bear sons and daughters — that you may be increased there, and not diminished.",
    7: "And seek the peace of the city where I have caused you to be carried away captive, and pray to the LORD for it; for in its peace you will have peace.\"",
    8: "For thus says the LORD of hosts, the God of Israel: \"Do not let your prophets and your diviners who are in your midst deceive you, nor listen to your dreams which you cause to be dreamed.",
    9: "For they prophesy falsely to you in My name; I have not sent them,\" says the LORD.",
    10: "For thus says the LORD: \"After seventy years are completed at Babylon, I will visit you and perform My good word toward you, and cause you to return to this place.",
    11: "For I know the thoughts that I think toward you, says the LORD, thoughts of peace and not of evil, to give you a future and a hope.",
    12: "Then you will call upon Me and go and pray to Me, and I will listen to you.",
    13: "And you will seek Me and find Me, when you search for Me with all your heart.",
    14: "I will be found by you, says the LORD, and I will bring you back from your captivity; I will gather you from all the nations and from all the places where I have driven you, says the LORD, and I will bring you to the place from which I cause you to be carried away captive.\"",
    15: "Because you have said, \"The LORD has raised up prophets for us in Babylon\" —",
    16: "therefore thus says the LORD concerning the king who sits on the throne of David, concerning all the people who dwell in this city, and concerning your brethren who have not gone out with you into captivity —",
    17: "thus says the LORD of hosts: \"Behold, I will send on them the sword, the famine, and the pestilence, and will make them like rotten figs that cannot be eaten, they are so bad.",
    18: "And I will pursue them with the sword, with the famine, and with the pestilence; and I will deliver them to trouble among all the kingdoms of the earth — to be a curse, an astonishment, a hissing, and a reproach among all the nations where I have driven them,",
    19: "because they have not heeded My words,\" says the LORD, \"which I sent to them by My servants the prophets, rising up early and sending them; neither would you heed,\" says the LORD.",
    20: "Therefore hear the word of the LORD, all you of the captivity, whom I have sent from Jerusalem to Babylon.",
    21: "Thus says the LORD of hosts, the God of Israel, concerning Ahab the son of Kolaiah, and Zedekiah the son of Maaseiah, who prophesy a lie to you in My name: \"Behold, I will deliver them into the hand of Nebuchadnezzar king of Babylon, and he shall slay them before your eyes.",
    22: "And because of them a curse shall be taken up by all the captivity of Judah who are in Babylon, saying, 'The LORD make you like Zedekiah and Ahab, whom the king of Babylon roasted in the fire';",
    23: "because they have done disgraceful things in Israel, have committed adultery with their neighbors' wives, and have spoken lying words in My name, which I have not commanded them. Indeed I know, and am a witness,\" says the LORD.",
    24: "You shall also speak to Shemaiah the Nehelamite, saying,",
    25: "Thus speaks the LORD of hosts, the God of Israel, saying: \"You have sent letters in your name to all the people who are at Jerusalem, to Zephaniah the son of Maaseiah the priest, and to all the priests, saying,",
    26: "'The LORD has made you priest instead of Jehoiada the priest, so that there should be officers in the house of the LORD over every man who is demented and considers himself a prophet, that you should put him in prison and in the stocks.",
    27: "Now therefore, why have you not reproved Jeremiah of Anathoth who makes himself a prophet to you?",
    28: "For he has sent to us in Babylon, saying, \"This captivity is long; build houses and dwell in them, and plant gardens and eat their fruit.\"'\"",
    29: "Now Zephaniah the priest read this letter in the hearing of Jeremiah the prophet.",
    30: "Then the word of the LORD came to Jeremiah, saying:",
    31: "Send to all those in captivity, saying, Thus says the LORD concerning Shemaiah the Nehelamite: \"Because Shemaiah has prophesied to you, and I have not sent him, and he has caused you to trust in a lie\" —",
    32: "therefore thus says the LORD: \"Behold, I will punish Shemaiah the Nehelamite and his descendants; he shall not have anyone to dwell among this people, nor shall he see the good that I will do for My people, says the LORD, because he has taught rebellion against the LORD.\"\"",
}

# Jeremiah 33 — "Call to Me, and I will answer you"
ch33 = {
    1: "Moreover the word of the LORD came to Jeremiah a second time, while he was still shut up in the court of the prison, saying,",
    2: "\"Thus says the LORD who made it, the LORD who formed it to establish it (the LORD is His name):",
    3: "'Call to Me, and I will answer you, and show you great and mighty things, which you do not know.'",
    4: "For thus says the LORD, the God of Israel, concerning the houses of this city and the houses of the kings of Judah, which have been pulled down to fortify against the siege mounds and the sword:",
    5: "'They come to fight with the Chaldeans, but only to fill their places with the dead bodies of men whom I will slay in My anger and My fury, all for whose wickedness I have hidden My face from this city.",
    6: "Behold, I will bring it health and healing; I will heal them and reveal to them the abundance of peace and truth.",
    7: "And I will cause the captives of Judah and the captives of Israel to return, and will rebuild those places as at the first.",
    8: "I will cleanse them from all their iniquity by which they have sinned against Me, and I will pardon all their iniquities by which they have sinned and by which they have transgressed against Me.",
    9: "Then it shall be to Me a name of joy, a praise, and an honor before all nations of the earth, who shall hear all the good that I do to them; they shall fear and tremble for all the goodness and all the prosperity that I provide for it.'",
    10: "\"Thus says the LORD: 'Again there shall be heard in this place — of which you say, \"It is desolate, without man and without beast\" — in the cities of Judah, in the streets of Jerusalem that are desolate, without man and without inhabitant and without beast,",
    11: "the voice of joy and the voice of gladness, the voice of the bridegroom and the voice of the bride, the voice of those who will say: \"Praise the LORD of hosts, for the LORD is good, for His mercy endures forever\" — and of those who will bring the sacrifice of praise into the house of the LORD. For I will cause the captives of the land to return as at the first,' says the LORD.",
    12: "\"Thus says the LORD of hosts: 'In this place which is desolate, without man and without beast, and in all its cities, there shall again be a dwelling place of shepherds causing their flocks to lie down.",
    13: "In the cities of the mountains, in the cities of the lowland, in the cities of the South, in the land of Benjamin, in the places around Jerusalem, and in the cities of Judah, the flocks shall again pass under the hands of him who counts them,' says the LORD.",
    14: "'Behold, the days are coming,' says the LORD, 'that I will perform that good thing which I have promised to the house of Israel and to the house of Judah:",
    15: "'In those days and at that time I will cause to grow up to David a Branch of righteousness; He shall execute judgment and righteousness in the earth.",
    16: "In those days Judah will be saved, and Jerusalem will dwell safely. And this is the name by which she will be called: THE LORD OUR RIGHTEOUSNESS.'",
    17: "\"For thus says the LORD: 'David shall never lack a man to sit on the throne of the house of Israel;",
    18: "nor shall the priests, the Levites, lack a man to offer burnt offerings before Me, to kindle grain offerings, and to sacrifice continually.'\"",
    19: "And the word of the LORD came to Jeremiah, saying,",
    20: "\"Thus says the LORD: 'If you can break My covenant with the day and My covenant with the night, so that there will not be day and night in their season,",
    21: "then My covenant may also be broken with David My servant, so that he shall not have a son to reign on his throne, and with the Levites, the priests, My ministers.",
    22: "As the host of heaven cannot be numbered, nor the sand of the sea measured, so will I multiply the descendants of David My servant and the Levites who minister to Me.'\"",
    23: "Moreover the word of the LORD came to Jeremiah, saying,",
    24: "\"Have you not considered what these people have spoken, saying, 'The two families which the LORD has chosen, He has also cast them off'? Thus they have despised My people, as if they should no more be a nation before them.",
    25: "Thus says the LORD: 'If My covenant is not with day and night, and if I have not appointed the ordinances of heaven and earth,",
    26: "then I will cast away the descendants of Jacob and David My servant, so that I will not take any of his descendants to be rulers over the descendants of Abraham, Isaac, and Jacob. For I will cause their captives to return, and will have mercy on them.'\"",
}

ENTRIES = {}
for v, t in ch17.items():
    ENTRIES[f"24_17_{v}"] = t
for v, t in ch29.items():
    ENTRIES[f"24_29_{v}"] = t
for v, t in ch33.items():
    ENTRIES[f"24_33_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Jeremiah landmark verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
