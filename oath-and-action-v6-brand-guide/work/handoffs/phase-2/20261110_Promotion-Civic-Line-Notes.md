# Promotion: Civic Line hand's notes

Oath & Action Edition 06, Phase 2, stage B, November 10, 2026. Written by the Civic Line icon designer (the design director role, one hand for the Civic Line family, D2-498), run as a subagent of the main session, for item 1 of `20261110_Promotion-Brief.md`. I started this file before the work and added to it as each part landed.

I read, in order: `.claude/agents/oa-design-director.md`, `CLAUDE.md`, the promotion brief, the decision log from DR-156 to DR-186 and D2-709 to D2-718, the October report `work/ledger/20261029_Civic-Line-Icons-Report.md`, the October inventory (CSV and JSON), the October pipeline in `work/build/scripts/civic-line/` (`cl_common.py`, `cl_svg.py`, `cl_tiles.py`, `build_tiles.py`, `build_icon.py`, `tile_calibration.py`, `verify_set.py`, `stroke_width.py`, `export_all.py`), the `icons_*` scripts in `work/build/scripts/phase-2/`, the stage B scripts named in the brief, the three stage B manifests, my stage B notes, the October variant review (sections S-1, S-2 and M-1) and the drawings board's figures file.

One note on sources. The brief points at the `icons_*` scripts in `work/build/scripts/phase-2/` for how the October set was built. Those scripts drew the October 28 pillar concepts board. The October Civic Line set was built by `work/build/scripts/civic-line/`, so that is the code this promotion reuses.

## Status

Done. Every check below passes, apart from one look-alike flag that the drawings board already showed (CL-014 against CL-035). Nothing is committed or pushed.

## What I promoted

**The Civic Line set in use, `work/build/assets/civic-line-v6/`.**

- `red-black/`, `black/`, `red-newsprint/` and `newsprint/` hold 124 SVGs each, 496 in all. The 116 unchanged drawings are October's files, copied byte for byte under their October names. The six redraws and the two new drawings are finals named `20261110_Oath-And-Action-Civic-Line-<ID>-<Slug>-<Edition>.svg`.
- Each final is its approved option's red-black or black file with four things changed: the root id and the ids that start with it (now October's pattern, `oa-civic-line-cl-025-red-black`), `data-id` (now the ID, so Testify reads `CL-073`), the title (the drawing's label, as October's titles are) and the description. The description says what the drawing shows, that it is the final approved by name on the stage B drawings board, the pick and its DR, and the promotion date.
- The Newsprint and Red-Newsprint editions of the eight come from the red-black final by October's own swap, `cl_svg.derive_editions` (DR-09): Charcoal lines become Newsprint, and in the Newsprint edition the red becomes Newsprint too.
- `png-256/` and `png-512/` hold the eight finals' previews in October's layout (one folder per edition, transparent ground): 64 PNGs, drawn by October's renderer.
- `tiles/` holds the eight finals' tiles in October's layout: six folders (square, rounded and circle, each on Charcoal and on Newsprint), each with `svg/`, `png-256/` and `png-512/`. That makes 12 tiles per drawing, 96 SVGs and 192 PNGs, written by October's tile code (`cl_tiles.tile_svg`, DR-10).
- `20261110_Civic-Line-V6-Inventory.csv` and `.json` hold 124 rows (D2-716). The 116 unchanged rows point at their October PNGs and tiles in `../civic-line/`.

**The pillar icons, `work/build/assets/pillar-icons/`.**

- `svg/` holds 16 files: CL-019 Explain, CL-020 Track, CL-021 Connect and CL-022 Act at 24 px (fit B) and 16 px (fit A), each in black and red-black, named `20261110_Pillar-Icon-<ID>-<Word>-<24px|16px>-<Black|Red-Black>.svg`. Each root carries `data-id` and `data-size`.
- `png/` holds 32 previews, at 1x and at 2x (`-2x.png`).
- `20261110_Pillar-Icons-Manifest.json` states DR-179's rule (the fits on 1x screens, the masters at 24 px on 2x screens), D2-634 for 16 px on 2x screens (the fit stays), and D2-497 (the black edition is the one in use under 48 px; the red-black edition is kept as the record of DR-133's red placements). It lists each file with its size, fit, line, edition, sprite symbol id, source file, hash and pixel map, and the four masters a 2x screen draws at 24 px.

**The script.** `work/build/scripts/phase-2/civic_line_v6_promote.py`, run with `python3 -I`. It builds everything above and then runs its checks; `--check-only` runs the checks alone. It imports the October modules and changes nothing on disk outside the two output folders.

## Every final and its source

Option files are in `work/build/assets/civic-line-redraws/svg/` or `work/build/assets/civic-line-new-topics/svg/`; the finals are in `work/build/assets/civic-line-v6/<edition>/`. Hashes are the first 12 hex digits of SHA-256; the inventory JSON carries the full hash of every SVG in use.

| ID | Label | Pick | DR | Source (option file stem) | Final red-black | Option red-black | Final black | Option black |
|---|---|---|---|---|---|---|---|---|
| CL-025 | Congress | Set B | DR-156 | `20261109_CL-025-Congress-Option-B` | `85c2ea9b5310` | `0d3c91d5bb9a` | `c2a9991b1dcf` | `a9ac5681c0e9` |
| CL-014 | Entrenched Power | Option C | DR-156 | `20261109_CL-014-Entrenched-Power-Option-C` | `44a6a488dee0` | `0a3636f42ed8` | `ba40796c8874` | `52d6d3600f08` |
| R-13 | Congressional Capacity | Set B | DR-156 | `20261109_R-13-Congressional-Capacity-Option-B` | `d9010bbd80f3` | `9ae7086d9573` | `d223282952d3` | `85c822fb3dc3` |
| R-42 | Congressional Tariff Votes | Set B | DR-156 | `20261109_R-42-Congressional-Tariff-Votes-Option-B` | `1cdb142f518a` | `88fc9b74298d` | `bb64e7a987c8` | `1446e5607fd8` |
| CL-059 | Credit Allocation | Option B | DR-157 | `20261109_CL-059-Credit-Allocation-Option-B` | `74350bed7e5a` | `029217170ad2` | `468b12f2af73` | `5154ca81f6c6` |
| R-48 | Agency Independence | Option C | DR-158 | `20261109_R-48-Agency-Independence-Option-C` | `c54dbb900f36` | `935d1601541e` | `bbcd2d68adad` | `a17ab48c023f` |
| CL-073 | Testify | Option A | DR-159 | `20261109_Testify-Option-A` | `4c6e71f49cde` | `ed1d20e81ac8` | `32ca8105bd01` | `d3572f476e34` |
| CL-074 | Contact an Official | Option A | DR-160 | `20261109_Contact-An-Official-Option-A` | `32c4d277a96f` | `40b97cfea51c` | `98bd79fdce0f` | `39ffab8bab23` |

The final's hash differs from its option's because the ids, title and description differ; the comparison below shows that nothing else does.

| Pillar icon | Source fit file (`work/build/assets/pillar-pixel-fit/svg/`) | Final black | Fit black |
|---|---|---|---|
| CL-019 Explain, 24 px | `20261109_CL-019-Explain-24px-Fit-B-*` | `18d14cde4f75` | `68378b251fd2` |
| CL-019 Explain, 16 px | `20261109_CL-019-Explain-16px-Fit-A-*` | `945612e61313` | `df8a22087b08` |
| CL-020 Track, 24 px | `20261109_CL-020-Track-24px-Fit-B-*` | `00bdf3df27b3` | `940c2a6c336e` |
| CL-020 Track, 16 px | `20261109_CL-020-Track-16px-Fit-A-*` | `d17f141f8bc9` | `9e7f31cd70e2` |
| CL-021 Connect, 24 px | `20261109_CL-021-Connect-24px-Fit-B-*` | `a8273bc8eca8` | `6ccd045174a9` |
| CL-021 Connect, 16 px | `20261109_CL-021-Connect-16px-Fit-A-*` | `e757165fb28f` | `e113625b4855` |
| CL-022 Act, 24 px | `20261109_CL-022-Act-24px-Fit-B-*` | `989029ca6c06` | `eacb8cde12d9` |
| CL-022 Act, 16 px | `20261109_CL-022-Act-16px-Fit-A-*` | `8f5442f926e6` | `7dfc270ac733` |

The red-black pillar finals and their hashes are in the manifest.

## The checks' figures

**Byte and path checks.**

- Unchanged copies: 464 of 464 SVGs (116 drawings in four editions) hash the same as their October files. The SHA-256 of the sorted list of names and hashes is `0bd6afb16398f26de982dfd2775e69b0acb02fc79b60ec051f18157e1b6f6302`.
- Finals, red-black and black: with the root id, `data-id`, title and description put back, each of the 16 files equals its approved option file byte for byte. So every `d`, every shape and every attribute is the option's.
- Finals, light editions: each of the 16 Newsprint and Red-Newsprint files, put back the same way, equals October's swap of the option's red-black file byte for byte. October's tree check (`verify_set.tree_identity`) agrees: the black and light editions match the red-black final element for element, with ink colors the only change (15 to 35 elements per drawing).
- The drawing behind the transform: each stage B source drawing, baked again with the stage B code, gives its option file byte for byte. So the inventory's scale, center and line weight belong to the drawing in use.
- October's structure checks (`verify_set.check_svg`) on all 32 final SVGs: viewBox `0 0 128 128`, only the edition's inks, no red in a black or Newsprint file, ids that start with the root id, nothing drawn outside the box. No error.
- Pillar finals: with the ids, title, description and `data-size` put back, each of the 16 equals its fit file byte for byte. The 32 PNG previews, drawn again from the finals, equal the stage B previews pixel for pixel.
- Ids across the set in use: October's id audit over 2,000 SVGs (496 bare files, 1,488 tiles in use and the 16 pillar files) finds 9,248 ids, none repeated, and 224 references, all resolved.
- Inventory: 124 rows in the JSON and the CSV, 6,076 paths checked and none missing, no empty CSV cell outside the flags column.
- Counts: 124 SVGs in each edition folder; 8 PNGs in each of the eight preview folders; 288 tile files; 16 pillar SVGs and 32 pillar PNGs.

**Before using October's code, I checked that it still makes October's files here.** Re-rendering CL-059's four October editions at 256 and 512 px gave October's PNGs pixel for pixel, and one tile PNG byte for byte. October's tile code rebuilt the 72 tiles of six October drawings byte for byte.

**Tiles (DR-10).** October's tile check (`verify_set.check_tile`) passes for all 96 tile SVGs: the shape first and exact, one group with one transform, the icon's geometry equal to its bare file, the line at or under 3.3508 units. All 192 tile PNGs pass October's PNG check. The smallest ink-to-edge margin per final, in units of 128, against October's floor of 12:

| ID | Square | Rounded | Circle | Optical scale | Offset | Tile line | Bare floor | Smallest tile, one-color | Smallest tile, two-color |
|---|---|---|---|---|---|---|---|---|---|
| CL-025 | 27.2 | 28.3 | 30.2 | 1.00 | 0 | 3.35 | 32 px | 48, 52, 52 | 72, 76, 80 |
| CL-014 | 22.6 | 23.8 | 24.7 | 1.05 | 0 | 3.25 | 48 px | 72, 76, 80 | 72, 76, 80 |
| R-13 | 33.6 | 34.3 | 26.7 | 0.95 | 0 | 3.18 | 48 px | 72, 76, 80 | 72, 76, 80 |
| R-42 | 34.9 | 35.7 | 28.4 | 0.96 | 0 | 3.22 | 48 px | 72, 76, 80 | 72, 76, 80 |
| CL-059 | 29.5 | 30.4 | 24.3 | 0.94 | 0 | 3.15 | 32 px | 48, 52, 52 | 72, 76, 80 |
| R-48 | 24.6 | 25.7 | 27.5 | 1.00 | 0 | 2.70 | 48 px | 72, 76, 80 | 72, 76, 80 |
| CL-073 | 27.7 | 28.7 | 25.9 | 0.94 | 0 | 3.15 | 32 px | 48, 52, 52 | 72, 76, 80 |
| CL-074 | 21.0 | 22.3 | 22.8 | 1.09 | 0 | 3.16 | 48 px | 72, 76, 80 | 72, 76, 80 |

Smallest tile sizes run square, rounded, circle, in px.

How the optical scale and offset were set. The variant review gave the 122 masters their values from two rules, S-1 (size) and S-2 (sideways shift), measured on renders. I apply the same rules on the build's own vector hull (`cl_tiles.hull_size`), dividing by that hull's median over the 122 masters (74.66 units) in place of the review's 74.4, so the measure and its median match. Run over the 122 masters, this form gives the review's table for 116 of the 118 icons outside the pillar group under S-1 (CL-072 and R-44 come out one step lower, 0.01) and for 122 of 122 under S-2. With 74.4 instead, two finals would move one step: R-42 to 0.95 and CL-074 to 1.08. No final reaches S-2's shift threshold.

Three finals change from their October originals' tile values. CL-014 goes from 0.95 to 1.05 (the new drawing is wide and low), R-13 from 1.05 to 0.95 (the new drawing fills its box), and R-48's one-color tiles rise from 48, 52 and 52 px to 72, 76 and 80 px because the new drawing stops reading at 32 px.

**Bare floors (October review, section 6).** I read each final at 32 and 24 px true size and enlarged. CL-025, CL-059 and CL-073 read at 32 px. CL-014, R-13, R-42, R-48 and CL-074 stop reading at 32 px: each combines three parts or leans on a small sign (the ballot's check, the chart line, the yes and no, the arrow at the brace, the speech mark). None reads at 24 px, as DR-136 expects. This is my reading as an agent, not a person's.

**Look-alike check** (`node work/build/scripts/phase-2/icon_likeness_check.js`, on the eight black finals; flag line 0.9127, watch line 0.8708, as on the board).

Against the 122 October masters, the check gives every figure the drawings board printed for the eight picks, to four places:

| ID | Closest master | Likeness | Board | Own original | Board |
|---|---|---|---|---|---|
| CL-025 | CL-014 Entrenched Power | 0.8961 (watch) | 0.8961 | 0.8670 | 0.8670 |
| CL-014 | CL-035 Residential Sorting | 0.9259 (flag) | 0.9259 | 0.8570 | 0.8570 |
| R-13 | CL-047 Data Rights | 0.8507 | 0.8507 | 0.5969 | 0.5969 |
| R-42 | R-43 Disaster Mitigation | 0.8849 (watch) | 0.8849 | 0.4486 | 0.4486 |
| CL-059 | CL-022 Act | 0.7591 | 0.7591 | 0.9746 | 0.9746 |
| R-48 | CL-035 Residential Sorting | 0.8528 | 0.8528 | 0.8322 | 0.8322 |
| CL-073 | CL-042 AI Concentration | 0.4487 | 0.4487 | none | none |
| CL-074 | R-36 Public Investment | 0.8962 (watch) | 0.8962 | none | none |

Against the set in use. The check always compares with October's 122, so I ran it a second time listing every pair, then set aside the six October originals that left the set and kept the finals' pairs with each other. Result: one flagged pair, CL-014 against CL-035 Residential Sorting at 0.926, the same flag the board showed beside CL-014 C, which Dustin approved. Sixteen pairs sit on watch, from 0.8722 to 0.9115. The closest are CL-014 against R-30 By-Right Housing (0.9115), CL-074 against R-36 Public Investment (0.8962), CL-014 against CL-026 Executive Power (0.8924), CL-014 against the R-48 final (0.8867) and the R-13 final against the R-42 final (0.8859). R-13 and R-42 share set B's chamber by design (DR-156). In the set in use, CL-025's closest drawing becomes CL-005 Public Meeting (0.8780), since CL-014's October drawing has left.

**Pixel-fit check** (`python3 -I work/build/scripts/phase-2/icon_pixel_fit_check.py`, `--size 24 --weight 1` for the 24 px fit B files, `--size 16 --weight 1` for the 16 px fit A files; both are 1 px lines). 16 of 16 pass at 1x and 2x, both editions. The eight black finals:

| Final | Straight edges on pixel edges | Soft pixels | Smallest gap | Counters kept |
|---|---|---|---|---|
| CL-019 Explain, 24 px | 24 of 24 | 0% | 2 px | 4 of 4 |
| CL-020 Track, 24 px | 15 of 15 | 0% | 2.25 px | 3 of 3 |
| CL-021 Connect, 24 px | 20 of 20 | 0% | one part | 3 of 3 |
| CL-022 Act, 24 px | 19 of 19 | 0% | 1 px | none drawn |
| CL-019 Explain, 16 px | 18 of 18 | 0% | 1 px | 4 of 4 |
| CL-020 Track, 16 px | 12 of 12 | 0% | 1 px | 2 of 2 |
| CL-021 Connect, 16 px | 8 of 8 | 0% | one part | 3 of 3 |
| CL-022 Act, 16 px | 16 of 16 | 0% | 1 px | none drawn |

Every figure equals the stage B run on the fit files.

**The look.** I looked at every final in all four editions on its own ground (red-black on Newsprint, black on White, Red-Newsprint on Charcoal, Newsprint on Prussian) at 128, 48, 32 and 24 px true size, at 2x (256 and 96 px), and at 48 px enlarged four times. I looked at all 96 tiles at 128 px and each tile at its smallest size, true size, at 2x and enlarged. I looked at the 16 pillar finals at 1x and 2x, true size and enlarged. Nothing clips, every edition carries the right inks, and the red sits where each DR puts it. The renders are in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ea3fc969-1fa2-5617-a502-a9fe32bb03e8/scratchpad/promotion/civic-line/look/`, and the check results in `.../promotion/civic-line/checks/` and `.../promotion/civic-line/20261110_Civic-Line-V6-Promote-Checks.json`.

## Routine calls

The main session numbers these when it records them.

- D2-xxx | A final's title is its label alone ("Congress"), and its description carries the approval, the pick, the DR and the date | October's titles are the label, and the title is the name a screen reader speaks wherever the sprite places the drawing
- D2-xxx | A final takes October's root id pattern, `oa-civic-line-<id>-<edition>`, the ids the replaced October files used | The sprite and October's tools find a drawing by that pattern; the replaced files are out of the set in use, and the id audit over the 2,000 files in use finds no repeat
- D2-xxx | A redraw's description says its October master stays in the October set as the record, without a folder path | The description travels with the file into the package
- D2-xxx | The light editions of the eight come from October's swap function on the red-black final | DR-09; the same function made October's 488 editions
- D2-xxx | The eight finals' tile optical scale and offset follow S-1 and S-2 on the build's vector hull, divided by that hull's own median over the 122 masters (74.66 units) | The review measured on renders; with a matching median the rule gives the review's table for 116 of 118 icons under S-1 and 122 of 122 under S-2
- D2-xxx | Bare floors: CL-025, CL-059 and CL-073 at 32 px; CL-014, R-13, R-42, R-48 and CL-074 at 48 px; none reads at 24 px | Read at 32 and 24 px as October's review read the 122; the five at 48 px combine three parts or lean on a small sign
- D2-xxx | CL-073 and CL-074 follow CL-024 in the inventory, as sheet 01, row 5, columns 1 and 2 | D2-714 files them with sheet 01, and the next row keeps the sheet's six-column grid for the contact sheets that chapter 10 redraws (D2-717)
- D2-xxx | Sheet fields a redrawn or new drawing does not have (sheet images, crop, registration, sheet overlap, reference crops, components, caption check, mask figures) are null in the JSON and "none" in the CSV | These drawings came from the drawings board, not from a supplied sheet, and a made-up value would read as a measurement
- D2-xxx | The eight rows' stroke medians are October's estimators run on each drawing's own stage B source at 1x (5.52 to 5.75 px, 6.0 px on the 1x estimator) | October measured the sheet; these drawings have no sheet, and their own line is the one to measure
- D2-xxx | The six redraws keep their October sheet, row and column, and their October labels and slugs | The redraw takes its original's place in the set; DR-185 sets the words chapter 10 prints, and file names and IDs stay as approved
- D2-xxx | The eight rows keep the status "reviewed", and the new `source` column names the approving DR | October's states end at "reviewed"; approval is what the source column records
- D2-xxx | The inventory adds five columns after October's 46: `source`, `source_file`, `png_256_dir`, `png_512_dir` and `tiles_dir`; the JSON adds each row's SVG hashes, its tile PNG paths and, for the eight, a `final` block with the option, the drawing it replaces, how it was measured, its reading at 32 and 24 px, its tile rule figures and its tile margins | October's columns keep their meaning, and the brief asks for the source and the paths
- D2-xxx | Every path in the inventory is relative to the inventory's own folder, as October's were | One convention for the whole file; the 116 unchanged rows then point at `../civic-line/` for PNGs and tiles (D2-716)
- D2-xxx | The pillar icons sit in `pillar-icons/svg/` and `pillar-icons/png/`, with root ids `oa-pillar-icon-<id>-<size>px-<edition>` and the pillar's word as title | The layout of `pillar-pixel-fit/`, which the engineer's build reads deep, picking the black files
- D2-xxx | The pillar manifest names D2-634 beside DR-179: a 16 px pillar icon keeps its fit on 2x screens | DR-179 names 2x screens at 24 px only, and D2-634 is the rule the board recommended for 16 px
- D2-xxx | The pillar PNG previews are drawn again from the finals and compared with the stage B previews | They match pixel for pixel, so the folder's previews are the finals' own

## Questions for Dustin

None from this pass.

## For the main session

1. **Python packages.** October's tile and stroke code needs `scipy` and `scikit-image`, and this container had neither. `python3 -I` ignores the user site, so I installed both into the system Python (`pip install --break-system-packages`). A fresh container needs the same before `civic_line_v6_promote.py` or October's tile scripts run. Recommendation: add them to the environment's setup when the session's environment is next saved.
2. **The brief's script pointer.** The `icons_*` scripts in `work/build/scripts/phase-2/` built the October 28 pillar concepts, not the Civic Line set. Recommendation: point later briefs at `work/build/scripts/civic-line/`.
3. **The look-alike check's master set.** `icon_likeness_check.js` reads October's inventory and black folder. Recommendation: when the engineer next touches it, let it read `civic-line-v6/` so "against the set in use" needs no second pass.

## Tested

- Byte checks: 464 unchanged copies against October; 32 finals against their option files or October's swap of them; 16 pillar finals against their fit files; the stage B sources re-baked against the eight option files.
- October's structure, edition-tree, tile and PNG checks from `verify_set.py` on every final, tile and preview; October's id audit over the 2,000 SVGs in use.
- The inventory: row counts, every path it names (6,076), no empty cell outside the flags column.
- October's renderer and tile code reproducing October's files before I used them.
- The engineer's look-alike check on the eight black finals, compared with the board's figures and filtered to the set in use.
- The engineer's pixel-fit check on the 16 pillar finals at their sizes and lines, 1x and 2x.
- A look at every final, tile and pillar file at true size and enlarged, at 1x and 2x, in Chromium renders.
- My reading of the eight finals at 32 and 24 px for the bare floors.

## Not tested

- Rendering outside Chromium, and opening the files in Illustrator, Figma or other design tools.
- A real 2x screen. The 2x renders draw each file at twice its pixel size, which is what a 2x screen draws.
- Any person naming the finals or reading them at 32 px. The floors rest on my reading as an agent.
- The engineer's sprite build reading these folders. The engineer runs that.
- The chapter 10 contact sheets drawn from this folder (D2-717); they belong to round 2.

## Change log

Nothing in `source/`, `work/ledger/`, `deliverables/`, `work/build/assets/civic-line/`, the option folders (`civic-line-redraws/`, `civic-line-new-topics/`, `pillar-pixel-fit/`), any board or another owner's files changed. Nothing was committed or pushed.

**Created**

- `work/build/assets/civic-line-v6/`
  - `red-black/`, `black/`, `red-newsprint/`, `newsprint/`: 124 SVGs each (116 copies, 8 finals)
  - `png-256/<edition>/` and `png-512/<edition>/`: 64 PNGs
  - `tiles/<shape>-<tile>/svg/`, `png-256/`, `png-512/`: 96 SVGs and 192 PNGs
  - `20261110_Civic-Line-V6-Inventory.csv` and `20261110_Civic-Line-V6-Inventory.json`
- `work/build/assets/pillar-icons/`
  - `svg/`: 16 SVGs
  - `png/`: 32 PNGs
  - `20261110_Pillar-Icons-Manifest.json`
- `work/build/scripts/phase-2/civic_line_v6_promote.py`
- `work/handoffs/phase-2/20261110_Promotion-Civic-Line-Notes.md` (this file)

**Modified:** none in the repository. Outside it, `scipy` and `scikit-image` were installed into the container's Python.

**Rebuild:** `python3 -I work/build/scripts/phase-2/civic_line_v6_promote.py`; checks alone with `--check-only`.
