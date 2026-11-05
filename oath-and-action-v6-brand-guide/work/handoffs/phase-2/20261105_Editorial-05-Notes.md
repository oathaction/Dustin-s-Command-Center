# Editorial system 05, Architecture: notes

Oath & Action Brand Guide, Edition 06. Phase 2, November 5, 2026. Page: `work/boards/phase-2/atlas-editorial/05-architecture/20261105_Editorial-05-Architecture.html`, built by `build_system.py` with `system.css` and `system.js` beside it.

## The idea

The atlas as a building a reader can walk through. Seven floors stack from the foundation up: Technology and Your household sit on Newsprint below a heavy ground line, and Wealth, Voice, Elections, Checks and Policy rise above it on White. Outside forces stand beside the building in their own column, with a stub and a count into each floor they push on. Each of the 51 variables is a room on its floor: a Civic Line tile with its code and short label. Each slab between floors carries an arrow, a count and one real connection as its example, with the count that pushes back down beside it. The return line runs down the left side from Policy into Wealth and Your household. A touch on any floor, tile or slab lights what it connects to and opens its record in the panel. Above it, five topic cards set like documents start from the reader's week.

## The views

- **Overview.** Headline, deck, how-to-read line and the four counts; five question cards holding the 16 everyday questions, each lighting its tiles; the building with its reading key in the panel's place; a census of where all 118 connections run; the 23 loops by home floor.
- **Elections.** A finding headline and a "You are here" elevation; the floor plan with its five inside connections; room cards; the 15 connections in and out, grouped by far floor and each drawn on its own; seven loop cycles; 39 issues by domain, each showing its real-world headline and opening to problem, fix and evidence; 10 reforms whose targets take the red when selected.
- **Loop R10.** V7's title, the read-aloud line, the full loop with each step's name, verb, sign, grade with gloss and delay; L53 named weakest; R-01's targets in the working red; a step-through; step cards with qualifications; evidence, the Alaska case and direction.
- **Reform R-01.** The problem and its issue records, what it changes, the loop with its targets, four effect families never added, routes with feasibility and check dates, both grades, tradeoffs, failure risks, and status with the disclosure in full.
- **Loop catalog.** All 23 loops by home floor as named cycles with kind, weakest step, read-aloud line, status, reform count and a tiny elevation of their floors. R2 and R16 carry their closure flag; B2, B3 and R9 draw open lines.
- **How to read.** Five drawn habits after Concept 00, 14 mix-ups and 21 terms.

## Decisions

- Plain name, formal title, then question on every floor (DR-32, DR-35).
- The ground line and Newsprint mark the economy and technology layers, so the layer survives grayscale.
- Each slab names the connection on the most loops, then the strongest evidence, then V7 order.
- Down counts print beside up counts, so the building does not read as a ladder (civic memo, misreading 7).
- Heavier arrows trace the main circuit; the 18 connections that skip a floor are counted, not drawn (DR-29).
- R-01's 96 px icon stands alone in signature red under Rule 05.3.
- Hub icons are Civic Line icons named for each topic: Essential Costs, Healthcare, Household Income, Local Government, Voting.
- Every reform shown beyond its title carries its disclosure from `reforms[id]['disclosure']`.
- Kit departures: a select picks the visible copy when a view holds desktop and phone drawings; the panel moves into each view's right column; hover previews pause while a question scrolls the building.

Studio drafts: the overview deck and how-to-read line, the Elections headline, the catalog headline (counts from the data), and section titles and decks. The overview headline is V7's question, R10's is V7's title, and How to read uses Dustin's Concept 00 line.

## Self-score

- Craft, 4: on grid, labels clean at 1x; the outside column runs tall below its list.
- Clarity, 4: floors, counts and the return line read fast; untested with readers.
- Brand fidelity, 4: locked palette and type, masters inlined, one working red; the red feature icon may draw comment.
- Usefulness, 5: every variable, flow, loop, issue and reform is one tap away.
- Evidence honesty, 5: texture, grades, weakest steps, sketches, undated routes and disclosures come from the data.
- Accessibility, 4: 0 axe violations and full keyboard paths; no screen reader test.
- Beauty and distinctiveness, 4: the section drawing reads as architecture; the cards could go further.

## Tested

- `atlas_concepts_verify.py --selftest`: PASS; all six planted errors caught.
- `atlas_concepts_check.js`: PASS, 6 views at 1440 and 390 px, 0 failures.
- Every view viewed at 1440 and 390 over three passes, plus the overview as a poster and R10 in grayscale.
- Selection states, the R10 step-through and the phone sheet.
- A script audit of every computed text style against the frame memo's scale.

## Not tested

- Screen readers, Firefox, Safari, real phones and 200 percent zoom.
- Widths between 391 and 1439 px beyond the layout rules.
- Reduced motion by eye, print, and the ten-second test with readers.

## Change log

Created in `work/boards/phase-2/atlas-editorial/05-architecture/`: `build_system.py`, `system.css`, `system.js`, the page, both results files and 18 captures. Also `work/handoffs/phase-2/20261105_Editorial-05-Notes.md`. Modified: none outside the folder. Nothing was committed.
