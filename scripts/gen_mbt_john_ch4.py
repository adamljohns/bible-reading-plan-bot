"""
MBT John 4 — The Woman at the Well, Fields White for Harvest,
Samaritan belief, the Official's Son healed. 54 verses.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch4 = {
    1: "Now the Lord became aware that the Pharisees had heard He was making and baptizing more disciples than John —",
    2: "though Jesus Himself was not baptizing; His disciples were —",
    3: "so He left Judea and went back into Galilee.",
    4: "And He had to pass through Samaria.",
    5: "So He came to a Samaritan town called Sychar, near the plot of ground Jacob had given to his son Joseph.",
    6: "Jacob's well was there. Jesus, worn out from the journey, sat down just as He was, beside the well. It was about the sixth hour.",
    7: 'A woman of Samaria came to draw water. Jesus said to her, "Give Me a drink" —',
    8: "for His disciples had gone off into the town to buy food.",
    9: 'So the Samaritan woman said to Him, "How is it that You, a Jew, are asking me for a drink — a Samaritan woman?" (For Jews have no dealings with Samaritans.)',
    10: 'Jesus answered her, "If you knew the gift of God, and who it is who is saying to you, \'Give Me a drink,\' you would have asked Him, and He would have given you living water."',
    11: '"Sir," she said to Him, "You have nothing to draw with, and the well is deep. Where then would You get this living water?',
    12: 'Are You greater than our father Jacob, who gave us the well, and drank from it himself — along with his sons and his livestock?"',
    13: 'Jesus answered her, "Everyone who drinks of this water will be thirsty again.',
    14: 'But whoever drinks of the water that I will give him will never thirst again — ever. The water that I will give him will become in him a spring of water welling up to eternal life."',
    15: 'The woman said to Him, "Sir, give me this water, so I will not be thirsty — and so I will not have to keep coming here to draw."',
    16: 'He told her, "Go, call your husband, and come back here."',
    17: 'The woman answered, "I do not have a husband." Jesus said to her, "You are right in saying, \'I do not have a husband\' —',
    18: 'for you have had five husbands, and the one you have now is not your husband. What you have said is true."',
    19: '"Sir," the woman said to Him, "I see that You are a prophet.',
    20: 'Our fathers worshiped on this mountain, but you Jews say that the place where people must worship is in Jerusalem."',
    21: 'Jesus said to her, "Woman, believe Me — an hour is coming when neither on this mountain nor in Jerusalem will you worship the Father.',
    22: 'You worship what you do not know; we worship what we know — for salvation is from the Jews.',
    23: 'But an hour is coming, and is already here, when the true worshipers will worship the Father in spirit and in truth — for these are the worshipers the Father is seeking.',
    24: 'God is spirit, and those who worship Him must worship in spirit and in truth."',
    25: 'The woman said to Him, "I know that Messiah is coming — the one called \'Christ.\' When He comes, He will explain everything to us."',
    26: 'Jesus said to her, "I am He — the One speaking to you."',
    27: 'Just then, His disciples came back. They were amazed that He was speaking with a woman. But none of them asked, "What do You want?" or "Why are You talking with her?"',
    28: "So the woman left her water jar, went off into the town, and said to the people,",
    29: '"Come — see a Man who told me everything I have ever done! Could this possibly be the Christ?"',
    30: "They went out of the town and were coming toward Him.",
    31: 'Meanwhile, the disciples were urging Him, "Rabbi, eat something."',
    32: 'But He told them, "I have food to eat that you do not know about."',
    33: 'So the disciples said to one another, "Could someone have brought Him something to eat?"',
    34: 'Jesus said to them, "My food is to do the will of the One who sent Me, and to finish His work.',
    35: "Do you not say, 'Four more months, and then the harvest'? Look — I tell you — lift up your eyes and see the fields: they are already white, ready for harvest.",
    36: "The reaper is already being paid; he is gathering fruit for eternal life, so that the sower and the reaper may rejoice together.",
    37: "For in this the saying rings true: 'One sows, and another reaps.'",
    38: 'I sent you to reap what you did not labor for. Others have labored, and you have come into the benefit of their labor."',
    39: 'Many of the Samaritans from that town believed in Him because of the word of the woman who testified, "He told me everything I ever did."',
    40: "So when the Samaritans came to Him, they urged Him to stay with them — and He stayed there two days.",
    41: "And many more believed because of His word.",
    42: 'They said to the woman, "It is no longer because of what you said that we believe — now we have heard for ourselves, and we know that this truly is the Savior of the world."',
    43: "After the two days, He left there for Galilee.",
    44: "For Jesus Himself had testified that a prophet has no honor in his own hometown.",
    45: "So when He came into Galilee, the Galileans welcomed Him — they had seen everything He had done in Jerusalem at the feast, for they too had gone to the feast.",
    46: "He came again to Cana in Galilee, where He had made the water wine. And there was a certain royal official whose son was sick in Capernaum.",
    47: "When this man heard that Jesus had come from Judea into Galilee, he went to Him and begged Him to come down and heal his son — for he was at the point of death.",
    48: 'So Jesus said to him, "Unless you people see signs and wonders, you will never believe."',
    49: 'The royal official said to Him, "Sir, come down before my little boy dies!"',
    50: 'Jesus said to him, "Go — your son lives." The man believed the word Jesus had spoken to him, and went on his way.',
    51: "As he was going down, his servants met him and told him that his boy was alive.",
    52: 'So he asked them what hour he began to get better. They told him, "Yesterday at the seventh hour the fever left him."',
    53: 'Then the father knew that it was at that very hour Jesus had said to him, "Your son lives." And he himself believed — and his whole household.',
    54: "This was now the second sign Jesus performed, when He had come from Judea into Galilee.",
}

CHAPTERS = {4: ch4}

def main():
    new_entries = {}
    for ch, verses in CHAPTERS.items():
        for v, text in verses.items():
            new_entries[f"43_{ch}_{v}"] = text
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
