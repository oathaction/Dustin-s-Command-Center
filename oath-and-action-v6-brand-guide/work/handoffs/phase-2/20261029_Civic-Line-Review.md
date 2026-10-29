# Civic Line trace review, Phase 2

October 29, 2026. Creative director pass, run as a subagent that drew none of the traces. It covers all 122 Civic Line icons in `work/build/assets/civic-line/src/`, checked against the black and red reference sheets through the QA overlays, the reference zooms and my own close crops. No source, export, script or status file changed. Fixes go back to the tracers through `20261029_Civic-Line-Review-Fixes.json`.

Terms used below. W is the set's one line weight, 5.5 source px, which exports as 2.6807 units on the 128 grid. `data-w` is a per-element weight that overrides W. Crop px are the coordinates of each icon's `src/<ID>.svg` viewBox. A "must" fix covers a missing or wrong part, wrong red or a visible fault. A "should" fix is polish.

## 1. Summary

- 100 PASS, 22 FIX.
- 13 icons carry at least one must fix: CL-007, CL-016, CL-020, CL-021, CL-022, CL-045, CL-070, R-01, R-07, R-11, R-27, R-45, R-46.
- 9 icons carry should fixes only: CL-009, CL-024, CL-046, CL-054, CL-060, CL-068, R-06, R-29, R-44.
- The JSON lists 24 instructions: 14 must and 10 should. CL-020 has two must items. R-11 has one must and one should.
- R-49 and R-50 were reviewed last, after both status files showed `traced`. Both pass.
- Pillar marks: CL-019 Explain is ready as an identity mark now. CL-020 Track, CL-021 Connect and CL-022 Act are ready once their must fixes land.

## 2. Verdicts for all 122 icons

| ID | Name | Verdict | Note |
|---|---|---|---|
| CL-001 | Voting | PASS | Box, lid, slot gap and red ballot top match both sheets. |
| CL-002 | Representation | PASS | Mirrored about the centre head; red centre head as the red sheet. |
| CL-003 | Registration | PASS | Card, person, rules and red check badge match. |
| CL-004 | Petition | PASS | One corner radius from fits; pen and clip parallel as drawn. |
| CL-005 | Public Meeting | PASS | Fourth figure inside the lectern kept; image over catalogue. |
| CL-006 | Civic Ties | PASS | Symmetric triangle of people; red ring gaps as drawn. |
| CL-007 | Turnout Equality | FIX must | Red marks drawn at data-w 7; take them to W. |
| CL-008 | Political Hostility | PASS | Mirrored bubbles, offset kept; red bolt matches. |
| CL-009 | Safe Seats | FIX should | Zero-length segment in the district path. |
| CL-010 | Decisive Primaries | PASS | Branch count, arrow and red node match. |
| CL-011 | Electoral Pressure | PASS | Figure, desk, arrow and box match; red arrow only. |
| CL-012 | Election Rules | PASS | Red starts partway along the upper rail as the red sheet shows. |
| CL-013 | Incumbent Defeat | PASS | Chair and red arrow match. |
| CL-014 | Entrenched Power | PASS | Elliptical rails and column count match. |
| CL-015 | Political Money | PASS | Coin, connector and box layering as the red sheet. |
| CL-016 | Lobbying | FIX must | Delete the stray tick beside the left shoulder. |
| CL-017 | Policy Favoritism | PASS | Middle bust red, route black, as the red sheet shows. |
| CL-018 | Earned Trust | PASS | Shield-shaped badge kept; see open calls. |
| CL-019 | Explain | PASS | Pillar mark, ready. |
| CL-020 | Track | FIX must | Handle short of the ring; unequal U-turns. |
| CL-021 | Connect | FIX must | Black arc ends blob into the red lens at both crossings. |
| CL-022 | Act | FIX must | Ring off the fingertip's centre; rays not mirrored. |
| CL-023 | Evidence | PASS | Five rules kept; image over catalogue. |
| CL-024 | Feedback Loop | FIX should | Lower arrowhead differs from the upper one. |
| CL-025 | Congress | PASS | Mirrored; dome's left foot gap kept as both sheets draw it. |
| CL-026 | Executive Power | PASS | One desk leg kept; image over catalogue. |
| CL-027 | Court Alignment | PASS | Scales, document and red seal match. |
| CL-028 | Watchdogs | PASS | Lens, red handle and rules match. |
| CL-029 | Public Services | PASS | Its data-w 10 is a mask cut for the visitor gap, not a stroke. |
| CL-030 | Reform Tests | PASS | Panels, links and red check match. |
| CL-031 | Local Government | PASS | Symmetric hall; red door matches. |
| CL-032 | Local Reporting | PASS | Paper fold and red block match. |
| CL-033 | Hostile Content | PASS | Laptop, bubble and red warning match. |
| CL-034 | New Technology | PASS | Bulb, red rays and red cord end match. |
| CL-035 | Residential Sorting | PASS | Red window inside the foreground home kept, as the red sheet shows. |
| CL-036 | Cross-Border Capital | PASS | Matching parcels; arrows point as drawn. |
| CL-037 | Foreign Interference | PASS | Globe, signal arcs, box and warning match. |
| CL-038 | External Shocks | PASS | Road and red burst match. |
| CL-039 | Feed Ranking | PASS | Top card open at the bottom kept; image over catalogue. |
| CL-040 | Platform Power | PASS | Three equal people under the red node. |
| CL-041 | Workplace AI | PASS | The two different robot ears kept as both sheets draw them. |
| CL-042 | AI Concentration | PASS | Equal panels and rules; red dollar matches. |
| CL-043 | Digital Government | PASS | Buildings and panel match. |
| CL-044 | Grid Demand | PASS | Removal of the bump and tail on the right wall confirmed. |
| CL-045 | Pricing Algorithms | FIX must | Lumpy knob where the string meets the front tag. |
| CL-046 | AI Infrastructure | FIX should | Chip and core 4 percent taller than wide; square them. |
| CL-047 | Data Rights | PASS | Key at W confirmed; stem vertical. |
| CL-048 | Public Records | PASS | Red rule at W confirmed. |
| CL-049 | Wealth Concentration | PASS | Stacks stand apart as drawn; image over catalogue. |
| CL-050 | Worker Bargaining | PASS | Figures, table and red double arrow match. |
| CL-051 | Market Power | PASS | Window marks made one shape; layout kept as drawn. |
| CL-052 | Household Security | PASS | House and red dollar ledger match. |
| CL-053 | Housing Scarcity | PASS | Dashed red house between two homes matches. |
| CL-054 | Home Equity | FIX should | Arrowhead uses a miter join; the set uses round. |
| CL-055 | Productivity | PASS | Desk figure, arrow and clock match. |
| CL-056 | Public Investment | PASS | Five rays, no hangers, three crests per line, as drawn. |
| CL-057 | Labor Share | PASS | Pie and red sector with its figure cut match. |
| CL-058 | Stock Ownership | PASS | Certificate, red seal and red bar match. |
| CL-059 | Credit Allocation | PASS | Two separate branches, no stem; image over catalogue. |
| CL-060 | Taxes & Benefits | FIX should | Rule 4 sits 0.31 px off the rule rhythm. |
| CL-061 | Household Income | PASS | Head offset kept; see open calls. |
| CL-062 | Assets & Debt | PASS | Coin stack and red minus badge match. |
| CL-063 | Essential Costs | PASS | House, bag and tag match; red bottle and dollar. |
| CL-064 | Trade Costs | PASS | Parcels, gate, red marks and arrow match. |
| CL-065 | Climate & Insurance | PASS | Rain cloud, house and red umbrella card match. |
| CL-066 | Energy & Emissions | PASS | Plug, cord, cloud and red plume match. |
| CL-067 | Healthcare | PASS | Equal cross arms; red pulse matches. |
| CL-068 | Education | FIX should | Hairline gap between page tops and the fork. |
| CL-069 | Childcare | PASS | Adult, child and red arm match. |
| CL-070 | Environment | FIX must | Knee in the leaf's top edge. |
| CL-071 | Policy | PASS | Page, rules and red knob match. |
| CL-072 | Reform | PASS | Branching path and red arrow match. |
| R-01 | All-Party Primaries | FIX must | Three arrowheads, three shapes. |
| R-02 | Ranked-Choice Voting | PASS | Frame 4 and numeral 2.6 weights kept; see open calls. |
| R-03 | Proportional Elections | PASS | 30 seats from the black sheet; red-only blob and bridges left out. |
| R-04 | Citizen Map Commissions | PASS | District lines at W confirmed. |
| R-05 | Automatic Registration | PASS | Card, person and red check badge match. |
| R-06 | On-Cycle Elections | FIX should | Arrowhead uses a miter join; the set uses round. |
| R-07 | Small-Donor Matching | FIX must | Knee and dent where the rear stack's hook arrives. |
| R-08 | Donor Disclosure | PASS | Ledger, dollar and red handle match. |
| R-09 | Stock-Trading Ban | PASS | Slash as one filled band, as the catalogue asks. |
| R-10 | Revolving-Door Limits | PASS | Torso 9.5 kept; shorter lower barb as drawn. |
| R-11 | Election Enforcement | FIX must | Black caps poke out at the red band corners; handle slit wobbles. |
| R-12 | Filibuster Reform | PASS | Bubbles, desk and red lock match. |
| R-13 | Congressional Capacity | PASS | People, capitol and book match; red lower page edge. |
| R-14 | Automatic Funding | PASS | Card, dollar and red arrow match. |
| R-15 | Watchdog Remedies | PASS | Lens, necked handle and red check match. |
| R-16 | Court Terms & Ethics | PASS | Scales, red clock and red check match. |
| R-17 | Civil Service | PASS | Card, figure and red brace match. |
| R-18 | Emergency-Power Limits | PASS | Red ears, black side ticks as the red sheet shows. |
| R-19 | Drug-Pricing Rules | PASS | Pill, red seam and red tag match. |
| R-20 | Merger Enforcement | PASS | Hairline drop confirmed; red neck as the red sheet shows. |
| R-21 | Labor-Law Remedies | PASS | Hard-hat worker, document and red check match. |
| R-22 | Wage Boards | PASS | 2.15 px move onto the shared axis confirmed. |
| R-23 | Indexed Minimum Wage | PASS | Four bars kept; image over catalogue. |
| R-24 | Paid Leave | PASS | Family, calendar, red date and red shield match. |
| R-25 | Child Tax Credit | PASS | Red coin ring as the red sheet shows. |
| R-26 | Automatic Recession Aid | PASS | House, coins and red falling arrow match. |
| R-27 | Tax Enforcement | FIX must | Handle ends stop short of the ring. |
| R-28 | Capital-Income Tax | PASS | Taller stack in front, as the sheet's lines show. |
| R-29 | Baby Bonds | FIX should | Child's arms and pig outline carry raster wobble. |
| R-30 | By-Right Housing | PASS | Homes, red door and red check badge match. |
| R-31 | Childcare Supply | PASS | Building, red door and figure match. |
| R-32 | Local-News Funding | PASS | Paper, red article block and coins match. |
| R-33 | Citizen Assemblies | PASS | Five people round the table; red centre figure. |
| R-34 | Participatory Budgeting | PASS | Faint ghost mark left out; open page frame kept. |
| R-35 | Term Limits · Rejected | PASS | Desk figure, clock and red X badge match. |
| R-36 | Public Investment | PASS | Red bulb, bridge and ledger with red dollar match. |
| R-37 | Feed Choice | PASS | Browser, red slider dot and keyhole match. |
| R-38 | Pricing-Data Limits | PASS | Two tags, red dollars and red prohibition sign match. |
| R-39 | Digital Service Teams | PASS | Three people kept; only the middle rule red, as the red sheet shows. |
| R-40 | Worker Voice on AI | PASS | Two message strokes and 16 pins, counted from the sheet. |
| R-41 | Grid Cost Allocation | PASS | Server, plug and bill with red dollar match. |
| R-42 | Congressional Tariff Votes | PASS | Whole ballot red; ribbed box as the sheet draws it. |
| R-43 | Disaster Mitigation | PASS | House, cloud, water and red roof band match. |
| R-44 | Digital Competition | FIX should | Windows sit 2.7 px apart in height. |
| R-45 | Paper Ballots & Audits | FIX must | Upper handle side stops 1.4 px short of the ring. |
| R-46 | Expand the House | FIX must | One seat size overrode the sheet's two seat types. |
| R-47 | Fusion Voting | PASS | Right connector mirrors the left, as the red sheet shows. |
| R-48 | Agency Independence | PASS | Red dot read as part of the brace, as the red sheet shows. |
| R-49 | Cross-Party Civic Work | PASS | Arc centred; collar, hooked arm and head bar as both sheets draw them. |
| R-50 | Popular-Vote Options | PASS | Four cards, card 3 dash, symmetric brace; map silhouette kept. |

## 3. Fix instructions

Coordinates are crop px. Keep every other part as it stands.

### CL-007 Turnout Equality
- Must. Take the three red marks from data-w 7 to W and keep their 25.5 px ink length: `mark-1` x 24.59 to 44.59, `mark-2` x 85.69 to 105.69, `mark-3` x 146.79 to 166.79, all at y 76.5. Remove `data-w` and its log entries. At W the marks still read and nothing closes, so the exception has no reason to exist.

### CL-009 Safe Seats
- Should. In `district`, delete the zero-length `L69.3 137.66` that repeats the end point of the arc ending at (69.3, 137.66).

### CL-016 Lobbying
- Must. Delete `mark-left`, the tick from (57.65, 44.4) to (59.25, 47.4). It floats off the left shoulder, attaches to nothing and has no partner on the mirrored right figure.

### CL-020 Track (pillar mark)
- Must. Extend the handle's upper-right side from (160.04, 104.45) 3.73 px along its own line to (157.47, 101.74), on the lens centreline, so the ring covers its butt end as it covers the lower-left side. The black sheet shows the handle joined to the ring on both sides.
- Must. Give both U-turns one radius, 14.5. Set the three straight runs at y 52.63, 81.63 and 110.63, with the right U centred at y 67.13 and the left U centred at y 96.13. Today the right U is r 14 and the left r 14.99, which shows as uneven loops in an identity mark.

### CL-021 Connect (pillar mark)
- Must. At the crossings (96.75, 26.38) and (96.75, 94.99), end the four black outer arcs with butt caps 2.75 px (3.17 deg of arc) past the crossing, so the black finishes in a sharp V pointing into the lens as on the red sheet. The current round caps push a soft blob 2.75 px into the red.

### CL-022 Act (pillar mark)
- Must. Make the ring concentric with the fingertip: centre (42.94, 38.34), r 27.02, same gap. Path: `M62.21 57.28 A27.02 27.02 0 1 0 24.51 58.10`.
- In the same pass, mirror the outer rays about y 39.06 from the fan origin (57.6, 39.06) at plus and minus 31.8 deg, inner radius 28.3, length 11.4: upper ray (81.65, 24.15) to (91.34, 18.14), lower ray (81.65, 53.97) to (91.34, 59.98). Leave the middle ray as it is.

### CL-024 Feedback Loop
- Should. Make `head-lower` the upper head turned 180 deg: points `51.62,100.04 34.9,99.1 32.18,112.58`.

### CL-045 Pricing Algorithms
- Must. The string's round end makes a lumpy knob at crop (42 to 47, 25 to 31). End the string 2 px shorter, at (42.96, 30.16), so its cap sits inside the front tag's right shoulder and leaves a clean V notch.

### CL-046 AI Infrastructure
- Should. Square the chip and core. Chip 62.04 px centred on (148.31, 60.92): x 117.29 to 179.33, y 29.9 to 91.94. Core 21.72 px: x 137.45 to 159.17, y 50.065 to 71.785. Pins at one pitch, 14.65 (x 133.66, 148.31, 162.96; y 46.27, 60.92, 75.57), all 17.5 long: top y 12.4 to 29.9, bottom y 91.94 to 109.44, left x 99.79 to 117.29, right x 179.33 to 196.83.

### CL-054 Home Equity
- Should. Remove `class="miter"` from `arrow-head` so its corner takes the round join. 27 of the set's 29 arrowheads use round joins, and R-26, the same rising chart arrow on another sheet, is round.

### CL-060 Taxes & Benefits
- Should. Move `rule-4` from y 87.6 to y 87.91 to sit on the rule rhythm.

### CL-068 Education
- Should. The page tops end at y 92.5 and the fork starts at y 93, which leaves a 0.5 px hairline. Set the `fork-top-cut` rect to y 84, height 10, so the fork starts at y 94 and the gap reads as the red sheet's clear 1.5 px.

### CL-070 Environment
- Must. The leaf's top edge has a knee at (60, 19.1): the curvature radius jumps from 48 to 317 and the curve inflects near (68, 17.4). Rebuild the edge from (17.57, 50.59) to the tip (103.5, 11.7) with continuous curvature and no inflection, within 0.75 px of the sheet, with the tip fixed.

### R-01 All-Party Primaries
- Must. Give the three arrowheads one shape, 90 deg with 8.85 px arms. `head-upper` points `105.6,37.75 105.6,46.6 96.75,46.6`. `head-lower` points `105.6,83.25 105.6,74.4 96.75,74.4`. `head-middle` points `100.99,54.07 107.25,60.33 100.99,66.59`. Today the middle head is a 79 deg chevron and the outer heads have unequal arms.

### R-06 On-Cycle Elections
- Should. Remove `class="miter"` from `arrow-head`. The sheet draws this tip as it draws R-07's, and every other level arrow in the set uses round joins.

### R-07 Small-Donor Matching
- Must. The rear stack's hook arrives 27 deg off vertical at (11.44, 85), which leaves a knee and an inner dent at crop (12 to 15, 83 to 88). Rebuild it to arrive with a vertical tangent at the join, for example `C15.8 77.2 11.44 79.2 11.44 85`, and check it against the sheet.

### R-11 Election Enforcement
- Must. Black round caps poke out past the red band corners at crop (108 to 112, 35 to 39), (129 to 134, 49 to 54) and (110 to 115, 71 to 76). Draw `body-left` and `body-right` before both bands so the red covers their caps. Replace `band-upper-inner-edge` with a butt-capped segment from (111.6, 38.46) to (128.59, 49.92), drawn after `band-upper`, so the black edge stays and its ends stop at the corners. Let the lower band's red sit over the end of `body-right`, as the red sheet shows.
- Should. Open the handle's slit to a constant 1.5 px over the last 20 px before the tip, from about (149, 84), keeping the outer edges within 0.5 px of the sheet.

### R-27 Tax Enforcement
- Must. Move both handle ends onto the ring's outer edge: the upper start from (123.71, 88.06) to (120.27, 84.71), and the lower end from (113.36, 94.68) to (111.5, 92.87). The black sheet shows both sides merged with the ring; the trace leaves a 2.3 px gap on one side and a tangent touch on the other.

### R-29 Baby Bonds
- Should. The child's arms use 34 cubic segments with 26 curvature reversals; the pig's forehead uses 18 with 20 reversals, its back 21 with 8, its belly 8 with 6. These are splines through raster samples. Rebuild each with a few clean curves, keeping the ear point, forehead notch, snout, feet, tail and hooked hands, within 0.5 px of the sheet.

### R-44 Digital Competition
- Should. Align the two browser windows: move each 1.35 px so both tops sit at y 12.625, with their contents moving with them. The 2.7 px offset reads as a mistake beside two equal windows.

### R-45 Paper Ballots & Audits
- Must. The handle's upper side stops 1.4 px clear of the ring, while the black sheet shows it merged. Start it at (157.61, 82.33), 5.1 px further along its line, on the ring's outer edge (r 37.35).

### R-46 Expand the House
- Must. The trace gives all 22 seats one size, 13.6 by 8.8. The sheet has two seat types, and the one size shrinks the inner windows to 3.3 px slots, so the inner rows read as solid chains. Sheet measurements: outer seats ink 20.5 by 14.4 with a 10.8 by 4.6 window; inner lower seats ink 17 to 18.5 by 16 with a 7.5 to 8.5 by 6 to 7 window; upper inner chain windows 6.4 to 7.6 by 5 to 6. Draw the ten outer seats at 15.5 by 9.5 on the centreline and the twelve inner seats at 12.5 by 11, all rx 2, equal within each group, mirrored, with the sheet's gaps (about 3 px outer, about 3.5 px inner lower). This overrides the earlier instruction to use one seat size, because the sheet draws two.

## 4. Open-call decisions

- CL-007 marks at data-w 7: drop to W. They read at W and nothing closes, so the extra weight is noise.
- R-02 cell frames at 4 and numerals at 2.6: keep. At W the frame's inside is 12.87 px against a 13.5 px numeral and the counters fill.
- R-10 torso at 9.5: keep. The torso is the figure's body mass on both sheets, and at W the walker turns into a stick figure.
- CL-029 data-w 10 and R-49 data-w 13.1 and 8.5: no call needed. These are mask cuts that make gaps, and they draw no ink.
- CL-016 teardrop mark: delete. It floats off one shoulder with nothing to attach to and no partner on the mirrored figure.
- CL-018 shield badge: keep the shield. Both sheets draw it, it is symmetric, and the spline runs smooth within 0.11 px.
- CL-046 4 percent tall squares: square them. The catalogue says square, and a 4 percent stretch reads as a near miss.
- R-20 dropped hairline: confirm the drop. It runs at a quarter of the set weight under one window only.
- R-22 2.15 px move: confirm. The central figure and the trapezoid top drifted together off the axis that the table, legs and side figures share.
- R-04 district lines at W: confirm. W closes no gap, and one weight holds the set together.
- CL-047 key and CL-048 red rule at W: confirm. Parts 1.15 to 1.27 times heavier on the sheet are generation noise, too small to read as a second weight.
- CL-061 head offset: keep. Both sheets draw it, and it matches the set's habit of heads leaning toward the action, as in CL-016 and CL-018.
- Image over catalogue: confirm all of these. CL-005 fourth figure, CL-023 five rules, CL-026 one leg, R-23 four bars, CL-059 no stem. The same holds for CL-012 and CL-017 red extent, CL-035 red window, CL-039 open top card, CL-049 separate stacks, R-25 red coin ring, R-28 taller stack in front, R-39 three people and one red rule, R-40 two message strokes, R-42 whole ballot red and ribbed box, R-48 red dot, and R-50 card 3 dash. In each case both sheets agree against the catalogue text.
- Raster clean-ups: confirm R-03 leaving out the red-only blob and the hairline bridges, R-34 leaving out the grey ghost mark, CL-044 removing the bump and tail, CL-051 making the window marks one shape, and keeping CL-025's dome foot gap and CL-041's two different ears, which both sheets draw.

## 5. Set-level findings

Method: `tile.py` in my scratchpad renders every red-black export from `work/build/assets/civic-line/red-black/` with the studio's `render_svgs.js` at 128, 64, 32 and 24 px on Newsprint #DCD9D2, then tiles them in catalogue order with IDs. I also measured arrowheads, magnifiers, ballot boxes, page corners, heads and stroke widths from the sources and exports.

- Weight and colour hold. 1,447 strokes export at 2.6807. The only other widths are R-02 (1.9496, 1.2672), R-10 (4.6303), CL-007 (3.4118, to go) and the mask cuts in CL-029 and R-49. Ink uses #121212 and #E63946 only. Black and white fills appear only inside masks, in seven icons.
- Arrowheads hold as one form. All 29 are open chevrons at 86 to 98 deg, except R-23 at 63 deg, which the sheet draws, and R-01's middle head at 79 deg, which is in the fix list. Arm lengths of 9 to 21 px follow each sheet's arrow size. Tips sit about 1 px behind the sheet's sharper tips everywhere, which is consistent and fine. Two heads break the round-join habit: CL-054 and R-06 use miter joins, while their sheets draw the same tip as the rest. Both are should fixes.
- Magnifiers hold. Eight lens-and-handle magnifiers run lens radius 21.5 to 37.5 and grip radius 5.5 to 7.05, close in proportion. Handle forms vary as the sheets vary: closed capsule (CL-023, CL-028, R-08), open U merging into the ring (CL-020, R-27, R-45), necked (R-15) and collared (R-20). Three open-U handles stop short of the ring where the black sheet shows them merged; their fixes are in the list.
- Ballot boxes follow their sheets. CL-001, CL-011, CL-015, CL-037 and R-42 differ in front proportion (width to height 1.4 to 2.8) and lid build, and so do their sheets. No flag.
- Page corners follow their sheets. Centreline radii run 2 to 7.25 px. A side-by-side check of CL-004, CL-012, CL-023, CL-028, CL-060 and R-18 against their red sheets shows each corner tracking its own sheet. No flag.
- Coin rims hold. CL-049, CL-062, R-07, R-26, R-28 and R-32 share one stack build: elliptical top rim over banded sides. R-07's rear-stack join is in the fix list.
- Caps and joins hold. Round caps and joins by default, butt only at colour splits and mask cuts, miter on architectural and page corners. The two miter arrowheads above are the only outliers.
- Heads hold. Repeats inside an icon are equal. Across icons the radius scales with figure size as the sheets draw it.
- Warning triangles in CL-033 and CL-037 differ by 0.8 px of corner radius (3 against 3.8). That is invisible at 128 px. No flag.
- Optical size, for information. The fixed export scale keeps every icon at one line weight, so wide compositions render small in the 128 grid: R-46, R-49, R-50, R-13, R-44 and CL-064 read smallest. That follows from the scale decision and needs no change in the masters.

## 6. Reading at 32 px and 24 px

Information only. The masters stay as they are. At 32 px the line is 0.67 px and at 24 px it is 0.5 px, so every icon greys out; the lists name the icons whose subject stops reading.

**Stops reading at 32 px (28):** CL-009, CL-014, CL-017, CL-035, CL-036, CL-037, CL-038, CL-041, CL-045, CL-046, CL-056, CL-063, CL-064, CL-065, R-01, R-04, R-12, R-13, R-16, R-24, R-34, R-36, R-40, R-42, R-43, R-46, R-49, R-50. Most combine three or more subjects or rely on a small inner sign (a dollar, a check, "AI", a lock). R-34's checked box reads like an envelope, as it does on the sheet.

**Also stops reading at 24 px (53 more):** CL-002, CL-003, CL-005, CL-007, CL-008, CL-011, CL-012, CL-015, CL-016, CL-018, CL-025, CL-026, CL-027, CL-029, CL-030, CL-033, CL-034, CL-042, CL-043, CL-044, CL-049, CL-052, CL-053, CL-055, CL-058, CL-059, CL-062, CL-066, CL-069, R-02, R-03, R-07, R-10, R-11, R-18, R-20, R-21, R-22, R-25, R-26, R-28, R-29, R-30, R-31, R-32, R-33, R-35, R-38, R-39, R-41, R-44, R-47, R-48.

**Still reads at 24 px (41):** CL-001, CL-004, CL-006, CL-010, CL-013, CL-019, CL-020, CL-021, CL-022, CL-023, CL-024, CL-028, CL-031, CL-032, CL-039, CL-040, CL-047, CL-048, CL-050, CL-051, CL-054, CL-057, CL-060, CL-061, CL-067, CL-068, CL-070, CL-071, CL-072, R-05, R-06, R-08, R-09, R-14, R-15, R-17, R-19, R-23, R-27, R-37, R-45. All four pillar marks are in this group.

## 7. Pillar marks (DR-04)

- **CL-019 Explain: ready now.** The book mirrors about the spine with one curve per edge type, the three red rays centre on the spine, and the edges sit within 0.5 px of the sheet at the 95th percentile. Hollow pages, the doubled lower edge and the cover stubs all match both sheets.
- **CL-020 Track: ready after two must fixes.** The handle's upper side has to reach the ring, and the two U-turns need one radius. Pin, path and lens otherwise hold.
- **CL-021 Connect: ready after one must fix.** The circles are true, equal and on one baseline. The black arcs have to end in a sharp V at both crossings so the red lens keeps its points.
- **CL-022 Act: ready after one must fix.** The ring has to share the fingertip's centre and the outer rays have to mirror about the middle ray. The hand itself holds.

## 8. What I tested and what I could not

Tested:
- Every icon's 2 by 2 composite (red sheet, trace, overlay, difference) at 4x, plus close zooms where a join, cap, gap or count was in doubt.
- Curvature and residual checks on cubic paths for wobble and knees (CL-018, CL-070, R-07, R-29, R-50 and others).
- Seat and window sizes on R-46 from the sheet's connected components.
- Set tiles of all 122 red-black exports at 128, 64, 32 and 24 px, and the arrowhead, magnifier, ballot box, corner, head, stroke-width and colour measurements above.

Not tested:
- How the fixes look once drawn; the tracers' rebuilds need a second look.
- The black-only and PNG exports, beyond what the red-black files share with them.
- Reading at 32 and 24 px in a live page or with users; the lists come from my eye on the rendered tiles.

## 9. Change log

Created:
- `work/handoffs/phase-2/20261029_Civic-Line-Review.md`
- `work/handoffs/phase-2/20261029_Civic-Line-Review-Fixes.json`

Scratchpad only, outside the project: review composites, zooms and `tile.py` with its tiles under `/tmp/claude-0/-home-user-Dustin-s-Command-Center/c42d0deb-36cd-5cae-968f-07f59acdce92/scratchpad/review/`.

Modified: none.
