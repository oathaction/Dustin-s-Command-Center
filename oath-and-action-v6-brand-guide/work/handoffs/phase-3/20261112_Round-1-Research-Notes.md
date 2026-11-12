# Round 1 research notes

Oath & Action Edition 06, Phase 3, round 1. Research lead (`oa-research-lead`), November 12, 2026, under `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Kept current as the work goes, since the container can restart.

## Summary

**Round 3's data plan** (`work/handoffs/phase-3/20261112_Round-3-Data-Plan.md`) was ready for sign-off at 04:05 UTC. It covers all 32 round 3 forms (rules 14.93 to 14.124): 20 new data-bearing specimens, 3 built maps that become entries (S07, S12, S16) and 9 rule-only sketches. The data lead signed it off with twelve changes and no dataset replaced; all twelve are applied in the plan's rows and listed in its section "Research lead, after the sign-off". Counted for chapter 14 as a whole (about 95 examples with round 4 as planned), the largest domain, elections and representation, holds 16 against a limit of 23, and no state passes 3 against 19.

**Fetched and frozen** (04:13 to 04:40 UTC): 25 new tables in `work/build/data/`, each with a sidecar under contract C1 and a research ledger row (Part 7, P7-201 to P7-217), plus 5 Atlas V7 tables from my extract script. The engineer's check reads 88 tables with 0 faults. Three sources differ from the plan's first text, each because the planned file could not carry what the sign-off asked: the House results come from the Clerk's compilation (the FEC's 2024 congressional file lists candidates without votes); the Sankey reads the FEC's current campaigns file (the API's candidate totals lack the receipt and loan lines change 7 needs); the bill search reads the Library of Congress's bulk bill status files (every title of every bill, change 6). **Waiting:** the map geometry, downloaded and staged as GeoJSON, frozen once the engineer sets ENG-10's shape; row 113, on download item 2.

Findings the makers and the main session need:
- **Row 83.** In April 2023 to March 2024, 76,734,167 renewals came due; 22,914,537 ended, 15,966,431 of them (69.7 percent) for a procedural reason; 48,967,998 kept coverage; 4,851,632 were still pending. V7 I062 cites KFF's "more than 25 million" over the whole unwinding; CMS's file ends with March 2024 renewals. The difference goes to Dustin as an open question (request below), not into a chart.
- **Row 92.** H.R. 5371 (Public Law 119-37): the Senate passed it as amended 60 to 40 (vote 618, November 10, 2025); the House agreed to the Senate's amendment 222 to 209 (roll call 285, November 12, 2025). Totals match each record.
- **Row 94.** The rule picks the Harris Victory Fund (C00744946; $528.7 million to the campaign) and the Trump National Committee JFC (C00873893; $246.8 million). Both principal campaign committees have since changed name and type (now Fight for the People PAC and Never Surrender, Inc.); the sidecar says so.
- **Row 96.** 18 bills name pharmacy benefit managers in a title: 10 House and 8 Senate. The House is drawn: 33 pairs of House bills share a backer.
- **Rows 109 and 111.** The Clerk's results give 220 Republican and 215 Democratic seats (Minnesota's DFL counted as Democratic). Seat kinds: 390 Republican and Democratic, 22 with one candidate on the ballot, 9 other pairings, 6 one-party contests in California, 6 Louisiana open primaries, Alaska's ranked-choice first round and Maine's 2nd district final round. New York's and Connecticut's fusion lines are summed to each candidate.
- **Row 87.** Ballotpedia, re-read after the election, still lists the same 19 states; no November 3, 2026 measure added or removed a ban (P7-218).
- **Row 100.** Cash at the start plus receipts, $2,608,168,369; spending, refunds, repayments, transfers and cash at the end, $2,606,635,211; the $1,533,158 remainder (0.06 percent) is printed in the sidecar.

**The seven remaining routes** are in `work/research/20261111_Policy-Workflow-Sources.md`, section "Round 1: the seven remaining routes" (done 04:15 UTC): FA, FR, ENF, CRT, AV, IC and CIV, each stage with the official source that sets it, a quote from the text read today, the address and the date checked. The Senate's vote records settle the 2013 and 2017 cloture precedents that round 0 left open, and 21 Congressional Review Act disapprovals became law in the 119th Congress through November 12, 2026, out of 140 laws.

## Routine calls

- D3-xxx | Round 3's rows continue the rounds 1 and 2 plan's numbering, 83 to 114, in chapter 14's rule order | One numbering across the data plans lets a spec, a sidecar and a ledger row cite the same row
- D3-xxx | Round 3's funnel draws Medicaid and CHIP renewal outcomes in place of the CPS voting tables | S04 and S16 already draw the CPS voting tables, rows 3 and 70 moved off them for the same reason, and V7 names the drop-out this funnel shows (I062)
- D3-xxx | Each round 3 domain follows V7's own issue for the topic where V7 has one, named in the row | The count then rests on the atlas's filing, which the data lead and a reader can check
- D3-xxx | The roll-call grid draws H.R. 5371, the November 2025 continuing appropriations act, with each chamber's recorded vote | H.R. 7008 already serves four specimens, and its Senate vote was on taking the bill up; H.R. 5371 has a recorded passage vote in each chamber
- D3-xxx | The network diagram draws both 2024 presidential joint fundraising committees the same way | Both parties use the mechanism, so Rule 01.11 asks for a case from each in the same form
- D3-xxx | Map geometry comes from the Census Bureau's 2024 cartographic boundary and Gazetteer files, frozen unprojected and unsimplified, with the kit projecting and simplifying at build (ENG-10) | Free to use with credit to the Census Bureau, as the files' own metadata says; projection is a drawing choice, so the data stays neutral and the page carries only drawn paths
- D3-xxx | The district tile map's layout is the studio's own, from the Census Bureau's district centers | Published tile layouts are third-party work, study only under Master Brief section 2
- D3-xxx | The executive action route shows revocation with one order from each of the last two transitions, Executive Order 13992 (2021) and Executive Order 14148 (2025), each counted from its Federal Register text | The mechanism belongs to every administration, so the source shows a case from each in the same form (Rule 01.11)
- D3-xxx | Quotes that hold an em dash in the source are split into quoted fragments rather than repunctuated | The guide sets no em dash, and a quote keeps the source's words and punctuation
- D3-xxx | Rows 109 and 111 draw the Clerk of the House's 2024 election statistics in place of an FEC file | The FEC's 2024 congressional file lists candidates without votes; the Clerk compiles official results from the states
- D3-xxx | The 2024 House margin is the winner's votes less the runner-up's over all votes for the office, with a labeled seat kind for one-candidate seats, one-party contests, other pairings, Alaska's first round, Maine's final round and Louisiana's open primary | One rule reads the same in every kind of seat (data lead change 9); blank, void and exhausted ballots are not votes for a candidate
- D3-xxx | New York's and Connecticut's fusion lines are summed to the candidate above them | The Clerk prints each party line separately, and a candidate's vote is the sum of the lines
- D3-xxx | Row 100 reads the FEC's current campaigns file (webl24) for every House candidate, primary losers included, and nets transfers between a candidate's own committees | The API's candidate totals lack the receipt and loan lines change 7 needs, and the FEC's own file description says to subtract those transfers
- D3-xxx | Row 96 searches every title in the Library of Congress's bill status bulk files for "pharmacy benefit manager" and the word PBM, and draws the House's 10 bills | Change 6 asks for every title; one bulk file per chamber reads them all, and the House has more matches
- D3-xxx | Row 94's committees are each nominee's joint fundraising committee that sent the most to the nominee's principal campaign committee, from the FEC's aggregates by recipient | One rule read the same way for both (change 8): the Harris Victory Fund and the Trump National Committee JFC
- D3-xxx | Row 83's funnel sums April 2023 to March 2024 and nests due, decided, not ended for a procedural reason, and kept coverage, with pending renewals set apart | Twelve months avoid counting a person due in March of both years, and change 11 asks for stages that nest from one base
- D3-xxx | Row 112 leaves out Puerto Rico and the island areas and drops the noise column, which the API returned as 0 for every county | The chart covers the 50 states and DC, and a column that says nothing is noise
- D3-xxx | V7 connection signs are stored as words (positive, negative, none) | The data check reads a bare "-" as a missing value, and words keep V7's sign without a symbol a reader could mistake

## Requests

- **ENG-10, to the engineer: map geometry in the data folder.** Raw files are in `.../round-1/research/dl/geometry/` (fetch log there), and GeoJSON is staged in `.../round-1/research/geometry-staged/`: `census-cb-2024-states.geojson` (52 features, 20m, 330 KB), `census-cb-2024-counties.geojson` (3,222, 20m, 2.3 MB), `census-cb-2024-counties-california-5m.geojson` (58, 5m, for the locator, 225 KB) and `census-cb-2024-cd119.geojson` (441, 5m, 4.2 MB). Each keeps the shapefile's attributes and ring order (outer rings clockwise, holes counterclockwise, as d3 expects), longitude and latitude to six decimals, unsimplified. The files' metadata asks for credit to the Census Bureau and says the 20m files are for display at 1:20,000,000 or smaller, so a one-state map (Michigan) uses the 5m districts. Tell me the shape you want (`.geojson` in the data folder, which today's check refuses, a subfolder, TopoJSON, or projected paths as CSV), and I freeze them with sidecars and ledger row P7-219 that hour.
- **ENG-11, to the engineer: the Ballotpedia bans sidecar.** Please add to `ballotpedia-rcv-prohibitions-by-state.meta.json` a note: "Re-read November 12, 2026, after the November 3, 2026 election: the same 19 states. The only 2026 measures on electoral systems, Alaska Ballot Measure 2 (trailing, uncertified) and Massachusetts Question 3 (rejected), add or remove no ban (research ledger P7-218)." The decision tree prints that as-of date (change 12).
- **To the main session: an open question for Dustin (change 11).** V7 issue I062 says "more than 25 million people were disenrolled, 69% of them for procedural reasons" (KFF, observed September 2024). CMS's own national file counts 22,914,537 ended for renewals due April 2023 to March 2024, 69.7 percent for a procedural reason, and ends with March 2024. The periods differ, and the chart prints CMS's figures and period. Proposed for the open questions ledger and the V7.1 list: whether V7 should cite CMS's own counts with their period beside KFF's.
- **To the main session: download item 2.** The Department of Labor's state minimum wage history page, https://www.dol.gov/agencies/whd/state/minimum-wage/history, saved as HTML or PDF and attached as is (dol.gov refused this container, HTTP 403, 03:58 UTC). It serves row 113 only; I freeze it the hour it arrives, with panels 2010, 2015, 2020 and 2026 (change 10).
- **To Maker B or whoever draws rows 109 and 111:** the national result to set apart is in the district file's sidecar notes (220 Republican, 215 Democratic seats).

## Tested

- Reachability of every host the plan relies on, logged in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f15cd04b-21be-5dde-a467-804e951756a2/scratchpad/phase-3/round-1/research/reach/` (`reach-1.tsv` to `reach-3.tsv`): which answered, which refused (dol.gov, ssa.gov, medicaid.gov, usace.army.mil, fcc.gov, uscis.gov, FEC's `cms-content` path) and which sent a bot check (federalregister.gov and ecfr.gov's pages).
- Every round 3 file fetched today from its publisher, each in its own folder under `.../round-1/research/dl/` with a `fetch-log.tsv` (time, address with keys removed, status, bytes, SHA-256 prefix); freeze scripts in `.../round-1/research/scripts/`.
- The engineer's contract check after each freeze: 88 tables, 0 faults at the end.
- Script cross-checks: the CMS national count of renewals due equals the sum of the states' counts in every month (asserted), and renewed equals ex parte plus form and ended equals ineligible plus procedural in every month; the funnel's stages nest (asserted); H.R. 5371's member rows sum to each record's printed totals (60 to 40; 222 to 209); the courts tree has 91 district courts of the states, DC and Puerto Rico, matching the count each state's section of 28 U.S.C. creates, plus 3 territorial courts, 179 circuit judgeships and 673 district judgeships with the four shared seats; the House results parse 435 districts, every state's seat count matching, with 220 and 215 seats; Michigan's 13 rows match the Clerk's printed figures, read by eye (all 13 against the candidate lines, nine also against the state's recapitulation); the V7 region matrix sums to 118 connections (70 positive, 41 negative, 7 with no sign) in 44 filled cells, as the data lead counted; the Sankey's two sides differ by 0.06 percent, printed.
- The Census key in no file in the repository, my scripts, downloads or logs (fixed-string search, 0 files), and my fetch helper stops if a response ever echoes it.
- The Ballotpedia ban list re-read today: 19 states, the same as the frozen file.
- The research ledger, the plan and the workflow sources file: no em dash or U+2011.
- Route sources: 53 requests between 04:05 and 04:10 UTC, 47 answered with the page or record asked for, each quoted from text extracted by script; the revocation counts (Executive Order 13992, 6 orders; 14148, 67 orders and 11 memoranda) and the 21 disapproval laws counted by script.

## Not tested

- Any chart drawn from these tables; the makers build round 3 later.
- The geometry files in the kit, and their weight on the page (ENG-10 and the data lead's request DL-E1).
- Alaska's and Maine's own round-by-round ranked-choice reports; the file carries the Clerk's printed round.
- Why the CBP county counts sum to about 7.7 million fewer paid employees than the national row, and what the API's noise code 0 means.
- Whether any law after the U.S. Code's 2024 edition changed a judgeship count.
- Whether a Tennessee city can run its own elections outside its county election commission; the decision tree follows the data lead's reading that Tennessee takes the ban branch.
- The route sources' pages that refused or were not found (ftc.gov's enforcement overview, justice.gov's filings page, rules.senate.gov, the appellate rules file, the Impoundment Control Act sections at the address tried); each is in the workflow file's round 1 claims.
- The Senate's committee steps for nominations and any precedent after 2017.

## Change log

Created:
- `work/handoffs/phase-3/20261112_Round-3-Data-Plan.md` (the data lead appended its sign-off; I applied its changes and added the last section)
- `work/handoffs/phase-3/20261112_Round-1-Research-Notes.md` (this file)
- In `work/build/data/`, each with its `.meta.json`: cms-medicaid-chip-renewal-outcomes, cms-medicaid-chip-renewal-funnel, congress-hr5371-roll-calls-by-member, clerk-house-committees-119, congress-gov-pbm-bills-119, congress-gov-pbm-bill-backers-119, congress-gov-pbm-bill-shared-backers-119, uscode-federal-courts-circuits-districts, govinfo-federal-rulemaking-steps, govinfo-snap-application-steps, usgov-route-requirements, census-acs-broadband-by-state, census-acs5-county-median-household-income, census-cbp-county-employment, census-gazetteer-2024-places, census-gazetteer-2024-cd119, clerk-house-results-2024-by-candidate, clerk-house-results-2024-by-district, fec-jfc-transfers-2024, fec-house-campaigns-2024-by-candidate, fec-house-campaigns-2024-money-in-out (CSV); v7-rcv-local-routes, v7-pathway-electric-decision-makers, v7-routes, v7-links-with-regions, v7-region-connection-matrix (JSON)

Modified:
- `work/research/20261111_Policy-Workflow-Sources.md`: the title, one sentence of the opening, item 5 of round 0's unverified claims, and the new section "Round 1: the seven remaining routes" with its own list of claims not verified
- `work/research/20261021_Research-Ledger.md`: Part 7's "Round 3 datasets" (P7-201 to P7-220), claims 10 to 15 of Part 7's unverified list, a settled note on claim 6, and a change log line
- `work/build/scripts/phase-3/research_v7_extract.py`: five round 3 tables and their docstring lines; the five round 0 tables it writes are unchanged

Scratch only, outside the repository: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f15cd04b-21be-5dde-a467-804e951756a2/scratchpad/phase-3/round-1/research/` (downloads, fetch logs, freeze scripts, staged GeoJSON).

## Fix pass

From the data lead's DL-R1 to DL-R3 and maker B's R-B1, R-B4, R-B5, R-B8 and R-B10. All the files are mine from round 0; none belongs to the engineer's scripts (only the board builder and the editor's rules builder read two of them). The round 0 freeze scripts lived in that session's scratch folder, which is gone, so `.../round-1/research/scripts/fix_pass_round1.py` edits the frozen files in place, idempotently, and records each change. The data check reads 89 tables with 0 faults after it.

- **DL-R1, S31.** `fred-unemployment-and-job-openings.meta.json` gains `source_line_variants.unemployment_rate_only`: "Source: U.S. Bureau of Labor Statistics, Current Population Survey, unemployment rate, seasonally adjusted, January 2022 to October 2026, United States, via FRED, Federal Reserve Bank of St. Louis. Retrieved November 11, 2026. No rate was published for October 2025."
- **DL-R2 and R-B8, S33.** `treasury-mts-receipts-by-source.meta.json` gains `source_line_variants.fiscal_2016_to_2026`, the printed line with "fiscal 2016 to 2026".
- **DL-R3, S30.** `govinfo-child-tax-credit-by-law.meta.json` describes `max_credit_per_child` as "maximum credit per qualifying child 6 or older (every qualifying child outside 2021)"; `max_credit_young_child` already holds 2021's $3,600.
- **R-B1, S29.** Both County Business Patterns sidecars gain `breaks_in_series`, from the Bureau's methodology page read today: CBP has been tabulated on NAICS since 1998, on SIC before.
- **R-B4, S24.** New derived file `census-bfs-business-applications-change-by-state` (52 rows: the nation, 50 states and DC; 2019, 2025, change and percent change to four decimals).
- **R-B5, S25.** `opm-federal-employment-by-agency.csv` gains an `agency` column in title case beside OPM's own `department`.
- **R-B10.** The research ledger's Part 7 records `illustrative-benefit-cliff` as P7-221, with a "Fix pass, round 1" note for the rest.

- D3-xxx | The round 0 data files are fixed in place by a recorded script, since their freeze scripts were lost with that session's scratch folder | Each change stays traceable, and a rerun gives the same files
- D3-xxx | S31's unemployment-only source line keeps "seasonally adjusted", as the file's printed line does, with the sidecar's unconfirmed note on it unchanged | UNRATE is FRED's seasonally adjusted series ID; FRED's series page was not reachable today to confirm it
- D3-xxx | OPM's agency names get a title-case column beside the publisher's capitals, with the official capitals kept for "From People Who Are" and acronyms (U.S., CHIP), one stray space in "SE VERELY" and doubled spaces removed | A reader's table needs readable names; the publisher's own column stays as published
- D3-xxx | Business applications' change by state is a derived file stored to four decimals, the round 0 rule (D3-95) | The maker asked for unrounded values; four decimals let a chart round once, as every computed value in my files does
- D3-xxx | Maker B's invented benefit-cliff file takes a Part 7 row (P7-221) | The ledger then accounts for every file in the data folder

Tested: the data check, 89 tables, 0 faults; the 52 change rows recomputed by script from the frozen counts; the 130 agency names read in full; the CBP methodology passage read on census.gov today (fetch log in `.../round-1/research/dl/cbp-docs/`).
Not tested: FRED's UNRATE page (unreachable today); any chart redrawn with these lines (the makers' work).

## Fix pass 2

From maker A's A1, A2, A6 and A7. A6 first, since it blocks S40. Scripts: `.../round-1/research/scripts/fix_pass2_housing.py` and `fix_pass2_more.py`; A7 is in `work/build/scripts/phase-3/research_v7_extract.py`. The data check reads 90 tables with 0 faults.

- **A6, S40.** Congress.gov's API answers the committee steps but not the hearing question in full. It records a hearing on a bill only as a "Hearings By" committee activity, and none of the eight bills has one; a hearing on the subject or on a draft with no bill number would not show. So I did not set step numbers. `congress-gov-housing-bills-119` gains facts maker A sets the Rule 11.1 steps from: `hearing_recorded` (false for all eight), `committee_record` (every activity with its date), `committee_vote` (H.R. 6644, December 17, 2025, 50 to 1; H.R. 225, June 10, 2025, 50 to 1; H.R. 1078, December 17, 2025, 29 to 22; H.R. 1640, June 30, 2026, 51 to 0; H.R. 5889, September 16, 2026, 47 to 2), `first_chamber_passed`, `second_chamber_passed` and `became_law_date`. H.R. 224 and H.R. 965 passed the House under suspension with no committee action; S. 2651 was reported by Senate Banking as an original measure; H.R. 224 was discharged from Senate Banking.
- **A1, S17.** `congress-gov-laws-by-congress` gains the variant `last_ten` in maker A's words.
- **A2, S20.** `census-hvs-homeownership-by-age` gains the variant `two_years` in maker A's words; the new file `census-hvs-homeownership-by-age-moe` (P7-222) gives each summary age group's 2015 and 2025 margins from HVS Table B-5 and the change's margin. The under-35 rise of 2.0 points passes its margin of about 0.8; so do all householders (1.5) and 35 to 44 (2.3); 45 to 54, 55 to 64 and 65 and over do not.
- **A7, S39.** `v7-claims-drug-prices` gains `source_words`: each source as V7's sources record names it, publisher and title, joined by "; " (CL1358: "Federal Trade Commission, FTC second interim PBM staff report release").

- D3-xxx | The housing bills file carries the committee and floor facts Congress.gov records, and maker A sets the Rule 11.1 steps from them | The API records no hearing on any of the eight bills but cannot show a hearing held on the subject without a bill number, so a step number would claim more than the record holds
- D3-xxx | The margin of a change between two HVS years is the root of the summed squares of the two published margins | The two years are separate samples, and the published tables give no covariance; the sidecar says the margin is approximate
- D3-xxx | V7 source titles print as V7 stores them, straight apostrophes included | Atlas values are copied, never edited; the words pass sets the guide's apostrophes

Tested: the data check, 90 tables, 0 faults; each bill's actions and committees read from the API (fetch log in `.../round-1/research/dl/housing-bills/`); the committee tallies checked against the action text; the two Table B-5 files read in full, with the United States column taken for the six rows; every drug-price claim has source words (11 of 11); the other V7 tables the script writes are byte for byte unchanged (git shows no change).
Not tested: hearings held without a bill number (the API cannot show them); a House or Senate committee calendar for such hearings.

## Fix pass 3

From the data lead's DL-R4 and DL-R5. The data check reads 91 tables with 0 faults.

- **DL-R4, S34.** Confirmed from the Senate's own record, so S34 keeps its clause. The Congressional Record of November 21, 2013 (govinfo) prints Senator Reid's point of order "that the vote on cloture under rule XXII for all nominations other than for the Supreme Court of the United States is by majority vote"; the Senate voted 48 to 52 not to sustain the chair (vote 242) and invoked cloture on Patricia Ann Millett's circuit nomination 55 to 43 with a majority requirement of one-half (vote 244). On April 6, 2017 it voted 48 to 52 not to sustain the chair (vote 109) and invoked cloture on Neil M. Gorsuch's Supreme Court nomination 55 to 45 with a majority requirement of one-half (vote 110). `senate-cloture-motions-by-congress.meta.json` moves the item out of `unconfirmed` into a note with these sources (script `.../round-1/research/scripts/fix_pass3_cloture.py`).
- **DL-R5, S38.** `v7-issues.meta.json` gains `source_line_variants` for each domain, `domain_d01` to `domain_d10`, written by `research_v7_extract.py`. S38 takes `domain_d01`: "Source: Oath & Action’s systems atlas, Who Do They Answer To?, issue records in the domain of news, records and public information, 17 of 194 issues, as of October 15, 2026, United States. Snapshot of October 15, 2026. Grades are the atlas’s own."

- D3-xxx | The 2013 and 2017 cloture changes rest on the Senate's vote records and the 2013 Congressional Record | They are the chamber's own record of each precedent and the vote that applied it; the senate.gov overview page names only the 1917 and 1975 rules
- D3-xxx | The issues table carries a source line variant for every domain, not only S38's | Any later one-domain table then names the rows it draws with no new request

Tested: the four vote records read on senate.gov today (242 and 244 of 2013, 109 and 110 of 2017), each with its title, result and majority requirement; Reid's point of order read in the November 21, 2013 Congressional Record's text; the ten variants generated and D01's count (17) checked against the table; the other V7 tables unchanged.
Not tested: the April 6, 2017 Congressional Record (govinfo's address for the day's Senate pages returned "Page Not Found"), so the 2017 point of order's exact words are not quoted.

## Fix pass 4

From maker B's R-B13. The data check reads 91 tables with 0 faults.

- **S32.** `govinfo-pl-119-75-effective-dates.meta.json`'s printed source line now reads "Two dates computed from “months after enactment”; plan-year dates apply as each plan year begins." with curly quotes (script `.../round-1/research/scripts/fix_pass4_quotes.py`). The CSV's cells, "plans'" among them, are unchanged; S32 keeps its `words` maps for those two cells.
- **The shared writers.** D3-175's writer curled apostrophes only. `research_v7_extract.py`'s line writer now curls double quotes too, in printed lines and variants, which corrected `v7-pathway-electric-decision-makers` ("Electric and utility bills" now in curly quotes); my round 3 helper got the same rule. A scan of every sidecar finds no other straight quote in a printed line or variant.

- D3-xxx | The printed-line writers set double quotes curly as well as apostrophes, an opening quote after a space, bracket or line start and a closing quote elsewhere | D3-175 covered apostrophes only, and a printed line is guide text under Rule 06's typography
- D3-xxx | Data cells keep the text as written, straight quotes included | The coordinator's instruction: the file's values stay as they are, and the spec sets the cell's words

Tested: the scan of all 91 sidecars' printed lines and variants for straight quotes (none left); the two changed lines read; the data check.
Not tested: S32 rebuilt with the new line (maker B's step).

## Fix pass 5

From the coordinator: the studio's own wording in `govinfo-pl-119-75-effective-dates.csv`. The data check reads 91 tables with 0 faults.

- The three `date_basis` cells that ended "computed by the studio" now end "computed by Oath & Action from the law’s text" (curly apostrophe); no other cell changed (git shows three lines changed). The sidecar's `date_basis` description says the column's wording is the studio's, and its qualification now says "computed by Oath & Action". Script: `.../round-1/research/scripts/fix_pass5_date_basis.py`.
- For maker B: S32's `words` map keys on the old cell text, so it no longer matches. Re-key it to "Not later than 18 months after enactment, computed by Oath & Action from the law’s text" and "Plan years beginning on or after 30 months after enactment, computed by Oath & Action from the law’s text", or drop those two entries, since the cells now carry reader wording.

- D3-xxx | The studio's own wording in a data file names Oath & Action, as reader text does | The cell reaches readers in the chart's CSV export; publisher cells stay as published

Tested: the data check; the diff (three cells in one column).
Not tested: S32 rebuilt (maker B's step).

## Download item 2

Row 113, from Dustin's saved Department of Labor page (D3-459), done in parallel with the review (D3-462). Script: `work/build/scripts/phase-3/research_dol_freeze.py`, run as `python3 -I work/build/scripts/phase-3/research_dol_freeze.py <saved page> --freeze`. It checks the file's bytes and SHA-256 against its record first and stops on a mismatch, then reads the page only with Python's own HTML parser. The data check reads 93 tables with 0 faults.

**What the page holds.** Six tables on one page, the federal rate and 54 jurisdictions (50 states, DC, Guam, Puerto Rico and the U.S. Virgin Islands) in the same order in each, 39 columns: selected years 1968 to 1998 and every year 2000 to 2024. The page's note sets the as-of day: "Wage rates are for January 1 of each year except 1968 and 1972, which show rates as of February." The federal row reads $6.55 in 2009 and $7.25 from 2010, as the January 1 day implies. The page's title reads "Selected Years 1968 to 2024", and its latest column is January 1, 2024. The "2025" the plan and the download record expected is the page's last line, "This document was last revised in January 2025."; the record's "1961" is from note (a). There is no 2025 or 2026 column.

**Frozen** (ledger P7-223; P7-220's placeholder now points to it):
- `work/build/data/dol-state-minimum-wage-history.csv` and `.meta.json`: the table as published, 2,145 rows (55 a year by 39 years). Each cell keeps its text and footnote marks as the page prints them, with the hourly rates read beside it, the marks as letters, the page's bold, and the cell's status. The sidecar quotes the page's note, sources and every key line.
- `work/build/data/dol-state-minimum-wage-classes.csv` and `.meta.json` (derived): 50 states and DC for every January 1 from 2010 to 2024, 765 rows, in change 10's three classes, with flags for a lower tier and an employer-size limit and the page's words for each mark on each row.

**What a maker needs to know.**
- Panels after July 24, 2009 at one as-of day: any January 1 from 2010 to 2024. Above $7.25 (of 51): 15 in 2010, 20 in 2013, 30 in 2015, 30 in 2020, 31 in 2024.
- **2015 and 2020 are the same, class for class.** Every change after 2010 falls in 2011 to 2015 (15 states), plus Virginia in 2021.
- Below $7.25 with a state rate: Georgia ($5.15, employers of six or more) and Wyoming ($5.15) in every year; Arkansas 2010 to 2014 ($6.25, employers of four or more); Minnesota 2010 to 2013 ($5.25 to $6.15); Colorado 2010 ($7.24). Marked "..." in every year: Alabama, Louisiana, Mississippi, South Carolina and Tennessee. The page's key says "not applicable", not "no law".
- Qualifications kept per row: employer size, [c] four or more (Arkansas, Illinois, Nebraska, Virginia), (d) six or more (Georgia), (e) two or more (Indiana, Michigan, Vermont); lower rates for smaller employers, (g) (Minnesota, Montana, Oklahoma; Oklahoma's $2.00 to $7.25 is classed at $7.25); and two rates with no footnote, Nevada 2010 to 2023 and Ohio 2014 to 2016. The page lists no tipped, youth, farm or city rates.
- The page's bold, which its note says marks an increase, is missing from most columns before 2001 and all of 2014, so read change from the rates.

**The 2026 panel.** No frozen copy of the July 1, 2026 state table exists. `work/build/data/` has none. Chapter 01 cites it only through Atlas V7 (source K1508, accessed October 15, 2026), for Ohio and Pennsylvania in words, and V7 keeps only its counts (claim CL1516: 30 states and DC above $7.25, 13 at, Georgia and Wyoming at $5.15, five with no law). Those counts equal January 1, 2024's here, but equal counts do not show the same states. A route with no new download: make the last panel January 1, 2024, so all four panels come from one table at one as-of day, and print V7's July 1, 2026 count as a sourced sentence beside the panels, not as a map. A July 1, 2026 map needs the Department's "State Minimum Wage Laws" page (https://www.dol.gov/agencies/whd/minimum-wage/state) saved as a new download, and would mix two as-of days.

- D3-xxx | The history file keeps all 55 rows and 39 columns the page prints, the federal rate and three territories included | C1 freezes the publisher's table as published; row 113 reads its 50 states and DC from the derived file
- D3-xxx | Each cell keeps its printed text and marks, with the hourly rates and the marks as letters in their own columns | A maker filters by mark without rereading the page, and the cell still reads as published
- D3-xxx | Rates are read as numbers only where a cell plainly reads as dollars an hour; weekly and daily rates and the typing slips "4..65" and "1.25`" keep their text with no number | Reading a slip as a number would put the studio's guess in the publisher's column
- D3-xxx | The page's four NA cells (U.S. Virgin Islands, 1968 to 1976) are left empty, with the status "not available" | C1 keeps a missing value as an empty cell, and the data check refuses NA
- D3-xxx | The page's bold is kept as a column, and the sidecar says to read change from the rates | The page's note says bold marks an increase, but bold is missing from most columns before 2001 and all of 2014, and 15 cells of 2020 do not match it
- D3-xxx | The classes file covers every January 1 from 2010 to 2024, not only four panel years | The data lead picks panels from one file; 2010 is the first January 1 after July 24, 2009
- D3-xxx | A state's class reads the highest rate its cell prints, with flags for a lower tier and for employer-size limits and the page's words for each mark | Change 10's three classes need one rule, and the flags let a maker draw a lower tier or a size limit honestly
- D3-xxx | A state marked "..." goes in "below $7.25 or no state minimum", and the sidecar says the page's key reads only "not applicable" | Change 10 puts "no state minimum" in that class; the page itself does not say "no law"
- D3-xxx | Colorado's 2010 rate of $7.24 is classed below $7.25 and named in the sidecar | The page prints 7.24; the maker can say why one state sits a cent below
- D3-xxx | The classes file's printed line says covered employers pay the federal rate where a state is below $7.25 or has none, with V7 claim CL1516 in the sidecar | A map with "below" states should not suggest workers there earn $5.15; the Department's own state page, as V7 records it, says so
- D3-xxx | The frozen files take a new ledger row, P7-223, and P7-220 points to it | P7-220 was a placeholder; a new row keeps the ledger's dated history, as P7-221 and P7-222 did

The two printed lines:
- History: "Source: U.S. Department of Labor, Wage and Hour Division, Changes in Basic Minimum Wages in Non-Farm Employment Under State Law: Selected Years 1968 to 2024, rates as of January 1 (February in 1968 and 1972), federal, 50 states, DC, Guam, Puerto Rico and the U.S. Virgin Islands. Retrieved November 12, 2026. State law only; some rates apply only to larger employers." Variant `states_and_dc_2010_to_2024`.
- Classes: "Source: U.S. Department of Labor, Wage and Hour Division, Changes in Basic Minimum Wages in Non-Farm Employment Under State Law, rates as of January 1, 2010 to 2024, 50 states and DC. Retrieved November 12, 2026. Classes by Oath & Action from each state’s highest listed rate; some rates apply only to larger employers, and where a state is below $7.25 or has none, covered employers pay the federal rate." Variant `panels_2010_2015_2020_2024`.

**Requests.**
- **To the data lead, change 10's panels.** Please pick the panels from the classes file. Since 2015 and 2020 match, 2010, 2013, 2015 and 2024 would show each step; 2010, 2015, 2020 and 2024 would show the five flat years. Either way the last panel is January 1, 2024 unless Dustin saves the July 1, 2026 page.
- **To the main session.** Round 3's plan (row 113's publisher cell and the download list) names the page "Selected Years 1968 to 2025"; the page reads 1968 to 2024. I left the plan alone, since this task named the files I may write. If you agree, I correct those two cells in a later pass.

Tested:
- The saved page's bytes and SHA-256 against its record, before parsing: 124,921 bytes, d16798c7...ccc0, equal. The hash is unchanged after the freeze.
- The page read only by my script with `html.parser`, run with `python3 -I` and the path as an argument; no browser opened it.
- The script's own assertions: the title; six tables, each with one heading row; the same 55 rows in the same order in every table; 39 years in order; every mark in a cell defined in the key; the federal row at $6.55 in 2009 and $7.25 from 2010 to 2024; the note's January 1 sentence; no em dash or U+2011 in any file written.
- Read-back: all 2,145 frozen cells equal the parsed cells (the four NA cells empty by rule), and every class recomputed from the frozen history file equals the classes file.
- A second comparison from the structure dump's grid, column by column: 2,145 of 2,145 cells and their bold equal the CSV.
- A rerun writes all four files byte for byte the same.
- Both CSV files: UTF-8 without a byte-order mark, LF line ends, snake_case headers. Every printed line and variant starts "Source: " and holds no straight quote or apostrophe.
- The data check, `data_round0_build.py --check`: 91 tables, 0 faults before (not 90: fix pass 3 added one); 93 tables and 1 fault after the first freeze (the NA cells); 93 tables, 0 faults after the fix.
- The class counts by year, every change of class, the bold against the rates, and the 2024 counts against V7 CL1516, all computed by script.
- Chapter 01's source, the data folder and V7 searched for the July 1, 2026 table: none frozen; V7 holds counts only.
- The Census key: in none of the files I wrote, my scratch files, the ledger or this file (fixed-string search; nothing printed).

Not tested:
- dol.gov was not retried, and the July 1, 2026 state page was not read.
- Nevada's and Ohio's laws behind their unmarked two rates; the five "..." states' laws; whether note (g)'s lower rates still applied after 2005, where its dates end.
- The 1968 to 1998 values against the Book of the States; no cell was compared with a second source.
- Dustin's save against the live page; the file is taken as the page dol.gov served him.
- Any map drawn from these files (the maker's step), and the kit's reading of them beyond the data check.

Change log:
- Created: `work/build/scripts/phase-3/research_dol_freeze.py`; in `work/build/data/`, `dol-state-minimum-wage-history.csv`, `dol-state-minimum-wage-history.meta.json`, `dol-state-minimum-wage-classes.csv` and `dol-state-minimum-wage-classes.meta.json`.
- Modified: `work/research/20261021_Research-Ledger.md` (Part 7's "Download item 2" section with P7-223, P7-220's status and checked cells, claims 16 to 19, a change log line); `work/research/downloads/20261112_DOL-State-Minimum-Wage-History-1968-To-2024.json` (`status` only); this file (this section).
- Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/256961f5-3911-5bd9-908d-f34ce0435ace/scratchpad/phase-3/round-1/research/` (the structure dump and the rerun hashes).

## Review fix pass

From `work/handoffs/phase-3/20261112_Round-1-Fix-Brief.md` (calls D3-476 to D3-488), with its brand and craft addendum, the editor’s ED-R1 and ED-R2, the data lead’s requests and the engineer’s template contract, relayed by the main session. One script does every item: `work/build/scripts/phase-3/research_review_fix_round1.py <item> [--dl <folder>]`; it sets values, never appends, and refuses to write when a check fails (a recount that differs from the page, a frozen file whose hash differs). A rerun of every item wrote nothing. The data check reads 95 tables with 0 faults.

### Summary, in the order done

- **ST M1, S24 (D3-476).** The two Business Formation Statistics files keep every figure and now print their release: "September 2026 monthly release (October 14, 2026)". The Bureau’s own pages confirm it: its release schedule lists the September 2026 report on October 14 and the October 2026 report on November 12, and its notice says the annual update came with the November 12 release. I summed the November 12 file myself: every row for 2005 to 2021 equals the frozen file, and 2022 to 2025 differ (2025 United States total 5,696,742 against 5,671,836). The revision heads the new Phase 5 refresh list in the research ledger’s Part 7. Rule 14.1’s plate reads variant `all_years`, same key, new words.
- **ST M3, S34.** The 119th Congress row now reads 297 motions, 295 votes on cloture and 248 invoked. The cloture counts page answered today and gives those figures; the Senate’s vote lists give the same 295 and 248 once six votes the lists show with no question are read from their own records (all six "On the Cloture Motion"). The reviewer’s 289 missed those six. Every other row equals the page. The line now says "through November 10, 2026", the latest roll call.
- **ST S1 and S3, S31.** Variant `with_margin`: the Employment Situation for October 2026 (November 6, 2026) and the Bureau’s 90 percent interval of plus or minus 0.3 point for a month’s change in the rate at a rate near 6 percent. Two reads of the technical note gave the same words. The reviewer’s 0.2 was not the note’s figure. The note gives no interval for a change longer than a month. Every line of the file names its releases now, `unemployment_rate_only` included, so S31 had to take the new line.
- **ST S2 and S3, S27.** The nation’s purchase-only index joins the file as code US, 142 quarters, from the same release of August 25, 2026, base and adjustment, as the data lead’s ruling (d) requires. The line names the release and "50 states, DC and the United States"; variant `states_and_dc` serves a chart of the states alone.
- **BC M3 and ST S3, S36.** Columns `party`, `party_full` and `party_words` hold the party affiliation each committee’s FEC record names, for every committee that has one (the main session’s standard): DCCC and DSCC Democratic, NRCC Republican, and SFA Fund, Inc., a hybrid PAC, Republican. So note 3’s "records no party for a PAC" is wrong for one row. The line names the processing date the totals stand on.
- **BC S20 and ST S3, S25.** OPM’s January 2025 file (version 4, October 3, 2026), counted the way the frozen columns were: 2,304,585 people, with the change before and after it per agency. The count reproduces the frozen January 2022 and August 2026 columns in all 130 rows. The printed line names each file’s version; variant `with_january_2025` names all three.
- **ED-R1.** `fjc-active-judges-by-court-of-appeals`, derived from the FJC file: 13 courts, 179 judges, with the plate’s short names.
- **ED-R2.** `fec-super-pacs-by-cycle` (P7-224): super PACs in the FEC’s totals for each cycle, 80 in 2010 to 2,062 in 2024. The FEC’s PAC count page returned 404, and the NLRB’s petition counts load only through an outside reporting service.
- **AX S1.** `source_line_templates` on nine multi-year files and the DOL classes file. The DOL classes lines read "January 1 rates", since the kit takes "as of January 1, 2010" for a vintage; the data lead’s panels variant replaces the unused 2015 and 2020 one.
- **ST S11.** S20’s line becomes variant `with_margins` on both its sidecars. S41 and S42’s line goes to the engineer (ENG-12 below): the Program’s page, reread today, still says "There is a margin of error of +/- 1.9%." and names no confidence level.
- **ST S12.** Row 113’s notes and cells in the round 3 plan now give January 1, 2010, 2014, 2019 and 2024 and the page’s "1968 to 2024"; change 12’s column goes to the engineer (ENG-13 below). Tennessee’s Public Chapter 621, read today, bars a county election commission from ranked-choice voting "for a statewide or local government office" and defines local government to include "an incorporated city or town". The question for the open questions file was already settled by D3-260 (call 7).

### Routine calls

- D3-xxx | Frozen files whose publisher revised them keep their figures and print the frozen release by name and date; only S34’s 119th row changes, because it never matched the Senate’s record | D3-476 freezes a revision, not an error
- D3-xxx | A vintage clause goes into the printed line itself (and every variant), so no line without it stays valid; a spec that set a variant by hand takes the new words | Access S1’s point: the default line has to be the honest one
- D3-xxx | Vintage clauses keep the wording makers were already copying, though the kit’s line check reads their 2026 dates | Every file’s period already reaches 2026 except Business Formation Statistics, which holds no 2026 rows, so no check weakens in practice
- D3-xxx | The BFS release is named "September 2026 monthly release (October 14, 2026)" | The Bureau names its releases by data month and posts each on a scheduled day; both identify the numbers a reader can find
- D3-xxx | The cloture recount counts a vote whose own record reads "On the Cloture Motion" when the Senate’s list leaves its question blank | The vote list is a summary; each vote’s record is the Senate’s fuller account, and with it the count equals the Senate’s cloture page
- D3-xxx | S31’s margin is the note’s interval for one month’s change, named as such | It is the only interval the Bureau publishes for the rate; a longer span has none, and the sidecar says so
- D3-xxx | The nation’s house price index joins the state file as code US, first, as the BFS files carry it | The engineer’s set-apart line reads the nation from the chart’s own file, and contract C1 names the nation US
- D3-xxx | The party columns copy the party affiliation each FEC committee record names, for every committee that has one, with the record’s spelling and a reader’s word | One standard for all 25 rows (DR-93, the main session’s ruling); the record is the commission’s own
- D3-xxx | Committee names stay as the 2024 totals print them; newer names on four records go in a note | The chart shows the 2024 cycle
- D3-xxx | OPM’s January 2025 column comes from the version published the same day as the January 2022 file’s | One publishing round for both early dates, so a later revision cannot fall between them
- D3-xxx | Rule 14.13’s new data is the FEC’s count of super PACs by cycle | A documented count with no sampling margin, from a publisher no rule plate draws, in money in politics (D03), eight values; the PAC count page is gone, ssa.gov refused in round 1, and the NLRB’s counts load only in a reporting service
- D3-xxx | Span templates go on annual files only, built from each printed line by swapping its period words | The kit fills years; monthly and quarterly files need month or quarter words a year cannot give
- D3-xxx | The DOL lines say "January 1 rates" | The kit’s line check reads "as of January 1, 2010" as a vintage and would drop the panel’s first year
- D3-xxx | Ohio’s ban is "partly" for city elections and Tennessee’s "yes" | Ohio leaves home-rule cities an opening at a cost (Ballotpedia); Tennessee’s act names city offices that county commissions conduct (Public Chapter 621)

### Requests

- **ENG-12, to the engineer (ST S11, S41 and S42).** In `data_round0_build.py`, add to `v7-stock-trading-ban`’s `source_line_variants` the key `survey_only_margin_credited`: "Source: Program for Public Consultation, University of Maryland, survey of 2,625 registered voters, fielded May 19 to 30, 2023, United States, as recorded in Oath & Action’s systems atlas, Who Do They Answer To?, snapshot of October 15, 2026. A margin of error of plus or minus 1.9 points for the whole sample, with none by party, from the Program’s survey page, read November 12, 2026." In `V7_NOTES`, change "read November 11, 2026" to "read November 11 and 12, 2026". Then maker A sets S41 and S42 to the new variant.
- **ENG-13, to the engineer (ST S12, row 87).** In `data_round0_build.py`, add two columns to `ballotpedia-rcv-prohibitions-by-state` (as `ADDED_ROWS` adds rows): `reaches_city_elections` (category; "yes" for AL, AR, FL, ID, IN, IA, KS, KY, LA, MS, MO, MT, ND, OK, SD, WV, WY and TN; "partly" for OH; empty where there is no ban) and `city_reach_note` (text; TN: "Public Chapter 621 bars a county election commission from ranked-choice voting for a statewide or local government office, and defines local government to include an incorporated city or town (read November 12, 2026)"; OH: "Home-rule cities may still adopt it, but lose state local government fund distributions while it is in effect (Ballotpedia; the act’s text not read)"; MO: "Ballotpedia says the amendment prohibits ranked-choice voting; the amendment’s text was not read"; empty for the others). Descriptions: "whether the ban reaches a city’s own elections" and "the source of that reading where it needs one".
- **To the main session.** Each landing was sent as a one-line message. Two flags for owners: S36’s note 3 (maker A and the editor), since SFA Fund, Inc.’s record names a party; and S25’s note on January 31, 2025, eleven days after the inauguration (maker B with the data lead).

### Tested

- Business Formation Statistics: the November 12 file downloaded (SHA-256 prefix 47975a1c7bca0aad, last-modified 15:00:14 GMT) and summed by script as the sidecar describes; 2005 to 2021 equal in all 52 rows a year, 2022 to 2025 differ, with the five figures above. The release schedule and the notice read on census.gov. The derived change file agrees with the frozen state file in all 52 rows.
- Cloture: both 119th vote lists and the 116th and 118th parsed; the 13 votes with no question read from their own records; the recount equals the page for the 119th (asserted before writing), and my method also gives the 116th’s 298 votes and 270 invoked and the 118th’s 241 votes, but 228 invoked for the 118th against the page’s 227 (not traced; the file keeps the page’s figure, and the 118th is not S34’s subject). All 54 other rows of the page equal the file.
- The technical note read twice through the web-fetch tool with different prompts; the JOLTS release read once; the file’s September 2026 openings (7,523 thousand) agree with its "7.5 million".
- FHFA: today’s state file equals the frozen rows in all 7,242 values; the national file’s columns, base (100 in the first quarter of 1991), 142 quarters and the release’s quarter and year changes asserted by script.
- FEC: 25 committee records read from the API, every ID matched; the CSV round trip byte for byte before the columns went in. Super PACs: the eight counts read from the API, and every row for 2012 and 2024 paged and counted (857 and 2,062 distinct committees).
- OPM: the January 2022 and August 2026 files fetched again match the frozen SHA-256 prefixes; my count reproduces both frozen columns in all 130 rows (asserted before writing).
- FJC: 13 courts summing to 179, the Ninth Circuit 29 (asserted).
- DOL: the freeze script rerun on the saved page after its hash check; both CSV files unchanged byte for byte (checked with sha256sum).
- The kit: S24, S25, S27, S34 and S36 pass `oa-chart.mjs check` (S24 and S34 also `build` at 1440 px, Newsprint, no PNG) with the new sidecars; a scratch copy of S31 passes with `with_margin` and the maker’s S31 failed with the old line, as expected; the production test’s spec passes the source check with `source_line_template: "two_years"` and with "span"; a scratch ranked-bar spec reads the judges file’s 13 rows.
- The data check, `data_round0_build.py --check`, after every item: 93, then 94, then 95 tables, 0 faults each time. A rerun of every item wrote nothing.
- No em dash or U+2011 in the plan or ledger text I wrote (asserted by the scripts that wrote them). The Census key appears in none of my files, downloads or logs; no Census API call was made in this pass.

### Not tested

- Any chart rebuilt by its maker with the new lines and columns, at every width and ground; I checked specs, not captures.
- The April 2017 and other cloture page history beyond the 119th row; the 2025 en bloc precedent is recorded in the sidecar but no chart was checked against it.
- BLS pages with this container’s own reader (bls.gov refuses it); the margin rests on the web-fetch tool’s quotes.
- FHFA’s August 25, 2026 news release itself; its date and figures come from the release list as the web-fetch tool read it.
- What a party entry on a hybrid PAC’s FEC record means; whether a committee with no financial report appears in the FEC totals.
- Ohio SB 63’s text; Tennessee’s code sections on who conducts municipal elections (Justia refused).
- OPM’s December 2024 file.
- ENG-12 and ENG-13 in the engineer’s script, and S41, S42 and row 87 with them.

### Change log

- Created: `work/build/scripts/phase-3/research_review_fix_round1.py`; in `work/build/data/`, `fjc-active-judges-by-court-of-appeals.csv` and `.meta.json`, `fec-super-pacs-by-cycle.csv` and `.meta.json`.
- Modified in `work/build/data/`: `census-bfs-business-applications-by-state.meta.json`, `census-bfs-business-applications-change-by-state.meta.json`, `senate-cloture-motions-by-congress.csv` (the 119th row) and `.meta.json`, `fred-unemployment-and-job-openings.meta.json`, `fhfa-house-price-index-by-state.csv` (142 rows added) and `.meta.json`, `fec-independent-expenditures-2024.csv` (three columns) and `.meta.json`, `opm-federal-employment-by-agency.csv` (three columns) and `.meta.json`, `census-hvs-homeownership-by-age.meta.json`, `census-hvs-homeownership-by-age-moe.meta.json`, `dol-state-minimum-wage-classes.meta.json`, `dol-state-minimum-wage-history.meta.json`, and the templates on `treasury-mts-outlays-by-function`, `treasury-mts-receipts-by-source`, `census-cbp-civic-organizations`, `census-cbp-newspaper-publishers`, `census-cps-median-household-income`, `cms-nhe-by-source-of-funds` and `census-nrc-completions-by-structure` (`.meta.json` each).
- Modified elsewhere: `work/build/scripts/phase-3/research_dol_freeze.py` (the classes lines, panels variant and templates); `work/handoffs/phase-3/20261112_Round-3-Data-Plan.md` (row 113’s cells and note, the download list, my status lines for changes 10 and 12); `work/research/20261021_Research-Ledger.md` (Part 7’s "Review fix pass" with P7-224, the "Phase 5 refresh list", claims 20 to 26, a change log line); this file (this section).
- Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/256961f5-3911-5bd9-908d-f34ce0435ace/scratchpad/phase-3/round-1-fix/research/` (downloads and fetch logs under `dl/`, helper scripts, the `pyarrow` environment, kit outputs).
