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

Limits. Rounds 0 to 3 hold 84 examples: one in four is 21, one in five is 16.8, so no domain may supply more than 21 and no state more than 16. Chapter 14 as a whole holds about 95: no domain more than 23, no state more than 19.

## Round 3: 32 forms

Family 3.10 Behavior, 3.11 Structure, 3.12 Relationships, 3.13 Flow, 3.14 Maps.

| # | Rule | Form | Tier | Reader question | Dataset (file in `work/build/data/`) | Publisher | Period | Geography | Domain | States | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 83 | 14.93 | Funnel | Extended | Of the people whose Medicaid or CHIP coverage came up for renewal, how many kept it, and where did the rest drop out? | `cms-medicaid-chip-renewal-outcomes` | Centers for Medicare & Medicaid Services, Medicaid and CHIP Updated Renewal Outcomes (data.medicaid.gov) | The unwinding's reporting months, as CMS's file gives them | United States, summed from the states' reports | Congress, agencies and public services (V7 I062) | None | Primary |
| 84 | 14.94 | Cohort chart | Reference | | | | | | | | Rule only |
| 85 | 14.95 | Survival curve | Reference | | | | | | | | Rule only |
| 86 | 14.96 | Process diagram | Core | How does a federal agency make or change a rule, and where can Congress or a court step in? | `govinfo-federal-rulemaking-steps` | U.S. Code, 5 U.S.C. 553 (notice and comment) and 5 U.S.C. 801 to 808 (Congressional Review Act), from govinfo; Executive Order 12866's review step, from the National Archives | Law in force on the retrieval date | United States | Checks on power and equal justice (V7's "Agency law" subsystem) | None | Primary |
| 87 | 14.97 | Decision tree | Core | Can my city switch its own elections to ranked-choice voting? | `ballotpedia-rcv-prohibitions-by-state` (frozen) and `v7-rcv-local-routes` (new) | Ballotpedia, labeled secondary; Atlas V7, Reforms R-01 and R-02, route LOC | As of November 2026 (bans); snapshot October 15, 2026 (routes) | 50 states and DC | Elections and representation | Ohio and Tennessee, if the tree names the two partial bans | Secondary and V7 |
| 88 | 14.98 | Who-decides diagram | Core | Who sets my electric bill, and who can change the rules behind it? | `v7-pathway-electric-decision-makers` | Atlas V7, pathway PW03, "Electric and utility bills", its decision makers | Snapshot October 15, 2026 | United States | Competition and market power (V7 I093) | None | V7 |
| 89 | 14.99 | Org chart | Extended | How is the House divided into committees and subcommittees? | `clerk-house-committees-119` | Clerk of the House, committee and subcommittee list (MemberData.xml) | 119th Congress, on the retrieval date | United States | Congress, agencies and public services | None | Primary |
| 90 | 14.100 | Hierarchy tree | Extended | Which federal court hears a case from my state, and where does an appeal go? | `uscode-federal-courts-circuits-districts` | U.S. Code, 28 U.S.C. 41 (circuits) and 81 to 131 (districts), from govinfo; the Supreme Court and the courts' structure from uscourts.gov | Law in force on the retrieval date | 50 states, DC and the territories | Checks on power and equal justice (V7's "Courts" subsystem) | None | Primary |
| 91 | 14.101 | Comparison grid | Extended | Which of the eleven routes can carry a reform, and what does each one take? | `v7-routes` (new) and `usgov-route-requirements` (new) | Atlas V7, its eleven routes; the Constitution, statutes and official pages behind each route's threshold (`work/research/20261111_Policy-Workflow-Sources.md`) | Snapshot October 15, 2026; law on the retrieval date | United States | Atlas-wide | None | V7 and Primary |
| 92 | 14.102 | Roll-call grid | Extended | How did each senator and representative vote on the November 2025 bill that ended the shutdown? | `congress-hr5371-roll-calls-by-member` | U.S. Senate roll call vote XML and Clerk of the House roll call XML, H.R. 5371 | November 2025 | United States | Congress, agencies and public services (V7 I054) | None | Primary |
| 93 | 14.103 | Mind map | Reference | | | | | | | | Rule only |
| 94 | 14.104 | Network diagram | Extended | Where did the two 2024 presidential joint fundraising committees send what they raised? | `fec-jfc-transfers-2024` | Federal Election Commission, Schedule B transfers, API | 2023 to 2024 election cycle | United States | Money, lobbying and influence | None | Primary |
| 95 | 14.105 | Adjacency matrix | Extended | Which parts of the atlas connect to which? | `v7-links-with-domains` and `v7-domain-connection-matrix` (derived) | Atlas V7, its 118 connections and the domain of each end | Snapshot October 15, 2026 | United States | Atlas-wide | None | V7 |
| 96 | 14.106 | Arc diagram | Extended | Which bills to rein in drug middlemen drew the same backers? | `congress-gov-pbm-bills-119` | Library of Congress, Congress.gov API: bills of the 119th Congress whose titles name pharmacy benefit managers, with sponsors and cosponsors | 119th Congress, to the retrieval date | United States | Competition and market power (V7 I084) | None | Primary |
| 97 | 14.107 | Chord diagram | Reference | | | | | | | | Rule only |
| 98 | 14.108 | Multi-network | Reference | | | | | | | | Rule only |
| 99 | 14.109 | Symmetrical links | Reference | | | | | | | | Rule only |
| 100 | 14.110 | Sankey | Extended | Where did the money for 2024 House campaigns come from, and where did it go? | `fec-house-campaigns-2024-money-in-out` | Federal Election Commission, candidate financial totals, 2023 to 2024 cycle | 2023 to 2024 election cycle | United States | Money, lobbying and influence | None | Primary |
| 101 | 14.111 | Alluvial | Reference | | | | | | | | Rule only |
| 102 | 14.112 | Journey map | Core | What happens after someone applies for SNAP food benefits, and how long can each step take? | `govinfo-snap-application-steps` | Code of Federal Regulations, 7 CFR 273.2 (application processing), from govinfo or eCFR; USDA Food and Nutrition Service's applicant page | Rule in force on the retrieval date | United States | Housing, health care and getting ahead (V7's "Food security" subsystem, I170) | None | Primary |
| 103 | 14.113 | Flow map | Reference | | | | | | | | Rule only |
| 104 | 14.114 | Tile-grid map, categorical | Core | Which states prohibit ranked-choice voting? | `ballotpedia-rcv-prohibitions-by-state` | Ballotpedia, labeled secondary | As of November 2026 | 50 states and DC | Elections and representation | None | Built S07 |
| 105 | 14.115 | Tile-grid map with shift arrows | Core | Where did the presidential margin move between 2020 and 2024? | `fec-presidential-shift-by-state` | Federal Election Commission | 2020 and 2024 | 50 states and DC | Elections and representation | New York, New Jersey, Florida, California | Built S12 |
| 106 | 14.116 | Bubble map | Core | Where did more citizens report voting in 2024? | `census-cps-2024-turnout-by-state` | U.S. Census Bureau, CPS Table 4a | 2024 | 50 states and DC | Taking part, trust and shared norms | Texas, Florida, New York | Built S16 |
| 107 | 14.117 | Choropleth, sequential | Core | Where do more households have a broadband internet subscription? | `census-acs-broadband-by-state` | U.S. Census Bureau, ACS 1-year, table B28002, with margins | 2025 | 50 states and DC, with the national figure set apart | News, records and public information (V7 I015) | None | Primary |
| 108 | 14.118 | Locator map | Core | Where is Lake Isabella, the town in chapter 01's photograph of a public meeting? | `census-gazetteer-2024-places` (one row) with the state and county geometry | U.S. Census Bureau, 2024 Gazetteer Files and Cartographic Boundary Files | 2024 vintage | Kern County, California | Housing, health care and getting ahead (V7's "Infrastructure" subsystem: the meeting concerned a dam safety project) | California | Primary |
| 109 | 14.119 | District map | Extended | How close was each of Michigan's 2024 House races? | `fec-house-results-2024-by-district` with the district geometry | Federal Election Commission, 2024 congressional general election results (official, compiled from the states' certified counts); Census CD119 boundaries | November 5, 2024 general election | Michigan's 13 districts | Elections and representation | Michigan | Primary |
| 110 | 14.120 | County choropleth | Extended | How does median household income vary from county to county? | `census-acs5-county-median-household-income` | U.S. Census Bureau, ACS 5-year, table B19013, with margins | 2020 to 2024 | Every county and county equivalent in the 50 states and DC | Taxes, wealth and economic security | None | Primary |
| 111 | 14.121 | District tile map | Extended | Which party won each House seat in 2024, and by how much? | `fec-house-results-2024-by-district` with `census-gazetteer-2024-cd119` for the studio's own tile layout | Federal Election Commission; U.S. Census Bureau | November 5, 2024 general election | All 435 districts | Elections and representation | None | Primary |
| 112 | 14.122 | Dot density map | Extended | Where are the jobs? | `census-cbp-county-employment` | U.S. Census Bureau, County Business Patterns, paid employees by county | 2023, the latest release | Every county in the 50 states and DC | Work, pay and bargaining power | None | Primary |
| 113 | 14.123 | Small-multiple maps | Extended | When did states set their minimum wage above the federal $7.25? | `dol-state-minimum-wage-history` | U.S. Department of Labor, Wage and Hour Division, "Changes in Basic Minimum Wages in Non-Farm Employment Under State Law: Selected Years 1968 to 2025", with the July 1, 2026 state table chapter 01 already cites | Selected years from 2009 to July 1, 2026 | 50 states and DC | Work, pay and bargaining power (V7 I104) | None | Download item 2 |
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
- **113.** dol.gov refuses this container today, so the history table is download item 2. If it arrives, the four maps are 2009, 2014, 2019 and July 1, 2026, or the years the data lead prefers.

## Rule 01.9 count for chapter 14

### Rounds 0 to 3: 84 examples

S01 to S16 (16), rounds 1 (26) and 2 (22) as signed off, and round 3's 20 new specimens. Round 3's built maps (S07, S12, S16) are already in the 16.

| Domain | Rounds 0 to 2 | Round 3 | Total | Share | Limit 21 |
|---|---|---|---|---|---|
| Taxes, wealth and economic security | 12 | 1 (county choropleth) | 13 | 15.5% | Holds |
| Housing, health care and getting ahead | 10 | 2 (journey map, locator) | 12 | 14.3% | Holds |
| Elections and representation | 8 | 3 (decision tree, district map, district tile map) | 11 | 13.1% | Holds |
| Work, pay and bargaining power | 7 | 2 (dot density, small-multiple maps) | 9 | 10.7% | Holds |
| Congress, agencies and public services | 4 | 3 (funnel, org chart, roll-call grid) | 7 | 8.3% | Holds |
| Money, lobbying and influence | 4 | 2 (network, Sankey) | 6 | 7.1% | Holds |
| Checks on power and equal justice | 3 | 2 (process diagram, hierarchy tree) | 5 | 6.0% | Holds |
| Competition and market power | 3 | 2 (who-decides, arc diagram) | 5 | 6.0% | Holds |
| News, records and public information | 2 | 1 (choropleth) | 3 | 3.6% | Holds |
| Taking part, trust and shared norms | 3 | 0 | 3 | 3.6% | Holds |
| Atlas-wide | 8 | 2 (comparison grid, adjacency matrix) | 10 | 11.9% | No single domain |
| **All** | **64** | **20** | **84** | | |

**By state.** Round 3 names Michigan once (district map) and California once (locator), and the decision tree may name Ohio and Tennessee once each. New York stays at 3, Florida at 2, California reaches 2. The limit is 16 of 84.

**Level and region (Rule 01.12).** Rows 109 and 108 are state and local (Michigan's districts; a town in Kern County, California). Every other round 3 example is national or covers every state or county alike.

### Chapter 14 as a whole: about 95 examples

Round 4 adds 11 data-bearing specimens (6 core and 5 extended in proportion and overlap and infographics). I count them with the two moves the data lead signed off for round 4 (the calendar to federal budget and tax deadlines, the step-by-step to applying for a benefit) and the coverage plan's data for the rest. Round 4's plan, a round ahead, re-picks them in detail.

| Domain | Rounds 0 to 3 | Round 4 as planned | Total | Limit 23 |
|---|---|---|---|---|
| Elections and representation | 11 | 5 (Venn, Euler, process explainer of a ballot measure, comparison cards on primaries, annotated ranked ballot) | 16 | Holds |
| Taxes, wealth and economic security | 13 | 2 (icon array, calendar) | 15 | Holds |
| Housing, health care and getting ahead | 12 | 1 (step-by-step: applying for a benefit) | 13 | Holds |
| Work, pay and bargaining power | 9 | 0 | 9 | Holds |
| Congress, agencies and public services | 7 | 1 (proportional symbols of outlays by agency) | 8 | Holds |
| Money, lobbying and influence | 6 | 0 | 6 | Holds |
| Checks on power and equal justice | 5 | 0 | 5 | Holds |
| Competition and market power | 5 | 0 | 5 | Holds |
| Taking part, trust and shared norms | 3 | 1 (the social data card, if it carries a taking-part specimen) | 4 | Holds |
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

After your sign-off. Each goes into `work/build/data/` under contract C1 with a sidecar and a row in the research ledger's Part 7, from P7-111 on.

| Dataset | Rows | Host | How |
|---|---|---|---|
| `cms-medicaid-chip-renewal-outcomes` | 83 | data.medicaid.gov | Dataset API |
| `govinfo-federal-rulemaking-steps` | 86 | www.govinfo.gov, www.archives.gov | Statute and order text |
| `v7-rcv-local-routes`, `v7-pathway-electric-decision-makers`, `v7-routes`, `v7-links-with-domains`, `v7-domain-connection-matrix` | 87, 88, 91, 95 | Repository | `work/build/scripts/phase-3/research_v7_extract.py`, extended |
| `clerk-house-committees-119` | 89 | clerk.house.gov | XML |
| `uscode-federal-courts-circuits-districts` | 90 | www.govinfo.gov, www.uscourts.gov | Statute text |
| `usgov-route-requirements` | 91 | Official pages in the workflow sources file | Text, each cell with its page |
| `congress-hr5371-roll-calls-by-member` | 92 | www.senate.gov, clerk.house.gov | Roll call XML |
| `fec-jfc-transfers-2024` | 94 | api.open.fec.gov | API, key injected |
| `congress-gov-pbm-bills-119` | 96 | api.congress.gov | API, key injected: every 119th Congress bill title, then sponsors and cosponsors of the matches |
| `fec-house-campaigns-2024-money-in-out` | 100 | api.open.fec.gov, www.fec.gov | API totals, checked against the bulk summary file `webl24.zip` |
| `govinfo-snap-application-steps` | 102 | www.govinfo.gov or www.ecfr.gov's API; www.fns.usda.gov | Regulation text |
| `census-acs-broadband-by-state` | 107 | api.census.gov | API, key from the environment |
| `census-gazetteer-2024-places`, `census-gazetteer-2024-cd119` | 108, 111 | www2.census.gov | Files |
| `fec-house-results-2024-by-district` | 109, 111 | www.fec.gov | File, `2024congressgecands.xlsx` |
| `census-acs5-county-median-household-income` | 110 | api.census.gov | API |
| `census-cbp-county-employment` | 112 | api.census.gov | API |
| `dol-state-minimum-wage-history` | 113 | www.dol.gov | Download item 2 |
| Geometry: `census-cb-2024-states`, `-counties`, `-cd119` | 107 to 112 | www2.census.gov | Files, converted to GeoJSON (ENG-10) |

Every host above answered this container today, between 03:58 and 04:04 UTC (the Congress.gov, FEC and Census APIs with their keys), except www.dol.gov, which refused. www.ssa.gov, www.medicaid.gov, www.usace.army.mil and www.fcc.gov also refused, and www.federalregister.gov and www.ecfr.gov's pages sent a bot check, so no row depends on them; eCFR's API answered. Only row 113 depends on a host that refused.

## Download list (DR-230)

Item 1 was Dustin's FRED file (round 0). One more is needed; three of the five would remain.

| # | Page to open | File to save | What it is | Specimen it serves |
|---|---|---|---|---|
| 2 | https://www.dol.gov/agencies/whd/state/minimum-wage/history | The page itself (in a browser, File, Save Page As, "Web page, HTML only"), or a PDF print of it; please attach it to the chat as is | The Department of Labor's table of each state's basic minimum wage in selected years from 1968 to 2025 | Row 113, small-multiple maps |

Why a download: dol.gov refused this container's reader (HTTP 403) at 03:58 UTC, and no other primary source gives every state's rate by year. If the file does not come, row 113 waits, and I propose the ACS uninsured rate by state for four years as its fallback.

## What stays Illustrative

Nothing in round 3. Every row has a primary source, V7 or a labeled secondary source.

## For the data lead's sign-off

Please check five things, under Rule 01.9 and DR-229:

1. The domain of each row, above all row 86 (the rule process under checks on power, V7's "Agency law" subsystem, rather than Congress and agencies), row 108 (the locator under housing, health care and getting ahead, for the dam project), and the two atlas-wide rows, 91 and 95.
2. The thirteen re-picks, form by form, against what each form teaches.
3. Rows 92 and 94, the two that touch party: the roll-call grid of H.R. 5371 and the joint fundraising committees of both nominees.
4. Rows 109 and 111 drawing one results file two ways.
5. The count for chapter 14 as a whole, and whether the editor's rule plates should enter it.

Reply in your notes with "signed off" or the changes. I fetch nothing you change until I re-pick it.

## Requests

- **ENG-10, to the engineer: map geometry in the data folder.** Contract C1 has no shape for geometry. I propose `census-cb-2024-states.geojson` (and `-counties`, `-cd119`) in `work/build/data/`, unprojected longitude and latitude, unsimplified, each with a sidecar in C1's fields plus `geometry_type`, `source_resolution` and `raw_file_sha256`. The kit projects (an Albers projection with Alaska and Hawaii set apart, as the tile maps already do) and simplifies at build, so the page carries only drawn paths. If you want another shape (a subfolder, TopoJSON, or a projected path table as CSV), say so in your contracts and I write that instead.
