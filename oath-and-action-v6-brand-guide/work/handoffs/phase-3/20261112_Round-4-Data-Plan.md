# Round 4 data plan

Oath & Action Edition 06, Phase 3, round 2. Research lead, November 12, 2026, for the data visualization lead's sign-off. Paths are relative to `oath-and-action-v6-brand-guide/`.

## What this plan settles

Round 4 builds chapter 14's last 13 forms: proportion and overlap (coverage plan section 3.8; rules 14.79 to 14.84) and infographics (section 3.16; rules 14.135 to 14.141), as listed in `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`. This plan gives each one its reader question, dataset, publisher, period, geography, atlas domain, states and status, in the shape of the round 3 plan. It then counts Rule 01.9 for chapter 14 as a whole, rounds 0 to 4 with the editor's rule plates, sets out which coverage plan picks I changed and why, and lists what I fetch and freeze once you sign off.

Rows continue the earlier plans' numbering, 115 to 127, in rule order. With them, each of chapter 14's 127 forms has a row.

Status words, as before:

- **Primary**: the publisher's own file, API or page.
- **V7**: Atlas V7, snapshot of October 15, 2026, read by script.
- **Secondary**: a labeled secondary source (Ballotpedia, D2-99).
- **Frozen**: a file already in `work/build/data/`, drawn again with no new fetch.
- **Illustrative**: invented values or names, labeled "Illustrative data" beside the chart.
- **Rule only**: a reference sketch or an avoid entry; it draws no dataset.

## How I counted (Rule 01.9 and Rule 01.12)

The counting rules of the earlier plans stand: one data-bearing specimen is one example; each takes the one domain its reader question belongs to; atlas-wide specimens count in the total and in no domain; a state counts when it is the subject, named in the title, or lit on the chart; charts of who reports voting count under taking part; reference sketches and avoid entries are left out. Three points for this count:

1. **The editor's rule plates count**, as your round 3 sign-off set. The figure is the generator's log, `work/build/guide/entries/14-example-log.json`, as round 1 wrote it: 13 plates, rules 14.1 to 14.13, one example each. Rule 14.14's plate draws no subject. Round 2 redraws two plates (RS-S4 on Rule 14.3, ED-E4 on Rule 14.9); as I read both tasks, neither changes its domain, and the log after round 2 gives the true figure (R3).
2. **Specimens count by their spec where one exists.** S38 now counts under news, records and public information: its spec took domain D01 in round 1's fix pass (DL-R5), where both earlier plans counted it atlas-wide. Rounds 0 to 3 therefore read news 4 and atlas-wide 9, one move from the round 3 plan's table. S50's spec, written today, names Vermont and Alaska.
3. **Shared data.** The Venn and the Euler draw one file, and the social card redraws S19's. Each counts as its own example, as S41 and S42 do. Counting the social card with S19 as one would take the total to 107 and change no finding below.

A script recounted the table below from the files themselves: the generator's log for round 1 and the plates, the round 2 and round 3 specs that exist (all 22 of round 2's new specs were written by 19:16 UTC, each in the domain the rounds 1 and 2 plan gave it), the plans' rows for the rest, and this plan's rows 115 to 127.

Limits. Chapter 14 holds 108 examples: 84 specimens in rounds 0 to 3, 13 rule plates and round 4's 11. One in four is 27, so no domain may supply more than 27; one in five is 21.6, so no state may supply more than 21.

## Round 4: 13 forms

Family 3.8 Proportion and overlap, 3.16 Infographics.

| # | Rule | Form | Tier | Reader question | Dataset (file in `work/build/data/`) | Publisher | Period | Geography | Domain | States | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 115 | 14.79 | Icon array with Civic Line icons | Core | How many of every 100 workers belong to a union? | `v7-union-membership` (new, read by script from V7 claim CL1514) | Atlas V7, claim CL1514 (graded documented), citing the U.S. Bureau of Labor Statistics, "Union Members, 2025" (February 18, 2026; V7 source S04) | 2025 annual average, with 1983 for comparison | United States, employed wage and salary workers | Work, pay and bargaining power (V7 I101) | None | V7 |
| 116 | 14.80 | Proportional symbols | Extended | How many governments of each kind does the country have? | `census-cog-2022-governments-by-type` | U.S. Census Bureau, 2022 Census of Governments, organization tables: governments by type | 2022, the latest census of governments the Bureau has published | United States: the federal government, the 50 states, and every county, municipal, township, special district and independent school district government | Congress, agencies and public services (V7 I165, "State and local government") | None | Primary |
| 117 | 14.81 | Venn diagram | Extended | How many people have private health coverage, public coverage, both, or neither? | `census-acs-health-coverage-types` (published) and `census-acs-health-coverage-overlap` (derived: the four regions) | U.S. Census Bureau, American Community Survey 1-year, Data Profile DP03, health insurance coverage, with margins | 2025 | United States, civilian noninstitutionalized population | Housing, health care and getting ahead (V7 I133) | None | Primary |
| 118 | 14.82 | Euler diagram | Extended | Same, with each region's area true to its count | The same two files | Same | 2025 | Same | Housing, health care and getting ahead (V7 I133) | None | Primary |
| 119 | 14.83 | Packed circles or bubble cloud | Reference | | | | | | | | Rule only |
| 120 | 14.84 | Rose chart | Avoid | | | | | | | | Rule only |
| 121 | 14.135 | Process explainer | Core | How does a disaster declaration bring federal help, and who asks for it at each step? | `govinfo-disaster-declaration-steps` | The Stafford Act, 42 U.S.C. 5170 (major disasters) and 5191 (emergencies), from govinfo; FEMA's regulation, 44 CFR part 206, subpart B (the declaration process) and the assistance sections its steps cite, from eCFR's API | Law in force on the retrieval date | United States: local, state, tribal and federal roles | Congress, agencies and public services (V7 I063) | None | Primary |
| 122 | 14.136 | By-the-numbers panel | Core | What do public schools spend, and where does the money come from? | `census-school-system-finances-2024` | U.S. Census Bureau, 2024 Annual Survey of School System Finances, summary tables; the National Center for Education Statistics' Digest for any fact the survey lacks | Fiscal 2024 | United States, every public school system | Housing, health care and getting ahead (V7 I137, "Education") | None, unless a fact names the highest and lowest state | Primary |
| 123 | 14.137 | Comparison cards | Core | How do the three kinds of federal trial judges differ: district, bankruptcy and magistrate judges? (data lead change 1) | `uscode-federal-trial-judges` | U.S. Code, 2024 edition, 28 U.S.C. 133, 134, 152, 631 and 633, from govinfo; the Administrative Office of the U.S. Courts, Types of Federal Judges and Judicial Business 2025 | Law in force on the retrieval date; seats as of September 30, 2025 | United States, the federal district courts | Checks on power and equal justice | None | Primary |
| 124 | 14.138 | Step-by-step | Core | How do I ask a federal agency for its records, and what can I do if it says no? | `govinfo-foia-request-steps` | The Freedom of Information Act, 5 U.S.C. 552, from govinfo; the Justice Department's guide on FOIA.gov; the National Archives' Office of Government Information Services, for mediation | Law in force on the retrieval date | United States, federal agencies | News, records and public information (V7 I013) | None | Primary |
| 125 | 14.139 | Annotated illustration | Extended | What does the first page of a law tell a reader? (data lead change 2) | `govinfo-pl-119-12-first-page` | U.S. Government Publishing Office, Public Law 119-12, the TAKE IT DOWN Act, 139 Stat. 55, from govinfo | Approved May 19, 2025 | United States | Congress, agencies and public services | None | Primary |
| 126 | 14.140 | Calendar | Extended | Which dates does federal law set for the budget and for taxes in 2027? | `govinfo-budget-and-tax-deadlines-2027` | U.S. Code from govinfo: 2 U.S.C. 631 (the congressional budget timetable); 31 U.S.C. 1102 and 1105(a) (the fiscal year and the President's budget); 26 U.S.C. 6072(a), 6081, 6654 and 7503 (returns, extensions, estimated tax, and dates that fall on a weekend or holiday); 26 CFR 1.6081-4 (the automatic extension), from eCFR; IRS Publication 509 for 2027 as a check, if published | Calendar 2027 | United States | Taxes, wealth and economic security | None | Primary |
| 127 | 14.141 | Social data card | Core | How many residents per 100,000 does each state hold in prison? (S19's question, set at 1080 by 1350 and 1080 by 1080) | `bjs-imprisonment-rate-by-state` (S19's file, P7-003) | Bureau of Justice Statistics, Prisoners in 2023, Table 7 | Year-end 2023 | 50 states | Checks on power and equal justice | Mississippi, Massachusetts (as S19 names them) | Frozen |

Eleven rows draw data (115 to 118 and 121 to 127); two are rule only (one reference, one avoid). Tiers: 6 core, 5 extended, 1 reference, 1 avoid, as the proposal sets them. Ten new files, one of them derived; the social card draws a frozen file. Rows 123 and 125 carry the data lead's changes 1 and 2.

Notes the makers need, row by row:

- **115.** V7 claim CL1514, graded documented, gives union membership as 10.0 percent of wage and salary workers in 2025 and 20.1 percent in 1983, with 5.9 percent in the private sector and 32.9 percent in the public sector, 14.7 million members in all, from the Bureau of Labor Statistics' release of February 18, 2026. bls.gov refused this container (HTTP 403 at 18:57 UTC) and the Bureau's data API answered 503, so the figures come from V7 by script, and the source line prints the release "as recorded in" the atlas, the way S41 prints its survey. V7's limitation travels with them: 2025 averages 11 months, since the October 2025 survey was not collected, and V7's source note says 2025 is not strictly comparable with other annual averages. An icon array rounds to whole people (10 of 100; 20 of 100 in 1983) and the table prints the published figures. If you want the Bureau's own table, it becomes download item 3.
- **116.** The Bureau's 2022 Census of Governments counts each government by type. Circles sized by area, with a key, suit counts that run from one federal government to tens of thousands of special districts, since area compresses a range that wide; the table prints every count. School systems run by a state, county or city count as part of that government, and the note says so. This is chapter 14's widest view of levels of government (Rule 01.12), and it shows school districts as one kind.
- **117 and 118.** One file drawn two ways, as rows 109 and 111 draw one results file. DP03 gives, for the civilian noninstitutionalized population, the number with health insurance coverage, with private coverage, with public coverage and with none, each with its margin of error. A person can hold both kinds, so private plus public exceeds the insured. The derived file sets out four regions (private only, both, public only, none) by adding and subtracting the published counts, with approximate margins, and the sidecar names the method. The Venn draws the four regions with their counts printed; the Euler draws the two circles at true area inside a frame for the whole population, with the uninsured as the space outside both. The Bureau counts TRICARE as private coverage and VA care as public, and the sidecar lists each side's plans. No region is ranked against another unless the gap passes its margin (DR-64).
- **121.** The explainer draws the path the law sets: the local and state response, a joint damage assessment, the request from a governor or a tribal chief executive, FEMA's review, the President's declaration of an emergency or a major disaster, and the kinds of help a declaration opens, with each time limit the regulation sets, read at the fetch. Icons stand for the actor at each level. FEMA's own pages refused this container (HTTP 403 at 18:57 UTC), so the steps rest on the statute and the regulation; OpenFEMA's data API answered, and the steps do not need it. The plate prints the date of the law it draws.
- **122.** Four to six facts from the Bureau's fiscal 2024 tables, each naming its own table in its source line: total revenue and the shares from federal, state and local sources; current spending per pupil; enrollment; and the share of students in the largest school systems, if the tables give it. A fact that names the highest and the lowest state counts toward both. The panel leaves out a count of school districts: the finance survey counts public school systems as the Bureau defines them, dependent systems included, so its count differs from row 116's, and two counts on one page would mislead. If the Bureau's notes flag one-time federal relief in fiscal 2024, the qualification says so. This is the school district example your round 3 note asked for (Rule 01.10).
- **123.** One card for each kind of judge, the same fields on each: who appoints, with whose consent, for how long, what cases they hear, how many seats there are, and who sets that number. District judges: appointed by the President with the Senate's consent, during good behavior; 677 positions on September 30, 2025, with Congress setting the number by law (28 U.S.C. 133 lists 673, four shared between districts). Bankruptcy judges: appointed by the circuit's court of appeals for 14 years; 345 judgeships authorized and funded (section 152(a)(2) lists 316; temporary judgeships sit in its notes). Magistrate judges: appointed by the district judges for 8 years full time or 4 part time; 593 positions, whose number the Judicial Conference sets. The cases each hears come from the courts' own page. No appointing president or party appears, as S49 leaves them out.
- **124.** The steps are what a requester does: find the agency's FOIA office, write a request that reasonably describes the records, say what fees you will pay or ask for a waiver, ask for expedited processing where the law allows it, appeal a denial, ask the Office of Government Information Services to mediate, and go to court. Each time limit is the statute's, read at the fetch; the plate calls it a limit in law, since V7 I013 records that agencies often take longer. The steps cover federal agencies only; each state has its own public records law, and the note says so.
- **125.** The callouts name each part a reader meets on the law's first page, as the page prints it: the running head, the Public Law number (119-12) and the Congress, the Statutes at Large citation (139 Stat. 55), the date approved (May 19, 2025), the bill number ([S. 146]), the long title, the enacting clause, the short title section and the U.S. Code margin note. The page sets its running head with dashes, so the file lists it in parts. S62 follows the same bill to its signing, so a reader can go from the steps to the text. Nothing is invented.
- **126.** The calendar marks 2027's dates as the statutes set them, with 26 U.S.C. 7503 moving any date that falls on a weekend or legal holiday, each with its section. The Budget Act's timetable and the tax dates differ in kind, and the plate says which dates the law attaches a consequence to and which are targets, as the text reads. A note says the IRS may postpone tax dates for a federally declared disaster (26 U.S.C. 7508A), which ties this plate to row 121.
- **127.** The card redraws S19's chart and finding from its frozen file at 1080 by 1350 and 1080 by 1080. Fifty labeled rows at a card's type size may not fit the square card; the card may then label the highest and lowest states and draw the rest as unlabeled dots, saying so, under DR-64's rule for a drawing that changes form with the same data and finding. S19 is a core specimen in one of the two smallest domains, and a ranked list of 50 states is the hardest crop a card takes.

## Rule 01.9 count for chapter 14 as a whole

### 108 examples: rounds 0 to 3, the rule plates and round 4

| Domain | Specimens, rounds 0 to 3 | Rule plates | Round 4 | Total | Share | Limit 27 |
|---|---|---|---|---|---|---|
| Taxes, wealth and economic security | 13 | 2 | 1 (calendar) | 16 | 14.8% | Holds |
| Elections and representation | 11 | 1 | 0 | 12 | 11.1% | Holds |
| Housing, health care and getting ahead | 10 | 1 | 3 (Venn, Euler, by-the-numbers) | 14 | 13.0% | Holds |
| Congress, agencies and public services | 8 | 2 | 3 (proportional symbols, process explainer, annotated law) | 13 | 12.0% | Holds |
| Work, pay and bargaining power | 9 | 0 | 1 (icon array) | 10 | 9.3% | Holds |
| Taking part, trust and shared norms | 4 | 4 | 0 | 8 | 7.4% | Holds |
| Money, lobbying and influence | 6 | 1 | 0 | 7 | 6.5% | Holds |
| News, records and public information | 4 | 1 | 1 (step-by-step) | 6 | 5.6% | Holds |
| Competition and market power | 5 | 1 | 0 | 6 | 5.6% | Holds |
| Checks on power and equal justice | 5 | 0 | 2 (comparison cards, social card) | 7 | 6.5% | Holds |
| Atlas-wide | 9 | 0 | 0 | 9 | 8.3% | No single domain |
| **All** | **84** | **13** | **11** | **108** | | |

The largest domain, taxes, wealth and economic security, holds 16 of 108, eleven under the limit. Every domain supplies at least six examples.

**By state.** California and Florida reach 5 each (Rule 14.9's plate, S12, S54, S55 and row 108; Rule 14.9's plate, S12, S16, S54 and S55); New York 4 (Rule 14.9's plate, S11, S12 and S16); Texas, North Dakota, Michigan, Ohio, Illinois, Mississippi and Massachusetts 2 each; Washington and Alaska 1 each. Row 122 names New York and Idaho only if its spec prints the highest and lowest state. The limit is 21. Round 2's states come from all 22 round 2 specs as written at 19:16 UTC; the build's log recounts every state from the finished titles.

**Level and region (Rule 01.12).** Round 4 adds a school district example (row 122, every public school system), every kind of government in one view (row 116), local, state, tribal and federal roles in one process (row 121), and the federal trial courts' three kinds of judges (row 123). It names no new state. With round 4, chapter 14 has examples at the federal, state, county, city and school district levels, and named states in all four Census regions.

## Re-picks from the coverage plan (DR-229)

Nine round 4 forms change data, keeping their form and tier (seven as proposed, and rows 123 and 125 under the data lead's changes 1 and 2). Most reasons are ones the earlier rounds already signed off: a specimen or chapter that already draws the data, or a domain that needs the example.

| # | Form | Coverage plan data | New data | Why |
|---|---|---|---|---|
| 115 | Icon array | Child poverty as people out of 100 | Union membership, 2025 (V7 CL1514, from the Bureau of Labor Statistics) | S02 and row 57 already chart child poverty, the reason row 107 moved off it; "one in ten" is the form's own use in the coverage plan, and V7 files the figure under work and pay (I101) |
| 116 | Proportional symbols | Federal outlays by agency | Governments by type, 2022 Census of Governments | Rows 26, 44 and 48 already draw the Monthly Treasury Statement, the reason row 100 moved off it; the counts span a range area shows better than length, and the view brings every level of government, school districts among them (Rule 01.12) |
| 117, 118 | Venn, Euler | States with a citizen initiative and states that ban ranked-choice voting | People with private health coverage, public coverage, both or neither, 2025 | S07 and row 87 already draw the Ballotpedia ban list, the reason row 113 moved off ranked-choice data; coverage types are groups of people that truly overlap, the case the creative director's correction looked for when it set aside party voters, who cannot overlap |
| 121 | Process explainer | How a ballot measure gets on the ballot | How a disaster declaration brings federal help | Chapter 11's ballot measure tracker (DR-231) and chapter 15's workflow for the citizen initiative route (researched in `work/research/20261111_Policy-Workflow-Sources.md`, section BI) are set to draw that route, the reason row 86 moved off lawmaking steps; a declaration shows local, state, tribal and federal roles in one process (V7 I063) |
| 122 | By-the-numbers panel | V7 headline figures | Public school finances, fiscal 2024 | S60's indicator row draws the same `v7-numbers` file; school systems give chapter 14 its first school district example (your round 3 note on Rule 01.10) |
| 124 | Step-by-step | Registering to vote in a state | Requesting federal records under FOIA | Moved off election data as signed off in the rounds 1 and 2 plan. Applying for a benefit, the first proposal, is now row 102's journey map, so your round 3 change 3 asked for another process and named public records, which lifts one of the two smallest domains (V7 I013) |
| 123 | Comparison cards | Top-two against top-four primaries | The three kinds of federal trial judges | Data lead change 1: the coverage plan writes the form's use as "Two or three options side by side", not an election question (round 3's DR-229 test), and the cards would have printed Alaska's uncertified 2026 measure |
| 125 | Annotated illustration | A ballot with ranked choices marked | The first page of Public Law 119-12 | Data lead change 2: the form's use is "A drawing with callouts"; S07 and row 87 already carry ranked-choice voting; nothing invented |
| 127 | Social data card | Any core specimen | S19's imprisonment rates by state | A core specimen in checks on power and equal justice, one of the two smallest domains; no new data |

Kept as signed off: row 126 moves the calendar to federal budget and tax deadlines, as the rounds 1 and 2 plan set and you signed off. No round 4 form keeps election data (next section).

## Election data in round 4 (DR-229)

The rounds 1 and 2 plan moved two round 4 forms off election data, the calendar and the step-by-step, and named the ranked ballot, the Venn and Euler of state election rules and the comparison cards on primaries as forms that keep it; the round 3 plan also counted the ballot measure explainer under elections. In round 3 you kept the decision tree on election data because the coverage plan wrote its use as the ranked-choice question. By that test, none of round 4's forms is built for elections: each use in the coverage plan is general ("Two or three groups that overlap", "A drawing with callouts", "Two or three options side by side", "Steps of a public process with icons").

I re-picked three of the five for reasons the earlier rounds signed off (the Venn, the Euler and the process explainer, above). The other two draw data nothing else in the guide draws, and the signed-off list names them, so they keep election data: the comparison cards on top-two and top-four primaries (row 123) and the annotated ranked ballot (row 125). If you read DR-229 as the round 3 test reads it, both move as well; sign-off point 2 proposes data for each. Elections and representation reaches 14 of 108 with them and 12 without, and the count holds either way.

**Outcome.** The data lead applied round 3's test to both (sign-off point 2, changes 1 and 2): rows 123 and 125 move, and round 4 draws no election data.

## Datasets to fetch and freeze

After your sign-off. Each goes into `work/build/data/` under contract C1 with a sidecar and a row in the research ledger's Part 7, from P7-301 on (round 4's rows take the 300s).

| Dataset | Rows | Host | How | Answered today (UTC) |
|---|---|---|---|---|
| `v7-union-membership` | 115 | Repository | A V7 extract script reading claim CL1514 and source S04 from `work/extract/atlas-v7-data.json` | Not a host |
| `census-cog-2022-governments-by-type` | 116 | www2.census.gov | The Census of Governments' 2022 organization tables | 200 at 19:01 (the 2022 tables folder) |
| `census-acs-health-coverage-types`, `census-acs-health-coverage-overlap` (derived) | 117, 118 | api.census.gov | ACS 1-year 2025, DP03, key from the environment | 200 at 18:57 and 19:01 (the 2025 ACS 1-year listing) |
| `govinfo-disaster-declaration-steps` | 121 | www.govinfo.gov; www.ecfr.gov's API | Statute and regulation text | 200 at 18:57, both |
| `census-school-system-finances-2024` | 122 | www2.census.gov; nces.ed.gov | The fiscal 2024 tables; the Digest if needed | 200 at 19:01, both (the 2024 tables folder) |
| `uscode-federal-trial-judges` | 123 | www.govinfo.gov, www.uscourts.gov | Statute text; the courts' pages and Judicial Business 2025 | 200 each at 19:23 to 19:31 |
| `govinfo-foia-request-steps` | 124 | www.govinfo.gov, www.foia.gov, www.justice.gov, www.archives.gov | Statute text and the agencies' pages | 200 each at 18:57 to 19:01 |
| `govinfo-pl-119-12-first-page` | 125 | www.govinfo.gov | The law's PDF and HTML text | 200 at 19:23 |
| `govinfo-budget-and-tax-deadlines-2027` | 126 | www.govinfo.gov, www.ecfr.gov, www.irs.gov | Statute and regulation text; Publication 509 as a check | 200 each at 18:57 to 19:01 |
| `bjs-imprisonment-rate-by-state` | 127 | None | Frozen in round 0 (P7-003) | Not fetched |

Refused today, with no row depending on them: www.bls.gov (403) and its data API (503); www.fema.gov's pages (403); the California and Washington legislatures' code sites (403); www.ssa.gov, www.dol.gov, www.medicaid.gov, www.gao.gov, www.cdc.gov, www.ed.gov, www.ncsl.org and www.nysenate.gov (403 each). The logs are in my scratch folder (`.../phase-3/round-2/research/reach/`).

## Download list (DR-230)

No download is needed. Row 115 reads the Bureau of Labor Statistics' figures through V7; if you want the Bureau's own table, it becomes download item 3: the "Union Members" news release's Table 1 from https://www.bls.gov/news.release/union2.t01.htm, saved as HTML.

## What stays Illustrative

None. Every row draws a primary source or V7 (data lead change 2).

## For the data lead's sign-off

Please check seven things, under Rule 01.9 and DR-229:

1. **The seven re-picks** (rows 115, 116, 117 and 118, 121, 122, 124 and 127), form by form, against what each form teaches.
2. **Rows 123 and 125 under DR-229.** Keep election data, as the signed-off list names them, or move them as the round 3 test reads DR-229. If they move, I propose for row 123 three kinds of federal judges side by side (district judges, bankruptcy judges and magistrate judges: who appoints them, for how long, and what they hear, from 28 U.S.C. and the courts' own pages; checks on power and equal justice), and for row 125 the first page of a public law with callouts for its parts (govinfo; Congress, agencies and public services).
3. **Row 124.** The brief's words for this form were "applying for a benefit"; your round 3 change 3 set that aside, since row 102 now draws it, and named public records. If you prefer a benefit after all, the alternative is applying for free or reduced-price school meals through the school district (7 CFR part 245, from eCFR; USDA's Food and Nutrition Service), which would be a second school district example and a third benefit process under Congress and agencies (rows 83 and 102).
4. **Domains.** Row 126 under taxes, wealth and economic security, where V7's overview names the federal budget, or under Congress and agencies, whose budget subsystem holds the shutdown deadline (I054); row 121 under Congress and agencies (I063) rather than housing's environment subsystem (I143); row 115 under work and pay (I101).
5. **Row 115's source.** V7's claim, which cites the release, against the Bureau's own table, which needs download item 3.
6. **Drawing rules a maker needs from you:** the Euler's frame for the whole population and where the uninsured sit; one year or two on the icon array, given V7's note that 2025 is not strictly comparable; the social card's crop at 1080 by 1080.
7. **The count:** the 13 rule plates in it, S38 counted under news and records, and the social card counted as its own example.

Reply in your notes with "signed off" or the changes. I fetch nothing you change until I re-pick it.

## Requests

- **To the main session.** The fetch and freeze scripts for this plan, like round 2's fix scripts, live in my scratch folder, since the round 2 ownership table gives me no script in `work/build/scripts/`. Each sidecar names its method, and each ledger row its source. If you want the scripts in the repository, as round 1's were, name the file and I copy them there.

## Data lead sign-off

**Signed off with two changes**, November 12, 2026, by the data visualization and systems lead, under Rule 01.9, DR-229 and the approved palettes (DR-236). Rows 115 to 118, 121, 122, 124, 126 and 127 may be fetched now. Rows 123 and 125 change data (changes 1 and 2); fetch them once re-picked as below. The conditions after the changes are for the makers and change nothing you fetch.

**What I checked, and how**

- The plan read in full against the rounds 1 and 2 plan, the round 3 plan and my sign-offs of both, and the coverage plan's rows for the 13 forms.
- By script: the generator's log, `work/build/guide/entries/14-example-log.json`, holds 13 plates for rules 14.1 to 14.13, in the domains the plan gives (taking part 4, Congress and agencies 2, taxes 2, and one each in competition, elections, housing, news and money). The 22 round 2 specs carry the domains the rounds 1 and 2 plan gave them (housing 6, taxes 7, work and pay 3, checks on power 2, and one each in elections, Congress and agencies, news, and atlas-wide), and name Vermont, Alaska, Florida, California, North Dakota and Illinois. Rounds 0 to 3 then read as the plan's table, with S38 under news and records, since its spec took domain D01 in round 1's fix pass.
- By script on `work/extract/atlas-v7-data.json`: claim CL1514 (graded documented: 10.0 percent in 2025, 20.1 percent in 1983, 5.9 percent private and 32.9 percent public, 14.7 million members; limitation: 2025 averages 11 months, since the October 2025 survey was not collected); issues I101 (D07), I165 and I063 (D04), I133, I137 and I143 (D09), I013 (D01) and I054 (D04, Budget). Each matches the plan.

**The seven points**

1. *The re-picks.* Signed off for rows 115, 116, 117 and 118, 121, 122, 124 and 127. Each keeps its form and tier and teaches what the form is for: a share as people out of 100, counts too far apart for length, groups that truly overlap, a public process with a role at each level of government, four to six sourced facts, steps a reader takes, and one chart cropped for a social feed. Rows 116 and 122 give chapter 14 every kind of government and its first school district example (Rule 01.10).
2. *Rows 123 and 125 move* (changes 1 and 2). One test for every round: a form keeps election data when the coverage plan writes its use as an election question, as it wrote the decision tree's ("Can my city adopt ranked-choice voting?"). The coverage plan writes these two uses as "Two or three options side by side" and "A drawing with callouts". The rounds 1 and 2 plan named them before round 3 set that test, and row 113 moved off ranked-choice data under it, with S07 and row 87 already carrying ranked-choice voting. Row 123 would also print Alaska's Ballot Measure 2 before the state certifies it (target November 25, 2026), so the plate could be out of date the week it is built.
3. *Row 124.* Signed off: the federal records request. It lifts news and records, one of the two smallest domains, and row 122 already gives the school district example that school meals would have brought.
4. *Domains.* Signed off as written: row 126 under taxes, wealth and economic security, since most of its dates are tax dates; row 121 under Congress, agencies and public services (I063, "Overlapping federal, state and local roles leave gaps", the question's own subject); row 115 under work, pay and bargaining power (I101).
5. *Row 115's source.* V7's claim CL1514, graded documented, citing the Bureau's release, printed "as recorded in" the atlas, as S41 prints its survey. No download item 3. V7's limitation prints with the figure.
6. *Drawing rules,* under "Conditions for the makers" below: the Euler draws no frame at true area; the icon array draws 2025 alone; both social card crops label only the states the title names.
7. *The count.* Signed off: the 13 rule plates count, S38 counts under news and records, and the social card counts as its own example, as S41 and S42 each count. Counting it with S19 gives 107 and changes no limit.

**Changes**

1. **Row 123, comparison cards: the three kinds of federal trial judges side by side,** as the plan proposes: district judges, bankruptcy judges and magistrate judges, each card with the same fields (who appoints, with whose consent, for how long, what cases they hear, how many seats there are and who sets that number), from 28 U.S.C. (sections 133 and 134, 152, and 631 and 633, read at the fetch) and the federal courts' own pages. Domain: checks on power and equal justice. No state. No appointing president or party, as S49 leaves them out.
2. **Row 125, annotated illustration: the first page of a public law with callouts,** from govinfo, naming each part a reader meets: the Public Law number, the Statutes at Large citation, the date approved, the long title, the enacting clause, the short title section and the bill number it came from. I suggest Public Law 119-12, the TAKE IT DOWN Act, since S62 follows that bill to its signing and a reader could then go from the steps to the text; it passed the Senate by unanimous consent and the House 409 to 2. Pick another short public law if its first page lacks a part. Domain: Congress, agencies and public services. Nothing in it is invented, so "What stays Illustrative" becomes none.

**The count with both changes:** 108 examples. Taxes, wealth and economic security 16; housing, health care and getting ahead 14; Congress, agencies and public services 13; elections and representation 12; work, pay and bargaining power 10; atlas-wide 9; taking part 8; money 7; checks on power 7; news and records 6; competition 6. The largest holds 16 against 27, and every domain holds at least six. By state: California 5 and Florida 5, the most, against 21; Washington and Alaska fall to one each and Maine leaves the count. Named states remain in all four Census regions.

**Conditions for the makers** (no change to the fetch)

- **Row 115, icon array.** One array for 2025: 10 of 100. The 1983 figure, 20.1 percent, and the private and public sector figures go in the note with V7's limitation, since V7 qualifies the 2025 average and two arrays would invite a comparison it qualifies. The named-mark ruling follows when the title is drafted, under round 2's principles.
- **Row 116, proportional symbols.** Circles at true area with a key for the local kinds. The federal government (1) and the 50 states print as counts in words beside the circles, since at true area their circles would draw under a pixel and a few pixels across. The table prints every count.
- **Rows 117 and 118.** The Venn draws a frame for everyone, with four regions and their counts printed, and its note says the circles' sizes carry no count. The Euler draws the private and public circles and their overlap at true area, and the uninsured as a third circle apart at true area, named, with no frame. A frame at true area would have to leave the uninsured as its spare space, and two circles cannot fill a rectangle that tightly: with the uninsured near 8 percent, as recent years run, the corners the larger circle leaves inside the frame already take more space than that. Check the shares at the fetch; if the uninsured share is large enough for a frame to work, ask me again. The everyone count goes in the measure line.
- **Rows 121, 124 and 126.** Each prints the date of the law it draws. Times are limits in law, and the titles say so (as rows 86 and 102). Row 126's note says which dates carry a consequence in law and which are targets.
- **Row 122.** Each fact names its table; the note says so if fiscal 2024 includes one-time federal pandemic relief.
- **Row 127, social card.** Both crops, 1080 by 1350 and 1080 by 1080, draw all 50 states as dots in rank order and label only the two the title names (Mississippi and Massachusetts, in the subject ink, as S19 draws them) and the all-states line (round 2 ruling (b)). A 1080 px card shows at about 390 px on a phone, about a third of its size, so 50 row labels at a size a reader can read would need far more height than either crop has. The card says each dot is a state and where the full list is.
- **Every row.** Parties appear in words only where a law names them (DR-48, DR-58); no disclosure (DR-100); no red and blue.

## Research lead, after the sign-off

Applied November 12, 2026, before the fetch. The tables above now carry both changes; this list says where, and what the fetch confirmed.

- **Change 1, row 123.** The comparison cards draw the three kinds of federal trial judges from `uscode-federal-trial-judges`, under checks on power and equal justice, with no state. The sections the sign-off names were read in the U.S. Code's 2024 edition on govinfo: 28 U.S.C. 133(a) (the President appoints district judges with the Senate's consent; its table lists 673 judgeships, four shared between districts), 134(a) (they "shall hold office during good behavior"), 152(a) (the circuit's court of appeals appoints bankruptcy judges "for a term of fourteen years"; its table lists 316, and its notes carry temporary judgeships), 631(a) and (e) (the district judges appoint magistrate judges, for eight years full time and four part time) and 633(b) (the Judicial Conference "shall determine" their number). Seats come from the courts' Judicial Business 2025, as of September 30, 2025: 677 district positions, 345 bankruptcy judgeships and 593 magistrate judge positions. The courts' counts include temporary judgeships the statute tables leave out; the 677 against 673 was not traced seat by seat.
- **Change 2, row 125.** The annotated illustration draws Public Law 119-12's first page from `govinfo-pl-119-12-first-page`, under Congress, agencies and public services. The page has every part the sign-off lists, read from the law's PDF and HTML on govinfo: Public Law 119-12, 119th Congress, 139 Stat. 55, May 19, 2025, [S. 146], the long title, the enacting clause and section 1's short title, with the U.S. Code margin note. "What stays Illustrative" now reads none.
- **The count** reads as the sign-off gives it, by the same script: 108 examples; taxes, wealth and economic security 16, the largest, against 27; California and Florida 5 each against 21; no state newly named.
- **The uninsured share, confirmed at the fetch:** 8.4 percent in 2025 (margin 0.1), 28,323,306 of 336,838,154 people in the civilian noninstitutionalized population. The Euler stays at true area with no frame.
- **Other statute sections confirmed at the fetch,** each quoted in its file: 42 U.S.C. 5170 and 5191 and 44 CFR 206.33 to 206.40, 206.112 and 206.202 (row 121); 5 U.S.C. 552 (row 124); 2 U.S.C. 631, 31 U.S.C. 1102, 1105 and 1341, 26 U.S.C. 6072, 6081, 6651, 6654, 7503 and 7508A, and 26 CFR 1.6081-4 (row 126). IRS Publication 509 for 2027 is not yet published, so the weekend and holiday rule was checked against the 2026 edition; no 2027 tax date falls on a weekend or a District of Columbia legal holiday.
- **Two findings the makers need.** The Census Bureau's documentation says fiscal 2024's federal school revenue includes COVID-19 relief; summed over every school system from its all data items file, relief came to $39.2 billion of $115.1 billion (row 122's qualification and fact 5). Table 13 labels its enrollment row "Fall enrollment, 2022" but prints Table 19's fall 2023 figure; the file takes Table 19.

### Conditions for round 4's maker

From the data lead's sign-off, gathered here so round 4's maker reads them with the rows:

- **Row 115, icon array.** One array for 2025 alone: 10 of 100. The 1983 figure (20.1 percent), the private and public sector figures and V7's limitation go in the note. The named-mark ruling follows when the title is drafted.
- **Row 116, proportional symbols.** Circles at true area, with a key, for the five kinds of local government. The federal government (1) and the states (50) print as counts in words beside the circles. The table prints every count.
- **Rows 117 and 118.** The Venn draws a frame for everyone, with four regions and their counts printed, and its note says the circles' sizes carry no count. The Euler draws the private and public circles and their overlap at true area, and the uninsured as a third circle apart at true area, named, with no frame; the count for everyone goes in the measure line.
- **Rows 121, 124 and 126.** Each prints the date of the law it draws. Times are limits in law, and the titles say so. Row 126's note says which dates carry a consequence in law and which are targets (the file's `kind` and `consequence` columns).
- **Row 122.** Each fact names its table; the note says fiscal 2024's federal revenue includes $39.2 billion in COVID-19 relief.
- **Row 123.** The same fields on every card; no appointing president or party.
- **Row 127, social card.** Both crops, 1080 by 1350 and 1080 by 1080, draw all 50 states as dots in rank order and label only the two the title names, Mississippi and Massachusetts, in the subject ink, as S19 draws them, with the all-states line. The card says each dot is a state and where the full list is.
- **Every row.** Parties appear in words only where a law names them (DR-48, DR-58); no disclosure (DR-100); no red and blue.

**Status of every dataset, November 12, 2026, 19:40 UTC.** Frozen in `work/build/data/` with sidecars under C1 and research ledger rows P7-301 to P7-310: rows 115 (`v7-union-membership`), 116 (`census-cog-2022-governments-by-type`), 117 and 118 (`census-acs-health-coverage-types` and the derived `census-acs-health-coverage-overlap`), 121 (`govinfo-disaster-declaration-steps`), 122 (`census-school-system-finances-2024`), 123 (`uscode-federal-trial-judges`), 124 (`govinfo-foia-request-steps`), 125 (`govinfo-pl-119-12-first-page`) and 126 (`govinfo-budget-and-tax-deadlines-2027`). Row 127 draws S19's frozen `bjs-imprisonment-rate-by-state` (P7-003). The data check reads 111 tables with 0 faults. Nothing waits.
