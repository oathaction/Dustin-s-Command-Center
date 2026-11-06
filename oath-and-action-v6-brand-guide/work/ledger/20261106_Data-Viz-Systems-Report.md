# Data visualization systems: Board 3 report

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Status: waiting for Dustin's pick. This is a stage review inside Phase 2, not a gate.

Open the board: `work/boards/20261106_Data-Viz-Systems-Board.html`, also published as a private page at https://claude.ai/artifact/PYArbPq2Vm1irRKzKJCHBF. The three systems are published as private pages:

| System | Private page | File |
|---|---|---|
| 01 Explainer | https://claude.ai/artifact/VECbhdNnEqnoTPqxwAeZs3 | `work/boards/phase-2/data-viz/01-explainer/20261106_Data-Viz-01-Explainer.html` |
| 02 Register | https://claude.ai/artifact/TTGuVz7s6V6cRvGBkqfwmD | `work/boards/phase-2/data-viz/02-register/20261106_Data-Viz-02-Register.html` |
| 03 Instrument | https://claude.ai/artifact/5KmjL3E71uiD5HFwjdrNYW | `work/boards/phase-2/data-viz/03-instrument/20261106_Data-Viz-03-Instrument.html` |

## What you are asked to decide

1. **Which chart system to finish** as chapter 14 and the chart kit. Recommended: Explainer, finished with Register's tables and social card and Instrument's Chart and Table switch, downloads and one-call kit.
2. **The page color** for charts and the atlas together (DR-45). Recommended: Newsprint, with printed reports using the paper as the ground.
3. **The diverging pair.** Recommended: B, Prussian through the page color to Verdigris, with a boxed arrow carrying the direction in every cell.
4. **The editor's disclosure** printed on the four election-rule charts (D2-106). Confirm the wording or correct any fact about your roles.
5. **S01's party split.** Recommended: keep the vote totals only until the Senate's record of Vote 253 can be read, then add both chambers' splits together (D2-104).
6. **A web address for social cards**, once your site is settled. Until then the cards carry none.
7. **The order of work after the pick.** Recommended: the full chapter 14 set and the chart kit next, then the open direction review items, then the rest of Phase 2 through Gate 2.
8. **A balanced chart set.** Recommended: choose the twenty or more charts so readers on each side meet a finding they would rather skip, and read every title from the left and the right before it ships.
9. **V7.1 item 35**, the uneven descriptions of redrawn maps in the repair log. Recommended: add it to the V7.1 list (done; confirm).

## 1. What was done

| Step | Who ran it | Output |
|---|---|---|
| Your answers logged, the V7 package checked and extracted | Main session | DR-44 to DR-51, D2-89, D2-90; `work/extract/` (git-ignored) |
| Public series and map geometry: Census child poverty, turnout by age and homeownership by race; Ballotpedia's state lists; us-atlas geometry and a tile grid; two follow-up checks | Research lead | `work/research/20261106_Data-Viz-Public-Series.md`; `work/boards/phase-2/data-viz/shared/public/` and `geo/` |
| The shared base: chart dataset, palette lab, data verifier with a planted-error self-test, rendered check with scale and party tests, the makers' brief | Main session | `work/boards/phase-2/data-viz/shared/`; `work/build/scripts/phase-2/dataviz_*`; `work/handoffs/phase-2/20261106_Data-Viz-Brief.md` |
| Three systems, ten like-for-like charts each, five views | Three specialist makers | `work/boards/phase-2/data-viz/01` to `03`; notes `work/handoffs/phase-2/20261106_Data-Viz-0N-Notes.md` |
| Red team: statistics, civic education, interface and accessibility, brand and nonpartisanship, type and drawing craft at 2x, production | Six reviewers, one lens each across all three | `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-*.md` |
| Reader panel: six simulated first-time readers | One reviewer | `work/handoffs/phase-2/20261106_Data-Viz-Reader-Panel.md` |
| Shared fixes from the reviews: scenario reading, verifier tolerance and dates, the disclosure as required text, two source lines | Main session | D2-105, D2-106, D2-110 |
| One fix pass against eighteen shared fixes | The three makers | `work/handoffs/phase-2/20261106_Data-Viz-Fix-Pass-Brief.md`; fix-pass sections in each notes file |
| Scores, recommendation, last faults and the board's content | Creative director | `work/handoffs/phase-2/20261106_CD-Review-Of-Data-Viz-Systems.md`; `work/boards/phase-2/data-viz/board-3/20261106_Board-3-Content.json` |
| Last faults fixed | The three makers | D2-112 |
| Checks rerun after every pass, captures, Board 3, publishing and this report | Main session | This file; the board |

## 2. Scores

The creative director's scores after the fix pass, 1 to 5, ship threshold 4 on every line.

| System | Craft | Clarity | Brand | Usefulness | Evidence | Accessibility | Beauty | Ships |
|---|---|---|---|---|---|---|---|---|
| 01 Explainer | 4 | 5 | 4 | 4 | 5 | 4 | 4 | Yes |
| 02 Register | 4 | 4 | 4 | 4 | 5 | 4 | 4 | Yes |
| 03 Instrument | 4 | 4 | 4 | 5 | 5 | 4 | 3 | No (beauty) |

The red team's scores, before the fix pass:

| System | Statistics | Civic education | Interface | Brand and nonpartisan | Craft | Production | Readers first |
|---|---|---|---|---|---|---|---|
| 01 Explainer | 4 | 4 | 4 | 3 | 3 | 3 | 4 of 6 |
| 02 Register | 3 | 3 | 4 | 2 | 2 | 2 | 1 of 6 |
| 03 Instrument | 3 | 3 | 3 | 4 | 3 | 3 | 1 of 6 |

The creative director scored the systems after the fix pass and before the last faults were fixed, and did not score them again after those.

## 3. What the round found in V7

Added to the V7.1 issue list (`work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md`):
- **31.** Child poverty prints the Census rates as first published (9.7, 5.2 and 13.4 percent for 2020, 2021 and 2024; history event of 2021 too). The current table reads 9.6, 5.1 and 13.5.
- **32.** Source W001's note names the official 2025 rate beside the SPM 2024 rate, which invites a mix-up.
- **33.** A newer quarter of homeownership by race is out (third quarter of 2026).
- **34.** Repair log entry RL47 rolls all 19 state bans on ranked-choice voting into one entry, while Missouri and Indiana also have entries, so counts from the log mix single changes with a roll-up.
- **35.** The log describes redrawn maps unevenly: a seat aim for Texas and Florida, only a response for California and Virginia.

Also checked: Missouri's certified Amendment 7 result (68.4 to 31.6 percent) matches V7; Ballotpedia prints 68.5 to 31.5. The Census Bureau asks readers to use caution with 2020 homeownership figures, and every homeownership chart now says so.

One correction to the studio's own words: citizen ballot initiatives moved the rules away from voters in none of 17 entries, while referendums did in 3 of 10, so "ballot measures, none of 17" overstated it (D2-103).

## 4. Verification

**Tested**
- Each page passes the data verifier against the shared data (every mark's value or category, every required row, evidence kind, the five chart parts, source words, the disclosure on S03, S06, S07 and S08, true dates on the timeline, no em dash and no hyphen used as a minus), and its self-test catches 7 of 7 planted errors on each page. Final run: Explainer 4,038 marks, Register 2,953, Instrument 4,025, 0 errors each.
- Each page passes the rendered check on all five views at 1440, 390 and 360 px: no sideways scroll, no text under 13 px, text contrast, labels inside drawings and apart, Rule 05.3, no party mark in Pillar Red or Prussian, every bar and dot on its scale, 0 axe-core violations, a visible focus ring on each stop, and the click from the first view into another and back.
- The scale test caught a planted wrong bar in a copy of Register's evidence chart and named the row; a planted off-scale point on a test page was caught and named.
- The red team measured scales in a browser, read the accessibility tree, injected wider text spacing, rendered every view at 2x, and built a new chart from each system's own code.
- Board 3 passes the rendered check at 1440, 390 and 360 px.

**Not tested**
- Real readers (Q-13). The panel was simulated by one model and saw the first versions.
- A real screen reader, Safari, Firefox, real phones, 200 percent text zoom and print.
- PNG export, and SVG downloads with embedded fonts. Instrument's downloads work in the local file; the private page's viewer blocks downloads, so they do nothing there.
- The creative director did not score again after the last faults were fixed, and the red team did not review again after the fix pass.

## 5. Change log

Paths relative to `oath-and-action-v6-brand-guide/`. Nothing in `source/`, the Civic Line icons, the identity masters or the atlas pick changed.

**Created**
- `work/boards/phase-2/data-viz/shared/`: `20261106_Chart-Data.json`, `20261106_Palette-Lab.json`, `20261106_Palette-Lab.html`, `public/` (six series with metadata), `geo/` (state geometry with its license and a tile grid)
- `work/boards/phase-2/data-viz/01-explainer/`, `02-register/`, `03-instrument/`: build scripts, pages, check results and captures
- `work/boards/phase-2/data-viz/board-3/`: the board's content, published page links and captures
- `work/boards/20261106_Data-Viz-Systems-Board.html` and its check results and captures in `work/boards/captures/`
- `work/build/scripts/phase-2/`: `dataviz_shared_data.py`, `dataviz_palette_lab.py`, `dataviz_verify.py`, `dataviz_check.js`, `dataviz_board3_capture.js`, `dataviz_board3_build.py`
- `work/handoffs/phase-2/`: `20261106_Data-Viz-Brief.md`, `20261106_Data-Viz-Red-Team-Brief.md`, `20261106_Data-Viz-0N-Notes.md` (three), six `20261106_Data-Viz-Red-Team-*.md`, `20261106_Data-Viz-Reader-Panel.md`, `20261106_Data-Viz-Fix-Pass-Brief.md`, `20261106_Data-Viz-CD-Brief.md`, `20261106_CD-Review-Of-Data-Viz-Systems.md`
- `work/research/20261106_Data-Viz-Public-Series.md`
- `work/ledger/20261106_Data-Viz-Systems-Report.md` (this file)

**Modified**
- `work/ledger/20261020_Decision-Log.md` (DR-44 to DR-51, D2-89 to D2-114)
- `work/ledger/20261020_Source-Manifest.md` (the November 6 files)
- `work/research/20261020_Rights-Ledger.md` (dvp-01 to dvp-07)
- `work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md` (items 31 to 35)
- `.gitignore` (font copies, D2-109)
