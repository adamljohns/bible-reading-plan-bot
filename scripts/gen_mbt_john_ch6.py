"""
MBT John 6 — Feeding of the 5,000, Walking on Water, Bread of Life discourse,
Many Disciples Turn Away. 71 verses. The Bread of Life discourse is one of
the most theologically dense passages in John; rendered with care for the
'eat/drink' language and the 'true food' / 'true drink' distinctions.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch6 = {
    1: "After this, Jesus went off to the other side of the Sea of Galilee — also called the Sea of Tiberias.",
    2: "A great crowd followed Him, because they had seen the signs He was performing on those who were sick.",
    3: "Jesus went up on the mountainside and sat down there with His disciples.",
    4: "The Passover — the feast of the Jews — was near.",
    5: 'So Jesus lifted up His eyes, and seeing that a huge crowd was coming toward Him, He said to Philip, "Where are we to buy bread so that these people may eat?"',
    6: "He said this to test him, for He Himself knew what He was about to do.",
    7: 'Philip answered Him, "Two hundred denarii\'s worth of bread would not be enough for each of them to get a little!"',
    8: "One of His disciples — Andrew, Simon Peter's brother — said to Him,",
    9: '"There is a boy here who has five barley loaves and two small fish. But what is that among so many?"',
    10: 'Jesus said, "Have the people sit down." Now there was plenty of grass in that place, so the men sat down — about five thousand of them.',
    11: "Then Jesus took the loaves, gave thanks, and distributed them to those sitting down — as much as they wanted — and likewise with the fish.",
    12: 'When they had eaten their fill, He said to His disciples, "Gather up the leftover pieces, so that nothing is wasted."',
    13: "So they gathered them up and filled twelve baskets with the pieces of the five barley loaves, left over by those who had eaten.",
    14: 'When the people saw the sign Jesus had performed, they began saying, "Truly — this is the Prophet who is to come into the world!"',
    15: "Then Jesus, knowing that they were about to come and take Him by force to make Him king, withdrew again to the mountain — alone.",
    16: "When evening came, His disciples went down to the sea.",
    17: "They got into a boat and started across the sea toward Capernaum. By now it was dark, and Jesus had not yet come to them.",
    18: "A strong wind was blowing, and the sea grew rough.",
    19: "When they had rowed about three or four miles, they saw Jesus walking on the sea, drawing near to the boat — and they were afraid.",
    20: 'But He said to them, "It is I — do not be afraid."',
    21: "Then they were willing to take Him into the boat, and at once the boat reached the land for which they had been heading.",
    22: "The next day, the crowd that had stayed on the other side of the sea realized that only one small boat had been there, and that Jesus had not gotten into the boat with His disciples — but His disciples had gone away alone.",
    23: "Other small boats from Tiberias came near the place where they had eaten the bread, after the Lord had given thanks.",
    24: "So when the crowd saw that Jesus was not there — and neither were His disciples — they got into the boats and came to Capernaum, looking for Jesus.",
    25: 'When they found Him on the other side of the sea, they said to Him, "Rabbi, when did You get here?"',
    26: 'Jesus answered them, "Truly, truly, I tell you — you are looking for Me not because you saw signs, but because you ate of the loaves and had your fill.',
    27: 'Do not work for the food that perishes, but for the food that endures into eternal life — the food which the Son of Man will give you. For on Him God the Father has set His seal."',
    28: 'So they said to Him, "What must we do to carry out the works of God?"',
    29: 'Jesus answered them, "This is the work of God — that you believe in the One He has sent."',
    30: 'So they said to Him, "Then what sign are You going to do, so we may see it and believe You? What work will You perform?',
    31: 'Our fathers ate the manna in the wilderness — as it is written, \'He gave them bread from heaven to eat.\'"',
    32: 'Jesus said to them, "Truly, truly, I tell you — it was not Moses who gave you the bread from heaven; My Father is giving you the true bread from heaven.',
    33: 'For the bread of God is the One who comes down from heaven and gives life to the world."',
    34: 'So they said to Him, "Sir, give us this bread always."',
    35: 'Jesus said to them, "I am the bread of life. The one who comes to Me will never hunger, and the one who believes in Me will never thirst.',
    36: "But as I told you, you have seen Me — and still you do not believe.",
    37: "Everyone the Father gives Me will come to Me, and the one who comes to Me I will never cast out.",
    38: "For I have come down from heaven — not to do My own will, but the will of the One who sent Me.",
    39: "And this is the will of the One who sent Me: that I should lose nothing of all He has given Me, but raise it up on the last day.",
    40: 'For this is the will of My Father: that everyone who sees the Son and believes in Him should have eternal life — and I Myself will raise him up on the last day."',
    41: 'So the Jewish leaders grumbled about Him, because He had said, "I am the bread that came down from heaven."',
    42: 'They said, "Is this not Jesus, the son of Joseph, whose father and mother we know? How then can He say, \'I have come down from heaven\'?"',
    43: 'Jesus answered them, "Stop grumbling among yourselves.',
    44: "No one can come to Me unless the Father who sent Me draws him — and I Myself will raise him up on the last day.",
    45: "It is written in the Prophets, 'And they will all be taught by God.' Everyone who has heard the Father and has learned from Him comes to Me.",
    46: "Not that anyone has seen the Father — except the One who is from God. He has seen the Father.",
    47: "Truly, truly, I tell you — the one who believes has eternal life.",
    48: "I am the bread of life.",
    49: "Your fathers ate the manna in the wilderness, and they died.",
    50: "This is the bread that comes down from heaven, so that anyone may eat of it and not die.",
    51: 'I am the living bread that came down from heaven. If anyone eats of this bread, he will live forever. And the bread I will give for the life of the world is My flesh."',
    52: 'The Jewish leaders then argued with one another, saying, "How can this Man give us His flesh to eat?"',
    53: 'So Jesus said to them, "Truly, truly, I tell you — unless you eat the flesh of the Son of Man and drink His blood, you have no life in yourselves.',
    54: "The one who feeds on My flesh and drinks My blood has eternal life, and I will raise him up on the last day.",
    55: "For My flesh is true food, and My blood is true drink.",
    56: "The one who feeds on My flesh and drinks My blood abides in Me, and I in him.",
    57: "Just as the living Father sent Me, and I live because of the Father — so the one who feeds on Me will live because of Me.",
    58: 'This is the bread that came down from heaven — not as the fathers ate and died. The one who feeds on this bread will live forever."',
    59: "He said these things while teaching in the synagogue at Capernaum.",
    60: 'When many of His disciples heard this, they said, "This is a hard teaching. Who can listen to it?"',
    61: 'But Jesus, knowing in Himself that His disciples were grumbling about this, said to them, "Does this offend you?',
    62: "What then — if you should see the Son of Man ascending to where He was before?",
    63: "It is the Spirit who gives life; the flesh profits nothing. The words that I have spoken to you — they are spirit, and they are life.",
    64: 'But there are some of you who do not believe." For Jesus knew from the beginning which ones did not believe, and who was going to betray Him.',
    65: 'And He said, "This is why I told you that no one can come to Me unless it has been granted to him by the Father."',
    66: "From that point on, many of His disciples turned back and no longer walked with Him.",
    67: 'So Jesus said to the twelve, "You do not want to go away also, do you?"',
    68: 'Simon Peter answered Him, "Lord, to whom shall we go? You have the words of eternal life.',
    69: 'We have come to believe — and we know — that You are the Holy One of God."',
    70: 'Jesus answered them, "Did I not choose you, the twelve? And yet one of you is a devil."',
    71: "He was speaking of Judas, the son of Simon Iscariot — for it was he, though one of the twelve, who was going to betray Him.",
}

CHAPTERS = {6: ch6}

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
