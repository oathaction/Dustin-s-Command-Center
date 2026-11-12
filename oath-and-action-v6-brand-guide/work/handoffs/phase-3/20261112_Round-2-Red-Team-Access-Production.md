# Round 2 red team: accessibility and the production test

Oath & Action Edition 06, Phase 3, round 2, November 12, 2026. Written by the UX and accessibility lead (`oa-ux-accessibility-lead`) as reviewer for `work/handoffs/phase-3/20261112_Phase-3-Round-2-Review-Brief.md`. I then ran a simulated panel. **The panel is simulated and untested with real people.** Its files are in `work/handoffs/phase-3/round-2-production-test/`. Paths are relative to `oath-and-action-v6-brand-guide/`.

**What I tested on.**
- The strict build at `/tmp/claude-0/-home-user-Dustin-s-Command-Center/3ab6316c-6935-5f23-804c-cfaafd548447/scratchpad/phase-3/round-2-review/main/guide.html` (10,587,775 bytes). I copied it into my scratch folder and left the original unchanged.
- For scripts off, I used the full page.
- For widths, forced colors, axe-core, print, reduced motion and the accessibility tree, I used a copy that keeps only chapters 13, 14 and 15, with the same shell, kit, tokens and fonts. I made it by loading the build with scripts off, removing the other chapter sections and saving the page (`guide-ch13-15.html`, 3,238,178 bytes).
- For narrow plots, I used my own kit builds of the 26 round 2 specs.
- My scripts, results and captures are in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/3ab6316c-6935-5f23-804c-cfaafd548447/scratchpad/phase-3/round-2-review/access-production/`.

## 1. Score

**4 of 5.** Every reading path holds for the 22 new specimens, the four built entries, the 15 sketches and chapter 15's six new rules:
- scripts off, with tables equal to the data;
- axe-core, with 0 violations;
- forced colors in both themes, with every drawing word at 13.98 to 1 or more;
- reduced motion, reflow and 200 percent zoom;
- chapter 15's wide stage at 1024, 800 and 768 px.

One fault takes away the very thing a specimen exists to show. S58's margin-of-error band is drawn at 1.16 to 1 and cannot be seen at any phone width.

## 2. Must fix

**AX M1. S58's margin-of-error band cannot be seen, so the band chart reads as an exact line.**
- **Where:**
  - `specs/s58.json`, entry 14.75;
  - Rule 14.75's own words, "a band in Stone magnitude step 1";
  - the data lead's ruling (e), "Stone magnitude steps for bands".
- **What is wrong.**
  - The band is `oac-f-mag-1`: rgb(204, 202, 197) on Newsprint rgb(220, 217, 210), **1.16 to 1**. On Charcoal it is rgb(35, 36, 38) on rgb(18, 18, 18), **1.21 to 1**.
  - The band has its size: about 6.5 px past the 2 px line on each side at 358 px. What it lacks is contrast.
  - In the guide at 390 px (a 326 px drawing), and in kit drawings at 358, 296 and 256 px, I could not find it in captures at 2x.
  - At 1440 px it shows as a faint haze only to a reader who knows to look.
  - Yet the chart note says "The gray band around the line spans each year's margin of error", and the title's claim rests on that band. The simulated reader asked why the end label says "±$1,040" when nothing on the line shows a range.
  - Forced colors outline the band, so it shows there. Normal color is where it is lost.
  - This is the brief's named fault in a new form: every kit check passes, and the interval is gone.
- **Rules broken.**
  - WCAG 1.4.11: the band is the graphic a reader needs, at under 3 to 1, with no edge to carry it.
  - R2-4's intent: an estimate is drawn with its interval.
- **Fix.**
  - Draw the band with edges in the context ink at 1 px (`K.parts.band` already takes `edge` and `edge_width`; rgb(93, 99, 109) measures 4.29 to 1 on Newsprint). Or draw it in a step that reaches 3 to 1 against the ground.
  - Change Rule 14.75's words to match, and the data lead's ruling (e) for bands that carry an interval.
  - Add a kit check for any `interval` form: the band's fill or edge reaches 3 to 1 against the ground, and the band shows at least 2 px past its line at every checked width.
  - S59's outer band uses the same step. It is wide and its ends print their figures (2.0 and 6.2), so it reads, but the same check would cover it.
- **Owners:** the data lead (ruling (e)), maker B (S58), the editor (Rule 14.75's words), the engineer (the check).

## 3. Should fix

**AX S1. The kit checks six widths; the guide draws a chart at any width from 256 to 723 px, and several specimens fault between them.**
- **Where:** `oa-chart.mjs` `GUIDE_WIDTHS` (656, 558, 358, 326, 296, 256); S63; S01; round 1's S09, S11, S13, S16, S25 and S34.
- **What is wrong.** I drew every spec at every whole width from 256 to 723 px with the kit's own `check_drawing`. Faults:
  - **S63:** at 18 widths, an issue title runs 0.7 to 1.9 px past the artboard. These include:
    - 329 px, which is a 393 px phone, the width of current iPhones. In the guide at 393 px, S63 carries `data-oa-warnings="1"`.
    - 560 px, which is a 768 px tablet, where the guide also flags it.
    - 636 px, which is a 700 px window.

    The words touch the edge, for example the "l" of "Federal".
  - **S01:** at every one of the 95 widths from 375 to 528 px (windows of about 439 to 592 px, a phone held sideways), the big "86%" runs into "By party", "Democrats" and "Republicans". I saw it at 480 px in Chromium: the "%" overlaps the "D" and the "R". S01's drawing is as Dustin approved it on board 1, at the widths board 1 showed.
  - **S09:** at 39 widths from 497 to 660 px, including 560 px at a 768 px tablet: words past the edge and a leader through "Congressional Budget and Impoundment".
  - **Round 1's S11, S13, S16, S25 and S34:** a few widths each.
  - The kit draws the 1440 and 390 px pages and six columns. It misses 329, 560 and 636, which the shell gives at common screens.
- **Fix.**
  - The kit's `build` draws every whole width from 256 to the artboard in Node, as I did. That took 24 seconds for 26 specs.
  - Maker A fixes S63's title wrap and S01's figure size.
  - The engineer clears the stale `data-oa-warnings` when a redraw is clean. `K.mount` never removes it today.
- **Owners:** the engineer, maker A (S63, S01), and the round 1 makers for their specs.

**AX S2. Lines and marks cross words at 256 and 296 px, and no guard sees them.**
- **Where:** `forms/waterfall.js` (S44), `forms/parliament.js` (S48), `forms/beeswarm.js` (S50).
- **What is wrong.**
  - **S44:** at 256 and 296 px, gridlines cross the minus sign of "−48.0", "−39.9", "−21.0", "−57.1" and "−52.6". A minus with a line through it can read as a plus. In forced colors, the GrayText gridlines cross the same words.
  - **S48:** at 256 px, which is a 320 px window, "1 independent, 2 vacant" sits on the inner rows of seats. At 296 px it touches them.
  - **S50:** at 256 px, the dashed "All 50 states" line runs through the 0 of "Alaska $2,290", the named mark's figure.
  - My probe found no text outside a drawing and no text on text at 656, 358, 326, 296 and 256 px for all 26 specs. The kit's guard does not test words against lines or dots in these forms.
- **Fix.** A halo on each value label, as other forms draw, or keep the labels clear of the gridlines. Place S48's label below the inner arc where the arc is too small. Then extend the layout guard to words against strokes and dots.
- **Owners:** the engineer (guard), maker A (S44, S48), maker B (S50).

**AX S3. In forced colors, S44's totals take the same inks as its steps.**
- **Where:** `kit.js` `K.FC` (`context: 'GrayText'`, `div-5: 'GrayText'`, `subject: 'CanvasText'`, `div-1: 'CanvasText'`); S44.
- **What is wrong.**
  - In both contrast themes, the "All receipts" total takes the key's "Adds to the running total" ink: dark red in light, green in dark. It reads as a step of +5,403.3.
  - The deficit takes the "Takes away from it" ink.
  - The note names colors the reader then does not see: "Steps that add are green and steps that take away are dark blue ... The bar for all receipts, in gray".
- **Fix.** Give a waterfall's totals their own forced-colors treatment, such as Canvas with a CanvasText outline. Name steps and totals in the note by role and place, not by color alone.
- **Owners:** the engineer (forced colors), maker A (S44's words).

**AX S4. S53 names its marks by color, and in forced colors they are not red.**
- **Where:** S53's drawing label "Red bars: ages 55 to 64, 41.2 million", its alt ("are red") and its chart note ("The red bars"). S47's note ("in red") is a lesser case.
- **What is wrong.**
  - In forced colors the bars are Highlight: cyan in the dark theme, deep blue in the light one. The words then name a color that is not on the screen.
  - For a reader who cannot tell red from gray, the band's Charcoal outline is the cue, and no word mentions it. The red against the light-fill bars beside it measures 1.63 to 1.
  - WCAG 1.4.1 holds, since the axis gives the ages. The label still teaches a reader to find the mark by its color.
- **Fix.** Name the mark by what it is, for example "Ages 55 to 64, outlined: 41.2 million", and keep red as a second cue in the alt and note.
- **Owners:** maker B (S53), maker A (S47), the editor (the words).

**AX S5. Four tables leave out, or leave unexplained, what the drawing shows.**
- **Where:** S53, S62, S51 and S58.
- **What is wrong.**
  - **S53:** the last row's header reads "100", while the drawing prints "100+" and the sidecar says "100 is 100 and over". A table reader hears 31,539 men aged 100.
  - **S62:** the table lists Congress.gov's seven actions but not the tracker's six steps or which two never happened. Only the alt says it.
  - **S51:** the drawing places 62 open circles, the farthest at 42.5 percent. The table and the CSV give only each region's count of counties past a whisker, so a reader of the table cannot learn the spread past the whiskers.
  - **S58:** 37 of the "Change in the survey" cells are blank, with no word for what a blank means. Round 1's S6 set that standard for S37 and S25.
- **Fix.**
  - S53: "100 and over".
  - S62: a "Step" column, with two rows for the steps that never happened.
  - S51: a "Highest county" column, or the 62 counties in a second table.
  - S58: "None" or the column's `empty` key.
- **Owners:** maker B (S51, S53, S58), maker A (S62).

**AX S6. A screen reader skips the avoid sketches' "do not publish" bar and hears each caption twice.**
- **Where:** the sketch stages from `phase3_ch14_build.py` and `guide_build.py`.
- **What is wrong.**
  - Each sketch stage is `role="img"` with `aria-label` set to the whole `sketch_alt`. A screen reader that reads an image as one object, as NVDA, JAWS and VoiceOver do in reading mode, hears that name and skips what is inside. In the four avoid pairs, that includes "Form to avoid: do not publish" and "Use instead: Bars" (14.57, 14.73, 14.91, 14.92). The plate's head, "Gauge, a form that misleads", still reaches the reader.
  - The visible caption (RS-S2) is the name's first sentence, so it is heard twice. For 11 of the 15 sketches, the name and the caption are the same sentence word for word.
- **Fix.** Make an avoid stage a group, named for its plate, holding the two drawings as images and the two bars as text in reading order. Or put "Form to avoid, do not publish" at the head of the stage's name. Then give the stage a name that does not repeat the caption, or hide the caption from assistive technology where the name holds it.
- **Owner:** the engineer.

**AX S7. The kit's README does not know round 2** (production test 1, steps 2 and 8).
- **Where:** `work/build/chart-kit/README.md`.
- **What is wrong.**
  - It still says "45 forms in 43 files" and "The specs for S01 to S42". The forms folder holds 65 files and the specs run to S64.
  - Its starter table has no row for `range-bar` or any other round 2 form.
  - Its only mention of intervals is `interval_of` and `whisker` in the parts list. A designer learns R2-C1, the interval form's contract, only from the kit's own faults.
  - Round 1's S8 found the same lag.
- **Fix.** Bring the table up to S64, and add one paragraph on the interval contract: fields, the level in the measure line, the margin column in the table, and the test for "differs".
- **Owner:** the engineer.

**AX S8. The designer could not draw the asked chart from the frozen data, and the kit passed a wrong source line** (production test 1, steps 3 to 5 and 8).
- **Where:** `census-acs-broadband-by-state` and its sidecar; `checks.js`.
- **What is wrong.**
  - The file holds `broadband_fixed_pct` with no margin in points. The only fixed margin, `broadband_fixed_moe`, is in households.
  - A designer cannot add a computed column. R2-2's derived files belong to a maker's script and the research lead's check.
  - With the household margin, the kit gave 1,030 faults ("a line (context) drawn outside its drawing, at x -90302 to 91398"), with no word that the margin and the value are in different units, though the sidecar gives both.
  - With a margin in points, the spec passed while it printed the sidecar's default source line, "broadband of any type", on a chart of fixed broadband. Leaving out `source_line` is what the README tells a designer to do.
  - One fault message reads "both "undefined" and "undefined"".
- **Fix.**
  - The research lead adds a margin in points beside every stored percent whose margin is a count.
  - The research lead's `source_line_variants` name the columns each one covers, and the check fails a line for a measure the chart does not draw.
  - The check fails a margin whose unit differs from its value's.
  - The message names the missing fields.
- **Owners:** the research lead, the engineer.

**AX S9. S45's middle stack cannot be seen for 17 of its 26 years.**
- **Where:** S45, `forms/stacked-column.js`.
- **What is wrong.** "Two to four units" is drawn under 1 px tall (0.8 to 1.1 px) from 2009 to 2025, at every width. The key names a mark the reader cannot find in those years. The note gives its 2024 count, and the table gives every year.
- **Fix.** Give a stacked segment a visible minimum with its figure printed, or say in the note that the segment is too thin to draw after 2008.
- **Owners:** maker A, with the data lead.

**AX S10. Words that stopped the simulated reader** (production test 2, `round-2-production-test/20261112_Reader-Log.md`).
- **Where and what.**
  - **Entry 14.60:** "quartile", which the rule never calls the middle half; the measure line says "middle half" but not "quartile".
  - **Entries 14.75 and 14.90:** "Stone magnitude step 1" and "magnitude steps", builder names for a color, in the rule a reader reads.
  - **Rule 15.12's plate:** "money, lowers", "information, raises" and the double ticks, with no key on that plate. The key is on Rule 15.13's plate, the next rule.
  - **Rule 15.17's plate:** the pills carry the atlas's variable names ("Executive unilateralism", "Congressional capacity") where the rule names bodies ("the executive", "Congress"), and its key leaves out the ticks.
- **Fix.**
  - Gloss "quartile" at first use.
  - Move color-step names to "For builders".
  - Point Rule 15.12's plate to Rule 15.13's key, or carry a short key.
  - Print each body's plain name with its variable name on Rule 15.17's plate, and add the ticks to its key.
- **Owners:** the editor (chapter 14's words), the systems designer (chapter 15's plates).

**AX S11. Print: a blank page, and a clipped plate head.**
- **Where:** `guide-shell.css` print rules; chapter 15's plate heads.
- **What is wrong.**
  - In Chromium's Letter PDF of chapters 13 to 15 (360 pages), page 11 is blank. It falls between chapter 13's first group opener and its first plate.
  - On chapter 15's plates, the head's right-hand note runs off the page. The failure plate of 15.12 prints "True size, 328 px wi".
  - Nothing else is lost: all 74 chapter 14 figures drew and opened their tables at `beforeprint`, and no page holds a title stranded from its chart. Round 1's S4 is closed.
- **Fix.** Let the first plate break from the opener, and wrap the plate head's note in print.
- **Owner:** the engineer.

## 4. The seven named places

1. **Narrow plots** (mine).
   - **Lost:**
     - S58's band at every phone width (AX M1);
     - S45's middle stack for 17 years (AX S9).
   - **Crossed or covered:**
     - S44's minus signs at 256 and 296 px, S48's label at 256 px and S50's "$2,290" at 256 px (AX S2);
     - S63 and S01 between the checked widths (AX S1).
   - **Seen and sound:**
     - S57 stacks its rows under 240 px and keeps every interval, though intervals narrower than the 7 px dot hide inside it (Florida at every width; California, Florida, New York and Texas at 256 px). Its chart note says so, and the table gives every margin.
     - S54 and S55 drop the United States label at 256 px and say so in a note.
     - S59 thins its year ticks at 296 and 256 px and keeps every median value.
     - No text sits outside any drawing at 656, 358, 326, 296 or 256 px.
2. **Derived summaries** (the statistics reviewer rebuilds them).
   - In my lens: S49, S51, S52 and S56's tables hold the derived rows (22, 4, 37 and 103), with live text and header scope.
   - Each note says each judge or county counts once.
   - S51's table leaves out the outlier file's 62 rows (AX S5).
3. **The party test** (not my lens). S48 names each party on its block and in its table. In forced colors every seat keeps one ink.
4. **S63's window** (not my lens). Its chips, words and dates print as live text with scripts off. Its width fault is AX S1.
5. **The four Estimate labels.** On S51, S52, S53 and S59, the label "Estimate", the "Documented:" line and the method note print as live text with scripts off. The simulated reader stopped at "Estimate" beside "Documented:" and found the answer three lines down in the note's "Method:" line.
6. **Chapter 15 against Atlas V7** (not my lens). For the six new rules I tested:
   - widths;
   - forced colors (the stages keep their colors, as AX-S6 set in round 0);
   - names and descriptions (each stage is a group named for its rule, described by its alt);
   - 320 px: the frames scroll 40 px with a tab stop and hint. Only 15.12's "Technology layer" and "Core layer" sit past the visible edge, inside a drawing.
7. **The sketches** (mine).
   - **Captions:** all 15 print `sketch_alt`'s first sentence as the caption, the same sentence as the first `<desc>`, with the "Illustrative" tag.
   - **Type:** every word is 13 px or more at true size, at 1440 and 390 px.
   - **Bars:** each of the four avoid pairs sets "Form to avoid: do not publish" over the misleading half only and "Use instead" over the better choice, at 1440 px side by side and at 390 px stacked. I saw no way to take an avoid drawing for one to copy.
   - **Fault:** the screen-reader names (AX S6).

## 5. Questions for Dustin

None. AX M1 keeps the band in the approved Stone steps (DR-236). Adding edges, or using a darker step, is the data lead's routine call.

## 6. Tested

**Scripts off**, on the full build at 1440 px:
- 79 kit figures in chapters 13 to 15, read with a script. All 26 round 2 entry figures (S43 to S64, S01, S06, S08, S10) show:
  - the title;
  - the alt as words;
  - the scripts-off line;
  - the source line;
  - an open table with a caption.
- Every header cell has `scope`.
- Rows equal my own count from each data file with each spec's `where` and pivot, for all 26. Where the spec draws a derived summary, I counted that file instead:
  - S49: 22 rows;
  - S51: 4;
  - S52: 37;
  - S56: 103.
- The 15 new sketches and four old ones show their drawings, bars and captions.

**Narrow plots**, kit builds of all 26 specs into scratch (all PASS, 0 faults):
- Drawn at 656, 358, 326, 296 and 256 px on both grounds, with a geometry probe:
  - text past the drawing;
  - text on text;
  - marks under 1.5 px.
- Contact sheets of every spec at 358, 296 and 256 px, and 2x crops of S44, S48, S50, S51, S56, S58, S59 and S63.
- S57's hidden intervals computed from the scale and the margins.

**Width sweep:** every whole width from 256 to 723 px through `check_drawing` in Node, for S01 to S64. The faults found were confirmed in Chromium for S63 (301, 329, 560 and 636 px) and S01 (380 to 520 px).

**Guide widths**, on the chapters 13 to 15 copy:
- Widths: 1440, 1024, 900, 800, 768, 700, 600, 540, 430, 412, 393, 390, 360 and 320 px, and 720 px at device scale 2 (200 percent zoom).
- Every figure drew, with no page error and no sideways page scroll.
- The smallest drawing text was 12.99 px at 1440 px, a rounding of 13.
- Guard flags: S63 at 393, 700 and 768 px; S09 at 768 px.
- Every scrolling table or plate frame has a tab stop, from 4 frames at 1440 px to 88 at 320 px.

**Chapter 15's wide stage:**
- At 1024, 800 and 768 px, all 37 stages hold in frames of 702, 736 and 704 px, with no sideways scroll; the wide plates draw at 680 px.
- At 390 and 360 px, every stage is 328 px with no scroll.
- At 320 px, each frame scrolls 40 px with its tab stop and hint. A text-node probe of the 12 new plates found words past the visible edge only on 15.12's layer labels.

**Forced colors**, Chromium's light and dark emulation at 1440 and 390 px:
- The probe covered every drawing text in the round 2 figures, the sketches and the four changed rule plates, measured against the paint under its center: 1,427 texts at 1440 px and 1,086 at 390 px.
  - 0 under 4.5 to 1 on a solid paint.
  - Lowest: 14.02 to 1 in the light theme and 13.98 in the dark.
  - Two words sit on a pattern, S46's "Medicaid" and "All other sources", each with a 3 px halo.
- Every data mark against its Canvas ground.
- Captures of S43, S44, S46, S47, S48, S51, S53, S58, S59, S62 and S64 in both themes. In S46, the Medicaid hatch and the all-other-sources hatch differ by line weight, and each band is named.
- Chapter 15's six new correct plates in the dark theme.

**Contrast by the WCAG formula, from rendered colors.** The text pairs come from the guide; the Charcoal pairs from kit pages of S43, S44, S46, S47, S53, S58, S59 and S62. 36 pairs:

| Pair | Ratio |
|---|---|
| Charcoal words on Newsprint (802 texts) | 13.29 |
| Secondary words rgb(78, 83, 91) on Newsprint (S62's steps, ticks) | 5.49 |
| White on Verdigris (S46 "Medicare", sketch 14.57) | 4.74 |
| White on Prussian (S46 "Medicaid") | 13.28 |
| White on Charcoal (S46, S62's step numbers, sketches) | 18.73 |
| Charcoal on the light fill (S47's tiles, S55) | 7.33 |
| Charcoal on Stone step 1 (S59's band words, sketch 14.70) | 11.44 |
| Charcoal on a Newsprint plate over S47's red tile | 13.29 |
| Charcoal on S06's four tints | 6.18, 8.01, 10.96, 11.76 |
| Newsprint words on Charcoal | 13.29 |
| Secondary words rgb(163, 161, 156) on Charcoal | 7.26 |
| Charcoal on the Charcoal-ground light fill (S47's tiles) | 5.41 |
| Newsprint on Stone step 1 on Charcoal (S59) | 11.02 |
| Charcoal on Prussian step 2 (S46 on Charcoal) | 6.18 |
| Subject ink on Newsprint | 13.29 |
| Red point on Newsprint, alone / its keyline | 2.96 / 13.29 |
| S53's red against the light-fill bars beside it | 1.63 |
| Light fill on Newsprint | 1.81 |
| Stone step 1, track and band, on Newsprint (S43's owners, S58's band, S61, S64) | 1.16 |
| S43's renter fill against its owner track | 1.56 |
| Verdigris (S45) | 3.37 |
| Context ink (S44's total, S51's whiskers) | 4.29 |
| Verdigris step (S44's adds) | 5.01 |
| Prussian (S44's take-aways, S45) | 9.42 |
| Charcoal deficit against Prussian steps (S44) | 1.41 |
| Gridline on Newsprint (sketches) | 1.47 |
| Red on Charcoal | 4.49 |
| Light fill on Charcoal | 5.41 |
| S44's steps on Charcoal | 5.42 and 5.55 |
| Stone step 1 on Charcoal (S58's band) | 1.21 |
| Track on Charcoal (S43) | 1.50 |
| Hexbin and contour steps (sketches 14.65, 14.66) | 1.70 and 2.46 |

- Every word clears 4.5 to 1.
- Marks under 3 to 1 print their value or word beside them, are context, or are steps in a keyed scale, as round 1 read WCAG 1.4.11. The exception is S58's band (AX M1).

**axe-core** (`work/build/node_modules/axe-core`, WCAG 2.0 to 2.2 A and AA plus best practice), scoped to chapters 13, 14 and 15 with every table open:
- 0 violations at 1440 and 390 px.
- "Color contrast" was left incomplete on 5,640 and 7,009 nodes, which is text over drawings and stages; I measured those myself (above).

**Accessibility tree:**
- Chromium's tree for sketches 14.91 and 14.54, S48, and chapter 15's plates 15.12 and 15.17.
- Every sketch's caption checked against its `sketch_alt` and first `<desc>` by script.

**Reduced motion** (`reducedMotion: 'reduce'`), at 1440 and 390 px: 0 transitions, 0 animations and 0 running animations in chapters 13 to 15. Scroll behavior is auto.

**Print:**
- Chromium Letter PDF of the copy: 360 pages. `beforeprint` drew all 74 chapter 14 figures and opened their tables.
- I counted pages by blank area and ink, and read the text layer: the six avoid bars, S51's "Gaines" note, S62's last action and S44's deficit are all present.
- I looked at the 15.12 pages at 50 dpi.

**Alt text:** I read all 26 round 2 entry figures' titles, alts, notes and chart notes, and checked S53's ages against the data by script (41,189,716 for ages 55 to 64; the largest single ages 23 to 37). S48, S53 and S62 each give the figures their title names.

**Production test 1 (simulated designer):**
- Spec versions V1 to V3 and four probe variants through the kit's check.
- The title's count by my own script.
- The drawing's dots counted in a kit page at 1440 and 390 px on both grounds.

**Production test 2 (simulated reader):** entries 14.60, 14.75 and 14.90 from the entry files and the build; Rules 15.12 and 15.17 from chapter 15's file and their plates as rendered.

## 7. Not tested

- **The four-width guide check and axe on the whole page.** The main session is running both.
- **The pages behind my results.** Forced colors, print and axe ran on the chapters 13 to 15 copy, not the full page.
- **Real people and real tools.** Real screen readers (NVDA, JAWS, VoiceOver, TalkBack), real devices and Windows' own contrast themes. Chromium's tree and Playwright's emulation stand in for them. AX S6 rests on how screen readers treat `role="img"`, which I did not run.
- **The panels.** Both are simulated and untested with real people.
- **Paper.** I read Chromium's PDF only.
- **Text and keyboard.** Browser text zoom alone and user text spacing (WCAG 1.4.12); I tested 200 percent as page zoom. A keyboard walk and focus-obscured check (2.4.11): round 2 adds no control besides table frames, whose tab stops I counted.
- **Other reviewers' ground.** The derived summaries' rebuild from source, the party test, S63's window, the Estimate labels against Rule 13.1, and chapter 15's values against Atlas V7.
- **Chapters 13 and 15's older plates.** I did not re-measure them in forced colors this round. Color-vision simulations were not run.

## Change log

Created:
- this report;
- `work/handoffs/phase-3/round-2-production-test/`, holding:
  - `20261112_Designer-Log.md`;
  - `20261112_Reader-Log.md`;
  - `20261112_P02-Spec-V1.json`, `20261112_P02-Spec-V2.json`, `20261112_P02-Spec-V3.json`;
  - `20261112_P02-Check-V1.txt`, `20261112_P02-Check-V3.json`;
  - `20261112_P02-Fixed-Broadband-Margins.csv`;
  - `20261112_P02-Capture-V3-Newsprint-1440.png`, `20261112_P02-Capture-V3-Newsprint-390.png`.

Modified: none.

Scratch only, in the folder named at the top:
- the chapters 13 to 15 copy;
- the kit builds of 26 specs;
- the probes and their results;
- the width sweep;
- the panel's data copy and probe specs;
- the PDF;
- the captures.
