# Board 2 engineer notes

Oath & Action Edition 06, Phase 3, board 2, November 13, 2026. Written by the engineer (`oa-engineer`) under `work/handoffs/phase-3/20261113_Board-2-Brief.md` (my row: A1's phrase check, A3, A6, and build needs the board raises). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/engineer/`.

## Status

Started 17:07 UTC (clock read). Read CLAUDE.md, my role file, the brief, the decision log from D3-1312 to DR-260 and my round 3 notes.

- **A1 (phrase):** confirmed. `work/build/chart-kit/words.json`'s `data_file` reads "this chart’s data file in the guide’s asset package", DR-254's words character for character. The export check is under "A1" below. No spec or entry carries `{data_file}` yet; the editor's A1 has not landed.
- **A3:** reading the checks while the cartographer draws. Findings under "A3".
- **A6:** waits on the data lead's sign-off of A1 to A5.

## Contracts

- **For the cartographer, A2 to A3 (17:15 UTC).** Draw the red and blue in the misleading half only, the file's first `<svg>`, as `fill="#RRGGBB"` attributes (a hex the build can see; no `style` attribute or element, no CSS color name). The build's literal color check will then flag that half alone, and I give it the named exemption DR-255 asks for; the better half keeps the kit's classes and stays under the check. Keep every word off the red and blue shapes (the key's words beside its swatches, on the ground), since the guide check reads a word's contrast against the shape under it. Keep the red more than 8 apart in some channel from Pillar Red (230, 57, 70) and the blue from Prussian (31, 45, 90), so the red checks do not read them as the guide's inks. Tell me in your notes when the file lands; I test it on a trimmed page within minutes.
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

The check still holds every row in each chart's CSV. S73's file now holds the seven funds' 125 rows (57 in round 3's first reading).

**After the editor's rewrite (17:15 UTC).** The nine places now read `{data_file}` after their verb or preposition, none opening a sentence (S69, S70, S72 and S73's captions; S73 note 3, S74 note 4, S81 note 3, S83 note 3; entry 14.120's rule text), and no spec of the eight holds "download" or "CSV file" (grep, case folded). The same build and script give the same table: 8 PASS, 0 faults, every export whole. A6's strict build is where I read the phrase as printed: no `{data_file}` may be left on the page.

## A3

DR-255: sketch 14.124's misleading half draws in a plain news red and blue that are none of the guide's inks. The checks that read a sketch, read before the drawing landed (17:12 to 17:20 UTC):

| Check | What it reads in the sketch | Red and blue there |
|---|---|---|
| `phase3_ch14_build.py` (the generator) | the file's bytes (4,096 at most), its drawings (an avoid pair), its first `<desc>` against `sketch_alt`'s first sentence | no color test; passes if the file stays under 4,096 bytes and the caption and first `<desc>` agree |
| `guide_build.py` `process_fragment` (every strict build) | any literal color (`#hex`, `rgb(`, `hsl(`) in a specimen, outside `var()` and path data, unless the manifest's `check_exempt` names `literal`; `plate()` then warns that `literal` is for failure plates only, and the avoid plate is not one | **warns, so the strict build exits 1.** A probe with a mock red and blue first half: "s-14-124-sketch: 2 literal color value(s) (#1F5AA6, #C8102E); use var(--oa-...) from tokens.css" |
| `guide_check.js` Rule 05.3 (`red`) | every SVG fill and stroke within 3 of Pillar Red (230, 57, 70) must sit under `data-red`; none on Prussian | fires only if the news red is within 3 of Pillar Red, which DR-255 rules out |
| `guide_check.js` `redTouchesPrussian` | pixels within 8 of Pillar Red within 2 px of pixels within 8 of Prussian (31, 45, 90), in stages that compute both | fires only if the red and blue sit that close to the two inks |
| `guide_check.js` text contrast | each text against the shape under its center | fires only if a word sits on a red or blue shape |
| `dataviz_check.js --kit` (`kitForced`) | in forced colors, sketch text on a shape at 3 to 1, and keyed marks on the ground | literal fills keep their color in forced colors (the drawing sets `forced-color-adjust: none`); fires only if a word sits on a red or blue shape |
| `checks.js` (the kit's spec and drawing checks) | kit specs only | never reads a sketch |

**Method for the real drawing.** A scratch page of chapter 14 trimmed to rules 14.7 and 14.124 (`guide_build.py --chapters <scratch>`, which leaves `plate-share.json` alone), then the real guide check (`--quick --no-captures`, 18 s) and `dataviz_check.js --kit` (2 s) on it, and the generator's `--check`. Baseline on today's gray file (17:13 UTC): the guide check lists 7 failures, every one an artifact of the trim (14 links to groups and 4 citations of rules left out, 19 codes in the proofs page, one zoom scroll at 390 px) and none in either sketch plate; the kit check PASS, 0 failures.

## A6 results

## Build needs

## Tested

## Not tested

## Files
