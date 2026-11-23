# Chat 12 engineer notes: the atlas kit (Engineer A)

Engineer A, chat 12's fix pass, November 23, 2026. Brief: `work/handoffs/phase-4/20261123_Chat-12-Fix-Brief.md`, section 3.2. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/6f635cd3-ba95-5230-9089-d140c7cc1cf8/scratchpad/c12/fix/engineer-atlas/`. Started 17:48:56 UTC (`date -u`).

Status (18:08 UTC): the Musts are coded in the kit and building in scratch; the in-place run order follows once the scratch build's checks pass. The data lead's R19 to R28 (17:55) and the editor's turn 1 keys (18:07) are wired.

## Routine calls

- D4-xxx | The stepper's crop name moves to a wrapper outside `[data-oa-stepper]` (`.wa-stw`), not to a new attribute | Chapter 18's script reads `data-oa-part` only inside the stepper's root, and the kit's crop code reads `data-oa-part`, so one wrapper fixes the spoken line and keeps every crop key (AX-1)
- D4-xxx | The atlas test's T11 counts a step's hold from the line chapter 18's script would write (its `part()` and `count()` read the same way), and a drawn state's status line must equal it | AX-1: the plate and the page can no longer disagree; a plant puts the part name back on the root
- D4-xxx | The working home page draws all 16 answers, each hidden until its question is pressed; a frame draws the pressed question's answer alone | R19, item 4: 16 answers add about 11 KB to the export and nothing to a plate, since a frame drops hidden markup
- D4-xxx | A chip in a table cell or inside stored text takes its record's stored name as its link's description (`aria-describedby` to one hidden list of names at the end of main); a chip in the page's own sentences takes the name in quotation marks at its first mention | R22, items 1 to 3: stored text is never changed (DR-37), and a 23-row table keeps its cells short
- D4-xxx | The kit prints straight marks from the model as the typographer's pair in every text node of main and in the tab title, never in an attribute, a style or a script | DF1, CR-4 and the fix brief's section 2; the exports' stored data stays as stored
- D4-xxx | The figure step reads every module from source (an empty `sys.pycache_prefix` for the run) | PR-S4: a cached `.pyc` hid `atlas_concepts_common.py` from the plates' inputs
- D4-xxx | The views list is written open with its button hidden, and the atlas's script closes it; the questions, the switch and the stepper's buttons wait for `data-wa-live`; with scripts off every answer shows under its question; a frame draws the scripted state | AX-8: every view reachable with scripts off, and no control that does nothing

## Words for

## Done

## Requests

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Tested

## Not tested
