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

## Contracts

- For the atlas engineer: R19's regions and load state; R20's figure method and its six-item known list; R21's line, disclosure and T7; R22's name table, composition and T1; R23's labels and T10; R27's key `atlas:loops-conceptual`; R28's fill.
- For the editor: R19's region heading and the empty-answer line; R22's name forms; R23's labels as given; R24's label; R25's and R26's terms; R27's note.
- For the design director: R24's second line with its label on box and card; R25's term in the specs; R27's head "Numbered loops".

## Sign-offs

To come, in numbered batches, as the views and S04's frames land.

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

## Requests

1. **Main session, atlas V7.1 items for Dustin (section 3.8's issue rows).** Six figures in four stored short answers are held by no claim in their pathway, so the pages print them without a link (R20): PW01's "29%" (asking rents, early 2026 against 2020), "$1,240" and "$2,420" (the monthly payment, 2020 and 2025; Claim CL1105 says "nearly doubled" in words); PW09's "about 2.1% a year since 1947" (Claim CL1500 holds 2.1% for late 2019 to mid-2026, a different period, so the answer and the claim disagree); PW10's "7.65%" (the payroll tax rate); PW14's "83%" (the property tax share of local school revenue). Each wants a claim, or a correction, in the next model.
2. **Atlas engineer, `tools/atlas_figures.py` around line 608:** replace the percent-only pattern and its substring match with R20's method, and carry R20's six-item list. Without it, the 16-answer page stops on PW01 and PW14 and links PW09's 2.1% to the wrong period.

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

## Not tested

- No page or plate was built or opened in a browser for these rulings; sign-offs follow as the views land.
- I did not check whether any atlas page prints a rule change or delivery case chip today; R22 names their fields for when one does.
