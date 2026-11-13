# Round 3 editor notes

Oath & Action Edition 06, Phase 3, round 3. Editor (`oa-editor`), November 13, 2026, under `work/handoffs/phase-3/20261113_Phase-3-Round-3-Brief.md` (the "Editor" paragraph binds). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c155381-70e7-5490-bd84-f6f867d97cb7/scratchpad/phase-3/round-3/editor/`. Written as I go; the container can restart.

The makers read the three "Words for" sections directly. Each row gives the file, the field, the old words and the new, and why. The owner applies them; once the main session tells me a maker has reported finished, I write straight into that maker's word fields (D3-669) and log each change here.

Words already settled, which every round 3 word field follows (from round 2):

- **One ink word in reader text (D3-914, D3-1042).** A mark the title names is "in the text’s ink"; other marks are "gray"; bands are "shaded"; stepped inks run "from closest to the page color to the strongest". No ink is called dark or light, since both swap on Charcoal. "Subject ink" stays a builders' word, in "For builders" lines only.
- **Rule 14.6's cases are cited, never restated.** An entry that needs the party tie, the sign case, the 5 percent share or the dashed total line writes "in the subject ink where Rule 14.6 sets ink in its place, as for a state" or "(Rule 14.6)", and gives no reason of its own.
- **The sketch caption (D3-709, D3-753, D3-791).** A sketch's visible caption is the first sentence of its entry's `sketch_alt`, and that sentence is the drawing's first `<desc>`, word for word. It says what the drawing shows and, for an avoid pair, why the better choice reads truer.

What round 2's words pass found most often, so you can write it right the first time (chapter 02's rule in brackets):

- A note names who acts: "The Clerk lists…", "CMS counts…", never "is counted" or "was published" with no actor (W02).
- Say what a thing is, with no "not X but Y", ", not", "rather than" or "never A, only B" turn, in notes, alts and entry `why` texts alike (W09, W10). A reason with "since" or "because" carries the same point.
- Numbers one to nine in words in notes, alts and entries; figures in labels, keys, tables and measure lines (H06). Months in words (H05). The true minus sign (H07).
- An atlas ID prints in its typed chip with the record's name the first time a field uses it, as "Issue I062 “Paperwork pushes eligible people off benefits”" (H11, Rule 13.9). Rule 13.9's kind words are Variable, Connection, Loop, Reform, Issue, Claim, Domain, Route, Rule change and Delivery case; a pathway or an atlas region has none, so name it in words ("the atlas’s pathway on electric and utility bills") and print no bare PW03 or region letter. A law by its number and plain name at first mention, as "Executive Order 14215 of February 18, 2025" (H12).
- Diagrams (R3-6): the table's words read in the reading order, each link named in plain words, as "Comment period, then final rule". Use the statute's or the record's own name for a step, and gloss a term of art in the notes the first time (H02), as S62 glossed a suspension of the rules.
- Parties in words, in the same ink as the text around them (H10); no word in a note or alt calls an ink red or blue for a party.
- A reference sketch's `sketch_alt` opens with what the drawing shows and its invented values; an avoid pair's opens with both drawings and why the better one reads truer, and the drawing carries "Illustrative data" (H03).

## Summary

- 00:50. Started. Read my role file, `CLAUDE.md`, chapter 02's writing rules, the round 3 brief and my round 2 notes. A rerun of `phase3_ch14_rules_build.py` before any change leaves `git status` clean. No round 3 spec, entry or sketch exists yet; the data lead's "Rulings" are in progress.
- 00:55. First look at the cartographer's entries 14.114 to 14.116, under "Words for the cartographer".
- 01:05. **The data lead's rulings (a) to (g) are in rules 14.1 to 14.14**, each case once, in `phase3_ch14_rules_build.py`, which rewrote `14-003`, `14-004`, `14-006`, `14-007`, `14-009` and `14-012`. No plate, drawing or caption changed. The cases and where each now lives are under "Rules 14.1 to 14.14" below. Entries cite these rules for them and never restate them.
- 01:05. **The opener no longer links a heading the page lacks.** With 14.114 written and the chapter build still on rounds 1 and 2, the opener linked group 15 to an id the page did not hold. The generator now reads which groups the last chapter build printed. See "Group lines 11 to 15".
- 01:11. First looks written for all three makers on what has landed (S65 to S69, S73, S74; entries 14.113 to 14.116 and sketch 14.113), as early items in the three "Words for" sections. The full words pass waits for the makers to report.
- 02:09. **Maker B's words pass, applied (D3-669); paused at 02:11 at the main session's word, since maker B reopens its files for the data lead's MB-1 to MB-9.** 34 changes in 13 files, written straight into its word fields and logged under "Words for maker B": S65, S73 to S77 and entries 14.94, 14.104 to 14.107, 14.110 and 14.112; the six sketch captions read and kept. All six specs pass the kit with the sweep. Maker B's figure check reads three sentences word for word that H06 and W02 changed; the new strings are under "Words for maker B" for the main session to pass on.
- 02:10. **Groups 11 to 15 now link from the opener**, after the chapter build took round 3 in, and **group lines 11, 13 and 14 are rewritten** against maker B's built entries (under "Group lines 11 to 15"). Group 12 waits for maker A, and group 15 for the cartographer.

## Routine calls

- D3-xxx | Rule 14.6 takes a third paragraph: a diagram or map that answers with its whole path or pattern names no single mark; the followed path in Charcoal at the subject weight and the branches in the context ink, one ink for every branch where the reader's case picks the path, and on a map only a place named as a point may take the red; spec row "A diagram’s path" | The data lead's principles 1 and 2 and ruling (a) for S79; one case to a paragraph, as CD R-S1 asked of this rule
- D3-xxx | Rule 14.6's 5 percent sentence becomes the area case: a named area takes Charcoal at any size (a part of a treemap, pie, donut or funnel, a region on a map, a node, a cell of a matrix, or a line or band whose width carries an amount), and a tall column in a short run keeps the share test; the spec row reads "A named area, or past 5 percent of the drawing" | Principles 2 and 3, RF-1's area rule (D3-916, D3-970); the rule said "would pass that share" for areas, and the ruling says outright
- D3-xxx | Rule 14.6's "Red never" line adds "or in a process" to "a step on a scale" | Principle 1: red on one step or branch would code it
- D3-xxx | Rule 14.6 adds the spec row "A total or national figure elsewhere": an open ring as a point, the first row set apart in a list, beside a map with its name and value, outside every region; the approved row for the line stays as worded | Ruling (b), "National figure", with the brief's call 4; ten map entries would otherwise each restate it
- D3-xxx | Rule 14.4 adds widths: a line or band whose width stands for an amount takes one unit across the drawing with a key, a line too thin at that unit drawn as a keyed hairline; related adds 14.110 | Principle 3 and ruling (b) for S73, S75 and S76; it is the same promise as a circle sized by area
- D3-xxx | Rule 14.3 adds the spec row "A state on a map": its code on or beside its shape, a leader for a small state, the full name in the table | Ruling (b), "State names", for every map
- D3-xxx | Rule 14.7 lets place include a party's own panel, and adds the spec row "Seats on a map" | Ruling (b) for S80 and S82, with its routine call under DR-58
- D3-xxx | Rule 14.9 takes a second paragraph on class maps (the three tests and the county case) and two spec rows; related adds 14.117 and 14.120 | Ruling (c): "a choropleth meets Rule 14.9 by three tests"
- D3-xxx | Rule 14.12's list of reasons to redraw adds marks too small or too crowded to read, as dots on a dot map, and each dot then stands for a larger count | The routine call for S83's phone drawing; the rule's "only when it must" list would otherwise leave S83 and S82 outside it
- D3-xxx | Rule 14.5 takes no case for four classes on steps 1, 3, 4 and 5 | The heat table (S37, board 1) draws four classes on steps 2 to 5, so the step choice stays per spec as ruling (b) gives it
- D3-xxx | No plate, drawing or caption of rules 14.1 to 14.14 changes for these cases | Each case is words in the rule and its spec rows; the plates' findings and inks still hold
- D3-xxx | The opener links a group's question only when its first entry exists and the last chapter build printed its heading | Round 3's entries land before the chapter build takes round 3 in; at 01:00 the opener linked `#group-14-15`, which the page lacked
- D3-xxx | Group lines 12 and 15 stand until their entries land | The brief: change a line only where the built entries make it untrue or unclear
- D3-xxx | Group 11's line reads "Funnels, cohort charts and survival curves follow people through a process and show at which stage, or how soon, they leave it." | A cohort chart and a survival curve show how soon people leave (14.94, 14.95), and "people move … in funnels" put the people inside the chart
- D3-xxx | Group 13's line reads "Networks, matrices and arc diagrams show who is connected to whom, with a width or a shade for each link’s amount or count." | S74's note says a matrix cell's count "gives no measure of their strength", so "how strongly" was untrue for the matrix
- D3-xxx | Group 14's line reads "Sankeys, alluvial charts and flow maps show where money or people go, and the table gives every flow’s amount. A journey map follows one person through a public service, step by step." | S76's note leaves $1.5 million "unaccounted for", so "every flow accounted for" was untrue; the journey map, the group's one core form, was missing from its line
- D3-xxx | The editor writes maker B's words pass straight into its word fields: 34 changes in S65, S73 to S77 and entries 14.94, 14.104 to 14.107, 14.110 and 14.112 | D3-669; the main session reported maker B finished
- D3-xxx | S65's note on the procedural reason quotes CMS's metric 5c and 5b words and gives no example; note 2 adds that a state that held its procedural terminations reports them as pending | The main session's relay of both CMS sidecars: CMS gives no example, and its note on 5d says so
- D3-xxx | S74 prints the research lead's new sidecar line, "snapshot of October 15, 2026, United States.", copied exactly | RB3-R3 (H04: the date once)
- D3-xxx | Maker B's entries cite Rule 14.4 for widths and Rule 14.6 for the path, a named arc, ribbon or flow, and the party tie, in place of restating them (14.104, 14.106, 14.107, 14.110, 14.112) | The rulings' cases now live in those rules
- D3-xxx | Where a maker's figure check reads a sentence word for word and H06 or W02 changes it, the editor makes the change and gives the maker the new string through the main session | H06 binds; the figures stay, and the check keeps reading the same facts
- D3-xxx | Other atlas source lines that print October 15, 2026 twice stay as they are this round, and the change goes to board 2 as an item (under "Requests", to the main session) | The main session's word: changing them would move round 0 to 2 specimens

## Group lines 11 to 15

Each line is read against the entries as they land, and changes only where a built entry makes it untrue or unclear. Status at 02:10, with maker B's entries and 14.113 to 14.116 in:

| Group | Line | Status |
|---|---|---|
| 11 Behavior | Funnels, cohort charts and survival curves follow people through a process and show at which stage, or how soon, they leave it. | **Rewritten.** The old line, "People move through a process in funnels, cohort charts and survival curves, which show where they leave it.", left out how soon: 14.94 and 14.95 measure time since a start |
| 12 Structure | Process diagrams, decision trees and who-decides diagrams show who decides and how a decision moves. | Waiting for 14.96 to 14.103 |
| 13 Relationships | Networks, matrices and arc diagrams show who is connected to whom, with a width or a shade for each link’s amount or count. | **Rewritten.** The old line ended "and how strongly", which S74's note contradicts; 14.104 and 14.106 draw amounts and counts as widths, 14.105 counts as shades |
| 14 Flow | Sankeys, alluvial charts and flow maps show where money or people go, and the table gives every flow’s amount. A journey map follows one person through a public service, step by step. | **Rewritten.** The old line said "with every flow accounted for", and S76 leaves $1.5 million "unaccounted for"; 14.110, 14.111 and 14.113 each give every flow's amount in the table; the journey map (14.112) was missing |
| 15 Maps | A map appears when the place answers the question, and it names its places in words as well as color. | 14.114 to 14.116 agree (codes in every square or circle, the table naming every state). To check against 14.120 and 14.122, where the map names no county and the table does, and Rule 14.3's new row |

**The opener (D3-452).** A group's question links to its heading only once the chapter build prints that heading. Round 3's entries now land before `phase3_ch14_build.py` takes round 3 in (its default is rounds 1 and 2), so an entry file alone no longer means the heading exists: at 01:00 the opener linked group 15 to `#group-14-15`, which the page did not hold. The generator now also reads the groups the last chapter build printed (`work/build/guide/chapters/14-data-visualization.json`), so it never links a heading the page lacks. **Done at 02:09:** the chapter build's default now takes round 3 in (DR-253), so I ran it, then the rules generator, then the chapter build again; the opener links groups 11 to 15, and every `#group-14-N` link in the strict build lands on an id. Each later rerun keeps it so.

## Rules 14.1 to 14.14

The data lead's rulings (`20261113_Round-3-Data-Lead-Notes.md`, "Rulings", "How the test runs this round" and (b) to (c)) add these cases. Each now sits once in its rule; an entry that needs one cites the rule by number, as "(Rule 14.6)", and gives no reason of its own. **Makers and the cartographer: please cite, never restate.**

| Rule | Case the ruling adds | Where it now sits | Ruling |
|---|---|---|---|
| 14.6 | A diagram or a map that answers with its whole path or pattern names no single mark; in a process the followed path takes Charcoal at the subject weight and the branches the context ink; where the reader's own case picks the path, as in a decision tree, every branch takes one ink; on a map only a place named as a point, such as a town, may take the red | Third paragraph (new), spec row "A diagram’s path", builders line ("a diagram or map that names no mark sets neither") | Principles 1 and 2; (a) for S79 |
| 14.6 | A named area takes Charcoal at any size: a part of a treemap, pie, donut or funnel, a region on a map, a node, a cell of a matrix, or a line or band whose width carries an amount, such as a flow | Last paragraph; spec row "A named area, or past 5 percent of the drawing" | Principles 2 and 3 (RF-1's area rule, D3-916); (a) for S65, S75, S76 |
| 14.6 | Red never codes a step in a process | "Red never" sentence and spec row | Principle 1 |
| 14.6 | A total or national figure as a point (an open ring), in a list (the first row, set apart) and on a map (beside it with its name and value, outside every region) | Spec row "A total or national figure elsewhere", beside the approved line row | (b) "National figure", the brief's call 4 |
| 14.4 | A line or band whose width stands for an amount takes one unit across the whole drawing, with a key; a line too thin to see at that unit draws as a hairline the key names | Second paragraph; spec row "Widths" | Principle 3; (b) for S73, S75, S76 |
| 14.3 | A state on a map takes its two-letter code on or beside its shape, with a leader for a small state, and its full name in the table | Spec row "A state on a map" | (b) "State names" |
| 14.7 | Party by place includes a party's own panel; seats on a map take one panel per party, named with the seats it won, each seat filled in its winner's panel and its margin in gray steps | First paragraph ("or in its party’s own panel"); spec row "Seats on a map" | (b) for S80 and S82 |
| 14.9 | A class map ranks survey figures too: each class at least as wide as the widest margin drawn, places two classes apart differing by more than their gap's margin, a note counting places whose interval crosses a class line, and, where small places' margins outrun any class, a note saying how many could fall in another class with no place set above another unless its gap passes | Second paragraph (new); spec rows "Classes on a map" and "A class map’s note"; related adds 14.117 and 14.120 | (c) |
| 14.12 | A phone drawing may change when marks grow too small or too crowded to read, as dots on a dot map do, and then each dot stands for a larger count | First paragraph; spec row "A new form" | (b) and the routine call for S83; (f)'s small tiles on S82 |

Left out on purpose: ruling (b)'s four sequential steps 1, 3, 4 and 5 for four classes. Rule 14.5 does not take it as a general case, because the heat table (S37, a board 1 drawing) draws its four classes on steps 2 to 5; the choice stays per spec, as the ruling gives it.

Weight: see "Tested".

## Words for maker A

### First look (01:11): S66 to S69 as drafted

Your words are still landing, so these are early; the full pass follows when you report. Apply what still fits.

| File | Field | Old words | New words | Why |
|---|---|---|---|---|
| S66 | chart_notes.0 | Numbered boxes on the heavy line are the steps every rule takes, in order. | Numbered boxes on the heavy line are the steps the law sets for a rule, in order. | Note 2 says some rules skip notice and comment, so "every rule takes" is untrue for steps 2 and 3 |
| S66 | notes.0 | Executive Order 14215 of February 18, 2025 sends | Executive Order 14215 of February 18, 2025, sends | A date inside a sentence closes with a comma after the year |
| S67 | title | Ohio’s ban leaves home-rule cities an opening at a price, | Ohio’s ban lets home-rule cities adopt it at the cost of state local government funds, | "At a price" holds the fact back (W06); the leaf and S07's note say what the price is |
| S68 | notes.0 | It says who decides, not which way. | It shows who decides and carries no sign for which way the decision goes. | W09, no "not" turn; the chart note's "it carries no sign" uses the same word |
| S69 | title | 20 standing committees and 3 select committees | 20 standing committees and three select committees | H06: one to nine in words in a title or note |
| S69 | alt | 3 select committees and 4 joint committees | three select committees and four joint committees | H06 |
| S69 | notes.0 | Two standing committees, the Budget and Ethics, have no subcommittees | Two standing committees, Budget and Ethics, have no subcommittees | "The Budget" reads as the budget itself |

Read and kept so far: S66's title, grade line, measure line and note 2; S67's notes and leaf words; S68's title, measure line, chart note and alt ("Congress and the Department of Health and Human Services" is one body in the atlas's record, for LIHEAP); S69's measure line.

## Words for maker B

### First look (01:11): S65, S73 and S74 as drafted

Your words are still landing, so these are early; the full pass follows when you report. Apply what still fits.

| File | Field | Old words | New words | Why |
|---|---|---|---|---|
| S65 | table.columns.1.label | People | Renewals | The measure line says a person due in two months counts twice, so the column counts renewals |
| S65 | notes.0 | Pending renewals are set apart: the states had not decided them three months after they were due. | Pending renewals sit apart, since the states had not decided them three months after they were due. | W06: the colon holds the reason back; W02 |
| S65 | notes (new) | (none) | A note that says, in CMS's words from the sidecar, what ending "for a procedural reason" means, such as a renewal form not returned | H02: the title's key term, and the reader question's "cut off for paperwork", need a plain gloss at first use |
| S73 | labels.key_hairline | A link under {v} draws 1 pixel wide | Under {v}: a hairline | A pixel is a builder's measure; a key line may be a phrase (chapter 02's scope) |
| S74 | title | and all 7 authority connections start there. | and all seven authority connections start there. | H06 |
| S74 | notes.0 | a count says how many connections join two regions, not how strong they are. | a count says how many connections join two regions and gives no measure of their strength. | W09, no "not" turn |
| S74 | source_line | …as of October 15, 2026, United States. Snapshot of October 15, 2026. … | (a request to the research lead's sidecar line, if it is theirs) | The date prints twice; H04's order wants it once |

Read and kept so far: S65's title, grade line, measure line and alt; S73's title, notes and alt; S74's measure line, note 2 and region names.

### Words pass, maker B finished (D3-669), 02:04 to 02:11 UTC

**Status, 02:11 UTC: paused at the main session's word.** The data lead held S65, S73, S76 and sketch 14.108 and asked for MB-1 to MB-9, so maker B reopens its files. All 34 changes below were already applied before the pause, and none is half done; the two fixes the main session sent are among them (S74's `source_line`, and S65's `notes.0` with `notes.1`). **Maker B: these are now in your files; keep them as you work MB-1 to MB-9, or tell me which one an MB item replaces.** I write nothing more into maker B's files until the main session resumes me after maker B reports again; then I read every field it changed.

The main session told me maker B had reported finished, so I wrote these straight into its word fields and log each here. I read every word field of S65 and S73 to S77, entries 14.93 to 14.95 and 14.104 to 14.112, and the six sketch captions with their first `<desc>`, by `words/words.py dump` (scratch) and then by hand, with its lint. `words.py apply` fails a change whose before-text is not found once in its field or whose after drops a figure (a figure moved or spelled out under H06 is marked so), proves by parsing that no other field moved, and edits the hand-laid specs (S65, S75 to S77) in their own text. No form, data, figure, grade line or kit file changed. S73 follows the data lead's RL-3a as written, S77 the research lead's 273.2(i) reading, S74 the research lead's new sidecar line, and S65's note on the procedural reason CMS's own terms, as the main session relayed (CMS gives no example, so the note names none).

| File | Field | Before | After | Why |
|---|---|---|---|---|
| S65 | notes.0 | A renewal ended for a procedural reason when the state stopped coverage for what CMS calls a procedural or administrative reason, with no finding that the person no longer qualified. A finding that the person no longer qualified counts as found ineligible. | CMS counts two kinds of ending: coverage “terminated for a procedural or administrative reason”, which this chart calls ended for a procedural reason, and people “determined ineligible” on the return of a renewal form, which it calls found ineligible. | H02 in CMS's own words (metrics 5c and 5b, both sidecars' notes), in place of a gloss CMS does not give and two negatives (W09) |
| S65 | notes.1 | since the states had not decided them three months after they were due. | since the states had not completed them three months after they were due; a state that held its procedural terminations reports them as pending too. | CMS's note on metric 5d, quoted in both sidecars: held procedural terminations count as pending |
| S65 | notes.2 | before every state had finished, | before every state had finished its renewals, | "Finished" left its object out |
| S73 | notes.2 | The 51 state party committees include the District of Columbia’s. Drawn here are transfers, | The 51 state party committees include the District of Columbia’s, and the download lists each with its transfers. Drawn here are transfers, | The two sentences on the state parties sit together |
| S73 | notes.2 |  The download lists each of the 51 state party committees with its transfers. The Trump |  The Trump | Moved up, beside the sentence it belongs with |
| S73 | chart_notes.0 | Both committees are drawn alike, in one ink, on one scale of widths. | The chart draws both committees alike, in one ink, on one scale of widths. | W02 |
| S74 | notes.1 | All seven start in governing institutions and fill three cells alone, each drawn with an outline. | All seven start in governing institutions and are the only connections in three cells, which the grid draws with an outline. | "Fill three cells alone" read as each filling a cell by itself |
| S74 | chart_notes.0 | Each filled cell is shaded by its count, with the count printed in it; the more connections, the stronger the shade. Lines of authority, which carry no sign, fill three cells drawn with an outline and no shade. | A filled cell’s shade grows stronger with its count, which is printed in it. Lines of authority, which carry no sign, are the only connections in three cells, drawn with an outline and no shade. | W02; W10, no "the more, the stronger" pair; the same reading of the three cells as note 2 |
| S74 | source_line | Source: Oath & Action’s systems atlas, Who Do They Answer To?, model connections counted by region, as of October 15, 2026, United States. Snapshot of October 15, 2026. Counted by Oath & Action. | Source: Oath & Action’s systems atlas, Who Do They Answer To?, model connections counted by region, snapshot of October 15, 2026, United States. Counted by Oath & Action. | The research lead's new sidecar line (RB3-R3), copied exactly; the date prints once (H04) |
| S74 | alt | from 1 to 7 each, | from one to seven each, | H06 |
| S75 | notes.0 | The search took every bill of the 119th Congress with a title, official, short or popular, that names “pharmacy benefit manager” or “PBM”, in the Library of Congress’s files of November 11, 2026: 10 House bills and 8 Senate bills. | We searched every bill of the 119th Congress in the Library of Congress’s files of November 11, 2026 for a title, official, short or popular, that names “pharmacy benefit manager” or “PBM”, and found 10 House bills and eight Senate bills. | W02, name who searched; H06 |
| S75 | chart_notes.0 | The widest arcs are drawn first, so narrow ones stay in view. | The chart draws the widest arcs first, so the narrow ones stay in view. | W02 |
| S75 | labels.key_hairline | An arc of one or two members draws at the width of three. | An arc of one or two members takes the width of three. | "Draws" with no object is a builder's verb |
| S76 | notes.0 | No dollar received is traced to a dollar spent: the node holds the committees of all 1,926 House candidates together, primary losers included. | The chart traces no dollar received to a dollar spent, since the node holds the committees of all 1,926 House candidates together, primary losers included. | W02; W06, the reason with "since" in place of a colon |
| S76 | notes.2 | Transfers between a candidate’s own committees are netted; on the way out | The chart nets transfers between a candidate’s own committees; on the way out | W02 |
| S76 | labels.key_hairline | A band under {v} draws 1 pixel wide. | A band under {v} shows as a hairline. | A pixel is a builder's measure; Rule 14.4 calls it a hairline |
| S77 | title | and at most 7 for a household | and at most seven days for a household | H06 |
| S77 | measure_line | and how long households wait is not measured here | and the chart measures no household’s wait | W02 |
| S77 | notes.1 | It sets no day for the interview, which may be held by phone, and it lets a state waive the interview in some cases. | It sets no day for the interview, which a state may hold by phone or, in some cases, waive. | W02; one clause for the interview |
| S77 | notes.2 | A household on the expedited branch is still interviewed within the 7 days. | The state still interviews a household on the expedited branch within the seven days. | W02; H06 |
| S77 | chart_notes.0 | The path every application takes is drawn in the text’s ink. The expedited branch is gray. | The main path is in the text’s ink, and the expedited branch is gray. | An expedited application leaves the path after its first step, so "every application takes" was untrue; W02 |
| S77 | table.columns.1.label | Who takes it | Applies to | The column holds which applications take a step ("Every application"), and "Who takes it" read as a person beside "Who acts" |
| 14-094 | rule.0 | Draw one line a group, the years since its start across and the share still enrolled up from 100 percent, and name | Draw one line for each group, with the years since its start along the bottom and the share still enrolled up the side, from 100 percent at the start, and name | W01: the axes said aloud; the lines fall from 100 percent |
| 14-104 | rule.0 | in one linear unit for the whole drawing, with a key of widths; a link too narrow to see draws one pixel wide, and the key says so. | in one linear unit for the whole drawing, with a key of widths (Rule 14.4). | Rule 14.4 now holds widths and the keyed hairline; the entry cites it |
| 14-104 | rule.0 | money spent to elect a candidate takes the party-mark ink, never red or blue (Rule 14.7). | money spent to elect a candidate takes one neutral ink for every party, with no red or blue (Rules 14.6 and 14.7). | "Party-mark ink" is a builder's name (D3-914); Rule 14.6 holds the tie, 14.7 the ink |
| 14-105 | rule.0 | an outline and a key entry of its own, never a step of the scale. | an outline and a key entry of its own, apart from the scale’s steps. | W09 |
| 14-106 | rule.0 | in one linear unit with a key of widths. | in one linear unit with a key of widths (Rule 14.4). | Cite the rule that holds widths |
| 14-106 | rule.0 | in the text’s ink with every other arc gray. | in the text’s ink with every other arc gray (Rule 14.6). | Rule 14.6 holds a named line whose width carries an amount |
| 14-107 | rule.0 | with the one the title names in the text’s ink. | with the one the title names in the text’s ink (Rule 14.6). | The same |
| 14-110 | rule.0 | with a key band, so the bands sum at the node. | with a key band (Rule 14.4), so the bands sum at the node. | Cite the rule that holds widths |
| 14-110 | rule.0 | say in a note that no dollar received is traced to a dollar spent. | say in a note that the chart traces no dollar received to a dollar spent. | W02, as S76's note now says it |
| 14-112 | rule.0 | say in the measure line that waits are not measured, | say in the measure line that the chart measures no wait, | W02 |
| 14-112 | rule.0 | The path every person takes is in the text’s ink and a branch is gray, with no red, since red on a step would code it. | The main path is in the text’s ink and a branch is gray (Rule 14.6). | Rule 14.6 now holds a diagram's path and red on a step; the entry cites it, never restates it |
| 14-112 | why.text.0 | A journey map follows one person rather than an office, so | A journey map follows the person who applies, so | W09, no "rather than" turn |

Read and kept: every title (S74's "32 of them" I kept because maker B's figure check reads it word for word; the data lead's MB-6 now changes it to "32 of the connections", which I agree reads better, since "them" follows "pairs"); S65's title, grade line, measure line, alt, chart note and table words; S73's title, measure line, notes 1 and 2 and the RL-3a note's words, alt and node names; S74's grade line, measure line, notes 1, 3 and 4, alt and region names, which are the atlas's own; S75's title, measure line, notes 2 and 3, alt and key words; S76's title, measure line, note 2's figures, alt, chart note, names and the sidecar's source line; S77's grade line, notes 1 and 3's second sentence, alt and step words; entries 14.93, 14.95, 14.108, 14.109 and 14.111 whole, and every title, use_when, use_instead and builders line of the twelve; all six sketch captions, each its drawing's first `<desc>` word for word (`words.py desc`), so no `<desc>` changed.

**For the main session, to maker B (three strings in its figure check).** `maker_b_round3_derive.py --figures` now reports 3 faults, each a sentence it reads word for word that H06 or W02 changed; no figure moved. Please have maker B change its `want()` strings to: S75 "10 House bills and eight Senate bills"; S77's title "at most 30 days from an application to a decision, and at most seven days for a household with very little income or cash"; S77's note "interviews a household on the expedited branch within the seven days".

**For maker B, two small things outside word fields (yours to take or leave):** S65's table prints the share of renewals due as a decimal, "0.9368", under "Share of renewals due, 0 to 1", while the drawing prints percents; `percent:1`, as `formats.share` already uses, would read the same in both. Sketch 14.94's value axis labels 100%, 80, 60, 40 and 0, with no 20.

## Words for the cartographer

### First look (01:11): entry 14.113 and its sketch

Read and kept: 14.113's title, rule, use_when, use_instead, why and builders, and the sketch's caption, which is its first `<desc>` word for word (2,664 bytes). One suggestion: the caption can say the values are invented, as "Curved lines run from one place to four others over a plain map, each as wide as the invented number of people who moved along it, with a key of two widths." The drawing already carries "Illustrative data", so this one is yours to take or leave; if you take it, change the `<desc>` too.

### First look (00:55): entries 14.114 to 14.116

Read against S07, S12 and S16 as board 1 approved them, and again at 01:05 against the data lead's rulings, which now sit in rules 14.1 to 14.14 (above). The cartographer applies these.

| File | Field | Old words | New words | Why |
|---|---|---|---|---|
| 14-114 | rule.0 | solid squares for the status the title names, open squares for a partial case and gray squares for none, each named in the key with its count. | solid squares for the status the title names, open squares for a partial case and gray squares for none, each named in the key. | S07's key gives no count for its first class ("Bans it in all elections, with the year it became law"), and S07 is a board 1 drawing that changes in placement only, so the entry says what its specimen shows |
| 14-114 | why.text.0 | large and empty states take most of the page | large, thinly settled states take most of the page | "Empty" overstates (W20) and reads as a judgment of the place |
| 14-115 | rule.0 | Give each state one square holding a flat arrow whose length follows its shift on one scale across the map, | Give each state one square holding an arrow that points the way the measure moved, its length set by the shift on one scale across the map, | "Flat arrow" leaves the reader to guess what flat means; S12's arrows point the way the margin moved |
| 14-115 | rule.0 | Name the direction in words in the key, as “toward the Republican nominee”, and draw every party in neutral ink (Rule 14.7). | Name the direction in words in the key, as “toward the Republican nominee”, so no color stands for a party (Rule 14.7). | S12 draws no party mark: its arrows carry the direction and the key's words name it |
| 14-115 | rule.0 | Set the national figure beside the key with its own label and arrow, never as a square, and frame | Set the national figure beside the key with its own label and arrow (Rule 14.6), and frame | Rule 14.6 now holds the national figure on a map ("beside it with its name and value, outside every region"); the entry cites it, with no "never" turn (W09) |
| 14-116 | rule.0 | and name each one by its code, inside the circle where it fits and beside it, with a leader where needed, where it does not. | and print each state’s code inside its circle, or beside it with a leader where the circle is too small to hold it (Rule 14.3). | Two "where" clauses in a row; one plain sentence says the same, and Rule 14.3 now holds a state's code on a map |
| 14-116 | rule.0 | Mark the national rate on the step key with its label, apart from the circles on the map. | Mark the national rate on the step key with its label (Rule 14.6). | Rule 14.6 holds the national figure on a map; cite it |
| 14-116 | why.text.0 | A shaded state lets its land speak for it, so a large, empty state outweighs a small, crowded one. | On a map of shaded states, land sets how much of the page each state takes, so a large state with few people outweighs a small, crowded one. | "Lets its land speak for it" is a figure of speech a listener has to decode (W01); "empty", as in 14.114 |

Read and kept: the three titles; 14.114's use_when, use_instead and builders; 14.115's phone paragraph (Rule 14.12) and why; 14.116's use_when, use_instead and builders.

**For S16's move to the 2024 outlines (R3-4):** its note 4 names the old file, "Map: U.S. Census Bureau cartographic boundary files (2017), via us-atlas 3.0.1 by Mike Bostock (ISC license)." Once S16 draws the 2024 file, that note names the 2024 file in the research lead's sidecar words, with no us-atlas credit, or the note says something untrue. Its other words stay, as the brief asks, unless a check fails.

## Requests

### To the main session

- **A board 2 item, the atlas's date printed twice.** Twenty-one distinct source lines in nine atlas sidecars print the snapshot date twice (by script), once as the period ("as of October 15, 2026", "checked on October 15, 2026", "verified through October 15, 2026") and again in the retrieval slot ("Snapshot of October 15, 2026."). They include `v7-issues` (11 lines), `v7-claims-by-grade`, `v7-claims-by-hub-and-grade`, `v7-claims-drug-prices`, `v7-issue-status-checks-on-power`, `v7-numbers`, and three that round 3 prints: `v7-rcv-local-routes` (S67), `v7-pathway-electric-decision-makers` (S68) and `v7-routes` (S71). The research lead's new line for S74, "…, snapshot of October 15, 2026, United States.", says it once, in chapter 13's atlas form. Recommendation for board 2: one pass over every atlas sidecar line into that form, with the specimens that print them rebuilt, since each change moves a round 0 to 2 specimen's words (H04: the date once). Left as they are this round, at your word.

## Tested

- `phase3_ch14_rules_build.py` before any change: a rerun left `git status` clean.
- After the rules' new cases: `--check-only` and the full run pass every check (no em dash or U+2011, no listed word, no studio word or bare code, every cited rule in the plan, no literal color, every token known). `git diff` showed only `14-003`, `14-004`, `14-006`, `14-007`, `14-009`, `14-012`, the generator, and the opener's group 15 link (since withdrawn, below).
- `phase3_ch14_build.py`: 0 faults (96 rules; round 3's entries wait for its round 3 run).
- Strict build (`guide_build.py --strict`) at 00:52 before any change: exit 0, 0 warnings, 10,638,223 bytes; rules 14.1 to 14.14 with the opener 172,255 bytes.
- Strict build after the rules' cases (`guide1.html`): exit 0, 0 warnings. Its page held `href="#group-14-15"` with no such id, found by script; the opener fix followed.
- Strict build after the opener fix (`guide2.html`): exit 0, 0 warnings, 10,697,303 bytes (the rest of the growth is other owners' kit work); rules 14.1 to 14.14 with the opener 175,538 bytes, 36,750 under 212,288. Every `#group-14-N` link in the page lands on an id, by script.
- In `guide2.html`, by Playwright (`cap.js`, scratch) at 1440, 1024, 768, 390 and 360 px, rules 14.3, 14.4, 14.6, 14.7, 14.9 and 14.12: 30 of 30 with no visible text under 13 px and no text past the page's width (text inside the tables' sideways-scrolling frames set aside), and no sideways page scroll. Looked at by eye: 14.6's rule text at 1440 px and its specifications at 390 px, 14.9's rule text at 360 px, 14.12's at 768, 14.7's at 1024 and 14.4's at 1440 px. Each new paragraph and spec row reads in place; 14.6 now runs five paragraphs of one case each.
- The words tool (`words/words.py`, scratch): `dump` and `lint` on S07, S12, S16, S57, S62, 14.73, 14.74 to calibrate; `dump` on S65 to S69 and S73, S74; `desc` on 14.113, whose caption and first `<desc>` agree.
- PW03's eight decision makers read from `work/extract/atlas-v7-data.json` by script, for S68's alt.

## Not tested

- No plate of rules 14.1 to 14.14 changed, so none was rebuilt in the kit; the plates' captures above show the rules' words only, and the plates on Charcoal, in grayscale and in forced colors were not looked at.
- The quick guide check (`guide_check.js`), the kit's `--all` and axe-core: the main session runs the first two.
- The words pass proper: no maker has reported. The first looks above read drafts that are still changing, and no word field of theirs was written by me.
- Group lines 11 to 14 against their entries, which have not landed.

## Files

- Modified: `work/build/scripts/phase-3/phase3_ch14_rules_build.py` (the rulings' cases in 14.3, 14.4, 14.6, 14.7, 14.9 and 14.12; the opener's printed-groups test), which rewrote `work/build/guide/entries/14-003.json`, `14-004.json`, `14-006.json`, `14-007.json`, `14-009.json`, `14-012.json`; `14-chapter.json` and `s-14-opener.html` were rewritten byte for byte as committed. `phase3_ch14_build.py` (the engineer's) rewrote `work/build/guide/chapters/14-data-visualization.json` with the new rule words, as every owner's run does.
- Created: this file.
- Scratch only: `words/words.py`, `cap.js`, the builds `guide0.html` to `guide2.html` and the captures in `caps2/`.
