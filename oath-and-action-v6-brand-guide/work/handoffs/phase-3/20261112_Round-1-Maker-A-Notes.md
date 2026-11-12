# Round 1 maker A notes: comparison, and tables and plain words

Oath & Action Edition 06, Phase 3, round 1, November 12, 2026. Maker A, briefed as a senior data journalist and graphics editor who builds lookup tables and comparison charts. Brief: `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`. Rows: maker "A" in `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

Read-first list done. Working one specimen at a time, simplest first. Each finished specimen has its form (when new), spec and entry, passes `oa-chart.mjs build` at every width on both grounds with parity, passes maker A's figure checks and words lint (both in scratch, `tools/figures.py` and `tools/words.py`), and has had its captures looked at at 1440 and 390 px on both grounds and in grayscale.

| Rule | Spec | Form ID | Status |
|---|---|---|---|
| 14.15 | S03 (built) | ranked-bar | entry to write |
| 14.16 | S17 | column | done: form, spec, entry 14-016; build passes; source line waits on request A1 |
| 14.17 | S18 | bar-benchmark-tick | done: form, spec, entry 14-017; build passes |
| 14.18 | S19 | dot-plot | done: form, spec, entry 14-018; build passes |
| 14.19 | S04 (built) | dumbbell | entry to write |
| 14.20 | S20 | slope | not started |
| 14.21 | S21 | lollipop | not started |
| 14.22 | S22 | grouped-bar | not started |
| 14.23 | S23 | small-multiple-bars | not started |
| 14.24 | sketch | radar (avoid) | waits for engineer's role classes |
| 14.125 | S15 (built) | results-table | entry to write |
| 14.126 | S36 | ranked-register | not started |
| 14.127 | S06 (built) | comparison-matrix | entry to write |
| 14.128 | S13 (built, maker B's spec) | sparkline-table | entry to write |
| 14.129 | S37 | heat-table | not started |
| 14.130 | S38 | filterable-lookup-table | not started |
| 14.131 | S39 | evidence-table | not started |
| 14.132 | S40 | tracker-list | not started |
| 14.133 | S41 | plain-table | not started |
| 14.134 | S42 | one-sentence | not started |

## Routine calls

- D3-xxx | S17 draws the ten complete Congresses, the 109th to the 118th, and leaves the 119th out with its partial count in a note | Data plan row 2 sets the last ten; a partial term beside full ones would read as a collapse
- D3-xxx | The column form sets the columns the title names in ink and the rest in gray, with no red | DR-234's one-in-ink pattern; a count of laws has no direction both sides would call good or bad, and red reads as alarm
- D3-xxx | The column form's phone drawing turns the columns into bars read top to bottom (`phone: differs`) | At 296 and 256 px ten three-digit values cannot sit over their columns; bars keep every name and value (Rule 14.12, DR-64)
- D3-xxx | A column fills its step in the same proportion a ranked bar fills its pitch (bar height over bar pitch, 0.57), in place of the monthly columns' 0.72 | Ten columns at 0.72 read as heavy slabs at twice size; the ratio comes from tokens, so the two comparison forms read alike
- D3-xxx | S18 draws the five fifths and gives the top 5 percent in a note | The top 5 percent sits inside the highest fifth; a sixth bar would count those households twice
- D3-xxx | The benchmark tick is an ink line on a keyline of the ground's color, and a value that would touch the tick prints inside its bar's end | The tick must read across a bar in ink; a value printed past the tick made the middle fifth's bar seem to reach 20 percent
- D3-xxx | S19 draws BJS's all-states row (318) as a dashed reference line, and that row stays in the table in rank order | The fix pass set the State row as the comparison base; the table holds every row the chart draws
- D3-xxx | S19 marks the six states whose prisons and jails form one system with open dots, and its table gives every state's reporting difference in words | Their rates include jail populations; Rule 14.11 marks a difference in the drawing
- D3-xxx | S19's title names the data's two ends, Massachusetts and Mississippi, as the range of the 50 states | The plan row names states only by the data; a range read from either side states the record (DR-93)
- D3-xxx | Reader text in maker A's specs and entries uses the typographic apostrophe (U+2019), as the built specs do | House style; the words lint now flags an ASCII apostrophe

## Requests

- **A1, research lead, `work/build/data/congress-gov-laws-by-congress.meta.json`.** Add `"source_line_variants": {"last_ten": "Source: Library of Congress, Congress.gov, laws by Congress, 109th to 118th Congress (2005 to 2024), United States. Retrieved November 11, 2026. A count of laws, short or long; the 119th Congress is still in session."}`. S17 charts the 109th to the 118th, as data plan row 2 sets, and H04 asks the source line for the charted period. Until it lands, S17 prints the sidecar's own line (93rd to 118th), which passes the check; then S17's `source_line` takes the variant.

## Tested

- S17: `node work/build/chart-kit/oa-chart.mjs build s17` passes, 0 faults: spec, data, table rows, source line, layout guard and chart check at 1440 and 390 px on Newsprint and Charcoal, the five guide widths (656, 558, 358, 296, 256) on Newsprint, and page-to-Node parity. Captures looked at: both grounds at 1440 and 390 px, and grayscale at Charcoal 1440 and Newsprint 390. Figure check `figures.py s17`, 8 assertions pass (274 the unique fewest of the ten; 482, 283, 442; under 400 since the 115th; the 119th's 138; the `where` rows). Words lint clean on `s17.json` and `14-016.json`.
- S18: build passes, 0 faults, at every width and both grounds with parity. Captures looked at: Newsprint 1440 and 390, Charcoal 390, and grayscale at Charcoal 1440 and 390. Figure check `figures.py s18`, 8 assertions pass (51.6 and 3.0; 8.5, 14.4, 22.6; the highest fifth over the other four together; fifths add to 100; 23.1; 0.08; each fifth 20 percent). Words lint clean on `s18.json` and `14-017.json`.
- S19: build passes, 0 faults, 51 rows (50 states and the all-states line), at every width and both grounds with parity. Captures looked at: Newsprint 1440, Charcoal 390. Figure check `figures.py s19`, 8 assertions pass. Words lint clean on `s19.json` and `14-018.json`.

## Not tested
