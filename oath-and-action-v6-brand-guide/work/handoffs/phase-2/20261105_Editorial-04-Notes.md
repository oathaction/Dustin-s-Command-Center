# Editorial system 04, Night Edition: notes

Oath & Action Brand Guide, Edition 06. Phase 2, November 5, 2026. Maker's notes for the editorial round. Page: `work/boards/phase-2/atlas-editorial/04-night-edition/20261105_Editorial-04-Night-Edition.html`, built by `build_system.py` beside it.

## The idea

Dustin's dark atlas, kept in its structure and cut to its main lines. The overview reads left to right as one circuit, from Wealth through Voice, Elections, Checks and Policy, with a return line back to Wealth. Each part is a raised card: plain name over formal title, its question, its first story sentence and every variable by short name. Only 18 bundled arrows run between the cards, each with its count; the circuit is bright Newsprint and the rest Stone. Loops are icon box-and-arrow cycles after the dark grid Dustin liked. Red appears only where a reform acts.

## The views

- **Overview.** Finding headline, deck, the two questions and four counts; the board under a band naming which question each part answers; 5 topics and 16 everyday questions; three loops to start (R8, R10, B4) and every loop by name.
- **Elections.** Question as headline, story, counts, a full-size drawing of the five variables and five inside connections, every edge-crossing connection listed by part with its line sample, the variables, seven loops, 10 reforms and 39 issues by V7 topic with real cases.
- **Loop R10.** Read-aloud line first; boxes with "a higher value means"; each step's name, verb, sign, grade and delay; L53 marked weakest; R-01's targets in red; a step-through; evidence, timing, qualification and the three reforms.
- **Reform R-01.** Summary, status with the full disclosure, its issues, R10 with its targets in red, four effect families never added, routes with feasibility and check dates, both grades, tradeoffs and risks.
- **All loops.** 23 cycles by home part, each with kind, plain name, V7 title, read-aloud line, weakest step and reform count.
- **How to read.** Concept 00's five rules drawn as specimens, plus the 14 mix-ups from the data.

## Decisions

- Proposed tint, Night Panel #1F1F1E: Charcoal with 8 percent Newsprint by OKLab mix, for raised cards and the panel only. Newsprint 11.70:1, Dim Newsprint 6.39:1, Pillar Red 3.96:1. Proposed, not adopted.
- Main flows carry 66 connections: circuit, return, back flows, outside forces into A to E, five layer flows. The other 15 are named under the map.
- Checks gets a wider card so seven variables fit and the board stays near 900 px tall.
- Small cycles use the tag as the arrowhead (dataviz memo); boxes carry 48 px icons, since 14 need it.
- R3 lists no weakest step; the page names L47 by grade, as R3's evidence summary does.
- The question band reads the dark atlas extract (`story.parts[].q`).
- "Color is the layer" becomes letter and place, since hue keeps one job on Charcoal: a departure from Concept 00.
- With no reform in view, selection takes the red (DR-18).
- Kit: one line selects the visible copy where a view holds two artboards; the panel is a right drawer.
- Every reform card and issue panel naming a flagged reform carries its disclosure.
- Studio-draft headlines: "Policy that favors insiders adds to the wealth that funds political spending." (rests on L03 and L01, both well supported); "18 of the 23 loops feed themselves. 22 have a reform aimed at them."; "The risk of losing office is where the safe-seat loop meets the loops that hold officials to account."; "Every line says what happens next, and how sure we are." (Concept 00). R10 and R-01 use V7's titles.

## Self-score

- Craft, 4: labels clear at 1x and 2x; some step labels wrap tightly in the Elections drawing.
- Clarity, 4: one bright circuit and plain names; not yet tested with readers.
- Brand fidelity, 4: locked type and palette, wordmark as delivered; the Night Panel tint awaits approval.
- Usefulness, 5: every part, variable, flow, loop, reform, issue and question opens a full record.
- Evidence honesty, 5: every word and count from the data; sketches, hypotheses and the disclosure shown.
- Accessibility, 4: 0 axe violations, full keyboard paths; untested with screen readers.
- Beauty and distinctiveness, 4: calm and luminous; the overview's lower cards are dense.

## Tested

- `atlas_concepts_verify.py`: PASS; the self-test caught all six planted errors.
- `atlas_concepts_check.js`: PASS, 6 views at 1440 and 390 px, 0 failures, 0 axe violations, text 13 px or larger, one red job per view.
- My runs: Tab on each view (every stop ringed); arrows walk R10 as C1, L08, C2 and round; Enter and Escape with focus returned; deep links; the step-through; R-04 moving the red; the phone sheet.
- Color captures at 1440 and 390, and 2x zooms of loop cards, viewed.

## Not tested

- Screen readers, Firefox, Safari, real phones, 200 percent zoom.
- Widths between 900 and 1339 px, where the board turns into a grid of cards.
- Reduced motion by eye, print and wall size, and the ten-second test with readers.
- Note: the check's grayscale style survives its hash navigation, so its later 1440 captures are gray; `-color` captures show them in color.

## Change log

Created:
- `work/boards/phase-2/atlas-editorial/04-night-edition/build_system.py`
- `work/boards/phase-2/atlas-editorial/04-night-edition/20261105_Editorial-04-Night-Edition.html`
- `work/boards/phase-2/atlas-editorial/04-night-edition/20261105_Editorial-04-Night-Edition-Verify-Results.json` and `-Check-Results.json`, written by the checks
- `work/boards/phase-2/atlas-editorial/04-night-edition/captures/`: 18 captures from the check, 5 color captures and 5 interaction states
- `work/handoffs/phase-2/20261105_Editorial-04-Notes.md`

Modified: none outside the folder. Nothing was committed.
