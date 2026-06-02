"""MBT generator: Leviticus landmark chapters.

Book ID 3. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Leviticus 16 (34 verses) — the Day of Atonement; the scapegoat
- Leviticus 19 (37 verses) — the holiness code; "love your neighbor"
- Leviticus 25 (55 verses) — Sabbath year and Jubilee

Total: 126 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Leviticus 16 — Day of Atonement
ch16 = {
    1: "Now the LORD spoke to Moses after the death of the two sons of Aaron, when they offered profane fire before the LORD, and died;",
    2: "and the LORD said to Moses: \"Tell Aaron your brother not to come at just any time into the Holy Place inside the veil, before the mercy seat which is on the ark, lest he die; for I will appear in the cloud above the mercy seat.",
    3: "Thus Aaron shall come into the Holy Place: with the blood of a young bull as a sin offering, and of a ram as a burnt offering.",
    4: "He shall put the holy linen tunic and the linen trousers on his body; he shall be girded with a linen sash, and with the linen turban he shall be attired. These are holy garments. Therefore he shall wash his body in water, and put them on.",
    5: "And he shall take from the congregation of the children of Israel two kids of the goats as a sin offering, and one ram as a burnt offering.",
    6: "Aaron shall offer the bull as a sin offering, which is for himself, and make atonement for himself and for his house.",
    7: "He shall take the two goats and present them before the LORD at the door of the tabernacle of meeting.",
    8: "Then Aaron shall cast lots for the two goats: one lot for the LORD and the other lot for the scapegoat.",
    9: "And Aaron shall bring the goat on which the LORD's lot fell, and offer it as a sin offering.",
    10: "But the goat on which the lot fell to be the scapegoat shall be presented alive before the LORD, to make atonement upon it, and to let it go as the scapegoat into the wilderness.",
    11: "\"And Aaron shall bring the bull of the sin offering, which is for himself, and make atonement for himself and for his house, and shall kill the bull as the sin offering which is for himself.",
    12: "Then he shall take a censer full of burning coals of fire from the altar before the LORD, with his hands full of sweet incense beaten fine, and bring it inside the veil.",
    13: "And he shall put the incense on the fire before the LORD, that the cloud of incense may cover the mercy seat that is on the Testimony, lest he die.",
    14: "He shall take some of the blood of the bull and sprinkle it with his finger on the mercy seat on the east side; and before the mercy seat he shall sprinkle some of the blood with his finger seven times.",
    15: "\"Then he shall kill the goat of the sin offering, which is for the people, bring its blood inside the veil, do with that blood as he did with the blood of the bull, and sprinkle it on the mercy seat and before the mercy seat.",
    16: "So he shall make atonement for the Holy Place, because of the uncleanness of the children of Israel, and because of their transgressions, for all their sins; and so he shall do for the tabernacle of meeting which remains among them in the midst of their uncleanness.",
    17: "There shall be no man in the tabernacle of meeting when he goes in to make atonement in the Holy Place, until he comes out, that he may make atonement for himself, for his household, and for all the assembly of Israel.",
    18: "And he shall go out to the altar that is before the LORD, and make atonement for it, and shall take some of the blood of the bull and some of the blood of the goat, and put it on the horns of the altar all around.",
    19: "Then he shall sprinkle some of the blood on it with his finger seven times, cleanse it, and consecrate it from the uncleanness of the children of Israel.",
    20: "\"And when he has made an end of atoning for the Holy Place, the tabernacle of meeting, and the altar, he shall bring the live goat.",
    21: "Aaron shall lay both his hands on the head of the live goat, confess over it all the iniquities of the children of Israel, and all their transgressions, concerning all their sins, putting them on the head of the goat, and shall send it away into the wilderness by the hand of a suitable man.",
    22: "The goat shall bear on itself all their iniquities to an uninhabited land; and he shall release the goat in the wilderness.",
    23: "\"Then Aaron shall come into the tabernacle of meeting, shall take off the linen garments which he put on when he went into the Holy Place, and shall leave them there.",
    24: "And he shall wash his body with water in a holy place, put on his garments, come out and offer his burnt offering and the burnt offering of the people, and make atonement for himself and for the people.",
    25: "The fat of the sin offering he shall burn on the altar.",
    26: "And he who released the goat as the scapegoat shall wash his clothes and bathe his body in water, and afterward he may come into the camp.",
    27: "The bull for the sin offering and the goat for the sin offering, whose blood was brought in to make atonement in the Holy Place, shall be carried outside the camp. And they shall burn in the fire their skins, their flesh, and their offal.",
    28: "Then he who burns them shall wash his clothes and bathe his body in water, and afterward he may come into the camp.",
    29: "\"This shall be a statute forever for you: in the seventh month, on the tenth day of the month, you shall afflict your souls, and do no work at all, whether a native of your own country or a stranger who dwells among you.",
    30: "For on that day the priest shall make atonement for you, to cleanse you, that you may be clean from all your sins before the LORD.",
    31: "It is a sabbath of solemn rest for you, and you shall afflict your souls. It is a statute forever.",
    32: "And the priest, who is anointed and consecrated to minister as priest in his father's place, shall make atonement, and put on the linen clothes, the holy garments;",
    33: "then he shall make atonement for the Holy Sanctuary, and he shall make atonement for the tabernacle of meeting and for the altar, and he shall make atonement for the priests and for all the people of the assembly.",
    34: "This shall be an everlasting statute for you, to make atonement for the children of Israel, for all their sins, once a year.\" And he did as the LORD commanded Moses.",
}

# Leviticus 19 — the holiness code
ch19 = {
    1: "And the LORD spoke to Moses, saying,",
    2: "\"Speak to all the congregation of the children of Israel, and say to them: 'You shall be holy, for I the LORD your God am holy.",
    3: "Every one of you shall revere his mother and his father, and keep My Sabbaths: I am the LORD your God.",
    4: "Do not turn to idols, nor make for yourselves molded gods: I am the LORD your God.",
    5: "And if you offer a sacrifice of a peace offering to the LORD, you shall offer it of your own free will.",
    6: "It shall be eaten the same day you offer it, and on the next day; and if any remains until the third day, it shall be burned in the fire.",
    7: "And if it is eaten at all on the third day, it is an abomination. It shall not be accepted.",
    8: "Therefore everyone who eats it shall bear his iniquity, because he has profaned the hallowed offering of the LORD; and that person shall be cut off from his people.",
    9: "\"When you reap the harvest of your land, you shall not wholly reap the corners of your field, nor shall you gather the gleanings of your harvest.",
    10: "And you shall not glean your vineyard, nor shall you gather every grape of your vineyard; you shall leave them for the poor and the stranger: I am the LORD your God.",
    11: "\"You shall not steal, nor deal falsely, nor lie to one another.",
    12: "And you shall not swear by My name falsely, nor shall you profane the name of your God: I am the LORD.",
    13: "\"You shall not cheat your neighbor, nor rob him. The wages of him who is hired shall not remain with you all night until morning.",
    14: "You shall not curse the deaf, nor put a stumbling block before the blind, but shall fear your God: I am the LORD.",
    15: "\"You shall do no injustice in judgment. You shall not be partial to the poor, nor honor the person of the mighty. In righteousness you shall judge your neighbor.",
    16: "You shall not go about as a talebearer among your people; nor shall you take a stand against the life of your neighbor: I am the LORD.",
    17: "\"You shall not hate your brother in your heart. You shall surely rebuke your neighbor, and not bear sin because of him.",
    18: "You shall not take vengeance, nor bear any grudge against the children of your people, but you shall love your neighbor as yourself: I am the LORD.",
    19: "\"You shall keep My statutes. You shall not let your livestock breed with another kind. You shall not sow your field with mixed seed. Nor shall a garment of mixed linen and wool come upon you.",
    20: "\"Whoever lies carnally with a woman who is betrothed to a man as a concubine, and who has not at all been redeemed nor given her freedom, for this there shall be scourging; but they shall not be put to death, because she was not free.",
    21: "And he shall bring his trespass offering to the LORD, to the door of the tabernacle of meeting, a ram as a trespass offering.",
    22: "The priest shall make atonement for him with the ram of the trespass offering before the LORD for his sin which he has committed. And the sin which he has committed shall be forgiven him.",
    23: "\"When you come into the land, and have planted all kinds of trees for food, then you shall count their fruit as uncircumcised. Three years it shall be as uncircumcised to you. It shall not be eaten.",
    24: "But in the fourth year all its fruit shall be holy, a praise to the LORD.",
    25: "And in the fifth year you may eat its fruit, that it may yield to you its increase: I am the LORD your God.",
    26: "\"You shall not eat anything with the blood, nor shall you practice divination or soothsaying.",
    27: "You shall not shave around the sides of your head, nor shall you disfigure the edges of your beard.",
    28: "You shall not make any cuttings in your flesh for the dead, nor tattoo any marks on you: I am the LORD.",
    29: "\"Do not prostitute your daughter, to cause her to be a harlot, lest the land fall into harlotry, and the land become full of wickedness.",
    30: "You shall keep My Sabbaths and reverence My sanctuary: I am the LORD.",
    31: "Give no regard to mediums and familiar spirits; do not seek after them, to be defiled by them: I am the LORD your God.",
    32: "\"You shall rise before the gray headed and honor the presence of an old man, and fear your God: I am the LORD.",
    33: "\"And if a stranger dwells with you in your land, you shall not mistreat him.",
    34: "The stranger who dwells among you shall be to you as one born among you, and you shall love him as yourself; for you were strangers in the land of Egypt: I am the LORD your God.",
    35: "\"You shall do no injustice in judgment, in measurement of length, weight, or volume.",
    36: "You shall have honest scales, honest weights, an honest ephah, and an honest hin: I am the LORD your God, who brought you out of the land of Egypt.",
    37: "Therefore you shall observe all My statutes and all My judgments, and perform them: I am the LORD.'\"",
}

# Leviticus 25 — Sabbath year and Jubilee
ch25 = {
    1: "And the LORD spoke to Moses on Mount Sinai, saying,",
    2: "\"Speak to the children of Israel, and say to them: 'When you come into the land which I give you, then the land shall keep a sabbath to the LORD.",
    3: "Six years you shall sow your field, and six years you shall prune your vineyard, and gather its fruit;",
    4: "but in the seventh year there shall be a sabbath of solemn rest for the land, a sabbath to the LORD. You shall neither sow your field nor prune your vineyard.",
    5: "What grows of its own accord of your harvest you shall not reap, nor gather the grapes of your untended vine, for it is a year of rest for the land.",
    6: "And the sabbath produce of the land shall be food for you: for you, your male and female servants, your hired man, and the stranger who dwells with you,",
    7: "for your livestock and the beasts that are in your land — all its produce shall be for food.",
    8: "\"And you shall count seven sabbaths of years for yourself, seven times seven years; and the time of the seven sabbaths of years shall be to you forty-nine years.",
    9: "Then you shall cause the trumpet of the Jubilee to sound on the tenth day of the seventh month; on the Day of Atonement you shall make the trumpet to sound throughout all your land.",
    10: "And you shall consecrate the fiftieth year, and proclaim liberty throughout all the land to all its inhabitants. It shall be a Jubilee for you; and each of you shall return to his possession, and each of you shall return to his family.",
    11: "That fiftieth year shall be a Jubilee to you; in it you shall neither sow nor reap what grows of its own accord, nor gather the grapes of your untended vine.",
    12: "For it is the Jubilee; it shall be holy to you; you shall eat its produce from the field.",
    13: "In this Year of Jubilee, each of you shall return to his possession.",
    14: "And if you sell anything to your neighbor or buy from your neighbor's hand, you shall not oppress one another.",
    15: "According to the number of years after the Jubilee you shall buy from your neighbor, and according to the number of years of crops he shall sell to you.",
    16: "According to the multitude of years you shall increase its price, and according to the fewer number of years you shall diminish its price; for he sells to you according to the number of the years of the crops.",
    17: "Therefore you shall not oppress one another, but you shall fear your God; for I am the LORD your God.",
    18: "\"So you shall observe My statutes and keep My judgments, and perform them; and you will dwell in the land in safety.",
    19: "Then the land will yield its fruit, and you will eat your fill, and dwell there in safety.",
    20: "And if you say, 'What shall we eat in the seventh year, since we shall not sow nor gather in our produce?'",
    21: "Then I will command My blessing on you in the sixth year, and it will bring forth produce enough for three years.",
    22: "And you shall sow in the eighth year, and eat old produce until the ninth year; until its produce comes in, you shall eat of the old harvest.",
    23: "'The land shall not be sold permanently, for the land is Mine; for you are strangers and sojourners with Me.",
    24: "And in all the land of your possession you shall grant redemption of the land.",
    25: "'If one of your brethren becomes poor, and has sold some of his possession, and if his redeeming relative comes to redeem it, then he may redeem what his brother sold.",
    26: "Or if the man has no one to redeem it, but he himself becomes able to redeem it,",
    27: "then let him count the years since its sale, and restore the balance to the man to whom he sold it, that he may return to his possession.",
    28: "But if he is not able to have it restored to himself, then what was sold shall remain in the hand of him who bought it until the Year of Jubilee; and in the Jubilee it shall be released, and he shall return to his possession.",
    29: "'If a man sells a house in a walled city, then he may redeem it within a whole year after it is sold; within a full year he may redeem it.",
    30: "But if it is not redeemed within the space of a full year, then the house in the walled city shall belong permanently to him who bought it, throughout his generations. It shall not be released in the Jubilee.",
    31: "However the houses of villages which have no wall around them shall be counted as the fields of the country. They may be redeemed, and they shall be released in the Jubilee.",
    32: "Nevertheless the cities of the Levites, and the houses in the cities of their possession, the Levites may redeem at any time.",
    33: "And if a man purchases a house from the Levites, then the house that was sold in the city of his possession shall be released in the Jubilee; for the houses in the cities of the Levites are their possession among the children of Israel.",
    34: "But the field of the common-land of their cities may not be sold, for it is their perpetual possession.",
    35: "'If one of your brethren becomes poor, and falls into poverty among you, then you shall help him, like a stranger or a sojourner, that he may live with you.",
    36: "Take no usury or interest from him; but fear your God, that your brother may live with you.",
    37: "You shall not lend him your money for usury, nor lend him your food at a profit.",
    38: "I am the LORD your God, who brought you out of the land of Egypt, to give you the land of Canaan and to be your God.",
    39: "'And if one of your brethren who dwells by you becomes poor, and sells himself to you, you shall not compel him to serve as a slave.",
    40: "As a hired servant and a sojourner he shall be with you, and shall serve you until the Year of Jubilee.",
    41: "And then he shall depart from you — he and his children with him — and shall return to his own family. He shall return to the possession of his fathers.",
    42: "For they are My servants, whom I brought out of the land of Egypt; they shall not be sold as slaves.",
    43: "You shall not rule over him with rigor, but you shall fear your God.",
    44: "And as for your male and female slaves whom you may have — from the nations that are around you, from them you may buy male and female slaves.",
    45: "Moreover you may buy the children of the strangers who dwell among you, and their families who are with you, which they beget in your land; and they shall become your property.",
    46: "And you may take them as an inheritance for your children after you, to inherit them as a possession; they shall be your permanent slaves. But regarding your brethren, the children of Israel, you shall not rule over one another with rigor.",
    47: "'Now if a sojourner or stranger close to you becomes rich, and one of your brethren who dwells by him becomes poor, and sells himself to the stranger or sojourner close to you, or to a member of the stranger's family,",
    48: "after he is sold he may be redeemed again. One of his brothers may redeem him;",
    49: "or his uncle or his uncle's son may redeem him; or anyone who is near of kin to him in his family may redeem him; or if he is able he may redeem himself.",
    50: "Thus he shall reckon with him who bought him: The price of his release shall be according to the number of years, from the year that he was sold to him until the Year of Jubilee; it shall be according to the time of a hired servant for him.",
    51: "If there are still many years remaining, according to them he shall repay the price of his redemption from the money with which he was bought.",
    52: "And if there remain but a few years until the Year of Jubilee, then he shall reckon with him, and according to his years he shall repay him the price of his redemption.",
    53: "He shall be with him as a yearly hired servant, and he shall not rule with rigor over him in your sight.",
    54: "And if he is not redeemed in these years, then he shall be released in the Year of Jubilee — he and his children with him.",
    55: "For the children of Israel are servants to Me; they are My servants whom I brought out of the land of Egypt: I am the LORD your God.",
}

ENTRIES = {}
for v, t in ch16.items():
    ENTRIES[f"3_16_{v}"] = t
for v, t in ch19.items():
    ENTRIES[f"3_19_{v}"] = t
for v, t in ch25.items():
    ENTRIES[f"3_25_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Leviticus landmark verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
