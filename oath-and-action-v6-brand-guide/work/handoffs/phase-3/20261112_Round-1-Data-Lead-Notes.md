# Round 1 data lead notes

Oath & Action Edition 06, Phase 3, round 1. The data visualization and systems lead, November 12, 2026, under `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. I write only this file and the "Data lead sign-off" section of the round 3 data plan, which the main session asked me to fill; every change to another agent's file is a numbered request below.

## Summary

- **Round 3's data plan: signed off with twelve changes**, written into `work/handoffs/phase-3/20261112_Round-3-Data-Plan.md`, section "Data lead sign-off". No dataset is replaced; every row may be fetched. Rule 01.9 holds in rounds 0 to 3 and for the chapter as a whole, and the editor's rule plates enter the count.
- **Round 1 charts:** in progress (section "Round 1 chart sign-off" below).
- **Chapter 15:** waiting for the systems designer's plates.

## Routine calls

- D3-xxx | Round 3's data plan is signed off with twelve changes; no dataset is replaced | Rule 01.9 and DR-229 hold on a scripted recount of both plans; the changes fix data that could not be drawn honestly as planned
- D3-xxx | Row 95's adjacency matrix groups V7's variables by its ten regions, not its ten domains | V7 gives 20 of its 51 variables no domain and nine two domains; regions place every variable once, so the studio assigns nothing
- D3-xxx | Row 108's locator counts under taking part, trust and shared norms (V7 I146), and row 102's journey map under Congress, agencies and public services (V7 I062) | Each question's own subject: a public meeting, and a benefit's paperwork path, the domain row 83 already takes
- D3-xxx | The editor's rule plates count toward Rule 01.9: a correct and failure pair on the same data is one example, on different data two; plates with no subject stay out | Rule 01.9 counts the examples a reader meets in a chapter, and a plate on data is one
- D3-xxx | Row 96's arc diagram draws one chamber's bills | No member can cosponsor a bill in the other chamber, so arcs across chambers cannot exist
- D3-xxx | Row 100's Sankey carries cash on hand at the start and end of the cycle | A flow through one node must balance; receipts and spending in a cycle do not

## Requests

### To the research lead (round 3 data plan)

The twelve changes in the plan's "Data lead sign-off" section, by row: 95, 108, 102, 86, 90, 96, 100, 94, 109 and 111, 113, 83, 87.

### To the engineer

- **DL-E1.** Before round 3 draws, measure one county map (about 3,100 paths) with its table equivalent against chapter 14's stop, with ENG-10, and say whether a county map's table may group by state with every row kept in the CSV export. The dot density map draws its dots from county counts and a recorded seed, so the page carries no element per dot.

### To the editor

- **DL-ED1.** Rule 14.7's plates need party data. For the other rule plates, pick data from the domains with most room in chapter 14's count: news and records (3 of 95), taking part (5), competition (5) and checks on power (5).

## Tested

- `recount.py` (scratch, `phase-3/round-1/data-lead/`): read the round 1 and 2 plan's 82 rows and the round 3 plan's 32 rows and recounted Rule 01.9; it matches both plans' tables, and gives the figures with my changes.
- V7 queries by script on `work/extract/atlas-v7-data.json`: issues I062, I015, I054, I084, I093, I104, I146, I170, I077, X02 and X14 with their domains and subsystems; every domain's subsystem names; PW03's decision makers; the eleven routes; R-01 and R-02's routes; nodes' domains, clusters and regions; links by type and polarity; the 10 by 10 region matrix (44 cells filled).
- `ballotpedia-rcv-prohibitions-by-state.csv` read row by row for row 87's branches.

## Not tested

- No fetch: I did not open any publisher's page, so the claims about FEC, Census, CMS, Congress.gov and DOL files in the changes (the FEC totals' cash-on-hand fields, the DOL table's as-of day, which states hold unusual House seats) are for the research lead to confirm at the fetch.
- Whether Tennessee's act reaches city elections: I read only the frozen scope note.
