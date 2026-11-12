# Round 1 red team: accessibility and the production test

Oath & Action Edition 06, Phase 3, round 1, November 12, 2026. Written by the UX and accessibility lead (`oa-ux-accessibility-lead`) as reviewer for `work/handoffs/phase-3/20261112_Phase-3-Round-1-Review-Brief.md`. I then ran a simulated panel. Paths are relative to `oath-and-action-v6-brand-guide/`. I reviewed the strict build at `/tmp/claude-0/-home-user-Dustin-s-Command-Center/256961f5-3911-5bd9-908d-f34ce0435ace/scratchpad/phase-3/round-1-review/build/guide.html` (10,017,051 bytes, 0 warnings) and left it unchanged. My scripts, results and captures are in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/256961f5-3911-5bd9-908d-f34ce0435ace/scratchpad/phase-3/round-1-review/access-production/`. The panel's files are in `work/handoffs/phase-3/round-1-production-test/`.

Under shared memory, the full 10 MB page crashed Chromium during the forced colors and capture passes. For those passes I used a copy of the build that keeps only chapters 14 and 15, with the same shell, kit, tokens and fonts. I made it by loading the build with scripts off, removing the other chapter sections and saving the page (`guide-ch14-15.html` in the scratch folder, 2,416,933 bytes). I ran the scripts-off and width checks on the full page.

## 1. Score

**4 of 5.** Every new specimen's reading path holds: scripts off, tables, keyboard, the lookup, reflow, 200 percent zoom, reduced motion, print and the measured contrast. Round 0's four Must fix items are closed or narrowed. One fault remains for a whole class of readers: in a dark contrast theme, every kit drawing in chapter 14 loses the mark its title names.

## 2. Must fix

**M1. In a dark contrast theme, every kit drawing in chapter 14 paints its named marks white on Newsprint.**
- **Where.** `work/build/chart-kit/kit.css`, the `@media (forced-colors: active)` block (D3-94), meeting `guide-shell.css`'s `.plate-stage { forced-color-adjust: none }` (AX-S6, "a specimen ... keeps its colors when the system forces its own"). It affects all 45 kit figures in chapter 14 (the 26 new specimens, the 10 built ones and the editor's 9 rule plates) and the four sketches 14.24, 14.43, 14.44 and 14.45.
- **What is wrong.** The stage keeps its Newsprint ground (rgb 220, 217, 210), but the kit's block still repaints the drawing in system colors. In a light contrast theme this works. My probe found 0 of 2,007 drawing texts at 1440 px, and 0 of 2,061 at 390 px, in the ink of the paint under them. In a dark theme (Playwright `forcedColors: 'active'` with `colorScheme: 'dark'`, which gives Windows High Contrast Black's colors), CanvasText turns white:
  - All 38 figures that carry a subject mark draw it white on Newsprint, at **1.41 to 1**. In S17, the 118th Congress's column, the one the title names, reads as an empty slot. In S21, the named row's stem and dot almost vanish, while the other 15 rows turn bright green (GrayText).
  - The four sketches drop to the same 1.41 to 1.
  - 1,786 drawing labels turn white with a 3 px black halo, so they read as outlined type on a light ground.
  - The figure's own HTML words stay Charcoal on Newsprint, because the stage keeps them.
  - Chapter 15's plates carry no forced-colors rules, so they keep their colors in both themes as AX-S6 intends. Chapter 14's drawings are the only pieces that split.
- **Rules broken.** WCAG 1.4.11 (the named mark falls under 3 to 1) and Master Brief section 22's forced-colors requirement, for readers who choose a dark contrast theme, a common setting for low vision.
- **Fix.** Make the drawing and its ground agree in forced colors. One rule in the kit's forced-colors block does it in any host page: `.oac-svg { background-color: Canvas }`. The system inks then always sit on the system ground. The other way is to exclude a drawing inside `.plate-stage` from the kit's block, so the specimen shows its true colors, as chapter 15's plates already do. I recommend the Canvas ground, because it also covers the atlas site and plain pages, where no stage keeps a ground. Then add the dark scheme to the kit's forced-colors check, and run it on chapter 13's kit plates too, which use the same CSS (not measured here).
- **Owner.** Engineer.

## 3. Should fix

**S1. The kit passes a source line that names the wrong period, and fails the true one** (production test 1, `round-1-production-test/20261112_Designer-Log.md`, steps 10 and 11).
- **Where.** `checks.js`'s source check, and `work/build/data/treasury-mts-outlays-by-function.meta.json`.
- **What is wrong.** The designer's chart of fiscal 2016 and 2026 left `source_line` out, as the README says. It printed the sidecar's line, "outlays by function, fiscal 2026", and passed. The true line, "fiscal 2016 and 2026" (`P01-Spec-V6.json`), fails: "the source line differs from ... printed_source_line and its variants ... ask the research lead to add a variant". The misleading path passes, and the honest one waits on another person. This breaks Rule 13.6 and H04 by default. Round 0's S7 named the slow path; this is the harm it causes.
- **Fix.** The check reads the years and periods a source line names against the years the spec draws, and fails a mismatch. The research lead gives each multi-year file a variant template for any span (for example "fiscal {from} and {to}"), which the check accepts once the kit fills it.
- **Owner.** Engineer (check), research lead (variants).

**S2. The dumbbell hides most of a chart's changes and leaves no room at its ends on phones** (production test 1, steps 5 to 9).
- **Where.** `forms/dumbbell.js`; the entry for Rule 14.19.
- **What is wrong.**
  - On one dollar scale, 12 of the 19 rows draw the 2016 dot under or against the 2026 dot. Examples: Transportation 92.9 to 142.9, Justice 57.1 to 109.9, Agriculture 20.2 to 52.6. No check reports it.
  - The phone layout keeps no room for a value printed at either end of the scale. "1,667.1" ran past the right edge and "−155.0" past the left at 358, 296 and 256 px. The designer passed the check only by padding `labels.domain` 37 percent past the data, which left a quarter of the 1440 px plot empty.
  - The form's header says "domain ([lo, hi])" without its unit. The designer first gave billions and got labels at x = 21,779,159,435.
- **Fix.**
  - The form reserves its end labels' width at every width, and its header says the domain is in the data's unit.
  - The kit's check flags two marks of one row drawn closer than their radius.
  - Rule 14.19's "Use instead" gains a line for items of very different size, pointing to Rule 14.26 with a percent change or to two panels.
- **Owner.** Engineer (form and check), maker A (the entry's words).

**S3. A screen reader hears each chart's description twice.**
- **Where.** `work/build/scripts/phase-2/guide_build.py`, which wraps each kit figure in `.plate-stage`; `kit.js` `K.mount`.
- **What is wrong.** Chromium's tree for S17, S38 and S42 shows the same alt text twice:
  - as the stage group's description (`aria-describedby="s-14-s17--alt"`);
  - as the drawing's name (`aria-labelledby="oac-s-14-s17-alt"`).
  
  The kit fixed this inside the figure (round 0's S1). The guide's stage adds the description back. Every stage is also named "..., interactive specimen", including static charts such as S17.
- **Fix.** When a stage holds a kit figure, leave out the stage's `aria-describedby`, since the drawing carries the alt. Name such a stage "specimen" unless it holds a control besides the table's disclosure.
- **Owner.** Engineer.

**S4. Printing leaves five chart titles alone on a page.**
- **Where.** `kit.css`'s print block (`.oac-art { break-inside: avoid }` with `.oac-title, .oac-measure { break-after: avoid }`).
- **What is wrong.** In Chromium's PDF of chapters 14 and 15 (238 Letter pages), the following pages print only a title, a grade line and a measure line. Each is 88 to 91 percent blank, and the drawing starts on the next page:
  - page 61, S19;
  - page 146, S15;
  - page 152, S36;
  - page 164, S37;
  - page 175, S39.
  
  Nothing is lost. Every row, note and source line is in the PDF's text layer, and S37's drawing breaks across pages 165 and 166 with no row missing. This closes round 0's M4, but a reader on paper meets a title with no chart under it.
- **Fix.** Let a drawing taller than the space left on the page break (`break-inside: auto` on `.oac-art` when it is taller than a page). Or move the title block with it, by giving the head and drawing a wrapper that avoids a break only when it fits.
- **Owner.** Engineer.

**S5. At 320 px, chapter 15's plates make a reader scroll sideways to read prose.**
- **Where.** All 25 plates in chapter 15. Each stage is fixed at 328 px (`width_px` in `manifest-systems-graphics.json`).
- **What is wrong.** At 320 px, which matches 1280 px at 400 percent zoom, the column is 288 px, so every plate scrolls 40 px sideways. The frames have a tab stop and a hint. The drawings fall under WCAG 1.4.10's exception for diagrams, but the step lists and sentences inside the stage ("Each step, and the weakest", the quotations, the source) do not. They fit at 360 and 390 px.
- **Fix.** Let each stage shrink to the column below 328 px, or set the plate's prose outside the fixed drawing.
- **Owner.** Systems designer, with the engineer for the stage.

**S6. Blank table cells that a screen reader announces as "blank", with no word for what they mean.**
- **Where.**
  - S37 (`specs/s37.json`): 424 of 550 cells blank. They mean the atlas names no such route for that reform, a meaning given only in the measure line above the drawing.
  - S25 (`specs/s25.json`): two "Change, percent" cells blank, for agencies that had no employees in January 2022.
- **What is wrong.** The table notes say what the tints mean, not what a blank means. This narrows round 0's S4. A8 made the absent cells bare to save bytes, which is fine as long as the table says what a blank means.
- **Fix.**
  - S37: add one sentence to the table's notes: "A blank cell is a route the atlas does not name for that reform." It adds no bytes per cell.
  - S25: use the column's `empty` key: "Not defined: none in January 2022".
- **Owner.** Maker A (S37), maker B (S25), with the editor for the words.

**S7. The lookup's chips put a check mark in their names, and Escape leaves the filter sheet open.**
- **Where.** `kit.css` `.oac-lk-chip[aria-pressed="true"]::before { content: "\2713" }`; `kit.js` `K.lookup`.
- **What is wrong.**
  - Chromium names the pressed chip "✓ Well supported", so a screen reader says "check mark" before a state `aria-pressed` already gives.
  - Escape clears the search, but with focus on a chip it leaves the sheet open (`hidden` false).
- **Fix.**
  - Set the mark as `content: "\2713" / ""` so it takes no name.
  - Escape inside the sheet closes it and returns focus to Filters, as chapter 18's filter bar does. Check Rule 18.16's keys and match them.
- **Owner.** Engineer.

**S8. A designer working from the kit meets a stale README and no word on dollars across years** (production test 1, steps 2 and 3).
- **Where.** `work/build/chart-kit/README.md`; chapter 14.
- **What is wrong.**
  - The README still says "19 forms in 17 files" and "The specs for S01 to S16", and its starter table lists only round 0's forms.
  - No rule or entry says whether to adjust dollars for inflation across years. The designer found "not adjusted for inflation" by example in S27's and S33's measure lines.
- **Fix.**
  - Bring the README's table up to the 42 specs.
  - Add one sentence, where the editor places it, for amounts across years: name "not adjusted for inflation" in the measure line, or adjust and name the index.
- **Owner.** Engineer (README), editor (the sentence).

**S9. Terms used bare on plates a reader may reach by a link** (production test 2, `round-1-production-test/20261112_Reader-Log.md`).
- **Where.**
  - S20: "householder", and "margin of error" with no gloss.
  - S31: "FRED" bare in the grade line; it is named in full only in the source line.
  - S37: "Article V" and "routes"; also "Estimate" over a judgment.
  - Rule 15.3: "variables".
  - Rule 15.13's plate: "money, raises" on each step, where "money" names the kind of connection, not an amount. The line code's ticks are not explained on the plate.
- **What is wrong.** The simulated reader stopped at one word on each of the five.
- **Fix.** Gloss each at first use on the plate or entry, in one clause.
- **Owner.** The editor for chapter 14's words (the makers apply them to the specs); the systems designer for chapter 15's plates.

**S10. In forced colors, a drawing made for Charcoal shows the red point close to its gray bars.**
- **Where.** `kit.js` `K.FC` (`point: 'Highlight'`, `context: 'GrayText'`). This affects the kit's own pages and any dark-mode page (DR-204), not the guide, whose drawings are made for Newsprint.
- **What is wrong.** In a scratch copy of S17 with the 118th Congress as the point, the Charcoal drawing in forced colors sets the point in Highlight against the other bars in GrayText:
  - 1.36 to 1 in the light theme (purple against dark red);
  - 1.02 to 1 in the dark theme (cyan against green), so only hue tells them apart.
  
  The Newsprint drawing keeps them clearly apart: its other bars use the light fill, which maps to Canvas with an outline.
- **Fix.** Map `context` to Canvas with a CanvasText outline when a chart names a point or a bar, as `light-fill` does.
- **Owner.** Engineer.

## 4. Questions for Dustin

None. M1's choice between a Canvas ground and true colors inside a stage is a routine call for the engineer. I recommend the Canvas ground.

## 5. Tested

**The red point after A11 (D3-453), as the task asked.**
- **Setup.** No live spec sets `labels.point`, so S17 and S03 as built carry no red point. I built scratch copies with the kit: S17P, with the 118th Congress as the point, and S03P, with its parts removed and Court ruling as the point. Both use `oa-chart.mjs build --out` into scratch, and both PASS with 0 faults.
- **Normal and print emulation.** Identical. The point is filled rgb(230, 57, 70):
  - on Newsprint, with its 1 px Charcoal keyline (red on Newsprint 2.96 to 1, keyline 13.29 to 1);
  - on Charcoal, with no keyline (4.49 to 1).
  
  The A11 fix holds: the point is filled, not hollow, on both forms.
- **The Letter PDF of S17P.** The red point and keyline print on white paper. The Charcoal half of the kit page loses its ground in print: its drawing's value and category labels print pale on white, and its HTML title prints mid gray. This matters only for kit pages and dark-mode pages.
- **Forced colors.** The point takes Highlight:
  - light theme: rgba(5, 0, 73, 0.8), CanvasText keyline on the Newsprint drawing;
  - dark theme: rgba(0, 230, 255, 0.8).
  
  On the Newsprint drawing it stands clear of the light-fill bars, which become Canvas with an outline. On the Charcoal drawing see S10. Inside a guide stage in a dark theme, M1 applies.
- **Captures.** Kit pages at 1440 and 390 px, in all four modes, were looked at as a contact sheet.

**Scripts off**, on the full page at 1440 px, for all 45 kit figures in chapter 14:
- Each figure shows its title (S42 by design prints the sentence instead), its alt as words, the scripts-off line, its source line and an open table.
- `scope` is on every header cell; captions are present.
- Rows equal an independent count from the raw data with each spec's `where` and pivot, by my own script, for all 36 specs (S17 to S42 and the ten built ones). There are 0 differences.
- Blank cells were counted per table.
- S38 hides its controls and shows all 17 rows.
- Chapter 15's 25 plates show their drawings and words with scripts off, and hold no controls.

**Widths**, on the full page, with scripts on and every figure drawn:
- Widths: 1440, 1024 and 390 px; 360 and 320 px; 720 px at device scale 2 for 200 percent zoom.
- Every figure drew, with 0 layout guard faults (`data-oa-warnings`), 0 page errors and no page-level sideways scroll.
- The smallest rendered drawing text is 13 px (12.99 at 723 px).
- Every table frame that scrolls has its tab stop: 21 frames at 390 px and 25 at 320 px.
- Chapter 15's plates fit at 360 px and wider, and scroll at 320 px (S5).
- Round 0's M2 is closed.

**Forced colors**, on the reduced page:
- Chromium's light emulation, at 1440 and 390 px: a geometry probe of every drawing text against the topmost paint under its center, plus captures of all 45 figures. I looked at the 26 new specimens as contact sheets: 0 texts in their ground's ink, and every mark kept apart. S37's middle tints keep their words through the halo. Round 0's M1 is closed for light themes.
- Dark emulation, at 1440 px: the same probe, plus a measure of every subject mark against its stage (M1), and the four sketches.
- Chapter 15's opener and the plates for 15.6 and 15.13, plus S38's controls, captured in both themes.

**Keyboard and names, S38's lookup**, in the guide at 1440 and 390 px:
- A Tab walk visits the search field, Filters, the table's disclosure, then the table frame (390 px only), then the links after the entry.
- Typing narrows the rows ("court": 1 of 17), and the status line is `role="status"`.
- Escape clears the search and keeps focus in the field. A search with no match prints the none words.
- Clear the search returns focus to the field.
- Enter opens the sheet (`aria-expanded` true), and Space presses a chip ("Filters, 1 on", 8 of 17).
- The searchbox is described by the count. Chromium's tree names every control (see S7 for the chip names).
- Every control is 45 px tall.
- The focus ring measures 3.37 to 1 on Newsprint (Verdigris) and 13.29 to 1 on Charcoal (Newsprint), on the kit page.
- No fixed element covered a focused control.

**axe-core** (`work/build/node_modules/axe-core`, WCAG 2.0 to 2.2 A and AA tags), at 1440 and 390 px:
- Scope: `#data-visualization` and `#systems-graphics`, with every table open and S38's filter sheet open.
- Result: 0 violations. "Color contrast" was left incomplete on 3,333 and 5,199 nodes, which is text over drawings and stages; I measured those myself (below).

**References and tree:**
- Every `aria-labelledby`, `aria-describedby` and `aria-controls` in chapters 14 and 15 points to an element that exists (round 0's M3 is closed).
- I read Chromium's tree (`Accessibility.getPartialAXTree`) for the stages and drawings of S17, S38 and S42 (S3).

**Reduced motion** (`reducedMotion: 'reduce'`): 0 transitions and 0 animations on any element in chapters 14 and 15, and no smooth scrolling. Running animations: 0 at every width.

**Print:**
- The reduced page's chapters 14 and 15 to a Letter PDF in Chromium with print media: 238 pages.
- `beforeprint` fired, drew all 45 figures and opened all 45 tables.
- I read the text layer for every table's last rows and for the 83 source lines.
- The 28 "do not publish" bars print, with their words in the text layer.
- I counted pages by blank area: 25 pages with over half left blank. Five are titles stranded from their charts (S4); the rest end a rule.
- I looked at contact sheets of all pages, and at S37's pages 164 to 169 at 40 and 80 dpi.

**Contrast by the WCAG 2.2 formula:**
- From `tokens.css` alone: 53 pairs, 27 on Newsprint and 26 on Charcoal, by my own script (`token_pairs.py`). These are the chart roles the round 1 forms use, the sequential and diverging steps, the group inks, the focus ring, the field and the borders.
- In the rendered guide: 56 text and paint pairs across S17 to S42 (11 distinct colors), and 67 mark and ground pairs.
- Every drawing text clears 4.5 to 1. The lowest is 5.20, white on S37's fourth tint, and S37's darker words on its third tint measure 5.41.
- Marks under 3 to 1 all print their value or word on or beside them: the light fill 1.81 (S17, S23, S36), S25's bars 2.15 and 1.66, and S37's first two tints 1.70 and 2.46. Under that reading of WCAG 1.4.11, none is a fault. Gridlines, bands and tracks are context.
- The two sources agree where they meet (for example 13.29, 5.49, 3.37, 2.46, 1.81).

**Alt text:** I read all 26 new specimens' alt, title and caption. Each says what a sighted reader learns, with the figures that carry the title. I also read four of chapter 15's alts.

**Production test 1 (simulated designer):**
- Six spec versions were checked with `oa-chart.mjs check`. V5 was built with `--out` into scratch and passed. V6 failed on its true source line.
- Its exports and captures were looked at, and its numbers were checked by script against the data.

**Production test 2 (simulated reader):** five pieces were read from the entry files, specs and chapter 15's file, and the 15.13 plate was looked at as rendered.

## 6. Not tested

- Real screen readers (VoiceOver, TalkBack, NVDA, JAWS) and real devices. Chromium's tree and axe-core stand in for them.
- Real people in either panel. Both panels are simulated and untested with real people (DR-202).
- Windows' own contrast themes. I used Playwright's emulation, whose light and dark colors match High Contrast White and High Contrast Black.
- Chapter 13's kit plates in a dark contrast theme. They use the same CSS as M1, but I did not measure them.
- Browser text zoom alone and user text spacing (WCAG 1.4.12). I tested 200 percent as page zoom.
- Paper. No page was printed; I read only Chromium's PDF.
- The full four-width guide check and the whole page under axe. The main session is running both.
- The kit's `dataviz_check.js` on its build pages, the four sketches beyond forced colors, the 360 px keyboard walk, and color-vision simulations.
- The full page in the forced colors and print passes. I used the chapters 14 and 15 copy described at the top.

## Change log

Created:
- this report;
- `work/handoffs/phase-3/round-1-production-test/` and in it:
  - `20261112_Designer-Log.md`;
  - `20261112_Reader-Log.md`;
  - `20261112_P01-Spec-V1.json` to `20261112_P01-Spec-V6.json`;
  - `20261112_P01-Check-V5.json`;
  - `20261112_P01-Dumbbell-Newsprint-1440.svg`;
  - `20261112_P01-Dumbbell.csv`;
  - `20261112_P01-Capture-V5-Newsprint-1440.png`;
  - `20261112_P01-Capture-V5-Newsprint-390.png`.

Modified: none.

Scratch only: the reduced page, the audit scripts, the results JSON, the kit builds of S17P, S03P, S38 and P01, the PDFs and the captures, in the scratch folder named at the top.
