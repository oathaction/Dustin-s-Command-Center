# Round 4 maker A notes: proportion and overlap

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. Maker A, briefed as a senior graphics editor at a newsroom known for exact, quiet charts, who draws exact share and overlap charts. Brief: `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`, the maker A row and its "Maker A" bullet. Rows: maker "A" in `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`, rules 14.79 to 14.84 (coverage plan 3.8). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/maker-a/`. Written as I go; the container can restart.

## Status

- 20:45 UTC (clock read 20:41). Started. Read `CLAUDE.md`, the round 4 brief, the plan file's round 4 rows, the round 4 data plan with its sign-off and "Conditions for round 4's maker", coverage plan 3.8, the kit README, round 3's maker A notes, DR-266 and D3-1679, Rules 10.1, 10.4 and 10.6, and my four data files with their sidecars. Writing the four forms now; named marks and inks wait on the data lead's "Rulings".

| Rule | Spec | Form ID | Status |
|---|---|---|---|
| 14.79 | S85 | icon-array | form started |
| 14.80 | S86 | proportional-symbols | waiting |
| 14.81 | S87 | venn-diagram | waiting |
| 14.82 | S88 | euler-diagram | waiting |
| 14.83 | sketch | packed circles (reference) | waiting |
| 14.84 | sketch | rose chart (avoid) | waiting |

## Summary

## Routine calls

## Requests

### Requests to the engineer

- **A4-E1, a Civic Line icon in a kit drawing (S85, DR-266).** S85 sets CL-050, Worker Bargaining, once at 48 px beside its word. The kit has no part that draws a Civic Line drawing, and the guide's sprite holds CL-050 as `oa-sym-cl-050`. I ask for one shared part, such as `K.parts.icon(c, 'CL-050', x, y, 48)`, that draws the approved black master at the size given in one ink (the text's ink, no red accent, so the plate keeps one working red), hidden from screen readers (Rule 10.6: the word beside it is read once), as `<use href="#oa-sym-cl-050">` on the guide's page and with the drawing inline in the SVG and PNG exports, and that the checks see as a mark with a box (so a word never sits on it). Until it lands, S85 draws no icon and holds its place. The infographics maker's S89 may want the same part for actors (data plan row 121).

## Tested

## Not tested
