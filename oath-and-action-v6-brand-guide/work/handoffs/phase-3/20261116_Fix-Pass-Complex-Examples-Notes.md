# Fix pass notes: complex examples maker, Rules 14.142 to 14.144

Oath & Action Edition 06, Phase 3, the fix pass after the review of rounds 4 and 5, chat 7, November 16, 2026. Written by the complex examples maker (a general-purpose agent briefed as a senior graphics editor) for `work/handoffs/phase-3/20261116_Rounds-4-5-Fix-Brief.md`, calls 2 and 3. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f55a08bf-cdcf-539d-a683-426e26f4f342/scratchpad/c07/fix/complex-examples/`.

Codes routed to me: CE-M1, CE-S13, CE-S14; ST-M1, ST-S1, ST-S2, ST-S8; DF-3, DF-4, DF-6, DF-7; NB-M1 (group 18's line, with the editor), NB-M3, NB-S1, NB-S2.

## Status

- 17:14 UTC: **The data lead's R2 to R5 and the editor's words for me are applied in the generator, written, and every check passes** (CE-M1, ST-M1, ST-S1, CE-S13, ST-S2, DF-3, DF-7, NB-S1, and the words of DF-4 and CE-S14 confirmed). Generator `--check` 10 of 10 current; figure checks 44 of 44 with the drawing measure. Waiting on: the research lead's source line (ST-S8 and R4b's sector series, my request 1), the browser load rule for NB-M3's computed strokes and the captures, the kit build of S96, a fresh strict build. NB-M1's group 18 line is the editor's own file (its notes say it changes it).
- 17:07 UTC: **NB-M3 (with CD-M1), NB-S2, DF-6, DF-4 and CE-S14 are in the generator and written; the strict build passes.** Generator run (5 files written, then 1 for CE-S14), its `--check` 10 of 10 current with every new check passing; the engineer's `phase3_ch14_build.py` and the strict build run in a scratch mirror of the project (`mirror/`, so no other owner's file is written in the real tree): 0 faults; strict build exit 0, 0 warnings (`b1/guide.html`, 12,109,716 bytes). Browser proof of NB-M3 waits on the load rule (two browsers open at 17:05 and 17:06). Waiting on the data lead's rulings, the editor's words and the research lead's facts for the rest.
- 17:00 UTC: started (clock read 16:59:21). Read `CLAUDE.md`, the brief, my round 5 notes and every code routed to me in the CE, ST, DF and NB reports. No data lead, research or editor notes for this pass exist yet. Starting with the items that wait on nobody: NB-M3, NB-S2, DF-6.

## Fixed

- **NB-M3 (and the creative director's CD-M1): with Reform R-38 chosen, Connection L39 no longer draws heavy.** Each chooser state's rule for a target of a reform not chosen now also sets its ink case to `stroke:none`, beside the mark, the pill and the head it already reset, so chapter 15's red-target case (`.crt .ak-case`, 6 px ink), which the first reform's targets carry in the markup, cannot outlast the choice. A new generator check fails the plate if any state's rule leaves out the case, the mark, the pill or the head. File: `phase3_ch14_complex_build.py` (`chooser_css`), writing `s-14-144-correct.html`. Proof: generator check passes; the diff adds exactly three rules (`.p:has([value="R-nn"]:checked) [data-oa-for]:not([data-oa-for~="R-nn"]) .ak-case{stroke:none}`); computed strokes in a browser: pending (load rule).
- **NB-S2: the failure figure differs from S96 by the band alone.** It keeps S96's measure line less the margin ("the span both jobs charts share" restored), S14's preliminary note and the three notes S96 takes from S14 whole, in S96's order (average, seasonal adjustment, the window's reason); the on-plot latest label is gone (the correct plate dropped it under DD-E3, so the pair differed twice; the craft reader saw the same); and its source line is the sidecar's plain line, with no margin sentence, since the drawing leaves the margin out (ST-M1's second and third points, which need no ruling). The caption itself waits on the data lead (ST-M1). Checks added for each. Files: `phase3_ch14_complex_build.py`, `maker_c_round5_derive.py` (the plain line read into the facts, with a stop if it is no longer the margin line less its margin sentence), writing `s-14-142-failure.chart.json` and `14-142.json`.
- **DF-6: each loop's grade label and gloss sit above its chip and title** on 14.143 (both loops) and 14.144 (Loop R8), as Rule 13.1 sets and Rule 15.15 prints the same two loops. Vertical space is unchanged (the 10 px and 4 px margins trade places), so Loop B4's 96 px drop that aligns the two C3 pills holds. A check fails either plate if a title stands above its label. Files: `phase3_ch14_complex_build.py`, writing `s-14-143-correct.html` and `s-14-144-correct.html`.
- **DF-4: "the text’s ink" in place of "the strongest ink"** in S96's reading guide, alt, key note and phone note and in the failure's alt, the ink word of the approved chart notes (S17, S47; DR-262, D3-914). A check fails S96 or its failure on "strongest ink" and on any of the five places that does not name the text’s ink. The editor reads it (its words govern if they differ). Files: `phase3_ch14_complex_build.py`, writing `s96.json`, `s-14-142-failure.chart.json`, `14-142.json`.
- **CE-S14: each card's band prints the atlas's definition after its word**, as Rules 15.11 and 15.20 do: "Rules: “Changes incentives, penalties and constraints: who may run, how votes count, what firms may do (level 5).”" A check fails a card whose band is bare. File: `phase3_ch14_complex_build.py`, writing `s-14-144-correct.html`.

## Not fixed

## Calls

| call | reason |
|---|---|

## Requests

## Tested

## Not tested
