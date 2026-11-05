# Editorial system 03, Reference Sheets: notes

Oath & Action Brand Guide, Edition 06. Phase 2, November 5, 2026. Maker's notes for the red team and Board 2. Page: `work/boards/phase-2/atlas-editorial/03-reference-sheets/20261105_Editorial-03-Reference-Sheets.html`, built by `build_system.py` beside it.

## The idea

The atlas as a field guide of numbered sheets on Newsprint. Sheet 00 sets out the conventions, and sheets 01 to 05 apply them. Each sheet holds numbered plates with a plate rule, a heading, a short dek and a footer line that names exactly what the plate draws. One grammar runs through every sheet: a white box with a layer rule down its left edge is a condition, an arrow ending in a filled head carries a circled sign and the word "raises" or "lowers", the texture of the line is the evidence grade, and ticks after the tail count the wait. A red bracket marks where reform R-01 acts. Red does that one job, so every view that shows red shows it for R-01's targets. Every label, count, sign, grade, delay, issue, example and reform text comes from the dataset by script. The headlines are studio drafts: "The system runs as a circuit, from wealth back to wealth.", "Safe seats keep themselves safe.", "Every mark on these sheets makes one claim." and "Of 23 loops, 18 feed themselves and 5 push back." (the numbers in that last one are printed from the data).

## The views

- **01 The system (`#overview`).** The circuit after Concept 09, simplified. Outside forces run across the top as an open frame. Wealth, Voice, Elections, Checks and Policy stand as five cards read left to right. Each card shows its plain name over its formal title, its question, one sentence on what it is, every condition with its short label, one "passes on to" line, the count of connections inside it and the loops based there. Each card has the same four sections at the same heights, so the five read across like a table. Your household and Technology form the channel beneath. Only bundled flows are drawn, 27 of them, each with its count. The main circuit is drawn at 3 px, and the return line from Policy to Wealth runs under the row and is labelled. Where lines cross without joining, the line underneath breaks. Every card, condition and flow opens its record in a drawer, and a flow's record lists each connection in words. Below the drawing come the flows in words, "Start from a question" (5 topics, 16 questions, each naming the parts it runs through) and the three sketches. On a phone the drawing becomes a stack of cards in circuit order, joined by connectors that print the main-circuit counts.
- **02 Elections (`#area-c`).** Plate 02.1 shows the five conditions with icon, description and "a higher value means". Plate 02.2 follows "What pushes on it and what it pushes on": the 8 arriving connections on the left and the 7 leaving on the right, each column grouped by part, with Elections in the middle and its 5 inside connections listed as rows. Each line runs in its own track, and the track order is chosen by brute force for the fewest crossings, so each label sits on a straight lead-in. Plate 02.3 holds the seven loops that run through Elections as box-and-arrow cycles. Plate 02.4 is an issue register: 39 rows that can be filtered by condition and opened for the real-world example, a fix tried elsewhere, the evidence, the response, the tradeoff and the measure of success. Plate 02.5 shows the 10 reforms aimed at Elections, each with its effects, which are never summed.
- **03 Loop R10 (`#loop-r10`).** The loop at full size, after the Atlas Visual System's R1 sheet: four boxes with accent rules, the arrows running clockwise, each step labelled with its name, sign, verb, grade with gloss, and delay. L53 is dashed and marked as the weakest step. A red bracket on each of R-01's targets (L08, C2 and L25) joins one spine to the R-01 card, which carries its disclosure. Beside it sit the loop's facts, then the read-aloud line, a step-through, seven evidence notes and the three reforms.
- **04 Reform R-01 (`#reform-r01`).** Eight plates: the problem and its two issue records, where the reform acts (the same ring), what it changes, effects on an ordinal scale (never added), routes with feasibility and check dates ("No check date in V7" where V7 has none), problem and remedy evidence side by side, tradeoffs and risks, and status. The disclosure appears in full twice, under the deck and in plate 04.8.
- **05 All loops (`#loops`).** All 23 loops grouped by home part, with an index. Each card carries its plain name, V7 title, kind, the drawn cycle, the read-aloud line, weakest step, one turn, direction and reform count. The sketches are drawn hollow. R2 and R16 carry their hypothesis disclosure.
- **00 How to read (`#how-to-read`).** The conventions sheet after Dustin's Atlas Visual System and Concept 00: the tip is the effect, texture is the evidence, ticks count the wait, loops have a character (R8, B4, and R16's untested step), color is the layer, a bracket marks a reform. It also annotates the Elections card and ends with a glossary of 18 terms quoted from V7.

## Decisions

- **The sign sits in a circle beside the verb.** I took this from Dustin's Visual System sheet. The ring sits next to the arrow, the arrowhead stays the one closed triangle, and "raises" or "lowers" is printed at every sign. This departs from the design frame memo's pointing tag (Choice 3 is still open), so the decision log needs an entry.
- **The red marks only R-01.** The kit's selection red is switched off (one line in `kit_js()`), so selection is shown in ink and weight. Every view then carries the same single job, "R-01 targets".
- **The R-01 marks stay on the overview at rest.** Dustin's Concept 09 kept one red ring where R-01 acts. Here that is two marks on the Elections card, at C2 and at the R-01 note.
- **The return line is the only labelled flow.** It closes the circuit, and the brief names it.
- **"Passes on to" shows one real connection.** Each card names the best-evidenced connection to the next part that sits on a loop, with the lowest ID breaking a tie, and prints that rule's result by name and ID.
- **Ports and tracks are computed.** Plate 02.2's crossings are minimized by search, not placed by hand.
- **Effects keep V7's qualifiers.** For example, R-47's "+S entry; −S extremity" is printed as "small positive (V7: …)" so no qualifier is lost.
- **Card disclosures.** Every reform card for a reform that has a disclosure in the dataset prints it (R-01, R-02, R-47 here).
- **Text measured in Chromium.** Every SVG label wraps on the page's own Google Fonts metrics (`measure_text.js`, cached).
- **Kit departures.** The panel is a fixed drawer on the right. Selection finds the visible copy of an item when a view holds a desktop and a phone drawing. The kit is otherwise inlined unchanged.

## Self-score

- Craft, 4: on the grid and clean at 2x, with no overlapping labels. The overview's under-row routing is busy in one band.
- Clarity, 4: plain names, questions and every condition sit on the first screen, and the conventions sheet teaches each mark. No reader has tested it.
- Brand fidelity, 4: locked palette and type, the wordmark masters inlined, one red job. The circled sign departs from the memo's default.
- Usefulness, 5: six complete sheets, an issue register that can be filtered, every record one click away.
- Evidence honesty, 5: grades appear as texture and words, weakest steps and hypotheses are disclosed, effects are never summed, and the disclosures appear in full.
- Accessibility, 4: 0 axe violations at both widths, keyboard paths, focus rings. Screen readers are untested.
- Beauty and distinctiveness, 4: it reads as documentation of museum quality. The overview drawing is dense under the row.

## Tested

- `atlas_concepts_verify.py --selftest`: PASS (51 variables, 118 connections, 23 loops, 10 reforms). All six planted errors were caught.
- `atlas_concepts_check.js`: PASS, 6 views at 1440 and 390 px, 0 failures, 0 axe violations, no text under 13 px, one red job per view.
- I looked at every view at 1440 and 390 px over three passes, at 2x on the circuit, R10 and B2, and in grayscale. I checked selections and panels (C3, the Wealth to Voice flow), step 3 of the step-through, and the phone stack.

## Not tested

- Real screen readers, Firefox, Safari, real phones, 200 percent zoom.
- Widths between 900 and 1439 px, beyond a check that layouts reflow.
- First-time readers and the ten-second test. Print or wall size.

## Change log

Created, all in `work/boards/phase-2/atlas-editorial/03-reference-sheets/`: `build_system.py`, `measure_text.js`, `measure_cache.json`, `20261105_Editorial-03-Reference-Sheets.html`, `-Verify-Results.json` and `-Check-Results.json` (written by the checks), and 18 captures in `captures/`. Also `work/handoffs/phase-2/20261105_Editorial-03-Notes.md`. No other file was modified, and nothing was committed.
