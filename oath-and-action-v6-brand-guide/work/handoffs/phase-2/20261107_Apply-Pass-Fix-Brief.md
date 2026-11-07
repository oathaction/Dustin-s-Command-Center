# Brief: fix pass after the apply pass review

Oath & Action Edition 06, Phase 2, November 7, 2026. Written by the main session. Three reviews read the page after round two:
- `20261107_CD-Review-Of-Apply-Pass.md` (CD-)
- `20261107_Apply-Pass-Red-Team-Brand-Evidence.md` (BE-)
- `20261107_Apply-Pass-Red-Team-Craft-Access.md` (CA-)

Read all three in full before you start. Every rule in `20261107_Apply-Pass-Brief.md` still binds.

**Must fix** items block the changes board, and each one is fixed in this pass. Fix **Should fix** items in this pass when the fix stays inside your files and changes no approved decision. Otherwise carry the item to stage B and say why in your notes. **Notes** are yours to take or leave. Anything that would change an identity master, a locked element or wording Dustin approved goes to him as a question with a recommendation, and you change nothing for it.

## Owners

**Identity designer: chapters 03, 04, 08 and the proofs.**
- CD-M1 with CA-S4, the end mark. Measure B and the capitals again at 17 px body text, and correct every figure on the page. Set B as close to cap height as B's minimum size allows. Then draw two plates at true size, in Newsprint, for Dustin's changes board only, to `work/boards/phase-2/apply-pass/end-mark/`:
  - (a) B at the text's cap height, as an exception to B's minimum size for the end mark alone.
  - (b) B at its minimum size.
  Each plate shows a paragraph's last line at 17 px and at 19 px.
- L6 for the board. Draw L6 as it is and L6 without its four pillar dots, side by side at L6's minimum width, to `work/boards/phase-2/apply-pass/l6/`. The guide's L6 stays as drawn (D2-403).
- CD-S4, CD-S7, CD-S8, CD-N3, CD-N5, CD-N7, CA-S1, CA-S2, CA-S5, CA-S9, CA-S10, CA-S11, and CA-S6 in your chapters.
- CA-S1, the lockmark drawn at two weights. If the fix needs a master change, write it as a question for Dustin and draw the comparison to `work/boards/phase-2/apply-pass/lockmark/`.

**Systems designer: chapters 05, 06, 07 and 11.**
- BE-01. Scope the hearing wording to what is true. Many state legislatures take public testimony at hearings. Congressional committees hear the witnesses they invite (House rule XI, Senate rule XXVI). Step 2's line, Rule 11.1's reason and step 5's line must say this plainly for both kinds of bill. Coordinate the wording of the H.R. 7008 card's step 2 with the editor through your notes.
- CA-M1. No plate may hide its point at true size, and Fit to window may never set type under 13 px. Redraw `s-11-1-correct` and the three 1,024 px extras so step 6, in both its Governor and President forms, shows within the chapter column at true size, or split them into plates that fit.
- BE-07, BE-08, BE-09, CD-S3, CD-S6, CA-N1, CA-N2, CA-N3, CA-N5, CA-N6, CA-N7, CA-N9, and CA-S6 in your chapters.

**Editor: chapters 01 and 02.**
- BE-02. Rule 01.11's correct plate must match the rule as Dustin approved it. Give the counts the record supports, from our systems atlas, with their source and grade. Or, if no count can be supported, recast the plate so it claims only what it shows. Ask the research lead's report, not memory.
- CA-S3. Draw the H.R. 7008 card on chapter 11's story card geometry.
- BE-03, BE-04, BE-05, BE-06, BE-10, BE-11, BE-12, BE-13, CD-S1, CD-S2, CD-N4, CD-N6, CA-S7, CA-S8, CA-S12, CA-N4, CA-N11, CA-N12, and CA-S6 in your chapters.

**Engineer: build, shell, checks.**
- CD-N1, CD-N2, CA-N8, CA-N9 (the switch), CA-N10.
- Chapter 09 is renamed "Pillar icons" in the chapter list (CD-S5). This is a routine call by the main session, D2-415, using Dustin's own words in DR-105 and DR-111.
- Add a check that fails any Fit to window plate whose smallest rendered type falls under 13 px. Self-test it with a planted fault.

## Hand back

Rebuild your chapters, then run `python3 -I work/build/scripts/phase-2/guide_build.py --strict` and `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`. Others rebuild the same page while you work. If the build fails in a file you do not own, wait a minute and retry.

Add a "Fix pass" section to your apply pass notes with:
- each item ID and what you did, or why you carried it
- routine calls as D2-xxx lines
- questions for Dustin with a recommendation
- Tested and Not tested, kept apart

Do not commit or push. Reply in 150 words or fewer.
