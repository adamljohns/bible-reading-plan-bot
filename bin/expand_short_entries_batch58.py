#!/usr/bin/env python3
"""Batch 58 — final polish: clears ALL featured-section stragglers.

16 entries in the four anchor sections (Doctrinal Anchors, Biblical
Order, Expressly Prohibited, Most Corrupted) plus Boomer Decoded's
final outlier. Pushes every featured-section entry to 90+ words.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'murder': (
        '<p>Murder is the unlawful killing of a human being made in the image of God — the sixth commandment of the Decalogue: <em>"Thou shalt not kill"</em> (<em>Exodus 20:13</em>; better rendered <em>"do not murder,"</em> from Hebrew <em>ratsach</em>). Christ raised the standard inwardly in the Sermon on the Mount: <em>"Whosoever is angry with his brother without a cause shall be in danger of the judgment"</em> (<em>Matthew 5:21-22</em>). Murder includes elective abortion (the deliberate killing of the unborn image-bearer, in the womb the LORD Himself was forming, <em>Psalm 139:13</em>), euthanasia, and unjust war. Scripture distinguishes murder sharply from capital punishment by the magistrate (<em>Romans 13:4</em>) and from killing in just war or self-defense. The murderer is excluded from the kingdom (<em>Revelation 21:8; 22:15</em>) — yet murderers are saved when they repent (David, Paul).</p>'
    ),
    'christology': (
        '<p>Christology is the branch of theology concerned with who Jesus Christ is and what He accomplished. Scripture presents Christ as fully God (<em>John 1:1; Colossians 2:9</em>: <em>"in him dwelleth all the fulness of the Godhead bodily"</em>) and fully man (<em>John 1:14; Hebrews 2:17</em>) — two natures united in one Person without mixture, confusion, division, or separation (Chalcedon, 451 AD). The orthodox formulation has been worked out across the great councils — Nicaea (325, against Arius), Constantinople (381, against the Pneumatomachians), Ephesus (431, against Nestorius), and Chalcedon (451) — and remains the church’s settled confession. Every Christological heresy denies one half of the formula: Arianism denied full deity; Docetism denied real humanity; Apollinarianism denied a human soul; Nestorianism split the Person; Eutychianism mixed the natures. The Reformed confessions hold the Chalcedonian center.</p>'
    ),
    'kings-hall': (
        '<p>Kings Hall Podcast is the long-form Reformed-patriarchal podcast hosted by Brian Sauve and Eric Conn, central to the twenty-first-century New Christian Right (NXR) conversation. Subjects include Christian nationalism, biblical patriarchy, the Long House diagnosis, the reviling-wife pattern, the recovery of embodied masculinity, theonomy, postmillennial ambition, classical-confessional Reformed theology, and the rejection of evangelical Big Eva. Recurring guests include Bnonn Tennant, Joel Webbon, William Wolfe, and the broader Reformed-confessional network. The podcast’s tone is unapologetic, scripturally direct, and aimed at men. It is best heard as one node in a wider conversation that includes Sauve’s church (Refuge Church, Ogden) and Conn’s church — pastors leading the recovery of the historic Reformed-confessional masculine vision.</p>'
    ),
    'predestination': (
        '<p>Predestination is the sovereign act of God by which He foreordains, according to His own will and purpose, those who will be conformed to the image of His Son and receive eternal life (<em>Romans 8:29-30; Ephesians 1:5, 11</em>). Predestination is not arbitrary fatalism but the loving choice of a sovereign Father exercised before the foundation of the world: <em>"According as he hath chosen us in him before the foundation of the world, that we should be holy and without blame before him in love"</em> (<em>Ephesians 1:4</em>). It humbles the saved (no boasting), comforts them (no losing what God secured), and frees them to evangelize (the elect will come). The Reformed tradition affirms double predestination — God elects some to salvation and passes others by — though the elect-side is biblically emphasized.</p>'
    ),
    'covetousness': (
        '<p>Covetousness is inordinate desire for what belongs to another — the violation of the tenth commandment: <em>"Thou shalt not covet thy neighbour’s house, thou shalt not covet thy neighbour’s wife, nor his manservant, nor his maidservant, nor his ox, nor his ass, nor any thing that is thy neighbour’s"</em> (<em>Exodus 20:17</em>). The tenth commandment is uniquely inward — it forbids the desire itself, not just the resulting deed. Paul lists covetousness with idolatry: <em>"Mortify therefore your members which are upon the earth; fornication, uncleanness, inordinate affection, evil concupiscence, and covetousness, which is idolatry"</em> (<em>Colossians 3:5</em>). Christ warns: <em>"Take heed, and beware of covetousness: for a man’s life consisteth not in the abundance of the things which he possesseth"</em> (<em>Luke 12:15</em>). Covetousness drives theft, adultery, slander, and most lawsuits. Mortify it at the root.</p>'
    ),
    'transvestism': (
        '<p>Transvestism is the clinical / technical term for cross-dressing — the wearing of clothing of the opposite sex. The same biblical prohibition applies as for cross-dressing generally: <em>"The woman shall not wear that which pertaineth unto a man, neither shall a man put on a woman’s garment: for all that do so are abomination unto the LORD thy God"</em> (<em>Deuteronomy 22:5</em>). The Hebrew <em>to‘evah</em> ("abomination") places it in the gravest moral category. The clinical framing of transvestism as a "sexual paraphilia" — neutral psychological terminology — has obscured the moral category Scripture establishes. Modern "drag," cross-dressing in performance, and the broader transgender ideology all fall under the same Mosaic prohibition. Christian men and women dress as the sex God assigned them in the womb; the LORD calls cross-dressing not preference but abomination.</p>'
    ),
    'submission': (
        '<p>Submission is the voluntary, willing placement of oneself under God-ordained authority — not out of weakness or coercion but out of trust in God’s design. Biblical submission is always <em>active</em>, never passive; <em>chosen</em>, never forced. Scripture calls all believers to submit to God (<em>James 4:7</em>), citizens to magistrates (<em>Romans 13:1</em>), saints to elders (<em>Hebrews 13:17</em>), servants to masters (<em>1 Peter 2:18</em>), wives to their own husbands (<em>Ephesians 5:22-24; Colossians 3:18; 1 Peter 3:1</em>), the church to Christ (<em>Ephesians 5:24</em>), and Christ Himself, in the economy of the Trinity, to the Father (<em>1 Corinthians 11:3; 15:28</em>). Submission therefore reflects God’s own internal triune order. It is dignified, masculine and feminine alike, and a covenantal virtue Christ Himself exemplified at Gethsemane.</p>'
    ),
    'contentious-wife': (
        '<p>The contentious wife is the near-synonym of the reviling wife — a wife whose default mode in marriage is strife, brawling, escalation, the picked fight, the constant friction. Distinguished from the wife who appeals respectfully, raises hard questions, or grieves real wrong, the contentious wife <em>seeks</em> the fight and refuses peace. Solomon writes of her four times: <em>"It is better to dwell in the wilderness, than with a contentious and an angry woman"</em> (<em>Proverbs 21:19</em>); <em>"It is better to dwell in a corner of the housetop, than with a brawling woman in a wide house"</em> (<em>21:9; 25:24</em>); <em>"A continual dropping in a very rainy day and a contentious woman are alike"</em> (<em>27:15</em>). The wisdom is unsparing — and identifies the husband’s misery. The remedy is not silence but repentance, and Christian elders who refuse to flatter the pattern.</p>'
    ),
    'justice': (
        '<p>Justice is the character of God expressed in giving every person their due — punishing wickedness, vindicating the righteous, protecting the vulnerable, and ordering society according to His law. Justice in Scripture is not a human social project but a divine attribute reflected in His commands: <em>"Shall not the Judge of all the earth do right?"</em> (<em>Genesis 18:25</em>); <em>"Justice and judgment are the habitation of thy throne: mercy and truth shall go before thy face"</em> (<em>Psalm 89:14</em>). True biblical justice is impartial (<em>"thou shalt not respect persons in judgment"</em>, <em>Deuteronomy 1:17</em>), protects property and life, defends widow and orphan, and rejects bribes. Modern "social justice" is the term’s most corrupted use — redistributing along racial or class lines in defiance of biblical impartiality. Recover the word; refuse the counterfeit.</p>'
    ),
    'regeneration': (
        '<p>Regeneration is the supernatural act of God by which a spiritually dead sinner is made alive in Christ — a new birth from above wrought entirely by the Holy Spirit. Regeneration is not reformation of character, moral improvement, or decision of the will; it is the resurrection of a soul that was dead in trespasses and sins (<em>Ephesians 2:1-5</em>). <em>"Except a man be born again, he cannot see the kingdom of God... That which is born of the flesh is flesh; and that which is born of the Spirit is spirit"</em> (<em>John 3:3-6</em>). The new heart (<em>Ezekiel 36:26</em>) is given monergistically — by God alone, without human cooperation — and produces faith, repentance, love, and obedience as fruit, not as cause. Regeneration is the doctrine the Reformers fought for against late-medieval semi-Pelagianism; it is the doctrine evangelicalism is currently in danger of losing again.</p>'
    ),
    'headship': (
        '<p>Headship is the God-ordained authority and sacrificial responsibility entrusted to Christ over the Church, and modeled by the husband in marriage. It is not domination or superiority of worth but a covenant role of servant-leadership — to love, lead, provide, protect, sanctify, and lay down one’s life for the household. <em>"For the husband is the head of the wife, even as Christ is the head of the church: and he is the saviour of the body"</em> (<em>Ephesians 5:23</em>). The order Paul lays out is precise: <em>"the head of every man is Christ; and the head of the woman is the man; and the head of Christ is God"</em> (<em>1 Corinthians 11:3</em>) — a Trinitarian ordering. Headship is essential, indispensable, and irrevocable; egalitarianism rejects what God has structured. Recover headship; live the burden it carries; expect the joy it brings.</p>'
    ),
    'christian-nationalism': (
        '<p>Christian Nationalism is the political-theological position that civil governments are accountable to Christ as Lord, that nations have a public duty to acknowledge Christ and order public life under His Lordship, and that this is the natural application of <em>Psalm 2:10-12</em>: <em>"Be wise now therefore, O ye kings: be instructed, ye judges of the earth. Serve the LORD with fear, and rejoice with trembling. Kiss the Son, lest he be angry"</em> — and the Great Commission’s claim that Christ has <em>all authority in heaven and earth</em> (<em>Matthew 28:18</em>). Major proponents include Stephen Wolfe (<em>The Case for Christian Nationalism</em>, 2022), Doug Wilson, Joel Webbon, and the NXR / Kings Hall network. Distinguished from civic religion (vague theistic civil ceremonialism) and from sectarian theocracy (pre-eschaton compulsion of conscience), it confesses Christ’s public crown rightly held by every nation.</p>'
    ),
    'white-knighting': (
        '<p>White-knighting is the activity of the white knight — positioning oneself as the defender of a woman in a public dispute without first weighing the case, often against other men to whom one owes deeper covenantal or fraternal loyalty. White-knighting is not the same as the husband’s legitimate defense of his wife, the father’s protection of his daughter, or the church’s discipline of the man who has actually wronged the woman in his care. It is the unbidden public intervention — typically by men with no covenantal standing — driven by the felt need to appear chivalrous, win female approval, or vent unprocessed feeling. Scripture warns: <em>"He that passeth by, and meddleth with strife belonging not to him, is like one that taketh a dog by the ears"</em> (<em>Proverbs 26:17</em>). The remedy is masculine restraint, deeper loyalty to the men of one’s own household, and refusing to be played.</p>'
    ),
    'occult': (
        '<p>Occult is the umbrella English term for the family of hidden-knowledge spiritual practices Scripture comprehensively forbids: divination, sorcery, witchcraft, necromancy, astrology, charm-work, familiar-spirit consultation, magic, and ritual ceremony aimed at acquiring supernatural power or information outside God’s revealed channel. <em>Deuteronomy 18:9-14</em> lists them by name and seals the verdict: <em>"For all that do these things are an abomination unto the LORD: and because of these abominations the LORD thy God doth drive them out from before thee."</em> Modern equivalents — tarot, ouija, astrology apps, Wicca, energy healing, channeling, mediumship, séances, "manifesting," New Age practice, much of yoga’s spiritual content, and most "magic" entertainment when treated as more than fiction — fall under the same Mosaic prohibition. Christ cast out demons; He did not negotiate with them. Christian men reject the occult absolutely.</p>'
    ),
    'a-ok': (
        '<p>"A-OK" is the Boomer-era affirmation meaning <em>"completely fine, fully operational, in perfect order"</em> — mainstreamed by the 1961 Mercury astronaut program (Alan Shepard’s flight communications) and used freely through the 1970s before declining. The slang is purely expressive — a status update of well-being. The Christian observation: the church has always had a vocabulary for status reports between saints, and it runs deeper than well-being. Paul’s standard letter-openings: <em>"Grace be to you, and peace, from God our Father, and from the Lord Jesus Christ"</em> (<em>Romans 1:7</em>). Paul’s closing greetings: <em>"The brethren which are with me greet you... All the saints salute you, chiefly they that are of Caesar’s household. The grace of our Lord Jesus Christ be with you all. Amen"</em> (<em>Philippians 4:21-23</em>). The Christian status-report is not "A-OK"; it is grace and peace.</p>'
    ),
    'sorcery': (
        '<p>Sorcery is effectively a synonym for witchcraft, with particular emphasis on the use of drugs, potions, and ritual technique to access supernatural power apart from God. The New Testament Greek word is <em>pharmakeia</em> (<em>Galatians 5:20; Revelation 9:21; 18:23; 21:8; 22:15</em>) — literally "the use of drugs, potions, or spells." It is the root of the English word <em>pharmacy</em>. The connection between drug-induced altered states and demonic encounter is ancient and persistent: shamanism in every traditional culture deploys pharmacological agents to open spiritual portals. Modern usage covers psychedelic mysticism, occult ritual involving substances, and ayahuasca tourism explicitly marketed as spiritual encounter. Scripture absolutely forbids it: <em>"the fearful, and unbelieving, and the abominable, and murderers, and whoremongers, and sorcerers... shall have their part in the lake which burneth with fire"</em> (<em>Revelation 21:8</em>). Sorcerers do not inherit the kingdom.</p>'
    ),
}

BD_RE = re.compile(r'(<div class="biblical-def">)(.*?)(</div>)', re.DOTALL)

def patch(slug, new_inner):
    fp = os.path.join(DICT_DIR, f'{slug}.html')
    if not os.path.exists(fp):
        return False, 'file missing'
    with open(fp, encoding='utf-8') as f:
        html = f.read()
    new_html, n = BD_RE.subn(
        rf'\g<1>\n                {new_inner}\n            \g<3>',
        html, count=1)
    if n == 0:
        return False, 'pattern not matched'
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_html)
    return True, 'ok'

def main():
    ok, fail = 0, 0
    for slug, new in EXPANSIONS.items():
        success, reason = patch(slug, new)
        if success:
            ok += 1
        else:
            fail += 1
            print(f'  FAIL {slug}: {reason}')
    print(f'Expanded {ok}/{ok+fail} entries')

if __name__ == '__main__':
    main()
