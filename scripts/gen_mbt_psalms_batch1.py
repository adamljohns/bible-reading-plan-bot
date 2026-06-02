"""MBT Psalms expansion batch 1 — Psalms 8, 16, 19, 22, 27, 32, 34. ~112 verses."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Psalm 8 — What is man?
ps_8 = {
    1: "For the choir director. On the Gittith. A Psalm of David. O LORD, our Lord, how majestic is Your name in all the earth — who have displayed Your splendor above the heavens!",
    2: "From the mouth of infants and nursing babes You have established strength, because of Your adversaries — to make the enemy and the revengeful cease.",
    3: "When I consider Your heavens, the work of Your fingers — the moon and the stars, which You have ordained;",
    4: "what is man, that You take thought of him? And the son of man, that You care for him?",
    5: "Yet You have made him a little lower than the angels — and You crown him with glory and majesty.",
    6: "You make him to rule over the works of Your hands. You have put all things under his feet —",
    7: "all sheep and oxen, and also the beasts of the field,",
    8: "the birds of the heavens, and the fish of the sea — whatever passes through the paths of the seas.",
    9: "O LORD, our Lord, how majestic is Your name in all the earth!",
}

# Psalm 16 — The LORD is my portion
ps_16 = {
    1: "A Mikhtam of David. Preserve me, O God — for I take refuge in You.",
    2: "I said to the LORD, \"You are my Lord. I have no good besides You.\"",
    3: "As for the saints who are in the earth, they are the majestic ones in whom is all my delight.",
    4: "The sorrows of those who have bartered for another god will be multiplied. I shall not pour out their drink offerings of blood — nor shall I take their names upon my lips.",
    5: "The LORD is the portion of my inheritance and my cup. You support my lot.",
    6: "The lines have fallen to me in pleasant places — indeed, my heritage is beautiful to me.",
    7: "I will bless the LORD who has counseled me. Indeed, my mind instructs me in the night.",
    8: "I have set the LORD continually before me. Because He is at my right hand, I will not be shaken.",
    9: "Therefore my heart is glad, and my glory rejoices — my flesh also will dwell securely.",
    10: "For You will not abandon my soul to Sheol — neither will You allow Your Holy One to undergo decay.",
    11: "You will make known to me the path of life. In Your presence is fullness of joy. In Your right hand there are pleasures forever.",
}

# Psalm 19 — The heavens declare + the Law is perfect
ps_19 = {
    1: "For the choir director. A Psalm of David. The heavens are telling of the glory of God — and their expanse is declaring the work of His hands.",
    2: "Day to day pours forth speech — and night to night reveals knowledge.",
    3: "There is no speech, nor are there words. Their voice is not heard.",
    4: "Their line has gone out through all the earth, and their utterances to the end of the world. In them He has placed a tent for the sun,",
    5: "which is as a bridegroom coming out of his chamber — it rejoices as a strong man to run his course.",
    6: "Its rising is from one end of the heavens, and its circuit to the other end of them — and there is nothing hidden from its heat.",
    7: "The law of the LORD is perfect, restoring the soul. The testimony of the LORD is sure, making wise the simple.",
    8: "The precepts of the LORD are right, rejoicing the heart. The commandment of the LORD is pure, enlightening the eyes.",
    9: "The fear of the LORD is clean, enduring forever. The judgments of the LORD are true — they are righteous altogether.",
    10: "They are more desirable than gold — yes, than much fine gold; sweeter also than honey and the drippings of the honeycomb.",
    11: "Moreover, by them Your servant is warned. In keeping them there is great reward.",
    12: "Who can discern his errors? Acquit me of hidden faults.",
    13: "Also keep back Your servant from presumptuous sins — let them not rule over me. Then I will be blameless, and I shall be acquitted of great transgression.",
    14: "Let the words of my mouth and the meditation of my heart be acceptable in Your sight, O LORD, my rock and my Redeemer.",
}

# Psalm 22 — My God, why have You forsaken me?
ps_22 = {
    1: "For the choir director. Upon Aijeleth Hashshahar. A Psalm of David. My God, my God, why have You forsaken me? Far from my deliverance are the words of my groaning.",
    2: "O my God, I cry by day, but You do not answer — and by night, but I have no rest.",
    3: "Yet You are holy, O You who are enthroned upon the praises of Israel.",
    4: "In You our fathers trusted. They trusted, and You delivered them.",
    5: "To You they cried out, and were delivered — in You they trusted, and were not disappointed.",
    6: "But I am a worm, and not a man — a reproach of men, and despised by the people.",
    7: "All who see me sneer at me — they separate with the lip, they wag the head, saying,",
    8: "\"Commit yourself to the LORD — let Him deliver him. Let Him rescue him, because He delights in him.\"",
    9: "Yet You are He who brought me forth from the womb — You made me trust when upon my mother's breasts.",
    10: "Upon You I was cast from birth. You have been my God from my mother's womb.",
    11: "Be not far from me — for trouble is near, for there is none to help.",
    12: "Many bulls have surrounded me. Strong bulls of Bashan have encircled me.",
    13: "They open wide their mouth at me — as a ravening and a roaring lion.",
    14: "I am poured out like water, and all my bones are out of joint. My heart is like wax — it is melted within me.",
    15: "My strength is dried up like a potsherd, and my tongue cleaves to my jaws — and You lay me in the dust of death.",
    16: "For dogs have surrounded me. A band of evildoers has encompassed me. They pierced my hands and my feet.",
    17: "I can count all my bones. They look — they stare at me.",
    18: "They divide my garments among them — and for my clothing they cast lots.",
    19: "But You, O LORD, be not far off! O You my help, hasten to my assistance.",
    20: "Deliver my soul from the sword — my only life from the power of the dog.",
    21: "Save me from the lion's mouth — and from the horns of the wild oxen You answer me.",
    22: "I will tell of Your name to my brethren. In the midst of the assembly I will praise You.",
    23: "You who fear the LORD, praise Him. All you descendants of Jacob, glorify Him — and stand in awe of Him, all you descendants of Israel.",
    24: "For He has not despised nor abhorred the affliction of the afflicted. Neither has He hidden His face from him — but when he cried to Him for help, He heard.",
    25: "From You comes my praise in the great assembly — I shall pay my vows before those who fear Him.",
    26: "The afflicted shall eat and be satisfied. Those who seek Him will praise the LORD. Let your heart live forever!",
    27: "All the ends of the earth will remember and turn to the LORD — and all the families of the nations will worship before You.",
    28: "For the kingdom is the LORD's — and He rules over the nations.",
    29: "All the prosperous of the earth will eat and worship — all those who go down to the dust will bow before Him, even he who cannot keep his soul alive.",
    30: "A posterity will serve Him. It will be told of the Lord to the coming generation.",
    31: "They will come and will declare His righteousness to a people who will be born, that He has performed it.",
}

# Psalm 27 — The LORD is my light
ps_27 = {
    1: "A Psalm of David. The LORD is my light and my salvation — whom shall I fear? The LORD is the defense of my life — whom shall I dread?",
    2: "When evildoers came upon me to devour my flesh, my adversaries and my enemies, they stumbled and fell.",
    3: "Though a host encamp against me, my heart will not fear. Though war arise against me, in spite of this I shall be confident.",
    4: "One thing I have asked from the LORD, that I shall seek: that I may dwell in the house of the LORD all the days of my life — to behold the beauty of the LORD, and to meditate in His temple.",
    5: "For in the day of trouble He will conceal me in His tabernacle. In the secret place of His tent He will hide me. He will lift me up on a rock.",
    6: "And now my head will be lifted up above my enemies around me. And I will offer in His tent sacrifices with shouts of joy — I will sing, yes, I will sing praises to the LORD.",
    7: "Hear, O LORD, when I cry with my voice — and be gracious to me, and answer me.",
    8: "When You said, \"Seek My face,\" my heart said to You, \"Your face, O LORD, I shall seek.\"",
    9: "Do not hide Your face from me — do not turn Your servant away in anger. You have been my help. Do not abandon me, nor forsake me, O God of my salvation.",
    10: "For my father and my mother have forsaken me — but the LORD will take me up.",
    11: "Teach me Your way, O LORD — and lead me in a level path, because of my foes.",
    12: "Do not deliver me over to the desire of my adversaries — for false witnesses have risen against me, and such as breathe out violence.",
    13: "I would have despaired unless I had believed that I would see the goodness of the LORD in the land of the living.",
    14: "Wait for the LORD. Be strong, and let your heart take courage. Yes, wait for the LORD.",
}

# Psalm 32 — Blessed is he whose transgression is forgiven
ps_32 = {
    1: "A Psalm of David. A Maskil. How blessed is he whose transgression is forgiven, whose sin is covered.",
    2: "How blessed is the man to whom the LORD does not impute iniquity — and in whose spirit there is no deceit.",
    3: "When I kept silent about my sin, my body wasted away through my groaning all day long.",
    4: "For day and night Your hand was heavy upon me. My vitality was drained away as with the fever-heat of summer.",
    5: "I acknowledged my sin to You — and my iniquity I did not hide. I said, \"I will confess my transgressions to the LORD\" — and You forgave the guilt of my sin.",
    6: "Therefore, let everyone who is godly pray to You in a time when You may be found — surely in a flood of great waters they shall not reach him.",
    7: "You are my hiding place. You preserve me from trouble. You surround me with songs of deliverance.",
    8: "I will instruct you and teach you in the way which you should go. I will counsel you with My eye upon you.",
    9: "Do not be as the horse or as the mule, which have no understanding — whose trappings include bit and bridle to hold them in check, otherwise they will not come near to you.",
    10: "Many are the sorrows of the wicked — but he who trusts in the LORD, lovingkindness shall surround him.",
    11: "Be glad in the LORD and rejoice, you righteous ones — and shout for joy, all you who are upright in heart.",
}

# Psalm 34 — Taste and see that the LORD is good
ps_34 = {
    1: "A Psalm of David, when he feigned madness before Abimelech, who drove him away and he departed. I will bless the LORD at all times — His praise shall continually be in my mouth.",
    2: "My soul shall make its boast in the LORD. The humble shall hear it and rejoice.",
    3: "O magnify the LORD with me — and let us exalt His name together.",
    4: "I sought the LORD, and He answered me — and delivered me from all my fears.",
    5: "They looked to Him and were radiant — and their faces shall never be ashamed.",
    6: "This poor man cried, and the LORD heard him — and saved him out of all his troubles.",
    7: "The angel of the LORD encamps around those who fear Him — and rescues them.",
    8: "O taste and see that the LORD is good — how blessed is the man who takes refuge in Him!",
    9: "O fear the LORD, you His saints — for to those who fear Him, there is no want.",
    10: "The young lions do lack and suffer hunger — but they who seek the LORD shall not be in want of any good thing.",
    11: "Come, you children, listen to me — I will teach you the fear of the LORD.",
    12: "Who is the man who desires life, and loves length of days that he may see good?",
    13: "Keep your tongue from evil — and your lips from speaking deceit.",
    14: "Depart from evil, and do good. Seek peace, and pursue it.",
    15: "The eyes of the LORD are toward the righteous — and His ears are open to their cry.",
    16: "The face of the LORD is against evildoers — to cut off the memory of them from the earth.",
    17: "The righteous cry, and the LORD hears — and delivers them out of all their troubles.",
    18: "The LORD is near to the brokenhearted — and saves those who are crushed in spirit.",
    19: "Many are the afflictions of the righteous — but the LORD delivers him out of them all.",
    20: "He keeps all his bones — not one of them is broken.",
    21: "Evil shall slay the wicked — and those who hate the righteous will be condemned.",
    22: "The LORD redeems the soul of His servants — and none of those who take refuge in Him will be condemned.",
}

ENTRIES = {}
for v, t in ps_8.items():  ENTRIES[f"19_8_{v}"] = t
for v, t in ps_16.items(): ENTRIES[f"19_16_{v}"] = t
for v, t in ps_19.items(): ENTRIES[f"19_19_{v}"] = t
for v, t in ps_22.items(): ENTRIES[f"19_22_{v}"] = t
for v, t in ps_27.items(): ENTRIES[f"19_27_{v}"] = t
for v, t in ps_32.items(): ENTRIES[f"19_32_{v}"] = t
for v, t in ps_34.items(): ENTRIES[f"19_34_{v}"] = t

def main():
    print(f"Psalms batch 1 verses: {len(ENTRIES)}")
    with open(MOOP_PATH) as f:
        moop = json.load(f)
    moop.update(ENTRIES)
    with open(MOOP_PATH, "w") as f:
        json.dump(moop, f, ensure_ascii=False)
    print("moop-translation.json updated.")

if __name__ == "__main__":
    main()
