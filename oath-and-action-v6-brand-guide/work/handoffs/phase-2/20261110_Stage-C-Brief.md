# Brief: stage board C, chapters 17, 18, 19 and 26

Oath & Action Edition 06, Phase 2, November 10, 2026. Written by the main session for the makers, the engineer, the accessibility lead, the research lead and the creative director. Built from the draft, `20261110_Stage-C-Brief_DRAFT.md`, which stays as the record. Dustin approved the plan and all four recommendations on November 10 ("yes to all recs"; DR-203 to DR-206). The studio's calls for this stage start at D2-1129.

## The goal

The four chapters of the Behavior and Production parts that Phase 2 owes, as finished guide pages in the same shell as chapters 01 to 12. A developer should be able to open chapter 18, copy a component, set it with tokens from chapter 26, and ship it with every state, keyboard path and announcement right, with no other document. The bar is unchanged: the best brand guide any studio has shipped, calm and exact, with every rule earning its place.

| No. | Chapter | Part | Anchor | Instruction line |
|---|---|---|---|---|
| 17 | Motion and states | Behavior | `#motion-and-states` | Keep motion under the reader's control, and give every state visible text. |
| 18 | Components and interaction | Behavior | `#components` | Build controls that work by keyboard and screen reader and announce every change. |
| 19 | Accessibility | Behavior | `#accessibility` | Check a page against WCAG 2.2 AA before you call it finished. |
| 26 | Tokens and how to choose them | Production | `#tokens` | Choose a token step by step from its surface, and call it by name. |

## What Dustin has decided for this stage

- **Code to copy (DR-203).** Every chapter 18 component ships as code a builder can copy: plain HTML and CSS that read only `tokens.css`, with a short script only where the component needs one. No framework. Chapter 26's examples do the same. The production test builds from this code.
- **Dark mode (DR-204).** One dark mode for every screen product (the website, the atlas and any other screen product), drawn from Night Edition on Charcoal (DR-36). It follows the reader's device setting and has a visible switch that remembers the reader's choice. Chapter 18 shows each component on Newsprint and on Charcoal. The guide itself stays on Newsprint whatever the device asks.
- **Drawings now (DR-205).** The 24 px pixel fits for the 37 topic and atlas drawings are drawn in this stage, on an early drawings board with the Housing topic drawing (DR-196) and the 16 px Pause and Filter redraws (DR-197), each for approval by name.
- **Reader check pages (DR-206).** Both unsent pages are deleted; their files stay in the repository as the record.
- **Settled and unchanged.** The Civic Line drawings as approved (DR-144, DR-156 to DR-182), the atlas visual system (System 1, DR-36), the chart system (DR-52 to DR-61), chapter 14's plan (DR-62, DR-63), DR-64's chart rules, chapter 02's writing rules (DR-73 to DR-83) and every answer from DR-95 to DR-206. No reader tests (DR-202).

## What each chapter holds

- **17 Motion and states.** The nine motion tokens as they stand (120, 200 and 320 ms, a 40 ms stagger, the hinge at 680 ms and the lever at 560 ms, the standard, enter and exit easings). The fifth edition's three behaviors, slide, draw and land, each played on request with pause, reset and a still view. Reduced motion: every duration resolves to 0 ms and the final state shows at once. Nothing loops. The loading state with visible words and a still drawing in place of the old pulse (D2-200). Every state Master Brief section 10 names, each with words or a shape as well as color: muted, disabled, hover, focus, loading, selected, warning, error, empty and success, on Newsprint and on Charcoal. Chapter 17 owns how a state looks and moves; chapter 18 owns where each component uses it.
- **18 Components and interaction.** The list comes from the accessibility lead's inventory (round 0). At least: buttons (primary, ask and quiet), links in text and to other sites (Rule 11.13), copy and download controls, disclosures, tabs, tables, the bill tracker as a component (Rule 11.5's polite live region), the symbol library's search and filters, the report reader, the loop stepper and other chart and diagram controls, forms with the approved error pattern (DR-199), the typed ID chip, the masthead menu with its part navigation, and the dark mode switch (DR-204). Each component shows every state, its keyboard path, its accessible name, what a screen reader hears when it changes, its target size, its forced colors drawing, and its code to copy.
- **19 Accessibility.** The WCAG 2.2 AA success criteria, each in W3C's words and tied to the guide rule that meets it. The verification matrix from Master Brief section 22, with the method for each check. The guide's own results so far, dated, with what was tested and what was not kept apart, and a short script anyone can run after launch for what this container cannot test (real screen readers, real phones, Windows contrast themes). Full results come at Phase 5, as the architecture map sets.
- **26 Tokens and how to choose them.** Token categories, names and tiers; the five conditions for adding a token; "How to choose a token" in five steps (surface, role, emphasis, state, then any component token, which wins), with the token architecture's four worked examples (section 8) at actual size beside their failures; how a token resolves in dark mode. A table of every token generated from `tokens.json`, with value, description and contrast on each surface it serves, searchable, with a copy button on each name. The version rule and the downloads.

## Who makes what

Each agent is a general-purpose agent told to read its role file in `.claude/agents/` first.

| Maker | Role file | Owns |
|---|---|---|
| Research lead | `oa-research-lead.md` | WCAG 2.2 AA criteria in W3C's own words; the WAI-ARIA Authoring Practices pattern for each component; browser support for every platform feature the rules depend on; Missouri's certified count at the Gate 2 preview |
| Accessibility lead | `oa-ux-accessibility-lead.md` | The inventory of every interactive part and state (round 0), which sets chapter 18's list; chapter 19; a check of every chapter 18 component |
| Icon designer | `oa-design-director.md` | The drawings, by one hand, as new files in new folders. Civic Line masters, the approved utility files and the approved pillar fits are read, never edited |
| Identity designer | `oa-design-director.md` | Chapter 08's open items (D2-715); chapter 09's opener figure; in round 1, the hinge motion and the lever landing in chapter 17, and a replacement for Rule 12.4's arcs if they retire |
| Systems designer | `oa-design-director.md`, checked against `oa-ux-accessibility-lead.md` | Round 1: chapter 17, chapter 18's anatomy plates with the accessibility lead, and chapter 10's opener figure |
| Engineer | `oa-engineer.md` | The shell pass; dark mode in the tokens; the code block and copy control; chapter 26 with its generated token table; the code each chapter 18 component ships; the new build checks |
| Editor | `oa-editor.md` | Round 1: every word, written alongside each maker, then the copy edit |
| Board builder | `oa-engineer.md` | Drawings board C |
| Creative director | `oa-creative-director.md` | Scores the drawings before the drawings board, judges Rule 12.4's arcs, then scores the chapters on the brief's six criteria |

## Order of work

1. **Round 0, in parallel.** The research lead, the accessibility lead's inventory, the engineer's shell pass and token work, the icon designer's drawings and the identity designer's chapter 08 items and chapter 09 opener.
2. **Drawings board C.** The creative director scores the drawings; a board builder makes the board from the icon designer's files; the main session checks and publishes it. Dustin approves by name while round 1 runs. Approved drawings are promoted before round 2.
3. **Round 1, chapters.** 26 and 17 first, since 18 cites both. Then 18. Then 19, which cites every chapter. The editor writes alongside each maker.
4. **Round 2, review.** Three red teams on one frozen copy as DR-190 set them, with the creative director reading at the same time. The production test asks a simulated developer to build a component the guide does not show, from chapters 18 and 26 alone, and to switch it to dark mode. One fix pass, DR-191's short second pass, the editor's read and the creative director's rescore.
5. **Board C.** The chapters page republished as version 6 with chapters 17, 18, 19 and 26, and a short decisions board with Rule 12.4's arcs and any call that needs Dustin.
6. **Gate 2.** The preview build of chapters 01 to 12, 17, 18, 19 and 26 as one file, and the Gate 2 report with the Phase 3 proposal.

## Round 0 tasks

### Research lead
Write `work/handoffs/phase-2/20261110_Stage-C-Research-Notes.md`, early, adding as you go.
1. Every WCAG 2.2 success criterion at levels A and AA, read on w3.org (the quick reference and the "Understanding" pages answer from this container): number, name, level and the criterion's own words, with each URL and the date read. Mark the criteria new in 2.2 and 4.1.1 Parsing's status in 2.2.
2. For each component on the draft list in "What each chapter holds", the matching WAI-ARIA Authoring Practices pattern (w3.org/WAI/ARIA/apg): its name, URL, keyboard interactions and the roles, states and properties it names. Say where no pattern fits.
3. Browser support, from MDN or the specifications, for: `prefers-reduced-motion`, `prefers-color-scheme`, the `color-scheme` property, `forced-colors` and `CanvasText` with the other system colors, `:focus-visible`, container queries, `text-wrap: balance` and `pretty`, the `inert` attribute, the `<dialog>` element, the Popover API, `aria-live` regions, and the Clipboard API's `writeText`. Give the first stable version in Chrome, Edge, Firefox and Safari (desktop and iOS) and the date checked.
4. How a page stores a reader's theme choice without a server (localStorage and its limits in private browsing), and how sites avoid a flash of the wrong theme on load, from MDN or a W3C or WHATWG source.

### Accessibility lead
Write `work/handoffs/phase-2/20261110_Stage-C-Interaction-Inventory.md`.
1. Every interactive part in the built chapters page (`work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`: read it with scripts, never whole), the shell (`work/build/guide/shell/`), the live specimens (`work/build/guide/specimens/s-11-*.html` and any other specimen with a script or a control) and Atlas V7 as its documents describe it (`work/research/atlas-v7-docs/`, the Phase 0 audit `work/handoffs/phase-0/20261020_UX-Accessibility-Audit.md` and `work/handoffs/phase-0/ux-data/`). For each: what it does, where it lives, its states, its keyboard path, its accessible name, what it announces, its target size, how it draws in forced colors, and any fault you find.
2. From that, chapter 18's component list: each component, its APG pattern if one fits, the states it must show (the ten states of Master Brief section 10, as they apply), and which chapter 11 or shell specimen it replaces as the canonical example. Mark which components need a script.
3. A states matrix: component by state, with what the state looks like now (token, shape or words), on Newsprint and on Charcoal, and any gap.
4. A first map for chapter 19: each WCAG 2.2 A and AA criterion against the guide rule that meets it, or "gap". Use the criterion numbers and names; the research lead supplies W3C's words for the chapter.

### Engineer
Write `work/handoffs/phase-2/20261110_Stage-C-Engineer-Round-0-Notes.md`.
1. **The 200 percent phone scroll (D2-1103).** Apply the recommendation in `20261110_Stage-B-Round-3-Engineer-Fix-Notes.md`, "Finding: text at 200 percent on a phone", then extend the guide check's 200 percent sideways test to 390 and 360 px.
2. **Opener figures (D2-965).** The shell renders an optional figure under a chapter's intro when the chapter's JSON names it as `"opener": "<specimen id>"`. The specimen sits in its owner's manifest like any other and fits the chapter column at true size. The identity designer supplies chapter 09's; the systems designer supplies chapter 10's in round 1. Chapters 01 to 08 stay with words alone.
3. **Dark mode in the tokens (DR-204).** A theme in `tokens.css` that maps every semantic role to its on-Charcoal value under `@media (prefers-color-scheme: dark)`, and an attribute on the root (name it) that forces light or dark and wins over the device setting. No new primitive. Chart tokens already exist on Charcoal (D2-136). Every role in the dark theme passes the contrast its kind needs, and the token tests prove it. The guide's own page forces light, so a device's dark setting changes nothing on the guide. Token version 6.0.0-gate2.7 with a change note.
4. **The code block and copy control (DR-203).** A shell component that shows a component's code, HTML and CSS in separate panels, with a copy button for each, in the guide's type and tokens, keyboard and screen reader ready, under 13 px never. Set the contract a chapter uses to attach code to a rule, and how the build checks that the copied code renders the same as the specimen.
5. **Chapter 26's token table.** A generator that reads `tokens.json` and writes the table (name, CSS name, value, description, tier, surfaces with measured contrast), with search and a copy button per name. It can land as a specimen now; the chapter's words come in round 1.
6. **The weight budget and new checks.** A weight budget for chapters 17, 18, 19 and 26 within 16 MB; the plan for the build checks round 1 needs (each component's keyboard path, reduced motion on every moving specimen, the token table's parity with `tokens.json`).
Do not create chapters 17, 18, 19 or 26 yet; their makers do in round 1.

### Icon designer
Write `work/handoffs/phase-2/20261110_Stage-C-Drawings-Notes.md` and new files only.
1. **The 24 px pixel fits for the 37 (DR-198, DR-205).** The 37 topic and atlas drawings in `20261110_Stage-B-Ch10-Construction.md`, section 10 (the 41 less the four pillar icons, which have their fits). Draw each at 24 px on whole pixels from its master in `work/build/assets/civic-line-v6/black/`, keeping every feature that makes it read, as the pillar fits did (`work/build/assets/pillar-icons/`, `work/build/scripts/phase-2/civic_line_stage_b_pillar_fit.py`, `20261109_Stage-B-Civic-Line-Icons-Notes.md`). One color, since Rule 10.4 sets 24 px in one color. The switch is the pillar icons' own: the fit on 1x screens, the master from 2x. Measure each fit and its master at 1x: the share of line pixels that reach full ink (the creative director found 2 of 18 masters do). Run the pixel fit check (`icon_pixel_fit_check.py` or `.js`) and the likeness check (`icon_likeness_check.js`), and make sure the five look-alikes (CL-023, CL-028, R-08, R-27, R-45; D2-971) grow no closer. Folder: `work/build/assets/civic-line-24-fit/`.
2. **The 16 px Pause and Filter (DR-197).** From the approved files in `work/build/assets/utility/svg-16/`: Pause's bars widen from 4 to 5 px (x 2 to 7 and 9 to 14), Filter's spout from 4 to 5 px, so each opening keeps one whole open pixel on 1x screens. Everything else stays. Folder: `work/build/assets/utility-16-redraw/`.
3. **Housing (DR-196).** A topic drawing in Civic Line's construction, drawn the way Testify and Contact an Official were (`work/build/scripts/phase-2/civic_line_stage_b_new_topics.py`, `work/build/assets/civic-line-new-topics/`), with its red edition, its tiles and its likeness against the whole set. Say whether it reads at 24 px. Add its files to `civic-line-new-topics/` as new dated files.
4. Previews at 1x and 2x for the board: each fit beside its master at 24 px, each redraw beside the approved file at 16 px, Housing beside its nearest topic drawings at 128, 48 and 24 px, on Newsprint and Charcoal.

### Identity designer
Write `work/handoffs/phase-2/20261110_Stage-C-Identity-Round-0-Notes.md`.
1. **Chapter 08's open items (D2-715).** The feed test on dark cards (CD-N12, `20261108_CD-Review-Of-Q1-To-Q4-Pass.md`); a print L3 (D2-482); the 5 red pixels the lever keeps at 360 px against a floor of 4 (same review, "The feed margin"). Fix what the drawing can fix inside the approved geometry; any change to identity geometry is a named approval for board C, shown side by side at actual size, not a change you make.
2. **Chapter 09's opener figure (D2-965).** The pillar row under the intro, from chapter 09's own specimens, as `s-09-opener`, wired with the engineer's `"opener"` key.
Change words and plates only through your generators (`promotion_identity.py`, `stage_b_identity_ch01.py` and the chapter 08 and 09 scripts), never in their outputs.

## Rules that bind every page

Everything in `20261109_Stage-B-Brief.md` under "Rules that bind every page", plus: the error mark in the text's ink with a 4 px Pillar Red bar (DR-199); Rule 10.5's tile exception (DR-200); motion specimens that play only on request, pause and reset, and show their final frame under reduced motion (Master Brief section 17); every component specimen on Newsprint and on Charcoal (DR-204); code to copy that reads only `tokens.css` (DR-203).

## Risks the plan answers

- **One component, two homes.** Chapter 11 runs the loop stepper, the report reader, the library and the error form live. Chapter 18 owns the component and its specification; chapter 11 keeps its plate and links to 18, so no second live copy adds weight or drifts.
- **A guide that flips dark.** The guide forces light (DR-204), and the guide check tests it with the device set to dark.
- **Page weight.** The page is 6.71 MB. The engineer sets a budget for the four chapters before round 1.
- **What this container cannot test.** Real screen readers, real phones and Windows contrast themes. Chapter 19 and the Gate 2 report list them as not tested.
- **Fresh containers and shared files.** The twelfth handoff's setup steps; the generator chain after any owner's change; each owner writes only its own files.

## Notes and limits for every agent

Each agent writes its notes with: what it built; routine calls as "D2-xxx | decision | reason" lines; questions for Dustin with a recommendation; Tested and Not tested, kept apart; a change log. Write notes early and add as you go. Use the scratchpad `/tmp/claude-0/-home-user-Dustin-s-Command-Center/67af6aec-b8e0-5b79-b000-c172e734e753/scratchpad/stage-c/<your role>/` for anything temporary, never `/tmp` itself. Run Python with `-I`. Follow `CLAUDE.md` and chapter 02's writing rules in every word: plain prose, no em dashes.

Never touch `source/`, `work/ledger/`, the Civic Line masters, the identity masters (new files beside them only), any existing board, or another owner's files. Do not commit or push. Reply to the main session in 200 words or fewer.
