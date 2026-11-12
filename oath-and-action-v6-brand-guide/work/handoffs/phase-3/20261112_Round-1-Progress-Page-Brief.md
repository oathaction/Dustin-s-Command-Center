# Brief: the round 1 progress page

Oath & Action Edition 06, Phase 3, November 12, 2026. Written by the main session for the page builder. Paths are relative to `oath-and-action-v6-brand-guide/`.

## What Dustin asked for

DR-241: "A short private progress page follows round 1 and round 2, showing each round's charts at desktop and phone widths and asking no decision; board 2 after round 3 stays the board where Dustin decides." The page is private, published with the Artifact tool by the main session. It asks nothing. It shows him the work as it stands after round 1's fix pass, second pass and the creative director's rescore.

## Who you are

The design director building a review page (`.claude/agents/oa-design-director.md`). You built board 1 in the last chat; read its builder notes, `work/handoffs/phase-3/20261112_Board-1-Builder-Notes.md`, and reuse its method and code where it fits (`work/build/scripts/phase-3/board_1_build.py`, `board_1_render.js`, `work/boards/20261021_Board-Conventions.md`, `work/boards/board-base.css`). The page is shorter than board 1: no decisions, no options, no Phase 2 comparison.

## What the page holds, in order

1. **Round 1 in one screen.** What round 1 built, every count read from files: chapter 14's 41 entries (26 new specimens S17 to S42, 11 built specimens as entries, 4 sketches), rules 14.1 to 14.14 with the opener, chapter 15's opener and its round 1 rules, round 3's data frozen, and the Department of Labor download frozen if the research lead's notes say so. One line that the page asks no decision and that board 2 follows round 3. Where the guide build stands: bytes, rules, specimens, warnings, from a fresh strict build.
2. **The 26 new charts.** Grouped by family in the plan file's order (`work/handoffs/phase-3/20261112_Chapter-14-Plan.json`). For each: its rule number and form name, its title as printed, the maker, and two composed pictures from the kit's own captures: Newsprint at 1440 and 390 px side by side, and the same on Charcoal (board 1's method, D3-195 and D3-196). Below the pair, one line with the chart's bytes in the guide and its check result.
3. **How an entry reads in the guide.** One entry photographed in the strict build at a 1440 px window and at 390 px, so Dustin sees the entry layout (use when, use instead, specimen, table) once.
4. **The four sketches** (14.24, 14.43, 14.44, 14.45), each with its heading as the guide prints it.
5. **Rules 14.1 to 14.14.** Each rule's title, with its correct and failure plates photographed from the strict build at a 1440 px window, composed side by side or stacked as reads best.
6. **Chapter 15's round 1 plates.** The opener and every plate built, photographed from the strict build at 1440 and 390 px.
7. **Scores.** The creative director's first-pass scores and rescores per item (`work/handoffs/phase-3/20261112_Round-1-CD-Scores.json` and the newest `*Round-1-CD-Rescore*.json` when it lands), and each red team report's score with its Must fix and Should fix counts, read from the reports' own numbered findings.
8. **Weight.** Chapter 14's bytes against its 2,803,941 byte stop, the share per plate still to come, chapter 15 against its ceiling, and the page projection against 15.5 MB, from the build report.
9. **Tested and Not tested**, kept apart, from the notes files and reports.
10. **Next.** One sentence: round 2 builds composition, distribution and density, correlation, uncertainty and estimates, and gauges and indicators. No question.

## How

- A script, `work/build/scripts/phase-3/progress_round_1_build.py` (and a render script beside it if Playwright work needs one), reads every number and picture from files at build time; a content file beside the page holds only words and file names. Nothing typed by hand, so the main session can rerun it after the rescore.
- Output: `work/boards/phase-3/round-1/progress/20261112_Round-1-Progress.html` with `img/` beside it, and a figures file and a check results file as board 1 had. Only composed pictures go in `img/`; raw captures and kit builds stay in scratch. Remove images the page no longer names on every run.
- Kit captures: `node work/build/chart-kit/oa-chart.mjs build sNN --out <scratch>/kit-out` (or `--all`), PNGs on. Guide pictures: a strict build of the guide into scratch (`python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/guide.html`), with the sticky bars set static and every chart drawn before you photograph (call `OAChart.draw_all()` and wait for positions to hold, D3-200).
- Pictures at true size on whole pixels, compressed without loss of the pixels; keep the folder under 200 files and 50 MB.
- The page: one HTML file with no scripts. Write page content directly (no `<!doctype>`, `<html>`, `<head>` or `<body>` tags; the host wraps it). Put `<title>Edition 06 Round 1 Progress</title>` and `<meta name="claude:viewport-fit-sides" content="cover">` at the top, then one `<style>`. Use the brand as board 1 did: Newsprint ground, Inter Tight and Inter from Google Fonts with fallback stacks, Charcoal text, the guide's tokens as named colors. It commits to one look (Newsprint), so it carries no dark-mode blocks, but every color is a token defined on `:root` and `body` sets its background from one. Side gutter: `padding-left: max(16px, env(safe-area-inset-left, 0px))` and `padding-right: max(16px, env(safe-area-inset-right, 0px))` on one outer wrapper, vertical padding with `padding-block`. No sideways page scroll at 390 px; a wide composite scrolls in its own `overflow-x: auto` frame with a name and a tab stop. Outside requests only to Google Fonts. Every image has alt text that says what it shows.
- Words follow chapter 02's rules (`work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`): plain, short, no em dashes, no studio words a reader would not know; decision codes and file paths only in small reference lines (D3-206).
- Check the page with `node work/build/scripts/phase-2/dataviz_check.js <page> --board` from `work/build` and report its result.

## Timing

Write the script and content now and run it once on the current files, so the method is proven. The fix pass is starting; specs, plates and scores will change. When the main session tells you the rescore has landed, rerun and report. Keep a section "Status" at the top of your notes file current.

## Notes and limits

- Notes: `work/handoffs/phase-3/20261112_Round-1-Progress-Page-Builder-Notes.md`, with "Status", "Routine calls" as `- D3-xxx | decision | reason` lines, "Tested" and "Not tested".
- Write only your script(s), your notes file and the `work/boards/phase-3/round-1/progress/` folder. Never touch `source/`, `deliverables/`, `work/ledger/`, specs, forms, entries, chapters or another owner's file. Do not commit, push or publish.
- Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/256961f5-3911-5bd9-908d-f34ce0435ace/scratchpad/phase-3/round-1/progress-page/` by absolute path; set TMPDIR to it. Run Playwright scripts with absolute output paths so nothing lands in the repository.
