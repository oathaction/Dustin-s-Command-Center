# Round 4 maker A notes: proportion and overlap

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. Maker A, briefed as a senior graphics editor at a newsroom known for exact, quiet charts, who draws exact share and overlap charts. Brief: `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`, the maker A row and its "Maker A" bullet. Rows: maker "A" in `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`, rules 14.79 to 14.84 (coverage plan 3.8). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/maker-a/`. Written as I go; the container can restart.

## Status

- 20:58 UTC (clock read 20:55). Rulings (a) to (c) read; applying them. Forms `icon-array`, `proportional-symbols` and `venn-diagram` drafted and building; `euler-diagram` next. S85 waits on A4-E1 (the icon part) and Q-A1 (its word and chip). Round 4's ceiling noted: 13,172 bytes a plate with its frame once S12's tile lands.
- 20:45 UTC (clock read 20:41). Started. Read `CLAUDE.md`, the round 4 brief, the plan file's round 4 rows, the round 4 data plan with its sign-off and "Conditions for round 4's maker", coverage plan 3.8, the kit README, round 3's maker A notes, DR-266 and D3-1679, Rules 10.1, 10.4 and 10.6, and my four data files with their sidecars. Writing the four forms now; named marks and inks wait on the data lead's "Rulings".

| Rule | Spec | Form ID | Status |
|---|---|---|---|
| 14.79 | S85 | icon-array | form and draft spec; waits on A4-E1 and Q-A1 |
| 14.80 | S86 | proportional-symbols | form and draft spec; passes |
| 14.81 | S87 | venn-diagram | form and draft spec; passes |
| 14.82 | S88 | euler-diagram | form next |
| 14.83 | sketch | packed circles (reference) | waiting |
| 14.84 | sketch | rose chart (avoid) | waiting |

## Summary

## Routine calls

## Requests

### Requests to the data lead

- **Q-A1, S85's topic word.** The editor's label table (`work/handoffs/phase-2/20261110_Stage-B-Ch10-Labels.json`) files CL-050 as an atlas variable: label "Worker bargaining power", chip "Variable A2" (V7 title "Workers' bargaining power"); its Civic Line word "Worker Bargaining" is the inventory's, for finding the drawing. Rule 10.6 sets an atlas drawing only beside the atlas's own name with its typed chip. I print "Worker bargaining power" beside the drawing (the approved label, checked by script) and ask whether the chip "Variable A2" prints beside it in the drawing, as chapter 10's register prints it. My reading: yes, since Rule 10.6 binds and the chip says why a picture of bargaining heads a chart of union membership (V7 files CL1514 under I101, collective bargaining). Say if you rule otherwise.

### Requests to the engineer

- **A4-E1, a Civic Line icon in a kit drawing (S85, DR-266).** S85 sets CL-050 once at 48 px beside its word. The kit has no part that draws a Civic Line drawing, and the guide's sprite holds CL-050 as `oa-sym-cl-050`. I ask for one shared part, such as `K.parts.icon(c, 'CL-050', x, y, 48)`, that draws the approved black master at the size given in the icon ink (`--oa-component-icon-ink`, the data lead's ruling (b); one color, no red accent), with `aria-hidden="true" focusable="false"`, `data-icon="CL-050"` and `data-icon-family` (Rule 10.6 and the chapter 10 construction file, section 11), as `<use href="#oa-sym-cl-050">` on the guide's page and with the drawing inline in the SVG and PNG exports, and that the checks see as a shape with a box, so no word sits on it. CL-050 is an atlas symbol (the editor's label table: "Worker bargaining power", chip "Variable A2"), so Rule 10.6 sets a typed chip beside its name: if the data lead rules the chip prints in the drawing, a chip part in the same call (`K.parts.chip(c, x, y, 'Variable A2')`, the chip-fill and chip-label roles kit.css already holds) would keep it in one style with the figure's HTML chips. Until it lands, S85 draws the name alone and fails its build on purpose (the form warns). The infographics maker's S89 takes no icon (ruling (b)), so this part is for S85 alone today.

## Tested

## Not tested
