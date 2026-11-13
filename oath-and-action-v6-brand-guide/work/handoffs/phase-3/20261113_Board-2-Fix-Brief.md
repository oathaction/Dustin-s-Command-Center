# Brief: board 2's fix round

Oath & Action Edition 06, Phase 3, November 13, 2026. Written by the main session after the creative director's score of the board's run 6: Craft 3, Clarity 3, Brand fidelity 4, Usefulness 3, Evidence honesty 3, Accessibility 4; 7 Must fix, 12 Should fix (`work/handoffs/phase-3/20261113_CD-Review-Of-Board-2.md`, `20261113_Board-2-CD-Scores.json`). Read the review's "Must fix", "Should fix" and "My view on S12" first; each item there names its owners. Paths are relative to `oath-and-action-v6-brand-guide/`. Every rule of the board 2 brief (`work/handoffs/phase-3/20261113_Board-2-Brief.md`, "Limits") still holds.

## The main session's calls

1. **Panel 1 serves the decision first (B2-M1).** It opens with the five replies Dustin owes as a numbered list, one line each with its recommendation and a same-page link, then the reply line; the five items carry those numbers; everything already answered (DR-254 to DR-258) folds closed under one "Done" heading with its chip (B2-S5). The cover's minutes line states what panel 1 takes to read once B2-M1 lands, measured by word count at 200 words a minute.
2. **S12 (B2-M2).** One row at a 1440 px window (the as-built frame as a reader sees it beside the stacked tile cropped to its drawing), one row at a 1024 px window (the frame in its column beside the stacked tile in its frame), then board 1's plate, the full as-built plates and the phone pair in a fold. The creative director's quoted view becomes its "My view on S12" text, and the data lead's view stays beside it. The 1024 px figures come from the cartographer's measure file only (B2-S8).
3. **Phone codes (B2-M3).** The board says what the guide's 326 px phone drawing shows for S12, S16 and S78, with every phone picture labeled by its drawing width. Coding every state at 326 px is a round 4 guide item, not this round's.
4. **One byte measure (B2-M4).** Every weight on the board is the build report's bytes as placed plus that plate's own frame, measured on the page by the engineer and named once at the top of panel 2. S73 prints its trimmed measure from the final build (13,263 bytes as placed in its report).
5. **R-01's outcome (B2-M5).** The data lead rules whether S03's and S08's notes keep "the unofficial count of November 10" until certification or take the November 12 count now. S03 and S08 are board 1 drawings: if their words change, the board lists the change among the board 1 changes for Dustin's approval. Either way the R-01 item says where the guide prints outcomes and from which count. The guide preview waits for this ruling.
6. **The board reads the current decisions file (B2-M6),** and the build fails, not warns, on a board 1 drawing that differs and panel 1 does not name, and on a "No" in the election table where the test was not applied.
7. **Every "approve as drawn" shows its drawing (B2-M7),** the Newsprint picture panel 2 already holds, linked to the form.
8. **Should fix B2-S1 to B2-S12** as the review writes them.

## Who does what

| Owner | Items | Writes |
|---|---|---|
| Board builder | B2-M1 (layout), B2-M2, B2-M4 (one measure on the board), B2-M6, B2-M7, B2-S2, B2-S3, B2-S5, B2-S6, B2-S8 (labels), B2-S12 | `board_2_build.py`, `board_2_render.js`, the content file, the board folder |
| Data lead | B2-M1 (the five lines), B2-M2 (views), B2-M3 (words), B2-M5 (the ruling), B2-M6 (confirm), B2-S4, B2-S7, B2-S8 (figures), B2-S11 | the decisions file, your notes |
| Editor | every word item: B2-M1, B2-M3, B2-M5 (S03 and S08 notes if ruled), B2-S1, B2-S3, B2-S5, B2-S9, B2-S10, B2-S11; then one read of the rebuilt board's visible text | the content file's words, the decisions file's words, S03 and S08 only under B2-M5's ruling |
| Cartographer | B2-M2 (the stacked tile photographed at its drawing's box at both widths), B2-S2 (the gray half in the same plate at 868 px) | `work/handoffs/phase-3/board-2-pictures/` |
| Engineer | B2-M4 (each plate's own frame bytes measured on the final build's page, written as one JSON the builder reads) | `work/handoffs/phase-3/board-2-pictures/20261113_Plate-Bytes.json` or a file you name in notes |

## Order

1. The data lead rules B2-M5 first and says so in its notes with a UTC time. If S03's or S08's words change, the editor makes the change, the data lead signs it off, and the main session rebuilds and rechecks the guide.
2. The others start at once. The builder reruns as files land, with `--reuse --check`.
3. The main session publishes the guide preview as version 9 after B2-M5's ruling, and tells the builder.
4. The creative director rescores the rebuilt board. Ship at 4 or more on all six with no Must fix.

Log each call as `- D3-xxx | decision | reason` under a "Fix round" section in your notes. Final message under 120 words.
