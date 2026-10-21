# Identity refinement notes

Phase 1, October 21, 2026. oa-design-director, for the Gate 1 report. Proposals only: no V5 master changed.

Board: `work/boards/20261021_Identity-Refinement-Board.html`. Files: `work/boards/phase-1/identity/`. Numbers: `20261021_Identity-Refinement-Measurements.json` and `20261021_Ampersand-Similarity.json` beside this note. x is one wordmark cap height, 100 units.

## What changed, and why

1. **Re-exported outlines (defect fix).** Six symbols get viewBoxes that hold their full ink; outlines and origins are unchanged.
2. **Hinge gaps (defect fix).** 2a applies V5's 0.10x rule; the right then holds 1.24 times the left's white. 2b, recommended, sets equal white area on both sides (rows counted to 0.15x past the nearest point), no ink closer than 0.07x. The area model is a design judgment. The ampersand moves 1.42 units toward ACTION.
3. **Wordmark masters (option, recommended).** Led by ampersand B; the A versions are item 4's fallback. Display master: 2b plus I to O and O to N opened 2.4 units, T joins 1.4. 24 px master: 22 px cap, 5 px stems, 4 px bars on whole pixels. 16 px master: 14 px cap, 3 px stems and bars, T arms 4 units shorter. At 16 px, T to H and T to I open from 0.73 and 0.62 to 1.00. At 16 and 24 px the ampersand fills the box height (1.14x and 1.09x cap), an optical-size change to V5's rule.
4. **Ampersand A (option, fallback).** Display tune: hairlines 70 to 85 font units, contrast 1.9 to about 1.7, overshoot 1.34 units. A 16 px master on the pixel grid: 2 px hairlines, 3 px stem, 3 px upper counter. Red median contrast at 16 px rises to the nominal value on every surface (Newsprint 2.68 to 2.96).
5. **Ampersand B (option, recommended direction).** Drawn as one self-crossing pen path, redrawn as cubic contours, weighted and refitted (41 nodes). Bowl stem 0.85 of the wordmark stem, hairlines 13.7 to 14.9 units, a beak serif toward the loop, a tail with its foot on the baseline, a near-square crossing. Silhouette overlap 0.77 with Lora Bold, 0.48 to 0.61 with four other serif ampersands on this machine. A 16 px master and a 0.85 narrow version. Next step in Phase 2, stated on the board and not drawn: contrast toward 1.7 to 1 and the crossing on the hinge diagram's center line.
6. **Condensed exploration (option).** From Inter Tight 800's capitals, narrowed to 0.74 (the A 0.81), stems restored, bars thinned. The 16 px test chose 7.5 to 1 over 6 to 1 (A counter 0.77 against 0.23 open); it gains 1.26x the cap height at the same width. Inter Tight stays the headline face; no OFL condensed family used. Decision row: draw it, with today's width in force until Gate 2.
7. **Hinge diagram V2 (option, recommended).** From Dustin's mockups: the ampersand in a circle on a line with four nodes, two solid hairline arcs running clockwise with open arrowheads, UNDERSTAND and IMPACT below. Its ampersand is signature red, as an identity mark. The dotted first draft is withdrawn; the board shows V5, the draft and V2 side by side. Display master from 526 px wide, compact from 241 px. Files: `07-hinge/20261021_Hinge-Display-Master_V2.svg` and `20261021_Hinge-Compact-Master_V2.svg`.
8. **Lockmark small masters (defect fix).** 16 px: node centers 2.5, 7.5, 12.5 px, 3 px nodes, 5 px lever, 1 px links on whole pixel rows. 24 px: centers 3.5, 11.5, 19.5 px, 5 px nodes, 7 px lever. Thresholds: 16 px master to 23 px, 24 px master to 47 px, V5 master from 48 px. Solid ink share at 24 px rises from 0.05 to 0.60.
9. **Minimum sizes (defect fix).** One rule: no mark draws its capitals under 14 px on screen and no lockup tagline under 13 px; each lockup names its replacement below its minimum. L1 16 px tall, L2 88 px, L3 200 px, L4 304 px, L5 384 px, L6 880 px, L7 250 px, L8 48 px and never a favicon. Favicons use the ampersand's 16 px master. The lockmark thresholds match item 8. Clear space surrounds the whole lockup.
10. **Red ampersand on Prussian (decision for Dustin).** The board quotes Rule 05.3 word for word (decision D1-26): "The wordmark's ampersand and the lockmark's lever are signature red and do not count, and neither does the ampersand inside the hinge diagram, which is an identity mark. The hinge diagram never shares a view with the wordmark and never stands in for the hinge divider. Each view (one screen, card, slide or printed page) then carries one working red, in this order of precedence: an error the reader must fix; the step a reader can take now; the one point the headline names, which in a systems figure is where a reform acts. One job may take several marks, such as each target of one reform. A hinge headline's ampersand uses the view's working red. The hinge divider's ampersand takes its surface's ink: Charcoal on Newsprint and White, Newsprint on Charcoal, White on Prussian. The Act handle is red only when the Act mark is itself the call to act, as on a social tile. In the guide itself, specimens, labeled failure cases and palette swatches do not count. Red never sits on Prussian." Under its last sentence A and C fall away; they stay as grayscale specimens labeled "Ruled out by Rule 05.3". B and D remain; I recommend D. V5 today stays beside them at 16 and 96 px (median 2.27:1 and 3.19:1), the only red on Prussian on the board. Every other Prussian cell is one color, White.

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

**Corrected after the creative director's re-check.** Item 7 check 8 and item 9 check 7 now describe White renders on Prussian. Item 8 check 8 reads "Fail on Newsprint, logotype; the lever's size carries its meaning in one color."

**Failed or open.**
- Pillar Red on Newsprint stays at 2.96:1 at best. WCAG exempts logotypes.
- Item 6 pixel fit: the narrowed ampersand at 16 and 24 px is scaled, so its edges blur.
- Item 6 similarity: heavy condensed capitals are common on campaign signs.
- Option B is a first drawing: it needs a refinement pass, a print proof and a commercial similarity check.

## Checked and not checked

**Checked.** Ink bounds from curves. Spacing from outlines. Every cell rendered in Chromium 141 (Linux, 1x), with overlays and measures taken from the renders. Silhouette overlap of B against five serif fonts. A red-on-Prussian pixel audit at 1440 and 390 px, panels closed and open: 2,290 red pixels touch Prussian, all in the labeled V5 today cells; 0 without them. The board at 1440 and 390 px after the review fixes: no horizontal page scroll, 1,791 images load, no skipped heading levels, no text under 13 px.

**Not checked.** Other systems and browsers (pixel fit holds for 1x Chromium on Linux). Print proofs. Commercial serif ampersands. Reader tests. Screen readers.

## Open risks

- The larger ampersand at 16 and 24 px (item 3) and the larger lever at 16 and 24 px (item 8) reverse stated V5 measures. Each needs a named approval.
- L4, L5 and L6 minimums grow sharply under the 13 px tagline rule.
- If Dustin approves B and the condensed width, Phase 2 draws a narrow B 16 px master and refines the condensed C, N and A first.

## Change log

**Created.** The board; `20261021_Hinge-V2-Ready.md`; `work/boards/phase-1/identity/` (SVG proposals, rendered PNGs in `png/`, grayscale specimens in `png/p10-ruled-out/`); the two JSON files; this note; the `p1_*` scripts in `work/build/scripts/phase-1/` (run with `python3 -I`, ending with `p1_render.py` and `p1_board.py`).

**Modified in the fix passes.** The board (items 3, 7 to 10, decisions); `p1_board.py`, `p1_pairs.py`, `p1_render.py`, `p1_marks.py`; this note. **Removed.** Every rendered cell that put red on Prussian, except the two labeled V5 today cells.

**Modified.** None: `source/`, `work/extract/` and the V5 masters are untouched. `skia-pathops` and `shapely` were installed for boolean geometry.
