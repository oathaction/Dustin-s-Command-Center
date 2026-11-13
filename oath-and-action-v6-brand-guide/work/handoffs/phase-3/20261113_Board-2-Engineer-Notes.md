# Board 2 engineer notes

Oath & Action Edition 06, Phase 3, board 2, November 13, 2026. Written by the engineer (`oa-engineer`) under `work/handoffs/phase-3/20261113_Board-2-Brief.md` (my row: A1's phrase check, A3, A6, and build needs the board raises). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/engineer/`.

## Status

Started 17:07 UTC (clock read). Read CLAUDE.md, my role file, the brief, the decision log from D3-1312 to DR-260 and my round 3 notes.

- **A1 (phrase):** confirmed. `work/build/chart-kit/words.json`'s `data_file` reads "this chart’s data file in the guide’s asset package", DR-254's words character for character. The export check is under "A1" below. No spec or entry carries `{data_file}` yet; the editor's A1 has not landed.
- **A3:** reading the checks while the cartographer draws. Findings under "A3".
- **A6:** waits on the data lead's sign-off of A1 to A5.

## Contracts

- `{data_file}` (my round 3 contract, D3-1448, unchanged): in a spec's table caption, a note or a chart note, the kit prints `words.json`'s `data_file`; in an entry file, `phase3_ch14_build.py` fills the same phrase. The phrase is lowercase and never opens a sentence (D3-1529).

## Routine calls

## A1

**The phrase.** `work/build/chart-kit/words.json` key `data_file` reads `this chart’s data file in the guide’s asset package`, with U+2019 in both apostrophes, DR-254's words exactly (read by script, 17:09 UTC). The kit fills `{data_file}` in a caption, note or chart note from it (`K.fill_words`), and `phase3_ch14_build.py`'s `fill_words` fills the same phrase in an entry file (entry 14.120's rule text). Nothing in the kit or the generator changes for A1: the words are the editor's.

**The export check.** `oa-chart.mjs build` writes each chart's CSV from every column of its first dataset and then reads the file back against the rows the chart draws (`checks.js` `check_csv`: the same count, the same columns, the same values); a short or changed export is a fault. Run on the eight charts whose words promise the full rows, before the editor's rewrite (17:10 UTC, `build s69 s70 s72 s73 s74 s81 s82 s83 --no-png --no-sweep`): 8 PASS, 0 faults. A script then read each export against its whole data file (`scratch/scripts/a1_export.cjs`):

| Chart | Data file | Rows exported | Columns | CSV faults |
|---|---|---|---|---|
| S69 | `clerk-house-committees-119.csv` | 136 of 136 | all 7 | 0 |
| S70 | `uscode-federal-courts-circuits-districts.csv` | 111 of 111 | all 9 | 0 |
| S72 | `congress-hr5371-roll-calls-by-member.csv` | 533 of 533 | all 10 | 0 |
| S73 | `fec-jfc-transfers-2024-by-node.csv` | 125 of 125 | all 25 | 0 |
| S74 | `v7-region-connection-matrix.json` | 44 of 100 cells; the 56 with no connection are left out by its `where` (`links` not 0), as in round 3 | all 9 | 0 |
| S81 | `census-acs5-county-median-household-income-classes.csv` | 3,144 of 3,144 | all 7 | 0 |
| S82 | `clerk-house-results-2024-classes.csv` | 435 of 435 | all 15 | 0 |
| S83 | `census-cbp-county-employment-dots.csv` | 3,144 of 3,144 | all 8 | 0 |

The check still holds every row in each chart's CSV. S73's file now holds the seven funds' 125 rows (57 in round 3's first reading). The rewrite changes words only, so the exports cannot change; A6's `build --all --no-png` runs the same check on all 84 specs after it lands.

## A3

## A6 results

## Build needs

## Tested

## Not tested

## Files
