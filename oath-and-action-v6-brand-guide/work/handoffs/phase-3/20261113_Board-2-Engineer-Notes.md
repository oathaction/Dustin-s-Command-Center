# Board 2 engineer notes

Oath & Action Edition 06, Phase 3, board 2, November 13, 2026. Written by the engineer (`oa-engineer`) under `work/handoffs/phase-3/20261113_Board-2-Brief.md` (my row: A1's phrase check, A3, A6, and build needs the board raises). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/engineer/`.

## Status

Started 17:07 UTC (clock read). Read CLAUDE.md, my role file, the brief, the decision log from D3-1312 to DR-260 and my round 3 notes.

- **A1: DONE (17:15 UTC).** `work/build/chart-kit/words.json`'s `data_file` reads "this chart’s data file in the guide’s asset package", DR-254's words character for character. The export check holds every row of each chart's CSV, before and after the editor's rewrite (8 PASS, 0 faults). Details under "A1".
- **A3: LANDED (17:18 UTC).** On the cartographer's red `#CC0000` and blue `#2C7BB6`, one check warned: the guide build's literal color scan, which would fail a strict build. That half has a named exemption in `guide_build.py` (`LITERAL_HALF`) with DR-64's one exception in its comment; nothing else changed. The guide check and the kit's rendered check pass the drawing with no exemption. `guide_build.py --self-test` 33 of 33. Details under "A3".
- **A6: PASSED (17:35 to 17:46 UTC)** after the data lead's sign-off of A1 to A5 (17:35): generator 0 faults, `--check` 87 of 87 current; `build --all --no-png` with the sweep 84 of 84 PASS, 84 check files, 0 faults, 0 warnings; data check 125 tables, 0 faults; `geo.js` current; V7 check PASS, 0 failures; kit self-test every fault caught; strict build exit 0, 0 warnings, 11,236,319 bytes, 344 rules, 638 specimens. **Share per plate 13,230** for round 4's 13 (13,322 before); **projection 15,044,827** of 15,500,000. `plate-share.json` not restored (its share changed, not only its time). Details under "A6 results".
- **Flag for the data lead and the main session:** S73 measures 14,148 bytes on the page with its frame, 42 over D3-1328's 14,106 (13,974 before Part A; the kit's estimate says 14,087). No check fails on it. Under "A6 results".
- **Build needs done:** the editor's raw `{data_file}` in two hidden caption copies (fixed in `kit-build.js`, 17:20); the research lead's R-B2-1 (`data_round0_build.py` carries A5's variants, 17:28). Under "Build needs".

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
- D3-xxx | A table caption's two hidden copies (the table's name and the summary's words) fill `{data_file}` as the visible caption does, with a kit self-test case | The editor's find: a screen reader heard the braces in S69, S70, S72 and S73; the fix sits in `kit-build.js`, off the page
- D3-xxx | `data_round0_build.py` takes the research lead's R-B2-1 diff, once A5 was signed off whole and after a scratch rebuild proved 34 of 34 files equal | The script would otherwise drop S10's and S23's `snapshot_once` variants on its next run; the script is mine to change
- D3-xxx | Each Part A plate's "before" is measured on a strict build of `33dc30a3` in scratch, its chapter 14 checked by its share (13,322, the committed figure) | A page measure on both sides, by one script, is the figure D3-1328 and D3-1412 were set in
- D3-xxx | `plate-share.json` keeps the strict build's 13,230 | The brief restores it only if the build rewrote nothing but its timestamp; the share changed with the chapter

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

Run from 17:35 to 17:46 UTC (clock read), after the data lead's "Part A: A1 to A5 all signed off (17:35 UTC)", on the specs as they stood, which hold the editor's two later word changes the data lead signed off before A6 (S74 at 17:28, S71 at 17:37). No browser in any step. Outputs in scratch `a6/`.

| Step | Result |
|---|---|
| `python3 -I work/build/scripts/phase-3/phase3_ch14_build.py` (17:35) | exit 0: 128 rules (114 entries, 84 chart plates), 97 examples logged, 13 numbers planned for later rounds; 87 files, 2 written (the chapter file and its manifest: 14.124's caption and alt); **0 faults** |
| `phase3_ch14_build.py --check` | **87 of 87 files current** (again at 17:46) |
| `node work/build/chart-kit/oa-chart.mjs build --all --no-png`, sweep on (17:35:36 to 17:38:55, 3 min 19 s) | exit 0: **84 of 84 PASS, 0 FAIL; 84 check files counted; 0 faults, 0 warnings** read from the 84 check files; 84 CSV exports, 0 CSV faults |
| Data check, `data_round0_build.py --check` (17:39) | **125 tables, 0 faults** |
| `tools/geo_build.py --check` | **`geo.js` is current** |
| Kit self-test, `oa-chart.mjs self-test` | **every planted fault caught** (132 lines, none missed; the board 2 caption case among them) |
| Strict build, `guide_build.py --strict --out scratch/a6/strict/guide.html` (17:39:19 to 17:39:30) | **exit 0, 0 warnings, 11,236,319 bytes, 344 rules, 638 specimens placed** (D3-1536's committed build: 11,235,128) |
| V7 check, `v7_check.py --page` that build (17:42 to 17:46) | **PASS, 0 failures**: chapter 13 50 chips, chapter 14 128, chapter 15 116; 102 kit specs and the data folder |

**On the strict page:** no `{data_file}` left anywhere; DR-254's phrase prints 18 times: S69's, S70's and S72's captions three times each (the visible caption, the table's name and the summary's hidden words), S73 four (its caption's three and note 3), S74, S81 and S83 once each in their notes, entry 14.120's rule text once, and the page's own copy of `words.json` in its script once. Sketch 14.124's misleading half prints `#CC0000` and `#3A8AC4`, each twice, with no warning (A3's exemption at work in the full build).

**Weight** (the strict build's report):

| Measure | Bytes | Against |
|---|---|---|
| Page | 11,236,319 | 16 MB; 11,235,128 before Part A |
| **Projected page** | **15,044,827** | 15,500,000: 455,173 of room; unchanged, since chapter 14 is held to its allocation in the projection |
| Chapter 14 as built | 1,582,289 | 1,581,098 before Part A (+1,191) |
| Chapter 14 with the kit | 2,228,367 | the 2,803,941 stop (DR-238) |
| Renderer, the "chart kit" part | 512,961 | unchanged; `kit-build.js` never rides on the page; grown to 97 forms 557,494 |
| Map geometry | 133,117 | 250,000, 116,883 unspent and held |
| Rules 14.1 to 14.14 with the opener | 175,678 | 212,288 |
| **Share per plate, round 4's 13 specimens** | **13,230** | 13,322 before Part A (the committed `plate-share.json`); 171,996 bytes of room |

The share fell 92 bytes a plate because the chapter as built grew 1,191 bytes (13 times 92 is 1,196), all of it in the plates below; the renderer did not grow.

**Each changed plate, before and after, on the page** (each `<figure class="plate">` whole, frame included, by `scratch/scripts/plates.py`). "Before" is a strict build of the committed state before Part A (`33dc30a3`'s `work/build` folders extracted to scratch, its unchanged `assets`, `node_modules` and `packages` linked): its chapter 14 built with no warning and gave the committed share, 13,322, so its chapter 14 is the committed one. (Its chapters 01 to 04, 17 and the proofs miss identity assets, since the build refuses a linked asset whose real path leaves its root, so only chapter 14's plates are compared.) Every other chapter 14 plate is byte for byte the same size.

| Plate | Part A item | Before | After | Change | Against |
|---|---|---|---|---|---|
| S10 | A5 | 8,163 | 8,166 | +3 | 14,106 |
| S16 | A4 | 10,732 | 10,933 | +201 | 14,106 |
| S21 | A5 | 6,428 | 6,431 | +3 | 14,106 |
| S23 | A5 | 6,971 | 6,974 | +3 | 14,106 |
| S38 | A5 | 10,835 | 10,811 | -24 | 14,106 |
| S39 | A5 | 11,150 | 11,154 | +4 | 14,106 |
| S60 | A5 | 9,803 | 9,819 | +16 | 14,106 |
| S63 | A5 | 11,106 | 11,082 | -24 | 14,106 |
| S69 | A1 | 14,556 | 14,553 | -3 | its own measure, under 15,000 (D3-1412) |
| S70 | A1 | 10,946 | 11,114 | +168 | 14,106 |
| S71 | the editor's later fix (a studio path in its table) | 12,452 | 12,801 | +349 | 14,106 |
| S72 | A1 | 7,961 | 8,093 | +132 | 14,106 |
| **S73** | A1 | 13,974 | **14,148** | +174 | **14,106: 42 over on the page measure** (the kit's estimate, with its 750-byte frame, gives 14,087) |
| S74 | A1, and the editor's measure line (17:28) | 11,813 | 11,760 | -53 | 14,106 |
| S81 | A1 | 13,611 | 13,654 | +43 | 14,106 |
| S83 | A1 | 13,393 | 13,436 | +43 | 14,106 |
| Sketch 14.124 | A2 | 5,612 | 5,725 | +113 | the sketch's file 3,941 of its 4,096 |

**S73, for the data lead and the main session.** On the page S73 now measures 14,148 bytes with its frame, 42 over D3-1328's 14,106, where it stood at 13,974. Of the 174 bytes, 86 are the editor's A1 words (the kit's 13,913 to 13,999) and 88 the caption fix (the filled phrase in the table's name and the summary's hidden words, which a screen reader hears; no reader sees them). The kit's own weight line puts it at 14,087, under, since its frame is an estimate of 750 bytes and S73's real frame is about 811. No check fails on it (the kit warns past 15,000; the strict build passed). Taking 42 bytes off S73's words would bring it under on both measures; the call is the data lead's, and the words the editor's. Every other Part A plate is under its ceiling on both measures.

**`plate-share.json`:** the strict build rewrote both its timestamp and its share (`per_plate` 13,322 to 13,230, `built` 07:17:18 to 17:39:30), so by the brief it is **not restored**; it holds this build's 13,230 for the kit's weight lines, and `git diff` shows it changed. The kit's `build --all` above ran before the strict build and printed 13,322.

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

## Fix round: B2-M4, one byte measure per chart (18:18 to 18:23 UTC)

Under `work/handoffs/phase-3/20261113_Board-2-Fix-Brief.md` call 4. Read only; no build file changed.

- **Wrote** `work/handoffs/phase-3/board-2-pictures/20261113_Plate-Bytes.json` (18:22 UTC) from the main session's final strict build, `.../board-2/main/final/guide.html` (11,236,230 bytes, SHA-256 `8a01b67e784a302c…`) and its build report. Script: `scratch/scripts/plate_bytes.py` (the rerun line in the JSON names it).
- **One measure:** `total` = `bytes_as_placed` (the report's) + `added_on_page` + `frame_bytes` = the plate whole on the page. 95 of the 97 chapter 14 charts sit on the page byte for byte as the report counts them; S06 (+360) and S67 (+48) carry D2-975's `<span class="nw">` round their atlas IDs, which the build adds after the report counts the chart. Frames run 723 to 847 bytes (the kit's line estimates 750).
- **Ceilings by round:** round 3 D3-1328's 14,106 total (S69 at its 14,556, D3-1412); rounds 1 and 2 and board 1 the far-over test on bytes as placed, 24,576 (S05 31,961 and S13 47,212, D3-350); sketches 4,096 for the file. **None over.** S73 after the trim: 13,263 + 796 = **14,059**, 47 under 14,106. S82 14,039 (67 under), S69 14,553 (3 under its own measure).
- 141 chapter 14 plates: 84 entries, 13 rule plates with charts (their frame and own HTML apart), 44 others (21 sketches, 7 avoid sketches, 15 rule plates with no chart, the opener).
- At 18:23 S09's, S10's and S21's specs show changed since that build (another owner's); their rows hold the final build's figures until a rebuild, as S03's and S08's would.
- **Remeasured on the version 9 build (18:50 UTC)**, `.../board-2/main/v9/guide.html` (11,236,260 bytes, SHA-256 `4c834d2b11c983d6…`, share per plate 13,235), and the JSON rewritten. Against the final build: S06 17,190 to 17,198, S09 13,791 to 13,801, S10 8,166 to 8,172, S21 6,431 to 6,437 (the curled apostrophes, in bytes as placed; frames unchanged); S42's `curl_quotes` prints no different byte (2,454 as placed in both reports); every other plate the same. None over its ceiling; S73 still 14,059. The earlier file is kept in scratch as `plate-bytes-final-build.json`.

## Tested

- **A1:** `words.json`'s `data_file` read by script against DR-254's words. `oa-chart.mjs build` on S69, S70, S72, S73, S74, S81, S82 and S83 with no PNG and no sweep, before (17:10) and after (17:15) the editor's rewrite, and after the caption fix (17:21): 8 PASS, 0 faults each time; each export read against its whole data file by script (rows, columns, CSV faults).
- **A3:** `process_fragment` probed with a mock red and blue half (warns) and on the final file with and without the exemption (warns without, silent with). The trimmed chapter 14 page (rules 14.7 and 14.124) built and checked three times, on the gray file, the first red and blue (17:16) and the final file (17:30): `guide_check.js --quick --no-captures` (18 s each; 7 trim failures each time, none in the sketch) and `dataviz_check.js --kit` (PASS each time, forced colors in both themes included); the generator's faults in memory (0 on the final file). `guide_build.py --self-test` 33 of 33 scenarios, 334 of 334 expectations, with three planted faults in the exemption each caught.
- **The caption fix:** a harness on seven specs, HEAD's `kit-build.js` 8 raw placeholders, today's 0; the kit self-test with the new case, every planted fault caught.
- **R-B2-1:** the patched writer run into scratch, 34 of 34 files equal to `work/build/data/`; the data check after, 125 tables, 0 faults.
- **A6:** every step in "A6 results", with its output read from its files: the 84 check files counted and summed, the strict build's report, the V7 check's results; the strict page searched for `{data_file}` and the sketch's two fills; every plate measured before and after on two strict builds by one script.

## Not tested

- The whole-page guide check, quick or at four widths, with or without photographs: the main session's (the brief). The guide check ran only on my trimmed chapter 14 page.
- `guide_check.js --self-test`: I did not change `guide_check.js`, so I did not run it (the brief asks for it if I touch it). The exemption is in `guide_build.py`, whose own self-test ran.
- `dataviz_check.js --kit` on the whole page: run only on the trimmed page.
- I looked at no picture of the red and blue sketch: the cartographer and the data lead did. My tests read it by script and by the two browser checks.
- The kit's `build --all` with PNG captures (`--no-png`, as the brief asks): no kit capture or page parity check in a browser this pass, so the caption fix's hidden words were read from the Node figure HTML and the strict page, not heard in a screen reader.
- Firefox and Safari; print; the four device scripts (DR-213).
- The research lead's `research_v7_extract.py` diff: theirs, not applied by me.

## Files

- Modified: `work/build/scripts/phase-2/guide_build.py` (`LITERAL_HALF` with DR-64's one exception in its comment, five lines in `process_fragment`, one self-test scenario); `work/build/chart-kit/kit-build.js` (the caption's two hidden copies fill `{data_file}`); `work/build/chart-kit/oa-chart.mjs` (one self-test case); `work/build/scripts/phase-3/data_round0_build.py` (the research lead's R-B2-1 diff); these notes.
- Written by the chain: `work/build/guide/chapters/14-data-visualization.json` and `work/build/guide/specimens/manifest-data-visualization.json` (the generator, A6); `work/build/chart-kit/plate-share.json` (the strict build, A6: 13,230).
- Created: `work/handoffs/phase-3/20261113_Board-2-Engineer-Notes.md`.
- Scratch (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/engineer/`): `a1-before/`, `a1-after/`, `a1-fix/` (kit builds); `a3/` (trimmed chapters, pages `base/`, `rb/`, `rbx/`, `fin/` with their check results, copies of the sketch as it landed); `kb/` (HEAD's `kit-build.js`, the writer's proofs); `a6/` (`kit-all/`, `strict/guide.html` with its report and V7 results, `before/` and `before-page/` for the pre-Part A build, `plates.json`, `plate-share.before.json`); `scripts/` (`a1_export.cjs`, `a3_probe.py`, `raw_placeholder.cjs`, `rb21_proof.py`, `plates.py`).
