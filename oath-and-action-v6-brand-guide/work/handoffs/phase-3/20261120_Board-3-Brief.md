# Brief: board 3, after Phase 3's rounds 4 and 5 and chapter 15

Written November 20, 2026, by the main session of chat 8. Dustin's go covers this build (DR-290). Board 3 is the last board before Gate 3. It asks Dustin for the decisions that rounds 4 and 5, chapter 15 and the review left for him, and shows the work they rest on at true size. Board 2 is the model: its brief (`work/handoffs/phase-3/20261113_Board-2-Brief.md`), its decision file (`20261113_Board-2-Decisions.json`), and the page as published (https://claude.ai/artifact/AyKqXMpc5Ao68NuZ7wL2m2). Keep its look.

The board reads the final build of chat 8: the strict build after DR-191's second pass, published as the chapters page's version 13 (DR-289). The main session tells the builder its path when it lands; until then, prove the method on the V12 page (`work/boards/phase-3/review-4-5/20261116_Guide-Preview-V12.html`). "Before" pictures of changed approved work come from the V11 page (`work/boards/phase-3/round-5/20261114_Guide-Preview-V11.html`), the state before chat 7's fix pass.

## What the board holds, in this order

1. **Cover.** Kicker "Edition 06 · Phase 3 · Board 3", a title, "For Dustin Cathcart" with the build date, a deck of two or three sentences, the panel list, and how long the decisions take to read.
2. **What you decide** (panel 1). Each item opens with its answer in a sentence or two and the studio's recommendation, then the pictures it needs.
   - **The two new trackers' step names.** Rule 11.10's ballot measure and Rule 11.11's court case, six steps each, twelve names in all, for Dustin's approval as DR-108 approved the bill's. Each tracker's correct plate at 1440 and 390 px, its step table, and the marks it uses.
   - **Changed approved work.** Every item the change ledger lists for board 3 (rows C-108 to C-134 carrying "listed for board 3" or "board 3 shows"), found by script, plus anything the second pass changes on approved work. Among them: S14's source line and its two label keys; the masthead's measured room and focus offsets; the "Where to start" links at 320 px with 200 percent text; chapter 26's token table selector; chapter 18's form script and the chooser's list form; the words inside image stages (95 hidden, 321 open, no visual change); the bill's step table; Rules 14.1 to 14.14; Rule 14.144's pips (ruling (d)'s "no pips" replaced, D3-2127); Rule 15.20's chooser (D3-2140); Rule 11's renumbering (C-118). Each with V11's picture beside the final build's at true size where it shows, or one line saying it does not show. One approval for the lot.
   - **Held for Dustin.** Every row of the deferred fixes register under "Held for Dustin (board 3)" (`work/ledger/20261116_Deferred-Fixes-Register.md`, 17 rows), and Q-12 (trademark clearance), each with what it changes, why it waits on him, the recommendation, and the pictures a choice needs (for example S59's "4.1" label before and after, the masthead at 360 to 375 px with each wordmark master, the red targets with and without the keyline, CE-S22's sharper question words, NB-S4's lockmark on a kit chart). Any second pass item flagged for him joins this list.
   - **The proposed atlas V7.1 row**, `routes[].who` (the research lead's round 4 notes; D3-1861), with the counts and a recommendation.
   - One reply line: "To answer, reply “As recommended”, or name the item and your change."
3. **Round 4's 13 forms**, by family in the plan file's order (`work/handoffs/phase-3/20261112_Chapter-14-Plan.json`), shown as board 2 showed its forms: rule number, form name, tier, reader question, a link to the live entry in the chapters page (version 13); desk and phone drawings side by side on Newsprint and on Charcoal at true size; the grayscale proof; the page table as live text in a fold with its caption; the source line as printed; bytes with the plate frame.
4. **Round 5.** The selection guide ("Choose a chart") at 1440 and 390 px, with its counts read from the check (127 form links, 6 road links, 16 questions); the palette specification; the three charts in full, Rules 14.142 to 14.144, each at 1440 and 390 px with its failure plate, and the stepper's and chooser's states as a reader moves through them.
5. **Chapter 15 whole.** Rules 15.1 to 15.25, each rule's title with its correct and failure plates at 1440 px, phone views of the plates a phone reader uses most, and the reconciliation table (Rule 15.25) with its resolutions and any new V7.1 items, which Gate 3 decides.
6. **Chapter 14's spend.** From the final strict build report: chapter 14 with the kit against its 2,803,941-byte figure, reported under DR-271; the kit; the heaviest plates; round 5's plates; the page projection against 15.5 MB and the 16 MB limit.
7. **The Rule 01.9 count.** Chapter 14's examples by atlas domain and by state against one in four and one in five, recounted by script for the finished chapter (`board_2_data_lead_counts.py` is the model), and DR-229's election-data count.
8. **Scores.** The nine readers of the review of rounds 4 and 5 with their Must and Should counts, read from the reports; the creative director's first pass, rescore and second pass rescore; the creative director's score of this board when it lands.
9. **Tested and Not tested**, kept apart, each figure read from its file: the strict build, the four-width check and the quick check with photographs (DR-288), the kit's `build --all --no-png`, the data check, the V7 check. Safari, Firefox, real screen readers and DR-213's four device scripts stay not tested (DR-279).
10. **Next.** One or two sentences: the Gate 3 report, with the Phase 4 proposal.

## How the page is built

- Copy `work/build/scripts/phase-3/board_2_build.py` and `board_2_render.js` to `board_3_build.py` and `board_3_render.js`; leave every earlier builder and page untouched. One script reads every number, word and picture from files at build time; a content file holds only the board's own words and the files it reads. Options as before: `--reuse`, `--check`, `--strict`, `--scratch`, `--out`.
- Outputs in `work/boards/phase-3/review-4-5/board-3/`: `20261120_Board-3.html`, `20261120_Board-3-Content.json`, `20261120_Board-3-Figures.json`, `20261120_Board-3-Check-Results.json`, and `img/` with composed pictures only. Raw captures stay in scratch.
- The page: one HTML file with no scripts and no `<!doctype>`, `<html>`, `<head>` or `<body>` tags, `<title>Edition 06 Board 3</title>` and `<meta name="claude:viewport-fit-sides" content="cover">` first, then one `<style>`, as board 2's. Tables are live text; folds are `<details>`. Every `<img>` carries `loading="lazy"`, its width and height, and alt text that says what it shows. No sideways page scroll at 390 px; a picture wider than the column scrolls in its own named frame. Outside requests only to Google Fonts. The page under 16 MB.
- Publishing limits: at most 511 files and 256 MB in all, each image under 15 MB, published in batches of at most 255 files and 64 MB. Aim for about 250 pictures and under 60 MB, so one publish carries it if it can; say the totals in your notes.
- Captures of the 12 MB page are slow (1 to 36 seconds an element). Capture only what the board shows, in priority order, and reuse captures between runs.
- Check with `node work/build/scripts/phase-2/dataviz_check.js <page> --board --no-captures` from `work/build`, on the page and on a copy wrapped as the host wraps it (`--check` does both), and report the result.

## The decision file

The data lead writes `work/handoffs/phase-3/20261120_Board-3-Decisions.json` in board 2's schema: the items of panel 1 (each with `id`, `title`, `what_changed`, `why`, `recommendation`, `refs`, and the pictures or file paths it needs), the changed approved work found by script, the held rows, the V7.1 row, and the Rule 01.9 and DR-229 counts with the script that made them. The builder reads it; the editor owns its words once the data lead has written them. Agree any schema change in your notes in the first 20 minutes.

## Who does what

| Owner | Role file | Notes file in `work/handoffs/phase-3/` | Work |
|---|---|---|---|
| Data visualization lead | `oa-dataviz-systems-lead.md` | `20261120_Board-3-Data-Lead-Notes.md` | The decision file; the Rule 01.9 and DR-229 recount; signs off every figure the board prints |
| Research lead | `oa-research-lead.md` | `20261120_Board-3-Research-Notes.md` | The facts behind the V7.1 row and Q-12; checks every source line, date and figure the board prints against its sidecar and the research ledger |
| Editor | `oa-editor.md` | `20261120_Board-3-Editor-Notes.md` | Every word on the board, in the content file and the decision file, once the builder's first full build lands; the twelve step names as the trackers print them |
| Board builder | `oa-design-director.md` as page builder | `20261120_Board-3-Builder-Notes.md` | The script, the content file and the page; reruns as owners land |
| Creative director | `oa-creative-director.md` | `20261120_CD-Review-Of-Board-3.md` and `20261120_Board-3-CD-Scores.json` | Scores the board on the six criteria once its full build lands; the main session starts it |

Owners read each other's notes directly: the data lead's "Rulings" and "Sign-off", the editor's "Words for". Write calls as `- D3-xxx | decision | reason` lines under "Calls", with "Tested" and "Not tested" sections and a "Status" line at the top of each notes file.

## Order

1. The data lead, research lead and builder start together; the builder proves its script on the V12 page while the decision file lands.
2. When the main session's final build and version 13 land, the builder reruns on it with `--reuse --check`.
3. The editor reads the board; the creative director scores it; one fix round; the builder's final run with `--check --strict`.
4. The main session reads every file, reads panel 1 against Dustin's "settled and not to be changed" list, and publishes the board privately.

## Limits

- **Load.** At most two browsers at once: run `bash /tmp/claude-0/-home-user-Dustin-s-Command-Center/318bf243-c48f-583b-8dd6-5600224b4263/scratchpad/c08/browsers.sh` first and open one only when it prints "OK to open one" (read its words, never its exit status). Never run the guide check; the main session runs it.
- **Clock.** Read `date -u` before you write a time.
- **Ownership.** Write only the files your row names, your notes and your own scratch folder. Never touch `source/`, `deliverables/`, `work/ledger/`, any earlier board or progress page, any generator, chapter, spec or kit file, or another owner's files. The board changes nothing in the guide. Do not commit, push or publish.
- **Scratch.** `/tmp/claude-0/-home-user-Dustin-s-Command-Center/318bf243-c48f-583b-8dd6-5600224b4263/scratchpad/c08/board-3/<your-role>/` by absolute path; set `TMPDIR` to it. Run Playwright and node scripts with absolute output paths, and check `git status` for stray files you made.
- **Keys.** Never print or save a key. Python that reads supplied or downloaded files runs with `-I`.
- **Words.** Chapter 02's rules (`work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`): plain, spoken prose, no em dashes, no studio words a reader would not know on the board's face; decision codes and file paths only in small reference lines.
- **Nonpartisan.** One standard of evidence for everyone (DR-93); read every recommendation and every line about a party from the left and from the right (DR-124). Never manufacture balance.
- **Settled work.** No recommendation may change a settled element: the Civic Line icons (DR-144 and the approved redraws), Reforms R-01 and R-02 like every other reform (DR-223), the atlas visual system (DR-36), the chart system (DR-52 to DR-61), the coverage plan and build order (DR-62, DR-63), the chart rules of DR-64 with DR-255's one exception, chapter 02's writing rules (DR-73 to DR-83), and every answer Dustin has given from DR-95 on.
- **Restarts.** Write your notes early and add to them as you go.
- Final message to the main session: under 150 words, your state, what landed, check results, and anything blocking.
