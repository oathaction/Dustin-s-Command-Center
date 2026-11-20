# Second pass, editor notes

Written November 20, 2026, by the editor. Brief: `20261120_Second-Pass-Brief.md`. Items in order: RS-1, RS-6, RS-2, RS-4, RS-5.

## Status

Started 16:38 UTC. RS-1 in at 16:43 UTC, proved by a strict build. RS-6 in at 16:45 UTC; its generator's check passes and a strict build is clean. RS-2 and RS-4 in at 16:54 UTC, RS-5 at 16:56 UTC. All five items are in; see RS-5 for what its change does and does not show a reader. Done at 16:58 UTC; I hold no file now.

HANDOVER: phase3_ch14_complex_build.py is free

A slip to report (16:48 UTC): to measure S90 and S91 before my word changes, I ran the kit's single-spec build (`oa-chart.mjs build <spec> --out <scratch>`) twice without `--no-png`, as the brief's command reads. Each run launched a headless Chromium through Playwright for its PNG exports and captures, and closed it when the run ended, at about 16:48 UTC, while the guide check's own browser (running since 16:32) was up. That broke this run's no-browser condition. No page or file in the repository changed from it; the PNGs sit in my scratch folder. Every kit build after it carries `--no-png`.

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

### RS-2: S91's title, one finding in 26 words

- **Original (33 words):** "Of the three kinds of judge who hear cases at trial in the federal district courts, only district judges serve for life, except in Guam, the Northern Mariana Islands and the Virgin Islands."
- **Revision (26 words):** "Of the federal district courts’ three kinds of judge, only district judges serve for life, except in Guam, the Northern Mariana Islands and the Virgin Islands."
- **Why the revision keeps the district courts.** The example, "Only district judges, of the three kinds who hear federal trial cases, serve for life, ...", widens the title's universe from the district courts to every federal trial court. Judges of the Court of International Trade also hold trials and serve for life, and the Court of Federal Claims and the Tax Court hear federal trial cases too, so "the three kinds who hear federal trial cases" would claim more than S91's data holds (H08, W20). The data lead's batch 9 (CD-S4) set the district courts as the title's universe, and the revision keeps it in "the federal district courts’ three kinds of judge", while the measure line under the title still says "who hears cases at trial in the federal district courts". The territorial exception stays whole, as the data lead's MI-4 and MI-7 ask (Puerto Rico's district judges serve for life, so the three territories are named).
- **Files:** `work/build/chart-kit/specs/s91.json` (the title; no generator writes this spec: `maker_i_round4_derive.py` only checks it). The derive script's S91 check looked for the old title's words, so I changed that one check in `work/build/scripts/phase-3/maker_i_round4_derive.py` to read the new scope words together with the measure line's universe, and added a check that the title stays at 27 words or fewer. Every other S91 check is as it was. `phase3_ch14_build.py` copies the title into Rule 01.12's example log (`14-example-log.json`, Rule 14.137's row) when it runs for RS-5.
- **Proof.** `maker_i_round4_derive.py --figures S90 S91`: all passed, exit 0. Kit: `oa-chart.mjs build s91 --no-png`: PASS, 0 faults; `build --all --no-png`: 96 specs PASS, exit 0, `plate-share.json` untouched. Strict guide build: exit 0, 0 warnings; the page prints the new title.
- **Bytes:** kit figure 6,762 to 6,734 as the guide places it; the plate in the page (`s-14-s91`) 7,559 to 7,531.

### RS-4: S90's row 4 note no longer points to a row the table leaves out

- **Original (the Note cell of row 4, "Share of revenue from federal sources"):** "Includes COVID-19 relief funds (row 5)"
- **Revision:** "Includes $39.2 billion in COVID-19 relief funds, as the first note says."
- **Why the cell says "the first note".** The plate prints its notes unnumbered, and the COVID-19 relief note comes first ("Federal revenue includes $39.2 billion in one-time COVID-19 relief, ..."); the second note is the Census Bureau's count of school systems. "Note 2" would send a reader to the wrong note, so the cell says "the first note". The figure is the rescore's, $39.2 billion, and the cell now says it the way the source line does ("Federal revenue includes $39.2 billion in COVID-19 relief funds.").
- **How.** The words come from the research lead's frozen data file (`census-school-system-finances-2024.csv`, row 4's note, which names row 5 of the file), and the table leaves row 5 out by `where`. The spec's `typography.replace` now prints the revision in place of the file's note, as the kit sets printed words for a spec, and a line in `notes_internal` says why. The data file is unchanged, and no other word on the plate holds the replaced phrase.
- **File:** `work/build/chart-kit/specs/s90.json`. `maker_i_round4_derive.py` does not write this spec, so it is unchanged for RS-4.
- **Proof.** `maker_i_round4_derive.py --figures S90`: all passed. Kit: `build s90 --no-png` PASS, 0 faults, and `build --all --no-png` as above. Strict guide build: exit 0, 0 warnings; the page prints the revision once and "row 5" nowhere.
- **Bytes:** kit figure 5,675 to 5,709; the plate in the page (`s-14-s90`) 6,439 to 6,473.

### RS-5: the entries' related rules

- **What changed.** 14.32 and 14.74 now list Rule 14.142; 14.96 and 14.135 list Rule 15.22; 14.88 lists Rules 11.10 and 11.11 after 11.2, in chapter order, and Rule 15.23 last. Before and after: 14.32 ["14.9", "14.11"] to ["14.9", "14.11", "14.142"]; 14.74 ["14.9", "13.5", "13.1"] to ["14.9", "13.5", "13.1", "14.142"]; 14.96 ["11.9", "14.88", "14.97"] to ["11.9", "14.88", "14.97", "15.22"]; 14.135 ["14.96", "14.112", "14.138"] to ["14.96", "14.112", "14.138", "15.22"]; 14.88 ["11.1", "11.2", "14.12"] to ["11.1", "11.2", "11.10", "11.11", "14.12", "15.23"].
- **Files:** `work/build/guide/entries/14-032.json`, `14-074.json`, `14-088.json`, `14-096.json`, `14-135.json`. No generator writes these entries: they are the makers' data, which `phase3_ch14_build.py` reads, so the change goes in them and the script then writes `work/build/guide/chapters/14-data-visualization.json` (each rule's `related_rules`, and chapter 15 added to the related chapters of 14.88, 14.96 and 14.135) and `work/build/guide/entries/14-example-log.json` (Rule 14.137's row takes RS-2's title).
- **Proof.** `phase3_ch14_build.py --check` before: 98 of 99 current, the example log behind by RS-2's title alone. After the run: 144 rules, 0 faults, 2 files written; `--check`: 99 of 99 current. Strict guide build: exit 0, 0 warnings, pictures 101 hidden and 315 open; chapter 14 2,117,476 bytes of 2,803,941; page 12,178,911 bytes (the engineer's work in progress included).
- **What a reader sees.** The page prints a rule's related items as chapters only (`guide_build.py`, `related_inline()`), and no code prints `related_rules`. So 14.88, 14.96 and 14.135 now show "15 Systems graphics" under Related chapters (14.135 had none), while the rule numbers themselves, and Rule 14.142 on 14.32 and 14.74, reach no reader. RP-3's reader, who picks columns with a moving average and never meets Rule 14.142, still meets it only through the selection guide's road. See Requests, 1; the creative director should know before rescoring R5-G.

## Not fixed

- **RS-5, the visible half.** The five entries carry the related rules RP-3 asks for, but the page shows rule-level related items only as chapters, so Rule 14.142 on 14.32 and 14.74 is not shown, and 11.10, 11.11, 15.22 and 15.23 show only as chapters 11 and 15. Printing `related_rules` as rule links is a page change in the engineer's `guide_build.py`, outside this pass's rows (Requests, 1).
- **Outside the six, for the register.** Rules 11.8 and 11.9's correct plates (`s-11-8-correct`, `s-11-9-correct`) are drawn by the same `records_piece()` and stay open stages for the same reason: their alts lack the title ("Where three records requests stand", "Where three agency rules stand") and "What the marks mean", and 11.9's lacks "How to send a comment". `alt_key()` would close both in two lines each, which would move the counts to 103 hidden and 313 open. I left them, since this pass asks for exactly six.

## Calls

- D3-xxx | RS-1: the six tracker alts open "Illustrative." and the plate's title, and end on the key in words, each mark's word with its shape in Rule 11.2's words, in the key's order | so each alt carries every word its picture holds in the picture's own order, and `plate()` hides the picture under D3-2153's test
- D3-xxx | RS-2: S91's title is "Of the federal district courts’ three kinds of judge, only district judges serve for life, except in Guam, the Northern Mariana Islands and the Virgin Islands." (26 words) in place of the rescore's example | the example's "the three kinds who hear federal trial cases" takes in every federal trial court, and judges of the Court of International Trade also hold trials and serve for life, so it would claim more than S91's data holds (H08); the data lead's CD-S4 universe stays
- D3-xxx | RS-2: the S91 scope check in `maker_i_round4_derive.py` reads the new title's words with the measure line's, and a new check holds the title at 27 words or fewer | the old check matched the old title's words; the universe it guards is unchanged
- D3-xxx | RS-4: S90's row 4 note reads "Includes $39.2 billion in COVID-19 relief funds, as the first note says." | the plate prints the COVID-19 relief note first and unnumbered, so "note 2" would point to the Census Bureau's note; the words match the source line's
- D3-xxx | RS-4: the note prints through S90's `typography.replace`, and the research lead's frozen data file is unchanged | the file's "(row 5)" is true of the file; only the printed table leaves row 5 out
- D3-xxx | RS-6: Rule 14.143's failure plate lists each step whole, cause first | that list prints no supposition, so a step opening "So" would read as if Loop B4's last step caused it

## Requests

1. **To the engineer, through the main session (RS-5).** `guide_build.py` prints a rule's `related` as chapters (`related_inline()`) and never prints `related_rules`, which `phase3_ch14_build.py` writes for every chapter 14 entry. For RP-3's second half to reach a reader, the page would need to print an entry's related rules as links beside Related chapters. That is a page change, so it may be a board 3 item; until then the creative director should read RS-5 as data only.
2. **To the research lead or the engineer (RS-4).** The kit's CSV export of S90 (`oa-chart.mjs build s90`, `20261120_S90-By-The-Numbers-Panel.csv`) still prints row 4's note as "Includes COVID-19 relief funds (row 5)" while it leaves row 5 out, since `typography.replace` sets printed words and the export carries the data. The guide page is right. The export is fixed either in the frozen data file's note (the research lead's) or by the export applying the spec's printed words (the kit's).
3. **To the main session.** I edited one check in `maker_i_round4_derive.py`, which RS-4's row names only if it writes S90's spec (it does not). Its S91 check matched the old title's words, so RS-2 could not pass without it. Revert it if you would rather route it to the infographics maker; the title change then fails that one check.

## Tested

## Requests

## Tested

- `apply_systems_ch11.py` run before my edit (no diff) and after it (exit 0); only the six `alt` fields in `manifest-systems.json` changed, and the six fragments are byte for byte as committed.
- D3-2153's test, the build's own `picture_words()` and `alt_words()` imported from `guide_build.py`, on the six stages: no word missing from any alt (scratch script `lacks.py`).
- Strict guide builds to my scratch folder, one at a time: before any change (exit 0, 0 warnings, 95 hidden, 321 open), after RS-1 (exit 0, 0 warnings, 101 and 315, the six stages named above the only ones to leave `open_stages`, none joined), after RS-6, after RS-2 and RS-4, and after RS-5 (each exit 0, 0 warnings, 101 and 315).
- `phase3_ch14_complex_build.py --check` before RS-6 (10 of 10 current); the generator after it (0 faults) and `--check` (10 of 10 current), the direction check reading the supposition for Loop R10's first step.
- `maker_i_round4_derive.py --figures S90 S91`: all passed.
- Kit: `oa-chart.mjs build s90` and `build s91`, before (with PNG, see Status) and after (`--no-png`), PASS with 0 faults; `build --all --no-png`: 96 specs PASS, exit 0; `plate-share.json` was not rewritten.
- `phase3_ch14_build.py` and its `--check`: 99 of 99 current after RS-5.
- The printed words in the built page: S91's new title, S90's new note once and "row 5" nowhere, Loop R10's first step, and the related chapters of the five entries.
- A script check of every new string and these notes for em and en dashes, U+2011 and the listed fillers, hedges and corporate verbs: none left. A full read of each new string against chapter 02's rules, from the left and from the right (DR-124): the words name no party or official, and S91's and S90's figures are the data's.

- Pattern violations left in my new words, by type: em dashes 0, en dashes 0, U+2011 0, listed fillers and intensifiers 0, corporate verbs 0, hedges 0 (by script); corrective negation, matched pairs, triplets, parallel runs and slogan closers 0 found (by reading, which no script can rule out).

## Not tested

- How the six alts sound in a screen reader, and whether each is heard once with the picture hidden: the accessibility lead's check, which needs a browser.
- S90, S91 and Rule 14.143 at 390 px or on Charcoal after the change: no browser in this run, by the run's condition.
- The guide check (`guide_check.js`): the main session runs it on the joined build.
- The status line's timing for Loop R10's first step (its hold drops from 16,500 to 15,000 ms by the script's formula); I did not run the stepper.

## Change log

Created: `work/handoffs/phase-3/20261120_Second-Pass-Editor-Notes.md` (this file).

Modified, generators and data: `work/build/scripts/phase-2/apply_systems_ch11.py` (RS-1); `work/build/scripts/phase-3/phase3_ch14_complex_build.py` (RS-6, handed over at 16:45 UTC); `work/build/chart-kit/specs/s91.json` (RS-2); `work/build/scripts/phase-3/maker_i_round4_derive.py` (RS-2's check); `work/build/chart-kit/specs/s90.json` (RS-4); `work/build/guide/entries/14-032.json`, `14-074.json`, `14-088.json`, `14-096.json`, `14-135.json` (RS-5).

Modified, outputs written by those generators: `work/build/guide/specimens/manifest-systems.json` (RS-1); `work/build/guide/specimens/s-14-143-correct.html` (RS-6); `work/build/guide/chapters/14-data-visualization.json` and `work/build/guide/entries/14-example-log.json` (RS-2 and RS-5).

Scratch only, outside the repository: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/318bf243-c48f-583b-8dd6-5600224b4263/scratchpad/c08/editor/` (the builds, their reports, the kit outputs and the check scripts `lacks.py`, `text.py` and `figbytes.py`).

