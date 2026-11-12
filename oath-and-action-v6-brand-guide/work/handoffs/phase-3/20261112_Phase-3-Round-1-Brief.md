# Brief: Phase 3, round 1, comparison, shift and swing, change over time, tables and plain words

Oath & Action Edition 06, Phase 3, November 12, 2026. Written by the main session for round 1's makers. Gate 2 approved the Phase 3 proposal (G2-01). Dustin approved board 1 (DR-236 to DR-239) and this round's plan (DR-240, DR-241). The studio's calls continue from D3-220. Paths are relative to `oath-and-action-v6-brand-guide/`.

## The goal

Round 1 builds chapter 14's first four families and opens chapter 15. It ends with the review, one fix pass, the second pass, the creative director's rescore and a short private progress page for Dustin (DR-241). Board 2 follows round 3. The bar is the guide's: a page that looks made by the best branding and design firm in the world, calm and exact, every rule earning its place. By the end of the round:

1. **Chapter 14 exists in the guide** as `work/build/guide/chapters/14-data-visualization.json`, with its opener, rules 14.1 to 14.14 for every chart, and the 41 entries of round 1 (14.15 to 14.45 and 14.125 to 14.134).
2. **26 new specimens** (S17 to S42) are drawn by the kit from frozen data, at every width and on both grounds, each with its table, exports and checks passing, and **4 sketches** (14.24, 14.43, 14.44, 14.45).
3. **The eleven built specimens** (S02 to S06, S09, S11, S13 to S15) sit in chapter 14 as entries.
4. **Chapter 15 has its rule list fixed** and its first plates: the systems grammar and worked examples 1 and 2.
5. **Round 3's data** is planned, signed off, fetched and frozen, and the seven remaining routes have official sources.
6. **The page holds its weight:** chapter 14 under its 2.804 MB stop, and a projection under 15.5 MB.

## Read first, every agent

`CLAUDE.md`; your role file in `.claude/agents/` (makers and the systems designer read the role description in this brief); `work/ledger/20261111_Gate-2-Report.md` section 9; the proposal, `work/handoffs/phase-2/20261111_Phase-3-Proposal-Draft.md`, sections 1, 5, 6 and 7; the coverage plan, `work/handoffs/phase-2/20261106_Data-Viz-Coverage-Plan.md`, sections 1 to 3; the decision log from DR-225 to the end, plus DR-44 to DR-72, DR-93, DR-98, DR-100, DR-124, DR-151 and DR-204 by search; chapter 02's writing rules, `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`, which bind every word; the engineer's round 0 contracts, `work/handoffs/phase-3/20261111_Round-0-Engineer-Notes.md`, section "Contracts" (C1 to C7); the plan file, `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`. Then the files your task names.

## Dustin's answers that shape this round

- **DR-240, chapter 14's shape.** Rules 14.1 to 14.14 apply to every chart, each with a correct and a failure plate. Each form then is a numbered entry in its family: when to use it, what to use instead, its specimen and table, and its phone drawing where the form changes. An avoid entry shows the misleading drawing as a small sketch beside the better choice. No form takes a failure plate of its own.
- **DR-241.** A progress page after this round shows its charts at desktop and phone widths and asks Dustin no decision.
- **DR-236.** The data palettes are approved, with the four-ink order Charcoal, Verdigris, Prussian, Stone, and Stone always hatched. Past four groups a chart splits into small multiples or shows one group in ink against gray (DR-234).
- **DR-238.** Chapter 14's hard stop is 2.804 MB. Chart data is carried compressed and every table stays live text.
- **DR-239.** S14's note carries the margin sentence; its figure prints in round 1 (D3-219).
- **DR-229.** No atlas domain supplies more than one example in four in chapter 14, and no state more than one in five. The data plan already holds the count; keep it.
- **Settled, never reopened:** Civic Line (DR-144 and the drawings it lists); R-01 and R-02 like every other reform (DR-223); System 1 (DR-36); Explainer on Newsprint with diverging pair B (DR-52 to DR-61); the coverage plan and its order (DR-62, DR-63); DR-64's chart rules; one standard of evidence (DR-93) with DR-124's wording; no disclosure anywhere (DR-100); invented bills from H.99001 and S.99002, labeled (DR-151); one dark mode on Charcoal (DR-204); chapter 13 as built (DR-237).

## Who does what

| Agent | Task | Owns (writes only these) | Notes file |
|---|---|---|---|
| Engineer (`oa-engineer`) | Round 1 contracts; entry support in the guide build; chapter 14's generator; the carried kit items; the makers' requests on shared kit code; the weight report | The kit's shared files (`kit.js`, `parts.js`, `kit.css`, `metrics.js`, `checks.js`, `oa-chart.mjs`, `words.json`, `README.md`, `tools/`, `fixtures/`); `work/build/scripts/phase-3/` except files named for others; `phase3_ch14_build.py`; `guide_build.py`, `guide_check.js`, `dataviz_check.js` and the shell; `work/build/tokens/`; `work/build/data/` sidecars the engineer's scripts write | `work/handoffs/phase-3/20261112_Round-1-Engineer-Notes.md` |
| Maker A, a general-purpose agent briefed as a senior data journalist and graphics editor who builds lookup tables and comparison charts | Comparison (3.1) and tables and plain words (3.15): S17 to S23 and S36 to S42, the radar sketch (14.24), and the entries for S03, S04, S06, S13's sparkline table and S15 | Forms `work/build/chart-kit/forms/<form-id>.js` for its new form IDs; specs `work/build/chart-kit/specs/s17.json` to `s23.json`, `s36.json` to `s42.json`, and `s03.json`, `s04.json`, `s06.json`, `s15.json`; entry files for its rules in `work/build/guide/entries/`; `work/build/guide/specimens/s-14-24-sketch.html` | `work/handoffs/phase-3/20261112_Round-1-Maker-A-Notes.md` |
| Maker B, a general-purpose agent briefed as a senior newspaper graphics editor who specializes in time series and change | Shift and swing (3.2) and change over time (3.3): S24 to S35, the sketches 14.43 to 14.45, and the entries for S02, S05, S09, S11, S13 and S14 | Forms for its new form IDs; specs `s24.json` to `s35.json`, and `s02.json`, `s05.json`, `s09.json`, `s11.json`, `s13.json`, `s14.json`; entry files for its rules; `s-14-43-sketch.html` to `s-14-45-sketch.html`; the data file `illustrative-benefit-cliff.csv` and its sidecar | `work/handoffs/phase-3/20261112_Round-1-Maker-B-Notes.md` |
| Editor (`oa-editor`) | Rules 14.1 to 14.14 with their plates and chapter 14's opener and introduction; a words pass on every spec and entry the makers write | Entry files `14-001.json` to `14-014.json`; `work/build/scripts/phase-3/phase3_ch14_rules_build.py`; specimens `s-14-<n>-correct.*` and `s-14-<n>-failure.*` for n 1 to 14, and `s-14-opener.*`; `work/build/guide/entries/14-chapter.json` (opener, introduction, group lines, sources) | `work/handoffs/phase-3/20261112_Round-1-Editor-Notes.md` |
| Research lead (`oa-research-lead`) | Round 3's data plan, signed off, fetched and frozen; workflow sources for FA, FR, ENF, CRT, AV, IC and CIV; any download list (four of DR-230's five remain) | New dataset files in `work/build/data/` under C1; `work/research/20261021_Research-Ledger.md` (Part 7, new rows); `work/research/20261111_Policy-Workflow-Sources.md`; `work/handoffs/phase-3/20261112_Round-3-Data-Plan.md` | `work/handoffs/phase-3/20261112_Round-1-Research-Notes.md` |
| Systems designer, a general-purpose agent briefed as the designer who drew chapters 11 and 12's systems plates | Chapter 15's rule list, file and generator; the systems grammar; worked examples 1 (Loop R1) and 2 (Loop R8) | `work/build/guide/chapters/15-systems-graphics.json`; `work/build/scripts/phase-3/phase3_ch15_build.py`; specimens `s-15-*`; `work/build/guide/specimens/manifest-systems-graphics.json` | `work/handoffs/phase-3/20261112_Round-1-Systems-Designer-Notes.md` |
| Data visualization lead (`oa-dataviz-systems-lead`), started when the first specimens land | Sign-off of every round 1 chart and of chapter 15's grammar and examples; sign-off of round 3's data plan | Its notes file only; changes go to owners as requests | `work/handoffs/phase-3/20261112_Round-1-Data-Lead-Notes.md` |

If you need a change in a file another agent owns, write it as a request in your notes under "Requests" and tell the main session in your summary. Do not edit it yourself. A maker who needs a shared drawing part (an axis, a key, a wrap) asks the engineer for it rather than copying kit code into a form.

## Contracts for round 1

C1 to C7 from round 0 stand. These add to them; the engineer writes anything more exact under "Contracts" in its notes within its first hour, and everyone follows that.

**R1. The plan file is the source of numbers.** `work/handoffs/phase-3/20261112_Chapter-14-Plan.json` fixes every rule number, family group, tier, round, spec ID, form ID, dataset and owner. Nobody renumbers; a maker who believes a form ID or dataset should change writes a request with the reason. The editor may tune the titles of rules 14.1 to 14.14 to chapter 02's rules but keeps each number and subject.

**R2. Entry files.** One JSON file per rule in `work/build/guide/entries/`, named `14-NNN.json` with the rule number padded to three digits (`14-016.json` for Rule 14.16). Keys, the same as a built chapter's rule plus three:

| Key | What it holds |
|---|---|
| `id` | `"14.16"` |
| `title` | One clause of about twelve words, in chapter 02's voice: "Use columns for a few categories or a short run of years" |
| `rule` | The rule as the guide states it, one or two sentences |
| `use_when` | When this form is the right choice, one or two sentences, from the reader's question |
| `use_instead` | A list of `{"when": "...", "rule": "14.NN"}`: when another form serves better, and which |
| `why` | Why the rule holds, one to three sentences |
| `specimen` | The spec ID it shows (`"S17"`), or its sketch ID (`"s-14-24-sketch"`) |
| `tier` | `core`, `extended`, `reference` or `avoid`, as the plan sets it |
| `tokens` | Token names the entry's words name, or `[]` |
| `related` | Rule numbers it cites (`"13.1"`, `"14.4"`), never restating them |
| `builders` | One line for a builder: the form ID and the kit command that draws it |
| `correct`, `failure` | For an entry: `correct` is null (the specimen is the plate) and `failure` is null (DR-240). For rules 14.1 to 14.14: chapter 13's shape, a correct and a failure plate |

**R3. Specimens in the guide.** An entry's chart is drawn from its kit spec by ID (`work/build/chart-kit/specs/s17.json`), placed by the generator as `<div data-oa-chart="s17">`. Every spec carries its table equivalent (C5). A spec's `domain` and `states` feed chapter 14's example log (Rule 01.12), which the generator writes and checks against Rule 01.9.

**R4. Sketches.** A reference or avoid sketch is an HTML fragment `work/build/guide/specimens/s-14-NN-sketch.html` holding one inline SVG, at most 4 KB for a reference sketch and 2 KB for an avoid sketch, drawn only in the kit's color role classes the engineer lists in its round 1 contracts (no literal color), with a title, an "Illustrative data" label inside the drawing, and a one-line description for screen readers. An avoid sketch draws the misleading form small; its entry's `use_instead` names the better choice.

**R5. Form modules.** A maker's form registers under C4 and draws only through the context, so every form inherits the layout guard, the color roles and the checks. A form never writes a color, a font name or a reader-facing word. Each form passes `oa-chart.mjs build` for its spec at 656, 558, 358, 296 and 256 px on both grounds, with page-to-Node parity.

**R6. Weight.** Chapter 14's stop is 2,803,941 bytes. The engineer's build report gives each round's share per plate; a specimen far over its tier's average fails `--strict`. Makers keep a specimen's data to the rows its chart and table draw.

**R7. Chapter 15's numbers** are fixed by the main session from the systems designer's proposed rule list before any other chapter cites them.

## Each task in more detail

**Engineer.** You take round 1 after the board 1 apply pass.
1. Round 1 contracts within your first hour: the kit's role classes for sketches (R4), any rule a form module must follow beyond C4, and the shared parts available to makers.
2. The guide build learns an entry: a rule whose plate is its specimen and which carries no failure plate, printing `use_when` and `use_instead` with live cross-references. Chapter 14's rail may list groups and only open each group's rules, if 141 rules crowd it; measure and decide.
3. `phase3_ch14_build.py` assembles `14-data-visualization.json` and `manifest-data-visualization.json` from the plan file, the editor's `14-chapter.json` and entry files, and the makers' entries and specs; writes chapter 14's example log; and fails on a missing entry for a built round, a number that disagrees with the plan, or Rule 01.9 over its limits.
4. Carried items: S05's gap brackets (D3-191); the light fill when a spec names one bar (R3, D3-164); the payroll margin's printed source line (D3-219), which maker B then prints in S14.
5. The makers' requests on shared code, in the order they arrive, logged in your notes.
6. Each build's weight report: chapter 14 against 2.804 MB, the share per plate still to come, and the page projection.

**Maker A** and **Maker B.** You are senior graphics editors at a newsroom known for exact, quiet charts. For each new specimen in your rows of the plan file:
- Read its data plan row (`work/handoffs/phase-3/20261111_Rounds-1-2-Data-Plan.md`, round 1 table, and the sign-off and fix pass sections below it), its dataset and sidecar in `work/build/data/`, and the coverage plan's row for the form.
- Write the form module if the form is new, then the spec under C2, then the entry under R2.
- Build it with `node work/build/chart-kit/oa-chart.mjs build sNN --out <your scratch>/kit-out` and fix every failed check. Look at every capture at 1440 and 390 px on both grounds and in grayscale, the way a design director would at twice size, and fix what reads badly even when the checks pass.
- Titles follow Rules 13.1 and 13.2: the evidence kind, and the verb its grade allows. Source lines follow Rule 13.6 and equal the sidecar's line. Every figure in a title or note is checked by script against the data, with the check named in `notes_internal`. Party data takes neutral inks with each party named on its mark (DR-48, DR-58); no election graphic uses red and blue (DR-64). Report what the record shows, read every title from the left and the right, and never add, soften or drop a finding for balance (DR-93, DR-124).
- For the built specimens in your rows, write only their entries and any word fix the editor asks for; their drawings stay as approved on board 1 unless a check fails.
- Draw your sketches last, after the engineer lists the role classes.
- Maker B also prints the payroll margin in S14 once the engineer's source line lands (D3-219), and writes `illustrative-benefit-cliff.csv` with its sidecar (`"kind": "illustrative"`) on the pattern the data plan row 28 names, telling the research lead.
- Maker A's filterable lookup table (S38) works by keyboard and screen reader and announces its count of results; it prints usefully with scripts off. Its interaction follows chapter 18's components.

**Editor.**
- Rules 14.1 to 14.14, each with its purpose, a correct plate and a failure plate. A plate that draws a chart uses a kit spec beside it (`s-14-<n>-correct.chart.json`, C7). Plates draw on frozen data in `work/build/data/` where real data teaches the rule, or carry "Illustrative data". Cite Rules 01.9, 05.3, 13.1 to 13.13, H08 and H09 by number and never restate them. Every failure caption leads "Fails Rule 14.N." and every failure plate a reader could lift carries the do-not-publish bar. Titles run to one clause of about twelve words.
- Chapter 14's opener (under 16 KB, D2-1708), introduction, the 17 group lines and sources, in `14-chapter.json`.
- Keep rules 14.1 to 14.14 with the opener under 0.20 MB, so round 5's selection guide and palette specification keep 0.10 MB.
- The words pass: read every spec and entry as the makers finish them and send each maker a list of word changes (title, reading guide, measure line, notes, source line, alt, entry words) under "Requests". The makers apply them. You own the words; they own the files.

**Research lead.**
- Round 3's data plan for its 32 forms (coverage plan sections 3.10 to 3.14: behavior, structure, relationships, flow, maps), in the shape of the rounds 1 and 2 plan, with Rule 01.9 counted for chapter 14 as a whole. Election data stays on forms built for elections (DR-229). Maps need state and district geometry; record its source and rights. Send the plan to the data lead for sign-off, then fetch and freeze each dataset under C1 with a ledger row.
- Workflow sources for FA, FR, ENF, CRT, AV, IC and CIV from the proposal's section 1.4, from official sources with the date checked.
- A download list only if a site refuses and no other primary source serves (DR-230 leaves four).
- Keys: FEC and Congress.gov keys are injected by the proxy (set any key variable a script needs to `proxy-injected`); the Census key is `CENSUS_API_KEY`, never printed, logged, written to a file or saved in a URL.

**Systems designer.** You drew chapters 11 and 12's systems plates in Phase 2, and you know the line code, typed chips, the loop stepper and the red target.
- First, within your first hour: chapter 15's rule list, numbers and subjects, in your notes under "Rule list", built from the proposal's sections 1.3 to 1.5 and Master Brief section 14. The main session fixes it (R7).
- Then the chapter file, generator and the first plates: the systems grammar (signed links, loops, open chains, boundaries, the authority link with no sign) and worked examples 1 (Loop R1, using chapter 11's live stepper) and 2 (Loop R8, with V7's own words on the model's revision).
- Every atlas value is read by script from `work/extract/atlas-v7-data.json` (snapshot October 15, 2026, printed beside anything that could have moved). The line code comes from the atlas build's `wire_marks` constants with the 28 px lead-in from `oa.chart.grade.leadIn` (D3-105, D3-165). Typed chips for every ID (H11). No effect total. Chapter 15 stays under 0.25 MB at this round's end, inside its 0.60 MB ceiling.
- Read the Phase 2 builders before you start: `work/build/scripts/phase-2/apply_systems_ch11.py` and `stage_b_ch12_systems_build.py`, and chapters 11 and 12 in `work/build/guide/chapters/`.

**Data visualization lead** (started by the main session when the first specimens land). Sign off each round 1 chart against the palettes (DR-236), DR-64's rules, chapter 13's rules and the coverage plan's intent, and chapter 15's grammar and examples. Sign off round 3's data plan under Rule 01.9 and DR-229. Send changes to owners as requests.

## Who works when

1. Now: maker A, maker B, the editor (after its apply pass part B), the research lead (after its apply pass) and the systems designer start. Makers write forms, specs and entries; sketches wait for the engineer's role classes.
2. After the board 1 apply pass: the engineer takes round 1 and writes its contracts first.
3. When the first specimens land: the data lead starts its sign-offs; the editor starts its words pass.
4. When the systems designer posts its rule list: the main session fixes chapter 15's numbers.
5. When all report: the main session runs the review (three red team agents covering six lenses, the creative director's first pass), one fix pass, the second pass, the rescore, the checks and the progress page.

## Notes and limits for every agent

- Write your notes file with sections: "Summary", "Contracts" (engineer), "Rule list" (systems designer), "Routine calls" as `- D3-xxx | decision | reason` lines, "Requests", "Tested" and "Not tested". The main session numbers and logs the calls. Write your notes early and keep them current, since the container can restart.
- Never touch `source/` or `deliverables/`. Never edit Atlas V7. Do not commit or push; the main session commits. Never run `git checkout --` or any command that discards changes.
- Scratch work and every capture you do not deliver go to `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f15cd04b-21be-5dde-a467-804e951756a2/scratchpad/phase-3/round-1/<your-role>/` by absolute path, never into the repository by a relative path. Run Playwright scripts with absolute output paths.
- Python reading supplied or downloaded files runs with `-I`. Downloads go into their own new folder.
- Every number outside the atlas carries its source, period and qualification, or the chart carries "Illustrative data" beside it.
- File names follow `CLAUDE.md`: `YYYYMMDD_Title-Case.ext` with 20261112, lowercase kebab-case folders; source code and data keep their conventions.
- No em dashes, no U+2011, no disclosure line, no decision codes or studio words in reader text.
- Report what you tested and what you did not as separate lists. Never describe a check you did not run.
- Your final message to the main session: a summary of under 200 words, the paths you wrote, and anything blocking.
