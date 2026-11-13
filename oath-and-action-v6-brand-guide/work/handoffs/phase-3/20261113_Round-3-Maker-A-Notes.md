# Round 3 maker A notes: structure

Oath & Action Edition 06, Phase 3, round 3, November 13, 2026. Maker A, briefed as a senior graphics editor who draws exact, quiet explainer diagrams of how institutions work. Brief: `work/handoffs/phase-3/20261113_Phase-3-Round-3-Brief.md`. Rows: maker "A" in `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`, rules 14.96 to 14.103 (coverage plan 3.11). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c155381-70e7-5490-bd84-f6f867d97cb7/scratchpad/phase-3/round-3/maker-a/`. Written as I go; the container can restart.

## Summary

- 00:5x. Started. Read `CLAUDE.md`, the round 3 brief, the kit README, the plan file's round 3 rows, data plan rows 86 to 93 with the sign-off's changes 4, 5 and 12 and its conditions, round 2's maker A notes, S62, `step-tracker` and entry 14.88, and the seven datasets with their sidecars.
- 01:2x. All seven forms, specs S66 to S72, entries 14.96 to 14.103 and the mind map sketch are written, on the engineer's R3-5 parts (`link`, `node`, `node_size`, `tree`) and under the data lead's rulings (a) to (d): no named mark on any of S66 to S72, inks and grade lines as ruled. Each spec builds PASS with the sweep, 0 faults. `maker_a_round3_derive.py` writes S71's joined table and checks every figure in my titles, notes and alts (23 checks, 0 failed so far; S71 and S72 checks being added). R3-A1 landed (the research lead's Ballotpedia publisher). Now: the review pass at 1440, 390, 296 and 256 px on both grounds and in grayscale, then the strict build and the quick guide check.

| Rule | Spec | Form ID | Status |
|---|---|---|---|
| 14.96 | S66 | process-diagram | form, spec, entry; build passes |
| 14.97 | S67 | decision-tree | form, spec, entry; build passes |
| 14.98 | S68 | who-decides | form, spec, entry; build passes |
| 14.99 | S69 | org-chart | form, spec, entry; build passes |
| 14.100 | S70 | hierarchy-tree | form, spec, entry; build passes |
| 14.101 | S71 | comparison-grid | form, spec, entry, derived table; build passes |
| 14.102 | S72 | roll-call-grid | form, spec, entry; build passes |
| 14.103 | sketch | mind map (reference) | sketch 2,4xx bytes, entry |

## Routine calls

## Requests to the engineer

- **A-E1, `kit.js` (`K.table_groups`), needed for S72's weight:** let `table.group.by` take a list of columns, the group's key their values joined with ", " (so `words` and `agg: "key"` read the joined key, such as "Senate, D"), groups in first-seen order after the spec's `sort`. S72's member-by-member table is 77,142 bytes of HTML (the plate 81,880, against 24,576 far-over and the 13,852 share); grouped by chamber and party, with `count` and `count_eq` columns for yes, no and not voting, it prints 5 rows and the CSV export keeps all 533 members, DR-249's pattern. A single column cannot split a party by chamber.
- **A-E2, optional, `kit.js` (`K.group_cell`):** `agg: "list"`, a field's non-empty values in the group joined with "; ", and `agg: "count_set"`, the rows whose field is non-empty. S69 would then group by committee and list each committee's subcommittees in one cell (27 rows in place of 136), and keep every name in the page's table.

## Requests to the data lead

## Requests to the research lead

- **R3-A1, `ballotpedia-rcv-prohibitions-by-state.meta.json`:** its `publisher` reads "Ballotpedia. Secondary source". S67 draws this file with `v7-rcv-local-routes`, so its source line names both, and the kit's check for a spec of two datasets wants each publisher's words in the line, here "Ballotpedia. Secondary source", which no reader line says. Please set `publisher` to "Ballotpedia, a secondary source" (the words S07's printed line already uses), or tell me the words to print. S67 fails only this check until then.

## Tested

## Not tested

## Files
