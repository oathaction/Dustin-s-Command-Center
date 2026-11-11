# Rounds 1 and 2 data plan

Oath & Action Edition 06, Phase 3, round 0. Research lead, November 11, 2026, for the data visualization lead's sign-off. Paths are relative to `oath-and-action-v6-brand-guide/`.

## What this plan settles

Rounds 1 and 2 build 82 of chapter 14's 127 forms: comparison, shift and swing, change over time, and tables and plain words in round 1; composition, distribution, correlation, uncertainty, and gauges and indicators in round 2 (coverage plan sections 3.1 to 3.7, 3.9 and 3.15). This plan gives every one of the 82 its reader question, dataset, publisher, period, geography, atlas domain, states and status. It then counts chapter 14's examples under Rule 01.9, with S01 to S16 included, and shows where I re-picked the coverage plan's data under DR-229.

Status words in the tables:

- **Primary**: the publisher's own file or API.
- **Primary, FRED copy**: a Bureau of Labor Statistics series as the St. Louis Fed copies it (DR-60).
- **V7**: Atlas V7, snapshot of October 15, 2026, read by script.
- **Illustrative**: invented values, labeled "Illustrative data" beside the chart.
- **Built Snn**: one of the 16 Phase 2 specimens that round 0 rebuilds in the kit.
- **Rule only**: a reference sketch or an avoid entry; it draws no dataset.

No round 1 or 2 specimen needs a labeled secondary source. Ballotpedia stays on the round 3 and 4 maps and diagrams that already use it.

## How I counted (Rule 01.9 and Rule 01.12)

1. **What counts as an example.** Every specimen that carries data: the 16 built specimens and every new core and extended specimen. Reference sketches and avoid entries draw no dataset and carry no topic, so they are left out of the count. One specimen is one example, even when it shows two forms (S06 and S13 each cover two).
2. **Domain.** Each example takes the one atlas domain its reader question belongs to, by V7's ten domain titles. A chart of the federal budget is "Taxes, wealth and economic security", which V7's own overview says covers "the federal budget". The repair log's 64 rows sit on Loops R10, R4a, R4b, B4, R1, R18 and B2, mostly electoral loops, so its specimens count as "Elections and representation".
3. **Atlas-wide.** Five new specimens and three built ones (S06, S09, S10) take their rows from every domain at once: the claims behind all 16 everyday answers, every reform's routes, every issue, V7's headline figures. They count in the total and supply no single domain. The data lead may prefer to give each a home domain; the table below shows the count either way stays under one in four.
4. **States.** An example counts toward a state when the state is its subject, is named in its title, or is lit or singled out on the chart. A chart that draws all 50 states and DC alike counts toward none, as chapter 01's log row "50 states and DC" does. Titles are written in each round, so the build's log recounts named states from the finished titles.
5. **Turnout.** Charts of who reports voting (S04, S16, and round 3's funnel) count under "Taking part, trust and shared norms", whose first subsystem V7 names "Who takes part". This follows the engineer's sidecars for the two CPS voting files. Charts of election rules and results count under "Elections and representation".
6. **Limits.** One in four of 64 is 16, so no domain may supply more than 16. One in five of 64 is 12.8, so no state may supply more than 12. For the whole chapter of about 95 examples, the limits are 23 and 19.

## Round 1: 41 forms

Family 3.1 Comparison, 3.2 Shift and swing, 3.3 Change over time, 3.15 Tables and plain words.

| # | Form | Tier | Reader question | Dataset (file in `work/build/data/`) | Publisher | Period | Geography | Domain | States | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Ranked bar | Core | Who changed the rules: voters, courts or legislatures? | Repair log (engineer's `v7-*` file) | Atlas V7 | 1965 to the November 3, 2026 ballot | United States, states and cities | Elections and representation | None in title | Built S03 |
| 2 | Column | Core | How many bills became law in each Congress? | `congress-gov-laws-by-congress` | Library of Congress, Congress.gov API | 93rd to 118th Congress (1973 to 2024); the chart shows the last ten | United States | Congress, agencies and public services | None | Primary |
| 3 | Bar with a benchmark tick | Core | What share of all household income goes to each fifth of households? | `census-acs-income-shares-by-quintile` | U.S. Census Bureau, American Community Survey 1-year, table B19082 | 2025 | United States | Taxes, wealth and economic security | None | Primary |
| 4 | Dot plot | Core | How many residents per 100,000 does each state hold in prison? | `bjs-imprisonment-rate-by-state` | Bureau of Justice Statistics, Prisoners in 2023, Table 7 | Year-end 2023, the latest edition found | 50 states | Checks on power and equal justice | Named in title only by the data | Primary |
| 5 | Dumbbell | Core | Which age groups vote, and did that change between two elections? | `census-cps-reported-voting` | U.S. Census Bureau, CPS Table A-1 | 2020 and 2024 | United States | Taking part, trust and shared norms | None | Built S04 |
| 6 | Slope chart | Core | Did younger households lose ground on owning a home? | `census-hvs-homeownership-by-age` | U.S. Census Bureau, CPS/Housing Vacancy Survey, homeownership by age of householder | 2015 and 2025 annual averages | United States | Housing, health care and getting ahead | None | Primary |
| 7 | Lollipop | Extended | Which everyday answers rest on the most claims? | `v7-claims-by-grade` (the engineer's, also S10's) | Atlas V7 | Snapshot October 15, 2026 | United States | Atlas-wide | None | V7 |
| 8 | Grouped bar | Extended | How does taking part in the labor force differ by age for men and women? | `census-acs-labor-force-by-age-sex` | U.S. Census Bureau, ACS 1-year, table B23001 | 2025 | United States | Work, pay and bargaining power | None | Primary |
| 9 | Small-multiple bars | Extended | How sure is each of the five topic hubs' evidence? | `v7-claims-by-grade` (its hub column) | Atlas V7 | Snapshot October 15, 2026 | United States | Atlas-wide | None | V7 |
| 10 | Radar chart | Avoid | | | | | | | | Rule only |
| 11 | Shift arrows | Core | Which states moved toward which party between 2020 and 2024, and how far? | `fec-presidential-results-by-state` | Federal Election Commission | 2020 and 2024 | 50 states and DC | Elections and representation | Washington, New York | Built S11 |
| 12 | Change lollipop with a size-of-shift key | Core | Where did applications to start a business rise most since 2019? | `census-bfs-business-applications-by-state` | U.S. Census Bureau, Business Formation Statistics | 2019 and 2025, annual totals | 50 states and DC | Competition and market power | Top states named by the data | Primary |
| 13 | Diverging bar | Core | Which federal agencies gained or lost civilian employees? | `opm-federal-employment-by-agency` | U.S. Office of Personnel Management, Federal Workforce Data, EHRI status files | January 2022 and August 2026 (data lead change 1) | United States | Congress, agencies and public services | None | Primary |
| 14 | Diverging bar with arrows over time | Extended | How large was the House majority's seat advantage in each Congress? | `house-history-party-divisions` | Office of the Historian and Clerk of the House, party divisions | 82nd to 119th Congress (1951 to 2026) | United States | Elections and representation | None | Primary |
| 15 | Line with event notes | Core | What happened to child poverty when the expanded child tax credit was paid, and after it lapsed? | `census-spm-child-poverty` | U.S. Census Bureau, P60-290 | 2009 to 2025 | United States | Taxes, wealth and economic security | None | Built S02 |
| 16 | Multi-line with one highlighted | Core | How far apart are homeownership rates by race, and has the gap closed? | `census-hvs-homeownership-by-race-annual` | U.S. Census Bureau, CPS/HVS | 1994 to 2025 | United States | Housing, health care and getting ahead | None | Built S05 |
| 17 | Line field with highlight | Extended | How did home prices move in every state, and where did they rise most? | `fhfa-house-price-index-by-state` | Federal Housing Finance Agency, House Price Index, purchase-only, by state | First quarter 1991 to second quarter 2026 | 50 states and DC | Housing, health care and getting ahead | One state lit, chosen by the data | Primary |
| 18 | Columns with a moving average | Core | How many jobs did the economy add each month? | `fred-payrolls-by-sector` | BLS Current Employment Statistics via FRED | January 2022 to September 2026 | United States | Work, pay and bargaining power | None | Built S14 |
| 19 | Sparkline | Core | Has the number of civic and social organizations grown or shrunk? | `census-cbp-civic-organizations` | U.S. Census Bureau, County Business Patterns, NAICS 813410 | 1998 to 2023 | United States | Taking part, trust and shared norms | None | Primary |
| 20 | Small-multiple area sparklines | Core | Which sectors added jobs since January 2022, and which lost them? | `fred-payrolls-by-sector` | BLS via FRED | January 2022 to September 2026 | United States | Work, pay and bargaining power | None | Built S13 |
| 21 | Area chart | Extended | How many people work for newspaper publishers? | `census-cbp-newspaper-publishers` | U.S. Census Bureau, County Business Patterns, newspaper publishers | 1998 to 2023 | United States | News, records and public information | None | Primary |
| 22 | Step line | Extended | How has the law changed the child tax credit's top amount per child since 2017? | `govinfo-child-tax-credit-by-law` | Public Laws 115-97, 117-2 and 119-21 on govinfo.gov; IRS for the 2026 amount | Tax years 2017 to 2026 | United States | Taxes, wealth and economic security | None | Primary |
| 23 | Line with a data gap marked | Core | What was the unemployment rate each month, and which month is missing? | `fred-unemployment-and-job-openings` | BLS Current Population Survey via FRED (UNRATE) | January 2022 to the latest month | United States | Work, pay and bargaining power | None | Primary, FRED copy; download item 1 |
| 24 | Timeline | Core | Which rule changes since 1870 decided who counts, who governs, who owns and who checks? | History events (engineer's `v7-*` file) | Atlas V7 | 1870 to 2026 | United States | Atlas-wide | None | Built S09 |
| 25 | Implementation timeline | Core | When does each part of the 2026 law on drug middlemen take effect? | `govinfo-pl-119-75-effective-dates` | Public Law 119-75 on govinfo.gov, checked against V7 issue I084 | February 3, 2026 to the last effective date | United States | Competition and market power | None | Primary |
| 26 | Indexed line | Core | Which sources of federal revenue grew fastest since fiscal 2016? | `treasury-mts-receipts-by-source` | U.S. Treasury, Monthly Treasury Statement | Fiscal 2016 to 2026 | United States | Taxes, wealth and economic security | None | Primary |
| 27 | Bubble timeline | Extended | How often has the Senate voted on ending debate, Congress by Congress? | `senate-cloture-motions-by-congress` | U.S. Senate, Senate Action on Cloture Motions | 65th Congress (1917) to the 119th to date | United States | Congress, agencies and public services | None | Primary |
| 28 | Benefit-cliff line | Extended | What does one family keep as its earnings rise and benefits phase out? | `illustrative-benefit-cliff` | Studio, on the pattern of the Urban Institute calculator and PolicyEngine | One year | Invented | Taxes, wealth and economic security | None, invented | Illustrative |
| 29 | Run chart | Reference | | | | | | | | Rule only |
| 30 | Cycle or seasonal chart | Reference | | | | | | | | Rule only |
| 31 | Streamgraph | Avoid | | | | | | | | Rule only |
| 32 | Results table with margin cells | Core | How did each state vote in 2024, and how did that compare with 2020? | `fec-presidential-results-by-state` | Federal Election Commission | 2020 and 2024 | 50 states and DC | Elections and representation | None in title | Built S15 |
| 33 | Ranked register | Core | Which groups spent the most on their own in the 2024 federal elections? | `fec-independent-expenditures-2024` | Federal Election Commission, independent expenditures | 2023 to 2024 cycle | United States | Money, lobbying and influence | None | Primary |
| 34 | Comparison matrix | Core | If a reform path were followed, which way would each outcome move? | Scenarios (engineer's `v7-*` file) | Atlas V7 | Scenarios to 2036 | United States | Atlas-wide | None | Built S06 |
| 35 | Sparkline table | Core | Which sectors added jobs since January 2022? | `fred-payrolls-by-sector` | BLS via FRED | January 2022 to September 2026 | United States | Work, pay and bargaining power | None | Built S13 (same specimen as row 20) |
| 36 | Heat table | Extended | Which routes could carry each reform, and how feasible is each? | `v7-reform-routes` | Atlas V7 | Snapshot October 15, 2026; 13 of 126 routes dated | United States | Atlas-wide | None | V7 |
| 37 | Filterable lookup table | Extended, interactive | Which issue records cover my question? | `v7-issues` | Atlas V7 | Snapshot October 15, 2026 | United States | Atlas-wide | None | V7 |
| 38 | Evidence table | Core | What does the evidence say about drug middlemen and prices? | `v7-claims-drug-prices` | Atlas V7, the 11 drug-price claims on pathway PW06 | Snapshot October 15, 2026 | United States | Competition and market power | None | V7 |
| 39 | Tracker list | Core | Where do this Congress's housing bills stand? | `congress-gov-housing-bills-119` | Library of Congress, Congress.gov API | 119th Congress to November 2026 | United States | Housing, health care and getting ahead | None | Primary |
| 40 | Plain table | Core | Do Republicans and Democrats agree on anything about Congress? | V7 headline figure 7 (engineer's `v7-*` file) and `congress-hr7008-roll-calls` | Atlas V7; Clerk of the House; U.S. Senate | 2023 survey; July 22 and September 30, 2026 votes | United States | Money, lobbying and influence | None | V7 and Primary |
| 41 | One sentence | Core | Same question, answered in one sourced sentence | V7 headline figure 7 | Atlas V7 | 2023 survey | United States | Money, lobbying and influence | None | V7 |

## Round 2: 41 forms

Family 3.4 Composition, 3.5 Distribution and density, 3.6 Correlation, 3.7 Uncertainty and estimates, 3.9 Gauges and indicators.

| # | Form | Tier | Reader question | Dataset (file in `work/build/data/`) | Publisher | Period | Geography | Domain | States | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 42 | 100 percent bar | Core | How much of each everyday answer rests on documented fact? | Claims by grade (engineer's `v7-*` file) | Atlas V7 | Snapshot October 15, 2026 | United States | Atlas-wide | None | Built S10 |
| 43 | Stacked share bar with a midline | Core | In which states do renters make up the larger share of households? | `census-acs-tenure-by-state` | U.S. Census Bureau, ACS 1-year, table B25003 | 2025 | 50 states and DC | Housing, health care and getting ahead | Named by the data | Primary |
| 44 | Waterfall | Core | How did fiscal 2026's receipts and outlays add up to the deficit? | `treasury-mts-fy2026-budget-results` | U.S. Treasury, Monthly Treasury Statement | Fiscal 2026 (October 2025 to September 2026) | United States | Taxes, wealth and economic security | None | Primary |
| 45 | Unit chart or waffle | Core | Have the rules been moving toward voters or away from them? | Repair log (engineer's `v7-*` file) | Atlas V7 | 1965 to 2026 | United States, states and cities | Elections and representation | None | Built S08 |
| 46 | Stacked column | Extended | What kinds of homes were finished each year? | `census-nrc-completions-by-structure` | U.S. Census Bureau, New Residential Construction | 2000 to 2025 | United States | Housing, health care and getting ahead | None | Primary |
| 47 | Stacked area | Extended | Who pays the nation's health care bill? | `cms-nhe-by-payer-four-groups` (folded from `cms-nhe-by-source-of-funds`, data lead change 2) | Centers for Medicare & Medicaid Services, National Health Expenditure Accounts | 1960 to 2024 | United States | Housing, health care and getting ahead | None | Primary |
| 48 | Treemap | Extended | Where did federal spending go in fiscal 2026? | `treasury-mts-outlays-by-function` | U.S. Treasury, Monthly Treasury Statement, outlays by budget function | Fiscal 2026 | United States | Taxes, wealth and economic security | None | Primary |
| 49 | Parliament chart | Extended | How are the House's seats divided by party today? | `house-history-party-divisions` | Office of the Historian and Clerk of the House | 119th Congress at its opening, and the Clerk's count on November 11, 2026 (`clerk-house-current-party-breakdown`) | United States | Elections and representation | None | Primary |
| 50 | Pie | Reference | | | | | | | | Rule only |
| 51 | Donut with a center number | Reference | | | | | | | | Rule only |
| 52 | Marimekko | Reference | | | | | | | | Rule only |
| 53 | 3D pie or bar | Avoid | | | | | | | | Rule only |
| 54 | Histogram | Core | How long have today's federal judges served? | `fjc-article-iii-judges` | Federal Judicial Center, Biographical Directory of Article III Federal Judges | Commissions to November 2026 | United States | Checks on power and equal justice | None | Primary |
| 55 | Beeswarm or strip plot | Core | How much does each state collect in taxes per resident? | `census-stc-state-tax-collections` | U.S. Census Bureau, Annual Survey of State Tax Collections, with Vintage 2025 population | Fiscal 2025 | 50 states | Taxes, wealth and economic security | Named by the data | Primary |
| 56 | Box plot | Extended | How widely do uninsured rates vary among counties in each region? | `census-sahie-county-uninsured` | U.S. Census Bureau, Small Area Health Insurance Estimates | 2024 | Every county, by Census region | Housing, health care and getting ahead | None | Primary, model estimates |
| 57 | Line histogram | Extended | Did county child poverty rates shift between 2019 and the latest year? | `census-saipe-county-child-poverty` | U.S. Census Bureau, Small Area Income and Poverty Estimates | 2019 and 2024 | Every county | Taxes, wealth and economic security | None | Primary, model estimates |
| 58 | Population pyramid | Extended | How many people are near the ages of Social Security and Medicare? | `census-pep-population-by-age-sex` | U.S. Census Bureau, Population Estimates, Vintage 2025 | July 1, 2025 | United States | Taxes, wealth and economic security | None | Primary |
| 59 | Violin | Reference | | | | | | | | Rule only |
| 60 | Ridgeline | Reference | | | | | | | | Rule only |
| 61 | Hexbin | Reference | | | | | | | | Rule only |
| 62 | Contour or density | Reference | | | | | | | | Rule only |
| 63 | Scatter plot with named points | Core | Where does rent take the biggest share of income? | `census-acs-rent-and-income-by-state` | U.S. Census Bureau, ACS 1-year, tables B25064 and B19013 | 2025 | 50 states and DC | Housing, health care and getting ahead | A few named by the data | Primary; Association label |
| 64 | Bubble chart | Extended | Same, with each state sized by its renter households | `census-acs-rent-and-income-by-state` | Same | 2025 | 50 states and DC | Housing, health care and getting ahead | A few named by the data | Primary; Association label |
| 65 | Connected scatter | Extended | How have unemployment and job openings moved together? | `fred-unemployment-and-job-openings` | BLS CPS and JOLTS via FRED (UNRATE, JTSJOL) | December 2000 to the latest month | United States | Work, pay and bargaining power | None | Primary, FRED copy; download item 1 |
| 66 | Correlogram | Reference | | | | | | | | Rule only |
| 67 | Pair plot | Reference | | | | | | | | Rule only |
| 68 | Trajectory or speed chart | Reference | | | | | | | | Rule only |
| 69 | Dual-axis line | Avoid | | | | | | | | Rule only |
| 70 | Range bar or error bar | Core | How do women's earnings compare with men's in each state, and how sure is each figure? | `census-acs-earnings-ratio-by-state` | U.S. Census Bureau, ACS 1-year, table B20017 (S2002 returned no state values) | 2025 | 50 states and DC | Work, pay and bargaining power | Named only past the margin of error | Primary |
| 71 | Confidence band on a line | Core | How has the typical household's income changed, and how sure is each year's figure? | `census-cps-median-household-income` | U.S. Census Bureau, Income in the United States: 2025, Table A-2 | 1967 to 2025 | United States | Taxes, wealth and economic security | None | Primary |
| 72 | Scenario directions | Core | If a reform path were followed, which way would each outcome move? | Scenarios (engineer's `v7-*` file) | Atlas V7 | Scenarios to 2036 | United States | Atlas-wide | None | Built S06 (same specimen as row 34) |
| 73 | Fan chart | Extended | Where do Federal Reserve officials expect unemployment to go, and how wide is the range? | `frb-fomc-projections-unemployment` | Federal Reserve Board, Summary of Economic Projections | September 2026 meeting, projections to 2029 | United States | Work, pay and bargaining power | None | Primary |
| 74 | Hypothetical outcomes | Reference | | | | | | | | Rule only |
| 75 | Big number in context | Core | Do Republicans and Democrats agree on anything about Congress? | V7 headline figure 7 | Atlas V7 | 2023 survey | United States | Money, lobbying and influence | None | Built S01 |
| 76 | Indicator row | Core | What are the atlas's headline figures? | `v7-numbers` | Atlas V7 | Snapshot October 15, 2026 | United States | Atlas-wide | None | V7 |
| 77 | Progress bar | Core | How close did the Senate come to the 60 votes it needs to end debate on H.R. 7008? | `congress-hr7008-roll-calls` | U.S. Senate, roll call vote 253, 119th Congress, second session | September 30, 2026 | United States | Congress, agencies and public services | None | Primary |
| 78 | Step tracker | Core | Where is a bill in its stages, from introduction to law? | `congress-gov-take-it-down-act-actions` | Library of Congress, Congress.gov API, S. 146, the TAKE IT DOWN Act | Introduction to signing, 2025 | United States | News, records and public information | None | Primary |
| 79 | Status chips | Core | Where do the fights over removals, spending and watchdogs stand? | `v7-issue-status-checks-on-power` | Atlas V7, statuses of issues I068, I070, I163, X05, X06 and X18 | As of October 15, 2026 | United States | Checks on power and equal justice | Illinois (Trump v. Illinois) | V7 |
| 80 | Bullet graph | Extended | How close is federal debt to the limit set in law? | `treasury-mspd-debt-subject-to-limit` | U.S. Treasury, Monthly Statement of the Public Debt, Table III | Latest month; the limit set by Public Law 119-21 | United States | Taxes, wealth and economic security | None | Primary |
| 81 | Gauge | Avoid | | | | | | | | Rule only |
| 82 | Thermometer | Avoid | | | | | | | | Rule only |

## Rule 01.9 count for chapter 14

### Rounds 0 to 2: 64 examples

S01 to S16 (16) plus the new specimens of rounds 1 (26) and 2 (22). Rows 20 and 35 are one specimen, S13, and so are rows 34 and 72, S06.

| Domain | S01 to S16 | Round 1 | Round 2 | Total | Share | Limit 16 |
|---|---|---|---|---|---|---|
| Taxes, wealth and economic security | 1 | 4 | 7 | 12 | 18.8% | Holds |
| Elections and representation | 6 | 1 | 1 | 8 | 12.5% | Holds |
| Housing, health care and getting ahead | 1 | 3 | 6 | 10 | 15.6% | Holds |
| Work, pay and bargaining power | 2 | 2 | 3 | 7 | 10.9% | Holds |
| Congress, agencies and public services | 0 | 3 | 1 | 4 | 6.3% | Holds |
| Money, lobbying and influence | 1 | 3 | 0 | 4 | 6.3% | Holds |
| Checks on power and equal justice | 0 | 1 | 2 | 3 | 4.7% | Holds |
| Competition and market power | 0 | 3 | 0 | 3 | 4.7% | Holds |
| News, records and public information | 0 | 1 | 1 | 2 | 3.1% | Holds |
| Taking part, trust and shared norms | 2 | 1 | 0 | 3 | 4.7% | Holds |
| Atlas-wide | 3 | 4 | 1 | 8 | 12.5% | No single domain |
| **All** | **16** | **26** | **22** | **64** | | |

If the data lead prefers to give each atlas-wide specimen a home domain, I rerun the count with those homes. The largest domain today holds 12, so it has room for four more before it reaches 16.

**By state.** The stretch titles name New York three times (S11, S12, S16), Florida twice (S12, S16), and Washington, New Jersey, California and Texas once each; row 79 adds Illinois once. The limit is 12 of 64. Rows 4, 12, 17, 43, 55, 63, 64 and 70 may name states their data singles out; even if each named New York, it would reach 11. The build's log recounts named states from the final titles.

**Level and region (Rule 01.12).** Sixty-one examples are national or cover every state alike. Row 79 names a federal case from Illinois. Row 28 is invented, and its log row says "invented" in its state and region fields.

### Chapter 14 as a whole: about 95 examples

Rounds 3 and 4 add about 31 data-bearing specimens. Counted with the coverage plan's data as written today, before I re-pick them a round ahead:

| Domain | Rounds 0 to 2 | Round 3 as planned | Round 4 as planned | Total | Limit 23 |
|---|---|---|---|---|---|
| Elections and representation | 8 | 4 (decision tree, district map, district tile map, small-multiple maps) | 7 (Venn, Euler, process explainer, comparison cards, step-by-step, annotated ballot, calendar) | 19 | Holds |
| Taxes, wealth and economic security | 12 | 3 (hierarchy tree, Sankey, choropleth of child poverty) | 1 (icon array) | 16 | Holds |
| Housing, health care and getting ahead | 10 | 1 (journey map) | 0 | 11 | Holds |
| Congress, agencies and public services | 4 | 3 (process diagram, org chart, arc diagram) | 1 (proportional symbols) | 8 | Holds |
| Money, lobbying and influence | 4 | 2 (roll-call grid of H.R. 7008, committee network) | 0 | 6 | Holds |
| Atlas-wide | 8 | 3 (who-decides, comparison grid, adjacency matrix) | 1 (by-the-numbers) | 12 | No single domain |
| Other five domains | 18 | 4 (funnel and county choropleth of turnout, both taking part; locator; dot density) | 1 (social card of a core specimen) | 23 | Each holds; the largest, work and pay, reaches 8 |

Elections and representation would reach 19 of about 95, four under the limit, and taxes and budgets 16. Round 4's seven election picks sit close together, so with the round 3 data plan I will propose moving the calendar to federal budget and tax deadlines and the step-by-step to applying for a benefit, which leaves 17. The forms built for elections (district map, district tile map, the ranked ballot, the Venn and Euler of state election rules, comparison cards on primaries) keep their election data, as DR-229 sets.

## Re-picks from the coverage plan (DR-229)

The coverage plan named election data for 12 round 1 and 2 forms that are not built for elections, and it reused the data of a built specimen for seven more. I re-picked each, keeping the form and tier.

| # | Form | Coverage plan data | New data | Why |
|---|---|---|---|---|
| 2 | Column | Census child poverty by year | Laws enacted by each Congress | S02 already charts child poverty; Congress and agencies had no example |
| 3 | Bar with a benchmark tick | CPS voters by age against eligible voters | Household income shares by quintile against each fifth's 20 percent | Election data on a general form; the 20 percent tick is a share against a population share |
| 4 | Dot plot | FEC presidential margin by state | Imprisonment rate by state | Election data on a general form; checks on power and equal justice had no example |
| 6 | Slope chart | Homeownership by race, 2019 and 2025 | Homeownership by age of householder, 2015 and 2025 | S05 already draws homeownership by race |
| 8 | Grouped bar | Turnout by age, presidential and midterm years | Labor force participation by age and sex | S04 already draws turnout by age |
| 12 | Change lollipop | FEC top shifts | Business applications by state, 2019 to 2025 | S11 and S12 already draw the FEC shifts |
| 13 | Diverging bar | Jobs change by sector since 2022 | Federal civilian employees by agency | S13 already states the sector finding |
| 17 | Line field | State turnout since 1980 | House prices by state since 1991 | Election data on a general form |
| 19 | Sparkline | Payrolls by industry | Civic and social organizations | S13 already draws payrolls by industry; taking part had no example |
| 21 | Area chart | Federal employment level | Newspaper publishers' employees | Row 13 now covers federal employment; news and records had no example |
| 25 | Implementation timeline | One rule's parts from V7's logs | Public Law 119-75's effective dates, the law V7 issue I084 names | The statute gives each part's date; V7 gives the pointer |
| 26 | Indexed line | Payrolls by industry since 2022 | Federal receipts by source since fiscal 2016 | S13 already draws payrolls by industry |
| 27 | Bubble timeline | Repair log entries by year | Senate cloture votes by Congress | S03 and S08 already draw the repair log |
| 33 | Ranked register | Repair log, claims per question | Independent spending by group, 2024 | Row 7 draws claims per question; money and influence needed a register |
| 43 | Stacked share bar | FEC vote shares by state | Renter and owner households by state | Election data on a general two-way form; S11 and S15 already use the FEC file |
| 46 | Stacked column | Repair log by year and direction | Homes completed by type of building | A third repair log chart |
| 47 | Stacked area | Federal spending by function | Health spending by who pays | Row 48 draws federal spending by function |
| 54 | Histogram | House margins | Years of service of federal judges | Election data on a general form |
| 55 | Beeswarm | FEC presidential margin by state | State tax collections per resident | Election data on a general form |
| 56 | Box plot | House margins by region | County uninsured rates by region | Election data on a general form |
| 57 | Line histogram | Margins in 2020 and 2024 | County child poverty rates, 2019 and 2024 | Election data on a general form |
| 63, 64 | Scatter and bubble chart | Turnout against registration deadline | Rent against income by state | Election data on a correlation form |
| 70 | Range bar | CPS turnout with margins | Women's to men's earnings ratio with margins | S16 and S04 already use the CPS voting tables |
| 71 | Confidence band | Census poverty with margins | Median household income with margins | S02 already charts poverty |
| 73 | Fan chart | CBO projections | Federal Reserve projections of unemployment | cbo.gov refuses automated readers; the Fed's projections carry published error ranges and need no download |
| 77 | Progress bar | A cloture vote against 60 | The Senate's September 30, 2026 cloture vote on H.R. 7008 | The same form, now with the Senate record D2-104 waited for |
| 78 | Step tracker | A bill's stages | The TAKE IT DOWN Act's stages to law | A finished route shows every stage; news and records had a second example |
| 79 | Status chips | Repair log status | V7's dated statuses of six checks-on-power issues | A third repair log chart |

Kept as the coverage plan set them: rows 7, 9, 14, 22, 23, 28, 36, 37, 40, 41, 44, 48, 49, 58, 65, 76 and 80, with row 38 narrowed to one pathway and row 39 to one subject.

## Datasets to fetch and freeze

Each goes into `work/build/data/` under the engineer's schema, with a sidecar and a row in the research ledger's Part 7. V7 files come from `work/extract/atlas-v7-data.json` by script. The fetch log in my notes records each one's state.

| Dataset | Rows it serves | Host | How |
|---|---|---|---|
| `congress-gov-laws-by-congress` | 2 | api.congress.gov | API, key injected |
| `census-acs-income-shares-by-quintile` | 3 | api.census.gov | API, key from the environment |
| `bjs-imprisonment-rate-by-state` | 4 | bjs.ojp.gov | File |
| `census-hvs-homeownership-by-age` | 6 | www.census.gov | File |
| `census-acs-labor-force-by-age-sex` | 8 | api.census.gov | API |
| `census-bfs-business-applications-by-state` | 12 | api.census.gov or www.census.gov | API or file |
| `opm-federal-employment-by-agency` | 13 | data.opm.gov | API, parquet files summed by agency |
| `house-history-party-divisions` | 14, 49 | history.house.gov | Page table |
| `fhfa-house-price-index-by-state` | 17 | www.fhfa.gov | File |
| `census-cbp-civic-organizations` | 19 | api.census.gov | API |
| `census-cbp-newspaper-publishers` | 21 | api.census.gov | API |
| `govinfo-child-tax-credit-by-law` | 22 | www.govinfo.gov, www.irs.gov | Statute text |
| `fred-unemployment-and-job-openings` | 23, 65 | fred.stlouisfed.org | Download item 1 |
| `govinfo-pl-119-75-effective-dates` | 25 | www.govinfo.gov | Statute text |
| `treasury-mts-receipts-by-source` | 26 | api.fiscaldata.treasury.gov | API |
| `senate-cloture-motions-by-congress` | 27 | www.senate.gov | Page table |
| `illustrative-benefit-cliff` | 28 | None | Studio values, labeled |
| `fec-independent-expenditures-2024` | 33 | api.open.fec.gov | API, key injected |
| `congress-gov-housing-bills-119` | 39 | api.congress.gov | API |
| `congress-hr7008-roll-calls` | 40, 77, and S01 | clerk.house.gov, www.senate.gov | Roll call XML |
| `census-acs-tenure-by-state` | 43 | api.census.gov | API |
| `treasury-mts-fy2026-budget-results` | 44 | api.fiscaldata.treasury.gov | API |
| `census-nrc-completions-by-structure` | 46 | www.census.gov | File |
| `cms-nhe-by-source-of-funds` | 47 | www.cms.gov | File |
| `treasury-mts-outlays-by-function` | 48 | api.fiscaldata.treasury.gov | API |
| `fjc-article-iii-judges` | 54 | www.fjc.gov | File |
| `census-stc-state-tax-collections` | 55 | api.census.gov | API |
| `census-sahie-county-uninsured` | 56 | api.census.gov | API |
| `census-saipe-county-child-poverty` | 57 | api.census.gov | API |
| `census-pep-population-by-age-sex` | 58 | www2.census.gov | File |
| `census-acs-rent-and-income-by-state` | 63, 64 | api.census.gov | API |
| `census-acs-earnings-ratio-by-state` | 70 | api.census.gov | API |
| `census-cps-median-household-income` | 71 | www2.census.gov | File |
| `frb-fomc-projections-unemployment` | 73 | www.federalreserve.gov | Page tables |
| `congress-gov-take-it-down-act-actions` | 78 | api.congress.gov | API |
| `treasury-mspd-debt-subject-to-limit` | 80 | api.fiscaldata.treasury.gov | API |
| `v7-claims-by-grade` (the engineer's), `v7-reform-routes`, `v7-issues`, `v7-claims-drug-prices`, `v7-numbers`, `v7-issue-status-checks-on-power` | 7, 9, 36, 37, 38, 76, 79 | Repository | `work/build/scripts/phase-3/research_v7_extract.py` |

## What stays Illustrative

Only row 28, the benefit-cliff line, whose family and benefit rules are invented and carry "Illustrative data" beside the chart. Every other round 1 and 2 specimen has a primary source or V7.

## For the data lead's sign-off

Please check four things, under Rule 01.9 and DR-229:

1. The domain I gave each specimen, above all the eight atlas-wide ones and row 58, where the pyramid answers a Social Security and Medicare question.
2. The re-picks, form by form, against what each form teaches.
3. The two new data sources on forms that touch elections: row 14 and row 49 both draw the House's party balance, the only election data left on new round 1 and 2 forms.
4. The plan for rounds 3 and 4 to take three forms off election data.

Reply in your notes with "signed off" or the changes, and I will re-pick before fetching any dataset you change.

## Data lead sign-off

**Signed off with five changes**, November 11, 2026, by the data visualization and systems lead, under Rule 01.9 and DR-229. A script recounted this plan's tables: 82 forms, 26 new data-bearing specimens in round 1 and 22 in round 2, and with S01 to S16 the same 64 examples and the same domain totals as the count above. The largest domain, taxes, wealth and economic security, holds 12 of 64 against a limit of 16, and no state comes near its limit of 12. I also read every form against the palette proposal (`work/handoffs/phase-3/20261111_Palette-Proposal.json`) and DR-234.

**Signed off as written**

1. Every domain the plan gives, with the eight atlas-wide specimens counted apart and row 58 under taxes, wealth and economic security. Each atlas-wide specimen draws its rows from across V7's domains or hubs. If a finished one turns out to draw most of its rows from one domain, its spec takes that domain and the count reruns.
2. The re-picks. Each keeps its form and tier and teaches what the form exists to teach. They spread chapter 14 across all ten domains, which keeps every share further under one in four than DR-229's four named areas alone would.
3. Rows 14 and 49 on the House's party balance. Both forms exist to show how seats divide, so they keep election data, as DR-229 allows.
4. Moving round 4's calendar and step-by-step off election data. Please send round 3's plan with its recount.

**Changes before the makers draw**

1. **Row 13, federal civilian employees by agency.** A window from September 2024 starts four months before the January 2025 inauguration, so readers on either side will take the chart as one administration's record. Set the window by the data's reach instead: from January 2022 to the latest month, the window S13 and S14 use, if OPM's files go back that far, with the reason printed (H09, DR-124). If the files start in September 2024, the measure line says the files start there.
2. **Rows 26, 47 and 48 pass four groups (DR-234).** The Monthly Treasury Statement splits receipts into seven sources, the health spending accounts name more than four payers, and outlays run to about 20 budget functions. Row 26 draws small multiples, or the fastest-growing source in ink against the rest in gray. Row 47 folds to four groups: private health insurance, Medicare, Medicaid and all other payers, the last as the hatched Stone group, with the folded payers listed in the note; the folded table is its own derived file under the engineer's contract C1. Row 48 draws every function in one light fill with its label and the function its title names in ink, and folds tiles too small to label into "All other functions", listed in the table.
3. **Rows 14 and 49 draw parties in one neutral ink**, with each party's name on its marks, and position and words carry the side (DR-48, DR-58). Neither takes pair B, the categorical inks or red.
4. **Row 77 names H.R. 7008 with both provisions at first mention** (DR-98), since its title cites the bill.
5. **Rows 6 and 23 carry the October 2025 gap.** The Census Bureau collected no CPS data that month (the footnote in `census-hvs-homeownership-by-race-annual`'s sidecar), so row 23 marks it as the missing month and row 6's 2025 average says it leaves October out.

**Palette notes for the makers** (no change to the plan)

- Rows 8, 46 and 56 have two to four groups and take the categorical set in its order, Charcoal, Prussian, Verdigris, then hatched Stone, each with a direct label.
- Rows 12 and 13 carry direction by position. A fill, where one helps, is diverging pair B with the value printed.
- Row 44's waterfall steps take the subject ink and the light fill by direction, with every value printed and no red.
- Row 73's fan takes the Stone magnitude steps 1 and 2 for its ranges, with the median line in ink; it needs no new color.
- No form in the plan needs a second sequential scale, so the palette proposal adds no Prussian sequential set.

## Research lead, after the sign-off

Applied on November 11, 2026, before the makers draw:

- **Change 1, row 13.** OPM's monthly files reach back to 2011, so `opm-federal-employment-by-agency` now compares January 31, 2022 with August 31, 2026, the jobs charts' window, with the reason in its sidecar. The August 2024 file is no longer used. The window ends in August because OPM flagged September 2026 as incomplete for some Department of War components.
- **Change 2, row 47.** `cms-nhe-by-payer-four-groups` is a derived file under contract C1: private health insurance, Medicare, Medicaid, and all other payers (out of pocket, CHIP, Defense, Veterans Affairs, other third parties, public health and investment), with the folded payers named in its sidecar. Rows 26 and 48 draw from their published files; the maker chooses small multiples or one source in ink for row 26, and folds row 48's small tiles in the table equivalent.
- **Changes 3 to 5** are drawing and wording choices for the makers. Row 6's sidecar already says the 2025 average leaves out October 2025; row 23's file waits on download item 1, and its sidecar will say October 2025 is missing once the file is read.

**Status of every dataset.** All frozen in `work/build/data/` with sidecars and ledger rows (research ledger Part 7), including `fred-unemployment-and-job-openings` (rows 23 and 65, from Dustin's download of November 11, with October 2025 missing as row 23 needs), except `illustrative-benefit-cliff` (row 28), whose invented values the round 1 maker writes under contract C1 with `kind: "illustrative"`.
