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

- Cards and the panel are Charcoal with a 1 px Stone rule. The proposed Night Panel tint (#1F1F1E) is withdrawn until Dustin rules on it.
- Main flows carry 66 connections: circuit, return, back flows, outside forces into A to E, five layer flows. The other 15 are named under the map.
- Checks gets a wider card so seven variables fit and the board stays near 900 px tall.
- Small cycles use the tag as the arrowhead (dataviz memo); boxes carry 48 px icons, since 14 need it.
- R3 lists no weakest step; the page names L47 by grade, as R3's evidence summary does.
- The question band reads the dark atlas extract (`story.parts[].q`).
- "Color is the layer" becomes letter and place, since hue keeps one job on Charcoal: a departure from Concept 00.
- With no reform in view, selection takes the red (DR-18).
- Kit: selection prefers the copy the reader used, else the visible copy; after the panel opens, the picked item scrolls into view.
- Every reform card and issue panel naming a flagged reform carries its disclosure.
- Studio drafts: the overview leads with the two questions and runs one finding built from the names of L03 and L01; "18 of the 23 loops can feed themselves. 22 have a reform aimed at them."; "4 loops pass through the risk of losing office. Two are drawn here..."; "Every line says what happens next, and how sure we are." (Concept 00).

## Self-score

- Craft, 4: labels clear at 1x and 2x; some step labels wrap tightly in the Elections drawing.
- Clarity, 4: one bright circuit and plain names; not yet tested with readers.
- Brand fidelity, 4: locked type and palette only, wordmark as delivered.
- Usefulness, 5: every part, variable, flow, loop, reform, issue and question opens a full record.
- Evidence honesty, 5: every word and count from the data; sketches, hypotheses and the disclosure shown.
- Accessibility, 4: 0 axe violations, full keyboard paths; untested with screen readers.
- Beauty and distinctiveness, 4: calm and luminous; the overview's lower cards are dense.

## Tested

- `atlas_concepts_verify.py`: PASS; the self-test caught all six planted errors.
- `atlas_concepts_check.js`: PASS, 6 views at 1440, 390 and 360 px, 0 failures, 0 axe violations, text 13 px or larger, one red job per view.
- My runs: Tab on each view (every stop ringed); arrows walk R10 as C1, L08, C2 and round; Enter and Escape with focus returned; deep links; the step-through; R-04 moving the red; the phone sheet.
- Color captures at 1440 and 390, and 2x zooms of loop cards, viewed.

## Not tested

- Screen readers, Firefox, Safari, real phones, 200 percent zoom.
- Widths between 900 and 1339 px by eye, where the board turns into a grid of cards.
- Reduced motion by eye, print and wall size, and the ten-second test with readers.
- Note: the check's grayscale style survives its hash navigation, so its later 1440 captures are gray; `-color` captures show them in color.

## Fix pass

Each finding I was given, what changed, or why it stayed.

**Shared fixes.**
1. First screen: the overview now opens with "The system at a glance": all eight parts with their questions, the circuit with counts, the return line and both layers, inside 900 px at 1440. On a phone it is a vertical circuit; all eight parts sit in the first two screens at 390 and 360 px.
2. Disclosures: every reform card, reform panel and issue panel naming a flagged reform prints it. R-01 has one box near the top: "The Atlas takes no position..." first, the disclosure second, apart from the case.
3. Dates: every sentence naming the November 3, 2026 ballot opens "As of October 15, 2026," by one rule in the build (13 sentences, 0 undated).
4. Claims: "can feed themselves" in the catalog headline, "can feed itself" for R10 in Elections and at the end of the step-through.
5. Steps read with the loop; "fewer" for countable things (fewer incumbents defeated, fewer watchdogs and enforcement).
6. Effects in words, with no glyph or code.
7. Sign tags stay in ink. On the loop and reform pages red marks only R-01's lines, arrowheads and box; the red swatches and the red rule on R-01's card are gone.
8. The panel is a column the layout makes room for; the picked item scrolls into view beside it. On a phone the tapped item moves above the sheet.
9. Phone figures are `width: 100%` on a 320 px viewBox, with labels at 15 px; at 320 px nothing falls under 13 px and nothing clips.
10. A visible skip link focuses the view's heading and keeps the hash. Drawings write "Arrow keys move between items. Enter opens one." when they take focus. `#area-a` to `#area-tc` open that part; unknown hashes show the status line.
11. Each catalog card leads with name and kind, then the drawing, the first summary sentence and the read-aloud line. R1 carries its qualification.
12. The evidence key sits on the overview, Elections, R10, R-01, the catalog and How to read.
13. Locked palette only; the name appears only as the wordmark.

**Civic education.** "One graded connection at a time" (M1; the dark atlas's paragraph with "documented" and "Rent climbs faster than pay" is no longer printed). The questions lead and the finding runs smaller (M2). Problems come before reforms (S3). Each circuit flow names one connection under the map (S4). R-01's problem opens with the R10 summary (S5). B4 is drawn beside R10 with "The loop works only where seats are competitive." (S6). "Light: the route you are reading." (P7). "Where a reform can interrupt a loop" (P8).

**Interface.** M1 and M2: skip link visible; issues, connections, variables and reforms are plain Tab stops (84 on Elections after the heading). S1: sticky "On this page" index and an `h3` per issue group. S2: panels build on demand from one JSON block, and only the 183 a reader can open ship: 1.49 MB, 220 KB gzipped. S3: the step controls pin above the phone drawing. S4: done. P1: the X badge is gone. P2: section heads 40/44, counts and card names 22/26, headings balanced, the doubled period fixed.

**Evidence and brand.** S1, S2, S3: done. Items 3 (the `fix` note dropped), 4 (tint and shadow gone) and 6 (only R-01's points on R-01's drawing) done. I kept "R-02 aims here" and "R-03 aims here" on the R10 page, which the civic educator asked others to borrow; the red legend now names them.

**Reader panel.** First screen and phone map: fixed as above. The headline no longer leads with the finding.

**Creative director's must-fixes.**
- The paragraph under "The full map" no longer states graded links as fact. It is built from the names of L01, L02, L25, L51 and L03, each with its grade ("political spending can tilt policy toward donors (plausible)"). Phones read "Read the parts from top to bottom" and "After Policy, the return line leads back to Wealth".
- How to read prints "A plus sign does not mean the change is good."
- In all 16 everyday answers, each sentence with a figure is followed by its source (title, publisher, year), taken from the V7 claim that carries the same figures (`work/extract/atlas-v7-data.json`). One figure, the 7.65% payroll tax in PW10, has no claim in V7, and the page says so.

**For Dustin.** L23's V7 name fights its minus sign (S4). "Democratic quality" may read as a party label. The "one documented connection" line comes from his dark atlas.

**Left.** Dim Newsprint stays the secondary ink (7.26:1). With the panel open, the 1312 px map scrolls sideways inside its region.

## Change log

Created:
- `work/boards/phase-2/atlas-editorial/04-night-edition/build_system.py`
- `work/boards/phase-2/atlas-editorial/04-night-edition/20261105_Editorial-04-Night-Edition.html`
- `work/boards/phase-2/atlas-editorial/04-night-edition/20261105_Editorial-04-Night-Edition-Verify-Results.json` and `-Check-Results.json`, written by the checks
- `work/boards/phase-2/atlas-editorial/04-night-edition/captures/`: 18 captures from the check, 5 color captures and 5 interaction states (refreshed after the fix pass)
- `work/handoffs/phase-2/20261105_Editorial-04-Notes.md`

Modified: none outside the folder. Nothing was committed.
