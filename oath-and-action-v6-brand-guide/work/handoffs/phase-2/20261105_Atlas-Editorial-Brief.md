# Editorial atlas systems: the brief

Oath & Action Brand Guide, Edition 06. Phase 2, November 5, 2026. Every maker and reviewer on this round reads this file first. It replaces the October 30 concepts brief for this round; that brief's section 4 (brand rules and Rule 05.3) still binds.

## 1. What Dustin asked for, in his words

- "I like the editorial desk, the direction we're going. My issue is like the main system overview and the loops... not exactly educational or clear."
- "When we show the whole system overview and we talk about economic structure, electoral systems, ... some of the attached images that I like include kind of all the subcomponents. Descriptions of those things."
- "When people look at the overview of the system, I want it to be clear, like what each component is, what the big relationships are, kind of how it all works together in that beautiful editorial desk style."
- "In some cases, they're too complex. There's like too many lines and stuff. So ideally, it starts at kind of like a high level, and you could click in and get more detail."
- "I want it in that editorial desk feel, like New York Times, Economist."
- "I want this to be a full and complete systems map with full and complete explanations of the problems or issues and then the solutions."
- "Think about this as a civic educator, a user experience and user interface expert."
- "This should look like it should be exceptional. It should look like a final product from a globally renowned branding and design firm, best in class."
- He will pick one system this round, then it gets finalized for the brand guide and for his future systems maps.

## 2. Rules for every system

1. **Plain names lead** (DR-32, DR-35), with the formal title beneath: Wealth (Economic structure), Voice (Political inputs), Elections (Electoral competition), Checks (Governing institutions), Policy (Legitimacy), Your household (How the economy reaches a household), Technology (Technology and its effects), Outside forces (Outside drivers). Each core part also carries its question: "Who holds the cards?", "Who pays for influence?", "Who picks them?", "Who checks their work?", "Whose side are the rules on?", "Who lives with the results?", "Who controls the machines?".
2. **The overview is complete and calm** (DR-29). Every one of the eight parts appears. Every one of the 51 variables is named on the overview or one tap away inside its part, with its short label; each part says in one or two plain sentences what it is. Only the big relationships are drawn: flows between parts, with their counts, and the main circuit. No individual connection lines on the overview. Detail sits one click down.
3. **Loops teach** (DR-30). Every loop is a named box-and-arrow cycle: boxes carry the variables' short labels, each arrow carries "raises" or "lowers" beside its sign, its evidence texture and its delay, the weakest step is marked, and the cycle reads aloud. No dot-plan route thumbnails.
4. **Problems and solutions in full** (DR-33). Area pages list the issues tracked there with their real-world examples, and the reforms aimed there with what each changes.
5. **Start from a question.** Each overview offers a way in through the reader's own life: the five hubs and 16 everyday questions in V7.
6. **Editorial craft.** Finding sentences as headlines, notes set inside drawings on fine leaders, gray context with one dark route, generous white space, confident type, nothing decorative. The Times and The Economist are the bar for clarity and finish; no mark, typeface, color or layout of theirs is copied (D2-65).
7. **Brand.** Locked palette and type (Inter Tight, Inter, Lora Italic for quoted words only), the approved wordmark masters, Civic Line icons exactly as drawn (D2-52), Rule 05.3 (one working red per view; where a reform acts on the reform and loop pages; red never on Prussian). The approved frame from October 30 still binds: the design frame memo's type scale and stroke family, the interaction memo's views with a panel, the civic education memo's wording rules ("raises" and "lowers" beside every sign; the read-aloud line built from the signs; "a plus sign means the two move the same way, not that the change is good").
8. **Honesty.** Every label, count, sign, grade, issue, example and reform text comes from the data by script. Headlines are studio drafts, marked so in the notes. Sketched loops (B2, B3, R9) and hypothesized steps (R2, R16) are disclosed. Reform effects are never summed. R-01 carries the editor's disclosure about the Yes on 3 campaign, in the dataset's `reforms['R-01']['disclosure']` (V7's own wording, which V7 prints on the profile); it must appear in full on the R-01 page.

## 3. The pages every system builds

All six views in one self-contained HTML page with hash views. Same subjects in every system so Dustin compares like with like.

| View | Hash | What it holds |
|---|---|---|
| Overview | `#overview` | Headline and deck; the whole system (rules 2 and 5); a short how-to-read line; a way to every part, loop and question |
| Elections | `#area-c` | What Elections is and its question; its five variables with their descriptions and "a higher value means"; what pushes on it and what it pushes on, grouped by part and named; the seven loops that run through it as small named cycles (R4a, R4b, R10, R11, R12, R16, B4); the issues tracked there (39 active records touch C1 to C5) with their real-world examples, shown so a reader can scan them and open any one; the reforms aimed there |
| Loop R10 | `#loop-r10` | The safe-seat loop at full size, step by step, with the read-aloud line, evidence, delays, the weakest step L53, the qualification, and R-01 marked where it acts |
| Reform R-01 | `#reform-r01` | The problem it answers, what it changes, where it acts (on the loop drawing), effects by family in words, routes with feasibility and check dates, problem and remedy evidence, tradeoffs, failure risks, status with the full disclosure |
| Loop catalog | `#loops` | All 23 loops as small named cycles, grouped by home part, each with its plain name, V7 title, kind, stations, weakest step and how many reforms aim at it |
| How to read | `#how-to-read` | The shared language, after Dustin's Concept 00: the tip is the effect, texture is the evidence, ticks count the wait, loops have a character, color is the layer |

Phone (390 px): every view works without sideways scroll. The overview becomes a readable stack, never a shrunken diagram.

## 4. The five systems

Each system is one maker's. References live in `work/research/chat-references/` (paths below). Five of Dustin's November 5 images were never saved to disk; they are described here.

### System 1. Times Explainer (White)
An explainer that reads like the best newspaper graphics: the system told as a story in order, with annotated drawings that do the teaching. The overview leads with "How the circuit runs", Dustin's newest atlas home (not on disk: a vertical list from Your household through Wealth, Voice, Elections, Checks and Policy to "The fix", each with its question and a sentence), then a calm annotated diagram of the eight parts with the main flows and counts, then "Start from your own bill". References: `atlas-editorial/20261105_Ref-Editorial-Desk-*` (what to improve), concept 12 Editorial Desk itself (`work/boards/phase-2/atlas-concepts/12-editorial-desk/`), `atlas-editorial/20261105_Ref-Atlas-Concept-03-R8-Diagram-Preview.webp` (restraint, boxes with code and plain label, arrow annotations), the research brief's direction A (`work/research/20261030_Data-Viz-System-References.md`, sections 4 to 6).

### System 2. Economist Register (Newsprint)
Dense, exact and scannable: the system as a register a reader reads across. The overview is a register of the eight parts, one row each: plain name and question, every variable named, counts of connections, loops and reforms, the evidence mix as a small bar, the main loop; opening a row unfolds its chain and the reform aimed at it. A compact diagram of the flows between parts sits above the register. References: Dustin's Concept 11 (not on disk: "The whole system on one register.", ten domains as rows with variables as chips, counts, evidence bars, main loop, and an open row showing R10 as a chain with R-01's effects on Prussian), Concept 00 "The Shared Language" (not on disk: "Every line says what happens next, and how sure we are."), the research brief's direction C and The Economist notes.

### System 3. Reference Sheets (Newsprint)
A field guide of numbered sheets, like a design system's own documentation: precise, technical, typographic. The overview is a simplified circuit after Dustin's Concept 09: five cards left to right with every variable listed and one "passes on to" line, the household and technology channel beneath, outside forces above, and only bundled flows with counts. References: `atlas-concepts/20261030_Ref-Atlas-Concept-09-The-Circuit.png`, `atlas-editorial/20261105_Ref-Atlas-Visual-System-Arrow-Conventions.webp` (arrow conventions, R1 sheet with accent rules on boxes, R16's untested step, R-28 attached to its target), `atlas-concepts/20261030_Ref-Atlas-Concept-07-Loop-Card-R10.png`, `atlas-editorial/20261105_Ref-Atlas-V8-Loop-Explorer-R1.webp` and `-Variable-Neighborhood-A3.png` (ChatGPT mockups Dustin likes; study their structure).

### System 4. Night Edition (Charcoal)
The dark atlas Dustin built, refined to a finished product: a dark editorial site that is calm, legible and luminous. The overview keeps the dark atlas's best ideas: area cards that list every part, main flows bundled with counts, "Start from a question", the loops as cards. It has far fewer lines and far more polish. References (not on disk unless named): the dark atlas home "Who do they answer to? Who does our country work for?" (whole system on one page, cards A to E with every variable listed, outside drivers strip, household and technology cards, bundled flows with counts, a "Main flows / Every connection" switch, question cards, loop cards with station lists, ten topics); the dark "Outside drivers" page (driver cards with description, "a higher value means" and issues, wired to a "pushes on" list grouped by part; loops, reforms and issues tracked here); `atlas-editorial/20261105_Ref-Atlas-Feedback-Loops-Dark-Grid.webp` (loop cards as icon box-and-arrow cycles). The dark atlas file itself: `work/extract/supplied-20261105/20261019_Oath-And-Action-Atlas-Interactive-Concept_V2.html` (open it in Chromium and study it; never copy its code).

### System 5. Architecture (White)
The system as a building: layers stacked from the economy up to public outcomes, each part shown as Civic Line icon tiles with names, labeled flows between layers (what each layer passes up), the outside forces standing beside, the policy-effects return line, and a selected-item panel that explains whatever the reader touches. Start from a question with document-style cards. References: `atlas-concepts/20261030_Ref-Atlas-Civic-Architecture-Layers.webp` ("The architecture of accountability"), `atlas-concepts/20261030_Ref-Atlas-Decision-Grid.webp` (named components in area panels, labeled flows "Resources", "Influence", "Electoral pressure", "Performance", "Policy effects", a mechanism detail panel), `atlas-editorial/20261105_Ref-Atlas-Follow-A-Question-Preview.webp` (question cards and topic tiles). These are generated mockups: keep their structure, replace their invented items with V7's real parts, and fix their faults (too much red, link glyphs on every label, dashed boxes).

## 5. Data and tools

- **Data:** `work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json`, built by `work/build/scripts/phase-2/atlas_editorial_data.py`: V7 with the dark atlas's plain layer. Keys: `parts` (eight, with plain name, question, formal title, chapter, story, nodes), `nodes` (label, title, description, increase_means, why), `links` (name, plain, sign, type, delay, evidence, mechanism, qualification), `loops` (plain_name, title, summary, steps, stations, weakest, reforms, qualification, delay_word), `reforms` (full profile with status, effects, routes), `issues` (summary, mechanism, grade, response, actor, tradeoff, success_measure, problem_example, fix_example), `domains`, `hubs`, `pathways`, `glossary`, `mixups`, `numbers`, `families`, `effect_codes`, `route_names`, `feasibility_scale`, `sources`.
- **Shared code and assets:** `work/build/scripts/phase-2/atlas_concepts_common.py` (palette, grades, `icon_svg()`), `work/boards/phase-2/atlas-concepts/shared/atlas-kit.js` and `atlas-kit.css` (behavior; restyle freely), the variable-to-icon map, the wordmark masters in `work/build/assets/identity/`.
- **Contract:** `<meta name="atlas-views" content="overview area-c loop-r10 reform-r01 loops how-to-read">`; `data-view-root` on each view; `data-part` (A to E, X, EC, TC) with `data-name` (plain name, formal title or chapter); `data-node` + `data-name`; `data-link` + `data-sign`, `data-grade`, `data-delay`; `data-loop` + `data-steps` (`sketch` for B2, B3, R9) + optional `data-name` (V7 title or plain name); `data-reform` + `data-targets`; `data-issue` + `data-name` (the issue title); `data-count` on printed counts; `data-strip="loops"` around the catalog; `data-red` and `data-red-job` on every Pillar Red mark; every drawing an `<svg data-view>`; Google Fonts only.
- **Checks, both must pass:** `python3 -I work/build/scripts/phase-2/atlas_concepts_verify.py <page>` and `node work/build/scripts/phase-2/atlas_concepts_check.js <page>`.

## 6. Process

1. Five makers build in parallel, one system each.
2. Red team, after all five are built: a civic educator, an interface and accessibility lead, and an evidence and brand auditor each review all five; a panel of first-time readers sees only screenshots and answers comprehension questions. Their findings go back to each maker as one ranked list.
3. Each maker makes one fix pass and reruns the checks.
4. The creative director scores all five on the seven-line rubric and recommends one.
5. Board 2 shows the five side by side for Dustin's pick.

## 7. Files

- Folder per system: `work/boards/phase-2/atlas-editorial/NN-slug/` holding `20261105_Editorial-NN-Title.html`, `build_system.py`, captures and check results.
- Notes: `work/handoffs/phase-2/20261105_Editorial-NN-Notes.md`.
- Slugs: `01-times-explainer`, `02-economist-register`, `03-reference-sheets`, `04-night-edition`, `05-architecture`.
