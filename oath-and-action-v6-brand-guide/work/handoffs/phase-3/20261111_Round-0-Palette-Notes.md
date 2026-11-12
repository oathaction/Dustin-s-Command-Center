# Round 0 palette notes: data palettes, proofs and the proposed chart tokens

Oath & Action Edition 06, Phase 3, round 0, November 11, 2026. Written by the data visualization and systems lead (`oa-dataviz-systems-lead`), with the design director's eye, for `work/handoffs/phase-3/20261111_Phase-3-Round-0-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

**The palette proposal is ready for the engineer:** `work/handoffs/phase-3/20261111_Palette-Proposal.json`. It holds 40 proposed tokens, each with its path under the token architecture, its value or alias, the surfaces it serves, its measured ratios and its reason, plus five description changes and six existing tints that take a second job. At 21:54 UTC I added the surfaces and ratios of those six tints to the file; no value changed.

Two colors are new, both Prussian mixed toward Newsprint in OKLab, so diverging pair B works on Charcoal in the dark theme: `oa.color.tint.prussianN56` (#828A9D, 5.42 to 1 on Charcoal) and `oa.color.tint.prussianN29` (#505C7D, 2.83 to 1, its value printed). Every other proposed token points at a value the release already holds:

- **Diverging on Charcoal** (10 tokens): the two new Prussian steps, the Charcoal band tint as the midpoint, and the sequential scale's Charcoal steps 3 and 4 as the Verdigris half. Each Prussian step matches its Verdigris partner in lightness within 0.002.
- **Categorical, four inks** (16 tokens, DR-234): Charcoal, Verdigris, Prussian and Stone on Newsprint; Newsprint, Verdigris, Prussian 62 percent toward Newsprint and Stone on Charcoal (the order changed in the fix pass; see below). The Stone group always carries the hatch, and every group carries a direct label and, on a line, its own end marker.
- **Ghost lines** for small multiples past four groups (2 tokens).
- **The grade line code** (10 tokens): the atlas build's patterns as stroke styles per 1 px of line width, the record square, the hollow line, the dotted line's clearance before its arrowhead and the shortest textured run (set in the fix pass under D3-84; see below).

**The proof sheet** is `work/boards/phase-3/round-0/palettes/20261111_Palette-Proofs.html`, with 43 PNG captures beside it and every measured value in `20261111_Palette-Proofs-Measures.json`. It shows each palette on Newsprint, Charcoal and White (the paper a printed report uses), the Prussian measurement behind keeping charts off Prussian, contrast of every fill on its ground and every label on its fill, grayscale, and protanopia, deuteranopia and tritanopia simulations. It adds the grade line code at 1x and 2x in five treatments, the red-on-red specimen in six views, and both forms past four groups, all on real data with source lines. 41 of 41 scripted checks pass. The simulation method is Machado, Oliveira and Fernandes (2009) at severity 1.0 in linear RGB, the Phase 2 palette lab's method; the captures apply the same matrices through SVG filters and match the script within 0.001 in OKLab.

**The rounds 1 and 2 data plan is signed off with five changes**, written at the plan's end under "Data lead sign-off" and listed under Routine calls below. Rule 01.9 holds: a script recount gives the plan's 64 examples, with the largest domain at 12 of 64 against a limit of 16.

Nothing blocks. The new colors wait for Dustin on board 1.

## Routine calls

D3-xxx | Diverging pair B on Charcoal takes two new tints, Prussian 56 and 29 percent toward Newsprint, with the Verdigris half reusing the sequential Charcoal steps 3 and 4 and the midpoint reusing the Charcoal band tint | Each Prussian step then matches its Verdigris partner in lightness (0.633 with 0.634, 0.478 with 0.476), so neither side outweighs the other, and only two values are new
D3-xxx | Labels on the Charcoal diverging steps: Charcoal on the two ends, Newsprint on the three middle steps | Each passes 4.5 to 1, at 4.61 to 1 the least
D3-xxx | The categorical set on Charcoal is Newsprint, Prussian 62 percent toward Newsprint (the existing `prussianN62`), Verdigris and Stone, in the Newsprint order | Prussian itself measures 1.41 to 1 on Charcoal; this set keeps every pair outside Verdigris and Stone at least 0.119 apart in lightness with no new value
D3-xxx | The Stone group of the categorical set always carries the 45 degree hatch at the existing hatch tokens, with its label beside it or on a halo of the ground | Verdigris and Stone sit 0.050 apart in lightness and 0.051 apart under deuteranopia (D2-95); the hatch also keeps the set's order in gray
D3-xxx | Categorical lines end on a marker per group (circle, square, triangle, diamond) and never take a dash | A dash reads as an evidence grade (Rule 10.10) or a projection; shapes and labels survive gray and one-ink print
D3-xxx | Small multiples draw the other groups as 1 px ghosts under a new role, `oa.chart.color.ghost`, pointing at `stoneN55` on Newsprint and `stoneC40` on Charcoal; one group in ink against gray uses the existing context role | DR-234 allows no new hue, and the ghosts repeat lines drawn in full in their own panels
D3-xxx | The grade line code becomes `oa.chart.grade` stroke styles per 1 px of width with Rule 10.10's ratios (4 and 2; 4, 1.5, 1 and 1.5; round dots 2.5 apart), the 7 px record square, the hollow line's rails and a 28-width shortest run | Rule 10.10 and the atlas frame memo already set these; tokens give the kit and chapters 13 and 15 one source. V7's renderer arrays (9 and 4; 9, 3, 2 and 3; 2 and 4) are the same textures at its own weight
D3-xxx | A red target never draws at 2 px; it takes the 4 px or heavier target weight | At 2 px the Charcoal case swallows the red of a dotted line, as the 2x proof shows
D3-xxx | Red on red resolves by Rule 05.3's order with Rule 11.16's yield: whenever an error or an ask is in the view, the chart's point yields to the subject ink and keeps its bold label and its place | No token is needed, and nothing the point says is lost; in gray the red bar and the Stone bars print almost alike (0.371 and 0.386 in Chromium's filter), so the keyline, label and title carry it there
D3-xxx | No chart tokens on White or Prussian: a printed report prints the Newsprint values on the paper, and a chart in a Prussian panel sits on its own Newsprint or Charcoal plate | Every Newsprint label holds on White; on Prussian the four categorical inks measure 1.00 to 2.80 to 1, and red never sits there (Rule 05.3)
D3-xxx | No Prussian sequential set | No chart in S01 to S16 or in rounds 1 and 2's plan needs a second measure in sequence (proposal section 1.6 adds it only on need)
D3-xxx | The proofs draw real data: 2024 reported turnout by state from the Census Bureau, and payrolls by sector from the Bureau of Labor Statistics via FRED, January 2022 to September 2026, the window S13 and S14 use | Real data tests the palettes as charts will use them, and one window across the jobs proofs follows H09
D3-xxx | The suggested release name is `6.0.0-gate3.1` | Rule 26.8 raises the number after the hyphen before 6.0.0; the engineer names it
D3-xxx | Data plan signed off with five changes: row 13's window from January 2022 rather than September 2024; rows 26, 47 and 48 past four groups under DR-234; rows 14 and 49 in one neutral party ink; row 77 names both provisions of H.R. 7008; rows 6 and 23 carry the October 2025 gap | Rule 01.9 and DR-229 hold as planned; the changes follow H09, DR-124, DR-234, DR-48, DR-58 and DR-98

## Requests

1. **Engineer: add the proposal's tokens as one pre-release.** Every token in `20261111_Palette-Proposal.json` under `tokens`, the five description changes and the six widened tints under `description_changes` (only `prussianN62` gains a surface, Charcoal, at 6.18 to 1). I suggest `6.0.0-gate3.1`; you name it under Rule 26.8. Every new description already ends "Proposed until board 1."
2. **Engineer: kit roles.** `div-1` to `div-5` now have Charcoal tokens. `cat-4` takes the hatch and every `cat-N` its marker (the `pattern` and `marker` fields in the proposal). The kit needs a `ghost` role and the `grade-*` stroke styles for any chart or diagram that draws a connection.
3. **Engineer: the key lightness test (proposal section 7, C3a).** Chromium's `grayscale(1)` filter weights the encoded color values; my captures match that formula exactly. It ranks Pillar Red darker than WCAG luminance or OKLab does, so a test on captures and a test on token values can disagree. I suggest testing token values in OKLab lightness: at least 0.10 between any two groups a key separates by fill alone, with a pattern or direct label exempting a pair, and at least 0.08 between neighbors on an ordered scale. Every palette on the sheet passes both (ordered neighbors 0.089 at the least, the sequential Charcoal steps 1 and 2).
4. **Editor: Rule 13.4's plates** draw the line code from the proposed `oa.chart.grade` values (Rule 10.10's ratios), with the 7 px record square before "Documented" and a red target at 4 px or heavier.
5. **Research lead: the five changes** at the end of `20261111_Rounds-1-2-Data-Plan.md`, before fetching the datasets they touch (rows 13, 26, 47 and 48 mainly).
6. **Main session:** the sheet and its captures are ready for board 1. The captures to show first are `20261111_Palette-Proofs-Diverging-1440.png` (the new colors), `-Categorical-1440.png`, `-Past-Four-Groups-1440.png`, `-Red-On-Red-1440.png` and `-Line-Code-1440-2x.png`.

## Tested

- Every ratio in the proposal and on the sheet, computed by `work/boards/phase-3/round-0/palettes/build_palette_proofs.py` from `tokens.json` release 6.0.0-gate2.9 with the WCAG 2.2 formula, and both new colors mixed in OKLab by the Phase 1 color module.
- 41 scripted checks, all passing: every label 4.5 to 1 or more on its fill, on every palette and ground; every categorical ink 3 to 1 or more on Newsprint, White and Charcoal; only the Verdigris and Stone pair under 0.10 in lightness, and it carries the hatch; gray order holds on every ordered scale and ground; neighbors 0.05 or more apart under all three simulations; the Charcoal diverging ends and near steps matched within 0.01; both new colors are palette colors mixed toward Newsprint; a 28-width run holds three dash-dot periods at 2, 3 and 6 px.
- The captures, sampled at 459 points: in the normal captures the 51 token swatches equal their tokens' hex values and the 204 simulation strips equal the script's values; in the grayscale captures the token swatches equal the Rec. 709 weights on the encoded values; in the three simulation captures they match the script's simulation within 0.001 in OKLab.
- The fonts: the capture script stops unless Inter and Inter Tight report loaded.
- The sheet at 390 px: no horizontal page scroll (0 px); wide figures scroll inside their own frames.
- The page carries no em dash and no U+2011, and every `var(--oa-...)` it uses is defined in its inline tokens. A scan of its words found none of chapter 02's flagged words.
- The data: the 15 sectors sum to total nonfarm in September 2026 within 2 thousand jobs; the turnout file gives 51 rows for 2024; the source lines follow the sidecars' and H04's order.
- My own read of every section at 1440 px, the line code at 2x, and the grayscale, deuteranopia and tritanopia captures of the diverging, categorical and red-on-red sections. The 2x read caught dots clipped at a line's ends; the build now insets round-capped runs by half a line width.
- The data plan's tables, recounted by script: 82 forms by tier, 26 and 22 new data-bearing specimens, 64 examples with S01 to S16, and the domain totals the plan prints.

## Not tested

- Any reader with a color-vision deficiency. The simulations model full dichromacy only (severity 1.0), with no anomalous trichromacy, and Machado's tritanopia matrix is an approximation; I did not cross-check with the Brettel or Viénot methods.
- Print. The black-only row is a luminance-matched screen estimate that ignores dot gain and paper; no proof was printed.
- The tokens in the build: the token rule test, the CSS and JSON parity test and the Gate 2 contrast table were not run on the proposal, since the engineer adds the tokens.
- The kit drawing with these tokens.
- axe-core, the guide check, forced colors, print styles and 200 percent zoom on the proof sheet, which is a board page outside the guide.
- A screen reader on the sheet.
- Whether OPM's files reach back to January 2022 for row 13; the research lead checks when fetching.
- Rendered contrast of every mark: the captures confirm the 51 probed token swatches, and the rest rely on the page drawing the same custom properties.

## Change log

Created:
- `work/handoffs/phase-3/20261111_Palette-Proposal.json`
- `work/handoffs/phase-3/20261111_Round-0-Palette-Notes.md` (this file)
- `work/boards/phase-3/round-0/palettes/build_palette_proofs.py` and `capture_palette_proofs.js`
- `work/boards/phase-3/round-0/palettes/20261111_Palette-Proofs.html`, `20261111_Palette-Proofs-Measures.json` and `20261111_Palette-Proofs-Capture-Log.json`
- 43 PNG captures in `work/boards/phase-3/round-0/palettes/`: `20261111_Palette-Proofs-<Section>-1440.png` and its `-Grayscale`, `-Protanopia`, `-Deuteranopia` and `-Tritanopia` versions for Sequential, Diverging, Categorical, Past-Four-Groups, Magnitude, Line-Code, Red-On-Red and Prussian; `-Line-Code-1440-2x.png`; `-Opening-1440.png`; `-Page-390.png`

Modified:
- `work/handoffs/phase-3/20261111_Rounds-1-2-Data-Plan.md`: the "Data lead sign-off" section appended at its end, as the brief asks; nothing above it changed.

Scratch, outside the repository: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/31ab6fca-308a-5402-b22c-b6bfd31a97ee/scratchpad/phase-3/round-0/palettes/` holds the exploration scripts and preview slices.

## Fix pass

From `work/handoffs/phase-3/20261111_Round-0-Fix-Brief-Part-1.md`. Every fix is made in `work/boards/phase-3/round-0/palettes/build_palette_proofs.py`, which rewrites the proposal, the sheet and its measures; the captures and their check were run again after the last change.

### D3-84, the line code from one source

The build script now reads the line code from the atlas build itself, `work/boards/phase-2/atlas-editorial/01-times-explainer/build_system.py`. It runs that file's `pattern()` and reads `wire_marks()`, `fitted()`, `ARROW`, `grade_glyph()`, `evidence_key()` and the shared grade table from the source text, and stops if `wire_marks` changes shape. The proposal records every value and its line under the new key `line_code_source`, and the sheet prints them in a table, "Every value, and where it comes from".

| Item | Value | Source |
|---|---|---|
| Patterns, per 1 px of line width | Plausible 4 and 2, butt caps; Contested 4, 1.5, 1 and 1.5, butt caps; Hypothesis 0 and 2.5, round caps; Documented and Well supported solid | `pattern()`, line 446 |
| Fitting | Stretched so each line starts and ends on ink | `fitted()`, line 456 |
| Line widths | 2, 3 and 6 px, no others | `ARROW`, line 436 |
| Hollow line | Two 1 px rails at every width, one line width of ground between them | `wire_marks()`, line 570 |
| Dotted line before an arrowhead | Stops 1.5 line widths short (new token `oa.chart.grade.headClearance`) | `wire_marks()`, line 570 |
| Shortest textured run | 20 line widths, key samples included: 40 px at 2 px | **Not in the build**; set here |
| Record square | 7 px, inline before the word Documented | **Not in the build**; set here |
| Hypothesis gloss | "not yet tested" | Rule 13.3's table; the build's shared table says "untested" |

Logged, where the build defines no value:
- **Shortest run.** The build has no shortest-line constant. Its keys draw 32 and 36 px samples on a 2 px line, which squeeze a dash-dot sample by up to a fifth. 20 widths holds two full dash-dot periods and the closing dash at every width, which is Rule 13.4's "pattern twice". It replaces both the frame memo's 28 widths, which the build never coded, and Rule 13.4's 48 px.
- **Record square.** The build draws none. Gate 1, M1 added it, and the frame memo and Rule 13.4 both give 7 px.
- **Withdrawn:** `oa.chart.grade.conceptual.railSelected` (2 px on the 6 px route). The build draws 1 px rails at every width.

Sent by message to the engineer (`ab61c63fec660d199`) and the editor (`aab950e18c7699aa7`) at about 23:00 UTC, with the categorical changes below for the engineer.

### What each review item became

| Codes | Fix | Where |
|---|---|---|
| CD M2, brand M3, statistics S8 | D3-84 above: one set of numbers, read from the atlas build, with the shortest run at 20 widths, the hollow line's 1 px rails and the gloss "not yet tested"; the sheet's line code section prints the same values and draws 1 px rails at 6 px | Proposal `tokens` and `line_code_source`; sheet section 06 |
| brand P3 | The Hypothesis gloss reads "not yet tested" in the tokens, the proposal and the sheet | `GLOSS` in the build script |
| CD M5, brand P1 | The categorical card draws the same four sectors in both charts, so each ink names one group in the figure | `cat_stack()` |
| CD M5, brand P2 | Every bar segment is named on the bar: values inside where they fit, names on leaders laid out so no leader crosses a name, and the narrow last segment named at the bar's end. The key above the bar is gone | `cat_stack()` |
| brand P2 | The categorical order becomes Charcoal, Verdigris, Prussian, Stone, so neither close pair ever touches in a stack. Charcoal and Prussian print at 99 and 97 percent black in one-ink print, and Verdigris and Stone sit 0.05 apart in lightness. Two new scripted checks hold it: stack neighbors stand 0.10 apart in lightness, or 10 points of black, or the second is hatched | `CAT`, `checks()` |
| CD S9 | Group 4's label token takes its placement in its name: `oa.chart.color.categorical.labelBeside.group4`, set beside the hatch or on a halo, never on the fill. I asked the engineer to have the kit refuse a label on `cat-4`'s fill | `cat_label_path()` |
| CD S8, brand P4 | At 390 px the sheet now shows the phone form the kit would use: the categorical charts at 320 px with names that wrap, small multiples in two columns, and ranked bars with each name above its bar for one-in-ink and all eight red-on-red views (DR-64). The desktop drawings stay at 1440 px | `dual()`, `ranked_bars_phone()`, phone arguments |
| brand P5 | Views 7 and 8 proof the variant: the other bars in the light fill, which prints each value beside its bar. In gray the red bar then prints darker than its neighbors (Chromium's filter: 0.371 against 0.635, where view 1 gives 0.371 against 0.386). Both are on the sheet and in its grayscale capture for the creative director to weigh; I recommend the light fill for bars wherever a red point stands among them, since its values print | `red_views()` |
| CD S10 | The font link asks for Inter Tight 800 only. The one-in-ink and red-on-red titles now say the September figure is preliminary ("a preliminary figure", as H08's example does) | head; `LEAD_TITLE` |
| CD S10, the period | **Not changed, with a reason.** The cards' titles are findings, and a finding title is a full sentence with its period (Rule 13.1, the engineer's spec contract). The other headings on the sheet are proof labels, and labels take no period (chapter 02's scope note). The two kinds now differ on sight: a finding carries the evidence chip and its grade line | |
| statistics S18 | The tile map's national figure was drawn at the key; it now reads "United States, margin 0.5", and a note under the map gives the national figure, the state margins (1.6 to 5.6 points) and why a state near a step's edge may belong in the next step. The script reads the national row from the data file once the engineer adds it (research lead's ENG-7), and from the sidecar until then | `tile_map()`, figure note |
| D3-83 on the sheet | Every finding card now carries the evidence chip with "Documented: a Bureau of Labor Statistics survey of employers, as copied by FRED" | `JOBS_GRADE` |

### D3-83 sign-off: signed off

The rule is right, and it needs no change from me: an outside figure takes its grade word from H08's table; a count or survey tabulation is a finding with the publisher's margin; a figure resting on a model's assumptions is an estimate with its range or method. For the makers and the editor, this is how rounds 1 and 2's plan rows read under it:

- **Documented, a record, a finding:** rows 2, 13, 14, 22, 25, 26, 27, 33, 39, 44, 48, 49, 54, 77, 78 and 80 (statutes, roll calls, filings, Treasury, OPM, judicial and House records), and the administrative counts in rows 4, 12, 19 and 21.
- **Documented, a survey tabulation, a finding with its margin:** rows 3, 6, 8, 23, 43, 63, 64, 65, 70 and 71, and the payroll series of S13, S14 and rows 18, 20 and 35. The research lead confirmed the Bureau's interval for total nonfarm monthly change as about plus or minus 122,000 at 90 percent.
- **An estimate, with its range or method:** rows 56 and 57 (small-area models), 58 (population estimates), 73 (projections), and any with-and-without figure, such as a benefit's effect on poverty.
- **A finding, with its method in the note:** row 17's repeat-sales price index and row 47's national health accounts, which compile records and surveys with no projection.
- **Illustration:** row 28. Atlas rows take V7's own grades through Rules 13.2 and 13.3.

### D3-88 sign-off: signed off

`census-acs-rent-and-income-by-state` now carries the Census Bureau's own measure, B25071 (median gross rent as a percentage of renter household income), with its margin. I checked the file by script: 52 rows, the United States at 30.9 percent with a margin of 0.1, and states from 23.8 (North Dakota) to 35.5 (Florida), every row with its margin, which matches the statistics review's figures. The scatter draws rent (B25064) against renter households' income (B25119) under the Association label, and names states by B25071 only past the margin. The domain and states are unchanged, so Rule 01.9 holds. One note for the round 2 maker: B25071 and B25064 count renters paying cash rent, and B25119 counts all renter households. The sidecar's universe line says so, and the chart's note should too.

### Fix pass routine calls

D3-xxx | The line code's numbers are read by script from the atlas build, with the shortest run set at 20 line widths and the record square at 7 px where the build defines none | D3-84; 20 widths holds two dash-dot periods and the closing dash, and 7 px is Gate 1 M1's size as the frame memo and Rule 13.4 give it
D3-xxx | `oa.chart.grade.conceptual.railSelected` is withdrawn and `oa.chart.grade.headClearance` (1.5 line widths) is added | The build draws 1 px rails at every width and stops a dotted line 1.5 widths short of its head
D3-xxx | The categorical order becomes Charcoal, Verdigris, Prussian, Stone | Charcoal and Prussian print 2 points of black apart in one-ink print, and Verdigris and Stone 0.05 apart in lightness; this order keeps both pairs from touching in a stack
D3-xxx | Group 4's label token is renamed `labelBeside` | Its label sits beside the hatch or on a halo; Charcoal on Stone measures 3.10 to 1
D3-xxx | The proof sheet shows the phone form at 390 px and the desktop drawing at 1440 px | Board 1 shows both widths, and DR-64 lets a phone drawing change form when it carries the same data and finding
D3-xxx | Recommended for the creative director: where a red point stands among bars, the other bars take the light fill | The red point then holds in gray print, and the light fill already prints its values

### Fix pass requests

1. **Engineer (sent):** the D3-84 token values, `railSelected` withdrawn, `headClearance` added, `minRun` from 28 to 20, the gloss; the categorical order (groups 2 and 3 swap values) and the `labelBeside.group4` rename; a kit check that refuses a label on `cat-4`'s fill.
2. **Editor (sent):** Rule 13.4's numbers and the 40 px key samples at 2 px; a red target at 4 px or heavier.
3. **Engineer:** the research lead's ENG-7, the national row in the turnout file. Done by the engineer; the proof sheet now reads its data from `work/build/data/` (contract C1), takes the national figure from that row, and prints the sidecars' own source lines (the turnout file's 2024 line, and the line S13 prints for the payroll series).
4. **Engineer (done, reported back):** the D3-84 values and the categorical changes are in release 6.0.0-gate3.1 with every token test passing; the kit refuses a label on `cat-4`'s fill without a halo.

### Fix pass tested

- The atlas build read by script: `pattern()` run for each texture, and the hollow line, head clearance, widths and key lengths read from the source with their lines; the script stops if `wire_marks` changes shape.
- 46 of 46 scripted checks pass, including the two new stack-order checks for the categorical set on Newsprint, White and Charcoal.
- The captures again: 43 PNGs; 459 samples; token swatches equal their tokens; grayscale equals the luma formula; the three simulations match the script within 0.001 in OKLab.
- At 390 px: no horizontal page scroll (0 px), and screenshots of the categorical card, the small multiples, the one-in-ink card and a red-on-red view show the phone forms with every name on screen.
- At 1440 px: the categorical card with both charts and the bar's callouts, the line code values table, and views 7 and 8 in color and in the grayscale capture.
- `census-acs-rent-and-income-by-state` by script for D3-88.
- A scan of the sheet's words: no em dash, no U+2011, none of chapter 02's flagged words; "untested" appears only in the source log.

### Fix pass not tested

- The engineer's and the editor's changes from the messages; I cannot see them yet.
- Chapter 13's plates against the new numbers; the editor redraws them.
- The guide build (`guide_build.py --strict`). The brief asks for it after a plate changes, and I changed no guide plate or chapter file.
- The light fill's effect in print; only the screen's grayscale filter was measured.
- The ACS universes behind rows 63 and 64, beyond the sidecar's own words.

## Fix pass 2

From the coordinator's message on November 12, 2026: the brand reviewer's S1 (a solid lead-in on patterned lines) and the access reviewer's S10 (scroll frames a keyboard cannot reach). No chart spec was rebuilt.

### Brand S1: a solid lead-in, 28 px

**Yes, there is one, and it is 28 px.** A patterned line (Plausible, Contested, Hypothesis) that carries delay ticks runs solid from its tail for 28 px. That holds at every width and for one, two or three ticks. After the lead-in the line leaves its pattern's own gap and starts the fitted pattern on ink: 2 widths for dashed, 1.5 for dash-dot, and a dot center 2.5 widths after the lead-in for dotted. Solid grades need nothing. Lines without ticks, such as key samples, take none. The shortest textured run, 20 line widths, counts after the lead-in. New token: `oa.chart.grade.leadIn`, 28 px.

**Why.** The atlas build's `tick_marks()` (line 560) places ticks 12 px from the tail, 5 px apart and 2 px wide at every line width, and `wire_marks()` starts the pattern at the tail with no lead-in. So a tick can land in a gap and read as a letter, as the reviewer saw on the opener. The build script now reads those three numbers by script, and the lead-in follows from them. The third tick ends at 23 px, and 5 px of clear line, the ticks' own spacing, brings it to 28. One length for every grade, width and tick count means a builder never counts ticks. The proposal logs it under `line_code_source`, and the sheet adds the row "Solid lead-in under the ticks" to its values table. A plate in section 06, "Delay ticks on a patterned line, at twice size", shows the build's drawing beside the lead-in.

Sent to the editor (`aab950e18c7699aa7`) and the engineer (`ab61c63fec660d199`) by message. The editor reported back on November 12: chapter 13 draws the lead-in on the opener's Connection L02 and on Rule 13.11's L02 only, since those are the patterned lines with ticks. The editor's generator reads the 28 px from the token and checks it against the tick constants, and Rule 13.4's specifications state it and cite the token. The strict build has 0 warnings. One carried item: the Phase 2 atlas build's `wire_marks` still draws no lead-in, so chapter 13's generator splits the line itself. The atlas build stays a Phase 2 record. If the atlas site or chapter 15 takes `wire_marks` forward, it should take the lead-in with it. The engineer reported the same day that `oa.chart.grade.leadIn` (28 px) is in pre-release 6.0.0-gate3.1 with its change note, 545 tokens in all, every token test passing. The kit does not use it yet, since no kit chart draws a connection with delay ticks.

### Access S10: scroll frames a keyboard can reach

`focusable_frames()` in `build_palette_proofs.py` gives each of the sheet's 40 sideways frames `tabindex="0"`, `role="region"` and a name. The name joins the section heading and the nearest heading or figure title, such as "Sequential Verdigris: On Newsprint, scrolls sideways", and the measured-value tables name their palettes. The page script removes all three from a frame that does not scroll at the reader's width, and checks again on resize and when a "Every measured value" table opens. That way, no empty tab stop is added. With scripts off every frame stays reachable. A focused frame shows the 3 px focus ring. The intro moved inside `<main>` so all content sits in a landmark; the capture script now clips the opening at the first section.

### Fix pass 2 routine calls

D3-xxx | Patterned lines with delay ticks start with a 28 px solid lead-in, then their pattern's own gap; `oa.chart.grade.leadIn` = 28 px | The atlas build places ticks at 12, 17 and 22 px but draws no lead-in, so a tick can sit in a gap; 28 px covers three ticks plus 5 px clear at every width, one number for every case
D3-xxx | A scroll frame on the proof sheet is a named, focusable region only while it scrolls | WCAG 2.1.1 asks that a keyboard reach any scrolling content, and frames that fit need no tab stop

### Fix pass 2 tested

- The tick geometry read by script from `tick_marks()` and the build's `.wire .tk` style; the build script asserts the lead-in comes to 28.
- The lead-in plate at 1440 px: in the build's drawing a tick falls in a gap on all three patterns, and with the lead-in all three ticks sit on solid line.
- axe-core 4.10 (WCAG 2.0 to 2.2 A and AA, plus best practice) on the sheet at 1440 and 390 px, with the measured-value tables closed and open: 0 violations. The 7 frames that scroll at 1440 px and the 26 at 390 px each have a tab stop, the region role and a name.
- A keyboard walk at 390 px: Tab reaches the scrolling frames, and in each one reached, two presses of the right arrow scroll it.
- 46 of 46 checks; 43 captures again, with 0 px of page overflow at 390 px; 459 samples matching tokens and simulations within 0.001.

### Fix pass 2 not tested

- A screen reader on the sheet; the names and roles were read from the DOM and axe only.
- The lead-in in the kit and in chapter 13's plates, which the engineer and the editor draw.

## Second pass

DR-191's second pass: the editor's "Fix pass read" in `work/handoffs/phase-3/20261111_Round-0-Editor-Notes.md` found seven faults in the proof sheet's words, P1 to P7. Each fix is in `build_palette_proofs.py`, and the sheet, its measures and its 43 captures were rebuilt from it.

| # | Fault | Fix |
|---|---|---|
| P1 | Straight apostrophes in the new text | A new function, `curly()`, sets every apostrophe a reader meets as U+2019. It covers the words on the page and the names and alt texts screen readers speak; style, script and code stay as written. The build now stops if a straight apostrophe is left in the words, and none is |
| P2 | "Closest pair, Group 2 and 4" | "Closest pair, Groups 2 and 4" |
| P3 | "margin 0.5 points" | "margin of error 0.5 points at 90 percent confidence" in the map's note. The label beside the national tile reads "United States, margin of error 0.5 points" |
| P4 | Two sentences on one frame ("Swatches marked…") | "Swatches marked In tokens come from release 6.0.0-gate3.1; those marked Proposed come from the palette proposal and wait for board 1." |
| P5 | "the 2 new colors" | "the two new colors", through a small `nw()` helper for numbers under ten in prose (H06) |
| P6 | "V7's renderer's dash arrays" | "the dash arrays in V7's drawing code" |
| P7 | The shortest-run sentence | "A run shorter than 20 line widths (40 px on a 2 px line), counted after any lead-in, prints its grade in words beside it, and a sample in a key runs at least that long." |

### Second pass tested

- Each new wording found in the rebuilt page by script. No straight apostrophe is left in its words or in any `aria-label`, `data-label`, `alt` or `title`, and no em dash.
- 46 of 46 checks. 43 captures with 0 px of page overflow at 390 px. 459 samples match tokens and simulations within 0.001.
- axe-core at 1440 and 390 px, with the measured-value tables closed and open: 0 violations. Every scrolling frame keeps its tab stop, role and name.
- The national tile's three-line label at 1440 px, clear of the map.

### Second pass not tested

- A screen reader on the curly apostrophes in names; axe and the DOM only.

## R3, the creative director's rescore

The creative director's rescore (`work/handoffs/phase-3/20261111_CD-Review-Of-Round-0.md`, "Rescore") marks the palette proofs ready and adopts the variant I put to it: **R3, the light fill for the other bars wherever one bar is named, in red or in ink.** It is applied at the source, `build_palette_proofs.py`.

- **Scope, measured.** On Newsprint the other bars take the light fill (`oa.chart.color.lightFill`, stoneN55). In Chromium's grayscale filter it prints at 0.635, against 0.371 for Pillar Red and 0.071 for Charcoal. On Charcoal the light fill is Stone, which prints at 0.386, as gray as Pillar Red, so there the other bars keep the context ink (stoneN35, 0.540). A new function, `other_bars()`, picks the fill by ground.
- **The proposal.** A new rule in `rules_with_the_palettes`, "Named bar (R3)", and a description change for `oa.chart.color.lightFill` with the decision recorded. No value, name or new token. The engineer has it by message.
- **The sheet.** Views 1 to 6 and the phone form of the one-in-ink chart draw the other bars by `other_bars()`. View 7 keeps the first proof's Stone bars as a labeled failure in gray print, with both gray levels printed. The section's side note states the rule. Four new checks hold it on both grounds, in red and in ink: the named bar stands at least 0.10 apart in gray from the other bars.

R3 routine call: D3-xxx | Where a chart names one bar, the other bars take the light fill on Newsprint and keep the context ink on Charcoal | The creative director's R3; on Charcoal the light fill is Stone, which prints as gray as Pillar Red (0.386 against 0.371), so the context ink holds the point there (0.540)

R3 tested: 50 of 50 checks; 43 captures again with 0 px of page overflow at 390 px; 459 samples matching tokens and simulations within 0.001; axe-core at 1440 and 390 px, tables closed and open, 0 violations; the red-on-red grayscale capture read by me, where the red bar now prints darker than its neighbors on Newsprint. R3 not tested: print, and the kit's own bar charts, which the engineer draws.

The engineer added the light fill's new description to pre-release 6.0.0-gate3.1. No value or name changed, the token tests pass and the token table is regenerated. The engineer left the "(R3)" marker out of the description, since descriptions are reader words, and recorded the decision in the change note instead. I removed the marker from the proposal's wording to match; its `decided` field keeps the record. Carried, not blocking: the kit draws R3's fills only once a spec names one bar, and no round 0 spec does.
