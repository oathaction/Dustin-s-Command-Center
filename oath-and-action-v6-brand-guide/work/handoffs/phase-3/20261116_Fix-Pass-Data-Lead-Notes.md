# Fix pass data lead notes

Oath & Action Edition 06, Phase 3, the fix pass after the review of rounds 4 and 5, chat 7. Written by the data visualization and systems lead (`oa-dataviz-systems-lead`) under `work/handoffs/phase-3/20261116_Rounds-4-5-Fix-Brief.md`. Started 17:00 UTC, November 16, 2026. Scratch and scripts: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f55a08bf-cdcf-539d-a683-426e26f4f342/scratchpad/c07/fix/data-lead/`.

## Status

- 17:40 UTC. **Batch 5:** DF-10 closed; both batch 4 items hold, and the court foot's "2024 edition" is right.
- 17:38 UTC. **Batch 4:** NB-S5 signed off (R6 printed and held by script). DF-10 signed off but two items: stage 2's Constitution and House Rule XX parts need their dates retrieved, and 15.23's "as amended" on Executive Order 12866 goes.
- 17:30 UTC. **Batch 3:** CE-S20's "No petition" sentence in place; chapter 11 signed off whole.
- 17:30 UTC. **Batch 2 (chapter 15):** the R1 stage marks signed off as built; every other code signed off on its source; DF-10 and NB-S5 wait on R7 and R6 being applied. Nothing sent back.
- 17:27 UTC. **Batch 1 (chapter 11):** marks unchanged; call 4's extension yes (steps 5 and 6 under slashes with no petition); facts signed off; one item sent back, CE-S20's "No petition" row needs a sentence. **Rulings R6 (NB-S5: keep R-28 with its rule printed) and R7 (DF-10: "Retrieved", and the version the copy states) written.** Batch 2, chapter 15, next.
- 17:08 UTC. **Rulings R1 to R5 written** (call 7), with R4b for ST-S2. Owners read them under "Rulings". Sign-off batches follow as owners report fixes.
- 17:00 UTC. Started.

## Rulings

Written 17:00 to 17:08 UTC for the owners to read directly (call 7). Every atlas value here was read by script (`python3 -I`) from `work/extract/atlas-v7-data.json` (snapshot October 15, 2026); every payroll figure from `work/build/data/fred-payrolls-by-sector.csv` and S96's spec; every mark from `phase3_ch15_build.py`, `phase3_ch13_build.py` and chapter 11's file. Final words are the editor's; the facts and limits below are not.

### R1. The stage mark on Rules 15.22 and 15.23 (call 1, DF-2, CE-S10; for the systems designer, the editor and the design director)

**What chapter 11 uses**, from Rules 11.2 and 11.3: a filled circle (done), a heavy ring (now), a fine ring (not yet), a fine ring under a slash (never happened), a filled square (stopped), the red disc (take part). Fill against outline means done against not yet, and a heavy edge against a fine one means now against not yet. Rule 13.4 also uses a 7 px filled square for a documented record.

**Ruling: a stage carries its number alone, set on its line, with no shape around it.**
1. *On 15.22.* Each stage's number is a bold figure in the data label type, in the text's ink, centered on its line where the square sits now. Behind the figure sits a knockout in the surface color with no edge, so the line breaks around the number and nothing reads as a mark. Every stage's number looks the same, on the spine and off it.
2. *Spine and paths differ by their lines, never by the number's mark.* The spine runs on the line in the text's ink at the subject weight; the paths that leave it and what follows the law run on the gray line at the context weight, with their set-in and arrow as now, and their words ("In place of the usual floor rules", "Then stage 6"). No fill against outline and no heavy edge against fine, since chapter 11 gives both pairs a state.
3. *A path that stops* keeps the 10 px filled square (`.sqm`), which is chapter 11's mark for exactly that (Rules 11.2 and 11.3). It is then the only square on the plate.
4. *The key* draws each entry as the plate draws it: a number on the line in the text's ink; a short gray arrow to a number; a number on the gray line; the square for a path that stops; the line back to stage 1. Its words follow DF-5 ("on the line in the text's ink", "on the gray line").
5. *On 15.23.* Each stage prints in words as now, "Stage 3: Suspension of the rules", with no square, ring or other mark (the `.wq` square goes). The tracker's steps keep chapter 11's numbers and names as chapter 11's step tables print them ("4 First chamber"), with no state mark, since the plate follows no bill and any mark would claim a state. If the systems designer keeps the difference between a stage on the spine and a path set to one side, it says so in words (for example "or, in place of it, Stage 3 ..."), never by fill or edge. CE-S10's lead line then has no squares to explain; a line saying that stages keep Rule 15.22's numbers and the word "Stage", and steps keep chapter 11's numbers, is the editor's choice.
6. *Forced colors and print.* The number in `CanvasText` on a `Canvas` knockout; lines and the stop square in `CanvasText`. Every stage number stays live text, so it reads aloud and survives grayscale.
7. *Rule 15.22's text* loses "in filled squares" and "dark line"; the editor writes it. The failure plates `s-15-22-failure` and `s-15-23-failure` take the same marks, so each still differs from its correct plate by its one fault.

**Why not Rule 14.96's box.** DF-2 offered it. A box with a heavy edge for the spine and a fine edge for the paths puts heavy against fine outlines beside chapter 11's heavy ring (now) and fine ring (not yet), and a 22 px outlined box with a number reads a stroke away from the stop square. A route's stage has an order and no state, and a bare number says an order and nothing else. Boxing all 20 stages and their source columns would also rebuild the layout that CE-M4 and DF-11 already change. Rule 14.96 itself is unchanged; it draws one process at Gate 2's approval and keeps its own look.

### R2. Rule 14.143's walk: say each change in the direction it runs (CE-M1; for the complex examples maker, the editor, the component engineer and the accessibility lead)

**The fault.** Each step's line is the connection's general sentence ("The quality of public services lowers the risk of losing office"), read straight after "suppose it falls", so its verb reads as the scenario's direction and runs the wrong way.

**The directions, by script** (start supposition, then each sign):

| Step | Connection, sign, grade | Direction under the walk |
|---|---|---|
| B4, 1 of 3 | L23, minus, well supported | Quality of public services falls, so the risk of losing office rises |
| B4, 2 of 3 | L24, plus, well supported | The risk rises, so the number of incumbents defeated or pushed into retirement rises |
| B4, 3 of 3 | L54, plus, well supported | That number rises, so the quality of public services rises: against the first fall |
| R10, 1 of 4 | L08, plus, documented | Seats with little electoral competition rise, so how often the primary decides the winner rises |
| R10, 2 of 4 | L25, minus, well supported | That rises, so the risk of losing office falls |
| R10, 3 of 4 | L53, minus, plausible | The risk falls, so officeholders' control over election rules can rise |
| R10, 4 of 4 | L42, plus, documented | That control can rise, so seats with little electoral competition can rise again: on top of the first rise |

**Ruling.**
1. *The line* (what the status line and the still list read first) states the walk's direction at both ends, cause first: "{from} falls, so {to} rises." Each direction comes from the start supposition and the signs, computed by the generator, never typed, and the build stops if a computed direction and the printed one disagree.
2. *A plausible step says "can"*, as now, and every direction after it keeps "can" until the loop closes, since the chain then rests on that step (R10, steps 3 and 4).
3. *The connection's own claim moves to the step's further words*, with its sign in words that hold either way: its chip and the atlas's name, then "a minus sign: when one rises the other falls" or "a plus sign: the two rise and fall together", then its grade and delay as now. The general sentence with "lowers" or "raises" as its verb does not print as the line. The atlas's `how_to_read` may still be quoted in a disclosure, marked as the atlas's words.
4. *Each loop closes on its result*, in Rule 15.6's words for the kind: B4 ends with the quality of public services rising against the first fall, so the loop pushes back and, with one minus sign, is balancing; R10 ends with seats with little electoral competition able to rise again on top of the first rise, so the loop can feed itself and, with two minus signs, is reinforcing. Rule 15.6's plate and spec ("one sentence that carries more or less around the loop and back to the start") govern the wording; the editor sets it.
5. *What stays.* The start sentences ("suppose it falls", "suppose they rise"), ruling (d)'s order, the drawn step numbers, Variable C3's title in full (DR-265), every grade, delay and qualification, and the sentence that the atlas holds no measure of either loop's strength. "How often the primary decides the winner" keeps its whole title in the sentence (DR-265); "rises" or "goes up" after it is the editor's call.
6. *Where it prints.* The line in the list, the status line, the still and print sequence, the keys file (component engineer) and the alt all read the same words, so a reader with scripts off meets the same directions.
7. *Read from both sides.* The walk claims nothing the model's signs do not: B4's push back rests on three well supported steps; R10's feed rests on a plausible step and says "can". Neither loop is weighed against the other.

### R3. Rule 14.142's failure plate: one fault, and the caption names it (ST-M1; for the complex examples maker and the editor)

**The one fault is that the margin is left out**, of the drawing and of the words. Counting seven is not the fault: Rule 14.142 asks for the count, and DR-239's title on the correct plate makes it.

**The failure plate is S96 with the margin taken out, and nothing else changed:**
- no band; all seven drops labeled alike, as if each were a finding; the title states seven months of lost jobs with no word on the margin (today's "The economy lost jobs in seven months of 2025 and 2026." does this);
- S96's window, scale (minus 400 to 850, and its narrow scale), columns, hatch, dashed average and notes, less the margin's note and the table's margin column;
- **no latest label**, as DD-E3 ruled for S96: a value inside the band is not the lesson;
- **the plain source line**, with no margin sentence, since the plate draws no margin. (The guide's `s-14-142-failure.chart.json` already lacks it; the placed figure in the review build printed it, so check the figure as built.)
- no red.

**The caption names that one fault and its effect.** Draft for the editor, from ST-M1: "<strong>Fails Rule 14.142.</strong> The survey's margin is left out. With no band, all seven drops look alike, and the title states seven months of lost jobs with no word on the margin. Five of the seven sit inside it, where the survey cannot tell them from no change." The alt says the same in words.

### R4. What S96 says a 90 percent band means across 57 months (ST-S1, CE-S13; for the complex examples maker, the editor and the statistics reader)

**The facts.** The band is the Bureau of Labor Statistics' 90 percent interval for one month's change, drawn around zero. Had a month's true change been zero, the survey's estimate would land inside the band nine times in ten: about one time in twenty below it and one in twenty above. The band holds for each month alone. Across many months, some months with no real change behind them can still pass it. It says nothing about the three-month average, and nothing about how far a revision may move a month (both already in the notes).

**Ruling.**
1. *S96, note 1*, carries three points in this order: the band's size and source; what it means, in the zero-centered form ("had a month's true change been zero, the survey's estimate would land inside the band nine times in ten"); and the caution, "The band holds for each month alone, so across 57 months a few columns could pass it by chance." The existing sentences on a column inside the band and on the average stay. ST-S1's draft ("a month with no real change still lands past it about one time in ten; over 57 months a few could pass it by chance") states the same facts and may be used.
2. *Rule 14.142's text* names the Bureau in full and glosses the level once: "give its size, its confidence, such as the Bureau of Labor Statistics' 90 percent, which means a month with no real change lands inside the band nine times in ten, and its source in a note (Rule 14.9)", then one sentence: the band holds for each month alone, so over many months a few can pass it by chance, and a note says so. The why may add the same clause.
3. *The alt* glosses the band once, in a short clause with the same meaning.
4. *Not to print:*
   - "a range that would hold the true change in nine samples out of ten" said of the drawn band (CE-S13's draft). That reading belongs to an interval around each month's estimate. This band sits around zero, and a month with a real gain of 300,000 sits far outside it.
   - "nine times in ten" joined to "cannot tell apart from no change" (CE-S13's note draft), which mixes the two statements.
   - "90 percent accurate", "90 percent sure", or "confidence" with no gloss.
   - A count of expected chance passes, such as ST-S1's 5.7 or 1.05. Each assumes no month had a real change, which the data rule out. They stay in our notes.
5. *What stays.* DR-239's title, the two named drops, the table's margin words (2 drops past, 32 gains past, 23 within), the band's look.
6. *Read from both sides.* A reader who wants a weak economy still reads that two drops pass the margin; a reader who wants a strong one reads that passing it is not proof. The caution applies to the 32 gains past the band as much as to the 2 drops.

### R4b. October 2025's and February 2026's drops: where each fell (ST-S2; for the complex examples maker, the editor and the research lead)

**Yes: note 2 gains one sentence, in words only, for both named months.** By script from `fred-payrolls-by-sector.csv` (the same FRED copy, PAYEMS matching S96's file):

| Month | Total | Private (USPRIV) | Government (USGOVT) | Federal (CES9091000001) |
|---|---|---|---|---|
| October 2025 | −140,000 | +13,000 | −153,000 | −166,000 |
| February 2026 | −156,000 | −148,000 | −8,000 | +4,000 |

1. Use the split into private and government for both months, so each pair adds to its month's total and both months take one form. Draft: "In October 2025, government payrolls fell 153,000 and private payrolls rose 13,000; in February 2026, private payrolls fell 148,000 and government payrolls 8,000." The federal figure may follow for October only if the editor wants it and it names state and local's rise too, so no reader adds two figures that do not make the total.
2. No cause, no program, no agency, no word of blame or praise. No words on the drawing; the named labels stay as they are.
3. The source line covers the two sector series: the research lead gives the words from the sector file's sidecar (Request 1 below).
4. Read from both sides: a reader on either side learns what fell in each month, one month in government and one in private payrolls, from the same official survey, stated the same way.

### R5. Rule 14.144's cards against Rule 15.20's panel, with Rule 13.5's pips (call 2, DF-3, DF-7, CE-S14; for the complex examples maker, the editor, the component engineer and the accessibility lead)

**Ruling (d)'s "no pips" (D3-1973) is replaced.** Rule 13.5 (DR-237) governs the effect mark. My reason then, that pips in three columns invite a reader to add them, is answered by the atlas's sentence that every card keeps, by the failure plate, which shows the total as the fault, and by one mark carrying one property across chapters 13, 14 and 15.

**Effects.**
1. Each family's row draws Rule 13.5's mark with `pips_svg` from `phase3_ch13_build.py`, the function Rules 15.16 and 15.20 call, so the mark is one by construction: one to three pips right of the zero line for a gain, left for a cost, a bar on the zero line for 0, and the zero line alone for "?". Same size in every card, in the text's ink, aria-hidden, with the forced-colors rule the shared CSS already gives `.pp`.
2. Beside the pips, the code whole as the atlas stores it, then the code's words, as ruling A-2 item 6 and Rule 14.144's own text set: "**+L** local, large positive"; "**0**, no expected effect". The qualifier is never moved after the words or reworded.
3. The row form follows 15.20's: a heading "Effects by outcome family" (the date stays once over the set, DD-R4), then one row a family in the atlas's order, the family's name, the pips, the code and words. The rows replace "Effect on quality of democracy" and its kin.
4. The seven-code key draws each code with its pips (the "?" with the zero line alone), so the key teaches the mark. The atlas's sentence stays, quoted, under it.
5. No total, count of codes or pips, average, rank, sort, fill, shade, length, width or color by code. Pips never line up across cards into a sum: each card keeps its own rows.
6. Rule 14.144's text: "Set the codes as text in the text ink" becomes a sentence that draws each code with Rule 13.5's pips beside it, whole, and keeps "with no total, count, average or rank, since the atlas never adds effects across families". The Never spec loses "bar", since Rule 13.5 draws a bar for 0; it reads, in substance, "a total, a count of codes or pips, a rank, or a fill, shade, length or color by code". The editor sets both.
7. *The failure plate.* Its total stays the fault and its caption stands. It draws the same codes as the cards, so if its table holds Rule 13.5's pips at its widths (328 and 680 px), draw them, and the caption may say the score counts each pip as a point; if it cannot hold them, keep the codes as text, since the fault is the total alone.

**Routes and grades take 15.20's and 15.16's form (DF-7).**
- *Routes:* the heading "Routes, with the date each was checked"; each route's chip and name, who acts on its own line, "**High** feasibility" with the word in bold, and "Not checked" or "Checked October 15, 2026" on its own line, as `route_rows` in `phase3_ch15_build.py` prints them. R-38's state statute route keeps its check date (DD-R4's condition 2).
- *Grades:* each grade as 15.16's `grade_block` prints it, the grade chip with Rule 13.3's gloss, then the atlas's term: "Well supported, strong research evidence, evidence of the problem" and "Plausible, some evidence, evidence for the remedy". R-38's problem grade is "Contested, evidence disputed". "Evidence for the problem" goes everywhere it prints.
- *Band (CE-S14):* the word, then the atlas's definition quoted, as 15.20 prints it: "**Rules**: “Changes incentives, penalties and constraints: who may run, how votes count, what firms may do (level 5).”" All three reforms are in the rules band, so the definition may print once over the set if the cards would repeat it three times; either way each card says "Rules".
- *Confidence:* the atlas's words quoted, as now.
- *Words:* "the text's ink", never "the text ink", in the rule and its specs.

**What stays.** Ruling (d)'s order and line-up, A-2's targets and status lines, DD-R4's single date, R-38 on the plate, no status text, no route note.

**A latent difference, for the systems designer, not blocking:** `effect_rows` in `phase3_ch15_build.py` prints a qualified code as "**+L** large positive, local", splitting the stored string, where Rule 15.16's own spec says "An effect prints its full code, qualifier or range whole, beside its pips". No chapter 15 plate shows a qualified code today (R-01, R-03 and R-04 have none; 38 effect values in the model do), so nothing on the page differs. If 14.144 reuses that function, it must print the stored string whole first.

### R6. Rule 15.24's one worked example: keep Reform R-28, and print the rule that picks it (NB-S5; for the systems designer, the editor and the main session)

Written 17:27 UTC.

**The rule: the reform an earlier drawing already put on a route.** By script on `v7-reconciliation-rows.json`, Rule 15.25's row 41 is the one row in which an earlier drawing showed one reform on one route: the fifth edition and the atlas visual system drew Reform R-28 on "a federal tax-law route through reconciliation", with no feasibility or date. Row 28 speaks of all route strands, not one reform. So the rule picks exactly one reform, R-28, and the example then shows that route drawn true to the model: Route FS, its entry's word "Reconciliation", low feasibility, "Not checked".

1. *Print it.* One sentence on the plate names the rule and the row, as the systems designer drafted: R-28 is the reform an earlier drawing already put on this path, and Rule 15.25's row 41 records that drawing. The editor sets the words. The failure plate keeps R-28, so it still differs by its one fault (the 60-vote path).
2. *Log it* with the call below and the read from both sides.
3. *Why not "the first reform in the atlas's order whose federal entry names reconciliation".* It picks R-25, also a tax reform, so a reader who thinks the example leans one way meets the same kind of reform; it would redraw the example and its failure; and it ties the example to nothing the guide corrects.
4. *Read from both sides.* The rule reads only the record of what earlier drawings showed, so it picks R-28 whoever applies it. The plate prints R-28's entry as the atlas holds it, low feasibility and not checked, which neither promotes the reform nor dismisses it, and its lesson is the route's form, not the tax.

### R7. A law's source line on Rules 15.22 to 15.24: "retrieved", and the version the copy states (DF-10; for the systems designer, the research lead, the editor and the main session)

Written 17:27 UTC. The version facts wait on the research lead's F10; this sets the form.

1. **"Retrieved", not "read", for the date we took a law's text.** Rule 13.6 (DR-237) and house rule H04 name the part "the date retrieved", and define it as "the day we read the file". Chapters 11, 13 and 14 print "retrieved" (8, 8 and 11 times in their chapter files by search); chapter 15's plates print "read" 43 times, from my round 5 ruling (e)'s "Source read". That ruling is replaced: chapter 15 takes the approved word. The distinction (e) wanted still holds, since "Retrieved" names our date and "Checked" or "Not checked" names an atlas entry's own date (Rule 13.10). Rule 15.24's group line "the date we read it" becomes the editor's equal with "retrieved". Board 2's S71 printed "read" on route pages; it is approved work, so it stays for this pass and goes on board 3's list.
2. **The version, from the copy itself.** Each statute or rule prints the version the copy we read states, in the title part of the line (Rule 13.7: name the vintage where the text can change): for govinfo's U.S. Code, its edition ("U.S. Code, 2024 edition"); for a copy that states how current it is (the House's U.S. Code site prints "current through Public Law" with its number), those words. "As in force on" a date prints only where the copy states that date. A date we retrieved a page is never relabeled as the law's date.
3. **A condition for F10.** Where a cited section may have changed after the edition we read (the U.S. Code 2024 edition stops before 2025's and 2026's laws), the research lead checks the section's current text or its amendment notes and says which; a section changed since then is cited from the current text.
4. **Order.** Rule 13.6's: publisher, the law and its version, the geography where one applies, "via" the copy, "Retrieved" and the date, then any qualification. 15.22's atlas sentence keeps its order as fixed (snapshot date with the atlas, then the stages' sources).

## Sign-offs

### Batch 1 (17:27 UTC): chapter 11 signed off but one item: CE-S20's "No petition" row needs its words (for the tracker designer, the editor, the research lead and the main session)

Read from the tracker designer's notes (17:23), `11-icons.json` (Rules 11.8, 11.10 and 11.11 whole, by script), `s-11-10-correct`, `s-11-ballot-steps` and the sources file's court and California rows. Marks and facts first, words last. The editor's second read of the same words runs now; nothing here sets words.

**Marks: unchanged, signed off.** By script, the `data-icon` marks and drawings of `s-11-10-correct`, `s-11-11-correct`, both failure plates and the ballot step table equal those at the review commit `8ace3dc6`. Each correct plate still holds one current, one decided or certified and one stopped item (DR-275). Only words moved: `11-icons.json`, Measure 99013's line and step 2's words.

**Call 4 (CE-S20) and its extension: yes.**
- A ruling no one appeals ends by a ruling, not a stop, so the steps the law did not reach go under slashes with its words, as Rule 11.8 keeps step 6 of a request no one appealed. The square keeps chapter 11's one meaning, "Stopped", for settlement, dismissal and a denied petition. My round 5 ruling (f) and batch 1 listed "never appealed" among the squares; call 4 replaces that.
- **Steps 5 and 6 under slashes when no one petitions the Supreme Court: yes.** The same reason holds one court up: the appeals court's ruling ends the case, and nothing stopped it. It also matches round 5's measure the Legislature passes, which keeps steps 5 and 6 under slashes after an end that is not a stop. A denied petition keeps its square at step 5, since there a step was taken and refused.
- **"No petition" names no day count: yes.** The sources file's step 5 row quotes 28 U.S.C. 2101(c) and Supreme Court Rule 13.5: a justice may extend the 90 days by up to 60, so a fixed count would be wrong for some cases.

**Sent back, by code.**
- **CE-S20, the "No petition" row has no words for its slashes.** Rule 11.2: a shape and the words beside it say the same thing. "Never appealed" carries its sentence ("No appeal was filed in the 30 days the law allows."); "No petition" gives the appeals court's ruling alone, so a reader sees two slashes with nothing saying why. Add one sentence after the appeals court's ruling, and after CE-S19's "The lower court's ruling stands." where the ruling leaves one in place, saying no one asked the Supreme Court to review it in the time the law allows. The editor sets the words; no day count.

**Suggestions, not conditions.**
- *"Never appealed".* 28 U.S.C. 2107(c) lets the district court extend the time to appeal on a motion, and the sources file's step 3 row quotes 2107(a) and (b) only. For parity with "No petition", the sentence could read "in the time the law allows, 30 days from the judgment, or 60 where the United States is a party", or the research lead adds 2107(c) to the row. Either way the slashes wait for the time, extensions included, to pass.
- *Both rows* could say the next step keeps a fine ring while the time runs, as Rule 11.8's step 6 spec does.

**Facts: signed off, each held to its source.**
- *ST-S3.* Measure 99013's line, "projected fewer than 95 percent of the valid signatures the law requires, so election officials did not go on to check every signature", matches the sources file's California row (Elections Code 9030 and 9031: under 95 percent fails; 95 to 110 percent a full check).
- *CE-S19.* Each "stands" sentence matches the court's act: Affirmed leaves the judgment below in place; a tie, by the step 6 row's quote, "the decision of the lower Court stands"; a denied petition leaves the appeals court's ruling.
- *CE-S18.* "And sent back", "which the court enters as remanded": remand is the docket's word (28 U.S.C. 2106), named once, as ED5-3 named "Affirmed".
- *CE-S16.* The slashes the text names (step 4 for a direct initiative, steps 1 to 3 for a referral) equal the specs.
- *CE-S17 and NB-S7*, on the research lead's F9 and F8: I did not read the four constitutions myself. The text's claims match those facts as stated: Massachusetts, Ohio and Michigan vote first on a proposed law, and California sends an initiative straight to the ballot; in Massachusetts and Ohio a passed measure goes to the governor, in Michigan it becomes law without one.
- *CE-S15.* "Where the law asks" keeps Massachusetts's certification (Article XLVIII) apart from California, whose attorney general certifies nothing. One older point, not this pass's: step 2's law row cites Massachusetts and California only, while the rule says the steps follow four states. Whether Ohio's and Michigan's step 2 belongs to the attorney general is for the research lead to confirm; I did not read those laws, and it sends nothing back.
- *CE-S11, CE-S21.* The gloss of "injunction" and "Fell short of the vote the law requires", with a sentence naming the test, claim nothing past their sources.

**Words, last.** No em dash, en dash, straight apostrophe or listed word in Rules 11.10 and 11.11 (my scan). Every word is the editor's to set in its second read.

**Not looked at:** any capture (none was taken; `browsers.sh` said WAIT for the tracker designer). I did not rerun the generator or a build; the tracker designer's three strict builds and rerun proofs are theirs.


### Batch 2 (17:30 UTC): chapter 15 signed off, the R1 stage marks first; DF-10 and NB-S5 wait on R7 and R6 being applied (for the systems designer, the editor, the research lead, the design director and the main session)

Read from the systems designer's notes (17:24), the generator's CSS for the marks, the plates `s-15-22-*` to `s-15-25-*`, `s-15-1`, `s-15-6` and `s-15-15-correct` by script, and Rules 15.20 to 15.23 in `15-systems-graphics.json`. `phase3_ch15_build.py --check-only` (17:29): exit 0, 25 rules, 51 plates. Marks and facts first, words last. The two rulings the main session asked for are R6 and R7 above.

**R1, the stage marks: signed off as built.**
- *15.22, by markup.* 20 stages, each a `.n` number and no other mark; 0 `.wq` squares; the six `.sqm` stop squares are the only squares, each on a path that stops (stages 10, 12, 16, 17, 18, 19). The `.n` rule has no edge and no fill but the surface knockout, in the text's ink, bold, tabular, and the old `.br`/`.af` outline rule is gone, so every number looks alike on and off the spine.
- *Spine and paths by line alone.* The spine's `li` line is the subject ink at the subject weight; `.af` lines and the `.br` arrows are the context ink at the context weight.
- *Key.* Three numbered entries (1 on the line in the text's ink, 3 on a short gray arrow, 14 on the gray line), then the stop square and the return line, drawn with the plate's own parts. No "dark" or "lighter" anywhere on the plate (DF-5).
- *Forced colors.* The number in `CanvasText` on `Canvas`, the stop square and arrowheads in `CanvasText`, on the plate and in the key.
- *Failure plates.* `s-15-22-failure` draws six numbered stages in the same marks, and no square; `s-15-23-failure` and `s-15-23-correct` hold no stage mark.
- *15.23.* Stages print "Stage 3: Suspension of the rules" with no mark; steps keep chapter 11's numbers and names. The lead line says so (CE-S10). The designer's call to keep no spine-against-path difference on 15.23 stands: the stage names say it, and the plate sends the reader to 15.22.
- *The rule and specs.* 15.22's text now gives the reason, "since a circle, a ring or a square on a tracker marks a state (Rule 11.2)", and the specs call the stop square "the plate's only square".
- Not seen: no capture exists, so the knockout's look on both grounds, at 390 px and in forced colors is the design director's to judge once a browser is free.

**Structure: signed off.**
- *CE-M4.* The line in the text's ink runs 1, 2, 6, 7, 8, 13 (by markup: `st` 1, 2, 6, 7, 8; `end` 13). Stage 9, "Signed", is a path at the President beside 10 to 12, each going on to stage 13. The key's "A stage every enacted bill passes" is now true: an enacted bill is always presented (8) and numbered (13).
- *CE-M2.* Step 5 holds stages 3 to 7, and stages 3 to 5 each still send the bill to stage 6.
- *CE-M3, DF-1.* "A federal request's stages in the law" and "The law's stages for a federal rule".
- *CE-S6, DF-11.* Every stop line is the mark and one span of words; the "Then stage 13." lines are plain blocks.
- *CE-S7, DF-9.* Route names after each chip; Route FS's card reads its stage names from 15.22's list.

**Facts: signed off, each held to its source.**
- *CE-S1, ST-S6 (stage 2).* "a majority of the members who vote, 218 when all 435 House members vote or 51 when all 100 senators do. A tie fails, and in the Senate the Vice President may break it." Right, and on F3's row.
- *CE-S2 (stage 7)*, on F4: one text by amendment between the chambers or in conference.
- *CE-S3, CE-S4, DF-14.* Stage 8 named "Sent to the President"; reconciliation glossed in the atlas glossary's words; the Byrd rule as an objection the presiding officer sustains (2 U.S.C. 644, as batch 3 of round 5 held); stages 3, 5, 6, 8, 11, 14 and 16 open with who acts.
- *CE-S5, ST-S5, NB-S6 (stage 19).* "The Supreme Court's most recent decision to hold part of an Act of Congress unconstitutional, in its opinions through November 9, 2026": the research row's rule, scope and date, on F7. Marbury names the power without "repugnant". The holding stays in the syllabus's words.
- *ST-M2, CE-S8 (15.23's records request).* The 20 working days start when the right office receives the request, and no later than 10 days after any office the agency names for requests receives it: the paragraph of 5 U.S.C. 552(a)(6)(A) the statistics reader quoted, on F1. Steps 2 to 5 now say what the agency does inside that clock.
- *CE-S9.* "A rule issued without advance comment, such as an interim final rule, or guidance, ..." matches Rule 11.9. The designer's request for a 553(b)(B) row stands with the research lead.
- *ST-S7.* Stage 16 cites 801(a) of November 11 and 801(b) of November 12; the FA and FS cards widen their dates to the rows they cite.
- *CE-S11, CE-S12, CE-S23.* Motions, discovery and doctrine glossed; "the seven effect codes, ranks of direction and rough size with no measured amount", and "ordinal" gone from chapter 15's reader text (0 by search); "fewer" on 15.1, 15.6 and 15.15.
- *ST-S9.* Rows 11 and 17 say "as our first audit read it"; rows 47, 48 and 52 open "As we read it on October 21, 2026", the date of our V7.1 list.
- *DF-8.* "Seven", "Six", "Five", "Four", "Three" and "One reform entry"; no "1 entries" left.
- *NB-M1 (Rule 15.20's sentence).* It offers "the reforms whose own records name the loop on the drawing" and names an off-drawing target in words with its layer, as 14.144 does.
- *My R5 note.* `effect_rows` now prints a qualified code whole, and stops the build on a range or a second code; no plate moved (the designer's hashes).
- *Rule 01.9.* Unchanged by this pass: 39 examples, Elections and representation (D02) the largest at 8, under one in four (9.75).

**Waiting, not sent back.**
- **DF-10**, the rest: R7 ("Retrieved" for the 43 "read" dates, the source line's "the date we read it", 15.24's group line, and each law's version from F10). Stage 2's line shows why: "U.S. Constitution, Article I, Sections 3 and 5; House Rule XX, clause 1" carry no date or version of their own; under R7 each part names its version (House Rule XX in the 119th Congress's rules) and its retrieved date. 15.22's source line order (snapshot date with the atlas) is signed off.
- **NB-S5**: R6's sentence and its log row. I read both when the designer reports them (batch 3).

**Two older points, not this pass's, sending nothing back.** 15.23's ballot step 2 ("The attorney general's title and summary") rests on Massachusetts and California, as batch 1 notes for Rule 11.10. And the court block's "within 30 days" takes the same 28 U.S.C. 2107(c) suggestion as batch 1.

**Words, last.** No em dash, en dash, straight apostrophe or listed word in the chapter file or any `s-15-*` plate (my scan, styles excluded). The words are the editor's second read.

### Batch 3 (17:30 UTC): CE-S20 closed; chapter 11 signed off whole (for the tracker designer, the editor and the main session)

The editor's sentence (17:29) prints in `11-icons.json`, from `apply_systems_ch11.py` (lines 1889 and 1934): Rule 11.11's third paragraph says a sentence after the end words gives the reason, "No one asked the Supreme Court to review the case in the time the law allows.", and the "No petition" row now carries the appeals court's ruling, "The lower court's ruling stands." where one stands, and that sentence, with no day count. The slashes and their words now say the same thing (Rule 11.2). By script, the court plates' marks still equal the review commit's. Batch 1's one item is closed, and Rules 11.10 and 11.11 are signed off whole. Batch 1's two suggestions (28 U.S.C. 2107(c) beside "the 30 days the law allows", and a fine ring while the time runs) stay suggestions.

Next: R6 and R7 as the systems designer applies them, with the research lead's F10.

### Batch 4 (17:38 UTC): NB-S5 signed off; DF-10 signed off but two small items (for the systems designer, the research lead, the editor and the main session)

Read from the systems designer's notes (17:29 on), the research lead's F10 and F11, the source lines of `s-15-22-*` to `s-15-24-*` by script, and `phase3_ch15_build.py --check-only` (17:37: exit 0, 25 rules, 51 plates, 39 examples, D02 8). Facts and form here; the words wait on the editor's read, now running, and this sign-off holds unless the editor's words move a fact.

**NB-S5, R6: signed off.** Rule 15.24 prints the rule above the example: Reform R-28 "is the one an earlier drawing put on a route", with the fifth edition's and the atlas visual system's words and a link to row 41 of Rule 15.25. The generator holds it by script: of the 57 reconciliation rows exactly one names a reform and a route, row 41, and the build stops if that changes. The failure plate keeps R-28 and its one fault (the 60-vote path); the alt follows the plate's order. Rule 01.9 is unchanged (39 examples).

**DF-10, R7 with F10 and F11: signed off but two items.**
- *"Retrieved".* No law date on 15.22 to 15.24 says "read" any more (0 by script); 30, 7 and 20 say "retrieved", and the plates' own lines say "with the date we retrieved it". Failure plates carry no source dates.
- *The U.S. Code's version.* Each section prints "as in force on" its retrieval date. F10 makes that true and checkable: all 29 sections read the same in govinfo's 2024 edition ("Laws In Effect As Of Date: January 6, 2025") and in the Law Revision Counsel's release current through Public Law 119-142 of November 10, 2026, the last law enacted. That meets R7's items 2 and 3.
- *Other versions*, as each copy states them: House Rules XV and XX "as printed January 16, 2025"; the Senate's rules "revised to January 24, 2013"; the Federal Rules of Civil Procedure of December 1, 2025 and of Appellate Procedure of December 1, 2024; the Supreme Court's rules "effective March 16, 2026"; 16 CFR 2.34, 2025 edition; the two Public Laws with their approval dates; the California guide "revised January 2026"; the charters and joint rules with the dates their pages give.
- *Stage 19.* 52 U.S.C. 30116(d) is named in the stage's words and nowhere said to be "in force", as F10 cautions.
- *Stage 8.* Its "10 days, Sundays excepted" now cites Article I, Section 7, clause 2, retrieved November 11, 2026 (F11), which closes the editor's point.

**Sent back (DF-10), two items.**
1. *Stage 2's source line* gives "U.S. Constitution, Article I, Sections 3 and 5; House Rule XX, clause 1, as printed January 16, 2025" no date retrieved, so the line's last date, "retrieved November 16, 2026", reads as the Senate page's alone. Rule 13.6 gives each source its date retrieved, as every other stage line does: add each part's date from F3's rows.
2. *15.23's rule-making block* prints "Executive Order 12866 of September 30, 1993, as amended". F10 records the National Archives copy of the 1993 order and says the later amendments were "not traced", so "as amended" names a version we did not retrieve. Print the copy's version, as 15.24's FA card already does ("of September 30, 1993"). The editor may add that later orders amended it, which F10 states.

**Suggestions, not conditions.** 15.24's compact card could name Minnesota's copy as "2026 Minnesota Statutes", the version its page states (F10). "We read this reform because ..." now uses "read" in its plain sense on a plate whose law dates say "retrieved"; the editor may prefer "We chose this reform".

### Batch 5 (17:40 UTC): DF-10 closed (for the systems designer, the editor, the research lead and the main session)

Read on the plates by script after the editor's 17:40 changes; `phase3_ch15_build.py --check-only` exit 0 (25 rules, 51 plates, 39 examples).
- *Stage 2.* Each part now carries its own date: the Constitution's Sections 3 and 5, retrieved November 16, 2026; House Rule XX, clause 1, as printed January 16, 2025, retrieved November 16, 2026; the Senate page, retrieved November 16, 2026 (F3).
- *Executive Order 12866* reads "of September 30, 1993" on 15.23 and 15.24 alike; no "as amended" is left beside it. The one "as amended" on the plates is Portland's charter, "as amended November 8, 2022", the version its page states (F10).
- *15.23's court foot*, "title 28 of the U.S. Code, 2024 edition", names the edition we retrieved and claims no in-force date. That is right, since F10's 29 sections leave out 28 U.S.C. 1292, which the block draws on for an injunction's appeal.
- *Stage 5's joined cite*, "2 U.S.C. 641 and 644, as in force on November 14, 2026, the day we retrieved them", is true on F10.
- No law date reads "read" on 15.22 to 15.24 (0 by script).

DF-10 is signed off whole, and so is chapter 15's part of this pass, pending the editor's words and a capture of R1's marks.

## Calls

| call | reason |
|---|---|
| Rules 15.22 and 15.23 number each stage with a bold figure on its line and no shape; the stop square stays for a path that stops alone; 15.23 prints stages in words with no mark | Chapter 11 gives fill against outline and heavy against fine a state (Rules 11.2, 11.3, DR-108); a route's stage has an order and no state |
| Rule 14.143's line states the walk's direction at both ends, computed from the start and the signs, with "can" from a plausible step to the loop's close | The connection's general verb read after the supposition ran the wrong way (CE-M1); a chain is as sure as its least certain step |
| Rule 14.142's failure plate is S96 with the margin left out and nothing else changed: no latest label, plain source line, same scale; its caption names that one fault | One fault per failure plate (ruling (c)); the count of seven is what the rule asks for (ST-M1) |
| S96 and Rule 14.142 say what the band means in the zero-centered form and that it holds for each month alone; no expected-count figure prints | The band sits around zero; a count of chance passes assumes no month changed, which the data rule out (ST-S1, CE-S13) |
| S96's note 2 says where each named drop fell, private against government, same form for both months, no cause | A reader asks what fell; the split adds to each total and treats both months alike (ST-S2) |
| A ruling no one takes further keeps the steps after it under slashes at the trial court and at the appeals court; the square stays for settlement, dismissal and a denied petition | Call 4: an end by a ruling is not a stop; one meaning for the square (Rules 11.2, 11.3); Rule 11.8 and round 5's measure the Legislature passes do the same |
| Rule 15.24's worked example stays Reform R-28, chosen as the one reform an earlier drawing put on a route (Rule 15.25's row 41), with the rule printed | A rule that reads only the record of earlier drawings picks one reform for either side; the other candidate, R-25, is the same kind of reform (NB-S5) |
| A law's date on Rules 15.22 to 15.24 prints "Retrieved", with the version the copy states; ruling (e)'s "read" is replaced | Rule 13.6 and H04 name the part "the date retrieved"; chapters 11, 13 and 14 use it; "Checked" stays the atlas entry's date (DF-10) |
| Rule 14.144 draws Rule 13.5's pips with `pips_svg` and takes 15.20's route form and 15.16's grade form; D3-1973's "no pips" is replaced | Call 2 and DR-237: one mark for one property across chapters 13 to 15 (DF-3, DF-7) |

## Requests

- **To the research lead (R4b).** The source words for S96's line once note 2 names the private and government series (USPRIV, USGOVT, and CES9091000001 if the editor keeps the federal figure), from `fred-payrolls-by-sector.meta.json`, in Rule 13.6's order, so the complex examples maker can print them with ST-S8's release words.
- **To the systems designer (R5, not blocking).** If convenient in this pass, `effect_rows` prints a qualified code whole before its words, as Rule 15.16's spec says. No plate changes today.

## Tested

- Rulings (17:00 to 17:08 UTC), by script with `python3 -I`: Loops B4 and R10's connections, ends, signs, grades and delays, and each step's direction under the walk's start supposition; Reforms R-03, R-04, R-06, R-30 and R-38's effects, grades, routes and check dates; the count of qualified effect values in the model (38); October 2025's and February 2026's changes by sector from `fred-payrolls-by-sector.csv`; S96's spec (title, notes, source line, alt) and the guide's failure spec; the review build's placed failure figure for its source line; chapter 11's Rules 11.2 and 11.3 and Rule 11.10's step spec; Rule 13.5's and 13.3's specs; Rule 14.96's entry; `pips_svg`, `effect_rows`, `route_rows` and `grade_block` in the generators; the marks and key CSS of 15.22 and 15.23 in `phase3_ch15_build.py`; the text of `s-15-16-correct`, `s-15-20-correct`, `s-15-23-correct`, `s-14-144-correct` and `s-14-144-failure`.
- Batches 1 to 3 (17:23 to 17:30 UTC), by script: Rules 11.8, 11.10 and 11.11 whole from `11-icons.json`; the `data-icon` marks and drawings of `s-11-10-*`, `s-11-11-*` and `s-11-ballot-steps` against `8ace3dc6`; the sources file's court rows (steps 3, 5, 6) and California's sampling row; chapter 11's rule words for dashes and listed words. For chapter 15: the marks CSS and key CSS in `phase3_ch15_build.py`; mark counts on `s-15-22-*` and `s-15-23-*` (`.n`, `.sqm`, `.wq`, `.kn`, `st`, `br`, `af`); every stage's words and sources on 15.22; the text of 15.23, 15.24's card lines and 15.25's attributed rows; Rules 15.20 to 15.23 in the chapter file; "ordinal", dashes and listed words over the chapter file and every `s-15-*` plate; `phase3_ch15_build.py --check-only` (exit 0, 39 examples, D02 8); `v7-reconciliation-rows.json` for rows naming one reform's route (row 41 alone); "retrieved" and "read" counted in chapters 11, 13, 14 and 15.

## Not tested

- Batches 1 and 2: no capture of any changed plate exists (each owner found `browsers.sh` at WAIT), so marks were read from markup and CSS only; I opened no browser. I did not rerun either generator except chapter 15's `--check-only`, nor build the page; the owners' strict builds are theirs. The four constitutions, Title 28 and 5 U.S.C. 552 were not reread by me (the research lead's rows and F1 to F9).

- Rulings: no capture looked at and no browser opened; S66 (Rule 14.96) read from its entry only, not its drawing. The BLS technical note not reread by me (ledger P7-042 through the statistics report). Whether the 14.144 failure table can hold pips at 328 px is left to the maker.
