# Concept 12, Editorial Desk: notes

Oath & Action Brand Guide, Edition 06. Phase 2, October 30, 2026. Maker's notes for Board 2. Page: `work/boards/phase-2/atlas-concepts/12-editorial-desk/20261030_Concept-12-Editorial-Desk.html`.

## The idea

The atlas drawn the way a newspaper graphics desk would draw it. Each view opens on a sentence that states a finding, with its evidence kind as a label above it. The route the headline names runs in Charcoal, and everything else stands back in Stone. Notes sit inside the drawing on 1 px leader lines and do the explaining. The overview, area C and R10 tell one story at three depths, and R10 keeps its real slot geometry at every level, so a reader who has seen its shape once knows it again. All headlines and decks are studio drafts built from V7's own sentences.

## The views

- **Overview.** The headline answers the atlas's question for one case: "In a safe seat, officials answer to the primary." On the left, the plan follows the data visualization memo's Part 3: the five core areas form a ring, the seven counts between them are printed as 40 px numbers with arrowheads showing direction, and each outer layer gets one band and one sentence. On the right, a magnified inset of area C draws R10 at reading size with two notes. The whole system fits a 1440 by 900 screen. Below come the ten areas in words and the index of all 23 loops, each with its route, kind, title, summary sentence, read-aloud line and status.
- **Area C.** "At electoral pressure, a loop that pushes back meets one that feeds itself." R10's parallelogram and B4's triangle meet at C3. All 20 connections are drawn: seven in Charcoal, 13 crossing the edge as Stone stubs that name the far variable with the verb ("Raised by X2 ..., area X"). Below come the five "a higher value means" lines, the four loops grouped here and the lines in words.
- **Loop R10.** The V7 title is the headline. The loop is told in order as the reader scrolls, the drawing held still beside the text: the current step takes 6 px ink and later steps step back to Stone. At rest the drawing shows the whole loop with its more-and-less marks. R-01's three targets carry the view's one working red.

## Decisions

- **Evidence label: "Causal claim" plus the V7 grade.** Section 15's four kinds describe measured charts; every atlas connection is a graded causal claim.
- **Verbs follow the grade.** "Answer to" rests on L08 and L25; anything leaning on L53 says "may".
- **No working red on the overview at rest.** The design frame memo says so; Charcoal carries the emphasis.
- **R10 at 45 degrees in every close-up.** Equal row and column spacing meets the frame's angle rule and keeps the slots.
- **Two artboards per view, switched at 1265 px.** Wide labels are 15 px, so they stay at 13 px or more down to that width.
- **Area C on a phone sits in a scroll region with a full-size button.** Thirteen named stubs do not fit 350 px; the memo allows it.
- **Kit departures.** The panel is a fixed drawer, so drawings keep the full grid. One line of `atlas-kit.js` selects the visible copy of an item when a view holds two artboards. R10's step-through is scroll-driven.
- **No icons.** The concept's rule is that nothing decorates. V7 labels carry every item.
- **No Times marks (D2-65).** Inter Tight takes the serif title's role. The research marks Times phone layouts unverified, so the phone form follows rule R25.

## Self-score

- Craft, 4: on the grid, labels clean at 1x and 2x; area C's stubs at C4 are dense.
- Clarity, 4: area names, counts and one dark route answer the ten-second questions; untested with readers.
- Brand fidelity, 4: locked palette and type, inlined wordmark, one working red per view.
- Usefulness, 4: three depths of one story, a full loop index, panels on every item.
- Evidence honesty, 5: grades sit in textures, labels and verbs; disclosures and weakest steps stated.
- Accessibility, 4: 0 axe violations, full keyboard paths; area C on a phone relies on a scroll region.
- Beauty and distinctiveness, 4: the inset and scroll story read as editorial work; the plan's boxes stay plain.

## Tested

- `atlas_concepts_verify.py`: PASS, and the self-test caught all six planted errors.
- `atlas_concepts_check.js`: PASS, 3 views at 1440 and 390 px, 0 failures, 0 axe violations.
- Captures viewed at 1440 (1x and 2x), 390 and grayscale; scroll states at the start, step 1 and step 4; panel states, including R-02 moving the red to C3; the Tab order on area C.

## Not tested

- Real screen readers, Firefox, Safari, real phones and 200 percent zoom.
- Widths between 391 and 1264 px beyond the layout rules.
- Reduced motion, by eye. The kit's rules are inlined unchanged.
- The ten-second test with readers, and print or wall size.

## Change log

Created:
- `work/boards/phase-2/atlas-concepts/12-editorial-desk/build_concept.py`
- `work/boards/phase-2/atlas-concepts/12-editorial-desk/20261030_Concept-12-Editorial-Desk.html`
- `work/boards/phase-2/atlas-concepts/12-editorial-desk/20261030_Concept-12-Editorial-Desk-Verify-Results.json`, written by the verifier
- `work/boards/phase-2/atlas-concepts/12-editorial-desk/20261030_Concept-12-Editorial-Desk-Check-Results.json` and nine captures in `captures/`, written by the check
- `work/handoffs/phase-2/20261030_Concept-12-Notes.md`

Modified: none outside the concept folder. Nothing was committed.
