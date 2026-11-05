# Editorial system 02, Economist Register: notes

Oath & Action Brand Guide, Edition 06. Phase 2, November 5, 2026. Maker's notes for the editorial round, updated after the fix pass. Page: `work/boards/phase-2/atlas-editorial/02-economist-register/20261105_Editorial-02-Economist-Register.html`, built by `build_system.py` beside it.

## The idea

The atlas as a register you read across, the way a weekly's data desk sets a table. The overview opens on a headline, the atlas in five figures and a compact circuit that names all eight parts with their questions: outside forces push down on five parts in a row, Your household and Technology sit beneath the parts they trade with most, and the return from Policy to Wealth runs round the outside. Under it sits the register, one row per part: plain name over formal title, its question, every variable as a chip, four counts, the evidence mix as a textured bar, and its main loop. Opening a row unfolds the part's story, its main loop drawn as a named chain, and the fix aimed at it on a Prussian card with its disclosure. Every chart carries a sentence title, a measure line and a source line under a Charcoal rule with a short tab. Selecting a variable lights the variables it connects to, so the register shows relationships without drawing a line.

## The views

- **Overview.** Headline, deck, figures; the circuit with every count opening its connections, the main flows each with one example connection, and a line naming the flows left undrawn; the register with an evidence key and Elections open; "Start from your own bill" with the 5 hubs and 16 questions; an index of all 23 loops.
- **Elections.** An "On this page" bar; the five variables with icon, description, why it matters and "a higher value means"; the 8 connections in, 7 out and 5 inside, grouped by part; the seven loops, R10 and B4 first, under a sentence on where they meet; the 39 problems by topic with real-world examples; the ten reforms, each with what it would do and any disclosure.
- **Loop R10.** The plain summary and the read-aloud line under the title; the chain at full size, R-01's three targets in red; a step-through directly under the drawing on a phone; evidence, qualification, the dated Alaska case; the three reforms with what each does.
- **Reform R-01.** A disclosure box near the top, stance first; where it acts; effects in words; routes; who decides, the law, implementation and costs; both evidence grades; tradeoffs, failure risks, success measures, alternatives; status.
- **All loops.** The 23 chains grouped by V7's home area, each with its first summary sentence; R1 carries its qualification.
- **How to read.** The five rules of the shared language with real connections as specimens.

## Decisions

- **Loops drawn as a vertical chain.** It reads aloud top to bottom and keeps one grammar from card to full size.
- **Main loop rule.** The loop with the most stations in the part; ties go to the loop more reforms aim at. Printed under the register.
- **Fix rule.** The main loop's first-listed reform, or with no loop the reform with the most targets in the part. Printed under the register.
- **Color is the layer, read as layers of meaning.** Charcoal the system, Stone context, Prussian the fix, red where a fix acts. Concept 00 is not on disk; needs Dustin's confirmation.
- **Red only where R-01 acts**, on the loop and reform views. Another selected reform lights its targets in ink.
- **Evidence bars filled with the line textures**, so the mix survives grayscale.
- **The disclosure quotes the dataset word for word**, so "Oath & Action" appears in live type there and nowhere else. Brand rule 13 and D2-80 meet here; Dustin's call.
- **Icon metadata renamed.** Civic Line files carry `data-part="base|accent"`, which the verifier reads as an atlas part; the inline copy renames it `data-cl-part`. The drawing is unchanged.
- **Kit departures.** Patches in `atlas-kit.js`: selection never takes red; red only on views flagged `data-red-ok` and only for that view's reform; the copy of a drawing on screen is the one selected.
- **Headlines are studio drafts**, built from model sentences and counts.

## Self-score

- Craft, 4: on the grid at 1440, 390, 360 and 320; the panel reflows the page.
- Clarity, 4: all eight parts and their questions on the first screen; untested with readers.
- Brand fidelity, 4: locked palette, inlined masters, one red job.
- Usefulness, 5: every variable, flow, problem, reform and loop is one click from the overview.
- Evidence honesty, 5: disclosures wherever a reform is argued, dated ballots, grades in words and textures.
- Accessibility, 4: 0 axe violations at three widths, 44 px phone targets, skip link, aliases; no screen-reader test.
- Beauty and distinctiveness, 4: a finished weekly register; the circuit is plain by design.

## Fix pass

Civic education:
1. Overview R-01 card: stance and disclosure added in a box under its title. Every row still loads with Elections open.
2. R10: the summary sits under the title, the read-aloud line after it.
3. Elections reforms: each row adds its first summary sentence and any disclosure.
4. R-01: disclosure box near the top; who decides, legal authority, implementation, costs and alternatives added.
5. Circuit: all eight parts drawn as named boxes; one example connection named for each main flow.
6. Elections: a sentence on the four loops through risk of losing office, R10 and B4 meeting there, and B4's "only where seats are competitive"; R10 and B4 lead the cards.
7. "Prussian tab" now reads "the dark tab".
8. The Touches column is gone; the panel names the touched conditions.

Interface:
- M1: step sentences follow the running sign ("Less risk of losing office means more incumbents control election rules").
- M2: chips, rows, buttons and standalone links at 44 px under 900 px.
- S1: each problem is its own Tab stop. S2: all eight parts lead the overview. S3: "On this page" bar and topic headings. S4: the stepper sits under the phone drawing.
- P1: counts underlined. P2: read-aloud and step words set in scale styles. The 8 px stroke is the memo's keyline case (two 1 px edges under a 6 px red line); left as specified.
- X1 to X6: scroll into the band above the sheet; arrow-key hint in the readout; phone figures drawn at 280 units; a skip link that focuses the `h1` and keeps the hash; `#area-{id}` aliases with a visible status; the panel as a column the page makes room for.

Evidence and brand: disclosures on the overview cards, Elections rows, R10 picker, reform, loop and issue panels (D2-80); every November 3 sentence opens "As of October 15, 2026,"; loops grouped by V7's home area, R4b with Elections; the main-loop rule says stations; the live-type credit removed; Stone and Newsprint at full strength; the swatch marked a specimen; the skipped flows named under the circuit; sign tags and ticks stay ink; "fewer" for countable things; effect qualifiers rewritten as words ("none to small negative (short run)"). S4 (L23's name against its sign) is Dustin's call.

Reader panel: counts carry a legend in the circuit and nouns in the example list; stance and disclosure sit together; rows with no loop say which parts their connections feed.

Fixes every system makes: items 1 to 13 done; the phone holds all eight parts within two screens with the figures strip folded away there.

Creative director's must-fixes:
1. The "R-01" tabs on Loop R10 and Reform R-01 are Charcoal wherever they sit beside red; Prussian stays only for reform cards elsewhere.
2. The overview readout now says each question as "Title: question", so "influence" and "Which" no longer run together.
3. Every figure in the 16 everyday answers carries its source (title, publisher, date) right after its sentence. The script reads V7's claims from `work/extract/atlas-v7-data.json`, matches each figure to the claim that carries it (the pathway's own claims first, a rounded match where the unit agrees, as with "about 12 cents" and V7's 11.8 cents), and stops the build if any figure has no source. 27 figure sentences in 15 answers matched; PW13 has none. One figure, PW10's 7.65 percent payroll tax, is sourced from a claim filed under PW11 (CL1467), since no PW10 claim states it.

## Tested

- `atlas_concepts_verify.py --selftest`: PASS; all six planted errors caught.
- `atlas_concepts_check.js`: PASS, 6 views at 1440, 390 and 360 px, 0 failures, 0 axe violations.
- A script at 320 and 360 px: no text under 13 px, no overflow. A text audit: every ballot sentence dated, no live-type name outside the disclosure.
- States: panel column with a picked variable and flow, phone sheet over C5, `#area-a`, an unknown hash, the R10 phone stepper, skip link and arrow-key hint by keyboard.

## Not tested

- Real screen readers, Firefox, Safari, real phones, 200 percent zoom.
- Reduced motion, by eye.
- The ten-second test and the wall test with readers or in print.

## Change log

Created:
- `work/boards/phase-2/atlas-editorial/02-economist-register/build_system.py`
- `work/boards/phase-2/atlas-editorial/02-economist-register/20261105_Editorial-02-Economist-Register.html`
- `work/boards/phase-2/atlas-editorial/02-economist-register/20261105_Editorial-02-Economist-Register-Verify-Results.json` and `-Check-Results.json`, written by the checks
- `work/boards/phase-2/atlas-editorial/02-economist-register/captures/`, 18 captures written by the check
- `work/handoffs/phase-2/20261105_Editorial-02-Notes.md`

Modified in the fix pass: the build script, the page, the check results and captures, and these notes. Nothing outside the folder; nothing committed.
