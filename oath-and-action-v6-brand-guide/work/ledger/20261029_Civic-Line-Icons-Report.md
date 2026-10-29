# Civic Line icons: delivery and fidelity report

Oath & Action Brand Guide, Edition 06. October 29, 2026. Status: approved by Dustin on October 29 (DR-07); variants built and delivered the same day. This report covers the Civic Line reconstruction Dustin asked for on October 29, under decisions DR-01 to DR-06.

Open the catalog: `work/build/assets/civic-line/20261029_Civic-Line-Icon-Catalog.html`, also published as a private page at https://claude.ai/artifact/XWvZnx86mnKkoVFV9PCcgD.

## What you are asked to decide

Dustin approved the set, framing option 3, the light editions and the tiles on October 29 (DR-07 to DR-11). Section 8 covers the variants. One item stays open:

1. **Rights (Q-16).** Which tool made the sheets, and under what terms. This is for the rights ledger only and holds nothing up.

## 1. What was done

- **Inputs.** The ten sheets you sent are saved in `work/research/chat-references/civic-line/`. Your assignment and answers are in `brief/phase-prompts/20261029_Civic-Line-Icon-Reconstruction-Prompt.md`.
- **Crops and inventory.** A script cut each pictogram from its caption and saved untouched source crops of both sheets. It confirmed the counts 24, 24, 24, 25 and 25, and wrote the 122-row inventory.
- **One weight, one scale.** The sheets' line weight drifts from 4.75 to 6.0 px. Every icon is drawn at one weight, 5.5 source px, the set's median (D2-31). One scale covers the whole set, so the widest icon, R-44, fills 116 of 128 units and every stroke exports at 2.68 units (D2-32).
- **Tracing.** Six tracers drew about 20 icons each. They worked one icon at a time: drew it, rendered it over its source crop, measured it and corrected it. Each kept a log of every clean-up. Each icon is one drawing with a separate accent group, and both editions are written from it.
- **Independent review.** The creative director checked all 122 against both sheets. 100 passed on first reading and 22 went back for fixes. A second check verified 21 of them. The last, the leaf in CL-070, was redrawn again and checked by the main session.
- **Exports.**
  - 244 SVGs and 488 transparent PNGs at 256 and 512 px.
  - Ten contact sheets carrying the approved Edition 06 wordmark (DR-05).
  - The searchable catalog.
  - A size ladder, and the pillar-mark side by side.
  - A review package.
- **Pillar marks.** CL-019 Explain, CL-020 Track, CL-021 Connect and CL-022 Act replace the Gate 1 pillar marks (DR-04, C-017). The record at actual sizes is `work/build/assets/civic-line/qa/20261029_Pillar-Marks-Side-By-Side.png`. No Direction A masters were drawn after Gate 1, so the record uses the Phase 1 sketch's 24 px cut.

## 2. Verification

**Tested**

- `verify_set.py`: 0 errors.
  - Counts: 122 IDs, 244 SVGs, 488 PNGs, 244 reference crops, 10 contact sheets.
  - Edition identity: every black file is its red-black file with Pillar Red replaced by Charcoal, byte for byte. A comparison of the parsed element trees agrees: 2,241 elements, with 342 color swaps as the only differences.
  - No red in any black file.
  - Every SVG parses, has a 0 0 128 128 viewBox, and has no text, images or background rectangles.
  - Nothing is drawn outside the box once stroke width is counted.
- Pipeline tests: 56 of 56 pass.
- Bake check: every export, rendered back at source scale, matches its source drawing. The 4x score is 1.000 for all 122.
- Catalog checks: 53 of 53 pass.
  - axe-core 4.10.2 finds 0 violations at 1440 and 390 px, in light and dark.
  - No horizontal scroll.
  - Search, edition, sheet and size controls, keyboard order and focus, and both theme overrides all work.
- Contact sheets: all ten sheet comparisons viewed beside their sources.
- Package: the zip was reopened and every entry matched byte for byte against its source.
- Visual review: every overlay by its tracer, all 122 by the independent reviewer, and the 22 fixes again after rework.

**Not tested**

- Rendering outside Chromium, and opening the files in Illustrator, Figma or other design tools.
- Whether people can name the icons. Every reader so far is an agent (Q-13).
- Pixel identity with the sheets. The SVGs are traced reconstructions and render differently from the generated rasters. The reference crops keep the source pixels.
- The catalog inside the claude.ai viewer beyond the published page itself.

## 3. Fidelity

Metrics compare each trace with its own source crop at source scale. The best offset is (0, 0) for all 122.

| Measure | Median | Range |
|---|---|---|
| Silhouette overlap (IoU) | 0.924 | 0.683 to 0.983 |
| Red overlap (IoU) | 0.896 | 0.626 to 0.995 |
| Mean edge distance | 0.20 px | 0.08 to 0.99 px |
| 95th percentile edge distance | 0.56 px | 0.25 to 2.06 px |
| Ink ratio, trace to sheet | 0.986 | 0.883 to 1.166 |

Most of the spread is deliberate. Where the sheet draws heavier or lighter than 5.5 px, the trace keeps the centerline and its edges sit evenly inside or outside the sheet's. Examples: CL-069 to CL-072 run 12 to 14 percent heavier, and R-50 runs 14 percent lighter. Per-icon figures are in `work/build/assets/civic-line/qa/20261029_Civic-Line-Fidelity-Metrics.csv` and in each icon's detail view in the catalog.

**Icons below 0.85 silhouette overlap, and why**

| ID | Overlap | Cause |
|---|---|---|
| R-44 | 0.68 | The two windows now share one top line, a 1.35 px move each (D2-38) |
| R-46 | 0.74 | One seat size per row, evenly spaced; the end seats move up to 2.7 px (D2-37) |
| CL-022 | 0.80 | Act's ring centered on the fingertip, a 1.8 px move, plus the sheet's heavier stroke |
| R-50 | 0.82 | The sheet draws 14 percent lighter than the set's weight |
| R-22 | 0.83 | Central figure moved 2.15 px onto the shared axis |
| CL-025 | 0.83 | Congress made symmetric; its parts drifted up to 1.75 px on the sheet |
| CL-071 | 0.83 | The sheet draws 13.6 percent heavier |
| R-49 | 0.83 | Arc and figures centered on one axis |
| CL-020 | 0.85 | Track's lens made a true circle and its two loops one radius |
| CL-067 | 0.85 | Healthcare's cross given four equal arms |

**Unresolved differences, by ID.** These are known and small. None is a missing part.

- CL-023 and R-27: the sheet fills small crotches where a handle meets its lens. The trace leaves those fillets out.
- CL-024: the arrows are about 1 px heavier on the sheet.
- CL-032: one inner corner is about 1.5 px softer on the sheet.
- CL-036: the dollar's terminals flare 0.8 px on the sheet.
- CL-056: a 1 px dip in the bulb base window is not drawn.
- CL-066: the cloud's notches are up to 0.8 px less sharp, because of round joins.
- R-11: the gavel's handle slit is cut at a constant 1.5 px.
- R-46: the two lowest outer seats are squarer on the sheet.
- R-47: the black sheet draws the right connector 4.5 px longer than the left. The trace mirrors the left, as the red sheet does.

**Where the image overrode the catalog text (D2-36)**

- Counts: CL-005 has a fourth figure, CL-023 five rules, CL-026 one desk leg, R-23 four bars, R-39 three people and R-40 two message strokes. CL-059 has no stem.
- Red: the red sheet colors more than the catalog names in CL-035, R-20, R-25, R-36, R-42 and R-48. It colors less in CL-017 and R-39.

**Removed as generation accidents:** a stray teardrop in CL-016, a hairline in R-20, a faint diagonal in R-34 and an extra blob on R-03's red sheet. Each is logged.

## 4. Small sizes

These are for your information; the masters do not change. At the shared scale the stroke is 0.67 px at 32 px and 0.5 px at 24 px.
- 41 icons still read at 24 px, including all four pillar marks.
- 53 more read at 32 px but not at 24.
- 28 stop reading at 32 px. These are mostly icons with three or more subjects, or ones that rely on a small inner sign.

The lists by ID are in section 6 of `work/handoffs/phase-2/20261029_Civic-Line-Review.md`. The ladder is `work/build/assets/civic-line/qa/20261029_Civic-Line-Size-Ladder.png`. Use below 48 px would need simplified small-size drawings, which no one has asked for yet.

## 5. Risks

- Option 1 framing leaves compact icons small in their square. Option 3 eases that with at most a 25 percent spread in line weight.
- Some sheets draw heavier or lighter than the set's weight, so a few icons read a shade lighter or heavier than you remember from the sheet.
- The set came from generated images. The rights ledger still needs the tool and its terms (Q-16).

## 6. What happens next

1. Your framing choice, then one rebuild and a republish of the catalog.
2. On your approval of the set, the package moves to `deliverables/`.
3. Then the visual system for the atlas and systems maps, and after that the other open items of the direction review (DR-06). That is a good point to start a new chat; the decision log, this report and the handoffs carry everything forward.

## 7. Change log

Paths are relative to `oath-and-action-v6-brand-guide/`. Nothing in `source/` changed.

**Created**

- `brief/phase-prompts/20261029_Civic-Line-Icon-Reconstruction-Prompt.md`
- `work/research/chat-references/civic-line/`: your ten sheets
- `work/build/assets/civic-line/`:
  - `src/`: 122 drawings and 122 correction logs
  - `red-black/` and `black/`: 244 SVGs
  - `png-256/` and `png-512/`: 488 PNGs
  - `contact-sheets/`: 30 files, ten sheets as SVG, PNG and 2x PNG
  - `reference-crops/`: 244 untouched crops
  - `qa/`: masks, zooms, overlays, size strips, metrics, status files, the completion ledger, the fidelity CSV, the framing options, the size ladder, the pillar record, sheet comparisons and catalog screenshots
  - The inventory (JSON and CSV) and the catalog page
- `work/build/packages/20261029_Oath-And-Action-Civic-Line-Icons_REVIEW.zip`: 19 MB, 1,010 entries
- `work/build/scripts/civic-line/`: 21 build, trace, verify and export scripts
- `work/build/tests/civic-line/test_pipeline.py`
- `work/handoffs/phase-2/`: the tracing guide, the review and the review fixes
- `work/ledger/20261029_Civic-Line-Icons-Report.md` (this report)

**Modified**

- `work/ledger/20261020_Decision-Log.md`: DR-01 to DR-06 (your answers) and D2-31 to D2-39
- `work/ledger/20261020_Change-Ledger.md`: C-016 to C-018
- `work/ledger/20261020_Open-Questions.md`: Q-15 and Q-16
- `work/research/20261020_Rights-Ledger.md`: the October 29 sheets

## 8. Variants, built after approval (DR-07 to DR-11)

Dustin approved the set and the studio's recommendations and asked for tiles and light versions. The catalog at the same link now shows them.

- **Framing.** Every standalone file uses the capped fit, option 3 (DR-08). 90 icons stop at the 1.25 cap and 32 fill to 116 units. Strokes run 2.68 to 3.35 units.
- **Four editions from one drawing.** Red-black and black for Newsprint and White grounds; red-newsprint and newsprint for Charcoal grounds. Newsprint alone serves Prussian, where red never sits. All four share every coordinate; verify confirms identical element trees with only ink colors swapped.
- **Tiles.** Square, rounded square and circle, on a Charcoal tile with the light editions and a Newsprint tile with the dark editions, each in two-color and one-color: 12 per icon, 1,464 SVGs and 2,928 PNGs. The rounded square is a superellipse of exponent 5 with continuous curvature (D2-41). Icons sit at 0.68, 0.66 and 0.62 of the tile, with an optical scale for 36 icons and a small sideways shift for 8 (D2-40, D2-44). The smallest margin to a tile edge is 21.45 units of 128 (R-44, square).
- **Minimum tile sizes (D2-42).** Two-color tiles: 72 px square, 76 px rounded, 80 px circle. One-color tiles: 48, 52 and 52 px, or 72, 76 and 80 px for the 28 icons that need 48 px on their own. The inventory records them per icon, and the catalog marks any card shown below its minimum.
- **Sheets.** Ten light contact sheets on Charcoal and twelve tile overview sheets, with one header and footer geometry across all 32 sheets.
- **Contrast.** Charcoal on Newsprint and Newsprint on Charcoal 13.29:1; Pillar Red on Charcoal 4.49:1, on White 4.17:1, on Newsprint 2.96:1; Newsprint on Prussian 9.42:1. Red on Newsprint sits under the 3:1 guideline for graphics, so the red parts carry emphasis while the shapes carry the meaning. The full table is `work/build/assets/civic-line/qa/20261029_Civic-Line-Contrast-Table.md`.
- **Usage rules in the readme.** Two-color tiles only where an icon stands alone (Rule 05.3); no Newsprint tile on a White page, where its edge measures 1.41:1; give app platforms the square tile and let them apply their own mask.
- **Review.** The design director reviewed the variants and raised two musts and eight shoulds; all ten are applied (`work/handoffs/phase-2/20261029_Civic-Line-Variant-Review.md`).

**Checks.** Verify: 0 errors, including an audit of 16,141 ids across 1,985 files with none repeated. Pipeline tests: 85 of 85. Catalog checks: 84 of 84, axe 0 violations at 1440 and 390 px in light and dark. A Chromium test with two files on one page shows 0 changed pixels after the id fix, against 16 broken pairs before.

**Not tested.** Safari, Firefox and design tools; app-store and Android icon specifications; most of the 2,928 tile PNGs one by one (the 12 overview sheets and samples were viewed); any human observer.

**Package.** `deliverables/20261029_Oath-And-Action-Civic-Line-Icons-SVG.zip` (14.2 MB) and `deliverables/20261029_Oath-And-Action-Civic-Line-Icons-PNG.zip` (77.9 MB). One zip came to 92 MB, so it is split in two.
