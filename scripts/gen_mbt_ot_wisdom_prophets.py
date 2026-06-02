"""MBT OT landmark wisdom + minor prophet passages.

Ecclesiastes 3:1-15 (a time for every purpose), Ecclesiastes 12
(remember your Creator), Ezekiel 37 (valley of dry bones),
Joel 2:28-32 (I will pour out My Spirit), Amos 5:21-24 (let
justice roll down), Micah 6:6-8 (do justly, love mercy),
Habakkuk 3:17-19 (yet I will rejoice), Zechariah 9:9 (Your king
comes), Malachi 3:6-12 (whole tithe), Malachi 4 (sun of
righteousness).
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Ecclesiastes 3:1-15 — A time for every purpose
eccl_3 = {
    1: "There is an appointed time for everything — and a time for every event under heaven.",
    2: "A time to give birth, and a time to die. A time to plant, and a time to uproot what is planted.",
    3: "A time to kill, and a time to heal. A time to tear down, and a time to build up.",
    4: "A time to weep, and a time to laugh. A time to mourn, and a time to dance.",
    5: "A time to throw stones, and a time to gather stones. A time to embrace, and a time to shun embracing.",
    6: "A time to search, and a time to give up as lost. A time to keep, and a time to throw away.",
    7: "A time to tear apart, and a time to sew together. A time to be silent, and a time to speak.",
    8: "A time to love, and a time to hate. A time for war, and a time for peace.",
    9: "What profit is there to the worker from that in which he toils?",
    10: "I have seen the task which God has given the sons of men with which to occupy themselves.",
    11: "He has made everything appropriate in its time. He has also set eternity in their heart — yet so that man will not find out the work which God has done from the beginning even to the end.",
    12: "I know that there is nothing better for them than to rejoice and to do good in one's lifetime.",
    13: "Moreover, that every man who eats and drinks sees good in all his labor — it is the gift of God.",
    14: "I know that everything God does will remain forever — there is nothing to add to it, and there is nothing to take from it. For God has so worked, that men should fear Him.",
    15: "That which is has been already, and that which will be has already been. For God seeks what has passed by.",
}

# Ecclesiastes 12 — Remember your Creator
eccl_12 = {
    1: "Remember also your Creator in the days of your youth, before the evil days come, and the years draw near when you will say, \"I have no delight in them.\"",
    2: "Before the sun, the light, the moon, and the stars are darkened, and clouds return after the rain.",
    3: "In the day that the watchmen of the house tremble, and mighty men stoop, the grinding ones stand idle because they are few, and those who look through windows grow dim.",
    4: "And the doors on the street are shut as the sound of the grinding mill is low, and one will arise at the sound of the bird, and all the daughters of song will sing softly.",
    5: "Furthermore, men are afraid of a high place and of terrors on the road. The almond tree blossoms, the grasshopper drags himself along, and the caperberry is ineffective. For man goes to his eternal home, while mourners go about in the street.",
    6: "Remember Him before the silver cord is broken, and the golden bowl is crushed, the pitcher by the well is shattered, and the wheel at the cistern is crushed.",
    7: "Then the dust will return to the earth as it was, and the spirit will return to God who gave it.",
    8: "\"Vanity of vanities,\" says the Preacher, \"all is vanity!\"",
    9: "In addition to being a wise man, the Preacher also taught the people knowledge. And he pondered, searched out, and arranged many proverbs.",
    10: "The Preacher sought to find delightful words and to write words of truth correctly.",
    11: "The words of wise men are like goads, and masters of these collections are like well-driven nails — they are given by one Shepherd.",
    12: "But beyond this, my son, be warned — the writing of many books is endless, and excessive devotion to books is wearying to the body.",
    13: "The conclusion, when all has been heard, is — fear God and keep His commandments. Because this applies to every person.",
    14: "For God will bring every act to judgment, everything which is hidden, whether it is good or evil.",
}

# Ezekiel 37 — Valley of dry bones
ezek_37 = {
    1: "The hand of the LORD was upon me — and He brought me out by the Spirit of the LORD and set me down in the middle of the valley, and it was full of bones.",
    2: "And He caused me to pass among them round about, and behold, there were very many on the surface of the valley — and lo, they were very dry.",
    3: "And He said to me, \"Son of man, can these bones live?\" And I answered, \"O Lord GOD, You know.\"",
    4: "Again He said to me, \"Prophesy over these bones, and say to them, 'O dry bones — hear the word of the LORD.'",
    5: "Thus says the Lord GOD to these bones: 'Behold, I will cause breath to enter you that you may come to life.",
    6: "And I will put sinews on you, make flesh grow back on you, cover you with skin, and put breath in you that you may come alive. And you will know that I am the LORD.'\"",
    7: "So I prophesied as I was commanded. And as I prophesied, there was a noise — and behold, a rattling, and the bones came together, bone to its bone.",
    8: "And I looked, and behold, sinews were on them, and flesh grew, and skin covered them. But there was no breath in them.",
    9: "Then He said to me, \"Prophesy to the breath, prophesy, son of man, and say to the breath, 'Thus says the Lord GOD: Come from the four winds, O breath, and breathe on these slain, that they come to life.'\"",
    10: "So I prophesied as He commanded me — and the breath came into them, and they came to life and stood on their feet, an exceedingly great army.",
    11: "Then He said to me, \"Son of man, these bones are the whole house of Israel. Behold, they say, 'Our bones are dried up, and our hope has perished. We are completely cut off.'",
    12: "Therefore prophesy, and say to them, 'Thus says the Lord GOD: Behold, I will open your graves and cause you to come up out of your graves, My people — and I will bring you into the land of Israel.",
    13: "Then you will know that I am the LORD, when I have opened your graves and caused you to come up out of your graves, My people.",
    14: "And I will put My Spirit within you, and you will come to life — and I will place you on your own land. Then you will know that I, the LORD, have spoken and done it,' declares the LORD.\"",
    15: "And the word of the LORD came again to me, saying,",
    16: "\"And you, son of man, take for yourself one stick and write on it, 'For Judah and for the sons of Israel, his companions.' Then take another stick and write on it, 'For Joseph, the stick of Ephraim and all the house of Israel, his companions.'",
    17: "Then join them for yourself one to another into one stick, that they may become one in your hand.",
    18: "And when the sons of your people speak to you saying, 'Will you not declare to us what you mean by these?'",
    19: "say to them, 'Thus says the Lord GOD: Behold, I will take the stick of Joseph, which is in the hand of Ephraim, and the tribes of Israel, his companions, and I will put them with it — with the stick of Judah, and make them one stick, and they will be one in My hand.'",
    20: "And the sticks on which you write will be in your hand before their eyes.",
    21: "And say to them, 'Thus says the Lord GOD: Behold, I will take the sons of Israel from among the nations where they have gone, and I will gather them from every side and bring them into their own land.",
    22: "And I will make them one nation in the land, on the mountains of Israel. And one king will be king for all of them — and they will no longer be two nations, and they will no longer be divided into two kingdoms.",
    23: "And they will no longer defile themselves with their idols, or with their detestable things, or with any of their transgressions — but I will deliver them from all their dwelling places in which they have sinned, and will cleanse them. And they will be My people, and I will be their God.",
    24: "And My servant David will be king over them, and they will all have one shepherd — and they will walk in My ordinances, and keep My statutes, and observe them.",
    25: "And they shall live on the land that I gave to Jacob My servant, in which your fathers lived — and they will live on it, they, and their sons, and their sons' sons, forever. And David My servant shall be their prince forever.",
    26: "And I will make a covenant of peace with them — it will be an everlasting covenant with them. And I will place them and multiply them, and will set My sanctuary in their midst forever.",
    27: "My dwelling place also will be with them — and I will be their God, and they will be My people.",
    28: "And the nations will know that I am the LORD who sanctifies Israel, when My sanctuary is in their midst forever.\"",
}

# Joel 2:28-32 — I will pour out My Spirit
joel_2 = {
    28: "\"And it will come about after this that I will pour out My Spirit on all mankind. And your sons and daughters will prophesy. Your old men will dream dreams. Your young men will see visions.",
    29: "And even on the male and female servants, I will pour out My Spirit in those days.",
    30: "And I will display wonders in the sky and on the earth — blood, fire, and columns of smoke.",
    31: "The sun will be turned into darkness, and the moon into blood — before the great and awesome day of the LORD comes.",
    32: "And it will come about that whoever calls on the name of the LORD will be delivered. For on Mount Zion and in Jerusalem there will be those who escape, as the LORD has said, even among the survivors whom the LORD calls.\"",
}

# Amos 5:21-24 — Let justice roll down
amos_5 = {
    21: "\"I hate, I reject your festivals — nor do I delight in your solemn assemblies.",
    22: "Even though you offer up to Me burnt offerings and your grain offerings, I will not accept them. And I will not even look at the peace offerings of your fatlings.",
    23: "Take away from Me the noise of your songs — I will not even listen to the sound of your harps.",
    24: "But let justice roll down like waters — and righteousness like an ever-flowing stream.\"",
}

# Micah 6:6-8 — Do justly, love mercy, walk humbly
mic_6 = {
    6: "With what shall I come to the LORD, and bow myself before the God on high? Shall I come to Him with burnt offerings, with yearling calves?",
    7: "Does the LORD take delight in thousands of rams, in ten thousand rivers of oil? Shall I present my first-born for my rebellious acts, the fruit of my body for the sin of my soul?",
    8: "He has told you, O man, what is good — and what does the LORD require of you, but to do justice, to love kindness, and to walk humbly with your God?",
}

# Habakkuk 3:17-19 — Yet I will rejoice
hab_3 = {
    17: "Though the fig tree should not blossom, and there be no fruit on the vines, though the yield of the olive should fail, and the fields produce no food, though the flock should be cut off from the fold and there be no cattle in the stalls —",
    18: "yet I will exult in the LORD. I will rejoice in the God of my salvation.",
    19: "The Lord GOD is my strength. And He has made my feet like hinds' feet, and makes me walk on my high places. For the choir director, on my stringed instruments.",
}

# Zechariah 9:9 — Your King comes
zech_9 = {
    9: "Rejoice greatly, O daughter of Zion! Shout in triumph, O daughter of Jerusalem! Behold, your king is coming to you — He is just and endowed with salvation, humble, and mounted on a donkey, even on a colt, the foal of a donkey.",
}

# Malachi 3:6-12 — The whole tithe
mal_3 = {
    6: "\"For I, the LORD, do not change. Therefore you, O sons of Jacob, are not consumed.",
    7: "From the days of your fathers you have turned aside from My statutes, and have not kept them. Return to Me, and I will return to you,\" says the LORD of hosts. \"But you say, 'How shall we return?'",
    8: "Will a man rob God? Yet you are robbing Me! But you say, 'How have we robbed You?' In tithes and offerings.",
    9: "You are cursed with a curse — for you are robbing Me, the whole nation of you.",
    10: "Bring the whole tithe into the storehouse, so that there may be food in My house — and test Me now in this,\" says the LORD of hosts, \"if I will not open for you the windows of heaven, and pour out for you a blessing until it overflows.",
    11: "Then I will rebuke the devourer for you, so that it may not destroy the fruits of the ground — nor will your vine in the field cast its grapes,\" says the LORD of hosts.",
    12: "\"And all the nations will call you blessed — for you shall be a delightful land,\" says the LORD of hosts.",
}

# Malachi 4 — Sun of righteousness
mal_4 = {
    1: "\"For behold, the day is coming, burning like a furnace — and all the arrogant and every evildoer will be chaff. And the day that is coming will set them ablaze,\" says the LORD of hosts, \"so that it will leave them neither root nor branch.",
    2: "But for you who fear My name, the sun of righteousness will rise with healing in its wings — and you will go forth and skip about like calves from the stall.",
    3: "And you will tread down the wicked, for they will be ashes under the soles of your feet on the day which I am preparing,\" says the LORD of hosts.",
    4: "Remember the law of Moses My servant, even the statutes and ordinances which I commanded him in Horeb for all Israel.",
    5: "Behold, I am going to send you Elijah the prophet before the coming of the great and terrible day of the LORD.",
    6: "And he will restore the hearts of the fathers to their children, and the hearts of the children to their fathers — lest I come and smite the land with a curse.\"",
}

ENTRIES = {}
for v, t in eccl_3.items():   ENTRIES[f"21_3_{v}"] = t
for v, t in eccl_12.items():  ENTRIES[f"21_12_{v}"] = t
for v, t in ezek_37.items():  ENTRIES[f"26_37_{v}"] = t
for v, t in joel_2.items():   ENTRIES[f"29_2_{v}"] = t
for v, t in amos_5.items():   ENTRIES[f"30_5_{v}"] = t
for v, t in mic_6.items():    ENTRIES[f"33_6_{v}"] = t
for v, t in hab_3.items():    ENTRIES[f"35_3_{v}"] = t
for v, t in zech_9.items():   ENTRIES[f"38_9_{v}"] = t
for v, t in mal_3.items():    ENTRIES[f"39_3_{v}"] = t
for v, t in mal_4.items():    ENTRIES[f"39_4_{v}"] = t

def main():
    print(f"MBT OT wisdom/prophets landmark verses: {len(ENTRIES)}")
    with open(MOOP_PATH) as f:
        moop = json.load(f)
    moop.update(ENTRIES)
    with open(MOOP_PATH, "w") as f:
        json.dump(moop, f, ensure_ascii=False)
    print("moop-translation.json updated.")

if __name__ == "__main__":
    main()
