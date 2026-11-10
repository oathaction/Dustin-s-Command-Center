# Stage C, round 0: identity designer's notes

Oath & Action Edition 06, Phase 2, stage C, November 10, 2026. Written by the identity designer (oa-design-director, run as a subagent of the main session) under `work/handoffs/phase-2/20261110_Stage-C-Brief.md`, "Round 0 tasks, Identity designer". I read my role file, `CLAUDE.md`, the stage C brief, Master Brief sections 3, 6, 9 to 12, 18 and 19, the creative director's review of the Q1 to Q4 pass (CD-N12, CD-S10, "The feed margin"), D2-465 to D2-469, D2-477, D2-478, D2-482, D2-483, DR-131, DR-180 to DR-182, D2-715, D2-805, D2-965 and D2-1134 in the decision log, my promotion notes and figures, chapters 08 and 09 as their generators write them, and the engineer's opener contract as it landed in `guide_build.py`.

I changed no existing identity master, board, ledger, `source/` or shell file, and no file another owner keeps. The generator chain rewrote one other owner's output, which its own script writes (see the change log). I committed and pushed nothing; the main session's snapshot commits took in some of my files while I worked.

**To rebuild my part:** `python3 -I work/build/scripts/phase-2/stage_c_identity_round0.py feed <scratch>` (about 3 minutes; writes the figures, keys `feed` and `feed_dark`), then `proposals`, then `plates <scratch>`, then the chain below, then `opener <scratch>` on the built page.

## Summary

| Item | Closed in the guide? | What closes it |
|---|---|---|
| CD-N12, the feed test on dark cards | Yes | Rule 08.2 gains a "Feed test, dark card" row with measured floors, and "Feed test, our card" gives the card's figures on Charcoal and Prussian |
| D2-482, a print L3 | No: needs Dustin's named approval | Drawn as new files beside the masters, with comparison plates at actual size and a print proof for board C. The guide keeps the October master for print until he approves |
| The 5 red pixels at 360 px | Partly | Measured: a JPEG of the uploaded card does not lower the count, and Chromium's own downscale passes. A thumbnail saved as a JPEG after shrinking takes all of the lever's red at 360 px, and only a larger lever closes that. Rule 08.2 now asks for the test on the file a builder uploads. The larger sign-off goes to board C as a named approval |
| D2-965, chapter 09's opener | Yes | `s-09-opener` in `manifest-identity.json`, named by `"opener": "s-09-opener"` in chapter 09. The engineer's shell support landed during my work, and the page draws it under the intro |

## 1. The feed test on a dark card (CD-N12)

**The problem.** Rule 08.2's test counts near-black nodes, so it cannot judge a card on Charcoal or Prussian, where the nodes are light. On a dark ground the links also take the nodes' own color (Newsprint on Charcoal, White on Prussian, Rule 03.5), so a link crossing a node's square can leave a light pixel too. On a light ground the links are Stone and never reach the near-black threshold.

**What I built.** `stage_a_identity_proofs._social` now takes a surface, so the guide's own link-preview card can be drawn on any approved ground; its Newsprint markup is byte for byte the same (checked against HEAD's function). `stage_c_identity_round0.py feed` captures the card on Newsprint, White, Charcoal and Prussian at 1x in Chromium, checks that each card draws the 48 px master tile at 1079, 509 pixel for pixel, and measures:

- **The floor.** For each dark ground I drew the 48 px master with its links alone, no node and no lever, and took the brightest pixel those links leave in any node's square, then the dimmest node's brightest pixel with the whole master. At the rule's two widths under Lanczos, bicubic, bilinear and box reductions:

| Ground | Links alone, brightest low channel | Weakest node, brightest low channel | Floor, halfway, rounded down to 5 |
|---|---|---|---|
| Charcoal, at 500 and 360 px | 146 and 125 | 210 and 165 | 155 |
| Prussian, at 500 and 360 px | 180 and 156 | 255 and 203 | 190 |

  One floor cannot serve both: Charcoal separates between 146 and 165 and Prussian between 180 and 203. Each floor sits about 71 percent of the way from its ground to the node's color (0.714 and 0.710), close to the light test's 70, which sits 74 percent of the way from Newsprint to Charcoal. Across every width from 300 to 600 px no node ever falls to the links' level on either ground, though the links reach 162 on Charcoal and 199 on Prussian at the wider widths, so the floors hold for the rule's two widths, which is what the rule tests.
- **The light test's 70 checked the same way.** The links alone never leave a pixel under 70 on Newsprint or White at any width from 300 to 600 px under any filter: the darkest is 135 on Newsprint and 146 on White.

**Results at the rule's widths, Lanczos** (nodes kept, red pixels):

| Ground | 500 px | 360 px |
|---|---|---|
| Newsprint, as the built page draws it (promotion figures) and as my capture draws it | 8 of 8, 11 | 8 of 8, 5 |
| White | 8 of 8, 10 | 8 of 8, 5 |
| Charcoal, floor 155 | 8 of 8, 11 | 8 of 8, 5 |
| Prussian, floor 190, the White lever as a ninth node | 9 of 9 | 9 of 9 |

Under the other three filters Charcoal and Prussian pass at both widths. White at 360 px loses one node under bilinear (7 of 8); the rule names Lanczos, under which it passes.

**What the page now says** (Rule 08.2's specifications, written through `stage_a_identity_chapters.py`, figures from the figures file):

- "Feed test": the light test as before, with "A test for a card on Charcoal or Prussian comes later" taken out.
- "Feed test, dark card" (new): "On Charcoal, each of the eight light nodes keeps at least one pixel with every color channel over 155, and the lever keeps at least four red pixels, counted as on a light ground. On Prussian, where the lever is White as well, each of the nine nodes keeps a pixel with every channel over 190. On a dark ground the links take the nodes' own color, so each floor sits halfway between the brightest pixel the links alone leave in a node's square and the dimmest node's brightest pixel, measured on our card at both widths"
- "Feed test, our card": the Newsprint figures as before, then "Drawn on Charcoal, the same card keeps 8 of 8 nodes and 11 red pixels at 500 px, and 8 of 8 nodes and 5 red pixels at 360 px. Drawn on Prussian, it keeps 9 of 9 nodes at 500 px and 9 of 9 at 360 px"
- Builders: "Run the feed test on every new template for a social card, on the file you will upload, before it ships."

## 2. The 5 red pixels at 360 px

**Measured** on the same captures (figures key `feed`):

- **A JPEG of the card as uploaded** changes nothing that matters. Saved at 1200 by 630 px at quality 60, 75, 85 and 95, with and without chroma subsampling (the color detail a JPEG keeps at half size), then reduced with Lanczos: Newsprint keeps 11 and 5 red pixels at every setting; Charcoal keeps 9 to 11 and 5; White 10 and 5; Prussian 9 of 9.
- **Chromium's own downscale**, the card as an `<img>` drawn at 500 and 360 px on a 1x screen, the way a browser draws a feed: Newsprint 9 and 5 red pixels, White 8 and 5, Charcoal 8 and 5, Prussian 9 of 9, all 8 of 8 nodes. After a JPEG at quality 80 with chroma at half size: 8 and 5 on each light or Charcoal card.
- **A JPEG saved after the card is shrunk**, as many image services store a thumbnail, is the failure the creative director feared. With chroma at half size the lever keeps 0 red pixels at 360 px at qualities 60 to 85 (2 at quality 95) on Newsprint and Charcoal; at 500 px it keeps at most 1 and 3 at qualities 60 and 75, and 8 at 85. With full chroma it passes from quality 75 (5 red at 360 px). The lever is 2.7 px across at 360 px, smaller than the 2 by 2 blocks a JPEG keeps color in.
- **Neighboring widths.** From 300 to 600 px, Lanczos, the light test fails at 12 widths on Newsprint, all under 333 px (the lever at 3 red pixels, or one node lost at 309 and 320 px); at 22 on White and 17 on Charcoal, which include 341, 346 and 347 px. 360 px sits at 5; 348 to 355 and 363 to 369 px sit at 4.
- **Placement.** Moving the lockmark to every whole-pixel position in a 60 px square, which covers every phase 500 and 360 px give, yields 4 to 7 red pixels at 360 px on Newsprint (29, 32, 37 and 2 percent of positions) and 4 to 6 on Charcoal. The best position for both widths gives 7 and 6. I did not move it: that tunes the card to the test's two widths, the other widths reshuffle, and the thumbnail path still fails.

**What the drawing and the words can do inside the approved geometry:** the words now ask for the test on the uploaded file, which a builder controls and which passes. Nothing inside the geometry keeps red in a shrunk JPEG thumbnail at 360 px.

**The proposal for board C: the social card's sign-off at 96 px**, drawn from the approved 48 px master at exactly twice its size, so every node, link and the lever still land on whole pixels and no new drawing is made. Social cards only; covers, posters and the masthead keep 48 px. On the card the 96 px lockmark stands 2.36 times the wordmark's 40.7 px capitals, between the masthead's 2.18 and the October L3's 2.4, so the two corners keep L3's own proportion. At 360 px it draws at 28.8 px, over the lockmark's 16 px floor, where today's draws at 14.4 px.

| Card | 500 px | 360 px | 360 px, then a JPEG at quality 75, chroma at half size | Widths 300 to 600 px that fail |
|---|---|---|---|---|
| Newsprint, 48 px today | 8 of 8, 11 red | 8 of 8, 5 red | 0 red | 12 of 301 |
| Newsprint, 96 px proposal | 8 of 8, 52 red | 8 of 8, 22 red | 17 red | 0 of 301 |
| Charcoal, 48 px today | 8 of 8, 11 red | 8 of 8, 5 red | 0 red | 17 of 301 |
| Charcoal, 96 px proposal | 8 of 8, 48 red | 8 of 8, 20 red | 16 red | 0 of 301 |

Thumbnail path at every fourth width from 300 to 600 px: today fails at 50 of 76 widths on Newsprint and 48 of 76 on Charcoal; the proposal at none. Its cost: at full size the doubled master shows its steps, 2 px stairs on 14 px nodes, the same stepped look the creative director noted for the 48 px master on a 2x screen, and the corner mark doubles in weight against the wordmark. The display master at 96 px is no answer: its lever is 7.4 px, smaller than today's 9 px.

Plates: `work/handoffs/phase-2/stage-c-identity/20261110_Social-Sign-Off-Comparison.html` (with `-1x.png` and `-2x.png` captures): both cards at actual size on Newsprint, the proposal on Charcoal at actual size, each card at 500 and 360 px as a feed draws it, the sign-off enlarged 8 times at each width and after the thumbnail JPEG, and the mark alone at 48 and 96 px on Newsprint and Charcoal beside the display master at 96 px.

## 3. A print L3 at the masthead's proportion (D2-482)

**Why it needs a named approval.** Since DR-131 the masthead sets L3's lockmark at 48 px beside 22 px capitals, 2.18 cap heights. Print and every other width still take the October master at 2.4 cap heights (D2-482), so L3 prints at one proportion and shows on screen at another. A print L3 at the masthead's proportion changes the printed lockup's geometry, which gate rule 4 reserves for Dustin.

**What I drew.** `lockups/20261110_L3-Horizontal-Print-Master.svg` and `prussian/20261110_L3-Horizontal-Print-Master-Prussian-White.svg`, new files beside the masters, written by `stage_c_identity_round0.py proposals`. Each is the October master with three changes and nothing else, which the script asserts by undoing them and comparing with the source: the nested lockmark drawn at 218.18 units (48/22 of the 100-unit capitals) instead of 240, its top moved from y −66 to −55.09 so it stays centered on the capitals, and the outer view box and the title. The wordmark, the 60 units (0.60 cap height) of space, the lockmark's display drawing, its 1 px links and every color stay. Width 1256.49 units against 1278.31. At 282 px wide the proposal sets 22.4 px capitals and a 49.0 px lockmark, the masthead's proportion; the October master sets 22.1 px and 52.9 px.

**In print.** At L3's 1.55 in print minimum (Rule 03.4) the proposal sets capitals of 3.13 mm and a lockmark of 0.269 in, over the 3 mm capitals and 0.25 in lockmark minimums of Rules 03.4 and 08.1; the October master sets 3.08 mm and 0.291 in. The print proof prints at true size: measured at 300 dpi, the ink of each pair at 1.55, 2.5 and 4 in boxes runs 1.533, 2.47 to 2.48 and 3.96 in wide, the difference being the lockmark field's own inner margin.

Plates: `work/handoffs/phase-2/stage-c-identity/20261110_Print-L3-Comparison.html` (with `-1x.png` and `-2x.png`): at the masthead's 282 px beside the masthead master; the pair at 16, 24, 48 and 96 px capitals with left edges together; display size with an overlay (the October master in Stone, the proposal over it in Charcoal and red); the four approved surfaces; one color on Newsprint and Charcoal; 1.55 and 2.5 in. `20261110_Print-L3-Comparison-Print.pdf` (with its HTML) prints both at 1.55, 2.5 and 4 in on US Letter.

**After approval**, in one pass: `stage_a_identity_lib.L3` gains the print key; Rule 03.2's Files and builders text, Rule 03.6's "In print" row and Rule 08.2 name the new file; the minimum sizes record takes its figures; the October master stays as the record.

## 4. Chapter 09's opener figure (D2-965, D2-1134)

**What I built.** `s_09_opener` in `stage_b_identity_ch09.py`: the 48 px pillar row from Rule 09.1's sheet (`row(48)`), on Newsprint, one color in the surface's icon ink token, each icon from the sprite with `data-icon-family="pillar"`, with no tag and no padding of its own (the shell keeps 24 px between a flowing stage and its keyline, its B1 rule) and no `width_px`, so it flows in the column. Rule 09.1 itself places the 48 px row "near the top of a page that introduces the four pillars". The chapter's JSON carries `"opener": "s-09-opener"` after the intro, and `stage_a_identity_chapters.specimens_used` now counts a chapter's opener, so the identity build stops if the opener names a missing specimen.

**The shell.** The engineer's support landed while I worked: `guide_build.py` renders the opener as a `plate--opener` figure under the intro, before the rule index. The strict build places it and warns about nothing.

**Measured in the built page** (Chromium, device set to dark, which the guide ignores as it should: `data-oa-theme="light"` and a Newsprint stage at every width):

| Width | Figure, px | Stage, px | Lines | Overflow |
|---|---|---|---|---|
| 1440, 1x and 2x | 866.7 wide | 770.7 by 96 | 1 | none |
| 1024 | 702 | 606 by 156 | 2 | none |
| 768 | 704 | 608 by 156 | 2 | none |
| 390, 2x | 350 | 358 by 284 | 4, stacked | none |
| 360, 2x | 328 | 328 by 284 | 4, stacked | none |

Words 22 px bold from 48em and 19 px on phones, icons 48 px, no scroll hint, no fit switch, no sideways page scroll. At 1440 by 900 the row stands on chapter 09's first screen (its stage ends at 852 px), which is what the creative director's S16 asked for. The one-line row needs 592 px; where the column gives less, from 48em to about 1,080 px, the row wraps two and two after an arrow, as Rule 09.1's own 48 px rows do at 1024 px (checked: both rows of Rules 09.1 and 09.2 set two lines at 1024 and one at 1280 and 1440).

## Routine calls

- D2-xxx | The feed test on a dark card counts light nodes, each keeping a pixel with every channel over a floor, 155 on Charcoal and 190 on Prussian; on Charcoal the lever counts red pixels as on a light ground, and on Prussian the White lever counts as a ninth node | CD-N12 asked for a light-node version with a measured floor; Rule 03.5 makes the lever White on Prussian
- D2-xxx | Each dark ground takes its own floor, set halfway between the links alone and the weakest node at the rule's two widths under four filters, rounded down to 5 | On a dark ground the links take the nodes' color; Charcoal separates between 146 and 165 and Prussian between 180 and 203, so no single number fits both
- D2-xxx | The dark test runs on the proofs' card drawn on Charcoal and Prussian by its own generator (`_social(surface)`), not on a new guide specimen | The card and its lockmark are the same pixels (asserted); a second 1200 px card in the proofs would add a plate no rule asks for
- D2-xxx | Rule 08.2 prints the dark figures from `20261110_Stage-C-Identity-Figures.json`, key `feed_dark`, read by `stage_a_identity_lib.figures`; the Newsprint figures stay the built page's from the promotion | D2-469 and D2-805: figures come from a file, and a stale or missing one shows a marker
- D2-xxx | Rule 08.2's builders text asks for the test on the file a builder will upload | A JPEG of the full card leaves the counts as they are, and the uploaded file is what a feed reduces
- D2-xxx | The lockmark keeps its place in the card's corner | Placement moves the 360 px count between 4 and 7, tuning to the test's two widths reshuffles the others, and it does not help the thumbnail path
- D2-xxx | The thumbnail risk goes to board C as a named approval, the social card's sign-off at 96 px from the 48 px master at twice its size | Only a larger lever keeps red in a shrunk JPEG; the size of an approved place (DR-131) is Dustin's to change
- D2-xxx | The print L3 goes to board C as a named approval, drawn as new files beside the masters; the guide keeps naming the October master for print | It changes the printed lockup's proportion from 2.4 to 2.18 cap heights (gate rule 4)
- D2-xxx | The print L3 is the October master with only the lockmark's size and position, the view box and the title changed, asserted by the script; the space stays 60 units | D2-477 describes the masthead's change as the lockmark alone and records its 13 px as 0.60 cap height
- D2-xxx | The comparison plates go to `work/handoffs/phase-2/stage-c-identity/` with captures at 1x and 2x and a print PDF, for the board builder | Boards are closed to me; the board builder makes board C
- D2-xxx | `s-09-opener` is Rule 09.1's 48 px row, one color, on Newsprint, with no tag, no padding of its own and no width | Rule 09.1 places that row near the top of a page that introduces the four pillars; the shell pads a flowing stage, and no width lets it fit every column
- D2-xxx | The opener wraps two and two after an arrow where the column is narrower than its 592 px line | Rule 09.1's own rows do the same there; its sizes and spacing stay as approved
- D2-xxx | `specimens_used` counts a chapter's opener | The identity build's guard then covers every specimen a chapter names

## Questions for Dustin

1. **The print L3.** Approve, by name, the print L3 at the masthead's proportion (`lockups/20261110_L3-Horizontal-Print-Master.svg`), the October master with its lockmark at 2.18 cap heights, for print and every width but the 282 px masthead? *Recommendation:* approve. L3 then has one proportion in every medium, the change touches nothing but the lockmark's size, and at L3's print minimum the lockmark stays over its own.
2. **The social card's sign-off.** Approve, by name, the sign-off on social cards at 96 px, the 48 px master drawn at exactly twice its size, with covers, posters and the masthead at 48 px? *Recommendation:* approve. Today's card passes the rule's test with 5 red pixels against 4, but a thumbnail saved as a JPEG after shrinking leaves none, and nearby widths already fall to 3. At 96 px the card passes at every width from 300 to 600 px and through the thumbnail path, with no new drawing, and the corners keep L3's proportion. The cost is a heavier corner and visible 2 px steps when the card is seen at full size. If you would rather keep 48 px, the risk stays as measured, and a real upload to each platform in Phase 3's applications would show whether any feed takes that path.

## For the main session and other owners

- **Board builder.** Both proposals' plates are in `work/handoffs/phase-2/stage-c-identity/`: the two HTML pages (self-contained apart from their PNGs in the same folder), their full-page captures at 1x and 2x, and the print proof PDF. Each page states the reason, shows the original and the proposal at actual size, and names the files.
- **Editor, round 1.** New reader text: Rule 08.2's "Feed test", "Feed test, dark card" and "Feed test, our card" rows and its builders sentence; `s-09-opener`'s alt. One gap the opener shows: Rule 09.1's specifications do not say that the 48 px row wraps after an arrow where the column is narrower than its line (about 592 px), from 48em to about 1,080 px screens. One clause in its "48 px row" row would cover it; I left the words as approved.
- **Engineer.** No shell change needed from me. Your opener contract works as written for a flowing specimen. The guide check fails one text item, "Remind me" in `s-11-15-correct`, at 4.17 to 1 at all four widths; it is chapter 11's specimen, and the token work in progress is the likely cause. For you or the systems designer.
- **Creative director.** CD-N12 is closed on the page; the feed margin and D2-482 wait for board C.
- **D2 numbers.** The routine calls carry D2-xxx for you to number.

## Tested

- The proofs' card drawn on Newsprint, White, Charcoal and Prussian at 1x in Chromium; the lockmark tile in each card against the master drawn alone, pixel for pixel.
- `_social()` on Newsprint against HEAD's function: the same markup.
- The light-node floors from the links-alone renders and the whole master, every width from 300 to 600 px, four Pillow filters.
- The light test's 70 against the links alone on Newsprint and White, the same range.
- The feed test at 500 and 360 px on all four grounds under four filters; through Chromium's `<img>` downscale; through JPEG at four qualities with and without chroma subsampling, before and after the reduction; at every width from 300 to 600 px; at every whole-pixel placement in a 60 px square on Newsprint and Charcoal.
- The 96 px sign-off captured on Newsprint and Charcoal and run through the same tests, with the thumbnail path at every fourth width.
- The print L3 files: the script's undo-and-compare against the October files; the plates at 1x and 2x and the print PDF at 300 dpi, measured.
- Every plate looked at in the captures; two caption errors found and fixed (the overlay's "the lockmark's center", which is its vertical center only, and figures printed to three decimals).
- The chain from the project folder, each with `python3 -I`: `apply_systems_ch11.py`, `stage_b_ch10_build.py --no-draw`, `stage_b_ch12_systems_build.py`, `promotion_identity.py specimens`, `guide_editor_build.py`, `stage_b_identity_ch01.py`: each exit 0. Diffs afterwards: my chapters 08 and 09, `manifest-identity.json` and the new `s-09-opener.html`, plus chapter 11's figures file's token version stamp.
- `guide_build.py --strict`, after a last full run of the chain on my finished code: exit 0, 0 warnings, 12 chapter files, 132 rules, 306 specimens, 6,812,035 bytes (the engineer's work in progress is in the page too).
- The opener in the built page at 1440, 1024 and 768 px at 1x, 390 and 360 px at 2x and 1440 px at 2x, with the device set to dark; chapter 09's first screen at 1440 by 900 and 390 by 844; Rule 09.1 and 09.2's 48 px rows at 1024, 1280 and 1440 px.
- My new reader text and the plates' text for em and en dashes and filler words: none.
- `guide_check.js --no-captures` at 1440, 1024, 390 and 360 px on a copy of the built page in my scratch folder, so no file in the board folder was written: 132 rules, 306 specimens, 1,101 same-page links, 8 failures, every one the same item at each width: "Remind me" in `s-11-15-correct`, chapter 11's specimen, at 4.17 to 1, with axe's matching color-contrast finding. None is in chapters 03, 04, 08 or 09 or the proofs. My work touches no chapter 11 file or token, so I take it to come from the token changes in progress; I did not confirm that by building without them.

## Not tested

- A real feed: no card was uploaded to any platform, and which platforms store a shrunk JPEG thumbnail is not checked here. The JPEG figures come from Pillow's encoder, not a platform's.
- Firefox, Safari, real phones and screens between 1x and 2x for the feed views; Chromium only.
- The print L3 and the 96 px sign-off on paper; the print proof was measured as a PDF, not printed.
- Screen readers by ear on the opener; its stage carries the alt as `role="img"`, as the shell gives every non-readable specimen.
- The 96 px sign-off on White and Prussian, and the dark test on White's neighbor surfaces beyond the four grounds.
- `stage_a_identity_q_measure.py`, `promotion_identity.py checks` and the board scripts were not rerun; my changes touch none of the drawings they measure.

## Change log

Created:
- `work/build/scripts/phase-2/stage_c_identity_round0.py`
- `work/build/assets/identity/lockups/20261110_L3-Horizontal-Print-Master.svg` (proposal, not in use)
- `work/build/assets/identity/prussian/20261110_L3-Horizontal-Print-Master-Prussian-White.svg` (proposal, not in use)
- `work/build/guide/specimens/s-09-opener.html` (generated)
- `work/handoffs/phase-2/20261110_Stage-C-Identity-Figures.json`
- `work/handoffs/phase-2/stage-c-identity/`: `20261110_Print-L3-Comparison.html`, `-1x.png`, `-2x.png`; `20261110_Print-L3-Comparison-Print.html` and `.pdf`; `20261110_Social-Sign-Off-Comparison.html`, `-1x.png`, `-2x.png`; eight `20261110_Social-Card-*-At-*.png` and sixteen `20261110_Sign-Off-*-8x.png` images the sign-off page shows
- `work/handoffs/phase-2/20261110_Stage-C-Identity-Round-0-Notes.md` (this file)

Modified:
- `work/build/scripts/phase-2/stage_a_identity_proofs.py`: `_social` takes a surface; Newsprint output unchanged
- `work/build/scripts/phase-2/stage_a_identity_chapters.py`: Rule 08.2's feed rows and builders sentence, `_feed_dark`, `specimens_used` counts an opener
- `work/build/scripts/phase-2/stage_a_identity_lib.py`: `FIGURES_STAGE_C`, and `figures` reads its `feed_dark` key
- `work/build/scripts/phase-2/stage_b_identity_ch09.py`: `s_09_opener` and the chapter's `"opener"` key
- `work/build/guide/chapters/08-lockmark.json`, `09-pillar-icons.json` and `work/build/guide/specimens/manifest-identity.json` (generated)

Rewritten by the chain, not my files: `work/handoffs/phase-2/20261110_Stage-B-Round-2-Ch11-Figures.json` (its token version stamp, 6.0.0-gate2.6 to 6.0.0-gate2.7, written by `apply_systems_ch11.py` after the engineer's token change); `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` and its build report, written by `guide_build.py --strict` as the task asks.

Scratch renders, captures and pages: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/67af6aec-b8e0-5b79-b000-c172e734e753/scratchpad/stage-c/identity/`.
