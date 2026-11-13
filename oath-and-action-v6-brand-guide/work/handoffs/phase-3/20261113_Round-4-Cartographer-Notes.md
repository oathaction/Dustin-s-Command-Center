# Round 4 cartographer notes: phone codes and S12's stacked tile

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. The cartographer, a senior news cartographer (general-purpose, as round 3's and board 2's). Brief: `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`, the cartographer row and its "Cartographer" bullet, under DR-261 and D3-1553. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch (`scratch/` below): `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/cartographer/`. Written as I go; the container can restart.

## Status

- 21:02 UTC (clock read). **S12 placed on the landed stacked tile** (`s12.json`: `stage_min` 618, the alt's clause, one `notes_internal` line): `build s12`, sweep on, PASS, 0 faults. **D4-1 ruled (A), the column** (20:57). Waiting on the engineer for C4-E1 (tile gap) and C4-E2 (S16's column, after the tile); then I add `labels.column_phone` to `s16.json`, name the radius check in its `notes_internal`, and run the closing checks. `cartographer_round4_derive.py` written: PASS on the mirror with both changes, FAIL with the six expected faults on the repository until they land.
- 20:56 UTC (clock read). **Phone codes: measured, two kit requests out (C4-E1, C4-E2), one choice for the data lead (D4-1).** No repository file changed yet. S12's stacked tile: ruling (d) signed off at 20:52; I write `s12.json` when the engineer marks the tile LANDED.
- 20:40 UTC. Started.

## Summary

At the guide's 326 px phone drawing (a 390 px window) today:

| Spec | Codes drawn at 326 px | Left to the note | Why |
|---|---|---|---|
| S12 (phone tiles) | 48 of 51 | WA, WV, WY | Tiles of 24 px; "WA" and "WV" measure 22.72 px and "WY" 22.53 px at 13 px semibold, past the 22 px a tile holds with 1 px a side |
| S78 (phone tiles) | 48 of 51 | WA, WV, WY | The same tile grid and test |
| S16 (bubbles) | 47 of 51 | DC, DE, ME, NH | The Northeast is boxed in by the drawing's right edge; no clear place within reach |

Proposed, each tested in a scratch mirror of the kit (nothing in `work/build/` changed):

- **S12 and S78: a 2 px tile gap on phones (C4-E1).** Tiles become 25 px at 326 px and every code fits with 1.14 px or more a side: all 51 coded on both maps from 322 to 479 px (today from 328), 0 faults. Under 322 px nothing gets worse (300 px: 43 coded, today 41; 296 px: 41, as today).
- **S16: a column of codes on the ocean for the small northeastern states, on phone drawings narrower than 358 px (C4-E2), or the note as today (D4-1).** At 326 px all 51 coded, with fewer leaders crossing a circle (11, today 15) and a shorter longest leader (72 px, today 104). From 358 to 479 px the drawing is identical to today at all 122 widths. Across 300 to 357 px the codes left out fall from 217 to 44 (summed over the 58 widths).

## Routine calls

- D3-xxx | The phone codes are fixed by the tile grid's gap (S12, S78) and a code column (S16), each in the kit by request; no font size, weight, word or ink changes | Rule 13's type floor is 13 px for tile codes (`type-tile-code-phone`), and D3-1325's 1 px a side stands; the only free variable is room
- D3-xxx | S16's column takes ME, NH, VT, MA, RI, CT, NJ, DE, MD, DC and WV, ordered by their circles from north to south, slots 16 px apart as near each circle's height as the pitch allows | Of four lists tried, this one left the fewest codes out with no leader thrown below Florida (lists without WV threw one at 326 px; adding VA, NC, SC and GA cost crossings and two sweep faults)
- D3-xxx | S16's column applies only under the phone artboard's 358 px | Today's search codes all 51 at 358 px (board 1's phone width, D3-1329, D3-1527), and the column there would drop NC; at 358 px and over nothing changes

## Requests

### To the engineer

- **C4-E1, the phone tile gap (S12, S78; D3-1553).** `--oa-chart-tile-phone-gap` from 2.5 px to 2 px (`work/build/tokens/src/oa-tokens.src.mjs`, `tile.phoneGap: chartDim(2.5, ...)`; diff of the built file in `scratch/requests/C4-E1_tile-phone-gap.diff`). At 326 px `K.parts.tiles` then gives 25 px tiles at a 27 px pitch, every tile edge on a whole pixel, and the widest codes ("WA", "WV", 22.72 px) fit with 1.14 px a side. Tested by patching `P.tiles` in the mirror (`gap = c.phone ? 2 : ...`): S12 and S78 code all 51 at 322, 326, 327, 328, 358, 390 and 479 px, 0 drawing faults at each. S07's phone tiles also grow 1 px (S07 draws no codes on a phone at these widths; 0 faults), so S07 would join board 3's list of changed drawings. If you would rather leave S07, a form-level gap for the two forms that code their tiles (`tile-map-shift-arrows`, `choropleth`'s phone tiles) does the same; no spec key is needed either way. No page bytes either way but a token value.
- **C4-E2, a code column on S16's phone drawing (D3-1553), if the data lead rules for it (D4-1).** `forms/bubble-map.js` takes `labels.column_phone` (codes) and `labels.column_under` (default the token `artboard-phone`, 358 px): on a phone drawing narrower than that, and not in the narrow mode under 300 px, the map fits narrower by the widest listed code plus 10 px, and the listed states whose circles cannot hold their code take a column at the right edge, in the order of their circles from north to south, slots 16 px apart placed as near each circle's height as that pitch allows (pool adjacent violators, so every run matches), each on a hairline leader from its circle's edge to 2 px short of its code; the search places the rest around them and keeps clear of the column's leaders. Patch: `scratch/requests/C4-E2_bubble-map-column.diff` (83 lines; the whole form is `C4-E2_bubble-map.js`); minified, the form grows from 10,455 to 11,850 bytes (+1,395). The spec I would then write is `scratch/requests/C4-E2_s16-with-column.json` (only `labels.column_phone` added). Tested in the mirror: `build` of that spec with the sweep (256 to 869 px on Newsprint, 1440 and 358 px pages on both grounds): PASS, 0 faults, plate 10,235 bytes as the guide places it (+52). Until it lands I add nothing to `s16.json`, since the kit fails a label key the form does not read.

### To the data lead

- **D4-1, S16 at 326 px: the column, or the note (D3-1553's "a ruling where a choice is needed").** (A) The column (C4-E2): every state coded at 326 px; 22 leaders, 11 crossing another state's circle (today 14 and 15), longest 72 px (today 104); the eleven column codes sit 41 to 84 px from their circles by design, in latitude order; the South's codes stay the search's, as today (GA's sits under Florida at 326 px, where today MD's does). Unchanged from 358 px up. Costs 1,395 bytes of renderer. (B) The note as today: "Not labeled at this width: DC, DE, ME, NH. The table names every one." Pictures: `scratch/exp/s16-o-map.png` (today, 326 px, 3x), `scratch/exp/s16-w3-map.png` (column, 326 px, 3x), `scratch/exp/s16-col-charcoal-326-map.png` (column on Charcoal, the kit's own export). I recommend (A).

## S12's stacked tile (DR-261, ruling (d))

**Placed at 21:01 UTC** (the tile LANDED at 20:57), from the draft below, unchanged. Drafted in scratch first: `scratch/draft/s12.json` changes `s12.json` in three places only: `"stage_min": 618` where `"stage": 1024` stood; the alt's desk clause reads "At a desk each square holds the state’s code over its figure, with an arrow beneath as long as the state’s shift ..." (was "holds an arrow as long as the state’s shift ..."), the scroll clause and every other word kept, since the frame still scrolls below a 618 px column; and one `notes_internal` line. `phone_note` stays: the kit does not print it, and its words still hold. Built against a copy of the engineer's mirror kit (20:57 UTC): PASS, 0 faults, sweep on; drawings at 1024, 723, 618, 618 (the 558 px column, framed) and 326 px; 13,206 bytes as the guide places it, about 13,956 with its frame, under 15,000 (ruling (d) gives 14,076 by the page measure). Looked at: 618 px on Newsprint (every tile holds its code, figure and arrow) and the 558 px column's frame (the hint above it; ME, NH and RI past the edge until the reader scrolls).

## Pixels changed, for board 3

(Filled in as changes land.)

## Tested

- `node work/build/chart-kit/oa-chart.mjs build s12 s16 s78 --widths 1440,787,682,358 --no-sweep --out scratch/before/kit-out` (20:44 UTC): 3 of 3 PASS, 0 faults; the "before" captures for board 3 (kit pages 358, 682, 787 and 1440 px give the guide's 326, 618 and 723 px drawings and the 1024 px stage). Before copies of the three specs and three entries in `scratch/before/`.
- By the kit's draw (no browser, `scratch/tools/probe_codes.mjs`), codes drawn today at 256, 296, 300, 326, 358 and 390 px on S12, S16 and S78 (table above); code widths by `K.measure` at 13 px.
- In the mirror (`scratch/tools/mirror.sh`: the chart kit copied, tokens, fonts, data and atlas extract linked read-only): the 2 px phone gap on S12, S78 and S07 at nine widths; S16 with longer reach, finer rings, a right margin, and four column lists; `scratch/tools/quality.mjs` over every whole width from 300 to 479 px for today and each column list (codes, leaders, crossings, distance); the column variant's kit `build` with the sweep (above).
- Looked at, 3x, Newsprint: S16 at 326 px today, with three search settings, and with three column lists; the chosen column on Charcoal from the kit's export at 2x.

## Not tested

- The tile gap through the token itself (tested by patching `P.tiles`, which reads the token); the guide page; grayscale of the column by eye.

## Files

Nothing in the repository yet but this notes file. Scratch: `before/`, `exp/`, `requests/`, `tools/`, `mirror/`.
