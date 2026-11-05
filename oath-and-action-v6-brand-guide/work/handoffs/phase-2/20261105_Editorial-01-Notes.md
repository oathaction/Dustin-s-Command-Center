# Editorial system 01, Times Explainer: notes

Oath & Action Brand Guide, Edition 06. Phase 2, November 5, 2026. Maker's notes for the editorial round. Page: `work/boards/phase-2/atlas-editorial/01-times-explainer/20261105_Editorial-01-Times-Explainer.html`, built by `build_system.py` beside it.

## The idea

The atlas told the way a newspaper explainer tells a complex system: in order, on a White page, with drawings that do the teaching. The overview reads top to bottom along a spine. Outside forces press in, then Wealth, Voice, Elections, Checks and Policy follow as numbered parts, each with its question, two sentences of its story and every condition by its short label. Between parts, a large figure counts the connections passed on, with the two best-evidenced connections named. A line at the left carries Policy and Your household back to Wealth, so the circuit closes in the layout itself. One calm summary diagram follows, then sixteen everyday questions. The route a headline names is Charcoal; everything else sits in Stone. Red appears only on the loop and reform pages, where R-01 acts.

## The views

- **Overview.** Headline, deck and key; the eight parts in reading order; "How the circuit runs" (all 51 conditions named, every part-to-part flow printed); the whole system as eight boxes listing their conditions, 19 flows drawn with no crossings; "Start from your own bill" with 16 questions that open in the panel.
- **Elections.** Its five conditions as cards, a drawing where the safe-seat and accountability loops meet, the 8 connections in and 7 out as sentence rows grouped by part, the seven loops through it, 39 problems with their cases (each opens in place) and 10 reforms with what each changes.
- **Loop R10.** The four-station cycle at full size with each step's name, sign and verb, delay, grade and gloss; the weakest step; a step-through; R-01's three targets in the working red, with R-02 and R-03 selectable.
- **Reform R-01.** Problem, change, the loop drawing with its targets, four effect families never added, routes with feasibility and check dates, both grades, tradeoffs, risks and the status with the full disclosure.
- **Loops.** All 23 as box-and-arrow cycles, grouped by home part, each with plain name, V7 title, kind, read-aloud line, status and reform count.
- **How to read.** Dustin's five ideas, each with a small drawing, and three mix-ups from the data.

## Decisions

- **The spine is drawn by script from the markers' real positions.** Text reflows at any width and the circuit keeps its shape at 390 px.
- **Summary diagram draws every pair with three or more connections.** The 10 connections in single or double flows are printed in the boxes and in "The flows in words", which keeps the drawing calm.
- **Variables are pills in every cycle.** The design frame memo makes variables full-radius; the brief's "boxes" become pills.
- **Read-aloud lines use the short labels**, with "fewer" for plural heads.
- **Selection stays in ink.** One kit line keeps red for R-01's targets alone. Two more kit lines select and animate the visible artboard when a view holds a wide and a narrow drawing.
- **The panel is a fixed drawer on desktop** (interaction departure), so drawings keep their grid.
- **Loops are grouped by the data's `home` field.** R4b sits under Elections, where the October model listed it under Voice.
- **No Civic Line icons.** Nothing decorates; the icon files' `data-part` attributes also trip the verifier.
- **R-01's disclosure is read from Atlas V7's interest table** in the V7 extract. The editorial data's status text lacks it, though the brief says it holds it. The main session may want to add it to the data file.
- **Studio drafts:** the overview headline and deck, the circuit's heading and lede, the Elections headline, R-01's section headings and the key texts. The how-to-read headline is Dustin's Concept 00 line. Headlines with counts are built from the data.

## Self-score

- Craft, 4: on the grid with clean labels; some step labels in the R10 drawing still break onto a short last line.
- Clarity, 4: the circuit answers what each part is and how they connect; untested with readers.
- Brand fidelity, 4: locked palette and type, wordmark master, one working red; no icons.
- Usefulness, 5: every variable, flow, loop, problem and reform in Elections is reachable.
- Evidence honesty, 5: grades, weakest steps, sketches, hypothesized steps and the disclosure are stated.
- Accessibility, 4: 0 axe violations; the Elections and summary drawings rely on lists or scroll regions on phones.
- Beauty and distinctiveness, 4: reads as an explainer; the summary boxes are plain by design.

## Tested

- `atlas_concepts_verify.py --selftest`: PASS, all six planted errors caught.
- `atlas_concepts_check.js`: PASS, 6 views at 1440 and 390 px, 0 failures, 0 axe violations, one working-red job on R10 and R-01, none elsewhere.
- Every view viewed at 1440 and 390 px over three refinement passes, and R10 in grayscale.
- Scripted: panel from a variable, a part and a question; Escape; the stepper; R-02 moving the red to C3 and back; `#loops/loop-r8`; the phone sheet; no page errors.
- No sideways scroll at 1024 and 1280 px.

## Not tested

- Real screen readers, Firefox, Safari, real phones, 200 percent zoom.
- Reduced motion and arrow keys inside drawings, by hand.
- The ten-second test with readers; print and wall size.

## Change log

Created:
- `work/boards/phase-2/atlas-editorial/01-times-explainer/build_system.py`
- `work/boards/phase-2/atlas-editorial/01-times-explainer/20261105_Editorial-01-Times-Explainer.html`
- `work/boards/phase-2/atlas-editorial/01-times-explainer/20261105_Editorial-01-Times-Explainer-Verify-Results.json` and `-Check-Results.json`, written by the checks
- `work/boards/phase-2/atlas-editorial/01-times-explainer/captures/`, 18 captures written by the check
- `work/handoffs/phase-2/20261105_Editorial-01-Notes.md`

Modified: none outside the folder and this file. Nothing was committed.
