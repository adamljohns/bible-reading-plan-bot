// Shared workflow dataset for usmcmin.org — loaded by BOTH workflows.html (active board)
// and archive.html (retired items). Single source of truth; edit here only.
// Globals: WORKFLOWS_DEFAULT, CATEGORIES, STATUS_LABELS.

const WORKFLOWS_DEFAULT = [
    {
        id: 'real-man-devotional',
        title: 'REAL MAN: 31 Days in Proverbs — Ebook Launch',
        category: 'Ministry',
        icon: '<img src="assets/icons/shield-bible.png" alt="" width="16" height="16" style="vertical-align:middle;margin-right:3px;">',
        status: 'active',
        currentStep: 3,
        steps: [
            { name: 'Write 31 Days',                desc: 'Complete all 31 devotional entries + Introduction + Conclusion. (DONE ✅)' },
            { name: 'Days 29-31 Husband Capstone',   desc: 'Rewrite Days 29-30 (REAL husband) + Day 31 WOMAN acrostic. (DONE ✅)' },
            { name: 'Three Ebook Versions',          desc: 'Create v1 (Devotional Only), v2 (Interactive + BTE links), v3 (Complete + MOOP text). (DONE ✅)' },
            { name: 'Moop Edit Pass',                desc: 'Moop reviews and edits all 31 days in Google Docs. (IN PROGRESS)' },
            { name: 'MOOP Translation Review',       desc: 'Read through MOOP translations for Proverbs 1-31, flag edits, add Hebrew.' },
            { name: 'Lexicon Gap Fill',              desc: 'Build 18 missing Hebrew word study pages for Proverbs.' },
            { name: 'QR Codes + Landing Pages',      desc: 'Generate QR codes for all 31 chapters, create static landing pages. (DONE ✅)' },
            { name: 'Branded PDF Generation',        desc: 'Build HTML template with USMC Ministries branding, logo, QR codes → export PDF.' },
            { name: 'Stripe Product Setup',          desc: 'Create Stripe product + payment link for 3 ebook tiers.' },
            { name: 'Website Sales Page',            desc: 'Build sales/landing page on usmcmin.org with purchase links.' },
            { name: 'Launch',                        desc: 'Publish and announce the REAL MAN devotional for sale. TARGET: May 1, 2026.' },
        ]
    },
    {
        id: 'usmc-mentoring-client',
        title: 'First USMC Ministries Mentorship Client',
        category: 'Ministry',
        icon: '✝️',
        status: 'active',
        currentStep: 2,
        steps: [
            { name: 'Intake Sent',           desc: 'Send intake questionnaire to mentoring client.' },
            { name: 'Intake Received',        desc: 'Client returns completed intake form.' },
            { name: 'Review & Pray',          desc: 'Review intake, pray for discernment before first session.' },
            { name: 'Schedule First Session', desc: 'Coordinate calendars and confirm session time.' },
            { name: 'Send Welcome Packet',    desc: 'Deliver welcome packet with expectations, schedule, and resources.' },
            { name: 'Set Up Billing ($150/mo)', desc: 'Configure recurring billing at $150/month.' },
            { name: 'First Session',          desc: 'Conduct first formal mentoring session.' },
            { name: 'Post-Session Follow-Up', desc: 'Send recap, action items, and next session date.' },
            { name: 'Monthly Cadence',        desc: 'Enter regular monthly session rhythm.' },
            { name: '90-Day Review',          desc: 'Evaluate progress, goals, and continuation.' },
        ]
    },
    {
        id: 'airbnb-guest-workflow',
        title: 'Airbnb Guest — Stay Workflow',
        category: 'Business',
        icon: '🏠',
        status: 'active',
        currentStep: 0,
        steps: [
            { name: 'Reservation Confirmed', desc: 'Airbnb booking confirmed, review details.' },
            { name: 'Pre-Arrival Message',   desc: 'Send check-in instructions and welcome message 24–48h before arrival.' },
            { name: 'Prep Unit',             desc: 'Clean, stock supplies, ensure everything is ready.' },
            { name: 'Check-In Day',          desc: 'Confirm smooth check-in, answer any questions.' },
            { name: 'During Stay',           desc: 'Monitor messages, address any mid-stay issues.' },
            { name: 'Checkout',              desc: 'Guest checks out. Inspect unit.' },
            { name: 'Request Review',        desc: 'Message guest requesting a 5-star review.' },
            { name: 'Post-Stay Follow-Up',   desc: 'Note any maintenance items, update unit if needed.' },
        ]
    },
    {
        id: 'tenant-onboarding',
        title: 'Tenant Onboarding',
        category: 'Business',
        icon: '🔑',
        status: 'active',
        currentStep: 0,
        steps: [
            { name: 'Call About Flex Dates', desc: 'Discuss flexible move-in date options with tenant.' },
            { name: 'Confirm Move-In Date',  desc: 'Lock in the official move-in date.' },
            { name: 'Install Blinds',        desc: 'Install window blinds before move-in.' },
            { name: 'Deep Clean',            desc: 'Complete deep clean of the unit.' },
            { name: 'Welcome Packet',        desc: 'Prepare and deliver tenant welcome packet with rules, contacts, utilities.' },
            { name: 'Key Handoff',           desc: 'Hand over keys, do walkthrough with tenant.' },
        ]
    },
    {
        id: 'boi-redemption',
        title: 'BOI Redemption',
        category: 'Personal',
        icon: '⚖️',
        status: 'active',
        currentStep: 1,
        steps: [
            { name: 'Locate Files',              desc: 'Find all relevant BOI files, documents, and recordings.' },
            { name: 'Transcribe Audio (7 parts)', desc: 'Transcribe all 7 audio recordings for accurate documentation.' },
            { name: 'Build Timeline',             desc: 'Construct chronological timeline of events.' },
            { name: 'Organize Evidence',          desc: 'Sort and organize all evidence by category and date.' },
            { name: 'Legal Review',               desc: 'Review case with legal advisor.' },
            { name: 'Draft Claim',                desc: 'Write formal claim document.' },
            { name: 'Submit',                     desc: 'File and submit the claim through proper channels.' },
            { name: 'Follow Up',                  desc: 'Track submission status and follow up as needed.' },
            { name: 'Resolution',                 desc: 'Receive and document final resolution.' },
        ]
    },


    {
        id: 'direct-booking-launch',
        title: 'Direct Booking & Payments (Bow & Arrow)',
        category: 'Business',
        icon: '<img src="assets/icons/shield-calendar.png" alt="" width="16" height="16" style="vertical-align:middle;margin-right:3px;">',
        status: 'active',
        currentStep: 3,
        steps: [
            { name: 'Build direct-booking page', desc: 'Live at usmcmin.com/direct-booking.html. Migrated OFF the ministry domain — usmcmin.org/stays/ now redirects here. (DONE ✅)' },
            { name: 'Real photos + full listings', desc: '3 Historic-District apartments + combined #6/#8 + 1405 Sunken Rd mid-term, with real B&A photography. (DONE ✅)' },
            { name: 'Add Car Rental section (Turo + Direct)', desc: 'Vehicle-rental section scaffolded on the booking page — Bow & Arrow LLC. (DONE ✅ — still need the Turo host URL + fleet photos.)' },
            { name: 'Set up payments — Bow & Arrow ONLY', desc: 'Stripe under Bow & Arrow Studio LLC (EIN 87-2937218) → deposits to a B&A bank. NEVER route to USMC (88-1966617) or C5iSR (92-3564161). (IN PROGRESS — Adam to create the Stripe account.)' },
            { name: 'Test booking + payment flow', desc: 'Run a real inquiry → quote → payment end-to-end before promoting.' },
            { name: 'Take Turo listing live', desc: 'Publish the Turo host page; replace the "Reserve a Vehicle" inquire placeholder with the live Turo URL.' },
            { name: 'Promote', desc: 'Add the direct-booking link to Airbnb checkout messages, bio, social, and the past-guest list.' },
            { name: '(Future) separate coaching/AI payment surfaces', desc: 'Ministry coaching → its own surface under USMC (coaching.html); AI support → C5iSR. Keep these OFF the B&A booking page to avoid crossing entity streams.' },
        ]
    },
    {
        id: 'counseling-service-launch',
        title: 'Counseling Service Launch',
        category: 'Ministry',
        icon: '🤝',
        status: 'active',
        currentStep: 4,
        steps: [
            { name: 'Intake Form Ready',       desc: 'Build and publish counseling intake form.' },
            { name: 'Define Pricing',           desc: 'Set counseling session rates and packages.' },
            { name: 'Build Welcome Packet',     desc: 'Create client welcome packet with expectations, consent, policies.' },
            { name: 'Set Up Scheduling',        desc: 'Configure scheduling tool (Calendly or similar).' },
            { name: 'First Client Onboarded',   desc: 'Successfully onboard the first paying counseling client.' },
        ]
    },
    // ── Ministry ──
    {
        id: 'bte-lexicon-expansion',
        title: 'BTE Lexicon Expansion',
        category: 'Ministry',
        icon: '<img src="assets/icons/shield-bible.png" alt="" width="16" height="16" style="vertical-align:middle;margin-right:3px;">',
        status: 'complete',
        currentStep: 5,
        steps: [
            { name: 'Initial 487 pages',     desc: 'Starting baseline: BTE lexicon at 487 pages.' },
            { name: '1,000 pages',           desc: 'Expand lexicon to 1,000 pages.' },
            { name: '3,000 pages',           desc: 'Continue expansion to 3,000 pages. Current: ~3,012 ✅' },
            { name: '5,000 pages',           desc: 'Push to 5,000 pages.' },
            { name: '7,700 pages (target)',  desc: 'Reach 7,700-page target — full BTE Lexicon complete.' },
        ]
    },
    {
        id: 'bte-crossref-expansion',
        title: 'BTE Cross-Reference Expansion',
        category: 'Ministry',
        icon: '🔗',
        status: 'active',
        currentStep: 4,
        steps: [
            { name: 'Initial 700',                desc: 'Starting baseline: 700 cross-references.' },
            { name: '10,000 refs',                desc: 'Expand to 10,000 cross-references.' },
            { name: '17,777 source verses',       desc: '17,777 distinct source verses linked. (DONE ✅ — 17,777/17,777, 100%)' },
            { name: '71,777 chain refs',          desc: 'Chain cross-references expanded to 71,777. (DONE ✅ — target hit)' },
            { name: 'Christological saturation',  desc: 'Ongoing: deepen Christ-centered cross-reference saturation across all 66 books.' },
        ]
    },
    {
        id: 'moop-dictionary',
        title: 'MOOP Dictionary',
        category: 'Ministry',
        icon: '<img src="assets/icons/shield-book.png" alt="" width="16" height="16" style="vertical-align:middle;margin-right:3px;">',
        status: 'active',
        currentStep: 4,
        steps: [
            { name: 'Initial 100 words',     desc: 'Starting baseline: 100 dictionary entries.' },
            { name: '1,000 words',           desc: 'Expand to 1,000 entries.' },
            { name: '2,500 words',           desc: 'Expand to 2,500 entries.' },
            { name: '5,000 words',           desc: 'Expand to 5,000 entries. Current: ~5,139 ✅' },
            { name: '7,777 words (target)',  desc: 'Reach the 7,777-entry target — full interconnected biblical word web.' },
        ]
    },
    {
        id: 'operation-watchman-pwa',
        title: 'Operation Watchman PWA',
        category: 'Ministry',
        icon: '<img src="assets/icons/shield-chain-sword-48.png" alt="" width="16" height="16" style="vertical-align:middle;margin-right:3px;">',
        status: 'active',
        currentStep: 0,
        steps: [
            { name: 'PWA Deployed',              desc: 'Progressive Web App live and accessible. (DONE ✅)' },
            { name: '4 Seasons Content',          desc: 'Build out all 4 seasons of content.' },
            { name: 'Daily Readings Integration', desc: 'Integrate daily Bible readings into the PWA.' },
            { name: 'Subscriber System',          desc: 'Set up subscriber/notification system.' },
            { name: 'Launch',                     desc: 'Official public launch of Operation Watchman.' },
        ]
    },
    {
        id: 'outreach-contact-tracker',
        title: 'Ministry Outreach Contact Tracker',
        category: 'Ministry',
        icon: '<img src="assets/icons/shield-broadcast-48.png" alt="" width="16" height="16" style="vertical-align:middle;margin-right:3px;">',
        status: 'active',
        currentStep: 2,
        steps: [
            { name: 'Tracker built', desc: 'Contact tracker live at usmcmin.org/contacts.html ("MOOP Command"). (DONE ✅)' },
            { name: 'Contacts imported', desc: '488 imported from the macOS Address Book — but 482 are tagged Personal, not ministry outreach. (DONE ✅)' },
            { name: 'Segment by entity/purpose', desc: 'Split Personal contacts out to the new Personal Outreach tracker (usmcmin.com/personal-outreach.html); keep only true ministry + civic contacts here. (IN PROGRESS — the ~2,000-contact address-book grind.) Relates to: Chaplain Chuck (ministry), Sheriff Roy (civic), Sally Mae (B&A clients).' },
            { name: 'Curate ministry-outreach list', desc: 'Build the real opt-in ministry list — people who actually want USMC Ministries outreach.' },
            { name: 'Email campaigns (opt-in only)', desc: 'Launch outreach ONLY to opted-in ministry contacts — never blast the imported personal address book (CAN-SPAM + relational risk).' },
        ]
    },
    {
        id: 'personal-outreach-tracker',
        title: 'Personal Outreach Tracker (Family & Friends)',
        category: 'Personal',
        icon: '👨‍👩‍👧‍👦',
        status: 'active',
        currentStep: 1,
        steps: [
            { name: 'Build the tracker', desc: 'Cadence-based family/friends tracker live at usmcmin.com/personal-outreach.html (PIN-gated; relationship, cadence, last-contacted, "Reach Out Soon"). (DONE ✅)' },
            { name: 'Populate real people', desc: 'Replace the example entries with real family + friends; set each cadence (weekly → yearly). Pull from the personal slice of the address-book grind.' },
            { name: 'Work the cadence', desc: 'Use the "Reach Out Soon" panel; log each touch so the next auto-schedules. Export periodically to back up.' },
        ]
    },
    {
        id: 'blog-publishing',
        title: 'Blog Publishing',
        category: 'Ministry',
        icon: '✍️',
        status: 'complete',
        currentStep: 5,
        steps: [
            { name: '149 posts migrated',          desc: 'All 149 existing posts migrated to new platform.' },
            { name: '2 new drafts written',        desc: 'Write 2 new blog post drafts. (In progress)' },
            { name: 'Images added',                desc: 'Add featured and inline images to new posts.' },
            { name: 'Published to index',          desc: 'Publish posts and add to blog index.' },
            { name: 'Verse refs linked to BTE',    desc: 'Link all scripture references to BTE entries.' },
        ]
    },
    {
        id: 'wedding-officiant-page',
        title: 'Wedding Officiant Page',
        category: 'Ministry',
        icon: '💍',
        status: 'active',
        currentStep: 0,
        steps: [
            { name: 'Design',          desc: 'Design the wedding officiant page layout and copy.' },
            { name: 'Build page',      desc: 'Build the page on usmcmin.org.' },
            { name: 'Add intake form', desc: 'Add wedding inquiry/intake form.' },
            { name: 'Publish',         desc: 'Publish and promote the page.' },
        ]
    },
    // ── Business ──
    {
        id: 'airbnb-photo-enhancement',
        title: 'Airbnb Photo Enhancement',
        category: 'Business',
        icon: '📸',
        status: 'active',
        currentStep: 0,
        steps: [
            { name: 'Research AI color theory', desc: 'Study AI-assisted photo enhancement and color science for STR listings.' },
            { name: 'Select listings',          desc: 'Choose which Airbnb listings to enhance first.' },
            { name: 'Edit photos',              desc: 'Apply enhancements using selected tools/techniques.' },
            { name: 'Upload',                   desc: 'Upload enhanced photos to Airbnb listings.' },
            { name: 'Monitor booking impact',   desc: 'Track booking rates before/after to measure uplift.' },
        ]
    },
    {
        id: 'airbnb-pricing-analysis',
        title: 'Airbnb Pricing Analysis',
        category: 'Business',
        icon: '<img src="assets/icons/shield-finance.png" alt="" width="16" height="16" style="vertical-align:middle;margin-right:3px;">',
        status: 'active',
        currentStep: 0,
        steps: [
            { name: 'Export CSV',        desc: 'Export pricing and booking data from Airbnb.' },
            { name: 'Competitor scrape', desc: 'Scrape competitor listing prices in target markets.' },
            { name: 'Analysis',          desc: 'Analyze data to identify pricing gaps and opportunities.' },
            { name: 'Adjust pricing',    desc: 'Update listing prices based on analysis.' },
            { name: 'Monitor',           desc: 'Track booking impact of pricing changes.' },
        ]
    },
    {
        id: 'airbnb-slow-season',
        title: 'Airbnb Slow Season Strategy',
        category: 'Business',
        icon: '📉',
        status: 'active',
        currentStep: 0,
        steps: [
            { name: 'Set Length-of-Stay Discounts', desc: 'Configure 7-day (10%), 14-day (15%), 28-day (20%) discounts for slow months (Jan-Mar, Jul-Sep) on all 5 active listings.' },
            { name: 'Audit Hero Photos', desc: 'Screenshot each listing in Airbnb search results. Check thumbnail visibility and "color bombing" — does the photo POP or blend in?' },
            { name: 'Add Bottleneck Amenity', desc: 'Add one unique amenity per property that competitors don\'t have (vintage record player, curated FXBG history bookshelf, fire pit, etc.).' },
            { name: 'Check Search-to-Listing CTR', desc: 'Review Airbnb analytics for each listing. Target: >2% CTR. If below, hero photo needs work.' },
            { name: 'Set 1-Night Minimum (Weekdays)', desc: 'Allow 1-night stays on slow weekday nights to capture gap bookings.' },
            { name: 'List on Whimstay', desc: 'Sign up at whimstay.com. Only 5% commission vs Airbnb\'s 15%. Specializes in last-minute bookings.' },
            { name: 'Review & Adjust Monthly', desc: 'Monthly check: occupancy rate, ADR, and revenue vs previous month. Adjust strategy.' },
        ]
    },
    {
        id: 'airbnb-listing-optimization',
        title: 'Airbnb Listing Optimization (Per Property)',
        category: 'Business',
        icon: '<img src="assets/icons/shield-target.png" alt="" width="16" height="16" style="vertical-align:middle;margin-right:3px;">',
        status: 'active',
        currentStep: 0,
        steps: [
            { name: 'Title Rewrite', desc: 'Rewrite titles: lead with unique selling point, include "Historic Downtown FXBG." Drop bedroom/bath count (already shown by Airbnb).' },
            { name: 'Hero Photo Test', desc: 'Test new hero photo with strong single color ("color bombing"). Check CTR after 2 weeks.' },
            { name: 'First 5 Photos Audit', desc: 'First 5 photos must show: 1) Hero/wow shot 2) Living space 3) Kitchen 4) Bedroom 5) Unique feature. Order matters — guests scroll in order.' },
            { name: 'Description Refresh', desc: 'Rewrite description: lead with experience, not specs. "Walk to 20+ restaurants" > "2BR/1BA apartment."' },
            { name: 'Amenity Audit', desc: 'Compare amenities list to top 5 competitors. Add anything missing that you actually have.' },
            { name: 'Review Response Blitz', desc: 'Respond to every review (positive and negative) within 24h. Professional, warm, specific.' },
            { name: 'Pricing Game Theory', desc: 'Don\'t just follow PriceLabs — be the outlier. Higher price + better photos + unique amenity beats the race to the bottom.' },
        ]
    },
    {
        id: 'airbnb-ai-implementation',
        title: 'Airbnb AI Implementation',
        category: 'Business',
        icon: '🤖',
        status: 'active',
        currentStep: 2,
        steps: [
            { name: 'Automated Guest Messaging', desc: 'Set up cron-driven pre-arrival, welcome, mid-stay, checkout, and review-request messages. (DONE ✅)' },
            { name: 'Daily Digest Cron', desc: 'Automated daily Airbnb digest pulling from calendar + messages. (DONE ✅)' },
            { name: 'Listing Description Generator', desc: 'Use AI to generate/test listing descriptions optimized for conversion.' },
            { name: 'Review Response Templates', desc: 'Build AI-powered review response system — personalized, not generic.' },
            { name: 'Pricing Analysis Reports', desc: 'Weekly AI-generated pricing report comparing your rates to market.' },
            { name: 'Guest Communication Playbook', desc: 'Document all message templates and triggers in a playbook for consistency.' },
            { name: 'Full Ops Dashboard', desc: 'Integrate all Airbnb data into the Bow & Arrow Studio OS dashboard.' },
        ]
    },
    {
        id: 'vrbo-expansion',
        title: 'VRBO / Multi-Platform Expansion',
        category: 'Business',
        icon: '🌐',
        status: 'active',
        currentStep: 0,
        steps: [
            { name: 'Create VRBO Account', desc: 'Set up Bow & Arrow Studio on VRBO/Vrbo.' },
            { name: 'List 2 Properties', desc: 'Start with Prof Row Cottage and Apt #7 (Boho) — best-performing listings.' },
            { name: 'Sync Calendars', desc: 'Set up iCal sync between Airbnb and VRBO to prevent double bookings.' },
            { name: 'Whimstay Signup', desc: 'List properties on Whimstay (5% commission, last-minute focus).' },
            { name: 'Channel Manager Evaluation', desc: 'Evaluate channel managers (Hospitable, Guesty, etc.) for multi-platform management.' },
            { name: 'Full Portfolio on 3+ Platforms', desc: 'All active listings on Airbnb + VRBO + Whimstay minimum.' },
        ]
    },
    {
        id: 'email-autopilot-v3',
        title: 'Email Autopilot v3',
        category: 'Business',
        icon: '📧',
        status: 'active',
        currentStep: 3,
        steps: [
            { name: 'v1 built',                 desc: 'Initial Email Autopilot version built.' },
            { name: 'v2 working',               desc: 'v2 working with improved logic.' },
            { name: 'v3 smart triage rebuilt',  desc: 'v3 smart triage system rebuilt. (In progress)' },
            { name: 'Test 1 week',              desc: 'Run v3 in production for 1 full week.' },
            { name: 'Add iMessage delivery',    desc: 'Integrate iMessage delivery channel.' },
            { name: 'Production',               desc: 'Full production deployment of Email Autopilot v3.' },
        ]
    },
    // ── Personal / Family ──
    {
        id: 'hd-organization',
        title: 'HD Organization',
        category: 'Personal',
        icon: '💾',
        status: 'active',
        currentStep: 2,
        steps: [
            { name: 'Phase 1 done (255GB)',              desc: 'Phase 1 cleanup complete — 255GB organized.' },
            { name: 'Phase 2 cleanup done',              desc: 'Phase 2 cleanup complete.' },
            { name: 'Phase 3: deep sort e-Toolbox (118GB)', desc: 'Deep sort e-Toolbox folder (118GB). (In progress)' },
            { name: 'Phase 3: deep sort Work Files (88GB)', desc: 'Deep sort Work Files folder (88GB).' },
            { name: 'Dedup',                             desc: 'Run deduplication across all organized drives.' },
            { name: 'Complete',                          desc: 'Full HD organization complete.' },
        ]
    },
    {
        id: 'boaz-formation-binder',
        title: 'Boaz Formation Binder',
        category: 'Family',
        icon: '📓',
        status: 'active',
        currentStep: 1,
        steps: [
            { name: 'Design doc written',     desc: 'Write the formation binder design document.' },
            { name: 'Review with Moop',       desc: 'Review design doc and refine.' },
            { name: 'Customize for Boaz',     desc: 'Personalize binder content for Boaz.' },
            { name: 'Print/present',          desc: 'Print and present the binder to Boaz.' },
            { name: 'Begin tracking',         desc: 'Start using binder for active formation tracking.' },
        ]
    },
    {
        id: 'job-search',
        title: 'Job Search',
        category: 'Personal',
        icon: '💼',
        status: 'active',
        currentStep: 1,
        steps: [
            { name: "St George's applied",      desc: "Applied to St George's position." },
            { name: 'Spotswood meeting Mar 26', desc: 'Meeting scheduled for March 26. (In progress)' },
            { name: 'Follow-up emails',         desc: 'Send follow-up emails after meetings.' },
            { name: 'Expand search',            desc: 'Broaden job search to additional opportunities.' },
            { name: 'Offer',                    desc: 'Receive and evaluate job offer.' },
        ]
    },
    {
        id: 'boi-audio-transcription',
        title: 'BOI Audio Transcription',
        category: 'Personal',
        icon: '🎙️',
        status: 'active',
        currentStep: 0,
        steps: [
            { name: 'Locate files',              desc: 'Find all BOI audio recording files.' },
            { name: 'Part 7 first (smallest)',   desc: 'Transcribe Part 7 first (smallest file) as a test run.' },
            { name: 'Parts 1–6',                 desc: 'Transcribe remaining Parts 1 through 6.' },
            { name: 'Build timeline',            desc: 'Construct chronological timeline from transcripts.' },
            { name: 'Legal review',              desc: 'Review transcripts and timeline with legal advisor.' },
        ]
    },
    {
        id: 'kings-point-reunion',
        title: 'Kings Point 25th Reunion',
        category: 'Personal',
        icon: '⚓',
        status: 'active',
        currentStep: 0,
        steps: [
            { name: 'Research date',  desc: 'Find official reunion date and details.' },
            { name: 'Plan travel',    desc: 'Book flights/hotel and plan travel logistics.' },
            { name: 'RSVP',           desc: 'Officially RSVP to the reunion.' },
            { name: 'Attend',         desc: 'Attend the Kings Point 25th Reunion.' },
        ]
    },
    {
        id: 'usmc-trademark',
        title: 'USMC Ministries Trademark Registration',
        category: 'Ministry',
        icon: '⚖️',
        status: 'active',
        currentStep: 1,
        steps: [
            { name: 'Confirm state registration', desc: 'Verify USMC Ministries is registered with Virginia State Corporation Commission. EIN: 88-1966617 (per Northwest Registered Agent records — NOT 92-3564161, which is C5iSR LLC).' },
            { name: 'TEAS search', desc: 'Run USPTO TEAS trademark search for "USMC Ministries" and "Uniting Serving Mentoring Counseling Ministries" to confirm no conflicts.' },
            { name: 'Confirm acronym distinction', desc: 'Document legal basis: USMC = Uniting, Serving, Mentoring, Counseling — distinct from United States Marine Corps. Acronyms not inherently protectable; full name is the mark.' },
            { name: 'Select filing class', desc: 'IC 041 — Religious education/services. IC 045 — Religious organization/ministry services. File in both.' },
            { name: 'Prepare TEAS Plus application', desc: 'File via USPTO TEAS Plus (~$250/class). Include: mark name, owner (Adam Johns or USMC Ministries), goods/services description, first use in commerce date (~2021-2022).' },
            { name: 'File with USPTO', desc: 'Submit TEAS Plus application online at teas.uspto.gov. Target: by April 30, 2026.' },
            { name: 'Monitor application', desc: 'USPTO review takes 8-12 months. Watch for office actions. Respond within 3 months of any office action.' },
            { name: 'Publication & registration', desc: 'Mark published in Official Gazette. 30-day opposition window. If no opposition, certificate issued.' },
        ]
    },
    {
        id: 'purity-ministry',
        title: "Freedom Group — Men's Purity Ministry",
        category: 'Ministry',
        icon: '🛡️',
        status: 'active',
        currentStep: 4,
        steps: [
            { name: 'Build /freedom/ site', desc: 'Public Freedom Group site at usmcmin.org/freedom/ — index, about, FAQ, resources, contact. (DONE ✅)' },
            { name: 'Accountability intake + confidentiality', desc: 'freedom/intake.html (men sign up → email notify) + signed confidentiality agreement. (DONE ✅)' },
            { name: 'Resources page', desc: 'freedom/resources.html — surveys, podcasts, articles, partner resources (Noble Warriors framework). (DONE ✅)' },
            { name: '12-week curriculum authored', desc: '3 phases (Foundation 1–4 / Formation 5–9 / Commissioning 10–12); all 12 weeks have Core Principle, Key Action, and discussion in freedom/curriculum.html. (DONE ✅)' },
            { name: 'Review & finalize curriculum', desc: 'Adam reviews/refines the drafted weeks (esp. 3 and 5–12) before teaching; optionally promote standout weeks to full standalone pages (cf. week-4.html). (IN PROGRESS)' },
            { name: 'Confirm launch logistics with Dr. Dan Cook', desc: 'Lock date, room, and Wednesday cadence with Spotswood Baptist. Contact freedom@spotswood.org.' },
            { name: 'Recruit & announce cohort', desc: 'Announcement to the men; intake → Battle Buddies assigned by Week 3; phones-in-the-box ground rules set.' },
            { name: 'Run full 12-week cohort', desc: 'Weekly Wednesday sessions. Track attendance, follow up with absent men, document testimonies.' },
            { name: 'Evaluate & commission', desc: 'Post-cohort review, gather testimonies, commission new leaders (2 Tim 2:2), plan next cohort or expand to other churches.' },
        ]
    },
    {
        id: 'disney-trip-2',
        title: 'Disney Trip Planning',
        category: 'Family',
        icon: '🏰',
        status: 'complete',
        archived: true,
        currentStep: 4,
        steps: [
            { name: 'Tickets paid',         desc: 'Disney park tickets purchased for the family. (DONE ✅)' },
            { name: 'Plan daily itinerary', desc: 'Research rides, shows, dining — build day-by-day plan.' },
            { name: 'Pack list',            desc: 'Create and complete family packing list.' },
            { name: 'Travel',               desc: 'Travel to Disney and execute the trip.' },
        ]
    },
];

const CATEGORIES = ['All', 'Ministry', 'Business', 'Family', 'Personal'];

const STATUS_LABELS = {
    active:   { icon: '🟢', label: 'Active',   cls: 'status-active' },
    waiting:  { icon: '🟡', label: 'Waiting',  cls: 'status-waiting' },
    blocked:  { icon: '🔴', label: 'Blocked',  cls: 'status-blocked' },
    complete: { icon: '✅', label: 'Complete', cls: 'status-complete' },
};
