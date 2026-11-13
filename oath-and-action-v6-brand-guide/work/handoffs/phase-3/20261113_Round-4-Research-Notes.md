# Round 4 research notes

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. Research lead (`oa-research-lead`), under `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`, the research lead's row and bullet. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/research/`. Written as I go, since the container can restart.

## Status

- 21:07 UTC. Resumed at 20:55 on the main session's word. Done since: the facts for 15.19 to 15.21 (20:56, told the main session); R-1 and IM-1 to IM-4 (four source line variants and row 11 of the Public Law 119-12 file, 20:59); R-2 (19 U.S. Code sections against the Law Revision Counsel's current release, 21:01 to 21:05: 18 read the same, 26 U.S.C. 7508A changed in parts the calendar does not draw; currency notes in four sidecars); R-3 (already item 29 of the V7.1 list; no new row). Derived files: none yet. The infographics maker's `maker_i_round4_derive.py` says it derives nothing; the cartographer's writes nothing; maker A has no derive script yet. Data check 125 tables, 0 faults.
- 20:48 UTC. Handed back to the main session before any derived file or ruling (f) landed; the watch is stopped. Still to do when resumed: the data check on each derived file as the makers write it (`scripts/r4_derived_check.py <root> 829d0db8`, then a recomputation for each file, then `data_round0_build.py --check`); the 15.20 facts once ruling (f) names the reforms (from `r4/reform-facts.json`, rechecked against the model); any V7.1 row round 4 raises; the data plan's status lines.
- 20:47 UTC. Data lead's rulings (a) to (c) read; (f) not yet posted. The reform facts table for all 50 reforms is ready in scratch (`r4/reform-facts.json`: 50 reforms, R-35 rejected; 126 route entries, 13 dated; 200 effect values, 38 beyond the seven codes, as the brief's section 14 counts). The common checker for changed data files (`scripts/r4_derived_check.py`, base commit 829d0db8) reads 0 changed tables so far. A watch on the makers' "derive" lines, the data folder and ruling (f) runs every 30 seconds.
- 20:44 UTC. Started round 4 after DR-269 (row 39 done, 20:43; see `work/handoffs/phase-3/20261113_Board-2-Apply-Research-Notes.md`, "Routine calls, DR-269"). Read the round 4 brief in full and the round 4 data plan. Baseline data check, `data_round0_build.py --check`: 125 tables, 0 faults. No derived file has landed yet: maker A's and the infographics maker's notes have no "derive" line. Data lead's ruling (f) not yet written. Preparing the 15.20 facts table for all 50 reforms from the model while I wait.

## Summary

## Data check over derived files

- **The data lead's ruling figures, rechecked from the frozen files (20:48 UTC), all equal:** S86, 90,837 local governments, 90,888 with the federal government and the states, special districts 39,555 (43.5 percent), county radius 0.277 of theirs; S87 and S88, the four regions recomputed from DP03 (189,377,193; 23,775,140; 95,362,515; 28,323,306; sum 336,838,154, the population), every gap past its approximate margin, the closest both kinds against none, 4,548,166 against 618,795; S90, shares 45.2341, 43.1987 and 11.5672 summing to 100.0000 and rounding to 45, 43 and 12, New York $31,917.51 and Idaho $11,060.40 per pupil; S94, 16 events on 13 days, 7 with a consequence stated and 9 without, every stored weekday equal to the calendar's; S95, 50 states, Mississippi 652 the highest and Massachusetts 96 the lowest.

- **Derived files as they land (21:07 UTC): none so far.** `maker_i_round4_derive.py` (the infographics maker) checks its specs' figures and writes no file: S89 to S95 draw files frozen in round 2 and S19's. `cartographer_round4_derive.py` writes nothing. Maker A has no `maker_a_round4_derive.py` yet. The checker (`scripts/r4_derived_check.py`, base 829d0db8) sees six changed tables, all mine (below), each with 0 faults.

## Requests answered

- **R-1 (data lead), S85's source line.** `v7-union-membership.meta.json` gains `source_line_variants.snapshot_in_grade`: "Source: U.S. Bureau of Labor Statistics, Union Members, 2025 (February 18, 2026), employed wage and salary workers, 2025, United States, as recorded in Oath & Action’s systems atlas, Who Do They Answer To? The 2025 average covers 11 months, since the October 2025 survey was not collected." For maker A.
- **IM-1, S89.** `govinfo-disaster-declaration-steps.meta.json` gains `in_force_in_grade`, the stored line without ", as in force November 9, 2026".
- **IM-2, S91.** `uscode-federal-trial-judges.meta.json` gains `seats_date_in_grade`, the stored line without ", seats as of September 30, 2025".
- **IM-3, S93.** `govinfo-pl-119-12-first-page.meta.json` gains `date_on_page`, the stored line without ", approved May 19, 2025".
- **IM-4, S93's margin words. Agreed: the margin holds two notes beside section 1.** Read again today from govinfo (PDF and HTML, fetched 20:58 UTC, logged with SHA-256 in `dl/pl119-12/fetch-log.tsv`): by word position on PDF page 1, eight margin lines "Tools to Address / Known / Exploitation by / Immobilizing / Technological / Deepfakes on / Websites and / Networks Act." sit above "47 USC 609 note.", and govinfo's HTML text gives them as two separate notes. `govinfo-pl-119-12-first-page.csv` gains row 11: part "Margin short title", printed text "Tools to Address Known Exploitation by Immobilizing Technological Deepfakes on Websites and Networks Act.", where "Right margin, beside section 1, above the U.S. Code note", what it tells "The law’s full short title, set in the margin beside the section that gives it". Row 10 is unchanged, so the draft's row numbers hold; the sidecar's notes say when and why row 11 came.
- Each variant is the stored line with one phrase cut, asserted by script (`scripts/r4_requests.py`): the stored line and every other key unchanged, the sidecar in its writer's format before and after, no em dash, U+2011 or straight quote; a rerun writes nothing. No repository script writes three of these sidecars; `research_round3_requests.py` sets keys in the judges' sidecar one by one, so a rerun keeps the variant.
- **R-2 (data lead), the in-force dates.** All 19 sections the four law files draw (the 18 the request lists and 5 U.S.C. 6103, the holiday list the calendar uses) were read today in the Office of the Law Revision Counsel's release (uscode.house.gov, "current through Public Law 119-138 (November 3, 2026)") and in the edition govinfo serves (the 2024 edition the files quote), 38 pages, each 200, logged in `dl/uscode-r2/fetch-log.tsv`. Compared word for word with spaces set aside (the two sites space enumerators and citations differently, and govinfo writes 66⅔ as "662/3"), **18 read the same: 42 U.S.C. 5170 and 5191; 28 U.S.C. 133, 134, 152, 631 and 633; 5 U.S.C. 552 and 6103; 2 U.S.C. 631; 31 U.S.C. 1102, 1105 and 1341; 26 U.S.C. 6072, 6081, 6651, 6654 and 7503.** Laws after 119-138: Congress.gov's API lists Public Laws 119-139 to 119-142 (latest action November 10, 2026); I read all four enrolled texts and none amends a drawn section (they amend 26 U.S.C. 7803, title 11's debt limits, Medicare wheelchair payment and a landmark). The Law Revision Counsel's classification tables list no law past 119-138.
  - **26 U.S.C. 7508A changed after the 2024 edition.** Its subsections (a) and (b), which the calendar file cites (`table_id`: 7508A(a)), read the same. Public Law 119-29 (July 24, 2025) added a new subsection (c): "The Secretary (after consultation with the Administrator of the Federal Emergency Management Agency) may, upon the written request of the Governor of a State (or the Mayor, in the case of the District of Columbia), apply the rules of subsections (a) and (b) to a qualified State declared disaster", and changed the mandatory extension from 60 to 120 days; Public Law 119-64 (December 26, 2025) added subsection (f). The file's qualification, "The IRS may postpone tax dates for a federally declared disaster (26 U.S.C. 7508A)", is true of (a) and no longer the whole rule. **For the data lead's ruling:** S94's grade line can keep "as in force on November 9, 2026" if its note reads, for example, "The IRS may postpone tax dates after a federally declared disaster or a significant fire, and, at a governor’s request, after a disaster a state declares (26 U.S.C. 7508A)"; I change the sidecar's qualification to match once you rule. No 2027 date in the file depends on 7508A.
  - Each of the four sidecars gains one note saying what was checked and when (`scripts/r4_currency_notes.py`, which asserts the report before writing; a rerun writes nothing).
- **R-3 (data lead), the loop and reform lists.** Already on the V7.1 list as item 29 (November 6): "Fourteen reforms list a loop that does not list them back, R-06 on R8 among them", `reforms[].loops` against `loops[].reforms`. Recounted by script today, the same: 15 pairs, 14 reforms, 12 loops, and no loop names a reform that does not name it back. By loop: B4 R-45; R3 R-37; R4b R-45; R6 R-40; R7 R-39; R8 R-06, R-38; R10 R-46, R-47; R12 R-03, R-50; R13 R-42; R15 R-49; R16 R-44; R18 R-48. No new row. For board 3, if Dustin wants it: add these 15 pairs to item 29's Where, so the editor has them in one place.

## Facts for Rules 15.19 to 15.21

For the systems designer, under the data lead's ruling (f). Written 20:56 UTC. Every value read by script (`scripts/r4_ch15_facts.py`, output `r4/ch15-facts.json` in scratch) from `work/extract/atlas-v7-data.json`, SHA-256 ef1028ac...c7f2, snapshot of October 15, 2026; the script asserts each structural point (f) states, and reruns its rule over all 20 closed loops: R4a alone passes. Quoted text is the atlas's as stored, with its straight apostrophes; the guide curls them in print. Delay words are the atlas's glossary: S under 2 years, M 2 to 10 years, L over 10 years.

### Rule 15.20: Reforms R-03 and R-04 on Loop R4a

Loop R4a, "Majorities draw maps that help them keep control": reinforcing, closed ("closed: every step is a numbered connection"), delay M. Loop grade text: "documented for C4 to C1 and D7 to C4; plausible for C1 to D7". Both lists agree: `loops.R4a.reforms` is R-03 and R-04, and no other reform names R4a. Its chain, with each variable's title (DR-265):

| Step | Connection | Name | From, to | Sign | Grade | Delay | Type |
|---|---|---|---|---|---|---|---|
| 1 | L42 | "Incumbent-drawn maps create safe seats" | C4 "Officeholders' control over election rules" to C1 "Seats with little electoral competition" | + | documented | M | causal |
| 2 | L55 | "Safe seats keep majorities in power" | C1 to D7 "Entrenched control of rule-setting institutions" | + | plausible | M | causal |
| 3 | L56 | "Durable majorities control maps and voting rules" | D7 to C4 | + | documented | S | causal |

R4a's `qualification`: "Courts and voters can interrupt the loop, as in Missouri, where the 2025 map is set aside for 2026 pending a November 3 referendum. Voters' residential sorting also makes seats safe without any map." (Missouri's Proposition A is V7.1 row 39's, DR-269; print it only under "As of October 15, 2026", as (f) says.) L56's own qualification also names the pending referendum.

| Field | R-03 | R-04 |
|---|---|---|
| Title | "Proportional elections in multi-seat House districts" | "Independent citizen commissions draw election maps" |
| Band | "rules" | "power to change the rules" |
| Targets | L42 (connection, "Incumbent-drawn maps create safe seats"); C1 (variable, "Seats with little electoral competition"); D7 (variable, "Entrenched control of rule-setting institutions") | L42 (connection); L56 (connection, "Durable majorities control maps and voting rules") |
| Loops it names | R4a, R10, R12 | R4a |
| Effects, as coded | DQ +L; GE ?; EP 0; EQ +S | DQ +M; GE 0; EP 0; EQ 0 |
| Qualifiers on effects | None: all four are bare codes | None: all four are bare codes |
| `effects_confidence` | "medium (representation); low (other)" | "high (fairness); medium (competition)" |
| Routes (route, who, feasibility, checked) | FS Federal statute, "Repeal the single-member mandate (2 U.S.C. 2c) and require ranked multi-winner counting", very low, Not checked; SS State statute, "State legislatures for their own chambers", low, Not checked; LOC Local, "City councils", medium, Not checked | BI State ballot, "Voters in initiative states", medium, Not checked; SS State statute, "Legislatures", low, Not checked; FS Federal statute, "Congress", very low, Not checked; CRT Court doctrine, "State courts enforcing fair-district clauses", medium, Not checked |
| Route notes | LOC only: "Cambridge, Massachusetts has counted this way since 1941; Portland, Oregon adopted it in 2022." | None |
| Problem evidence grade | documented | documented |
| Remedy evidence grade | plausible | plausible |
| Remedy evidence text | "Support comes from comparisons across countries and from simulations. Carey and Hix (2011) found in cross-national data that districts electing three to eight members improve proportionality without fragmenting governments. Main limitation: no U.S. congressional election has used the system, so there is no direct American test." | "Evidence that commissions reduce partisan bias comes from one descriptive study of the 2021-22 maps: Warshaw, McGhee and Migurski found less partisan bias in commission-drawn and court-drawn maps than in legislature-drawn ones. Evidence that commissions create more competitive seats is weaker. Main limitation: that study covers one redistricting cycle and uses descriptive measures." |
| `tradeoffs` | "Each member would represent a larger area, which weakens the tie to one place. In small states with one or two seats, little changes. Coalition-building can get harder when more parties win seats." | "Commissions correct bias more than they increase competition. A state that adopts one while its neighbors do not can lose seats, and that risk can drive retaliatory redraws elsewhere." |

Points for the systems designer and the data lead:
- **No route of either reform has a `checked` date**, so all seven print "Not checked" (Rule 15.16). R-04's status carries a check date (2026-10-15) and R-03's none; neither dates a route.
- **R-03's federal route stores an action in `who`** ("Repeal the single-member mandate (2 U.S.C. 2c) and require ranked multi-winner counting"); the other six routes of R-03 and R-04 name who acts. Printed under a "Who acts" label it would misread. Across the atlas the field is loose: of 126 entries, 89 distinct values mix actors ("Congress" 12 times, "Voters" 9, "Legislatures" 8), instruments ("Statute" 5, "Amendment" 3, "P.L. 119-75", "FTC consent orders") and five actions that open with a verb (R-03 FS, R-11 FS "Restructure the commission", R-17 FS and FA, R-47 SS "Legalize fusion"). One way: print the route name and the atlas's words as stored under a label such as "What it takes", or ask the data lead to rule. Proposed for board 3 as a V7.1 row (below).
- **"?" is the atlas's code for "direction uncertain"** (V7's effect codes: +L large positive, +M moderate positive, +S small positive, 0 no expected effect, -S small negative, -M moderate negative, ? direction uncertain). R-03's GE prints "?", never 0.
- R-03 also names R10 and R12, which list it back; only R4a holds all of its targets.

### Rule 15.19: Loop R1's steps

Loop R1, "Wealth and political influence reinforce each other": reinforcing, closed, loop grade "plausible", loop delay L. Reforms the loop lists: R-08, R-09, R-11, R-28 (not printed by 15.19).

| Step | Connection | Name | From, to (titles, DR-265) | Sign | Grade | Delay | Type | `qualification` |
|---|---|---|---|---|---|---|---|---|
| 1 | L01 | "Concentrated wealth funds more political spending" | A1 "Concentration of household wealth" to B1 "Money spent to influence politics" | + | well-supported | S | money | none |
| 2 | L02 | "Political spending can tilt policy toward donors" | B1 to E1 "Policy advantages for wealthy and organized interests" | + | plausible | M | money | "A 2016 field experiment (Kalla and Broockman) found congressional offices granted meetings more often to people identified as donors; affluent and middle-income Americans want the same policy about 90% of the time, so any tilt shows on the issues where they differ." |
| 3 | L03 | "Policy advantages add to wealth at the top" | E1 to A1 | + | well-supported | L | money | "CBO estimated that about 75% of the benefit of lower tax rates on capital gains and dividends went to the top 1% of households in 2019; asset prices also move the top share, so policy is one cause among several." |

Each step's `sign_meaning`: L01 "When wealth becomes more concentrated at the top, spending to influence politics tends to rise."; L02 "When more money is spent to influence politics, policy tends to favor wealthy and organized interests more."; L03 "When policy favors wealthy and organized interests more, wealth tends to become more concentrated at the top."

R1's `qualification`, printed once under the steps: "The loop runs on issues where wealthy donors' preferences differ from those of middle-income voters; on most issues the two groups agree, so its reach depends on the issue." Its `evidence_summary` names L02 as "plausible and the weakest". The three titles equal those (f) gives for the DR-267 code set.

### Rule 15.21: Connection L55

L55, "Safe seats keep majorities in power": C1 "Seats with little electoral competition" to D7 "Entrenched control of rule-setting institutions"; causal; sign + ("When safe seats increase, majority control tends to become more entrenched."); grade plausible, not contested; delay M; in loops R4a and R12. Its `qualification`, the sentence the correct plate rests on: "Seat safety is documented (Unite America's 2026 count, an advocacy source); the effect on how long majorities last relies on seats-votes analysis with no single estimate in this model." The model holds no strength, amount or estimate for L55: its record has no numeric field (keys: id, layer, from, to, polarity, type, delay, evidence, contested, loops, spine, name, plain, sign_meaning, qualification, mechanism, citation, counterevidence, summary_of). Its `citation`: "Unite America 2026 (W017) for seat safety; seats-votes analysis in the redistricting literature".

## V7.1 items raised in round 4

Proposed for board 3, not added to the list (a new row needs Dustin's word):

- **`routes[].who` mixes who acts, the instrument and the action.** Of the 126 route entries (89 distinct values), many name an actor ("Congress" 12, "Voters" 9, "Legislatures" 8, "City councils" 2), others an instrument ("Statute" 5, "Amendment" 3, "P.L. 119-75", "FTC consent orders", "Litigation"), and five an action that opens with a verb: R-03 FS "Repeal the single-member mandate (2 U.S.C. 2c) and require ranked multi-winner counting", R-11 FS "Restructure the commission", R-17 FS "Codify protections and reverse Schedule Policy/Career", R-17 FA "Rescind the OPM rule", R-47 SS "Legalize fusion" (`reforms[].routes[].who`). Proposed fix: keep `who` for the actor and move the instrument or action to the route's `note` or a new `instrument` field. Found reading 15.20's facts, 20:56 UTC; counted by script at 21:08.

Raised and already covered: the loop and reform lists (item 29, R-3 above); Missouri's pending referendum in R4a's and L56's qualifications, which 15.20's loop carries (row 39, DR-269).

## Routine calls

## Requests

## Tested

## Not tested
