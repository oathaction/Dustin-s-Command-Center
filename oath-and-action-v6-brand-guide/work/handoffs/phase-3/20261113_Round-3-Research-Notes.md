# Round 3 research notes

Oath & Action Edition 06, Phase 3, round 3. Research lead (`oa-research-lead`), November 13, 2026, under `work/handoffs/phase-3/20261113_Phase-3-Round-3-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Kept current as the work goes, since the container can restart.

## Summary

Started 00:49 UTC. Order of work, as the brief binds it: the boundary files (P7-219), the atlas re-check (DR-250), the judge counts, the stale lines, then the data check over each file the makers derive.

## Geometry

Each file is RFC 7946 GeoJSON under R1-C7: NAD83 longitude and latitude, unprojected, every vertex kept, six decimals, outer rings counterclockwise and holes clockwise (RFC 7946 section 3.1.6; the reverse of the shapefile, and of what d3-geo expects), properties `geoid`, `code`, `name` (and `district`), sorted by `geoid`. Each sidecar quotes the Bureau's terms from the zip's own metadata, the product page and the description page. Written by `work/build/scripts/phase-3/research_geometry_freeze.py`.

- 00:58 UTC. `work/build/data/census-cb-2024-states.geojson` frozen (P7-219a): 52 features (50 states, DC, Puerto Rico), 1:20,000,000, 13,706 vertices, 324,241 bytes; raw `cb_2024_us_state_20m.zip`, SHA-256 7bc773d8...23ef.
- 00:58 UTC. `work/build/data/census-cb-2024-counties.geojson` frozen (P7-219b): 3,222 features (3,144 counties and equivalents of the 50 states and DC, Connecticut's nine planning regions among them, and Puerto Rico's 78 municipios), 1:20,000,000, 56,386 vertices, 1,737,922 bytes; raw `cb_2024_us_county_20m.zip`, SHA-256 c9a54fd9...35ff. All 3,144 rows of `census-acs5-county-median-household-income` join on `geoid`; `census-cbp-county-employment` has 3,142, lacking 15005 (Kalawao County, Hawaii) and 48269 (King County, Texas).
- 00:58 UTC. `work/build/data/census-cb-2024-cd119.geojson` frozen (P7-219c): 441 features (435 districts, six of them at large with `district` "AL", and six delegate areas, DC, Puerto Rico, American Samoa, Guam, the Northern Mariana Islands and the Virgin Islands, with `district` "98"), 1:5,000,000, 175,196 vertices read, 8 dropped where rounding made two in a row equal (named in the sidecar), 4,111,123 bytes; raw `cb_2024_us_cd119_5m.zip`, SHA-256 17370f9f...4cc6. All 435 rows of `clerk-house-results-2024-by-district` join by state FIPS code plus district (the Clerk writes at-large seats "00", this file "AL"; join on `geoid`). Michigan has 13.
- 00:59 UTC. `work/build/data/census-cb-2024-nation.geojson` frozen (P7-219d): one MultiPolygon of 82 parts (the 50 states, DC and Puerto Rico; the island areas are absent at this scale), 1:20,000,000, 5,834 vertices, 136,520 bytes; raw `cb_2024_us_nation_20m.zip`, SHA-256 3316da94...6213.
- 00:58 UTC. `work/build/data/census-cb-2024-counties-california-5m.geojson` frozen (P7-219e, D3-1087): California's 58 counties, the features of the national 1:5,000,000 file whose STATEFP is 06, 8,690 vertices, 214,571 bytes; raw `cb_2024_us_county_5m.zip` (national), SHA-256 a867f873...614b. Kern County is `06029`.
- 01:00 UTC. All five frozen; told the main session. A rerun of the script writes nothing. Today's data check (`data_round0_build.py --check`) refuses `.geojson` files until the engineer's R3-2 reading lands (request below).

For the engineer and the cartographer: Alaska's Aleutians west of 180 degrees carry positive longitudes (to 179.773922), as published; the 20m files hold no island areas (the districts file holds their six delegate areas); Connecticut's counties are its nine planning regions.

## Requests landed

- **R3-A1 (maker A, 01:08 UTC).** `ballotpedia-rcv-prohibitions-by-state.meta.json`'s `publisher` reads "Ballotpedia, a secondary source", the words its printed line uses (D2-99's labeled secondary). One line changed. S07 built before and after: PASS, 0 faults, all 19 files (pages, SVG, PNG, CSV, captures, check file) equal byte for byte, since a one-dataset spec's check compares the line with `printed_source_line` and never reads `publisher`. S67 went from FAIL ("the source line does not name Ballotpedia. Secondary source") to PASS, 0 faults. The engineer's script would write the old words back on a rerun (ENG-R3-1).
- **RL-1 (data lead, cartographer; 01:15 UTC).** `census-acs5-county-median-household-income` has the nation as its first row, code `US`: $80,734 with a 90 percent margin of $166, B19013, 2020 to 2024, read November 13, 2026 with the county call, which returned all 3,144 frozen values unchanged. Variant `with_united_states` names the nation. The nation sits $734 from the data lead's $80,000 break.
- **RL-2 (data lead, cartographer; 01:15 UTC).** `census-cbp-county-employment` gains `emp_noise_flag` and `emp_noise_words`, from the Bureau's downloadable 2023 county file (`cbp23co.zip`), whose counts and establishments equal the frozen API values in all 3,142 rows. The 2020 to 2023 record layout defines G (under 2 percent noise), H (2 to under 5) and J (5 percent or more): 2,735 G, 378 H, 29 J. The API's `EMP_N` ("Noise range for number of employees") returned 0 everywhere and its variable list defines no values, so the flags come from the file. The gap of 7,679,940 between the counties (132,151,802) and the nation (139,831,742) is the 50 statewide records (county code 999; 7,679,935; Florida 1,927,806, California 1,017,858, Texas 602,614), "Employers without a fixed location within a state (or of unknown county location)" in the methodology's words, plus 5 that Hawaii's (3) and Texas's (2) state totals hold beyond their counties and statewide records, the two states whose one county the file leaves out. The 51 state totals sum to the nation exactly. Variant `with_noise_flags`.
- **RL-3 (data lead, maker B; 01:15 UTC).** `fec-jfc-transfers-2024` gains `recipient_name_2024_election` (the name the joint fundraising committee wrote on its last itemized payment on or before November 5, 2024): "HARRIS FOR PRESIDENT" (its 14 payments to July 2024 say "BIDEN FOR PRESIDENT") and "DONALD J. TRUMP FOR PRESIDENT 2024, INC." (12 of 13 payments; the last, December 2024, says "NEVER SURRENDER, INC."). The FEC's committee history for the 2024 cycle could not serve: it already lists Trump's committee as Never Surrender, a leadership PAC. Also `recipient_names_itemized`, `amount_lines`, `line_21b_amount`, `line_21b_transactions`. **Finding:** the FEC aggregate the frozen amounts come from (equal today in all 57 rows) sums line 22 transfers, plus a line 28C refund for two committees (Progressive Turnout Project $80,000; Operating Engineers Local 478 $1,000), and leaves out line 21B operating expenditures: $11,993,565.82 to Harris's campaign (7 payments), $15,146,635.19 to the DNC (32), $1,501.00 to Kentucky's party (1). The sidecar said "sums of itemized disbursements"; its qualification and three column descriptions now say what the amounts hold. Variant `transfers_and_refunds` names lines 22 and 28C. S73 rebuilt: PASS, 0 faults; only its CSV export differs (7,527 to 14,460 bytes, the new columns).

## Atlas re-check (DR-250)

(In progress.)

## Judge counts

(Queued.)

## Stale lines

(Queued.)

## Data check over derived files

(Waiting for the makers.)

## Routine calls

- D3-xxx | The boundary files are fetched again and frozen by a script in the repository, `research_geometry_freeze.py`, with its own standard-library shapefile reader checked against pyshp | Round 1's staging was lost with its scratch folder; anyone can rerun the freeze with no package the build lacks, and a rerun writes nothing
- D3-xxx | Rings are written in RFC 7946's order, outer rings counterclockwise and holes clockwise, reversing the shapefile's vertex sequence with no value changed | R1-C7 names RFC 7946, whose section 3.1.6 makes the order a MUST; the kit uses no d3-geo, and a planar projection fills either way
- D3-xxx | A vertex that rounding to six decimals makes equal to the one before it is dropped and counted (8 in the districts file, none elsewhere) | R1-C7 allows six decimals; a segment of no length would trip code that takes a segment's direction, and neighboring districts drop the same vertex, so shared edges stay identical
- D3-xxx | At-large seats read "AL" and delegate areas keep the Bureau's "98" | R1-C7 names "AL" for an at-large seat; a delegate has no vote on the House floor, so calling the area an at-large seat would mislead
- D3-xxx | Each boundary file keeps every feature the Bureau's file holds, Puerto Rico and the delegate areas included | C1 freezes a table as published; a map's CSV chooses what it draws
- D3-xxx | Each boundary sidecar quotes the Bureau's terms in `terms_of_use`: the zip metadata's use and access constraints word for word, the product page and the description page | The brief asks for the terms in each sidecar; the metadata carries the formal terms, and neither page states a license
- D3-xxx | States, counties and nation take domain `all`, the districts D02 and California's counties D10, as the locator's Gazetteer row does | A boundary file carries no data values and serves each map's own domain
- D3-xxx | The Ballotpedia sidecar's `publisher` reads "Ballotpedia, a secondary source" | The words the printed line and D2-99 already use; the two-dataset check reads the publisher, and S07's one-dataset check does not
- D3-xxx | The county income file's national row goes first with code `US` | The kit and the broadband and business formation files carry the nation that way
- D3-xxx | County noise flags come from the Bureau's downloadable county file, not the API's code | The file's record layout defines its flags and its counts equal the API's in every row; the API defines no values for its code
- D3-xxx | A recipient's name in the cycle is the name its joint fundraising committee wrote on its last itemized payment on or before November 5, 2024 | One date read the same way for every recipient; the FEC's 2024 committee history already shows a change made after the election
- D3-xxx | The JFC amounts stay as the FEC's aggregate gives them, line 22 and two line 28C refunds, with line 21B in its own columns | D3-476 freezes figures; the aggregate is the commission's own and reads the same lines for both nominees, and the new columns show what it leaves out

## Requests

- **To the engineer (R3-2).** The five boundary files are frozen. Today's `data_round0_build.py --check` reads 117 tables with 10 faults, all of them these files: "only .csv, .json and .meta.json files belong here" and "no rows", five each. They clear when the check reads `.geojson` under R1-C7. The script's own check of R1-C7 (`research_geometry_freeze.py` without `--freeze`) passes for all five. Two facts for the projection: rings are in RFC 7946's order (outer counterclockwise; reverse them if you use d3-geo), and Alaska's Aleutians west of 180 degrees carry positive longitudes.
- **ENG-R3-1, to the engineer (maker A's R3-A1).** `ballotpedia-rcv-prohibitions-by-state.meta.json`'s `publisher` now reads "Ballotpedia, a secondary source", the words its printed line already uses and the labeled-secondary wording of D2-99. `data_round0_build.py` copies `publisher` from the Phase 2 sidecar ("Ballotpedia. Secondary source"), so a rerun would write the old words back (checked by calling its `public_meta` without writing). Please carry the new publisher in the script, for example a `publisher` key in `LINE_FIXES` that `public_meta` applies.
- **To the cartographer.** `census-cb-2024-counties-california-5m` is frozen for S79 (Kern County `06029`). For S83, County Business Patterns has no row for 15005 (Kalawao County, Hawaii) or 48269 (King County, Texas), which the county geometry holds. The district file's at-large seats read "AL" where the Clerk's file reads "00"; join on `geoid`.

## Tested

## Not tested

## Files
