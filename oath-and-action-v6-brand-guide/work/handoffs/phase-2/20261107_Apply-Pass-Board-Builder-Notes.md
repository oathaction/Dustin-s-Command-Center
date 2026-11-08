# Apply pass changes board: builder's notes

Oath & Action Edition 06, Phase 2, November 7, 2026. Written by the board builder, working as the engineer (`.claude/agents/oa-engineer.md`) with the design director's layout judgment (`.claude/agents/oa-design-director.md`), for the main session. I published nothing, committed nothing and pushed nothing. Paths are relative to `oath-and-action-v6-brand-guide/`.

**To open:** `work/boards/phase-2/apply-pass/20261107_Apply-Pass-Changes-Board.html`.

**To publish:** the copy in my scratchpad, `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ab3d43b8-cc87-5ece-933a-c4123e99234a/scratchpad/publish-apply-pass-board/20261107_Apply-Pass-Changes-Board.html`, with `files.json` beside it mapping the 58 images to `captures/`. It has no document skeleton and sets `lang="en"` by script, as board A's copy does (D2-317). The page and its images come to 7.60 MB (0.22 MB of HTML, 7.38 MB of images).

**To rebuild:**

```
git show 3130c5b:oath-and-action-v6-brand-guide/work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html > <scratch>/before.html
python3 -I work/build/scripts/phase-2/apply_pass_board_build.py --strict --before <scratch>/before.html
node work/build/scripts/phase-2/dataviz_check.js work/boards/phase-2/apply-pass/20261107_Apply-Pass-Changes-Board.html --board --no-captures
```

The builder never rebuilds the chapters page. It reads the after page as it stands, `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` (last written 7:45 a.m. UTC), and the before page from commit 3130c5b, the apply pass brief's commit at 6:08 a.m. UTC, before any owner changed the guide.

## What the board holds

- **Cover.** What the board shows, what Dustin is asked, and a sample reply: "Q1 to Q10: as recommended, and I approve Q1, Q2, Q3, Q5, Q6 and Q7 by name."
- **01 Scores.** From `20261107_CD-Scores.json`: the lowest score on each criterion with the creative director's reason (all six at 4), the sign-off (signed), a table by chapter, every chapter score with its reason in a disclosure, and what the recheck left open. The builder checks that each criterion's stated lowest matches the chapters' scores.
- **02 What changed.** 21 cards, Board 6 first, then board A. 18 carry captures; DR-114, DR-121 and DR-123 changed nothing visible and take one line each. Each card gives the decision in one sentence, its links into the published chapters page, the before above the after at 1,440 px, and both side by side at 390 px for the trackers, the pillar row, the H.R. 7008 card and the lockup sheet. DR-128 has a card of its own after B6-1, and it holds the H.R. 7008 card on six steps. DR-127's card shows one view, since H10's line read the same before the pass.
- **03 What the review found.** The four Must fix items (CD-M1, BE-01, BE-02, CA-M1), each with what was found and how it was closed, and the 28 Should fix items by state: 22 fixed in full, 3 fixed with one part carried to stage B (BE-08, CA-S7, CA-S12), 1 fixed with its size waiting on Q2 (CA-S4), and 2 waiting on Q3 (CA-S1, CA-S2). I took the counts from the four owners' fix pass sections.
- **04 Decisions for you.** Q1 L6's pillar dots, Q2 the end mark at cap height, Q3 the proposed 48 px lockmark master, Q4 Rule 01.11's reason with its three versions side by side and each sentence's word count computed by the builder. Q1, Q2 and Q3 say they need approval by name; Q4 says why gate rule 4 does not apply.
- **05 Stage B.** The proposed scope for chapters 09 to 12 in a table, then Q5 to Q10 from the scoping notes, with Q5, Q6 and Q7 marked as needing approval by name.
- **06 Your reply.** The one Prussian panel. Marks save in the viewer's browser only, keyed to the questions' text (D2-316); a tick in "I approve Qn by name" adds "Approved by name." to that answer's line.

## Routine calls

- D2-xxx | A 1,440 px view is the chapter column, 24 px either side of it, under the masthead, cropped to a set height or to just above the rule's "Tokens" label | Each view shows the place that changed, and 50 captures come to 7.4 MB, well inside 16 MB
- D2-xxx | The before page is the chapters page at commit 3130c5b, saved outside the repository and passed to the builder by path | It is the last state of the page before any apply pass change, and the repository holds no second copy of it
- D2-xxx | Before sits above after at 1,440 px, joined by the hinge divider, and the two sit side by side at 390 px | Old above new with the hinge divider, as D2-314 set for board A's letter spacing pairs
- D2-xxx | From 80em a change card sets its words in a sticky column beside a 920 px column of views; a card with a plate wider than that stacks | The decision stays in sight while Dustin scrolls tall captures, and wide plates keep true size
- D2-xxx | The decision plates use the identity designer's own twice-size renders, shown at true size; L6's pair is captured cell by cell from the designer's plate page and set one above the other at one left edge | Two 884 px strips side by side need 1,866 px, so stacked they show whole at 1,440 px without scrolling
- D2-xxx | The designer's "masters compared" plate stays off the board | At 1,389 px it would scroll, and the places plates, the larger sizes plate and the card's figures carry the same comparison
- D2-xxx | The board adds a plate of today's display master and the proposed 48 px master at 48, 96 and 192 px, drawn by the capture script from the two files, and reads "display size" as 192 px | The creative director's recheck recommends approval once the board shows 96 px and display size; 192 px is four times the proposal's grid, and neither file changes
- D2-xxx | The questions run Q1 to Q10 across both sections | One reply line per question, with no clash with board A's A numbers, Board 6's B6 numbers or lockup S1
- D2-xxx | A card that needs approval by name carries an "I approve by name" box, and its tick adds "Approved by name." to the reply line | Gate rule 4 needs the approval in Dustin's words, and the box lets him give it question by question
- D2-xxx | A10's before shows the record of retired lines as it stood, with four lines | The before page never printed DR-122's two lines, which waited on board A
- D2-xxx | The board check runs with `--no-captures` once it has passed with captures | Its full-page captures land in the board's own captures folder, and at 390 px the page runs past the 65,535 px a JPEG can hold, so that capture is an empty file; I removed the three by-products and looked at the board through my own renders
- D2-xxx | The publish copy and its `files.json` sit in my scratchpad, rebuilt on every run | As board A's builder does, so the publish call sends only the images the board uses

## Questions for Dustin on the board

| # | Question | Recommendation | Named approval |
|---|---|---|---|
| Q1 | Should L6 lose its four pillar dots? | (a) L6 without the dots | Yes |
| Q2 | Should the end mark stand at the text's cap height, below B's 16 px minimum? | (a) cap height, as an exception | Yes |
| Q3 | Should the masthead and the sign-off take a new 48 px lockmark master? | (a) approve the 48 px master | Yes |
| Q4 | Which wording should Rule 01.11's reason take? | (c) the creative director's recast | No |
| Q5 | Should the studio draw the four pillar icons on whole pixels at 16 and 24 px? | (a) draw pixel-fit versions | Yes |
| Q6 | Should the studio draw a set of utility icons? | (a) draw about eighteen | Yes |
| Q7 | How should the studio settle the domes and columns in six icons? | (a) redraw those parts | Yes |
| Q8 | How small may topic and atlas symbols go? | (a) a 48 px floor | No |
| Q9 | Which drawings become our topic set? | (a) Civic Line's 72 | No |
| Q10 | Should a part opener carry a pillar icon? | (a) no pillar icon on a part opener | No |

## For the main session

- Every "where it lives" link and every "Open in the published page" link points at `https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF#<anchor>`, and the builder checks each anchor against the after page. Anchors such as `lockmark`, `rule-11-1` and `fig-s-01-uneven` exist only once the published chapters page is republished from the after page. The board's cover says the after page is the copy the studio will publish.
- Q3's recommendation rests on the creative director's condition that the board show both drawings at 96 px and display size. The board meets it with a plate of its own, and its caption says the board builder drew it from the two files.
- The CD's two notes for the next pass (CD-N8, Rule 04.6's "a little taller"; CD-N9, Rule 08.2's place labels on the frame) print under "Left open after the recheck".

## Tested

- `python3 -I work/build/scripts/phase-2/apply_pass_board_build.py --strict --before <the 3130c5b page>`: exit 0 with no warnings. 50 views and 3 plates captured with 0 errors, 5 plates copied from the identity designer's renders; every view's anchor and find text found on its page; every "where" anchor found on the after page; no em dash, en dash or flagged word on the board; every image the board references exists, and no capture sits unused.
- `node work/build/scripts/phase-2/dataviz_check.js <board> --board`: PASS, 0 failures at 1,440, 390 and 360 px, run once with captures and again with `--no-captures` after the last build. At every width: no sideways scroll, smallest text 13 px, no contrast failure, no red mark, axe-core 4.10.2 with no violations, 40 focus stops at 1,440 px each with a visible ring, fonts Inter, Inter Tight and Lora loaded.
- Size: the board's HTML and the 58 images it references come to 7,604,779 bytes, 7.60 MB.
- The reply box, by script in Chromium: the sample shows until a mark is made; marking Q1 (a) with its name box and Q4 (b) with a note gives "Q1: as recommended (a). Approved by name." and "Q4: (b) the editor’s one sentence. Keep it short."; the marks survive a reload. All 105 links to the published page carry the published address, and every link inside the board reaches an element on it.
- Looked at by me in Chromium, from my own renders: at 1,440 px the cover, the scores, B6-1, DR-128, A1, A3, A15, the review, all four decision cards, stage B's table and first cards, Q10 and the reply box; at 390 px the cover, B6-1, DR-128, the pillar row's phone pair, the review table, Q1, Q3 and Q4. Every capture on contact sheets after the first build, and again for each capture I re-cropped; the L6, end mark, larger sizes and masters plates at full resolution. These looks led to fixes: view crops that cut rows or showed the wrong row (A10, A12, A13's example, A15, B6-1's nine stages, DR-128), A14's view landing on the first row because a visually hidden description held the same words (the capture script now skips hidden text), change cards that fell to one column because the 916 px views missed a 914 px column, a "lowest, of 5" label that wrapped, the hint's wording, a plate that scrolled inside its decision card, and table spacing.
- The board's words, read by me in full against chapter 02's rules, from the visible text the builder writes. This led to rewrites of the scores' open items into full sentences, a passive in the review's opening, an ambiguous "its" and "the other choice", two claims the sources did not hold (Q8's second sentence and Q3's "the one candidate a shrunk card keeps", since the 24 px master doubled also holds up), and Q3's larger sizes caption.
- Quoted wording checked against its source: Rule 01.11's approved reason against the after page, the editor's sentence against the editor's notes, the creative director's recast against the review; DR-124's three sentences and H10's line against the decision log; the 28 Should fix items against the three reviews and the four fix pass sections.

## Not tested

- The board in Safari, Firefox or on a real phone, with a screen reader by ear, at 200 percent text, in forced colors or in print.
- The published links themselves. The chapters page at that address has not been republished from the after page yet, so I could not open the new anchors there.
- The board at 360 px by eye; the check covered it by script.
- Whether every rewrite on the board avoids every pattern chapter 02 lists. I read each line, and no script can rule out a triplet or a parallel run.
- The captures' faithfulness beyond what a look shows: they are Chromium renders of both pages at device scale 2, and JPEG at quality 80 softens fine lines a little.
- The facts behind the changes. I took them from the decision log, the change ledger, the owners' notes, the research report and the reviews, and checked none against a primary source.

## Change log

Created:
- `work/build/scripts/phase-2/apply_pass_board_build.py`
- `work/build/scripts/phase-2/apply_pass_board_capture.js`
- `work/boards/phase-2/apply-pass/20261107_Apply-Pass-Board-Content.json`
- `work/boards/phase-2/apply-pass/20261107_Apply-Pass-Changes-Board.html`
- `work/boards/phase-2/apply-pass/20261107_Apply-Pass-Changes-Board-Check-Results.json` (written by the check)
- `work/boards/phase-2/apply-pass/captures/`: 50 JPEG captures and 8 PNG plates named `20261107_Apply-Board-*`, and `20261107_Apply-Board-Capture-Facts.json`
- `work/handoffs/phase-2/20261107_Apply-Pass-Board-Builder-Notes.md` (this file)
- Outside the repository: the before page, my renders and the publish copy in my scratchpad

Modified: none. I left the chapters page, the identity designer's plate folders, the scores file, every ledger and every other owner's file as I found them.
