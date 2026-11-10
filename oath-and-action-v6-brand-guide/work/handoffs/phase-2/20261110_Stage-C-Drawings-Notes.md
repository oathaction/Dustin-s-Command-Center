# Stage C, round 0: icon designer's notes

Oath & Action Edition 06, Phase 2, November 10, 2026. Written by the icon designer (`oa-design-director`), one hand for every new drawing in this stage, under `20261110_Stage-C-Brief.md` ("Round 0 tasks, Icon designer") and the main session's addition on Housing and options. For the creative director, the board builder of drawings board C (`20261110_Drawings-Board-C-Brief.md`) and the main session.

## Where the work stands

Round 0 is done. The 37 fits, the 16 px Pause and Filter redraws, three Housing options with their editions and tiles, the previews and the checks are all built by one script and ready for the creative director's scores and the board. Nothing here is in use: every file waits for Dustin's approval by name on drawings board C.

**Rebuild:** `python3 -I work/build/scripts/phase-2/civic_line_stage_c_drawings.py` (parts: `--part fits`, `utility`, `housing`, `previews`, `measure`; `--draft <ID>` prints the first draft of a fit). It writes only new files and reads the masters, the approved utility files and the pillar fits without changing them.

## What I drew

**The 24 px fits for the 37 (DR-198, DR-205, D2-1132).** One fit for each topic and atlas drawing on the list in `20261110_Stage-B-Ch10-Construction.md`, section 10, drawn pixel by pixel on the 24 px grid as the approved pillar fit B was (DR-179): every pixel is Charcoal or empty, the line is one pixel, and each file is the black edition only. Each fit keeps the parts its master's construction note names, the accent's shape included, drawn in the ink since nothing under 48 px takes red. Each drawing grows toward 22 px across, between 1.01 and 1.39 times its master's extent at 24 px, and sits centered on the box, as the pillar fits grew (D2-613). The switch is the pillar icons' own: the fit on 1x screens, the master from 2x.

How I drew them. For each drawing the script's `--draft` step first rasterizes the master's own centerlines onto the grid; that draft is kept only as the record of where each map began. I then redrew every map by hand against the master rendered sharp at 8 and 16 times with the grid laid over it, and judged each fit at true size beside its master as a 1x screen draws it. The maps in the script are the finals. A one-line account of what each fit holds sits in the script (`FIT_NOTES`) and in the manifest.

**The 16 px Pause and Filter (DR-197).** Pause, once, exactly as DR-197 sets it: bars widened from 4 to 5 px, x 2 to 7 and 9 to 14. Filter, two options, because a 5 px spout cannot sit centered on the funnel with both outer edges on whole pixels: option A widens the spout to the right and keeps both outer edges on whole pixels; option B widens it half a pixel each side, so the funnel stays symmetric and the spout's inner edges fall on whole pixels. Everything else is the approved files'. The generators first rebuild the approved Pause and Filter paths byte for byte, so each redraw changes only what DR-197 names.

**Housing (DR-196).** Three options in Civic Line's construction, drawn and baked with the stage B family code as Testify and Contact an Official were: the 5.5 source px line, round caps and joins, one red accent, the capped fit of DR-08. Each has four editions, 12 tiles and previews beside its nearest settled drawings.

## Housing meaning note

Written before drawing, as D2-502 had the research lead do for Testify and Contact an Official, from the atlas model (`work/extract/atlas-v7-data.json`, read by script).

- **V7's name and ID.** The atlas has no node called Housing. The subject runs through three variables, all in domain D09 "Housing, health care and getting ahead": A5 Housing scarcity ("A shortage of homes where people need or want to live"), A6 Homeowners' equity ("The value owners hold in their homes after mortgage debt") and EC9 Cost of essentials ("What households pay for necessities such as housing, care and insurance"). Loop R8 ties the first two together ("Housing scarcity strengthens owners' incentive to restrict building"). Four issues carry it to readers: I129 zoning limits on new homes, I130 homes that do not reach the lowest-income renters, I131 homebuying subsidies, I132 eviction. Reforms R-30 (more homes allowed by right near jobs), R-38 (limits on rent-pricing software) and R-43 (building codes against disaster losses) act on it.
- **Its meaning in one sentence.** Housing is where people live and what it costs them to rent or own a home: how many homes get built, who can afford one and who can stay in it.
- **What a reader must recognize.** Homes for many households, renters as well as owners. A single house says "home" (the home page, a residence or an address) and in Civic Line it already stands for one household: it is the base of CL-052 Household Security, CL-054 Home Equity, CL-063 Essential Costs, CL-065 Climate & Insurance, R-26 and R-43, and rows of narrow houses carry CL-053 Housing Scarcity, CL-035 Residential Sorting and R-30 By-Right Housing. A Housing drawing has to stand apart from all of them.
- **What readers expect.** The U.S. Web Design System's icon set names its house glyph "home" (designsystem.digital.gov/components/icon, read November 10, 2026), which confirms the collision. The best-known U.S. housing mark, a house around an equal sign, is HUD's Equal Housing Opportunity logo: it narrows the subject to fair housing and imitates a federal mark, so I did not draw from it. My web search found no public topic system that documents its housing icon, so this point rests on that one icon set and on the set's own drawings.

## Housing: the three options

Files in `work/build/assets/civic-line-new-topics/`: `src/20261110_Housing-Option-<X>.svg`; `svg/20261110_Housing-Option-<X>-Red-Black.svg`, `-Black.svg`, `-Red-Newsprint.svg`, `-Newsprint.svg`; `png/` at 128 and 256 px; `tiles/<shape>-<tile>/svg|png-256|png-512/`; `previews/`; `qa/`; `20261110_Stage-C-Housing-Manifest.json`. Likeness is the engineer's check at 24 px against the 124 drawings in use (flag 0.9092, watch 0.8678); every pair is in `qa/20261110_Housing-Likeness-All-Pairs.json`. The naming test is my own reading at 48 px with no label, one reader's guess; the creative director repeats it.

| Option | What it shows | Red | Naming test (mine) | Closest settled drawing | CL-054 Home Equity | CL-053 / R-30 / CL-063 | Tile margin |
|---|---|---|---|---|---|---|---|
| A | An apartment block of three floors and a pitched-roof house on one ground line | One window of the block: one household's home among many | "Housing" or "homes"; at worst "neighborhood" | CL-051 Market Power, 0.690 (42nd percentile) | 0.501 | 0.251 / 0.290 / 0.575 | 22.3 units |
| B | One apartment house: three floors under a pitched roof, two windows a floor, an arched door | The door | "Apartment building"; at worst "house" or "school" | CL-033 Hostile Content, 0.659 (34th) | 0.482 | 0.398 / 0.413 / 0.461 | 21.6 units |
| C | A house key: a key whose bow is a house, with a stem and two teeth | The house-shaped bow | "House key", which a reader may call "home" or "real estate" | CL-022 Act, 0.656 (33rd) | 0.270 | 0.058 / 0.269 / 0.469 | 24.1 units |

Nothing is flagged or watched; the check exits 0. Between the options: A and B 0.452, A and C 0.431, B and C 0.165, so each is a different choice. All three sit at the cap (line 3.3508 units). The engineer's pixel fit check at 48 px, their floor: each fails only on straight edges, as every master does, keeps its smallest gap at 1.7 px or more and keeps every counter. Every tile keeps at least 21 units to its edge, the set's minimum in chapter 10, section 8.

**Which reads best.** At 48 px and up, A says housing as the atlas means it, homes of more than one kind, and keeps furthest from the house drawings that mean one household. Its block echoes CL-051's tower at 48 px, though the house beside it and its outlined windows keep the two apart (0.690, the median of the set's pairs). C is the clearest silhouette at every size, yet its bow is a house, so it leans toward "home". B is the plainest building and the most likely to be named something else.

**Does Housing read at 24 px?** As a master on a 1x screen it draws a gray line like the 37 do, so it would need its own pixel fit. On a 2x screen, at 48 device pixels, all three read beside their neighbors (`previews/*-Neighbors-24px-*-2x.png`). On a 1x screen C still reads as a key, A reads as two buildings whose windows close up, and B reads as a house. Housing is not on the list of 41, so it stays at 48 px and up until Dustin adds it (question 5).

## The 16 px Pause and Filter

Files in `work/build/assets/utility-16-redraw/`: `svg/20261110_Utility-Pause-16px-Redraw.svg`, `20261110_Utility-Filter-16px-Redraw-A.svg`, `-B.svg`; `png/` at 16 and 32 px in Charcoal; `previews/` (each beside the approved file at 16 px, 1x and 2x, Newsprint and Charcoal, and the 1x pair enlarged 10 times with a pixel grid); `qa/`; the manifest. "Open" is a pixel inside the opening with alpha under 8 when drawn at 16 px on a 1x screen.

| File | Open pixels | Row 8, inside the opening (alpha, 255 is full ink) | Pixel fit check, 16 px, 1.5 px line |
|---|---|---|---|
| Approved Pause (DR-171) | none: 0 of 8 rows in each bar | 127, 128 | Pass |
| **Pause redraw** | one on every row: 8 of 8 rows in each bar | 128, 0, 128 | Pass |
| Approved Filter (DR-169) | none: 0 of 4 spout rows | 127, 128 | Pass |
| **Filter redraw A** | one on 3 of 4 spout rows; on the fourth the slanted foot begins and the pixel draws 72 | 128, 0, 128 | Pass |
| **Filter redraw B** | one or two on 4 of 4 spout rows | 0, 0 (outer edges 128) | Pass |

Option A keeps the approved file's construction, both outer edges on whole pixels, and matches the Pause redraw; its right cone side meets the spout about a pixel higher than the left. Option B keeps the funnel symmetric and opens the spout fully, and its outer edges draw half gray.

## The 24 px fits: figures

Files in `work/build/assets/civic-line-24-fit/`: `svg/20261110_Civic-Line-24px-Fit-<ID>-<Slug>-Black.svg`; `png/` at 24 and 48 px, transparent; `previews/<stem>-Pair-<Newsprint|Charcoal>-<1x|2x>.png` (the master and the fit side by side as a 1x and as a 2x screen draws them) and four sheets of all 37; `qa/`; `20261110_Civic-Line-24px-Fits-Manifest.json` with every map and figure.

**Full ink.** The share of a drawing's ink pixels (alpha 8 or more) that reach full ink (alpha 247 or more) at 24 px on a 1x screen, from the pixel fit check's own soft-edge count. No master line reaches full ink: 32 masters have no full-ink pixel at all, and the five that have some (CL-031 3.2%, CL-032 5.0%, CL-051 2.1%, CL-057 8.3%, R-06 1.1%) have them only in filled parts. Drawn with those fills removed, the five's darkest line pixels reach alpha 161 to 211 of 255. The creative director counted 2 of 18 masters reaching full Charcoal; in my render on Newsprint, 4 of the first 18 on the list do (CL-031, CL-032, CL-051 and CL-057), each only through a filled part, so the count differs while the finding holds: no line reaches full ink. Every fit is 100%. The masters' main line measures 0.55 to 0.65 px at 1x.

| ID | Word | Atlas | Full ink, master | Full ink, fit | Fit across | Growth | Pixel fit | Like own master | Closest other drawing |
|---|---|---|---|---|---|---|---|---|---|
| CL-001 | Voting | | 0% (0 of 135) | 100% | 22 px | 1.35 | Pass | 0.561 | CL-048 Public Records, 0.726 |
| CL-004 | Petition | | 0% (0 of 157) | 100% | 20 px | 1.36 | Pass | 0.656 | CL-060 Taxes & Benefits, 0.692 |
| CL-006 | Civic Ties | B3 | 0% (0 of 117) | 100% | 22 px | 1.24 | Pass | 0.771 | CL-040 Platform Power, 0.748 |
| CL-010 | Decisive Primaries | C2 | 0% (0 of 113) | 100% | 22 px | 1.11 | Pass | 0.927 | R-39 Digital Service Teams, 0.819 |
| CL-013 | Incumbent Defeat | C5 | 0% (0 of 117) | 100% | 22 px | 1.34 | Pass | 0.712 | CL-039 Feed Ranking, 0.616 |
| CL-023 | Evidence | | 0% (0 of 211) | 100% | 22 px | 1.20 | Pass | 0.828 | CL-060 Taxes & Benefits, 0.733 |
| CL-024 | Feedback Loop | | 0% (0 of 118) | 100% | 22 px | 1.26 | Pass | 0.594 | R-07 Small-Donor Matching, 0.581 |
| CL-028 | Watchdogs | D4 | 0% (0 of 156) | 100% | 22 px | 1.39 | Pass | 0.656 | CL-023 Evidence, 0.782 |
| CL-031 | Local Government | | 3.2% (6 of 188) | 100% | 22 px | 1.05 | Pass | 0.982 | R-31 Childcare Supply, 0.872 |
| CL-032 | Local Reporting | B2 | 5.0% (12 of 240) | 100% | 22 px | 1.28 | Pass | 0.751 | CL-052 Household Security, 0.769 |
| CL-039 | Feed Ranking | TC1 | 0% (0 of 269) | 100% | 22 px | 1.23 | Pass | 0.489 | CL-055 Productivity, 0.421 |
| CL-040 | Platform Power | TC2 | 0% (0 of 143) | 100% | 22 px | 1.20 | Pass | 0.748 | CL-068 Education, 0.760 |
| CL-047 | Data Rights | | 0% (0 of 156) | 100% | 20 px | 1.36 | Pass | 0.528 | CL-023 Evidence, 0.554 |
| CL-048 | Public Records | | 0% (0 of 171) | 100% | 22 px | 1.16 | Pass | 0.804 | R-21 Labor-Law Remedies, 0.630 |
| CL-050 | Worker Bargaining | A2 | 0% (0 of 177) | 100% | 22 px | 1.01 | Pass | 0.956 | CL-007 Turnout Equality, 0.902 |
| CL-051 | Market Power | A3 | 2.1% (4 of 187) | 100% | 22 px | 1.06 | Pass | 0.927 | CL-023 Evidence, 0.773 |
| CL-054 | Home Equity | A6 | 0% (0 of 173) | 100% | 22 px | 1.08 | Pass | 0.958 | CL-052 Household Security, 0.898 |
| CL-057 | Labor Share | EC3 | 8.3% (11 of 133) | 100% | 21 px | 1.30 | Pass | 0.592 | CL-059 Credit Allocation, 0.372 |
| CL-060 | Taxes & Benefits | EC6 | 0% (0 of 194) | 100% | 22 px | 1.23 | Pass | 0.700 | CL-039 Feed Ranking, 0.668 |
| CL-061 | Household Income | EC7 | 0% (0 of 107) | 100% | 22 px | 1.13 | Pass | 0.917 | R-06 On-Cycle Elections, 0.812 |
| CL-067 | Healthcare | | 0% (0 of 139) | 100% | 20 px | 1.27 | Pass | 0.506 | R-01 All-Party Primaries, 0.619 |
| CL-068 | Education | | 0% (0 of 212) | 100% | 21 px | 1.05 | Pass | 0.931 | CL-019 Explain, 0.823 |
| CL-070 | Environment | | 0% (0 of 124) | 100% | 22 px | 1.19 | Pass | 0.746 | CL-029 Public Services, 0.647 |
| CL-071 | Policy | | 0% (0 of 174) | 100% | 22 px | 1.28 | Pass | 0.686 | CL-039 Feed Ranking, 0.712 |
| CL-072 | Reform | | 0% (0 of 88) | 100% | 22 px | 1.24 | Pass | 0.797 | R-24 Paid Leave, 0.613 |
| R-05 | Automatic Registration | R-05 | 0% (0 of 187) | 100% | 22 px | 1.20 | Pass | 0.856 | CL-003 Registration, 0.881 |
| R-06 | On-Cycle Elections | R-06 | 1.1% (2 of 190) | 100% | 22 px | 1.01 | Pass | 0.947 | R-41 Grid Cost Allocation, 0.917 |
| R-08 | Donor Disclosure | R-08 | 0% (0 of 134) | 100% | 22 px | 1.29 | Pass | 0.792 | CL-023 Evidence, 0.886 |
| R-09 | Stock-Trading Ban | R-09 | 0% (0 of 183) | 100% | 22 px | 1.29 | Pass | 0.626 | CL-052 Household Security, 0.717 |
| R-14 | Automatic Funding | R-14 | 0% (0 of 195) | 100% | 22 px | 1.11 | Pass | 0.911 | R-45 Paper Ballots & Audits, 0.892 |
| R-15 | Watchdog Remedies | R-15 | 0% (0 of 163) | 100% | 22 px | 1.06 | Pass | 0.961 | R-01 All-Party Primaries, 0.868 |
| R-17 | Civil Service | R-17 | 0% (0 of 190) | 100% | 22 px | 1.13 | Pass | 0.904 | R-23 Indexed Minimum Wage, 0.831 |
| R-19 | Drug-Pricing Rules | R-19 | 0% (0 of 116) | 100% | 21 px | 1.10 | Pass | 0.931 | R-24 Paid Leave, 0.829 |
| R-23 | Indexed Minimum Wage | R-23 | 0% (0 of 160) | 100% | 22 px | 1.36 | Pass | 0.574 | CL-023 Evidence, 0.623 |
| R-27 | Tax Enforcement | R-27 | 0% (0 of 157) | 100% | 20 px | 1.31 | Pass | 0.660 | CL-023 Evidence, 0.826 |
| R-37 | Feed Choice | R-37 | 0% (0 of 198) | 100% | 22 px | 1.04 | Pass | 0.926 | R-32 Local-News Funding, 0.861 |
| R-45 | Paper Ballots & Audits | R-45 | 0% (0 of 200) | 100% | 22 px | 1.10 | Pass | 0.920 | CL-044 Grid Demand, 0.850 |

"Like own master" is the fit against its own master at 24 px; it runs low where the fit grew most and where the master's gray line blurs to a soft shape (CL-039 0.489, CL-067 0.506), and it is reported apart by the check and never fails.

**The five look-alikes (D2-971).** Every one of their ten pairs moved apart. Each set was run through the likeness check under neutral names (`qa/20261110_Five-Look-Alikes-*-Likeness.json`).

| Pair | Masters | Fits | Change |
|---|---|---|---|
| CL-028 and R-27 | 0.958 | 0.861 | −0.097 |
| R-08 and R-27 | 0.945 | 0.770 | −0.175 |
| CL-028 and R-08 | 0.942 | 0.842 | −0.100 |
| CL-023 and CL-028 | 0.927 | 0.897 | −0.030 |
| CL-023 and R-08 | 0.892 | 0.855 | −0.037 |
| CL-023 and R-27 | 0.885 | 0.809 | −0.076 |
| R-08 and R-45 | 0.876 | 0.865 | −0.011 |
| CL-023 and R-45 | 0.850 | 0.764 | −0.086 |
| CL-028 and R-45 | 0.817 | 0.702 | −0.115 |
| R-27 and R-45 | 0.802 | 0.717 | −0.085 |

Among the masters four of these pairs sit above the flag line; among the fits none does. CL-023 and CL-028 stay on the watch line (0.897), so D2-971's rule still matters: two of the five never share a view at 24 px.

**The checks across the set.**
- Pixel fit check (`node work/build/scripts/phase-2/icon_pixel_fit_check.js --size 24 --weight 1 <fits>`): 37 of 37 pass at 1x and 2x, with no soft pixel, every straight edge on a pixel edge, a one-pixel main line, gaps of at least one pixel and every counter kept. The 37 masters at 24 px: 0 of 37 pass; at 1x all fail on width, 36 on straight edges, 35 on soft pixels, 33 on counters and 31 on gaps.
- Likeness check (`node work/build/scripts/phase-2/icon_likeness_check.js work/build/assets/civic-line-24-fit/svg/`): exit 1, two pairs flagged and 16 to watch. To read them I ran the same check on the 37 masters under neutral names (`qa/20261110_Masters-Baseline-Likeness.json`), so each pair carries its masters' own figure (in the manifest). Both flags are inherited: R-06's fit against R-41 Grid Cost Allocation (0.917; the masters 0.937) and against R-44 Digital Competition (0.915; the masters 0.964, among the closest pairs in the set). Of the 18 flagged or watched pairs, one grew closer than its masters: R-06 against CL-046 AI Infrastructure, 0.903 to 0.908, under the flag line.
- CL-050 was redrawn after the first run: with 3 px heads its fit crossed the flag line against R-30 By-Right Housing (0.912, where the masters measure 0.909) and grew toward CL-035 and five other masters. With 4 px heads, the people sign the other fits use, every pair of CL-050's on or above the watch line fell under its masters' figure (R-30 0.866, CL-007 0.902 against 0.928).

## Routine calls

- D2-xxx | The fits are drawn pixel by pixel with a one-pixel line, every pixel Charcoal or empty | The approved pillar fit B's construction (DR-179); one pixel is the nearest whole-pixel weight to the masters' 0.55 to 0.65 px line
- D2-xxx | One fit for each of the 37, no second fit | No drawing offered two real ways to keep its parts at 24 px; where a part could not keep its own form, the fit's note says how it was kept (R-06's chevron, R-19's tag hole)
- D2-xxx | Each fit grows toward 22 px across, 1.01 to 1.39 times its master, centered on the box | The pillar fits' D2-613; at the masters' own size, rules and heads fall closer than one pixel apart
- D2-xxx | A fit file holds one path, data-part base, with no accent group | One color, black edition only (D2-1132); the accent's shape stays in the drawing, in ink
- D2-xxx | A master's visible corner radius shows as one dropped corner pixel; corners the master draws nearly square stay square | One pixel cannot draw a curve smaller than itself
- D2-xxx | Rings are clean pixel rings with no doubled pixel, and CL-057's large ring is a midpoint circle | Each ring keeps its counter
- D2-xxx | The Civic Line person at 24 px is a 4 px ring over open shoulders with one empty row between, where the room allows (CL-006, CL-040, CL-050, R-17); a 3 px ring in R-05 and a 5 px ring in CL-061, where the master's head is smaller or larger | One person sign across the fits, and the 3 px heads drew CL-050 toward R-30
- D2-xxx | One dollar sign for every fit that holds one (R-08, R-14, R-19, R-23): a top tick over a squared S, 3 by 6 pixels | At true size it reads as a dollar where a thin S read as a pound sign, and it fits each page without stretching it
- D2-xxx | A drawing whose center line must stay one pixel wide is drawn on column 11 (CL-068); one that cannot move keeps a one-pixel stem half a pixel off the axis (CL-040) | One pixel cannot straddle the box's center
- D2-xxx | R-06's arrow between the calendars becomes a chevron | Each calendar needs nine columns to keep its three columns of date dots, the middle one the master's accent, which leaves four columns between them
- D2-xxx | R-19's tag loses its string hole | At 24 px the hole cannot keep a clear pixel from the roof without stretching the tag; the string, the pentagon and the dollar carry the tag
- D2-xxx | R-37's window grows one row taller than its master's proportion | Its three dots need their own row between the top edge and the header
- D2-xxx | Full ink is the pixel fit check's own measure: alpha 247 or more among ink pixels of alpha 8 or more | One definition, from the check the brief names
- D2-xxx | A baseline run of the 37 masters under neutral names gives every flagged or watched pair its masters' figure | The stage B notes' method, so a flag reads as inherited or new
- D2-xxx | Previews show the master and the fit as a 1x screen and as a 2x screen draw them, on Newsprint and Charcoal; on Charcoal the master is its Newsprint edition and the fit's ink is Newsprint, as the sprite sets it | DR-179's switch and the board brief
- D2-xxx | The checks' pixel pictures stay in my scratch folder; their JSON results sit in each folder's qa/ | As D2-618
- D2-xxx | Pause is redrawn once, exactly as DR-197 sets it; Filter has two options | DR-197 fixes Pause's bars; a 5 px spout cannot be centered with both outer edges on whole pixels, a real choice (D2-622)
- D2-xxx | The redraws come from generators that first rebuild the approved files byte for byte | Proof that each redraw changes only the widths DR-197 names
- D2-xxx | Housing has three options | Three real, clear choices: homes of more than one kind, one apartment house, a house key (DR-146, D2-622)
- D2-xxx | Housing draws no lone house, no row of narrow houses, no house with an object and no equal sign | Each collides with "home", with the set's household drawings or with HUD's Equal Housing Opportunity mark
- D2-xxx | Housing B's ground line is shortened | It kept 20.07 units to the circle tile's edge; chapter 10 states every drawing keeps at least 21
- D2-xxx | Housing's tiles take the 48 px bare floor, so 72, 76 and 80 px | No 32 px reading is approved for it

## Questions for Dustin

1. **The 37 fits (card 3).** Approve all 37 by name, with the pillar icons' switch: the fit on 1x screens, the master from 2x. *Recommendation:* yes, all 37. Every fit passes the pixel fit check, every line reaches full ink where no master line does, and the five look-alikes all moved apart.
2. **Pause (card 2).** *Recommendation:* approve the redraw by name. It opens one whole pixel on every row of each bar, where the approved file opens none.
3. **Filter, A or B (card 2).** *Recommendation:* A. It keeps the approved file's construction with both outer edges on whole pixels, matches the Pause redraw, and opens a whole pixel on three of the spout's four rows. B opens every row and keeps the funnel symmetric, but its outer edges draw half gray at 16 px.
4. **Housing, which option (card 1).** *Recommendation:* A, homes of more than one kind. It names housing as the atlas covers it, renters and owners alike, and keeps furthest from the drawings where a house means one household (0.50 against CL-054, 0.25 against CL-053, 0.29 against R-30). If you would rather have the clearest small shape, C, the house key, is the one; it may be named "home".
5. **Housing at 24 px.** Housing is not on the list of 41, and adding it changes what DR-136 approved. *Recommendation:* keep it at 48 px and up for now. If you want it in kickers, I draw its 24 px fit once you pick an option, and it joins the list by your approval.
6. **R-06 at 24 px.** Its fit is flagged against R-41 and R-44, as its master already was, more closely. *Recommendation:* no change to the fit; when chapter 10 sets neighbors side by side (Rule 10.9), R-06, R-41 and R-44 can join the groups that never share a view at small sizes, as the five do.

## Tested

- The pixel fit check on the 37 fits at 24 px with a one-pixel line, at 1x and 2x: 37 of 37 pass.
- The pixel fit check on the 37 masters at 24 px, for their full-ink figures; the five masters with fills drawn with those fills removed, to show no line reaches full ink; and the first 18 masters on Newsprint at 1x, counting pixels that reach Charcoal, to compare with the creative director's count.
- The likeness check on the 37 fits against the 124 masters and each other; the same check on the 37 masters under neutral names as a baseline; the five look-alikes as masters and as fits; CL-050's variants before I chose one.
- The pixel fit check at 16 px with a 1.5 px line on the approved Pause and Filter and the three redraws: all pass. The open pixels in each opening, counted from 1x renders.
- The generators rebuild the approved Pause and Filter paths byte for byte.
- Housing: the likeness check on the three options with every pair listed; the pixel fit check at 48 px; each tile's margin to its edge with the October tile code's own measure.
- Visual review, in Chromium at device scale 1 and 2: every fit against its master sharp at 8 and 16 times with the grid, then at true size beside the master; the contact sheets on Newsprint and Charcoal; Housing at 128, 48 and 24 px beside its neighbors on both surfaces; the redraws at 16 px on 1x and 2x and enlarged 10 times.
- My own naming reading of the Housing options at 48 px with no label.

## Not tested

- Real screens. Every render is Chromium on Linux at device scale 1 or 2; no 1.25 or 1.5 scale, no other browser, no Windows or macOS text rendering.
- The switch in the guide's sprite, which the engineer builds.
- Whether people can name any fit, redraw or Housing option. No reader test covers them (DR-202); the naming readings are mine, one reader.
- The fits in a live kicker beside Inter text at 24 px.
- October's `verify_set.check_tile` on the Housing tiles; I checked their structure and margins with the tile code's own functions, not with that script.
- Whether Housing reads at 32 px, which would set a lower tile floor.
- The creative director's scores and naming test, which come next.

## Change log

Created:
- `work/build/scripts/phase-2/civic_line_stage_c_drawings.py`
- `work/build/assets/civic-line-24-fit/`: `svg/` (37), `png/` (74), `previews/` (152: 148 pairs and 4 sheets), `qa/` (6 JSON), `20261110_Civic-Line-24px-Fits-Manifest.json`
- `work/build/assets/utility-16-redraw/`: `svg/` (3), `png/` (6), `previews/` (18), `qa/` (1 JSON), `20261110_Utility-16px-Redraw-Manifest.json`
- `work/build/assets/civic-line-new-topics/`, new dated files beside stage B's: `src/` (3), `svg/` (12), `png/` (24), `tiles/` (36 SVGs, 72 PNGs), `previews/` (36), `qa/` (3 JSON), `20261110_Stage-C-Housing-Manifest.json`
- `work/handoffs/phase-2/20261110_Stage-C-Drawings-Notes.md` (this file)

Modified: none. Removed: none. Scratch work stays in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/67af6aec-b8e0-5b79-b000-c172e734e753/scratchpad/stage-c/icons/`.
