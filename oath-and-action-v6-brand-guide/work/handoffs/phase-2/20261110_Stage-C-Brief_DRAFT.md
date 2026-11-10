# Brief: stage board C, chapters 17, 18, 19 and 26 (draft for Dustin's go)

Oath & Action Edition 06, Phase 2, November 10, 2026. Written by the main session from the architecture map (sections 2 and 8), Master Brief sections 10, 17, 21 and 22, the token architecture, the stage B accessibility audit and the carried items in the twelfth handoff. This is a draft. Nothing here is built until Dustin gives his go and answers the four questions at the end. Where an answer would change the plan, the line says so.

## The goal

The four chapters of the Behavior and Production parts that Phase 2 owes, as finished guide pages in the same shell as chapters 01 to 12. A developer should be able to open chapter 18, take a component, set it with tokens from chapter 26, and ship it with every state, keyboard path and announcement right, with no other document. The bar is unchanged: the best brand guide any studio has shipped, calm and exact, with every rule earning its place.

| No. | Chapter | Anchor | Instruction line |
|---|---|---|---|
| 17 | Motion and states | `#motion-and-states` | Keep motion under the reader's control, and give every state visible text. |
| 18 | Components and interaction | `#components` | Build controls that work by keyboard and screen reader and announce every change. |
| 19 | Accessibility | `#accessibility` | Check a page against WCAG 2.2 AA before you call it finished. |
| 26 | Tokens and how to choose them | `#tokens` | Choose a token step by step from its surface, and call it by name. |

## What each chapter holds

- **17 Motion and states.** The nine motion tokens as they stand (120, 200 and 320 ms, a 40 ms stagger, the hinge at 680 ms and the lever at 560 ms, three easings). Fifth edition's three behaviors, slide, draw and land, each played on request with pause, reset and a still view. Reduced motion: every duration resolves to 0 ms and the final state shows at once. Nothing loops. The loading state with visible words and a still drawing in place of the old pulse (D2-200). Every state the brief names, each with words or a shape as well as color: muted, disabled, hover, focus, loading, selected, warning, error, empty and success. Chapter 17 owns how a state looks and moves; chapter 18 owns where each component uses it.
- **18 Components and interaction.** Buttons (primary, ask and quiet), links in text and to other sites (Rule 11.13), copy and download controls, disclosures, tabs, tables, the bill tracker as a component (its live updates through a polite live region, as Rule 11.5 promises), the symbol library's search and filters, the report reader, the loop stepper and other chart and diagram controls, forms with the approved error pattern (DR-199), the typed ID chip, and the masthead menu with its part navigation. Each component shows every state, its keyboard path, its accessible name, what a screen reader hears when it changes, its target size and its forced colors drawing.
- **19 Accessibility.** The WCAG 2.2 AA requirements, each tied to the guide rule that meets it. The verification matrix from Master Brief section 22, with the method for each check. The guide's own results so far, dated, with what was tested and what was not kept apart. The architecture map puts the full results at Phase 5, so chapter 19 says when the next run happens.
- **26 Tokens and how to choose them.** Token categories, names and tiers; the five conditions for adding a token; "How to choose a token" in five steps (surface, role, emphasis, state, then any component token, which wins), with the token architecture's four worked examples at actual size beside their failures. A table of all 496 tokens generated from `tokens.json`, with values, descriptions and contrast on each surface, searchable and with a copy button on each name. The version rule and the two downloads, `tokens.css` and `tokens.json`.

## Carried items folded into this stage

- **The shell's last pass.** Chapter 08's open items: the feed test on dark cards, a print L3 and the 5 red pixels at 360 px (D2-715). An opener figure for chapters 09 and 10 (D2-965). The sideways scroll at 200 percent text on phones, with the causes in the engineer's round 3 notes (D2-1103).
- **Drawings for approval by name.** The 16 px Pause and Filter redraws (DR-197), the Housing topic drawing (DR-196) and, if question 3 says so, the 24 px pixel fits for the 37 drawings (DR-198).
- **Rule 12.4's hinge arcs.** The creative director judges keep or retire on the built page; the call goes to Dustin on board C as a decision card (D2-1114).
- **Missouri.** The state certifies after counties file on November 17. The research lead reads the certified count when the Gate 2 preview is built; until then the plate keeps its "unofficial" wording (D2-838).

## Who makes what

| Maker | Role file (`.claude/agents/`) | Owns |
|---|---|---|
| Accessibility lead | `oa-ux-accessibility-lead.md` | An inventory of every interactive part and every state in chapters 01 to 12, the shell and Atlas V7, which sets chapter 18's list; chapter 19; a check of every chapter 18 component |
| Systems designer | `oa-design-director.md` | Chapter 17; chapter 18's anatomy plates, with the accessibility lead |
| Identity designer | `oa-design-director.md` | Chapter 08's open items; the opener figure for chapter 09; the hinge motion and the lever landing in chapter 17, since both move identity marks; a replacement for Rule 12.4's arcs if they retire |
| Icon designer | `oa-design-director.md` | The drawings, by one hand, as new files in new folders; Civic Line masters are read, never edited |
| Engineer | `oa-engineer.md` | Chapter 26 with its generated table; the code each chapter 18 component ships (question 1); the shell pass; new build checks for keyboard paths, reduced motion on every moving specimen and the token table's parity |
| Editor | `oa-editor.md` | Every word, written alongside each maker, then the copy edit |
| Research lead | `oa-research-lead.md` | WCAG 2.2 criteria in W3C's own words; the WAI-ARIA Authoring Practices pattern for each component; browser support facts the rules depend on; Missouri |
| Creative director | `oa-creative-director.md` | Scores the drawings before the drawings board, judges Rule 12.4's arcs, then scores the chapters on the brief's six criteria |

## Order of work

1. **Round 0, in parallel.** The research lead, the accessibility lead's inventory, the engineer's shell pass and checks, and the icon designer's drawings.
2. **Drawings board C, early.** Each drawing beside its master or the approved file at true size, scored by the creative director, published while the chapters are being written. Approved drawings are promoted before round 2, so the reviewers see the page as it will ship.
3. **Round 1, chapters.** 26 and 17 first, since 18 cites both. Then 18. Then 19, which cites every chapter. The editor writes alongside each maker.
4. **Round 2, review.** Three red teams on one frozen copy, as DR-190 set them, with the creative director reading at the same time. The production test asks a simulated developer to build a component the guide does not show, from chapters 18 and 26 alone. Then one fix pass, DR-191's short second pass for craft or wording, the editor's read and the creative director's rescore.
5. **Board C.** The chapters page republished as version 6 with chapters 17, 18, 19 and 26, and a short decisions board with Rule 12.4's arcs and any call that needs Dustin.
6. **Then Gate 2.** The preview build of chapters 01 to 12, 17, 18, 19 and 26 as one file, and the Gate 2 report with the Phase 3 proposal.

## Rules that bind every page

Everything in `20261109_Stage-B-Brief.md` under "Rules that bind every page", plus the answers since: the error mark in the text's ink with a 4 px Pillar Red bar (DR-199), Rule 10.5's tile exception (DR-200), and no reader tests (DR-202). Motion specimens play only on request, pause and reset, and show their final frame under reduced motion (Master Brief section 17).

## Risks the plan answers

- **One component, two homes.** Chapter 11 already runs the loop stepper, the report reader, the library and the error form live. Chapter 18 owns the component and its specification; chapter 11 keeps its plate and links to 18, so no second live copy adds weight or drifts.
- **Page weight.** The page is 6.71 MB. The engineer sets a weight budget for the four chapters before round 1.
- **What this container cannot test.** Real screen readers, real phones and Windows contrast themes. Chapter 19 and the Gate 2 report list them as not tested, with a short script anyone can run after launch.

## Questions for Dustin

1. **Code to copy in chapters 18 and 26.** Should each component ship as code a builder can copy: plain HTML and CSS that read only `tokens.css`, with a short script where a component needs one? *Recommendation:* yes. It works in the atlas's single file, on a static site and with AI coding tools, and the production test can build from it. The other choice is specifications and anatomy only.
2. **Dark mode for screen products.** Night Edition is already the atlas's dark mode (DR-36), and the tokens hold every role on Charcoal. *Recommendation:* one dark mode for every screen product, drawn from Night Edition on Charcoal, which follows the reader's device setting and has a visible switch that remembers a reader's choice. Chapter 18 then shows each component on Newsprint and on Charcoal, and the guide itself stays on Newsprint. The other choice is a dark mode in the atlas alone, by switch.
3. **The 24 px pixel fits for the 37 drawings.** *Recommendation:* draw them now, on the early drawings board with Housing and the 16 px Pause and Filter, so the Gate 2 preview meets the brief's line that icons sit on the pixel grid at 24 px. The other choice is Phase 3 (DR-198 allows either).
4. **The two unsent reader check pages.** *Recommendation:* delete both published pages now; their files stay in the repository as the record (D2-1113). Each delete needs your yes.
