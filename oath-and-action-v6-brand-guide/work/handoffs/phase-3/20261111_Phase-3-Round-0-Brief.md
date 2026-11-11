# Brief: Phase 3, round 0, the chart kit, the palette proofs and chapter 13

Oath & Action Edition 06, Phase 3, November 11, 2026. Written by the main session for round 0's makers. Gate 2 approved the Phase 3 proposal as proposed (G2-01). Dustin's Gate 2 decisions are DR-229 to DR-232; his answers on the round 0 plan are DR-233 to DR-235. The studio's Phase 3 calls run from D3-01. Paths are relative to `oath-and-action-v6-brand-guide/`.

## The goal

Round 0 ends at board 1, where Dustin approves the palette colors and chapter 13 and sees the chart kit proven on the 16 charts Phase 2 finished. The bar is the guide's: a page that looks made by the best branding and design firm in the world, calm and exact, every rule earning its place. By the end of the round:

1. **The chart kit** draws S01 to S16 from their data files with one command, at 1440 and 390 px on Newsprint and Charcoal, with SVG, PNG and CSV exports, and every check passing.
2. **The drawing method** is chosen by measurement on those 16 charts, and chapter 14's projected weight for 97 finished specimens is known against its 1.75 MB stop.
3. **The palette proofs** show every data palette on every approved surface, measured, in grayscale and under three color-vision simulations, with the red-on-red specimen.
4. **Chapter 13** is built in the guide: 13 rules, each with its purpose, a correct plate and a failure plate, under 0.25 MB.
5. **Rounds 1 and 2's data** is fetched and frozen with sidecars and ledger rows, with the Rule 01.9 count for those rounds.

## Read first, every agent

`CLAUDE.md`; your role file in `.claude/agents/`; `work/ledger/20261111_Gate-2-Report.md` section 9; the proposal, `work/handoffs/phase-2/20261111_Phase-3-Proposal-Draft.md` (all of it); Master Brief sections 8, 13, 14, 15 and 22 in `brief/20261021_Oath-And-Action-V6-Master-Brief_V2.md`; the decision log from DR-225 to the end, plus DR-44 to DR-72 and DR-93, DR-97, DR-98, DR-100, DR-124, DR-151, DR-204 and DR-222 by search; chapter 02's writing rules, `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`, which bind every word. Then the files your task names.

## Dustin's answers that shape this round

- **DR-233, corrections.** Chapter 13 adds a rule: a dated note at the top of the piece that says what was wrong and what changed; the fixed chart replaces the old one; a corrections page keeps every note.
- **DR-234, groups.** The categorical set is the four brand inks, Charcoal, Prussian, Verdigris and Stone, with no added hue. Past four groups a chart splits into small multiples or shows one group in ink and the rest in gray, every group labeled on the chart. Verdigris and Stone never tell two groups apart alone (D2-95).
- **DR-235, a page later.** The renderer must run in a plain browser page with no install and no build step, reading `tokens.css`, a data file and a spec, so a later page can let a person drop in a CSV, pick a form and download the SVG, PNG and CSV. That page is not built now; it goes to Gate 3 as a proposed item for Phase 5's asset package.
- **DR-229, Rule 01.9.** No atlas domain supplies more than one example in four in a chapter, and no state more than one in five. Election data stays on forms built for elections; other forms take data from taxes and budgets, work and pay, housing, Congress and agencies.
- **DR-232, if chapter 14 runs over.** Only if the pilot projects chapter 14 over 1.75 MB with the lightest method: first the reference and avoid sketches become one image sheet, then extended forms whose form does not change drop their separate phone drawing. If both fall short, board 1 asks Dustin.
- **Settled, never reopened:** Civic Line (DR-144 and the drawings it lists); R-01 and R-02 like every other reform (DR-223); System 1 (DR-36); Explainer on Newsprint with diverging pair B (DR-52 to DR-61); the coverage plan and its order (DR-62, DR-63); DR-64's chart rules; one standard of evidence (DR-93) with DR-124's wording; no disclosure anywhere (DR-100); invented bills from H.99001 and S.99002, labeled (DR-151); one dark mode on Charcoal (DR-204).

## Who does what

| Agent | Task | Owns (writes only these) | Notes file |
|---|---|---|---|
| Engineer (`oa-engineer`) | The chart kit; the drawing-method pilot; the data folder's layout; the weight gates in the build; the V7 check and the chart check grown for Phase 3; the token pre-release that carries the palette tokens | `work/build/chart-kit/`; `work/build/data/` (layout, schema, and the 16 specimens' data moved in); `work/build/scripts/phase-3/` except files named for others; `guide_build.py`, `guide_check.js`, `dataviz_check.js` and the shell; `work/build/tokens/` | `work/handoffs/phase-3/20261111_Round-0-Engineer-Notes.md` |
| Data visualization lead (`oa-dataviz-systems-lead`), working with the design director's eye (read `oa-design-director.md` too) | The palette proofs and the proposed palette tokens; then the sign-off of the research lead's rounds 1 and 2 data plan | `work/boards/phase-3/round-0/palettes/`; `work/handoffs/phase-3/20261111_Palette-Proposal.json` | `work/handoffs/phase-3/20261111_Round-0-Palette-Notes.md` |
| Editor (`oa-editor`), with the data lead's rules in view | Chapter 13 whole: words, plates and its generator | `work/build/guide/chapters/13-evidence.json`; `work/build/scripts/phase-3/phase3_ch13_build.py`; specimens `s-13-*`; `work/build/guide/specimens/manifest-evidence.json` | `work/handoffs/phase-3/20261111_Round-0-Editor-Notes.md` |
| Research lead (`oa-research-lead`) | Rounds 1 and 2's data plan, fetched and frozen; the five-download list; the first workflow sources; the lessons of Our World in Data, LOOPY and En-ROADS; the outcomes of R-01's two November 3 ballot measures | New dataset files in `work/build/data/` under the engineer's schema; `work/research/20261021_Research-Ledger.md` (a new Part 7, Phase 3 data); `work/research/20261111_Policy-Workflow-Sources.md`; `work/research/20261111_Data-And-Interaction-Lessons.md`; `work/handoffs/phase-3/20261111_Rounds-1-2-Data-Plan.md` | `work/handoffs/phase-3/20261111_Round-0-Research-Notes.md` |
| Explainer maker (a general-purpose agent briefed as a senior newspaper graphics editor), starting once the engineer's contracts are written | S01 to S16 rebuilt as kit specs, with their words, at both widths and both grounds | The 16 spec files in the folder the engineer names; captures in `work/boards/phase-3/round-0/specimens/` | `work/handoffs/phase-3/20261111_Round-0-Explainer-Notes.md` |

If you need a change in a file another agent owns, write it as a request in your notes under "Requests" and tell the main session in your summary. Do not edit it yourself.

## Contracts

The engineer writes the exact formats into its notes' "Contracts" section as its first deliverable, within its first hour, and the others follow them. These points are fixed now so everyone can start:

1. **Data files.** One dataset per file in `work/build/data/`, named for its publisher and contents in lowercase kebab-case, such as `census-spm-child-poverty.csv`, with a sidecar `<name>.meta.json`. The sidecar keeps Phase 2's fields (see `work/boards/phase-2/data-viz/shared/public/census-spm-child-poverty.meta.json`): publisher, title or table, table or series ID, URL, observation period, geography, universe, unit, date retrieved, vintage, qualification, columns. It adds `printed_source_line` (H04's order: publisher, title or table, period, geography, date retrieved, the qualification that matters), `ledger_row` (its row in the research ledger's Part 7), `domain` (the Atlas V7 domain it serves, for Rule 01.9) and `states` (state codes it names, or none). Atlas V7 data comes from `work/extract/atlas-v7-data.json` by script into `v7-*.json` files whose sidecar names the snapshot, October 15, 2026. Phase 2's board files stay where they are as records; the engineer copies their data in.
2. **Spec files.** One file per specimen that holds every word and setting the chart prints: its ID (S01 to S16 keep theirs), form, family, tier, dataset, reader question, evidence kind (finding, association, estimate or illustration), V7 grade where it applies, title, reading guide, measure line, notes, source line, the Illustrative flag, alt text, the table equivalent's columns, whether a phone drawing differs (DR-64), domain and states. Words never live in the renderer or a form's code (the generator trap).
3. **Color and type.** A chart takes color only from `oa.chart.*` tokens, as CSS custom properties from `tokens.css`; no literal color in a spec, form or renderer. Type follows Rule 06.1's one set; no text under 13 px except where Rule 06's exceptions allow it, and the guide check fails off-scale sizes. One working red per view (Rule 05.3); red never touches Prussian.
4. **The renderer.** Plain JavaScript with no outside library unless the engineer measures it and logs the call, running in a browser page with no build step (DR-235) and in the build for exports and still images. One renderer draws the guide, the exports and the boards, so they cannot drift.
5. **The table equivalent.** Every specimen carries its table as live text, readable with scripts off, with rows equal to its data file. The build fails a specimen without one.
6. **IDs and words.** Typed chips for every atlas ID (H11). IDs print with an ASCII hyphen in a no-wrap span, never U+2011 (D2-975). No em dashes. No disclosure line anywhere (DR-100); the chart check fails any copy of the old one.
7. **Chapter 13's numbers, fixed ahead** so chapters 14 and 15 can cite them. The editor may tune each title to chapter 02's rules but keeps the number and subject:

| Rule | Subject |
|---|---|
| 13.1 | Title a chart or diagram as a finding, an association, an estimate or an illustration |
| 13.2 | Give the title the verb its grade allows |
| 13.3 | Print V7's grade words with a plain gloss, from one mapping table |
| 13.4 | Draw a connection's grade in V7's line code |
| 13.5 | Keep grade, effect size, uncertainty and delay apart |
| 13.6 | Write the source line in its six parts |
| 13.7 | Print the period and the vintage, and give charts shown together one window |
| 13.8 | Label an invented item beside it |
| 13.9 | Name every atlas ID in its typed chip |
| 13.10 | Date what can change, and print an undated route as not checked |
| 13.11 | Draw documented events apart from causal findings |
| 13.12 | Quote a person exactly, with who, when and where |
| 13.13 | Correct in the open (DR-233) |

Where chapter 01 or 02 already states a rule (H03, H04, H08, H09, H11, Rules 01.9, 01.11, 01.12, 01.22, 01.23 among them), chapter 13 cites it by number and shows its evidence side, so no rule is stated two ways.

## Each task in more detail

**Engineer.** Read the proposal's section 3 and section 7 closely; they are your specification.
- The kit: one shared renderer; a module per form for the forms S01 to S16 use (19 of the 127, by the proposal's count); `register_chart()`; the layout guard; SVG, PNG and CSV exports; one command that builds a chart from its spec and data and runs its checks. Model the look on the approved Explainer (`work/boards/phase-2/data-viz/01-explainer/`) and the stretch page (`.../stretch/`), whose drawings Dustin approved (DR-52 to DR-61, DR-64).
- The pilot: measure at least lean inline SVG and drawing when the page loads on all 16 charts in a guide build, and any third method you think lighter. Pick the lightest that passes the guide check at 1440 and 390 px, axe-core, a page with scripts off (words and tables readable), print, forced colors, reduced motion and export parity. Project chapter 14 for 97 specimens, 22 sketches and 8 avoid entries with the proposal's other parts, and report against 1.75 MB. If it runs over, apply DR-232's order and report what each step saves.
- The gates: chapter ceilings 13 at 0.25, 14 at 1.75 and 15 at 0.60 MB; chapter 14's stop fails every mode; the projection test against 15.5 MB; the fonts as their own part; a self-test that plants each fault.
- The checks: grow the V7 check and the chart check of the proposal's section 7 enough to run on round 0's work (every V7 value in S01 to S16 and chapter 13; source lines against sidecars; the disclosure; grayscale captures with the lightness-margin test on each key). Chapter 13 is built through `guide_build.py` like every chapter; keep the strict build at 0 warnings.
- Tokens: add the palette tokens from the data lead's proposal as one pre-release named under Rule 26.8, marked in their descriptions as proposed until board 1, with the token tests passing and tokens.css and tokens.json in parity.
- Phase 2's chart scripts stay as records. Do not rerun the November 10 promotion scripts.

**Data visualization lead.** The proposal's section 1.6 is your specification, under DR-234.
- Proofs for the sequential Verdigris steps, diverging pair B with new Charcoal steps for dark mode, the four-ink categorical set with direct labels and patterns, the magnitude Stone steps, the grade line code as dash patterns (V7's renderer: dotted hypothesis, dashed plausible, dash-dot contested, solid documented and well supported), and the red emphasis point. Each proof on Newsprint and Charcoal, and on White and Prussian where the rules allow; each with measured contrast of fills against ground and labels against fills, grayscale, and protanopia, deuteranopia and tritanopia simulations; the grade patterns at 1x and 2x in color and in black.
- The red-on-red specimen (Master Brief tension 14): a chart whose data already uses red meets a status red, resolved in a drawn specimen.
- Show what happens past four groups (DR-234) with one proof of small multiples and one of one group in ink against gray.
- Write the proposed token values in `20261111_Palette-Proposal.json` (names under the token architecture, values, which surfaces, measured ratios) and send them to the engineer through your notes. New colors are only those dark-mode and step values the existing tokens lack; no new hue.
- When the research lead's data plan lands, read it and sign it off or send changes, under Rule 01.9 and DR-229.

**Editor.** Chapter 13 as the table above sets it, in the shape of the built chapters: model the file on `work/build/guide/chapters/11-icons.json` (keys `number`, `anchor`, `title`, `part`, `instruction`, `intro`, `groups`, `rules`, `extras`, `related_chapters`, `sources`; each rule `id`, `title`, `rule`, `tokens`, `why`, `correct`, `failure`, `specs`, `related`, `builders`), written by your generator. Every chapter now opens on an opener plate under 16 KB (D2-1708). Failure captions lead "Fails Rule 13.N." and every failure plate that draws a piece a reader could lift carries the do-not-publish bar (CD-S2). Titles run to one clause of about twelve words. Plates draw on chapter 01, 02 and 12's existing styles and devices; a plate that draws a chart uses the kit once it lands, or a static SVG you swap for the kit's output before the review. Real examples carry their real sources; invented ones carry Illustrative beside the item. Rule 13.13's correct plate shows a correction note at the top of a piece and a corrections page entry, both Illustrative. Keep chapter 13 under 0.25 MB.

**Research lead.** Stay one round ahead.
- The data plan for rounds 1 and 2: for each of their 82 forms in `work/handoffs/phase-2/20261106_Data-Viz-Coverage-Plan.md`, the reader question, the dataset, its publisher, period and geography, its atlas domain and states, and whether it is primary, labeled secondary or Illustrative. Count the plan by domain and by state for chapter 14 as a whole (with S01 to S16 included) under Rule 01.9 and DR-229, and re-pick until no domain passes one in four and no state one in five. Send the plan to the data lead for sign-off, then fetch and freeze each dataset under the engineer's schema with a ledger row. Use your own api.data.gov and Census access: FEC and Congress.gov keys are injected by the proxy (set any key variable a script needs to `proxy-injected`); the Census key is the environment variable `CENSUS_API_KEY`, which you never print, log or write to a file, and never put in a URL you save.
- The five-download list (DR-230): up to five files Dustin downloads himself from sites that refuse automated readers, each with its exact page, file name and the specimen it serves. Only files rounds 1 and 2 need; fewer is better.
- Workflow sources for chapter 15: start with FS, SS, BI and LOC from the proposal's section 1.4, from official sources with the date checked.
- The lessons of Our World in Data, LOOPY and En-ROADS (Master Brief sections 13 and 14), as teachable rules.
- The November 3, 2026 outcomes of the two ballot measures named in R-01's V7 status, from official or labeled secondary sources, into the research ledger and as a V7.1 issue-list item for the data lead. V7 is never edited.

**Explainer maker** (started by the main session when the engineer's contracts land). Rebuild S01 to S16 as kit specs from their Phase 2 words and data (`dataviz_shared_data.py`, `dataviz_stretch_data.py`, the Explainer and stretch pages), with every later decision applied: S01 names "H.R. 7008, the Stop Insider Trading Act" with both provisions at first mention (DR-98) and keeps D2-104's vote totals unless the research lead can now read the Senate's record; no disclosure (DR-100, D2-1756); DR-124's wording; typed chips; "Fails Rule" captions where a failure is drawn. Capture each at 1440 and 390 px on Newsprint and Charcoal, with its grayscale proof.

## Who works when

1. Now: the engineer, the data lead, the editor and the research lead start together.
2. When the engineer's "Contracts" section is written: the main session starts the Explainer maker, and tells the others.
3. When the data lead's palette proposal lands: the engineer adds the tokens.
4. When the research lead's data plan lands: the data lead signs it off.
5. When all five report: the main session runs the review (three red team agents covering six lenses, the creative director's first pass), one fix pass, DR-191's short second pass, the creative director's scores and the checks, then board 1.

## Notes and limits for every agent

- Write your notes file with sections: "Summary", "Contracts" (engineer), "Routine calls" as `D3-xxx | decision | reason` lines, "Requests", "Tested" and "Not tested". The main session numbers and logs the calls. Write your notes early and keep them current, since the container can restart.
- Never touch `source/` or `deliverables/`. Never edit Atlas V7. Do not commit or push; the main session commits. Never run `git checkout --` or any command that discards changes.
- Scratch work and every Playwright capture you do not deliver go to `/tmp/claude-0/-home-user-Dustin-s-Command-Center/31ab6fca-308a-5402-b22c-b6bfd31a97ee/scratchpad/phase-3/round-0/<your-role>/` by absolute path, never into the repository by a relative path.
- Python reading supplied or downloaded files runs with `-I`. Downloads go into their own new folder.
- Every number outside the atlas carries its source, period and qualification, or the chart carries "Illustrative data" beside it. Report findings as the record shows them (DR-93), never adding, softening or dropping one for balance.
- File names follow `CLAUDE.md`: `YYYYMMDD_Title-Case.ext` with 20261111, lowercase kebab-case folders; source code keeps its language's conventions.
- Report what you tested and what you did not as separate lists. Never describe a check you did not run.
- Your final message to the main session: a summary of under 200 words, the paths you wrote, and anything blocking.
