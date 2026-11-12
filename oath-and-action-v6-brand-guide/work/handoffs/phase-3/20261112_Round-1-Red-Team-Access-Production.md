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

## Second pass

November 12, 2026, under DR-191, after the fix pass.

**What I reviewed.**
- The fix brief, `work/handoffs/phase-3/20261112_Round-1-Fix-Brief.md`.
- The decision log from D3-476 to D3-584.
- The "Review fix pass" sections of the engineer's, makers' and systems designer's notes.
- The fresh strict build, `/tmp/claude-0/-home-user-Dustin-s-Command-Center/256961f5-3911-5bd9-908d-f34ce0435ace/scratchpad/phase-3/round-1-second/build/guide.html` (9,986,588 bytes), which I left unchanged.

**Where I tested.**
- The full build, for scripts off and widths.
- A copy holding chapters 13, 14 and 15, made with scripts off as before, for forced colors, print, keyboard and axe-core (`second/guide-ch13-15.html` in my scratch folder, 2,632,909 bytes).
- My own kit builds of all 42 specs, plus pages for 11 of them, in the scratch folder.

### New score

**4 of 5.** All but one of my eleven items are closed. M1 is closed in both contrast themes. Four new faults hold the score at 4:
- three in the build: S10's source line, S34 at the 390 px column, and Rule 14.9's static plate at 320 px;
- one that has landed in the kit's files since the build: S37's low-step words in forced colors.

### Status of each item

**M1, closed.** In forced colors every kit drawing now sits on Canvas (D3-535). Results:
- Chapters 13 to 15, in light and dark themes: 70 drawings at 1440 px and 59 at 390 px, sketches and phone views included, every one on its own Canvas ground (white, or black in the dark theme).
- Every subject and point mark clears 21 to 1 against it. No data mark falls under 3 to 1.
- No word sits on a solid paint under 4.5 to 1: 2,993 drawing texts at 1440 px and 2,196 at 390 px.
- In captures in the dark theme, S17's 118th Congress is a white column among outlined ones, and S21's named row ends in the Highlight dot.
- The only words not on a solid paint are on hatched steps: S37's "Medium" and "Very low" (73 at 1440 px), and S16's 34 state codes on its kit page. They read through their halo. S37's are legible in my captures; I did not look at S16's.

**S1, closed.**
- The kit now fails the production test's V1, V3 and V5 on their source line ("the source line names 2026, but the chart draws 2016 to 2026 ... such as one of the sidecar's source_line_templates").
- V6's true line ("fiscal 2016 and 2026") passes the source check.
- The outlays sidecar carries `span` and `two_years` templates.

**S2, closed.**
- V1 to V6 now fail the dots check, on 6 to 10 rows per drawing.
- V3's end values fit at every width, with no layout fault.
- The dumbbell's header gives the domain's unit.
- Entry 14.19 sends rows of very different size to Rule 14.26 (D3-579).

**S3, closed.**
- All 36 entry stages in chapter 14 carry no description of their own.
- 35 are named "..., specimen", and S38's alone "..., interactive specimen".

**S4, open.**
- Chromium's PDF of chapters 13 to 15 (295 Letter pages) still prints five titles alone, each page 88 percent blank, with the chart on the next page: S19 (page 109), S15 (198), S36 (209), S37 (223) and S39 (233).
- `beforeprint` marks these drawings `data-oa-tall`, and `kit.css` sets `break-inside: auto` on the drawing box. But the `<svg>` inside is one unbreakable box, and Chromium moves it whole to the next page.
- Nothing is lost: the text layer holds all 126 source lines and the 40 "do not publish" bars.
- Fix: break the tall drawing itself, for example by drawing it as two SVGs at a row boundary for print, or keep the title block with it by moving the title into the same unbreakable wrapper only when the drawing fits a page. Owner: engineer.

**S5, closed.**
- At 320 px each chapter 15 frame still scrolls 8 px sideways (a 328 px stage in a 320 px frame), with its hint and tab stop.
- No word of prose sits past the frame's visible edge on any of the 25 plates. I measured every text node's glyph boxes.
- At 360 px nothing scrolls.

**S6, closed.**
- S37's chart note now says "A blank cell is a route the atlas does not name for that reform."
- S25's two cells print "Not defined: none in January 2022", and its table has no blank cell.

**S7, closed.**
- S38's pressed chip is named "Well supported", with no check mark.
- Escape in the sheet closes it (`hidden`, `aria-expanded` false) and returns focus to Filters.
- The live list now takes the still drawing's place: the still hides, and all 17 rows and "17 of 17 issue records" show.

**S8, closed.**
- The README lists 45 forms and S01 to S42.
- The README explains dollars across years and two values far apart in size.
- Chapter 14 now says "A chart of dollars across years says in its measure line 'not adjusted for inflation', or names the dollars' year and the price index that adjusted them".

**S9, closed.** Each term the simulated reader stopped at is now explained where the reader meets it:
- "householder" and margin of error (S20);
- FRED in the grade line (S31);
- routes, Article V and an estimate given in words (S37);
- variables (Rule 15.3);
- "money, raises" and the ticks, in the "Reading a step" key (Rule 15.13's plate).

**S10, closed.** In forced colors, beside a red point, the context marks of the Charcoal drawing now take Canvas with a CanvasText outline (D3-536). On S21's and S23's kit pages, the point stands at 19.04 to 1 from them in the light theme and 13.76 to 1 in the dark.

### Maker A's flag: words on solid GrayText fills

In the build, I found no word printed on a solid GrayText fill in any form. I checked every kit drawing in chapters 13 to 15 at 1440 and 390 px in both themes. I also checked the kit pages of S01, S06, S07, S08, S10, S12, S15, S16 and S37 on both grounds in both themes. Those pages cover the five specs outside the guide and the forms that set words on tiles, cells and steps. S37 is the one form that sets words on the GrayText step, and in the build its plate holds them at full contrast.

### New faults from the fix pass

**N1. S10 fails the kit's own check.**
- **Where.** `specs/s10.json`.
- **What is wrong.** D3-560 rewrote the claims line in `v7-claims-by-grade.meta.json` ("432 of the 433 claims checked on October 15, 2026"). S10 still sets the old line by hand ("claims checked through October 15, 2026"). It now fails: "the source line differs from v7-claims-by-grade.json's printed_source_line and its variants". `oa-chart.mjs build --all` reports it, and so does the main session's own kit build (`round-1-second/kit-out/s10/s10-check.json`). S10 is not in the guide yet.
- **Fix.** Drop S10's `source_line` so it prints the sidecar's line.
- **Owner.** Maker A, who held S10's words in round 1.

**N2. S34's phone row runs past its drawing in the 390 px guide column.**
- **Where.** `specs/s34.json`, `forms/bubble-timeline.js`.
- **What is wrong.** At a 390 px window the guide gives the chart 326 px. The kit's own draw there reports "text outside the artboard: '295 through November 10, 2026' at 102 (226.3 wide; artboard 326)", 2 px past the edge. The figure carries `data-oa-warnings="1"`. The words came with D3-511. The kit's check draws 358, 296 and 256 px, never 326, so it passed.
- **Fix.** Wrap or shorten the row at that width. Add 326 px, and any other width the shell gives a chart (294, 264 and 224 px at 390, 360 and 320), to the kit's checked widths.
- **Owner.** Maker B (S34), engineer (widths).

**N3. Rule 14.9's new static plate shrinks its words and blocks its table at 320 px.**
- **Where.** `s-14-9-correct`, the figure `s-14-9-dots` made by `oa-chart.mjs figure` (D3-558).
- **What is wrong.** At 320 px, the plate's 256 px phone drawing scales to 224 px, so its words fall to 11.38 px. They hold 13 px at 360 px and wider. Its table frame also scrolls with no tab stop (WCAG 2.1.1; axe's scrollable-region-focusable): the kit wires a frame's tab stop only for figures that carry a data island, and a static figure carries none.
- **Fix.** Wire `K.frame` for static figures too. Give the plate a drawing at 224 px, or let the stage scroll rather than scale.
- **Owner.** Engineer, with the editor for the plate.

**N4. In the kit's files since the build, S37's low-step words turn invisible in forced colors.**
- **Where.** `kit.js` line 474 (`oac-fc-on-gray`, the response to maker A's flag) and `kit.css` line 139, both dated after the build. They meet S37's Canvas plate from D3-568.
- **What is wrong.** `Ctx.text` finds the GrayText cell under each "Low", ignoring the plate, which is `oac-f-none`, and sets the word in Canvas. The word then sits on the plate's Canvas. On kit pages built from the current files, 90 words at 1440 px and 90 at 390 px sit at 1 to 1 against their plate in both themes, readable only through the 3 px halo. At 390 px these include the chips ("Federal statute: Low"). This is the fault D3-568 fixed, back again. The build I reviewed predates the change and is fine.
- **Fix.** Keep one of the two: either `fill_under` reads an `oac-fc-plate` as Canvas, or S37 drops its plates now that words on GrayText take Canvas. The Canvas word on GrayText measures 14 to 1 in the light emulation.
- **Owner.** Engineer, with maker A.

### Tested in the second pass

- **Forced colors, light and dark,** on the chapters 13 to 15 copy at 1440 and 390 px: the geometry probe on every drawing text and data mark, and captures of S17, S21 and S37.
- **Kit pages, forced colors:** S01, S06, S07, S08, S10, S12, S15, S16, S21, S23 and S37 on both grounds, in both themes. S37 was built a second time to read its words' classes. In my first batch, S16 and S37 failed page-to-Node parity; built alone, both passed, and I treat that as a flake under load.
- **The kit's check** on production specs V1, V3, V5 and V6, and `oa-chart.mjs build` of all 42 specs (41 pass; S10 fails, N1).
- **Scripts off,** on the full build: all 49 kit figures. Rows equal my independent count from the raw data for all 36 specs counted. Every header has `scope`. Blank cells remain only in S37 (explained) and in the editor's Rule 14.11 plate (16 empty "Change in the survey" cells for years with no change).
- **Widths 1440, 1024, 390, 360 and 320 px, and 720 px at device scale 2,** on the full build: every figure drew except the static one, which is drawn in the page. There were no page errors and no page-level scroll. The only guard flag was S34 at 390 px (N2). Visible drawing text was 13 px or more everywhere except Rule 14.9's plate at 320 px (N3). Every scrolling kit table frame has its tab stop, except that plate's (N3).
- **Accessibility tree:** Chromium's tree for all 36 entry stages.
- **S38:** by keyboard, its tree snapshot and Escape.
- **Chapter 15 at 320 and 360 px:** stage and frame widths, and text-node glyph boxes against the frame's visible edge.
- **axe-core** on chapters 13 to 15 at 1440 and 390 px, with every table and S38's sheet open: 0 violations. Also checked: no broken ID references, no transitions or animations with reduced motion.
- **Print:** the copy's chapters 13 to 15 to a Letter PDF (295 pages). `beforeprint` opened all 54 tables and drew 53 figures; the 54th is the static figure, already in the page. I counted pages by blank area and read the text layer.

### Not tested in the second pass

- The four-width guide check and axe on the whole page. The main session is running both.
- Paper, real screen readers, real devices and Windows' own contrast themes.
- The chapters outside 13 to 15 in forced colors.
- A capture of S16's hatched words.
- The editor's second pass on the changed words, which is the editor's.

### Change log, second pass

Modified: this report (this section).

Created: none in the repository.

Scratch only: the chapters 13 to 15 copy, the probes, the kit builds and pages, the PDF and the captures, under `/tmp/claude-0/-home-user-Dustin-s-Command-Center/256961f5-3911-5bd9-908d-f34ce0435ace/scratchpad/phase-3/round-1-review/access-production/second/`.
