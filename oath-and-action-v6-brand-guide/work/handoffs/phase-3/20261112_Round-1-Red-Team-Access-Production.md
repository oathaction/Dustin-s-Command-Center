# Round 1 red team: accessibility and the production test

Oath & Action Edition 06, Phase 3, round 1, November 12, 2026. Written by the UX and accessibility lead (`oa-ux-accessibility-lead`) as reviewer, for `work/handoffs/phase-3/20261112_Phase-3-Round-1-Review-Brief.md`, then as the runner of a simulated panel. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch work is in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/256961f5-3911-5bd9-908d-f34ce0435ace/scratchpad/phase-3/round-1-review/access-production/`. The build reviewed is the strict build at `/tmp/claude-0/-home-user-Dustin-s-Command-Center/256961f5-3911-5bd9-908d-f34ce0435ace/scratchpad/phase-3/round-1-review/build/guide.html` (10,017,051 bytes).

Status: in progress. Sections fill as checks finish.

Working notes (to be folded into the sections below):
- Scripts off, 1440 px: all 45 kit figures in chapter 14 carry title, alt shown as words, the scripts-off line, source and an open table; every `th` has `scope`; rows equal an independent count from the raw data and the spec's `where` on all 36 specs counted (26 new and 10 built). S37 prints 424 of 550 cells blank; S25 two.
- Widths 1440, 1024, 720 at device scale 2 (200 percent), 390, 360, 320: all 45 draw, 0 guard faults, 0 page errors, no page scroll, smallest drawing text 13 px (12.99 at 723 px). Every table frame that scrolls has its tab stop. At 320 px all 25 chapter 15 plates scroll sideways in their frames (hint and tab stop present).
- Forced colors, Chromium's light emulation: 2,007 drawing texts at 1440 and 2,061 at 390, none in the ink of the paint under it.
- Forced colors with a dark theme (`colorScheme: 'dark'`): the plate stage keeps Newsprint (AX-S6, `forced-color-adjust: none`) while `kit.css`'s forced-colors block repaints the drawing in system colors. All 38 figures with a subject mark draw it white on Newsprint, 1.41 to 1; labels turn white with a 3 px black halo. Chapter 15's plates keep their own colors in both themes.

## 1. Score

Pending.

## 2. Must fix

Pending.

## 3. Should fix

Pending.

## 4. Questions for Dustin

Pending.

## 5. Tested

Pending.

## 6. Not tested

Pending.
