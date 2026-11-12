# Round 2 progress page builder notes

Oath & Action Edition 06, Phase 3, round 2, November 12, 2026. The page builder works as the design director building a review page (`.claude/agents/oa-design-director.md`), under `work/handoffs/phase-3/20261112_Round-2-Progress-Page-Brief.md` (DR-241, DR-246). Paths are relative to `oath-and-action-v6-brand-guide/`.

## Status

- **Method proven; waiting for the main session's word that the rescore has landed.** Then: `python3 -I work/build/scripts/phase-3/progress_round_2_build.py --reuse --check`, read the parts' states, report.
- Built: `work/boards/phase-3/round-2/progress/20261112_Round-2-Progress.html` with `img/` beside it, by `work/build/scripts/phase-3/progress_round_2_build.py` and `progress_round_2_render.js` (copied from round 1's and adapted; round 1's scripts and page untouched), from the words in `20261112_Round-2-Progress-Content.json`. Figures go to `20261112_Round-2-Progress-Figures.json`; the check writes `20261112_Round-2-Progress-Check-Results.json`.
- **The page in the folder now is a method run, not one to publish.** The fix pass has the strict guide build failing (exit 1, 388 warnings from the kit's new label guard on round 1 and round 2 charts), so the last runs used `--photos-from-failed-build`: the guide pictures come from that failed build, every part that reads the guide carries "Part waiting for a passing guide build", "The guide today" says the strict build did not pass, and the figures file records `pictures_from_failed_build: true`. The final run drops the flag.
- Folder at the last run: 88 files, about 24.5 MB (the page about 130 kB, 84 composed PNGs, the three JSON files). Limits: under 200 files and 50 MB.
- What waits on others: the strict build passing; the quick guide check's results file (the brief's path, `.../round-2-review/main/quick/guide-Guide-Check-Results.json`, does not exist: that run's log shows a Playwright timeout, exit 1; the four-width file exists and reads 0 failures); the reviewers' second passes; the rescore; the kit's faults on S47, S50, S55, S57, S59, S62 and S63 (the fix pass's new sweep and guards), which print under each chart until they pass.

## How to rerun

```
python3 -I work/build/scripts/phase-3/progress_round_2_build.py --reuse --check
```

- About 4 minutes while the fix pass changes the kit's shared files and the guide's styles, since then nothing can be reused (a strict build, 24 kit charts, 97 photographs and measurements, 84 compositions, the two checks); well under a minute once nothing changes. Drop `--reuse` to remake every capture.
- `--reuse` keeps a kit capture when its spec, data, form module and the kit's shared files (and tokens.css) are unchanged, and a guide photograph or measurement when its element's HTML, the guide page's styles and scripts and the window width are unchanged. The strict guide build always runs afresh.
- `--check` runs `dataviz_check.js --board --no-captures` from `work/build` twice: on the page itself and on a scratch copy wrapped as the host wraps it. `--strict` exits 1 on any warning. `--photos-from-failed-build` is for a method run only. Scratch defaults to `/tmp/claude-0/-home-user-Dustin-s-Command-Center/3ab6316c-6935-5f23-804c-cfaafd548447/scratchpad/phase-3/round-2/progress-page/`; `--scratch DIR` moves it.
- When the main session names the final build's guide check results, change the two `scratch_glob` lines in the content file's `sections.tested.tested` (paths under the session's scratchpad folder). The build warns while a results file's build differs in bytes from today's strict build.
- The rescore is read from the newest `work/handoffs/phase-3/*Round-2-CD-Rescore*.json`; each reviewer's second score from its report's "Second pass" section.

## What the page reads

| Part | Reads |
|---|---|
| 1, round 2 in one screen | the plan file's round 2 rows (by status), chapter 14's entries for those rows; chapter 15's rules less those round 1's figures file lists; round 4's plan table "Datasets to fetch and freeze" against `work/build/data/`, each new file's sidecar ledger row (from the row the plan names first, P7-301) and that row in the research ledger; Rule 14.9's and 14.3's chart files that their correct plates name (form, red point and its name in the title); the build report's plate style bytes; chapter 13's chart files' titles; every chapter 15 wide plate measured at 1024 and 768 px; the strict build's report |
| 2, the 22 new charts | the plan's new forms in its order under its family titles; each title and evidence label as the strict build prints them, the label marked where it reads "Estimate"; the kit's own captures and check file from a fresh `oa-chart.mjs build`; bytes from the build report |
| 3, S18 and S33 | the same as part 2, from the plan's round 1 rows, with the content file's line on what changed |
| 4, an entry | Rule 14.74 photographed whole at 1440 and 390 px, and the desk's phone drawing heading read from it |
| 5, sketches | the plan's sketch forms, avoid first; heading, chip and caption read from each figure; each photographed at 1440 px |
| 6, the rules for every chart | the rules the creative director's `ch14_rules` item names in its parenthesis (14.3, 14.6, 14.9, 14.11, 14.12), with the opener, photographed at 1440 px |
| 7, chapter 15 | the new rules' plates at 1440 and 390 px, the first new wide plate at 1024 px, under chapter 15's group titles |
| 8, scores | the first scores, the newest rescore, the three red team reports (first score and counts before "Second pass", second score after it) |
| 9, weight | the build report |
| 10, tested | today's build report; the guide check results files in scratch; the engineer's, research lead's and makers' notes by pattern; the second passes; the rescore; each Not tested line checked against the report that names it |

## Routine calls

- D3-xxx | Round 2's page is round 1's page copied and adapted, with round 1's readers, page style, checks and composition kept, and round 1's scripts and page left as they are | The brief keeps round 1's look and method, and round 1's page stays as published
- D3-xxx | The 15 sketches print the guide's heading and caption under each photograph, the avoid pairs first under their own group title | The brief asks for the heading and caption as the guide prints them, the four avoid pairs first
- D3-xxx | A chart the guide labels "Estimate" carries the same label in its header, and part 2's lede names the four; the grade line stays in the picture only | "Mark the four Estimate charts as the guide labels them"; printing the grade line twice, one line apart, read as noise
- D3-xxx | Chapter 15's new rules are chapter 15's rules less those round 1's figures file lists | Chapter 15's file carries no round; round 1's page recorded the rules it showed
- D3-xxx | The rules part shows the rules the creative director's first scores name as changed in the `ch14_rules` item | A file names them, so nothing is typed by hand; the build warns if the item stops naming any
- D3-xxx | Round 1's carried items each print as their own fact in part 1, read from the file that shows each done: the chart file Rule 14.9's correct plate names and its form, the red point on Rule 14.3's chart file with its name checked against the title, the build report's shared plate style, chapter 13's five chart titles, and every chapter 15 wide plate measured at 1024 and 768 px | The brief asks for each as done, read from files; a measurement shows the wide stage holds where a file could only claim it
- D3-xxx | The wide stage counts the chapter's opener with its rule plates, 22 in all | The systems designer's notes count 22, and the opener takes the same stage
- D3-xxx | Chapter 15's 1024 px picture is the first new wide plate the guide sets, Rule 15.11's correct plate | "One wide plate also at 1024 px", chosen by the files and not by hand
- D3-xxx | Round 4's data counts files and rows from its plan's table against the data folder, and names the new files by their sidecars' ledger rows from the row the plan names first | Round 1's round 3 method, with the ledger rows read from the sidecars and checked in the research ledger
- D3-xxx | Red team finding IDs now read with a space inside them (ST M1, BC S18, AX M1) | Round 2's reports prefix their IDs; the old reader fell back to bullet counts and read 12 Must fix for 3
- D3-xxx | The creative director's part names print without review IDs in parentheses (RS-S1) | A reader would not know them (D3-206)
- D3-xxx | A kit fault under a chart moves its decision codes to the part's reference line and stops at 180 characters | The fix pass's new checks print long lines with codes; the final run should show none
- D3-xxx | `--photos-from-failed-build` photographs a strict build that failed, for a method run only, and every part that reads the guide then stays "Part waiting for a passing guide build" | The fix pass had the strict build failing at the first run, and the method still needed its photographs proven
- D3-xxx | A tested line for the second passes or the rescore reads "Waits for the end of the fix pass." until its file lands | "Not found in its file" would read as a fault
- D3-xxx | The quick guide check's line reads its results file from the brief's path and says "Not found" while the file is missing | That run timed out in Playwright and wrote no results; the four-width check's file stands beside it

## Tested

- First run, without `--reuse`, with `--check`: exit 0; the strict guide build failed (exit 1), so no guide pictures; the kit built all 24 charts (22 new, S18, S33), 24 check files counted: 17 PASS, 7 FAIL under the fix pass's new sweep and guards (S47, S50, S55, S57, S59, S62, S63); `dataviz_check.js --board --no-captures` on the page: only axe html-has-lang at 1440, 390 and 360 px; the wrapped copy: PASS.
- Runs two to five, with `--reuse --check --photos-from-failed-build`: every kit chart and guide element remade each time (the fix pass changed shared files between runs); 95 to 97 elements photographed or measured with no failure in the renderer's log; 84 composed images; the page check the same as above, the wrapped copy PASS at 1440, 390 and 360 px.
- Part 8's red team counter on round 2's reports, by script: statistics 4 of 5, 3 Must fix, 11 Should fix; brand and craft 3 of 5, 3 and 18; access 4 of 5, 1 and 11; each matches the fix brief's table and the reports' headings.
- Part 1's figures against the files: 41 entries, 22 new (S43 to S64), four built (S10, S08, S06, S01), 15 sketches with four avoid; chapter 15's six rules and 12 plates; round 4's 10 new files, P7-301 to P7-310, each row in the research ledger, 11 of 11 data rows; Rule 14.9 on `range-bar`; Rule 14.3's red point on 18 to 24, named in its title; the plate style block; five of five chapter 13 titles with a period; 22 of 22 wide plates at 680 px at 1024 and 768 px.
- The build's own checks on every run, as round 1's: no em or en dash, no flagged word, no unfilled field, no decision code on the face, every reference code in the decision log, no private path, no script, no document tags, no dark-mode block, no color outside a token, no type under 13 px, alt text on every image, the page names exactly the images in `img/`.
- The wrapped copy read by eye from screenshots at 1440 px (cover, parts 1, 2's S51, 4, 5, 7, 8) and 390 px (part 3); no sideways scroll at either width (scroll width equal to the window). Two composed pictures viewed whole (Rule 15.11 at 1024 px, the sketch for Rule 14.73).

## Not tested

- The page with a passing strict build, the quick guide check's results, the second passes or the rescore: none exists yet.
- The page in Safari or Firefox, on a 2x screen, printed, or as the host wraps it once published; the wrapped copy stands in.
- 82 of the 84 composed pictures one by one, and most parts at 390 px by eye.
- A keyboard walk past the first 40 stops, and a screen reader.
- The figures quoted from teammates' notes beyond reading each line's pattern; the page prints them as written.
- Publishing; the main session publishes.

## Change log

- Created: `work/build/scripts/phase-3/progress_round_2_build.py`, `work/build/scripts/phase-3/progress_round_2_render.js`, `work/boards/phase-3/round-2/progress/20261112_Round-2-Progress.html`, `20261112_Round-2-Progress-Content.json`, `20261112_Round-2-Progress-Figures.json`, `20261112_Round-2-Progress-Check-Results.json` and `img/` (all in `work/boards/phase-3/round-2/progress/`), and this file.
- Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/3ab6316c-6935-5f23-804c-cfaafd548447/scratchpad/phase-3/round-2/progress-page/` (the strict guide build and its report, `kit-out/`, `shots/`, the signature and composition caches, `publish-view/` with the wrapped copy and its check results, run logs, `probe/` and `view/` screenshots).
- Modified: none outside these.
