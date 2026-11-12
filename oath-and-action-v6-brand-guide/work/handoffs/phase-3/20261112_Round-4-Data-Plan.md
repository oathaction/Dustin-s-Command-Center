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
| 123 | 14.137 | Comparison cards | Core | How do a top-two primary and a top-four primary differ? | `usgov-primary-systems-top-two-top-four` | The California and Washington Secretaries of State, their pages on the top-two primary; Alaska Statutes, title 15, from the Alaska Legislature; the Alaska Division of Elections for the status of Ballot Measure 2 of November 3, 2026 | Law in force on the retrieval date; Alaska's 2026 measure as counted on that date | California, Washington and Alaska | Elections and representation | California, Washington, Alaska | Primary |
| 124 | 14.138 | Step-by-step | Core | How do I ask a federal agency for its records, and what can I do if it says no? | `govinfo-foia-request-steps` | The Freedom of Information Act, 5 U.S.C. 552, from govinfo; the Justice Department's guide on FOIA.gov; the National Archives' Office of Government Information Services, for mediation | Law in force on the retrieval date | United States, federal agencies | News, records and public information (V7 I013) | None | Primary |
| 125 | 14.139 | Annotated illustration | Extended | How do I mark a ranked-choice ballot, and what happens to a ranking I skip or double? | `maine-rcv-ballot-rules`, with the ballot's office and candidates invented | Maine Revised Statutes, title 21-A, section 723-A (ranked-choice tabulation), from the Maine Legislature; the Maine Secretary of State's ranked-choice voting instructions | Law in force on the retrieval date | Maine | Elections and representation | Maine | Primary rules; Illustrative names |
| 126 | 14.140 | Calendar | Extended | Which dates does federal law set for the budget and for taxes in 2027? | `govinfo-budget-and-tax-deadlines-2027` | U.S. Code from govinfo: 2 U.S.C. 631 (the congressional budget timetable); 31 U.S.C. 1102 and 1105(a) (the fiscal year and the President's budget); 26 U.S.C. 6072(a), 6081, 6654 and 7503 (returns, extensions, estimated tax, and dates that fall on a weekend or holiday); 26 CFR 1.6081-4 (the automatic extension), from eCFR; IRS Publication 509 for 2027 as a check, if published | Calendar 2027 | United States | Taxes, wealth and economic security | None | Primary |
| 127 | 14.141 | Social data card | Core | How many residents per 100,000 does each state hold in prison? (S19's question, set at 1080 by 1350 and 1080 by 1080) | `bjs-imprisonment-rate-by-state` (S19's file, P7-003) | Bureau of Justice Statistics, Prisoners in 2023, Table 7 | Year-end 2023 | 50 states | Checks on power and equal justice | Mississippi, Massachusetts (as S19 names them) | Frozen |

Eleven rows draw data (115 to 118 and 121 to 127); two are rule only (one reference, one avoid). Tiers: 6 core, 5 extended, 1 reference, 1 avoid, as the proposal sets them. Nine new files, one of them derived; the social card draws a frozen file.

Notes the makers need, row by row:

- **115.** V7 claim CL1514, graded documented, gives union membership as 10.0 percent of wage and salary workers in 2025 and 20.1 percent in 1983, with 5.9 percent in the private sector and 32.9 percent in the public sector, 14.7 million members in all, from the Bureau of Labor Statistics' release of February 18, 2026. bls.gov refused this container (HTTP 403 at 18:57 UTC) and the Bureau's data API answered 503, so the figures come from V7 by script, and the source line prints the release "as recorded in" the atlas, the way S41 prints its survey. V7's limitation travels with them: 2025 averages 11 months, since the October 2025 survey was not collected, and V7's source note says 2025 is not strictly comparable with other annual averages. An icon array rounds to whole people (10 of 100; 20 of 100 in 1983) and the table prints the published figures. If you want the Bureau's own table, it becomes download item 3.
- **116.** The Bureau's 2022 Census of Governments counts each government by type. Circles sized by area, with a key, suit counts that run from one federal government to tens of thousands of special districts, since area compresses a range that wide; the table prints every count. School systems run by a state, county or city count as part of that government, and the note says so. This is chapter 14's widest view of levels of government (Rule 01.12), and it shows school districts as one kind.
- **117 and 118.** One file drawn two ways, as rows 109 and 111 draw one results file. DP03 gives, for the civilian noninstitutionalized population, the number with health insurance coverage, with private coverage, with public coverage and with none, each with its margin of error. A person can hold both kinds, so private plus public exceeds the insured. The derived file sets out four regions (private only, both, public only, none) by adding and subtracting the published counts, with approximate margins, and the sidecar names the method. The Venn draws the four regions with their counts printed; the Euler draws the two circles at true area inside a frame for the whole population, with the uninsured as the space outside both. The Bureau counts TRICARE as private coverage and VA care as public, and the sidecar lists each side's plans. No region is ranked against another unless the gap passes its margin (DR-64).
- **121.** The explainer draws the path the law sets: the local and state response, a joint damage assessment, the request from a governor or a tribal chief executive, FEMA's review, the President's declaration of an emergency or a major disaster, and the kinds of help a declaration opens, with each time limit the regulation sets, read at the fetch. Icons stand for the actor at each level. FEMA's own pages refused this container (HTTP 403 at 18:57 UTC), so the steps rest on the statute and the regulation; OpenFEMA's data API answered, and the steps do not need it. The plate prints the date of the law it draws.
- **122.** Four to six facts from the Bureau's fiscal 2024 tables, each naming its own table in its source line: total revenue and the shares from federal, state and local sources; current spending per pupil; enrollment; and the share of students in the largest school systems, if the tables give it. A fact that names the highest and the lowest state counts toward both. The panel leaves out a count of school districts: the finance survey counts public school systems as the Bureau defines them, dependent systems included, so its count differs from row 116's, and two counts on one page would mislead. If the Bureau's notes flag one-time federal relief in fiscal 2024, the qualification says so. This is the school district example your round 3 note asked for (Rule 01.10).
- **123.** The cards give each system the same fields: who may run, who may vote in the primary, how many advance, how the general election is counted, where it is used for congressional and state offices and since when, and the law that sets it. Top-two: California and Washington. Top-four with a ranked general election: Alaska. California's and Washington's code sites refused this container (HTTP 403), so their rules come from each Secretary of State's own page. Alaska's Ballot Measure 2 of November 3, 2026, which would repeal the top-four system, trailed in the unofficial count of November 10 (P7-036a), and the Division set November 25, 2026 as its target date to certify; the cards print the measure's status on the retrieval date, with that date. The Division's site sends an incomplete certificate chain, which round 0 read with verification on by adding the missing intermediate certificate; if it fails, Ballotpedia, labeled secondary, gives the status cell alone. Parties appear in words only, where a law names them (DR-48, DR-58). The coverage plan's disclosure is retired (DR-100).
- **124.** The steps are what a requester does: find the agency's FOIA office, write a request that reasonably describes the records, say what fees you will pay or ask for a waiver, ask for expedited processing where the law allows it, appeal a denial, ask the Office of Government Information Services to mediate, and go to court. Each time limit is the statute's, read at the fetch; the plate calls it a limit in law, since V7 I013 records that agencies often take longer. The steps cover federal agencies only; each state has its own public records law, and the note says so.
- **125.** One contest on a ranked ballot the studio draws to Maine's rules, with an invented office and invented candidates, labeled Illustrative and named for no real person or party. The callouts come from the statute and the Secretary of State's instructions: how to rank, what happens when a voter skips a ranking or marks two candidates at one ranking, and when a ballot stops counting. The disclosure is retired (DR-100).
- **126.** The calendar marks 2027's dates as the statutes set them, with 26 U.S.C. 7503 moving any date that falls on a weekend or legal holiday, each with its section. The Budget Act's timetable and the tax dates differ in kind, and the plate says which dates the law attaches a consequence to and which are targets, as the text reads. A note says the IRS may postpone tax dates for a federally declared disaster (26 U.S.C. 7508A), which ties this plate to row 121.
- **127.** The card redraws S19's chart and finding from its frozen file at 1080 by 1350 and 1080 by 1080. Fifty labeled rows at a card's type size may not fit the square card; the card may then label the highest and lowest states and draw the rest as unlabeled dots, saying so, under DR-64's rule for a drawing that changes form with the same data and finding. S19 is a core specimen in one of the two smallest domains, and a ranked list of 50 states is the hardest crop a card takes.

## Rule 01.9 count for chapter 14 as a whole

### 108 examples: rounds 0 to 3, the rule plates and round 4

| Domain | Specimens, rounds 0 to 3 | Rule plates | Round 4 | Total | Share | Limit 27 |
|---|---|---|---|---|---|---|
| Taxes, wealth and economic security | 13 | 2 | 1 (calendar) | 16 | 14.8% | Holds |
| Elections and representation | 11 | 1 | 2 (comparison cards, annotated ballot) | 14 | 13.0% | Holds |
| Housing, health care and getting ahead | 10 | 1 | 3 (Venn, Euler, by-the-numbers) | 14 | 13.0% | Holds |
| Congress, agencies and public services | 8 | 2 | 2 (proportional symbols, process explainer) | 12 | 11.1% | Holds |
| Work, pay and bargaining power | 9 | 0 | 1 (icon array) | 10 | 9.3% | Holds |
| Taking part, trust and shared norms | 4 | 4 | 0 | 8 | 7.4% | Holds |
| Money, lobbying and influence | 6 | 1 | 0 | 7 | 6.5% | Holds |
| News, records and public information | 4 | 1 | 1 (step-by-step) | 6 | 5.6% | Holds |
| Competition and market power | 5 | 1 | 0 | 6 | 5.6% | Holds |
| Checks on power and equal justice | 5 | 0 | 1 (social card) | 6 | 5.6% | Holds |
| Atlas-wide | 9 | 0 | 0 | 9 | 8.3% | No single domain |
| **All** | **84** | **13** | **11** | **108** | | |

The largest domain, taxes, wealth and economic security, holds 16 of 108, eleven under the limit. Every domain supplies at least six examples.

**By state.** California reaches 6 (Rule 14.9's plate, S12, S54, S55, row 108 and row 123); Florida 5 (Rule 14.9's plate, S12, S16, S54 and S55); New York 4 (Rule 14.9's plate, S11, S12 and S16); Texas, Washington, Alaska, North Dakota, Michigan, Ohio, Illinois, Mississippi and Massachusetts 2 each. The limit is 21. Round 2's states come from all 22 round 2 specs as written at 19:16 UTC; the build's log recounts every state from the finished titles.

**Level and region (Rule 01.12).** Round 4 adds a school district example (row 122, every public school system), every kind of government in one view (row 116), and local, state, tribal and federal roles in one process (row 121). Maine (Northeast) and California, Washington and Alaska (West) join the states already named. With round 4, chapter 14 has examples at the federal, state, county, city and school district levels, and named states in all four Census regions.

## Re-picks from the coverage plan (DR-229)

Seven round 4 forms change data, keeping their form and tier. Most reasons are ones the earlier rounds already signed off: a specimen or chapter that already draws the data, or a domain that needs the example.

| # | Form | Coverage plan data | New data | Why |
|---|---|---|---|---|
| 115 | Icon array | Child poverty as people out of 100 | Union membership, 2025 (V7 CL1514, from the Bureau of Labor Statistics) | S02 and row 57 already chart child poverty, the reason row 107 moved off it; "one in ten" is the form's own use in the coverage plan, and V7 files the figure under work and pay (I101) |
| 116 | Proportional symbols | Federal outlays by agency | Governments by type, 2022 Census of Governments | Rows 26, 44 and 48 already draw the Monthly Treasury Statement, the reason row 100 moved off it; the counts span a range area shows better than length, and the view brings every level of government, school districts among them (Rule 01.12) |
| 117, 118 | Venn, Euler | States with a citizen initiative and states that ban ranked-choice voting | People with private health coverage, public coverage, both or neither, 2025 | S07 and row 87 already draw the Ballotpedia ban list, the reason row 113 moved off ranked-choice data; coverage types are groups of people that truly overlap, the case the creative director's correction looked for when it set aside party voters, who cannot overlap |
| 121 | Process explainer | How a ballot measure gets on the ballot | How a disaster declaration brings federal help | Chapter 11's ballot measure tracker (DR-231) and chapter 15's workflow for the citizen initiative route (researched in `work/research/20261111_Policy-Workflow-Sources.md`, section BI) are set to draw that route, the reason row 86 moved off lawmaking steps; a declaration shows local, state, tribal and federal roles in one process (V7 I063) |
| 122 | By-the-numbers panel | V7 headline figures | Public school finances, fiscal 2024 | S60's indicator row draws the same `v7-numbers` file; school systems give chapter 14 its first school district example (your round 3 note on Rule 01.10) |
| 124 | Step-by-step | Registering to vote in a state | Requesting federal records under FOIA | Moved off election data as signed off in the rounds 1 and 2 plan. Applying for a benefit, the first proposal, is now row 102's journey map, so your round 3 change 3 asked for another process and named public records, which lifts one of the two smallest domains (V7 I013) |
| 127 | Social data card | Any core specimen | S19's imprisonment rates by state | A core specimen in checks on power and equal justice, one of the two smallest domains; no new data |

Kept as signed off: row 126 moves the calendar to federal budget and tax deadlines, as the rounds 1 and 2 plan set and you signed off. Kept as the coverage plan set them: rows 123 and 125, the comparison cards on primaries and the annotated ranked ballot, under the next section.

## Election data in round 4 (DR-229)

The rounds 1 and 2 plan moved two round 4 forms off election data, the calendar and the step-by-step, and named the ranked ballot, the Venn and Euler of state election rules and the comparison cards on primaries as forms that keep it; the round 3 plan also counted the ballot measure explainer under elections. In round 3 you kept the decision tree on election data because the coverage plan wrote its use as the ranked-choice question. By that test, none of round 4's forms is built for elections: each use in the coverage plan is general ("Two or three groups that overlap", "A drawing with callouts", "Two or three options side by side", "Steps of a public process with icons").

I re-picked three of the five for reasons the earlier rounds signed off (the Venn, the Euler and the process explainer, above). The other two draw data nothing else in the guide draws, and the signed-off list names them, so they keep election data: the comparison cards on top-two and top-four primaries (row 123) and the annotated ranked ballot (row 125). If you read DR-229 as the round 3 test reads it, both move as well; sign-off point 2 proposes data for each. Elections and representation reaches 14 of 108 with them and 12 without, and the count holds either way.

## Datasets to fetch and freeze

After your sign-off. Each goes into `work/build/data/` under contract C1 with a sidecar and a row in the research ledger's Part 7, from P7-301 on (round 4's rows take the 300s).

| Dataset | Rows | Host | How | Answered today (UTC) |
|---|---|---|---|---|
| `v7-union-membership` | 115 | Repository | A V7 extract script reading claim CL1514 and source S04 from `work/extract/atlas-v7-data.json` | Not a host |
| `census-cog-2022-governments-by-type` | 116 | www2.census.gov | The Census of Governments' 2022 organization tables | 200 at 19:01 (the 2022 tables folder) |
| `census-acs-health-coverage-types`, `census-acs-health-coverage-overlap` (derived) | 117, 118 | api.census.gov | ACS 1-year 2025, DP03, key from the environment | 200 at 18:57 and 19:01 (the 2025 ACS 1-year listing) |
| `govinfo-disaster-declaration-steps` | 121 | www.govinfo.gov; www.ecfr.gov's API | Statute and regulation text | 200 at 18:57, both |
| `census-school-system-finances-2024` | 122 | www2.census.gov; nces.ed.gov | The fiscal 2024 tables; the Digest if needed | 200 at 19:01, both (the 2024 tables folder) |
| `usgov-primary-systems-top-two-top-four` | 123 | www.sos.ca.gov, www.sos.wa.gov, www.akleg.gov, www.elections.alaska.gov | Official pages and statute text | 200, 200 and 200 at 18:57; the Alaska Division's site failed this container's certificate check, as in round 0 |
| `govinfo-foia-request-steps` | 124 | www.govinfo.gov, www.foia.gov, www.justice.gov, www.archives.gov | Statute text and the agencies' pages | 200 each at 18:57 to 19:01 |
| `maine-rcv-ballot-rules` | 125 | legislature.maine.gov, www.maine.gov | Statute text and the Secretary of State's instructions | 200 each at 18:57 and 19:01 |
| `govinfo-budget-and-tax-deadlines-2027` | 126 | www.govinfo.gov, www.ecfr.gov, www.irs.gov | Statute and regulation text; Publication 509 as a check | 200 each at 18:57 to 19:01 |
| `bjs-imprisonment-rate-by-state` | 127 | None | Frozen in round 0 (P7-003) | Not fetched |

Refused today, with no row depending on them: www.bls.gov (403) and its data API (503); www.fema.gov's pages (403); the California and Washington legislatures' code sites (403); www.ssa.gov, www.dol.gov, www.medicaid.gov, www.gao.gov, www.cdc.gov, www.ed.gov, www.ncsl.org and www.nysenate.gov (403 each). The logs are in my scratch folder (`.../phase-3/round-2/research/reach/`).

## Download list (DR-230)

No download is needed. Row 115 reads the Bureau of Labor Statistics' figures through V7; if you want the Bureau's own table, it becomes download item 3: the "Union Members" news release's Table 1 from https://www.bls.gov/news.release/union2.t01.htm, saved as HTML.

## What stays Illustrative

Row 125's office and candidates, invented and labeled. Every other row draws a primary source or V7.

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
