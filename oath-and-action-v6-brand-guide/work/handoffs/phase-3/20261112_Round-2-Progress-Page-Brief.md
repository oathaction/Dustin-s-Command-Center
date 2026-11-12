# Brief: the round 2 progress page

Oath & Action Edition 06, Phase 3, November 12, 2026. Written by the main session for the page builder. Paths are relative to `oath-and-action-v6-brand-guide/`.

## What Dustin asked for

DR-241 and DR-246: a short private progress page follows round 2, showing its charts at desktop and phone widths and asking no decision. Board 2 after round 3 stays the board where Dustin decides. The page is private, published with the Artifact tool by the main session. It shows him the work as it stands after round 2's fix pass, second pass and the creative director's rescore.

## Who you are

The design director building a review page (`.claude/agents/oa-design-director.md`). Round 1's page is your model: read its brief, `work/handoffs/phase-3/20261112_Round-1-Progress-Page-Brief.md`, and its builder notes, `work/handoffs/phase-3/20261112_Round-1-Progress-Page-Builder-Notes.md` ("Status", "How to rerun", "What the page reads"). Copy `work/build/scripts/phase-3/progress_round_1_build.py` and `progress_round_1_render.js` to `progress_round_2_build.py` and `progress_round_2_render.js` and adapt them; leave round 1's scripts and page untouched. The round 1 page as published is the look to keep, at the same quality: https://claude.ai/artifact/AUM5CtTDVPvPARKM5B3Hu6 (its source is `work/boards/phase-3/round-1/progress/20261112_Round-1-Progress.html`).

## What the page holds, in order

1. **Round 2 in one screen.** Every count read from files: chapter 14's 41 new entries (22 new specimens S43 to S64, four built specimens as entries, 15 sketches), chapter 15's six new rules (15.11, 15.12, 15.15 to 15.18) with their 12 plates, round 4's data frozen (P7-301 to P7-310), and the carried items now done (Rule 14.9 on the interval form, Rule 14.3's red point, chapter 14's plate style printed once, chapter 13's five titles with a period, chapter 15's wide stage at 1024 and 768 px). One line that the page asks no decision and that board 2 follows round 3. Where the guide build stands: bytes, rules, specimens, warnings, from a fresh strict build.
2. **The 22 new charts.** Grouped by family in the plan file's order (`work/handoffs/phase-3/20261112_Chapter-14-Plan.json`, round 2's rows). For each: rule number and form name, title as printed, maker, and round 1's two composed pictures (Newsprint at 1440 and 390 px side by side; the same on Charcoal), with one line of bytes in the guide and the check result. Mark the four Estimate charts (S51, S52, S53, S59) as the guide labels them.
3. **Two round 1 charts the round changed**, S18 and S33, in the same form, each with one line saying what changed (the two named fifths in ink; the all receipts line dashed in the text's ink).
4. **How an entry reads in the guide.** One round 2 entry photographed in the strict build at 1440 and 390 px; take 14.74 (the range bar, S57), which shows the desk's "On a phone" drawing.
5. **The 15 sketches**, each photographed at 1440 px with its heading and its caption as the guide prints them, the four avoid pairs first.
6. **Rules 14.1 to 14.14 as round 2 changed them**: Rules 14.3, 14.6, 14.9, 14.11 and 14.12, each title with its correct and failure plates photographed at 1440 px; and the opener.
7. **Chapter 15's six new rules**, every plate photographed from the strict build at 1440 and 390 px, and one wide plate also at 1024 px.
8. **Scores.** The creative director's first-pass scores and rescores per item (`work/handoffs/phase-3/20261112_Round-2-CD-Scores.json` and the newest `*Round-2-CD-Rescore*.json` when it lands), and each red team report's score with its Must fix and Should fix counts and its second score, read from the reports' own numbered findings.
9. **Weight.** Chapter 14's bytes against its 2,803,941-byte stop, the share per plate still to come, chapter 15 against its ceiling, and the page projection against 15.5 MB, from the build report.
10. **Tested and Not tested**, a short summary as round 1's part 9 became (about 200 words), each figure read from its file: the strict build, the quick and four-width guide checks (the main session's results files in scratch, named below), the kit's `build --all`, the data check, the makers' figure checks, the second passes and the rescore.
11. **Next.** One sentence: round 3 builds maps, structure, relationships, flow and behavior, with a cartographer. No question.

## How

- Everything as round 1's brief section "How" sets it: one script reads every number and picture from files at build time; a content file holds only words and file names; nothing typed by hand, so the main session can rerun it after the rescore.
- Output: `work/boards/phase-3/round-2/progress/20261112_Round-2-Progress.html` with `img/` beside it, `20261112_Round-2-Progress-Content.json`, `-Figures.json` and `-Check-Results.json`. Only composed pictures go in `img/`; raw captures and kit builds stay in scratch. Keep the folder under 200 files and 50 MB.
- The page: one HTML file with no scripts, no `<!doctype>`, `<html>`, `<head>` or `<body>` tags; `<title>Edition 06 Round 2 Progress</title>` and `<meta name="claude:viewport-fit-sides" content="cover">` first, then one `<style>`, exactly as round 1's page. No sideways page scroll at 390 px. Outside requests only to Google Fonts. Every image has alt text that says what it shows.
- Words follow chapter 02's rules (`work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`): plain, short, no em dashes, no studio words a reader would not know; decision codes and file paths only in small reference lines.
- The guide check results: the quick check's results file is `/tmp/claude-0/-home-user-Dustin-s-Command-Center/3ab6316c-6935-5f23-804c-cfaafd548447/scratchpad/phase-3/round-2-review/main/quick/guide-Guide-Check-Results.json` and the four-width check's `.../main/full/guide-Guide-Check-Results.json` for the review's build; the main session names the final build's results when the rescore lands.
- Check the page with `node work/build/scripts/phase-2/dataviz_check.js <page> --board` from `work/build`, on the page and on a copy wrapped as the host wraps it, and report the result.

## Timing

Write the script and content now and run it once on the current files, so the method is proven. The fix pass will start soon; specs, plates and scores will change. When the main session tells you the rescore has landed, rerun with `--reuse --check` and report. Keep a section "Status" at the top of your notes file current.

## Notes and limits

- Notes: `work/handoffs/phase-3/20261112_Round-2-Progress-Page-Builder-Notes.md`, with "Status", "How to rerun", "Routine calls" as `- D3-xxx | decision | reason` lines, "Tested" and "Not tested".
- Write only your two scripts, your notes file and the `work/boards/phase-3/round-2/progress/` folder. Never touch `source/`, `deliverables/`, `work/ledger/`, round 1's progress scripts and page, specs, forms, entries, chapters or another owner's file. Do not commit, push or publish.
- Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/3ab6316c-6935-5f23-804c-cfaafd548447/scratchpad/phase-3/round-2/progress-page/` by absolute path; set TMPDIR to it. Run Playwright scripts with absolute output paths so nothing lands in the repository.
- Final message to the main session: under 150 words, the page's state, its file count and bytes, the check result, and anything blocking.
