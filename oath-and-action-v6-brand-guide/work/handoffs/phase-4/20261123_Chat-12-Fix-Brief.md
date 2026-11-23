# Chat 12 fix brief: chapters 16, 20 and 21 after the review

Written November 23, 2026 by the main session, from six reports of chat 12's review (the engineer's weight measurements follow as an addendum). Phase 4 is active (Gate 3); Dustin approved this pass as handoff V33 sets it (DR-326): one fix pass, then DR-191's short second pass and the creative director's rescore. Every path is relative to the project folder `oath-and-action-v6-brand-guide/`. Calls continue from D4-309.

## 1. Read first, every owner

1. Your role file in `.claude/agents/`, `CLAUDE.md`, and chapter 02's writing rules, `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`.
2. The review brief, `work/handoffs/phase-4/20261123_Chat-12-Review-Brief.md`, sections 1, 3 and 6 (what was reviewed, the settled list, how to look).
3. The reports, for every code this brief gives you. Each finding there says where, what is wrong, the fix and why; this brief only assigns it. Read the code in its report before you act on it:

| Codes | Report in `work/handoffs/phase-4/` |
|---|---|
| ST, NB | `20261123_Chat-12-Review-Evidence-Balance.md` |
| AX | `20261123_Chat-12-Review-Accessibility.md` |
| CE, DF, RP | `20261123_Chat-12-Review-Words-Readers.md` |
| CR, BR | `20261123_Chat-12-Review-Craft-Brand.md` |
| PR | `20261123_Chat-12-Review-Production.md` (the producer's files in `chat-12-production-test/`) |
| CD-M, CD-S | `20261123_Chat-12-CD-Review.md` and `20261123_Chat-12-CD-Scores.json` |

4. The decision log from "## Chat 11c" to the end of `work/ledger/20261020_Decision-Log.md` (line 7590 on). Never read the whole log.

## 2. What the review settled

- **The wall test passed (DR-315).** ED-F1 closes and Rule 15.25's resolution stands. No layer color.
- **C11C-TB closes.** The atlas's Charcoal title bar stays in both themes (the accessibility reader and the creative director agree).
- **F-8 and F-14 close.** UX-4 (AX-2) and F-15 (AX-1) stay open until this pass fixes them.
- **Apostrophes in stored text (CR-4, DF1).** Chapter 21 prints the atlas's stored apostrophes as typographic ones, as approved chapter 15 already does for the same stored titles; the stored words stay as stored (DR-37). The main session logs this as a routine call; board 1 reports it.
- **Settled and not to be changed:** as in the review brief's section 3. A fix that would change an approved chapter (01 to 15, 17 to 19, 26, the chart kit, chapter 18's code set) is not made; it goes to board 1. The items already held for Dustin: DD10-NF1 (ampersand B as text; locked identity), E11b-1 and E11b-2 (chapter 18), C11C-R14d (chapter 15's red target case), Rule 15.16's confidence sentence, Rule 01.16 and 13.2's "same length", S66's source line, "dashed means two things" (Rule 13.4).

## 3. Owners and their items

One writer per file. A need in another owner's file goes in your notes under "Requests" (file, key, what to do); the main session relays.

### 3.1 Engineer W (web kit, shared kit code, guide build and check): resumed from the weight job
Files: `work/build/app-kit/oa-app.mjs`, `renderers/web-site.mjs`, `renderers/site-parts.mjs`, every other renderer except `atlas-page.mjs`, `tools/` except `atlas_figures.py` and `atlas_test.py`, specs `a01` to `a10`; `work/build/scripts/phase-2/guide_build.py`, `guide_check.js`; `work/build/scripts/phase-3/guide_charts.py`.
1. **PR-M1 first.** Scope every kit style the page's head carries to its frames, so no kit rule reaches a guide plate. Prove Rules 14.143 and 15.15's plates draw as they did before chapter 20 joined (pixel comparison at 1440 and 390 px, both themes, against version 15's committed page, `work/boards/phase-4/chat-10/20261121_Guide-Preview-V15.html` (built before chapter 20 joined)), and that every kit frame is unchanged. Add a guide check plant for a head rule that reaches a non-kit element.
2. **CD-M1 and CR-1** (the dropped spaces), **CR-13** (IDs and addresses break at hyphens; CD-S11's docket address), **CR-15**, **CR-16**, **PR-S8**, and CD-S6 if the chip is drawn in `site-parts.mjs`.
3. **PR-M2's web half:** an article page's words may come from its own content file, the generator's fill kept as the fallback; and **PR-S1, PR-S2, PR-S3, PR-S5, PR-S6.**
4. **CD-S8:** chapter 16's files (a placeholder template at five ratios, a sample WebVTT file, the shot list and rights row as CSV) as kit exports if each takes under 20 minutes; else write a register row naming the chapter or phase that holds it.
5. **PR-S7:** measure only, for board 1.
Run order after a change to A01 to A10: `phase4_ch20_build.py` (run, never edit), `node work/build/app-kit/oa-app.mjs build A04 A05 A06 A07 A08 A09 A10 --date 20261121`, `phase4_ch20_build.py` again, then the strict build.

### 3.2 Engineer A (the atlas kit): new
Files: `work/build/app-kit/renderers/atlas-page.mjs`, `tools/atlas_figures.py`, `tools/atlas_test.py`, specs `a11` to `a20`, `plates/atlas-page.css` and the atlas plates. Read your own chat 11c predecessor's notes (`20261122_Chat-11c-Engineer-Notes.md`) and the data lead's rulings (chat 11c, and this chat's as they land).
1. **The Musts:** AX-1, AX-2, AX-3, AX-4 with CD-M2 (each question its own answer, or words that say the atlas holds none; the page loads with no question pressed; the plates keep the pressed state), AX-10, ST-1 (the confidence line and Rule 15.20's disclosure under each panel; extend T7), CE1 (every chip followed by its record's name, with the data lead's ruling on which name; extend T1), RP1 (labels on the two readings, the editor's words), CR-3 (no word alone on a line in the drawing, the tables or the phone layouts).
2. **The Shoulds:** AX-5, AX-6, AX-8, AX-9, CE8, CR-5 to CR-10, CR-21, CD-S1 (with the design director's spec), CD-S2 and CD-S3 (crops drawn at true size from their part), CD-S6 if the chip is drawn here, CD-S10, PR-S4, PR-S9, PR-S10, and DF1's apostrophes at render (section 2).
3. **PR-M2's atlas half, bounded:** a page's words may come from its content file; the reform template names every target, not only variables, and says in words when its drawing does not apply. Run the atlas test over every reform in the model and report how many draw cleanly. If the template's other shapes take more than about 60 minutes, land the two parts above and write the rest as a register row.
Run order after a change: `phase4_ch21_build.py` (run, never edit), `node work/build/app-kit/oa-app.mjs build A11 A12 A13 A14 A15 A16 A17 A18 A19 A20 --date 20261122`, `phase4_ch21_build.py` again, then the strict build. The atlas test and its self-test pass on your last build, and axe reads 0 on the six working pages.

### 3.3 Design director: new
Files, in two turns (3.6): `work/build/scripts/phase-4/phase4_ch16_build.py`, `phase4_ch20_build.py` and `phase4_ch21_build.py` outside their word fields, with their outputs; `work/handoffs/phase-4/20261121_Web-Page-Specs.md` and `20261122_Atlas-View-Specs.md`. Read the chat 11c design director's notes first.
- Turn 1, chapters 16 and 20: CR-2, CR-17, CR-20 with CD-S9 (ED11-3's footers; place chapter 20's opener caption), CR-22, CE2 (Rule 20.9's correct plate: the measure and drawing), CD-S7 (S04 drawn by the chart kit in chapter 16's vertical and storyboard frames; the data lead signs it off), and AX-7 for chapters 16 and 20.
- Turn 2, chapter 21: CR-11, CR-12, CR-14, CR-18, CR-19, CD-S1 (the spec), CD-S2, CD-S3, CD-S4 (the opener as the home's first screens), AX-7 for chapter 21, and **C11C-SP** (confirm or change A14's phone spacing).
- Specs for the engineers go in the two specs files and your notes' "Contracts"; layout calls in the kit are theirs to build.

### 3.4 Editor: new
Files, in two turns (3.6): the word fields of the same three generators (every word a reader sees, page words included through `--page-words`); words the kit types (frame names and alts) go to the engineers under "Words for". Read the chat 11c editor's notes first.
- Turn 1, chapter 21: CE1's names (with the data lead's ruling), CE6, CE7, CE8, CE9, CE12, CE15 (chapter 21's share), RP1's labels, RP2 (one sentence on why these four views, read from the left and the right), RP3, RP4, ST-1's line, ST-2, DF1, DF2, DF6, DF7, DF8, DF10, CD-S5, and the words AX-1 to AX-4 need.
- Turn 2, chapters 16 and 20: NB-1 (the record's two reasons, its safety finding, and the 2022 context, with Rule 20.8's "concerns"), NB-2, NB-3, ST-3, ST-4, CE3, CE4, CE5, CE10, CE11, CE13, CE14, CE15 (chapters 16 and 20), CE16, DF3, DF4, DF5 (words for the engineers), DF9, CD-S11's words, PR-S11.

### 3.5 Data visualization lead: new
Files: your notes; scripts in your scratch. Read your chat 11c predecessor's rulings R1 to R18 first.
1. **Rulings within 20 minutes**, under "Rulings": what each home question's answer is in the model, or that it holds none (CD-M2, AX-4); the confidence line's form on the loop page (ST-1, R12); which stored name follows each chip (CE1); the labels for R-23's two readings (RP1); RP4's two names for one part; DF2's "flow"; DF6's sheet naming; ST-2's loops column; DD11C-Q1, the locator's fill.
2. **Sign off every changed atlas view and chart** as it lands, at 1440 and 390 px, light and dark, in numbered batches; S04 in chapter 16 (CD-S7).

### 3.6 Turns on the three generators
- Turn 1: the editor holds `phase4_ch21_build.py`; the design director holds `phase4_ch16_build.py` and `phase4_ch20_build.py`.
- Each ends its turn by writing "Turn 1 done, HH:MM UTC" (from `date -u`) in its notes and handing back a summary. The main session then resumes each with turn 2, the files swapped.
- The engineers may run a generator (never edit it) after a kit build, under the lock.

### 3.7 Accessibility lead: resumed
1. **Chapter 19's six entries:** make the change you set out, in `work/build/scripts/phase-2/stage_c_ch19_build.py` and its outputs, with its `--check` current.
2. Then recheck your Musts as the engineers land them (the second pass starts there).

### 3.8 Main session
NB-1's correction of `work/research/20261121_Act-Page-Docket.md`; atlas V7.1 issue rows for Connection L14's citation (ST's item for Dustin) and Loop R18's "other party's instances" (the words reader's item 3); the recapture of the three plates that drew S86 black; the register; the closing checks.

## 4. Shared rules

- **Scratch:** `/tmp/claude-0/-home-user-Dustin-s-Command-Center/6f635cd3-ba95-5230-9089-d140c7cc1cf8/scratchpad/c12/fix/<your-role>/`, by absolute path.
- **Lock:** wrap every generator run, kit build and page build in `flock /tmp/claude-0/-home-user-Dustin-s-Command-Center/6f635cd3-ba95-5230-9089-d140c7cc1cf8/scratchpad/c12/build.lock <command>`.
- **Strict build:** `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <your scratch>/guide.html`: exit 0, 0 warnings, 0 stale plates.
- **Browsers:** run `bash /tmp/claude-0/-home-user-Dustin-s-Command-Center/6f635cd3-ba95-5230-9089-d140c7cc1cf8/scratchpad/c12/browsers.sh` first and open one only on "OK to open one". Close it after each batch. Never run the guide check; the main session runs it.
- **Generators:** chapter files, specimens, keys files and plates are generator output. Change the generator or its data, run it, and prove with `git diff --stat` that only the intended files moved.
- **Times** only from `date -u` read in the same command. **Git:** never commit, push, stash or run `git checkout --`; the main session commits. Check `git status` for stray files you made.
- **Bytes:** report each chapter's bytes before and after. Nothing is cut to meet a figure (DR-271).
- **Notes:** `work/handoffs/phase-4/20261123_Chat-12-<Role>-Notes.md` (Engineer, Engineer-Atlas, Design-Director, Editor, Dataviz-Lead, Accessibility-Lead), with "Routine calls" (`- D4-xxx | decision | reason`), "Rulings", "Contracts" or "Words for" where you have them, "Done" (each code with what changed), "Requests", "Not fixed" (rows `| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |`), "Tested" and "Not tested". Every code assigned to you ends in "Done" or "Not fixed". Never describe a check you did not run.
- **Hand back** a summary of no more than 15 lines.
