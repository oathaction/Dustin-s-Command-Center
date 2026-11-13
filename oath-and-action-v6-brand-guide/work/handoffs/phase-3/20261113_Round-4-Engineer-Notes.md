# Round 4 engineer notes

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. Written by the engineer (`oa-engineer`) under `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/engineer/` (`scratch/` below).

## Status

Started 20:39 UTC (clock read).

- **R4-2, DR-261's measure: WRITTEN (20:50 UTC), for the data lead's sign-off.** Under "Contracts", R4-2. Share per plate 13,235 to **13,172** (63 bytes less a plate). The stacked tile is built and proved in a scratch mirror only; nothing in `work/build/` has changed. It lands in the kit once the data lead signs it off.
- R4-3, R4-4, R4-5 contracts: in progress.

## Summary

## Contracts

Round 0 to round 3 contracts and board 2's stand. Round 4's follow. A line marked **LANDED** is in the kit now; **MEASURED** or **SET** means written here and not yet in the kit.

### R4-2. DR-261: the stacked tile's measure (MEASURED 20:50 UTC, for the data lead's sign-off)

**What I built to measure it** (in a scratch mirror of the repository: the chart kit, the scripts and the guide folder copied, everything else linked read-only; its baseline strict build gives chapter 14 the committed share, 13,235, to the byte):

1. **`forms/tile-map-shift-arrows.js`, the stacked tile at a desk.** The cartographer's board 2 route (`work/handoffs/phase-3/board-2-pictures/20261113_S12-Stacked-Tile-Form.js`), made the form's only desk tile: each tile sets the state's code in bold on line 1 (baseline 16), its figure on line 2 (baseline 32, the kit's 16 px leading for 13 px text), and board 1's arrow beneath on board 1's scale rule (the tile less 14 px for the largest shift), its head 2 px clear of the figure's box, at the tile's foot less 10 px where there is room. The stacked tile fits where the arrowhead ends 1 px or more inside the tile and the widest code or figure ends 2 px or more inside its right edge: tiles of 46 px, from a 618 px drawing. Where it does not fit, the form draws the phone's gray steps (as today, board 1's phone drawing unchanged). The board's `labels.stack: "force"` is not carried: no spec can force the stacked tile where it overruns.
2. **`kit.js`, a floor for the stage: `spec.stage_min`.** A width in px. A desk drawing takes the column's width where the column gives `stage_min` or more, and draws at `stage_min` in the stage's scrolling frame (its tab stop, name, hint, edges and scroll bar, as RS-1 built them) where the column gives less; a phone column draws the phone form. `"stage_min": 618` gives DR-261's words exactly: the stacked tile in the column from a 618 px drawing (a 1,104 px window, the cartographer's measure), a 618 px frame that scrolls below that (62 px at a 1024 px window, where the column gives 556). `stage` (one fixed width) stays as it is for any spec that sets it; a spec sets one or the other, and the kit's check fails both, or a floor outside 480 px to the artboard. A spec with `stage_min` does not take the breakout over the rail that `phase3_ch14_build.py` gives a fixed stage, since DR-261 draws it in the column.
3. **`kit.js` and `checks.js`, the check D3-1546 asks for: cells.** A form may open a cell, `c.cell(x, y, w, h, {key, spare})`, and close it with `c.cell(null)`: every shape and word drawn while it is open must sit inside it with `spare` px (default 1) on every side, a stroke by half its width. `checks.js` (`check_drawing`, so `build`, `check` and the sweep at every width) fails one that leaves it: "chart: N cell(s) hold a shape or word that runs past the cell's edge less its spare (AL: polygon by 4.5 px; ...)". The page carries only the recording (the check never rides on the page). `tile-map-shift-arrows` opens a cell for each desk tile round its code, figure and arrow; the frame drawn round a tile whose leader changed sits outside the cell, as it should.

**The planted case** (`scratch/scripts/plant_overrun.mjs`, to join the kit's self-test when it lands): S12's spec and data, the form's fit test removed so the stacked tile draws at 558 px, the board's picture at a 1024 px window. The check fails it: **51 cells**, every arrowhead 4.5 px past the tile less its 1 px spare (the cartographer's 3.5 px overrun plus the spare), and on most tiles the tail dot and shaft too. The real form at the same 558 px draws the gray steps (0 cells, 0 faults); at 618, 723 and 1024 px it draws the stacked tile, 51 cells, 0 faults. Round 3's kit had no such check and passes the planted drawing.

**`build s12` in the mirror** (sweep on, every whole width 256 to 869 px; 1440 and 390 px on both grounds): PASS, 0 faults. Desk columns from 480 to 617 px draw at 618.

**The bytes** (each file minified as `kit_parts()` puts it on the page; the strict build's report in the mirror against the committed build's, 20:44 and 20:49 UTC):

| Part | Before | After | Change |
|---|---|---|---|
| `tile-map-shift-arrows.js` | 5,084 | 5,435 | +351 |
| `kit.js` | 52,722 | 53,112 | +390: the floor 104, the cell 286 |
| `kit.css`, `parts.js`, `metrics.js`, every other form | | | 0 |
| `checks.js`, `oa-chart.mjs` (off the page) | | | not page bytes |
| **The "chart kit" part on the page** | 512,961 | 513,702 | **+741** |
| Renderer grown to 97 forms (the share's measure: a form's growth counts 97 / 87 times, since it raises the average of the 10 forms still to come) | 557,494 | 558,276 | **+782** |
| S12's plate on the page, frame included (the island's `stage_min`, the manifest's breakout gone, the alt's added clause "with the state’s code over its figure", which is the cartographer's to word) | 14,042 | 14,076 | +34 |
| Chapter 14 as built | 1,582,230 | 1,582,264 | +34 |
| Chapter 14 with the kit | 2,228,308 | 2,229,083 | +775, against the 2,803,941 stop |
| Map geometry | 133,117 | 133,117 | 0 |
| **Share per plate, round 4's 13** | **13,235** | **13,172** | **−63** |
| Projected page | 15,044,827 | 15,044,827 by rule (chapter 14 is held to its allocation in the projection) | 0; read again on the first real strict build after landing |

**What the share falls to:** 13,172 bytes a plate, frame included, for S85 to S95 and the two sketch entries' successors (D3-1328's rule: none past 15,000). The drawing itself is drawn in the reader's browser and is not page bytes; the island, words and table of S12 do not change but for the 34 bytes above.

**After sign-off:** I land items 1 to 3 in the kit with the self-test case, `build s12` with captures at 1440, 1024, 768 and 390 px, the kit's `build --all --no-png`, and a strict build whose share I report here. The cartographer then writes `s12.json`: `"stage_min": 618` in place of `"stage": 1024`, its alt and phone words, and the `notes_internal` line (placement and words only; the form and its inks are the kit's).

## Routine calls

- D3-xxx | The stacked tile is S12's only desk tile; the board's `labels.stack: "force"` is not carried into the kit | DR-261 approves the stacked tile at a desk, and a key that draws a tile known to overrun would undo D3-1546's check
- D3-xxx | DR-261's frame is a floor on the stage, `stage_min`, beside the fixed `stage` | DR-261 draws the tile in the column from 618 px and scrolls only below it; a fixed stage would draw 618 px at every desk width
- D3-xxx | The overrun check reads cells a form declares, in `checks.js`, and the page carries only the recording | D3-1546: the layout guard does not read a tile's edge against its arrow; the sweep draws every width the guide gives, so the check need not ride on the page
- D3-xxx | A cell's spare is 1 px by default | The cartographer's board 2 measure called a tile "held" at 1 px or more to spare on every side

## Requests

## Tested

- R4-2 (scratch mirror only): baseline strict build in the repository (20:44, exit 0, 0 warnings, share 13,235; `plate-share.json`'s timestamp alone changed, so the committed file was put back) and in the mirror (chapter 14 the same, share 13,235); the mirror's `build s12` with the sweep, PASS; the planted case caught and the real form clean at 558, 618, 723 and 1024 px; two mirror strict builds measured (share 13,166 with a first, larger cell, then 13,172); each page part minified and compared.

## Not tested

- The stacked tile in a browser: no capture yet (after sign-off, at landing).
