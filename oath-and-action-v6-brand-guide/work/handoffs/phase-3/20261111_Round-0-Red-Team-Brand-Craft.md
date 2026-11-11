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

## Part 2

Reviewed: the 16 kit specs in `work/build/chart-kit/specs/`; the fresh kit pages (each `sNN/sNN.html` with its captures, grayscale proofs, exports and check file) in the scratch folder `phase-3/round-0-review/kit-pages/`; the board folder `work/boards/phase-3/round-0/specimens/`; the Explainer maker's notes in full and the engineer's notes from the summary to the palette tokens. Phase 2's approved drawings were captured afresh, figure by figure, from the Newsprint view of `work/boards/phase-2/data-viz/01-explainer/20261106_Data-Viz-01-Explainer.html` and `.../stretch/20261106_Data-Viz-Stretch.html` (the pages behind the `captures/` folders), at 1440 px at 1x and 2x and at 390 px, and set beside the kit's drawings. Not reported here because they are already in flight: the engineer's weight pass, the categorical order swap and the line code token values (D3-84).

### Score for this lens: 3 of 5

Eleven of the 16 hold Phase 2's standard or beat it, and the words read fairly from both sides with one exception. But S16's circles are drawn at a third of their size, S09 strikes its labels through, S01's vote bars read as a party chart, and five forms lost drawing detail that carried their titles' claims.

Where the kit beats Phase 2: S11's labels now clear the even line and its reading aid is drawn; S12 and S15 carry the national figure (DR-64); S03 and S08 credit every direction code to the atlas in the title and give the one-standard cases in words (Texas HB 4 and California's Proposition 50 both coded away from voters), which is the treatment Part 1's M1 asks of Rule 13.11; every grade line now opens with the grade word; every source line matches its sidecar; and no disclosure prints.

### Must fix

**K1. S16's circles are scaled to the whole nation, so every state's circle shrinks to a third.** Owner: Engineer.
- Where: S16, `work/build/chart-kit/forms/bubble-map.js`, line 18 (`maxv` over every row).
- What is wrong: the United States row added to `census-cps-2024-turnout-by-state` (ENG-7, 236,138 thousand) sets the size domain, though it draws no circle. California's radius is 16.37 px in the 1440 export, which is exactly 50 × √(25,327 / 236,138); Phase 2 drew it near 43 px. The title is about "the four states with the most citizens 18 and over", and that size is now barely visible: the 1, 5 and 20 million key circles are dots, and on Charcoal the small circles sink into the dark land.
- Fix: take the size domain from the rows that draw a circle (leave out the national row, or any row the map has no shape for). Then recheck S16 at every width and ground.

**K2. At 390 px S16's leader lines cross its labels.** Owner: Engineer.
- Where: S16 Newsprint and Charcoal at 390 px, the Northeast.
- What is wrong: leaders run through PA, MA, NY, VT, CT, TN and DE, and Ohio's leader runs to the frame's right edge. The kit's check passes because its guard tests text against text only.
- Fix: after K1, place the phone labels again (E21's `offsets_phone`, or leaders out to the map's edge that clear every label), and let the guard fail any leader that crosses a text box.

**K3. S09 strikes its own labels and says it shortens names it prints in full.** Owners: Engineer (form), Explainer maker (notes).
- Where: S09 at 1440 and 390 px.
- What is wrong: at 1440 px, leader lines pass through "2013 Nuclear option ...", the asides under "1978 Proposition 13" and "2026 Trump v. Slaughter and Trump v. Cook (NRSC v. FEC, June 30, 2026; inspector general removals, ...; Storch v. Hegseth ruling, ...)". The third note says "Event names are the atlas's, shortened at any parenthesis", but every parenthesis prints, four lines deep. At 390 px the first note describes shaded bands that the phone list does not draw. Phase 2's drawing was clean.
- Fix: land E16's `cut_at: "("` and stop each leader at its label; add a phone note that matches the list. Until then, do not show S09 on board 1, as the Explainer maker advised.

**K4. S01's vote bars read as a party chart about the ban.** Owners: Explainer maker (words), Engineer (E27).
- Where: S01 at both widths and grounds, the section "What Congress did next", and its alt text.
- What is wrong: the title says nearly nine in ten voters in both parties favored a ban. Under it, the votes now split by party (D3-07) with the words "for" and "against" gone (E27 open). So the heavy ink reads "Republican 218" and "Republican 53", and the gray reads "Democratic 198" and "Democratic 45", on both grounds. The labels say only "The House passed H.R. 7008" and "The Senate vote to take it up fell short". The bill's second provision, the photo ID requirement to vote, is in the reading guide but not where the votes are drawn, and the alt text leaves it out. Read from the left, the drawing says Democrats voted against a ban their voters wanted. Each fact is true, but the picture leaves out what the votes were on.
- Fix: name both provisions where the votes are drawn, for example "Votes on H.R. 7008, which pairs a limit on members' stock trading with a photo ID requirement to vote"; print "for" and "against" in each segment ("Republican 218 for", "Democratic 198 against"), so the ink reads as the vote; and name both provisions in the alt text. See Q2.

### Should fix

**KS1. The reading guide sits between the title and the measure line.** Owner: Engineer. In S01, S05, S06, S10 and S15, the kit sets the reading guide right under the title in body ink at 15 px, with the measure line after it in larger gray type. Rule 13.7 defines the measure line as "the line under a chart's title", and Rule 12.6 sets keys "Under the title and measure line". Phase 2 put the reading guide after the measure line (S06's "Up means better", S04's gap line). Order them title, measure line, reading guide, and set the guide no larger than the measure line.

**KS2. S13's two parts lost their drawing.** Owner: Engineer. The totals' sparklines run flat across 570 px, and they lost Phase 2's baselines, peak dot and "Peak: 3,013,000 in October 2024" label. In the panels, the darker area fill hides the gray all-nonfarm line that the key promises "in every panel". Use Phase 2's lighter fill with the context line above it, give the sparklines Phase 2's height and baseline, and mark the federal peak.

**KS3. S05 no longer draws its title's claim.** Owner: Engineer. The gap brackets (E13), the heavier highlight line, the yearly dots and the 2003 tick are gone, so "a wider gap than in 2003" lives only in a note.

**KS4. Short shift arrows draw as a filled diamond.** Owner: Engineer. In S12's tiles and S15's shift column, shifts of 1.0 to 1.8 points (Washington, Utah, Oregon, Oklahoma, Nebraska) draw the tail dot under the arrowhead with no shaft, so they read as a diamond, a shape the atlas's glyphs already use for authority (Rule 10.10). Below a minimum length, draw the head alone, as Phase 2 did, or a minimum shaft.

**KS5. S14's scale and phone label.** Owner: Engineer. The scale runs to +1,000,000 for a largest month of +819,000 (E6), and the "+29,000 jobs" label crowds the top line. At 390 px, "Three-month average" sits on the columns and the line crosses its first letter; Phase 2's phone moved it into a key.

**KS6. S06's cell words are set at tick size in the secondary ink** (E18b), where Phase 2 set them at reading size. They are the atlas's words and the chart's content. Owner: Engineer.

**KS7. S10's rows are 23 px apart against Phase 2's 35**, so the 16 bars read as one block. Owners: Engineer and Explainer maker.

**KS8. Small collisions at 390 px.** Owner: Engineer. In S01, Independent 1's leader runs through "Democratic 13". In S15, the header "Shift toward the Republican nominee" wraps to five lines of one word, flush right.

**KS9. Table headers take two styles.** Owner: Engineer. S03, S07 and S13 head in the tracked caps label style, while S06 and S15 use sentence case at tick size. Pick one style for the kit.

**KS10. S02's annotations.** Owners: Explainer maker and Engineer. At 1440 px the 2025 note leaves "child." alone on its third line. At 390 px the key lists "Official measure" before "Supplemental measure", the line the title is about.

**KS11. S08's ring leader stops short of the ring** (E28), and the ring sits on the stack's top square. Owner: Engineer.

**KS12. The footer lost "How to read our charts"**, which every Phase 2 specimen carried. Owner: Engineer. Print it where the guide has a target for it, or record the call to leave it out.

### Questions for Dustin

**Q2. Should S01 keep both chambers' party splits (D3-07)?** The splits are the record, and DR-93 reports findings as the record shows them. But under a title about voters in both parties favoring a ban, two near party-line votes on a bill that also requires photo ID to vote invite a reading the votes cannot carry. Recommendation: keep the splits with K4's fixes (both provisions named where the votes are drawn, and "for" and "against" in every segment); if the fixes cannot land before board 1, show the totals without the split there.

### Tested

- Read the Explainer maker's notes in full and the engineer's notes from the summary through the palette tokens.
- Dumped every printed word field of the 16 specs by script (title, grade line, reading guide, measure line, notes, source line, alt) and read each from the left and from the right.
- Captured Phase 2's approved Newsprint figures with Playwright at 1440 px (1x and 2x) and 390 px, 48 captures, and set each beside the kit's capture of the same specimen. At 1440 px I looked at all 16 pairs. At 390 px I built all 16 pairs and looked at S01, S02, S04, S05, S06, S09, S11, S12, S13, S14, S15 and S16.
- Looked at the kit's Charcoal captures at 1440 px for S01, S03, S06, S08, S10, S11, S13 and S16.
- Looked at the kit's 2x PNG exports, cropped, for S01 (phone), S08, S09, S12 (phone), S13, S15 and S16 (phone).
- Measured S16's circle radii from its 1440 SVG export and confirmed the national row sets the scale; read the form's code at that line.
- Found, by script, text set flush to the artboard's right edge in S05, S10, S13 and S14. It is inside the drawing and is not reported as a fault.
- Checked the 16 kit drawings by eye for red (none), red with Prussian (none), party colors (none), the national row on state results (S11, S12, S15, and S16 in the key) and the shared window note (S13, S14).

### Not tested

- The kit's 390 px captures beside Phase 2's for S03, S07, S08 and S10, and the Charcoal captures at 390 px.
- The kit's grayscale proofs and the lightness-margin test (the accessibility lens).
- The table equivalents, scripts off, keyboard and the exports' contents.
- The facts behind the specs' words (the statistics lens).
- The engineer's notes past the palette tokens section (contracts, routine calls, requests).
- Phase 2's 2x captures beside the kit's 2x exports for any specimen not named above.
