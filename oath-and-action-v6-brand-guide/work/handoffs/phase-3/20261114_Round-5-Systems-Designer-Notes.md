# Round 5 notes: systems designer, Rules 15.22 to 15.25

Oath & Action Edition 06, Phase 3, round 5, November 14, 2026. Written by the systems designer (a general-purpose agent briefed as the designer who drew chapter 15) under `work/handoffs/phase-3/20261114_Phase-3-Round-5-Brief.md`, contracts R5-5, R5-6 and R5-8. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/7633c399-b692-5041-be92-a87ecd098fbf/scratchpad/phase-3/round-5/systems-designer/`.

## Status

- 01:43 UTC. Started. Read `CLAUDE.md`, the round 5 brief in full, my round 1, 2 and 4 notes, the generator and chapter file as they stand, the workflow sources file, Phase 0's reconciliation table and the November 13 rerun. Baseline run of `phase3_ch15_build.py`: every check passes, 21 rules, 43 plates, and no file of mine changes. Starting 15.22, 15.24 and 15.25 (group 5 and group 6) while the data lead's rulings (e) and (g) and the research lead's "Facts for owners" land. 15.23 waits on the tracker designer.
- 01:46 UTC. **R5-8 applied** in `phase3_ch15_build.py` with one function (the tracker designer's map and pattern, `(?<![\d.])11\.1[0-6](?!\d)`): three matches, lines 2316, 2332 and 3583, each "Rule 11.14’s plate" to "Rule 11.16’s plate" (the loop stepper's plate). The generator ran clean twice; the second run changed nothing (hashes of the chapter file, the manifest and every `s-15-*` plate), and `git diff` on my files shows those three lines in the generator and the same three in `15-systems-graphics.json`, no plate changed.

## Summary

To come.

## Contracts

To come: which drawing functions in `phase3_ch15_build.py` the complex examples maker may import read-only.

## Routine calls

- D3-xxx | R5-8's map is applied in `phase3_ch15_build.py` by one regular-expression function over the source, never a chain of replaces | The tracker designer's contract; a chain would carry 11.14 on to 11.16 and then 11.18

## Requests

## Tested

## Not tested
