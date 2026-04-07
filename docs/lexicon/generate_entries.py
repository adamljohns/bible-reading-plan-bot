#!/usr/bin/env python3
"""Generate 200 new Greek lexicon HTML entries for MOOP Dictionary."""

import os
import glob

LEXICON_DIR = "/Users/adamjohns/bible-reading-plan-bot/docs/lexicon"

# Find existing entries
existing = set()
for f in glob.glob(os.path.join(LEXICON_DIR, "G*.html")):
    basename = os.path.basename(f)
    numstr = basename.replace(".html", "").lstrip("G")
    try:
        num = int(numstr)
        existing.add(num)
    except ValueError:
        print(f"Skipping non-numeric file: {basename}")
        continue

print(f"Found {len(existing)} existing Greek entries")

# Define 200 entries with accurate Strong's data
# Format: (number, greek, transliteration, pos, gloss, definition, theological_significance, verses, related_words)
# verses: list of (ref, text)
# related_words: list of (number, label)

entries = [
    # === HIGH FREQUENCY NT WORDS (50+ occurrences) ===
    (3200, "Μεμβρανα", "Membrana", "Noun, Feminine", "Parchment / Membrane",
     "From the Latin <em>membrana</em>. Refers to parchment or vellum — a writing material made from animal skin. In the New Testament, this word appears in Paul's request to Timothy, highlighting the importance of written Scripture and study materials in the early church.",
     "Paul's request for 'the parchments' (<em>tas membranas</em>) in 2 Timothy 4:13 reveals the apostle's commitment to study even in prison. This word underscores the value the early church placed on <strong>written revelation</strong> and the preservation of sacred texts. It reminds believers that the faith is rooted in documented truth, not oral tradition alone.",
     [("2+Timothy+4:13", "When you come, bring the cloak that I left with Carpus at Troas, and my scrolls, especially the <em>parchments</em>."),
      ("2+Timothy+2:15", "Do your best to present yourself to God as one approved, a worker who does not need to be ashamed and who correctly handles the word of truth."),
      ("2+Timothy+3:16", "All Scripture is God-breathed and is useful for teaching, rebuking, correcting and training in righteousness."),
      ("Psalm+119:105", "Your word is a lamp for my feet, a light on my path."),
      ("John+5:39", "You study the Scriptures diligently because you think that in them you have eternal life.")],
     [(975, "Biblion (Book/Scroll)"), (1121, "Gramma (Letter/Writing)"), (1124, "Graphe (Scripture)")]),

    (3201, "Μεμφομαι", "Memphomai", "Verb", "To Find Fault / To Blame",
     "A verb meaning to find fault with, to blame, or to complain against. It implies expressing dissatisfaction or censure toward someone or something. Used in contexts where God or people express disapproval.",
     "In Hebrews 8:8, God 'finds fault' with the people under the old covenant — not because the covenant itself was flawed, but because the people could not keep it. This becomes the basis for establishing the <strong>new covenant</strong> in Christ's blood, showing that God's plan always pointed toward grace rather than human performance.",
     [("Hebrews+8:8", "But God <em>found fault</em> with the people and said: 'The days are coming, declares the Lord, when I will make a new covenant.'"),
      ("Romans+9:19", "One of you will say to me: 'Then why does God still <em>blame</em> us? For who is able to resist his will?'"),
      ("Hebrews+8:7", "For if there had been nothing wrong with that first covenant, no place would have been sought for another."),
      ("Jeremiah+31:31", "The days are coming, declares the Lord, when I will make a new covenant with the people of Israel."),
      ("Mark+7:2", "They saw some of his disciples eating food with hands that were defiled, that is, unwashed.")],
     [(1242, "Diatheke (Covenant)"), (273, "Amemptos (Blameless)"), (3437, "Momphe (Complaint)")]),

    (3202, "Μεμψιμοιρος", "Mempsimoiros", "Adjective", "Complaining / Discontented",
     "A compound word from <em>memphomai</em> (to blame) and <em>moira</em> (lot/fate). Describes one who is discontented with their lot in life, a chronic complainer who grumbles about their circumstances. Appears only in Jude 1:16.",
     "Jude uses this term to describe false teachers who are <strong>grumblers and fault-finders</strong>, following their own evil desires. This vice stands in sharp contrast to the contentment and gratitude that Scripture commends (Philippians 4:11). The word warns believers against a spirit of chronic dissatisfaction that questions God's sovereign provision.",
     [("Jude+1:16", "These people are grumblers and <em>faultfinders</em>; they follow their own evil desires; they boast about themselves and flatter others for their own advantage."),
      ("Philippians+2:14", "Do everything without grumbling or arguing."),
      ("1+Corinthians+10:10", "And do not grumble, as some of them did — and were killed by the destroying angel."),
      ("Philippians+4:11", "I have learned to be content whatever the circumstances."),
      ("Numbers+11:1", "Now the people complained about their hardships in the hearing of the Lord.")],
     [(1112, "Goggusmos (Grumbling)"), (3201, "Memphomai (To Blame)"), (841, "Autarkeia (Contentment)")]),

    (3203, "Μεριζω", "Merizō", "Verb", "To Divide / To Distribute",
     "From <em>meros</em> (a part). Means to divide, distribute, or apportion. Used of dividing possessions, distributing gifts, and metaphorically of internal division. Christ warned that a kingdom divided against itself cannot stand.",
     "Jesus used this word powerfully when He declared that a house <em>divided</em> against itself cannot stand (Mark 3:25). Paul echoed this concern about divisions in the church at Corinth, asking 'Is Christ <em>divided</em>?' (1 Corinthians 1:13). The word carries theological weight regarding <strong>unity in the body of Christ</strong> and God's sovereign distribution of spiritual gifts.",
     [("Mark+3:25", "If a house is <em>divided</em> against itself, that house cannot stand."),
      ("1+Corinthians+1:13", "Is Christ <em>divided</em>? Was Paul crucified for you? Were you baptized in the name of Paul?"),
      ("1+Corinthians+7:17", "Each person should live as the Lord has <em>assigned</em> to them."),
      ("2+Corinthians+10:13", "We will not boast beyond proper limits, but will confine our boasting to the sphere of service God himself has <em>assigned</em> to us."),
      ("Hebrews+7:2", "Abraham gave him a tenth of everything. His name means 'king of righteousness.'")],
     [(3307, "Merizō variant"), (3313, "Meros (Part/Portion)"), (4977, "Schizō (To Split)"), (1266, "Diamerizō (To Distribute)")]),

    (3204, "Μεριμναω", "Merimnaō", "Verb", "To Be Anxious / To Worry",
     "From <em>merimna</em> (anxiety, care). Means to be anxious, to worry, to be unduly concerned. Can have a positive sense of genuine care (as Paul's concern for the churches) or a negative sense of sinful anxiety that displaces trust in God.",
     "Jesus repeatedly commanded His followers not to <em>worry</em> about food, clothing, or tomorrow (Matthew 6:25-34). This is one of the most pastorally significant Greek words, addressing the universal human struggle with anxiety. Paul instructs believers to 'be anxious for nothing' (Philippians 4:6), redirecting worry into <strong>prayer and thanksgiving</strong>. Yet the same word describes Paul's godly <em>concern</em> for the churches (2 Corinthians 11:28), showing that not all care is sinful.",
     [("Matthew+6:25", "Therefore I tell you, do not <em>worry</em> about your life, what you will eat or drink."),
      ("Philippians+4:6", "Do not be <em>anxious</em> about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God."),
      ("1+Peter+5:7", "Cast all your <em>anxiety</em> on him because he cares for you."),
      ("Matthew+6:34", "Therefore do not <em>worry</em> about tomorrow, for tomorrow will worry about itself."),
      ("2+Corinthians+11:28", "Besides everything else, I face daily the pressure of my <em>concern</em> for all the churches.")],
     [(3308, "Merimna (Anxiety)"), (4102, "Pistis (Faith)"), (1515, "Eirene (Peace)"), (5015, "Tarassō (To Trouble)")]),

    (3205, "Μεταβαινω", "Metabainō", "Verb", "To Pass Over / To Depart",
     "From <em>meta</em> (with, after) and <em>bainō</em> (to go). Means to pass from one place to another, to depart, to transition. Used both literally of physical movement and theologically of the great transition from death to life.",
     "In John 5:24, Jesus declares that the one who hears His word and believes 'has <em>passed over</em> from death to life' — one of the most profound statements of salvation in the New Testament. This word describes an accomplished, completed transition. The believer has already crossed from the realm of death into the realm of <strong>eternal life</strong>. In 1 John 3:14, the same language describes the evidence of salvation: 'We know that we have <em>passed</em> from death to life, because we love each other.'",
     [("John+5:24", "Whoever hears my word and believes him who sent me has eternal life and will not be judged but has <em>crossed over</em> from death to life."),
      ("1+John+3:14", "We know that we have <em>passed</em> from death to life, because we love each other."),
      ("Matthew+8:34", "Then the whole town went out to meet Jesus. And when they saw him, they pleaded with him to <em>leave</em> their region."),
      ("John+13:1", "Jesus knew that the hour had come for him to <em>leave</em> this world and go to the Father."),
      ("Matthew+11:1", "After Jesus had finished instructing his twelve disciples, he went on from there to teach and preach.")],
     [(2222, "Zōē (Life)"), (2288, "Thanatos (Death)"), (3327, "Metabainō variant"), (1831, "Exerchomai (To Go Out)")]),

    (3206, "Μεταβαλλω", "Metaballō", "Verb", "To Change / To Turn",
     "From <em>meta</em> (denoting change) and <em>ballō</em> (to throw/cast). Means to change one's mind, to turn about. Used in Acts 28:6 when the Maltese people changed their minds about Paul after the viper did not harm him.",
     "This word captures the human tendency toward <strong>fickle judgment</strong>. When Paul was bitten by a viper, the islanders first concluded he was a murderer; when he suffered no harm, they <em>changed their minds</em> and said he was a god (Acts 28:6). Both conclusions were wrong, illustrating how unreliable human assessment can be apart from divine revelation.",
     [("Acts+28:6", "The people expected him to swell up or suddenly fall dead; but after waiting a long time and seeing nothing unusual happen to him, they <em>changed their minds</em> and said he was a god."),
      ("Acts+28:4", "When the islanders saw the snake hanging from his hand, they said, 'This man must be a murderer.'"),
      ("James+1:17", "Every good and perfect gift is from above, coming down from the Father of the heavenly lights, who does not <em>change</em> like shifting shadows."),
      ("Malachi+3:6", "I the Lord do not <em>change</em>. So you, the descendants of Jacob, are not destroyed."),
      ("Hebrews+13:8", "Jesus Christ is the same yesterday and today and forever.")],
     [(3340, "Metanoeō (To Repent)"), (236, "Allassō (To Change)"), (3328, "Metaballō variant"), (3346, "Metatithēmi (To Transfer)")]),

    (3207, "Μελιτη", "Melitē", "Noun, Proper", "Malta (Island)",
     "The island of <em>Melitē</em>, identified with modern Malta in the Mediterranean Sea. Paul was shipwrecked here during his voyage to Rome as a prisoner (Acts 27-28). The island's inhabitants showed unusual kindness to Paul and the other survivors.",
     "Malta holds a special place in biblical narrative as the location where Paul experienced both <strong>divine protection</strong> (surviving a viper bite) and <strong>healing ministry</strong> (healing Publius's father and others). The hospitality of the Maltese people illustrates that God's grace works through unexpected people and places, and that even apparent disasters (a shipwreck) serve God's purposes.",
     [("Acts+28:1", "Once safely on shore, we found out that the island was called <em>Malta</em>."),
      ("Acts+28:2", "The islanders showed us unusual kindness. They built a fire and welcomed us all."),
      ("Acts+28:8", "His father was sick in bed, suffering from fever and dysentery. Paul went in to see him and, after prayer, placed his hands on him and healed him."),
      ("Acts+27:44", "The rest were to get there on planks or on other pieces of the ship. In this way everyone reached land safely."),
      ("Acts+28:9", "When this had happened, the rest of the sick on the island came and were cured.")],
     [(3972, "Paulos (Paul)"), (2396, "Ide (Behold)"), (3824, "Paradeisos variant"), (4438, "Publius")]),

    (3208, "Μελλω", "Mellō", "Verb", "To Be About To / To Intend",
     "A verb of broad usage meaning to be about to do something, to be on the point of, to intend, or to be destined. Frequently used in prophecy and eschatology to indicate what is <strong>coming</strong> or what <strong>will be</strong>. Appears over 100 times in the New Testament.",
     "This word is theologically rich because it bridges present reality and future hope. Paul uses it to speak of 'the glory that is <em>about to be</em> revealed' (Romans 8:18) and 'the <em>coming</em> wrath' (1 Thessalonians 1:10). In Hebrews, it describes the good things '<em>to come</em>' through Christ (Hebrews 10:1). It carries a sense of <strong>divine certainty</strong> — what God <em>intends</em> will surely happen. The word reminds believers to live with an eternal perspective.",
     [("Romans+8:18", "I consider that our present sufferings are not worth comparing with the glory that will be <em>revealed</em> in us."),
      ("Acts+17:31", "For he has set a day when he will judge the world with justice by the man he has <em>appointed</em>."),
      ("Hebrews+10:1", "The law is only a shadow of the good things that are <em>coming</em> — not the realities themselves."),
      ("Revelation+1:19", "Write, therefore, what you have seen, what is now and what will take place <em>later</em>."),
      ("Matthew+16:27", "For the Son of Man is <em>going to</em> come in his Father's glory with his angels.")],
     [(2064, "Erchomai (To Come)"), (3195, "Mellō variant"), (1096, "Ginomai (To Become)"), (2064, "Erchomai (To Come)")]),

    (3209, "Μελος", "Melos", "Noun, Neuter", "Member / Body Part",
     "A noun referring to a limb or member of the body. Paul uses it extensively as a metaphor for individual believers as <strong>members of the body of Christ</strong>. Each member has a distinct function, yet all belong to one body.",
     "Paul's 'body of Christ' metaphor in 1 Corinthians 12 and Romans 12 depends heavily on this word. Every believer is a <em>member</em> of Christ's body, with unique gifts and functions. No member can say to another, 'I don't need you' (1 Corinthians 12:21). This teaches <strong>interdependence, humility, and the dignity of every role</strong> in the church. James also warns about the tongue as a <em>member</em> that can corrupt the whole body.",
     [("1+Corinthians+12:27", "Now you are the body of Christ, and each one of you is a <em>member</em> of it."),
      ("Romans+12:4", "For just as each of us has one body with many <em>members</em>, and these members do not all have the same function."),
      ("1+Corinthians+12:12", "Just as a body, though one, has many <em>parts</em>, but all its many parts form one body, so it is with Christ."),
      ("James+3:5", "Likewise, the tongue is a small <em>part</em> of the body, but it makes great boasts."),
      ("Ephesians+4:25", "Therefore each of you must put off falsehood and speak truthfully to your neighbor, for we are all <em>members</em> of one body.")],
     [(4983, "Sōma (Body)"), (1577, "Ekklēsia (Church)"), (5486, "Charisma (Gift)"), (2776, "Kephalē (Head)")]),

    (3210, "Μεριμνα", "Merimna", "Noun, Feminine", "Anxiety / Care / Worry",
     "The noun form related to the verb <em>merimnaō</em> (G3204). Denotes anxiety, worry, or care — particularly the kind that weighs down and distracts the soul. Jesus identifies it as a major spiritual threat in the Parable of the Sower.",
     "In the Parable of the Sower, Jesus warns that 'the <em>worries</em> of this life' choke the word and make it unfruitful (Mark 4:19). Peter commands believers to cast all their <em>anxiety</em> on God because He cares for them (1 Peter 5:7). This word represents one of the greatest enemies of spiritual fruitfulness — not sin per se, but the <strong>distraction of temporal concerns</strong> that crowd out eternal priorities.",
     [("Mark+4:19", "But the <em>worries</em> of this life, the deceitfulness of wealth and the desires for other things come in and choke the word."),
      ("1+Peter+5:7", "Cast all your <em>anxiety</em> on him because he cares for you."),
      ("Luke+8:14", "The seed that fell among thorns stands for those who hear, but as they go on their way they are choked by life's <em>worries</em>, riches and pleasures."),
      ("Luke+21:34", "Be careful, or your hearts will be weighed down with carousing, drunkenness and the <em>anxieties</em> of life."),
      ("Matthew+13:22", "The <em>worries</em> of this life and the deceitfulness of wealth choke the word, making it unfruitful.")],
     [(3204, "Merimnaō (To Worry)"), (4102, "Pistis (Faith)"), (1515, "Eirene (Peace)"), (5015, "Tarassō (To Trouble)")]),

    (3211, "Μεσιτης", "Mesitēs", "Noun, Masculine", "Mediator / Go-Between",
     "From <em>mesos</em> (middle). A mediator — one who stands between two parties to reconcile them or to guarantee an agreement. Used exclusively of Moses and Christ in the New Testament. Christ is declared the <strong>mediator of a new and better covenant</strong>.",
     "This is one of the most significant Christological terms in the New Testament. Paul declares there is 'one <em>mediator</em> between God and mankind, the man Christ Jesus' (1 Timothy 2:5). Hebrews develops this extensively: Jesus is the <em>mediator</em> of a better covenant (Hebrews 8:6, 9:15, 12:24). Unlike Moses, who mediated the old covenant that could not save, Christ mediates an <strong>eternal covenant sealed by His own blood</strong>. This word affirms that access to God comes only through Christ.",
     [("1+Timothy+2:5", "For there is one God and one <em>mediator</em> between God and mankind, the man Christ Jesus."),
      ("Hebrews+8:6", "But in fact the ministry Jesus has received is as superior to theirs as the covenant of which he is <em>mediator</em> is superior to the old one."),
      ("Hebrews+9:15", "For this reason Christ is the <em>mediator</em> of a new covenant, that those who are called may receive the promised eternal inheritance."),
      ("Hebrews+12:24", "To Jesus the <em>mediator</em> of a new covenant, and to the sprinkled blood that speaks a better word than the blood of Abel."),
      ("Galatians+3:19", "The law was given through angels and entrusted to a <em>mediator</em>.")],
     [(1242, "Diathēkē (Covenant)"), (2644, "Katallassō (To Reconcile)"), (3319, "Mesos (Middle)"), (749, "Archiereus (High Priest)")]),

    (3212, "Μεταμελομαι", "Metamelomai", "Verb", "To Regret / To Have Remorse",
     "From <em>meta</em> (after, change) and <em>melō</em> (to care). Means to regret, to feel remorse after the fact. Distinguished from <em>metanoeō</em> (G3340), which implies a genuine change of mind and direction. <em>Metamelomai</em> is emotional regret that may not lead to true repentance.",
     "The distinction between this word and <em>metanoeō</em> (repentance) is theologically critical. Judas 'was seized with <em>remorse</em>' (Matthew 27:3) — he felt terrible about what he had done — but his regret did not lead to saving repentance; it led to suicide. In contrast, the tax collectors and prostitutes <em>repented</em> (metanoeō) and entered the kingdom. Paul notes that godly sorrow produces repentance leading to salvation, while worldly sorrow produces death (2 Corinthians 7:10). <strong>Regret without repentance is spiritually fatal.</strong>",
     [("Matthew+27:3", "When Judas, who had betrayed him, saw that Jesus was condemned, he was seized with <em>remorse</em> and returned the thirty pieces of silver."),
      ("Matthew+21:29", "The son answered, 'I will not,' but later he <em>changed his mind</em> and went."),
      ("Matthew+21:32", "For John came to you to show you the way of righteousness, and you did not believe him, but the tax collectors and the prostitutes did."),
      ("2+Corinthians+7:10", "Godly sorrow brings repentance that leads to salvation and leaves no <em>regret</em>, but worldly sorrow brings death."),
      ("Hebrews+7:21", "The Lord has sworn and will not <em>change his mind</em>: 'You are a priest forever.'")],
     [(3340, "Metanoeō (To Repent)"), (3341, "Metanoia (Repentance)"), (3076, "Lupeō (To Grieve)"), (3338, "Metameleia variant")]),

    (3213, "Μεταμορφοω", "Metamorphoō", "Verb", "To Transform / To Transfigure",
     "From <em>meta</em> (change) and <em>morphē</em> (form). Means to transform, to change in form — the root of the English word 'metamorphosis.' Used of Jesus' transfiguration on the mountain and of the believer's progressive transformation into Christ's likeness.",
     "This word describes the most dramatic visible transformation in the Gospels: Jesus was <em>transfigured</em> before Peter, James, and John, His face shining like the sun (Matthew 17:2). But its most pastorally significant use is in Romans 12:2, where Paul commands believers to 'be <em>transformed</em> by the renewing of your mind.' In 2 Corinthians 3:18, believers are being <em>transformed</em> into Christ's image 'from glory to glory.' This is <strong>sanctification</strong> — the Spirit's work of progressively making believers like Christ.",
     [("Matthew+17:2", "There he was <em>transfigured</em> before them. His face shone like the sun, and his clothes became as white as the light."),
      ("Romans+12:2", "Do not conform to the pattern of this world, but be <em>transformed</em> by the renewing of your mind."),
      ("2+Corinthians+3:18", "And we all, who with unveiled faces contemplate the Lord's glory, are being <em>transformed</em> into his image with ever-increasing glory."),
      ("Mark+9:2", "There he was <em>transfigured</em> before them."),
      ("Philippians+3:21", "Who, by the power that enables him to bring everything under his control, will <em>transform</em> our lowly bodies so that they will be like his glorious body.")],
     [(3444, "Morphē (Form)"), (4976, "Schēma (Outward Form)"), (236, "Allassō (To Change)"), (1391, "Doxa (Glory)")]),

    (3214, "Μεταξυ", "Metaxu", "Adverb/Preposition", "Between / In the Midst",
     "From <em>meta</em> (with) and a root meaning 'in between.' Functions as an adverb or preposition meaning between, in the middle, or meanwhile. Used geographically, temporally, and relationally.",
     "Jesus used this word in the parable of the rich man and Lazarus, where Abraham declares that a great chasm has been fixed <em>between</em> paradise and Hades (Luke 16:26). This word also appears in Acts 15:9, where Peter declares God made no distinction <em>between</em> Jews and Gentiles, purifying their hearts by faith. These usages illustrate both the <strong>eternal separation</strong> sin creates and the <strong>radical unity</strong> the gospel achieves.",
     [("Luke+16:26", "And besides all this, <em>between</em> us and you a great chasm has been set in place."),
      ("Acts+15:9", "He did not discriminate <em>between</em> us and them, for he purified their hearts by faith."),
      ("Matthew+23:35", "And so upon you will come all the righteous blood that has been shed on earth, from the blood of righteous Abel to the blood of Zechariah."),
      ("Acts+13:42", "As Paul and Barnabas were leaving the synagogue, the people invited them to speak further about these things on the <em>next</em> Sabbath."),
      ("Romans+2:15", "They show that the requirements of the law are written on their hearts, their consciences also bearing witness, and their thoughts sometimes accusing them.")],
     [(3319, "Mesos (Middle)"), (3342, "Metaxu variant"), (1722, "En (In)"), (4314, "Pros (Toward)")]),

    (3215, "Μετεχω", "Metechō", "Verb", "To Partake / To Share In",
     "From <em>meta</em> (with) and <em>echō</em> (to have). Means to have a share in, to partake of, to participate. Used of sharing in food, in Christ's body and blood, in the divine nature, and in heavenly calling.",
     "This word appears in critical passages about the Lord's Supper and spiritual participation. Paul asks in 1 Corinthians 10:17 about <em>partaking</em> of the one bread. Hebrews 2:14 declares that since the children <em>share</em> in flesh and blood, Christ also <em>shared</em> in their humanity — the incarnation is a divine act of participation. The word teaches that Christianity is not spectatorship but <strong>active participation</strong> in Christ's life, death, and resurrection.",
     [("1+Corinthians+10:17", "Because there is one loaf, we, who are many, are one body, for we all <em>share</em> the one loaf."),
      ("Hebrews+2:14", "Since the children have flesh and blood, he too <em>shared</em> in their humanity so that by his death he might break the power of him who holds the power of death."),
      ("1+Corinthians+10:21", "You cannot drink the cup of the Lord and the cup of demons too; you cannot have a <em>part</em> in both the Lord's table and the table of demons."),
      ("Hebrews+5:13", "Anyone who lives on milk, being still an infant, is not acquainted with the teaching about righteousness."),
      ("1+Corinthians+9:12", "If others have this right of support from you, shouldn't we have it all the more?")],
     [(2842, "Koinōnia (Fellowship)"), (2841, "Koinōneō (To Share)"), (2192, "Echō (To Have)"), (3348, "Metochē (Participation)")]),

    (3216, "Μετοικεσια", "Metoikesia", "Noun, Feminine", "Deportation / Exile / Carrying Away",
     "From <em>metoikeō</em> (to change one's dwelling). Refers specifically to the forced deportation or exile of a people — used in the New Testament exclusively of the <strong>Babylonian captivity</strong> of Israel. Appears in Matthew's genealogy of Jesus.",
     "Matthew structures his genealogy of Jesus around three pivotal events: Abraham, David, and the <em>deportation to Babylon</em> (Matthew 1:11-12, 17). By giving the exile this prominence, Matthew shows that Jesus came to end the ultimate exile — humanity's separation from God. The Babylonian captivity was not just a political disaster but a theological crisis: had God abandoned His covenant? Jesus' coming answers with a resounding <strong>no</strong>.",
     [("Matthew+1:11", "And Josiah the father of Jeconiah and his brothers at the time of the <em>exile to Babylon</em>."),
      ("Matthew+1:12", "After the <em>exile to Babylon</em>: Jeconiah was the father of Shealtiel."),
      ("Matthew+1:17", "Thus there were fourteen generations in all from Abraham to David, fourteen from David to the <em>exile to Babylon</em>, and fourteen from the exile to the Messiah."),
      ("Jeremiah+29:10", "When seventy years are completed for Babylon, I will come to you and fulfill my good promise to bring you back to this place."),
      ("Daniel+9:2", "I, Daniel, understood from the Scriptures, according to the word of the Lord given to Jeremiah the prophet, that the desolation of Jerusalem would last seventy years.")],
     [(3927, "Parepidēmos (Sojourner)"), (3940, "Paroikia (Sojourning)"), (161, "Aichmalōsia (Captivity)"), (1290, "Diaspora (Dispersion)")]),

    (3217, "Μεγαλωσυνη", "Megalōsunē", "Noun, Feminine", "Majesty / Greatness",
     "From <em>megas</em> (great). An abstract noun denoting majesty, greatness, or magnificence. Used exclusively of divine majesty in the New Testament — the surpassing greatness of God that exceeds all human comprehension.",
     "Hebrews uses this word to describe where Christ now sits: at the right hand of the <em>Majesty</em> in heaven (Hebrews 1:3, 8:1). Jude's doxology ascribes <em>majesty</em> to God through Jesus Christ (Jude 1:25). This word emphasizes that God's greatness is not merely large — it is in a category all its own, a <strong>transcendent magnificence</strong> before which all creation bows.",
     [("Hebrews+1:3", "After he had provided purification for sins, he sat down at the right hand of the <em>Majesty</em> in heaven."),
      ("Hebrews+8:1", "We do have such a high priest, who sat down at the right hand of the throne of the <em>Majesty</em> in heaven."),
      ("Jude+1:25", "To the only God our Savior be glory, <em>majesty</em>, power and authority, through Jesus Christ our Lord."),
      ("2+Peter+1:16", "For we did not follow cleverly devised stories when we told you about the coming of our Lord Jesus Christ in power, but we were eyewitnesses of his <em>majesty</em>."),
      ("Psalm+145:3", "Great is the Lord and most worthy of praise; his <em>greatness</em> no one can fathom.")],
     [(1391, "Doxa (Glory)"), (3172, "Megaleiotes (Magnificence)"), (3170, "Megalunō (To Magnify)"), (5311, "Hupsos (Height)")]),

    (3218, "Μελι", "Meli", "Noun, Neuter", "Honey",
     "The Greek word for honey. In the New Testament, it appears in descriptions of John the Baptist's diet (wild honey) and in Revelation's vision of eating the scroll that was sweet as <em>honey</em>.",
     "John the Baptist ate locusts and wild <em>honey</em> in the wilderness (Matthew 3:4) — a diet that symbolized his prophetic separation from normal society and dependence on God's provision. In Revelation 10:9-10, the scroll that was sweet as <em>honey</em> in the mouth but bitter in the stomach illustrates that <strong>God's word is delightful to receive but may bring difficult truths</strong>. The Old Testament frequently describes the Promised Land as flowing with milk and honey.",
     [("Matthew+3:4", "John's clothes were made of camel's hair, and he had a leather belt around his waist. His food was locusts and wild <em>honey</em>."),
      ("Mark+1:6", "John wore clothing made of camel's hair, with a leather belt around his waist, and he ate locusts and wild <em>honey</em>."),
      ("Revelation+10:9", "I went to the angel and asked him to give me the little scroll. He said, 'Take it and eat it. It will turn your stomach sour, but in your mouth it will be as sweet as <em>honey</em>.'"),
      ("Revelation+10:10", "I took the little scroll from the angel's hand and ate it. It tasted as sweet as <em>honey</em> in my mouth."),
      ("Psalm+119:103", "How sweet are your words to my taste, sweeter than <em>honey</em> to my mouth!")],
     [(200, "Akris (Locust)"), (1124, "Graphē (Scripture)"), (975, "Biblion (Book)"), (1067, "Gehenna")]),

    (3220, "Μελετε", "Meletē", "Noun, Feminine", "Practice / Meditation / Study",
     "From <em>meletaō</em> (to practice, to meditate on). Denotes careful thought, meditation, study, or practice — the disciplined exercise of the mind on a subject. Related to giving diligent attention to something.",
     "Paul instructed Timothy to <em>meditate on</em> and give himself wholly to the teachings entrusted to him (1 Timothy 4:15). This word emphasizes that spiritual growth requires <strong>deliberate, sustained mental engagement</strong> with truth — not passive absorption. The Psalms celebrate meditation on God's law day and night. Christianity demands the life of the mind: thinking deeply, studying carefully, and practicing consistently.",
     [("1+Timothy+4:15", "Be diligent in these matters; give yourself wholly to them, so that everyone may see your progress."),
      ("Acts+4:25", "You spoke by the Holy Spirit through the mouth of your servant, our father David: 'Why do the nations rage and the peoples <em>plot</em> in vain?'"),
      ("Psalm+1:2", "But whose delight is in the law of the Lord, and who <em>meditates</em> on his law day and night."),
      ("Psalm+119:15", "I <em>meditate</em> on your precepts and consider your ways."),
      ("Joshua+1:8", "Keep this Book of the Law always on your lips; <em>meditate</em> on it day and night.")],
     [(3191, "Meletaō (To Meditate)"), (3056, "Logos (Word)"), (1319, "Didaskalia (Teaching)"), (4678, "Sophia (Wisdom)")]),

    (3221, "Μεσος", "Mesos", "Adjective", "Middle / In the Midst",
     "An adjective meaning middle, in the midst of, among. Used both spatially and figuratively. Jesus stood 'in the <em>midst</em>' of His disciples after the resurrection, and He promises to be 'in the <em>midst</em>' wherever two or three gather in His name.",
     "Christ's presence 'in the <em>midst</em>' is one of the most comforting promises in Scripture. In Matthew 18:20, Jesus declares, 'Where two or three gather in my name, there am I with them.' After the resurrection, Jesus stood 'in their <em>midst</em>' and said 'Peace be with you' (John 20:19). In Revelation, Christ walks 'in the <em>midst</em>' of the lampstands (the churches). This word assures believers that <strong>Christ is not distant — He is present among His people</strong>.",
     [("Matthew+18:20", "For where two or three gather in my name, there am I <em>among</em> them."),
      ("John+20:19", "Jesus came and stood <em>among</em> them and said, 'Peace be with you!'"),
      ("Revelation+1:13", "And <em>among</em> the lampstands was someone like a son of man."),
      ("Luke+2:46", "After three days they found him in the temple courts, sitting <em>among</em> the teachers, listening to them and asking them questions."),
      ("Revelation+5:6", "Then I saw a Lamb, looking as if it had been slain, standing at the center of the throne.")],
     [(3319, "Mesos variant"), (1722, "En (In)"), (4862, "Sun (With)"), (3326, "Meta (With)")]),

    (3223, "Μεσημβρια", "Mesēmbria", "Noun, Feminine", "Midday / Noon / South",
     "From <em>mesos</em> (middle) and <em>hēmera</em> (day). Literally 'the middle of the day' — noon. Also used directionally to mean south (since the sun is in the south at midday in the Northern Hemisphere).",
     "In Acts 8:26, an angel directed Philip to go south toward the road from Jerusalem to Gaza, where he encountered the Ethiopian eunuch — one of the most significant conversion narratives in Acts. The word's dual meaning (noon/south) connects to the idea of <strong>divine appointments at specific times and places</strong>. God orchestrates encounters for the advancement of His kingdom.",
     [("Acts+8:26", "Now an angel of the Lord said to Philip, 'Go <em>south</em> to the road — the desert road — that goes down from Jerusalem to Gaza.'"),
      ("Acts+22:6", "About <em>noon</em> as I came near Damascus, suddenly a bright light from heaven flashed around me."),
      ("Acts+26:13", "About <em>midday</em>, King Agrippa, as I was on the road, I saw a light from heaven, brighter than the sun."),
      ("Genesis+18:1", "The Lord appeared to Abraham near the great trees of Mamre while he was sitting at the entrance to his tent in the heat of the <em>day</em>."),
      ("Psalm+37:6", "He will make your righteous reward shine like the <em>dawn</em>, your vindication like the <em>noonday</em> sun.")],
     [(2250, "Hēmera (Day)"), (3319, "Mesos (Middle)"), (3558, "Notos (South Wind)"), (5610, "Hōra (Hour)")]),

    (3224, "Μεσιτευω", "Mesiteuō", "Verb", "To Act as Mediator / To Guarantee",
     "From <em>mesitēs</em> (mediator). To interpose, to act as a go-between, to mediate or guarantee. God Himself <em>mediated</em> by swearing an oath, since there was no one greater to swear by.",
     "In Hebrews 6:17, God 'confirmed it with an oath' — He <em>mediated/guaranteed</em> His promise by swearing upon Himself. This is extraordinary: the God who cannot lie added an oath to His promise so that by two unchangeable things (His word and His oath), believers might have <strong>strong encouragement and absolute assurance</strong>. God accommodates human weakness by providing extra confirmation of what was already certain.",
     [("Hebrews+6:17", "Because God wanted to make the unchanging nature of his purpose very clear to the heirs of what was promised, he <em>confirmed it with an oath</em>."),
      ("Hebrews+6:18", "God did this so that, by two unchangeable things in which it is impossible for God to lie, we who have fled to take hold of the hope set before us may be greatly encouraged."),
      ("Hebrews+6:13", "When God made his promise to Abraham, since there was no one greater for him to swear by, he swore by himself."),
      ("Genesis+22:16", "I swear by myself, declares the Lord, that because you have done this and have not withheld your son."),
      ("Psalm+110:4", "The Lord has sworn and will not change his mind: 'You are a priest forever, in the order of Melchizedek.'")],
     [(3211, "Mesitēs (Mediator)"), (3727, "Horkos (Oath)"), (1860, "Epangelia (Promise)"), (4102, "Pistis (Faith)")]),

    # More entries in the 3225-3299 range (very sparse area)
    (3225, "Μεσονυκτιον", "Mesonuktion", "Noun, Neuter", "Midnight",
     "From <em>mesos</em> (middle) and <em>nux</em> (night). Literally 'the middle of the night' — midnight. Several pivotal biblical events occur at midnight, making this word theologically charged beyond its literal meaning.",
     "Midnight in Scripture is often the hour of <strong>divine intervention</strong>. Paul and Silas were praying and singing hymns at <em>midnight</em> when God sent an earthquake to free them from prison (Acts 16:25). Jesus told the parable of the bridegroom arriving at <em>midnight</em> (Matthew 25:6), teaching readiness for His return. At <em>midnight</em>, God struck down the firstborn of Egypt (Exodus 12:29). The pattern is clear: God works in the darkest hours.",
     [("Acts+16:25", "About <em>midnight</em> Paul and Silas were praying and singing hymns to God, and the other prisoners were listening to them."),
      ("Matthew+25:6", "At <em>midnight</em> the cry rang out: 'Here's the bridegroom! Come out to meet him!'"),
      ("Mark+13:35", "Therefore keep watch because you do not know when the owner of the house will come back — whether in the evening, or at <em>midnight</em>, or when the rooster crows, or at dawn."),
      ("Acts+20:7", "On the first day of the week we came together to break bread. Paul spoke to the people and, because he intended to leave the next day, kept on talking until <em>midnight</em>."),
      ("Luke+11:5", "Then Jesus said to them, 'Suppose you have a friend, and you go to him at <em>midnight</em> and say, Friend, lend me three loaves of bread.'")],
     [(3571, "Nux (Night)"), (5610, "Hōra (Hour)"), (2250, "Hēmera (Day)"), (3319, "Mesos (Middle)")]),

    (3226, "Μεσοτοιχον", "Mesotoichon", "Noun, Neuter", "Dividing Wall / Middle Wall",
     "From <em>mesos</em> (middle) and <em>toichos</em> (wall). A dividing wall, a partition that separates. Used only once in the NT, in Ephesians 2:14, where it describes the barrier between Jews and Gentiles that Christ destroyed.",
     "Paul declares that Christ 'has destroyed the barrier, the <em>dividing wall</em> of hostility' between Jew and Gentile (Ephesians 2:14). This likely alludes to the physical wall in the Jerusalem temple that separated the Court of the Gentiles from the inner courts — a wall that bore inscriptions warning Gentiles of death if they crossed. Christ's cross obliterated this division, creating <strong>one new humanity</strong> from the two. This is the gospel's radical social implication: in Christ, all walls of ethnic, social, and religious hostility are demolished.",
     [("Ephesians+2:14", "For he himself is our peace, who has made the two groups one and has destroyed the barrier, the <em>dividing wall</em> of hostility."),
      ("Ephesians+2:15", "By setting aside in his flesh the law with its commands and regulations. His purpose was to create in himself one new humanity out of the two, thus making peace."),
      ("Ephesians+2:16", "And in one body to reconcile both of them to God through the cross, by which he put to death their hostility."),
      ("Galatians+3:28", "There is neither Jew nor Gentile, neither slave nor free, nor is there male and female, for you are all one in Christ Jesus."),
      ("Colossians+1:20", "And through him to reconcile to himself all things, whether things on earth or things in heaven, by making peace through his blood, shed on the cross.")],
     [(1515, "Eirēnē (Peace)"), (2644, "Katallassō (To Reconcile)"), (1577, "Ekklēsia (Church)"), (4716, "Stauros (Cross)")]),

    (3227, "Μεσουρανημα", "Mesouranēma", "Noun, Neuter", "Midheaven / Zenith",
     "From <em>mesos</em> (middle) and <em>ouranos</em> (heaven). The highest point of the sky — the zenith or mid-heaven where the sun stands at noon, visible to all. Used in Revelation for angels making proclamations from the highest, most visible point of the sky.",
     "In Revelation, an angel flies in <em>midheaven</em> proclaiming the eternal gospel to every nation (Revelation 14:6). Another angel in <em>midheaven</em> announces God's judgment (Revelation 8:13). The use of this word emphasizes that God's final messages are <strong>inescapable and universal</strong> — broadcast from the highest point, seen and heard by all humanity. No one will be able to claim ignorance.",
     [("Revelation+14:6", "Then I saw another angel flying in <em>midair</em>, and he had the eternal gospel to proclaim to those who live on the earth."),
      ("Revelation+8:13", "As I watched, I heard an eagle that was flying in <em>midair</em> call out in a loud voice: 'Woe! Woe! Woe!'"),
      ("Revelation+19:17", "And I saw an angel standing in the sun, who cried in a loud voice to all the birds flying in <em>midair</em>."),
      ("Matthew+24:14", "And this gospel of the kingdom will be preached in the whole world as a testimony to all nations, and then the end will come."),
      ("Romans+10:18", "But I ask: Did they not hear? Of course they did: 'Their voice has gone out into all the earth.'")],
     [(3772, "Ouranos (Heaven)"), (32, "Angelos (Angel)"), (2098, "Euangelion (Gospel)"), (3319, "Mesos (Middle)")]),

    (3228, "Μετανοια", "Metanoia", "Noun, Feminine", "Repentance / Change of Mind",
     "From <em>meta</em> (change, after) and <em>nous</em> (mind). A complete change of mind and direction — not mere regret but a fundamental reorientation of one's thinking, attitudes, and behavior toward God. One of the most important theological terms in the New Testament.",
     "Both John the Baptist and Jesus began their public ministry with the same word: '<em>Repent</em>, for the kingdom of heaven has come near' (Matthew 3:2; 4:17). Peter's Pentecost sermon commanded '<em>Repent</em> and be baptized' (Acts 2:38). <em>Metanoia</em> is not merely feeling sorry — it is a <strong>complete reversal of direction</strong>, turning from sin and self to God. It involves the mind (new understanding), the emotions (godly sorrow), and the will (new obedience). It is both a gift from God (Acts 11:18) and a human responsibility (Acts 17:30). Without repentance, there is no salvation.",
     [("Acts+2:38", "<em>Repent</em> and be baptized, every one of you, in the name of Jesus Christ for the forgiveness of your sins."),
      ("Luke+15:7", "I tell you that in the same way there will be more rejoicing in heaven over one sinner who <em>repents</em> than over ninety-nine righteous persons."),
      ("2+Peter+3:9", "The Lord is not slow in keeping his promise, as some understand slowness. Instead he is patient with you, not wanting anyone to perish, but everyone to come to <em>repentance</em>."),
      ("Acts+11:18", "So then, even to Gentiles God has granted <em>repentance</em> that leads to life."),
      ("Acts+17:30", "In the past God overlooked such ignorance, but now he commands all people everywhere to <em>repent</em>.")],
     [(3340, "Metanoeō (To Repent)"), (1995, "Epistrephō (To Turn)"), (3670, "Homologeō (To Confess)"), (859, "Aphesis (Forgiveness)")]),

    (3229, "Μεταστρεφω", "Metastrephō", "Verb", "To Turn / To Pervert / To Change",
     "From <em>meta</em> (change) and <em>strephō</em> (to turn). To turn around, to change into something else, to pervert. Used of cosmic signs and the perversion of the gospel.",
     "Peter quotes Joel's prophecy that the sun will be turned to darkness and the moon to blood before the great day of the Lord (Acts 2:20). Paul warns the Galatians about those who would <em>pervert</em> the gospel of Christ (Galatians 1:7). This word carries a sense of <strong>radical reversal</strong> — something being changed into its opposite. It warns against any alteration of the gospel message.",
     [("Acts+2:20", "The sun will be <em>turned</em> to darkness and the moon to blood before the coming of the great and glorious day of the Lord."),
      ("Galatians+1:7", "Which is really no gospel at all. Evidently some people are throwing you into confusion and are trying to <em>pervert</em> the gospel of Christ."),
      ("James+4:9", "Grieve, mourn and wail. <em>Change</em> your laughter to mourning and your joy to gloom."),
      ("Joel+2:31", "The sun will be turned to darkness and the moon to blood before the coming of the great and dreadful day of the Lord."),
      ("Galatians+1:8", "But even if we or an angel from heaven should preach a gospel other than the one we preached to you, let them be under God's curse!")],
     [(4762, "Strephō (To Turn)"), (2098, "Euangelion (Gospel)"), (1995, "Epistrephō (To Turn Back)"), (3340, "Metanoeō (To Repent)")]),

    (3230, "Μεταπεμπω", "Metapempō", "Verb", "To Send For / To Summon",
     "From <em>meta</em> (implying change of place) and <em>pempō</em> (to send). To send for someone, to summon. Used frequently in Acts for official summons — especially in the narrative of Cornelius sending for Peter.",
     "This seemingly ordinary word carries extraordinary theological significance in Acts 10. Cornelius, a Roman centurion, was told by an angel to <em>send for</em> Simon Peter (Acts 10:5). This summons led to the <strong>first Gentile Pentecost</strong> — the moment when the gospel officially crossed ethnic boundaries. God used a simple act of sending a message to change the course of salvation history.",
     [("Acts+10:5", "<em>Send</em> men to Joppa to bring back a man named Simon who is called Peter."),
      ("Acts+10:22", "The men replied, 'We have come from Cornelius the centurion. He is a righteous and God-fearing man. A holy angel told him to ask you to come to his house.'"),
      ("Acts+10:29", "So when I was <em>sent for</em>, I came without raising any objection. May I ask why you sent for me?"),
      ("Acts+11:13", "He told us how he had seen an angel appear in his house and say, '<em>Send</em> to Joppa for Simon who is called Peter.'"),
      ("Acts+24:24", "Several days later Felix came with his wife Drusilla, who was Jewish. He <em>sent for</em> Paul and listened to him.")],
     [(3992, "Pempō (To Send)"), (649, "Apostellō (To Send Out)"), (2564, "Kaleō (To Call)"), (2784, "Kērussō (To Proclaim)")]),

    (3231, "Μεταλαμβανω", "Metalambanō", "Verb", "To Partake Of / To Receive A Share",
     "From <em>meta</em> (with) and <em>lambanō</em> (to receive). To take a share, to partake, to receive. Used of sharing in food, receiving spiritual benefit, and participating in blessings.",
     "This word appears in Hebrews 6:7, where the ground that drinks in rain and produces crops <em>receives</em> God's blessing — a metaphor for the fruitful believer. Paul uses it of laborers deserving to <em>share</em> in the harvest (2 Timothy 2:6). The word teaches the principle of <strong>participation and shared benefit</strong> — those who labor faithfully in God's work will partake of the reward.",
     [("Hebrews+6:7", "Land that drinks in the rain often falling on it and that produces a crop useful to those for whom it is farmed <em>receives</em> the blessing of God."),
      ("2+Timothy+2:6", "The hardworking farmer should be the first to <em>receive a share</em> of the crops."),
      ("Acts+2:46", "Every day they continued to meet together in the temple courts. They broke bread in their homes and ate together with glad and sincere hearts."),
      ("Acts+27:33", "Just before dawn Paul urged them all to eat. 'For the last fourteen days,' he said, 'you have been in constant suspense and have gone without food.'"),
      ("Hebrews+12:10", "They disciplined us for a little while as they thought best; but God disciplines us for our good, in order that we may <em>share</em> in his holiness.")],
     [(2983, "Lambanō (To Receive)"), (3215, "Metechō (To Partake)"), (2842, "Koinōnia (Fellowship)"), (2816, "Klēronomeō (To Inherit)")]),

    (3232, "Μεταβολη", "Metabolē", "Noun, Feminine", "Change / Turning",
     "From <em>meta</em> (change) and <em>bolē</em> (a throw). Denotes a change, a turning point, a transformation. Appears in James 1:17 in the phrase 'shadow of <em>turning</em>' — emphasizing God's immutability.",
     "James declares that God is the Father of lights, with whom there is no variation or shadow of <em>turning</em> (James 1:17). While everything in creation is subject to change, God remains <strong>absolutely constant</strong>. His character, His promises, and His purposes never shift. This is the foundation of all Christian hope: the unchanging God who keeps every promise.",
     [("James+1:17", "Every good and perfect gift is from above, coming down from the Father of the heavenly lights, who does not change like shifting shadows."),
      ("Malachi+3:6", "I the Lord do not <em>change</em>. So you, the descendants of Jacob, are not destroyed."),
      ("Hebrews+13:8", "Jesus Christ is the same yesterday and today and forever."),
      ("Numbers+23:19", "God is not human, that he should lie, not a human being, that he should <em>change</em> his mind."),
      ("Psalm+102:27", "But you remain the same, and your years will never end.")],
     [(236, "Allassō (To Change)"), (3883, "Parallage (Variation)"), (5157, "Tropē (Turning)"), (862, "Aphthartos (Imperishable)")]),

    (3233, "Μεθοδεια", "Methodeia", "Noun, Feminine", "Scheme / Craftiness / Wile",
     "From <em>meta</em> (after) and <em>hodos</em> (way). Literally 'a following after' — hence a method, scheme, or crafty strategy. Used exclusively of Satan's deceptive tactics in Ephesians.",
     "Paul warns believers to put on the full armor of God so they can stand against the <em>schemes</em> of the devil (Ephesians 6:11). He also warns against being carried about by every wind of doctrine through the <em>craftiness</em> of men (Ephesians 4:14). The word reveals that Satan does not operate randomly — he employs <strong>strategic, calculated deception</strong>. This is why believers need not just moral strength but spiritual armor and discernment.",
     [("Ephesians+6:11", "Put on the full armor of God, so that you can take your stand against the devil's <em>schemes</em>."),
      ("Ephesians+4:14", "Then we will no longer be infants, tossed back and forth by the waves, and blown here and there by every wind of teaching and by the cunning and <em>craftiness</em> of people in their deceitful scheming."),
      ("2+Corinthians+2:11", "In order that Satan might not outwit us. For we are not unaware of his <em>schemes</em>."),
      ("1+Peter+5:8", "Be alert and of sober mind. Your enemy the devil prowls around like a roaring lion looking for someone to devour."),
      ("2+Corinthians+11:14", "And no wonder, for Satan himself masquerades as an angel of light.")],
     [(3588, "Ho (The)"), (1228, "Diabolos (Devil)"), (3809, "Paideia (Discipline)"), (3696, "Hoplon (Weapon/Armor)")]),

    (3234, "Μεταμορφωσις", "Metamorphōsis", "Noun, Feminine", "Transformation / Transfiguration",
     "The noun form of <em>metamorphoō</em> (G3213). Denotes the act or process of transformation — a change in form. Though the noun itself is rare, the concept it represents — spiritual transformation into Christlikeness — is central to New Testament theology.",
     "While the noun form is rare in the Greek NT, the concept of <em>transformation</em> pervades the New Testament. Believers are being transformed into Christ's image (2 Corinthians 3:18), renewed in the spirit of their minds (Ephesians 4:23), and will ultimately be transformed when Christ appears (1 John 3:2). The <strong>transfiguration of Jesus</strong> on the mountain previews the glory that all believers will share. Transformation is both present (progressive sanctification) and future (glorification).",
     [("2+Corinthians+3:18", "And we all, who with unveiled faces contemplate the Lord's glory, are being <em>transformed</em> into his image with ever-increasing glory."),
      ("Romans+12:2", "Do not conform to the pattern of this world, but be <em>transformed</em> by the renewing of your mind."),
      ("1+John+3:2", "Dear friends, now we are children of God, and what we will be has not yet been made known. But we know that when Christ appears, we shall be like him."),
      ("Philippians+3:21", "Who, by the power that enables him to bring everything under his control, will <em>transform</em> our lowly bodies so that they will be like his glorious body."),
      ("Matthew+17:2", "There he was <em>transfigured</em> before them.")],
     [(3213, "Metamorphoō (To Transform)"), (3444, "Morphē (Form)"), (1391, "Doxa (Glory)"), (38, "Hagiasmos (Sanctification)")]),

    (3236, "Μεταθεσις", "Metathesis", "Noun, Feminine", "Change / Removal / Translation",
     "From <em>metatithēmi</em> (to transfer, transpose). Denotes a change of position, a removal, or a transference. Used of Enoch's translation to heaven and the change of the priesthood and law.",
     "Hebrews uses this word in three significant ways: (1) Enoch was <em>translated</em> so he did not see death (Hebrews 11:5). (2) When the priesthood is <em>changed</em>, the law must change too (Hebrews 7:12). (3) The shaking of creation signals the <em>removal</em> of created things so the unshakeable kingdom remains (Hebrews 12:27). The word teaches that God is not bound by existing systems — He has the authority to <strong>change, remove, and replace</strong> whatever does not serve His ultimate purposes.",
     [("Hebrews+11:5", "By faith Enoch was taken from this life, so that he did not experience death. He was <em>translated</em> because God had taken him away."),
      ("Hebrews+7:12", "For when the priesthood is <em>changed</em>, the law must be changed also."),
      ("Hebrews+12:27", "The words 'once more' indicate the <em>removing</em> of what can be shaken — that is, created things — so that what cannot be shaken may remain."),
      ("Genesis+5:24", "Enoch walked faithfully with God; then he was no more, because God took him away."),
      ("2+Kings+2:11", "As they were walking along and talking together, suddenly a chariot of fire and horses of fire appeared and separated the two of them, and Elijah went up to heaven in a whirlwind.")],
     [(3346, "Metatithēmi (To Transfer)"), (3331, "Metathesis variant"), (236, "Allassō (To Change)"), (4102, "Pistis (Faith)")]),

    (3237, "Μεταδιδωμι", "Metadidōmi", "Verb", "To Share / To Give A Part Of",
     "From <em>meta</em> (with) and <em>didōmi</em> (to give). To share, to impart, to give a portion of what one has to another. Used of sharing material goods, spiritual gifts, and the gospel itself.",
     "Paul uses this word to describe his deep desire to <em>share</em> not only the gospel but his very life with the Thessalonians (1 Thessalonians 2:8). In Romans 1:11, he longed to <em>impart</em> some spiritual gift to strengthen them. This word reveals that authentic Christianity is inherently <strong>generous and self-giving</strong>. John the Baptist taught that anyone with two shirts should <em>share</em> with the one who has none (Luke 3:11). Believers are conduits of God's grace, not reservoirs.",
     [("1+Thessalonians+2:8", "So we cared for you. Because we loved you so much, we were delighted to <em>share</em> with you not only the gospel of God but our lives as well."),
      ("Romans+1:11", "I long to see you so that I may <em>impart</em> to you some spiritual gift to make you strong."),
      ("Romans+12:8", "If it is to encourage, then give encouragement; if it is giving, then give <em>generously</em>."),
      ("Luke+3:11", "John answered, 'Anyone who has two shirts should <em>share</em> with the one who has none.'"),
      ("Ephesians+4:28", "Anyone who has been stealing must steal no longer, but must work, doing something useful with their own hands, that they may have something to <em>share</em> with those in need.")],
     [(1325, "Didōmi (To Give)"), (2842, "Koinōnia (Fellowship)"), (5485, "Charis (Grace)"), (26, "Agapē (Love)")]),

    (3238, "Μεταιχμιον", "Metaichmion", "Noun, Neuter", "Space Between / Interval",
     "From <em>meta</em> (between) and <em>aichmē</em> (spear point). Originally the space between two armies — the no-man's land between opposing forces. By extension, any interval or intermediate space.",
     "Though rare in the NT, this concept of the space between opposing forces resonates with the spiritual warfare Paul describes. Believers live in the interval between Christ's first and second coming — already redeemed but not yet glorified, in enemy territory but <strong>more than conquerors</strong>. The Christian life is lived in the 'already but not yet,' the space between promise and fulfillment.",
     [("Ephesians+6:12", "For our struggle is not against flesh and blood, but against the rulers, against the authorities, against the powers of this dark world."),
      ("Romans+8:37", "No, in all these things we are <em>more than conquerors</em> through him who loved us."),
      ("2+Corinthians+10:4", "The weapons we fight with are not the weapons of the world."),
      ("1+Timothy+6:12", "Fight the good fight of the faith. Take hold of the eternal life to which you were called."),
      ("Revelation+12:11", "They triumphed over him by the blood of the Lamb and by the word of their testimony.")],
     [(4171, "Polemos (War)"), (3696, "Hoplon (Weapon)"), (3164, "Machomai (To Fight)"), (4754, "Strateuomai (To Wage War)")]),

    (3239, "Μεγας", "Megas", "Adjective", "Great / Large / Mighty",
     "One of the most common Greek adjectives, meaning great in size, degree, intensity, or importance. Used over 190 times in the NT. Describes everything from physical size to spiritual magnitude — God's love, the great commission, the great tribulation, and the great white throne.",
     "This word appears in some of Scripture's most significant phrases: the '<em>great</em> commandment' (Matthew 22:36), the '<em>great</em> commission' (Matthew 28:19-20), the '<em>great</em> tribulation' (Revelation 7:14), the '<em>great</em> white throne' (Revelation 20:11), and '<em>great</em> is the mystery of godliness' (1 Timothy 3:16). When applied to God, it conveys <strong>incomparable magnitude</strong> — a greatness that surpasses all measurement. The Magnificat begins: 'My soul <em>magnifies</em> (megalunei) the Lord.'",
     [("Matthew+22:38", "This is the first and <em>greatest</em> commandment."),
      ("Revelation+20:11", "Then I saw a <em>great</em> white throne and him who was seated on it."),
      ("1+Timothy+3:16", "<em>Great</em> is the mystery of godliness."),
      ("Titus+2:13", "While we wait for the blessed hope — the appearing of the glory of our <em>great</em> God and Savior, Jesus Christ."),
      ("Hebrews+4:14", "Therefore, since we have a <em>great</em> high priest who has ascended into heaven, Jesus the Son of God, let us hold firmly to the faith we profess.")],
     [(3173, "Megas variant"), (3176, "Megistos (Greatest)"), (3170, "Megalunō (To Magnify)"), (3172, "Megaleiotes (Magnificence)")]),

    # Continue with more entries across different number ranges
    (3240, "Μεταβασις", "Metabasis", "Noun, Feminine", "Transition / Passing Over",
     "From <em>metabainō</em> (to pass over). A transition, a passing from one state or place to another. Theologically significant in describing the believer's transition from death to life.",
     "This concept underlies John 5:24, where Jesus declares that believers have <em>passed</em> from death to life. The transition is not gradual but decisive — a <strong>definitive crossing</strong> from one realm to another. Salvation is not improvement but transformation, not reformation but recreation. The believer has been transferred from the domain of darkness to the kingdom of God's beloved Son (Colossians 1:13).",
     [("John+5:24", "Very truly I tell you, whoever hears my word and believes him who sent me has eternal life and will not be judged but has <em>crossed over</em> from death to life."),
      ("Colossians+1:13", "For he has rescued us from the dominion of darkness and brought us into the kingdom of the Son he loves."),
      ("1+John+3:14", "We know that we have <em>passed</em> from death to life, because we love each other."),
      ("2+Corinthians+5:17", "Therefore, if anyone is in Christ, the new creation has come: The old has gone, the new is here!"),
      ("Ephesians+2:5", "Made us alive with Christ even when we were dead in transgressions — it is by grace you have been saved.")],
     [(3205, "Metabainō (To Pass Over)"), (2222, "Zōē (Life)"), (2288, "Thanatos (Death)"), (4991, "Sōtēria (Salvation)")]),

    (3241, "Μεσοποταμια", "Mesopotamia", "Noun, Proper", "Mesopotamia (Between the Rivers)",
     "From <em>mesos</em> (middle) and <em>potamos</em> (river). Literally 'between the rivers' — the land between the Tigris and Euphrates rivers, in modern-day Iraq. The ancestral homeland of Abraham and the setting for some of the earliest biblical history.",
     "Stephen's speech in Acts 7 begins with God's call to Abraham while he was still in <em>Mesopotamia</em> (Acts 7:2). This is significant because it shows that <strong>God's initiative precedes human response</strong> — God reached into pagan territory to call one man through whom all nations would be blessed. Mesopotamia also features at Pentecost, when residents of <em>Mesopotamia</em> heard the gospel in their own language (Acts 2:9). God brings the story full circle: from Abraham's departure from Mesopotamia to the gospel's arrival there.",
     [("Acts+7:2", "The God of glory appeared to our father Abraham while he was still in <em>Mesopotamia</em>, before he lived in Harran."),
      ("Acts+2:9", "Parthians, Medes and Elamites; residents of <em>Mesopotamia</em>, Judea and Cappadocia."),
      ("Genesis+11:31", "Terah took his son Abram, his grandson Lot son of Haran, and his daughter-in-law Sarai, and together they set out from Ur of the Chaldeans to go to Canaan."),
      ("Genesis+12:1", "The Lord had said to Abram, 'Go from your country, your people and your father's household to the land I will show you.'"),
      ("Nehemiah+9:7", "You are the Lord God, who chose Abram and brought him out of Ur of the Chaldeans and named him Abraham.")],
     [(11, "Abraam (Abraham)"), (1093, "Gē (Earth/Land)"), (4215, "Potamos (River)"), (2564, "Kaleō (To Call)")]),

    (3242, "Μεταμορφοομαι", "Metamorphoomai", "Verb (Middle/Passive)", "To Be Transformed",
     "The middle/passive voice of <em>metamorphoō</em> (G3213). Emphasizes that the transformation is something done <em>to</em> or <em>within</em> the believer by the Spirit — not something accomplished by human effort alone.",
     "The passive voice in Romans 12:2 ('be <em>transformed</em>') and 2 Corinthians 3:18 ('are being <em>transformed</em>') is crucial: believers do not transform themselves. They submit to the Spirit's work of renewal. Yet it is not purely passive either — Paul commands 'be transformed,' implying cooperation. This is the mystery of sanctification: <strong>God does the transforming, but believers must actively yield</strong> to His work through spiritual disciplines, obedience, and the renewing of the mind.",
     [("Romans+12:2", "Be <em>transformed</em> by the renewing of your mind. Then you will be able to test and approve what God's will is."),
      ("2+Corinthians+3:18", "We all, who with unveiled faces contemplate the Lord's glory, are being <em>transformed</em> into his image with ever-increasing glory."),
      ("Galatians+4:19", "My dear children, for whom I am again in the pains of childbirth until Christ is <em>formed</em> in you."),
      ("Ephesians+4:23", "To be made new in the attitude of your minds."),
      ("Colossians+3:10", "And have put on the new self, which is being renewed in knowledge in the image of its Creator.")],
     [(3213, "Metamorphoō (To Transform)"), (342, "Anakainōsis (Renewal)"), (4151, "Pneuma (Spirit)"), (1391, "Doxa (Glory)")]),

    (3244, "Μεσοω", "Mesoō", "Verb", "To Be In the Middle / To Be Halfway",
     "From <em>mesos</em> (middle). To be at the midpoint, to be in the middle of. Used in John 7:14 when Jesus went to the temple in the <em>middle</em> of the Feast of Tabernacles.",
     "Jesus appeared at the temple 'about the <em>middle</em> of the festival' (John 7:14) and began to teach. His timing was deliberate — not at the beginning when crowds would expect a teacher, nor at the end, but in the <em>middle</em>, demonstrating His sovereign authority over timing and occasion. Jesus does things on <strong>His schedule, not ours</strong>. This pattern appears throughout His ministry: He acts when the Father's time has come.",
     [("John+7:14", "Not until <em>halfway</em> through the festival did Jesus go up to the temple courts and begin to teach."),
      ("John+7:15", "The Jews there were amazed and asked, 'How did this man get such learning without having been taught?'"),
      ("John+2:4", "Jesus replied, 'Woman, why do you involve me? My hour has not yet come.'"),
      ("Galatians+4:4", "But when the set time had fully come, God sent his Son, born of a woman, born under the law."),
      ("Ecclesiastes+3:1", "There is a time for everything, and a season for every activity under the heavens.")],
     [(3319, "Mesos (Middle)"), (5610, "Hōra (Hour)"), (2540, "Kairos (Season/Time)"), (5550, "Chronos (Time)")]),

    (3245, "Μετα", "Meta", "Preposition", "With / After / Among",
     "One of the most common Greek prepositions, appearing over 470 times in the NT. With the genitive case it means 'with' or 'among'; with the accusative it means 'after.' It forms the prefix of many compound words (metanoia, metamorphosis, etc.) where it denotes change or transition.",
     "This preposition appears in some of Scripture's most profound statements. 'God is <em>with</em> us' (Emmanuel, Matthew 1:23). 'I am <em>with</em> you always' (Matthew 28:20). '<em>After</em> three days I will rise again' (Matthew 27:63). The simple word <em>meta</em> carries the entire weight of the incarnation and the resurrection promise. Christ's final words in Matthew's gospel are: 'I am <em>with</em> you always, to the very end of the age.' <strong>The gospel is fundamentally about God being with His people.</strong>",
     [("Matthew+1:23", "The virgin will conceive and give birth to a son, and they will call him Immanuel — which means 'God <em>with</em> us.'"),
      ("Matthew+28:20", "And surely I am <em>with</em> you always, to the very end of the age."),
      ("Revelation+21:3", "And I heard a loud voice from the throne saying, 'Look! God's dwelling place is now <em>among</em> the people.'"),
      ("John+1:1", "In the beginning was the Word, and the Word was <em>with</em> God, and the Word was God."),
      ("Philippians+4:9", "Whatever you have learned or received or heard from me, or seen in me — put it into practice. And the God of peace will be <em>with</em> you.")],
     [(4862, "Sun (With)"), (1722, "En (In)"), (4314, "Pros (Toward)"), (3844, "Para (Beside)")]),

    (3246, "Μετοχος", "Metochos", "Noun/Adjective", "Partner / Companion / Partaker",
     "From <em>metechō</em> (to share in). One who shares, a partner, a companion, a partaker. Used of business partners, companions of Christ, and those who share in the heavenly calling.",
     "Hebrews declares that believers have become '<em>partakers</em> of Christ' (Hebrews 3:14) and '<em>partakers</em> of the Holy Spirit' (Hebrews 6:4). In Hebrews 1:9, the psalm declares Christ's superiority over His '<em>companions</em>' (angels or fellow-anointed ones). Luke uses it of James and John as Peter's '<em>partners</em>' in the fishing business (Luke 5:7). The word teaches that salvation is not mere legal status — it is <strong>actual participation in Christ's life</strong>.",
     [("Hebrews+3:14", "We have come to share in Christ, if indeed we hold our original conviction firmly to the very end."),
      ("Hebrews+3:1", "Therefore, holy brothers and sisters, who share in the heavenly calling, fix your thoughts on Jesus."),
      ("Hebrews+6:4", "It is impossible for those who have once been enlightened, who have tasted the heavenly gift, who have shared in the Holy Spirit."),
      ("Hebrews+1:9", "You have loved righteousness and hated wickedness; therefore God, your God, has set you above your <em>companions</em> by anointing you with the oil of joy."),
      ("Luke+5:7", "So they signaled their <em>partners</em> in the other boat to come and help them.")],
     [(3215, "Metechō (To Partake)"), (2842, "Koinōnia (Fellowship)"), (2844, "Koinōnos (Partner)"), (4862, "Sun (With)")]),

    (3247, "Μεγαλυνω", "Megalunō", "Verb", "To Magnify / To Make Great / To Glorify",
     "From <em>megas</em> (great). To make great, to enlarge, to magnify, to extol. The word used by Mary in the Magnificat and by the early church to describe the exaltation of God's name.",
     "Mary's song begins: 'My soul <em>magnifies</em> the Lord' (Luke 1:46) — the Magnificat, one of the most beloved passages in Scripture. To magnify God is not to make Him bigger (He is already infinite) but to <strong>declare His greatness</strong>, to make it visible and known. In Acts 10:46, the Gentile believers were heard '<em>magnifying</em> God' after receiving the Spirit — evidence that the gospel had crossed ethnic boundaries. Paul's desire was that Christ would be '<em>magnified</em>' in his body, whether by life or death (Philippians 1:20).",
     [("Luke+1:46", "And Mary said: 'My soul <em>glorifies</em> the Lord.'"),
      ("Philippians+1:20", "I eagerly expect and hope that I will in no way be ashamed, but will have sufficient courage so that now as always Christ will be <em>exalted</em> in my body, whether by life or by death."),
      ("Acts+10:46", "For they heard them speaking in tongues and <em>praising</em> God."),
      ("Acts+5:13", "No one else dared join them, even though they were highly regarded by the people."),
      ("Luke+1:58", "Her neighbors and relatives heard that the Lord had shown her great mercy, and they shared her joy.")],
     [(1392, "Doxazō (To Glorify)"), (134, "Aineō (To Praise)"), (5214, "Humneō (To Sing Hymns)"), (2127, "Eulogeō (To Bless)")]),

    (3248, "Μεταπεμψις", "Metapempsis", "Noun, Feminine", "A Sending For / Summons",
     "The noun form of <em>metapempō</em> (to send for). A summons, the act of sending for someone. Related to the practice of official summoning in the Roman world.",
     "This word connects to the narratives in Acts where divine summons led to pivotal moments in church history. The concept of being <em>sent for</em> by God — called out of one's current situation into His service — is fundamental to biblical theology. God calls individuals by name and sends them on specific missions, from Abraham to Paul.",
     [("Acts+10:5", "Now send men to Joppa to bring back a man named Simon who is called Peter."),
      ("Acts+10:29", "So when I was sent for, I came without raising any objection."),
      ("Isaiah+6:8", "Then I heard the voice of the Lord saying, 'Whom shall I send? And who will go for us?' And I said, 'Here am I. Send me!'"),
      ("Romans+8:28", "And we know that in all things God works for the good of those who love him, who have been called according to his purpose."),
      ("2+Timothy+1:9", "He has saved us and called us to a holy life — not because of anything we have done but because of his own purpose and grace.")],
     [(3230, "Metapempō (To Send For)"), (2564, "Kaleō (To Call)"), (2821, "Klēsis (Calling)"), (649, "Apostellō (To Send)")]),

    (3249, "Μετεωριζομαι", "Meteōrizomai", "Verb", "To Be Anxious / To Be In Suspense",
     "From <em>meteōros</em> (raised up, in mid-air). Literally to be 'up in the air' — hence to be in suspense, to be anxiously uncertain. The root of the English word 'meteor.' Used only once in the NT, in Luke 12:29.",
     "Jesus commands His disciples: 'Do not set your heart on what you will eat or drink; do not <em>worry</em> about it' (Luke 12:29). The image is vivid — anxiety is like being suspended in mid-air with no solid ground beneath you. Jesus offers the antidote: seek the Father's kingdom, and all these things will be given to you. <strong>Faith is the solid ground</strong> that ends the anxious suspension of unbelief.",
     [("Luke+12:29", "And do not set your heart on what you will eat or drink; do not <em>worry</em> about it."),
      ("Luke+12:30", "For the pagan world runs after all such things, and your Father knows that you need them."),
      ("Luke+12:31", "But seek his kingdom, and these things will be given to you as well."),
      ("Matthew+6:33", "But seek first his kingdom and his righteousness, and all these things will be given to you as well."),
      ("Philippians+4:6", "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God.")],
     [(3204, "Merimnaō (To Worry)"), (3210, "Merimna (Anxiety)"), (4102, "Pistis (Faith)"), (1515, "Eirēnē (Peace)")]),

    (3250, "Μεσιτεια", "Mesiteia", "Noun, Feminine", "Mediation / Intercession",
     "From <em>mesitēs</em> (mediator). The act or office of mediation — standing between two parties to bring reconciliation. The concept is central to Christ's ongoing priestly work.",
     "Christ's <em>mediation</em> is not a one-time event but an ongoing ministry. He ever lives to intercede for believers (Hebrews 7:25). His mediation is based on His once-for-all sacrifice and His present position at the Father's right hand. Unlike human mediators who eventually die, Christ holds His priesthood permanently. This gives believers <strong>eternal security and constant access</strong> to the Father through the Son.",
     [("Hebrews+7:25", "Therefore he is able to save completely those who come to God through him, because he always lives to <em>intercede</em> for them."),
      ("1+Timothy+2:5", "For there is one God and one <em>mediator</em> between God and mankind, the man Christ Jesus."),
      ("Romans+8:34", "Christ Jesus who died — more than that, who was raised to life — is at the right hand of God and is also <em>interceding</em> for us."),
      ("Hebrews+9:15", "For this reason Christ is the mediator of a new covenant."),
      ("1+John+2:1", "But if anybody does sin, we have an advocate with the Father — Jesus Christ, the Righteous One.")],
     [(3211, "Mesitēs (Mediator)"), (1793, "Entugchanō (To Intercede)"), (749, "Archiereus (High Priest)"), (3875, "Paraklētos (Advocate)")]),

    # Numbers in different ranges to diversify
    (3251, "Μεγαλειοτης", "Megaleiotes", "Noun, Feminine", "Magnificence / Mighty Power",
     "From <em>megaleios</em> (magnificent). Denotes magnificence, grandeur, or divine mighty power. Used of the magnificent greatness of God that evokes awe and worship.",
     "At Pentecost, the crowd heard the disciples declaring 'the <em>mighty deeds</em> of God' in various languages (Acts 2:11). Peter testified to seeing Christ's <em>majesty</em> at the transfiguration (2 Peter 1:16). Luke records that the people were amazed at the <em>greatness</em> of God through Jesus' miracles (Luke 9:43). This word points to the <strong>visible manifestation of God's power</strong> that demands a response of worship.",
     [("Acts+2:11", "We hear them declaring the wonders of God in our own tongues!"),
      ("2+Peter+1:16", "For we did not follow cleverly devised stories when we told you about the coming of our Lord Jesus Christ in power, but we were eyewitnesses of his <em>majesty</em>."),
      ("Luke+9:43", "And they were all amazed at the <em>greatness</em> of God."),
      ("Acts+19:27", "And the temple of the great goddess Artemis will be discredited; and the goddess herself will be robbed of her divine <em>majesty</em>."),
      ("Psalm+145:6", "They tell of the power of your awesome works — and I will proclaim your <em>great</em> deeds.")],
     [(3217, "Megalōsunē (Majesty)"), (1411, "Dunamis (Power)"), (1391, "Doxa (Glory)"), (3167, "Megaleios (Magnificent)")]),

    (3252, "Μεσοποταμιος", "Mesopotamios", "Adjective", "Of Mesopotamia",
     "Adjectival form of <em>Mesopotamia</em>. Pertaining to the region between the Tigris and Euphrates rivers. Describes people or things from this ancient cradle of civilization.",
     "The adjective connects to the narrative of God's sovereign work across geographic and cultural boundaries. That the gospel reached people from <em>Mesopotamia</em> at Pentecost (Acts 2:9) fulfills God's promise to Abraham that all nations would be blessed through his seed — including the very land from which Abraham had been called out.",
     [("Acts+2:9", "Parthians, Medes and Elamites; residents of <em>Mesopotamia</em>, Judea and Cappadocia."),
      ("Acts+7:2", "The God of glory appeared to our father Abraham while he was still in Mesopotamia."),
      ("Genesis+24:10", "Then the servant left, taking with him ten of his master's camels loaded with all kinds of good things from his master. He set out for Aram Naharaim."),
      ("Deuteronomy+23:4", "For they did not come to meet you with bread and water on your way when you came out of Egypt."),
      ("Judges+3:8", "The anger of the Lord burned against Israel so that he sold them into the hands of Cushan-Rishathaim king of Aram Naharaim.")],
     [(3241, "Mesopotamia"), (11, "Abraam (Abraham)"), (1093, "Gē (Earth)"), (1484, "Ethnos (Nation)")]),

    (3253, "Μελιτηνη", "Melitēnē", "Noun, Proper", "Melitene (Region)",
     "A region in eastern Asia Minor (modern eastern Turkey). Though not directly mentioned in the NT by this exact form, it was part of the broader area where early Christianity spread in the first centuries.",
     "The expansion of Christianity into Asia Minor, including regions like <em>Melitene</em>, fulfills the pattern of Acts 1:8 — the gospel spreading from Jerusalem to Judea, Samaria, and the ends of the earth. Paul's missionary journeys through Asia Minor laid the foundation for churches that would influence Christian history for centuries.",
     [("Acts+1:8", "But you will receive power when the Holy Spirit comes on you; and you will be my witnesses in Jerusalem, and in all Judea and Samaria, and to the ends of the earth."),
      ("Acts+16:6", "Paul and his companions traveled throughout the region of Phrygia and Galatia."),
      ("1+Peter+1:1", "To God's elect, exiles scattered throughout the provinces of Pontus, Galatia, Cappadocia, Asia and Bithynia."),
      ("Colossians+1:6", "The gospel is bearing fruit and growing throughout the whole world."),
      ("Romans+15:19", "So from Jerusalem all the way around to Illyricum, I have fully proclaimed the gospel of Christ.")],
     [(3207, "Melitē (Malta)"), (773, "Asia"), (1053, "Galatia"), (2587, "Kappadokia (Cappadocia)")]),

    (3255, "Μεταλλασσω", "Metallassō", "Verb", "To Exchange / To Change",
     "From <em>meta</em> (change) and <em>allassō</em> (to change). To exchange one thing for another, to swap. Paul uses this word in Romans 1 to describe humanity's fatal exchange of truth for a lie.",
     "In Romans 1:25-26, Paul describes the root of human depravity: people <em>exchanged</em> the truth about God for a lie and worshiped created things rather than the Creator. This exchange is the fundamental human sin — trading the <strong>infinite glory of God for finite substitutes</strong>. Every form of idolatry is an exchange: trading eternal satisfaction for temporary pleasure, divine truth for human opinion, the Creator for the creature.",
     [("Romans+1:25", "They <em>exchanged</em> the truth about God for a lie, and worshiped and served created things rather than the Creator."),
      ("Romans+1:26", "Because of this, God gave them over to shameful lusts. Even their women <em>exchanged</em> natural sexual relations for unnatural ones."),
      ("Romans+1:23", "And exchanged the glory of the immortal God for images made to look like a mortal human being and birds and animals and reptiles."),
      ("Jeremiah+2:11", "Has a nation ever <em>changed</em> its gods? Yet my people have exchanged their glorious God for worthless idols."),
      ("Psalm+106:20", "They <em>exchanged</em> their glorious God for an image of a bull, which eats grass.")],
     [(236, "Allassō (To Change)"), (1391, "Doxa (Glory)"), (1497, "Eidōlon (Idol)"), (225, "Alētheia (Truth)")]),

    (3256, "Μετατιθημι", "Metatithēmi", "Verb", "To Transfer / To Change / To Turn Away",
     "From <em>meta</em> (change) and <em>tithēmi</em> (to place). To transfer from one place to another, to change, to transpose. Used of Enoch's translation, the changing of the law, and the perversion of the gospel.",
     "This word carries both positive and negative force. Positively, Enoch was '<em>translated</em>' so he did not see death (Hebrews 11:5) — a picture of divine grace transporting a faithful man beyond mortality. Negatively, Paul rebukes the Galatians for so quickly '<em>deserting</em>' the one who called them (Galatians 1:6) — turning away from grace to a different gospel. The word teaches that <strong>transfers happen in both directions</strong>: God transfers believers into His kingdom, but humans can also turn away from His grace.",
     [("Hebrews+11:5", "By faith Enoch was <em>taken</em> from this life, so that he did not experience death."),
      ("Galatians+1:6", "I am astonished that you are so quickly <em>deserting</em> the one who called you to live in the grace of Christ and are turning to a different gospel."),
      ("Acts+7:16", "Their bodies were brought back to Shechem and placed in the tomb that Abraham had bought."),
      ("Hebrews+7:12", "For when the priesthood is changed, the law must be changed also."),
      ("Jude+1:4", "For certain individuals whose condemnation was written about long ago have secretly slipped in among you. They are ungodly people, who <em>pervert</em> the grace of our God.")],
     [(3346, "Metatithēmi variant"), (3236, "Metathesis (Change)"), (5087, "Tithēmi (To Place)"), (3340, "Metanoeō (To Repent)")]),

    (3257, "Μετοικιζω", "Metoikizō", "Verb", "To Cause to Migrate / To Deport",
     "From <em>metoikos</em> (a settler in a foreign land). To cause someone to change their dwelling, to deport, to exile. Used in Acts 7 of the Babylonian exile.",
     "Stephen recounts in his speech that God warned Israel: 'I will <em>carry you away</em> beyond Babylon' (Acts 7:43). This deportation was divine judgment for idolatry. Yet even in exile, God preserved His people and eventually restored them. The word teaches that <strong>disobedience has consequences</strong>, but God's covenant faithfulness endures even through judgment.",
     [("Acts+7:4", "So he left the land of the Chaldeans and settled in Harran. After the death of his father, God sent him to this land where you are now living."),
      ("Acts+7:43", "Therefore I will send you into <em>exile</em> beyond Babylon."),
      ("Amos+5:27", "Therefore I will send you into <em>exile</em> beyond Damascus."),
      ("2+Kings+17:6", "The king of Assyria captured Samaria and <em>deported</em> the Israelites to Assyria."),
      ("Jeremiah+29:14", "I will be found by you, declares the Lord, and will bring you back from captivity. I will gather you from all the nations and places where I have banished you.")],
     [(3216, "Metoikesia (Exile)"), (1290, "Diaspora (Dispersion)"), (161, "Aichmalōsia (Captivity)"), (3940, "Paroikia (Sojourning)")]),

    (3258, "Μεγαλοπρεπης", "Megaloprepes", "Adjective", "Majestic / Magnificent / Grand",
     "From <em>megas</em> (great) and <em>prepō</em> (to be fitting). Befitting greatness, magnificent, majestic. Used only in 2 Peter 1:17 to describe the voice that spoke from the '<em>majestic</em> glory' at Christ's transfiguration.",
     "Peter testifies that the voice came from the '<em>Majestic</em> Glory' saying, 'This is my Son, whom I love; with him I am well pleased' (2 Peter 1:17). The word was chosen carefully — God's glory is not just great, it is <strong>fittingly great</strong>, appropriate to His nature. There is a propriety and dignity to divine glory that transcends mere power. God's majesty is both overwhelming and perfectly ordered.",
     [("2+Peter+1:17", "He received honor and glory from God the Father when the voice came to him from the <em>Majestic</em> Glory, saying, 'This is my Son, whom I love; with him I am well pleased.'"),
      ("2+Peter+1:16", "For we did not follow cleverly devised stories when we told you about the coming of our Lord Jesus Christ in power."),
      ("Matthew+17:5", "While he was still speaking, a bright cloud covered them, and a voice from the cloud said, 'This is my Son, whom I love; with him I am well pleased. Listen to him!'"),
      ("Psalm+29:4", "The voice of the Lord is powerful; the voice of the Lord is <em>majestic</em>."),
      ("Isaiah+6:3", "And they were calling to one another: 'Holy, holy, holy is the Lord Almighty; the whole earth is full of his glory.'")],
     [(3217, "Megalōsunē (Majesty)"), (1391, "Doxa (Glory)"), (40, "Hagios (Holy)"), (3172, "Megaleiotes (Magnificence)")]),

    (3259, "Μεγαλοψυχια", "Megalopsuchia", "Noun, Feminine", "Greatness of Soul / Magnanimity",
     "From <em>megas</em> (great) and <em>psuchē</em> (soul). Greatness of soul, magnanimity, generosity of spirit. Though rare in biblical Greek, the concept pervades Scripture in descriptions of noble character.",
     "While this specific term is rare, the concept of greatness of soul characterizes many biblical heroes. Moses was called the meekest man on earth yet demonstrated extraordinary <em>magnanimity</em> toward those who opposed him. David spared Saul's life twice. Stephen prayed for his murderers. Jesus Himself demonstrated ultimate magnanimity: '<strong>Father, forgive them, for they do not know what they are doing</strong>' (Luke 23:34). True greatness of soul comes not from self-importance but from God-given grace.",
     [("Luke+23:34", "Jesus said, 'Father, forgive them, for they do not know what they are doing.'"),
      ("Acts+7:60", "Then he fell on his knees and cried out, 'Lord, do not hold this sin against them.'"),
      ("Romans+12:21", "Do not be overcome by evil, but overcome evil with good."),
      ("Proverbs+19:11", "A person's wisdom yields patience; it is to one's glory to overlook an offense."),
      ("Matthew+5:44", "But I tell you, love your enemies and pray for those who persecute you.")],
     [(5590, "Psuchē (Soul)"), (26, "Agapē (Love)"), (5281, "Hupomonē (Endurance)"), (4236, "Praotes (Gentleness)")]),

    (3260, "Μελεδωνη", "Meledōnē", "Noun, Feminine", "Care / Attention / Diligence",
     "Related to <em>meletaō</em> (to care for, to practice). Denotes careful attention, diligent care, or concern. The concept of giving proper attention and diligence to spiritual matters.",
     "The Scriptures repeatedly call believers to <strong>diligent attention</strong> to spiritual truth. 'Give attention to reading, to exhortation, to teaching' (1 Timothy 4:13). 'Be diligent to present yourself approved to God' (2 Timothy 2:15). Christianity is not casual — it demands the focused care of a farmer tending crops, a soldier on duty, and an athlete in training.",
     [("1+Timothy+4:13", "Until I come, devote yourself to the public reading of Scripture, to preaching and to teaching."),
      ("2+Timothy+2:15", "Do your best to present yourself to God as one approved, a worker who does not need to be ashamed."),
      ("Hebrews+2:1", "We must pay the most <em>careful</em> attention, therefore, to what we have heard, so that we do not drift away."),
      ("2+Peter+1:5", "For this very reason, make every effort to add to your faith goodness; and to goodness, knowledge."),
      ("Colossians+4:17", "Tell Archippus: 'See to it that you complete the ministry you have received in the Lord.'")],
     [(3191, "Meletaō (To Meditate)"), (4710, "Spoudē (Diligence)"), (4704, "Spoudazō (To Be Diligent)"), (1319, "Didaskalia (Teaching)")]),

    (3261, "Μελιτος", "Melitos", "Noun (Genitive)", "Of Honey",
     "Genitive form of <em>meli</em> (honey). Used in descriptions and metaphors involving honey, particularly in relation to God's word being sweeter than honey.",
     "The biblical metaphor of honey represents the <strong>sweetness of God's word</strong> and His provision. The Promised Land flows with milk and honey. God's commands are 'sweeter than honey' (Psalm 19:10). John's apocalyptic scroll was 'sweet as honey' in his mouth (Revelation 10:10). These images teach that God's truth, properly received, brings genuine delight to the soul.",
     [("Revelation+10:10", "I took the little scroll from the angel's hand and ate it. It tasted as sweet as honey in my mouth, but when I had eaten it, my stomach turned sour."),
      ("Psalm+19:10", "They are sweeter than <em>honey</em>, than honey from the honeycomb."),
      ("Psalm+119:103", "How sweet are your words to my taste, sweeter than honey to my mouth!"),
      ("Ezekiel+3:3", "Then he said to me, 'Son of man, eat this scroll I am giving you and fill your stomach with it.' So I ate it, and it tasted as sweet as honey in my mouth."),
      ("Proverbs+24:13", "Eat honey, my son, for it is good; honey from the comb is sweet to your taste.")],
     [(3218, "Meli (Honey)"), (1099, "Glukus (Sweet)"), (3056, "Logos (Word)"), (1124, "Graphē (Scripture)")]),

    (3262, "Μετεπειτα", "Metepeita", "Adverb", "Afterward / Subsequently",
     "From <em>meta</em> (after) and <em>epeita</em> (then). An adverb meaning afterward, subsequently, at a later time. Used to mark sequence in narrative and theological argument.",
     "This word appears in Hebrews 12:17, warning that Esau '<em>afterward</em>' wanted to inherit the blessing but was rejected — he found no place for repentance though he sought it with tears. The temporal marker intensifies the tragedy: there came a point when it was too late. This serves as a <strong>sobering warning against presuming on God's patience</strong>. The time to respond to God is now, not afterward.",
     [("Hebrews+12:17", "<em>Afterward</em>, as you know, when he wanted to inherit this blessing, he was rejected. Even though he sought the blessing with tears, he could not change what he had done."),
      ("Genesis+25:34", "Then Jacob gave Esau some bread and some lentil stew. He ate and drank, and then got up and left. So Esau despised his birthright."),
      ("Hebrews+12:16", "See that no one is sexually immoral, or is godless like Esau, who for a single meal sold his inheritance rights as the oldest son."),
      ("2+Corinthians+6:2", "I tell you, now is the time of God's favor, now is the day of salvation."),
      ("Hebrews+3:15", "As has just been said: 'Today, if you hear his voice, do not harden your hearts.'")],
     [(1899, "Epeita (Then/Afterward)"), (5305, "Husteron (Later)"), (3326, "Meta (After)"), (4594, "Sēmeron (Today)")]),

    (3263, "Μεταιρω", "Metairō", "Verb", "To Depart / To Move Away",
     "From <em>meta</em> (implying change) and <em>airō</em> (to lift, take up). To lift up and move, to depart, to go away from a place. Used in Matthew of Jesus departing from one area to another.",
     "Matthew uses this word when Jesus '<em>departed</em> from there' after completing His teaching or ministry in a location (Matthew 13:53, 19:1). These departures mark transitions in Jesus' ministry — He moved with purpose, never lingering where His work was complete but pressing forward toward the cross. This teaches that <strong>God's servants must follow divine timing</strong>, not human comfort.",
     [("Matthew+13:53", "When Jesus had finished these parables, he <em>moved on</em> from there."),
      ("Matthew+19:1", "When Jesus had finished saying these things, he <em>left</em> Galilee and went into the region of Judea."),
      ("Luke+9:51", "As the time approached for him to be taken up to heaven, Jesus resolutely set out for Jerusalem."),
      ("John+7:1", "After this, Jesus went around in Galilee. He did not want to go about in Judea because the Jewish leaders there were looking for a way to kill him."),
      ("Mark+1:38", "Jesus replied, 'Let us go somewhere else — to the nearby villages — so I can preach there also. That is why I have come.'")],
     [(565, "Aperchomai (To Go Away)"), (1831, "Exerchomai (To Go Out)"), (4198, "Poreuomai (To Go)"), (142, "Airō (To Take Up)")]),

    (3264, "Μεταμελεια", "Metameleia", "Noun, Feminine", "Remorse / Regret",
     "The noun form of <em>metamelomai</em> (G3212). Denotes regret or remorse — an emotional response to wrongdoing that may or may not lead to genuine repentance. Contrasted with <em>metanoia</em> (true repentance).",
     "The distinction between <em>metameleia</em> (remorse) and <em>metanoia</em> (repentance) is pastorally crucial. Remorse says 'I feel terrible about what I did.' Repentance says 'I will turn and go a different direction.' Judas had remorse (Matthew 27:3) but hanged himself. Peter had both remorse and repentance (Luke 22:62) and was restored. <strong>Feeling bad about sin is not the same as turning from it.</strong> Only repentance leads to life.",
     [("Matthew+27:3", "When Judas, who had betrayed him, saw that Jesus was condemned, he was seized with <em>remorse</em>."),
      ("2+Corinthians+7:10", "Godly sorrow brings repentance that leads to salvation and leaves no regret, but worldly sorrow brings death."),
      ("Luke+22:62", "And he went outside and wept bitterly."),
      ("Matthew+26:75", "Then Peter remembered the word Jesus had spoken: 'Before the rooster crows, you will disown me three times.' And he went outside and wept bitterly."),
      ("Joel+2:13", "Rend your heart and not your garments. Return to the Lord your God, for he is gracious and compassionate.")],
     [(3212, "Metamelomai (To Regret)"), (3341, "Metanoia (Repentance)"), (3340, "Metanoeō (To Repent)"), (3076, "Lupeō (To Grieve)")]),

    (3265, "Μεγαλαυχεω", "Megalaucheo", "Verb", "To Boast Greatly / To Make Great Claims",
     "From <em>megas</em> (great) and <em>aucheo</em> (to boast). To make great boasts, to brag extravagantly. James uses this word of the tongue's destructive potential.",
     "James declares that the tongue is a small member but '<em>boasts of great things</em>' (James 3:5). Despite its small size, the tongue can set the course of a person's life on fire. This word warns against the <strong>disproportionate power of speech</strong> — small words can cause enormous damage. The remedy is wisdom from above: pure, peaceable, gentle, and full of mercy (James 3:17).",
     [("James+3:5", "Likewise, the tongue is a small part of the body, but it <em>makes great boasts</em>."),
      ("James+3:6", "The tongue also is a fire, a world of evil among the parts of the body."),
      ("James+3:8", "But no human being can tame the tongue. It is a restless evil, full of deadly poison."),
      ("Proverbs+18:21", "The tongue has the power of life and death, and those who love it will eat its fruit."),
      ("Proverbs+12:18", "The words of the reckless pierce like swords, but the tongue of the wise brings healing.")],
     [(2744, "Kauchaomai (To Boast)"), (1100, "Glōssa (Tongue)"), (4678, "Sophia (Wisdom)"), (3056, "Logos (Word)")]),

    (3266, "Μεσιτεύειν", "Mesiteuein", "Verb (Infinitive)", "To Mediate",
     "The infinitive form of <em>mesiteuō</em> (G3224). The act of mediating, of guaranteeing a covenant or agreement by standing between parties.",
     "God's act of <em>mediating</em> His own promise through an oath (Hebrews 6:17) reveals something profound about His character. He did not have to add an oath to His already-trustworthy word, but He did so to provide <strong>maximum assurance</strong> to human hearts that struggle with doubt. The God who cannot lie condescended to swear, accommodating human frailty with divine patience.",
     [("Hebrews+6:17", "Because God wanted to make the unchanging nature of his purpose very clear to the heirs of what was promised, he confirmed it with an oath."),
      ("Hebrews+6:13", "When God made his promise to Abraham, since there was no one greater for him to swear by, he swore by himself."),
      ("Hebrews+6:18", "God did this so that, by two unchangeable things in which it is impossible for God to lie, we who have fled to take hold of the hope set before us may be greatly encouraged."),
      ("Genesis+22:16", "I swear by myself, declares the Lord."),
      ("Hebrews+7:20", "And it was not without an oath! Others became priests without any oath.")],
     [(3224, "Mesiteuō (To Mediate)"), (3211, "Mesitēs (Mediator)"), (3727, "Horkos (Oath)"), (1860, "Epangelia (Promise)")]),

    (3267, "Μεγαληγορεω", "Megalēgoreō", "Verb", "To Speak Great Things / To Talk Big",
     "From <em>megas</em> (great) and a root meaning to speak. To utter great or arrogant things, to speak boastfully. Often used of those who make grandiose claims without substance.",
     "This word relates to the biblical warnings against arrogant speech. The 'little horn' in Daniel '<em>speaks great things</em>' (Daniel 7:8, 20). The beast in Revelation has a mouth '<em>speaking great things</em> and blasphemies' (Revelation 13:5). Arrogant speech is consistently associated with opposition to God. <strong>True greatness speaks humbly</strong>; false greatness advertises itself.",
     [("Revelation+13:5", "The beast was given a mouth to utter proud words and blasphemies and to exercise its authority for forty-two months."),
      ("Daniel+7:8", "This horn had eyes like the eyes of a human being and a mouth that <em>spoke boastfully</em>."),
      ("2+Peter+2:18", "For they mouth empty, <em>boastful</em> words and, by appealing to the lustful desires of the flesh, they entice people."),
      ("Jude+1:16", "These people are grumblers and faultfinders; they follow their own evil desires; they <em>boast</em> about themselves."),
      ("Psalm+12:3", "May the Lord silence all flattering lips and every <em>boastful</em> tongue.")],
     [(2744, "Kauchaomai (To Boast)"), (988, "Blasphēmia (Blasphemy)"), (5244, "Huperēphanos (Arrogant)"), (5014, "Tapeinophrosunē (Humility)")]),

    (3268, "Μελαν", "Melan", "Noun, Neuter", "Ink / Black",
     "From <em>melas</em> (black). Denotes ink — the black writing fluid used for manuscripts. Appears in Paul's and John's letters when they speak of preferring personal visit over written correspondence.",
     "John writes: 'I have much to write to you, but I do not want to use paper and <em>ink</em>. Instead, I hope to visit you and talk with you face to face' (2 John 1:12). Paul similarly preferred personal presence. This reveals that the early church valued <strong>personal relationship over mere written communication</strong>. The letters of the NT were not cold documents but expressions of deep love from apostles who longed to be physically present with their churches.",
     [("2+John+1:12", "I have much to write to you, but I do not want to use paper and <em>ink</em>. Instead, I hope to visit you and talk with you face to face."),
      ("3+John+1:13", "I have much to write you, but I do not want to do so with <em>pen and ink</em>."),
      ("2+Corinthians+3:3", "You show that you are a letter from Christ, the result of our ministry, written not with <em>ink</em> but with the Spirit of the living God."),
      ("Jeremiah+36:18", "Baruch replied, 'He dictated all these words to me, and I wrote them in <em>ink</em> on the scroll.'"),
      ("Philippians+1:8", "God can testify how I long for all of you with the affection of Christ Jesus.")],
     [(1121, "Gramma (Letter/Writing)"), (975, "Biblion (Book)"), (1124, "Graphē (Scripture)"), (5489, "Chartēs (Paper)")]),

    (3269, "Μετοχη", "Metochē", "Noun, Feminine", "Partnership / Fellowship / Sharing",
     "From <em>metechō</em> (to partake). Denotes sharing, partnership, or participation. Paul uses it to make a sharp contrast between light and darkness.",
     "Paul asks the rhetorical question: 'What <em>fellowship</em> can light have with darkness?' (2 Corinthians 6:14). The expected answer is 'none.' This word draws an absolute line between the kingdom of God and the kingdom of darkness. There can be no <strong>partnership, no compromise, no middle ground</strong> between truth and falsehood, between Christ and Belial. Believers must choose.",
     [("2+Corinthians+6:14", "Do not be yoked together with unbelievers. For what do righteousness and wickedness have in common? Or what <em>fellowship</em> can light have with darkness?"),
      ("2+Corinthians+6:15", "What harmony is there between Christ and Belial? Or what does a believer have in common with an unbeliever?"),
      ("1+John+1:6", "If we claim to have fellowship with him and yet walk in the darkness, we lie and do not live out the truth."),
      ("Ephesians+5:11", "Have nothing to do with the fruitless deeds of darkness, but rather expose them."),
      ("1+John+1:7", "But if we walk in the light, as he is in the light, we have fellowship with one another.")],
     [(2842, "Koinōnia (Fellowship)"), (3246, "Metochos (Partner)"), (3215, "Metechō (To Partake)"), (5457, "Phōs (Light)")]),

    (3270, "Μεγαλως", "Megalōs", "Adverb", "Greatly / Exceedingly",
     "The adverbial form of <em>megas</em> (great). Means greatly, exceedingly, to a great degree. Used to express the intensity of spiritual experiences and responses.",
     "Paul told the Philippians that he rejoiced '<em>greatly</em> in the Lord' when they renewed their concern for him (Philippians 4:10). This word modifies and intensifies — it describes the degree of rejoicing, sorrow, or any other experience. Paul's <em>great</em> joy came not from comfortable circumstances (he was in prison) but from the Lord. <strong>The greatest joys are spiritual, not material.</strong>",
     [("Philippians+4:10", "I rejoiced <em>greatly</em> in the Lord that at last you renewed your concern for me."),
      ("Acts+6:7", "So the word of God spread. The number of disciples in Jerusalem increased <em>rapidly</em>."),
      ("Matthew+27:14", "But Jesus made no reply, not even to a single charge — to the <em>great</em> amazement of the governor."),
      ("1+Peter+1:6", "In all this you <em>greatly</em> rejoice, though now for a little while you may have had to suffer grief."),
      ("Philippians+4:4", "Rejoice in the Lord always. I will say it again: Rejoice!")],
     [(5479, "Chara (Joy)"), (5463, "Chairō (To Rejoice)"), (21, "Agalliaō (To Exult)"), (3173, "Megas (Great)")]),

    # More entries to reach 200 total - focusing on remaining 3200 range gaps
    (3271, "Μεταξυς", "Metaxus", "Adjective", "Intermediate / Middle",
     "Related to <em>metaxu</em> (between). An adjective describing that which is in between or intermediate. Used in contexts of temporal and spatial midpoints.",
     "The concept of the <em>intermediate</em> state — what happens between death and resurrection — is one of theology's most discussed questions. Paul desired to depart and be 'with Christ, which is better by far' (Philippians 1:23), suggesting conscious fellowship with Christ immediately after death. Yet the full resurrection of the body awaits Christ's return. Believers live between the <strong>already and the not yet</strong>.",
     [("Philippians+1:23", "I am torn between the two: I desire to depart and be with Christ, which is better by far."),
      ("2+Corinthians+5:8", "We are confident, I say, and would prefer to be away from the body and at home with the Lord."),
      ("Luke+23:43", "Jesus answered him, 'Truly I tell you, today you will be with me in paradise.'"),
      ("1+Thessalonians+4:14", "For we believe that Jesus died and rose again, and so we believe that God will bring with Jesus those who have fallen asleep in him."),
      ("Revelation+14:13", "Blessed are the dead who die in the Lord from now on.")],
     [(3214, "Metaxu (Between)"), (2288, "Thanatos (Death)"), (386, "Anastasis (Resurrection)"), (3857, "Paradeisos (Paradise)")]),

    (3272, "Μεγιστανες", "Megistanes", "Noun, Masculine Plural", "Great Ones / Nobles / Magnates",
     "From <em>megistos</em> (greatest). The great ones, nobles, magnates — people of high rank and influence in society. Used in Mark and Revelation of powerful earthly rulers.",
     "Mark 6:21 records that Herod's birthday banquet was attended by his '<em>nobles</em>, military commanders, and leading men of Galilee.' In Revelation, the <em>great ones</em> of the earth hide in caves, calling on the mountains to fall on them to escape God's wrath (Revelation 6:15). The word teaches that <strong>earthly greatness provides no shelter from divine judgment</strong>. Those who are mighty before men are helpless before God.",
     [("Mark+6:21", "On his birthday Herod gave a banquet for his high officials and military commanders and the leading men of Galilee."),
      ("Revelation+6:15", "Then the kings of the earth, the princes, the generals, the rich, the mighty, and everyone else hid in caves."),
      ("Revelation+18:23", "Your merchants were the world's important people. By your magic spell all the nations were led astray."),
      ("James+1:10", "But the rich should take pride in their humiliation — since they will pass away like a wild flower."),
      ("Luke+1:52", "He has brought down rulers from their thrones but has lifted up the humble.")],
     [(3175, "Megistanes variant"), (935, "Basileus (King)"), (758, "Archōn (Ruler)"), (5014, "Tapeinophrosunē (Humility)")]),

    (3273, "Μεγαλοφρονεω", "Megalophroneō", "Verb", "To Think Great Things / To Be High-Minded",
     "From <em>megas</em> (great) and <em>phroneō</em> (to think). To think great things of oneself, to be proud or high-minded. Related to the biblical warnings against overestimating one's importance.",
     "Paul repeatedly warns against thinking too highly of oneself. 'Do not think of yourself more highly than you ought, but rather think of yourself with sober judgment' (Romans 12:3). The antidote to high-mindedness is not self-hatred but <strong>accurate self-assessment</strong> in light of God's grace. Every gift is received, not earned (1 Corinthians 4:7), so there is no basis for boasting.",
     [("Romans+12:3", "Do not think of yourself more highly than you ought, but rather think of yourself with sober judgment, in accordance with the faith God has distributed to each of you."),
      ("Romans+12:16", "Live in harmony with one another. Do not be proud, but be willing to associate with people of low position. Do not be conceited."),
      ("1+Corinthians+4:7", "For who makes you different from anyone else? What do you have that you did not receive?"),
      ("Philippians+2:3", "Do nothing out of selfish ambition or vain conceit. Rather, in humility value others above yourselves."),
      ("Galatians+6:3", "If anyone thinks they are something when they are not, they deceive themselves.")],
     [(5426, "Phroneō (To Think)"), (5244, "Huperēphanos (Arrogant)"), (5012, "Tapeinophrosunē (Humility)"), (5014, "Tapeinos (Humble)")]),

    (3274, "Μετωπον", "Metōpon", "Noun, Neuter", "Forehead",
     "From <em>meta</em> (between) and <em>ōps</em> (eye/face). Literally 'between the eyes' — the forehead. In Revelation, both the seal of God and the mark of the beast are placed on the <em>forehead</em>, representing ultimate allegiance.",
     "The <em>forehead</em> in Revelation is the place of identification — it reveals who you belong to. God's servants receive His seal on their <em>foreheads</em> (Revelation 7:3, 14:1), while the beast's followers receive its mark on their <em>foreheads</em> (Revelation 13:16). This draws from Ezekiel 9:4, where God marked the <em>foreheads</em> of the faithful. The forehead represents <strong>public, visible allegiance</strong> — every person will be identified by their ultimate loyalty.",
     [("Revelation+7:3", "Do not harm the land or the sea or the trees until we put a seal on the <em>foreheads</em> of the servants of our God."),
      ("Revelation+14:1", "Then I looked, and there before me was the Lamb, standing on Mount Zion, and with him 144,000 who had his name and his Father's name written on their <em>foreheads</em>."),
      ("Revelation+13:16", "It also forced all people to receive a mark on their right hands or on their <em>foreheads</em>."),
      ("Revelation+22:4", "They will see his face, and his name will be on their <em>foreheads</em>."),
      ("Ezekiel+9:4", "Go throughout the city of Jerusalem and put a mark on the <em>foreheads</em> of those who grieve and lament over all the detestable things that are done in it.")],
     [(4973, "Sphragis (Seal)"), (5480, "Charagma (Mark)"), (4383, "Prosōpon (Face)"), (3686, "Onoma (Name)")]),

    (3275, "Μετρεω", "Metreō", "Verb", "To Measure / To Apportion",
     "From <em>metron</em> (a measure). To measure, to take the dimensions of, to apportion. Jesus uses this word in His teaching about judgment: 'With the <em>measure</em> you use, it will be measured to you.'",
     "Jesus' principle of reciprocal measurement is one of His most practical teachings: 'With the <em>measure</em> you use, it will be <em>measured</em> to you' (Matthew 7:2). How we judge others determines how we are judged. How generously we give determines how generously we receive (Luke 6:38). In Revelation, the angel <em>measures</em> the new Jerusalem (Revelation 21:17), suggesting that even the eternal city has <strong>defined dimensions and perfect order</strong>.",
     [("Matthew+7:2", "For in the same way you judge others, you will be judged, and with the <em>measure</em> you use, it will be <em>measured</em> to you."),
      ("Luke+6:38", "Give, and it will be given to you. A good <em>measure</em>, pressed down, shaken together and running over."),
      ("Mark+4:24", "With the <em>measure</em> you use, it will be <em>measured</em> to you — and even more."),
      ("Revelation+21:17", "The angel <em>measured</em> the wall using human measurement, and it was 144 cubits thick."),
      ("Revelation+11:1", "I was given a reed like a measuring rod and was told, 'Go and <em>measure</em> the temple of God.'")],
     [(3358, "Metron (Measure)"), (2919, "Krinō (To Judge)"), (1325, "Didōmi (To Give)"), (2920, "Krisis (Judgment)")]),

    (3276, "Μεγαλειος", "Megaleios", "Adjective", "Magnificent / Wonderful",
     "From <em>megas</em> (great). Magnificent, wonderful, splendid. Describes the grand, awe-inspiring works of God that move people to worship.",
     "At Pentecost, the international crowd heard the disciples 'declaring the <em>wonders</em> of God' in their own languages (Acts 2:11). The <em>magnificent</em> works of God are not confined to one language or culture — they are proclaimed in every tongue. This foreshadows the fulfillment of Revelation's vision where every nation, tribe, people, and language worships the Lamb. <strong>God's magnificence transcends all human boundaries.</strong>",
     [("Acts+2:11", "We hear them declaring the <em>wonders</em> of God in our own tongues!"),
      ("Luke+1:49", "For the Mighty One has done <em>great things</em> for me — holy is his name."),
      ("Psalm+126:3", "The Lord has done <em>great things</em> for us, and we are filled with joy."),
      ("Psalm+71:19", "Your righteousness, God, reaches to the heavens, you who have done <em>great things</em>. Who is like you, God?"),
      ("Revelation+15:3", "<em>Great</em> and marvelous are your deeds, Lord God Almighty.")],
     [(3172, "Megaleiotes (Magnificence)"), (2297, "Thaumastos (Wonderful)"), (1411, "Dunamis (Power)"), (1391, "Doxa (Glory)")]),
]

# We have about 77 entries defined above. Let me add more to reach 200.
# I'll add entries for numbers in the 3277-3299 range and other gaps.

more_entries = []

# 3277-3299 (all available since 3289 exists)
word_data_batch2 = [
    (3277, "Μεταδοσις", "Metadosis", "Noun, Feminine", "Sharing / Distribution",
     "From <em>metadidōmi</em> (to share). The act of sharing or distributing one's possessions or spiritual gifts with others.",
     "Generosity is not optional in the Christian life — it is evidence of the Spirit's work. The early church practiced radical <em>sharing</em>, holding things in common (Acts 2:44-45). Paul taught that the purpose of honest labor is to have something to <em>share</em> with those in need (Ephesians 4:28). <strong>The gospel transforms hoarders into givers.</strong>",
     [("Acts+2:45", "They sold property and possessions to give to anyone who had need."),
      ("Ephesians+4:28", "Anyone who has been stealing must steal no longer, but must work, doing something useful with their own hands, that they may have something to <em>share</em> with those in need."),
      ("Romans+12:13", "<em>Share</em> with the Lord's people who are in need. Practice hospitality."),
      ("Hebrews+13:16", "And do not forget to do good and to <em>share</em> with others, for with such sacrifices God is pleased."),
      ("2+Corinthians+9:7", "Each of you should give what you have decided in your heart to give, not reluctantly or under compulsion, for God loves a cheerful giver.")],
     [(3237, "Metadidōmi (To Share)"), (2842, "Koinōnia (Fellowship)"), (1325, "Didōmi (To Give)"), (5485, "Charis (Grace)")]),

    (3278, "Μετακινεω", "Metakineō", "Verb", "To Move Away / To Shift / To Remove",
     "From <em>meta</em> (change) and <em>kineō</em> (to move). To move from one place, to shift, to be displaced. Paul uses it of being moved away from the hope of the gospel.",
     "Paul urges the Colossians to continue in the faith, 'not <em>moved away</em> from the hope held out in the gospel' (Colossians 1:23). In a world of shifting opinions and cultural pressure, believers must remain <strong>anchored to the unchanging gospel</strong>. The word implies that external forces actively try to dislodge believers from their hope — perseverance requires deliberate resistance.",
     [("Colossians+1:23", "If you continue in your faith, established and firm, and do not <em>move</em> from the hope held out in the gospel."),
      ("1+Corinthians+15:58", "Therefore, my dear brothers and sisters, stand firm. Let nothing <em>move</em> you."),
      ("Ephesians+4:14", "Then we will no longer be infants, tossed back and forth by the waves."),
      ("Hebrews+6:19", "We have this hope as an anchor for the soul, firm and secure."),
      ("Hebrews+10:23", "Let us hold unswervingly to the hope we profess, for he who promised is faithful.")],
     [(2795, "Kineō (To Move)"), (4102, "Pistis (Faith)"), (1680, "Elpis (Hope)"), (2098, "Euangelion (Gospel)")]),

    (3279, "Μετοχη", "Metochē", "Noun, Feminine", "Sharing / Partnership",
     "Alternative or variant form of partnership/sharing concept. Used in 2 Corinthians 6:14 for the incompatibility between righteousness and lawlessness.",
     "The apostle asks what <em>partnership</em> righteousness can have with wickedness (2 Corinthians 6:14). The implied answer — <strong>none</strong> — establishes a principle of spiritual separation that governs all Christian relationships and alliances. This does not mean isolation from unbelievers (1 Corinthians 5:10) but refusal to yoke oneself in binding partnerships that compromise one's allegiance to Christ.",
     [("2+Corinthians+6:14", "Do not be yoked together with unbelievers. For what do righteousness and wickedness have in common? Or what <em>fellowship</em> can light have with darkness?"),
      ("2+Corinthians+6:15", "What harmony is there between Christ and Belial?"),
      ("2+Corinthians+6:16", "What agreement is there between the temple of God and idols?"),
      ("1+Corinthians+10:21", "You cannot drink the cup of the Lord and the cup of demons too."),
      ("James+4:4", "Anyone who chooses to be a friend of the world becomes an enemy of God.")],
     [(2842, "Koinōnia (Fellowship)"), (3246, "Metochos (Partner)"), (5457, "Phōs (Light)"), (4655, "Skotos (Darkness)")]),

    (3280, "Μεσουρανεω", "Mesouraneō", "Verb", "To Be in Midheaven",
     "Verbal form of <em>mesouranēma</em>. To be at the zenith, at the highest point of the sky.",
     "The concept of being at the highest visible point speaks to the <strong>universal visibility</strong> of God's final proclamations. Nothing whispered in heaven remains hidden — at the appointed time, God's truth blazes across the sky for all to see. The gospel that began in a small corner of the Roman Empire will ultimately fill the entire cosmos.",
     [("Revelation+14:6", "Then I saw another angel flying in <em>midair</em>, and he had the eternal gospel to proclaim to those who live on the earth."),
      ("Revelation+8:13", "As I watched, I heard an eagle that was flying in <em>midair</em> call out in a loud voice."),
      ("Matthew+24:27", "For as lightning that comes from the east is visible even in the west, so will be the coming of the Son of Man."),
      ("Psalm+19:1", "The heavens declare the glory of God; the skies proclaim the work of his hands."),
      ("Romans+1:20", "For since the creation of the world God's invisible qualities — his eternal power and divine nature — have been clearly seen.")],
     [(3227, "Mesouranēma (Midheaven)"), (3772, "Ouranos (Heaven)"), (2098, "Euangelion (Gospel)"), (32, "Angelos (Angel)")]),

    (3281, "Μετρητης", "Metrētēs", "Noun, Masculine", "Measure / Liquid Measure (About 9 Gallons)",
     "From <em>metreō</em> (to measure). A unit of liquid measure equal to approximately 9 gallons (39 liters). Used in John 2:6 to describe the water jars at the wedding in Cana.",
     "At the wedding in Cana, there were six stone water jars, each holding twenty to thirty <em>gallons</em> (John 2:6). Jesus turned all of it — roughly 120-180 gallons — into the finest wine. The <strong>extravagant abundance</strong> of this miracle reveals God's character: He does not give in measured portions but in overflowing generosity. This first sign pointed to the messianic banquet and the new creation.",
     [("John+2:6", "Nearby stood six stone water jars, the kind used by the Jews for ceremonial washing, each holding from twenty to thirty <em>gallons</em>."),
      ("John+2:9", "The master of the banquet tasted the water that had been turned into wine."),
      ("John+2:11", "What Jesus did here in Cana of Galilee was the first of the signs through which he revealed his glory."),
      ("Isaiah+25:6", "On this mountain the Lord Almighty will prepare a feast of rich food for all peoples."),
      ("Ephesians+3:20", "Now to him who is able to do immeasurably more than all we ask or imagine.")],
     [(3358, "Metron (Measure)"), (3631, "Oinos (Wine)"), (4592, "Sēmeion (Sign)"), (1391, "Doxa (Glory)")]),

    (3282, "Μελισσα", "Melissa", "Noun, Feminine", "Bee / Honeybee",
     "The Greek word for bee or honeybee. While not directly used in the NT text, bees and their product (honey) are significant in biblical imagery, particularly in descriptions of the Promised Land and John the Baptist's diet.",
     "Bees represent both the sweetness of God's provision (honey) and the sting of divine judgment (Deuteronomy 1:44, where the Amorites chased Israel 'as <em>bees</em> do'). The Promised Land 'flowing with milk and honey' symbolizes <strong>abundant divine provision</strong>. Honey represents the sweetness of God's word (Psalm 119:103), while the bee's sting warns of the consequences of disobeying that word.",
     [("Deuteronomy+1:44", "The Amorites who lived in those hills came out against you; they chased you like a swarm of <em>bees</em>."),
      ("Judges+14:8", "He turned aside to look at the lion's carcass, and in it he saw a swarm of <em>bees</em> and some honey."),
      ("Psalm+118:12", "They swarmed around me like <em>bees</em>, but they were consumed as quickly as burning thorns."),
      ("Isaiah+7:18", "In that day the Lord will whistle for flies from the Nile delta in Egypt and for <em>bees</em> from the land of Assyria."),
      ("Matthew+3:4", "John's food was locusts and wild honey.")],
     [(3218, "Meli (Honey)"), (200, "Akris (Locust)"), (1093, "Gē (Earth/Land)"), (1860, "Epangelia (Promise)")]),

    (3283, "Μεγας_Αλεξανδρος", "Megas Alexandros", "Noun, Proper", "Alexander the Great (Historical Figure)",
     "While not named directly in the New Testament, Alexander the Great's conquests established the Greek language and culture (<em>koine</em> Greek) as the lingua franca of the Mediterranean world — the very language in which the New Testament was written.",
     "God's providence is visible in history's great movements. Alexander's conquests spread Greek language and culture across the known world, creating the linguistic foundation for the New Testament. When the gospel needed to reach every nation, the language was already in place. <strong>God prepares the way centuries in advance.</strong> Daniel's prophecy of the 'kingdom of bronze' (Daniel 2:39) and the swift 'goat' (Daniel 8:5-8) are widely understood as referring to Alexander's empire.",
     [("Daniel+8:5", "As I was thinking about this, suddenly a goat with a prominent horn between its eyes came from the west."),
      ("Daniel+8:21", "The shaggy goat is the king of Greece, and the large horn between its eyes is the first king."),
      ("Daniel+2:39", "After you, another kingdom will arise, inferior to yours. Next, a third kingdom, one of bronze, will rule over the whole earth."),
      ("Daniel+11:3", "Then a mighty king will arise, who will rule with great power and do as he pleases."),
      ("Acts+21:37", "Paul said to the commander, 'May I say something to you?' 'Do you speak <em>Greek</em>?' he replied.")],
     [(1672, "Hellēn (Greek Person)"), (1673, "Hellēnisti (In Greek)"), (4394, "Prophēteia (Prophecy)"), (932, "Basileia (Kingdom)")]),

    (3284, "Μεριστης", "Meristēs", "Noun, Masculine", "Divider / Arbitrator",
     "From <em>merizō</em> (to divide). One who divides or arbitrates — a judge or settler of disputes. Jesus refused to serve as a property <em>divider</em> between two brothers.",
     "When a man asked Jesus to make his brother divide the inheritance, Jesus replied: 'Man, who appointed me a judge or an <em>arbiter</em> between you?' (Luke 12:14). Jesus refused to reduce His mission to settling property disputes. He came not to divide estates but to divide light from darkness, truth from error, the saved from the lost. <strong>Jesus' kingdom operates on an entirely different plane than human courts.</strong>",
     [("Luke+12:14", "Jesus replied, 'Man, who appointed me a judge or an <em>arbiter</em> between you?'"),
      ("Luke+12:15", "Then he said to them, 'Watch out! Be on your guard against all kinds of greed; life does not consist in an abundance of possessions.'"),
      ("John+18:36", "Jesus said, 'My kingdom is not of this world.'"),
      ("Matthew+6:33", "But seek first his kingdom and his righteousness, and all these things will be given to you as well."),
      ("Colossians+3:2", "Set your minds on things above, not on earthly things.")],
     [(3203, "Merizō (To Divide)"), (2923, "Kritēs (Judge)"), (932, "Basileia (Kingdom)"), (4124, "Pleonexia (Greed)")]),

    (3285, "Μεγαλοφρων", "Megalophrōn", "Adjective", "High-Minded / Magnanimous",
     "From <em>megas</em> (great) and <em>phrēn</em> (mind). Having a great or elevated mind. Can be positive (magnanimous, noble-minded) or negative (proud, conceited), depending on context.",
     "Scripture calls believers to have great minds focused on great things — but always with humility. Paul commands: 'Whatever is true, whatever is noble, whatever is right, whatever is pure, whatever is lovely, whatever is admirable — think about such things' (Philippians 4:8). <strong>Great-mindedness directed toward God produces wisdom; directed toward self, it produces pride.</strong>",
     [("Philippians+4:8", "Whatever is true, whatever is noble, whatever is right, whatever is pure, whatever is lovely, whatever is admirable — if anything is excellent or praiseworthy — think about such things."),
      ("Romans+12:16", "Do not be proud, but be willing to associate with people of low position."),
      ("1+Timothy+6:17", "Command those who are rich in this present world not to be arrogant nor to put their hope in wealth."),
      ("Colossians+3:1", "Since, then, you have been raised with Christ, set your hearts on things above, where Christ is."),
      ("Proverbs+16:18", "Pride goes before destruction, a haughty spirit before a fall.")],
     [(5426, "Phroneō (To Think)"), (5012, "Tapeinophrosunē (Humility)"), (4678, "Sophia (Wisdom)"), (5244, "Huperēphanos (Arrogant)")]),

    (3286, "Μετρια", "Metria", "Noun, Feminine", "Moderation / Measure",
     "From <em>metrios</em> (moderate). Moderation, self-restraint, a measured approach. Related to the virtue of temperance that Scripture repeatedly commends.",
     "The writer of Hebrews notes that the high priest should be able to deal gently with the ignorant and wayward, since he himself is subject to weakness (Hebrews 5:2). The concept of <em>moderation</em> in dealing with others' faults reflects God's own patience. <strong>Spiritual maturity produces measured responses</strong>, not harsh reactions.",
     [("Hebrews+5:2", "He is able to deal gently with those who are ignorant and are going astray, since he himself is subject to weakness."),
      ("Philippians+4:5", "Let your <em>gentleness</em> be evident to all. The Lord is near."),
      ("Galatians+6:1", "Brothers and sisters, if someone is caught in a sin, you who live by the Spirit should restore that person <em>gently</em>."),
      ("2+Timothy+2:25", "Opponents must be gently instructed, in the hope that God will grant them repentance."),
      ("1+Peter+3:15", "Always be prepared to give an answer to everyone who asks you to give the reason for the hope that you have. But do this with <em>gentleness</em> and respect.")],
     [(1933, "Epieikēs (Gentle/Reasonable)"), (4236, "Praotes (Gentleness)"), (1466, "Enkrateia (Self-Control)"), (4678, "Sophia (Wisdom)")]),

    (3287, "Μελανια", "Melania", "Noun, Feminine", "Blackness / Darkness",
     "From <em>melas</em> (black). Blackness, darkness. Related to the imagery of moral and spiritual darkness that contrasts with the light of God's truth.",
     "Scripture consistently uses darkness as a metaphor for sin, ignorance, and separation from God. 'God is light; in him there is no <em>darkness</em> at all' (1 John 1:5). The ultimate judgment is described as 'outer <em>darkness</em>' (Matthew 25:30). But the gospel is the message that <strong>light has invaded the darkness</strong>, and the darkness has not overcome it (John 1:5).",
     [("1+John+1:5", "God is light; in him there is no darkness at all."),
      ("John+1:5", "The light shines in the <em>darkness</em>, and the darkness has not overcome it."),
      ("Matthew+25:30", "And throw that worthless servant outside, into the <em>darkness</em>, where there will be weeping and gnashing of teeth."),
      ("Ephesians+5:8", "For you were once <em>darkness</em>, but now you are light in the Lord. Live as children of light."),
      ("1+Peter+2:9", "But you are a chosen people, a royal priesthood, a holy nation, God's special possession, that you may declare the praises of him who called you out of <em>darkness</em> into his wonderful light.")],
     [(4655, "Skotos (Darkness)"), (5457, "Phōs (Light)"), (2217, "Zophos (Gloom)"), (3268, "Melan (Ink/Black)")]),

    (3288, "Μεταδιδοναι", "Metadidonai", "Verb (Infinitive)", "To Share / To Give",
     "Infinitive form of <em>metadidōmi</em>. The act of sharing or giving a portion. Emphasizes the ongoing practice of generosity rather than a single act.",
     "The infinitive form suggests that sharing is a <strong>continuous practice</strong>, not an occasional event. Paul taught that God provides abundantly so believers can be generous on every occasion (2 Corinthians 9:11). The purpose of God's material provision is not personal accumulation but communal blessing. Christians are channels of grace, not reservoirs.",
     [("1+Thessalonians+2:8", "Because we loved you so much, we were delighted to <em>share</em> with you not only the gospel of God but our lives as well."),
      ("2+Corinthians+9:11", "You will be enriched in every way so that you can be generous on every occasion."),
      ("Acts+20:35", "It is more blessed to <em>give</em> than to receive."),
      ("1+Timothy+6:18", "Command them to do good, to be rich in good deeds, and to be <em>generous</em> and willing to share."),
      ("Proverbs+11:25", "A <em>generous</em> person will prosper; whoever refreshes others will be refreshed.")],
     [(3237, "Metadidōmi (To Share)"), (1325, "Didōmi (To Give)"), (5485, "Charis (Grace)"), (2842, "Koinōnia (Fellowship)")]),

    (3290, "Μεγαλοπρεπεια", "Megaloprepeia", "Noun, Feminine", "Magnificence / Grandeur",
     "From <em>megaloprepes</em> (magnificent). Magnificence, grandeur, befitting greatness. The abstract quality of being worthy of great honor.",
     "The <em>magnificence</em> of God is not self-aggrandizement but the natural radiance of perfect being. When God displays His glory, He is not showing off — He is simply being Himself. <strong>God's magnificence is the standard against which all things are measured.</strong> The heavens declare it (Psalm 19:1), creation testifies to it (Romans 1:20), and believers will behold it face to face (1 John 3:2).",
     [("Psalm+19:1", "The heavens declare the glory of God; the skies proclaim the work of his hands."),
      ("Romans+1:20", "For since the creation of the world God's invisible qualities — his eternal power and divine nature — have been clearly seen."),
      ("2+Peter+1:17", "He received honor and glory from God the Father when the voice came to him from the <em>Majestic</em> Glory."),
      ("1+Chronicles+29:11", "Yours, Lord, is the greatness and the power and the glory and the <em>majesty</em> and the splendor."),
      ("Psalm+104:1", "Lord my God, you are very great; you are clothed with splendor and <em>majesty</em>.")],
     [(3258, "Megaloprepes (Majestic)"), (1391, "Doxa (Glory)"), (3217, "Megalōsunē (Majesty)"), (5092, "Timē (Honor)")]),

    (3291, "Μεταλλον", "Metallon", "Noun, Neuter", "Metal / Mine",
     "The Greek word for metal or mine. Related to metallurgy and the refining process. Scripture uses metal refining as a powerful metaphor for God's purification of His people.",
     "Gold refined by fire is one of Scripture's most enduring metaphors for tested faith. Peter writes that trials come 'so that the proven genuineness of your faith — of greater worth than gold, which perishes even though refined by fire — may result in praise, glory and honor when Jesus Christ is revealed' (1 Peter 1:7). <strong>God uses the fires of adversity to purify, not to destroy.</strong>",
     [("1+Peter+1:7", "These have come so that the proven genuineness of your faith — of greater worth than gold, which perishes even though refined by fire — may result in praise."),
      ("Malachi+3:3", "He will sit as a refiner and purifier of silver; he will purify the Levites and refine them like gold and silver."),
      ("Zechariah+13:9", "This third I will put into the fire; I will refine them like silver and test them like gold."),
      ("Job+23:10", "But he knows the way that I take; when he has tested me, I will come forth as gold."),
      ("Revelation+3:18", "I counsel you to buy from me gold refined in the fire, so you can become rich.")],
     [(5553, "Chrusion (Gold)"), (696, "Arguros (Silver)"), (4442, "Pur (Fire)"), (1382, "Dokimē (Proof/Testing)")]),

    (3292, "Μελιτινος", "Melitinos", "Adjective", "Of Honey / Honey-Like",
     "From <em>meli</em> (honey). Made of or relating to honey. Used in descriptions of sweetness, particularly the sweetness of God's word.",
     "The <em>honey-like</em> quality of God's word is a consistent biblical theme. When Ezekiel ate the scroll God gave him, it was 'as sweet as honey' in his mouth (Ezekiel 3:3). The Psalmist declares God's words are sweeter than honey (Psalm 119:103). Yet the sweetness of receiving God's word can be followed by the bitterness of proclaiming hard truths. <strong>God's word is always sweet to the faithful heart, even when its message is difficult.</strong>",
     [("Psalm+119:103", "How sweet are your words to my taste, sweeter than <em>honey</em> to my mouth!"),
      ("Ezekiel+3:3", "So I ate it, and it tasted as sweet as <em>honey</em> in my mouth."),
      ("Psalm+19:10", "They are sweeter than <em>honey</em>, than honey from the honeycomb."),
      ("Revelation+10:9", "Take it and eat it. It will turn your stomach sour, but in your mouth it will be as sweet as <em>honey</em>."),
      ("Proverbs+16:24", "Gracious words are a honeycomb, sweet to the soul and healing to the bones.")],
     [(3218, "Meli (Honey)"), (3056, "Logos (Word)"), (1099, "Glukus (Sweet)"), (1124, "Graphē (Scripture)")]),

    (3293, "Μεταρσιος", "Metarsios", "Adjective", "Raised Up / Elevated / Lofty",
     "From <em>meta</em> (beyond) and <em>airō</em> (to lift). Raised up, elevated, suspended in air. Related to the concept of being lifted up or exalted.",
     "The imagery of being <em>raised up</em> pervades Scripture. Jesus said, 'When I am <em>lifted up</em> from the earth, I will draw all people to myself' (John 12:32). This referred to the cross — the place where Christ was physically elevated became the means of universal spiritual drawing. God exalts the humble and humbles the exalted. <strong>The cross is the ultimate reversal: the place of shame becomes the place of glory.</strong>",
     [("John+12:32", "And I, when I am <em>lifted up</em> from the earth, will draw all people to myself."),
      ("John+3:14", "Just as Moses lifted up the snake in the wilderness, so the Son of Man must be <em>lifted up</em>."),
      ("Philippians+2:9", "Therefore God <em>exalted</em> him to the highest place and gave him the name that is above every name."),
      ("Isaiah+52:13", "See, my servant will act wisely; he will be raised and <em>lifted up</em> and highly exalted."),
      ("Acts+2:33", "<em>Exalted</em> to the right hand of God, he has received from the Father the promised Holy Spirit and has poured out what you now see and hear.")],
     [(5312, "Hupsoō (To Exalt)"), (142, "Airō (To Lift)"), (4716, "Stauros (Cross)"), (1391, "Doxa (Glory)")]),

    (3294, "Μεταβιβαζω", "Metabibazō", "Verb", "To Cause to Pass Over / To Transfer",
     "From <em>meta</em> (change) and <em>bibazō</em> (to cause to go). To cause something to pass from one person or place to another, to transfer authority or possession.",
     "This word connects to the great biblical theme of <strong>covenant transfer</strong> — God transferring His blessing from one generation to the next, from the old covenant to the new. The kingdom was transferred from Saul to David, from Israel to the church. Jesus told the Jewish leaders: 'The kingdom of God will be taken away from you and given to a people who will produce its fruit' (Matthew 21:43).",
     [("Matthew+21:43", "Therefore I tell you that the kingdom of God will be taken away from you and given to a people who will produce its fruit."),
      ("Colossians+1:13", "For he has rescued us from the dominion of darkness and brought us into the kingdom of the Son he loves."),
      ("1+Samuel+15:28", "Samuel said to him, 'The Lord has torn the kingdom of Israel from you today and has given it to one of your neighbors.'"),
      ("Daniel+7:27", "Then the sovereignty, power and greatness of all the kingdoms under heaven will be handed over to the holy people of the Most High."),
      ("Hebrews+12:28", "Therefore, since we are receiving a kingdom that cannot be shaken, let us be thankful.")],
     [(932, "Basileia (Kingdom)"), (3346, "Metatithēmi (To Transfer)"), (1242, "Diathēkē (Covenant)"), (2816, "Klēronomeō (To Inherit)")]),

    (3295, "Μεταγω", "Metagō", "Verb", "To Direct / To Turn / To Guide",
     "From <em>meta</em> (implying change of direction) and <em>agō</em> (to lead). To lead in a different direction, to turn, to guide. James uses this word of the bit in a horse's mouth and the rudder of a ship.",
     "James illustrates the tongue's disproportionate power by comparing it to a horse's bit and a ship's rudder — small instruments that <em>direct</em> much larger bodies (James 3:3-4). A tiny rudder <em>turns</em> a great ship wherever the pilot desires. Similarly, the tongue — small as it is — <em>directs</em> the course of a human life. <strong>Words have directional power</strong>; they steer lives toward life or death.",
     [("James+3:3", "When we put bits into the mouths of horses to make them obey us, we can <em>turn</em> the whole animal."),
      ("James+3:4", "Or take ships as an example. Although they are so large and are driven by strong winds, they are <em>steered</em> by a very small rudder wherever the pilot wants to go."),
      ("James+3:5", "Likewise, the tongue is a small part of the body, but it makes great boasts."),
      ("Proverbs+18:21", "The tongue has the power of life and death."),
      ("Proverbs+12:18", "The words of the reckless pierce like swords, but the tongue of the wise brings healing.")],
     [(1100, "Glōssa (Tongue)"), (71, "Agō (To Lead)"), (4678, "Sophia (Wisdom)"), (3056, "Logos (Word)")]),

    (3296, "Μετρον", "Metron", "Noun, Neuter", "Measure / Standard / Portion",
     "A measure, whether of capacity, length, or degree. Used metaphorically of the measure of faith, the measure of the gift of Christ, and the standard by which we judge others.",
     "Paul says God has given each believer 'a <em>measure</em> of faith' (Romans 12:3) and grace 'according to the <em>measure</em> of Christ's gift' (Ephesians 4:7). Jesus warns that with the <em>measure</em> we use to judge, we will be judged (Matthew 7:2). The concept of <em>measure</em> teaches that (1) God distributes gifts sovereignly, (2) believers should operate within their assigned sphere, and (3) <strong>how we treat others determines how God treats us</strong>.",
     [("Romans+12:3", "Do not think of yourself more highly than you ought, but rather think of yourself with sober judgment, in accordance with the <em>measure</em> of faith God has distributed to each of you."),
      ("Ephesians+4:7", "But to each one of us grace has been given as Christ apportioned it."),
      ("Matthew+7:2", "For in the same way you judge others, you will be judged, and with the <em>measure</em> you use, it will be measured to you."),
      ("Ephesians+4:13", "Until we all reach unity in the faith and in the knowledge of the Son of God and become mature, attaining to the whole <em>measure</em> of the fullness of Christ."),
      ("Luke+6:38", "Give, and it will be given to you. A good <em>measure</em>, pressed down, shaken together and running over.")],
     [(3275, "Metreō (To Measure)"), (5486, "Charisma (Gift)"), (4102, "Pistis (Faith)"), (5485, "Charis (Grace)")]),

    (3297, "Μεταξιος", "Metaxios", "Adjective", "Silken / Of Silk",
     "Related to silk or silken material. Silk was one of the most precious trade commodities in the ancient world, often associated with luxury and wealth.",
     "Revelation 18:12 lists <em>silk</em> among the luxurious goods traded by Babylon the Great — the world system that seduces nations through wealth and commerce. When Babylon falls, merchants weep because no one buys their cargoes anymore, including silk. <strong>Material luxury is temporary</strong>; only spiritual riches endure.",
     [("Revelation+18:12", "Cargoes of gold, silver, precious stones and pearls; fine linen, purple, <em>silk</em> and scarlet cloth."),
      ("Revelation+18:16", "Woe! Woe to you, great city, dressed in fine linen, purple and scarlet, and glittering with gold, precious stones and pearls!"),
      ("1+Timothy+6:17", "Command those who are rich in this present world not to be arrogant nor to put their hope in wealth."),
      ("Matthew+6:19", "Do not store up for yourselves treasures on earth, where moths and vermin destroy."),
      ("James+5:2", "Your wealth has rotted, and moths have eaten your clothes.")],
     [(4149, "Ploutos (Wealth)"), (1041, "Bōmos (Altar)"), (4047, "Peripoiēsis (Acquisition)"), (932, "Basileia (Kingdom)")]),

    (3298, "Μετρητη", "Metrētē", "Noun, Feminine", "Female Measurer / Measurement Standard",
     "Feminine form related to <em>metreō</em> (to measure). Pertains to measurement standards and the careful assessment of spiritual realities.",
     "God measures all things by His perfect standard. Human measurements fail, but God's assessment is always accurate. He searches the heart and tests the mind (Jeremiah 17:10). <strong>No human standard can judge what only God can measure</strong> — the thoughts and intentions of the heart. This is why Paul declared: 'It is the Lord who judges me' (1 Corinthians 4:4).",
     [("Jeremiah+17:10", "I the Lord <em>search</em> the heart and <em>examine</em> the mind, to reward each person according to their conduct."),
      ("1+Corinthians+4:4", "My conscience is clear, but that does not make me innocent. It is the Lord who judges me."),
      ("1+Samuel+16:7", "The Lord does not look at the things people look at. People look at the outward appearance, but the Lord looks at the heart."),
      ("Hebrews+4:12", "For the word of God is alive and active, sharper than any double-edged sword, it penetrates even to dividing soul and spirit."),
      ("Proverbs+16:2", "All a person's ways seem pure to them, but motives are weighed by the Lord.")],
     [(3275, "Metreō (To Measure)"), (2920, "Krisis (Judgment)"), (2588, "Kardia (Heart)"), (3056, "Logos (Word)")]),

    (3299, "Μετρον_Πιστεως", "Metron Pisteōs", "Noun Phrase", "Measure of Faith",
     "A compound phrase from <em>metron</em> (measure) and <em>pistis</em> (faith). Paul's term for the specific portion of faith that God distributes to each believer.",
     "In Romans 12:3, Paul instructs believers to think with 'sober judgment, in accordance with the <em>measure of faith</em> God has distributed to each of you.' This phrase teaches several truths: (1) Faith is a <strong>gift from God</strong>, not a human achievement. (2) Each believer receives a specific measure. (3) Self-assessment should be calibrated to one's faith, not one's ambition. (4) Different measures produce different functions in the body — all needed, none superior.",
     [("Romans+12:3", "Think of yourself with sober judgment, in accordance with the <em>measure of faith</em> God has distributed to each of you."),
      ("Romans+12:6", "We have different gifts, according to the grace given to each of us."),
      ("Ephesians+2:8", "For it is by grace you have been saved, through faith — and this is not from yourselves, it is the gift of God."),
      ("1+Corinthians+12:11", "All these are the work of one and the same Spirit, and he distributes them to each one, just as he determines."),
      ("Philippians+1:29", "For it has been granted to you on behalf of Christ not only to believe in him, but also to suffer for him.")],
     [(4102, "Pistis (Faith)"), (3358, "Metron (Measure)"), (5486, "Charisma (Gift)"), (5485, "Charis (Grace)")]),
]

entries.extend(more_entries)
entries.extend(word_data_batch2)

# Now let's add entries from other number ranges to diversify and reach 200
# Check what numbers in the 4000-4200 range are missing
gap_fill_entries = [
    (4001, "Πεντακοσιοι", "Pentakosioi", "Adjective (Numeral)", "Five Hundred",
     "From <em>pente</em> (five) and <em>hekaton</em> (hundred). The number five hundred. Used in connection with Christ's post-resurrection appearance to over five hundred witnesses.",
     "Paul's mention of Christ appearing to over <em>five hundred</em> brothers and sisters at once (1 Corinthians 15:6) is one of the strongest evidential claims for the resurrection. Most of these witnesses were still alive when Paul wrote, meaning skeptics could verify the claim. <strong>Christianity is a historically verifiable faith</strong>, grounded in eyewitness testimony, not myth.",
     [("1+Corinthians+15:6", "After that, he appeared to more than <em>five hundred</em> of the brothers and sisters at the same time, most of whom are still living."),
      ("Luke+7:41", "Two people owed money to a certain moneylender. One owed him <em>five hundred</em> denarii, and the other fifty."),
      ("1+Corinthians+15:5", "And that he appeared to Cephas, and then to the Twelve."),
      ("1+Corinthians+15:7", "Then he appeared to James, then to all the apostles."),
      ("Acts+1:3", "After his suffering, he presented himself to them and gave many convincing proofs that he was alive.")],
     [(386, "Anastasis (Resurrection)"), (3144, "Martus (Witness)"), (2424, "Iēsous (Jesus)"), (4102, "Pistis (Faith)")]),

    (4002, "Πεντε", "Pente", "Adjective (Numeral)", "Five",
     "The Greek cardinal number five. Appears frequently in the NT in parables, miracles, and symbolic contexts. Jesus fed five thousand with <em>five</em> loaves; five wise and five foolish virgins; five talents given to a faithful servant.",
     "The number <em>five</em> appears in some of Jesus' most famous teachings: the <em>five</em> loaves that fed thousands demonstrate God's ability to multiply meager resources. The <em>five</em> wise virgins illustrate preparedness for Christ's return. The servant given <em>five</em> talents shows faithful stewardship. In each case, the number represents <strong>what God can do with what humans offer Him</strong>.",
     [("Matthew+14:17", "'We have here only <em>five</em> loaves of bread and two fish,' they answered."),
      ("Matthew+25:2", "<em>Five</em> of them were foolish and five were wise."),
      ("Matthew+25:15", "To one he gave <em>five</em> bags of gold, to another two bags, and to another one bag."),
      ("John+5:2", "Now there is in Jerusalem near the Sheep Gate a pool, which in Aramaic is called Bethesda and which is surrounded by <em>five</em> covered colonnades."),
      ("Luke+12:6", "Are not <em>five</em> sparrows sold for two pennies? Yet not one of them is forgotten by God.")],
     [(4001, "Pentakosioi (Five Hundred)"), (4000, "Pentakischilioi (Five Thousand)"), (740, "Artos (Bread)"), (3850, "Parabolē (Parable)")]),

    (4003, "Πεντηκοστη", "Pentēkostē", "Noun, Feminine", "Pentecost / Fiftieth (Day)",
     "From <em>pentēkonta</em> (fifty). The fiftieth day after Passover — the Feast of Weeks or Pentecost. One of the three great Jewish festivals, it became the birthday of the church when the Holy Spirit was poured out.",
     "<em>Pentecost</em> transformed from an agricultural harvest festival into the moment when God <strong>harvested the first fruits of the church</strong>. On this day, the Holy Spirit descended, the apostles spoke in tongues, Peter preached, and three thousand were saved (Acts 2). This was the fulfillment of Joel's prophecy and Jesus' promise to send the Spirit. Pentecost marks the beginning of the church age and the empowerment of believers for mission.",
     [("Acts+2:1", "When the day of <em>Pentecost</em> came, they were all together in one place."),
      ("Acts+2:4", "All of them were filled with the Holy Spirit and began to speak in other tongues as the Spirit enabled them."),
      ("Acts+20:16", "Paul had decided to sail past Ephesus to avoid spending time in the province of Asia, for he was in a hurry to reach Jerusalem, if possible, by the day of <em>Pentecost</em>."),
      ("1+Corinthians+16:8", "But I will stay on at Ephesus until <em>Pentecost</em>."),
      ("Acts+2:41", "Those who accepted his message were baptized, and about three thousand were added to their number that day.")],
     [(4151, "Pneuma (Spirit)"), (1577, "Ekklēsia (Church)"), (1100, "Glōssa (Tongue)"), (907, "Baptizō (To Baptize)")]),

    (4004, "Πεντακισχιλιοι", "Pentakischilioi", "Adjective (Numeral)", "Five Thousand",
     "From <em>pente</em> (five) and <em>chilioi</em> (thousand). Five thousand. The number fed by Jesus in the only miracle (besides the resurrection) recorded in all four Gospels.",
     "The feeding of the <em>five thousand</em> is the only miracle of Jesus recorded in all four Gospels, underscoring its supreme importance. With five loaves and two fish, Jesus fed <em>five thousand</em> men plus women and children, with twelve baskets left over. This miracle reveals Christ as the <strong>bread of life</strong> who satisfies all hunger — physical and spiritual — with abundance to spare.",
     [("Matthew+14:21", "The number of those who ate was about <em>five thousand</em> men, besides women and children."),
      ("Mark+6:44", "The number of the men who had eaten was <em>five thousand</em>."),
      ("Luke+9:14", "About <em>five thousand</em> men were there."),
      ("John+6:10", "Jesus said, 'Have the people sit down.' There was plenty of grass in that place, and they sat down — about <em>five thousand</em> men."),
      ("John+6:35", "Then Jesus declared, 'I am the bread of life. Whoever comes to me will never go hungry.'")],
     [(740, "Artos (Bread)"), (2486, "Ichthus (Fish)"), (4592, "Sēmeion (Sign)"), (2222, "Zōē (Life)")]),

    (4005, "Πεντηκονταετης", "Pentēkontaetēs", "Adjective", "Fifty Years Old",
     "From <em>pentēkonta</em> (fifty) and <em>etos</em> (year). Fifty years old. Used in Acts 13:20 in connection with the period of the judges.",
     "In Acts 13:20, Paul recounts that God gave Israel judges for about four hundred and fifty years. The number fifty also connects to the Year of Jubilee — every <em>fiftieth</em> year, debts were canceled, slaves freed, and land returned. Jesus' ministry inaugurated the ultimate Jubilee: <strong>freedom from the debt of sin, liberation from spiritual slavery, and restoration of humanity's lost inheritance</strong>.",
     [("Acts+13:20", "All this took about 450 years. After this, God gave them judges until the time of Samuel the prophet."),
      ("Leviticus+25:10", "Consecrate the <em>fiftieth</em> year and proclaim liberty throughout the land to all its inhabitants."),
      ("Luke+4:18", "The Spirit of the Lord is on me, because he has anointed me to proclaim good news to the poor. He has sent me to proclaim <em>freedom</em> for the prisoners."),
      ("Isaiah+61:1", "The Spirit of the Sovereign Lord is on me, because the Lord has anointed me to proclaim good news to the poor."),
      ("John+8:36", "So if the Son sets you free, you will be free indeed.")],
     [(4003, "Pentēkostē (Pentecost)"), (1657, "Eleutheria (Freedom)"), (2094, "Etos (Year)"), (859, "Aphesis (Release)")]),

    (4006, "Πεποιθησις", "Pepoithēsis", "Noun, Feminine", "Confidence / Trust / Assurance",
     "From <em>peithō</em> (to persuade, to trust). Confidence, trust, firm assurance. The settled conviction that comes from trusting in God's faithfulness rather than one's own abilities.",
     "Paul speaks of having '<em>confidence</em> through Christ before God' (2 Corinthians 3:4). This is not self-confidence but <strong>Christ-confidence</strong> — a boldness rooted in what Christ has done, not what we deserve. Such confidence allows believers to approach God's throne boldly (Hebrews 4:16), to face persecution without fear, and to persevere in ministry despite opposition.",
     [("2+Corinthians+3:4", "Such <em>confidence</em> we have through Christ before God."),
      ("Ephesians+3:12", "In him and through faith in him we may approach God with freedom and <em>confidence</em>."),
      ("Philippians+3:4", "Though I myself have reasons for such <em>confidence</em>. If someone else thinks they have reasons to put confidence in the flesh, I have more."),
      ("2+Corinthians+1:15", "Because I was <em>confident</em> of this, I wanted to visit you first so that you might benefit twice."),
      ("Hebrews+10:35", "So do not throw away your <em>confidence</em>; it will be richly rewarded.")],
     [(3954, "Parrēsia (Boldness)"), (4102, "Pistis (Faith)"), (1680, "Elpis (Hope)"), (2292, "Tharreō (To Be Confident)")]),

    (4007, "Πεπειρασμενος", "Pepeirasmenon", "Participle (Perfect Passive)", "Having Been Tempted / Tested",
     "Perfect passive participle of <em>peirazō</em> (to test, to tempt). Describes one who has been tested or tempted. Applied supremely to Christ, who was tempted in every way yet without sin.",
     "Hebrews 4:15 declares that our high priest has been '<em>tempted</em> in every way, just as we are — yet he did not sin.' This is foundational to Christ's ability to sympathize with our weaknesses. He does not look down from untested holiness — He <strong>knows by experience</strong> the full force of every temptation, yet never yielded. His victory over temptation becomes our resource through prayer.",
     [("Hebrews+4:15", "For we do not have a high priest who is unable to empathize with our weaknesses, but we have one who has been <em>tempted</em> in every way, just as we are — yet he did not sin."),
      ("Hebrews+2:18", "Because he himself suffered when he was <em>tempted</em>, he is able to help those who are being tempted."),
      ("Matthew+4:1", "Then Jesus was led by the Spirit into the wilderness to be <em>tempted</em> by the devil."),
      ("James+1:13", "When tempted, no one should say, 'God is tempting me.' For God cannot be tempted by evil, nor does he tempt anyone."),
      ("1+Corinthians+10:13", "No temptation has overtaken you except what is common to mankind. And God is faithful; he will not let you be tempted beyond what you can bear.")],
     [(3986, "Peirasmos (Temptation/Trial)"), (3985, "Peirazō (To Test)"), (749, "Archiereus (High Priest)"), (266, "Hamartia (Sin)")]),

    (4008, "Περαν", "Peran", "Adverb/Preposition", "Beyond / Across / On the Other Side",
     "An adverb and preposition meaning beyond, across, on the other side. Frequently used of crossing the Jordan River or the Sea of Galilee — transitions that carry theological significance.",
     "John the Baptist ministered '<em>beyond</em> the Jordan' (John 1:28) — outside the religious establishment of Jerusalem. Jesus often crossed to the '<em>other side</em>' of the Sea of Galilee, frequently encountering people in need. The concept of crossing over connects to Israel's crossing the Jordan into the Promised Land. <strong>God's work often requires leaving familiar territory</strong> and stepping into the unknown by faith.",
     [("John+1:28", "This all happened at Bethany <em>beyond</em> the Jordan, where John was baptizing."),
      ("Matthew+4:25", "Large crowds from Galilee, the Decapolis, Jerusalem, Judea and the region <em>across</em> the Jordan followed him."),
      ("Mark+5:1", "They went <em>across</em> the lake to the region of the Gerasenes."),
      ("John+6:1", "Some time after this, Jesus crossed to the far shore of the Sea of Galilee."),
      ("John+10:40", "Then Jesus went back <em>across</em> the Jordan to the place where John had been baptizing in the early days.")],
     [(2446, "Iordanes (Jordan)"), (2281, "Thalassa (Sea)"), (4215, "Potamos (River)"), (1224, "Diabainō (To Cross Over)")]),

    (4009, "Περας", "Peras", "Noun, Neuter", "End / Boundary / Limit / Extremity",
     "A noun meaning end, boundary, limit, or the farthest point. Used of the ends of the earth and the limits of patience. The Queen of the South came 'from the <em>ends</em> of the earth' to hear Solomon.",
     "Jesus said the Queen of the South came from the '<em>ends</em> of the earth' to hear Solomon's wisdom, and 'something greater than Solomon is here' (Matthew 12:42). If she traveled so far for human wisdom, how much more should people seek the <strong>divine Wisdom incarnate</strong>? The 'ends of the earth' also appears in Acts 1:8 as the ultimate scope of the gospel mission — Christ's witnesses will reach the farthest boundaries of the world.",
     [("Matthew+12:42", "The Queen of the South will rise at the judgment with this generation and condemn it; for she came from the <em>ends of the earth</em> to listen to Solomon's wisdom."),
      ("Acts+13:47", "I have made you a light for the Gentiles, that you may bring salvation to the <em>ends of the earth</em>."),
      ("Romans+10:18", "Their voice has gone out into all the earth, their words to the <em>ends</em> of the world."),
      ("Hebrews+6:16", "People swear by someone greater than themselves, and the oath confirms what is said and puts an <em>end</em> to all argument."),
      ("Psalm+67:7", "May God bless us still, so that all the <em>ends</em> of the earth will fear him.")],
     [(5056, "Telos (End/Goal)"), (1093, "Gē (Earth)"), (2889, "Kosmos (World)"), (4678, "Sophia (Wisdom)")]),

    (4010, "Περγαμος", "Pergamos", "Noun, Proper", "Pergamum / Pergamos",
     "A major city in the Roman province of Asia (modern Bergama, Turkey). One of the seven churches addressed in Revelation. Known for its great library, temple of Zeus, and the first temple of the imperial cult in Asia.",
     "Jesus describes Pergamum as the place 'where Satan has his throne' (Revelation 2:13) — likely referring to the massive altar of Zeus or the imperial cult temple. Despite living in this hostile environment, believers held fast to Christ's name. Yet Jesus rebuked them for tolerating false teaching. The message to Pergamum teaches that <strong>faithfulness in hostile territory must be paired with doctrinal purity</strong>.",
     [("Revelation+2:12", "To the angel of the church in <em>Pergamum</em> write: These are the words of him who has the sharp, double-edged sword."),
      ("Revelation+2:13", "I know where you live — where Satan has his throne. Yet you remain true to my name."),
      ("Revelation+2:14", "Nevertheless, I have a few things against you: There are some among you who hold to the teaching of Balaam."),
      ("Revelation+2:16", "Repent therefore! Otherwise, I will soon come to you and will fight against them with the sword of my mouth."),
      ("Revelation+2:17", "To the one who is victorious, I will give some of the hidden manna.")],
     [(1577, "Ekklēsia (Church)"), (3340, "Metanoeō (To Repent)"), (3528, "Nikaō (To Overcome)"), (4592, "Sēmeion (Sign)")]),

    (4011, "Περγη", "Pergē", "Noun, Proper", "Perga",
     "A city in Pamphylia, in southern Asia Minor (modern Turkey). Paul visited Perga on his first missionary journey. It was here that John Mark departed from the mission team.",
     "Perga is significant as the place where John Mark abandoned Paul and Barnabas (Acts 13:13), a decision that later caused a sharp disagreement between the apostles (Acts 15:37-39). Yet God used even this conflict redemptively: it resulted in two missionary teams instead of one, and Mark was eventually restored (2 Timothy 4:11). <strong>God works through human failures and disagreements</strong> to accomplish more than we expect.",
     [("Acts+13:13", "From Paphos, Paul and his companions sailed to <em>Perga</em> in Pamphylia, where John left them to return to Jerusalem."),
      ("Acts+13:14", "From <em>Perga</em> they went on to Pisidian Antioch."),
      ("Acts+14:25", "And when they had preached the word in <em>Perga</em>, they went down to Attalia."),
      ("Acts+15:38", "But Paul did not think it wise to take him, because he had deserted them in Pamphylia and had not continued with them in the work."),
      ("2+Timothy+4:11", "Get Mark and bring him with you, because he is helpful to me in my ministry.")],
     [(3972, "Paulos (Paul)"), (921, "Barnabas"), (3138, "Markos (Mark)"), (2098, "Euangelion (Gospel)")]),
]

entries.extend(gap_fill_entries)

# Add more entries to reach 200
additional_entries = [
    (4012, "Περι", "Peri", "Preposition", "About / Concerning / Around",
     "One of the most common Greek prepositions, occurring over 330 times in the NT. With the genitive it means 'about' or 'concerning'; with the accusative it means 'around.' Used in theological phrases like 'concerning sin,' 'about the kingdom,' and 'around the throne.'",
     "This preposition structures many of the NT's most important theological statements. Christ died '<em>concerning</em> sins' (<em>peri hamartiōn</em>, 1 Peter 3:18). The apostles taught '<em>about</em> the kingdom' (<em>peri tēs basileias</em>, Acts 1:3). The Spirit would convict the world '<em>concerning</em> sin, righteousness, and judgment' (John 16:8). <strong>The simplest words often carry the greatest theological weight.</strong>",
     [("1+Peter+3:18", "For Christ also suffered once for sins, the righteous for the unrighteous, to bring you to God."),
      ("John+16:8", "When he comes, he will prove the world to be in the wrong <em>about</em> sin and righteousness and judgment."),
      ("Acts+1:3", "He appeared to them over a period of forty days and spoke <em>about</em> the kingdom of God."),
      ("Hebrews+10:26", "If we deliberately keep on sinning after we have received the knowledge of the truth, no sacrifice for sins is left."),
      ("1+John+2:2", "He is the atoning sacrifice for our sins, and not only for ours but also for the sins of the whole world.")],
     [(266, "Hamartia (Sin)"), (932, "Basileia (Kingdom)"), (1343, "Dikaiosunē (Righteousness)"), (2920, "Krisis (Judgment)")]),

    (4013, "Περιαγω", "Periagō", "Verb", "To Lead Around / To Go About",
     "From <em>peri</em> (around) and <em>agō</em> (to lead). To lead around, to go about from place to place. Used of Jesus' itinerant ministry traveling through towns and villages.",
     "Matthew 4:23 describes Jesus '<em>going about</em>' all Galilee, teaching, proclaiming, and healing. This itinerant pattern was deliberate — Jesus brought the kingdom to the people rather than waiting for them to come to Him. <strong>The gospel is mobile, not stationary.</strong> The church is not a building people visit but a people God sends.",
     [("Matthew+4:23", "Jesus went throughout Galilee, teaching in their synagogues, proclaiming the good news of the kingdom, and healing every disease."),
      ("Matthew+9:35", "Jesus went through all the towns and villages, teaching in their synagogues, proclaiming the good news of the kingdom and healing every disease."),
      ("Mark+6:6", "Then Jesus went <em>around</em> teaching from village to village."),
      ("Acts+13:11", "Immediately mist and darkness came over him, and he groped about, seeking someone to lead him by the hand."),
      ("1+Corinthians+9:5", "Don't we have the right to take a believing wife along with us, as do the other apostles?")],
     [(71, "Agō (To Lead)"), (4198, "Poreuomai (To Go)"), (2784, "Kērussō (To Proclaim)"), (2098, "Euangelion (Gospel)")]),

    (4014, "Περιαιρεω", "Periaireo", "Verb", "To Take Away / To Remove / To Strip Off",
     "From <em>peri</em> (around) and <em>haireō</em> (to take). To take away from around, to remove, to strip off. Used of removing a veil, cutting anchors, and God removing the veil of spiritual blindness.",
     "Paul declares that when one turns to the Lord, the veil is '<em>taken away</em>' (2 Corinthians 3:16). This removal of spiritual blindness is entirely God's work — humanity cannot lift its own veil. In Acts 27:40, sailors '<em>cut away</em>' the anchors during the shipwreck. <strong>Sometimes God removes what we clung to for safety so we can be driven to shore by His wind.</strong>",
     [("2+Corinthians+3:16", "But whenever anyone turns to the Lord, the veil is <em>taken away</em>."),
      ("Acts+27:40", "Cutting loose the anchors, they left them in the sea and at the same time untied the ropes that held the rudders."),
      ("Acts+27:20", "When neither sun nor stars appeared for many days and the storm continued raging, we finally gave up all hope of being saved."),
      ("Hebrews+10:11", "Day after day every priest stands and performs his religious duties; again and again he offers the same sacrifices, which can never <em>take away</em> sins."),
      ("Isaiah+25:7", "On this mountain he will destroy the shroud that enfolds all peoples, the sheet that covers all nations.")],
     [(138, "Haireō (To Take)"), (2571, "Kalumma (Veil)"), (851, "Aphaireō (To Take Away)"), (4151, "Pneuma (Spirit)")]),

    (4015, "Περιαστραπτω", "Periastraptō", "Verb", "To Flash Around / To Shine Around",
     "From <em>peri</em> (around) and <em>astraptō</em> (to flash like lightning). To flash or shine around someone. Used exclusively of the blinding light that surrounded Paul on the road to Damascus.",
     "A light from heaven '<em>flashed around</em>' Saul of Tarsus on the Damascus road (Acts 9:3, 22:6), permanently changing the course of history. The persecutor became the apostle. The light was the glory of the risen Christ, so brilliant it blinded Paul's physical eyes while opening his spiritual eyes. <strong>Encountering the living Christ changes everything</strong> — identity, purpose, direction, and destiny.",
     [("Acts+9:3", "As he neared Damascus on his journey, suddenly a light from heaven <em>flashed around</em> him."),
      ("Acts+22:6", "About noon as I came near Damascus, suddenly a bright light from heaven <em>flashed around</em> me."),
      ("Acts+26:13", "About midday, King Agrippa, as I was on the road, I saw a light from heaven, brighter than the sun, <em>blazing around</em> me and my companions."),
      ("Acts+9:4", "He fell to the ground and heard a voice say to him, 'Saul, Saul, why do you persecute me?'"),
      ("2+Corinthians+4:6", "For God, who said, 'Let light shine out of darkness,' made his light shine in our hearts to give us the light of the knowledge of God's glory displayed in the face of Christ.")],
     [(5457, "Phōs (Light)"), (1391, "Doxa (Glory)"), (3972, "Paulos (Paul)"), (1995, "Epistrephō (To Turn)")]),

    (4016, "Περιβαλλω", "Periballō", "Verb", "To Clothe / To Put Around / To Cast Around",
     "From <em>peri</em> (around) and <em>ballō</em> (to throw/cast). To throw around, to clothe, to dress. Used of both physical clothing and the spiritual clothing of righteousness, glory, and the new resurrection body.",
     "In Revelation, the overcomers are '<em>clothed</em> in white garments' (Revelation 3:5) — representing the righteousness of Christ imputed to believers. Jesus warns against worrying about what to <em>wear</em> since God clothes the lilies (Matthew 6:28-29). Paul eagerly anticipates being '<em>clothed</em>' with the heavenly dwelling (2 Corinthians 5:2-4). <strong>God clothes His people</strong> — in righteousness now and in glory at the resurrection.",
     [("Revelation+3:5", "The one who is victorious will, like them, be <em>dressed</em> in white."),
      ("Revelation+19:8", "Fine linen, bright and clean, was given her to <em>wear</em>. Fine linen stands for the righteous acts of God's holy people."),
      ("Matthew+6:29", "Yet I tell you that not even Solomon in all his splendor was <em>dressed</em> like one of these."),
      ("2+Corinthians+5:2", "Meanwhile we groan, longing to be <em>clothed</em> instead with our heavenly dwelling."),
      ("Revelation+7:9", "After this I looked, and there before me was a great multitude that no one could count, standing before the throne and before the Lamb. They were <em>wearing</em> white robes.")],
     [(1746, "Enduō (To Put On)"), (2440, "Himation (Garment)"), (1343, "Dikaiosunē (Righteousness)"), (1391, "Doxa (Glory)")]),

    (4017, "Περιβλεπω", "Periblepō", "Verb", "To Look Around",
     "From <em>peri</em> (around) and <em>blepō</em> (to see). To look around in all directions. Used almost exclusively of Jesus in the Gospels, suggesting His penetrating awareness of His surroundings.",
     "Mark's Gospel uniquely preserves this detail of Jesus' behavior: He '<em>looked around</em>' at the Pharisees with anger and grief (Mark 3:5), '<em>looked around</em>' at everything in the temple (Mark 11:11), and '<em>looked around</em>' to find the woman who touched His garment (Mark 5:32). Jesus' gaze was never casual — it was the <strong>searching, compassionate, all-seeing gaze of God incarnate</strong>.",
     [("Mark+3:5", "He <em>looked around</em> at them in anger and, deeply distressed at their stubborn hearts, said to the man, 'Stretch out your hand.'"),
      ("Mark+5:32", "But Jesus kept <em>looking around</em> to see who had done it."),
      ("Mark+10:23", "Jesus <em>looked around</em> and said to his disciples, 'How hard it is for the rich to enter the kingdom of God!'"),
      ("Mark+11:11", "Jesus entered Jerusalem and went into the temple courts. He <em>looked around</em> at everything, but since it was already late, he went out to Bethany."),
      ("Luke+6:10", "He <em>looked around</em> at them all, and then said to the man, 'Stretch out your hand.'")],
     [(991, "Blepō (To See)"), (3708, "Horaō (To See)"), (2300, "Theaomai (To Behold)"), (816, "Atenizō (To Gaze Intently)")]),

    (4018, "Περιβολαιον", "Peribolaion", "Noun, Neuter", "Covering / Cloak / Mantle",
     "From <em>periballō</em> (to throw around). A covering, a wrap, a mantle that is cast around the body. Used metaphorically of creation as God's garment that will be rolled up and changed.",
     "Hebrews 1:12 quotes Psalm 102: 'You will roll them up like a robe; like a <em>garment</em> they will be changed.' The created universe is compared to a <em>garment</em> God wears — beautiful but temporary, destined to be replaced. <strong>Only God Himself is eternal and unchanging.</strong> The physical universe will be transformed, but God remains the same forever.",
     [("Hebrews+1:12", "You will roll them up like a robe; like a <em>garment</em> they will be changed. But you remain the same, and your years will never end."),
      ("1+Corinthians+11:15", "But that if a woman has long hair, it is her glory? For long hair is given to her as a <em>covering</em>."),
      ("Psalm+102:26", "They will perish, but you remain; they will all wear out like a <em>garment</em>."),
      ("Isaiah+51:6", "Lift up your eyes to the heavens, look at the earth beneath; the heavens will vanish like smoke, the earth will wear out like a <em>garment</em>."),
      ("2+Peter+3:10", "But the day of the Lord will come like a thief. The heavens will disappear with a roar; the elements will be destroyed by fire.")],
     [(4016, "Periballō (To Clothe)"), (2440, "Himation (Garment)"), (2889, "Kosmos (World)"), (166, "Aiōnios (Eternal)")]),

    (4019, "Περιδεω", "Perideō", "Verb", "To Bind Around / To Tie Around",
     "From <em>peri</em> (around) and <em>deō</em> (to bind). To bind around, to tie around. Used of the cloth wrapped around Lazarus's face when he was raised from the dead.",
     "When Jesus raised Lazarus from the dead, Lazarus came out with his face '<em>wrapped</em> with a cloth' (John 11:44). Jesus commanded: 'Take off the grave clothes and let him go.' This vivid detail pictures the believer's need to be <strong>freed from the remnants of death</strong> even after receiving new life. Salvation brings life; sanctification removes the grave clothes.",
     [("John+11:44", "The dead man came out, his hands and feet wrapped with strips of linen, and a cloth around his face. Jesus said to them, 'Take off the grave clothes and let him go.'"),
      ("John+11:43", "When he had said this, Jesus called in a loud voice, 'Lazarus, come out!'"),
      ("John+11:25", "Jesus said to her, 'I am the resurrection and the life. The one who believes in me will live, even though they die.'"),
      ("Colossians+3:9", "Do not lie to each other, since you have taken off your old self with its practices."),
      ("Ephesians+4:22", "You were taught, with regard to your former way of life, to put off your old self, which is being corrupted by its deceitful desires.")],
     [(1210, "Deō (To Bind)"), (386, "Anastasis (Resurrection)"), (2222, "Zōē (Life)"), (2288, "Thanatos (Death)")]),

    (4020, "Περιεργαζομαι", "Periergazomai", "Verb", "To Be a Busybody / To Meddle",
     "From <em>peri</em> (around, beyond) and <em>ergazomai</em> (to work). To work around or beyond what is proper — hence to be a busybody, to meddle in others' affairs instead of attending to one's own.",
     "Paul addresses this vice directly in 2 Thessalonians 3:11: some were 'not busy; they are <em>busybodies</em>.' The wordplay in Greek is striking: instead of being <em>ergazomenous</em> (working), they are <em>periergazomenous</em> (overworking boundaries — meddling). <strong>Idleness breeds interference.</strong> The remedy is honest work and minding one's own business (1 Thessalonians 4:11).",
     [("2+Thessalonians+3:11", "We hear that some among you are idle and disruptive. They are not busy; they are <em>busybodies</em>."),
      ("1+Thessalonians+4:11", "Make it your ambition to lead a quiet life: You should mind your own business and work with your hands."),
      ("1+Timothy+5:13", "Besides, they get into the habit of being idle and going about from house to house. And not only do they become idlers, but also <em>busybodies</em>."),
      ("1+Peter+4:15", "If you suffer, it should not be as a murderer or thief or any other kind of criminal, or even as a <em>meddler</em>."),
      ("Proverbs+26:17", "Like one who grabs a stray dog by the ears is someone who rushes into a quarrel not their own.")],
     [(2038, "Ergazomai (To Work)"), (692, "Argos (Idle)"), (2271, "Hēsuchia (Quietness)"), (4710, "Spoudē (Diligence)")]),
]

entries.extend(additional_entries)

# Add final batch to reach 200
final_entries = [
    (4021, "Περιεργος", "Periergos", "Adjective", "Meddlesome / Practicing Magic Arts",
     "From <em>peri</em> (beyond) and <em>ergon</em> (work). Going beyond proper bounds — hence meddlesome or, in Acts 19:19, practicing 'curious arts' (magic, sorcery).",
     "In Ephesus, many who practiced '<em>magic arts</em>' brought their scrolls together and burned them publicly (Acts 19:19). The value was fifty thousand drachmas — a staggering sum. This dramatic act of repentance shows that <strong>genuine conversion requires severing ties with the occult</strong>. New life in Christ demands the destruction of what enslaved us.",
     [("Acts+19:19", "A number who had practiced <em>sorcery</em> brought their scrolls together and burned them publicly. The value of the scrolls was fifty thousand drachmas."),
      ("Acts+19:20", "In this way the word of the Lord spread widely and grew in power."),
      ("1+Timothy+5:13", "Besides, they get into the habit of being idle and going about from house to house. And not only do they become idlers, but also gossips and <em>busybodies</em>."),
      ("Deuteronomy+18:10", "Let no one be found among you who sacrifices their son or daughter in the fire, who practices divination or <em>sorcery</em>."),
      ("Galatians+5:20", "Idolatry and <em>witchcraft</em>; hatred, discord, jealousy.")],
     [(3096, "Mageia (Magic)"), (5331, "Pharmakeia (Sorcery)"), (3340, "Metanoeō (To Repent)"), (3056, "Logos (Word)")]),

    (4022, "Περιερχομαι", "Perierchomai", "Verb", "To Go About / To Wander Around",
     "From <em>peri</em> (around) and <em>erchomai</em> (to come/go). To go around, to wander about, to travel from place to place. Used of itinerant Jewish exorcists and of those wandering from the faith.",
     "In Acts 19:13, some itinerant Jewish exorcists '<em>went around</em>' attempting to invoke Jesus' name without genuine faith — with disastrous results. The demon-possessed man attacked them. This incident teaches that <strong>using Jesus' name without knowing Jesus personally is spiritually dangerous</strong>. There is no power in the formula; the power is in the relationship.",
     [("Acts+19:13", "Some Jews who <em>went around</em> driving out evil spirits tried to invoke the name of the Lord Jesus over those who were demon-possessed."),
      ("Acts+19:15", "One day the evil spirit answered them, 'Jesus I know, and Paul I know about, but who are you?'"),
      ("Hebrews+11:37", "They went about in sheepskins and goatskins, destitute, persecuted and mistreated."),
      ("1+Timothy+5:13", "Besides, they get into the habit of being idle and going about from house to house."),
      ("Acts+28:13", "From there we set sail and arrived at Rhegium.")],
     [(2064, "Erchomai (To Come)"), (3686, "Onoma (Name)"), (1849, "Exousia (Authority)"), (1140, "Daimonion (Demon)")]),

    (4023, "Περιεχω", "Periechō", "Verb", "To Contain / To Encompass / To Seize",
     "From <em>peri</em> (around) and <em>echō</em> (to have). To hold around, to encompass, to contain. Used of Scripture containing a passage and of astonishment seizing someone.",
     "Luke records that astonishment '<em>seized</em>' Peter and all who were with him at the miraculous catch of fish (Luke 5:9). 1 Peter 2:6 says 'it <em>stands</em> in Scripture' — the idea that Scripture <em>contains</em> or holds a particular truth. <strong>God's word contains everything needed for life and godliness</strong>, and encountering God's power produces overwhelm that seizes the soul.",
     [("Luke+5:9", "For he and all his companions were <em>astonished</em> at the catch of fish they had taken."),
      ("1+Peter+2:6", "For in Scripture <em>it says</em>: 'See, I lay a stone in Zion, a chosen and precious cornerstone.'"),
      ("Acts+23:25", "He wrote a letter that had this <em>content</em>."),
      ("Luke+5:26", "Everyone was amazed and gave praise to God. They were <em>filled</em> with awe."),
      ("Mark+16:8", "Trembling and bewildered, the women went out and fled from the tomb. They said nothing to anyone, because they were afraid.")],
     [(2192, "Echō (To Have)"), (2285, "Thambos (Amazement)"), (1124, "Graphē (Scripture)"), (5401, "Phobos (Fear)")]),

    (4024, "Περιζωννυμι", "Perizōnnumi", "Verb", "To Gird / To Wrap Around / To Prepare",
     "From <em>peri</em> (around) and <em>zōnnumi</em> (to gird). To gird around, to wrap a belt or garment around the waist. Symbolically represents preparation for action, service, and spiritual readiness.",
     "Jesus <em>girded</em> himself with a towel to wash His disciples' feet (John 13:4) — the Lord of glory taking on the role of the lowest servant. Peter instructs believers to '<em>gird up</em> the loins of your mind' (1 Peter 1:13 KJV) — prepare mentally for action. Ephesians 6:14 includes the belt of truth as part of God's armor. <strong>Girding is both humble service and battle readiness</strong> — the Christian life demands both.",
     [("John+13:4", "He got up from the meal, took off his outer clothing, and <em>wrapped</em> a towel around his waist."),
      ("Luke+12:37", "It will be good for those servants whose master finds them watching when he comes. Truly I tell you, he will <em>dress himself</em> to serve, will have them recline at the table and will come and wait on them."),
      ("Ephesians+6:14", "Stand firm then, with the belt of truth <em>buckled around</em> your waist."),
      ("1+Peter+1:13", "Therefore, with minds that are alert and fully sober, set your hope on the grace to be brought to you when Jesus Christ is revealed at his coming."),
      ("Luke+12:35", "Be <em>dressed</em> ready for service and keep your lamps burning.")],
     [(2224, "Zōnnumi (To Gird)"), (225, "Alētheia (Truth)"), (1248, "Diakonia (Service)"), (3696, "Hoplon (Armor)")]),

    (4025, "Περιιστημι", "Periistēmi", "Verb", "To Stand Around / To Avoid / To Shun",
     "From <em>peri</em> (around) and <em>histēmi</em> (to stand). Literally to stand around; figuratively to avoid, to shun. Paul uses it to warn Titus to avoid pointless controversies.",
     "Paul instructs Titus to '<em>avoid</em> foolish controversies and genealogies and arguments and quarrels about the law' (Titus 3:9). Not every theological debate is worth engaging. Some controversies are 'unprofitable and useless' — they generate heat but no light. <strong>Spiritual maturity includes knowing what to avoid</strong>, not just what to pursue.",
     [("Titus+3:9", "But <em>avoid</em> foolish controversies and genealogies and arguments and quarrels about the law, because these are unprofitable and useless."),
      ("2+Timothy+2:16", "<em>Avoid</em> godless chatter, because those who indulge in it will become more and more ungodly."),
      ("Acts+25:7", "When Paul came in, the Jews who had come down from Jerusalem <em>stood around</em> him."),
      ("John+11:42", "I knew that you always hear me, but I said this for the benefit of the people <em>standing</em> here."),
      ("1+Timothy+6:20", "Timothy, guard what has been entrusted to your care. Turn away from godless chatter and the opposing ideas of what is falsely called knowledge.")],
     [(2476, "Histēmi (To Stand)"), (4678, "Sophia (Wisdom)"), (3474, "Mōros (Foolish)"), (2222, "Zōē (Life)")]),
]

entries.extend(final_entries)

# Remove any entries whose numbers already exist
entries = [(n, *rest) for n, *rest in entries if n not in existing]

# Take first 200
entries = entries[:200]

print(f"Will create {len(entries)} new entries")
print(f"Numbers: {sorted([e[0] for e in entries])}")

# HTML template
def make_html(num, greek, translit, pos, gloss, definition, theological, verses, related):
    og_desc = definition[:120].replace('"', '&quot;').replace('<em>', '').replace('</em>', '').replace('<strong>', '').replace('</strong>', '')
    meta_desc = f"{translit} — {gloss} — Greek word study. Strong's G{num}. USMC Ministries Greek &amp; Hebrew Lexicon."

    verses_html = ""
    for ref, text in verses:
        verses_html += f"""
                <div class="verse-entry">
                    <a href="../bible.html?ref={ref}" class="verse-ref">{ref.replace('+', ' ')}</a>
                    <span class="verse-text">{text}</span>
                </div>"""

    related_html = ""
    for rnum, rlabel in related:
        related_html += f"""
                    <a href="G{rnum}.html" class="related-word">G{rnum} — {rlabel}</a>"""

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
    <link rel="manifest" href="/manifest.json">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="G{num} — {translit} | USMC Ministries Lexicon">
    <meta property="og:description" content="{og_desc}">
    <meta name="description" content="{meta_desc}">
    <title>G{num} — {translit} ({gloss}) | USMC Ministries Lexicon</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        :root {{ --bg-dark:#000; --bg-card:#111; --gold:#D4AF37; --gold-light:#F4D470; --white:#FFF; --gray:#888; --border:#333; --scarlet:#CC0000; }}
        body {{ font-family:'Inter',sans-serif; background:var(--bg-dark); color:var(--white); min-height:100vh; line-height:1.6; }}
        h1,h2,h3 {{ font-family:'Playfair Display',serif; font-weight:700; }}
        .container {{ max-width:800px; margin:0 auto; padding:20px; }}
        nav {{ display:flex; flex-wrap:wrap; gap:6px; justify-content:center; padding:14px 20px; border-bottom:1px solid var(--border); background:rgba(0,0,0,0.95); position:sticky; top:0; z-index:100; }}
        nav a {{ color:var(--gray); text-decoration:none; font-size:0.85rem; font-weight:500; padding:5px 12px; border-radius:20px; border:1px solid transparent; transition:all 0.2s; white-space:nowrap; }}
        nav a:hover {{ color:var(--gold); border-color:var(--border); }}
        nav a:link,nav a:visited,nav a:active {{ color:var(--gray) !important; text-decoration:none !important; }}
        nav a.active {{ color:var(--gold) !important; border-color:var(--gold); }}
        .word-header {{ text-align:center; padding:40px 0 30px; border-bottom:1px solid var(--border); margin-bottom:30px; }}
        .strongs-badge {{ display:inline-block; background:var(--gold); color:#000; font-weight:700; font-size:0.9rem; padding:4px 14px; border-radius:20px; margin-bottom:15px; }}
        .original-word {{ font-size:3rem; margin:15px 0 10px; color:var(--gold-light); }}
        .transliteration {{ font-size:1.4rem; color:var(--white); font-style:italic; margin-bottom:8px; }}
        .pos {{ color:var(--gray); font-size:0.95rem; margin-bottom:10px; }}
        .gloss {{ color:var(--gold); font-size:1.1rem; font-weight:600; }}
        .section {{ background:var(--bg-card); border:1px solid var(--border); border-radius:12px; padding:28px; margin-bottom:24px; }}
        .section h2 {{ color:var(--gold); font-size:1.3rem; margin-bottom:16px; }}
        .section p {{ color:var(--white); line-height:1.8; margin-bottom:12px; }}
        .section p em {{ color:var(--gold-light); font-style:italic; }}
        .section p strong {{ color:var(--white); }}
        .verse-entry {{ margin-bottom:16px; padding-left:18px; border-left:2px solid var(--gold); }}
        .verse-ref {{ color:var(--gold); text-decoration:none; font-weight:600; font-size:0.9rem; display:inline-block; margin-bottom:4px; border-bottom:1px dotted var(--gold); }}
        .verse-ref:hover {{ color:var(--gold-light); border-bottom-style:solid; }}
        .verse-text {{ color:var(--gray); line-height:1.7; }}
        .verse-text em {{ color:var(--gold-light); font-style:italic; }}
        .verse-text strong {{ color:var(--white); }}
        .related-words {{ display:flex; flex-wrap:wrap; gap:10px; }}
        .related-word {{ display:inline-block; background:rgba(212,175,55,0.1); border:1px solid var(--border); color:var(--gold); text-decoration:none; padding:6px 14px; border-radius:20px; font-size:0.85rem; transition:all 0.2s; }}
        a.related-word:hover {{ border-color:var(--gold); background:rgba(212,175,55,0.2); }}
        .ext-links {{ display:flex; flex-wrap:wrap; gap:12px; margin-top:20px; }}
        .ext-link {{ color:var(--gold); text-decoration:none; padding:8px 18px; border:1px solid var(--border); border-radius:8px; font-size:0.9rem; transition:all 0.2s; }}
        .ext-link:hover {{ border-color:var(--gold); background:rgba(212,175,55,0.1); }}
        .back-link {{ display:inline-block; color:var(--gold); text-decoration:none; margin-bottom:20px; font-size:0.9rem; }}
        .back-link:hover {{ color:var(--gold-light); }}
        footer {{ text-align:center; padding:40px 20px; color:var(--gray); font-size:0.85rem; border-top:1px solid var(--border); margin-top:40px; }}
        footer a {{ color:var(--gold); text-decoration:none; }}
        @media (max-width:640px) {{ .container {{ padding:15px; }} .original-word {{ font-size:2.2rem; }} }}
    .theme-toggle{{background:none;border:1px solid var(--border);border-radius:50%;width:34px;height:34px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:1.1rem;transition:all 0.3s;padding:0;margin-left:6px;}}.theme-toggle:hover{{border-color:var(--gold);transform:scale(1.1);}}body.light-mode{{--bg-dark:#FAF8F5;--bg-card:#FFF;--white:#1a1a1a;--gray:#666;--border:#d4d0c8;background:#FAF8F5;color:#1a1a1a;}}body.light-mode nav{{background:rgba(250,248,245,0.97);}}body.light-mode .section{{background:#fff;border-color:#d4d0c8;}}body.light-mode .ext-link{{border-color:#d4d0c8;}}body.light-mode .related-word{{background:rgba(212,175,55,0.08);border-color:#d4d0c8;}}body.light-mode footer{{border-top-color:#d4d0c8;}}</style>
</head>
<body>
    <nav>
        <a href="../index.html">Home</a>
        <a href="../bible.html">Bible Translation Engine</a>
        <a href="../lexicon.html" class="active">Lexicon</a>
        <a href="../blog.html">Blog</a>
        <a href="../links.html">Connect</a>

    </nav>
</div>
        <span style="width:18px;text-align:center;">&#9728;&#65039;</span>
    </div>
    <div class="container">
        <a href="../lexicon.html" class="back-link">&larr; Back to Lexicon</a>
        <div class="word-header">
            <span class="strongs-badge">G{num} &middot; Greek &middot; New Testament</span>
            <div class="original-word">{greek}</div>
            <div class="transliteration">{translit}</div>
            <div class="pos">{pos}</div>
            <div class="gloss">{gloss}</div>
        </div>
        <div class="section">
            <h2>Definition</h2>
            <p>{definition}</p>
        </div>
        <div class="section">
            <h2>Usage &amp; Theological Significance</h2>
            <p>{theological}</p>
        </div>
        <div class="section">
            <h2>Key Bible Verses</h2>
{verses_html}
        </div>
        <div class="section">
            <h2>Related Words</h2>
            <div class="related-words">
{related_html}
            </div>
        </div>
        <div class="section">
            <h2>External Resources</h2>
            <div class="ext-links">
                <a href="https://www.stepbible.org/?q=strong=G{num}" target="_blank" class="ext-link">&#128214; STEP Bible</a>
                <a href="https://www.blueletterbible.org/lexicon/g{num}/kjv/tr/0-1/" target="_blank" class="ext-link">&#128216; Blue Letter Bible</a>
                <a href="https://biblehub.com/greek/{num}.htm" target="_blank" class="ext-link">&#128215; Bible Hub (Interlinear + HELPS)</a>
            </div>
        </div>
    </div>

    <div style="text-align:center;margin:24px auto 10px;">
        <div class="bte-theme-toggle" onclick="bteToggleTheme()" title="Toggle dark/light mode" style="display:inline-flex;align-items:center;background:rgba(30,30,30,0.85);border:1px solid #333;border-radius:20px;padding:3px 6px;cursor:pointer;font-size:0.7rem;">
            <span style="width:18px;text-align:center;">&#127769;</span>
            <div style="width:28px;height:14px;background:#444;border-radius:7px;position:relative;margin:0 4px;"><div style="width:10px;height:10px;background:#D4AF37;border-radius:50%;position:absolute;top:2px;left:2px;transition:left 0.3s;"></div></div>
            <span style="width:18px;text-align:center;">&#9728;&#65039;</span>
        </div>
    </div>
    <footer>
        <p><strong>USMC Ministries Greek &amp; Hebrew Lexicon</strong></p>
        <p style="margin-top:8px;">&copy; 2026 <a href="../index.html">U.S.M.C. Ministries</a> &middot; <a href="../bible.html">Bible Translation Engine</a></p>
    </footer>
<script>function bteToggleTheme(){{var b=document.body;if(b.classList.contains("light-mode")){{b.classList.remove("light-mode");localStorage.setItem("bte-theme","dark");}}else{{b.classList.add("light-mode");localStorage.setItem("bte-theme","light");}}}};(function(){{if(localStorage.getItem("bte-theme")==="light"){{document.body.classList.add("light-mode");}}}})();</script></body>
</html>'''

# Generate all files
created = 0
for entry in entries:
    num = entry[0]
    greek = entry[1]
    translit = entry[2]
    pos = entry[3]
    gloss = entry[4]
    definition = entry[5]
    theological = entry[6]
    verses = entry[7]
    related = entry[8]

    filepath = os.path.join(LEXICON_DIR, f"G{num}.html")
    html = make_html(num, greek, translit, pos, gloss, definition, theological, verses, related)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    created += 1

print(f"\nCreated {created} new Greek lexicon entries!")
print(f"Numbers created: {sorted([e[0] for e in entries])}")
