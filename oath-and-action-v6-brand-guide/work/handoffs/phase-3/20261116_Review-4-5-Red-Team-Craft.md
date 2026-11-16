# Review of rounds 4 and 5, red team: craft at twice size

Oath & Action Edition 06, Phase 3, review of rounds 4 and 5, chat 7, November 16, 2026. Reader: craft at twice size, holding `.claude/agents/oa-design-director.md` as a craft critic who has not seen this work before. Brief: `work/handoffs/phase-3/20261116_Phase-3-Rounds-4-5-Review-Brief.md`. Codes CR. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f55a08bf-cdcf-539d-a683-426e26f4f342/scratchpad/c07/review/craft/`. I edit only this file.

## Status

- 17:09 UTC. First full draft written from the shared captures at Newsprint 1x, 1440 and 390 px, with pixel zooms of the 1440 px captures, the built page's markup and plate CSS, and Node-only kit drawings of S14 and S59. Charcoal, grayscale and the 2x captures had not landed; I add a pass on them below as they land.
- 17:01 UTC. Newsprint 1x at 1440 px read for the selection guide, the palette plate, S96 and its failure, 14.143, 14.144 and 15.19 to 15.25.
- 16:51 UTC. Started. Read the brief whole, my role file, and the round 4 and round 5 design director notes.

## 1. Score

**3.5 of 5.** The new work reads as one calm, well-made system at a desk and on a phone, but one plate prints broken words at a desk (15.22's stage 10), and a run of alignment and consistency faults (a chooser ragged on both edges, two orders for one stepper, columns on two lines in 15.23, blurred lines on the palette reference page) keeps it short of what the best firm would sign.

## 2. Must fix

**CR-M1. Rule 15.22, stage 10: words broken into three columns at a desk.** Where: `s-15-22-correct`, stage 10 "Veto and override", at 1440 px (and every width where the line wraps). The line "Short of two-thirds in either chamber, the bill dies." prints as three side-by-side blocks: "Short / of", "two-thirds", "in either chamber, the / bill dies." The next line prints "With  two-thirds  in each, then stage 13." with wide gaps around the held word. Cause, read in the built page: the plate's CSS sets `.wf .sq{display:flex;gap:8px;align-items:baseline}`, and the line's text runs and its `<span class="nw2">two-thirds</span>` hold (DD-S4's fix) become separate flex items. A scan of every `p.sq` on the page finds these two lines and no others. A reader meets this in the middle of chapter 15's longest plate. Fix: keep the square and the words as two flex items by wrapping the words in one span (`<span class="sqm" aria-hidden="true"></span><span>Short of <span class="nw2">two-thirds</span> in either chamber, the bill dies.</span>`), or set `.sq` as a block with the square as an inline-block or `::before`. Add a check to `phase3_ch15_build.py` that no flex row holds bare text beside an inline span. Owner: systems designer.

## 3. Should fix

**CR-S1. The chooser on Rules 15.20 and 14.144 (DD-R2 and DD-R5, with two more faults found here).** Where: `s-15-20-correct` and `s-14-144-correct`, `.ch1` and the red target CSS. At 1440 px the options shrink to their labels, so their right edges step (14.144: 644, 553 and 587 px), and the chosen option's check mark pushes its chip 28 px right (x 165 against 137), so the three chips start on two lines. The stack is ragged on both edges. The red connection's shaft carries its keyline, but its arrowhead is plain Pillar Red with no edge, which is the 2.96 to 1 red mark on Newsprint my role's check 8 forbids. Fix, one change in the shared CSS, both plates together (R4-5): stretch the options to one width (DD-R2); give every option a fixed 24 px slot for the check so each chip starts at one x; keyline the chosen pill inside its red ring (DD-R5); and keyline the red arrowhead as the shaft is. Owners: systems designer and complex examples maker, the component engineer for the part.

**CR-S2. One look for one effect code (agrees with the main session's call 2).** 15.20 draws a tick and pips before "+L large positive" (Rule 13.5); 14.144 prints "+L local, large positive" with no pips, and sets each family name as a two-line all-caps eyebrow ("EFFECT ON QUALITY OF / DEMOCRACY"), 33 of them across the three cards, heavier than the codes they label. When the pips land, set the family names as 15.20 sets them (sentence case, one line where it fits, secondary ink), so the codes are the strongest marks in each row. Drop the chip repeated at the start of each card's first line ("Reform R-06 turns one connection red." under the heading's own "Reform R-06"). Owner: complex examples maker; the editor for the words.

**CR-S3. 14.144 on a phone: no line-up.** At 390 px the three cards stack, so R-38's effects sit about 2,600 px below R-06's and the rule's comparison rests on memory. DD-R1's phone half (a small table before the cards, families as rows and the three reforms as columns, each code whole with its pips, no total) is still open. Owner: complex examples maker.

**CR-S4. One stepper, two orders.** 14.143 (after DD-C1) sets the drawings, the status line, the buttons, then the steps. 15.19 (round 4) sets the drawing, then the status line and the steps, then the buttons; at 1440 px its drawing ends near y 610 and Play starts near y 950, with the drawing's column empty for about 800 px below it. Give 15.19 14.143's order, and at a desk let 15.19's drawing column stick beside the list (`position: sticky`, top below the masthead) so the drawing that lights stays in view. On a phone, 14.143's first drawing still sits about 1,000 px above Play; say on board 3 whether a sticky control row is wanted. Owners: systems designer and component engineer, with the accessibility lead's yes on focus order.

**CR-S5. 15.22, the top of the spine.** The black spine runs up past stage 1 to meet the gray return line, so the return's gray arrowhead sits on black and its tip stops about 4 px above stage 1's square (3x zoom). End the spine at stage 1, and bring the return into stage 1's top edge in its own ink with 2 px clear. Owner: systems designer.

**CR-S6. 15.22's key mark for a path.** The key says "set to one side on a short arrow" and draws a dash and a square with no arrowhead; the drawing uses an arrow. Draw the key mark as the drawing draws it. Redraw the key with call 1's new stage mark. Owner: systems designer.

**CR-S7. 15.23, two column lines and a ragged name edge.** Route FS's stage column starts at x 322 and the other four blocks' at x 342 (1440 px). The two-digit stage squares (10 to 20) are wider than the single-digit ones, so "Veto and override" starts 5 px right of "Signed". Set one column line for all five blocks, and give each stage square a fixed slot so every name starts at one x. Owner: systems designer.

**CR-S8. 15.21, scales broken across lines.** In a 300 px column the grade ladder runs "Documented, Well supported, Plausible" then "Contested, Hypothesis" on a second row, and the delay classes break the same way, so neither reads as one ordered scale. Set each scale as a short vertical list with the plate's own value marked, or on one line. The drawing's column also stands empty for about 300 px below the two pills. Owner: systems designer.

**CR-S9. S96, the dashed average over the preliminary months.** At a desk the average over August and September 2026 spans about 23 px, and its dash pattern leaves two specks beside the hatched columns (4x zoom), which read as debris, not a line. Use a pattern that starts and ends on ink over that span (as the palette plate's grade lines do), or dots at the two preliminary averages. The form is S14's too (`columns-moving-average`): measure S14 before and after. Owner: complex examples maker, through the engineer.

**CR-S10. 14.142's failure differs by two things.** The failure plate still carries "+29,000 jobs / in September 2026, preliminary" on a leader that runs about 260 px down the drawing's right edge, which the correct plate dropped (DD-E3). A reader comparing the pair sees two differences, and the second is not the fault. Drop the latest label from the failure. Owner: complex examples maker.

**CR-S11. The palette plate's 3 px grade lines blur at 1x.** On the reference page, every 3 px grade line lands across four pixel rows (gray values 117, 18, 18, 117 at 1440 px), so it prints soft beside the crisp 2 px line above it. Center odd widths on the half pixel. Owner: engineer (`palette_spec_build.py`).

**CR-S12. The palette plate's tables are hard to read as a reference.** Token names break at their dots over three lines ("oa.chart.color. / sequential. / fill.step1"), and each ground cell runs four facts as one wrapped run ("3.69 to 1, marks Label in White, 5.20 to 1, text Lightness 0.527"). A designer copying a token or comparing a ratio has to hunt. Set each token name on one line (its own full-width line under the step, smaller mono size), and each ground cell as labeled lines, one fact a line, in tabular figures. Owner: engineer.

**CR-S13. S93, the callouts beside the parts list.** At a desk the page's margin callouts 2, 6, 7, 10 and 11 sit about 20 px left of the list's own discs at the same height, so a reader sees "⑦ ③ Public Law number" and "② ① Running head"; discs 6 and 7 sit 1 px apart. Open the gutter between the sheet's callouts and the list to at least 32 px with a hairline, or start the list in its own column, and part 6 from 7 by 4 px. Owner: infographics maker.

**CR-S14. S94's key, and the year mark (DD-I18).** At a desk the two key entries sit 4 px apart ("Consequence in law □ No consequence stated"); at 390 px the second breaks from its mark ("□ No / consequence stated"). Hold each entry as one unit with 16 px between, stacked on a phone. See named place 1 for DD-I18. Owner: infographics maker.

**CR-S15. S14's latest label against its top gridline (the carried item).** Measured in Node: at drawing widths 488 to 720 px (pages 520 to 1440) the label's second line, "in September 2026, preliminary" at 14 px, sits on a baseline at y 137 with the +750,000 gridline at 141.5, so its descenders end about 1 px above the line and the halo breaks the gridline under them. At the 448 px drawing it sits clear. Raise the label block so its last line clears the gridline by 4 px at every width, in the form. Owner: engineer, with the complex examples maker; the data lead signs, since S14 is board 1's.

**CR-S16. Held phrases still breaking.** "2 to / 10 years" in 14.143's steps (R10 step 3); "2 / U.S.C. 644" and "5 / U.S.C. 706" in 15.22's sources; "size-of- / shift" in the selection guide's "Change lollipop with a size-of-shift key" at 1440 px; "10- / year terms" in S91 at 390 px. Hold "N to N years", "N U.S.C. N" and hyphenated compounds in names. Owners: complex examples maker, systems designer, selection guide maker, infographics maker.

**CR-S17. ID chips print "R - 06".** In every typed chip with a hyphenated ID (Reform R-06, R-30, R-38, R-03, R-04, R-28, R-35), the hyphen sits with a space's width on each side at 1x and 4x, so the ID reads like "R minus 06". The markup holds a plain hyphen in `.chip .id .nw` with `font-variant-numeric: tabular-nums`; I did not trace the spacing's cause. Owner: component engineer (the chip), with the engineer.

**CR-S18. "2 conflict".** 15.25's indicator row prints "2" over "conflict, both in row 42". Say "conflicts". Owner: editor, through the systems designer.

**CR-S19. Two header layouts for the evidence chip.** S89, S91 and S94 set the "FINDING" chip alone with the grade line on the next line; S85 to S88, S90, S92, S93, S95 and S96 set them on one line. Where the grade line will not fit beside the chip, wrap it beside the chip with a hanging indent, so every plate's head keeps one layout. Owner: engineer.

## 4. The named places in my lens

1. **Carried items, my call on each.**
   - DD-R2 with DD-R5 on 15.20 and 14.144: **take both, together, now**, with the check slot and the red arrowhead's keyline (CR-S1). The ragged edges and the jumping chips are faults, not taste. Board 3 shows both plates after.
   - SG-6, the tier word above the name: **take it, with the accessibility lead's yes and the DOM order changed with it.** The guide's own grammar sets an eyebrow above its title (S89's "In place of step 3", S92's "Optional, when the need is urgent", the cards' field labels). Set above the name, the tier sits directly under the picture on one line per row without help, and the uneven gap between a one-line name and its tier (about 25 px under "Sparkline") goes. If the accessibility lead says no, keep it as built: the subgrid already aligns the tiers.
   - 15.24's boxed example: **keep it as built.** It now closes the plate in a 1 px frame after the eleven cards, which reads as one use of the set.
   - S14's label: **move it** (CR-S15), shown on board 3 beside today's drawing, since S14 is approved.
   - DD-I18, S94's year mark: **take it.** The year still draws about 220 px wide in a 720 px column, with 5 to 6 px day marks at 1x where an open square reads as a dot, and April 15's three marks stack in a tower. Drawn at the column's width, with 8 to 10 px marks, the year reads at the plate's scale.
   - The engineer's edge guard (opt-in because S59's "4.1" fails it): **board 3 should show it**, S59 at 390 and 558 px with its label moved, so the guide holds one standard (DD-E7: no line through a label's words, haloed or not); then the guard can go on for every form. I rendered S59 in Node but did not measure its crossing; I rely on the engineer's notes for where it falls.
   - The optional S16 note: not looked at; no call.
   - Round 4's cards on a phone: S91 and S94 at 390 px read cleanly as stacked cards, except S94's key (CR-S14). On Charcoal: pending the captures.
4. **The selection guide at true size.** At 1440 and 390 px the 127 pictures read as one drawing system: one box, one line weight, and the 2 px lines land crisp (3x zoom of the first row). By a script over the 82 pictures I could isolate at 1440 px, the median picture is about 4 percent subject ink; the heaviest (the party-colored map avoid tile, the donut, the big number) run 13 to 16 percent, under DD-G3's third. Avoid tiles read as struck in frame and falling rule. Tier words line up per row. Its markup is 149,403 bytes, and 127 of its 128 SVGs are a `<use>` of one shared symbol, so no geometry repeats. Not yet seen: 320 px (captures pending). The capture at 1440 px is cut short (see Not tested).
5. **The palette specification.** The order works (each palette's two ground panels, then its measures, then its table), and the method closes on short labeled lines. As a page a firm would print, two things fail: the 3 px grade lines (CR-S11) and the tables (CR-S12). "On Prussian" is in words only, as asked. A designer can choose a palette from the job sentence over each palette; the tables then need the work in CR-S12 to be used as a lookup.
6. **Rule 14.142, S96.** The band, the two drops in the strongest ink, the hatched preliminary months, the scale to 850,000 with no rule below zero, and the phone line all read as specified. At 1440 px every word clears every gridline: "Three-month average" sits between the +750,000 and +500,000 rules, "Margin of error" inside the band, and the two named labels under it on short leaders into their columns' feet. Two faults: the dashed preliminary average (CR-S9) and the failure's second difference (CR-S10).
7. **14.143 and 14.144, live and still.** From the captures at rest: each loop numbers its own steps (B4 one to three, R10 one to four), the two black C3 pills share one line at 680 px, and 14.144's cards carry no total and say R-38's targets sit off the loop in words ("Targets on Loop R8: None", then the words under "Targets outside this loop"). The still sequence, print, reduced motion and the 320 px text at 200 percent: not tested by me.
8. **Chapter 15 as one chapter.** 15.19 to 15.25 hold the chapter's grammar: the 680 px composition, typed chips, the evidence chip with its gloss, label-style heads, sources in the secondary ink. 15.25 is the calmest plate in the round. Against that: one broken line (CR-M1), two stepper orders (CR-S4), the stage mark (call 1), 15.23's two column lines (CR-S7) and 15.21's broken scales (CR-S8).
11. **Weight, from the build report.** Page 12,107,102 bytes; chapter 14 2,072,555 against its 2,803,941 figure; the kit 565,548; chapter 15 562,202 against 600,000; chapter 11 500,801 against 550,000. S96's figure on the page measures 16,299 bytes, and the kit prints about 16,140 with its frame, past its 15,000 share. The page is 3,892,898 bytes under 16 MB for Phase 4's seven chapters; I did not rebuild the projection. In what I measured (the selection guide, S96, 14.143, 14.144, the palette plate, 15.22, 15.24, S12, S89, S95, 11.10), I found no bytes a reader never meets: the charts draw from their specs, the guide shares its symbols, and 15.24's 62,060 bytes are mostly words behind disclosures a reader opens.

## 6. Questions for Dustin

1. **Board 3: S14's latest label and S59's "4.1" label.** Both are approved drawings where a label sits on or against a line. Recommendation: approve moving both, shown side by side at true size, so one standard holds across the guide and the kit's guard can apply to every form.

## 7. Tested

- Read the brief, my role file, the round 4 and round 5 design director notes, the V26 handoff's carried items, and the engineer's and cartographer's notes on the edge guard and S16.
- Looked at, from the shared captures at Newsprint 1x, 1440 px, whole and in tiles: the selection guide; the palette plate; S96 and its failure; 14.143 and 14.144 at rest; 15.19 to 15.25 (correct plates); S85 to S95, S12, sketches 14.83 and 14.84; Rules 11.10 and 11.11's trackers; the ballot and bill step tables.
- Pixel zooms (nearest neighbor, 2x to 6x) of the 1440 px captures: the selection guide's first row and the donut; the palette plate's grade lines; S96's key and its right end; 14.144's loop, chooser and chips; 15.20's effect rows; 15.22's key and spine top; S93's callout gutter; S95's all-states label in both crops (cleared by a knockout box).
- By script on the captures: each capture's caption edge; the palette plate's grade line pixel rows; the step tables' rule colors (one ink, 93, 99, 109); the subject ink share of 82 selection guide pictures.
- At Newsprint 1x, 390 px: S96, 14.143, 14.144, the selection guide (first 4,200 px), S91 and S94.
- On the built page (`c07/main/guide.html`), by script: 15.22's stage 10 markup and plate CSS; every `p.sq` on the page; the chip and `.id` CSS; the selection guide's skip links and SVG markup; the byte size of twelve plates. The build report's weight section.
- Node-only kit drawings (`run_spec`, no browser) to my scratch: S14 at pages 480 to 1440 px, measured for the latest label against the top gridline; S59 at 390, 1024 and 1440 px (rendered, not measured). `git status` before and after showed no file of mine in the repository.

## Not tested

- Charcoal, grayscale and every 2x capture: not landed when this draft was written.
- 320, 360, 768 and 1024 px; the `states/` captures; the `rules/` whole-rule captures.
- The selection guide's last question at 1440 px: the capture `newsprint-1x/1440/s-14-selection-guide.png` starts about 290 px above the guide (the opener's last row) and stops inside the Infographics question, so its last row and foot are not in the picture. The 390 px capture starts at the guide's title.
- Rules 15.1 to 15.18, the chapter 11 failure plates and Rule 11.12's plates: captured, not looked at closely.
- Any browser: I opened none (the load script printed WAIT at 17:05 UTC).
- Print, reduced motion, scripts off, forced colors, 200 percent text, keyboard and focus order.
- S16 and its note; S59's crossing measured; S14 and S96's dashed segment measured in the SVG.
