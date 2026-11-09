# Stage B, round 1: the utility icons

Oath & Action Edition 06, Phase 2, November 9, 2026. Written by the icon designer for the utility hand (D2-498), in the `oa-design-director` role, run as a subagent of the main session, under `20261109_Stage-B-Drawings-Brief.md`. I read my role file, `CLAUDE.md`, the drawings brief, the final stage B brief, the decision log from "Stage B answers" to the end, section 1 of the accessibility audit (with section 2 for the rules a glyph must meet), the engineer's notes and Master Brief sections 3, 10 and 11. Every drawing, check and page below was made by this subagent.

**The plate to open:** `work/boards/phase-2/stage-b/drawings/utility/20261109_Utility-Icons-Plates.html`. Capture it at device scale 1, 1176 px wide.

## What I drew

The 18 drawings section 1.1 of the audit lists for its 17 actions, three options each, 54 options in all. The words-only actions in section 1.3 stay words, and nothing outside the list was drawn. Each option has a 24 px master and its own 16 px master, so 108 SVG files, each with a 1x and a 2x PNG preview.

Construction, shared by every option so the set stays one family whichever option Dustin picks:

- A 24-unit grid. Squares and frames fill 3 to 21, circles 2 to 22, so a ring and a square look the same size; arrowheads and the warning's apex may reach past that, as points do.
- A 2 px line at 24 px, the token `--oa-component-icon-utility-line-medium`. Every straight centerline sits on a whole unit, so both edges of the line land on pixel edges.
- Its own 16 px master on a 16-unit grid with a 1.5 px line. Every straight centerline sits on a quarter (n.25 or n.75), so one edge lands on a pixel edge. A glyph built on one upright line, such as the "!" or the download arrow, takes x = 7.75 as its axis, and its ring or frame is centred on it.
- Round caps and joins. A frame's corner rounds by half the line on the centerline, so its outer corner rounds by one line width and its inner corner stays sharp, as in Civic Line. A dot is as wide as the line.
- One color through `currentColor`, no red. Every file carries `aria-hidden="true"`, `focusable="false"`, `data-icon="U-<name>"` and `data-icon-family="utility"`, as section 2 of the audit asks.
- Beside Civic Line: the same finish (round ends, sharp inner corners, open arrowheads), never one of its subjects. The 2 px line is heavier than Civic Line's line at its own floor (1.26 px at 48 px); the token fixes it, and the plate shows the two side by side.

The options differ in the picture: bare, in a ring, in a frame, or a different known form (a tray or a line under the download arrow, a diamond or a triangle for the warning). Play and Pause share letters and are picked as a pair. The arrow is one drawing: Previous mirrors it and the sort order in use turns it. The chevron points down when closed and turns for open.

Folders, all under `work/build/assets/utility-icons/`:

- `svg-24/` and `svg-16/`: the 108 masters, named `20261109_Utility-<Drawing>-Option-<A|B|C>-<24|16>px.svg`
- `png/`: 216 previews, Charcoal ink on a clear ground, `...-24px.png` (1x) and `...-24px-2x.png` (2x), as the Civic Line previews are made
- `qa/`: the check results behind every figure here
- `20261109_Utility-Icons-Manifest.json`: every option, what it shows and its files

## Recommended options

| Drawing | Pick | Why |
|---|---|---|
| Close | A, a bare cross | The sign readers look for. The enclosed crosses read near Error and measure as near twins of other enclosed options |
| Menu | A, three even wide bars | The phone convention, as the shell draws it. B sits on the watch line against CL-012 Election Rules; C reads as text |
| Arrow (Next, Previous, sort order) | A | The arrow readers know; it turns cleanly, and its head matches the sort arrows |
| Chevron | A | Clear at both sizes and apart from the arrow, which keeps its shaft |
| Download | A, into a tray | The best known download sign. B, onto a line, is the pick if you want the most distance from CL-001 Voting (0.644 against 0.793, both under the watch line) |
| Another site | A, an arrow leaving a box by its corner | The known sign, leaving by the corner as the audit asks; CL-001 Voting is under the 1st percentile |
| Search | A | The plain magnifier; the glint in B moves it toward CL-023 Evidence |
| Filter | A, a funnel with a slanted spout | The funnel readers know; the slant keeps it from reading as a glass |
| Copy | A, two square sheets | Reads as Copy at both sizes; C's text lines crowd at 16 px |
| Play and Pause | A and A | The plain triangle and bars; the ringed pairs measure as near twins, and C says video |
| Reset | B, an upright corner head at the upper left | Reads as undo or reset, its head sits on whole pixels, and it is furthest from CL-024 Feedback Loop (under the 1st percentile). A reads as refresh |
| Error | A, "!" in a circle | The audit's form, apart from the Warning triangle and the bare Close cross |
| Success | B, a check leaving an open circle | Apart from Civic Line's closed check badges and from a ticked box. C, the only option with no circle, reads as a checkbox |
| Selected check | A | The proportions readers know; C measures 0.924 against the chevron |
| View full size | A, four corners | The video sign; B blurs at 16 px, C is near the outside-link arrow |
| Sort | A, an up and a down arrow | Shares the arrowhead of Next, which turns to show the order in use; B borrows the chevron, C reads as resize |
| Warning | A, "!" in a wide triangle | The warning shape readers know, in ink only |

As a set, the 18 picks measure at most 0.752 against each other (Error A and Success B, the 60th percentile of the master pairs), and one sits on the watch line against a master: Pause A against CL-012 Election Rules, 0.897. I looked at that pair side by side: two hollow bars beside a page with two sliders. They share a tall blurred shape and do not read alike, and Pause only ever sits beside its word in a media control.

## Every option

Paths are relative to `work/build/assets/utility-icons/`. "Naming" is my reading at 24 px with no label (see Tested). Likeness figures are from the engineer's check at 24 px, with the percentile among the 7,381 pairs of Civic Line masters; it watches from 0.871 (95th) and flags from 0.913 (99th). Every option passes the pixel-fit check at its own size, so that column is left out; the plate gives each option's figures.

| Drawing | Option | What it shows | Files (24 px; 16 px) | Naming at 24 px | Closest Civic Line at 24 px | Near twin in the set (watch or flag) |
|---|---|---|---|---|---|---|
| Close | A (recommended) | A bare cross | `svg-24/20261109_Utility-Close-Option-A-24px.svg`; `svg-16/20261109_Utility-Close-Option-A-16px.svg` | Names it: Close. | CL-022 Act, 0.834 (86th pct.) | none |
| Close | B | The cross in a circle | `svg-24/20261109_Utility-Close-Option-B-24px.svg`; `svg-16/20261109_Utility-Close-Option-B-16px.svg` | Partly: Close or clear; also reads as a cancel badge. | CL-009 Safe Seats, 0.648 (29th pct.) | Pause B, 0.973 flag |
| Close | C | The cross in a square, the window sign | `svg-24/20261109_Utility-Close-Option-C-24px.svg`; `svg-16/20261109_Utility-Close-Option-C-16px.svg` | Partly: Close the window; may read as a box marked no. | CL-039 Feed Ranking, 0.573 (14th pct.) | Success C, 0.899 watch |
| Menu | A (recommended) | Three even bars, wide | `svg-24/20261109_Utility-Menu-Option-A-24px.svg`; `svg-16/20261109_Utility-Menu-Option-A-16px.svg` | Names it: Menu. | CL-012 Election Rules, 0.737 (55th pct.) | none |
| Menu | B | Three even bars, narrow and closer | `svg-24/20261109_Utility-Menu-Option-B-24px.svg`; `svg-16/20261109_Utility-Menu-Option-B-16px.svg` | Names it: Menu. | CL-012 Election Rules, 0.872 (95th pct.) | none |
| Menu | C | Three bars, the last one short | `svg-24/20261109_Utility-Menu-Option-C-24px.svg`; `svg-16/20261109_Utility-Menu-Option-C-16px.svg` | No: Text, or align left. | CL-039 Feed Ranking, 0.708 (46th pct.) | none |
| Arrow | A (recommended) | An arrow with a shaft and a square-cut head | `svg-24/20261109_Utility-Arrow-Option-A-24px.svg`; `svg-16/20261109_Utility-Arrow-Option-A-16px.svg` | Names it: Next, or go forward. | CL-002 Representation, 0.774 (68th pct.) | none |
| Arrow | B | The arrow in a circle | `svg-24/20261109_Utility-Arrow-Option-B-24px.svg`; `svg-16/20261109_Utility-Arrow-Option-B-16px.svg` | Names it: Next, or go; reads as a button. | CL-009 Safe Seats, 0.654 (30th pct.) | Play B, 0.949 flag |
| Arrow | C | A long shaft with a small head | `svg-24/20261109_Utility-Arrow-Option-C-24px.svg`; `svg-16/20261109_Utility-Arrow-Option-C-16px.svg` | Names it: Next, or continue. | R-07 Small-Donor Matching, 0.830 (85th pct.) | none |
| Chevron | A (recommended) | A chevron, 12 units wide | `svg-24/20261109_Utility-Chevron-Option-A-24px.svg`; `svg-16/20261109_Utility-Chevron-Option-A-16px.svg` | Names it: Show more, or open the list. | CL-064 Trade Costs, 0.728 (53rd pct.) | Selected Check C, 0.924 flag |
| Chevron | B | The chevron in a circle | `svg-24/20261109_Utility-Chevron-Option-B-24px.svg`; `svg-16/20261109_Utility-Chevron-Option-B-16px.svg` | Names it: Show more, or scroll down. | CL-009 Safe Seats, 0.538 (10th pct.) | Success A, 0.947 flag |
| Chevron | C | A small chevron, 8 units wide | `svg-24/20261109_Utility-Chevron-Option-C-24px.svg`; `svg-16/20261109_Utility-Chevron-Option-C-16px.svg` | Partly: Open the list; small and light beside a word. | CL-009 Safe Seats, 0.700 (43rd pct.) | none |
| Download | A (recommended) | An arrow down into an open tray | `svg-24/20261109_Utility-Download-Option-A-24px.svg`; `svg-16/20261109_Utility-Download-Option-A-16px.svg` | Names it: Download. | CL-001 Voting, 0.793 (74th pct.) | none |
| Download | B | An arrow down onto a line | `svg-24/20261109_Utility-Download-Option-B-24px.svg`; `svg-16/20261109_Utility-Download-Option-B-16px.svg` | Names it: Download, or save. | CL-025 Congress, 0.774 (68th pct.) | none |
| Download | C | An arrow down in a circle | `svg-24/20261109_Utility-Download-Option-C-24px.svg`; `svg-16/20261109_Utility-Download-Option-C-16px.svg` | Partly: Download, or move down. | CL-009 Safe Seats, 0.663 (32nd pct.) | Play B, 0.945 flag |
| Another Site | A (recommended) | An arrow leaving a box by its top right corner | `svg-24/20261109_Utility-Another-Site-Option-A-24px.svg`; `svg-16/20261109_Utility-Another-Site-Option-A-16px.svg` | Names it: Open somewhere else, or open in a new tab. | CL-057 Labor Share, 0.535 (9th pct.) | none |
| Another Site | B | A bare arrow up and to the right | `svg-24/20261109_Utility-Another-Site-Option-B-24px.svg`; `svg-16/20261109_Utility-Another-Site-Option-B-16px.svg` | Partly: Up and to the right; may read as trending up. | CL-057 Labor Share, 0.768 (66th pct.) | none |
| Another Site | C | An arrow leaving a ring by its upper right | `svg-24/20261109_Utility-Another-Site-Option-C-24px.svg`; `svg-16/20261109_Utility-Another-Site-Option-C-16px.svg` | No: Share, or export. | CL-057 Labor Share, 0.501 (7th pct.) | none |
| Search | A (recommended) | A magnifier: round lens, handle to the lower right | `svg-24/20261109_Utility-Search-Option-A-24px.svg`; `svg-16/20261109_Utility-Search-Option-A-16px.svg` | Names it: Search. | CL-024 Feedback Loop, 0.651 (29th pct.) | none |
| Search | B | The magnifier with a glint in the lens | `svg-24/20261109_Utility-Search-Option-B-24px.svg`; `svg-16/20261109_Utility-Search-Option-B-16px.svg` | Names it: Search, or a magnifying glass. | CL-023 Evidence, 0.738 (56th pct.) | none |
| Search | C | A larger lens on a short handle | `svg-24/20261109_Utility-Search-Option-C-24px.svg`; `svg-16/20261109_Utility-Search-Option-C-16px.svg` | Partly: Search, or zoom. | CL-057 Labor Share, 0.478 (5th pct.) | none |
| Filter | A (recommended) | A funnel with a slanted spout | `svg-24/20261109_Utility-Filter-Option-A-24px.svg`; `svg-16/20261109_Utility-Filter-Option-A-16px.svg` | Names it: Filter. | CL-012 Election Rules, 0.668 (33rd pct.) | none |
| Filter | B | A funnel with a square spout | `svg-24/20261109_Utility-Filter-Option-B-24px.svg`; `svg-16/20261109_Utility-Filter-Option-B-16px.svg` | Names it: Filter. | CL-012 Election Rules, 0.657 (31st pct.) | none |
| Filter | C | A wide funnel with a short spout | `svg-24/20261109_Utility-Filter-Option-C-24px.svg`; `svg-16/20261109_Utility-Filter-Option-C-16px.svg` | Partly: Filter; may read as a glass. | CL-030 Reform Tests, 0.753 (61st pct.) | none |
| Copy | A (recommended) | Two square sheets, the back one up and to the left | `svg-24/20261109_Utility-Copy-Option-A-24px.svg`; `svg-16/20261109_Utility-Copy-Option-A-16px.svg` | Names it: Copy, or duplicate. | CL-039 Feed Ranking, 0.548 (11th pct.) | none |
| Copy | B | Two tall sheets, the back one shown as a corner below and to the left | `svg-24/20261109_Utility-Copy-Option-B-24px.svg`; `svg-16/20261109_Utility-Copy-Option-B-16px.svg` | Names it: Copy, or pages. | CL-039 Feed Ranking, 0.623 (23rd pct.) | none |
| Copy | C | Two sheets, the front one with two lines of text | `svg-24/20261109_Utility-Copy-Option-C-24px.svg`; `svg-16/20261109_Utility-Copy-Option-C-16px.svg` | Partly: Copy text, or documents. | CL-067 Healthcare, 0.702 (44th pct.) | none |
| Play | A (recommended) | A triangle pointing right | `svg-24/20261109_Utility-Play-Option-A-24px.svg`; `svg-16/20261109_Utility-Play-Option-A-16px.svg` | Names it: Play. | CL-004 Petition, 0.796 (75th pct.) | none |
| Play | B | The triangle in a circle | `svg-24/20261109_Utility-Play-Option-B-24px.svg`; `svg-16/20261109_Utility-Play-Option-B-16px.svg` | Names it: Play. | CL-009 Safe Seats, 0.667 (33rd pct.) | Pause B, 0.958 flag |
| Play | C | The triangle on a screen | `svg-24/20261109_Utility-Play-Option-C-24px.svg`; `svg-16/20261109_Utility-Play-Option-C-16px.svg` | Partly: Play the video. | CL-068 Education, 0.613 (20th pct.) | Pause C, 0.966 flag |
| Pause | A (recommended) | Two upright bars | `svg-24/20261109_Utility-Pause-Option-A-24px.svg`; `svg-16/20261109_Utility-Pause-Option-A-16px.svg` | Names it: Pause. | CL-012 Election Rules, 0.897 (98th pct.) | none |
| Pause | B | Two bars in a circle | `svg-24/20261109_Utility-Pause-Option-B-24px.svg`; `svg-16/20261109_Utility-Pause-Option-B-16px.svg` | Names it: Pause. | CL-009 Safe Seats, 0.558 (12th pct.) | Close B, 0.973 flag |
| Pause | C | Two bars on a screen | `svg-24/20261109_Utility-Pause-Option-C-24px.svg`; `svg-16/20261109_Utility-Pause-Option-C-16px.svg` | Partly: Pause the video. | CL-068 Education, 0.593 (17th pct.) | Play C, 0.966 flag |
| Reset | A | Three quarters of a circle, the head at the top pointing left | `svg-24/20261109_Utility-Reset-Option-A-24px.svg`; `svg-16/20261109_Utility-Reset-Option-A-16px.svg` | No: Refresh, or reload. | CL-057 Labor Share, 0.595 (17th pct.) | none |
| Reset | B (recommended) | Three quarters of a circle, an upright corner head at the upper left | `svg-24/20261109_Utility-Reset-Option-B-24px.svg`; `svg-16/20261109_Utility-Reset-Option-B-16px.svg` | Names it: Undo, or reset. | CL-057 Labor Share, 0.481 (5th pct.) | none |
| Reset | C | Three quarters of a circle, the head at the left pointing down | `svg-24/20261109_Utility-Reset-Option-C-24px.svg`; `svg-16/20261109_Utility-Reset-Option-C-16px.svg` | Partly: Undo, or turn left. | CL-057 Labor Share, 0.511 (7th pct.) | none |
| Error | A (recommended) | An exclamation mark in a circle | `svg-24/20261109_Utility-Error-Option-A-24px.svg`; `svg-16/20261109_Utility-Error-Option-A-16px.svg` | Names it: Error, or alert. | CL-068 Education, 0.568 (13th pct.) | Pause B, 0.882 watch |
| Error | B | An exclamation mark in an octagon, the stop sign | `svg-24/20261109_Utility-Error-Option-B-24px.svg`; `svg-16/20261109_Utility-Error-Option-B-16px.svg` | Names it: Stop, or error. | CL-068 Education, 0.680 (37th pct.) | none |
| Error | C | An exclamation mark in a square | `svg-24/20261109_Utility-Error-Option-C-24px.svg`; `svg-16/20261109_Utility-Error-Option-C-16px.svg` | Partly: Notice, or important. | CL-068 Education, 0.493 (6th pct.) | none |
| Success | A | A check in a circle | `svg-24/20261109_Utility-Success-Option-A-24px.svg`; `svg-16/20261109_Utility-Success-Option-A-16px.svg` | Names it: Done, or success. | CL-009 Safe Seats, 0.509 (7th pct.) | Chevron B, 0.947 flag |
| Success | B (recommended) | A check leaving an open circle | `svg-24/20261109_Utility-Success-Option-B-24px.svg`; `svg-16/20261109_Utility-Success-Option-B-16px.svg` | Names it: Done, or success. | CL-068 Education, 0.513 (8th pct.) | Chevron B, 0.933 flag |
| Success | C | A check in a square | `svg-24/20261109_Utility-Success-Option-C-24px.svg`; `svg-16/20261109_Utility-Success-Option-C-16px.svg` | No: A ticked box: selected, more than success. | CL-039 Feed Ranking, 0.507 (7th pct.) | Close C, 0.899 watch |
| Selected Check | A (recommended) | A check, long arm at 45 degrees | `svg-24/20261109_Utility-Selected-Check-Option-A-24px.svg`; `svg-16/20261109_Utility-Selected-Check-Option-A-16px.svg` | Names it: Check, or done. | CL-049 Wealth Concentration, 0.688 (39th pct.) | none |
| Selected Check | B | A tick, the long arm steeper | `svg-24/20261109_Utility-Selected-Check-Option-B-24px.svg`; `svg-16/20261109_Utility-Selected-Check-Option-B-16px.svg` | Names it: Check, or tick. | R-28 Capital-Income Tax, 0.679 (36th pct.) | none |
| Selected Check | C | A compact check | `svg-24/20261109_Utility-Selected-Check-Option-C-24px.svg`; `svg-16/20261109_Utility-Selected-Check-Option-C-16px.svg` | Partly: Check, though near the chevron at this size. | CL-013 Incumbent Defeat, 0.725 (51st pct.) | Chevron A, 0.924 flag |
| View Full Size | A (recommended) | Four corners | `svg-24/20261109_Utility-View-Full-Size-Option-A-24px.svg`; `svg-16/20261109_Utility-View-Full-Size-Option-A-16px.svg` | Names it: Full screen, or expand. | CL-033 Hostile Content, 0.142 (0th pct.) | none |
| View Full Size | B | Four arrows from the middle out to the corners | `svg-24/20261109_Utility-View-Full-Size-Option-B-24px.svg`; `svg-16/20261109_Utility-View-Full-Size-Option-B-16px.svg` | Names it: Expand; busy at 16 px. | CL-033 Hostile Content, 0.520 (8th pct.) | none |
| View Full Size | C | Two arrows out to opposite corners | `svg-24/20261109_Utility-View-Full-Size-Option-C-24px.svg`; `svg-16/20261109_Utility-View-Full-Size-Option-C-16px.svg` | Partly: Expand, or resize; near the outside-link arrow. | CL-057 Labor Share, 0.406 (2nd pct.) | none |
| Sort | A (recommended) | An up arrow and a down arrow side by side | `svg-24/20261109_Utility-Sort-Option-A-24px.svg`; `svg-16/20261109_Utility-Sort-Option-A-16px.svg` | Names it: Sort, or swap. | CL-047 Data Rights, 0.737 (55th pct.) | none |
| Sort | B | Two chevrons, one up and one down | `svg-24/20261109_Utility-Sort-Option-B-24px.svg`; `svg-16/20261109_Utility-Sort-Option-B-16px.svg` | Partly: Sort, or choose from a list. | CL-034 New Technology, 0.683 (38th pct.) | none |
| Sort | C | One upright arrow with a head at each end | `svg-24/20261109_Utility-Sort-Option-C-24px.svg`; `svg-16/20261109_Utility-Sort-Option-C-16px.svg` | No: Move up and down, or resize. | CL-012 Election Rules, 0.712 (47th pct.) | none |
| Warning | A (recommended) | An exclamation mark in a wide triangle | `svg-24/20261109_Utility-Warning-Option-A-24px.svg`; `svg-16/20261109_Utility-Warning-Option-A-16px.svg` | Names it: Warning, or caution. | CL-059 Credit Allocation, 0.782 (71st pct.) | none |
| Warning | B | An exclamation mark in a diamond, the road sign | `svg-24/20261109_Utility-Warning-Option-B-24px.svg`; `svg-16/20261109_Utility-Warning-Option-B-16px.svg` | Names it: Warning; the road sign. | CL-068 Education, 0.716 (48th pct.) | none |
| Warning | C | An exclamation mark in a narrower triangle | `svg-24/20261109_Utility-Warning-Option-C-24px.svg`; `svg-16/20261109_Utility-Warning-Option-C-16px.svg` | Names it: Warning, or caution. | CL-040 Platform Power, 0.840 (88th pct.) | none |

## The checks and their figures

**Pixel fit** (`icon_pixel_fit_check.js`, the engineer's thresholds):

```
node work/build/scripts/phase-2/icon_pixel_fit_check.js --size 24 --weight 2 --json work/build/assets/utility-icons/qa/20261109_Utility-Pixel-Fit-24px.json work/build/assets/utility-icons/svg-24/
node work/build/scripts/phase-2/icon_pixel_fit_check.js --size 16 --weight 1.5 --json work/build/assets/utility-icons/qa/20261109_Utility-Pixel-Fit-16px.json work/build/assets/utility-icons/svg-16/
node work/build/scripts/phase-2/icon_pixel_fit_check.js --size 16 --weight 1.5 --json work/build/assets/utility-icons/qa/20261109_Utility-Pixel-Fit-24px-Drawn-At-16px.json work/build/assets/utility-icons/svg-24/
```

- 24 px masters at 24 px: 54 of 54 pass at 1x and 2x. Main line 2 px, every straight stroke on whole pixels. Soft pixels at 1x average 49 percent.
- 16 px masters at 16 px: 54 of 54 pass. Main line 1.5 px, every straight stroke with one edge on a pixel edge. Soft pixels at 1x average 71 percent.
- The 24 px masters drawn at 16 px: 27 of 54 pass, with a 1.33 px line at the very edge of the 0.15 px tolerance, and 79 percent soft pixels on average. The fails are straight edges off the grid (48 size and scale cases), soft pixels (7), gaps (4) and counters (2). So every option keeps its own 16 px master.
- First runs failed 3 files at 24 px and 9 at 16 px. I fixed each and reran: the octagon's flats moved onto whole pixels; Success B's ring opened wider so the check clears it; the two shafts of Full Size C stopped short of the middle; Another Site C's ring opened past the arrowhead; Search B's glint shrank at 16 px; Play C's screen and triangle grew at 16 px so the triangle keeps its counter; the 16 px Warning triangles grew and their "!" shortened, so it clears the sides; Selected Check A's 16 px arms now run through pixel centres; the 16 px dots moved onto quarter pixels.

**Look-alike** (`icon_likeness_check.js`):

```
node work/build/scripts/phase-2/icon_likeness_check.js work/build/assets/utility-icons/ --recursive --json work/build/assets/utility-icons/qa/20261109_Utility-Likeness.json
node work/build/scripts/phase-2/icon_likeness_check.js work/build/assets/utility-icons/svg-24/ --watch 1 --json work/build/assets/utility-icons/qa/20261109_Utility-Likeness-All-Pairs-24px.json
```

- Against the 122 Civic Line masters: no option is flagged. Four pairs sit on the watch line: Menu B at 16 px against CL-012 Election Rules (0.898) and CL-047 Data Rights (0.893), Pause A against CL-012 (0.897) and Menu B at 24 px against CL-012 (0.872). Menu B is not recommended; Pause A is discussed above.
- Inside the set the check exits 1: 30 pairs are flagged, every one between two subjects drawn in a ring or a frame (Close B and Pause B 0.973, Pause C and Play C 0.966, Pause B and Play B 0.958 and so on), plus Selected Check C against Chevron A (0.924). Several measure above the closest pair of Civic Line masters (0.964). The enclosure carries the shape at 24 px. This is the measured case for bare actions.
- The pairs the audit names in section 1.4 (second command, which lists every pair down to the 1st percentile), each option's highest:
  - Reset and CL-024 Feedback Loop: A 0.452, B under the 1st percentile, C 0.483
  - Search and R-44 Digital Competition: all three under the 1st percentile. Against CL-023 Evidence: A 0.588, B 0.738, C 0.381. Against CL-020 Track: A 0.451, B 0.465, C under the 1st
  - Another Site and CL-001 Voting: A and C under the 1st percentile, B 0.549
  - Filter and the sliders CL-012, CL-071 and R-37: at most 0.687 (C against CL-012)
  - Error and Close against R-35 Term Limits, Rejected: Error under the 1st percentile for all three; Close A 0.515
  - Success against the circled check badges and checked boxes: at most 0.446 (A against R-01); B and C under the 1st percentile for most
  - Warning and CL-033 Hostile Content: A 0.612, B 0.504, C 0.695; CL-037 Foreign Interference under the 1st percentile
  - Sort and CL-060 Taxes and Benefits: at most 0.581; R-44 under the 1st percentile
  - Download and CL-001 Voting: A 0.793, B 0.644, C 0.428

**Naming test at 24 px.** Of 54 options, 34 name their subject, 15 name it among other readings, and 5 name something else: Menu C (text), Another Site C (share), Reset A (refresh), Success C (a ticked box) and Sort C (resize). Every recommended option names its subject.

**Plate.** All 745 glyphs sit on whole CSS pixels at device scale 1, checked with `node work/build/scripts/phase-2/utility_icons_render.js plate`.

To rebuild everything: `python3 -I work/build/scripts/phase-2/utility_icons_draw.py`, then `node work/build/scripts/phase-2/utility_icons_render.js previews`, the five check commands above, then `python3 -I work/build/scripts/phase-2/utility_icons_plates.py`.

## Routine calls

- D2-xxx | Every option has its own 16 px master on a 16-unit grid with a 1.5 px line, and a 16 px glyph always comes from that file | Drawn at 16 px, the 24 px files pass for 27 of 54 options with a 1.33 px line; the masters pass 54 of 54 with the 1.5 px line and fewer soft pixels
- D2-xxx | At 24 px every straight centerline sits on a whole unit; at 16 px on a quarter, with x = 7.75 as the axis of a glyph built on one upright line and its enclosure centred on that axis | Both edges of a 2 px line, and one edge of a 1.5 px line, then land on pixel edges, as the engineer's check asks
- D2-xxx | A frame's corner rounds by half the line on the centerline (1 unit at 24 px, 0.75 at 16) | Sharp inner corners as in Civic Line, and one rule for every frame
- D2-xxx | A dot is as wide as the line, and at 16 px its centre sits on a quarter pixel | A 1.5 px dot on a whole pixel lands as two grey pixels; on the quarter it fills one
- D2-xxx | The arrow ships as one drawing pointing right; Previous mirrors it and the sort order in use turns it up or down | The audit's one drawing for three uses; turning about the centre keeps every line on the grid
- D2-xxx | The chevron ships pointing down, closed, and turns half round for open | The audit's two states from one drawing
- D2-xxx | Play and Pause options share a letter, to be picked as a pair | One button swaps them
- D2-xxx | Every success option holds one check, Selected Check A's proportions scaled to fit | The audit draws both from one check; if Dustin picks another bare check, the success mark follows it
- D2-xxx | Another Site C became an arrow leaving a ring, replacing a first draft of an arrow leaving a corner bracket | At true size the bracket draft read as View Full Size C
- D2-xxx | Files are named for the drawing (Arrow, Chevron, Another-Site, View-Full-Size, Selected-Check) and carry `data-icon="U-<name>"` | Short stable names for a sprite, and the IDs a checker looks for (audit section 2)
- D2-xxx | PNG previews are Charcoal on a clear ground, 1x and 2x | As the Civic Line previews
- D2-xxx | Check results live in `work/build/assets/utility-icons/qa/`; the pixel pictures stay in my scratch folder | Civic Line keeps a `qa/` folder; the engineer asks for the pictures outside `work/build`
- D2-xxx | The naming test is run at 24 px, as the main session's task sets, not the brief's 48 px | Utility glyphs are used only at 24 and 16 px (audit B-3)
- D2-xxx | The 16 px line is 1.5 px, from the engineer's notes; `tokens.css` has no 16 px utility line token yet | The token source adds it with the first 16 px utility icon on a page
- D2-xxx | The plate moves each glyph by under one pixel onto whole CSS pixels with a small script | Text before a glyph can leave it on a fraction of a pixel, which would misstate the masters in the capture
- D2-xxx | The 2 px line stays heavier than Civic Line's line at 48 px | The token sets 2 px; the shared finish ties the two families, and the subjects keep them apart

## Questions for Dustin

1. **Which option for each icon?** Approve one per drawing by name. Recommendation: Close A, Menu A, Arrow A, Chevron A, Download A, Another Site A, Search A, Filter A, Copy A, Play A, Pause A, Reset B, Error A, Success B, Selected Check A, View Full Size A, Sort A and Warning A. Each reads as its action at 24 px, passes both checks, and keeps clear of the Civic Line drawings.
2. **Bare actions, enclosed marks?** Recommendation: keep every action bare and draw only Error, Success and Warning inside a shape. Options drawn inside a ring look alike to each other (Close B and Pause B measure 0.973, closer than any two Civic Line drawings), so a toolbar of ringed glyphs loses the shapes a reader tells apart. Mixing bare and ringed actions would also break the family.

## Tested

- The pixel-fit check on all 108 masters at their own size and line: 54 of 54 at 24 px, 54 of 54 at 16 px, at 1x and 2x.
- The 24 px masters at 16 px: 27 of 54 pass, which is the reason for the 16 px masters.
- The look-alike check on all 108 files against the 122 Civic Line masters and each other, at the default lines and again down to the 1st percentile for the pairs the audit names.
- Every option looked at true size and with enlarged 1x pixels, on Newsprint and Charcoal, and the check's own pixel pictures for every first-run fail.
- The naming test as my own reading, from a shuffled sheet of all 54 options at 24 px with no labels.
- The plate: 745 glyphs on whole pixels at device scale 1, a 1176 px page with no sideways scroll, and its full capture looked at.
- No SVG holds a color value: all 108 draw in `currentColor` only.

## Not tested

- Any reader. The naming readings are mine, as the designer who drew them; the creative director repeats the test, and the combined reader check comes after the board (D2-501).
- Naming at the brief's 48 px.
- Forced colors mode and live controls (audit D-1 to D-4, G-1 to G-5); the glyphs are drawn for them in `currentColor`, which is all a drawing can do.
- Contrast on rendered pixels (audit C-2).
- Browsers other than Chromium on Linux, Windows and macOS text rendering, and device scales other than 1 and 2, where the whole-pixel fit does not hold.
- Right-to-left use of the mirrored arrow.
- The plate at phone width (it is a fixed 1176 px capture page) and in print.
- The plate with Google's Inter; the capture used the Inter installed locally.

## Change log

Created:

- `work/build/assets/utility-icons/svg-24/`: 54 SVG masters at 24 px
- `work/build/assets/utility-icons/svg-16/`: 54 SVG masters at 16 px
- `work/build/assets/utility-icons/png/`: 216 PNG previews, 1x and 2x
- `work/build/assets/utility-icons/20261109_Utility-Icons-Manifest.json`
- `work/build/assets/utility-icons/qa/`: `20261109_Utility-Pixel-Fit-24px.json`, `20261109_Utility-Pixel-Fit-16px.json`, `20261109_Utility-Pixel-Fit-24px-Drawn-At-16px.json`, `20261109_Utility-Likeness.json`, `20261109_Utility-Likeness-All-Pairs-24px.json`
- `work/build/scripts/phase-2/utility_icons_draw.py` (the drawings), `utility_icons_render.js` (previews, review sheet, plate check), `utility_icons_plates.py` (the plate)
- `work/boards/phase-2/stage-b/drawings/utility/20261109_Utility-Icons-Plates.html`
- `work/handoffs/phase-2/20261109_Stage-B-Utility-Icons-Notes.md` (this file)

Modified: none. No file outside these was touched; the Civic Line masters were read only, and `source/`, `work/ledger/`, the identity masters, every existing board and other owners' files are unchanged. Nothing was committed or pushed.
