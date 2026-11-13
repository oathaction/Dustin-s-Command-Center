# Round 4 maker A notes: proportion and overlap

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. Maker A, briefed as a senior graphics editor at a newsroom known for exact, quiet charts, who draws exact share and overlap charts. Brief: `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`, the maker A row and its "Maker A" bullet. Rows: maker "A" in `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`, rules 14.79 to 14.84 (coverage plan 3.8). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/maker-a/`. Written as I go; the container can restart.

## Status

- 21:16 UTC (clock read 21:13). All four forms, specs S85 to S88, entries 14.79 to 14.84 and both sketches are written. S86, S87 and S88 build PASS with the sweep, 0 faults; S85 fails only for the icon and chip parts it waits on (A4-E1). The data lead's MA-1 to MA-8 and Q-A1, the research lead's R-1 variant and the editor's first and second looks are applied. Figure checks 51 of 51. Next: strict build, quick guide check on the sketches, and the design director's read.
- 20:58 UTC (clock read 20:55). Rulings (a) to (c) read; applying them. Forms `icon-array`, `proportional-symbols` and `venn-diagram` drafted and building; `euler-diagram` next. S85 waits on A4-E1 (the icon part) and Q-A1 (its word and chip). Round 4's ceiling noted: 13,172 bytes a plate with its frame once S12's tile lands.
- 20:45 UTC (clock read 20:41). Started. Read `CLAUDE.md`, the round 4 brief, the plan file's round 4 rows, the round 4 data plan with its sign-off and "Conditions for round 4's maker", coverage plan 3.8, the kit README, round 3's maker A notes, DR-266 and D3-1679, Rules 10.1, 10.4 and 10.6, and my four data files with their sidecars. Writing the four forms now; named marks and inks wait on the data lead's "Rulings".

| Rule | Spec | Form ID | Status |
|---|---|---|---|
| 14.79 | S85 | icon-array | form, spec, entry; fails only on A4-E1 (icon and chip parts) |
| 14.80 | S86 | proportional-symbols | form, spec, entry; PASS with the sweep |
| 14.81 | S87 | venn-diagram | form, spec, entry; PASS with the sweep |
| 14.82 | S88 | euler-diagram | form, spec, entry; PASS with the sweep |
| 14.83 | sketch | packed circles (reference) | sketch 1,893 bytes, entry |
| 14.84 | sketch | rose chart (avoid) | sketch 3,037 bytes, entry |

## Summary

## Routine calls

- D3-xxx | S85 draws its 100 marks larger than the unit chart's 14 px squares: 24 px with 4 px gaps at a desk, up to 22 px with 3 px gaps on a phone, a row of ten always | DR-266's plain unit marks in their style (filled, open), sized so a hundred stay countable in a 720 px column; one grid at every width (ruling (b))
- D3-xxx | S85's key words sit beside their marks: "Union member" beside the filled row and "Not a member" beside the first open row at a desk, both under the grid on a phone, each with its swatch | Ruling (b): the key in the file's words, each beside its mark
- D3-xxx | S85's table prints all four published rows (2025 all workers, private, public, 1983) and the array draws the 2025 row alone through `labels.draw`, the limitation in the table's caption | Ruling (b): the table prints the published figures with V7's limitation as its caption note; the kit has no separate table note
- D3-xxx | S85's topic: CL-050 at 48 px, "Worker bargaining power" beside it and the chip "Variable A2" after it, all above the grid | Q-A1 and Rule 10.6; checked by script against the editor's label table and chapter 10's list of 41
- D3-xxx | S86 sets the federal government and the states in one line over the circles, "Not drawn: 1 federal government and 50 state governments, too few to draw at this scale.", with a hairline under it | Ruling (b) ("above or beside the circles with a hairline gap"); above, the five circles take the column's full width at a desk (the largest 196 px across at 720 px against about 140 with the words at the left)
- D3-xxx | S86 keeps the Bureau's order (county, municipal, township, special district, independent school district), the file's `order`, in the drawing and the table | The plan's levels read in the order the Bureau prints them; drawing and table read alike
- D3-xxx | S86's special districts print their name and count inside their circle, in the label-on-subject ink, where both fit each chord with 6 px to spare; every other circle is named under it at a desk and beside it on a phone | Ruling (b)
- D3-xxx | S86's key draws three nested circles in the context ink with a hairline leader to each count, under the circles at the left | MA-5; the key is as tall as the largest circle, which the design director may weigh
- D3-xxx | S87's circles overlap by 1.2 times the radius between centers at a desk and 1.12 on a phone, the frame full width with the two circles centered, "No coverage" beside the second circle where it fits and in a band under the circles where it does not | Equal circles carry no count; the overlap wide enough for "Both", its count and share at 256 px
- D3-xxx | S87 and S88 print each group's name, count and share on their own lines, inside the group where each line fits its region at its own height with 4 px to spare, the label size first, then the tick size, then narrower | Ruling (b), "inside the region where it fits with 4 px to spare"; one rule in both forms, so the pair reads as one file drawn two ways
- D3-xxx | S88 finds the distance between the two centers that gives the shared area by bisection on the lens formula and fails the drawing past 1 percent; the kit's `area_of` check holds each radius | Ruling (b): each drawn area within 1 percent of its count at every width, named in `notes_internal`
- D3-xxx | S88's overlap words ("Both", 23.8 million, 7.1%) sit under the circles on a leader at every width, since the overlap is 0.45 of the larger radius wide | Ruling (b), a leader in the context ink where the words do not fit
- D3-xxx | S88 places "No coverage" beside the pair at a desk, its circle one radius clear of the public circle, and under the pair on a phone with its words beside it | Ruling (b): a gap at least its own radius
- D3-xxx | S87's and S88's titles: S87 lists the four groups; S88 states the two circles and their overlap ("In 2025, 213.2 million people had private health coverage and 119.1 million had public coverage, and 23.8 million had both.") | MA-8 and the editor's words: two findings from one file, each in its drawing's terms
- D3-xxx | No derived file this round: the derive script only checks figures (`--figures`, 51 checks) | S85 to S88 draw the research lead's frozen files as they stand
- D3-xxx | The packed circles sketch draws an illustrative city budget of 12 lines packed by a greedy tangent search, the four largest named, track ink with a context edge | R3-9's frame (320 px, 10 px inset); the same budget the mind map sketch uses, so the two reference sketches read as one family
- D3-xxx | The rose chart sketch draws four illustrative values as quarter wedges whose radius is the value (A 2, B 4, C 3, D 1) beside bars of the same values from one zero line | R3-9's frame (two 288 px halves of one height); "a value twice another looks four times as large" is A against B
- D3-xxx | I ran `phase3_ch14_build.py --rounds 1,2,3,4` so my entries reach the chapter file for my own strict build | The generator's default builds rounds 1 to 3 (DR-253); its five faults are the infographics maker's entries not yet landed

## Requests

### Requests to the data lead

- **Q-A1, S85's topic word.** The editor's label table (`work/handoffs/phase-2/20261110_Stage-B-Ch10-Labels.json`) files CL-050 as an atlas variable: label "Worker bargaining power", chip "Variable A2" (V7 title "Workers' bargaining power"); its Civic Line word "Worker Bargaining" is the inventory's, for finding the drawing. Rule 10.6 sets an atlas drawing only beside the atlas's own name with its typed chip. I print "Worker bargaining power" beside the drawing (the approved label, checked by script) and ask whether the chip "Variable A2" prints beside it in the drawing, as chapter 10's register prints it. My reading: yes, since Rule 10.6 binds and the chip says why a picture of bargaining heads a chart of union membership (V7 files CL1514 under I101, collective bargaining). Say if you rule otherwise.

### Requests to the engineer

- **A4-E1, a Civic Line icon in a kit drawing (S85, DR-266).** S85 sets CL-050 once at 48 px beside its word. The kit has no part that draws a Civic Line drawing, and the guide's sprite holds CL-050 as `oa-sym-cl-050`. I ask for one shared part, such as `K.parts.icon(c, 'CL-050', x, y, 48)`, that draws the approved black master at the size given in the icon ink (`--oa-component-icon-ink`, the data lead's ruling (b); one color, no red accent), with `aria-hidden="true" focusable="false"`, `data-icon="CL-050"` and `data-icon-family` (Rule 10.6 and the chapter 10 construction file, section 11), as `<use href="#oa-sym-cl-050">` on the guide's page and with the drawing inline in the SVG and PNG exports, and that the checks see as a shape with a box, so no word sits on it. CL-050 is an atlas symbol (the editor's label table: "Worker bargaining power", chip "Variable A2"), so Rule 10.6 sets a typed chip beside its name: if the data lead rules the chip prints in the drawing, a chip part in the same call (`K.parts.chip(c, x, y, 'Variable A2')`, the chip-fill and chip-label roles kit.css already holds) would keep it in one style with the figure's HTML chips. Until it lands, S85 draws the name alone and fails its build on purpose (the form warns). The infographics maker's S89 takes no icon (ruling (b)), so this part is for S85 alone today.

## Tested

## Not tested
