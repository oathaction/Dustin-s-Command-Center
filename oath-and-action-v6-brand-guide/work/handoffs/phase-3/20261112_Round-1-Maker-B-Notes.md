# Round 1 maker B notes: shift and swing, change over time

Oath & Action Edition 06, Phase 3, round 1, November 12, 2026. Maker B, a senior newspaper graphics editor for time series and change. Brief: `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

Started. Read the brief's "Read first" list. Working one specimen at a time, starting with S29 (area chart).

| Rule | Form | Spec | Form file | Entry | Build | Captures looked at |
|---|---|---|---|---|---|---|
| 14.35 | Area chart | S29 | `forms/area.js` (new) | `14-035.json` | PASS, 0 faults | 1440 and 390, both grounds, grayscale |
| 14.36 | Step line | S30 | `forms/step-line.js` (new) | `14-036.json` | PASS, 0 faults | 1440 and 390, both grounds |
| 14.37 | Line with a data gap marked | S31 | `forms/line-data-gap.js` (new) | `14-037.json` | PASS, 0 faults | 1440 and 390, both grounds |

## Routine calls

- D3-xxx | S31 draws the unemployment rate on a scale from zero, with the gap as a light column under the grid and small dots where the line stops and starts | A cut scale would make a 1.1-point rise look like a tripling; the dots show the line ends on purpose
- D3-xxx | S31 runs January 2022 to October 2026, one month past the jobs charts' September end, to the latest month | The sidecar's printed line covers that window; the measure line gives the reason
- D3-xxx | S29's area takes the band fill, the role S13's approved panels give an area, with the line in the subject ink on top | The light fill read as a heavy gray block at 720 px; the band keeps the gridlines readable through the fill on both grounds
- D3-xxx | Entry files follow chapter 13's built rule shape where R2 leaves it open: `title` a clause ending in a period, `rule` a list of paragraphs, `why` an object with `text` and `basis` | R2 says the keys are a built chapter's rule plus three; the generator can then read both chapters alike

## Requests

- R-B3, to the engineer: a range in `where`, such as `{"month": {"from": "2022-01", "to": "2026-10"}}`, so S31 (and S33) need not list every month; S31's `where` lists 58 months today
- R-B2, to the engineer: a `dollars` number format (`dollars`, `dollars:N`, and a signed form) for axis ticks, table cells and `{y}` fills, so S30's axis and table can print $2,000 where today they print 2,000 and the measure line names dollars. S35 (benefit cliff) needs the same
- R-B1, to the research lead: add to `census-cbp-newspaper-publishers.meta.json` (and `census-cbp-civic-organizations.meta.json`) a `breaks_in_series` line saying County Business Patterns moved from SIC to NAICS with the 1998 data year, so S29's measure line ("The count starts in 1998, the first year County Business Patterns sorted businesses by the North American Industry Classification System") traces to the sidecar

## Tested

## Not tested
