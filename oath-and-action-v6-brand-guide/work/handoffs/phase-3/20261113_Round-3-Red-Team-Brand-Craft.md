# Round 3 red team: nonpartisanship, brand and craft

Oath & Action Edition 06, Phase 3, round 3 review, November 13, 2026. Reviewer: the design director (`oa-design-director.md`) as reviewer, holding the creative director's brand knowledge (`oa-creative-director.md`), for `work/handoffs/phase-3/20261113_Phase-3-Round-3-Review-Brief.md`. Lens: nonpartisanship, brand and craft. Codes run BC-M1 (Must fix) and BC-S1 (Should fix). Paths are relative to `oath-and-action-v6-brand-guide/`.

Build read: the main session's strict build of `8507b822` (`.../round-3-review/main/guide.html`, 11,226,718 bytes, 0 warnings), copied to this lens's scratch before any capture. All 20 round 3 specs and S07, S12 and S16 were also built alone with the kit at page widths 1440, 390, 328 and 288 (drawings of 720, 358, 296 and 256 px; S16 at its wide widths) on both grounds: 23 of 23 PASS, 0 faults. Scratch and captures: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c39ddae-7cec-55d0-9e8a-b2e47330229b/scratchpad/phase-3/round-3-review/brand-craft/`. Report finished 04:45 UTC by the container's clock.

## 1. Score for this lens: 3 of 5

The twenty new forms join rounds 1 and 2 and board 1 as one family (one box style across the six diagrams, one sequential ink across the six maps, no red but S79's one point, parties in one ink and named), and most titles pass the party test from both sides; three faults keep the round from the bar: S73's title contrasts the two nominees' fundraising breadth with a rule that picked one committee each, two diagram tables misprint their links, and the maps lose many state codes and some marks at phone width and on Charcoal, with S16 worse at 390 px than board 1 drew it.

## 2. Must fix

**BC-M1. S73's title sets one fundraising committee of each nominee against the other, and the breadth it contrasts comes from the rule that picked them.** Owners: maker B (S73, entry 14.104), the research lead (the other committees' transfers), the data lead (sign-off), the editor (words).
- Where: `work/build/chart-kit/specs/s73.json`; `work/build/data/fec-jfc-transfers-2024.meta.json`.
- What is wrong: the title reads "The Harris Victory Fund sent $899.4 million to 53 committees in the 2024 cycle, and the Trump National Committee JFC sent $273.8 million to two." The file picks, for each nominee, "the joint fundraising committee that transferred the most to the nominee’s principal campaign committee". That rule is read the same way for both, but the title's contrast is breadth ("53 committees" against "two"), which the rule does not measure. The sidecar's own note lists the committees left out: for Trump, "TRUMP SAVE AMERICA JOINT FUNDRAISING COMMITTEE" ($134,018,942.92 to the campaign) and "TRUMP 47 COMMITTEE, INC." ($26,908,283.76); for Harris, "HARRIS ACTION FUND" ($4,900,000.00) and "HARRIS BALDWIN VICTORY FUND" ($35,265.62). The file reads only what those four sent to the campaigns, never what they sent to party committees. Read from the right, the title and the drawing say Trump's joint fundraising reached two committees while Harris's reached 52 party committees; a reader who knows that another Trump committee raised money with party committees will take the chart as built to show the gap. Read from the left, the title holds as a statement about two named committees. When one reading leaves a side short on evidence the chart never read, DR-93 and DR-124 are not met. The chart note's "$4.9 million and ... $160.9 million" gives the campaigns' side of the other committees and nothing of their transfers to parties, so the reader cannot judge the breadth claim.
- Fix, either: (a) the research lead reads line 22 for the four other committees (two for each nominee), the note gives each nominee's committees together with counts of recipients, and the title keeps a breadth contrast only if it holds across all of them; or (b) the title names what the rule picks and drops the breadth contrast, for example "The Harris Victory Fund sent its campaign $528.7 million and the Trump National Committee JFC sent its campaign $246.8 million in the 2024 cycle", with the Harris fund's $370.7 million to 52 party committees and the RNC's $26.9 million left to the drawing, and a note naming the four committees not drawn and saying their transfers to party committees are not counted here. (b) needs no new data. The data lead picks; the editor reads the new title from both sides.

**BC-M2. Two diagram tables print their links wrong, so the page table no longer answers who sent what or who governs whom.** Owners: the engineer (`table.group`, `agg: "first"`, and a check for an empty grouped column), maker B (S73), maker A (S68). Named place 4.
- S73 (`specs/s73.json`, `table.group.columns[0]`, `{"label": "From", "agg": "first", "field": "jfc_name"}`): the "From" column is empty in all 7 rows of the page table, in the kit's own page and in the guide build alike, and the two refund rows' "Report line" is empty too. The CSV export holds `jfc_name` for all 57 rows. With scripts off or with a screen reader, the table lists "Harris for President, the campaign", "Republican National Committee" and the two refunds with no sender, so it no longer prints links as rows (from, to, measure) as R3-6 asks, and it cannot answer "Where did each 2024 presidential nominee’s joint fundraising committee send what it raised?" The kit passed it (23 of 23 PASS).
- S68 (`specs/s68.json`, the column `{"field": "order", "label": "Line of authority", "words": {...}, "empty": "None drawn"}`): `words` maps orders 1, 2, 5 and 6 only, so four bodies print their sort number as their line of authority: "Congress and the Department of Health and Human Services ... 7", "City council or municipal utility board ... 3", "Electric cooperative board of directors ... 4", "Investor-owned utility ... 8". A reader takes "7" for a count of lines.
- Fix: the engineer makes `agg: "first"` carry a text field the group's rows hold, maps the refunds' `28C` through the column's `words`, and fails the check when a grouped column is empty in every row. Maker A gives S68's column words for every order ("None drawn" for 3, 4, 7 and 8), or moves the authority words to a field of their own so `empty` applies.

**BC-M3. S71 prints a studio word in reader text.** Owners: maker A (`usgov-v7-route-grid` or the spec's words), the editor.
- Where: S71, the "State statute" row, under "What it takes": "State constitutions read in round 0: Massachusetts, Nebraska, Virginia, Arizona; read November 11, 2026".
- What is wrong: the round's limits say "no decision codes or studio words in reader text". "Round 0" names the studio's process, which a reader cannot know.
- Fix: "State constitutions of Massachusetts, Nebraska, Virginia and Arizona; read November 11, 2026".

## 3. Should fix

**BC-S1. S80 lets land stand in for seats, the fault entry 14.124 names.** Owners: the cartographer (S80), the editor (entry 14.119 and the note), the data lead (sign-off).
- On Newsprint, the Republican panel is a near-solid dark Michigan, since its 20-point districts are the large rural ones (the 1st runs across the Upper Peninsula), while the Democrats' panel is almost all outlines; on Charcoal the Republican panel is the brightest mass on the plate. Four of the six Democratic seats (the 6th, 11th, 12th and 13th) are districts in and around Detroit, a few pixels across: "Not labeled at this width: 10, 12" at 720 px, "10, 12, 13" at 296 px and "10, 11, 12, 13" at 256 px. The panel heads print 7 and 6 correctly, but read from the left the drawing shows a Republican state; entry 14.124's why says "On real shapes the color also lets land stand in for votes, and a party that wins large, thinly settled places looks bigger than its count", and S80 shows the same effect in one ink.
- Fix: a Detroit inset in both panels at every width (the standard for a Michigan district map), with every district numbered; one note line, "A district’s area is not its voters: each elects one member"; entry 14.119 adds the same and points to Rule 14.121 for seat counts.

**BC-S2. S73's nodes cannot be seen, and S76's key draws in an ink no band takes.** Owners: maker B, the engineer (`flows`, `flow_band`, `width_key`).
- S73: each sender and receiver bar is 12 px wide in the same ink as the bands and touches them (`rect x="0" ... width="12"` and `x="138"`), so the drawing reads as one solid block with notches: on Newsprint a black mass about 150 by 225 px on the Harris side, on Charcoal a light one. Entry 14.104 tells builders to draw "each sender and each receiver as a bar", and the reader cannot find one. Set a 2 px ground gap between each bar and its bands, or draw the bands one step lighter in the party-mark ink with the bars solid, as S76 sets its node apart.
- S76: the key's "$500 million" band is a 32 by 84 px swatch in Stone (rgb 93, 99, 109, the hairline ink) on Newsprint, while every band takes the light fill (rgb 161, 162, 163) or the track (204, 202, 197). Draw the key band in the band fill with its edge.

**BC-S3. S81 on Charcoal: "No estimate" and "Under $50,000" are the same swatch.** Owner: the cartographer. Key swatches rgb(32, 33, 34) and rgb(32, 42, 40), 1.09 to 1, both with the same gray edge; De Baca County reads as a low-income county. Give "No estimate" a hatch on both grounds, or the land ink the Newsprint drawing gives it, lighter than the ground.

**BC-S4. S82's closest races are the faintest marks, and on Charcoal at phone width they read as the other party's outlines.** Owners: the cartographer, the data lead.
- The title names "36 of the 435 races were decided by under 5 points". On Charcoal the under-5 fill (rgb 46, 67, 64) measures 1.78 to 1 against the ground and the ghost's inset outline 1.80 to 1; at 358 px and below on Charcoal, and in grayscale, an under-5 seat and an empty outline look alike at true size. C-1 fixed this on Newsprint.
- At 720 px the grid runs to the drawing's last pixel (a square ends at x 720 and a state line at 721).
- Fix: on Charcoal, start the won steps at one that reaches 3 to 1 against the ground, or thin the ghost to a dotted hairline; inset the grid 2 px.

**BC-S5. The maps drop many state codes on a phone, and S16 now places them worse than board 1.** Owners: the engineer (`map_labels`), the cartographer.
- S78: "Not labeled": MA, MD and WV at 720 px; 22 states and DC at 358; 35 states and DC at 256. At 358, Georgia, Michigan, Minnesota, Pennsylvania, New York, Ohio and Washington lose their codes while Montana and Idaho keep theirs.
- S82: AK, ND, VT and WY uncoded at 720 px; 33 states at 358, 44 at 296 and 46 at 256.
- S16 at 358 px against board 1: CT's code moved from beside its circle in the Northeast to over the Carolinas on a long leader; TN's moved west past Missouri; VA's code is dropped ("Not labeled at this width: MA, NJ, VA", against board 1's "MA, NJ"). The circles moved at most 3.5 px (North Carolina), so board 1's word places still fit. The data lead signed S16 off at 1440 px only.
- Fix: let codes sit on mid and dark steps in the step's label ink at phone widths, as the desk drawing does; an east column with short leaders for New England and the Mid-Atlantic; single-seat states beside with a leader at desk width; S16's codes at board 1's places where they still clear.

**BC-S6. S79's neighbors draw as stray strokes.** Owner: the cartographer. Nevada's, Oregon's and Arizona's borders show as short unconnected lines in empty space (top right and right of California, at every width and on both grounds), which read as drawing errors. Draw each neighbor's outline whole, clipped at a drawn frame, or leave the neighbors to their names. "Kern County" sits under the county over Ventura and Los Angeles counties; set it inside Kern's lower right, which has room at 720 px.

**BC-S7. S69 and S70 scatter their order across columns.** Owner: maker A. "Each card in the shortest column" puts S70's second row as Third, Fifth, Fourth, and S69's alphabet zigzags (Energy and Commerce under Foreign Affairs in the first column, Ethics under Judiciary in the second). Entry 14.99 says the cards fill columns "so the order reads from the top down", which the drawings do not. Fill each column top to bottom in order, balanced by height, and sort S69 by the printed name, not the full name that starts "Committee on the".

**BC-S8. S66's main line runs empty after step 1.** Owner: maker A. The three branches out of step 1 stack beside it, so about 270 px of heavy line separate step 1 from step 2 while the later gaps are about 30 px; distance along a process line reads as time. Let the branch column run beside steps 1 and 2 so the spine's gaps stay even.

**BC-S9. S65's title reads one way from the right.** Owners: maker B, the editor, the research lead.
- The title sets "16.0 million ended for a procedural reason" against "6.9 million found ineligible", and the chart never says in plain words what a procedural ending is, or that it does not tell whether the person was eligible. Note 1 quotes CMS's "terminated for a procedural or administrative reason". Read from the right, the title says 16 million eligible people lost coverage over paperwork; read from the left, it states the record. "Ended" also hides who ended them, the states.
- Fix: one note sentence, "A procedural ending means the state closed the case without deciding eligibility, most often because a renewal form came back incomplete or not at all; some of those people were still eligible and some were not." The research lead checks the wording against CMS's definition. The title may say "states ended".

**BC-S10. Two titles and an example name one side where the record has two.** Owners: maker A, the cartographer, the editor.
- S72: "with seven Democrats and one independent joining 52 Republicans" names the Senate's yes-side crossovers, and neither the Republican who voted no nor the House's eight crossovers (notes 1 and 2 give them). Name the crossovers both ways in both chambers, or none in the title.
- Entry 14.115: "Name the direction in words in the key, as “toward the Republican nominee”". Give both: "as “toward the Democratic nominee” or “toward the Republican nominee”".

**BC-S11. Words left behind by C-1.** Owners: the cartographer, the editor.
- Entry 14.119's why: "Gray steps for the margin keep a close race and a safe one apart". The steps are Verdigris now: "Steps of one ink".
- Entry 14.124's `use_when`: "gets a fairer answer from gray panels by party". The panels are not gray: "from two panels, one for each party".
- Entry 14.124's `sketch_alt`: "takes a side at a glance, while two panels ... show" is a contrasting pair (chapter 02); two sentences.

**BC-S12. Typography and edges.** Owners as named.
- S65's title breaks "16.0 / million" at 720 px; S75's note breaks "S. / 3349"; S81's key breaks "2020 to / 2024" at 256 px. Hold figures with their units, bill numbers and periods with no-break spaces (makers A and B, the cartographer).
- S67's table, Missouri: "certified returns: 1966852 to 906851" prints no thousands separators (maker A).
- S71's "38" and its head "Reforms that" end on the drawing's last pixel at 720 px; the 8 clips at 2x (maker A).
- S66's "Office of Information and Regulatory Affairs (OMB)" reads as if OMB were its initials: "in the Office of Management and Budget" (maker A).

**BC-S13. S77 states a measured fact the chart says it does not measure.** Owners: maker B, the editor. Note 1: "a state may move faster, and some miss the limits." The measure line says "the chart measures no household’s wait". Cut "and some miss the limits", or source it.

**BC-S14. S74's title names the diagonal, and the drawing does not mark it.** Owner: maker B. "32 of the connections stay within one region" sums the diagonal, which looks like any other cells. A hairline along the diagonal, keyed "Within one region".

**BC-S15. The rule rail cuts its active entry.** Owner: the engineer. At 1440 px with group 13 at the top, the active "Rule 14.103 Keep a" sits half cut at the rail's bottom edge. Round 2's BC S17 asked the open group to scroll to a whole line.

## 4. The seven named places

**1. Maps at 256 to 390 px on Charcoal (mine).** Built S78 to S84 and S16 at drawings of 358, 296 and 256 px on both grounds and in grayscale, and S78, S80, S84 in the guide at 360 px. The light land on Charcoal holds by its 1 px edge on S81 and S83. Codes are lost in large numbers on phones (BC-S5), and S16 lost CT's and VA's places against board 1. Leaders hold where drawn; S78's NY at 256 px sits above New England on a short leader. Alaska and Hawaii sit in their frames on every map, with dots in both on S83. DC's square draws at every width on S78 and S84, though S78 stops naming it under 720 px. S82's rings and dots drop under 10 px and the notes name the seats; the closest races fade into the ghosts on Charcoal (BC-S4). S83's 50,000 dots read as a pattern at 256 px. S79's inset stacks under the map on phones and stays legible; its neighbor lines do not (BC-S6). S81's no-estimate swatch merges with the lowest class on Charcoal (BC-S3).

**2. Grouped tables (not my lens; seen in passing).** S73's grouped table prints no sender in any row (BC-M2). I did not read S69, S70, S72, S81, S82 and S83 against their reader questions or open their CSVs beyond S73's.

**3. The party test (mine).** Every round 3 title, note and entry read from the left and from the right.

| Spec | Mark the title names | Ink | From the left | From the right | Verdict |
|---|---|---|---|---|---|
| S65 | Procedural endings | Subject ink, stages gray | States the record | Implies eligible people lost coverage; no plain meaning given | Holds on the record; words lean (BC-S9) |
| S66 | None | Path and branches | Names Executive Order 14215 neutrally | Same | Holds |
| S67 | None | One ink, every answer alike | Bans named as the record has them | Same | Holds |
| S68 | None | One node style, open diamond | Neutral | Neutral | Holds; table misprints (BC-M2) |
| S69, S70 | None | One ink | Neutral | Neutral | Holds |
| S71 | None | One series | "though most bills need 60 senators" is fact; 2013 and 2017 cloture changes named together | Same | Holds; studio word (BC-M3) |
| S72 | None | One party ink, solid and outline | Headline names only Democratic crossovers | Neutral | Holds; words should match both ways (BC-S10) |
| S73 | None | One party ink, one scale | Holds as a statement about two committees | Breadth contrast rests on one committee per nominee | Fails DR-93 as titled (BC-M1) |
| S74 | None | Verdigris steps, authority outlined | Note 2's examples, Congress and the executive, read neutrally | Same | Holds |
| S75 | Pair of bills | Subject ink | No party | No party | Holds |
| S76 | Individuals' gifts | Subject ink | No party | No party | Holds |
| S77 | None | Path in ink | Neutral | Neutral | Holds; "some miss the limits" unsourced (BC-S13) |
| S78, S81, S83 | None | Sequential Verdigris or dots | Neutral | Neutral | Holds |
| S79 | Lake Isabella | The one red point | Neutral | Neutral | Holds |
| S80 | None | Verdigris margin steps by panel | Land makes the Republican panel look like the state | Neutral | Holds on ink; the drawing leans by area (BC-S1) |
| S82 | None | Verdigris margin steps by panel | Neutral; title gives the winner first, panels Democrats first | Same | Holds |
| S84 | None | Three sequential steps | "up from" is neutral; darker means a higher wage, not a better one | Same | Holds |
| Sketch 14.124 | None | Gray stand-in | Neutral | Neutral | Holds; teaching weak (place 7) |

No red and blue anywhere, no Prussian for a party, and no party named by color. Neutral party ink with each party named on S72, S73, S80 and S82. S73's line 22 is one measure read the same way for both nominees (RL-3a), apart from BC-M1's breadth. The Verdigris margin steps on S80 and S82 read as magnitude only: both panels take the same ink, darker for a wider margin, and the steps never stand for a side.

**4. The diagrams' reading order (mine).** S66 (way in, step 1, its branches, steps 2 to 4, court review, step 5, Congress), S67 (the tree's order), S69 (by committee), S70 (by circuit) and S77 (path, then the expedited branch) print their tables in reading order with each link named ("Then", "Next step"). S74, S75 and S76 print links as rows (from, to, measure). S73 prints no "from", and S68's "Line of authority" column prints sort numbers for four bodies (BC-M2). S68's two lines of authority end in Rule 15.5's open diamond at the body governed, with no sign and no loop. Across chapters 14 and 15 one mark keeps one meaning: the diamond for authority; arrowheads in S66, S67 and S77 mean "next step" and carry no sign tag; no round 3 diagram uses a dash, which Rule 13.4 keeps for a connection's grade. Chapter 15 prints "decides" on its diamond lines and S68 prints no verb; the note says what the diamond means, which serves.

**5. The weight of every plate (mine).** Measured in the guide build, each plate's figure with its frame: S65 6,440; S66 10,135; S67 13,291; S68 9,655; S69 14,591; S70 10,870; S71 12,166; S72 12,282; S73 9,699; S74 11,677; S75 7,924; S76 7,481; S77 7,835; S78 9,096; S79 4,376; S80 6,514; S81 13,264; S82 13,270; S83 13,226; S84 10,869. Only S69 passes 13,852 (by 739), and none passes 15,000. The build report gives chapter 14 with the kit at 2,219,208 of 2,803,941, map geometry at 133,117 of 250,000, rules 14.1 to 14.14 with the opener at 175,796 of 212,288, the share per plate 14,106 for round 4's 13, and the page projection 15,044,385 of 15,500,000. S69 buys its extra 739 bytes with the 109 subcommittee names, which the drawing and the table both need. No plate spends bytes on ornament. S80, at 6,514, has room for BC-S1's inset.

**6. Rule 14.9 on the class maps (not my lens).** I read S78's and S81's notes as printed ("Thirteen of the 50 states and the District of Columbia"; "1,707 of 3,143 ... and 182") and found no county or state named above another, but I recomputed none of the three tests.

**7. The sketches at true size (mine).** All nine in the guide at 1440 px at 1x, and 14.124 at 390 px at 1x and 2x. The eight reference sketches share one 320 px frame with a 10 px inset and "Illustrative data" at the corner, their captions are the first sentence of `sketch_alt`, and each draws its form plainly (14.108's two kinds of tie are now solid and named on a line, under MB-8). On 14.124, the "Form to avoid / Do not publish" bar sits over the misleading half only and "Use instead / Panels by party" over the better one, at desk and phone. The gray stand-in does not teach the failure plainly. At true size it is a tidy two-shade winner map, and a builder could take it for the neutral way to draw one: the fault the entry names, party color, is absent from the drawing and present only in words. The key's "Party A, shown red" also reads literally as a claim the drawing contradicts. See question 1.

## 5. Questions for Dustin

1. **Sketch 14.124: literal red and blue in the half marked "Do not publish"?** Recommendation: yes, confined to that half at sketch size, with the key reading "Party A" and "Party B" and the bar above it. The gray stand-in reads as a usable neutral map, which is the opposite of the lesson. The engineer would need the guide check to pass red beside a blue that is not Prussian inside an avoid half only, and DR-64 would record the one exception. If you prefer gray, change the key to "Party A: red in the form this stands for" and draw the second fault the why names, a large rural place filling the page, so the drawing shows a fault a reader can see.

## 6. Tested

- `node work/build/chart-kit/oa-chart.mjs build s65 ... s84 s07 s12 s16 --widths 1440,390,328,288 --out <scratch>/kit-out`, sweep on: 23 of 23 PASS, 0 faults, read from the full log.
- Looked at by eye from the kit's pages: every round 3 drawing at 720 px on Newsprint at 1x (S71, S73, S74, S76, S82 and S83 also at 2x crops); S65, S73, S78, S80, S81 and S82 at 720 px on Charcoal; S65, S73, S76, S78, S79, S81, S82, S83, S84 and S16 at 358, 296 and 256 px on Charcoal and S78, S79, S80, S81, S82, S83, S84 and S16 on Newsprint, from the 2x exports; S82 at 358 px in grayscale on both grounds; true-size crops of S82's and S78's narrow drawings enlarged by nearest neighbor.
- S16 against board 1's captures in `work/boards/phase-3/round-0/specimens/` at 1440 and 390 px on both grounds; circle centers and radii compared by script from both SVGs (at most 3.5 px moved, North Carolina; radii and the 1024 by 791 frame unchanged).
- The guide build, Chromium, one browser at a time: every entry 14.93 to 14.124 captured whole at 1440 px (1x) and 390 px (1x); 14.116 to 14.123 at 360 px (1x); 14.113, 14.119, 14.121 and 14.124 at 390 px (2x); viewport views at groups 11, 13 and 15 and Rule 14.117 at 1440, 1024, 768 and 390 px. Looked at: 14.124 at 1440 and 390 (1x and 2x), the eight reference sketches at 1440, 14.121 whole at 1440, 14.117, 14.119 and 14.123 at 360, the page views at 1440, 1024, 768 and 390.
- Page tables read by script (HTML parse) from the guide build for all 23 specs, with a scan for columns empty in every row (S73's "From" the only one); S66, S67, S68, S69, S70, S73 to S77 tables read row by row from the kit's pages; S73's CSV read for `jfc_name`.
- Plate bytes measured by script from the guide build for the 20 round 3 plates and S07, S12, S16; the build report's weight and projection read by script.
- Contrast by the WCAG formula on rendered SVG colors: S81's Charcoal swatches; S82's Charcoal under-5 fill, ghost outline and won edge against the ground.
- Every round 3 spec's title, measure line, notes and phone note, and every entry's rule, use, instead, why, builders and `sketch_alt`, read by script and read from both sides.
- `fec-jfc-transfers-2024.meta.json` read for the selection rule and the other committees.
- `git status` checked: I wrote only this report in the repository.

## 7. Not tested

- Charcoal inside the guide's column: the guide stays on Newsprint (DR-204, D2-1133), so Charcoal was read from the kit's pages only.
- S66 to S72, S74, S75 and S77 below 720 px on Charcoal, and S66 to S72 below 720 px on Newsprint, beyond the guide's 390 px entry captures (captured; I looked at 14.124 only among those closely).
- Grayscale beyond S82 at 358 px; forced colors, reduced motion, print and scripts off (the access lens).
- Named places 2 and 6 in full: the grouped tables against their reader questions and the CSVs other than S73's; Rule 14.9's three tests recomputed.
- Any figure in a title or note against the data; the derived files.
- The guide check and the four-width check (the main session runs them).
- S07 and S12 beyond their kit builds (placement only, unchanged drawings).
- Chapter 15's plates beside the round 3 diagrams; I read chapter 15's grammar from its manifest's alt text, not its plates.
