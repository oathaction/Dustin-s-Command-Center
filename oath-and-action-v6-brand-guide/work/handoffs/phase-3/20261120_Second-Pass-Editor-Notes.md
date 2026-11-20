# Second pass, editor notes

Written November 20, 2026, by the editor. Brief: `20261120_Second-Pass-Brief.md`. Items in order: RS-1, RS-6, RS-2, RS-4, RS-5.

## Status

Started 16:38 UTC. RS-1 in at 16:43 UTC, proved by a strict build. RS-6 in at 16:45 UTC; its generator's check passes and a strict build is clean. Working on RS-2 next.

HANDOVER: phase3_ch14_complex_build.py is free

Message for the main session (16:45 UTC): RS-6 is in and `phase3_ch14_complex_build.py` passes its own check, so the engineer can take the file for CR-S23 now; I will not edit it again in this pass.

## Fixed

### RS-1 (Must): the six tracker alts carry every word their pictures hold

- **What changed.** Each of the six alts now opens with the plate's label and title ("Illustrative. Where three ballot measures stand.", the rescore's form) and closes with the key as the plate prints it: its step heading and names ("The six steps: 1 Filed, 2 Title and summary, ...") and then "What the marks mean:" with each mark's word and shape ("Done, a filled circle; Never happened, the fine ring under a slash"), in the key's own order. The shapes are Rule 11.2's words. A new helper, `alt_key()`, builds that last part from the same step names and mark list the key draws, so the two cannot drift. The correct plates' first sentence now reads "The plate is 360 px wide on Newsprint and draws each state ballot measure as six numbered steps with the bill tracker's marks." The inner "Illustrative" moved to the head, so the label is heard once, first. Each failure alt keeps the maker's fault sentences and "Failure case: do not publish." first, as the plate prints its band; s-11-12-failure also gains the states its marks draw ("Steps 1 to 3 are done, step 4 is where the request is now, and steps 5 to 7 are not yet reached.").
- **Stages:** `s-11-10-correct`, `s-11-10-failure`, `s-11-11-correct`, `s-11-11-failure`, `s-11-12-correct`, `s-11-12-failure` (Rules 11.10, 11.11 and 11.12; the brief's table says "Rules 11.8 to 11.11", but the chapter numbers these plates 11.10 to 11.12).
- **File:** `work/build/scripts/phase-2/apply_systems_ch11.py` (`MARK_SHAPE`, `alt_key()`, `s_11_10()`, `s_11_11()`, `s_11_12()`). Output changed: `work/build/guide/specimens/manifest-systems.json`, the six `alt` fields only. No fragment changed: the six `.html` files are byte for byte as committed.
- **Proof.** The generator ran clean (exit 0) before the edit with no diff, then after it. D3-2153's test (the build's own `picture_words()` and `alt_words()`) finds no word missing from any of the six alts. Strict build to my scratch folder, before and after: exit 0, 0 warnings both times; `pictures.hidden` 95 to 101, `pictures.open` 321 to 315; the stages that left `open_stages` are exactly the six above, and none joined.
- **Bytes, plate in the page, before and after:** s-11-10-correct 12,094 to 12,321; s-11-10-failure 7,056 to 7,321; s-11-11-correct 10,939 to 11,117; s-11-11-failure 6,081 to 6,343; s-11-12-correct 9,744 to 10,054; s-11-12-failure 7,316 to 7,661. Chapter 11 505,397 to 506,984 of 550,000. Page 12,174,060 to 12,175,647.

### RS-6: Loop R10's first step prints its start once

- **What changed.** The step said "Start at seats with little electoral competition, and suppose they rise." and then "Seats with little electoral competition rise, so how often the primary decides the winner goes up." The supposition line still carries the start, and the step's line now reads "So how often the primary decides the winner goes up.", the rescore's words, in Rule 14.143's cause-first form with the cause in the supposition. The status line hears it the same way: "Loop R10, step 1 of 4: Start at seats with little electoral competition, and suppose they rise. So how often the primary decides the winner goes up. Connection L08 ...". The step's hold drops from 16,500 to 15,000 ms, by the script's own formula from the shorter status line.
- **The failure plate keeps its words.** Rule 14.143's failure plate lists the seven steps with no supposition beside them, so its fourth item would have opened on "So" after Loop B4's last step and read as if B4 caused it. Each step now also carries its whole line (`whole`), and the failure list prints that, so `s-14-143-failure.html` is byte for byte as committed and its one fault stays as captioned.
- **The direction check still runs on every step.** For a step with a supposition, the check (near line 1364) reads the cause from the supposition ("... suppose they rise") and the effect from the line after "So", and the walk's direction and "can" are tested as before. A new hold in `walk_steps()` stops the build if the supposition and the first step's direction ever disagree, and a new check fails if Loop R10's first step names its start twice or loses the rescore's line.
- **File:** `work/build/scripts/phase-3/phase3_ch14_complex_build.py` (`walk_steps()`, the failure list in `rule_14_143()`, the checks). Output changed: `work/build/guide/specimens/s-14-143-correct.html` only.
- **Proof.** `--check` before the edit: 10 of 10 files current. After: the generator ran with 0 faults and wrote one file; `--check` then reads 10 of 10 current (exit 0). Strict build to my scratch folder: exit 0, 0 warnings, pictures 101 hidden and 315 open, unchanged by RS-6.
- **Bytes.** Fragment `s-14-143-correct` 25,269 to 25,223; the plate in the page 27,451 to 27,405. `s-14-143-failure` unchanged at 9,134 (10,655 in the page).

## Not fixed

## Calls

## Requests

## Tested

## Not tested
