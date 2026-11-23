# Chat 12 design director notes

Design director, chat 12's fix pass, November 23, 2026. Brief: `work/handoffs/phase-4/20261123_Chat-12-Fix-Brief.md`, sections 1, 2, 3.3, 3.6 and 4. Started 17:51 UTC (`date -u`). Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/6f635cd3-ba95-5230-9089-d140c7cc1cf8/scratchpad/c12/fix/design-director/`.

Turn 1 (this turn) files: `work/build/scripts/phase-4/phase4_ch16_build.py` and `phase4_ch20_build.py` outside their word fields, with their outputs; `work/handoffs/phase-4/20261121_Web-Page-Specs.md` and `20261122_Atlas-View-Specs.md`; this file. The editor holds `phase4_ch21_build.py` this turn. Turn 1 items: CR-2, CR-17, CR-20 with CD-S9, CR-22, CE2, CD-S7, AX-7 (chapters 16 and 20), and the atlas engineer's specs for CD-S1, CD-S2 and CD-S3.

## Routine calls

## Rulings

## Contracts

- **DD12-C1, for the atlas engineer: CD-S1, CD-S2 and CD-S3, landed 18:02 UTC** (`date -u`) in `work/handoffs/phase-4/20261122_Atlas-View-Specs.md`, section 15. In short:
  - **15.1, CD-S1 (A11, A17, A20 from 75em):** the drawing's last ink and the key end at y 880 or above at 1440 by 900, in the load state and the plates' pressed state. Head band padding 16 and 16, the intro in `oa.type.body-small` at cols 5 to 10 (104 px with three lines); 16 px above the drawing; key 12 px under it. Drawing rows 44, 44, 204, 96, 92, 44 (closed 524, was 578), with the moved lane offsets listed there; core box 196 wide with 12 px side padding (172 inner), question and lit line balanced, counts as two fixed lines (CR-3), R24's labelled second line at most two lines. Sum 878.
  - **15.2, CD-S2:** a crop is cut on both axes: the union of every element carrying the part's name, plus 24 px of the page each side, clipped to the page; its frame width is that box's width. 680 px or less shows at true size; wider shows reduced with its scale stated by the plate. New parts: `pair` (A11 and A17, on the Wealth and Voice boxes), `hub` (A11, the pressed question's hub column), `art` (A12's "Where it acts" heading and drawing block; A14's loop drawing block), `sheettop` (A18, the sheet band and its first three connection rows); `stepper` moves to the stepper's own block and `chooser` to the list alone; A20's answer block takes `max-width: 37.37rem`. New frames: A17 `1440-light-pair`; A11 `1440-light-pair`, `1440-light-hub`; A12 `1440-light-art`; A14 and A13 `390-light-rowl14`; A18 `390-light-sheettop`; A14 `1440-dark-art`. Existing keys keep working until my turn 2 rewires the plates.
  - **15.3, CD-S3:** a new window width for A16 alone, `680-light-marks`, cropped to `marks` (the five groups); fallback `390-light-marks`.
  - **15.4:** a spec line for CR-8 and CD-S10, if the engineer takes them (the loop at 1.5 times chapter 15's geometry from 64em, weights unchanged, the chooser under the read-aloud column).
- **DD12-C2, the frame names' form (AX-7, for the engineer and the editor):** every frame's name (its SVG's `aria-label`, AL-18) says what that frame shows that its plate's other frames do not. A whole page keeps AL-18's short form ("Loop R18’s page in our systems atlas. At 1440 px, on Newsprint."). A crop or a state names the part and the state first, then the width and the ground: "The everyday questions, with “Why can the same care produce different bills?” pressed. At 1440 px, on Newsprint." The words are the editor's (`--page-words`, by part key); the kit composes them. Chapter 20's state frames follow the same form (see "Done", AX-7).

## Words for the editor

## Done

## Requests

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Bytes

## Tested

## Not tested
