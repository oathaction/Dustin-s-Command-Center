# Brief: Phase 3, round 5, chapter 14's front door and three charts in full, chapter 15's workflows and reconciliation, and two new trackers

Oath & Action Edition 06, Phase 3, November 14, 2026. Written by the main session for round 5's owners, on round 4's model (`work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`). Gate 2 approved the Phase 3 proposal (G2-01), whose section 9 sets this round. Dustin's answers through DR-271 hold. The studio's calls continue from D3-1868. Paths are relative to `oath-and-action-v6-brand-guide/`.

**Status: approved.** Dustin replied "GO AS RECOMMENDED" on November 14, 2026: the plan (DR-276) and the four questions as recommended (DR-272 to DR-275). The systems designer's work splits in two by file (D3-1877), so round 5 has eleven owners.

## The goal

Round 5 finishes chapters 14 and 15 and adds chapter 11's last two trackers. The build ends when every owner has reported and the strict build, the kit's `build --all` and the quick guide check pass. The review of rounds 4 and 5 together, one fix pass, the second pass and the creative director's rescore follow in the next chat, then board 3 and Gate 3. The bar is the guide's: a page that looks made by the best branding and design firm in the world, calm and exact, every rule earning its place. By the end of the build:

1. **Chapter 14 opens on a selection guide, "Choose a chart"**, between its opener and Rule 14.1: all 127 forms under the 16 reader questions that name the chapter's families, each form a link to its entry with its tier, and each drawn as a small picture of the form (Q5-2). This is the creative director's front door (board 2, round 1 and round 3 reviews).
2. **The palette specification sits after Rule 14.5**, which it serves, as a labeled reference plate: every data palette by job (sequential, diverging pair B, the four-ink groups with Stone hatched, magnitude), its tokens and values on each approved ground, contrast, grayscale and three color-vision proofs, written by script from the tokens so it cannot drift from them (DR-234, DR-236).
3. **Three charts in full** close chapter 14 as a new group 18, Rules 14.142 to 14.144, the three complex examples Gate 2 approved: S14's monthly job change with its three-month average; Loops B4 and R10 stepped one connection at a time through the variable they share; and the three reforms that act on Loop R8 (R-06, R-30, R-38) compared by target, band, ordinal effects, grades and routes, with no summed score.
4. **Rules 15.22 to 15.25 exist with their plates**: the federal statute drawn as its whole workflow through reversal (15.22); which stages sit behind each tracker's six steps (15.23); the 11 routes to change as a reference set, each with its official source and the date it was checked, an undated route printed as not checked (15.24); and the reconciliation table, all 2,644 comparisons rerun (DR-258), each conflict's model value, its resolution and where the guide applies it (15.25).
5. **The ballot measure and court case trackers (DR-231)** join chapter 11's group 2 as Rules 11.10 and 11.11 (DR-274), six-step trackers under DR-108 and DR-150 with invented items labeled Illustrative (DR-275). Today's Rules 11.10 to 11.16 become 11.12 to 11.18, every link fixed in one pass.
6. **Carried items closed:** S95's second crop named by its size (the accessibility lead's low item); ED4-7, S92's sidecar source line.
7. **Weight is reported, never a stop (DR-271).** The page stays one file under 16 MB, with the 15.5 MB projection as its early warning; every plate's bytes are reported; no form, word or picture is cut to meet a figure.

## Read first, every agent

`CLAUDE.md`; your role file in `.claude/agents/` where you have one (the makers, the tracker designer and the systems designer read the role description in this brief); `work/ledger/20261111_Gate-2-Report.md` section 9; this brief, all of it; round 4's brief, `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`, whose calls and contracts R4-1 to R4-7 still hold where this brief does not replace them; the decision log from D3-1675 to the end, with DR-44 to DR-72, DR-93, DR-108, DR-124, DR-144, DR-150, DR-151, DR-195, DR-204 and DR-223 to DR-276 by search; chapter 02's writing rules, `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`, which bind every word; the engineer's contracts (the round 0 to round 4 engineer notes, "Contracts" and their fix pass sections) and the component engineer's round 4 notes; the data lead's round 4 notes, "Rulings" and every "Sign-off" section; the accessibility lead's round 4 "Interaction specification"; the plan file, `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`; the coverage plan, `work/handoffs/phase-2/20261106_Data-Viz-Coverage-Plan.md`; for chapter 15 and the trackers, `work/research/20261111_Policy-Workflow-Sources.md`, `work/handoffs/phase-3/20261112_Round-1-Systems-Designer-Notes.md` (chapter 15's rule plan), `work/handoffs/phase-0/20261020_Atlas-Reconciliation-Table.md` and `work/research/20261113_Atlas-Recheck-Full-Table.md`. Then the files your task names. The container is set up: the atlas model is at `work/extract/atlas-v7-data.json`, and `npm` and `pip` packages are installed.

## Dustin's answers to the four questions (DR-272 to DR-275)

All four as recommended. The table keeps the questions as asked.

| # | Question | Recommendation |
|---|---|---|
| Q5-1 | The data keys are saved on the environment "Oath & Action Brand Polish - Round 2", and this chat runs on "Oath & Action", which holds none: today FEC and Congress.gov answered 403 and the Census variable is absent. Round 5 needs Congress.gov at most, for a bill's actions in the federal workflow; it needs no FEC or Census data. May the studio open the secure key form for api.congress.gov on this environment when the research lead first needs it? | Yes. Future chats start on the environment that holds all three keys, or you add them to this one in its settings |
| Q5-2 | Should the selection guide draw every form as a small picture under its question, or list the forms as a table of names by question and tier? | Pictures, as the creative director asked: about 127 small drawings in one style from one shared set of symbols, near 100 to 150 KB, which DR-271 allows; the projection stays under 15.5 MB |
| Q5-3 | Where do the two new trackers sit in chapter 11? (A) In group 2 beside records requests and agency rules, as Rules 11.10 and 11.11, with today's 11.10 to 11.16 each moving two numbers and every link fixed in one pass, as D2-325 did for chapter 08. (B) As a new group 5 at the chapter's end, Rules 11.17 and 11.18, with no number moving | (A): a reader meets all six trackers in one group. Nothing has shipped, the guide check proves every same-page link, and the change ledger maps old numbers to new for the log's history |
| Q5-4 | Real ballot measures and court cases on the plates, or invented ones labeled Illustrative as chapter 11's other trackers use (DR-151, Rules 11.8 and 11.9)? | Invented and labeled, with each step's name and end words taken from the law and its source cited. A plate shows three items in different states side by side, real items rarely line up that way, and a pending real one (the 2026 measures, a case on appeal) would be out of date by launch. Real cases stay in chapter 15's court workflow as the steps' source |

## Dustin's answers that shape this round

- **DR-272 to DR-276.** The four answers above and the plan as posted.
- **DR-271.** Allocations move as content needs; only the page's 16 MB is fixed, with the 15.5 MB projection as its early warning. Report each plate's bytes; never cut a form, word or picture to meet a figure.
- **DR-231.** Ballot measure and court case trackers join chapter 11 as six-step trackers under DR-108 and DR-150, drawn by the systems designer and shown on board 3.
- **DR-254.** The guide page offers no per-chart download; each chart's full data is one CSV in Phase 5's asset package, named through `{data_file}`. A complex example's exports are the kit's, checked row for row by the engineer, never a page button.
- **DR-258 and C-101.** All 2,644 of Phase 0's comparisons were rerun on November 13 from Dustin's three uploads, every result Phase 0's (`work/research/20261113_Atlas-Recheck-Full-Table.md`).
- **DR-234, DR-236.** The categorical set is the four brand inks, Charcoal, Verdigris, Prussian, Stone, in that order, Stone always hatched; diverging pair B on Charcoal takes #828A9D and #505C7D.
- **DR-223.** R-01 and R-02 are treated like every other reform.
- **Settled, never reopened:** Civic Line (DR-144 and the drawings it lists); System 1 (DR-36); Explainer on Newsprint with diverging pair B (DR-52 to DR-61); the coverage plan and its order (DR-62, DR-63); DR-64's chart rules, among them no red and blue on any election graphic, with DR-255's one exception; one standard of evidence (DR-93) with DR-124's wording; no disclosure anywhere (DR-100); invented bills from H.99001 and S.99002, labeled (DR-151); one dark mode on Charcoal (DR-204); chapter 13 as built (DR-237); DR-265 and DR-267's one name per variable in every loop drawing; chapter 02's writing rules (DR-73 to DR-83).

Nonpartisan means one standard of evidence for everyone, with findings reported as the record shows them, even when they fall more on one side (DR-93). Never add, soften or drop a finding for balance.

## Rounds 1 to 4's calls, now rules for every round 5 item

Round 4's brief's eight calls hold, with call 3 replaced by DR-271. Round 4 added these.

1. **Weight is reported (DR-271).** Each build reports each plate's bytes, chapter 14 and 15's totals and the projection; nobody cuts content to meet them.
2. **Measure a global change's reach before landing it (V25).** A change to a shared kit part, the shell or a token is measured over every drawing it touches and landed opt-in if it would move a signed-off drawing.
3. **Cards and reference sets as HTML text (R4-3).** Lists, tables, stage lists and the selection guide's names are live HTML text a reader can search and copy; the kit's drawing parts only where a mark carries data or a picture is the content.
4. **One copy of each live component (R4-5).** A live loop stepper is Rule 18.22's code; a reform chooser is Rule 15.20's. Complex examples reuse them, never a second copy.
5. **Generator traps.** Chapter files and plates are generator output. A word or number changes in its generator, and a second run with an empty `git diff` proves nothing crossed.
6. **One name per variable (DR-265, DR-267).** Every drawing that holds an atlas variable prints its own title.

## Who does what

| Agent | Task | Owns (writes only these) | Notes file |
|---|---|---|---|
| Data visualization lead (`oa-dataviz-systems-lead`) | Rulings first, within 20 minutes; the palette specification's content with the design director; sign-off of every round 5 item; Rule 01.9 and DR-229 after round 5 | Its notes file only; changes go to owners as requests | `work/handoffs/phase-3/20261114_Round-5-Data-Lead-Notes.md` |
| Engineer (`oa-engineer`) | Round 5 contracts within the hour: the plan file's new rows (rules 14.142 to 14.144, group 18, specimen IDs), labeled extras in the local contents, the selection guide's symbol set and link contract, the palette specification's generator from the tokens, S14's full spec in the kit; the makers' requests; the weight report | As in round 4: the kit's shared files, `phase3_ch14_build.py`, `guide_build.py`, `guide_check.js`, `dataviz_check.js`, `guide_charts.py`, `work/build/tokens/`, `work/build/scripts/phase-3/` except files named for others, the plan file's new rows | `work/handoffs/phase-3/20261114_Round-5-Engineer-Notes.md` |
| Component engineer (`oa-engineer`, second instance) | The live parts of complex examples 2 and 3 on Rule 18.22's stepper and Rule 15.20's chooser, with their keys files; the shell; any tracker interaction | `work/build/guide/code/`, the shell, the keys files it writes | `work/handoffs/phase-3/20261114_Round-5-Component-Engineer-Notes.md` |
| Selection guide maker, a general-purpose agent briefed as a senior information designer who draws reference systems | The selection guide: 127 small drawings of the forms in one style, the "Choose a chart" plate at every width, its words with the editor | `work/build/scripts/phase-3/selection_guide_build.py`, its specimen and symbol files | `work/handoffs/phase-3/20261114_Round-5-Selection-Guide-Notes.md` |
| Complex examples maker, a general-purpose agent briefed as a senior graphics editor (as round 4's makers) | Rules 14.142 to 14.144 with their plates: S14 in full (a new kit spec from S14's frozen data); the drawings of Loops B4 and R10 for the stepper; the R8 reform comparison; the entries' words with the editor | Specs and entry files the plan file names for rules 14.142 to 14.144; `work/build/scripts/phase-3/maker_c_round5_derive.py` | `work/handoffs/phase-3/20261114_Round-5-Complex-Examples-Notes.md` |
| Tracker designer, a general-purpose agent briefed as the designer who drew chapter 11's trackers and chapters 11, 12 and 15's systems plates | DR-274's renumbering pass first (R5-8), then the two new trackers, Rules 11.10 and 11.11, with their plates and group 2's line with the editor | Chapter 11's generators `apply_systems_ch11.py` and `apply_systems_ch11_ui.py` with their outputs (`11-icons.json`, `s-11-*`, `manifest-systems.json`); for R5-8 only, string edits in `stage_a_systems_ch05.py`, `stage_b_ch12_systems_build.py`, `stage_c_ch17_build.py`, `stage_c_identity_ch17.py`, `stage_c_ch19_build.py`, `civic_line_stage_b_drawings.py`, `token_table_build.py`'s inputs if they cite chapter 11, and the outputs those generators write | `work/handoffs/phase-3/20261114_Round-5-Tracker-Designer-Notes.md` |
| Systems designer, a general-purpose agent briefed as the designer who drew chapter 15 | Rules 15.22 to 15.25 with their plates; R5-8's map in its own generator | `work/build/guide/chapters/15-systems-graphics.json`; `phase3_ch15_build.py`; specimens `s-15-*`; `manifest-systems-graphics.json` | `work/handoffs/phase-3/20261114_Round-5-Systems-Designer-Notes.md` |
| Design director (`oa-design-director`) | One read of the selection guide's first drawings, the palette specification, the three complex examples and the trackers at 1440, 390 and 320 px on both grounds and in grayscale, at twice size; then one read of the fixes | Its notes file only | `work/handoffs/phase-3/20261114_Round-5-Design-Director-Notes.md` |
| Accessibility lead (`oa-ux-accessibility-lead`) | The interaction specification first: the selection guide's 127 links and their skip path, complex examples 2 and 3 on the existing components, the trackers' words; then tests as built | Its notes file only | `work/handoffs/phase-3/20261114_Round-5-Accessibility-Notes.md` |
| Editor (`oa-editor`) | The words pass on every round 5 item; group 18's line; chapter 14's and 15's intros where they name what the chapter holds; the trackers' step names and end words with the research lead | Entry files `14-001.json` to `14-014.json`, `14-chapter.json`, `phase3_ch14_rules_build.py`, the words it is handed by owners who have finished (D3-669) | `work/handoffs/phase-3/20261114_Round-5-Editor-Notes.md` |
| Research lead (`oa-research-lead`) | The workflow facts first: each of the 11 routes' stages, the gaps its November 11 and 12 file left, and the tracker steps' sources; the reconciliation table's data with where the guide applies each resolution; ED4-7; the data check | `work/research/20261111_Policy-Workflow-Sources.md` (new sections), the research ledger (Part 7, new rows), `work/build/data/` (new files and checks), the V7.1 issue list (new rows only) | `work/handoffs/phase-3/20261114_Round-5-Research-Notes.md` |

If you need a change in a file another agent owns, write it under "Requests" in your notes, addressed by name, and tell the main session in one line. Do not edit it yourself.

**Read each other's notes, so the main session relays less.** The data lead's "Rulings", the engineer's "Contracts", the accessibility lead's "Interaction specification", the research lead's "Facts for owners" and the editor's "Words for ..." sections are written for you to read directly.

## Contracts for round 5

**R5-1. The plan file is the source of numbers.** The engineer adds round 5's rows to `work/handoffs/phase-3/20261112_Chapter-14-Plan.json` before any maker draws: group 18 and its rules 14.142 to 14.144, their spec IDs and entry files, the selection guide's and palette specification's specimen IDs. Nobody renumbers.

**R5-2. The selection guide.** An extra with no `after_rule` in chapter 14, so it sits between the opener and group 1, and a line in the local contents. Its groups are the 16 family questions as the chapter prints them. Each form is a link to its entry, named in live HTML text with its tier; each picture draws from one symbol set (`<symbol>` and `<use>`), hidden from screen readers, so its link's name says the form. Avoid forms read as such in words and in their mark. Every form in the plan file appears once, checked by script.

**R5-3. The palette specification.** An extra after Rule 14.5, labeled, generated from the tokens by a script the engineer owns, so a token release rewrites it. It shows each palette's job, steps, token names and values on Newsprint, White, Charcoal and Prussian where approved, contrast against each ground, grayscale and three color-vision proofs, and the grade line code. Chapter 26's table stays the token list; this plate is how a chart uses them.

**R5-4. Three charts in full.** Each of Rules 14.142 to 14.144 is a rule with its lesson as its title, a correct plate and, where the lesson has a common misreading, a failure plate, built under chapter 14's anatomy. Example 1 is a new kit spec from S14's frozen data (the specimen is placed once; S14 stays at its entry). Examples 2 and 3 run on Rule 18.22's stepper and Rule 15.20's chooser with a still sequence for print, reduced motion and scripts off. Every atlas value is read by script from the model of October 15, 2026, with that date beside any status or route. No control offers amounts, odds, totals or loop strengths the model does not hold (Rule 15.21).

**R5-5. The workflows.** 15.22 draws the federal statute (FS) whole: stages, the paths a bill can take instead, vetoes and overrides, funding, implementation by rule, litigation, and repeal or sunset, each stage tied to its source. 15.24 sets the 11 routes as a reference set in live HTML text, each with V7's name and instrument, its stages, its official source and the date it was checked; V7's 113 undated route entries print as not checked (Rule 13.10). 15.23 maps each tracker's six steps to its workflow's stages, the new trackers included.

**R5-6. The reconciliation table (15.25).** Phase 0's 45 rows of conflicts and ambiguities and the two value conflicts, each with the model's value, the resolution and the chapter and rule where the guide applies it, and new rows for what Phase 2 drew from V7; the 2,644 rerun stated with its date. No earlier drawing is cited as evidence for a V7 value. The full table may live behind a disclosure, with its counts on the plate.

**R5-8. The chapter 11 number map (DR-274).** Old 11.10 becomes 11.12, 11.11 becomes 11.13, and so on to 11.16, which becomes 11.18; the new trackers take 11.10 (ballot measure) and 11.11 (court case). The tracker designer lists every match by script first (`11.10` to `11.16` followed by a non-digit), reads each in context so a size or a data value is never taken for a rule, writes the list under "Contracts" in its notes, then applies the map in the files it owns and sends each other owner its lines: the engineer (`guide_build.py`), the component engineer (`stage_c_ch18_build.py`, `stage_c_ch18_anatomy_build.py`, `work/build/guide/code/`), the systems designer (`phase3_ch15_build.py`). Every generator then reruns; a second run gives an empty `git diff`, a rescan finds no old number left in reader text, and the guide check proves every same-page link. The two board builders keep their numbers (D3-1878).

**R5-7. The trackers.** Six steps each, under DR-108's marks and DR-150's slash; step names and end words from the law (ballot measures: the state's constitution and election office; court cases: Title 28 and the Supreme Court's rules), shown on board 3 for Dustin's approval as DR-108's were. A stopped item ends its line on a square; a decided or certified one says so in words.

## Each task in more detail

**Data visualization lead** (first; your rulings unblock the others). Under "Rulings", within 20 minutes:
- (a) **The selection guide:** which form a question lists first (core, then extended, then reference, then avoid, as the plan's tiers), how an avoid form shows, and whether any form answers two questions (listed once, under its family).
- (b) **The palette specification's content:** which palettes, which grounds, which proofs, and the words for each job.
- (c) **Complex example 1:** which months S14 in full draws, how the preliminary months and the margin show, and its named mark (DR-239's two drops past the margin).
- (d) **Complex examples 2 and 3:** the stepping order through Variable C3 for B4 and R10; how R-06, R-30 and R-38 line up with no total, their qualifiers ("+L local", "+S delayed", "+M renter-owner", "+S sector", "+S renters") kept whole.
- (e) **15.22 to 15.25:** what the FS plate draws first, and the reconciliation table's row order.
- (f) **The trackers:** what counts as each step's evidence and each end's words.
- (g) **Rule 01.9 and DR-229 after round 5** under D3-689's test.

**Engineer.** Contracts within your first hour (R5-1 to R5-3); S14's full spec support; the extras in the local contents; the guide check's coverage of the new plates; requests in order; each build's weight report.

**Component engineer.** Complex examples 2 and 3 on the existing components under the accessibility lead's specification, with keys files the guide check walks.

**Selection guide maker.** Read the plan file's 127 rows, every entry's specimen at its entry, the coverage plan and the data lead's ruling (a). Draw each form small, in one stroke weight and the kit's inks, so a reader knows the form at a glance; the shape is the form's, not its data. Lay out the 16 questions at every width the guide gives, from 1440 to 320 px.

**Complex examples maker.** Build each example under R5-4 and the rulings, check every figure by script against its data, and look at every capture at 1440, 390, 296 and 256 px on both grounds and in grayscale.

**Tracker designer.** R5-8 first, within your first hour, so the other owners apply the map before they rerun their generators. Then the two trackers, Rules 11.10 and 11.11, each with a correct and a failure plate and the extras chapter 11's trackers carry where they need them: three invented items labeled Illustrative per plate in different states, step names and end words from the research lead's sources, on chapter 11's marks. Group 2's title and line take in the new trackers with the editor's words. Report to the systems designer when the trackers land, since 15.23 maps them.

**Systems designer.** Start with 15.22, 15.24 and 15.25, which need no tracker; 15.23 after the tracker designer reports. Rules 15.22 to 15.25 on chapter 15's stage (true 296 px drawings, the 680 px composition and the 328 px column). Apply R5-8's map in `phase3_ch15_build.py` when the tracker designer posts it.

**Design director.** One read as drafts land, one read of the fixes. Hierarchy, rhythm, type on the scale, alignment, white space and what a reader sees first, on both grounds and in grayscale. The selection guide is the chapter's front door: it should read as one calm system at a glance.

**Accessibility lead.** Your "Interaction specification" within your first hour; then tests at 1440, 1024, 390 and 320 px with the keyboard alone and the accessibility tree. Report what you tested and what you could not (no screen reader runs here).

**Editor.** The words pass as items land; group 18's line and title; the selection guide's and palette specification's labels and captions; the trackers' words with the research lead. Word passes never touch mark or ink keys.

**Research lead.** "Facts for owners" first: for each of the 11 routes, its stages with sources and dates, and the gaps closed or named; the ballot measure and court case steps' sources; the reconciliation rows with their model values. Then ED4-7, the data check, and any V7.1 item as a proposed row for board 3. Keys: Congress.gov only (DR-272). When you first need it, tell the main session; it opens the secure form on this environment, and once the key is saved the proxy sends it for you (set any key variable to `proxy-injected`). Never print or store a key.

## Who works when

1. On Dustin's go: the data lead (rulings first), the engineer (contracts first), the accessibility lead (its specification first), the research lead (facts first), the editor (group 18's line, then words as items land).
2. At once, beside them: the tracker designer (R5-8's list and map first), the systems designer (15.22, 15.24 and 15.25 first).
3. When the contracts and rulings land: the selection guide maker, the complex examples maker and the component engineer draw.
4. When the trackers land: the systems designer builds 15.23.
5. When the first drafts land: the design director reads them.
6. When each owner finishes: it rebuilds what it owns, runs its checks and reports.
7. When all report: the main session runs the strict build, the kit's `build --all`, the V7 check, the data check and the quick guide check with photographs; commits; republishes the chapters page privately as version 11; writes handoff V26 for the review chat.

## Checks every owner runs before reporting

- Makers: `node work/build/chart-kit/oa-chart.mjs build sNN --out <scratch>/kit-out` for every spec touched, sweep on; captures at 1440, 390, 296 and 256 px looked at; `python3 -I work/build/scripts/phase-3/phase3_ch14_build.py`; a strict build of your own to scratch.
- Tracker designer and systems designer: the generators you own with their checks, a second run with a clean `git diff`, a strict build, captures at 1440, 1024, 768, 390 and 360 px on both grounds.
- Engineer: the kit's self-test and `build --all --no-png`, `guide_build.py --self-test`, the guide check's self-test where it changes, a strict build.
- Research lead: the data check over the folder; the V7 check over chapter 15.
- Accessibility lead, design director and data lead: each names what it looked at, at which widths.
- Load: no more than two agents drive a browser at once; wait for `uptime` under 4 before a browser run; run the guide check with `--no-captures` unless the photographs are what you need; never count a crashed check as run.

## Notes and limits for every agent

- Write your notes file with sections: "Status" at the top, kept current; "Summary"; "Contracts" (engineer), "Rulings" (data lead), "Interaction specification" (accessibility lead), "Facts for owners" (research lead); "Routine calls" as `- D3-xxx | decision | reason` lines; "Requests" (addressed by owner); "Tested" and "Not tested". The main session numbers and logs the calls. Write your notes early, since the container can restart.
- Never touch `source/` or `deliverables/`. Never edit Atlas V7 or `work/research/atlas-v7-docs/`. Never touch `work/ledger/`, any board or progress page. Do not commit, push or publish. Never run `git checkout --`, `git stash`, `git reset` or any command that discards changes.
- Scratch work and every capture you do not deliver go to `/tmp/claude-0/-home-user-Dustin-s-Command-Center/7633c399-b692-5041-be92-a87ecd098fbf/scratchpad/phase-3/round-5/<your-role>/` by absolute path. Set `TMPDIR` to it. Check `git status` for stray files you made.
- Read `date -u` before you write a time.
- Python reading supplied or downloaded files runs with `-I`. Downloads go into their own new folder.
- Every number outside the atlas carries its source, period and qualification, or the item carries "Illustrative" beside it.
- File names follow `CLAUDE.md`: `YYYYMMDD_Title-Case.ext` with 20261114, lowercase kebab-case folders; source code and data keep their conventions.
- No em dashes, no U+2011, no disclosure line, no decision codes or studio words in reader text, curly apostrophes.
- Report what you tested and what you did not as separate lists. Never describe a check you did not run.
- Your final message to the main session: a summary of under 200 words, the paths you wrote, and anything blocking.
