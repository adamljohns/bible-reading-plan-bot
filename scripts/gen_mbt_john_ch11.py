"""
MBT John 11 — Lazarus. 57 verses. The seventh sign and the hinge of the
book. 'I am the resurrection and the life.'
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch11 = {
    1: "Now a certain man was sick — Lazarus of Bethany, the village of Mary and her sister Martha.",
    2: "(Mary was the one who anointed the Lord with perfume and wiped His feet with her hair; it was her brother Lazarus who was sick.)",
    3: 'So the sisters sent to Him, saying, "Lord, look — the one You love is sick."',
    4: 'When Jesus heard it, He said, "This sickness will not end in death. It is for the glory of God — so that the Son of God may be glorified through it."',
    5: "Now Jesus loved Martha and her sister and Lazarus.",
    6: "So when He heard that he was sick, He stayed two more days in the place where He was.",
    7: 'Then after this He said to the disciples, "Let us go into Judea again."',
    8: 'The disciples said to Him, "Rabbi, the Jewish leaders were just now trying to stone You — and You are going back there?"',
    9: 'Jesus answered, "Are there not twelve hours in the day? If anyone walks during the day, he does not stumble, because he sees the light of this world.',
    10: "But if anyone walks at night, he stumbles, because the light is not in him.",
    11: 'Our friend Lazarus has fallen asleep. But I am going so that I may wake him up."',
    12: 'So the disciples said to Him, "Lord, if he has fallen asleep, he will recover."',
    13: "Jesus had been speaking about his death, but they thought He meant sleep — natural rest.",
    14: 'Then Jesus told them plainly, "Lazarus is dead.',
    15: 'And for your sake I am glad I was not there — so that you may believe. But let us go to him."',
    16: 'So Thomas, who was called the Twin, said to the other disciples, "Let us also go, so that we may die with Him."',
    17: "When Jesus arrived, He found that Lazarus had already been in the tomb four days.",
    18: "Now Bethany was near Jerusalem — about two miles off —",
    19: "and many of the Jews had come to Martha and Mary, to console them concerning their brother.",
    20: "When Martha heard that Jesus was coming, she went out to meet Him — but Mary stayed sitting in the house.",
    21: 'Martha said to Jesus, "Lord, if You had been here, my brother would not have died.',
    22: 'And even now, I know that whatever You ask of God, God will give You."',
    23: 'Jesus said to her, "Your brother will rise again."',
    24: 'Martha said to Him, "I know that he will rise again — in the resurrection, on the last day."',
    25: 'Jesus said to her, "I am the resurrection and the life. The one who believes in Me — even if he dies — will live.',
    26: 'And everyone who lives and believes in Me will never die — ever. Do you believe this?"',
    27: 'She said to Him, "Yes, Lord. I have come to believe that You are the Christ, the Son of God, the One who is coming into the world."',
    28: 'Having said this, she went off and called her sister Mary in secret, saying, "The Teacher is here, and is calling for you."',
    29: "When Mary heard it, she got up quickly and came to Him.",
    30: "Jesus had not yet come into the village, but was still in the place where Martha had met Him.",
    31: "When the Jews who had been with Mary in the house, consoling her, saw her get up quickly and go out, they followed her — thinking she was going to the tomb to weep there.",
    32: 'When Mary came to the place where Jesus was, and saw Him, she fell at His feet, saying to Him, "Lord, if You had been here, my brother would not have died."',
    33: "When Jesus saw her weeping, and the Jews who had come with her also weeping, He was deeply moved in spirit — and troubled.",
    34: 'And He said, "Where have you laid him?" They said to Him, "Lord, come and see."',
    35: "Jesus wept.",
    36: 'So the Jews were saying, "See how He loved him!"',
    37: 'But some of them said, "Could not this Man, who opened the eyes of the blind, have kept this man from dying?"',
    38: "Jesus, again deeply moved in Himself, came to the tomb. It was a cave, with a stone lying against it.",
    39: 'Jesus said, "Take away the stone." Martha, the sister of the dead man, said to Him, "Lord, by now there is a stench — it has been four days."',
    40: 'Jesus said to her, "Did I not tell you that if you believed, you would see the glory of God?"',
    41: 'So they took away the stone. And Jesus lifted up His eyes and said, "Father, I thank You that You have heard Me.',
    42: 'I knew that You always hear Me — but I said this for the sake of the crowd standing around, so that they may believe that You sent Me."',
    43: 'When He had said this, He cried out with a loud voice: "Lazarus, come out!"',
    44: 'The man who had died came out — his hands and feet bound with strips of linen, his face wrapped with a cloth. Jesus said to them, "Unbind him, and let him go."',
    45: "Many of the Jews, therefore, who had come with Mary and had seen what He did, believed in Him.",
    46: "But some of them went off to the Pharisees and told them what Jesus had done.",
    47: 'So the chief priests and the Pharisees called a council and said, "What are we doing? For this Man is performing many signs.',
    48: 'If we let Him go on like this, everyone will believe in Him. Then the Romans will come and take away both our place and our nation."',
    49: 'One of them, Caiaphas, who was high priest that year, said to them, "You know nothing at all!',
    50: 'You do not realize that it is better for you that one man should die for the people, than that the whole nation should perish."',
    51: "He did not say this on his own — but being high priest that year, he prophesied that Jesus was about to die for the nation,",
    52: "and not for the nation only — but also to gather into one the children of God who had been scattered abroad.",
    53: "So from that day on, they plotted how to kill Him.",
    54: "Therefore Jesus no longer walked openly among the Jewish leaders, but went away from there to the region near the wilderness, to a town called Ephraim. And He stayed there with His disciples.",
    55: "Now the Passover of the Jews was near, and many went up from the country to Jerusalem before the Passover to purify themselves.",
    56: 'They were looking for Jesus, and as they stood in the temple, they were saying to one another, "What do you think? He will not come to the feast at all, will He?"',
    57: "Now the chief priests and the Pharisees had given orders that if anyone knew where He was, he should report it — so that they might arrest Him.",
}

CHAPTERS = {11: ch11}

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
