# Chat 11c: data visualization lead's notes

Data visualization lead, Phase 4, chat 11c, November 22, 2026. Started 21:48 UTC (`date -u`). Brief: `work/handoffs/phase-4/20261122_Chat-11c-Brief.md`, section 6.2. Plan: `work/handoffs/phase-4/20261121_Chapter-21-Plan.md`. Model: `work/extract/atlas-v7-data.json`, SHA-256 ef1028ac87e402e30af9e3cda234fed63794b5570d0a165b9dab39073e08c7f2 (read 21:48 UTC). Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/e76584b2-1bba-5266-a75e-730f247433d8/scratchpad/c11c/dataviz-lead/`.

## Routine calls

- D4-xxx | The weakest step is read from the loop's evidence summary by one fixed method (R8), checked against the least certain grade | Rule 15.13's builder line asks for both and a stop when they disagree; two summaries (R7, R8) name no connection, so the method needs a defined outcome for them
- D4-xxx | A range effect code such as "0 to −S at high bite" draws both ends on Rule 13.5's pip scale, joined, with the code whole (R12) | chapter 15's `effect_rows` stops on any range ("draw it before printing it"), and Reform R-23's economic performance row is a range
- D4-xxx | The 390 px home drawing lists each part's outgoing flows only, so each of the 27 pairs prints once (R7) | listing incoming flows too would print every count twice and break T3's sum

- D4-xxx | A red target on a patterned connection draws its 6 px case on the red's rhythm, each case dash 1 px longer at each end, with the pattern at the drawn width (16 and 8 px at 4 px) and the case Charcoal in both themes (R14) | A solid case reads as a solid line in gray (Rule 13.4's failure); Rule 13.4 states patterns in line widths; Rule 12.5 names a Charcoal edge
- D4-xxx | T10 checks a contested remedy's stored text whole, in order, split at one sentence, both blocks with the same standing, and prints their lengths without judging them (R15) | DR-37 keeps the stored text; DR-314 and DR-323 set "at the length the record holds"; H08 never set a length
- D4-xxx | Plan corrections C1 to C5 (below, under Done): "same length" and the H08 citation leave sections 3.3, 5 (Rule 21.4's draft and specifications) and 8 (T10) | They followed Rule 01.22's old words, which DR-314 replaced, and cited a house rule that sets no length
- D4-xxx | The atlas title bar stays a Charcoal band in both themes (R17), and plan 3.1 follows the build (C6) | AL-17's "never a second banner" concerns landmarks, met by one header and a named nav; chapter 20 as built and D4-189 set the band; brief section 5 makes the build govern the shell
- D4-xxx | Count keys `records-naming:<S>:<V>` and `atlas:loops-reinforcing`/`-balancing` join R2 (R16), the latter over all 23 loops | The engineer's ask; the loop index prints all 23 by kind (DR-321)
- D4-xxx | The loop index's grade column follows R11's grade-line form for every loop (R18) | It prints the same stored field as Loop R18's grade line, and Rule 13.3 allows no stored spelling on a page
- D4-xxx | Batch 1 signs off every view's data and holds every view for display faults, requests 4 to 28 | Data matched the model on all 59 pages; the faults are in marks and layout, which the plates show to readers
- D4-xxx | Batch 2 signs off A12 to A16 and A18 to A20 whole, and holds A11 at 390 px and A17 for requests 29 to 31 | Every batch 1 item but part of 27 is fixed and seen; the three new faults were found on round 2's captures

## Rulings

Landed in this file by 21:53 UTC (`date -u` read at 21:53:52, straight after the write; corrections at 21:53 UTC). For the design director and the engineer. Every value named here is read from the model at build time; the values in brackets are today's, for checking only (R9).

### R1. Each data attribute and the model field it carries

| Attribute | Carries | Model field, read at build time | Printed as |
|---|---|---|---|
| `data-atlas-kind` | One of Rule 13.9's ten kinds: `variable`, `connection`, `loop`, `reform`, `issue`, `claim`, `domain`, `route`, `rule-change`, `delivery-case` (if C9's renderer already writes the kind word as Rule 13.9 prints it, "Variable", "Rule change", that spelling stands; one spelling across every page is what the test needs) | Where the ID lives: `nodes`, `links`, `loops`, `reforms`, `issues`, `claims`, `domains[].id`, `routes.items[].code`, `repairLog.rows[].id`, `deliveryLog.rows[].id` | The chip's kind word, capitalized as Rule 13.9 lists it |
| `data-atlas-id` | The ID exactly as the model keys it, ASCII hyphen (`R-23`, `L14`, `D04`, `SS`, `RL19`, `CL1340`) | The record's key | Inside the chip, on one line. Lowercase only inside anchors |
| `data-sign` | `+`, `-`, or `none` | `links[k].polarity`; `null` (the 7 authority connections) is `none` | Sign tag with "raises" or "lowers"; authority: open diamond and "decides", no tag. A true minus wherever a sign prints as text |
| `data-type` | `causal`, `money`, `information`, `ownership`, `authority` | `links[k].type` as stored | Rule 15.4's type words |
| `data-delay` | `S`, `M`, `L` | `links[k].delay` as stored | One, two or three ticks with "under 2 years", "2 to 10 years", "over 10 years". The letter never prints |
| `data-grade` | The stored grade, spelled as the record that holds it spells it | `links[k].evidence` (`documented`, `well-supported`, `plausible`, `plausible_contested`, `hypothesis`); `issues[k].grade` (`well_supported` with an underscore); `claims[k].confidence`; `reforms[k].problem_evidence.grade` and `.remedy_evidence.grade` (`contested`) | The display word from Rule 13.3's one table, never the stored spelling, on every mark and label the page composes (see R11 for stored prose) |
| `data-count`, `data-count-of` | The integer printed, and the method that counts it | R2's list, nothing else | The number in figures, with its words |
| `data-red="working"` | A mark the chosen reform targets | `reforms[chosen].targets`, variables and connections | Rule 12.5's red target (R10) |
| `data-effect-family` | `DQ`, `GE`, `EP`, `EQ` | `outcomes.families` keys, in that order | DQ as "Quality of democracy" (DR-39, over the model's "Democratic quality"); the other three as stored |
| `data-effect-code` | The stored code whole, qualifier included, ASCII hyphen | `reforms[k].effects[family]` (such as `0 to -S at high bite`) | Each minus as U+2212, every other character as stored (R12) |
| `data-route` | The route code | `reforms[k].routes[].route` (`SS`, `BI`, `LOC`, `FS`, `FR`, `CRT` ...) | Chip and the name from `routes.items[].name` |
| `data-checked` | The stored date, or `none` | `reforms[k].routes[].checked` (`null` is `none`) | "Checked" and the date in words, or "Not checked". Never the reform's `status.checked` |
| `data-evidence-href` | The one link to the record that grades the claim | R5 | A chip link, figure link or step link |

Aligned at 21:55:55 UTC with the engineer's contract C9 (his notes, written 21:52 UTC, which landed beside these rulings). C9's marks stand; these few additions let T4, T8 and T12 read what they claim to check:

- **`data-atlas-reads`** (C9's, on the read-aloud line) carries each variable's direction as well as the order: `D2:rises L14 D4:falls L15 D2:rises` for Loop R18. The first token is the loop's first variable, then each connection and the variable it reaches with `rises` or `falls` (R4). The visible words say the same.
- **`data-weakest="true"`** on the weakest step's mark only (R8), the drawing's and the stepper's.
- **A part box is not a typed record.** Rule 10.8 names the parts in words, with no chip, so a box on the home drawing carries `data-part` (`A`, `B`, `C`, `D`, `E`, `X`, `EC`, `TC`) and no `data-atlas-kind`; T1 would read a box's kind as a fault. With a question pressed, each box also carries `data-lit="true"` or `"false"`, and the pressed question's button `data-pathway="PW06"` (C9's `pressed_question` key already names the pathway by ID).
- **`data-status-date`** (C9's) holds `reforms[k].status.checked`; `data-checked` on a route never takes that value (Rule 15.16's "never a route dated from the reform's status").
- Each Register row carries its own `data-atlas-kind` and `data-atlas-id`, and a connection's row its four marks' attributes.

### R2. The count methods, by name

`part(v)` is `EC` or `TC` for a variable in the economy or technology layer, else its `cluster` (`A` to `E`, `X`). `sheet(v)` is `EC` or `TC` the same way, else the first domain in its `domain` field (split on `/`). A connection files on `sheet(links[k].to)`. A numbered loop is one whose `closure` does not start with "conceptual". These are Appendix A's functions, unchanged.

C9 names the keys; this table fixes each key's method. The keys follow C9's examples (`part-inside:B`, `flow:A>B`, `sheet:D04:connections`, `sheet:D04:grade:plausible`, `atlas:variables`, `records-shown:D04`, `loop:R18:minus`, `loop:R18:records`) and extend them the same way.

| `data-count-of` | Counts |
|---|---|
| `atlas:variables`, `atlas:connections`, `atlas:loops`, `atlas:loops-numbered`, `atlas:reforms`, `atlas:issues`, `atlas:issues-retired`, `atlas:hubs`, `atlas:pathways` | The whole model [51, 118, 23, 20, 50, 194, 1 (I128), 5, 16] |
| `atlas:reforms-active` | Reforms not rejected [49] |
| `atlas:grade:<stored grade>` | All connections at that grade [32, 37, 35, 7, 7] |
| `hub:<hub ID>:questions` | Pathways whose `hub` is that hub |
| `part-variables:<P>` | Variables with `part(v) == P` |
| `part-inside:<P>` | Connections with both ends in P [E and X hold 0] |
| `flow:<P>><Q>` | Connections from a variable in P to one in Q, P not Q [27 pairs, 81 in all] |
| `sheet:<S>:variables`, `sheet:<S>:connections` | Variables on S; connections filed on S |
| `sheet:<S>:loops` | Numbered loops with any `chain` variable on S |
| `sheet:<S>:reforms` | Reforms not rejected that target a variable on S or a connection filed on S |
| `sheet:<S>:issues` | `len(domains[S].issues)`; EC and TC have no list, so they print "none filed" with `data-count="0"` |
| `sheet:<S>:grade:<stored grade>` | Connections filed on S at that grade |
| `records-shown:<S>` | Issue records on sheet S whose `nodes` hold any variable the filter has checked (the page's own filter state) [9 for D04 with D4] |
| `records-grade:<S>:<stored grade>` | Issue records on S at that grade [D04: 11 documented, 6 well supported, 3 plausible] |
| `loop:<L>:steps`, `loop:<L>:minus`, `loop:<L>:records` | `len(links)`; minus signs among them; `len(records)` [R18: 2, 2, 8] |
| `question:<PW>:parts` | Distinct `part(v)` over the pathway's `model_refs.nodes` [PW06: 3, parts A, D and EC] |

A count the page prints under a key not on this list is a FAIL under T3 until I add its method here.

### R3. Which grade takes which line (Rule 13.4)

| Stored grade | Line | Word | Mark |
|---|---|---|---|
| `documented` | Solid | Documented | The 7 px record square before the word, and nowhere else |
| `well-supported` | Solid | Well supported | None |
| `plausible` | Dashed, 8 and 4 px on a 2 px line | Plausible | None |
| `plausible_contested` | Dash and dot, 8, 3, 2 and 3 px on a 2 px line | Contested | None. All 7 carry `contested: true` today; the flag and the value agree. If they ever disagree, the build stops |
| `hypothesis` | Round dots 5 px apart, stopping 3 px short of the arrowhead | Hypothesis | None |
| A conceptual loop's step | Hollow line, two 1 px rails | The loop's grade word on its label | None |
| Authority (`type: authority`) | Solid, open diamond 14 by 11 px | "decides" | No sign tag; never in a loop drawing |

A patterned line that carries delay ticks runs solid for its first 28 px (the lead-in). A step shorter than 40 px after the lead-in prints its grade word beside it. Every line on a view is one width; width never carries a grade, a count or an effect. Issue records, claims and a reform's two grades draw no line: their grade prints as the word, with Rule 13.3's gloss in a key. On the Register's index, each grade column's head carries a 40 px sample of its line and its word (plan 3.4). Sheet D04's ten lines today: L10 and L54 solid; L14 and L22 solid with the record square; L12, L17, L21, T03 and LT15 dashed; L19 dotted.

### R4. The read-aloud line turns at each minus (Rule 15.6, ED-F6)

1. Start at the loop's first variable, `loops[k].chain[0][0]` (the first connection's `from`), and say it rises ("start with more").
2. Walk `loops[k].links` in order. At a `+` the next variable moves the same way as the last; at a `-` it turns, rises to falls or falls to rises. That is the only place a turn happens.
3. Each step clause names its connection's chip, its sign word ("raises" or "lowers") and the direction of the variable it reaches. The turn is visible twice: the minus tag with "lowers", and the direction word that changed.
4. The last step returns to the first variable. The line ends by saying it moves the same way it started (reinforcing) or the other way (balancing), with the count of minus signs and the kind. The build stops if that ending disagrees with `loops[k].type` or with the parity of `loop:<L>:minus`.
5. Loop R18 today: Variable D2 rises; Connection L14, minus, so Variable D4 falls; Connection L15, minus, so Variable D2 rises, the same way it started. Two minus signs, an even count: reinforcing [Q09].

The editor writes the words. The atlas's own `how_to_read` sentence is stored prose and never replaces the composed line; where a page quotes it, it prints as stored (R11).

### R5. Where each evidence link goes (Rule 21.7, T9)

| Record | `data-evidence-href` target | Anchor ID |
|---|---|---|
| Connection | Its line on the Register sheet `sheet(links[k].to)` | `register-<id>`, as `register-l14` on D04, `register-l15` on D05, `register-le15` on EC |
| Variable | Its entry on sheet `sheet(v)` | `variable-<id>` |
| Issue record | Its row on its own sheet, `issues[k].domain` | `issue-<id>` |
| Loop, reform | Its own page | the page |
| Domain | Its sheet | the sheet |
| Claim | A disclosure on the same page (Rule 18.8), closed on load, holding the claim's stored `claim`, `confidence` (as its display word), `population`, `jurisdiction`, `period`, `limitation` and its sources in Rule 13.6's parts. There is no claim page template (plan 9.1) | `claim-<id>`, as `claim-cl1340` |
| Route | Its workflow (Rule 15.22) | the workflow |
| A figure inside stored text | The claim that holds it: among the pathway's `claim_ids`, the one whose `claim` text holds the same figure and year. If none or more than one does, the build stops and lists them for me | as Claim |

The engineer chooses the path prefixes. The sheet in every path is computed by `sheet()`, never typed. T9 passes a link when its target exists: inside the same export, the anchor is on the page; outside it, the record exists in the model and the path is the scheme's path for that kind and ID.

### R6. The home drawing's inks

- **The main circuit,** the five part-to-part arrows `flow:A>B`, `flow:B>C`, `flow:C>D`, `flow:D>E`, `flow:E>A` [5, 4, 4, 4, 3], in `--oa-color-graphic-essential-on-newsprint`, and on Charcoal `--oa-color-graphic-essential-on-charcoal`.
- **Every other arrow** (22 pairs) in `--oa-color-graphic-subtle-on-newsprint` (Stone, 4.29 to 1, which passes 3 to 1 for a mark), and on Charcoal `--oa-color-graphic-subtle-on-charcoal` (dim Newsprint, 7.26 to 1). Never Stone on Charcoal (3.10 to 1 by token arithmetic [Q14]; AL-23 bars it).
- **Counts are text,** so every count, on every arrow, prints in the text ink at 4.5 to 1 or better, never in Stone. The main circuit's counts print bold, and a key line names "the main circuit" in words, so the main circuit survives the loss of color (Rule 1.4.1). One arrow width throughout.
- **One arrow per directed pair.** A pair that runs both ways (B and C, B and D, C and D, D and E, A and EC, and the rest the model holds) draws two arrows, each with its own count. No double-headed arrow.
- **With a question pressed,** the arrows keep their inks and counts. The lit boxes stay in full ink with the words "This question reaches here" (draft). The other boxes take Rule 17.8's muted state: outline in `--oa-color-state-muted-mark-on-newsprint`, on Charcoal `--oa-color-state-muted-mark-on-charcoal` (AL-23), and their words in the text ink at regular weight, so no word drops under 4.5 to 1. The lit parts are `question:PW06:parts`, read from the pathway's own variables [A, D, EC].
- **No red** on the home view.

### R7. The home drawing at 390 px

- One stacked list of the eight parts, in the order effects travel: Outside forces (X), Wealth (A), Voice (B), Elections (C), Checks (D), Policy (E), Your household (EC), Technology (TC).
- Each card: the plain name, its question, the model's own title beneath, its count of variables (`part-variables:<P>`) and its count inside (`part-inside:<P>`; Policy and Outside forces print their 0 in words, such as "none inside", with `data-count="0"`).
- Under it, one line for each **outgoing** pair, "5 to Voice" (draft), each with `data-count-of="flow:P>Q"`. Outgoing only, so each of the 27 pairs prints exactly once, the lines sum to 81 and, with the inside counts, to 118 (T3 checks both sums). The main-circuit line comes first and prints bold with the key's words; the rest follow in the stack's order, regular weight, all in the text ink.
- No arrows drawn between cards (DR-64 lets a phone drawing change form when it carries the same data). The pressed question lights and mutes cards as R6 sets.

### R8. The weakest step (Rule 15.13)

The weakest step is the connection the loop's own `evidence_summary` names as weakest, read by this one method:

1. In the summary, replace each "`<ID>: <connection name>`" with the bare ID first, because some names hold the word: Connection L11's name is "A weaker Congress invites presidential action".
2. Take the first sentence holding the word "weakest" or "weaker".
3. If the word is followed by "is" or "step is" and an ID ("The weakest is L02", "The weakest step is L53"), that ID is the step. Otherwise the step is the last ID before the word ("L57 is the weakest", "L15 ... is plausible and the weaker").
4. Check: the ID is one of the loop's own `links`, and its grade is the least certain among them, in Rule 13.3's order (Documented, Well supported, Plausible, Contested, Hypothesis). Ties are allowed (B4, B5, R2, R6, R12 and R15 tie at their lowest grade, and the summary breaks the tie). A step that fails the check stops the build.
5. If the sentence names no ID, no step is marked "Weakest step" and the label still takes the least certain grade. Today two loops are so: R7 ("its funding channel is a hypothesis and the weakest part of the loop", about the second half of L21, while both steps are plausible) and R8 ("it is the weaker step", about L39, with no ID in the sentence). Neither is drawn in chapter 21; if a later page draws them, I rule on each.

Run on today's model, the method names: R1 L02, R1b L04, R2 L19, R3 L47, R4a L55, R4b L45, R5 L36, R6 L02, R10 L53, R11 L52, R12 L57, R13 L12, R15 L32, R16 T01, **R18 L15**, B1a L17, B4 L54, B5 L49, R7 none, R8 none (read by eye from a script's printout; step 2 runs the method itself by script). Loop R18's label reads Plausible, from L15. ED-F4's line, "The loop holds only as firmly as this link." (draft), sits under L15 only.

### R9. Values the plan prints that the build must never copy

The build reads every one of these from the model, or counts it from the editor's words, at build time:

- Every count in plan sections 2, 3.2, 3.4 and Appendix B: 51, 118, 23, 20, 50, 194, I128, 49, the 27 flows, the inside counts, the whole index table and its grade columns, "9 of 20", D1's 8, D5's 11, R18's 8 records.
- **The D04 connection table's citations.** The plan shortened them ("shortened above only for this plan"). The page prints `links[k].citation` whole.
- **Q10's status lines and holds, 9,750 and 14,500 ms.** Those lines are my drafts, not the atlas's words. The holds are re-counted from the editor's final lines at 250 ms a word of everything the status line reads, "Step 2 of 2:" included, never under 6,000 ms (AL-24).
- **Q14's contrast ratios.** T13 measures the frame's pixels (AL-23); the plan's figures are token arithmetic only.
- R18's reform list (`[k for k in reforms if "R18" in reforms[k].loops]`, today R-11, R-15, R-48, never the loop's own two-item list); R-11's and R-23's targets, bands, effects, effects confidence, routes, feasibility, notes and check dates; R-23's other reforms at A4; R-35's targets, effects, grades and route note; R6's name on the reform page.
- Every stored text: summaries, short answers, cases, adaptations, qualifications, problem and remedy texts, increase_means sentences, titles, the everyday questions, the snapshot date (`meta.snapshot`, printed in words). The figures inside them (254%, 2022, 1.3 million, $7.25, seventeen, 87%) print from the stored text, never typed.
- The family names except DQ (R1), the route names, the band words.
- What the content files may name: IDs and choices only (plan 9.2), plus the plain part names Wealth, Voice, Elections, Checks, Policy, Your household, Technology and Outside forces, which are Dustin's words (DR-35, DR-41) and sit in the word fields, not the model.

### R10. One working red a view (Rules 05.3, 12.5, 21.5; T6)

"One working red a view" means one reform's targets, however many marks that is.

| View | Red marks, `data-red="working"` | In ink |
|---|---|---|
| Home | None | Everything |
| Reform R-23 | The outlines of Variables EC7 and A4 (its `targets`) | Connection LE15 (not a target); the chips of Reforms R-24, R-25, R-26 and R-31 "aims here" |
| The Register, sheet D04 | None. Reform R-35 is the rejected option; its targets L18 and L19 never turn red | Everything |
| Loop R18, Reform R-11 chosen | Variable D4's outline and Connections L14 and L15 (R-11's `targets`), three marks of one reform | The tags "Reform R-15 and Reform R-48 also aim here" |

Red sits on the drawing only, never on a chip, tag, button, panel, heading or word. It draws at 4 px on a 1 px Charcoal edge (Rule 13.5, DR-305), in `--oa-color-data-emphasis-red-on-newsprint` or `-on-charcoal`, and never on a Charcoal panel or on Prussian. When the reader chooses another reform, the red moves to that reform's targets and the last reform's marks return to ink.

### R11. Stored prose, chips and grade words

- The atlas's stored prose prints as stored (DR-37). Where it holds a bare ID of one of the ten kinds, the renderer sets that ID in its typed chip and changes nothing else. Where the prose already gives the kind word before the ID ("loop R1"), the chip takes that word in. For the four colliding codes, B2 to B5 (variable and loop), the kind comes from the kind word in the prose; with no kind word, the build stops and lists the place for me.
- Source IDs (`sources` keys, such as Q255, W117, K1508, N52) are not among the ten kinds. They print as stored in citations and take no chip. T1 skips them.
- The three reviewed connections, LTR1 to LTR3 (`rejectedLinks`), are not in `links`, so a "Connection" chip would fail T1. They print as "reviewed connection LTR1" in plain text with the words "reviewed and not drawn", the form Rule 13.9 gives a source line. T1 treats them as known.
- Grade words inside stored prose print as stored. T10's display-word check applies to every grade the page composes: marks, labels, keys, counts' heads, the issue rows' grade words and Loop R18's grade line.
- Loop R18's grade line is composed, not quoted: from `loops.R18.evidence`, each stored grade word becomes its display word and each bare variable code its chip, "Documented for Variable D2 to Variable D4; Plausible for Variable D4 to Variable D2" (the editor sets the words around it). Its closure prints in the atlas's words, and its delay as ticks and words.

### R12. Effects (Rule 15.16, T7)

- Four rows a reform, in the order DQ, GE, EP, EQ. Each row: the family name (R1), the pips of Rule 13.5, the code as stored with true minus signs, then its words from `outcomes.effect_codes`.
- A code with a qualifier prints whole, the qualifier straight after the code and the words after a comma: "+M lower tail, moderate positive"; "+M precondition, moderate positive".
- **A range** such as "0 to −S at high bite" (Reform R-23, Economic performance) draws both ends on the pip scale, the zero bar and one pip left, joined by a 1 px line in the same ink, and prints the code whole with both ends' words: "0 to −S at high bite, no expected effect to small negative" (draft; the editor's words). Chapter 15's `effect_rows` stops on a range by design ("draw it before printing it"), so the figure step must not call it for a range row; the atlas page's own effect row handles it.
- The atlas's confidence words print quoted as stored (`effects_confidence`), once, under the four rows. No total, average, score, bar length or color across the four.

### R13. The selection rules (DR-55, DR-93; plan 3.6)

I read each view's selection from both sides at sign-off, against plan 3.6's table, and each finding at the grade the model gives it. A view passes when the finding each side may want to skip prints at the same prominence as the rest of its section, with nothing added or softened. Specifically: on the reform page both readings of the contested remedy sit side by side with the same standing, each at the length the record holds (R15, DR-314, DR-323); on the loop page the case and the adaptation both print whole as stored; on the Register, Reform R-35 prints with its grade and the atlas's words on what the grade measures, and its route note (the 87% figure) prints as stored where routes print.

### R14. A red target on a patterned connection (the engineer's Request 1)

Written 22:26:44 UTC, at the main session's request. Reform R-11's targets on Loop R18 include Connection L15, plausible, drawn dashed. Chapter 15's `conn()` draws a red target only on a solid line, and chapter 15 stays as approved, so the figure step draws this case itself from System 1's `wire_marks(lit=True)` and `fitted()`, as the engineer proposes. Rule 12.5 sets the weights; Rule 13.4 sets the pattern; this ruling fills the gap between them and changes neither.

**(a) The case follows the dashes.** The 6 px Charcoal case dashes on the red line's rhythm, never solid under it. Each case dash runs 1 px past each end of its red dash (the case pattern is the red pattern with each dash 2 px longer and each gap 2 px shorter, offset 1 px back), so every red dash carries Rule 12.5's 1 px edge on its ends as well as its sides. Red on Newsprint measures 2.96 to 1 [Q14], and the edge exists to lift every red edge that meets Newsprint. The gaps show the page's ground.

Why not solid: a solid case leaves an unbroken 6 px Charcoal band at 13.29 to 1 against Newsprint, with the red dashes inside it at 4.49 to 1 against the Charcoal. In gray, and at reading distance in color, that band reads as a solid line, which is the failure Rule 13.4's plate shows: a plausible step looking as firm as a documented one. In gray the ruled form reads as dark-rimmed mid-gray dashes (red's luminance is about 0.20, Charcoal's 0.006, Newsprint's about 0.69) with clear light gaps between them.

**(b) Dash lengths scale with the weight.** Rule 13.4 states every pattern in line widths, so at 4 px the dashed pattern is 4 and 2 line widths: 16 px dash, 8 px gap, flat ends, stretched by `fitted('dashed', 4, run)` to start and end on ink. The 2 px lengths (8 and 4) are not kept: ringed by the case, their gap would close to 2 px and the line would read solid. On L15 today the run after the lead-in and its gap is about 192 px to the line's trimmed end and about 180 px to the 6 px arrowhead's base (measured from the figure step's own path at 22:26 UTC), so the fit to the base gives about 15.7 and 7.8 px for the red and 17.7 and 5.8 px for the case, seven whole periods. The same rule covers the other patterns at 4 px, should a later page need them: dash and dot 16, 6, 4 and 6 px; dots 4 px across, 10 px apart on centers, with 6 px case dots on the same centers.

- **Where the fit ends.** `wire_marks` trims the line 10 px short of the tip for the 2 px arrowhead, and the target's arrowhead is the 6 px one, 22 px long, so the pattern fits the run a reader sees: from the lead-in's gap to the 6 px arrowhead's base, 22 px from the tip, where the last dash ends whole. The solid line under the arrowhead's last 12 px is hidden by it either way.
- **The lead-in** stays 28 px from the tail at every width (Rule 13.4), solid red on a solid case, carrying the ticks. The pattern then leaves its own gap at 4 px, 8 px, and starts on ink.
- **The shortest run** counts at the drawn width: 20 line widths, 80 px at 4 px, after the lead-in and gap. L15 clears it. A target step shorter than that prints its grade word beside it, Rule 13.4's own fallback, and one under two whole periods (48 px for dashed) stops the figure step so I can rule.

**(c) Tag, ticks and arrowhead** stay as the approved solid target draws them (chapter 15's `rt` block, Rule 12.5's "arrowheads and sign tags at the 6 px sizes"): the sign tag at its 6 px size (18, 8, 22, 10 and 2 px) in ink with its sign in the surface color; the two delay ticks at the 6 px size, 14 px long and 2 px in ink, on the solid lead-in, the second ending at 18 px from the tail, so the 28 px lead-in keeps its clear line; the arrowhead in red at its 6 px size, 22 by 18 px, with no edge (DR-305). The tag sits where `wire_marks` places it, at the middle of the longest straight run, and covers the pattern under it, as it does on a 2 px dashed line. Nothing marks the grade except the pattern and the grade word, so the grade stays readable in gray and the red stays the target's alone.

**(d) The case is Charcoal in both themes.** Chapter 15's `rt` block strokes the case with `var(--oa-color-graphic-essential)`, which turns Newsprint on a Charcoal surface (`tokens.css`, line 1037), so a dark frame would rim the red in Newsprint. Rule 12.5 names a Charcoal edge and its token, `oa.color.graphic.essential.onNewsprint`. The atlas pages stroke the case with `--oa-color-graphic-essential-on-newsprint` in both themes: on Newsprint it is the edge, and on Charcoal it disappears into the ground, where the red stands at 4.49 to 1 alone [Q14] and the gaps show the ground. This applies to the solid target, L14, as well. I have not checked whether chapter 15's own plates draw a red target on Charcoal; if any does, it is a "Not fixed" item, not a change here.

**For the atlas test:** T2 reads L15's grade from its pattern as on any line, at the drawn width (a dash-to-gap ratio of about 2, counting the red mark, not the case); T6 then passes with D4, L14 and L15 red; T13 measures the red dashes at 3 to 1 or better against what they touch, which on Newsprint is the case.

### R15. T10 and a contested remedy's two readings (the editor's Request 6)

Written 22:26:44 UTC. The plan's T10 asked two readings "within a line's length of each other (H08)". That condition cannot hold for every record without editing the atlas's stored text, which DR-37 forbids, and DR-314 and DR-323 have since set "at the length the record holds" for Rules 01.22 and 13.12. H08 is the house rule on titles and grade verbs; it never set a length, so the plan cited it wrongly. I take the editor's proposal, with the checks made exact:

T10 passes a contested remedy when:

1. **Whole and in order.** The two blocks, read in order, give the stored `remedy_evidence.text` exactly, with whitespace collapsed. Nothing added, cut or moved.
2. **Split at one sentence.** The split falls at the start of the sentence the content file's `remedy_split` names, counted from 1 by the one splitter both the kit and the test use (System 1's: a break after `.`, `!` or `?` and a space, before a capital, a digit or an opening quotation mark), and each block holds at least one whole sentence. The kit and the test print the sentence list once in their logs, so the index can be read against it.
3. **The same standing.** At 1440 px the two blocks sit side by side in one row, tops aligned; under the specs' breakpoint they stack in order. Both are open on load, in the same type token, weight and ink, neither in a disclosure, a smaller size or a muted state, and each ends with its link to its source (T9).
4. **Lengths for the record.** The test's line prints each block's words and its line count at 1440 px, as in `PASS T10 A12 1440-light Reform R-23: remedy contested, two blocks, 42 and 38 words, N and M lines`. Length is reported and never fails the check.

Today only Reform R-23 has a contested remedy. Its stored text splits into four sentences of 8, 21, 13 and 38 words; `remedy_split: 4` gives blocks of 42 and 38 words, and the four sentences rejoin to the stored text exactly (checked by script at 22:26 UTC). Whether a split separates the two readings, rather than cutting one in half, is a judgment the test cannot make; I check it at sign-off, and R-23's split at "Main limitation" does separate them.

### R16. Two more count keys (the engineer's ask, batch 1)

Written 23:20:20 UTC. Added to R2's table, with these methods; the atlas test already counts them this way.

| `data-count-of` | Counts |
|---|---|
| `records-naming:<S>:<V>` | Issue records on sheet S whose `nodes` hold Variable V, whatever the filter shows [D04: D1 8, D4 9, D5 11] |
| `atlas:loops-reinforcing`, `atlas:loops-balancing` | All 23 loops by their stored `type`, numbered or conceptual [18 and 5], as the loop index prints all 23 (DR-321). A count of numbered loops alone would take `atlas:loops-numbered-reinforcing` and `-balancing` [17 and 3]; no page prints one today |

### R17. The atlas title bar on a Charcoal band stands (the design director's DD11C-R1)

Written 23:20:20 UTC. The specs' shell section sets the title bar as `<nav class="wa-bar oa-surface-charcoal" aria-label="Atlas views">`, Charcoal in both themes. It stands, for four reasons:

1. **AL-17 is met.** AL-17's "never a second banner" is about landmarks: the atlas's bar must be a second navigation named for what it holds, not a second `banner`. On all six exports I counted one `<header>` (the site's masthead), no `role="banner"`, a `nav` named "Atlas views", one `main` and one `h1` (by script, between date reads at 23:09 and 23:14 UTC). The band carries no wordmark and no copy of the site's parts.
2. **Chapter 20 as built governs the shell** (brief section 5), and its home page opens the atlas section with this same bar on Charcoal (D4-189). A reader who follows it into the atlas meets the same band, which WCAG 3.2.4's consistent identification favors.
3. **Rule 05.1 under DR-310.** On pages whose first screen is a drawing or a table on Newsprint, the band is that screen's dark element (6.2 percent of a 1440 by 900 window, by the specs' measure).
4. **My plan's sentence "never a dark panel" (section 3.1) predates D4-189.** I wrote it to keep the bar from reading as a banner; the band does that work through its markup and contents instead. I correct the plan (C6, under Done).

It stands on these conditions, all met today: it stays a `nav` with no wordmark or site parts; it holds no red; in the dark theme its bottom edge takes the 1 px `--oa-color-border-hairline-on-charcoal` so it does not merge into the ground (specs, shell section); and its words keep 4.5 to 1 through `.oa-surface-charcoal`'s tokens.

### R18. The loop index's grade column is each loop's grade line (batch 1, A15)

Written 23:20:20 UTC. R11 composes Loop R18's grade line from its stored `evidence` field, and the loop index (Rule 21.14) prints the same field for all 23 loops, so R11 applies to every row. In each row, every stored grade token (`documented`, `well-supported`, `plausible`, `plausible_contested`, `hypothesis`) becomes its Rule 13.3 display word, capitalized at the start of the field and after a semicolon and lowercase elsewhere, never with a hyphen or an underscore; every bare variable code becomes its chip; every other word stays as stored. A field that is one grade alone prints the display word alone: "Plausible", "Contested", "Hypothesis", "Well supported". Loop B4's row becomes "Well supported where seats are competitive; Variable C5 to Variable D5 well supported". T10 then reads these cells as composed text.

## Contracts

- For the engineer: C9's marks, with R1's additions (`data-atlas-reads` with directions, `data-weakest`, `data-part` in place of a kind on a part box, `data-lit`, `data-pathway`) and R2's method for each `data-count-of` key, in C9's naming. Aligned at 21:55:55 UTC.
- For the design director: R6's inks and R7's 390 px form; R10's red table; R12's range row.

## Sign-offs

### Batch 1 (A11 to A20), 23:20:20 UTC

**What I checked, and how.**
- **Data, by my own script, not the atlas test.** I wrote `signoff/check.py` in my scratch: it reads the six working exports (`work/build/exports/phase-4/20261122_Atlas-*.html`) and every frame of the ten plates (`work/build/app-kit/plates/a11.json` to `a20.json`), 59 pages in all, and checks each mark against the model by R1 to R18's methods. Run at 23:09 UTC: 1,560 typed IDs (each kind and ID in the model, each chip's words), 164 connection marks (sign, type, delay, grade), 2,544 counts (each key's method and its number in the words), 11 read-aloud lines (R4), 88 effect rows (code whole, true minus), 54 routes (check date or "Not checked"), every status date, every in-page evidence link's target, the lit parts, the weakest step (L15 only) and 18 stepper holds (L14 37 words, 9,250 ms; L15 64 words, 16,000 ms). **0 faults.** No bare ID in any text outside a chip.
- **Red, by pixels.** Every PNG export scanned for Pillar Red (23:08 UTC). Beyond the identity marks every chapter 20 page carries (the masthead's red ampersand and lockmark dot, and the footer lockmark's dot), red appears only on Reform R-23's page (two outlines, EC7 and A4) and Loop R18's page (the drawing alone, D4, L14 and L15), in light and dark, at 1440 and 390 px. None on the home, the Register, the loop index or How to read. In markup, every `data-red` mark is a target of its view's reform.
- **L15 against R14,** in the A14 export's markup and its 1440 px captures, light, dark and gray: 28 px solid lead-in with its two ticks; 8 px gap; red dashes 15.75 and 7.87 px, case 17.75 and 5.87 px offset 1 px, with 1 px stubs ringing the run's ends; the fit ending at the 6 px arrowhead's base; the red arrowhead with no edge; the case pinned to Charcoal in both themes (`.ws.wa .sv .rt .ak-case`). In gray it reads as a dashed line next to L14's solid one. **R14 holds.**
- **Stored text whole,** by script: Loop R18's summary, case, qualification and adaptation; PW06's short answer; Reform R-23's summary, problem, status and both remedy blocks; Reform R-35's remedy and its 87 percent route note; all ten D04 citations; D04's everyday question.
- **Both sides (plan 3.6, DR-55, DR-93).** Each view prints the finding each side may want to skip at the standing of its section: PW06's 254 percent figure and its Medicare outpatient sentence; the CBO estimate beside the $7.25 floor and 30 states; L14 documented beside R-35's finding of harm and its 87 percent note; R18's 2025 removals beside the 2021 removals and the plausible return step. Nothing added or softened.
- **By eye:** the 1440 px light captures of A11 to A16, A11's 1440 dark and 390 light, A13's and A14's 390 light, and A17 to A20 as headless screenshots of the engineer's scratch exports (23:14 UTC, load 0.03).

**Verdicts.** Every value on every view matches the model: IDs, signs, grades, delays, counts, effects, routes, dates and stored text. **Signed off on data for A11 to A20.** No view is signed off whole yet: each has display faults in its marks or layout, listed below with the request that fixes it.

| View | Data | Held for (request) |
|---|---|---|
| A11 home | Signed | Box text overflowing at 1440 (4); two counts run together (5); the main circuit lost at 390 (6); the key's words (7) |
| A12 reform R-23 | Signed | LE15 unnamed and a step from nothing (8); "As of" after the status (9); feasibility without its word (10); the spaced colon (11) |
| A13 Register, D04 | Signed | The grade head row (12); the record square (13); chips broken mid-word (14); the 390 px row heads hidden (15); R-35's targets and its date (16) |
| A14 loop R18 | Signed | The chooser's red, the engineer's E11c-2 (17); no note naming R-11's targets (18); the 390 px stepper in one column (19); an opening quotation mark (20) |
| A15 loop index | Signed | Grade words (21, R18); "No numbered chain" broken mid-word (22) |
| A16 How to read | Signed (its chips) | The red target sample drawn in ink (23); the authority diamond filled (24); the Documented sample (25); two samples without their words (26) |
| A17 every variable | Signed | A pill and the count line overflow the Checks box; a pill's words overflow it in Policy (27) |
| A18 Register, D10 | Signed | Requests 12 to 15 as on A13; the editor's words still missing (T16), so "reviewed connection LTR1" (R11) is not yet seen |
| A19 loop on step 2 | Signed | Held with A14 (17 to 19) |
| A20 claim open | Signed (CL1340's six fields and its source) | The field labels wait for the editor's words (T16) |

**The atlas test against these findings.** Its report (`atlas-test.json`, run 23:01:35 UTC) passes every check but T16 on every view, yet requests 8, 12 to 15, 17, 21 and 23 to 25 are faults the plan's checks name. Job 4 below says which check misses each and why.

### Job 4: the atlas test against plan section 8

Read whole between date reads at 23:14 and 23:19 UTC: `work/build/app-kit/tools/atlas_test.py`, 908 lines, SHA-256 19f6201f... Each check against the line it prints. "Tests its line" means the check would catch any page that breaks the condition as plan section 8 states it.

| Check | Tests its line? | What it misses |
|---|---|---|
| T1 Typed IDs | Yes | Alt text and `aria-label` are not read. A chip hidden by CSS (A13 at 390, request 15) counts as present |
| T2 Connection marks | **In part** | Reads the four attributes against the model, and a drawing only as solid or patterned: a plausible step drawn dotted passes. In a table row it fails a wrong grade word but never an absent one, and never reads the sign, type or delay words. It never checks the record square (requests 13, 25) |
| T3 Counts | Yes, for every marked count | A number printed without `data-count` is never read; chapter 28's line says "every count on an atlas page" |
| T4 Loops | **In part** | The read-aloud line and the weakest step, yes. "Kind matches its count of minus signs" is checked on the model, not on the page; the page's kind is checked only as the word appearing anywhere in it |
| T5 Authority | Yes | (The open diamond is Rule 15.5's, not T5's line; request 24 escapes every check) |
| T6 Red | **In part** | Only the chooser's state on load: R-15's and R-48's states are never read (E11c-2 escapes). It skips How to read's sample entirely, so a red target drawn in ink passes (request 23). It reads markup only: a red painted without `data-red` escapes; a pixel scan beside it would catch one. Its first `jobs =` line is dead code |
| T7 Effects | Yes | |
| T8 Routes and dates | Mostly | The words "As of" and their place before the status are not checked (request 9) |
| T9 Evidence a step away | **In part** | Checks every `data-evidence-href` and every connection chip; never a reform chip or a figure without a link, and never a drawn connection that no chip or link on the page names (LE15, request 8). In a frame every `#` link passes unread |
| T10 Grades in words | **In part** | R15's four points exactly. But it skips every `[data-atlas-field]`, so the loop index's grade column, composed text under R18, prints `plausible_contested` and passes (request 21). It never requires a display word to be present for a `data-grade` mark |
| T11 Stepper | Yes | (Buttons' layout at 390 px is AL-22's and no check's; request 19 escapes) |
| T12 Pressed and lit | **In part** | No check of the 2 px edge, and none of the lit parts being named in the status line, both in its line |
| T13 Colors | **In part** | Text at 4.5 to 1 from the measured words, yes. "Marks at 3 to 1 on the frame's pixels" is not measured: `atlas_contrast.py` puts four rows in each plate's `contrast`, and T13 reads none of them |
| T14 Type | **In part** | Sizes, yes. The one-word last line skips every label whose first line starts with a digit, which is every step label, the labels ED-F9 names. Chapter 15's approved typed step ("1 money," then "lowers") explains the skip; the exception should name that form, not every step |
| T15 Site frame | Mostly | The bar's name is not compared with "Atlas views"; Help's "Contact us" is read only through the group heads |
| T16 Words retired | **In part** | Its list holds one newspaper's name, "Times Explainer"; the other editorial system named for a newspaper, "Economist Register", is not on it (D2-65). It also carries the stand-in check (`⟦…⟧`), so a T16 FAIL today means missing words, not retired ones; that check wants its own line |

**The self-test** plants one fault a check (17 plants with T10's second) and, on the 23:01 report, catches all 17; it fails only because the clean pages are not quiet while the editor's words are missing. Each plant is the easiest case of its check, so none exercises the gaps above. Plants that would: a plausible step drawn dotted (T2); a minus row whose word reads "raises" (T2); red on a drawn variable the chosen reform does not target, and the chooser's second state (T6); a drawn connection named nowhere (T9); `plausible_contested` in a loop index grade cell (T10); a mark under 3 to 1 (T13); a two-line step label ending on one word (T14).

### Batch 2 (round 2, A11 to A20), November 23, 00:18:32 UTC

**What I checked, and how.**
- **Data, by my script again** (00:13 UTC), now resolving each frame's `<use>` of a plate symbol to the symbol's own markup (`signoff/pages.py`, `inline_uses`; every `oa-app-wa-*` reference in the ten plates resolved) and reading each chooser state by its `data-atlas-for` wrapper: the six exports and every plate frame, 1,336 IDs, 110 connection marks, 1,733 counts, 5 read-aloud lines, 76 effect rows, 48 routes, 14 holds (L14 9,250 ms, L15 16,000 ms). **0 faults**, no bare ID. Red by state: R-11 lights D4, L14 and L15; R-15 and R-48 light L14 and L15 only; R-23 lights EC7 and A4; How to read's key sample only.
- **Red, by pixels** (00:13 UTC): as in batch 1, and now How to read's sample is red (434 px at 1440 and at 390).
- **By eye:** the 1440 px light captures of A11 to A16 at every fixed item; A11 and A14 at 390 light; A13 at 390 light; zooms of How to read's red target and open diamond; a scratch copy of A14's export with Reform R-15 checked, rendered headless (00:15 UTC, load 0.05): D4 in ink, L14 and L15 red, the note and tags changed. A17 and A18 seen as headless renders of the engineer's round 2 exports in his scratch (`r2/out`, 23:58 UTC run; their plates' frame markup matches the repository plates written 00:08 UTC). A19's and A20's frames read in markup.
- **Lit and muted edges, by pixels,** on A11 at 1440 and 390, light and dark.

**Fixed and seen:** 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17 (E11c-2), 18, 19, 20, 21, 22, 23, 24, 25, 26; 27 in part (boxes hold their pills and counts); R16 and R18 in place; A18's "reviewed connection LTR1" (R11); A20's field labels.

**Status by view:**

| View | Status | Still failing |
|---|---|---|
| A11 home | **Held at 390 px** (1440 passes) | 29, 30 |
| A12 reform R-23 | **Signed off whole** | |
| A13 Register, D04 | **Signed off whole** | (The C5 index screen is the design director's) |
| A14 loop R18 | **Signed off whole** on my items | (The dark drawing crop is the design director's; R-15's "Its other targets ... sit" singular is the editor's `chosen_off`) |
| A15 loop index | **Signed off whole** | |
| A16 How to read | **Signed off whole** | |
| A17 every variable | **Held** | 31 |
| A18 Register, D10 | **Signed off whole** | |
| A19 loop on step 2 | **Signed off whole** | (as A14) |
| A20 claim open | **Signed off whole** | |

**Job 4 follow-up:** the test's new branches and plants, read by search at about 00:18 UTC (not re-read whole; SHA-256 a3fe5540...), cover each gap request 28 named: hidden row heads (T1), texture by grade, the sign word and the record square (T2), every chooser state and the key's red sample (T6), drawn connections named by a chip (T9), loop grade cells (T10), the plate's measured ratios (T13), the typed-step exception (T14), "Economist Register" (T16). Requests 29 to 31 are not covered by any check; 30 and 31 are visual and would need the kit's measure.

## Done

- Rulings R1 to R13, in this file by 21:53 UTC (`date -u` 21:53:52), five minutes after the start at 21:48.
- R1 and R2 aligned with the engineer's contract C9 at 21:55:55 UTC: C9's count keys and marks stand, R2 fixes each key's method, and R1 adds directions to `data-atlas-reads`, `data-weakest`, and `data-part` in place of a kind on a part box.
- **Appendix A rerun (brief 6.2, job 2).** The script copied unchanged from the plan to my scratch (`ch21_queries.py`, SHA-256 84cfd834...), run under the lock from the project folder with `python3 -I` at 21:54:10 UTC, exit 0, on the model with SHA-256 ef1028ac87e402e30af9e3cda234fed63794b5570d0a165b9dab39073e08c7f2 and `tokens.css` 3ecfb1cb... Its output is **identical, byte for byte, to Appendix B** (30,336 bytes, all 17 queries). No value differs, so no value in the plan changed. (C1 to C5 below change wording on a contested remedy's length, for R15, not values.)
- Beyond Appendix A, a second script (`ruling_checks.py` in my scratch, run 21:54:56 UTC, exit 0) checked: the plan's index table in section 3.4 against the model, 13 rows, no mismatch; the plan's D04 connection table, 10 rows (from, to, sign, type, delay in words, grade word, and that each files on D04), no mismatch; R8's weakest-step method on all 20 numbered loops, every one passing its check (R18: L15; R7 and R8 name none); R4's directions on all 20, each ending the way its kind says (17 reinforcing return the same way, 3 balancing the other way), with no authority connection in any loop; R5's figure rule on PW06, where 254% with 2022 finds exactly one claim, CL1340; R7's sums, 27 outgoing lines totalling 81, plus 37 inside, 118; the lit parts of PW06, A, D and EC; the D04 filter, 9 of 20; the red targets of R-23 (EC7, A4) and R-11 (D4, L14, L15), R18's reforms by their own records (R-11, R-15, R-48) and R-35 rejected; and the bare IDs inside the stored prose the four views print. Only Loop R18's grade text (D2, D4, D4, D2, all variables) and its evidence summary (L14, L15, connections) hold any; none is one of the colliding codes B2 to B5.
- Written: `work/handoffs/phase-4/20261122_Chapter-21-Query-Results.json` (47,105 bytes, valid JSON, written 21:55:13 UTC): the run's details, the comparison, all 17 queries' output lines, and the second script's results.
- R14 (a red target on a patterned line) and R15 (T10 and a contested remedy), at the main session's request; R13's sign-off line now follows R15. Written by 22:26:44 UTC.
- **Plan corrections, chat 11c,** each in `work/handoffs/phase-4/20261121_Chapter-21-Plan.md`, with a dated note under its opening paragraph (22:27:15 UTC; C5 at 22:27:48 UTC). A copy of the plan before them is in my scratch, `plan_before_C1-C4.md`. They follow DR-314 and DR-323 (Rule 01.22's and Rule 13.12's "at the length the record holds") and R15; H08 sets title verbs, not length.
  - C1, section 3.3's Entry: "print both readings at the same length (house rule H08)" becomes "print both readings its record holds, each at the length the record holds (DR-314, DR-323; chat 11c ruling R15)".
  - C2, section 3.3, item 4: "side by side at the same length" becomes "side by side, the stored text whole and in order, split at one sentence".
  - C3, Rule 21.4's specifications: "each the same length within a line, each with its source a step away (H08)" becomes "the stored text whole and in order, split at one sentence into two readings, ... each at the length the record holds, each with its source a step away (DR-314, DR-323; R15)".
  - C4, section 8, T10's pass condition: R15's condition in place of "within a line's length of each other (H08)".
  - C5, Rule 21.4's draft rule: "print both readings at the same length" becomes the editor's chat 11c words, "set the readings its record holds side by side, in the atlas's own words" (their Request 2). Draft words stay the editor's to finish.

- R16, R17 and R18, and sign-off batch 1 with job 4's reading of the atlas test, written by 23:20:20 UTC.
- **Plan correction C6** (`work/handoffs/phase-4/20261121_Chapter-21-Plan.md`, section 3.1, 23:20:29 UTC; copy before it in my scratch, `plan_before_C6.md`): "The title bar takes the page's own ground, Newsprint or Charcoal, and is never a dark panel" becomes the Charcoal band that chapter 20 as built and D4-189 set, by R17; logged in the plan's dated note.

## Requests

- **1. To the engineer, R14 (written 22:27:48 UTC):** in `work/build/app-kit/tools/atlas_figures.py`, draw L15's red target as R14 sets it: case dashed on the red's rhythm, each case dash 2 px longer and offset 1 px back; the pattern at 4 px (16 and 8 px) fitted to the run from the lead-in's 8 px gap to the 6 px arrowhead's base; the 28 px lead-in solid; tag, ticks and arrowhead as chapter 15's `rt` block draws them; the case stroked with `--oa-color-graphic-essential-on-newsprint` in both themes, on L14's solid target too. Then L15 leaves `not_red`, and T6 should pass on A14.
- **2. To the engineer, R15:** T10's contested-remedy check as R15's four points, with System 1's sentence splitter shared by the kit and the test, and each block's words and 1440 px line count printed in the line. Length never fails it.
- **3. To the design director, R15:** `work/handoffs/phase-4/20261122_Atlas-View-Specs.md`, the reform view's row "The remedy" (about line 244): "their lengths within one line of each other at 1440 (T10, H08)" becomes "each at the length the record holds, both with the same standing (R15; DR-314, DR-323)". The split at `remedy_split: 4` stands; it separates the two readings.
- **Batch 1 requests, written 23:20:20 UTC.** Owners as the brief's section 4 sets them; the main session relays.
- **4. Engineer (A11, A17; `atlas-page.css`):** at 1440 px the count lines overflow three boxes: in Checks, "7 variables 7 connections inside" runs under the box's bottom edge into the flow labels; in Your household, "This question reaches here" sits on the box's bottom edge; in Technology, its count line sits on it. Grow each box to hold its words, or move the flows that run under it.
- **5. Editor and engineer (A11 at 1440 and 390, A17):** each box prints its two counts as one run, "6 variables 6 connections inside", which reads as "6 variables 6". Set them apart, on two lines or with words between them; the editor's words.
- **6. Engineer (A11 at 390):** every outgoing line prints bold, and no key appears, so the main circuit cannot be told from the other flows. R7: the main-circuit line bold with the key's words, the rest regular.
- **7. Editor (A11's key):** "Other flows Each number counts connections" runs two phrases together; it needs its stop.
- **8. Engineer and editor (A12):** the drawing joins EC7 and A4 by Connection LE15, but no chip, words or link name it, so its documented grade, under-2-year delay and line are a step from nothing (Rules 13.4, 21.7; plan 3.3 item 2). Add the chip Connection LE15 with its name and its marks in words beside the drawing ("raises, under 2 years, Documented" with the record square), linked to `#register-le15` on sheet EC.
- **9. Engineer (A12):** "As of October 15, 2026" prints after the status words; Rule 13.10 puts "As of" and the date before them.
- **10. Editor (A12, A13, A14 routes):** feasibility prints as a bare "high", "medium" or "low". Chapter 15's route rows print "High feasibility" (Rule 15.16's form).
- **11. Engineer (A12):** the tag line reads "Variable A4 : Reform R-24 ..." with a spaced colon; drop the space before it, or set the chip as the line's head.
- **12. Engineer (A13, A18, head row on Charcoal):** at 1440 px "Documented" and "Well supported" collide ("Documentedsupported") and "Hypothesis" is clipped by the table's right edge. Widen the grade columns or let the head wrap within its own cell.
- **13. Engineer (A13, A18, rows and the 390 px key):** R3 and Rule 13.4 put the 7 px record square inline before the word Documented. The head sample has none; in the rows and the phone key the square sits after the arrowhead and wraps away from the word.
- **14. Engineer (A13, A18 at 1440):** the first column breaks the chip's kind word mid-word ("Connec / tion L10"). Rule 13.9 holds a chip on one line; widen the column or keep the chip from wrapping.
- **15. Engineer (A13, A18 at 390, light and dark):** the restyled table hides each row's head: the index cards begin "Variables: 3" with no sheet chip or title, and each connection block begins "From, to:" with no Connection chip. Show the row's `th` as each card's head (specs: "the sheet's chip and title on a line"). The test cannot see this (T1, job 4).
- **16. Engineer and editor (A13, R-35):** the rejected option never names its targets, Connections L18 and L19, so a reader cannot see why it files on D04 (plan 3.4, Rule 21.10). Name both in ink chips, linked to their lines. Its effects also want "As of October 15, 2026" over them, as on every reform (Rule 15.16).
- **17. Engineer (A14, A19 working pages; the engineer's E11c-2):** choosing R-15 or R-48 leaves R-11's red; Variable D4 stays red though neither targets it. R10 moves the red with the choice: R-15 lights L14 and L15 (its third target, L16, is not on this loop; its panel names it in words), R-48 lights L14 and L15, and D4 returns to ink. The ink tags change with it ("Reform R-11 and Reform R-48 also aim here" when R-15 is chosen). T6 should read each chooser state.
- **18. Engineer and editor (A14, A19):** no note names the chosen reform and its targets beside the drawing. Rule 12.5 asks one: "Reform R-11 acts where the marks turn red: on Variable D4, Connection L14 and Connection L15" (draft), changing with the chooser.
- **19. Engineer (A14, A19 at 390):** the stepper's buttons stack one to a row. AL-22 asks a two-by-two grid on phones in reading order, Play and Reset the loop, then Previous step and Next step (plan 3.5).
- **20. Engineer (A14):** Loop R18's case stores `'almost undoubtedly'` with straight marks, and the page prints `’almost undoubtedly’`, its opening mark turned the wrong way. Print the stored marks as stored (DR-37), or pair them as ‘ and ’.
- **21. Engineer (A15):** the grade column prints stored spellings ("plausible_contested", "well-supported", a lowercase "plausible" standing alone). R18 sets every row; T10 should read these cells (job 4).
- **22. Engineer and editor (A15):** "No numbered chain" in the Steps and Minus signs columns breaks mid-word ("numbere / d chain"). Print a short word the column holds, such as "None", and let the closure column explain it.
- **23. Engineer (A16):** the "Red target" sample draws in ink, not red: its svg class `tgt` has no style, `.ln .ak-case{stroke:none}` removes the case, and both the 2 px and the 6 px tag and arrowhead show, the larger arrowhead running into the words' column. Give it the `rt` style (4 px red on the 6 px Charcoal case, the 6 px marks only) and keep it in its cell. No PNG of A16 holds red beyond the masthead's and footer's identity marks (scan at 23:08 UTC).
- **24. Engineer (A16):** the "Open diamond, decides" sample fills its diamond in ink; `.dm`'s open style is scoped to `.wa-tagm` only. Rule 15.5: an open diamond, surface fill, 2 px ink edge.
- **25. Engineer (A16):** the Documented sample sets the record square after the arrowhead, while its own words say "with a filled square before the word". Put the square before the row's word Documented (Rule 13.4).
- **26. Design director (A16; suggestions):** the "Weakest step" sample is a plain dashed line, the same as Plausible's; add the words "weakest step" under it as the drawings print them. The "Pressed question" sample is a box with a check and no words; Rule 17.10's look is the check, bold words and the 2 px edge.
- **27. Engineer (A17):** with every variable shown, the Checks box's seventh pill ("Entrenched control of rule-setting institutions") and its count line run past the box's bottom into the flows, and in Policy the first pill's words overflow its outline. Grow the boxes to their pills.
- **28. Engineer (the atlas test, job 4):** close the gaps in job 4's table, and add the plants it lists, so the test catches requests 8, 13, 15, 17, 21 and 23 to 25 the next time they occur. The most urgent are T6 (every chooser state, and How to read's sample), T9 (drawn connections) and T10 (loop grade lines).
- **Batch 2 requests, written 00:18:32 UTC.**
- **29. Engineer and editor (A11 at 390 px):** the list codes the main circuit by weight, bold beside regular, but the key under it still shows two line samples, Charcoal and Stone, which match nothing in the list; at 390 the second sample also sits at the end of the first line, away from its words. At this width the key says what the list draws, such as "Bold: the main circuit, part to part. Regular: other flows. Each number counts connections." (the editor's words), with no line samples.
- **30. Engineer (A11 at 390 px, light and dark):** with the question pressed, all eight cards keep an ink edge, so the five parts it does not reach are not muted as they are at 1440 (R6, R7; Rule 17.8). Give those cards the muted edge, `--oa-color-state-muted-mark-on-newsprint` and `-on-charcoal`. Measured by pixels at 00:18 UTC: Outside forces, Voice and the lit Wealth all edge in #121212 on Newsprint and #DCD9D2 on Charcoal. I missed this in batch 1.
- **31. Engineer (A17):** the boxes now hold their pills, but in the narrow Checks and Policy columns a pill's three lines still meet its rounded ends: "organized interests" crosses the outline left and right, and "Policy advantages" and "Presidential action" touch it. An 8 px inset holds on the straight sides only; at a pill's ends the inset must follow the curve (a 76 px pill's ends have a 38 px radius), or the words wrap to a narrower measure on their first and last lines.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Tested

- Model SHA-256 read 21:48 UTC: begins ef1028ac87e402e3, as the brief names.
- The sentences holding "weak" in all 20 numbered loops' evidence summaries, printed by script beside each loop's least certain steps (21:50 UTC). R8's method itself then ran by script at 21:54:56 UTC and gave the list R8 prints.
- The contested flag against `plausible_contested` on all 118 connections (21:50 UTC): they agree, 7 and 7.
- ID collisions across the ten kinds, sources and reviewed connections (between 21:50 and 21:52 UTC): only B2, B3, B4 and B5, variable and loop.
- Appendix A rerun against Appendix B, byte for byte (21:54:10 UTC): identical.
- The plan's two tables in section 3.4 against the model, and the rulings' checks listed under Done (21:54:56 UTC).
- `git status` (21:55 UTC): my only files are this notes file and the query results; no stray file of mine in the project.
- R-23's stored remedy text split by System 1's splitter (22:26:07 UTC): four sentences of 8, 21, 13 and 38 words, blocks of 42 and 38 at `remedy_split: 4`, rejoining to the stored text exactly; R-23 is the model's only reform whose remedy is graded contested.
- L15's run in the figure step's A14 output (run under the lock between 22:22 and 22:26 UTC; read by script at 22:26:07): 28 px lead-in, then about 196 px at the 2 px gap; about 192 px to the trimmed end and about 180 px to the 6 px arrowhead's base at 4 px.
- Chapter 15's `rt` block, `conn()` and System 1's `wire_marks`, `pattern`, `fitted`, `tick_marks`, `TAG` and `ARROW`, read for R14; and the dark theme's `--oa-color-graphic-essential` in `tokens.css`.
- The plan before and after C1 to C5, by `diff` against my scratch copy: only the five lines and the dated note moved.
- Batch 1's data check, `signoff/check.py` (23:09 UTC), and its pixel scan, `signoff/redscan.py` (23:08 UTC), in my scratch, as the Sign-offs section lists; the landmark count of the six exports and the stored-text check (both between date reads at 23:09 and 23:14 UTC); headless screenshots of A17 to A20 at 1440 px from the engineer's scratch exports (23:14 UTC, load 0.03, one browser at a time, closed after each).
- The atlas test read whole (908 lines) against plan section 8; its 23:01:35 UTC report read for every FAIL line.
- Batch 2 (from 00:12:56 UTC): the data check with symbols and chooser states resolved (00:13:34 UTC); the pixel red scan (00:13:42 UTC); crops of every fixed item; the R-15 chooser state rendered from a scratch copy (00:15 UTC); A17 and A18 rendered from the engineer's `r2/out` exports and A17 to A20's plate pages (00:16 to 00:17 UTC, load under 0.1, one browser at a time); card edges sampled at 390 px (between 00:17 and 00:18:32 UTC).

## Not tested

- The plan's prose values outside Appendix B and the two tables of section 3.4 were not parsed one by one; each carries its query tag, and every tagged query's output matches Appendix B exactly.
- Chapter 15's `effect_rows` was read, not run, for R12's finding that it stops on a range code.
- R14 is not yet drawn, so the gray reading it predicts rests on luminance arithmetic, not on a capture; I check it at sign-off on the A14 frames, in color and in grayscale.
- Whether chapter 15's own plates draw a red target on Charcoal with a Newsprint case (R14 (d)).
- Batch 1 looked by eye at the 1440 light captures of A11 to A16, A11 dark and 390 light, A13 and A14 at 390 light, and A14's drawing in dark and gray. The other dark captures (A12, A13 at 1440 and 390; A14 at 390 dark) were checked by pixels for red and inks only, and A11's dark inks by sampled pixels.
- A17 to A20 were seen only as headless screenshots of the engineer's scratch exports at 1440 px, in their state on load: A19's step 2 and A20's open claim were read in the plates' frame markup, not seen drawn.
- I ran neither the atlas test nor its self-test; I read its code and its 23:01:35 report.
- Batch 2: A17 and A18 were seen from the engineer's 23:58 UTC scratch run, not the repository run of 00:06 to 00:08 UTC; their plates' frame markup matched, but I did not render the repository plates themselves (their page needs the guide's styles). A12, A13 and A14 at 390 dark and A12 at 390 light were checked by pixels and markup only. The R-48 state was checked in markup, not rendered. I did not run the atlas test or its self-test, and read the test's new code by search only.
