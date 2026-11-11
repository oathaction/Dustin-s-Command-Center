# Promotion C: icon designer's notes

**Ready for the engineer and the systems designer (November 11):** `work/build/assets/civic-line-v6/fit-24/` exists with the 37 fits in use (`20261111_Civic-Line-<ID>-<Slug>-24px-Fit-Black.svg`, root `data-id` and `data-size="24"`), their PNGs in `fit-24/png/` and `20261111_Civic-Line-24px-Fits-In-Use-Manifest.json`. CL-075's black SVG exists: `civic-line-v6/black/20261111_Oath-And-Action-Civic-Line-CL-075-Housing-Black.svg` (`data-id="CL-075"`), with its other three editions, PNGs and tiles. **Update:** the inventory's 125th row (CL-075, after CL-072, sheet 03) is in, and the utility `svg-16/20261111_Utility-Pause-16px.svg` and `20261111_Utility-Filter-16px.svg` are in use, the stage B pair moved to `utility/_archive/svg-16/`. With 125 rows, `stage_b_ch10_build.py` (it stops on any count but 124) and `icon_likeness_check.js --self-test` (it expects 124) need their counts raised by their owners.

Oath & Action Edition 06, Phase 2, stage C, November 11, 2026. Written by the icon designer (`oa-design-director`), one hand for every drawing, run as a subagent of the main session, for owner 1 of `20261111_Promotion-Stage-C-Brief.md`. I started this file before the work and added to it as each part landed.

I read, in order: my role file, `CLAUDE.md`, the stage C promotion brief, the November 10 promotion brief, the November 10 Civic Line and utility promotion notes, my round 0 notes (`20261110_Stage-C-Drawings-Notes.md`), DR-207 to DR-211 and D2-1235 to D2-1267 in the decision log, the stage B and stage C scripts I reuse (`civic_line_v6_promote.py`, `utility_icons_promote.py`, `civic_line_stage_c_drawings.py`, `civic_line_stage_b_common.py`, the October `civic-line/` modules), the approved files' manifests, the engineer's sprite reader in `guide_build.py` and drawings board C's figures file (`work/boards/phase-2/stage-c/drawings/20261110_Stage-C-Drawings-Board-Figures.json`).

## Status

Done. Every check below passes, and no figure differs from drawings board C's. Nothing is committed or pushed. The `git mv` of the six replaced utility files sits staged in the index, as `git mv` leaves it.

**Rebuild:** `python3 -I work/build/scripts/phase-2/stage_c_icons_promote.py` (parts: `--part fits`, `housing`, `inventory`, `utility`; `--check-only` runs the checks alone and writes them to the scratch folder).

## What I promoted

**1. CL-075 Housing (DR-207, D2-1262), in `work/build/assets/civic-line-v6/`.**

- `red-black/`, `black/`, `red-newsprint/` and `newsprint/` each gain `20261111_Oath-And-Action-Civic-Line-CL-075-Housing-<Edition>.svg`, so each holds 125 SVGs. Each is option A's file with four things changed: the root id and the ids that start with it (October's pattern, `oa-civic-line-cl-075-red-black`), `data-id` (now `CL-075`), the title ("Housing") and the description. The description says what the drawing shows, that Dustin approved it by name on drawings board C as option A (DR-207), the new number (D2-1262), sheet 03, and that it is set at 48 px and up and stays off the list of drawings set at 24 px (D2-1238).
- The light editions come from October's swap, `cl_svg.derive_editions` (DR-09), as option A's did.
- `png-256/<edition>/` and `png-512/<edition>/`: eight PNGs, drawn by October's renderer on a clear ground.
- `tiles/<shape>-<tile>/svg|png-256|png-512/`: 12 tile SVGs and 24 PNGs by October's tile code (DR-10), named `20261111_Oath-And-Action-Civic-Line-CL-075-Housing-Tile-<Shape>-<Tile>-<Mode>`.
- `20261110_Civic-Line-V6-Inventory.csv` and `.json`: a 125th row, CL-075, after CL-072 as sheet 03, row 5, column 1, filled as the CL-073 and CL-074 rows are, with `source` DR-207. The JSON's header now counts 125 rows (sheet 03: 25; DR-207: 1), and its decisions, layout, order and tile rule name CL-075; it keeps its first date and gains `"updated": "20261111"`. Every other row and every other CSV line is as it stood in git HEAD.

**2. The 37 fits in use (DR-209, D2-1265), in `work/build/assets/civic-line-v6/fit-24/`.**

- 37 SVGs named `20261111_Civic-Line-<ID>-<Slug>-24px-Fit-Black.svg`, slugs from the inventory in use. Each is its approved fit with its root id (now `oa-civic-line-<id>-24px-fit-black`, and the path's id after it), its description and its file name changed. The root keeps `data-id="<ID>"`, `data-size="24"`, the 24-unit viewBox and `shape-rendering="crispEdges"`. The title stays the word.
- `fit-24/png/`: 74 previews at 1x (24 px) and 2x (48 px), on a clear ground.
- `20261111_Civic-Line-24px-Fits-In-Use-Manifest.json`: the switch, the list of 41, the edition and the neighbor rules; for each fit its ID, word, family (12 topic, 25 atlas) and atlas ID, the approving DR (DR-209), its files, its sprite symbol (`oa-sym-<id>-24px`), the master a 2x screen draws (`../black/<file>`, `oa-sym-<id>`), its source file and three SHA-256 hashes (source, file in use, drawing), and what it keeps.

**3. Utility at 16 px (DR-208, D2-1264), in `work/build/assets/utility/`.**

- `svg-16/20261111_Utility-Pause-16px.svg` (the Pause redraw) and `svg-16/20261111_Utility-Filter-16px.svg` (Filter option A). Each keeps its approved file's root tag (`data-icon`, `data-icon-family="utility"`, `data-size="16"`, `aria-hidden`, `focusable`, no `data-option`) and every byte after its comment line. The comment now says the file is the final approved on drawings board C (DR-208), names the approved file, and says the stage B final it replaces stays in `_archive/`.
- `png/20261111_Utility-<Pause|Filter>-16px.png` and `-2x.png`, drawn by the utility promotion's own Chromium step, as the other 68 previews in `png/` were.
- `git mv` moved `svg-16/20261110_Utility-Pause-16px.svg` and `svg-16/20261110_Utility-Filter-16px.svg` to `_archive/svg-16/`, and their four previews to `_archive/png/`, bytes unchanged. `svg-16/` and `png/` now hold one file per icon, size and scale: 18 SVGs and 72 PNGs.
- `20261110_Utility-Icons-Manifest.json`: the two 16 px rows now name the files in use, the approved redraw as source, their hashes, an `approved` block (DR-208, with DR-197 behind the redraw) and a `replaces` block (the archived file, DR-171 or DR-169, its old source and hashes). The manifest gains `updated` and one `updates` entry. Nothing else in it changed against git HEAD.

**The script.** `work/build/scripts/phase-2/stage_c_icons_promote.py`, run with `python3 -I`. It imports the stage B promotion modules (`civic_line_v6_promote`, `utility_icons_promote`) and October's `civic-line/` code, writes only the files above, and runs its checks after every part. It sets CL-075's tile optics and floor in its own process; `cl_common.py` on disk is unchanged.

## Every file in use and its source

Hashes are the first 12 hex digits of SHA-256. A file in use hashes differently from its source because its ids, description or comment and name differ; the byte checks below show nothing else does.

**CL-075 Housing.** Sources in `work/build/assets/civic-line-new-topics/svg/`.

| Edition | File in use | In use | Approved file | Approved |
|---|---|---|---|---|
| Red-Black | `red-black/20261111_Oath-And-Action-Civic-Line-CL-075-Housing-Red-Black.svg` | `cade6dfd68ec` | `20261110_Housing-Option-A-Red-Black.svg` | `bc97501d4f45` |
| Black | `black/20261111_Oath-And-Action-Civic-Line-CL-075-Housing-Black.svg` | `a9cf2083b595` | `20261110_Housing-Option-A-Black.svg` | `c28c3dcfc7c8` |
| Red-Newsprint | `red-newsprint/20261111_Oath-And-Action-Civic-Line-CL-075-Housing-Red-Newsprint.svg` | `7e8e25e33a1c` | `20261110_Housing-Option-A-Red-Newsprint.svg` | `5c8c06ff15d1` |
| Newsprint | `newsprint/20261111_Oath-And-Action-Civic-Line-CL-075-Housing-Newsprint.svg` | `ff96c79bcc6c` | `20261110_Housing-Option-A-Newsprint.svg` | `95bcc11f5104` |

Its 12 tiles come from `civic-line-new-topics/tiles/<shape>-<tile>/svg/20261110_Housing-Option-A-Tile-*.svg`, one for one. The inventory row holds the full hashes of the four SVGs.

**The 37 fits.** Sources in `work/build/assets/civic-line-24-fit/svg/`. The manifest in use holds the full hashes.

| ID | Word | Family | File in use, `civic-line-v6/fit-24/` | In use | Approved file | Approved |
|---|---|---|---|---|---|---|
| CL-001 | Voting | topic | `20261111_Civic-Line-CL-001-Voting-24px-Fit-Black.svg` | `9b95a9281e30` | `20261110_Civic-Line-24px-Fit-CL-001-Voting-Black.svg` | `0a7c21659976` |
| CL-004 | Petition | topic | `20261111_Civic-Line-CL-004-Petition-24px-Fit-Black.svg` | `8deb2a55f9b7` | `20261110_Civic-Line-24px-Fit-CL-004-Petition-Black.svg` | `50b287dd595d` |
| CL-006 | Civic Ties | atlas (B3) | `20261111_Civic-Line-CL-006-Civic-Ties-24px-Fit-Black.svg` | `0800ca384e62` | `20261110_Civic-Line-24px-Fit-CL-006-Civic-Ties-Black.svg` | `041f3a35aa00` |
| CL-010 | Decisive Primaries | atlas (C2) | `20261111_Civic-Line-CL-010-Decisive-Primaries-24px-Fit-Black.svg` | `63eae5f55a95` | `20261110_Civic-Line-24px-Fit-CL-010-Decisive-Primaries-Black.svg` | `c11975c871d7` |
| CL-013 | Incumbent Defeat | atlas (C5) | `20261111_Civic-Line-CL-013-Incumbent-Defeat-24px-Fit-Black.svg` | `f81de80c4b57` | `20261110_Civic-Line-24px-Fit-CL-013-Incumbent-Defeat-Black.svg` | `c7636df99f55` |
| CL-023 | Evidence | topic | `20261111_Civic-Line-CL-023-Evidence-24px-Fit-Black.svg` | `eda621ec0755` | `20261110_Civic-Line-24px-Fit-CL-023-Evidence-Black.svg` | `60772bfe4303` |
| CL-024 | Feedback Loop | topic | `20261111_Civic-Line-CL-024-Feedback-Loop-24px-Fit-Black.svg` | `06beb8a589c8` | `20261110_Civic-Line-24px-Fit-CL-024-Feedback-Loop-Black.svg` | `ade2da0ebeca` |
| CL-028 | Watchdogs | atlas (D4) | `20261111_Civic-Line-CL-028-Watchdogs-24px-Fit-Black.svg` | `a7009aca4f73` | `20261110_Civic-Line-24px-Fit-CL-028-Watchdogs-Black.svg` | `1fc42b82458d` |
| CL-031 | Local Government | topic | `20261111_Civic-Line-CL-031-Local-Government-24px-Fit-Black.svg` | `696c331fd312` | `20261110_Civic-Line-24px-Fit-CL-031-Local-Government-Black.svg` | `a61d1edd2b4b` |
| CL-032 | Local Reporting | atlas (B2) | `20261111_Civic-Line-CL-032-Local-Reporting-24px-Fit-Black.svg` | `c83687eeb899` | `20261110_Civic-Line-24px-Fit-CL-032-Local-Reporting-Black.svg` | `1f5957bf8584` |
| CL-039 | Feed Ranking | atlas (TC1) | `20261111_Civic-Line-CL-039-Feed-Ranking-24px-Fit-Black.svg` | `e36953da84be` | `20261110_Civic-Line-24px-Fit-CL-039-Feed-Ranking-Black.svg` | `b3a775c1c0cd` |
| CL-040 | Platform Power | atlas (TC2) | `20261111_Civic-Line-CL-040-Platform-Power-24px-Fit-Black.svg` | `2849d4529446` | `20261110_Civic-Line-24px-Fit-CL-040-Platform-Power-Black.svg` | `569b94f18c10` |
| CL-047 | Data Rights | topic | `20261111_Civic-Line-CL-047-Data-Rights-24px-Fit-Black.svg` | `4a0e8d547277` | `20261110_Civic-Line-24px-Fit-CL-047-Data-Rights-Black.svg` | `29eb413f3ad1` |
| CL-048 | Public Records | topic | `20261111_Civic-Line-CL-048-Public-Records-24px-Fit-Black.svg` | `894584cd9840` | `20261110_Civic-Line-24px-Fit-CL-048-Public-Records-Black.svg` | `7fd6abb86f4c` |
| CL-050 | Worker Bargaining | atlas (A2) | `20261111_Civic-Line-CL-050-Worker-Bargaining-24px-Fit-Black.svg` | `bb514c610763` | `20261110_Civic-Line-24px-Fit-CL-050-Worker-Bargaining-Black.svg` | `de7a63d6cc06` |
| CL-051 | Market Power | atlas (A3) | `20261111_Civic-Line-CL-051-Market-Power-24px-Fit-Black.svg` | `2ea568cbc125` | `20261110_Civic-Line-24px-Fit-CL-051-Market-Power-Black.svg` | `c84c39da3caa` |
| CL-054 | Home Equity | atlas (A6) | `20261111_Civic-Line-CL-054-Home-Equity-24px-Fit-Black.svg` | `da0c5cc8f1c2` | `20261110_Civic-Line-24px-Fit-CL-054-Home-Equity-Black.svg` | `c083abd21296` |
| CL-057 | Labor Share | atlas (EC3) | `20261111_Civic-Line-CL-057-Labor-Share-24px-Fit-Black.svg` | `fd213ebb0a91` | `20261110_Civic-Line-24px-Fit-CL-057-Labor-Share-Black.svg` | `9f589be10581` |
| CL-060 | Taxes & Benefits | atlas (EC6) | `20261111_Civic-Line-CL-060-Taxes-And-Benefits-24px-Fit-Black.svg` | `9405b3686e6e` | `20261110_Civic-Line-24px-Fit-CL-060-Taxes-And-Benefits-Black.svg` | `b5a97495b3bd` |
| CL-061 | Household Income | atlas (EC7) | `20261111_Civic-Line-CL-061-Household-Income-24px-Fit-Black.svg` | `63a3bf70c9aa` | `20261110_Civic-Line-24px-Fit-CL-061-Household-Income-Black.svg` | `3c8cebcc59b8` |
| CL-067 | Healthcare | topic | `20261111_Civic-Line-CL-067-Healthcare-24px-Fit-Black.svg` | `c78305149d6b` | `20261110_Civic-Line-24px-Fit-CL-067-Healthcare-Black.svg` | `f0ba2a144b5c` |
| CL-068 | Education | topic | `20261111_Civic-Line-CL-068-Education-24px-Fit-Black.svg` | `3361692f2e8d` | `20261110_Civic-Line-24px-Fit-CL-068-Education-Black.svg` | `ee4a16fd82d3` |
| CL-070 | Environment | topic | `20261111_Civic-Line-CL-070-Environment-24px-Fit-Black.svg` | `5984733792c1` | `20261110_Civic-Line-24px-Fit-CL-070-Environment-Black.svg` | `68f6c74a3672` |
| CL-071 | Policy | topic | `20261111_Civic-Line-CL-071-Policy-24px-Fit-Black.svg` | `94a746601bd6` | `20261110_Civic-Line-24px-Fit-CL-071-Policy-Black.svg` | `47e8fcc5ffa9` |
| CL-072 | Reform | topic | `20261111_Civic-Line-CL-072-Reform-24px-Fit-Black.svg` | `305c88e05cdb` | `20261110_Civic-Line-24px-Fit-CL-072-Reform-Black.svg` | `26eccc96e844` |
| R-05 | Automatic Registration | atlas | `20261111_Civic-Line-R-05-Automatic-Registration-24px-Fit-Black.svg` | `6fe2f2f7a8d4` | `20261110_Civic-Line-24px-Fit-R-05-Automatic-Registration-Black.svg` | `eb470f50de19` |
| R-06 | On-Cycle Elections | atlas | `20261111_Civic-Line-R-06-On-Cycle-Elections-24px-Fit-Black.svg` | `6a76401074c3` | `20261110_Civic-Line-24px-Fit-R-06-On-Cycle-Elections-Black.svg` | `9f502aa56295` |
| R-08 | Donor Disclosure | atlas | `20261111_Civic-Line-R-08-Donor-Disclosure-24px-Fit-Black.svg` | `f334e1bd036b` | `20261110_Civic-Line-24px-Fit-R-08-Donor-Disclosure-Black.svg` | `1c07182f544e` |
| R-09 | Stock-Trading Ban | atlas | `20261111_Civic-Line-R-09-Stock-Trading-Ban-24px-Fit-Black.svg` | `786407f2ca98` | `20261110_Civic-Line-24px-Fit-R-09-Stock-Trading-Ban-Black.svg` | `79145e2ed634` |
| R-14 | Automatic Funding | atlas | `20261111_Civic-Line-R-14-Automatic-Funding-24px-Fit-Black.svg` | `1e469b6d6a3b` | `20261110_Civic-Line-24px-Fit-R-14-Automatic-Funding-Black.svg` | `54b9825854a4` |
| R-15 | Watchdog Remedies | atlas | `20261111_Civic-Line-R-15-Watchdog-Remedies-24px-Fit-Black.svg` | `f5971671439b` | `20261110_Civic-Line-24px-Fit-R-15-Watchdog-Remedies-Black.svg` | `0411854b06f9` |
| R-17 | Civil Service | atlas | `20261111_Civic-Line-R-17-Civil-Service-24px-Fit-Black.svg` | `3e4c5517c9e1` | `20261110_Civic-Line-24px-Fit-R-17-Civil-Service-Black.svg` | `0e46ed6312a6` |
| R-19 | Drug-Pricing Rules | atlas | `20261111_Civic-Line-R-19-Drug-Pricing-Rules-24px-Fit-Black.svg` | `61e285b62aa1` | `20261110_Civic-Line-24px-Fit-R-19-Drug-Pricing-Rules-Black.svg` | `2f89c5dc1ff9` |
| R-23 | Indexed Minimum Wage | atlas | `20261111_Civic-Line-R-23-Indexed-Minimum-Wage-24px-Fit-Black.svg` | `4a339adcd181` | `20261110_Civic-Line-24px-Fit-R-23-Indexed-Minimum-Wage-Black.svg` | `2da76c9fadfe` |
| R-27 | Tax Enforcement | atlas | `20261111_Civic-Line-R-27-Tax-Enforcement-24px-Fit-Black.svg` | `05859061428b` | `20261110_Civic-Line-24px-Fit-R-27-Tax-Enforcement-Black.svg` | `302d79516988` |
| R-37 | Feed Choice | atlas | `20261111_Civic-Line-R-37-Feed-Choice-24px-Fit-Black.svg` | `c8b27d92dd72` | `20261110_Civic-Line-24px-Fit-R-37-Feed-Choice-Black.svg` | `ede564e61733` |
| R-45 | Paper Ballots & Audits | atlas | `20261111_Civic-Line-R-45-Paper-Ballots-And-Audits-24px-Fit-Black.svg` | `e7481e3e8fd2` | `20261110_Civic-Line-24px-Fit-R-45-Paper-Ballots-And-Audits-Black.svg` | `42a72eea68d6` |

**Utility at 16 px.**

| File in use | In use | Approved file | Approved | Drawing, both |
|---|---|---|---|---|
| `utility/svg-16/20261111_Utility-Pause-16px.svg` | `d913d5d172a0` | `utility-16-redraw/svg/20261110_Utility-Pause-16px-Redraw.svg` | `afeed9829681` | `b28265315006` |
| `utility/svg-16/20261111_Utility-Filter-16px.svg` | `e1682890df75` | `utility-16-redraw/svg/20261110_Utility-Filter-16px-Redraw-A.svg` | `7581c73bdb86` | `cfeb8d490256` |

"Drawing" is the hash of every byte after the comment line; it is the same in the approved file and the file in use.

**The archive (D2-1264).** Each file hashes in `_archive/` as it did in git HEAD at its old place.

| Archived file, `utility/_archive/` | SHA-256, now and in HEAD |
|---|---|
| `svg-16/20261110_Utility-Pause-16px.svg` | `fd03dbac341a` |
| `svg-16/20261110_Utility-Filter-16px.svg` | `193627516829` |
| `png/20261110_Utility-Pause-16px.png` | `96087f1335ce` |
| `png/20261110_Utility-Pause-16px-2x.png` | `b926979a8271` |
| `png/20261110_Utility-Filter-16px.png` | `5738a2fe4e17` |
| `png/20261110_Utility-Filter-16px-2x.png` | `3b9c225f7b0d` |

## The checks' figures

The checks' JSON sits in my scratch folder: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/promotion-c/icons/20261111_Promotion-C-Icons-Checks.json`, with the pixel fit and likeness results in `.../promotion-c/icons/checks/`.

### Byte and path checks

- **The 37 fits.** With its root id and description put back, each file in use equals its approved fit byte for byte, 37 of 37, and its path data (`d`) is the approved file's, character for character. Root attributes: `data-id` the ID, `data-size="24"`, viewBox `0 0 24 24`, 37 of 37. The 74 previews equal the approved fits' previews pixel for pixel.
- **CL-075.** With its root id, `data-id`, title and description put back, each of the four editions equals option A's file byte for byte. Option A's own source, baked again with the stage B family code, gives its red-black file byte for byte, so the inventory's scale (0.609244), center and line (3.3508 units) belong to the drawing in use. October's structure check (`verify_set.check_svg`) finds no error in the four, and October's tree check matches the black and light editions to the red-black element for element (16 elements; 1, 10 and 11 ink swaps). Each 256 px preview equals option A's 256 px preview pixel for pixel. Each of the 12 tiles, with its ids, `data-id` and description put back, equals option A's tile byte for byte; October's tile check passes all 12; the 24 tile PNGs pass October's PNG check and equal option A's tile PNGs pixel for pixel.
- **Utility.** For both files the root tag and every byte after the comment line equal the approved redraw's, and the parsed elements match. The four previews equal the redraws' previews pixel for pixel, though a different Chromium step drew them. The six archived files hash as they did in git HEAD, and none is left at its old place.
- **Inventory.** 125 rows in the JSON and the CSV, IDs unique, CL-075 after CL-072 and before R-01. All 124 other rows equal git HEAD's, field for field, and all other CSV lines equal HEAD's, byte for byte (before writing, I confirmed both files rewrite byte for byte as they stood). 6,125 paths checked, none missing; no empty CSV cell outside the flags column. Each edition folder holds 125 SVGs; each preview folder 9 PNGs; `tiles/` 324 files.
- **Ids across the sets in use.** 661 SVGs in `civic-line-v6/` (with `fit-24/` and the tiles) and `pillar-icons/`: 2,230 ids, none repeated, and 56 references, all resolved.
- **The sprite.** The engineer's `guide_build.py --sprite-sheet`, written to my scratch folder, reads 206 symbols with no warning and no missing folder: Civic Line 125 (with `oa-sym-cl-075`), fit-24 37 (`oa-sym-cl-001-24px` to `oa-sym-r-45-24px`), utility 36 (`oa-sym-u-pause-16px` and `oa-sym-u-filter-16px` from the new files) and pillar 8.

### Pixel fit

```
python3 -I work/build/scripts/phase-2/icon_pixel_fit_check.py --size 24 --weight 1 --quiet --json <scratch>/checks/pixel-fit-fits-24.json work/build/assets/civic-line-v6/fit-24/
python3 -I work/build/scripts/phase-2/icon_pixel_fit_check.py --size 16 --weight 1.5 --quiet --json <scratch>/checks/pixel-fit-utility-16.json work/build/assets/utility/svg-16/20261111_Utility-Pause-16px.svg work/build/assets/utility/svg-16/20261111_Utility-Filter-16px.svg
```

- **The 37 fits:** 37 of 37 pass at 1x and 2x, exit 0. No soft pixel, a one-pixel main line (thinnest 1.02 px), every straight edge on a pixel edge, every counter open, gaps of at least one pixel. Every figure for every file equals round 0's run on the approved fits (`civic-line-24-fit/qa/20261110_Fits-Pixel-Fit-24px.json`), and each fit's pass, fails and full-ink share (100%, 3,687 ink pixels in all) equal the board's.
- **Pause and Filter at 16 px:** 2 of 2 pass at 1x and 2x, exit 0. Pause: main line 1.5 px, 8 of 8 straight strokes on the grid, 2 of 2 counters open, smallest gap 2 px, soft share 59.6% at 1x. Filter: main line 1.5 px, 3 of 3 straight strokes on the grid, 1 of 1 counter open, soft share 67.1% at 1x. Every figure equals a run on the approved redraw files, and the pass and fails equal the board's.
- **The open pixels, read from the 1x previews in use:** row 8 draws `128, 0, 128` across each Pause bar, as the board printed. Filter's spout opens one whole pixel on rows 8, 9 and 10; on row 11 the slanted foot begins and the pixel draws 72, so 3 of 4 rows, as the board printed.

### Likeness on CL-075

```
node work/build/scripts/phase-2/icon_likeness_check.js work/build/assets/civic-line-v6/black/20261111_Oath-And-Action-Civic-Line-CL-075-Housing-Black.svg --watch 0.01 --json <scratch>/checks/likeness-cl-075-against-<124|125>.json
```

- **Against the 124 in use, before CL-075's row went in (the board's set):** nothing flagged, exit 0. Flag line 0.9092, watch line 0.8678, 7,626 pairs, as on the board. All 124 pair figures equal the board's option A figures to four places. The closest is CL-051 Market Power, 0.6899 (42.4th percentile). CL-054 Home Equity 0.5008, CL-063 Essential Costs 0.5746, R-30 By-Right Housing 0.2902, CL-053 Housing Scarcity 0.2508, CL-031 Local Government 0.5737, R-31 Childcare Supply 0.5071.
- **Against the 125 in use, CL-075 now among them:** nothing flagged, exit 0. 7,750 pairs; flag line 0.9091, watch line 0.8672, median 0.7113. Every pair figure stays the same; only the percentiles move, since the set grew: CL-051 0.6899 at the 43.3rd, CL-054 9.7th, CL-063 17.6th, R-30 2nd, CL-053 1.8th. The check reports CL-075 against itself apart, as its own drawing.

### The look

I drew every file in use in Chromium at device scale 1 and 2, each on whole CSS pixels (0 of every sheet's drawings off the grid), and read each sheet at true size, then enlarged with nearest-neighbour pixels.

- **The 37 fits**, each beside its master at 24 px, on Newsprint and on Charcoal (Newsprint ink, as the sprite sets it), at 1x and 2x, and the 1x sheets enlarged three times. Every fit draws one-pixel Charcoal lines where its master draws a grey line, and keeps the parts its manifest names. At 2x the master, which a 2x screen draws, reads cleanly beside its fit.
- **CL-075**, all four editions on their grounds (Red-Black on Newsprint, Black on White, Red-Newsprint on Charcoal, Newsprint on Prussian) at 128, 48, 32 and 24 px, at 1x and 2x, beside CL-054, CL-053, CL-063, R-30, CL-051, CL-031, R-31, CL-052 and CL-065 at 48 px, and the 1x row enlarged. The red sits on the block's top right window in the two-color editions only. At 48 px it reads as homes of two kinds and stays apart from the house drawings. At 24 px on 1x its windows close up, as round 0 found, which is why it stays at 48 px and up.
- **CL-075's 12 tiles** at 128 px and at their smallest sizes (72, 76 and 80 px), at 1x and 2x. Nothing clips; the smallest margin is 22.26 units, at the circle, against the floor of 12.
- **The 18 utility icons at 16 px in use**, on Newsprint and Charcoal at 1x and 2x, with the archived Pause and Filter and the 24 px pair beside them, enlarged four and ten times. The in-use Pause opens a whole pixel inside each bar on every row at 1x, where the archived file fills grey; Filter A opens its spout on three of four rows. At 2x both open cleanly.

The sheets sit in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/promotion-c/icons/look/`. This is my reading as an agent, not a person's.

### Figures that differ from drawings board C's

None. The only new figures are the percentiles against the 125 in use, which the board could not print, since CL-075 was not yet in the set.

## Routine calls

The main session numbers these when it records them.

- D2-xxx | A fit in use takes the root id `oa-civic-line-<id>-24px-fit-black`, and its path the root id plus `-base` | The id follows the file name's order (ID, size, fit, edition), and it differs from the master's `oa-civic-line-<id>-black` and the approved fit's `oa-civic-line-24-fit-<id>-black`, so no id repeats across the sets in use
- D2-xxx | A fit's title stays its word; its description says it is in use, gives the switch and DR-209, and drops "for approval" | The title is what a screen reader speaks, and the description travels into the package
- D2-xxx | The fits manifest calls a fit "atlas" when the drawing carries an atlas ID and "topic" otherwise, with the atlas ID beside it: 12 topic, 25 atlas | The construction notes' section 10 table, which gives each of the 37 its atlas ID or none
- D2-xxx | The fits manifest names each fit's sprite symbol, the master a 2x screen draws (file and symbol), the three hashes and what the fit keeps; the pixel maps stay in the approved fits' manifest | The engineer's switch needs both symbols; the maps belong to the record
- D2-xxx | Paths in the fits manifest are relative to `fit-24/` | As the inventory's and the pillar manifest's paths are relative to their own folders
- D2-xxx | CL-075 is filed with sheet 03, Economy & Public Issues, as row 5, column 1, after CL-072 | Housing sits in the atlas's domain D09 beside CL-053 and CL-054, both on sheet 03; D2-714 filed CL-073 and CL-074 after sheet 01's last drawing the same way
- D2-xxx | CL-075 takes October's root id pattern (`oa-civic-line-cl-075-<edition>`), "Housing" as its title, and a description that names DR-207, D2-1262, sheet 03 and its 48 px floor | As the eight stage B finals
- D2-xxx | CL-075's tiles carry optical scale 0.94 and offset 0, option A's values, which the stage B form of S-1 and S-2 gives again on the final | One rule with the eight finals; the tiles then equal option A's byte for byte apart from their ids
- D2-xxx | CL-075's row records `reads_at_px` 32 as null, with D2-1236's 48 px floor and the round 0 reading at 24 px in its reader note | No 32 px reading is approved for Housing, and a made-up value would read as a measurement
- D2-xxx | CL-075's row adds `final.new_id` (D2-1262) and `final.sizes` (48 px and up) | The number's decision and the size rule travel with the row
- D2-xxx | The inventory keeps its first date and gains `"updated": "20261111"`; its header counts, decisions, layout, order and tile rule text name CL-075 | A living file keeps its first date (`CLAUDE.md`), and the header has to agree with its rows
- D2-xxx | The four previews of the replaced 16 px Pause and Filter also move by `git mv`, to `utility/_archive/png/` | D2-1264's reason holds for previews: `png/` then holds one preview per icon, size and scale, and the package never meets a preview of a retired drawing
- D2-xxx | The utility previews in use are drawn by the utility promotion's own Chromium step | The other 68 previews in `png/` came from it; the four match the redraws' previews pixel for pixel all the same
- D2-xxx | The utility manifest's two 16 px rows gain `approved` (DR-208) and `replaces` (the archived file, its DR and hashes); each icon's own `approved` block stays the stage B pick, which still holds at 24 px; the manifest gains `updated` and one `updates` entry | Each size names its own approval, and the record of the replaced file stays findable
- D2-xxx | The utility finals' comment lines name DR-208, the approved file and the archive | As the stage B finals' comments name their DR and option file
- D2-xxx | One script, `stage_c_icons_promote.py`, builds the three parts and checks them, reusing the stage B promotion modules | The November 10 method, with one rebuild command
- D2-xxx | The likeness check on CL-075 ran against the 124 in use before its row went in, then against the 125 | The board measured against 124; the second run gives the figures for the set as it now stands

## Questions for Dustin

None from this pass.

## For the main session

1. **Two counts that stop at 124.** `work/build/scripts/phase-2/stage_b_ch10_build.py` stops when the inventory holds any count but 124 (line 122), and `icon_likeness_check.js --self-test` now misses one assertion: "masters: 125 drawings" against its expected 124. I ran the self-test to confirm: one wrong, every other assertion right. Recommendation: the systems designer raises chapter 10's count to 125 as CL-075 joins the library, and the engineer raises the self-test's to 125. Neither file is mine.
2. **Stage B and round 0 scripts are now records.** Rerunning `civic_line_v6_promote.py` would write a 124-row inventory, and its `--check-only` now fails on counts (9 PNGs per preview folder, 324 tile files). Rerunning `utility_icons_promote.py` would write the stage B Pause and Filter back into `svg-16/` beside the new ones. The utility part of `civic_line_stage_c_drawings.py` reads the approved stage B pair from `svg-16/`, where it no longer sits, and writes into the makers' option folders. Recommendation: rerun none of them; `stage_c_icons_promote.py` rebuilds and checks this pass.
3. **The staged moves.** `git mv` staged the six renames in the index; the other files are unstaged or untracked. The commit takes them together.

## Tested

- Byte checks: the 37 fits against their approved files; CL-075's four editions and 12 tiles against option A's; option A's source baked again against its red-black file; the two utility files' root tags and drawings against the approved redraws; the six archived files against their bytes in git HEAD.
- October's structure, edition tree, tile and PNG checks (`verify_set.py`) on CL-075's files.
- Every preview in use against the approved file's preview, pixel for pixel: 74 fits, 4 CL-075 at 256 px, 24 CL-075 tiles, 4 utility.
- The inventory: row counts, order, every other row and CSV line against git HEAD, all 6,125 paths, empty cells, CL-075's hashes.
- The id audit over the 661 SVGs in `civic-line-v6/` and `pillar-icons/`.
- The pixel fit check on the 37 fits (`--size 24 --weight 1`) and the two utility files (`--size 16 --weight 1.5`), at 1x and 2x, against round 0's run, the redraws' run and the board's figures.
- The likeness check on CL-075 against the 124 in use and against the 125, every pair compared with the board.
- The likeness check's self-test, to confirm the count it now misses.
- The engineer's sprite reading the four families from the folders in use (`--sprite-sheet`, into scratch).
- A look at every file in use at true size and enlarged, at 1x and 2x, in Chromium on Linux.

## Not tested

- Renders outside Chromium on Linux, device scales other than 1 and 2, and a real 2x screen. A 2x render draws each file at twice its pixel size, which is what a 2x screen draws.
- Opening the files in Illustrator, Figma or other design tools.
- Any person naming a file in use. The readings are mine, an agent's.
- The strict guide build, the guide check and the 1x and 2x switch on real pages. The engineer runs those with these folders.
- The generator chain and a look at plates at 1440 and 390 px: I changed no chapter and no plate, so I ran neither.
- `civic_line_v6_promote.py --check-only` and `stage_b_ch10_build.py`, which would fail on the new count by design (see For the main session).
- A pixel fit check on CL-075 at 48 px. The brief does not ask for it, and round 0 ran it on option A's identical drawing.
- Whether Housing reads at 32 px. D2-1236 keeps its tiles on the 48 px floor until a 32 px reading is approved.

## Change log

Nothing in `source/`, `work/ledger/`, `deliverables/`, the October folder `work/build/assets/civic-line/`, the makers' option folders (`civic-line-24-fit/`, `utility-16-redraw/`, `civic-line-new-topics/`), `pillar-icons/`, any board or another owner's files changed. Nothing was committed or pushed.

**Created**

- `work/build/assets/civic-line-v6/fit-24/`: 37 SVGs, `png/` with 74 PNGs, `20261111_Civic-Line-24px-Fits-In-Use-Manifest.json`
- `work/build/assets/civic-line-v6/<edition>/20261111_Oath-And-Action-Civic-Line-CL-075-Housing-<Edition>.svg`: 4 SVGs
- `work/build/assets/civic-line-v6/png-256/<edition>/` and `png-512/<edition>/`: 8 PNGs for CL-075
- `work/build/assets/civic-line-v6/tiles/<shape>-<tile>/svg|png-256|png-512/`: 12 SVGs and 24 PNGs for CL-075
- `work/build/assets/utility/svg-16/20261111_Utility-Pause-16px.svg` and `20261111_Utility-Filter-16px.svg`
- `work/build/assets/utility/png/20261111_Utility-Pause-16px.png`, `-2x.png`, `20261111_Utility-Filter-16px.png`, `-2x.png`
- `work/build/scripts/phase-2/stage_c_icons_promote.py`
- `work/handoffs/phase-2/20261111_Promotion-C-Icons-Notes.md` (this file)

**Modified**

- `work/build/assets/civic-line-v6/20261110_Civic-Line-V6-Inventory.csv` and `.json` (the 125th row and the JSON header)
- `work/build/assets/utility/20261110_Utility-Icons-Manifest.json` (the two 16 px rows, `updated`, `updates`)

**Moved with `git mv`, bytes unchanged**

- `work/build/assets/utility/svg-16/20261110_Utility-Pause-16px.svg` and `20261110_Utility-Filter-16px.svg` to `work/build/assets/utility/_archive/svg-16/`
- `work/build/assets/utility/png/20261110_Utility-Pause-16px.png`, `-2x.png`, `20261110_Utility-Filter-16px.png`, `-2x.png` to `work/build/assets/utility/_archive/png/`

**Scratch**, outside the repository, in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/promotion-c/icons/`: the checks' JSON, `checks/` (pixel fit, likeness, self-test and sprite sheet results, hashes before the move), `look/` (review sheets and enlargements), the render folders and the two look scripts.
