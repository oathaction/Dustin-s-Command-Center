# Board B, the decisions board: builder's notes

Oath & Action Edition 06, Phase 2, stage B, November 10, 2026. Written by the board builder for the main session, under `20261110_Board-B-Brief.md`, with the design director's layout judgment (`.claude/agents/oa-design-director.md`) and the editor's rules (`.claude/agents/oa-editor.md`, chapter 02). I published nothing, committed nothing and pushed nothing. Paths are relative to `oath-and-action-v6-brand-guide/`.

Status: rebuilt at 5:05 p.m. UTC with the creative director's rescore and the fixes for B1 and B2 from the creative director's read of the board (`20261110_CD-Review-Of-Stage-B-Chapters.md`, "Rescore after the fix pass"). **One rerun is left:** at publish, with the reader check's real address (B3). The rescore now prints (B4).

**To open:** `work/boards/phase-2/stage-b/board-b/20261110_Board-B.html`.

**To publish:** `/tmp/claude-0/-home-user-Dustin-s-Command-Center/c9dc3e94-c343-5611-8fc3-849f48a2fa49/scratchpad/publish-board-b/20261110_Board-B.html`, with `files.json` beside it mapping its seven files to `img/`. Like the earlier boards' copies (D2-317), it has no document skeleton, opens with its `<title>` and the viewport-fit tag, and sets `lang="en"` by script. Title: "Board B Decisions". Suggested icon: "checklist".

## What the board holds, in the brief's order

1. **Cover.** Kicker, "For Dustin Cathcart" and the build date, the title "Two decisions are yours", two sentences on what board B is, the three pages and what each is for (the chapters page linked at version 5, the reader check linked once its address is real, this board), the sample reply "All as recommended, and I approve option A for the error mark by name." with a copy button, and a short contents list.
2. **Decision 1, the error mark.** A row-by-row comparison of option A (as built) and option B (the mark in Pillar Red, same bar): the sign-up field and its message at actual size, built as `s-11-15-correct` builds its error state, with the message read from that specimen; the mark alone at 24 px on Newsprint and on the Error Band; the same enlarged four times, named; each figure with its contrast, computed from tokens.css. Recommendation A, and what Dustin approves: "Option A for the error mark, as Rule 11.15 draws it."
3. **Decision 2, tiles under the 48 px floor.** Rule 10.5's third paragraph quoted from the chapter file; Public meeting (CL-005) as a 48 px one-color Charcoal tile, alone at 48 px and alone at 32 px, at actual size, beside the other answer's smallest tile at 72 px. Recommendation: keep the exception. Approve: "Keep the one-color tile exception in Rule 10.5."
4. **The scores.** The round 3 table, six criteria for the five items, boxed under 4, each item linked to its chapter; the creative director's reason for each score under 4. A line says the rescore comes next. With a rescore, a second table sets the rescore apart, gives "was 3" in any cell that moved, and lists one line of reason for each move.
5. **Calls Dustin may overrule.** Four cards: the pillar row (Rule 09.1's places sentences and the social card's "Left out" line, both quoted from the files), the five look-alikes at 24 px with Rule 10.9's line, the examples moved off R-01 and R-02 (one sentence each for Rules 10.8 and 11.16), and the tokens zip (the file name read from D2-964).
6. **Answered this chat.** DR-190 to DR-198, one plain line each.
7. **Carried.** Missouri, Virginia's 2025 House count, Tangipa v. Newsom and Ohio's minutes, stage C's list, and the first reader check page's deletion.
8. **The reader check.** One Prussian panel: who it goes to, its address, the editor's two lines read from "The invitation" with the address in place of [link], and a copy button.

Decision codes sit only in small "codes" lines beside each card, which a screen reader hears as "For the record: …". Every rule number links to `https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF#rule-NN-N`, 18 anchors in all.

## How to rebuild and check

```
python3 -I work/build/scripts/phase-2/stage_b_board_b_build.py --strict --reader-check-url https://claude.ai/artifact/<id> [--guide <built chapters page>]
node work/build/scripts/phase-2/dataviz_check.js /tmp/claude-0/-home-user-Dustin-s-Command-Center/c9dc3e94-c343-5611-8fc3-849f48a2fa49/scratchpad/board-b/check-copy/20261110_Board-B.html --board
node work/build/scripts/phase-2/dataviz_check.js work/boards/phase-2/stage-b/board-b/20261110_Board-B.html --board --no-captures
```

The script holds only the board's own words (the `W` block at its top). Every fact comes from a file on each run: contrast from tokens.css, quoted rule text from the chapter files, the form's message from `s-11-15-correct`, the "Left out" line from `s-proofs-social`, the drawings and tile sizes from the inventory in use, names from the chapter 10 labels, the invitation from the editor's file, the zip's name from D2-964, and the scores from the scores file. It writes the board, `20261110_Board-B-Content.json` (every string and figure, with sources), `img/` beside the board, a check copy in the scratchpad and the publish copy. `--guide PAGE` also checks every anchor against a built chapters page. `--scores PATH` reads another scores file, for testing.

`--strict` exits 1 on any warning: a quoted sentence the chapters no longer hold, a contrast figure that differs from Rule 11.15's text, a decision code missing from the log, a studio code outside the codes lines, a flagged word, an en dash, a rule link with no rule behind it, a private path, a host other than claude.ai and Google Fonts, or a rescore it cannot read or a moved score with no reason. An em dash, a misquoted tagline or a page over 16 MB stops it. A missing rescore and the placeholder address print as notes.

**When the rescore lands.** Rerun. The script reads a `rescore` block shaped like the round 3 file: a dict with `items` (a list of `{key, scores, reasons, ready}`, or a dict keyed by item), or a dict keyed by item key directly. For a moved score it takes the reason from `moved`, `changes`, `reasons` or `why` under that criterion, or a plain string. If the creative director uses another shape, `--strict` fails and says so; then add the shape in `read_scores` and `moved_reason`. I tested two invented shapes (below).

**Copy edits** to strings taken from the scores file go in `OVERRIDES` near the top: exact text and replacement; the build warns when one matches nothing. One is in use: the group item's brand fidelity reason, rewritten to drop `s-05-3-corrective`, DR-173 and D2-881 from the reader's way.

## Routine calls

- D2-xxx | The board's words live in the script's `W` block, and the content JSON records every string and figure it prints | The brief asks the script to write the content JSON; one source of words keeps a rerun clean
- D2-xxx | Option B keeps the 4 px red bar and changes only the mark's color | D2-880 puts the mark "drawn in red" beside A, and the token described both the mark and its bar in red
- D2-xxx | Both options sit in one comparison, row by row: the form, the mark alone at 24 px, the mark enlarged four times | Dustin compares like with like on one line; on phones each row stacks A over B, still row by row
- D2-xxx | "On Newsprint" shows the mark alone on Newsprint, and "On the Error Band" shows it on the band, since in the form the mark sits only on the band | The brief asks for both grounds, and Rule 11.15's figures name both
- D2-xxx | The enlargement draws the 24 px master as a vector at 96 px and names it "four times", with its 8 px line | The brief asks that the enlargement be named; a vector keeps the drawing exact
- D2-xxx | Contrast figures are computed by WCAG 2.2's formula from tokens.css and rounded to two places, and the build warns if Rule 11.15 prints different figures | The brief asks for figures computed by the script; 2.64, 2.96 and 11.89 match the rule, and A on Newsprint is 13.29
- D2-xxx | A figure under 3 to 1 carries a box and the words "under 3 to 1" | No color carries the failure, and the board has no red of its own
- D2-xxx | The recommendation adds that a 2 px line has no room for Rule 05.5's Charcoal keyline | Dustin may ask why B cannot take the keyline red marks take on Newsprint; the chapter 11 notes give this reason
- D2-xxx | The form's message is read from `s-11-15-correct`, with its no-break space before "@" | The board shows the words the rule's own form shows, and the line breaks as the fixed specimen does
- D2-xxx | Every Pillar Red mark sits under `data-red="working"` with the job "error" | The board check counts one working-red job per view; every red on the board is the error's
- D2-xxx | Decision 2 shows Public meeting (CL-005) | A topic symbol off the list of 41 whose one-color tile starts at 48 px, and a subject Rule 10.9 already names
- D2-xxx | Decision 2 adds the other answer's smallest tile, 72 px, set apart in its own stage | The choice is between the two, and seeing both at actual size is what Dustin approves on
- D2-xxx | The tile's drawing size is printed as "about 33 px" and "about 49 px", from the inventory's 0.68 square factor | 48 × 0.68 is 32.64 and 72 × 0.68 is 48.96; the rule says 32 to 34
- D2-xxx | Civic Line drawings show as images of their own SVG files in `img/`; the error mark draws inline in currentColor | Civic Line files carry ids that would repeat inline (D2-617); the error mark needs currentColor to change color
- D2-xxx | A small script moves each mark and drawing by under one pixel onto whole CSS pixels | As D2-565, so a 1x screen draws them as their masters are drawn
- D2-xxx | Rule quotes are found by content, not by position, and the footer names the paragraph's place | The editor may still move sentences; a quote that disappears warns
- D2-xxx | The board's section headings use the section style for the two decisions and the reader check, and the H3 style for the rest | The two decisions are what Dustin answers; the rest supports them
- D2-xxx | The reader check's address shows as text while it is the placeholder, and as a link once real | A placeholder link would lead nowhere
- D2-xxx | Copy buttons call the clipboard first, then select the text and use the browser's own copy, then ask for Ctrl or Command and C | The viewer may refuse the clipboard; the brief asks for a button that works without the host
- D2-xxx | Rule links open in the same tab | Rule 11.13 says our own links open in the same tab
- D2-xxx | One light look, on the brand's surfaces, with every color set explicitly | The board shows specimens on Newsprint and the Error Band at actual size; a dark version would change what Dustin approves
- D2-xxx | CSS comments are stripped from the page, the tokens' header included | It printed repository paths, which the brief keeps off the page
- D2-xxx | The scores table scrolls inside its own region on phones | Six criteria and an item name do not fit 360 px; the region takes keyboard focus

## Tested

- `python3 -I work/build/scripts/phase-2/stage_b_board_b_build.py --strict --guide <scratch>/board-b/guide/guide.html`: exit 0, 0 warnings, two notes (no rescore yet; the placeholder address). The page is 115 kB with seven SVG files of 18.5 kB. The guide page I built for the anchor check came from `guide_build.py --out <scratch>/board-b/guide/guide.html`, and `git status` was the same before and after it. All 18 anchors are on it.
- `node work/build/scripts/phase-2/dataviz_check.js <board> --board`, with captures on the scratch copy and with `--no-captures` on the board: PASS, 0 failures at 1,440, 390 and 360 px. At each width: no sideways scroll, smallest text 13 px, no contrast failure, axe-core 4.10.2 with no violations, 19 red marks all under `data-red` with one job, "error", fonts Inter, Inter Tight and Lora loaded; 35 focus stops at 1,440 px, each with a visible ring. An earlier run failed at 360 px (369 px wide) from the placeholder address in the invitation; it now wraps.
- Copy buttons, by script in Chromium: with the clipboard allowed, both buttons put the exact text on the clipboard (the invitation with its two paragraphs and the address); with `writeText` rejecting, and with no clipboard API at all, both select the text, the browser's copy returns true, and the status reads "Copied."
- The rescore path, on two invented scores files in the scratchpad, never in the repository: a list-shaped block printed the second table, "was 3" in three cells and two reason lines, and `--strict` failed on the third move, which had no reason, as it should; a dict-shaped block passed.
- A real-looking address (`https://claude.ai/artifact/AbCdEfGh123`, built to the scratchpad) shows as a link and fills the invitation; a non-claude.ai address stops the build before it writes anything.
- The publish copy and the board in Chromium: nine images, none broken, ten inline marks, `lang="en"`, no page errors.
- By the build's own checks: no em dash, en dash or flagged word; no DR or D2 code outside the codes lines; no `/home/`, `/tmp/`, `file:` or `work/` on the page; every DR and D2 code on the board is in the decision log; DR-190 to DR-198 each name Dustin as source; Rule 10.5's paragraph names 94, the inventory's count of drawings whose one-color tile starts at 48 px; Rule 10.8's caption says all 10; Rule 11.16's caption names R-32.
- Looked at by me: at 1,440 px at 1x every section; at 1,440 px at 2x the comparison rows and the five look-alikes; at 390 px at 1x the cover, decision 1, the calls; at 390 px at 2x decision 2 and the reader check. Fixes from those looks: an absolutely placed hidden label in the table that pushed the page to 640 px at 390, the tile figures stretched and out of line, "48 / px" split across lines, the look-alike captions at uneven heights, the zip's name broken at a hyphen, the tile figures stacked on phones, and a too-narrow column for the 72 px tile.

## Not tested

- Safari, Firefox, a real phone, a real 2x screen, a screen reader by ear, 200 percent text, forced colors and print.
- What the system clipboard holds on the fallback path; the script saw the selection and a true return from the browser's copy only.
- The board inside the claude.ai viewer, where the clipboard and links behave as the host allows.
- The rescore as the creative director will write it; I tested two shapes I invented.
- Whether my words pass every pattern chapter 02 lists. I read them against the rules and changed a parallel run (DR-190), three passive lines and a few others; the editor has not read them.
- The chapter files as the fix pass finishes them. The board reads them on each run, so a rerun after the pass picks up their final words.

## Second build, after the creative director's read of board B

- **B1.** The sample reply names both decisions: "All as recommended. I approve option A for the error mark by name, and keep the one-color tile exception in Rule 10.5."
- **B2.** The examples card no longer says the guide stays off R-01 and R-02. It says Rule 10.8 used to show only R-01 and R-02 and now draws all 10; Rule 11.16's bill moved to local news grants and reform R-32; and nothing else moved. Rule 12.5's marker and the reader check stay on loop R10 and reform R-01, and the only change DR-195 made was to move chapter 11's stepper to loop R1. DR-195 joins the card's codes.
- **B4.** The rescore table and "What moved in the rescore" print. Five moves, each with the creative director's reason; the group item's reason goes through a new copy edit that drops `s-05-3-corrective`, D2-881 and D2-959.
- **Answered and carried.** DR-195 to DR-198 were already in "answered". "Carried" adds the tile question (D2-976) as its last line, which closes when Dustin answers decision 2.
- Rule links keep "Rule" and the number on one line.
- Tested: `--strict` with the placeholder address and `--guide` on my scratch guide build: exit 0, 0 warnings, 20 anchors. `dataviz_check.js --board` at 1,440, 390 and 360 px: PASS, 0 failures, on the board and on the scratch copy. The sample reply's copy button copies the new words. Looked at the scores section and the examples card at 1,440 px at 1x.
- Not tested: the editor's read of the new sentences.

## Change log

Created:
- `work/build/scripts/phase-2/stage_b_board_b_build.py`
- `work/boards/phase-2/stage-b/board-b/20261110_Board-B.html`
- `work/boards/phase-2/stage-b/board-b/20261110_Board-B-Content.json`
- `work/boards/phase-2/stage-b/board-b/20261110_Board-B-Check-Results.json` (written by the check)
- `work/boards/phase-2/stage-b/board-b/img/` (seven Civic Line SVGs, copied from `work/build/assets/`)
- `work/handoffs/phase-2/20261110_Board-B-Builder-Notes.md` (this file)
- Outside the repository, in the scratchpad: the publish copy and `files.json` in `publish-board-b/`; in `board-b/`, the check copy and its results and captures, my capture and test scripts in `tools/`, the scratch guide build, and the rescore and address tests.

Modified in the second build: the script, the board, its content JSON and check results, and this file. Modified: none of anyone else's. I left `source/`, `work/ledger/`, `deliverables/`, the guide's chapters, specimens and shell, every other board and the reader check pages as I found them.
