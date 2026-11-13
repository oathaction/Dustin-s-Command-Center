# Round 4 maker A notes: proportion and overlap

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. Maker A, briefed as a senior graphics editor at a newsroom known for exact, quiet charts, who draws exact share and overlap charts. Brief: `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`, the maker A row and its "Maker A" bullet. Rows: maker "A" in `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`, rules 14.79 to 14.84 (coverage plan 3.8). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/maker-a/`. Written as I go; the container can restart.

## Status

- 21:31 UTC (clock read 21:29). A4-E1 landed and S85 draws its icon and chip. The design director's DD-A1 to DD-A11 are applied (DD-A5 and DD-A6 after the data lead's yes). All four build PASS with the sweep, 0 faults. Waiting on the quick guide check of my strict build (sketches), then a last strict build.
- 21:16 UTC (clock read 21:13). All four forms, specs S85 to S88, entries 14.79 to 14.84 and both sketches are written. S86, S87 and S88 build PASS with the sweep, 0 faults; S85 fails only for the icon and chip parts it waits on (A4-E1). The data lead's MA-1 to MA-8 and Q-A1, the research lead's R-1 variant and the editor's first and second looks are applied. Figure checks 51 of 51. Next: strict build, quick guide check on the sketches, and the design director's read.
- 20:58 UTC (clock read 20:55). Rulings (a) to (c) read; applying them. Forms `icon-array`, `proportional-symbols` and `venn-diagram` drafted and building; `euler-diagram` next. S85 waits on A4-E1 (the icon part) and Q-A1 (its word and chip). Round 4's ceiling noted: 13,172 bytes a plate with its frame once S12's tile lands.
- 20:45 UTC (clock read 20:41). Started. Read `CLAUDE.md`, the round 4 brief, the plan file's round 4 rows, the round 4 data plan with its sign-off and "Conditions for round 4's maker", coverage plan 3.8, the kit README, round 3's maker A notes, DR-266 and D3-1679, Rules 10.1, 10.4 and 10.6, and my four data files with their sidecars. Writing the four forms now; named marks and inks wait on the data lead's "Rulings".

| Rule | Spec | Form ID | Status |
|---|---|---|---|
| 14.79 | S85 | icon-array | form, spec, entry; PASS with the sweep, icon and chip drawn |
| 14.80 | S86 | proportional-symbols | form, spec, entry; PASS with the sweep |
| 14.81 | S87 | venn-diagram | form, spec, entry; PASS with the sweep |
| 14.82 | S88 | euler-diagram | form, spec, entry; PASS with the sweep |
| 14.83 | sketch | packed circles (reference) | sketch 1,893 bytes, entry |
| 14.84 | sketch | rose chart (avoid) | sketch 2,986 bytes, entry |

## Summary

- Four forms (`icon-array`, `proportional-symbols`, `venn-diagram`, `euler-diagram`), specs S85 to S88, entries 14.79 to 14.84 and two sketches (14.83 packed circles, reference; 14.84 rose chart, avoid) are written, on the data lead's rulings (a) to (c), Q-A1 and MA-1 to MA-10, the editor's words and the design director's DD-A1 to DD-A13. All four build PASS with the sweep, 0 faults. The data lead signed off S86 and S88 and S87 with MA-9 since applied; the design director's second read passes all four.
- No red on any plate (ruling (a)). S85 and S86 name one mark in the subject ink; S87 and S88 name none.
- `maker_a_round4_derive.py --figures` checks 51 figures and facts (CL-050's name and chip against chapter 10, every gap against its margin, the Euler's areas), 0 failed. No derived file this round.
- Plates, as the final strict build places them: S85 4,228, S86 4,283, S87 4,694, S88 4,733 bytes (about 750 more each with the frame). Sketches: s-14-83 1,893 bytes, s-14-84 2,986 bytes.

## Routine calls

- D3-xxx | S85 draws its 100 marks larger than the unit chart's 14 px squares: 24 px with 4 px gaps at a desk, up to 22 px with 3 px gaps on a phone, a row of ten always | DR-266's plain unit marks in their style (filled, open), sized so a hundred stay countable in a 720 px column; one grid at every width (ruling (b))
- D3-xxx | S85's key words sit beside their marks: "Union member" beside the filled row and "Not a member" beside the first open row at a desk, both under the grid on a phone, each with its swatch | Ruling (b): the key in the file's words, each beside its mark
- D3-xxx | S85's table prints all four published rows (2025 all workers, private, public, 1983) and the array draws the 2025 row alone through `labels.draw`, the limitation in the table's caption | Ruling (b): the table prints the published figures with V7's limitation as its caption note; the kit has no separate table note
- D3-xxx | S85's topic: CL-050 at 48 px, "Worker bargaining power" beside it and the chip "Variable A2" after it on the name's baseline, all above the grid; where name and chip do not fit one line (the 256 px drawing) the chip sits under the name and the two center on the drawing | Q-A1 and Rule 10.6; checked by script against the editor's label table and chapter 10's list of 41
- D3-xxx | S86 sets the federal government and the states in one line, "Not drawn: 1 federal government and 50 state governments, too few to draw at this scale.", in the key's band: beside the key at a desk, under it on a phone, with no hairline | DD-A6 with the data lead's yes (21:25 UTC); the circles follow the measure line directly and take the column's full width at a desk
- D3-xxx | S86's circles run largest first at every width; the table opens with the federal government and the states, then the local kinds in the same order (`sort` by level, then by count) | DD-A4: the row reads as the ranking the title states, and the named circle comes first
- D3-xxx | S86's special districts print their name and count inside their circle, in the label-on-subject ink, where both fit each chord with 6 px to spare; every other circle is named under it at a desk and beside it on a phone | Ruling (b)
- D3-xxx | S86's key takes S16's grammar: an eyebrow title, "Circle area shows the count", and rings at 1,000, 10,000 and 40,000 side by side on one line in the context ink at 1 px, each count centered under its ring, under the circles at the left | MA-5, DD-A5 with the data lead's yes, DD-A12; the editor moved the area sentence from the measure line to the key's title
- D3-xxx | S87's circles overlap by 1.2 times the radius between centers at a desk and 1.12 on a phone, the frame full width with the two circles centered, "No coverage" beside the second circle where it fits and in a band under the circles where it does not | Equal circles carry no count; the overlap wide enough for "Both", its count and share at 256 px
- D3-xxx | S87 and S88 print each group's name, count and share on their own lines, inside the group where each line fits its region at its own height with 4 px to spare, the label size first, then the tick size, then narrower | Ruling (b), "inside the region where it fits with 4 px to spare"; one rule in both forms, so the pair reads as one file drawn two ways
- D3-xxx | S88 finds the distance between the two centers that gives the shared area by bisection on the lens formula and fails the drawing past 1 percent; the kit's `area_of` check holds each radius | Ruling (b): each drawn area within 1 percent of its count at every width, named in `notes_internal`
- D3-xxx | S88's overlap words ("Both", 23.8 million, 7.1%) sit under the circles on a leader at every width, since the overlap is 0.45 of the larger radius wide | Ruling (b), a leader in the context ink where the words do not fit
- D3-xxx | S88 places "No coverage" beside the pair at a desk, its circle one radius clear of the public circle, and under the pair on a phone with its words beside it | Ruling (b): a gap at least its own radius
- D3-xxx | S87's and S88's titles: S87 lists the four groups; S88 states the two circles and their overlap ("In 2025, 213.2 million people had private health coverage and 119.1 million had public coverage, and 23.8 million had both.") | MA-8 and the editor's words: two findings from one file, each in its drawing's terms
- D3-xxx | No derived file this round: the derive script only checks figures (`--figures`, 51 checks) | S85 to S88 draw the research lead's frozen files as they stand
- D3-xxx | The packed circles sketch draws an illustrative city budget of 12 lines packed by a greedy tangent search, the four largest named, track ink with a context edge | R3-9's frame (320 px, 10 px inset); the same budget the mind map sketch uses, so the two reference sketches read as one family
- D3-xxx | The rose chart sketch draws four illustrative values as quarter wedges whose radius is the value (A 2, B 4, C 3, D 1) beside bars of the same values from one zero line | R3-9's frame (two 288 px halves of one height); "a value twice another looks four times as large" is A against B
- D3-xxx | S87's words for a group that cannot fit inside it (at the narrowest drawings, "Both") sit under the circles inside the frame, on a leader straight down from the group, and the frame grows to hold them | MA-9: the count shows at every width; the same rule S88 uses
- D3-xxx | S88's `notes_internal` names its area check: the form's 1 percent test on the shared area, the kit's `area_of` on each radius, and the derive script's recomputation at six radii | MA-10
- D3-xxx | I ran `phase3_ch14_build.py --rounds 1,2,3,4` so my entries reach the chapter file for my own strict build | The generator's default builds rounds 1 to 3 (DR-253); its five faults are the infographics maker's entries not yet landed

## Requests

### Requests to the data lead

- **Q-A1, S85's topic word.** The editor's label table (`work/handoffs/phase-2/20261110_Stage-B-Ch10-Labels.json`) files CL-050 as an atlas variable: label "Worker bargaining power", chip "Variable A2" (V7 title "Workers' bargaining power"); its Civic Line word "Worker Bargaining" is the inventory's, for finding the drawing. Rule 10.6 sets an atlas drawing only beside the atlas's own name with its typed chip. I print "Worker bargaining power" beside the drawing (the approved label, checked by script) and ask whether the chip "Variable A2" prints beside it in the drawing, as chapter 10's register prints it. My reading: yes, since Rule 10.6 binds and the chip says why a picture of bargaining heads a chart of union membership (V7 files CL1514 under I101, collective bargaining). Say if you rule otherwise. **Answered (21:01 UTC): yes, the name and the chip; applied, with `CL1514` in `v7.ids`.**

- **Q-A2, S86's key and its "not drawn" line (the design director's DD-A5 and DD-A6, both "with the data lead's yes").** (1) DD-A5 asks S86's size key to take S16's grammar, approved on board 1: three circles side by side on one baseline, each value centered under its circle, an eyebrow title; your ruling (b) names three nested circles (1,000, 10,000 and 40,000). (2) DD-A6 asks the line "Not drawn: 1 federal government and 50 state governments, too few to draw at this scale." to move from over the circles into the key's band (at a desk to the key's right, its first line level with the key's title; on a phone under the key), with no hairline; your ruling (b) says "above or beside the circles with a hairline gap". My view: yes to both. One key grammar in chapter 14 reads as one hand, and the line is a statement about the scale, so it belongs beside the scale; the circles then follow the measure line directly. Same counts, same words, same circles. Say yes or no to each; I hold both until you do. **Answered: yes to both (21:25 UTC); applied.**

### Requests to the engineer

- **A4-E1, a Civic Line icon in a kit drawing (S85, DR-266).** S85 sets CL-050 once at 48 px beside its word. The kit has no part that draws a Civic Line drawing, and the guide's sprite holds CL-050 as `oa-sym-cl-050`. I ask for one shared part, such as `K.parts.icon(c, 'CL-050', x, y, 48)`, that draws the approved black master at the size given in the icon ink (`--oa-component-icon-ink`, the data lead's ruling (b); one color, no red accent), with `aria-hidden="true" focusable="false"`, `data-icon="CL-050"` and `data-icon-family` (Rule 10.6 and the chapter 10 construction file, section 11), as `<use href="#oa-sym-cl-050">` on the guide's page and with the drawing inline in the SVG and PNG exports, and that the checks see as a shape with a box, so no word sits on it. CL-050 is an atlas symbol (the editor's label table: "Worker bargaining power", chip "Variable A2"), so Rule 10.6 sets a typed chip beside its name: if the data lead rules the chip prints in the drawing, a chip part in the same call (`K.parts.chip(c, x, y, 'Variable A2')`, the chip-fill and chip-label roles kit.css already holds) would keep it in one style with the figure's HTML chips. Until it lands, S85 draws the name alone and fails its build on purpose (the form warns). The infographics maker's S89 takes no icon (ruling (b)), so this part is for S85 alone today. **Done by the engineer (21:1x UTC): `K.parts.icon` and `K.parts.chip`; S85 draws both.**

## Sign-off items from the data lead

| Item | Done |
|---|---|
| MA-1 | S85's grade line is ruling (c)'s; its source line is the sidecar's `snapshot_in_grade` variant (R-1) |
| MA-2 | S85's open marks: a 1 px context-ink edge and no fill, set in the form for every open mark (no spec key needed) |
| MA-3, Q-A1 | S85 prints "Worker bargaining power" and the chip "Variable A2", checked by script against the label table and chapter 10's list of 41; `CL1514` in `v7.ids` |
| MA-4 | S86's unnamed circles take the track ink with a 1 px context-ink edge on both grounds |
| MA-5 | S86's key: 40,000, 10,000 and 1,000 |
| MA-6 | S86's title in the past tense, in the editor's words |
| MA-7 | A4-E1 landed (`K.parts.icon`, `K.parts.chip`); S85 draws CL-050 at 48 px with its name and chip, PASS |
| MA-8 | S88's title states the finding, in the editor's words |
| MA-9 | S87's "Both" takes a leader under the circles where it cannot fit inside; PASS at 1440, 390, 328, 288 and 256 px pages and in the sweep |
| MA-10 | S88's area check named in `notes_internal` |

## The editor's words

- First look (20:57) and second look (21:03): applied to S85 to S88 as given (S85's note 1 and chart note; S86's title, note and chart note; S87's note 1 and the TRICARE note; S88's title without "of them", its short cross-reference and the TRICARE note).
- The design director's ask, ruled 21:24: S86's measure line drops "; each circle’s area is in proportion to its count", and the key's eyebrow title reads "Circle area shows the count", so the sentence the editor counted on stands beside the circles.
- Entries and sketches, read 21:12: all ten rows applied: 14.79 ("rows of 10", "the name and typed chip chapter 10 gives it", the why's figures and "a Civic Line drawing"); 14.80 (the 2022 count of county governments; "track gray"); 14.81 ("track gray"); 14.82 (the why ends on its last reason); 14.83 (the why and the sketch caption's second sentence name the reader); 14.84 (`sketch_alt` in two sentences, its first equal to the sketch's first `<desc>`, which ends at "four times as large.").

## The design director's requests

Read at 21:22 UTC; all eleven applied by 21:30 UTC. No figure or word changed; DD-A5 and DD-A6 waited for the data lead's yes (21:25 UTC).

| Item | Spec, form | Done |
|---|---|---|
| DD-A1, Must | S85, `icon-array` | The icon, the name and the chip are one row on the icon's vertical center: the chip sits on the name's baseline, 8 px after it. Where they do not fit one line (the 256 and 288 px drawings and the 320 px drawing) the chip drops under the name at x 60, 6 px below, and the two center on the icon. The layout guard passes at every width of the sweep |
| DD-A2, Must | S85, `icon-array` | A4-E1 landed: CL-050 draws at 48 px in the icon ink at x 0 to 48, flush with the grid's left edge; one row pitch (28 px at a desk, 25 on a phone) under the icon's box before the grid. Captures in my scratch `kit-final/s85/` at 1440, 390, 352, 328 and 288 px pages, both grounds |
| DD-A3, Should | S85 spec | `typography.hold: ["October 15, 2026"]` (with `nbsp`), so the grade line never breaks the date |
| DD-A4, Should | S86 spec | Sorted by level, then by count, largest first: the circles run special districts, municipalities, townships, independent school districts, counties at every width; the table opens with the federal government and the states, then the same order |
| DD-A5, Should | S86, `proportional-symbols` | The key takes S16's grammar: an eyebrow title, "Governments", and circles at 1,000, 10,000 and 40,000 side by side on one baseline, each count centered under its circle, in the label ink at the bubble outline's width as S16 draws them. On a phone the gaps close to 6 px and every circle shrinks with the key's scale until the key fits the width (one area scale at every width) |
| DD-A6, Should | S86, `proportional-symbols` | "Not drawn: ..." moved into the key's band: at a desk to the key's right, its first line level with the key's title; on a phone under the key; no hairline. The circles now follow the measure line directly |
| DD-A7, Should | S86 spec | `typography.hold: ["this scale"]`, so "scale." never stands alone |
| DD-A8, Must | S87, `venn-diagram` | Every region inside the circles takes one line structure from one top line: the fewest breaks at which both lone groups fit (name, count and share; then the count's figure and unit apart; then the name's words apart), the label size only. "Both" takes the same structure from the same top line or leaves on its leader, under the circles in the frame (390 and 320 px today) |
| DD-A9, Should | S87, S88 | Each set's name is centered over its circle (x = its center), wrapped to the distance between the centers less 12 px, both names on as many lines as the longer needs |
| DD-A10, Must | S88, `euler-diagram` | One label size: the same rule as DD-A8, so "Both" leaves on its leader at every width where the overlap cannot hold it in the label size with 4 px to spare, desk included |
| DD-A11, Should | S88, `euler-diagram` | The leader runs down the overlap's own axis (x = the two crossing points'), so it leaves the overlap through its lower point |
| DD-A12, Should (second read) | S86, `proportional-symbols` | The key's rings in the context ink at 1 px, lighter than the data circles' edges, as ruling (b) first set them |
| DD-A13, Should (second read) | S86, `proportional-symbols` | Each key step's width counts its ring's stroke, the gaps close to keep 1 px clear of the edge, and on a phone the circles shrink until the key fits with that 1 px; measured in Node at 256, 296, 320, 326, 358, 480, 558, 656 and 720 px: at least 1.00 px clear at every one, the county circle at least 21.6 px across |

## Tested

- Second set (21:3x UTC), after DD-A1 to DD-A13 and the editor's entry words: `oa-chart.mjs build s85 s86 s87 s88 --widths 1440,390,352,328,288`, sweep on, both grounds with grayscale: 4 PASS, 0 faults (S86 again after DD-A12 and DD-A13 with `--no-png`, sweep on: PASS; its PNGs wait for the machine's load to fall, per the main session's rule). `phase3_ch14_build.py --rounds 1,2,3,4`: 141 rules, 127 entries, 0 faults. `maker_a_round4_derive.py --figures`: 51 of 51.
- Final strict build to scratch (`guide-final.html`, 21:32 UTC, before DD-A12 and DD-A13): exit 1 on two warnings, both S95's card ("no place clear of the dots for Massachusetts 96", the infographics maker's); none names S85 to S88 or my sketches. 11,493,502 bytes. Plates as the guide places them: S85 4,228, S86 4,283, S87 4,694, S88 4,733 bytes, each about 750 more with its frame.
- After DD-A12 and DD-A13 (21:40 UTC, load under 3): `oa-chart.mjs build s86 --widths 1440,390,352,288`, sweep on: PASS, 0 faults; the key's rings looked at in the 1440 px Newsprint and 256 px Charcoal captures. Last strict build (`guide-last.html`): exit 0, no warning, 11,500,303 bytes; plates S85 4,228, S86 4,283, S87 4,694, S88 4,733 bytes.
- The quick guide check on my first strict build (`guide.html`) crashed after about 20 minutes ("page.goto: Target page, context or browser has been closed") under a machine load of about 8: not counted.

- `node work/build/chart-kit/oa-chart.mjs build s85 s86 s87 s88`, sweep on (256 to 720 px), PNGs at 1440 and 390 px pages on both grounds with grayscale: 4 of 4 PASS, 0 faults (S85 after A4-E1 landed, 21:19 UTC; S86 to S88 at 21:1x). Also built without the sweep at 328 and 288 px pages (296 and 256 px drawings) on both grounds, and S87 at 256 px pages (224 px drawing) after MA-9: PASS.
- Captures looked at as contact sheets, as a design director would at twice size: all four at 1440 px Newsprint; S86 to S88 at 358 px (S86 Charcoal, S87 and S88 Newsprint); S85 at 1440 px Newsprint, 358 px Charcoal and 256 px Newsprint with the icon and chip; S85, S86 and S88 at 256 px Newsprint and 296 px Charcoal in grayscale; S87 at 224, 256 (Charcoal, grayscale) and 296 px. Fixes that came of them: S86's key and words line moved, S86's names under the circles, S87's three-line region words and its leader, S85's chip on the name's baseline.
- `python3 -I work/build/scripts/phase-3/maker_a_round4_derive.py --figures`: 51 checks, 0 failed.
- Words lint by script on S85 to S88, entries 14.79 to 14.84 and both sketches: no em or en dash, U+2011, straight apostrophe in reader text, banned word or decision code; titles 14, 22, 25 and 20 words.
- Both sketches captured on Newsprint and Charcoal and in grayscale (my own page with tokens.css and kit.css): s-14-83 1,893 bytes, s-14-84 2,986 bytes; the rose's first `<desc>` holds `sketch_alt`'s first sentence (the generator's R2-3 check).
- `python3 -I work/build/scripts/phase-3/phase3_ch14_build.py --rounds 1,2,3,4`: my six entries, four specs and two sketches load with no fault; its five faults are the infographics maker's entries 14.136, 14.137, 14.138, 14.140 and 14.141, not yet written.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/guide.html` (21:15 UTC, before A4-E1): exit 0; its only warnings were S85's icon and chip, since cleared. Plates as the guide places them: S85 4,172, S86 4,233, S87 4,694, S88 4,733 bytes, each about 750 more with its frame, under the 12,495 share.

## Not tested

- Real screen readers, devices, print and 200 percent text; forced colors only through the kit's own checks (no `dataviz_check.js --kit` run).
- The CSV exports beyond S85's.

## Files

Created: `work/build/chart-kit/forms/icon-array.js`, `proportional-symbols.js`, `venn-diagram.js`, `euler-diagram.js`; `work/build/chart-kit/specs/s85.json` to `s88.json`; `work/build/guide/entries/14-079.json` to `14-084.json`; `work/build/guide/specimens/s-14-83-sketch.html`, `s-14-84-sketch.html`; `work/build/scripts/phase-3/maker_a_round4_derive.py` (checks only); this notes file.
Written by running the engineer's generator (`phase3_ch14_build.py --rounds 1,2,3,4`), not by hand: chapter 14's JSON, its manifest, the example log and the `s-14-s85.html` to `s-14-s88.html` fragments.
Outside the repository, by mistake: `/mtest.mjs`, a 289-byte minifier test script I wrote to the file system's root when a shell variable was empty (20:49 UTC). The sandbox's safety check refused my removal of it; it is harmless and needs a person to delete it.
Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/maker-a/` (kit-out, kit-4w, kit-dd, kit-final, kit-a12, the sketch generators and captures, contact sheets, the strict builds and their logs).
