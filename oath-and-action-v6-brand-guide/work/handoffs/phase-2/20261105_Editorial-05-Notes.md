# Editorial system 05, Architecture: notes

Oath & Action Brand Guide, Edition 06. Phase 2, November 5, 2026. Page: `work/boards/phase-2/atlas-editorial/05-architecture/20261105_Editorial-05-Architecture.html`, built by `build_system.py` with `system.css` and `system.js` beside it. Updated after the fix pass; the fix pass section below lists each finding and what changed.

## The idea

The atlas as a building a reader can walk through. Seven floors stack: Technology and Your household are the two shaded floors at the base, and Wealth, Voice, Elections, Checks and Policy stand above them. Outside forces stand beside the building, with a stub and a count into each floor they push on. Each of the 51 variables is a room on its floor: a Civic Line tile with its code and short label. Each joint between neighboring floors carries influence both ways, each direction with its count and one named connection. The return line runs from Policy to Wealth and Your household at the same weight as the joints, so the building reads as a circuit. A touch on any floor, tile or joint lights what it connects to and opens its record in the panel beside the building.

## The views

- **Overview.** The first screen pairs the headline with "The system at a glance": all eight parts with plain names and questions, the counts both ways between neighbors, the return line and the outside forces. Then five question cards with the 16 everyday questions, the full building with its key, a census of where all 118 connections run, and the 23 loops by home floor.
- **Elections.** A finding headline and a "You are here" elevation; the floor plan with an evidence key; room cards; the 15 connections in and out, grouped by far floor; the seven loops, R10 and B4 first, with the sentence that ties them; 39 issues by domain; 10 reforms, each saying what it does.
- **Loop R10.** V7's title and the read-aloud line, the full loop with the step-through beside it, L53 named the weakest step and what that means, R-01's targets in red, a link to R-01, step cards and the evidence.
- **Reform R-01.** A stance and disclosure box under the summary, then the problem, what it changes, where it acts, effects in words, routes, legal authority, carrying it out, costs, how to judge results, both grades, tradeoffs, failure risks, alternatives and status.
- **Loop catalog.** All 23 loops by home floor, each card with its summary's first sentence, the floors it stands on, the cycle, the read-aloud line and status; R1 carries its qualification.
- **How to read.** Five drawn habits after Concept 00, 14 mix-ups and 21 terms.

## Decisions

- Plain name, formal title, then question on every floor (DR-32, DR-35).
- Joints name both directions with equal arrows; the copy drops "up" and "down".
- Each joint names the connection on the most loops, then the strongest evidence, then V7 order.
- The 18 connections between floors that are not neighbors are counted, not drawn (DR-29).
- Phones get their own 280-unit drawings, so text holds at 13 px down to 320 px.
- Red marks only a reform's targets or the selected item; sign tags, ticks and the R-01 icon stay in ink.
- Hub icons are Civic Line icons named for each topic: Essential Costs, Healthcare, Household Income, Local Government, Voting.
- Kit departures: a select picks the visible copy; the panel moves into each view's right column; hover previews pause while the page scrolls to a pick.

Studio drafts: the overview deck and how-to-read line, the Elections headline, the catalog headline, the sentence tying R10 to B4, "The loop holds only as firmly as this link." (after System 3), and section titles and decks.

## Fix pass

Civic educator: M1 ladder: two-way joints, equal weights, no "up" or "down" in the copy. M2: reform cards print the summary's first sentence. M3: R-01 gains five sections, and the disclosure moves beside the summary. S4: the glance puts every part on the first screen. S5: the question deck now reads "Pick a question about a bill or a notice you already know." S6: "The weakest step" in bold with its line. S7: the R10 and B4 sentence, cards side by side. P8: the plus-sign line from the shared kit; no palette names. P9: floors named in words.

Interface: M1, M2 as above. S1: h3 per issue group, loop card and index group. S2: each catalog card is a Tab stop. S3: Elections opens its page on the click; R-01 linked under the loop. S4: the step-through sits beside the drawing. S5: 44 px rows for phone links. P1: no 4 px strokes, the atlas named in the page title, empty fields dropped. X1 to X5: phone picks scroll above the sheet, the arrow-key line, the skip link, and a visible router message.

Evidence auditor: disclosures on issue records; 14 ballot mentions open "As of October 15, 2026"; Well supported in every key; "Open any one for its full record"; R4b under Elections; ink sign tags; the return line names Your household; "Switched off"; no Lora; "fewer" for countable things.

Reader panel: the glance answers the first screen; on a phone it comes before the questions, and every joint names both floors.

Left as they are: L23's name and the family name "Democratic quality" are Dustin's calls. The full building stays long; the glance carries the first screen.

Creative director's two must-fixes: the Terms glossary shared the class `gl` with the glance's grid, which squeezed it into 34 and 30 px columns; it now has its own class and sets as two columns, one on phones. The route table stacks on phones, so every check date shows. Each of the 16 question answers now prints a numbered source (title, publisher, year) after every sentence that carries a figure, read by script from V7's pathway claims in `work/extract/atlas-v7-data.json`. Twelve answers carry figures; all are sourced. PW13's "three-quarters" and its 2028 projection are sourced too.

## Self-score

- Craft, 4: on grid at three widths; the outside column runs tall.
- Clarity, 4: the first screen names every part and both directions; untested with readers.
- Brand fidelity, 5: locked palette and type, masters inlined, red only where a reform acts or on a pick.
- Usefulness, 5: every variable, flow, loop, issue and reform is one tap away.
- Evidence honesty, 5: data-built text, dated ballot lines, disclosures wherever a reform is argued.
- Accessibility, 4: 0 axe violations; no screen reader test.
- Beauty and distinctiveness, 4: the section drawing reads as architecture.

## Tested

- `atlas_concepts_verify.py --selftest`: PASS; six planted errors caught.
- `atlas_concepts_check.js`: PASS, 6 views at 1440, 390 and 360 px, 0 failures.
- My own audit at 320 and 360 px: no text under 13 px, nothing past the edge, no label overflowing its tile.
- Every view viewed at 1440 and 390, and the overview as a poster.
- Skip link, an unknown hash, `#area-a`, the arrow-key line, glance jumps and the phone sheet, by script.

## Not tested

- Screen readers, Firefox, Safari, real phones and 200 percent zoom.
- Reduced motion by eye, print, and readers.

## Change log

Created in `work/boards/phase-2/atlas-editorial/05-architecture/`: `build_system.py`, `system.css`, `system.js`, the page, both results files and the captures. Also `work/handoffs/phase-2/20261105_Editorial-05-Notes.md`. Modified in the fix pass: the same files. Nothing outside the folder; nothing committed.
