// Typically-female given names for the lead-pastor HOLD guard.
//
// One list, shared by merge-pastor-enrichments.js (the local grind) and
// apply-roster-pastor-leads.js (denominational rosters). They used to carry two
// different hand-kept lists, and each missed names the other caught: on
// 2026-10-03 the grind published "Elisabeth Chapin", "Sandy Kessinger" and
// "Lynn Carter" (her own church page says "her") as senior pastors because the
// grind's list had "elizabeth" but not "elisabeth", "sandra" but not "sandy",
// and no "lynn" at all — while the roster list did have "lynn".
//
// Conservative by design: a false positive costs one manual look, a miss puts an
// unreviewed female senior pastor on a public page.
const NAMES = `
mary patricia jennifer linda elizabeth elisabeth elisa eliza liz beth betsy barbara susan susanne suzanne sue
jessica sarah karen nancy lisa betty margaret maggie sandra sandy ashley kimberly kim emily donna michelle carol
carole amanda dorothy melissa deborah debra debbie deb stephanie rebecca becky sharon laura cynthia cindy kathleen
amy angela shirley anna anne ann brenda pamela pam emma nicole helen samantha katherine catherine kathryn kate
katie kathy cathy kathie christine christina kristina kristin kristen krista ruth rachel carolyn janet janice
jane joan joanne joann jo jodi jodie heather diane dianne diana julie julia joyce virginia victoria lauren
evelyn judith judy megan andrea cheryl hannah jacqueline martha gloria teresa theresa sara madison frances fran
jean jeanne jeanette jeannie abigail alice sophia denise amber doris marilyn danielle beverly isabella natalie
brittany charlotte kayla alexis lori annemarie annmarie maryann maryanne marianne marybeth sarahbeth leanne
deanne roseanne rose annabelle annalise annika janelle bettye tammy tanya tonya sonya wanda paula carla marcia
marsha vicki vickie peggy sally sherry terri toni traci tracy tracey wendy kelly marie grace lynn lynne lynette
dawn robin leslie shannon erin holly crystal tina stacy stacey monica allison rhonda bonnie april renee colleen
lindsay lindsey whitney courtney jenna alicia felicia regina priscilla phoebe naomi esther miriam roberta
geraldine josephine eileen lorraine constance yvonne claudia marlene gwendolyn sylvia melinda jill erica tiffany
jasmine kari kara gail gayle joy carrie connie kristy amelia lydia lucy margo marjorie meredith molly nora
maria olivia olga patti patty rosa rosemary ruby stella susie tabitha valerie vanessa vera
`.trim().split(/\s+/);

const FEMALE_FIRST = new Set(NAMES);

// First given name, skipping a leading title ("Rev. Dr. Lynn Carter" -> "lynn").
function firstGivenName(name) {
  const t = String(name || '').trim().split(/\s+/);
  let i = 0;
  while (i < t.length - 1 && /^(dr|rev|revd|reverend|pastor|fr|father|bro|brother|sis|sister|mrs|ms|miss|mr|elder|bishop|apostle|prophetess|minister)\.?$/i.test(t[i])) i++;
  return (t[i] || '').toLowerCase().replace(/[^a-z]/g, '');
}

function looksFemaleFirstName(name) {
  return FEMALE_FIRST.has(firstGivenName(name));
}

module.exports = { FEMALE_FIRST, firstGivenName, looksFemaleFirstName };
