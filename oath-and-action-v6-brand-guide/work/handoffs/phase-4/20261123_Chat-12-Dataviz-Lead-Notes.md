# Chat 12 fix pass: data visualization lead's notes

Written November 23, 2026 by the data visualization lead, started 17:48:12 UTC (`date -u`). Every value below was read from `work/extract/atlas-v7-data.json` by my own scripts, `dv_rulings.py` and `dv_figures.py` in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/6f635cd3-ba95-5230-9089-d140c7cc1cf8/scratchpad/c12/fix/dataviz-lead/scripts/`, with their printouts beside them (`dv_rulings.out`, `dv_figures.out`). Values in brackets are today's, for checking only; the build reads each one from the model (R9 stands).

Chat 11c's rulings R1 to R18 stand unless a ruling here says otherwise. This chat's rulings continue the numbers, R19 to R28. No loop in the model is numbered R19 or higher, so the numbers do not collide with a loop ID.

## Routine calls

The main session numbers these.

- D4-xxx | R19: every home question prints its own stored short answer, hidden until pressed; the page loads with none pressed | The model holds one answer for each of the 16 pathways, so no question needs "the atlas holds none".
- D4-xxx | R20: R5's figure method tightened (whole figures, the year after the figure, one chip per claim per sentence at the sentence's end) and six figures in four answers print with no chip | The old method would stop the build on two answers and, on a third, link a figure to a claim from a different period.
- D4-xxx | R21: the loop page's confidence line takes the reform page's form, with chapter 15's disclosure under each panel | R12 and approved Rule 15.20.
- D4-xxx | R22: the name after each chip is the record's stored title (a connection's stored `name`), in quotation marks, never recased | One field per kind, and the pages already print Connection LE15 this way.
- D4-xxx | R23: Reform R-23's two readings take Rule 01.16's own labels, "One reading" and "The other reading" | Approved matching labels; our words, so DR-37 holds.
- D4-xxx | R27: the Register's loops column stays numbered loops, headed as such, with the reason in the note | The Register files connections, and a conceptual loop has no complete chain of them.
- D4-xxx | R29: Reform R-23's remedy splits at sentence 4; R-01's and R-22's contested remedies print whole, from a listed exception the test holds | No sentence boundary in either separates two readings of one question, and the record is Dustin's to change.

## Rulings

Landed in this file at the time the line at the end of this section gives. For the atlas engineer, the editor and the design director.

### R19. Each home question's answer (CD-M2, AX-4)

**The model holds an answer for every question.** Each of the 16 pathways stores its own `short_answer` [94 to 110 words]. None is empty, so no question needs words saying the atlas holds none. If a later model holds a pathway with an empty `short_answer`, the region prints the editor's line saying the atlas has no short answer for that question yet, and the build reports it; it never shows another question's answer.

| Pathway | Hub | Question (stored) | Answer, words | Parts it lights, `question:<PW>:parts` |
|---|---|---|---|---|
| PW01 | cost-of-living | Why did my rent go up? | 101 | Wealth, Your household, Technology |
| PW02 | cost-of-living | Why is my grocery bill higher? | 110 | Outside forces, Wealth, Checks, Your household |
| PW03 | cost-of-living | Why is my electric bill going up? | 107 | Wealth, Your household, Technology |
| PW04 | cost-of-living | Why did my home insurance premium go up? | 105 | Outside forces, Wealth, Your household |
| PW05 | health-and-care | Why is it hard to find an appointment? | 110 | Wealth, Checks, Your household, Technology |
| PW06 | health-and-care | Why can the same care produce different bills? | 108 | Wealth, Checks, Your household |
| PW07 | health-and-care | Why does childcare cost so much, and why can't I find an opening? | 100 | Wealth, Your household |
| PW08 | health-and-care | Why is it so hard to get help at home as I age or live with a disability? | 105 | Wealth, Your household |
| PW09 | work-and-security | Why isn't my pay keeping up with what my work produces? | 106 | Wealth, Your household |
| PW10 | work-and-security | How do taxes and benefit rules change what my household keeps? | 110 | Wealth, Your household |
| PW11 | work-and-security | What will I get from Social Security, and could the rules change before I retire? | 94 | Wealth, Checks, Your household |
| PW12 | community-services | Who makes sure my tap water is safe? | 106 | Checks, Your household |
| PW13 | community-services | Why is the repair on my street taking so long? | 104 | Outside forces, Checks, Your household |
| PW14 | community-services | Why does my child's school have less than schools in other districts? | 103 | Outside forces, Voice, Checks |
| PW15 | voice-and-power | Which election decides who represents me, and how can I influence the people who decide? | 103 | Outside forces, Voice, Elections, Checks |
| PW16 | voice-and-power | How do algorithms affect the prices I pay, my job, what I see online and the services I get? | 110 | Wealth, Voice, Checks, Technology |

The lit parts are R2's `question:<PW>:parts` (distinct `part(v)` over `model_refs.nodes`). The kit's `data-parts` on all 16 buttons in today's home export match this table (by script, 0 mismatches).

How the page carries them:

1. **One answer region a question,** drawn from that pathway's own `short_answer`, printed whole as stored (DR-37), its apostrophes typographic at render (fix brief section 2), with R20's claim chips. Each region is hidden until its question is pressed; the button names it with `aria-controls`. Each region's heading names its question with the stored `question` text after the editor's label (AX-4's form, "The short answer: Why can the same care produce different bills?", is the shape; the words are the editor's). One region shows at a time.
2. **The working page loads with no question pressed.** No button has `aria-pressed="true"`, no answer region shows, the status line is empty, every part box and card is in its full, unlit state, and "This question reaches here" (or the editor's CE9 words) prints nowhere. Pressing a question lights its parts by R6, shows its answer and writes the status line; pressing it again clears all three.
3. **The plates keep the pressed state.** The specs' `pressed_question: "PW06"` sets the frame state for the plates only, as today. The working export does not take it.
4. **Weight.** Sixteen answers add about 1,700 words and 17 claim disclosures (R20). If the engineer finds that too heavy, AX-4's fallback stands: one region, filled from the pressed pathway's stored answer by the page's script, labelled with its question, shown only while pressed. The words still come from the model at build time, carried in the page, never typed.
5. **For the atlas test:** for every pathway, pressing its button shows exactly one answer region whose stored text equals that pathway's `short_answer` (whitespace collapsed, apostrophes normalized), whose heading holds that pathway's `question`, and whose lit parts equal this table's. On load, none shows. A region holding another pathway's text is a FAIL.

### R20. The claim chips in the 16 answers (R5's last row, tightened)

R5 links a figure in stored text to "the claim that holds it: among the pathway's `claim_ids`, the one whose `claim` text holds the same figure and year". Run over all 16 answers, the kit's present pattern (percent figures only, with substring matching) would stop the build on PW01 (29% held by no claim) and PW14 (44% held by two), would miss every dollar figure and every "percent" written as a word, and on PW09 would link "about 2.1% a year since 1947" to Claim CL1500, whose 2.1% covers late 2019 to mid-2026. The method, made exact:

1. **Figures.** A dollar amount (`$1,240`, `$23.1 billion`), a number with `%` or the word "percent", or a number with "million", "billion" or "trillion". A year alone is not a figure.
2. **Whole figures only.** A claim holds a figure when its `claim` text holds the same characters with no digit, point, comma or dollar sign touching either end. "7%" is not held by "5.7%".
3. **The year.** The first four-digit year after the figure in the same sentence (System 1's sentence splitter). Where there is one, the claim must also hold that year.
4. **A tie** among the pathway's claims goes to the claim holding the most of that sentence's figures. Still tied, or no claim: no chip for that figure.
5. **Placement.** One chip a claim a sentence, set at the end of the sentence before its closing mark. For PW06 that is where the chip sits today, after "in 2022". Each claim's disclosure prints once, under its answer, by R5's form (`<pid>-claim-<id>`).

Run today, the method links 22 figures to 17 claims and leaves 6 figures in 4 answers with no claim:

| Pathway | Figure (year) | Claim |
|---|---|---|
| PW01 | 29% (2026); $1,240 (2020); $2,420 (2025) | none |
| PW01 | 7% (2026) | CL1105 |
| PW02 | 1.8% (2026) | CL1201 |
| PW03 | $23.1 billion | CL1243 |
| PW04 | 72% (2019); $201 | CL1168, one chip |
| PW05 | 92.3 million | CL1321 |
| PW06 | 254% (2022) | CL1340 |
| PW07 | $16.82 (2025); $13,184 (2025); 16 percent (2022) | CL1402; CL1404; CL1406 |
| PW08 | 61 percent (2022), $415 billion (2022) | CL1433, one chip |
| PW08 | $17.21 (2025) | CL1439 |
| PW09 | 2.1% (1947) | none: CL1500 holds 2.1% for late 2019 to mid-2026 |
| PW09 | 52.8% (2026) | CL1503 |
| PW10 | 7.65% | none |
| PW11 | 3.6 percent; 78 percent | CL1470; CL1471 |
| PW12 | 96% | CL1609 |
| PW13, PW16 | no figures | none |
| PW14 | 44%, 46% | CL1660, one chip |
| PW14 | 83% | none |
| PW15 | 9.4% | CL1700 |

Every linked claim's `confidence` is `documented`, `well-supported` or `plausible`, so each disclosure's grade takes its Rule 13.3 word.

**The six unlinked figures print as stored, with no chip of their own.** The page cannot invent a link, and the stored text cannot change. The build carries these six, by pathway and figure, as a known list: it stops on any other figure the method cannot link, and it stops if a listed figure starts to link, so the list stays true when the model changes. Where a sentence's chip follows an unlinked figure (PW01's $1,240 and $2,420 sit in Claim CL1105's sentence; CL1105 says the payment "nearly doubled" over the same years), the chip stands for the claim's own words, which its disclosure prints whole. The six go to Dustin as atlas V7.1 items (Requests, item 1).

### R21. The confidence line on the loop page (ST-1, R12)

Each reform panel on Loop R18's page (A14, A19), all three whether shown or not:

1. **Under the four effect rows,** before the routes, one line in the reform page's form and words (A12's `effects_confidence`, "Our atlas's confidence in these effects: “…”"), holding the stored `effects_confidence` quoted whole, once.

| Reform | Effects (stored) | `effects_confidence` (stored) | Remedy grade |
|---|---|---|---|
| R-11 | DQ +M precondition, GE +S, EP 0, EQ 0 | medium (design inference) | plausible, 39 words |
| R-15 | DQ +M, GE +M, EP +S, EQ 0 | medium (value); low (post-Slaughter durability) | plausible, 23 words |
| R-48 | DQ +M, GE +S, EP 0, EQ 0 | low (doctrine) | hypothesis, 25 words |

2. **Rule 15.20's disclosure under the panel,** closed on load, as approved chapter 15's `s-15-20-correct` holds it: its summary names the reform by chip; its body holds the remedy's evidence with its grade's display word, lowercase mid-sentence (R18's casing), and the stored `remedy_evidence.text` whole in quotation marks, then the stored `tradeoffs` whole [14, 12 and 14 words]. The confidence words print once, in the line above, so the disclosure does not repeat them (R12's "once").
3. Nothing sums, averages or colors across the four rows (R12). The remedy grade stays a word; it never changes the pips.
4. **For T7:** each of the three panels carries exactly one confidence line, after its fourth effect row, whose quoted text equals that reform's stored `effects_confidence` (apostrophes normalized), and one `details` element, closed on load, holding the stored remedy text whole, its grade's display word and the stored tradeoffs whole. A panel missing either is a FAIL. The same check passes A12 as built.

### R22. Which stored name follows each chip (CE1)

| Chip kind | The name that follows it |
|---|---|
| Variable | `nodes[k].title` |
| Connection | `links[k].name` |
| Loop | `loops[k].title` |
| Reform | `reforms[k].title`, whole, so Reform R-35 reads "Rejected option: term limits for legislators" |
| Issue | `issues[k].title` |
| Domain | `domains[].title` |
| Route | `routes.items[].name` |
| Rule change | `repairLog.rows[].rule` |
| Delivery case | `deliveryLog.rows[].what_was_done` |
| Claim | No name. The figure's own sentence names it, and its disclosure holds the stored `claim` whole (R5, R20) |

1. **The first time a page names a record,** in document order, the chip is followed by its name, as stored, in typographic quotation marks with typographic apostrophes, never recased or shortened. A comma sets the name off when the sentence runs on (CE8): "Start with Variable D2, “Presidential action without new legislation”, rising." Later mentions on the same page take the chip alone. A chip inside a heading or table row whose own text prints the name already counts as the first mention.
2. **A list of chips** joins with commas and "and", each with its name: "Reform R-24 “Paid family and medical leave insurance”, Reform R-25 “Full child tax credit for low-earning families”, Reform R-26 “Recession aid that starts automatically” and Reform R-31 “Childcare supply and pay for care workers” also aim here."
3. **In a table cell** (the loop index's grade column, R18), the name is the chip link's accessible description (`aria-describedby` to an element holding the stored name), as Rule 21.6's specification allows, so 23 rows stay readable.
4. **Loop R18's grade line is composed by connection,** replacing R11's last bullet for the loop page only. Each "X to Y" span in the stored `loops[k].evidence` names the one connection among the loop's own `links` that runs from X to Y, and the line prints that connection's chip, its name and the span's grade word: "Documented for Connection L14 “Presidential removals weaken watchdog agencies”; Plausible for Connection L15 “Independent watchdogs restrain unilateral action”" (the editor sets the words around it). The build stops if a span maps to no connection or to more than one, or if that connection's own `evidence` gives a different display word from the span's. Today both hold: L14 is documented and L15 plausible. The loop index keeps R18's form, with item 3's descriptions.
5. **Today's first mentions that need a name** (from CE1, checked against the model): Variable A4 “Households’ financial security”; Reforms R-24, R-25, R-26 and R-31 as in item 2; Loop R6 “Weak bargaining power and concentrated wealth reinforce each other”; Connections L14 and L15 as in item 4; on the Register, Connection L18 “Congressional expertise may reduce insider influence” and Connection L19 “Insider-tilted policy may weaken congressional expertise”. Where any of these is named earlier on its page, the earlier mention takes the name instead.
6. **For T1:** for each kind and ID on a page, the first chip in document order passes when the stored name (whitespace, quotation marks and apostrophes normalized) follows it within the same text run, separated by nothing but a space or a comma, or sits in the text of the row or heading that holds it, or is the text of its `aria-describedby` target. Claim chips and source IDs are exempt (R11). Anything else is a FAIL that names the chip.

### R23. The labels on Reform R-23's two readings (RP1)

- **"One reading" over the first block and "The other reading" over the second,** Rule 01.16's own matching labels, from approved chapter 01's plate. They are our words, so nothing stored changes (DR-37, D4-253).
- The blocks stay as R15 split them: sentences 1 to 3 (42 words: little job loss within the studied ranges, the 2019 study and its dispute, evidence strongest to about 60% of the local median wage) and sentence 4 (38 words: higher floors fall outside the studied range, and the Congressional Budget Office's 2019 median estimate of 1.3 million jobs lost and 1.3 million people lifted from poverty). I read the split again today: it separates the two readings and cuts neither, and the second block carries both halves of the Congressional Budget Office's estimate.
- Both labels take the same type token, weight, ink and position over their block, and neither carries an order word that ranks it. At 1440 px they sit level; stacked, each stays directly above its block.
- **For T10:** the labels sit outside the element that holds the stored text, so R15's rejoin still reads the stored text alone. T10 also checks that both labels are present, in this order, with the same class.

### R24. Two names for one part (RP4)

The plain name is the part's name. It is Dustin's (DR-35, DR-41), it heads the box and the card, and it is their accessible name. The second line is our atlas's own title for the part, read from the model at build, never typed:

| Part | Name | The atlas's title (field) |
|---|---|---|
| X | Outside forces | Outside drivers (`layers.core.regions[X].title`) |
| A | Wealth | Economic structure (`regions[A].title`) |
| B | Voice | Political inputs (`regions[B].title`) |
| C | Elections | Electoral competition (`regions[C].title`) |
| D | Checks | Governing institutions (`regions[D].title`) |
| E | Policy | Legitimacy (`regions[E].title`) |
| EC | Your household | How the economy reaches a household (`layers.economy.title`) |
| TC | Technology | Technology and its effects (`layers.technology.title`) |

The second line carries a label on every box at 1440 px and every card at 390 px, in the caption style, so a reader on a phone, far from any key, can tell which line is the name. The label speaks of "our atlas", as the pages do, rather than "the model" (the editor's words, as in "In our atlas: Outside drivers"). Counts, inks and lit states do not change.

### R25. "Flow" (DF2)

In the model, "flow" names a kind of variable: 9 of the 51 are flows (B1, C5, D6, EC2, EC5, EC6, EC7, EC12, TC6), an amount per period, and the glossary holds "Flow" beside "Stock". Approved chapter 15's "nine are flows" matches. The home drawing's arrows count something else: connections from a variable in one part to a variable in another [81 connections in 27 directed pairs; 37 more run inside parts; 118 in all].

So no word a reader meets calls an arrow, or what it counts, a "flow". The mark is an arrow, and its number counts connections: "5 connections from Wealth to Voice", "Other arrows between parts" (the editor's words; DF2's "Other connections between parts." is also faithful). This holds for chapter 21's rules, captions and alts, the home page's key and lines, and the design director's specs. The machine key `flow:P>Q` (R2) stays: no reader meets it, and renaming it would move the kit, the test and every atlas plate for nothing a reader sees.

### R26. Naming a sheet (DF6)

- **A domain's sheet is "the sheet for Domain D04",** with the Domain chip, and on the page's first mention its stored title after it (R22): Domain D04 “Congress, agencies and public services”. A bare "sheet D04" never prints in reader words, alts or frame labels.
- **The economy and technology sheets belong to layers,** which are not among Rule 13.9's ten kinds, so they take no chip and no code. They are named by the layer's stored title, as the Register's index already prints them: “How the economy reaches a household” and “Technology and its effects” (the editor sets the words around them). The codes EC and TC never print alone as a sheet's name. Variable chips such as Variable EC7 are unchanged.
- The machine keys (`sheet:D04:...`, `sheet:EC:...`) stay.

### R27. The Register's loops column (ST-2)

The column counts numbered loops, by R2's `sheet:<S>:loops`, and its whole-atlas cell counts `atlas:loops-numbered` [20]. That is the right count for the Register, which files connections: a conceptual loop has no complete chain of numbered connections to file. The model holds 23 loops, 20 numbered and 3 conceptual: B2 "Automatic benefits cushion economic shocks", B3 "New competitors can limit market power" and R9 "Taking part in a successful repair may support the next one". Of the twelve sheets, only D10 would read differently if all loops counted (4 numbered; R9 reaches it through Variable E2).

- The column's head reads "Numbered loops" (the design director's head; the index head's grade samples are unchanged).
- The note under the table gives the reason with both counts, each counted from the model, never typed: the 20 numbered loops, and the loop index's 23 with its 3 conceptual loops (the editor's words; ST-2's draft is faithful).
- **A new count key,** added to R2's table: `atlas:loops-conceptual` counts loops whose `closure` starts with "conceptual" [3]. The 23 takes `atlas:loops`, as now.

### R28. The locator's fill (DD11C-Q1)

The design director's reading stands, and the evidence reader found the built pages match it on every view. The locator fills the parts, by R2's `part()`, of the variables of the page's own record:

| Page | Its record's variables | Parts filled |
|---|---|---|
| Reform R-23 (A12) | Its target variables, and the `to` of any target connection [EC7, A4] | Wealth, Your household |
| Sheet for Domain D04 (A13) | Variables with `sheet(v)` = D04 [D1, D4, D5] | Checks |
| Sheet for Domain D10 (A18) | [B3, B4, E2, X2] | Outside forces, Voice, Policy |
| Loop R18 (A14, A19) | Its `chain` [D2, D4] | Checks |

- On a loop page the fill stays the loop's, whichever reform the reader chooses. Reform R-15 targets Connection L16, which reaches Variable E1 off the drawing; Rule 15.20 names that in words, and the locator does not change.
- A layer's sheet fills Your household or Technology.
- A page with no single record (the home, the loop index, How to read) fills no part.
- The fill is ink, never red (Rule 12.7, R10). A record in two or more parts fills each, which reads correctly against Rule 12.7's "current part".

Rulings R19 to R28 landed in this file by 17:55:41 UTC (`date -u` read straight after the write).

### R29. Where a contested remedy splits (PR-M2, part 3)

Written about 19:40 UTC, at the atlas engineer's ask (his run of the reform template over all 49 active reforms). First, a correction to R15: it said "only Reform R-23 has a contested remedy". The model holds three. R-23's `remedy_evidence.grade` is `contested`, and R-01's and R-22's are `plausible_contested`, which Rule 13.3 (R3) also prints as "Contested". I read each stored text by sentence (System 1's splitter):

| Reform | Sentences (words) | Ruling |
|---|---|---|
| R-23 | 8, 21, 13, 38 | **`remedy_split: 4`**, as R15 and R23 set: "One reading" over sentences 1 to 3, "The other reading" over sentence 4 |
| R-01 | 12, 38, 26 | **Whole.** Sentence 1 says more contested elections and more candidates are "plausible results". Sentence 2 says whether legislators become more moderate "is contested", then cites only evidence of little or conditional effect. Sentence 3 is the limitation. No sentence boundary separates two readings of one question: a split at 2 would set "more competition" against "no moderation" as if they disagreed, and they do not |
| R-22 | 3, 40, 12 | **Whole.** Both readings sit inside sentence 2 ("Two studies ... disagree on its effects on jobs and prices; an early evaluation by Reich ... reported no detectable job loss"), and only one of the two studies is named. A split would cut a sentence or label a limitation as a reading |

How the template carries it:

1. A contested remedy (stored grade `contested` or `plausible_contested`) needs `remedy_split` in its content file: a sentence number, as R15 counts it, or `"whole"`.
2. `"whole"` prints the stored text as one block, open on load, with its grade word "Contested" and its gloss as Reform R-23's page prints them, its source link after it, and no reading labels. It is accepted only for the reforms this ruling lists (today R-01 and R-22). The kit and the test carry that list, as they carry R20's.
3. A contested remedy with neither value, or with `"whole"` and not on the list, fails T10 and names the reform, so a new contested record waits for my reading.
4. T10 for a whole block: its text equals the stored text whole, whitespace collapsed.

The two stored texts that print whole also go to Dustin (Requests, item 3): R-22's names one side's study and not the other, and R-01's cites evidence on one side of the moderation question only. Under DR-93 a reader on the other side finds their evidence unnamed. The page prints what the record holds; the record is his to change.

## Contracts

- For the atlas engineer: R19's regions and load state; R20's figure method and its six-item known list; R21's line, disclosure and T7; R22's name table, composition and T1; R23's labels and T10; R27's key `atlas:loops-conceptual`; R28's fill.
- For the editor: R19's region heading and the empty-answer line; R22's name forms; R23's labels as given; R24's label; R25's and R26's terms; R27's note.
- For the design director: R24's second line with its label on box and card; R25's term in the specs; R27's head "Numbered loops".

## Sign-offs

S04 in chapter 16's frames (CD-S7) was not built this pass, so it has no sign-off (the main session, 19:28 UTC).

### Batch 1: A11 to A20, the build of 19:23:01 to 19:26:09 UTC. Signed at 19:40 UTC, with three items back

Inputs: the six working exports and their 20 PNGs in `work/build/exports/phase-4/` (written 19:23:04 to 19:25:02), the ten atlas plates in `work/build/app-kit/plates/` (19:26:09), and the main session's guide captures of the chapter 21 plates (`captures-fix/newsprint-1x/1440/`, 19:32 to 19:37). Scripts: `dv_signoff.py`, `dv_frames.py`, `dv_text.py` and `dv_tiles.py` in my scratch.

**Against the model and the rulings, by script.** The checks rebuild every expected value from `atlas-v7-data.json` by R2's methods and never read the engineer's test.
- **The exports** (`dv_signoff.py`): 567 checks, 0 FAIL.
  - Counts: every count with an R2 method matches the model (A11 139, A13 138, A14 4, A15 40). The home's 27 directed pairs sum to 81.
  - A11, on load: no question pressed, no part lit, an empty status line. Each of the 16 answer regions is hidden, is headed with its own question, and holds its pathway's stored `short_answer` whole. Its claim chips are exactly R20's table, each at its sentence's end, and each disclosure holds its stored claim. Every box and card carries R24's labelled title. No "flow" appears in reader text, and there is no red.
  - A12: red only on R-23's targets, EC7 and A4. "One reading" comes before its block and "The other reading" before the second. The first chips are followed by their R22 names. The confidence line is present, and the locator fills Wealth and Your household.
  - A13: the "Numbered loops" head, with `atlas:loops`, `atlas:loops-conceptual` and `atlas:loops-numbered` all counted. No bare "sheet D04" and no EC or TC printed alone. No red. R-35's confidence line, the names after L18 and L19, and the locator filling Checks.
  - A14: the grade line by connection (R22 item 4). Each of the three panels carries one confidence line after its fourth row, holding the stored words. Each has a closed disclosure holding the stored remedy text, its grade word and the stored tradeoffs (R21). `data-atlas-reads` reads `D2:rises L14 D4:falls L15 D2:rises` (R4), and the weakest mark is on L15 (R8). Seven red marks: R-11's D4, L14 and L15, and R-15's and R-48's L14 and L15, one figure a reform (R10). The locator fills Checks.
  - A15: 23 rows. The 37 variable chips in the grade column take their stored titles as descriptions (R22 item 3), and no stored grade spelling prints (R18).
- **The plate frames** (`dv_frames.py`, all 64 frames of A11 to A20): 88 checks, 0 FAIL.
  - A pressed frame presses PW06 alone, lights Wealth, Checks and Your household, draws one answer under PW06's question, and names those three parts in its status line. A20's frame opens CL1340, and A17's draws 51 pills.
  - The drawing symbols carry red on R-23's EC7 and A4 and, with R-11 chosen, on D4, L14 and L15. No home or Register frame carries red.
  - The locators read A12 Wealth and Your household, A13 Checks, A14 Checks. A18's frames are crops without the locator, so R28's D10 row is not shown there.

**By eye.**
- **Exports viewed:**
  - A11: 1440 light (both bands), 1440 dark (the drawing), 390 light (whole).
  - A12: 1440 light (top and evidence bands), 1440 dark (top), 390 light (whole).
  - A13: 1440 light and dark (the index), 1440 light (layer rows and note), 390 light (the index's first cards).
  - A14: 1440 light (three bands), the drawing at twice size in light and dark, 390 light and dark (the first 5,400 px).
  - A15: 1440 light (top), 390 light (the first 5,400 px).
  - A16: 1440 light (two bands).
- **Guide plates viewed** (1440 viewport): `s-21-1-correct`, `s-21-home` (its first band: 1440 light, 390 light, 390 dark) and `s-21-5-correct`.
- **What I confirmed in them:** the loop's patterned red target with its case dashes in light and none on Charcoal (R14), CD-S10's solid run from L15's last corner into its arrowhead (signed: the dashes carry the run, and the shaft is about as long as the 28 px lead-in at the tail), CR-9's whole-pixel lines, the range pips on R-23's Economic performance (R12), the readings set level with matching labels (R23), the main circuit and the other arrows in their inks in both themes (R6), the 390 cards (R7), and the unpressed home on load with the pressed state kept in the plates (R19).

**Signed off:** A11, A14, A16, A17, A19 and A20 as built. A12, A13 and A15 are signed off for their data. Each also carries a fault sent back below. None of the three changes a value; each changes how a value reads.

**Sent back** (Requests, items 4 to 8):
1. The guide's plates draw the wordmark's ampersand black in every 390 px masthead, and invisible on Charcoal: 25 uses in 15 plates of chapters 20 and 21 (item 4, Engineer W). This is the locked identity, so it comes first.
2. A13's phone cards put the five grade counts beside "Issue records" with nothing saying they count connections (item 5).
3. CR-3's single words in A15's cells, A13's "none filed" and A12's phone lines (item 6).
4. A12's confidence line sits above its rows, where A13 and A14 set it below (item 7, a Should).
5. A tag's hyphen in the data-label type renders spaced (item 8, low).

### Batch 2: A12, A13 and A15 whole, and the sprite fix, on Engineer W's final rebuild (19:56 to 20:01 UTC). Signed at 20:15 UTC

Inputs: the exports written 19:58:04 to 20:00:01, the plates at 20:01:09, and Engineer W's strict build `fix/engineer-w/fx8/guide.html` (20:01:27).

- **By script, again from the model:** `dv_signoff.py` gives 567 checks and 0 FAIL on the six exports. `dv_frames.py` gives 86 checks and 0 FAIL on the plate frames. Against batch 1, A12's text moved one line, the confidence line, which now follows the fourth effect row. A13's index gained 13 "Connections by grade" groups, one a row: ten domains, two layers and the whole atlas.
- **By eye:**
  - A12 at 1440 light (effects and routes) and 390 light and dark (whole). The confidence line follows the rows at both widths, as A13 and A14 set it. "also aim here" is held on one line, and so is "small negative".
  - A13 at 1440 light (the index and note) and 390 light and dark (the first three cards). "none filed" sits on one line. Each phone card sets its five grade counts under "Connections by grade", each with its line sample, apart from the structure counts. The sheet titles break in balance.
  - A15 at 1440 light (the first eleven rows) and 390 light (the first five cards). The titles and "How it closes" cells break in balance, with no word alone.
- **The sprite fix:** the scoped rule now reads `.oa-masthead-amp:where(.oa-app-art *,:not(:root *))`. I opened one browser (after `browsers.sh` printed "OK to open one") on the strict build. I shot the 390 px frames of `s-21-home` (dark), `s-21-loop` (light and dark), `s-21-1-correct` (390 light, views open) and `s-20-1-correct` (light and dark). The ampersand paints red in every one, Charcoal included (`b3/amp-sheet.png` in my scratch).

**Signed off:** A12 and A13 whole. A15 is signed off with one low item back (Requests, item 10): at 390 px a chip at a line's end can leave its semicolon to open the next line. Loop R4a's card shows it ("... to Variable C4 / ; Plausible for"). The loop index has nine chips followed by a semicolon (C4, A1, C2, C3, C3, C4, D2, D4, D4). Batch 1's items 4 to 7 are answered and built, and item 8 (the hyphen in the tags) stays with the design director.

## Done

- CD-M2 and AX-4: ruled (R19, R20).
- ST-1: ruled (R21).
- CE1: ruled (R22).
- RP1: ruled (R23).
- RP4: ruled (R24).
- DF2: ruled (R25).
- DF6: ruled (R26).
- ST-2: ruled (R27).
- DD11C-Q1: ruled (R28); the row can close.
- Sign-off of the changed atlas views, batch 1: A11, A14, A16, A17, A19 and A20 signed off; A12, A13 and A15 signed off for their data, with items 4 to 8 under Requests sent back.
- PR-M2, part 3 (the contested remedies' splits): ruled (R29); R-23 splits at sentence 4, R-01 and R-22 print whole, and R15's "only R-23" is corrected.
- CD-S7 (S04 in chapter 16): not built this pass, so no sign-off (main session, 19:28 UTC).
- Batch 2 (20:15 UTC): A12 and A13 signed off whole, A15 with one low item (Requests, item 10); the plates' red ampersand confirmed at 390 px in light and on Charcoal.

## Requests

1. **Main session, atlas V7.1 items for Dustin (section 3.8's issue rows).** Six figures in four stored short answers are held by no claim in their pathway, so the pages print them without a link (R20): PW01's "29%" (asking rents, early 2026 against 2020), "$1,240" and "$2,420" (the monthly payment, 2020 and 2025; Claim CL1105 says "nearly doubled" in words); PW09's "about 2.1% a year since 1947" (Claim CL1500 holds 2.1% for late 2019 to mid-2026, a different period, so the answer and the claim disagree); PW10's "7.65%" (the payroll tax rate); PW14's "83%" (the property tax share of local school revenue). Each wants a claim, or a correction, in the next model.
2. **Atlas engineer, `tools/atlas_figures.py` around line 608:** replace the percent-only pattern and its substring match with R20's method, and carry R20's six-item list. Without it, the 16-answer page stops on PW01 and PW14 and links PW09's 2.1% to the wrong period. **Answered** (his notes, AX-4: R20's table to the letter; batch 1 confirms it).
3. **Main session, atlas V7.1 items for Dustin (R29):** two contested remedies print whole because their stored texts hold one side's evidence only. Reform R-22's says two studies of California's fast-food wage "disagree" and names only the one that found no detectable job loss. Reform R-01's says the moderation effect "is contested" and cites only evidence of little or conditional effect. Each wants the other side's source named in the next model (DR-93).
4. **Engineer W, `work/build/app-kit/oa-app.mjs`, PR-M1's frame scoping (batch 1; the locked identity):** in the strict build (`fix/engineer-atlas/guide.html`, 19:26:27) the ampersand's rule is scoped as `.oa-masthead-amp:where(.oa-app-art *)`. The 24 px wordmark is drawn by `<use href="#oa-app-id-chapter-18-wordmark-24px">`, and its symbol sits in the sprite outside `.oa-app-art`, so the selector never matches the symbol's path. The ampersand falls back to black, and on a Charcoal frame it disappears. This is seen in the main session's captures: `s-21-home`'s 390 light and 390 dark frames, and `s-21-1-correct`'s 390 frame. By script, 25 uses in 15 plates: `s-20-opener`, `s-20-1`, `-2`, `-5`, `-6`, `-7`, `-8-correct`, `s-21-opener`, `s-21-home`, `s-21-1-correct`, `s-21-reform`, `s-21-7-correct`, `s-21-register`, `s-21-loop` and `s-21-14-correct`. The exports themselves draw it red. Fix: let the scope reach the plates' symbol sprite (for example `:where(.oa-app-art *, <the sprite's container> *)`, or write the sprite inside an `.oa-app-art` element), then recapture. Add a guide check plant: a kit symbol whose scoped rule no longer reaches it.
5. **Atlas engineer and editor, `renderers/atlas-page.mjs` and A13's words, the Register's phone cards (batch 1; a reading fault):** at 390 px each card sets "Issue records: 20" and then "Documented: 2", "Well supported: 2" and the rest in two columns. Nothing says those five count connections, and issue records carry grades of their own (D04's are 11 documented, 6 well supported and 3 plausible, R2), so a reader can take "Documented: 2" for two documented issue records. At 1440 px the column heads carry the line samples, which say "connections". Fix: set the five grade counts as their own group after the structure counts, under a label in the editor's words (such as "Its connections by grade"), with each count's line sample before its word as the key above shows it.
6. **Atlas engineer, `renderers/atlas-page.mjs` and `plates/atlas-page.css`, CR-3 (batch 1):** single words still end lines.
   - A15, at 1440 and 390: the "How it closes" cells ("closed: every step is a numbered / connection", most rows) and some titles ("... reinforce each / other", "... outside / expertise").
   - A13, 1440 index: "none / filed" in both layer rows.
   - A13, 390 cards: sheet titles ("... public / information", "... public / services", "... equal / justice").
   - A12, 390: the tag line's "also aim / here" and the effect words "no expected effect to small / negative".
   - Fix: `text-wrap: balance` on the loop index's cells and the cards' titles, `.wa-one` on "none filed", and a held "also aim here" and last pair of effect words (`ws-nb`), as the tag lines already hold a name's last word.
7. **Atlas engineer, with the design director, A12 (a Should, R12 and R21):** the reform page prints "Our atlas’s confidence in these effects" in the "What it would change" band, above the four rows. The loop panels and the Register's rejected option print it after the fourth row, as R12 sets. Fix: print it after the rows on A12 too, so the line sits in one place on every page.
8. **Design director, low:** in the tags' data-label type a stored hyphen renders with space around it ("low - earning" in Reform R-25's name on A12, at 1440 and 390). It looks like the type token's figure settings. Fix: say whether stored names inside tags should take `font-variant-numeric: normal`, or accept it.
9. **Atlas engineer, for the register row (PR-M2):** Reform R-25's partner page draws its target Connection LE14 in ink. T6 fails it, so no page ships that way. Until the other target shapes land, the figure step could print the `where_none` words for a target set it cannot draw wholly red, rather than a drawing with a target missing its red.
10. **Atlas engineer, A15 at 390 px, low (batch 2):** the grade cells hold a chip and the semicolon after it apart, so a line can open on ";" (Loop R4a's card). Fix: hold each chip with the punctuation that follows it (`ws-nb`), as the tag lines hold a name's last word and its mark.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

None of mine. Every code assigned to me is ruled under "Done".

## Tested

- The 16 pathways, their stored questions, hubs and answer lengths, and each one's lit parts by R2's `part()`, by `dv_rulings.py`.
- The kit's `data-parts` on all 16 buttons in `20261122_Atlas-Home-Page.html` against those parts: 0 mismatches.
- R20's figure method over all 16 answers, by `dv_figures.py`; the claims it links and their stored `confidence` and `period`.
- The three Loop R18 reforms (by `reforms[k].loops`), their stored effects, `effects_confidence`, remedy grades and lengths, and tradeoffs lengths; Reform R-23's for comparison.
- Every stored name R22 quotes; Reform R-23's targets and the four other active reforms aimed at Variable A4; Reform R-35's targets.
- Reform R-23's remedy text split into its four sentences (8, 21, 13 and 38 words).
- The part titles R24 quotes, from `layers`.
- The node types (9 flows) and the connection counts inside and between parts (37, 81, 27 pairs).
- The domain titles, and the Register export's index row names for the two layer sheets.
- The 23 loops, 20 numbered and 3 conceptual, and each sheet's numbered and all-loop counts.
- The locator's parts for A12, A13, A14 and A18's records.
- Approved chapter 15's `s-15-20-correct` disclosure contents, read from its specimen file, and chapter 01's `s-01-16-correct.html`, which holds the labels "One reading" and "The other reading".

- Batch 1: `dv_signoff.py` over the six exports (567 checks, 0 FAIL) and `dv_frames.py` over the 64 plate frames (88 checks, 0 FAIL), both rebuilding the expected values from the model. The PNGs and plate captures listed under batch 1 were viewed by eye, with the loop drawing at twice size in both themes.
- The three contested remedies (R-01, R-22, R-23) read by sentence for R29.
- The wordmark fault: the scoped rule and the 25 symbol uses counted by script in the 19:26:27 strict build's `guide.html`, and the black ampersand seen in the main session's captures.

- Batch 2: both scripts on the 19:58 to 20:01 build, the text diffs against batch 1, the PNG crops named under batch 2, and one browser on `fix/engineer-w/fx8/guide.html` shooting seven 390 px masthead frames (`scripts/dv_amp.cjs`).

## Not tested

- Batch 2 did not view A13's and A15's lower bands, or the plate captures of A12, A13 and A15 (still being captured at 20:09). A15 has no dark export.
- Batch 1 opened no browser. The sign-off reads the kit's exported PNGs and the main session's guide captures; I pressed no question, chose no reform and stepped no loop myself, so the scripted states are read from the frames' markup and the engineer's own walk.
- By eye I did not view: A11's 390 dark export; A12's 390 dark; A13's 1440 dark below the index and both 390 exports below the index's first cards; A14's 1440 dark outside the drawing; A15's and A16's lower bands; any plate capture at 390, 1024 or 360 viewports or on Charcoal or in gray (they were still being captured at 19:37); `s-21-reform`, `-register`, `-loop` and the other s-21 plates beyond the three named.
- I did not check whether any atlas page prints a rule change or delivery case chip today; R22 names their fields for when one does.
