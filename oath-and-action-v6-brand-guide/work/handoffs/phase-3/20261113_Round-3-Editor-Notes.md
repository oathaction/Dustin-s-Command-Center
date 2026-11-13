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
- 01:15. **The data lead's rulings (a) to (g) are in rules 14.1 to 14.14**, each case once, in `phase3_ch14_rules_build.py`, which rewrote `14-003`, `14-004`, `14-006`, `14-007`, `14-009`, `14-012` and the opener (group 15 now links, since 14.114 exists). No plate, drawing or caption changed. The cases and where each now lives are under "Rules 14.1 to 14.14" below. Entries cite these rules for them and never restate them.
- 00:55. First look at the cartographer's entries 14.114 to 14.116, under "Words for the cartographer".

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

## Group lines 11 to 15

(Checked against the entries as they land.)

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

(Waiting for S66 to S72, entries 14.96 to 14.103 and sketch 14.103.)

## Words for maker B

(Waiting for S65, S73 to S77, entries 14.93 to 14.95 and 14.104 to 14.112, and six sketches.)

## Words for the cartographer

### First look (00:55): entries 14.114 to 14.116

Read against S07, S12 and S16 as board 1 approved them, and again at 01:15 against the data lead's rulings, which now sit in rules 14.1 to 14.14 (above). The cartographer applies these.

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

## Tested

## Not tested

## Files
