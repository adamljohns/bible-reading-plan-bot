"""
Generate MBT (MOOP's Bible Translation) for John chapters 1-3.

Style anchors:
- NKJV word-for-word fidelity as the skeleton
- Peterson (The Message) natural English flow where it helps
- Occasional interlinear-order preservation + multi-word expansions when a
  Greek concept carries more weight than a single English word can hold
- Retains load-bearing theological terms (Word, Son, Spirit, Messiah)

Writes to docs/assets/mbt-john.json (create/append) and then merges into
docs/assets/moop-translation.json by replacing all "43_*" keys.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Chapter 1 (51 verses) — The Prologue, John's Testimony, First Disciples
ch1 = {
    1: "In the beginning, the Word already was — face-to-face with God, and Himself God.",
    2: "He was there, in the beginning, with God.",
    3: "Through Him everything came to be. Without Him, not one thing that exists came into being.",
    4: "In Him was life, and that life was the light of every person.",
    5: "The light keeps shining into the darkness, and the darkness has never overcome it — nor understood it.",
    6: "A man came, sent from God. His name was John.",
    7: "He came as a witness — to testify about the Light, so that through him, everyone might come to believe.",
    8: "He himself was not the Light; he was sent to bear witness to the Light.",
    9: "The true Light — the Light that gives light to every person — was now coming into the world.",
    10: "He was in the world, and the world came into being through Him, yet the world did not recognize Him.",
    11: "He came to what was His own, and His own people did not receive Him.",
    12: "But to all who received Him — all who believed on His name — He gave the right to become children of God,",
    13: "born not from bloodlines, nor from human desire, nor from a husband's will, but born of God Himself.",
    14: "And the Word became flesh. He pitched His tent among us, and we saw His glory with our own eyes — the glory of the Father's one-and-only Son, full of grace and full of truth.",
    15: 'John testified about Him and called out: "This is the One I was speaking of when I said, \'The One coming after me has outranked me, because He existed before me.\'"',
    16: "From His fullness we have all received — one grace piled on another, grace in exchange for grace.",
    17: "The law was given through Moses; grace and truth came through Jesus Christ.",
    18: "No one has ever seen God. The one-and-only Son, Himself God, who rests at the Father's side — He is the One who has made Him known.",
    19: 'This is the testimony of John, when the Jewish leaders sent priests and Levites from Jerusalem to ask him, "Who are you?"',
    20: 'He confessed it openly; he did not deny, but confessed: "I am not the Christ."',
    21: 'So they asked him, "What then? Are you Elijah?" He said, "I am not." "Are you the Prophet?" He answered, "No."',
    22: 'Then they said, "Who are you — so we can give an answer to those who sent us? What do you say about yourself?"',
    23: 'He said, "I am the voice of one calling out in the wilderness: \'Make the way of the Lord straight,\' just as the prophet Isaiah said."',
    24: "Now those who had been sent were from the Pharisees.",
    25: 'They pressed him: "Why then are you baptizing — if you are not the Christ, nor Elijah, nor the Prophet?"',
    26: 'John answered them, "I baptize with water. But standing among you is One you do not know —',
    27: 'the One coming after me, whose sandal-strap I am not worthy to untie."',
    28: "These things happened in Bethany, across the Jordan, where John was baptizing.",
    29: 'The next day, John saw Jesus coming toward him and said, "Look! — the Lamb of God, who takes away the sin of the world!',
    30: "This is the One I was speaking of when I said, 'A man is coming after me who has outranked me, because He existed before me.'",
    31: 'I myself did not know who He was — but the reason I came baptizing with water was so that He might be revealed to Israel."',
    32: 'Then John testified: "I saw the Spirit descending from heaven like a dove, and He remained on Him.',
    33: "I myself did not know Him, but the One who sent me to baptize with water said to me, 'The One on whom you see the Spirit descend and remain — He is the One who baptizes with the Holy Spirit.'",
    34: 'And I have seen it. I testify: this is the Son of God."',
    35: "The next day, John was standing there again with two of his disciples,",
    36: 'and as he watched Jesus walking by, he said, "Look — the Lamb of God!"',
    37: "The two disciples heard him say it and followed Jesus.",
    38: 'Jesus turned and saw them following, and asked them, "What are you looking for?" They said to Him, "Rabbi" (which translates \'Teacher\'), "where are You staying?"',
    39: 'He told them, "Come, and you will see." So they came and saw where He was staying, and they stayed with Him that day. It was about the tenth hour.',
    40: "Andrew, Simon Peter's brother, was one of the two who had heard John and followed Jesus.",
    41: 'He first found his own brother Simon and told him, "We have found the Messiah" (which translates \'the Christ\').',
    42: 'He brought him to Jesus. Looking at him, Jesus said, "You are Simon, son of Jonah. You shall be called Cephas" (which translates \'Peter\').',
    43: 'The next day, Jesus decided to go to Galilee. He found Philip and told him, "Follow Me."',
    44: "Now Philip was from Bethsaida, the town of Andrew and Peter.",
    45: 'Philip found Nathanael and told him, "We have found the One Moses wrote about in the Law — and the Prophets, too — Jesus of Nazareth, son of Joseph."',
    46: 'Nathanael said to him, "From Nazareth? Can anything good come out of there?" Philip said, "Come and see."',
    47: 'Jesus saw Nathanael coming toward Him and said about him, "Look — a true Israelite, a man in whom there is no deceit!"',
    48: 'Nathanael said to Him, "How do You know me?" Jesus answered, "Before Philip called you, when you were still under the fig tree, I saw you."',
    49: 'Nathanael answered, "Rabbi, You are the Son of God! You are the King of Israel!"',
    50: 'Jesus answered him, "You believe because I said I saw you under the fig tree? You will see greater things than these."',
    51: 'And He said to him, "Truly, truly, I tell you — you will all see heaven opened, and the angels of God ascending and descending on the Son of Man."',
}

# Chapter 2 (25 verses) — Cana wedding, Temple cleansing
ch2 = {
    1: "On the third day, there was a wedding at Cana in Galilee, and the mother of Jesus was there.",
    2: "Jesus and His disciples had also been invited to the wedding.",
    3: 'When the wine ran out, the mother of Jesus said to Him, "They have no wine."',
    4: 'Jesus said to her, "Woman, why does that involve Me? My hour has not yet come."',
    5: 'His mother told the servants, "Whatever He tells you to do, do it."',
    6: "Now six stone water jars were standing there, used for the Jewish purification rites, each holding twenty or thirty gallons.",
    7: 'Jesus told the servants, "Fill the jars with water." And they filled them to the brim.',
    8: 'Then He said, "Now draw some out and take it to the head steward." So they took it.',
    9: "When the head steward tasted the water — now become wine — and he did not know where it came from, though the servants who had drawn the water knew, he called the bridegroom",
    10: 'and said to him, "Everyone serves the good wine first, and then, after the guests have had plenty to drink, the lesser wine. But you have saved the best wine until now!"',
    11: "This — the first of His signs — Jesus performed in Cana of Galilee. He revealed His glory, and His disciples believed in Him.",
    12: "After this, He went down to Capernaum with His mother, His brothers, and His disciples — and they stayed there a few days.",
    13: "The Passover of the Jews was near, so Jesus went up to Jerusalem.",
    14: "In the temple He found those selling oxen, sheep, and doves, and the money-changers sitting at their tables.",
    15: "So He made a whip out of cords and drove them all out of the temple — the sheep and the oxen too. He scattered the coins of the money-changers and overturned their tables.",
    16: 'To those selling doves He said, "Get these things out of here! Do not turn My Father\'s house into a marketplace!"',
    17: 'His disciples remembered that it is written: "Zeal for Your house will consume Me."',
    18: 'The Jewish leaders responded, "What sign can You show us to prove You have the authority to do this?"',
    19: 'Jesus answered them, "Tear down this temple, and in three days I will raise it up."',
    20: 'The Jewish leaders said, "It has taken forty-six years to build this temple, and You will raise it up in three days?"',
    21: "But He was speaking about the temple of His body.",
    22: "So when He was raised from the dead, His disciples remembered that He had said this, and they believed the Scripture, and the word that Jesus had spoken.",
    23: "While He was in Jerusalem during the Passover feast, many believed in His name when they saw the signs He was doing.",
    24: "But Jesus did not entrust Himself to them, because He knew them all,",
    25: "and because He did not need anyone to testify about what was in a person — He Himself knew what was in every person.",
}

# Chapter 3 (36 verses) — Nicodemus, John 3:16, John the Baptist's final witness
ch3 = {
    1: "There was a man of the Pharisees named Nicodemus, a ruler of the Jews.",
    2: 'This man came to Jesus by night and said to Him, "Rabbi, we know You are a teacher who has come from God — for no one can do these signs that You do unless God is with him."',
    3: 'Jesus answered him, "Truly, truly, I tell you — unless a person is born from above, he cannot see the kingdom of God."',
    4: 'Nicodemus said to Him, "How can a man be born when he is old? Can he enter his mother\'s womb a second time and be born?"',
    5: 'Jesus answered, "Truly, truly, I tell you — unless a person is born of water and the Spirit, he cannot enter the kingdom of God.',
    6: "What is born of the flesh is flesh; what is born of the Spirit is spirit.",
    7: "Do not be amazed that I said to you, 'You must be born from above.'",
    8: 'The wind blows wherever it pleases. You hear its sound, but you do not know where it comes from or where it is going. So it is with everyone born of the Spirit."',
    9: 'Nicodemus answered, "How can these things be?"',
    10: 'Jesus answered, "You are the teacher of Israel, and you do not know these things?',
    11: "Truly, truly, I tell you — We speak of what We know and bear witness to what We have seen, and yet you do not receive Our testimony.",
    12: "If I have told you about earthly things and you do not believe, how will you believe if I tell you about heavenly things?",
    13: "No one has ascended into heaven except the One who descended from heaven — the Son of Man.",
    14: "And just as Moses lifted up the serpent in the wilderness, so must the Son of Man be lifted up,",
    15: 'so that whoever believes in Him may have eternal life."',
    16: "For God so loved the world that He gave His one-and-only Son, so that everyone who believes in Him will not perish but have eternal life.",
    17: "For God did not send His Son into the world to condemn the world, but so that the world might be saved through Him.",
    18: "The one who believes in Him is not condemned; but the one who does not believe stands already condemned, because he has not believed in the name of the one-and-only Son of God.",
    19: "And this is the verdict: the Light has come into the world, but people loved the darkness rather than the Light — because their deeds were evil.",
    20: "Everyone who practices evil hates the Light, and does not come into the Light, so that his deeds may not be exposed.",
    21: "But the one who does what is true comes into the Light, so that his deeds may be clearly seen — that they have been carried out in God.",
    22: "After these things, Jesus and His disciples went into the Judean countryside, and He stayed there with them and was baptizing.",
    23: "John also was baptizing at Aenon near Salim, because there was plenty of water there, and people were coming and being baptized —",
    24: "for John had not yet been thrown into prison.",
    25: "A dispute arose between some of John's disciples and a Jew over ritual purification.",
    26: 'They came to John and said to him, "Rabbi, the One who was with you on the other side of the Jordan — the One you testified about — look, He is baptizing, and everyone is going to Him!"',
    27: 'John answered, "A person can receive nothing unless it has been given to him from heaven.',
    28: "You yourselves are my witnesses that I said, 'I am not the Christ — I have been sent ahead of Him.'",
    29: "The one who has the bride is the bridegroom. The friend of the bridegroom, who stands by and listens to him, rejoices with great joy at the bridegroom's voice. So this joy of mine is now made full.",
    30: 'He must increase; I must decrease."',
    31: "The One who comes from above is above all. The one who is from the earth belongs to the earth and speaks from the earth. The One who comes from heaven is above all.",
    32: "He testifies to what He has seen and heard, and yet no one receives His testimony.",
    33: "Whoever has received His testimony has set his seal to this: that God is true.",
    34: "For the One whom God has sent speaks the words of God — for God gives the Spirit without measure.",
    35: "The Father loves the Son and has given all things into His hand.",
    36: "The one who believes in the Son has eternal life, but the one who refuses to believe the Son will not see life — for the wrath of God remains on him.",
}

CHAPTERS = {1: ch1, 2: ch2, 3: ch3}

def load_json(path, default):
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return default

def main():
    # Build flat dict of MBT John entries to write
    new_entries = {}
    for ch, verses in CHAPTERS.items():
        for v, text in verses.items():
            new_entries[f"43_{ch}_{v}"] = text
    print(f"Chapters drafted: {list(CHAPTERS.keys())}")
    print(f"Total new verses: {len(new_entries)}")

    # Merge into mbt-john.json (persistent standalone)
    mbt_john = load_json(MBT_JOHN_PATH, {})
    mbt_john.update(new_entries)
    with open(MBT_JOHN_PATH, "w") as f:
        json.dump(mbt_john, f, indent=2, ensure_ascii=False)
    print(f"Wrote {MBT_JOHN_PATH} ({len(mbt_john)} total John verses)")

    # Merge into moop-translation.json (runtime source consumed by BTE)
    moop = load_json(MOOP_PATH, {})
    before = sum(1 for k in moop if k.startswith("43_"))
    moop.update(new_entries)
    after = sum(1 for k in moop if k.startswith("43_"))
    with open(MOOP_PATH, "w") as f:
        json.dump(moop, f, ensure_ascii=False)
    print(f"Merged into {MOOP_PATH}: {before} John entries -> {after} total")

if __name__ == "__main__":
    main()
