# Data Viz Public Series

Oath & Action Brand Guide, Edition 06, chapter 14 data visualization system. Research lead, November 6, 2026. Decision DR-46 lets charts use primary public data with a full source line. This brief records the public series the chart specimens need, so each maker can draw them and print an exact source line.

Every file sits in `work/boards/phase-2/data-viz/shared/`. Each CSV has a `.meta.json` sidecar with the publisher, table, URL, period, geography, base, unit, retrieval date, vintage, the qualification a reader must know, unconfirmed items and a ready source line. Raw downloads stayed in the session scratchpad and are not in the repo. Every value below was read from the downloaded file or page on November 6, 2026.

## 1. Child poverty, Supplemental Poverty Measure and official measure

**File:** `public/census-spm-child-poverty.csv` (116 rows)

**What it is.** The official poverty measure compares pretax money income with a national threshold. The Supplemental Poverty Measure (SPM) adds several government programs for low-income families that the official measure leaves out, and it adjusts its thresholds for local housing costs. It also accounts for taxes, work expenses and medical expenses (P60-290 report page). The file holds both for children under 18 and for all ages, 2009 to 2025, United States, with 90 percent margins of error for the SPM.

**Where it came from.** U.S. Census Bureau, *Poverty in the United States: 2025* (P60-290), released September 15, 2026: Table 8 for the SPM and Table 3 for the official measure. For comparison the file also keeps the earlier SPM vintage from *Poverty in the United States: 2024* (P60-287) Table B-2, released September 9, 2025. The revision itself is described in Census working paper SEHSD WP2026-17, "Revising Supplemental Poverty Measure Estimates from 2019 to 2024" (dated August 2026 and listed August 19, 2026). It says the Bureau of Labor Statistics corrected the SPM thresholds for 2019 to 2024 on July 17, 2026 and rebased them to 82 percent of median spending instead of 83 percent.

**Source line (default):** Source: U.S. Census Bureau, Poverty in the United States: 2025 (P60-290), Table 8, Supplemental Poverty Measure, children under 18, 2009 to 2025, United States. Retrieved November 6, 2026. Figures for 2019 to 2024 include the Bureau's August 2026 revision and differ by up to 0.4 points from those first published.

**Source line (official measure):** Source: U.S. Census Bureau, Poverty in the United States: 2025 (P60-290), Table 3, official poverty measure, children under 18, 2009 to 2025, United States. Retrieved November 6, 2026. The official measure compares pretax money income with a national threshold and leaves out several assistance programs that the SPM counts.

**How V7 compares.** V7's headline (numbers[5]) gives 9.7% in 2020, 5.2% in 2021 and 13.4% in 2024, "as first published." Those three match the first-published tables exactly: P60-287 Table B-2 reads 9.7, 5.2 and 13.4, and P60-277 Table B-2 (September 13, 2022) also reads 9.7 and 5.2. The current table does not match. P60-290 Table 8 reads 9.6 (2020), 5.1 (2021) and 13.5 (2024). The 2020 and 2021 values fell 0.1 point under the corrected thresholds. The 2024 value is 13.4 under the corrected thresholds with Vintage 2024 population controls (working paper Table 4), and P60-290 then reweighted every 2024 estimate to Vintage 2025 controls, which gives 13.5. Across 2019 to 2024 the child rate moved by -0.4 to +0.1 points between vintages; 2009 to 2018 did not change. V7's dates for the revision (August 2026) and the 2025 report (September 15, 2026) are correct.

**Which to chart.** Charts use the P60-290 values (`vintage = p60-290`). A chart that quotes V7's sentence as written uses the P60-287 rows and says "as first published" in its source line; the sidecar has that line ready. In 2025 the child SPM rate was 13.4% (margin of error 0.6) and the official child rate was also 13.4%. That coincidence matters: V7 source W001's note says "official child poverty 13.4%, a record low," which is the 2025 official measure, a different measure and year from numbers[5]'s 13.4% SPM figure for 2024.

**Breaks in the series.** The table gives two estimates for 2013 (split survey panels), 2017 (old and new processing systems) and, for the SPM, 2019 (old and new methods). The `comparable_with` column says which estimate joins the later years. A line chart either shows a step at each break or plots only the `later` rows.

**Gaps.** The original 2020 SPM report (P60-275) was not read. The "record low" wording in W001 was not checked. The BLS correction page was not requested, because bls.gov refuses automated requests.

## 2. Reported voting, by age, Current Population Survey

**File:** `public/census-cps-reported-voting.csv` (227 rows), with the age groups the coordinator added.

**What it is.** The share of people who told the Census Bureau's November survey that they voted, for every presidential and midterm election from 1964 to 2024, overall and for the table's four age groups: 18 to 24, 25 to 44, 45 to 64, and 65 and over (`age_group = all` is the total). The `base` column holds two bases. The citizen voting-age population (citizens 18 and over) runs from 1978 for the total and from 2002 for age groups. The total voting-age population (everyone 18 and over) runs from 1964 for all groups. Charts use the citizen base where it exists.

**Where it came from.** U.S. Census Bureau, Current Population Survey Voting and Registration Supplement, historical Table A-1, "Reported Voting and Registration by Race, Hispanic Origin, Sex and Age Groups: November 1964 to 2024" (the historical tables page was last revised April 24, 2025).

**Source line:** Source: U.S. Census Bureau, Current Population Survey Voting and Registration Supplement, Table A-1, reported voting by age, November 1964 to 2024, United States. Retrieved November 6, 2026. Self-reported voting among citizens 18 and over (from 1978; by age from 2002); earlier years use all people 18 and over.

**Values worth knowing.** In 2024, 65.3% of voting-age citizens reported voting: 47.7% of those 18 to 24 and 74.7% of those 65 and over. In 2022 the citizen rate was 52.2%.

**How V7 compares.** V7 cites "82.5% of citizens with an advanced degree" and "52.5% of high school graduates" for 2024. Table A-1 has no education breakdown, so those were not checked here. Table A-2 holds education and was not downloaded.

**Gaps.** Table A-1 gives no margins of error. The census notes that citizenship was not collected uniformly before 1996 and that the youngest group before 1972 is mostly people 21 to 24; both notes travel in the `note` column. The November 2026 supplement is not yet out.

## 3. Homeownership by race and ethnicity of householder

**Files:** `public/census-hvs-homeownership-by-race-annual.csv` (132 rows, 1994 to 2025) and `public/census-hvs-homeownership-by-race-quarterly.csv` (524 rows, first quarter 1994 to third quarter 2026).

**What it is.** The homeownership rate, which the survey's definitions page describes as the number of households that are owners divided by the total number of households, for all households and for non-Hispanic White, Black and Hispanic householders (Hispanic of any race), United States.

**Where it came from.** U.S. Census Bureau, Current Population Survey/Housing Vacancy Survey (CPS/HVS). Annual: Annual Statistics 2025, Table 22, dated March 24, 2026, with 2025 margins of error from Table B-7. Quarterly: historical Table 16, dated October 28, 2026, with margins of error from Table B-8 for 2010 onward.

**Source line (annual):** Source: U.S. Census Bureau, Current Population Survey/Housing Vacancy Survey, Annual Statistics 2025, Table 22, homeownership rate by race and ethnicity of householder, 1994 to 2025, United States. Retrieved November 6, 2026. Race categories changed in 2003; the 2025 average leaves out October, when no data were collected.

**Source line (quarterly):** Source: U.S. Census Bureau, Current Population Survey/Housing Vacancy Survey, Table 16, homeownership rate by race and ethnicity of householder, first quarter 1994 to third quarter 2026, United States. Retrieved November 6, 2026. Quarterly survey estimates, with margins of error up to 0.9 points for each group.

**How V7 compares.** V7 gives 74.5% non-Hispanic White, 45.4% Black and 48.1% Hispanic for the second quarter of 2026, with a national rate of 65.0%. Table 16 matches all four. A newer quarter is out: the third quarter of 2026, released October 28, reads 75.1%, 44.4%, 48.1% and 65.5%. The 2025 annual averages are 74.3%, 44.7%, 48.5% and 65.2%.

**Gaps.** Two quarterly cells carry an extra digit. The 1995 fourth-quarter U.S. cell reads 65.13; Table 14 gives 65.1, so the file uses 65.1 and keeps the raw cell in `cell_as_read`. The 1998 fourth-quarter Hispanic cell reads 45.73; the file uses 45.7 by the same reading, with no second table to confirm it. The table does not say whether Table 16 is seasonally adjusted. V7's release date for the second-quarter data, July 28, 2026, was not checked. Annual margins of error before 2025 were not collected.

## 4. State lists for maps

### 4a. States that prohibit ranked-choice voting

**File:** `public/ballotpedia-rcv-prohibitions-by-state.csv` (51 rows, one per state and DC; 19 flagged)

**Source used, and why.** V7's source W049 is the National Conference of State Legislatures (NCSL) page. It returned HTTP 403 behind a Cloudflare security challenge, and the studio did not retry it. The list therefore comes from Ballotpedia, a secondary source, which states its list "as of November 2026." Ranked-choice voting (RCV) means voters rank candidates and the count runs in rounds until one has a majority.

**Source line:** Source: Ballotpedia, Ranked-choice voting (RCV), state laws prohibiting RCV, as of November 2026, 50 states and DC. Retrieved November 6, 2026. Ohio's and Tennessee's bans cover some elections; the other 17 cover all.

**The 19 states.** AL, AR, FL, ID, IN, IA, KS, KY, LA, MS, MO, MT, ND, OH, OK, SD, TN, WV, WY. These are the same 19 states, with the same enactment years, as V7 repair log row RL47 as of October 15, 2026.

**Scope.** Seventeen bans cover all elections as Ballotpedia quotes them. Two cover some:

- Ohio (SB 63, March 17, 2026) bars RCV "except as otherwise permitted under Article X or Article XVIII" of the state constitution. Home-rule cities may still adopt it, but they lose state local government fund distributions while it is in effect.
- Tennessee (SB 1820, Public Chapter 621) bars county election commissions from using RCV "for a statewide or local government office." Federal offices are not named. I read this one on the Tennessee General Assembly's own bill record, which shows the governor signed on February 28, 2022; Ballotpedia's March 7 date is when the public chapter number was assigned.

Missouri's ban is in its constitution (Amendment 7, November 5, 2024); the other 18 are statutes. Alabama, Arkansas and Louisiana carve out ranked runoff ballots for military and overseas voters, which the file treats as all-election bans. Mississippi's quoted text names statewide, county, local, municipal and school district elections and party contests, but not congressional district races; the file marks it "all" as Ballotpedia describes it and flags the point.

### 4b. States with a citizen initiative

**File:** `public/ballotpedia-citizen-initiative-states.csv` (51 rows)

**Source used.** Ballotpedia, "States with initiative or referendum" (secondary). NCSL was not tried after its refusal above.

**Source line:** Source: Ballotpedia, States with initiative or referendum, 50 states and DC. Retrieved November 6, 2026. Mississippi's process exists on paper but cannot be used after a 2021 state supreme court ruling.

**The 24 states.** AK, AZ, AR, CA, CO, FL, ID, IL, ME, MA, MI, MS, MO, MT, NE, NV, ND, OH, OK, OR, SD, UT, WA, WY. Twenty-one allow an initiated statute and 18 an initiated constitutional amendment. Florida and Illinois allow amendments only. Mississippi cannot use its process, so 23 work. Maryland and New Mexico have a veto referendum and no initiative. DC has an initiative process, but Ballotpedia does not itemize its types. The `initiated_statute_form` and `initiated_amendment_form` columns say direct or indirect; in an indirect process (studio gloss) the petitioned measure goes to the legislature before it can reach the ballot.

**How V7 compares.** V7 claim CL1735 says 24 states, DC and the U.S. Virgin Islands have a citizen initiative and that Mississippi's has been ruled void; V7 elsewhere counts 23 working processes. The file agrees on both counts.

## 5. Map geometry and tile grid

**Files:** `geo/states-albers-10m.json`, `geo/us-atlas-LICENSE.txt`, `geo/us-state-tile-grid.json`, `geo/geo.meta.json`

The TopoJSON comes from the `us-atlas` npm package, version 3.0.1 (published April 19, 2023), copied unchanged from the registry tarball. Its README says it redistributes the Census Bureau's 2017 cartographic boundary files, projected with Albers USA to fit a 975 by 610 frame, with Alaska and Hawaii as insets. Each state carries its two-digit FIPS code as `id` and its name. Ten small Alaska polygons in the western Aleutians fall left of x = 0, so a frame starting at 0 clips them. The license is ISC, "Copyright 2013-2019 Michael Bostock," and it asks that the copyright and permission notice travel with every copy. The underlying Census data are federal works: 17 U.S.C. 105, read on copyright.gov, says "Copyright protection under this title is not available for any work of the United States Government." No Census page I read states a license for the boundary files themselves.

**Credit line:** Map: U.S. Census Bureau cartographic boundary files (2017), via us-atlas 3.0.1 by Mike Bostock (ISC license).

The tile grid is a studio design layout: 51 squares in 12 columns and 8 rows, west to east and north to south, with Alaska at the top left and Hawaii at the bottom left. It follows the square tile-grid convention newsrooms have used for state maps since the mid-2010s and copies no single publication. Each record carries `code`, `name`, `fips`, `col` and `row`, so it joins to every CSV here.

## 6. Optional series not collected

The Federal Election Commission series was skipped. One request to the FEC's public API with its shared demonstration key returned HTTP 429 (rate limited), and the brief allowed only a few minutes.

## 7. Rights rows for the reader to add

These rows follow the main table in `work/research/20261020_Rights-Ledger.md`, with set "data-viz-public." I did not edit the ledger. Three terms codes are proposed:

- **T-USGOV:** 17 U.S.C. 105, read on copyright.gov on November 6, 2026. U.S. government works carry no U.S. copyright. The Census Bureau's citation page asks users to cite the Bureau as the source.
- **T-ISC-USATLAS:** the us-atlas LICENSE file, read from the package. Copy and redistribute with the copyright and permission notice.
- **T-GFDL-BP:** Ballotpedia:Copyrights, read on November 6, 2026. Ballotpedia text is under the GNU Free Documentation License, with attribution by link. The studio files copy facts and short statutory phrases only.

Two likely-origin values are proposed for the key: "federal public data" and "open-source package."

| # | File or reference | Set | Likely origin | Evidence | Permitted use | Notes |
|---|---|---|---|---|---|---|
| dvp-01 | `public/census-spm-child-poverty.csv` | data-viz-public | federal public data | P60-290 Tables 3 and 8, P60-287 Table B-2, read November 6, 2026 | may ship | T-USGOV. Print the source line from the sidecar |
| dvp-02 | `public/census-cps-reported-voting.csv` | data-viz-public | federal public data | CPS Table A-1, read November 6, 2026 | may ship | T-USGOV |
| dvp-03 | `public/census-hvs-homeownership-by-race-annual.csv` | data-viz-public | federal public data | HVS Annual Table 22 and B-7, read November 6, 2026 | may ship | T-USGOV |
| dvp-04 | `public/census-hvs-homeownership-by-race-quarterly.csv` | data-viz-public | federal public data | HVS Table 16 and B-8, read November 6, 2026 | may ship | T-USGOV |
| dvp-05 | `public/ballotpedia-rcv-prohibitions-by-state.csv` and `public/ballotpedia-citizen-initiative-states.csv` | data-viz-public | third-party reference data | Ballotpedia pages, revisions 12746538 and 11698211, read November 6, 2026; Tennessee bill record | may ship | T-GFDL-BP. Facts only; credit Ballotpedia and label it secondary. Whether facts drawn from a GFDL page need GFDL terms is a judgment, not a legal opinion |
| dvp-06 | `geo/states-albers-10m.json` | data-viz-public | open-source package | us-atlas 3.0.1 tarball; hashes match the npm registry | may ship with license text | T-ISC-USATLAS for the file, T-USGOV for the Census geometry. Ship `geo/us-atlas-LICENSE.txt` with it |
| dvp-07 | `geo/us-state-tile-grid.json` | data-viz-public | Oath & Action original | Made by the research lead, November 6, 2026 | may ship | Design layout; no third-party source |

## 8. What I tested

- Compared V7's figures, read from `work/extract/atlas-v7-data.json` (numbers[5], CL1120, RL47, CL1735 and sources S19, N05, W001, K1913, W049), with the tables.
- Checked all 12 child SPM values for 2019 to 2024 in both vintages against working paper Table 4. Eleven match; 2024 in P60-290 differs by the documented population reweighting.
- Checked the 1995 fourth-quarter U.S. homeownership cell against HVS Table 14.
- Verified the us-atlas tarball's SHA-1 and SHA-512 against the npm registry, and confirmed the copied TopoJSON and LICENSE are byte-identical to the package files.
- Decoded every TopoJSON arc in Python: 51 states, no unclosed rings, positive area for every state, extent as stated above.
- Checked the tile grid: 51 unique cells, codes and names matching the TopoJSON.
- Parsed every CSV: lowercase headers, numeric columns parse as numbers, no commas, percent signs or currency marks in number fields.
- Parsed every `.meta.json` as JSON and checked all new files for em dashes.

## 9. What I could not test

- NCSL's ranked-choice page (V7 source W049): 403 behind a Cloudflare challenge; not retried. NCSL's list and its "some or all" labels were not read.
- The Mississippi and Ohio legislature sites failed TLS certificate verification. I did not bypass verification, so those statutes were not read.
- Missouri's Amendment 7 text: a guessed Secretary of State address returned 404.
- The statutes for the other 16 ban states; their scope rests on Ballotpedia's quotations.
- The FEC series (429 rate limit).
- The BLS correction page, which I did not request because bls.gov refuses automated requests.
- I rendered no map or chart from these files.

## 10. Claims I could not verify

- The 2020 SPM child rate in the original 2020 report (P60-275).
- W001's "record low" description of the 2025 official child rate.
- V7's July 28, 2026 release date for second-quarter homeownership data.
- V7's 2024 voting rates by education (82.5% and 52.5%); they sit in Table A-2, which I did not download.
- Alabama's bill number, which Ballotpedia prints as "SB 1886."
- Iowa's bill number (Ballotpedia gives HF 954 and HF 1954) and North Dakota's signing date (April 15 or April 18, 2025).
- The 1998 fourth-quarter Hispanic homeownership cell (45.73 as printed, 45.7 in the file).
- Whether HVS Table 16 is seasonally adjusted.

## Change log

Files created on November 6, 2026 (paths from the project root):

- `work/boards/phase-2/data-viz/shared/public/census-spm-child-poverty.csv`
- `work/boards/phase-2/data-viz/shared/public/census-spm-child-poverty.meta.json`
- `work/boards/phase-2/data-viz/shared/public/census-cps-reported-voting.csv`
- `work/boards/phase-2/data-viz/shared/public/census-cps-reported-voting.meta.json`
- `work/boards/phase-2/data-viz/shared/public/census-hvs-homeownership-by-race-annual.csv`
- `work/boards/phase-2/data-viz/shared/public/census-hvs-homeownership-by-race-annual.meta.json`
- `work/boards/phase-2/data-viz/shared/public/census-hvs-homeownership-by-race-quarterly.csv`
- `work/boards/phase-2/data-viz/shared/public/census-hvs-homeownership-by-race-quarterly.meta.json`
- `work/boards/phase-2/data-viz/shared/public/ballotpedia-rcv-prohibitions-by-state.csv`
- `work/boards/phase-2/data-viz/shared/public/ballotpedia-rcv-prohibitions-by-state.meta.json`
- `work/boards/phase-2/data-viz/shared/public/ballotpedia-citizen-initiative-states.csv`
- `work/boards/phase-2/data-viz/shared/public/ballotpedia-citizen-initiative-states.meta.json`
- `work/boards/phase-2/data-viz/shared/geo/states-albers-10m.json`
- `work/boards/phase-2/data-viz/shared/geo/us-atlas-LICENSE.txt`
- `work/boards/phase-2/data-viz/shared/geo/us-state-tile-grid.json`
- `work/boards/phase-2/data-viz/shared/geo/geo.meta.json`
- `work/research/20261106_Data-Viz-Public-Series.md`

Files modified: none. The build scripts and raw downloads are in the session scratchpad, outside the repo.
