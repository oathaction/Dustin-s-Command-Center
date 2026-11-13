# Round 3 maker A notes: structure

Oath & Action Edition 06, Phase 3, round 3, November 13, 2026. Maker A, briefed as a senior graphics editor who draws exact, quiet explainer diagrams of how institutions work. Brief: `work/handoffs/phase-3/20261113_Phase-3-Round-3-Brief.md`. Rows: maker "A" in `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`, rules 14.96 to 14.103 (coverage plan 3.11). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c155381-70e7-5490-bd84-f6f867d97cb7/scratchpad/phase-3/round-3/maker-a/`. Written as I go; the container can restart.

## Summary

- 00:5x. Started. Read `CLAUDE.md`, the round 3 brief, the kit README, the plan file's round 3 rows, data plan rows 86 to 93 with the sign-off's changes 4, 5 and 12 and its conditions, round 2's maker A notes, S62, `step-tracker` and entry 14.88, and the seven datasets with their sidecars.
- 01:2x. All seven forms, specs S66 to S72, entries 14.96 to 14.103 and the mind map sketch are written, on the engineer's R3-5 parts (`link`, `node`, `node_size`, `tree`) and under the data lead's rulings (a) to (d): no named mark on any of S66 to S72, inks and grade lines as ruled. Each spec builds PASS with the sweep, 0 faults. `maker_a_round3_derive.py` writes S71's joined table and checks every figure in my titles, notes and alts (23 checks, 0 failed so far; S71 and S72 checks being added). R3-A1 landed (the research lead's Ballotpedia publisher). Now: the review pass at 1440, 390, 296 and 256 px on both grounds and in grayscale, then the strict build and the quick guide check.

| Rule | Spec | Form ID | Status |
|---|---|---|---|
| 14.96 | S66 | process-diagram | form, spec, entry; build passes |
| 14.97 | S67 | decision-tree | form, spec, entry; build passes |
| 14.98 | S68 | who-decides | form, spec, entry; build passes |
| 14.99 | S69 | org-chart | form, spec, entry; build passes |
| 14.100 | S70 | hierarchy-tree | form, spec, entry; build passes |
| 14.101 | S71 | comparison-grid | form, spec, entry, derived table; build passes |
| 14.102 | S72 | roll-call-grid | form, spec, entry; build passes |
| 14.103 | sketch | mind map (reference) | sketch 2,4xx bytes, entry |

## Routine calls

- D3-xxx | Every structure form sets the words it prints once, by the spec's typography or, where the page's rows arrive unset, the guide's own (curly quotes, held dates), and measures what it prints | Parity: the page carries a grouped table's island raw and draws with no typography, so "Veterans' Affairs" and "January 6, 2021" printed differently on the page and in Node
- D3-xxx | Boxes holding words take the track ink, not the light fill (S67's answers, S70's territorial courts), with a context edge | The light fill measures 4.29 to 1 under the text's ink on Charcoal and 3.0 to 1 under the secondary ink on Newsprint; the track holds both above 4.5 on both grounds
- D3-xxx | S66 draws the five main steps numbered 1 to 5 on a heavy line (2 px, subject ink) with arrowheads, boxes with a 1 px subject edge; the five branches (petition in; White House review and guidance out of step 1; court review out of step 4; Congress out of step 5) in boxes with a 1 px context edge and context links, each with a line saying when it applies | Ruling (b), principle 1; the five branches are the file's rows with path "branch"
- D3-xxx | S66's desk sets the steps at the left and each step's branches stacked beside it, a step's way in first; under two 200 px columns one column, ways in above a step and branches below it, set in from the line | The spine stays one straight line at every width; a way in reads before the step it enters
- D3-xxx | S67 asks one further question under "No" ("Does it let a city set its own election rules?"), whose two answers rest on V7's local route: its instrument (ordinance, charter amendment or local practice) and Dillon's Rule states | Change 12: the last leaf says to check the state's home-rule law; a second question makes the tree teach chained questions without claiming which states are which
- D3-xxx | S67's third answer counts 31 states and the District of Columbia by a where that leaves DC out of its count | The words read "31 states and the District of Columbia"; the table keeps all 51 rows
- D3-xxx | S68 lays its two bands under column heads federal to private, one node style, names as V7 stores them with the words in parentheses set under the name; one label size for every name where all fit their 118 px column, else the tick size; under five such columns, one column a body with its level once over each run | Ruling (b); a name too long for its column drew no box at all (`node` returns null) until the size was chosen for all eight together
- D3-xxx | S68 draws the two lines of authority the ruling names, FERC to PJM and the legislature to the commission, as context arrows with no sign; the body a line leaves sits last in its column, so the line leaves into the gap under the band | Ruling (b), R3-6; Rule 15.5 draws authority with an open diamond in chapter 15, the ruling an arrowhead here (question Q-A1 below)
- D3-xxx | S69 draws House, then each kind of committee under a heading with its count (20 standing, 3 select, 4 joint, shared with the Senate), each committee a card with its subcommittees under it on the kit's indent tree, cards in as many 220 px columns as fit, each in the shortest | Ruling (b); a down tree of 27 committees and 109 subcommittees cannot fit 720 px; joint committees kept with their kind named, since the file lists them
- D3-xxx | S69 prints standing committees without "Committee on" (`labels.drop`) and collapses the file's double spaces in two names | The heading names the kind; the table and CSV keep every full name as stored
- D3-xxx | S70 draws the Supreme Court, the 12 regional courts of appeals as cards (each with its judgeships and the sum of its district courts'), and the Federal Circuit apart, named, with its note; each state or territory a row under its circuit naming its district courts with their judgeships, each name held to its count; territorial courts shaded with "not an Article III court" | Ruling (b) and change 5: a count at every node, so each level sums; 94 district boxes would run the drawing to about 2,300 px
- D3-xxx | S70 prints 673 Article III district judgeships (shared seats included) and four in the territorial courts, and no 677 total | The research lead's trace: the courts' 677 is 673 plus the four territorial judgeships
- D3-xxx | S71 joins V7's routes to the official requirements by my derive script (`usgov-v7-route-grid`, ledger row P7-209), rows in V7's order, with the texts and their reading date under each "What it takes" cell; the count as one series of bars in the subject ink with values | The brief's "each threshold cell with its official page and date"; ruling (b)
- D3-xxx | S72 sets each party as a row of squares (yes solid, no in 1.2 px outline, not voting in the light fill, vacant as a ghost outline), Democrats, independents, Republicans, vacant seats between the first party and the rest; the party's name and counts beside its squares where 20 a row fit, else above | Ruling (b); a block for each party keeps its count readable, and stacking parties keeps every name clear at 256 px
- D3-xxx | S72 counts vacant seats as the chamber's seats less members recorded: House 435 less 433, Senate 100 less 100, and names no vacant seat | The file lists no vacancies; which seats were vacant is not in it
- D3-xxx | Titles and notes spell out numbers under ten (S69 "three select committees", S70 "four", S72 "seven Democrats and one independent", "two of its 435 seats") | H06
- D3-xxx | D3-1097 (weight): S72's table groups by chamber and party with each vote counted, S69's by committee with its subcommittees listed, S70's by the court that hears appeals; every row stays in each CSV export | The engineer's `table.group` with A-E1 and A-E2, DR-249's pattern
- D3-xxx | S67's table drops its "Then" and "Year" columns | D3-1097; the drawing gives what each answer means, and the year sits in the CSV
- D3-xxx | The mind map sketch draws an invented city budget, one topic with four parts and an idea beside each, in 2,4xx bytes, 320 px with the 10 px inset | R3-9; the entry sends a reader to the process diagram, hierarchy tree or a table

## Requests to the engineer

- **A-E1, `kit.js` (`K.table_groups`), needed for S72's weight:** let `table.group.by` take a list of columns, the group's key their values joined with ", " (so `words` and `agg: "key"` read the joined key, such as "Senate, D"), groups in first-seen order after the spec's `sort`. S72's member-by-member table is 77,142 bytes of HTML (the plate 81,880, against 24,576 far-over and the 13,852 share); grouped by chamber and party, with `count` and `count_eq` columns for yes, no and not voting, it prints 5 rows and the CSV export keeps all 533 members, DR-249's pattern. A single column cannot split a party by chamber.
- **A-E2, optional, `kit.js` (`K.group_cell`):** `agg: "list"`, a field's non-empty values in the group joined with "; ", and `agg: "count_set"`, the rows whose field is non-empty. S69 would then group by committee and list each committee's subcommittees in one cell (27 rows in place of 136), and keep every name in the page's table.

## Requests to the data lead

- **Q-A1, S68:** ruling (b) draws the lines of authority with an arrowhead; chapter 15's Rule 15.5 draws authority with an open diamond and "decides". I followed the ruling; entry 14.98 cites Rule 15.5 for the no-sign, no-loop grammar. Say if S68 should take the diamond instead.

## Requests to the research lead

- **Dropped, D3-1097:** `clerk-house-committees-119-grouped` and `congress-hr5371-roll-calls-grouped` (with sidecars), which my derive script wrote for a few minutes and a snapshot commit caught, are gone: the kit's grouped table (A-E1, A-E2) reads the frozen files directly. Nothing waits on them. `usgov-v7-route-grid` stays, now with ledger row P7-209 from the script.

- **R3-A1, `ballotpedia-rcv-prohibitions-by-state.meta.json`:** its `publisher` reads "Ballotpedia. Secondary source". S67 draws this file with `v7-rcv-local-routes`, so its source line names both, and the kit's check for a spec of two datasets wants each publisher's words in the line, here "Ballotpedia. Secondary source", which no reader line says. Please set `publisher` to "Ballotpedia, a secondary source" (the words S07's printed line already uses), or tell me the words to print. S67 fails only this check until then.

## Tested

## Not tested

## Files
