# Brief: the Gate 3 board

Written November 20, 2026, by the main session of chat 9. Dustin approved a Gate 3 board on board 3's model, smaller (DR-293). Board 3 is the model: its brief (`work/handoffs/phase-3/20261120_Board-3-Brief.md`), its builder (`work/build/scripts/phase-3/board_3_build.py`, `board_3_render.js`) and the page as published (https://claude.ai/artifact/DTyFuqgpUj4FybK7JdyaEb). Keep its look.

The board reads the final build of the apply pass, published as the chapters page's version 14. The main session gives the builder its path when it lands. "Before" pictures come from version 13 (`work/boards/phase-3/review-4-5/20261120_Guide-Preview-V13.html`).

## What the board holds, in this order

1. **Cover.** Kicker "Edition 06 · Phase 3 · Gate 3", a title, "For Dustin Cathcart" with the build date, a deck of two or three sentences, the panel list, and how long the decisions take to read.
2. **What you decide at Gate 3** (panel 1). Each item opens with its answer and the studio's recommendation, then what it rests on. The items and their words come from the Gate 3 report (`work/ledger/20261120_Gate-3-Report.md`, section "At Gate 3 you decide"), which the main session writes; until it lands, use the list in this brief's last section. One reply line: "To answer, reply “As proposed”, or name the item and your change."
3. **The Phase 4 proposal** (panel 2). The eight channels as a table (channel, chapter, applications, starting sizes to verify), the chapter allocations against the page's 16 MB, the chats and boards, and the checks. Words from the report's section 9.
4. **Board 3's answers, applied** (panel 3). One card per reply in `work/handoffs/phase-3/20261120_Board-3-Answers.md`, in reply order: what the answer asked, what changed and in which rule, version 13's picture beside version 14's at true size where the change shows (1440 px, and 390 px where the change is a phone's), or one line saying where nothing changes on screen and how the change was checked. Replies that changed nothing (1 to 5, 19, 21, 24) take one line each. The owners' notes say what changed: `work/handoffs/phase-3/20261120_Apply-Pass-Editor-Notes.md`, `20261120_Apply-Pass-Engineer-Notes.md`, `20261120_Apply-Pass-Data-Lead-Notes.md`, `20261120_Apply-Pass-Accessibility-Notes.md`.
5. **The label clearance list** (panel 4, DR-295). The charts the kit's label clearance check would move if it were switched on for every chart, read from `work/handoffs/phase-3/20261120_Label-Clearance-List.json`: chart, width, label, and a picture of each at the width it fails, with S59's moved label beside its old place.
6. **Scores** (panel 5). The creative director's last score for every Phase 3 item, read by `python3 -I work/build/scripts/phase-3/gate_3_scores.py --out <scratch>/scores.json`; the apply pass rescore (`20261120_Apply-Pass-CD-Rescores.json`); boards 2 and 3; this board's score when it lands.
7. **Page weight** (panel 6). From version 14's strict build report: the page, each chapter against its figure, chapter 14 with the kit, the projection, and Phase 4's room under 16 MB.
8. **Tested and Not tested** (panel 7), kept apart, each figure read from its file: the strict build, the four-width check and the quick check with photographs, the kit's `build --all --no-png`, `phase3_ch14_build.py --check`, the data check, the V7 check. Safari, Firefox, real screen readers and DR-213's four device scripts stay not tested (DR-279).

## How the page is built

- Copy `board_3_build.py` and `board_3_render.js` to `work/build/scripts/phase-3/gate_3_board_build.py` and `gate_3_board_render.js`; leave every earlier builder and page untouched. One script reads every number, word and picture from files at build time; a content file holds only the board's own words and the files it reads. Options as before: `--reuse`, `--check`, `--strict`, `--scratch`, `--out`.
- Outputs in `work/boards/phase-3/gate-3/board/`: `20261120_Gate-3-Board.html`, `20261120_Gate-3-Board-Content.json`, `20261120_Gate-3-Board-Figures.json`, `20261120_Gate-3-Board-Check-Results.json`, and `img/` with composed pictures only. Raw captures stay in scratch.
- The page: one HTML file with no scripts and no `<!doctype>`, `<html>`, `<head>` or `<body>` tags, `<title>Edition 06 Gate 3</title>` and `<meta name="claude:viewport-fit-sides" content="cover">` first, then one `<style>`, as board 3's. Tables are live text; folds are `<details>`. Every `<img>` carries `loading="lazy"`, its width and height, and alt text that says what it shows. No sideways page scroll at 390 px. Outside requests only to Google Fonts. Aim for under 120 pictures and under 30 MB so one publish carries it.
- Check with `node work/build/scripts/phase-2/dataviz_check.js <page> --board --no-captures` from `work/build`, on the page and on a copy wrapped as the host wraps it (`--check` does both).

## Who does what

| Owner | Role file | Notes file | Work |
|---|---|---|---|
| Board builder | `oa-design-director.md` as page builder | `work/handoffs/phase-3/20261120_Gate-3-Board-Builder-Notes.md` | The script, the content file, the board's words in first draft, and the page |
| Creative director | `oa-creative-director.md` | `20261120_CD-Review-Of-Gate-3-Board.md`, `20261120_Gate-3-Board-CD-Scores.json` | Scores the board on the six criteria; one fix round |

The main session reads every word on the board against chapter 02's rules and Dustin's settled list before publishing, and publishes it privately.

## Limits

- **Load.** Run `bash /tmp/claude-0/-home-user-Dustin-s-Command-Center/b10533d7-1a9f-5c9c-9fa4-64f6867e8ec0/scratchpad/c09/browsers.sh` first and open a browser only on "OK to open one" (read its words, never its exit status). Never run the guide check.
- **Clock.** Read `date -u` before you write a time.
- **Ownership.** Write only the files your row names, your notes and your scratch folder `/tmp/claude-0/-home-user-Dustin-s-Command-Center/b10533d7-1a9f-5c9c-9fa4-64f6867e8ec0/scratchpad/c09/builder/` (set `TMPDIR` to it). Never touch `source/`, `deliverables/`, `work/ledger/`, any earlier board, any generator, chapter, spec or kit file. The board changes nothing in the guide. Do not commit, push or publish.
- **Words.** Chapter 02's rules: plain, spoken prose, no em dashes, no studio words a reader would not know on the board's face; decision codes and file paths only in small reference lines.
- **Nonpartisan.** One standard of evidence for everyone (DR-93). Never manufacture balance.
- **Settled work.** No recommendation may change a settled element: the Civic Line icons, Reforms R-01 and R-02 like every other reform (DR-223), the atlas visual system (DR-36), the chart system (DR-52 to DR-61), the coverage plan (DR-62, DR-63), the chart rules of DR-64 with DR-255's exception, chapter 02's writing rules, and every answer Dustin has given from DR-95 on.
- Final message to the main session: under 150 words, your state, what landed, check results, and anything blocking.

## The decisions, until the report lands

1. Chapters 13, 14 and 15 as built, with the creative director's scores.
2. The chart kit as an asset of Phase 5's package.
3. The reconciliation table's resolutions (Rule 15.25) and the atlas V7.1 rows 38 to 46.
4. The token release 6.0.0-gate3.3's chart tokens, to ship in 6.0.0 at Phase 5.
5. The label clearance check: switch it on for every chart, or keep it opt-in (DR-295).
6. The Phase 4 proposal, with its questions.
