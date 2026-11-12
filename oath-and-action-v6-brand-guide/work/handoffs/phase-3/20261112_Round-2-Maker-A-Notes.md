# Round 2 maker A notes: composition, and gauges and indicators

Oath & Action Edition 06, Phase 3, round 2, November 12, 2026. Maker A, briefed as a senior data journalist and graphics editor who builds part-to-whole charts and dashboards. Brief: `work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`. Rows: maker "A" in `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`, rules 14.46 to 14.57 and 14.85 to 14.92. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

In progress (19:05). Forms written and passing their first builds: `stacked-share-bar`, `waterfall`, `stacked-column`, `stacked-area`, `treemap`, on the engineer's `K.parts.stack` (R2-C2). The data lead's rulings (a) to (g) and requests A1 to A6 are read and applied to S43 to S47 as they stand; S48 and S60 to S64 next, then entries, S18 (A2), and the sketches last.

| Rule | Spec | Form ID | Status |
|---|---|---|---|
| 14.46 | S10 (built) | percent-bar | entry to write |
| 14.47 | S43 | stacked-share-bar | form in progress |
| 14.48 | S44 | waterfall | form in progress |
| 14.49 | S08 (built) | unit-chart | entry to write |
| 14.50 | S45 | stacked-column | form in progress |
| 14.51 | S46 | stacked-area | form in progress |
| 14.52 | S47 | treemap | form in progress |
| 14.53 | S48 | parliament | form in progress |
| 14.54 | sketch | pie (reference) | to draw |
| 14.55 | sketch | donut (reference) | to draw |
| 14.56 | sketch | marimekko (reference) | to draw |
| 14.57 | sketch | 3D pie or bar (avoid) | to draw |
| 14.85 | S01 (built) | big-number | entry to write |
| 14.86 | S60 | indicator-row | form in progress |
| 14.87 | S61 | progress-bar | form in progress |
| 14.88 | S62 | step-tracker | form in progress |
| 14.89 | S63 | status-chips | form in progress |
| 14.90 | S64 | bullet-graph | form in progress |
| 14.91 | sketch | gauge (avoid) | to draw |
| 14.92 | sketch | thermometer (avoid) | to draw |

## Routine calls

- D3-xxx | S43 draws the nation as the first row, set apart by a gap (`labels.apart`), and the District of Columbia's renter part in the subject ink (`labels.named`); every other renter part takes the light fill and every owner part the track ink; the midline is 1 px in the text's ink | Rulings (a), (b) and (e)
- D3-xxx | S43 sorts by `code` with `values: ["US"]` first, then renter share, so the table reads in the drawing's order | The set-apart row leads both
- D3-xxx | S43 prints the state's code in place of its name where the full name would leave the bar under 60 percent of the row (phone widths) | A name over each of 51 bars would double the phone drawing to about 2,100 px; the table names every state
- D3-xxx | S44 draws all 30 Treasury lines with no folds; steps that add in diverging pair B's Verdigris end, steps that take away in its Prussian end, all receipts in the context ink, the deficit in the subject ink, connectors in the secondary ink at 1 px | Ruling (e) and A3; folding needs a derived file, and every line fits at 26 to 42 px a row
- D3-xxx | S44 prints each value beside its bar on the side its step moves to, on a halo of the ground, 3.5 px from the bar | On Charcoal the two diverging ends differ by 0.4 in lightness, so the key passes only where every step carries its value beside it (the kit's direct-label test); a value column at the right failed it
- D3-xxx | S44's line names follow S33's sentence case ("Payroll taxes" for Employment and General Retirement), through `labels.names`; the table keeps the Treasury's names | One wording across the two Treasury charts
- D3-xxx | S45 names each part beside the last column on desktop and in a key on a phone, with a 1 px gap of the ground between parts | Ruling (e); a gap keeps Charcoal and Prussian apart where the two-to-four part is a sliver
- D3-xxx | S45 prints the published total over 2006, 2011 and 2024 (`encode.total`), raised over any taller neighbor | The parts' sum differs from the total by rounding in several years (1,979.5 against 1,979.4 in 2006)
- D3-xxx | S46 names each band inside it at its right end, flush right, with each band's 2024 share past the edge | Ruling (e)
- D3-xxx | S46's text on a band sits on a patch of that band's own fill | The kit's forced-colors check reads rects and circles only, so a word on a path read as Canvas on Canvas; the patch is the band's ink and invisible
- D3-xxx | S47 folds the 11 functions under 6 percent into "All other functions, 11 in all" ($1,089.9 billion), so every tile prints its name and value at every width from 256 px | At 5 percent, Veterans' benefits and services (5.5 percent) could not hold its words at 296 and 256 px; one fold at every width keeps the drawings alike
- D3-xxx | S47's tile words take the text's ink on the light fill and on red, and the ground's dark on Charcoal, where the light fill is the context ink | Ruling (e): Charcoal on Pillar Red; light words on the context ink measured about 2.5 to 1

## Requests to the engineer

## Requests to others

## Tested

## Not tested

## Files
