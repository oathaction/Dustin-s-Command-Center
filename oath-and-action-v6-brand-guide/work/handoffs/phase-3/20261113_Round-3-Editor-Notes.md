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
- 01:15. **The data lead's rulings (a) to (g) are in rules 14.1 to 14.14**, each case once, in `phase3_ch14_rules_build.py`, which rewrote `14-003`, `14-004`, `14-006`, `14-007`, `14-009` and `14-012`. No plate, drawing or caption changed. The cases and where each now lives are under "Rules 14.1 to 14.14" below. Entries cite these rules for them and never restate them.
- 01:15. **The opener no longer links a heading the page lacks.** With 14.114 written and the chapter build still on rounds 1 and 2, the opener linked group 15 to an id the page did not hold. The generator now reads which groups the last chapter build printed. See "Group lines 11 to 15".
- 01:20. First looks written for all three makers on what has landed (S65 to S69, S73, S74; entries 14.113 to 14.116 and sketch 14.113), as early items in the three "Words for" sections. The full words pass waits for the makers to report.

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
- D3-xxx | Group lines 11 to 15 stand until their entries land; 14.113 to 14.116 agree with groups 14 and 15 | The brief: change a line only where the built entries make it untrue or unclear

## Group lines 11 to 15

Each line is read against the entries as they land, and changes only where a built entry makes it untrue or unclear. Status at 01:15, with entries 14.113 to 14.116 in:

| Group | Line | Status |
|---|---|---|
| 11 Behavior | People move through a process in funnels, cohort charts and survival curves, which show where they leave it. | Waiting for 14.93 to 14.95. To check: a survival curve shows when people leave, as well as where |
| 12 Structure | Process diagrams, decision trees and who-decides diagrams show who decides and how a decision moves. | Waiting for 14.96 to 14.103 |
| 13 Relationships | Networks, matrices and arc diagrams show who is connected to whom, and how strongly. | Waiting for 14.104 to 14.109. To check: S74's matrix counts connections and says the count is no measure of strength |
| 14 Flow | Sankeys, alluvial charts and flow maps show where money or people go, with every flow accounted for. | 14.113 agrees. Waiting for 14.110 to 14.112. To check: the journey map (14.112, a core form) sits outside the line's list, and S76's note says no dollar received is traced to a dollar spent, so "accounted for" must mean the node balances |
| 15 Maps | A map appears when the place answers the question, and it names its places in words as well as color. | 14.114 to 14.116 agree (codes in every square or circle, the table naming every state). To check against 14.120 and 14.122, where the map names no county and the table does, and Rule 14.3's new row |

**The opener (D3-452).** A group's question links to its heading only once the chapter build prints that heading. Round 3's entries now land before `phase3_ch14_build.py` takes round 3 in (its default is rounds 1 and 2), so an entry file alone no longer means the heading exists: at 01:00 the opener linked group 15 to `#group-14-15`, which the page did not hold. The generator now also reads the groups the last chapter build printed (`work/build/guide/chapters/14-data-visualization.json`), so it never links a heading the page lacks. **For the main session:** once the chapter build takes round 3 in, rerun `python3 -I work/build/scripts/phase-3/phase3_ch14_rules_build.py` and then `phase3_ch14_build.py`, so groups 11 to 15 link; I will do it in the words pass if I am resumed after that build.

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

### First look (01:20): S66 to S69 as drafted

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

### First look (01:20): S65, S73 and S74 as drafted

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

## Words for the cartographer

### First look (01:20): entry 14.113 and its sketch

Read and kept: 14.113's title, rule, use_when, use_instead, why and builders, and the sketch's caption, which is its first `<desc>` word for word (2,664 bytes). One suggestion: the caption can say the values are invented, as "Curved lines run from one place to four others over a plain map, each as wide as the invented number of people who moved along it, with a key of two widths." The drawing already carries "Illustrative data", so this one is yours to take or leave; if you take it, change the `<desc>` too.

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
