# Round 2 research notes

Oath & Action Edition 06, Phase 3, round 2. Research lead (`oa-research-lead`), November 12, 2026, under `work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Kept current as the work goes, since the container can restart.

## Summary

Started 18:56 UTC.

**Row 113 (done 19:00 UTC).** The round 3 plan's row 113 named the four January 1 panels from Dustin's Department of Labor download but not DR-243's sentence. Its cells and its note now say that the atlas's July 1, 2026 count prints beneath the maps as one sourced sentence, read by script from V7 claim CL1516 (graded documented: 30 states and DC above $7.25, 13 at $7.25, Georgia and Wyoming at $5.15, five with no minimum wage law), citing the Department's "State Minimum Wage Laws" page updated July 1, 2026 (V7 source K1508, accessed October 15, 2026). Nothing else in the file changed (git shows two lines).

**The data lead's R1 and R2 (done 19:10 UTC).**
- **R1, `census-stc-state-tax-collections` (S50).** The DC row is the Bureau's own: the FY2025 flat file prints a DC column (22 of 25 tax items with a value, $11,261,267 thousand), and its U.S. column equals the 50 state columns' sum exactly. Every frozen state row and the DC row reproduce from the flat file and the population file. The U.S. row kept the 50 states' taxes but divided them by the nation's 340,003,797 residents, DC's included; it now uses the 50 states' 339,312,487, so taxes per resident read $4,526.3401 in place of $4,517.137. Its code stays `US`, and its name is now "All 50 states". The DC row stays, outside the total; S50 already leaves it out.
- **R2, `treasury-mspd-debt-subject-to-limit` (S64).** Public Law 119-21, section 72001 (139 Stat. 332, approved July 4, 2025), read on govinfo.gov today: the limit "is increased by $5,000,000,000,000". Public Law 118-5, section 401, suspended the limit through January 1, 2025 and raised it on January 2, 2025. The frozen table agrees (no limit through December 2024; $36,103,995.66 million from January 2025; $41,103,995.66 million from July 2025). The sidecar's qualification and a new note now cite both laws.

**Round 4's data plan:** in progress.

**Maker B's derived files:** not landed at 19:10 UTC (`maker_b_round2_derive.py` does not exist yet).

## Routine calls

- D3-xxx | Row 113's sentence reads V7 claim CL1516 and names source K1508, with the counts in the claim's own supporting text | DR-243 asks for the atlas's July 1, 2026 count as a sourced sentence; the claim holds the counts, and K1508 is the page it cites
- D3-xxx | The state tax file keeps the Bureau's DC column as its own row, outside the U.S. total | The publisher's flat file prints it, and C1 freezes a table as published; a chart of the states leaves it out
- D3-xxx | The U.S. row of state tax collections divides the 50 states' taxes by the 50 states' residents and is named "All 50 states", code `US` kept | Numerator and denominator then count the same places (data lead's R1); the code is the Bureau's own column name, and maker B reads it as the reference row
- D3-xxx | Round 2's fix scripts live in the research lead's scratch folder, not in `work/build/scripts/` | The round 2 ownership table gives the research lead data files, the ledger, the plans and its notes, and no script; each script refuses to write unless the frozen file reproduces from the publisher's file, and a rerun writes nothing

## Requests

- **To the main session.** S50's file has landed (one line: the U.S. row is code `US`, "All 50 states", 339,312,487 residents, $4,526.3401 per resident; the DC row stays and S50's `where` already drops it). S64's law is confirmed on govinfo.gov.

## Tested

- Host reachability for round 4's candidate sources, 18:57 to 19:01 UTC, logged in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/65b3d20e-985e-5fe9-b272-d7d01bd821cd/scratchpad/phase-3/round-2/research/reach/` (`reach-1.tsv`, `reach-2.tsv`, and `reach-3.tsv` for HEAD requests on planned paths, no body read). No round 4 dataset was fetched.
- Row 113: V7's CL1516, K1508, Q255 and I104 read and asserted by script (`scripts/row113_v7_read.py` in the scratch folder); the round 3 plan's diff shows two lines changed; no em dash or U+2011 in the file.
- R1: the flat file and population file fetched into their own folder (`dl/stc-r1/`, fetch log with SHA-256 prefixes); the fix script asserts the U.S. column equals the 50-state sum, every state and DC row equals the publisher's figures, and the old U.S. population equals the nation's; it changed one CSV line and the sidecar; a rerun wrote nothing (hashes compared).
- R2: both public laws fetched from govinfo.gov (`dl/plaw-r2/`), read with Python's HTML parser; the script asserts the table's empty limit through December 2024 and the $5 trillion step between June and July 2025 before writing; a rerun wrote nothing.
- The data check, `data_round0_build.py --check`: 100 tables, 0 faults before the fixes and after each.

## Not tested

- Why the Bureau's flat file prints DC outside its U.S. total; the survey's methodology and user notes pages, read today, say nothing about DC (ledger claim 27).
- S50 and S64 rebuilt with the changed sidecars (the makers' step).

## Files

Modified:
- `work/handoffs/phase-3/20261112_Round-3-Data-Plan.md` (row 113's cells and note only)
- `work/build/data/census-stc-state-tax-collections.csv` (the U.S. row) and `.meta.json` (geography, two column descriptions, two notes)
- `work/build/data/treasury-mspd-debt-subject-to-limit.meta.json` (qualification and one note)
- `work/research/20261021_Research-Ledger.md` (Part 7's "Round 2 fixes", claim 27, a change log line)

Created:
- `work/handoffs/phase-3/20261112_Round-2-Research-Notes.md` (this file)

Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/65b3d20e-985e-5fe9-b272-d7d01bd821cd/scratchpad/phase-3/round-2/research/` (reach logs, downloads with fetch logs, scripts).
