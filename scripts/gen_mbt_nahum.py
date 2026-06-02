"""MBT generator: Nahum (complete book, 3 chapters, 47 verses).

Book ID 34. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

The sequel to Jonah, a hundred and fifty years later. Nineveh
that had once repented now ripe for judgment.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "The burden against Nineveh. The book of the vision of Nahum the Elkoshite.",
    2: "God is jealous, and the LORD avenges; the LORD avenges and is furious. The LORD will take vengeance on His adversaries, and He reserves wrath for His enemies;",
    3: "the LORD is slow to anger and great in power, and will not at all acquit the wicked. The LORD has His way in the whirlwind and in the storm, and the clouds are the dust of His feet.",
    4: "He rebukes the sea and makes it dry, and dries up all the rivers. Bashan and Carmel wither, and the flower of Lebanon wilts.",
    5: "The mountains quake before Him, the hills melt, and the earth heaves at His presence, yes, the world and all who dwell in it.",
    6: "Who can stand before His indignation? And who can endure the fierceness of His anger? His fury is poured out like fire, and the rocks are thrown down by Him.",
    7: "The LORD is good, a stronghold in the day of trouble; and He knows those who trust in Him.",
    8: "But with an overflowing flood He will make an utter end of its place, and darkness will pursue His enemies.",
    9: "What do you conspire against the LORD? He will make an utter end of it. Affliction will not rise up a second time.",
    10: "For while tangled like thorns, and while drunken like drunkards, they shall be devoured like stubble fully dried.",
    11: "From you comes forth one who plots evil against the LORD, a wicked counselor.",
    12: "Thus says the LORD: \"Though they are safe, and likewise many, yet in this manner they will be cut down when he passes through. Though I have afflicted you, I will afflict you no more;",
    13: "for now I will break off his yoke from you, and burst your bonds apart.\"",
    14: "The LORD has given a command concerning you: \"Your name shall be perpetuated no longer. Out of the house of your gods I will cut off the carved image and the molded image. I will dig your grave, for you are vile.\"",
    15: "Behold, on the mountains the feet of him who brings good tidings, who proclaims peace! O Judah, keep your appointed feasts, perform your vows. For the wicked one shall no more pass through you; he is utterly cut off.",
}

ch2 = {
    1: "He who scatters has come up before your face. Man the fort! Watch the road! Strengthen your flanks! Fortify your power mightily.",
    2: "For the LORD will restore the excellence of Jacob like the excellence of Israel, for the emptiers have emptied them out and ruined their vine branches.",
    3: "The shields of his mighty men are made red, the valiant men are in scarlet. The chariots come with flaming torches in the day of his preparation, and the spears are brandished.",
    4: "The chariots rage in the streets, they jostle one another in the broad roads; they seem like torches, they run like lightning.",
    5: "He remembers his nobles; they stumble in their walk; they make haste to her walls, and the defense is prepared.",
    6: "The gates of the rivers are opened, and the palace is dissolved.",
    7: "It is decreed: she shall be led away captive, she shall be brought up; and her maidservants shall lead her as with the voice of doves, beating their breasts.",
    8: "Though Nineveh of old was like a pool of water, now they flee away. \"Halt! Halt!\" they cry; but no one turns back.",
    9: "Take spoil of silver! Take spoil of gold! There is no end of treasure, or wealth of every desirable prize.",
    10: "She is empty, desolate, and waste! The heart melts, and the knees shake; much pain is in every side, and all their faces are drained of color.",
    11: "Where is the dwelling of the lions, and the feeding place of the young lions, where the lion walked, the lioness and lion's cub, and no one made them afraid?",
    12: "The lion tore in pieces enough for his cubs, killed for his lionesses, filled his caves with prey, and his dens with flesh.",
    13: "\"Behold, I am against you,\" says the LORD of hosts, \"I will burn your chariots in smoke, and the sword shall devour your young lions; I will cut off your prey from the earth, and the voice of your messengers shall be heard no more.\"",
}

ch3 = {
    1: "Woe to the bloody city! It is all full of lies and robbery. Its victim never departs.",
    2: "The noise of a whip and the noise of rattling wheels, of galloping horses, of clattering chariots!",
    3: "Horsemen charge with bright sword and glittering spear. There is a multitude of slain, a great number of bodies, countless corpses — they stumble over the corpses —",
    4: "because of the multitude of harlotries of the seductive harlot, the mistress of sorceries, who sells nations through her harlotries, and families through her sorceries.",
    5: "\"Behold, I am against you,\" says the LORD of hosts; \"I will lift your skirts over your face, I will show the nations your nakedness, and the kingdoms your shame.",
    6: "I will cast abominable filth upon you, make you vile, and make you a spectacle.",
    7: "It shall come to pass that all who look upon you will flee from you, and say, 'Nineveh is laid waste! Who will bemoan her?' Where shall I seek comforters for you?\"",
    8: "Are you better than No Amon that was situated by the River, that had the waters around her, whose rampart was the sea, whose wall was the sea?",
    9: "Ethiopia and Egypt were her strength, and it was boundless; Put and Lubim were your helpers.",
    10: "Yet she was carried away, she went into captivity; her young children also were dashed to pieces at the head of every street; they cast lots for her honorable men, and all her great men were bound in chains.",
    11: "You also will be drunk; you will be hidden; you also will seek refuge from the enemy.",
    12: "All your strongholds are fig trees with ripened figs: if they are shaken, they fall into the mouth of the eater.",
    13: "Surely, your people in your midst are women! The gates of your land are wide open for your enemies; fire shall devour the bars of your gates.",
    14: "Draw your water for the siege! Fortify your strongholds! Go into the clay and tread the mortar! Make strong the brick kiln!",
    15: "There the fire will devour you, the sword will cut you off; it will eat you up like a locust. Make yourself many — like the locust, make yourself many — like the swarming locusts!",
    16: "You have multiplied your merchants more than the stars of heaven. The locust plunders and flies away.",
    17: "Your commanders are like swarming locusts, and your generals like great grasshoppers, which camp in the hedges on a cold day; when the sun rises they flee away, and the place where they are is not known.",
    18: "Your shepherds slumber, O king of Assyria; your nobles rest in the dust. Your people are scattered on the mountains, and no one gathers them.",
    19: "Your injury has no healing, your wound is severe. All who hear news of you will clap their hands over you, for upon whom has not your wickedness passed continually?",
}

CHAPTERS = {1: ch1, 2: ch2, 3: ch3}


def main():
    data = json.loads(MOOP_PATH.read_text())
    new_entries = {}
    for ch, verses in CHAPTERS.items():
        for v, text in verses.items():
            new_entries[f"34_{ch}_{v}"] = text
    data.update(new_entries)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Nahum verses authored: {len(new_entries)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
