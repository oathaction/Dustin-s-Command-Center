# Round 2 maker B notes: distribution and density, correlation, uncertainty and estimates

Oath & Action Edition 06, Phase 3, round 2, November 12, 2026. Maker B, a senior newspaper graphics editor for distributions, relationships and uncertainty. Brief: `work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch and captures: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/65b3d20e-985e-5fe9-b272-d7d01bd821cd/scratchpad/phase-3/round-2/maker-b/`.

## Summary

In progress. Order: `range-bar` first (R2-4), then the other ten forms, R2-2's derived files, specs, entries, sketches last.

**RANGE-BAR READY** (18:58). `work/build/chart-kit/forms/range-bar.js` is written and S57 (draft words, final words after the data lead's rulings) passes `oa-chart.mjs build` with 0 faults at 1440 and 390 px on both grounds and the guide widths. For the editor (ED-E4): `encode` takes `category`, `value`, and `margin` (or `low` and `high`), with `key` (optional, the code a label names) and `status` (optional). `labels.reference: "US"` draws the reference row as a line across the rows, named over it by `labels.reference_label` (`"Nation {value}%"`); `labels.test: "reference"` gives an open dot to every row whose gap to the reference sits inside the gap's own margin (the square root of the sum of the two squared margins, as Rule 14.9's specs say); `labels.value` sets the right column's words (`"{value}%"`; `{margin}`, `{low}`, `{high}` also fill); `labels.named` and `labels.point` as in the other listing forms; `labels.short` gives names printed only on a phone; `labels.key_filled`, `key_open`, `key_interval` draw an optional key above the rows. A trial of Rule 14.9's plate spec on the form (form and `encode` changed, `labels` as above) passes at every width and finds the same five states past the margin and five within as the plate's note: scratch `.../maker-b/s-14-9-trial.chart.json`.

## Routine calls

## Requests to the engineer

## Requests to the research lead

## Requests to the data lead

## Requests to the editor

## Tested

## Not tested

## Files
