# Round 1 research notes

Oath & Action Edition 06, Phase 3, round 1. Research lead (`oa-research-lead`), November 12, 2026, under `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Kept current as the work goes, since the container can restart.

## Summary

**Round 3's data plan** is written for the data lead's sign-off: `work/handoffs/phase-3/20261112_Round-3-Data-Plan.md` (ready 04:05 UTC). It covers all 32 round 3 forms (rules 14.93 to 14.124): 20 new data-bearing specimens, 3 built maps that become entries (S07, S12, S16) and 9 rule-only sketches. Thirteen forms change data from the coverage plan under DR-229 and one dataset per lesson. Counted for chapter 14 as a whole (about 95 examples with round 4 as planned), the largest domain, elections and representation, reaches 16 against a limit of 23, and no state passes 3 against 19. One download is needed (item 2, the Department of Labor's state minimum wage history, for row 113), and one request goes to the engineer (ENG-10, geometry in the data folder).

**Status.** Plan: waiting for sign-off. Route sources (FA, FR, ENF, CRT, AV, IC, CIV): in progress. Fetch and freeze: after sign-off.

## Routine calls

- D3-xxx | Round 3's rows continue the rounds 1 and 2 plan's numbering, 83 to 114, in chapter 14's rule order | One numbering across the data plans lets a spec, a sidecar and a ledger row cite the same row
- D3-xxx | Round 3's funnel draws Medicaid and CHIP renewal outcomes in place of the CPS voting tables | S04 and S16 already draw the CPS voting tables, rows 3 and 70 moved off them for the same reason, and V7 names the drop-out this funnel shows (I062)
- D3-xxx | Each round 3 domain follows V7's own issue for the topic where V7 has one, named in the row | The count then rests on the atlas's filing, which the data lead and a reader can check
- D3-xxx | The roll-call grid draws H.R. 5371, the November 2025 continuing appropriations act, with each chamber's recorded vote | H.R. 7008 already serves four specimens, and its Senate vote was on taking the bill up; H.R. 5371 has a recorded passage vote in each chamber
- D3-xxx | The network diagram draws both 2024 presidential joint fundraising committees the same way | Both parties use the mechanism, so Rule 01.11 asks for a case from each in the same form
- D3-xxx | Map geometry comes from the Census Bureau's 2024 cartographic boundary and Gazetteer files, frozen unprojected and unsimplified, with the kit projecting and simplifying at build (ENG-10) | Public-domain federal files; projection is a drawing choice, so the data stays neutral and the page carries only drawn paths
- D3-xxx | The district tile map's layout is the studio's own, from the Census Bureau's district centers | Published tile layouts are third-party work, study only under Master Brief section 2

## Requests

- **ENG-10, to the engineer: map geometry in the data folder.** As written in the round 3 plan's "Requests": `census-cb-2024-states.geojson`, `-counties`, `-cd119` in `work/build/data/`, longitude and latitude, unsimplified, with C1 sidecars plus `geometry_type`, `source_resolution` and `raw_file_sha256`; or the shape you set in your contracts.
- **To the main session: download item 2.** The Department of Labor's state minimum wage history page, https://www.dol.gov/agencies/whd/state/minimum-wage/history, saved as HTML or PDF and attached as is (dol.gov refused this container, HTTP 403, 03:58 UTC). It serves row 113 only.
- **To the data lead, through the main session:** the round 3 plan's sign-off, with the five checks its last section lists.

## Tested

- Reachability of every host the plan relies on, one request each, logged with time, status and bytes in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f15cd04b-21be-5dde-a467-804e951756a2/scratchpad/phase-3/round-1/research/reach/` (`reach-1.tsv` to `reach-3.tsv`). Answered: data.medicaid.gov and its dataset catalog, govinfo.gov (CFR XML and the U.S. Code), clerk.house.gov (MemberData.xml, a 2025 roll call XML), senate.gov (a 2025 vote XML), uscourts.gov, www2.census.gov (the 2024 boundary and Gazetteer folders), fec.gov (its results page and `webl24.zip`), regulations.gov, archives.gov, law.cornell.edu, fns.usda.gov, supremecourt.gov, house.gov and senate.gov's committee pages, bea.gov, eCFR's API, and the Congress.gov, FEC and Census APIs with their keys (200 each). Refused (403): dol.gov, ssa.gov, medicaid.gov, usace.army.mil, fcc.gov, uscis.gov, and FEC's `cms-content` PDF path. Bot check: federalregister.gov and ecfr.gov's pages. FRED timed out.
- That data.medicaid.gov lists "Medicaid and CHIP Updated Renewal Outcomes" (identifier e6205a51-e6d7-4849-9882-4483b8a28c41, modified November 1, 2024), and that fec.gov links `2024congressgecands.xlsx` and the Census folders hold every file the geometry table names.
- The round 3 table's domain totals, recounted by script from the plan's own rows: 20 new specimens, with the totals the count table prints.
- No em dash or U+2011 in the plan.

## Not tested

- Any dataset's contents: nothing is fetched until the sign-off.
- The Census Bureau's own terms for its boundary files, which I read before freezing.
- Whether data.medicaid.gov's renewal file covers every state for every month; the sidecar will say.
- The FEC committee IDs of the two joint fundraising committees, and the H.R. 5371 roll call numbers; both are read from the record at fetch.

## Change log

Created:
- `work/handoffs/phase-3/20261112_Round-3-Data-Plan.md`
- `work/handoffs/phase-3/20261112_Round-1-Research-Notes.md` (this file)
