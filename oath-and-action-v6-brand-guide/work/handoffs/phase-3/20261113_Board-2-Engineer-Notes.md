# Board 2 engineer notes

Oath & Action Edition 06, Phase 3, board 2, November 13, 2026. Written by the engineer (`oa-engineer`) under `work/handoffs/phase-3/20261113_Board-2-Brief.md` (my row: A1's phrase check, A3, A6, and build needs the board raises). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/engineer/`.

## Status

Started 17:07 UTC (clock read). Read CLAUDE.md, my role file, the brief, the decision log from D3-1312 to DR-260 and my round 3 notes.

- **A1: DONE (17:15 UTC).** `work/build/chart-kit/words.json`'s `data_file` reads "this chart’s data file in the guide’s asset package", DR-254's words character for character. The export check holds every row of each chart's CSV, before and after the editor's rewrite (8 PASS, 0 faults). Details under "A1".
- **A3: LANDED (17:18 UTC).** On the cartographer's red `#CC0000` and blue `#2C7BB6`, one check warned: the guide build's literal color scan, which would fail a strict build. That half has a named exemption in `guide_build.py` (`LITERAL_HALF`) with DR-64's one exception in its comment; nothing else changed. The guide check and the kit's rendered check pass the drawing with no exemption. `guide_build.py --self-test` 33 of 33. Details under "A3".
- **A6:** waits on the data lead's sign-off of A1 to A5.

## Contracts

- **For the cartographer, A2 to A3 (17:15 UTC).** Draw the red and blue in the misleading half only, the file's first `<svg>`, as `fill="#RRGGBB"` attributes (a hex the build can see; no `style` attribute or element, no CSS color name). The build's literal color check will then flag that half alone, and I give it the named exemption DR-255 asks for; the better half keeps the kit's classes and stays under the check. Keep every word off the red and blue shapes (the key's words beside its swatches, on the ground), since the guide check reads a word's contrast against the shape under it. Keep the red more than 8 apart in some channel from Pillar Red (230, 57, 70) and the blue from Prussian (31, 45, 90), so the red checks do not read them as the guide's inks. Tell me in your notes when the file lands; I test it on a trimmed page within minutes.
- `{data_file}` (my round 3 contract, D3-1448, unchanged): in a spec's table caption, a note or a chart note, the kit prints `words.json`'s `data_file`; in an entry file, `phase3_ch14_build.py` fills the same phrase. The phrase is lowercase and never opens a sentence (D3-1529).

## Routine calls

- D3-xxx | A1 needs no kit or generator change: `words.json`'s `data_file` already reads DR-254's phrase, and the export check already reads every exported row back | ST-M2's placeholder (D3-1448) was built so Dustin's answer changes one string and no spec
- D3-xxx | A3's exemption lives in `guide_build.py`'s literal color scan, named by specimen and half (`LITERAL_HALF`), not in the manifest's `check_exempt` | `check_exempt` covers a whole stage and is for failure plates only; DR-255 exempts the misleading half alone, and the better half keeps the check
- D3-xxx | The exemption names the half by its place in the pair (the first `<svg>`, the one under the do-not-publish bar) and applies only while the file is a pair | It needs no new attribute in the cartographer's file, and a file that stops being the avoid pair falls back under the check
- D3-xxx | `guide_check.js` and `checks.js` stay unchanged | On the real drawing neither reads the red or blue as a guide ink or finds a fault; DR-255 asks for an exemption only where a check fails or warns
- D3-xxx | The exemption's proof is a self-test scenario of the build, with three planted faults caught | The brief allows changing nothing else in the check; a test changes no check and keeps the exemption from widening unseen
- D3-xxx | A3 was tested on a scratch page of chapter 14 trimmed to rules 14.7 and 14.124, with the real guide check and kit check | The brief keeps the whole-page guide check with the main session; the trimmed page runs the same checks on the sketch in 20 seconds

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

**The red and blue drawing (landed 17:16 UTC, 3,932 bytes, SHA-256 `41f79d7e5adc89aa…`):** the first `<svg>` fills Party A's places and swatch `fill="#CC0000"` and Party B's `fill="#2C7BB6"`, words on the ground. Tested on the trimmed page (17:16 to 17:17 UTC), against the gray baseline:

| Check | Result on the red and blue |
|---|---|
| `guide_build.py` (the build's specimen check) | **one new warning:** "s-14-124-sketch: 4 literal color value(s) (#2C7BB6, #CC0000); use var(--oa-...) from tokens.css", so a strict build would exit 1 |
| `guide_check.js --quick --no-captures` | the same 7 trim failures as the gray baseline, none in the sketch; Rule 05.3: 23 red marks, 0 unmarked at both widths (the sketch's red is not read as Pillar Red); `redTouchesPrussian` 0 hits; no low contrast in the sketch |
| `dataviz_check.js --kit` | PASS, 0 failures at 1440 and 390 px, forced colors in both themes included |
| `phase3_ch14_build.py` faults | one, not a color test: the first `<desc>` does not yet hold `sketch_alt`'s first sentence (the editor's words and the cartographer's `<desc>` are being matched, R2-3); the file is under its 4,096 bytes |
| `checks.js` | never reads a sketch |

**The exemption (17:17 UTC), in `work/build/scripts/phase-2/guide_build.py`.** A named table beside `EXEMPT_KINDS`, `LITERAL_HALF = {"s-14-124-sketch": 0}`, with DR-64's one exception recorded in its comment (DR-255: the misleading half of sketch 14.124 draws a plain news red and blue that are none of the guide's inks, at sketch size, under its do-not-publish bar). In `process_fragment`, for that specimen only and only when its file holds an avoid pair (two `<svg>`), the literal color scan leaves out the drawing at that index, the first, the half `plate()` sets under the bar. The better half, every other specimen, the regular expression and the warning are unchanged; the manifest's `check_exempt`, the failure-plates-only rule and the generator are untouched. The guide check needs no exemption, since neither ink is a guide ink (above), so `guide_check.js` is unchanged.

- Self-test scenario added ("board 2: DR-64's one exception ..."): `s-14-124-sketch` with `#CC0000` in its first half and `#2C7BB6` in its second must warn "1 literal color value(s) (#2C7BB6)" and never both; another avoid sketch, `s-26-skx`, with `#CC0000` in its first half must still warn; the exempt half still draws its red under the bar. `guide_build.py --self-test`: **33 of 33 scenarios, 334 of 334 expectations** (32 and 328 before; `plate-share.json` byte for byte unchanged). Planted faults, each caught by the new scenario: the exemption removed (both halves warn), moved to the better half, and widened to `s-26-skx`.
- The trimmed page rebuilt with the exemption (17:18 UTC): its warnings equal the gray baseline's, none new and none gone; both fills on the page twice each; the guide check the same 7 trim failures, none in the sketch; the kit check PASS.
- **Retested on the final file (17:30 UTC):** the blue moved to `#3A8AC4` at 17:28 and the first `<desc>` took the editor's caption; 3,941 bytes, SHA-256 `d75d9e349e57fffb…`. The trimmed chapter regenerated in memory from today's entries (generator: 0 faults); the build's warnings equal the gray baseline's, none new; both fills on the page; the guide check the same 7 trim failures, none in the sketch (Rule 05.3: 23 red marks, 0 unmarked, 0 on Prussian, at both widths; `redTouchesPrussian` 0 hits; no low contrast in the sketch); the kit check PASS. Without the exemption the same file warns "s-14-124-sketch: 4 literal color value(s) (#3A8AC4, #CC0000)"; with it, nothing.
- For the cartographer: no attribute is needed on the `<svg>`; the exemption names the specimen and the half. If the misleading half ever stops being the file's first drawing, or the file stops being a pair, the exemption stops applying and the build warns, which is what it should do.

**Method for the real drawing.** A scratch page of chapter 14 trimmed to rules 14.7 and 14.124 (`guide_build.py --chapters <scratch>`, which leaves `plate-share.json` alone), then the real guide check (`--quick --no-captures`, 18 s) and `dataviz_check.js --kit` (2 s) on it, and the generator's `--check`. Baseline on today's gray file (17:13 UTC): the guide check lists 7 failures, every one an artifact of the trim (14 links to groups and 4 citations of rules left out, 19 codes in the proofs page, one zoom scroll at 390 px) and none in either sketch plate; the kit check PASS, 0 failures.

## A6 results

## Build needs

| Need | From | Status |
|---|---|---|
| A table caption's `{data_file}` printed raw in its two hidden copies, the table's name (`aria-label`) and the summary's hidden words | editor (17:16 UTC, "Words for the engineer") | **Done (17:20 UTC)** in `work/build/chart-kit/kit-build.js` (`K.figure`): both copies go through `K.fill_words`, as the visible caption does. A harness on the seven specs (`scratch/scripts/raw_placeholder.cjs`): HEAD's builder half prints 8 raw placeholders (two each in S69, S70, S72 and S73), today's none. New kit self-test case (a caption's `{data_file}` fills in all three places, with and without the guide's markup); self-test every planted fault caught. `kit-build.js` never rides on the guide's page, so the kit part's bytes do not change; the four plates gain the filled words in two hidden places, below |
| R-B2-1: carry A5's `snapshot_once` variants in `data_round0_build.py` (S10's and S23's sidecars) so a rerun keeps them | research lead (17:13 UTC, "Requests") | **Done (17:28 UTC), after the data lead signed off A5 whole (17:27).** Proven first in scratch (`scratch/scripts/rb21_proof.py`: the script's text run with its real path and its output folder in scratch, every file compared byte for byte with `work/build/data/`): today's script wrote 34 files with 2 differing (it would have dropped S10's and S23's variants on a rerun); the research lead's patched copy wrote 34 of 34 equal. Applied the research lead's diff with `patch -p1` (no fuzz); the script then equals the proven copy, rebuilds 34 of 34 equal, and the data check reads 125 tables, 0 faults. The research lead's own `research_v7_extract.py` is theirs to patch |

**Plate weights through A1 and the caption fix** (kit `build --no-sweep`, about 750 bytes of frame, the kit's own measure; the strict build's page measure follows in A6):

| Plate | Before A1 (17:10) | After the editor's words (17:16, editor's notes) | After the caption fix (17:21) | Against |
|---|---|---|---|---|
| S69 | 14,369 | 14,278 | 14,366 | its own measure before A1, under 15,000 (D3-1412) |
| S70 | 10,703 | 10,783 | 10,871 | 14,106 (D3-1328) |
| S72 | 7,802 | 7,846 | 7,934 | 14,106 |
| S73 | 13,913 | 13,999 | 14,087 | 14,106: 19 bytes under |
| S74 | 11,707 | 11,750 | 11,750 | 14,106 |
| S81 | 13,597 | 13,640 | 13,640 | 14,106 |
| S83 | 13,295 | 13,338 | 13,338 | 14,106 |

## Tested

## Not tested

## Files
