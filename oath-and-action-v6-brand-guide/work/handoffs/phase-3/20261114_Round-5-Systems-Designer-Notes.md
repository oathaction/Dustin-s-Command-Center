# Round 5 notes: systems designer, Rules 15.22 to 15.25

Oath & Action Edition 06, Phase 3, round 5, November 14, 2026. Written by the systems designer (a general-purpose agent briefed as the designer who drew chapter 15) under `work/handoffs/phase-3/20261114_Phase-3-Round-5-Brief.md`, contracts R5-5, R5-6 and R5-8. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/7633c399-b692-5041-be92-a87ecd098fbf/scratchpad/phase-3/round-5/systems-designer/`.

## Status

- 01:43 UTC. Started. Read `CLAUDE.md`, the round 5 brief in full, my round 1, 2 and 4 notes, the generator and chapter file as they stand, the workflow sources file, Phase 0's reconciliation table and the November 13 rerun. Baseline run of `phase3_ch15_build.py`: every check passes, 21 rules, 43 plates, and no file of mine changes. Starting 15.22, 15.24 and 15.25 (group 5 and group 6) while the data lead's rulings (e) and (g) and the research lead's "Facts for owners" land. 15.23 waits on the tracker designer.
- 01:46 UTC. **R5-8 applied** in `phase3_ch15_build.py` with one function (the tracker designer's map and pattern, `(?<![\d.])11\.1[0-6](?!\d)`): three matches, lines 2316, 2332 and 3583, each "Rule 11.14’s plate" to "Rule 11.16’s plate" (the loop stepper's plate). The generator ran clean twice; the second run changed nothing (hashes of the chapter file, the manifest and every `s-15-*` plate), and `git diff` on my files shows those three lines in the generator and the same three in `15-systems-graphics.json`, no plate changed.

- 02:20 UTC. **15.22, 15.24 and 15.25 drafted in the generator and passing its checks**; captures and a words pass next, then 15.23 on the tracker designer's Rules 11.10 and 11.11 (landed 02:17, relayed). 15.22 follows ruling (e): the spine (stages every enacted bill passes) in Charcoal at the subject weight with filled squares, the paths that leave it in the context ink with outlined squares in the order a bill meets them (suspension, cloture, reconciliation, veto and override, law without a signature, the pocket veto), then funding, rules, congressional review and the courts, and reversal last, with a line back to step 1; 19 stages, each tied by script to a row of the workflow sources file with its read date. 15.24: the eleven routes as live-text cards in the atlas's order, the 126 entries in disclosures, Reform R-28 read through 15.22's reconciliation path. 15.25: the research lead's 57 rows in ruling (e)'s order, every model value read here from the model, the four value, sign, grade and delay rows on the plate and all 57 in a disclosure.

## Summary

To come.

## Contracts

### C-SD1. Drawing functions the complex examples maker may import, read-only (01:50 UTC)

Load `work/build/scripts/phase-3/phase3_ch15_build.py` with `importlib.util.spec_from_file_location` and call these; never write its outputs, never call `main()`, `write()` or `chapter()`, and set `sys.dont_write_bytecode = True` before the load. Importing it runs only its `need()` checks on the model; it writes nothing.

- **Loops:** `two_loop(codes, lids, ...)` (with `stacked_loop` behind it), `three_loop(codes, lids, ..., steps_g=False, lit=(), for_=None, only=None)`, `four_loop(codes, lids, ..., steps_g=False)`. Each returns the SVG body and its height (two_loop also the pills); wrap it with `svg_wrap(body, h)` for the 296 px artboard. Every title is the variable's own (DR-265).
- **Parts:** `Pill`, `conn`, `step_words`, `verb_at`, `loop_id`, `read_aloud`, `short`, `gl` (a connection's chip with its grade word), `step_lines`, `label_for`, `ticks_line`, `stepper_steps(lid)` (Rule 18.22's step list for a loop).
- **Styles:** the `CSS` dict's entries `sv`, `id`, `sn`, `rt`, `rp`, `sh` draw what these functions mark up; `dw` and `stepper_css(n)` draw a stepper's band (`.bd`) and its current step. Copy what you need into your own plate CSS; chapter 15's `plate_css` is scoped to chapter 15.
- **`four_loop(..., steps_g=True)`** (added 01:50 UTC at the maker's request, its notes' Requests item 1): wraps each step (a `.bd` band path, its marks and its words) in `<g data-s="1">` to `"4"` and each pill in `<g data-p="0">` to `"3"`, as `three_loop` does for Rule 15.19, so Rule 14.143 can light Loop R10's current step. The default, `False`, draws every chapter 15 plate as before: after the change the generator ran clean, and the chapter file, the manifest and all 43 `s-15-*` plates hash the same as before it (checked with `sha1sum`), so `git diff` on my outputs shows nothing from it.
- Signatures may grow keyword arguments with defaults that keep today's drawing; I will say so here first if one ever has to change.

## Routine calls

- D3-xxx | `four_loop` takes `steps_g` as `three_loop` does, default False | The complex examples maker's request for Rule 14.143's stepper drawing of Loop R10 (one drawing function, R4-5); no chapter 15 plate changes, proved by hashes
- D3-xxx | R5-8's map is applied in `phase3_ch15_build.py` by one regular-expression function over the source, never a chain of replaces | The tracker designer's contract; a chain would carry 11.14 on to 11.16 and then 11.18

## Requests

## Tested

## Not tested
