# Atlas V7.1 issue list

For the atlas editor. Prepared by the data visualization and systems lead on October 21, 2026, under Dustin's decision DC-08 ("Prepare them for an atlas V7.1").

Every value below was read by script from the Atlas V7 snapshot of 2026-10-15 (`work/extract/atlas-v7-data.json`) and the extracted renderer (`work/extract/atlas-v7/script.js`). Script: `work/build/scripts/phase-1/build_v71_issue_list.py`. Nothing in V7 was changed. V6 never edits the model; the last line of each item says how the guide handles the issue until V7.1 exists.

How to read an item: **Where** gives the JSON path (or renderer location), **Evidence** quotes or counts what V7 holds, **Fix** is the proposal, and **V6 works around it** says what the guide does meanwhile. Items 1 to 22 are in the model JSON; the rest are in the renderer, which ships in the same atlas file.

| # | Issue | Where | Kind |
|---|---|---|---|
| 1 | Grade vocabulary differs across record types | `links[].evidence` | Model |
| 2 | The `contested` flag repeats the `plausible_contested` grade | `links[].contested` | Model |
| 3 | Issue remedy grades live only as the first word of a note | `issues[].remedy_note` | Model |
| 4 | Mixed is defined, nearly unused and missing from the glossary list | `methods.how_claims_are_assessed` | Model |
| 5 | Not yet tested appears in the glossary and renderer, in no record | `glossary` term "Confidence label" | Model |
| 6 | A status sits in the grade field of one issue | `issues.I128.grade` | Model |
| 7 | Two definitions of well supported | `methods.how_claims_are_assessed` | Model |
| 8 | D6 is typed as a flow and described as a stock | `nodes.D6.type` | Model |
| 9 | Most route entries have no check date | `reforms[].routes[].checked` | Model |
| 10 | Effect values extend the seven codes with qualifiers and ranges | `reforms[].effects` | Model |
| 11 | Effect confidence is free text on a third scale | `reforms[].effects_confidence` | Model |
| 12 | Identifiers collide across kinds | IDs in `nodes`, `loops`, `reforms`, `domains`, `issues` | Model |
| 13 | The glossary's driver pills do not match the renderer | `glossary` term "Outside driver" | Model |
| 14 | Source count and register size differ without a label | `meta.counts.sources` | Model |
| 15 | Issue count includes a retired record | `meta.counts.issues` | Model |
| 16 | Conceptual loop chains mix labels and IDs | `loops.B2.chain` | Model |
| 17 | Conceptual loops carry loop grades without numbered steps | `loops.B2.evidence` | Model |
| 18 | Delivery log dates are free text in several formats, out of time order | `deliveryLog.rows[].date` | Model |
| 19 | Mixed names a direction, a jurisdiction and a grade | `repairLog.rows[].direction` | Model |
| 20 | Log rows reference loops by text | `repairLog.rows[].loop` | Model |
| 21 | Some variables carry two domains in one string | `nodes[].domain` | Model |
| 22 | Effect codes and delay codes share the letters S, M and L | `reforms[].effects` | Model |
| 23 | Two words for areas | renderer `KIND_LABEL` (`script.js` line 159) | Renderer |
| 24 | Documented and well supported draw the same line | renderer legend and `.edge` styles | Renderer |
| 25 | Conceptual steps are close to the plausible dash | renderer `.edge.u-concept` | Renderer |
| 26 | Authority links end in an arrowhead | renderer markers (`-t` teal arrowhead) and `.edge.authority` | Renderer |
| 27 | Interface palette and fonts | renderer styles | Renderer |

## 1. Grade vocabulary differs across record types

- **Where:** `links[].evidence`; `issues[].grade`; `claims[].confidence`; `reforms[].problem_evidence.grade`; `reforms[].remedy_evidence.grade`; `deliveryLog.rows[].evidence_grade`; `loops[].evidence`
- **Evidence:** Connections: `well-supported` 37, `plausible` 35, `documented` 32, `plausible_contested` 7, `hypothesis` 7. Issues: `well_supported` 89, `documented` 70, `plausible` 32, `hypothesis` 2, `retired` 1. Claims: `documented` 321, `well-supported` 56, `plausible` 38, `contested` 18. Reform problem evidence: `documented` 34, `well-supported` 13, `plausible_contested` 2, `plausible` 1. Reform remedy evidence: `plausible` 29, `well-supported` 11, `hypothesis` 7, `plausible_contested` 2, `contested` 1. Delivery log: `well-supported` 12, `documented` 10, `plausible` 2. Loops hold free text, for example R10: "documented for C1 to C2; well-supported for C2 to C3; plausible for C3 to C4 (the weakest link)". Well supported is spelled `well-supported` in five fields and `well_supported` in one; contested is `plausible_contested` on connections and `contested` on claims, and reform remedies use both.
- **Fix:** Pick one stored code per grade (for example `well-supported` and `contested`) and use it in every field. If `plausible_contested` should stay a separate grade from `contested`, define it in the methods text and the glossary. Give loops a grade field for the weakest step and keep the free text as a note.
- **V6 works around it:** Yes. The guide shows one display word per grade from a mapping table (Systems Marks Board, Mark 2) and keeps V7's stored code in record panels and downloads.

## 2. The `contested` flag repeats the `plausible_contested` grade

- **Where:** `links[].contested`
- **Evidence:** The flag is true on 7 connections (L09, L47, LE04, LE06, LT04, LT05, LT12), exactly the 7 graded `plausible_contested`.
- **Fix:** Drop the flag, or document it as derived from the grade so the two cannot drift apart.
- **V6 works around it:** Yes. The guide reads the grade field only.

## 3. Issue remedy grades live only as the first word of a note

- **Where:** `issues[].remedy_note`
- **Evidence:** First words: `Hypothesis` 90, `Plausible` 68, `Well supported` 27, `Documented` 6, `Contested` 1, `Retired` 1, `Mixed` 1. No issue record has a remedy grade field, while reforms keep `remedy_evidence.grade` as a field.
- **Fix:** Add `issues[].remedy_grade` with the same codes as other grade fields, and keep the note as prose.
- **V6 works around it:** Yes. The guide parses the first word, as V7's renderer does (`leadGrade`).

## 4. Mixed is defined, nearly unused and missing from the glossary list

- **Where:** `methods.how_claims_are_assessed`; `glossary` term "Confidence label"; `issues.X16.remedy_note`
- **Evidence:** The methods text defines it: "Mixed means the evidence points in different directions for different parts of a claim." One record uses it, as the first word of issue X16's remedy note ("Mixed. Restoring voting rights on release is a documented fix, as is North Dakota's 2020 consent decree, which lets trib…"). The glossary's confidence label list reads: "The short label on a claim or response saying what kind of evidence supports it: documented, well-supported, plausible, contested, hypothesis or not yet tested. The same scale grades connections on the map." It omits Mixed.
- **Fix:** Either add Mixed to the glossary list and to a grade field where it applies, or remove it from the methods text and recode X16.
- **V6 works around it:** Yes. The guide's display list includes Mixed and shows it only where a record uses it.

## 5. Not yet tested appears in the glossary and renderer, in no record

- **Where:** `glossary` term "Confidence label"; renderer `GRADES` table (`script.js` line 100)
- **Evidence:** Records that use it: 0. The methods text does not define it. The renderer text: "No evaluation of this response's effects exists yet."
- **Fix:** Define it in the methods text if responses will carry it, or remove it from the glossary list.
- **V6 works around it:** Yes. The guide keeps the word in its key, marked as reserved.

## 6. A status sits in the grade field of one issue

- **Where:** `issues.I128.grade`; `issues.I128.retired`
- **Evidence:** I128 "Broad access to asset ownership (retired record)" has `grade: "retired"` and `retired: true`. Its status text: "Retired record, merged into loop R1: Wealth and political influence reinforce each other. Kept for reference only."
- **Fix:** Set the grade to the record's last grade or to null, and keep retirement in `retired` and `status`.
- **V6 works around it:** Yes. The guide shows Retired as a status chip, never as a grade.

## 7. Two definitions of well supported

- **Where:** `methods.how_claims_are_assessed`; `glossary` term "Well-supported"
- **Evidence:** Methods: "Well supported means strong evidence backs the direction: a well-designed study such as a randomized experiment, several consistent studies, or an official estimate made with a published method, with no credible study finding the opposite." Glossary: "The confidence label for a relationship on which several credible studies, designed to rule out other explanations, agree about direction. Each study's setting and limits still apply." The methods text allows one well-designed study or an official estimate; the glossary asks for several studies that agree.
- **Fix:** Use one definition in both places.
- **V6 works around it:** Partly. The guide's gloss ("strong studies agree on the direction") fits both; it quotes neither until they agree.

## 8. D6 is typed as a flow and described as a stock

- **Where:** `nodes.D6.type`; `nodes.D6.kind_plain`
- **Evidence:** `type: "flow"`. `kind_plain`: "Stock (an amount built up over time). The listed indicators count adoptions per year, which is a flow; the stock would be the number of reforms in force or the legal room states and localities have to act."
- **Fix:** Set `type` to `stock` and keep the indicator note, or rewrite `kind_plain` to explain why the variable is a flow.
- **V6 works around it:** Yes. The guide prints V7's `type` and quotes the `kind_plain` text in the record panel, so the conflict stays visible.

## 9. Most route entries have no check date

- **Where:** `reforms[].routes[].checked`
- **Evidence:** 13 of 126 entries carry a date, all 2026-10-15: R-01 BI, R-01 LOC, R-08 BI, R-09 FS, R-19 FS, R-21 ENF, R-29 FS, R-37 SS, R-38 SS, R-39 FA, R-40 LOC, R-44 ENF, R-45 SS. The other entries are null. Reform R-01 has dates for BI and LOC and none for SS and FS, though its status was checked 2026-10-15.
- **Fix:** Add a check date to every route entry, or store an explicit state such as `"not checked"` with a reason.
- **V6 works around it:** Yes. The guide prints "no check date in V7" for a null date and never infers one from the reform's status date.

## 10. Effect values extend the seven codes with qualifiers and ranges

- **Where:** `reforms[].effects`
- **Evidence:** 38 of 200 values are not one of the seven codes. Examples: R-06 DQ "+L local"; R-07 DQ "+S entry; -S extremity"; R-09 DQ "+S direct; trust +M if enforced"; R-11 DQ "+M precondition"; R-12 DQ "+M / -M risk"; R-16 DQ "+M structure"; R-16 EQ "+S indirect, decades"; R-19 EP "+M sector". 6 values on live reforms state a cost: R-07 DQ "+S entry; -S extremity"; R-12 DQ "+M / -M risk"; R-21 EP "0 to -S short run"; R-22 EP "0 to -S covered employment"; R-23 EP "0 to -S at high bite"; R-28 EP "0 to -S".
- **Fix:** Store each effect as a code plus structured extras, for example `{"code": "0", "range_to": "-S", "qualifier": "short run"}`, and keep the display string.
- **V6 works around it:** Yes. The guide's pips read the codes in each string, and the words beside them quote V7's full value.

## 11. Effect confidence is free text on a third scale

- **Where:** `reforms[].effects_confidence`
- **Evidence:** 11 of 50 reforms use a single level and 39 use scoped text, for example R-01: "medium (participation); low (moderation)". The levels high, medium and low also name route feasibility.
- **Fix:** Store confidence per outcome family or per named scope, with the level as a code.
- **V6 works around it:** Yes. The guide prints it as "Confidence in the effect: …", apart from the grade and the effect mark.

## 12. Identifiers collide across kinds

- **Where:** IDs in `nodes`, `loops`, `reforms`, `domains`, `issues`; renderer `ambiguousCode` (`script.js` line 196)
- **Evidence:** Identical codes: B2, B3, B4, B5 name both a variable and a loop. Codes that match once a hyphen or leading zero is set aside: loop and reform R1, R10, R11, R12, R13, R15, R16, R18, R2, R3, R5, R6, R7, R8, R9; variable and domain D1, D2, D3, D4, D5, D6, D7; variable and issue X1, X2, X3, X4, X5. Variable B1 sits beside loop B1a. V7's methods text says: "Identifiers are exact: R-05 is a reform profile and R5 is a loop, and a code such as B2 can name a variable (local reporting) or a loop (automatic benefits), so the text always says which." The renderer adds a type word only for identical codes: `return (kind === 'variable' && LOOPS[id]) || (kind === 'loop' && NODES[id]);`.
- **Fix:** Keep the IDs, since sources and backlinks cite them. Extend the renderer so every reference to a loop, reform, domain or issue carries its type word, as it already does for B2 to B5.
- **V6 works around it:** Yes. The guide's typed chips carry the type word every time (Mark 3).

## 13. The glossary's driver pills do not match the renderer

- **Where:** `glossary` term "Outside driver"; renderer pill code (`script.js` line 777) and `regionMap` (line 1284)
- **Evidence:** Glossary: "A force that affects the model but whose own causes lie outside its boundary, such as technology, population patterns, trade, foreign interference and major shocks. Drawn as a rounded pill outside the clusters." In the renderer the only rounded pill (rx 11) is the connection label, and X1 to X5 appear as a sixth area card titled "Outside drivers". The rendered map was not inspected beyond two screenshots.
- **Fix:** Change the glossary sentence to describe what the renderer draws, or draw drivers as pills.
- **V6 works around it:** Yes. The guide does not quote the sentence and sets its own driver mark in Phase 3.

## 14. Source count and register size differ without a label

- **Where:** `meta.counts.sources`; `meta.counts.sources_total_ids`; `sources`
- **Evidence:** `sources` 1099, `sources_total_ids` 1140. The register holds 1140 IDs, of which 41 carry `duplicate_of`; 1140 minus those is 1099, so `sources` appears to count unique sources. No field says so.
- **Fix:** Rename the first count `sources_unique` and say in the methods text what it counts.
- **V6 works around it:** Yes. The guide quotes 1,099 as unique sources and names the register size where it matters.

## 15. Issue count includes a retired record

- **Where:** `meta.counts.issues`; `meta.counts.issues_active`; methods and glossary text
- **Evidence:** `issues` 194, `issues_active` 193. The methods text and the glossary say 193.
- **Fix:** Rename the first count `issue_records` or show 193 everywhere with the retired record footnoted.
- **V6 works around it:** Yes. The guide says 193 active issue records.

## 16. Conceptual loop chains mix labels and IDs

- **Where:** `loops.B2.chain`; `loops.B3.chain`; `loops.R9.chain`
- **Evidence:** Closed loops list variable IDs in `chain`. The conceptual loops list B2: "A4 hardship", "Automatic support"; B3: "Excess profits", "Entry", "Competitive pressure"; R9: "Effective participation", "Accountable delivery", "E2". "A4 hardship" puts an ID inside a label.
- **Fix:** Keep `chain` for IDs only (null where a step has no variable) and put the words in `chain_labels`.
- **V6 works around it:** Yes. The guide draws conceptual loops from `chain_labels`.

## 17. Conceptual loops carry loop grades without numbered steps

- **Where:** `loops.B2.evidence`; `loops.B3.evidence`; `loops.R9.evidence`
- **Evidence:** B2: "well-supported"; B3: "well-supported where entry is possible"; R9: "hypothesis". The glossary says: "A complete path of connections that returns to the starting variable. If any closing step is only a hypothesis, the whole loop stays uncertain."
- **Fix:** Say what the grade covers when a loop has no complete numbered chain, for example the evidence for its mechanism.
- **V6 works around it:** Yes. The guide prints the closure status first and the grade text second, with the hollow line for conceptual steps.

## 18. Delivery log dates are free text in several formats, out of time order

- **Where:** `deliveryLog.rows[].date`
- **Evidence:** 7 formats across 24 rows: "9999-9999" 17, "9999-99-99 to 9999-99-99" 2, "9999-99-99 onward" 1, "9999-9999, published 9999" 1, "9999-99 to 9999-99" 1, "FY9999" 1, "9999 analysis" 1 (9 stands for a digit). Rows are not in time order of their start dates, for example DL07 (1935-2023) follows DL06 (1966-2012).
- **Fix:** Add `start`, `end`, `precision` and `kind` (span, open span, point) beside the display string.
- **V6 works around it:** Yes. The guide's period rule parses all 24 strings (Mark 5).

## 19. Mixed names a direction, a jurisdiction and a grade

- **Where:** `repairLog.rows[].direction`; `issues[].jurisdiction`; methods grade Mixed
- **Evidence:** Repair log rows with direction `mixed`: 3. Issues with jurisdiction `mixed`: 42.
- **Fix:** Rename the non-grade values, for example `both directions` and `several levels`, or document the three meanings.
- **V6 works around it:** Yes. The guide displays "Mixed direction" and "Several levels of government".

## 20. Log rows reference loops by text

- **Where:** `repairLog.rows[].loop`; `deliveryLog.rows[].loop`
- **Evidence:** All 64 repair rows and 14 delivery rows give a loop as "Loop R10: title". Every title matches V7 today; delivery rows add notes such as "(running in the improving direction)".
- **Fix:** Add `loop_id` and keep the text as a note.
- **V6 works around it:** Yes. The guide reads the ID from the text.

## 21. Some variables carry two domains in one string

- **Where:** `nodes[].domain`
- **Evidence:** A4 "D08/D09"; D4 "D04/D05"; D6 "D02/D05"; E1 "D03/D08"; X1 "D06/D07"; X2 "D10/D02"; X3 "D08/D06"; X5 "D05/D09"; D7 "D02/D05".
- **Fix:** Store a list, first domain first.
- **V6 works around it:** Yes. The guide splits on "/" and files a variable under its first domain, as Concept 11 does.

## 22. Effect codes and delay codes share the letters S, M and L

- **Where:** `reforms[].effects`; `links[].delay`
- **Evidence:** Delay codes: "The time between a change and its effect. Codes: S, under 2 years; M, 2 to 10 years; L, over 10 years." Effect codes: +L large positive, +M moderate positive, +S small positive, 0 no expected effect, -S small negative, -M moderate negative, ? direction uncertain.
- **Fix:** Document the overlap in the methods text, or spell delays out in every display.
- **V6 works around it:** Yes. The guide never prints a bare letter outside a data table (Mark 6).

## 23. Two words for areas

- **Where:** renderer `KIND_LABEL` (`script.js` line 159); `layers.*.regions`; `methods.boundary`
- **Evidence:** The renderer labels a domain "Issue area" and lists clusters under "Areas of this layer"; the methods text calls the clusters "clusters"; the data key for D01 to D10 is `domains`.
- **Fix:** One word per level: for example "domain" for D01 to D10 and "area" for A to E and X.
- **V6 works around it:** Yes. The guide uses Domain for D01 to D10 and area for A to E.

## 24. Documented and well supported draw the same line

- **Where:** renderer legend and `.edge` styles
- **Evidence:** Legend: "documented or well supported" share the solid line; dashes plausible 9 4, contested 9 3 2 3, hypothesis 2 4.
- **Fix:** If Dustin approves the record square at Gate 1, add it to documented connection labels.
- **V6 works around it:** Yes. The guide adds the square in its own figures.

## 25. Conceptual steps are close to the plausible dash

- **Where:** renderer `.edge.u-concept`
- **Evidence:** Conceptual steps use dash 5 4 in #8b9095; plausible uses 9 4. Both are dashed gray lines that differ in shade and dash length, which is a weak difference in grayscale and print.
- **Fix:** If approved at Gate 1, draw conceptual steps as a hollow line.
- **V6 works around it:** Yes. The guide draws the hollow line.

## 26. Authority links end in an arrowhead

- **Where:** renderer markers (`-t` teal arrowhead) and `.edge.authority`
- **Evidence:** Authority connections are drawn teal with a filled arrowhead and "auth" in the label. The arrowhead is the causal end mark.
- **Fix:** If approved at Gate 1, end authority lines in an open diamond with "no sign" in the label.
- **V6 works around it:** Yes. The guide draws the open diamond.

## 27. Interface palette and fonts

- **Where:** renderer styles
- **Evidence:** V7 uses its own palette (paper #F3F2EA, red #BD2C32, navy #223458, teal #3F6C64) and renamed URW Nimbus faces.
- **Fix:** Converge on Inter Tight, Inter and Pillar Red, as Dustin decided (DC-03).
- **V6 works around it:** Yes. Decided; listed so the atlas editor has it in one place.

## Checks that found no problem

- Loop type against signs: every loop with numbered steps has an even count of negative steps when reinforcing and an odd count when balancing (20 loops, all consistent).
- Loop delay: each loop's delay equals its slowest step (20 loops, all consistent).
- Loop chains and link lists agree in order, start variable and sign, and every connection that names a loop is listed by that loop.
- Authority: all 7 authority connections have no sign and sit in no loop.
- Connection ID prefixes match the glossary (L, LE, LT, LX, T).
- The loop titles quoted in the repair and delivery logs all match V7's loop records.

## Concept and guide files (not the model)

These belong to the supplied demonstrations, which V6 replaces. They need no V7.1 change. Full detail is in `work/handoffs/phase-0/20261020_Atlas-Reconciliation-Table.md`.

- **Concept 06 Ledger** counts the rejected reform R-35 in its D03 and D04 totals (10 and 14; V7 has 9 and 13 live reforms there). R-35 is V7's only rejected reform (R-35). Its link counts also use a different rule from Concept 11's (links that touch a domain against links filed under the variable they move), and neither page prints its rule.
- **Concept 08 Field Guide** says "20 loops close fully"; V7 counts 18 closed, 2 closed with a hypothesized step and 3 conceptual. Its specimens set a loop ID among ring variables ("D5 C3 C5 B4", where B4 is the loop).
- **Concept 09 Circuit** says the return line carries policy "back into the economy"; the three return connections run to area A, Economic structure.
- **Concept 04 Broadsheet** names Massachusetts Question 3 and omits Alaska Ballot Measure 2, which V7's R-01 text names.
- **Concept 05 Iceberg** renames V7's reform bands.
- **Concept 03 Field Manual** draws all 31 cross-layer connections dotted, the hypothesis texture, though none is a hypothesis.
- **Concepts 10 and 11** draw ordinal effects as widths or thirds, drop the 38 qualifiers, and Concept 10 draws gains only and two feasibility classes.
- **Concepts V2 boards** use about 45 board-only short names for variables, beside V7's own `chain_labels`.
- **V5 Polished and the Atlas Visual System** dash hypotheses (V7 dots them), draw plausible L02 and LE26 solid, show the placeholder "L##", draw associations as a dotted map line, and draw ownership as a frame.
- **Correction to the Phase 0 table, row 40.** Phase 0 listed the Atlas Visual System's "L54 is the weakest transfer to U.S. services" as a conflict. V7's own loop summary says "For U.S. services the weakest is L54, since its main study covers Brazilian mayors" (`loops.B4.evidence_summary`), so the figure is faithful. The grade of all three B4 steps is well supported.

## Change log

- Created: `work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md` (this file), by `work/build/scripts/phase-1/build_v71_issue_list.py`.
- Modified: none. V7 and every file in `source/` are unchanged.
