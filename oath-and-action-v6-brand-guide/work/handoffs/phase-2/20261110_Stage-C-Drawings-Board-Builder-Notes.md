# Drawings board C: builder's notes

Oath & Action Edition 06, Phase 2, November 10, 2026. Written by the board builder, working as the engineer (`.claude/agents/oa-engineer.md`) with the design director's layout judgment (`.claude/agents/oa-design-director.md`), for the main session, under `20261110_Drawings-Board-C-Brief.md`, "The board builder". I published nothing, committed nothing and pushed nothing. Paths are relative to `oath-and-action-v6-brand-guide/`.

The board was built first while the creative director scored (every card marked "Scores pending"), again when the scores file landed with Housing option B at Clarity 3, and last on the final scores (all five cards ready) and the icon designer's fix round, which withdrew B. Every figure, reading, pick and score on the board is from that last run.

**To open:** `work/boards/phase-2/stage-c/drawings/20261110_Stage-C-Drawings-Board.html`.

**To publish:** `/tmp/claude-0/-home-user-Dustin-s-Command-Center/67af6aec-b8e0-5b79-b000-c172e734e753/scratchpad/stage-c/board/publish/20261110_Stage-C-Drawings-Board.html`, with `files.json` beside it mapping its 181 files to `img/`. It has no document skeleton and sets `lang="en"` by script, as the stage B board's copy does (D2-317). The page and its files come to 2.58 MB.

## What the board holds

- **Cover.** What Dustin is choosing, how to answer, the sample reply "All as recommended, and I approve every card by name.", a key (1x and 2x screens, as a 1x screen draws it, the switch, full ink, the pixel-fit check, the look-alike figure, the open pixel, the naming test and scores) and an index of the five cards.
- **Card 1, Housing.** Options A and C at 128, 48 and 24 px, the red edition and the black on Newsprint, the red edition and one color on Charcoal, from their own SVG files. Each option prints what it shows, the creative director's naming reading and verdict, the icon designer's verdict, the creative director's note, its closest settled drawing, its figure against CL-054 Home Equity and against the other option, and its six scores. "Why two options" prints B's withdrawal in the icon designer's words. Below sit the five settled neighbours the manifest names (CL-054, CL-053, CL-063, R-30, CL-051) at 128, 48 and 24 px, each with both options' figures against it, then the 24 px question: each option as a 1x and a 2x screen draws it, the recommendation to keep Housing at 48 px and up for now, and a second answer group for it.
- **Card 2, the 16 px Pause and Filter.** The approved Pause and its redraw; the approved Filter and options A and B. Each at 16 px as a 1x and a 2x screen draws it on Newsprint and Charcoal, then the 1x picture ten times larger with a pixel grid on both grounds. Each prints its open pixels, the ink across the opening 8 px down (the creative director's "row 8"), the pixel-fit check at 16 px with the 1.5 px line, and for each redraw the creative director's naming reading and six scores.
- **Card 3, the 37 fits.** At the head: this run's summary, the creative director's scores for the set, and the five look-alikes' ten pairs as masters and as fits. Then one compact row per drawing in chapter 10's order: ID, word and atlas ID; the master and the fit at 24 px as a 1x screen draws them and the master as a 2x screen draws it; full ink, master to fit, with pixel counts; the pixel-fit result; the creative director's verdict; a "Hold back" box. The five look-alikes carry a Look-alike mark and their four figures before and after; R-06 carries its two flags, its masters' own figures and one line that the studio settled it apart from the board. One answer, "All 37, with the switch", approves the set; ticking any row's "Hold back" switches the answer to "All but those I hold back" and the reply names each one.
- **Card 4, a print L3.** What it gains and what it costs side by side; at 282 px the masthead master, the October master and the proposal; at 48 px capitals the October master and the proposal; the two over each other (October in Stone); both White files on Prussian; links to the print proof PDF and the identity designer's plate capture; the proportions and 1.55 in figures from the figures file.
- **Card 5, the social sign-off.** Gain and cost; today's card and the proposal at actual size, 1,200 by 630 px, and the proposal on Charcoal; each card as a feed draws it at 500 and 360 px on Newsprint and Charcoal, with nodes, red pixels and the lockmark's size against its 16 px floor; the corner four times larger at each width and after the shrunk JPEG; the mark alone at 48 and 96 px; the width and thumbnail figures.
- **Your reply.** The Prussian panel: one line per card with its answer buttons, the recommended answer named, card 3's "Held back" list and an "I approve by name" box, then the reply box and a copy button. Marks save in the viewer's browser only, inside `try` and `catch`.

## How to rebuild, check and publish

```
python3 -I work/build/scripts/phase-2/stage_c_drawings_board_build.py --strict
node work/build/scripts/phase-2/dataviz_check.js /tmp/claude-0/-home-user-Dustin-s-Command-Center/67af6aec-b8e0-5b79-b000-c172e734e753/scratchpad/stage-c/board/check-copy/20261110_Stage-C-Drawings-Board.html --board
```

The build takes about 25 seconds. It reads the content file (the board's own words), the scores file, the three manifests, the inventory in use, chapter 10's section 10, both designers' notes (their recommended answers only, and B's withdrawal reason), the identity figures file and the identity designer's plates. It runs the likeness check and the pixel-fit check on today's files into `<scratchpad>/stage-c/board/checks/` (`--reuse-checks` skips them for layout work and warns), makes the board's pictures in Chromium, and writes the board, `20261110_Stage-C-Drawings-Board-Figures.json`, `renders/`, the check copy with absolute file links and the publish copy with `files.json`. `--strict` exits 1 on any warning, among them "scores pending", a card the creative director has not signed off, a score under 4, a row with no verdict, a withdrawn option with no reason, a stated recommendation that differs from the designer's notes, an override that matches nothing, a decision number outside the footer, a flagged word or an en dash. An em dash, a misquoted tagline or a page over 15 MB stops the build.

To publish, hand the publish copy and its `files.json` to the Artifact tool. For the editor: words taken from other owners' files go through `editor_overrides` in the content file, as on the stage B board; it holds two entries now (below).

## Routine calls

- D2-xxx | The board prints the likeness and pixel-fit figures and the full-ink shares from this run's checks on today's files, never from the notes | The brief's rule; I compared the results with the notes afterwards, and they agree
- D2-xxx | The likeness check runs once on the 37 fits with every pair listed (`--watch 0.01`), and the board takes the watch line from that run's 95th percentile | One run gives the fits' own-master figures, their closest drawings, their flags and every pair among the fits; the flag and watch lines stay those of the default run
- D2-xxx | The masters' figures come from one run of copies under neutral names: the five look-alikes and every master a fit is flagged beside (R-06, R-41, R-44) | The check compares two masters only as new drawings; this is the icon designer's own method
- D2-xxx | Full ink is the pixel-fit check's soft-edge count at 1x: pixels at alpha 247 or more among pixels at 8 or more | The measure the icon designer describes, from the check the brief names
- D2-xxx | Open pixels are counted on the board's own 1x pictures in the rows where the opening runs at its narrowest between straight sides, with the opening found from a 16 times picture | A rule read from the drawing, not a band typed into the script; it gives rows 4 to 11 in each Pause bar and 8 to 11 down the spout, as the designer counted
- D2-xxx | Each file prints the ink across the opening on the row 8 px below the top of the box | The creative director's Should fix ("row 8"), and the same row for every file
- D2-xxx | Every view that claims to show a 1x or 2x screen is a PNG made in this run at device scale 1 or 2 from today's file and set at its own CSS size with `image-rendering: pixelated`; a 2x picture therefore shows at twice the drawing's size and says so | The brief's section "Showing what a 1x screen draws"
- D2-xxx | The board's pictures live in `renders/` beside the board, 141 PNGs, remade on every run | The 1x rows need pictures of single masters, which no maker made; a folder keeps the page light
- D2-xxx | Housing's options, its neighbours and the L3 and lockmark drawings at true size draw from their own files, the Civic Line ones as images and the identity ones inline | D2-617 and D2-565; the identity files draw in currentColor and the page's custom properties, which only an inline drawing takes
- D2-xxx | An option the manifest marks withdrawn leaves the card, its checks and its scores, and the card prints the designer's sentence after "B is withdrawn." under "Why two options" | The creative director's Should fix and the stage B short cards (D2-622)
- D2-xxx | Housing prints each option's six scores from the scores file's `option_scores` | The brief asks for each option's scores, and the creative director scored per option
- D2-xxx | Each card shows the designer's recommendation in the board's words with this run's figures, and the creative director's beside it; the reply marks the creative director's as recommended | The designers' notes carry figures the board must not copy; the build reads only their recommended value and warns if the board's words differ
- D2-xxx | Card 3 is one row per drawing with one "All 37" answer and a "Hold back" box on each row; a hold switches the answer to "All but those I hold back", and choosing "All 37" clears the holds | The brief's compact rows and a way to hold any back by name
- D2-xxx | R-06's row prints its two flags with its masters' figures and one line that the studio settled it; no question about it is asked | D2-1237
- D2-xxx | Decision numbers appear only in the footer; two in the creative director's score reasons go through `editor_overrides` ("as the pillar fits do (D2-613)." and "which dark mode (DR-204) now needs") | The brief's rule on studio codes; the scores file stays as its owner wrote it
- D2-xxx | A drawing ID such as CL-054 never breaks across two lines | A line break inside "R-30" read as two words at 1,440 px
- D2-xxx | The print L3 card draws the files at the masthead's 282 px, at 48 px capitals, over each other and on Prussian, and computes its sizes and the 9.1 percent from the figures file's units | Gate rule 4's actual sizes; the figures stay the identity designer's
- D2-xxx | The cost line names the lockmark's 0.25 in print minimum, and the build checks chapter 08 still says so | A rule value, not a measurement, kept true to the chapter
- D2-xxx | The social cards at actual size are pictures of the identity designer's plate made in Chromium at device scale 1 and 2, clipped to the card's own box on whole CSS pixels and set through `srcset`; the build checks the heading above each card and that Inter loaded | The brief takes the cards from the plate; each screen draws its own picture at true size
- D2-xxx | The designer's eight-times corner pictures are set at half their pixel size and labeled four times | Each reduced pixel stays an exact block (8 by 8 device pixels on a 2x screen), and the card is half as long
- D2-xxx | The 360 px captions say the lockmark is under or over its 16 px floor | The creative director's Should fix
- D2-xxx | A figure in the creative director's words that neither this run nor the identity figures file holds is reported as a notice in the build, not a warning | They are the creative director's words; on the final run there is none
- D2-xxx | Marks key to a hash of the cards and their answers; the PDF and the two plate captures travel in `img/` | A rebuild with changed answers starts clean (D2-316); the links work in the published copy

## Tested

- `python3 -I work/build/scripts/phase-2/stage_c_drawings_board_build.py --strict` on the final scores and today's files, with fresh checks: exit 0, no warning, no notice. 5 cards; the page is 335 kB and its 181 files 2.24 MB, 2.58 MB in all. No em dash, en dash or flagged word on the board, and no decision number outside the footer.
- The checks' exit codes as expected: pixel fit on the fits 0 (37 of 37 pass at 1x and 2x), on the masters 1 (0 of 37 pass at 24 px), on the five 16 px files 0 (all pass); likeness on the fits 1 (R-06 against R-41 0.917 and R-44 0.915, its masters 0.937 and 0.964; 16 more to watch), on Housing 0, on the neutral masters 1 (the five's own flags).
- This run's figures against the designers' notes, compared after the build: full ink 0% to 8.3% in the masters and every fit pixel at full ink; the ten look-alike pairs (CL-028 and R-27 0.958 to 0.861, down to R-27 and R-45 0.802 to 0.717); open pixels, none in either approved file, 8 of 8 rows in each Pause bar, 3 of 4 and 4 of 4 down the Filter spouts; Housing A closest CL-051 0.690 and CL-054 0.501, C closest CL-022 0.656 and CL-054 0.270, A against C 0.431. All agree.
- `node work/build/scripts/phase-2/dataviz_check.js <check copy> --board`: PASS, 0 failures at 1,440, 390 and 360 px. At every width: no sideways scroll, smallest text 13 px, no contrast failure, axe-core with no violations, 16 red marks all under `data-red` and no working-red job, fonts Inter, Inter Tight and Lora loaded; 40 focus stops at 1,440 px, each with a visible ring.
- By script in Chromium: every image loads at 1,440, 390 and 360 px, nothing runs past the window outside a labeled frame, and no page error. At 390 px five frames scroll at true size (the L3 rows at 48 px capitals, the overlay, Prussian, the cards at actual size, the feed views); at 360 px the 282 px row too.
- The reply, by script: the sample shows until a mark; marks give "Card 1, Housing: option A; Housing at 48 px and up for now, as recommended. Approved by name." and "Card 3, The 24 px fits for the 37: the fits with the switch, all but CL-039 Feed Ranking and R-06 On-Cycle Elections, which I hold back. Approved by name."; a mark on a card shows on its panel line and the reverse; holds switch the answer and show in the panel; "All 37" clears them; marks survive a reload; with storage blocked the page works with no error.
- The publish copy in Chromium: 211 images, none broken, `lang="en"`, the three links resolve under `img/`; `files.json` maps 181 files.
- The social card pictures: 1,200 by 630 and 2,400 by 1,260 px, each under its expected heading, with Inter loaded.
- Looked at by me in Chromium at 1,440 px: the cover and every card, card 1 again after B's withdrawal; at 390 px card 1, card 3's head and first rows, and the reply panel. These looks led to fixes: blank images in my own screenshots (decoding; the check found none), a 631 px card picture, eight-times corners stacking into a long column, a line break inside "R-30", columns out of line where an option has no chip, "100% or more" in the summary, and the Housing lede after B left.

## Not tested

- Safari, Firefox, a real phone, a real 2x screen, a screen reader by ear, 200 percent text, forced colors and print. The board was checked in Chromium at device scale 1 only.
- That a 1x screen in every browser draws the half-size corner pictures as exact four-times blocks; on a 2x screen they map pixel for pixel.
- The board at 360 px by eye; the check covered it by script.
- `dataviz_check.js` on the board file itself with `--no-captures`; it ran on the check copy only, as the brief asks.
- The PDF and plate links inside a published artifact.
- Whether my words pass every pattern chapter 02 lists; no editor has read the board.
- The creative director's scores, readings and verdicts and the designers' words; the board prints them as their owners wrote them, with the two overrides above. The withdrawn Housing B, which the board no longer shows.

## Change log

Created:
- `work/build/scripts/phase-2/stage_c_drawings_board_build.py`
- `work/boards/phase-2/stage-c/drawings/20261110_Stage-C-Drawings-Board-Content.json`
- `work/boards/phase-2/stage-c/drawings/20261110_Stage-C-Drawings-Board.html`
- `work/boards/phase-2/stage-c/drawings/20261110_Stage-C-Drawings-Board-Figures.json`
- `work/boards/phase-2/stage-c/drawings/renders/` (141 PNGs, remade each run)
- `work/handoffs/phase-2/20261110_Stage-C-Drawings-Board-Builder-Notes.md` (this file)
- Outside the repository, in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/67af6aec-b8e0-5b79-b000-c172e734e753/scratchpad/stage-c/board/`: `checks/`, `measure/`, `render/`, `check-copy/` (with the check results and captures), `publish/` and my test scripts in `tools/`

Modified: none of anyone else's. The main session's snapshot commits took in some of my files while I worked. I left `source/`, `work/ledger/`, every drawing, master, chapter, specimen, plate, existing board, the scores file, the review and the designers' notes and manifests as I found them, and `work/build/scripts/phase-2/stage_b_drawings_board_build.py` untouched.
