"""
MBT John 12 — Mary anoints Jesus, Triumphal Entry, Greeks seek Jesus,
Son of Man Lifted Up, the Unbelief of the People. 50 verses.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch12 = {
    1: "Six days before the Passover, Jesus came to Bethany, where Lazarus was — the one Jesus had raised from the dead.",
    2: "So they gave a dinner for Him there. Martha was serving; Lazarus was one of those reclining at table with Him.",
    3: "Then Mary took a pound of pure nard — a very costly perfume — and anointed Jesus' feet. She wiped His feet with her hair, and the house was filled with the fragrance of the perfume.",
    4: 'But Judas Iscariot, one of His disciples, who was about to betray Him, said,',
    5: '"Why was this perfume not sold for three hundred denarii, and given to the poor?"',
    6: "He said this not because he cared about the poor, but because he was a thief — and being in charge of the money box, he used to steal what was put into it.",
    7: 'So Jesus said, "Leave her alone. She has kept this for the day of My burial.',
    8: 'For the poor you always have with you — but you do not always have Me."',
    9: "A great crowd of the Jews learned that He was there, and they came — not only for the sake of Jesus, but also to see Lazarus, whom He had raised from the dead.",
    10: "So the chief priests plotted to kill Lazarus as well,",
    11: "because on account of him many of the Jews were going away and believing in Jesus.",
    12: "On the next day, the great crowd that had come to the feast heard that Jesus was coming into Jerusalem.",
    13: 'So they took branches of palm trees and went out to meet Him, shouting: "Hosanna! Blessed is He who comes in the name of the Lord — the King of Israel!"',
    14: "And Jesus, finding a young donkey, sat on it — as it is written:",
    15: '"Do not be afraid, daughter of Zion. Look — your King is coming, seated on a donkey\'s colt."',
    16: "His disciples did not understand these things at first — but when Jesus was glorified, then they remembered that these things had been written about Him, and that they had done these things for Him.",
    17: "So the crowd who had been with Him when He called Lazarus out of the tomb and raised him from the dead kept bearing witness.",
    18: "For this reason the crowd also came out to meet Him — because they had heard that He had performed this sign.",
    19: 'So the Pharisees said to one another, "You see — you are getting nowhere. Look — the whole world has gone after Him!"',
    20: "Now there were some Greeks among those who went up to worship at the feast.",
    21: 'These came to Philip, who was from Bethsaida in Galilee, and asked him, "Sir, we want to see Jesus."',
    22: "Philip went and told Andrew, and then Andrew and Philip went and told Jesus.",
    23: 'Jesus answered them, saying, "The hour has come for the Son of Man to be glorified.',
    24: "Truly, truly, I tell you — unless a grain of wheat falls into the earth and dies, it remains alone. But if it dies, it bears much fruit.",
    25: "The one who loves his life loses it, and the one who hates his life in this world will keep it into eternal life.",
    26: "If anyone serves Me, he must follow Me — and where I am, there My servant also will be. If anyone serves Me, the Father will honor him.",
    27: "Now My soul is troubled. And what shall I say? 'Father, save Me from this hour'? But it was for this very reason that I came to this hour.",
    28: 'Father, glorify Your name." Then a voice came from heaven: "I have glorified it, and I will glorify it again."',
    29: 'The crowd standing by heard it and said, "It has thundered." Others said, "An angel has spoken to Him."',
    30: 'Jesus answered, "This voice came for your sake — not for Mine.',
    31: "Now is the judgment of this world. Now the ruler of this world will be cast out.",
    32: 'And when I am lifted up from the earth, I will draw all people to Myself."',
    33: "He said this to show by what kind of death He was about to die.",
    34: 'The crowd answered Him, "We have heard from the Law that the Christ will remain forever. How can You say, \'The Son of Man must be lifted up\'? Who is this Son of Man?"',
    35: 'Then Jesus said to them, "The Light is among you for a little while longer. Walk while you have the Light, so that the darkness does not overtake you. The one who walks in the darkness does not know where he is going.',
    36: 'While you have the Light, believe in the Light, so that you may become sons of Light." Jesus spoke these things, and departed, and hid Himself from them.',
    37: "Although He had performed so many signs before them, they still would not believe in Him —",
    38: 'so that the word of Isaiah the prophet might be fulfilled, which he spoke: "Lord, who has believed what we have heard? And to whom has the arm of the Lord been revealed?"',
    39: "For this reason they could not believe — because again, Isaiah said:",
    40: '"He has blinded their eyes, and hardened their heart — so that they would not see with their eyes, and understand with their heart, and turn — and I would heal them."',
    41: "Isaiah said these things because he saw His glory, and spoke about Him.",
    42: "Yet even so, many of the rulers believed in Him. But because of the Pharisees, they would not confess it, for fear of being put out of the synagogue —",
    43: "for they loved the glory that comes from men more than the glory that comes from God.",
    44: 'Then Jesus cried out and said, "The one who believes in Me believes not in Me, but in the One who sent Me.',
    45: "And the one who sees Me sees the One who sent Me.",
    46: "I have come as Light into the world — so that everyone who believes in Me will not remain in the darkness.",
    47: "If anyone hears My words and does not keep them, I do not judge him — for I did not come to judge the world, but to save the world.",
    48: "The one who rejects Me and does not receive My words has one who judges him: the word I have spoken — that will judge him on the last day.",
    49: "For I have not spoken on My own. The Father who sent Me — He Himself has given Me a command: what I am to say, and what I am to speak.",
    50: 'And I know that His command is eternal life. So the things I speak — just as the Father has told Me, so I speak."',
}

CHAPTERS = {12: ch12}

def main():
    new_entries = {f"43_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"Chapter {list(CHAPTERS.keys())[0]}: {len(new_entries)} verses")
    with open(MBT_JOHN_PATH) as f: mbt_john = json.load(f)
    mbt_john.update(new_entries)
    with open(MBT_JOHN_PATH, "w") as f: json.dump(mbt_john, f, indent=2, ensure_ascii=False)
    print(f"mbt-john.json: {len(mbt_john)} total verses")
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f: json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT John verses")

if __name__ == "__main__":
    main()
