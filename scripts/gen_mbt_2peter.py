"""MBT 2 Peter — 3 chapters, 61 verses. Book ID 61."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_PATH = ROOT / "docs" / "assets" / "mbt-nt-extra.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "Simon Peter, a bondservant and apostle of Jesus Christ — to those who have obtained a faith of equal standing with ours, by the righteousness of our God and Savior Jesus Christ:",
    2: "Grace and peace be multiplied to you in the knowledge of God and of Jesus our Lord.",
    3: "His divine power has granted to us all things pertaining to life and godliness, through the full knowledge of Him who called us by His own glory and excellence —",
    4: "by which He has granted to us His precious and very great promises, so that through them you may become partakers of the divine nature, having escaped the corruption that is in the world through evil desire.",
    5: "For this very reason, make every effort to add to your faith virtue; and to virtue, knowledge;",
    6: "and to knowledge, self-control; and to self-control, perseverance; and to perseverance, godliness;",
    7: "and to godliness, brotherly affection; and to brotherly affection, love.",
    8: "For if these qualities are yours and are increasing, they keep you from being ineffective or unfruitful in the full knowledge of our Lord Jesus Christ.",
    9: "For the one who lacks these things is so nearsighted that he is blind — having forgotten the cleansing from his former sins.",
    10: "Therefore, brothers, be all the more diligent to make your calling and election sure. For if you do these things, you will never stumble —",
    11: "for in this way, the entrance into the eternal kingdom of our Lord and Savior Jesus Christ will be richly supplied to you.",
    12: "For this reason I will always be ready to remind you of these things — though you know them, and are established in the truth that is with you.",
    13: "I think it right, as long as I am in this body, to stir you up by way of reminder —",
    14: "knowing that the laying aside of my body will be soon, just as our Lord Jesus Christ has made clear to me.",
    15: "And I will make every effort, so that after my departure you will always be able to call these things to remembrance.",
    16: "For we did not follow cleverly devised myths when we made known to you the power and coming of our Lord Jesus Christ — but we were eyewitnesses of His majesty.",
    17: "For when He received honor and glory from God the Father, when such a voice came to Him from the Majestic Glory: \"This is My beloved Son, with whom I am well pleased\" —",
    18: "we ourselves heard this voice come from heaven when we were with Him on the holy mountain.",
    19: "And we have the prophetic word made even more sure — to which you do well to pay attention, as to a lamp shining in a dark place, until the day dawns and the morning star rises in your hearts.",
    20: "Knowing this first: that no prophecy of Scripture comes from one's own interpretation.",
    21: "For no prophecy was ever produced by the will of man — but men spoke from God as they were carried along by the Holy Spirit.",
}
ch2 = {
    1: "But there were also false prophets among the people, just as there will be false teachers among you — who will secretly bring in destructive heresies, even denying the Master who bought them — bringing on themselves swift destruction.",
    2: "And many will follow their licentiousness, and because of them the way of truth will be blasphemed.",
    3: "And in their greed they will exploit you with deceptive words. Their condemnation, from long ago, is not idle — and their destruction is not asleep.",
    4: "For if God did not spare angels when they sinned, but cast them down to hell and committed them to chains of gloomy darkness, kept until the judgment;",
    5: "and if He did not spare the ancient world, but preserved Noah, a herald of righteousness, with seven others, when He brought a flood upon the world of the ungodly;",
    6: "and if He condemned the cities of Sodom and Gomorrah by reducing them to ashes, making them an example of what is going to happen to the ungodly;",
    7: "and if He rescued righteous Lot, who was distressed by the licentious behavior of lawless men —",
    8: "for as that righteous man lived among them day after day, his righteous soul was tormented by what he saw and heard of their lawless deeds —",
    9: "then the Lord knows how to rescue the godly from trial, and how to keep the unrighteous under punishment for the day of judgment;",
    10: "and especially those who walk according to the flesh in defiling lust, and who despise authority. Bold and arrogant, they are not afraid to revile glorious beings —",
    11: "whereas angels, though greater in might and power, do not bring a reviling judgment against them before the Lord.",
    12: "But these, like irrational animals, born of nature to be caught and destroyed — speaking abusively about things they do not understand — will also be destroyed in their corruption,",
    13: "suffering wrong as the wages for doing wrong. They count it pleasure to revel in broad daylight. They are spots and blemishes, reveling in their own deceptions while they feast with you.",
    14: "Their eyes are full of adultery and never cease from sin. They entice unsteady souls. They have hearts trained in greed — accursed children!",
    15: "Forsaking the right way, they have gone astray. They have followed the way of Balaam, son of Beor, who loved the wages of unrighteousness —",
    16: "but he was rebuked for his own transgression: a speechless donkey spoke with a man's voice and restrained the prophet's madness.",
    17: "These are springs without water, and mists driven by a storm. The gloom of darkness has been reserved for them.",
    18: "For when they speak arrogant, empty words, they entice — by lusts of the flesh, by sensuality — those who are barely escaping from the ones who live in error.",
    19: "They promise them freedom, while they themselves are slaves of corruption — for whatever overcomes a man, by that he is enslaved.",
    20: "For if, after escaping the defilements of the world through the full knowledge of our Lord and Savior Jesus Christ, they are again entangled in them and overcome — the last state has become worse for them than the first.",
    21: "It would have been better for them not to have known the way of righteousness than, having known it, to turn back from the holy commandment delivered to them.",
    22: "For them the true proverb has come true: \"A dog returns to its own vomit,\" and, \"A washed sow returns to wallowing in the mire.\"",
}
ch3 = {
    1: "This is now, beloved, the second letter I am writing to you — in both of which I am stirring up your sincere mind by way of reminder,",
    2: "that you should remember the words spoken beforehand by the holy prophets, and the commandment of the Lord and Savior given through your apostles —",
    3: "knowing this first: that scoffers will come in the last days, walking according to their own lusts,",
    4: "and saying, \"Where is the promise of His coming? For ever since the fathers fell asleep, all things continue as they were from the beginning of creation.\"",
    5: "For they deliberately overlook this fact: that long ago by the word of God the heavens existed, and the earth was formed out of water and through water,",
    6: "by which the world that then existed was destroyed by being flooded with water.",
    7: "But by the same word, the present heavens and earth are stored up for fire — being kept until the day of judgment and the destruction of ungodly people.",
    8: "But do not overlook this one fact, beloved: with the Lord, one day is as a thousand years, and a thousand years as one day.",
    9: "The Lord is not slow concerning His promise, as some count slowness — but He is patient toward you, not wishing that any should perish, but that all should reach repentance.",
    10: "But the day of the Lord will come like a thief — in which the heavens will pass away with a roar, and the elements will be dissolved with intense heat, and the earth and the works that are on it will be exposed.",
    11: "Since all these things are to be dissolved in this way, what kind of people ought you to be — in holy conduct and godliness,",
    12: "looking for and hastening the coming of the day of God, on account of which the heavens will be set on fire and dissolved, and the elements will melt with intense heat?",
    13: "But according to His promise, we are looking for new heavens and a new earth — in which righteousness dwells.",
    14: "Therefore, beloved — since you are looking for these things — be diligent to be found by Him in peace, spotless and blameless.",
    15: "And consider the patience of our Lord as salvation — just as our beloved brother Paul also wrote to you, according to the wisdom given to him,",
    16: "speaking of these things in all his letters — in which there are some things hard to understand, which the ignorant and unstable distort, as they do also the rest of the Scriptures, to their own destruction.",
    17: "You therefore, beloved — knowing this beforehand — be on guard, so that you are not carried away by the error of the lawless and lose your own steadfastness.",
    18: "But grow in the grace and full knowledge of our Lord and Savior Jesus Christ. To Him be the glory both now and to the day of eternity. Amen.",
}
CHAPTERS = {1: ch1, 2: ch2, 3: ch3}

def main():
    new_entries = {f"61_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"2 Peter total verses authored: {len(new_entries)}")
    with open(MBT_PATH) as f: existing = json.load(f)
    existing.update(new_entries)
    with open(MBT_PATH, "w") as f: json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"mbt-nt-extra.json: {len(existing)} total verses")
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f: json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT 2 Peter verses")

if __name__ == "__main__":
    main()
