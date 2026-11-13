# Production test 1: a designer makes a county map from chapter 14 and the kit alone

Oath & Action Edition 06, Phase 3, round 3 review, November 13, 2026. **Simulated panel, untested with real people.** The UX and accessibility lead played a designer who knows the guide's chapters but not this round's notes, and worked only from chapter 14's rules and entries in the built guide, the specimen pages, and the kit's README. Every step, every place looked and every guess is logged. Nothing was written into `work/build/`.

**The task.** "Where in the country do the most people under 65 go without health insurance, county by county, and how sure can a reader be of any one county?" Data: `census-sahie-county-uninsured` (3,144 counties, each with its margin).

## Files in this folder

- `sahie_classes_derive.py`: the designer's derive script (Rule 14.9's tests, the class column).
- `census-sahie-county-uninsured-classes.csv` and `.meta.json`: the derived file and sidecar it writes (`kind: "derived"`).
- `p03_kit_run.mjs`: a runner that calls the kit's own exported `run_spec` with a scratch data folder (step 7 says why).
- `20261113_P03-Spec-V1.json` to `20261113_P03-Spec-V4.json`: the spec at each step.
- `20261113_P03-Check-V1.txt`, `20261113_P03-Check-V2.json` to `20261113_P03-Check-V4.json`: the kit's output for each.
- `20261113_P03-Counties-Export.csv`: the CSV the kit writes for V3 and V4 (3,144 rows).
- `20261113_P03-Capture-V4-Newsprint-1440.png`, `-390.png`, `20261113_P03-Capture-V4-Charcoal-1440.png`, `-390.png`.

## Steps

1. **Read the question.** "The most people" can mean a count or a rate. "How sure can a reader be of any one county" asks for margins. *Guess:* the file gives a margin only for the percent (`uninsured_moe`, in points), none for the count of people, so the honest map is a rate map.
2. **Pick the form** (chapter 14, group 15, "Maps: where is it happening?"). Entry 14.120 says "Use it when: the reader asks how a figure varies across the whole country, place by place". Entry 14.122 says use a dot density map when "a count matters more than a rate", and its "Use instead" sends a rate back to 14.120. Neither entry says what to do when the question names a count but only the rate carries a margin. *Guess:* 14.120, the county choropleth. Time to choose: about five minutes of reading.
3. **Find the starter.** The README's starter table stops at round 2 (`range-bar` to `bullet-graph`); it has no `county-choropleth` row, and the README still says "65 files" and "The specs for S01 to S64". Entry 14.120's "For builders" line named `s81` and `county-choropleth`, so I copied `specs/s81.json`.
4. **Read the map recipe.** The README's "Maps (round 3)" section told me to name the data file first and the boundary file second, and showed `table.group` with "the CSV export lists every row". Clear.
5. **The class column.** The form's header and entry 14.120 say the drawing reads `cls`, "written by a derive script". The README's "Summaries" paragraph names the sidecar keys (`kind`, `derived_from`, `derivation`). No shared tool writes a class column, so I read S81's derived sidecar for its shape and wrote `sahie_classes_derive.py`.
6. **Rule 14.9's class map paragraph.** "Make each class at least as wide as the widest margin of error drawn." The widest margin is 3.3 points (the widest interval 6.6). *Guess:* the rule says margin, so classes 4 points wide pass. Breaks at 8, 12 and 16 percent:
   - classes 634, 1,144, 753 and 612 counties, and Kalawao County, Hawaii, with no estimate;
   - 1,705 of the 3,142 counties with a published margin have an interval that crosses a break, and none crosses two;
   - no two counties drawn two classes apart sit within their gap's margin (the second test, by script);
   - Loving County, Texas, has an estimate and no published margin (the source prints "<0.1").
   I tried 8, 13, 18 and 10, 14, 18 as well; 8, 12, 16 kept round numbers and crossed no county two classes.
7. **First run, the README's way** (`oa-chart.mjs check` on spec V1). Two faults:
   - `"source_line" is missing`. The README's step 5 says to leave it out; its key list says only "a chart of one dataset may leave it out", and a map always names two.
   - `no sidecar work/build/data/census-sahie-county-uninsured-classes.meta.json`. The kit reads data only from `work/build/data/` and the command has no option for another folder. A designer outside the studio, or one told not to write there, stops here. **Help used:** I read `oa-chart.mjs` and called its exported `run_spec` with `data_dir` set to a scratch folder linking every frozen file plus mine (`p03_kit_run.mjs`). The README does not describe this.
8. **V2: a source line written by hand**, joining the SAHIE line and the boundary file's. 0 faults with the sweep. But I wrote "Retrieved November 11 and 12, 2026", and the boundary file's sidecar says November 13; the kit passed the wrong date. V3 corrects it: 0 faults.
9. **The national figure.** Entry 14.120 says "Put the national figure above the map". The SAHIE file holds no national row and the kit did not flag its absence. *Guess:* leave it out and ask the research lead for a national row, as S81's maker did. V3 and V4 print none.
10. **The evidence label.** The starter (S81) says "Finding". The sidecar says "Model-based estimates". Nothing in the entry or the README says how to label a modeled figure. I searched the specs for the dataset's name, found S51 with "Estimate" and "Documented: the Census Bureau's Small Area Health Insurance Estimates", and copied both. The kit does not check the label against the sidecar.
11. **The table.** Grouped by state with counts in each class and the lowest and highest county, as S81 does, it answers "where" but not "how sure". V4 adds "Could fall in the next class" (`count_in` on `breaks_crossed`); its 51 rows sum to 1,705, matching the note. The CSV holds all 3,144 counties with percent, margin, people, class and breaks crossed. The state rows print in postal-code order (Alaska before Alabama), as S81's do.
12. **Weight.** Nothing in the README, the entries or the kit's output says how many bytes a plate may carry. **Help used:** I found "share per plate 14,106" in the build report. Measured the kit's way (`K.figure` with the lean table and `island_table`, as guide_build.py's load-table method places an entry): V4's figure is 12,664 bytes, about 13,400 with a 750-byte frame, under the share.
13. **Result.** V4 passes the kit's check, sweep included, at 0 faults, and draws at 1440 and 390 px on both grounds (captures in this folder). Title: "In 2024, 612 counties had 16 percent or more of people under 65 without health insurance by the Census Bureau's estimates, 397 of them in Texas, Georgia and Oklahoma." Counts checked by the derive script.

## Did chapter 14 and the README lead the designer, without help?

| To | Reached unaided? | How, or what stopped them |
|---|---|---|
| The form | Yes, with a guess | Entries 14.120 and 14.122; the count-or-rate question is not covered |
| The map parts | Not needed | The form draws every part; the README's map section reads clearly |
| The class column and its derive script | Partly | The entry says "a derive script"; no shared tool, so the designer copied S81's sidecar shape |
| Rule 14.9's tests | Yes | The rule's paragraph and a script; the rule says "margin", which allows 4-point classes here |
| `table.group` with every county in the CSV | Yes | README and entry 14.120's builders line |
| Running the kit on a derived file | **No** | The kit reads only `work/build/data/`; the README never says so or offers another way |
| The source line | Partly | README step 5 misleads for maps; a wrong retrieval date passed |
| The national figure | **No** | Required by the entry, absent from the file, not checked |
| The weight limit | **No** | Not in the README, the entries or the kit's output |
