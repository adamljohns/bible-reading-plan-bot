"""MBT generator: Song of Solomon (complete book, 8 chapters, 117 verses).

Book ID 22. NKJV-faithful skeleton, modern English flow.
The covenant love poem. Reverential pronouns are NOT applied to
the lovers' speech to each other — these are addressed between
a man and a woman, not to God. Capitalization is reserved for
the rare moments God or the LORD is invoked.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "The song of songs, which is Solomon's.",
    2: "Let him kiss me with the kisses of his mouth — for your love is better than wine.",
    3: "Because of the fragrance of your good ointments, your name is ointment poured forth; therefore the virgins love you.",
    4: "Draw me away! We will run after you. The king has brought me into his chambers. We will be glad and rejoice in you; we will remember your love more than wine. Rightly do they love you.",
    5: "I am dark, but lovely, O daughters of Jerusalem, like the tents of Kedar, like the curtains of Solomon.",
    6: "Do not look upon me because I am dark, because the sun has tanned me. My mother's sons were angry with me; they made me the keeper of the vineyards, but my own vineyard I have not kept.",
    7: "Tell me, O you whom I love, where you feed your flock, where you make it rest at noon. For why should I be as one who veils herself by the flocks of your companions?",
    8: "If you do not know, O fairest among women, follow in the footsteps of the flock, and feed your little goats beside the shepherds' tents.",
    9: "I have compared you, my love, to my filly among Pharaoh's chariots.",
    10: "Your cheeks are lovely with ornaments, your neck with chains of gold.",
    11: "We will make you ornaments of gold with studs of silver.",
    12: "While the king is at his table, my spikenard sends forth its fragrance.",
    13: "A bundle of myrrh is my beloved to me, that lies all night between my breasts.",
    14: "My beloved is to me a cluster of henna blooms in the vineyards of En Gedi.",
    15: "Behold, you are fair, my love! Behold, you are fair! You have dove's eyes.",
    16: "Behold, you are handsome, my beloved! Yes, pleasant! Also our bed is green.",
    17: "The beams of our houses are cedar, and our rafters of fir.",
}

ch2 = {
    1: "I am the rose of Sharon, and the lily of the valleys.",
    2: "Like a lily among thorns, so is my love among the daughters.",
    3: "Like an apple tree among the trees of the woods, so is my beloved among the sons. I sat down in his shade with great delight, and his fruit was sweet to my taste.",
    4: "He brought me to the banqueting house, and his banner over me was love.",
    5: "Sustain me with cakes of raisins, refresh me with apples, for I am lovesick.",
    6: "His left hand is under my head, and his right hand embraces me.",
    7: "I charge you, O daughters of Jerusalem, by the gazelles or by the does of the field, do not stir up nor awaken love until it pleases.",
    8: "The voice of my beloved! Behold, he comes leaping upon the mountains, skipping upon the hills.",
    9: "My beloved is like a gazelle or a young stag. Behold, he stands behind our wall; he is looking through the windows, gazing through the lattice.",
    10: "My beloved spoke, and said to me: \"Rise up, my love, my fair one, and come away.",
    11: "For lo, the winter is past, the rain is over and gone.",
    12: "The flowers appear on the earth; the time of singing has come, and the voice of the turtledove is heard in our land.",
    13: "The fig tree puts forth her green figs, and the vines with the tender grapes give a good smell. Rise up, my love, my fair one, and come away!",
    14: "O my dove, in the clefts of the rock, in the secret places of the cliff, let me see your face, let me hear your voice; for your voice is sweet, and your face is lovely.\"",
    15: "Catch us the foxes, the little foxes that spoil the vines, for our vines have tender grapes.",
    16: "My beloved is mine, and I am his. He feeds his flock among the lilies.",
    17: "Until the day breaks and the shadows flee away, turn, my beloved, and be like a gazelle or a young stag upon the mountains of Bether.",
}

ch3 = {
    1: "By night on my bed I sought the one I love; I sought him, but I did not find him.",
    2: "\"I will rise now,\" I said, \"and go about the city; in the streets and in the squares I will seek the one I love.\" I sought him, but I did not find him.",
    3: "The watchmen who go about the city found me; I said, \"Have you seen the one I love?\"",
    4: "Scarcely had I passed by them, when I found the one I love. I held him and would not let him go, until I had brought him to the house of my mother, and into the chamber of her who conceived me.",
    5: "I charge you, O daughters of Jerusalem, by the gazelles or by the does of the field, do not stir up nor awaken love until it pleases.",
    6: "Who is this coming out of the wilderness like pillars of smoke, perfumed with myrrh and frankincense, with all the merchant's fragrant powders?",
    7: "Behold, it is Solomon's couch, with sixty valiant men around it, of the valiant of Israel.",
    8: "They all hold swords, being expert in war. Every man has his sword on his thigh because of fear in the night.",
    9: "Of the wood of Lebanon Solomon the King made himself a palanquin:",
    10: "He made its pillars of silver, its support of gold, its seat of purple, its interior paved with love by the daughters of Jerusalem.",
    11: "Go forth, O daughters of Zion, and see King Solomon with the crown with which his mother crowned him on the day of his wedding, the day of the gladness of his heart.",
}

ch4 = {
    1: "Behold, you are fair, my love! Behold, you are fair! You have dove's eyes behind your veil. Your hair is like a flock of goats, going down from Mount Gilead.",
    2: "Your teeth are like a flock of shorn sheep which have come up from the washing, every one of which bears twins, and none is barren among them.",
    3: "Your lips are like a strand of scarlet, and your mouth is lovely. Your temples behind your veil are like a piece of pomegranate.",
    4: "Your neck is like the tower of David, built for an armory, on which hang a thousand bucklers, all shields of mighty men.",
    5: "Your two breasts are like two fawns, twins of a gazelle, which feed among the lilies.",
    6: "Until the day breaks and the shadows flee away, I will go my way to the mountain of myrrh and to the hill of frankincense.",
    7: "You are all fair, my love, and there is no spot in you.",
    8: "Come with me from Lebanon, my spouse, with me from Lebanon. Look from the top of Amana, from the top of Senir and Hermon, from the lions' dens, from the mountains of the leopards.",
    9: "You have ravished my heart, my sister, my spouse; you have ravished my heart with one look of your eyes, with one link of your necklace.",
    10: "How fair is your love, my sister, my spouse! How much better than wine is your love, and the scent of your perfumes than all spices!",
    11: "Your lips, O my spouse, drip as the honeycomb; honey and milk are under your tongue; and the fragrance of your garments is like the fragrance of Lebanon.",
    12: "A garden enclosed is my sister, my spouse, a spring shut up, a fountain sealed.",
    13: "Your plants are an orchard of pomegranates with pleasant fruits, fragrant henna with spikenard,",
    14: "spikenard and saffron, calamus and cinnamon, with all trees of frankincense, myrrh and aloes, with all the chief spices —",
    15: "a fountain of gardens, a well of living waters, and streams from Lebanon.",
    16: "Awake, O north wind, and come, O south! Blow upon my garden, that its spices may flow out. Let my beloved come to his garden and eat its pleasant fruits.",
}

ch5 = {
    1: "I have come to my garden, my sister, my spouse; I have gathered my myrrh with my spice; I have eaten my honeycomb with my honey; I have drunk my wine with my milk. Eat, O friends! Drink, yes, drink deeply, O beloved ones!",
    2: "I sleep, but my heart is awake; it is the voice of my beloved! He knocks, saying, \"Open for me, my sister, my love, my dove, my perfect one; for my head is covered with dew, my locks with the drops of the night.\"",
    3: "I have taken off my robe; how can I put it on again? I have washed my feet; how can I defile them?",
    4: "My beloved put his hand by the latch of the door, and my heart yearned for him.",
    5: "I arose to open for my beloved, and my hands dripped with myrrh, my fingers with liquid myrrh, on the handles of the lock.",
    6: "I opened for my beloved, but my beloved had turned away and was gone. My heart leaped up when he spoke. I sought him, but I could not find him; I called him, but he gave me no answer.",
    7: "The watchmen who went about the city found me. They struck me, they wounded me; the keepers of the walls took my veil away from me.",
    8: "I charge you, O daughters of Jerusalem, if you find my beloved, that you tell him I am lovesick!",
    9: "What is your beloved more than another beloved, O fairest among women? What is your beloved more than another beloved, that you so charge us?",
    10: "My beloved is white and ruddy, chief among ten thousand.",
    11: "His head is like the finest gold; his locks are wavy, and black as a raven.",
    12: "His eyes are like doves by the rivers of waters, washed with milk, and fitly set.",
    13: "His cheeks are like a bed of spices, banks of scented herbs. His lips are lilies, dripping liquid myrrh.",
    14: "His hands are rods of gold set with beryl. His body is carved ivory inlaid with sapphires.",
    15: "His legs are pillars of marble set on bases of fine gold. His countenance is like Lebanon, excellent as the cedars.",
    16: "His mouth is most sweet, yes, he is altogether lovely. This is my beloved, and this is my friend, O daughters of Jerusalem!",
}

ch6 = {
    1: "Where has your beloved gone, O fairest among women? Where has your beloved turned aside, that we may seek him with you?",
    2: "My beloved has gone to his garden, to the beds of spices, to feed his flock in the gardens, and to gather lilies.",
    3: "I am my beloved's, and my beloved is mine. He feeds his flock among the lilies.",
    4: "O my love, you are as beautiful as Tirzah, lovely as Jerusalem, awesome as an army with banners!",
    5: "Turn your eyes away from me, for they have overcome me. Your hair is like a flock of goats going down from Gilead.",
    6: "Your teeth are like a flock of sheep which have come up from the washing; every one bears twins, and none is barren among them.",
    7: "Like a piece of pomegranate are your temples behind your veil.",
    8: "There are sixty queens and eighty concubines, and virgins without number.",
    9: "My dove, my perfect one, is the only one, the only one of her mother, the favorite of the one who bore her. The daughters saw her and called her blessed, the queens and the concubines, and they praised her.",
    10: "Who is she who looks forth as the morning, fair as the moon, clear as the sun, awesome as an army with banners?",
    11: "I went down to the garden of nuts to see the verdure of the valley, to see whether the vine had budded and the pomegranates had bloomed.",
    12: "Before I was even aware, my soul had made me as the chariots of my noble people.",
    13: "Return, return, O Shulamite; return, return, that we may look upon you! What would you see in the Shulamite — as it were, the dance of the two camps?",
}

ch7 = {
    1: "How beautiful are your feet in sandals, O prince's daughter! The curves of your thighs are like jewels, the work of the hands of a skillful workman.",
    2: "Your navel is a rounded goblet which lacks no blended beverage. Your waist is a heap of wheat set about with lilies.",
    3: "Your two breasts are like two fawns, twins of a gazelle.",
    4: "Your neck is like an ivory tower, your eyes like the pools in Heshbon by the gate of Bath Rabbim. Your nose is like the tower of Lebanon which looks toward Damascus.",
    5: "Your head crowns you like Mount Carmel, and the hair of your head is like purple; a king is held captive by your tresses.",
    6: "How fair and how pleasant you are, O love, with your delights!",
    7: "This stature of yours is like a palm tree, and your breasts like its clusters.",
    8: "I said, \"I will go up to the palm tree, I will take hold of its branches.\" Let now your breasts be like clusters of the vine, the fragrance of your breath like apples,",
    9: "and the roof of your mouth like the best wine. The wine goes down smoothly for my beloved, moving gently the lips of sleepers.",
    10: "I am my beloved's, and his desire is toward me.",
    11: "Come, my beloved, let us go forth to the field; let us lodge in the villages.",
    12: "Let us get up early to the vineyards; let us see if the vine has budded, whether the grape blossoms are open, and the pomegranates are in bloom. There I will give you my love.",
    13: "The mandrakes give off a fragrance, and at our gates are pleasant fruits, all manner, new and old, which I have laid up for you, my beloved.",
}

ch8 = {
    1: "Oh, that you were like my brother, who nursed at my mother's breasts! If I should find you outside, I would kiss you; I would not be despised.",
    2: "I would lead you and bring you into the house of my mother, she who used to instruct me. I would cause you to drink of spiced wine, of the juice of my pomegranate.",
    3: "His left hand is under my head, and his right hand embraces me.",
    4: "I charge you, O daughters of Jerusalem, do not stir up nor awaken love until it pleases.",
    5: "Who is this coming up from the wilderness, leaning upon her beloved? I awakened you under the apple tree; there your mother brought you forth, there she who bore you brought you forth.",
    6: "Set me as a seal upon your heart, as a seal upon your arm; for love is as strong as death, jealousy as cruel as the grave; its flames are flames of fire, a most vehement flame.",
    7: "Many waters cannot quench love, nor can the floods drown it. If a man would give for love all the wealth of his house, it would be utterly despised.",
    8: "We have a little sister, and she has no breasts. What shall we do for our sister in the day when she is spoken for?",
    9: "If she is a wall, we will build upon her a battlement of silver; and if she is a door, we will enclose her with boards of cedar.",
    10: "I am a wall, and my breasts like towers; then I became in his eyes as one who found peace.",
    11: "Solomon had a vineyard at Baal Hamon; he leased the vineyard to keepers; everyone was to bring for its fruit a thousand silver coins.",
    12: "My own vineyard is before me. You, O Solomon, may have a thousand, and those who tend its fruit two hundred.",
    13: "You who dwell in the gardens, the companions listen for your voice — let me hear it!",
    14: "Make haste, my beloved, and be like a gazelle or a young stag on the mountains of spices.",
}

CHAPTERS = {1: ch1, 2: ch2, 3: ch3, 4: ch4, 5: ch5, 6: ch6, 7: ch7, 8: ch8}


def main():
    data = json.loads(MOOP_PATH.read_text())
    new_entries = {}
    for ch, verses in CHAPTERS.items():
        for v, text in verses.items():
            new_entries[f"22_{ch}_{v}"] = text
    data.update(new_entries)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Song of Solomon verses authored: {len(new_entries)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
