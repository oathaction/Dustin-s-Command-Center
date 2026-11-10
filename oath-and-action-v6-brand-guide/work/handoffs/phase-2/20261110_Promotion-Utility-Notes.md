# Promotion: the utility icons

Oath & Action Edition 06, Phase 2, stage B, November 10, 2026. Written by the icon designer for the utility hand, in the `oa-design-director` role, run as a subagent of the main session, under `20261110_Promotion-Brief.md` (item 2 under "Who does what"). I read my role file, `CLAUDE.md`, the promotion brief, the decision log's utility calls D2-637 to D2-663 and its entries DR-161 to DR-178 and D2-709 to D2-718, my stage B notes, the options' manifest, the three utility scripts and section 1 of the accessibility audit. This subagent made every file and ran every check below.

**The folder to open:** `work/build/assets/utility/`. The review sheets sit in my scratch folder (see Tested).

## What I promoted

Dustin approved the bare family (DR-161) and the 18 utility icons by name (DR-162 to DR-178) on the stage B drawings board. Each icon is now a final at 24 and 16 px:

- `svg-24/` and `svg-16/`: 36 SVG finals, named `20261110_Utility-<Name>-<24px|16px>.svg`.
- `png/`: 72 previews, Charcoal on a clear ground, at 1x (`...-24px.png`) and 2x (`...-24px-2x.png`).
- `20261110_Utility-Icons-Manifest.json`: for each icon its ID, drawing, approving DR, the audit's rank, action, word, uses, states and target, its turns and mirrors with the transform for each size, and for each size its files, line width, sprite symbol id, source file and three SHA-256 hashes (the source file, the final and the drawing).

Three things change from an approved option file to its final:

1. The file name.
2. The root attributes. `data-option` goes from all 36. Two IDs change to match their file names: Selected Check now carries `data-icon="U-selected-check"` (its option has `U-check`), and View Full Size carries `data-icon="U-view-full-size"` (its option has `U-full-size`). The other 16 icons keep their option's `data-icon`. Every final keeps `data-icon-family="utility"`, `data-size`, `aria-hidden="true"` and `focusable="false"`.
3. The comment. It now says the file is the final approved on the stage B drawings board, names the option Dustin approved and its DR, and names the option file the drawing came from.

Every byte after the comment line is the option file's. None of the 18 drawings carries an id, a mask or a title, so no id needed a new name. The options stay in `work/build/assets/utility-icons/` as the record (D2-718), and I left that folder as it was.

For the engineer: the manifest lists each file's sprite symbol id under the brief's pattern, from `oa-sym-u-close-24px` to `oa-sym-u-warning-16px`. The masthead's menu glyph is `svg-24/20261110_Utility-Menu-24px.svg` (`U-menu`).

The script is `work/build/scripts/phase-2/utility_icons_promote.py`. It writes the finals, the manifest and the previews, compares each final with its option file and each preview with the option's preview, and exits 1 on any difference. With `--report DIR` it writes the comparison as JSON; with `--review DIR` it draws review sheets and the turned and mirrored copies. Run it as `python3 -I work/build/scripts/phase-2/utility_icons_promote.py --report <scratch> --review <scratch>`.

## Every final and its source

| ID | Icon | Pick | DR | Drawing |
|---|---|---|---|---|
| `U-close` | Close | A | DR-162 | A bare cross |
| `U-menu` | Menu | A | DR-163 | Three even bars |
| `U-arrow` | Arrow | A | DR-164 | An arrow with a shaft and an open head, pointing right. Previous mirrors it; the sort order in use turns it |
| `U-chevron` | Chevron | A | DR-165 | A chevron pointing down, for closed. Open turns it half round |
| `U-download` | Download | A | DR-166 | An arrow down into an open tray |
| `U-another-site` | Another Site | A | DR-167 | An arrow leaving a box by its top right corner |
| `U-search` | Search | A | DR-168 | A magnifier with its handle to the lower right |
| `U-filter` | Filter | A | DR-169 | A funnel with a slanted spout |
| `U-copy` | Copy | A | DR-170 | Two square sheets, the back one up and to the left |
| `U-play` | Play | A | DR-171 | A triangle pointing right |
| `U-pause` | Pause | A | DR-171 | Two upright bars |
| `U-reset` | Reset | B | DR-172 | Three quarters of a circle with an upright corner head at the upper left |
| `U-error` | Error | A | DR-173 | An exclamation mark in a circle |
| `U-success` | Success | B | DR-174 | A check leaving an open circle |
| `U-selected-check` | Selected Check | A | DR-175 | A check |
| `U-view-full-size` | View Full Size | A | DR-176 | Four corners |
| `U-sort` | Sort | A | DR-177 | An up arrow and a down arrow side by side |
| `U-warning` | Warning | A | DR-178 | An exclamation mark in a triangle, in ink |

Each final beside its source, with hashes. The finals sit in `work/build/assets/utility/svg-24/` and `svg-16/`, the sources in `work/build/assets/utility-icons/svg-24/` and `svg-16/`. A hash here is SHA-256, cut to its first 16 hex digits; the manifest holds them in full. "Drawing" is the hash of every byte after the comment line, and it is the same in the source and the final.

| Final | Approved option file (source) | Source SHA-256 | Final SHA-256 | Drawing SHA-256, source and final |
|---|---|---|---|---|
| `20261110_Utility-Another-Site-24px.svg` | `20261109_Utility-Another-Site-Option-A-24px.svg` | `332758a36d714d2d` | `67ab675bb846c99f` | `5fe86ad7bc28ccfc` |
| `20261110_Utility-Arrow-24px.svg` | `20261109_Utility-Arrow-Option-A-24px.svg` | `4cca37f916d39fbd` | `df1083b89b776190` | `a51c77f474fa2c8d` |
| `20261110_Utility-Chevron-24px.svg` | `20261109_Utility-Chevron-Option-A-24px.svg` | `3c971a0b23172ce7` | `7f26c59a62d297fe` | `8f47c9977f342009` |
| `20261110_Utility-Close-24px.svg` | `20261109_Utility-Close-Option-A-24px.svg` | `7462f326076da9c0` | `e998802f17265617` | `831fbdce3d5c7040` |
| `20261110_Utility-Copy-24px.svg` | `20261109_Utility-Copy-Option-A-24px.svg` | `bd0fab702a2e77cd` | `d0d4c9481dc94e0c` | `01b3aefe95b69ca7` |
| `20261110_Utility-Download-24px.svg` | `20261109_Utility-Download-Option-A-24px.svg` | `ef1aad99249f024d` | `5c242349c218bebe` | `9d05df704404743a` |
| `20261110_Utility-Error-24px.svg` | `20261109_Utility-Error-Option-A-24px.svg` | `b415bdfdd8494ca0` | `92a3618a8f78105d` | `2db58d08ec317e61` |
| `20261110_Utility-Filter-24px.svg` | `20261109_Utility-Filter-Option-A-24px.svg` | `e7c178deac3d22a4` | `b8d90cfc65fc335e` | `b53f7cee8fcee0b6` |
| `20261110_Utility-Menu-24px.svg` | `20261109_Utility-Menu-Option-A-24px.svg` | `f8b262f675f953b9` | `09c561681c824f04` | `932d8e9f2e8d9b2a` |
| `20261110_Utility-Pause-24px.svg` | `20261109_Utility-Pause-Option-A-24px.svg` | `49dd85cca826ccb6` | `3fb62db093144338` | `1da3608af053cf1a` |
| `20261110_Utility-Play-24px.svg` | `20261109_Utility-Play-Option-A-24px.svg` | `27eb57fa6f48cae5` | `d6426cfd7e4f5d0d` | `a775b6f394875581` |
| `20261110_Utility-Reset-24px.svg` | `20261109_Utility-Reset-Option-B-24px.svg` | `a013bb4a05307da2` | `5005e85bbae91d10` | `1a933d16d747649b` |
| `20261110_Utility-Search-24px.svg` | `20261109_Utility-Search-Option-A-24px.svg` | `422097c0bbd54ef3` | `80c2f3f182ff9a0e` | `08085323d7577ec0` |
| `20261110_Utility-Selected-Check-24px.svg` | `20261109_Utility-Selected-Check-Option-A-24px.svg` | `bf8f44c76a5130c5` | `f77395e8dd5d4a2d` | `3d927cfadca427ab` |
| `20261110_Utility-Sort-24px.svg` | `20261109_Utility-Sort-Option-A-24px.svg` | `e89776c5c7fd5653` | `0ccae7bcec74d87e` | `1ff11bd89f5b4cf6` |
| `20261110_Utility-Success-24px.svg` | `20261109_Utility-Success-Option-B-24px.svg` | `103723291862dd12` | `f28b81f58e2c5030` | `c983cbd41e743932` |
| `20261110_Utility-View-Full-Size-24px.svg` | `20261109_Utility-View-Full-Size-Option-A-24px.svg` | `8f65ce499d42e922` | `13eddfa71f8d6c8d` | `09b08bfc19fcb69e` |
| `20261110_Utility-Warning-24px.svg` | `20261109_Utility-Warning-Option-A-24px.svg` | `f4099026c5153e75` | `07693eb134f24980` | `09fcb1db763826e8` |
| `20261110_Utility-Another-Site-16px.svg` | `20261109_Utility-Another-Site-Option-A-16px.svg` | `5b842c5fd54b4696` | `769a97f36ba475e2` | `88debdfe8cee8943` |
| `20261110_Utility-Arrow-16px.svg` | `20261109_Utility-Arrow-Option-A-16px.svg` | `c53fc8e9c66ed6ea` | `8135adc3ef1b4884` | `19b4d3bf839dde8b` |
| `20261110_Utility-Chevron-16px.svg` | `20261109_Utility-Chevron-Option-A-16px.svg` | `0dd7f53822ee0e4b` | `7006ba27c7008e53` | `dc26aa219d01cbb8` |
| `20261110_Utility-Close-16px.svg` | `20261109_Utility-Close-Option-A-16px.svg` | `8e5090264407d52b` | `88d38ad36ba70864` | `2595651dffe6a483` |
| `20261110_Utility-Copy-16px.svg` | `20261109_Utility-Copy-Option-A-16px.svg` | `ef280a9e3b61595f` | `04bc84f47b41e97e` | `16c2164deb870a64` |
| `20261110_Utility-Download-16px.svg` | `20261109_Utility-Download-Option-A-16px.svg` | `7da5f94cabde6aca` | `a4a27df9f2781f51` | `bc368ba0b5bffdf1` |
| `20261110_Utility-Error-16px.svg` | `20261109_Utility-Error-Option-A-16px.svg` | `304aa2f7ff8a9d3d` | `a97c774c9e562834` | `e2ecee14ca605e13` |
| `20261110_Utility-Filter-16px.svg` | `20261109_Utility-Filter-Option-A-16px.svg` | `c3aa8ac0e696c8f5` | `193627516829b1a6` | `40ef64f6d51b5008` |
| `20261110_Utility-Menu-16px.svg` | `20261109_Utility-Menu-Option-A-16px.svg` | `f774246490c409c7` | `119bd738d20fdd7d` | `187a638c18446ac7` |
| `20261110_Utility-Pause-16px.svg` | `20261109_Utility-Pause-Option-A-16px.svg` | `cba96d8e49132589` | `fd03dbac341a354d` | `eac1bbdda84fda02` |
| `20261110_Utility-Play-16px.svg` | `20261109_Utility-Play-Option-A-16px.svg` | `d3f4f8f04b9fbbc7` | `af4dc46cdcff881a` | `2cda25efa257b3d9` |
| `20261110_Utility-Reset-16px.svg` | `20261109_Utility-Reset-Option-B-16px.svg` | `dc31833fd00b3d24` | `dfcadd8c6f1dcee4` | `8b9acff982978d2c` |
| `20261110_Utility-Search-16px.svg` | `20261109_Utility-Search-Option-A-16px.svg` | `58e27b621e6aea3a` | `f84ca1078aa7d108` | `d0ce005692f1b701` |
| `20261110_Utility-Selected-Check-16px.svg` | `20261109_Utility-Selected-Check-Option-A-16px.svg` | `83401dfee0725572` | `1411698c7f7b719c` | `1d0cce632ffd1957` |
| `20261110_Utility-Sort-16px.svg` | `20261109_Utility-Sort-Option-A-16px.svg` | `8c502a063bc0cedb` | `183e1ff5a1e2f1cb` | `d51866da3e07ad10` |
| `20261110_Utility-Success-16px.svg` | `20261109_Utility-Success-Option-B-16px.svg` | `b4635c255883201a` | `dee2d5648d2f3852` | `59262b20a2fa3ee5` |
| `20261110_Utility-View-Full-Size-16px.svg` | `20261109_Utility-View-Full-Size-Option-A-16px.svg` | `8fc6f0351001c11d` | `755c4bd00d390012` | `6b451270e4f4c3d4` |
| `20261110_Utility-Warning-16px.svg` | `20261109_Utility-Warning-Option-A-16px.svg` | `018d88f777acd49d` | `22681e472a0b6467` | `e9bf8f597acd12d8` |

## Checks and their figures

### Byte and path comparison

The script compared each final with its approved option file in three ways, and the previews with the options' previews:

- The bytes after the comment line: 36 of 36 identical. A separate `cmp` of each pair from the third line on agrees, 36 of 36.
- Every element under the root, parsed as XML, with all its attributes: every `d`, every circle's centre, radius, fill and stroke. 36 of 36 identical: 64 elements in all, 56 paths and 8 circles, one to four per file.
- The root tag: the same in all 36 apart from `data-option`, removed from all 36, and `data-icon`, changed in the four Selected Check and View Full Size files.
- The previews: 72 of 72 draw the same pixels as the option's preview, and all 72 match it byte for byte.

A second run of the script left every SVG and PNG byte as the first run wrote it.

### Pixel fit

```
python3 -I work/build/scripts/phase-2/icon_pixel_fit_check.py --size 24 --weight 2 --json <scratch>/pixel-fit-24px.json --png <scratch>/pixel-fit-pictures-24 work/build/assets/utility/svg-24/
python3 -I work/build/scripts/phase-2/icon_pixel_fit_check.py --size 16 --weight 1.5 --json <scratch>/pixel-fit-16px.json --png <scratch>/pixel-fit-pictures-16 work/build/assets/utility/svg-16/
```

18 of 18 pass at 24 px and 18 of 18 at 16 px, at 1x and 2x, and both runs exit 0. The main line measures 2 px at 24 px (Selected Check 1.95, inside the 0.15 px tolerance) and 1.5 px at 16 px. The thinnest stroke is 1.93 px at 24 px and 1.45 px at 16 px. Every straight stroke sits on the grid, and no counter fills in. For all 36 files the pass, the soft share and the straight-stroke count equal the drawings board's figures for the option.

The turned and mirrored states (Previous, the arrow turned up and down, the open chevron), drawn from the finals with the manifest's transforms: 4 of 4 pass at 24 px and 4 of 4 at 16 px, with the same weights.

### Look-alike

```
node work/build/scripts/phase-2/icon_likeness_check.js work/build/assets/utility/svg-24/ work/build/assets/utility/svg-16/ --json <scratch>/likeness-finals.json
node work/build/scripts/phase-2/icon_likeness_check.js work/build/assets/utility/svg-24/ --watch 1 --json <scratch>/likeness-all-pairs-24px.json
node work/build/scripts/phase-2/icon_likeness_check.js work/build/assets/utility/svg-16/ --watch 1 --json <scratch>/likeness-all-pairs-16px.json
```

- Against the 122 Civic Line masters and each other, nothing is flagged, and the check exits 0. One pair sits on the watch line: Pause at 24 px against CL-012 Election Rules, 0.897 (percentile 98.1). The board printed the same figure, and my stage B notes record the look at that pair.
- For each 24 px final, the closest master and its figure equal the board's, 18 of 18. The board printed no 16 px figures. At 16 px the highest is Close against CL-022 Act at 0.831, and Pause against CL-012 measures 0.863, under the watch line of 0.871.
- Among the 18 finals, the closest pair at 24 px is Error and Success at 0.752 (percentile 60), the figure the family card gave for the bare set. At 16 px it is Pause and Sort at 0.806 (percentile 78).
- The October masters miss eight drawings in the set in use, so I added the eight changed Civic Line drawings (the approved options' black files) and the eight pillar fits in use (24 px fit B, 16 px fit A) to one run with the 36 finals. No utility pair reaches the watch line. The highest is Pause at 24 px against R-42 set B, 0.769 (percentile 66). That run exits 1 on CL-014 C against CL-035 Residential Sorting (0.926), a Civic Line pair the board printed, with no utility icon in it.
- The turned and mirrored states against the masters and the finals: nothing flagged or watched. The open chevron comes closest to the line, against R-03 Proportional Elections, a hemicycle of dots: 0.869 at 16 px and 0.861 at 24 px. Topic and atlas symbols never draw at 16 px (DR-136), and R-03 meets the open chevron at 24 px only if round 2's list of 41 symbols that read there names it.

Each final's figures. "Soft" is the share of ink pixels with partial coverage at 1x; the percentile ranks the figure among the 7,381 pairs of masters.

| Icon | 24 px: pass, main line, soft at 1x, straight strokes on the grid | 16 px: pass, main line, soft at 1x, straight strokes on the grid | Closest Civic Line master at 24 px, the same on the board | Closest at 16 px |
|---|---|---|---|---|
| Close | Pass, 2 px, 79%, 0 of 0 | Pass, 1.5 px, 69%, 0 of 0 | CL-022 Act, 0.834, percentile 86.5 | CL-022 Act, 0.831, percentile 86 |
| Menu | Pass, 2 px, 11%, 3 of 3 | Pass, 1.5 px, 62%, 3 of 3 | CL-012 Election Rules, 0.737, percentile 55.4 | CL-012 Election Rules, 0.752, percentile 60.4 |
| Arrow | Pass, 2 px, 58%, 1 of 1 | Pass, 1.5 px, 63%, 1 of 1 | CL-002 Representation, 0.774, percentile 68 | CL-002 Representation, 0.794, percentile 74.3 |
| Chevron | Pass, 2 px, 81%, 0 of 0 | Pass, 1.5 px, 71%, 0 of 0 | CL-064 Trade Costs, 0.728, percentile 52.6 | CL-064 Trade Costs, 0.734, percentile 54.4 |
| Download | Pass, 2 px, 40%, 4 of 4 | Pass, 1.5 px, 66%, 4 of 4 | CL-001 Voting, 0.793, percentile 73.9 | CL-025 Congress, 0.777, percentile 68.7 |
| Another Site | Pass, 2 px, 34%, 6 of 6 | Pass, 1.5 px, 59%, 6 of 6 | CL-057 Labor Share, 0.535, percentile 9.4 | CL-057 Labor Share, 0.600, percentile 18 |
| Search | Pass, 2 px, 67%, 0 of 0 | Pass, 1.5 px, 74%, 0 of 0 | CL-024 Feedback Loop, 0.651, percentile 29.2 | CL-024 Feedback Loop, 0.632, percentile 24.6 |
| Filter | Pass, 2 px, 41%, 3 of 3 | Pass, 1.5 px, 67%, 3 of 3 | CL-012 Election Rules, 0.668, percentile 33.3 | CL-012 Election Rules, 0.718, percentile 49 |
| Copy | Pass, 2 px, 17%, 6 of 6 | Pass, 1.5 px, 62%, 6 of 6 | CL-039 Feed Ranking, 0.548, percentile 10.7 | CL-068 Education, 0.232, percentile 0 |
| Play | Pass, 2 px, 54%, 1 of 1 | Pass, 1.5 px, 71%, 1 of 1 | CL-004 Petition, 0.796, percentile 74.9 | CL-004 Petition, 0.825, percentile 84.2 |
| Pause | Pass, 2 px, 15%, 8 of 8 | Pass, 1.5 px, 62%, 4 of 4 | CL-012 Election Rules, 0.897, percentile 98.1 | CL-012 Election Rules, 0.863, percentile 93.5 |
| Reset | Pass, 2 px, 60%, 2 of 2 | Pass, 1.5 px, 82%, 2 of 2 | CL-057 Labor Share, 0.481, percentile 5.4 | CL-057 Labor Share, 0.503, percentile 6.8 |
| Error | Pass, 2 px, 64%, 1 of 1 | Pass, 1.5 px, 81%, 1 of 1 | CL-068 Education, 0.568, percentile 13.1 | CL-068 Education, 0.479, percentile 5.2 |
| Success | Pass, 2 px, 68%, 0 of 0 | Pass, 1.5 px, 84%, 0 of 0 | CL-068 Education, 0.513, percentile 7.5 | CL-068 Education, 0.438, percentile 3.2 |
| Selected Check | Pass, 1.95 px, 54%, 0 of 0 | Pass, 1.5 px, 69%, 0 of 0 | CL-049 Wealth Concentration, 0.688, percentile 39.3 | R-28 Capital-Income Tax, 0.703, percentile 44 |
| View Full Size | Pass, 2 px, 29%, 8 of 8 | Pass, 1.5 px, 72%, 8 of 8 | CL-033 Hostile Content, 0.142, percentile 0 | CL-059 Credit Allocation, -0.184, percentile 0 |
| Sort | Pass, 2 px, 44%, 2 of 2 | Pass, 1.5 px, 68%, 2 of 2 | CL-047 Data Rights, 0.737, percentile 55.3 | CL-047 Data Rights, 0.752, percentile 60.4 |
| Warning | Pass, 2 px, 54%, 2 of 2 | Pass, 1.5 px, 75%, 2 of 2 | CL-059 Credit Allocation, 0.782, percentile 70.6 | CL-068 Education, 0.559, percentile 12 |

### The look

I drew every final at true size on Newsprint and on Charcoal at device scale 1 and 2, with the four turned and mirrored states beside them, 88 glyphs a sheet, each on whole CSS pixels. I enlarged each sheet with nearest-neighbour pixels and read it row by row, and enlarged the previews of Success, Selected Check, Pause and Filter the same way. Every final reads as its subject at both sizes and both scales, as it did on the board.

One point for the creative director's next pass: at 16 px on a 1x screen, the inside of Pause's two bars and of Filter's spout fills grey. Each counter is one pixel wide and straddles two pixels, so both come out half covered. The pixel-fit check counts both counters as open, and at 2x they open cleanly. The board drew the same pixels, since the previews match the options' byte for byte. These are the approved drawings, and I changed nothing.

### Success B and Selected Check A's check (D2-655)

Measured from the finals' coordinates:

| | Selected Check A | Success B |
|---|---|---|
| Arms | Each at 45 degrees, a right angle at the foot | The same |
| Line and ends | 2 px at 24 px, 1.5 px at 16 px, round caps and joins | The same |
| Long arm over short arm, 24 px | 2.20 | 2.71 in all; 2.37 up to the ring |
| Long arm over short arm, 16 px | 2.33 | 2.60 in all; 2.30 up to the ring |
| Short arm, as a share of Selected Check A's | | 0.70 at 24 px, 0.83 at 16 px |

The final keeps Selected Check A's angles, line and ends. Its long arm runs on past the ring's opening, so it measures 2.71 times the short arm at 24 px, where Selected Check A's measures 2.20. At 16 px the arms up to the ring hold Selected Check A's proportion within 0.03. The final is the drawing Dustin approved, byte for byte; question 1 asks what the record should say.

## Routine calls

- D2-xxx | Selected Check and View Full Size carry `data-icon="U-selected-check"` and `data-icon="U-view-full-size"` in their finals, where their options carry `U-check` and `U-full-size`; the other 16 keep their option's ID | The brief builds the ID from the file's name, so file, ID and sprite symbol share one name, as the creative director's cards do; no page or script reads the two old IDs
- D2-xxx | Each final's comment names its drawing, size and line, the option Dustin approved, its DR and the option file it came from | The brief asks the comment to name the board and the DR, and the file name lets a reader trace the bytes
- D2-xxx | At 16 px the arrow points down by a mirror across the diagonal (`matrix(0 1 1 0 0 0)`); every other state is a turn or a mirror about the centre | A quarter turn would put the down arrow's shaft on x = 8.25, half a pixel from the up arrow's 7.75 in one column of headings. The diagonal mirror keeps both on 7.75 (D2-649), and since the arrow is symmetric about its shaft it draws the same shape
- D2-xxx | The promotion script draws the previews with its own short Node step, the way `utility_icons_render.js` draws them | That script reads the options' manifest and clears stale files from the options' `png/`, which stays as the record; the new previews match the options' byte for byte
- D2-xxx | Check results, review sheets and the turned copies stay in my scratch folder; the manifest holds each file's hashes, and these notes hold the figures | The brief names `svg-24/`, `svg-16/`, `png/` and the manifest for the folder the package copies
- D2-xxx | The manifest names the board and the DRs and carries no link to the board | The board is a private page and the package will travel beyond the studio; the decision log holds the link
- D2-xxx | The manifest lists each file's sprite symbol id under the brief's pattern | The sprite and the manifest then name each symbol the same way; the engineer owns the sprite and can drop the field

## Questions for Dustin

1. **Success B's check.** D2-655 says every success option holds Selected Check A's check, its proportions scaled to fit. Success B, which you approved, shares that check's angles, line and ends, and its long arm runs on past the ring, so its arms stand in a different proportion: 2.71 to 1 at 24 px against Selected Check A's 2.20 to 1. Recommendation: keep Success B as you approved it, and have the main session reword D2-655 in the log to "the same check angles, line and ends". A check with Selected Check A's exact arm lengths would be a new drawing, and it would come back to you by name.

## Tested

- The byte and path comparison above: the script's four comparisons on all 36 SVGs and 72 PNGs, a separate `cmp` of every drawing, and a `diff` of every root tag, word by word, against its option's.
- The pixel-fit check on all 36 finals, with `--weight 2` at 24 px and `--weight 1.5` at 16 px, at 1x and 2x, and on the eight turned and mirrored copies.
- Every pixel-fit figure (pass, soft share, straight strokes) against the drawings board's figures file, 36 of 36 equal.
- The look-alike check on the 36 finals against the 122 masters and each other; on all pairs down to the 1st percentile at each size; with the eight changed Civic Line drawings and the eight pillar fits in use; and on the turned and mirrored copies.
- Each 24 px closest-master figure against the board's figures file, 18 of 18 equal.
- A look at every final at true size and enlarged, at 1x and 2x, on Newsprint and Charcoal, with the turned states beside them; 0 of 88 glyphs off whole CSS pixels on each sheet.
- The 72 previews: each at its size in device pixels (16, 24, 32 or 48), with a clear corner pixel and solid ink at Charcoal (#121212, within 4 levels where colour rounding touches an edge pixel).
- The two checks' arm lengths and angles, from the final files' coordinates.
- The manifest parses as JSON, lists 18 icons and 36 files, and holds no em or en dash.

## Not tested

- The finals in the guide's sprite or on any page. That is the engineer's step.
- A reader naming the finals. The naming readings are stage B's; the drawings did not change.
- Forced colors mode, live controls and contrast on rendered pixels (audit C-2, D-1 to D-4 and G-1 to G-5).
- The turned states as CSS transforms on a page. I drew them as SVG transforms on a group.
- Right-to-left use of the mirrored arrow.
- Browsers other than Chromium on Linux, Windows and macOS rendering, and device scales other than 1 and 2.
- The second look-alike pass at the corner where a badge sits, which audit finding UX-2 asks of the engineer.
- A 16 px line token, which does not exist yet (D2-661).

## Change log

Created:

- `work/build/assets/utility/svg-24/`: 18 SVG finals
- `work/build/assets/utility/svg-16/`: 18 SVG finals
- `work/build/assets/utility/png/`: 72 PNG previews, 1x and 2x
- `work/build/assets/utility/20261110_Utility-Icons-Manifest.json`
- `work/build/scripts/phase-2/utility_icons_promote.py`
- `work/handoffs/phase-2/20261110_Promotion-Utility-Notes.md` (this file)

Modified: none.

Scratch, outside the repository, in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ea3fc969-1fa2-5617-a502-a9fe32bb03e8/scratchpad/promotion/utility/`: `checks/` (the comparison JSON, the pixel-fit and look-alike results, the pixel pictures) and `review/` (the review sheets at 1x and 2x, their enlargements and crops, and the eight turned and mirrored copies in `turned/`).

I left `source/`, `work/ledger/`, `deliverables/`, `work/build/assets/utility-icons/`, every board and every other owner's files as they were. Nothing was committed or pushed.
