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

## Requests

- **To the engineer (R3-2).** The five boundary files are frozen. Today's `data_round0_build.py --check` reads 117 tables with 10 faults, all of them these files: "only .csv, .json and .meta.json files belong here" and "no rows", five each. They clear when the check reads `.geojson` under R1-C7. The script's own check of R1-C7 (`research_geometry_freeze.py` without `--freeze`) passes for all five. Two facts for the projection: rings are in RFC 7946's order (outer counterclockwise; reverse them if you use d3-geo), and Alaska's Aleutians west of 180 degrees carry positive longitudes.
- **To the cartographer.** `census-cb-2024-counties-california-5m` is frozen for S79 (Kern County `06029`). For S83, County Business Patterns has no row for 15005 (Kalawao County, Hawaii) or 48269 (King County, Texas), which the county geometry holds. The district file's at-large seats read "AL" where the Clerk's file reads "00"; join on `geoid`.

## Tested

## Not tested

## Files
