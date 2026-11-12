# Round 2 red team: accessibility and the production test

Oath & Action Edition 06, Phase 3, round 2, November 12, 2026. Written by the UX and accessibility lead (`oa-ux-accessibility-lead`) as reviewer for `work/handoffs/phase-3/20261112_Phase-3-Round-2-Review-Brief.md`. I then ran a simulated panel. The panel is simulated and untested with real people. Paths are relative to `oath-and-action-v6-brand-guide/`.

Status: in progress. This report is written as I go, so the container can restart without loss.

### Working notes (to be folded into the sections below)

- Scripts off, full build, 1440 px: 26 round 2 entry figures (S43 to S64, S01, S06, S08, S10) show title, alt, scripts-off line, source and an open table; every header has scope; rows equal my count from the data files (derived summaries for S49, S51, S52, S56). S58 has 37 blank "Change in the survey" cells.
- Kit builds of the 26 specs into scratch: all PASS, 0 faults.
- Narrow probe on kit pages at 656, 358, 326, 296, 256 px: no text outside a drawing, no text on text, no page error.
- S58: the margin-of-error band is Stone step 1, rgb(204, 202, 197) on Newsprint rgb(220, 217, 210), about 1.15 to 1; it is barely seen at 656 px and lost at 358 px and under. Candidate Must fix.
- S48: at 256 px "1 independent, 2 vacant" sits on the inner rows of seats; at 296 px it touches them.
- S50: at 256 px the dashed "All 50 states" line runs through the 0 of "Alaska $2,290".
- S44: at 256 and 296 px gridlines cross the minus sign of several step values.
- S45: the two-to-four-units segment is under 1 px tall for 2009 to 2025 at every width.
- S57: intervals narrower than the 7 px dot hide inside it: FL at every width; CA, FL, NY, TX at 256 px.


## 1. Score

Pending.

## 2. Must fix

Pending.

## 3. Should fix

Pending.

## 4. The seven named places

Pending.

## 5. Questions for Dustin

Pending.

## 6. Tested

Pending.

## 7. Not tested

Pending.

## Change log

Created: this report; `work/handoffs/phase-3/round-2-production-test/`.
