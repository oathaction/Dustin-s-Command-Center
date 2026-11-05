# Editorial system 02, Economist Register: notes

Oath & Action Brand Guide, Edition 06. Phase 2, November 5, 2026. Maker's notes for the editorial round. Page: `work/boards/phase-2/atlas-editorial/02-economist-register/20261105_Editorial-02-Economist-Register.html`, built by `build_system.py` beside it.

## The idea

The atlas as a register you read across, the way a weekly's data desk sets a table. The overview opens on a headline, the atlas in five figures, and a compact circuit: five named boxes in a row with the count of connections each passes to the next, the counts that run back, and the return from Policy to Wealth. Under it sits the register, one row per part: plain name over formal title, its question, every variable as a chip, four counts, the evidence mix as a textured bar, and its main loop. Opening a row unfolds the part's story, its main loop drawn as a named chain, and the fix aimed at it on a Prussian card. Every chart carries a sentence title, a measure line and a source line under a Charcoal rule with a short tab. Selecting a variable lights the variables it connects to, so the register shows relationships without drawing a line.

## The views

- **Overview.** Headline, deck, figures, key; the circuit (every flow between the eight parts counted, with each count opening its connections); the register with Elections open; "Start from your own bill" with the 5 hubs and 16 questions; then an index of all 23 loops. The register title names a finding from its own columns: Policy has the thinnest evidence, 6 of 17 connections documented or well supported.
- **Elections.** Story and figures; the five variables with icon, description and "a higher value means"; the 8 connections in, 7 out and 5 inside, grouped by part, each drawn in its texture; the seven loops as chains; the 39 issues as a table grouped by topic with each real-world example, each opening its full record; the ten reforms with one column per outcome family.
- **Loop R10.** The chain at full size, read from the top, with each step's name, sentence, sign word, grade with gloss and delay, the weakest step L53, and R-01's three targets in the view's one red. Beside it: the read-aloud line, V7's own sentence, and a step-through. Below: evidence, qualification, the Alaska case, and the three reforms (selecting R-02 or R-03 moves the red).
- **Reform R-01.** Summary with the no-position line; the R10 chain with the targets in red; problem and what it changes; effects table with categorical marks, never summed; routes with feasibility and check dates; both evidence grades; tradeoffs, failure risks, success measures; status with the editor's disclosure in full.
- **All loops.** The 23 chains grouped by home part, each with plain name, V7 title, kind, stations, weakest step, delay, direction and reform count; R2, R16 and the three sketches disclosed.
- **How to read.** The five rules of the shared language, each with real connections as specimens and model counts.

## Decisions

- **Loops drawn as a vertical chain.** It reads aloud top to bottom, fits a 310 px card and a phone unchanged, and keeps one grammar from card to full size.
- **Main loop rule.** The loop with the most stations in the part; ties go to the loop more reforms aim at. Printed under the register.
- **Fix rule.** The main loop's first-listed reform, or with no loop the reform with the most targets in the part. Printed under the register.
- **Color is the layer, read as layers of meaning.** Charcoal is the system, Stone the context, Prussian the fix, red where a fix acts. Concept 00 is not on disk; this reading needs Dustin's confirmation.
- **Red only on the loop and reform views.** Both show where R-01 acts, as the brief's section 3 and rule 7 ask. Selection elsewhere goes to ink.
- **Evidence bars filled with the line textures.** Each grade's bar segment uses its own pattern, so the mix survives grayscale.
- **Disclosure in full.** The R-01 status prints `reforms['R-01']['disclosure']` from the shared dataset word for word, and the script asserts it is present. Open item: R-02, R-39 and R-47 also carry disclosures and appear on this page (panels, the Elections reform table, Technology's fix card); per the main session's instruction only R-01 changed this round.
- **Icon metadata renamed.** Civic Line files carry `data-part="base|accent"`, which the November verifier reads as an atlas part. The inline copy renames that attribute to `data-cl-part`; the drawing is unchanged. Other makers who use icons will hit the same failure.
- **Kit departures.** Three small patches in `atlas-kit.js`: selection never takes red; red marks only on views flagged `data-red-ok`; a view with a wide and a phone drawing selects the copy on screen.
- **Headlines are studio drafts**, built from model sentences and counts.

## Self-score

- Craft, 4: on a 12-column grid, labels clean at 1x; the wide circuit scrolls between 900 and 1440 px.
- Clarity, 4: names, questions and counts answer the ten-second questions; untested with readers.
- Brand fidelity, 4: locked palette and type, inlined masters, one red job per view.
- Usefulness, 5: every variable, flow, issue, reform and loop is one click from the overview.
- Evidence honesty, 5: grades in bars, textures and words; disclosures and selection rules printed.
- Accessibility, 4: 0 axe violations, keyboard paths, rings on drawn items; no screen-reader test.
- Beauty and distinctiveness, 4: a register that reads as a finished weekly table; the circuit is plain by design.

## Tested

- `atlas_concepts_verify.py --selftest`: PASS; all six planted errors caught.
- `atlas_concepts_check.js`: PASS, 6 views at 1440 and 390 px, 0 failures, 0 axe violations, no text under 13 px, no sideways scroll, one red job on the loop and reform views only.
- Viewed every view at 1440 and 390 and the grayscale captures; states: a selected variable with its panel, a selected flow, the stepper at step 2, R-02 moving the red, the phone sheet, a selected issue and loop.
- Keyboard: Tab into the circuit, arrow keys between boxes, ring visible.

## Not tested

- Real screen readers, Firefox, Safari, real phones, 200 percent zoom.
- Widths between 391 and 1439 px beyond the layout rules.
- Reduced motion, by eye.
- The ten-second test and the wall test with readers or in print.

## Change log

Created:
- `work/boards/phase-2/atlas-editorial/02-economist-register/build_system.py`
- `work/boards/phase-2/atlas-editorial/02-economist-register/20261105_Editorial-02-Economist-Register.html`
- `work/boards/phase-2/atlas-editorial/02-economist-register/20261105_Editorial-02-Economist-Register-Verify-Results.json` and `-Check-Results.json`, written by the checks
- `work/boards/phase-2/atlas-editorial/02-economist-register/captures/`, 18 captures written by the check
- `work/handoffs/phase-2/20261105_Editorial-02-Notes.md`

Modified: none outside the folder. Nothing was committed.
