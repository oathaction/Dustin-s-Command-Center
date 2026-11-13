# Round 3 maker A notes: structure

Oath & Action Edition 06, Phase 3, round 3, November 13, 2026. Maker A, briefed as a senior graphics editor who draws exact, quiet explainer diagrams of how institutions work. Brief: `work/handoffs/phase-3/20261113_Phase-3-Round-3-Brief.md`. Rows: maker "A" in `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`, rules 14.96 to 14.103 (coverage plan 3.11). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c155381-70e7-5490-bd84-f6f867d97cb7/scratchpad/phase-3/round-3/maker-a/`. Written as I go; the container can restart.

## Summary

- 00:5x. Started. Read `CLAUDE.md`, the round 3 brief, the kit README, the plan file's round 3 rows, data plan rows 86 to 93 with the sign-off's changes 4, 5 and 12 and its conditions, round 2's maker A notes, S62, `step-tracker` and entry 14.88, and the seven datasets with their sidecars.
- 02:2x. **Done.** Seven forms, specs S66 to S72, entries 14.96 to 14.103 and the mind map sketch; the editor's 15 word changes applied; every plate under 13,852 bytes (D3-1097); strict build exit 0 with no warning; quick guide check clean for my sketch and plates (its two failures are the cartographer's s-14-124 sketch). Open: Q-A1 to the data lead (S68's arrowhead against Rule 15.5's diamond), A-E3 optional to the engineer, and the data lead's sign-off.
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

- D3-xxx | The editor's first look applied as given: S66's chart note ("the steps the law sets for a rule") and note 1's comma; S67's title ("lets home-rule cities adopt it at the cost of state local government funds"); S68's note ("It shows who decides and carries no sign for which way the decision goes."); S69's "three" and "four" and "Budget and Ethics" | Editor, "Words for maker A", first look
- D3-xxx | S70's note 2 reads "Judgeships count the seats the law creates, filled or vacant, and leave out senior judges."; S71's note 1 drops "not how likely a change is"; entry 14.99's why says the question is about the body as a whole | W09, W11: no turn on "not"
- D3-xxx | S70's Federal Circuit card reads "12 judgeships." with its note, through `labels.card_sub_none`, in place of "0 in its district courts" | A court of appeals with no district courts has no sum to print
- D3-xxx | The node forms (S68 to S70) size each box at the width the kit's node fits it, and warn, so the build fails, wherever a node cannot hold its words | At 720 px S68 drew seven boxes of eight with every check passing (A-E3)

- D3-xxx | The editor's words pass of 02:12 applied, 15 of 15: S67's measure line comma; S68's title ("the rules behind it") and table word; S70's note 1 gloss of Article III courts; S71's title, note 1, alt and chart note; entries 14.96 (and its title, the editor's suggested "the steps an institution takes to decide"), 14.97, 14.98, 14.99 and 14.102 | Editor, "Words for maker A"; figure checks rerun, 35 of 35
- D3-xxx | S67's source line reads "reform profiles R-01 and reform R-02, the local route", with "reform" in lower case before R-02 as well | The editor's words ("reform profiles R-01 and R-02") print "and Reform R-02": the kit's chip adds its type word wherever the 16 characters before an ID lack it, and "reform" before R-02 keeps Rule 13.9's lower-case kind word

## Requests to the engineer

- **A-E1, `kit.js` (`K.table_groups`), needed for S72's weight:** let `table.group.by` take a list of columns, the group's key their values joined with ", " (so `words` and `agg: "key"` read the joined key, such as "Senate, D"), groups in first-seen order after the spec's `sort`. S72's member-by-member table is 77,142 bytes of HTML (the plate 81,880, against 24,576 far-over and the 13,852 share); grouped by chamber and party, with `count` and `count_eq` columns for yes, no and not voting, it prints 5 rows and the CSV export keeps all 533 members, DR-249's pattern. A single column cannot split a party by chamber.
- **A-E1 and A-E2: done** by the engineer (noted 01:3x); S69, S70 and S72 group their tables on them.
- **A-E3, optional, `parts.js` (`node`):** `node` fits its words at the box's inner width but sets them with `max` half a pixel wider, so a box sized by `node_size` at the same width can draw its words on one line fewer and show a blank line at its foot (S68's "Congress and the Department of Health and Human Services" at 720 px). And `node_size` at `max: w + 0.5` against `node` at `w` let a name fit the size and fail the node, which then drew nothing (S68 at 720 px lost that box until I sized at `w`). Fitting and setting at one width would close both. My forms now warn, so the build fails, wherever a node cannot hold its words.
- **A-E7, `kit.js` (`group_table`), small:** a grouped table's cells are printed without the spec's `typography`, so S72's list prints the record's "Davis (NC)" with its state again, "Davis (NC) (NC, Yea)". Setting group cells through `K.typeset`, as every other printed word is (D3-519), lets S72's two replace pairs, already in its spec, print "Davis (NC, Yea)" and "Golden (ME, Yea)".
- **A-E4, A-E5, A-E6: done** by the engineer; S68, S70 and S72 use them.
- **A-E4, `parts.js` (`link`), for MA-7:** an open-diamond end, Rule 15.5's mark (14 by 11 px, open, in the link's ink), as `arrow: 'diamond'`. S68 draws the diamond in its form until it lands.
- **A-E5, `kit.js` (`K.group_cell`), for MA-8:** `distinct: true` on `agg: "list"`, each value once in first-seen order, so S70's grouped table lists New York once, not four times.
- **A-E6, `kit.js` (`K.group_cell`), for MA-6:** on `agg: "list"`, `odd: <field>` lists only the rows whose field differs from the group's most common value (every row where no value is most common, as the Senate's two independents split), and `with: [fields]` adds those fields in parentheses after each, so S72 can print "Cuellar (TX, Yea)". Without it I write a derived column in my script, a 533-row copy for the research lead to check.
- **A-E2, optional, `kit.js` (`K.group_cell`):** `agg: "list"`, a field's non-empty values in the group joined with "; ", and `agg: "count_set"`, the rows whose field is non-empty. S69 would then group by committee and list each committee's subcommittees in one cell (27 rows in place of 136), and keep every name in the page's table.

## Requests to the data lead

- **Q-A1, S68:** ruling (b) draws the lines of authority with an arrowhead; chapter 15's Rule 15.5 draws authority with an open diamond and "decides". I followed the ruling; entry 14.98 cites Rule 15.5 for the no-sign, no-loop grammar. Say if S68 should take the diamond instead.

## Requests to the research lead

- **Dropped, D3-1097:** `clerk-house-committees-119-grouped` and `congress-hr5371-roll-calls-grouped` (with sidecars), which my derive script wrote for a few minutes and a snapshot commit caught, are gone: the kit's grouped table (A-E1, A-E2) reads the frozen files directly. Nothing waits on them. `usgov-v7-route-grid` stays, now with ledger row P7-209 from the script.

- **R3-A1, `ballotpedia-rcv-prohibitions-by-state.meta.json`:** its `publisher` reads "Ballotpedia. Secondary source". S67 draws this file with `v7-rcv-local-routes`, so its source line names both, and the kit's check for a spec of two datasets wants each publisher's words in the line, here "Ballotpedia. Secondary source", which no reader line says. Please set `publisher` to "Ballotpedia, a secondary source" (the words S07's printed line already uses), or tell me the words to print. S67 fails only this check until then.

## Tested

- `node work/build/chart-kit/oa-chart.mjs build` for S66 to S72 with the sweep (256 to 720 px) and PNGs at 1440, 390, 328 and 288 px pages (720, 358, 296 and 256 px drawings) on both grounds with grayscale captures: 7 of 7 PASS, 0 faults, 7 check files counted (last full run 01:4x after the last form change; S67, S68, S70 and S71 again with the sweep after the editor's words, PASS).
- Captures looked at, at twice size or as contact sheets: S66 to S72 at 1440 px Newsprint; at 358 px on both grounds (Charcoal in grayscale), 296 px Newsprint and 256 px Charcoal; S66 to S72 (less S69) at 1440 px Charcoal in grayscale; S69's top and S70's top at 1440 px; the mind map sketch on both grounds and Charcoal in grayscale. Fixes that came of it: S66's stretched step box, S67's follow-on question in its own box, S68's missing nodes (twice), S70's orphaned counts, S71's phone block, S72's party rows at 358 px.
- Page-to-Node parity on every drawing (the build's own check): failed for S69 and S72 until the forms set their words once (curly quotes, held dates) for both; passes.
- `python3 -I work/build/scripts/phase-3/maker_a_round3_derive.py --figures`: 35 checks, 0 failed, every figure in my titles, notes and alts against the data files (named in each spec's `notes_internal`); `--check`: the derived grid equals what the script computes.
- Words lint by script on the seven specs, eight entries and the sketch: no em or en dash, U+2011, straight quote in reader text, banned word or studio code; every "no", "not" and "never" read: the rest are vote words, the data lead's "not an Article III court" or the rule's own terms.
- `python3 -I work/build/scripts/phase-3/phase3_ch14_build.py --rounds 1,2,3`: 128 rules, 114 entries, 0 faults.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/guide-final.html` after the editor's words (02:2x): exit 0, no warning, 11,221,845 bytes; share per plate 14,478 for the 13 still to come. My plates: S66 9,165; S67 12,495; S68 8,695; S69 13,838; S70 9,049; S71 11,399; S72 10,512 bytes, each under 13,852 (D3-1097).
- `node work/build/scripts/phase-2/guide_check.js <scratch>/guide-check.html --quick --no-captures` on the strict build of 02:02 (run when fewer than two other guide checks were driving a browser; an earlier run of mine, started as a third, I stopped and do not count): exit 1 with 2 failures, both contrast in the cartographer's `s-14-124-sketch` ("Party B" at 2.65 to 1, at 1440 and 390 px); no line names `s-14-103-sketch` or any of S66 to S72. The editor's word changes after that build touch no sketch.

## Not tested

- Real screen readers, devices, print and 200 percent text; forced colors only through the kit's own checks (no `dataviz_check.js --kit` run this round).
- The data lead's sign-off of the drawings and of the grouped tables.

## Files

Created: `work/build/chart-kit/forms/process-diagram.js`, `decision-tree.js`, `who-decides.js`, `org-chart.js`, `hierarchy-tree.js`, `comparison-grid.js`, `roll-call-grid.js`; `work/build/chart-kit/specs/s66.json` to `s72.json`; `work/build/guide/entries/14-096.json` to `14-103.json`; `work/build/guide/specimens/s-14-103-sketch.html`; `work/build/scripts/phase-3/maker_a_round3_derive.py`; `work/build/data/usgov-v7-route-grid.csv` and `.meta.json` (by the script); this notes file.
Created and removed (a snapshot commit caught them): `work/build/data/clerk-house-committees-119-grouped.*`, `congress-hr5371-roll-calls-grouped.*`.
Written by running the engineer's generator, not by hand: chapter 14's JSON, its manifest, the example log and the `s-14-sNN.html` fragments.
Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c155381-70e7-5490-bd84-f6f867d97cb7/scratchpad/phase-3/round-3/maker-a/` (kit-out, kit-final, guide.html, captures, contact sheets, lint and parity tools).

## Sign-off fixes

November 13, 2026, after the data lead's "Sign-off, maker A" (MA-1 to MA-8, with Q-A1 answered: the open diamond).

| Item | Spec or file | Done |
|---|---|---|
| MA-1 | S66 title, alt | "and Congress and the President can strike the rule down"; the alt says a joint resolution Congress passes and the President signs, or that survives a veto |
| MA-2 | S66 branch, table, alt | White House review reads "Before steps 2 and 4, for significant rules"; the table's "Then" for it reads "Step 2, and again before step 4, the final rule"; the alt says review comes before the proposed and again before the final rule |
| MA-3 | S69 grade line | "Documented: the Clerk of the House’s committee list of November 3, 2026" |
| MA-4 | S69 note 2 | "The Clerk’s file lists the select subcommittee on January 6, 2021, as a committee, and the chart follows it." ("of its own" dropped to keep the plate within 13,852 bytes) |
| MA-5 | S70 title | "The 94 district courts try federal cases, an appeal goes to the court of appeals for the region, and the Supreme Court sits over all 13 courts of appeals." |
| MA-6 | S72 table; entry 14.102 | A column "Voted the other way or did not vote" names each member whose vote differs from their party's most common vote in that chamber, with state and recorded vote (A-E6, `odd` and `with`), both independents where they split: 20 names; the caption says every member not named voted with most of their party and the CSV file lists all 533; the entry adds the data lead's line |
| MA-7 | S68 lines, notes; entry 14.98 | Lines of authority end in Rule 15.5's open diamond through `K.parts.link(..., {arrow: 'diamond'})` (A-E4; my in-form diamond, drawn while it landed, is gone); note 1 and the chart note say a line ending in an open diamond is a line of authority; the entry takes the data lead's words |
| MA-8 | S70 table | A column "States and territories" lists each group's places once, in the drawing's order (A-E5, `distinct`) |

### Routine calls

- D3-xxx | S72's list prints the record's names, so two House names that carry their state ("Davis (NC)", "Golden (ME)") print it twice until group cells take the spec's typography (A-E7); S72's two replace pairs are set and take effect then | The record's words stay as stored in the data; the fix belongs in the printed words
- D3-xxx | S70's row for the Supreme Court as the court of appeals' destination lists every circuit's places, "All Federal judicial districts" among them | `distinct` reads the field as stored; the row is the Supreme Court's reach, and its 13 courts and 179 judgeships sit beside it
- D3-xxx | S69's words trimmed to hold 13,851 bytes after note 2: caption, measure line ("the U.S. House"), phone note, chart note, alt (drops "from Agriculture to Ways and Means") | D3-1097: every plate at or under 13,852

### Tested

- `oa-chart.mjs build` with the sweep and PNGs at 1440, 390, 328 and 288 px pages, both grounds, after the last change (S66 to S72 into `kit-signoff`): 7 of 7 PASS, 0 faults, 7 check files counted.
- `maker_a_round3_derive.py --figures`: 35 of 35 (S66's and S70's checked phrases kept: "five steps", "94 district courts", "13 courts of appeals"; S72's counts and names read from the file by script for MA-6, the 20 names equal the data lead's list).
- Words lint on the seven specs and eight entries: no dash, U+2011, straight quote, banned word or studio code.
- Strict build (`guide-final.html`): exit 0, no warning, 11,226,900 bytes; share per plate 14,092 for the 13 to come. Plates: S66 9,357; S67 12,495; S68 8,749; S69 13,851; S70 10,605; S71 11,399; S72 11,508 bytes.
- `phase3_ch14_build.py --rounds 1,2,3`, last run: 128 rules, 114 entries, 0 faults (an earlier run showed two faults, both the cartographer's sketch 14.124 mid-edit).
- Looked at: S68's diamonds at 1440 px Newsprint and 358 px Charcoal (drawn in-form first, then on the kit's part, its path read from the SVG); S72's and S70's grouped tables read from the build pages.

### Not tested

- The quick guide check after these fixes (no sketch changed since its run; the tables and words changed).
- Captures of every touched spec at all four widths by eye: S68 looked at; S66, S69, S70 and S72 checked by the build and their words read, not re-captured by eye.
