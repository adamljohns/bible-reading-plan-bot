# Dedup report — 66 merge groups, 75 records to remove

Directory 4127 → 4052 after merges.

## Rating conflicts within dup groups (need human attention)

- **Bellevue Baptist Church** (cordova, TN): ratings = ['green', 'yellow']
  - canonical: bellevue-baptist-church-cordova-tn = green
  - dupe: bellevue-baptist-church-memphis-sbc = yellow
  - dupe: bellevue-baptist-memphis-tn = green
  - dupe: bellevue-baptist-cordova-tn = green
- **Stonebriar Community Church** (frisco, TX): ratings = ['green', 'yellow']
  - canonical: stonebriar-community-church-frisco-tx = yellow
  - dupe: stonebriar-community-church-frisco-sbc-tx = yellow
  - dupe: stonebriar-community-frisco-tx = green
- **First Orlando Baptist Church** (orlando, FL): ratings = ['green', 'yellow']
  - canonical: first-orlando-baptist-church = green
  - dupe: first-baptist-orlando-sbc-fl = yellow
  - dupe: first-baptist-orlando-fl = yellow
- **Idlewild Baptist Church** (lutz, FL): ratings = ['green', 'yellow']
  - canonical: idlewild-baptist-tampa-fl = green
  - dupe: idlewild-baptist-church-tampa-fl = green
  - dupe: idlewild-baptist-church-tampa-sbc-fl = yellow
- **Cottage Hill Baptist Church** (mobile, AL): ratings = ['green', 'yellow']
  - canonical: cottage-hill-baptist-church-mobile-sbc = green
  - dupe: cottage-hill-baptist-mobile-al = green
  - dupe: cottage-hill-baptist-mobile = yellow
- **Champion Forest Baptist Church** (houston, TX): ratings = ['green', 'yellow']
  - canonical: champion-forest-baptist-houston = green
  - dupe: champion-forest-baptist-church-houston-sbc = yellow
  - dupe: champion-forest-baptist-houston-tx = green
- **First Baptist Church of Glenarden** (upper marlboro, MD): ratings = ['red', 'yellow']
  - canonical: first-baptist-church-glenarden-md = red
  - dupe: first-baptist-glenarden-md = yellow
- **Prestonwood Baptist Church** (plano, TX): ratings = ['green', 'yellow']
  - canonical: prestonwood-baptist-church-plano-sbc = yellow
  - dupe: prestonwood-baptist-plano-tx = green
- **The Summit Church** (durham, NC): ratings = ['green', 'yellow']
  - canonical: summit-church-durham-sbc-nc = yellow
  - dupe: the-summit-church-durham-nc = green
- **Scottsdale Bible Church** (scottsdale, AZ): ratings = ['green', 'yellow']
  - canonical: scottsdale-bible-church-az = green
  - dupe: scottsdale-bible-church-sbc-az = yellow
- **Second Baptist Church Houston** (houston, TX): ratings = ['green', 'yellow']
  - canonical: second-baptist-church-houston-sbc = yellow
  - dupe: second-baptist-houston-tx = green
- **First Baptist Church Atlanta** (atlanta, GA): ratings = ['green', 'yellow']
  - canonical: first-baptist-atlanta = green
  - dupe: first-baptist-church-atlanta = yellow
- **12Stone Church** (lawrenceville, GA): ratings = ['red', 'yellow']
  - canonical: twelve-stone-lawrenceville = yellow
  - dupe: 12stone-church-lawrenceville-ga = red
- **Long Hollow Baptist Church** (hendersonville, TN): ratings = ['green', 'yellow']
  - canonical: long-hollow-baptist-church-hendersonville-sbc = yellow
  - dupe: long-hollow-baptist-hendersonville-tn = green
- **First Baptist Church Chattanooga** (chattanooga, TN): ratings = ['red', 'yellow']
  - canonical: first-baptist-chattanooga-tn = yellow
  - dupe: first-baptist-chattanooga-sbc-tn = red
- **North Valley Baptist Church** (santa clara, CA): ratings = ['green', 'yellow']
  - canonical: north-valley-baptist-santa-clara-ca = yellow
  - dupe: north-valley-baptist-church-santa-clara = green
- **First Baptist Church Hammond** (hammond, IN): ratings = ['red', 'yellow']
  - canonical: first-baptist-hammond-in = red
  - dupe: first-baptist-church-hammond-in = yellow
- **Hebron Baptist Church** (dacula, GA): ratings = ['green', 'yellow']
  - canonical: hebron-baptist-church-dacula-sbc = yellow
  - dupe: hebron-baptist-dacula-ga = green
- **Sagemont Church** (houston, TX): ratings = ['green', 'yellow']
  - canonical: sagemont-church-houston-tx = green
  - dupe: sagemont-church-houston = yellow
- **First Baptist Church Opelika** (opelika, AL): ratings = ['green', 'yellow']
  - canonical: first-baptist-church-opelika-al = yellow
  - dupe: first-baptist-opelika-al = green
- **West Jackson Baptist Church** (jackson, TN): ratings = ['green', 'yellow']
  - canonical: west-jackson-baptist-jackson-tn = green
  - dupe: west-jackson-baptist-church-jackson-sbc = yellow
- **Henderson Hills Baptist Church** (edmond, OK): ratings = ['green', 'yellow']
  - canonical: henderson-hills-baptist-edmond-ok = yellow
  - dupe: henderson-hills-baptist-church-edmond-sbc = green
- **Southern Hills Baptist Church** (oklahoma city, OK): ratings = ['green', 'yellow']
  - canonical: southern-hills-baptist-okc-ok = yellow
  - dupe: southern-hills-baptist-church-okc-sbc = green
- **Parkside Church** (chagrin falls, OH): ratings = ['green', 'yellow']
  - canonical: parkside-church-cleveland = green
  - dupe: parkside-church-chagrin-falls-oh = yellow
- **Ada Bible Church** (ada, MI): ratings = ['green', 'yellow']
  - canonical: ada-bible-church-grand-rapids-mi = green
  - dupe: ada-bible-church-ada-mi = yellow
- **Hinson Baptist Church** (portland, OR): ratings = ['green', 'yellow']
  - canonical: hinson-baptist-portland-or = green
  - dupe: hinson-baptist-church-portland-or = yellow
- **Brentwood Baptist Church** (brentwood, TN): ratings = ['green', 'yellow']
  - canonical: brentwood-baptist-church-brentwood-sbc = yellow
  - dupe: brentwood-baptist-church-brentwood-tn = green
- **New Birth Missionary Baptist Church** (lithonia, GA): ratings = ['black', 'red']
  - canonical: prog-new-birth-missionary-lithonia-ga = black
  - dupe: new-birth-missionary-baptist-lithonia-ga = red
- **Ebenezer Baptist Church** (atlanta, GA): ratings = ['black', 'red']
  - canonical: prog-ebenezer-baptist-atlanta-ga = black
  - dupe: ebenezer-baptist-church-atlanta-ga = red

## All merge groups

### Bellevue Baptist Church — cordova, TN (bellevue.org)
- **KEEP**: `bellevue-baptist-church-cordova-tn` (green, richness=57)
- REMOVE: `bellevue-baptist-church-memphis-sbc` (yellow, richness=49)
- REMOVE: `bellevue-baptist-memphis-tn` (green, richness=45)
- REMOVE: `bellevue-baptist-cordova-tn` (green, richness=43)

### First Baptist Church Dallas — dallas, TX (firstdallas.org)
- **KEEP**: `first-baptist-church-dallas-dallas-tx` (green, richness=68)
- REMOVE: `first-baptist-dallas-sbc-tx` (green, richness=62)
- REMOVE: `first-baptist-dallas-tx` (green, richness=54)

### Stonebriar Community Church — frisco, TX (stonebriar.org)
- **KEEP**: `stonebriar-community-church-frisco-tx` (yellow, richness=66)
- REMOVE: `stonebriar-community-church-frisco-sbc-tx` (yellow, richness=58)
- REMOVE: `stonebriar-community-frisco-tx` (green, richness=46)

### First Orlando Baptist Church — orlando, FL (firstorlando.com)
- **KEEP**: `first-orlando-baptist-church` (green, richness=54)
- REMOVE: `first-baptist-orlando-sbc-fl` (yellow, richness=44)
- REMOVE: `first-baptist-orlando-fl` (yellow, richness=27)

### Idlewild Baptist Church — lutz, FL (idlewild.org)
- **KEEP**: `idlewild-baptist-tampa-fl` (green, richness=84)
- REMOVE: `idlewild-baptist-church-tampa-fl` (green, richness=60)
- REMOVE: `idlewild-baptist-church-tampa-sbc-fl` (yellow, richness=45)

### Cottage Hill Baptist Church — mobile, AL (cottagehill.org)
- **KEEP**: `cottage-hill-baptist-church-mobile-sbc` (green, richness=64)
- REMOVE: `cottage-hill-baptist-mobile-al` (green, richness=48)
- REMOVE: `cottage-hill-baptist-mobile` (yellow, richness=41)

### Green Acres Baptist Church — tyler, TX (gabc.org)
- **KEEP**: `green-acres-baptist-church-tyler-sbc` (green, richness=55)
- REMOVE: `green-acres-baptist-tyler-tx` (green, richness=52)
- REMOVE: `green-acres-baptist-tyler` (green, richness=37)

### Champion Forest Baptist Church — houston, TX (championforest.org)
- **KEEP**: `champion-forest-baptist-houston` (green, richness=80)
- REMOVE: `champion-forest-baptist-church-houston-sbc` (yellow, richness=54)
- REMOVE: `champion-forest-baptist-houston-tx` (green, richness=44)

### Heritage Baptist Church — lynchburg, VA (hbclynchburg.com)
- **KEEP**: `heritage-baptist-lynchburg` (green, richness=61)
- REMOVE: `heritage-baptist-lynchburg-2` (green, richness=54)

### Redeemer Bible Church — spotsylvania, VA (redeemerva.org)
- **KEEP**: `redeemer-bible-church-spotsylvania` (green, richness=67)
- REMOVE: `redeemer-bible-church-spotsylvania-va` (green, richness=51)

### First Baptist Church of Glenarden — upper marlboro, MD (fbcglenarden.org)
- **KEEP**: `first-baptist-church-glenarden-md` (red, richness=71)
- REMOVE: `first-baptist-glenarden-md` (yellow, richness=59)

### Prestonwood Baptist Church — plano, TX (prestonwood.org)
- **KEEP**: `prestonwood-baptist-church-plano-sbc` (yellow, richness=52)
- REMOVE: `prestonwood-baptist-plano-tx` (green, richness=46)

### The Summit Church — durham, NC (summitchurch.com)
- **KEEP**: `summit-church-durham-sbc-nc` (yellow, richness=65)
- REMOVE: `the-summit-church-durham-nc` (green, richness=47)

### North Point Community Church — alpharetta, GA (northpoint.org)
- **KEEP**: `north-point-community-church-alpharetta-ga` (red, richness=73)
- REMOVE: `north-point-community-church-alpharetta` (red, richness=67)

### Scottsdale Bible Church — scottsdale, AZ (scottsdalebible.com)
- **KEEP**: `scottsdale-bible-church-az` (green, richness=89)
- REMOVE: `scottsdale-bible-church-sbc-az` (yellow, richness=42)

### Briarwood Presbyterian Church — birmingham, AL (briarwood.org)
- **KEEP**: `briarwood-presbyterian-church-birmingham-sbc` (green, richness=55)
- REMOVE: `briarwood-pca-birmingham-al` (green, richness=52)

### Second Baptist Church Houston — houston, TX (second.org)
- **KEEP**: `second-baptist-church-houston-sbc` (yellow, richness=62)
- REMOVE: `second-baptist-houston-tx` (green, richness=49)

### Coral Ridge Presbyterian Church — fort lauderdale, FL (crpc.org)
- **KEEP**: `coral-ridge-presbyterian-ft-lauderdale-fl` (green, richness=80)
- REMOVE: `coral-ridge-presbyterian-fort-lauderdale-sbc` (green, richness=54)

### First Baptist Church Atlanta — atlanta, GA (fba.org)
- **KEEP**: `first-baptist-atlanta` (green, richness=55)
- REMOVE: `first-baptist-church-atlanta` (yellow, richness=32)

### 12Stone Church — lawrenceville, GA (12stone.com)
- **KEEP**: `twelve-stone-lawrenceville` (yellow, richness=61)
- REMOVE: `12stone-church-lawrenceville-ga` (red, richness=59)

### Long Hollow Baptist Church — hendersonville, TN (longhollow.com)
- **KEEP**: `long-hollow-baptist-church-hendersonville-sbc` (yellow, richness=47)
- REMOVE: `long-hollow-baptist-hendersonville-tn` (green, richness=39)

### Clear Creek Community Church — league city, TX (clearcreek.org)
- **KEEP**: `clear-creek-community-church-league-city-tx` (yellow, richness=50)
- REMOVE: `clear-creek-community-league-city` (yellow, richness=50)

### First Baptist Church Midland — midland, TX (fbc-midland.org)
- **KEEP**: `first-baptist-midland` (yellow, richness=57)
- REMOVE: `first-baptist-midland-sbc-tx` (yellow, richness=54)

### First Baptist Church Pflugerville — pflugerville, TX (fbcpville.org)
- **KEEP**: `first-baptist-pflugerville` (yellow, richness=45)
- REMOVE: `first-baptist-pflugerville-tx` (yellow, richness=29)

### First Baptist Church Round Rock — round rock, TX (fbcrr.org)
- **KEEP**: `first-baptist-round-rock` (yellow, richness=37)
- REMOVE: `first-baptist-round-rock-tx` (yellow, richness=22)

### First Baptist Church San Marcos — san marcos, TX (sanmarcosfbc.org)
- **KEEP**: `first-baptist-san-marcos` (yellow, richness=49)
- REMOVE: `first-baptist-san-marcos-tx` (yellow, richness=30)

### First Baptist Church Temple — temple, TX (firsttemple.org)
- **KEEP**: `first-baptist-temple` (yellow, richness=42)
- REMOVE: `first-baptist-temple-tx` (yellow, richness=24)

### Sugar Creek Baptist Church — sugar land, TX (sugarcreek.net)
- **KEEP**: `sugar-creek-baptist-sugar-land` (green, richness=103)
- REMOVE: `sugar-creek-baptist-sugar-land-tx` (green, richness=71)

### First Baptist Church Amarillo — amarillo, TX (firstamarillo.org)
- **KEEP**: `first-baptist-amarillo-sbc-tx` (yellow, richness=54)
- REMOVE: `first-baptist-amarillo` (yellow, richness=51)

### First Baptist Church Starkville — starkville, MS (fbcstarkville.com)
- **KEEP**: `first-baptist-church-starkville-ms-2` (yellow, richness=60)
- REMOVE: `first-baptist-starkville-ms` (yellow, richness=49)

### First Baptist Church Columbia — columbia, SC (fbccola.com)
- **KEEP**: `first-baptist-church-columbia-sbc-sc` (green, richness=66)
- REMOVE: `first-baptist-columbia-sc` (green, richness=49)

### First Baptist Church Greenville SC — greenville, SC (firstbaptistgreenville.com)
- **KEEP**: `first-baptist-greenville-sc` (black, richness=59)
- REMOVE: `first-baptist-greenville-sbc-sc` (black, richness=58)

### First Baptist Spartanburg — spartanburg, SC (fbs.org)
- **KEEP**: `first-baptist-spartanburg-sbc-sc` (green, richness=58)
- REMOVE: `first-baptist-spartanburg-sc` (green, richness=45)

### First Baptist Church Knoxville — knoxville, TN (fbcknox.org)
- **KEEP**: `first-baptist-knoxville-sbc-tn` (red, richness=57)
- REMOVE: `first-baptist-knoxville-tn` (red, richness=47)

### First Baptist Church Chattanooga — chattanooga, TN (fbcchattanooga.org)
- **KEEP**: `first-baptist-chattanooga-tn` (yellow, richness=58)
- REMOVE: `first-baptist-chattanooga-sbc-tn` (red, richness=50)

### Immanuel Baptist Church — little rock, AR (ibclr.org)
- **KEEP**: `immanuel-baptist-little-rock-ar` (yellow, richness=44)
- REMOVE: `immanuel-baptist-church-little-rock-sbc` (yellow, richness=29)

### Lookout Mountain Presbyterian Church — lookout mountain, TN (lmpc.org)
- **KEEP**: `lookout-mountain-pca-lookout-mountain-ga` (green, richness=61)
- REMOVE: `lookout-mountain-pca-tn` (green, richness=33)

### Calvary Chapel South Bay (Calvary LIFE) — gardena, CA (calvarylife.com)
- **KEEP**: `calvary-chapel-south-bay-gardena-ca-2` (yellow, richness=59)
- REMOVE: `calvary-chapel-south-bay-gardena-ca` (yellow, richness=23)

### Lancaster Baptist Church — lancaster, CA (lancasterbaptist.org)
- **KEEP**: `lancaster-baptist-church-lancaster-ca` (yellow, richness=59)
- REMOVE: `lancaster-baptist-lancaster-ca` (yellow, richness=54)

### North Valley Baptist Church — santa clara, CA (nvbc.org)
- **KEEP**: `north-valley-baptist-santa-clara-ca` (yellow, richness=42)
- REMOVE: `north-valley-baptist-church-santa-clara` (green, richness=37)

### First Baptist Church Hammond — hammond, IN (fbchammond.com)
- **KEEP**: `first-baptist-hammond-in` (red, richness=49)
- REMOVE: `first-baptist-church-hammond-in` (yellow, richness=31)

### First Baptist Church Tallahassee — tallahassee, FL (fbctlh.org)
- **KEEP**: `first-baptist-tallahassee-fl` (yellow, richness=57)
- REMOVE: `first-baptist-tallahassee-sbc-fl` (yellow, richness=44)

### First Baptist Church Woodstock — woodstock, GA (fbcw.org)
- **KEEP**: `first-baptist-church-woodstock-ga` (green, richness=50)
- REMOVE: `first-baptist-woodstock-ga` (green, richness=44)

### Hebron Baptist Church — dacula, GA (hebronchurch.org)
- **KEEP**: `hebron-baptist-church-dacula-sbc` (yellow, richness=54)
- REMOVE: `hebron-baptist-dacula-ga` (green, richness=35)

### Thomas Road Baptist Church — lynchburg, VA (trbc.org)
- **KEEP**: `thomas-road-baptist-lynchburg-va` (green, richness=62)
- REMOVE: `thomas-road-baptist-church-lynchburg-sbc` (green, richness=50)

### First Baptist Church Edmond — edmond, OK (fbcedmond.org)
- **KEEP**: `first-baptist-church-edmond-ok` (green, richness=53)
- REMOVE: `first-baptist-edmond-ok` (green, richness=47)

### Quail Springs Baptist Church — oklahoma city, OK (qsbc.org)
- **KEEP**: `quail-springs-baptist-church-okc-sbc` (green, richness=46)
- REMOVE: `quail-springs-baptist-okc-ok` (green, richness=36)

### The Church at Brook Hills — birmingham, AL (brookhills.org)
- **KEEP**: `the-church-at-brook-hills-birmingham` (green, richness=49)
- REMOVE: `the-church-at-brook-hills-al` (green, richness=44)

### Bent Tree Bible Fellowship — carrollton, TX (benttree.org)
- **KEEP**: `bent-tree-bible-carrollton-tx` (yellow, richness=38)
- REMOVE: `bent-tree-bible-fellowship-carrollton-tx` (yellow, richness=23)

### Sagemont Church — houston, TX (sagemontchurch.org)
- **KEEP**: `sagemont-church-houston-tx` (green, richness=46)
- REMOVE: `sagemont-church-houston` (yellow, richness=32)

### Christ Fellowship Church — palm beach gardens, FL (christfellowship.church)
- **KEEP**: `christ-fellowship-palm-beach-sbc-fl` (red, richness=54)
- REMOVE: `christ-fellowship-palm-beach-fl` (red, richness=49)

### First Baptist Church Opelika — opelika, AL (fbcopelika.com)
- **KEEP**: `first-baptist-church-opelika-al` (yellow, richness=52)
- REMOVE: `first-baptist-opelika-al` (green, richness=42)

### Whitesburg Baptist Church — huntsville, AL (whitesburgbaptist.org)
- **KEEP**: `whitesburg-baptist-church-huntsville-sbc` (green, richness=64)
- REMOVE: `whitesburg-baptist-huntsville-al` (green, richness=46)

### West Jackson Baptist Church — jackson, TN (westjacksonbc.org)
- **KEEP**: `west-jackson-baptist-jackson-tn` (green, richness=69)
- REMOVE: `west-jackson-baptist-church-jackson-sbc` (yellow, richness=44)

### Shandon Baptist Church — columbia, SC (shandon.org)
- **KEEP**: `shandon-baptist-columbia-sc` (green, richness=75)
- REMOVE: `shandon-baptist-church-columbia-sbc` (green, richness=53)

### Henderson Hills Baptist Church — edmond, OK (hhbc.com)
- **KEEP**: `henderson-hills-baptist-edmond-ok` (yellow, richness=58)
- REMOVE: `henderson-hills-baptist-church-edmond-sbc` (green, richness=49)

### Southern Hills Baptist Church — oklahoma city, OK (myshbc.com)
- **KEEP**: `southern-hills-baptist-okc-ok` (yellow, richness=64)
- REMOVE: `southern-hills-baptist-church-okc-sbc` (green, richness=53)

### Parkside Church — chagrin falls, OH (parksidechurch.com)
- **KEEP**: `parkside-church-cleveland` (green, richness=65)
- REMOVE: `parkside-church-chagrin-falls-oh` (yellow, richness=33)

### Ada Bible Church — ada, MI (adabible.org)
- **KEEP**: `ada-bible-church-grand-rapids-mi` (green, richness=85)
- REMOVE: `ada-bible-church-ada-mi` (yellow, richness=44)

### Hinson Baptist Church — portland, OR (hinsonchurch.org)
- **KEEP**: `hinson-baptist-portland-or` (green, richness=82)
- REMOVE: `hinson-baptist-church-portland-or` (yellow, richness=24)

### Calvary Chapel Fort Lauderdale — fort lauderdale, FL (calvaryftl.org)
- **KEEP**: `calvary-chapel-ft-lauderdale-fort-lauderdale-fl` (yellow, richness=63)
- REMOVE: `calvary-chapel-fort-lauderdale` (yellow, richness=52)

### Calvary Chapel Las Vegas — las vegas, NV (calvarylv.com)
- **KEEP**: `calvary-chapel-las-vegas-las-vegas-nv` (yellow, richness=62)
- REMOVE: `calvary-chapel-las-vegas-nv` (yellow, richness=53)

### Brentwood Baptist Church — brentwood, TN (brentwoodbaptist.com)
- **KEEP**: `brentwood-baptist-church-brentwood-sbc` (yellow, richness=55)
- REMOVE: `brentwood-baptist-church-brentwood-tn` (green, richness=51)

### New Birth Missionary Baptist Church — lithonia, GA (newbirth.org)
- **KEEP**: `prog-new-birth-missionary-lithonia-ga` (black, richness=71)
- REMOVE: `new-birth-missionary-baptist-lithonia-ga` (red, richness=47)

### Ebenezer Baptist Church — atlanta, GA (ebenezeratl.org)
- **KEEP**: `prog-ebenezer-baptist-atlanta-ga` (black, richness=80)
- REMOVE: `ebenezer-baptist-church-atlanta-ga` (red, richness=63)

### Judson Memorial Church — new york, NY (judson.org)
- **KEEP**: `prog-judson-memorial-nyc-ny` (black, richness=31)
- REMOVE: `judson-memorial-church-nyc-ny` (black, richness=30)

