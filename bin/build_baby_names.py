#!/usr/bin/env python3
"""build_baby_names.py — generate docs/dictionary/baby-names.html

A curated, browseable baby-name directory split off from the broader
biblical-names index. Categorizes by male / female / unisex (place-names
that work for both, biblical figures whose names cross gender lines).

Each name shows:
  * Headword (linked to the full dictionary entry)
  * One-line meaning / origin
  * Common nicknames and variants (English, Hebrew, Greek, Spanish, etc.)

The curated mapping below is hand-maintained — biblical baby-naming is
high-touch and benefits from editorial curation more than automated
inference. Each entry is a tuple of (slug, short_meaning, variants_list).
"""
import os
import re
import html as html_mod

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')
OUT = os.path.join(DICT_DIR, 'baby-names.html')

WORD_TITLE_PAT = re.compile(r'<div class="word-title">(.*?)</div>', re.DOTALL)
H1_TITLE_PAT = re.compile(r'<h1[^>]*class="[^"]*word-title[^"]*"[^>]*>(.*?)</h1>', re.DOTALL)
BARE_H1_PAT = re.compile(r'<body[^>]*>.*?<h1[^>]*>(.*?)</h1>', re.DOTALL)
TAG_STRIP = re.compile(r'<[^>]+>')


def get_headword(slug):
    fp = os.path.join(DICT_DIR, f'{slug}.html')
    if not os.path.exists(fp):
        return None
    with open(fp, 'r', encoding='utf-8') as f:
        h = f.read()
    for pat in (WORD_TITLE_PAT, H1_TITLE_PAT, BARE_H1_PAT):
        m = pat.search(h)
        if m:
            t = TAG_STRIP.sub('', m.group(1))
            t = t.replace('&mdash;', '—').replace('&amp;', '&').replace('&#39;', "'")
            t = re.sub(r'\s+', ' ', t).strip()
            t = re.sub(r'\s*\([^)]*\)\s*$', '', t)
            return t
    return None


# Hand-curated mapping: (slug, short_meaning, variants_list)
# Variants include nicknames, language variants (Hebrew/Greek/Spanish/Italian),
# and modern spelling variations. They DO count toward total-displayed-names.

MALE = [
    # Patriarchs
    ('adam',            'man, earth; the first human',
                        ['Adamo', 'Adan', 'Adi']),
    ('abel',            'breath, vapor; the first martyr (Gen 4)',
                        ['Abe']),
    ('seth-son',        'appointed; son of Adam after Abel',
                        ['Sett']),
    ('enoch',           'dedicated; walked with God, was not (Gen 5:24)',
                        ['Hanoch', 'Enok']),
    ('noah',            'rest; the ark-builder',
                        ['Noé', 'Noach', 'No-ah']),
    ('abraham',         'father of many nations; the friend of God',
                        ['Abe', 'Avi', 'Avram', 'Bram', 'Ibrahim']),
    ('isaac',           'laughter; son of promise to Abraham',
                        ['Ike', 'Izaak', 'Yitzhak', 'Isak', 'Itzhak']),
    ('jacob',           'supplanter; renamed Israel; the patriarch',
                        ['Jake', 'Jakob', 'Yakov', 'Iago', 'Diego', 'Jago']),
    # Twelve tribe sons of Jacob
    ('reuben',          'see, a son! (Gen 29:32); Jacob\'s firstborn',
                        ['Reuven', 'Rueben', 'Reub', 'Ruben']),
    ('simeon',          'hearing (Gen 29:33); Jacob\'s second son',
                        ['Simon', 'Shimon', 'Sim']),
    ('levi-son',        'joined (Gen 29:34); ancestor of the priestly tribe',
                        ['Lev', 'Levy', 'Levi']),
    ('judah',           'praised; the tribe through which Messiah came',
                        ['Jude', 'Judas', 'Yehuda']),
    ('dan-tribe',       'judge (Gen 30:6); son of Jacob and Bilhah',
                        ['Dann']),
    ('naphtali',        'my wrestling (Gen 30:8); tribe of Galilee',
                        ['Naftali']),
    ('gad',             'fortune / a troop cometh (Gen 30:11); warrior tribe',
                        []),
    ('asher',           'happy / blessed (Gen 30:13); coastal tribe',
                        ['Ash', 'Asherel']),
    ('issachar',        'there is reward (Gen 30:18); the tribe of understanding the times',
                        ['Issa', 'Issachar']),
    ('zebulun',         'dwelling / honor (Gen 30:20); maritime-trade Galilean tribe',
                        ['Zebulon', 'Zeb']),
    ('joseph-figure',   'he will add; the dreamer-savior of Egypt',
                        ['Joe', 'Joey', 'Yosef', 'Yousef', 'Yusuf', 'Pepe', 'Giuseppe', 'José']),
    ('benjamin',        'son of the right hand (Gen 35:18); youngest of Jacob; tribe of Saul and Paul',
                        ['Ben', 'Benny', 'Benji', 'Bennett']),
    ('ephraim',         'fruitful (Gen 41:52); Joseph\'s younger son who received the double-portion',
                        ['Efraim', 'Efrem', 'Efren']),
    # Other OT figures
    ('moses',           'drawn out; the lawgiver and deliverer',
                        ['Moshe', 'Mose', 'Musa']),
    ('aaron',           'mountain of strength; the first high priest',
                        ['Aron', 'Ari', 'Aharon']),
    ('caleb-doctrine',  'whole-hearted; one of two faithful spies',
                        ['Cale', 'Kaleb', 'Kayleb']),
    ('joshua-figure',   'Yahweh is salvation; led Israel into the land',
                        ['Josh', 'Yeshua', 'Jeshua', 'Hoshea', 'Joshuah']),
    ('gideon',          'mighty warrior; judge of three hundred',
                        ['Gid', 'Gidi', 'Gideeon']),
    ('samson',          'sun, brightness; the long-haired Nazirite judge',
                        ['Sam', 'Shimshon', 'Samsone']),
    ('boaz-doctrine',   'swift, strong; kinsman-redeemer of Ruth',
                        ['Boz']),
    ('samuel',          'heard by God; the last judge, the first prophet of kings',
                        ['Sam', 'Sammy', 'Shmuel', 'Samuele']),
    ('saul',            'asked of God; the first king of Israel',
                        ['Shaul', 'Sol']),
    ('david',           'beloved; king after God\'s own heart',
                        ['Dave', 'Davy', 'Davis', 'Davide', 'Dawid', 'Dovid']),
    ('solomon',         'peace; David\'s wise son; temple-builder',
                        ['Sol', 'Solly', 'Salomon', 'Salman', 'Shlomo', 'Suleyman']),
    ('elijah',          'my God is Yahweh; great prophet of Mount Carmel',
                        ['Eli', 'Elias', 'Elia', 'Ilya', 'Elie']),
    ('elisha',          'God is salvation; successor of Elijah',
                        ['Elish', 'Elisée']),
    ('hezekiah',        'Yahweh strengthens; reforming king of Judah',
                        ['Hez', 'Heskiah', 'Chizkiyahu']),
    ('josiah',          'the LORD heals; the boy-king of reform',
                        ['Josias', 'Josi']),
    ('asa-king',        'physician / healer; reforming king of Judah',
                        []),
    ('uzziah-king',     'my strength is Yahweh; king of Judah',
                        ['Azariah']),
    ('rehoboam',        'enlarger of the people; Solomon\'s son',
                        ['Roboam']),
    ('manasseh-king',   'making to forget; the wicked-then-repentant king of Judah',
                        ['Menasseh', 'Manasses']),
    ('phinehas',        'mouth of brass; Aaron\'s zealous grandson (Num 25)',
                        ['Pinchas', 'Phineas']),
    # Prophets (writing)
    ('isaiah',          'the LORD is salvation; the messianic prophet',
                        ['Isiah', 'Izzy', 'Yeshayahu', 'Esaias', 'Isaias']),
    ('jeremiah',        'the LORD exalts; the weeping prophet',
                        ['Jerry', 'Jem', 'Yirmeyahu', 'Jeremias']),
    ('ezekiel',         'God will strengthen; the prophet of the exile',
                        ['Zeke', 'Ezekial', 'Yechezkel']),
    ('daniel',          'God is my judge; the prophet in exile',
                        ['Dan', 'Danny', 'Dani', 'Daniyyel']),
    ('hosea',           'salvation; prophet of God\'s covenant love',
                        ['Hoshea', 'Oshea', 'Osee']),
    ('joel-prophet',    'Yahweh is God; prophet of the day of the LORD',
                        ['Yoel']),
    ('amos-prophet',    'burden-bearer; prophet of justice',
                        []),
    ('obadiah',         'servant of Yahweh; shortest OT book',
                        ['Obadias']),
    ('jonah',           'dove; the reluctant prophet',
                        ['Jonas', 'Yonah', 'Yunus']),
    ('micah',           'who is like God; the prophet of Bethlehem',
                        ['Micaiah', 'Mica', 'Mika']),
    ('nahum',           'comforter; prophet of Nineveh\'s fall',
                        ['Naum']),
    ('habakkuk',        'embrace; prophet of \'the just shall live by faith\'',
                        ['Habacuc']),
    ('zephaniah',       'Yahweh hides; prophet of the coming day',
                        ['Tzefania']),
    ('haggai',          'festal; prophet of the second-temple build',
                        ['Haggi', 'Aggeus']),
    ('zechariah',       'Yahweh remembers; prophet of post-exile vision',
                        ['Zach', 'Zac', 'Zacharias']),
    ('malachi',         'my messenger; last prophet of the OT',
                        ['Mal', 'Malakai']),
    ('ezra',            'help; the priest-scribe of the return',
                        ['Esdras', 'Ezri']),
    ('nehemiah',        'the LORD comforts; wall-builder of Jerusalem',
                        ['Neh', 'Nechemiah']),
    ('mordecai',        'devoted to Marduk; Esther\'s cousin and guardian',
                        ['Mort', 'Modi']),
    # NT figures
    ('zacharias-prophet', 'Yahweh remembers; father of John the Baptist',
                        ['Zach', 'Zachary', 'Zac', 'Zak', 'Zachariah']),
    ('john-the-baptist', 'Yahweh is gracious; the forerunner of Christ',
                        ['Jack', 'Johnny', 'Sean', 'Ian', 'Evan', 'Juan', 'Hans', 'Ivan', 'Giovanni', 'Jonas', 'João', 'Yohanan']),
    ('andrew',          'manly, courageous; brought Peter to Jesus',
                        ['Andy', 'Drew', 'Andre', 'Anders', 'Andreas', 'Anderson']),
    ('peter',           'rock; chief apostle, fisherman',
                        ['Pete', 'Petros', 'Pedro', 'Pierre', 'Pyotr', 'Cephas', 'Piotr']),
    ('james-apostle',   'supplanter (Greek for Jacob); apostle and brother of John',
                        ['Jim', 'Jimmy', 'Jamie', 'Jaime', 'Iago', 'Diego', 'Santiago']),
    ('philip',          'lover of horses; apostle and evangelist',
                        ['Phil', 'Felipe', 'Filippo', 'Philippos', 'Phillip']),
    ('nathanael',       'gift of God; \'in whom is no guile\' (John 1:47)',
                        ['Nat', 'Natty', 'Nathaniel', 'Nathan']),
    ('matthew-apostle', 'gift of God; tax collector turned apostle',
                        ['Matt', 'Matty', 'Mateo', 'Matias', 'Mathieu', 'Matthias']),
    ('thomas',          'twin; the doubting-then-believing apostle',
                        ['Tom', 'Tommy', 'Thom', 'Tomás', 'Tomasso', 'Toma']),
    ('mark-book',       'warrior (Latin); the second evangelist',
                        ['Marc', 'Marcus', 'Markos', 'Marko', 'Marcos']),
    ('luke',            'light; physician and evangelist',
                        ['Lucas', 'Lukas', 'Loukas', 'Luca', 'Luc']),
    ('paul',            'small; apostle to the Gentiles',
                        ['Paolo', 'Pablo', 'Pasha', 'Pavel', 'Paulo']),
    ('barnabas-doctrine', 'son of encouragement; companion of Paul',
                        ['Barney', 'Barnaby']),
    ('silas',           'woods, forest; Paul\'s missionary companion',
                        ['Silvanus', 'Cy']),
    ('timothy',         'honored by God; Paul\'s son in the faith',
                        ['Tim', 'Timmy', 'Timotheus', 'Timoteo']),
    ('titus-doctrine',  'honored; Paul\'s Gentile companion',
                        ['Tito', 'Tit']),
    ('apollos',         'destroyer; eloquent Alexandrian Christian (Acts 18-19)',
                        []),
    ('jude',            'praise (same root as Judah); brother of James and of the Lord; author of Jude',
                        ['Judah', 'Judas', 'Yehuda']),
    ('philemon',        'affectionate; addressee of Paul\'s letter; runaway-slave-restorer',
                        []),
    ('onesimus',        'profitable; the runaway slave restored by Paul\'s letter',
                        []),
    ('epaphras',        'lovely; servant of the Colossian church (Col 1:7)',
                        []),
    ('epaphroditus',    'lovely / charming; the Philippian church\'s messenger to Paul (Phil 2:25)',
                        ['Aphro']),
    ('tychicus',        'fortunate; Paul\'s trusted letter-carrier',
                        []),
    ('aristarchus',     'best ruler; companion of Paul in Macedonia and Rome',
                        []),
    ('crispus',         'curly-haired; synagogue ruler at Corinth converted by Paul',
                        []),
    ('trophimus',       'nourishing; Ephesian companion of Paul',
                        []),
    ('sosthenes',       'safe in strength; ruler of synagogue at Corinth',
                        []),
    ('tertius',         'third (Latin); scribe of Romans (Rom 16:22)',
                        []),
    ('agabus',          'locust; prophet who foretold famine (Acts 11) and Paul\'s arrest (Acts 21)',
                        []),
    ('stephen',         'crown; the first Christian martyr',
                        ['Steve', 'Stefan', 'Stephan', 'Esteban', 'Etienne', 'Stefano', 'Stevie']),
    ('cornelius-the-centurion', 'horn (Latin); first Gentile baptized into the church (Acts 10)',
                        ['Corny', 'Cornel', 'Corneliu']),
    ('gabriel',         'man of God; the announcing angel',
                        ['Gabe', 'Gabby', 'Gavriel', 'Gabriele']),
    # Editor's family
    ('malachi-andrew',  'memorial — Adam & Maria\'s first child (2017)',
                        []),
]

FEMALE = [
    # OT matriarchs
    ('sarah',           'princess; Abraham\'s wife; mother of nations',
                        ['Sara', 'Sally', 'Sarai', 'Zara', 'Sariah']),
    ('hagar',           'flight, stranger; Egyptian handmaid; mother of Ishmael',
                        ['Hajar']),
    ('rebekah',         'to bind; Isaac\'s wife; mother of Jacob and Esau',
                        ['Rebecca', 'Becky', 'Becca', 'Reba', 'Beck']),
    ('leah',            'weary; Jacob\'s first wife; mother of Judah',
                        ['Lea', 'Lia', 'Lee', 'Léa']),
    ('rachel',          'ewe; Jacob\'s beloved wife; mother of Joseph and Benjamin',
                        ['Rae', 'Raquel', 'Rachelle', 'Rakel', 'Rahel']),
    ('miriam',          'bitter; prophetess, sister of Moses and Aaron',
                        ['Mariam', 'Mira', 'Miri']),
    ('asenath',         'gift of the sun-god (Egyptian); wife of Joseph; mother of Manasseh and Ephraim',
                        ['Aseneth']),
    # Other OT figures
    ('rahab',           'broad / wide; the Jericho harlot who hid the spies; in Christ\'s line',
                        ['Rachab']),
    ('deborah',         'bee; prophetess and judge',
                        ['Deb', 'Debbie', 'Debby', 'Devorah', 'Deborra']),
    ('jael',            'mountain goat; the tent-peg woman of Judges 4',
                        ['Yael', 'Jaella']),
    ('naomi',           'pleasant; Ruth\'s mother-in-law',
                        ['Nomi', 'Noemi', 'Noémie']),
    ('ruth',            'companion, friend; the Moabite great-grandmother of David',
                        ['Ruthie', 'Rut']),
    ('hannah',          'grace; the long-barren mother of Samuel',
                        ['Hanna', 'Hana', 'Anna', 'Anne', 'Ann', 'Annie', 'Hanne', 'Hannele']),
    ('abigail',         'father is joy; David\'s wife of wisdom',
                        ['Abby', 'Abbie', 'Gail', 'Abi', 'Avigail']),
    ('bathsheba',       'daughter of the oath; mother of Solomon',
                        ['Sheba']),
    ('tamar',           'palm tree; mother in the line of Christ (Matt 1:3)',
                        ['Tamara', 'Tammy', 'Tamir']),
    ('huldah-prophetess', 'weasel; prophetess of Josiah\'s reform (2 Kings 22)',
                        ['Hulda']),
    ('vashti',          'beautiful; the queen Ahasuerus deposed before Esther (Esth 1)',
                        ['Vasht']),
    ('esther',          'star; queen who saved her people',
                        ['Hadassah', 'Essie', 'Hettie', 'Estee', 'Ester']),
    # NT figures
    ('elisabeth-mother-of-john', 'God is my oath; mother of John the Baptist',
                        ['Liz', 'Beth', 'Betsy', 'Eliza', 'Lisbeth', 'Elsa', 'Elise', 'Lisa', 'Bess', 'Lizzie', 'Elspeth']),
    ('mary',            'bitter, beloved; mother of Christ',
                        ['Maria', 'Marie', 'Maryam', 'Molly', 'Polly', 'Mae', 'May', 'Mariah']),
    ('anna-the-prophetess', 'grace; the temple-prophetess at Christ\'s presentation',
                        ['Anne', 'Ann', 'Annie', 'Anya', 'Anita']),
    ('martha',          'lady, mistress; sister of Mary and Lazarus',
                        ['Marta', 'Marty', 'Mattie', 'Marthe']),
    ('mary-magdalene',  'of Magdala; first witness of the resurrection',
                        ['Maggie', 'Madeline', 'Madeleine', 'Magda', 'Magdalena']),
    ('salome',          'peace; mother of James and John; at the resurrection',
                        ['Sal', 'Salma']),
    ('joanna',          'Yahweh is gracious; faithful woman at the resurrection',
                        ['Jo', 'Joan', 'Joanne', 'Johanna', 'Jana']),
    ('tabitha',         'gazelle (Hebrew); raised by Peter (Acts 9:36-42)',
                        ['Tabby', 'Dorcas']),
    ('dorcas',          'gazelle (Greek for Tabitha); the same disciple raised by Peter',
                        ['Tabitha']),
    ('lydia',           'woman from Lydia; first European convert (Acts 16)',
                        ['Liddy', 'Lyddie', 'Lydie']),
    ('phoebe',          'radiant; deacon of Cenchrea (Rom 16:1)',
                        ['Phebe', 'Phoebee']),
    ('priscilla',       'ancient; co-worker with Paul (with husband Aquila)',
                        ['Prisca', 'Cilla', 'Priscille']),
    ('rhoda',           'rose; the maid who knew Peter\'s voice (Acts 12:13-15)',
                        ['Rhody']),
    ('lois',            'unfeigned-faith grandmother of Timothy (2 Tim 1:5)',
                        ['Lo']),
    ('eunice',          'good victory; believing Jewish mother of Timothy (2 Tim 1:5)',
                        ['Uni']),
    ('chloe',           'green sprout; the Christian woman whose household reported Corinthian divisions to Paul (1 Cor 1:11)',
                        ['Clo', 'Khloe', 'Cloe']),
    ('damaris',         'gentle (uncertain); convert at Athens through Paul\'s Mars\' Hill sermon (Acts 17:34)',
                        ['Mara']),
    ('susanna',         'lily; supporter of Christ\'s Galilean ministry (Luke 8:3)',
                        ['Susan', 'Sue', 'Susie', 'Suzy', 'Suzanne', 'Shoshana', 'Zuzanna', 'Susannah']),
    ('claudia',         'noble Roman gens; Christian woman in Rome named in Paul\'s final epistle (2 Tim 4:21)',
                        ['Claudette', 'Claudine', 'Claudine']),
    ('julia',           'noble Roman gens; Christian woman in Rome greeted by Paul (Rom 16:15)',
                        ['Julie', 'Juliet', 'Juliana', 'Yulia', 'Giulia']),
    ('eve',             'life-giver; the first woman, mother of all living (Gen 3:20)',
                        ['Eva', 'Evie', 'Eveline', 'Eveline', 'Chava']),
    ('bethany',         'house of figs; the village of Lazarus, Mary, Martha',
                        ['Beth', 'Bethy']),
    # Editor's family
    ('maria',           'the Latin form of Mary; the editor\'s wife — bitter made sweet',
                        ['Mary', 'Marie', 'Mariana', 'Marietta']),
    ('hope-twin',       'memorial — Adam & Maria\'s twin daughter (2018)',
                        []),
    ('mercy-twin',      'memorial — Adam & Maria\'s twin daughter (2018)',
                        []),
]

UNISEX = [
    ('shiloh-doctrine', 'he whose right it is (Gen 49:10); Messianic title + place-name; modern unisex use',
                        []),
    ('jordan-river',    'descend, flow down; the river of baptism; modern unisex',
                        ['Jordy', 'Jordana']),
    ('eden',            'delight, pleasure; the garden of original creation; modern unisex',
                        ['Edie', 'Edyn']),
    ('carmel',          'vineyard, garden; the mountain where Elijah called down fire; unisex',
                        ['Carmela', 'Carmen']),
    ('zion',            'fortification, parched place; God\'s holy hill; modern unisex',
                        ['Zionie']),
    ('tamar',           'palm tree; primarily female but used as both in modern use',
                        ['Tamara']),
    ('hannah',          'grace; primarily female but rare male use in some traditions',
                        ['Hanna']),
]


def render_card(slug, meaning, variants, headword):
    safe_h = html_mod.escape(headword or slug)
    safe_m = html_mod.escape(meaning)
    variants_html = ''
    if variants:
        v_safe = [html_mod.escape(v) for v in variants]
        variants_html = (
            f'<div class="name-variants"><span class="vk">Also:</span> '
            f'{", ".join(v_safe)}</div>'
        )
    return (
        f'<a class="name-card" href="{slug}.html">'
        f'<div class="name-word">{safe_h}</div>'
        f'<div class="name-meaning">{safe_m}</div>'
        f'{variants_html}'
        f'</a>'
    )


def render_section(title, anchor, intro, names):
    cards = []
    primaries = 0
    variant_count = 0
    for slug, meaning, variants in names:
        hw = get_headword(slug)
        if hw is None:
            print(f'  WARN: no headword for {slug} (skipping)')
            continue
        cards.append(render_card(slug, meaning, variants, hw))
        primaries += 1
        variant_count += len(variants)
    if not cards:
        return ('', 0, 0)
    cards_html = '\n        '.join(cards)
    total = primaries + variant_count
    sec = f'''
    <section class="names-section" id="{anchor}">
        <h2>{title} <span class="count-badge-lg">{primaries} <span style="opacity:0.7;font-weight:400;">primary · {total} total w/ variants</span></span></h2>
        <p class="sec-intro">{intro}</p>
        <div class="names-grid">
        {cards_html}
        </div>
    </section>
    '''
    return (sec, primaries, variant_count)


def main():
    print('Building baby-names.html (with variants)…')
    male_html, male_p, male_v = render_section(
        'Boy Names', 'boys',
        'Biblical names suited for boys — drawn from patriarchs, prophets, judges, kings, and apostles. Each card shows the canonical headword, a one-line meaning, and common nicknames/variants. Click any name for the full dictionary entry.',
        MALE,
    )
    female_html, female_p, female_v = render_section(
        'Girl Names', 'girls',
        'Biblical names suited for girls — drawn from matriarchs, prophetesses, queens, and disciples. Each card shows the canonical headword, a one-line meaning, and common nicknames/variants.',
        FEMALE,
    )
    unisex_html, unisex_p, unisex_v = render_section(
        'Unisex Names', 'unisex',
        'Biblical place-names and concept-names that have crossed into modern use for both boys and girls — like Shiloh, Eden, Jordan, and Zion.',
        UNISEX,
    )

    total_p = male_p + female_p + unisex_p
    total_v = male_v + female_v + unisex_v
    grand = total_p + total_v

    html_out = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="canonical" href="https://usmcmin.org/dictionary/baby-names.html">
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Baby Names from the Bible &mdash; The MOOP Dictionary</title>
    <meta name="description" content="Biblical baby names with Hebrew and Greek meaning, plus common nicknames and language variants — boys, girls, and unisex names from Scripture.">
    <meta property="og:title" content="Biblical Baby Names &mdash; The MOOP Dictionary">
    <meta property="og:description" content="Boy, girl, and unisex names from the Bible — with original-language meaning and common nicknames/variants.">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        :root {{ --bg:#000; --card:#111; --gold:#D4AF37; --gold-light:#F4D470; --white:#FFF; --gray:#888; --border:#333; }}
        body {{ font-family:'Inter',sans-serif; background:var(--bg); color:var(--white); min-height:100vh; line-height:1.7; }}
        h1, h2, h3 {{ font-family:'Playfair Display',serif; }}
        nav {{ display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:4px 8px; padding:10px 16px; border-bottom:1px solid var(--border); position:sticky; top:0; background:rgba(0,0,0,0.95); backdrop-filter:blur(8px); z-index:100; }}
        nav a {{ color:var(--gray); text-decoration:none; font-size:0.8rem; padding:3px 6px; border-radius:6px; }}
        nav a:hover, nav a.active {{ color:var(--gold); }}
        .container {{ max-width:1100px; margin:0 auto; padding:30px 20px 60px; }}
        .hero {{ text-align:center; padding:40px 0 30px; border-bottom:1px solid var(--border); margin-bottom:30px; }}
        .hero h1 {{ font-size:2.6rem; color:var(--gold-light); margin-bottom:12px; }}
        .hero .lead {{ color:var(--gray); max-width:680px; margin:10px auto; font-size:1rem; }}
        .hero .totals {{ display:flex; flex-wrap:wrap; gap:10px; justify-content:center; margin-top:14px; }}
        .hero .totals > span {{ display:inline-block; background:var(--gold); color:#000; font-weight:700; padding:4px 14px; border-radius:14px; font-size:0.82rem; }}
        .quick-nav {{ display:flex; flex-wrap:wrap; gap:10px; justify-content:center; margin:28px 0 10px; }}
        .quick-nav a {{ background:var(--card); border:1px solid var(--border); color:var(--white) !important; text-decoration:none; padding:8px 18px; border-radius:20px; font-size:0.9rem; }}
        .quick-nav a:hover {{ border-color:var(--gold); color:var(--gold) !important; }}
        .editor-note {{ background:rgba(212,175,55,0.05); border:1px solid var(--border); border-radius:10px; padding:18px 22px; margin:24px 0 0; font-size:0.92rem; }}
        .editor-note h3 {{ color:var(--gold); font-size:1rem; margin-bottom:6px; font-family:'Inter',sans-serif; font-weight:600; }}
        .names-section {{ margin:48px 0; scroll-margin-top:80px; }}
        .names-section h2 {{ color:var(--gold-light); font-size:1.7rem; border-bottom:1px solid var(--border); padding-bottom:10px; margin-bottom:8px; }}
        .sec-intro {{ color:var(--gray); font-size:0.92rem; margin-bottom:20px; max-width:760px; }}
        .count-badge-lg {{ display:inline-block; background:var(--gold); color:#000; font-size:0.75rem; font-weight:700; padding:3px 10px; border-radius:10px; margin-left:8px; vertical-align:middle; }}
        .names-grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(260px, 1fr)); gap:12px; }}
        .name-card {{ display:block; background:var(--card); border:1px solid var(--border); border-radius:10px; padding:14px 18px; text-decoration:none; color:var(--white) !important; transition:border-color 0.2s, transform 0.15s; }}
        .name-card:hover {{ border-color:var(--gold); transform:translateY(-1px); }}
        .name-word {{ font-family:'Playfair Display',serif; font-size:1.18rem; color:var(--gold-light); margin-bottom:5px; }}
        .name-meaning {{ font-size:0.83rem; color:var(--gray); line-height:1.5; }}
        .name-variants {{ font-size:0.78rem; color:var(--gold); margin-top:7px; padding-top:6px; border-top:1px dashed rgba(212,175,55,0.25); font-style:italic; }}
        .name-variants .vk {{ font-style:normal; opacity:0.7; font-size:0.72rem; letter-spacing:0.04em; }}
        footer {{ text-align:center; padding:32px 20px; border-top:1px solid var(--border); margin-top:50px; color:var(--gray); font-size:0.88rem; }}
        footer a {{ color:var(--gray); text-decoration:none; }}
        footer a:hover {{ color:var(--gold); }}
        body.light-mode {{ --bg:#F5F3EF; --card:#FFF; --white:#1a1a1a; --gray:#666; --border:#d4d0c8; background:#F5F3EF; color:#1a1a1a; }}
        body.light-mode nav {{ background:rgba(245,243,239,0.97); }}
        body.light-mode .name-card,
        body.light-mode .quick-nav a,
        body.light-mode .editor-note {{ background:#fff; border-color:#d4d0c8; }}
        body.light-mode .editor-note {{ background:rgba(212,175,55,0.04); }}
        a, a:link, a:visited {{ color:var(--gold) !important; }}
        @media (max-width:560px) {{ .hero h1 {{ font-size:2rem; }} .names-grid {{ grid-template-columns:1fr; }} }}
    </style>
</head>
<body>
    <nav>
        <a href="../index.html">Home</a>
        <a href="../bible.html">BTE</a>
        <a href="index.html" class="active">Dictionary</a>
        <a href="names.html">Biblical Names</a>
        <a href="baby-names.html" class="active">Baby Names</a>
        <a href="../blog.html">Blog</a>
    </nav>
    <div class="container">
        <div class="hero">
            <h1>Biblical Baby Names</h1>
            <p class="lead">Boy, girl, and unisex names drawn from Scripture &mdash; with Hebrew, Greek, and original-language meaning. Each card lists common nicknames and language variants (English, Hebrew, Greek, Spanish, Italian, etc.) and links to the full dictionary entry.</p>
            <div class="totals">
                <span>{total_p} primary names</span>
                <span>{total_v} variants</span>
                <span>{grand} total displayed</span>
            </div>
            <div class="quick-nav">
                <a href="#boys">Boys &#9662;</a>
                <a href="#girls">Girls &#9662;</a>
                <a href="#unisex">Unisex &#9662;</a>
                <a href="names.html">Full Names Index &rarr;</a>
            </div>
            <div class="editor-note">
                <h3>&#128153; A Note from the Editor</h3>
                <p>This baby-name directory is split off from the larger biblical-names index to serve expecting parents and curious readers. The page is curated by Adam Johns, editor of the MOOP Dictionary, and includes a small number of personal-family entries (Maria, Malachi Andrew, Hope, Mercy) representing his wife and three children lost too soon. Each name links to its full entry with original-language etymology, and lists common nicknames and language variants for the same name.</p>
            </div>
        </div>

        {male_html}
        {female_html}
        {unisex_html}

        <section class="names-section">
            <h2>Looking for More?</h2>
            <p class="sec-intro">The full <a href="names.html">Biblical Names index</a> covers every name in the dictionary (not just those traditionally given as baby names). The full <a href="index.html">dictionary index</a> covers all 5,000+ entries across doctrine, persons, places, and Hebrew/Greek word studies.</p>
        </section>
    </div>
    <footer>
        <p>Baby Names from the Bible &middot; Part of <a href="index.html">The MOOP Dictionary</a> &middot; <a href="../bible.html">Bible Translation Engine</a></p>
        <p style="margin-top:8px;font-size:0.78rem;">&copy; 2026 U.S.M.C. Ministries</p>
    </footer>
</body>
</html>'''

    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(html_out)

    print(f'Wrote {OUT}')
    print(f'  Primary names: {total_p}')
    print(f'    Boys: {male_p}, Girls: {female_p}, Unisex: {unisex_p}')
    print(f'  Variants: {total_v}')
    print(f'    Boys: {male_v}, Girls: {female_v}, Unisex: {unisex_v}')
    print(f'  GRAND TOTAL (primary + variants): {grand}')


if __name__ == '__main__':
    main()
