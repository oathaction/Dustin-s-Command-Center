# Identity refinement notes

Phase 1, October 21, 2026. oa-design-director, for the Gate 1 report. Proposals only: no V5 master changed.

Board: `work/boards/20261021_Identity-Refinement-Board.html`. Files: `work/boards/phase-1/identity/`. Numbers: `20261021_Identity-Refinement-Measurements.json` and `20261021_Ampersand-Similarity.json` beside this note. x is one wordmark cap height, 100 units.

## What changed, and why

1. **Re-exported outlines (defect fix).** `#amp`, `#tl-1`, `#tl-2a`, `#tl-2b`, `#url-1` and `#stacked` get viewBoxes that hold their full ink. Outlines and origins are unchanged; the board lists the new L4, L5, L6 and hinge placements.
2. **Hinge gaps (defect fix).** 2a applies V5's 0.10x nearest-ink rule; the right side then holds 1.24 times the left's white. 2b, recommended, sets equal white area on both sides (rows counted to 0.15x past the nearest point), no ink closer than 0.07x. The area model is a design judgment. The ampersand moves 1.42 units toward ACTION; both areas measure 0.205x; the width holds.
3. **Wordmark masters (option, recommended).** Led by ampersand B; the A versions are item 4's fallback. Display master: 2b plus I to O and O to N opened 2.4 units, T joins 1.4. 24 px master: 22 px cap, 5 px stems, 4 px bars on whole pixels. 16 px master: 14 px cap, 3 px stems and bars, T arms 4 units shorter. At 16 px, T to H and T to I open from 0.73 and 0.62 to 1.00. At 16 and 24 px the ampersand fills the box height (1.14x and 1.09x cap), an optical-size change to V5's rule.
4. **Ampersand A (option, fallback).** Display tune: an elliptical-pen embolden (hairlines 70 to 85 font units, contrast 1.9 to about 1.7), overshoot set to the O's 1.34 units. A 16 px master on the pixel grid: 2 px hairlines, 3 px stem, 3 px upper counter. Red median contrast at 16 px rises to the nominal value on every surface (Newsprint 2.68 to 2.96).
5. **Ampersand B (option, recommended direction).** Drawn as one self-crossing pen path, redrawn as cubic contours, weighted and refitted (41 nodes). Bowl stem 0.85 of the wordmark stem, hairlines 13.7 to 14.9 units, a beak serif toward the loop, a tail with its foot on the baseline, a near-square crossing. Silhouette overlap 0.77 with Lora Bold, 0.48 to 0.61 with four other serif ampersands on this machine. A 16 px master and a 0.85 narrow version. Next step in Phase 2, stated on the board and not drawn: contrast toward 1.7 to 1 and the crossing on the hinge diagram's center line.
6. **Condensed exploration (option, Dustin's call).** Drawn from Inter Tight 800's own capitals: narrowed to 0.74 (the A to 0.81), stems restored to 22 units, bars thinned 2.2 units, cap band restored. Two widths by ink height: 7.5 to 1 and 6 to 1. The 16 px test chose 7.5 to 1: its A counter stays 0.77 open, the 6 to 1 closes to 0.23. At the same width it gains 1.26x the cap height (6 to 1 would give 1.56x). Inter Tight stays the headline face. Base: Inter Tight, Copyright 2022 The Inter Project Authors, SIL OFL 1.1; no OFL condensed family used.
7. **Hinge diagram V2 (option, recommended).** From Dustin's mockups: the ampersand at 1.25x cap in a circle of 2.2x cap, on a line with four nodes, and two solid hairline arcs running clockwise, each with one open arrowhead; UNDERSTAND and IMPACT below the words. The first draft's dotted arcs are withdrawn, since V7 gives dotted and dashed lines to evidence grades; the board shows V5, the draft and V2 side by side. The display master holds 13 px labels from 526 px wide (lines 1.27 px, arcs 1.02 px there); the compact master drops the labels and holds 1 px down to 241 px. Files: `07-hinge/20261021_Hinge-Display-Master_V2.svg` and `20261021_Hinge-Compact-Master_V2.svg`; the first-draft files stay.
8. **Lockmark small masters (defect fix).** 16 px: node centers 2.5, 7.5, 12.5 px, 3 px nodes, 5 px lever, 1 px links on whole pixel rows. 24 px: centers 3.5, 11.5, 19.5 px, 5 px nodes, 7 px lever. Thresholds: 16 px master to 23 px, 24 px master to 47 px, V5 master from 48 px. Solid ink share at 24 px rises from 0.05 to 0.60.
9. **Minimum sizes (defect fix).** One rule: no mark draws its capitals under 14 px on screen and no lockup tagline under 13 px; each lockup names its replacement below its minimum. L1 16 px tall, L2 88 px, L3 200 px, L4 304 px, L5 384 px, L6 880 px, L7 250 px, L8 48 px and never a favicon. Favicons use the ampersand's 16 px master. The lockmark thresholds match item 8. Clear space surrounds the whole lockup.
10. **Red ampersand on Prussian (decision for Dustin).** Median contrast at 16 px: V5 red 2.27; A, red at display size only, 8.27 at 16 px and 3.19 from 48 px; B, Newsprint, 6.06; C, red with a Newsprint keyline, 4.15; D, White, 8.27 (13.28 at 96). The board states the red rule verbatim: "The wordmark's ampersand and the lockmark's lever are signature red and do not count. Each view (one screen, card, slide or printed page) then carries one working red, in this order of precedence: an error the reader must fix; the step a reader can take now; the one point the headline names, which in a systems figure is where a reform acts. A hinge headline's ampersand uses the view's working red. The hinge divider's ampersand is Charcoal. The Act handle is red only when the Act mark is itself the call to act, as on a social tile. Red never sits on Prussian." Under it A and C fall away. I recommend D, White, for identity marks on Prussian.

## Rubric scores

| Item | Craft | Clarity | Brand fidelity | Usefulness | Evidence honesty | Accessibility |
|---|---|---|---|---|---|---|
| 1 Re-export | 5 | 5 | 5 | 5 | 5 | 4 |
| 2 Hinge gaps (2b) | 4 | 4 | 5 | 4 | 5 | 4 |
| 3 Wordmark masters | 4 | 4 | 4 | 5 | 5 | 4 |
| 4 Ampersand A | 4 | 4 | 5 | 4 | 5 | 4 |
| 5 Ampersand B | 4 | 4 | 4 | 4 | 5 | 4 |
| 6 Condensed | 3 | 4 | 3 | 4 | 5 | 4 |
| 7 Hinge diagram V2 | 4 | 4 | 4 | 4 | 5 | 4 |
| 8 Lockmark | 5 | 4 | 4 | 5 | 5 | 4 |
| 9 Minimum sizes | 4 | 4 | 5 | 5 | 5 | 4 |
| 10 Prussian (D) | 4 | 4 | 4 | 4 | 5 | 5 |

Item 6 is under threshold: its letters want a drawing pass, its 16 px ampersand is scaled, and it changes the locked proportions.

## Craft checks

**Passed.** Silhouette at 16 px for items 1 to 5 and 7 to 9. Pixel fit for the 16 and 24 px wordmark, ampersand and lockmark masters. Consistent weights inside each master. Overshoot at 1.34 units in A and the display wordmark. One color on all four surfaces. Red follows the red rule. Hinge diagram lines reach 3:1 and use no dotted or dashed line. Taglines and labels at 13 px or more at their minimums.

**Failed or open.**
- Pillar Red on Newsprint stays at 2.96:1 at best; the 1 px Charcoal edge rule stays for informative use. WCAG exempts logotypes.
- Item 6 pixel fit: the narrowed ampersand at 16 and 24 px is scaled, so its edges blur.
- Item 6 similarity: heavy condensed capitals are common on campaign signs.
- Option B is a first drawing. It needs a refinement pass at 2x, a print proof and a check against commercial serif ampersands.

## Checked and not checked

**Checked.** Ink bounds from curves. Spacing from outlines. Every cell rendered in Chromium 141 on Linux at device scale 1, with overlays, red pixel contrast, solid share and joins measured from them. Silhouette overlap of B against Lora Bold, Caladea, Liberation Serif, FreeSerif and DejaVu Serif. The board at 1440 and 390 px after the review fixes: no horizontal page scroll, 2,045 images load, no skipped heading levels, no text under 13 px.

**Not checked.** Windows, macOS, high-density screens, Firefox and Safari (pixel fit holds for 1x Chromium on Linux). Print proofs. Commercial serif ampersands. Reader tests. Screen readers. A 16 px favicon tile.

## Open risks

- The larger ampersand at 16 and 24 px (item 3) and the larger lever at 16 and 24 px (item 8) reverse stated V5 measures. Each needs a named approval.
- L4, L5 and L6 minimums grow sharply under the 13 px tagline rule. Smaller lockups would mean redrawing their taglines larger relative to the wordmark.
- If Dustin approves B and the condensed width, Phase 2 draws a narrow B 16 px master and refines the condensed C, N and A first.
- The similarity check covers only fonts on this machine.

## How to rebuild

Run the `p1_*` scripts in `work/build/scripts/phase-1/` with `python3 -I`, ending with `p1_render.py` and `p1_board.py`.

## Change log

**Created.** The board; `20261021_Hinge-V2-Ready.md` beside this note; `work/boards/phase-1/identity/` (SVG proposals in eight item folders, 1,427 rendered PNGs in `png/`); the two JSON files above; this note; the `p1_*`, `oa_p1.py`, `oa_stroke.py` and `render_cells_p1.js` scripts in `work/build/scripts/phase-1/`.

**Modified.** None: `source/`, `work/extract/` and the V5 masters are untouched. `skia-pathops` and `shapely` were installed for boolean geometry.
