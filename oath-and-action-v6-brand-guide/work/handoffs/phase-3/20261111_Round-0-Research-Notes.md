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

- **ENG-1. S01's source line with the bill text.** Please add to `v7-stock-trading-ban.meta.json` a `source_line_variants.with_bill_text`: "Source: Program for Public Consultation, University of Maryland, survey of 2,625 registered voters, fielded May 19 to 30, 2023, United States; U.S. Government Publishing Office, H.R. 7008, Stop Insider Trading Act, text as passed by the House, sections 2 and 3; U.S. House of Representatives, Roll Call 280, July 22, 2026; U.S. Senate, Vote 253, September 30, 2026; as recorded in Oath & Action, Who Do They Answer To? Systems Atlas V7, snapshot of October 15, 2026. Bill text retrieved November 11, 2026. The survey predates both votes by three years." In `qualification`, replace "The vote totals carry no party split until both chambers' records can be read (D2-104)." with "Both chambers' party splits are in congress-hr7008-roll-calls, read November 11, 2026."
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
