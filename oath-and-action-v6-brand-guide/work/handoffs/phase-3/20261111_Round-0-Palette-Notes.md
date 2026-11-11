# Round 0 palette notes: data palettes, proofs and the proposed chart tokens

Oath & Action Edition 06, Phase 3, round 0, November 11, 2026. Written by the data visualization and systems lead (`oa-dataviz-systems-lead`), with the design director's eye, for `work/handoffs/phase-3/20261111_Phase-3-Round-0-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

**The palette proposal is ready for the engineer:** `work/handoffs/phase-3/20261111_Palette-Proposal.json`. It holds 40 proposed tokens, each with its path under the token architecture, its value or alias, the surfaces it serves, its measured ratios and its reason, plus five description changes and six existing tints that take a second job. At 21:54 UTC I added the surfaces and ratios of those six tints to the file; no value changed.

Two colors are new, both Prussian mixed toward Newsprint in OKLab, so diverging pair B works on Charcoal in the dark theme: `oa.color.tint.prussianN56` (#828A9D, 5.42 to 1 on Charcoal) and `oa.color.tint.prussianN29` (#505C7D, 2.83 to 1, its value printed). Every other proposed token points at a value the release already holds:

- **Diverging on Charcoal** (10 tokens): the two new Prussian steps, the Charcoal band tint as the midpoint, and the sequential scale's Charcoal steps 3 and 4 as the Verdigris half. Each Prussian step matches its Verdigris partner in lightness within 0.002.
- **Categorical, four inks** (16 tokens, DR-234): Charcoal, Prussian, Verdigris and Stone on Newsprint; Newsprint, Prussian 62 percent toward Newsprint, Verdigris and Stone on Charcoal. The Stone group always carries the hatch, and every group carries a direct label and, on a line, its own end marker.
- **Ghost lines** for small multiples past four groups (2 tokens).
- **The grade line code** (10 tokens): Rule 10.10's patterns as stroke styles per 1 px of line width, the record square, the hollow line and the shortest textured run.

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

Work in progress, from `work/handoffs/phase-3/20261111_Round-0-Fix-Brief-Part-1.md`. D3-84's values are set in the palette proposal under `line_code_source` and were sent to the engineer and the editor at about 23:00 UTC; the categorical order and group 4's label path changed with them.
