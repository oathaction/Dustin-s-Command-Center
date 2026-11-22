# Chat 11c: data visualization lead's notes

Data visualization lead, Phase 4, chat 11c, November 22, 2026. Started 21:48 UTC (`date -u`). Brief: `work/handoffs/phase-4/20261122_Chat-11c-Brief.md`, section 6.2. Plan: `work/handoffs/phase-4/20261121_Chapter-21-Plan.md`. Model: `work/extract/atlas-v7-data.json`, SHA-256 ef1028ac87e402e30af9e3cda234fed63794b5570d0a165b9dab39073e08c7f2 (read 21:48 UTC). Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/e76584b2-1bba-5266-a75e-730f247433d8/scratchpad/c11c/dataviz-lead/`.

## Routine calls

- D4-xxx | The weakest step is read from the loop's evidence summary by one fixed method (R8), checked against the least certain grade | Rule 15.13's builder line asks for both and a stop when they disagree; two summaries (R7, R8) name no connection, so the method needs a defined outcome for them
- D4-xxx | A range effect code such as "0 to −S at high bite" draws both ends on Rule 13.5's pip scale, joined, with the code whole (R12) | chapter 15's `effect_rows` stops on any range ("draw it before printing it"), and Reform R-23's economic performance row is a range
- D4-xxx | The 390 px home drawing lists each part's outgoing flows only, so each of the 27 pairs prints once (R7) | listing incoming flows too would print every count twice and break T3's sum

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

I read each view's selection from both sides at sign-off, against plan 3.6's table, and each finding at the grade the model gives it. A view passes when the finding each side may want to skip prints at the same prominence as the rest of its section, with nothing added or softened. Specifically: on the reform page both readings of the contested remedy sit side by side within a line's length of each other (H08, T10); on the loop page the case and the adaptation both print whole as stored; on the Register, Reform R-35 prints with its grade and the atlas's words on what the grade measures, and its route note (the 87% figure) prints as stored where routes print.

## Contracts

- For the engineer: C9's marks, with R1's additions (`data-atlas-reads` with directions, `data-weakest`, `data-part` in place of a kind on a part box, `data-lit`, `data-pathway`) and R2's method for each `data-count-of` key, in C9's naming. Aligned at 21:55:55 UTC.
- For the design director: R6's inks and R7's 390 px form; R10's red table; R12's range row.

## Done

- Rulings R1 to R13, in this file by 21:53 UTC (`date -u` 21:53:52), five minutes after the start at 21:48.
- R1 and R2 aligned with the engineer's contract C9 at 21:55:55 UTC: C9's count keys and marks stand, R2 fixes each key's method, and R1 adds directions to `data-atlas-reads`, `data-weakest`, and `data-part` in place of a kind on a part box.
- **Appendix A rerun (brief 6.2, job 2).** The script copied unchanged from the plan to my scratch (`ch21_queries.py`, SHA-256 84cfd834...), run under the lock from the project folder with `python3 -I` at 21:54:10 UTC, exit 0, on the model with SHA-256 ef1028ac87e402e30af9e3cda234fed63794b5570d0a165b9dab39073e08c7f2 and `tokens.css` 3ecfb1cb... Its output is **identical, byte for byte, to Appendix B** (30,336 bytes, all 17 queries). No value differs, so the plan needs no correction and none was made.
- Beyond Appendix A, a second script (`ruling_checks.py` in my scratch, run 21:54:56 UTC, exit 0) checked: the plan's index table in section 3.4 against the model, 13 rows, no mismatch; the plan's D04 connection table, 10 rows (from, to, sign, type, delay in words, grade word, and that each files on D04), no mismatch; R8's weakest-step method on all 20 numbered loops, every one passing its check (R18: L15; R7 and R8 name none); R4's directions on all 20, each ending the way its kind says (17 reinforcing return the same way, 3 balancing the other way), with no authority connection in any loop; R5's figure rule on PW06, where 254% with 2022 finds exactly one claim, CL1340; R7's sums, 27 outgoing lines totalling 81, plus 37 inside, 118; the lit parts of PW06, A, D and EC; the D04 filter, 9 of 20; the red targets of R-23 (EC7, A4) and R-11 (D4, L14, L15), R18's reforms by their own records (R-11, R-15, R-48) and R-35 rejected; and the bare IDs inside the stored prose the four views print. Only Loop R18's grade text (D2, D4, D4, D2, all variables) and its evidence summary (L14, L15, connections) hold any; none is one of the colliding codes B2 to B5.
- Written: `work/handoffs/phase-4/20261122_Chapter-21-Query-Results.json` (47,105 bytes, valid JSON, written 21:55:13 UTC): the run's details, the comparison, all 17 queries' output lines, and the second script's results.

## Requests

None yet.

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

## Not tested

- The plan's prose values outside Appendix B and the two tables of section 3.4 were not parsed one by one; each carries its query tag, and every tagged query's output matches Appendix B exactly.
- Chapter 15's `effect_rows` was read, not run, for R12's finding that it stops on a range code.
- No view has landed yet, so no sign-off has run (job 3), and the atlas test is not yet written (job 4).
