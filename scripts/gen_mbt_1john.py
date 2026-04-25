"""
MBT 1 John — all 5 chapters, 105 verses. Book ID 62.

The Johannine epistle most theologically dense after the Gospel itself.
Renders with the Gospel's vocabulary held consistent: 'remain' for meno,
'children of God,' 'born of God,' 'love' for agape, 'Light,' 'life.'
Reverential capitalization throughout for God/Jesus/Spirit pronouns.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_PATH = ROOT / "docs" / "assets" / "mbt-1-3-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Chapter 1 (10 verses) — The Word of Life; Walking in the Light
ch1 = {
    1: "That which was from the beginning, which we have heard, which we have seen with our own eyes, which we have looked at and our hands have touched — concerning the Word of Life —",
    2: "and the Life was made manifest, and we have seen, and bear witness, and proclaim to you the eternal Life, which was with the Father and was made manifest to us —",
    3: "that which we have seen and heard, we proclaim also to you, so that you too may have fellowship with us. And our fellowship is with the Father and with His Son, Jesus Christ.",
    4: "And these things we are writing so that our joy may be made full.",
    5: "And this is the message we have heard from Him and announce to you: God is Light, and in Him there is no darkness at all.",
    6: "If we say that we have fellowship with Him, and yet walk in the darkness, we lie and do not practice the truth.",
    7: "But if we walk in the Light — as He Himself is in the Light — we have fellowship with one another, and the blood of Jesus, His Son, cleanses us from all sin.",
    8: "If we say that we have no sin, we deceive ourselves, and the truth is not in us.",
    9: "If we confess our sins, He is faithful and just to forgive us our sins, and to cleanse us from all unrighteousness.",
    10: "If we say that we have not sinned, we make Him a liar, and His word is not in us.",
}

# Chapter 2 (29 verses) — Christ Our Advocate; the New/Old Commandment;
# Do Not Love the World; Antichrists; Abide in Him
ch2 = {
    1: "My little children, I am writing these things to you so that you may not sin. But if anyone does sin, we have an Advocate with the Father — Jesus Christ, the Righteous One.",
    2: "And He Himself is the propitiation for our sins — and not for ours only, but also for the sins of the whole world.",
    3: "And by this we know that we have come to know Him: if we keep His commandments.",
    4: 'The one who says, "I have come to know Him," and yet does not keep His commandments — that one is a liar, and the truth is not in him.',
    5: "But whoever keeps His word, in him truly the love of God has been made perfect. By this we know that we are in Him:",
    6: "the one who says he remains in Him ought himself to walk in the same way that He walked.",
    7: "Beloved, I am not writing a new commandment to you, but an old commandment that you have had from the beginning. The old commandment is the word that you have heard.",
    8: "Yet again, it is a new commandment that I am writing to you — which is true in Him and in you, because the darkness is passing away, and the true Light is already shining.",
    9: "The one who says he is in the Light, and yet hates his brother, is in the darkness still.",
    10: "The one who loves his brother remains in the Light — and in him there is no cause for stumbling.",
    11: "But the one who hates his brother is in the darkness, and walks in the darkness, and does not know where he is going — because the darkness has blinded his eyes.",
    12: "I am writing to you, little children, because your sins are forgiven for the sake of His name.",
    13: "I am writing to you, fathers, because you have known Him who is from the beginning. I am writing to you, young men, because you have overcome the evil one.",
    14: "I have written to you, little children, because you have known the Father. I have written to you, fathers, because you have known Him who is from the beginning. I have written to you, young men, because you are strong, and the word of God remains in you, and you have overcome the evil one.",
    15: "Do not love the world, nor the things in the world. If anyone loves the world, the love of the Father is not in him.",
    16: "For everything in the world — the desire of the flesh, the desire of the eyes, and the pride of life — is not from the Father, but is from the world.",
    17: "And the world is passing away, along with its desire — but the one who does the will of God remains forever.",
    18: "Little children, it is the last hour. And just as you have heard that Antichrist is coming, even now many antichrists have appeared. By this we know that it is the last hour.",
    19: "They went out from us, but they were not of us. For if they had been of us, they would have remained with us. But this happened so that it would be made plain that none of them are of us.",
    20: "But you have an anointing from the Holy One, and all of you know.",
    21: "I have not written to you because you do not know the truth, but because you do know it — and because no lie comes from the truth.",
    22: "Who is the liar but the one who denies that Jesus is the Christ? This is the Antichrist — the one who denies the Father and the Son.",
    23: "Everyone who denies the Son does not have the Father either. The one who confesses the Son has the Father also.",
    24: "As for you, let what you have heard from the beginning remain in you. If what you have heard from the beginning remains in you, you also will remain in the Son and in the Father.",
    25: "And this is the promise He Himself made to us: eternal life.",
    26: "I have written these things to you concerning those who are trying to deceive you.",
    27: "As for you, the anointing you have received from Him remains in you, and you do not need anyone to teach you. But just as His anointing teaches you about all things — and is true and is no lie — and just as it has taught you, so remain in Him.",
    28: "And now, little children, remain in Him, so that when He appears, we may have boldness, and not shrink away from Him in shame at His coming.",
    29: "If you know that He is righteous, you also know that everyone who practices righteousness has been born of Him.",
}

# Chapter 3 (24 verses) — Children of God; Love One Another; Confidence Before God
ch3 = {
    1: "See what kind of love the Father has given to us — that we should be called children of God! And we are! The reason the world does not know us is that it did not know Him.",
    2: "Beloved, now we are children of God; and what we shall be has not yet appeared. We do know this: when He appears, we shall be like Him — for we shall see Him as He is.",
    3: "And everyone who has this hope set on Him purifies himself, just as He is pure.",
    4: "Everyone who practices sin practices lawlessness — for sin is lawlessness.",
    5: "And you know that He appeared in order to take away sins, and in Him there is no sin.",
    6: "Everyone who remains in Him does not keep on sinning. The one who keeps on sinning has not seen Him, nor has known Him.",
    7: "Little children, let no one deceive you. The one who practices righteousness is righteous, just as He is righteous.",
    8: "The one who practices sin is of the devil, for the devil has been sinning from the beginning. The reason the Son of God appeared was to destroy the works of the devil.",
    9: "No one born of God keeps on sinning, because His seed remains in him; and he is not able to keep on sinning, because he has been born of God.",
    10: "By this it is clear who are the children of God, and who are the children of the devil: anyone who does not practice righteousness is not of God — nor anyone who does not love his brother.",
    11: "For this is the message you have heard from the beginning: that we should love one another.",
    12: "Not as Cain, who was of the evil one and murdered his brother. And why did he murder him? Because his own works were evil, and his brother's were righteous.",
    13: "Do not be amazed, brothers, if the world hates you.",
    14: "We know that we have crossed over from death into life, because we love the brothers. The one who does not love remains in death.",
    15: "Everyone who hates his brother is a murderer — and you know that no murderer has eternal life remaining in him.",
    16: "By this we have come to know love: He laid down His life for us. And we ought to lay down our lives for the brothers.",
    17: "But whoever has the world's goods, and sees his brother in need, and closes his heart against him — how does the love of God remain in him?",
    18: "Little children, let us not love in word, nor with the tongue, but in deed and in truth.",
    19: "By this we will know that we are of the truth, and we will reassure our heart before Him —",
    20: "whenever our heart condemns us. For God is greater than our heart, and He knows everything.",
    21: "Beloved, if our heart does not condemn us, we have confidence before God.",
    22: "And whatever we ask, we receive from Him — because we keep His commandments and do what is pleasing in His sight.",
    23: "And this is His commandment: that we believe in the name of His Son Jesus Christ, and love one another, just as He gave us the commandment.",
    24: "The one who keeps His commandments remains in Him, and He in him. And by this we know that He remains in us — by the Spirit He has given us.",
}

# Chapter 4 (21 verses) — Test the Spirits; God Is Love
ch4 = {
    1: "Beloved, do not believe every spirit, but test the spirits to see whether they are from God — for many false prophets have gone out into the world.",
    2: "By this you know the Spirit of God: every spirit that confesses Jesus Christ has come in the flesh is from God.",
    3: "And every spirit that does not confess Jesus is not from God. This is the spirit of the Antichrist, of which you have heard that it is coming — and now it is already in the world.",
    4: "You are from God, little children, and you have overcome them — because greater is the One who is in you than the one who is in the world.",
    5: "They are from the world. Therefore they speak from the world, and the world listens to them.",
    6: "We are from God. The one who knows God listens to us. The one who is not from God does not listen to us. By this we know the Spirit of truth — and the spirit of error.",
    7: "Beloved, let us love one another — for love is from God. And everyone who loves has been born of God and knows God.",
    8: "The one who does not love does not know God — for God is love.",
    9: "By this the love of God was revealed among us: that God sent His one-and-only Son into the world, so that we might live through Him.",
    10: "In this is love — not that we have loved God, but that He loved us, and sent His Son to be the propitiation for our sins.",
    11: "Beloved, if God so loved us, we also ought to love one another.",
    12: "No one has ever seen God. If we love one another, God remains in us, and His love has been made perfect in us.",
    13: "By this we know that we remain in Him, and He in us: because He has given us of His Spirit.",
    14: "And we have seen, and we testify, that the Father has sent the Son to be the Savior of the world.",
    15: "Whoever confesses that Jesus is the Son of God — God remains in him, and he in God.",
    16: "And we have come to know and to believe the love that God has for us. God is love. And the one who remains in love remains in God, and God in him.",
    17: "By this love has been perfected with us — so that we may have boldness on the day of judgment, because as He is, so also are we in this world.",
    18: "There is no fear in love, but perfect love casts out fear — for fear involves punishment, and the one who fears has not been perfected in love.",
    19: "We love because He first loved us.",
    20: 'If anyone says, "I love God," and yet hates his brother, he is a liar. For the one who does not love his brother, whom he has seen, cannot love God, whom he has not seen.',
    21: "And this is the commandment that we have from Him: the one who loves God must also love his brother.",
}

# Chapter 5 (21 verses) — Faith That Overcomes; the Confidence of Knowing
ch5 = {
    1: "Everyone who believes that Jesus is the Christ has been born of God. And everyone who loves the Father loves the One born of Him.",
    2: "By this we know that we love the children of God: when we love God and keep His commandments.",
    3: "For this is the love of God: that we keep His commandments. And His commandments are not burdensome,",
    4: "because everyone who has been born of God overcomes the world. And this is the victory that has overcome the world: our faith.",
    5: "And who is the one who overcomes the world, except the one who believes that Jesus is the Son of God?",
    6: "This is the One who came by water and blood — Jesus Christ. He came not by water alone, but by the water and the blood. And the Spirit is the One who testifies — because the Spirit is the truth.",
    7: "For there are three who testify:",
    8: "the Spirit, and the water, and the blood — and these three agree as one.",
    9: "If we receive the testimony of men, the testimony of God is greater. For this is the testimony of God: that He has testified concerning His Son.",
    10: "The one who believes in the Son of God has the testimony in himself. The one who does not believe God has made Him a liar — because he has not believed in the testimony that God has borne concerning His Son.",
    11: "And this is the testimony: that God has given us eternal life — and this life is in His Son.",
    12: "The one who has the Son has the life. The one who does not have the Son of God does not have the life.",
    13: "These things I have written to you who believe in the name of the Son of God — so that you may know that you have eternal life.",
    14: "And this is the confidence that we have toward Him: that if we ask anything according to His will, He hears us.",
    15: "And if we know that He hears us — whatever we ask — we know that we have the requests we have asked of Him.",
    16: "If anyone sees his brother committing a sin not leading to death, he shall ask, and God will give him life — for those committing sin not leading to death. There is a sin that leads to death; I do not say that he should pray about that.",
    17: "All unrighteousness is sin — and there is sin not leading to death.",
    18: "We know that everyone who has been born of God does not keep on sinning. But the One who was born of God keeps him, and the evil one does not touch him.",
    19: "We know that we are of God, and that the whole world lies under the sway of the evil one.",
    20: "And we know that the Son of God has come and has given us understanding, so that we may know Him who is true. And we are in Him who is true — in His Son Jesus Christ. He is the true God and eternal life.",
    21: "Little children, keep yourselves from idols.",
}

CHAPTERS = {1: ch1, 2: ch2, 3: ch3, 4: ch4, 5: ch5}

def main():
    new_entries = {f"62_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"1 John total verses authored: {len(new_entries)}")

    # Standalone artifact for all three Johannine epistles
    if MBT_PATH.exists():
        with open(MBT_PATH) as f: existing = json.load(f)
    else:
        existing = {}
    existing.update(new_entries)
    with open(MBT_PATH, "w") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"mbt-1-3-john.json: {len(existing)} total verses")

    # Merge into runtime moop-translation.json
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f:
        json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT 1 John verses")

if __name__ == "__main__":
    main()
