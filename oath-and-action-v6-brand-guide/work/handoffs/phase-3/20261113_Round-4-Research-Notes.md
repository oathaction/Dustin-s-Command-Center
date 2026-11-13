# Round 4 research notes

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. Research lead (`oa-research-lead`), under `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`, the research lead's row and bullet. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/research/`. Written as I go, since the container can restart.

## Status

- 20:48 UTC. Handed back to the main session before any derived file or ruling (f) landed; the watch is stopped. Still to do when resumed: the data check on each derived file as the makers write it (`scripts/r4_derived_check.py <root> 829d0db8`, then a recomputation for each file, then `data_round0_build.py --check`); the 15.20 facts once ruling (f) names the reforms (from `r4/reform-facts.json`, rechecked against the model); any V7.1 row round 4 raises; the data plan's status lines.
- 20:47 UTC. Data lead's rulings (a) to (c) read; (f) not yet posted. The reform facts table for all 50 reforms is ready in scratch (`r4/reform-facts.json`: 50 reforms, R-35 rejected; 126 route entries, 13 dated; 200 effect values, 38 beyond the seven codes, as the brief's section 14 counts). The common checker for changed data files (`scripts/r4_derived_check.py`, base commit 829d0db8) reads 0 changed tables so far. A watch on the makers' "derive" lines, the data folder and ruling (f) runs every 30 seconds.
- 20:44 UTC. Started round 4 after DR-269 (row 39 done, 20:43; see `work/handoffs/phase-3/20261113_Board-2-Apply-Research-Notes.md`, "Routine calls, DR-269"). Read the round 4 brief in full and the round 4 data plan. Baseline data check, `data_round0_build.py --check`: 125 tables, 0 faults. No derived file has landed yet: maker A's and the infographics maker's notes have no "derive" line. Data lead's ruling (f) not yet written. Preparing the 15.20 facts table for all 50 reforms from the model while I wait.

## Summary

## Data check over derived files

- **The data lead's ruling figures, rechecked from the frozen files (20:48 UTC), all equal:** S86, 90,837 local governments, 90,888 with the federal government and the states, special districts 39,555 (43.5 percent), county radius 0.277 of theirs; S87 and S88, the four regions recomputed from DP03 (189,377,193; 23,775,140; 95,362,515; 28,323,306; sum 336,838,154, the population), every gap past its approximate margin, the closest both kinds against none, 4,548,166 against 618,795; S90, shares 45.2341, 43.1987 and 11.5672 summing to 100.0000 and rounding to 45, 43 and 12, New York $31,917.51 and Idaho $11,060.40 per pupil; S94, 16 events on 13 days, 7 with a consequence stated and 9 without, every stored weekday equal to the calendar's; S95, 50 states, Mississippi 652 the highest and Massachusetts 96 the lowest.

## Facts for Rule 15.20's reforms

## V7.1 items raised in round 4

## Routine calls

## Requests

## Tested

## Not tested
