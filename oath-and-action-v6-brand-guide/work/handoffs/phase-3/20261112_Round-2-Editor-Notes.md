# Round 2 editor notes

Oath & Action Edition 06, Phase 3, round 2. Editor (`oa-editor`), November 12, 2026, under `work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Written as I go; the container can restart.

## Summary

- **DR-242 (D3-656), done.** Chapter 13's five chart titles end with a period: `s-13-7-all`, `s-13-7-children`, `s-13-7-fail-all`, `s-13-13-correct`, `s-13-13-fail-chart`. The change is in `work/build/scripts/phase-3/phase3_ch13_build.py`, which now fails a rerun that drops any of the five periods. `git diff` after the rerun shows the five `title` lines and the generator, nothing else.
- RS-S4: waiting on the data lead's ruling (f).
- Rulings (b) and (c): waiting on the data lead.
- ED-E13: waiting on the engineer's `plate_css` hook.
- Group lines 5 to 10: in progress.
- Words for maker A, maker B and the systems designer: started below.

## Routine calls

- D3-xxx | `s-13-7-all` takes the period: "Poverty among all people stood at 13.1 percent in 2025." | DR-242
- D3-xxx | `s-13-7-children` takes the period: "Child poverty stood at 13.4 percent in 2025." | DR-242
- D3-xxx | `s-13-7-fail-all` takes the period: "Poverty among all people stood at 13.1 percent in 2025." | DR-242
- D3-xxx | `s-13-13-correct` takes the period: "The Main Library will be open the most hours of the three branches." | DR-242
- D3-xxx | `s-13-13-fail-chart` takes the period: "The Main Library will be open the most hours of the three branches." | DR-242
- D3-xxx | Rule 13.7's correct plate keeps its alt byte for byte; it names both titles inside one sentence, and the second title's period already ends that sentence | DR-242 changes the titles only; a second period inside the alt would break its sentence
- D3-xxx | The chapter 13 generator fails a rerun if any of the five titles lacks its period | So a later rerun keeps DR-242

## Words for maker A

## Words for maker B

## Words for the systems designer

## Requests

### To the main session

- **Chapter 13's script-drawn chart heads still end without a period (for Dustin, if wanted).** DR-242 names five kit titles. Seven more chart titles in chapter 13's plates are drawn by the script and keep no period: Rule 13.1's four chart heads, Rule 13.6's jobs chart head on both plates, and the left chart head on Rule 13.7's failure plate, which now sits beside `s-13-7-fail-all` with its period. The failure heads in 13.1, 13.2 and 13.3 show faulty titles on purpose. I changed none of them, since D3-656 says nothing else in chapter 13 changes. If Dustin wants one rule for every chart title, the generator's `chart_head` can add the period to 13.1's four correct heads, 13.6's two and 13.7's failure head in one line.

## Tested

- `python3 -I work/build/scripts/phase-3/phase3_ch13_build.py` before any change: a rerun of the committed generator left `git status` clean.
- The same after DR-242: every check passes; `git diff` shows the five `title` lines in the five `.chart.json` files and the generator, and no other file changed (the chapter file, the manifest and all 27 plates are byte for byte as before).
- `node work/build/chart-kit/oa-chart.mjs check` on the five specs: 5 of 5 PASS, 0 faults.

## Not tested

## Files

- Modified: `work/build/scripts/phase-3/phase3_ch13_build.py`; `work/build/guide/specimens/s-13-7-all.chart.json`, `s-13-7-children.chart.json`, `s-13-7-fail-all.chart.json`, `s-13-13-correct.chart.json`, `s-13-13-fail-chart.chart.json`.
- Created: this file.
