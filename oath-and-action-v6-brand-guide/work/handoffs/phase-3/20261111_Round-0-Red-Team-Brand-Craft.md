# Round 0 red team: nonpartisanship, brand and craft

Oath & Action Edition 06, Phase 3, round 0, November 11, 2026. Reviewer: the design director as reviewer, not maker (`oa-design-director.md`), with the creative director's brand knowledge (`oa-creative-director.md`), for `work/handoffs/phase-3/20261111_Phase-3-Round-0-Review-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

The review runs in two parts. Part 1 covers chapter 13 beside chapters 01 to 12, and the palette proofs with their proposal. Part 2 covers the kit's S01 to S16 once they are final.

## Part 1

Reviewed: `work/build/guide/chapters/13-evidence.json`, the 27 plates `s-13-*`, `manifest-evidence.json` and the editor's notes; the review build's `#evidence` at 1440 and 390 px; `work/handoffs/phase-3/20261111_Palette-Proposal.json`, the palette notes and the proof sheet's captures in `work/boards/phase-3/round-0/palettes/`.

### Score for this lens: 3 of 5

Chapter 13 takes the built chapters' form and red discipline, its words are careful, and the palettes keep to the four inks and pair B, but three faults stand between it and board 1: a direction label on Rule 13.11's plate that reads as partisan, correct plates that print a grade word Rule 13.3 forbids, and line measurements stated one way in Rule 13.4 and another in the proposed tokens.

### Must fix

**M1. Rule 13.11's correct plate groups the campaign finance rulings under an unattributed effect label.** Owner: Editor.
- Where: `s-13-11-correct`, Loop R1's repair log rows.
- What is wrong: the plate sorts the seven rows under two headings, "TOWARD VOTERS" (New York City's Local Law 8 and Charter Question 1, Seattle's Democracy Vouchers levy, Alaska's Ballot Measure 1) and "AWAY FROM VOTERS" (Citizens United v. FEC, McCutcheon v. FEC, NRSC v. FEC). The words are the atlas's own, and the plate keeps every row, which is right under DR-93. The atlas's note that the direction "describes the rule's effect on who officials answer to and carries no judgment of the people or parties involved" sits at the foot, after the reader has met the headings. Read from the right, the brand's own guide files three Supreme Court rulings under "away from voters" as if that were part of the record. It also cuts against the rule the plate teaches. Rule 13.11 says an event "takes no arrowhead, no line pattern and no sign", and its failure plate faults Citizens United drawn as an arrow with a plus sign, yet the correct plate gives the same ruling a direction of effect in words, with no grade and no attribution.
- Fix: keep all seven rows and their order. Move the coding note to the top of the events list and make each heading the atlas's: "The atlas codes these rows toward voters" and "The atlas codes these rows away from voters". Add one sentence to Rule 13.11's rule and a line to its Specifications: a row's direction is the atlas's assessment of the rule's effect, printed in the atlas's words with the atlas named, and it stays apart from the event's date, place and text.

**M2. Three correct plates print "Official statistic" where Rule 13.3 requires a grade word.** Owner: Editor.
- Where: `s-13-1-correct` (the Finding head, "Official statistic: a Census Bureau survey"), `s-13-6-correct` ("Official statistic: a Bureau of Labor Statistics survey of employers"), `s-13-7-correct` (both heads); the failure plates `s-13-6-failure` and `s-13-7-failure` carry it too.
- What is wrong: Rule 13.1 says "The grade follows the label in words on the same line", and Rule 13.3 prints "one display word for each grade, from the table in this rule". "Official statistic" is in no row of that table, which is the fault Rule 13.3's own failure plate shows with "Strong". The kit's specs already moved off this lead (D3-25): `work/build/chart-kit/specs/*.json` print "Documented: an official statistic from a Census Bureau survey". So the chapter and the 16 specimens print the same grade line two ways, and the chapter's correct plates are the ones that break its rule.
- Fix: lead each Finding head with the grade word and its gloss source, as the kit does: "Documented: an official statistic from a Census Bureau survey" and "Documented: an official statistic from a Bureau of Labor Statistics survey of employers". In the failure plates, keep only the fault each one teaches.

**M3. Rule 13.4's measurements disagree with the proposed grade tokens.** Owners: Editor and Data visualization lead, together.
- Where: Rule 13.4's rule text and Specifications in `13-evidence.json`; `oa.chart.grade.minRun`, `oa.chart.grade.conceptual.rail` and `.gap` in `20261111_Palette-Proposal.json`; the proof sheet's grade line code section.
- What is wrong: Rule 13.4 says "Every graded line runs at least 48 px, long enough to show its pattern twice" and "Shortest line: 48 px, two full cycles of the pattern". The token says "The shortest run that may carry a texture: 28 line widths, 56 px on a 2 px line. A shorter step prints its grade in words beside it", and the sheet says three dash-dot periods. Rule 13.4 draws the hollow line as "A 5 px line in ink with a 2 px line of the page's color down its middle", which gives 1.5 px rails on half pixels; the tokens give 1 px rails with a gap of one line width. Both go to board 1, chapters 14 and 15 will draw from the tokens, and a builder reading chapter 13 gets other numbers.
- Fix: agree one set of values, keep them in the tokens as the one source, and have Rule 13.4 cite the token names with the values the tokens hold (56 px at 2 px and the 1 px rails, or whatever the two owners settle). Redraw 13.4's and 13.3's glyphs from those values.

### Should fix, chapter 13

**S1. The opener's first screen has three craft faults.** Owner: Editor. In `s-13-opener` at 1440 px, the line after the chip "Variable E1" starts with a comma (", policy advantages for wealthy and organized interests"); keep each chip and the punctuation after it in one no-wrap span. The two delay ticks sit on the dashed line where a dash runs between them, so at 1x the start of the line reads as the letters "-H" (the same happens on Connection L02 in `s-13-11-correct`); start the dash pattern after the tick zone, on a solid lead-in, as the atlas's `wire_marks` is meant to. The panel "What each part carries" lists six numbered parts, but nothing on the record marks where each part is; set a small numeral at each of the six places (the verb, the grade word, the line, the ticks, the chip, the date) so the list points at the drawing.

**S2. Rule 13.3's mapping table has staggered rules.** Owner: Editor. In `s-13-3-correct` at 1440 px, the last column's cells are `display:flex`, so they leave the table layout and their bottom hairlines float above the row's hairline in the Well supported, Plausible, Contested and Hypothesis rows (seen at 2x). Put the flex on an inner span and leave the cell a table cell. The column's line glyphs carry 32 to 36 px of line, under the 48 px Rule 13.4 sets for every graded line; lengthen them to the agreed minimum (M3) or say in the rule that a key glyph is exempt.

**S3. The chapter's line glyphs drift from Rule 10.10.** Owner: Editor, with the engineer if `wire_marks` needs exposing. The generator draws its own glyphs. Its delay ticks are 1.5 px strokes on whole-pixel x positions (`M13 3V13`), so at 1x each tick lands across a pixel boundary and blurs; Rule 10.10's plate draws them at 2 px. The opener names "Sign +" in words but draws no sign tag, and Rule 13.4's Loop R10 draws Connections L25 and L53, both minus in the atlas, with no sign at all. Draw from the atlas build's function and the grade tokens, as Rule 13.4's own "For builders" note asks, and either draw Rule 10.10's sign tags or say in the caption that signs are left out so the grade stands alone.

**S4. Rule 13.5 shows where Reform R-30 acts without Rule 12.5's red target.** Owner: Editor. `s-13-5-correct` heads its last row "Delay: where it acts, and how long that takes" and draws Connection L39 as a plain 2 px ink line. Rule 12.5 says "Where a figure shows a reform at work, only the marks it acts on turn Pillar Red, at a heavier weight", at 4 px with a 1 px Charcoal edge on Newsprint and a note naming the reform. Draw it that way. It would also be the chapter's one working red, which today it never uses.

**S5. Rule 13.7 teaches one window with no chart to see it on.** Owner: Editor, with the kit. The correct plate shows two chart heads and the failure "a chart beside it starts in another year", but neither draws a plot, so the window shows only in the measure lines. Draw the two charts small from the kit on the shared 2009 to 2025 axis, and the failure's chart from 2017. Then add the sidecar's own qualification, which the printed lines drop: "A change between two years is a descriptive change, not the effect of one policy." The years the earlier release holds (2020, 2021 and 2024) are the expanded child tax credit's year and the years either side, and the failure title ("fell from 9.7 percent in 2020 to 5.2 percent in 2021, then rose to 13.5 percent in 2024") reads to many readers as a policy story; the qualification keeps the plate to its lesson.

**S6. A studio word in a reader's specification.** Owner: Editor. Rule 13.8's Specifications say "Illustrative, in the shell's label". Write "in the label style" and name the token.

**S7. No plate carries the "True size" line.** Owner: Editor. Every chapter from 01 to 12 prints "True size, N px wide" in its plate heads (12 to 64 per chapter); chapter 13 prints none, since `manifest-evidence.json` sets `width_px` to null for all 27 plates. The story cards in 13.8 and 13.13 are 360 px pieces; give those plates their width so the head says so.

**S8. Rule statements run long in the lede face.** Owner: Editor. Chapter 13's rule statements average 795 characters, against 160 to 690 in chapters 01 to 12. Rule 13.5 runs 1,163 characters, about 24 lines of 22 px type at 1440 px and 33 lines at 390 px, and 13.1 (953), 13.6 (872) and 13.10 (850) follow. Keep each rule to what a builder must do and the terms it must define (H02), and move the rest, such as 13.5's tick counts and 13.6's three kinds of source, into Specifications, where they already partly repeat.

**S9. Related chapters run in no order.** Owner: Editor. Rule 13.1 lists 14, 15, 02 and Rule 13.13 lists 26, 05, 20, 24, where chapters 11 and 12 list theirs in ascending order. Sort them.

### Should fix, palette proofs

**P1. One categorical proof gives one color two meanings.** Owner: Data visualization lead. The panel "Four groups on a line chart, and in one bar" uses Verdigris for Manufacturing on the line and for Professional and business services in the bar under it, and the Stone group for Information on the line and All other sectors in the bar. A reader takes a color in one panel to mean one group. Draw the same four groups in both charts, or split them into two panels.

**P2. The categorical bar uses a legend, and its first two groups merge in gray and in one ink.** Owner: Data visualization lead. The proposal's rule says "every group carries a direct label", but the bar names its groups in a legend above it. In the grayscale capture the Charcoal and Prussian swatches and segments print near alike (Rec. 709 luma about 18 and 45), and the sheet's own "Black only" row prints them at 99 and 97 percent screen. Name each segment on the bar. Consider also ordering a stacked form so the two darkest inks never sit side by side (for instance Charcoal, Verdigris, Prussian, Stone), and show that order on the sheet.

**P3. The Hypothesis gloss is stated two ways.** Owner: Data visualization lead. The tokens and the sheet gloss Hypothesis as "untested"; Rules 12.6 and 13.3 print "not yet tested". Use the guide's wording in `oa.chart.grade.hypothesis`, and keep the editor's V7.1 note on the atlas's separate "not yet tested" label in view.

**P4. At 390 px the sheet clips what Dustin needs to judge.** Owner: Data visualization lead. In `20261111_Palette-Proofs-Page-390.png` the one-group-in-ink chart shows its values with the sector names past the frame's right edge, and the small multiples show one and a half panels per row. The frames scroll, but board 1 shows both widths; draw the phone form the kit will use, with names wrapped under values or one panel per row.

**P5. The red point disappears in gray print.** Owner: Data visualization lead, for the creative director to weigh. The sheet says it: the red bar and the Stone bars print at 0.371 and 0.386, so in black-and-white print only a 1 px keyline and the bold label mark the point. Proof one variant with the unmarked bars in the lighter context step (`stoneN55`, which the ghost role already uses) and show both, so the choice is made on sight.

### Questions for Dustin

**Q1. Does DR-124 govern a chapter's teaching examples as it governs chart sets?** Read as a set from the right, chapter 13's real examples lean one way. Seven show public programs or rules that work (Social Security lifting 28.8 million people out of poverty, automatic benefits that cushion shocks, the Medicare insulin cap under the Inflation Reduction Act, federal vehicle safety standards, public services and trust, child poverty under a measure that counts benefits, twice). Four show private money or market power doing harm (Connection L02 in the opener and in 13.6, Loop R1 in 13.9 and 13.11, employer concentration and wages). None shows a program or rule that fell short. Each title is accurate and fairly worded, the domain count passes Rule 01.9, and the failure plates hold claims readers on the left would like to the same standard. Recommendation: treat teaching examples as DR-124 treats chart sets, so nothing is added or swapped to even the score; fix M1, which is the one plate where the words themselves invite a partisan reading; and let the editor's next pick, wherever a plate is redrawn for another reason, come from the evidence that teaches the rule best, read from both sides.

### Tested

- Read in full: `CLAUDE.md`, both role files, the review brief and every file its "Read first" list names (the round 0 brief; the proposal's sections 1, 3 and 7; Master Brief sections 3, 6 to 15, 18 and 22; the decision log from DR-225 to the end and DR-44 to DR-72, DR-93, DR-97, DR-98, DR-100, DR-124, DR-151, DR-204, DR-222 and DR-223; chapter 02's writing rules), the editor's notes and the palette notes.
- Read every rule's text, Specifications, captions, "For builders" notes and sources in `13-evidence.json`, and every plate's words and alt text from the 27 plate files and the manifest, by script.
- Captured the review build's `#evidence` with Playwright in Chromium: at 1440 px, 1x, in 37 parts, every part looked at; at 390 px, 1x, in 43 parts, every part looked at on contact sheets; and every one of the 27 plates as an element capture at 2x at both 1440 and 390 px, of which I looked at the opener, 13.1, 13.3, 13.8 (correct and failure side by side) and 13.11 closely.
- Measured in the rendered page at 1440 and 390 px, inside `#evidence`: every font size and weight used in the plates (13 px the smallest, all on the scale); computed Pillar Red on any element (none); tabular figures in Rule 13.7's table (present); each line glyph's drawn size; the table cells' display in Rule 13.3 (the last column `flex`, confirmed at 1440); punctuation at the start of a line (one, in the opener at 1440); the story card's type sizes in 13.8's correct and failure plates.
- Compared chapter 13 with chapters 11 and 12 on screen at 1440 px (their openers and first rules), and with chapters 01 to 12 by script on the page: "True size" heads, "Fails Rule" captions, the do-not-publish bar, the opener, related-chapter order and rule statement length. All 13 failure plates carry "Fails Rule 13.N." and the bar.
- Compared the generator's glyph geometry with Rule 10.10's plate (`s-10-10-correct`) and with the proposed grade tokens.
- Read every title, note, example and source line in chapter 13 from the left and from the right; scanned the chapter's words for party names, side words and color words (none print a party in color or name a side).
- Checked against `work/extract/atlas-v7-data.json` by script: the grade, sign and delay of the 15 connections the plates name, and the repair log's direction vocabulary ("toward voters" and "away from voters", 24 rows each).
- Read the generator's example log (24 entries) by script.
- Read the palette proposal's grade tokens and rules, and looked at the proof captures: Opening, Diverging, Categorical (normal and grayscale), Past four groups, Red on red (normal, with the grayscale panels 1 and 6), Grade line code at 1440 including its twice-size section, Sequential, Magnitude, and the 390 px page in samples. Checked the four inks only (DR-234), pair B (DR-54), one working red per view, no red on Prussian, and the Charcoal steps.

### Not tested

- The protanopia, deuteranopia and tritanopia captures, the diverging grayscale capture, the Prussian section and the separate 2x line code capture; I relied on the sheet's measures for those.
- Any contrast ratio recomputed from the token values (the accessibility lens does this).
- The proof sheet live in a browser, including its view switcher.
- Chapter 13 at 1024 and 360 px, under forced colors, reduced motion, 200 percent text, print or with scripts off, and axe-core.
- The facts and figures behind the examples (the statistics lens does this).
- Every 2x plate capture other than those named above, one by one.
- The kit's specimens S01 to S16, which wait for Part 2.
- My element captures at 2x show the page's sticky header across the top of tall plates; that is the capture method and not the page.
