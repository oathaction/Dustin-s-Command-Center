# Fix pass engineer notes

Oath & Action Edition 06, Phase 3, chat 7, November 16, 2026. Written by the engineer (`oa-engineer`) under `work/handoffs/phase-3/20261116_Rounds-4-5-Fix-Brief.md`, Addendum 1 (calls 9, 11, 13 and 14). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f55a08bf-cdcf-539d-a683-426e26f4f342/scratchpad/c07/fix/engineer/` (`scratch/` below).

## Status

- 17:45 UTC (clock read): started. Read `CLAUDE.md`, my role file, the fix brief whole with Addendum 1, the production report whole, the accessibility report's codes and reach sections, and my codes in the CD, craft, drift, nonpartisan brand, statistics and reader panel reports; the research lead's request. Order: call 9, call 13, call 11, call 14, then the rest.

- 17:49 UTC (clock read): **call 9 and call 13 landed in their generators**, each rerun twice (the second wrote nothing) and `--check` passing; the strict build for both waits for call 11's change, so one build proves the three. The main session's DR-282 word read: "Not fixed" below takes its five parts for every code.

## Fixed

| Code | What changed | File | Proof |
|---|---|---|---|
| Call 9 (ST-S4, AX-S1, PR-S6) | The label ratio in each table cell is measured from the label's hex and the fill's hex (the ground's, for group 4's label beside the hatch) and rounded down by the plate's own `ratio()`, as the ground ratios already were; round 0's half-up figure is kept only as a cross-check (a fault if the two differ by more than 0.006). 16 numbers drop by 0.01: 10.47 to 10.46, 7.81 to 7.80, 7.48 to 7.47, 5.41 to 5.40, 4.61 to 4.60 (twice), 5.42 to 5.41, 6.18 to 6.17 (twice), 11.76 to 11.75, 10.64 to 10.63, 11.44 to 11.43, 7.33 to 7.32 (twice), 4.92 to 4.91, 9.38 to 9.37. Every other character of the plate is the same, the "text", "large text" words included | `work/build/scripts/phase-3/palette_spec_build.py`; output `s-14-palette-spec.html` | Rerun: 1 file written, 0 faults; second run 0 written; `--check` 2 of 2 current. `scratch/ratio_diff.py` on the old and new plate: 91 ratios printed, 16 changed, each by 0.01, the rest of the file equal |
| Call 13 (PR-S1, DR-278 (d)) | The token table's script finds its own plate first (`document.currentScript.closest('[data-specimen]')`, as the other eleven plate scripts do) and selects `.tt` inside it only; the index link finds its group among the table's own groups, not by a page-wide `getElementById`. The style was already scoped to the plate by the build's `@scope` (read on the built page), so it does not change | `work/build/scripts/phase-2/token_table_build.py`; output `s-26-token-table.html` (8 lines added, 2 changed, the script only) | Rerun; `--check` matches tokens.json 6.0.0-gate3.3, 545 tokens; the script parses in Node |

## Not fixed

## Calls

| call | reason |
|---|---|

## Requests

## Words for the editor

## Tested

## Not tested

## Change log
