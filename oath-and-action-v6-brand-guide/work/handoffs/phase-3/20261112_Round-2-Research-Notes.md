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
- `work/research/20261021_Research-Ledger.md` (Part 7's "Round 2" section and "Round 4 datasets" section with P7-301 to P7-310; claims 27 to 30; change log lines)

Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/65b3d20e-985e-5fe9-b272-d7d01bd821cd/scratchpad/phase-3/round-2/research/` (reach logs; downloads with fetch logs under `dl/`; scripts `fetch.sh`, `freeze_round4.py`, `fix_stc_r1.py`, `fix_mspd_r2.py`, `recount_ch14.py`, `plan4_v7_check.py`, `row113_v7_read.py`, `check_maker_b_derived.py`, `stc_read.py`, `html_text_grep.py`, `htmltext.py`, `ecfrtext.py`, `xl_dump.py`).
