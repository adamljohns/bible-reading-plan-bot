'use strict';
// denomination-alias-rules.js — the deterministic rules that classify every
// raw `denomination` label in churches.json as one of:
//   body       → a canonical denomination/network id (may carry a sub-field:
//                conference, presbytery, diocese, convention, region)
//   generic    → a family or placeholder label (Baptist, Non-Denominational,
//                Unverified …). No graded page, ever.
//   unresolved → ambiguous, hedged, multi-affiliated, or unknown. Stays unmapped.
//
// A local model may PROPOSE mappings (data/denominations/aliases/alias-proposals.json)
// but nothing here reads them. These rules and the tests decide.

// Hedge words: a label that matches a body but carries one of these is NOT
// mapped ("SBC (verify)", "Formerly UMC", "EFCA-tagged", "AG roots").
const HEDGE = /\b(verify|verified|unverified|likely|possibl[ey]|may be|unclear|unknown|uncertain|conflicting|formerly|former|ex-|was |withdrew|expelled|disfellowshipped|disaffiliated|departed|at risk|loosely|nominal|orbit|adjacent|roots|rooted|heritage|tagged|connected|context|listed|aligned|discerning|status not)\b|\bex-|\bpost-|-adjacent|-tagged|-connected|-listed|-aligned|-linked|\?/i;
// Explicit multi-affiliation markers.
const MULTI = /\bdual|\bdually|multiply|federated|\+/i;
// A second affiliation that is not itself a canonical body still blocks a
// mapping ("NBC/PNBC", "National Baptist Convention / BGAV", "Independent/BGAV").
const OTHER_AFFIL = /(?<!Progressive )National Baptist(?! Convention,? USA)|National Missionary Baptist|\bNBC\b|Independent\s*\/|\/\s*Independent/;
// "NOT SBC" names a body only to deny it.
const NEGATED = /\bnot\s+[A-Za-z-]+/gi;

// Canonical bodies. `re` must match the label; `not` vetoes; `absorbs` lists
// bodies this one is a more specific form of (SBCV inside an SBC label).
const BODIES = [
  // Baptist
  { id: 'sbc', name: 'Southern Baptist Convention', short_name: 'SBC', family: 'baptist', re: /\bSBC\b|southern baptist/i,
    sub: { field: 'convention', re: /(SBTC|BSCNC|GBMB|GBC|KBC|Kentucky Baptist Convention|Hawaii Pacific Baptist Convention|SC Baptist Convention|Dale Baptist Association|Send Network|Calvary Family of Churches)/ } },
  { id: 'sbcv', name: 'Southern Baptist Conservatives of Virginia', short_name: 'SBCV', family: 'baptist', absorbs: ['sbc'],
    re: /\bSBCV\b|Southern Baptists? (Conservatives )?of Virginia|SBC of Virginia|Southern Baptist Convention of Virginia/i },
  { id: 'bgav', name: 'Baptist General Association of Virginia', short_name: 'BGAV', family: 'baptist', re: /\bBGAV\b|Baptist General Association of Virginia/i },
  { id: 'cbf', name: 'Cooperative Baptist Fellowship', short_name: 'CBF', family: 'baptist', re: /\bCBF\b|Cooperative Baptist Fellowship/i },
  { id: 'abcusa', name: 'American Baptist Churches USA', short_name: 'ABCUSA', family: 'baptist', re: /ABC-?USA|American Baptist|\bABC\b/i },
  { id: 'nbcusa', name: 'National Baptist Convention, USA', short_name: 'NBC USA', family: 'baptist', re: /National Baptist Convention,? USA/i },
  { id: 'pnbc', name: 'Progressive National Baptist Convention', short_name: 'PNBC', family: 'baptist', re: /Progressive National Baptist|\bPNBC\b/i },
  { id: 'garbc', name: 'General Association of Regular Baptist Churches', short_name: 'GARBC', family: 'baptist', re: /\bGARBC\b/i },
  { id: 'bbfi', name: 'Baptist Bible Fellowship International', short_name: 'BBFI', family: 'baptist', re: /\bBBFI\b/i },
  { id: 'nafwb', name: 'National Association of Free Will Baptists', short_name: 'Free Will Baptist', family: 'baptist', re: /Free Will Baptist|\bFWB\b/i },
  { id: 'converge', name: 'Converge (Baptist General Conference)', short_name: 'Converge', family: 'baptist', re: /\bConverge\b|Baptist General Conference|\bBGC\b/i },
  { id: 'cbamerica', name: 'CBAmerica (Conservative Baptist Association of America)', short_name: 'CBAmerica', family: 'baptist', re: /CBAmerica|Conservative Baptist Association|\bCB Northwest\b/i,
    sub: { field: 'region', re: /(CB Northwest)/ } },
  { id: 'arbca', name: 'Association of Reformed Baptist Churches of America', short_name: 'ARBCA', family: 'baptist', re: /\bARBCA\b/i },
  { id: 'aba', name: 'American Baptist Association', short_name: 'ABA', family: 'baptist', re: /\bABA\b/ },
  { id: 'fgbcf', name: 'Full Gospel Baptist Church Fellowship', short_name: 'FGBCF', family: 'baptist', re: /Full Gospel Baptist Church Fellowship/i },
  { id: 'alliance-of-baptists', name: 'Alliance of Baptists', short_name: 'Alliance of Baptists', family: 'baptist', re: /Alliance of Baptists/i },
  { id: 'bgct', name: 'Baptist General Convention of Texas', short_name: 'BGCT', family: 'baptist', re: /\bBGCT\b|Texas Baptists/i },
  { id: 'scba', name: 'Southeast Association of Confessional Baptists', short_name: 'SEACB', family: 'baptist', re: /Southeast Association of Confessional Baptists/i },
  { id: 'continental-baptist', name: 'Continental Baptist Churches', short_name: 'Continental Baptist', family: 'baptist', re: /Continental Baptist Churches/i },
  { id: 'acts29', name: 'Acts 29 Network', short_name: 'Acts 29', family: 'network', re: /Acts 29/i },
  { id: 'sgc', name: 'Sovereign Grace Churches', short_name: 'SGC', family: 'network', re: /Sovereign Grace/i },
  { id: 'arc', name: 'Association of Related Churches', short_name: 'ARC', family: 'network', re: /\bARC\b|Association of Related Churches/ },
  { id: 'every-nation', name: 'Every Nation Churches', short_name: 'Every Nation', family: 'network', re: /Every Nation/i },
  { id: 'hillsong', name: 'Hillsong Network', short_name: 'Hillsong', family: 'network', re: /Hillsong/i },
  { id: 'c3-global', name: 'C3 Global (Christian City Church)', short_name: 'C3', family: 'network', re: /C3 Global/i },
  { id: 'newfrontiers', name: 'Newfrontiers', short_name: 'Newfrontiers', family: 'network', re: /Newfrontiers/i },
  // Methodist / Wesleyan / Holiness
  { id: 'umc', name: 'United Methodist Church', short_name: 'UMC', family: 'methodist', re: /United Methodist|\bUMC\b/i,
    sub: { field: 'conference', re: /(Virginia Conference|BWC)/, map: { 'Virginia Conference': 'Virginia Annual Conference', BWC: 'Baltimore-Washington Conference' } } },
  { id: 'gmc', name: 'Global Methodist Church', short_name: 'GMC', family: 'methodist', re: /Global Methodist|\bGMC\b/i },
  { id: 'ame', name: 'African Methodist Episcopal Church', short_name: 'AME', family: 'methodist', re: /African Methodist Episcopal|\bAME\b/i }, // bare "AMEC" in this directory is the Anabaptist Alliance of Mennonite Evangelical Congregations, not the AME (CCW-1119-DIR3)
  { id: 'amez', name: 'African Methodist Episcopal Zion Church', short_name: 'AME Zion', family: 'methodist', absorbs: ['ame'], re: /AME Zion|Methodist Episcopal Zion/i },
  { id: 'cme', name: 'Christian Methodist Episcopal Church', short_name: 'CME', family: 'methodist', re: /Christian Methodist Episcopal|\bCME\b/i },
  { id: 'fmc', name: 'Free Methodist Church USA', short_name: 'Free Methodist', family: 'methodist', absorbs: ['wesleyan'], re: /Free Methodist/i },
  { id: 'wesleyan', name: 'The Wesleyan Church', short_name: 'Wesleyan', family: 'methodist', re: /^(The )?Wesleyan( Church)?$/i },
  { id: 'emc-methodist', name: 'Evangelical Methodist Church', short_name: 'EMC', family: 'methodist', re: /Evangelical Methodist/i },
  { id: 'nazarene', name: 'Church of the Nazarene', short_name: 'Nazarene', family: 'methodist', re: /Nazarene/i },
  { id: 'salvation-army', name: 'The Salvation Army', short_name: 'Salvation Army', family: 'methodist', re: /Salvation Army/i },
  // Presbyterian / Reformed
  { id: 'pca', name: 'Presbyterian Church in America', short_name: 'PCA', family: 'presbyterian', re: /\bPCA\b|(?<!Cumberland )Presbyterian Church in America/i,
    sub: { field: 'presbytery', re: /—\s*(.+?)\s*$/ } },
  { id: 'cpca', name: 'Cumberland Presbyterian Church in America', short_name: 'CPCA', family: 'presbyterian', re: /Cumberland Presbyterian Church in America/i },
  { id: 'opc', name: 'Orthodox Presbyterian Church', short_name: 'OPC', family: 'presbyterian', re: /\bOPC\b|Orthodox Presbyterian/i,
    sub: { field: 'presbytery', re: /—\s*(Presbytery.+?)\s*$/ } },
  { id: 'arp', name: 'Associate Reformed Presbyterian Church', short_name: 'ARP', family: 'presbyterian', re: /\bARP\b|Associate Reformed Presbyterian/i },
  { id: 'epc', name: 'Evangelical Presbyterian Church', short_name: 'EPC', family: 'presbyterian', re: /\bEPC\b|Evangelical Presbyterian(?!s)/i,
    sub: { field: 'presbytery', re: /—\s*(.+?Presbytery)\s*$/ } },
  { id: 'eco', name: 'ECO: A Covenant Order of Evangelical Presbyterians', short_name: 'ECO', family: 'presbyterian', re: /^ECO\b|Covenant Order of Evangelical Presbyterians/ },
  { id: 'pcusa', name: 'Presbyterian Church (U.S.A.)', short_name: 'PCUSA', family: 'presbyterian', re: /PCUSA|PC\(USA\)|Presbyterian Church \(U\.?S\.?A\.?\)|Presbyterian Church USA/i },
  { id: 'rpcna', name: 'Reformed Presbyterian Church of North America', short_name: 'RPCNA', family: 'presbyterian', re: /\bRPCNA\b|Reformed Presbyterian Church of North America/i },
  { id: 'rpcga', name: 'Reformed Presbyterian Church General Assembly', short_name: 'RPCGA', family: 'presbyterian', re: /\bRPCGA\b|Reformed Presbyterian Church General Assembly/i,
    sub: { field: 'presbytery', re: /,\s*(.+Presbytery)\s*$/ } },
  { id: 'bpc', name: 'Bible Presbyterian Church', short_name: 'BPC', family: 'presbyterian', re: /Bible Presbyterian/i },
  { id: 'kapc', name: 'Korean American Presbyterian Church', short_name: 'KAPC', family: 'presbyterian', re: /\bKAPC\b/ },
  { id: 'fcsc', name: 'Free Church of Scotland (Continuing)', short_name: 'FCC', family: 'presbyterian', re: /Free Church of Scotland \(Continuing\)/i,
    sub: { field: 'presbytery', re: /—\s*(.+?)\s*$/ } },
  { id: 'presrc', name: 'Presbyterian Reformed Church', short_name: 'PresRC', family: 'presbyterian', re: /^Presbyterian Reformed Church$/i },
  { id: 'urcna', name: 'United Reformed Churches in North America', short_name: 'URCNA', family: 'reformed', re: /\bURCNA\b|United Reformed Churches/i },
  { id: 'crcna', name: 'Christian Reformed Church in North America', short_name: 'CRC', family: 'reformed', re: /\bCRC(NA)?\b|Christian Reformed Church/i },
  { id: 'canrc', name: 'Canadian and American Reformed Churches', short_name: 'CanRC', family: 'reformed', re: /Canadian Reformed/i },
  { id: 'rcus', name: 'Reformed Church in the United States', short_name: 'RCUS', family: 'reformed', re: /\bRCUS\b|Reformed Church in the United States/i },
  { id: 'prca', name: 'Protestant Reformed Churches in America', short_name: 'PRCA', family: 'reformed', re: /\bPRCA\b/ },
  { id: 'hrcna', name: 'Heritage Reformed Congregations', short_name: 'HRC', family: 'reformed', re: /\bHRC(NA)?\b/ },
  { id: 'frcna', name: 'Free Reformed Churches of North America', short_name: 'FRCNA', family: 'reformed', re: /\bFRCNA\b|Free Reformed Churches/i },
  { id: 'nrc', name: 'Netherlands Reformed Congregations', short_name: 'NRC', family: 'reformed', re: /^NRC$/ },
  { id: 'rca', name: 'Reformed Church in America', short_name: 'RCA', family: 'reformed', re: /Reformed Church in America|\bRCA\b/ },
  { id: 'crec', name: 'Communion of Reformed Evangelical Churches', short_name: 'CREC', family: 'reformed', re: /\bCREC\b|Communion of Reformed Evangelical Churches/i },
  { id: 'ucc', name: 'United Church of Christ', short_name: 'UCC', family: 'congregational', re: /United Church of Christ|\bUCC\b/i },
  { id: 'cccc', name: 'Conservative Congregational Christian Conference', short_name: 'CCCC', family: 'congregational', re: /\bCCCC\b|Conservative Congregational Christian Conference/i },
  { id: 'disciples', name: 'Christian Church (Disciples of Christ)', short_name: 'Disciples', family: 'restorationist', re: /Disciples of Christ/i },
  // Lutheran
  { id: 'lcms', name: 'Lutheran Church—Missouri Synod', short_name: 'LCMS', family: 'lutheran', re: /\bLCMS\b|Missouri Synod/i },
  { id: 'elca', name: 'Evangelical Lutheran Church in America', short_name: 'ELCA', family: 'lutheran', re: /\bELCA\b|Evangelical Lutheran Church in America/i },
  { id: 'wels', name: 'Wisconsin Evangelical Lutheran Synod', short_name: 'WELS', family: 'lutheran', re: /\bWELS\b|Wisconsin Evangelical Lutheran/i },
  { id: 'els', name: 'Evangelical Lutheran Synod', short_name: 'ELS', family: 'lutheran', re: /^ELS$/ },
  { id: 'lcmc', name: 'Lutheran Congregations in Mission for Christ', short_name: 'LCMC', family: 'lutheran', re: /\bLCMC\b|Lutheran Congregations in Mission for Christ/i },
  { id: 'nalc', name: 'North American Lutheran Church', short_name: 'NALC', family: 'lutheran', re: /\bNALC\b/ },
  { id: 'aalc', name: 'The American Association of Lutheran Churches', short_name: 'AALC', family: 'lutheran', re: /\bAALC\b|American Association of Lutheran Churches/i },
  // Anglican / Episcopal / Catholic / Orthodox
  { id: 'tec', name: 'The Episcopal Church', short_name: 'TEC', family: 'anglican', re: /\bThe Episcopal Church\b|^Episcopal Church\b|\bTEC\b/,
    sub: { field: 'diocese', re: /(Diocese of [A-Z][A-Za-z ]+?)\s*\)?\s*$/ } },
  { id: 'acna', name: 'Anglican Church in North America', short_name: 'ACNA', family: 'anglican', re: /\bACNA\b|Anglican Church in North America/,
    sub: { field: 'diocese', re: /(?:—|,)\s*((?:Anglican )?Diocese[^)]*|Rocky Mountain Anglican)\)?\s*$/ } },
  { id: 'rec', name: 'Reformed Episcopal Church', short_name: 'REC', family: 'anglican', re: /\bREC\b|Reformed Episcopal Church/ },
  { id: 'amia', name: 'Anglican Mission in America', short_name: 'AMiA', family: 'anglican', re: /\bAMiA\b|Anglican Mission in America/ },
  { id: 'cana', name: 'Convocation of Anglicans in North America', short_name: 'CANA', family: 'anglican', re: /^CANA$/ },
  { id: 'acc', name: 'Anglican Catholic Church', short_name: 'ACC', family: 'anglican', re: /\bACC\b|Anglican Catholic Church/ },
  { id: 'apa', name: 'Anglican Province of America', short_name: 'APA', family: 'anglican', re: /\bAPA\b|Anglican Province of America/ },
  { id: 'apck', name: 'Anglican Province of Christ the King', short_name: 'APCK', family: 'anglican', re: /\bAPCK\b|Anglican Province of Christ the King/ },
  { id: 'rcc', name: 'Roman Catholic Church', short_name: 'Catholic', family: 'catholic', re: /Roman Catholic|^Catholic$/i,
    sub: { field: 'diocese', re: /((?:Arch)?[Dd]iocese of [A-Z][A-Za-z ]+)/ } },
  { id: 'coptic', name: 'Coptic Orthodox Church', short_name: 'Coptic Orthodox', family: 'orthodox', re: /Coptic Orthodox/i },
  { id: 'antiochian', name: 'Antiochian Orthodox Christian Archdiocese', short_name: 'Antiochian Orthodox', family: 'orthodox', re: /Antiochian Orthodox/i },
  // Free church / evangelical
  { id: 'efca', name: 'Evangelical Free Church of America', short_name: 'EFCA', family: 'free-church', re: /\bEFCA\b|Evangelical Free|E\.F\.C\.A\.|\bEV Free\b|\bE-Free\b/i },
  { id: 'ecc', name: 'Evangelical Covenant Church', short_name: 'ECC', family: 'free-church', re: /Evangelical Covenant/i },
  { id: 'cma', name: 'Christian and Missionary Alliance', short_name: 'C&MA', family: 'free-church', re: /C&MA|\bCMA\b|Christian (and|&) Missionary Alliance/i },
  { id: 'ifca', name: 'IFCA International', short_name: 'IFCA', family: 'free-church', re: /\bIFCA\b/ },
  { id: 'bfc', name: 'Bible Fellowship Church', short_name: 'BFC', family: 'free-church', re: /Bible Fellowship Church/i },
  { id: 'calvary-chapel', name: 'Calvary Chapel', short_name: 'Calvary Chapel', family: 'network', re: /Calvary Chapel(?! Association)/i },
  { id: 'calvary-chapel-association', name: 'Calvary Chapel Association', short_name: 'CCA', family: 'network', re: /Calvary Chapel Association/i },
  { id: 'vineyard', name: 'Vineyard USA', short_name: 'Vineyard', family: 'charismatic', re: /Vineyard/i },
  // Pentecostal
  { id: 'aog', name: 'Assemblies of God', short_name: 'AoG', family: 'pentecostal', re: /Assemblies of God|\bAoG\b|\bAG\b/ },
  { id: 'foursquare', name: 'International Church of the Foursquare Gospel', short_name: 'Foursquare', family: 'pentecostal', re: /Foursquare|\bICFG\b/i },
  { id: 'cog-cleveland', name: 'Church of God (Cleveland, Tennessee)', short_name: 'Church of God (Cleveland)', family: 'pentecostal', re: /Church of God \(Cleveland/i },
  { id: 'cog-anderson', name: 'Church of God (Anderson, Indiana)', short_name: 'Church of God (Anderson)', family: 'holiness', re: /Church of God \(Anderson/i },
  { id: 'cogop', name: 'Church of God of Prophecy', short_name: 'COGOP', family: 'pentecostal', re: /Church of God of Prophecy/i },
  { id: 'cogic', name: 'Church of God in Christ', short_name: 'COGIC', family: 'pentecostal', re: /\bCOGIC\b|Church of God in Christ/i },
  { id: 'upci', name: 'United Pentecostal Church International', short_name: 'UPCI', family: 'pentecostal', re: /\bUPCI?\b/ },
  { id: 'uhca', name: 'United Holy Church of America', short_name: 'UHCA', family: 'pentecostal', re: /United Holy Church of America/i },
  // Anabaptist / Brethren
  { id: 'cmc-mennonite', name: 'CMC (Conservative Mennonite Conference) / Rosedale Network', short_name: 'CMC', family: 'anabaptist', re: /\bCMC\b|Rosedale Network/ },
  { id: 'smc-mennonite', name: 'Southeastern Mennonite Conference', short_name: 'SMC', family: 'anabaptist', re: /SMC Mennonite/ },
  { id: 'mb', name: 'U.S. Conference of Mennonite Brethren Churches', short_name: 'USMB', family: 'anabaptist', re: /Mennonite Brethren|\bUSMB\b/i },
  { id: 'mcusa', name: 'Mennonite Church USA', short_name: 'MC USA', family: 'anabaptist', re: /Mennonite Church USA/i },
  { id: 'bic', name: 'Brethren in Christ U.S.', short_name: 'BIC', family: 'anabaptist', re: /Brethren in Christ/i },
  { id: 'beachy', name: 'Beachy Amish Mennonite Fellowship', short_name: 'Beachy', family: 'anabaptist', re: /Beachy Amish/i },
  { id: 'nationwide-fellowship', name: 'Nationwide Fellowship Churches', short_name: 'Nationwide Fellowship', family: 'anabaptist', re: /Nationwide Fellowship/i },
  { id: 'epmc', name: 'Eastern Pennsylvania Mennonite Church', short_name: 'EPMC', family: 'anabaptist', re: /Eastern Pennsylvania Mennonite/i },
  { id: 'mamf', name: 'Mid-Atlantic Mennonite Fellowship', short_name: 'MAMF', family: 'anabaptist', re: /Mid-Atlantic Mennonite Fellowship/i },
  { id: 'mcf', name: 'Mennonite Christian Fellowship', short_name: 'MCF', family: 'anabaptist', re: /Mennonite Christian Fellowship/i },
  { id: 'keystone-mennonite', name: 'Keystone Mennonite Fellowship', short_name: 'Keystone', family: 'anabaptist', re: /Keystone Mennonite Fellowship/i },
  { id: 'pilgrim-mennonite', name: 'Pilgrim Mennonite Conference', short_name: 'Pilgrim Mennonite', family: 'anabaptist', re: /Pilgrim Mennonite Conference/i },
  { id: 'bma-mennonite', name: 'Biblical Mennonite Alliance', short_name: 'BMA', family: 'anabaptist', re: /^BMA Mennonite$/ },
  { id: 'charity', name: 'Charity Christian Fellowship', short_name: 'Charity', family: 'anabaptist', re: /Charity Christian Fellowship/i },
  { id: 'dunkard', name: 'Dunkard Brethren Church', short_name: 'Dunkard Brethren', family: 'anabaptist', re: /Dunkard Brethren/i },
  { id: 'ogbb-nc', name: 'Old German Baptist Brethren, New Conference', short_name: 'OGBB New Conference', family: 'anabaptist', re: /Old German Baptist Brethren New Conference/i },
  { id: 'charis', name: 'Charis Fellowship (Fellowship of Grace Brethren Churches)', short_name: 'Charis', family: 'brethren', re: /Charis Fellowship|Fellowship of Grace Brethren|\bFGBC\b/i },
  // Other
  { id: 'sda', name: 'Seventh-day Adventist Church', short_name: 'SDA', family: 'adventist', re: /Seventh-day Adventist/i },
  { id: 'uua', name: 'Unitarian Universalist Association', short_name: 'UUA', family: 'non-trinitarian', re: /Unitarian Universalist/i },
  { id: 'mcc', name: 'Metropolitan Community Churches', short_name: 'MCC', family: 'other', re: /Metropolitan Community Church/i },
  { id: 'unity', name: 'Unity (New Thought)', short_name: 'Unity', family: 'non-trinitarian', re: /^Unity \(New Thought\)$/i },
  { id: 'christian-science', name: 'Church of Christ, Scientist', short_name: 'Christian Science', family: 'non-trinitarian', re: /Christian Science|Church of Christ, Scientist/i },
];

// Family/placeholder labels: no body. Checked only when no body matched.
// First hit wins, so narrower families come first.
const GENERIC = [
  { family: 'placeholder', re: /^\s*$|^(unverified|verify|unknown)$/i },
  { family: 'reformed-baptist', re: /reformed baptist|reforming baptist|\b1689\b|founders|confessional baptist|calvinistic baptist|reformed baptistic/i },
  { family: 'independent-baptist', re: /independent (fundamental )?baptist|\bIFB\b|independent kjv|kjv/i },
  { family: 'anabaptist', re: /mennonite|anabaptist|amish/i },
  { family: 'brethren', re: /brethren/i },
  { family: 'baptist', re: /baptist|^NBC$/i },
  { family: 'presbyterian', re: /presbyterian/i },
  { family: 'reformed', re: /reformed|three forms of unity|savoy/i },
  { family: 'lutheran', re: /lutheran/i },
  { family: 'pentecostal-charismatic', re: /pentecostal|charismatic|apostolic|full gospel|nar\b/i },
  { family: 'holiness', re: /holiness/i },
  { family: 'methodist', re: /methodist|wesleyan/i },
  { family: 'anglican', re: /anglican|episcopal/i },
  { family: 'orthodox', re: /orthodox/i },
  { family: 'restorationist', re: /church of christ|churches of christ|christian church|restoration/i },
  { family: 'quaker', re: /quaker|friends church/i },
  { family: 'adventist', re: /adventist/i },
  { family: 'church-of-god', re: /^church of god$/i },
  { family: 'congregational', re: /congregational/i },
  { family: 'non-denominational', re: /non-?denom|nondenom|interdenominational|^independent\b|bible church|bible chapel|^bible\b|independent bible|^evangelical$|^christian\b|network$/i },
];

function classifyLabel(label) {
  const raw = label == null ? '' : String(label);
  const s = raw.trim();
  const m0 = s.replace(NEGATED, ' ');
  const hits = [];
  for (const b of BODIES) if (b.re.test(m0)) hits.push(b);
  const absorbed = new Set(hits.flatMap(b => b.absorbs || []));
  const bodies = hits.filter(b => !absorbed.has(b.id));
  if (bodies.length) {
    const hedge = s.match(HEDGE);
    if (hedge) return { status: 'unresolved', reason: `hedged ("${hedge[0].trim()}")`, candidates: bodies.map(b => b.id) };
    if (bodies.length > 1) return { status: 'unresolved', reason: 'names more than one body', candidates: bodies.map(b => b.id) };
    if (MULTI.test(s)) return { status: 'unresolved', reason: 'multi-affiliation marker', candidates: bodies.map(b => b.id) };
    if (OTHER_AFFIL.test(m0)) return { status: 'unresolved', reason: 'second affiliation named', candidates: bodies.map(b => b.id) };
    const b = bodies[0];
    const out = { status: 'body', id: b.id };
    if (b.sub) {
      const m = s.match(b.sub.re);
      if (m && m[1]) out[b.sub.field] = (b.sub.map && b.sub.map[m[1]]) || m[1].trim();
    }
    return out;
  }
  for (const g of GENERIC) if (g.re.test(s)) return { status: 'generic', family: g.family };
  return { status: 'unresolved', reason: 'no rule matches', candidates: [] };
}

module.exports = { BODIES, GENERIC, HEDGE, MULTI, OTHER_AFFIL, classifyLabel };
