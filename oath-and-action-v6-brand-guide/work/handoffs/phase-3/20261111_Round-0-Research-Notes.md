# Round 0 research notes

Oath & Action Edition 06, Phase 3, round 0. Research lead (`oa-research-lead`), November 11, 2026. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

**The data plan** (`work/handoffs/phase-3/20261111_Rounds-1-2-Data-Plan.md`) covers all 82 round 1 and 2 forms and was ready at 21:45 UTC. The data visualization lead signed it off with five changes, and I applied the two that touch data (row 13's window from January 2022; row 47 folded to four payer groups). Counted with S01 to S16, chapter 14's 64 examples so far hold Rule 01.9: the largest domain, taxes, wealth and economic security, supplies 12 of 64 (limit 16); elections and representation 8; no state is named more than three times (limit 12). For the whole chapter of about 95 examples, elections would reach 19 (limit 23) with the coverage plan's round 3 and 4 data, and I propose two more re-picks with round 3's plan.

**Data fetched and frozen.** 44 new tables in `work/build/data/`, each with a sidecar under the engineer's contract C1, fetched from 21:32 to 22:16 UTC: 36 public tables and 5 V7 tables for the plan, and 3 that answer the Explainer maker's requests. The engineer's check (`python3 -I work/build/scripts/phase-3/data_round0_build.py --check`) reads all 60 tables in the folder with 0 faults. Dustin's download (item 1) arrived at 22:27 UTC and is frozen as `fred-unemployment-and-job-openings` (ledger P7-013); its October 2025 unemployment rate is blank, as expected. The folder now holds 61 tables, 0 faults. One planned file is not frozen: row 28's Illustrative benefit-cliff values, which the round 1 maker writes. Each has a row in the research ledger's new Part 7 with its URL and date checked.

**The two ballot measures in Reform R-01's V7 status.** Massachusetts Question 3 was rejected: No 1,566,336 (61.04 percent), Yes 999,746 (38.96 percent), 2,383 of 2,384 precincts, unofficial, from NBC Boston's results page (labeled secondary; the Secretary of the Commonwealth had posted no 2026 results), with the Associated Press calling the race at 1:37 a.m. on November 4. Alaska's Ballot Measure 2 trails in the Division of Elections' unofficial count of November 10: Yes 110,298 (47.43 percent), No 122,266 (52.57 percent); mailed ballots arrive until November 13 and overseas ballots until November 18, and the target date to certify is November 25. Neither is certified. Both are in the ledger (P7-036) and in the V7.1 item below.

**Also written:** `work/research/20261111_Policy-Workflow-Sources.md` (FS, SS, BI and LOC, stage by stage, with official sources and dates; four states' veto rules from their constitutions) and `work/research/20261111_Data-And-Interaction-Lessons.md` (15 rules from Our World in Data, LOOPY and En-ROADS, each from a page read in full today).

## Answers to the Explainer maker (R1 to R4)

- **R1, S02's source line. Answered; nothing to change.** The engineer's copy of `census-spm-child-poverty.meta.json` already carries the line, under `source_line_variants.source_line_both_measures`, word for word as you asked.
- **R2, S16's 2024-only line. Answered; nothing to change.** `census-cps-2024-turnout-by-state.meta.json` carries it under `source_line_variants.source_line_2024_only`, the line Phase 2 printed.
- **R3, S01's bill text. Answered with a new table.** `govinfo-hr7008-engrossed-sections` holds H.R. 7008's sections as the House passed them, read today on govinfo.gov (`BILLS-119hr7008eh`). Section 2, "Restrictions on covered investments", bars a Member, spouse or dependent child from buying a covered investment and requires public notice 7 to 14 days before a sale; section 3, "Requiring voters to provide photo identification", requires a valid photo ID to receive a ballot in person in a federal election, with a provisional ballot otherwise. Folding it into S01's own line needs the engineer (ENG-1).
- **D2-104 can now be lifted.** Both chambers' records are read (`congress-hr7008-roll-calls`): House roll call 280, July 22, 2026, on passage, Republicans 218 to 0, Democrats 13 to 198 with 1 not voting, the independent 1 to 0; Senate vote 253, September 30, 2026, on cloture on the motion to proceed (60 needed, rejected), Republicans 53 to 0, Democrats 0 to 45, independents 0 to 2. The Senate vote was on ending debate on taking the bill up, not on the bill. Whether S01 now shows the split is for the data lead and the main session.
- **R4, margins for S04 and S05. Answered with two new tables.**
  - S04, `census-cps-voting-age-gap-moe`: Table A-1 prints no margins, so I used the Census Bureau's own method, the generalized variance parameters in the November 2020 and 2024 Source and Accuracy statements (b = 5,411 and 6,643) on Table 1's citizen bases. The gap between citizens 65 and over and citizens 18 to 24 was 23.1 points in 2020 (margin 1.4) and 27.0 in 2024 (margin 1.5); it grew 3.9 points with a margin of about 2.0, so **the change passes the margin of error**.
  - S05, `census-hvs-homeownership-gap-moe`: the 2003 annual statistics publish standard errors (Table B-7) and the 2025 statistics publish margins. The non-Hispanic White and Black gap was 27.3 points in 2003 and 29.6 in 2025; it widened 2.3 points with a margin of about 0.7, so **the change passes**. The non-Hispanic White and Hispanic gap narrowed 2.9 points, also past its margin.

## Fix pass

From `work/handoffs/phase-3/20261111_Round-0-Fix-Brief-Part-1.md`: every item the statistics and civic education review gives the research lead, D3-88, D3-89, the editor's request for the Brandeis row, and the Bureau of Labor Statistics' figure for question 1. Each data fix is made in my freeze scripts and the files rebuilt from them; the engineer's contract check reads 61 tables with 0 faults after the last change.

**Question 1, the payroll interval (statistics M4). Confirmed from the Bureau's own page.** The Employment Situation Technical Note on bls.gov (the October 2026 release, "Last Modified Date: November 06, 2026") says that at about a 90-percent level of confidence the interval for the monthly change in total nonfarm employment "is on the order of plus or minus 122,000". The reviewer's ±136,000 came from memory of an older note. I read the page through the session's web-fetch tool, since bls.gov refuses this container's own reader; the tool quotes in short fragments, and the note's own example (a 50,000 gain spans −72,000 to +172,000) matches the figure. Tested against `fred-payrolls-monthly-change`: of the seven drops, only October 2025 (−140,000) and February 2026 (−156,000) pass ±122,000. So the reviewer's sentence holds as written: "Only the October 2025 and February 2026 drops pass the survey's margin of error." Ledger row P7-042. One caveat for Dustin: the note gives the interval for the current release, and the Bureau's figure has differed in past years, so the sentence should cite this note and its date.

| Item | What I did | Where |
|---|---|---|
| D3-88, statistics M5 (rows 63, 64) | Rebuilt `census-acs-rent-and-income-by-state` from the Census Bureau's own measure, B25071, median gross rent as a percentage of household income, with margins (United States 30.9 percent, margin 0.1), beside median gross rent (B25064) and renter households' median income (B25119_003). The studio ratio is gone; the reader question now asks whether rents run higher where renters earn more and where rent takes the largest share of renters' income. Domain and states unchanged, so the Rule 01.9 count stands (largest domain 12 of 64; New York 3 of 64). For the data lead's sign-off | `freeze_census_b.py`; the data file and sidecar; plan rows 63 and 64; ledger P7-030 |
| D3-89, statistics M6 (row 40) | Row 40's plain table shows the May 2023 survey alone. The votes stay in row 77 and S01, whose words must name both provisions (DR-98), print each vote's question, and say where a reader sees it that the survey asked about a ban alone and came three years before the bill | Plan row 40 and its fix-pass section |
| Statistics S13 (row 77) | The row and `congress-hr7008-roll-calls`' printed line now say the Senate voted on ending debate on taking up the bill | `freeze_other_a.py`; plan row 77 |
| Statistics S14 (row 13) | Added `size_1000_plus` to `opm-federal-employment-by-agency`: the chart draws absolute change for the 37 agencies with 1,000 or more employees on either date (99.4 percent of January 2022's employees); the other 92 stay in the table. A note says each bar nets every change between January 31, 2022 and August 31, 2026 | `freeze_other_b.py`; sidecar notes; plan row 13 |
| Statistics S15 (rows 47, 48) | `cms-nhe-by-payer-four-groups` adds each group's percent of the year's total, and its fourth group is "all other sources of funds", since investment and public health are not payers. `treasury-mts-outlays-by-function` adds a `treemap_fy2026` source line and note: the positive functions sum to $7,566.3 billion against net outlays of $7,395.8 billion, so tiles are shares of the positive functions | `freeze_other_b.py`, `freeze_treasury.py`; plan rows 47 and 48 |
| Statistics S16 (rows 4, 56, 57) | The BJS sidecar says to set states beside the STATE row (318 in 2023), not the US row (360), which adds federal prisoners; the SAHIE and SAIPE sidecars say each county counts once, whatever its population | `freeze_other_b.py`, `freeze_census_b.py`; plan rows 4, 56 and 57 |
| Statistics M3 (S02's sidecar) | Request ENG-5 below: the engineer's copy holds the printed line and the variant | Request |
| Statistics S17 (Ballotpedia label) | Request ENG-6 below | Request |
| Statistics S18 (a United States row for the turnout map) | Request ENG-7 below, with the national rows read today from the Bureau's Table 4a files, whose SHA-256 prefixes match Phase 2's | Request |
| Engineer's R5 ("Atlas V7" in reader text) | `research_v7_extract.py` now names the atlas "Oath & Action’s systems atlas, Who Do They Answer To?" as publisher and in every printed line, as `data_round0_build.py` does; the five tables are rebuilt. ENG-1's requested line takes the same words. A scan of every sidecar's printed line and variants finds "V7" only in the engineer's own kept variants | `work/build/scripts/phase-3/research_v7_extract.py`; `v7-reform-routes`, `v7-issues`, `v7-claims-drug-prices`, `v7-numbers`, `v7-issue-status-checks-on-power` |
| Statistics S10, the editor's request | Ledger row P7-041: New State Ice Co. v. Liebmann, 285 U.S. 262, at 311, read in U.S. Reports through the Library of Congress's scan. U.S. Reports prints "a single courageous State" and "the Nation"; the Legal Information Institute's copy lower-cases both. For the editor: quote U.S. Reports with the page | Research ledger, Part 7 |

New requests to the engineer (his script writes these sidecars):

- **ENG-5. S02's source lines (statistics M3).** In `census-spm-child-poverty.meta.json`, end `printed_source_line` and `source_line_variants.source_line_both_measures` with "Figures for 2019 to 2024 include the Bureau's August 2026 correction to the poverty thresholds, and 2024 also takes new population weights; they differ by up to 0.4 points from the earlier release." in place of the sentence that begins "Figures for 2019 to 2024 include the Bureau's August 2026 revision". Replace `source_line_first_published` with: "Source: U.S. Census Bureau, Poverty in the United States: 2024 (P60-287), Table B-2, Supplemental Poverty Measure, children under 18, 2020, 2021 and 2024, United States. Retrieved November 6, 2026. Rates as published before the Bureau's August 2026 correction; P60-277 (September 13, 2022) printed the same 2020 and 2021 rates." These follow the sidecar's own `v7_comparison` record.
- **ENG-6. Ballotpedia's label (statistics S17).** In `ballotpedia-rcv-prohibitions-by-state.meta.json`, set `printed_source_line` to "Source: Ballotpedia, a secondary source, Ranked-choice voting (RCV), state laws prohibiting RCV, as of November 2026, 50 states and DC. Retrieved November 6, 2026. Ohio's and Tennessee's bans cover some elections; the other 17 cover all." (Rule 13.6's wording for a secondary source).
- **ENG-7. National rows for the turnout file (statistics S18).** Add to `census-cps-2024-turnout-by-state.csv` the rows `US,United States,2020,231593,66.8,0.4` and `US,United States,2024,236138,65.3,0.5`, read today from the United States rows of Table 4a (`vote04a_2024.xlsx`, SHA-256 prefix 068e47d3c7fc9701; `table04a.xlsx` for 2020, 8afd077c560de260), and say in the sidecar that code US is the national figure, drawn set apart (DR-64).

Routine calls:

D3-xxx | Rows 63 and 64 draw the Census Bureau's B25071 rent share with its margin, rent against renter households' income, and drop the studio's ratio | D3-88; the Bureau's measure answers the question, and the old ratio ran 6.9 to 12.6 points low in every state
D3-xxx | Row 40 shows the 2023 survey alone | D3-89 and DR-98: the survey asked about a ban in general, and the bill also carries a photo ID requirement
D3-xxx | Row 13's chart draws absolute change for agencies with 1,000 or more employees on either date and leaves the rest to the table | Percent change would be led by bodies of a few people; the floor keeps 99.4 percent of employees
D3-xxx | Row 47 draws shares of each year's total, and its fourth group is "all other sources of funds" | Nominal dollars over 64 years hide the mix behind inflation, and investment and public health are not payers
D3-xxx | The payroll interval is cited as ±122,000 from the October 2026 Technical Note, read through the web-fetch tool, with its date | It is the Bureau's current figure; bls.gov refuses this container's reader, and the note's own example checks against it

Tested:
- The engineer's contract check after every rebuild: 61 tables, 0 faults.
- B25071's United States figure, 30.9 percent, against the API's own row; every state row read from the same request.
- The seven payroll drops against ±122,000, by script on the frozen file.
- The treemap sum of positive functions from Treasury's unrounded figures: $7,566.3 billion.
- The agency size floor by script: 37 agencies, 99.4 percent of January 2022's employees.
- The Brandeis passage in the Library of Congress's scan of U.S. Reports, page 311 (text extracted from the PDF), and in the Legal Information Institute's copy.
- The national Table 4a rows, from the Bureau's files fetched today, with SHA-256 prefixes equal to Phase 2's.

Not tested:
- The Technical Note's full paragraph in one piece; the tool returns fragments. Dustin can save the page if the main session wants the full text on file.
- Any chart or plate; I changed no plate, so no guide rebuild was needed for my files.
- The engineer's ENG-5 to ENG-7 changes, which are his to make.

## Fix pass 2

From `work/handoffs/phase-3/20261111_Round-0-Fix-Brief-Part-2.md`: D3-98 first, then D3-95, then the statistics report's part 2 items for the research lead (P2-M2's Missouri facts, P2-S2, P2-S3 and P2-S7). The contract check reads 61 tables with 0 faults after the last change.

**D3-98: the three November 3, 2026 measures, as the record stands on November 11, 2026.** Re-read at about 23:40 UTC; none had changed since the first reading. Sent to the Explainer maker by message, in these words:

1. **Massachusetts Question 3** (repair log RL64), one all-candidate primary with the top two advancing: rejected, 1,566,336 no (61.04 percent) to 999,746 yes (38.96 percent), 2,383 of 2,384 precincts; unofficial, not certified; the Associated Press called it on November 4. Source: NBC Boston, Massachusetts ballot question results, report of November 9, 2026, 7:26 p.m., a secondary source (the Secretary of the Commonwealth had posted no 2026 results). Retrieved November 11, 2026. Ledger P7-036b.
2. **Alaska Ballot Measure 2** (RL62), repeal of the top-four primary and ranked-choice general election: trailing, 110,298 yes (47.43 percent) to 122,266 no (52.57 percent); unofficial count of November 10, 2026; mailed ballots due by November 13 and overseas ballots by November 18; certification targeted for November 25. Source: State of Alaska, Division of Elections, 2026 General Election, Election Summary Report, unofficial results, November 10, 2026. Retrieved November 11, 2026. Not decided. Ledger P7-036a.
3. **Missouri Proposition A** (RL63), the referendum on House Bill 1's 2025 congressional map (a no vote keeps the 2022 districts): rejected in the unofficial statewide count, 1,273,815 no to 785,969 yes (61.84 percent no, computed by us); not certified. Source: St. Charles County, Missouri, "Voters Turn Out for 2026 Midterm Election in St. Charles County", November 4, 2026, unofficial statewide returns. Retrieved November 11, 2026. The Secretary of State's results site refused our reader. These are the figures chapter 01's Rule 01.11 plate already prints. Ledger P7-036c.

**D3-95: values stored below the publisher's precision.** I read every rounding in my freeze scripts and changed each at its source:

| File | Before | Now |
|---|---|---|
| `treasury-mts-receipts-by-source`, `treasury-mts-outlays-by-function`, `treasury-mts-fy2026-budget-results` | billions, rounded to a tenth (the treemap's positive sum came to 7,566.4 from rounded parts against 7,566.3 from the published dollars) | dollars to the cent, exactly as Treasury publishes them; columns renamed `receipts_dollars`, `outlays_dollars`, `amount_dollars` |
| `treasury-mspd-debt-subject-to-limit` | billions, rounded to a tenth | millions, exactly as published; columns end `_millions` |
| `census-acs-labor-force-by-age-sex` (participation), `census-acs-tenure-by-state` (shares), `census-acs-earnings-ratio-by-state` (ratio and margin), `census-stc-state-tax-collections` (per resident), `fjc-article-iii-judges` (years), `opm-federal-employment-by-agency` (percent change), `cms-nhe-by-payer-four-groups` (shares), `frb-fomc-projections-unemployment` (bands), `census-cps-voting-age-gap-moe` and `census-hvs-homeownership-gap-moe` (errors, gaps) | computed values rounded to one or two decimals | the same values stored to four decimals, so a chart rounds once |

Values copied from a publisher (Census tables, FHFA, CBP, the FEC's dollars, the Senate's counts) were already stored as published. The two files the statistics report names, `fec-presidential-shift-by-state` and `fred-payrolls-by-sector-change`, are the engineer's derived files (request ENG-8).

**P2-S3, S04's margins by age group.** `census-cps-voting-age-gap-moe` now holds each age group's own change from 2020 to 2024 with its margin, by the same Census method (bases from Table 1): 18 to 24 fell 3.7 points (margin 1.7) and 25 to 44 fell 2.4 (margin 1.0), both past their margins; 45 to 64 fell 1.0 against a margin of 0.96, too close to call because the published rates are rounded to a tenth; 65 and over rose 0.2 (margin 1.1), inside it. For the Explainer maker: label each change by these, in place of the two-point rule.

**P2-S2, margins for S01 and S13.**
- S01's survey: the Program for Public Consultation's own page says the 2,625-voter sample, fielded May 19 to 30, 2023, has "a margin of error of +/- 1.9%". It gives no margin for each party's voters and states no confidence level (ledger P7-043; request ENG-9).
- S13: the Bureau of Labor Statistics publishes sampling errors for employment levels and for one-, three- and twelve-month changes, and none for a change as long as S13's 56 months; for levels it gives relative standard errors of 0.1 percent (total nonfarm), 0.3 (professional and business services; health care and social assistance) and 0.9 (information), and it says "estimates of variance are not available for government sectors". Read through the web-fetch tool, first 100,000 characters of the page (ledger P7-044; request ENG-9). A sentence for S13's note: "The Bureau publishes no sampling error for a change over this many months; for employment levels it gives errors of 0.1 to 0.9 percent in these industries, and none for government."

**P2-S7, S06's 2036.** V7's scenarios name no horizon in their introduction or fields; 2036 appears in one scenario's own words (iv-d, "flat through 2036"), and scenario ii is named "State and local track by 2030". The year comes from V7's outcome indicators: `outcomes.indicator_note` says "Each indicator gives its latest reading and two thresholds for 2036", and each indicator carries a `baseline_2026`. For the Explainer maker: either cite that ("directions for the outcome families the atlas measures against thresholds for 2036, from a 2026 baseline") or drop the year, as the reviewer offers.

**The Explainer maker's R7, R8 and the 2036 source (its "Fix pass 2").** All three are answered above:
- **R7, S04's margin by age group: done in a file I own.** `census-cps-voting-age-gap-moe`, rows `change_2020_to_2024_18_to_24`, `_25_to_44`, `_45_to_64` and `_65_and_over`, each with its 90 percent margin (`moe_90`) and the published rates behind it.
- **R8, S13's sampling errors: answered, with a sidecar request.** The Bureau publishes no error for a change over 56 months; its level errors and the government gap are above, the sentence for S13's note is above, and ENG-9 asks the engineer to put the same words in `fred-payrolls-by-sector.meta.json` (ledger P7-044).
- **S06's 2036: answered; nothing to add to a data file.** V7's `outcomes.indicator_note` sets the 2036 thresholds and the indicators' `baseline_2026` sets the base year; the scenarios themselves name no horizon. The words cite that or drop the year.

New requests to the engineer:

- **ENG-8. Derived files stored from rounded figures (D3-95, statistics P2-M1).** Please compute `fec-presidential-shift-by-state`'s margins and shifts from the vote counts in `fec-presidential-results-by-state` (margin = (rep_votes − dem_votes) / total_votes × 100), unrounded, and `fred-payrolls-by-sector-change`'s percent change from the levels, unrounded. The reviewer's four cells (North Dakota 2024, 36.446; North Carolina 2020, 1.348; Mississippi 2020, 16.545; professional and business services, 1.348 percent) then print right.
- **ENG-9. Margins in two sidecars (P2-S2).** In `v7-stock-trading-ban.meta.json`, add a note: "The Program for Public Consultation gives the full sample's margin of error as plus or minus 1.9 percent (https://publicconsultation.org/united-states/stock-trading-by-members-of-congress/, read November 11, 2026); it gives none for each party's voters and states no confidence level." In `fred-payrolls-by-sector.meta.json`, add: "The Bureau of Labor Statistics publishes sampling errors for levels and for one-, three- and twelve-month changes (All Employees Standard Error Tables, https://www.bls.gov/web/empsit/cesvarae.htm, read November 11, 2026), none for longer changes, and none for government sectors."

Routine calls:

D3-xxx | Every computed value in my data files is stored to four decimals, and every published value exactly as published | D3-95: a chart rounds once, from the stored value
D3-xxx | Treasury and debt files store dollars and millions as published, with columns renamed for their unit | Billions to a tenth made a treemap's sum differ from Treasury's by a tenth; no maker has drawn from these files yet
D3-xxx | S03 and S08's note gives Missouri's count from St. Charles County's report of the unofficial statewide returns | The Secretary of State's results site refuses this container's reader, and the county is an election authority reporting the state's returns; chapter 01 already prints the same figures

Tested:
- The contract check after every rebuild: 61 tables, 0 faults.
- Alaska's report re-read at 23:40 UTC (unchanged, November 10, 6:45 p.m. report); NBC Boston's page data re-read (unchanged, November 9 report); the St. Charles County release read in full for Proposition A's statewide figures.
- The treemap's positive sum from published dollars: $7,566.3 billion; the stored deficit equals Table 1's to the cent.
- Each age group's margin by script with the Bureau's formula and Table 1's bases.
- The survey page's margin read on the page itself.

Not tested:
- Missouri's certified count or its certification date; the state's results site refused, and the date in chapter 01's plate was not checked here.
- The Bureau's change errors for twelve months by industry (Tables 3 and 4 lie past the part of the page the tool read).
- Whether any spec already names a renamed Treasury column; none of rows 26, 44, 48 or 80 is drawn yet.

## Routine calls

D3-xxx | Rule 01.9 counts every specimen that carries data (the 16 built and every new core and extended form) and leaves out reference sketches and avoid entries | They draw no dataset and carry no topic
D3-xxx | Specimens whose rows span every domain (claims across the 16 everyday answers, all reforms, all issues, V7's headline figures, scenarios, history) count as atlas-wide, in the total and in no single domain | Contract C1 allows `domain: "all"`; the data lead signed it off
D3-xxx | A specimen counts toward a state when the state is its subject, is named in its title or is lit on the chart; a chart of all states alike counts toward none | Chapter 01's rotation log treats "50 states and DC" this way
D3-xxx | Charts of who reports voting (S04, S16, round 3's funnel) count under taking part, trust and shared norms; charts of election rules and results under elections and representation | V7's first D10 subsystem is "Who takes part", and the engineer's sidecars code the CPS voting files D10
D3-xxx | Twenty-eight round 1 and 2 forms take new data: twelve move off election data and sixteen off data a built specimen already draws | DR-229, and one dataset per lesson
D3-xxx | Row 73's fan chart uses the Federal Reserve's September 2026 projections of unemployment with its published historical errors in place of CBO projections | cbo.gov refuses automated readers, and the Fed's error table gives the bands with no download
D3-xxx | Row 77's progress bar uses the Senate's September 30, 2026 cloture vote on H.R. 7008 (53 of the 60 needed) | It is the Senate record D2-104 waited for, and it teaches the 60-vote rule with a real vote
D3-xxx | Row 70 computes women's to men's earnings ratios from ACS Table B20017 with the Census Bureau's ratio approximation for the margin | The data API returned empty state values for Table S2002 today; the computed U.S. ratio, 82.0, matches S2002's published 82.0
D3-xxx | Row 13 compares federal civilian employees on January 31, 2022 and August 31, 2026 | The data lead's change 1 (the jobs charts' window, no split at an inauguration); OPM flagged September 2026 as incomplete for some Department of War components
D3-xxx | Row 47 draws `cms-nhe-by-payer-four-groups`, a derived file that folds every payer but private insurance, Medicare and Medicaid into "all other" | The data lead's change 2 under DR-234
D3-xxx | Row 39's tracker list holds eight housing bills of the 119th Congress that moved past referral, two of them now law | Congress.gov's API has no policy-area filter, so I read the bill lists of Senate Banking and House Financial Services and kept the housing bills that moved
D3-xxx | Row 79's status chips draw V7's dated statuses of six checks-on-power issues, and Illinois counts once for Trump v. Illinois | The statuses name rulings and cases, which is what status chips are for
D3-xxx | The Alaska Division of Elections site sends an incomplete certificate chain; I added only the missing GlobalSign intermediate its certificate names to a copy of the proxy's CA bundle, and verification stayed on | The chain then verified to GlobalSign Root R46 in the trusted store; nothing was fetched with verification off
D3-xxx | My V7 tables come from my own script, `work/build/scripts/phase-3/research_v7_extract.py`, which imports nothing of the engineer's and writes only `v7-reform-routes`, `v7-issues`, `v7-claims-drug-prices`, `v7-numbers` and `v7-issue-status-checks-on-power` | Contract C1 allows it; rows 7 and 9 reuse the engineer's `v7-claims-by-grade`
D3-xxx | The five-download list holds one file | Every other round 1 and 2 dataset answered from its publisher today; fewer is better (DR-230)

## Requests

To the engineer (sidecars his script writes):

- **ENG-1. S01's source line with the bill text.** Please add to `v7-stock-trading-ban.meta.json` a `source_line_variants.with_bill_text`: "Source: Program for Public Consultation, University of Maryland, survey of 2,625 registered voters, fielded May 19 to 30, 2023, United States; U.S. Government Publishing Office, H.R. 7008, Stop Insider Trading Act, text as passed by the House, sections 2 and 3; U.S. House of Representatives, Roll Call 280, July 22, 2026; U.S. Senate, Vote 253, September 30, 2026; as recorded in Oath & Action’s systems atlas, Who Do They Answer To?, snapshot of October 15, 2026. Bill text retrieved November 11, 2026. The survey predates both votes by three years." In `qualification`, replace "The vote totals carry no party split until both chambers' records can be read (D2-104)." with "Both chambers' party splits are in congress-hr7008-roll-calls, read November 11, 2026."
- **ENG-2. S04's margins.** Please add to `census-cps-reported-voting.meta.json` the note: "Margins for the 2020 and 2024 age-gap figures are in census-cps-voting-age-gap-moe: the gap between citizens 65 and over and citizens 18 to 24 grew 3.9 points with a margin of about 2.0 points."
- **ENG-3. S05's margins.** Please add to `census-hvs-homeownership-by-race-annual.meta.json` the note: "Margins for 2003 and the 2003 to 2025 gaps are in census-hvs-homeownership-gap-moe: the non-Hispanic White and Black gap widened 2.3 points with a margin of about 0.7 points." and change its `unconfirmed` item on earlier margins to name that file.
- **ENG-4. Ledger rows for the Phase 2 tables.** Their sidecars read `ledger_row: "none yet"`. Part 7 of the research ledger gives them P7-101 to P7-110: ballotpedia-rcv-prohibitions-by-state P7-101, census-cps-2024-turnout-by-state P7-102, census-cps-reported-voting P7-103, census-hvs-homeownership-by-race-annual P7-104, census-spm-child-poverty P7-105, fec-presidential-results-by-state P7-106, fec-presidential-shift-by-state P7-107, fred-payrolls-by-sector P7-108, fred-payrolls-by-sector-change P7-109, fred-payrolls-monthly-change P7-110.

To the data visualization lead: the plan's changes are applied (the plan's last section). Round 3's plan, with its recount and the two proposed re-picks, follows a round ahead.

To the main session: download item 1 below, and the V7.1 item below.

## The five-download list (DR-230)

One file is enough for rounds 1 and 2. Everything else answered from its publisher today.

| # | Page to open | File to save | What it is | Specimens it serves |
|---|---|---|---|---|
| 1 | https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE,JTSJOL (opening it in a browser downloads the file) | `fredgraph.csv`, as the browser names it; please attach it to the chat as is | Two monthly series from the St. Louis Fed's FRED copies of Bureau of Labor Statistics data: the unemployment rate (UNRATE, Current Population Survey) and job openings (JTSJOL, Job Openings and Labor Turnover Survey), from each series' start to the latest month | Row 23, line with a data gap marked (the unemployment rate, with October 2025 missing), and row 65, connected scatter (unemployment against job openings) |

Why a download: FRED closed the connection on the one try the brief allowed (21:20 UTC, an HTTP/2 stream reset), and bls.gov refuses automated readers. **Done.** Dustin attached the file at 22:27 UTC (SHA-256 10c1d1ed61e8b494195f087331ad53aa7651ba3ceca05597599a7953c1a58532, 946 rows). It is frozen as `fred-unemployment-and-job-openings` with its sidecar and ledger row P7-013. October 2025's unemployment rate is blank in the file, and the frozen row says so in its note column; job openings for that month (7,170 thousand) are present. Row 23's source line runs January 2022 to October 2026; a variant for row 65 runs December 2000 to September 2026.

## Proposed V7.1 issue-list item

**V7.1-R01. Reform R-01's ballot measures were decided on November 3, 2026.** V7 (snapshot of October 15, 2026) describes Massachusetts Question 3 and Alaska Ballot Measure 2 as pending. As the record stands on November 11, 2026, Massachusetts voters rejected Question 3 (No 61.04 percent, Yes 38.96 percent, unofficial, from NBC Boston's results page with the Associated Press's call; labeled secondary), and Alaska's Ballot Measure 2 trails, Yes 47.43 percent to No 52.57 percent, in the Division of Elections' unofficial count of November 10, with certification targeted for November 25. Fields that name the measures, found by script: `reforms.R-01` (summary, who_decides, costs, status, routes BI note); `reforms.R-08.status` and `reforms.R-47.status`; `repairLog` rows RL62 (Alaska, "pending") and RL64 (Massachusetts, "pending") and the rule or source text of RL14, RL17, RL21 and RL26; `issues` I025, I026, X01 and X11 (status or notes); claims CL1724 to CL1730; pathway PW15's sub-issues, rule-changers and first response; `numbers[0]`'s caption; one history chip; and sources W039, W040, K1700 to K1703, K1900, K1923 and Q562. Proposed: the atlas editor updates these after Alaska certifies, citing the Division of Elections and the Secretary of the Commonwealth's certified results. The guide keeps printing V7's values with "as of October 15, 2026" and never edits V7. Repair log row RL63 (Missouri, Proposition A, also November 3) is outside this item and was not researched. For the data lead: S03 and S08 count RL62 to RL64 as pending, which stays true of the snapshot they print.

## Tested

- The engineer's contract check on the data folder: 61 tables, 0 faults, after the FRED file was frozen.
- Dustin's FRED file: its SHA-256 matches the coordinator's, it has 946 data rows of three columns, and the 2025-10 unemployment cell is empty (read by script with `-I`).
- Every new table was fetched from its publisher today, each download in its own folder under `/tmp/claude-0/-home-user-Dustin-s-Command-Center/31ab6fca-308a-5402-b22c-b6bfd31a97ee/scratchpad/phase-3/round-0/research/dl/`, with a fetch log of 1,826 requests (time, address with keys removed, status, bytes, SHA-256 prefix) in `.../research/logs/fetch-log.tsv`, and host checks in `.../research/reach.tsv` and `reach2.tsv`.
- The Census key appears in no file in the repository, my scripts or my logs (a fixed-string search for its value found 0 files).
- Cross-checks run by script: state tax totals summed from the published flat file equal the data API's aggregate for every state; NHE payer lines sum to the published total in 2024; the U.S. earnings ratio computed from B20017 (82.0) equals Table S2002's published figure; the Senate vote's party counts sum to 53 and 47 as recorded; the FY2026 Treasury rows match Table 1's receipts, outlays and deficit; BJS's footnote b marks the six states named in the sidecar.
- The plan's domain totals, recounted from its own table after each edit, and by the data lead's script.
- The ballot figures: Alaska's from the Division's own PDF report (text extracted and read); Massachusetts's from the numbers embedded in NBC Boston's page source, not only from a summary.
- No em dash in any file I wrote (searched).

## Not tested

- Any chart drawn from these tables; the makers build them in rounds 1 and 2.
- Whether each sidecar's printed source line reads well at chart size; the editor and the chart check judge that.
- The Illustrative benefit-cliff values, which do not exist yet.
- Whether FRED's UNRATE and JTSJOL are the seasonally adjusted series was not read on their FRED pages; the sidecar lists it as unconfirmed.
- Certified results for either ballot measure; none exist yet.
- Pages that refused or sent no text: congress.gov, ncsl.org, csg.org, leginfo.legislature.ca.gov, the Texas statutes site, library.municode.com, boston.gov's council page, the Massachusetts Secretary of the Commonwealth's Question 3 page and Alaska's ballot measures page.
- The Boston and Minneapolis ordinance rules in the workflow file rest on search snippets from the cities' own domains.
- OPM's monthly files between January 2022 and August 2026 were not read; row 13 draws two points.
- Rule 01.9's state count for rows whose titles are not yet written; the build's log recounts named states from the finished titles.

## Change log

Created:
- `work/handoffs/phase-3/20261111_Rounds-1-2-Data-Plan.md` (the data lead appended its sign-off; I added the last section after it)
- `work/handoffs/phase-3/20261111_Round-0-Research-Notes.md` (this file)
- `work/research/20261111_Policy-Workflow-Sources.md`
- `work/research/20261111_Data-And-Interaction-Lessons.md`
- `work/build/scripts/phase-3/research_v7_extract.py`
- In `work/build/data/`, each with its `.meta.json`: bjs-imprisonment-rate-by-state, census-acs-earnings-ratio-by-state, census-acs-income-shares-by-quintile, census-acs-labor-force-by-age-sex, census-acs-rent-and-income-by-state, census-acs-tenure-by-state, census-bfs-business-applications-by-state, census-cbp-civic-organizations, census-cbp-newspaper-publishers, census-cps-median-household-income, census-cps-voting-age-gap-moe, census-hvs-homeownership-by-age, census-hvs-homeownership-gap-moe, census-nrc-completions-by-structure, census-pep-population-by-age-sex, census-sahie-county-uninsured, census-saipe-county-child-poverty, census-stc-state-tax-collections, clerk-house-current-party-breakdown, cms-nhe-by-payer-four-groups, cms-nhe-by-source-of-funds, congress-gov-housing-bills-119, congress-gov-laws-by-congress, congress-gov-take-it-down-act-actions, congress-hr7008-roll-calls, fec-independent-expenditures-2024, fhfa-house-price-index-by-state, fjc-article-iii-judges, frb-fomc-projections-unemployment, govinfo-child-tax-credit-by-law, govinfo-hr7008-engrossed-sections, govinfo-pl-119-75-effective-dates, house-history-party-divisions, opm-federal-employment-by-agency, senate-cloture-motions-by-congress, treasury-mspd-debt-subject-to-limit, treasury-mts-fy2026-budget-results, treasury-mts-outlays-by-function, treasury-mts-receipts-by-source, fred-unemployment-and-job-openings (CSV), and v7-claims-drug-prices, v7-issue-status-checks-on-power, v7-issues, v7-numbers, v7-reform-routes (JSON)

Modified:
- `work/research/20261021_Research-Ledger.md`: Part 7, Phase 3 data, inserted before "Claims I could not verify", and a line in its change log

Scratch only, outside the repository: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/31ab6fca-308a-5402-b22c-b6bfd31a97ee/scratchpad/phase-3/round-0/research/` (downloads, freeze scripts, logs, a Python virtual environment for reading OPM's parquet files).
