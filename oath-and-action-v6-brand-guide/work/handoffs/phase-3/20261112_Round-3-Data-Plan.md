# Round 3 data plan

Oath & Action Edition 06, Phase 3, round 1. Research lead, November 12, 2026, for the data visualization lead's sign-off. Paths are relative to `oath-and-action-v6-brand-guide/`.

## What this plan settles

Round 3 builds 32 of chapter 14's 127 forms: behavior, structure, relationships, flow and maps (coverage plan sections 3.10 to 3.14; chapter 14 rules 14.93 to 14.124 in `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`). This plan gives each one its reader question, dataset, publisher, period, geography, atlas domain, states and status, in the shape of the rounds 1 and 2 plan. It then counts Rule 01.9 for chapter 14 as a whole, rounds 0 to 4, names the map geometry with its source and rights, and lists what I fetch and freeze once you sign off.

Rows continue the rounds 1 and 2 plan's numbering, 83 to 114, in rule order.

Status words, as before:

- **Primary**: the publisher's own file or API.
- **V7**: Atlas V7, snapshot of October 15, 2026, read by script.
- **Secondary**: a labeled secondary source (Ballotpedia, D2-99).
- **Built Snn**: one of the 16 Phase 2 specimens rebuilt in round 0; it becomes an entry.
- **Rule only**: a reference sketch or an avoid entry; it draws no dataset.
- **Download**: a primary file Dustin saves, because the publisher refuses this container (DR-230).

Nothing in round 3 is Illustrative.

## How I counted (Rule 01.9 and Rule 01.12)

The six counting rules of the rounds 1 and 2 plan stand as signed off: one data-bearing specimen is one example; each takes the one domain its reader question belongs to; atlas-wide specimens count in the total and in no domain; a state counts when it is the subject, named in the title, or lit on the chart; charts of who reports voting count under taking part. Reference sketches and avoid entries draw no data and are left out.

Two additions for round 3:

1. **Maps of every state or county alike** count toward no state, as before. A map that singles out one state (the district map, the locator) counts once toward it.
2. **Domains follow V7's own issue for the topic** wherever V7 has one, named in each row's reason: V7 files paperwork that pushes people off benefits under Congress, agencies and public services (I062), slow internet under news, records and public information (I015), drug middlemen under competition (I084), utility networks under competition (I093), shutdowns under Congress and agencies (I054), and the minimum wage under work and pay (I104).

Limits. Rounds 0 to 3 hold 84 examples: one in four is 21, one in five is 16.8, so no domain may supply more than 21 and no state more than 16. Chapter 14 as a whole holds about 95: no domain more than 23, no state more than 19. (Research lead, round 2 review fix pass, November 12, 2026: superseded. The round 4 plan counts 108 examples for the chapter, 84 specimens in rounds 0 to 3, 13 rule plates and round 4’s 11, so no domain may supply more than 27 and no state more than 21; see the note under "Rule 01.9 count for chapter 14".)

## Round 3: 32 forms

Family 3.10 Behavior, 3.11 Structure, 3.12 Relationships, 3.13 Flow, 3.14 Maps.

| # | Rule | Form | Tier | Reader question | Dataset (file in `work/build/data/`) | Publisher | Period | Geography | Domain | States | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 83 | 14.93 | Funnel | Extended | Of the people whose Medicaid or CHIP coverage came up for renewal, how many had a decision, how many were not cut off for paperwork, and how many kept coverage? | `cms-medicaid-chip-renewal-outcomes` (monthly, as published) and `cms-medicaid-chip-renewal-funnel` (derived: the nested stages) | Centers for Medicare & Medicaid Services, Medicaid and CHIP Updated Renewal Outcomes (data.medicaid.gov) | The unwinding's reporting months, as CMS's file gives them | United States, summed from the states' reports | Congress, agencies and public services (V7 I062) | None | Primary |
| 84 | 14.94 | Cohort chart | Reference | | | | | | | | Rule only |
| 85 | 14.95 | Survival curve | Reference | | | | | | | | Rule only |
| 86 | 14.96 | Process diagram | Core | How does a federal agency make or change a rule, and where can Congress or a court step in? | `govinfo-federal-rulemaking-steps` | U.S. Code, 5 U.S.C. 551 and 553 (rule making), 701 to 706 (court review) and 801 to 808 (Congressional Review Act), from govinfo; Executive Order 12866 as in force on the retrieval date, with Executive Order 14215 of February 18, 2025 (V7 X14, source Q514), from the Federal Register on govinfo | Law in force on the retrieval date | United States | Checks on power and equal justice (V7's "Agency law" subsystem) | None | Primary |
| 87 | 14.97 | Decision tree | Core | Can my city switch its own elections to ranked-choice voting? (The first branch asks whether a state ban reaches city elections.) | `ballotpedia-rcv-prohibitions-by-state` (frozen) and `v7-rcv-local-routes` (new) | Ballotpedia, labeled secondary; Atlas V7, Reforms R-01 and R-02, route LOC | Bans as of the fetch date, re-confirmed after the November 3, 2026 election; routes, snapshot October 15, 2026 | 50 states and DC | Elections and representation | Ohio and Tennessee, if the tree names the two partial bans | Secondary and V7 |
| 88 | 14.98 | Who-decides diagram | Core | Who sets my electric bill, and who can change the rules behind it? | `v7-pathway-electric-decision-makers` | Atlas V7, pathway PW03, "Electric and utility bills", its decision makers | Snapshot October 15, 2026 | United States | Competition and market power (V7 I093) | None | V7 |
| 89 | 14.99 | Org chart | Extended | How is the House divided into committees and subcommittees? | `clerk-house-committees-119` | Clerk of the House, committee and subcommittee list (MemberData.xml) | 119th Congress, on the retrieval date | United States | Congress, agencies and public services | None | Primary |
| 90 | 14.100 | Hierarchy tree | Extended | Which federal court hears a case from my state, and where does an appeal go? | `uscode-federal-courts-circuits-districts`, with authorized judgeships | U.S. Code, 28 U.S.C. 41 and 44 (circuits and their judgeships), 81 to 131 and 133 (districts and their judgeships), from govinfo; the territorial courts of Guam, the Virgin Islands and the Northern Mariana Islands from Title 48, cited as courts that are not Article III courts | Law in force on the retrieval date | 50 states, DC and the territories | Checks on power and equal justice (V7's "Courts" subsystem) | None | Primary |
| 91 | 14.101 | Comparison grid | Extended | Which of the eleven routes can carry a reform, and what does each one take? | `v7-routes` (new) and `usgov-route-requirements` (new) | Atlas V7, its eleven routes; the Constitution, statutes and official pages behind each route's threshold (`work/research/20261111_Policy-Workflow-Sources.md`) | Snapshot October 15, 2026; law on the retrieval date | United States | Atlas-wide | None | V7 and Primary |
| 92 | 14.102 | Roll-call grid | Extended | How did each senator and representative vote on the November 2025 bill that ended the shutdown? | `congress-hr5371-roll-calls-by-member` | U.S. Senate roll call vote XML and Clerk of the House roll call XML, H.R. 5371 | November 2025 | United States | Congress, agencies and public services (V7 I054) | None | Primary |
| 93 | 14.103 | Mind map | Reference | | | | | | | | Rule only |
| 94 | 14.104 | Network diagram | Extended | Where did each 2024 presidential nominee's joint fundraising committee send what it raised? | `fec-jfc-transfers-2024` | Federal Election Commission, Schedule B, API. Each nominee's committee is the one that transferred the most to the nominee's principal campaign committee in the cycle, read the same way for both | 2023 to 2024 election cycle | United States | Money, lobbying and influence | None | Primary |
| 95 | 14.105 | Adjacency matrix | Extended | Which parts of the atlas connect to which? | `v7-links-with-regions` and `v7-region-connection-matrix` (derived) | Atlas V7, its 118 connections and the region of each end (V7's ten regions: core A, B, C, D, E and X; three economy; one technology) | Snapshot October 15, 2026 | United States | Atlas-wide | None | V7 |
| 96 | 14.106 | Arc diagram | Extended | Which House bills to rein in drug middlemen drew the same backers? | `congress-gov-pbm-bills-119`, `congress-gov-pbm-bill-backers-119` and `congress-gov-pbm-bill-shared-backers-119` (derived) | Library of Congress, Congress.gov API: bills of the 119th Congress with any listed title (official, short or popular) that names "pharmacy benefit manager" or "PBM", with sponsors and cosponsors; the chamber with more matching bills is drawn and the other listed in the table | 119th Congress, to the retrieval date | United States | Competition and market power (V7 I084) | None | Primary |
| 97 | 14.107 | Chord diagram | Reference | | | | | | | | Rule only |
| 98 | 14.108 | Multi-network | Reference | | | | | | | | Rule only |
| 99 | 14.109 | Symmetrical links | Reference | | | | | | | | Rule only |
| 100 | 14.110 | Sankey | Extended | Where did the money for 2024 House campaigns come from, and where did it go? | `fec-house-campaigns-2024-by-candidate` and `fec-house-campaigns-2024-money-in-out` (derived) | Federal Election Commission, candidate financial totals for every House candidate's principal campaign committee with activity in the 2023 to 2024 cycle, with cash on hand at the cycle's start and end so the node balances | 2023 to 2024 election cycle | United States | Money, lobbying and influence | None | Primary |
| 101 | 14.111 | Alluvial | Reference | | | | | | | | Rule only |
| 102 | 14.112 | Journey map | Core | What happens after someone applies for SNAP food benefits, and how long can each step take? | `govinfo-snap-application-steps` | Code of Federal Regulations, 7 CFR 273.2 (application processing), from govinfo or eCFR; USDA Food and Nutrition Service's applicant page | Rule in force on the retrieval date | United States | Congress, agencies and public services (V7 I062, "Delivering services") | None | Primary |
| 103 | 14.113 | Flow map | Reference | | | | | | | | Rule only |
| 104 | 14.114 | Tile-grid map, categorical | Core | Which states prohibit ranked-choice voting? | `ballotpedia-rcv-prohibitions-by-state` | Ballotpedia, labeled secondary | As of November 2026 | 50 states and DC | Elections and representation | None | Built S07 |
| 105 | 14.115 | Tile-grid map with shift arrows | Core | Where did the presidential margin move between 2020 and 2024? | `fec-presidential-shift-by-state` | Federal Election Commission | 2020 and 2024 | 50 states and DC | Elections and representation | New York, New Jersey, Florida, California | Built S12 |
| 106 | 14.116 | Bubble map | Core | Where did more citizens report voting in 2024? | `census-cps-2024-turnout-by-state` | U.S. Census Bureau, CPS Table 4a | 2024 | 50 states and DC | Taking part, trust and shared norms | Texas, Florida, New York | Built S16 |
| 107 | 14.117 | Choropleth, sequential | Core | Where do more households have a broadband internet subscription? | `census-acs-broadband-by-state` | U.S. Census Bureau, ACS 1-year, table B28002, with margins | 2025 | 50 states and DC, with the national figure set apart | News, records and public information (V7 I015) | None | Primary |
| 108 | 14.118 | Locator map | Core | Where is Lake Isabella, the town in chapter 01's photograph of a public meeting? | `census-gazetteer-2024-places` (one row) with the state and county geometry | U.S. Census Bureau, 2024 Gazetteer Files and Cartographic Boundary Files | 2024 vintage | Kern County, California | Taking part, trust and shared norms (V7 I146, "Public meetings hear mostly from organized insiders") | California | Primary |
| 109 | 14.119 | District map | Extended | How close was each of Michigan's 2024 House races, by one margin rule for every kind of seat? | `clerk-house-results-2024-by-district` (and `-by-candidate`) with the district geometry | Clerk of the House, "Statistics of the Presidential and Congressional Election of November 5, 2024" (official sources, published March 10, 2025); Census CD119 boundaries. The FEC’s 2024 congressional file lists candidates without votes | November 5, 2024 general election | Michigan's 13 districts | Elections and representation | Michigan | Primary |
| 110 | 14.120 | County choropleth | Extended | How does median household income vary from county to county? | `census-acs5-county-median-household-income` | U.S. Census Bureau, ACS 5-year, table B19013, with margins | 2020 to 2024 | Every county and county equivalent in the 50 states and DC | Taxes, wealth and economic security | None | Primary |
| 111 | 14.121 | District tile map | Extended | Which party won each House seat in 2024, and by how much, with the same margin classes as row 109? | `clerk-house-results-2024-by-district` with `census-gazetteer-2024-cd119` for the studio’s own tile layout | Clerk of the House; U.S. Census Bureau | November 5, 2024 general election | All 435 districts | Elections and representation | None | Primary |
| 112 | 14.122 | Dot density map | Extended | Where are the jobs? | `census-cbp-county-employment` | U.S. Census Bureau, County Business Patterns, paid employees by county | 2023, the latest release | Every county in the 50 states and DC | Work, pay and bargaining power | None | Primary |
| 113 | 14.123 | Small-multiple maps | Extended | When did states set their minimum wage above the federal $7.25? | Maps: `dol-state-minimum-wage-classes` (from `dol-state-minimum-wage-history`), Dustin's Department of Labor download. Beneath them, one sourced sentence with the atlas's July 1, 2026 count, read by script from Atlas V7 claim CL1516 in `work/extract/atlas-v7-data.json` (DR-243) | Maps: U.S. Department of Labor, Wage and Hour Division, "Changes in Basic Minimum Wages in Non-Farm Employment Under State Law: Selected Years 1968 to 2024". Sentence: Atlas V7, claim CL1516 (graded documented), citing the Department's "State Minimum Wage Laws" page, updated July 1, 2026 (V7 source K1508, accessed October 15, 2026) | Maps: January 1 of 2010, 2014, 2019 and 2024 (DR-243), the data lead's panels (review fix pass): the latest as-of day and every fifth year back, 2009 moved to 2010, the first January 1 under the federal $7.25 of July 24, 2009. Sentence: July 1, 2026, from V7's snapshot of October 15, 2026 | 50 states and DC | Work, pay and bargaining power (V7 I104) | None | Download item 2 for the maps; V7 for the sentence |
| 114 | 14.124 | Party-colored map or red and blue scale | Avoid | | | | | | | | Rule only |

Twenty rows take new data (83, 86 to 92, 94 to 96, 100, 102, 107 to 113); three are built (104 to 106); nine are rule only (eight reference, one avoid). Tiers: 9 core, 14 extended, 8 reference, 1 avoid, as the proposal sets them.

Notes the makers need, row by row:

- **83.** CMS reports by state and month; some states reported late or revised. The sidecar will say which months and states the national sums cover and that the file is the "updated" outcomes, which counts renewals completed after the first report. A funnel of shares needs every step from the same base, so the base is renewals due in the months the file covers.
- **86.** The diagram draws the stages the statutes name. The guide's tracker for an agency rule (Rule 11.9) stays the reader's display; this is the full process behind it, with the review, comment, disapproval and court branches. The Federal Register's own guide refused this container (a bot check), so the steps rest on the statute text.
- **87.** The tree stops at what the record shows: whether the state bans ranked-choice voting, in all or some elections, and V7's note that home-rule cities can adopt it for municipal offices where no ban applies. It does not say whether a given city has home rule; that is state law, and the last leaf says to check it.
- **91.** Each route's threshold (votes needed, who signs, who can undo it) comes from the workflow sources file, each with its official page and date. V7 supplies the route names, who acts and the count of reforms that list each route. This is a different lesson from row 36's heat table, which draws each reform's feasibility by route.
- **92.** Both votes are recorded votes on the same bill: the Senate's vote on passage as amended and the House's vote to agree to the Senate's amendment. Each vote's question prints as the record words it (row 40's lesson). Party marks in neutral inks with the party named (DR-48, DR-58).
- **94.** One committee for each major-party nominee, drawn the same way (Rule 01.11): the recipients of each committee's transfers, summed. State party recipients may fold into one labeled node per committee; the table lists each.
- **96.** The bills are every bill whose title, as Congress.gov lists it, names pharmacy benefit managers; the sidecar states the rule and its limit (a bill whose listed title does not name them is left out). An arc joins two bills that share a sponsor or cosponsor; bills sit in order of introduction.
- **100.** One node, "2024 House campaigns", with the FEC's receipt lines on the left and its disbursement lines on the right. A note says no dollar received is traced to a dollar spent. Transfers between a candidate's own committees are netted out.
- **108.** Lake Isabella is a census-designated place in Kern County. The locator ties chapter 14 to chapter 01's Rule 01.8 photograph (pho-04r). The Corps of Engineers' project page refused this container, so the place comes from the Census Bureau's Gazetteer and the story from the photograph's record.
- **109 and 111.** The same official results drawn two ways is the lesson: real geography for one state, every seat equal for the nation. The 119th Congress's districts are the ones elected in 2024; districts several states redrew for 2026 do not apply. Certified 2026 results replace these at Phase 5 if they exist by then (proposal section 2.3, item 6). No red and blue (DR-64); neutral inks with the party named.
- **110.** Connecticut's counties are its nine planning regions in the 2024 files, and the geometry uses the same units. Margins are large in small counties; the sidecar says so, and the map's classes are read with them.
- **111.** The tile layout is the studio's own, built from the Census Bureau's district centers. Published hex or tile layouts (newsroom and blog cartograms) are study only and never traced.
- **112.** Dots sit at random inside each county, from a fixed seed the spec records; a dot is a count, never an address.
- **113.** dol.gov refused this container, so the history table came as download item 2, Dustin's saved page, frozen November 12, 2026 (P7-223). The page's latest column is January 1, 2024; it has no 2025 or 2026 column. The four maps are January 1, 2010, 2014, 2019 and 2024 from `dol-state-minimum-wage-classes`, printed with its variant `panels_2010_2014_2019_2024` (data lead, review fix pass). Beneath them, DR-243 prints the atlas's July 1, 2026 count as one sourced sentence, not a map: V7 claim CL1516, graded documented, gives 30 states and DC above $7.25, 13 states at $7.25, Georgia and Wyoming at $5.15 and five states with no minimum wage law, where the federal rate applies to covered employers, from the Department's "State Minimum Wage Laws" page updated July 1, 2026 (V7 source K1508, accessed October 15, 2026). The maker reads those figures from `work/extract/atlas-v7-data.json` by script, and the sentence names the atlas as its source with the snapshot date. No new download: a July 1, 2026 map would need the Department's current state table and would mix two as-of days.

## Rule 01.9 count for chapter 14

**Superseded (Research lead, round 2 review fix pass, November 12, 2026).** The two tables below are the record of round 3’s sign-off. The chapter’s current count is the round 4 plan’s, `work/handoffs/phase-3/20261112_Round-4-Data-Plan.md`, section "Rule 01.9 count for chapter 14 as a whole": 108 examples (84 specimens in rounds 0 to 3, 13 rule plates and round 4’s 11), limits of 27 per domain and 21 per state, taxes, wealth and economic security the largest at 16, and California and Florida the most-named states at 5 each. That count puts S38 under news, records and public information, so rounds 0 to 3 read news and records 4 and atlas-wide 9, and it re-picks round 4’s forms, so the round 4 column in the second table no longer holds.

### Rounds 0 to 3: 84 examples

S01 to S16 (16), rounds 1 (26) and 2 (22) as signed off, and round 3's 20 new specimens. Round 3's built maps (S07, S12, S16) are already in the 16.

| Domain | Rounds 0 to 2 | Round 3 | Total | Share | Limit 21 |
|---|---|---|---|---|---|
| Taxes, wealth and economic security | 12 | 1 (county choropleth) | 13 | 15.5% | Holds |
| Housing, health care and getting ahead | 10 | 0 | 10 | 11.9% | Holds |
| Elections and representation | 8 | 3 (decision tree, district map, district tile map) | 11 | 13.1% | Holds |
| Work, pay and bargaining power | 7 | 2 (dot density, small-multiple maps) | 9 | 10.7% | Holds |
| Congress, agencies and public services | 4 | 4 (funnel, org chart, roll-call grid, journey map) | 8 | 9.5% | Holds |
| Money, lobbying and influence | 4 | 2 (network, Sankey) | 6 | 7.1% | Holds |
| Checks on power and equal justice | 3 | 2 (process diagram, hierarchy tree) | 5 | 6.0% | Holds |
| Competition and market power | 3 | 2 (who-decides, arc diagram) | 5 | 6.0% | Holds |
| News, records and public information | 2 | 1 (choropleth) | 3 | 3.6% | Holds |
| Taking part, trust and shared norms | 3 | 1 (locator) | 4 | 4.8% | Holds |
| Atlas-wide | 8 | 2 (comparison grid, adjacency matrix) | 10 | 11.9% | No single domain |
| **All** | **64** | **20** | **84** | | |

**By state.** Round 3 names Michigan once (district map) and California once (locator), and the decision tree may name Ohio and Tennessee once each. New York stays at 3, Florida at 2, California reaches 2. The limit is 16 of 84.

**Level and region (Rule 01.12).** Rows 109 and 108 are state and local (Michigan's districts; a town in Kern County, California). Every other round 3 example is national or covers every state or county alike.

### Chapter 14 as a whole: about 95 examples

Superseded by the round 4 plan’s count of 108; see the note at the head of this section.

Round 4 adds 11 data-bearing specimens (6 core and 5 extended in proportion and overlap and infographics). I count them with the two moves the data lead signed off for round 4 (the calendar to federal budget and tax deadlines, the step-by-step to applying for a benefit) and the coverage plan's data for the rest. Round 4's plan, a round ahead, re-picks them in detail.

| Domain | Rounds 0 to 3 | Round 4 as planned | Total | Limit 23 |
|---|---|---|---|---|
| Elections and representation | 11 | 5 (Venn, Euler, process explainer of a ballot measure, comparison cards on primaries, annotated ranked ballot) | 16 | Holds |
| Taxes, wealth and economic security | 13 | 2 (icon array, calendar) | 15 | Holds |
| Housing, health care and getting ahead | 10 | 1 (step-by-step: round 4 picks another process, since row 102 now draws applying for a benefit; counted here as the data lead counted it) | 11 | Holds |
| Work, pay and bargaining power | 9 | 0 | 9 | Holds |
| Congress, agencies and public services | 8 | 1 (proportional symbols of outlays by agency) | 9 | Holds |
| Money, lobbying and influence | 6 | 0 | 6 | Holds |
| Checks on power and equal justice | 5 | 0 | 5 | Holds |
| Competition and market power | 5 | 0 | 5 | Holds |
| Taking part, trust and shared norms | 4 | 1 (the social data card, if it carries a taking-part specimen) | 5 | Holds |
| News, records and public information | 3 | 0 | 3 | Holds |
| Atlas-wide | 10 | 1 (by-the-numbers panel) | 11 | No single domain |
| **All** | **84** | **11** | **95** | |

The largest domain, elections and representation, reaches 16 of 95, seven under the limit; taxes and budgets reach 15. No state passes 3 of 95 against a limit of 19.

One thing the count does not yet hold: chapter 14's rules 14.1 to 14.14 have correct and failure plates, and the editor's plates may draw charts on frozen data. If the generator counts those plates as examples, each adds one in its file's domain. With 14 more, the limit rises to 27 and the largest domain has 11 to spare, so none can break it; the generator's log gives the true figure (R3).

## Re-picks from the coverage plan (DR-229)

Thirteen round 3 forms change data, keeping their form and tier. The decision tree, the district map and the district tile map are built for elections and keep election data (DR-229); the three built maps keep theirs.

| # | Form | Coverage plan data | New data | Why |
|---|---|---|---|---|
| 83 | Funnel | Eligible, registered, voted (CPS) | Medicaid and CHIP renewals: due, renewed, dropped for paperwork, found ineligible | S04 and S16 already draw the CPS voting tables, and rows 3 and 70 moved off them for that reason; V7 names this drop-out (I062) |
| 86 | Process diagram | Federal and state lawmaking steps | How a federal agency makes or changes a rule | Chapter 11's tracker and chapter 15's workflows already draw the lawmaking steps; the rule process has branches a diagram shows best |
| 88 | Who-decides diagram | V7 pathway decision makers, unnamed pathway | V7 pathway PW03, electric and utility bills | Its eight decision makers split cleanly into those who change a rule and those who apply it, across federal, state, local and private hands |
| 90 | Hierarchy tree | Federal budget functions | Federal courts: the Supreme Court, 13 courts of appeals, 94 district courts | Row 48's treemap already draws budget functions; checks on power had three examples |
| 91 | Comparison grid | V7 reforms against routes | V7's eleven routes against what each takes | Row 36's heat table already draws reforms against routes |
| 92 | Roll-call grid | Both chambers' votes on one bill (H.R. 7008 by default) | H.R. 5371, the November 2025 continuing appropriations act | H.R. 7008 already serves S01 and rows 40, 41 and 77, and its Senate vote was on taking the bill up; H.R. 5371 has a recorded passage vote in each chamber |
| 94 | Network diagram | FEC committee transfers for one example | Both 2024 presidential joint fundraising committees, drawn alike | One committee would show one party's mechanism; both parties use it (Rule 01.11) |
| 96 | Arc diagram | Bills that share sponsors, no subject named | Pharmacy benefit manager bills of the 119th Congress | A subject with many bills and cross-party backers; competition had three examples |
| 100 | Sankey | Treasury receipts and outlays through one node | 2024 House campaigns' receipts and spending | Rows 26, 44 and 48 already draw the Monthly Treasury Statement; money and influence needs the flow it asks about |
| 107 | Choropleth, sequential | Child poverty by state | Households with a broadband subscription by state | S02 and row 57 already chart child poverty; news and public information had two examples (V7 I015) |
| 110 | County choropleth | County turnout or income | County median household income | No primary source gives turnout by county for every state, and income is the coverage plan's own alternative |
| 112 | Dot density map | Population by county | Paid employees by county | A count with a domain; the same county geometry as row 110 |
| 113 | Small-multiple maps | Ranked-choice adoption over time | State minimum wages above $7.25 over time | Election data on a general form; the decision tree and the tile map already carry ranked-choice voting |

Row 108's locator keeps the coverage plan's "any state or county" and picks Lake Isabella, California, to tie chapter 14 to chapter 01's photograph.

## Map geometry: source and rights

| Geometry | File the studio fetches | Publisher and page | Rights |
|---|---|---|---|
| States, nation | `cb_2024_us_state_20m.zip`, `cb_2024_us_nation_20m.zip` | U.S. Census Bureau, Cartographic Boundary Files, 2024, https://www2.census.gov/geo/tiger/GENZ2024/shp/ | A work of the U.S. federal government, no U.S. copyright (17 U.S.C. 105); I read the Bureau's own terms on the product page before freezing and quote them in each sidecar |
| Counties | `cb_2024_us_county_20m.zip`, and `_5m` for California's counties in the locator | As above | As above |
| Congressional districts, 119th Congress | `cb_2024_us_cd119_5m.zip` | As above | As above |
| District, county and place centers | `2024_Gaz_119CDs_national.zip`, `2024_Gaz_counties_national.zip`, `2024_Gaz_place_national.zip` | U.S. Census Bureau, 2024 Gazetteer Files, https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2024_Gazetteer/ | As above |
| Tile layouts | None fetched | The studio draws its own from the centers above | Studio work. Published layouts by newsrooms or blogs are study only (Master Brief section 2) |

I convert each shapefile to GeoJSON in longitude and latitude, with no simplification, and record the raw file's SHA-256. Projection and simplification belong to the kit (request ENG-10 below), so the page carries only what a map draws.

## Datasets to fetch and freeze

After your sign-off. Each goes into `work/build/data/` under contract C1 with a sidecar and a row in the research ledger’s Part 7, from P7-201 on (round 3’s rows take the 200s).

| Dataset | Rows | Host | How |
|---|---|---|---|
| `cms-medicaid-chip-renewal-outcomes` | 83 | data.medicaid.gov | Dataset API |
| `govinfo-federal-rulemaking-steps` | 86 | www.govinfo.gov, www.archives.gov | Statute and order text |
| `v7-rcv-local-routes`, `v7-pathway-electric-decision-makers`, `v7-routes`, `v7-links-with-regions`, `v7-region-connection-matrix` | 87, 88, 91, 95 | Repository | `work/build/scripts/phase-3/research_v7_extract.py`, extended |
| `clerk-house-committees-119` | 89 | clerk.house.gov | XML |
| `uscode-federal-courts-circuits-districts` | 90 | www.govinfo.gov, www.uscourts.gov | Statute text |
| `usgov-route-requirements` | 91 | Official pages in the workflow sources file | Text, each cell with its page |
| `congress-hr5371-roll-calls-by-member` | 92 | www.senate.gov, clerk.house.gov | Roll call XML |
| `fec-jfc-transfers-2024` | 94 | api.open.fec.gov | API, key injected |
| `congress-gov-pbm-bills-119` and its two companions | 96 | www.govinfo.gov | The Library of Congress’s bill status bulk files for the 119th Congress (every title, sponsor and cosponsor) |
| `fec-house-campaigns-2024-by-candidate`, `fec-house-campaigns-2024-money-in-out` | 100 | www.fec.gov | The current campaigns file `webl24.zip` (the API’s candidate totals lack the receipt and loan lines) |
| `govinfo-snap-application-steps` | 102 | www.govinfo.gov or www.ecfr.gov's API; www.fns.usda.gov | Regulation text |
| `census-acs-broadband-by-state` | 107 | api.census.gov | API, key from the environment |
| `census-gazetteer-2024-places`, `census-gazetteer-2024-cd119` | 108, 111 | www2.census.gov | Files |
| `clerk-house-results-2024-by-candidate`, `clerk-house-results-2024-by-district` | 109, 111 | clerk.house.gov | The Clerk’s 2024 election statistics (PDF) |
| `census-acs5-county-median-household-income` | 110 | api.census.gov | API |
| `census-cbp-county-employment` | 112 | api.census.gov | API |
| `dol-state-minimum-wage-history` | 113 | www.dol.gov | Download item 2 |
| Geometry: `census-cb-2024-states`, `-counties`, `-cd119` | 107 to 112 | www2.census.gov | Files, converted to GeoJSON (ENG-10) |

Every host above answered this container today, between 03:58 and 04:04 UTC (the Congress.gov, FEC and Census APIs with their keys), except www.dol.gov, which refused. www.ssa.gov, www.medicaid.gov, www.usace.army.mil and www.fcc.gov also refused, and www.federalregister.gov and www.ecfr.gov's pages sent a bot check, so no row depends on them; eCFR's API answered. Only row 113 depends on a host that refused. (Research lead, round 2 review fix pass, November 12, 2026: its page came as download item 2 and is frozen as P7-223.)

## Download list (DR-230)

Item 1 was Dustin's FRED file (round 0). One more is needed; three of the five would remain. (Research lead, round 2 review fix pass, November 12, 2026: item 2 came. Dustin saved the page on November 12, 2026, and it is frozen as P7-223 in `dol-state-minimum-wage-history` and `dol-state-minimum-wage-classes`.)

| # | Page to open | File to save | What it is | Specimen it serves |
|---|---|---|---|---|
| 2 | https://www.dol.gov/agencies/whd/state/minimum-wage/history | The page itself (in a browser, File, Save Page As, "Web page, HTML only"), or a PDF print of it; please attach it to the chat as is | The Department of Labor's table of each state's basic minimum wage in selected years from 1968 to 2024 (the plan first read 2025; the page's title reads 1968 to 2024) | Row 113, small-multiple maps |

Why a download: dol.gov refused this container's reader (HTTP 403) at 03:58 UTC, and no other primary source gives every state's rate by year. If the file does not come, row 113 waits, and I propose the ACS uninsured rate by state for four years as its fallback. (Research lead, round 2 review fix pass, November 12, 2026: superseded. The file came the same day and is frozen as P7-223, so row 113 waits on nothing and the fallback is not used.)

## What stays Illustrative

Nothing in round 3. Every row has a primary source, V7 or a labeled secondary source.

## For the data lead's sign-off

Please check five things, under Rule 01.9 and DR-229:

1. The domain of each row, above all row 86 (the rule process under checks on power, V7's "Agency law" subsystem, rather than Congress and agencies), row 108 (the locator under housing, health care and getting ahead, for the dam project; the sign-off’s change 2 moved it to taking part, trust and shared norms, V7 I146, as the table above now reads), and the two atlas-wide rows, 91 and 95.
2. The thirteen re-picks, form by form, against what each form teaches.
3. Rows 92 and 94, the two that touch party: the roll-call grid of H.R. 5371 and the joint fundraising committees of both nominees.
4. Rows 109 and 111 drawing one results file two ways.
5. The count for chapter 14 as a whole, and whether the editor's rule plates should enter it.

Reply in your notes with "signed off" or the changes. I fetch nothing you change until I re-pick it.

## Requests

- **ENG-10, to the engineer: map geometry in the data folder.** Contract C1 has no shape for geometry. I propose `census-cb-2024-states.geojson` (and `-counties`, `-cd119`) in `work/build/data/`, unprojected longitude and latitude, unsimplified, each with a sidecar in C1's fields plus `geometry_type`, `source_resolution` and `raw_file_sha256`. The kit projects (an Albers projection with Alaska and Hawaii set apart, as the tile maps already do) and simplifies at build, so the page carries only drawn paths. If you want another shape (a subfolder, TopoJSON, or a projected path table as CSV), say so in your contracts and I write that instead.

## Data lead sign-off

**Signed off with twelve changes**, November 12, 2026, by the data visualization and systems lead, under Rule 01.9 and DR-229. No dataset is replaced, so every row may be fetched now: changes 1 to 3 move a domain or a grouping, and changes 4 to 12 name a source, a field or a rule the fetch must carry. The conditions after them are for the makers when they draw and change nothing you fetch.

**What I checked, and how**

- A script (`recount.py`, in my scratch folder `phase-3/round-1/data-lead/`) read both plans' row tables and recounted Rule 01.9. It finds the plan's own figures: 32 forms, 20 new data-bearing specimens, 84 examples in rounds 0 to 3 with the same domain totals, and 95 for the chapter with round 4 as planned. Taxes, wealth and economic security leads rounds 0 to 3 with 13 of 84 against a limit of 21; elections and representation leads the chapter with 16 of 95 against 23. No state passes 3 of 84.
- Every V7 value the plan names, read by script from `work/extract/atlas-v7-data.json` (snapshot October 15, 2026): issues I062 and I054 (D04), I015 (D01), I104 (D07), I084 and I093 (D06), I170 (D09, Food security); the subsystems Agency law and Courts (D05) and Infrastructure (D09); pathway PW03's eight decision makers, six of whom can change a rule; the eleven routes; route LOC on R-01 and R-02; the 118 connections. Each matches the plan, with the two exceptions in changes 1 and 2.
- The five checks the plan asks for, and four I added: the party and election rules on every row that touches either (DR-48, DR-58, DR-64, D2-269, Rule 01.11); Rule 01.10's levels and regions; every form that sizes a line, a node or a flow, which needs a defined measure and a key; and survey margins on the choropleths (DR-64, Rule 14.9).

**The five checks**

1. *Domains.* Signed off as written except rows 102 and 108 (changes 2 and 3). Row 86 stays under checks on power and equal justice: its question asks where Congress or a court can step in, and V7's Agency law subsystem is titled "Who interprets the law", about authority shifting "between Congress, agencies and judges". V7 files its cross-cutting record X14 under Congress and agencies, so the pick could go either way, and the count holds either way. Rows 91 and 95 stay atlas-wide: one draws all eleven routes, the other every connection.
2. *Re-picks.* All thirteen keep their form and tier and teach what the form exists for, with changes 4 to 11 for rows 83, 86, 90, 94, 96, 100 and 113. Rows 89 and 90 both draw trees; change 5 gives row 90 a count at every node, so the org chart teaches who sits under whom inside one body and the hierarchy tree teaches parts nested inside parts. The decision tree keeps election data because the coverage plan wrote its use as the ranked-choice question.
3. *Rows 92 and 94.* Signed off, with change 8 and the conditions below. Each draws the same thing for both sides, as Rule 01.11 asks, and neither needs a counterweight.
4. *Rows 109 and 111.* Signed off with change 9. One results file drawn on real geography and on equal tiles teaches what the district tile map is for, and the pair teaches it only if both take the same margin classes, the same party marks and the same handling of unusual seats.
5. *The whole-chapter count, and the editor's plates.* The count holds. With changes 2 and 3, rounds 0 to 3 read: taxes 13, elections 11, housing 10, atlas-wide 10, work and pay 9, Congress and agencies 8, money 6, checks on power 5, competition 5, taking part 4, news and records 3. The chapter reads: elections 16, taxes 15, housing 11, atlas-wide 11, work and pay 9, Congress and agencies 9, money 6, taking part, checks on power and competition 5 each, news and records 3. **The editor's plates enter the count.** Rule 01.9 counts the examples a reader meets in a chapter, and a plate on real or invented data is one. Count a rule's correct and failure plates as one example when they draw the same data and as two when they draw different data, each in the domain of what it draws; a plate that draws no subject, such as an anatomy diagram or a palette strip, stays out. With 14 plates the chapter holds 109 examples, the limits are 27 per domain and 21 per state, and elections, the largest domain, has 11 to spare. Rule 14.7's plates need party data; the editor's other plates have most room in news and records, taking part, competition and checks on power. The generator's log gives the true figure (R3).

**Changes before the fetch**

1. **Row 95, adjacency matrix: group by V7's ten regions, not its domains.** V7 gives no domain to 20 of its 51 variables (all twelve economy and all eight technology variables) and gives two domains to nine more, so a domain matrix would need the studio to assign them, which changes the model. V7's own regions place every variable once: six in the core layer (A, B, C, D, E and X), three in the economy layer and one in technology, ten in all. The 118 connections fill 44 of the 100 cells. Keep the question; name the derived files for regions (`v7-links-with-regions`, `v7-region-connection-matrix`); the row stays atlas-wide. The seven authority connections carry no sign in V7, so if a cell splits by sign they form their own class with no sign.
2. **Row 108, locator: domain to taking part, trust and shared norms** (V7 I146, "Public meetings hear mostly from organized insiders", in the Participation subsystem: "meeting formats ... that decide who shows up between elections"). The question names the public meeting, and chapter 01 shows the photograph for its meeting. V7's Infrastructure subsystem covers poor connections that raise household costs, which a dam safety meeting is not. California still counts once.
3. **Row 102, journey map: domain to Congress, agencies and public services** (V7 I062, Administration: "Delivering services"), the domain row 83 takes for the same kind of question: how a person gets through a benefit's paperwork and time limits. I170 concerns the harm of going without food, not applying. Round 4's step-by-step was to show applying for a benefit, which row 102 now draws, so round 4's plan picks another process; requesting public records would also lift news and records, the smallest domain at 3.
4. **Row 86, process diagram: add the court and review sources.** The court branch rests on 5 U.S.C. 701 to 706, which the row does not list. The review step rests on Executive Order 12866 as in force on the retrieval date and on Executive Order 14215 of February 18, 2025, which V7 itself cites (X14, source Q514) for sending independent agencies' significant rules to the Office of Information and Regulatory Affairs. Without it the diagram shows who goes through review as it stood before 2025.
5. **Row 90, hierarchy tree: add each court's count and the territorial courts' source.** Add the authorized judgeships for each circuit and district from 28 U.S.C. 44 and 133, in the same statute text, so each node carries a number and the tree sums. 28 U.S.C. 81 to 131 set up the districts of the states, DC and Puerto Rico; if the tree draws 94 district courts, the courts of Guam, the Virgin Islands and the Northern Mariana Islands rest on Title 48, and the sidecar cites those sections and says they are not Article III courts.
6. **Row 96, arc diagram: one chamber, and a stated search.** A representative cannot cosponsor a Senate bill, so no arc could join a House bill to a Senate bill, and companion bills, the closest ties, would never connect. Draw the chamber with more matching bills and list the other chamber's in the table. Search every title Congress.gov lists for a bill (official, short and popular) for "pharmacy benefit manager" and "PBM", and print that rule. Arc width counts shared backers, with a key, or every arc takes one weight and the table gives the count. Three of competition's five examples are now about drug middlemen (S32, S39 and this row). Rule 01.9 counts domains and holds, and this diagram ends at the law S32 draws, so I accept it; the entry should not retell S32's story.
7. **Row 100, Sankey: make the node balance.** A cycle's receipts do not equal its spending, so a Sankey through one node needs cash on hand at the start of the cycle on the left and at its end on the right, from the same FEC totals, and the sidecar prints any remainder that does not balance. Candidate loans and loan repayments stay separate lines, so a loan is not read as a gift. Name the base in the sidecar: every House candidate's principal campaign committee with activity in the cycle, primary losers included, or the subset the totals cover.
8. **Row 94, network diagram: one stated rule picks each committee.** Each nominee had more than one joint fundraising committee. Take for each the one that transferred the most to its nominee's principal campaign committee in the cycle, read the same way for both, and print that rule in the sidecar with the Schedule B lines used. Line width encodes dollars transferred, with a key, and every recipient sums the same lines.
9. **Rows 109 and 111: define the margin for every kind of seat.** "By how much" needs a rule where the usual margin does not exist: unopposed seats (some states print no votes for them), top-two contests between two candidates of one party (such as California's), ranked-choice contests (Alaska and Maine: say whether the margin is the first round or the last), and Louisiana's November open primary with any runoff. Each case gets its own labeled class in both maps and both tables, and both maps take the same margin classes. Row 109's sidecar says why Michigan in terms of the lesson (for example, districts that run from close to safe for each party, if the results bear that out); the words say nothing about how the lines were drawn.
10. **Row 113, small-multiple maps: panels after July 24, 2009, at one as-of day.** The federal $7.25 took effect July 24, 2009. If the Department of Labor's table gives January 1 rates, a 2009 panel compares states with $6.55. Take years whose as-of day falls after that date, for example 2010, 2015, 2020 and 2026, all at the table's own as-of day, and name July 1, 2026 where the last panel differs. Three classes: above $7.25; at $7.25; below it or no state minimum, where the federal rate covers most workers. The uninsured fallback moves the row to housing, health care and getting ahead (11 there, within every limit) and carries its margins.
   (Research lead, round 2 review fix pass, November 12, 2026: the panel years above are superseded. The data lead’s review fix pass and DR-243 set January 1 of 2010, 2014, 2019 and 2024, printed from `dol-state-minimum-wage-classes` with its variant `panels_2010_2014_2019_2024`, and the page has no 2026 column, so the atlas’s July 1, 2026 count prints beneath the maps as one sourced sentence (V7 claim CL1516); no fallback is used. Row 113 above and its note carry this.)
11. **Row 83, funnel: nested stages from one base.** A funnel narrows, so each stage sits inside the one before: renewals due; renewals decided, with pending renewals counted and set apart; renewals not ended for procedural reasons; renewals that kept coverage. Automatic and form renewals can split in the table. If CMS's national sums differ from V7 I062's figures (more than 25 million disenrolled, 69 percent for procedural reasons, from KFF), the chart prints CMS's own figures and period, and the difference goes to the open questions ledger for Dustin, never into the chart as a correction of V7.
12. **Row 87, decision tree: branch on whether a ban reaches city elections, and confirm the date.** "All or some" is the wrong branch for a city. Tennessee's ban is partial, but its scope note names local government offices, so unless the act's text shows a route for a city, a Tennessee city follows the ban branch with the other 17. Only Ohio's leaves home-rule cities an opening, at the price its note names. The bans were read November 6, 2026, three days after a general election: at the fetch, confirm that no measure decided November 3, 2026 changed a state's status, and print the as-of date. The coverage plan's disclosure on this tree and the ranked-choice maps is retired (DR-100).

**Conditions for the makers** (no change to the fetch)

- **Rows 92, 94, 100, 109 and 111.** Parties take the neutral party ink with each party named on its mark, solid and outline in the same ink where sides must be told apart at a glance (D2-269); no red and blue and no Prussian (DR-48, DR-58, DR-64). Row 92 names independents as the Senate record lists them and folds them into no party, prints each vote's question in the record's words, and shows members not voting and vacant seats. Rows 109 and 111 print the national result set apart and labeled (DR-64): the House seats each party won in 2024.
- **Row 88.** Lines of authority, such as FERC approving a grid operator's rules or a legislature setting a commission's powers, take no sign and close no loop, as chapter 15's grammar draws them.
- **Rows 94, 96 and 100.** A width or a flow encodes one defined measure with a key; a Sankey's flows share one unit and sum at the node.
- **Row 107.** Name the B28002 line used: "broadband of any type" counts a household with a cellular data plan alone. The national figure stands apart. Class breaks sit wide enough that states differ in class only past their margins, and a note says so (DR-64, Rule 14.9).
- **Row 110.** County margins are wide in small counties. A note gives the share of counties whose 90 percent interval crosses a class break, and no county is named or singled out unless its gap passes its margin.
- **Row 112.** County Business Patterns counts paid employees of private establishments and leaves out government, the self-employed and most farm and household workers. The title and measure line say so ("Where are the private-sector jobs?"), and counties the Bureau flags are marked in the table.
- **Rows 86 and 102.** The journey map's times are the regulation's limits, not measured waits, and its title says so; both diagrams print the date of the law they draw.
- **Weight, for the engineer.** Rows 110 and 112 draw about 3,100 counties each, and each table equivalent would carry one row per county. Please measure one county map with its table against chapter 14's stop before round 3 draws (with ENG-10), and say whether a county map's table may group by state with the full rows in the CSV export. The dot density map should draw its dots from the county counts and the recorded seed, so the page never carries one element per dot.

**Rule 01.10, levels and regions.** Round 3 adds state, county and city examples beside the federal ones, and Michigan and Ohio (Midwest), California (West) and Tennessee (South) join New York and New Jersey (Northeast) and Florida and Texas (South) already named. Chapter 14 still has no school district example; round 4's plan should find one where its data allows.

## Research lead, after the sign-off

Applied November 12, 2026, before the fetch. The tables above now carry each change; this list says where.

- **Change 1, row 95.** The matrix groups V7's 51 variables by its ten regions, and the files are `v7-links-with-regions` and `v7-region-connection-matrix`. The authority connections keep no sign and form their own class.
- **Changes 2 and 3, rows 108 and 102.** The locator moves to taking part, trust and shared norms (I146) and the journey map to Congress, agencies and public services (I062). The count tables above take the data lead's figures: rounds 0 to 3, taxes 13, elections 11, housing 10, atlas-wide 10, work and pay 9, Congress and agencies 8; the chapter, elections 16, taxes 15, housing 11, atlas-wide 11, work and pay 9, Congress and agencies 9.
- **Change 4, row 86.** The fetch adds 5 U.S.C. 701 to 706 and Executive Order 14215 of February 18, 2025, and reads Executive Order 12866 as amended where the record shows it.
- **Change 5, row 90.** The fetch adds each circuit's and district's authorized judgeships (28 U.S.C. 44 and 133) and the territorial courts' Title 48 sections.
- **Change 6, row 96.** The search reads every title Congress.gov lists for each bill, official, short and popular, for "pharmacy benefit manager" and "PBM"; the chamber with more matches is drawn.
- **Change 7, row 100.** The file carries cash on hand at the start and end of the cycle, loans and loan repayments as their own lines, and the base in its sidecar.
- **Change 8, row 94.** One rule, read the same way for both nominees, picks each committee, and the sidecar prints it with the Schedule B lines used.
- **Change 9, rows 109 and 111.** The results file carries a margin class for every seat, with labeled classes for unopposed seats, one-party contests, ranked-choice contests (first and last round) and Louisiana's open primary.
- **Change 10, row 113.** Done November 12, 2026 from download item 2: the classes file holds every January 1 from 2010 to 2024 in three classes, and the panels are January 1, 2010, 2014, 2019 and 2024 (the data lead's choice in the review fix pass; 2015 and 2020 classed every state alike).
- **Change 11, row 83.** A derived file holds the nested stages from one base; CMS's national sums are compared with V7 I062's figures, and any difference goes to the open questions for Dustin.
- **Change 12, row 87.** The bans are re-confirmed after the November 3, 2026 election and printed with their as-of date. The branch on whether a ban reaches city elections needs its own column, since `scope` codes Tennessee "some" like Ohio (statistics review S12): `reaches_city_elections` (yes for the 17 full bans and Tennessee, partly for Ohio, empty where there is no ban) with `city_reach_note`, requested from the engineer, whose script writes the file (research notes, "Review fix pass", ENG-13). Tennessee's Public Chapter 621, read November 12, 2026, bars a county election commission from ranked-choice voting "for a statewide or local government office" and defines local government to include "an incorporated city or town".

**Status of every dataset, November 12, 2026, 04:40 UTC.** Frozen in `work/build/data/` with sidecars and research ledger rows P7-201 to P7-217, the engineer’s check reading 88 tables with 0 faults: rows 83 (two files), 86, 87 (V7 routes; the Ballotpedia bans re-read, P7-218), 88, 89, 90, 91 (two files), 92, 94, 95 (two files), 96 (three files), 100 (two files), 102, 107, 108, 109 and 111 (two files), 110 and 112. Three changes from this plan's text, each for its source: the House results come from the Clerk’s compilation, since the FEC’s 2024 congressional file lists candidates without votes; the Sankey reads the FEC’s current campaigns file, since the API’s candidate totals lack the receipt and loan lines change 7 needs; and the bill search reads the Library of Congress’s bulk bill status files, which carry every title of every bill. Waiting: the map geometry (raw Census files downloaded and GeoJSON staged; frozen when the engineer sets ENG-10’s shape, P7-219) and row 113 (download item 2, P7-220).

**Since then (Research lead, round 2 review fix pass, November 12, 2026).** Row 113 waits on nothing: download item 2 came on November 12, 2026 and is frozen as P7-223 (`dol-state-minimum-wage-history`, and the derived `dol-state-minimum-wage-classes`), printed with the variant `panels_2010_2014_2019_2024`; P7-220 was its placeholder and points to P7-223. The map geometry still waits (P7-219): the engineer posted the shape (R1-C7), and the kit’s projection and the data check’s reading of `.geojson` files are queued.
