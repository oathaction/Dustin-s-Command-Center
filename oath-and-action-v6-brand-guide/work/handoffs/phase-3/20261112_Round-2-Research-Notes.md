# Round 2 research notes

Oath & Action Edition 06, Phase 3, round 2. Research lead (`oa-research-lead`), November 12, 2026, under `work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Kept current as the work goes, since the container can restart.

## Summary

Started 18:56 UTC; this state at 19:42 UTC. Every task is done and nothing waits.

**Round 4's data is planned, signed off, fetched and frozen.** The plan (`work/handoffs/phase-3/20261112_Round-4-Data-Plan.md`) gives rows 115 to 127 for the 13 forms: 11 draw data, 2 are rule only. The data lead signed it off with two changes, both applied: row 123's comparison cards draw the three kinds of federal trial judges, and row 125's annotated illustration draws the first page of Public Law 119-12. Round 4 now draws no election data. Ten new files are frozen in `work/build/data/` under C1, with research ledger rows P7-301 to P7-310 (fetched 19:23 to 19:31 UTC); the social card draws S19's frozen file. The data check reads 111 tables with 0 faults. The plan's last section, "Research lead, after the sign-off", records what the fetch confirmed and the data lead's conditions for round 4's maker.

What the fetch found:
- **Row 115.** Union membership from V7 claim CL1514: 10.0 percent of wage and salary workers in 2025 (11 months), 20.1 percent in 1983.
- **Row 116.** 2022 Census of Governments: 90,888 governments, 1 federal, 50 states and 90,837 local (3,031 county, 19,491 municipal, 16,214 township, 39,555 special district, 12,546 independent school district).
- **Rows 117 and 118.** ACS 2025: 336,838,154 people; private only 56.2 percent, both 7.1, public only 28.3, uninsured 8.4 (margin 0.1). The uninsured share confirms the Euler at true area with no frame.
- **Row 122.** Fiscal 2024: $994.9 billion in revenue, 45.2 percent state, 43.2 local, 11.6 federal; $17,619 current spending per pupil. Federal revenue includes $39.2 billion in COVID-19 relief, which I summed from the Bureau's all data items file after its documentation said relief is included. Table 13 mislabels fall 2023 enrollment as fall 2022.
- **Row 123.** Seats on September 30, 2025: 677 district, 345 bankruptcy and 593 magistrate judge positions. The statute tables list 673 and 316; the courts' counts include temporary judgeships.
- **Row 126.** No 2027 tax date falls on a weekend or DC holiday. Publication 509 for 2027 is not out, so the rule was checked against the 2026 edition.

**Rule 01.9 for chapter 14 as a whole, after the changes:** 108 examples. Taxes, wealth and economic security holds 16 against a limit of 27; California and Florida hold 5 each against 21. A script recounted it from the generator's log, the specs and the plans' rows, and it matches the data lead's figures.

**Row 113 (done 19:00 UTC).** The round 3 plan's row 113 named the four January 1 panels from Dustin's Department of Labor download but not DR-243's sentence. Its cells and note now say the atlas's July 1, 2026 count prints beneath the maps as one sourced sentence, read by script from V7 claim CL1516 (graded documented: 30 states and DC above $7.25, 13 at $7.25, Georgia and Wyoming at $5.15, five with no minimum wage law), citing the Department's "State Minimum Wage Laws" page updated July 1, 2026 (V7 source K1508, accessed October 15, 2026). Nothing else in the file changed.

**The data lead's R1 and R2 (done 19:10 UTC).**
- **R1, `census-stc-state-tax-collections` (S50).** The DC row is the Bureau's own: the FY2025 flat file prints a DC column (22 of 25 tax items with a value, $11,261,267 thousand), and its U.S. column equals the 50 state columns' sum exactly. Every frozen state row and the DC row reproduce from the flat file and the population file. The U.S. row now divides the 50 states' taxes by the 50 states' 339,312,487 residents ($4,526.3401 per resident, was $4,517.137 over a population that included DC's); code `US` kept, named "All 50 states". The DC row stays, outside the total; S50 already leaves it out.
- **R2, `treasury-mspd-debt-subject-to-limit` (S64).** Public Law 119-21, section 72001 (139 Stat. 332, approved July 4, 2025), read on govinfo.gov: the limit "is increased by $5,000,000,000,000". Public Law 118-5, section 401, suspended the limit through January 1, 2025 and raised it on January 2, 2025. The frozen table agrees. The sidecar's qualification and a new note cite both laws.

**Maker B's derived files (checked 19:20 UTC, rechecked 19:40 UTC).** Five tables from `maker_b_round2_derive.py`. My check recomputed every figure from the frozen files by its own method. It found two faults: the judges' bins counted 850 service records, which hold 845 judges, and two printed lines had a straight apostrophe. Maker B fixed both, and the recheck finds 0 faults; the bins now hold 845 judges, each once, median 8.0246 years. No new ledger row is needed, since each sidecar cites its source's row; the ledger lists all five under those rows.

**The editor's wording change (19:50 UTC).** `census-acs-earnings-ratio-by-state.meta.json`'s printed line now ends "each median covers all such workers, whatever their jobs." in place of "medians for all such workers, not for the same jobs." The sidecar has no variant or template carrying the clause, and no script writes it (maker B's derive script only reads the file), so S57 takes the new line from the sidecar. The data check reads 111 tables with 0 faults.

**S53's program ages (maker B's RB-R3, 20:10 UTC).** Both ages hold, read November 12, 2026. 42 U.S.C. 402(a) (U.S. Code, 2024 edition, govinfo) entitles a fully insured individual who "has attained age 62" to old-age insurance benefits, and 416(l)(2) defines "early retirement age" as "age 62" for an old-age benefit. 42 U.S.C. 426(a) entitles to Medicare's hospital insurance an individual who "has attained age 65" and is entitled to Social Security or railroad retirement benefits; medicare.gov's "Get started with Medicare" reads "Medicare is health insurance for people 65 or older who meet citizenship or residency requirements", with earlier eligibility for a disability, End-Stage Renal Disease or ALS. ssa.gov refused this container (HTTP 403). The note's words hold: "can start at age 62" matches the law, and "covers most people from age 65" is a fair summary of the age-65 rule with its residency and disability qualifications. `census-pep-population-by-age-sex.meta.json` gains the variant `with_program_ages`, its printed line plus "Program ages from the Social Security Act, 42 U.S.C. 402(a) and 426(a), read November 12, 2026.", and a note quoting what was read. Data check: 111 tables, 0 faults.

**S62's hearing step (maker A's R-A1, 20:20 UTC).** "None in the bill's record" holds, read November 12, 2026. Congress.gov's API (key injected) gives S. 146's full action list, 23 actions, and its committees record: Senate Commerce's only activities are Referred To (January 16, 2025) and Discharged From (February 13, 2025, by unanimous consent), with no hearing or markup. The House held the bill at the desk and passed it under suspension with no committee referral. The committee's own hearings list (commerce.senate.gov, 24 pages, the 240 most recent meetings, 99 of them in the 119th Congress from January 15, 2025) names no hearing on the bill or its subject. The House companion, H.R. 633, was marked up by House Energy and Commerce on April 8, 2025 and reported April 28; that is a different bill's record. `congress-gov-take-it-down-act-actions.meta.json` carries a note with all of this, and the ledger a line under P7-034. Data check: 111 tables, 0 faults.

## Routine calls

- D3-xxx | Row 113's sentence reads V7 claim CL1516 and names source K1508, with the counts in the claim's own supporting text | DR-243 asks for the atlas's July 1, 2026 count as a sourced sentence; the claim holds the counts, and K1508 is the page it cites
- D3-xxx | The state tax file keeps the Bureau's DC column as its own row, outside the U.S. total | The publisher's flat file prints it, and C1 freezes a table as published; a chart of the states leaves it out
- D3-xxx | The U.S. row of state tax collections divides the 50 states' taxes by the 50 states' residents and is named "All 50 states", code `US` kept | Numerator and denominator then count the same places (data lead's R1); the code is the Bureau's own column name, and maker B reads it as the reference row
- D3-xxx | Round 2's fix, check and freeze scripts live in the research lead's scratch folder, not in `work/build/scripts/` | The round 2 ownership table gives the research lead data files, the ledger, the plans and its notes, and no script; each script refuses to write unless its checks pass, and a rerun writes nothing
- D3-xxx | Round 4's plan counts the editor's 13 rule plates from the generator's log and each specimen by its spec where one exists | The data lead's round 3 sign-off put the plates in the count, and the log and specs are what the build counts (R3)
- D3-xxx | Round 4's re-picks follow the reasons rounds 1 to 3 signed off: a specimen or chapter that already draws the data moves the new form to other data | The same test applied to every round keeps chapter 14 from drawing one dataset three or four times
- D3-xxx | The icon array reads union membership from V7 claim CL1514, citing the Bureau of Labor Statistics' release | bls.gov refused (403) and its API answered 503; V7 graded the figure documented, and S41 prints a V7-recorded survey the same way; the data lead declined download item 3
- D3-xxx | Round 4's step-by-step draws a federal records request (FOIA) | The data lead's round 3 change 3 set aside applying for a benefit, which row 102 now draws, and named public records; signed off
- D3-xxx | The by-the-numbers panel leaves out a count of school districts | The finance survey counts public school systems, dependent ones included, and would print a different count from row 116's Census of Governments
- D3-xxx | Maker B's derived files cite their frozen sources' ledger rows and take no new row; the ledger lists them under those rows | The derived files under P7-006 and P7-025 set that form, and C1's `ledger_row` is met
- D3-xxx | Row 123's seats are the courts' own counts on September 30, 2025, with the statute tables' counts in their own column | The courts count positions authorized, temporary judgeships included, and the statute tables do not; both are printed so neither reads as the other
- D3-xxx | Row 122 prints fiscal 2024's COVID-19 relief within federal revenue, summed from the Bureau's all data items file | The data lead asked the note to say so if relief was included; the Bureau's documentation says it is, and the summed items show how much ($39.2 billion of $115.1 billion)
- D3-xxx | Row 125 lists the running head in its three parts, with semicolons | The page sets it with dashes; the guide sets no em dash, and the round 1 call splits such text rather than repunctuating a quote
- D3-xxx | Row 126 counts calendar 2027 and marks Budget Act dates as a timetable and tax dates as due dates with a consequence | The data lead asked which dates carry a consequence; section 631 attaches none, and the tax code adds to tax for a missed date
- D3-xxx | The union membership table is a V7 file with ledger row P7-301 | The main session asked for ledger rows from P7-301, and the row records the Bureau's release V7 cites

## Requests

- **To the main session.** Round 4's data is frozen; round 4's maker reads the plan's last section for the data lead's conditions. The fetch, freeze and check scripts live in my scratch folder, since the ownership table gives me no script. If you want them in the repository, as round 1's were, name the file and I copy them there.
- **Closed:** the data lead's sign-off (signed off with two changes, both applied); RL-B1 and RL-B2 to maker B (both fixed); the data lead's R1 and R2.

## Tested

- Host reachability for round 4's candidate sources, 18:57 to 19:01 UTC, logged in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/65b3d20e-985e-5fe9-b272-d7d01bd821cd/scratchpad/phase-3/round-2/research/reach/` (`reach-1.tsv` to `reach-3.tsv`).
- Round 4's fetch, 19:23 to 19:31 UTC: every file in its own folder under `.../research/dl/` (uscode, plaw-119-12, ecfr, cog, f33, acs, foia, courts, irs), each with a fetch log of time, address with any key removed, status, bytes and SHA-256 prefix. Every request returned 200 except four eCFR versioner calls (406), replaced by its renderer, and five uscourts.gov addresses (404), replaced by the pages' current addresses.
- `scripts/freeze_round4.py` asserts, before writing: every quoted phrase in the step, judge, law and calendar files against its source text; the Census of Governments' parts summing to its totals; DP03's insured plus uninsured equal to the population, and the four overlap regions summing to it; the school finance revenue sources summing to the total, and the all data items file's federal revenue equal to Table 1's; the judgeship tables summing to 673 and 316; the law's first-page parts on the PDF's page 1; the weekend and holiday rule against Publication 509 (2026); every 2027 date's weekday. A rerun wrote nothing.
- The data check, `data_round0_build.py --check`: 100 tables, 0 faults before R1 and R2 and after each; 101 with maker B's files; 111 with round 4's, 0 faults.; 111, 0 faults after the editor's wording change.
- The count after the changes, by `scripts/recount_ch14.py`: 108 examples, every domain as the data lead gives it, California and Florida 5 each, both limits holding.
- Every V7 value the plan cites, asserted by `scripts/plan4_v7_check.py`; row 113's by `scripts/row113_v7_read.py`.
- R1 and R2: each publisher file fetched and read by script, each fix asserted against it, a rerun writing nothing.
- Maker B's five derived files, by `scripts/check_maker_b_derived.py` (own binning, quartiles by linear interpolation written out, quarterly means, outlier sets, and each sidecar and CSV under C1): two faults at 19:20, 0 at 19:40 after maker B's fixes; maker B's own `--check`, 0 faults.
- No em dash or U+2011 in any file I wrote (asserted by the writing scripts, and checked on the plans, the ledger and these notes).
- The Census key: one ACS call, its address built from the environment at request time; a fixed-string search finds the key in none of the data folder, the research folder, the handoffs or my scratch folder (0 files), and the fetch log records the address with the key removed.

## Not tested

- A hearing on the subject held under another name or in a subcommittee; the committee's list was searched by title, and Congress.gov records no hearing activity on S. 146.
- ssa.gov's own pages on claiming at 62 (HTTP 403); the age rests on the statute.
- Any round 4 chart; round 4's maker draws them later.
- Why the courts count 677 district positions against the 673 in 28 U.S.C. 133's table; temporary judgeships are the likely difference and were not traced seat by seat (ledger claim 28).
- The Bureau of Labor Statistics' release itself (bls.gov refused); row 115 rests on V7's record of it (claim 29).
- The rest of the Congressional Budget Act, searched for a consequence attached to a missed timetable date; only section 631 was read (claim 30).
- IRS Publication 509 for 2027, not yet published; DC's own holiday law, behind 26 U.S.C. 7503's "legal holiday in the District of Columbia", was not read, and the holiday list follows Publication 509 (2026).
- Whether the editor's round 2 redraws of Rules 14.3 and 14.9 change either plate's domain or states; the log after round 2 gives that.
- Why the Bureau's state tax flat file prints DC outside its U.S. total (claim 27).
- S49, S50, S51, S52, S56 and S64 rebuilt with the changed or checked files (the makers' step).

## Files

Created:
- `work/handoffs/phase-3/20261112_Round-4-Data-Plan.md` (the data lead appended its sign-off; I applied its changes and added the last section)
- `work/handoffs/phase-3/20261112_Round-2-Research-Notes.md` (this file)
- In `work/build/data/`, each with its `.meta.json`: `v7-union-membership.json`; `census-cog-2022-governments-by-type`, `census-acs-health-coverage-types`, `census-acs-health-coverage-overlap` (derived), `govinfo-disaster-declaration-steps`, `census-school-system-finances-2024`, `uscode-federal-trial-judges`, `govinfo-foia-request-steps`, `govinfo-pl-119-12-first-page`, `govinfo-budget-and-tax-deadlines-2027` (CSV)

Modified:
- `work/handoffs/phase-3/20261112_Round-3-Data-Plan.md` (row 113's cells and note only)
- `work/build/data/census-stc-state-tax-collections.csv` (the U.S. row) and `.meta.json`
- `work/build/data/treasury-mspd-debt-subject-to-limit.meta.json` (qualification and one note)
- `work/build/data/census-acs-earnings-ratio-by-state.meta.json` (the printed line's last clause, the editor's words)
- `work/build/data/census-pep-population-by-age-sex.meta.json` (variant `with_program_ages` and one note, for S53)
- `work/build/data/congress-gov-take-it-down-act-actions.meta.json` (one note, the hearing check for S62)
- `work/research/20261021_Research-Ledger.md` (Part 7's "Round 2" section and "Round 4 datasets" section with P7-301 to P7-310; claims 27 to 30; change log lines)

Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/65b3d20e-985e-5fe9-b272-d7d01bd821cd/scratchpad/phase-3/round-2/research/` (reach logs; downloads with fetch logs under `dl/`; scripts `fetch.sh`, `freeze_round4.py`, `fix_stc_r1.py`, `fix_mspd_r2.py`, `recount_ch14.py`, `plan4_v7_check.py`, `row113_v7_read.py`, `check_maker_b_derived.py`, `stc_read.py`, `html_text_grep.py`, `htmltext.py`, `ecfrtext.py`, `xl_dump.py`).

## Review fix pass

November 12, 2026, 22:00 to 22:30 UTC, under `work/handoffs/phase-3/20261112_Round-2-Fix-Brief.md` (research lead’s paragraph, the access addendum D3-905, and D3-910), the data lead’s rulings RF-4, RF-5, RF-11, RF-11a and RF-20, and the main session’s messages. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/3ab6316c-6935-5f23-804c-cfaafd548447/scratchpad/phase-3/round-2-fix/research-lead/` (scripts in `scripts/`, downloads in their own folders under `dl/`, each with `fetch-log.tsv`).

### Summary

Every item is done, and nothing waits on me. No frozen figure changed (D3-476). Each fix is a sidecar field, a source line variant, or a column the publisher prints beside a frozen one. The data check reads 111 tables with 0 faults. The data lead signed off RF-11a’s columns, and the access reviewer rechecked AX S8’s counts by script.

- **ST M3 (with RF-5).** `house-history-party-divisions.meta.json`: `observation_period` now reads "82nd Congress (1951 to 1953) to 119th Congress (2025 to 2027), as first elected for each Congress", and the note calls the table "the count as first elected for each Congress", not an opening count. The Clerk’s sidecar gains variant `with_party_divisions_119th`, the line S48 prints. It gives the Clerk’s count first, since it is drawn, then the Historian’s 119th Congress row with its geography and qualification. It names both publishers the way the kit’s two-dataset check reads them.
- **ST S5 (with RF-11 and RF-11a).** `census-acs-tenure-by-state` gains three kinds of column:
  - `households_moe` (B25003_001M), read from the same table and vintage; the same API call returned every frozen count unchanged.
  - `owner_pct_moe_dp04` and `renter_pct_moe_dp04`, the Bureau’s own margins from Data Profile DP04. These are the margins a chart prints.
  - `owner_pct_moe_formula` and `renter_pct_moe_formula`, formula (6) of the Bureau’s ACS handbook, chapter 8, kept as a check and printed nowhere.

  Variant `with_dp04_margin` names DP04. DC’s renter share, 61.9 percent, carries 1.5 points. Every state sits below half past its margin. RF-11 first ruled the formula. I then found that DP04 prints the margins, and RF-11a re-ruled to the published ones.
- **AX S8’s data side (D3-905).** The Census Bureau publishes no percent margin in Table B28002, which holds counts and count margins only. It does publish both shares with their margins in Subject Table S2801 of the same ACS 2025 1-year release, and S2801’s counts equal B28002’s in all 52 rows. `census-acs-broadband-by-state` gains `households_moe` (B28002_001M), the printed `broadband_any_pct_moe_s2801` and `broadband_fixed_pct_moe_s2801`, and the check-only `broadband_fixed_pct_moe_formula`. Round 3’s frozen `broadband_any_pct_moe` stays and is now check-only. Variants `any_with_s2801_margin` and `fixed_with_s2801_margin` name S2801, and the formula variants I first wrote are withdrawn; no spec used them. Both margin sidecars gain three fields for the engineer’s check:
  - `source_line_columns`: the columns each line covers.
  - `margin_columns`: each value’s printable margin.
  - `check_only_columns`: margins a chart must not print.

  Against the nation with S2801’s margins, 20 states and DC sit above, 22 states below and 8 within. Nevada sits near the line, above it by under 0.02 point.
- **ST S6, the data side.**
  - S47: `treasury-mts-outlays-by-function` gains variant `treemap_fy2026_september_statement` and a note on the year-end report. Today’s API record of September 30, 2026 equals all 20 frozen fiscal 2026 lines.
  - S46: `cms-nhe-by-payer-four-groups` gains variant `release_named` ("release with data through 2024"; "Each release can revise every earlier year"). Today’s CMS zip equals the frozen file in all 715 cells.
  - S45: `census-nrc-completions-by-structure` gains template `span_september_2026_release`. The release is September 2026, released October 20, 2026, CB26-162, and today’s file has the frozen SHA-256 prefix.
  - S58: `census-cps-median-household-income` gains a note quoting Table 2’s deflator words (C-CPI-U from 2000, R-CPI-U-RS before). The table, read again, equals all 61 frozen rows.
- **RF-20.** `frb-fomc-projections-unemployment` gains variant `with_unemployment_history`, which adds the Bureau of Labor Statistics’ fourth-quarter averages for 2021 to 2024 and says 2025 has none.
- **RF-4, D3-835 and D3-910.** `v7-numbers.meta.json`’s qualification says V7 stores figure 4’s inspectors general sentence under figure 5, and that figure 7’s calls H.R. 7008 "a ban". The engrossed text of July 22, 2026, read on govinfo.gov, has two parts: section 2, "Restrictions on covered investments", and section 3, "Requiring voters to provide photo identification". Ballot Measure 2 now reads "on the ballot on November 3, 2026". `work/build/scripts/phase-3/research_v7_extract.py` writes the same qualification; that one string is the only change to the script. I ran it first in a scratch mirror, where 20 of 20 outputs came out byte for byte, then in the repository, where `git status` and `git diff --stat` on `work/build/data` matched the state before the run.
- **The stale lines.** The round 3 data plan keeps every line as the record and marks the stale ones:
  - Its limits sentence and both count tables point to the round 4 plan’s 108 examples, with limits of 27 per domain and 21 per state.
  - The host line, download item 2 and the fallback sentence say the file came and is frozen as P7-223, so row 113 waits on nothing.
  - The sign-off request notes row 108’s move to taking part, trust and shared norms.
  - Change 10’s panel years point to DR-243’s 2010, 2014, 2019 and 2024 and the variant `panels_2010_2014_2019_2024`.
  - The status paragraph gains a "Since then" line.

  The research ledger’s P7-220 now reads "1968 to 2024" and DR-243’s panels, and Part 7 gains a "Review fix pass, round 2" section, three Phase 5 refresh rows (Treasury, NHE, NRC) and claims 31 to 33.

### When a margin is missing (AX S8, for the editor and the engineer to carry into entry 14.74 and the README)

The Bureau does publish a margin for the fixed broadband share, so AX S8’s case is closed by the columns above. The same question will come back for other files, so this is the order a designer follows:

1. Read the sidecar’s `margin_columns` for the value the chart draws, and print that column. Never print a column listed in `check_only_columns`, and never draw a margin whose unit differs from its value’s, such as a count margin on a percent.
2. If the sidecar names no margin, ask the research lead whether the publisher prints one elsewhere in the same release. For the American Community Survey, look in the Data Profile (DP) and Subject (S) tables of the same year and vintage. The research lead adds it as a column under C1; a spec never computes one.
3. If the publisher prints no margin for the figure drawn, as for S57’s state ratios, the research lead computes it by the Bureau’s published formula, stores it with its method in the sidecar, and the chart’s note says it was computed (RF-11a).
4. If no margin exists and none can be computed, as for a studio share without its denominator’s margin, draw no interval. The words then rank or compare nothing the survey cannot support, and the note says the publisher gives no margin. `census-acs-labor-force-by-age-sex`, whose participation rates carry no published margin and lack the pieces of a derived one, is the case in the data folder today.

### Routine calls

- D3-xxx | The margins a chart prints are the publisher’s own where the same release prints them (DP04 for tenure, S2801 for broadband); the formula margins stay as check-only columns | RF-11a; Rule 14.9 prints the publisher’s uncertainty, and the formula differs from the published margins by up to 0.32 points
- D3-xxx | New margin columns carry the table in their names (`_dp04`, `_s2801`, `_formula`), and no column keeps the bare name `*_pct_moe` for a new margin | A designer meeting two margins for one value picks by name and by `margin_columns`, never by guess (AX S8)
- D3-xxx | Sidecars with more than one margin or measure gain `source_line_columns`, `margin_columns` and `check_only_columns` | They give the engineer’s check the data it needs to fail a line or margin the chart does not draw (AX S8)
- D3-xxx | New columns are appended after the frozen ones, and the scripts assert every frozen field unchanged in every row | D3-476 freezes figures; a column beside them adds without altering
- D3-xxx | S48’s joined line sits in the Clerk’s sidecar as `with_party_divisions_119th` | The Clerk’s count is drawn and comes first (RF-5); a two-dataset spec copies a line no sidecar would otherwise hold
- D3-xxx | S46’s variant names the NHE release by its data year, "release with data through 2024", with no date | CMS’s page names no release date, and the 2024 comprehensive revision came out with the 2023 data, so "2024 release" would mislead
- D3-xxx | S45 takes a template, not a variant, for its release | S45 prints its years through `source_line_template`, and the template keeps them fitted to what it draws
- D3-xxx | The stale lines in the round 3 plan stay, each marked superseded with a pointer | The plan is the record of round 3’s sign-off; the current count lives in the round 4 plan
- D3-xxx | `research_v7_extract.py` carries v7-numbers’ qualification verbatim, run first in a scratch mirror | D3-910; a rerun must write what the file holds, and the mirror proved it before the repository run

### Requests

- **To the engineer.** Read `margin_columns`, `check_only_columns` and `source_line_columns` in the check (AX S8’s kit side). Only the two ACS margin sidecars carry them today. Other sidecars whose lines cover different measures (`census-spm-child-poverty`, `fred-unemployment-and-job-openings`, `census-cps-reported-voting`, `v7-stock-trading-ban`) can take `source_line_columns` once the check reads it; say so under Contracts and I add them.
- **To the editor and the engineer.** "When a margin is missing", above, for entry 14.74 and the README.
- **Closed:** the data lead’s RF-4, RF-5, RF-11, RF-11a and RF-20; D3-905; D3-910; the main session’s D3-835 wording. I told maker A (S43, S45, S46, S47, S48), maker B (S58, S59), the access reviewer, the engineer and the data lead.

### Tested

- Census Bureau API, 22:06 UTC, with the key from the environment, never printed or saved; a fixed-string search finds it in none of my scratch files. I read B25003 and B28002 again, plus DP04 and S2801 for the states and the nation. Every frozen count and count margin in both files equals the API’s. Every DP04 and S2801 share equals the file’s share rounded to one decimal. S2801’s counts equal B28002’s.
- Formula (6) and its ratio form, read in the Bureau’s handbook chapter 8 PDF. The `_formula` columns recompute from the stored counts and margins. No share needed the ratio form.
- S43’s claims under DP04’s margins: DC above half, and every state below half past its margin. The broadband state-against-nation test by both methods: 20, 22 and 9 by the formula; 21, 22 and 8 by S2801, with Nevada the one change.
- Treasury fiscaldata API, MTS Table 9 for September 30, 2026: all 20 frozen fiscal 2026 lines are equal. The 19 functions sum to the frozen total, positive functions sum to $7,566.3 billion and net outlays to $7,395.8 billion, and the two negative lines are as named.
- CMS: the historical page, highlights PDF, 2024 comprehensive revision summary and zip, with NHE2024.csv compared in all 715 cells. Crossref for the Health Affairs article (February 2026 issue).
- Census: the NRC release page and `comps_cust.xlsx` (SHA-256 prefix, last month September 2026); P60-289 Table 2 (header words; 61 all-races rows equal to the frozen file).
- Congress.gov API (proxy key): H.R. 7008’s titles and text versions. govinfo.gov: the engrossed text’s section headings and the photo identification section’s federal-election words.
- `research_v7_extract.py`: rerun unchanged in a mirror (only `v7-numbers.meta.json` differed, as expected), then rerun edited in the mirror (20 of 20 byte for byte), then rerun in the repository (`git status` and `git diff --stat` on the data folder unchanged).
- Each fix script asserts its checks before writing and wrote nothing on a rerun: `review_fix_round2.py`, `rf11a_published_margins.py`, `plan3_stale_lines.py`, `ledger_round2_fix.py`.
- The data check, `data_round0_build.py --check`, after every write: 111 tables, 0 faults.
- No em dash or U+2011 in any file I changed (asserted by each script).

### Not tested

- No chart drawn or built; the makers rebuild S43, S45 to S48, S58 and S59.
- How the Bureau computes DP04’s and S2801’s margins, and why they run up to 0.32 points from the formula (ledger claim 32).
- CMS’s release date for the data through 2024; its page names none (claim 31).
- The Treasury’s year-end report for fiscal 2026 (claim 33).
- ssa.gov and bls.gov were not retried.
- The map geometry (P7-219) is still waiting on the kit’s projection and the data check’s `.geojson` reading; untouched this pass.

### Files

Modified:
- `work/build/data/house-history-party-divisions.meta.json`, `clerk-house-current-party-breakdown.meta.json` (ST M3, RF-5)
- `work/build/data/census-acs-tenure-by-state.csv` and `.meta.json` (ST S5, RF-11, RF-11a; columns appended)
- `work/build/data/census-acs-broadband-by-state.csv` and `.meta.json` (AX S8, D3-905, RF-11a; columns appended)
- `work/build/data/treasury-mts-outlays-by-function.meta.json`, `cms-nhe-by-payer-four-groups.meta.json`, `census-nrc-completions-by-structure.meta.json`, `census-cps-median-household-income.meta.json` (ST S6)
- `work/build/data/frb-fomc-projections-unemployment.meta.json` (RF-20)
- `work/build/data/v7-numbers.meta.json` (RF-4, D3-835)
- `work/build/scripts/phase-3/research_v7_extract.py` (D3-910, the one qualification string)
- `work/handoffs/phase-3/20261112_Round-3-Data-Plan.md` (stale lines marked)
- `work/research/20261021_Research-Ledger.md` (P7-220, the new section, refresh rows, claims 31 to 33, change log)
- `work/handoffs/phase-3/20261112_Round-2-Research-Notes.md` (this section)

Not changed: `work/handoffs/phase-3/20261112_Round-4-Data-Plan.md`, whose counts are the current ones.

Scratch only: the folder above. Scripts are `fetch.sh`, `review_fix_round2.py`, `rf11a_published_margins.py`, `plan3_stale_lines.py`, `ledger_round2_fix.py`, `compare_margins.py`, `margin_compare_tests.py`, `mts_check.py`, `nhe_check.py`, `htmltext.py` and `xl_dump.py`. The `mirror-v7/` folder holds the v7 script's mirror run, `baseline/` holds the files as they stood before this pass, and `dl/` holds the downloads (acs-margins, acs-handbook, mts, nhe, nrc, p60, congress), each with its fetch log.
