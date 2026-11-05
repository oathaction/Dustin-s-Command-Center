# Editorial system 01, Times Explainer: notes

Oath & Action Brand Guide, Edition 06. Phase 2, November 5, 2026. Maker's notes for the editorial round, updated after the fix pass. Page: `work/boards/phase-2/atlas-editorial/01-times-explainer/20261105_Editorial-01-Times-Explainer.html`, built by `build_system.py` beside it.

## The idea

The atlas told the way a newspaper explainer tells a complex system: in order, on a White page, with drawings that do the teaching. The overview opens on the atlas question, "Who do they answer to?", with the finding set beneath it as a marked studio draft. The whole system follows on the first screen: eight parts by name and question, the flows between them with their counts, and the return line to Wealth. Then come sixteen everyday questions, then "How the circuit runs", the parts in reading order along a spine. Each part has its question, two sentences of its story and every condition by its short label, and a counted flow names its best-evidenced connections. The route a headline names is Charcoal; everything else sits in Stone. Red appears only on the loop and reform pages, where R-01 acts.

## The views

- **Overview.** Question, deck, finding, a how-to-read and evidence key; the whole system (desktop: one row of five parts with the outer three around it; phone: the parts stacked with the return line at left); the 16 questions; the walk-through; on desktop, a second drawing with every condition named.
- **Elections.** Five condition cards, the drawing where the safe-seat and accountability loops meet, 8 connections in and 7 out as sentence rows, seven loops, 39 problems (38 with a case) and 10 reforms.
- **Loop R10.** The cycle at full size with each step's name, sign and verb, delay, grade and gloss; the weakest step; a step-through; R-01's targets in red, with R-02 and R-03 selectable.
- **Reform R-01.** A stance and disclosure box at the top; problem, change, the loop drawing, effects in words, routes with check dates, evidence, tradeoffs, risks and status.
- **Loops.** All 23 as box-and-arrow cycles grouped by the part they are based in, each with its summary's first sentence.
- **How to read.** Dustin's five ideas, each drawn, and three mix-ups from the data.

## Decisions

- **The spine is drawn by script from the markers' real positions**, so text reflows freely.
- **The first-screen drawing draws every pair with three or more connections**; the ten in thinner flows are printed in the boxes and in "The flows in words".
- **Variables are pills in every cycle**, as the design frame memo asks.
- **Phone figures are drawn for 320 px with nothing under 15 px**, so they hold 13 px on a 320 px phone.
- **Four kit lines:** selection stays in ink; reform red only on the loop and reform pages; select and animate the visible artboard.
- **The panel is a column**: the body makes room for it on wide screens, and container queries reflow each view.
- **Disclosures come from the dataset's `disclosure` field** on every reform card, picker and panel.
- **No Civic Line icons.** Nothing decorates.
- **Studio drafts:** the finding, the deck, the circuit heading and lede, the Elections headline, R-01's section headings and the key texts. The how-to-read headline is Dustin's Concept 00 line. Headlines with counts are built from the data.

## Fix pass

Civic education:
1. Diagram 4,600 px down: the whole system now fills the first screen at 1440 and ends by 1,320 px at 360.
2. Thesis headline: the atlas question leads; the finding sits beneath, marked "Studio draft", with why it says "can".
3. No evidence key: the five textures with glosses on the overview, Elections, R10, R-01 and the catalog.
4. "+M" display: effects in words, no glyph or code.
5. R-01 problem order: the R10 summary first, then the counts, then I026 and X01.
6. Question panels: every part, condition, loop and reform now opens.
7. Touched conditions moved inside the opened record. 8. "Down" removed from the story.

Interface: M1 as above. S1: sticky page index on desktop; on phones the problem groups start closed (I kept the domain groups; conditions overlap too much to group by). S2: an `h2` per R10 block; Elections headings close the skipped level. P1: a locator on every other view (hidden on phones). P2: an R-01 link under Elections. P3: example heads on the scale, sketch rails as two 1 px paths, no empty "Who acts". X1 to X6: done.

Evidence and brand: "38 with a real case"; disclosures on R-47 and the R10 picker; every ballot sentence opens "As of October 15, 2026,"; "Loops based here"; sign tags and ticks in ink; "Four loops pass through risk of losing office; two are drawn here"; "the cost of essentials"; "The problem is graded plausible; the remedy, contested." Left for Dustin: L23's name beside its minus sign, and whether "Democratic quality" should read "quality of democracy".

Creative director, two must-fixes: (1) the part questions in the lower overview drawing now wrap inside their boxes; a script confirms no text runs past any box in either drawing. (2) Each sentence with a figure in the 16 everyday answers is now followed by its sources (title, publisher, year). The script finds each figure in the text of a V7 claim, checking the pathway's own claims first, and prints that claim's sources. Every figure that is a statistic found its claim. Dates and law numbers, such as Public Law 119-21's "21", get no source.

Reader panel: questions moved up; a phone drawing that fits; connection codes off the overview and band labels off the cards; R10's key says red never marks a problem; the stance box. Left: "household" naming in two parts, which is DR-35's.

## Self-score

- Craft, 4: on the grid; a few step labels still end on a short line.
- Clarity, 5: the first screen names every part and shows how they connect; untested with readers.
- Brand fidelity, 4: locked palette and type, wordmark master, one working red; no icons.
- Usefulness, 5: every variable, flow, loop, problem and reform in Elections is reachable.
- Evidence honesty, 5: grades, weakest steps, sketches, dates and disclosures stated.
- Accessibility, 4: 0 axe violations at three widths; no screen-reader test.
- Beauty and distinctiveness, 4: reads as an explainer; the boxes stay plain.

## Tested

- `atlas_concepts_verify.py --selftest`: PASS, six of six planted errors caught.
- `atlas_concepts_check.js`: PASS, 6 views at 1440, 390 and 360 px, 0 failures, 0 axe violations, rerun after the creative director's fixes.
- Every figure-to-claim match in the 16 answers checked by eye against the claim text.
- My own audit at 320 and 360 px: no text under 13 px and nothing overflowing on any view.
- Scripted: the panel column, a reform opened from a question (no red), the aliases and an unknown hash, the skip link, the arrow-key hint on three drawings, the phone sheet, no page errors; every ballot sentence dated.

## Not tested

- Screen readers, Firefox, Safari, real phones, 200 percent zoom, reduced motion by eye.
- The ten-second test with readers; print and wall size.

## Change log

Created:
- `work/boards/phase-2/atlas-editorial/01-times-explainer/build_system.py`
- `work/boards/phase-2/atlas-editorial/01-times-explainer/20261105_Editorial-01-Times-Explainer.html`
- `work/boards/phase-2/atlas-editorial/01-times-explainer/20261105_Editorial-01-Times-Explainer-Verify-Results.json` and `-Check-Results.json`, written by the checks
- `work/boards/phase-2/atlas-editorial/01-times-explainer/captures/`, written by the check
- `work/handoffs/phase-2/20261105_Editorial-01-Notes.md`

Modified in the fix pass: the build script, the page, the results, the captures and these notes. Nothing outside the folder and this file. Nothing was committed.
