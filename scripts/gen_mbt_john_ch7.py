"""
MBT John 7 — Feast of Tabernacles: Jesus Goes to the Feast, Teaches at
the Feast, 'Is This the Christ?', Rivers of Living Water, Unbelief of
the Leaders. 53 verses (7:53 + 8:1-11 = pericope adulterae).
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch7 = {
    1: "After these things, Jesus went about in Galilee. He did not want to go about in Judea, because the Jewish leaders were looking to kill Him.",
    2: "Now the Jewish Feast of Tabernacles was at hand.",
    3: 'So His brothers said to Him, "Leave here and go into Judea, so that Your disciples may see the works You are doing.',
    4: 'For no one does anything in secret who wants to be known in the open. If You are doing these things, show Yourself to the world!"',
    5: "For even His own brothers did not believe in Him.",
    6: 'Jesus said to them, "My time has not yet come — but for you, the time is always right.',
    7: "The world cannot hate you, but it hates Me, because I testify about it that its works are evil.",
    8: 'You yourselves go up to the feast. I am not going up to this feast, because My time has not yet fully come."',
    9: "Having said this, He remained in Galilee.",
    10: "But after His brothers had gone up to the feast, then He Himself also went up — not openly, but as though in secret.",
    11: 'So the Jewish leaders were looking for Him at the feast, and asking, "Where is that Man?"',
    12: 'And there was much muttering about Him among the crowds. Some were saying, "He is a good man." Others were saying, "No — He is leading the people astray."',
    13: "But no one spoke openly about Him, for fear of the Jewish leaders.",
    14: "Now about the middle of the feast, Jesus went up into the temple and began teaching.",
    15: 'The Jewish leaders were astonished and said, "How does this Man know the Scriptures, when He has never studied?"',
    16: 'Jesus answered them, "My teaching is not My own; it comes from the One who sent Me.',
    17: "If anyone wants to do His will, he will know about the teaching — whether it is from God, or I am speaking on My own authority.",
    18: "The one who speaks on his own seeks his own glory; but the One who seeks the glory of the One who sent Him — He is true, and there is no unrighteousness in Him.",
    19: "Did not Moses give you the law? And yet none of you keeps the law. Why are you trying to kill Me?",
    20: 'The crowd answered, "You have a demon! Who is trying to kill You?"',
    21: 'Jesus answered them, "I did one work, and you all marvel.',
    22: "Moses gave you circumcision — not that it is from Moses, but from the fathers — and on the Sabbath you circumcise a man.",
    23: "If a man is circumcised on the Sabbath so that the law of Moses may not be broken, are you angry with Me because I made a whole man well on the Sabbath?",
    24: 'Stop judging by outward appearance — judge with right judgment."',
    25: 'Then some from Jerusalem began saying, "Is not this the Man they are trying to kill?',
    26: 'And look — He is speaking openly, and they say nothing to Him! Have the rulers truly come to know that this is the Christ?',
    27: 'But we know where this Man is from. When the Christ comes, no one will know where He is from."',
    28: 'Then Jesus, teaching in the temple, cried out: "You know Me, and you know where I am from. And yet I have not come on My own — but the One who sent Me is true, and you do not know Him.',
    29: 'I know Him, because I am from Him, and He sent Me."',
    30: "Then they tried to seize Him, but no one laid a hand on Him — because His hour had not yet come.",
    31: 'Yet many in the crowd believed in Him, and they said, "When the Christ comes, will He do more signs than this Man has done?"',
    32: "The Pharisees heard the crowd muttering these things about Him, and the chief priests and Pharisees sent officers to arrest Him.",
    33: 'Then Jesus said, "A little while longer I am with you, and then I am going to the One who sent Me.',
    34: 'You will look for Me and will not find Me; and where I am, you cannot come."',
    35: 'So the Jewish leaders said to one another, "Where is He about to go, that we will not find Him? Is He about to go to the dispersion among the Greeks, and teach the Greeks?',
    36: 'What did He mean when He said, \'You will look for Me and will not find Me,\' and, \'Where I am, you cannot come\'?"',
    37: 'On the last and greatest day of the feast, Jesus stood up and cried out, "If anyone is thirsty, let him come to Me and drink!',
    38: 'Whoever believes in Me — as the Scripture has said — \'Out of his heart will flow rivers of living water.\'"',
    39: "Now He said this about the Spirit, whom those who believed in Him were about to receive. For as yet the Spirit had not been given, because Jesus was not yet glorified.",
    40: 'When they heard these words, some of the crowd began saying, "This truly is the Prophet."',
    41: 'Others said, "This is the Christ." But some were saying, "Surely the Christ is not going to come out of Galilee, is He?',
    42: "Has not the Scripture said that the Christ is to come from the offspring of David, and from Bethlehem, the village where David was?",
    43: "So there was a division in the crowd because of Him.",
    44: "Some of them wanted to seize Him, but no one laid hands on Him.",
    45: 'The officers then came to the chief priests and Pharisees, who said to them, "Why did you not bring Him?"',
    46: 'The officers answered, "Never has any man spoken like this!"',
    47: 'So the Pharisees answered them, "Have you been led astray too?',
    48: "Have any of the rulers believed in Him? Or any of the Pharisees?",
    49: 'But this crowd that does not know the law — they are accursed!"',
    50: "Nicodemus — who had come to Him earlier, and was one of them — said to them,",
    51: '"Does our law judge a man before it first hears him and knows what he is doing?"',
    52: 'They answered him, "Are you also from Galilee? Search and see — no prophet arises from Galilee."',
    53: "And everyone went off to his own house.",
}

CHAPTERS = {7: ch7}

def main():
    new_entries = {f"43_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"Chapter {list(CHAPTERS.keys())[0]}: {len(new_entries)} verses")

    with open(MBT_JOHN_PATH) as f:
        mbt_john = json.load(f)
    mbt_john.update(new_entries)
    with open(MBT_JOHN_PATH, "w") as f:
        json.dump(mbt_john, f, indent=2, ensure_ascii=False)
    print(f"mbt-john.json: {len(mbt_john)} total verses")

    with open(MOOP_PATH) as f:
        moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f:
        json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT John verses")

if __name__ == "__main__":
    main()
