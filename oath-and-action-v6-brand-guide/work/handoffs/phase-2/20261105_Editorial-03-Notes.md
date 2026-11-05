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

## Fix pass, November 5

The idea stays the same: numbered sheets, one set of marks, and the circled sign as a deliberate variant (D2-81). The biggest change is the overview. Its first screen is now a compact circuit with all eight parts, their questions and the main flows. The cards follow with no wiring, and every flow appears in a table. On the loop and reform sheets, red now sits on R-01's targets themselves.

### The thirteen shared fixes

1. **First screen.** At 1440 by 900 the compact circuit (plate 01.1) shows all eight parts with plain name, formal title and question. It also shows 20 of the 27 bundles with counts: the main circuit, the return line, outside forces, and the household and technology links. A note says the seven small bundles that skip a part (14 connections) are in the flow table. On a phone the circuit is a list in circuit order with counts between the parts. Technology ends at 1,507 px at 390 and 1,597 px at 360, inside two 844 px screens.
2. **Disclosures.** The R-01 sheet has one labelled box, "Where the atlas stands", beside the head. It prints the no-position sentence first and the disclosure second. I removed the no-position sentence from the reform's case so the two stay apart. Every reform card, the R10 reform cards, the R-01 panel record, and each "Reforms aimed at it" line in the issue register carry the dataset's disclosure where one exists (R-01, R-02, R-47, R-49 on these sheets).
3. **Ballot dates.** A script adds "As of October 15, 2026," to every clause in V7's prose that names the November 3, 2026 ballot. A text scan of the built page finds no undated mention.
4. **Headlines.** R10's headline now reads "Safe seats can keep themselves safe, through one plausible step." The grade word is built from L53. The overview deck no longer states the chain as fact. It says every connection carries a grade.
5. **Step direction and "fewer".** Step sentences come from the running product of signs. Countable labels take "fewer" ("fewer incumbents defeated", "fewer watchdogs and enforcement").
6. **Effects in words.** Effects print in words with V7's qualifiers kept, for example "small positive for entry; small negative for extremity" (R-07). The code glyphs are gone from the R-01 scale head.
7. **Red.** No working red remains on the overview, Elections, the catalog or sheet 00, whose sample is marked a specimen. On R10 and R-01, red marks only L08, L25 (line and arrowhead, with Charcoal keylines) and the C2 box. The joining wires are gone, and ink tags name R-01, R-02 and R-03 where they aim. Signs stay ink.
8. **Panel.** On desktop, an open panel pads the page, so the layout gives it a column. The pick scrolls into view inside its drawing. On a phone, the tapped item scrolls above the sheet: C5 ends at 187 px with the sheet top at 439.
9. **Small phones.** Loop chains are drawn in a 300-unit viewBox with the return line inside. Margins drop to 10 px under 360. There is no sideways scroll and no text under 13 px at 390, 360 and 320.
10. **Keyboard.** A skip link focuses the view's heading and keeps the hash. A drawing that takes focus writes "Arrow keys move between items. Enter opens one." into its readout. `#area-a` through `#area-tc` open each part's record, `#reform-r-01` opens the reform sheet, and `#loop-r10/reform-r-01` keeps its selection. An unknown hash shows a visible status line.
11. **Catalog.** Each card prints the first sentence of its summary under the title. R1's card carries its qualification. The return step is labelled at the bottom, where the chain closes.
12. **Evidence key.** It appears on the overview, Elections, R10, R-01 and the catalog, where it includes the hollow line.
13. **Palette and wordmark.** The only colors in the page are the locked palette plus Deep Stone. The name appears only as the wordmark master.

### My sections of the reports

- **Civic 1 to 3 (Must):** the deck and evidence key are fixed; the R-01 target is off the overview; Elections leads with the connections in words, and the drawing opens from a button.
- **Civic 4 to 7 (Should):** each question opens its V7 short answer first, with a link to its loop or part. The R10 red now sits on the targets. The headline is rewritten. Plate 02.3 says R10 and B4 meet at C3 and quotes B4's "works only where seats are competitive".
- **Civic 8 and 9 (Polish):** codes now follow names in a lighter weight on the cards, the phone stack and the loop chains. "Kind" is off the condition cards, and "auxiliary" is put in plain words in the panels. Return steps sit at the bottom.
- **Interface M1:** the step-through sits beside the ring at 1440. The controls start at about 650 px, inside the first screen. On a phone they sit under the chain.
- **Interface M2:** fixed, as in fix 9.
- **Interface S1:** clicks on the Checks header now land; tested on both drawings.
- **Interface S2:** loop chips on the phone stack are now 44 by 44 pills.
- **Interface S3:** the "On this sheet" bar stays in view on desktop.
- **Interface S4:** fixed, as in fix 10.
- **Interface P1:** filter buttons are now 15/600 and hub heads 22/800. Headings balance their lines. The empty "()" is gone. The red strokes are now 3 px with 1 px keylines.
- **Evidence 1 to 10:** 1 (R-49 and other disclosures in issue lines), 2 (dates), 3 (red), 4 (headline), 5 (R-07 wording), 6 ("3 of the 23 are sketches"), 7 ("Checked October 15, 2026"), 8 (V7's "Drawn as" notes trimmed from the glossary), 9 ("an idea with no numbered connection") and 10 ("fewer") are all done.
- **Reader panel:** the wiring under the cards is gone. The word "Plate" is dropped from plate numbers and "Key plan" now reads "You are here". The two counts on the reform sheet are labelled: the problem evidence counts 2026 seats, and each issue example carries its year.

### Left as is, and why

- **Phone length of Elections** (interface S3): 29 phone screens. The issues are closed rows and the index is at the top. A phone-only regrouping would need its own design pass.
- **The sheet numbers and IDs:** they are the system's idea. I kept them and moved them after the plain names.
- **Hollow sketch lines:** these stay 4 and 2 px. Moving them to 3 and 1 px would close the gap that makes them read as hollow.
- **For Dustin:** whether "Democratic quality" may print as "quality of democracy" (civic report), and L23's name against its sign (red team S4).

### Fix pass tested

- `atlas_concepts_verify.py --selftest`: PASS, and all six planted errors were caught.
- `atlas_concepts_check.js`: PASS at 1440, 390 and 360 px, with 0 failures and 0 axe violations. The minimum text size is 13 px. There is one red job ("R-01 targets") on R10 and R-01 and none elsewhere.
- I scripted these checks:
  - All 8 parts lie inside the first 900 px at 1440, and within two phone screens at 390 and 360.
  - No sideways scroll or small text at 320.
  - Every alias and the skip link land where they should, and the unknown-hash status shows.
  - E1 is not covered by the open panel, and C5 sits above the phone sheet.
  - Clicks land on the parts.
  - Step 3's status line reads correctly.
  - No undated ballot mention and no off-palette color remain.
- I viewed every reworked plate at 1440, the phone forms at 390, 360 and 320, and the overview in grayscale.

### Fix pass not tested

- Real screen readers and phones, Firefox and Safari, readers on the new first screen.

## Change log

Created, all in `work/boards/phase-2/atlas-editorial/03-reference-sheets/`: `build_system.py`, `measure_text.js`, `measure_cache.json`, `20261105_Editorial-03-Reference-Sheets.html`, `-Verify-Results.json` and `-Check-Results.json` (written by the checks), and 18 captures in `captures/`. Also `work/handoffs/phase-2/20261105_Editorial-03-Notes.md`. The fix pass modified `build_system.py`, the page, `measure_cache.json`, both results files, the captures and these notes, all in the same places. No other file was modified, and nothing was committed.
