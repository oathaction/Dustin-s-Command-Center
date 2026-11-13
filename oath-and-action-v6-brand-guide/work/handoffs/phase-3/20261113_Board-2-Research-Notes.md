# Board 2 research notes

Oath & Action Edition 06, Phase 3, board 2. Research lead (`oa-research-lead`), November 13, 2026, under `work/handoffs/phase-3/20261113_Board-2-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Kept current as the work goes, since the container can restart.

## Status

17:08 UTC. Started. Order: A5's `snapshot_once` variants, then the V7.1 facts, then DR-258's rerun.

17:12 UTC. The main session reports Concepts V2 and the Atlas Visual System uploaded, each equal to the Phase 0 manifest; DR-258's rerun now covers all 2,644 comparisons from all three pages, written as `work/research/20261113_Atlas-Recheck-Full-Data.json` and `-Full-Table.md` (in place of the V5P files, not yet started). A5 still first.

17:16 UTC. **A5 done:** six `snapshot_once` variants in six sidecars for S10, S21, S23, S38, S39, S60 and S63 ("Variants for the editor"); the kit check passes all seven with the variants; the data check reads 125 tables, 0 faults. Waiting on the data lead's sign-off; the editor sets the specs. Next: the V7.1 facts.

## Variants for the editor

**A5 (DR-257) done at 17:12 UTC; for the data lead's sign-off.** Six variants in six atlas sidecars, one for each line an older spec prints with October 15, 2026 twice. The stored `printed_source_line` and every existing variant stay byte for byte; each sidecar gains one key and nothing else (asserted by script; `git diff` shows one added line each, plus the `source_line_variants` wrapper where a sidecar had none). Script: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/research/scripts/a5_variants.py` (a rerun writes nothing).

**How they were found.** By script on this chat's strict build (`.../board-2/main/guide.html`, 11,235,128 bytes), reading every kit figure's grade line and source line (96 figures with a source line), and by script over every `v7-*` sidecar line.
- The brief's test, grade line and source line both printing the date, finds six figures: S60 and S63 (older), and S67, S68, S71 and S74 (round 3, each already printing the date once in its source line under D3-1327 and D3-1493).
- The fault DR-257 names, a source line that prints the date twice, finds seven figures, all older: S10, S21, S23, S38, S39, S60 and S63. They print 6 of the 21 sidecar lines D3-1308 counted (21 lines in nine sidecars, recounted today: `v7-issues` 11, and one each in `v7-claims-by-grade` and `v7-claims-by-hub-and-grade` twice (printed and `phase_2_wording`), `v7-claims-drug-prices`, `v7-issue-status-checks-on-power`, `v7-numbers`, `v7-pathway-electric-decision-makers`, `v7-rcv-local-routes`, `v7-routes`). The other 15 lines print nowhere on the page (each line's text counted on the page by script): `v7-issues`' printed line and domains D02 to D10, the two `phase_2_wording` lines, and the printed lines of `v7-pathway-electric-decision-makers` (S68 prints its variant), `v7-rcv-local-routes` (S67 writes its own two-source line) and `v7-routes` (S71 reads `usgov-v7-route-grid`).
- No source line outside chapter 14's kit figures prints the date twice; every other atlas line on the page already reads "snapshot of October 15, 2026" once.

**Rule for the words.** S68's form: the period phrase and the "Snapshot of October 15, 2026." sentence become one "snapshot of October 15, 2026" in the period's place, before "United States." Where the stored period said the atlas checked something ("432 of the 433 claims checked on", "verified through", "checked"), the fact stays as a sentence after the geography, "The atlas checked ... on that date.", each checked against the model: 432 of the 433 claims carry `verified_on` 2026-10-15 and CL1723 carries none; all 11 drug-price claims carry 2026-10-15; all eight headline figures carry `verified_status` "checked October 15, 2026"; all six statuses carry `checked` 2026-10-15. Each new line prints the date once, holds no em dash, U+2011 or straight quote, and keeps the stored line's qualification words.

| Spec | Sidecar | Prints today | Set `source_line` to variant | New line |
|---|---|---|---|---|
| S10, S21 | `v7-claims-by-grade` | `printed_source_line` (no `source_line` key) | `snapshot_once` | Source: Oath & Action’s systems atlas, Who Do They Answer To?, claims register, 433 claims across 16 everyday questions, snapshot of October 15, 2026, United States. The atlas checked 432 of the 433 claims on that date. Grades are the atlas’s own, defined on its evidence page; a claim’s grade covers that claim alone. |
| S23 | `v7-claims-by-hub-and-grade` | `printed_source_line` (no key) | `snapshot_once` | Source: Oath & Action’s systems atlas, Who Do They Answer To?, claims register, 433 claims across 16 everyday questions grouped by its five topic hubs, snapshot of October 15, 2026, United States. The atlas checked 432 of the 433 claims on that date. Grades are the atlas’s own, defined on its evidence page; a claim’s grade covers that claim alone. |
| S38 | `v7-issues` | `domain_d01` (its own `source_line`) | `domain_d01_snapshot_once` | Source: Oath & Action’s systems atlas, Who Do They Answer To?, issue records in the domain of news, records and public information, 17 of 194 issues, snapshot of October 15, 2026, United States. Grades are the atlas’s own. |
| S39 | `v7-claims-drug-prices` | `printed_source_line` (no key) | `snapshot_once` | Source: Oath & Action’s systems atlas, Who Do They Answer To?, claims register, pathway PW06, 11 claims about drug prices, snapshot of October 15, 2026, United States. The atlas checked all 11 on that date. Each claim states its own period and limitation; grades are the atlas’s own. |
| S60 | `v7-numbers` | `printed_source_line` (no key) | `snapshot_once` | Source: Oath & Action’s systems atlas, Who Do They Answer To?, headline figures, eight figures, snapshot of October 15, 2026, United States. The atlas checked all eight on that date. Each figure carries its own source and qualification. |
| S63 | `v7-issue-status-checks-on-power` | `printed_source_line` (no key) | `snapshot_once` | Source: Oath & Action’s systems atlas, Who Do They Answer To?, issue records, status of six issues on checks on power, snapshot of October 15, 2026, United States. Statuses may have changed since that date. |

The old lines, for the editor's list: S10 and S21 "…, 433 claims across 16 everyday questions, 432 of the 433 claims checked on October 15, 2026, United States. Snapshot of October 15, 2026. Grades are…"; S23 the same with "grouped by its five topic hubs"; S38 "…, 17 of 194 issues, as of October 15, 2026, United States. Snapshot of October 15, 2026. Grades are the atlas’s own."; S39 "…, 11 claims about drug prices, verified through October 15, 2026, United States. Snapshot of October 15, 2026. Each claim…"; S60 "…, eight figures, checked October 15, 2026, United States. Snapshot of October 15, 2026. Each figure…"; S63 "…, status of six issues on checks on power, as of October 15, 2026, United States. Snapshot of October 15, 2026. Statuses may…". The full old and new lines are in `.../board-2/research/out/a5_dry.json`.

**For the editor.** The kit's check accepts a spec's `source_line` only when it equals the sidecar's printed line or a variant, so copy each line exactly from the sidecar (the six specs that print the sidecar's line today need a `source_line` key added). S60's and S63's grade lines keep "as of October 15, 2026", as S68's does (D3-1493). The two sentences "The atlas checked … on that date." are words the editor may tighten; tell me and I change the variant to match, since the check reads it word for word.

**Bytes, each plate before and after (kit `check`, as the guide places it, frame about 750 more):** S10 7,403 to 7,406; S21 5,679 to 5,682; S23 6,209 to 6,212; S38 10,041 to 10,017; S39 10,277 to 10,281; S60 9,061 to 9,077; S63 10,355 to 10,331. Every plate stays under the 13,322 share per plate the kit reads and under 15,000 (D3-1328). A5 changes no figure, no drawing and no table: only the source line's words.

**A rerun of the writer scripts would drop the variants.** Four sidecars come from `research_v7_extract.py` (mine) and two from `data_round0_build.py` (the engineer's); both write each sidecar whole. This pass lets me write only the sidecars, so neither script is edited. The patches that make each script carry its variant beside the printed line (D3-1413's form) are in scratch, `.../board-2/research/out/a5_proof/research_v7_extract.diff` and `data_round0_build.diff`; applied to in-memory copies and run into scratch, the two scripts rebuild all 34 of their V7 files byte for byte equal to `work/build/data/` as it now stands. No step of A6's chain runs either writer (the data check and the V7 check write nothing). Request R-B2-1 below.

## V7.1 facts

Pending.

## DR-258 rerun (V5 Polished)

Pending.

## Requests

- **R-B2-1, to the main session and the engineer (not blocking A6).** Carry A5's variants in the two writer scripts so a rerun keeps them: `research_v7_extract.py` (mine; this pass's scope let me write only sidecars) and `data_round0_build.py` (the engineer's). The diffs are in scratch (`.../board-2/research/out/a5_proof/*.diff`), proven to rebuild every V7 file they write byte for byte as it now stands.

## Routine calls

## Tested

## Not tested
