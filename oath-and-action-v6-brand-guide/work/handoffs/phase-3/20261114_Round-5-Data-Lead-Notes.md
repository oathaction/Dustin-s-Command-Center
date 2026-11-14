# Round 5 data lead notes

Oath & Action Edition 06, Phase 3, round 5. Written by the data visualization and systems lead (`oa-dataviz-systems-lead`) under `work/handoffs/phase-3/20261114_Phase-3-Round-5-Brief.md`. Started 01:40 UTC, November 14, 2026.

## Status

- 01:54 UTC. **All seven rulings, (a) to (g), are posted.** Owners may draw. Sign-offs follow as items land. Requests R-1 to R-3 to the research lead and E-1 to E-3 to the engineer.
- 01:41 UTC. Started.

## Summary

Every owner reads "Rulings" directly. In short:

- **(a) The selection guide.** All 127 forms, each once, under its plan family (the coverage plan's own rule: "Each form sits in one family"). Within a question, Core, then Extended, then Reference, then Avoid; inside a tier, rule order. An avoid form says "Avoid" in words and carries one diagonal stroke across its picture, never red. Pictures draw shapes only, in the neutral chart inks, with no numbers, words or party colors.
- **(b) The palette specification.** Rule 14.5's four palettes (sequential, diverging pair B, the four group inks, magnitude) and the grade line code, on Newsprint and Charcoal, with the Newsprint values measured on White as printed paper and no swatch on Prussian. Every number from the tokens by script with round 0's methods.
- **(c) Example 1.** All 57 months, January 2022 to September 2026 (DR-64 forbids a window that starts at the inauguration). The margin as a band of plus or minus 122,000 around zero; the two drops past it in Charcoal at the subject weight, never red, since red never codes a loss (Rule 14.6).
- **(d) Examples 2 and 3.** Loop B4's three steps, then Loop R10's four, each in the atlas's order, so the drawn step numbers hold. R-06, R-30 and R-38 in ID order, codes printed whole, no total, with the atlas's own sentence that codes are never added.
- **(e), (f), (g).** 15.22 draws the path to a public law first. 15.25 orders rows by what a wrong copy could mislead. Trackers mark a step only on an official dated record. Rule 01.9 holds in chapters 14 and 15.

## Rulings

Every figure here was read by script (`python3 -I`) from `work/extract/atlas-v7-data.json` (snapshot October 15, 2026), `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`, `work/build/tokens/tokens.json` (release 6.0.0-gate3.3), `work/build/chart-kit/specs/s14.json`, `work/build/data/fred-payrolls-monthly-change.csv` with its sidecar, the entries `14-005.json` to `14-007.json`, `14-example-log.json` and `phase3_ch15_build.py`'s log calls. Each selection rule was read from both sides (DR-93, DR-124), with R-01 and R-02 treated as every other reform (DR-223).

### (a) The selection guide (for the selection guide maker, the engineer, the accessibility lead and the editor)

**What it lists.** Every one of the plan file's 127 `forms` rows, once. By script: 127 distinct rules; 56 Core, 41 Extended (one of them written "Extended, interactive", Rule 14.130), 22 Reference, 8 Avoid; every row's tier agrees with its entry file's `tier`. The 16 questions are the plan's group titles for groups 2 to 17, word for word as the chapter prints them, in group order.

**One form, one place.** No form answers two questions on this plate. The coverage plan settled it before Phase 3 (section 2, approved under DR-62 and DR-63): "Each form sits in one family: the fan chart under uncertainty, the bullet graph under gauges and indicators, the shift-arrow map under maps." A second listing would also break R5-2's count of one, and a "see also" link would add links the accessibility lead's 127 do not hold. Two pairs of forms share one specimen, S06 (14.76 Scenario directions and 14.127 Comparison matrix) and S13 (14.34 Small-multiple area sparklines and 14.128 Sparkline table). Each pair is two forms with two entries, so each form gets its own picture and link under its own family.

**Order within a question.**
1. By tier: Core, then Extended, then Reference, then Avoid. The tier is the plan's first word before any comma, so 14.130 sorts and prints as Extended; its entry already says "extended".
2. Inside a tier, by rule number.

Why: a reader who opens the guide wants the form the studio builds and supports first; rule order inside a family follows the build rounds, not that preference. By script, this moves forms in four families only: Change over time (14.31 Line field, Extended, now follows the nine Core forms), Flow (14.112 Journey map, Core, now leads), Tables and plain words (14.129 and 14.130, Extended, now follow the eight Core forms) and Infographics (14.141 Social data card, Core, now precedes 14.139 and 14.140). I suggest each item print its rule number as live text before its name, in the guide's rule-number style, so a reader who sees 14.112 before 14.110 knows why; the editor and design director decide.

**Tier in words.** Each tier's run under a question is labeled once with its word (Core, Extended, Reference, Avoid), and each item also carries its tier in its accessible name, since a link read alone must say it (the accessibility lead sets the exact name). Tier words come from the plan by script, never typed by hand.

**An avoid form.** Eight forms: 14.24 Radar chart, 14.45 Streamgraph, 14.57 3D pie or bar, 14.73 Dual-axis line, 14.84 Rose chart, 14.91 Gauge, 14.92 Thermometer, 14.124 Party-colored map or red and blue scale.
- Words first: "Avoid" printed beside the name in text, so it survives grayscale, one-ink print and a screen reader.
- Its mark: the picture drawn whole, in the same symbols and stroke as every other, so a reader recognizes the form they were about to choose, with one straight diagonal rule across the picture's frame, lower left to upper right, in the text ink at the pictures' stroke weight. The rule crosses the shape and hides none of it.
- No red. Rule 05.3 gives a view one working red, in the order error, step, named point. An avoid form is none of these, and Rule 14.6 says red that codes a group reads as a warning about it. No hatch either: the hatch is Stone's group mark (DR-236).
- 14.124's picture takes the tile map's shape in the guide's one ink with the avoid rule. DR-255's literal red and blue cover sketch 14.124's misleading half alone, under its do-not-publish bar. This plate is not that sketch, so DR-64's "no red and blue on any election graphic" applies in full. The name says what is avoided.

**What a picture holds.** A shape, never data: no number, word, axis value, state, party mark or color scale inside a picture, so the plate states no figure, logs no example, needs no source line and needs no Illustrative label. Inks: the neutral chart roles only (the text or subject ink for the shape's main stroke, the context ink, the light fill, the track and the gridline ink). A form whose identity is one highlighted mark (14.30, 14.31) shows it by the subject weight against the context weight. A form that shows groups or two directions shows them by fill against outline, the kit's hatch where a fourth group needs it, and position from a center line, never by the group, diverging or sequential palettes, which the palette specification shows. The design director judges the look; these are the data limits.

**Checks I will read at sign-off**, by script: 127 links, each `form_id` or rule once; each link's target is that form's entry anchor; each tier word equals the plan's first word and the entry's `tier`; no picture holds `<text>`; no picture uses a fill or stroke outside the roles above; no red anywhere on the plate.

### (b) The palette specification's content (for the engineer, the design director and the editor)

**Which palettes.** The four Rule 14.5 names, in its order, each with every step, its token name and value, and its label ink on that step:

| Palette | Steps | Tokens |
|---|---|---|
| Sequential Verdigris | 5 | `oa.chart.color.sequential.fill.step1` to `step5`, `.label.step1` to `step5`, and `.outline` |
| Diverging, pair B | 5, step 3 the midpoint | `oa.chart.color.diverging.fill.step1` to `step5` and `.label.step1` to `step5` |
| Groups, four inks | 4, in the order Charcoal, Verdigris, Prussian, Stone; on Charcoal, Newsprint, Verdigris, Prussian lifted 62 percent, Stone | `oa.chart.color.categorical.fill.group1` to `group4`, `.label.group1` to `group3`, `.labelBeside.group4`, the hatch tokens, and each group's marker (circle, square, triangle, diamond) |
| Magnitude, Stone | 4 | `oa.chart.color.magnitude.fill.step1` to `step4` and `.label.step1` to `step4` |

Then the grade line code: the `oa.chart.grade` stroke styles at 2 px and 3 px on both grounds, each with its grade word (Rule 13.3) and the 7 px record square before "Documented", as Rule 13.4 draws them.

The role inks (subject, context, light fill, track, band, ghost, point red and its keyline) stay with Rule 05.7 and chapter 26's table. One job per plate: Rule 14.5 names four palettes, and chapter 26 already lists every token.

**Which grounds.**
- **Newsprint and Charcoal**, every palette, every step. These are the tokens' `chartGrounds`; chart tokens exist for these two only.
- **White**, measured only: the Newsprint values' contrast on White, labeled as the paper a printed report uses. Round 0 ruled that a printed report prints the Newsprint values on white paper and has no tokens of its own.
- **Prussian**, no swatches. One line of text says a chart in a Prussian panel sits on its own Newsprint or Charcoal plate, with the measured reason read by the generator (round 0 measured the four group inks at 1.00 to 2.80 to 1 on Prussian), and that red never sits on Prussian (Rule 05.3). Swatches on Prussian would read as approval.

**Which proofs**, all computed by the generator from `tokens.json`, never typed:
1. **Contrast** by the WCAG 2.2 formula: each fill against its ground (3 to 1 is the bar for a mark a reader needs) and each label ink on its own step (4.5 to 1). Every ratio prints to two decimals as "4.61 to 1", and pass or fail is judged on the unrounded value. A light sequential or magnitude step under 3 to 1 against its ground prints its measured value and names what carries it (its edge or outline token, or its printed value), as the kit draws it. No ratio is rounded up to pass.
2. **Grayscale**: each palette's steps through the CSS `grayscale(1)` filter, the one a browser applies, with each step's OKLab lightness printed under it. Ordered neighbors at least 0.08 apart; groups a key separates by fill alone at least 0.10 apart, with Verdigris and Stone exempt because Stone carries the hatch (round 0, D2-95).
3. **Three color-vision proofs**: protanopia, deuteranopia and tritanopia, Machado, Oliveira and Fernandes (2009) at severity 1.0 in linear RGB, round 0's method, with round 0's neighbor measure and threshold printed under each row. The note names the method and says it models full dichromacy only.

Use round 0's functions in `work/boards/phase-3/round-0/palettes/build_palette_proofs.py` (request E-1), so the plate's numbers equal board 1's, which Dustin approved under DR-236.

The plate prints the token release it was written from ("Tokens 6.0.0-gate3.3"), so a later release that changes a value rewrites the plate and a reader can see which release it shows.

**Words for each job.** Drafts for the editor, who sets the final words under chapter 02's rules; each states the job, then when to choose it:
- *Sequential.* "One measure from low to high, such as a rate in each state. Low values sit closest to the ground and high values farthest from it, on Newsprint and on Charcoal."
- *Diverging, pair B.* "A measure with a middle that means something, such as a change above or below zero. Prussian runs one way and Verdigris the other, and the middle step sits close to the ground. A sign or a boxed arrow says which way each side runs. Never for parties (Rule 14.7)."
- *Groups.* "Up to four named groups with no order. Charcoal, Verdigris, Prussian, then Stone with its hatch, always in that order. Each group carries its name on the chart, and each line ends on its own marker. Past four groups, split the chart into small multiples, or show one group in ink and the rest in gray."
- *Magnitude.* "Size in ordered steps with no direction, where a hue would add a meaning the data does not hold. The fan chart's bands, the confidence band and the bullet graph's ranges use it, and so do phone tile maps that show how far each state moved." (By script, specs S10, S58, S59 and S64 use the magnitude roles today; the generator may list them from the specs.)
- *Grade line code.* "How sure the evidence is, drawn in the line itself, separate from color: solid for documented and well supported, dashed for plausible, dash-dot for contested, dotted for a hypothesis."

### (c) Complex example 1, S14 in full (for the complex examples maker, the engineer and the editor)

**Months.** All 57 in S14's frozen file, January 2022 to September 2026, the window S14 and the second jobs chart share, printed with its reason in S14's words ("so they hold three full years before the January 2025 inauguration and every month since"). DR-64 decides it: charts shown together share one window, and no chart splits a period at an inauguration date. A window from January 2025, where all seven drops sit, would start at an inauguration; any other cut would break the shared window. S14's first note stays: the averages for January and February 2022 draw on November and December 2021, months the chart does not show.

**Preliminary months.** August and September 2026 (`status` "preliminary", by script), drawn as S14 draws them, so the chapter teaches one convention: hatched columns, and the three-month average dashed where it includes a preliminary month. A note says the Bureau revises each month's first estimate in its next two monthly reports and that a yearly benchmark can move earlier months, and that the margin band does not show how far a revision may move a month.

**The margin.** A band from minus 122,000 to plus 122,000 jobs around the zero line, across all 57 months, behind the columns. The figure is the Bureau's 90 percent interval for one month's change in its survey of employers, from the Employment Situation technical note, October 2026 release, retrieved November 11, 2026 (ledger P7-042), as S14's `with_margin` source line already prints. Ink: Stone magnitude step 1 with 1 px context-ink edges through the kit's shared band part, the treatment S58's confidence band takes (RB-D2), so one kind of uncertainty looks one way across the chapter. Its label on the drawing and in the key, in words: the survey's margin of error for one month's change. A note says what it means: a column that ends inside the band is a change the survey cannot tell apart from no change at the Bureau's 90 percent level. A second note says the band applies to one month's change and not to the three-month average. The zero baseline stays on top of the band.

By script, of the seven drops, October 2025 (minus 140,000) and February 2026 (minus 156,000) pass the margin; January (minus 48,000), June (minus 20,000), August (minus 70,000) and December 2025 (minus 17,000) and July 2026 (minus 10,000) sit inside it. Both named drops are final months. August 2026's preliminary gain of 133,000 also passes the band; nothing names it.

**The named mark.** DR-239's two drops past the margin, October 2025 and February 2026, each labeled with its month and value. They take **Charcoal at the subject weight** through `labels.named` with a list of two, never the red point. Rule 14.6's own rows decide it: "Red never codes a series, a group, a step on a scale or in a process, or a sign, such as a deficit or a loss", and both named marks are losses; and "Two findings: both in Charcoal at the subject weight, each with its label". Every other column keeps the light fill. The three-month average draws in the context ink at the context weight, so the title's two marks alone carry the subject ink. No red anywhere on the plate.

**Title kind and grade line.** A Finding, with S14's grade line: "Documented: a Bureau of Labor Statistics survey of employers, as copied by FRED". I suggest the title join the two sentences Dustin approved under DR-239, word for word: "Payrolls shrank in seven of the 57 months charted, and only the October 2025 and February 2026 drops pass the survey’s margin of error." The editor may tune its words; the counts stay. Read from both sides: a reader who wants a weak economy sees seven drops counted; a reader who wants a strong one sees that five of them sit inside the margin. The latest average, 51,000 in September 2026, preliminary (50.67 thousand by script), prints in a chart note, as S14's "Latest" note does.

**Failure plate.** The lesson has a common misreading, so it takes one: the same 57 columns with no band, all seven drops labeled alike as job losses, under a title that counts seven losses as findings. Its caption: fails because five of the seven sit inside the survey's margin (DR-64: a chart singles out survey estimates only where the gap passes the margin, and says so). One fault per failure plate: no red on it either.

### (d) Complex examples 2 and 3 (for the complex examples maker, the component engineer and the accessibility lead)

**Example 2, Loops B4 and R10 stepped through Variable C3.**

By script: Loop B4 is L23, L24, L54 (D5 to C3 to C5 to D5), balancing; Loop R10 is L08, L25, L53, L42 (C1 to C2 to C3 to C4 to C1), reinforcing. The two share Variable C3 alone.

| Step | Connection | From, to | Sign | Grade | Delay |
|---|---|---|---|---|---|
| B4, 1 of 3 | L23 "Poor service raises incumbents' risk of losing" | D5 to C3 | minus | well supported | short |
| B4, 2 of 3 | L24 "Electoral pressure leads to actual defeats" | C3 to C5 | plus | well supported | medium |
| B4, 3 of 3 | L54 "Removing incumbents improves performance of those remaining" | C5 to D5 | plus | well supported | medium |
| R10, 1 of 4 | L08 "Safe seats make the primary decisive" | C1 to C2 | plus | documented | short |
| R10, 2 of 4 | L25 "Decisive primaries reduce general-election pressure" | C2 to C3 | minus | well supported | short |
| R10, 3 of 4 | L53 "Officials safe from defeat write rules for themselves" | C3 to C4 | minus | plausible | medium |
| R10, 4 of 4 | L42 "Incumbent-drawn maps create safe seats" | C4 to C1 | plus | documented | medium |

- **Order: Loop B4's three steps, then Loop R10's four, each loop in the atlas's own order.** Each loop drawing numbers its steps in that order (Rule 15.6; `three_loop` and `four_loop` number by the atlas's `links`), and each loop's `how_to_read` reads in that order, so the stepper's "step 2 of 3" always lights the drawn 2. Starting each loop at C3 would make the first lit step a drawn 2 or 3, teaching that the numbers mean nothing. In this order C3 sits in the middle of both walks: B4's steps 1 and 2 enter and leave it, and R10's steps 2 and 3 do the same.
- **B4 first.** The atlas calls B4 "the main balancing loop in the model" and says its strength depends on C1 and C2, the two ends of R10's first step. A reader who has watched the risk of losing office turn poor service into defeats knows what R10 takes away when it lowers that risk. Rule 15.15 also sets B4 first, so the chapter 14 example and the chapter 15 plate agree. Read from both sides: a reader who trusts elections to discipline officials meets B4's three steps at their grade, well supported, with the atlas's limit on L54 ("its main study covers Brazilian mayors"); a reader who thinks safe seats have broken that meets R10 next, with its weakest step, L53, printed at its grade, plausible. Each loop's qualification prints once, in the atlas's words. Neither loop is softened or raised.
- **The starting supposition** follows each loop's first connection: in B4, start at the quality of public services and suppose it falls (L23's name speaks of poor service); in R10, start at seats with little electoral competition and suppose they rise (R10 runs up). Each loop's walk keeps its own supposition, and the status line says when the walk changes loops.
- **Variable C3** carries its own title, "Risk of losing office", in both drawings and in every status line (DR-265, DR-267). "Electoral pressure", the atlas's chain label, never prints as its name; it may print only as the glossary term in quotes, as Rule 15.15 does. The other titles: D5 "Quality of public services", C5 "Incumbents defeated or pushed into retirement", C1 "Seats with little electoral competition", C2 "How often the primary decides the winner", C4 "Officeholders' control over election rules".
- **Marks.** C3's pill filled in ink in both drawings, as Rule 15.15 sets. The lit step takes the selected look Rule 18.22 sets, never Pillar Red, which on a loop drawing means a reform's target. No reform appears on example 2: the Gate 2 example is the two loops' structure, and the reform comparison is example 3's. R-01 and R-02, which both loops list, are neither added nor dropped for who works on them (DR-223); the example holds no reform at all.

**Example 3, the three reforms that act on Loop R8.**

**Which three.** R-06, R-30 and R-38 are the reforms whose own records name Loop R8 (`reforms[].loops`). Loop R8's own record lists R-30 alone; this is the disagreement V7.1 item 29 already records (D3-1860). The plate says so in plain words, from the model: "Each of these reforms names Loop R8 in its own record; the loop's record lists Reform R-30 only." Read from both sides, the rule picks by the atlas's structure, not by subject: the three sit in three different reform groups (Elections and representation; Housing, care, energy and infrastructure; Competition and technology).

**By target**, read by script; the drawing holds Loop R8 alone (A5 "Housing scarcity", A6 "Homeowners' equity", L38 and L39, both well supported, both long), and Rule 12.5's red lights only a target of the chosen reform that sits on it (Rule 15.11):

| Reform | Targets on Loop R8 | Targets outside it, printed in words with layer |
|---|---|---|
| R-06 "Hold local elections alongside November races" | L39 | Variable B5 "Equality of voter turnout" (core layer) |
| R-30 "More homes allowed by right near jobs" | L39 and A5 | Connection LE17 "Housing scarcity raises rents and prices" (economy layer) |
| R-38 "Limits on pricing software using rivals' data" | None | Connection LT12 "Shared-data pricing software can raise rents", plausible and contested, and Variable TC7 "Use of pricing algorithms" (technology layer) |

R-38 lights nothing on the drawing, and its column says so in words: "None of this reform's targets sits on Loop R8." The plate draws no variable or connection outside R8. By script, LT12 and LE17 both end at EC9 "Cost of essentials", and no connection runs from EC9 back into A5 or A6; drawing them would invent a path into the loop that the model does not hold.

**Line-up with no total.** One column per reform in ID order, R-06, R-30, R-38, with R-06 checked at load, as Rule 15.20's chooser does. Rows, all live text: targets on the loop; targets outside it; band (all three "rules", in the atlas's word); then the four effects one family to a row in the atlas's order, Democratic quality, Government efficacy, Economic performance, Income and wealth equality; then the problem evidence grade, the remedy evidence grade and the atlas's confidence in its effects; then the routes.

| Family | R-06 | R-30 | R-38 |
|---|---|---|---|
| Democratic quality | +L local | +S delayed | 0 |
| Government efficacy | +S | 0 | 0 |
| Economic performance | 0 | +M | +S sector |
| Income and wealth equality | +S | +M renter-owner | +S renters |

- Each code prints whole as the atlas stores it, the qualifier in the same cell after the code: "+L local", "+S delayed", "+M renter-owner", "+S sector", "+S renters". Never a footnote, a tooltip or a cut.
- "0" prints with its meaning, "no expected effect", never blank, a dash or "none".
- A key under the table gives the atlas's seven codes in its order with its words (+L large positive, +M moderate positive, +S small positive, 0 no expected effect, -S small negative, -M moderate negative, ? direction uncertain), so a reader sees the scale's ends and that "?" is not zero. Then the atlas's own sentence, quoted: "The codes are conditional on the reform working as described, and codes for different families are never added together."
- No total row or column, no count of plus codes, no sort, no ranking word, no fill, bar, heat ramp or ink by code. The codes are text in the text ink.
- Grades as the atlas holds them: problem evidence R-06 well supported, R-30 well supported, R-38 plausible and contested; remedy evidence R-06 well supported, R-30 plausible, R-38 plausible; confidence in effects verbatim, R-06 "high", R-30 "high where binding; medium for US statutes", R-38 "low to medium". A grade is a typed word (Rule 13.3), never a mark size or a shade. The remedy evidence's words, with each "Main limitation", go in the disclosure (Rule 18.8), verbatim, with `tradeoffs`.
- Routes as Rule 15.20 prints them: the route's V7 name, the atlas's `who` words, feasibility in the atlas's word, and "Not checked" where `checked` is empty. By script, eight of the nine route entries are undated; R-38's state statute route alone carries a check date and prints "Checked October 15, 2026". No route note prints: R-30's note on Massachusetts Question 7 speaks of a November 3, 2026 vote after the model's date.
- No status text, as Rule 15.20. R-30's status describes Question 7 as on the ballot; the plate adds nothing about the vote. Any status or route the plate does print sits under "As of October 15, 2026".
- No control offers an amount, odds, a total or a loop strength (Rule 15.21).

### (e) Rules 15.22 to 15.25 (for the systems designer and the research lead)

**15.22, the federal statute: what draws first.** The spine first: the stages every enacted bill passes, in order, from introduction and committee, through the floor in each chamber and reconciling the two versions, to enrolling, presentment, signature and the public law number, in Charcoal at the subject weight, as Rule 14.6 gives a diagram the path the question follows. Then, in the order a bill meets them, the paths that leave the spine, each in the context ink and each named in words where it leaves: cloture in the Senate; suspension of the rules in the House; veto, then override or a stop; law without signature; the pocket veto. A path that ends a bill ends its line on a square, as the trackers do (DR-108). Then what follows the law: funding by appropriation, implementation by rule (5 U.S.C. 553 and 801), and litigation. Reversal comes last: repeal by a later law, a sunset in the law's own text, a court striking it down.

Why the spine first: the route's question is how a reform becomes federal law and how it can be undone; the spine answers the first half with what every enacted bill shares; and the bill tracker's six steps sit on it, so 15.23 maps onto what the reader already holds. The plate heads with V7's route name and instrument, "Federal statute", "Act of Congress, including appropriations and reconciliation", under the model's date. Since V7's instrument names reconciliation, the plate draws the reconciliation path with its source, or names it as not yet sourced; it never drops it (request R-1). Each stage carries its source and the date it was read. A stage whose source was not read in full (the research file marks the courts' page "its text was not read closely") prints no read date until the research lead reads it (R-1). No real bill sits on the plate. If the systems designer adds one bill's path as an example, it is drawn as a documented record (Rule 13.11), dated, and logged.

**15.24, the 11 routes.** V7's order (LOC, SS, BI, FS, FR, FA, ENF, CRT, AV, IC, CIV), never sorted by feasibility or count. Each route: V7's name and instrument; its stages; its official source; the date the studio read it; and, from the model, how many reform route entries name it and how many carry a check date. By script: 126 entries, 13 dated (FS 38 entries, 3 dated; SS 29, 3; LOC 15, 2; BI 11, 2; CRT 7, 0; FA 7, 1; FR 6, 0; ENF 5, 2; CIV 4, 0; AV 3, 0; IC 1, 0). Two dates never share one word: "Source read" for the studio's reading of the law, and "Checked" or "Not checked" for an atlas route entry (Rule 13.10). The atlas's feasibility words (four levels) and its five dependency questions (authority, funding, enforcement, capacity, durability) print once for the set, in its words.

**15.25, the reconciliation table: row order.** Phase 0's numbers stay as the row IDs, so each row can be traced to Phase 0's file and the November 13 rerun. Rows group by what a copied drawing could mislead a reader about, values first:
1. A value: row 42, the Ledger's reform counts, D03 shown 10 against 9 and D04 shown 14 against 13, both counting the rejected R-35. These are the two value conflicts.
2. A sign (row 19), a grade (row 40), a delay (row 10).
3. Identifiers (rows 1 to 9).
4. Structure (rows 22, 23, 27, 43, 44, 45).
5. Encoding (rows 11 to 18, 20, 21, 24 to 26, 28).
6. Labels (rows 29 to 39, 41).
7. New rows for what Phase 2 and Phase 3 drew from V7, numbered from 46, in chapter order.

Inside a group, Phase 0's number order. Why: the first two groups decide what a reader believes the model says; the rest change how the model is drawn or named. The plate prints the counts (2,644 comparisons rerun on November 13, 2026, from Dustin's three uploads: 2,642 match, 2 conflict, both in row 42; 45 rows: 9 identifier, 1 sign, 1 grade, 1 delay, 12 label, 7 structure, 14 encoding; 8 flags read and set aside); the full table may sit behind a disclosure.

**Each row's model value is read from the model by script, never copied from Phase 0's table.** Row 40 shows why. Phase 0 wrote "V7 names no weakest step" for Loop B4, but the model's own `evidence_summary` for B4, read today, ends: "For U.S. services the weakest is L54, since its main study covers Brazilian mayors." The model file is the one Phase 0 read, byte for byte (the rerun's SHA-256). Row 40's resolution therefore becomes: keep "weakest" only in the atlas's own words, which name the limit for U.S. services, with all three steps graded well supported, as Rule 15.15 already prints it. No earlier drawing is cited for any V7 value (R5-6).

### (f) The trackers: each step's evidence and each end's words (for the tracker designer, the research lead and the editor)

The step names and end words come from the research lead's sources; these rules decide what marks a step and how a line ends, for both trackers, under DR-108's marks and DR-150's slash.

- **Done.** A step is done only on a dated official record of it, from the body that takes the step. For a ballot measure: the filing office's or attorney general's record of the filing or certification, the election office's notice that the measure qualified, the certified canvass. For a court case: the court's own docket or judgment, such as a complaint filed, a judgment entered, an appeals court's judgment, the Supreme Court's docketing of a petition, its order on it, its opinion.
- **Not evidence of a done step:** a news report, a campaign's or a party's claim, a signature count announced by proponents, an unofficial election count, a scheduled date (an election day, an argument date), or an argument heard. The research lead's own case shows the gap: Alaska's 2026 measure had an unofficial count on November 10 and a target date to certify of November 25. Until certification, the vote step is current, not done.
- **Current.** The record shows the step has begun (a petition filed, a case docketed or argued) and shows no record that it ended.
- **Slash.** A step the law of that state or court does not have keeps its number with a slash (DR-108, DR-150), as a direct initiative state with no legislature step. A step a plate's item simply has not reached stays blank.
- **Stopped.** An item that ends before the last step ends its line on a square at the last step it reached, with the record's own word for why: for example, did not qualify, withdrawn, removed from the ballot by a court, dismissed, settled, review denied.
- **End words.** The certifying or deciding body's own word, in words, with its date. A measure: its certified result, never inferred from a count. A case: the court's disposition as its judgment enters it (for example affirmed, reversed, vacated, remanded), naming the court. A remand prints in words; the line never runs backward and draws no second pass, which would invent steps. A decided or certified item says so in words, as a signed bill reads as law (DR-108); a filled last mark never says it alone.
- **Invented items (DR-275).** Each plate's three items show different states (one current, one stopped, one decided or certified), each labeled Illustrative beside it. Read from both sides: no invented subject is a question the record ties to one party, no real person, party, group, company or official appears, and the three outcomes do not line up for one side. An invented number takes a form the real office or court cannot issue (DR-151's practice), and the tracker designer says how that was checked. Any state an item names counts toward Rule 01.9 in chapter 11's log.

### (g) Rule 01.9 and DR-229 after round 5 (for the systems designer, the engineer and the main session)

**Chapter 14 holds.** By script from `14-example-log.json`: 108 examples today, Taxes, wealth and economic security (D08) the largest at 16. Round 5 adds four, each logged by its owner:
- Example 1, S14's data, Work, pay and bargaining power (D07): 10 to 11. A second plate of a file already drawn is a second example, as S95 was.
- Example 2, Loop B4 (D04, 13 to 14) and Loop R10 (D02, 12 to 13), logged in the domains Rule 15.15 uses.
- Example 3, Loop R8 and its three reforms, Housing, health care and getting ahead (D09, 14 to 15), as Rule 15.14 logs R8.

The selection guide and the palette specification draw no data and log nothing. That makes 112 examples, D08 still the largest at 16 against a limit of 28. No state is added, since examples 1 to 3 print no status or route note naming one. California, Florida and New York stay at 5 each, against a limit of 22.

**Chapter 15 holds.** By script from `phase3_ch15_build.py`'s log calls: 30 examples today, Elections and representation (D02) the largest at 7. Round 4 set that one more D02 example needs a chapter of 32 or more. I rule that 15.22 logs one example (D04, a federal statute's workflow), 15.24 one (atlas-wide, the 11 routes) and 15.25 one (atlas-wide, the whole model), which bring the chapter to 33, D02 still 7. 15.23 then logs one example per tracker it maps, in the domain chapter 11 gives it, the ballot measure tracker in D02 and the court case tracker in Checks on power and equal justice (D05). With the five trackers round 1's plan names for 15.23 (Rules 11.1, 11.8 and 11.9 and the two new ones), the chapter reaches 38 with D02 at 8 at most, under one in four (9.5 allowed). The generator's own Rule 01.9 check over the final log decides; it fails anything past the limit.

**DR-229 under D3-689's test.** Round 5 adds no chapter 14 form, so no form's data moves. The test governs new picks of form data, and the complex examples are Gate 2's named picks, one from each of three domains, approved with the Phase 3 proposal. Of them, only Loop R10 is an elections subject, and it adds one D02 example, 13 of 112. The ballot measure tracker is chapter 11's, approved under DR-231, and its use is an election question by definition, which is what D3-689's test asks.

## Routine calls

- D3-xxx | The selection guide lists each of the 127 forms once, under its plan family | The coverage plan's section 2, approved under DR-62 and DR-63: "Each form sits in one family"; a second listing breaks R5-2's count of one
- D3-xxx | Within a question, forms run Core, Extended, Reference, Avoid, then by rule number; 14.130 sorts as Extended | A reader meets the supported forms first; rule order inside a family follows build rounds; 14.130's entry already says extended
- D3-xxx | An avoid form shows "Avoid" in words and one diagonal rule across its whole picture, never red or hatch | Words survive gray and screen readers; red is the view's one working red (Rule 05.3) and reads as a warning about a group (Rule 14.6); the hatch is Stone's group mark
- D3-xxx | Selection guide pictures hold shapes only, in the neutral chart roles, with no number, word or party color, and 14.124's picture takes no red or blue | The plate then states no figure and logs no example; DR-255's exception covers only sketch 14.124's misleading half
- D3-xxx | The palette specification shows Rule 14.5's four palettes and the grade line code on Newsprint and Charcoal, Newsprint values measured on White, no swatch on Prussian | Chart tokens exist for two grounds (`chartGrounds`); round 0 set White as printed paper and kept charts off Prussian
- D3-xxx | The palette plate's numbers come from round 0's measure functions, pass judged on unrounded values | Board 1's approved numbers (DR-236) and the plate then agree, and no ratio is rounded up to pass
- D3-xxx | Example 1 draws all 57 months, January 2022 to September 2026 | DR-64: one shared window, and no window starts at an inauguration date
- D3-xxx | Example 1's margin is a band of plus or minus 122,000 around zero in magnitude step 1 with context edges | The Bureau's 90 percent interval for one month's change; S58's treatment, so one kind of uncertainty looks one way
- D3-xxx | Example 1's two drops past the margin take Charcoal at the subject weight, never red | Rule 14.6: red never codes a loss, and two findings take Charcoal with their labels
- D3-xxx | Example 2 steps B4's three connections, then R10's four, each in the atlas's order | The drawn step numbers and each loop's reading then agree; B4 is the model's main balancing loop and Rule 15.15 sets it first
- D3-xxx | Example 3 offers R-06, R-30 and R-38 in ID order on Loop R8 alone, off-loop targets in words, and says the loop's record lists R-30 only | The three reforms whose own records name R8; drawing EC9 would invent a path into the loop; V7.1 item 29 records the lists' disagreement
- D3-xxx | Example 3 prints each effect code whole, "0" with its meaning, the atlas's seven-code key and its sentence that codes are never added; no total, sort, fill or status | Rule 15.21, the role file's ordinal rule and the atlas's own note
- D3-xxx | 15.22 draws the path to a public law first, then the paths that leave it, then funding, rule, courts, and reversal last | The route's question in its order; the bill tracker's steps sit on the spine
- D3-xxx | 15.24 keeps V7's route order and prints "Source read" apart from "Checked" | No ranking by feasibility; Rule 13.10's date is the atlas entry's, not the studio's reading
- D3-xxx | 15.25 orders rows value, sign, grade, delay, identifier, structure, encoding, label, then new rows, keeping Phase 0's numbers | A copied value or sign misleads first; Phase 0's numbers keep each row traceable to its file and the rerun
- D3-xxx | 15.25 reads every model value from the model by script; row 40's resolution keeps "weakest" in the atlas's own words | B4's `evidence_summary` names L54 the weakest for U.S. services, which Phase 0's table missed
- D3-xxx | A tracker step is done only on a dated official record from the body that takes it; ends print the body's own word | DR-108's "reads as law in words" applied to measures and cases; unofficial counts and scheduled dates are not records of a step
- D3-xxx | 15.22, 15.24 and 15.25 each log one example (D04, atlas-wide, atlas-wide) before 15.23's trackers log theirs | Chapter 15 reaches 33 before any D02 example is added, as round 4's limit set

## Requests

### To the research lead

- **R-1, 15.22's stages (ruling (e)).** Read in full, with the date: the courts' structure page (marked "not read closely"); the House rule for suspension of the rules and its two-thirds vote; and the law that sets budget reconciliation's limit on Senate debate, since V7's instrument for the federal statute route names reconciliation. Name any you cannot read.
- **R-2, 15.25's model values (ruling (e)).** Each of the 45 rows' model value read by script from today's model into your notes for the systems designer, row 40 with B4's `evidence_summary` sentence; and the new rows for what Phase 2 and Phase 3 drew from V7, each with its chapter and rule.
- **R-3, the trackers (ruling (f)).** For each step of both trackers, the official record that marks it done, from the state constitutions and election offices you hold and from Title 28 and the Supreme Court's rules (the rules on a petition's time and on its disposition), with each end's word as the source writes it.

### To the engineer

- **E-1, the palette generator (ruling (b)).** Reuse round 0's contrast, OKLab, grayscale and Machado functions from `work/boards/phase-3/round-0/palettes/build_palette_proofs.py`, or import them, so the plate equals board 1. Print the token release on the plate.
- **E-2, the selection guide check (ruling (a)).** In the guide check or the selection guide build: 127 links, each form once, each target its entry, each tier word equal to the plan's first word and the entry's `tier`, no `<text>` in a picture, no ink outside the neutral roles, no red.
- **E-3, example 1 (ruling (c)).** In the new spec's form: a constant value band from minus 122 to plus 122 through the shared band part (`mag-1`, context edges) behind the columns; `labels.named` with a list of two columns; the average line in the context ink at the context weight.

### To the complex examples maker

- Build examples 1 to 3 to rulings (c) and (d). Check by script every figure the plates print against the data file and the model, and name each check in `notes_internal`.

### To the component engineer

- Example 2's keys file in ruling (d)'s order, seven steps with the status line naming the change of loop; no reform state. Example 3 on Rule 15.20's chooser, R-06 checked at load, lighting only on-loop targets (R-38 lights none).

### To the systems designer and the tracker designer

- Read (e), (f) and (g). Each plate logs as (g) sets.

### To the selection guide maker and the accessibility lead

- Read (a). Tier word in each link's accessible name; the avoid word in text, never in the picture alone.

## Sign-offs

None yet. Items are signed off here as owners land them.

## Tested

- Read: CLAUDE.md; my role file; the round 5 brief, all of it; Gate 2's section 9; my round 4 notes, rulings and sign-offs; DR-64, DR-93, DR-108, DR-124, DR-150, DR-151, DR-223, DR-229, DR-234, DR-236, DR-239, DR-255, DR-258 and DR-271 to DR-276; D3-689, D3-1566 and D3-1850 to D3-1878; Rules 14.5, 14.6 and 14.7 from their entry files; the coverage plan's section 2; round 0's palette notes (summary, calls, tested); the policy workflow sources (FS, SS, BI, LOC); round 1's chapter 15 rule plan for 15.22 to 15.25; Phase 0's reconciliation table and the November 13 rerun table; Rule 15.15's generator code.
- By script (`python3 -I`): the plan file's 127 forms by family and tier, duplicates, shared specimens and reorders under tier order, and every tier against its entry file; the chart tokens and their values in `tokens.json` 6.0.0-gate3.3; which specs use the magnitude, sequential, diverging and group roles; S14's data file (57 months, the seven drops, the two past 122,000, the preliminary months, the latest average); Loops B4, R10 and R8, their connections' ends, signs, grades and delays, and their variables' titles; Reforms R-06, R-30 and R-38, their targets with layer and loop, bands, effects, grades, confidence, routes and check dates; EC9's connections; the effect codes, families and their note; the 126 route entries by code with check dates; the 45 reconciliation rows by type; B4's `evidence_summary` against Phase 0's row 40; chapter 14's example log by domain and state; chapter 15's 30 log calls by domain.

## Not tested

- No build of any round 5 item: none has landed. No kit build, capture or guide check of my own yet.
- The palette proofs' numbers: I read the method and round 0's tested list, not a rerun of its script.
- The selection guide's pictures, the trackers' step names and the workflow stages' sources: they are not written yet.
- Whether Rule 18.22's stepper code holds two loops in one sequence: the component engineer's to say.
- Chapter 15's example count read from the generator's source, not from a run of it.
