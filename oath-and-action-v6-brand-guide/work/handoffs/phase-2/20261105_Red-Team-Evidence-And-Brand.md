# Red team: evidence and brand

Oath & Action Brand Guide, Edition 06. Phase 2, November 5, 2026. One reviewer, two lenses: a standards-desk fact-checker and a brand guardian. I read the visible text of all six views of each system (Playwright, 1440 px), checked it against `shared/20261105_Atlas-Editorial-Data.json` by script, opened issue panels where the text loads on click, and audited computed colors, fonts, red marks, the wordmark and the icons. No page or project script was edited.

The counts are strong. Across the five systems the scripts compared about 3,300 structured facts (ID and name pairs, grades, delays, signs, loop cards, issue rows, effects) and found no mismatch. The failures sit in untagged prose, in disclosures and in red discipline.

## Shared findings

**S1. A vote that already happened, told in the present tense (Must fix, all five).** The R10 case paragraph says "A second repeal is on the November 3, 2026 ballot", and R-01's who-decides paragraph says "Massachusetts Question 3 and Alaska's repeal measure are both on the November 3, 2026 ballot." The pages are dated November 5. The dataset holds these as of the October 15 snapshot, and the status block says so; these two paragraphs drop the date. Undated mentions: 01 two, 02 one, 03 two, 04 three, 05 two. Fix: open each with "As of October 15, 2026,".

**S2. Red sign tags (Should fix, 01, 02, 04, 05).** On loop R10 and reform R-01 the tag body on L08 and L25 fills Pillar Red with ground-colored bars (01 `g.tg polygon`, 02 `g.tag polygon`, 04 `path.tg`, 05 `path.tgb`). The design frame says no sign is ever colored. Fix: keep the tag in ink and let the line, arrowhead and box carry the red.

**S3. "less" for countable things (Polish, 02 to 05).** "less incumbents defeated" (B4, 24 times) and "less watchdogs and enforcement" (R18, 8 times). 01 alone prints "fewer". Fix the read-aloud builder.

**S4. A V7 name that fights its sign (note for Dustin).** L23 is named "Poor service raises incumbents' risk of losing" and carries a minus. Every system prints the name beside "− lowers". The name is V7's; changing it is Dustin's call.

## 1. System by system

### 01 Times Explainer: 4 of 5

True almost everywhere, clean palette, red only on the loop and reform pages. Three holes.

**Must fix**
1. Elections, section head: "39 problems tracked here, each with a real case." I028, "Equal Senate seats give small-state residents more weight", has no `problem_example`, and the row itself prints "No worked example in the record". Fix: "39 problems tracked here; 38 with a real case."
2. Disclosures (D2-80). Elections: the R-47 card shows what it changes, its targets and its effects with no disclosure (R-01 and R-02 carry theirs). Loop R10: the reform picker shows R-01 and R-02 cards with "Acts on" lines and no disclosure. Data: `reforms[...]['disclosure']`. Fix: print it on each card.
3. S1, two mentions.

**Should fix**
4. Overview part rows and the catalog: "Loops that start here" and "Four loops start in Wealth". The lists follow the dataset's `home` field, and five loops start elsewhere: R12 at D3 and B4 at D5 (Checks), both filed under Elections; R15 at A2 (Wealth), under Voice; B1a and B5 at E1 (Policy), under Checks. The page's own drawings start R12 at "Rulings favoring appointers". Fix: "Loops based here".
5. S2.

**Polish**
6. Elections: "Two loops meet at risk of losing office." C3 sits on four loops (B4, R10, R11, R16). Fix: "Four loops pass through risk of losing office; two are drawn here."
7. Overview: "A condition is something that can rise or fall, such as safe seats or rent." No variable is rent. Use "the cost of essentials".
8. Reform: "The problem is better established than the remedy." V7 ranks plausible and contested alike (rank 2). Fix: "The problem is graded plausible; the remedy, contested."

### 02 Economist Register: 3 of 5

The most exact register of counts, and the weakest on disclosure. It cannot ship until item 1 is fixed.

**Must fix**
1. Disclosures missing on four of six views. Overview, Elections row, "The fix aimed at it": R-01 with summary, targets and effects. Overview, Technology row: R-39 with effects and route. Elections reform table: R-01, R-02 and R-47 with effects and most open route. Loop R10 picker: R-01 and R-02. Issue panels (opened I026 and X09): R-01, R-02, R-47 and R-49 with reasons. None prints a disclosure; only the R-01 profile does. Data: `reforms[...]['disclosure']`, D2-80. Fix: print it wherever the reform shows more than its title.
2. S1, one mention.

**Should fix**
3. Overview "Every loop" and the catalog: "Grouped by the part where each loop starts." R4b starts at C4 (Elections) and R15 at A2 (Wealth), both filed under Voice; R12 and B4 start in Checks; B1a and B5 start in Policy. The grouping is V7's `loop_groups`, and the Elections page counts R4b among its seven loops. Fix: "Grouped by V7's home area", and file R4b with Elections to match that page.
4. Register note: "Main loop: the loop with the most steps in the part". By that rule Wealth's loop is R8 (two steps inside, L38 and L39; R6 has one, L30) and Voice's is R3 (L46 and L47; R15 has one, L34). The picks follow stations. Fix: "the loop with the most stations in the part".
5. The brand name in live type: "Oath & Action" in Inter 600 (`span.credit`) under 16 chart source lines. Fix: drop it; the masthead wordmark signs the page.
6. Off-palette hairlines: `rgba(93,99,109,.45)` on 118 connection rows, `rgba(93,99,109,.3)` in the panel, `rgba(220,217,210,.5)` in the overview effects list. Fix: full-strength Stone or Deep Stone.
7. S2.

**Polish**
8. Flows in words: "Flows that skip a step: ... Checks to Voice 2". That flow runs back two parts. Say so.
9. The circuit drawing leaves out Voice to Checks (2), Voice to Policy (3) and Checks to Voice (2); only "The flows in words" names them. Add a line under the drawing, as 04 does.
10. How to read: the red swatch carries `data-red="working"`, job "palette swatch". Rule 05.3 exempts swatches; mark it as a specimen.
11. S3.

### 03 Reference Sheets: 3 of 5

Every structured fact checked clean (964 of them), and the R-01 sheet is complete. It spends red where the rules keep it out, and one headline claims more than the loop's evidence.

**Must fix**
1. Sheet 02 issue details list "Reforms aimed at it" with a reason for R-02, R-47 and R-49 (R-49 three times). R-49's disclosure, "Oath & Action's editor is an Army veteran.", appears nowhere on the sheet, and the R-02 and R-47 lines sit far from their cards. Fix: add the disclosure to each line.
2. S1, two mentions.

**Should fix**
3. Working red outside the loop and reform pages. Sheet 01 overview: a red ring legend and marks on the Elections card (6 marks). Sheet 02 Elections: 3 marks. Sheet 05 catalog: 3 marks on the R10 card. Sheet 00: a specimen marked `working`. The brief allows the reform's red on the reform and loop pages, the frame memo keeps the overview at rest to signature red, and none of these headlines names R-01. Fix: remove it from sheets 01, 02 and 05; mark sheet 00's as a specimen.
4. Sheet 03 headline: "Safe seats keep themselves safe." The loop closes through L53, graded plausible, and V7's qualification says seat safety also comes from where voters live. Fix: V7's title, or "Safe seats can keep themselves safe, through one plausible step."
5. Sheet 02, R-07: "Democratic quality small positive (V7: +S entry; −S extremity)". The lead word turns a mixed effect into a gain. Fix: "small positive for entry, small negative for extremity", as 02 prints it.
6. Plate 01.3: "Of the 23 loops, 18 feed themselves and 5 push back. The atlas also holds 3 sketches". "Also" reads as 26 loops. Fix: "Three of the 23 are sketches".

**Polish**
7. Route tables print "Checked 2026-10-15"; every other date reads "October 15, 2026".
8. Sheet 00 glossary, from V7: "Outside driver ... Drawn as a rounded pill outside the clusters." The sheet draws outside forces as "an open frame with no rule". Trim the drawing note.
9. Sheet 00: "It is an idea, not a numbered connection." Corrective negation. Fix: "It is an idea with no numbered connection."
10. S3.

### 04 Night Edition: 4 of 5

The best on disclosure: the only system that carries them into issue panels (I026 and X09 opened). One overclaim, one leaked editor's note, and an unapproved tint.

**Must fix**
1. S1, three mentions.

**Should fix**
2. Overview deck: "This atlas traces how that happens, one documented connection at a time." 32 of 118 connections are graded documented, and the page teaches Documented as a grade. The words are V7's opening; on this page they overclaim. Fix: "one graded connection at a time".
3. Loop R10, "What would widen the deciding electorate": prints V7's internal `fix` note, which ends "Drop the moderation claim." That is an instruction to an editor, and the paragraph prescribes reforms in the atlas's voice on the page where the editor's own campaign is disclosed. Fix: drop the section; the reform cards below already say what each would change.
4. Off palette: the proposed Night Panel `#1F1F1E` fills 104 loop boxes (`rect.ak-mark bx`) and the `.qcard` and `.aloud` grounds across five views. The notes mark it proposed; the page does not. A `box-shadow: -24px 0 48px rgba(0,0,0,.45)` on the side panel at 900 px and wider adds faux depth, a listed fault. Fix: Charcoal with a 1 px Stone rule until Dustin approves the tint; drop the shadow.
5. S2.

**Polish**
6. Loop R10 and reform R-01 drawings label "R-03 aims here", "R-02 aims here" and "R-03 acts on this step" on R-01's own page, where a reader expects only R-01's points. Keep other reforms on the picker.
7. Overview deck: "Rent climbs faster than pay." A policy claim with no source or period (CLAUDE.md honesty rule). Source it or cut it.
8. S3.

### 05 Architecture: 3 of 5

Every floor count, flow count and hub reach checks out, and the icons are exact. It drops a grade from its keys and keeps disclosures off its issue panels.

**Must fix**
1. Elections issue panels list "Reforms aimed at it" with reasons: R-01 and R-02 twice each, R-47 and R-49 three times each, with no disclosure. R-49's appears nowhere on the floor. Fix: print the disclosure beside each.
2. S1, two mentions.

**Should fix**
3. Grade keys on the overview ("Inside a floor, lines carry their evidence"), the R-01 page ("Texture is the evidence") and the catalog ("Reading a loop card") list Documented, Plausible, Contested and Hypothesis, and leave out "Well supported: strong research evidence", the grade of 37 connections. Fix: add it.
4. Elections issues intro: "Open any one for its real-world problem, a fix tried somewhere, and what the evidence says." 27 of 39 records carry a tried fix, and I028 has no real-world problem. Fix: "Open any one for its full record."
5. "The 23 loops, by home floor" puts R4b under Voice. The dataset's `home` is C, and the Elections floor counts R4b among its seven loops. Fix: move it.
6. S2.

**Polish**
7. "The return line at left carries policy's effects back down to Wealth." One of its four connections, LE12, lands in Your household, as the page's own count says. Add "and your household".
8. Catalog prints V7's raw "Disabled" (B1a) and "Disabled in concentrated sectors" (B3). 01's "Switched off" reads better.
9. Lora Italic on unquoted text: "Policy that favors insiders adds to wealth at the top." on the return line, and "Improvement or decline can reinforce itself." in the catalog. Quote and attribute them, or set them in Inter.
10. S3.

## 2. Facts checked

"Structured" means facts tied to an ID or a fixed row format, checked by script: ID and name pairs, grade, delay and sign words beside a connection, loop cards (kind, weakest step, delay, reform count, sketch and hypothesis notes), issue rows (title, example, grade, touched conditions), connection rows and reform effects. "Untagged prose" means counts and set claims in sentences and headings, checked by script or by hand against computed values: flows between parts, part counts, loops per part, register columns, hub reach, issue counts, headline claims.

| System | Structured facts | Failed | Untagged prose statements | Failed | Undated ballot statements (S1) |
|---|---|---|---|---|---|
| 01 Times Explainer | 591 | 0 | about 95 | 2 | 2 |
| 02 Economist Register | 716 | 0 | about 80 | 2 | 1 |
| 03 Reference Sheets | 964 | 0 | about 70 | 2 | 2 |
| 04 Night Edition | 525 | 0 | about 45 | 1 | 3 |
| 05 Architecture | 492 | 0 | about 50 | 2 | 2 |

The failed prose statements: 01 "each with a real case" and "loops start here"; 02 "where each loop starts" and the main-loop rule; 03 "also holds 3 sketches" and R-07's "small positive"; 04 "one documented connection"; 05 "a fix tried somewhere" and R4b's home floor.

Completeness passed in all five: all 51 conditions and all eight parts with their questions on the overview; all 23 loops in the catalog; all 39 active Elections issues with their example headlines, and all ten Elections reforms. In 02 and 04 the example texts load when a row opens; I opened three per system (I001, I026, X09).

Honesty rules, all five: sketched loops (B2, B3, R9) and hypothesized steps (R2, R16) disclosed in the catalog, and R16's on the Elections view; no reform effects summed; undated routes shown as "No check date in V7"; the plus-sign line taught; R-01's disclosure in full on its page; no partisan framing (party and officeholder names appear only inside V7's examples, and the map-drawing example names both parties). Exceptions are listed above: disclosures elsewhere (01, 02, 03, 05), the Well supported gloss (05) and overclaiming headlines (01, 03, 04).

Brand, all five: the 24 px and 16 px wordmark masters inlined with their path data intact, 221 by 24 px at 64, 24 (23.5 in 05); no live-type wordmark in a masthead; only Inter, Inter Tight and Lora declared; no red on hover, navigation or Prussian among the controls I hovered; every red mark carries `data-red`. Colors other than the locked and approved values: 04 `#1F1F1E` and `rgba(0,0,0,.45)`; 02 Stone at 45 and 30 percent and Newsprint at 50 percent. The `#000000` in 04 and 05 is the mask cut inside approved Civic Line files. Icons appear in 03 (14), 04 (200) and 05 (141); every path matches the package, at 48 px, with one 64 px (03) and one 96 px feature icon (05). 01 and 02 use none.

Writing: no em dashes in any view. The regex scan for antithesis, corrective negation, intensifiers, hedges and corporate verbs found one studio hit (03, item 9). Hits inside V7 text were set aside.

## 3. What I checked and what I could not

**Checked**
- Visible text (`innerText`) and full DOM text of all 30 views at 1440 px, written per view to the scratchpad.
- `idcheck.py`: every connection, reform and issue ID against its name, grade, delay and sign word on the same line.
- `loopcheck.py` and `s03loops.py`: all 23 catalog cards and the seven Elections loops per system; per-step sign, grade and delay on 03's cards.
- `issuecheck.py`: the 39 Elections issues per system (titles, example headlines and texts, grades, touched conditions in 01).
- `facts.py` and inline scripts: the 27 flows between parts, counts inside parts, busiest pair, loops and issues per part, the 02 register columns and main-loop rule, the 05 floor counts and flow classes, the 03 pathway routes, reform targets, effects and most open routes, delay and grade totals.
- Disclosure presence per view for all eight flagged reforms; opened issues I001, I026 and X09 in 02 and 04.
- `extract.js`, `colors.py`: computed color, background, border, fill and stroke on every visible element of every view; raw color literals in each file.
- `redaudit.js`, `tagprobe.js`: every Pillar Red element per view with its `data-red`, job, nearest control and ground; hover on up to 40 controls per overview.
- Wordmark path data against both masters; icon paths against all 1,060 package paths (`icons.js`).
- Every headline and section head, read against the evidence it names.

All scripts sit in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/116edc6c-f1d0-50f6-9263-c43fde110995/scratchpad/`.

**Could not check**
- The 390 px views; I extracted text and colors at 1440 px only.
- Rendered fonts. I blocked network requests, so the font check reads declared families, not loaded faces.
- Selected and focus states beyond hover on overview controls, and most panels. 05 holds about 85 red-accent icon elements hidden at rest; I could not confirm their state when shown.
- Every untagged sentence inside the 39 issue records and the long reform texts; I sampled them.
- Rhetorical triplets, nominalizations and setup-and-payoff lines across all body text; I read headings and decks for these, and the regex scan does not catch them.
- Whether the dataset matches V7 or the world, including the November 3 results, which the dataset does not hold.
- Sources and URLs behind the examples.
- Contrast, grayscale captures and print.
