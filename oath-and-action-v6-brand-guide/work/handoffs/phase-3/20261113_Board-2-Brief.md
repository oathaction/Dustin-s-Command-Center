# Brief: board 2, after Phase 3's rounds 1 to 3

Oath & Action Edition 06, Phase 3, November 13, 2026. Written by the main session for board 2's owners. Paths are relative to `oath-and-action-v6-brand-guide/`. The studio's calls continue from D3-1538; Dustin's answers for this board are DR-254 to DR-260 in `work/ledger/20261020_Decision-Log.md` (read them first).

## Where things stand

Rounds 1 to 3 built chapter 14's forms in 14 families (rule 14.15 to 14.124, less round 4's rows). Round 3 is reviewed, fixed, second-passed and rescored: the creative director scores all five items 4 or more on every criterion and calls round 3 ready for board 2 (`work/handoffs/phase-3/20261113_Round-3-CD-Rescores.json`). This chat's strict build of the committed state passed (D3-1536: exit 0, 0 warnings, 11,235,128 bytes, 344 rules, 638 specimens) and the quick guide check passed (D3-1537: 694 specimens, 3,296 same-page links, 0 failures).

Board 2 is set by Gate 2's section 9 (`work/ledger/20261111_Gate-2-Report.md`) and DR-252: **the 114 forms of rounds 1 to 3 at true size by family, each with its phone drawing, grayscale proof, table and source line; the Rule 01.9 count; chapter 14's spend so far.** Dustin decides there any form whose tier or data changed and any atlas V7.1 item. Handoff V23 (`work/handoffs/phase-3/20261113_Next-Session-Handoff_V23.md`, section 1 "For board 2") lists what the board must carry.

Dustin answered V23's five questions before the board (DR-254 to DR-258), so the board shows those as done, each with its old version beside it, and asks only what is still open.

## Part A: apply Dustin's answers first

These land before the board's pictures are taken. The data lead signs off each change before the engineer's chain and checks run.

| # | Answer | Work | Owner |
|---|---|---|---|
| A1 | DR-254: each chart's full data is one CSV in Phase 5's asset package; notes name it through `{data_file}` | Rewrite the nine promises (captions of S69, S70, S72, S73; notes S73 note 3, S74 note 4, S81 note 3, S83 note 3; entry 14.120's rule text) to name the file through `{data_file}`, never opening a sentence with it (D3-1529). Confirm by script that no reader text in chapter 14 still says "download" or "CSV file" | Editor; engineer confirms `words.json`'s phrase and the export check |
| A2 | DR-255: sketch 14.124's misleading half in literal red and blue | Draw the misleading half in a plain news red and blue that are none of the guide's inks (not Pillar Red, not Prussian, not any `oa.color.*` value), under its do-not-publish bar, with the colors also named in the key so the lesson holds in grayscale; the better half stays as signed off. The caption (`sketch_alt`) and first `<desc>` drop "Drawn here in gray" and name the colors. Keep the file within R3-9's 4,096 bytes. Keep a copy of today's gray file in scratch for the board's "before" picture | Cartographer (drawing), editor (caption words) |
| A3 | DR-255's exception | If any guide or kit check fails or warns on the new red and blue, give that one half a named exemption in the check, as the failure plates have, and change nothing else in the check; record DR-64's one exception in the check's comment | Engineer |
| A4 | DR-256: S16's range words | Note 3: "Range: Arkansas 52.8% (±2.7), lowest by more than the margin of error; DC 79.5% (±3.3), highest, within the margin of error of Minnesota’s 75.9% and Oregon’s 75.3%." The alt's last sentence: "Arkansas, at 52.8 percent, sits lowest by more than its margin of error; DC, at 79.5, is highest but within the margin of Minnesota and Oregon." The editor holds the draft (D3-1486). Every figure checked by script against S16's data | Editor; cartographer checks S16's layout at every width the sweep runs |
| A5 | DR-257: the 21 older atlas source lines that print October 15, 2026 twice | Find them by script on the built page (every chart whose grade line and source line both print the date). Apply round 3's rule (D3-1327, D3-1485, D3-1493): the snapshot date prints once. Where the source line comes from an atlas sidecar, the research lead adds a `snapshot_once` source variant as it did for S68 (D3-1413) and the editor sets each spec to it. List every specimen changed, with its old and new line, in the editor's notes | Research lead (variants), editor (specs) |
| A6 | Chain and checks | After the data lead's sign-off of A1 to A5: `phase3_ch14_build.py` and `--check`; `oa-chart.mjs build --all --no-png` with the sweep (84 of 84 PASS, 0 faults); the data check; `geo_build.py --check`; the V7 check; the kit self-test; a strict build to scratch. Report the share per plate and the projection after | Engineer |

The data lead also confirms that A2 to A5 change no figure, and that A5 changes words only.

## Part B: board 2

### What the board holds, in this order

1. **Cover.** Kicker "Edition 06 · Phase 3 · Board 2", a title, "For Dustin Cathcart" with the build date, a deck of two or three sentences, the panel list, and a line on how long the decisions take to read.
2. **What you decide** (panel 1). Each item opens with its answer in a sentence or two and the studio's recommendation, then the pictures it needs:
   - **Board 1 drawings that changed.** S12: the 1024 px stage that scrolls (now breaking out over the rail from 80em) beside the stacked tile the creative director asked to see (code and figure on two lines per tile), both at a 1440 px window and at 1024 px; the data lead writes the recommendation and the creative director's view goes beside it. S16: the 2024 outlines, coast edge, Alaska and Hawaii framed, DC's leader, phone codes, credit line and DR-256's range words, board 1's picture beside today's. S10's dashed total line. The placement-only moves (D3-904, D3-909, D3-911) and the 12 round 1 specs whose note words changed (D3-914) as a list. One approval for the lot.
   - **Forms whose tier or data changed.** By script against the coverage plan (`work/handoffs/phase-2/20261106_Data-Viz-Coverage-Plan.md`) and the round 1, 2 and 3 data plans, the data lead lists every form whose tier changed (the main session found none; confirm) and every specimen whose dataset, measure or derivation changed from what its plan row said: at least S73 (every designated joint fundraising committee, seven funds, with the July 21, 2024 split), S76 (transfers net candidate by candidate), S78 (its phone drawing on the tile grid; fixed broadband) and S80 (the Detroit inset), and any others the data plans' changes made (round 3's twelve changes, rounds 1 and 2's). One line each on what changed and why, and one approval.
   - **Atlas V7.1 items.** Every item carried for board 2, each with a one-line recommendation: Q-18 (CMS's 22,914,537 renewals ended against I062's KFF figure); RL-3 (the FEC's joint fundraising aggregate mixes lines 22, 28C and 21B); Variable D6's kind (D3-261); Medicaid renewals (D3-260); R-01's measures; maker A's A15 atlas strings and the Article V wording; headline figure 5 storing figure 4's qualification (D3-668); three issue titles that state an effect, with a reread of the atlas's headings (D3-908); figure 7's qualification calling H.R. 7008 "a ban" (D3-908); and the one question whether every variable's loop chain label gives way to its own title (D1, D2, D4, D6, E1, B4, B2; chapters 10, 11 and 15 together, D3-912), which is a question for Dustin and gets its own recommendation. The V7.1 list Dustin approved under Q-07 is `work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md`; say which items are new to it.
   - **Answered before the board** (DR-254 to DR-258), each shown done with its old version beside it: the data file phrase (old and new words of the nine places); sketch 14.124 gray before, red and blue now, at true size; S16's range words before and after; the specimens whose source lines changed under DR-257, old and new; the 668 comparisons (DR-258), with what was uploaded and rerun by the board's build.
   - One reply line: "To answer, reply “As recommended”, or name the item and your change."
3. **The 114 forms by family**, in the plan file's order (`work/handoffs/phase-3/20261112_Chapter-14-Plan.json`, rounds 1 to 3: 86 rows with a spec, 84 specs, and 28 sketches). For each form: rule number, form name, tier, round, maker, its reader question, and a link to its live entry in the guide preview (version 9, `https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF#<anchor>`, as board C's builder links rules, `work/build/scripts/phase-2/stage_c_board_c_build.py` `rule_href`). For a form with a specimen: the title and evidence label as printed; the desk and phone drawings side by side on Newsprint (a 1440 px window and a 390 px window, as the guide draws them, at true size); the same on Charcoal; the grayscale proof of both grounds; the page table as live HTML text in a fold, with its caption; the source line as printed; bytes with the plate frame. A form a board 1 specimen serves says so and whether its drawing changed since board 1. For a sketch form: the sketch at true size with its heading and caption as the guide prints them; the avoid pairs marked and first in their family. Mark the Estimate charts as the guide labels them.
4. **Rules 14.1 to 14.14 and the opener**, as rounds 1 to 3 left them: each rule's title with its correct and failure plates photographed at 1440 px, and the opener.
5. **The Rule 01.9 count.** Chapter 14's examples by atlas domain and by state, against one in four and one in five, recounted by script (the data lead's ruling (g) holds at 108; say what the recount gives), and DR-229's election-data count under D3-689's test.
6. **Chapter 14's spend.** From this chat's final strict build report: chapter 14 with the kit against its 2,803,941-byte stop; the kit, map geometry (against its 250,000 reserve, with the unspent bytes held), rules with the opener; bytes by family; the heaviest plates; the share per plate for round 4's 13 specimens; the page projection against 15.5 MB.
7. **Scores.** The creative director's first scores and rescores for rounds 1, 2 and 3 (`*Round-1-CD-*`, `*Round-2-CD-*`, `*Round-3-CD-*` in `work/handoffs/phase-3/`), each red team's first and second scores with Must fix and Should fix counts, read from the reports' own findings, and the creative director's score of this board when it lands.
8. **Tested and Not tested**, kept apart, each figure read from its file: the strict build, the quick guide check, the kit's `build --all`, the data check, the sweep, and what this board did not test. The four device scripts (DR-213) stay not tested.
9. **Next.** One or two sentences: rounds 4 and 5 with chapter 15, ending at board 3, then Gate 3.

### How the page is built

- Build on board 1's model (`work/build/scripts/phase-3/board_1_build.py`, `board_1_render.js`, `work/boards/phase-3/round-0/board-1/`) and the round 2 progress page's (`progress_round_2_build.py`, `progress_round_2_render.js`), which already compose kit captures and guide photographs by family. Copy to `work/build/scripts/phase-3/board_2_build.py` and `board_2_render.js`; leave every earlier builder and page untouched. Board 1 as published is the look to keep: https://claude.ai/artifact/5ncsC9iTiQ2Kyu3yqbZ4P1.
- One script reads every number, word and picture from files at build time; a content file holds only the board's own words and the files it reads; nothing typed by hand, so the main session can rerun it after each owner lands. Options as the progress builders have them: `--reuse`, `--check`, `--strict`, `--scratch`, `--out`.
- Outputs in `work/boards/phase-3/round-3/board-2/`: `20261113_Board-2.html`, `20261113_Board-2-Content.json`, `20261113_Board-2-Figures.json`, `20261113_Board-2-Check-Results.json`, and `img/` with composed pictures only. Raw captures and kit builds stay in scratch.
- The page: one HTML file with no scripts and no `<!doctype>`, `<html>`, `<head>` or `<body>` tags, `<title>Edition 06 Board 2</title>` and `<meta name="claude:viewport-fit-sides" content="cover">` first, then one `<style>`, as board 1's. Tables are live text; folds are `<details>`. Every `<img>` carries `loading="lazy"`, its width and height, and alt text that says what it shows. No sideways page scroll at 390 px; a picture wider than the column scrolls in its own named frame. Outside requests only to Google Fonts. The page under 16 MB.
- Publishing limits the folder must meet: at most 511 files and 256 MB in all, each image under 15 MB; the main session publishes it in batches of at most 255 files and 64 MB. Compose each picture so the folder stays near 300 files and under 120 MB; say the totals in your notes.
- Check with `node work/build/scripts/phase-2/dataviz_check.js <page> --board --no-captures` from `work/build`, on the page and on a copy wrapped as the host wraps it (`--check` does both), and report the result.

### The decision files the board reads

The data lead writes `work/handoffs/phase-3/20261113_Board-2-Decisions.json`: the items of panel 1 (each with `id`, `title`, `what_changed`, `why`, `recommendation`, `refs`, and the pictures or file paths it needs), the Rule 01.9 and DR-229 counts with the script that made them, and the forms-changed list. The builder reads it; the editor owns its words once the data lead has written them. Agree the schema between you in your notes in the first 20 minutes.

The cartographer writes the board-only pictures' sources into `work/handoffs/phase-3/board-2-pictures/`: the S12 stacked tile, drawn in scratch from a copy of the tile form at the guide's desk width with S12's data and nothing in `work/build/` changed; and today's gray 14.124 sketch file. The builder photographs them as it photographs the guide's.

## Who does what

| Owner | Role file | Notes file in `work/handoffs/phase-3/` | Work |
|---|---|---|---|
| Data visualization lead | `oa-dataviz-systems-lead.md` | `20261113_Board-2-Data-Lead-Notes.md` | Signs off A1 to A5 first; then the decision file: board 1 changes with S12's recommendation, forms whose tier or data changed, the V7.1 list, the Rule 01.9 and DR-229 recount; signs off every figure the board prints |
| Editor | `oa-editor.md` | `20261113_Board-2-Editor-Notes.md` | A1, A2's words, A4, A5's specs; then every word on the board, in the content file and the decision file, once the builder's first full build lands |
| Cartographer | a senior news cartographer (general-purpose, as round 3's, D3-1082) | `20261113_Board-2-Cartographer-Notes.md` | A2's drawing, A4's layout check; the board-only pictures |
| Research lead | `oa-research-lead.md` | `20261113_Board-2-Research-Notes.md` | A5's `snapshot_once` variants; the facts behind each V7.1 item; DR-258's rerun of the 668 comparisons from the files Dustin uploads, as data only, reading them in place from the upload folder (never copying into `source/`, which the session's permission check refuses) |

**DR-258's files so far.** V5 Polished arrived and matches the October 20 manifest byte for byte (4,285,909 bytes, SHA-256 `f4fff9cc…09c8d2`): `/root/.claude/uploads/4af740fe-eb77-5222-8bcc-cd714f9f6532/ef88da19-20261018_Oath-And-Action-Brand-Guide_V5-Polished.html`. Read it in place with `python3 -I`, by extraction script, never whole (CLAUDE.md, "Large files"); Phase 0's `work/build/scripts/extract_sources.py` and the reconciliation data (`work/handoffs/phase-0/20261020_Atlas-Reconciliation-Data.json`) and round 3's re-check (`work/research/20261113_Atlas-Recheck-Table.md`, `-Data.json`, D3-1094) show which comparisons read V5 Polished. Concepts V2 and the Atlas Visual System are not here yet; the main session tells you when either arrives.
| Engineer | `oa-engineer.md` | `20261113_Board-2-Engineer-Notes.md` | A1's phrase check, A3, A6; any build need the board or the stacked tile picture raises |
| Board builder | `oa-design-director.md` as page builder | `20261113_Board-2-Builder-Notes.md` | Part B: the script, the content file and the page; reruns as owners land |
| Creative director | `oa-creative-director.md` | `20261113_CD-Review-Of-Board-2.md` and `20261113_Board-2-CD-Scores.json` | Scores the board on the six criteria once its full build lands; the main session starts it |

Owners read each other's notes directly (D3-662): the data lead's "Rulings" and "Sign-off", the engineer's "Contracts", the editor's "Words for". Write calls as `- D3-xxx | decision | reason` lines under "Routine calls", with "Tested" and "Not tested" sections. Keep a "Status" section at the top of each notes file current.

## Order

1. All six owners start together. The data lead's sign-off of A1 to A5 comes as each lands; the builder writes and runs its script on today's files at once, so the method is proven while Part A lands.
2. When A6 passes, the main session makes a strict build and runs the quick guide check, then publishes the guide preview as version 9 (DR-259) and tells the builder; the builder reruns with `--reuse --check` against that build.
3. The editor reads the board; the creative director scores it; one fix round; the builder's final run with `--check --strict`.
4. The main session reads every file and publishes the board privately.

## Limits

- **Load.** At most two agents drive a browser at once; long runs use `--no-captures` where a tool offers it. Never run the guide check yourself; the main session runs it. Never count a crashed or cut-off check as run.
- **Clock.** Read `date -u` before you write a time.
- **Ownership.** Write only the files your row names, your notes, and your own scratch folder. The engineer alone edits the kit's shared files and the guide build and checks. Never touch `source/`, `deliverables/`, `work/ledger/`, any earlier board or progress page, or another owner's files. Word passes never touch mark or ink keys (V22). Do not commit, push or publish.
- **Weight.** A1 to A5 add no plate weight past D3-1328's ceilings; say each plate's bytes before and after in your notes.
- **Scratch.** `/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/<your-role>/` by absolute path; set `TMPDIR` to it. Run Playwright and node scripts with absolute output paths so nothing lands in the repository, and check `git status` for stray files you made.
- **Keys.** Never print or save a key. FEC and Congress.gov take the proxy's key (set a key variable to `proxy-injected`); the Census key is `CENSUS_API_KEY`. Python that reads supplied or downloaded files runs with `-I`.
- **Words.** Chapter 02's rules (`work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`): plain, spoken prose, no em dashes, no studio words a reader would not know on the board's face; decision codes and file paths only in small reference lines.
- **Nonpartisan.** One standard of evidence for everyone (DR-93); read every recommendation and every line about a party from the left and from the right (DR-124). Never manufacture balance.
- **Restarts.** Write your notes early and add to them as you go; the container can restart.
- Final message to the main session: under 150 words, your state, what landed, check results, and anything blocking.
