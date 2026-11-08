# Creative director's review of the Q1 to Q4 pass

Oath & Action Edition 06, Phase 2, November 8, 2026. Written by the creative director (`.claude/agents/oa-creative-director.md`), scored on the six criteria in Master Brief section 6. Page reviewed: `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` at commit b63d82b5, after the identity designer's work and the editor's copy edit. I compared it with the page I signed off (commit a8599c6, published unchanged at b8d8e863). I read DR-129 to DR-132, D2-462 to D2-478, the pass brief and the "Q1 to Q4 pass" sections of the identity and editor notes, and I rendered the page myself in Chromium. I changed no other file and committed nothing.

## Decision or verdict

Signed off. Every changed chapter reaches 4 or more on all six criteria, and nothing blocks republishing. Dustin's four answers read on the page as he gave them: L6 has no dots, the end mark stands at the text's cap height, the masthead and the sign-off draw the 48 px master, and Rule 01.11's reason is his wording to the character.

One thing went backward. Insetting Rule 08.2's labels (my CD-N9) widened the places plate to 802 px, so at 1,440 px it now overflows its frame by 31 px, sits off center and tells the reader to scroll a plate they can already see whole (CD-S9). A second gap is new too: Rule 03.2's Files list dropped the October L3 master, so no listed L3 file serves print or any width but 282 px (CD-S10). Both are Should fix.

## Scores

| Chapter | Craft | Clarity | Brand fidelity | Usefulness | Evidence honesty | Accessibility |
|---|---|---|---|---|---|---|
| 01 Purpose | 4: only the reason changed; it sets in four lines at 1,440 px and five at 390 px, with no lone last word | 4: the reason now opens on what the reader sees, a case from each party; the Track card still runs long on a phone | 5: DR-132 appears once, character for character, and the old first sentence appears nowhere on the page | 4: the builders note still says to count the atlas's case records by party first | 4: "the finding stands as the record shows it" stays; the count by party waits for stage B | 4: the reason is plain text, and the owners' guide check passes |
| 03 Identity | 4: L3's 48 px lockmark lands on whole pixels on the lockup sheet and in all of Rule 03.6's mastheads; at its 196 px minimum L3 still draws the 24 px master at 34 px, whose rows part | 4: Rule 03.4 defines the end mark where the guide first names it, and L6's caption says what closes a narrower page | 4: DR-129 and DR-131 read as approved; L3 shows two lockmark weights in one chapter until Dustin answers D2-478 | 4: the masthead master's size, spacing and file are exact; no file is named for L3 in print (CD-S10) | 4: every L3 figure (282 by 48, 13 px, 48 px) matches the master file | 4: L6's and L3's alt texts describe what the plates now draw |
| 04 The Ampersand and the hinge | 4: B stands 14.1 px beside 12.4 px capitals at 17 px; its place moves 1 px with the line's position (CD-N10) | 4: the figure replaces "a little taller", so CD-N8 is closed | 5: DR-118 and DR-130 hold: B measures 1.14 cap heights tall at every text size I tried, 15 to 28 px | 4: `height: 0.831em` and `vertical-align: -0.052em`, with the sizes they hold for, can be pasted | 4: the 17 px figures match my rerun; the 19 px row prints one of two positions 1 px apart | 4: B stays `aria-hidden`, so a screen reader ends on the last word |
| 08 The lockmark | 4: every place is crisp at 1x with labels inset 16 px; the places plate now overflows the 1,440 px column (CD-S9) | 5: "It has four masters" and the list of places say which master each place draws | 5: the 48 px master equals the approved proposal apart from its title, and each place shows nine nodes and one red lever | 4: the feed test gives thresholds, filter and counting box; the sign-off's print master is unnamed (CD-S10) | 4: the feed figures match my rerun within one red pixel; "the four places read at one weight" overstates 42 against 22 percent ink (CD-N11) | 4: the scroll region is labeled and focusable; at 1,440 px its "Scroll sideways" label describes a plate that fits |
| Identity proofs | 4: the card's lockmark sits at whole pixels (1,079 and 509 in the card) with no soft pixel at 1x | 4: the new "Feed test" row says what passed and at which widths | 5: one lockmark in each view, drawn from the approved 48 px master | 5: a builder can copy the card from its rows, pass figures included | 4: the figures come from the built card and match my rerun within one red pixel; the card stays labeled Illustrative once | 4: the specifications are text, and the owners' guide check passes |

Lowest by criterion: Craft 4, Clarity 4, Brand fidelity 4, Usefulness 4, Evidence honesty 4, Accessibility 4.

## Reasons

### Items closed by name

| Item | Closed? | What the page shows |
|---|---|---|
| CA-S1, the lockmark drawn at two weights | Yes, with one residue that D2-478 already carries | The hairline square is gone from the masthead and the sign-off. All ten correct 48 px lockmarks on the page, at 1,440 and 390 px at 1x, draw the same 507 ink pixels with none off the palette. Rule 08.1 says in words that the 16, 24 and 48 px masters draw heavier nodes, and Rule 08.3 names what stays the same. The residue is L3 at its 196 px minimum, where the 24 px master at 34 px still reads as a dense block. |
| CA-S2, the sign-off on a card a feed shrinks | Yes | Rule 08.2's specifications now hold the test in plain words. I reran it on the card as the page draws it: 8 of 8 nodes at both widths, and 10 and 5 red pixels at 500 and 360 px with Lanczos (the page prints 11 and 5), with the same pass under bicubic, bilinear and box filters. The signed-off card, drawn with the display master, fails under all four. |
| CD-N8, Rule 04.6's sentence | Yes | "In 17 px body text it is 14.1 px tall beside capitals 12.4 px tall." |
| CD-N9, Rule 08.2's place labels | Yes, with a side effect | The labels stand 16 px in from the frame. The fix widened the plate past the column (CD-S9). |

### What did not go backward

A text diff of chapters 01, 03, 04, 08, the proofs and their alt text against the signed-off page shows only the intended changes, and the rest of the page differs only in its build stamp. The 48 px master file matches the approved proposal apart from its title. No em or en dash appears in the five chapters or their alt text.

## Required changes

### Must fix

None.

### Should fix

- **CD-S9, chapter 08, `s-08-2-correct` (engineer, shell).** The 802 px plate plus the scroll frame's 48 px side padding needs 898 px in an 867 px column. Let the shell drop a frame's side padding to 32 px when that makes a plate fit, and mark a plate "Wider than this column" only when it still does not. The places plate then sits whole and centered at 1,440 px, with no hint and no tab stop.
- **CD-S10, chapters 03 and 08 (identity designer, then the editor).** Name the file for each size the rules allow. Put `20261028_L3-Horizontal-Master.svg` back in Rule 03.2's Files and add one line to its builders note: the masthead master serves the 282 px masthead, and the October master serves print and other widths until stage B draws a print L3 at the masthead's proportion. In Rule 08.2's sign-off row, say which master prints at 0.50 in. I recommend the display master, since the 48 px master is built row by row for a screen's pixel grid.

### Notes

- **CD-N10, chapter 04.** Chromium snaps B to whole pixels and the text's baseline on its own, so B sits 0.6 or 1.6 px over the cap line by where the line falls. The Charcoal sample at 1,440 px shows 1.6 px over and 0.1 px under. Add to the "At 17 px text" and "At 19 px text" rows: "A screen may move B 1 px up or down as it rounds to whole pixels; its height stays the same."
- **CD-N11, chapter 08, Rule 08.2's reason.** Replace "the four places read at one weight" with "the four places read as one mark at the size each one sets". The 24 px master still covers 42 percent of its field against 22 percent for the 48 px master.
- **CD-N12, chapter 08, the feed test.** It counts near-black nodes, so it cannot judge a Charcoal or Prussian card. State a light-node version (every channel over a measured floor) and run it on one dark card, or limit the sentence to light cards for now.
- **CD-N13, chapter 01, Rule 01.11's failure plate.** It shows Texas alone but keeps the California sources in its source line. Give it the Texas source alone, as a piece that dropped California would print. This predates the pass.

## Risks for Dustin to weigh

- **The 48 px master on a sharp screen.** At 1x it is exact. On a 2x screen each 7 px node doubles into a stepped shape, which the masthead shows up close.
- **The feed margin.** At 360 px the lever keeps 5 red pixels against a floor of 4. A platform's JPEG compression could take it under, and no real feed was tested.
- **L3 at its minimum.** Until you answer D2-478, L3 at 196 px draws a striped, heavier lockmark than the masthead.
- **L6 without dots.** The wordmark and tagline now sit about 10 px above the strip's middle while the lockmark sits on it. Centering them changes L6's proportion, so it would need your approval by name at stage B.

## Tested

- The page in Playwright Chromium at 1,440 and 390 px, at 1x and 2x, with the sticky header released for captures: Rule 01.11; the lockup sheet, L6 scrolled to both ends, Rule 03.4's minimum plate and table, Rule 03.6's two plates; Rule 04.6's correct plate; Rules 08.1 and 08.2's plates and specifications; the proofs' masthead and social card. The signed-off page's versions of the same plates, for comparison.
- DR-132 against the page by script: one exact match, and the old first sentence absent from the whole file.
- Every 48 px lockmark on the page at 1x at both widths: ink, near-black, red and off-palette pixels counted.
- The 48 px master against the board's proposal, by diff with titles removed.
- The end mark at eight times beside an inserted capital H, in my page instance only: both Rule 04.6 samples at both widths, at 1x and 2x, and at 15, 17, 19, 20, 24, 27 and 28 px text with four sub-pixel offsets.
- My own feed test on the card captured at 1x from both pages, four filters, 500 and 360 px, with enlarged views.
- Scrolling frames in the five chapters at 1,440 and 390 px, before and after; B's `aria-hidden`; the places plate's tab stop and label.
- A whole-page text diff, and an em and en dash count in the five chapters and their alt text.

## Not tested

- The strict build, the guide check and the token tests. The guide check rewrites captures in the board folder, and this task allows no other file change, so I rely on the owners' runs.
- 1,024 and 360 px by eye.
- Firefox, Safari, a Windows scrollbar on the places plate, real phones, screen readers by ear, forced colors, 200 percent zoom and print.
- A real feed upload and JPEG compression.
- The 48 px master and the new L3 in a PDF or on paper; L3's email PNG, which does not exist yet; the letterhead PDF.

## Change log

- Created `work/handoffs/phase-2/20261108_CD-Review-Of-Q1-To-Q4-Pass.md` (this file).
- Scratch captures and scripts sit in my session scratchpad only.
- No guide file, board, ledger or source file changed, and nothing was committed or pushed.
